"""Author finite Source derivatives only. Never import any candidate/API/guard."""
import ast
import difflib
import hashlib
import json
from pathlib import Path

P=Path(__file__).resolve().parent
parent=P/'PARENT_GENUINE_NATIVE_HOST'
old_host=(parent/'complete_native_XSM_ASCII_genuine_host.UNREADY.py').read_text()
old_binder=(parent/'bind_complete_native_SOURCE_only.UNREADY.py').read_text()
replacements={
 'COMPLETE_NATIVE_XSM_ASCII':'COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION',
 'complete_native_XSM_ASCII':'complete_final_MICROLIB_MACROLIB_aggregation',
 'complete_native_checker':'complete_final_aggregation_engine',
 'ACTUAL_COMPLETE_NATIVE_PERSISTED_XSM_ASCII_BIT_EVIDENCE_ONLY_V1':'ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_EVIDENCE_ONLY_V1',
 'ROOT_ACTUAL_COMPLETE_NATIVE_XSM_ASCII_BINDING_V1':'ROOT_ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_BINDING_V1',
 'INDEPENDENT_COMPLETE_NATIVE_GENUINE_HOST_BINDER_SOURCE_REVIEW_V1':'INDEPENDENT_COMPLETE_FINAL_AGGREGATION_ENGINE_HOST_BINDER_SOURCE_REVIEW_V1',
 'ROOT_ACTUAL_COMPLETE_NATIVE_HOST_BINDER_SOURCE_ADMISSION_V1':'ROOT_ACTUAL_COMPLETE_FINAL_AGGREGATION_ENGINE_HOST_BINDER_SOURCE_ADMISSION_V1',
 'ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1':'ROOT_ACTUAL_COMPLETE_FINAL_AGGREGATION_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1',
 'ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_ONLY_NOT_RUNTIME_OR_SCIENCE':'ACTUAL_COMPLETE_FINAL_AGGREGATION_SOURCE_ADMISSION_ONLY_NOT_RUNTIME_OR_SCIENCE',
 'ACTUAL_COMPLETE_NATIVE_SOURCE_SCOPE_COUPLING_V1':'ACTUAL_COMPLETE_FINAL_AGGREGATION_SOURCE_SCOPE_COUPLING_V1',
 'CURRENT150_AB_GENUINE_COMPLETE_NATIVE_PERSISTED_XSM_ASCII_HOST_V1':'CURRENT150_AB_GENUINE_COMPLETE_FINAL_AGGREGATION_HOST_V1',
 'ACTUAL_SAVED_COMPLETE_NATIVE_PERSISTED_BYTE_EVIDENCE_ONLY_EXTERNAL_ROOT_CLOSURE_REVIEW_REQUIRED':'ACTUAL_COMPLETE_CONSTRUCTION_EVIDENCE_ONLY_EXTERNAL_ROOT_CLOSURE_REQUIRED',
 'FAILED_COMPLETE_NATIVE_BYTE_CHECK_NO_RETRY_NO_QUALIFICATION':'FAILED_COMPLETE_FINAL_AGGREGATION_NO_RETRY_NO_QUALIFICATION',
 'actual_native_byte_qualification_sha256':'new_aggregation_qualification_sha256',
 'new_native_walker_controls_actual_run':'new_complete_aggregation_controls_actual_run',
 'native_xsm_ascii':'final_micro_macro_aggregation',
 'all_four_actual_author_Source_fullpins_coupled':'all_five_actual_author_Source_fullpins_coupled',
 'NEW_NATIVE_WALKER_CONTROLS_NOT_EXECUTED':'NEW_COMPLETE_AGGREGATION_CONTROLS_NOT_EXECUTED',
}
host=old_host
for a,b in replacements.items():host=host.replace(a,b)
host=host.replace("'qualified_source_manifest','host_template','checker_template','binder'",
                  "'qualified_source_manifest','host_template','engine_template','adapter','binder'")
host=host.replace("len(b['complete_input_pins'])==129", "len(b['original129_input_pins'])==129 and len(b['complete_input_pins'])>=129")
host=host.replace("len({p['path']for p in b['complete_input_pins']})==129", "len({p['path']for p in b['complete_input_pins']})==len(b['complete_input_pins']) and b['complete_input_pins'][:129]==b['original129_input_pins']")
old="""        require(report['schema']=='ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_EVIDENCE_ONLY_V1'and report['source_binding']['sha256']==BINDING_SHA and report['original_caps']==CAPS and report['native_persisted_XSM_value_bits_verified']is True,'actual complete persisted-native byte comparison only')
        require([row['state']for row in report['states']]==['A','B']and report['all_complete_state_scope_retained']is True,'complete A release then B required')
        for row in report['states']:
            macro,micro=row['complete_MACROLIB'],row['complete_MICROLIB']
            require(type(macro['records'])is int and macro['records']==19619 and macro['physical_headers_including_all_closes']==19990 and macro['numeric_components']==2264113,'full original macro scope')
            require(row['native_persisted_XSM_value_bits_verified']is True and all(v['all_persisted_native_value_bits_equal_ASCII']is True and v['native_physical_preorder_equal_original_ASCII']is True and v['all_complete_orders_preserved_on_disk']is True for v in(macro,micro)),'full original micro/macro type/order/value bits')
"""
new="""        require(report['schema']=='ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_EVIDENCE_ONLY_V1'and report['source_binding']['sha256']==BINDING_SHA and report['original_caps']==CAPS and report['complete_final_construction_qualified']is False,'honest final construction evidence only, no science or historical machine arithmetic')
        require([row['state']for row in report['states']]==['A','B']and report['all_complete_state_scope_retained']is True,'complete A release then B required')
        for row in report['states']:
            require(type(row['complete_MACROLIB_records'])is int and row['complete_MACROLIB_records']==19619 and row['original_scope']==[370,8,3,32,64,62,18,6,48],'all original complete aggregation scope')
            require(row['all_original_native_records_and_bytes_preserved']is True and row['all_state_databases_and_pool_closed_before_next_state']is True and row['complete_final_construction_qualified']is False,'no scope reduction, no fabricated construction PASS')
"""
assert old in host
host=host.replace(old,new)
# Current complete evidence engine deliberately returns nonzero for unresolved
# producers/history. The original runner thus records genuine FAIL and retains
# its full report in the unchanged failure path. No wrapper turns it into PASS.
host=host.replace('native_persisted_XSM_value_bits_verified=True,','complete_final_construction_qualified=False,')
host=host.replace('native_persisted_XSM_value_bits_verified=False,','complete_final_construction_qualified=False,')
host=host.replace('complete native persisted-byte stage','complete saved final-micro construction stage')
host=host.replace('actual_native=stage','actual_aggregation=stage')
host=host.replace('actual_native_report_pin_if_saved','actual_complete_construction_report_pin_if_saved')
host=host.replace('ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_EVIDENCE_REPORT.json',
                  'ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_REPORT.json')
failure_anchor="""        if host.is_dir():
            saved=out/'ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_REPORT.json'
"""
failure_replacement="""        if host.is_dir():
            # The complete diagnostic intentionally exits2. Protect all inputs
            # and frozen D/E after that honest failure too, with no retry or
            # second child. A failed verification is saved, never labelled PASS.
            failure_post_inputs=[];failure_post_errors=[]
            for entry in inputs+[hpin,rpin,*genuine_pins]:
                try:
                    require(time.monotonic()-started<WHOLE_CAP,'whole budget during failure fullEOF checks')
                    actual=support.pin(entry['path'],entry['sha256'])
                    require(actual==entry,'complete protected input changed after failure')
                    failure_post_inputs.append(actual)
                except BaseException as post_error:
                    failure_post_errors.append(dict(path=entry['path'],error=repr(post_error)))
            failure_resources_after=None;failure_freeze_after=None
            try:
                failure_resources_after=resources.check()
                failure_freeze_after=dict(Source=complete_source_inputs(support,archive),receipts=complete_source_inputs(support,receipts),Source_directories=complete_directory_identity(archive),receipt_directories=complete_directory_identity(receipts))
                require(failure_freeze_after==dict(Source=source_inputs,receipts=receipt_inputs,Source_directories=source_directories,receipt_directories=receipt_directories),'complete frozen Source and receipt namespaces changed after failure')
            except BaseException as post_error:
                failure_post_errors.append(dict(scope='full_D_E_and_resources',error=repr(post_error)))
            saved=out/'ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_REPORT.json'
"""
assert host.count(failure_anchor)==1
host=host.replace(failure_anchor,failure_replacement)
host=host.replace("error=repr(error),stage_records=[]if runner is None else runner.records,",
    "error=repr(error),input_sources_before=inputs,input_sources_after_failure=failure_post_inputs,full_postclose_input_and_D_E_check_errors=failure_post_errors,full_postclose_input_and_D_E_checked=not failure_post_errors,complete_D_E_freeze_after_failure=failure_freeze_after,resources_after_failure=failure_resources_after,complete_joint_HOCDE_archive_bytes_after_failure=support.archive_bytes(roots5),actual_host_PID=os.getpid(),original_caps=CAPS,genuine_guard_sources=genuine_pins,original_helper=hpin,resource_factory=rpin,stage_records=[]if runner is None else runner.records,")
host_name='complete_final_MICROLIB_MACROLIB_aggregation_genuine_host.UNREADY.py'
(P/host_name).write_text(host)

# Complete parent binder's pin, actual-terminal, five-source scope and reversible
# global-binding functions stay present. Its main is replaced for the new family.
prefix=old_binder[:old_binder.index('def main():')]
for a,b in replacements.items():prefix=prefix.replace(a,b)
prefix=prefix.replace('checker_template','engine_template')
prefix=prefix.replace('all original129','all original129 plus actual saved-native evidence')
main=r'''def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-manifest-sha256',required=True)
    parser.add_argument('--request',required=True)
    parser.add_argument('--request-sha256',required=True)
    parser.add_argument('--output-source-dir',required=True)
    args=parser.parse_args()
    mp=pin(P/'MANIFEST.json')
    require(mp['sha256']==args.source_manifest_sha256,'complete independent Source manifest')
    manifest=strict_json((P/'MANIFEST.json').read_bytes())
    members=manifest['members']
    require(type(members)is list and type(manifest['member_count'])is int and len(members)==manifest['member_count'],'complete author Source inventory')
    files=[]
    for f in sorted(P.rglob('*')):
        require(not f.is_symlink(),'complete Source copy cannot alias')
        if f.is_file()and f!=P/'MANIFEST.json':files.append(str(f))
    require(files==[m['path']for m in members],'no omitted/extra Source member')
    for m in members:typed_pin({k:m[k]for k in('path','sha256','size_bytes','identity')})
    rp=pin(args.request)
    require(rp['sha256']==args.request_sha256,'actual Root request full pin')
    request=strict_json(Path(args.request).read_bytes())
    require(request['schema']=='ROOT_ACTUAL_COMPLETE_FINAL_AGGREGATION_SOURCE_BINDING_REQUEST_V1'and request['source_only']is True,'new Source family only')
    for k in('source_admission_pin','actual_Root_Source_admission_tool_return_pin','independent_host_binder_Source_review_pin','prior_actual_V22_build_tool_return_pin','actual_native_terminal_pin','actual_native_saved_coverage_contract_pin'):
        typed_pin(request[k])
    source_truth=actual_terminal(request['actual_Root_Source_admission_tool_return_pin'],True,'ROOT_ACTUAL_COMPLETE_FINAL_AGGREGATION_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1')
    prior=actual_terminal(request['prior_actual_V22_build_tool_return_pin'],False,'ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1')
    # This prescribed Root observation wrapper keeps the original underlying
    # receipt/output intact. Honest native nonzero is allowed if full saved pools
    # independently exist; Source/binary linkage is not a made-up data gate.
    native=actual_terminal(request['actual_native_terminal_pin'],False,'ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVED_TERMINAL_FOR_AGGREGATION_V1')
    coverage=strict_json(Path(request['actual_native_saved_coverage_contract_pin']['path']).read_bytes())
    require(coverage['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_SAVED_POOL_COVERAGE_FOR_AGGREGATION_V1'and coverage['all_complete_paired_pools_saved']is True and coverage['actual_native_terminal_pin']==request['actual_native_terminal_pin']and coverage['state_order']==['A','B']and coverage['same_actual_native_report_and_independent_review_bound']is True and coverage['scientific_qualification_created']is False,'actual independent complete saved-pool coverage, not raw-reader qualification')
    for key in('actual_native_report_pin','actual_native_independent_review_pin'):typed_pin(coverage[key])
    expected=dict(qualified_source_manifest=mp,host_template=pin(P/'complete_final_MICROLIB_MACROLIB_aggregation_genuine_host.UNREADY.py'),engine_template=pin(P/'complete_final_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py'),adapter=pin(P/'saved_native_data_access_adapter.UNREADY.py'),binder=pin(Path(__file__).resolve()))
    coupling=source_scope_contract(request,expected,source_truth)
    namespaces=request['namespaces']
    require(type(namespaces)is dict and set(namespaces)=={'host','output','control','source','receipts'}and all(type(v)is str and Path(v).is_absolute()and '..'not in Path(v).parts for v in namespaces.values()),'complete genuine namespaces')
    paths={k:Path(v)for k,v in namespaces.items()}
    require(all(paths[k].is_relative_to(ART)and paths[k]!=ART for k in('host','output','control'))and all(paths[k].is_relative_to(BASE)and paths[k]!=BASE for k in('source','receipts')),'original history and separate Source/receipts')
    require(len(set(paths.values()))==5 and not any(a.is_relative_to(b)for a in paths.values()for b in paths.values()if a!=b),'five disjoint roots')
    require(all(not os.path.lexists(paths[k])for k in('host','output','control','source')),'fresh H/O/C/D zero retry')
    dest=Path(args.output_source_dir)
    require(dest.is_absolute()and dest.is_relative_to(Path('/private/tmp'))and not os.path.lexists(dest)and not dest.is_relative_to(P)and not P.is_relative_to(dest),'fresh TMP only')
    original=request['original129_input_pins']
    additional=request['additional_actual_evidence_input_pins']
    require(type(original)is list and len(original)==129 and type(additional)is list and len(additional)>0,'all original129 plus actual native/context/meta pins')
    complete=original+additional
    # Shape-only: Source binder MUST NOT hash or read numeric/native/material
    # inputs. Genuine host/child later protect all complete inputs at full EOF.
    for p in complete:
        require(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['path'])is str and Path(p['path']).is_absolute()and type(p['sha256'])is str and re.fullmatch('[0-9a-f]{64}',p['sha256'])is not None and type(p['size_bytes'])is int and p['size_bytes']>=0 and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int and x>=0 for x in p['identity'])and p['identity'][3]==1 and p['identity'][4]==p['size_bytes'],'all original exact typed input pin shapes')
    require(len({p['path']for p in complete})==len(complete),'all inputs unique, no replacement of129')
    states=request['states']
    require(type(states)is dict and set(states)=={'A','B'},'complete A/B states')
    for state in('A','B'):
        require(states[state]==coverage['states'][state]and type(states[state])is dict and set(states[state])=={'sqlite_pin','native_pool_pin'},'full actual paired native state pins')
        for p in states[state].values():
            require(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['path'])is str and Path(p['path']).is_absolute()and type(p['sha256'])is str and re.fullmatch('[0-9a-f]{64}',p['sha256'])is not None and type(p['size_bytes'])is int and p['size_bytes']>=0 and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int and x>=0 for x in p['identity'])and p['identity'][3]==1 and p['identity'][4]==p['size_bytes'],'strict shape paired native pins without Source-only payload read')
        require(all(states[state][k]in complete for k in('sqlite_pin','native_pool_pin')),'both paired native files protected by genuine fullinputs')
    require(request['new_aggregation_qualification_sha256']is None and request['actual_scientific_qualification_sha256']is None and request['new_complete_aggregation_controls_actual_run']is None,'future qualification unknown, no invented arithmetic/walker controls')
    # This unchanged sealed adapter has a real observed full7ID already. No
    # staging copy or guessed future inode is needed. Host pins its Source too.
    adapter_pin=expected['adapter']
    binding=dict(schema='ROOT_ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_BINDING_V1',source_only=True,Root_only_actual_execution=True,scientific_qualification_created=False,original_caps=CAPS,state_order=['A','B'],states=states,Source_route=dict(schema='ROOT_BOUND_FINAL_TONE_LIBMIX_SOURCE_ROUTE_V1',ITSTMP=0,historical_call_proved=False),namespaces=namespaces,joint_archive_roots=[namespaces[k]for k in('host','output','control','source','receipts')],original129_input_pins=original,complete_input_pins=complete,source_admission_pin=request['source_admission_pin'],actual_Root_Source_admission_tool_return_pin=request['actual_Root_Source_admission_tool_return_pin'],independent_host_binder_Source_review_pin=request['independent_host_binder_Source_review_pin'],prior_actual_V22_build_tool_return_pin=request['prior_actual_V22_build_tool_return_pin'],actual_author_Source_contract=expected,actual_Source_scope_coupling=coupling,saved_native_adapter_pin=adapter_pin,actual_native_terminal_pin=request['actual_native_terminal_pin'],actual_native_saved_coverage_contract_pin=request['actual_native_saved_coverage_contract_pin'],new_complete_aggregation_controls_actual_run=None,new_aggregation_qualification_sha256=None,actual_scientific_qualification_sha256=None,original_native_build_binary_Source_linkage_qualified=False,historical_original_context_saved=False)
    binding_raw=(json.dumps(binding,indent=2,allow_nan=False)+'\n').encode()
    binding_sha=hashlib.sha256(binding_raw).hexdigest()
    # Bind only the actual deterministic binding SHA. The genuine host and
    # child observe its installed full7ID and protect it before/after; the Source
    # binder never invents a copy's future inode/time and needs no second bind.
    engine=(P/'complete_final_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py').read_bytes()
    engine_bound,engine_inverse=bind_globals(engine,dict(SOURCE_STATUS='READY_ROOT_BOUND_SOURCE_ONLY',SOURCE_BINDING_SHA256=binding_sha,BOUND_ADAPTER_PIN=adapter_pin))
    engine_sha=hashlib.sha256(engine_bound).hexdigest()
    host=(P/'complete_final_MICROLIB_MACROLIB_aggregation_genuine_host.UNREADY.py').read_bytes()
    bound_host,host_inverse=bind_globals(host,dict(SOURCE_STATUS='READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED',SOURCE_ARCHIVE=namespaces['source'],RECEIPTS=namespaces['receipts'],HOST=namespaces['host'],OUT=namespaces['output'],CONTROL=namespaces['control'],TARGET=str(paths['source']/'Root_bound_complete_final_aggregation_engine.py'),TARGET_SHA=engine_sha,BINDING=str(paths['source']/'Root_actual_aggregation_SOURCE_binding.json'),BINDING_SHA=binding_sha,SOURCE_ADMISSION_SHA=request['source_admission_pin']['sha256']))
    shutil.copytree(P,dest)
    outputs={'Root_actual_aggregation_SOURCE_binding.json':binding_raw,'Root_bound_complete_final_aggregation_engine.py':engine_bound,'Root_bound_complete_final_aggregation_genuine_host.py':bound_host,'Root_actual_complete_aggregation_Source_binding_inverse.json':(json.dumps(dict(schema='ROOT_ACTUAL_COMPLETE_AGGREGATION_SOURCE_GLOBALS_FULL_INVERSE_V1',source_only=True,engine_full_inverse=engine_inverse,host_full_inverse=host_inverse,engine_original_bytes_restored=True,host_original_bytes_restored=True,installed_binding7ID_observed_only_at_actual_runtime=True),indent=2)+'\n').encode()}
    for name,raw in outputs.items():
        with(dest/name).open('xb')as stream:stream.write(raw)
    record=dict(schema='ROOT_ACTUAL_COMPLETE_AGGREGATION_SOURCE_BINDING_RECORD_V1',source_only=True,request=rp,author_manifest=mp,actual_Source_scope_coupling=coupling,actual_native_terminal=native,prior_actual_build_terminal=prior,complete_original129_preserved=True,complete_inputs_count=len(complete),bound_outputs={name:pin(dest/name)for name in outputs},actual_source_installed=None,actual_genuine_host_run=None,new_aggregation_qualification_sha256=None,actual_scientific_qualification_sha256=None,no_candidate_helper_API_guard_compile_execution=True,no_numeric_material_payload_read=True)
    with(dest/'Root_actual_complete_aggregation_Source_binding_record.json').open('x')as stream:json.dump(record,stream,indent=2,allow_nan=False);stream.write('\n')
    require(pin(P/'MANIFEST.json')==mp and pin(args.request)==rp,'complete Source/request unchanged')
    for m in members:typed_pin({k:m[k]for k in('path','sha256','size_bytes','identity')})
    print(json.dumps(dict(source_only=True,status='ACTUAL_AGGREGATION_SOURCE_DERIVED_UNREADY_NOT_RUN',binding_record=pin(dest/'Root_actual_complete_aggregation_Source_binding_record.json'),bound_outputs=record['bound_outputs'],complete_inputs_count=len(complete),actual_engine_activation=None),indent=2,allow_nan=False),flush=True)


if __name__=='__main__':main()
'''
binder=prefix+main
(P/'bind_complete_aggregation_SOURCE_only.UNREADY.py').write_text(binder)
proof=[]
for label,old,new in(('host',old_host,host),('binder',old_binder,binder)):
    a=old.splitlines(keepends=True);b=new.splitlines(keepends=True)
    hunks=[dict(tag=tag,old_start0=i,old_end0=j,new_start0=k,new_end0=l,old_full_lines=a[i:j],new_full_lines=b[k:l])for tag,i,j,k,l in difflib.SequenceMatcher(a=a,b=b,autojunk=False).get_opcodes()if tag!='equal']
    restored=b[:]
    for h in reversed(hunks):
        assert restored[h['new_start0']:h['new_end0']]==h['new_full_lines']
        restored[h['new_start0']:h['new_end0']]=h['old_full_lines']
    assert ''.join(restored)==old
    ast.parse(new)
    proof.append(dict(label=label,parent_sha256=hashlib.sha256(old.encode()).hexdigest(),candidate_sha256=hashlib.sha256(new.encode()).hexdigest(),all_hunks_full_inverse=hunks,complete_original_bytes_restored=True))
(P/'COMPLETE_HOST_BINDER_FULL_SOURCE_INVERSE.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps(dict(source_only=True,host_source_sha256=hashlib.sha256(host.encode()).hexdigest(),binder_source_sha256=hashlib.sha256(binder.encode()).hexdigest(),full_inverse_counts=[len(p['all_hunks_full_inverse'])for p in proof],candidate_or_guard_executed=False)))
