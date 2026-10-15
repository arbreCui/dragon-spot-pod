"""Root-only aggregate Source preparation; no worker, native, compiler or decoder."""
import argparse,ast,importlib.util,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
def need(v,m):
 if v is not True:raise RuntimeError(m)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--admission-packet-pin',required=True);a=ap.parse_args()
 need(not any(os.path.lexists(BASE/n)for n in('PLAN.json','SOURCE_REVIEW_READY.json')),'fresh once Source generation, no overwrite or retry')
 q=BASE/'aggregate_Source_contract.UNREADY.py';spec=importlib.util.spec_from_file_location('B_aggregate_prepare_contract',q);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 author=m.metadata(m.pin(BASE/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json'));need(author['Source_only_frozen_before_Root_generation']is True and author['native_or_compiler_executed_by_author']is False and author['Source_preparer_or_publisher_executed_by_author']is False,'author Source-only freeze, Root sole executor')
 for p in author['whole_Source_file_pins']:need(m.pin(p['path'])==p,'all author frozen Source intact')
 packet=m.metadata(json.loads(a.admission_packet_pin));build,bm,manifest,binding,state,extraction,extraction_post=m.admit(packet)
 need(packet['source_role_pin_audit_complete']is True and packet['only_current_stage']=='aggregate','actual capture/post/latest field audit and aggregate-only stage mandatory')
 before=0
 for root in packet['complete_joint_roots']:
  if not Path(root).exists():continue
  for p in Path(root).rglob('*'):
   s=p.lstat();need(not stat.S_ISLNK(s.st_mode),'entire joint namespace no alias')
   if stat.S_ISREG(s.st_mode):before+=s.st_size
 for p in packet['explicit_cumulative_metadata_file_pins']:
  bm.current_metadata_role(p,build)
  if not any(Path(p['path']).is_relative_to(Path(r))for r in packet['complete_joint_roots']):before+=p['size_bytes']
 need(before+m.OUTPUT_BOUND+m.SOURCE_BOUND<2*2**30,'entire latest prefix+full aggregate320MiB+Source16MiB within original2GiB; actual Root rechecks original resources/open-unlinked')
 for p in author['whole_Source_file_pins']:
  if p['path'].endswith('.py'):ast.parse(Path(p['path']).read_text())
 table={Path(p['path']).name:p for p in author['whole_Source_file_pins']};plan=dict(packet,schema='CURRENT_B_COMPLETE_AGGREGATE_SOURCE_ONLY_PLAN_V1',source_only=True,Source_only_cumulative_bytes_before_reservations=before,Source_generation_science_bodies_decoded=False,Source_generation_decoder_or_native_executed=False,**m.FALSE)
 m.write(BASE/'PLAN.json',plan);pp=m.pin(BASE/'PLAN.json');ready=dict(schema='CURRENT_B_COMPLETE_AGGREGATE_SOURCE_REVIEW_READY_V1',source_only=True,control_plan_pin=pp,complete_source_file_pins=author['whole_Source_file_pins'],host_source_pin=table['run_guarded_current_B_complete_aggregate.UNREADY.py'],contract_Source_pin=table['aggregate_Source_contract.UNREADY.py'],dependencies=m.unique([json.loads(a.admission_packet_pin),pp]+packet['explicit_control_metadata_pins']),original_caps=m.CAPS,Source_or_decoder_or_native_business_executed=False)
 m.write(BASE/'SOURCE_REVIEW_READY.json',ready);print(json.dumps(dict(status='CURRENT_B_COMPLETE_AGGREGATE_SOURCE_PREPARED_ONLY',ready_pin=m.pin(BASE/'SOURCE_REVIEW_READY.json'),decoder_executed=False,native_executed=False)),flush=True)
if __name__=='__main__':main()
