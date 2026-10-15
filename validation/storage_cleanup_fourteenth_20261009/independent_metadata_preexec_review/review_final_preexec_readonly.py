from pathlib import Path
import ast, hashlib, json, os, stat
H=Path(__file__).resolve().parent;ROOT=Path('/Users/wen/spot');V=ROOT/'validation';R=V/'storage_cleanup_fourteenth_20261009'
MS='90f6851e4fb4d40f795467ae06bb8669d8311d282b8c49253a9a1d805e582035';SS='886be02cde541acd00e922d5f67965250ca1b50dc8302e374904b3f0839d541d'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_bytes())
m=load(R/'audit_metadata_manifest.json');assert sha(R/'audit_metadata_manifest.json')==MS
source=(R/'manage_audit_metadata.py').read_text();assert hashlib.sha256(source.encode()).hexdigest()==SS==m['management_source_sha256']
tree=ast.parse(source);compile(tree,str(R/'manage_audit_metadata.py'),'exec')
imports={alias.name for n in tree.body if isinstance(n,ast.Import)for alias in n.names}|{n.module for n in tree.body if isinstance(n,ast.ImportFrom)}
assert imports=={'argparse','gzip','hashlib','json','os','pathlib','stat'}
defs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
segments={k:ast.get_source_segment(source,n)for k,n in defs.items()}
assert set(defs)=={'digest','identity','write_new','fingerprint','valid_plan','verified_archive','pack','load_manifest','retire','restore','main'}
assert "choices=('list', 'pack', 'retire', 'restore'), default='list'"in segments['main']
assert "else: print(json.dumps([r['path'] for r in valid_plan()]"in segments['main']
assert "assert expected and digest(MANIFEST) == expected"in segments['load_manifest']
assert "assert [r['path'] for r in m['records']] == [r['path'] for r in plan]"in segments['load_manifest']
assert "len(items) == 10"in segments['valid_plan']and "len({r['path'] for r in items}) == 10"in segments['valid_plan']
assert "p.parts[len(ROOT.parts) + 1].startswith('storage_cleanup_')"in segments['valid_plan']
assert 's.st_nlink == 1'in segments['identity']and 'path.resolve() == path'in segments['identity']and 'path.is_relative_to(ROOT)'in segments['identity']
assert "row = [str(p.relative_to(ROOT)), 'directory_path']"in segments['fingerprint']and 'directory_paths=directories'in segments['fingerprint']
assert 'before = identity(archive)'in segments['verified_archive']and 'assert identity(archive) == before'in segments['verified_archive']
assert 'h.hexdigest() == record[\'sha256\'] and size == record[\'size\']'in segments['verified_archive']
assert segments['retire'].count('.unlink()')==1 and "Path(r['path']).unlink()"in segments['retire']and 'verified_archive(r)'in segments['retire']
assert "assert now == {k: r[k] for k in now} and digest(p) == r['sha256']"in segments['retire']
assert 'fingerprint({r[\'path\'] for r in records}) == m[\'untouched_before\']'in segments['retire']
assert 'assert after == m[\'untouched_before\']'in segments['retire']and "assert all(not os.path.lexists(r['path']) for r in records)"in segments['retire']
assert 'created = False'in segments['restore']and 'created = True'in segments['restore']and "tmp.open('xb')"in segments['restore']
assert 'if created and os.path.lexists(tmp): tmp.unlink()'in segments['restore']and 'assert not os.path.lexists(tmp)'in segments['restore']
assert 'os.link(tmp, p); tmp.unlink()'in segments['restore']and 'restores_original_inode_or_ctime=False'in segments['restore']
assert "with path.open('x', encoding='utf-8')"in segments['write_new']and 'f.flush(); os.fsync(f.fileno())'in segments['write_new']
content=load(H/'archive_and_dependency_review.json');assert sha(H/'archive_and_dependency_review.json')=='5b5aabb3d21720468c67a95b32449bad359c0d3edce5f95f900cd03d498caffd'
assert content['manifest_sha256']==MS and content['source_sha256']==SS and content['all10_originals_still_present_fullSHA_identity_stable']is True and content['all8_gzip_fully_decompressed_fullSHA_size_equal']is True
selected={r['path']for r in m['records']};assert len(selected)==10
for record in content['all_fullread_pins']:
 p=Path(record['path']);s=p.lstat()
 for key,value in dict(size=s.st_size,allocated=s.st_blocks*512,dev=s.st_dev,ino=s.st_ino,nlink=s.st_nlink,mode=s.st_mode,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns).items():assert record[key]==value
 assert not p.is_symlink()and p.resolve(strict=True)==p
def fingerprint():
 h=hashlib.sha256();regular=links=directories=0
 for folder,sub,files in os.walk(ROOT,followlinks=False):
  sub.sort();files.sort();sub[:]=[name for name in sub if Path(folder)/name not in(ROOT/'.git',R)]
  for name in sub+files:
   p=Path(folder)/name
   if str(p)in selected:continue
   s=p.lstat();relative=str(p.relative_to(ROOT))
   if stat.S_ISREG(s.st_mode):record=[relative,s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_blocks,s.st_mtime_ns,s.st_ctime_ns];regular+=1
   elif stat.S_ISLNK(s.st_mode):record=[relative,'symlink',os.readlink(p)];links+=1
   elif stat.S_ISDIR(s.st_mode):record=[relative,'directory_path'];directories+=1
   else:continue
   h.update(json.dumps(record,separators=(',',':')).encode()+b'\n')
 return dict(sha256=h.hexdigest(),regular_files=regular,symlinks=links,directory_paths=directories)
before=fingerprint();assert before==m['untouched_before']
root_observation=load(R/'Root_predelete_archive_observation.json')
assert root_observation['archive_pack_tool']==dict(initial_chunk='e7f99b',session_id=57240,terminal_chunk='4387c4',actual_exit_code=0,closed=True)
assert root_observation['boundary_revision_tool']==dict(initial_chunk='aa95b3',session_id=49400,terminal_chunk='270778',actual_exit_code=0,closed=True)
assert root_observation['current_manifest_sha256']==MS and root_observation['source_sha256']==SS and root_observation['originals_still_present']is True
docs=[]
for folder in('storage_cleanup_20261008','storage_cleanup_more_20261008','storage_cleanup_tenth_20261009','storage_cleanup_eleventh_20261009'):
 p=V/folder/'REPORT.txt';docs.append(dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size))
for p in sorted((V/'storage_cleanup_eleventh_20261009/independent_preflight_review/reader_attempt01_stopped').glob('*.json')):
 if str(p)in selected:continue
 docs.append(dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size))
assert not os.path.lexists(R/'audit_metadata_retirement_result.json')
assert all(os.path.lexists(p)for p in selected)
after=fingerprint();assert before==after
assert sha(R/'audit_metadata_manifest.json')==MS and sha(R/'manage_audit_metadata.py')==SS
report=dict(status='PASS',schema='SPOT_R14_EXACT_TEN_LOSSLESS_AUDIT_METADATA_PREEXEC_INDEPENDENT_REVIEW_V1',manifest_sha256=MS,management_source_sha256=SS,plan_sha256='3123063df07044807785f11dff9070cee43452e1442b538fe7df243f8c1159df',fixed_paths=sorted(selected),candidate_count=10,unique_permanent_gzip_archives=8,content_and_current_dependency_report_path=str(H/'archive_and_dependency_review.json'),content_and_current_dependency_report_sha256='5b5aabb3d21720468c67a95b32449bad359c0d3edce5f95f900cd03d498caffd',full10_raw_SHA_and_identity_verified=True,full8_compressed_SHA_AND_decompressed_original_SHA_size_verified=True,archive_before_after_ordinary_canonical_singlelink_gates=True,all_gzip_archives_and_manifest_must_remain_permanent=True,original_allocated_bytes=content['raw_original_allocated_bytes'],archive_allocated_bytes=content['unique_archive_allocated_bytes'],expected_allocated_reduction_bytes=content['raw_original_allocated_bytes']-content['unique_archive_allocated_bytes'],only_metadata_not_scientific_results=True,current_2cad_fed209_whole65_descriptor_CANON_NAMESPACE_ALIAS_resource_root_exclusions=True,old_closed_readers_need_original_JSON_restored_first=True,active_formal_business_and_existing_restore_tools_do_not_read_candidates=True,original_results_reports_failure_receipts_logs_ledger_and_protection_index_unchanged=True,selected_control_docs_freshSHA=docs,default_list_has_no_write_or_child_call=True,retire_explicit_action_and_exact_cli_manifestSHA_gate=True,only_fixed_manifest_ten_paths_unlink_once=True,all_raw_fullSHA_identity_and_archive_complete_verify_before_unlink=True,all_other_regular_identity_symlink_targets_and_directory_paths_fingerprint_equal=before,independent_before_after_baseline_equal=True,root_pack_true0_CLOSED=root_observation['archive_pack_tool'],root_boundary_revision_true0_CLOSED=root_observation['boundary_revision_tool'],restore_single_exact_selected_path_only=True,restore_exclusive_owned_temp_only_and_atomic_nonoverwriting_link=True,source_result_write_exclusive_fsync_and_absence_lexists=True,restore_original_bytes_mode_mtime_but_not_inode_or_ctime=True,actual_retirement_outcome=None,actual_retirement_tool=None,source_AST_compiled_only_not_executed=True,manage_list_pack_retire_restore_called_by_reviewer=False,project_or_ART_written_by_reviewer=False,files_deleted=False,business_API_PREP_RUN_watch_worker_native_solver_called=False,scientific_or_native_RSS_credit=False,limits=['PASS qualifies only exact above manifest/source and unchanged project boundary, not an actual retirement result.','Stored historical snapshot/hash tables remain losslessly recoverable, and old source/reports are unchanged; a historical reader first restores matching JSON, and no old inode/ctime or current reproduction of historical whole-project fingerprints is promised.','Only metadata and required scope descriptors were read;35GB numerical INPUT files were not rehashed here.','No instantaneous APFS free-space release promise; claimed reduction is original allocation minus unique archives, before small report overhead.'])
with(H/'independent_preexec_review.json').open('x')as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status='PASS',manifest_sha256=MS,source_sha256=SS,report_sha256=sha(H/'independent_preexec_review.json'),candidate10=True,unique_gzip8=True,baseline=before,raw_allocated=content['raw_original_allocated_bytes'],gzip_allocated=content['unique_archive_allocated_bytes'],no_business=True)),flush=True)
