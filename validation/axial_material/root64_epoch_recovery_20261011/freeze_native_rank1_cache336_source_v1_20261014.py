#!/usr/bin/env python3
"""Source-only freeze after one genuine independent exact Source review."""
import argparse
import importlib.util
import json
import os
from pathlib import Path

REC = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
PREP = REC/'prepare_native_rank1_cache336_source_v1_20261014.py'
OUT = REC/'native_rank1_exact_cache336_source_v1_20261014'
SF = OUT/'COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_AND_CONTROL_SOURCE_FREEZE.json'

def contained(data,pin):
    if isinstance(data,dict):
        if data == pin:
            return True
        return any(contained(value,pin) for value in data.values())
    return isinstance(data,list) and any(contained(value,pin) for value in data)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--peer-review',required=True)
    p.add_argument('--peer-true-tools',required=True)
    a=p.parse_args()
    # This imports only the owning Source preparer definitions, never Host/math.
    spec=importlib.util.spec_from_file_location('cache336_exact_source_preparer',PREP)
    s=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(s)
    ready_bytes,ready_pin=s.read(OUT/'SOURCE_ONLY_READY.json')
    ready=json.loads(ready_bytes)
    plan_bytes,plan_pin=s.read(OUT/'CACHE336_EXACT_BIT_CONTROL_AND_RUNTIME_PLAN.json')
    plan=json.loads(plan_bytes)
    review_bytes,review_pin=s.read(a.peer_review)
    review=json.loads(review_bytes)
    tools_bytes,tools_pin=s.read(a.peer_true_tools)
    tools=json.loads(tools_bytes)
    if not review.get('status','').startswith('PASS') or review.get('failure') is not None or review.get('source_only') is not True or review.get('compiler_executed') is not False or review.get('numerical_executed') is not False:
        raise RuntimeError('independent Source-only PASS/failureNone required')
    actual=tools['actual_review_return']
    if type(actual.get('exit_code')) is not int or actual['exit_code'] != 0 or actual.get('session_id') is not None or tools.get('observed_closed') is not True:
        raise RuntimeError('genuine terminal independent tool integer0/closedtrue/no session')
    lines=[line for line in actual['output'].splitlines() if line.strip()]
    if not lines or json.loads(lines[-1]).get('review_pin') != review_pin:
        raise RuntimeError('exact independent review output PF required')
    for key in ('candidate_driver_pin','candidate_control_pin','complete_byte_inverse_pin','control_plan_pin','causal_review_pin','preparer_pin'):
        row=ready[key]
        if s.read(row['path'])[1] != row or not contained(review,row):
            raise RuntimeError('all owning candidate exact Source pins in independent review')
    if ready['control_plan_pin'] != plan_pin:
        raise RuntimeError('complete own control plan must be exact')
    inverse_bytes,inverse_pin=s.read(ready['complete_byte_inverse_pin']['path'])
    inverse=json.loads(inverse_bytes)
    original_driver=s.read(inverse['original_driver_pin']['path'])
    candidate_driver=s.read(inverse['candidate_driver_pin']['path'])
    recovered=candidate_driver[0]
    for block in reversed(inverse['driver_blocks']):
        old=block['old'].encode();new=block['new'].encode()
        if recovered.count(new) != 1:
            raise RuntimeError('exact single Driver inverse block')
        recovered=recovered.replace(new,old)
    if recovered != original_driver[0] or original_driver[1] != inverse['original_driver_pin']:
        raise RuntimeError('Driver whole-byte original recovery')
    original_control=s.read(inverse['original_control_pin']['path'])
    candidate_control=s.read(inverse['candidate_control_pin']['path'])
    recovered=candidate_control[0]
    for block in reversed(inverse['control_blocks']):
        old=block['old'].encode();new=block['new'].encode()
        if recovered.count(new) != 1:
            raise RuntimeError('exact single control inverse block')
        recovered=recovered.replace(new,old)
    if recovered != original_control[0] or original_control[1] != inverse['original_control_pin']:
        raise RuntimeError('control whole-byte original recovery')
    evidence=plan['exact_source_evidence_pins']
    for row in plan['original_source_pins']+evidence:
        if s.read(row['path'])[1] != row:
            raise RuntimeError('complete original/evidence EOF7 unchanged')
    files=[ready['candidate_driver_pin'],ready['candidate_control_pin'],ready['complete_byte_inverse_pin'],
      ready['control_plan_pin'],ready['causal_review_pin'],ready_pin,ready['preparer_pin'],
      s.read(__file__)[1],s.read(OUT/'TRUE_TOOL_RETURNS.json')[1],review_pin,tools_pin]
    frozen=dict(schema='COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_AND_CONTROL_SOURCE_ONLY_FREEZE_V1',
      source_only=True,compiled=False,numerical_executed=False,files=files,
      original_source_pins=plan['original_source_pins'],complete_byte_inverse_pin=inverse_pin,
      control_plan_pin=plan_pin,exact_source_evidence_pins=evidence,
      actual_independent_Source_review_pin=review_pin,actual_independent_Source_review_true_tool_pin=tools_pin,
      internal_exact_cache_working_set_bytes=336*2**20,original_acceptance_RSS_cap_bytes=512*2**20,
      original_math_SPOT1P64_pin=plan['original_source_pins'][1],original_math_modified=False,
      public_Driver_ABI_unchanged=True,Driver_single_literal_368_to336=True,
      old_control_assertions_retained=301,new_control_expected_assertions=338,new_control_expected_calls=121,
      complete70_driver_replacement_zero_based_index=37,retained69_inputs=True,
      actual_new_driver_object_pin=None,actual_new_Dragon_pin=None,actual_build_report_pin=None,
      actual_bit_control_report_pin=None,actual_full50_report_pin=None,
      production_reader_qualified=False,physics_qualified=False,GLOBAL_qualified=False,goal_complete=False)
    frozen_pin=s.put(SF,frozen)
    print(json.dumps(dict(status='SOURCE_ONLY_FREEZE_CLOSED0',source_freeze_pin=frozen_pin),ensure_ascii=False),flush=True)

if __name__=='__main__':
    main()
