import hashlib
import json
from pathlib import Path

D=Path('/private/tmp/axmat_v13_full86_factory_source_independent_review_20261009')
def pin(p):
    b=p.read_bytes()
    return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b))
report=pin(D/'REPORT.json')
assert report['sha256']=='3c94602d87625c1f40a67e463eb44084534076cd63bde2e5ba00e89e5654f8a4'
assert (D/'review_v2.stderr').read_bytes()==b''
observed=json.loads((D/'review_v2.stdout').read_text())
assert observed['report_sha256']==report['sha256'] and observed['status']=='PASS_SOURCE_ONLY_UNREADY'
receipt=dict(schema='AXMAT_ACTUAL_READONLY_SOURCE_REVIEW_TOOL_RETURN_V1',
    actual_tool_terminal_return_observed=True,record_written_after_actual_terminal_return=True,
    actual_tool_result=dict(chunk_id='3ce373',exit_code=0,closed=True,session_id=None),
    command=['env','-u','PYTHONPATH','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1',
      '/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',str(D/'review_full_factory_source_only_v2.py')],
    source=pin(D/'review_full_factory_source_only_v2.py'),report=report,
    full_stdout=pin(D/'review_v2.stdout'),full_stderr=pin(D/'review_v2.stderr'),
    initial_review_failure=dict(chunk_id='cafab1',exit_code=1,closed=True,
      retained_receipt=pin(D/'actual_failed_reader_cafab1_tool_return.json'),
      original_source=pin(D/'review_full_factory_source_only.py'),
      full_stdout=pin(D/'review.stdout'),full_stderr=pin(D/'review.stderr')),
    source_only=True,business_imported=False,candidate_called=False,fixtures_executed=False,
    project_written=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
with (D/'actual_readonly_tool_return.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
files=sorted(p for p in D.iterdir() if p.is_file())
manifest=dict(schema='AXMAT_V13_FULL86_SOURCE_REVIEW_SMALL_EVIDENCE_MANIFEST_V1',
    evidence_files=[pin(p) for p in files],source_only=True,project_written=False)
with (D/'EVIDENCE_MANIFEST.json').open('x') as f:json.dump(manifest,f,indent=2);f.write('\n')
print(json.dumps(dict(status='PASS_SOURCE_ONLY_UNREADY',REPORT=report,
    actual_readonly_tool_return=pin(D/'actual_readonly_tool_return.json'),
    EVIDENCE_MANIFEST=pin(D/'EVIDENCE_MANIFEST.json'))))
