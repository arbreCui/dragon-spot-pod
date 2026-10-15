"""One actual V3 stdlib Source seal, never executes any binder/candidate/API."""
from pathlib import Path
import ast,hashlib,json,stat,sys
P=Path(sys.argv[1]);S=Path(str(P)+'_seal_receipt')
assert P.is_relative_to(Path('/private/tmp')) and not S.exists() and not (P/'MANIFEST.json').exists()
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(q):
    q=Path(q);s=q.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and not q.is_symlink()
    raw=q.read_bytes();assert identity(q.lstat())==identity(s) and len(raw)==s.st_size
    return dict(path=str(q),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))
rp=pin(P/'AUTHOR_COMPLETE_SOURCE_ONLY_REPORT_V3.json');r=json.loads(Path(rp['path']).read_text())
assert r['source_only'] is True and r['all_checks_typed_true'] is True and r['blockers']==[]
assert type(r['check_count']) is int and r['check_count']==len(r['checks'])==234 and len({x['check'] for x in r['checks']})==234
assert all(type(x['passed']) is bool and x['passed'] is True for x in r['checks'])
assert r['all_environment_and_future_business_qualification_pins'] is None
assert r['candidate_API_guard_resource_helper_BINDER_or_business_executed'] is False and r['actual_whole_BUILD_INPUT_RSS_native_or_science_qualified'] is False
for q in list(r['qualified_role_Source_pins'].values())+list(r['qualified_utility_Source_pins'].values()):assert pin(q['path'])==q
assert len(r['qualified_role_Source_pins'])==len(r['qualified_utility_Source_pins'])==7
p=pin(P/'COMPLETE_SOURCE_INVERSES.json');assert p==r['actual_consumed_proof_pin']
proof=json.loads((P/'COMPLETE_SOURCE_INVERSES.json').read_text())
assert proof['schema']=='V25_COMPLETE_BUILD_MEMORY_OBSERVATION_WHOLE_SOURCE_INVERSES_V1' and len(proof['role_current_paths'])==14
for role,rel in proof['role_current_paths'].items():
    text=(P/rel).read_text()
    for row in reversed(proof['exact_finite_transforms'][role]):
        assert text.count(row['new'])==row['count'],(role,row['label'])
        text=text.replace(row['new'],row['old'])
    original=(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text()
    assert text==original and ast.dump(ast.parse(text),include_attributes=False)==ast.dump(ast.parse(original),include_attributes=False)
cons=json.loads(Path(r['actual_consumer_static_results_pin']['path']).read_text())
assert cons['actual_consumed_proof_pin']==p and len(cons['complete_all_14_role_results'])==14
assert set(cons['actual_both_consumers'])=={'prepare_binder','build_binder'} and cons['actual_candidate_BINDER_or_READY_binding_execution'] is False
for role in cons['actual_both_consumers']:
    body=cons['actual_both_consumers'][role];assert pin(body['binder_pin']['path'])==body['binder_pin']
    assert body['actual_main_proof_relative_path']=='COMPLETE_SOURCE_INVERSES.json' and body['candidate_binder_not_executed'] is True
t=json.loads((P/'ACTUAL_AUTHOR_V3_SOURCE_TOOL_RETURN.json').read_text());term=t['terminal_tool_return']
assert t['observed_terminal'] is True and t['closed'] is True and t['session_repolled_after_close'] is False
assert type(term['exit_code']) is int and term['exit_code']==0 and term['chunk_id']=='62b6f1' and 'session_id' not in term
stdout=json.loads(term['output']);assert stdout['current_author_report_pin']==rp and stdout['actual_consumed_proof_pin']==p and stdout['candidate_or_business_executed'] is False
provenance=json.loads(Path(r['actual_V2_FAILED_source_provenance_pin']['path']).read_text())
for key in ['V2_failed_independent_report','V2_failed_independent_manifest','V2_failed_independent_terminal','V2_failed_independent_seal','V2_failed_independent_postseal']:
    assert pin(provenance[key]['path'])==provenance[key]
assert provenance['V2_Source_FAILED_not_V3_PASS'] is True
v2=Path(r['parent_V2_manifest_pin']['path']).parent;v2m=json.loads((v2/'MANIFEST.json').read_text())
assert pin(v2/'MANIFEST.json')==r['parent_V2_manifest_pin'] and {name:pin(v2/name) for name in v2m['members']}==v2m['members']
ast_count=0
for q in P.rglob('*.py'):ast.parse(q.read_text());ast_count+=1
assert ast_count==55
(P/'MANIFEST.json').write_bytes(b'')
members={str(q.relative_to(P)):pin(q) for q in sorted(P.rglob('*')) if q.is_file() and q!=P/'MANIFEST.json'}
directories={str(q.relative_to(P)):identity(q.lstat()) for q in [P]+sorted(P.rglob('*')) if q.is_dir()}
m=dict(schema='V25_COMPLETE_BUILD_MEMORY_OBSERVATION_UNREADY_SOURCE_PACKAGE_V3',source_only=True,status='UNREADY_V3_ACTUAL_CONSUMER_SOURCE_PROOF_FIXED_PENDING_NEW_INDEPENDENT_REVIEW_AND_ROOT_BINDING',member_count=len(members),members=members,directories=directories,total_member_bytes=sum(q['size_bytes'] for q in members.values()),current_author_report='AUTHOR_COMPLETE_SOURCE_ONLY_REPORT_V3.json',current_actual_consumed_complete_inverse='COMPLETE_SOURCE_INVERSES.json',current_consumer_static_results='V3_BOTH_ACTUAL_BINDER_SOURCE_CONSUMER_AND_ALL_14_WHOLE_BYTE_AST_RESULTS.json',current_JSON_inverse='V3_ACTUAL_CONSUMED_COMPLETE_PROOF_THREE_ROW_WHOLE_JSON_INVERSE.json',all_current_Source_role_count=14,current_author_check_count=234,all_runtime_Source_bytes_unchanged_from_V2=True,all_actual_future_business_or_environment_qualification_pins=None,candidate_or_business_executed=False,V1_V2_failed_reviews_are_provenance_only=True)
(P/'MANIFEST.json').write_text(json.dumps(m,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
assert members=={name:pin(P/name) for name in members}
assert directories=={str(q.relative_to(P)):identity(q.lstat()) for q in [P]+sorted(P.rglob('*')) if q.is_dir()}
S.mkdir()
result=dict(schema='ACTUAL_AUTHOR_V3_COMPLETE_SOURCE_SEAL_RESULT_V1',source_only=True,manifest_pin=pin(P/'MANIFEST.json'),current_author_report_pin=rp,actual_consumed_complete_inverse_pin=p,complete_file_count=len(members)+1,member_count=len(members),directory_count_including_root=len(directories),all_full_Source_AST_count=ast_count,all_current_role_count=14,typed_author_checks=234,independent_Source_PASS_granted=False,candidate_or_business_executed=False)
(S/'SOURCE_SEAL_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))

