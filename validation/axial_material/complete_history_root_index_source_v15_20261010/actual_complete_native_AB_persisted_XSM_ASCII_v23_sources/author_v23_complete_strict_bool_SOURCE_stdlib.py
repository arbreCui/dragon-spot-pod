"""Author a complete SOURCE-only derivative; never import/execute any candidate."""
from pathlib import Path
import ast, copy, hashlib, json, shutil

P=Path(__file__).parent
PARENT=Path('/private/tmp/axmat_native_host_BINDER_STRICT_SCOPE_UNREADY_SOURCE_20261010_gs2tnzvo')
BOUND=Path('/private/tmp/axmat_complete_native_actual_BOUND_SOURCE_ROOT_20261010_503adf')
BASE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
ART=Path('/Users/wen/spot/validation/artifacts')
E=BASE/'actual_complete_native_AB_persisted_XSM_ASCII_v22_receipts'
H=ART/'axial-material-complete-native-AB-persisted-XSM-ASCII-host-v22-20261010'
PARENT_SHA='f1b5cd5fc1b01077b1fc181c5da1199020570ff7c9ba569355f875c0f5bd4ffa'
BOUND_SHA='bce973287d8776ddcfca502494f9f9dff0113d653aa316666ebfa962a4ea74d9'
CHECKER_NAME='complete_native_XSM_ASCII_checker_v4.UNREADY.py'
HOST_NAME='complete_native_XSM_ASCII_genuine_host.UNREADY.py'
BINDER_NAME='bind_complete_native_SOURCE_only.UNREADY.py'
CHECKER_SHA='5c50b197032b8875b9b800c0b3d8301f922846871f9d90d3190960b1e62eaf1e'
HOST_SHA='9cd50de1033ee0c598500fc54e8b92137ecc746dd9b07dce4dd4c7f88686d42e'
BINDER_SHA='1ec6f89d00d4b72aa1a5ed70e7bdca95e8267ead7c07aa5351daa70ae64bc585'

def identity(path):
    s=path.lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    before=identity(path);raw=path.read_bytes();after=identity(path)
    assert before==after and len(raw)==before[4]
    return {'path':str(path),'sha256':hashlib.sha256(raw).hexdigest(),'size_bytes':len(raw),'identity':before}
def write(name,value):
    f=P/name;assert not f.exists()
    f.write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def dump(node):return ast.dump(node,include_attributes=False)
def defs(tree):return {n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
def segment(text,node):return ''.join(text.splitlines(keepends=True)[node.lineno-1:node.end_lineno])
checks=[]
def check(name,condition,evidence=None):
    passed=bool(condition);checks.append({'check':name,'passed':passed,'evidence':evidence});assert passed,name
def verified_package(root,manifest_name,sha,expected_members):
    manifest_path=root/manifest_name;mp=pin(manifest_path);assert mp['sha256']==sha
    v=json.loads(manifest_path.read_bytes());members=v['members']
    if type(members)is dict:
        entries=[dict(relative_path=relative,**entry)for relative,entry in members.items()]
    else:entries=members
    assert len(entries)==expected_members
    paths={str(f.relative_to(root))for f in root.rglob('*')if f.is_file()}
    assert paths=={e.get('relative_path',e.get('relative'))for e in entries}|{manifest_name}
    actual_pins={}
    for entry in entries:
        relative=entry.get('relative_path',entry.get('relative'));f=root/relative
        actual=pin(f);actual_pins[relative]=actual
        if 'path'in entry:assert actual['path']==entry['path']
        assert actual['sha256']==entry['sha256']
        assert actual['size_bytes']==entry.get('size_bytes',entry.get('bytes'))
        assert actual['identity']==entry['identity']
    for f in root.rglob('*'):assert not f.is_symlink()
    actual_pins[manifest_name]=mp
    return actual_pins,{str(f):identity(f)for f in root.rglob('*')if f.is_dir()},identity(root)

parent_pins,parent_dirs,parent_root=verified_package(PARENT,'MANIFEST.json',PARENT_SHA,82)
bound_pins,bound_dirs,bound_root=verified_package(BOUND,'Root_actual_complete_bound_native_SOURCE_manifest.json',BOUND_SHA,88)
check('complete_fixed_parent_82_members_plus_manifest',len(parent_pins)==83)
check('complete_actual_V22_bound_88_members_plus_manifest',len(bound_pins)==89)
shutil.copytree(PARENT,P/'ORIGINAL_STRICT_SCOPE_V22_SOURCE')
shutil.copytree(BOUND,P/'ORIGINAL_ACTUAL_BOUND_V22_SOURCE')
# The original relative data path is required by the unchanged genuine binder.
shutil.copytree(PARENT/'ORIGINAL_FIXED_HOST_BINDER_SOURCE',P/'ORIGINAL_FIXED_HOST_BINDER_SOURCE')
for name in (HOST_NAME,BINDER_NAME):shutil.copyfile(PARENT/name,P/name)
parent_checker=(PARENT/CHECKER_NAME).read_bytes()
check('original_checker_fixed_SHA',hashlib.sha256(parent_checker).hexdigest()==CHECKER_SHA)
old="    require(type(inputs) is list and inputs, 'complete explicit input pins required')\n"
new="    require(type(inputs) is list and len(inputs)>0, 'complete explicit input pins required')\n"
text=parent_checker.decode()
check('one_original_invalid_condition_anchor',text.count(old)==1)
candidate=text.replace(old,new,1)
(P/CHECKER_NAME).write_text(candidate)
restored=candidate.replace(new,old,1)
check('one_hunk_full_bytes_inverse_to_5c50',restored.encode()==parent_checker)
pt,ct=ast.parse(text),ast.parse(candidate)
check('full_AST_inverse_to_5c50',dump(ast.parse(restored))==dump(pt))
check('all_17_checker_definitions_preserved',list(defs(pt))==list(defs(ct))and len(defs(pt))==17)
for name,original in defs(pt).items():
    if name!='main':
        check('unchanged_checker_complete_definition_'+name,segment(text,original)==segment(candidate,defs(ct)[name])and dump(original)==dump(defs(ct)[name]))
old_call=next(x for x in ast.walk(pt)if isinstance(x,ast.Call)and isinstance(x.func,ast.Name)and x.func.id=='require'and ast.unparse(x.args[0])=='type(inputs) is list and inputs')
new_call=next(x for x in ast.walk(ct)if isinstance(x,ast.Call)and isinstance(x.func,ast.Name)and x.func.id=='require'and ast.unparse(x.args[0])=='type(inputs) is list and len(inputs) > 0')
check('original_strict_require_and_error_text_retained',dump(defs(pt)['require'])==dump(defs(ct)['require'])and dump(old_call.func)==dump(new_call.func)and dump(old_call.args[1])==dump(new_call.args[1]))
normalized=copy.deepcopy(ct)
for x in ast.walk(normalized):
    if isinstance(x,ast.Call)and isinstance(x.func,ast.Name)and x.func.id=='require'and dump(x.args[0])==dump(new_call.args[0]):x.args[0]=copy.deepcopy(old_call.args[0])
check('only_one_AST_condition_changed_complete_Source',dump(normalized)==dump(pt))
for name,sha in ((HOST_NAME,HOST_SHA),(BINDER_NAME,BINDER_SHA)):
    raw=(P/name).read_bytes()
    check('complete_bytes_AST_unchanged_'+name,raw==(PARENT/name).read_bytes()and hashlib.sha256(raw).hexdigest()==sha and dump(ast.parse(raw))==dump(ast.parse((PARENT/name).read_bytes())))
    for n in defs(ast.parse(raw)):
        check('every_full_definition_unchanged_'+name+'_'+n,
              segment(raw.decode(),defs(ast.parse(raw))[n])==segment((PARENT/name).read_text(),defs(ast.parse((PARENT/name).read_bytes()))[n]))
check('all_checker_globals_and_original_caps_unchanged',
      [dump(n)for n in pt.body if not isinstance(n,(ast.FunctionDef,ast.ClassDef))]==[dump(n)for n in ct.body if not isinstance(n,(ast.FunctionDef,ast.ClassDef))])
for relative,before in parent_pins.items():
    local=P/'ORIGINAL_STRICT_SCOPE_V22_SOURCE'/relative
    check('entire_parent_file_preserved_'+relative,local.read_bytes()==(PARENT/relative).read_bytes())
for relative,before in bound_pins.items():
    local=P/'ORIGINAL_ACTUAL_BOUND_V22_SOURCE'/relative
    check('entire_actual_bound_file_preserved_'+relative,local.read_bytes()==(BOUND/relative).read_bytes())
actual_binding=json.loads((BOUND/'Root_actual_native_SOURCE_binding.json').read_bytes())
blueprint=json.loads((P/'ORIGINAL_FIXED_HOST_BINDER_SOURCE/PARENT_NATIVE_SOURCE/ROOT_BINDING_BLUEPRINT.UNREADY.json').read_bytes())
inputs=actual_binding['complete_input_pins']
check('actual_bound_complete_129_LIST_not_missing_or_wrong_key',type(inputs)is list and len(inputs)==129)
check('all129_pins_exact_original_blueprint',inputs==blueprint['complete_input_pins'])
check('all129_unique_paths_and_full4pinfields',len({q['path']for q in inputs})==129 and all(set(q)=={'path','sha256','size_bytes','identity'}for q in inputs))
for index,q in enumerate(inputs):
    check('typed_metadata_original_pin_'+str(index),type(q['path'])is str and type(q['sha256'])is str and type(q['size_bytes'])is int and type(q['identity'])is list and len(q['identity'])==7 and all(type(v)is int for v in q['identity']))
# This explicit Python expression operates only on saved pin META. It is not
# import/eval/exec of a candidate, reader, checker, guard or material algorithm.
old_value=type(inputs)is list and inputs
new_value=type(inputs)is list and len(inputs)>0
check('old_actual_129_condition_returns_LIST',type(old_value)is list and len(old_value)==129)
check('new_actual_129_condition_is_exact_bool_True',type(new_value)is bool and new_value is True)
cases=[]
for name,value in [('empty_list',[]),('None',None),('empty_dict',{}),('tuple',()),('False',False),('True',True),('zero',0),('nonempty_string','invalid')]:
    result=type(value)is list and len(value)>0
    check('new_condition_wrong_or_empty_exact_bool_False_'+name,type(result)is bool and result is False)
    cases.append({'case':name,'input_type':type(value).__name__,'result_type':type(result).__name__,'result':result})

failure_files=[
 (E/'Root_actual_complete_native_tool_terminal_return.json','dd6d7b78e8118006be63a745d6ec6f6afe9c802027ed582e06c9d2b11c6c5060'),
 (E/'Root_actual_complete_native_postclose_summary.json','2f464d12e72229451fe8203e3ca39b0e2a06a25a44022841ebcb26c432b2d94d'),
 (E/'Root_actual_complete_native_postclose_namespace_manifest.json','722c4f17d7c5212658a794e6d51fa13cfa90bc49590f7d69baf962d31f0507f8'),
 (E/'Root_actual_complete_native_postclose_META_writer_tool_return.json','dad973c0bede0a8e520f3006079169f781cdf71a3e6e43984f51ea6fd0be6e0b'),
 (E/'Root_complete_native_D_source_freeze.json','2f83e196c5f86020ae0a66e1ee53deee174bfeac8808352653b511d058c3d0ea'),
 (E/'Root_actual_native_prelaunch_frozen_D_E.json','4a8c84c2a867d2b492ad7afa5cfbe10651a19641059fcfca5b39eead38586c3f'),
 (E/'Root_actual_complete_native_merged_external_host_stdout_stderr.log',None),
 (H/'native_run/native_xsm_ascii.log',None),
 (H/'native_run/native_xsm_ascii.watchdog.json',None),
 (H/'failed_host_result.json',None),
]
failure_pins=[]
for f,expected in failure_files:
    actual=pin(f);check('fixed_actual_failure_META_'+f.name,expected is None or actual['sha256']==expected)
    dest=P/'ACTUAL_V22_FAILED_SOURCE_AND_META'/('HOST'if f.is_relative_to(H)else'RECEIPTS')/f.relative_to(H if f.is_relative_to(H)else E)
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,dest)
    failure_pins.append(actual)
terminal=json.loads((E/'Root_actual_complete_native_tool_terminal_return.json').read_bytes())
tr=terminal['terminal_tool_return']
check('actual_efc410_typed_EXIT1_CLOSED_no_repoll',terminal['closed']is True and terminal['observed_terminal']is True and terminal['session_repolled_after_close']is False and terminal['actual_terminal_chunk']=='efc410'and tr['chunk_id']=='efc410'and type(tr['exit_code'])is int and tr['exit_code']==1 and 'session_id'not in tr)
summary=json.loads((E/'Root_actual_complete_native_postclose_summary.json').read_bytes())
check('actual_failure_no_native_report_or_scope_qualification',summary['actual_child_report']is None and summary['actual_host_result']is None and summary['native_persisted_XSM_value_bits_verified']is False and summary['all_complete_A_B_scopes_retained_and_verified']is False and summary['actual_native_byte_qualification_sha256']is None)
log=(H/'native_run/native_xsm_ascii.log').read_text()
check('actual_child_failed_at_exact_old_condition_before_material_comparison',old.strip()in log and 'ValueError: complete explicit input pins required'in log)

def boolean_shape(node):
    if isinstance(node,ast.Compare):return True,'comparison returns bool'
    if isinstance(node,ast.UnaryOp)and isinstance(node.op,ast.Not):return True,'not returns bool'
    if isinstance(node,ast.Constant)and type(node.value)is bool:return True,'exact bool constant'
    if isinstance(node,ast.BoolOp):
        result=[boolean_shape(n)for n in node.values]
        return all(ok for ok,_ in result),'all boolean operands'if all(ok for ok,_ in result)else'requires local name/function provenance or rejecting short-circuit analysis'
    if isinstance(node,ast.Call):
        name=ast.unparse(node.func)
        if name in ('all','any','bool','math.isfinite','stat.S_ISREG','stat.S_ISLNK','stat.S_ISDIR')or name.endswith(('.is_absolute','.is_relative_to','.is_dir','.is_symlink','.exists')):
            return True,'standard-library/builtin boolean-return function'
        if name=='finite':return True,'complete original nested finite returns all or comparison/or of boolean operands'
    if isinstance(node,ast.Name)and node.id in ('ended','full'):
        return True,'complete Source assignments inspected: ended=False/True; full=all(...)'
    return False,'not proven boolean as an arbitrary operand'
audits=[]
for filename in (CHECKER_NAME,HOST_NAME,BINDER_NAME):
    source=(P/filename).read_text();tree=ast.parse(source)
    for call in sorted([x for x in ast.walk(tree)if isinstance(x,ast.Call)and isinstance(x.func,ast.Name)and x.func.id=='require'],key=lambda x:x.lineno):
        shape,reason=boolean_shape(call.args[0]);expression=ast.unparse(call.args[0])
        rejecting=False
        if not shape and expression=='name and name not in names':
            # XSM.directory constructs name as .decode('ascii'). Empty str is
            # rejected under strict require; nonempty valid names reach bool
            # membership comparison. This is not a valid-path LIST terminal.
            rejecting=True;reason='original name is decoded str; empty name returns empty str and is intentionally rejected; every nonempty name reaches boolean not-in comparison'
        check('finite_all_strict_require_condition_'+filename+'_'+str(call.lineno),shape or rejecting,{'expression':expression,'boolean_on_valid_path':shape or rejecting,'false_only_nonbool_short_circuit_preserved':rejecting,'reason':reason})
        audits.append({'Source_role':filename,'line':call.lineno,'expression':expression,'bool_for_all_typed_values_proven':shape,'nonbool_false_operand_intentionally_rejected':rejecting,'reason':reason})
check('only_one_remaining_false_only_nonbool_operand_no_valid_nonbool_terminal',sum(a['nonbool_false_operand_intentionally_rejected']for a in audits)==1 and all(a['bool_for_all_typed_values_proven']or a['nonbool_false_operand_intentionally_rejected']for a in audits))

namespaces={
 'host':str(ART/'axial-material-complete-native-AB-persisted-XSM-ASCII-host-v23-20261010'),
 'output':str(ART/'axial-material-complete-native-AB-persisted-XSM-ASCII-output-v23-20261010'),
 'control':str(ART/'axial-material-complete-native-AB-persisted-XSM-ASCII-controls-v23-20261010'),
 'source':str(BASE/'actual_complete_native_AB_persisted_XSM_ASCII_v23_sources'),
 'receipts':str(BASE/'actual_complete_native_AB_persisted_XSM_ASCII_v23_receipts'),
}
request=json.loads((PARENT/'ROOT_SOURCE_REQUEST_TEMPLATE.UNREADY.json').read_bytes())
request['namespaces']=namespaces
write('ROOT_SOURCE_REQUEST_TEMPLATE.UNREADY.json',request)
check('same_exact_original_request_contract_only_fresh_namespace_values',dict(request,namespaces={k:None for k in namespaces})==json.loads((PARENT/'ROOT_SOURCE_REQUEST_TEMPLATE.UNREADY.json').read_bytes()))
check('all_true_admission_peer_tool_BUILD_pins_unknown_None',all(request[k]is None for k in ('source_admission_pin','actual_Root_Source_admission_tool_return_pin','independent_host_binder_Source_review_pin','prior_actual_V22_build_tool_return_pin')))
check('same_V22_BUILD_actual_schema_required_not_v23_fake_or_PREP',request['actual_prior_BUILD_tool_contract']['schema']=='ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1'and request['actual_prior_BUILD_tool_contract']['PREP_cannot_substitute_BUILD']is True)
check('all_five_v23_paths_nonoverlap_and_correct_ART_BASE_Source_scope',len(set(namespaces.values()))==5 and all(Path(namespaces[k]).is_relative_to(ART)for k in ('host','output','control'))and all(Path(namespaces[k]).is_relative_to(BASE)for k in ('source','receipts'))and all(not Path(a).is_relative_to(Path(b))for a in namespaces.values()for b in namespaces.values()if a!=b))
blueprint_input_file=P/'ORIGINAL_FIXED_HOST_BINDER_SOURCE/PARENT_NATIVE_SOURCE/ROOT_BINDING_BLUEPRINT.UNREADY.json'
rolepins={'host_template':pin(P/HOST_NAME),'checker_template':pin(P/CHECKER_NAME),'binder':pin(P/BINDER_NAME)}
write('V23_SOURCE_ROLES_AND_FRESH_ROOT_NAMESPACES.UNREADY.json',{
 'schema':'COMPLETE_NATIVE_V23_STRICT_BOOL_FAMILY_SOURCE_DESIGN_V1','status':'UNREADY_SOURCE_ONLY_REQUIRES_NEW_ACTUAL_SOURCE_ADMISSION_AND_BINDING','source_only':True,
 'qualified_source_manifest':None,**rolepins,'future_namespaces':namespaces,
 'original_full129_input_blueprint_pin':pin(blueprint_input_file),'original_input_count':129,
 'Root_must_observe_namespace_absence_before_bind_and_run':True,'future_actual_Source_admission':None,
 'future_actual_Source_admission_terminal':None,'future_actual_Source_peer':None,'future_actual_Source_binding_tool':None,
 'actual_native_byte_qualification_sha256':None,'actual_scientific_qualification_sha256':None,
 'no_new_Q_or_Root_receipt_fabricated':True,'prior_actual_failed_BUILD_stays_V22_original_schema':True,
 'original_caps':actual_binding['original_caps'],'all129_material_payloads_read_here':False,
 'six_future_business_pins':[None]*6,'all_science_qualified':False})
write('ONE_HUNK_COMPLETE_CHECKER_SOURCE_INVERSE.json',{
 'schema':'V23_COMPLETE_NATIVE_STRICT_BOOL_ONE_HUNK_FULL_SOURCE_INVERSE_V1','source_only':True,
 'parent_checker_pin':parent_pins[CHECKER_NAME],'new_checker_pin':pin(P/CHECKER_NAME),
 'hunks':[{'old_utf8':old,'new_utf8':new,'unique_old_anchor':True,'unique_new_anchor':True}],
 'full_bytes_inverse_to_5c50':True,'full_AST_inverse':True,'complete_checker_definitions':17,
 'other_16_definitions_full_bytes_AST_unchanged':True,'host_complete_bytes_AST_unchanged':True,'binder_complete_bytes_AST_unchanged':True,
 'default_public_native_algorithm_inputs_caps_changed':False,
 'actual_V22_bound_original_checker_pin':bound_pins['Root_bound_complete_native_checker.py'],
 'actual_V22_bound_checker_functions_same_as_original':dump(defs(ast.parse((BOUND/'Root_bound_complete_native_checker.py').read_bytes()))['main'])==dump(defs(pt)['main']),
 'old_parent_and_actual_bound_complete_Source_inventory_retained':True,'new_native_or_physics_PASS':False})
write('ALL_STRICT_REQUIRE_SOURCE_CONDITION_AUDIT.json',{
 'schema':'COMPLETE_NATIVE_ALL_STRICT_REQUIRE_BOOL_CONDITIONS_FINITE_SOURCE_AUDIT_V1','source_only':True,
 'complete_Source_roles':rolepins,'conditions':audits,'condition_count':len(audits),
 'original_true_path_LIST_terminal_fixed':{'old':ast.unparse(old_call.args[0]),'new':ast.unparse(new_call.args[0]),'original_line':old_call.lineno,'actual_saved_input_type':'list','actual_saved_input_count':129},
 'one_preserved_false_only_nonbool_operand':'name and name not in names returns empty str only for a rejected blank name; valid nonempty name always reaches bool membership test',
 'original_Source_name_construction':"name_raw.split(b'\\0', 1)[0].rstrip(b' ').decode('ascii')",
 'complete_Source_proven_bool_names':{'ended':'assigned exact False or True in compare_ascii','full':'assigned builtin all(...) in main'},
 'Source_only_actual_pin_META_expression_demonstration':{'original_result_type':type(old_value).__name__,'original_length':len(old_value),'new_result_type':type(new_value).__name__,'new_result':new_value,'empty_and_wrongtype_cases':cases},
 'no_candidate_function_or_payload_executed':True,'does_not_grant_native_RSS_bits_or_science':True})
for rel,original in parent_pins.items():check('parent_EOF_SHA7ID_unchanged_'+rel,pin(PARENT/rel)==original)
for rel,original in bound_pins.items():check('actual_bound_EOF_SHA7ID_unchanged_'+rel,pin(BOUND/rel)==original)
check('parent_directories_and_root7ID_unchanged',parent_dirs=={str(f):identity(f)for f in PARENT.rglob('*')if f.is_dir()}and parent_root==identity(PARENT))
check('actual_bound_directories_and_root7ID_unchanged',bound_dirs=={str(f):identity(f)for f in BOUND.rglob('*')if f.is_dir()}and bound_root==identity(BOUND))
for fp in failure_pins:check('actual_failure_META_before_after_'+Path(fp['path']).name,pin(Path(fp['path']))==fp)
write('SOURCE_SELF_REVIEW.json',{'schema':'COMPLETE_NATIVE_V23_STRICT_BOOL_COMPLETE_SOURCE_SELF_REVIEW_V1','status':'PASS_SOURCE_ONLY_UNREADY_NO_NATIVE_EXECUTION_OR_SCIENCE',
 'source_only':True,'checks':checks,'check_count':len(checks),'all_checks_typed_true':all(c['passed']is True for c in checks),'blockers':[],
 'original_parent_manifest_pin':parent_pins['MANIFEST.json'],'original_actual_bound_manifest_pin':bound_pins['Root_actual_complete_bound_native_SOURCE_manifest.json'],
 'all_parent_source_pins_before_after_unchanged':True,'all_actual_bound_source_pins_before_after_unchanged':True,'related_actual_failed_META_pins':failure_pins,
 'fixed_current_Source_roles':rolepins,'original_caps':actual_binding['original_caps'],'complete_original_input_pins':129,
 'all_candidate_or_checker_reader_guard_API_business_executed':False,'material_native_or_ASCII_payload_read':False,
 'candidate_Source_only_bool_expression_on_saved_pin_list':True,'actual_new_Source_admission':None,'native_science_Q':None,'all_science_qualified':False})
(P/'ROOT_EXECUTION_SEQUENCE_AND_REQUIRED_PINS.md').write_text('''# Root-only v23 complete native SOURCE procedure

This is a fresh, complete UNREADY v23 family. The only checker code change is `type(inputs) is list and len(inputs)>0`; strict require, all original129 pins, all algorithms and all original caps remain. HOST and BINDER are byte exact to 9cd50/1ec6. ORIGINAL_STRICT_SCOPE_V22_SOURCE retains all83 original mother files; ORIGINAL_ACTUAL_BOUND_V22_SOURCE retains all89 genuine previous bound Source files; ACTUAL_V22_FAILED_SOURCE_AND_META retains the genuine efc410 CLOSED1 failure. That execution stopped before full material bit comparison; no native bit/RSS/scientific qualification is inherited. Do not retry any v22 namespace.

1. Independently review the entire final v23 MANIFEST and complete Source. The generic original peer contract remains schema INDEPENDENT_COMPLETE_NATIVE_GENUINE_HOST_BINDER_SOURCE_REVIEW_V1; status SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE; source_only/all_checks_passed true; blockers[]; check_count equals full unique checks [{check,passed:true}]. Four exact current fullpins must be qualified_source_manifest, host_template, checker_template, binder. Use the new final v23 MANIFEST fullpin and three Source role pins. Historical manifests/reviews inside this package apply only to preserved historical Source.
2. Root writes a NEW actual Source admission using the unchanged ROOT_ACTUAL_COMPLETE_NATIVE_HOST_BINDER_SOURCE_ADMISSION_V1 contract, same exact four current v23 pins plus the actual new peer fullpin; source_only true, status SOURCE_ONLY_ADMITTED_NOT_RUNTIME_OR_SCIENCE, scientific_qualification_created false, new native/science pins None. The genuine Source admission tool output must bind that actual admission fullpin. Save the actual CLOSED0 tool observation under ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1, observed_terminal true, repoll false, exact chunk/typed0/noSession. Do not invent future receipts or use the old v22 Source peer/admission as new v23 admission.
3. Fill ROOT_SOURCE_REQUEST_TEMPLATE.UNREADY.json with the real new Source admission/terminal/Source peer pins, plus the unchanged genuine prior V22 BUILD CLOSED integer terminal pin (65203e EXIT1 is acceptable for persisted byte checking only). The binder requires ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1. A PREP receipt cannot substitute BUILD. All five namespaces already name fresh v23 paths; Root must actually check H/O/C/D absent and separately manage E. The saved v22 native failure is not a BUILD receipt.
4. Run only the unchanged stdlib SOURCE binder, after SOURCE admission:

    python3.12 <this package>/bind_complete_native_SOURCE_only.UNREADY.py --source-manifest-sha256 <final v23 MANIFEST actual SHA> --request <actual Root request path> --request-sha256 <its actual SHA> --output-source-dir <fresh TMP bound SOURCE>

This document intentionally leaves future actual argv pins unknown. Binder preserves every Source member and every original129 four-field pin, writes complete two-checker/eleven-host global inverses, and does not read material arrays or execute checker/guard/API. Root must record the genuine SOURCE tool return, then obtain a complete independent actual-bound Source review before installation/execution.
5. Root installs and freezes the ENTIRE bound Source namespace and admits the original genuine host. Run that host once normally with no extra argv, serially after any Root business child has closed. Retain original genuine guard/MRO/resources and whole1800/stage600/RSS512/jointHOCDE2GiB/history96/free8/thread1/child1/retry0. All129 input and all new Source/peer/admission/build fullpins require fresh full EOF/SHA/7ID before and after. D/E must not mutate during the host; capture actual outer merged stdout/stderr and tools outside frozen E, save only after CLOSED. Inner merged child log/watch in H and every O spool/SQLite/journal/temp remain inside original joint caps. Do not fabricate an empty separate stderr.
6. Save actual success OR nonzero loss/mismatch/structural failure. REAL64 and CHAR/logical export loss remain true failure, all full-stream order/types/bits and complete macro/micro scope remain original. A Source fix is not an assertion the comparison will pass. Historical RAM bits, reaction/transport balance, native build/Source linkage, whole INPUT, AAA/ABA/science remain false/None. Original native walker malformed controls are still unexecuted None; old raw protocol controls retain only their own original scope.
''')
print(json.dumps({'source_only':True,'status':'COMPLETE_V23_SOURCE_ONLY_UNREADY','package':str(P),
                  'checker':pin(P/CHECKER_NAME),'host':pin(P/HOST_NAME),'binder':pin(P/BINDER_NAME),
                  'report':pin(P/'SOURCE_SELF_REVIEW.json'),'check_count':len(checks),'require_condition_count':len(audits),
                  'new_actual_admission':None,'native_checker_executed':False},separators=(',',':')))
