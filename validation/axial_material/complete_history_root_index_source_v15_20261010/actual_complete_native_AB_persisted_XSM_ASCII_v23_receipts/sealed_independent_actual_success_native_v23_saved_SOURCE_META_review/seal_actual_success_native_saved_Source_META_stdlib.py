import hashlib,json,stat,shutil
from pathlib import Path
D=Path("/private/tmp/axmat_v23_actual_success_native_saved_SOURCE_META_review_20261010_q7x1ir_k")
def pin(p):
 s=p.lstat();ids=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns];assert p.is_absolute() and p.resolve()==p and stat.S_ISREG(s.st_mode) and s.st_nlink==1
 with p.open('rb') as f:b=f.read();assert len(b)==s.st_size and f.read(1)==b''
 assert ids(p.lstat())==ids(s)
 return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ids(s))
shutil.copyfile('/private/tmp/spot_review_v23_actual_success_native_saved_Source_META_stdlib.initial_failed.py',D/'review_actual_success_native_saved_Source_META_stdlib.initial_failed.py')
rv=json.loads((D/'REVIEW.json').read_text());assert rv['schema']=='INDEPENDENT_V23_ACTUAL_SUCCESS_NATIVE_PERSISTED_BYTE_SAVED_SOURCE_META_REVIEW_V1' and rv['status']=='PASS_ACTUAL_NATIVE_PERSISTED_BYTE_SAVED_SOURCE_META_EVIDENCE_ONLY' and rv['all_checks_typed_true'] is True and rv['blockers']==[] and rv['check_count']==len(rv['checks'])==19431 and all(c['passed'] is True for c in rv['checks'])
for k in ('actual_Root_native_terminal_pin','actual_Root_postclose_summary_pin','actual_Root_complete_namespace_manifest_pin','actual_Root_prelaunch_pin','actual_Root_postclose_META_writer_terminal_pin','actual_child_report_pin','actual_genuine_host_result_pin','actual_genuine_watchdog_pin','actual_merged_child_log_pin','actual_source_binding_pin','actual_checker_Source_pin','actual_host_Source_pin','actual_postclose_writer_Source_pin'):assert set(rv[k])=={'path','sha256','size_bytes','identity'} and pin(Path(rv[k]['path']))==rv[k]
assert rv['actual_native_byte_qualification_sha256'] is None and rv['actual_native_replayed_by_this_review'] is False and rv['native_XSM_API_export_preorder_equal_original_ASCII'] is False and rv['native_physical_LCM_copy_preorder_equal_original_ASCII'] is True
m=dict(schema='INDEPENDENT_V23_ACTUAL_SUCCESS_NATIVE_SAVED_SOURCE_META_REVIEW_PACKAGE_MANIFEST_V1',saved_Source_META_only=True,members={str(p.relative_to(D)):pin(p) for p in sorted(D.rglob('*')) if p.is_file() and p!=D/'MANIFEST.json'},excludes_only_root_manifest=True,does_not_claim_independent_large_numeric_payload_hash=True)
p=D/'MANIFEST.json'
with p.open('x') as f:json.dump(m,f,indent=2,allow_nan=False);f.write('\n')
assert set(m['members'])=={str(p.relative_to(D)) for p in D.rglob('*') if p.is_file() and p!=D/'MANIFEST.json'}
for name,q in m['members'].items():assert pin(D/name)==q
print(json.dumps(dict(status='SEALED_PASS_ACTUAL_NATIVE_PERSISTED_BYTE_SAVED_SOURCE_META_EVIDENCE_ONLY',manifest=pin(p),review=pin(D/'REVIEW.json'),member_count=len(m['members']),check_count=rv['check_count'],new_native_qualification_created=False,no_payload_or_native_replay=True)))

