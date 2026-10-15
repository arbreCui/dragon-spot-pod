"""Complete genuine parent derivatives by Source text only. No API imports."""
import ast,difflib,hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parent;B=P/'COMPLETE_FIXED_PARENT_SOURCE';proof=[]
def one(s,a,b):assert s.count(a)==1,(a,s.count(a));return s.replace(a,b)
def emit(name,old,new):
    ast.parse(new);a=old.splitlines(keepends=True);b=new.splitlines(keepends=True)
    h=[dict(tag=t,old_start0=i,old_end0=j,new_start0=k,new_end0=l,old_full_lines=a[i:j],new_full_lines=b[k:l])for
        t,i,j,k,l in difflib.SequenceMatcher(a=a,b=b,autojunk=False).get_opcodes()if t!='equal']
    back=b[:]
    for x in reversed(h):assert back[x['new_start0']:x['new_end0']]==x['new_full_lines'];back[x['new_start0']:x['new_end0']]=x['old_full_lines']
    assert ''.join(back)==old;(P/name).write_text(new)
    proof.append(dict(candidate=name,original_SHA256=hashlib.sha256(old.encode()).hexdigest(),candidate_SHA256=hashlib.sha256(new.encode()).hexdigest(),complete_zero_based_hunks=h,original_full_bytes_restored=True))
schema_map={
 'ROOT_ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_BINDING_V1':'ROOT_ACTUAL_COMPLETE_CONTEXT_AWARE_MICRO_MACRO_BINDING_V2',
 'ROOT_ACTUAL_COMPLETE_FINAL_AGGREGATION_SOURCE_BINDING_REQUEST_V1':'ROOT_ACTUAL_COMPLETE_CONTEXT_AWARE_SOURCE_BINDING_REQUEST_V2',
 'ROOT_ACTUAL_COMPLETE_FINAL_AGGREGATION_ENGINE_HOST_BINDER_SOURCE_ADMISSION_V1':'ROOT_ACTUAL_COMPLETE_CONTEXT_AWARE_ENGINE_HOST_BINDER_SOURCE_ADMISSION_V2',
 'ROOT_ACTUAL_COMPLETE_FINAL_AGGREGATION_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1':'ROOT_ACTUAL_COMPLETE_CONTEXT_AWARE_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V2',
 'INDEPENDENT_COMPLETE_FINAL_AGGREGATION_ENGINE_HOST_BINDER_SOURCE_REVIEW_V1':'INDEPENDENT_COMPLETE_CONTEXT_AWARE_ENGINE_HOST_BINDER_SOURCE_REVIEW_V2'}
def family(s):
    for a,b in schema_map.items():s=s.replace(a,b)
    return s
old=(B/'complete_final_MICROLIB_MACROLIB_aggregation_genuine_host.UNREADY.py').read_text();new=family(old)
new=one(new,'SOURCE_ADMISSION_SHA = None','SOURCE_ADMISSION_SHA = None\nOBSERVATION_OPERATION = None')
new=one(new,"{'qualified_source_manifest','host_template','engine_template','adapter','binder'}",
    "{'qualified_source_manifest','host_template','engine_template','adapter','binder','old_XSM_extractor','observer_module'}")
new=one(new,"    inputs.append(recheck_full_pin(support,b['source_admission_pin']))",
    "    require(b['operation']==OBSERVATION_OPERATION and OBSERVATION_OPERATION in('old_XSM_extraction','context_aggregation'),'new actual operation binding')\n    inputs.append(recheck_full_pin(support,b['source_admission_pin']))")
new=one(new,"        stage,report=observed_stage(support,runner,host/'native_run','final_micro_macro_aggregation',command,out/'ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_REPORT.json',host_pid)",
    "        report_name='ACTUAL_COMPLETE_OBSERVED_XSM_EXTRACTION_REPORT.json'if OBSERVATION_OPERATION=='old_XSM_extraction'else'ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_REPORT.json'\n        stage,report=observed_stage(support,runner,host/'native_run','final_micro_macro_aggregation',command,out/report_name,host_pid)")
start=new.index("        require(report['schema']=='ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_EVIDENCE_ONLY_V1'")
end=new.index("        require(len(runner.records)==1",start)
new=new[:start]+'''        require(report['source_binding']['sha256']==BINDING_SHA and report['original_caps']==CAPS and
            report['complete_final_construction_qualified']is False,'same operation Source binding, no unproved construction PASS')
        if OBSERVATION_OPERATION=='context_aggregation':
            require(report['schema']=='ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_EVIDENCE_ONLY_V1'and
                [row['state']for row in report['states']]==['A','B']and report['all_complete_state_scope_retained']is True,'full actual serial aggregation states')
            for row in report['states']:
                require(type(row['complete_MACROLIB_records'])is int and row['complete_MACROLIB_records']==19619 and row['original_scope']==[370,8,3,32,64,62,18,6,48],
                    'complete original19619/62/370x8/three moments/prompt/delayed scope')
                require(row['all_original_native_records_and_bytes_preserved']is True and row['all_state_databases_and_pool_closed_before_next_state']is True and
                    row['complete_final_construction_qualified']is False,'no scope reduction or construction PASS')
        else:
            require(report['schema']=='ACTUAL_COMPLETE_OBSERVED_OLD_POST_FINAL_XSM_EXTRACTION_EVIDENCE_ONLY_V1'and
                set(report['states'])=={'A','B'}and report['all_complete_state_scope_retained']is True and
                report['all_handles_closed_before_B']is True,'complete actual extraction all states/trees release beforeB')
            require(report['input_sources']==b['complete_input_pins'],'all original129 and actual observation inputs')
            for state in('A','B'):
                require(len(report['states'][state])==len(b['complete_state_snapshot_inputs'][state]),'all snapshots retained')
                for row in report['states'][state]:
                    require(row['all_original_types_counts_words_and_physical_API_orders_saved']is True and row['ASCII_used_or_invented']is False,
                        'full raw native walker, no invented ASCII or type filtering')
''' +new[end:]
new=one(new,"            saved=out/'ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_REPORT.json'",
    "            saved=out/('ACTUAL_COMPLETE_OBSERVED_XSM_EXTRACTION_REPORT.json'if OBSERVATION_OPERATION=='old_XSM_extraction'else'ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_REPORT.json')")
emit('complete_context_aware_aggregation_and_oldXSM_genuine_host.UNREADY.py',old,new)
old=(B/'bind_complete_aggregation_SOURCE_only.UNREADY.py').read_text();new=family(old)
new=new.replace('complete_final_MICROLIB_MACROLIB_aggregation_genuine_host.UNREADY.py','complete_context_aware_aggregation_and_oldXSM_genuine_host.UNREADY.py')
new=new.replace('complete_final_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py','complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py')
new=one(new,"adapter=pin(P/'saved_native_data_access_adapter.UNREADY.py'),binder=pin(Path(__file__).resolve()))",
    "adapter=pin(P/'saved_native_data_access_adapter.UNREADY.py'),binder=pin(Path(__file__).resolve()),old_XSM_extractor=pin(P/'complete_observed_old_post_final_XSM_extractor.UNREADY.py'),observer_module=pin(P/'AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90'))")
anchor="    require(request['new_aggregation_qualification_sha256']is None"
pos=new.index(anchor)
extra='''    operation=request['operation']
    require(operation in('old_XSM_extraction','context_aggregation'),'exact actual operation, no concurrent numeric stages')
    observations=request['complete_state_snapshot_inputs']
    require(type(observations)is dict and set(observations)=={'A','B'},'complete snapshot lists A/B')
    def shape_only(p):
        require(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and
            type(p['path'])is str and Path(p['path']).is_absolute()and type(p['sha256'])is str and re.fullmatch('[0-9a-f]{64}',p['sha256'])is not None and
            type(p['size_bytes'])is int and p['size_bytes']>=0 and type(p['identity'])is list and len(p['identity'])==7 and
            all(type(v)is int and v>=0 for v in p['identity'])and p['identity'][3]==1 and p['identity'][4]==p['size_bytes'],
            'actual observation pin exact shape, no Source-only material read')
        require(p in complete,'every actual context/snapshot input belongs to all complete inputs')
    for state in('A','B'):
        require(type(observations[state])is list and observations[state],'all original physical-order snapshots')
        previous=0
        for item in observations[state]:
            require(type(item)is dict and set(item)=={'event','role','root_prefix','input_pin'}and type(item['event'])is int and item['event']>=previous,
                'exact original snapshot event order, no sorting or duplicates')
            previous=item['event'];shape_only(item['input_pin'])
            require((item['role']in('oldmacro-pre-LIBMIX','oldmacro-LIBDEN','postmacro-LIBMIX')and item['root_prefix']==['MACROLIB'])or
                (item['role']=='final-complete-micro'and item['root_prefix']==[]),'full native snapshot original prefix')
    for key in('actual_observation_manifest_pin','independent_observation_Source_admission_pin'):shape_only(request[key])
    actual_context=request['actual_context_states']
    if operation=='context_aggregation':
        require(type(actual_context)is dict and set(actual_context)=={'A','B'},'actual saved full context states')
        for state in('A','B'):
            ctx=actual_context[state]
            require(type(ctx)is dict and set(ctx)=={'complete_context_pins','all_snapshot_pairs','actual_extraction_report_pin','actual_observation_manifest_pin',
                'selected_last_libmix_number','actual_extraction_coverage_contract_pin'},'full actual context explicit contract')
            require(type(ctx['complete_context_pins'])is list and ctx['complete_context_pins']and type(ctx['selected_last_libmix_number'])is int and ctx['selected_last_libmix_number']>0,
                'complete context pins and exact original last call number')
            for p in ctx['complete_context_pins']:shape_only(p)
            for key in('actual_extraction_report_pin','actual_observation_manifest_pin','actual_extraction_coverage_contract_pin'):shape_only(ctx[key])
            require(type(ctx['all_snapshot_pairs'])is list and len(ctx['all_snapshot_pairs'])==len(observations[state]),'all observed snapshot pairs')
            for pair,original in zip(ctx['all_snapshot_pairs'],observations[state]):
                require(type(pair)is dict and set(pair)=={'event','role','root_prefix','input_pin','sqlite_pin','native_pool_pin'}and
                    all(pair[key]==original[key]for key in original),'all original full snapshots, no omitted one')
                for key in('input_pin','sqlite_pin','native_pool_pin'):shape_only(pair[key])
    else:require(actual_context is None,'extraction precedes saved context; future paired values cannot be guessed')
'''
new=new[:pos]+extra+new[pos:]
new=one(new,"    binding_raw=(json.dumps(binding,indent=2,allow_nan=False)+'\\n').encode()",
    "    binding.update(operation=operation,complete_state_snapshot_inputs=observations,actual_context_states=actual_context,actual_observation_manifest_pin=request['actual_observation_manifest_pin'],independent_observation_Source_admission_pin=request['independent_observation_Source_admission_pin'])\n    binding_raw=(json.dumps(binding,indent=2,allow_nan=False)+'\\n').encode()")
new=one(new,"    engine_bound,engine_inverse=bind_globals(engine,dict(SOURCE_STATUS='READY_ROOT_BOUND_SOURCE_ONLY',SOURCE_BINDING_SHA256=binding_sha,BOUND_ADAPTER_PIN=adapter_pin))",
    "    if operation=='old_XSM_extraction':\n        engine=(P/'complete_observed_old_post_final_XSM_extractor.UNREADY.py').read_bytes()\n        engine_bound,engine_inverse=bind_globals(engine,dict(SOURCE_STATUS='READY_ROOT_BOUND_SOURCE_ONLY',ROOT_BOUND_BINDING_SHA256=binding_sha))\n    else:\n        engine_bound,engine_inverse=bind_globals(engine,dict(SOURCE_STATUS='READY_ROOT_BOUND_SOURCE_ONLY',SOURCE_BINDING_SHA256=binding_sha,BOUND_ADAPTER_PIN=adapter_pin))")
new=one(new,"SOURCE_ADMISSION_SHA=request['source_admission_pin']['sha256']))",
    "SOURCE_ADMISSION_SHA=request['source_admission_pin']['sha256'],OBSERVATION_OPERATION=operation))")
emit('bind_complete_context_aware_and_oldXSM_SOURCE_only.UNREADY.py',old,new)
old=(P/'complete_observed_old_post_final_XSM_extractor.UNREADY.py').read_text();new=old
new=new.replace('ROOT_ACTUAL_COMPLETE_OBSERVATION_XSM_EXTRACTION_BINDING_V1','ROOT_ACTUAL_COMPLETE_CONTEXT_AWARE_MICRO_MACRO_BINDING_V2')
new=one(new,"binding['new_qualification_sha256']is None","binding['new_aggregation_qualification_sha256']is None and binding['operation']=='old_XSM_extraction'")
new=one(new,"all_inputs=binding['original129_input_pins']+binding['additional_actual_observation_input_pins']","all_inputs=binding['complete_input_pins']")
new=one(new,"        actual_child_PID=os.getpid(),actual_parent_PID=os.getppid(),states=states,original_caps=CAPS,",
    "        status='ACTUAL_COMPLETE_OBSERVED_XSM_EXTRACTION_EVIDENCE_ONLY',source_binding=binding_pin,\n        actual_child_PID=os.getpid(),actual_parent_PID=os.getppid(),states=states,original_caps=CAPS,")
new=one(new,"        complete_aggregation_qualified=False,new_qualification_sha256=None,**FALSE)",
    "        complete_aggregation_qualified=False,complete_final_construction_qualified=False,new_qualification_sha256=None,**FALSE)")
emit('complete_observed_old_post_final_XSM_extractor.UNREADY.py',old,new)
(P/'COMPLETE_CONTEXT_GENUINE_HOST_BINDER_FULL_INVERSE.json').write_text(json.dumps(dict(schema='COMPLETE_CONTEXT_GENUINE_HOST_BINDER_FULL_INVERSE_V2',
    source_only=True,derivations=proof,all_original_genuine_guard_caps_MRO_cleanup_preserved=True,actual_context_Q=None,actual_host_run=None),indent=2)+'\n')
print(json.dumps(dict(source_only=True,full_derivatives=len(proof),full_inverse_hunks=sum(len(p['complete_zero_based_hunks'])for p in proof),
    complete_genuine_guard_or_material_not_executed=True)))
