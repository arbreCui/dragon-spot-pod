"""Root-only metadata Source preparation; no compiler/native/science execution."""
import argparse,ast,importlib.util,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--admission-packet-pin',required=True);a=ap.parse_args()
 need=lambda v,s:None if v is True else(_ for _ in()).throw(RuntimeError(s))
 with(BASE/'ROOT_SOURCE_GENERATION_CLAIM.json').open('x')as f:json.dump(dict(Source_generation_only=True,Root_PID=os.getpid(),claim_before_helper_import=True),f);f.write('\n');f.flush();os.fsync(f.fileno())
 q=BASE/'build_B_plane2_runtime_Source_contract.UNREADY.py';spec=importlib.util.spec_from_file_location('B_plane2_runtime_prepare_contract',q);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 author=m.metadata(m.pin_source(BASE/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json'));need(author['Source_only_frozen_before_Root_generation']is True and author['compiler_or_native_executed_by_author']is False and author['Source_preparer_or_publisher_executed_by_author']is False,'frozen Source only; Root sole executor')
 for p in author['whole_Source_file_pins']:need(m.pin_source(p['path'])==p,'all seven author-frozen Sources wholebytes')
 need(json.loads(a.admission_packet_pin)==author['immutable_admission_packet_pin'],'exact author-frozen immutable admission packet fullPF');packet=m.metadata(json.loads(a.admission_packet_pin));need(packet['schema']=='ROOT_B_PLANE2_MINIMAL_RUNTIME_BUILD_CURRENT_ADMISSION_PACKET_V1'and packet['original_caps']==m.CAPS and packet['actual_business_preconditions_closed']is True,'true corrected bridge0/post0 and actual latest resource facts mandatory, NULL hard reject')
 need(not any(os.path.lexists(BASE/n)for n in('PLAN.json','SOURCE_REVIEW_READY.json'))and not os.path.lexists(m.OUT),'fresh Source generation and complete owning root once/no retry')
 m.admit_lifecycle(packet)
 for p in packet['compile_and_link_input_pins']:m.current_metadata_role(p,packet)
 for p in packet['whole_byte_build_source_copy_pins']:need(m.pin_source(p['path'])==p,'three new Source wholebyte copies only')
 for row in packet['original_compile_include_directory_identities']:
  p=Path(row['path']);s=p.lstat();need(stat.S_ISDIR(s.st_mode)and m.identity(s)==row['identity']and not any(x.is_symlink()for x in(p,*p.parents)),'exact existing compile include directory identity/order')
 plan=dict(admission_packet_pin=json.loads(a.admission_packet_pin),schema='B_PLANE2_RUNTIME_SOURCE_ONLY_PLAN_V1',source_only=True,planned_actual_output_root=str(m.OUT),bounded_new_output_reservation_bytes=m.OUTPUT_BOUND,bounded_new_Source_metadata_reservation_bytes=m.SOURCE_BOUND,host_summary_hard_bound_bytes=6*2**20,Source_preparation_science_bodies_decoded=False,Source_generation_compiler_executed=False,**m.FALSE)
 result=m.commands(dict(packet,**plan));plan['exact_four_stage_commands']=result['compile_commands']+[result['link_command']];plan['planned_ordered71_link_inputs']=result['ordered71_link_inputs'];plan['original70_link_argv_inverse_equal']=True;plan['new_explicit_object_count']=67;plan['archive_count']=4
 roots=packet['complete_joint_roots'];before=0
 for root in roots:
  if not Path(root).exists():continue
  for p in Path(root).rglob('*'):
   s=p.lstat();need(not stat.S_ISLNK(s.st_mode),'whole owning namespace rejects aliases')
   if stat.S_ISREG(s.st_mode):before+=s.st_size
 for p in packet['explicit_cumulative_metadata_file_pins']:
  m.current_metadata_role(p,packet)
  if not any(Path(p['path']).is_relative_to(Path(r))for r in roots):before+=p['size_bytes']
 unlinked={}
 for name in os.listdir('/dev/fd'):
  try:s=os.fstat(int(name))
  except(ValueError,OSError):continue
  if stat.S_ISREG(s.st_mode)and s.st_nlink==0:unlinked[s.st_dev,s.st_ino]=s.st_size
 need(before+sum(unlinked.values())+m.OUTPUT_BOUND+m.SOURCE_BOUND<2*2**30,'whole83 plus fresh84 and all explicit metadata/openunlinked plus output32/Source8 under original2GiB')
 plan['Source_only_current_cumulative_bytes_before_reservations']=before;plan['Source_only_open_unlinked_bytes']=sum(unlinked.values())
 for p in author['whole_Source_file_pins']:
  if p['path'].endswith('.py'):ast.parse(Path(p['path']).read_text())
 m.write_once(BASE/'PLAN.json',plan);pp=m.pin_source(BASE/'PLAN.json')
 ready=dict(schema='B_PLANE2_RUNTIME_SOURCE_REVIEW_READY_V1',source_only=True,control_plan_pin=pp,complete_source_file_pins=author['whole_Source_file_pins'],host_source_pin=next(p for p in author['whole_Source_file_pins']if Path(p['path']).name=='run_guarded_B_plane2_minimal_runtime_build.UNREADY.py'),contract_Source_pin=m.pin_source(q),dependencies=m.unique([json.loads(a.admission_packet_pin),pp]+packet['explicit_control_metadata_pins']),original_caps=m.CAPS,Source_or_compiler_business_executed=False)
 m.write_once(BASE/'SOURCE_REVIEW_READY.json',ready);print(json.dumps(dict(status='B_PLANE2_RUNTIME_BUILD_SOURCE_PREPARED_ONLY',ready_pin=m.pin_source(BASE/'SOURCE_REVIEW_READY.json'),compiler_executed=False,native_executed=False)),flush=True)
if __name__=='__main__':main()
