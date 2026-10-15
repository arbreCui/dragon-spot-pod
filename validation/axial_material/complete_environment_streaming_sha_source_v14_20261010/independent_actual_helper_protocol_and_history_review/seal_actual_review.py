from pathlib import Path
import hashlib,json
D=Path('/private/tmp/axmat_v14_actual_helper_controls_independent_review_20261010')
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
report=D/'REPORT.json';evidence=D/'EVIDENCE.json';stdout=D/'review.stdout';stderr=D/'review.stderr'
obs=json.loads(stdout.read_text())
assert obs['REPORT_sha256']==sha(report) and obs['EVIDENCE_sha256']==sha(evidence)
assert stderr.stat().st_size==0
for r in json.loads(evidence.read_text())['full_fresh_file_pins']:
    x=Path(r['path']).lstat()
    assert [x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]==r['identity']
receipt={'schema':'AXMAT_V14_ACTUAL_HELPER_CONTROLS_AND_HISTORY_INDEPENDENT_READONLY_TOOL_RETURN_V1',
 'initial_chunk_id':'c0c38a','session_id':9117,'terminal_chunk_id':'d200ce','exit_code':0,'exit_code_type':'int','closed':True,
 'command':'env -u PYTHONPATH -u PYTHONOPTIMIZE PYTHONDONTWRITEBYTECODE=1 /Users/wen/miniforge3/envs/openmc-dev/bin/python3.12 -B '+str(D/'review_actual_controls.py'),
 'source':{'path':str(D/'review_actual_controls.py'),'sha256':sha(D/'review_actual_controls.py')},
 'stdout':{'path':str(stdout),'size_bytes':stdout.stat().st_size,'sha256':sha(stdout)},
 'stderr':{'path':str(stderr),'size_bytes':0,'sha256':sha(stderr)},
 'report':{'path':str(report),'sha256':sha(report)},'evidence':{'path':str(evidence),'sha256':sha(evidence)},
 'business_or_helper_imported_or_called':False,'control_fixture_or_history_action_rerun':False,
 'historical_28GB_re_read':False,'Root_handle_polled':False,'project_written':False,
 'admission_scope':'Helper IO protocol only. No full86 component, native512, AAA or ABA credit.'}
(D/'actual_readonly_tool_return.json').write_text(json.dumps(receipt,indent=2)+'\n')
txt=D/'REPORT.txt'
txt.write_text(txt.read_text()+'完整历史环境已真实执行并封存：旧25213次/28,562,424,798B，新13588次/27,794,515,455B，均完整EOF；本独审未重读这些历史大字节。旧15.705013834秒、新15.688161875秒（含不同观测开销），没有实质提速证据；history watch135.28125MiB仅表示此次辅助读取进程。\n独立纯只读c0c38a/session9117→d200ce，EXIT0 CLOSED。\n')
manifest={'schema':'AXMAT_V14_ACTUAL_HELPER_PROTOCOL_REVIEW_SMALL_EVIDENCE_MANIFEST_V1',
 'files':[{'path':str(p),'size_bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(D.iterdir()) if p.is_file() and p.name!='EVIDENCE_MANIFEST.json'],
 'project_evidence_is_bound_not_copied':True,'science_credit':False}
(D/'EVIDENCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({n:sha(D/n) for n in ['REPORT.json','REPORT.txt','EVIDENCE.json','actual_readonly_tool_return.json','EVIDENCE_MANIFEST.json','review_actual_controls.py']},indent=2))
