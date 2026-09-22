#!/usr/bin/env python3
"""Bounded synthetic arithmetic/format checks; no transport or physics gate."""

import argparse
import csv
import hashlib
from pathlib import Path
import platform
import subprocess
import tempfile

FLAGS = (
    "-std=f2008 -O0 -g -pedantic -Wall -Wextra -Werror "
    "-Wno-compare-reals -fcheck=all -ffp-contract=off -fno-fast-math"
).split()

# Only groups 1..3 have nonzero operators. Exact integer/quarter arithmetic,
# reverse KEYFLX, padded source-group-descending SCAT00, deliberately unusable
# self entries in SCAT00, signed self/off-group XS and signed LEAK1D64.
FIXTURE = r"""
program fixture
  use GANLIB
  use, intrinsic :: iso_c_binding, only: c_ptr
  use, intrinsic :: iso_fortran_env, only: real32,real64
  use, intrinsic :: ieee_arithmetic, only: ieee_value,ieee_quiet_nan
  implicit none
  integer,parameter :: np=3,ng=370,nr=132,ns=12,nu=144,nm=6
  type(c_ptr) :: root,a,tracks,fluxes,systems,libraries,track,flux,system,library
  type(c_ptr) :: macro,mg,sg,mi,si,fl,ql,sl
  integer :: p,g,i,m,h,state(40),mat(nr),key(nr),cur(ns),bc(ns),zone(nu)
  integer :: njj(nm),ijj(nm),ipos(nm)
  real(real32) :: volume(nr),weight(nu),alpha(6),total(0:nm),self(0:nm),used(0:nm),scat(31)
  real(real64) :: u(nu),q(nu),source(nu),leak(ng)
  character(len=32) :: mode
  call get_command_argument(1,mode)
  call LCMOP(root,'input.xsm',0,2,0)
  call LCMPTC(root,'SIGNATURE',12,'L_ARCHIVE   ')
  call LCMPUT(root,'LISTDIM',1,1,np)
  a=LCMDID(root,'SPOT-R64')
  call LCMPTC(a,'STATE',12,'RETURNED    ')
  call LCMPUT(a,'NPLANE',1,1,np)
  call LCMPUT(a,'EPOCH',1,1,8)
  tracks=LCMLID(root,'TRACK',np)
  fluxes=LCMLID(root,'FLUX',np)
  systems=LCMLID(root,'SYSTEM',np)
  libraries=LCMLID(root,'MICROLIB2',np)
  do p=1,np
    track=LCMDIL(tracks,p)
    flux=LCMDIL(fluxes,p)
    system=LCMDIL(systems,p)
    library=LCMDIL(libraries,p)
    call LCMPTC(track,'SIGNATURE',12,'L_TRACK     ')
    state=0
    state(1)=nr; state(2)=nu; state(4)=nm; state(5)=ns
    call LCMPUT(track,'STATE-VECTOR',40,1,state)
    do i=1,nr
      mat(i)=1+mod(i-1,nm)
      key(i)=nr+1-i
      volume(i)=real(1+mod(i,5),real32)
    enddo
    cur=[(nu+1-i,i=1,ns)]
    bc=[(i,i=1,ns)]
    if(mode=='bad_index') cur(1)=key(1)
    if(mode=='bad_material') mat(1)=7
    if(mode=='bad_bc') bc(1)=2
    zone(:nr)=mat
    zone(nr+1:)=[(-1-mod(i-1,6),i=1,ns)]
    weight(:nr)=volume
    weight(nr+1:)=2.0_real32
    alpha=1.0_real32
    call LCMPUT(track,'MATCOD',nr,1,mat)
    call LCMPUT(track,'KEYFLX',nr,1,key)
    call LCMPUT(track,'KEYFLX$ANIS',nr,1,key)
    call LCMPUT(track,'KEYCUR$MCCG',ns,1,cur)
    call LCMPUT(track,'BC-REFL+TRAN',ns,1,bc)
    call LCMPUT(track,'ICODE',6,1,[-1,-2,-3,-4,-5,-6])
    call LCMPUT(track,'NZON$MCCG',nu,1,zone)
    call LCMPUT(track,'VOLUME',nr,2,volume)
    call LCMPUT(track,'V$MCCG',nu,2,weight)
    call LCMPUT(track,'ALBEDO',6,2,alpha)
    call LCMPUT(system,'SPOT-L1-RAW',1,1,1)
    call LCMPUT(flux,'SPOT-FS-EQN',1,1,1)
    leak=0.0_real64
    leak(1:3)=[0.5_real64,-0.25_real64,0.0_real64]
    if(mode=='bad_leak_type') then
      call LCMPUT(flux,'LEAK1D64',ng,2,real(leak,real32))
    else
      call LCMPUT(flux,'LEAK1D64',ng,4,leak)
    endif
    a=LCMDID(flux,'SPOT-R64')
    call LCMPTC(a,'STATE',12,'SOLVED      ')
    call LCMPUT(a,'EPOCH',1,1,8)
    call LCMPUT(a,'RHO',1,4,0.75_real64)
    fl=LCMLID(a,'FLUX',ng)
    ql=LCMLID(a,'QFISS',ng)
    sl=LCMLID(a,'SOUR',ng)
    do g=1,ng
      u=1.0_real64
      q=0.0_real64
      if(g<=3) then
        do i=1,nr
          u(key(i))=real(p*8+i+g,real64)
          q(key(i))=real(2*p+i+2*g,real64)
        enddo
      endif
      source=q
      ! Legal terminal SOUR differs from QFISS; it must not enter the sum.
      source(key(1))=source(key(1))+42
      if(mode=='nan_flux'.and.g==1) u(1)=ieee_value(0.0_real64,ieee_quiet_nan)
      if(mode=='bad_flux_type'.and.g==1) then
        call LCMPDL(fl,g,nu,2,real(u,real32))
      else
        call LCMPDL(fl,g,nu,4,u)
      endif
      call LCMPDL(ql,g,nu,4,q)
      call LCMPDL(sl,g,nu,4,source)
    enddo
    if(mode=='missing_qfiss') call LCMDEL(a,'QFISS')
    macro=LCMDID(library,'MACROLIB')
    call LCMPTC(macro,'SIGNATURE',12,'L_MACROLIB  ')
    state=0; state(1)=ng; state(2)=nm
    call LCMPUT(macro,'STATE-VECTOR',40,1,state)
    mg=LCMLID(macro,'GROUP',ng)
    sg=LCMLID(system,'GROUP',ng)
    do g=1,ng
      mi=LCMDIL(mg,g)
      si=LCMDIL(sg,g)
      total=0.0_real32; self=0.0_real32; scat=999.0_real32
      njj=3; ijj=3; ipos=[(2+5*(m-1),m=1,nm)]
      do m=1,nm
        if(g<=3) then
          total(m)=real(4+m+g,real32)
          self(m)=real(m-2*g,real32)
        endif
        do h=1,3
          scat(ipos(m)+3-h)=0.0_real32
          if(g<=3) then
            scat(ipos(m)+3-h)=real(h+m-g,real32)
            if(h==g) scat(ipos(m)+3-h)=127.0_real32
          endif
        enddo
      enddo
      used=self
      if(mode=='bad_self'.and.g==1) used(1)=used(1)+1
      if(mode=='bad_scatter'.and.g==1) ipos(1)=31
      if(mode=='bad_group'.and.g==1) ijj(1)=2
      call LCMPUT(si,'DRAGON-TXSC',nm+1,2,total)
      call LCMPUT(si,'SPOT-S0-PHYS',nm+1,2,self)
      call LCMPUT(si,'DRAGON-S0XSC',nm+1,2,used)
      call LCMPUT(mi,'NJJS00',nm,1,njj)
      call LCMPUT(mi,'IJJS00',nm,1,ijj)
      call LCMPUT(mi,'IPOS00',nm,1,ipos)
      call LCMPUT(mi,'SCAT00',31,2,scat)
    enddo
  enddo
  call LCMCL(root,1)
end program fixture
"""

BAD = {
    "bad_index": "DUPLICATE FLUX/CURRENT INDEX",
    "bad_material": "INVALID MATERIAL MAP",
    "bad_bc": "REQUIRES IDENTITY WHITE BOUNDARIES",
    "bad_leak_type": "INVALID RECORD LENGTH/TYPE: LEAK1D64",
    "bad_flux_type": "AUTHORITY LIST MUST BE REAL64",
    "nan_flux": "NONFINITE REAL64 AUTHORITY FIELD",
    "missing_qfiss": "INVALID RECORD LENGTH/TYPE: QFISS",
    "bad_self": "SPOT-S0-PHYS MUST BE BITWISE DRAGON-S0XSC",
    "bad_scatter": "SCATTER PACKED INDEX INVALID",
    "bad_group": "SCATTER GROUP RANGE INVALID",
}


def run(command, work, check=True):
    return subprocess.run([str(x) for x in command], cwd=work, timeout=10,
                          capture_output=True, text=True, check=check)


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def expected(plane, group):
    c = s0 = off = z = q = scale = 0.0
    if group <= 3:
        for i in range(1, 133):
            material = 1 + (i - 1) % 6
            volume = 1 + i % 5
            flux = plane * 8 + i + group
            ci = volume * (4 + material + group) * flux
            si = volume * (material - 2 * group) * flux
            zi = volume * (0.5, -0.25, 0.0)[group - 1] * flux
            qi = volume * (2 * plane + i + 2 * group)
            # Integer formula is independent of the fixture's compressed layout.
            terms = [volume * (h + material - group) * (plane * 8 + i + h)
                     for h in (1, 2, 3) if h != group]
            c += ci
            s0 += si
            off += sum(terms)
            z += zi
            q += qi
            scale += abs(ci) + abs(si) + abs(zi) + abs(qi) + sum(map(abs, terms))
    removal = c - s0 - off
    residual = removal + z - q
    return dict(collision=c, self_scatter=s0, offgroup_scatter=off,
                net_removal=removal, axial_loss=z, frozen_fission=q,
                boundary_net=0.0, residual_components=residual,
                residual_local=residual, roundoff_difference=0.0,
                absolute_term_scale=scale)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", type=Path, help="use a previously built diagnostic host")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    root = here.parent.parent
    ganlib = root / "Ganlib/lib" / f"{platform.system()}_{platform.machine()}"
    with tempfile.TemporaryDirectory(prefix="d4a-balance-test-") as temporary:
        work = Path(temporary)
        host = args.host.resolve() if args.host else work / "diagnose"
        if not args.host:
            run(["gfortran", *FLAGS, "-I", ganlib / "modules",
                 here / "diagnose_d4a_radial_balance.f90", ganlib / "libGanlib.a",
                 "-lstdc++", "-o", host], work)
        source = work / "fixture.f90"
        source.write_text(FIXTURE)
        fixture = work / "fixture"
        run(["gfortran", *FLAGS, "-I", ganlib / "modules", source,
             ganlib / "libGanlib.a", "-lstdc++", "-o", fixture], work)
        for mode in ("good", *BAD):
            case = work / mode
            case.mkdir()
            run([fixture, mode], case)
            input_file = case / "input.xsm"
            before = hashlib.sha256(input_file.read_bytes()).digest()
            result = run([host, "input.xsm", "balance.csv"], case, check=False)
            require(hashlib.sha256(input_file.read_bytes()).digest() == before,
                    f"{mode}: input modified")
            output = case / "balance.csv"
            if mode != "good":
                require(result.returncode != 0 and BAD[mode] in result.stderr,
                        f"{mode}: unexpected result: {result.stdout}{result.stderr}")
                require(not output.exists(), f"{mode}: published output after rejection")
                print(f"{mode}: expected rejection; input unchanged")
                continue
            require(result.returncode == 0, result.stdout + result.stderr)
            rows = list(csv.DictReader(output.open()))
            require(len(rows) == 1110, "wrong row count")
            require([(int(r["plane"]), int(r["group"])) for r in rows] ==
                    [(p, g) for p in (1, 2, 3) for g in range(1, 371)], "wrong row order/coverage")
            for row in rows:
                wanted = expected(int(row["plane"]), int(row["group"]))
                for key, value in wanted.items():
                    require(float(row[key]) == value, f"exact reference mismatch: {key}: {row}")
                scale = wanted["absolute_term_scale"]
                if scale:
                    require(row["normalization_status"] == "defined", "missing defined status")
                    require(float(row["residual_over_scale"]) == wanted["residual_components"] / scale,
                            "normalized residual mismatch")
                else:
                    require(row["normalization_status"] == "zero_denominator" and
                            row["residual_over_scale"] == "undefined", "zero denominator not explicit")
            saved = output.read_bytes()
            repeat = run([host, "input.xsm", "balance.csv"], case, check=False)
            require(repeat.returncode != 0 and "REFUSING TO OVERWRITE" in repeat.stderr,
                    "overwrite was not rejected")
            require(output.read_bytes() == saved, "existing output changed")
            print("good: 1110 exact rows; padded descending off-group indices; signed leakage/XS;")
            print("      SOUR differs from QFISS; zero denominators explicit; input unchanged; overwrite rejected")
    print("D4A RADIAL BALANCE SYNTHETIC CHECKS COMPLETE; NO PHYSICS ACCEPTANCE")


if __name__ == "__main__":
    main()
