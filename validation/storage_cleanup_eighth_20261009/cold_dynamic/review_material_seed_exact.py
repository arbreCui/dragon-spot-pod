import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import time

ROOT = Path('/Users/wen/spot')
ART = ROOT/'validation/artifacts'
OUT = Path('/private/tmp/spot_eighth_storage_independent_source_review_20261009')
EXACT = Path('/private/tmp/spot_eighth_storage_readonly_scan_20261009/exact_content_groups.json')
GRAPH = ART/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v7-20261009/input_graph.json'
INDEX = ROOT/'validation/storage_review_more_20261008/normalized_protection_index.json'
CRITICAL = ROOT/'validation/storage_cleanup_fifth_20261009/critical_source_scope_scan.json'
TOOLS = ROOT/'validation/axial_material'
if not __debug__:
    raise RuntimeError('optimization must be disabled')

def identity(p):
    s = Path(p).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def pin(p, expected=None):
    p=Path(p)
    before=identity(p)
    assert stat.S_ISREG(before[2]) and before[6]==1, str(p)
    assert not any(a.is_symlink() for a in p.parents), str(p)
    h=hashlib.sha256()
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb') as stream:
        fs=os.fstat(stream.fileno())
        assert [fs.st_dev,fs.st_ino,fs.st_mode,fs.st_size,fs.st_mtime_ns,fs.st_ctime_ns,fs.st_nlink]==before
        while block:=stream.read(4*1024**2):h.update(block)
        fs=os.fstat(stream.fileno())
        assert [fs.st_dev,fs.st_ino,fs.st_mode,fs.st_size,fs.st_mtime_ns,fs.st_ctime_ns,fs.st_nlink]==before
    assert identity(p)==before
    digest=h.hexdigest()
    if expected is not None:assert digest==expected,str(p)
    return dict(path=str(p),sha256=digest,size=before[3],identity=before,stable_full_content_read=True)

def read_json(p,expected=None):
    item=pin(p,expected)
    return json.loads(Path(p).read_text()),item

def strings(d):
    if isinstance(d,str):yield d
    elif isinstance(d,dict):
        for k,v in d.items():yield from strings(k);yield from strings(v)
    elif isinstance(d,list):
        for v in d:yield from strings(v)

def under(p,root):return p==root or p.startswith(root.rstrip('/')+'/')

def main():
    started=time.monotonic()
    exact,exactpin=read_json(EXACT,'e88304048fb5c9c38b72a641891881a9ae352bfe41c6e91d00b6a8ddd2ddd564')
    graph,graphpin=read_json(GRAPH,'9103f35a3f121972969270162be56babe72143869b050f5220af6f3eb0715e68')
    old,oldpin=read_json(INDEX,'30893b4a333c6dc39df420b136b095e076e0ad2ac6255336b8e3eb26ced49b86')
    critical,criticalpin=read_json(CRITICAL,'10843bbf7fa7c1eb4dfbc55c089d1044e3112296d6bef5a6219b2e81df643407')
    absolute_strings={s for s in strings(graph) if s.startswith('/')}
    canonical={r['path'] for r in graph['canonical_files']}
    nsroots={r[k] for r in graph['namespaces'] for k in ('root','canonical_root')}
    aliasfiles={r[k] for r in graph['aliases'] for k in ('path','target') if r['kind']=='file'}
    aliasdirs={r[k] for r in graph['aliases'] for k in ('path','target') if r['kind']=='directory'}
    oldfiles=set(old['protected_files'])
    olddirs=set(old['protected_directories'])
    oldtargets=set(old['inbound_alias_targets'])
    crit=critical['critical_roots_excluded_wholesale']
    links=[]
    for base,dirs,files in os.walk(ROOT,followlinks=False):
        for name in dirs+files:
            p=Path(base)/name
            if p.is_symlink():links.append(dict(path=str(p),text=os.readlink(p),target=str(p.resolve()),target_is_directory=p.is_dir()))
    primary_paths={
        '/A/material.xsm':ART/'axial-material-inputs-20261003/A/material.xsm',
        '/B/material.xsm':ART/'axial-material-inputs-20261003/B/material.xsm',
        '/A/seed_A.xsm':ART/'axial-material-inputs-20261003/A/snapshot_A.xsm',
        '/B/seed_B.xsm':ART/'axial-material-inputs-20261003/B/snapshot_B.xsm'}
    selected=[];holds=[];archives=[]
    manifests={};sourcepins={};primaries={};runtimepins={}
    def cached_pin(cache,p,expected=None):
        name=str(p)
        if name not in cache:cache[name]=pin(p,expected)
        if expected is not None:assert cache[name]['sha256']==expected,name
        return cache[name]
    for group in exact['groups']:
        for row in group['rows']:
            p=row['path'];tail=next((k for k in primary_paths if p.endswith(k)),None)
            if tail is None:
                if '/archives/' in p and p.endswith('snapshots.xsm'):
                    archives.append(dict(path=p,sha256=group['sha256'],size=group['size'],decision='HOLD_THIS_ROUND',reason='Archive consumer and complete sealed-stage proof deliberately outside exact materials/seed subset; protected/aliased production archives are never candidates.',screen_protected=row['protected'],inbound_link=row['inbound_link']))
                continue
            if p==str(primary_paths[tail]):continue
            exclusions=dict(current_graph_absolute_literal=p in absolute_strings,current_canonical=p in canonical,current_namespace=any(under(p,s) for s in nsroots),current_file_alias=p in aliasfiles,current_directory_alias=any(under(p,s) for s in aliasdirs),old_file=p in oldfiles,old_directory=any(under(p,s) for s in olddirs),old_alias_target=any(p==s or Path(s).is_dir() and under(p,s) for s in oldtargets),critical_scope=any(under(p,s) for s in crit),inbound_link=any(p==s['target'] or s['target_is_directory'] and under(p,s['target']) for s in links))
            assert not row['protected'] and not row['inbound_link'],p
            assert not any(exclusions.values()),(p,exclusions)
            manifest=Path(p).parent.parent/'execution.json'
            if not manifest.exists():
                holds.append(dict(path=p,sha256=group['sha256'],size=group['size'],decision='HOLD',reason='Rejected preparation has no original execution.json binding for this exact path. Do not turn fresh duplicate equality into a historical signed receipt.',exclusions=exclusions))
                continue
            md=json.loads(manifest.read_text());wanted=md['files'].get(p)
            assert wanted==group['sha256'],p
            mp=cached_pin(manifests,manifest)
            primary=cached_pin(primaries,primary_paths[tail],wanted)
            value=pin(p,wanted)
            assert value['identity']==row['identity'],p
            assert value['identity'][:2]!=primary['identity'][:2],p
            originals=[]
            for source,want in md['files'].items():
                if source.startswith(str(TOOLS)+'/') and source.endswith('.py'):
                    sp=cached_pin(sourcepins,Path(source),want)
                    text=Path(source).read_text();ast.parse(text)
                    originals.append(dict(path=source,sha256=sp['sha256'],original_execution_sha256=want,copy_related_excerpt=[dict(line=n,text=line) for n,line in enumerate(text.splitlines(),1) if any(s in line for s in ('shutil.copy','material.xsm','seed_A.xsm','snapshot_A.xsm','snapshot_B.xsm','seed_B.xsm','manifest[\'files\']','original[\'files\']'))][:35]))
            deck=Path(p).parent/'snapshot.x2m'
            local_consumers=[]
            if deck.exists() and str(deck) in md['files']:
                dp=cached_pin(runtimepins,deck,md['files'][str(deck)])
                lines=[dict(line=n,text=line) for n,line in enumerate(deck.read_text().splitlines(),1) if any(s in line for s in ('material.xsm','seed_A.xsm','seed_B.xsm'))]
                local_consumers.append(dict(path=str(deck),sha256=dp['sha256'],literal_local_reads=lines))
            selected.append(dict(path=p,sha256=wanted,size=row['size'],allocated_bytes=row['allocated_bytes'],identity=value['identity'],retained_primary=primary,original_manifest=dict(path=str(manifest),sha256=mp['sha256'],field='files['+p+']',expected_sha256=wanted),exclusions=exclusions,pinned_historical_sources=originals,pinned_local_decks=local_consumers,restore=dict(source=primary['path'],target=p,sha256=wanted,mode=stat.S_IMODE(value['identity'][2]),mtime_ns=value['identity'][4]),old_full_validation_requires_exact_restore=True))
    # Original primary material and snapshot pins are documented in preserved scientific manifests.
    primary_metadata=[]
    for letter in 'AB':
        audit=ART/'axial-material-inputs-20261003'/letter/'material_audit.json';d,ap=read_json(audit)
        material=str(primary_paths['/'+letter+'/material.xsm'])
        assert d['source_sha256'][material]==primaries[material]['sha256'];primary_metadata.append(ap)
    results,rp=read_json(ART/'axial-material-inputs-20261003/material_results.json');primary_metadata.append(rp)
    for letter in 'AB':
        snapshot=str(primary_paths['/'+letter+'/seed_'+letter+'.xsm'])
        assert results['states'][letter]['archive_sha256']==primaries[snapshot]['sha256']
    # Static actual current/original admission semantics: no import or execution.
    gate_sources=[]
    for name in ('qualified_snapshot_ingestion.py','prepare_qualified_AB_production.py','prepare_qualified_AB_production_v2.py','verify_r64_snapshot_diagnostics.py','verify_residual_diagnostics.py','production_runner.py'):
        p=TOOLS/name;sp=cached_pin(sourcepins,p)
        text=p.read_text();ast.parse(text)
        gate_sources.append(dict(path=str(p),sha256=sp['sha256'],relevant_lines=[dict(line=n,text=line) for n,line in enumerate(text.splitlines(),1) if any(s in line for s in ('verify_offline_state','manifest[\'files\']','verify_prepared','verify_sealed_directory','training_snapshots.xsm','aba_snapshots.xsm','aaa_snapshots.xsm','axial-material-r64-system-normalization','axial-material-r64-snapshot-B-dependencyfix'))]))
    # Static bounded source inventory; include all family literal references from the source directory.
    families={Path(s['path']).parent.parent.name for s in selected}
    refs=[]
    for p in sorted(TOOLS.glob('*.py')):
        if not p.is_file() or p.is_symlink():continue
        text=p.read_text()
        matches=[dict(line=n,text=line) for n,line in enumerate(text.splitlines(),1) if any(f in line for f in families)]
        if matches:
            sp=cached_pin(sourcepins,p);refs.append(dict(path=str(p),sha256=sp['sha256'],matches=matches))
    # Recheck all pinned endpoints after complete screening.
    for cache in (primaries,manifests,sourcepins,runtimepins):
        for item in cache.values():assert identity(item['path'])==item['identity'],item['path']
    for s in selected:assert identity(s['path'])==s['identity'],s['path']
    report=dict(status='PASS_EXACT_RESTORABLE_MATERIAL_AND_INITIAL_SEED_SUBSET_ONLY',scope='Read-only independent exact old work-copy review; no deletion or scientific execution.',source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),exact_scan_report=exactpin,graph=graphpin,old_protection_index=oldpin,critical_scope_index=criticalpin,current_graph_counts=dict(canonical_files=len(canonical),namespaces=len(graph['namespaces']),aliases=len(graph['aliases']),live_resource_roots=len(graph['live_resource_roots']),absolute_strings=len(absolute_strings)),project_symlink_count=len(links),selected_count=len(selected),selected_logical_bytes=sum(s['size'] for s in selected),selected_allocated_bytes=sum(s['allocated_bytes'] for s in selected),selected=selected,holds=holds,archive_holds=archives,retained_primary_pins=list(primaries.values()),retained_primary_metadata_pins=primary_metadata,original_manifest_pins=list(manifests.values()),historical_source_pins=list(sourcepins.values()),local_deck_pins=list(runtimepins.values()),actual_original_gate_source_evidence=gate_sources,static_source_family_references=refs,path_dependency_boundary='Current V7 full stored graph has no selected physical path in any string field, canonical list, requirement symbol, namespace or alias scope. Original verify_offline_state and legacy diagnostics/preparation still full-read historical inherited execution.files and local material/seed deck paths; these original workflows require exact restoration first. Their original receipts/manifests stay immutable and are not credited with a fresh pass after retirement.',preserved_scope='Original inputs A/B material, original snapshots and DLIB; final qualified A/B snapshots/tracks/runtime/audits/receipts; every closed state, unique scientific output, source, result, manifest, document and log. Selection is only explicit material.xsm and initial seed files with full exact source copies.',limitations=['Static path inventory does not execute arbitrary dynamic source paths. Whole input APIs and all scientific solvers were intentionally not run.','The proposed restore map guarantees file content; original inode/ctime cannot be reproduced by copying. No old admission semantics are weakened or reinterpreted.','Unsealed rejected-preparation files and all archive snapshots are HOLD this round. No unique scientific bytes are identified as disposable.'],files_deleted=0,scientific_API_imported=False,PREP_or_RUN_executed=False,formal_or_artifact_writes=False,elapsed_seconds=time.monotonic()-started)
    path=OUT/'independent_material_seed_exact_candidates.json'
    with path.open('x') as stream:json.dump(report,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps(dict(status=report['status'],path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),selected_count=len(selected),logical_bytes=report['selected_logical_bytes'],allocated_bytes=report['selected_allocated_bytes'],holds=len(holds),archive_holds=len(archives),symlinks=len(links),elapsed_seconds=report['elapsed_seconds'])))

if __name__=='__main__':main()
