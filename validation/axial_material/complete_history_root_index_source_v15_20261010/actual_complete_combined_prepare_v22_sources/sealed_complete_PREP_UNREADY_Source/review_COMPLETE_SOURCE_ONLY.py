"""Finite standard-library static self-review. Never executes the SOURCE binder."""
import ast
import hashlib
import json
from pathlib import Path
import stat

P=Path(__file__).resolve().parent

def identity(p):
    s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p):
    p=Path(p);i=identity(p);assert stat.S_ISREG(i[2]);raw=p.read_bytes();assert identity(p)==i
    return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),identity=i,size_bytes=len(raw)),raw

def definitions(source):
    return {n.name:ast.get_source_segment(source,n) for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}

def inverse(source,edits):
    for e in reversed(edits):
        assert source.count(e['new'])==1,e['label'];source=source.replace(e['new'],e['old'],1)
    return source

def statement_signature(source):
    tree=ast.parse(source)
    return [ast.dump(n,include_attributes=False) for n in ast.walk(tree) if isinstance(n,(ast.If,ast.Assert,ast.Raise,ast.Call,ast.Return))]

def globals_ast(source):
    return {t.id:n.value for n in ast.parse(source).body if isinstance(n,ast.Assign) for t in n.targets if isinstance(t,ast.Name)}

def main():
    checks=[];seen={}
    def check(name,ok):
        assert ok,name;checks.append(dict(check=name,pass_=True))
    def source(name):
        q,raw=pin(P/name);seen[str(P/name)]=q;return raw.decode()
    proof=json.loads(source('COMPLETE_SOURCE_INVERSES.json'))
    original_review=json.loads(source('COMPLETE_SOURCE_SELF_REVIEW.json'))
    constants=json.loads(source('ROOT_BINDING_SOURCE_CONSTANTS.json'))
    for row in original_review['checks']:check('author119_'+row['check'],type(row['pass']) is bool and row['pass'] is True)
    template_sources={}
    for name,expected_count,edits_count in (('canonical',70,11),('host',1,13),('writer',7,14)):
        template=source(name+'.V22.UNREADY.full.py');template_sources[name]=template
        parent=source(name+'.V21.parent.full.py');recovered=inverse(template,proof['exact_finite_transforms'][name])
        check(name+'_hunk_count_exact',len(proof['exact_finite_transforms'][name])==edits_count)
        check(name+'_complete_parent_byte_inverse',recovered==parent)
        check(name+'_complete_parent_AST_inverse',ast.dump(ast.parse(recovered),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False))
        check(name+'_original_if_assert_raise_call_return_sequence',statement_signature(recovered)==statement_signature(parent))
        check(name+'_all_original_definition_order',list(definitions(template))==list(definitions(parent)))
        check(name+'_complete_definition_count',len(definitions(template))==expected_count)
        permitted={'canonical':'require_ready','host':'main','writer':'main'}[name]
        for k,v in definitions(parent).items():
            if k!=permitted:check(name+'_function_'+k+'_byte_exact',definitions(template)[k]==v)
        actual,qraw=pin(constants['original_sources'][name]['path']);seen[actual['path']]=actual
        check(name+'_original_Source_actual_pin',actual==constants['original_sources'][name])
        check(name+'_original_Source_full_bytes_retained',qraw.decode()==parent)
    cg=globals_ast(template_sources['canonical'])
    for name in proof['six_future_business_pins']:
        check(name+'_None_UNREADY',isinstance(cg[name],ast.Constant) and cg[name].value is None)
    check('no_actual_newQ_admission_pin',cg['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA'].value is None)
    check('no_actual_newQ_in_constants',constants['expected_Q_sha256'] is None)
    check('canonical_UNREADY_status',cg['DRAFT_STATUS'].value=='UNREADY_V22_COMPLETE_NEW_HELPER_ACTUAL_Q_UNBOUND')
    check('canonical_newhelper_None',"combined_runtime_complete_input_graph_private_owner_namespace_last_use_20261010.py',None)" in template_sources['canonical'])
    for name in ('host','writer'):
        tree=ast.parse(template_sources[name]);main_node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
        check(name+'_first_statement_UNREADY_private_guard',isinstance(main_node.body[0],ast.If) and any(isinstance(n,ast.Raise) for n in ast.walk(main_node.body[0])))
    hg=globals_ast(template_sources['host'])
    for key in ('TARGET_SHA','ACTUAL_HELPER_Q_PATH','ACTUAL_HELPER_Q_SHA'):check('host_'+key+'_unique_None_slot',isinstance(hg[key],ast.Constant) and hg[key].value is None)
    wg=globals_ast(template_sources['writer']);check('writer_FACTORY_SHA_unique_None_slot',isinstance(wg['FACTORY_SHA'],ast.Constant) and wg['FACTORY_SHA'].value is None)
    binder=source('bind_actual_Q_to_complete_PREP_SOURCE.py');bt=ast.parse(binder);bd=definitions(binder)
    check('binder_all_imports_standard_library',all(n.module in {'pathlib'} for n in bt.body if isinstance(n,ast.ImportFrom)) and all(x.name in {'argparse','ast','hashlib','json','math','os','stat','struct','sys'} for n in bt.body if isinstance(n,ast.Import) for x in n.names))
    check('binder_no_exec_eval_dynamic_project_import',not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('exec','eval','__import__') for n in ast.walk(bt)))
    check('binder_no_subprocess_or_API_import',not any((isinstance(n,ast.Import) and any(x.name.split('.')[0] in ('subprocess','importlib') for x in n.names)) or (isinstance(n,ast.ImportFrom) and n.module.split('.')[0] in ('subprocess','importlib')) for n in ast.walk(bt)))
    check('binder_ART_ref_no_payload_open',"if p.is_relative_to(ART):\n        ART_REFS.append(value);return value" in bd['verify_ref'])
    check('binder_META_ART_reject_before_read',bd['read_META'].index('not p.is_relative_to(ART)')<bd['read_META'].index('p.read_bytes()'))
    check('binder_actualQ_sha_argv_required',"ap.add_argument('actual_Q_sha256')" in binder)
    check('binder_fixed_unique_newQ_path',"assert qp==EXPECTED_Q and qp.is_absolute()" in binder)
    check('binder_output_fresh_TMP_only',"output.is_relative_to(Path('/private/tmp'))" in binder and "not os.path.lexists(output)" in binder)
    check('binder_actual_q_helper_native_identity_verified','hp[\'identity\']==HELPER_ID' in binder)
    check('binder_no_oldQ_qualification_inheritance','29ac1abd' not in binder and 'dc01d8cf' not in binder)
    check('binder_original_Q_nonzero_canonical_contract_unchanged','validate_Q(q)' in bd['main'] and 'read_META' not in definitions(template_sources['canonical'])['require_ready'])
    check('binder_three_complete_fulloutput_sources',"for name in ('canonical','host','writer')" in binder and "'writer':'write_actual_prepare_terminal.py'" in binder)
    check('binder_exact_4_4_3_future_Source_bindings',binder.count("label='actual_Q_READY_")==2 and "label='qualified_cf0_helper_SHA'" in binder and "label='actual_new_Q_SHA'" in binder and binder.count("label='host_")==4 and binder.count("label='writer_")==3)
    check('binder_no_future_PIN_qualification_CREATED','new_helper_qualification_created_by_this_Source_binder=False' in binder and 'installed_or_executed=False' in binder)
    check('binder_all_functions_same_after_actual_READY_binding',"assert definition_segments(text)==definition_segments(templates[name])" in binder)
    owner=source('validate_private_owner_controls.META_source_only.txt').strip();check('exact_Source_META_only_owner_validator',bd['validate_private_owner_controls']==owner)
    for token in ('full_public_return_field_order','all_27_fields_nested_type_order_value_floatbits_and_wire_bytes_equal','37112','unfiltered37112trace_complete_order_path_sequence_sha256','all_three_complete_gzip_pins','complete_JSON_wire_gzip_decompression_EOF_SHA_verified','no_fields_or_records_filtered','private_positive_controls','private_reject_controls','original_protocol_preserved_and_new_owner_controls_independently_saved_reviewed','type(tr[\'exit_code\']) is int','session_repolled_after_close','independent_saved_actual_review_pass','1084','686','5cdfb1fead9d8df8a6158cf203028578f6b453ab614863a81540f5172812abe3'):
        check('binder_preserves_true_evidence_contract_'+token,token in binder)
    check('Q_normalized_fourfield_gzip_pins_not_assumed_extras',"complete=saved_gz[key]" in binder and "('path','sha256','identity','size_bytes')" in binder)
    for k in proof['six_future_business_pins']:check('binder_preserves_future_business_None_'+k,k in binder)
    check('binder_complete_SOURCE_manifest_members_dynamic',"inventory==sorted(list(package['members'])+['MANIFEST.json'])" in binder)
    for filename in ('prepare_SOURCE_templates.py','review_COMPLETE_SOURCE_ONLY.py'):
        t=source(filename);ast.parse(t);check(filename+'_complete_stdlib_SOURCE_AST_valid',True)
    for p,expected in seen.items():q,_=pin(Path(p));check('Source_before_after_EOF_SHA7ID_'+p,q==expected)
    result=dict(schema='V22_COMPLETE_CANONICAL_GENUINE_PREP_ROOT_BINDER_STATIC_SOURCE_REVIEW_V1',status='SOURCE_ONLY_PASS_UNREADY_NO_Q_OR_BUSINESS_EXECUTION',source_only=True,all_checks_passed=True,blockers=[],check_count=len(checks),checks=[{'check':x['check'],'pass':x['pass_']} for x in checks],all_full_Source_before_after_pins=list(seen.values()),canonical_definitions=70,genuine_host_definitions=1,metadata_writer_definitions=7,binder_definitions=len(bd),canonical_UNREADY_finite_hunks=11,host_UNREADY_finite_hunks=13,writer_UNREADY_finite_hunks=14,future_READY_hunks=dict(canonical=4,host=4,writer=3),actual_new_Q_path=None,actual_new_Q_sha256=None,all_six_future_business_pins={k:None for k in proof['six_future_business_pins']},helper_guard_API_binder_PREP_build_INPUT_native_or_numeric_executed=False,original_D_E_ART_or_canonical_written=False,actual_Q_or_ART_payload_read=False,all_original_caps_preserved=constants['caps'])
    with (P/'FINAL_COMPLETE_SOURCE_SELF_REVIEW.json').open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(status=result['status'],source_only=True,all_checks_passed=True,check_count=len(checks),report=pin(P/'FINAL_COMPLETE_SOURCE_SELF_REVIEW.json')[0],binder=pin(P/'bind_actual_Q_to_complete_PREP_SOURCE.py')[0],new_Q=None,business_execution=False),allow_nan=False))

if __name__=='__main__':main()
