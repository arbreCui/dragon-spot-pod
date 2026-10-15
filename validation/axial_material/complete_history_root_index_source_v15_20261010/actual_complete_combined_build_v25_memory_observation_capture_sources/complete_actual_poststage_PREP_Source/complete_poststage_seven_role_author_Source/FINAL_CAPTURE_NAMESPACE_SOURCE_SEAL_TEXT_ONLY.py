"""One namespace-only Source seal, no candidate/binder/API/runtime execution."""
from pathlib import Path
import ast,hashlib,json,stat,sys
P=Path(sys.argv[1]);S=Path(str(P)+'_seal_receipt')
assert P.is_relative_to(Path('/private/tmp')) and not S.exists() and not (P/'MANIFEST.json').exists()
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(q):
    q=Path(q);s=q.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and not q.is_symlink()
    raw=q.read_bytes();assert ident(q.lstat())==ident(s) and len(raw)==s.st_size
    return dict(path=str(q),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ident(s))
rp=pin(P/'AUTHOR_CAPTURE_NAMESPACE_ONLY_SOURCE_REPORT.json')
report=json.loads(Path(rp['path']).read_text())
assert report['source_only'] is True and report['all_checks_typed_true'] is True and report['blockers']==[]
assert type(report['check_count']) is int and report['check_count']==len(report['checks'])==171
assert len({c['check'] for c in report['checks']})==171 and all(type(c['passed']) is bool and c['passed'] is True for c in report['checks'])
assert report['all_actual_future_environment_business_or_Source_qualification_pins'] is None and report['whole_INPUT_BUILD_RSS_native_or_science_qualified'] is False
assert report['candidate_BINDER_API_guard_resource_helper_material_numeric_or_business_executed'] is False
assert len(report['qualified_role_Source_pins'])==len(report['qualified_utility_Source_pins'])==7
for p in list(report['qualified_role_Source_pins'].values())+list(report['qualified_utility_Source_pins'].values()):assert pin(p['path'])==p
proofp=pin(P/'COMPLETE_SOURCE_INVERSES.json');assert proofp==report['actual_consumed_complete_inverse_pin']
proof=json.loads(Path(proofp['path']).read_text())
assert len(proof['role_current_paths'])==14
inverse=json.loads(Path(report['complete_namespace_inverse_pin']['path']).read_text())
assert inverse['actual_consumer_proof_pin']==proofp and inverse['exact_namespace_hunk_count']==24
for role,rel in proof['role_current_paths'].items():
    text=(P/rel).read_text();p3text=text
    for row in reversed(inverse['roles'][role]['namespace_finite_transforms']):
        assert p3text.count(row['new'])==row['count'];p3text=p3text.replace(row['new'],row['old'])
    parent=Path(inverse['roles'][role]['actual_P3_role_pin']['path']).read_text()
    assert p3text==parent and ast.dump(ast.parse(p3text),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False)
    for row in reversed(proof['exact_finite_transforms'][role]):
        assert text.count(row['new'])==row['count'];text=text.replace(row['new'],row['old'])
    original=(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text()
    assert text==original and ast.dump(ast.parse(text),include_attributes=False)==ast.dump(ast.parse(original),include_attributes=False)
t=json.loads((P/'ACTUAL_CAPTURE_AUTHOR_SOURCE_TOOL_RETURN.json').read_text());term=t['terminal_tool_return']
assert t['source_only'] is True and t['closed'] is True and t['observed_terminal'] is True and t['session_repolled_after_close'] is False
assert type(term['exit_code']) is int and term['exit_code']==0 and term['chunk_id']=='568595' and 'session_id' not in term
a=json.loads(term['output']);assert a['current_author_report_pin']==rp and a['current_actual_consumed_complete_inverse_pin']==proofp and a['candidate_or_business_executed'] is False
prov=json.loads(Path(report['actual_parent_provenance_pin']['path']).read_text())
assert prov['P3_qualification_is_lineage_not_capture_admission'] is True and prov['new_actual_CAPTURE_env_business_peers_and_results'] is None
for key in ['P3_manifest','P3_independent_source_review','P3_independent_source_review_manifest','P3_true_review_terminal','P3_true_seal','P3_true_postseal']:assert pin(prov[key]['path'])==prov[key]
parent_root=Path(prov['P3_manifest']['path']).parent;parentm=json.loads((parent_root/'MANIFEST.json').read_text())
assert {rel:pin(parent_root/rel) for rel in parentm['members']}==parentm['members']
astcount=0
for q in P.rglob('*.py'):ast.parse(q.read_text());astcount+=1
assert astcount==57
# Add the fixed actual future path spellings to the existing CLI note. This is
# metadata documentation only, no directories/streams or future outputs are created.
nextp=P/'ROOT_CAPTURE_NEXT_STEPS.txt'
ns=report['actual_capture_namespaces']
nextp.write_text(nextp.read_text()+'\nFixed capture PREP D='+ns['prepare_D']+'\nFixed capture PREP E='+ns['prepare_E']+'\nExact future Root PREP launch spelling (only after actual binding/install/prelaunch; do not execute this Source package):\n'+'env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /Users/wen/miniforge3/envs/openmc-dev/bin/python3.12 -B '+ns['prepare_D']+'/combined_prepare_host.py > '+ns['prepare_E']+'/parent_stdout.log 2> '+ns['prepare_E']+'/parent_stderr.log\n')
(P/'MANIFEST.json').write_bytes(b'')
members={str(q.relative_to(P)):pin(q) for q in sorted(P.rglob('*')) if q.is_file() and q!=P/'MANIFEST.json'}
dirs={str(q.relative_to(P)):ident(q.lstat()) for q in [P]+sorted(P.rglob('*')) if q.is_dir()}
m=dict(schema='V25_MEMORY_OBSERVATION_CAPTURE_NAMESPACE_ONLY_UNREADY_SOURCE_PACKAGE_V1',source_only=True,status='UNREADY_CAPTURE_NAMESPACE_ONLY_PENDING_NEW_INDEPENDENT_SOURCE_REVIEW_AND_ROOT_BINDING',member_count=len(members),members=members,directories=dirs,total_member_bytes=sum(p['size_bytes'] for p in members.values()),current_author_report='AUTHOR_CAPTURE_NAMESPACE_ONLY_SOURCE_REPORT.json',actual_consumed_complete_inverse='COMPLETE_SOURCE_INVERSES.json',whole_namespace_inverses='CAPTURE_NAMESPACE_COMPLETE_14_ROLE_BYTE_AST_AND_JSON_INVERSES.json',current_Source_role_count=14,typed_author_check_count=171,only_runtime_change_two_namespace_tokens=True,namespace_hunk_count=24,all_actual_future_environment_business_or_Source_qualification_pins=None,candidate_or_business_executed=False,old_P3_source_business_results_and_qualifications_are_lineage_only=True)
(P/'MANIFEST.json').write_text(json.dumps(m,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
assert members=={rel:pin(P/rel) for rel in members}
assert dirs=={str(q.relative_to(P)):ident(q.lstat()) for q in [P]+sorted(P.rglob('*')) if q.is_dir()}
S.mkdir()
result=dict(schema='ACTUAL_CAPTURE_NAMESPACE_ONLY_SOURCE_SEAL_RESULT_V1',source_only=True,manifest_pin=pin(P/'MANIFEST.json'),current_author_report_pin=rp,actual_consumed_proof_pin=proofp,whole_namespace_inverse_pin=report['complete_namespace_inverse_pin'],Root_CLI_note_pin=pin(nextp),member_count=len(members),full_file_count=len(members)+1,directory_count_including_root=len(dirs),full_Source_AST_count=astcount,current_role_count=14,namespace_hunks=24,typed_author_checks=171,independent_Source_PASS_granted=False,candidate_or_business_executed=False)
(S/'SOURCE_SEAL_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))

