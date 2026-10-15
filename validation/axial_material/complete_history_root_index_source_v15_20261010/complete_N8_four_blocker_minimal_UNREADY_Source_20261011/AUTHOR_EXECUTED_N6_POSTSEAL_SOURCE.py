import ast,hashlib,json,stat
from pathlib import Path
P=Path('/private/tmp/axmat_complete_native_observation_N6_shared_original_libraries_UNREADY_Source_p8u1h6xc')
S=Path(str(P)+'_seal_receipt')
def pin(q):
 s=q.lstat();i=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 assert stat.S_ISREG(s.st_mode)and s.st_nlink==1 and all(not v.is_symlink()for v in(q,*q.parents))
 with q.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 z=q.lstat();assert[z.st_dev,z.st_ino,z.st_mode,z.st_nlink,z.st_size,z.st_mtime_ns,z.st_ctime_ns]==i
 return dict(path=str(q),sha256=h,size_bytes=s.st_size,identity=i)
truth=json.loads((S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json').read_bytes());t=truth['terminal_tool_return'];assert truth['observed_terminal']is True and truth['closed']is True and truth['session_repolled_after_close']is False and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and truth['actual_terminal_chunk']==t['chunk_id']
raw=json.loads(t['output']);assert raw['manifest_pin']==pin(P/'MANIFEST.json')and raw['report_pin']==pin(P/'AUTHOR_N6_SOURCE_ONLY_REPORT.json')
mf=json.loads((P/'MANIFEST.json').read_bytes());expected={r['relative_path']for r in mf['members']}|{'MANIFEST.json'}
assert{str(q.relative_to(P))for q in P.rglob('*')if q.is_file()}==expected
for row in mf['members']:assert pin(P/row['relative_path'])==row['fullpin']
assert{str(q)for q in[P,*P.rglob('*')]if q.is_dir()}==set(mf['complete_directory_identity'])
for q,i in mf['complete_directory_identity'].items():
 s=Path(q).lstat();assert[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==i
report=json.loads((P/'AUTHOR_N6_SOURCE_ONLY_REPORT.json').read_bytes());assert report['check_count']==len(report['checks'])==310 and all(type(c['passed'])is bool and c['passed']is True for c in report['checks'])
for q in P.rglob('*.py'):ast.parse(q.read_bytes())
value=dict(schema='ACTUAL_N6_FULL_SOURCE_POSTSEAL_VERIFICATION_V1',source_only=True,manifest_pin=pin(P/'MANIFEST.json'),report_pin=pin(P/'AUTHOR_N6_SOURCE_ONLY_REPORT.json'),all_members_full_EOF_SHA7ID_and_directory_identity_unchanged=True,member_count=mf['member_count'],file_count_including_manifest=mf['full_file_count_including_manifest'],directory_count=mf['directory_count'],candidate_helper_guard_API_native_material_or_compile_executed=False,actual_runtime_or_storage_or_RSS_or_physical_qualification_created=False)
q=S/'FULL_SOURCE_POSTSEAL_VERIFICATION.json'
with q.open('x')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(value,status='ACTUAL_N6_FULL_SOURCE_POSTSEAL_ONLY_NOT_BUSINESS_OR_SCIENCE',postseal_report_pin=pin(q)),allow_nan=False))
