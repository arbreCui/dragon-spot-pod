"""
OpenMC continuous-energy model of the IRENA fissile assembly (full hex).

Mirrors the DRAGON-side rnr_assembly.py at
    /Users/wen/dragon-5.1/Dragon/irena_colorset_assembly_pin/assembly/rnr_assembly.py

Geometry (matches the GLOW lattice-box spec [-0.05, 0.45, 0.225] perp cm):
    - 8 surrounding rings + centre = 217 fuel pins (each: He_HOLE / FUEL_MOX
      / He_GAP / CLAD_AIM1 / Na around clad), SIDE = 0.61776479 cm.
    - Continuous EM10 wrapper of 4.5 mm perp thickness, with its inner face
      sitting 0.5 mm INSIDE glow's lattice envelope. The 0.5 mm clip is in
      the Na collar between the actual pin cells and the inscribed envelope
      hex — the 217 fuel/clad/gap/hole cylinders themselves are NOT clipped
      (glow's volume report confirms exact 217-pin fuel area).
    - Outer Na half-lame of 2.25 mm perp thickness (book IGE-407 Fig. 33:
      Espace inter-assemblage = 4.5 mm, half on each side of the wrapper).
    - Reflective BC on the assembly outer hex.

Boundary-condition pairing for OpenMC ↔ DRAGON comparison:
    - OpenMC reflective BC  ↔  DRAGON TSPC (specular)
    - OpenMC white BC       ↔  DRAGON TISO (isotropic)
    (do NOT compare OpenMC reflective to DRAGON TISO and vice versa.)

Fuel discretisation:
    - OpenMC here uses 1-zone MOX (CE doesn't need geometric self-shielding
      sub-zones). DRAGON uses 4-zone MOX with identical composition in all
      four sub-rings — the sub-zoning is purely so TONE can compute four
      independent self-shielded cross-sections.

Atom densities are ported line-by-line from rnr_cc.c2m + rnr_interpol.c2m
(same as the pincell port), extended with the EM10 wrapper material that
the pincell does not need.

The density-dilation formula carried over from rnr_cc.c2m is
    rho(T) = rho0 / (1 + alpha*(T-20))^3
using the corrected DRAGON density convention for bulk solid/liquid materials.
"""
from __future__ import annotations

import math
from pathlib import Path

import openmc


# -------------------------------------------------------------------- #
#  Inputs (verbatim from rnr_0burn.x2m)                                #
# -------------------------------------------------------------------- #
p_Pu, p_U = 0.21, 0.79

p_Pu38, p_Pu39, p_Pu40, p_Pu41, p_Pu42, p_Am = (
    0.0259, 0.552, 0.2585, 0.0727, 0.0787, 0.0122
)
p_U5, p_U8 = 0.002, 0.998

# AIM1 cladding mass fractions
p_Fe_AIM1, p_Cr_AIM1, p_Ni_AIM1, p_Mn_AIM1 = 0.6575, 0.145, 0.155, 0.015
p_Mo_AIM1, p_Si_AIM1, p_Ti_AIM1 = 0.015, 0.0085, 0.004

# EM10 wrapper mass fractions (book IGE-407 Fig. 21)
p_Fe_EM10, p_Cr_EM10, p_Ni_EM10, p_Mo_EM10 = 0.8908, 0.085, 0.005, 0.01
p_Mn_EM10, p_C_EM10, p_Si_EM10, p_Ti_EM10 = 0.005, 0.001, 0.003, 0.0002

T_comb, T_clad, T_Na = 750.0, 620.0, 475.0  # degC

# Pin cell dimensions (cm), 4-zone fuel matching rnr_assembly.py
SIDE = 0.61776479
R_HOLE = 0.11
R_FUEL_1 = 0.308712
R_FUEL_2 = 0.381084
R_FUEL_3 = 0.412536
R_FUEL_4 = 0.4225
R_GAP = 0.435
R_CLAD = 0.485

PIN_RINGS = 8  # surrounding rings; centre + 8 rings = 217 fuel pins

# Wrapper-box layer specification (perp thickness in cm, outward from
# glow's lattice envelope perp = (1.5N+1)*SIDE = bbox-min/2). Matches
# DRAGON GLOW's lat.build_lattice_box([-0.05, 0.45, 0.225]) call. The
# -0.05 is the "hack" that lets a 217-pin / 4.5 mm wrapper / 17.5 cm
# pitch geometry close — it pushes the wrapper inner 0.5 mm perp inside
# the glow envelope, which clips the 6 ring-8 corner pins along the
# lattice apothem direction (they become EM10 instead of fuel).
LAYER_PERP = [-0.05, 0.45, 0.225]


# -------------------------------------------------------------------- #
#  rnr_interpol.c2m port — piecewise-linear dilation coefficients      #
# -------------------------------------------------------------------- #
def _interp(T, table):
    for T_lo, T_hi, y_lo, y_hi in table:
        if T <= T_hi:
            slope = (y_hi - y_lo) / (T_hi - T_lo)
            inter = (T_hi * y_lo - T_lo * y_hi) / (T_hi - T_lo)
            return slope * T + inter
    raise ValueError(f"out of interpolation domain: T={T}")


_TABLE_comb = [
    (0, 100, 0.0, 1.0578e-5), (100, 200, 1.0578e-5, 1.0577e-5),
    (200, 300, 1.0577e-5, 1.0602e-5), (300, 400, 1.0602e-5, 1.0640e-5),
    (400, 500, 1.0640e-5, 1.0690e-5), (500, 600, 1.0690e-5, 1.0750e-5),
    (600, 700, 1.0750e-5, 1.0803e-5), (700, 800, 1.0803e-5, 1.0888e-5),
    (800, 900, 1.0888e-5, 1.0990e-5), (900, 1000, 1.0990e-5, 1.1111e-5),
    (1000, 1100, 1.1111e-5, 1.1254e-5), (1100, 1200, 1.1254e-5, 1.1420e-5),
]
_TABLE_AIM1 = [
    (0, 100, 0.0, 1.6400e-5), (100, 200, 1.6400e-5, 1.6900e-5),
    (200, 300, 1.6900e-5, 1.7350e-5), (300, 400, 1.7350e-5, 1.7800e-5),
    (400, 500, 1.7800e-5, 1.8200e-5), (500, 600, 1.8200e-5, 1.8500e-5),
    (600, 700, 1.8500e-5, 1.8800e-5), (700, 800, 1.8800e-5, 1.9000e-5),
]
_TABLE_EM10 = [  # rnr_interpol.c2m uses T_Na for EM10 (T_box = T_Na hypothesis)
    (0, 100, 0.0, 1.0620e-5), (100, 200, 1.0620e-5, 1.1060e-5),
    (200, 300, 1.1060e-5, 1.1460e-5), (300, 400, 1.1460e-5, 1.1830e-5),
    (400, 500, 1.1830e-5, 1.2170e-5), (500, 600, 1.2170e-5, 1.2480e-5),
    (600, 700, 1.2480e-5, 1.2750e-5), (700, 750, 1.2750e-5, 1.2880e-5),
    (750, 800, 1.2880e-5, 1.2990e-5),
]
_TABLE_na = [
    (0, 100, 0.0, 8.6560e-5), (100, 200, 8.6560e-5, 8.9030e-5),
    (200, 300, 8.9030e-5, 9.1380e-5), (300, 400, 9.1380e-5, 9.3910e-5),
    (400, 500, 9.3910e-5, 9.6690e-5), (500, 600, 9.6690e-5, 9.9540e-5),
    (600, 700, 9.9540e-5, 1.0270e-4), (700, 800, 1.0270e-4, 1.0590e-4),
    (800, 900, 1.0590e-4, 1.0920e-4), (900, 1000, 1.0920e-4, 1.1260e-4),
    (1000, 1100, 1.1260e-4, 1.1620e-4), (1100, 1200, 1.1620e-4, 1.1980e-4),
    (1200, 1300, 1.1980e-4, 1.2350e-4), (1300, 2300, 1.2350e-4, 1.2351e-4),
]

a_comb = _interp(T_comb, _TABLE_comb)
a_AIM1 = _interp(T_clad, _TABLE_AIM1)
a_EM10 = _interp(T_Na,   _TABLE_EM10)  # EM10 uses T_Na
a_na   = _interp(T_Na,   _TABLE_na)


# -------------------------------------------------------------------- #
#  rnr_cc.c2m port — atom densities (atoms/(barn*cm))                  #
# -------------------------------------------------------------------- #
p_Fe54, p_Fe56, p_Fe57, p_Fe58 = 0.058, 0.9172, 0.022, 0.0028
p_Cr50, p_Cr52, p_Cr53, p_Cr54 = 0.0434, 0.8381, 0.0949, 0.0236
p_Ni58, p_Ni60, p_Ni61, p_Ni62, p_Ni64 = 0.6827, 0.261, 0.0113, 0.0359, 0.0091
p_Mo92, p_Mo94, p_Mo95, p_Mo96, p_Mo97, p_Mo98, p_Mo100 = (
    0.148, 0.091, 0.159, 0.167, 0.095, 0.244, 0.096
)

A_AVOGADRO = 6.022094e-1  # /1e24 -> atoms/(barn*cm)

O_M_MOX = 1.98
fuel_compaction = 0.955

M_U_HM = p_U5 * 235.0439231 + p_U8 * 238.0507826
M_Pu_HM = (p_Pu38 * 238.0495534 + p_Pu39 * 239.0521565 + p_Pu40 * 240.0538075
           + p_Pu41 * 241.0568453 + p_Pu42 * 242.0587368 + p_Am * 241.0568229)
M_U = M_U_HM + O_M_MOX * 15.9949
M_Pu = M_Pu_HM + O_M_MOX * 15.9949
M_Fe = p_Fe54 * 53.9396148 + p_Fe56 * 55.9349421 + p_Fe57 * 56.9353987 + p_Fe58 * 57.9332805
M_Cr = p_Cr50 * 49.9460496 + p_Cr52 * 51.9405119 + p_Cr53 * 52.9406538 + p_Cr54 * 53.9388849
M_Ni = (p_Ni58 * 57.9353479 + p_Ni60 * 59.9307906 + p_Ni61 * 60.9310604
        + p_Ni62 * 61.9283488 + p_Ni64 * 63.9279696)
M_Mn = 54.938045
M_Mo = (p_Mo92 * 91.906824 + p_Mo94 * 93.905090 + p_Mo95 * 94.905888
        + p_Mo96 * 95.904668 + p_Mo97 * 96.905969 + p_Mo98 * 97.905355
        + p_Mo100 * 99.907252)
M_Si = 28.0855
M_Ti = 47.867
M_C = 12.0107

rho0_MOX =  11.46 * fuel_compaction
rho0_AIM1 = 7.95
rho0_EM10 = 7.76
rho0_Na = 0.971
rho0_He = 0.125

coeff_1 = 1.0 + a_comb * (T_comb - 20.0)
coeff_2 = coeff_1 ** 3
rho_MOX = rho0_MOX / coeff_2

coeff_3 = 1.0 + a_AIM1 * (T_clad - 20.0)
coeff_4 = coeff_3 ** 3
rho_AIM1 = rho0_AIM1 / coeff_4

coeff_7 = 1.0 + a_EM10 * (T_Na - 20.0)
coeff_8 = coeff_7 ** 3
rho_EM10 = rho0_EM10 / coeff_8

coeff_11 = 1.0 + a_na * (T_Na - 20.0)
coeff_12 = coeff_11 ** 3
rho_Na = rho0_Na / coeff_12

coeff_13 = 1.0 - a_comb * (T_comb - 20.0)
rho_He_1 = rho0_He / (coeff_1 * coeff_13 ** 2)

coeff_14 = 1.0 - a_AIM1 * (T_clad - 20.0)
rho_He_2 = rho0_He / (coeff_1 ** 3 * coeff_14 ** 2)


# MOX fuel
ox_corr = 1.0 + O_M_MOX * 15.9949 * (p_U / M_U_HM + p_Pu / M_Pu_HM)
rho_HM = rho_MOX / ox_corr
N_MOX = rho_HM * p_Pu * A_AVOGADRO / M_Pu_HM
N_U = rho_HM * p_U * A_AVOGADRO / M_U_HM
N_U5, N_U8 = p_U5 * N_U, p_U8 * N_U
N_Pu38, N_Pu39, N_Pu40, N_Pu41, N_Pu42 = (
    p_Pu38 * N_MOX, p_Pu39 * N_MOX, p_Pu40 * N_MOX, p_Pu41 * N_MOX, p_Pu42 * N_MOX
)
N_Am = p_Am * N_MOX
N_O = O_M_MOX * N_U + O_M_MOX * N_MOX

# AIM1 cladding
_n_AIM1 = lambda p, M: p * rho_AIM1 * A_AVOGADRO / M
N_Fe_AIM1, N_Cr_AIM1, N_Ni_AIM1 = _n_AIM1(p_Fe_AIM1, M_Fe), _n_AIM1(p_Cr_AIM1, M_Cr), _n_AIM1(p_Ni_AIM1, M_Ni)
N_Mn_AIM1, N_Mo_AIM1, N_Si_AIM1, N_Ti_AIM1 = (
    _n_AIM1(p_Mn_AIM1, M_Mn), _n_AIM1(p_Mo_AIM1, M_Mo), _n_AIM1(p_Si_AIM1, M_Si), _n_AIM1(p_Ti_AIM1, M_Ti)
)

# EM10 wrapper
_n_EM10 = lambda p, M: p * rho_EM10 * A_AVOGADRO / M
N_Fe_EM10, N_Cr_EM10, N_Ni_EM10 = _n_EM10(p_Fe_EM10, M_Fe), _n_EM10(p_Cr_EM10, M_Cr), _n_EM10(p_Ni_EM10, M_Ni)
N_Mn_EM10, N_Mo_EM10, N_Si_EM10, N_Ti_EM10 = (
    _n_EM10(p_Mn_EM10, M_Mn), _n_EM10(p_Mo_EM10, M_Mo), _n_EM10(p_Si_EM10, M_Si), _n_EM10(p_Ti_EM10, M_Ti)
)
N_C_EM10 = p_C_EM10 * rho_EM10 * A_AVOGADRO / M_C

# Sodium and helium
N_Na = rho_Na * A_AVOGADRO / 22.98976928
N_He_1 = rho_He_1 * A_AVOGADRO / 4.002602
N_He_2 = rho_He_2 * A_AVOGADRO / 4.002602


# -------------------------------------------------------------------- #
#  OpenMC model                                                        #
# -------------------------------------------------------------------- #
def _ck(T_celsius):
    return T_celsius + 273.15


def _add_isotopes_mass_weighted(material, element_fraction_in_steel, M_element,
                                rho_steel, isotope_fractions):
    """Add isotopes of one element to a steel material, with atom densities
    computed from steel rho × mass fraction in steel × isotope fraction."""
    N_element = element_fraction_in_steel * rho_steel * A_AVOGADRO / M_element
    for iso, frac in isotope_fractions:
        material.add_nuclide(iso, frac * N_element)


def make_materials():
    fuel = openmc.Material(name="FUEL_MOX")
    fuel.add_nuclide("U235",  N_U5)
    fuel.add_nuclide("U238",  N_U8)
    fuel.add_nuclide("Pu238", N_Pu38)
    fuel.add_nuclide("Pu239", N_Pu39)
    fuel.add_nuclide("Pu240", N_Pu40)
    fuel.add_nuclide("Pu241", N_Pu41)
    fuel.add_nuclide("Pu242", N_Pu42)
    fuel.add_nuclide("Am241", N_Am)
    fuel.add_nuclide("O16",   N_O)
    fuel.set_density("sum")
    fuel.temperature = _ck(T_comb)

    he_hole = openmc.Material(name="He_HOLE")
    he_hole.add_nuclide("He4", N_He_1)
    he_hole.set_density("sum")
    he_hole.temperature = _ck(T_comb)

    he_gap = openmc.Material(name="He_GAP")
    he_gap.add_nuclide("He4", N_He_2)
    he_gap.set_density("sum")
    he_gap.temperature = _ck(T_clad)

    clad = openmc.Material(name="CLAD_AIM1")
    _add_isotopes_mass_weighted(clad, p_Fe_AIM1, M_Fe, rho_AIM1,
        [("Fe54", p_Fe54), ("Fe56", p_Fe56), ("Fe57", p_Fe57), ("Fe58", p_Fe58)])
    _add_isotopes_mass_weighted(clad, p_Cr_AIM1, M_Cr, rho_AIM1,
        [("Cr50", p_Cr50), ("Cr52", p_Cr52), ("Cr53", p_Cr53), ("Cr54", p_Cr54)])
    _add_isotopes_mass_weighted(clad, p_Ni_AIM1, M_Ni, rho_AIM1,
        [("Ni58", p_Ni58), ("Ni60", p_Ni60), ("Ni61", p_Ni61),
         ("Ni62", p_Ni62), ("Ni64", p_Ni64)])
    _add_isotopes_mass_weighted(clad, p_Mo_AIM1, M_Mo, rho_AIM1,
        [("Mo92", p_Mo92), ("Mo94", p_Mo94), ("Mo95", p_Mo95),
         ("Mo96", p_Mo96), ("Mo97", p_Mo97), ("Mo98", p_Mo98), ("Mo100", p_Mo100)])
    clad.add_nuclide("Mn55", N_Mn_AIM1)
    clad.add_nuclide("Si28", N_Si_AIM1)
    clad.add_nuclide("Ti48", N_Ti_AIM1)
    clad.set_density("sum")
    clad.temperature = _ck(T_clad)

    em10 = openmc.Material(name="BOX_EM10")
    _add_isotopes_mass_weighted(em10, p_Fe_EM10, M_Fe, rho_EM10,
        [("Fe54", p_Fe54), ("Fe56", p_Fe56), ("Fe57", p_Fe57), ("Fe58", p_Fe58)])
    _add_isotopes_mass_weighted(em10, p_Cr_EM10, M_Cr, rho_EM10,
        [("Cr50", p_Cr50), ("Cr52", p_Cr52), ("Cr53", p_Cr53), ("Cr54", p_Cr54)])
    _add_isotopes_mass_weighted(em10, p_Ni_EM10, M_Ni, rho_EM10,
        [("Ni58", p_Ni58), ("Ni60", p_Ni60), ("Ni61", p_Ni61),
         ("Ni62", p_Ni62), ("Ni64", p_Ni64)])
    _add_isotopes_mass_weighted(em10, p_Mo_EM10, M_Mo, rho_EM10,
        [("Mo92", p_Mo92), ("Mo94", p_Mo94), ("Mo95", p_Mo95),
         ("Mo96", p_Mo96), ("Mo97", p_Mo97), ("Mo98", p_Mo98), ("Mo100", p_Mo100)])
    em10.add_nuclide("Mn55", N_Mn_EM10)
    em10.add_nuclide("C12",  N_C_EM10)
    em10.add_nuclide("Si28", N_Si_EM10)
    em10.add_nuclide("Ti48", N_Ti_EM10)
    em10.set_density("sum")
    em10.temperature = _ck(T_Na)  # rnr_cc hypothesis: T_box = T_Na

    coolant = openmc.Material(name="COOLANT_Na")
    coolant.add_nuclide("Na23", N_Na)
    coolant.set_density("sum")
    coolant.temperature = _ck(T_Na)

    return openmc.Materials([fuel, he_hole, he_gap, clad, em10, coolant]), {
        "fuel": fuel, "he_hole": he_hole, "he_gap": he_gap,
        "clad": clad, "em10": em10, "coolant": coolant,
    }


def make_pin_universe(mats):
    """Build one fuel-pin universe (5 concentric cylinders + Na outside clad).
    The hex boundary of the pin cell is handled by the enclosing HexLattice."""
    s_hole = openmc.ZCylinder(r=R_HOLE)
    s_fuel = openmc.ZCylinder(r=R_FUEL_4)
    s_gap  = openmc.ZCylinder(r=R_GAP)
    s_clad = openmc.ZCylinder(r=R_CLAD)

    c_hole = openmc.Cell(fill=mats["he_hole"], region=-s_hole,             name="pin_hole")
    c_fuel = openmc.Cell(fill=mats["fuel"],    region=+s_hole & -s_fuel,    name="pin_fuel")
    c_gap  = openmc.Cell(fill=mats["he_gap"],  region=+s_fuel & -s_gap,     name="pin_gap")
    c_clad = openmc.Cell(fill=mats["clad"],    region=+s_gap  & -s_clad,    name="pin_clad")
    c_cool = openmc.Cell(fill=mats["coolant"], region=+s_clad,              name="pin_outer")
    return openmc.Universe(cells=[c_hole, c_fuel, c_gap, c_clad, c_cool])


def _hex_apothem_perp_glow(pin_rings, side):
    """Glow's lattice envelope apothem: half of the lattice bbox in vertex
    direction (= the smaller bbox dimension for an N-ring lattice of pins
    with edge=side, since pins are flat-top after pin.rotate(90))."""
    p = side * math.sqrt(3.0)        # pin pitch (F2F)
    return pin_rings * p * math.cos(math.pi / 6.0) + side


def _lattice_apothem_perp(pin_rings, side):
    """Actual perpendicular apothem of an N-ring 'y'-orient hex pin lattice
    in the apothem direction (= max y extent for flat-top lattice).

    For a lattice with N surrounding rings of pins + centre, the topmost pin
    centre is at distance N × pin_pitch from origin (along apothem direction).
    Adding the pin's own apothem gives the top flat position:
        y_top = N × p + p/2 = (2N+1) × p / 2 = (2N+1) × side × sin60°
    """
    return (2 * pin_rings + 1) * side * math.sin(math.pi / 3.0)


def make_geometry(pin_universe, mats):
    pitch = SIDE * math.sqrt(3.0)    # 1.07 cm

    # Hex lattice with 8 surrounding rings + centre = 217 pin universes.
    # orientation 'y' = flat-top (matches GLOW after pin.rotate(90)).
    lat = openmc.HexLattice(name="assembly_lattice")
    lat.center = (0.0, 0.0)
    lat.pitch = (pitch,)
    lat.orientation = "y"
    lat.universes = [
        [pin_universe] * (6 * k) if k > 0 else [pin_universe]
        for k in range(PIN_RINGS, -1, -1)   # outer ring first
    ]
    # outer fill (positions outside the explicit ring count): pure Na
    outer_na_univ = openmc.Universe(cells=[
        openmc.Cell(fill=mats["coolant"], name="lat_outer_na")
    ])
    lat.outer = outer_na_univ

    # Lattice-box layer boundaries (perp apothem of each hex), accumulated
    # outward from glow's lattice envelope (= bbox-min/2, NOT the lattice's
    # actual apothem-direction extent). This matches DRAGON GLOW's
    # build_lattice_box convention exactly:
    sin60 = math.sin(math.pi / 3.0)
    perp = [_hex_apothem_perp_glow(PIN_RINGS, SIDE)]   # 8.0309 cm
    for p_layer in LAYER_PERP:
        perp.append(perp[-1] + p_layer)
    # perp = [lat_envelope, wrapper_inner, wrapper_outer, assembly_outer]
    # In edge_length units for OpenMC's HexagonalPrism: edge = perp / sin60
    edge_inner = perp[1] / sin60
    edge_outer = perp[2] / sin60
    edge_asm   = perp[3] / sin60

    # Wrapper / assembly hexes use the SAME orientation ('y' = flat-top) as
    # the lattice, matching glow's default Hexagon orientation. Edge lengths
    # are derived from perp apothems via E = perp / sin(60°). The wrapper
    # inner sits at perp 7.981 cm (= glow envelope 8.031 − 0.05), inside
    # the lattice envelope's Na collar; the 217 fuel/clad/gap/hole cylinders
    # remain geometrically complete — the lattice's pin cells are not
    # clipped, only the outer Na "bulge" between actual pins and the
    # inscribed envelope hex is replaced by EM10 wrapper material.
    wrap_inner = openmc.model.HexagonalPrism(edge_length=edge_inner, orientation="y")
    wrap_outer = openmc.model.HexagonalPrism(edge_length=edge_outer, orientation="y")
    asm_outer  = openmc.model.HexagonalPrism(edge_length=edge_asm,   orientation="y",
                                             boundary_type="white")

    z_lo = openmc.ZPlane(z0=-50.0, boundary_type="reflective")
    z_hi = openmc.ZPlane(z0=+50.0, boundary_type="reflective")

    # Lattice region is the interior of wrap_inner — the wrapper boundary
    # clips lattice cells where they extend past it (matches DRAGON's
    # "-0.05 perp" inner Na layer where the wrapper cuts into outer pins).
    c_lat   = openmc.Cell(fill=lat, region=-wrap_inner & +z_lo & -z_hi, name="lattice")
    c_wrap  = openmc.Cell(fill=mats["em10"],
                          region=+wrap_inner & -wrap_outer & +z_lo & -z_hi,
                          name="wrapper_EM10")
    c_outer = openmc.Cell(fill=mats["coolant"],
                          region=+wrap_outer & -asm_outer & +z_lo & -z_hi,
                          name="outer_Na_lame")

    geom = openmc.Geometry([c_lat, c_wrap, c_outer])
    geom._lattice_envelope_perp = perp[0]   # stash for diagnostics
    geom._boundary_perp = perp
    return geom


def make_settings():
    s = openmc.Settings()
    s.batches = 250
    s.inactive = 50
    s.particles = 20_000
    s.run_mode = "eigenvalue"
    s.temperature = {"method": "interpolation", "tolerance": 1000}
    # Source: uniform in the fuel annulus of a single pin near the centre.
    src = openmc.IndependentSource()
    src.space = openmc.stats.CylindricalIndependent(
        r=openmc.stats.Uniform(R_HOLE, R_FUEL_4),
        phi=openmc.stats.Uniform(0.0, 2 * math.pi),
        z=openmc.stats.Uniform(-49.0, 49.0),
    )
    src.energy = openmc.stats.Watt()
    s.source = src
    return s


def main():
    out = Path(__file__).resolve().parent
    materials, mats = make_materials()
    pin_universe = make_pin_universe(mats)
    geometry = make_geometry(pin_universe, mats)
    settings = make_settings()

    materials.export_to_xml(out / "materials.xml")
    geometry.export_to_xml(out / "geometry.xml")
    settings.export_to_xml(out / "settings.xml")

    sin60 = math.sin(math.pi / 3.0)
    print(f"a_comb={a_comb:.4e}  a_AIM1={a_AIM1:.4e}  a_EM10={a_EM10:.4e}  a_na={a_na:.4e}")
    print(f"rho_MOX={rho_MOX:.4f}  rho_AIM1={rho_AIM1:.4f}  rho_EM10={rho_EM10:.4f}  rho_Na={rho_Na:.4f}")
    print(f"N_U5={N_U5:.4e} N_U8={N_U8:.4e} N_Pu39={N_Pu39:.4e} N_Fe56_EM10={p_Fe_EM10*p_Fe56*rho_EM10*A_AVOGADRO/M_Fe:.4e}")
    print(f"lattice envelope perp = {geometry._lattice_envelope_perp:.4f} cm")
    print(f"boundary perps (cm)   : {[round(p, 4) for p in geometry._boundary_perp]}")
    print(f"boundary edges (cm)   : {[round(p/sin60, 4) for p in geometry._boundary_perp]}")

    openmc.run(cwd=str(out))


if __name__ == "__main__":
    main()
