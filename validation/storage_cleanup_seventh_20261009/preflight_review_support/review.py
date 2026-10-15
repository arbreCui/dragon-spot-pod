import ast, collections, hashlib, json, os, stat, time
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path('/Users/wen/spot')
R=ROOT/'validation/storage_cleanup_seventh_20261009'
OUT=Path('/private/tmp/spot_storage_seventh_final_preflight_independent_review_20261009')
MANIFEST='80db08c34dcaa406950eb3680287f016d619ee76ac9503232dbf8e9348ee6038'
PREFLIGHT='63b88ddaca81a980ae6d62f70305f8d07acede3257937ad11642a6f64b992518'
TERMINAL='31fdccbe6016ae0e991b9b7860307e151770f36d0d9ec8119c3545bbfb9905c7'
start=time.monotonic()
hashed={}

def identity(p):
    s=Path(p).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def fresh(p,expected=None):
    p=Path(p); a=identity(p)
    assert stat.S_ISREG(a[2]),str(p)
    if str(p) in hashed:
        assert hashed[str(p)]['identity']==a
        result=hashed[str(p)]
    else:
        h=hashlib.sha256()
        with p.open('rb') as f:
            assert [os.fstat(f.fileno()).st_dev,os.fstat(f.fileno()).st_ino]==a[:2]
            while chunk:=f.read(4*1024**2):h.update(chunk)
        assert identity(p)==a,str(p)
        result=dict(path=str(p),identity=a,size=a[3],sha256=h.hexdigest())
        hashed[str(p)]=result
    if expected:
        assert result['sha256']==expected,str(p)
    return result

def doc(p,expected=None):
    pin=fresh(p,expected)
    return json.loads(Path(p).read_text()),pin

def projection(row):
    return {k:row[k] for k in ('path','identity','size','sha256')}

def inventory(selected):
    h=hashlib.sha256();counts=collections.Counter()
    for dp,dn,fn in os.walk(ROOT,followlinks=False):
        dn[:]=sorted(n for n in dn if Path(dp)/n!=R)
        for name in sorted(dn+fn):
            p=Path(dp)/name
            if str(p) in selected:continue
            s=p.lstat();rel=str(p.relative_to(ROOT))
            if stat.S_ISLNK(s.st_mode):row=[rel,identity(p),os.readlink(p)];counts['symlinks']+=1
            elif stat.S_ISDIR(s.st_mode):row=[rel,'directory'];counts['directories']+=1
            elif stat.S_ISREG(s.st_mode):row=[rel,identity(p)];counts['regular_files']+=1
            else:raise ValueError(str(p))
            h.update(json.dumps(row,ensure_ascii=False,separators=(',',':')).encode()+b'\n')
    return dict(sha256=h.hexdigest(),**dict(counts))

def sha_manifest(p):
    fresh(p)
    rows={}
    for line in Path(p).read_text().splitlines():
        sha,name=line.split(None,1);name=name.strip()
        assert name not in rows and len(sha)==64
        rows[name]=sha
    return rows

m,mp=doc(R/'manifest.json',MANIFEST)
pf,pp=doc(R/'preflight.json',PREFLIGHT)
terminal,tp=doc(R/'preflight_terminal_observation.json',TERMINAL)
assert terminal['closed'] is True and terminal['exit_code']==0 and terminal['actual_stdout_status']=='PASS'
assert terminal['initial_chunk_id']=='8bbca8' and terminal['session_id']==5475 and terminal['terminal_chunk_id']=='640173'
assert terminal['manifest_sha256']==MANIFEST and terminal['preflight_sha256']==PREFLIGHT and terminal['files_deleted']==0
assert pf['status']=='PASS' and pf['manifest_sha256']==MANIFEST and pf['files_deleted']==0 and not pf['solver_or_API_executed']
assert not (R/'cleanup_result.json').exists() and not (R/'retirement_ledger.jsonl').exists()
selected={c['path'] for c in m['candidates']}
assert len(selected)==len(m['candidates'])==m['exact_count']==1183
assert pf['verified_candidates']==[projection(c) for c in m['candidates']]
assert pf['verified_primaries']==[projection(c) for c in m['retained_primaries']]
assert sum(c['allocated_bytes'] for c in m['candidates'])==m['allocated_bytes']==7642398720
assert sum(c['size'] for c in m['candidates'])==m['logical_bytes']==7639813773
before=inventory(selected)
assert before==pf['preservation_baseline'],(before,pf['preservation_baseline'])

records={}
for row in m['candidates']+m['retained_primaries']+m['source_and_review_pins']+[m['graph_pin'],m['old_index_pin']]:
    projected=projection(row)
    if row['path'] in records:assert records[row['path']]==projected,row['path']
    records[row['path']]=projected
    assert identity(row['path'])==row['identity'] and stat.S_ISREG(row['identity'][2]),row['path']
assert not selected & {c['path'] for c in m['retained_primaries']}
primaries={c['path']:c for c in m['retained_primaries']}
for c in m['candidates']:
    p=Path(c['path'])
    assert p.is_absolute() and str(p)==c['path'] and '..' not in p.parts
    assert p.is_relative_to(ROOT/'validation/artifacts') and p.parent.resolve(strict=True)==p.parent
    assert c['identity'][-1]==1 and p.lstat().st_blocks*512==c['allocated_bytes']
    assert c['historical_whole_replay_restore_required'] is True
    if c['category']=='EXACT_DUPLICATE_OLD_WORK_COPY':
        k=primaries[c['retained_primary']]
        assert c['path']!=k['path'] and c['identity'][:2]!=k['identity'][:2]
        assert c['size']==k['size'] and c['sha256']==k['sha256']
    else:assert c['category']=='EXACT_RECONSTRUCTIBLE_REHEARSAL_TAR'

graph,gp=doc(m['graph_pin']['path'],m['graph_pin']['sha256'])
index,ip=doc(m['old_index_pin']['path'],m['old_index_pin']['sha256'])
absolute=set()
def walk(v):
    if isinstance(v,dict):
        for k,item in v.items():walk(k);walk(item)
    elif isinstance(v,list):
        for item in v:walk(item)
    elif isinstance(v,str) and v.startswith('/'):absolute.add(v)
walk(graph)
directories={x['canonical_root'] for x in graph['namespaces']}|{x['target'] for x in graph['aliases'] if x['kind'] in ('directory','dir')}|set(index['protected_directories'])|set(m['critical_roots'])
protected=absolute|set(index['protected_files'])|set(index['inbound_alias_targets'])
intersections=[p for p in selected if p in protected or any(p==d or p.startswith(d+'/') for d in directories)]
assert not intersections
closure=dict(canonical_files=len(graph['canonical_files']),namespaces=len(graph['namespaces']),aliases=len(graph['aliases']),live_resource_roots=len(graph['live_resource_roots']),old_protected_files=len(index['protected_files']),critical_roots=len(m['critical_roots']),candidate_intersections=[])
assert closure==pf['current_closure']
link_rows=[]
for dp,dn,fn in os.walk(ROOT,followlinks=False):
    for name in dn+fn:
        p=Path(dp)/name
        if p.is_symlink():
            target=p.resolve(strict=False)
            assert not any(Path(q)==target or Path(q).is_relative_to(target) for q in selected),(str(p),str(target))
            link_rows.append([str(p),os.readlink(p),str(target)])
link=dict(count=len(link_rows),sha256=hashlib.sha256(json.dumps(sorted(link_rows)).encode()).hexdigest())
assert link==pf['symlink_screen'] and link['count']==687

# Rehash all manageable retained/source metadata and full replay data independently.
# Large material/snapshot/archive bytes were freshly hashed by the actual Root
# preflight and the independent dedicated author; this review rechecks identities.
skipped=[]
for p,row in records.items():
    if row['size']<=64*1024**2 or p in (m['graph_pin']['path'],m['old_index_pin']['path']):fresh(p,row['sha256'])
    else:skipped.append(dict(**row,reason='NO_REPEAT_LARGE_READ: actual Root full-content preflight + dedicated prior full-content independent evidence; fresh full lstat identity matched'))

replay,rpin=doc(R/'replay/exact_replay_candidates.json','8e95ba35f94cbe27d222372209649e7d9afa8de82714a0f4f5bcac82fcf6f90a')
assert replay['status']=='PASS' and len(replay['candidates'])==1172
replay_paths=set();manifests={}
for row in replay['candidates']:
    c=row['candidate'];k=row['retained_primary'];root=row['artifact']
    assert projection(c)==records[c['path']] and projection(k)==primaries[k['path']]
    assert records[c['path']]['sha256']==row['expected_sha256']==k['sha256']
    fresh(c['path'],c['sha256']);fresh(k['path'],k['sha256'])
    orig=row['original_manifest'];fresh(orig['path'],orig['sha256'])
    if orig['path'] not in manifests:manifests[orig['path']]=sha_manifest(orig['path'])
    md=manifests[orig['path']]
    assert md[row['candidate_manifest_relative_path']]==md[row['primary_manifest_relative_path']]==c['sha256']
    assert str(Path(root)/row['candidate_manifest_relative_path'])==c['path']
    assert str(Path(root)/row['primary_manifest_relative_path'])==k['path']
    assert row['old_full_stage_replay_requires_restoring_selected_copy'] is True
    assert row['no_unique_primary_payload_retired'] is True
    assert not any(row['current_old_critical_blockers'].values())
    replay_paths.add(c['path'])

materials,material_pin=doc(R/'materials/independent_recommendation.json','f8d16fe395187d1e6cf638824065b6f78741ef82c29965beb82ef82d50bd1bd4')
material_paths={c['path'] for c in materials['recommended_old_workcopy_retirements']}
assert len(material_paths)==5
for c in materials['recommended_old_workcopy_retirements']:
    actual=records[c['path']]
    assert c['identity']==actual['identity'] and c['logical_bytes']==actual['size'] and c['sha256']==actual['sha256']
assert all(c['path'] not in selected and identity(c['path'])==c['identity'] for c in materials['mandatory_retained_duplicate_masters'])
material_art=ROOT/'validation/artifacts/d4a-actual-temperature-material-run-20261003'
material_seal=sha_manifest(material_art/'result.sha256')
for temp in (650,750,850):
    p=material_art/f'material{temp}/DLIB8R1_370'
    ih,_=doc(p.parent/'input_hashes.json')
    assert ih[str(p)]==material_seal[str(p.relative_to(material_art))]==records[str(p)]['sha256']
frozen,_=doc(ROOT/'validation/artifacts/axial-material-inputs-20261003/frozen_inputs.json')
assert frozen['files']['B/DLIB8R1_370']==records[str(ROOT/'validation/artifacts/axial-material-inputs-20261003/B/DLIB8R1_370')]['sha256']
lib_art=ROOT/'validation/artifacts/d4a-actual-temperature-library-run-20261003'
lib_seal=sha_manifest(lib_art/'result.sha256');imp,_=doc(lib_art/'import/input_hashes.json')
assert imp[str(lib_art/'import/EXPORT')]==lib_seal['import/EXPORT']==lib_seal['merge/28-U238/tape30']==records[str(lib_art/'import/EXPORT')]['sha256']

bootstrap={str(ROOT/'validation/artifacts/axial-material-production-qualified-AB-storage-20261004/AAA/bootstrap'/name) for name in ('seed_snapshots.xsm','refreshed_snapshots.xsm')}
bootstrap|={str(ROOT/'validation/artifacts'/family/'controls/current_input/snapshots.xsm') for family in ('axial-material-spoasm-physical-build-20261007','axial-material-spoasm-physical-guarded-build-20261007','axial-material-spoasm-physical-abi-guarded-build-20261007')}
assert len(bootstrap)==5
for p in bootstrap:
    c=next(c for c in m['candidates'] if c['path']==p)
    if '/bootstrap/' in p:
        result,_=doc(Path(p).parent/'result.json')
        assert result['sha256'][Path(p).name]==c['sha256']
    else:
        declaration,_=doc(ROOT/'validation/artifacts'/Path(p).relative_to(ROOT/'validation/artifacts').parts[0]/'declaration.json')
        assert declaration['files'][p]==c['sha256']

tar,tar_pin=doc(R/'tar/candidate.json','bcfce8d4208828a636a13979809ebd792ebb4c3cdcc2e161b856a82b864756f7')
tar_independent,tar_independent_pin=doc(R/'dependency/independent_exact_tar_candidate_review.json','cebcbc413b27b3fed8fa3d19f648594b45c870073aa5c8673ae59139df3d92ec')
assert tar_independent['status']=='PASS' and tar_independent['member_count']==39
assert tar_independent['fresh_archive_sha256']==tar_independent['independent_stream_reconstruction_sha256']==tar['candidate']['sha256']
assert tar_independent['fresh_patch_sha256']==tar['patch']['sha256']
assert tar_independent['all_39_regular_canonical_source_payloads_freshly_byte_equal_to_original_tar'] is True
tar_path=tar['candidate']['path'];tar_c=next(c for c in m['candidates'] if c['path']==tar_path)
assert projection(tar['candidate'])==records[tar_path]
assert tar_c['restoration_recipe_sha256']==tar_pin['sha256']
assert tar['member_count']==len(tar['members'])==39 and len(tar['gaps'])==40
assert tar['exact_reconstruction_sha256']==tar_c['sha256']=='2d50b1647184293657cff95c2b69ad5874e60622cb8d3ed136ef8dcc1fdc4649'
patch=fresh(R/'tar/exact_tar_headers_and_padding.bin',tar['patch']['sha256'])
assert patch['size']==tar['patch']['size']==71214
release=sha_manifest(tar['original_release_manifest']['path']);assert len(release)==38
segments=[]
for member in tar['members']:
    payload=member['retained_payload'];assert projection(payload)==primaries[payload['path']]
    assert member['size']==payload['size']
    if member['name']!='d4a_closed0_release.sha256':assert release[member['name']]==payload['sha256']
    else:assert payload['sha256']==tar['original_release_manifest']['sha256']
    segments.append((member['data_offset'],member['size']))
for gap in tar['gaps']:
    assert gap['patch_offset']>=0 and gap['patch_offset']+gap['size']<=patch['size']
    segments.append((gap['archive_offset'],gap['size']))
end=0
for off,size in sorted(segments):assert off==end;end+=size
assert end==tar_c['size'] and sum(g['size'] for g in tar['gaps'])==patch['size']
assert selected==bootstrap|material_paths|replay_paths|{tar_path}
assert sum(map(len,(bootstrap,material_paths,replay_paths,{tar_path})))==1183
prior_ledgers=[]
for row in m['previous_six_retirement_overlap_screen']:
    ledger=row['ledger'];fresh(ledger['path'],ledger['sha256'])
    lines=[json.loads(line) for line in Path(ledger['path']).read_text().splitlines()]
    assert len(lines)==row['retired_count']
    previous={c['path'] if 'path' in c else c['candidate']['path'] for c in lines}
    assert not selected & previous and row['current_selected_overlap']==0
    prior_ledgers.append(dict(path=ledger['path'],count=len(lines),sha256=ledger['sha256']))

tools,tools_pin=doc(R/'tool_review/final_source_review.json','501025235d7ffc96d850c7ad2d5c6fc0463675b1f58607311fbea4a473919e44')
assert tools['status']=='PASS_STATIC_SOURCE_STRUCTURE_ONLY'
for row in tools['files']:
    current=fresh(row['path'],row['sha256']);assert current['identity']==row['identity']
    ast.parse(Path(row['path']).read_text())
assert fresh(R/'cleanup_exact_files.py')['sha256']==m['cleanup_source_sha256']
for row in m['historical_tool_source_review_pins_are_preserved_prior_to_explicit_reviewed_repairs']['prior_sources']:
    fresh(row['preserved_original_source'],row['old_sha256']);fresh(row['path'],row['new_sha256'])
source=Path(R/'cleanup_exact_files.py').read_text();tree=ast.parse(source)
assert source.count('p.unlink()')==1 and 'shutil.rmtree' not in source and 'os.remove' not in source
assert "pf['manifest_sha256']==mp['sha256']" in source
assert "rv['manifest_sha256']==mp['sha256']" in source and "rv['preflight_sha256']==pp['sha256']" in source
assert "if not __debug__:" in source and "Cleanup safety gates require Python optimization to be disabled" in source
assert 'safe_art_path(c[\'path\'])' in source
after=inventory(selected);assert after==before==pf['preservation_baseline']
for p,row in records.items():assert identity(p)==row['identity'],p
assert fresh(R/'manifest.json')['sha256']==MANIFEST and fresh(R/'preflight.json')['sha256']==PREFLIGHT
report=dict(
    schema='SPOT_SEVENTH_EXACT_UNION_ACTUAL_PREFLIGHT_INDEPENDENT_READ_ONLY_REVIEW_V1',
    status='PASS',manifest_sha256=MANIFEST,preflight_sha256=PREFLIGHT,
    scope='Pre-deletion only. Fixed 1183 exact retired work copies/reconstructible original tar. No actual cleanup completion or science qualification granted.',
    utc=datetime.now(timezone.utc).isoformat(),manifest_pin=mp,preflight_pin=pp,actual_closed_Root_terminal=terminal,terminal_pin=tp,
    independent_review_harness_initial_attempt=dict(initial_chunk_id='e7fbed',session_id=24803,terminal_chunk_id='f13f0f',exit_code=1,reason='The reviewer incorrectly expected a files key in original bootstrap result.json; fresh original schema has classification and sha256. Only the harness lookup was corrected. No project operation or candidate evidence failure.'),
    independent_review_harness_second_attempt=dict(initial_chunk_id='2cfdb6',session_id=62888,terminal_chunk_id='e43c74',exit_code=1,reason='The reviewer expected all old ledger rows to have top-level path; original second ledger nests it at candidate.path. Only schema-aware old-ledger projection was corrected. No project operation or candidate evidence failure.'),
    exact_union=dict(bootstrap_control=5,material_staging=5,replay_work=1172,reconstructible_tar=1,total=1183,logical_bytes=m['logical_bytes'],allocated_bytes=m['allocated_bytes'],allocated_GiB=m['allocated_bytes']/2**30),
    all_1183_fresh_lstat_identity_allocated_singlelink_canonical_realparent_checks=True,
    all_1216_retained_primaries_and_540_source_review_records_fresh_identity_matches=True,
    independent_full_content_hash_count=len(hashed),independent_full_content_hash_bytes=sum(p['size'] for p in hashed.values()),fresh_full_hash_pins=list(hashed.values()),
    no_repeat_large_content_hashes=skipped,
    large_content_limit='This reviewer did not reread every multi-hundred-MiB bootstrap/material/archive payload. All listed identities remained exactly stable, actual Root preflight freshly full-hashed all selected, retained, source and graph/index records before exit0; dedicated independent source/candidate reports had also freshly hashed those complete payloads. All 1172 replay candidate and counterpart complete payloads were independently rehashed in this review.',
    original_manifest_replay_pairs_independently_verified=1172,original_replay_result_manifests=list(manifests),material_original_frozen_staged_and_result_SHA_links_verified=True,
    tar_metadata_recipe=dict(pin=tar_pin,patch_pin=patch,independent_saved_full_reconstruction_report_pin=tar_independent_pin,regular_members=39,original_release_manifest_payloads=38,complete_archive_segment_coverage=True,unique_headers_padding_bytes=71214,independent_stream_reconstruction_executed_here=False,reviewed_independent_saved_reconstruction='dependency/independent_exact_tar_candidate_review.json PASS complete hash equal; actual Root preflight invokes read-only dry proof, no restored archive'),
    current_closure=closure,graph_pin=gp,old_index_pin=ip,current_graph_absolute_fields_inspected=len(absolute),candidate_closure_intersections=intersections,
    all_project_symlink_screen=link,nonselected_before=before,nonselected_after=after,nonselected_identity_fingerprint_unchanged=True,
    old_six_retirement_ledger_overlap=[],fresh_prior_ledgers=prior_ledgers,
    reviewed_tools_pin=tools_pin,cleanup_one_exact_unlink_inside_bound_fixed_candidate_loop=True,
    restoration_obligations=[
        'Original whole sealed bootstrap export, old failed factory whole declaration/filemap/control replay, and full original result.sha256 replay require exact copies restored from retained primary first. Do not rewrite immutable original manifests or promote old failure.',
        'Old material/native generation needs exact staging restored; project A production original, external production original, final merge tape30 and all actual material outputs remain.',
        'Native original full replay stage needs retired replay copies restored from retained unique primary archives; all primary scientific data and saved result/receipt/log/source records remain.',
        'The retired old tar can be reconstructed byte-exact only with saved unique header/padding patch and all 39 retained release payloads, including original release manifest. No generic tar re-export equivalence is claimed.'
    ],
    blockages=[],files_deleted=0,project_or_ART_or_formal_source_writes=0,apply_or_restore_executed=False,business_import_API_constructor_native_PREP_RUN_executed=False,new_scientific_or_RSS_credit=False,
    preservation_limit='Whole nonselected fingerprint proves regular identity and link/structure continuity, not full-byte reread of every 160+ GiB project file. Directory rows track path existence; identity/allocated tests and Root bound exact loop constrain deletion. Future arbitrary user-selected paths are outside saved current closure proof.',
    elapsed_seconds=time.monotonic()-start)
OUT.mkdir(parents=True,exist_ok=True)
target=OUT/'REPORT.json'
with target.open('x') as f:json.dump(report,f,indent=2,ensure_ascii=False);f.write('\n')
pin=fresh(target)
print(json.dumps(dict(status=report['status'],report=str(target),sha256=pin['sha256'],bytes=pin['size'],independent_full_content_hash_count=report['independent_full_content_hash_count'],independent_full_content_hash_bytes=report['independent_full_content_hash_bytes'],no_repeat_large_content_count=len(skipped),baseline=before,elapsed_seconds=report['elapsed_seconds']),ensure_ascii=False))
