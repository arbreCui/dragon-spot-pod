import ast,copy,hashlib,json,os,stat
from pathlib import Path
from types import SimpleNamespace

R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
O=R/'independent_bq64_build_v4_fresh17_v2_post_curated66_Source_review_20261013'
checks=[];cache={};reports=[]
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(p):return {k:p[k]for k in ('path','sha256','size_bytes','identity')}
def pin(path):
    p=Path(path);i=ident(p.lstat())
    if not stat.S_ISREG(i[2]):raise AssertionError('ordinary Source/meta')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb')as f:
        if ident(os.fstat(f.fileno()))!=i:raise AssertionError('open7')
        raw=f.read()
        if ident(os.fstat(f.fileno()))!=i:raise AssertionError('EOF7')
    if ident(p.lstat())!=i:raise AssertionError('after7')
    pf=dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=i);cache[str(p)]=(pf,raw);return pf,raw
def same(p):
    p=norm(p);x=cache.get(p['path'])or pin(p['path'])
    if x[0]!=p:raise AssertionError('actual Source/meta PF '+p['path'])
    return x[1]
def read(p):
    pf,raw=pin(p);return json.loads(raw),pf
def check(ok,name):
    if not ok:raise AssertionError(name)
    checks.append(name)
def bound_review(path,toolpath):
    review,p=read(path);tool,tp=read(toolpath)
    check(review['failure']is None and review['status'].startswith('PASS'),'original retained Source review PASS')
    result=tool.get('actual_review_return')or tool.get('actual_tool_result')
    if result:
        check(result['exit_code']==0,'original retained Source true integer EXIT0')
        line=result['output'].strip().splitlines()[-1];out=json.loads(line)
        if 'review_pin'in out:check(norm(out['review_pin'])==p,'original raw tool0 exact review PF')
    return review,p,tp

common_sf,sfp=read(R/'post_curated66_current_catalog_common_source_v2_20261013/COMPLETE_POST_CURATED66_CURRENT_CATALOG_BINDING_COMMON_SOURCE_FREEZE.json')
check(sfp['sha256']=='e2b380b7acf9d0d550adf260420454f2a08f16380e41f1d66bd6b7f678aae5d9'and sfp['size_bytes']==17014,'actual completed new CommonSF exactSHA/size')
check(common_sf['source_only']is True and all(common_sf[k]is False for k in ('compiled','compiler_executed','numerical_executed','business_executed','Host_imported','deletion_executed','compiler_qualified','reader_qualified','AAA_qualified','ABA_admitted')),'new CommonSF Source only scope false actual qualification')
check(all(common_sf[k]is None for k in ('future_actual_build_object_pin','future_actual_build_report_pin','future_actual_control_report_pin')),'new CommonSF future actual pins None')
for p in common_sf['files']+common_sf['original_source_metadata_pins']:same(p)
sf_tool,stp=read(R/'ACTUAL_POST_CURATED66_CATALOG_COMMON_V2_FINAL_SOURCE_FREEZE_TRUE_TOOL_RETURN_20261013.json');tool=sf_tool['actual_source_freeze_tool_return']
check(tool['exit_code']==0 and norm(json.loads(tool['output'].strip().splitlines()[-1])['source_freeze_pin'])==sfp,'actual2df20b Sourcefreeze tool0 exactSFpin')
peer,peerp=read(common_sf['actual_independent_source_role_review_pin']['path']);same(common_sf['actual_independent_source_role_review_pin'])
pt,ptp=read(common_sf['actual_independent_source_role_true_tool_return_pin']['path']);same(common_sf['actual_independent_source_role_true_tool_return_pin'])
check(peer['status']=='PASS_POST_CURATED66_CATALOG_BINDING_COMMON_SOURCE_ONLY'and peer['failure']is None and pt['actual_review_return']['exit_code']==0 and norm(json.loads(pt['actual_review_return']['output'].strip().splitlines()[-1])['review_pin'])==peerp,'new CommonSF exact independent5398d1 review and trueTool0')
common=common_sf['new_Common_Source_pin'];same(common)
cases=[('BUILD','bq64_compact_expected_build_host_source_v4_20261013','build_bq64_compact_expected_runtime.py','COMPLETE_BUILD_HOST_V3_TO_V4_COMMON_OUTPUT_BYTE_INVERSE.json','97c65524edcb0649f0f33c426ffd155f192794e48fe20cb4280922fb7d1bd8f0',16066,'PASS_BUILD_V4_POST_CURATED66_COMMON_OUTPUT_ONLY_SOURCE_REVIEW','review_command_builder_source_only.py'),('FRESH17','bq64_compact_expected_connected17_host_source_v2_20261013','run_fresh_connected17.py','COMPLETE_FRESH17_HOST_V1_TO_V2_COMMON_OUTPUT_BYTE_INVERSE.json','c68980d2079817b72cf578ded142841d0bedf8389e4773bc2ae8bf920e75ba69',16913,'PASS_FRESH17_V2_POST_CURATED66_COMMON_OUTPUT_ONLY_SOURCE_REVIEW','review_fresh17_commands_source_only_v2.py')]
O.mkdir()
for kind,dirname,filename,invname,sha,size,status,reviewer in cases:
    begin=len(checks);D=R/dirname;host,raw=pin(D/filename);tree=ast.parse(raw)
    check((host['sha256'],host['size_bytes'])==(sha,size),'exact current '+kind+' Source SHA/size')
    inverse,ip=read(D/invname);check(norm(inverse['new_host_pin'])==host,'new host wholeinverse exact current PF')
    original_raw=same(inverse['original_host_pin']);restored=raw
    check(len(inverse['changed_exact_literals'])==3,'only3 declared literals')
    for s in inverse['changed_exact_literals']:
        after=s['new_literal'].encode();before=s['old_literal'].encode();check(restored.count(after)==1,'literal occurs exactly once');restored=restored.replace(after,before,1)
    check(restored==original_raw,'wholeEOF bytes inverse restores exact last independently reviewed Source')
    oldtree=ast.parse(original_raw)
    check([ast.dump(x,include_attributes=False)for x in tree.body if isinstance(x,(ast.FunctionDef,ast.ClassDef))]==[ast.dump(x,include_attributes=False)for x in oldtree.body if isinstance(x,(ast.FunctionDef,ast.ClassDef))],'all helpers/oracles/firsterror/guard procedures entire AST unchanged')
    out_node=next(x for x in tree.body if isinstance(x,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='OUT'for t in x.targets));out=Path('/Users/wen/spot')/ast.literal_eval(out_node.value.right)
    check(not out.exists()and not out.is_symlink(),'new business output still absent')
    check(str(Path(common['path']).relative_to(R)).encode()in raw and common['sha256'].encode()in raw,'Host exact Source-reviewed postreleaseCommon path/SHA')
    reviewer_pf,reviewer_raw=pin(D/reviewer);reviewer_tree=ast.parse(reviewer_raw);fn=next(x for x in reviewer_tree.body if isinstance(x,ast.FunctionDef)and x.name=='main')
    proofpath=O/(kind+'_FINITE_COMMAND_PROOF.json');ns=dict(ast=ast,copy=copy,hashlib=hashlib,json=json,os=os,Path=Path,SimpleNamespace=SimpleNamespace,HERE=D,REC=R,REPORT=proofpath)
    exec(compile(ast.Module(body=[fn],type_ignores=[]),'<extracted author source reviewer main>','exec'),ns);ns['main']()
    proof,proofpf=read(proofpath)
    check(proof['host_source_sha256']==sha and proof['positive_cases']==1 and len(proof.get('exact_negative_cases',proof.get('exact_refusals')))==8,'own actual extracted pure command proof1positive8refusals exact current Source')
    if kind=='BUILD':
        plan,pp=read(D/'EXACT_ORIGINAL70_TO_COMPACT_BQ64_BUILD_PLAN.json');oldplan,opp=read(R/'bq64_compact_expected_build_host_source_v3_20261013/EXACT_ORIGINAL70_TO_COMPACT_BQ64_BUILD_PLAN.json')
        check(plan['planned_output_root']==str(out)and norm(plan['source_Host_pin_before_freeze'])==host and norm(plan['selected_current_Common_pin'])==norm(common),'current PLAN exact Host/OUT/Common physical pins')
        check(plan['selected_postrelease_catalog_binding_Source_freeze_path']==sfp['path'],'PLAN exact postrelease SourceSF filename')
        check(plan['original_ordered70_input_pins']==oldplan['original_ordered70_input_pins']and len(plan['original_ordered70_input_pins'])==70 and plan['original_compile_module_full_EOF_pins']==oldplan['original_compile_module_full_EOF_pins']and len(plan['original_compile_module_full_EOF_pins'])==95 and plan['original_nine_core_object_pins']==oldplan['original_nine_core_object_pins'],'original70/95module/core9 full rows order unchanged')
        check(plan['original_caps']==oldplan['original_caps']and plan['original_compile_flags']==oldplan['original_compile_flags']and plan['original_compile_include_arguments']==oldplan['original_compile_include_arguments'],'original caps/flags/includes exact')
        check(all(plan[k]is None for k in plan if k.startswith('actual_new_'))and all(plan[k]is False for k in ('compile_qualified','new_reader_qualified','AAA_qualified','ABA_admitted')),'PLAN actual new build/controls/qualification remain future None/false')
        oldreview,rp,tp=bound_review(R/'independent_bq64_compact_build_host_v3_and_public_READ_plan_Source_review_20261013/REVIEW.json',R/'independent_bq64_compact_build_host_v3_and_public_READ_plan_Source_review_20261013/TRUE_TOOL_RETURN.json')
        freezer= D/'prepare_complete_build_freeze_source_only.py';freezerpf,freezerraw=pin(freezer);ast.parse(freezerraw)
        check(b"post_rows=post['files']+post['original_source_metadata_pins']"in freezerraw and b"[review_pin,review_true_pin,post_pin]+post_rows"in freezerraw and b"selected_postrelease_catalog_binding_Source_freeze_pin=post_pin"in freezerraw and b"selected_current_Common_pin=plan['selected_current_Common_pin']"in freezerraw,'draft freezer includes whole postSF closure+own exactCommonSF/currentCommon fields')
        extras=dict(plan_pin=pp,original_plan_pin=opp,draft_freezer_source_pin=freezerpf)
    else:
        oldreview,rp,tp=bound_review(R/'independent_fresh17_connected_new_BOOTQ_Host_source_review_20261013/REVIEW.json',R/'independent_fresh17_connected_new_BOOTQ_Host_source_review_20261013/TRUE_TOOL_RETURNS.json')
        check(norm(oldreview['candidate_source_pin'])==norm(inverse['original_host_pin']),'latest actualc8/1ebe3e Source0 used as original; historical491 not substituted')
        check(proof['original20_stages_retained']is True and proof['synthetic_future_paths_are_not_actual_PF']is True,'exact20commands17cases18phases proof does not invent actual new build PF')
        extras=dict(future_actual_new_build_report_pin=None,own_host_freeze_pin=None,full_original_control_source_and_oracle_inherited_unchanged=True)
    report=dict(schema='INDEPENDENT_POST_CURATED66_NEW_COMMON_HOST_THREE_LITERAL_SOURCE_ONLY_REVIEW_V1',kind=kind,status=status,failure=None,current_host_pin=host,original_host_pin=norm(inverse['original_host_pin']),complete_byte_inverse_pin=ip,selected_new_Common_Source_pin=norm(common),selected_postrelease_catalog_binding_Source_freeze_pin=sfp,selected_actual_common_sf_true_tool_pin=stp,selected_Common_independent_source_review_pin=peerp,selected_Common_independent_true_tool_pin=ptp,original_current_Source_review_pin=rp,original_current_Source_true_tool_pin=tp,actual_independent_finite_command_proof_pin=proofpf,finite_reviewer_source_pin=reviewer_pf,command_positive_cases=1,command_refusal_cases=8,source_only=True,Host_imported=False,Host_main_executed=False,compiler_executed=False,compiled=False,numerical_executed=False,controls_executed=False,business_executed=False,deletion_executed=False,released_targets_opened=False,science_EOF_repeated=False,reader_qualified=False,AAA_qualified=False,ABA_admitted=False,all_file_descriptors_closed=True,checks=checks[:begin]+checks[begin:],**extras)
    reports.append(report)
for pf,_ in cache.values():
    if ident(Path(pf['path']).lstat())!=pf['identity']:raise AssertionError('all Source/meta final7')
pins=[]
for report in reports:
    p=O/(report['kind']+'_REVIEW.json');p.write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n');pins.append(pin(p)[0])
print(json.dumps(dict(status='PASS_BUILD_V4_AND_FRESH17_V2_SOURCE_ONLY',failure=None,BUILD_REVIEW_pin=pins[0],FRESH17_REVIEW_pin=pins[1],current_build_host_pin=reports[0]['current_host_pin'],current_fresh17_host_pin=reports[1]['current_host_pin'],selected_postrelease_catalog_binding_Source_freeze_pin=sfp,compiler_executed=False,controls_executed=False,all_file_descriptors_closed=True),ensure_ascii=False))
