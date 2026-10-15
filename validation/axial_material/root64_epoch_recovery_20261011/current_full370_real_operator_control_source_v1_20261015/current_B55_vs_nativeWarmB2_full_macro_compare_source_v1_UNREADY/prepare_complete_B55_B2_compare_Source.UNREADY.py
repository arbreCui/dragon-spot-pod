"""Root-only full B2 Source preparation. No physical walker or algorithm executes."""
import argparse,ast,hashlib,importlib.util,json,os,time
from pathlib import Path
BASE=Path(__file__).absolute().parent
def main():
 started=time.monotonic();ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--admission-packet-pin',required=True);a=ap.parse_args()
 with(BASE/'ROOT_SOURCE_PREPARATION_CLAIM.json').open('x')as f:json.dump(dict(schema='ROOT_B55_B2_COMPLETE_COMPARISON_SOURCE_PREPARATION_ONCE_V1',PID=os.getpid(),original_started=started,claim_before_project_import=True,decoder_executed=False),f);f.write('\n');f.flush();os.fsync(f.fileno())
 q=BASE/'B55_B2_compare_Source_contract.UNREADY.py';spec=importlib.util.spec_from_file_location('B2_Source_preparation_contract',q);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 m.need(not any(os.path.lexists(BASE/n)for n in('PLAN.json','SOURCE_REVIEW_READY.json')),'Source generation once without overwrite')
 pa=m.pin(BASE/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json');author=m.metadata(pa);m.need(author['Source_only_frozen_before_Root_generation']is True and author['native_or_compiler_executed_by_author']is False and author['Source_preparer_or_publisher_executed_by_author']is False,'author froze Source only; Root sole GEN')
 for p in author['whole_Source_file_pins']:m.need(m.pin(p['path'])==p,'all whole frozen Source intact');ast.parse(Path(p['path']).read_text())
 ppkt=json.loads(a.admission_packet_pin);packet=m.metadata(ppkt);build,bm,extractplan,extraction,post=m.admit(packet)
 resources=m.Resources(packet,build,bm,packet['explicit_cumulative_metadata_file_pins']+author['whole_Source_file_pins']+[pa,ppkt],started,600);before=resources.check();m.admit_reservation(packet,before)
 plan=dict(packet,schema='CURRENT_B55_B2_COMPLETE_COMPARISON_SOURCE_ONLY_PLAN_V1',source_only=True,Source_generation_science_payload_decoded=False,Source_generation_worker_or_native_executed=False,Source_only_resource_snapshot=before,**m.FALSE)
 m.write(BASE/'PLAN.json',plan);pp=m.pin(BASE/'PLAN.json');table={Path(p['path']).name:p for p in author['whole_Source_file_pins']}
 ready=dict(schema='CURRENT_B55_B2_COMPLETE_TYPED_COMPARISON_SOURCE_REVIEW_READY_V1',source_only=True,control_plan_pin=pp,complete_source_file_pins=author['whole_Source_file_pins'],host_source_pin=table['run_guarded_complete_B55_B2_typed_compare.UNREADY.py'],contract_Source_pin=table['B55_B2_compare_Source_contract.UNREADY.py'],dependencies=m.unique([ppkt,pp,pa]+packet['explicit_cumulative_metadata_file_pins']),original_caps=m.CAPS,Source_or_decoder_or_native_business_executed=False)
 m.write(BASE/'SOURCE_REVIEW_READY.json',ready);resources.check();print(json.dumps(dict(status='CURRENT_B55_B2_COMPLETE_TYPED_COMPARISON_SOURCE_PREPARED_ONLY',ready_pin=m.pin(BASE/'SOURCE_REVIEW_READY.json'),decoder_executed=False,native_executed=False)),flush=True)
if __name__=='__main__':main()
