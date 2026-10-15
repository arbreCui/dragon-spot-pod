import hashlib,json,stat
from pathlib import Path
D=Path("/private/tmp/axmat_v23_ROOT_native_postclose_writer_finite_SOURCE_review_20261010_m2zisvx7")
def pin(p):
    s=p.lstat();assert p.is_absolute() and p.resolve()==p and stat.S_ISREG(s.st_mode) and s.st_nlink==1
    b=p.read_bytes();t=p.lstat();assert (s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)==(t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns)
    return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns])
for name in ('initial_failed','second_failed'):
    src=Path('/private/tmp/spot_independent_native_v23_metadata_writer_literal_source_review.'+name+'.py')
    dest=D/('review_writer_literal_Source_stdlib.'+name+'.py');assert not dest.exists();dest.write_bytes(src.read_bytes())
rv=json.loads((D/'REVIEW.json').read_text());assert rv['status']=='PASS_ROOT_NATIVE_POSTCLOSE_METADATA_SOURCE_ONLY' and rv['all_checks_typed_true'] is True and rv['blockers']==[] and rv['check_count']==len(rv['checks'])==74 and all(c['passed'] is True for c in rv['checks'])
assert 'installer_pin' not in rv and rv['installer_Source_reviewed'] is False
for k in ('writer_pin','original_reviewed_writer_pin','prior_Source_review_pin'):assert pin(Path(rv[k]['path']))==rv[k]
for name,rc in (('actual_initial_review_count_failed_tool_return.json',1),('actual_second_review_count_failed_tool_return.json',1),('actual_complete_writer_Source_review_tool_return.json',0)):
    tr=json.loads((D/name).read_text());r=tr['actual_tool_return'];assert type(r['exit_code']) is int and r['exit_code']==rc and 'session_id' not in r and tr['closed'] is True and tr['observed_terminal'] is True
m=dict(schema='INDEPENDENT_V23_ROOT_NATIVE_POSTCLOSE_WRITER_LITERAL_SOURCE_REVIEW_MANIFEST_V1',source_only=True,members={str(p.relative_to(D)):pin(p) for p in sorted(D.rglob('*')) if p.is_file() and p.name!='MANIFEST.json'},excludes_own_manifest=True)
p=D/'MANIFEST.json'
with p.open('x') as f:json.dump(m,f,indent=2,allow_nan=False);f.write('\n')
for name,v in m['members'].items():assert pin(D/name)==v
print(json.dumps(dict(status='SEALED_PASS_ROOT_NATIVE_POSTCLOSE_METADATA_SOURCE_ONLY',manifest=pin(p),review=pin(D/'REVIEW.json'),member_count=len(m['members']),check_count=rv['check_count'],writer_pin=rv['writer_pin'],no_installer_pin_created=True,no_reviewed_code_executed=True)))

