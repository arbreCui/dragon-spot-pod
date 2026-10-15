"""R20 fixed thirty old intermediates current-readset review; no business."""
import hashlib
import json
import os
from pathlib import Path
import stat
import time

D=Path('/private/tmp/spot_storage_twentieth_current_graph_dependency_review_20261009')
ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts'
R=Path('/private/tmp/spot_storage_twentieth_root_20261009')
W=ART/'axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009'
S=ART/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-admission-scipy-env-physical-basis-own-pid-peak-v9-20261009'
START=time.monotonic();PINS={}

def identity(p):
    s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def pin(p,expected=None):
    p=Path(p);before=identity(p);assert stat.S_ISREG(before[2])and p.resolve(strict=True)==p
    h=hashlib.sha256()
    with p.open('rb')as f:
        while block:=f.read(4*2**20):h.update(block)
    assert identity(p)==before,str(p)
    row=dict(path=str(p),sha256=h.hexdigest(),bytes=before[3],identity=before)
    assert expected is None or row['sha256']==expected,str(p)
    PINS[str(p)]=row;return row

def pairs(items):
    result={}
    for k,v in items:assert k not in result;result[k]=v
    return result

def read(p,expected=None):
    row=pin(p,expected);result=json.loads(Path(p).read_bytes(),object_pairs_hook=pairs)
    assert identity(p)==row['identity'];return result

def allstrings(value):
    if type(value)is str:yield value
    elif type(value)is dict:
        for k,v in value.items():yield k;yield from allstrings(v)
    elif type(value)is list:
        for v in value:yield from allstrings(v)

proof=read(R/'proposed_candidates_full_byte_proof.json','517ef094a4cfb8163ef12db9fdc8d58c0d12584f891c09f2e90fd7af3ef6632e')
inventory=read(R/'inventory.json');prefilter=set(read(R/'graph_protected_paths.json'))
pin(R/'prove_candidates.py')
rows=proof['candidates'];chosen={r['path'] for r in rows}
names={'projected_proposal.xsm','candidate_radial.xsm','candidate_snapshots.xsm','candidate_axial.xsm','candidate_system.xsm','parent_for_checker.xsm'}
dates=['20260925','20260926','20260926','20260927','20260927']
independent_paths={str(ART/f'd4a-scattering-mesh12-picard-map{i}-{day}'/name)for i,day in enumerate(dates,1)for name in names}
assert len(chosen)==30 and chosen==independent_paths and chosen.isdisjoint(prefilter)
before_candidates={r['path']:identity(r['path'])for r in rows}
for r in rows:
    assert before_candidates[r['path']]==r['identity'] and stat.S_ISREG(r['identity'][2])and r['identity'][6]==1
    assert Path(r['path']).resolve(strict=True)==Path(r['path'])
    assert r['sha256']in r['original_manifest_sha256s'].values()and set(r['original_manifest_sha256s'].values())=={r['sha256']}
    assert r['not_a_closed_state']is True
for row in proof['original_manifests']:
    actual=pin(row['path'],row['sha256']);assert actual['identity']==row['identity']
assert proof['total_size_bytes']==2580841168 and proof['total_allocated_bytes']==2580910080

failure_proof=read('/private/tmp/axmat_v9_actual_native_failed_graph_resource_independent_review_20261009/REPORT.json','95e1da2142352dc0074d88a65f01913b6768270959891361622a87dad516e364')
failure_receipt=read('/private/tmp/axmat_v9_actual_native_failed_graph_resource_independent_review_20261009/actual_readonly_tool_return.json','0b29aa88caa40af3ab1ba7440353aeb2e19b72f92c32a1b5732124b405e942c3')
assert failure_receipt['actual_tool_result']['exit_code']==0 and failure_receipt['actual_tool_result']['closed']is True
binding=read(W/'own_rss_binding.json','4e8de93043fa08ac0c6e1f1702b69606a6bf0b155c30007c356ec4837919c930')
m=read(S/'rank1_factor_cache_admission.json','564592df0acffc7bbc2c0743cd1b4849db859ec7e83b6101def72ce4a5175742')
gp=failure_proof['graph_full_current_wire_pin'];graph=read(gp['path'],gp['sha256']);assert identity(gp['path'])==gp['identity']
canonical={r['path']:r for r in graph['canonical_files']}
assert len(binding['files'])==37395 and len(m['files'])==37339 and len(canonical)==35647
assert len(graph['namespaces'])==86 and len(graph['aliases'])==186 and len(graph['absence_inputs'])==445
current_sets=dict(expected37395=set(binding['files']),component37339=set(m['files']),canonical35647=set(canonical),
    requirement_symbol_paths=set(graph['requirements']['paths']),aliases_endpoints={v for r in graph['aliases']for v in (r['path'],r['target'])},
    absence445=set(graph['absence_inputs']),graph_exact_literal_strings=set(allstrings(graph)))
hits={k:sorted(chosen&v)for k,v in current_sets.items()}
namespace_hits=[]
for p in map(Path,chosen):
    for r in graph['namespaces']:
        root=Path(r['canonical_root'])
        if p==root or root in p.parents:namespace_hits.append(dict(path=str(p),namespace_root=str(root)))
assert all(not v for v in hits.values())and not namespace_hits

# Reuse the complete already independently audited native + prepare read-chain
# expansion through immutable source and metadata fullSHA, not guessed ancestry.
chain_root=Path('/private/tmp/spot_storage_nineteenth_current_native_snapshot_read_paths_20261009')
chain=read(chain_root/'REPORT.json','f055e095769fe065a11b24cf3b29693d8bc887c485da39495964ff2f7af7d6cf')
chain_receipt=read(chain_root/'actual_readonly_tool_return.json','49d955a57998d043c225e3023ae691a79de37585bd43f0b06400120c3bdff1bb')
assert chain['status']=='PASS' and chain_receipt['actual_tool_result']['exit_code']==0 and chain_receipt['status']=='CLOSED'
for p,row in chain['full_metadata_and_source_pins'].items():
    now=pin(p,row['sha256']);assert now['identity']==row['identity'],p
groups=chain['derived_read_path_groups'];paths={p for items in groups.values()for p in items}
assert len(groups['offline_snapshot_complete_explicit_union'])==672 and len(paths)==38055
resolved={str(Path(p).resolve(strict=True))for p in paths}
path_hits=sorted(chosen&paths);resolved_hits=sorted(chosen&resolved)
inodes={(r['identity'][0],r['identity'][1])for r in rows};inode_hits=[]
for p in paths:
    actual=Path(p).resolve(strict=True)
    s=actual.stat()
    if stat.S_ISREG(s.st_mode)and(s.st_dev,s.st_ino)in inodes:inode_hits.append(p)
assert not path_hits and not resolved_hits and not inode_hits

# Root full-project metadata inventory provides all links. Independently check
# every supplied literal and normalized target now. nlink1 plus the Root full
# inode sweep excludes any other ordinary pathname sharing selected bytes.
links=inventory['symlinks'];incoming=[];link_identities={}
for r in links:
    p=Path(r['path']);ids=identity(p);assert stat.S_ISLNK(ids[2])and os.readlink(p)==r['text']
    target=str(p.resolve(strict=False));assert target==r['target']
    link_identities[str(p)]=ids
    if target in chosen:incoming.append(r)
assert len(links)==668 and not incoming and proof['no_project_symlinks_or_other_hardlinks_to_candidates']is True

before_maps6to9=[]
for i,day in enumerate(['20260927','20260928','20260928','20260928'],6):
    folder=ART/f'd4a-scattering-mesh12-picard-map{i}-{day}'
    for name in names:
        p=folder/name;before_maps6to9.append(dict(path=str(p),identity=identity(p)))
before_closed=[]
for i,day in enumerate(dates,1):
    folder=ART/f'd4a-scattering-mesh12-picard-map{i}-{day}'
    for name in ('closed_axial.xsm','closed_snapshots.xsm'):
        p=folder/name;before_closed.append(dict(path=str(p),identity=identity(p)))

assert before_candidates=={p:identity(p)for p in chosen}
assert link_identities=={p:identity(p)for p in link_identities}
for row in before_maps6to9+before_closed:assert identity(row['path'])==row['identity']
for p,row in PINS.items():assert identity(p)==row['identity']
report=dict(schema='SPOT_R20_FIXED30_EARLY_MESH12_INTERMEDIATE_CURRENT_DEPENDENCY_READONLY_REVIEW_V1',status='PASS',
    scope='Current full INPUT/native/producer readchain and all link exclusions only; result/source/recovery semantics reviewed by complementary peer.',
    Root_full_byte_proof_pin=PINS[str(R/'proposed_candidates_full_byte_proof.json')],
    Root_full_byte_tool_reported=dict(initial_chunk_id='3c8b45',session_id=76019,terminal_chunk_id='a956ce',exit_code=0,closed=True),
    candidate_count=30,candidates=rows,logical_bytes=2580841168,allocated_bytes_at_Root_fullbyte_observation=2580910080,
    original_manifest_fresh_pins=[PINS[r['path']]for r in proof['original_manifests']],
    current_index_hit_sets=hits,current_namespace_ancestor_hits=namespace_hits,
    native_and_prepare_offline672_fullsource_pin_inherited=True,complete_static_read_path_count=38055,
    exact_dynamic_read_hits=path_hits,resolved_read_hits=resolved_hits,physical_inode_read_hits=inode_hits,
    all36_source_metadata_pin_seven_identities_unchanged=True,
    original_current_entrypoint_source_calls=chain['entrypoint_proof'],original_native_new_parent_induction=chain['fresh_native_parent_induction'],
    physical_common_basis_fixed_paths=chain['physical_common_basis_verifier'],
    global668_symlink_literal_and_target_fresh_checked=True,global_incoming_symlink_hits=incoming,
    all30_nlink1_no_other_file_hardlinks=True,global_other_hardlink_scan_Root_proof_bound=True,
    maps6to9_six_intermediate_classes_kept=before_maps6to9,all_early_closed_states_kept=before_closed,
    map6_candidate_radial_neutron_balance_source_explicitly_HOLD=True,
    same_declared_resource_roots_dynamic_capacity_not_immutable_old_filecount=True,
    bootstrap_closed_last_maps_and_all_results_sources_logs_manifests_recovery_masters_not_selected=True,
    old_whole_stage_revalidation_requires_isolated_recomputation=True,
    candidate_numeric_payload_full_reads_by_this_reader=0,old35GB_full_reads_by_this_reader=0,
    prior_R18_and_R19_retired_ranges_not_reselected=True,
    deletion_approval_requires_complementary_source_results_recovery_PASS_and_Root_fixed_preflight=True,
    approved_deletion_candidates_by_this_partial_scope_only=[],project_written=False,files_deleted=0,business_executed=False,
    native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,scientific_qualification=False,
    small_fresh_read_pins=PINS,elapsed_seconds=time.monotonic()-START)
with(D/'REPORT.json').open('x')as f:json.dump(report,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
with(D/'REPORT.txt').open('x')as f:
    f.write('第20轮固定30份旧mesh12迭代中间物：当前依赖范围 PASS。\nmap1..5各6份 projected_proposal/candidate_radial/candidate_snapshots/candidate_axial/candidate_system/parent_for_checker，逻辑2,580,841,168B，Root全文校验时分配2,580,910,080B（约2.404GiB）。\n当前37395期望读取、37339组件、35647canonical、全部requirement符号路径、86namespace、186alias、445absence及graph精确字面值均无命中。原当前native/prepare的672离线展开与38055静态读取集合 exact/resolve/inode均无命中，36份依赖源/metadata鲜SHA与7身份保持；原运行只取新WORK父状态，不重验这些旧中间物。\n全668条项目链接文本与目标鲜核无incoming；30份nlink1，Root完整inode扫无其他硬链接。\n全部closed/bootstrap/map6..9保留；map6 candidate_radial作为历史径向balance来源继续HOLD。结果/日志/源码/原清单和恢复主本不在本轮候选。\n本报告只审当前依赖/链接，需互补结果与恢复关系PASS及Root固定预检才能退役。退役后原逐阶段wholemanifest重验需隔离重算；不承诺即时或未经验证的逐字节复现。\n本核验只读TMP，候选数值及旧35GB无新全文读，未删文件、改项目或运行业务，也不赋科学成功。\n')
print(json.dumps(dict(status='PASS',report=str(D/'REPORT.json'),sha256=hashlib.sha256((D/'REPORT.json').read_bytes()).hexdigest(),candidate_count=30,elapsed_seconds=report['elapsed_seconds'])))
