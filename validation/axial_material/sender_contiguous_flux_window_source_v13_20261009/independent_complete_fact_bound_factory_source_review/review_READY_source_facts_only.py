"""Read/hash/AST only; no candidate, helper, controls or auditor import/call."""
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import struct

D=Path('/private/tmp/axmat_v13_full86_READY_fact_binding_independent_review_20261009')
READY_DIR=Path('/private/tmp/axmat_v13_full_sender_window_component_READY_source_candidates_20261009')
DRAFT_DIR=Path('/private/tmp/axmat_v13_full_sender_window_component_source_draft_20261009')
AM=Path('/Users/wen/spot/validation/axial_material')
READY=READY_DIR/'prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py'
DRAFT=DRAFT_DIR/READY.name
OLD=AM/'prepare_qualified_AB_rank1_factor_cache_cross_group_identity_key_delta_production.py'
PROOF=READY_DIR/'Root_complete_source_fact_binding_proof.json'
PRIOR=Path('/private/tmp/axmat_v13_full86_factory_source_independent_review_20261009')
EXACT={READY:'d2d2c7616d329cd8ffbf30f749de6ef8ae08d294240b653cfe8b92a3fe1c8633',
       DRAFT:'a6dd0796316aec5b6c16ff73677c689a7e7146697759a0cde9187be962807821',
       OLD:'f136baab5047a8727cfd2c0abb5399acf617c25c4f4e7692242419e6f9daef4e',
       PROOF:'6e9cdb78e26aacbdf1ae6193cf5a9d5cea6b80de5bdf21087323524ac8a34357',
       PRIOR/'REPORT.json':'3c94602d87625c1f40a67e463eb44084534076cd63bde2e5ba00e89e5654f8a4',
       PRIOR/'actual_readonly_tool_return.json':'e7c9c75cec53051071896fd095f8292877a123ab4c9f625b286f3257e5f77d05'}
SOURCE_PATHS={
 'SENDER_PATCH_HELPER_SHA':AM/'sender_contiguous_flux_window_patch_v13.py',
 'CANDIDATE_SENDER_SHA':AM/'sender_contiguous_flux_window_source_v13_20261009/FLU2DR64.f',
 'SENDER_SOURCE_PROOF_SHA':AM/'sender_contiguous_flux_window_source_v13_20261009/source_patch_proof.json',
 'SENDER_SOURCE_INPUT_SHA':AM/'sender_contiguous_flux_window_source_v13_20261009/source_admission_INPUT.json',
 'SENDER_CONTROL_SOURCE_SHA':AM/'sender_contiguous_flux_window_observer_controls_v13.f90',
 'SENDER_CONTROL_CONTRACT_SHA':AM/'sender_contiguous_flux_window_source_v13_20261009/wrapper_control_contract.json',
 'SENDER_CONTROLS_AUDITOR_SHA':AM/'sender_contiguous_flux_window_controls_audit_v13.py'}
def sha(b):return hashlib.sha256(b).hexdigest()
def identity(p):
 s=p.stat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def unique(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('duplicate JSON key: '+k)
  d[k]=v
 return d
def load(b):return json.loads(b,object_pairs_hook=unique,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))
files=list(EXACT)+[DRAFT_DIR/'composition_regions.json']+list(SOURCE_PATHS.values())
assert len(files)==len(set(files))
for p in files:assert p.is_absolute() and not p.is_symlink() and p.is_file() and p.stat().st_nlink==1,str(p)
before={str(p):identity(p) for p in files}
raw={str(p):p.read_bytes() for p in files}
pins={str(p):dict(path=str(p),sha256=sha(raw[str(p)]),size_bytes=len(raw[str(p)]),identity=before[str(p)]) for p in files}
for p,want in EXACT.items():assert pins[str(p)]['sha256']==want,str(p)
proof=load(raw[str(PROOF)])
assert proof['schema']=='AXMAT_ROOT_V13_FULL_FACTORY_COMPLETE_SOURCE_FACT_BINDING_V1'
assert proof['status']=='READY_SOURCE_ONLY_FOR_INDEPENDENT_REVIEW'
assert proof['draft']==dict(path=str(DRAFT),sha256=EXACT[DRAFT])
assert proof['candidate']==dict(path=str(READY),sha256=EXACT[READY])
assert proof['source_parent']==dict(path=str(OLD),sha256=EXACT[OLD])
texts={p:raw[str(p)].decode('utf-8') for p in [READY,DRAFT,OLD]}
trees={p:ast.parse(s) for p,s in texts.items()}
def constants(t):
 d={}
 for n in t.body:
  if isinstance(n,ast.Assign):
   for x in n.targets:
    if isinstance(x,ast.Name):d[x.id]=n.value
 return d
c=constants(trees[READY]);dc=constants(trees[DRAFT])
def segments(t,s):
 lines=s.splitlines(keepends=True);d={}
 def walk(n,prefix=''):
  for x in ast.iter_child_nodes(n):
   if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
    k=prefix+x.name;d[k]=''.join(lines[x.lineno-1:x.end_lineno]);walk(x,k+'.')
   else:walk(x,prefix)
 walk(t);return d
rseg=segments(trees[READY],texts[READY]);dseg=segments(trees[DRAFT],texts[DRAFT])
assert len(rseg)==len(dseg)==96 and rseg==dseg
assert not any(isinstance(n,ast.ClassDef) for n in ast.walk(trees[READY]))
edits=proof['source_binding_edits'];assert len(edits)==proof['source_binding_edit_count']==11
allowed=set(SOURCE_PATHS)|{'complete_normalized_layout','source_status','stage_order_doc','source_binding_doc'}
assert {e['name'] for e in edits}==allowed
unbound=texts[READY]
edit_summary=[]
for e in reversed(edits):
 assert e['count']==1 and unbound.count(e['after'])==1,e['name']
 unbound=unbound.replace(e['after'],e['before'],1)
 edit_summary.append(dict(name=e['name'],before_sha256=sha(e['before'].encode()),after_sha256=sha(e['after'].encode())))
assert unbound==texts[DRAFT]
regions=load(raw[str(DRAFT_DIR/'composition_regions.json')])
if isinstance(regions,dict):regions=regions['regions']
assert len(regions)==proof['parent_region_count']==32
assert regions==proof['source_parent_composition_regions']
inverse=unbound
for e in reversed(regions):
 assert inverse.count(e['after'])==e['count'],e['name']
 inverse=inverse.replace(e['after'],e['before'],e['count'])
assert inverse==texts[OLD]

def typed_order_equal(a,b,where='root'):
 assert type(a) is type(b),(where,type(a).__name__,type(b).__name__)
 if isinstance(a,dict):
  assert list(a)==list(b),(where,'key order')
  for k in a:typed_order_equal(a[k],b[k],where+'.'+k)
 elif isinstance(a,list):
  assert len(a)==len(b),where
  for i,(x,y) in enumerate(zip(a,b)):typed_order_equal(x,y,where+'['+str(i)+']')
 elif isinstance(a,float):assert struct.pack('>d',a)==struct.pack('>d',b),where
 else:assert a==b,where

source_records={}
for name,p in SOURCE_PATHS.items():
 bound=ast.literal_eval(c[name]);assert bound==pins[str(p)]['sha256'],name
 assert ast.literal_eval(dc[name]) is None,name
 actual=dict(path=str(p),sha256=bound,identity=before[str(p)])
 assert proof['source_inputs_before'][name]==proof['source_inputs_after'][name]==actual,name
 source_records[name]=actual
assert set(proof['source_inputs_before'])==set(proof['source_inputs_after'])==set(SOURCE_PATHS)
contract=load(raw[str(SOURCE_PATHS['SENDER_CONTROL_CONTRACT_SHA'])])
normalized=copy.deepcopy(contract)
for name in ['source_driver','reference_unit']:
 assert set(normalized[name])=={'path','sha256','size_bytes','identity'}
 del normalized[name]['path'];del normalized[name]['identity']
layout=ast.literal_eval(c['SENDER_CONTROL_LAYOUT'])
typed_order_equal(layout,normalized)
typed_order_equal(load(proof['normalized_layout']),normalized)
assert contract['source_driver']['sha256']==ast.literal_eval(c['SENDER_CONTROL_SOURCE_SHA'])
assert contract['source_driver']['size_bytes']==pins[str(SOURCE_PATHS['SENDER_CONTROL_SOURCE_SHA'])]['size_bytes']
assert layout['compiler_or_control_execution_performed'] is False and layout['actual_outputs'] is None
assert layout['planned_counts_not_actual']['wrapper_calls_total']==48
assert layout['planned_counts_not_actual']['raw_files_total']==70
assert layout['planned_counts_not_actual']['raw_bytes_total']==288241824
assert ast.literal_eval(c['SOURCE_STATUS'])=='READY_SOURCE_ONLY_FOR_ROOT_REVIEWED_COMPONENT_EXECUTION'
assert ast.literal_eval(c['ORIGINAL_STAGE_COUNT'])==68 and ast.literal_eval(c['COMPLETE_STAGE_COUNT'])==86
for k in ['FUTURE_ACTUAL_BUILD_TERMINAL_SHA','FUTURE_ACTUAL_BUILD_SEAL_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']:
 assert ast.literal_eval(c[k]) is None,k
for k in ['ARCHIVE_RESERVE','HISTORY_CAP','FREE_FLOOR','TAIL_FIELDS','FAMILY','SENDER_MODES']:
 assert ast.dump(c[k],include_attributes=False)==ast.dump(dc[k],include_attributes=False),k
caps=[n for n in trees[READY].body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Tuple)
      and [x.id for x in n.targets[0].elts]==['TOTAL_WALL','STAGE_WALL','RSS_CAP']]
assert len(caps)==1 and ast.literal_eval(caps[0].value)==(1800,600,512)
prior=load(raw[str(PRIOR/'REPORT.json')]);pr=load(raw[str(PRIOR/'actual_readonly_tool_return.json')])
assert prior['status']=='PASS_SOURCE_ONLY_UNREADY' and prior['original_math_real_kernel_invocations']==2710
assert pr['actual_tool_terminal_return_observed'] is True and type(pr['actual_tool_result']['exit_code']) is int
assert pr['actual_tool_result']['exit_code']==0 and pr['actual_tool_result']['closed'] is True
for k in ['compiled','component_controls_executed','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted']:
 assert proof[k] is False,k
newroots=[Path('/Users/wen/spot/validation/artifacts')/name for name in
 ['axial-material-qualified-AB-sender-contiguous-flux-window-build-admission-v13-20261009',
  'axial-material-sender-contiguous-flux-window-build-v13-20261009',
  'axial-material-qualified-AB-sender-contiguous-flux-window-build-terminal-v13-20261009']]
assert all(not os.path.lexists(p) for p in newroots)
assert before=={str(p):identity(p) for p in files}
D.mkdir(parents=True,exist_ok=True)
evidence=dict(schema='AXMAT_V13_READY_SOURCE_FACTS_COMPLETE_STATIC_EVIDENCE_V1',
 fresh_full_SHA_and_7identity=pins,source_records=source_records,
 binding_regions=list(reversed(edit_summary)),inverse_binding_to_draft=True,inverse_draft_to_f136=True,
 all96_segments={name:sha(s.encode()) for name,s in rseg.items()},
 normalized_full_typed_order_floatbits_equal=True,normalized_contract_sha256=sha(json.dumps(normalized,separators=(',',':'),allow_nan=False).encode()),
 deleted_descriptor_fields_only=['source_driver.path','source_driver.identity','reference_unit.path','reference_unit.identity'],
 metadata_and_source_7identity_before_after_equal=True,newroots_absent=[str(p) for p in newroots])
with (D/'complete_fresh_fact_binding_evidence.json').open('x') as f:json.dump(evidence,f,indent=2,allow_nan=False);f.write('\n')
report=dict(schema='AXMAT_V13_READY_FULL86_FACTORY_SOURCE_BINDING_INDEPENDENT_REVIEW_V1',status='PASS_SOURCE_BINDING_ONLY',
 candidate=pins[str(READY)],root_fact_binding_proof=pins[str(PROOF)],
 exact_binding_regions=11,exact_full_parent_regions=32,complete_function_class_segments_unchanged=96,
 seven_source_fullSHA_7identity_before_after_equal=True,whole_normalized_contract_typed_order_floatbits_equal=True,
 original_control_audit_and_archive_forecast_byteexact_inherited=True,
 complete_stage_count=86,original_stage_count=68,real_SPOT_kernel_calls_separate=2710,planned_wrapper_stub_calls_separate=48,
 budgets_unchanged=True,future_actual_seal_terminal_native_pins_None=True,newartifactroots_absent=True,
 source_ready_does_not_mean_component_controls_or_RSS_pass=True,source_blockers=[],
 root_binder_tool_facts_as_supplied_by_Root=[dict(chunk_id='9ecf8e',exit_code=1,closed=True,
   reason='purebinder incorrect UNREADY literal assertion; no business function changed or retried'),
   dict(chunk_id='0328bf',exit_code=0,closed=True)],
 business_imported=False,candidate_called=False,compile_or_fixture_executed=False,project_written=False,
 actual_component_controls_passed=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,
 evidence_files=['complete_fresh_fact_binding_evidence.json'],actual_readonly_terminal_return=None)
with (D/'REPORT.json').open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
with (D/'REPORT.txt').open('x') as f:f.write('完整 SOURCE 事实绑定独审通过：7 个真实文件全 SHA/7 身份前后稳定；规范化完整契约仅去掉两个源 descriptor 各 path/identity 后，类型、字段顺序与浮点位精确相等。11 区域整逆 a6dd，继续 32 区域整逆 f136，96 函数/类源码段完全未改。READY 仅允许 Root 后续真实组件执行，尚无新构建/68+18 控制、RSS、native、AAA 或 ABA 通过信用。Root 首次纯 binder 断言错误真1与修正后真0作为 Root 提供事实如实区分，未业务重试。本审仅 STDlib 鲜读/哈希/AST，不调用任何业务。\n')
print(json.dumps(dict(status=report['status'],REPORT_path=str(D/'REPORT.json'),REPORT_sha256=sha((D/'REPORT.json').read_bytes()),all96_segments_exact=True,all7_sources_fresh_and_stable=True,binding_region_count=11,parent_region_count=32),allow_nan=False))
