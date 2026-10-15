#!/usr/bin/env python3
"""Validate only the completed TMP report/source, without business reads."""
import hashlib
import json
from pathlib import Path

root=Path('/private/tmp/spot_storage_nineteenth_current_native_snapshot_read_paths_20261009')
report_path=root/'REPORT.json'
raw=report_path.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='f055e095769fe065a11b24cf3b29693d8bc887c485da39495964ff2f7af7d6cf'
report=json.loads(raw)
assert report['status']=='PASS'
assert report['fixed_candidate_plan']['sha256']=='b0cf9e8577d91ee6c3be70eada54d3f7f20078335e60db08a43ed1b3a093b79a'
assert report['original_phase_future_native_result'] is None
assert not report['candidate_specific_blockers']
assert not report['resolved_candidate_alias_hits']
assert not report['candidate_regular_device_inode_hits']
assert not report['derived_read_paths_missing_now']
assert all(not x['exact_candidate_path_hits'] for x in report['exact_path_checks'].values())
assert all(v==0 for v in report['actual_tool_zero'].values())
pins={}
for path in (report_path,root/'REPORT.txt',root/'review_readonly.py',Path(__file__)):
    content=path.read_bytes()
    pins[str(path)]={'path':str(path),'sha256':hashlib.sha256(content).hexdigest(),'bytes':len(content)}
print(json.dumps({'status':'CLOSED_READONLY_PASS','report_pins':pins,
    'business_and_candidate_payload_reads_during_closeout':0,
    'reported_prior_business_and_candidate_payload_tool_counts':report['actual_tool_zero'],
    'original_phase_future_native_result':None},sort_keys=True))
