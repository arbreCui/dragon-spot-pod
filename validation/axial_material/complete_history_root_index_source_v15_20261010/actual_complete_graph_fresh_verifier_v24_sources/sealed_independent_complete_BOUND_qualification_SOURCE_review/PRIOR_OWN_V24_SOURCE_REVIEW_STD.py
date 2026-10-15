"""Read-only complete V23 bound SOURCE review. No project code is imported/run."""
from pathlib import Path
import ast
import hashlib
import json
import os
import shutil
import stat
import sys

P = Path('/private/tmp/axmat_inactive_audit_v24_actual_COMPLETE_BOUND_SOURCE_ROOT_20261010_10a0e4')
N = Path('/private/tmp/axmat_v24_complete_inactive_audit_Popen_identity_UNREADY_SOURCE_hsjpb0_6')
B = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
E = B/'actual_complete_graph_helper_controls_v23_receipts'
OUT = Path(__file__).resolve().parent
MANIFEST = 'ROOT_FULL_GENERATED_QUALIFICATION_SOURCE_MANIFEST.json'
MSHA = '345aad2f97bac81f1aea0b37b9f7f700b3d0a905716b9f79daf456d6abc57f29'
NSHA = 'd6c95ff130261e14875d5b6422d8a3f19c5e80dc8e20cb8bf8894247b8e42302'
HELPER_SHA = '3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'
MODULE = 'inactive_audit_snapshot_controls_SOURCE_ONLY.py'
ROLES = ('pure_helper_controls.py','pure_helper_controls_host.py','fresh_verifier_controls.py','fresh_verifier_host.py')
checks = []
read_pins = {}

def check(label, condition, evidence=None):
    passed = type(condition) is bool and condition is True
    checks.append(dict(check=label,passed=passed,evidence=evidence))
    if not passed:
        raise AssertionError(label)

def identity(path):
    s=Path(path).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(path):
    path=Path(path)
    before=identity(path)
    check('regular_one_link:'+str(path),stat.S_ISREG(before[2]) and before[3]==1)
    raw=path.read_bytes()
    after=identity(path)
    check('full_EOF_identity_stable:'+str(path),before==after and len(raw)==before[4])
    value=dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before)
    if str(path) in read_pins:
        check('repeat_actual_full_pin_stable:'+str(path),read_pins[str(path)]==value)
    else:
        read_pins[str(path)]=value
    return value

def pairs(values):
    d={}
    for k,v in values:
        if k in d: raise ValueError('duplicate META key')
        d[k]=v
    return d

def reject(value):
    raise ValueError('nonfinite META constant '+value)

def decode(raw):
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=reject)

def read(path,sha=None):
    a=pin(path)
    if sha is not None:check('fixed_SHA:'+str(path),a['sha256']==sha)
    value=decode(Path(path).read_bytes())
    check('META_full_pin_after_decode:'+str(path),pin(path)==a)
    return value,a

def checkpin(ref,label):
    check(label+':exact_full_pin_fields',type(ref) is dict and set(ref)=={'path','sha256','size_bytes','identity'})
    check(label+':exact_integer7ID',type(ref['identity']) is list and len(ref['identity'])==7 and all(type(x) is int for x in ref['identity']) and type(ref['size_bytes']) is int and ref['size_bytes']==ref['identity'][4])
    check(label+':full_actual_pin',pin(ref['path'])==ref)

def check3(ref,label):
    check(label+':three_pin_fields',type(ref) is dict and set(ref)=={'path','sha256','identity'})
    check(label+':strict_integer7ID',type(ref['identity']) is list and len(ref['identity'])==7 and all(type(x) is int for x in ref['identity']))
    value=pin(ref['path'])
    check(label+':complete_current_pin',ref=={k:value[k] for k in ref})
    return value

def inventory(root,excluded=()):
    root=Path(root)
    items=sorted(root.rglob('*'))
    check('no_aliases:'+str(root),not any(x.is_symlink() for x in items))
    files={x.relative_to(root).as_posix():pin(x) for x in items if x.is_file() and x.relative_to(root).as_posix() not in excluded}
    dirs={x.relative_to(root).as_posix():identity(x) for x in items if x.is_dir()}
    return dict(root=str(root),root_identity=identity(root),files=files,directories=dirs,symlinks=[])

def segment(s,n):
    return ''.join(s.splitlines(keepends=True)[n.lineno-1:n.end_lineno])

def globals_of(s):
    out={}
    for n in ast.parse(s).body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            try:out[n.targets[0].id]=ast.literal_eval(n.value)
            except (ValueError,TypeError):pass
    return out

def inverse(new,hunks,label):
    restored=new
    for i,h in enumerate(reversed(hunks)):
        check(label+':unique_inverse_span:'+str(i),restored.count(h['new_utf8'])==1)
        restored=restored.replace(h['new_utf8'],h['old_utf8'],1)
    return restored

def write(name,value):
    (OUT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')

def main():
    check('own_Source_stdlib_only_execution',sys.dont_write_bytecode and not sys.flags.optimize and len(sys.argv)==1)
    m,mp=read(P/MANIFEST,MSHA)
    bound_before=inventory(P)
    check('bound_manifest_schema_sourceonly',m['schema']=='ROOT_V24_ACTUAL_SOURCE_ONLY_FULL_QUALIFICATION_BOUND_NAMESPACE_V1' and m['source_only'] is True)
    check('bound_unknown_newQ_and_six_future_business_pins',m['new_actual_helper_qualification'] is None and m['six_future_business_pins']==[None]*6 and m['controller_helper_guard_API_or_business_executed'] is False)
    expected={Path(x['path']).relative_to(P).as_posix():x for x in m['members']}
    check('complete_bound_manifest_exact164_unique_members',type(m['member_count']) is int and m['member_count']==164 and len(expected)==len(m['members'])==164)
    check('bound_full164_files_matches_manifest_EOFSHA7ID',expected=={k:v for k,v in bound_before['files'].items() if k!=MANIFEST})
    check('bound_complete165_file_inventory',len(bound_before['files'])==165)
    for rel,ref in expected.items():
        check('bound_member_exact_integer_fullpin:'+rel,type(ref['identity']) is list and len(ref['identity'])==7 and all(type(x) is int for x in ref['identity']) and type(ref['size_bytes']) is int)
    n,np=read(N/'MANIFEST.json',NSHA)
    mother_before=inventory(N)
    nm={Path(x['path']).relative_to(N).as_posix():x for x in n['members']}
    check('complete_parent154_members',type(n['member_count']) is int and n['member_count']==154 and len(nm)==154)
    check('complete_parent_full_file_namespace',nm=={k:v for k,v in mother_before['files'].items() if k!='MANIFEST.json'})
    check('complete_parent_directory_identity',mother_before['directories']==n['directories'] and mother_before['root_identity']==n['package_root_identity'])
    copied=inventory(P/'COMPLETE_QUALIFICATION_TEMPLATE_SOURCE')
    check('whole_mother155_file_copy_names',set(copied['files'])==set(mother_before['files']))
    check('whole_mother_all_directories_preserved',set(copied['directories'])==set(mother_before['directories']))
    for rel,ref in mother_before['files'].items():
        check('whole_mother_full_byte_exact_copy:'+rel,(P/'COMPLETE_QUALIFICATION_TEMPLATE_SOURCE'/rel).read_bytes()==(N/rel).read_bytes() and copied['files'][rel]['sha256']==ref['sha256'])
    proof,pp=read(P/'ALL_FOUR_ACTUAL_SOURCE_BINDING_INVERSES.json','15339f4e66e92fcabb0d77a59e5b65bf2b4b66d46905405f55863a3f756b0a4b')
    check('actual_inverse_schema',proof['schema']=='ROOT_V24_ACTUAL_PRIVATE_INACTIVE_AUDIT_QUALIFICATION_SOURCE_BINDING_INVERSES_V1' and proof['source_only'] is True and proof['new_actual_helper_qualification'] is None and proof['six_future_business_pins']==[None]*6)
    for key in ('actual_installed_helper','actual_Root_install_witness','actual_Source_install_record','actual_independent_Source_peer','complete_template_manifest','complete_control_module_Source'):
        checkpin(proof[key],'proof_reference_'+key)
    witness,wp=read(E/'Root_actual_complete_helper_SOURCE_install_tool_return.json','a305a84b712276aecadd5ebc7fced99d0d58b68a061e228747f0ccfbeed63c12')
    check('install_wrapper_actual_Source_schema',witness['schema']=='ROOT_V23_ACTUAL_COMPLETE_HELPER_SOURCE_INSTALL_TOOL_RETURN_V1' and witness['source_only'] is True and witness['closed'] is True and witness['actual_tool_terminal_return_observed'] is True)
    tr=witness['terminal_tool_return']
    check('real_Source_install_integer_EXIT0_CLOSED',type(tr['exit_code']) is int and tr['exit_code']==0 and ('session_id' not in tr or tr['session_id'] is None) and tr['chunk_id']=='10a0e4')
    observed=decode(tr['output'])
    check('Source_install_stdout_exact_Python_integer7IDs',observed['installed_helper']==witness['installed_helper'] and observed['source_install_record']==witness['source_install_record'] and all(type(x) is int for x in observed['installed_helper']['identity']+observed['source_install_record']['identity']))
    hp=check3(witness['installed_helper'],'installed_helper')
    rp=check3(witness['source_install_record'],'installed_record')
    check('helper_exactreviewedSource',hp==proof['actual_installed_helper'] and hp['sha256']==HELPER_SHA and hp['size_bytes']==150986)
    helper_copy=P/'COMPLETE_QUALIFICATION_TEMPLATE_SOURCE/COMPLETE_SOURCE_REVIEWED_NEW_HELPER_CANDIDATE/combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume.UNREADY.py'
    check('installed_helper_all_bytes_identical_reviewed_candidate',Path(hp['path']).read_bytes()==helper_copy.read_bytes())
    record,_=read(rp['path'],rp['sha256'])
    check('actual_installrecord_schema_Sourceonly',record['schema']=='ROOT_V23_COMPLETE_HELPER_SOURCE_INSTALL_RECORD_V1' and record['source_only'] is True and record['installed_helper']==witness['installed_helper'] and record['business_or_guard_or_helper_API_executed'] is False)
    falsekeys=('actual_pure_helper_protocol_qualified','actual_full_current_graph_verifier_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted')
    check('install_not_qualification_or_science',all(witness[k] is False and record[k] is False for k in falsekeys) and witness['complete_build_qualified'] is False and record['actual_complete_build_qualified'] is False and witness['actual_new_helper_qualification_sha256'] is None and record['actual_new_helper_qualification_sha256'] is None)
    installed_snapshots={}
    for name,v in record['source_packages'].items():
        checkpin(v['copied_manifest'],'installed_package_manifest_'+name)
        root=Path(v['copied_manifest']['path']).parent
        snap=inventory(root)
        installed_snapshots[name]=snap
        want=dict(v['copied_members']);want['MANIFEST.json']=v['copied_manifest']
        check('installed_full_namespace:'+name,snap['files']==want and snap['directories']==v['copied_directories'] and snap['root_identity']==v['copied_root_identity'])
        original=v['original_source_package']
        for rel,ref in original['members'].items():
            check('installed_preserved_source_byte_SHA:'+name+':'+rel,snap['files'][rel]['sha256']==ref['sha256'] and snap['files'][rel]['size_bytes']==ref['size_bytes'])
    check('actual_Source_count223_plus_helper1',type(record['source_file_count']) is int and record['source_file_count']==observed['source_file_count']==223 and record['installed_helper_source_file_count']==1)
    protected=record['old_helper_Q_canonical_fullEOF_unchanged']
    check('three_originalprotectedpins',len(protected)==3 and {x['sha256'] for x in protected}=={'cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c','89d2f03c0af74844731ddf5225307c38ae40521d99ca29c88c5d8db39796b816','09e53974005082a14d9675f69258549609a991f86ec231ab6b15edfe20dd265e'})
    for i,ref in enumerate(protected):checkpin(ref,'old_protected_'+str(i))
    peer,peerp=read(proof['actual_independent_Source_peer']['path'],proof['actual_independent_Source_peer']['sha256'])
    check('actual_independent_template_Source_contract',peer['schema']=='INDEPENDENT_PRIVATE_INACTIVE_AUDIT_COMPLETE_QUALIFICATION_SOURCE_REVIEW_V1' and peer['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_QUALIFICATION' and peer['source_only'] is True and peer['all_checks_typed_true'] is True and peer['blockers']==[] and type(peer['check_count']) is int and peer['check_count']==len(peer['checks'])==2008 and all(type(x['passed']) is bool and x['passed'] is True for x in peer['checks']))
    check('peer_complete_manifest_five_Source_roles',peer['qualified_template_manifest_pin']==np and peer['qualified_helper_candidate_SHA']==HELPER_SHA and peer['qualified_template_Source_pins']=={name:pin(N/name) for name in ('pure_helper_controls.UNREADY.py','pure_helper_controls_host.UNREADY.py','fresh_verifier_controls.UNREADY.py','fresh_verifier_host.UNREADY.py',MODULE)})
    btool,btp=read('/private/tmp/spot_v24_actual_complete_qualification_SOURCE_binding_tool_return_ROOT.json','6856a6801897299be18fc8db92d120819e7c40714924a994792d71d7981ce51e')
    check('actual_Sourcebinder_receipt_observedClosed',btool['source_only'] is True and btool['closed'] is True and btool['actual_tool_terminal_return_observed'] is True and btool['actual_controller_or_helper_API_executed'] is False and btool['schema']=='ROOT_V24_ACTUAL_COMPLETE_QUALIFICATION_SOURCE_BINDING_TOOL_RETURN_V1')
    btr=btool['terminal_tool_return']
    check('actual_Sourcebinder_terminal_typed0_noSession',type(btr['exit_code']) is int and btr['exit_code']==0 and btr['chunk_id']=='0e2780' and ('session_id' not in btr or btr['session_id'] is None))
    bo=decode(btr['output'])
    check('actual_Sourcebinder_stdout_exact_complete_manifest_and_proof',bo['complete_bound_manifest']==mp and bo['bindings']==proof['all_four_full_Source_bindings'] and bo['output']==str(P) and bo['source_only'] is True and bo['new_actual_helper_qualification'] is None and bo['six_future_business_pins']==[None]*6)
    for name,ref in [('ORIGINAL_ROOT_ACTUAL_SOURCE_INSTALL_WITNESS.json',wp),('ORIGINAL_ROOT_ACTUAL_SOURCE_INSTALL_RECORD.json',rp),('ORIGINAL_INDEPENDENT_COMPLETE_SOURCE_REVIEW.json',peerp)]:
        check('complete_actual_META_copy_byteexact:'+name,(P/name).read_bytes()==Path(ref['path']).read_bytes())
    oldinv,_=read(N/'ORIGINAL_SEALED_V23_COMPLETE_MOTHER_SOURCE/ALL_FOUR_COMPLETE_QUALIFICATION_TEMPLATE_INVERSES.json')
    v24inv,_=read(N/'V24_COMPLETE_MODULE_CONTROLLER_BINDER_SOURCE_INVERSE.json')
    definitions={}
    source_texts={}
    all_globals={}
    allowed=[['SOURCE_STATUS','AUDIT_CONTROL_PATH','HELPER_PATH'],['SOURCE_STATUS','BOUND_HELPER_PIN','INSTALL_WITNESS_PIN','SOURCE_INSTALL_RECORD_PIN','AUDIT_CONTROL_PATH','TARGET_SHA'],['SOURCE_STATUS','AUDIT_CONTROL_PATH','NEW_HELPER_PATH','NEW_HELPER_IDENTITY'],['SOURCE_STATUS','BOUND_HELPER_PIN','INSTALL_WITNESS_PIN','SOURCE_INSTALL_RECORD_PIN','AUDIT_CONTROL_PATH','TARGET_SHA']]
    check('exact_allfour_inverse_members',set(proof['all_four_full_Source_bindings'])==set(ROLES))
    for i,name in enumerate(ROLES):
        item=proof['all_four_full_Source_bindings'][name]
        checkpin(item['template_pin'],'template_'+name);checkpin(item['bound_pin'],'bound_'+name)
        new=(P/name).read_text();old=Path(item['template_pin']['path']).read_text()
        source_texts[name]=new;all_globals[name]=globals_of(new)
        check('only_finite_expected_globals:'+name,[h['global_name'] for h in item['full_hunks']]==allowed[i])
        restored=inverse(new,item['full_hunks'],'bound_'+name)
        check('whole_Source_bytes_AST_inverse:'+name,restored==old and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False))
        a=[x for x in ast.parse(old).body if isinstance(x,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef))]
        z=[x for x in ast.parse(new).body if isinstance(x,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef))]
        check('all_definition_names_order:'+name,[x.name for x in a]==[x.name for x in z])
        definitions[name]=[x.name for x in z]
        for x,y in zip(a,z):
            check('complete_definition_bytes_AST_preserved:'+name+':'+x.name,segment(old,x)==segment(new,y) and ast.dump(x,include_attributes=False)==ast.dump(y,include_attributes=False))
        check('definition_proof_flags:'+name,item['all_definitions_bytes_AST_unchanged'] is True and item['full_template_bytes_AST_inverse'] is True)
        intermediate=v24inv['all_complete_Source_finite_inverse'][name.replace('.py','.UNREADY.py')]
        v23orig=inverse(old,intermediate['full_hunks'],'V24_to_V23_'+name)
        check('whole_V24_template_inverse_to_V23:'+name,v23orig.encode()==Path(intermediate['original_pin']['path']).read_bytes() and ast.dump(ast.parse(v23orig),include_attributes=False)==ast.dump(ast.parse(Path(intermediate['original_pin']['path']).read_bytes()),include_attributes=False))
        origin=oldinv['all_four_complete_source_inverse'][name]
        check('original_inverse_hunkcount:'+name,len(origin['full_hunks'])==[10,13,13,14][i])
        originalbytes=Path(origin['original_Source_pin']['path']).read_bytes()
        originrestored=inverse(v23orig,origin['full_hunks'],'original_'+name)
        check('complete_old_Q89_source_original_inverse:'+name,originrestored.encode()==originalbytes and ast.dump(ast.parse(originrestored),include_attributes=False)==ast.dump(ast.parse(originalbytes),include_attributes=False))
        check('ready_Source_only_unknown_qualification:'+name,all_globals[name]['SOURCE_STATUS']=='READY_SOURCE_BOUND_BY_ROOT')
    check('four_definition_exactcounts',[len(definitions[x]) for x in ROLES]==[25,2,16,9])
    module=(P/MODULE).read_bytes()
    check('shared_control_module_fullbytes_AST_same',module==(N/MODULE).read_bytes() and hashlib.sha256(module).hexdigest()=='d439eb9641f45e09c17814a38a16dc7e2cbb6120fc09119df901e415daf28483')
    module_parent=v24inv['all_complete_Source_finite_inverse'][MODULE]
    restored_module=inverse(module.decode(),module_parent['full_hunks'],'V24_complete_module')
    check('module_nine_full_hunk_inverse_to_original_tuple_witness',len(module_parent['full_hunks'])==9 and restored_module.encode()==Path(module_parent['original_pin']['path']).read_bytes() and ast.dump(ast.parse(restored_module),include_attributes=False)==ast.dump(ast.parse(Path(module_parent['original_pin']['path']).read_bytes()),include_attributes=False))
    mdefs={x.name:x for x in ast.parse(module).body if isinstance(x,ast.FunctionDef)}
    pdefs={x.name:x for x in ast.parse(restored_module).body if isinstance(x,ast.FunctionDef)}
    check('public_ninefield_snapshot_comparator_remains_wholebytes',segment(module.decode(),mdefs['complete_snapshot_equal'])==segment(restored_module,pdefs['complete_snapshot_equal']))
    cmp_source=segment(module.decode(),mdefs['complete_audit_state_equal'])
    check('private_state_full_fields_metadata_type_list_tuple_order_actual_is',all(text in cmp_source for text in ['list(left) == list(right) == fields','type(lrefs) is list','type(rrefs) is list','type(lrow) is tuple','type(rrow) is tuple','len(lrow) == len(rrow) == 4','exact_value(list(lrow[:3]), list(rrow[:3])','type(lrow[3]) is type(rrow[3]) and lrow[3] is rrow[3]']))
    fresh_v23=Path(v24inv['all_complete_Source_finite_inverse']['fresh_verifier_controls.UNREADY.py']['original_pin']['path']).read_text()
    current_fresh_defs={x.name:x for x in ast.parse(source_texts[ROLES[2]]).body if isinstance(x,ast.FunctionDef)}
    old_fresh_defs={x.name:x for x in ast.parse(fresh_v23).body if isinstance(x,ast.FunctionDef)}
    check('Fresh_run_wholebytes_original_and_exact_no_subprocess_scope',segment(source_texts[ROLES[2]],current_fresh_defs['run'])==segment(fresh_v23,old_fresh_defs['run']) and "trace['subprocess_records']==[]" in source_texts[ROLES[2]])
    mg=globals_of(module.decode())
    check('full_nine_snapshot_fields_order',mg['SNAPSHOT_FIELDS']==['schema','coverage','records','subprocess_records','unique_records','actual_read_open_attempts','record_storage','success_of_open_attempt_is_not_observed','native_libc_HDF5_loader_and_directory_stat_are_not_traced'])
    check('all_5_positive_13_reject_3_failure_controls',len(mg['POSITIVES'])==5 and len(mg['REJECTS'])==13 and len(mg['FAILURES'])==3)
    check('private_same_Popen_observation_no_crossrun_normalization',"Real Popen references are the same actual objects from one observation." in module.decode() and 'disjoint_owned_audit' in module.decode())
    check('no_actual_success_pins_in_drivers',all(all_globals[name]['ACTUAL_SUCCESS_PINS'] is None for name in (ROLES[0],ROLES[2])))
    for kind,driver,host in [('pure',ROLES[0],ROLES[1]),('fresh',ROLES[2],ROLES[3])]:
        dg,hg=all_globals[driver],all_globals[host]
        check('driver_hash_bound_to_wholehost:'+kind,hg['TARGET_SHA']==pin(P/driver)['sha256'])
        check('actual_helper_witness_record_exact_3pin:'+kind,hg['BOUND_HELPER_PIN']==witness['installed_helper'] and hg['INSTALL_WITNESS_PIN']=={k:wp[k] for k in ('path','sha256','identity')} and hg['SOURCE_INSTALL_RECORD_PIN']==witness['source_install_record'])
        check('shared_module_path_and_SHA:'+kind,dg['AUDIT_CONTROL_PATH']==hg['AUDIT_CONTROL_PATH'] and dg['AUDIT_CONTROL_SHA256']==hg['AUDIT_CONTROL_SHA256']==hashlib.sha256(module).hexdigest() and dg['AUDIT_CONTROL_SOURCE_BYTES']==hg['AUDIT_CONTROL_SOURCE_BYTES']==len(module))
        expectedcaps='WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP='+('60,60,512,64*2**20' if kind=='pure' else '1800,600,512,64*2**20')
        capnode=[x for x in ast.parse(source_texts[host]).body if isinstance(x,ast.Assign) and isinstance(x.targets[0],ast.Tuple) and [a.id for a in x.targets[0].elts]==['WHOLE_CAP','STAGE_CAP','RSS_CAP','ARCHIVE_CAP']]
        check('genuine_whole_stage_RSS_jointarchive_caps:'+kind,len(capnode)==1 and ast.dump(capnode[0],include_attributes=False)==ast.dump(ast.parse(expectedcaps).body[0],include_attributes=False))
        hs=source_texts[host]
        for token in ['OwnRSSSerialExecutor','__bases__','production.SerialExecutor','DynamicHistoryResources','8*2**30','96*2**30','support.THREAD_KEYS','children_at_once=1','retries=0','own_child_only','liveness_group_cleanup']:
            check('unchanged_genuine_scope:'+kind+':'+token,token in hs)
        roots_literal="str(support.SOURCE),str(support.OUT),str(support.TERMINAL)" if kind=='pure' else 'declared_history_roots=(HOST,OUT,support.SOURCE,support.OUT,support.TERMINAL)'
        check('history_roots_only_original_ART_descendants:'+kind,roots_literal in hs and 'resource.history_roots' in hs)
    fs=source_texts[ROLES[2]];fh=source_texts[ROLES[3]]
    for token in ('37111','37112','private_trace_controls','expected_return_from_old','lossless_json_gzip','full_consumed_snapshot_wire_compare'):
        check('full_current_graph_Source_contract:'+token,token in fs)
    check('three_original_lossless_gzips_contract',n['complete_fresh_original_lossless_gzip_files']==3)
    check('full_original_27_37111_37112_manifest_contract',n['complete_fresh_public_return_fields']==27 and n['complete_fresh_canonical_files']==37111 and n['complete_fresh_actual_read_records']==37112)
    check('full_fresh_27_return_and_9_trace_field_lists',len(all_globals[ROLES[3]]['RETURN_FIELDS'])==27 and all_globals[ROLES[3]]['TRACE_FIELDS']==mg['SNAPSHOT_FIELDS'])
    check('full_fresh_six_output_files_contract',"if set(p.name for p in OUT.iterdir())!={'ACTUAL_RUN_CLAIM.json','ACTUAL_REPORT.json','private_trace_fixture.txt','EXPECTED_COMPLETE_RETURN_CONTRACT.json.gz','ACTUAL_COMPLETE_VERIFIER_RETURN.json.gz','ACTUAL_COMPLETE_READ_OPEN_TRACE.json.gz'}" in fh)
    parsed=[]
    for rel in bound_before['files']:
        if rel.endswith('.py'):
            ast.parse((P/rel).read_bytes());parsed.append(rel)
            check('complete_bound_python_Source_AST_valid:'+rel,True)
    shutil.copytree(P,OUT/'COMPLETE_REVIEWED_BOUND_SOURCE')
    copied_review=inventory(OUT/'COMPLETE_REVIEWED_BOUND_SOURCE')
    check('complete_review_source_copy_all165_names',set(copied_review['files'])==set(bound_before['files']))
    for rel,ref in bound_before['files'].items():check('complete_review_copy_wholebytes:'+rel,(OUT/'COMPLETE_REVIEWED_BOUND_SOURCE'/rel).read_bytes()==(P/rel).read_bytes() and copied_review['files'][rel]['sha256']==ref['sha256'])
    shutil.copy2(E/'Root_actual_complete_helper_SOURCE_install_tool_return.json',OUT/'Root_actual_complete_helper_SOURCE_install_tool_return.json')
    shutil.copy2('/private/tmp/spot_v24_actual_complete_qualification_SOURCE_binding_tool_return_ROOT.json',OUT/'Root_actual_complete_qualification_SOURCE_binding_tool_return.json')
    bound_after=inventory(P)
    mother_after=inventory(N)
    check('complete_bound_all_files_dirs_root_before_after_exact',bound_after==bound_before)
    check('complete_parent_all_files_dirs_root_before_after_exact',mother_after==mother_before)
    for name,snap in installed_snapshots.items():check('complete_installed_Source_copy_before_after:'+name,inventory(snap['root'])==snap)
    for path,ref in list(read_pins.items()):check('all_read_Source_META_final_fullpin:'+path,pin(path)==ref)
    write('FULL_SOURCE_AND_META_PINS_BEFORE_AFTER.json',dict(bound_before=bound_before,bound_after=bound_after,parent_before=mother_before,parent_after=mother_after,installed_Source_packages=installed_snapshots,all_read_fullpins=read_pins))
    qualified_roles={name:pin(P/name) for name in ROLES+(MODULE,)}
    review=dict(schema='INDEPENDENT_V24_ACTUAL_COMPLETE_BOUND_PRIVATE_INACTIVE_AUDIT_QUALIFICATION_SOURCE_REVIEW_V1',status='SOURCE_ONLY_PASS_NO_EXECUTION_OR_QUALIFICATION',source_only=True,all_checks_typed_true=True,blockers=[],check_count=len(checks),checks=checks,bound_manifest_pin=mp,actual_binding_inverse_pin=pp,actual_Root_binding_tool_receipt_pin=btp,actual_Root_Source_install_witness_pin=wp,actual_installed_helper_pin=hp,complete_parent_manifest_pin=np,qualified_bound_Source_pins=qualified_roles,complete_bound_member_count=m['member_count'],complete_bound_files_including_manifest=len(bound_before['files']),complete_bound_directory_count=len(bound_before['directories']),complete_parent_members=n['member_count'],original_Source_definition_names=definitions,parsed_python_files=parsed,new_actual_helper_qualification=None,six_future_business_pins=[None]*6,helper_guard_or_controller_API_executed=False,any_numeric_or_material_decode_or_replay=False,any_RSS_build_INPUT_native_or_science_qualification=False,scope_notes=['All 164 bound members plus manifest were read to full EOF and SHA7ID checked; complete before/after directory identity is independently captured because the Root bound manifest declares all file members.','Four controllers only have exact 3/6/4/6 global bindings; all definitions retain complete byte/AST equivalence. Complete V24-to-V23 inverses, original 10/13/13/14 Q89 inverses and all155 V24 mother-package files retain the complete125-file V23 parent. Original tuple failure is preserved; actual observed objects are compared by exact type/is without normalizing key/type/id metadata.','One Popen observation is the shared provenance of default/private states; no cross-run PID/FD normalization is introduced. Default and True full nine-field order/type/bits checks remain complete.','Original pure 60/60 and fresh 1800/600, RSS512MiB, archive64MiB, history96GiB/free8GiB and genuine guard/MRO/threads1/child1/retry0 are unchanged.','This review is SOURCE-only; installation and binding are not helper protocol qualification, RSS/build/INPUT/native science admission.'])
    write('REVIEW.json',review)
    print(json.dumps(dict(status=review['status'],source_only=True,check_count=review['check_count'],blockers=[],review_pin=pin(OUT/'REVIEW.json'),output=str(OUT)),separators=(',',':')))

if __name__=='__main__':
    main()
