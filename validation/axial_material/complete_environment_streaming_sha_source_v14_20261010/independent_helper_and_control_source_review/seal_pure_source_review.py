from pathlib import Path
import hashlib,json
D=Path('/private/tmp/axmat_v14_complete_environment_streaming_helper_controls_source_only_20261010')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
e=json.loads((D/'complete_helper_source_inverse_and_driver_static_evidence.json').read_text())
for path,value in e['full_source_SHA_and_7identity_before_after'].items():
 p=Path(path);x=p.lstat();actual=[x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
 assert actual==value['identity'] and sha(p)==value['sha256']
stdout=D/'source_review_v2.stdout';stderr=D/'source_review_v2.stderr';report=D/'REPORT.json'
r=json.loads(stdout.read_text());assert r['REPORT_sha256']==sha(report) and stderr.stat().st_size==0
receipt={'schema':'AXMAT_V14_HELPER_CONTROL_DRAFT_PURE_SOURCE_ACTUAL_TOOL_RETURN_V1','initial_chunk_id':'ec5276','terminal_chunk_id':'ec5276','session_id':None,'exit_code':0,'exit_code_type':'int','closed':True,
 'command':'env -u PYTHONPATH -u PYTHONOPTIMIZE PYTHONDONTWRITEBYTECODE=1 /Users/wen/miniforge3/envs/openmc-dev/bin/python3.12 -B '+str(D/'verify_helper_and_control_sources_only_v2.py'),
 'source':{'path':str(D/'verify_helper_and_control_sources_only_v2.py'),'sha256':sha(D/'verify_helper_and_control_sources_only_v2.py')},
 'stdout':{'path':str(stdout),'sha256':sha(stdout),'size_bytes':stdout.stat().st_size},'stderr':{'path':str(stderr),'sha256':sha(stderr),'size_bytes':0},
 'report':{'path':str(report),'sha256':sha(report)},'driver_source':{'path':str(D/'helper_only_controls.UNREADY.py'),'sha256':sha(D/'helper_only_controls.UNREADY.py')},
 'supervision_source_plan':{'path':str(D/'GENUINE_OWNRSS_SUPERVISION_SOURCE_PLAN.json'),'sha256':sha(D/'GENUINE_OWNRSS_SUPERVISION_SOURCE_PLAN.json'),'source_plan_generation_chunk':'86bd2f','source_plan_generation_exit_code':0},
 'previous_readonly_assertion_error':{'chunk_id':'808dd4','exit_code':1,'closed':True,'preserved_receipt':str(D/'actual_failed_source_reader_808dd4.json'),'reason':'expected literal omitted actual explicit cwd=state[cwd]; only TMP reader assertions corrected'},
 'helper_imported_or_called':False,'fixture_controls_or_benchmark_executed':False,'project_written':False,'Root_polled':False,
 'all_future_actual_helper_results':None,'component_or_native_RSS_AAA_ABA_credit':False}
(D/'actual_readonly_tool_return.json').write_text(json.dumps(receipt,indent=2)+'\n')
m={'schema':'AXMAT_V14_HELPER_DRIVER_SOURCE_ONLY_EVIDENCE_MANIFEST_V1','files':[{'path':str(p),'size_bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(D.iterdir()) if p.is_file() and p.name!='EVIDENCE_MANIFEST.json'],
 'unknown_bindings':'driver STATUS remainsUNREADY and canonical HELPER_SHA256 remainsNone; only Root may source-bind after admission, then solely execute original bounded helper-only controls.'}
(D/'EVIDENCE_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({n:sha(D/n) for n in ['REPORT.json','helper_only_controls.UNREADY.py','complete_helper_source_inverse_and_driver_static_evidence.json','GENUINE_OWNRSS_SUPERVISION_SOURCE_PLAN.json','actual_readonly_tool_return.json','EVIDENCE_MANIFEST.json']},indent=2))
