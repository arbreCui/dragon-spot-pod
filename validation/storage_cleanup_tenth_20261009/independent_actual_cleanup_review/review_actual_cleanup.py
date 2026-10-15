"""Read-only actual cleanup review. Never invokes cleanup, restore or business."""
import hashlib
import json
import os
import stat
import time
from pathlib import Path

ROOT=Path('/Users/wen/spot');R=ROOT/'validation/storage_cleanup_tenth_20261009'
OUT=Path('/private/tmp/spot_storage_tenth_result_preservation_readonly_review_20261009')
M_SHA='b1d2b4b2b2a0e12b8926f0f6d6f488db2ed22b637d1984eaf57770efdeb3913b'
PF_SHA='a8eb7d19aef6e45a4d932c452efcb59803eb4d4b90f169a5f00523f7b3c1484b'
RESULT_SHA='3dc9383b393f48746b5f911a4c1cb94dc8c4be6377802feb65009752bdcea8e6'
TOOL_SHA='e45940f85c18081f936e770f50c28b7503ffc0ec74b0cff4c8f906690bc32d70'
PRE_REVIEW_SHA='62b14680458212fb5fa6f3b9536aa4ccc6810efeb2646b4282d9f2cc99070cdd'
PINS={};START=time.monotonic()

def identity(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def fullpin(p,expected=None):
    p=Path(p);before=identity(p)
    assert p.is_absolute() and '..' not in p.parts and p.parent.resolve(strict=True)==p.parent and stat.S_ISREG(before[2])
    if type(expected)is dict:
        assert before==expected['identity'] and before[3]==expected['size'],str(p)
        if 'allocated_bytes' in expected:assert p.lstat().st_blocks*512==expected['allocated_bytes'],str(p)
    h=hashlib.sha256();length=0
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
        s=os.fstat(f.fileno());assert [s.st_dev,s.st_ino]==before[:2]
        while block:=f.read(1024**2):h.update(block);length+=len(block)
    assert identity(p)==before and length==before[3]
    digest=h.hexdigest()
    if expected is not None:assert digest==(expected['sha256'] if type(expected)is dict else expected),(str(p),digest)
    record=dict(path=str(p),identity=before,size=length,sha256=digest)
    if str(p) in PINS:assert PINS[str(p)]==record,str(p)
    PINS[str(p)]=record;return record

def load(p,expected=None):
    record=fullpin(p,expected);data=Path(p).read_bytes();assert hashlib.sha256(data).hexdigest()==record['sha256'] and identity(Path(p))==record['identity']
    return json.loads(data)

def save(name,value):
    with (OUT/name).open('xb') as f:
        f.write((json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode());f.flush();os.fsync(f.fileno())

def snapshot():
    files={};links={};dirs=[]
    for current,sub,names in os.walk(ROOT,followlinks=False):
        base=Path(current)
        if base==ROOT:sub[:]=[s for s in sub if s!='.git']
        sub[:]=[s for s in sub if base/s!=R]
        dirs.append(str(base.relative_to(ROOT)))
        for name in sub+names:
            p=base/name;s=p.lstat();rel=str(p.relative_to(ROOT));ident=identity(p)
            if stat.S_ISLNK(s.st_mode):links[rel]=[ident,os.readlink(p)]
            elif stat.S_ISREG(s.st_mode):files[rel]=ident
    return {'files':files,'links':links,'dirs':sorted(dirs)}

def fingerprint(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

m=load(R/'manifest.json',M_SHA);pre=load(R/'preflight.json',PF_SHA);result=load(R/'cleanup_result.json',RESULT_SHA)
terminal=load(R/'cleanup_terminal_observation.json',TOOL_SHA)
prior=load(OUT/'independent_preflight_review.json',PRE_REVIEW_SHA)
assert prior['status']=='PASS' and prior['manifest_sha256']==M_SHA and prior['preflight_sha256']==PF_SHA
assert terminal['initial_tool']['chunk_id']=='7b96af' and terminal['initial_tool']['session_id']==25157
assert terminal['completion_tool']['chunk_id']=='fd61d0' and terminal['completion_tool']['exit_code']==0 and terminal['completion_tool'].get('session_id') is None
assert terminal['closed'] is True and terminal['exit_code']==0 and json.loads(terminal['completion_tool']['output'])==result
assert result['status']=='PASS_ACTUAL_EXACT_DUPLICATE_CLEANUP' and result['manifest_sha256']==M_SHA
rows=m['candidates'];selected={r['path'] for r in rows}
assert len(rows)==len(selected)==result['removed_count']==22
assert result['removed_paths']==[row['path'] for row in rows]
assert result['removed_allocated_bytes']==m['allocated_bytes']==sum(row['allocated_bytes'] for row in rows)==491978752
assert result['removed_logical_bytes']==m['logical_bytes']==sum(row['size'] for row in rows)==491945768
assert result['scientific_credit'] is False and result['all_other_regular_paths_and_identities_unchanged'] is True
assert result['all_symlinks_and_directory_paths_unchanged'] is True
assert result['result_documents_full_sha_checked_before_and_after']==32452
ledger_pin=fullpin(R/'retirement_ledger.jsonl');ledger=[json.loads(line) for line in (R/'retirement_ledger.jsonl').read_text().splitlines()]
assert len(ledger)==22
for original,actual in zip(rows,ledger):
    assert set(actual)==set(original)|{'removed_at'} and {k:v for k,v in actual.items() if k!='removed_at'}==original
    assert type(actual['removed_at'])in (float,int) and result['started']<=actual['removed_at']<=result['finished']
    assert not os.path.lexists(original['path']),original['path']

before=snapshot();after_fp=fingerprint(before)
reconstructed={**before,'files':dict(before['files'])}
for row in rows:
    rel=str(Path(row['path']).relative_to(ROOT));assert rel not in reconstructed['files'];reconstructed['files'][rel]=row['identity']
reconstructed_fp=fingerprint(reconstructed)
assert reconstructed_fp==pre['untouched_snapshot_sha256']==prior['whole_project_baseline']['fingerprint_before']
assert len(before['files'])+22==173810 and len(before['links'])==687 and len(before['dirs'])==6928
print(json.dumps(dict(phase='all22_absent_exactledger_and_whole_remaining_metadata_proved',reconstructed_preflight_fingerprint=reconstructed_fp,after_fingerprint=after_fp)),flush=True)

prior_records=load(OUT/'independent_preflight_fresh_SHA_records.json')
remaining_records=[record for record in prior_records if record['path'] not in selected]
assert len(prior_records)==34893 and len(remaining_records)==34871
for i,record in enumerate(remaining_records,1):
    fullpin(record['path'],record)
    if i%8000==0:print(json.dumps(dict(phase='independent_all_preserved_full_SHA_read',checked=i,expected=len(remaining_records))),flush=True)
for row in m['retained_primaries']:fullpin(row['path'],row)
for row in m['source_and_review_pins']:fullpin(row['path'],row)
documents=load(R/'result_document_full_sha_baseline.json',m['result_document_baseline_sha256'])
assert documents['count']==len(documents['rows'])==32452 and documents['bytes']==3738511671
assert all(str(ROOT/row['path']) in PINS and PINS[str(ROOT/row['path'])]['sha256']==row['sha256'] for row in documents['rows'])
resource_stats=load(OUT/'independent_228_live_resource_root_path_lstats.json')
assert len(resource_stats)==228
for row in resource_stats:
    s=Path(row['path']).lstat();assert [s.st_dev,s.st_ino,s.st_mode]==[row[k] for k in ('dev','ino','mode')]
    if not stat.S_ISDIR(s.st_mode):assert [s.st_size,s.st_nlink]==[row[k] for k in ('size','nlink')]
end=snapshot();assert end==before and fingerprint(end)==after_fp
for p,record in PINS.items():assert identity(Path(p))==record['identity'],p
assert all(not os.path.lexists(p) for p in selected)

capacity_before=result['before_capacity']['project_allocated_bytes_du'];capacity_after=result['after_capacity']['project_allocated_bytes_du']
assert (capacity_before,capacity_after)==(160753418240,160261513216)
report=dict(schema='SPOT_TENTH_ACTUAL_FIXED_EXACT_DUPLICATE_CLEANUP_INDEPENDENT_REVIEW_V1',status='PASS',manifest_sha256=M_SHA,preflight_sha256=PF_SHA,result_sha256=RESULT_SHA,cleanup_tool_observation_sha256=TOOL_SHA,cleanup_source_sha256=m['cleanup_source_sha256'],prior_independent_preflight_sha256=PRE_REVIEW_SHA,ledger_sha256=ledger_pin['sha256'],actual_root_tool=dict(initial_chunk='7b96af',session_id=25157,completion_chunk='fd61d0',exit_code=0,closed=True,complete_raw_stdout_equals_result_json=True),exact_count=22,all_selected_absent=True,ledger_exact_original22_rows_in_order=True,retained_primaries_count=13,source_and_review_pins_count=2684,all_13_primaries_and_2684_sources_fresh_full_SHA_identity_preserved=True,all32452_original_result_documents_full_SHA_identity_preserved=True,result_document_bytes=3738511671,original_result_seal_logs_sources_not_rewritten=True,current_228_resource_root_paths_inode_and_type_retained=True,current_seven_INPUT_and_V8_failed_source_OUT_TERM_and_cold_graph_kept=True,default_iterative_seed_retained=True,old_restore_sources_and_permanent89_gzip_archives_metadata_preserved=True,full_read_unique_files=len(PINS),full_read_unique_bytes=sum(row['size'] for row in PINS.values()),all_fresh_SHA_records='independent_actual_fresh_SHA_records.json',whole_project_metadata=dict(after_fingerprint_before_review=after_fp,after_fingerprint_after_review=fingerprint(end),reinsert_exact22_original_identity_reconstructs_original_preflight_fingerprint=reconstructed_fp,counts_after={k:len(v) for k,v in before.items()},original_regular_files=173810,exact_regular_files_removed=22,all_other_files_identities_links_and_directory_paths_preserved=True,excludes=['top-level .git','this round report directory'],not_all_project_contents_rehashed=True),capacity_observation=dict(candidate_allocated_bytes=491978752,logical_bytes=491945768,Root_du_before_bytes=capacity_before,Root_du_after_bytes=capacity_after,Root_du_observed_reduction_bytes=capacity_before-capacity_after,Root_du_observed_reduction_GiB=(capacity_before-capacity_after)/1024**3,Root_free_bytes_before=result['before_capacity']['free_bytes'],Root_free_bytes_after=result['after_capacity']['free_bytes'],no_instant_APFS_free_space_promise=True),source_and_scope_previous_review_reused=True,review_elapsed_seconds=time.monotonic()-START,cleanup_restore_or_business_script_invoked=False,files_deleted_by_independent_review=0,formal_ART_written_by_independent_review=False,scientific_or_combined_native_RSS_AAA_ABA_credit=False,limits=['Review performed pure file/JSON metadata hashing and namespace snapshots, not a scientific graph verifier or full35GB numerical INPUT admission.','All32,452 original result documents were independently reread in full again; retained primary/source/meta set also reread. Remaining scientific arrays not in this set were checked by whole project metadata identity, not claimed as full content rehash.','The entire after snapshot plus exact original22 candidate identities reconstructs the pinned preflight fingerprint, proving only those22 paths changed outside the report/.git exclusion. Two after snapshots are identical.','Historical complete manifests/export/whole replay require restoring these exact22 paths from retained primaries first, then separately restoring earlier retired paths if required. Inode/ctime cannot be restored.','Unique final/closed states and material originals remain; ninth89 gzip archive bytes were strictly validated in their original independent audit and their identities remain unchanged here. No compression/restore/deletion was repeated.','Final README/current-progress/report updates may be intentionally written by Root after this PASS and must be separately recorded.'])
save('independent_actual_fresh_SHA_records.json',list(PINS.values()))
save('independent_actual_cleanup_review.json',report)
print(json.dumps(dict(status='PASS',report=str(OUT/'independent_actual_cleanup_review.json'),report_sha256=hashlib.sha256((OUT/'independent_actual_cleanup_review.json').read_bytes()).hexdigest(),result_sha256=RESULT_SHA,ledger_sha256=ledger_pin['sha256'],fresh_files=len(PINS),fresh_bytes=report['full_read_unique_bytes'],whole_baseline=reconstructed_fp,files_deleted_by_review=0)),flush=True)
