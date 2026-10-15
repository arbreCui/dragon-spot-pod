import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
import traceback

B = Path('/private/tmp/spot_Root_actual_V25_single_pre_graph_gc_PREP_bound_Source_20261011')
A = Path('/private/tmp/axmat_single_pre_graph_gc_complete_UNREADY_Source_82j4vp0_')
T = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/Root_actual_single_pre_graph_gc_complete_PREP_Source_binding_tool_terminal_return_20261011.json')
EXPECTED_MF = '50a350dcc3ab24f1a4ccd992b714079342f90d19deacdeb8a6f146d8663dab55'
EXPECTED_TERMINAL = 'f8ef1a30de92230f2c50e9b9ebd4e4b6ba1840a0f7c584417f247abd608ca56d'
EXPECTED_AUTHOR = '8ddab63da54f05828a93728b50a7c2cff680973409022725e64e5b083cbdf854'
RESOURCE = '/Users/wen/miniforge3/envs/openmc-dev/lib/python3.12/lib-dynload/resource.cpython-312-darwin.so'
RESOURCE_SHA = 'cbd0358d5dfb6a5271a7e645118a36d0537b49e84452a2bcd7d26a73eb131164'
ROLES = dict(canonical='prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_memory_observation_capture_pre_graph_gc.py', prepare_host='combined_prepare_host.py', prepare_writer='write_actual_prepare_terminal.py')
CAPS = dict(whole_wall_seconds=1800, stage_wall_seconds=600, rss_mib=512, joint_archive_bytes=2**31, history_bytes=96*2**30, free_floor_bytes=8*2**30, threads=1, children_at_once=1, retries=0)
CHECKS, BLOCKERS, READS = [], [], {}
OUT = Path(tempfile.mkdtemp(prefix='axmat_actual_single_pre_graph_gc_PREP_bound_Source_INDEPENDENT_', dir='/private/tmp'))

def identity(s): return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def strict(raw):
    def pairs(items):
        d={}
        for k,v in items:
            if k in d: raise ValueError('duplicate JSON key: '+k)
            d[k]=v
        return d
    def reject(v): raise ValueError('nonfinite JSON: '+v)
    return json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=reject)

def read(p, allow_resource=False):
    p=Path(p);s=p.lstat();i=identity(s)
    allowed_nlink = 2 if allow_resource and str(p)==RESOURCE else 1
    if not stat.S_ISREG(s.st_mode) or s.st_nlink != allowed_nlink or not 0<=s.st_size<=8*2**20:
        raise ValueError('bounded regular Source/META required: '+str(p))
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,'rb',buffering=0) as f:
        if identity(os.fstat(f.fileno()))!=i:raise ValueError('opened descriptor mismatch')
        raw=f.read(s.st_size+1)
        if len(raw)!=s.st_size or f.read(1)!=b'' or identity(os.fstat(f.fileno()))!=i:raise ValueError('full EOF stability failed')
    if identity(p.lstat())!=i:raise ValueError('path changed during full EOF')
    pin=dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=i)
    if allowed_nlink==2 and pin['sha256']!=RESOURCE_SHA:raise ValueError('sole exact resource module exception differs')
    if str(p)in READS and READS[str(p)]!=pin:raise ValueError('Source/META changed on repeated read')
    READS[str(p)]=pin
    return raw,pin

def exact(pin):
    if type(pin)is not dict or set(pin)!={'path','sha256','size_bytes','identity'} or type(pin['size_bytes'])is not int or type(pin['identity'])is not list or len(pin['identity'])!=7 or any(type(n)is not int for n in pin['identity']):raise ValueError('strict fourpin required')
    raw,actual=read(pin['path'],allow_resource=(pin['path']==RESOURCE))
    if pin!=actual:raise ValueError('fullpin differs: '+pin['path'])
    return raw

def check(name, passed, evidence=None):
    if type(passed)is not bool or name in {c['check']for c in CHECKS}:raise ValueError('unique typed bool required')
    c=dict(check=name,passed=passed)
    if evidence is not None:c['evidence']=evidence
    CHECKS.append(c)
    if not passed:BLOCKERS.append(name)

def dump(x):return (json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
def write(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True);fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'wb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
    return read(p)[1]

def reverse(text,rows):
    replay=[]
    for r in reversed(rows):
        if type(r['count'])is not int or r['count']<1:raise ValueError('strict transform count')
        n=text.count(r['new']);replay.append(dict(label=r['label'],expected=r['count'],observed=n))
        if n!=r['count']:raise ValueError('inverse occurrence mismatch: '+r['label'])
        text=text.replace(r['new'],r['old'])
    return text,replay

def ast_equal(a,b):return ast.dump(ast.parse(a),include_attributes=False)==ast.dump(ast.parse(b),include_attributes=False)
def definitions(text):return [(type(n).__name__,n.name,ast.get_source_segment(text,n),ast.dump(n,include_attributes=False))for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
def assignments(text):return {n.targets[0].id:n.value for n in ast.parse(text).body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
def literals(text):
    d={}
    for k,v in assignments(text).items():
        try:d[k]=ast.literal_eval(v)
        except (ValueError,TypeError):pass
    return d

def run():
    mr,mp=read(B/'MANIFEST.json');mf=strict(mr)
    check('bound_manifest_expected_full_EOF_SHA',mp['sha256']==EXPECTED_MF and mp['size_bytes']==3865,mp)
    check('bound_source_only_not_project_executed',mf['source_only']is True and mf['executed_project']is False)
    files={str(p.relative_to(B)):p for p in B.rglob('*')if stat.S_ISREG(p.lstat().st_mode)}
    dirs={str(p.relative_to(B)):identity(p.lstat())for p in [B,*B.rglob('*')]if stat.S_ISDIR(p.lstat().st_mode)}
    check('bound_complete_enumeration_8files_1dir',set(files)==set(mf['members'])|{'MANIFEST.json'} and len(files)==8 and len(dirs)==1 and type(mf['member_count'])is int and mf['member_count']==7)
    check('bound_all_directory7IDs_exact',dirs==mf['directories'])
    data,pins={},{}
    for rel,pin in mf['members'].items():
        raw,actual=read(B/rel);check('bound_complete_full_EOF_SHA_7ID:'+rel,actual==pin,actual);data[rel],pins[rel]=raw,actual
        if rel.endswith('.py'):ast.parse(raw,filename=rel)
    ar,ap=read(A/'MANIFEST.json');author=strict(ar)
    check('current_gc_complete_author_manifest_expected',ap['sha256']==EXPECTED_AUTHOR,ap)
    check('current_gc_author_complete_members_dirs_match',set(str(p.relative_to(A))for p in A.rglob('*')if stat.S_ISREG(p.lstat().st_mode))==set(author['members'])|{'MANIFEST.json'} and {str(p.relative_to(A)):identity(p.lstat())for p in [A,*A.rglob('*')]if stat.S_ISDIR(p.lstat().st_mode)}==author['directories'])
    traw,tp=read(T);term=strict(traw);t=term['terminal_tool_return']
    check('actual_Root_binding_terminal_expected_full_EOF_SHA',tp['sha256']==EXPECTED_TERMINAL and tp['size_bytes']==7584,tp)
    check('actual_Root_binding_genuine_closed_strictint0',term['record_producer']=='root'and term['source_only']is True and term['closed']is True and term['observed_terminal']is True and term['observed_after_actual_terminal_return']is True and term['session_repolled_after_close']is False and type(t['exit_code'])is int and t['exit_code']==0 and t['chunk_id']=='2728ba'and 'session_id'not in t and term['initial_tool_return']==t)
    check('actual_Root_binding_scope_no_install_or_business_credit',all(term[k]is False for k in ['candidate_or_business_executed','installed','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','goal_complete']))
    observed=strict(t['output'].encode());roles={k:pins[v]for k,v in ROLES.items()}
    check('actual_Root_stdout_bound_current_role_and_manifest_fullpins',observed['manifest']==mp and observed['canonical']==roles['canonical']and observed['host']==roles['prepare_host']and observed['writer']==roles['prepare_writer']and observed['source_only']is True and observed['business_or_science_executed']is False)
    inv=strict(data['Root_actual_Q_bound_complete_PREP_Source_inverse.json']);proof=strict(exact(author['members']['COMPLETE_SOURCE_INVERSES.json']))
    check('actual_inverse_source_only_no_runtime_or_install',inv['source_only']is True and inv['candidate_guard_API_compiler_or_numeric_executed']is False and inv['installed']is False)
    check('actual_inverse_exact_three_roles',set(inv['complete_original_source_inverses'])==set(ROLES))
    replay={}
    for role,rel in ROLES.items():
        current=data[rel].decode();template_raw=exact(author['members'][proof['role_current_paths'][role]]);template=template_raw.decode();spec=inv['complete_original_source_inverses'][role]
        normalized,counts=reverse(current,spec['READY_to_UNREADY'])
        check('bound_complete_byte_inverse_to_current_gc_template:'+role,normalized.encode()==template_raw)
        check('bound_complete_AST_inverse_to_current_gc_template:'+role,ast_equal(normalized,template))
        check('bound_functions_classes_occurrence_order_wholebytes_unchanged:'+role,definitions(current)==definitions(template))
        check('bound_original_consumed_inverse_rows_exact_current_proof:'+role,spec['UNREADY_to_original']==proof['exact_finite_transforms'][role])
        original,ocounts=reverse(normalized,spec['UNREADY_to_original']);op=proof['original_parent_fullpins'][role];original_raw=exact(op)
        check('bound_complete_byte_inverse_to_original_parent:'+role,original.encode()==original_raw)
        check('bound_complete_AST_inverse_to_original_parent:'+role,ast_equal(original,original_raw.decode()))
        replay[role]=dict(actual_bound_Source_pin=roles[role],template_Source_pin=author['members'][proof['role_current_paths'][role]],original_parent_Source_pin=op,READY_to_UNREADY_counts=counts,UNREADY_to_original_counts=ocounts,whole_bytes_and_AST_verified=True)
    canonical=data[ROLES['canonical']].decode();values=literals(canonical)
    business=[k for k in values if k.startswith('FUTURE_ACTUAL_')and k in inv['all_six_future_business_pins']]
    check('all_six_future_business_fields_still_unknown',len(business)==6 and set(business)==set(inv['all_six_future_business_pins'])and all(values[k]is None and inv['all_six_future_business_pins'][k]is None for k in business))
    check('bound_READY_changes_exact_allowed_labels_and_counts',[r['label']for r in inv['complete_original_source_inverses']['canonical']['READY_to_UNREADY']]==['actual_Q_READY_truthful_doc','actual_Q_READY_status','actual_Q_SHA','actual_external_new_Q_fullpin_FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN','actual_external_new_Q_fullpin_FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN','actual_external_new_Q_fullpin_FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN','actual_diagnostic_dependency_fullpin']and [r['label']for r in inv['complete_original_source_inverses']['prepare_host']['READY_to_UNREADY']]==['actual_FUTURE_V25_ACTUAL_Q_SHA','actual_FUTURE_V25_CANONICAL_SHA','actual_Q_and_canonical_bound']and [r['label']for r in inv['complete_original_source_inverses']['prepare_writer']['READY_to_UNREADY']]==['actual_FUTURE_V25_CANONICAL_SHA','actual_Q_and_canonical_bound']and all(type(r['count'])is int and r['count']==1 for s in inv['complete_original_source_inverses'].values()for r in s['READY_to_UNREADY']))
    qraw=exact(inv['actual_Q']);q=strict(qraw)
    check('actual_Q_bytes_original_pin_and_bound_copy_exact',inv['actual_Q']==observed['actual_Q']and qraw==data['ACTUAL_V25_HELPER_ONLY_JOINT_Q.byte_exact.json']and inv['actual_Q']['sha256']=='c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b')
    check('existing_Q_metadata_only_scope_not_requalified',q['schema']=='AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_INACTIVE_AUDIT_HELPER_ACTUAL_JOINT_ADMISSION_V25'and q['scope']=='HELPER_METADATA_ORIGINAL_COMPLETE_PROTOCOL_AND_SAME_CURRENT_GRAPH_VERIFIER_ONLY_NO_WHOLE_INPUT_BUILD_NATIVE_OR_SCIENCE'and all(q[k]is False for k in ['fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','whole_build_qualified','whole_INPUT_admitted','physical_balance_qualified','supervisor_class_or_MRO_modified']))
    check('actual_bound_Q_global_exact_existing_Q_sha',values['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA']==inv['actual_Q']['sha256'])
    helper_raw=exact(q['helper']);check('actual_helper_Source_full_EOF_same3b_no_execution',q['helper']['sha256']=='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092',q['helper']);ast.parse(helper_raw)
    read_pins=inv['all_read_Source_META_fullpins'];check('actual_binder_complete_147_Source_META_read_domain',type(read_pins)is list and len(read_pins)==147 and len({p['path']for p in read_pins})==147)
    for pin in read_pins:
        exact(pin);check('actual_binder_dependency_full_EOF_SHA_same7ID:'+pin['path'],READS[pin['path']]==pin,pin)
    check('all_original_340_explicit_Q_typed_owner_hashes_retained',type(inv['all_Q_and_proof_explicit_typed_owner_expected_files'])is dict and len(inv['all_Q_and_proof_explicit_typed_owner_expected_files'])==340 and all(type(p)is str and type(h)is str and len(h)==64 for p,h in inv['all_Q_and_proof_explicit_typed_owner_expected_files'].items()))
    for name in ['FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN']:
        exact(values[name]);check('actual_external_Q_Source_META_global_pin_current:'+name,READS[values[name]['path']]==values[name])
    envpin=values['FUTURE_ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS_PIN'];envraw=exact(envpin);env=strict(envraw)
    check('actual_environment_bound_copy_and_stdout_fullpin_match',envraw==data['ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS.byte_exact.json']and envpin==observed['actual_diagnostic_resource_environment_witness']and envpin['sha256']=='945b3d52207b4d3dde2c672c017dd643a51e0d586375193faf0ec91b53184aa1')
    etraw=exact(env['actual_environment_tool_terminal_fullpin']);et=strict(etraw);etr=et['terminal_tool_return'];eo=strict(etr['output'].encode())
    check('actual_environment_original_terminal_and_copy_closed0',etraw==data['ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS_TOOL_TERMINAL.byte_exact.json']and et['closed']is True and et['observed_terminal']is True and et['session_repolled_after_close']is False and type(etr['exit_code'])is int and etr['exit_code']==0 and etr['chunk_id']=='5ae744'and 'session_id'not in etr)
    check('actual_environment_original_stdout_payload_coupled',all(env[k]==v for k,v in eo.items()if k!='schema')and eo['schema']=='ROOT_ACTUAL_DARWIN_RESOURCE_SELF_RUSAGE_DIAGNOSTIC_ENVIRONMENT_QUERY_V1')
    for name in ['actual_python_fullpin','actual_resource_module_fullpin','actual_environment_producer_Source_fullpin','environment_witness_META_writer_Source_fullpin']:
        exact(env[name]);check('actual_environment_dependency_full_EOF_SHA7ID:'+name,READS[env[name]['path']]==env[name],env[name])
    check('environment_scope_historical_self_peak_not_current_guard_RSS',env['platform']=='darwin'and env['diagnostic_dependency_verified']is True and type(env['query_count'])is int and env['query_count']==1 and type(env['actual_python_optimization'])is int and env['actual_python_optimization']==0 and all(v=='1'for v in env['actual_thread_environment'].values())and env['ru_maxrss_semantics']=='DARWIN_RUSAGE_SELF_NATIVE_BYTES_PROCESS_HISTORICAL_HIGH_WATER_NOT_CURRENT_RSS_OR_GUARD_PEAK'and all(env[k]is False for k in ['whole_BUILD_qualified','whole_INPUT_qualified','native_or_science_qualified','candidate_guard_helper_compile_material_or_numeric_executed']))
    check('sole_pinned_resource_positive_hardlink_exception_exact',env['actual_resource_module_fullpin']['path']==RESOURCE and env['actual_resource_module_fullpin']['sha256']==RESOURCE_SHA and env['actual_resource_module_fullpin']['identity'][3]==2 and all(p['identity'][3]==1 for p in read_pins if p['path']!=RESOURCE))
    hostvalues=literals(data[ROLES['prepare_host']].decode());writervalues=literals(data[ROLES['prepare_writer']].decode())
    check('host_and_writer_bound_canonical_Q_source_pins_exact',hostvalues['FUTURE_V25_ACTUAL_Q_SHA']==inv['actual_Q']['sha256']and hostvalues['FUTURE_V25_CANONICAL_SHA']==roles['canonical']['sha256']and writervalues['FUTURE_V25_CANONICAL_SHA']==roles['canonical']['sha256'])
    phase=next(n for n in ast.parse(canonical).body if isinstance(n,ast.FunctionDef)and n.name=='complete_input_phase');ptext=ast.get_source_segment(canonical,phase)
    idx=[i for i,n in enumerate(phase.body)if isinstance(n,ast.Delete)and [ast.unparse(t)for t in n.targets]==['specs','original_aliases']]
    check('bound_gc_last_use_and_both_full_graph_algorithms_same_template',len(idx)==1 and ast.unparse(phase.body[idx[0]+1])=='gc.collect()'and isinstance(phase.body[idx[0]+3],ast.With)and ptext.count("g.verify_graph(d['input_graph']['path']")==1 and ptext.count("g.strict_json(d['input_graph']['path']")==1)
    fixed=strict(exact(author['members']['utilities/FIXED_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT.UNREADY.json']))
    check('all_ten_business_namespaces_fresh_not_installed',len(fixed['namespaces'])==10 and all(not os.path.lexists(v)for v in fixed['namespaces'].values()))
    author_report=strict(exact(author['actual_author_report_pin']));check('original_nine_caps_strictly_retained_by_whole_Source_binding_inverses',author_report['original_caps']==CAPS and all(type(v)is int for v in author_report['original_caps'].values())and all(x['whole_bytes_and_AST_verified']is True for x in replay.values()))
    for rel,pin in pins.items():check('final_bound_full_EOF_SHA7ID:'+rel,read(B/rel)[1]==pin)
    check('final_bound_manifest_directory_and_Root_terminal_unchanged',read(B/'MANIFEST.json')[1]==mp and {str(p.relative_to(B)):identity(p.lstat())for p in [B,*B.rglob('*')]if stat.S_ISDIR(p.lstat().st_mode)}==dirs and read(T)[1]==tp)
    evidence=dict(schema='INDEPENDENT_ACTUAL_SINGLE_PRE_GRAPH_GC_PREP_BOUND_SOURCE_REPLAY_EVIDENCE_V1',source_only=True,actual_complete_bound_Source_manifest_pin=mp,current_gc_template_manifest_pin=ap,actual_Root_Source_binding_tool_terminal_pin=tp,roles=replay,all_complete_current_Source_META_and_dependency_full_EOF_pins=READS.copy(),actual_Q_owner340_only_current_Source_expected_ownership_not_new_runtime_proof=True,old_Q_not_requalified=True,actual_API_or_business_executed=False)
    ep=write(OUT/'REPLAY_EVIDENCE.json',dump(evidence))
    report=dict(schema='INDEPENDENT_ACTUAL_V25_MEMORY_OBSERVATION_COMPLETE_PREP_BOUND_SOURCE_REVIEW_V1',status='PASS_ACTUAL_Q_BOUND_COMPLETE_PREP_MEMORY_OBSERVATION_SOURCE_ONLY_NOT_INSTALLED_OR_EXECUTED'if not BLOCKERS else 'FAIL_ACTUAL_Q_BOUND_COMPLETE_PREP_MEMORY_OBSERVATION_SOURCE_ONLY_NOT_INSTALLED_OR_EXECUTED',source_only=True,all_checks_typed_true=not BLOCKERS,check_count=len(CHECKS),checks=CHECKS,blockers=BLOCKERS,actual_complete_bound_Source_manifest_pin=mp,actual_ready_role_Source_pins=roles,actual_Root_Source_binding_tool_terminal_pin=tp,current_gc_complete_template_manifest_pin=ap,independent_replay_evidence_pin=ep,original_nine_caps=CAPS,scope='Actual three-role PREP Source binding only. Full EOF/SHA/7ID of bound8 and genuine Root terminal, all147 consumed Source/META dependencies, original environment producer/tool/Python/resource bytes; whole READY-to-current-template-to-OriginalParent byte/AST replay. Original Q metadata qualification is only an unchanged prerequisite and is not newly qualified.',source_only_current_binding_admitted=True,all_six_future_business_fields_None=True,whole_INPUT_PREP_BUILD_runtime_native_or_science_qualification=None,actual_RSS_qualified=False,AAA_ABA_or_goal_qualified=False,actual_candidate_binder_guard_helper_resource_API_PS_lsof_native_business_executed=False,project_or_old_frozen_D_E_or_results_modified=False)
    rp=write(OUT/'REVIEW.json',dump(report));write(OUT/'REVIEW_SOURCE.py',Path(__file__).read_bytes())
    for rel,path in [('EVIDENCE/actual_bound_manifest.byte_exact.json',B/'MANIFEST.json'),('EVIDENCE/actual_Root_binding_terminal.byte_exact.json',T),('EVIDENCE/current_gc_manifest.byte_exact.json',A/'MANIFEST.json')]:write(OUT/rel,read(path)[0])
    print(json.dumps(dict(package=str(OUT),review_pin=rp,replay_evidence_pin=ep,check_count=len(CHECKS),all_checks_typed_true=not BLOCKERS,blockers=BLOCKERS,source_only=True,actual_candidate_or_business_executed=False,no_runtime_RSS_or_science_credit=True),sort_keys=True))
    return not BLOCKERS

if __name__=='__main__':
    try:ok=run()
    except Exception as e:
        write(OUT/'ACTUAL_REVIEW_FAILURE.json',dump(dict(schema='ACTUAL_INDEPENDENT_BOUND_GC_PREP_SOURCE_REVIEW_FAILURE_V1',source_only=True,checks=CHECKS,blockers=BLOCKERS,error=repr(e),traceback=traceback.format_exc(),actual_candidate_or_business_executed=False)))
        write(OUT/'FAILED_REVIEW_SOURCE.py',Path(__file__).read_bytes());print(json.dumps(dict(package=str(OUT),source_only=True,Source_review_failed=True,error=repr(e))));raise
    if not ok:raise SystemExit(1)
