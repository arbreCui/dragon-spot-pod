"""Metadata/source-protection screen only; no deletion or business modules."""
import collections
import hashlib
import json
import os
import stat
from pathlib import Path

ROOT=Path('/Users/wen/spot');OUT=Path('/private/tmp/spot_storage_tenth_exact_dependency_review_20261009')
PINS={}
def load(p,expected=None):
    p=Path(p);s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink];assert stat.S_ISREG(s.st_mode)
    raw=p.read_bytes();s=p.lstat();assert before==[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
    sha=hashlib.sha256(raw).hexdigest()
    if expected:assert sha==expected
    PINS[str(p)]=dict(path=str(p),sha256=sha,size=len(raw),identity=before)
    return json.loads(raw)
inventory=load('/private/tmp/spot_storage_tenth_root_audit_20261009/fresh_inventory.json')
m9=load(ROOT/'validation/storage_cleanup_ninth_20261009/manifest.json','e4b9c50d79ae6370cd62bb90ed4f2896b6e010438139c52af920672ccad8b4f8')
oldindex=load(m9['old_index_pin']['path'],m9['old_index_pin']['sha256'])
graph=load(m9['graph_pin']['path'],m9['graph_pin']['sha256'])
restore=load(ROOT/'validation/storage_cleanup_ninth_20261009/reviews/prior_restore_cross_176/all_9124_existing_old_restoration_sources_fresh_stat_canonical_paths.json')
exact8=load(ROOT/'validation/storage_cleanup_eighth_20261009/inventory/exact_content_groups.json','e88304048fb5c9c38b72a641891881a9ae352bfe41c6e91d00b6a8ddd2ddd564')
exact_paths={};prefixes={};allgraphstrings=set()
def protect(path,reason):
    if type(path) is str and path.startswith('/'):
        exact_paths.setdefault(path,set()).add(reason)
        if '#' in path:exact_paths.setdefault(path.split('#',1)[0],set()).add(reason+' OWNER_PREFIX')
def prefix(path,reason):
    if type(path) is str and path.startswith('/'):prefixes.setdefault(path.rstrip('/'),set()).add(reason)
for p in oldindex['protected_files']:protect(p,'OLD_PROTECTION_INDEX')
for p in oldindex['protected_directories']:prefix(p,'OLD_PROTECTED_DIRECTORY')
for p in oldindex['inbound_alias_targets']:protect(p,'OLD_LINK_TARGET')
for p in graph['canonical_files']:protect(p['path'],'CURRENT_V8_CANONICAL_FILE')
for n in graph['namespaces']:prefix(n['canonical_root'],'CURRENT_V8_EXHAUSTIVE_NAMESPACE')
for a in graph['aliases']:
    if a['kind']=='directory':
        prefix(a['path'],'CURRENT_V8_DIRECTORY_ALIAS_PATH');prefix(a['target'],'CURRENT_V8_DIRECTORY_ALIAS_TARGET')
    else:protect(a['path'],'CURRENT_V8_FILE_ALIAS_PATH');protect(a['target'],'CURRENT_V8_FILE_ALIAS_TARGET')
def strings(value):
    if isinstance(value,dict):
        for k,v in value.items():
            if isinstance(k,str):yield k
            yield from strings(v)
    elif isinstance(value,list):
        for v in value:yield from strings(v)
    elif isinstance(value,str):yield value
for s in strings(graph):
    if s.startswith('/') and not '\n' in s:protect(s,'CURRENT_V8_ALL_ABSOLUTE_STRINGS')
for p in m9['critical_roots']:prefix(p,'CRITICAL_ROOT')
for p in m9['current_cold_extra_protected_files']:protect(p,'CURRENT_FUTURE_COLD_DYNAMIC')
for p in restore:protect(p['path'],'ROUND1_TO8_RESTORE_SOURCE')
for k in ('retained_primaries','source_and_review_pins'):
    for p in m9[k]:protect(p['path'],'ROUND9_'+k.upper())
prefix(str(ROOT/'validation/storage_cleanup_ninth_20261009/packed_material_intermediates'),'PERMANENT_ROUND9_LOSSLESS_GZIP_ARCHIVE')
rules=[]
for name in ('storage_cleanup_20261008','storage_cleanup_more_20261008','storage_cleanup_third_20261008','storage_cleanup_fourth_20261008','storage_cleanup_fifth_20261009','storage_cleanup_sixth_20261009','storage_cleanup_seventh_20261009','storage_cleanup_eighth_20261009','storage_cleanup_ninth_20261009'):
    p=ROOT/'validation'/name/'REPORT.txt';s=p.lstat();raw=p.read_bytes();assert s.st_mtime_ns==p.lstat().st_mtime_ns
    rules.append(dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size=len(raw)))
    # Every explicit restoration primary/evidence in original manifests remains protected.
    mp=p.parent/'manifest.json'
    if mp.exists():
        manifest=load(mp)
        for k in ('retained_primaries','retained_tapes','source_and_review_pins','source_metadata_pins'):
            if k in manifest:
                for s in strings(manifest[k]):protect(s,'PRIOR_ROUND_EXPLICIT_RETAINED_OR_SOURCE_'+name)
linkrows=[]
for base,dirs,files in os.walk(ROOT,followlinks=False):
    dirs[:]=[d for d in dirs if d not in ('.git','.aws','.codex','.agents')]
    for name in list(dirs)+files:
        p=Path(base)/name
        if p.is_symlink():
            target=str(p.resolve(strict=False));text=os.readlink(p)
            linkrows.append(dict(path=str(p),text=text,target=target,is_directory_target=p.is_dir()))
            if p.is_dir():prefix(target,'FRESH_PROJECT_DIRECTORY_LINK_TARGET');prefix(str(p),'FRESH_PROJECT_DIRECTORY_LINK_PATH')
            else:protect(target,'FRESH_PROJECT_LINK_TARGET');protect(str(p),'FRESH_PROJECT_LINK_PATH')
def reasons(path):
    why=set(exact_paths.get(path,set()))
    for root,rs in prefixes.items():
        if path==root or path.startswith(root+'/'):why.update(rs)
    return sorted(why)
rows=[];sizegroups=collections.defaultdict(list)
for record in inventory['rows']:
    if not record['path'].startswith('validation/artifacts/') or record['size']<=8*1024**2:continue
    path=str(ROOT/record['path']);s=Path(path).lstat()
    assert [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]==[record['dev'],record['ino'],record['mode'],record['size'],record['mtime_ns'],record['ctime_ns'],record['nlink']]
    row=dict(path=path,size=record['size'],allocated_bytes=record['allocated'],identity=[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink],protection_reasons=reasons(path))
    if s.st_nlink!=1:row['protection_reasons'].append('MULTIPLE_HARDLINKS')
    rows.append(row);sizegroups[row['size']].append(row)
by_path={r['path']:r for r in rows}
remaining_old_groups=[]
for group in exact8['groups']:
    live=[by_path[r['path']] for r in group['rows'] if r['path'] in by_path]
    if len(live)>1 and any(not r['protection_reasons'] for r in live):
        remaining_old_groups.append(dict(prior_exact_sha256=group['sha256'],size=group['size'],rows=live,prior_eighth_group_not_new_full_hash=True))
report=dict(schema='SPOT_TENTH_LARGE_DUPLICATE_METADATA_PROTECTION_SCREEN_V1',status='METADATA_SCREEN_ONLY_NOT_DELETE_APPROVAL',large_artifact_files=len(rows),logical_bytes=sum(r['size'] for r in rows),allocated_unique_inode_bytes=sum({(r['identity'][0],r['identity'][1]):r['allocated_bytes'] for r in rows}.values()),fully_unprotected_files=sum(not r['protection_reasons'] for r in rows),potential_equal_size_groups=[dict(size=size,rows=group) for size,group in sorted(sizegroups.items(),reverse=True) if len(group)>1 and any(not r['protection_reasons'] for r in group)],remaining_prior_exact_groups=remaining_old_groups,protection_counts=dict(exact_paths=len(exact_paths),directory_prefixes=len(prefixes),fresh_project_symlinks=len(linkrows),current_canon=len(graph['canonical_files']),current_namespaces=len(graph['namespaces']),current_aliases=len(graph['aliases']),critical_roots=len(m9['critical_roots']),cold_extra=len(m9['current_cold_extra_protected_files']),round1_to8_restore_source_records=len(restore)),rules_read=rules,source_metadata_pins=PINS,no_business_API_or_import_or_PREP_RUN=True,files_deleted=0,formal_ART_written=False)
for name,value in [('metadata_screen.json',report),('large_file_rows.json',rows),('fresh_symlink_inventory.json',linkrows)]:
    with (OUT/name).open('x') as f:json.dump(value,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps(dict(status=report['status'],large_files=len(rows),unprotected=report['fully_unprotected_files'],size_groups=len(report['potential_equal_size_groups']),remaining_old_exact_groups=len(remaining_old_groups),source_pins=len(PINS),fresh_project_symlinks=len(linkrows))))
for group in remaining_old_groups[:25]:print(json.dumps(dict(size=group['size'],sha=group['prior_exact_sha256'],rows=[dict(path=r['path'],protected=r['protection_reasons'][:3]) for r in group['rows']]),separators=(',',':')))
