import hashlib,json,os,shutil,stat,tempfile
from pathlib import Path
OLD=Path('/private/tmp/axmat_native_v23_actual_BOUND_complete_independent_SOURCE_review_20261010_599a7s57')
D=Path(tempfile.mkdtemp(prefix='axmat_native_v23_actual_BOUND_complete_SOURCE_review_final_20261010_',dir='/private/tmp'))
def pin(p):
 s=p.lstat();assert p.is_absolute() and p.resolve()==p and stat.S_ISREG(s.st_mode) and s.st_nlink==1
 with p.open('rb') as f:b=f.read();assert f.read(1)==b'' and len(b)==s.st_size
 t=p.lstat();assert (s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)==(t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns)
 return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns])
oldfiles={str(p.relative_to(OLD)):pin(p) for p in sorted(OLD.rglob('*')) if p.is_file()}
for name,q in oldfiles.items():
 dest=D/('original_own_incomplete_nested_manifest.json' if name=='MANIFEST.json' else name)
 dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(q['path'],dest);assert pin(dest)['sha256']==q['sha256'] and pin(dest)['size_bytes']==q['size_bytes']
for src,name in [(Path('/private/tmp/spot_native_v23_actual_bound_Source_review_seal_correction_actual_tools.json'),'actual_original_seal_and_failed_inventory_tool_returns.json'),(Path(__file__),'correct_own_seal_manifest_root_only_stdlib.py')]:
 shutil.copyfile(src,D/name)
rv=json.loads((D/'REVIEW.json').read_text());assert rv['schema']=='INDEPENDENT_ACTUAL_BOUND_COMPLETE_NATIVE_SOURCE_REVIEW_V1' and rv['status']=='PASS_ACTUAL_BOUND_COMPLETE_NATIVE_SOURCE_ONLY' and rv['all_checks_typed_true'] is True and rv['blockers']==[] and rv['check_count']==11449
for k in ('actual_bound_Source_manifest_pin','actual_binding_pin','actual_host_pin','actual_checker_pin','actual_Root_binding_tool_receipt_pin'):assert pin(Path(rv[k]['path']))==rv[k]
P=Path(rv['actual_bound_Source_manifest_pin']['path']).parent
m=json.loads((P/'Root_actual_complete_bound_native_SOURCE_manifest.json').read_text())
assert len(m['members'])==273
for name,q in m['members'].items():
 assert pin(P/name)==q
 copied=pin(D/'COMPLETE_ACTUAL_BOUND_SOURCE'/name);assert copied['sha256']==q['sha256'] and copied['size_bytes']==q['size_bytes']
assert pin(P/'Root_actual_complete_bound_native_SOURCE_manifest.json')==rv['actual_bound_Source_manifest_pin']
actual_src={str(p.relative_to(D/'COMPLETE_ACTUAL_BOUND_SOURCE')) for p in (D/'COMPLETE_ACTUAL_BOUND_SOURCE').rglob('*') if p.is_file()}
assert actual_src==set(m['members'])|{'Root_actual_complete_bound_native_SOURCE_manifest.json'} and len(actual_src)==274
proof=dict(schema='INDEPENDENT_V23_ACTUAL_BOUND_SOURCE_REVIEW_OWN_SEAL_COMPLETENESS_CORRECTION_V1',original_sealed_review_package=str(OLD),original_manifest_pin=oldfiles['MANIFEST.json'],original_original_TOOL_SEAL_EXIT0_and_actual_terminal_inventory_EXIT1_preserved=True,correction='Manifest excludes only its root file; all 9 original nested MANIFEST.json Source files must remain listed.',all_original_286_package_files_SHA_bytes_preserved=True,all_actual_bound_274_Source_files_present_SHA_bytes_equal=True,all11_449_review_conditions_unchanged=True,Root_candidate_Source_unchanged=True,new_candidate_native_numeric_execution=False)
with (D/'OWN_SEAL_COMPLETENESS_CORRECTION_PROOF.json').open('x') as f:json.dump(proof,f,indent=2,allow_nan=False);f.write('\n')
members={str(p.relative_to(D)):pin(p) for p in sorted(D.rglob('*')) if p.is_file()}
assert len([k for k in members if k.endswith('/MANIFEST.json')])==9
manifest=dict(schema='INDEPENDENT_ACTUAL_BOUND_COMPLETE_NATIVE_V23_SOURCE_REVIEW_PACKAGE_MANIFEST_V1',source_only=True,members=members,member_count=len(members),excludes_only_own_root_manifest=True,complete_original_nested_manifests_included=True,all_actualbound274_Source_files_complete=True)
f=D/'MANIFEST.json'
with f.open('x') as o:json.dump(manifest,o,indent=2,allow_nan=False);o.write('\n')
assert set(members)=={str(p.relative_to(D)) for p in D.rglob('*') if p.is_file() and p!=f}
for name,q in members.items():assert pin(D/name)==q
for name,q in oldfiles.items():assert pin(OLD/name)==q
print(json.dumps(dict(status='SEALED_PASS_ACTUAL_BOUND_COMPLETE_NATIVE_SOURCE_ONLY',directory=str(D),manifest=pin(f),review=pin(D/'REVIEW.json'),member_count=len(members),actualbound_Source_file_count=274,all_nine_nested_manifests_included=True,check_count=11449,no_candidate_API_guard_native_or_numeric_executed=True)))

