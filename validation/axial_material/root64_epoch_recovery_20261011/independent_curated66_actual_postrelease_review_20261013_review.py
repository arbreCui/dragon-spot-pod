import os, stat, json, hashlib, shutil
from pathlib import Path
from collections import Counter

R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
P=R/'storage_release_curated66_old_private_copies_source_v3_20261013'
A=R/'storage_release_curated66_old_private_copies_actual_receipts_20261013/ACTUAL_EXACT_CURATED66_OLD_PRIVATE_RELEASE_RECEIPT.json'
O=R/'independent_curated66_actual_postrelease_review_20261013'
checks=[]; EOF={}
def identity(s): return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(p): return {k:p[k] for k in ('path','sha256','size_bytes','identity')}
def check(ok,name):
    if not ok: raise AssertionError(name)
    checks.append(name)
def pin(path):
    path=Path(path); before=identity(path.lstat())
    check(stat.S_ISREG(before[2]), 'regular '+str(path))
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb') as f:
        if identity(os.fstat(f.fileno()))!=before: raise AssertionError('open7 '+str(path))
        digest=hashlib.file_digest(f,'sha256').hexdigest()
        if identity(os.fstat(f.fileno()))!=before: raise AssertionError('EOF7 '+str(path))
    if identity(path.lstat())!=before: raise AssertionError('after7 '+str(path))
    p=dict(path=str(path),sha256=digest,size_bytes=before[4],identity=before);EOF[str(path)]=p;return p
def same(p):
    p=norm(p); actual=EOF.get(p['path']) or pin(p['path'])
    if actual!=p: raise AssertionError('fullPF '+p['path'])
def read(path):
    p=pin(path);data=json.loads(Path(path).read_bytes())
    if identity(Path(path).lstat())!=p['identity']: raise AssertionError('json after7')
    return data,p
def inventory(roots):
    files={};dirs={};links={}
    stack=list(map(Path,roots))
    while stack:
        d=stack.pop();ds=identity(d.lstat());dirs[str(d)]=ds
        fd=os.open(d,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:
            with os.scandir(fd) as entries:
                for e in entries:
                    s=e.stat(follow_symlinks=False);p=d/e.name
                    if stat.S_ISDIR(s.st_mode): stack.append(p)
                    elif stat.S_ISREG(s.st_mode): files[str(p)]=identity(s)
                    elif stat.S_ISLNK(s.st_mode): links[str(p)]=os.readlink(p)
                    else: raise AssertionError('unsupported inventory')
        finally: os.close(fd)
    return dict(ordinary_file_identities=files,directory_identities=dirs,symlinks=links)

m,mp=read(P/'EXACT_CURATED66_OLD_PRIVATE_RELEASE_MANIFEST.json')
a,ap=read(A)
check(ap['sha256']=='114d2fd0f13c1af1396823cbba0c4b693130361092ed83ad4ecb6ca2849aadda' and ap['size_bytes']==436781,'actual release receipt exact SHA/bytes')
check(mp['sha256']=='938c685869b5fd6e9e0e8579be66c8de9eb1a45bae9afb3695a3e3eb57db014f' and mp['size_bytes']==6559455,'actual manifest exact SHA/bytes')
check(norm(a['manifest_pin'])==mp,'receipt selects exact actual MF')
check(a['schema']=='ACTUAL_EXACT_CURATED66_OLD_PRIVATE_RELEASE_RECEIPT_V1' and a['status']=='EXACT_CURATED66_OLD_PRIVATE_RELEASE_ALL_RETAINED_FULL_EOF_VERIFIED','actual release closed successful schema/status')
check(a['execute_requested'] is True and a['compiler_or_business_executed'] is False and a['next_target_intent'] is None,'release only no business and no pending intent')
sf,sp=read(m['selected_Source_freeze_pin']['path']);same(m['selected_Source_freeze_pin'])
for p in m['Source_pins']:same(p)
target={p['path']:norm(p) for p in m['target_full_EOF_pins']}
protected={p['path']:norm(p) for p in m['current_protected_full_EOF_pins']}
retained={p['path']:norm(p) for p in m['retained_all_other12_old_files_full_EOF_pins']}
check(len(target)==66 and len(protected)==7030 and len(retained)==2123,'literal66 / protected7030 / retained2123')
check(set(target).isdisjoint(protected) and set(target).isdisjoint(retained),'historical targets not active protected')
check(a['deleted_files']==66 and a['logical_bytes_released']==sum(p['size_bytes'] for p in target.values())==1751559764,'actual exact66 and byte sum')
check(len(a['deletion_records'])==66 and [norm(x['original_fullpin']) for x in a['deletion_records']]==list(target.values()),'all actual unlink records literal order PF exact')
parents=Counter(str(Path(p).parent)for p in target)
chain={}
for row in a['deletion_records']:
    name=row['original_fullpin']['path']; parent=str(Path(name).parent);before=row['parent_before_seven_id'];after=row['parent_after_seven_id']
    if row['actual_unlink_returned'] is not True or row['confirmed_absent'] is not True:raise AssertionError('real return absent')
    if before[:3]!=after[:3] or after[3]!=before[3]-1 or after[4]!=before[4]-32:raise AssertionError('each APFS parent -1/-32')
    if parent in chain and chain[parent]!=before:raise AssertionError('parent chain')
    chain[parent]=after
    if Path(name).exists() or Path(name).is_symlink():raise AssertionError('target still exists')
check(True,'each real unlink return and immediate parent chain -1/-32; all66 absent')
check(len(a['affected_parent_changes'])==len(parents)==24,'24 affected parent rows exact')
affected={}
for row in a['affected_parent_changes']:
    name=row['path'];before=row['before'];after=row['after'];n=parents[name]
    if row['removed_children']!=n or row['nlink_delta']!=-n or row['size_delta']!=-32*n or before[:3]!=after[:3] or after[3]!=before[3]-n or after[4]!=before[4]-32*n or chain[name]!=after or identity(Path(name).lstat())!=after:raise AssertionError('aggregate parent delta/current7')
    affected[name]=after
check(True,'every affected parent actual7 and aggregate -n/-32n')
for p in protected.values():same(p)
for p in retained.values():same(p)
check(True,'all7030 protected and2123 retained full EOF SHA all7 unchanged')
oldroots=[x['root'] for x in m['actual_closed_failed12_owner_proofs']]
old=inventory(oldroots);before=m['complete_before_inventory']
expect={p:i for p,i in before['ordinary_file_identities'].items()if p not in target}
check(old['ordinary_file_identities']==expect and set(expect)==set(retained),'old12 actual inventory exactly subtract literal66')
check(old['symlinks']==before['symlinks'],'old12 complete symlinks unchanged')
check(old['directory_identities']=={p:affected.get(p,i)for p,i in before['directory_identities'].items()},'old12 all284 dirs7 exact expected24 changes')
dag=m['Source_DAG_provenance']
for key in ('current_v14_complete_inventory','current_v12_complete_inventory'):
    inv=dag[key]; roots=[p for p in inv['directory_identities']if not any(str(Path(p).parent)==q for q in inv['directory_identities'])]
    check(inventory(roots)==inv,key+' complete files/dirs/symlinks unchanged')
check(len(dag['only30_literal_target_rows_migrated'])==30 and set(dag['only30_literal_target_rows_migrated']).issubset(target) and dag['remaining5595_exact_rows_retained'] is True,'only historical30 migration retains5595 active')
hf,hp=read(sf['additional_newSource_build_HF_pin']['path']);same(sf['additional_newSource_build_HF_pin'])
check(len(hf['dependencies'])==2532 and all(norm(x)==protected.get(x['path'])for x in hf['dependencies']),'new buildHF exact2532 active dependencies all protected')
same(sf['additional_compact_Fortran_Source_freeze_pin']);csf,cp=read(sf['additional_compact_Fortran_Source_freeze_pin']['path'])
check(csf['compiled'] is False and csf['numerical_executed'] is False,'candidate Source qualification remains false')
for p in csf['files']+csf['original_source_pins']:same(p)
check(a['all_latest_v14_v12_v3PACK_old_ax_current_other_science_Source_logs_retained'] is True and a['only_old_private_exact_path_replay_lost'] is True,'receipt exact retained science scope')
b=a['original_budget_before'];after=a['original_budget_after']
check(b['artifact_bytes']-after['artifact_bytes']==1751559764 and b['regular_files']-after['regular_files']==66,'actual family before-after exact66/bytes')
for budget in (b,after):
    check((budget['min_free_bytes'],budget['artifact_budget_bytes'],budget['original_cold_reserve_bytes'],budget['metadata_reserve_bytes'],budget['initial_fresh_reserve_bytes'])==(8*2**30,96*2**30,20971764748,64*2**20,2*2**30),'original budget all caps unchanged')
    remain=budget['artifact_budget_bytes']-budget['artifact_bytes']-budget['original_cold_reserve_bytes']-budget['metadata_reserve_bytes']-budget['initial_fresh_reserve_bytes']
    check(remain==budget['remaining_after_original_initial_reserves_bytes'] and budget['original_initial_reserve_admitted']==(remain>0),'receipt original reserve arithmetic')
art=Path('/Users/wen/spot/validation/artifacts')
dynamic={str(p)for p in art.iterdir()if p.name.startswith('axial-material')and p.is_dir()and not p.is_symlink()}
roots=sorted(set(after['declared_resource_roots'])|dynamic)
check(roots==after['resource_roots']==b['resource_roots'],'dynamic axial family original roots exact709')
total=0;count=0;stack=list(map(Path,roots))
while stack:
    d=stack.pop()
    try: fd=os.open(d,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    except FileNotFoundError: continue
    try:
        with os.scandir(fd)as entries:
            for e in entries:
                s=e.stat(follow_symlinks=False)
                if stat.S_ISDIR(s.st_mode):stack.append(d/e.name)
                elif stat.S_ISREG(s.st_mode):total+=s.st_size;count+=1
    finally:os.close(fd)
check((total,count)==(after['artifact_bytes'],after['regular_files']),'independent original family current actual bytes/files equal receipt after')
free=shutil.disk_usage(art).free;remaining=96*2**30-total-20971764748-64*2**20-2*2**30
check(free>=8*2**30 and remaining==176591187 and remaining>0 and after['original_initial_reserve_admitted'] is True,'independent true current free/reserve positive176591187')
for p in EOF.values():
    if identity(Path(p['path']).lstat())!=p['identity']:raise AssertionError('all read final7 '+p['path'])
check(True,'all read FDs closed and final7 identities stable')
report=dict(schema='INDEPENDENT_CURATED66_ACTUAL_POSTRELEASE_READONLY_REVIEW_V1',status='PASS_ACTUAL_EXACT66_POSTRELEASE_READONLY',failure=None,manifest_pin=mp,actual_release_receipt_pin=ap,Source_freeze_pin=sp,source_only=False,readonly=True,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed_by_this_reviewer=False,actual_target_absent_count=66,actual_deleted_bytes=1751559764,actual_protected_EOF_count=7030,actual_retained_old12_EOF_count=2123,actual_current_family_bytes=total,actual_current_family_regular_files=count,actual_current_disk_free_bytes=free,actual_original_reserve_remaining_bytes=remaining,all_file_descriptors_closed=True,checks=checks,checked_full_EOF_pins=list(EOF.values()))
O.mkdir()
out=O/'REVIEW.json';out.write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
rp=pin(out)
print(json.dumps(dict(status=report['status'],failure=None,review_pin=rp,actual_protected_EOF_count=7030,actual_original_reserve_remaining_bytes=remaining,all_file_descriptors_closed=True),ensure_ascii=False))
