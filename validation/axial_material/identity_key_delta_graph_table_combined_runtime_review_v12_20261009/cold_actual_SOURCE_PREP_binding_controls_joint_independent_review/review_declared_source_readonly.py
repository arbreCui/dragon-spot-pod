"""Read SOURCE31 and existing small metadata; never import/call business code."""
import ast
import copy
import hashlib
import json
import struct
from pathlib import Path

D=Path(__file__).resolve().parent
ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
SOURCE=ART/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-cold-source-v12-20261009'
TERM=ART/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-cold-terminal-v12-20261009'
R=ROOT/'validation/axial_material/identity_key_delta_graph_table_combined_runtime_review_v12_20261009'
F=ROOT/'validation/axial_material/prepare_owned_specs_identity_key_delta_graph_table_cold_runtime_v12.py'
PINS={}

def pin(path,wanted=None):
    path=Path(path);assert path.is_file()and not path.is_symlink(),path
    before=path.stat();h=hashlib.sha256()
    with path.open('rb')as stream:
        for block in iter(lambda:stream.read(1<<20),b''):h.update(block)
    after=path.stat()
    assert(before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns)
    obj=dict(path=str(path),sha256=h.hexdigest(),bytes=before.st_size)
    if wanted is not None:assert obj['sha256']==wanted,(path,obj['sha256'],wanted)
    PINS[str(path)]=obj;return obj

def read(path,wanted=None):
    pin(path,wanted);return json.loads(Path(path).read_text())

def owned(item):
    return read(item['path'],item['sha256'])

def sha(text):return hashlib.sha256(text.encode()).hexdigest()

def definitions(text):
    return {n.name:ast.get_source_segment(text,n)for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}

def exact(a,b):
    if type(a)is not type(b):return False
    if isinstance(a,float):return struct.pack('>d',a)==struct.pack('>d',b)
    if isinstance(a,dict):return a.keys()==b.keys()and all(exact(a[k],b[k])for k in a)
    if isinstance(a,list):return len(a)==len(b)and all(exact(x,y)for x,y in zip(a,b))
    return a==b

def restored(candidate,parent,changed,added=()):
    value=copy.deepcopy(candidate)
    for path in changed:
        dst,src=value,parent
        for key in path[:-1]:dst,src=dst[key],src[key]
        dst[path[-1]]=copy.deepcopy(src[path[-1]])
    for path in added:
        dst=value
        for key in path[:-1]:dst=dst[key]
        del dst[path[-1]]
    assert exact(value,parent)

def constants(tree,names):
    nodes={n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
    cache={}
    def val(n):
        try:return ast.literal_eval(n)
        except(ValueError,TypeError):
            if isinstance(n,ast.Name):return get(n.id)
            if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='Path':return Path(val(n.args[0]))
            if isinstance(n,ast.BinOp):
                a,b=val(n.left),val(n.right)
                if isinstance(n.op,ast.Div):return a/b
                if isinstance(n.op,ast.Mult):return a*b
                if isinstance(n.op,ast.Pow):return a**b
            raise ValueError(ast.dump(n))
    def get(name):
        if name not in cache:cache[name]=val(nodes[name])
        return cache[name]
    return {n:get(n)for n in names}

pin(F,'7037cf10b98e0f5098a87bb87808940a85132abce48e6156db7b136eddcfbf71')
fs=F.read_text();ft=ast.parse(fs)
fc=constants(ft,{'ADMISSION_HOST','CALLBACK_METADATA_SCHEMA','BASE_CONTROLLER','BASE_CONTROLLER_SHA','BASE_WORK','OLD','PREPARED_SHA','BUILD','BUILD_FACTORY','BUILD_FACTORY_SHA','CORRECTION_SCOPE','HOST','HOST_SHA','CONTROLS','CONTROLS_SHA','DECK_HELPER','DECK_HELPER_SHA','PRIVATE_INPUT_CONSUMER','PRIVATE_INPUT_CONSUMER_SHA','PHYSICAL_BASIS_HELPER','PHYSICAL_BASIS_HELPER_SHA','SCIPY_HELPER','SCIPY_HELPER_SHA'})
seal=read(SOURCE/'factory_seal.json','d182259bb17b580bbe45fe1853168c188515ef0b5ef654cfe7a72b668c32f3d5')
assert len(seal['files'])==30
actual_members={p.name for p in SOURCE.iterdir()}
assert actual_members==set(seal['files'])|{'factory_seal.json'}and all(p.is_file()and not p.is_symlink()for p in SOURCE.iterdir())
for name,wanted in seal['files'].items():pin(SOURCE/name,wanted)
decl=read(SOURCE/'declaration.json','758db9578a8b259afd8da2faf1f50614e6d4f581a0922d22083824350fdfd75d')
rootterm=read(TERM/'declaration_terminal_return.json','66c0647d69ba276460a84a09cee6502b272ded07c5b24b5f3509a64ae47d0b2c')
typed=read(R/'Root_actual_cold_declare_tool_input.json')
rootreview=read(R/'Root_actual_cold_declare_tool_terminal_return.json')
assert typed['actual_initial_tool_result']['chunk_id']=='e23c07'and typed['actual_initial_tool_result']['session_id']==72878
assert typed['actual_terminal_tool_result']['chunk_id']=='dab921'and type(typed['actual_terminal_tool_result']['exit_code'])is int and typed['actual_terminal_tool_result']['exit_code']==0 and 'session_id'not in typed['actual_terminal_tool_result']
assert rootreview['actual_initial_tool_result']==typed['actual_initial_tool_result']and rootreview['actual_terminal_tool_result']==typed['actual_terminal_tool_result']and rootreview['session_closed']is True
assert rootreview['source_complete_inventory']==dict(seal['files'],**{'factory_seal.json':PINS[str(SOURCE/'factory_seal.json')]['sha256']})
assert rootterm['actual_tool_result']==rootreview['actual_tool']==dict(initial_chunk_id='e23c07',session_id=72878,terminal_chunk_id='dab921',exit_code=0)
for key in ['source','declaration','factory_seal','full_stdout','full_stderr']:pin(rootterm[key]['path'],rootterm[key]['sha256'])
assert Path(rootterm['full_stdout']['path']).read_bytes()==(R/'cold_declare.stdout').read_bytes()
assert Path(rootterm['full_stderr']['path']).read_bytes()==(R/'cold_declare.stderr').read_bytes()==b''
stdout=json.loads(Path(rootterm['full_stdout']['path']).read_text())
assert stdout['classification']=='DECLARED_COMBINED_PHYSICAL_DEDUP_FILE_SNAPSHOT_COLD_INPUT_ONLY'
assert stdout['declaration']==rootterm['declaration']and stdout['factory_seal']==rootterm['factory_seal']
assert rootterm['returncode']==0 and rootterm['scientific_qualification']is False and rootterm['transport_started']is False
assert rootterm['command']==[read(SOURCE/'analysis_environment.json')['executable'],str(F),'declare','--factory-sha256',PINS[str(F)]['sha256']]

eq=read(SOURCE/'source_equivalence.json')
runtime_inverses={}
parent_paths={'production_runner.py':fc['BASE_CONTROLLER'],'qualified_snapshot_ingestion.py':fc['BASE_WORK']/'runtime/qualified_snapshot_ingestion.py','numerical_layout_admission.py':fc['BASE_WORK']/'runtime/numerical_layout_admission.py'}
for name,parent_path in parent_paths.items():
    proof=eq['patches'][name]
    candidate=(SOURCE/name).read_text();old=Path(parent_path).read_text();pin(parent_path,proof['original_sha256'])
    inv=candidate
    for before,after in reversed(proof['replacements']):
        assert inv.count(after)==1;inv=inv.replace(after,before,1)
    assert inv==old
    original_defs,candidate_defs=definitions(old),definitions(candidate)
    assert original_defs.keys()==candidate_defs.keys()
    listed=proof.get('unchanged_definitions',proof.get('unchanged_function_AST',[]))
    assert all(original_defs[k]==candidate_defs[k]for k in listed)
    if name=='production_runner.py':assert original_defs['SerialExecutor']==candidate_defs['SerialExecutor']and original_defs['resource_monitor']==candidate_defs['resource_monitor']and original_defs['qualify_aba']==candidate_defs['qualify_aba']
    runtime_inverses[name]=dict(original_sha256=sha(old),candidate_sha256=sha(candidate),complete_byte_inverse=True,replacement_regions=len(proof['replacements']),listed_definitions_byteexact=True)
for name,item in eq['unchanged_files'].items():
    pin(item['parent']['path'],item['parent']['sha256'])
    assert Path(item['parent']['path']).read_bytes()==(SOURCE/name).read_bytes()
for key,name in [('HOST','combined_cold_own_rss_host.py'),('CONTROLS','combined_cold_own_rss_controls.py'),('DECK_HELPER','combined_cold_file_snapshot_decks.py'),('PRIVATE_INPUT_CONSUMER','cold_component_input_consumer_identity_key_delta_graph_table_own_pid_peak_v12.py'),('PHYSICAL_BASIS_HELPER','physical_common_basis_admission.py'),('SCIPY_HELPER','cold_scipy_environment_admission_namespace_v3_20261008.py')]:
    pin(fc[key],fc[key+'_SHA']);assert Path(fc[key]).read_bytes()==(SOURCE/name).read_bytes()

m=read(SOURCE/'rank1_factor_cache_admission.json')
assert m['schema']==fc['CALLBACK_METADATA_SCHEMA']=='AXMAT_OWNED_SPECS_IDENTITY_KEY_DELTA_GRAPH_TABLE_SCIPY_ENV_COLD_INPUT_ADMISSION_V12'
bpath=ROOT/'validation/axial_material/cold_owned_specs_identity_key_delta_graph_table_component_input_intake_binding_v12_20261009.json'
b=read(bpath,'1e2b3c99e8f09c2716a5e44eca4cb9520339229c6e44a44ae6758d0dcd98d8db')
expected_intake=copy.deepcopy(b);expected_intake['binding_descriptor']=dict(path=str(bpath),sha256=PINS[str(bpath)]['sha256'])
assert exact(m['component_input_intake'],expected_intake)
assert m['whole_component_body_source']==b['api_return']and m['whole_component_return_encoding']=='COMPLETE_EXTERNAL_API_JSON_POINTER_MATERIALIZED_AFTER_FRESH_GRAPH'
api=owned(m['whole_component_body_source'])
assert m['combined_runtime']==api['corrected_runtime']and m['input_aliases']==api['input_aliases']
assert all(m['files'].get(p)==h for p,h in api['descriptor_files'].items())and len(api['descriptor_files'])==36804
assert len(api['input_aliases'])==186 and m['component_input_intake']['actual_V11_component_control_counts']==api['actual_last_cprime_trim_admission']['cache_unit_control_counts']and len(b['actual_V11_component_control_counts'])==30
for name,wanted in m['component_runtime_file_hashes'].items():assert seal['files'][name]==wanted
assert len(m['component_runtime_file_hashes'])==7
assert m['component_API_reexecution_in_cold_process']is False and m['new_binding_controls_not_yet_executed']is True and m['whole_component_returns_preserved']is True
for p,h in m['files'].items():assert type(p)is str and Path(p).is_absolute()and '..'not in Path(p).parts and type(h)is str and len(h)==64 and all(c in '0123456789abcdef'for c in h)

host=(SOURCE/'rank1_factor_cache_admission.py').read_text();hosttree=ast.parse(host)
hostnodes={n.targets[0].id:n.value for n in hosttree.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
mapping={'EXPECTED_BUILD_ROOT':'__BUILD_ROOT__','EXPECTED_BUILD_SEAL':'__BUILD_SEAL__','EXPECTED_RUNTIME_SHA':'__RUNTIME_SHA__','EXPECTED_RUNTIME_PATH':'__RUNTIME_PATH__','FACTORY_DESCRIPTOR':'__FACTORY_DESCRIPTOR__','EXPECTED_PARENT_PREPARED_SHA':'__PREPARED_SHA__','EXPECTED_BUILD_FACTORY':'__BUILD_FACTORY__','EXPECTED_BUILD_FACTORY_SHA':'__BUILD_FACTORY_SHA__','EXPECTED_TERMINAL_EVIDENCE':'__TERMINAL_EVIDENCE__','EXPECTED_TERMINAL_VALIDATION':'__TERMINAL_VALIDATION__','EXPECTED_TERMINAL_CHAIN':'__TERMINAL_CHAIN__','EXPECTED_CORRECTION_SCOPE':'__CORRECTION_SCOPE__','EXPECTED_RESOURCE_SCOPE_CONTRACT':'__RESOURCE_SCOPE_CONTRACT__'}
expected_host={'EXPECTED_BUILD_ROOT':str(fc['BUILD']),'EXPECTED_BUILD_SEAL':api['actual_components']['original92']['build_seal_sha256'],'EXPECTED_RUNTIME_SHA':m['combined_runtime']['sha256'],'EXPECTED_RUNTIME_PATH':m['combined_runtime']['path'],'FACTORY_DESCRIPTOR':dict(path=str(F),sha256=PINS[str(F)]['sha256']),'EXPECTED_PARENT_PREPARED_SHA':fc['PREPARED_SHA'],'EXPECTED_BUILD_FACTORY':str(fc['BUILD_FACTORY']),'EXPECTED_BUILD_FACTORY_SHA':fc['BUILD_FACTORY_SHA'],'EXPECTED_TERMINAL_EVIDENCE':m['build_terminal_evidence'],'EXPECTED_TERMINAL_VALIDATION':m['build_terminal_validation'],'EXPECTED_TERMINAL_CHAIN':m['build_terminal_chain'],'EXPECTED_CORRECTION_SCOPE':fc['CORRECTION_SCOPE'],'EXPECTED_RESOURCE_SCOPE_CONTRACT':m['resource_scope_contract']}
inv_host=host
for name,token in mapping.items():
    assert exact(ast.literal_eval(hostnodes[name]),expected_host[name])
    value_text=ast.get_source_segment(host,hostnodes[name]);assignment=name+' = '+value_text
    assert inv_host.count(assignment)==1;inv_host=inv_host.replace(assignment,name+' = '+token,1)
scope=eq['patches']['rank1_factor_cache_admission_metadata_scope']
assert inv_host.count(scope['new_scope_predicate'])==1
inv_host=inv_host.replace(scope['new_scope_predicate'],scope['old_scope_predicate'],1)
assert inv_host==fc['ADMISSION_HOST']
generated_host_inverse=dict(all13_token_values_match_actual_inputs=True,metadata_schema_exact_V12=True,whole_source_inverse_to_frozen_template=True,scope_predicate_inverse_regions=1)

gate=read(SOURCE/'input_and_gate_equivalence.json');spec=read(SOURCE/'case_spec.json');parent_spec=owned(gate['parent_case_spec'])
restored(spec,parent_spec,[('experiment_id',),('status',),('production','implementation'),('qualified_snapshot_producers','receiver_sha256'),('qualified_snapshot_producers','receipt'),('conditional_white_trace_trial','variant')],[('rank1_factor_cache_trial',)])
assert exact(spec['rank1_factor_cache_trial']['actual_combined_runtime_admission'],api)
parent_decl=read(fc['OLD']/'declaration.json')
restored(decl,parent_decl,[('experiment_id',),('case_spec',),('rank_addendum',),('resource_roots',),('conditional_white_receiver_variant',),('helper',),('inputs','material_results')],[('rank1_factor_cache_revision',),('rank1_factor_cache_equivalence',),('rank1_factor_cache_resource_admission',)])
variant=read(SOURCE/'conditional_white_receiver_variant.json');parent_variant=owned(m['parent_variant'])
restored(variant,parent_variant,[('candidate_runtime',),('files',)],[('rank1_factor_cache_revision',)])
producer=read(SOURCE/'producer_ingestion_receipt.json');parent_producer=owned(m['parent_producer_receipt'])
restored(producer,parent_producer,[('online_receiver_sha256',),('conditional_white_receiver_variant',),('scope',)],[('rank1_factor_cache_revision',)])
assert m['original_inputs']==parent_decl['inputs']and producer['states']==parent_producer['states']
assert decl['budgets']==gate['budgets']==parent_decl['budgets']==dict(setup_seconds=120,bootstrap_axial_seconds=4200,bootstrap_radial_seconds=600,radial_seconds=300,axial_seconds=4200,host_seconds=120,max_maps=100,total_seconds=43200)
assert decl['production_config']==gate['production_config']==parent_decl['production_config']
assert gate['four_thresholds']==dict(radial=2.5e-7,axial=5e-8,MCCG=2.5e-8,coupled_outer=5e-7)
resources=read(SOURCE/'resource_admission.json')
assert resources['unchanged_history_cap_bytes']==96*2**30 and resources['unchanged_min_free_bytes']==8*2**30 and resources['retries']==0 and resources['threads']==1 and resources['numeric_children_at_once']==1
env=read(SOURCE/'analysis_environment.json');assert set(env['thread_environment'].values())=={'1'}and all(env[k]is False for k in ['original_exact_dictionary_comparison_changed','original_numerical_rules_changed','transport_started'])
for obj in [m,gate]:
    for key in ['AAA_accuracy_qualified','ABA_admitted','reference_qualification_created']:assert obj[key]is False

report=dict(schema='AXMAT_V12_ACTUAL_COLD_SOURCE31_DECLARATION_INDEPENDENT_READONLY_REVIEW_V1',status='PASS_ACTUAL_DECLARATION_SOURCE31_INPUT_POINTERS_AND_SOURCE_INVERSES_ONLY',
    source_root=str(SOURCE),source_namespace_file_count=31,seal_member_count=30,full_SOURCE31_normal_namespace_hashes_verified=True,source_has_no_dirs_or_symlinks=True,
    actual_declaration_tool=dict(initial_chunk_id='e23c07',session_id=72878,terminal_chunk_id='dab921',exit_code=0),declaration_terminal=PINS[str(TERM/'declaration_terminal_return.json')],
    actual_declared_source_and_full_stdout_stderr_hashes_and_typed_tool_records_match=True,stderr_empty=True,
    runtime_original_complete_inverse=runtime_inverses,seven_unchanged_original_pipeline_files_byteexact=True,six_current_helper_and_consumer_copies_byteexact=True,
    generated_admission_host=generated_host_inverse,generated_host8_definitions_and_body_whole_inverse=True,metadata_schema=fc['CALLBACK_METADATA_SCHEMA'],
    whole_input_external_pointer_and_complete36804_descriptor_pins_preserved=True,whole_input_aliases186_preserved=True,complete30key_V11_counts68_scope_preserved=True,
    complete_case_spec_trial_whole_combined_API_return_typed_and_floatbits_equal=True,metadata_all_seven_runtime_source_pins_exact=True,metadata_file_pin_map_entries=len(m['files']),
    original_case_spec_declaration_variant_and_producer_whole_restore_exact=True,all_A_B_material_snapshot_tracking_and_reference_inputs_unchanged=True,
    original_budget_fields=decl['budgets'],original_production_config=decl['production_config'],four_original_thresholds=gate['four_thresholds'],original_512_96GiB_8GiB_threads1_child1_retries0_preserved=True,
    no_business_module_import=True,no_business_call=True,no_phase_or_fixture_execution=True,no_Root_session_poll=True,no_project_write=True,no_historical_payload_mass_hash=True,
    preparation_result_not_observed_or_claimed=True,cold_prepared=False,native_RSS_verified=False,actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False,evidence_pins=PINS)
text=json.dumps(report,ensure_ascii=False,indent=2)+'\n';(D/'REPORT_SOURCE31.json').write_text(text)
print(json.dumps(dict(status=report['status'],report=str(D/'REPORT_SOURCE31.json'),report_sha256=sha(text),source_files=31,runtime_inverses=3,generated_template_inverse=True,future_PREP_claimed=False,evidence_files=len(PINS)),ensure_ascii=False))
