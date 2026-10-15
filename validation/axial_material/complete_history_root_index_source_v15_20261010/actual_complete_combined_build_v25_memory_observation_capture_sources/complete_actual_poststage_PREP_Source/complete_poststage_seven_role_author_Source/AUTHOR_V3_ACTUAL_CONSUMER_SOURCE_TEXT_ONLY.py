"""Finite actual-consumer Source-proof integration; only stdlib text/AST operations."""
from pathlib import Path
import ast,copy,hashlib,json,shutil,stat,sys
P=Path(sys.argv[1])
V2=Path('/private/tmp/axmat_V25_complete_BUILD_memory_observation_V2_finite_UNREADY_Source_919_qh5t')
V1=Path('/private/tmp/axmat_V25_complete_BUILD_memory_observation_UNREADY_Source_ynjrvdf7')
F=Path('/private/tmp/axmat_V25_memory_observation_V2_INDEPENDENT_review_NI6UOV')
FS=Path(str(F)+'_seal_receipt')
assert P.is_relative_to(Path('/private/tmp')) and P.is_dir() and P!=V2
checks=[]
def check(name,value,evidence=None):
    assert type(value) is bool
    checks.append(dict(check=name,passed=value,evidence=evidence))
    if not value:raise AssertionError(name)
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(q):
    q=Path(q);s=q.lstat()
    assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and not q.is_symlink()
    raw=q.read_bytes()
    assert identity(q.lstat())==identity(s) and len(raw)==s.st_size
    return dict(path=str(q),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))
def write(name,x):
    q=P/name;assert not q.exists();q.parent.mkdir(parents=True,exist_ok=True)
    q.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    return pin(q)
def ast_dump(n):return ast.dump(n,include_attributes=False)
def definitions(text):
    return [(n.name,ast.get_source_segment(text,n),ast_dump(n)) for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
# This function is our handwritten stdlib algorithm matching both read Source functions.
# We do not import, exec, compile or invoke any candidate function or binder.
def static_source_inverse(text,rows,role):
    observed=[]
    for row in reversed(rows):
        count=text.count(row['new'])
        if count!=row['count']:raise ValueError('own static inverse anchor '+role+'/'+row['label'])
        observed.append(dict(label=row['label'],expected_exact_occurrences=row['count'],actual_occurrences=count))
        text=text.replace(row['new'],row['old'])
    return text,observed
mp=pin(V2/'MANIFEST.json')
check('genuine_sealed_V2_manifest_SHA',mp['sha256']=='69e22423b0211ae1ae5a1fc5cc20e41843cd41d96838b053c164696d492301b4')
m=json.loads((V2/'MANIFEST.json').read_text())
before={rel:pin(V2/rel) for rel in m['members']}
check('genuine_V2_complete_79_members_full_EOF_SHA_7ID',len(before)==79 and before==m['members'])
dirs={str(q.relative_to(V2)):identity(q.lstat()) for q in [V2]+sorted(V2.rglob('*')) if q.is_dir()}
check('genuine_V2_all_complete_directories_exact',dirs==m['directories'])
delivery=json.loads((FS/'DELIVERY_INDEX.json').read_text())
check('genuine_V2_failed_peer_delivery_scope',delivery['Source_review_actual_exit_int']==1 and delivery['Source_verdict_PASS'] is False and delivery['check_count']==161 and delivery['passed_count']==156 and delivery['failed_count']==5)
fp=pin(F/'REVIEW.json');fm=pin(F/'MANIFEST.json')
check('genuine_V2_failed_peer_report_and_manifest_fullpins',fp==delivery['review_pin'] and fm==delivery['manifest_pin'] and delivery['candidate_manifest_pin']==mp)
failed=json.loads((F/'REVIEW.json').read_text())
check('V2_independent_FAIL_not_used_as_admission',failed['all_checks_typed_true'] is False and len(failed['blockers'])==1 and failed['blockers'][0]['id']=='SOURCE_V2_FINAL_INVERSE_NOT_CONSUMED_BY_ACTUAL_BINDERS')
ft=pin(F/'ACTUAL_SOURCE_REVIEW_TOOL_RETURN.json');tool=json.loads(Path(ft['path']).read_text());term=tool['terminal_tool_return']
check('genuine_V2_cce11c_CLOSED_typed1',tool['closed'] is True and tool['observed_terminal'] is True and tool['session_repolled_after_close'] is False and tool['actual_terminal_chunk']=='cce11c' and term['chunk_id']=='cce11c' and type(term['exit_code']) is int and term['exit_code']==1 and 'session_id' not in term)
sealpin=pin(FS/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json');postpin=pin(FS/'ACTUAL_POSTSEAL_TOOL_RETURN.json')
for label,q,chunk in [('seal',sealpin,'8ec3cd'),('postseal',postpin,'6dc399')]:
    t=json.loads(Path(q['path']).read_text());r=t['terminal_tool_return']
    check('V2_failed_peer_actual_'+label+'_closed0_only_failure_integrity',t['closed'] is True and t['observed_terminal'] is True and t['session_repolled_after_close'] is False and type(r['exit_code']) is int and r['exit_code']==0 and r['chunk_id']==chunk and 'session_id' not in r and t['Source_verdict_PASS'] is False)
for rel in before:
    q=P/rel;assert not q.exists();q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(V2/rel,q)
q=P/'V3_SOURCE_PROVENANCE/ORIGINAL_V2_COMPLETE_MANIFEST.byte_exact.json';q.parent.mkdir();q.write_bytes((V2/'MANIFEST.json').read_bytes())
old_raw=(V2/'COMPLETE_SOURCE_INVERSES.json').read_bytes()
old=json.loads(old_raw);proof=copy.deepcopy(old)
check('actual_consumer_fixed_proof_schema_and_structure',proof['schema']=='V25_COMPLETE_BUILD_MEMORY_OBSERVATION_WHOLE_SOURCE_INVERSES_V1' and proof['source_only'] is True and set(proof['role_current_paths'])==set(proof['exact_finite_transforms'])==set(proof['definitions_by_role']) and len(proof['role_current_paths'])==14)
changes=[]
for role in ('prepare_host','build_host','build_writer'):
    rel=proof['role_current_paths'][role]
    old_text=(V1/rel).read_text();current=(P/rel).read_text()
    old_funcs={n.name:ast.get_source_segment(old_text,n)+'\n' for n in ast.parse(old_text).body if isinstance(n,ast.FunctionDef) and n.name in ('memory_diagnostic_pin','memory_diagnostic_rows')}
    new_funcs={n.name:ast.get_source_segment(current,n)+'\n' for n in ast.parse(current).body if isinstance(n,ast.FunctionDef) and n.name in ('memory_diagnostic_pin','memory_diagnostic_rows')}
    rows=[row for row in proof['exact_finite_transforms'][role] if row['label']=='bounded_saved_diagnostic_reader']
    check(role+'_one_actual_consumed_reader_transform',len(rows)==1 and rows[0]['count']==1)
    row=rows[0];old_new=row['new']
    for name in ('memory_diagnostic_pin','memory_diagnostic_rows'):
        check(role+'_'+name+'_original_fullblock_once_in_actual_row_new',row['new'].count(old_funcs[name])==1)
        row['new']=row['new'].replace(old_funcs[name],new_funcs[name],1)
    changes.append(dict(role=role,label=row['label'],old_new=old_new,current_new=row['new'],count=row['count'],changed_only_two_complete_diagnostic_functions=True))
    check(role+'_old_actual_consumer_known_failed_anchor_still_zero',current.count(old_new)==0)
check('only_three_new_fields_changed_proof_structure_metadata',all(proof[k]==old[k] for k in proof if k!='exact_finite_transforms'))
for role in proof['exact_finite_transforms']:
    for a,b in zip(old['exact_finite_transforms'][role],proof['exact_finite_transforms'][role]):
        check(role+'_'+a['label']+'_only_target_new_payload_may_change',a==b if role not in ('prepare_host','build_host','build_writer') or a['label']!='bounded_saved_diagnostic_reader' else all(a[k]==b[k] for k in a if k!='new'))
# Serialize in precisely the original format; reverse the three JSON field changes to literal original bytes.
old_serial=(json.dumps(old,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
check('original_consumed_JSON_byte_serialization_exact',old_serial==old_raw)
new_raw=(json.dumps(proof,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
restored_proof=copy.deepcopy(proof)
for row in changes:
    selected=[x for x in restored_proof['exact_finite_transforms'][row['role']] if x['label']==row['label']][0]
    selected['new']=row['old_new']
check('whole_JSON_three_row_inverse_to_original_V2_bytes',(json.dumps(restored_proof,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()==old_raw)
(P/'COMPLETE_SOURCE_INVERSES.json').write_bytes(new_raw)
observed={}
roles=proof['role_current_paths']
for role,rel in roles.items():
    check(role+'_current_path_exact_relative_file',type(rel) is str and not Path(rel).is_absolute() and '..' not in Path(rel).parts and (P/rel).is_file())
    current=(P/rel).read_text()
    original=(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text()
    restored,anchors=static_source_inverse(current,proof['exact_finite_transforms'][role],role)
    check(role+'_actual_consumed_rows_whole_byte_inverse_to_originalParent',restored.encode()==original.encode())
    check(role+'_actual_consumed_rows_whole_AST_inverse_to_originalParent',ast_dump(ast.parse(restored))==ast_dump(ast.parse(original)))
    original_defs=definitions(original);current_defs=definitions(current)
    old_names={r[0] for r in original_defs};filtered=[r for r in current_defs if r[0] in old_names]
    recomputed=dict(original_count=len(original_defs),new_count=len(current_defs),unchanged_original_definition_occurrences=[dict(name=a[0],occurrence=i,whole_bytes_and_AST_unchanged=(a==b)) for i,(a,b) in enumerate(zip(original_defs,filtered))])
    check(role+'_all_definitions_current_metadata_exact',recomputed==proof['definitions_by_role'][role] and len(filtered)==len(original_defs))
    check(role+'_all_runtime_Source_bytes_equal_sealed_V2',pin(P/rel)['sha256']==before[rel]['sha256'] and pin(P/rel)['size_bytes']==before[rel]['size_bytes'])
    observed[role]=dict(current_path=rel,current_role_pin=pin(P/rel),complete_literal_parent_pin=pin(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')),actual_parent_lineage_pin=proof['original_parent_fullpins'][role],actual_ordered_reverse_anchors=anchors,whole_byte_inverse=True,whole_AST_inverse=True,current_definition_metadata_verified=True)
consumers={}
for role,rel,template_roles in [('prepare_binder',roles['prepare_binder'],['canonical','prepare_host','prepare_writer']),('build_binder',roles['build_binder'],['build_host','build_writer'])]:
    text=(P/rel).read_text();tree=ast.parse(text);defs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
    main=ast.get_source_segment(text,defs['main'])
    check(role+'_actual_main_consumes_same_fixed_proof',main.count("proof=read(HERE/'COMPLETE_SOURCE_INVERSES.json')")==1)
    inv=ast.get_source_segment(text,defs['source_inverse'])
    expected=ast.parse("""def source_inverse(text,rows):
    for row in reversed(rows):
        if text.count(row['new'])!=row['count']:raise ValueError('inverse anchor '+row['label'])
        text=text.replace(row['new'],row['old'])
    return text
""").body[0]
    check(role+'_handwritten_text_algorithm_matches_actual_Source_AST',ast_dump(defs['source_inverse'])==ast_dump(expected))
    verify=ast.get_source_segment(text,defs['source_verify_original_inverse'])
    check(role+'_actual_READY_then_UNREADY_to_originalParent_composition', "source_inverse(source_inverse(text,ready_rows),proof['exact_finite_transforms'][role])" in verify and "(HERE/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text()" in verify and 'original!=parent or ast.dump(ast.parse(original),include_attributes=False)!=ast.dump(ast.parse(parent),include_attributes=False)' in verify)
    check(role+'_actual_no_function_changes_and_verify_before_output_creation',main.index('source_verify_original_inverse(role,text,')<main.index('output.mkdir()') and 'source_definitions(text)' in main)
    replace=ast.get_source_segment(text,defs['source_replace'])
    future=ast.get_source_segment(text,defs['source_future_bind'])
    check(role+'_READY_global_edits_record_full_counted_reverse_rows',"rows.append(dict(label=label,old=old,new=new,count=count));return text.replace(old,new)" in replace and "text=source_replace(text,rows,name+'=None'" in future)
    # We do not fill any value or produce bound Source. The empty READY layer is exactly
    # the still-UNREADY template. Reversible recorded literal edits are separately proven in Source AST.
    template_results={}
    for tr in template_roles:
        unready=(P/roles[tr]).read_text()
        unchanged,empty_anchors=static_source_inverse(unready,[],tr)
        restored,anchors=static_source_inverse(unchanged,proof['exact_finite_transforms'][tr],tr)
        parent=(P/'ORIGINAL_PARENT_SOURCE'/(tr+'.full.py')).read_text()
        check(role+'_'+tr+'_actual_two_layer_template_consumer_byte_AST',restored==parent and ast_dump(ast.parse(restored))==ast_dump(ast.parse(parent)))
        template_results[tr]=dict(actual_template=pin(P/roles[tr]),actual_consumed_proof=pin(P/'COMPLETE_SOURCE_INVERSES.json'),READY_rows_not_populated_future_values_still_None=True,READY_layer_empty_for_current_UNREADY_text=True,UNREADY_layer_full_anchors=anchors,complete_parent_byte_AST=True)
    consumers[role]=dict(binder_pin=pin(P/rel),actual_main_proof_relative_path='COMPLETE_SOURCE_INVERSES.json',actual_source_inverse_full_text=inv,actual_source_verify_original_inverse_full_text=verify,actual_source_replace_full_text=replace,actual_source_future_bind_full_text=future,template_roles=template_roles,template_results=template_results,candidate_binder_not_executed=True,actual_READY_binding_not_performed=True)
unmodified={rel:pin(P/rel) for rel in before if rel!='COMPLETE_SOURCE_INVERSES.json'}
check('all_other_78_V2_members_literal_bytes_preserved',len(unmodified)==78 and all(q['sha256']==before[rel]['sha256'] and q['size_bytes']==before[rel]['size_bytes'] for rel,q in unmodified.items()))
check('all_14_role_bytes_unchanged_and_all_None_globals_still_unknown',all(pin(P/rel)['sha256']==before[rel]['sha256'] for rel in roles.values()))
py_count=0
for q in P.rglob('*.py'):ast.parse(q.read_text());py_count+=1
check('all_current_54_full_Source_texts_AST_only_parsed',py_count==54)
check('V2_all_original_members_manifest_and_directories_unchanged',before=={rel:pin(V2/rel) for rel in before} and pin(V2/'MANIFEST.json')==mp and dirs=={str(q.relative_to(V2)):identity(q.lstat()) for q in [V2]+sorted(V2.rglob('*')) if q.is_dir()})
check('genuine_V2_FAIL_sourcepeer_fullpins_beforeafter_unchanged',pin(F/'REVIEW.json')==fp and pin(F/'MANIFEST.json')==fm and pin(F/'ACTUAL_SOURCE_REVIEW_TOOL_RETURN.json')==ft and pin(FS/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json')==sealpin and pin(FS/'ACTUAL_POSTSEAL_TOOL_RETURN.json')==postpin)
lineage=write('V3_ACTUAL_V2_FAILED_SOURCE_REVIEW_AND_PARENT_FULLPIN_PROVENANCE.json',dict(schema='V25_MEMORY_OBSERVATION_V3_ACTUAL_V2_FAILED_SOURCE_PROVENANCE_V1',source_only=True,parent_V2_manifest=mp,parent_V2_current_author_report=pin(V2/'AUTHOR_COMPLETE_SOURCE_ONLY_REPORT_V2_FINAL.json'),V2_failed_independent_report=fp,V2_failed_independent_manifest=fm,V2_failed_independent_terminal=ft,V2_failed_independent_seal=sealpin,V2_failed_independent_postseal=postpin,V2_delivery_index=pin(FS/'DELIVERY_INDEX.json'),V2_actual_failure_terminal_wrapper=tool,V2_actual_failed_check_count=161,V2_actual_true_check_count=156,V2_actual_false_check_count=5,V2_Source_FAILED_not_V3_PASS=True,V2_blockers=failed['blockers'],all_parent_V2_member_fullpins=before,old_actual_consumed_proof=before['COMPLETE_SOURCE_INVERSES.json']))
json_inverse=write('V3_ACTUAL_CONSUMED_COMPLETE_PROOF_THREE_ROW_WHOLE_JSON_INVERSE.json',dict(schema='V25_MEMORY_OBSERVATION_V3_ACTUAL_CONSUMED_PROOF_THREE_ROW_WHOLE_JSON_INVERSE_V1',source_only=True,old_full_JSON_pin=before['COMPLETE_SOURCE_INVERSES.json'],current_full_JSON_pin=pin(P/'COMPLETE_SOURCE_INVERSES.json'),exact_changes=changes,other_JSON_fields_all_unchanged=True,full_original_V2_JSON_bytes_recovered=True,actual_consumer_filename='COMPLETE_SOURCE_INVERSES.json',schema_unchanged=proof['schema']))
consumer=write('V3_BOTH_ACTUAL_BINDER_SOURCE_CONSUMER_AND_ALL_14_WHOLE_BYTE_AST_RESULTS.json',dict(schema='V25_MEMORY_OBSERVATION_V3_ACTUAL_BOTH_BINDER_SOURCE_CONSUMER_STATIC_RESULTS_V1',source_only=True,actual_consumed_proof_pin=pin(P/'COMPLETE_SOURCE_INVERSES.json'),complete_all_14_role_results=observed,actual_both_consumers=consumers,actual_candidate_BINDER_or_READY_binding_execution=False,all_future_values_not_populated=True))
src_roles=['canonical','prepare_binder','build_binder','prepare_host','prepare_writer','build_host','build_writer']
report=dict(schema='AUTHOR_V25_COMPLETE_BUILD_MEMORY_OBSERVATION_V3_ACTUAL_CONSUMER_SOURCE_ONLY_REPORT_V1',status='UNREADY_V3_SOURCE_ONLY_AUTHOR_CHECKS_PENDING_NEW_INDEPENDENT_REVIEW_AND_ROOT_BINDING',source_only=True,check_count=len(checks),checks=checks,all_checks_typed_true=all(c['passed'] is True for c in checks),blockers=[],qualified_role_Source_pins={r:pin(P/roles[r]) for r in src_roles},qualified_utility_Source_pins={r:pin(P/roles[r]) for r in roles if r not in src_roles},actual_consumed_proof_pin=pin(P/'COMPLETE_SOURCE_INVERSES.json'),actual_consumer_static_results_pin=consumer,full_JSON_three_row_inverse_pin=json_inverse,actual_V2_FAILED_source_provenance_pin=lineage,parent_V2_manifest_pin=mp,current_runtime_Source_role_count=14,all_runtime_Source_bytes_unchanged_from_V2=True,only_original_member_changed='COMPLETE_SOURCE_INVERSES.json',only_three_rows_new_payload_changed=True,unchanged_parent_member_count=78,all_environment_and_future_business_qualification_pins=None,candidate_API_guard_resource_helper_BINDER_or_business_executed=False,project_ART_parent_or_failed_review_written=False,actual_whole_BUILD_INPUT_RSS_native_or_science_qualified=False,limitations=['Author Source checks only; new independent Source admission is required.','V1 and V2 actual independent Source FAIL remain FAIL provenance.','All 14 runtime Source byte streams are exactly current V2; three new complete helper blocks are now wired in the actual consumed proof JSON.','Both binder Source main/path/schema/transforms and exact source_inverse algorithm are checked by handwritten stdlib text/AST simulation, not candidate execution.','No actual READY pins were supplied and no bound Source was generated; Root must later run true Source binding with actual environment/Q and business proof inputs.'])
rp=write('AUTHOR_COMPLETE_SOURCE_ONLY_REPORT_V3.json',report)
(P/'ROOT_V3_NEXT_STEPS.txt').write_text('UNREADY V3 finite actual-consumer integration, Source only. Only COMPLETE_SOURCE_INVERSES.json changes relative to V2 original members: three bounded_saved_diagnostic_reader rows new payloads include the current whole helper block. All 14 role Source bytes and all 78 other V2 members are byte exact. Both actual binders continue to consume that same filename/schema/count/transform structure and restore original Parent Source bytes/AST. V2 failed Source peer is preserved only by exact fullpins and real cce11c integer1 wrapper; no PASS is borrowed.\n1. Obtain new independent full14 Source review coupled to current V3 MANIFEST, 7 role and 7 utility actualfullpins, actual consumed proof and complete algorithm results.\n2. Follow original ROOT_NEXT_STEPS.txt with current V3 package and new peer. Root alone supplies true c6 Q/helper3b/new Q proofs and actual resource environment witness via unchanged PREP binder CLI. All future environmental/business qualification pins are None here.\n3. Root actual Source binding, bound independent review, install/freeze/full PREP, saved PREP review, full BUILD binding/independent review/install/prelaunch/one genuine full BUILD remain required under unchanged original caps. Current Source proves no RSS, physical or scientific qualification; no actual binding or candidate/runtime execution occurred here.\n')
print(json.dumps(dict(source_only=True,check_count=len(checks),all_checks_typed_true=True,current_author_report_pin=rp,actual_consumed_proof_pin=pin(P/'COMPLETE_SOURCE_INVERSES.json'),actual_consumer_static_results_pin=consumer,complete_JSON_inverse_pin=json_inverse,actual_V2_FAILED_provenance=lineage,all_runtime_Source_14_bytes_unchanged=True,candidate_or_business_executed=False),ensure_ascii=False))

