"""Pure source patch for the recovered SPOASM production baseline.

Only anisotropic SPOT/POD assembly changes. The scalar radial solver,
its transport correction and the radial feedback expression are untouched.
No file access, compilation, controls or transport occurs at import.
"""
import hashlib

BASELINE_REVISION = '299546c405a47f7e3a7f75af54d392492d649781'
BASELINE_SHA = '25435d9be70540c094346452b063c90ef3f212e905a6f57a949504fb2f7e8d26'
BASELINE_OBJECT_SHA = '8a5fbf4dc7395710c2b3aa4c33e153d54f15acd87a50becdb8eb26dae0fca298'
LIBRARY_SHA = '954ed8568c59fdfc3ee566d027abac35c7a1469436afb0b147e4db7a7f28a1d9'
PREFIX = 'SPOASM AXIAL PN: '
NEGATIVES = {
    'ntot_length': PREFIX+'INVALID NTOT0 RECORD.',
    'ntot_type': PREFIX+'INVALID NTOT0 RECORD.',
    'sigw1_length': PREFIX+'INVALID SIGW RECORD.',
    'sigw2_missing': PREFIX+'INVALID SIGW RECORD.',
    'sigw2_type': PREFIX+'INVALID SIGW RECORD.',
    'ntot_nonfinite': PREFIX+'NON-FINITE PHYSICAL XS.',
    'sigw1_nonfinite': PREFIX+'NON-FINITE PHYSICAL XS.',
    'requested_order': PREFIX+'INCOMPLETE MACRO ANGULAR ORDER.',
    'moment_total_order': PREFIX+'UNSUPPORTED MOMENT-DEPENDENT TOTAL.',
    'radial_length': PREFIX+'INVALID RADIAL S0XSC RECORD.',
    'radial_type': PREFIX+'INVALID RADIAL S0XSC RECORD.',
}
DECLARATION_ANCHOR = '      TYPE(C_PTR) JPBASIS,KPBASIS\n'
DECLARATIONS = ('      TYPE(C_PTR) JPMACAX,KPMACAX\n'
                '      CHARACTER AXCAN*2\n')
MACRO_ANCHOR = '      NANIS=IPAR(3)\n'
MACRO_GUARD = ('      IF(ISCAT.GT.1) THEN\n'
 '*       STATE(10)=NW: THIS NTOT0 PATH SUPPORTS ONLY NW=0.\n'
 '*       STATE(6) IS THE LIBRARY TRANC OPTION, NOT A CLAIM THAT\n'
 '*       THE RAW NTOT0/SIGW RECORDS ARE ALREADY CORRECTED.\n'
 '        IF(NANIS.NE.ISCAT) CALL XABORT(\n'
 "     1    'SPOASM AXIAL PN: INCOMPLETE MACRO ANGULAR ORDER.')\n"
 '        IF(IPAR(10).NE.0) CALL XABORT(\n'
 "     1    'SPOASM AXIAL PN: UNSUPPORTED MOMENT-DEPENDENT TOTAL.')\n"
 '      ENDIF\n')
ZERO_ANCHOR = '      SXSC=0.0\n'
PHYSICAL_READ = (
 '*     AXIAL PN USES UNCORRECTED PHYSICAL MACROLIB MOMENTS.\n'
 '*     RADIAL TRANSPORT-CORRECTED P0 IS STILL USED ONLY FOR RADIAL R.\n'
 '      IF(ISCAT.GT.1) THEN\n'
 "        CALL LCMLEN(IPMACR,'GROUP',ILONG,ITYLCM)\n"
 '        IF((ILONG.NE.NGRP).OR.(ITYLCM.NE.10)) CALL XABORT(\n'
 "     1    'SPOASM AXIAL PN: INVALID MACRO GROUP LIST.')\n"
 "        JPMACAX=LCMGID(IPMACR,'GROUP')\n"
 '        DO IGR=1,NGRP\n'
 '          KPMACAX=LCMGIL(JPMACAX,IGR)\n'
 "          CALL LCMLEN(KPMACAX,'NTOT0',ILONG,ITYLCM)\n"
 '          IF((ILONG.NE.MAXMIX).OR.(ITYLCM.NE.2)) CALL XABORT(\n'
 "     1      'SPOASM AXIAL PN: INVALID NTOT0 RECORD.')\n"
 "          CALL LCMGET(KPMACAX,'NTOT0',TXSC(1,IGR))\n"
 '          DO IL=1,NANIS\n'
 "            WRITE(AXCAN,'(I2.2)') IL-1\n"
 "            CALL LCMLEN(KPMACAX,'SIGW'//AXCAN,ILONG,ITYLCM)\n"
 '            IF((ILONG.NE.MAXMIX).OR.(ITYLCM.NE.2)) CALL XABORT(\n'
 "     1        'SPOASM AXIAL PN: INVALID SIGW RECORD.')\n"
 "            CALL LCMGET(KPMACAX,'SIGW'//AXCAN,SXSC(1,IL,IGR))\n"
 '          ENDDO\n'
 '          IF(ANY(.NOT.IEEE_IS_FINITE(TXSC(:,IGR))).OR.\n'
 '     1       ANY(.NOT.IEEE_IS_FINITE(SXSC(:,:,IGR)))) CALL XABORT(\n'
 "     2      'SPOASM AXIAL PN: NON-FINITE PHYSICAL XS.')\n"
 '        ENDDO\n'
 '      ENDIF\n')
RADIAL_GET = "          CALL LCMGET(MPSNAP,'DRAGON-S0XSC',SXSC2D)\n"
RADIAL_GUARD = (
 '          IF(ISCAT.GT.1) THEN\n'
 "            CALL LCMLEN(MPSNAP,'DRAGON-S0XSC',ILONG,ITYLCM)\n"
 '            IF((ILONG.NE.NMIX2D+1).OR.(ITYLCM.NE.2))\n'
 '     1        CALL XABORT(\n'
 "     2        'SPOASM AXIAL PN: INVALID RADIAL S0XSC RECORD.')\n"
 '          ENDIF\n')
COPY_BLOCK = (
 '          IF(ISNAP.EQ.1) THEN\n'
 '            TXSC(0,IGR)=TXSC2D(0)\n'
 '            SXSC(0,:NANIS,IGR)=SXSC2D(0,:NANIS)\n'
 '          ENDIF\n'
 '          DO IBM=1,NMIX2D\n'
 '            IMAT=(ISNAP-1)*NMIX2D+IBM\n'
 '            TXSC(IMAT,IGR)=TXSC2D(IBM)\n'
 '            SXSC(IMAT,:NANIS,IGR)=SXSC2D(IBM,:NANIS)\n'
 '          ENDDO\n')
SCALAR_COPY = '          IF(ISCAT.EQ.1) THEN\n'+COPY_BLOCK+'          ENDIF\n'


def sha(source):
    return hashlib.sha256(source.encode()).hexdigest()


def replace_once(source, old, new):
    if source.count(old) != 1:
        raise ValueError('recovered baseline has missing/duplicate exact patch anchor')
    return source.replace(old,new,1)


def patch_source(original):
    if sha(original) != BASELINE_SHA:
        raise ValueError('the real recovered Git baseline is mandatory; current dirty source is forbidden')
    changed=original
    changes=[(DECLARATION_ANCHOR,DECLARATION_ANCHOR+DECLARATIONS),
             (MACRO_ANCHOR,MACRO_ANCHOR+MACRO_GUARD),
             (ZERO_ANCHOR,ZERO_ANCHOR+PHYSICAL_READ),
             (RADIAL_GET,RADIAL_GUARD+RADIAL_GET),(COPY_BLOCK,SCALAR_COPY)]
    for old,new in changes: changed=replace_once(changed,old,new)
    restored=changed
    for old,new in reversed(changes):restored=replace_once(restored,new,old)
    if restored != original:
        raise ValueError('complete source inverse restoration failed')
    reference=replace_once(original,'      SUBROUTINE SPOASM(', '      SUBROUTINE SPOASM_BASELINE_REBUILT(')
    unit=replace_once(changed,'      SUBROUTINE SPOASM(', '      SUBROUTINE SPOASM_PHYSICAL_UNIT(')
    # R and its source-selection, precision, leakage, normalization, POD and
    # output recipes are not changed. Only the upstream T/S assignment differs.
    return dict(production_source=changed,reference_source=reference,unit_source=unit,
        proof=dict(schema='AXMAT_SPOASM_PHYSICAL_ANGULAR_SOURCE_PATCH_V1',
            original_source_sha256=BASELINE_SHA,production_source_sha256=sha(changed),
            original_object_sha256=BASELINE_OBJECT_SHA,original_library_sha256=LIBRARY_SHA,
            exact_inverse_source_restoration=True,exact_patch_regions=5,
            scalar_branch_original_statement_bytes_preserved=True,
            radial_P0_solver_and_R_formula_source_bytes_preserved=True,
            macro_legendre_coefficients_copied_without_extra_2l_plus_1=True,
            original_radial_transport_correction_not_removed=True,
            supported_macro_total_order_NW=0,macro_TRANC_option_not_interpreted_as_raw_XS_correction=True,
            anisotropic_axial_T_and_all_self_Pn_from_physical_macrolib=True,
            temporary_radial_higher_tail_never_consumed_by_anisotropic_axis=True,
            baseline_higher_tail_is_undefined_and_not_equivalence_target=True,
            original_object_full_source_byte_reproduction_claimed=False,
            controls_executed=False,transport_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False))


def verify_sources(original,production,reference,unit):
    expected=patch_source(original)
    if (production,reference,unit) != tuple(expected[k] for k in
            ('production_source','reference_source','unit_source')):
        raise ValueError('actual emitted sources differ from full inverse patch')
    return expected['proof']


def control_contract():
    return dict(schema='AXMAT_SPOASM_PHYSICAL_ANGULAR_CONTROL_CONTRACT_V1',
        positive_fixtures=[dict(name=f'{kind}370_{precision}',groups=370,radial_regions=8,
            radial_unknowns=14,axial_cells=48,axial_unknowns=1800,materials=24,
            radial_materials=8,snapshots=3,sn=32,rank=1,
            scat=3 if kind=='physical' else 1,real64_authority=precision==64)
            for kind in ('physical','scalar') for precision in (64,32)],
        positive_args=['positive'],negative_cases=[dict(name=k,args=['negative',k],
            expected_message=v) for k,v in NEGATIVES.items()],
        raw_before_numeric_gates=True,all_groups=list(range(1,371)),
        actual_archive_baseline_and_rebuilt_baseline_calls_required=True,
        all_defined_baseline_outputs_bitexact=True,all_physical_T_S0_S1_S2_bitexact=True,
        radial_R_basis_recipe_and_diagnostics_bitexact=True,
        old_undefined_higher_tail_preserved_raw_but_not_scientific_input=True,
        original_radial_scalar_records_words=9,new_axial_Pn_record_words=75,
        supported_macro_total_order_NW=0,actual_macro_TRANC_option=2,
        actual_current_input_fixture=dict(name='actualphysical370_64',groups=370,
            snapshots=3,materials=24,radial_regions=8,radial_unknowns=14,
            axial_cells=48,axial_unknowns=1800,sn=32,scat=3,rank=1,
            assembly_only=True,all_original_native_records_byteexact_required=True),
        current_real_track_transport_replayed=False,transport_calls=0,linear_solves=0,
        original_scientific_thresholds_changed=False,synthetic_controls_only=False,
        actual_current_input_control_required=True)
