"""Root-only Source preparation interface. No compiler, native job or science decoder."""
import argparse,ast,hashlib,importlib.util,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
def need(v,m):
 if v is not True:raise RuntimeError(m)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--admission-packet-pin',required=True);a=ap.parse_args()
 need(not any(os.path.lexists(BASE/n)for n in('PLAN.json','SOURCE_REVIEW_READY.json')),'fresh Source preparation once/no retry')
 q=BASE/'build_IO_Source_contract.UNREADY.py';spec=importlib.util.spec_from_file_location('B_IO_prepare_contract',q);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 author=m.metadata(m.pin_source(BASE/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json'))
 need(author['Source_only_frozen_before_Root_generation']is True and author['compiler_or_native_executed_by_author']is False and author['Source_preparer_or_publisher_executed_by_author']is False,'author Source-only freeze; Root sole executor')
 for p in author['whole_Source_file_pins']:need(m.pin_source(p['path'])==p,'all author-frozen Source intact')
 packet=m.metadata(json.loads(a.admission_packet_pin));need(packet['schema']=='ROOT_B_IO_BUILD_CURRENT_ADMISSION_PACKET_V1'and packet['original_caps']==m.CAPS and packet['actual_business_preconditions_closed']is True,'real Root packet mandatory; all draft null fields remain UNREADY')
 need(not os.path.lexists(m.OUT),'fresh whole owning build root, no retry')
 m.admit_lifecycle(packet);need(packet['C_compiler_pin']['path']=='/Library/Developer/CommandLineTools/usr/bin/clang','Root-captured literal current C compiler executable, not historical clang++78')
 proof=m.metadata(packet['C_compiler_tool_full_pin_metadata']);need(proof['schema']=='ROOT_CURRENT_EXISTING_C_COMPILER_TOOL_BYTE_PIN_ONLY_V1'and proof['compiler_tool_pin']==packet['C_compiler_pin']and proof['compiler_executed']is False and proof['ABI_qualified']is False,'Root-captured compiler fullPF metadata exact actual role; no compiler qualification assumed')
 m.current(packet['C_compiler_pin'],packet['C_compiler_pin'])
 need(packet['C_configuration']==dict(architecture='arm64',platform='Darwin',hdf5=False,openmp=False,mpi=False,preprocessor=['-DLinux','-DUnix']),'new explicit clang IO route retains the declared current Ganlib Makefile flags; historical compiler is not reconstructed')
 need(packet['original_Ganlib_configuration_Source_evidence_complete']is True and packet['original_Ganlib_header_include_closure_complete']is True,'Source/header ABI authority must be bound, not inferred from old binary name')
 config=m.metadata(packet['configuration_header_Source_evidence_pin'])
 need(config['schema']=='INDEPENDENT_B_IO_GANLIB_CONFIG_AND_LOCAL_HEADERS_SOURCE_PREFLIGHT_V1'and config['status']=='PASS_SOURCE_ONLY'and config['failure']is None and config['configuration_and_header_Source_pins']==packet['original_Ganlib_configuration_and_header_Source_pins']and config['actual_active_nonHDF5_local_include_closure']==packet['active_nonHDF5_project_header_closure'],'exact eight independent Source PFs and five active local headers')
 need(config['original_Ganlib_Makefile_Source_facts']['default_ccompiler_line44']=='gcc'and config['original_Ganlib_Makefile_Source_facts']['llvm1_ccompiler_line41']=='clang'and config['original_compiled_archive_ABI_or_features_reconstructed']is False and config['new_compiled_ABI_or_IO_semantics_qualified']is False and packet['explicit_new_clang_IO_compiler_route']is True,'Makefile default gcc and explicit new clang route remain distinct; no historical or new compiled qualification inherited')
 for p in packet['compile_and_link_input_pins']:m.current(p,packet['C_compiler_pin'])
 for p in packet['original_SCI_current7_only_pins']:m.current(p)
 for p in packet['original_Ganlib_configuration_and_header_Source_pins']:need(m.pin_source(p['path'])==p,'whole original project ABI/config/header Source')
 old=m.metadata(packet['original75_build_report_pin']);links=[r for r in old['records']if r['label']=='build/link_Dragon'];need(len(links)==1 and old['status']=='ACTUAL_FIVE_COMPILE_COMPLETE75_LINK_CLOSED0_ONLY'and old['failure']is None and all(r['status']=='PASS'for r in old['records']),'original actual build metadata only')
 original=links[0]['command'];needed=[p for p in original if p.endswith(('.o','.a'))];bound={p['path']:p for p in packet['compile_and_link_input_pins']}
 need(len(needed)==75 and sum(x.endswith('.o')for x in needed)==71 and sum(x.endswith('.a')for x in needed)==4 and all(x in bound for x in needed),'all71 objects+4 archives exact saved fullPF/current7; no body rehash by Sourcegen')
 for p in packet['whole_byte_build_source_copy_pins']:need(m.pin_source(p['path'])==p,'whole retained code Source copies only')
 plan=dict(packet,schema='B_IO_BUILD_QUALIFICATION_SOURCE_ONLY_PLAN_V1',source_only=True,planned_actual_output_root=str(m.OUT),bounded_new_output_reservation_bytes=m.OUTPUT_BOUND,bounded_new_Source_metadata_reservation_bytes=m.SOURCE_BOUND,host_summary_hard_bound_bytes=6*2**20,Source_preparation_science_bodies_decoded=False,Source_generation_compiler_executed=False,**m.FALSE)
 result=m.commands(plan);plan['exact_five_stage_commands']=result['compile_commands']+[result['link_command']];plan['original75_link_argv_inverse_equal']=True;plan['new_explicit_object_count']=74;plan['archive_count']=4
 roots=plan['complete_joint_roots'];before=0
 for root in roots:
  if not Path(root).exists():continue
  for p in Path(root).rglob('*'):
   s=p.lstat();need(not stat.S_ISLNK(s.st_mode),'complete output namespace has no aliases')
   if stat.S_ISREG(s.st_mode):before+=s.st_size
 for p in plan['explicit_cumulative_metadata_file_pins']:
  m.current_metadata_role(p,plan)
  if not any(Path(p['path']).is_relative_to(Path(r))for r in roots):before+=p['size_bytes']
 need(before+m.OUTPUT_BOUND+m.SOURCE_BOUND<2*2**30,'exact current whole prefix+build32MiB+Source16MiB within original2GiB; no old11.4MiB assumption')
 plan['Source_only_current_cumulative_bytes_before_reservations']=before
 for p in author['whole_Source_file_pins']:
  if p['path'].endswith('.py'):ast.parse(Path(p['path']).read_text())
 m.write_once(BASE/'PLAN.json',plan);pp=m.pin_source(BASE/'PLAN.json')
 ready=dict(schema='B_IO_BUILD_QUALIFICATION_SOURCE_REVIEW_READY_V1',source_only=True,control_plan_pin=pp,complete_source_file_pins=author['whole_Source_file_pins'],host_source_pin=next(p for p in author['whole_Source_file_pins']if Path(p['path']).name=='run_guarded_B_IO_build_qualification.UNREADY.py'),contract_Source_pin=m.pin_source(q),dependencies=m.unique([json.loads(a.admission_packet_pin),pp]+plan['explicit_control_metadata_pins']),original_caps=m.CAPS,Source_or_compiler_business_executed=False)
 m.write_once(BASE/'SOURCE_REVIEW_READY.json',ready);print(json.dumps(dict(status='B_IO_BUILD_SOURCE_PREPARED_ONLY',ready_pin=m.pin_source(BASE/'SOURCE_REVIEW_READY.json'),compiler_executed=False,native_executed=False)),flush=True)
if __name__=='__main__':main()
