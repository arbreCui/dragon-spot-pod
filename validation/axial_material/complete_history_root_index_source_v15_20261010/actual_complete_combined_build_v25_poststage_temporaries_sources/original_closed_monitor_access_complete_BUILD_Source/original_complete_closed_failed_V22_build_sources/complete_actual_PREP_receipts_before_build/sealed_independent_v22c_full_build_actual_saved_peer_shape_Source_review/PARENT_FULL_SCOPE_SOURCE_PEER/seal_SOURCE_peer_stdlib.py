from pathlib import Path
import ast,hashlib,json,os,stat
P=Path('/private/tmp/axmat_v22_fullbuild_Root_Source_binder_independent_review_05fs3v3d')
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode)and s.st_nlink==1
 with p.open('rb')as f:
  assert identity(os.fstat(f.fileno()))==identity(s)
  b=f.read();assert len(b)==s.st_size and f.read(1)==b'' and identity(os.fstat(f.fileno()))==identity(s)
 assert identity(p.lstat())==identity(s)
 return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=identity(s))
r=json.loads((P/'REVIEW.json').read_bytes());assert r['PASS']is True and r['all_checks_passed']is True and r['blockers']==[]
assert len(r['checks'])==r['check_count']==184 and all(c['passed']is True for c in r['checks'])
assert r['complete_prior_source_check_count']==len(r['complete_prior_source_checks'])==185 and all(c['passed']is True for c in r['complete_prior_source_checks'])
assert pin(P/'REVIEW.json')['sha256']=='f191c36657da9532fef4d24412a137de9f1ec29767172c77c74ad92602b3238a'
for v in r['full_explicit_SOURCE_META_reads'].values():assert pin(Path(v['path']))==v
t=json.loads((P/'ACTUAL_SOURCE_REVIEW_TOOL_RETURNS.json').read_bytes());tr=t['terminal_tool_return']
assert t['source_only']is True and t['closed']is True and t['actual_tool_terminal_return_observed']is True
assert type(tr['exit_code'])is int and tr['exit_code']==0 and 'session_id'not in tr and tr['chunk_id']=='94f905'
assert not(P/'MANIFEST.json').exists()
rows=[]
for f in sorted(P.iterdir()):
 assert f.is_file()and not f.is_symlink()
 if f.suffix=='.py':ast.parse(f.read_bytes())
 v=pin(f);v['relative_path']=f.name;rows.append(v)
m=dict(schema='INDEPENDENT_FIXED_ROOT_FULLBUILD_SOURCE_BINDER_PEER_MANIFEST_V1',source_only=True,
 reviewed_generator_sha256=r['fixed_generator']['sha256'],review_sha256=pin(P/'REVIEW.json')['sha256'],
 all_original_five_stages_preserved=True,original_caps=r['original_caps'],
 source_check_count=369,members=rows,member_count=len(rows),member_bytes=sum(v['size_bytes']for v in rows),
 actual_saved_PREP_peer_authenticated_here=False,reviewed_generator_or_host_or_project_executed=False,
 actual_new_fullbuild_or_INPUT_or_native_or_scientific_qualification=None)
(P/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
for v in rows:assert pin(Path(v['path']))=={k:w for k,w in v.items()if k!='relative_path'}
print(json.dumps(dict(source_only=True,manifest=pin(P/'MANIFEST.json'),review=pin(P/'REVIEW.json'),
 members=len(rows),source_checks=369,actual_project_executed=False),indent=2))
