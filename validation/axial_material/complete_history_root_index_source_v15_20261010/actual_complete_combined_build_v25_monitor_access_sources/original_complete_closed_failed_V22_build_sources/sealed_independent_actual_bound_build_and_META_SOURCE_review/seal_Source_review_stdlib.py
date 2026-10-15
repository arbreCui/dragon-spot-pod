"""Stdlib-only full Source peer package seal."""
import hashlib,json,pathlib,stat
P=pathlib.Path(__file__).parent
def pin(p):
 i=p.lstat();a=[i.st_dev,i.st_ino,i.st_mode,i.st_nlink,i.st_size,i.st_mtime_ns,i.st_ctime_ns]
 with p.open('rb') as f:d=hashlib.file_digest(f,'sha256').hexdigest()
 t=p.lstat();b=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
 if a!=b or not stat.S_ISREG(a[2]) or a[3]!=1:raise ValueError('full EOF single regular pin required')
 return dict(path=str(p),sha256=d,size_bytes=a[4],identity=a)
r=json.loads((P/'REVIEW.json').read_text())
if r['status']!='PASS_ACTUAL_BOUND_FULL_BUILD_AND_POSTCLOSE_META_SOURCE_ONLY' or r['all_checks_typed_true'] is not True or r['blockers']!=[] or len(r['checks'])!=r['check_count'] or not all(q['passed'] is True for q in r['checks']):raise ValueError('complete true Source review required')
for q in r['complete_reviewed_Source_and_META_file_pins']:
 if pin(pathlib.Path(q['path']))!=q:raise ValueError('third full EOF Source/META pin changed')
t=json.loads((P/'actual_review_tool_returns.json').read_text())
v=t['actual_tool_return']
if t['closed'] is not True or t['observed_terminal'] is not True or type(v['exit_code']) is not int or v['exit_code']!=0 or 'session_id' in v:raise ValueError('real closed reviewer0 required')
members=[pin(p) for p in sorted(P.iterdir()) if p.name!='MANIFEST.json']
m=dict(schema='INDEPENDENT_V22_FULL_BUILD_POSTCLOSE_META_SOURCE_PEER_MANIFEST_V1',source_only=True,members=members,member_count=len(members),member_bytes=sum(p['size_bytes'] for p in members),all_complete_Source_META_inputs_third_full_EOF_SHA7ID_stable=True,actual_review_exit_code=0,new_business_or_numeric_execution=False,whole_INPUT_native_or_science_qualified=False)
with (P/'MANIFEST.json').open('x') as f:json.dump(m,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(status='SEALED_FULL_SOURCE_ONLY_PASS',manifest=pin(P/'MANIFEST.json'),review=pin(P/'REVIEW.json'),member_count=len(members),actual_reviewer_chunk=v['chunk_id']),allow_nan=False))

