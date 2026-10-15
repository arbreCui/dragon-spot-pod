"""Stdlib-only finite failed-build evidence seal, no project execution."""
import hashlib,json,pathlib,stat
P=pathlib.Path(__file__).parent
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 a=identity(p)
 if not stat.S_ISREG(a[2]) or a[3]!=1:raise ValueError('single regular file required')
 with p.open('rb') as f:d=hashlib.file_digest(f,'sha256').hexdigest()
 if a!=identity(p):raise ValueError('full EOF identity changed')
 return dict(path=str(p),sha256=d,size_bytes=a[4],identity=a)
r=json.loads((P/'REVIEW.json').read_text())
if r['status']!='PASS_ACTUAL_FAILED_BUILD_EVIDENCE_ONLY' or r['all_checks_typed_true'] is not True or r['blockers']!=[] or len(r['checks'])!=r['check_count'] or not all(q['passed'] is True for q in r['checks']):raise ValueError('complete saved failure evidence review required')
for q in r['all_complete_saved_Source_META_file_pins']:
 if pin(pathlib.Path(q['path']))!=q:raise ValueError('third complete EOF changed '+q['path'])
ns=json.loads(pathlib.Path(r['actual_failed_build_complete_namespace_pin']['path']).read_text())
for view in ns['namespaces']:
 if pathlib.Path(view['root']).name!='actual_complete_combined_build_v22_receipts':
  for rel,i in view['directories'].items():
   if identity(pathlib.Path(view['root'])/rel)!=i:raise ValueError('complete namespace directory changed')
actual=json.loads((P/'actual_review_tool_returns.json').read_text())
t=actual['actual_tool_return']
if actual['closed'] is not True or actual['observed_terminal'] is not True or type(t['exit_code']) is not int or t['exit_code']!=0 or 'session_id' in t:raise ValueError('real closed review0 required')
members=[pin(p) for p in sorted(P.iterdir()) if p.name!='MANIFEST.json']
m=dict(schema='INDEPENDENT_V22_ACTUAL_FAILED_BUILD_SAVED_META_COMPLETE_REVIEW_MANIFEST_V1',source_only_reviewer=True,members=members,member_count=len(members),member_bytes=sum(q['size_bytes'] for q in members),all_reviewed558_files_third_full_EOF_SHA7ID_stable=True,actual_review_EXIT0_observed=True,actual_business_build_failed=True,whole_build_INPUT_native_science_qualified=False)
with (P/'MANIFEST.json').open('x') as f:json.dump(m,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(status='SEALED_SAVED_ACTUAL_FAILURE_EVIDENCE_ONLY',manifest=pin(P/'MANIFEST.json'),review=pin(P/'REVIEW.json'),member_count=len(members),actual_review_chunk=t['chunk_id']),allow_nan=False))

