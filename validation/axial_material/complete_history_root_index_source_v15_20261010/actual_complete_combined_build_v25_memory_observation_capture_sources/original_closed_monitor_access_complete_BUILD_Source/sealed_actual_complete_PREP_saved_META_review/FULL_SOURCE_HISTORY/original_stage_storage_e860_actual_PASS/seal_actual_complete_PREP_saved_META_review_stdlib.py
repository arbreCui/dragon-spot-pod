"""Seal only a completed genuine independent saved PREP review package.

This stdlib metadata writer does not execute any reviewed Source. It requires
the actual successful independent review, its real closed tool receipt and all
six credit fields False. The manifest is the last file inside the package.
Real seal/postseal tool receipts must be saved in a sibling, never appended to
the sealed package. No future success or new business qualification is created.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat


def ident(p):
    s=p.lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def pin(p):
    before=ident(p)
    if not stat.S_ISREG(before[2]) or before[3]!=1: raise ValueError('regular single-link Source/META required')
    with p.open('rb') as f: sha=hashlib.file_digest(f,'sha256').hexdigest()
    if ident(p)!=before: raise ValueError('Source/META changed at full EOF')
    return dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--review-root',required=True)
    parser.add_argument('--review-sha256',required=True)
    parser.add_argument('--actual-review-tool-receipt',required=True)
    parser.add_argument('--actual-review-tool-receipt-sha256',required=True)
    args=parser.parse_args()
    root=Path(args.review_root)
    if not root.is_relative_to(Path('/private/tmp')) or root.is_symlink() or not root.is_dir(): raise ValueError('actual finite TMP saved review root required')
    reportpin=pin(root/'REVIEW.json')
    if reportpin['sha256']!=args.review_sha256: raise ValueError('exact actual reviewed report required')
    report=json.loads((root/'REVIEW.json').read_bytes())
    if report['schema']!='INDEPENDENT_V25_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_V1' or report['status']!='PASS_ACTUAL_COMPLETE_PREP_ONLY': raise ValueError('actual whole PREP saved peer required')
    if report['source_only'] is not True or report['all_checks_typed_true'] is not True or type(report['blockers']) is not list or report['blockers']!=[]: raise ValueError('Source-only full successful saved review required')
    if type(report['check_count']) is not int or report['check_count']!=len(report['checks']) or not all(type(row['passed']) is bool and row['passed'] is True for row in report['checks']): raise ValueError('strict exact typed checks and count required')
    for key in ('actual_PREP_closed_EXIT0_verified','actual_metadata_writer_closed_EXIT0_verified','all_complete_scope_verified','actual_PREP_metadata_only'):
        if report[key] is not True: raise ValueError('actual PREP complete '+key)
    for key in ('whole_combined_build_qualified','whole_combined_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','goal_complete'):
        if report[key] is not False: raise ValueError('PREP cannot confer '+key)
    toolp=Path(args.actual_review_tool_receipt); toolpin=pin(toolp)
    if toolpin['sha256']!=args.actual_review_tool_receipt_sha256: raise ValueError('actual independent review tool receipt fullpin required')
    tool=json.loads(toolp.read_bytes());tr=tool['actual_success_tool_return']
    if tool['source_only'] is not True or tool['raw_tool_stdout_preserved_as_strings'] is not True or type(tr['exit_code']) is not int or tr['exit_code']!=0 or 'session_id' in tr: raise ValueError('actual independent review closed integer EXIT0 required')
    observed=json.loads(tr['output'])
    if observed['status']!=report['status'] or observed['source_only'] is not True or observed['all_checks_typed_true'] is not True or observed['check_count']!=report['check_count'] or observed['review_pin']!=reportpin: raise ValueError('actual raw tool stdout binds this complete review')
    manifest=root/'MANIFEST.json'
    if os.path.lexists(manifest): raise ValueError('one seal only; manifest already exists')
    manifest.touch(exist_ok=False)
    files={};dirs={'.':ident(root)}
    for folder,names,fnames in os.walk(root,followlinks=False):
        for name in names:
            p=Path(folder)/name
            if p.is_symlink() or not p.is_dir(): raise ValueError('no Source package aliases')
            dirs[str(p.relative_to(root))]=ident(p)
        for name in fnames:
            p=Path(folder)/name
            if p!=manifest: files[str(p.relative_to(root))]=pin(p)
    body=dict(schema='INDEPENDENT_V25_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_MANIFEST_V1',source_only=True,member_count=len(files),complete_member_bytes=sum(row['size_bytes'] for row in files.values()),members=files,directories=dirs,review=reportpin,actual_success_review_tool_receipt=toolpin,new_business_or_science_qualification_created=False)
    with manifest.open('w') as f: json.dump(body,f,indent=2,allow_nan=False);f.write('\n')
    for row in files.values():
        if pin(Path(row['path']))!=row: raise ValueError('complete sealed member changed')
    for rel,row in dirs.items():
        if ident(root if rel=='.' else root/rel)!=row: raise ValueError('sealed directory changed')
    print(json.dumps(dict(source_only=True,manifest_pin=pin(manifest),review_pin=reportpin,actual_review_tool_receipt_pin=toolpin,member_count=len(files),check_count=report['check_count'],all_checks_typed_true=True,actual_Root_PREP_summary_pin=report['actual_Root_PREP_summary_pin'],actual_Root_PREP_terminal_pin=report['actual_Root_PREP_terminal_pin'],actual_complete_namespace_manifest_pin=report['actual_complete_namespace_manifest_pin'],whole_build_INPUT_native_or_science_qualified=False),allow_nan=False))


if __name__=='__main__': main()
