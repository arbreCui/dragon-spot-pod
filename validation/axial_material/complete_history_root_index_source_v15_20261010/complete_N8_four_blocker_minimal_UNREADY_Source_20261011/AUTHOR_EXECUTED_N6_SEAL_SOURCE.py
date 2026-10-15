import ast,gzip,hashlib,json,os,stat,shutil
from pathlib import Path
P=Path('/private/tmp/axmat_complete_native_observation_N6_shared_original_libraries_UNREADY_Source_p8u1h6xc')
def pin(q):
 s=q.lstat();i=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 if not stat.S_ISREG(s.st_mode)or s.st_nlink!=1 or any(v.is_symlink()for v in(q,*q.parents)):raise ValueError('Source regular singlelink noaliases')
 with q.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 z=q.lstat()
 if[z.st_dev,z.st_ino,z.st_mode,z.st_nlink,z.st_size,z.st_mtime_ns,z.st_ctime_ns]!=i:raise ValueError('Source EOF race')
 return dict(path=str(q),sha256=h,size_bytes=s.st_size,identity=i)
shutil.copy2(Path(__file__),P/'AUTHOR_EXECUTED_N6_SEAL_SOURCE.py')
post=Path('/private/tmp/axmat_postseal_N6_shared_original_libraries_Source_20261010.py');shutil.copy2(post,P/'AUTHOR_EXECUTED_N6_POSTSEAL_SOURCE.py')
report=json.loads((P/'AUTHOR_N6_SOURCE_ONLY_REPORT.json').read_bytes());checks=report['checks']
assert type(report['check_count'])is int and report['check_count']==len(checks)==310 and all(type(c['passed'])is bool and c['passed']is True for c in checks)and len({c['check']for c in checks})==len(checks)and report['actual_candidate_or_guard_or_API_or_native_or_material_executed']is False
for q in P.rglob('*.py'):ast.parse(q.read_bytes())
with gzip.open(P/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz','rb')as f:
 while f.read(2**20):pass
mf=P/'MANIFEST.json';mf.open('x').close()
dirs={}
for q in[P,*sorted(P.rglob('*'))]:
 s=q.lstat()
 if stat.S_ISDIR(s.st_mode):dirs[str(q)]=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 elif not stat.S_ISREG(s.st_mode)or s.st_nlink!=1:raise ValueError('complete Source files noaliases')
members=[dict(relative_path=str(q.relative_to(P)),fullpin=pin(q))for q in sorted(P.rglob('*'))if q.is_file()and q!=mf]
value=dict(schema='COMPLETE_NATIVE_OBSERVATION_BUILD5_AB_UNREADY_SOURCE_MANIFEST_V1',status='UNREADY_SOURCE_ONLY_REQUIRES_INDEPENDENT_REVIEW',source_only=True,members=members,member_count=len(members),full_file_count_including_manifest=len(members)+1,directory_count=len(dirs),complete_directory_identity=dirs,whole_original_native_Source_archive_members=1365,finite_necessary_full_Source_retention_only=True,author_finite_Source_check_pin=pin(P/'AUTHOR_N6_SOURCE_ONLY_REPORT.json'),finite_full_Source_fix_inverse_pin=pin(P/'COMPLETE_N6_FOUR_ROLE_WHOLE_BYTE_AST_SOURCE_INVERSE.json'),actual_author_Source_check_tool_returns_pin=pin(P/'ACTUAL_AUTHOR_N6_SOURCE_ONLY_TOOL_RETURNS.json'),original_frozen_N5_manifest_pin=report['actual_parent_N5_manifest_pin'],N5_complete_manifest_whole_byte_copy_pin=pin(P/'PREVIOUS_SEALED_N5_SOURCE_PROVENANCE/MANIFEST.json'),N6_changed_role_count=4,N6_all_seven_seed_roles_and_original_c2m_byte_provenance_saved=True,N6_shared_original_libraries_copied_once_noaliases=True,N6_only_three_original_procedure_FIL_path_literals_replaced=True,N6_original_material_x2m_unchanged=True,N6_ILIBRARYNAME_provenance_changes_explicit_not_normalized=True,N6_all_original9caps_unchanged=True,N6_source_does_not_predict_storage_RSS_or_numerical_equality=True,N4_or_N5_Source_admission_cannot_admit_N6=True,actual_peer_review=None,actual_Root_Source_admission=None,actual_Root_runtime_terminal=None,actual_observation_manifest=None,actual_native_Source_binary_linkage=None,actual_new_native_controls=None,actual_new_native_objects_archives_executable=None,scientific_qualification_created=False,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
with mf.open('w')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
for row in members:assert pin(P/row['relative_path'])==row['fullpin']
for q,i in dirs.items():
 s=Path(q).lstat();assert[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==i
print(json.dumps(dict(status='ACTUAL_N6_SOURCE_ONLY_SEAL_NOT_BUSINESS_OR_SCIENCE',source_only=True,manifest_pin=pin(mf),report_pin=pin(P/'AUTHOR_N6_SOURCE_ONLY_REPORT.json'),member_count=len(members),file_count_including_manifest=len(members)+1,directory_count=len(dirs),author_typed_true_check_count=len(checks),full_1365_Source_archive_EOF_and_gzip_CRC_read=True,candidate_helper_guard_API_native_material_or_compile_executed=False),allow_nan=False))
