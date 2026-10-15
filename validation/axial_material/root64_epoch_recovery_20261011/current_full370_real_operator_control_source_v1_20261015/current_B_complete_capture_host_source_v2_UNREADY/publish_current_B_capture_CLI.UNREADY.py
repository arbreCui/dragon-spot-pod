"""Root-only future Source publication after genuine SourceGEN0 and independent review0."""
import argparse,importlib.util,json,os,shlex
from pathlib import Path
BASE=Path(__file__).absolute().parent
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for name in('review-pin','review-tools-pin','generation-tools-pin'):ap.add_argument('--'+name,required=True)
 a=ap.parse_args();spec=importlib.util.spec_from_file_location('B_capture_publish_contract',BASE/'capture_Source_contract.UNREADY.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 ready=m.metadata(m.pin(BASE/'SOURCE_REVIEW_READY.json'));plan=m.metadata(ready['control_plan_pin']);pr=json.loads(a.review_pin);pt=json.loads(a.review_tools_pin);pg=json.loads(a.generation_tools_pin);review=m.metadata(pr);tools=m.metadata(pt);generation=m.metadata(pg)
 m.genuine(tools,'actual_review_return',pr,'review_pin');m.genuine(generation,'actual_Source_preparation_return',m.pin(BASE/'SOURCE_REVIEW_READY.json'),'ready_pin')
 m.need(review['source_only']is True and review['status']=='PASS_SOURCE_ONLY_CURRENT_B_COMPLETE_CAPTURE'and review['failure']is None and review['control_plan_pin']==ready['control_plan_pin']and review['complete_source_file_pins']==ready['complete_source_file_pins'],'same-round independent complete Source review0')
 for p in ready['complete_source_file_pins']:m.need(m.pin(p['path'])==p,'all original author-frozen Source through publication')
 for n in('FINAL_SOURCE_FREEZE.json','FINAL_HOST_FREEZE.json','FINAL_ROOT_REVIEWABLE_CLI.json'):m.need(not os.path.lexists(BASE/n),'publication once and no overwrite')
 sf=dict(schema='CURRENT_B_COMPLETE_CAPTURE_SOURCE_FREEZE_V1',source_only=True,native_executed=False,control_plan_pin=ready['control_plan_pin'],complete_source_file_pins=ready['complete_source_file_pins'],independent_Source_review_pin=pr,independent_Source_review_tools_pin=pt,Root_Source_generation_true_tools_pin=pg)
 m.write(BASE/'FINAL_SOURCE_FREEZE.json',sf);psf=m.pin(BASE/'FINAL_SOURCE_FREEZE.json')
 hf=dict(schema='CURRENT_B_COMPLETE_CAPTURE_HOST_FREEZE_V1',source_only=True,selected_source_freeze_pin=psf,host_source_pin=ready['host_source_pin'],contract_Source_pin=ready['contract_Source_pin'],original_caps=m.CAPS,explicit_cumulative_metadata_file_pins=m.unique(plan['explicit_cumulative_metadata_file_pins']+[pr,pt,pg,psf,ready['control_plan_pin']]),Root_actual_exec_command_sandbox_permissions_required='require_escalated',native_executed=False)
 m.write(BASE/'FINAL_HOST_FREEZE.json',hf);phf=m.pin(BASE/'FINAL_HOST_FREEZE.json');argv=plan['original_complete_ENV_Python_B_prefix']+[ready['host_source_pin']['path']]
 for role,p in(('source-freeze',psf),('host-freeze',phf)):argv+=['--'+role+'-summary',p['path'],'--'+role+'-sha256',p['sha256'],'--'+role+'-seven-id',json.dumps(p['identity'],separators=(',',':'))]
 m.need(len(argv)==24,'original complete24 owning Root argv')
 cli=dict(schema='CURRENT_B_CAPTURE_FINAL_REVIEWABLE_ROOT_CLI_V1',argv=argv,command=shlex.join(argv),source_freeze_pin=psf,host_freeze_pin=phf,Root_actual_exec_command_sandbox_permissions_required='require_escalated',original_caps=m.CAPS,native_executed=False,**m.FALSE)
 m.write(BASE/'FINAL_ROOT_REVIEWABLE_CLI.json',cli);print(json.dumps(dict(status='CURRENT_B_CAPTURE_FINAL_CLI_PUBLISHED_ONLY',CLI_pin=m.pin(BASE/'FINAL_ROOT_REVIEWABLE_CLI.json'),native_executed=False)),flush=True)
if __name__=='__main__':main()
