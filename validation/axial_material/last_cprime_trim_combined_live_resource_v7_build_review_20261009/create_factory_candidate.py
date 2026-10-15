from pathlib import Path
import ast,hashlib,json,difflib
BASE=Path('/private/tmp/axmat-trim-v7-owned-phase-lifetimes-factory-source-draft-20261009')
ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts'
PARENT=ROOT/'validation/axial_material/prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v6.py'
CANDIDATE=BASE/'prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v7.py'
OLD_HELPER=ROOT/'validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_same_literal_phase_identity_20261008.py'
NEW_HELPER=ROOT/'validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_owned_phase_owner_lifetimes_20261009.py'
TMP_HELPER=Path('/private/tmp/axmat-owned-phase-owner-lifetimes-graph-draft-20261009/combined_runtime_reviewed_metadata_historical_input_graph_owned_phase_owner_lifetimes_20261009.py')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p):return dict(path=str(p),sha256=sha(p),size_bytes=p.stat().st_size)
assert sha(PARENT)=='6bcef269814a120f0cf8a5e9d068a6de0b509017690b8ae646b50b2ef27d8921'
assert sha(OLD_HELPER)=='07b22c9f2f4fba626fbe7f4faec5edd9cbbc15f0e0f4f4edf5858aac489be612'
assert sha(TMP_HELPER)=='85551979317309cfa70bb27a4b0e04ae908bbd33865dc3edfbe6c7f4d70baf6c'
if NEW_HELPER.exists():assert sha(NEW_HELPER)==sha(TMP_HELPER)
old=PARENT.read_text();new=old
old_doc=ast.get_source_segment(old,ast.parse(old).body[0])
new_doc='''"""Reviewed independent combined-runtime temporary owner-map lifetime candidate.

Derived from frozen v6, whose actual fifth Python input-audit child exceeded
its original 512 MiB RSS cap. No success or memory credit is inherited from
that failed run or separate input diagnostics. The new reviewed helper only
consumes its own freshly normalized nonconsumer owner descriptors after each
complete original expected-file edge sequence; all owner new-input roles keep
their original later positions, and consumer lineage keeps complete owners.
The full regular-byte union, old seven-key body, actual trim input, all namespaces
and every original wall/RSS/disk/thread/child/terminal gate remain required.
"""'''
regions=[dict(kind='honest-module-docstring',before=old_doc,after=new_doc)]
for assignment in ('SOURCE','OUT','TERMINAL'):
 node=next(n for n in ast.parse(old).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==assignment for t in n.targets))
 before=ast.get_source_segment(old,node)
 after=before.replace('scopes-v6-20261008','scopes-v7-20261009')
 assert before!=after
 regions.append(dict(kind=assignment+'-new-family-root',before=before,after=after))
regions += [
 dict(kind='new-family-link-identity',before="FAMILY = 'HISTORICAL_INPUT_TRIM_COMBINED_RUNTIME_LINK_V6'",after="FAMILY = 'HISTORICAL_INPUT_TRIM_COMBINED_RUNTIME_LINK_V7'"),
 dict(kind='new-prefix-identity',before="PREFIX = 'AXMAT_HISTORICAL_INPUT_OWNED_SPECS_LAST_CPRIME_TRIM_COMBINED_PHYSICAL_DEDUP_RUNTIME_LIVE_RESOURCE_SCOPES_V6'",after="PREFIX = 'AXMAT_HISTORICAL_INPUT_OWNED_SPECS_LAST_CPRIME_TRIM_COMBINED_PHYSICAL_DEDUP_RUNTIME_LIVE_RESOURCE_SCOPES_V7'"),
 dict(kind='new-formal-factory-basename',before="prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v6.py",after="prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v7.py"),
 dict(kind='new-reviewed-graph-module-basename',before=OLD_HELPER.name,after=NEW_HELPER.name),
 dict(kind='new-reviewed-graph-module-SHA',before=sha(OLD_HELPER),after=sha(TMP_HELPER))]
for r in regions:
 assert new.count(r['before'])==1,(r['kind'],new.count(r['before']))
 new=new.replace(r['before'],r['after'],1)
rev=new
for r in reversed(regions):
 assert rev.count(r['after'])==1,(r['kind'],rev.count(r['after']))
 rev=rev.replace(r['after'],r['before'],1)
assert rev.encode('utf-8')==PARENT.read_bytes()
CANDIDATE.write_text(new)
oldtree=ast.parse(old);newtree=ast.parse(new)
oldfunc={n.name:ast.get_source_segment(old,n) for n in oldtree.body if isinstance(n,ast.FunctionDef)}
newfunc={n.name:ast.get_source_segment(new,n) for n in newtree.body if isinstance(n,ast.FunctionDef)}
assert oldfunc==newfunc and len(oldfunc)==65
oldassign={n.targets[0].id:ast.get_source_segment(old,n)for n in oldtree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
newassign={n.targets[0].id:ast.get_source_segment(new,n)for n in newtree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
assert set(oldassign)==set(newassign)
changedassign=[name for name in oldassign if oldassign[name]!=newassign[name]]
assert changedassign==['SOURCE','OUT','TERMINAL','FAMILY','PREFIX','FORMAL_FACTORY','INPUT_HELPERS'],changedassign
assert oldassign['INPUT_SPECS']==newassign['INPUT_SPECS'] and oldassign['INPUT_SPECS_SHA']==newassign['INPUT_SPECS_SHA'] and oldassign['BODY_BINDING']==newassign['BODY_BINDING']
assert newfunc['actual_components']==oldfunc['actual_components'] and 'entire historical seven-key body differs; no field filtering' in newfunc['actual_components']
inputspec=ROOT/'validation/axial_material/combined_runtime_complete_historical_input_specs_20261007.json'
assert sha(inputspec)=='2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa'
source_inverse=dict(schema='AXMAT_TRIM_V7_OWNED_PHASE_LIFETIME_FACTORY_COMPLETE_SOURCE_INVERSE_V1',status='PASS_SOURCE_ONLY_STOPPED',parent=pin(PARENT),candidate=pin(CANDIDATE),regions=regions,region_count=len(regions),whole_source_inverse_bytes_equal=True,parent_top_level_functions=65,candidate_top_level_functions=65,all_65_function_bodies_byte_exact=True,changed_assignments=changedassign,unchanged_assignments=[name for name in oldassign if name not in changedassign],historical_whole_seven_key_body_INPUT_SPECS=pin(inputspec),BODY_BINDING_assignment_byte_exact=True,actual_components_full_seven_key_validation_function_byte_exact=True,all_math_controls_input_data_supervisor_environment_resource_and_negative_gates_unchanged=True,top_docstring_is_failed_V6_provenance_not_a_success_pin=True,no_business_or_numeric_or_constructor_or_project_import=True)
(BASE/'source_inverse.json').write_text(json.dumps(source_inverse,indent=2,sort_keys=True)+'\n')
(BASE/'full.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=str(PARENT),tofile=str(CANDIDATE))))
# Read small actual V6 declaration/resource metadata only, not its full graph.
v6out=ART/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v6-20261008'
v6term=ART/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-owned-specs-last-cprime-trim-live-resource-scopes-v6-20261008'
decl=v6out/'declaration.json';actual=json.loads(decl.read_text());oldroots=actual['resource_roots']
assert len(oldroots)==221 and oldroots==sorted(set(oldroots))
v6diag=ART/'axial-material-trim-combined-v6-python-input-memory-diagnostic-20261008'
assert v6diag.is_dir() and str(v6diag) not in oldroots
newroots=[str(ART/name)for name in (
'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-admission-owned-specs-last-cprime-trim-live-resource-scopes-v7-20261009',
'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v7-20261009',
'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-owned-specs-last-cprime-trim-live-resource-scopes-v7-20261009')]
assert all(root not in oldroots for root in newroots)
expected=sorted(set(oldroots)|set(newroots)|{str(v6diag)})
assert len(expected)==225
# Metadata-only exact name observation for the unchanged axial-family glob.
currentfamily={str(path)for path in ART.glob('axial-material-*')}
not_in_expected=sorted(currentfamily-set(expected))
assert not not_in_expected,not_in_expected
scope=dict(schema='AXMAT_TRIM_V7_SOURCE_ONLY_RESOURCE_SCOPE_PREDICTION_V1',status='METADATA_ONLY_NOT_ACTUAL_V7_DECLARATION',actual_parent_declaration=pin(decl),parent_actual_roots=oldroots,parent_actual_root_count=221,expected_new_family_roots=newroots,expected_new_existing_diagnostic_root=str(v6diag),expected_all_roots=expected,expected_all_root_count=225,all_221_original_roots_retained=True,new_roots_not_old_path_replacements=True,unchanged_live_history_roots_and_validation_functions_byte_exact=True,original_body_calls_original_history_glob_and_rechecks_new_roots_on_real_PREP=True,no_resource_scope_module_or_constructor_called=True,actual_V7_PREP_must_check_real_root_set=True,original_V6_graph_bytes=67097740,original_graph_cap_bytes=67108864,original_V6_slack_bytes=11124,new_graph_size_not_measured=True,no_cap_relaxation=True)
(BASE/'resource_root_scope_prediction.json').write_text(json.dumps(scope,indent=2,sort_keys=True)+'\n')
receipt=v6term/'terminal_return.json';failure=json.loads(receipt.read_text());assert failure['returncode']==1 and failure['failed_python_audit_peak_rss_mib']==518.625 and failure['combined_runtime_native_RSS_proved']is False
hand=dict(schema='AXMAT_TRIM_V7_OWNED_PHASE_LIFETIME_FACTORY_SOURCE_ONLY_STOPPED_HANDOFF_V1',status='STOPPED_REQUIRES_ROOT_SOURCE_REVIEW_HELPER_FORMAL_COPY_AND_NEW_FAMILY_EXECUTION',source=pin(CANDIDATE),parent=pin(PARENT),source_inverse=pin(BASE/'source_inverse.json'),full_diff=pin(BASE/'full.diff'),scope_prediction=pin(BASE/'resource_root_scope_prediction.json'),planned_formal_factory=str(ROOT/'validation/axial_material'/CANDIDATE.name),planned_formal_helper=str(NEW_HELPER),reviewed_TMP_helper=pin(TMP_HELPER),formal_helper_exists_at_author_observation=NEW_HELPER.exists(),future_declaration_sha256=None,future_PREP_sha256=None,future_RUN_sha256=None,future_build_seal_sha256=None,future_actual_complete_input_admission=None,failed_parent_context_not_success=pin(receipt),failed_parent_true_returncode=1,failed_parent_sampled_peak_rss_mib=518.625,actual_helpers_input_only_source_proof=True,actual_V7_graph_size=None,original64MiB_cap_not_waived=True,all_full_inputs_and_whole_seven_key_body_retained=True,actual_V7_root_count_not_observed=True,any_original_actual_success_pins_are_unchanged_old_component_INPUT_only=True,combined_runtime_native_RSS_proved=False,actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False,scientific_qualification=False,no_ART_or_formal_source_written=True,no_APIs_executed_or_globals_modified=True,no_generic_root_review_path_retargting=True)
(BASE/'STOPPED_handoff.json').write_text(json.dumps(hand,indent=2,sort_keys=True)+'\n')
(BASE/'AUTHOR_REPORT.txt').write_text('''V7 独占临时归属表生命周期组合工厂源码候选（2026-10-09）

从正式V6源6bcef完整9处逆向产生新V7，仅docstring与7个顶层赋值改变；
全部65函数正文及其原执行门、schema负例、物理输入和限额逐字节不变。
SOURCE/OUT/TERMINAL是3个新的scopes-v7-20261009根，FORMAL basename、
PREFIX/FAMILY仅V7身份；INPUT_HELPERS.graph钉新helper 855519。
V6失败518.625 MiB仅是诚实来源，不是继承成功或RSS通过凭据。

原2cad9全部19,356,767B INPUT_SPECS实际sha核验保持，BODY_BINDING及
actual_components整七键回传检查原源未改；旧组件真实成功pin都仅INPUT
含义，绝不改作新V7成功。无futureDECL/PREP/RUN/seal值。

资源根在函数正文里由原历史动态axial-material-*规则观察；这里不加
独立新常量或改根函数。元数据只读的V6声明原221根全部保留，预测再
增加V7三根及新V6诊断根，共225根。现存family名称未发现额外未计根；
真实V7 PREP必须再次观察，预测不是实际新声明。源不存在全局替换导致
老V6root被抹掉的情况，原221根在原live目录和预测表内全部保留。

原graph已经compact，V6实际67,097,740B距64MiB门仅11,124B。
本作者未生成V7 graph，不承诺其尺寸，保留严格原64MiB门。
正式新helper观察尚未存在时，TMP工厂不能执行，require_ready原函数
会拒绝TMP __file__；只能Root先审源/复制正式helper再决定实际新family。

未执行项目导入、构造器、API、生产、原生或数学，不写ART或正式源。
''')
print(json.dumps(dict(source=pin(CANDIDATE),inverse=pin(BASE/'source_inverse.json'),scope_prediction=pin(BASE/'resource_root_scope_prediction.json'),handoff=pin(BASE/'STOPPED_handoff.json'),regions=len(regions),unchanged_functions=len(oldfunc),predicted_roots=len(expected))))
