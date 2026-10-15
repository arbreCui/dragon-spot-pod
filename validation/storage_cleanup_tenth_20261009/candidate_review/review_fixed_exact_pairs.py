"""Fixed full-byte proofs and static dependencies only. No restore/delete/API."""
import hashlib
import json
import os
import re
import stat
from pathlib import Path

ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts';OUT=Path('/private/tmp/spot_storage_tenth_exact_dependency_review_20261009')
PINS={};PAYLOADS={}
def full_read(p,expected=None,metadata=None,keep=False):
    p=Path(p);s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
    assert p.is_absolute() and p.parent.resolve(strict=True)==p.parent and stat.S_ISREG(s.st_mode)
    if metadata:assert before==metadata['identity'] and s.st_blocks*512==metadata['allocated_bytes']
    h=hashlib.sha256();length=0;parts=[]
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
        fs=os.fstat(f.fileno());assert [fs.st_dev,fs.st_ino]==before[:2]
        while chunk:=f.read(1024**2):
            length+=len(chunk);h.update(chunk)
            if keep:parts.append(chunk)
    s=p.lstat();assert before==[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink] and length==before[3]
    digest=h.hexdigest()
    if expected:assert digest==expected,(str(p),digest,expected)
    rec=dict(path=str(p),sha256=digest,size=length,allocated_bytes=s.st_blocks*512,identity=before)
    if str(p) in PINS:assert PINS[str(p)]==rec
    PINS[str(p)]=rec
    if keep:PAYLOADS[str(p)]=b''.join(parts)
    return rec
def readjson(p,expected=None):full_read(p,expected,keep=True);return json.loads(PAYLOADS[str(p)])
def write(name,value):
    with (OUT/name).open('x') as f:json.dump(value,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
selection=readjson(OUT/'preliminary_fixed_pair_selection.json')
screen=readjson(OUT/'metadata_screen.json')
assert len(selection)==23
selected_paths={r['candidate']['path'] for r in selection}
primary_paths={r['primary']['path'] for r in selection}
assert not selected_paths.intersection(primary_paths)
held_seed=ART/'iterative-seed/initial_axial_macrolib.xsm'
recommended=[];held=[];proofs=[]
for pair in selection:
    c=full_read(pair['candidate']['path'],pair['original_eighth_sha256'],pair['candidate'])
    p=full_read(pair['primary']['path'],pair['original_eighth_sha256'],pair['primary'])
    assert c['size']==p['size'] and c['sha256']==p['sha256'] and c['identity'][:2]!=p['identity'][:2]
    assert c['identity'][-1]==1  # Primary is read/retained; it may have other kept hard links.
    assert not pair['candidate']['protection_reasons']
    evidence=[]
    for side,path in [('candidate',Path(c['path'])),('primary',Path(p['path']))]:
        members=[]
        for item in sorted(path.parent.iterdir()):
            if not item.is_file() or item.is_symlink():continue
            if item.suffix not in ('.sha256','.txt','.log','.sh','.py','.x2m','.c2m','.l2m','.json','.md','.tsv') and item.name!='Makefile':continue
            if item.stat().st_size>8*1024**2:continue
            pin=full_read(item,keep=True);members.append(pin)
            if item.suffix=='.sha256':
                for line_no,line in enumerate(PAYLOADS[str(item)].decode('utf-8').splitlines(),1):
                    match=re.fullmatch(r'([0-9a-f]{64})\s+\*?(.+)',line)
                    if not match:continue
                    filename=match.group(2)
                    resolved=Path(filename) if filename.startswith('/') else item.parent/filename
                    resolved=Path(os.path.normpath(str(resolved)))
                    if resolved==path:
                        assert match.group(1)==c['sha256'],(str(item),filename)
                        evidence.append(dict(side=side,manifest=str(item),manifest_sha256=pin['sha256'],line=line_no,original_path_field=filename,resolved_bound_path=str(path),original_sha256=match.group(1)))
        proofs.append(dict(side=side,work_directory=str(path.parent),retained_original_small_manifest_recipe_and_logs=members))
    primary_manifest=[e for e in evidence if e['side']=='primary'];assert primary_manifest,('retained primary has no original path-bound manifest',p['path'])
    candidate_manifest=[e for e in evidence if e['side']=='candidate']
    if pair['class_']=='OLD_PORTABLE_PARENT_AXIAL_WORK_COPY':assert candidate_manifest
    item=dict(path=c['path'],sha256=c['sha256'],size=c['size'],allocated_bytes=c['allocated_bytes'],identity=c['identity'],category='EXACT_DUPLICATE_OLD_WORK_COPY',retained_primary=p['path'],retained_primary_pin=p,original_evidence_classification='BOTH_ORIGINAL_PATH_BOUND_MANIFESTS_PLUS_FRESH_EXACT_BYTES' if candidate_manifest else 'FRESH_EXACT_BYTES_RETAINED_PRIMARY_ORIGINAL_MANIFEST_AND_OLD_RECIPE_LOG_ONLY_NO_CANDIDATE_MANIFEST',original_path_manifest_edges=evidence,static_current_protection_reasons=pair['candidate']['protection_reasons'],prior_eighth_full_SHA=pair['original_eighth_sha256'],work_copy_class=pair['class_'],restore_byte_exact_mapping=True,historical_limit='Old whole manifests/readers or generic user-selected old work replay require restoring this exact path from retained primary first; original seal/input/result digests remain unchanged. Other prior missing work files also need their earlier restoration recipes. No old inode/ctime recreation or science credit promised.')
    if c['path']==str(held_seed):item['hold_reason']='CURRENT_GENERIC_ITERATIVE_DEFAULT_INPUT_READ_BY_TWO_FORMAL_RUNNERS';held.append(item)
    else:recommended.append(item)
assert len(recommended)==22 and len(held)==1

# Fresh nonartifact sources: literal family/path and retained default-input proof.
families={Path(c['path']).relative_to(ART).parts[0] for c in recommended}
families.add('iterative-seed')
source_matches=[];source_pins=[];formal_sources=[]
for base,dirs,files in os.walk(ROOT,followlinks=False):
    dirs[:]=[d for d in dirs if d not in ('.git','.codex','.agents','.aws','artifacts') and not (Path(base)==ROOT/'validation' and d.startswith('storage_'))]
    for name in files:
        path=Path(base)/name
        if path.is_symlink() or path.suffix not in ('.py','.sh','.x2m','.c2m','.f','.f90','.c','.h','.toml','.yaml','.yml') or not path.is_file():continue
        if path.stat().st_size>4*1024**2:continue
        pin=full_read(path,keep=True);text=PAYLOADS[str(path)].decode('utf-8',errors='replace');source_pins.append(pin)
        found=[]
        for i,line in enumerate(text.splitlines(),1):
            names=sorted(f for f in families if f in line)
            if names:found.append(dict(line=i,text=line,families=names))
        if found:source_matches.append(dict(path=str(path),sha256=pin['sha256'],matches=found))
        if name in ('run_pin_current_picard.sh','run_full_rank_physical_map.sh'):
            assert 'SEED="$ROOT/validation/artifacts/iterative-seed"' in text and '"$SEED/initial_axial_macrolib.xsm"' in text
            formal_sources.append(dict(path=str(path),sha256=pin['sha256'],default_input=str(held_seed),lines=[dict(line=i,text=line) for i,line in enumerate(text.splitlines(),1) if 'SEED=' in line or '$SEED/initial_axial_macrolib.xsm' in line]))
assert len(formal_sources)==2
safe_families={Path(c['path']).relative_to(ART).parts[0] for c in recommended if c['work_copy_class']=='OLD_ITERATIVE_INITIAL_AXIAL_WORK_COPY'}
assert not any(set(row['families']).intersection(safe_families) for match in source_matches for row in match['matches'])

# Read exact original copy/admission definitions; never run them.
source_contracts=[]
for name in ('run_d4a_rank2_picard_map.sh','run_d4a_rank2_picard_series.sh','freeze_d4a_corrected_map.sh','check_d4a_corrected_acceptance.sh','export_d4a_corrected_result.py','run_d4a_corrected_final_observables.sh','run_d4a_axial_mesh_probe.py'):
    path=ROOT/'validation/iterative'/name;pin=full_read(path,keep=True);text=PAYLOADS[str(path)].decode()
    lines=[dict(line=i,text=line) for i,line in enumerate(text.splitlines(),1) if any(token in line for token in ('parent_axial_closed','closed_axial.xsm','initial_axial_macrolib','PARENT=','MAP8 =','INPUT_LINKS=','STAGE/','SOURCE/','for name in'))]
    source_contracts.append(dict(source_pin=pin,relevant_lines=lines))
picard=PAYLOADS[str(ROOT/'validation/iterative/run_d4a_rank2_picard_map.sh')].decode()
assert 'ln -s "$PARENT/closed_axial.xsm" "$WORK/parent_axial_closed.xsm"' in picard
freeze=PAYLOADS[str(ROOT/'validation/iterative/freeze_d4a_corrected_map.sh')].decode()
assert 'parent_axial_closed.xsm' in freeze and 'symlink_provenance.tsv' in freeze
mesh=PAYLOADS[str(ROOT/'validation/iterative/run_d4a_axial_mesh_probe.py')].decode()
assert "'macro.xsm': 'initial_axial_macrolib.xsm'" in mesh and "'reference.xsm': 'candidate_system.xsm'" in mesh
assert 'parent_axial_closed.xsm' not in mesh

before_primaries={c['retained_primary'] for c in recommended};assert not before_primaries.intersection(c['path'] for c in recommended)
for path,expected in list(PINS.items()):
    s=Path(path).lstat();assert [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]==expected['identity']
write('fixed_exact_recommendations.json',recommended)
write('explicit_current_default_input_HOLD.json',held)
write('fresh_entire_file_SHA_identity_records.json',list(PINS.values()))
write('original_manifest_and_recipe_log_proof.json',dict(path_manifest_edges=[c['original_path_manifest_edges'] for c in recommended],retained_small_directory_records=proofs,current_source_literal_matches=source_matches,held_current_default_source_proof=formal_sources,original_copy_and_legacy_manifest_contracts=source_contracts))
report=dict(schema='SPOT_TENTH_FIXED_EXACT_WORK_COPY_READONLY_RECOMMENDATION_V1',status='PASS_READONLY_EXACT_CANDIDATE_REVIEW_NOT_APPLY_APPROVAL',candidate_count=len(recommended),by_class=dict(OLD_ITERATIVE_INITIAL_AXIAL_WORK_COPY=sum(c['work_copy_class']=='OLD_ITERATIVE_INITIAL_AXIAL_WORK_COPY' for c in recommended),OLD_PORTABLE_PARENT_AXIAL_WORK_COPY=sum(c['work_copy_class']=='OLD_PORTABLE_PARENT_AXIAL_WORK_COPY' for c in recommended)),logical_bytes=sum(c['size'] for c in recommended),allocated_bytes=sum(c['allocated_bytes'] for c in recommended),allocated_GiB=sum(c['allocated_bytes'] for c in recommended)/1024**3,candidate_and_primary_all_fresh_full_SHA_size_equal=True,all_candidates_canonical_regular_singlelink=True,all_primary_paths_retained_distinct_no_cycle=True,all_retained_primary_original_path_bound_manifest=True,candidate_original_manifest_counts=dict(path_bound=sum(bool([e for e in c['original_path_manifest_edges'] if e['side']=='candidate']) for c in recommended),no_candidate_original_manifest=sum(not bool([e for e in c['original_path_manifest_edges'] if e['side']=='candidate']) for c in recommended)),all_candidate_current_V8_old_index_cold_dynamic_critical_restore_source_and_links_intersections_zero=True,current_default_seed_HOLD_count=1,current_generic_seed_formal_runner_sources=formal_sources,only_fixed_small_subset_reviewed=True,whole_project_content_hash_performed=False,full_read_unique_files=len(PINS),full_read_bytes=sum(p['size'] for p in PINS.values()),formal_nonartifact_source_files_read=len(source_pins),original_seals_results_and_documents_preserved_no_rewrite=True,all_final_closed_states_materials_unique_raw_nuclear_full_native_inputs_retained=True,fresh_complete_links=screen['protection_counts']['fresh_project_symlinks'],source_scope_limits=['V8 graph and explicit cold6248 path closure statically exclude these exact candidates; no actual business admission or API was reexecuted.','Generic archival consumers/export/acceptance with caller-chosen retired old work paths still require exact restoration; no global ban or promise about arbitrary future parameters.','No raw unique data removed or aggregated substitute claimed. Retained closed primaries and canonical clean replay preserve exact scientific bytes; paths can be recovered, inode/ctime cannot.'],files_deleted=0,formal_or_ART_written=False,business_API_ctor_PREP_RUN_or_native_child=False,AAA_ABA_credit=False)
write('REPORT.json',report)
print(json.dumps(dict(status=report['status'],candidates=len(recommended),logical_bytes=report['logical_bytes'],allocated_bytes=report['allocated_bytes'],allocated_GiB=report['allocated_GiB'],held=1,full_read_files=len(PINS),full_read_bytes=report['full_read_bytes'],report_sha256=hashlib.sha256((OUT/'REPORT.json').read_bytes()).hexdigest(),recommendations_sha256=hashlib.sha256((OUT/'fixed_exact_recommendations.json').read_bytes()).hexdigest())))
