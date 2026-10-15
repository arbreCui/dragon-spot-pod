"""R19 current exact dependency exclusion only; no business/API or deletion."""
import ast,hashlib,json,os,stat,time
from pathlib import Path
D=Path('/private/tmp/spot_storage_nineteenth_current_graph_closed_state_review_20261009')
ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts';SRC=ROOT/'validation/axial_material'
PINS={};START=time.monotonic()
def identity(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p,wanted):
 p=Path(p);before=identity(p);assert stat.S_ISREG(before[2])and p.resolve(strict=True)==p
 raw=p.read_bytes();assert identity(p)==before and hashlib.sha256(raw).hexdigest()==wanted,str(p)
 PINS[str(p)]=dict(path=str(p),bytes=len(raw),sha256=wanted,identity=before);return raw
def read(p,wanted):return json.loads(pin(p,wanted))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()).hexdigest()

S=ART/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-admission-scipy-env-physical-basis-own-pid-peak-v9-20261009'
W=ART/'axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009'
B=Path('/private/tmp/axmat_v9_actual_cold_binding_graph_resource_independent_review_20261009/REPORT.json')
b=read(B,'03ebde650f63e045ae7a35f1018e02f787aac47fef28812a9a7a7fd719760e3c')
POST=Path('/private/tmp/spot_storage_review_eighteenth_graph_20261009/ACTUAL_POST_RETIREMENT_REPORT.json')
post=read(POST,'08ddf7e740c49cd9ca8962c35b5a557ae6e09773bf4628ddd9ba81852a55ebb0')
m=read(S/'rank1_factor_cache_admission.json','564592df0acffc7bbc2c0743cd1b4849db859ec7e83b6101def72ce4a5175742')
expected={**m['files'],**b['additional_expected_files']}
assert len(m['files'])==37339 and len(expected)==37395 and digest(expected)==post['current_expected37395_complete_sha256']
GRAPH=ART/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009/input_graph.json'
graph=read(GRAPH,'0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3')
canonical={r['path']for r in graph['canonical_files']};assert len(canonical)==35647
ns_roots={r[k]for r in graph['namespaces']for k in('root','canonical_root')};assert len(graph['namespaces'])==86
aliases={r[k]for r in graph['aliases']for k in('path','target')};assert len(graph['aliases'])==186
assert len(graph['absence_inputs'])==len(graph['absence_observations'])==445
strings=set();stack=[graph]
while stack:
 v=stack.pop()
 if type(v)is str:strings.add(v)
 elif type(v)is list:stack.extend(v)
 elif type(v)is dict:strings.update(v.keys());stack.extend(v.values())

# Exact narrowed family/epoch policy, with three final closed snapshots retained.
families=[('axial-material-production-qualified-AB-white-trace-20261004',11),
 ('axial-material-production-qualified-AB-rank1-factor-cache-20261007',12),
 ('axial-material-production-qualified-AB-compensated-20261004',4)]
raw=[];links=[];kept=[];statuspins=[]
for family,last in families:
 root=ART/family;status=read(root/'AAA/run_status.json',hashlib.sha256((root/'AAA/run_status.json').read_bytes()).hexdigest())
 maps=status['cases']['AAA']['maps'];assert len(maps)==last and [r['epoch']for r in maps]==list(range(1,last+1))
 assert status['classification']=='WAITING_REFERENCE'and all(r['classification']=='VALID_NOT_MET'for r in maps[:-1])and maps[-1]['classification']=='VALID_MET'
 statuspins.append(PINS[str(root/'AAA/run_status.json')])
 for n in range(1,last-2):
  path=root/'AAA'/f'map{n:03d}'/'closed_snapshots.xsm';ids=identity(path)
  assert stat.S_ISREG(ids[2])and ids[6]==1 and path.resolve(strict=True)==path
  resultpath=path.parent/'result.json';result_raw=resultpath.read_bytes();resultsha=hashlib.sha256(result_raw).hexdigest();result=read(resultpath,resultsha)
  assert set(result)=={'classification','sha256'}and result['classification']=='SEALED_STAGE_OUTPUTS'
  assert 'closed_snapshots.xsm'in result['sha256'];wanted=result['sha256']['closed_snapshots.xsm']
  assert type(wanted)is str and len(wanted)==64
  raw.append(dict(path=str(path),identity=ids,logical_bytes=ids[3],allocated_bytes=path.lstat().st_blocks*512,
   original_expected_SHA256=wanted,original_seal=dict(path=str(resultpath),sha256=resultsha,field='sha256.closed_snapshots.xsm'),
   family=family,epoch=n,actual_closed_stage_manifest=True,fresh_payload_SHA_read=False))
  alias=root/'AAA'/f'map{n+1:03d}'/'parent_snapshots_closed.xsm';lids=identity(alias)
  assert stat.S_ISLNK(lids[2])and os.readlink(alias)==str(path)and alias.resolve(strict=True)==path
  links.append(dict(path=str(alias),identity=lids,logical_bytes=lids[3],allocated_bytes=alias.lstat().st_blocks*512,
   literal_link_text=os.readlink(alias),target=str(path),family=family,epoch=n+1))
 for n in range(last-2,last+1):
  path=root/'AAA'/f'map{n:03d}'/'closed_snapshots.xsm';kept.append(dict(path=str(path),identity=identity(path),reason='Last three closed states; preserve last two maps and their incoming parent target.'))
 assert (root/'AAA/bootstrap/closed_snapshots.xsm').is_file()

allselected={r['path']for r in raw+links};assert len(raw)==len(links)==18 and len(allselected)==36
checks={};blocked=[]
for r in raw+links:
 p=r['path'];hits=dict(binding_files=p in expected,canonical=p in canonical,alias_endpoint=p in aliases,
  graph_literal=p in strings,namespace_roots=[root for root in ns_roots if Path(p).is_relative_to(root)],
  absence_observation=p in graph['absence_inputs']or p in graph['absence_observations'])
 checks[p]=hits
 if any(v for v in hits.values()):blocked.append(dict(path=p,current_hits=hits))

# A bounded full-family symlink scan catches all incoming old parent references;
# Root separately scans the whole project687 links before any approval/apply.
inbound={r['path']:[]for r in raw}
for family,last in families:
 for base,dirs,files in os.walk(ART/family,followlinks=False):
  for name in dirs+files:
   p=Path(base)/name
   if p.is_symlink():
    target=str(p.resolve(strict=True))
    if target in inbound:inbound[target].append(str(p))
unknown_incoming={p:rows for p,rows in inbound.items()if set(rows)!={r['path']for r in links if r['target']==p}}

consumer=SRC/'cold_component_input_consumer_last_cprime_trim_own_pid_peak.py'
ct=pin(consumer,'2fa0cb00ec458e9bbbbdf2f15db703a1c0547b08d35f585b6c7e6e6274d06d59').decode()
defs={n.name:n for n in ast.parse(ct).body if isinstance(n,ast.FunctionDef)}
current_functions=[]
for name in ('original_ordinary_paths','current_component_paths','current_checks','current_cold_binding','complete_input_phase','expected_union'):
 node=defs[name];segment=ast.get_source_segment(ct,node)
 current_functions.append(dict(name=name,line=node.lineno,complete_source_sha256=hashlib.sha256(segment.encode()).hexdigest()))
assert 'original_component_APIs_executed_in_this_process=False'in ast.get_source_segment(ct,defs['complete_input_phase'])
prior=ART/'axial-material-physical-dedup-combined-runtime-build-20261007/declaration.json'
p=read(prior,'aa3e33a10b64deb947f82fd9f8b19559f9f700f58396e641a4e66def5d4b46a4')
ordinaryhits=sorted(allselected.intersection(p['files']))
ordinary_ns_hits=sorted(pth for pth in allselected if any(Path(pth).is_relative_to(row['root'])for row in p['component_namespaces']))
prepared=read(W/'prepared_cold.json','1290a19501ba7801deafe351407b244bd32f71a6cf0d010d4a14fd64e61d8b3e')
resources_membership={family:[root for root in prepared['resource_roots']if (ART/family).is_relative_to(root)]for family,last in families}

# Fixed current index field names: binding's actual key is files, not expected_files.
indices=dict(binding=dict(path=str(W/'own_rss_binding.json'),sha256='4e8de93043fa08ac0c6e1f1702b69606a6bf0b155c30007c356ec4837919c930',field='files',count=37395),
 component_metadata=dict(path=str(S/'rank1_factor_cache_admission.json'),sha256='564592df0acffc7bbc2c0743cd1b4849db859ec7e83b6101def72ce4a5175742',field='files',count=37339),
 independent_extra56=dict(path=str(B),sha256=PINS[str(B)]['sha256'],field='additional_expected_files',count=56),
 graph=dict(path=str(GRAPH),sha256=PINS[str(GRAPH)]['sha256'],canonical_field='canonical_files',canonical_count=35647,
  namespaces_field='namespaces',namespace_count=86,aliases_field='aliases',alias_count=186,
  absence_fields=['absence_inputs','absence_observations'],absence_count=445,requirements_field='requirements',logical_requirement_rows=235528))
for row in raw+links+kept:assert identity(row['path'])==row['identity']
for path,row in PINS.items():assert identity(path)==row['identity']
status='CURRENT_INDEX_EXCLUDED_PENDING_GLOBAL_LINK_RESTORE_AND_ORIGINAL_SOURCE_REVIEW'if not blocked and not unknown_incoming and not ordinaryhits and not ordinary_ns_hits else 'HOLD_CURRENT_OR_INCOMING_DEPENDENCY'
report=dict(schema='SPOT_R19_OLD_EARLY_AAA_CLOSED_STATES_CURRENT_EXACT_DEPENDENCY_READONLY_REVIEW_V1',status=status,
 current_read_indices=indices,independently_derived_expected37395_SHA256=digest(expected),proposed_regular18=raw,proposed_related_symlink18=links,
 proposed_regular_logical_bytes=sum(r['logical_bytes']for r in raw),proposed_regular_allocated_bytes=sum(r['allocated_bytes']for r in raw),
 preserve_last_three_closed_snapshots=kept,preserve_last_two_complete_maps_and_all_bootstrap=True,current_path_checks=checks,
 current_blockers=blocked,unknown_family_incoming_symlinks=unknown_incoming,ordinary26784_file_hits=ordinaryhits,ordinary_namespace_hits=ordinary_ns_hits,
 candidate_families_within_original_dynamic_resource_roots=resources_membership,
 resource_membership_is_live_capacity_gate_not_frozen_payload_inventory=True,
 current_source_complete_functions=current_functions,
 current_read_chain_scope='Current consumer complete_input_phase freshly checks full graph and expected_union plus original26784 ordinary files/namespaces, current component library/working-snapshot/absence predicates, member predicates derived by full graph and failed namespace scope, genuine cold MRO and dynamic resource caps. It does not reexecute old component APIs or old production map manifests. Candidate-specific whole future native snapshot admission path proof and prior restore/global incoming symlink proof remain complementary scopes.',
 original_result_manifest_semantics='Per-map result.json.sha256 is the original SEALED_STAGE_OUTPUTS map; there is no independent result.sha256 text file in these map directories.',
 fresh_candidate_payload_SHA_reads=0,old35GB_rehashed=False,approved_deletion_candidates=[],files_deleted=0,project_written=False,business_executed=False,
 candidate_dependency_final_approval=False,required_remaining=['Root global incoming symlink inventory','Peer original result/source/recomputability and prior restore-master intersections','Fresh fullSHA against each original result.json.sha256 before any retirement'],
 full_small_metadata_and_source_pins=PINS,elapsed_seconds=time.monotonic()-START)
out=D/'REPORT.json'
with out.open('x')as f:json.dump(report,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
with (D/'REPORT.txt').open('x')as f:f.write('旧AAA早期closed状态当前依赖审计\n状态：'+status+'\n固定范围18个常规closed_snapshots.xsm与18个下一map的parent symlink。最后3个closed、最后2个map及全部bootstrap保留。\n当前绑定真实字段为files（37395）；metadata.files为37339。当前canonical35647、namespace86、alias186、absence445与原ordinary26784逐项排除结果见机器报告。\n本次未读取4GB候选payload或35GB当前科学数据，未运行任何科学业务、未改项目、未删除。尚待全项目incoming links/旧恢复主本/原生产重算证据和候选全文SHA，未批准删除。\n')
print(json.dumps(dict(status=status,regular_count=len(raw),symlink_count=len(links),current_blockers=len(blocked),unknown_family_incoming=len(unknown_incoming),report=str(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest())))
