"""Root-only B2 extraction CLI publication after genuine GEN0 and independent Source0."""
import argparse,importlib.util,json,os,shlex
from pathlib import Path
BASE=Path(__file__).absolute().parent
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in('review-pin','review-tools-pin','generation-tools-pin'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();spec=importlib.util.spec_from_file_location('B2_extract_publisher_contract',BASE/'B55_B2_compare_Source_contract.UNREADY.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 ready_pin=m.pin(BASE/'SOURCE_REVIEW_READY.json');ready=m.metadata(ready_pin);plan=m.metadata(ready['control_plan_pin']);pr=json.loads(a.review_pin);pt=json.loads(a.review_tools_pin);pg=json.loads(a.generation_tools_pin);review=m.metadata(pr)
 m.genuine(m.metadata(pt),'actual_review_return',pr,'review_pin');m.genuine(m.metadata(pg),'actual_Source_preparation_return',ready_pin,'ready_pin')
 m.need(review['source_only']is True and review['status']=='PASS_SOURCE_ONLY_CURRENT_B55_B2_COMPLETE_TYPED_COMPARISON'and review['failure']is None and review['control_plan_pin']==ready['control_plan_pin']and review['complete_source_file_pins']==ready['complete_source_file_pins'],'same-round complete independent Source0 and actual GEN0, no algorithm output claimed')
 m.admit(plan)
 for p in ready['complete_source_file_pins']:m.need(m.pin(p['path'])==p,'whole author frozen Source')
 for n in('FINAL_SOURCE_FREEZE.json','FINAL_HOST_FREEZE.json','FINAL_ROOT_REVIEWABLE_CLI.json'):m.need(not os.path.lexists(BASE/n),'final publication once, no overwrite')
 sf=dict(schema='COMPLETE_CURRENT_B55_B2_TYPED_COMPARISON_SOURCE_ONLY_FREEZE_V1',candidate_executed=False,source_only=True,control_plan_pin=ready['control_plan_pin'],complete_source_file_pins=ready['complete_source_file_pins'],independent_Source_review_pin=pr,independent_Source_review_tools_pin=pt,Root_Source_generation_true_tools_pin=pg)
 m.write(BASE/'FINAL_SOURCE_FREEZE.json',sf);psf=m.pin(BASE/'FINAL_SOURCE_FREEZE.json')
 hf=dict(schema='CURRENT_B55_B2_COMPLETE_COMPARISON_HOST_FREEZE_V1',source_only=True,selected_source_freeze_pin=psf,host_source_pin=ready['host_source_pin'],contract_Source_pin=ready['contract_Source_pin'],independent_Source_review_pin=pr,independent_Source_review_tools_pin=pt,original_caps=m.CAPS,explicit_cumulative_metadata_file_pins=m.unique(plan['explicit_cumulative_metadata_file_pins']+[pr,pt,pg,psf,ready['control_plan_pin'],ready_pin]+ready['complete_source_file_pins']),Root_actual_exec_command_sandbox_permissions_required='require_escalated',decoder_executed=False)
 m.write(BASE/'FINAL_HOST_FREEZE.json',hf);phf=m.pin(BASE/'FINAL_HOST_FREEZE.json');argv=plan['original_complete_ENV_Python_B_prefix']+[ready['host_source_pin']['path']]
 for role,p in(('source-freeze',psf),('host-freeze',phf)):argv+=['--'+role+'-summary',p['path'],'--'+role+'-sha256',p['sha256'],'--'+role+'-seven-id',json.dumps(p['identity'],separators=(',',':'))]
 m.need(len(argv)==24,'complete original24 owning Root argv')
 cli=dict(schema='CURRENT_B55_B2_COMPLETE_TYPED_COMPARISON_FINAL_ROOT_CLI_V1',argv=argv,command=shlex.join(argv),source_freeze_pin=psf,host_freeze_pin=phf,Root_actual_exec_command_sandbox_permissions_required='require_escalated',original_caps=m.CAPS,decoder_executed=False,native_executed=False,comparison_executed=False,**m.FALSE)
 m.write(BASE/'FINAL_ROOT_REVIEWABLE_CLI.json',cli);print(json.dumps(dict(status='CURRENT_B55_B2_COMPLETE_TYPED_COMPARISON_FINAL_CLI_PUBLISHED_ONLY',CLI_pin=m.pin(BASE/'FINAL_ROOT_REVIEWABLE_CLI.json'),decoder_executed=False,native_executed=False)),flush=True)
if __name__=='__main__':main()
