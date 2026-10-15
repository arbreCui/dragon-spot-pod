"""Seal / recheck only this peer's finite fresh private TMP Source-META package."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat

def identity(p):
    s=Path(p).lstat(); return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def ordinary(p):
    p=Path(p)
    if not p.is_absolute() or '..' in p.parts: raise ValueError('absolute ordinary private TMP path')
    for a in [*reversed(p.parents),p]:
        i=identity(a)
        if stat.S_ISLNK(i[2]) or (a!=p and not stat.S_ISDIR(i[2])): raise ValueError('alias path')
    return p

def pin(p):
    p=ordinary(p); before=identity(p)
    if not stat.S_ISREG(before[2]): raise ValueError('regular member required')
    with p.open('rb') as f: sha=hashlib.file_digest(f,'sha256').hexdigest()
    if identity(p)!=before: raise ValueError('member changed during complete EOF')
    return dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)

def read(p):
    def pairs(items):
        d={}
        for k,v in items:
            if k in d: raise ValueError('duplicate key')
            d[k]=v
        return d
    return json.loads(Path(p).read_bytes(),object_pairs_hook=pairs)

def snapshot(root):
    files={}; dirs={'.':identity(root)}
    for p in sorted(root.rglob('*')):
        i=identity(p); rel=str(p.relative_to(root))
        if stat.S_ISLNK(i[2]): raise ValueError('symlink not allowed')
        if stat.S_ISDIR(i[2]): dirs[rel]=i
        elif stat.S_ISREG(i[2]): files[rel]=pin(p)
        else: raise ValueError('nonregular entry')
    return files,dirs

def main():
    a=argparse.ArgumentParser(); a.add_argument('--root',required=True); a.add_argument('--mode',required=True,choices=['seal','postseal']); args=a.parse_args()
    root=ordinary(args.root)
    if not root.is_relative_to(Path('/private/tmp')): raise ValueError('only private TMP peer package')
    manifest=root/'MANIFEST.json'
    review=read(root/'REVIEW.json')
    if review['schema']!='INDEPENDENT_V25_ACTUAL_BOUND_FULL_BUILD_POSTCLOSE_META_SOURCE_REVIEW_V1' or review['status']!='PASS_ACTUAL_BOUND_FULL_BUILD_AND_POSTCLOSE_META_SOURCE_ONLY' or review['all_checks_typed_true'] is not True or review['blockers']!=[]: raise ValueError('strict actual Source-only PASS required')
    if type(review['check_count']) is not int or review['check_count']!=len(review['checks']) or any(type(r['passed']) is not bool or r['passed'] is not True for r in review['checks']): raise ValueError('all exact typed checks required')
    if args.mode=='seal':
        if os.path.lexists(manifest): raise ValueError('one-use source seal')
        manifest.touch(exist_ok=False)
        files,dirs=snapshot(root); members={rel:p for rel,p in files.items() if rel!='MANIFEST.json'}
        value=dict(schema='INDEPENDENT_V25_BOUND_BUILD_AND_UTILITY_SOURCE_REVIEW_COMPLETE_PACKAGE_MANIFEST_V1',source_only=True,member_count=len(members),complete_member_bytes=sum(p['size_bytes'] for p in members.values()),members=members,directories=dirs,review_pin=pin(root/'REVIEW.json'),qualified_actual_bound_Source_manifest_pin=review['qualified_actual_bound_Source_manifest_pin'],candidate_helper_guard_API_compiler_numeric_executed=False,whole_build_INPUT_native_science_qualified=False)
        manifest.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
    value=read(manifest); files,dirs=snapshot(root)
    if dirs!=value['directories'] or set(files)!=set(value['members'])|{'MANIFEST.json'} or any(files[k]!=p for k,p in value['members'].items()): raise ValueError('complete sealed peer package changed')
    if value['member_count']!=len(value['members']) or pin(root/'REVIEW.json')!=value['review_pin']: raise ValueError('complete metadata coupling differs')
    print(json.dumps(dict(status='PASS_COMPLETE_INDEPENDENT_SOURCE_REVIEW_SEAL' if args.mode=='seal' else 'PASS_COMPLETE_INDEPENDENT_SOURCE_REVIEW_POSTSEAL',source_only=True,manifest_pin=pin(manifest),review_pin=pin(root/'REVIEW.json'),complete_file_count=len(files),complete_subdirectory_count=len(dirs)-1,check_count=review['check_count'],candidate_helper_guard_API_compiler_numeric_executed=False,whole_build_INPUT_native_science_qualified=False),allow_nan=False))

if __name__=='__main__': main()
