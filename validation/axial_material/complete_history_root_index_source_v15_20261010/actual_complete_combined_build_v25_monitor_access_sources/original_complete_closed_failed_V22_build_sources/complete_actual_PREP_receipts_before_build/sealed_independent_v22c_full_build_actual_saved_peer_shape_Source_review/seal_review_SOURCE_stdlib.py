from pathlib import Path
import ast,hashlib,json,os,stat
P=Path('/private/tmp/axmat_v22c_fullbuild_actual_sealed_peer_shape_SOURCE_review_5ihu8mkh')
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode)and s.st_nlink==1
 with p.open('rb')as f:
  assert identity(os.fstat(f.fileno()))==identity(s)
  b=f.read();assert len(b)==s.st_size and f.read(1)==b'' and identity(os.fstat(f.fileno()))==identity(s)
 assert identity(p.lstat())==identity(s)
 return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=identity(s))
r=json.loads((P/'REVIEW.json').read_bytes());assert r['PASS']is True and r['blockers']==[]
assert r['check_count']==len(r['checks'])==403 and all(c['passed']is True for c in r['checks'])
assert pin(P/'REVIEW.json')['sha256']=='642bff62750c5201f9c1549dae1d40f4d3e2a4e6af26c5b636a0ab81fe2e98e8'
for v in r['full_explicit_SOURCE_META_reads'].values():assert pin(Path(v['path']))==v
t=json.loads((P/'ACTUAL_SOURCE_META_REVIEW_TOOL_TERMINAL_RETURN.json').read_bytes());tr=t['terminal_tool_return']
assert t['source_only']is True and t['closed']is True and t['actual_tool_terminal_return_observed']is True
assert type(tr['exit_code'])is int and tr['exit_code']==0 and 'session_id'not in tr and tr['chunk_id']=='041446'
assert not(P/'MANIFEST.json').exists();rows=[]
for f in sorted(P.rglob('*')):
 assert not f.is_symlink()
 if f.is_dir():continue
 if f.suffix=='.py':ast.parse(f.read_bytes())
 v=pin(f);v['relative_path']=f.relative_to(P).as_posix();rows.append(v)
m=dict(schema='INDEPENDENT_V22C_FULLBUILD_SOURCE_META_PEER_SEALED_MANIFEST_V1',source_only=True,
 qualified_generator_sha256=r['qualified_generator']['sha256'],actual_savedPREP_peer_sha256=r['actual_sealed_savedPREP_peer']['sha256'],
 review_sha256=pin(P/'REVIEW.json')['sha256'],checks403_new_plus369_original=True,
 original_fullcaps=r['original_caps'],members=rows,member_count=len(rows),member_bytes=sum(v['size_bytes']for v in rows),
 actual_source_binder_or_business_executed=False,actual_new_build_or_scientific_qualification=None)
(P/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
for v in rows:assert pin(Path(v['path']))=={k:w for k,w in v.items()if k!='relative_path'}
print(json.dumps(dict(source_only=True,manifest=pin(P/'MANIFEST.json'),review=pin(P/'REVIEW.json'),
 members=len(rows),new_Sourcechecks403=True,prior_Sourcechecks369=True,actual_source_binder_or_business_executed=False),indent=2))
