import ast, hashlib, json, os, stat
from pathlib import Path
ROOT=Path('/Users/wen/spot');R=ROOT/'validation/storage_cleanup_fourteenth_20261009'
O=Path('/private/tmp/spot_storage_fourteenth_exact5_preexec_independent_review_20261009');PINS={}
def identity(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p,sha=None):
 p=Path(p);before=identity(p);assert stat.S_ISREG(before[2]) and before[-1]==1 and p.resolve()==p
 h=hashlib.sha256()
 with p.open('rb')as f:
  s=os.fstat(f.fileno());assert [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]==before
  while b:=f.read(1024**2):h.update(b)
 assert identity(p)==before
 r=dict(path=str(p),sha256=h.hexdigest(),size_bytes=before[3],identity=before)
 if sha:assert r['sha256']==sha
 PINS[str(p)]=r;return r
def pairs(rows):
 d={}
 for k,v in rows:assert k not in d;d[k]=v
 return d
def read(p,sha=None):
 r=pin(p,sha);x=json.loads(Path(p).read_text(),object_pairs_hook=pairs);assert identity(p)==r['identity'];return x
def fingerprint_without_management_import(excluded):
 h=hashlib.sha256();count=links=directories=0
 for base,dirs,files in os.walk(ROOT,followlinks=False):
  dirs.sort();files.sort();dirs[:]=[d for d in dirs if Path(base)/d not in (ROOT/'.git',R)]
  for name in dirs+files:
   p=Path(base)/name
   if str(p)in excluded:continue
   s=p.lstat()
   if stat.S_ISREG(s.st_mode):
    row=[str(p.relative_to(ROOT)),s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_blocks,s.st_mtime_ns,s.st_ctime_ns];count+=1
   elif stat.S_ISLNK(s.st_mode):row=[str(p.relative_to(ROOT)),'symlink',os.readlink(p)];links+=1
   elif stat.S_ISDIR(s.st_mode):row=[str(p.relative_to(ROOT)),'directory_path'];directories+=1
   else:continue
   h.update(json.dumps(row,separators=(',',':')).encode()+b'\n')
 return dict(sha256=h.hexdigest(),regular_files=count,symlinks=links,directory_paths=directories)
source=R/'manage_old_runtime_copies.py';helper=R/'manage_audit_metadata.py';planpath=R/'old_runtime_dependency_review/exact5_runtime_candidates.json';mpath=R/'runtime_retirement_manifest.json'
pin(source,'0ec862f16b566add1eea3ad6610237b34763dee45ea4862457ef22cdcd47f14f');pin(helper,'886be02cde541acd00e922d5f67965250ca1b50dc8302e374904b3f0839d541d')
plan=read(planpath,'02f7ffe3c5775e381c2326cc766dc3f9274590635fda8838338c30e55835d4ee')
manifest=read(mpath,'00b3ff33f045f825137763dca4dbaffa61d013c92e0e3c5e946d4e72eb1f1096');rows=plan['candidates']
assert manifest['candidates']==rows and manifest['kind']=='FIVE_EXACT_OLD_FAILED_RUNTIME_COPIES_ONLY' and manifest['scientific_credit']is False
assert manifest['source_sha256']==PINS[str(source)]['sha256'] and manifest['helper_sha256']==PINS[str(helper)]['sha256'] and manifest['plan_sha256']==PINS[str(planpath)]['sha256']
assert [r['version']for r in rows]==[2,3,4,5,6]
for r in rows:
 expected=ROOT/'validation/artifacts'/f"axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v{r['version']}-20261008/runtime/Dragon"
 assert r['path']==str(expected);fresh=pin(expected,r['sha256']);assert fresh['identity']==r['identity'] and fresh['size_bytes']==r['size_bytes']==9225720
 assert r['sha256']=='77fe179d3230eefcc7d9d7897650e414f342e7579ba65f9e6c641bfd9b1db7ba'
primary=rows[0]['retained_primary'];assert all(r['retained_primary']==primary for r in rows)
fresh=pin(primary['path'],primary['sha256']);assert fresh['identity']==primary['identity'] and fresh['size_bytes']==primary['size_bytes']
assert len({tuple(r['identity'][:2])for r in rows})==5 and tuple(primary['identity'][:2])not in {tuple(r['identity'][:2])for r in rows}
observation=read(R/'Root_runtime_preparation_observation.json');tool=observation['prepare_tool']
assert observation['kind']=='ROOT_OBSERVED_EXACT5_PREPARED_NO_DELETION' and observation['source_sha256']==PINS[str(source)]['sha256'] and observation['manifest_sha256']==PINS[str(mpath)]['sha256']
assert tool==dict(initial_chunk='32f85f',session_id=26895,terminal_chunk='4d2d92',actual_exit_code=0,closed=True) and type(tool['actual_exit_code'])is int
assert observation['actual_retire_tool']is None and not os.path.lexists(R/'runtime_retirement_result.json')
assert observation['first_prepare_failed_before_mutation']['actual_exit_code']==1
assert (R/observation['first_prepare_failed_before_mutation']['preserved_source']).is_file()
# AST/source inspection only. Management/helper modules are never imported.
src=source.read_text();ast.parse(src);ht=helper.read_text();ast.parse(ht)
for text in ("default='list'", "assert n.manifest_sha256 and h['digest'](MANIFEST) == n.manifest_sha256", "m['candidates'] == rows", "same_identity(h, p, r['identity'])", "assert after == m['untouched_before']", "tmp.open('xb')", "os.link(tmp, p)", "if created and os.path.lexists(tmp): tmp.unlink()"):
 assert text in src,text
assert "if __name__ == '__main__': main()"in src and "if __name__ == '__main__': main()"in ht
excluded={r['path']for r in rows};before=fingerprint_without_management_import(excluded);assert before==manifest['untouched_before']
after=fingerprint_without_management_import(excluded);assert after==before
for path,r in PINS.items():assert identity(path)==r['identity']
report=dict(schema='SPOT_EXACT5_RUNTIME_SOURCE_PREPARED_MANIFEST_PREEXEC_INDEPENDENT_REVIEW_V1',status='PASS',manifest_sha256=PINS[str(mpath)]['sha256'],source_sha256=PINS[str(source)]['sha256'],helper_sha256=PINS[str(helper)]['sha256'],plan_sha256=PINS[str(planpath)]['sha256'],selected_count=5,all_literal_paths_exact_V2_V6_Oct08=True,all5_and_retained_primary_full_SHA_original_identity_fresh=True,all_original_failed_facts_unchanged=True,source_only_default_list_and_retire_restore_pin_and_atomic_nooverwrite_ownedtemp_contract_reviewed=True,manifest_full_exact_candidate_and_source_helper_plan_bindings_verified=True,prepared_fingerprint=before,independent_fingerprint_before=before,independent_fingerprint_after=after,expectedwholebaseline=before,Root_genuine_prepare_tool=tool,Root_first_failed_prepare_source_and_actual1_preserved=True,runtime_retirement_not_started_or_executed_by_this_reader=True,management_helper_or_business_module_imported=False,management_prepare_retire_restore_list_function_called=False,files_deleted=0,formal_or_ART_written=False,scientific_credit=False,scope='Fixed5 management source and actual prepared manifest/file snapshot only; sealed fullscience37/12 source proof reused unchanged.',full_read_pins=list(PINS.values()),audit_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
with (O/'REPORT.json').open('x')as f:json.dump(report,f,indent=2);f.write('\n')
print(json.dumps(dict(status='PASS',report=str(O/'REPORT.json'),report_sha256=hashlib.sha256((O/'REPORT.json').read_bytes()).hexdigest(),manifest_sha256=report['manifest_sha256'],baseline=before)))
