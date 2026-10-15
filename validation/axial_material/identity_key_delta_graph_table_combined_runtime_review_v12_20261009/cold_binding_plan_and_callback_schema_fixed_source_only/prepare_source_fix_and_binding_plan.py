import ast
import difflib
import hashlib
import json
import stat
from pathlib import Path

D=Path('/private/tmp/axmat_v12_cold_binding_authoritative_sources_and_callback_schema_fix_source_only_20261009')
B=Path('/private/tmp/axmat_v12_graph_table_cold_source_only_20261009')
M=Path('/private/tmp/axmat_v11_cold_component_input_consumer_source_only_20261009')
AM=Path('/Users/wen/spot/validation/axial_material')
R=AM/'identity_key_delta_graph_table_combined_runtime_review_v12_20261009'
F='prepare_owned_specs_identity_key_delta_graph_table_cold_runtime_v12.py'
C='cold_component_input_consumer_identity_key_delta_graph_table_own_pid_peak_v12.py'
N='cold_owned_specs_identity_key_delta_graph_table_component_input_intake_binding_v12_20261009.json'
expected={F:'ee7fc7ab17124fe110ec965829710a9cb4c9e19368991b806badbea18422cb3c',C:'0e47a2084acc30085784c132eb480db7e53b10963db6c4ca85b66cc76cf557fa',N:'563b3f7fa28c93427b9a4613bb7b958d998e56a66a2fe85d959c3ec88440abc0','source_inverse_proof.json':'3dca8c5e1f91be24df0fc671007783d5e316f9e7a9b5fb41052aabf3c3c8f8f7'}
def sha(raw):return hashlib.sha256(raw).hexdigest()
def seven(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode)
 return dict(dev=s.st_dev,ino=s.st_ino,mode=s.st_mode,nlink=s.st_nlink,size=s.st_size,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns)
pins={}
def rawpin(p,expected_sha=None):
 p=Path(p);before=seven(p);raw=p.read_bytes();digest=sha(raw);assert seven(p)==before
 if expected_sha:assert digest==expected_sha,(str(p),digest,expected_sha)
 pins[str(p)]=dict(path=str(p),sha256=digest,identity=before)
 return raw
texts={name:rawpin(B/name,pin).decode() for name,pin in expected.items()}
old=texts[F];tree=ast.parse(old)
assigns={n.targets[0].id:n for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
callback=ast.literal_eval(assigns['CALLBACK_METADATA_SCHEMA'].value)
old_schema='AXMAT_HISTORICAL_INPUT_OWNED_SPECS_SCIPY_ENV_CROSS_GROUP_IDENTITY_KEY_DELTA_COMBINED_FILE_SNAPSHOT_COLD_INPUT_ADMISSION_V1'
assert callback=='AXMAT_OWNED_SPECS_IDENTITY_KEY_DELTA_GRAPH_TABLE_SCIPY_ENV_COLD_INPUT_ADMISSION_V12'
assert old.count(old_schema)==1 and old_schema in ast.literal_eval(assigns['ADMISSION_HOST'].value)
new=old.replace(old_schema,callback,1)
assert new.replace(callback,old_schema,1)!=old # the first occurrence is the top current schema
old_segment=ast.get_source_segment(old,assigns['ADMISSION_HOST'])
new_node=next(n for n in ast.parse(new).body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='ADMISSION_HOST')
new_segment=ast.get_source_segment(new,new_node)
assert new_segment.replace(callback,old_schema,1)==old_segment
assert new.replace(new_segment,old_segment,1)==old
assert new.count(old_schema)==0
edits=[dict(name='ADMISSION_HOST generated metadata schema identity only',old=old_segment,new=new_segment)]
embedded=ast.literal_eval(new_node.value);embedded_tree=ast.parse(embedded)
embedded_metadata=next(n for n in embedded_tree.body if isinstance(n,ast.FunctionDef) and n.name=='metadata')
comparisons=[n for n in ast.walk(embedded_metadata) if isinstance(n,ast.Compare) and isinstance(n.left,ast.Subscript) and isinstance(n.left.value,ast.Name) and n.left.value.id=='data' and isinstance(n.left.slice,ast.Constant) and n.left.slice.value=='schema']
assert len(comparisons)==1 and ast.literal_eval(comparisons[0].comparators[0])==callback
def defs(s):
 out={}
 def walk(nodes,prefix=''):
  for n in nodes:
   if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
    out[prefix+n.name]=ast.get_source_segment(s,n);walk(n.body,prefix+n.name+'.')
 walk(ast.parse(s).body);return out
assert defs(old)==defs(new) and len(defs(old))==55
prior=json.loads(texts['source_inverse_proof.json']);v11_name=Path(prior['proofs'][F]['parent_path']).name
inverse=new.replace(new_segment,old_segment,1)
for edit in reversed(prior['proofs'][F]['edits']):assert inverse.count(edit['new'])==1;inverse=inverse.replace(edit['new'],edit['old'],1)
assert sha(inverse.encode())==prior['proofs'][F]['parent_sha256']
mother_proof=json.loads(rawpin(M/'source_inverse_proof.json').decode())['proofs'][v11_name]
for edit in reversed(mother_proof['edits']):
 if edit['name'].startswith('literal family identity '):assert inverse.count(edit['new'])>0;inverse=inverse.replace(edit['new'],edit['old'])
 else:assert inverse.count(edit['new'])==1;inverse=inverse.replace(edit['new'],edit['old'],1)
assert sha(inverse.encode())=='bc8eaa6a72e0e732be5f95ef06fe430a2f8e8848d4edba3bedcd53adc29fecf9'
for name,src in ((F,new),(C,texts[C]),(N,texts[N])):assert not (D/name).exists();(D/name).write_text(src)
(D/'callback_schema_identity.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=str(B/F),tofile=str(D/F))))
sourceproof=dict(schema='AXMAT_V12_COLD_GENERATED_CALLBACK_SCHEMA_MINIMAL_SOURCE_INVERSE_V1',status='UNREADY_SOURCE_ONLY',original_frozen_factory_sha256=expected[F],new_factory_sha256=sha(new.encode()),one_region_inverse_to_Fee7_byteexact=True,complete_1_plus_22_regions_inverse_to_V11_753abe=True,complete_chain_to_genuine_V10_bc8e_sha256=sha(inverse.encode()),all_55_factory_functions_byteexact_to_Fee7=True,consumer_and_binding_byteexact=True,generated_metadata_schema_equals_exact_CALLBACK_METADATA_SCHEMA=True,whole_seven_INPUT_math_P14_P12_MRO_budgets_and_all_None_unchanged=True,edits=edits)
(D/'source_inverse_proof.json').write_text(json.dumps(sourceproof,indent=2)+'\n')
# Formal V12 metadata is an existing authority for build/source identity only.
# It is not a replacement for the future actual bounded host durable log.
formal=json.loads(rawpin(R/'admit.stdout.json').decode())
observer=json.loads(rawpin(R/'Root_actual_formal_admit_tool_terminal_return.json').decode())
assert type(observer['returncode'])is int and observer['returncode']==0 and observer['formal_admission_passed']is True
assert observer['bounded_whole_INPUT_intake_qualified']is False
assert formal['schema']=='AXMAT_OWNED_SPECS_IDENTITY_KEY_DELTA_GRAPH_TABLE_COMBINED_RUNTIME_V12_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1'
assert len(formal['descriptor_files'])==36804 and len(formal['input_aliases'])==186
trim=formal['actual_last_cprime_trim_admission'];counts=trim['cache_unit_control_counts']
assert type(counts)is dict and counts['total_declared_stages']==68
assert (counts['original_factor_diagonal_45_stages_retained'],counts['additional_keycodec_driver_build_stages'],counts['additional_keycodec_execute_stages'])==(45,2,21)
tr=Path(trim['build_root']);trseal=json.loads(rawpin(tr/'seal.json',trim['build_seal_sha256']).decode())
ctrlpin=trim['compiled_unit_controls'];assert ctrlpin==dict(path=str(tr/'audit/controls.json'),sha256=trseal['files']['audit/controls.json'])
ctrl=json.loads(rawpin(ctrlpin['path'],ctrlpin['sha256']).decode())
audit=json.loads(rawpin(tr/'audit/result.json',trseal['files']['audit/result.json']).decode())
driver=json.loads(rawpin(tr/'driver_result.json',trseal['files']['driver_result.json']).decode())
assert ctrl['counts']==audit['control_counts']==driver['control_counts']==counts
assert ctrl['status']=='PASS' and ctrl['keycodec_controls']['standalone_control_count']==21
assert audit['cross_group_identity_controls_passed']is True and driver['cross_group_identity_controls_passed']is True
assert driver['error']is None
counts_sha=sha(json.dumps(counts,sort_keys=True,separators=(',',':'),allow_nan=False).encode())
future_sources={
 'INTAKE_ROOT_SHA':'future durable INTAKE_ROOT/Root_terminal_return.json full byte SHA after host true0, recorder true0, and complete independent wholeINPUT admission',
 'INTAKE_RETURN_SHA':'future durable INTAKE_ROOT/intake/admit.log whole bytes, exact duplicate of original API merged log',
 'API_SEAL_SHA':'actual formal V12 return build_seal_sha256 == V12 OUT/seal.json full SHA, subsequently identical in durable actual host log',
 'API_TERMINAL_SHA':'actual formal V12 return actual_external_terminal_evidence.sha256 == TERM12/terminal_return.json, subsequently identical in durable host log',
 'API_PREP_SHA':'actual formal V12 return actual_prepare_terminal_evidence.sha256 == TERM12/declaration_terminal_return.json, subsequently identical in durable host log',
 'COMBINED_BUILD_SEAL':'same actual V12 build seal authority as API_SEAL_SHA',
 'COMBINED_TERMINAL_SHA':'same actual V12 RUN Root receipt authority as API_TERMINAL_SHA',
 'COMBINED_RUNTIME_SHA':'actual V12 corrected_runtime SHA full file pin, subsequently identical in durable actual host body',
 'TRIM_DECL_SHA':'genuine V11 component TRIM_BUILD/declaration.json independently pinned by full V11 seal and original declaration receipt',
 'TRIM_SEAL_SHA':'genuine V11 component actual_last_cprime_trim_admission.build_seal_sha256 and TRIM_BUILD/seal.json',
 'TRIM_TERMINAL_SHA':'genuine V11 component actual_last_cprime_trim_admission.actual_external_terminal_evidence.sha256 and genuine component terminal',
 'TRIM_OBJECT_SHA':'genuine V11 component actual_last_cprime_trim_admission.compiled_kernel.sha256 and seal build/SPOT1P64.o',
 'TRIM_RUNTIME_SHA':'genuine V11 component actual_last_cprime_trim_admission.corrected_runtime.sha256 and seal runtime/Dragon',
 'TRIM_SOURCE_ADMISSION_SHA':'genuine V11 component source_admission descriptor full SHA and source namespace pin',
 'TRIM_CONTROL_COUNTS':'complete 30-key actual V11 component cache_unit_control_counts, exact equality to sealed controls.counts/audit.control_counts/driver.control_counts, then future actual host durable whole return',
 'EXPECTED_API_DESCRIPTOR_COUNT':'derive len(future actual durable whole return descriptor_files), independent complete fullgraph owner-union review; current formal observation36804 is a crosscheck only',
 'EXPECTED_API_ALIAS_COUNT':'derive len(future actual durable whole return input_aliases), all exact identities/targets verified; current formal observation186 is a crosscheck only',
 'EXPECTED_INTAKE_PAYLOAD_COUNT':'derive future durable Root receipt.payload_inventory.files count; original consumer requires9 payload files plus independent Root10',
 'PRIVATE_INPUT_CONSUMER_SHA':'fresh SHA of final bound reviewed consumer after all actual bindings and READY source admission; no old source SHA reuse',
 'COMPONENT_INTAKE_DESCRIPTOR_SHA':'fresh SHA of final filled B bytes after final consumer SHA; B does not contain its own binding_descriptor or SHA',
 'FORMAL_FACTORY_SHA':'documentary field can stayNone; execution identity comes from actual final reviewed installed F full SHA via AXMAT_COLD_FACTORY_SHA256',
 'BINDING_CONTROLS_ACTUAL':'real later run-controls Root receipt passed as true completed descriptor, never a prefilled proof',
 'FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA':'actual V12 PREP Root receipt, same authority as API_PREP_SHA',
 'FUTURE_ACTUAL_COLD_DECLARATION_TERMINAL_SHA':'future COLD_TERMINAL/declaration_terminal_return.json after unique declare true0 and independent source/graph/environment review',
 'FUTURE_ACTUAL_COLD_PREPARED_SHA':'future OUTPUT/prepared.json after unique original prepare true0; later prepared_cold.json is a separately pinned descriptor and must not be confused',
 'FUTURE_ACTUAL_COLD_BINDING_SHA':'future OUTPUT/own_rss_binding.json after prepare-binding true0; complete independently expected files owner union and no self-SHA cycle',
 'FUTURE_ACTUAL_COLD_CONTROL_SEAL_SHA':'future OUTPUT/binding_controls/seal.json after genuine new controls and raw/watchdog admission',
 'FUTURE_ACTUAL_COLD_CONTROL_TERMINAL_SHA':'future CONTROL_TERMINAL/terminal_return.json after genuine controls true0',
 'FUTURE_ACTUAL_COLD_TERMINAL_SHA':'future COLD_TERMINAL/terminal_return.json only real successful run-AAA true0 plus all stages/seals/fourtail gates; real failures remain separate',
 'FUTURE_ACTUAL_COLD_CLOSEOUT_SEAL_SHA':'future OUTPUT/cold_closeout_seal.json from actual successful native namespace; cannot be minted from source/INPUT status'}
none_maps={}
for name,s in ((C,texts[C]),(F,new)):
 a={n.targets[0].id:n for n in ast.parse(s).body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)}
 values=[k for k,n in a.items()if isinstance(n.value,ast.Constant)and n.value.value is None]
 assert all(k in future_sources for k in values)
 none_maps[name]={k:future_sources[k]for k in values}
assert len(counts)==30
# Inventory/graph binding fields are filled only from future qualified durable
# evidence; neither current formal snapshots nor former V10 sizes supply them.
binding_plan={
 'actual_bounded_api_terminal_evidence':future_sources['INTAKE_ROOT_SHA'],
 'api_return':future_sources['INTAKE_RETURN_SHA'],
 'intake_proof_files':'all9 durable Root payload_inventory files plus separately created Root_terminal_return.json path/SHA; compare every original payload pin exactly',
 'intake_namespaces':'full durable tree directories/files(no symlinks) derived from actual Root payload inventory and exact live namespace, not a source-only prediction',
 'helper_sources':'fresh final installed graph e8f/typed codec758c/checks86e full source SHA; graph two owned decode entrances only and original full verification scope retained',
 'complete_historical_input_graph':'future actual durable return historical_input_graph full descriptor == V12 real graph stored byte SHA/content SHA/scope; decoded canonical_files retains all36776rows, source-only plan does not rehash graph',
 'binding_source':'final bound reviewed consumer canonical path and fresh SHA; preserve no class/module overlay',
 'expected_complete_alias_count':future_sources['EXPECTED_API_ALIAS_COUNT'],
 'expected_complete_descriptor_count':future_sources['EXPECTED_API_DESCRIPTOR_COUNT'],
 'expected_intake_payload_count':future_sources['EXPECTED_INTAKE_PAYLOAD_COUNT'],
 'actual_V11_component_control_counts':future_sources['TRIM_CONTROL_COUNTS']}
templates=[]
for n in ast.parse(new).body:
 if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and isinstance(n.value,ast.Constant)and isinstance(n.value.value,str)and '\n' in n.value.value:
  templates.append(dict(name=n.targets[0].id,line=n.lineno,bytes=len(n.value.value.encode()),classification='CURRENT_V12_CALLBACK_SCHEMA_FIXED_ONLY'if n.targets[0].id=='ADMISSION_HOST'else'ORIGINAL_MRO_CONSTRUCTOR_DECK_OR_PARENT_TEMPLATE_UNCHANGED',unchanged_from_Fee7=n.targets[0].id!='ADMISSION_HOST'))
workflow=[dict(phase=phase,source_function=fn,future_outputs=outputs)for phase,fn,outputs in (
 ('declare','declare','SOURCE31 full namespace plus declaration/factory_seal/source_equivalence/analysis_environment and immutable callback metadata; Root actual declaration receipt+fullstreams separately'),
 ('prepare','prepare','original controller3arg prepare through execve producerP14; INPUT-only OUTPUT prepared.json/local source/deck files, no transport'),
 ('prepare-binding','prepare_binding_in_clean_process','whole normal canonical OwnRSS binding with all expected file/module owners; no fixture/native credit'),
 ('run-controls','run_controls','new real positive/oversize/short watches/logs/results/seal plus independent CONTROL_TERMINAL receipt, kernel missing values preserved'),
 ('finalize-cold','finalize_cold_in_clean_process','original prepared dictionary plus one real own_child_supervision descriptor only; new prepared_cold SHA'),
 ('run-AAA','cold_launch_in_clean_process','one fresh original native attempt no retries, actual stages/rawlog/math observers/seals/maps and fourtail before native-only WAITING_REFERENCE admission'))]
report=dict(schema='AXMAT_V12_COLD_SOURCE_FIX_AND_AUTHORITATIVE_BINDING_PLAN_V1',status='PASS_SOURCE_FIX_AND_BINDING_PLAN_ONLY_UNREADY',new_factory=dict(path=str(D/F),sha256=sha(new.encode())),consumer_unchanged=dict(path=str(D/C),sha256=expected[C]),binding_unchanged=dict(path=str(D/N),sha256=expected[N]),source_inverse_proof_sha256=sha((D/'source_inverse_proof.json').read_bytes()),fixed_current_callback_schema=callback,generated_templates_scanned=templates,frozen_V11_component_paths_and0800_5e343e_kept=True,None_binding_authorities=none_maps,binding_descriptor_authorities=binding_plan,actual_existing_formal_V12_build_only_observation=dict(source_stdout=pins[str(R/'admit.stdout.json')],Root_formal_admit=pins[str(R/'Root_actual_formal_admit_tool_terminal_return.json')],schema=formal['schema'],descriptor_count=36804,input_alias_count=186,bounded_whole_INPUT_qualified=False),actual_V11_complete68_counts_cross_evidence=dict(counts=counts,key_count=len(counts),sorted_complete_counts_sha256=counts_sha,sealed_controls=pins[ctrlpin['path']],audit=pins[str(tr/'audit/result.json')],driver=pins[str(tr/'driver_result.json')],seal=pins[str(tr/'seal.json')],equal_to_actual_nested_API_counts=True,original45_plus2_plus21_preserved=True),binding_order=['Wait for unique bounded host true0/closed, Rootdurable9+Root10, complete wholeINPUT independent admission.','Bind C actual return/graph/aliases/counts/complete68 dictionary plus known source identities; source review then final C SHA.','Fill B complete durable proof map/ns and full graph descriptor/helper sources/final C SHA; no own binding_descriptor then hash B.','Bind F genuine combined runtime/PREP/RUN/68 component facts, final C/B hashes and independently observed counts; preserve documentary self-SHA None plus external AXMAT_COLD_FACTORY_SHA256.','Independent complete SOURCE/body/inverse review then Root READY transition+new source hash, sole canonical install, then phased actual declare/PREP/binding/controls/finalize/native gates.'],workflow=workflow,source_inventory_and_callback_contract='SOURCE inventory generated by actual declare, copied new consumer/runtime helpers + sealed generated sources; rank1_factor_cache_admission schema equals ADMISSION_HOST metadata predicate. Runtime files, producer environment430+SciPy1424/full union/fullgraph owner rows/callback complete65+seven+trim retain original full fresh gates, no old count reuse.',whole_seven_INPUT_complete_decoded_graph_all_namespace_alias_absence_gates_unchanged=True,P14_producer_P12_analysis_budget_and_math_source_unchanged=True,own_RSS_MiB=512,bootstrap_axial_seconds=4200,total_cold_seconds=43200,future_actual_bounded_INPUT=None,future_actual_cold_declare=None,future_actual_PREP=None,future_actual_controls=None,future_actual_native=None,business_module_imported=False,business_API_or_CLI_executed=False,fixture_or_compiler_executed=False,project_written=False,scientific_qualification=False,AAA_accuracy_qualified=False,ABA_admitted=False,all_fresh_small_metadata_source_pins=pins)
(D/'BINDING_PLAN_AND_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
(D/'REPORT.txt').write_text('V12冷入口新SOURCE修订仅纠正ADMISSION_HOST生成metadata()的schema字面，精确等于当前CALLBACK_METADATA_SCHEMA；原Fee7/C0e/B563冻结不改。\n完整1+22区域逆向V11，再完整chain到真实V10，55工厂函数与原Fee7逐字不变；所有数学、MRO、7INPUT、P14/P12和512/4200/43200预算保持。\n未来绑定plan逐一标明真实权威来源。TRIM_CONTROL_COUNTS从真实V11 68步骤封存controls/audit/driver及当前实际完整嵌套API30键字典共同核对；不会用旧45统计冒充。\n当前formal V12仅观察36804descriptor/186alias；真正bounded host未获准入，必须未来durable全log+9payload及独立Root10后重新derive实际counts/graph/namespace并填值。\n所有未来success/count/inventory None保留，未执行业务/fixture/编译/controls/declare/native，未项目写；方案不授科学信用。\n')
print(json.dumps(dict(status=report['status'],new_factory_sha256=report['new_factory']['sha256'],source_inverse_sha256=report['source_inverse_proof_sha256'],report_sha256=sha((D/'BINDING_PLAN_AND_REPORT.json').read_bytes()),actual_complete68_counts=len(counts),template_count=len(templates))))
