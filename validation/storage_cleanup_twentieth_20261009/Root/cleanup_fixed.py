from pathlib import Path
import sys, os, stat, json, gzip, hashlib, subprocess, shutil

ROOT = Path('/Users/wen/spot')
TMP = Path('/private/tmp/spot_storage_twentieth_root_20261009')
DEST = ROOT/'validation/storage_cleanup_twentieth_20261009'
PLAN = TMP/'fixed_delete_plan.json'

def identity(path):
    s = path.lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()

def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()

def save(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def inventory(excluded):
    files={}; links={}; directories={}
    for base,dirs,names in os.walk(ROOT,followlinks=False):
        bp=Path(base)
        if bp==ROOT: dirs[:]=[n for n in dirs if n!='.git']
        dirs[:]=[n for n in dirs if bp/n != DEST]
        s=bp.lstat();directories[str(bp.relative_to(ROOT))]=[s.st_dev,s.st_ino,s.st_mode]
        for n in names+[n for n in dirs if (bp/n).is_symlink()]:
            p=bp/n
            if str(p) in excluded:continue
            s=p.lstat(); rel=str(p.relative_to(ROOT))
            if stat.S_ISLNK(s.st_mode):links[rel]={'identity':identity(p),'text':os.readlink(p),'resolved':str(p.resolve())}
            elif stat.S_ISREG(s.st_mode):files[rel]=identity(p)
            else:raise AssertionError(('unsupported file type',str(p)))
    result={'regular_files':dict(sorted(files.items())),'symlinks':dict(sorted(links.items())),
            'directories':dict(sorted(directories.items()))}
    result['fingerprint_sha256']=hashlib.sha256(canonical(result)).hexdigest()
    return result

def critical_docs():
    paths=set((ROOT/'validation/iterative').glob('*.md'))
    paths|={ROOT/'README.md',ROOT/'HISTORY.md',
            ROOT/'validation/axial_material/last_cprime_trim_build_review_20261008/current_progress.json',
            ROOT/'validation/axial_material/last_cprime_trim_combined_live_resource_v9_build_review_20261009/REPORT.txt',
            ROOT/'validation/storage_cleanup_nineteenth_20261009/REPORT.txt',
            ROOT/'validation/storage_review_eighteenth_20261009/REPORT.txt'}
    build=ROOT/'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009'
    paths.add(build/'input_graph.json')
    for i,day in enumerate(('20260925','20260926','20260926','20260927','20260927'),1):
        d=ROOT/'validation/artifacts'/f'd4a-scattering-mesh12-picard-map{i}-{day}'
        paths|={d/'result.sha256',d/'input_manifest.sha256',d/'output_manifest.sha256'}
    return {str(p):{'identity':identity(p),'sha256':digest(p)} for p in sorted(paths)}

def du_kib():
    return int(subprocess.check_output(['du','-sk',str(ROOT)],text=True).split()[0])

def execute():
    plan=json.loads(PLAN.read_bytes());assert plan['status']=='READY_EXACT_30_ROOT_DELETE_WITH_RESULTS_AND_CURRENT_INPUTS_PRESERVED'
    rows=plan['candidates'];assert len(rows)==30 and len({x['path'] for x in rows})==30
    assert not DEST.exists(),str(DEST)
    for review in plan['independent_review_pins']:
        assert digest(Path(review['path']))==review['sha256']
    for row in rows:
        p=Path(row['path']);assert p.is_relative_to(ROOT/'validation/artifacts')
        assert p.name in ('projected_proposal.xsm','candidate_radial.xsm','candidate_snapshots.xsm','candidate_axial.xsm','candidate_system.xsm','parent_for_checker.xsm')
        assert identity(p)==row['identity'] and stat.S_ISREG(row['identity'][2]) and row['identity'][6]==1
        assert digest(p)==row['sha256']
    selected={x['path'] for x in rows}
    before=inventory(selected);docs=critical_docs();size_before=du_kib()
    for rel,row in before['symlinks'].items():assert row['resolved'] not in selected
    save(TMP/'critical_docs_before.json',docs)
    (TMP/'protected_before.json.gz').write_bytes(gzip.compress(canonical(before),compresslevel=6,mtime=0))
    archives=json.loads((TMP/'lossless_archive_manifest.json').read_bytes())
    assert archives['status']=='ALL_30_FULL_GZIP_INVERSE_MATCH_ORIGINAL_FULL_MANIFEST_BYTES'
    assert len(archives['archives'])==30 and {x['original_path'] for x in archives['archives']}==selected
    assert plan['lossless_archive_manifest_sha256']==digest(TMP/'lossless_archive_manifest.json')
    archive_allocated=0
    for row in archives['archives']:
        source=Path(row['temporary_archive_path']);saved=DEST/row['saved_archive_relative_path']
        assert source.stat().st_size==row['gzip_size_bytes'] and digest(source)==row['gzip_sha256']
        saved.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,saved)
        assert saved.stat().st_size==row['gzip_size_bytes'] and digest(saved)==row['gzip_sha256']
        h=hashlib.sha256();n=0
        with gzip.open(saved,'rb') as f:
            for b in iter(lambda:f.read(1024*1024),b''):h.update(b);n+=len(b)
        assert n==row['raw_size_bytes'] and h.hexdigest()==row['raw_sha256']
        archive_allocated+=saved.stat().st_blocks*512
    save(DEST/'Root/lossless_archive_manifest.json',archives)
    shutil.copyfile(TMP/'restore_archived_intermediates.py',DEST/'restore_archived_intermediates.py')
    deleted=[]
    for row in rows:
        p=Path(row['path']);assert identity(p)==row['identity']
        p.unlink();deleted.append({'path':str(p),'original_identity':row['identity'],'original_sha256':row['sha256'],'allocated_bytes':row['allocated_bytes']})
        save(TMP/'actual_deletion_ledger.json',{'schema':'SPOT_R20_EXACT_ROOT_DELETE_LEDGER_V1','deleted_count':len(deleted),'deleted':deleted})
    after=inventory(set());assert before==after
    assert critical_docs()==docs
    assert all(not os.path.lexists(x['path']) for x in rows)
    size_after=du_kib()
    (TMP/'protected_after.json.gz').write_bytes(gzip.compress(canonical(after),compresslevel=6,mtime=0))
    result={'schema':'SPOT_R20_ROOT_ACTUAL_30_INTERMEDIATE_DELETE_POSTCHECK_V1','status':'COMPLETE_EXACT_30_WITH_UNCHANGED_PROTECTED_PROJECT_AND_DOCUMENTS',
            'deleted_count':len(deleted),'deleted_allocated_bytes':sum(x['allocated_bytes'] for x in rows),
            'deleted_logical_bytes':sum(x['size_bytes'] for x in rows),
            'du_before_kib':size_before,'du_after_operation_kib':size_after,
            'du_before_gib':size_before/1024**2,'du_after_operation_gib':size_after/1024**2,
            'protected_regular_files':len(before['regular_files']),'protected_symlinks':len(before['symlinks']),
            'protected_directories':len(before['directories']),'protected_fingerprint_sha256':before['fingerprint_sha256'],
            'protected_before_after_exact':True,'full_sha_documents_and_manifests_unchanged':len(docs),
            'no_directory_or_symlink_deleted':True,'all_closed_states_bootstrap_and_maps6_to9_kept':True,
            'git_excluded_from_protection_and_unmodified_by_cleanup':True,
            'science_business_executed':False,'science_input_code_threshold_progress_modified':False,
            'lossless_archives_count':len(archives['archives']),
            'lossless_archive_raw_bytes':archives['raw_bytes'],
            'lossless_archive_gzip_bytes':archives['gzip_bytes'],
            'lossless_archive_allocated_bytes':archive_allocated,
            'lossless_inverse_verified_after_saved_project_copy':True,
            'old_early_stage_full_manifest_requires_restoration_from_archives':True,
            'recomputation_not_required_for_archived_original_content':True}
    save(TMP/'cleanup_result.json',result)
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':
    assert sys.argv[1:]==['execute']
    execute()
