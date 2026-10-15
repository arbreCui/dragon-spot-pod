"""Metadata/root accounting only; no GENDF publication, parser or child execution."""
import ast, base64, copy, hashlib, json, os, stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'current_eleven_saved_gendf_complete_cumulative_ten_roots_host_source_v7_20261014'
OUT=R/'current_eleven_saved_gendf_actual_cumulative_sixteen_roots_host_source_v10_20261014'
ART=Path('/Users/wen/spot/validation/artifacts')

def require(value,text):
    if not value:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    p=Path(path);s=p.lstat();require(stat.S_ISREG(s.st_mode),'ordinary Source/metadata')
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
        require(identity(os.fstat(f.fileno()))==identity(s),'open identity');sha=hashlib.file_digest(f,'sha256').hexdigest();require(identity(os.fstat(f.fileno()))==identity(s),'EOF identity')
    require(identity(p.lstat())==identity(s),'path identity')
    return dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=identity(s))
def read(p):return json.loads(Path(p['path']).read_bytes())
def write(p,value):
    raw=value if type(value)is bytes else (json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
    with p.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
    return pin(p)
def mutate(source,old,new,changes):
    require(source.count(old)==1,'one exact Source metadata splice');changes.append(dict(before=old,after=new));return source.replace(old,new,1)

def main():
    require(not OUT.exists(),'fresh Source namespace')
    oldplanpin=pin(OLD/'CURRENT_ELEVEN_GENDF_HOST_SOURCE_PREPARATION_PLAN.json');plan=read(oldplanpin)
    postpin=pin(R/'independent_empty_root_cumulative12_first_A_aggregate_actual_evidence_postverify_20261014/REVIEW.json');post=read(postpin)
    posttoolpin=pin(Path(postpin['path']).parent/'TRUE_TOOL_RETURNS.json');tools=read(posttoolpin)
    require(post['schema']=='INDEPENDENT_EMPTY_ROOT_CUMULATIVE12_FIRST_A_AGGREGATE_ACTUAL_EVIDENCE_POSTVERIFICATION_V1'and post['status']=='PASS_ACTUAL_EMPTY_ROOT_CUMULATIVE12_FIRST_A_AGGREGATE_EVIDENCE_POSTVERIFICATION'and post['failure']is None,'actual corrected aggregate independent evidence post')
    requestpin=post['actual_request_pin'];request=read(requestpin);aggpin=post['actual_aggregate_host_pin'];agg=read(aggpin)
    require(len(request['joint_archive_roots'])==12 and agg['operation']=='aggregate'and agg['failure']is None and agg['after_check_error']is None,'actual corrected cumulative request and host')
    for key in ['actual_review_return','actual_postverification_return']:
        term=tools[key];require(type(term['exit_code'])is int and term['exit_code']==0 and term.get('session_id')is None,'genuine actual independent post0')
        require(json.loads(term['output'].strip().splitlines()[-1])['review_pin']==postpin,'real post stdout identity')
    output=ART/'axial-material-current-eleven-saved-GENDF-complete-cumulative-sixteen-roots-20261014-v10'
    child=output.with_name(output.name+'-evidence')
    closure=plan['original_five_role_roots_preserved'][2]
    original5=[str(output),str(child),closure,str(OUT),plan['original_five_role_roots_preserved'][4]]
    roots=original5+[v for v in request['joint_archive_roots']if v not in original5]
    require(len(roots)==16 and len(set(roots))==16 and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'true complete16 cumulative distinct roots')
    artifact=[v for v in roots if Path(v).is_relative_to(ART)];source=[v for v in roots if not Path(v).is_relative_to(ART)]
    require(len(artifact)==10 and len(source)==6 and all(Path(v).is_relative_to(R)for v in source),'10 ART and6 exact Source/request metadata roots')
    sourcecode=(OLD/'run_current_eleven_gendf_extraction.py').read_text();host=sourcecode;hc=[]
    host=mutate(host,'source_root_paths=[str(BASE),str(Path(planpin[\'path\']).parent)]','source_root_paths=[str(BASE),str(Path(planpin[\'path\']).parent)]+sf[\'cumulative_Source_root_paths\'][2:]',hc)
    host=mutate(host,'len(artifact_roots)!=8 or len(source_root_paths)!=2 or len(set(roots))!=10','len(artifact_roots)!=10 or len(source_root_paths)!=6 or len(set(roots))!=16',hc)
    host=mutate(host,"'ten disjoint cumulative original2GiB roles: original five plus capture/extract/aggregate'","'sixteen disjoint cumulative original2GiB roles: original five plus all actual capture/extract/aggregate and REC roots'",hc)
    host=mutate(host,"'original joint fresh2GiB: eight cumulative ART roles plus two full Source trees and host open-unlinked'","'original joint fresh2GiB: ten cumulative ART roles plus six full Source/request trees and host open-unlinked'",hc)
    host=mutate(host,'complete_ten_role_joint_bytes=joint','complete_sixteen_role_joint_bytes=joint',hc)
    writer0=(OLD/'write_once_GENDF_cumulative_ten_roots_SF_HF_recipe.py').read_text();writer=writer0;wc=[]
    for a,z in [("argv['exact_argv']","argv['argv']"),('INDEPENDENT_EIGHT_ROOT_FIRST_A_COMPLETE_AGGREGATE_ACTUAL_EVIDENCE_POSTVERIFICATION_V1',post['schema']),('PASS_ACTUAL_EIGHT_ROOT_FIRST_A_COMPLETE_AGGREGATE_EVIDENCE_POSTVERIFICATION',post['status']),('expected_original_DiskResources_ART_role_count=8,complete_joint_source_tree_role_count=2,complete_cumulative_joint_root_count=10','expected_original_DiskResources_ART_role_count=10,complete_joint_source_tree_role_count=6,complete_cumulative_joint_root_count=16'),('complete_cumulative_joint_root_count=10,candidate_executed=False','complete_cumulative_joint_root_count=16,candidate_executed=False'),('requires_original_closed_capture_plus_extraction_plus_aggregation_complete_cumulative_ten_roots=True','requires_original_closed_capture_plus_extraction_plus_both_aggregations_and_REC_complete_cumulative_sixteen_roots=True'),("status='GENDF_TEN_ROOTS_SOURCE_METADATA_PUBLISHED_ONLY'","status='GENDF_SIXTEEN_ROOTS_SOURCE_METADATA_PUBLISHED_ONLY'")]:
        if a=="argv['exact_argv']":
            require(writer.count(a)==2,'two true argv references');before=writer;writer=writer.replace(a,z);wc.append(dict(before=before,after=writer))
        else:writer=mutate(writer,a,z,wc)
    canon="canon={'actual_report_pin':pins['aggregate-report'],'actual_Root_true_tool_return_pin':pins['aggregate-Root-tools'],'actual_Root_argv_pin':pins['aggregate-Root-argv']}"
    writer=mutate(writer,canon,"canon={'actual_aggregate_host_pin':pins['aggregate-report'],'actual_Root_true_tool_pin':pins['aggregate-Root-tools'],'actual_Root_argv_pin':pins['aggregate-Root-argv'],'actual_aggregate_report_pin':childpin}",wc)
    ast.parse(host);ast.parse(writer)
    OUT.mkdir();copies=[]
    for name in ['extract_current_eleven_saved_gendf.py','run_current_eleven_gendf_extraction.py','build_root_reviewable_actual_gendf_cli.py']:
        original=pin(OLD/name);raw=host.encode()if name=='run_current_eleven_gendf_extraction.py'else Path(original['path']).read_bytes()
        if name=='extract_current_eleven_saved_gendf.py':
            text=raw.decode();before="type(roots)is list and len(roots)==5 and len(set(roots))==5,'all five disjoint joint roles'";after="type(roots)is list and len(roots)==16 and len(set(roots))==16,'all sixteen disjoint cumulative joint roles'";require(text.count(before)==1,'exact child resource role count guard');raw=text.replace(before,after,1).encode()
        candidate=write(OUT/name,raw)
        copies.append(dict(predecessor_pin=original,candidate_pin=candidate,whole_bytes_unchanged=raw==Path(original['path']).read_bytes()))
    wp=write(OUT/'write_once_GENDF_cumulative_ten_roots_SF_HF_recipe.py',writer.encode())
    for after,before,changes in [(host,sourcecode,hc),(writer,writer0,wc)]:
        back=after
        for c in reversed(changes):require(back.count(c['after'])==1,'unique full inverse');back=back.replace(c['after'],c['before'],1)
        require(back==before,'exact full inverse to previous immutable Source')
    inverse=write(OUT/'COMPLETE_GENDF_V7_TO_ACTUAL_CUMULATIVE16_V10_SOURCE_WHOLE_BYTE_INVERSE.json',dict(schema='COMPLETE_GENDF_V7_TO_ACTUAL_CUMULATIVE16_V10_SOURCE_WHOLE_BYTE_INVERSE_V1',source_only=True,host_predecessor_pin=pin(OLD/'run_current_eleven_gendf_extraction.py'),host_candidate_pin=pin(OUT/'run_current_eleven_gendf_extraction.py'),host_changes=hc,writer_predecessor_pin=pin(OLD/'write_once_GENDF_cumulative_ten_roots_SF_HF_recipe.py'),writer_candidate_pin=wp,writer_changes=wc,host_original_whole_bytes_base64=base64.b64encode(sourcecode.encode()).decode(),writer_original_whole_bytes_base64=base64.b64encode(writer0.encode()).decode(),source_copies=copies,child_budget_exact_original_count=5,child_budget_exact_current_count=16,child_original_whole_bytes_base64=base64.b64encode((OLD/'extract_current_eleven_saved_gendf.py').read_bytes()).decode(),child_candidate_source_pin=pin(OUT/'extract_current_eleven_saved_gendf.py'),whole_host_and_writer_inverse_byte_equal=True,only_child_Budget_init_resource_count_changed=True,all_child_scientific_functions_and_original_parser_and_metadata_builder_whole_bytes_unchanged=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
    replacements={v['predecessor_pin']['path']:v['candidate_pin']for v in copies}
    plan['complete_source_file_pins']=[replacements.get(v['path'],v)for v in plan['complete_source_file_pins']]
    plan.update(schema='GENDF_ACTUAL_COMPLETE_CUMULATIVE_SIXTEEN_ROOTS_SOURCE_PLAN_V1',source_only=True,Source_author_pin=pin(__file__),predecessor_v7_plan_pin=oldplanpin,source_copies=copies,candidate_host_source_pin=pin(OUT/'run_current_eleven_gendf_extraction.py'),original_five_role_roots_preserved=original5,cumulative_artifact_root_paths=artifact,cumulative_Source_root_paths=source,complete_cumulative_ten_role_roots=roots,complete_cumulative_sixteen_role_roots=roots,planned_actual_output_root=str(output),planned_actual_evidence_root=str(child),future_aggregation_artifact_roots=[str(Path(aggpin['path']).parent),str(Path(post['actual_aggregate_report_pin']['path']).parent)],actual_aggregation_report_pin=aggpin,actual_aggregation_post_pin=postpin,actual_aggregation_Root_tool_pin=post['actual_Root_true_tool_pin'],actual_aggregation_Root_argv_pin=post['actual_Root_argv_pin'],actual_aggregation_post_tools_pin=posttoolpin,actual_aggregation_POST_schema=post['schema'],actual_aggregation_POST_status=post['status'],actual_corrected_aggregation_request_pin=requestpin,complete_scoped_byte_inverse_pin=inverse,complete_cumulative_ART_role_count=10,complete_cumulative_Source_request_role_count=6,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,physics_qualified=False)
    plan['selected_closed_current_authority_pins']+= [postpin,posttoolpin,aggpin,post['actual_aggregate_report_pin'],requestpin,post['actual_Root_true_tool_pin'],post['actual_Root_argv_pin']]
    pp=write(OUT/'CURRENT_ELEVEN_GENDF_HOST_SOURCE_PREPARATION_PLAN.json',plan)
    ready=dict(schema='GENDF_ACTUAL_CUMULATIVE16_CANDIDATE_WRITER_SOURCE_READY_V1',source_only=True,plan_pin=pp,complete_inverse_pin=inverse,writer_source_pin=wp,selected_Source_pins=[pin(OUT/v)for v in ['run_current_eleven_gendf_extraction.py','extract_current_eleven_saved_gendf.py','build_root_reviewable_actual_gendf_cli.py']]+[pp,inverse,wp],actual_aggregation_report_pin=aggpin,actual_GENDF_report_pin=None,future_Source_freeze_pin=None,future_Host_freeze_pin=None,future_recipe_pin=None,original_Host_argv_count=32,original_metadata_builder_argv_count=18,once_writer_required_fullpin_role_count=8,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,physics_qualified=False)
    rp=write(OUT/'SOURCE_REVIEW_READY.json',ready)
    fd=os.open(OUT,os.O_RDONLY|os.O_DIRECTORY);os.fsync(fd);os.close(fd)
    print(json.dumps(dict(status='GENDF_ACTUAL_CUMULATIVE16_SOURCE_ONLY_READY_NOT_PUBLISHED',ready_pin=rp,plan_pin=pp,inverse_pin=inverse,writer_source_pin=wp,Source_author_pin=pin(__file__),actual_GENDF_report_pin=None,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)))

if __name__=='__main__':main()
