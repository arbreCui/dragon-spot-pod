"""Seal only the new finite review package; do not read project evidence again."""
import hashlib
import json
from pathlib import Path
import stat

OUT = Path(__file__).parent
review = json.loads((OUT/'REVIEW.json').read_bytes())
receipts = json.loads((OUT/'actual_readonly_tool_returns.json').read_bytes())
assert review['status'] == 'ACTUAL_COMPLETE_PREP_EVIDENCE_PASS_ONLY_NOT_BUILD_INPUT_NATIVE_SCIENCE'
assert review['all_checks_typed_true'] is True and not review['blocking_findings']
assert all(type(value) is bool and value is True for value in review['checks'].values())
actual = receipts['actual_full_read_tool_return']
assert type(actual['exit_code']) is int and actual['exit_code'] == 0 and 'session_id' not in actual
assert actual['chunk_id'] == '70e402'
assert receipts['actual_exploratory_shape_tool_return']['exit_code'] == 1
assert receipts['actual_corrected_shape_tool_return']['exit_code'] == 0
assert all(value is False for key, value in review['qualification'].items() if key != 'actual_complete_PREP_resource_result_verified')
assert review['qualification']['actual_complete_PREP_resource_result_verified'] is True

def identity(path):
    s = path.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

files = {}
for path in sorted(OUT.iterdir()):
    if path.name == 'sealed_manifest.json':
        continue
    before = identity(path)
    assert stat.S_ISREG(before[2])
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    after = identity(path)
    assert before == after
    files[path.name] = dict(path=str(path), sha256=digest, size_bytes=before[4], identity=before, full_EOF_SHA7ID_verified=True)
manifest = dict(schema='AXMAT_V20_FINITE_ACTUAL_PREP_REVIEW_SEALED_PACKAGE_V1', status='PASS_ACTUAL_COMPLETE_PREP_ONLY', package=str(OUT), all_finite_review_tool_returns_preserved=True, actual_full_read_exit_code=0, actual_full_read_exit_code_is_integer=True, actual_full_read_chunk_id='70e402', no_running_review_session=True, exploratory_int1_preserved_and_corrected=True, all_review_checks_typed_true=True, original_evidence_reread_by_sealing=False, original_namespace_modified=False, SOURCE_qualification_repeated=False, original_history_rescanned=False, qualification=review['qualification'], files=files)
target = OUT/'sealed_manifest.json'
target.write_text(json.dumps(manifest, indent=2)+'\n')
with target.open('rb') as stream:
    digest = hashlib.file_digest(stream, 'sha256').hexdigest()
print(json.dumps(dict(status=manifest['status'], package=str(OUT), manifest_sha256=digest, manifest_bytes=target.stat().st_size, files=len(files), REVIEW_sha256=files['REVIEW.json']['sha256'], actual_full_read_chunk_id='70e402', actual_full_read_exit_code=0)))
