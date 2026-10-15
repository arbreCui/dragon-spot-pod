"""One reviewed full58 diagnostic Source/Host freeze; original24-argument recipe."""
import argparse,json,os
from pathlib import Path
import control_source_common as c

def main():
    ap=argparse.ArgumentParser(allow_abbrev=False)
    for n in ('source-review-pin','source-review-tools-pin','source-generation-tools-pin'):ap.add_argument('--'+n,required=True)
    a=ap.parse_args();receipt=c.BASE/'FINAL_PUBLICATION_RECEIPT.json';r=dict(schema='FULL370_COMPACT_INPUT_ONCE_PUBLICATION_RECEIPT_V1',status='CLAIMED_ONCE_SOURCE_PUBLICATION',failure=None,business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,**c.FALSE)
    with receipt.open('xb') as f:
        try:
            c.snapshot(f,r);ready_pin=c.pin(c.BASE/'SOURCE_REVIEW_READY.json',64*2**20);ready=c.read(ready_pin);plan=c.read(ready['plan_pin']);c.check_finite(plan)
            peerpin=json.loads(a.source_review_pin);tools=json.loads(a.source_review_tools_pin);gen=json.loads(a.source_generation_tools_pin);peer=c.read(peerpin)
            selected=c.unique([ready_pin,ready['plan_pin'],ready['author_source_freeze_pin'],ready['worker_source_pin'],ready['host_source_pin'],ready['original_Source_inverse_proof_pin']]+ready['selected_Source_and_metadata_pins'])
            c.require(peer['status'].startswith('PASS') and peer.get('failure') is None and all(c.contains(peer,p) for p in selected+[gen]) and all(peer.get(k,False) is False for k in ('business_executed','numerical_executed','compiler_executed','files_deleted')),'same-round complete selected Source/metadata/READY/GEN peer0 only')
            c.closed0(c.read(tools),'actual_review_return',peerpin,'review_pin');c.closed0(c.read(gen),'actual_Source_preparation_return',ready_pin,'ready_pin')
            for p in selected:c.require(c.pin(p['path'])==p,'selected current whole Source/metadata unchanged')
            dependencies=c.unique(plan['source_dependency_pins']+selected+[peerpin,tools,gen])
            c.require(all(p['path'] not in c.RETIRED_PATHS for p in dependencies),'old A1 pair historical only, never live dependencies')
            for p in dependencies:c.current(p)
            metadata=c.unique(plan['explicit_cumulative_metadata_file_pins']+[p for p in dependencies if p not in plan['scientific_input_current7_pins']])
            sf=c.write(c.BASE/'COMPLETE_FULL370_REAL_OPERATOR_CONTROL_SOURCE_ONLY_FREEZE.json',dict(schema='COMPLETE_FULL370_REAL_OPERATOR_CONTROL_SOURCE_ONLY_FREEZE_V1',source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False,original_caps=c.CAPS,control_plan_pin=ready['plan_pin'],selected_Source_pins=selected,same_round_Source_review_pin=peerpin,same_round_Source_tools_pin=tools,actual_Source_generation_tool_pin=gen,actual_control_report_pin=None,**c.FALSE))
            hf=c.write(c.BASE/'COMPLETE_FULL370_REAL_OPERATOR_CONTROL_HOST_SOURCE_ONLY_FREEZE.json',dict(schema='COMPLETE_FULL370_REAL_OPERATOR_CONTROL_HOST_SOURCE_ONLY_FREEZE_V1',source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False,original_caps=c.CAPS,host_source_pin=ready['host_source_pin'],selected_source_freeze_pin=sf,dependencies=dependencies+[sf],explicit_cumulative_metadata_file_pins=metadata,actual_control_report_pin=None,**c.FALSE))
            old=c.read(c.pin(c.V6/'ROOT_REVIEWABLE_ONE_ACTUAL_TRACK_COMPONENT_CONTROL_ARGV.json',64*2**20));argv=old['argv'][:11]+[ready['host_source_pin']['path']]
            for role,p in (('source-freeze',sf),('host-freeze',hf)):argv+=['--'+role+'-summary',p['path'],'--'+role+'-sha256',p['sha256'],'--'+role+'-seven-id',json.dumps(p['identity'],separators=(',',':'))]
            c.require(len(argv)==24,'unchanged original env11/host/two exact fullPF triples')
            cli=c.write(c.BASE/'ROOT_REVIEWABLE_FULL370_REAL_OPERATOR_CONTROL_ARGV.json',dict(schema='ROOT_REVIEWABLE_FULL370_REAL_OPERATOR_CONTROL_ARGV_V1',argv=argv,is_complete_executable_argv=True,source_freeze_pin=sf,host_freeze_pin=hf,planned_actual_output_root=str(c.OUT),actual_control_report_pin=None,**c.FALSE))
            r.update(status='FULL370_REAL_OPERATOR_CONTROL_SF_HF_CLI24_PUBLISHED_ONLY',source_freeze_pin=sf,host_freeze_pin=hf,CLI_pin=cli);c.snapshot(f,r)
        except BaseException as error:r.update(status='FAILED_ONCE_SOURCE_PUBLICATION_NO_RETRY',failure=repr(error));c.snapshot(f,r);raise
    fd=os.open(c.BASE,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)
    print(json.dumps(dict(status=r['status'],Source_freeze_pin=sf,Host_freeze_pin=hf,CLI_pin=cli,publication_receipt_pin=c.pin(receipt),compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False,**c.FALSE)),flush=True)
if __name__=='__main__':main()
