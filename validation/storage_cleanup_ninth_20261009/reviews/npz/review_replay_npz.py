import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import time

ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts'
OUT=Path('/private/tmp/spot_ninth_storage_build_cache_independent_review_20261009')
GRAPH=ART/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v8-20261009/input_graph.json'
COLD=Path('/private/tmp/spot_eighth_storage_independent_source_review_20261009/current_cold_dynamic_protected_files.json')
INDEX=ROOT/'validation/storage_review_more_20261008/normalized_protection_index.json'
CRITICAL=ROOT/'validation/storage_cleanup_fifth_20261009/critical_source_scope_scan.json'
FAMILIES={'exact-native-flight-20260929':('verify_exact_native_flight.py','qualify_exact_native_flight.py'),'native-directional-response-20260929':('verify_native_directional.py','qualify_native_directional.py'),'native-source-current-consistency-20260928':('verify_native_source_current.py','audit_native_source_current.py'),'axial-cell-characteristic-20260929':('verify_axial_cell_characteristic.py','qualify_axial_cell_characteristic.py')}
if not __debug__:raise RuntimeError('optimization forbidden')

def identity(p):
    s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def pin(p,wanted=None):
    p=Path(p);before=identity(p);assert stat.S_ISREG(before[2]) and before[6]==1 and not any(a.is_symlink() for a in p.parents)
    h=hashlib.sha256();fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb') as f:
        s=os.fstat(f.fileno());assert [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]==before
        while b:=f.read(4*1024**2):h.update(b)
        s=os.fstat(f.fileno());assert [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]==before
    assert identity(p)==before
    observed=h.hexdigest()
    if wanted:assert observed==wanted,(str(p),wanted,observed)
    return dict(path=str(p),sha256=observed,size_bytes=before[3],allocated_bytes=Path(p).lstat().st_blocks*512,identity=before,stable_full_content_read=True)

def read(p,wanted=None):
    item=pin(p,wanted);return json.loads(Path(p).read_text()),item

def strings(d):
    if isinstance(d,str):yield d
    elif isinstance(d,dict):
        for k,v in d.items():yield from strings(k);yield from strings(v)
    elif isinstance(d,list):
        for v in d:yield from strings(v)

def under(p,r):return p==r or p.startswith(r.rstrip('/')+'/')

def main():
    started=time.monotonic()
    graph,gp=read(GRAPH,'242e995536b1b1cb92a03a16dd7936814f646ea6c02d486c71b6e8e2fb5d9044')
    cold,cp=read(COLD,'11f9f07e92ca6c11ccb90ed4bf58b9d98a0e726bf2893a40e457c32edbc9e161')
    old,op=read(INDEX,'30893b4a333c6dc39df420b136b095e076e0ad2ac6255336b8e3eb26ced49b86')
    critical,crp=read(CRITICAL,'10843bbf7fa7c1eb4dfbc55c089d1044e3112296d6bef5a6219b2e81df643407')
    literal={s for s in strings(graph) if s.startswith('/')};canon={x['path'] for x in graph['canonical_files']}
    ns={x[k] for x in graph['namespaces'] for k in ('root','canonical_root')}
    aliasfiles={x[k] for x in graph['aliases'] for k in ('path','target') if x['kind']=='file'}
    aliasdirs={x[k] for x in graph['aliases'] for k in ('path','target') if x['kind']=='directory'}
    oldfiles=set(old['protected_files']);olddirs=set(old['protected_directories']);oldtargets=set(old['inbound_alias_targets'])
    coldpaths={x['path'] for x in cold['current_cold_dynamic_protected_files']};cr=critical['critical_roots_excluded_wholesale']
    links=[]
    for folder,dirs,files in os.walk(ROOT,followlinks=False):
        for name in dirs+files:
            p=Path(folder)/name
            if p.is_symlink():links.append(dict(path=str(p),text=os.readlink(p),target=str(p.resolve()),is_directory=p.is_dir()))
    protected_primary_paths=set()
    cleanup_manifest_pins=[]
    # Conservative prior retirement ledger path references keep all known restore sources.
    for folder in sorted((ROOT/'validation').glob('storage_cleanup*')):
        p=folder/'manifest.json'
        if p.is_file():
            d,item=read(p);cleanup_manifest_pins.append(item)
            protected_primary_paths|={s for s in strings(d) if s.startswith('/') and os.path.lexists(s)}
    def exclude(p):
        p=str(p)
        return dict(current_graph_literal=p in literal,current_canonical=p in canon,current_namespace=any(under(p,r) for r in ns),current_file_alias=p in aliasfiles,current_directory_alias=any(under(p,r) for r in aliasdirs),current_future_cold_dynamic=p in coldpaths,old_protected_file=p in oldfiles,old_protected_directory=any(under(p,r) for r in olddirs),old_alias_target=p in oldtargets,critical_root=any(under(p,r) for r in cr),project_link=p in {x['target'] for x in links if not x['is_directory']} or any(under(p,x['target']) for x in links if x['is_directory']),prior_cleanup_restore_source=p in protected_primary_paths)
    selected=[];held=[];familyproof=[];sources=[];metadata=[];endpoints=[]
    def source(p,wanted=None):
        sp=pin(p,wanted);text=Path(p).read_text();ast.parse(text)
        relevant=[dict(line=i,text=line) for i,line in enumerate(text.splitlines(),1) if any(v in line for v in ('replay/analysis','analysis_files_byte_identical','byte_identical_analysis_files','np.savez','initial_json_serialization','digest(a/','digest(p)','digest(path)','rglob','result.sha256'))]
        sources.append(dict(**sp,relevant_lines=relevant));return sp
    for family,(verifier,producer) in FAMILIES.items():
        base=ART/family;manifest=pin(base/'result.sha256');metadata.append(manifest)
        signed={}
        for line in (base/'result.sha256').read_text().splitlines():
            digest,path=line.split('  ',1);assert path not in signed;signed[path]=digest
        verification=pin(base/'verification.json',signed['verification.json']);metadata.append(verification);v=json.loads((base/'verification.json').read_text());assert v['all_verification_checks_passed'] is True
        for name in (verifier,producer):
            source(base/'build'/name,signed['build/'+name]);source(ROOT/'validation/iterative'/name,signed['build/'+name])
        count=0;logical=0;previous_absent=[]
        for rel in signed:
            if rel.startswith('replay/analysis/') and rel.endswith('.npz') and not (base/rel).exists():previous_absent.append(rel)
        for replay in sorted((base/'replay/analysis').rglob('*.npz')):
            rel=str(replay.relative_to(base));primaryrel=rel.removeprefix('replay/');primary=base/primaryrel
            assert rel.startswith('replay/analysis/') and 'initial_json_serialization' not in rel and 'analysis_initial' not in rel
            assert signed[rel]==signed[primaryrel],rel
            flags=exclude(replay)
            if any(flags.values()):held.append(dict(path=str(replay),sha256=signed[rel],reason='Protected current/future/old/alias/restore path',protection=flags));continue
            a=pin(replay,signed[rel]);b=pin(primary,signed[primaryrel]);assert a['identity'][:2]!=b['identity'][:2],rel
            count+=1;logical+=a['size_bytes'];endpoints.extend([a,b])
            selected.append(dict(path=str(replay),sha256=a['sha256'],size_bytes=a['size_bytes'],allocated_bytes=a['allocated_bytes'],identity=a['identity'],retained_primary=b,original_result_manifest=manifest,original_manifest_entries={rel:signed[rel],primaryrel:signed[primaryrel]},original_replay_verification=verification,exclusions=flags,restore=dict(source=str(primary),target=str(replay),sha256=a['sha256'],mode=stat.S_IMODE(a['identity'][2]),mtime_ns=a['identity'][4]),old_full_replay_requires_restore_before_verification=True))
        familyproof.append(dict(family=family,selected_count=count,selected_logical_bytes=logical,retained_original_verification=dict(pin=verification,byte_identical_analysis_count=v.get('byte_identical_analysis_files',v.get('analysis_files_byte_identical')),qualification_is_historical_only=True),prior_manifest_replay_NPZ_currently_absent=previous_absent,do_not_claim_old_full_replay_pass_after_retirement=True))
    # Next cold/current actual source family literals are statically absent; do not run those APIs.
    coldsrc=Path('/private/tmp/axmat-last-cprime-trim-cold-v7-input-v5-draft-20261009')
    nextsources=[coldsrc/'prepare_historical_input_owned_specs_physical_last_cprime_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak.py',coldsrc/'cold_component_input_consumer_last_cprime_trim_own_pid_peak.py',ROOT/'validation/axial_material/prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v8.py']
    nextsourceproof=[]
    for p in nextsources:
        sp=pin(p);text=p.read_text();ast.parse(text);matches=[dict(line=n,text=line) for n,line in enumerate(text.splitlines(),1) if any(f in line for f in FAMILIES)]
        assert not matches,str(p);nextsourceproof.append(dict(**sp,candidate_family_literal_matches=matches))
    # Entire current scientific source directory exact replay path references are absent.
    codepins=[];literalhits=[];selectedpaths={x['path'] for x in selected}
    for p in sorted((ROOT/'validation/axial_material').glob('*.py')):
        if not p.is_file() or p.is_symlink():continue
        text=p.read_text()
        matches=[dict(line=n,text=line) for n,line in enumerate(text.splitlines(),1) if any(f in line for f in FAMILIES) or any(x in line for x in selectedpaths)]
        if matches:literalhits.append(dict(path=str(p),matches=matches))
    assert not literalhits,literalhits
    for e in endpoints+metadata+nextsourceproof:assert identity(e['path'])==e['identity'],e['path']
    report=dict(status='PASS_EXACT_OLD_REPLAY_NPZ_WORK_COPY_SUBSET',source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),graph=gp,current_cold_dynamic=cp,old_index=op,critical_scope=crp,project_symlink_count=len(links),prior_cleanup_manifest_pins=cleanup_manifest_pins,selected_count=len(selected),logical_bytes=sum(x['size_bytes'] for x in selected),allocated_bytes=sum(x['allocated_bytes'] for x in selected),selected=selected,held=held,families=familyproof,original_producer_and_verifier_source_pins=sources,next_current_cold_and_V8_source_static_pins=nextsourceproof,current_axial_source_directory_family_or_exact_path_literal_hits=literalhits,preservation='All primary analysis NPZ and native layered/full-oblique inputs remain; all original result.sha256, verification, raw runs, initial_json_serialization/analysis_initial, sources, docs and logs remain. Only named exact replay/analysis NPZ with both original signed SHA entries and fresh full matching content are proposed.',path_dependency_boundary='Original family full replay and transitive prior-manifest verifiers still need these precise replay paths; retired copies must be restored from the unchanged primary before those legacy workflows. Current V8 graph/full typed symbols/aliases/namespaces, cold6194 direct dynamic protected map and next source literals exclude this subset. No legacy gate is relabeled or modified.',limits=['No science/API/import/constructor/PREP/RUN or large scientific verification executed. SHA equality is byte-level, not fresh scientific qualification.','Static absence checks do not prove arbitrary unbounded external future programs cannot access historical replay paths. They cover the explicitly frozen next cold/V8 source, full stored graph and current known dynamic protection.','Previously absent signed replay NPZ are recorded without inventing a new original replay success.'],files_deleted=0,formal_or_ART_write=False,business_API_executed=False,elapsed_seconds=time.monotonic()-started)
    path=OUT/'exact_replay_npz_source_proof.json'
    with path.open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(status=report['status'],path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),selected_count=len(selected),logical_bytes=report['logical_bytes'],allocated_bytes=report['allocated_bytes'],held=len(held),family_summary=[{k:x[k] for k in ('family','selected_count','selected_logical_bytes')} for x in familyproof],elapsed_seconds=report['elapsed_seconds'])))

if __name__=='__main__':main()
