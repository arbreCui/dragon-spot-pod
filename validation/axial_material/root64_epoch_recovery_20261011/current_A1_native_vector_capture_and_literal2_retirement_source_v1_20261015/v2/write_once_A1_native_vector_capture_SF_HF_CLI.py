"""One reviewed Source/Host publication and the original env11/host/12 argv."""
import argparse,json,os
from pathlib import Path
import capture_source_common as c

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for k in ('source-review-pin','source-review-tools-pin','source-generation-tools-pin'):ap.add_argument('--'+k,required=True)
 a=ap.parse_args();receipt_path=c.BASE/'FINAL_PUBLICATION_RECEIPT.json';r=dict(schema='A1_NATIVE_VECTOR_CAPTURE_ONCE_PUBLICATION_RECEIPT_V1',status='CLAIMED_ONCE_SOURCE_PUBLICATION',failure=None,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False,**c.FALSE)
 with receipt_path.open('xb') as f:
  try:
   c.snapshot(f,r);ready_pin=c.pin(c.BASE/'SOURCE_REVIEW_READY.json');ready=c.read(ready_pin);plan=c.read(ready['plan_pin']);c.check_finite(plan['finite_prerequisite_pins'],plan['finite_post_schema'],plan['finite_post_status'])
   peer_pin=json.loads(a.source_review_pin);peer_tools=json.loads(a.source_review_tools_pin);generation_pin=json.loads(a.source_generation_tools_pin);peer=c.read(peer_pin)
   selected=c.unique([ready_pin,ready['plan_pin'],ready['author_source_freeze_pin'],ready['original_Source_proof_pin']]+ready['source_pins']+ready['selected_metadata_pins'])
   c.require(peer['status'].startswith('PASS') and peer.get('failure') is None and all(c.contains(peer,p) for p in selected+[generation_pin]) and all(peer.get(k,False) is False for k in ('business_executed','numerical_executed','compiler_executed','files_deleted')),'same-round actual complete selected Source/metadata/READY/GEN review only')
   c.closed0(c.read(peer_tools),'actual_review_return',peer_pin,'review_pin');c.closed0(c.read(generation_pin),'actual_Source_preparation_return',ready_pin,'ready_pin')
   for p in selected:c.require(c.pin(p['path'])==p,'selected current whole Source/metadata bytes unchanged')
   dependencies=c.unique(plan['source_dependency_pins']+selected+[peer_pin,peer_tools,generation_pin])
   for p in dependencies:c.current(p)
   sf=c.write(c.BASE/'FINAL_SOURCE_FREEZE.json',dict(schema='A1_NATIVE_VECTOR_CAPTURE_SOURCE_ONLY_FREEZE_V1',source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False,original_caps=c.CAPS,control_plan_pin=ready['plan_pin'],selected_Source_pins=selected,same_round_Source_review_pin=peer_pin,same_round_Source_tools_pin=peer_tools,actual_Source_generation_tool_pin=generation_pin,actual_control_report_pin=None,**c.FALSE))
   hf=c.write(c.BASE/'FINAL_HOST_FREEZE.json',dict(schema='A1_NATIVE_VECTOR_CAPTURE_HOST_SOURCE_ONLY_FREEZE_V1',source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False,original_caps=c.CAPS,host_source_pin=ready['host_source_pin'],selected_source_freeze_pin=sf,dependencies=dependencies+[sf],explicit_cumulative_metadata_file_pins=c.unique(plan['explicit_cumulative_metadata_file_pins']+[peer_pin,peer_tools,generation_pin]),actual_control_report_pin=None,**c.FALSE))
   old=c.read(c.pin(c.V6/'ROOT_REVIEWABLE_ONE_ACTUAL_TRACK_COMPONENT_CONTROL_ARGV.json'));argv=old['argv'][:11]+[ready['host_source_pin']['path']]
   for role,p in (('source-freeze',sf),('host-freeze',hf)):argv+=['--'+role+'-summary',p['path'],'--'+role+'-sha256',p['sha256'],'--'+role+'-seven-id',json.dumps(p['identity'],separators=(',',':'))]
   c.require(len(argv)==24,'unchanged original env11/host/two exact fullPF triples')
   cli=c.write(c.BASE/'FINAL_ROOT_REVIEWABLE_CLI.json',dict(schema='A1_NATIVE_VECTOR_CAPTURE_ROOT_REVIEWABLE_CLI_V1',argv=argv,is_complete_executable_argv=True,source_freeze_pin=sf,host_freeze_pin=hf,planned_actual_output_root=str(c.OUT),actual_control_report_pin=None,**c.FALSE))
   r.update(status='A1_NATIVE_VECTOR_CAPTURE_SF_HF_CLI24_PUBLISHED_ONLY',source_freeze_pin=sf,host_freeze_pin=hf,CLI_pin=cli);c.snapshot(f,r)
  except BaseException as error:r.update(status='FAILED_ONCE_SOURCE_PUBLICATION_RETAINED_NO_RETRY',failure=repr(error));c.snapshot(f,r);raise
 fd=os.open(c.BASE,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status=r['status'],Source_freeze_pin=sf,Host_freeze_pin=hf,CLI_pin=cli,publication_receipt_pin=c.pin(receipt_path),compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False,**c.FALSE)),flush=True)
if __name__=='__main__':main()
