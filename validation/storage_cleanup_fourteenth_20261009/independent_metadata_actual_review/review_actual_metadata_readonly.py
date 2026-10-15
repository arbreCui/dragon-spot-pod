from pathlib import Path
import gzip, hashlib, json, os, stat
H=Path(__file__).resolve().parent;ROOT=Path('/Users/wen/spot');V=ROOT/'validation';R=V/'storage_cleanup_fourteenth_20261009'
MS='90f6851e4fb4d40f795467ae06bb8669d8311d282b8c49253a9a1d805e582035';SS='886be02cde541acd00e922d5f67965250ca1b50dc8302e374904b3f0839d541d'
PINS={}
def identity(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode)and s.st_nlink==1 and p.resolve(strict=True)==p
 return dict(size=s.st_size,allocated=s.st_blocks*512,dev=s.st_dev,ino=s.st_ino,nlink=s.st_nlink,mode=s.st_mode,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns)
def raw(p,expected=None):
 p=Path(p);before=identity(p);value=p.read_bytes();h=hashlib.sha256(value).hexdigest();assert identity(p)==before
 if expected:assert h==expected,(str(p),h,expected)
 PINS[str(p)]=dict(path=str(p),sha256=h,**before);return value
def obj(p,expected=None):return json.loads(raw(p,expected))
m=obj(R/'audit_metadata_manifest.json',MS);raw(R/'manage_audit_metadata.py',SS)
assert m['management_source_sha256']==SS
result=obj(R/'audit_metadata_retirement_result.json');root=obj(R/'Root_actual_metadata_retirement_and_protected_restore.json')
selected={x['path']for x in m['records']};assert len(selected)==10
held=str(V/'storage_cleanup_20261008/preservation_baseline.json');missing=selected-{held}
assert root['kind']=='ROOT_ACTUAL_RETIREMENT_AND_ONE_PROTECTED_INVENTORY_RESTORATION'
assert root['retire_tool']==dict(initial_chunk='961fab',session_id=97713,terminal_chunk='08e247',actual_exit_code=0,closed=True,original_JSON_paths_retired_at_that_window=10)
assert root['restore_tool']==dict(initial_chunk='c4e803',session_id=None,terminal_chunk='c4e803',actual_exit_code=0,closed=True,path=held,sha256='e311d296eff2b9c9b8fd3cb7fb28dc4976e26ebe4229d8198dc50e473254288b')
assert type(root['retire_tool']['actual_exit_code'])is int and type(root['restore_tool']['actual_exit_code'])is int
assert set(root['final_retired_metadata_paths'])==missing and len(missing)==root['final_retired_metadata_count']==9 and root['held_original_path']==held
assert root['original_inode_and_ctime_restored']is False and root['scientific_credit']is False
assert result['status']=='TEN_ORIGINAL_INVENTORIES_RETIRED_ALL_BYTES_RECOVERABLE'and result['manifest_sha256']==MS and result['deleted_paths']==[x['path']for x in m['records']]and result['scientific_credit']is False
assert all(not os.path.lexists(p)for p in missing)
heldrow=next(x for x in m['records']if x['path']==held);restored=raw(held,heldrow['sha256']);currentidentity=identity(Path(held))
assert len(restored)==heldrow['size']and currentidentity['mode']==heldrow['mode']and currentidentity['mtime_ns']==heldrow['mtime_ns']
assert currentidentity['ino']!=heldrow['ino']and currentidentity['ctime_ns']!=heldrow['ctime_ns']
oldindex=obj(V/'storage_review_more_20261008/current_protection_index.json','53ea86ecd81baf22e3b86697af7db52f59c401c2672370b236a0262d1e367b74')
normalized=obj(V/'storage_review_more_20261008/normalized_protection_index.json','30893b4a333c6dc39df420b136b095e076e0ad2ac6255336b8e3eb26ced49b86')
assert selected.intersection(oldindex['canonical_protected_files'])=={held}and selected.intersection(normalized['protected_files'])=={held}
archives={}
for row in m['records']:
 path=Path(row['archive_path']);assert path.parent==R/'metadata_archives'and path.name==row['sha256']+'.json.gz'
 if str(path)in archives:
  assert archives[str(path)]['decoded_sha256']==row['sha256']and archives[str(path)]['decoded_bytes']==row['size'];continue
 data=raw(path,row['archive_sha256']);assert len(data)==row['archive_size']and identity(path)['allocated']==row['archive_allocated']
 before=identity(path);digest=hashlib.sha256();size=0
 with gzip.open(path,'rb')as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):digest.update(chunk);size+=len(chunk)
 assert digest.hexdigest()==row['sha256']and size==row['size']and identity(path)==before
 archives[str(path)]=dict(path=str(path),compressed_sha256=row['archive_sha256'],compressed_bytes=row['archive_size'],allocated_bytes=row['archive_allocated'],decoded_sha256=digest.hexdigest(),decoded_bytes=size)
assert len(archives)==8
assert set(str(p)for p in(R/'metadata_archives').iterdir())==set(archives)
def fingerprint():
 h=hashlib.sha256();regular=links=directories=0
 for folder,sub,files in os.walk(ROOT,followlinks=False):
  sub.sort();files.sort();sub[:]=[n for n in sub if Path(folder)/n not in(ROOT/'.git',R)]
  for name in sub+files:
   p=Path(folder)/name
   if str(p)in selected:continue
   s=p.lstat();path=str(p.relative_to(ROOT))
   if stat.S_ISREG(s.st_mode):row=[path,s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_blocks,s.st_mtime_ns,s.st_ctime_ns];regular+=1
   elif stat.S_ISLNK(s.st_mode):row=[path,'symlink',os.readlink(p)];links+=1
   elif stat.S_ISDIR(s.st_mode):row=[path,'directory_path'];directories+=1
   else:continue
   h.update(json.dumps(row,separators=(',',':')).encode()+b'\n')
 return dict(sha256=h.hexdigest(),regular_files=regular,symlinks=links,directory_paths=directories)
before=fingerprint();assert before==m['untouched_before']==result['unchanged_other_files']
prior=obj(Path('/private/tmp/spot_storage_fourteenth_metadata_archives_independent_review_20261009/independent_preexec_review.json'),'b95eeeae532946a7e4787dbcc4741304aeeaa6dee8a815447c59b51968bd0665')
assert prior['status']=='PASS'and prior['manifest_sha256']==MS and prior['management_source_sha256']==SS
for pin in prior['selected_control_docs_freshSHA']:raw(pin['path'],pin['sha256'])
raw(R/'RESTORE.txt')
after=fingerprint();assert after==before
for path,pin in PINS.items():assert identity(Path(path))=={k:pin[k]for k in identity(Path(path))}
report=dict(status='PASS',schema='SPOT_R14_METADATA_ACTUAL_RETIREMENT_AND_PROTECTED_RESTORATION_INDEPENDENT_REVIEW_V1',manifest_sha256=MS,management_source_sha256=SS,result_sha256=PINS[str(R/'audit_metadata_retirement_result.json')]['sha256'],Root_actual_two_window_observation_sha256=PINS[str(R/'Root_actual_metadata_retirement_and_protected_restore.json')]['sha256'],true_retire_tool=root['retire_tool'],true_restore_tool=root['restore_tool'],original_ten_retirement_window_result_preserved_not_rewritten=True,final_retired_count=9,final_absent_paths=sorted(missing),all_nine_absent_even_symlink=True,restored_historical_canonical_protected_path=held,restored_whole_SHA=heldrow['sha256'],restored_size_mode_mtime_exact=True,restored_current_identity=currentidentity,original_held_identity={k:heldrow[k]for k in currentidentity},original_inode_and_ctime_not_restored=True,historical_oldindex_protection_hit_count=1,historical_oldindex_and_normalized_fullSHA_unchanged=True,permanent_archives=8,all_unique_archives_compressed_fullSHA_AND_complete_decompressed_SHA_size_again_verified=True,archives=list(archives.values()),other10excluded_files_links_dirpaths_exact_beforeafter=before,all_original_control_reports_and_failure_receipts_fullSHA_preserved=True,all_current_scientific_INPUT_source_results_arrays_preserved_by_unchanged_regular_identity_boundary=True,current_scientific_CANON_NS_alias_resource_and_whole65_body_exclusion_previous_review_retained=True,previous_preexec_did_not_check_this_oldindex_edge_now_explicitly_corrected=True,archives_manifest_old_reports_failedfacts_and_restore_rule_retained=True,raw_nine_original_allocated_bytes=sum(x['allocated']for x in m['records']if x['path']in missing),unique_archives_allocated_bytes=sum(x['allocated_bytes']for x in archives.values()),currently_restored_baseline_allocated_bytes=currentidentity['allocated'],all_fullread_pins=list(PINS.values()),no_following_runtime_retirement_included_in_this_metadata_window=True,manage_retire_restore_pack_or_business_invoked_by_reviewer=False,formal_project_ART_written=False,files_deleted_by_reviewer=False,scientific_or_native_RSS_credit=False,limits=['True initial ten-path retirement and later one-path restore are separate facts; final state is nine missing and one restored, not ten missing.','Recovered protected baseline has identical bytes/mode/mtime; it has a new inode/ctime and old index was retained without rewriting old identity claims.','All eight gzip archives remain permanent even for the restored baseline, and old metadata readers restore corresponding original JSON before use.','Other project regular identities/symlink targets/directory paths were independently scanned twice;4GB result docs and35GB numerical arrays were not redundantly rehashed.','This verifies only the metadata retirement/restore window; any later runtime deletion requires separate fresh evidence.'])
with(H/'independent_actual_metadata_review.json').open('x')as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status='PASS',report_sha256=hashlib.sha256((H/'independent_actual_metadata_review.json').read_bytes()).hexdigest(),final_absent9=True,protected_restored1=True,gzip8_full_decode=True,others=before,business=False)),flush=True)
