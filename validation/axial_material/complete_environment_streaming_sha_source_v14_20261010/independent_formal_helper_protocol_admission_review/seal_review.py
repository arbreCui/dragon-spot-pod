from pathlib import Path
import json,hashlib
D=Path('/private/tmp/axmat_v14_helper_protocol_formal_admission_readonly_review_20261010')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
o=json.loads((D/'review.stdout').read_text());assert o['REPORT_sha256']==sha(D/'REPORT.json') and o['EVIDENCE_sha256']==sha(D/'EVIDENCE.json');assert (D/'review.stderr').stat().st_size==0
r={'schema':'AXMAT_V14_FORMAL_HELPER_PROTOCOL_ADMISSION_READONLY_ACTUAL_TOOL_RETURN_V1','initial_chunk_id':'261961','terminal_chunk_id':'261961','session_id':None,'exit_code':0,'exit_code_type':'int','closed':True,'command':'env -u PYTHONPATH -u PYTHONOPTIMIZE PYTHONDONTWRITEBYTECODE=1 /Users/wen/miniforge3/envs/openmc-dev/bin/python3.12 -B '+str(D/'review_formal_admission.py'),'source':{'path':str(D/'review_formal_admission.py'),'sha256':sha(D/'review_formal_admission.py')},'stdout':{'path':str(D/'review.stdout'),'sha256':sha(D/'review.stdout'),'size_bytes':(D/'review.stdout').stat().st_size},'stderr':{'path':str(D/'review.stderr'),'sha256':sha(D/'review.stderr'),'size_bytes':0},'report':{'path':str(D/'REPORT.json'),'sha256':sha(D/'REPORT.json')},'initial_readonly_display_error_bc9bcd':{'exit_code':1,'reason':'Missing guessed inventories display key; actual schema read directly afterward. No business/source modification.'},'business_imports_calls_or_gates':False,'project_written':False}
(D/'actual_readonly_tool_return.json').write_text(json.dumps(r,indent=2)+'\n')
m={'schema':'AXMAT_V14_FORMAL_HELPER_PROTOCOL_ADMISSION_SMALL_REVIEW_MANIFEST_V1','files':[{'path':str(p),'sha256':sha(p),'size_bytes':p.stat().st_size} for p in sorted(D.iterdir()) if p.is_file() and p.name!='EVIDENCE_MANIFEST.json']}
(D/'EVIDENCE_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({n:sha(D/n) for n in ('REPORT.json','EVIDENCE.json','actual_readonly_tool_return.json','EVIDENCE_MANIFEST.json')},indent=2))
