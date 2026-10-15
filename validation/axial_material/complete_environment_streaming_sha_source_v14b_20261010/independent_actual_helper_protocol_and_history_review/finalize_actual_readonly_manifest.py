from pathlib import Path
import hashlib,json
D=Path(__file__).parent;R=D/'actual_review_attempt_01'
def sha(p):
    with p.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def read(p):return json.loads(p.read_text())
report=read(R/'FINAL_REPORT.json');receipt=read(R/'actual_readonly_tool_return.json')
assert report['status']=='PASS_HELPER_PROTOCOL_ONLY'
assert type(receipt['exit_code']) is int and receipt['exit_code']==0 and receipt['closed'] is True
assert receipt['initial_chunk_id']=='0a71f5' and receipt['session_id']==66554 and receipt['terminal_chunk_id']=='126a34'
assert sha(R/'FINAL_REPORT.json')=='903606fcc04bc4a80518a4577a801e4611e6f4df7bfc4e280c92d925af91f758'
assert sha(R/'actual_readonly_tool_return.json')=='14631f52667148a4769c2d490d14dfd02ddcae3fb54a11feac356bdbf6310cfc'
for row in read(R/'EVIDENCE.json')['full_fresh_file_pins']:
    info=Path(row['path']).lstat()
    assert [info.st_dev,info.st_ino,info.st_mode,info.st_nlink,info.st_size,info.st_mtime_ns,info.st_ctime_ns]==row['identity']
closure={'schema':'AXMAT_V14B_ACTUAL_READONLY_COMPLETE_TRUE_TERMINAL_CLOSURE_V1','status':'PASS_HELPER_PROTOCOL_ONLY',
    'actual_reader':{'initial_chunk_id':'0a71f5','session_id':66554,'terminal_chunk_id':'126a34','exit_code':0,'exit_code_type':'int','closed':True},
    'report_sealer':{'chunk_id':'52cbd6','exit_code':0,'exit_code_type':'int','closed':True},
    'final_report':{'path':str(R/'FINAL_REPORT.json'),'sha256':sha(R/'FINAL_REPORT.json')},
    'actual_reader_receipt':{'path':str(R/'actual_readonly_tool_return.json'),'sha256':sha(R/'actual_readonly_tool_return.json')},
    'project_source_and_control_evidence_7identity_still_exact':True,
    'project_written':False,'helper_loaded_or_fixture_history_reexecuted':False,
    'no_component_native_AAA_ABA_credit':True}
(D/'ACTUAL_COMPLETE_TOOL_CLOSURE.json').write_text(json.dumps(closure,indent=2)+'\n')
manifest={'schema':'AXMAT_V14B_ACTUAL_READONLY_COMPLETE_SMALL_EVIDENCE_MANIFEST_V1','status':'PASS_HELPER_PROTOCOL_ONLY',
    'files':[{'path':str(p),'size_bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(D.rglob('*')) if p.is_file() and p.name!='FINAL_EVIDENCE_MANIFEST.json'],
    'only_TMP_written':True,'no_project_payload_copied':True,'historical_big_content_not_reread':True,
    'actual_reader_report_receipt_and_true_terminal_closure_complete':True,'no_science_credit':True}
(D/'FINAL_EVIDENCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'status':'PASS_HELPER_PROTOCOL_ONLY','final_manifest_sha256':sha(D/'FINAL_EVIDENCE_MANIFEST.json'),
    'complete_tool_closure_sha256':sha(D/'ACTUAL_COMPLETE_TOOL_CLOSURE.json'),'files':len(manifest['files']),
    'total_small_evidence_bytes':sum(x['size_bytes'] for x in manifest['files'])},indent=2))
