"""Independent STDlib source-only review. Never import or call a factory."""
import ast
import hashlib
import json
import os
from pathlib import Path

D = Path('/private/tmp/axmat_v13_full86_factory_source_independent_review_20261009')
CAND = Path('/private/tmp/axmat_v13_full_sender_window_component_source_draft_20261009')
AM = Path('/Users/wen/spot/validation/axial_material')
OLD = AM / 'prepare_qualified_AB_rank1_factor_cache_cross_group_identity_key_delta_production.py'
NEW = CAND / 'prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py'
OLD_SHA = 'f136baab5047a8727cfd2c0abb5399acf617c25c4f4e7692242419e6f9daef4e'
NEW_SHA = 'a6dd0796316aec5b6c16ff73677c689a7e7146697759a0cde9187be962807821'
AUDITOR_SHA = '64262e89bd2adf13260a8d0f643c31d709f84665e5e9223cdd2969ab78a721e1'
DRIVER_SHA = '053747437865119be4fdd5d8eb466c96a85d8cf22f6d9cdcceebe19bc47352bb'
ART = Path('/Users/wen/spot/validation/artifacts')
OLD_OUT = ART / 'axial-material-rank1-factor-cache-cross-group-identity-key-delta-build-v11-20261009'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def identity(p):
    s = p.stat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

files = [OLD, NEW, CAND/'composition_regions.json', CAND/'source_complete_inverse_proof.json',
         CAND/'REPORT.json', CAND/'actual_source_tool_terminal_returns.json', CAND/'small_source_manifest.json',
         AM/'sender_contiguous_flux_window_controls_audit_v13.py',
         AM/'sender_contiguous_flux_window_observer_controls_v13.f90',
         AM/'sender_contiguous_flux_window_source_v13_20261009/wrapper_control_contract.json',
         OLD_OUT/'declaration.json', OLD_OUT/'audit/controls.json', OLD_OUT/'seal.json']
before = {str(p): identity(p) for p in files}
raw = {str(p): p.read_bytes() for p in files}
pins = {str(p): dict(sha256=sha(raw[str(p)]), size_bytes=len(raw[str(p)]), identity=before[str(p)]) for p in files}
assert pins[str(OLD)]['sha256'] == OLD_SHA
assert pins[str(NEW)]['sha256'] == NEW_SHA
assert pins[str(AM/'sender_contiguous_flux_window_controls_audit_v13.py')]['sha256'] == AUDITOR_SHA
assert pins[str(AM/'sender_contiguous_flux_window_observer_controls_v13.f90')]['sha256'] == DRIVER_SHA
old = raw[str(OLD)].decode('utf-8'); new = raw[str(NEW)].decode('utf-8')
ot = ast.parse(old); nt = ast.parse(new)

def defs(tree, text):
    result = {}
    lines = text.splitlines(keepends=True)
    def walk(node, prefix=''):
        for item in ast.iter_child_nodes(node):
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                name = prefix + item.name
                result[name] = (item, ''.join(lines[item.lineno-1:item.end_lineno]))
                walk(item, name+'.')
            else:
                walk(item, prefix)
    walk(tree)
    return result

od, nd = defs(ot, old), defs(nt, new)
assert len(od) == 81 and len(nd) == 96
assert not any(isinstance(n, ast.ClassDef) for n in ast.walk(nt))
changed = sorted(k for k in od if od[k][1] != nd[k][1])
assert changed == sorted(['require_ready','source_inputs','stage_commands','stage_labels','prepare_build',
    'declaration_admission','check_watch','expected_stage_exit','stage_outcome_valid','binary_audit',
    'audit_build','run_build','production_admission'])
unchanged = sorted(set(od) - set(changed))
assert len(unchanged) == 68
for k in ['control_audit','archive_forecast','patch_admission','cache_accounting',
          'production_cache_shape_forecast','helper','resources_for',
          'environment','external_terminal_admission','strict_terminal_json','terminal_file']:
    assert od[k][1] == nd[k][1], k

regions = json.loads(raw[str(CAND/'composition_regions.json')])
if type(regions) is dict:
    regions = regions['regions']
assert len(regions) == 32
restored = new; region_proof = []
for r in reversed(regions):
    assert restored.count(r['after']) == r['count'], r['name']
    restored = restored.replace(r['after'], r['before'], r['count'])
    region_proof.append(dict(name=r['name'], count=r['count'],
        before_sha256=sha(r['before'].encode()), after_sha256=sha(r['after'].encode())))
assert restored == old and sha(restored.encode()) == OLD_SHA

def dump(n):
    return ast.dump(n, include_attributes=False)

def returns(name, table):
    return next(n.value for n in table[name][0].body if isinstance(n, ast.Return))

# Project the sole new sender list from stage_commands, retaining each old AST expression.
nr = returns('stage_commands', nd); orr = returns('stage_commands', od)
assert isinstance(nr, ast.List) and isinstance(orr, ast.List)
extra = [x for x in nr.elts if 'sender_control_contract' in ast.unparse(x)]
assert len(extra) == 1
projected = ast.List(elts=[x for x in nr.elts if x not in extra], ctx=ast.Load())
assert dump(projected) == dump(orr)
def add_terms(n):
    if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add):
        return add_terms(n.left)+add_terms(n.right)
    return [n]
nl = add_terms(returns('stage_labels', nd)); ol = add_terms(returns('stage_labels', od))
sender_terms = [x for x in nl if 'sender_control_contract' in ast.unparse(x)]
assert len(sender_terms) == 1
assert [dump(x) for x in nl if x not in sender_terms] == [dump(x) for x in ol]

def command_parts(node):
    bases = [n.value for n in node.body if isinstance(n, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id=='commands' for t in n.targets)]
    extensions = [n.value.args[0] for n in node.body if isinstance(n, ast.Expr)
        and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Attribute)
        and isinstance(n.value.func.value, ast.Name) and n.value.func.value.id=='commands'
        and n.value.func.attr=='extend']
    inserts = [n.value for n in node.body if isinstance(n, ast.Expr)
        and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Attribute)
        and isinstance(n.value.func.value, ast.Name) and n.value.func.value.id=='commands'
        and n.value.func.attr=='insert']
    return bases, extensions, inserts
ob, oe, oi = command_parts(od['prepare_build'][0]); nb, ne, ni = command_parts(nd['prepare_build'][0])
assert len(ob)==len(nb)==1 and dump(ob[0])==dump(nb[0])
assert len(oe)==1 and len(ne)==2 and dump(oe[0])==dump(ne[0])
assert len(oi)==0 and len(ni)==1 and ast.literal_eval(ni[0].args[0])==1
assert len(ob[0].elts)==6 and len(oe[0].elts)==2 and len(ne[1].elts)==3
assert 'FLU2DR64.f' in ast.unparse(ni[0].args[1])
assert all(n not in ast.unparse(ne[1]) for n in ['candidate_unit','SPOF64.o'])
assert all(n in ast.unparse(ne[1]) for n in ['FLU2DR64.o','FLUSP64.original_reference_unit.o',
    'sender_window_controls.o','libGanlib.a'])

tops = {}
for node in nt.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name): tops[target.id] = node.value
for name in ['SENDER_PATCH_HELPER_SHA','CANDIDATE_SENDER_SHA','SENDER_SOURCE_PROOF_SHA',
             'SENDER_SOURCE_INPUT_SHA','SENDER_CONTROL_SOURCE_SHA','SENDER_CONTROL_CONTRACT_SHA',
             'SENDER_CONTROLS_AUDITOR_SHA','SENDER_CONTROL_LAYOUT',
             'FUTURE_ACTUAL_BUILD_TERMINAL_SHA','FUTURE_ACTUAL_BUILD_SEAL_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']:
    assert ast.literal_eval(tops[name]) is None, name
assert ast.literal_eval(tops['SOURCE_STATUS']).startswith('UNREADY')
assert ast.literal_eval(tops['ORIGINAL_STAGE_COUNT']) == 68
assert ast.literal_eval(tops['COMPLETE_STAGE_COUNT']) == 86
for root in [ART/'axial-material-qualified-AB-sender-contiguous-flux-window-build-admission-v13-20261009',
             ART/'axial-material-sender-contiguous-flux-window-build-v13-20261009',
             ART/'axial-material-qualified-AB-sender-contiguous-flux-window-build-terminal-v13-20261009']:
    assert not os.path.lexists(root), str(root)

contract = json.loads(raw[str(AM/'sender_contiguous_flux_window_source_v13_20261009/wrapper_control_contract.json')])
modes = ast.literal_eval(tops['SENDER_MODES'])
assert [c['name'] for c in contract['cases']] == list(modes) and len(modes)==14
assert contract['source_driver']['sha256']==DRIVER_SHA
assert contract['compiler_or_control_execution_performed'] is False and contract['actual_outputs'] is None
raw_count=0; raw_bytes=0; steps=0; positivecalls=0
for i,c in enumerate(contract['cases']):
    assert c['args']==[c['name']] and c['expected_returncode']==(0 if i<10 else 1)
    assert c['negative'] is (i>=10)
    assert (c['nun'],c['ngrp'])==((1800,370) if c['name']=='all' else (12,1 if c['name']=='scalar_one' else 8))
    cases_steps=c['steps'] if i<10 else [dict(step=1,active_groups=c['ngrp'] if c['name'].endswith('_active') else 0)]
    expected=[]
    for s in cases_steps:
        n,g,r,m,z,active=[c[k] for k in ['nun','ngrp','nreg','nmat','nmerg']]+[s['active_groups']]
        size=8*(18+g+2*r+m+r+4+z*g+8*n*g+2*active+n*active)+72
        for who in (['input','reference','candidate'] if i<10 else ['input']):
            expected.append(dict(name=c['name']+'.s'+str(s['step'])+'.'+who+'.bin',size_bytes=size,who=who))
    assert c['raw_files']==expected
    assert c['strict_case_namespace']==['execute.log','execute.watchdog.json','wrapper_manifest.jsonl']+[r['name'] for r in expected]
    raw_count+=len(expected); raw_bytes+=sum(r['size_bytes'] for r in expected)
    if i<10: steps+=len(cases_steps); positivecalls+=2*len(cases_steps)
assert (raw_count,raw_bytes,steps,positivecalls+4)==(70,288241824,22,48)
olddecl = json.loads(raw[str(OLD_OUT/'declaration.json')])
oldcontrols = json.loads(raw[str(OLD_OUT/'audit/controls.json')])
assert len(olddecl['build_commands'])==8
assert len(oldcontrols['counts'])==30 and oldcontrols['counts']['total_declared_stages']==68
c=olddecl['control_contract']
names=['positive']+['negative_'+x['name'] for x in c['negative_cases']+c['cap_negative_cases']]
names+=['memory_positive']+['memory_negative_'+x['name'] for x in c['memory_negative_cases']]
names+=['dedup_positive']+['dedup_negative_'+x['name'] for x in c['dedup_negative_cases']]
names+=['factor_positive']+['factor_negative_'+x['name'] for x in c['factor_negative_cases']]
names+=['keycodec_positive']+['keycodec_negative_'+x['name'] for x in c['keycodec_negative_cases']]
assert len(names)==59 and len(set(names))==59 and 12+59+14+1==86
build_map=[0,2,3,4,5,6,7,8]
stage_map=[dict(old_index=i,new_index=build_map[i]) for i in range(8)]
stage_map += [dict(old_index=8+i,new_index=12+i,label='controls/'+name+'/execute') for i,name in enumerate(names)]
stage_map += [dict(old_index=67,new_index=85,label='audit/audit')]
assert len(stage_map)==68 and len(set(r['new_index'] for r in stage_map))==68

evidence = {
 'full_inverse_regions': list(reversed(region_proof)),
 'all_definition_inventory': {name:dict(old_sha256=sha(od[name][1].encode()) if name in od else None,
    new_sha256=sha(pair[1].encode()),new_start_line=pair[0].lineno,
    old_start_line=od[name][0].lineno if name in od else None) for name,pair in nd.items()},
 'changed_original_definitions':changed,'unchanged_original_definitions':unchanged,
 'added_definitions':sorted(set(nd)-set(od)),
 'original68_to_new86_stage_mapping':stage_map,
 'new_stage_indices':[1,9,10,11]+list(range(71,85)),
 'source_gate_review':{
  'source_and_publicABI': [364,567], 'full_contract_no_defaults':[568,708],
  'forecast_original_allowance_and_complete_cap':[710,759],
  'commands_full_old_projection':[1095,1121], 'production_two_override_inverse':[1138,1143],
  'actual_fullsender_unit_link':[1162,1170], 'genuine_constructor_and_caps':[1188,1255],
  'declaration_revalidation':[1268,1323], 'raw_preacceptance_7identity':[2116,2188],
  'unchanged68_audit_and_separate_stubcounts':[2191,2203],
  'objects_symbols_real_production_and_unit_separation':[2206,2278],
  'actual_audit_child_stage_guard':[2282,2323], 'all_controls_true_once':[2367,2427],
  'postseal_four_tails':[2462,2474], 'Root_true0_fullstdout_binding':[2543,2578],
  'sealed_all_namespace_fresh_raw_reaudit':[2591,2685]},
 'source_review_conclusions':[
  'Old control_audit/archive_forecast and original mathematical/FP/cache functions are byte-exact.',
  '8 original builds retain exact base AST; additional compile inserted before production link and three unit builds appended.',
  'Original59 control commands and labels keep the complete AST and order; 14 sender modes occur before audit.',
  'Production link inverts both changed objects and output to original92 recipe; unit observer/reference objects excluded from production.',
  'Observer unit links actual complete production sender object, original reference wrapper and realGANLIB.',
  'Old30-field control count dictionary retained separately; wrapper48/observer34 never add to original realSPOT kernel count.',
  'Whole raw sender namespace SHA+7identity archived before acceptance, fresh before/after independent auditor and factory checks.',
  'Full sealed namespace, independent Root typed zero/full stdout/four tails mandatory for runtime input admission.',
  'Only original single1GiB nonraw allowance retained; full forecast adds all70 raw288241824 and complete newsource overhead below original2GiB.',
  'All7 newpins/layoutNone and UNREADY keep every execution blocked; no actual new component outcome has been inferred.'
 ]
}
after={str(p):identity(p) for p in files}
assert before==after
D.mkdir(parents=True, exist_ok=True)
for name,value in [('source_static_inverse_and_stage_evidence.json',evidence),('fresh_source_evidence_pins.json',pins)]:
    with (D/name).open('x') as f: json.dump(value,f,indent=2,allow_nan=False); f.write('\n')
report=dict(schema='AXMAT_V13_FULL86_FACTORY_INDEPENDENT_SOURCE_REVIEW_V1',
 status='PASS_SOURCE_ONLY_UNREADY',candidate=dict(path=str(NEW),sha256=NEW_SHA),
 mother=dict(path=str(OLD),sha256=OLD_SHA),full_byte_inverse=True,region_count=32,
 original_definitions=81,new_definitions=96,unchanged_original_definition_bodies=68,
 original_control_audit_and_archive_forecast_byteexact=True,original_stages=68,
 additional_build_stages=4,additional_sender_control_stages=14,complete_stages=86,
 original_math_real_kernel_invocations=oldcontrols['counts']['actual_total_unit_kernel_invocations'],
 original_counts_field_count=30,wrapper_calls_planned=48,observer_calls_planned=34,
 new_raw_files_planned=70,new_raw_bytes_planned=288241824,
 source_before_after_identity_equal=True,all_future_pins_None=True,new_roots_absent=True,
 source_blockers=[],required_before_Root_execution=['Bind and independently verify all7 exactnewsource SHA values and the whole normalized sender contract.','Root-only newsource status transition, no fixture or current business run credited by this review.'],
 budget_and_physics_unchanged=True,business_module_imported=False,candidate_or_auditor_called=False,
 compile_or_control_or_numeric_executed=False,project_written=False,
 actual_new_component_build_success=False,native_RSS_verified=False,
 AAA_accuracy_qualified=False,ABA_admitted=False,
 evidence_files=['source_static_inverse_and_stage_evidence.json','fresh_source_evidence_pins.json'],
 actual_readonly_tool_terminal_return=None)
with (D/'REPORT.json').open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
with (D/'REPORT.txt').open('x') as f:f.write('源审通过，候选仍为 UNREADY。32 区域完整逆回原 V11；原 68 阶段保留，增加 4 构建和 14 观察器控制，总 86。原控制审计、归档预测及数学计算函数保持字节一致。生产仅替换完整 sender 与 kernel 两对象，观察器/reference 只进入单元链接；全 raw namespace、7 身份、封存及独立 Root 真零退出/四 tails 仍为准入必要条件。7 新源 SHA 和完整 layout 尚为 None，执行被阻止。未导入或调用业务，未编译、执行 fixture、写项目；不提供 RSS/native/AAA/ABA 资格。\n')
print(json.dumps(dict(status=report['status'],report_path=str(D/'REPORT.json'),report_sha256=sha((D/'REPORT.json').read_bytes()),source_static_checks=32,original_stage_mapping_count=68,complete_stages=86,all_source_identities_stable=True),allow_nan=False))
