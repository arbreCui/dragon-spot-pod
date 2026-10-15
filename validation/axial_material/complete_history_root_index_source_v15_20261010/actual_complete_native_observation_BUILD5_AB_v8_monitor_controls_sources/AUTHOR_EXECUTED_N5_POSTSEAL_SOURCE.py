from pathlib import Path
import hashlib,json,stat
P=Path('/private/tmp/axmat_complete_native_observation_N5_closed_PS_only_UNREADY_Source_ei2bldc9');S=P.with_name(P.name+'_seal_receipt')
def i7(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 a=p.lstat();assert stat.S_ISREG(a.st_mode)and a.st_nlink==1 and not p.is_symlink();raw=p.read_bytes();assert i7(a)==i7(p.lstat());return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=i7(a))
mfpin=pin(P/'MANIFEST.json');m=json.loads((P/'MANIFEST.json').read_bytes());members={r['relative_path']:r['fullpin']for r in m['members']};dirs=m['complete_directory_identity']
assert {str(q.relative_to(P))for q in P.rglob('*')if q.is_file()}==set(members)|{'MANIFEST.json'}and {'.'}|{str(q.relative_to(P))for q in P.rglob('*')if q.is_dir()}==set(dirs)
for rel,wanted in members.items():assert pin(P/rel)==wanted
for rel,wanted in dirs.items():assert i7((P if rel=='.'else P/rel).lstat())==wanted
inputs=json.loads((P/'N5_ALL_ORIGINAL_SOURCE_AND_SMALL_META_FULLPINS.json').read_bytes())
for row in inputs['pins']:assert pin(Path(row['path']))==row
assert pin(P/'MANIFEST.json')==mfpin
out=dict(schema='FULL_N5_CLOSED_PS_ONLY_SOURCE_POSTSEAL_VERIFICATION_V1',source_only=True,manifest=mfpin,report=pin(P/'AUTHOR_N5_SOURCE_ONLY_REPORT.json'),member_count=m['member_count'],directory_count=len(dirs),all_complete_Source_member_names_dirs_full_EOF_SHA7ID_unchanged=True,all_original_inputs_unchanged=True,candidate_helper_guard_PS_lsof_compile_material_or_numeric_executed=False,new_business_or_science_qualified=False)
with(S/'FULL_SOURCE_POSTSEAL_VERIFICATION.json').open('x')as f:json.dump(out,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(out))
