"""Root-only metadata publication after genuine independent Source review0."""
import argparse,importlib.util,json,os,shlex
from pathlib import Path
BASE=Path(__file__).absolute().parent
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--review-pin',required=True);ap.add_argument('--review-tools-pin',required=True);a=ap.parse_args()
 spec=importlib.util.spec_from_file_location('B_PLANE2_RUNTIME_publish_contract',BASE/'build_B_plane2_runtime_Source_contract.UNREADY.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 ready=m.metadata(m.pin_source(BASE/'SOURCE_REVIEW_READY.json'));plan=m.load_plan(ready['control_plan_pin']);pr=json.loads(a.review_pin);pt=json.loads(a.review_tools_pin);review=m.metadata(pr);tools=m.metadata(pt)
 m.genuine(tools,'actual_review_return',pr,'review_pin')
 m.need(review['source_only']is True and review['status']=='PASS_SOURCE_ONLY_B_PLANE2_MINIMAL_RUNTIME_COMPLETE71_BUILD'and review['failure']is None and review['control_plan_pin']==ready['control_plan_pin']and review['complete_source_file_pins']==ready['complete_source_file_pins'],'same actual independent Source-only review0; no business qualification')
 for p in ready['complete_source_file_pins']:m.need(m.pin_source(p['path'])==p,'whole Source bytes frozen through publication')
 for n in('FINAL_SOURCE_FREEZE.json','FINAL_HOST_FREEZE.json','FINAL_ROOT_REVIEWABLE_CLI.json'):m.need(not os.path.lexists(BASE/n),'final publication once/no overwrite')
 sf=dict(schema='B_PLANE2_RUNTIME_SOURCE_FREEZE_V1',source_only=True,business_executed=False,control_plan_pin=ready['control_plan_pin'],complete_source_file_pins=ready['complete_source_file_pins'],independent_Source_review_pin=pr,independent_Source_review_tools_pin=pt)
 m.write_once(BASE/'FINAL_SOURCE_FREEZE.json',sf);psf=m.pin_source(BASE/'FINAL_SOURCE_FREEZE.json')
 hf=dict(schema='B_PLANE2_RUNTIME_HOST_FREEZE_V1',source_only=True,selected_source_freeze_pin=psf,host_source_pin=ready['host_source_pin'],contract_Source_pin=ready['contract_Source_pin'],original_caps=m.CAPS,explicit_cumulative_metadata_file_pins=m.unique(plan['explicit_cumulative_metadata_file_pins']+[pr,pt,psf,ready['control_plan_pin']]),Root_actual_exec_command_sandbox_permissions_required='require_escalated',compiler_executed=False)
 m.write_once(BASE/'FINAL_HOST_FREEZE.json',hf);phf=m.pin_source(BASE/'FINAL_HOST_FREEZE.json');argv=plan['original_complete_ENV_Python_B_prefix']+[ready['host_source_pin']['path']]
 for role,p in(('source-freeze',psf),('host-freeze',phf)):argv+=['--'+role+'-summary',p['path'],'--'+role+'-sha256',p['sha256'],'--'+role+'-seven-id',json.dumps(p['identity'],separators=(',',':'))]
 m.need(len(argv)==24,'original complete24 owning Root argv')
 cli=dict(schema='B_PLANE2_RUNTIME_BUILD_FINAL_REVIEWABLE_ROOT_CLI_V1',argv=argv,command=shlex.join(argv),source_freeze_pin=psf,host_freeze_pin=phf,Root_actual_exec_command_sandbox_permissions_required='require_escalated',original_caps=m.CAPS,compiler_executed=False,native_executed=False,**m.FALSE)
 m.write_once(BASE/'FINAL_ROOT_REVIEWABLE_CLI.json',cli);print(json.dumps(dict(status='B_PLANE2_RUNTIME_BUILD_FINAL_CLI_PUBLISHED_ONLY',CLI_pin=m.pin_source(BASE/'FINAL_ROOT_REVIEWABLE_CLI.json'),compiler_executed=False,native_executed=False)),flush=True)
if __name__=='__main__':main()
