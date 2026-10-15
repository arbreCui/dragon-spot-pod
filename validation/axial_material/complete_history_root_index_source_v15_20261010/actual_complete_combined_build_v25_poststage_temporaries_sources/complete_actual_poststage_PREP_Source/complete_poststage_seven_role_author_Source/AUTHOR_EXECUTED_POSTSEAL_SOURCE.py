from pathlib import Path
import hashlib,json,stat
P=Path('/private/tmp/axmat_V25_poststage_temporaries_complete_UNREADY_Source_v2ept7ev');S=P.with_name(P.name+'_seal_receipt')
def i7(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 a=p.lstat();assert stat.S_ISREG(a.st_mode)and a.st_nlink==1 and not p.is_symlink();r=p.read_bytes();assert i7(a)==i7(p.lstat());return dict(path=str(p),sha256=hashlib.sha256(r).hexdigest(),size_bytes=len(r),identity=i7(a))
before=pin(P/'MANIFEST.json');m=json.loads((P/'MANIFEST.json').read_bytes());files={str(q.relative_to(P))for q in P.rglob('*')if q.is_file()};dirs={'.'}|{str(q.relative_to(P))for q in P.rglob('*')if q.is_dir()}
assert files==set(m['members'])|{'MANIFEST.json'}and dirs==set(m['directories'])
for rel,wanted in m['members'].items():assert pin(P/rel)==wanted
for rel,wanted in m['directories'].items():assert i7((P if rel=='.'else P/rel).lstat())==wanted
for row in json.loads((P/'ALL_ORIGINAL_READ_SOURCE_AND_SMALL_META_PINS.json').read_bytes())['full_read_input_pins']:assert pin(Path(row['path']))==row
assert pin(P/'MANIFEST.json')==before
out=dict(schema='FULL_V25_POSTSTAGE_TEMPORARIES_SOURCE_POSTSEAL_VERIFICATION_V1',source_only=True,all_complete_Source_members_dirs_full_EOF_SHA7ID_unchanged=True,all_original_Source_and_small_META_fullpins_unchanged=True,manifest=before,member_count=m['member_count'],directory_count=len(dirs),author_report=pin(P/'AUTHOR_SOURCE_ONLY_REPORT.json'),candidate_helper_guard_API_compile_numeric_executed=False,new_business_or_science_qualified=False)
with(S/'FULL_SOURCE_POSTSEAL_VERIFICATION.json').open('x')as f:json.dump(out,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(out))
