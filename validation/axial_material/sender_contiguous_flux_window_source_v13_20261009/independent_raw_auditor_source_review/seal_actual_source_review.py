from pathlib import Path
import hashlib,json
D=Path('/private/tmp/axmat_v13_sender_window_raw_auditor_source_independent_review_20261009')
def pin(p):
    a=p.stat();b=p.read_bytes();z=p.stat();keys=['st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns']
    assert [getattr(a,k) for k in keys]==[getattr(z,k) for k in keys]
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'size_bytes':len(b),'identity':dict(zip(keys,[getattr(z,k) for k in keys]))}
assert (D/'review.stderr').read_bytes()==b''
summary=json.loads((D/'review.stdout').read_bytes())
report=json.loads((D/'REPORT.json').read_bytes())
assert pin(D/'REPORT.json')['sha256']==summary['report_sha256']
for original in report['all_source_pins']:
    assert pin(Path(original['path']))==original
receipt={'schema':'AXMAT_ACTUAL_READONLY_SOURCE_REVIEW_TOOL_RETURN_V1','tool_result':
 {'chunk_id':'b33e27','wall_time_seconds':0.000011708,'exit_code':0,'original_token_count':0,'output':''},
 'state':'CLOSED','returncode_type':'int','executed_only':'STDlib review_raw_auditor_source_only.py; no audited module execution',
 'report':pin(D/'REPORT.json'),'stdout':pin(D/'review.stdout'),'stderr':pin(D/'review.stderr'),
 'source_only':True,'compiler_controls_fixtures_or_business_executed':False,'project_written':False,'Root_polled':False,
 'actual_controls_result':None,'actual_RSS_or_native_credit':False}
with (D/'actual_readonly_tool_return.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
items=[pin(p) for p in sorted(D.iterdir()) if p.is_file()]
with (D/'EVIDENCE_MANIFEST.json').open('x') as f:
 json.dump({'schema':'AXMAT_V13_SENDER_RAW_AUDITOR_SOURCE_REVIEW_EVIDENCE_MANIFEST_V1','status':'PASS_SOURCE_CONTRACT_ONLY',
 'files':items,'actual_review_tool_chunk':'b33e27','actual_review_exit_code':0,'actual_review_state':'CLOSED',
 'actual_control_or_native_result':None},f,indent=2);f.write('\n')
print(json.dumps({'report':pin(D/'REPORT.json'),'receipt':pin(D/'actual_readonly_tool_return.json'),
                 'manifest':pin(D/'EVIDENCE_MANIFEST.json')},separators=(',',':')))
