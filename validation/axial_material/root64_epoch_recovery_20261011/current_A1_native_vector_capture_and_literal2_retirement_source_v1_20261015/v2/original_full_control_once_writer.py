"""Publish one reviewed Source/Host freeze and original24-argument recipe."""
import argparse,json,os
from pathlib import Path
import control_source_common as c

def main():
    ap=argparse.ArgumentParser(allow_abbrev=False)
    for k in ('source-review-pin','source-review-tools-pin','source-generation-tools-pin'):ap.add_argument('--'+k,required=True)
    args=ap.parse_args()
    ready_pin=c.pin(c.BASE/'SOURCE_REVIEW_READY.json',64*2**20);ready=c.read(ready_pin)
    plan=c.read(ready['plan_pin']);c.check_finite(plan)
    peer_pin=json.loads(args.source_review_pin);peer_tools=json.loads(args.source_review_tools_pin)
    generation_pin=json.loads(args.source_generation_tools_pin)
    peer=c.read(peer_pin)
    selected=c.unique([ready_pin,ready['plan_pin'],ready['author_source_freeze_pin'],ready['worker_source_pin'],ready['host_source_pin']]
        +c.read(ready['author_source_freeze_pin'])['source_pins'])
    c.require(peer['status'].startswith('PASS') and peer.get('failure') is None
        and all(c.contains(peer,p) for p in selected),'same-round actual complete Source-only review pending')
    c.closed0(c.read(peer_tools),'actual_review_return',peer_pin,'review_pin')
    c.closed0(c.read(generation_pin),'actual_Source_preparation_return',ready_pin,'ready_pin')
    for p in selected:c.require(c.pin(p['path'])==p,'selected current Source bytes unchanged')
    dependencies=c.unique(plan['source_dependency_pins']+selected+[peer_pin,peer_tools,generation_pin])
    for p in dependencies:c.current(p)
    sf=c.write(c.BASE/'COMPLETE_FULL370_REAL_OPERATOR_CONTROL_SOURCE_ONLY_FREEZE.json',dict(
        schema='COMPLETE_FULL370_REAL_OPERATOR_CONTROL_SOURCE_ONLY_FREEZE_V1',source_only=True,
        compiler_executed=False,numerical_executed=False,business_executed=False,original_caps=c.CAPS,
        control_plan_pin=ready['plan_pin'],selected_Source_pins=selected,same_round_Source_review_pin=peer_pin,
        same_round_Source_tools_pin=peer_tools,actual_Source_generation_tool_pin=generation_pin,
        actual_control_report_pin=None,**c.FALSE))
    hf=c.write(c.BASE/'COMPLETE_FULL370_REAL_OPERATOR_CONTROL_HOST_SOURCE_ONLY_FREEZE.json',dict(
        schema='COMPLETE_FULL370_REAL_OPERATOR_CONTROL_HOST_SOURCE_ONLY_FREEZE_V1',source_only=True,
        compiler_executed=False,numerical_executed=False,business_executed=False,original_caps=c.CAPS,
        host_source_pin=ready['host_source_pin'],selected_source_freeze_pin=sf,dependencies=dependencies+[sf],
        actual_control_report_pin=None,**c.FALSE))
    old=c.read(c.pin(c.V6/'ROOT_REVIEWABLE_ONE_ACTUAL_TRACK_COMPONENT_CONTROL_ARGV.json',64*2**20))
    argv=old['argv'][:11]+[ready['host_source_pin']['path']]
    for role,p in (('source-freeze',sf),('host-freeze',hf)):
        argv+=['--'+role+'-summary',p['path'],'--'+role+'-sha256',p['sha256'],
            '--'+role+'-seven-id',json.dumps(p['identity'],separators=(',',':'))]
    c.require(len(argv)==24,'unchanged original env11/host/two exact fullPF triples')
    cli=c.write(c.BASE/'ROOT_REVIEWABLE_FULL370_REAL_OPERATOR_CONTROL_ARGV.json',dict(
        schema='ROOT_REVIEWABLE_FULL370_REAL_OPERATOR_CONTROL_ARGV_V1',argv=argv,is_complete_executable_argv=True,
        source_freeze_pin=sf,host_freeze_pin=hf,planned_actual_output_root=str(c.OUT),actual_control_report_pin=None,**c.FALSE))
    fd=os.open(c.BASE,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)
    print(json.dumps(dict(status='FULL370_REAL_OPERATOR_CONTROL_SF_HF_CLI24_PUBLISHED_ONLY',
        Source_freeze_pin=sf,Host_freeze_pin=hf,CLI_pin=cli,compiler_executed=False,numerical_executed=False,**c.FALSE)),flush=True)

if __name__=='__main__':main()
