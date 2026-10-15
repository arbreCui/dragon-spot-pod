import collections
import hashlib
import json
import os
from pathlib import Path
import stat
import time

ROOT=Path('/Users/wen/spot')
OUT=Path('/private/tmp/spot_ninth_storage_build_cache_independent_review_20261009')
if not __debug__:raise RuntimeError('optimization forbidden')

def identity(p):
    s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def pin(row):
    p=Path(row['path']);before=identity(p);assert before==row['identity'] and stat.S_ISREG(before[2]) and not any(a.is_symlink() for a in p.parents)
    h=hashlib.sha256();fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb') as f:
        while b:=f.read(4*1024**2):h.update(b)
    assert identity(p)==before
    return dict(**row,sha256=h.hexdigest(),stable_full_content_read=True)

def main():
    started=time.monotonic();meta=json.loads((OUT/'build_cache_metadata_screen.json').read_text())
    prior=ROOT/'validation/storage_cleanup_sixth_20261009/duplicate_library_source_review.json';raw=prior.read_bytes();proof=json.loads(raw)
    preserve={r['path'] for r in proof['retained_original_result_source_log_parameter_command_and_unique_executable_pins']+proof['explicitly_preserved_signed_host_libraries']+proof['retained_primary_libraries']}
    metadata_paths=[]
    for row in meta['all_build_cache_file_metadata']:
        if row['kind'] in ('.o','.a','.dylib','.mod','.smod','executable_binary'):
            metadata_paths.append(row)
    hashed=[];by_hash=collections.defaultdict(list)
    for row in metadata_paths:
        value=pin(row)
        hold=dict(primary_non_ART=not value['path'].startswith(str(ROOT/'validation/artifacts')+'/'),prior_explicit_unique_evidence_or_signed_library=value['path'] in preserve,future_cold_SciPy=value['family']=='axial-material-cold-cp314-scipy-dependency-20261008',original_known_protection=value['protected'])
        value['additional_hold_flags']=hold;value['available_for_future_source_proof']=not any(hold.values())
        hashed.append(value);by_hash[value['sha256']].append(value)
    exact=[];potential=[]
    for h,rows in by_hash.items():
        if len(rows)<2:continue
        eligible=[r for r in rows if r['available_for_future_source_proof']]
        if not eligible:continue
        keep=next((r for r in rows if not r['available_for_future_source_proof']),rows[0])
        candidates=[r for r in eligible if r['path']!=keep['path'] and r['identity'][6]==1 and r['identity'][:2]!=keep['identity'][:2]]
        if not candidates:continue
        exact.append(dict(sha256=h,size=rows[0]['size'],retained_peer=keep['path'],candidate_paths=[r['path'] for r in candidates],all_peers=[r['path'] for r in rows],allocated_candidate_bytes=sum(r['allocated_bytes'] for r in candidates),decision='HOLD_PENDING_ORIGINAL_SEAL_AND_COMPLETE_DYNAMIC_SOURCE_PROOF'))
        potential.extend(candidates)
    categories=collections.defaultdict(lambda:dict(count=0,allocated_bytes=0))
    for r in potential:categories[r['kind']]['count']+=1;categories[r['kind']]['allocated_bytes']+=r['allocated_bytes']
    for row in hashed:assert identity(row['path'])==row['identity'],row['path']
    report=dict(status='PASS_READ_ONLY_COMPILED_EXACT_CONTENT_SCREEN_NO_DELETE_APPROVAL',source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),metadata_report_sha256=hashlib.sha256((OUT/'build_cache_metadata_screen.json').read_bytes()).hexdigest(),prior_explicit_preservation_source=dict(path=str(prior),sha256=hashlib.sha256(raw).hexdigest(),explicit_preserve_path_count=len(preserve)),full_read_count=len(hashed),full_read_bytes=sum(r['size'] for r in hashed),exact_groups=exact,potential_exact_copy_count=len(potential),potential_exact_copy_allocated_bytes=sum(r['allocated_bytes'] for r in potential),potential_classes=dict(categories),all_fresh_compiled_hash_records=hashed,approved_compiled_deletion_paths=[],preserved_scope='All unique executable evidence and signed original host libraries, current/future V8/cold/graph/index/namespace/alias/critical bytes, restore sources and primary project build files remain. A same SHA peer here is a screen, not final source/path proof.',git=dict(allocated_bytes=445710336,decision='KEEP',reason='Git objects/history supply exact source baselines and recovery; no disposable cache proof. Never remove pack or object files manually.'),node_modules=dict(directories_found=0,decision='NO_CANDIDATES_FOUND'),ordinary_cache=dict(total_allocated_bytes=8122368,unprotected_allocated_bytes=7344128,decision='LOW_RETURN_ONLY_SEPARATE_EXACT_FILE_CHECK',reason='About 7MiB is not material storage pressure. Namespace or receipt-listed cache files remain protected; no wildcard directory retirement is approved.'),cp314_SciPy=dict(decision='KEEP_ENTIRE_FAMILY',reason='Frozen intended next cold factory explicitly binds SCIPY_DEPENDENCY_ROOT and adds target to PYTHONPATH; its .so/.dylib are not merely old caches even when V8 input graph does not name every installed file.'),archives=dict(existing_generic_archive_count=sum(1 for r in meta['all_build_cache_file_metadata'] if r['kind'].startswith('archive')),decision='NONE_CURRENTLY_FOUND_IN_THIS_SUFFIX_SCAN',reason='Prior tar exact inverse retirement recipe and all canonical payloads stay preserved; no new unique/archive bytes may be inferred disposable from name.'),files_deleted=0,formal_or_ART_write=False,scientific_API_imported=False,PREP_or_RUN_executed=False,elapsed_seconds=time.monotonic()-started)
    target=OUT/'compiled_exact_screen_and_holds.json'
    with target.open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(status=report['status'],path=str(target),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),full_read_count=len(hashed),full_read_bytes=report['full_read_bytes'],potential_exact_copy_count=len(potential),potential_exact_allocated_bytes=report['potential_exact_copy_allocated_bytes'],potential_classes=dict(categories),approved_compiled_deletion_count=0,elapsed_seconds=report['elapsed_seconds'])))

if __name__=='__main__':main()
