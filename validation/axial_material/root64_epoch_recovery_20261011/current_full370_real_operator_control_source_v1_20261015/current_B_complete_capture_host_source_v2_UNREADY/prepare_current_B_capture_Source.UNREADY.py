"""Root-only future Source generation. No compiler, native child, decoder or cleanup."""
import argparse,ast,importlib.util,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
def need(v,m):
 if v is not True:raise RuntimeError(m)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--admission-packet-pin',required=True);a=ap.parse_args()
 need(not any(os.path.lexists(BASE/n)for n in('PLAN.json','SOURCE_REVIEW_READY.json')),'fresh once Source generation, no overwrite or retry')
 q=BASE/'capture_Source_contract.UNREADY.py';spec=importlib.util.spec_from_file_location('B_capture_prepare_contract',q);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 author=m.metadata(m.pin(BASE/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json'));need(author['Source_only_frozen_before_Root_generation']is True and author['native_or_compiler_executed_by_author']is False and author['Source_preparer_or_publisher_executed_by_author']is False,'author Source freeze only; Root sole executor')
 for p in author['whole_Source_file_pins']:need(m.pin(p['path'])==p,'all author frozen Source intact')
 packet=m.metadata(json.loads(a.admission_packet_pin));build,bm=m.admit(packet)
 need(packet['source_role_pin_audit_complete']is True,'all exact genuine build/runtime/latest-prefix/input roles bound before Source preparation')
 io=m.metadata(packet['original_B_IO_Source_metadata_plan_pin']);seed=m.metadata(packet['original_v10_seed_plan_pin'])
 need(packet['original_v10_seed_plan_pin']['sha256']=='9bf2ba8444f0fe17989db3a31c373730da1d73bae564405c6ca71f5bc6c6579b'and seed['current_case_spec_pin']['sha256']=='fbe3362e16c19c93b87de2ebf67607c5ac0a579daa1f7af5891aae9c9faa7b16','exact original B current CASE and original v10 seed authority')
 need(packet['original_B_native_stage_inputs']==seed['states']['B']['native_stage_inputs']==io['original_B_native_stage_inputs']and packet['original_B_material_deck_pin']==seed['states']['B']['original_material_deck_pin']==io['original_B_material_deck_pin']and packet['actual_consumed_readonly_cwd_role_pins']==io['actual_consumed_readonly_cwd_role_pins'],'all original seven B inputs and distinct readonly old-cwd roles')
 for row in packet['original_B_native_stage_inputs']:m.current(row['input_pin'])
 for p in packet['actual_consumed_readonly_cwd_role_pins'].values():m.current(p)
 source_table={Path(p['path']).name:p for p in author['whole_Source_file_pins']};route=m.source(source_table['B_original_input_binding.UNREADY.py'],'B_capture_prepare_route')
 cwd=Path(route.NATIVE_CWD);need(not os.path.lexists(cwd/route.IO_COMPONENT),'literal fresh b63 absent, no replay or reused B output')
 binding=dict(schema='CURRENT_B_ORIGINAL_INPUT_AND_FRESH_IO_BINDING_V1',state='B',state_order=['B'],observation_scope=route.B_SCOPE,current_case_spec_pin=seed['current_case_spec_pin'],original_B_native_stage_inputs=packet['original_B_native_stage_inputs'],original_B_material_deck_pin=packet['original_B_material_deck_pin'],actual_native_cwd=str(cwd),io_component=route.IO_COMPONENT,actual_observation_directory=str(m.OUT),actual_output_root=str(m.OUT),material_product_names=dict(zip(route.PRODUCT_ROLES,route.PRODUCT_NAMES)),actual_consumed_readonly_cwd_role_pins=packet['actual_consumed_readonly_cwd_role_pins'],original_library_pins=io['original_library_pins'],original_caps=m.CAPS,library_copy_created=False,historical_B_context_claimed=False,native_executed_by_author=False,original_v10_seed_plan_pin=packet['original_v10_seed_plan_pin'],derived_B_material_deck_pin=source_table['material_B.b63.UNREADY.x2m'])
 route.validate_B_binding(binding,seed,packet['original_v10_seed_plan_pin']);oldcwd=route.snapshot_old_cwd_current7()
 need(oldcwd==packet['all_old_cwd_entries_current7_before_child'],'all old SCI-cwd entries current7 freshly bound by Root packet')
 before=0
 for root in packet['complete_joint_roots']:
  if not Path(root).exists():continue
  for p in Path(root).rglob('*'):
   s=p.lstat();need(not stat.S_ISLNK(s.st_mode),'no aliases in complete current joint prefix')
   if stat.S_ISREG(s.st_mode):before+=s.st_size
 for p in packet['explicit_cumulative_metadata_file_pins']:
  bm.current_metadata_role(p,build)
  if not any(Path(p['path']).is_relative_to(Path(r))for r in packet['complete_joint_roots']):before+=p['size_bytes']
 need(before+m.CAPTURE_BOUND+m.SOURCE_BOUND<2*2**30,'entire current prefix plus capture640MiB and Source16MiB fits original2GiB before GEN; actual guard rechecks open-unlinked')
 for p in author['whole_Source_file_pins']:
  if p['path'].endswith('.py'):ast.parse(Path(p['path']).read_text())
 plan=dict(packet,schema='CURRENT_B_COMPLETE_CAPTURE_SOURCE_ONLY_PLAN_V1',source_only=True,B_binding_template=binding,Source_only_cumulative_bytes_before_reservations=before,Source_generation_science_bodies_decoded=False,Source_generation_native_executed=False,**m.FALSE)
 m.write(BASE/'PLAN.json',plan);pp=m.pin(BASE/'PLAN.json');ready=dict(schema='CURRENT_B_COMPLETE_CAPTURE_SOURCE_REVIEW_READY_V1',source_only=True,control_plan_pin=pp,complete_source_file_pins=author['whole_Source_file_pins'],host_source_pin=source_table['run_guarded_current_B_complete_capture.UNREADY.py'],contract_Source_pin=source_table['capture_Source_contract.UNREADY.py'],dependencies=m.unique([json.loads(a.admission_packet_pin),pp]+packet['explicit_control_metadata_pins']),original_caps=m.CAPS,Source_or_native_business_executed=False)
 m.write(BASE/'SOURCE_REVIEW_READY.json',ready);print(json.dumps(dict(status='CURRENT_B_CAPTURE_SOURCE_PREPARED_ONLY',ready_pin=m.pin(BASE/'SOURCE_REVIEW_READY.json'),native_executed=False)),flush=True)
if __name__=='__main__':main()
