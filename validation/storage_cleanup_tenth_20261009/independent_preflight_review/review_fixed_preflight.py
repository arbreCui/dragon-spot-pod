"""Read-only independent audit. Does not invoke cleanup/restore/business scripts."""
import ast
import collections
import hashlib
import json
import os
import re
import stat
import time
from pathlib import Path

ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
R=ROOT/'validation/storage_cleanup_tenth_20261009'
OUT=Path('/private/tmp/spot_storage_tenth_result_preservation_readonly_review_20261009')
M_SHA='b1d2b4b2b2a0e12b8926f0f6d6f488db2ed22b637d1984eaf57770efdeb3913b'
PF_SHA='a8eb7d19aef6e45a4d932c452efcb59803eb4d4b90f169a5f00523f7b3c1484b'
SOURCE_SHA='7b593bf7b195219dab6fe04cc6d2247f699205276985c3698c96759bf7774d9b'
DOC_SHA='796db4235dcb38da89470758da23f1690182a86e59f81e7222626156baf2e452'
TERMINAL_SHA='1ab02e8b2f25c6e1dd77c16527e67febbaca57e411048f8acf3902c37ac51ca1'
PINS={};START=time.monotonic()

def identity(p):
    s=p.lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def fullpin(p,expected=None):
    p=Path(p);before=identity(p)
    assert p.is_absolute() and '..' not in p.parts and p.parent.resolve(strict=True)==p.parent and stat.S_ISREG(before[2])
    if isinstance(expected,dict):
        assert before==expected['identity'] and before[3]==expected['size'],str(p)
        if 'allocated_bytes' in expected:assert p.lstat().st_blocks*512==expected['allocated_bytes'],str(p)
    h=hashlib.sha256();length=0
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
        s=os.fstat(f.fileno());assert [s.st_dev,s.st_ino]==before[:2]
        while block:=f.read(1024**2):h.update(block);length+=len(block)
    assert identity(p)==before and length==before[3]
    digest=h.hexdigest()
    if expected is not None:assert digest==(expected['sha256'] if isinstance(expected,dict) else expected),(str(p),digest)
    record=dict(path=str(p),identity=before,size=length,sha256=digest)
    if str(p) in PINS:assert PINS[str(p)]==record,str(p)
    PINS[str(p)]=record
    return record

def load(p,expected=None):
    record=fullpin(p,expected);data=Path(p).read_bytes();assert hashlib.sha256(data).hexdigest()==record['sha256'] and identity(Path(p))==record['identity']
    return json.loads(data)

def save(name,value):
    with (OUT/name).open('xb') as f:
        f.write((json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode());f.flush();os.fsync(f.fileno())

def allstrings(value):
    if type(value) is dict:
        for k,v in value.items():
            if type(k)is str:yield k
            yield from allstrings(v)
    elif type(value)is list:
        for v in value:yield from allstrings(v)
    elif type(value)is str:yield value

def snapshot():
    files={};links={};dirs=[]
    for current,sub,names in os.walk(ROOT,followlinks=False):
        base=Path(current)
        if base==ROOT:sub[:]=[s for s in sub if s!='.git']
        sub[:]=[s for s in sub if base/s!=R]
        dirs.append(str(base.relative_to(ROOT)))
        for name in sub+names:
            p=base/name;s=p.lstat();rel=str(p.relative_to(ROOT))
            ident=[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
            if stat.S_ISLNK(s.st_mode):links[rel]=[ident,os.readlink(p)]
            elif stat.S_ISREG(s.st_mode):files[rel]=ident
    result={'files':files,'links':links,'dirs':sorted(dirs)}
    return result,hashlib.sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest()

m=load(R/'manifest.json',M_SHA);pre=load(R/'preflight.json',PF_SHA)
terminal=load(R/'preflight_terminal_observation.json',TERMINAL_SHA)
assert terminal['initial_tool']==dict(chunk_id='b06636',session_id=91021,exit_code=None)
assert terminal['completion_tool']==dict(chunk_id='6091f8',exit_code=0,session_id=None) and terminal['closed'] is True and terminal['deleted'] is False
assert terminal['manifest_sha256']==M_SHA and terminal['source_sha256']==SOURCE_SHA and terminal['preflight_json_sha256']==PF_SHA
assert pre['status']=='PASS_FIXED_FULL_SHA_PREFLIGHT' and pre['manifest_sha256']==M_SHA and pre['executed'] is False
assert pre['candidates']==m['exact_count']==len(m['candidates'])==22
assert m['cleanup_source_sha256']==SOURCE_SHA and m['result_document_baseline_sha256']==DOC_SHA
assert m['scientific_credit'] is False and m['old_replay_requires_exact_path_restoration'] is True
assert not (R/'retirement_ledger.jsonl').exists() and not (R/'cleanup_result.json').exists()
source=fullpin(R/'cleanup_fixed_duplicates.py',SOURCE_SHA)
tree=ast.parse((R/'cleanup_fixed_duplicates.py').read_bytes());compile(tree,str(R/'cleanup_fixed_duplicates.py'),'exec')
assert [n.lineno for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='unlink']==[122]
assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('rmdir','rmtree') for n in ast.walk(tree))
restore_pin=fullpin(R/'restore_retired_work_copies.py');compile(ast.parse((R/'restore_retired_work_copies.py').read_bytes()),str(R/'restore_retired_work_copies.py'),'exec')

candidates=m['candidates'];selected={r['path'] for r in candidates};primaries={r['path']:r for r in m['retained_primaries']}
assert len(selected)==22 and len(primaries)==13 and not selected.intersection(primaries)
assert sum(r['size'] for r in candidates)==m['logical_bytes']==491945768
assert sum(r['allocated_bytes'] for r in candidates)==m['allocated_bytes']==491978752
assert len({tuple(r['identity'][:2]) for r in candidates})==22
assert collections.Counter(r['work_copy_class'] for r in candidates)==dict(OLD_ITERATIVE_INITIAL_AXIAL_WORK_COPY=10,OLD_PORTABLE_PARENT_AXIAL_WORK_COPY=12)
assert str(ART/'iterative-seed/initial_axial_macrolib.xsm') not in selected
before,before_digest=snapshot();assert before_digest==pre['untouched_snapshot_sha256']
before_counts={k:len(v) for k,v in before.items()}
print(json.dumps(dict(phase='independent_baseline_matches_Root',fingerprint=before_digest,counts=before_counts)),flush=True)

scope=load(R/'candidate_review/metadata_screen.json')
scope_sources=scope['source_metadata_pins']
for p,record in scope_sources.items():fullpin(p,record)
m9_path=ROOT/'validation/storage_cleanup_ninth_20261009/manifest.json';m9=load(m9_path,scope_sources[str(m9_path)])
graph=load(m9['graph_pin']['path'],m9['graph_pin']['sha256'])
old=load(m9['old_index_pin']['path'],m9['old_index_pin']['sha256'])
restore_source_path=ROOT/'validation/storage_cleanup_ninth_20261009/reviews/prior_restore_cross_176/all_9124_existing_old_restoration_sources_fresh_stat_canonical_paths.json'
restore_sources=load(restore_source_path,scope_sources[str(restore_source_path)])
assert len(restore_sources)==9124
exact=set();prefixes=set()
def protect(p):
    if type(p)is str and p.startswith('/') and '\n' not in p:
        exact.add(p)
        if '#' in p:exact.add(p.split('#',1)[0])
def prefix(p):
    if type(p)is str and p.startswith('/'):prefixes.add(p.rstrip('/'))
for p in old['protected_files']:protect(p)
for p in old['protected_directories']:prefix(p)
for p in old['inbound_alias_targets']:protect(p)
for row in graph['canonical_files']:protect(row['path'])
for row in graph['namespaces']:prefix(row['canonical_root'])
for row in graph['aliases']:
    if row['kind']=='directory':prefix(row['path']);prefix(row['target'])
    else:protect(row['path']);protect(row['target'])
for s in allstrings(graph):protect(s)
for p in m9['critical_roots']:prefix(p)
for p in m9['current_cold_extra_protected_files']:protect(p)
for row in restore_sources:protect(row['path'])
for k in ('retained_primaries','source_and_review_pins'):
    for row in m9[k]:protect(row['path'])
prefix(str(ROOT/'validation/storage_cleanup_ninth_20261009/packed_material_intermediates'))
prior_scopes=sorted((ROOT/'validation').glob('storage_cleanup*/manifest.json'))
prior_scopes=[p for p in prior_scopes if p.parent!=R]+[ROOT/'validation/storage_review_20261008/first_batch_24_files.json',ROOT/'validation/storage_review_20261008/second_batch_replay_arrays.json',ROOT/'validation/storage_review_more_20261008/exact_retirement_manifest.json']
assert len(prior_scopes)==10
prior_retired=set()
for p in prior_scopes:
    pm=load(p)
    if type(pm)is dict:
        for k,v in pm.items():
            if any(token in k.lower() for token in ('retained','source_pins','source_and_review_pins','source_metadata_pins')):
                for s in allstrings(v):protect(s)
        for k in ('candidates','files','retired_files'):
            if k in pm and type(pm[k])is list:
                for row in pm[k]:
                    if type(row)is dict:
                        pth=row.get('path') or row.get('candidate')
                        if type(pth)is str:prior_retired.add(pth if pth.startswith('/') else str(ROOT/pth))
    elif type(pm)is list:
        for row in pm:
            if type(row)is dict and type(row.get('path'))is str:prior_retired.add(row['path'])
assert not selected.intersection(prior_retired)
graph_counts=dict(canonical_files=len(graph['canonical_files']),namespaces=len(graph['namespaces']),aliases=len(graph['aliases']),resources=len(graph['resource_entries'])) if 'resource_entries' in graph else dict(canonical_files=len(graph['canonical_files']),namespaces=len(graph['namespaces']),aliases=len(graph['aliases']),resources=scope['protection_counts'].get('resources',228))
assert (graph_counts['canonical_files'],graph_counts['namespaces'],graph_counts['aliases'])==(35647,86,186)
resource_roots=[]
for key in ('resources','resource_entries'):
    for row in graph.get(key,[]):
        for fld in ('canonical_root','root','path'):
            if type(row)is dict and type(row.get(fld))is str and row[fld].startswith('/'):
                p=Path(row[fld]);assert p.exists();resource_roots.append(str(p))
graph_counts['resource_root_paths_still_present']=len(set(resource_roots))
del graph
link_records=[]
for rel,[ident,text] in before['links'].items():
    p=ROOT/rel;target=p.resolve(strict=False)
    link_records.append(dict(path=str(p),target=str(target),text=text,identity=ident))
    if p.is_dir():prefix(str(p));prefix(str(target))
    else:protect(str(p));protect(str(target))
for p in selected:
    assert p not in exact,(p,'direct protected path')
    assert not any(p==d or p.startswith(d+'/') for d in prefixes),(p,'protected directory/alias')
    assert not any(p==row['target'] or p.startswith(row['target']+'/') for row in link_records),(p,'symbolic inbound')

for row in candidates:
    p=Path(row['path']);assert p.is_relative_to(ART) and p.suffix=='.xsm' and row['category']=='EXACT_DUPLICATE_OLD_WORK_COPY' and row['identity'][6]==1
    assert row['retained_primary'] in primaries and row['static_current_protection_reasons']==[]
    fullpin(p,row);primary=primaries[row['retained_primary']];assert row['retained_primary_pin']['sha256']==primary['sha256']
    assert (row['size'],row['sha256'])==(primary['size'],primary['sha256'])
    assert row['identity'][:2]!=primary['identity'][:2]
    candidate_edges=0;primary_edges=0
    for edge in row['original_path_manifest_edges']:
        ep=Path(edge['manifest']);fullpin(ep,edge['manifest_sha256'])
        line=ep.read_text().splitlines()[edge['line']-1]
        match=re.fullmatch(r'([0-9a-f]{64})\s+\*?(.+)',line);assert match
        original_hash,field=match.groups();assert field==edge['original_path_field'] and original_hash==edge['original_sha256']==row['sha256']
        resolved=Path(os.path.normpath(str(Path(field) if field.startswith('/') else ep.parent/field)))
        assert str(resolved)==edge['resolved_bound_path']
        assert resolved==Path(row['path'] if edge['side']=='candidate' else row['retained_primary'])
        candidate_edges+=edge['side']=='candidate';primary_edges+=edge['side']=='primary'
    assert primary_edges>0
    if row['work_copy_class']=='OLD_PORTABLE_PARENT_AXIAL_WORK_COPY':assert candidate_edges>0
for row in m['retained_primaries']:fullpin(row['path'],row)
for row in m['source_and_review_pins']:fullpin(row['path'],row)
print(json.dumps(dict(phase='all22_candidates13_primaries2684_source_pins_fresh_full_SHA_verified',fresh_files=len(PINS))),flush=True)

# Independently scan all ordinary formal source files; do not import them.
families={Path(row['path']).relative_to(ART).parts[0] for row in candidates}|{'iterative-seed'}
macrolib_families={Path(row['path']).relative_to(ART).parts[0] for row in candidates if row['work_copy_class']=='OLD_ITERATIVE_INITIAL_AXIAL_WORK_COPY'}
source_matches=[];formal_count=0;seed_proofs=[]
for current,dirs,names in os.walk(ROOT,followlinks=False):
    dirs[:]=[d for d in dirs if d not in ('.git','.codex','.agents','.aws','artifacts') and not (Path(current)==ROOT/'validation' and d.startswith('storage_'))]
    for name in names:
        p=Path(current)/name
        if p.is_symlink() or not p.is_file() or p.suffix not in ('.py','.sh','.x2m','.c2m','.f','.f90','.c','.h','.toml','.yaml','.yml') or p.stat().st_size>4*1024**2:continue
        rec=fullpin(p);formal_count+=1;text=p.read_text(errors='replace');matches=[]
        for line_no,line in enumerate(text.splitlines(),1):
            found=sorted(f for f in families if f in line)
            if found:matches.append(dict(line=line_no,text=line,families=found))
        if matches:source_matches.append(dict(path=str(p),sha256=rec['sha256'],matches=matches))
        if name in ('run_pin_current_picard.sh','run_full_rank_physical_map.sh'):
            assert 'SEED="$ROOT/validation/artifacts/iterative-seed"' in text and '"$SEED/initial_axial_macrolib.xsm"' in text
            seed_proofs.append(dict(source=rec,retained_input=str(ART/'iterative-seed/initial_axial_macrolib.xsm')))
assert len(seed_proofs)==2
assert not any(set(match['families']).intersection(macrolib_families) for row in source_matches for match in row['matches'])
seed=fullpin(ART/'iterative-seed/initial_axial_macrolib.xsm','2e01e806683ce25b5771af055112dc86dcf147245abc5a5c3dceac4d9939373a')
mesh=ROOT/'validation/iterative/run_d4a_axial_mesh_probe.py';mesh_text=mesh.read_text();mesh_tree=ast.parse(mesh_text)
inputs=next(ast.literal_eval(n.value) for n in mesh_tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='INPUTS' for t in n.targets))
assert inputs=={'radial.xsm':'candidate_radial.xsm','basis.xsm':'basis_reference.xsm','macro.xsm':'initial_axial_macrolib.xsm','reference.xsm':'candidate_system.xsm'}
assert 'parent_axial_closed.xsm' not in mesh_text
for name in inputs.values():assert str(ART/'d4a-corrected-material-rank2-series-from-map5-20260922/map-003.portable'/name) not in selected

documents=load(R/'result_document_full_sha_baseline.json',DOC_SHA)
assert documents['count']==pre['result_documents_full_sha_checked']==len(documents['rows'])==32452
assert documents['bytes']==pre['result_document_bytes']==sum(row['size'] for row in documents['rows'])==3738511671
assert len({row['path'] for row in documents['rows']})==32452
for i,row in enumerate(documents['rows'],1):
    p=ROOT/row['path'];assert p.is_relative_to(ROOT) and str(p) not in selected
    fullpin(p,row)
    if i%8000==0:print(json.dumps(dict(phase='full_result_document_SHA_read',checked=i,expected=32452)),flush=True)
after,after_digest=snapshot();assert before==after and before_digest==after_digest==pre['untouched_snapshot_sha256']
for p,record in list(PINS.items()):assert identity(Path(p))==record['identity'],p
assert fullpin(R/'manifest.json',M_SHA)['sha256']==M_SHA and fullpin(R/'preflight.json',PF_SHA)['sha256']==PF_SHA
assert not (R/'retirement_ledger.jsonl').exists() and not (R/'cleanup_result.json').exists()

report=dict(schema='SPOT_TENTH_FIXED_EXACT_DUPLICATE_PREFLIGHT_INDEPENDENT_REVIEW_V1',status='PASS',manifest_sha256=M_SHA,preflight_sha256=PF_SHA,cleanup_source_sha256=SOURCE_SHA,Root_preflight_terminal_sha256=TERMINAL_SHA,result_document_baseline_sha256=DOC_SHA,scope='PRE_DELETE_ONLY; no cleanup/restore/business script was invoked and no actual deletion success is claimed',exact_candidates=22,retained_primaries=13,source_and_review_pins=2684,logical_bytes=491945768,allocated_bytes=491978752,allocated_GiB=491978752/1024**3,all_candidates_fresh_full_SHA_and_singlelink_unique_identity=True,all_pairs_full_size_SHA_equal_and_distinct_inode=True,all_original_path_bound_manifest_edges_independently_resolved=True,candidate_original_manifest_counts=dict(path_bound=sum(any(e['side']=='candidate' for e in row['original_path_manifest_edges']) for row in candidates),no_candidate_original_manifest=sum(not any(e['side']=='candidate' for e in row['original_path_manifest_edges']) for row in candidates)),all_source_pins_fresh_full_SHA=True,all_32452_original_result_document_bytes_fresh_full_SHA=True,result_document_bytes=3738511671,full_content_read_unique_files=len(PINS),full_content_read_unique_bytes=sum(p['size'] for p in PINS.values()),full_content_pin_records='independent_preflight_fresh_SHA_records.json',whole_project_baseline=dict(fingerprint_before=before_digest,fingerprint_after=after_digest,counts=before_counts,whole_files_links_directory_paths_exact_equal=True,excludes=['top-level .git','this round report directory'],all_project_file_content_hash=False),current_closure=dict(graph=graph_counts,old_protection_index_rebuilt=True,current_cold6248_paths=len(m9['current_cold_extra_protected_files']),prior9124_restore_source_records=len(restore_sources),prior_restore_unique_paths=len({r['path'] for r in restore_sources}),critical_roots=len(m9['critical_roots']),prior_round9_retained_primaries=len(m9['retained_primaries']),prior_round9_sources=len(m9['source_and_review_pins']),conservative_exact_paths=len(exact),directory_prefixes=len(prefixes),fresh_symlinks=len(link_records),candidate_intersections_zero=True,permanent89gzip_archive_prefix_protected=True,old_225_and_new3_resource_root_contract_not_pruned=True),default_iterative_seed=dict(pin=seed,two_formal_runner_source_proofs=seed_proofs),source_literal_matches=source_matches,formal_source_files_fresh_read=formal_count,current_map8_mesh_probe_inputs_retained=inputs,restore_helper_source_pin=restore_pin,source_review=dict(previous_independent_report='cleanup_source_review.json',only_unlink_line=122,no_scanning_delete_or_restore_run=True,source_compiled_not_invoked=True),Root_preflight_actual_terminal=terminal,elapsed_seconds=time.monotonic()-START,actual_apply_tool_terminal=None,files_deleted=0,ART_or_formal_written=False,business_API_constructor_PREP_RUN_or_solver=False,scientific_or_RSS_credit=False,limits=['Copies without candidate-original manifest are honestly classified from complete fresh byte equality, original retained clean-primary manifest and old recipe/log evidence; no missing candidate seal is invented.','Generic historical accept/export/whole-manifest/replay readers of retired old paths must restore these exact22 copies from retained primary first. Earlier missing history has its earlier separate recipes;89 archived raw material primaries require gzip restore first. Inode/ctime cannot be recreated.','All unique final/closed states, numerical outputs, original sources/results/logs, current seven INPUT/cold/full native namespaces and frozen V8 source/OUT/TERM remain retained.','No new scientific INPUT admission, physics, combined/native memory measurement or V8 failure-line localization was performed.','Scope permit is limited to exact approved manifest/source/preflight bytes and whole original baseline; any change requires fresh review.'])
save('independent_preflight_fresh_SHA_records.json',list(PINS.values()))
save('independent_preflight_review.json',report)
print(json.dumps(dict(status='PASS',report=str(OUT/'independent_preflight_review.json'),report_sha256=hashlib.sha256((OUT/'independent_preflight_review.json').read_bytes()).hexdigest(),manifest_sha256=M_SHA,preflight_sha256=PF_SHA,fresh_files=len(PINS),fresh_bytes=report['full_content_read_unique_bytes'],baseline=before_digest,files_deleted=0)),flush=True)
