"""Seal this completed independent Source review; never imports candidate."""
import hashlib
import json
from pathlib import Path
import stat

P=Path(__file__).parent


def require(v,m):
    if type(v) is not bool or not v:raise ValueError(m)


def seven(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def pin(p):
    b=p.lstat();require(stat.S_ISREG(b.st_mode) and b.st_nlink==1 and not p.is_symlink(),'regular singleton Source member')
    raw=p.read_bytes();a=p.lstat();require(seven(b)==seven(a) and len(raw)==b.st_size,'finite completeEOF7ID stable')
    return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=seven(a))


def write(p,v):
    with p.open('x') as f:json.dump(v,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')


r=json.loads((P/'REVIEW.json').read_bytes())
require(r['schema']=='INDEPENDENT_COMPLETE_HELPER_INACTIVE_AUDIT_SNAPSHOT_SOURCE_REVIEW_V1'
    and r['status']=='SOURCE_ONLY_PASS_UNREADY_REQUIRES_NEW_FULL_QUALIFICATION'
    and r['source_only'] is True and r['all_checks_passed'] is True and r['blockers']==[], 'strict Source-only report')
require(type(r['check_count']) is int and r['check_count']==479==len(r['checks'])
    and all(c['passed'] is True for c in r['checks']),'all complete typed checks')
require(r['candidate_or_helper_executed'] is False and r['guard_or_business_executed'] is False
    and r['numerical_or_ART_payload_read'] is False and r['canonical_private_call_wired'] is False
    and r['runtime_qualification_created'] is False and r['new_Q'] is None
    and r['future_RSS_or_build_pass_predicted'] is None,'no unperformed credit')
v=json.loads((P/'actual_independent_SOURCE_review_tool_terminal_return.json').read_bytes());t=v['terminal_tool_return']
require(v['closed'] is True and v['observed_terminal'] is True and v['source_only'] is True
    and v['session_repolled_after_close'] is False and type(t['exit_code']) is int and t['exit_code']==0
    and 'session_id' not in t and v['actual_terminal_chunk']==t['chunk_id'],'actual independent tool typed0 CLOSED')
observed=json.loads(t['output'])
require(observed['review_pin']==pin(P/'REVIEW.json'),'review unchanged after genuine tool')
for expected in json.loads((P/'FULL_MEMBER_AND_TOOL_PROVENANCE.json').read_bytes())['complete_original_member_pins']:
    require(pin(Path(expected['path']))==expected,'all21 original Source members remain fixed')
require(pin(Path(r['qualified_source_manifest']['path']))==r['qualified_source_manifest'],'author source manifest remains fixed')
members=[];dirs=[]
for p in sorted(P.rglob('*')):
    s=p.lstat();require(not stat.S_ISLNK(s.st_mode),'no peer namespace alias')
    if stat.S_ISDIR(s.st_mode):dirs.append(dict(relative_path=str(p.relative_to(P)),identity=seven(s)))
    else:members.append(dict(relative_path=str(p.relative_to(P)),**pin(p)))
m=dict(schema='SEALED_INDEPENDENT_COMPLETE_INACTIVE_AUDIT_SNAPSHOT_SOURCE_REVIEW_V1',
    status=r['status'],source_only=True,root=str(P),member_count=len(members),members=members,
    total_member_bytes=sum(x['size_bytes'] for x in members),directories=dirs,
    review_pin=pin(P/'REVIEW.json'),author_manifest_pin=r['qualified_source_manifest'],candidate_pin=r['candidate'],
    actual_review_tool_receipt_pin=pin(P/'actual_independent_SOURCE_review_tool_terminal_return.json'),
    candidate_executed=False,new_Q=None)
write(P/'MANIFEST.json',m)
for row in members:require(pin(Path(row['path']))=={k:row[k] for k in ('path','sha256','size_bytes','identity')},'all peer full Source stable after manifest')
sibling=Path(str(P)+'_seal_receipt');sibling.mkdir()
seal=dict(schema='ACTUAL_INDEPENDENT_COMPLETE_INACTIVE_AUDIT_SOURCE_SEAL_V1',
    source_only=True,status=r['status'],manifest_pin=pin(P/'MANIFEST.json'),review_pin=m['review_pin'],
    original_author_manifest_pin=r['qualified_source_manifest'],candidate_pin=r['candidate'],
    member_count=len(members),root_directory_identity_after_manifest=seven(P.lstat()),
    fullEOF_SHA7ID_all_members_fixed=True,source_checks=479,candidate_executed=False,new_Q=None)
write(sibling/'SOURCE_SEAL.json',seal)
print(json.dumps(dict(status=r['status'],source_only=True,manifest_pin=seal['manifest_pin'],review_pin=m['review_pin'],
    member_count=len(members),total_member_bytes=m['total_member_bytes'],seal_pin=pin(sibling/'SOURCE_SEAL.json'),
    actual_review_receipt_pin=m['actual_review_tool_receipt_pin'],candidate_executed=False,new_Q=None),ensure_ascii=False,allow_nan=False))
