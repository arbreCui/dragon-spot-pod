"""Retire the exact 30 reviewed duplicate paths; keep every primary and document."""
import argparse, hashlib, json, stat, time
from pathlib import Path
from exact_retire_utils import ROOT, OUT, identity, digest, save, inventory, capacity, symlink_check

GRAPH=ROOT/'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v6-20261008/input_graph.json'
GRAPH_SHA='8563867dd30b3c50ccaa71b744d3cba81fce9d84fc74945fc8ab1d75182a6711'
OLD_INDEX=ROOT/'validation/storage_review_more_20261008/normalized_protection_index.json'
INDEX_SHA='30893b4a333c6dc39df420b136b095e076e0ad2ac6255336b8e3eb26ced49b86'
SOURCE_PINS={'duplicate_snapshot_source_review.json':'cd13e5c995d25e8754ff3957ac9f421535ae942a3207d35fb1fcd667e095d7f2','duplicate_library_source_review.json':'d4dd266fad432d0c008eb8b8aae6a4e42931355375af2c3d97c322267d5826b0','critical_source_supplement.json':'dd018492a5d5b77cd77fdf7c9ea8124541ab588e627f134e00e8efafa4028325','critical_source_scope_scan.json':'10843bbf7fa7c1eb4dfbc55c089d1044e3112296d6bef5a6219b2e81df643407'}

def absolute_strings(v):
    if isinstance(v,str):
        return {v} if v.startswith('/') else set()
    if isinstance(v,list):
        return set().union(*(absolute_strings(x) for x in v))
    if isinstance(v,dict):
        return set().union(*(absolute_strings(x) for x in [*v.keys(),*v.values()]))
    return set()

def original_entry(p, ref):
    record=Path(ref['record']); found=[]
    for line in record.read_text().splitlines():
        parts=line.split(maxsplit=1)
        if len(parts)==2 and (record.parent/parts[1].lstrip('*')).resolve()==p:
            found.append(parts[0])
    if not found or set(found)!={ref['expected_sha256']}:
        raise ValueError(f'original manifest does not bind {p}')
    return digest(record)

def plan():
    source=[]
    for name,sha in SOURCE_PINS.items():
        pin=digest(OUT/name)
        if pin['sha256']!=sha: raise ValueError('review source changed')
        source.append(pin)
    if digest(GRAPH)['sha256']!=GRAPH_SHA or digest(OLD_INDEX)['sha256']!=INDEX_SHA:
        raise ValueError('current closure metadata changed')
    g=json.loads(GRAPH.read_text()); old=json.loads(OLD_INDEX.read_text())
    exact=absolute_strings(g)|set(old['protected_files'])|set(old['inbound_alias_targets'])
    directories={n['canonical_root'] for n in g['namespaces']}|set(old['protected_directories'])
    directories|={a[k] for a in g['aliases'] if a['kind']=='dir' for k in ('path','target')}
    supplement=json.loads((OUT/'critical_source_supplement.json').read_text()); libs=json.loads((OUT/'duplicate_library_source_review.json').read_text())
    if supplement['selected_count']!=22 or libs['candidate_count']!=8: raise ValueError('wrong reviewed counts')
    rows=[]; metadata={}; kept={}
    for r in supplement['selected_candidates']:
        a,b=r['candidate'],r['primary']; p=Path(a['path']); q=Path(b['path'])
        for ref in a['original_sha256_pins']+b['original_sha256_pins']:
            owner=p if ref in a['original_sha256_pins'] else q
            z=original_entry(owner,ref); metadata[z['path']]=z
        for x in (a,b):
            for ref in x['directory_manifest_records']:
                z=digest(Path(ref['path']))
                if z['sha256']!=ref['sha256']: raise ValueError('original result metadata changed')
                metadata[z['path']]=z
        if any(r['candidate_actual_full_content'][k]!=a[k] for k in ('path','size_bytes','allocated_bytes','device','inode','mtime_ns','ctime_ns','nlink')):
            raise ValueError('candidate author evidence mismatch')
        rows.append({'path':str(p),'retained_primary':str(q),'expected_sha256':r['expected_sha256'],'expected_bytes':a['size_bytes'],'allocated_bytes':a['allocated_bytes'],'identity':identity(p),'category':r['category']})
        for x,path in ((a,p),(b,q)):
            i=identity(path)
            if [i[0],i[1],i[3],i[4],i[5],i[6]]!=[x[k] for k in ('device','inode','size_bytes','mtime_ns','ctime_ns','nlink')]: raise ValueError('candidate or primary changed')
        kept[str(q)]={'path':str(q),'identity':identity(q),'sha256':r['expected_sha256'],'bytes':b['size_bytes']}
    for r in libs['candidates']:
        a,b=r['candidate'],r['retained_primary']; p=Path(a['path']);q=Path(b['path'])
        for x,path in ((a,p),(b,q)):
            i=identity(path)
            if [i[0],i[1],i[2],i[3],i[4],i[6]]!=[x[k] for k in ('device','inode','mode','bytes','mtime_ns','nlink')]: raise ValueError('library identity changed')
        if a['sha256']!=b['sha256'] or a['bytes']!=b['bytes']: raise ValueError('not duplicate libraries')
        rows.append({'path':str(p),'retained_primary':str(q),'expected_sha256':a['sha256'],'expected_bytes':a['bytes'],'allocated_bytes':a['allocated_bytes'],'identity':identity(p),'category':r['rationale']})
        kept[str(q)]={'path':str(q),'identity':identity(q),'sha256':b['sha256'],'bytes':b['bytes']}
    for r in libs['retained_evidence_and_unique_executables']:
        z=digest(Path(r['path']))
        if z['sha256']!=r['sha256']: raise ValueError('retained build evidence changed')
        metadata[z['path']]=z
    for ref in supplement['preserved_track_original_manifest_pins']+supplement['three_probe_source_pins_and_replay_cost']+[supplement['three_snapshot_origin_record'],supplement['three_probe_result_manifest_pin']]:
        z=digest(Path(ref['path']))
        if z['sha256']!=ref['sha256']: raise ValueError('critical source evidence changed')
        metadata[z['path']]=z
    held=supplement['held_23rd_candidate']; h=held['candidate']; kept[h['path']]={'path':h['path'],'identity':identity(Path(h['path'])),'sha256':held['expected_sha256'],'bytes':h['size_bytes']}
    for ref in supplement['preserved_track_full_content_proofs']:
        p=Path(ref['path']);kept[str(p)]={'path':str(p),'identity':identity(p),'sha256':ref['sha256'],'bytes':ref['size_bytes']}
    selected={r['path'] for r in rows}
    if len(rows)!=30 or len(selected)!=30 or selected&set(kept): raise ValueError('wrong exact selection')
    for r in rows:
        p=Path(r['path']);i=identity(p)
        if not p.is_relative_to(ROOT/'validation/artifacts') or p.resolve()!=p or not stat.S_ISREG(i[2]) or i[6]!=1: raise ValueError('not independent ordinary artifact')
        if p.suffix not in ('.xsm','.bin','.a') or str(p) in exact or any(p.is_relative_to(Path(d)) for d in directories): raise ValueError('current closure or document conflict')
        if i!=r['identity'] or i[3]!=r['expected_bytes'] or p.stat().st_blocks*512!=r['allocated_bytes']: raise ValueError('selection changed')
    save('manifest.json',{'schema':'SPOT_FIFTH_EXACT_DUPLICATE_RETIREMENT_V1','status':'ROOT_PLAN_NOT_DELETED','candidates':rows,'retained_primaries_and_critical_sources':list(kept.values()),'source_metadata_pins':list(metadata.values()),'review_pins':source,'graph_pin':digest(GRAPH),'old_index_pin':digest(OLD_INDEX),'latest_graph_screen':{'canonical_files':len(g['canonical_files']),'namespaces':len(g['namespaces']),'aliases':len(g['aliases']),'all_selected_intersections':0,'API_executed':False},'symlink_check':symlink_check(selected),'selected_count':30,'logical_bytes':sum(r['expected_bytes'] for r in rows),'allocated_bytes':sum(r['allocated_bytes'] for r in rows),'all_documents_logs_sources_primary_results_retained':True,'old_duplicate_paths_require_restore_for_full_replay':True,'files_deleted':0})
    print(json.dumps({'status':'EXACT_30_PLANNED','allocated_bytes':sum(r['allocated_bytes'] for r in rows)}))

def preflight():
    m=json.loads((OUT/'manifest.json').read_text());selected={r['path'] for r in m['candidates']}; before=inventory(selected)
    for z in m['review_pins']+m['source_metadata_pins']+[m['graph_pin'],m['old_index_pin']]:
        if digest(Path(z['path']))!=z: raise ValueError('review or dependency metadata changed')
    if symlink_check(selected)!=m['symlink_check']: raise ValueError('project links changed')
    candidates=[];kept=[]
    for r in m['candidates']:
        z=digest(Path(r['path']))
        if z['identity']!=r['identity'] or z['sha256']!=r['expected_sha256'] or z['bytes']!=r['expected_bytes']: raise ValueError('fresh candidate bytes mismatch')
        candidates.append(z)
    for r in m['retained_primaries_and_critical_sources']:
        z=digest(Path(r['path']))
        if z!=r: raise ValueError('fresh retained primary mismatch')
        kept.append(z)
    if inventory(selected)!=before: raise ValueError('nonselected identity changed during read')
    save('preflight.json',{'schema':'SPOT_FIFTH_ROOT_FRESH_CONTENT_PREFLIGHT_V1','status':'PASS','manifest_sha256':digest(OUT/'manifest.json')['sha256'],'verified_candidates':candidates,'verified_kept':kept,'preservation_baseline':before,'capacity_before':capacity(),'files_deleted':0,'solver_or_API_executed':False})
    print(json.dumps({'status':'PREFLIGHT_PASS','manifest_sha256':digest(OUT/'manifest.json')['sha256'],'preflight_sha256':digest(OUT/'preflight.json')['sha256'],'candidate_count':len(candidates),'kept_count':len(kept)}))

def apply(msha,psha,rsha):
    start=time.monotonic()
    if digest(OUT/'manifest.json')['sha256']!=msha or digest(OUT/'preflight.json')['sha256']!=psha or digest(OUT/'independent_preflight_review.json')['sha256']!=rsha: raise ValueError('Root-observed pins required')
    m=json.loads((OUT/'manifest.json').read_text());p=json.loads((OUT/'preflight.json').read_text());review=json.loads((OUT/'independent_preflight_review.json').read_text())
    if review['status']!='PASS' or review['manifest_sha256']!=msha or review['preflight_sha256']!=psha: raise ValueError('independent preflight review required')
    selected={r['path'] for r in m['candidates']}
    if len(selected)!=30 or p['status']!='PASS' or p['manifest_sha256']!=msha or [r['path'] for r in p['verified_candidates']]!=[r['path'] for r in m['candidates']]: raise ValueError('preflight selection mismatch')
    if inventory(selected)!=p['preservation_baseline'] or symlink_check(selected)!=m['symlink_check']: raise ValueError('preservation or links changed')
    for z in p['verified_candidates']+p['verified_kept']+m['source_metadata_pins']+m['review_pins']+[m['graph_pin'],m['old_index_pin']]:
        if identity(Path(z['path']))!=z['identity']: raise ValueError('checked file changed')
    with (OUT/'retirement_ledger.jsonl').open('x') as ledger:
        for z in p['verified_candidates']:
            q=Path(z['path'])
            if identity(q)!=z['identity']: raise ValueError('candidate changed before unlink')
            q.unlink(); ledger.write(json.dumps(dict(**z,deleted=True))+'\n');ledger.flush()
    after=inventory(selected)
    if after!=p['preservation_baseline'] or any(Path(x).exists() or Path(x).is_symlink() for x in selected): raise ValueError('unexpected preservation or deletion result')
    save('cleanup_result.json',{'schema':'SPOT_FIFTH_ACTUAL_EXACT_DUPLICATE_RETIREMENT_V1','status':'PASS','deleted_files':30,'deleted_logical_bytes':m['logical_bytes'],'deleted_allocated_bytes':m['allocated_bytes'],'capacity_before':p['capacity_before'],'capacity_after':capacity(),'nonselected_before':p['preservation_baseline'],'nonselected_after':after,'symlink_check_after':symlink_check(selected),'solver_or_API_executed':False,'new_scientific_credit':False,'elapsed_seconds':time.monotonic()-start})
    print(json.dumps({'status':'CLEANUP_PASS','deleted_files':30,'deleted_allocated_bytes':m['allocated_bytes'],'nonselected_fingerprint':after}))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['plan','preflight','apply']);parser.add_argument('--manifest-sha');parser.add_argument('--preflight-sha');parser.add_argument('--review-sha');a=parser.parse_args()
    if a.action=='plan': plan()
    elif a.action=='preflight': preflight()
    else: apply(a.manifest_sha,a.preflight_sha,a.review_sha)
