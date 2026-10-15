#!/usr/bin/env python3
"""Source only: exact owning compiler metadata names, and Driver v2 namespace."""
import ast
import importlib.util
import json
from pathlib import Path

REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=REC/'native_rank1_cache336_budget_bit_control_host_source_v1_20261014'
NEW=REC/'native_rank1_cache336_budget_bit_control_host_source_v2_20261014'

def main():
    spec=importlib.util.spec_from_file_location('cache336_Source_helpers',REC/'prepare_native_rank1_cache336_source_v1_20261014.py')
    s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
    if NEW.exists():raise RuntimeError('unique Source namespace only, no overwrite')
    raw,oldhost=s.read(OLD/'run_guarded_cache336_budget_bit_controls.py');text=raw.decode();changes=[]
    def once(before,after,reason):
        nonlocal text
        if text.count(before)!=1:raise RuntimeError('one exact Source splice '+reason)
        text=text.replace(before,after);changes.append(dict(before=before,after=after,reason=reason))
    once("OUT=R/'validation/artifacts/axial-material-new-native-rank1-cache336-budget-bit-controls-20261014-v1'",
      "OUT=R/'validation/artifacts/axial-material-new-native-rank1-cache336-budget-bit-controls-20261014-v2'",'unique v2 own OUT')
    before="""        if sorted(p.name for p in (OUT/'build').iterdir())!=['control.o']:
            raise RuntimeError('control compile creates exactly control.o, no rebuilt math module')
        owned.append(c.pin(OUT/'build/control.o'))"""
    after="""        allowed=['compile_control.log','compile_control.watchdog.json','control.o']
        if sorted(p.name for p in (OUT/'build').iterdir())!=allowed:
            raise RuntimeError('control compile permits only exact object/current compile log/watch; no module or other file')
        for name in allowed:
            path=OUT/'build'/name;row=c.pin(path)
            if not stat.S_ISREG(row['identity'][2])or row['identity'][3]!=1 or path.lstat().st_uid!=os.getuid():
                raise RuntimeError('own current compile object/log/watch ordinary UID single-link fullPF')
        owned.append(c.pin(OUT/'build/control.o'))"""
    once(before,after,'exact current compile metadata roles retained, no math module or other files')
    ast.parse(text);inverse=text
    for block in reversed(changes):
        if inverse.count(block['after'])!=1:raise RuntimeError('exact one reverse block')
        inverse=inverse.replace(block['after'],block['before'])
    if inverse.encode()!=raw:raise RuntimeError('entire v1 Host inverse')
    rawplan,oldplan=s.read(OLD/'EXACT_CONTROL_HOST_SOURCE_ONLY_PLAN.json');prior=json.loads(rawplan);plan=dict(prior)
    oldout='axial-material-new-native-rank1-cache336-budget-bit-controls-20261014-v1'
    newout='axial-material-new-native-rank1-cache336-budget-bit-controls-20261014-v2'
    oldbuild='native_rank1_cache336_build_host_source_v1_20261014';newbuild='native_rank1_cache336_build_host_source_v2_20261014'
    oldart='axial-material-new-native-rank1-cache336-driver-complete70-build-only-20261014-v1';newart='axial-material-new-native-rank1-cache336-driver-complete70-build-only-20261014-v2'
    fields={}
    for key in ('planned_output_root','selected_new_build_Host_freeze_pin_path','new_build_compile_include_arguments',
      'new_build_expected_build_directory','new_build_expected_Driver_object_path','new_build_expected_Dragon_path','new_build_expected_report_path'):
        old=prior[key]
        if isinstance(old,list):new=[x.replace(oldart,newart)for x in old]
        else:new=old.replace(oldout,newout).replace(oldbuild,newbuild).replace(oldart,newart)
        if new==old:raise RuntimeError('exact selected v2 namespace field change '+key)
        plan[key]=new;fields[key]=dict(old=old,new=new)
    for key in ('control_Source_pin','production_Source_pin','unchanged_math_object_pin','unchanged_math_Source_pin',
      'original_ordered70_paths','current_nine_core_pins','original_four_archive_paths','original_caps'):
        if plan[key]!=prior[key]:raise RuntimeError('original Fortran/math/inputs/caps wholedata retained')
    NEW.mkdir();host=s.put(NEW/'run_guarded_cache336_budget_bit_controls.py',text.encode())
    inv=s.put(NEW/'COMPLETE_BIT_HOST_V1_TO_V2_OWN_RECORD_SCOPE_BYTE_INVERSE.json',dict(
      schema='COMPLETE_CACHE336_BIT_HOST_V1_TO_V2_EXACT_RECORD_SCOPE_INVERSE_V1',source_only=True,
      original_host_pin=oldhost,candidate_host_pin=host,changes=changes,whole_restored_original_bytes_equal=True,
      original_plan_pin=oldplan,plan_namespace_field_changes=fields,original_plan_data=prior,
      compiler_executed=False,numerical_executed=False,files_deleted=False))
    plan.update(Source_Host_pin=host,Source_inverse_pin=inv,preparer_pin=s.read(__file__)[1],
      predecessor_bit_Host_freeze_pin=s.read(OLD/'COMPLETE_CONTROL_HOST_SOURCE_FREEZE.json')[1],
      predecessor_bit_CLI_pin=s.read(OLD/'DECLARED_EXECUTION_INTERFACE.json')[1],
      compile_stage_exact_owned_build_names=['compile_control.log','compile_control.watchdog.json','control.o'],
      completed_build_exact_owned_names=['compile_control.log','compile_control.watchdog.json','control.o','link_control.log','link_control.watchdog.json'],
      all_other_original_plan_fields_wholedata_preserved=True)
    pplan=s.put(NEW/'EXACT_CONTROL_HOST_SOURCE_ONLY_PLAN.json',plan)
    originalfreezer,oldfreezer=s.read(OLD/'freeze_cache336_budget_bit_control_host_source_only_v2.py')
    freezer=originalfreezer.decode()
    needle="    rows=bhf['dependencies']+predecessor['dependencies']+[pbhf,psf,ppred,pr,pt,pcommon]+own+"
    replacement="    previous_bit,previous_bit_pin=load(plan['predecessor_bit_Host_freeze_pin']['path'],plan['predecessor_bit_Host_freeze_pin'])\n    previous_cli,previous_cli_pin=load(plan['predecessor_bit_CLI_pin']['path'],plan['predecessor_bit_CLI_pin'])\n    rows=(previous_bit['dependencies']+[previous_bit_pin,previous_cli_pin]+bhf['dependencies']+predecessor['dependencies']+[pbhf,psf,ppred,pr,pt,pcommon]+own+"
    # The already corrected v1 freezer has the opening parenthesis.
    needle=needle.replace('rows=','rows=(')
    if freezer.count(needle)!=1:raise RuntimeError('exact predecessor complete HF inheritance Source')
    freezer=freezer.replace(needle,replacement)
    ast.parse(freezer)
    pfreezer=s.put(NEW/'freeze_cache336_budget_bit_control_host_source_only.py',freezer.encode())
    finv=s.put(NEW/'COMPLETE_BIT_FREEZER_V1_TO_V2_FULL_HF_INHERITANCE_INVERSE.json',dict(
      schema='CACHE336_BIT_FREEZER_V1_TO_V2_EXACT_FULL_HF_INHERITANCE_INVERSE_V1',source_only=True,
      original_freezer_pin=oldfreezer,candidate_freezer_pin=pfreezer,old=needle,new=replacement,
      whole_reverse_equal=freezer.replace(replacement,needle).encode()==originalfreezer,
      compiler_executed=False,numerical_executed=False))
    ready=s.put(NEW/'SOURCE_ONLY_READY.json',dict(status='READY_FOR_INDEPENDENT_CACHE336_BIT_V2_RECORD_SCOPE_SOURCE_REVIEW',
      failure=None,source_only=True,compiler_executed=False,numerical_executed=False,
      Host_pin=host,plan_pin=pplan,inverse_pin=inv,preparer_pin=s.read(__file__)[1],
      final_freezer_pin=pfreezer,freezer_inverse_pin=finv,future_own_HF_pin=None,future_own_CLI_pin=None,
      future_actual_control_report_pin=None))
    print(json.dumps(dict(status='SOURCE_ONLY_BIT_V2_EXACT_OWN_RECORD_ROLE_PREPARED_CLOSED0',Host_pin=host,
      plan_pin=pplan,inverse_pin=inv,freezer_pin=pfreezer,freezer_inverse_pin=finv,ready_pin=ready)),flush=True)

if __name__=='__main__':main()
