import hashlib
import json
from pathlib import Path
D=Path('/private/tmp/axmat_v13_actual_component_PREP_declaration_independent_review_20261009')
def pin(p):
 b=p.read_bytes();return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b))
report=pin(D/'REPORT.json')
assert report['sha256']=='bb2fe51788110ea9d4ff580a28aeda2c4688ac62c94a961918e000a69152ca34'
assert (D/'review_v2.stderr').read_bytes()==b''
returned=json.loads((D/'review_v2.stdout').read_text())
assert returned['REPORT_sha256']==report['sha256'] and returned['status']=='PASS_DECLARATION_PLAN_ONLY'
receipt=dict(schema='AXMAT_ACTUAL_READONLY_DECLARATION_REVIEW_TOOL_RETURN_V1',
 actual_tool_terminal_return_observed=True,record_written_after_actual_terminal_return=True,
 actual_tool_result=dict(chunk_id='8219ae',exit_code=0,closed=True,session_id=None),
 command=['env','-u','PYTHONPATH','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1',
  '/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',str(D/'review_actual_declaration_stdlib_v2.py')],
 source=pin(D/'review_actual_declaration_stdlib_v2.py'),report=report,
 full_stdout=pin(D/'review_v2.stdout'),full_stderr=pin(D/'review_v2.stderr'),
 initial_review_failure=dict(chunk_id='096ac5',exit_code=1,closed=True,
  retained_receipt=pin(D/'actual_failed_reader_096ac5_tool_return.json'),
  source=pin(D/'review_actual_declaration_stdlib.py'),full_stdout=pin(D/'review.stdout'),full_stderr=pin(D/'review.stderr')),
 source_and_declaration_only=True,live_RUN_polled=False,live_stage_data_read=False,
 business_imported=False,candidate_called=False,compile_or_fixture_executed=False,project_written=False,
 actual_component_RUN_success=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
with (D/'actual_readonly_tool_return.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
manifest=dict(schema='AXMAT_V13_ACTUAL_DECLARATION_REVIEW_COMPLETE_SMALL_EVIDENCE_MANIFEST_V1',
 evidence_files=[pin(p) for p in sorted(D.iterdir()) if p.is_file()],project_written=False)
with (D/'EVIDENCE_MANIFEST.json').open('x') as f:json.dump(manifest,f,indent=2);f.write('\n')
print(json.dumps(dict(status='PASS_DECLARATION_PLAN_ONLY',REPORT=report,
 actual_readonly_tool_return=pin(D/'actual_readonly_tool_return.json'),EVIDENCE_MANIFEST=pin(D/'EVIDENCE_MANIFEST.json'))))
