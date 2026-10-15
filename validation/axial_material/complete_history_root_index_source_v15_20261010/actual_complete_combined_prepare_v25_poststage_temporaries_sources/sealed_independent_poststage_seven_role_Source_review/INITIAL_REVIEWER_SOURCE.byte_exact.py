"""Independent full finite Source / already saved small META review only.
No import or execution of candidates, binders, project APIs, guards or numerical work.
No graph, trace, gzip, material, DB, binary or archive payload is read.
"""
import argparse
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import stat

P=Path('/private/tmp/axmat_V25_poststage_temporaries_complete_UNREADY_Source_v2ept7ev')
SIB=Path(str(P)+'_seal_receipt')
EXPECTED_MF='9085afa282c04c927118323d101c9d23ffce51ebcdd2f2ddda7e4b8d0500d6bd'
EXPECTED_ROLES={'canonical':'241e5a6fa40922e13da7fa1579cd190971d1757f5515e00c27770ad5e07fa79f','prepare_host':'2e4a19c3290c48026ce3efde6a421f308ca33d85c6643895ec3a13b2ad40b1cb','prepare_writer':'2b090b206d2aa153c7fb0a83cbbd43833c03f7a67b368a6114f6039a7d1a5c90','build_host':'8c0e64137c26b41943fd9b833c4e313023813419141f0d3d6a7b4d0215b5280e','build_writer':'db7767aafbbb69ad3a3713bc28db0f109ad4c9f8459299420cbdbbd8002662ca','prepare_binder':'1ac47d61e92fd02d2f1033485557c13a0b9dbc73a92c8e1bfa125c79dc82c7d3','build_binder':'7422f24840921396694b2983756ad7c71a67b62a8e99e394d8afc7c5cd7811f7'}
BUSINESS=('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA')
NEW_BASENAME='prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_poststage_temporaries.py'
NS_TRANSFORMS={'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_monitor_access.py':NEW_BASENAME,'v25-monitor-access-20261010':'v25-poststage-temporaries-20261010','v25_monitor_access_sources':'v25_poststage_temporaries_sources','v25_monitor_access_receipts':'v25_poststage_temporaries_receipts'}
FALSE=('whole_build_qualified','whole_combined_INPUT_admitted','native_RSS_qualified','native_transport_executed','physical_balance_qualified','AAA_accuracy_qualified','ABA_admitted','goal_complete')
checks=[];blockers=[];pins={};AST_sources={};definition_counts={};name_refs={}

def check(name,value):
    value=value is True;checks.append(dict(check=name,passed=value))
    if not value:blockers.append(name)

def identity(p):
    s=Path(p).lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def ordinary(p):
    p=Path(p)
    if not p.is_absolute()or'..'in p.parts:raise ValueError('absolute ordinary Source/META')
    for a in(p,*p.parents):
        i=identity(a)
        if stat.S_ISLNK(i[2])or(a!=p and not stat.S_ISDIR(i[2])):raise ValueError('no Source aliases')
    return p

def pin(p):
    p=ordinary(p);before=identity(p)
    if not stat.S_ISREG(before[2])or before[4]>4*2**20:raise ValueError('finite regular Source/small META only')
    if p.suffix in('.gz','.a','.o','.sqlite','.db')or p.name in('input_graph.json','input_creation_python_open_trace.json','Dragon'):raise ValueError('payload excluded')
    with p.open('rb')as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
    if identity(p)!=before:raise ValueError('full EOF Source/META changed')
    q=dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before);pins[str(p)]=q;return q

def read(p):
    before=pin(p)
    def pairs(items):
        answer={}
        for k,v in items:
            if k in answer:raise ValueError('duplicate META key')
            answer[k]=v
        return answer
    def finite(value):raise ValueError('nonfinite JSON')
    q=json.loads(Path(p).read_bytes(),object_pairs_hook=pairs,parse_constant=finite)
    if pin(p)!=before:raise ValueError('META changed while parsing')
    return q

def dump(n):return ast.dump(n,include_attributes=False)

def defs(text):
    tree=ast.parse(text);lines=text.splitlines(keepends=True);result={}
    for n in tree.body:
        if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
            start=min([n.lineno,*[q.lineno for q in n.decorator_list]])
            if n.name in result:raise ValueError('duplicate Source definition')
            result[n.name]=( ''.join(lines[start-1:n.end_lineno]),dump(n))
    return result

def assignments(tree):
    return{n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}

def verify_actual_closed(name,record,chunk):
    t=record['terminal_tool_return']
    check(name+'.actual_closed',record['closed']is True and record['observed_terminal']is True and record['session_repolled_after_close']is False)
    check(name+'.strict_int0',type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and t['chunk_id']==chunk==record['actual_terminal_chunk'])
    check(name+'.scope_Source_only',record['source_only']is True and record['candidate_helper_guard_API_compile_numeric_executed']is False and record['new_business_or_science_qualified']is False)
    return json.loads(t['output'])

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output)
    if not str(out).startswith('/private/tmp/')or os.path.lexists(out):raise ValueError('fresh private TMP review output')
    mf=read(P/'MANIFEST.json');mfpin=pin(P/'MANIFEST.json')
    check('exact_actual_author_manifest_SHA',mfpin['sha256']==EXPECTED_MF and mfpin['size_bytes']==19158)
    check('author_manifest_explicit_Source_only',mf['source_only']is True and mf['author_not_independent_peer']is True and mf['candidate_helper_guard_API_compile_numeric_executed']is False and mf['new_business_or_science_qualified']is False)
    current_files={str(p.relative_to(P))for p in P.rglob('*')if p.is_file()};current_dirs={'.'}|{str(p.relative_to(P))for p in P.rglob('*')if p.is_dir()}
    check('complete_exact38_file_set',current_files==set(mf['members'])|{'MANIFEST.json'}and len(current_files)==38 and mf['member_count']==len(mf['members'])==37)
    check('complete_exact5_directory_set',current_dirs==set(mf['directories'])and len(current_dirs)==5)
    for rel,i in mf['directories'].items():check('complete_author_directory7ID.'+rel,identity(P if rel=='.'else P/rel)==i)
    for rel,q in mf['members'].items():
        check('complete_author_member_EOF_SHA7ID.'+rel,pin(P/rel)==q)
        if Path(rel).suffix=='.py':AST_sources[rel]=ast.parse((P/rel).read_bytes(),filename=str(P/rel))
    check('complete_author_total_bytes',sum(q['size_bytes']for q in mf['members'].values())+mfpin['size_bytes']==3091611)
    report=read(P/'AUTHOR_SOURCE_ONLY_REPORT.json');inverse=read(P/'COMPLETE_SOURCE_INVERSES.json');contract=read(P/'FUTURE_ROOT_BINDING_AND_NAMESPACE_CONTRACT.UNREADY.json');ledger=read(P/'ALL_ORIGINAL_READ_SOURCE_AND_SMALL_META_PINS.json')
    check('author_report_exact_full_SHA',pin(P/'AUTHOR_SOURCE_ONLY_REPORT.json')['sha256']=='24ed53a90cbde4d3616a87d0fb87de5e7482b9de002475f9ac59e9db1cd75e15')
    check('inverse_exact_full_SHA',pin(P/'COMPLETE_SOURCE_INVERSES.json')['sha256']=='f22930a541575af96cded23ded09f01e1efe74b6646586270d9f5a010b87beff')
    check('author_report_not_independent',report['source_only']is True and report['author_not_independent_peer']is True and report['status']=='AUTHOR_SOURCE_ONLY_COMPLETE_UNREADY_NO_EXECUTION'and report['new_helper_Q_or_software_business_or_science_qualification']is False and report['candidate_helper_guard_API_compile_native_material_numeric_executed']is False and report['new_Source_install_executed']is False)
    check('author_report66_unique_exactbool_checks',type(report['check_count'])is int and report['check_count']==len(report['checks'])==66 and len({q['check']for q in report['checks']})==66 and all(type(q['passed'])is bool and q['passed']is True for q in report['checks'])and report['all_checks_typed_true']is True and report['blockers']==[])
    check('inverse_whole_original_Source_scope',inverse['source_only']is True and inverse['all_original_full_Source_preserved']is True and inverse['all_physical_body_or_caps_changed']is False and inverse['new_business_pins_unknown']is True and inverse['known_current_helper_Q_SHA']=='c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b')
    check('all_original19_Source_META_ledger',ledger['source_only']is True and ledger['all_read_inputs_unchanged']is True and len(ledger['full_read_input_pins'])==19)
    for number,q in enumerate(ledger['full_read_input_pins']):check('original_input_EOF_SHA7ID.'+str(number),pin(q['path'])==q)
    originals={};candidates={}
    check('seven_complete_roles',set(inverse['role_filenames'])==set(EXPECTED_ROLES)==set(inverse['parent_Source_pins'])==set(report['qualified_role_Source_pins']))
    for role,rel in inverse['role_filenames'].items():
        original=(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text();candidate=(P/rel).read_text();restored=candidate
        origpin=pin(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py'));parentpin=pin(inverse['parent_Source_pins'][role]['path'])
        check(role+'.parent_actual_full_pin',parentpin==inverse['parent_Source_pins'][role])
        check(role+'.complete_parent_copy_full_bytes',origpin['sha256']==parentpin['sha256']and origpin['size_bytes']==parentpin['size_bytes'])
        check(role+'.qualified_actual_candidate_pin',pin(P/rel)==report['qualified_role_Source_pins'][role]and pin(P/rel)['sha256']==EXPECTED_ROLES[role])
        for index,row in enumerate(reversed(inverse['exact_finite_transforms'][role])):
            label=row['label'];old=row['old'];new=row['new'];count=row['count']
            check(role+'.inverse_transform_count.'+str(index),type(count)is int and count>0 and restored.count(new)==count)
            check(role+'.finite_allowed_transform.'+str(index),label.startswith(('fresh_namespace_','unknown_'))or label in('three_private_last_use_temporaries_only','truthful_UNREADY_doc','truthful_READY_binding_doc_only','new_installed_canonical_output_basename'))
            if label.startswith('fresh_namespace_'):check(role+'.exact_new_namespace_pair.'+str(index),NS_TRANSFORMS.get(old)==new)
            if label.startswith('unknown_'):
                old_ast=ast.parse(old).body;new_ast=ast.parse(new).body
                check(role+'.unknown_only_same_global_assignment.'+str(index),len(old_ast)==len(new_ast)==1 and isinstance(old_ast[0],ast.Assign)and isinstance(new_ast[0],ast.Assign)and dump(old_ast[0].targets[0])==dump(new_ast[0].targets[0]))
                name=new_ast[0].targets[0].id
                check(role+'.only_future_or_ready_global.'+str(index),name.startswith('FUTURE_')or name in('DRAFT_STATUS','SOURCE_BINDING_STATUS'))
                check(role+'.future_None_or_UNREADY_literal.'+str(index),isinstance(new_ast[0].value,ast.Constant)and(new_ast[0].value.value is None if name.startswith('FUTURE_')else'UNREADY'in new_ast[0].value.value))
            restored=restored.replace(new,old)
        check(role+'.complete_full_byte_inverse',restored==original)
        check(role+'.complete_full_AST_inverse',dump(ast.parse(restored))==dump(ast.parse(original)))
        od=defs(original);cd=defs(restored)
        check(role+'.complete_original_definition_set',list(od)==list(cd))
        for name in od:
            check(role+'.complete_definition_byte_AST_inverse.'+name,od[name]==cd[name])
        definition_counts[role]=len(od);originals[role]=original;candidates[role]=candidate
        check(role+'.no_old_target_namespace',all(old not in candidate for old in NS_TRANSFORMS))
        check(role+'.original_imports_AST_unchanged',[dump(n)for n in ast.parse(original).body if isinstance(n,(ast.Import,ast.ImportFrom))]==[dump(n)for n in ast.parse(candidate).body if isinstance(n,(ast.Import,ast.ImportFrom))])
    check('actual_parent_canonical_complete214132B',pin(inverse['parent_Source_pins']['canonical']['path'])['sha256']=='643d1b5fcfada4c7ec13f8c5d4c01fb6a77529f51a109d73fac214952f849ef2'and pin(P/'ORIGINAL_PARENT_SOURCE/canonical.full.py')['size_bytes']==214132)
    canonical_tree=ast.parse(candidates['canonical']);canonical_assign=assignments(canonical_tree);original_tree=ast.parse(originals['canonical'])
    check('all_six_future_business_SHA_None',all(isinstance(canonical_assign[k],ast.Constant)and canonical_assign[k].value is None for k in BUSINESS))
    check('canonical_actual_Q_and_external_proofs_unbound',all(isinstance(canonical_assign[k],ast.Constant)and canonical_assign[k].value is None for k in('FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA','FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN')))
    check('canonical_status_UNREADY',ast.literal_eval(canonical_assign['DRAFT_STATUS'])=='UNREADY_V25_COMPLETE_INACTIVE_AUDIT_ACTUAL_Q_UNBOUND')
    run=next(n for n in canonical_tree.body if isinstance(n,ast.FunctionDef)and n.name=='run_build');old_run=next(n for n in original_tree.body if isinstance(n,ast.FunctionDef)and n.name=='run_build')
    outer_try=next(n for n in run.body if isinstance(n,ast.Try));old_try=next(n for n in old_run.body if isinstance(n,ast.Try))
    check('run_build_exactly_two_added_statements',len(outer_try.body)==len(old_try.body)+2)
    delete,collect=outer_try.body[-2:];update=outer_try.body[-3]
    check('private_release_exact_three_names',dump(delete)==dump(ast.parse('del stages,audit,commands').body[0]))
    check('gc_collect_empty_args_exact',dump(collect)==dump(ast.parse('gc.collect()').body[0]))
    check('lastuse_release_after_complete_preserved_result_update',dump(update)==dump(old_try.body[-1])and isinstance(update,ast.Expr)and isinstance(update.value,ast.Call)and isinstance(update.value.func,ast.Attribute)and update.value.func.attr=='update'and update.value.func.value.id=='result')
    stripped=copy.deepcopy(run);stripped_try=next(n for n in stripped.body if isinstance(n,ast.Try));stripped_try.body=stripped_try.body[:-2]
    check('run_build_all_other_full_AST_body_exact',dump(stripped)==dump(old_run))
    for name in ('stages','audit','commands'):
        refs=sorted([dict(line=n.lineno,context=type(n.ctx).__name__)for n in ast.walk(run)if isinstance(n,ast.Name)and n.id==name],key=lambda q:q['line']);name_refs[name]=refs
        check('lastuse_no_future_read_or_write.'+name,all(q['line']<=delete.lineno for q in refs))
        check('lastuse_owned_local_assigned_before_delete.'+name,any(q['context']=='Store'and q['line']<delete.lineno for q in refs))
    check('lastuse_no_run_build_dynamic_local_introspection',not any(isinstance(n,ast.Name)and n.id in('locals','vars','eval','exec','_getframe','currentframe')for n in ast.walk(run)))
    check('retained_result_is_not_deleted',all(isinstance(n,ast.Name)and n.id not in('result','runner','d','resources')for n in delete.targets))
    check('all_five_stage_and_audit_guards_precede_release',all(x in ast.get_source_segment(candidates['canonical'],run)for x in("len(stages)!=5","any(s['status']!='PASS' for s in stages)","audit['classification']!='PASS_COMBINED_RUNTIME_LINK_IDENTITY_ONLY'","watchdogs=[check_watch(s) for s in stages]")))
    check('result_retains_all_watchdogs_and_runtime_identity',[kw.arg for kw in update.value.keywords]==['classification','watchdogs','corrected_runtime','fresh_cold_AAA_required'])
    check('canonical77_complete_definitions',definition_counts['canonical']==report['canonical_top_definition_count']==77)
    check('helper_source_and_Q_13_field_protocol_retained',"3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092"in candidates['canonical']and"'full_protocol_fields'"in candidates['prepare_binder']and'[13,27,37112,55,42]'in candidates['prepare_binder'])
    for role in ('prepare_host','prepare_writer','build_host','build_writer'):
        a=assignments(ast.parse(candidates[role]));future={k:v for k,v in a.items()if k.startswith('FUTURE_V25_')}
        check(role+'.future_actual_SHA_all_None',bool(future)and all(isinstance(v,ast.Constant)and v.value is None and k+'=None'in candidates[role]for k,v in future.items()))
        check(role+'.binding_status_UNREADY',isinstance(a['SOURCE_BINDING_STATUS'],ast.Constant)and'UNREADY'in a['SOURCE_BINDING_STATUS'].value)
        main=next(n for n in ast.parse(candidates[role]).body if isinstance(n,ast.FunctionDef)and n.name=='main')
        first=main.body[0]
        check(role+'.first_main_guard_UNREADY_before_io',isinstance(first,ast.If)and any(isinstance(n,ast.Name)and n.id=='SOURCE_BINDING_STATUS'for n in ast.walk(first.test))and any(isinstance(n,ast.Raise)for n in ast.walk(first)))
    prep=candidates['prepare_binder'];build=candidates['build_binder']
    check('PREP_binder_exact_new_canonical_basename',"'canonical':'"+NEW_BASENAME+"'"in prep)
    check('PREP_binder_actual_Q_not_omitted','deps=helper_Q_admission()'in prep and all(option in prep for option in('--actual-new-Q-writer-terminal','--actual-Q-saved-peer','--actual-Q-saved-peer-retention')))
    check('BUILD_binder_new_PREP_receipts_only',"E=BASE/'actual_complete_combined_prepare_v25_poststage_temporaries_receipts'"in build and '--saved-prep-peer-report'in build and 'actual_PREP_closed_EXIT0_verified'in build and 'helper_Q_admission()'in build)
    check('both_Source_binders_full_manifest_inverse_required',all(all(token in text for token in('source_package()','source_verify_original_inverse','complete SOURCE member full pin'))for text in(prep,build)))
    check('new_business_results_unknown_contract',contract['status']=='UNREADY_ALL_NEW_BUSINESS_RESULTS_UNKNOWN'and all(v is None for v in contract['new_PREP_BUILD_result_pins'].values())and all(v is None for v in contract['new_actual_Source_binding_install_freeze_and_independent_peers'].values()))
    check('new_contract_original_caps',contract['original_caps']==dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_HSOTDE_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0))
    for key,q in contract['original_install_interface_Source_pins'].items():
        check('original_install_interface_real_pin.'+key,pin(q['path'])==q)
        cp=pin(P/'ORIGINAL_ROOT_INSTALL_INTERFACES'/(key+'.full.py'))
        check('original_install_interface_complete_copy.'+key,cp['sha256']==q['sha256']and cp['size_bytes']==q['size_bytes'])
    next_text=(P/'ROOT_NEXT_STEPS.txt').read_text()
    check('new_install_interfaces_not_falsely_READY','Existing interface Sources are originals, not ready new installers.'in next_text and 'prepares finite new installer/prelaunch/complete-E-snapshot Source'in next_text)
    check('RSS_not_predicted','No memory success is predicted.'in next_text and 'RSS reduction is not predicted.'in candidates['canonical'])
    failure=read(P/'ACTUAL_PRIOR_FAILED_BUILD_META/FULL_ORIGINAL_FAILURE_SCOPE_AND_FIELD_DIFFERENCE.json');old_summary=read(P/'ACTUAL_PRIOR_FAILED_BUILD_META/Root_actual_failed_complete_combined_build_summary.json');old_watch=read(P/'ACTUAL_PRIOR_FAILED_BUILD_META/build.watchdog.json');old_stages=read(P/'ACTUAL_PRIOR_FAILED_BUILD_META/original_inner_five_stages.json')['stages']
    check('complete_old_failure_scope_same_author_report',failure==report['prior_failure_scope'])
    for name,q in failure['actual_failure_pins'].items():
        check('old_failed_actual_original_meta_pin.'+name,pin(q['path'])==q)
        cp=pin(P/'ACTUAL_PRIOR_FAILED_BUILD_META'/name)
        check('old_failed_complete_byte_copy.'+name,cp['sha256']==q['sha256']and cp['size_bytes']==q['size_bytes'])
    check('old_5_inner_PASS_precise_scope',[q['label']for q in old_stages]==['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']and all(q['status']=='PASS'for q in old_stages)and old_stages[-1]['elapsed_seconds']==48.33631362498272 and failure['actual_five_inner_stages_all_PASS']is True)
    check('old_outer_RSS512_578_exit1_scope',old_watch['sampled_peak_rss_mib']==failure['actual_whole_peak_rss_mib']==512.578125 and old_watch['rss_cap_mib']==512 and old_watch['returncode']==-15 and old_watch['elapsed_seconds']==failure['actual_whole_seconds']==316.0239865001058 and old_summary['actual_terminal_exit_code']==1 and failure['actual_whole_EXIT1']is True)
    check('old_summary_formal_failure_not_false_deny_innerPASS',old_summary['all_five_build_stages_passed']is False and old_summary['original_five_build_stages_executed']is False and old_summary['observed_PASS_inner_stage_labels']==[q['label']for q in old_stages]and failure['formal_flags_not_used_to_deny_observed_inner_PASS']is True)
    check('no_precise_peak_line_or_new_success_inferred',failure['precise_peak_line_not_observed']is True and failure['driver_result_and_seal_not_generated']is True and failure['new_PREP_or_BUILD_success']is False and failure['new_source_release_does_not_predict_RSS']is True)
    seal_record=read(SIB/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json');post_record=read(SIB/'ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json')
    check('actual_author_seal_receipt_SHA',pin(SIB/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json')['sha256']=='c7a3d25be21b3d56fcc56e10ab23e0a19f165ebbbc99bd63a963348a99b7af2c')
    check('actual_author_postseal_receipt_SHA',pin(SIB/'ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json')['sha256']=='9c32afd693d32164e504500dcf7c44e7bb0e2a159a3076698b0d571a2abb215b')
    sealed=verify_actual_closed('genuine_author_seal',seal_record,'538ff2');post=verify_actual_closed('genuine_author_postseal',post_record,'fd5c4a')
    check('actual_author_seal_output_fullpins',sealed['manifest']==mfpin and sealed['report']==pin(P/'AUTHOR_SOURCE_ONLY_REPORT.json')and sealed['inverse']==pin(P/'COMPLETE_SOURCE_INVERSES.json')and sealed['roles']==report['qualified_role_Source_pins']and sealed['all_original_Source_and_small_META_unchanged']is True)
    check('actual_author_postseal_output_fullpins',post['manifest']==mfpin and post['author_report']==pin(P/'AUTHOR_SOURCE_ONLY_REPORT.json')and post['all_complete_Source_members_dirs_full_EOF_SHA7ID_unchanged']is True and post['all_original_Source_and_small_META_fullpins_unchanged']is True)
    pv=read(SIB/'FULL_SOURCE_POSTSEAL_VERIFICATION.json')
    check('actual_postseal_saved_report_SHA',pin(SIB/'FULL_SOURCE_POSTSEAL_VERIFICATION.json')['sha256']=='8a624adbf12f6e742e48c0c830a07dd8e7fedabdcd52ff2988db4d381991ca1e')
    check('actual_postseal_saved_report_exact',pv==post)
    author_tools=read(P/'ACTUAL_AUTHOR_SOURCE_ONLY_TOOL_RETURNS.json')
    check('author_tools_not_independent_credit',author_tools['author_not_independent_peer']is True and author_tools['source_only']is True and author_tools['candidate_helper_guard_API_compile_numeric_executed']is False)
    for name,t in author_tools['actual_tools'].items():check('genuine_author_Source_tool_terminal.'+name,type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and type(t['chunk_id'])is str and bool(t['chunk_id']))
    for q in list(pins.values()):check('final_full_Source_META_7ID_stable.'+q['path'],identity(q['path'])==q['identity'])
    for rel,i in mf['directories'].items():check('final_sealed_directory7ID_stable.'+rel,identity(P if rel=='.'else P/rel)==i)
    value=dict(schema='INDEPENDENT_V25_POSTSTAGE_TEMPORARIES_COMPLETE_SOURCE_REVIEW_V1',
        status='PASS_COMPLETE_POSTSTAGE_TEMPORARIES_SOURCE_ONLY_UNREADY_NO_EXECUTION'if not blockers else'BLOCKED_COMPLETE_POSTSTAGE_TEMPORARIES_SOURCE_REVIEW',
        source_only=True,all_checks_typed_true=not blockers,check_count=len(checks),checks=checks,blockers=blockers,
        qualified_complete_Source_manifest_pin=mfpin,qualified_role_Source_pins=report['qualified_role_Source_pins'],actual_original_canonical_Source_pin=inverse['parent_Source_pins']['canonical'],
        actual_author_Source_report_pin=pin(P/'AUTHOR_SOURCE_ONLY_REPORT.json'),actual_complete_Source_inverse_pin=pin(P/'COMPLETE_SOURCE_INVERSES.json'),
        actual_author_seal_receipt_pin=pin(SIB/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json'),actual_author_postseal_receipt_pin=pin(SIB/'ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json'),
        independent_full_EOF_Source_small_META_pins=list(pins.values()),actual_complete_author_files=38,actual_complete_author_directories_including_root=5,actual_complete_author_full_bytes=3091611,actual_full_Source_AST_parse_count=len(AST_sources),whole_role_definition_counts=definition_counts,
        actual_private_lastuse_name_references=name_refs,private_release_exactly_three_owned_JSON_command_locals_after_all_checks=True,all_original_result_records_fields_caps_and_physical_Source_preserved=True,
        original_current_Q_has_no_new_qualification=True,new_Q_proofs_must_be_truly_reread_by_actual_Root_Source_binders=True,
        existing_install_interfaces_are_original_references_only=True,new_complete_installer_prelaunch_snapshot_Source_still_required=True,
        new_PREP_or_BUILD_result=None,new_install_or_bound_Source_result=None,actual_new_RSS_result=None,no_RSS_or_allocator_reclamation_prediction=True,
        no_candidate_binder_helper_guard_API_compile_native_material_numeric_execution=True,no_project_old_namespace_or_author_package_mutation=True,
        no_graph_trace_gzip_material_DB_binary_archive_payload_read=True,cleanup_performed=False,**{k:False for k in FALSE})
    out.mkdir();(out/'REVIEW.json').write_text(json.dumps(value,indent=2,allow_nan=False)+'\n');(out/'REVIEWER_SOURCE.byte_exact.py').write_bytes(Path(__file__).read_bytes())
    print(json.dumps(dict(status=value['status'],source_only=True,all_checks_typed_true=value['all_checks_typed_true'],check_count=len(checks),blockers=blockers,review_pin=pin(out/'REVIEW.json'),qualified_complete_Source_manifest_pin=mfpin,whole_build_INPUT_native_science_qualified=False),allow_nan=False))

if __name__=='__main__':main()
