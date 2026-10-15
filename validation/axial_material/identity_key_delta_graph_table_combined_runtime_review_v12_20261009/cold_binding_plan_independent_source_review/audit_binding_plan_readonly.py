"""Independent bounded stdlib audit of binding authorities; no business imports."""
import ast
import hashlib
import json
import math
import os
import stat
from pathlib import Path

DEST=Path('/private/tmp/axmat_v12_cold_binding_plan_independent_readonly_review_20261009')
D=Path('/private/tmp/axmat_v12_cold_binding_authoritative_sources_and_callback_schema_fix_source_only_20261009')
ROOT=Path('/Users/wen/spot')
MAX=64*1024*1024
checks={}
pins={}

def check(name,test):
    if test is not True:raise ValueError(name)
    checks[name]=True

def fresh(path,expected=None,collect=True):
    path=Path(path)
    check('ordinary_absolute:'+str(path),path.is_absolute()and '..'not in path.parts)
    for ancestor in [*reversed(path.parents),path]:
        st=ancestor.lstat()
        check('no_alias:'+str(ancestor),not stat.S_ISLNK(st.st_mode))
        if ancestor!=path:check('ordinary_ancestor:'+str(ancestor),stat.S_ISDIR(st.st_mode))
    before=path.lstat()
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    identity=lambda st:tuple(getattr(st,k)for k in('st_dev','st_ino','st_mode','st_size','st_mtime_ns','st_ctime_ns','st_nlink'))
    try:
        first=os.fstat(fd)
        check('ordinary_opened_regular:'+str(path),stat.S_ISREG(first.st_mode)and identity(before)==identity(first))
        check('bounded_reader:'+str(path),not collect or first.st_size<=MAX)
        sha=hashlib.sha256();chunks=[];size=0
        while raw:=os.read(fd,1024*1024):
            sha.update(raw);size+=len(raw)
            if collect:
                check('bounded_actual_read:'+str(path),size<=MAX);chunks.append(raw)
        last=os.fstat(fd)
        after=path.lstat()
        check('stable_opened_and_pathname:'+str(path),identity(first)==identity(last)==identity(after)and size==first.st_size)
        value=sha.hexdigest()
        if expected is not None:check('exact_pin:'+str(path),value==expected)
        pins[str(path)]=dict(path=str(path),sha256=value,size_bytes=size)
        return b''.join(chunks)if collect else value
    finally:os.close(fd)

def strict(raw):
    def pairs(rows):
        out={}
        for key,val in rows:
            if key in out:raise ValueError('duplicate JSON key')
            out[key]=val
        return out
    def reject(value):raise ValueError('nonfinite JSON constant')
    body=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=reject)
    def finite(value):
        if isinstance(value,float)and not math.isfinite(value):raise ValueError('nonfinite JSON number')
        if isinstance(value,dict):
            for val in value.values():finite(val)
        elif isinstance(value,list):
            for val in value:finite(val)
    finite(body);return body

def data(path,sha=None):return strict(fresh(path,sha))
def source(path,sha=None):return fresh(path,sha).decode('utf-8')
def assignments(src):
    values={};nones=[]
    for node in ast.parse(src).body:
        if isinstance(node,ast.Assign)and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
            try:value=ast.literal_eval(node.value)
            except(ValueError,TypeError):continue
            values[node.targets[0].id]=value
            if value is None:nones.append(node.targets[0].id)
    return values,nones

plan=data(D/'BINDING_PLAN_AND_REPORT.json')
check('plan_source_only_unready',plan['status']=='PASS_SOURCE_FIX_AND_BINDING_PLAN_ONLY_UNREADY')
consumer=source(plan['consumer_unchanged']['path'],'0e47a2084acc30085784c132eb480db7e53b10963db6c4ca85b66cc76cf557fa')
factory=source(plan['new_factory']['path'],'1941375f15d61b44c17ec11e2466048f646112c6c5939ce568c9fdffc84a93a6')
binding=data(plan['binding_unchanged']['path'],'563b3f7fa28c93427b9a4613bb7b958d998e56a66a2fe85d959c3ec88440abc0')
for field in ('consumer_unchanged','binding_unchanged','new_factory'):
    check('plan_declared_exact_source:'+field,plan[field]['sha256']==pins[plan[field]['path']]['sha256'])
ca,cn=assignments(consumer);fa,fn=assignments(factory)
check('consumer_all_22_none_preserved',len(cn)==22)
check('factory_all_25_none_preserved',len(fn)==25)
check('consumer_unready',ca['STATUS']=='UNREADY')
check('factory_unready',fa['DRAFT_STATUS']=='UNREADY')
check('binding_unready',binding['draft_status']=='UNREADY_V12_GRAPH_TABLE_SOURCE_ONLY_NO_ACTUAL_NEW_SUCCESS_BINDING')
for key,nones,filename in (('consumer',cn,Path(plan['consumer_unchanged']['path']).name),('factory',fn,Path(plan['new_factory']['path']).name)):
    authority=plan['None_binding_authorities'][filename]
    check('authority_covers_all_and_only_top_level_None:'+key,set(authority)==set(nones))
    check('all_authority_prose_nonempty:'+key,all(type(x)is str and bool(x.strip())for x in authority.values()))
expected_b_authority={'actual_bounded_api_terminal_evidence','api_return','intake_proof_files','intake_namespaces','helper_sources','complete_historical_input_graph','binding_source','expected_complete_alias_count','expected_complete_descriptor_count','expected_intake_payload_count','actual_V11_component_control_counts'}
check('binding_dynamic_and_helper_authorities_complete',set(plan['binding_descriptor_authorities'])==expected_b_authority)
check('binding_no_self_SHA_cycle','binding_descriptor'not in binding and 'if \'binding_descriptor\' in value:'in factory and 'return dict(value,binding_descriptor=dict(path=str(COMPONENT_INTAKE_DESCRIPTOR),sha256=COMPONENT_INTAKE_DESCRIPTOR_SHA))'in factory)
check('binding_all_future_actual_pin_values_still_None',binding['actual_bounded_api_terminal_evidence']['sha256']is None and binding['api_return']['sha256']is None and binding['intake_proof_files']is None and binding['intake_namespaces']is None and binding['complete_historical_input_graph']['sha256']is None and binding['complete_historical_input_graph']['content_sha256']is None and binding['binding_source']['sha256']is None and all(binding[k]is None for k in ('expected_complete_alias_count','expected_complete_descriptor_count','expected_intake_payload_count','actual_V11_component_control_counts')))
check('binding_scope_false_flags',all(binding[k]is False for k in ('component_API_executed_in_cold_process','production_module_identity_overlay','science_qualification')))

formal_observation=plan['actual_existing_formal_V12_build_only_observation']
api=data(formal_observation['source_stdout']['path'],'65fc18ba1fab484b91c626a48d79a55a9bd5f21b65a391d18b9c4313e2333536')
root_receipt=data(formal_observation['Root_formal_admit']['path'],'86f4ea404d0304b22c819278723a8797b5a0cf53fce251cbae3d778a2f596459')
check('formal_actual_typed_zero',type(root_receipt['returncode'])is int and root_receipt['returncode']==0 and type(root_receipt['actual_tool_result']['exit_code'])is int and root_receipt['actual_tool_result']['exit_code']==0 and root_receipt['actual_tool_terminal_return_observed']is True and root_receipt['record_written_after_actual_terminal_return']is True)
check('formal_cannot_substitute_bounded_host_evidence',formal_observation['bounded_whole_INPUT_qualified']is False and root_receipt['bounded_whole_INPUT_intake_qualified']is False)
check('current_formal_counts_are_observed_only',len(api['descriptor_files'])==formal_observation['descriptor_count']==36804 and len(api['input_aliases'])==formal_observation['input_alias_count']==186 and ca['EXPECTED_API_DESCRIPTOR_COUNT']is None and fa['EXPECTED_API_DESCRIPTOR_COUNT']is None and binding['expected_complete_descriptor_count']is None)
check('actual_correct_nested_component_field','actual_last_cprime_trim_admission'in api and 'actual_last_cprime_trim_component_admission'not in api)
trim=api['actual_last_cprime_trim_admission']
cross=plan['actual_V11_complete68_counts_cross_evidence']
seal=data(cross['seal']['path'],'5517c1ada26e43ba55683092baf8f63f8676eeff58ee907cd03560047c7a0b19')
tr=Path(trim['build_root'])
check('nested_V11_real_seal_authority',trim['build_seal_sha256']==pins[str(tr/'seal.json')]['sha256']and seal['schema']=='AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_SEAL_V1')
controls=data(cross['sealed_controls']['path'],seal['files']['audit/controls.json'])
audit=data(cross['audit']['path'],seal['files']['audit/result.json'])
driver=data(cross['driver']['path'],seal['files']['driver_result.json'])
check('cross_plan_exact_current_sealed_pins',all(cross[k]['sha256']==pins[cross[k]['path']]['sha256']for k in ('sealed_controls','audit','driver','seal')))
counts=trim['cache_unit_control_counts']
check('all_actual_complete_30_key_counts_equal',type(counts)is dict and len(counts)==30 and cross['key_count']==30 and counts==cross['counts']==controls['counts']==audit['control_counts']==driver['control_counts'])
check('all_count_values_exact_nonnegative_int',all(type(v)is int and v>=0 for v in counts.values()))
count_sha=hashlib.sha256(json.dumps(counts,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
check('complete_sorted_counts_full_digest',count_sha==cross['sorted_complete_counts_sha256']=='9c423f03cec7f5effdd07d86a750277996d1f412011d13d2fe103e2acd4d5eaf')
check('complete_68_is_45_plus2_plus21',counts['total_declared_stages']==68 and counts['original_factor_diagonal_45_stages_retained']==45 and counts['additional_keycodec_driver_build_stages']==2 and counts['additional_keycodec_execute_stages']==21 and 45+2+21==68 and counts['inherited_last_cprime_stages_retained']==40)
stage_names=[name for name in seal['files']if name.endswith('/stages.json')]
check('one_sealed_original_V11_stage_document',len(stage_names)==1)
stage_doc=data(tr/stage_names[0],seal['files'][stage_names[0]])
component_declaration=data(tr/'declaration.json',seal['files']['declaration.json'])
negative_cases=component_declaration['control_contract']['keycodec_negative_cases']
expected_negative_labels={'controls/keycodec_negative_'+row['name']+'/execute'for row in negative_cases}
check('original_V11_twenty_expected23_negative_cases',len(negative_cases)==20 and len(expected_negative_labels)==20 and all(row['expected_returncode']==23 for row in negative_cases))
check('original_V11_68_actual_stage_outcomes_match_original_contract',len(stage_doc['stages'])==68 and all(row['status']==('FAILED'if row['label']in expected_negative_labels else'PASS')for row in stage_doc['stages'])and {row['label']for row in stage_doc['stages']if row['status']=='FAILED'}==expected_negative_labels)
check('original_V11_68_watchdogs_and67_previous',len(driver['watchdogs'])==68 and len(audit['previous_stage_watchdogs'])==67 and driver['watchdogs'][:-1]==audit['previous_stage_watchdogs'])
check('actual_V11_sealed_control_success_only',controls['status']=='PASS' and audit['classification']=='PASS_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_CONTROLS_ONLY' and audit['control_status']=='PASS' and audit['binary_status']=='PASS' and driver['classification']=='COMPLETE_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_CONTROLS_ONLY' and driver['error']is None)
check('nested_controls_authority_matches_seal',trim['compiled_unit_controls']==dict(path=str(tr/'audit/controls.json'),sha256=seal['files']['audit/controls.json']))
check('nested_V11_object_runtime_matches_seal',trim['compiled_kernel']==dict(path=str(tr/'build/SPOT1P64.o'),sha256=seal['files']['build/SPOT1P64.o'])and trim['corrected_runtime']==dict(path=str(tr/'runtime/Dragon'),sha256=seal['files']['runtime/Dragon']))
declaration_sha=fresh(tr/'declaration.json',seal['files']['declaration.json'],False)
check('actual_V11_declaration_identity',declaration_sha=='2e5c1cda328ee1be5484e756e01337d134a956ae9e6d8623215f49f75e9b42ee')
fresh(trim['source_admission']['path'],trim['source_admission']['sha256'],False)
terminal=data(trim['actual_external_terminal_evidence']['path'],'26ef721c5b76af13036e6a486468f40d7362b584485c20a8713da82a23a9f430')
check('actual_V11_terminal_typed_zero',type(terminal['returncode'])is int and terminal['returncode']==0)
check('V11_control_evidence_does_not_confer_native_science',all(trim[k]is False for k in ('native_RSS_proof_obtained','actual_full_FLU_entry_executed','production_pipeline_prepared','AAA_accuracy_qualified','ABA_admitted'))and all(audit[k]is False for k in ('actual_full_FLU_entry_executed','transport_launched','native_RSS_proof_obtained','AAA_accuracy_qualified','ABA_admitted'))and all(driver[k]is False for k in ('actual_full_FLU_entry_executed','transport_launched','AAA_accuracy_qualified','ABA_admitted')))

check('plan_intake_gate_before_binding',len(plan['binding_order'])==5 and 'host true0/closed'in plan['binding_order'][0]and 'Rootdurable9+Root10'in plan['binding_order'][0]and 'complete wholeINPUT independent admission'in plan['binding_order'][0])
check('plan_order_C_then_B_then_F','Bind C'in plan['binding_order'][1]and 'Fill B'in plan['binding_order'][2]and 'Bind F'in plan['binding_order'][3])
check('plan_final_consumer_SHA_must_include_READY_admission','after all actual bindings and READY source admission'in plan['None_binding_authorities'][Path(plan['new_factory']['path']).name]['PRIVATE_INPUT_CONSUMER_SHA'])
check('plan_future_descriptor_alias_counts_derive_durable_body','future actual durable whole return descriptor_files'in plan['binding_descriptor_authorities']['expected_complete_descriptor_count']and 'future actual durable whole return input_aliases'in plan['binding_descriptor_authorities']['expected_complete_alias_count'])
check('consumer_9_payload_plus_Root10_and_full_map_guards',"len(v['files'])!=9"in consumer and "wanted[receipt['path']]=receipt['sha256']"in consumer and "if proof!=wanted:"in consumer and "if set(e['source_payload_pins'])!=set(v['files']):"in consumer)
check('consumer_complete_live_namespace_guard',"inventory_shape(g,root,dict(files={**v['files'],Path(receipt['path']).name:receipt['sha256']},"in consumer and "for row in binding['intake_namespaces']:inventory_shape(g,row['root'],row['inventory'])"in consumer)
check('consumer_actual_host_watch_stages_full_merged_stream_guards',"host_stdout!=result"in consumer and "type(tool['exit_code'])is not int"in consumer and "len(stages)!=1"in consumer and "not 0<watch['sampled_peak_rss_mib']<512"in consumer and "e['whole_API_return']!=binding['api_return']"in consumer)
check('plan_all_future_success_remains_None',all(plan[k]is None for k in ('future_actual_bounded_INPUT','future_actual_cold_declare','future_actual_PREP','future_actual_controls','future_actual_native')))
check('plan_no_execution_science_claims',all(plan[k]is False for k in ('business_module_imported','business_API_or_CLI_executed','fixture_or_compiler_executed','project_written','scientific_qualification','AAA_accuracy_qualified','ABA_admitted')))
check('distinct_combined_and_component_runtime_binding',"actual V12 corrected_runtime SHA"in plan['None_binding_authorities'][Path(plan['new_factory']['path']).name]['COMBINED_RUNTIME_SHA']and 'genuine V11 component'in plan['None_binding_authorities'][Path(plan['new_factory']['path']).name]['TRIM_RUNTIME_SHA'])
check('source_budget_values_only_unchanged_contract',plan['own_RSS_MiB']==512 and plan['bootstrap_axial_seconds']==4200 and plan['total_cold_seconds']==43200)

report=dict(schema='AXMAT_V12_COLD_BINDING_AUTHORITIES_INDEPENDENT_READONLY_REVIEW_V1',status='PASS_SOURCE_ONLY_UNREADY_BINDING_PLAN',plan_pin=pins[str(D/'BINDING_PLAN_AND_REPORT.json')],consumer_None_count=22,factory_None_count=25,None_authority_coverage_complete=True,binding_order='actual durable independent intake admission -> final READY consumer SHA -> full binding bytes SHA -> factory bindings and final source SHA',actual_nested_field='actual_last_cprime_trim_admission',V11_complete_count_key_count=30,V11_complete_declared_stages=68,V11_full_counts_sha256=count_sha,V11_counts_equal_across_plan_nested_API_sealed_controls_audit_driver=True,V11_stage_outcomes=dict(PASS=48,expected23_negative_FAILED=20,all_original_expected_outcomes_qualified=True),actual_formal_descriptor_count_observed_only=36804,actual_formal_alias_count_observed_only=186,checks=checks,fresh_observed_files=pins,findings=[],implementation_constraints=[dict(action='Freeze the reviewed consumer READY status before its final SHA enters B, then hash B before F; changing C bytes later requires new B and F hashes.',already_supported_by_plan=True),dict(action='Derive all actual intake counts, the full graph descriptor, all proof pins and complete namespaces from the future admitted durable whole return; use current formal counts only as crosschecks.',already_supported_by_plan=True)],business_imported=False,business_API_or_CLI_executed=False,fixtures_or_compilers_executed=False,pure59_controls_repeated=False,project_files_written=False,Root_sessions_polled=False,actual_future_durable_pins_prefilled=False,native_RSS_budget_granted=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,scope_limit='Authority and small sealed metadata audit; no original mathematical controls rerun, whole graph decode, runtime or object fresh rehash.',initial_reader_errors=[dict(chunk_id='519481',exit_code=1,reason='Pure audit incorrectly required all68 statuses PASS; original contract qualifies20 expected23 keycodec negatives with FAILED status. Initial script preserved.'),dict(chunk_id='32d6c9',exit_code=1,reason='Pure exploratory reader expected returncode in driver watchdog pin summaries, not raw watchdog objects.'),dict(chunk_id='e7d754',exit_code=1,reason='Pure exploratory reader expected label in driver watchdog pin summaries, not raw watchdog objects.')])
with (DEST/'REPORT.json').open('x')as stream:json.dump(report,stream,indent=2,allow_nan=False);stream.write('\n')
print(json.dumps(dict(status=report['status'],report_path=str(DEST/'REPORT.json'),report_sha256=hashlib.sha256((DEST/'REPORT.json').read_bytes()).hexdigest(),plan_sha256=report['plan_pin']['sha256'],counts=30,V11_stages=68,consumer_None=22,factory_None=25,findings=[]),allow_nan=False))
