from pathlib import Path
import hashlib,json
D=Path('/private/tmp/axmat_v14b_manual_alias_helper_source_independent_review_20261010')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
o=json.loads((D/'review.stdout').read_text());assert o['REPORT_sha256']==sha(D/'REPORT.json') and o['EVIDENCE_sha256']==sha(D/'EVIDENCE.json');assert (D/'review.stderr').stat().st_size==0
r={'schema':'AXMAT_V14B_MANUAL_ALIAS_HELPER_INDEPENDENT_SOURCE_ACTUAL_TOOL_RETURN_V1','initial_chunk_id':'0f82bc','terminal_chunk_id':'0f82bc','session_id':None,'exit_code':0,'exit_code_type':'int','closed':True,'command':'env -u PYTHONPATH -u PYTHONOPTIMIZE PYTHONDONTWRITEBYTECODE=1 /Users/wen/miniforge3/envs/openmc-dev/bin/python3.12 -B '+str(D/'review_source.py'),'source':{'path':str(D/'review_source.py'),'sha256':sha(D/'review_source.py')},'stdout':{'path':str(D/'review.stdout'),'sha256':sha(D/'review.stdout'),'size_bytes':(D/'review.stdout').stat().st_size},'stderr':{'path':str(D/'review.stderr'),'sha256':sha(D/'review.stderr'),'size_bytes':0},'report':{'path':str(D/'REPORT.json'),'sha256':sha(D/'REPORT.json')},'business_or_helper_imported_called':False,'fixtures_controls_performance_executed':False,'project_written':False,'initial_readonly_display_error_c63b5e':{'exit_code':1,'reason':'Proof619 uses before/after and proof839 uses old/new. Only inspection field assumption corrected; no helper execution.'}}
(D/'actual_readonly_tool_return.json').write_text(json.dumps(r,indent=2)+'\n')
m={'schema':'AXMAT_V14B_MANUAL_ALIAS_SOURCE_SMALL_REVIEW_MANIFEST_V1','files':[{'path':str(p),'sha256':sha(p),'size_bytes':p.stat().st_size} for p in sorted(D.iterdir()) if p.is_file() and p.name!='EVIDENCE_MANIFEST.json']}
(D/'EVIDENCE_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({n:sha(D/n) for n in ('REPORT.json','EVIDENCE.json','actual_readonly_tool_return.json','EVIDENCE_MANIFEST.json')},indent=2))
