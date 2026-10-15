"""Seal this own finite SOURCE/saved-META audit package, never reviewed business code."""
import hashlib,json,stat
from pathlib import Path
P=Path(__file__).parent
def pin(p):
 s=p.lstat();a=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 assert p.resolve()==p and stat.S_ISREG(a[2])and a[3]==1
 with p.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 t=p.lstat();b=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
 assert a==b
 return dict(path=str(p),sha256=h,size_bytes=a[4],identity=a)
report=json.loads((P/'REVIEW.json').read_text())
assert report['status']=='PASS_ACTUAL_FAILED_NATIVE_SAVED_EVIDENCE_ONLY'and report['all_checks_typed_true']is True and report['blockers']==[]and report['check_count']==4681
assert report['actual_root_native_exit_code']==1 and report['actual_child_returncode']==1
assert report['sampled_zero_RSS_is_not_memory_admission']is True and report['native_RSS_verified']is False
assert report['original129_material_payloads_not_read_or_rehashed_by_reviewer']is True
assert report['native_persisted_XSM_value_bits_verified']is False and report['AAA_accuracy_qualified']is False and report['ABA_admitted']is False
strict=json.loads((P/'STRICT_REQUIRE_ALL108_SOURCE_REVIEW.json').read_text())
assert strict['strict_require_call_count']==108 and len(strict['all108_calls_preserved'])==108 and strict['no_other_determinate_valid_input_nonbool_rejection_identified']is True
assert strict['no_dynamic_candidate_or_protocol_test_executed']is True
for name,q in report['full_EOF_reviewed_input_pins'].items():assert pin(Path(name))==q
members={};dirs=[]
for q in sorted(P.rglob('*')):
 assert not q.is_symlink()
 if q.is_dir():dirs.append(str(q.relative_to(P)))
 else:members[str(q.relative_to(P))]=pin(q)
manifest=dict(schema='INDEPENDENT_V22_ACTUAL_FAILED_NATIVE_COMPLETE_SOURCE_META_REVIEW_MANIFEST_V1',
 status=report['status'],source_and_saved_META_only=True,
 all_business_native_scientific_success_qualifications_false=True,
 original_failed_V22_family_not_rerun=True,
 members=members,member_count=len(members),member_bytes=sum(q['size_bytes']for q in members.values()),
 directories=dirs,manifest_excluded_from_own_members=True,
 true_actual_failure_saved_review_tool=members['actual_saved_failure_full_EOF_review_tool_return.json'],
 true_actual_all108_Source_review_tool=members['actual_all108_Source_fixed_review_tool_return.json'],
 own_initial_AST_review_failed_expectation_preserved=True,
 material129_payloads_not_read_or_rehashed=True)
with (P/'MANIFEST.json').open('x')as f:json.dump(manifest,f,indent=2,allow_nan=False);f.write('\n')
for name,q in members.items():assert pin(P/name)==q
assert set(str(q.relative_to(P))for q in P.rglob('*')if q.is_file())==set(members)|{'MANIFEST.json'}
print(json.dumps(dict(status='SEALED_ACTUAL_FAILED_NATIVE_SOURCE_META_EVIDENCE_ONLY',manifest=pin(P/'MANIFEST.json'),review=pin(P/'REVIEW.json'),strict_require_Source_review=pin(P/'STRICT_REQUIRE_ALL108_SOURCE_REVIEW.json'),member_count=len(members),member_bytes=manifest['member_bytes'],actual_primary_review_checks=4681,actual_complete_unique_Source_META_inputs=522,all_native_science_qualification_false=True,no_candidate_guard_native_numeric_executed=True)))
