from pathlib import Path
import hashlib,json
D=Path('/private/tmp/axmat_v14b_manual_alias_helper_controls_source_only_20261010')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
o=json.loads((D/'source.stdout').read_text());assert o['REPORT_sha256']==sha(D/'REPORT.json') and o['driver_sha256']==sha(Path(o['driver']));assert (D/'source.stderr').stat().st_size==0
r={'schema':'AXMAT_V14B_HELPER_ONLY_CONTROL_DRIVER_PURE_SOURCE_ACTUAL_TOOL_RETURN_V1','initial_chunk_id':'655d6f','terminal_chunk_id':'655d6f','session_id':None,'exit_code':0,'exit_code_type':'int','closed':True,'command':'env -u PYTHONPATH -u PYTHONOPTIMIZE PYTHONDONTWRITEBYTECODE=1 /Users/wen/miniforge3/envs/openmc-dev/bin/python3.12 -B '+str(D/'generate_source_draft.py'),'source':{'path':str(D/'generate_source_draft.py'),'sha256':sha(D/'generate_source_draft.py')},'stdout':{'path':str(D/'source.stdout'),'sha256':sha(D/'source.stdout'),'size_bytes':(D/'source.stdout').stat().st_size},'stderr':{'path':str(D/'source.stderr'),'sha256':sha(D/'source.stderr'),'size_bytes':0},'report':{'path':str(D/'REPORT.json'),'sha256':sha(D/'REPORT.json')},'helper_or_driver_loaded_called':False,'fixture_or_performance_executed':False,'project_written':False}
(D/'actual_source_tool_terminal_return.json').write_text(json.dumps(r,indent=2)+'\n')
m={'schema':'AXMAT_V14B_HELPER_ONLY_DRIVER_SMALL_SOURCE_EVIDENCE_MANIFEST_V1','files':[{'path':str(p),'sha256':sha(p),'size_bytes':p.stat().st_size} for p in sorted(D.iterdir()) if p.is_file() and p.name!='EVIDENCE_MANIFEST.json']}
(D/'EVIDENCE_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({n:sha(D/n) for n in ('helper_only_controls_v14b.UNREADY.py','REPORT.json','COMPLETE_SOURCE_INVERSE_PROOF.json','CONTROL_CONTRACT.json','actual_source_tool_terminal_return.json','EVIDENCE_MANIFEST.json')},indent=2))
