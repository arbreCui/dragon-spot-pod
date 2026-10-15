import hashlib,json,tempfile
from pathlib import Path
OLD=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_native_AB_persisted_XSM_ASCII_v22_sources/sealed_independent_actual_bound_native_SOURCE_review/review_actual_bound_complete_native_SOURCE_stdlib.py')
old=OLD.read_bytes();assert hashlib.sha256(old).hexdigest()=='17c3a313b2c1fdff3bfe2c0f1cd79bfac7d1c450e2a5ea1ce610739c77f74269'
out=Path(tempfile.mkdtemp(prefix='axmat_native_v23_actual_BOUND_complete_independent_SOURCE_review_20261010_',dir='/private/tmp'))
t=old.decode();changes=[]
def replace(a,b,count=1):
    global t
    assert t.count(a)==count,(a,t.count(a),count)
    t=t.replace(a,b);changes.append(dict(old=a,new=b,count=count))
replace("P=Path('/private/tmp/axmat_complete_native_actual_BOUND_SOURCE_ROOT_20261010_503adf')","P=Path('/private/tmp/axmat_complete_native_v23_actual_BOUND_SOURCE_ROOT_20261010_748877')")
replace("A=Path('/private/tmp/axmat_native_host_BINDER_STRICT_SCOPE_UNREADY_SOURCE_20261010_gs2tnzvo')","A=Path('/private/tmp/axmat_native_v23_strict_bool_complete_SOURCE_ens_zo_p')")
replace("OUT=Path('/private/tmp/axmat_native_actual_BOUND_complete_SOURCE_peer__g2keoz6')","OUT=Path("+repr(str(out))+")")
replace("'bce973287d8776ddcfca502494f9f9dff0113d653aa316666ebfa962a4ea74d9'","'dfb3278dcab1c9db3af8dd82edace64dd24373c550c0b7d75047135144670958'")
replace("m['member_count']==len(m['members'])==88 and m['original_complete_parent_member_count']==83","m['member_count']==len(m['members'])==273 and m['original_complete_parent_member_count']==267")
replace("'f1b5cd5fc1b01077b1fc181c5da1199020570ff7c9ba569355f875c0f5bd4ffa'and len(am['members'])==82","'dd422e462869baf9edfc4652bd2111912be7d31be326c9c81190375671b92511'and len(am['members'])==267")
for a,b in [
 ('067838d4d01a2c8509fcf771c4ba2d9c78945780f2041ca691a5f57725fda155','765fb053ae13a10aa71cd9d20ced1aff4a8f275d7b2a2a3ac9a838a403927d87'),
 ('29e4a9d6903f548064bae30c7a9fbf658bf7fb17b3340b421f9abecac280a20b','90d4cf339eaa2aceb01e9736f65443351c64948ff96496b8d6a416dcf022f76f'),
 ('403feaa916159c901f7b4f44c6a7c70798afac7ce5035cdbded90a14a5c96517','9d8494234a3a6d58ef4cf8f151ff0505f35c750929ad444dfee8ca8a667dedb0'),
 ('0b36a6ecab0db339058eec23eab0cd09747d8a8979f81a00a1b7bf2c21c352c1','505ec5800adb2793837a717e0d504a6e1d636620cc347cc97c870f66daa19c5d')]:replace(a,b)
replace("rec['complete_parent_Source_members']==82","rec['complete_parent_Source_members']==267")
replace("'7a80064209ee3aa4ff15a9240a378643ff03ffe34b2159be501f3d6112e28816'","'42d2f2d903fde7515f3c312c5e2f3c49ed2744aecade896ca14ca5eb5d2c8c7f'")
replace('5741','4528',10)
replace("0,'503adf'","0,'748877'")
replace("t=tool['actual_tool_return'];check('actualbinder true7f9a7f typed0 CLOSED',tool['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_BINDING_TOOL_RETURN_V1'and tool['source_only']is True and tool['closed']is True and tool['observed_terminal']is True and type(t['exit_code'])is int and t['exit_code']==0 and t['chunk_id']=='7f9a7f'and 'session_id'not in t)","t=tool['terminal_tool_return'];check('actualbinder truef73f14 typed0 CLOSED',tool['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_BINDING_TOOL_TERMINAL_RETURN_V1'and tool['source_only']is True and tool['closed']is True and tool['observed_terminal']is True and tool['session_repolled_after_close']is False and tool['actual_terminal_chunk']==t['chunk_id'] and type(t['exit_code'])is int and t['exit_code']==0 and t['chunk_id']=='f73f14'and 'session_id'not in t)")
replace('actualSource89_fullinventory','actualSource274_fullinventory')
replace('all89_files_beforeafter_fixed','all274_files_beforeafter_fixed')
replace('all83_original_source_files_byteexact','all268_original_source_files_byteexact')
replace('actual89 files complete88plusmanifest','actual274 files complete273plusmanifest')
replace('all89 file inventory exact','all274 file inventory exact')
replace('author actual83 completefixedsource','author actual268 completefixedsource')
replace('all full83 parentSource byte copies','all full268 parentSource byte copies')
replace('real bound Source manifest bce973','real bound Source manifest dfb327')
prefix="""
# This auditor preserves the whole original 8133 reference protocol, adapting
# only the explicitly observed v23 Source family, counts and genuine tool schema.
# It imports no reviewed Source and never reads complete material payloads.
"""
t=prefix+t
insert="""
old_reference=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_native_AB_persisted_XSM_ASCII_v22_sources/sealed_independent_actual_bound_native_SOURCE_review/REVIEW.json')
oldref=json.loads(read(old_reference));check('preserved original8133 bound reference schema',pins[str(old_reference)]['sha256']=='8f585b96311e4818c99cddad4fe6b8032a19787d06ffc88e9bd9d04aeeab231b' and oldref['schema']=='INDEPENDENT_ACTUAL_BOUND_COMPLETE_NATIVE_SOURCE_REVIEW_V1' and oldref['status']=='PASS_ACTUAL_BOUND_COMPLETE_NATIVE_SOURCE_ONLY' and oldref['all_checks_typed_true'] is True and oldref['blockers']==[] and oldref['check_count']==len(oldref['checks'])==8133)
check('new_source_does_not_reuse_old_actual_native_or_science_credit',b['actual_native_byte_qualification_sha256'] is None and b['actual_scientific_qualification_sha256'] is None)
checker_main=definitions(raw[checker_name])['main']
check('755_exact_bool_fix_in_bound_checker',"require(type(inputs) is list and len(inputs)>0, 'complete explicit input pins required')" in checker)
if any(n.name=='require' for n in definitions(raw[checker_name]).values()):
    req=definitions(raw[checker_name])['require'];check('strict_require_unchanged_exact_bool_gate',"type(value) is not bool" in ast.get_source_segment(checker,req))
check('originalv22_failed_native_retained_as_failure_not_priorBUILD',json.loads(raw['ACTUAL_V22_FAILED_SOURCE_AND_META/RECEIPTS/Root_actual_complete_native_tool_terminal_return.json'])['terminal_tool_return']['exit_code']==1)
check('manifest_full_newparent_Source_not_runtime',m['original_complete_parent_member_count']==267 and m['actual_native_execution'] is False)
check('actual_admission_source_contract_precisely_request_coupled',exact(request['Source_admission_contract'],adm) and exact(request['actual_Source_admission_tool_contract']['terminal_tool_return'],source_truth['terminal_tool_return']))
check('actual_source_receipt_output_three_direct_values_not_fabricated',exact(request['actual_Source_admission_tool_contract']['required_actual_terminal_output'],stdout))
check('prior_BUILD_complete_schema_EXIT1_not_v22nativefailure',b['prior_actual_V22_build_tool_return_pin']['sha256']=='7b66ecbcac1048e079b8197a7821e12761d05c55d4ff6603555c53d220f09d07' and build_truth['schema']=='ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1')
check('all27fbeadmission_scope_and_4528peer_pin_current',b['source_admission_pin']['sha256']=='27fbe88b45493ce20b29a69866ecbab57a04cb1e1097ac564c92fea4ad99bc3e' and b['independent_host_binder_Source_review_pin']['sha256']=='9521056f8efefaefcd282a64a103feb52b841492ebf639647a8d24656c90fb1b')
read(old_reference);check('old8133_reference_fullpin_beforeafter',pins[str(old_reference)]==first[str(old_reference)])
"""
replace_marker="check('complete allchecks unique typedtrue',"
assert t.count(replace_marker)==1;t=t.replace(replace_marker,insert+'\n'+replace_marker)
extra="""
report['original8133_bound_review_reference_pin']=pins[str(old_reference)]
report['original8133_count_not_claimed_as_new_run']=True
report['actual_source_file_count_including_manifest']=274
report['original_parent_source_file_count_including_manifest']=268
report['whole_combined_build_qualified']=False
report['whole_combined_INPUT_admitted']=False
report['physical_balance_qualified']=False
report['scientific_accuracy_qualified']=False
report['all_original_bound_review_contract_scope_retained']=True
report['all_six_future_business_pins_still_None']=all(hg[k] is None for k in ('ACTUAL_PROTOCOL_QUALIFICATION_SHA256','ACTUAL_TRANSFER_QUALIFICATION_SHA256','REACTION_MULTIPLICITY_QUALIFICATION_SHA256','ACTUAL_SCIENTIFIC_REFERENCE_SHA256','PROTOCOL','PROTOCOL_SHA'))
"""
marker="(OUT/'REVIEW.json').write_text";assert t.count(marker)==1;t=t.replace(marker,extra+'\n'+marker)
(out/'review_actual_bound_complete_native_v23_SOURCE_stdlib.py').write_text(t)
(out/'original8133_review_actual_bound_complete_native_SOURCE_stdlib.py').write_bytes(old)
(out/'auditor_Source_adaptation_record.json').write_text(json.dumps(dict(schema='INDEPENDENT_V23_ACTUAL_BOUND_SOURCE_AUDITOR_ADAPTATION_V1',original_auditor_path=str(OLD),original_auditor_sha256=hashlib.sha256(old).hexdigest(),finite_retargets=changes,original_complete_protocol_preserved=True,no_reviewed_Source_executed=True),indent=2)+'\n')
print(json.dumps(dict(directory=str(out),audit_script=str(out/'review_actual_bound_complete_native_v23_SOURCE_stdlib.py'),source_only=True)))
