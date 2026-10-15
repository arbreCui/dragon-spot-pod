import ast,hashlib,json,os,pathlib,stat,tempfile,time
START=time.monotonic();OLD=pathlib.Path('/private/tmp/SPOT_INSTALLED6A_NEW_Q_FACTORY_CORRECTED_SOURCE_ONLY_V29_m_27vcch');BASE=pathlib.Path('/private/tmp/SPOT_INSTALLED6A_NEW_Q_FACTORY_SOURCE_ONLY_V29_wbh7cowp');NEW=pathlib.Path(tempfile.mkdtemp(prefix='SPOT_INSTALLED6A_NEW_Q_FACTORY_SOURCE_ONLY_V29_V3_COUNTFINAL_',dir='/private/tmp'))
def ids(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=pathlib.Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and not any(q.is_symlink() for q in (p,*p.parents));h=hashlib.sha256();n=0
 with p.open('rb') as f:
  assert ids(os.fstat(f.fileno()))==ids(s)
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
  assert ids(os.fstat(f.fileno()))==ids(s)
 assert ids(p.lstat())==ids(s) and n==s.st_size
 return dict(path=str(p),size_bytes=n,sha256=h.hexdigest(),identity=ids(s))
def put(p,v):
 b=v if isinstance(v,bytes) else (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 return pin(p)
M=json.loads((OLD/'FINAL_CORRECTED_SOURCE_ONLY_MANIFEST.json').read_bytes());P=json.loads((OLD/'CORRECTED_SOURCE_WHOLE_INVERSE_AND_SCHEMA_PROOF.json').read_bytes());B=json.loads((BASE/'FINAL_SOURCE_ONLY_MANIFEST.json').read_bytes());A=pathlib.Path('/private/tmp/new_q_contract_independent_audit_v29_v2_countfinal_20261011.json');S=pathlib.Path('/private/tmp/new_q_contract_independent_scope_supplement_v29_v2_countfinal_20261011.json');AD=json.loads(A.read_bytes());SD=json.loads(S.read_bytes());assert AD['check_count']==len(AD['checks'])==5400 and all(type(c['passed'])is bool and c['passed']is True for c in AD['checks']);assert len(AD['all_verified_inputs'])==209
for r in AD['all_verified_inputs']:assert pin(r['path'])==r
W=(OLD/'WRITE_ACTUAL_NEW_INSTALLED6A_METADATA_Q_AFTER_ROOT_REVIEW.py').read_text();F=(OLD/'UNREADY_NEW_INSTALLED6A_ORIGINAL_COMBINED_FACTORY.py').read_text();assert pin(OLD/'WRITE_ACTUAL_NEW_INSTALLED6A_METADATA_Q_AFTER_ROOT_REVIEW.py')==M['corrected_writer_Source'];assert pin(OLD/'UNREADY_NEW_INSTALLED6A_ORIGINAL_COMBINED_FACTORY.py')==M['corrected_UNREADY_factory_Source'];failed_tools=pathlib.Path('/private/tmp/Root_corrected_new6a_Q_actual_tool_returns_20261011.json');FT=json.loads(failed_tools.read_bytes());assert FT['initial']==FT['closed'] and FT['closed']['chunk_id']=='7ed0a8' and type(FT['closed']['exit_code'])is int and FT['closed']['exit_code']==1 and 'session_id'not in FT['closed'];assert not pathlib.Path(M['old_candidate_Q_output_path']).parent.exists()
currentpaths=[pathlib.Path('/private/tmp/new_q_contract_independent_audit_v29_20261011.py'),pathlib.Path('/private/tmp/new_q_contract_independent_audit_v29_20261011.json'),pathlib.Path('/private/tmp/new_q_contract_independent_scope_supplement_v29_20261011.json'),pathlib.Path('/private/tmp/new_q_contract_independent_audit_v29_v2_countfinal_20261011.py'),A,S,pathlib.Path('/private/tmp/new_q_independent_audit_v2_countfinal_Source_inverse_20261011.json'),pathlib.Path('/private/tmp/new_q_contract_independent_audit_v2_actual_tool_return_20261011.json'),pathlib.Path('/private/tmp/new_q_corrected_source_prepare_v29_20261011.py'),pathlib.Path('/private/tmp/new_q_corrected_source_prepare_v29_v2_20261011.py'),pathlib.Path('/private/tmp/new_q_corrected_source_prepare_v1_actual_failed_tool_return_20261011.json'),pathlib.Path('/private/tmp/new_q_corrected_source_v2_final_schema_review_20261011.json'),failed_tools,pathlib.Path(__file__)]
currentpins=[pin(p) for p in currentpaths];audits=[pin(A),pin(S)];failednames=sorted(p.name for p in OLD.iterdir());assert len(failednames)==4
changes=[]
def change(a,b):
 global W
 assert W.count(a)==1,(a[:140],W.count(a));W=W.replace(a,b,1);changes.append(dict(before=a,after=b))
change('_AUDIT_EVIDENCE_PINS='+repr(M['independent_source_audit_and_precise_scope_supplement']),'_AUDIT_EVIDENCE_PINS='+repr(audits))
change('_SOURCE_ROOTS = [Path(OLD_SOURCE_ROOT), Path(__file__).parent]',"_SOURCE_ROOTS = [Path(OLD_SOURCE_ROOT), Path(FAILED_WRITER_SOURCE_ROOT), Path(__file__).parent]")
extra='\nFAILED_WRITER_SOURCE_ROOT='+repr(str(OLD))+'\n_FAILED_SOURCE_NAMES='+repr(failednames)+'\n_CURRENT_FRESH_EXPLICIT_PINS='+repr(currentpins)+'\n_FAILED_WRITER_ACTUAL_TOOLS_PIN='+repr(pin(failed_tools))+"\n_ROOT_REVIEW_SOURCE_PATH='/private/tmp/Root_review_corrected_new6a_Q_Source_v3_20261011.py'\n_ROOT_REVIEW_REPORT_PATH='/private/tmp/Root_corrected_new6a_Q_independent_Source_review_v3_20261011.json'\n_CURRENT_FRESH_RUNTIME_PINS=[]\n"
extra+='''
def verify_current_fresh_inputs_and_actual_Root_prelaunch_review():
    global _CURRENT_FRESH_RUNTIME_PINS
    for r in _CURRENT_FRESH_EXPLICIT_PINS:assert pin(r['path'])==r
    failed=_read_pinned_audit(_FAILED_WRITER_ACTUAL_TOOLS_PIN)
    assert failed['initial']==failed['closed'] and failed['closed']['chunk_id']=='7ed0a8' and type(failed['closed']['exit_code']) is int and failed['closed']['exit_code']==1 and 'session_id' not in failed['closed']
    assert 'verify_preserved_independent_audit_inputs' in failed['closed']['output'] and 'AssertionError' in failed['closed']['output']
    root_Source_pin=pin(_ROOT_REVIEW_SOURCE_PATH);root_report_pin=pin(_ROOT_REVIEW_REPORT_PATH)
    root_report=_read_pinned_audit(root_report_pin)
    assert root_report['status']=='ROOT_SOURCE_REVIEW_PASS_AUTHORIZE_ONE_ACTUAL_NEW6A_METADATA_Q_WRITER'
    assert root_report['writer']==pin(__file__) and root_report['metadata_contract']==CONTRACT_PIN
    assert root_report['manifest']==pin(Path(__file__).parent/'FINAL_CORRECTED_SOURCE_ONLY_MANIFEST.json')
    for key in ('whole_writer_inverse_and_original_function_AST_equal','whole_factory_inverse_to_117ec099_equal','original_resource_prefix_preserved','original_scientific_and_complete_build_gates_not_granted'):assert root_report[key] is True
    _CURRENT_FRESH_RUNTIME_PINS=_CURRENT_FRESH_EXPLICIT_PINS+[root_Source_pin,root_report_pin]
'''
change('# A new Source family is added without altering the original resource prefix.',extra+'\n# A new Source family is added without altering the original resource prefix.')
change("namespaces=[complete_Source_namespace(_SOURCE_ROOTS[0],_OLD_SOURCE_NAMES),complete_Source_namespace(_SOURCE_ROOTS[1],_NEW_SOURCE_NAMES)]","namespaces=[complete_Source_namespace(_SOURCE_ROOTS[0],_OLD_SOURCE_NAMES),complete_Source_namespace(_SOURCE_ROOTS[1],_FAILED_SOURCE_NAMES),complete_Source_namespace(_SOURCE_ROOTS[2],_NEW_SOURCE_NAMES)]")
change('    return total,root_records','''    for r in _CURRENT_FRESH_RUNTIME_PINS:
        assert pin(r['path'])==r
        key=(r['identity'][0],r['identity'][1]);added=0
        if key not in seen:seen.add(key);total+=r['size_bytes'];added=r['size_bytes']
        root_records.append(dict(path=r['path'],identity=r['identity'],new_unique_regular_bytes=added,kind='current_stage_fresh_explicit_regular_file'))
    return total,root_records''')
change('for r in _PRESERVED_AUDIT_INPUTS:assert pin(r[\'path\'])==r',"for r in _PRESERVED_AUDIT_INPUTS+_CURRENT_FRESH_RUNTIME_PINS:assert pin(r['path'])==r")
change('min(frees.values())-reserve>=8*2**30',"min([*frees.values(),*(int(os.statvfs(Path(r['path']).parent).f_bavail)*int(os.statvfs(Path(r['path']).parent).f_frsize) for r in _CURRENT_FRESH_RUNTIME_PINS)])-reserve>=8*2**30")
change('tmp_disk_free_bytes=frees,min_free_bytes=8*2**30',"tmp_disk_free_bytes=frees,current_stage_fresh_explicit_file_pins=_CURRENT_FRESH_RUNTIME_PINS,min_free_bytes=8*2**30")
change('fixed+extra+_PRESERVED_AUDIT_INPUTS+[r for ns in _SOURCE_NAMESPACE_BEFORE for r in ns[\'files\']]','fixed+extra+_PRESERVED_AUDIT_INPUTS+_CURRENT_FRESH_RUNTIME_PINS+[r for ns in _SOURCE_NAMESPACE_BEFORE for r in ns[\'files\']]')
change('verify_preserved_independent_audit_inputs()\nassert len(sys.argv)', 'verify_current_fresh_inputs_and_actual_Root_prelaunch_review()\nverify_preserved_independent_audit_inputs()\nassert len(sys.argv)')
wp=put(NEW/'WRITE_ACTUAL_NEW_INSTALLED6A_METADATA_Q_AFTER_ROOT_REVIEW.py',W.encode());oldexp='EXPECTED_NEW6A_Q_WRITER_SOURCE_PIN='+repr(M['corrected_writer_Source']);newexp='EXPECTED_NEW6A_Q_WRITER_SOURCE_PIN='+repr(wp);assert F.count(oldexp)==1;F=F.replace(oldexp,newexp,1);fp=put(NEW/'UNREADY_NEW_INSTALLED6A_ORIGINAL_COMBINED_FACTORY.py',F.encode())
r=W
for c in reversed(changes):assert r.count(c['after'])==1;r=r.replace(c['after'],c['before'],1)
assert r.encode()==(OLD/'WRITE_ACTUAL_NEW_INSTALLED6A_METADATA_Q_AFTER_ROOT_REVIEW.py').read_bytes();original=r
for c in reversed(P['writer_forward_changes']):assert original.count(c['after'])==1;original=original.replace(c['after'],c['before'],1)
assert original.encode()==pathlib.Path(P['original_writer']['path']).read_bytes()
f2=F.replace(newexp,oldexp,1);assert f2.encode()==(OLD/'UNREADY_NEW_INSTALLED6A_ORIGINAL_COMBINED_FACTORY.py').read_bytes();fbase=f2.replace(P['factory_corrected_assignment_after'],P['factory_corrected_assignment_before'],1);assert fbase.encode()==(BASE/'UNREADY_NEW_INSTALLED6A_ORIGINAL_COMBINED_FACTORY.py').read_bytes();foriginal=fbase.replace(B['factory_added_constants'],'',1)
for c in reversed(B['factory_forward_changes']):assert foriginal.count(c['after'])==1;foriginal=foriginal.replace(c['after'],c['before'],1)
assert foriginal.encode()==pathlib.Path(B['actual_original_closed_endpoints']['old_immutable_factory']['path']).read_bytes()
def defs(t):return {n.name:ast.dump(n,include_attributes=False) for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
a=defs(ast.parse(original));b=defs(ast.parse(W));assert all(b[k]==v for k,v in a.items());assert defs(ast.parse(foriginal))['helper_Q_admission']!=defs(ast.parse(F))['helper_Q_admission'];assert defs(ast.parse((OLD/'UNREADY_NEW_INSTALLED6A_ORIGINAL_COMBINED_FACTORY.py').read_bytes()))==defs(ast.parse(F))
assert W.count(B['Q_writer_original_prefix_after'])==1;assert hashlib.sha256(B['Q_writer_original_prefix_before'].encode()).hexdigest()==B['Q_writer_prefix_original_full_inverse_sha256']
proof=dict(status='SOURCE_ONLY_V3_STRICT_FINAL_COUNT_NEW_FRESH_INPUTS_AND_ROOT_PRELAUNCH_BINDING_NO_EXECUTION',failed_corrected_v2_writer_Source=M['corrected_writer_Source'],corrected_v3_writer_Source=wp,failed_corrected_v2_factory_Source=M['corrected_UNREADY_factory_Source'],corrected_v3_factory_Source=fp,v3_to_failed_v2_writer_complete_whole_inverse_byte_exact=True,v3_to_failed_v2_writer_sha256=hashlib.sha256(r.encode()).hexdigest(),v3_writer_forward_changes=changes,v2_to_original531_writer_forward_changes=P['writer_forward_changes'],v3_to_original531_writer_complete_whole_inverse_byte_exact=True,v3_to_original531_writer_sha256=hashlib.sha256(original.encode()).hexdigest(),original_writer_function_and_class_AST_entirely_identical=True,original_resource_prefix_preserved_bytes_and_AST=True,original_resource_prefix_full_inverse_sha256=B['Q_writer_prefix_original_full_inverse_sha256'],factory_v3_to_failed_v2_assignment_before=oldexp,factory_v3_to_failed_v2_assignment_after=newexp,factory_v2_to_v1_assignment_before=P['factory_corrected_assignment_before'],factory_v2_to_v1_assignment_after=P['factory_corrected_assignment_after'],factory_v1_added_constants=B['factory_added_constants'],factory_v1_forward_changes=B['factory_forward_changes'],v3_to_original117ec_factory_complete_whole_inverse_byte_exact=True,v3_to_original117ec_factory_sha256=hashlib.sha256(foriginal.encode()).hexdigest(),all_failed_v2_factory_function_and_class_AST_identical=True,actual_5400_saved_check_count_equals5400_saved_checks=True,actual209_full_original_EOF7ID_inputs_held=AD['all_verified_inputs'],no_strict_count_predicate_relaxed=True,new_actual_audit_scope_pins=audits,Source_only=True,writer_factory_Native_or_PS_executed=False,Q_created=False)
pp=put(NEW/'CORRECTED_SOURCE_WHOLE_INVERSE_AND_SCHEMA_PROOF.json',proof)
manifest=dict(status='NEW6A_Q_WRITER_V3_STRICT_FINAL_COUNT_COMPLETE_FRESH_INPUTS_ROOT_REVIEW_SOURCE_ONLY_PENDING_ROOT',corrected_writer_Source=wp,corrected_UNREADY_factory_Source=fp,whole_inverse_and_actual_schema_proof=pp,metadata_contract_Source=M['metadata_contract_Source'],failed_v2_Source_manifest=pin(OLD/'FINAL_CORRECTED_SOURCE_ONLY_MANIFEST.json'),failed_v2_actual_writer_tools=pin(failed_tools),complete_original209_audit_inputs=AD['all_verified_inputs'],actual_independent_audit5400_checks_strict_count=True,new_actual_audit_and_precise_scope_supplement=audits,three_complete_Q_Source_family_roots=[str(BASE),str(OLD),str(NEW)],explicit_current_stage_fresh_inputs=currentpins,prelaunch_Root_review_contract=dict(Source_path='/private/tmp/Root_review_corrected_new6a_Q_Source_v3_20261011.py',report_path='/private/tmp/Root_corrected_new6a_Q_independent_Source_review_v3_20261011.json',required_status='ROOT_SOURCE_REVIEW_PASS_AUTHORIZE_ONE_ACTUAL_NEW6A_METADATA_Q_WRITER',writer_field='writer',metadata_contract_field='metadata_contract',current_manifest_field='manifest',required_true_fields=['whole_writer_inverse_and_original_function_AST_equal','whole_factory_inverse_to_117ec099_equal','original_resource_prefix_preserved','original_scientific_and_complete_build_gates_not_granted'],no_future_review_SHA_embedded=True,dynamic_actual_review_two_full_EOF7ID_inputs_required_and_accounted=True),expected_future_actual_writer_tool_file='/private/tmp/Root_corrected_new6a_Q_v3_actual_tool_returns_20261011.json',old_candidate_Q_output_path=M['old_candidate_Q_output_path'],actual_Q_pin=None,factory_future_Q_and_external_closure_still_None=True,original_joint_account_prefix_and_complete_physics_functions_unchanged=True,original_600s_512MiB_2GiB_96GiB_free8GiB_fiveguards_DE_held=True,actual_after_Q_resource_witness_and_afterwitness_stdout_retained=True,reused_v27_v28_historical_protocol_64_and_history96_scope_unchanged=True,Source_preparation_only=True,writer_factory_Native_or_PS_executed=False,Q_created=False,whole_INPUT_native_BOOT_AAA_ABA_admitted=False,preparation_Source=pin(__file__),elapsed_seconds=time.monotonic()-START)
mp=put(NEW/'FINAL_CORRECTED_SOURCE_ONLY_MANIFEST.json',manifest)
assert len(list(NEW.iterdir()))==4
for r in AD['all_verified_inputs']:assert pin(r['path'])==r
for r in currentpins:assert pin(r['path'])==r
print(json.dumps(dict(Source_root=str(NEW),writer=wp,factory=fp,proof=pp,manifest=mp,actual_5400_of5400_count=True,Source_only=True,writer_factory_Native_or_PS_executed=False,Q_created=False)))
