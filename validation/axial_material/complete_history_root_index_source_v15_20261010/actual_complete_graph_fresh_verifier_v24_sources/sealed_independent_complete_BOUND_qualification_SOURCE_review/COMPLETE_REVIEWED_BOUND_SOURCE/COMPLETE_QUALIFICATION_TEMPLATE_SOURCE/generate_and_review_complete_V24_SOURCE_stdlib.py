"""Generate SOURCE only; never import or execute helpers/controllers/guard."""
from pathlib import Path
import ast
import hashlib
import json
import shutil
import stat
import sys

ROOT=Path(__file__).resolve().parent
PARENT=Path('/private/tmp/axmat_inactive_audit_full_qualification_EXACT_META_SOURCE_uuezesbp')
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
E=B/'actual_complete_graph_helper_controls_v23_receipts'
D=B/'actual_complete_graph_helper_controls_v23_sources'
H=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-inactive-audit-helper-controls-host-v23-20261010')
MODULE='inactive_audit_snapshot_controls_SOURCE_ONLY.py'
ROLES=('pure_helper_controls.UNREADY.py','pure_helper_controls_host.UNREADY.py','fresh_verifier_controls.UNREADY.py','fresh_verifier_host.UNREADY.py')
checks=[]
allread={}

def check(label,condition,evidence=None):
    passed=type(condition) is bool and condition is True
    checks.append(dict(check=label,passed=passed,evidence=evidence))
    if not passed:raise AssertionError(label)

def identity(path):
    s=path.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(path):
    path=Path(path);before=identity(path)
    check('regular_one_link:'+str(path),stat.S_ISREG(before[2]) and before[3]==1)
    raw=path.read_bytes();check('full_EOF_stable:'+str(path),identity(path)==before and len(raw)==before[4])
    value=dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before)
    if str(path) in allread:check('repeat_read_unchanged:'+str(path),value==allread[str(path)])
    else:allread[str(path)]=value
    return value

def write(name,value):
    (ROOT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')

def inventory(root,exclude=()):
    files={p.relative_to(root).as_posix():pin(p) for p in sorted(root.rglob('*')) if p.is_file() and p.relative_to(root).as_posix() not in exclude}
    dirs={p.relative_to(root).as_posix():identity(p) for p in root.rglob('*') if p.is_dir()}
    check('no_aliases:'+str(root),not any(p.is_symlink() for p in root.rglob('*')))
    return dict(files=files,directories=dirs,root_identity=identity(root))

def replace(s,old,new,label,hunks):
    check('unique_complete_hunk:'+label,s.count(old)==1)
    hunks.append(dict(label=label,old_utf8=old,new_utf8=new))
    return s.replace(old,new,1)

def reverse(s,hunks,label):
    for i,h in enumerate(reversed(hunks)):
        check('unique_inverse:'+label+':'+str(i),s.count(h['new_utf8'])==1)
        s=s.replace(h['new_utf8'],h['old_utf8'],1)
    return s

def defs(s):
    return {n.name:n for n in ast.parse(s).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}

def segment(s,n):
    return ''.join(s.splitlines(keepends=True)[n.lineno-1:n.end_lineno])

def main():
    check('own_Source_stdlib_only',len(sys.argv)==1 and sys.dont_write_bytecode and not sys.flags.optimize)
    mp=pin(PARENT/'MANIFEST.json');m=json.loads((PARENT/'MANIFEST.json').read_bytes())
    check('fixed125_file_parent_manifest',mp['sha256']=='6745562c8153cbabe088324c6b9c932354b7f55c349aab3bc0fe75615913b847' and m['member_count']==124)
    before=inventory(PARENT)
    check('parent_complete124_member_EOFSHA7ID',before['files']=={**{Path(x['path']).relative_to(PARENT).as_posix():x for x in m['members']},'MANIFEST.json':mp})
    check('parent_dirs_and_root',before['directories']==m['directories'] and before['root_identity']==m['package_root_identity'])
    original_root=ROOT/'ORIGINAL_SEALED_V23_COMPLETE_MOTHER_SOURCE'
    shutil.copytree(PARENT,original_root)
    for rel in before['files']:
        check('all125_original_parent_files_retained:'+rel,(original_root/rel).read_bytes()==(PARENT/rel).read_bytes())
    proofs={}
    old=(PARENT/MODULE).read_text();new=old;hunks=[]
    new=replace(new,"    objects = [(key, type(value).__module__ + '.' + type(value).__qualname__, id(value))\n", "    objects = [(key, type(value).__module__ + '.' + type(value).__qualname__, id(value), value)\n",'retain_original_key_typename_id_and_actual_object_reference',hunks)
    comparator='''def complete_audit_state_equal(left, right, exact_value, label):
    """All private state; original metadata plus exact same observed objects.

    State witnesses stay local and never enter JSON reports. Tuple metadata
    retains original key/type/id values; no PID/FD/inode is normalized.
    """
    fields = ['data', 'exact_Popen_object_map_identity',
              'exact_actual_Popen_object_references']
    require(type(left) is dict and type(right) is dict
            and list(left) == list(right) == fields,
            label + ': complete audit state type/fields/order')
    for field in fields[:2]:
        exact_value(left[field], right[field], label + '/' + field)
    lrefs = left[fields[2]]
    rrefs = right[fields[2]]
    require(type(lrefs) is list and type(rrefs) is list and len(lrefs) == len(rrefs),
            label + ': exact complete Popen reference list type/count/order')
    for index, (lrow, rrow) in enumerate(zip(lrefs, rrefs)):
        where = label + '/' + fields[2] + '/' + str(index)
        require(type(lrow) is tuple and type(rrow) is tuple
                and len(lrow) == len(rrow) == 4,
                where + ': complete original metadata tuple and actual object')
        exact_value(list(lrow[:3]), list(rrow[:3]), where + '/original_key_type_id')
        require(type(lrow[3]) is type(rrow[3]) and lrow[3] is rrow[3],
                where + ': exact actual observed object type and identity')

'''
    anchor='def complete_snapshot_equal(left, right, exact_value, label):\n'
    new=replace(new,anchor,comparator+anchor,'add_full_private_audit_state_comparator_without_changing_public_comparator',hunks)
    tree=ast.parse(old)
    state_calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='exact_value' and len(n.args)>=2 and isinstance(n.args[1],ast.Call) and isinstance(n.args[1].func,ast.Name) and n.args[1].func.id=='audit_state_pin']
    check('actual_module_seven_state_calls_one_public_call',len(state_calls)==7 and len([n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='exact_value'])==8)
    for n in sorted(state_calls,key=lambda n:n.lineno):
        call=ast.get_source_segment(old,n)
        replacement='complete_audit_state_equal('+call[len('exact_value('):-1]+', exact_value)' # rewritten below preserves the original label argument
        replacement=ast.unparse(ast.Call(func=ast.Name(id='complete_audit_state_equal',ctx=ast.Load()),args=[n.args[0],n.args[1],ast.Name(id='exact_value',ctx=ast.Load()),n.args[2]],keywords=[]))
        new=replace(new,call,replacement,'state_comparison_call_line_'+str(n.lineno),hunks)
    (ROOT/MODULE).write_text(new)
    restore=reverse(new,hunks,MODULE)
    check('complete_module_bytes_AST_inverse',restore==old and ast.dump(ast.parse(restore),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False))
    od,nd=defs(old),defs(new)
    check('module_only_one_new_function',list(nd)==list(od)[:4]+['complete_audit_state_equal']+list(od)[4:])
    for name in od:
        if name not in ('audit_state_pin','small_private_snapshot_controls'):
            check('all_other_module_definitions_byte_AST_unchanged:'+name,segment(old,od[name])==segment(new,nd[name]) and ast.dump(od[name],include_attributes=False)==ast.dump(nd[name],include_attributes=False))
    check('public_nine_fields_comparison_function_byteexact',segment(old,od['complete_snapshot_equal'])==segment(new,nd['complete_snapshot_equal']))
    check('retain_original_control_names_counts',all(segment(old,n)==segment(new,next(x for x in ast.parse(new).body if isinstance(x,ast.Assign) and ast.unparse(x.targets[0])==ast.unparse(n.targets[0]))) for n in ast.parse(old).body if isinstance(n,ast.Assign)))
    proofs[MODULE]=dict(original_pin=pin(PARENT/MODULE),new_pin=pin(ROOT/MODULE),full_hunks=hunks,complete_bytes_AST_inverse_to_original=True,changed_original_functions=['audit_state_pin','small_private_snapshot_controls'],new_function='complete_audit_state_equal',state_comparison_calls_replaced=7,public_snapshot_comparison_unchanged=True)
    modulepin=pin(ROOT/MODULE)
    for fn in ROLES:
        old=(PARENT/fn).read_text();new=old;hunks=[]
        for global_name,oldvalue,newvalue in [('AUDIT_CONTROL_SHA256',repr('ba82f5e386fb99af2a43d63a4e4a696a4e296f461cc1c2926b0a7531560038b5'),repr(modulepin['sha256'])),('AUDIT_CONTROL_SOURCE_BYTES','22336',str(modulepin['size_bytes']))]:
            new=replace(new,global_name+' = '+oldvalue+'\n',global_name+' = '+newvalue+'\n',fn+'/'+global_name,hunks)
        tokens=[]
        for line in old.splitlines(keepends=True):
            if 'v23' in line or 'V23' in line:
                tokens.append(line)
        for line in tokens:
            new=replace(new,line,line.replace('v23','v24').replace('V23','V24'),fn+'/fresh_family_literal_'+str(len(hunks)),hunks)
        (ROOT/fn).write_text(new)
        restored=reverse(new,hunks,fn)
        check('controller_full_bytes_AST_inverse:'+fn,restored==old and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False))
        od,nd=defs(old),defs(new)
        check('all_controller_definition_names_order:'+fn,list(od)==list(nd))
        for name in od:
            osrc=segment(old,od[name]);nsrc=segment(new,nd[name])
            check('all_controller_algorithm_definitions_unchanged_except_schema_literals:'+fn+'/'+name,nsrc.replace('V24','V23').replace('v24','v23')==osrc and ast.dump(ast.parse(nsrc.replace('V24','V23').replace('v24','v23')),include_attributes=False)==ast.dump(ast.parse(osrc),include_attributes=False))
        proofs[fn]=dict(original_pin=pin(PARENT/fn),new_pin=pin(ROOT/fn),full_hunks=hunks,complete_bytes_AST_inverse_to_original=True,complete_original_definition_names=list(od),algorithm_definitions_unchanged_except_explicit_family_schema_literals=True)
    fn='bind_complete_qualification_SOURCE_only.py'
    old=(PARENT/fn).read_text();new=old;hunks=[]
    for suffix in ('ACTUAL_PRIVATE_INACTIVE_AUDIT_QUALIFICATION_SOURCE_BINDING_INVERSES_V1','ACTUAL_SOURCE_ONLY_FULL_QUALIFICATION_BOUND_NAMESPACE_V1'):
        new=replace(new,'ROOT_V23_'+suffix,'ROOT_V24_'+suffix,fn+'/'+suffix,hunks)
    (ROOT/fn).write_text(new)
    check('Sourcebinder_full_bytes_AST_inverse',reverse(new,hunks,fn)==old)
    check('Sourcebinder_actual_V23_install_schema_facts_not_renamed',"ROOT_V23_ACTUAL_COMPLETE_HELPER_SOURCE_INSTALL_TOOL_RETURN_V1" in new and "ROOT_V23_COMPLETE_HELPER_SOURCE_INSTALL_RECORD_V1" in new and "ROOT_V24_ACTUAL_COMPLETE_HELPER_SOURCE_INSTALL_TOOL_RETURN_V1" not in new)
    proofs[fn]=dict(original_pin=pin(PARENT/fn),new_pin=pin(ROOT/fn),full_hunks=hunks,complete_bytes_AST_inverse_to_original=True,original_actual_Source_install_record_and_witness_schema_unchanged=True)
    plan=json.loads((PARENT/'ROOT_FIXED_SOURCE_NAMESPACES_AND_FUTURE_ACTUAL_PINS.UNREADY.json').read_bytes())
    for kind in ('pure','fresh'):
        plan['namespaces'][kind]={k:v.replace('v23','v24') for k,v in plan['namespaces'][kind].items()}
    plan['module_Source_pin']=modulepin
    plan['new_complete_helper_candidate_pin']=pin(Path(plan['namespaces']['planned_installed_helper']))
    actualwitness=E/'Root_actual_complete_helper_SOURCE_install_tool_return.json';actualrecord=E/'Root_actual_complete_helper_SOURCE_install_record.json'
    plan['existing_actual_unchanged_V23_Source_install_witness_pin']=pin(actualwitness)
    plan['existing_actual_unchanged_V23_Source_install_record_pin']=pin(actualrecord)
    plan['Source_install_reused_fact_not_a_new_tool_run']=True
    plan['new_Source_install_witness']=None;plan['new_Source_install_record']=None
    write('ROOT_FIXED_SOURCE_NAMESPACES_AND_FUTURE_ACTUAL_PINS.UNREADY.json',plan)
    failures=ROOT/'ACTUAL_CLOSED_FAILED_V23_SOURCE_AND_META_CONTEXT';failures.mkdir()
    failed_paths=[E/'Root_actual_complete_qualification_tool_terminal_return.json',E/'Root_actual_complete_qualification_postclose_summary.json',E/'Root_actual_complete_qualification_postclose_namespace_manifest.json',E/'Root_actual_complete_qualification_prelaunch_frozen_D_E.json',E/'Root_final_complete_qualification_SOURCE_freeze.json',E/'Root_actual_complete_qualification_outer_merged_stdout_stderr.log',H/'run/admit.log',H/'run/admit.watchdog.json',H/'failed_host_result.json',D/MODULE,D/'pure_helper_controls.py',D/'pure_helper_controls_host.py']
    failurepins=[]
    for path in failed_paths:
        ref=pin(path);name=('H__' if path.is_relative_to(H) else 'D__' if path.is_relative_to(D) else 'E__')+path.relative_to(H if path.is_relative_to(H) else D if path.is_relative_to(D) else E).as_posix().replace('/','__')
        shutil.copy2(path,failures/name);check('failed_full_Source_META_byteexact:'+name,(failures/name).read_bytes()==path.read_bytes())
        failurepins.append(dict(original_pin=ref,copied_pin=pin(failures/name)))
    terminal=json.loads((E/'Root_actual_complete_qualification_tool_terminal_return.json').read_bytes())
    tr=terminal['terminal_tool_return']
    check('real_failed_V23_int1_CLOSED_no_repoll',terminal['closed'] is True and terminal['actual_tool_terminal_return_observed'] is True and type(tr['exit_code']) is int and tr['exit_code']==1 and tr['chunk_id']=='437ca4' and ('session_id' not in tr or tr['session_id'] is None))
    log=(H/'run/admit.log').read_text()
    check('exact_actual_failed_tuple_comparator_context',"exact_actual_Popen_object_references/0" in log and "JSON scalar differs" in log and "line 192" in log)
    failed_summary=json.loads((E/'Root_actual_complete_qualification_postclose_summary.json').read_bytes())
    check('no_saved_failedqualification_credit',failed_summary['actual_complete_control_success'] is False and failed_summary['new_actual_helper_qualification'] is None)
    write('ACTUAL_FAILED_V23_COMPLETE_SOURCE_META_CONTEXT_PINS.json',dict(source_only=True,actual_failed_terminal=pin(E/'Root_actual_complete_qualification_tool_terminal_return.json'),failure_scope='JSON-only comparator rejected the refs[0] metadata tuple; not a Popen instance passed to JSON scalar comparator',full_context_pins=failurepins,old_complete_HODE_frozen_in_project_not_duplicated_as_new_Source_scope=True,new_actual_qualification=None))
    # The fullgraph phase has zero subprocess records. Its two private state
    # witnesses remain local; no Popen object is emitted in any report/gzip.
    fs=(ROOT/ROLES[2]).read_text()
    check('fresh_whole_private_state_before_after_original_kept',"require(audit_controls.audit_state_pin(audit,include_records=False)==other_audit_state_before,'whole audit subprocess/identity state must remain unchanged')" in fs)
    check('fresh_fullphase_has_no_subprocess_records',"trace['subprocess_records']==[]" in fs or "trace['subprocess_records'] == []" in fs)
    check('private_refs_never_in_small_actual_report',"exact_actual_Popen_object_references" not in segment(new if False else (ROOT/MODULE).read_text(),defs((ROOT/MODULE).read_text())['validate_small_control_report']))
    # Preserve the original peer field contract; independent PASS does not exist.
    peer=json.loads((PARENT/'INDEPENDENT_SOURCE_PEER_REQUIRED_CONTRACT.UNREADY.json').read_bytes())
    peer['qualified_template_manifest_pin']=None
    peer['qualified_template_Source_pins']={name:pin(ROOT/name) for name in ROLES+(MODULE,)}
    peer['qualified_helper_candidate_SHA']='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'
    peer['new_actual_helper_qualification']=None
    peer['six_future_business_pins']=[None]*6
    write('INDEPENDENT_SOURCE_PEER_REQUIRED_CONTRACT.UNREADY.json',peer)
    write('V24_COMPLETE_MODULE_CONTROLLER_BINDER_SOURCE_INVERSE.json',dict(schema='COMPLETE_V24_PRIVATE_POPEN_IDENTITY_SOURCE_FINITE_INVERSE_V1',source_only=True,full_parent_manifest_pin=mp,all_complete_Source_finite_inverse=proofs,public_nine_fields_order_type_floatbits_algorithms_unchanged=True,private_state_seven_module_call_sites_replaced=True,actual_original_V23_install_schema_and_tool_facts_retained=True,new_actual_qualification=None,six_future_business_pins=[None]*6))
    after=inventory(PARENT);check('whole_original125_Source_members_dirs_root_unchanged',after==before)
    for path,ref in list(allread.items()):check('all_Source_and_failed_META_final_EOFpin_unchanged:'+path,pin(Path(path))==ref)
    write('FULL_ORIGINAL_SOURCE_AND_META_PINS_BEFORE_AFTER.json',dict(parent_before=before,parent_after=after,all_read_fullpins=allread))
    roles={name:pin(ROOT/name) for name in ROLES+(MODULE,)}
    binderpin=pin(ROOT/'bind_complete_qualification_SOURCE_only.py')
    inversepin=pin(ROOT/'V24_COMPLETE_MODULE_CONTROLLER_BINDER_SOURCE_INVERSE.json')
    review=dict(schema='COMPLETE_V24_POPEN_IDENTITY_QUALIFICATION_SOURCE_SELF_REVIEW_V1',status='SOURCE_ONLY_PASS_NO_EXECUTION_OR_QUALIFICATION',source_only=True,all_checks_typed_true=True,blockers=[],check_count=len(checks),checks=checks,complete_original_parent_manifest_pin=mp,complete_original_parent_files=125,qualified_template_Source_pins=roles,source_binding_generator_pin=binderpin,complete_Source_inverse_pin=inversepin,unchanged_helper_Source_sha256='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092',private_state_comparison_changes=7,public_snapshot_comparator_unchanged=True,all_original_5positive_13reject_3failure_controls_preserved=True,new_actual_helper_qualification=None,six_future_business_pins=[None]*6,helper_controller_guard_API_or_binding_executed=False,any_numeric_or_material_decode=False,any_RSS_build_INPUT_or_science_pass_prediction=None)
    write('SOURCE_SELF_REVIEW.json',review)
    print(json.dumps(dict(status=review['status'],source_only=True,check_count=review['check_count'],module_pin=modulepin,role_pins=roles,review_pin=pin(ROOT/'SOURCE_SELF_REVIEW.json'),output=str(ROOT)),separators=(',',':')))

if __name__=='__main__':
    main()
