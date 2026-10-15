"""Once-seal and postseal stdlib Source receipts; no candidate execution."""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

P=Path(__file__).parent
SIBLING=Path(str(P)+'_seal_receipt')

def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def require(value,message):
    if type(value)is not bool or not value:raise ValueError(message)
def pin(path):
    p=Path(path);s=p.lstat();require(stat.S_ISREG(s.st_mode)and s.st_nlink==1,'regular Source single link')
    h=hashlib.sha256();size=0
    with p.open('rb')as f:
        require(identity(os.fstat(f.fileno()))==identity(s),'Source before identity')
        while True:
            raw=f.read(2**20)
            if not raw:break
            h.update(raw);size+=len(raw)
        require(identity(os.fstat(f.fileno()))==identity(s),'Source full EOF unchanged')
    require(identity(p.lstat())==identity(s)and size==s.st_size,'Source path unchanged')
    return dict(path=str(p),sha256=h.hexdigest(),size_bytes=size,identity=identity(s))
def inventory():
    members=[];dirs=[]
    for p in [P,*sorted(P.rglob('*'))]:
        s=p.lstat();rel='.'if p==P else str(p.relative_to(P));require(not stat.S_ISLNK(s.st_mode),'no Source aliases')
        if stat.S_ISDIR(s.st_mode):dirs.append(dict(relative_path=rel,path=str(p),identity=identity(s)))
        elif p.name!='MANIFEST.json':members.append(dict(relative_path=rel,**pin(p)))
    return members,dirs
def review_guard():
    r=json.loads((P/'REVIEW.json').read_bytes())
    require(r['schema']=='INDEPENDENT_COMPLETE_CONTEXT_AWARE_ENGINE_HOST_BINDER_SOURCE_REVIEW_V2'and r['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'and r['source_only']is True,'exact independent Source-only PASS')
    c=r['checks'];require(type(r['check_count'])is int and r['check_count']==len(c)==54 and len({x['check']for x in c})==54 and all(type(x)is dict and set(x)=={'check','passed'}and x['passed']is True for x in c)and r['blockers']==[],'full typed finite checks no blockers')
    require(r['new_Q']is None and r['scientific_qualification_created']is False and r['AAA_accuracy_qualified']is False and r['ABA_admitted']is False and r['actual_independent_candidate_execution']is None,'no numeric or science qualification')
    return r
mode=sys.argv[1]
r=review_guard()
if mode=='seal':
    require(not(P/'MANIFEST.json').exists()and not SIBLING.exists(),'once seal fresh paths')
    with(P/'MANIFEST.json').open('x')as f:f.write('')
    members,dirs=inventory()
    manifest=dict(schema='INDEPENDENT_COMPLETE_CONTEXT_SIX_FIX_SOURCE_REVIEW_MANIFEST_V1',source_only=True,status='SEALED_SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE',root=str(P),member_count=len(members),total_member_bytes=sum(x['size_bytes']for x in members),members=members,directory_count=len(dirs),directories=dirs,independent_review_pin=pin(P/'REVIEW.json'),actual_candidate_execution=None,new_Q=None,scientific_qualification_created=False)
    with(P/'MANIFEST.json').open('w')as f:json.dump(manifest,f,indent=2);f.write('\n')
    mp=pin(P/'MANIFEST.json');a,b=inventory();require(a==members and b==dirs,'all independent Source unchanged across manifest seal')
    SIBLING.mkdir()
    receipt=dict(schema='INDEPENDENT_COMPLETE_CONTEXT_SIX_FIX_SOURCE_REVIEW_SEAL_V1',source_only=True,sealed_original_manifest_pin=mp,sealed_original_source_root=str(P),full_member_count=len(members)+1,all_manifest_members_full_EOF_SHA_seven_ID=True,all_directories_seven_ID=True,independent_review_pin=pin(P/'REVIEW.json'),check_count=54,checks_all_typed_true=True,once_seal=True,candidate_executed=False,project_written=False,new_Q=None)
    with(SIBLING/'SOURCE_SEAL.json').open('x')as f:json.dump(receipt,f,indent=2);f.write('\n')
    print(json.dumps(dict(source_only=True,status='SEALED_SOURCE_ONLY_PASS',source_root=str(P),manifest_pin=mp,review_pin=pin(P/'REVIEW.json'),source_seal_pin=pin(SIBLING/'SOURCE_SEAL.json'),member_count=len(members),directory_count=len(dirs),new_Q=None,candidate_execution=False)),flush=True)
elif mode=='postseal':
    seal=json.loads((SIBLING/'SOURCE_SEAL.json').read_bytes());manifest=json.loads((P/'MANIFEST.json').read_bytes());mp=pin(P/'MANIFEST.json')
    require(mp==seal['sealed_original_manifest_pin'],'sealed manifest unchanged')
    members,dirs=inventory();require(members==manifest['members']and dirs==manifest['directories'],'postseal every Source member and directory unchanged')
    require(manifest['independent_review_pin']==pin(P/'REVIEW.json')==seal['independent_review_pin'],'review sealed Source current unchanged')
    true=json.loads((SIBLING/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json').read_bytes());terminal=true['terminal_tool_return']
    require(true['source_only']is True and true['closed']is True and type(terminal['exit_code'])is int and terminal['exit_code']==0 and 'session_id'not in terminal,'actual seal genuine exact int0 CLOSED')
    result=dict(schema='INDEPENDENT_COMPLETE_CONTEXT_SIX_FIX_SOURCE_REVIEW_POSTSEAL_V1',source_only=True,manifest_pin=mp,review_pin=pin(P/'REVIEW.json'),all_full_EOF_SHA_seven_ID_unchanged=True,all_directory_IDs_unchanged=True,full_file_count=len(members)+1,check_count=54,once_postseal=True,genuine_closed_seal_tool_pin=pin(SIBLING/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json'),candidate_executed=False,project_written=False,new_Q=None)
    with(SIBLING/'FULL_SOURCE_POSTSEAL_VERIFICATION.json').open('x')as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(dict(source_only=True,status='POSTSEAL_ALL_SOURCE_EXACT',manifest_pin=mp,review_pin=pin(P/'REVIEW.json'),postseal_pin=pin(SIBLING/'FULL_SOURCE_POSTSEAL_VERIFICATION.json'),full_file_count=len(members)+1,check_count=54,candidate_execution=False,new_Q=None)),flush=True)
else:raise ValueError('Source seal mode')
