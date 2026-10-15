"""Independent finite namespace-only review on the already qualified V3 base.
No memory implementation reassessment, candidate imports or process/resource APIs.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

F=Path('/private/tmp/axmat_INDEPENDENT_V25_capture_namespace_Source_f8j_l6gn')
P=Path('/private/tmp/axmat_V25_memory_observation_capture_namespace_ONLY_UNREADY_Source_20261011_13_9k38l')
M=Path('/private/tmp/axmat_V25_complete_BUILD_memory_observation_V3_actual_consumer_UNREADY_Source_nl8d0t72')
B=Path('/private/tmp/axmat_V25_memory_observation_V3_INDEPENDENT_review_2FVRNl')
PAIRS=(('v25_memory_observation','v25_memory_observation_capture'),('v25-memory-observation','v25-memory-observation-capture'))
STATUS='PASS_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_ONLY_UNREADY_NO_EXECUTION'

def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def readpin(path):
    path=Path(path);before=ident(path.lstat())
    assert path.is_absolute()and stat.S_ISREG(before[2])and before[3]==1 and before[4]<2**20 and all(not q.is_symlink()for q in(path,*path.parents))
    with path.open('rb')as stream:
        assert ident(os.fstat(stream.fileno()))==before;raw=stream.read();assert stream.read(1)==b'' and len(raw)==before[4]and ident(os.fstat(stream.fileno()))==before
    assert ident(path.lstat())==before
    return dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before),raw
def pin(path):return readpin(path)[0]
def get(path):return json.loads(readpin(path)[1])
def snapshot(root,sha):
    mf,raw=readpin(root/'MANIFEST.json');assert mf['sha256']==sha
    data=json.loads(raw);assert type(data['members'])is dict and type(data['directories'])is dict
    assert {str(p.relative_to(root))for p in root.rglob('*')if p.is_file()}==set(data['members'])|{'MANIFEST.json'}
    dirs={'.':ident(root.lstat()),**{str(p.relative_to(root)):ident(p.lstat())for p in root.rglob('*')if p.is_dir()}}
    assert dirs==data['directories']and all(not p.is_symlink()for p in root.rglob('*'))
    records={};texts={};py=0
    for rel,wanted in data['members'].items():
        assert type(rel)is str and not Path(rel).is_absolute()and '..'not in Path(rel).parts
        actual,body=readpin(root/rel);assert actual==wanted;records[rel]=actual;texts[rel]=body
        if rel.endswith('.py'):ast.parse(body,filename=str(root/rel));py+=1
    assert dirs=={'.':ident(root.lstat()),**{str(p.relative_to(root)):ident(p.lstat())for p in root.rglob('*')if p.is_dir()}}
    return mf,data,records,texts,dirs,py
def inverse(text,rows):
    counts=[]
    for row in reversed(rows):
        assert set(row)=={'label','old','new','count'}and type(row['count'])is int and row['count']>0 and type(row['old'])is str and type(row['new'])is str
        count=text.count(row['new']);assert count==row['count'];counts.append(dict(label=row['label'],actual=count,expected=row['count']))
        text=text.replace(row['new'],row['old'])
    return text,counts
def transform(text):
    for old,new in PAIRS:text=text.replace(old,new)
    return text
def closed(path,chunk):
    w=get(path);t=w['terminal_tool_return']
    assert w['source_only']is True and w['closed']is True and w['observed_terminal']is True and w['session_repolled_after_close']is False and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and t['chunk_id']==chunk==w['actual_terminal_chunk']
    return json.loads(t['output'])
def write(path,value):
    with path.open('x')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')

def main():
    checks=[];results={}
    def check(name,value):
        assert type(value)is bool and name not in {c['name']for c in checks};checks.append(dict(name=name,passed=value))
    pm,pmeta,pins,body,pdirs,py=snapshot(P,'c100e191a6d841465fe9eb36999c7cbf2c45c7be94569bdc43b66f9cfc751538')
    mm,mmeta,mpins,mbody,mdirs,mpy=snapshot(M,'ef360cd59c6e3f9851eee17bd9173382f9c526de4d9fd9ec81e4fd737c814837')
    bm,bmeta,bpins,bbody,bdirs,bpy=snapshot(B,'4c430af18d9ce09168cad49e4b70b393c139eee7496f777c213ac09f1c53f2b0')
    check('current_complete_namespace_package_97_members_98_files_9dirs_57_AST',len(pins)==97 and len(pdirs)==9 and py==57 and pmeta['source_only']is True and pmeta['candidate_or_business_executed']is False)
    check('qualified_V3_complete_base_89_members_8dirs',len(mpins)==89 and len(mdirs)==8)
    base=get(B/'REVIEW.json');check('different_author_V3_formal186_typedTrue_Source_qualification',base['schema']=='INDEPENDENT_V25_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_REVIEW_V1'and base['status']==STATUS and base['source_only']is True and base['all_checks_typed_true']is True and base['check_count']==len(base['checks'])==186 and len({r['name']for r in base['checks']})==186 and all(type(r['passed'])is bool and r['passed']is True for r in base['checks'])and base['blockers']==[] and base['qualified_complete_Source_manifest_pin']==mm)
    check('V3_formal_review_exact_real_fullpin',pin(B/'REVIEW.json')['sha256']=='6e5b323ba3a2028c2963262bfe71f33651dfcc5ba2e88bc47ecb3668f2855375')
    r=closed(B/'ACTUAL_SOURCE_REVIEW_TOOL_RETURN.json','d393d8');s=closed(Path(str(B)+'_seal_receipt')/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json','9eba3c');t=closed(Path(str(B)+'_seal_receipt')/'ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json','269334')
    check('V3_real_review_seal_postseal_closed0_coupling',r['candidate_manifest_pin']==mm and r['check_count']==r['passed_count']==186 and s['manifest_pin']==bm and s['review_pin']==pin(B/'REVIEW.json')and t['manifest_pin']==bm and t['review_pin']==pin(B/'REVIEW.json'))
    ps=closed(Path(str(P)+'_seal_receipt')/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json','0c480e');pt=closed(Path(str(P)+'_seal_receipt')/'ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json','c0df0b')
    check('current_author_real_seal_postseal_closed0_exact_source_manifest',ps['manifest_pin']==pt['manifest_pin']==pm and ps['member_count']==97 and ps['current_role_count']==14 and pt['all_source_bytes_and_identity_beforeafter_unchanged']is True)
    check('retained_complete_P3_manifest_original_bytes',body['CAPTURE_P3_PROVENANCE/ORIGINAL_P3_COMPLETE_MANIFEST.byte_exact.json']==(M/'MANIFEST.json').read_bytes())
    provenance=get(P/'CAPTURE_ACTUAL_P3_PARENT_SOURCE_AND_PEER_FULLPIN_PROVENANCE.json')
    check('declared_actual_P3_Source_and_peer_fullpins_not_future_qualification',provenance['P3_manifest']==mm and provenance['P3_independent_source_review']==pin(B/'REVIEW.json')and provenance['P3_independent_source_review_manifest']==bm and provenance['P3_qualification_is_lineage_not_capture_admission']is True and provenance['new_actual_CAPTURE_env_business_peers_and_results']is None)
    q=get(P/'COMPLETE_SOURCE_INVERSES.json');q3=get(M/'COMPLETE_SOURCE_INVERSES.json');n=get(P/'CAPTURE_NAMESPACE_COMPLETE_14_ROLE_BYTE_AST_AND_JSON_INVERSES.json')
    check('current_consumed_inverse_exact_SHA_fullpin',pin(P/'COMPLETE_SOURCE_INVERSES.json')['sha256']=='5901777ea59d2d8846750ee468a4e9233fa0aca6cd8337bad6be5296abb1bc70'and n['actual_consumer_proof_pin']==pin(P/'COMPLETE_SOURCE_INVERSES.json'))
    roles=q['role_current_paths'];brole={**base['qualified_role_Source_pins'],**base['qualified_utility_Source_pins']}
    check('actual_all14_role_paths_match_qualified_base_and_consumer_scope',len(roles)==14 and roles==q3['role_current_paths']and set(roles)==set(brole)==set(n['roles']))
    check('current_consumed_proof_other_fields_preserved',all(q[k]==q3[k]for k in q if k!='exact_finite_transforms'))
    hunks=0
    for role,rel in roles.items():
        old=mbody[rel].decode();new=body[rel].decode();rows=n['roles'][role]['namespace_finite_transforms']
        check('namespace_only_whole_source:'+role,transform(old)==new)
        restored,anchors=inverse(new,rows);check('namespace_full_byte_AST_inverse_to_qualified_V3:'+role,restored==old and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False))
        check('actual_full_role_Source_pins_coupled:'+role,brole[role]==mpins[rel]and n['roles'][role]['actual_P3_role_pin']==mpins[rel]and n['roles'][role]['current_capture_role_pin']==pins[rel])
        check('only_two_declared_namespace_pairs:'+role,all((row['old'],row['new'])in PAIRS for row in rows))
        check('current_consumed_whole_chain_is_P3_chain_plus_namespace:'+role,q['exact_finite_transforms'][role]==q3['exact_finite_transforms'][role]+rows)
        original,allanchors=inverse(new,q['exact_finite_transforms'][role]);stored=body['ORIGINAL_PARENT_SOURCE/'+role+'.full.py'].decode();op,ob=readpin(q['original_parent_fullpins'][role]['path'])
        check('complete_consumed_inverse_to_original_parent_Source_bytes_AST:'+role,original==stored==ob.decode()and op==q['original_parent_fullpins'][role]and ast.dump(ast.parse(original),include_attributes=False)==ast.dump(ast.parse(stored),include_attributes=False))
        original_nodes=[node for node in ast.parse(old).body if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))];new_nodes=[node for node in ast.parse(restored).body if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
        check('all_original_definition_occurrences_after_namespace_inverse:'+role,len(original_nodes)==len(new_nodes)and all(ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False)for a,b in zip(original_nodes,new_nodes)))
        none=lambda text:[n.targets[0].id for n in ast.parse(text).body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and isinstance(n.value,ast.Constant)and n.value.value is None]
        check('future_None_top_globals_preserved:'+role,none(old)==none(new))
        hunks+=len(rows);results[role]=dict(relative_path=rel,qualified_V3_fullpin=mpins[rel],current_namespace_fullpin=pins[rel],namespace_rows=rows,namespace_inverse_actual_anchors=anchors,actual_consumed_full_chain_anchors=allanchors,whole_byte_AST_inverse_to_qualified_V3=True,whole_consumed_inverse_to_original_parent=True,qualified_original_parent_fullpin=op,original_definition_occurrence_count=len(original_nodes))
    check('exact24_namespace_transform_rows',hunks==24==n['exact_namespace_hunk_count']==pmeta['namespace_hunk_count'])
    rel='utilities/FIXED_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT.UNREADY.json';old=json.loads(mbody[rel]);new=json.loads(body[rel]);expected=dict(old);expected['namespaces']={k:transform(v)for k,v in old['namespaces'].items()}
    check('only_ten_fixed_namespace_map_values_changed',len(new['namespaces'])==10 and expected==new and n['original_contract_namespace_map']==old['namespaces']and n['current_capture_namespace_map']==new['namespaces'])
    owners=new['complete_old_frozen_Source_owners']
    check('fixed_contract_original463_owners_and_future_facts_unchanged',old['complete_old_frozen_Source_owners']==owners and set(owners)=={'PREP','BUILD'}and sum(len(row['complete_files'])for row in owners.values())==463 and all(row['original_file_count']==len(row['complete_files'])and row['original_directory_count_including_root']==len(row['complete_directories'])for row in owners.values())and new['all_original_physical_Source_owners_retained_without_reduction']is True and new['whole_INPUT_native_or_science_qualified']is False and new['Source_install_or_prelaunch_executed']is False)
    changed={r for r in mpins if body[r]!=mbody[r]};allowed=set(roles.values())|{'COMPLETE_SOURCE_INVERSES.json',rel}
    check('all_old_P3_members_retained_changes_only14_roles_consumed_proof_and_fixed_map',set(mpins)<=set(pins)and changed<=allowed)
    for rel in sorted(set(mpins)-changed):check('unchanged_original_source_and_history_bytes:'+rel,body[rel]==mbody[rel])
    consumers={}
    for role,needed in [('prepare_binder',{'canonical','prepare_host','prepare_writer'}),('build_binder',{'build_host','build_writer'})]:
        text=body[roles[role]].decode();tree=ast.parse(text);functions={node.name:node for node in tree.body if isinstance(node,ast.FunctionDef)}
        f=functions['source_verify_original_inverse'];assert "proof['exact_finite_transforms'][role]"in ast.get_source_segment(text,f)
        loads=[node for node in ast.walk(tree)if isinstance(node,ast.Call)and isinstance(node.func,ast.Name)and node.func.id=='read'and len(node.args)==1 and isinstance(node.args[0],ast.BinOp)and isinstance(node.args[0].right,ast.Constant)and node.args[0].right.value=='COMPLETE_SOURCE_INVERSES.json']
        calls=[node for node in ast.walk(tree)if isinstance(node,ast.Call)and isinstance(node.func,ast.Name)and node.func.id=='source_verify_original_inverse'and len(node.args)==4 and isinstance(node.args[3],ast.Name)and node.args[3].id=='proof']
        check('actual_current_binder_consumes_updated_whole_proof:'+role,len(loads)==1 and bool(calls)and needed<=set(q['exact_finite_transforms']))
        consumers[role]=dict(full_Source_pin=pins[roles[role]],actual_proof_read_count=len(loads),actual_full_inverse_call_count=len(calls),affected_role_set=sorted(needed),all_whole_inverses_actual_Source_only=True)
    note=body['ROOT_CAPTURE_NEXT_STEPS.txt'].decode()
    check('new_launch_note_declares_actual_separate_external_streams_and_no_synthetic_empty',' > 'in note and ' 2> 'in note and 'parent_stdout.log'in note and 'parent_stderr.log'in note and 'Never synthesize missing stderr'in note and 'No old PREP success'in note)
    check('no_actual_new_namespace_runtime_or_environment_qualification',pmeta['all_actual_future_environment_business_or_Source_qualification_pins']is None and pmeta['old_P3_source_business_results_and_qualifications_are_lineage_only']is True)
    check('readonly_complete_candidate_base_peer_views_unchanged',pin(P/'MANIFEST.json')==pm and pin(M/'MANIFEST.json')==mm and pin(B/'MANIFEST.json')==bm and all(pin(P/rel)==wanted for rel,wanted in pins.items())and all(pin(M/rel)==wanted for rel,wanted in mpins.items())and all(pin(B/rel)==wanted for rel,wanted in bpins.items()))
    index=dict(schema='INDEPENDENT_V25_CAPTURE_NAMESPACE_ONLY_COMPLETE_SOURCE_EOF_AND_INVERSE_RESULTS_V1',source_only=True,qualification_scope='NAMESPACE_ONLY_DERIVATION_ON_DIFFERENT_AUTHOR_QUALIFIED_V3_BASE',candidate_manifest_pin=pm,candidate_members=pins,candidate_directories=pdirs,qualified_base_manifest_pin=mm,qualified_base_members=mpins,qualified_base_directories=mdirs,formal_different_author_base_review_manifest_pin=bm,formal_base_review_pin=pin(B/'REVIEW.json'),namespace_pairs=PAIRS,exact_namespace_rows=hunks,full_role_inverse_results=results,actual_current_binder_consumer_results=consumers,actual_old_members_changed=sorted(changed),memory_implementation_reassessment_performed=False,candidate_or_API_or_guard_or_numeric_executed=False)
    write(F/'COMPLETE_NAMESPACE_SOURCE_EOF_AND_INVERSE_RESULTS.json',index)
    blockers=[c['name']for c in checks if not c['passed']]
    required=get(P/'INDEPENDENT_SOURCE_PEER_REQUIRED_CONTRACT.UNREADY.json');report=dict(schema=required['required_report_schema'],status=STATUS if not blockers else'BLOCKED_NAMESPACE_SOURCE_DERIVATION',source_only=True,qualification_scope='NAMESPACE_ONLY_DERIVATION_ON_DIFFERENT_AUTHOR_QUALIFIED_V3_BASE',memory_implementation_reassessment_performed=False,all_checks_typed_true=not blockers,check_count=len(checks),checks=checks,blockers=blockers,qualified_complete_Source_manifest_pin=pm,qualified_role_Source_pins={k:pins[roles[k]]for k in required['Source_roles']},qualified_utility_Source_pins={k:pins[roles[k]]for k in required['utility_roles']},qualified_V3_baseline_Source_manifest_pin=mm,actual_different_author_V3_review_manifest_pin=bm,actual_different_author_V3_review_pin=pin(B/'REVIEW.json'),qualified_V3_baseline_check_count=186,actual_complete_namespace_Source_EOF_and_inverse_results_pin=pin(F/'COMPLETE_NAMESPACE_SOURCE_EOF_AND_INVERSE_RESULTS.json'),exact_namespace_pairs=PAIRS,exact_namespace_transform_rows=hunks,original_B_history_and_463_Source_owners_preserved=True,original_empty_external_stderr_gate_and_physics_Q_witness_caps_MRO_functions_preserved_by_whole_namespace_inverse=True,previous_missing_external_stderr_not_recovered_or_invented=True,actual_new_runtime_environment_witness=None,actual_new_PREP_execution=None,actual_new_BUILD_execution=None,actual_native_or_scientific_qualification_created=False,candidate_or_business_or_guard_or_resource_API_executed=False)
    write(F/'REVIEW.json',report)
    print(json.dumps(dict(status=report['status'],source_only=True,qualification_scope=report['qualification_scope'],check_count=len(checks),passed_count=sum(c['passed']for c in checks),blockers=blockers,review_pin=pin(F/'REVIEW.json'),qualified_complete_Source_manifest_pin=pm,candidate_or_business_executed=False),allow_nan=False))
    if blockers:raise SystemExit(1)

if __name__=='__main__':main()
