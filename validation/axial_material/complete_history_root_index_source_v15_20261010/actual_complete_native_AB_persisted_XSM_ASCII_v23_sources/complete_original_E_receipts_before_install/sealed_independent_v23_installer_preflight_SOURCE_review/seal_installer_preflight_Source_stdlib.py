import hashlib,json,stat
from pathlib import Path
D=Path("/private/tmp/axmat_v23_ROOT_native_installer_preflight_finite_SOURCE_review_20261010_uy_o0v6g")
def pin(p):
 s=p.lstat();assert p.is_absolute() and p.resolve()==p and stat.S_ISREG(s.st_mode) and s.st_nlink==1;b=p.read_bytes();t=p.lstat();ids=lambda q:[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns];assert ids(s)==ids(t)
 return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns])
r=json.loads((D/'REVIEW.json').read_text());assert r['status']=='PASS_ROOT_NATIVE_INSTALLER_AND_PREFLIGHT_SOURCE_ONLY' and r['all_checks_typed_true'] is True and r['blockers']==[] and r['check_count']==len(r['checks'])==118 and all(c['passed'] is True for c in r['checks'])
for k in ('installer_pin','preflight_pin','writer_pin','actual_Root_Source_author_tool_receipt_pin','actual_complete_bound_Source_peer_pin','actual_postclose_writer_Source_peer_pin','actual_bound_Source_manifest_pin'):assert set(r[k])=={'path','sha256','size_bytes','identity'} and pin(Path(r[k]['path']))==r[k]
for p,q in r['all_complete_Source_META_input_pins'].items():assert pin(Path(p))==q
m=dict(schema='INDEPENDENT_ROOT_NATIVE_V23_INSTALLER_PREFLIGHT_SOURCE_REVIEW_PACKAGE_MANIFEST_V1',source_only=True,members={str(p.relative_to(D)):pin(p) for p in sorted(D.rglob('*')) if p.is_file() and p!=D/'MANIFEST.json'},excludes_only_root_manifest=True)
p=D/'MANIFEST.json'
with p.open('x') as f:json.dump(m,f,indent=2,allow_nan=False);f.write('\n')
assert set(m['members'])=={str(p.relative_to(D)) for p in D.rglob('*') if p.is_file() and p!=D/'MANIFEST.json'}
for name,q in m['members'].items():assert pin(D/name)==q
print(json.dumps(dict(status='SEALED_PASS_ROOT_NATIVE_INSTALLER_AND_PREFLIGHT_SOURCE_ONLY',manifest=pin(p),review=pin(D/'REVIEW.json'),member_count=len(m['members']),check_count=r['check_count'],installer_pin=r['installer_pin'],preflight_pin=r['preflight_pin'],no_candidate_or_native_or_guard_executed=True)))
