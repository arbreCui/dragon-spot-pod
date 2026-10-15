"""Independent static final C/B/F review; no business import, fixture or session access."""
import ast
import hashlib
import json
from pathlib import Path

D = Path(__file__).resolve().parent
FINAL = Path('/private/tmp/axmat_v12_final_cold_input_candidates_20261009')
BINDER = Path('/private/tmp/axmat_v12_actual_INPUT_bound_cold_B_F_UNREADY_source_binder_20261009')
AUTH = Path('/private/tmp/axmat_v12_cold_binding_authoritative_sources_and_callback_schema_fix_source_only_20261009')
V12 = Path('/private/tmp/axmat_v12_graph_table_cold_source_only_20261009')
V11 = Path('/private/tmp/axmat_v11_cold_component_input_consumer_source_only_20261009')
ROOT = Path('/Users/wen/spot')
FNAME = 'prepare_owned_specs_identity_key_delta_graph_table_cold_runtime_v12.py'
CNAME = 'cold_component_input_consumer_identity_key_delta_graph_table_own_pid_peak_v12.py'
BNAME = 'cold_owned_specs_identity_key_delta_graph_table_component_input_intake_binding_v12_20261009.json'
PINS = {}

def pin(path, expected=None):
    path = Path(path)
    assert path.is_file() and not path.is_symlink(), path
    before = path.stat()
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for data in iter(lambda: stream.read(1 << 20), b''):
            h.update(data)
    after = path.stat()
    assert (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns)
    item = dict(path=str(path),bytes=before.st_size,sha256=h.hexdigest())
    if expected is not None: assert item['sha256']==expected,(path,expected,item['sha256'])
    PINS[str(path)] = item
    return item

def read_json(path, sha=None):
    pin(path, sha)
    return json.loads(Path(path).read_text())

def source(path, sha):
    pin(path, sha)
    text = Path(path).read_text()
    return text, ast.parse(text)

def definitions(text, tree):
    result = {}
    def visit(node, prefix=''):
        for child in ast.iter_child_nodes(node):
            if isinstance(child,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                key=prefix+child.name
                assert key not in result
                start=min([child.lineno]+[n.lineno for n in child.decorator_list])
                result[key]=''.join(text.splitlines(keepends=True)[start-1:child.end_lineno])
                visit(child,key+'.')
            else:visit(child,prefix)
    visit(tree)
    return result

def inverse(text, edits):
    for edit in reversed(edits):
        count=text.count(edit['new'])
        all_literals=edit.get('name','').startswith('literal family identity ')
        assert count>0 and(all_literals or count==1),(edit.get('name'),count)
        text=text.replace(edit['new'],edit['old'])if all_literals else text.replace(edit['new'],edit['old'],1)
    return text

def static_values(tree, names):
    nodes={n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
    cache={}
    def resolve(node):
        try:return ast.literal_eval(node)
        except(ValueError,TypeError):
            if isinstance(node,ast.Name):return get(node.id)
            if isinstance(node,ast.Call)and isinstance(node.func,ast.Name)and node.func.id=='Path'and len(node.args)==1 and not node.keywords:return Path(resolve(node.args[0]))
            if isinstance(node,ast.Call)and isinstance(node.func,ast.Name)and node.func.id=='dict'and not node.args:return {x.arg:resolve(x.value)for x in node.keywords}
            if isinstance(node,ast.BinOp):
                a,b=resolve(node.left),resolve(node.right)
                if isinstance(node.op,ast.Div):return a/b
                if isinstance(node.op,ast.Mult):return a*b
                if isinstance(node.op,ast.Pow):return a**b
                if isinstance(node.op,ast.Add):return a+b
            raise ValueError(ast.dump(node))
    def get(name):
        if name not in cache:cache[name]=resolve(nodes[name])
        return cache[name]
    return {name:get(name)for name in names}

c_report_path=Path('/private/tmp/axmat_v12_final_cold_consumer_independent_source_review_20261009/REPORT.json')
c_report=read_json(c_report_path,'b0161d0bfaa9e3b96513bb93f3b180cad1b9cd28b28c7610562689c1abd3aec7')
c_tool=read_json(c_report_path.parent/'actual_readonly_tool_terminal_return.json','4c80c1a3a2344349c2202a705b1afc4b29ac019bb093f1a63b1b6b5006d7f3c5')
assert c_report['status']=='PASS_SOURCE_AND_ACTUAL_BOUNDED_INPUT_BINDINGS_ONLY_NO_COLD_NATIVE_AAA_ABA'
assert type(c_tool['actual_tool_return']['exit_code'])is int and c_tool['actual_tool_return']['exit_code']==0
pin(FINAL/CNAME,'6688e1fe2967bc63ff12900631e86ae18e30a0ee1bd0b98bb9fbcc4f0ac27823')
bindproof=read_json(BINDER/'source_inverse_proof.json','a417fccb7f48ae80d70c7f0e9b25ec2faa0d623ee24d561ef4305d8fb9987931')
readyproof=read_json(FINAL/'Root_factory_READY_complete_inverse_proof.json','21ca8fe34080f1ae1cd950d77bbe4e34c2b339a29e0b880f2c0a6427b00dffb4')
final,ftree=source(FINAL/FNAME,'7037cf10b98e0f5098a87bb87808940a85132abce48e6156db7b136eddcfbf71')
bound,btree=source(BINDER/FNAME,'30550654e04190cd06d920f8f3d5c5ea50e4cfb4b86de7d41782159d040f11e9')
unbound,utree=source(AUTH/FNAME,'1941375f15d61b44c17ec11e2466048f646112c6c5939ce568c9fdffc84a93a6')
assert len(readyproof['regions'])==2 and inverse(final,readyproof['regions'])==bound
assert len(bindproof['regions'])==16
inverse16=bound
for edit in reversed(bindproof['regions']):
    assert edit['old']=='None'
    assert inverse16[edit['new_start']:edit['new_end']]==edit['new']
    inverse16=inverse16[:edit['new_start']]+edit['old']+inverse16[edit['new_end']:]
assert inverse16==unbound
fdefs=definitions(final,ftree)
assert len(fdefs)==55 and fdefs==definitions(bound,btree)==definitions(unbound,utree)
top_f={n.targets[0].id:ast.get_source_segment(final,n)for n in ftree.body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)}
top_bound={n.targets[0].id:ast.get_source_segment(bound,n)for n in btree.body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)}
top_unbound={n.targets[0].id:ast.get_source_segment(unbound,n)for n in utree.body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)}
assert set(top_f)==set(top_bound)==set(top_unbound)
assert {k for k in top_f if top_f[k]!=top_bound[k]}=={'DRAFT_STATUS'}
assert {k for k in top_bound if top_bound[k]!=top_unbound[k]}=={x['name']for x in bindproof['regions']}
assert top_f['ADMISSION_HOST']==top_unbound['ADMISSION_HOST']

callback=read_json(AUTH/'source_inverse_proof.json','99a4405448cd305be7e5c9eda2589ca12f529d588b8a0ae1ad70aeb0bf3834be')
ancestor_ee=inverse(unbound,callback['edits'])
ee,ee_tree=source(V12/FNAME,'ee7fc7ab17124fe110ec965829710a9cb4c9e19368991b806badbea18422cb3c')
assert ancestor_ee==ee
v12proof=read_json(V12/'source_inverse_proof.json','3dca8c5e1f91be24df0fc671007783d5e316f9e7a9b5fb41052aabf3c3c8f8f7')['proofs'][FNAME]
ancestor_v11=inverse(ancestor_ee,v12proof['edits'])
v11,v11_tree=source(v12proof['parent_path'],v12proof['parent_sha256'])
assert ancestor_v11==v11 and len(v12proof['edits'])==22
v11proof=read_json(V11/'source_inverse_proof.json','e6ed4db3f137f7c50a99f7e27184877a14392a9f8af3b321c1418a28e6e1a4c1')['proofs'][Path(v12proof['parent_path']).name]
ancestor_v10=inverse(ancestor_v11,v11proof['edits'])
genuine_path=ROOT/'validation/axial_material/prepare_historical_input_owned_specs_physical_factor_diagonal_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak_v10.py'
genuine,genuine_tree=source(genuine_path,'bc8eaa6a72e0e732be5f95ef06fe430a2f8e8848d4edba3bedcd53adc29fecf9')
assert ancestor_v10==genuine and len(v11proof['edits'])==29

binding=read_json(FINAL/BNAME,'1e2b3c99e8f09c2716a5e44eca4cb9520339229c6e44a44ae6758d0dcd98d8db')
assert (FINAL/BNAME).read_bytes()==(BINDER/BNAME).read_bytes()
parent_binding=read_json(bindproof['binding_parent']['path'],bindproof['binding_parent']['sha256'])
inverse_b=json.loads(json.dumps(binding))
for edit in reversed(bindproof['binding_JSON_differences']):
    parts=edit['path'].strip('/').split('/')
    obj=inverse_b
    for part in parts[:-1]:obj=obj[part]
    assert obj[parts[-1]]==edit['new']
    obj[parts[-1]]=edit['old']
assert inverse_b==parent_binding and len(bindproof['binding_JSON_differences'])==12
assert (json.dumps(inverse_b,ensure_ascii=False,indent=2)+'\n').encode()==Path(bindproof['binding_parent']['path']).read_bytes()
assert set(binding)==set(parent_binding)

names={x['name']for x in bindproof['regions']}|{'FORMAL_FACTORY_SHA','BINDING_CONTROLS_ACTUAL','DRAFT_STATUS','BUDGETS','ADMISSION_HOST','COMBINED_BUILD','COMBINED_FACTORY','COMBINED_FACTORY_SHA','COMBINED_TERMINAL','COMBINED_RUNTIME','PRIVATE_INPUT_CONSUMER','COMPONENT_INTAKE_DESCRIPTOR'}
names|={name for name in top_f if name.startswith('FUTURE_ACTUAL_COLD_')}
fv=static_values(ftree,names)
assert fv['FORMAL_FACTORY_SHA']is None and fv['BINDING_CONTROLS_ACTUAL']is None
future={k:v for k,v in fv.items()if k.startswith('FUTURE_ACTUAL_COLD_')}
assert len(future)==7 and all(x is None for x in future.values())
assert fv['DRAFT_STATUS']=='REVIEWED_IDENTITY_KEY_DELTA_COLD_INPUT_REUSE_FACTORY_WITH_ACTUAL_BOUNDED_INTAKE'
assert fv['DRAFT_STATUS'] in fdefs['require_input_ready']
assert fv['BUDGETS']==dict(setup_seconds=120,bootstrap_axial_seconds=4200,bootstrap_radial_seconds=600,radial_seconds=300,axial_seconds=4200,host_seconds=120,max_maps=100,total_seconds=43200)
host_ast=ast.parse(fv['ADMISSION_HOST'])
host_defs=definitions(fv['ADMISSION_HOST'],host_ast)
assert len(host_defs)==8
assert 'AXMAT_OWNED_SPECS_IDENTITY_KEY_DELTA_GRAPH_TABLE_SCIPY_ENV_COLD_INPUT_ADMISSION_V12' in fv['ADMISSION_HOST']
admission=read_json(c_report['actual_whole_INPUT_independent_admission']['path'],c_report['actual_whole_INPUT_independent_admission']['sha256'])
root=read_json(binding['actual_bounded_api_terminal_evidence']['path'],binding['actual_bounded_api_terminal_evidence']['sha256'])
api=read_json(binding['api_return']['path'],binding['api_return']['sha256'])
counts=c_report['complete30key_control_counts']
assert binding['actual_V11_component_control_counts']==fv['TRIM_CONTROL_COUNTS']==api['actual_last_cprime_trim_admission']['cache_unit_control_counts']==counts
assert len(counts)==30 and counts['total_declared_stages']==68
assert binding['complete_historical_input_graph']==api['historical_input_graph']
graph=binding['complete_historical_input_graph']
assert graph['sha256']=='4ba5f793ca13018d2d9ac5d29d76827a1503b0368c7e5c9f70ba08e0435f0c9e'and graph['content_sha256']=='ee2cabfd7b93d10bb7c5dc17c01a3d190202faf16eb7d2d8f8125d9507671427'
pin(graph['path'],graph['sha256'])
assert graph['scope']=='COMPLETE_HISTORICAL_INPUT_ONLY'
assert len(binding['intake_namespaces'])==1
ns=binding['intake_namespaces'][0]
nsroot=Path(ns['root'])
assert nsroot==Path(binding['actual_bounded_api_terminal_evidence']['path']).parent
nsfiles=ns['inventory']['files']
assert len(nsfiles)==10 and ns['inventory']['symlinks']=={}
assert set(ns['inventory']['directories'])=={'STANDALONE_BOUNDED_RUNTIME_API_INTAKE','intake','runtime'}
expected_files=dict(root['payload_inventory']['files'])
expected_files['Root_terminal_return.json']=binding['actual_bounded_api_terminal_evidence']['sha256']
assert nsfiles==expected_files
assert binding['intake_proof_files']=={str(nsroot/k):v for k,v in nsfiles.items()}
actual_files={};actual_dirs=[]
for path in nsroot.rglob('*'):
    assert not path.is_symlink(),path
    relative=str(path.relative_to(nsroot))
    if path.is_dir():actual_dirs.append(relative)
    else:actual_files[relative]=pin(path,nsfiles[relative])['sha256']
assert actual_files==nsfiles and sorted(actual_dirs)==sorted(ns['inventory']['directories'])
assert binding['binding_source']==dict(path=str(fv['PRIVATE_INPUT_CONSUMER']),sha256=c_report['candidate']['sha256'])
assert fv['PRIVATE_INPUT_CONSUMER_SHA']==c_report['candidate']['sha256']
assert fv['COMPONENT_INTAKE_DESCRIPTOR_SHA']==PINS[str(FINAL/BNAME)]['sha256']
assert str(fv['COMPONENT_INTAKE_DESCRIPTOR']) not in binding['intake_proof_files'] and str(FINAL/BNAME) not in binding['intake_proof_files']
assert not any('self' in k for k in binding)
expected_helpers={'graph':('combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py','e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28'),'codec':('combined_runtime_typed_specs_codec.py','758c6d39ecb4c37e5ff5b3d6639ab8404447719e7cfd3ff72336276a94bb2e69'),'checks':('combined_runtime_historical_input_checks.py','86e7d6340da59c74abcff57fa52bb07d690f51cc33fe76f330ece2e0d158258e')}
assert set(binding['helper_sources'])==set(expected_helpers)
for key,(name,sha) in expected_helpers.items():
    item=binding['helper_sources'][key]
    assert item==dict(path=str(ROOT/'validation/axial_material'/name),sha256=sha)
    pin(item['path'],sha)
assert binding['expected_complete_descriptor_count']==fv['EXPECTED_API_DESCRIPTOR_COUNT']==len(api['descriptor_files'])==36804
assert binding['expected_complete_alias_count']==fv['EXPECTED_API_ALIAS_COUNT']==len(api['input_aliases'])==186
assert binding['expected_intake_payload_count']==fv['EXPECTED_INTAKE_PAYLOAD_COUNT']==len(root['payload_inventory']['files'])==9
expected16={
    'COMBINED_BUILD_SEAL':api['build_seal_sha256'],
    'COMBINED_TERMINAL_SHA':api['actual_external_terminal_evidence']['sha256'],
    'COMBINED_RUNTIME_SHA':api['corrected_runtime']['sha256'],
    'PRIVATE_INPUT_CONSUMER_SHA':c_report['candidate']['sha256'],
    'COMPONENT_INTAKE_DESCRIPTOR_SHA':PINS[str(FINAL/BNAME)]['sha256'],
    'TRIM_DECL_SHA':c_report['actual_15_fact_bindings']['TRIM_DECL_SHA'],
    'TRIM_SEAL_SHA':c_report['actual_15_fact_bindings']['TRIM_SEAL_SHA'],
    'TRIM_TERMINAL_SHA':c_report['actual_15_fact_bindings']['TRIM_TERMINAL_SHA'],
    'TRIM_OBJECT_SHA':c_report['actual_15_fact_bindings']['TRIM_OBJECT_SHA'],
    'TRIM_RUNTIME_SHA':c_report['actual_15_fact_bindings']['TRIM_RUNTIME_SHA'],
    'TRIM_SOURCE_ADMISSION_SHA':c_report['actual_15_fact_bindings']['TRIM_SOURCE_ADMISSION_SHA'],
    'TRIM_CONTROL_COUNTS':counts,
    'EXPECTED_API_DESCRIPTOR_COUNT':36804,'EXPECTED_API_ALIAS_COUNT':186,'EXPECTED_INTAKE_PAYLOAD_COUNT':9,
    'FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA':api['actual_prepare_terminal_evidence']['sha256']}
assert set(expected16)=={x['name']for x in bindproof['regions']}
assert all(fv[k]==v for k,v in expected16.items())
pin(api['corrected_runtime']['path'],fv['COMBINED_RUNTIME_SHA'])
pin(fv['COMBINED_FACTORY'],fv['COMBINED_FACTORY_SHA'])
for obj in [binding,api,admission]:
    for key in ['science_qualification','AAA_accuracy_qualified','ABA_admitted','cold_prepared','native_RSS_verified']:
        if key in obj:assert obj[key]is False
assert binding['component_API_executed_in_cold_process']is False and binding['production_module_identity_overlay']is False
for name in ['Root_consumer_READY_generation_actual_tool_returns.json','Root_factory_READY_generation_actual_tool_return.json']:
    pin(FINAL/name)
for name in ['actual_binder_tool_terminal_return.json','actual_supplement_tool_terminal_return.json']:
    pin(BINDER/name)

report=dict(schema='AXMAT_V12_FINAL_C_B_F_PREINSTALL_INDEPENDENT_SOURCE_AND_BINDING_REVIEW_V1',status='PASS_PREINSTALL_SOURCE_AND_COMPLETE_ACTUAL_INPUT_BINDINGS_ONLY',
    candidate_C=PINS[str(FINAL/CNAME)],candidate_B=PINS[str(FINAL/BNAME)],candidate_F=PINS[str(FINAL/FNAME)],
    independent_C_report=PINS[str(c_report_path)],independent_C_actual_return=PINS[str(c_report_path.parent/'actual_readonly_tool_terminal_return.json')],
    C_all27_defs_and_62_regions_complete_inverse_previously_verified_and_final_source_unchanged=True,
    F_all55_defs_byteexact_to305_and194=True,F_all8_ADMISSION_HOST_template_defs_byteexact=True,
    F_READY_only_doc_and_status_two_regions=True,F_16_actual_bindings_only_top_level_None_values=True,
    F_two_regions_inverse_to305=True,F_18_regions_inverse_to194=True,F_19_regions_inverse_toee7=True,F_41_regions_inverse_toV11_753abe=True,F_70_regions_inverse_to_genuine_V10_bc8e=True,
    F_full_parent_source_byte_inverse=True,F_all_other_top_assignments_templates_math_MRO_P14_P12_whole7_caps_byteexact=True,
    exact_16_actual_fact_bindings=expected16,F_READY_guard_status_matches=True,
    F_FORMAL_FACTORY_SHA=None,F_BINDING_CONTROLS_ACTUAL=None,F_future_cold7=future,
    B_all_fields_retained=True,B_12_JSON_changes_complete_byte_inverse_to563=True,B_actual_namespace_map_files=10,B_namespaces=1,B_namespace_directories=3,
    B_raw_graph_descriptor_matches_actual_whole_API=True,B_graph_storage_raw_pin_verified=True,B_lossless_content_digest_authority='Already independently admitted actual complete graph; no business helper import or repeated graph decode.',
    B_helpers_complete3_and_real_pins=True,B_consumer_source_sha6688_matches_final=True,B_no_self_sha_descriptor=True,
    descriptor_files=36804,input_aliases=186,intake_payload_files=9,complete_V11_control_counts=counts,complete_V11_control_count_keys=30,component68_scope_retained=True,
    original_cold_budgets=fv['BUDGETS'],genuine_normal_MRO_and_constructor_checks_retained=True,MRO_runtime_not_executed_by_this_review=True,
    no_historical_payload_mass_read=True,no_business_import=True,no_business_call=True,no_fixture_or_CLI_execution=True,no_session_poll=True,no_project_write=True,
    cold_prepared=False,native_RSS_verified=False,actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False,evidence_pins=PINS)
text=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
(D/'REPORT.json').write_text(text)
print(json.dumps(dict(status=report['status'],report=str(D/'REPORT.json'),report_sha256=hashlib.sha256(text.encode()).hexdigest(),Fdefs=55,Cdefs=27,Bfiles=10,Bnamespaces=1,Bdirs=3,counts=30,F_inverse_regions=70,future_cold_None=7),ensure_ascii=False))
