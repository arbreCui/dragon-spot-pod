import hashlib,json,os,shutil,stat
from pathlib import Path
D=Path("/private/tmp/axmat_native_v23_actual_BOUND_complete_independent_SOURCE_review_20261010_599a7s57")
P=Path('/private/tmp/axmat_complete_native_v23_actual_BOUND_SOURCE_ROOT_20261010_748877')
def pin(p):
 s=p.lstat();assert p.is_absolute() and p.resolve()==p and stat.S_ISREG(s.st_mode) and s.st_nlink==1
 with p.open('rb') as f:b=f.read();assert f.read(1)==b'' and len(b)==s.st_size
 t=p.lstat();assert (s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)==(t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns)
 return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns])
rv=json.loads((D/'REVIEW.json').read_text())
assert rv['schema']=='INDEPENDENT_ACTUAL_BOUND_COMPLETE_NATIVE_SOURCE_REVIEW_V1' and rv['status']=='PASS_ACTUAL_BOUND_COMPLETE_NATIVE_SOURCE_ONLY' and rv['all_checks_typed_true'] is True and rv['blockers']==[]
assert len(rv['checks'])==rv['check_count']==11449 and all(type(c['passed']) is bool and c['passed'] is True for c in rv['checks']) and len({c['check'] for c in rv['checks']})==len(rv['checks'])
fields=('actual_bound_Source_manifest_pin','actual_binding_pin','actual_host_pin','actual_checker_pin','actual_Root_binding_tool_receipt_pin')
for key in fields:assert set(rv[key])=={'path','sha256','size_bytes','identity'} and pin(Path(rv[key]['path']))==rv[key]
m=json.loads((P/'Root_actual_complete_bound_native_SOURCE_manifest.json').read_text())
assert set(m['members'])|{'Root_actual_complete_bound_native_SOURCE_manifest.json'}=={str(p.relative_to(P)) for p in P.rglob('*') if p.is_file()}
for name,q in m['members'].items():
 assert pin(P/name)==q
 qdest=D/'COMPLETE_ACTUAL_BOUND_SOURCE'/name;qdest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/name,qdest);assert pin(qdest)['sha256']==q['sha256'] and pin(qdest)['size_bytes']==q['size_bytes']
dest=D/'COMPLETE_ACTUAL_BOUND_SOURCE'/'Root_actual_complete_bound_native_SOURCE_manifest.json';shutil.copyfile(P/dest.name,dest);assert pin(dest)['sha256']==rv['actual_bound_Source_manifest_pin']['sha256']
for src,destname in [(Path('/private/tmp/spot_generate_native_v23_actual_bound_Source_auditor_stdlib.py'),'generate_v23_actual_bound_Source_auditor_stdlib.py'),(Path('/private/tmp/spot_generate_native_v23_actual_bound_Source_auditor_stdlib.initial_failed.py'),'generate_v23_actual_bound_Source_auditor_stdlib.initial_failed.py'),(Path(rv['original8133_bound_review_reference_pin']['path']),'original8133_complete_actual_bound_Source_REVIEW.json')]:
 shutil.copyfile(src,D/destname);assert pin(src)['sha256']==pin(D/destname)['sha256']
for name,q in m['members'].items():assert pin(P/name)==q
assert pin(P/'Root_actual_complete_bound_native_SOURCE_manifest.json')==rv['actual_bound_Source_manifest_pin']
for key in fields:assert pin(Path(rv[key]['path']))==rv[key]
(D/'REPORT.txt').write_text('SOURCE-only PASS: actual bound complete native v23, 274 files including manifest.\n11,449 typed checks; complete original 268-file mother Source copied and preserved; host 11 + checker 2 global hunks reverse entire bytes and AST; every function unchanged.\nAll original 129 saved declarations retained exactly; original material payloads not freshly read or hashed. Real Source admission748877 EXIT0, binderf73f14 EXIT0 and prior BUILD65203e EXIT1 retained.\nNo native, binder, guard, helper, reader, API, compile or numerical operation executed. No native bytes, RSS, full BUILD/INPUT or scientific qualification created.\n')
manifest=dict(schema='INDEPENDENT_ACTUAL_BOUND_COMPLETE_NATIVE_V23_SOURCE_REVIEW_PACKAGE_MANIFEST_V1',source_only=True,members={str(p.relative_to(D)):pin(p) for p in sorted(D.rglob('*')) if p.is_file() and p.name!='MANIFEST.json'},excludes_own_manifest=True)
f=D/'MANIFEST.json'
with f.open('x') as out:json.dump(manifest,out,indent=2,allow_nan=False);out.write('\n')
for name,q in manifest['members'].items():assert pin(D/name)==q
print(json.dumps(dict(status='SEALED_PASS_ACTUAL_BOUND_COMPLETE_NATIVE_SOURCE_ONLY',manifest=pin(f),review=pin(D/'REVIEW.json'),member_count=len(manifest['members']),check_count=rv['check_count'],exact_five_consumed_pins=True,no_candidate_API_guard_native_or_numeric_executed=True)))

