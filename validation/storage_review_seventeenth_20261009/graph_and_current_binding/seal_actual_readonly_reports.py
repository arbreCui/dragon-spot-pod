import hashlib,json
from pathlib import Path
D=Path('/private/tmp/spot_storage_review_seventeenth_graph_20261009')
def pin(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)
report=json.loads((D/'REPORT.json').read_text())
assert report['status']=='PASS' and report['approved_deletion_candidates']==[] and report['files_deleted']==0
assert report['project_formal_ART_written'] is False and (D/'review.stderr').stat().st_size==0
# Preserve the genuine executed reader's exact original output. The final
# machine report adds only the requested explicit project_written synonym and
# its readonly observed provenance; no scientific field or old file changes.
original=D/'REPORT_actual_metadata_reader.json'
assert not original.exists()
(D/'REPORT.json').rename(original)
original_pin=pin(original)
observed=dict(initial_chunk_id='85da9f',session_id=16531,terminal_chunk_id='8b8354',exit_code=0,closed=True)
report['project_written']=False
report['actual_readonly_reader_tool']=observed
report['unaltered_original_actual_reader_report']=original_pin
with(D/'REPORT.json').open('x')as f:json.dump(report,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
receipt=dict(schema='SPOT_R17_INDEPENDENT_ACTUAL_READONLY_STORAGE_REVIEW_TOOL_RETURN_V1',actual_tool_result=observed,
 reader_source=pin(D/'review_storage_incremental_readonly.py'),original_executed_reader_report=original_pin,final_machine_report=pin(D/'REPORT.json'),Chinese_report=pin(D/'REPORT.txt'),full_stdout=pin(D/'review.stdout'),full_stderr=pin(D/'review.stderr'),finalization_scope='Explicit project_written synonym and true closed reader provenance only; original reader JSON byteexact retained.',files_deleted=0,project_written=False,business_executed=False,only_TMP_written=True)
with(D/'actual_readonly_tool_return.json').open('x')as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(dict(status=report['status'],approved_deletion_candidates=[],files_deleted=0,project_written=False,report=pin(D/'REPORT.json'),Chinese_report=pin(D/'REPORT.txt'),receipt=pin(D/'actual_readonly_tool_return.json')),sort_keys=True),flush=True)
