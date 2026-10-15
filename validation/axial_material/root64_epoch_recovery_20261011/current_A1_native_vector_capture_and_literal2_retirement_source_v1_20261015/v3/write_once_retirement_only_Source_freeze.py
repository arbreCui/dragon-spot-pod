"""Publish only a reviewed retirement Source freeze; no capture HF/CLI."""
import argparse,json
from pathlib import Path
import capture_source_common as c
BASE=Path(__file__).absolute().parent

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in ('source-review-pin','source-review-tools-pin','source-generation-tools-pin'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();path=BASE/'RETIREMENT_SOURCE_PUBLICATION_RECEIPT.json';r=dict(schema='RETIREMENT_ONLY_ONCE_SOURCE_PUBLICATION_RECEIPT_V1',status='CLAIMED_ONCE_RETIREMENT_SOURCE_ONLY',failure=None,business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,capture_republished=False,capture_rerun=False,**c.FALSE)
 with path.open('xb') as f:
  try:
   c.snapshot(f,r);pr=c.pin(BASE/'SOURCE_REVIEW_READY.json');ready=c.read(pr);pp=ready['plan_pin'];plan=c.read(pp)
   peerpin=json.loads(a.source_review_pin);tools=json.loads(a.source_review_tools_pin);gen=json.loads(a.source_generation_tools_pin);peer=c.read(peerpin)
   selected=c.unique([pr,pp]+ready['selected_Source_and_metadata_pins'])
   c.require(peer['status'].startswith('PASS') and peer['failure'] is None and all(c.contains(peer,p) for p in selected+[gen]) and all(peer.get(k,False) is False for k in ('business_executed','numerical_executed','compiler_executed','files_deleted')),'actual complete retirement Source-only selected/READY/GEN review')
   c.closed0(c.read(tools),'actual_review_return',peerpin,'review_pin');c.closed0(c.read(gen),'actual_Source_preparation_return',pr,'ready_pin')
   for p in selected:c.require(c.pin(p['path'])==p,'reviewed whole Source/metadata bytes unchanged')
   sf=c.write(BASE/'RETIREMENT_SOURCE_ONLY_FREEZE.json',dict(schema='RETIREMENT_ONLY_REVIEWED_SOURCE_FREEZE_V1',source_only=True,control_plan_pin=pp,selected_retirement_source_pin=ready['retirement_source_pin'],selected_Source_and_metadata_pins=selected,same_round_Source_review_pin=peerpin,same_round_Source_tools_pin=tools,actual_Source_generation_tool_pin=gen,original_capture_plan_pin=plan['original_capture_plan_pin'],original_capture_source_freeze_pin=plan['original_capture_source_freeze_pin'],complete_joint_roots=plan['complete_joint_roots'],original_caps=c.CAPS,business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,capture_republished=False,capture_rerun=False,**c.FALSE))
   r.update(status='RETIREMENT_ONLY_REVIEWED_SOURCE_FREEZE_PUBLISHED_ONLY',retirement_source_freeze_pin=sf);c.snapshot(f,r)
  except BaseException as error:r.update(status='FAILED_ONCE_RETIREMENT_SOURCE_PUBLICATION_NO_RETRY',failure=repr(error));c.snapshot(f,r);raise
 print(json.dumps(dict(status=r['status'],retirement_source_freeze_pin=sf,publication_receipt_pin=c.pin(path),business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,**c.FALSE)),flush=True)
if __name__=='__main__':main()
