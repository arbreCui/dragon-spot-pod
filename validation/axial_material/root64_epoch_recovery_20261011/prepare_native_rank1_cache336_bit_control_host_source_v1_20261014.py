#!/usr/bin/env python3
"""Source-only three-stage bit-control Host; never compiler or numerical work."""
import ast
import difflib
import importlib.util
import json
from pathlib import Path

R=Path('/Users/wen/spot')
REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
OLD=REC/'bq64_private_GANLIB_model_control_host_source_v5_20261013'
HERE=REC/'native_rank1_cache336_budget_bit_control_host_source_v1_20261014'
SOURCE=REC/'native_rank1_exact_cache336_source_v1_20261014'
BUILD=REC/'native_rank1_cache336_build_host_source_v1_20261014'
OUT=R/'validation/artifacts/axial-material-new-native-rank1-cache336-budget-bit-controls-20261014-v1'

ORACLE='''def model_oracle(c,root,record,cwd):
    rows,log_pin=log_rows(c,root,record)
    matches=[row for row in rows if row.get('status')=='ACTUAL_GENERIC_RANK1_CACHE336_BUDGET_COMPONENT_BIT_CONTROLS_COMPLETED_ONLY']
    if len(matches)!=1:raise RuntimeError('one genuine cache336 exact-budget bit terminal JSON')
    actual=matches[0]
    if type(actual.get('actual_assertions'))is not int or actual['actual_assertions']!=338 or \\
       type(actual.get('actual_SPOT1P64_calls'))is not int or actual['actual_SPOT1P64_calls']!=121 or \\
       any(actual.get(k)is not False for k in ('formal_SN32_quadrature_equivalence','genuine_solver_qualified',
         'physics_qualified','AAA_qualified','ABA_admitted','goal_complete')):
        raise RuntimeError('genuine338 assertions/121 calls, original301+110 and new37+11, unqualified scope')
    return dict(actual_assertions=actual['actual_assertions'],actual_SPOT1P64_calls=actual['actual_SPOT1P64_calls'],
      actual_terminal=actual,actual_log_pin=log_pin,original301_preserved=True,new37_budget_assertions_completed=True)


'''

def main():
    spec=importlib.util.spec_from_file_location('cache336_source_author_helpers',REC/'prepare_native_rank1_cache336_source_v1_20261014.py')
    s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
    if HERE.exists() or OUT.exists():raise RuntimeError('unique Source/runtime namespaces, no overwrite')
    original,oldpin=s.read(OLD/'run_guarded_model_controls.py');text=original.decode()
    def once(old,new):
        nonlocal text
        if text.count(old)!=1:raise RuntimeError('exact one Source splice: '+old[:80])
        text=text.replace(old,new)
    once('"""Guarded model controls; Source-only until a genuine closed2 build is supplied."""',
      '"""Guarded exact-cache budget bit controls; compile test/link unchanged math/run."""')
    once("OUT=R/'validation/artifacts/axial-material-new-BQ64-private-GANLIB-model-controls-20261013-v5'",
      "OUT=R/'validation/artifacts/axial-material-new-native-rank1-cache336-budget-bit-controls-20261014-v1'")
    once("KIND='model'","KIND='cache336'")
    once("HF_SCHEMA='COMPLETE_BQ64_PRIVATE_GANLIB_MODEL_CONTROL_HOST_SOURCE_ONLY_FREEZE_V1'",
      "HF_SCHEMA='COMPLETE_NATIVE_RANK1_CACHE336_BUDGET_BIT_CONTROL_HOST_SOURCE_ONLY_FREEZE_V1'")
    once("SF_SCHEMA='COMPLETE_BQ64_COMPACT_EXPECTED_COMPOSED_FORTRAN_SOURCE_ONLY_FREEZE_V1'",
      "SF_SCHEMA='COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_AND_CONTROL_SOURCE_ONLY_FREEZE_V1'")
    once("REPORT_SCHEMA='ACTUAL_BQ64_PRIVATE_GANLIB_MODEL_GUARDED_CONTROL_REPORT_V1'",
      "REPORT_SCHEMA='ACTUAL_NATIVE_RANK1_CACHE336_BUDGET_BIT_GUARDED_CONTROL_REPORT_V1'")
    once("PASS_STATUS='ACTUAL_PRIVATE_GANLIB_MODEL_CONTROLS_CLOSED0_ONLY'",
      "PASS_STATUS='ACTUAL_CACHE336_ENABLED_STORE_REJECT_MIXED_GROUP_BIT_CONTROLS_CLOSED0_ONLY'")
    start=text.index('def model_oracle(');end=text.index('def public_oracle(',start)
    text=text[:start]+ORACLE+text[end:]
    text=text.replace("KIND=='model'","KIND=='cache336'")
    text=text.replace("expected_new[40]=plan['new_build_expected_BOOTQ_object_path']","expected_new[37]=plan['new_build_expected_Driver_object_path']")
    text=text.replace("plan['new_build_expected_BOOTQ_object_path']","plan['new_build_expected_Driver_object_path']")
    # Exact previous70 source files and original inputs remain protected. Only the
    # new Driver output is replaced, and the existing math object becomes test input.
    once("    link_cmd=[compiler,'-O2','-ffp-contract=off',obj,*core,*libraries,'-o',exe]",
      "    math=plan['unchanged_math_object_pin']\n    if new[57]!=math['path'] or math['path'] not in new:\n        raise RuntimeError('exact retained mathematical SPOT1P64 object at link57')\n    c.same_pin(math['path'],math)\n    core=[math['path']]\n    link_cmd=[compiler,'-O2','-ffp-contract=off',obj,*core,*libraries,'-o',exe]")
    once("        if selected!=plan.get(key)or not isinstance(selected,dict)or hf_table.get(selected['path'])!=selected:",
      "        if not isinstance(selected,dict)or selected.get('path')!=plan[key+'_path']or hf_table.get(selected['path'])!=selected:")
    once("    if psf!=plan['selected_control_Source_freeze_pin']or hf_table.get(psf['path'])!=psf or ",
      "    if psf!=selected_fortran_sf or psf['path']!=plan['selected_control_Source_freeze_path']or hf_table.get(psf['path'])!=psf or ")
    once("base.get('schema')!='ACTUAL_BQ64_COMPACT_EXPECTED_COMPLETE70_BUILD_ONLY_V1'", "base.get('schema')!='ACTUAL_NATIVE_RANK1_CACHE336_DRIVER_COMPLETE70_BUILD_ONLY_V1'")
    once("base.get('status')!='ACTUAL_ONE_BOOTQ_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'", "base.get('status')!='ACTUAL_ONE_CACHE336_DRIVER_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'")
    once("base.get('replacement_zero_based_complete70_input_index')!=40", "base.get('replacement_zero_based_complete70_input_index')!=37")
    once("'original_four_archives_identical_and_retained','original_eight_unchanged_core_objects_identical_and_retained'", "'original_four_archives_identical_and_retained','current_nine_core_objects_identical_and_retained'")
    once("'transport_executed','new_entry_controls_executed','new_reader_control_qualification'", "'transport_executed','new_entry_controls_executed','new_reader_control_qualification','new_cache_budget_component_control_qualification'")
    once("'new BOOTQ genuine actual build output PF'","'new Driver genuine actual build output PF'")
    once("    for row in plan['original_nine_core_pins'][:5]+plan['original_nine_core_pins'][6:]:", "    for row in plan['current_nine_core_pins']:")
    text=text.replace('actual_new_BOOTQ_object_pin=new_object','actual_new_Driver_object_pin=new_object')
    once("        owned.append(c.pin(OUT/'build/control.o'));owned.extend(c.pin(p)for p in sorted((OUT/'build').glob('*.mod')))",
      "        if sorted(p.name for p in (OUT/'build').iterdir())!=['control.o']:\n            raise RuntimeError('control compile creates exactly control.o, no rebuilt math module')\n        owned.append(c.pin(OUT/'build/control.o'))")
    once("            cwd=OUT/'model';cwd.mkdir();record=run(cwd,'run_model',[exe])\n            actual.append(model_oracle(c,OUT,record,cwd))\n            owned.extend(actual[-1]['actual_retained_model_file_pins'])",
      "            cwd=OUT/'bits';cwd.mkdir();record=run(cwd,'run_budget_bits',[exe])\n            actual.append(model_oracle(c,OUT,record,cwd))")
    once("          private_model_does_not_independently_qualify_public_reader=True,old17_PASS_inherited=False,\n          actual_model_controls_passed=good if KIND=='cache336'else False,",
      "          component_bit_controls_do_not_independently_qualify_solver_or_physics=True,old17_PASS_inherited=False,\n          actual_cache336_budget_bit_controls_passed=good,original301_assertions_retained=True,new37_assertions_expected=True,\n          actual_model_controls_passed=False,")
    once("final_report_resource_check_passed=False,compiler_executed=True,synthetic_protocol_fixture_only=True,",
      "final_report_resource_check_passed=False,compiler_executed=(OUT/('compact-'+KIND+'-controls/compile_control.watchdog.json')).exists(),synthetic_protocol_fixture_only=True,")
    once("                  actual_model_controls_passed=False,actual_seven_genuine_public_READ_controls_passed=False)",
      "                  actual_cache336_budget_bit_controls_passed=False,actual_model_controls_passed=False,actual_seven_genuine_public_READ_controls_passed=False)")
    ast.parse(text)
    a=original.decode().splitlines(keepends=True);b=text.splitlines(keepends=True)
    blocks=[dict(old_start_line=i,new_start_line=k,old=''.join(a[i:j]),new=''.join(b[k:l])) for tag,i,j,k,l in difflib.SequenceMatcher(a=a,b=b,autojunk=False).get_opcodes() if tag!='equal']
    recovered=list(b)
    for block in reversed(blocks):
        i=block['new_start_line'];new=block['new'].splitlines(keepends=True)
        if recovered[i:i+len(new)]!=new:raise RuntimeError('exact positional inverse')
        recovered[i:i+len(new)]=block['old'].splitlines(keepends=True)
    if ''.join(recovered).encode()!=original:raise RuntimeError('whole original model5 Host bytes recover')
    bpraw,bppin=s.read(BUILD/'EXACT_COMPACT70_TO_CACHE336_DRIVER_BUILD_PLAN.json');bp=json.loads(bpraw)
    sf_future=SOURCE/'COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_AND_CONTROL_SOURCE_FREEZE.json'
    hf_future=BUILD/'COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_BUILD_HOST_SOURCE_FREEZE.json'
    control=s.read(SOURCE/'test_generic_rank1_cache336_budget_bits_with_abort.f90')[1]
    driver=s.read(SOURCE/'SPOT_GLOBAL_NATIVE_DRIVER64.f')[1]
    HERE.mkdir()
    host=s.put(HERE/'run_guarded_cache336_budget_bit_controls.py',text.encode())
    inverse=s.put(HERE/'COMPLETE_MODEL5_TO_CACHE336_BUDGET_BIT_HOST_WHOLE_BYTE_INVERSE.json',dict(
      schema='COMPLETE_MODEL5_TO_CACHE336_BUDGET_BIT_HOST_WHOLE_BYTE_INVERSE_V1',source_only=True,
      original_host_pin=oldpin,candidate_host_pin=host,blocks=blocks,whole_original_recovery=True,
      original_guard_FirstFailure_aux128_pending8_methods_wholebytes_retained=True,
      compiler_executed=False,numerical_executed=False))
    plan=s.put(HERE/'EXACT_CONTROL_HOST_SOURCE_ONLY_PLAN.json',dict(
      schema='CACHE336_BUDGET_BIT_CONTROL_HOST_SOURCE_ONLY_PLAN_V1',kind='cache336',source_only=True,
      compiler_executed=False,numerical_executed=False,planned_output_root=str(OUT),
      selected_new_build_Host_freeze_pin_path=str(hf_future),selected_new_Fortran_Source_freeze_pin_path=str(sf_future),
      selected_control_Source_freeze_path=str(sf_future),control_Source_pin=control,production_Source_pin=driver,
      original_ordered70_paths=[v['path'] for v in bp['original_ordered70_input_pins']],
      unchanged_math_object_pin=bp['unchanged_SPOT1P64_object_pin'],unchanged_math_Source_pin=bp['unchanged_SPOT1P64_Source_pin'],
      current_nine_core_pins=bp['current_nine_core_object_pins'],
      original_nine_core_paths=[v['path']for v in bp['current_nine_core_object_pins']],
      original_compiler_pin=bp['original_compiler_pin'],original_compile_flags=bp['original_compile_flags'],
      original_compile_include_arguments=bp['original_compile_include_arguments'],
      original_four_archive_paths=[v['path']for v in bp['original_ordered70_input_pins']if v['path'].endswith('.a')],
      new_build_compile_include_arguments=['-I'+str(Path(bp['planned_output_root'])/'build')]+bp['original_compile_include_arguments'],
      new_build_expected_build_directory=str(Path(bp['planned_output_root'])/'build'),
      new_build_expected_Driver_object_path=str(Path(bp['planned_output_root'])/'build/SPOT_GLOBAL_NATIVE_DRIVER64.o'),
      new_build_expected_Dragon_path=str(Path(bp['planned_output_root'])/'runtime/Dragon'),
      new_build_expected_report_path=str(Path(bp['planned_output_root'])/'Root_actual_build_only_summary.json'),
      original_caps=bp['original_caps'],original_aux_cap_bytes=128*2**20,original_pending_metadata_bytes=8*2**20,
      planned_run_phases=[dict(case='enabled_STORE_reject_and_mixed_two_groups',phase='single',expected_assertions=338,expected_SPOT1P64_calls=121)],
      expected_stage_labels=['compile_control','link_control','run_budget_bits'],expected_actual_assertions=338,
      expected_actual_SPOT1P64_calls=121,original_assertions=301,additional_assertions=37,
      original_math_module_recompiled=False,guarded_stages=3,
      current_predecessor_build_plan_pin=bppin,current_unchanged_model5_Host_freeze_pin=s.read(OLD/'COMPLETE_CONTROL_HOST_SOURCE_FREEZE.json')[1],
      original_common_Source_pin=s.read(REC/'post_curated66_current_catalog_common_source_v2_20261013/guarded_warm_A_common.py')[1],
      selected_new_Common_Source_freeze_pin=bp['selected_new_Common_Source_freeze_pin'],
      future_actual_new_build70_report_pin=None,future_actual_control_object_pin=None,
      future_actual_control_executable_pin=None,future_actual_control_report_pin=None,
      Source_Host_pin=host,Source_inverse_pin=inverse,preparer_pin=s.read(__file__)[1],
      component_only=True,reader_qualified=False,physics_qualified=False))
    ready=s.put(HERE/'SOURCE_ONLY_READY.json',dict(status='READY_FOR_INDEPENDENT_CACHE336_BIT_HOST_SOURCE_REVIEW',failure=None,
      source_only=True,compiler_executed=False,numerical_executed=False,Host_pin=host,plan_pin=plan,
      inverse_pin=inverse,preparer_pin=s.read(__file__)[1],future_own_HF_pin=None,future_own_CLI_pin=None,
      future_actual_control_report_pin=None))
    print(json.dumps(dict(status='SOURCE_ONLY_CACHE336_BUDGET_BIT_HOST_PREPARED_CLOSED0',Host_pin=host,
      plan_pin=plan,inverse_pin=inverse,ready_pin=ready),ensure_ascii=False),flush=True)

if __name__=='__main__':main()
