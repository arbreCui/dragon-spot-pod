"""Seal / postseal only an already PASS finite new private TMP peer report."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat

def identity(p):
    s=Path(p).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def ordinary(p):
    p=Path(p)
    if not p.is_absolute() or '..' in p.parts: raise ValueError('absolute ordinary path')
    for a in [*reversed(p.parents),p]:
        i=identity(a)
        if stat.S_ISLNK(i[2]) or (a!=p and not stat.S_ISDIR(i[2])): raise ValueError('no aliases')
    return p

def pin(p):
    p=ordinary(p);before=identity(p)
    if not stat.S_ISREG(before[2]): raise ValueError('regular private report member')
    with p.open('rb') as f: sha=hashlib.file_digest(f,'sha256').hexdigest()
    if identity(p)!=before: raise ValueError('changed while full EOF hashing')
    return dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)

def read(p):
    def pairs(items):
        answer={}
        for k,v in items:
            if k in answer: raise ValueError('duplicate metadata key')
            answer[k]=v
        return answer
    def finite(value): raise ValueError('nonfinite metadata value')
    return json.loads(Path(p).read_bytes(),object_pairs_hook=pairs,parse_constant=finite)

def snapshot(root):
    files={};dirs={'.':identity(root)}
    for p in sorted(root.rglob('*')):
        i=identity(p);rel=str(p.relative_to(root))
        if stat.S_ISDIR(i[2]): dirs[rel]=i
        elif stat.S_ISREG(i[2]): files[rel]=pin(p)
        else: raise ValueError('ordinary regular finite package only')
    return files,dirs

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',required=True)
    ap.add_argument('--mode',required=True,choices=('seal','postseal'));a=ap.parse_args()
    root=ordinary(a.root)
    if not root.is_relative_to(Path('/private/tmp')): raise ValueError('private TMP package only')
    r=read(root/'REVIEW.json')
    if r['schema']!='INDEPENDENT_V25_ACTUAL_FAILED_BUILD_SAVED_SMALL_META_SOURCE_REVIEW_V1' or r['status']!='PASS_ACTUAL_FAILED_BUILD_SAVED_SMALL_META_SOURCE_ONLY' or r['all_checks_typed_true'] is not True or r['blockers']!=[]: raise ValueError('actual failed BUILD saved Source / small META PASS required')
    if type(r['typed_true_check_count']) is not int or r['typed_true_check_count']!=len(r['checks']) or any(type(q['typed_true']) is not bool or q['typed_true'] is not True for q in r['checks']): raise ValueError('exact typed checks required')
    tool=read(root/'ACTUAL_INDEPENDENT_REVIEW_TOOL_RETURN.json');t=tool['actual_tool_return']
    if tool['closed'] is not True or tool['observed_terminal'] is not True or type(t['exit_code']) is not int or t['exit_code']!=0 or 'session_id' in t: raise ValueError('genuine peer review closed terminal required')
    actual=json.loads(t['output'])
    if actual['report']['sha256']!=pin(root/'REVIEW.json')['sha256'] or actual['typed_true_check_count']!=len(r['checks']): raise ValueError('actual peer tool coupling differs')
    if r['actual_BUILD_exit_code']!=1 or r['whole_BUILD_qualified'] is not False or r['no_whole_INPUT_native_science_credit'] is not True: raise ValueError('actual failure qualification boundary required')
    mf=root/'MANIFEST.json'
    if a.mode=='seal':
        if os.path.lexists(mf): raise ValueError('fresh one-use peer seal required')
        mf.touch(exist_ok=False);files,dirs=snapshot(root)
        members={k:v for k,v in files.items() if k!='MANIFEST.json'}
        value=dict(schema='INDEPENDENT_V25_ACTUAL_FAILED_BUILD_SAVED_SOURCE_SMALL_META_PACKAGE_MANIFEST_V1',
            Source_small_META_only=True,member_count=len(members),members=members,directories=dirs,
            complete_member_bytes=sum(q['size_bytes'] for q in members.values()),review_pin=pin(root/'REVIEW.json'),
            actual_BUILD_exit_code=1,actual_root_BUILD_terminal_pin=r['actual_BUILD_Root_terminal_pin'],
            actual_writer_closed_terminal_pin=r['actual_postclose_writer_Root_terminal_pin'],
            all_five_inner_stages_observed_PASS=True,whole_BUILD_qualified=False,
            candidate_guard_API_compile_business_executed=False,no_whole_INPUT_native_science_credit=True)
        mf.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
    value=read(mf);files,dirs=snapshot(root)
    if dirs!=value['directories'] or set(files)!=set(value['members'])|{'MANIFEST.json'} or any(files[k]!=q for k,q in value['members'].items()): raise ValueError('complete sealed peer changed')
    if value['member_count']!=len(value['members']) or pin(root/'REVIEW.json')!=value['review_pin']: raise ValueError('complete coupling changed')
    print(json.dumps(dict(status='PASS_ACTUAL_FAILED_BUILD_SOURCE_SMALL_META_SEAL' if a.mode=='seal' else 'PASS_ACTUAL_FAILED_BUILD_SOURCE_SMALL_META_POSTSEAL',manifest_pin=pin(mf),review_pin=pin(root/'REVIEW.json'),complete_file_count=len(files),complete_subdirectory_count=len(dirs)-1,typed_true_check_count=len(r['checks']),candidate_guard_API_compile_business_executed=False,no_whole_INPUT_native_science_credit=True),allow_nan=False))

if __name__=='__main__': main()
