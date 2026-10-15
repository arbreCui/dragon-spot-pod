import hashlib,json,shutil,stat
from pathlib import Path

ROOT=Path('/private/tmp/axmat_v25_final_bound_BUILD_and_utility_Source_independent_review_20261010')
CORE=Path('/private/tmp/axmat_v25_actual_bound_BUILD_Source_independent_review_ATTEMPT1_20261010')
ADDON=Path('/private/tmp/axmat_v25_complete_BUILD_utility_Source_independent_addon_V2_PASS_20261010')
FAILED=Path('/private/tmp/axmat_v25_complete_BUILD_utility_Source_independent_addon_ATTEMPT1_20261010')
TOOLS=Path('/private/tmp/axmat_v25_independent_bound_BUILD_Source_reviewer_lc9abzxf')

def pin(p):
    s=p.lstat();i=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    if not stat.S_ISREG(s.st_mode):raise ValueError('regular Source/META')
    with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    z=p.lstat()
    if i!=[z.st_dev,z.st_ino,z.st_mode,z.st_nlink,z.st_size,z.st_mtime_ns,z.st_ctime_ns]:raise ValueError('EOF changed')
    return dict(path=str(p),sha256=h,size_bytes=s.st_size,identity=i)

def read(p):
    before=pin(p);v=json.loads(p.read_bytes())
    if pin(p)!=before:raise ValueError('META changed')
    return v

def actual(tool,report,chunk):
    tr=tool['actual_tool_return']
    if type(tr['exit_code']) is not int or tr['exit_code']!=0 or 'session_id' in tr or tr['chunk_id']!=chunk:raise ValueError('real closed integer EXIT0')
    if json.loads(tr['output'])['review_pin']!=pin(report):raise ValueError('real raw tool report pin')

def main():
    if ROOT.exists():raise ValueError('fresh complete peer package required')
    c=read(CORE/'REVIEW.json');a=read(ADDON/'REVIEW.json')
    for v in (c,a):
        if v['all_checks_typed_true'] is not True or v['blockers']!=[] or v['check_count']!=len(v['checks']) or any(type(x['passed']) is not bool or x['passed'] is not True for x in v['checks']):raise ValueError('strict finite review PASS')
    actual(read(CORE/'ACTUAL_INDEPENDENT_CORE_SOURCE_REVIEW_TOOL_RETURN.json'),CORE/'REVIEW.json','6da22e')
    actual(read(ADDON/'ACTUAL_INDEPENDENT_UTILITY_SOURCE_REVIEW_TOOL_RETURN.json'),ADDON/'REVIEW.json','390c85')
    if c['status']!='PASS_ACTUAL_BOUND_FULL_BUILD_AND_POSTCLOSE_META_SOURCE_ONLY' or a['status']!='PASS_UTILITY_SOURCE_ONLY':raise ValueError('actual Source-only report classification')
    ROOT.mkdir();copies={}
    for role,directory in [('historical_actual_core',CORE),('actual_utility_addon_PASS',ADDON),('historical_reviewer_count_contract_failure',FAILED)]:
        (ROOT/role).mkdir()
        for p in sorted(directory.iterdir()):
            if not p.is_file():raise ValueError('complete finite report package members')
            before=pin(p);dest=ROOT/role/p.name;shutil.copyfile(p,dest)
            if pin(p)!=before or pin(dest)['sha256']!=before['sha256']:raise ValueError('exact complete copy')
            copies[str(dest.relative_to(ROOT))]=dict(original=before,saved=pin(dest))
    for name in ['ACTUAL_UTILITY_REVIEWER_DIRECTORY_COUNT_SINGLE_HUNK_INVERSE.json','ACTUAL_REVIEWER_DIRECTORY_COUNT_SOURCE_FIX_TOOL_RETURN.json','join_actual_core_and_utility_review_Source_META_only.py','seal_complete_independent_Source_review_stdlib_only.py']:
        p=TOOLS/name;dest=ROOT/name;before=pin(p);shutil.copyfile(p,dest)
        if pin(p)!=before or pin(dest)['sha256']!=before['sha256']:raise ValueError('Source / true tool inverse copy')
        copies[name]=dict(original=before,saved=pin(dest))
    result=dict(c)
    result.update(schema='INDEPENDENT_V25_ACTUAL_BOUND_FULL_BUILD_POSTCLOSE_META_SOURCE_REVIEW_V1',status='PASS_ACTUAL_BOUND_FULL_BUILD_AND_POSTCLOSE_META_SOURCE_ONLY',scope='COMPLETE_ACTUAL_BOUND_FIVE_STAGE_BUILD_POSTCLOSE_SOURCE_PLUS_FULL_SOURCE_INSTALLER_PRELAUNCH_UTILITY_AND_SAVED_PREP_Q_META_ONLY',all_checks_typed_true=True,blockers=[],check_count=len(a['checks']),checks=a['checks'],utility_Source_checks_typed_true=True,original_bound_Source_review_report_pin=pin(CORE/'REVIEW.json'),actual_original_core_review_tool_pin=pin(CORE/'ACTUAL_INDEPENDENT_CORE_SOURCE_REVIEW_TOOL_RETURN.json'),actual_utility_addon_review_pin=pin(ADDON/'REVIEW.json'),actual_utility_addon_review_tool_pin=pin(ADDON/'ACTUAL_INDEPENDENT_UTILITY_SOURCE_REVIEW_TOOL_RETURN.json'),actual_Source_utility_manifest_pin=a['actual_Source_utility_manifest_pin'],actual_Root_source_installer_Source_pin=a['actual_Root_source_installer_Source_pin'],actual_Root_prelaunch_checker_Source_pin=a['actual_Root_prelaunch_checker_Source_pin'],utility_full_byte_AST_inverses_verified=True,utility_all275_author_provenance_bytes_destination_equivalence=a['utility_all275_author_provenance_bytes_destination_equivalence'],utility_all144_original_PREP_inputs_current_full_EOF_SHA7ID_verified=True,core_and_addon_reports_retained_original_bytes=True,original_6da_core_report_not_overwritten=True,historical_reviewer_count_contract_failure_retained=True,complete_private_TMP_Source_review_copy_pairs=copies,actual_utility_installer_executed=False,actual_utility_prelaunch_executed=False,actual_BUILD_terminal=None,actual_BUILD_postclose_manifest=None,whole_build_qualified=False,whole_INPUT_admitted=False,native_RSS_verified=False,physical_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,goal_complete=False,candidate_helper_guard_API_compiler_numeric_executed=False,project_modified=False)
    (ROOT/'REVIEW.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(status=result['status'],source_only=True,review_pin=pin(ROOT/'REVIEW.json'),check_count=result['check_count'],actual_core_review_chunk='6da22e',actual_utility_addon_review_chunk='390c85',project_executed=False),allow_nan=False))

if __name__=='__main__':main()
