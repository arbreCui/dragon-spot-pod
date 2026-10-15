"""One actual author Source seal. Executes only stdlib Source/META validation."""
from pathlib import Path
import ast,hashlib,json,stat,sys
P=Path(sys.argv[1]);S=Path(str(P)+'_seal_receipt')
assert P.is_relative_to(Path('/private/tmp')) and not S.exists() and not (P/'MANIFEST.json').exists()
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(q):
    q=Path(q);s=q.lstat()
    assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and not q.is_symlink()
    raw=q.read_bytes();assert identity(q.lstat())==identity(s) and len(raw)==s.st_size
    return dict(path=str(q),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))
def ast_dump(n):return ast.dump(n,include_attributes=False)
rp=pin(P/'AUTHOR_COMPLETE_SOURCE_ONLY_REPORT_V2_FINAL.json')
report=json.loads(Path(rp['path']).read_text())
assert report['source_only'] is True and report['all_checks_typed_true'] is True
assert type(report['check_count']) is int and report['check_count']==len(report['checks'])==129
assert len({x['check'] for x in report['checks']})==129 and all(type(x['passed']) is bool and x['passed'] is True for x in report['checks'])
assert report['blockers']==[] and report['future_environment_witness'] is None and report['future_business_pins'] is None
assert report['diagnostic_RUNTIME_controls_executed'] is False and report['whole_INPUT_build_RSS_native_or_science_qualified'] is False
assert len(report['qualified_role_Source_pins'])==7 and len(report['qualified_utility_Source_pins'])==7
for q in list(report['qualified_role_Source_pins'].values())+list(report['qualified_utility_Source_pins'].values()):assert pin(q['path'])==q
inverse=json.loads(Path(report['complete_inverse_pin']['path']).read_text())
assert pin(report['complete_inverse_pin']['path'])==report['complete_inverse_pin']
assert inverse['hunk_count']==6 and inverse['unbuffered_descriptor_reads'] is True and len(inverse['roles'])==14
for role,row in inverse['roles'].items():
    cur=(P/row['relative_path']).read_text()
    for h in reversed(row['exact_finite_transforms']):
        assert cur.count(h['new'])==1
        cur=cur.replace(h['new'],h['old'],1)
    original=Path(row['parent_V1_pin']['path']).read_text()
    assert cur.encode()==original.encode() and ast_dump(ast.parse(cur))==ast_dump(ast.parse(original))
    assert pin(row['parent_V1_pin']['path'])==row['parent_V1_pin'] and pin(P/row['relative_path'])==row['current_V2_pin']
for name,p in inverse['unchanged_V1_member_fullpins'].items():assert pin(P/name)==p
v1=Path(report['parent_V1_manifest_pin']['path']).parent
v1manifest=json.loads((v1/'MANIFEST.json').read_text())
assert pin(v1/'MANIFEST.json')==report['parent_V1_manifest_pin']
assert {name:pin(v1/name) for name in v1manifest['members']}==v1manifest['members']
prov=json.loads((P/'V2_ACTUAL_V1_FAILED_REVIEW_AND_ORIGINAL_SOURCE_FULLPIN_PROVENANCE.json').read_text())
assert prov['V1_is_failed_not_V2_admission'] is True
for key in ['actual_failed_V1_review','actual_failed_V1_review_manifest','actual_failed_V1_review_terminal']:assert pin(prov[key]['path'])==prov[key]
for name,chunk in [('ACTUAL_AUTHOR_V2_INITIAL_SOURCE_TOOL_RETURN.json','2399f6'),('ACTUAL_AUTHOR_V2_FINAL_SOURCE_TOOL_RETURN.json','35db66')]:
    t=json.loads((P/name).read_text());r=t['terminal_tool_return']
    assert t['source_only'] is True and t['closed'] is True and t['observed_terminal'] is True and t['session_repolled_after_close'] is False
    assert type(r['exit_code']) is int and r['exit_code']==0 and r['chunk_id']==chunk and t['actual_terminal_chunk']==chunk and 'session_id' not in r
    assert type(r['output']) is str and json.loads(r['output'])['candidate_or_business_executed'] is False
pycount=0
for q in sorted(P.rglob('*.py')):ast.parse(q.read_text());pycount+=1
assert pycount==53
# Create the manifest directory entry before capturing directory identities.
(P/'MANIFEST.json').write_bytes(b'')
members={str(q.relative_to(P)):pin(q) for q in sorted(P.rglob('*')) if q.is_file() and q!=P/'MANIFEST.json'}
directories={str(q.relative_to(P)):identity(q.lstat()) for q in [P]+sorted(P.rglob('*')) if q.is_dir()}
assert all(not q.is_symlink() for q in P.rglob('*'))
m=dict(schema='V25_COMPLETE_BUILD_MEMORY_OBSERVATION_UNREADY_SOURCE_PACKAGE_V2',source_only=True,status='UNREADY_V2_FINITE_SOURCE_ONLY_PENDING_NEW_INDEPENDENT_REVIEW_AND_ROOT_BINDING',member_count=len(members),members=members,directories=directories,total_member_bytes=sum(q['size_bytes'] for q in members.values()),current_author_report='AUTHOR_COMPLETE_SOURCE_ONLY_REPORT_V2_FINAL.json',current_complete_inverse='V2_FINAL_COMPLETE_THREE_ROLE_SIX_FUNCTION_WHOLE_SOURCE_INVERSES.json',complete_current_role_count=14,current_author_check_count=129,all_actual_future_business_or_environment_qualification_pins=None,candidate_or_business_executed=False,V1_FAILED_review_is_only_provenance=True)
(P/'MANIFEST.json').write_text(json.dumps(m,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
assert members=={name:pin(P/name) for name in members}
assert directories=={str(q.relative_to(P)):identity(q.lstat()) for q in [P]+sorted(P.rglob('*')) if q.is_dir()}
S.mkdir()
result=dict(schema='ACTUAL_AUTHOR_V2_COMPLETE_SOURCE_SEAL_RESULT_V1',source_only=True,manifest_pin=pin(P/'MANIFEST.json'),current_author_report_pin=rp,current_complete_inverse_pin=report['complete_inverse_pin'],member_count=len(members),complete_file_count=len(members)+1,directory_count_including_root=len(directories),all_full_Source_AST_count=pycount,all_current_role_count=14,typed_author_checks=129,independent_Source_PASS_granted=False,candidate_or_business_executed=False)
(S/'SOURCE_SEAL_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))

