"""Finite SOURCE-only full EOF/AST/inverse checks and package manifest."""
from pathlib import Path
import ast, hashlib, json

P=Path(__file__).parent
def identity(path):
    s=path.lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def fullpin(path):
    before=identity(path);raw=path.read_bytes();after=identity(path)
    assert before==after and len(raw)==before[4]
    return {'path':str(path),'sha256':hashlib.sha256(raw).hexdigest(),'size_bytes':len(raw),'identity':before}
assert not (P/'MANIFEST.json').exists()
members=sorted([f for f in P.rglob('*') if f.is_file()],key=lambda f:str(f.relative_to(P)))
assert all(not f.is_symlink() for f in P.rglob('*'))
pins={str(f):fullpin(f) for f in members}
dirs={str(f):identity(f)for f in P.rglob('*')if f.is_dir()}
inverse=json.loads((P/'EXACT_COMPLETE_SOURCE_INVERSE.json').read_bytes())
candidate=Path(inverse['candidate_pin']['path'])
assert pins[str(candidate)]==inverse['candidate_pin']
src=candidate.read_text();restored=src
for h in reversed(inverse['hunks']):
    assert restored.count(h['new_utf8'])==1
    restored=restored.replace(h['new_utf8'],h['old_utf8'],1)
parent=(P/'ORIGINAL_cf0_COMPLETE_HELPER.py').read_bytes()
assert restored.encode()==parent
assert hashlib.sha256(parent).hexdigest()=='cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c'
assert ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False)
canon=(P/'ORIGINAL_09e_COMPLETE_CANONICAL.py').read_bytes()
assert hashlib.sha256(canon).hexdigest()=='09e53974005082a14d9675f69258549609a991f86ec231ab6b15edfe20dd265e'
for actual_pin in json.loads((P/'SOURCE_SELF_REVIEW.json').read_bytes())['parent_Source_pins_before'].values():
    assert fullpin(Path(actual_pin['path']))==actual_pin
review=json.loads((P/'SOURCE_SELF_REVIEW.json').read_bytes())
assert review['all_checks_typed_true'] is True and review['blockers']==[]
assert review['check_count']==126==len(review['checks'])
assert all(type(c['pass']) is bool and c['pass'] is True for c in review['checks'])
assert len({c['name'] for c in review['checks']})==len(review['checks'])
assert review['new_actual_qualification'] is None and review['six_future_business_pins']==[None]*6
assert all(v is None for v in inverse['all_new_helper_qualification_pins'].values())
py_count=0
for f in members:
    if f.suffix=='.py':ast.parse(f.read_bytes());py_count+=1
old=P/'ORIGINAL_SEALED_LAST_USE_PROPOSAL'
om=json.loads((old/'MANIFEST.json').read_bytes())
for e in om['members']:
    local=old/e['relative_path'];raw=local.read_bytes()
    assert len(raw)==e['size_bytes'] and hashlib.sha256(raw).hexdigest()==e['sha256']
for filename in ('ACTUAL_SOURCE_CANDIDATE_GENERATION_TOOL_RETURN.json',
                 'ACTUAL_ORIGINAL_SOURCE_CONTEXT_READ_TOOL_RETURN.json',
                 'ACTUAL_SEALED_PARENT_SOURCE_MANIFEST_READ_TOOL_RETURN.json'):
    v=json.loads((P/filename).read_bytes());t=v['terminal_tool_return']
    assert v['source_only'] is True and v['closed'] is True and v['actual_tool_terminal_return_observed'] is True
    assert type(t['exit_code']) is int and t['exit_code']==0 and 'session_id' not in t
    assert v['candidate_or_helper_executed'] is False and v['guard_or_business_executed'] is False
assert pins=={str(f):fullpin(f) for f in members}
assert dirs=={str(f):identity(f)for f in P.rglob('*')if f.is_dir()}
manifest={'schema':'SEALED_COMPLETE_HELPER_INACTIVE_AUDIT_SOURCE_CANDIDATE_V1',
          'status':'UNREADY_COMPLETE_SOURCE_ONLY_NO_HELPER_OR_BUSINESS_EXECUTION','source_only':True,
          'members':[dict(relative_path=str(f.relative_to(P)),**pins[str(f)])for f in members],
          'member_count':len(members),'total_member_bytes':sum(v['size_bytes']for v in pins.values()),
          'subdirectories':[{'path':path,'identity':sig}for path,sig in dirs.items()],
          'candidate_pin':pins[str(candidate)],'inverse_pin':pins[str(P/'EXACT_COMPLETE_SOURCE_INVERSE.json')],
          'SOURCE_self_review_pin':pins[str(P/'SOURCE_SELF_REVIEW.json')],
          'SOURCE_check_count':126,'parsed_python_file_count':py_count,
          'parent_helper_sha256':'cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c',
          'all_new_actual_qualification_pins':inverse['all_new_helper_qualification_pins'],
          'six_future_business_pins':[None]*6,'actual_candidate_helper_guard_business_executed':False,
          'observed_peak_line_or_RSS_PASS_prediction':None}
(P/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
assert pins=={str(f):fullpin(f)for f in members}
assert dirs=={str(f):identity(f)for f in P.rglob('*')if f.is_dir()}
print(json.dumps({'source_only':True,'closed_SOURCE_scope':True,'manifest':fullpin(P/'MANIFEST.json'),
                  'package_directory_identity_after_manifest':identity(P),'member_count':len(members),
                  'total_member_bytes':manifest['total_member_bytes'],'SOURCE_check_count':126,
                  'parsed_python_file_count':py_count,'all_full_EOF_SHA7ID_before_after_unchanged':True,
                  'candidate':pins[str(candidate)],'new_qualification':None},separators=(',',':')))
