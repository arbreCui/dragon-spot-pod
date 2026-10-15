#!/usr/bin/env python3
"""Unique driver-only build Host draft; Source only, no compiler or child."""
import ast
import difflib
import importlib.util
import json
from pathlib import Path

R=Path('/Users/wen/spot')
REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
OLD=REC/'bq64_compact_expected_build_host_source_v4_20261013'
OUT=REC/'native_rank1_cache336_build_host_source_v1_20261014'
FUTURE=R/'validation/artifacts/axial-material-new-native-rank1-cache336-driver-complete70-build-only-20261014-v1'
SOURCE=REC/'native_rank1_exact_cache336_source_v1_20261014'
BASE=R/'validation/artifacts/axial-material-new-BQ64-compact-expected-composed-complete70-build-only-20261013-v4/Root_actual_build_only_summary.json'

def main():
    spec=importlib.util.spec_from_file_location('cache336_source_author',REC/'prepare_native_rank1_cache336_source_v1_20261014.py')
    s=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(s)
    if OUT.exists() or FUTURE.exists():
        raise RuntimeError('unique Source/actual namespaces must not exist')
    old_bytes,old_pin=s.read(OLD/'build_bq64_compact_expected_runtime.py')
    text=old_bytes.decode()
    old=text
    def replace(a,b):
        nonlocal text
        if text.count(a) != 1:
            raise RuntimeError('exact one Host Source replacement required: '+a[:90])
        text=text.replace(a,b)
    replace('"""One BOOTQ compile and exact ordered70 relink under the original supervisor.\n\nThis build does not run connected controls, transport, AAA, or ABA. The old70\nand old17 remain historical premises. Only BOOTQ at zero-based link index40\nis replaced. A separate fresh control report is necessary for the new reader.\n"""',
      '"""One internal cache-bound Driver compile and exact ordered70 relink.\n\nThe genuine compact BOOTQ build remains the premise. Only Driver at index37\nis replaced; all69 other ordered inputs, current9 core and four archives\nremain exact. Component bit controls and a future guarded full50 are separate.\n"""')
    replace("PLAN = HERE/'EXACT_ORIGINAL70_TO_COMPACT_BQ64_BUILD_PLAN.json'","PLAN = HERE/'EXACT_COMPACT70_TO_CACHE336_DRIVER_BUILD_PLAN.json'")
    replace("SOURCE = REC/'bq64_compact_expected_composed_source_draft_v1_20261013'","SOURCE = REC/'native_rank1_exact_cache336_source_v1_20261014'")
    replace("SF = SOURCE/'COMPLETE_BQ64_COMPACT_EXPECTED_COMPOSED_SOURCE_FREEZE.json'","SF = SOURCE/'COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_AND_CONTROL_SOURCE_FREEZE.json'")
    replace("OUT = R/'validation/artifacts/axial-material-new-BQ64-compact-expected-composed-complete70-build-only-20261013-v4'","OUT = R/'validation/artifacts/axial-material-new-native-rank1-cache336-driver-complete70-build-only-20261014-v1'")
    replace("HF_SCHEMA = 'COMPLETE_BQ64_COMPACT_EXPECTED_BUILD_HOST_SOURCE_ONLY_FREEZE_V1'","HF_SCHEMA = 'COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_BUILD_HOST_SOURCE_ONLY_FREEZE_V1'")
    replace("SF_SCHEMA = 'COMPLETE_BQ64_COMPACT_EXPECTED_COMPOSED_FORTRAN_SOURCE_ONLY_FREEZE_V1'","SF_SCHEMA = 'COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_AND_CONTROL_SOURCE_ONLY_FREEZE_V1'")
    replace("REPORT_SCHEMA = 'ACTUAL_BQ64_COMPACT_EXPECTED_COMPLETE70_BUILD_ONLY_V1'","REPORT_SCHEMA = 'ACTUAL_NATIVE_RANK1_CACHE336_DRIVER_COMPLETE70_BUILD_ONLY_V1'")
    replace("PASS_STATUS = 'ACTUAL_ONE_BOOTQ_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'","PASS_STATUS = 'ACTUAL_ONE_CACHE336_DRIVER_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'")
    # Whole unchanged low-level supervisor and first-failure blocks remain below.
    for a,b in [
      ("Path(p).name == 'SPOR64_BOOTQ64.o'] != [40]","Path(p).name == 'SPOT_GLOBAL_NATIVE_DRIVER64.o'] != [37]"),
      ("old[40] != plan['original_BOOTQ_object_pin']['path']","old[37] != plan['original_Driver_object_pin']['path']"),
      ("'exact old70/one BOOTQ input40/original order'","'exact compact70/one Driver input37/original order'"),
      ("obj = str(OUT/'build/SPOR64_BOOTQ64.o')","obj = str(OUT/'build/SPOT_GLOBAL_NATIVE_DRIVER64.o')"),
      ("'-c',str(SOURCE/'SPOR64_BOOTQ64.f90'),'-o',obj]","'-c',str(SOURCE/'SPOT_GLOBAL_NATIVE_DRIVER64.f'),'-o',obj]"),
      ("new[40] = obj","new[37] = obj"),
      ("[(40,old[40],obj)]","[(37,old[37],obj)]"),
      ("'only BOOTQ40 replacement;69 retained inputs;four exact archives'","'only Driver37 replacement;69 retained inputs including BOOTQ40;four exact archives'"),
      ("'actual_new_BOOTQ_object_pin'","'actual_new_Driver_object_pin'"),
      ("base['schema'] != 'ACTUAL_NATIVE_RANK1_EXACT_BLOCK_CACHE_COMPLETE70_BUILD_ONLY_V2'","base['schema'] != 'ACTUAL_BQ64_COMPACT_EXPECTED_COMPLETE70_BUILD_ONLY_V1'"),
      ("base['status'] != 'ACTUAL_TWO_CACHE_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'","base['status'] != 'ACTUAL_ONE_BOOTQ_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'"),
      ("base['old_nine_objects_identical_and_retained'] is not True","base['original69_other_inputs_identical_and_retained'] is not True or \\\n       base['original_four_archives_identical_and_retained'] is not True or \\\n       base['original_eight_unchanged_core_objects_identical_and_retained'] is not True or \\\n       base['replacement_zero_based_complete70_input_index'] != 40 or \\\n       base['actual_host_Source_freeze_pin'] != plan['selected_previous_complete70_Host_freeze_pin'] or \\\n       base['actual_new_Source_freeze_pin'] != plan['selected_previous_compact_Fortran_Source_freeze_pin']"),
      ("'exact genuine closed old70 build premise'","'exact genuine compact BOOTQ closed2 build premise, selected previous freezes'"),
      ("c.closed_report(base,helper,Path(pbase['path']).parent,3)","c.closed_report(base,helper,Path(pbase['path']).parent,2)"),
      ("'exact one-new-BOOTQ Source-only complete freeze'","'exact one-new-cache336 Driver Source-only complete freeze'"),
      ("str(SOURCE/'SPOR64_BOOTQ64.f90')","str(SOURCE/'SPOT_GLOBAL_NATIVE_DRIVER64.f')"),
      ("'single exact new BOOTQ Fortran Source'","'single exact new Driver Fortran Source'")]:
        replace(a,b)
    replace("    if plan['original_BOOTQ_Source_pin'] not in sf['original_source_pins'] or \\\n       plan['original_BOOT64_Source_pin'] not in sf['original_source_pins']:\n        raise RuntimeError('whole old BOOTQ/BOOT64 Source pins retained')\n",
      "    if plan['original_Driver_Source_pin'] not in sf['original_source_pins'] or \\\n       plan['unchanged_SPOT1P64_Source_pin'] not in sf['original_source_pins'] or \\\n       sf['Driver_single_literal_368_to336'] is not True or sf['public_Driver_ABI_unchanged'] is not True or \\\n       sf['original_math_modified'] is not False or sf['internal_exact_cache_working_set_bytes'] != 336*2**20:\n        raise RuntimeError('one cache-bound literal, whole original Driver/math and public ABI retained')\n")
    replace("    old9 = binding['seventeen_required_same_production_object_pins']\n    if old9 != plan['original_nine_core_object_pins'] or len(old9) != 9 or old9[5] != plan['original_BOOTQ_object_pin']:\n        raise RuntimeError('old9 premise maps BOOTQ one-based core6 to zero-based link40')\n",
      "    historical9 = binding['seventeen_required_same_production_object_pins']\n    if historical9 != plan['historical_original_nine_core_object_pins'] or len(historical9) != 9:\n        raise RuntimeError('historical original9 remain exact; not current new9 qualification')\n    old9 = plan['current_nine_core_object_pins']\n    if len(old9) != 9 or old9[:5]+old9[6:] != historical9[:5]+historical9[6:] or \\\n       old9[5] != plan['retained_current_BOOTQ_object_pin'] or old70[40] != old9[5] or \\\n       old70[37] != plan['original_Driver_object_pin']:\n        raise RuntimeError('exact current9 unchanged; BOOTQ core6 link40 retained, Driver link37 outside core9')\n")
    replace("    for row in old70+old9:\n", "    for row in old70+old9+historical9:\n")
    # Historical Q is no longer an actual70 link input; its exact fixed pin remains protected.
    replace("if table.get(row['path']) != row or row['path'] not in base['actual_complete70_link_inputs']:",
      "if table.get(row['path']) != row or (row not in historical9 and row['path'] not in base['actual_complete70_link_inputs']):")
    replace("base['fixed_current_pins']+base['output_pins']+old70+old9)","base['fixed_current_pins']+base['output_pins']+old70+old9+historical9)")
    replace("for name in ('build','runtime','compact-bq-build'):","for name in ('build','runtime','cache336-driver-build'):")
    replace("'compact-bq-build',resources)","'cache336-driver-build',resources)")
    replace("      replacement_zero_based_complete70_input_index=40,original_caps=caps,", "      replacement_zero_based_complete70_input_index=37,original_caps=caps,")
    replace("zip(('compile_BOOTQ','link_Dragon'),planned)","zip(('compile_Driver','link_Dragon'),planned)")
    replace("if label == 'compile_BOOTQ':\n                owned.append(c.pin(OUT/'build/SPOR64_BOOTQ64.o'))\n                owned.extend(c.pin(p) for p in sorted((OUT/'build').glob('*.mod')))",
      "if label == 'compile_Driver':\n                if sorted(p.name for p in (OUT/'build').iterdir()) != ['SPOT_GLOBAL_NATIVE_DRIVER64.o']:\n                    raise RuntimeError('Driver-only compile must create exactly one object, no module or other outputs')\n                owned.append(c.pin(OUT/'build/SPOT_GLOBAL_NATIVE_DRIVER64.o'))")
    replace("replacement_zero_based_complete70_input_index=40,original_nine_core_object_pins=old9,", "replacement_zero_based_complete70_input_index=37,original_nine_core_object_pins=old9,")
    replace("          original_eight_unchanged_core_objects_identical_and_retained=retained,\n          old_nine_objects_retained_as_historical_premise=retained,new_reader_control_qualification=False,",
      "          current_nine_core_objects_identical_and_retained=retained,\n          historical_original_nine_core_object_pins=historical9,\n          selected_previous_complete70_Host_freeze_pin=plan['selected_previous_complete70_Host_freeze_pin'],\n          selected_previous_compact_Fortran_Source_freeze_pin=plan['selected_previous_compact_Fortran_Source_freeze_pin'],\n          retained_current_BOOTQ_object_pin=plan['retained_current_BOOTQ_object_pin'],\n          unchanged_SPOT1P64_Source_pin=plan['unchanged_SPOT1P64_Source_pin'],\n          internal_R1_exact_cache_working_set_bytes=336*2**20,original_RSS_acceptance_cap_bytes=512*2**20,\n          new_cache_budget_component_control_qualification=False,new_reader_control_qualification=False,")
    ast.parse(text)
    old_lines=old.splitlines(keepends=True);new_lines=text.splitlines(keepends=True)
    sm=difflib.SequenceMatcher(a=old_lines,b=new_lines,autojunk=False)
    blocks=[]
    for tag,i,j,k,l in sm.get_opcodes():
        if tag != 'equal':
            blocks.append(dict(old_start_line=i,new_start_line=k,old=''.join(old_lines[i:j]),new=''.join(new_lines[k:l])))
    recovered=list(new_lines)
    for row in reversed(blocks):
        index=row['new_start_line'];newblock=row['new'].splitlines(keepends=True)
        if recovered[index:index+len(newblock)] != newblock:
            raise RuntimeError('Host inverse exact positional block')
        recovered[index:index+len(newblock)]=row['old'].splitlines(keepends=True)
    if ''.join(recovered).encode() != old_bytes:
        raise RuntimeError('Host whole-file inverse')
    base_bytes,pbase=s.read(BASE);base=json.loads(base_bytes)
    oldcmd=base['records'][-1]['command'];ordered=oldcmd[3:-2]
    full={row['path']:row for row in base['fixed_current_pins']+base['output_pins']}
    old70=[full[path] for path in ordered]
    if len(old70) != 70 or Path(ordered[37]).name != 'SPOT_GLOBAL_NATIVE_DRIVER64.o' or Path(ordered[40]).name != 'SPOR64_BOOTQ64.o' or Path(ordered[57]).name != 'SPOT1P64.o':
        raise RuntimeError('actual compact70 exact three object roles')
    historical9=base['original_nine_core_object_pins']
    current9=list(historical9);current9[5]=old70[40]
    first=base['records'][0]['command']
    source_driver=s.read(REC/'native_rank1_exact_block_cache_source_v1/SPOT_GLOBAL_NATIVE_DRIVER64.f')[1]
    source_math=s.read(REC/'native_rank1_exact_block_cache_source_v1/SPOT1P64.f90')[1]
    for row in old70+historical9+[base['actual_host_Source_freeze_pin'],base['actual_new_Source_freeze_pin']]:
        if s.read(row['path'])[1] != row:
            raise RuntimeError('actual compact70 Source-only current EOF7 proof')
    OUT.mkdir()
    host=s.put(OUT/'build_native_rank1_cache336_driver_runtime.py',text.encode())
    inverse=s.put(OUT/'COMPLETE_COMPACT_BUILD4_TO_CACHE336_DRIVER_HOST_BYTE_INVERSE.json',dict(
      schema='COMPLETE_COMPACT_BUILD4_TO_CACHE336_DRIVER_HOST_BYTE_INVERSE_V1',source_only=True,
      original_host_pin=old_pin,candidate_host_pin=host,blocks=blocks,whole_bytes_reverse_to_original=True,
      original_ownRSS_supervisor_and_first_failure_code_retained=True,compiler_executed=False,numerical_executed=False))
    caps=base['original_caps']
    plan=s.put(OUT/'EXACT_COMPACT70_TO_CACHE336_DRIVER_BUILD_PLAN.json',dict(
      schema='EXACT_COMPACT70_TO_CACHE336_DRIVER_SOURCE_ONLY_BUILD_PLAN_V1',source_only=True,
      compiler_executed=False,numerical_executed=False,planned_output_root=str(FUTURE),
      selected_new_Fortran_Source_freeze_path=str(SOURCE/'COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_AND_CONTROL_SOURCE_FREEZE.json'),
      actual_new_Driver_object_pin=None,actual_new_Dragon_pin=None,actual_new_build_report_pin=None,
      original_actual_complete70_report_pin=pbase,original_complete70_link_command=oldcmd,
      original_ordered70_input_pins=old70,original_compiler_pin=full[first[0]],
      original_compile_flags=first[1:10],original_compile_include_arguments=[v for v in first if v.startswith('-I')],
      original_Driver_object_pin=old70[37],original_Driver_Source_pin=source_driver,
      unchanged_SPOT1P64_Source_pin=source_math,unchanged_SPOT1P64_object_pin=old70[57],
      retained_current_BOOTQ_object_pin=old70[40],historical_original_nine_core_object_pins=historical9,
      current_nine_core_object_pins=current9,selected_previous_complete70_Host_freeze_pin=base['actual_host_Source_freeze_pin'],
      selected_previous_compact_Fortran_Source_freeze_pin=base['actual_new_Source_freeze_pin'],
      replacement_zero_based_complete70_input_index=37,remaining69_retained=True,
      current9_unchanged=True,four_archives_original_order_retained=True,original_caps=caps,
      selected_new_Common_Source_freeze_pin=s.read(REC/'post_curated66_current_catalog_common_source_v2_20261013/COMPLETE_POST_CURATED66_CURRENT_CATALOG_BINDING_COMMON_SOURCE_FREEZE.json')[1],
      Source_inverse_pin=inverse,Source_Host_pin=host,
      qualification_order='preserve genuine BOOTQ-only build index40 and its four component reports, then separately admit this Driver-only index37 build and new bit controls; finally new50 runtime selects this final70',
      new_driver_control_required=True,old_fresh17_and_model_and_public7_not_repeated=True,
      old_component_scope_argument='current9 core are unchanged; GLOBAL Driver outside current9, SPOT1P64 mathematical module is exact unchanged',
      old_base_complete_build_Host_freeze_pin=s.read(OLD/'COMPLETE_BQ64_COMPACT_EXPECTED_BUILD_HOST_SOURCE_FREEZE.json')[1],
      preparer_pin=s.read(__file__)[1]))
    ready=s.put(OUT/'SOURCE_ONLY_READY.json',dict(status='READY_FOR_INDEPENDENT_DRIVER_BUILD_HOST_SOURCE_REVIEW',
      failure=None,source_only=True,compiler_executed=False,numerical_executed=False,
      Host_pin=host,plan_pin=plan,whole_byte_inverse_pin=inverse,preparer_pin=s.read(__file__)[1],
      final_Host_freeze_pin=None,actual_new_build_report_pin=None))
    print(json.dumps(dict(status='CACHE336_DRIVER_BUILD_HOST_DRAFT_SOURCE_ONLY_CLOSED0',
      Host_pin=host,plan_pin=plan,inverse_pin=inverse,ready_pin=ready),ensure_ascii=False),flush=True)

if __name__=='__main__':
    main()
