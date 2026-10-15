"""Source-only exact publication mapping and cumulative metadata accounting."""
import ast, base64, copy, hashlib, json, os, stat
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=REC/'current_eleven_saved_gendf_actual_cumulative_sixteen_roots_host_source_v10_20261014'
OUT=REC/'current_eleven_saved_gendf_actual_cumulative_seventeen_roots_host_source_v11_20261014'
ART=Path('/Users/wen/spot/validation/artifacts')
NAMES=('extract_current_eleven_saved_gendf.py','run_current_eleven_gendf_extraction.py','build_root_reviewable_actual_gendf_cli.py')
META=('ROOT_EXACT_GENDF_CUMULATIVE16_ACTUAL32_ARGV_20261014.json','ROOT_ACTUAL_GENDF_CUMULATIVE16_METADATA18_BINDER_TRUE_TOOL_RETURNS_20261014.json')
def require(ok,text):
    if not ok:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    p=Path(path);s=p.lstat()
    require(p.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid()and not any(a.is_symlink()for a in(p,*p.parents)),'ordinary own single-link Source/metadata')
    require(s.st_size<64*2**20,'bounded Source/metadata')
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
        require(identity(os.fstat(f.fileno()))==identity(s),'open7');h=hashlib.file_digest(f,'sha256').hexdigest();require(identity(os.fstat(f.fileno()))==identity(s),'EOF7')
    require(identity(p.lstat())==identity(s),'current7')
    return dict(path=str(p),sha256=h,size_bytes=s.st_size,identity=identity(s))
def read(p):
    require(pin(p['path'])==p,'exact selected metadata fullPF');return json.loads(Path(p['path']).read_bytes())
def write(p,v):
    raw=v if type(v)is bytes else(json.dumps(v,indent=2,allow_nan=False)+'\n').encode()
    with p.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
    return pin(p)
def splice(text,before,after,changes):
    require(text.count(before)==1,'one exact Source splice');changes.append(dict(before=before,after=after));return text.replace(before,after,1)
def inverse(candidate,original,changes):
    back=candidate
    for change in reversed(changes):
        require(back.count(change['after'])==1,'one exact inverse splice');back=back.replace(change['after'],change['before'],1)
    require(back==original,'whole-byte original Source inverse')
def main():
    require(not OUT.exists(),'fresh Source-only namespace')
    previous_plan_pin=pin(OLD/'CURRENT_ELEVEN_GENDF_HOST_SOURCE_PREPARATION_PLAN.json');plan=read(previous_plan_pin)
    loaded_sf=read(plan['predecessor_source_freeze_pin'])
    loaded_hf=read(plan['predecessor_host_freeze_pin'])
    original_selection=[loaded_sf['complete_source_file_pins'][i]for i in(0,1,3)]
    require([Path(p['path']).name for p in original_selection]==list(NAMES),'three exact loaded predecessor Source roles')
    require(all(p in loaded_hf['dependencies']for p in original_selection),'three exact loaded predecessor HF rows')
    metadata=[pin(REC/name)for name in META]
    require(len({tuple(p['identity'][:2])for p in metadata})==2,'two distinct explicit metadata nodes')
    published=[pin(OLD/name)for name in('COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json','COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json','ROOT_REVIEWABLE_CURRENT_GENDF_V4_CLI_SOURCE_ONLY.json')]
    closure_rows=[p for p in plan['selected_closed_current_authority_pins']if Path(p['path']).parent==Path(plan['original_five_role_roots_preserved'][2])and Path(p['path']).name=='Root_actual_material_observation_execution_summary.json']
    require(len(closure_rows)==1,'one exact retained completion report authority')
    closure=read(closure_rows[0]);capture_owner=str(Path(closure['actual_prior_A_cwd']).parent)
    require(closure['completion_only_existing_closed_stage']is True and closure['Dragon_or_compiler_or_material_child_launched_by_continuation']is False and Path(closure['original_failed_phase_pin']['path']).parent==Path(capture_owner),'exact original captured physical owner')
    host0=(OLD/NAMES[1]).read_text();host=host0;hc=[]
    host=splice(host,'len(source_root_paths)!=6 or len(set(roots))!=16','len(source_root_paths)!=7 or len(set(roots))!=17',hc)
    host=splice(host,"'sixteen disjoint cumulative original2GiB roles: original five plus all actual capture/extract/aggregate and REC roots'","'seventeen disjoint cumulative original2GiB roles: original five plus all actual capture/extract/aggregate and published Source roots'",hc)
    host=splice(host,"str(Path(observed['actual_prior_A_cwd']).parent)!=artifact_roots[3] or Path(observed['original_failed_phase_pin']['path']).parent!=Path(artifact_roots[3])","str(Path(observed['actual_prior_A_cwd']).parent)!=sf['retained_actual_capture_owner_root'] or Path(observed['original_failed_phase_pin']['path']).parent!=Path(sf['retained_actual_capture_owner_root'])",hc)
    # Exact two top-level metadata files are counted without scanning all REC.
    host=splice(host,'    source_roots=[Path(value)for value in source_root_paths]\n','    source_roots=[Path(value)for value in source_root_paths]\n    explicit_metadata=sf[\'cumulative_explicit_metadata_file_pins\']\n    if len(explicit_metadata)!=2 or [p[\'path\']for p in explicit_metadata]!=[str(REC/name)for name in '+repr(META)+']:\n        raise RuntimeError(\'exact two previous metadata publications\')\n',hc)
    host=splice(host,'        return total,count\n','''        nodes=set()
        for expected in explicit_metadata:
            p=Path(expected['path']);item=p.lstat()
            actual=[item.st_dev,item.st_ino,item.st_mode,item.st_nlink,item.st_size,item.st_mtime_ns,item.st_ctime_ns]
            if actual!=expected['identity'] or expected['size_bytes']!=item.st_size or not stat.S_ISREG(item.st_mode) or item.st_nlink!=1 or item.st_uid!=os.getuid() or any(a.is_symlink()for a in(p,*p.parents)):
                raise RuntimeError('exact ordinary explicit metadata current7/no aliases')
            node=(item.st_dev,item.st_ino)
            if node in nodes:raise RuntimeError('distinct explicit metadata nodes')
            nodes.add(node)
            if not any(p.is_relative_to(root)for root in source_roots+[Path(v)for v in artifact_roots]):
                total+=item.st_size;count+=1
        return total,count
''',hc)
    host=splice(host,"'original joint fresh2GiB: ten cumulative ART roles plus six full Source/request trees and host open-unlinked'","'original joint fresh2GiB: ten cumulative ART roles plus seven full Source/request trees, two explicit metadata files and host open-unlinked'",hc)
    host=splice(host,'complete_sixteen_role_joint_bytes=joint','complete_seventeen_role_joint_bytes=joint',hc)
    host=splice(host,"    fixed+=[psf,phf,pobserved,planpin,casepin,release,hf['host_source']]+hf['dependencies']+sf['complete_source_file_pins']","    fixed+=[psf,phf,pobserved,planpin,casepin,release,hf['host_source']]+hf['dependencies']+sf['complete_source_file_pins']+explicit_metadata",hc)
    host=splice(host,'requested_mts=[5],joint_archive_roots=roots,output_directory=str(childout),fixed_current_pins=fixed,','requested_mts=[5],joint_archive_roots=roots,cumulative_explicit_metadata_file_pins=explicit_metadata,output_directory=str(childout),fixed_current_pins=fixed,',hc)
    child0=(OLD/NAMES[0]).read_text();child=child0;cc=[]
    child=splice(child,'    def __init__(self,roots):\n        require(type(roots)is list and len(roots)==16 and len(set(roots))==16,\'all sixteen disjoint cumulative joint roles\')','    def __init__(self,roots,explicit_metadata):\n        require(type(roots)is list and len(roots)==17 and len(set(roots))==17,\'all seventeen disjoint cumulative joint roles\')\n        require(type(explicit_metadata)is list and len(explicit_metadata)==2,\'exact two explicit metadata file pins\')\n        self.explicit_metadata=explicit_metadata',cc)
    child=splice(child,'        unlinked={}\n','''        nodes=set()
        for expected in self.explicit_metadata:
            require(type(expected)is dict and set(expected)=={'path','sha256','size_bytes','identity'},'exact explicit metadata fullPF')
            p=Path(expected['path']);s=p.lstat()
            require(p.is_absolute()and not any(a.is_symlink()for a in(p,*p.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid()and identity(s)==expected['identity']and s.st_size==expected['size_bytes'],'ordinary explicit metadata current7/no aliases')
            node=(s.st_dev,s.st_ino);require(node not in nodes,'distinct explicit metadata nodes');nodes.add(node)
            if not any(p.is_relative_to(root)for root in self.roots):total+=s.st_size
        unlinked={}
''',cc)
    child=splice(child,"    budget=Budget(binding['joint_archive_roots']);budget.check()","    budget=Budget(binding['joint_archive_roots'],binding['cumulative_explicit_metadata_file_pins']);budget.check()",cc)
    child=splice(child,"    table={p['path']:p for p in sf['complete_source_file_pins']}","    require(sf['cumulative_explicit_metadata_file_pins']==binding['cumulative_explicit_metadata_file_pins'],'same exact explicit metadata resource bindings')\n    table={p['path']:p for p in sf['complete_source_file_pins']}",cc)
    writer0=(OLD/'write_once_GENDF_cumulative_ten_roots_SF_HF_recipe.py').read_text();writer=writer0;wc=[]
    writer=splice(writer," replacements={r['predecessor_pin']['path']:r['candidate_pin']for r in plan['source_copies']}\n sf['complete_source_file_pins']=[replacements.get(p['path'],p)for p in sf['complete_source_file_pins']]",''' mapping=plan['publication_source_mapping']
 if len(mapping)!=3 or len({row['predecessor_pin']['path']for row in mapping})!=3:raise RuntimeError('three explicit loaded-predecessor publication rows')
 for row in mapping:
  if row['predecessor_pin']not in sf['complete_source_file_pins'] or row['predecessor_pin']not in hf['dependencies'] or pin(row['candidate_pin']['path'])!=row['candidate_pin']:raise RuntimeError('exact fullPF predecessor-to-candidate publication mapping')
 counts=[0,0,0]
 def replace_exact(value):
  if type(value)is dict:
   for index,row in enumerate(mapping):
    if value==row['predecessor_pin']:
     counts[index]+=1;return copy.deepcopy(row['candidate_pin'])
   return {key:replace_exact(item)for key,item in value.items()}
  if type(value)is list:return[replace_exact(item)for item in value]
  return value
 sf=replace_exact(sf);hf=replace_exact(hf)
 if counts!=[2,2,2]:raise RuntimeError('exact three SF and three HF current Source pointers')
 if any(row['candidate_pin']not in sf['complete_source_file_pins'] or row['candidate_pin']not in hf['dependencies']for row in mapping):raise RuntimeError('all three actual current Source pointers published')''',wc)
    writer=splice(writer,'expected_original_DiskResources_ART_role_count=10,complete_joint_source_tree_role_count=6,complete_cumulative_joint_root_count=16','expected_original_DiskResources_ART_role_count=10,complete_joint_source_tree_role_count=7,complete_cumulative_joint_root_count=17,cumulative_explicit_metadata_file_pins=plan[\'cumulative_explicit_metadata_file_pins\']',wc)
    writer=splice(writer,"cumulative_Source_root_paths=plan['cumulative_Source_root_paths'],selected_actual_aggregation_report_pin=","cumulative_Source_root_paths=plan['cumulative_Source_root_paths'],retained_actual_capture_owner_root=plan['retained_actual_capture_owner_root'],selected_actual_aggregation_report_pin=",wc)
    writer=splice(writer,'complete_cumulative_joint_root_count=16,candidate_executed=False','complete_cumulative_joint_root_count=17,cumulative_explicit_metadata_file_pins=plan[\'cumulative_explicit_metadata_file_pins\'],candidate_executed=False',wc)
    writer=splice(writer,'requires_original_closed_capture_plus_extraction_plus_both_aggregations_and_REC_complete_cumulative_sixteen_roots=True','requires_original_closed_capture_plus_extraction_plus_both_aggregations_and_REC_complete_cumulative_seventeen_roots_and_two_exact_metadata_files=True',wc)
    writer=splice(writer,"status='GENDF_SIXTEEN_ROOTS_SOURCE_METADATA_PUBLISHED_ONLY'","status='GENDF_SEVENTEEN_ROOTS_EXACT_PUBLICATION_MAPPING_SOURCE_METADATA_PUBLISHED_ONLY'",wc)
    for value in(host,child,writer):ast.parse(value)
    for candidate,original,changes in[(host,host0,hc),(child,child0,cc),(writer,writer0,wc)]:inverse(candidate,original,changes)
    OUT.mkdir();copies=[]
    for name,raw in[(NAMES[0],child.encode()),(NAMES[1],host.encode()),(NAMES[2],(OLD/NAMES[2]).read_bytes())]:
        before=pin(OLD/name);after=write(OUT/name,raw);copies.append(dict(predecessor_pin=before,candidate_pin=after,whole_bytes_unchanged=before['sha256']==after['sha256']))
    wp=write(OUT/'write_once_GENDF_cumulative_ten_roots_SF_HF_recipe.py',writer.encode())
    mapping=[dict(predecessor_pin=before,candidate_pin=row['candidate_pin'])for before,row in zip(original_selection,copies)]
    output=ART/'axial-material-current-eleven-saved-GENDF-complete-cumulative-seventeen-roots-20261014-v11';evidence=output.with_name(output.name+'-evidence')
    artifact=copy.deepcopy(plan['cumulative_artifact_root_paths']);artifact[:2]=[str(output),str(evidence)]
    source=copy.deepcopy(plan['cumulative_Source_root_paths']);source[0]=str(OUT);source.append(str(OLD))
    roots=artifact[:3]+source+artifact[3:]
    require(len(artifact)==10 and len(source)==7 and len(set(roots))==17 and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'exact complete17 disjoint roots')
    inv=write(OUT/'COMPLETE_GENDF_V10_TO_V11_EXACT_PUBLICATION_AND_RESOURCE_WHOLE_BYTE_INVERSE.json',dict(schema='COMPLETE_GENDF_V10_TO_V11_EXACT_PUBLICATION_AND_RESOURCE_WHOLE_BYTE_INVERSE_V1',source_only=True,host_predecessor_pin=pin(OLD/NAMES[1]),host_candidate_pin=copies[1]['candidate_pin'],host_changes=hc,child_predecessor_pin=pin(OLD/NAMES[0]),child_candidate_pin=copies[0]['candidate_pin'],child_changes=cc,writer_predecessor_pin=pin(OLD/'write_once_GENDF_cumulative_ten_roots_SF_HF_recipe.py'),writer_candidate_pin=wp,writer_changes=wc,host_original_whole_bytes_base64=base64.b64encode(host0.encode()).decode(),child_original_whole_bytes_base64=base64.b64encode(child0.encode()).decode(),writer_original_whole_bytes_base64=base64.b64encode(writer0.encode()).decode(),publication_source_mapping=mapping,all_three_whole_file_inverse_byte_equal=True,all_scientific_parser_math_threshold_functions_whole_bytes_unchanged=True,original_caps_unchanged=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
    current_rows=copy.deepcopy(loaded_sf['complete_source_file_pins'])
    for row in mapping:
        index=current_rows.index(row['predecessor_pin']);current_rows[index]=row['candidate_pin']
    plan.update(schema='GENDF_ACTUAL_COMPLETE_CUMULATIVE_SEVENTEEN_ROOTS_EXACT_PUBLICATION_SOURCE_PLAN_V1',Source_author_pin=pin(__file__),predecessor_v10_plan_pin=previous_plan_pin,source_copies=copies,publication_source_mapping=mapping,complete_source_file_pins=current_rows,candidate_host_source_pin=copies[1]['candidate_pin'],cumulative_artifact_root_paths=artifact,cumulative_Source_root_paths=source,complete_cumulative_seventeen_role_roots=roots,original_five_role_roots_preserved=[artifact[0],artifact[1],artifact[2],source[0],source[1]],planned_actual_output_root=str(output),planned_actual_evidence_root=str(evidence),complete_scoped_byte_inverse_pin=inv,complete_cumulative_ART_role_count=10,complete_cumulative_Source_request_role_count=7,cumulative_explicit_metadata_file_pins=metadata,explicit_metadata_file_bytes=sum(p['size_bytes']for p in metadata),original_v10_published_metadata_pins=published,source_only=True,candidate_executed=False,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,physics_qualified=False)
    plan['selected_closed_current_authority_pins']+=published+metadata+[previous_plan_pin]
    plan['retained_actual_capture_owner_root']=capture_owner
    plan['retained_actual_capture_owner_authority_pin']=closure_rows[0]
    plan['predecessor_cumulative_sixteen_role_roots']=plan['complete_cumulative_sixteen_role_roots']
    plan['complete_cumulative_sixteen_role_roots']=roots
    plan['complete_cumulative_ten_role_roots']=roots
    pp=write(OUT/'CURRENT_ELEVEN_GENDF_HOST_SOURCE_PREPARATION_PLAN.json',plan)
    ready=dict(schema='GENDF_ACTUAL_CUMULATIVE17_EXACT_MAPPING_CANDIDATE_WRITER_SOURCE_READY_V1',source_only=True,plan_pin=pp,complete_inverse_pin=inv,writer_source_pin=wp,selected_Source_pins=[row['candidate_pin']for row in copies]+[pp,inv,wp],actual_aggregation_report_pin=plan['actual_aggregation_report_pin'],actual_GENDF_report_pin=None,future_Source_freeze_pin=None,future_Host_freeze_pin=None,future_recipe_pin=None,original_Host_argv_count=32,original_metadata_builder_argv_count=18,once_writer_required_fullpin_role_count=8,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,physics_qualified=False)
    rp=write(OUT/'SOURCE_REVIEW_READY.json',ready)
    fd=os.open(OUT,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)
    print(json.dumps(dict(status='GENDF_CUMULATIVE17_EXACT_MAPPING_SOURCE_ONLY_READY_NOT_PUBLISHED',ready_pin=rp,plan_pin=pp,inverse_pin=inv,writer_source_pin=wp,Source_author_pin=pin(__file__),actual_GENDF_report_pin=None,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)))
if __name__=='__main__':main()
