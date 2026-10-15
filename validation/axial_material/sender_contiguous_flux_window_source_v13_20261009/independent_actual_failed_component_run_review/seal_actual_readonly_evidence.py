from pathlib import Path
import hashlib,json,stat
D=Path('/private/tmp/axmat_v13_actual_component_failed_RUN_independent_review_20261010')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def identity(p):
    x=p.lstat()
    return [x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
e=json.loads((D/'actual_failed_RUN_complete_stage_raw_byte_evidence.json').read_text())
for p,v in e['source_and_file_fullSHA_7identity'].items():assert identity(Path(p))==v['identity'],p
source=D/'review_failed_component_stdlib_v2.py'
old=D/'review_failed_component_stdlib.py'
assert source.read_text()==old.read_text().replace("assert all(v=='1' for v in decl['threads'].values()) and len(decl['threads'])==5","assert type(decl['threads']) is int and decl['threads']==1\nassert all(k+'=1' in actual['input']['cmd'] for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'])")
stdout=D/'review_v2.stdout';stderr=D/'review_v2.stderr';report=D/'REPORT.json'
actual=json.loads(stdout.read_text())
assert actual['REPORT_sha256']==sha(report) and actual['status']=='PASS_ACTUAL_FAILURE_EVIDENCE_ONLY'
assert stderr.stat().st_size==0
receipt={'schema':'AXMAT_PURE_READONLY_ACTUAL_FAILED_COMPONENT_REVIEW_TOOL_RETURN_V1',
    'initial_chunk_id':'9667a7','terminal_chunk_id':'9667a7','session_id':None,'exit_code':0,'exit_code_type':'int',
    'closed':True,'actual_tool_terminal_observed':True,
    'command':'env -u PYTHONPATH -u PYTHONOPTIMIZE PYTHONDONTWRITEBYTECODE=1 /Users/wen/miniforge3/envs/openmc-dev/bin/python3.12 -B '+str(source),
    'source':{'path':str(source),'sha256':sha(source),'identity':identity(source)},
    'stdout':{'path':str(stdout),'sha256':sha(stdout),'size_bytes':stdout.stat().st_size},
    'stderr':{'path':str(stderr),'sha256':sha(stderr),'size_bytes':0},
    'report':{'path':str(report),'sha256':sha(report)},
    'stage_raw_evidence':{'path':str(D/'actual_failed_RUN_complete_stage_raw_byte_evidence.json'),'sha256':sha(D/'actual_failed_RUN_complete_stage_raw_byte_evidence.json')},
    'actual_business_exit_code':1,'component_qualified':False,
    'raw_numeric_acceptance_not_executed':True,'factory_auditor_called':False,'project_written':False,
    'prior_pure_readonly_errors':[{'tool_chunk_id':'518b35','exit_code':1,'closed':True,'source_form':'inline directory exploration','reason':'assumed receipt directory under ART SOURCE; actual AM path read from failed_terminal'},
        {'tool_chunk_id':'87882e','exit_code':1,'closed':True,'preserved_receipt_path':str(D/'actual_failed_reader_87882e_tool_return.json'),'preserved_receipt_sha256':sha(D/'actual_failed_reader_87882e_tool_return.json')}],
    'final_reader_only_change':'Correct actual scalar declaration threads=int1; separately verify all five original Root thread environment keys=1',
    'new_business_retry_performed':False}
(D/'actual_readonly_tool_return.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
manifest={'schema':'AXMAT_V13_ACTUAL_FAILED_COMPONENT_READONLY_REVIEW_EVIDENCE_MANIFEST_V1',
    'scope':'actual failure/preservation only; no replacement numeric acceptance',
    'files':[{'path':str(p),'size_bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(D.iterdir()) if p.is_file() and p.name!='EVIDENCE_MANIFEST.json']}
(D/'EVIDENCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({n:sha(D/n) for n in ['REPORT.json','actual_failed_RUN_complete_stage_raw_byte_evidence.json','actual_readonly_tool_return.json','EVIDENCE_MANIFEST.json']},indent=2))
