"""Resource metadata only: retain actual GENDF and the current OVERV control roots."""
import ast,base64,copy,hashlib,json,os,shlex,stat
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=REC/'current_material_evidence_compare_three_exact_historical_terminal_schema_source_v6_20261014'
NEW=REC/'current_material_evidence_compare_three_after_GENDF_cumulative_resources_source_v7_20261014'
GF=REC/'current_eleven_saved_gendf_actual_cumulative_seventeen_roots_host_source_v11_20261014'
ART=Path('/Users/wen/spot/validation/artifacts')
def require(ok,text):
 if not ok:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat();require(p.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_size<64*2**20 and not any(a.is_symlink()for a in(p,*p.parents)),'ordinary bounded Source/metadata')
 with p.open('rb')as f:b=f.read()
 require(identity(p.lstat())==identity(s),'current7');return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=identity(s))
def read(p):
 require(pin(p['path'])==p,'exact selected metadata PF');return json.loads(Path(p['path']).read_bytes())
def write(p,v):
 b=v if type(v)is bytes else(json.dumps(v,indent=2,allow_nan=False)+'\n').encode()
 with p.open('xb')as f:f.write(b);f.flush();os.fsync(f.fileno())
 return pin(p)
def splice(s,a,b,changes):
 require(s.count(a)==1,'one exact resource metadata splice');changes.append(dict(before=a,after=b));return s.replace(a,b,1)
def inverse(candidate,original,changes):
 for c in reversed(changes):
  require(candidate.count(c['after'])==1,'one exact inverse');candidate=candidate.replace(c['after'],c['before'],1)
 require(candidate==original,'complete original file inverse')
def union(rows):
 out=[]
 for row in rows:
  if row not in out:out.append(row)
 return out
def main():
 require(not NEW.exists(),'fresh Source-only namespace')
 ready0=read(pin(OLD/'SOURCE_REVIEW_READY.json'));plan=read(ready0['plan_pin'])
 sfpin=pin(GF/'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json');gfsf=read(sfpin)
 hfp=pin(GF/'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json');dynpin=pin(GF/'ROOT_REVIEWABLE_CURRENT_GENDF_V4_CLI_SOURCE_ONLY.json')
 rootpin=pin(REC/'ROOT_ACTUAL_GENDF_CUMULATIVE17_ACTUAL32_TRUE_TOOL_RETURNS_20261014.json');root=read(rootpin)
 argvpin=pin(REC/'ROOT_EXACT_GENDF_CUMULATIVE17_ACTUAL32_ARGV_20261014.json');argv=read(argvpin)
 terminal=root['actual_terminal_return'];require(type(terminal['exit_code'])is int and terminal['exit_code']==0 and terminal.get('session_id')is None and root['observed_closed']is True and type(root['original_integer_exit_code'])is int and root['original_integer_exit_code']==0 and shlex.split(root['exact_executed_command'])==argv['argv']and len(argv['argv'])==32,'actual GENDF Root closed0 exact32')
 reportpin=pin(Path(gfsf['cumulative_artifact_root_paths'][0])/'Root_actual_eleven_saved_gendf_extraction_summary.json');report=read(reportpin)
 require(report['schema']=='ACTUAL_CURRENT_ELEVEN_NONZERO_NX_SAVED_GENDF_GUARDED_ROOT_V1'and report['status']=='ACTUAL_ELEVEN_SAVED_MT5_EXTRACTION_CLOSED0_ONLY'and report['failure']is None and report['after_check_error']is None and len(report['records'])==1 and report['records'][0]['status']=='PASS'and report['source_freeze_pin']==sfpin,'actual one closed GENDF evidence stage, no physics qualification')
 childpin=report['actual_child_receipt']['report'];require(Path(childpin['path']).parent==Path(gfsf['cumulative_artifact_root_paths'][1]),'exact actual GF child root')
 gfroots=gfsf['cumulative_artifact_root_paths'][:3]+gfsf['cumulative_Source_root_paths']+gfsf['cumulative_artifact_root_paths'][3:]
 require(len(gfroots)==len(set(gfroots))==17 and len(gfsf['cumulative_explicit_metadata_file_pins'])==2,'actual GF17 and explicit two metadata file roles')
 controlplanpin=pin(REC/'OVERV_original_guarded_integer_control_source_v3_20261014/PLAN.json');controlplan=read(controlplanpin)
 retained=union(gfroots+controlplan['cumulative_joint_roots']+[str(OLD)])
 explicit=gfsf['cumulative_explicit_metadata_file_pins']+[argvpin,rootpin]
 require(len({p['path']for p in explicit})==4,'two existing GF metadata roles plus two actual Root protocol files')
 for p in explicit:require(identity(Path(p['path']).lstat())==p['identity'],'explicit metadata current7')
 b0=Path(ready0['builder_source_pin']['path']).read_text();b=b0;bc=[]
 b=splice(b,'joint_archive_roots=roots,request_preparation_only=True,','joint_archive_roots=roots,explicit_cumulative_metadata_file_pins=[],request_preparation_only=True,',bc)
 old="    target=root/'CURRENT_ACTUAL_MATERIAL_EVIDENCE_REQUEST.json';write(target,request)"
 new="""    if args.operation=='compare-three':
        request['original_compare_sixteen_role_roots']=list(request['joint_archive_roots'])
        for retained in sf['retained_actual_GENDF_and_control_joint_roots']:
            if retained not in request['joint_archive_roots']:request['joint_archive_roots'].append(retained)
        require(len(request['joint_archive_roots'])==len(set(request['joint_archive_roots']))and
          not any(Path(a).is_relative_to(Path(b))for a in request['joint_archive_roots']for b in request['joint_archive_roots']if a!=b),
          'original compare16 plus all retained actual GENDF and current control roles, one unchanged2GiB')
        request['explicit_cumulative_metadata_file_pins']=sf['retained_actual_GENDF_explicit_metadata_file_pins']
        request['retained_actual_GENDF_resource_authority_pins']=sf['retained_actual_GENDF_resource_authority_pins']
        request['complete_input_pins']=unique(request['complete_input_pins']+
          sf['retained_actual_GENDF_current_dependency_pins']+request['explicit_cumulative_metadata_file_pins'])
    target=root/'CURRENT_ACTUAL_MATERIAL_EVIDENCE_REQUEST.json';write(target,request)"""
 b=splice(b,old,new,bc)
 h0=Path(ready0['host_source_pin']['path']).read_text();h=h0;hc=[]
 h=splice(h,'    class Resources:\n',"    explicit_metadata=request['explicit_cumulative_metadata_file_pins']\n    class Resources:\n",hc)
 h=splice(h,"            return dict(original_history_cold_free=oldresources.check(),complete_joint_five_root_fresh=joined.check())","""            history=oldresources.check();fresh=joined.check();extra=0;nodes=set()
            for expected in explicit_metadata:
                path=Path(expected['path']);item=path.lstat()
                fields=[item.st_dev,item.st_ino,item.st_mode,item.st_nlink,item.st_size,item.st_mtime_ns,item.st_ctime_ns]
                if fields!=expected['identity']or expected['size_bytes']!=item.st_size or not stat.S_ISREG(item.st_mode)or item.st_nlink!=1 or item.st_uid!=os.getuid()or any(a.is_symlink()for a in(path,*path.parents)):
                    raise RuntimeError('exact ordinary explicit metadata current7/no aliases')
                node=(item.st_dev,item.st_ino)
                if node in nodes:raise RuntimeError('distinct explicit metadata nodes')
                nodes.add(node)
                if not any(path.is_relative_to(Path(root))for root in roots):extra+=item.st_size
            if fresh['artifact_bytes']+extra>=2*2**30:raise RuntimeError('unchanged cumulative joint2GiB including exact metadata files outside roots')
            return dict(original_history_cold_free=history,complete_joint_five_root_fresh=fresh,
              explicit_metadata_files=explicit_metadata,explicit_external_metadata_bytes=extra,
              complete_joint_roots_plus_metadata_bytes=fresh['artifact_bytes']+extra)""",hc)
 h=splice(h,'import shutil\n','import shutil\nimport stat\n',hc)
 c0=Path(ready0['scientific_child_source_pin']['path']).read_text();c=c0;cc=[]
 c=splice(c,'    def __init__(self,roots):\n','    def __init__(self,roots,explicit_metadata):\n        require(type(explicit_metadata)is list,\'explicit metadata roles required\');self.explicit_metadata=explicit_metadata\n',cc)
 c=splice(c,'        unlinked={}\n',"""        nodes=set()
        for expected in self.explicit_metadata:
            require(type(expected)is dict and set(expected)=={'path','sha256','size_bytes','identity'},'exact explicit metadata fullPF')
            p=Path(expected['path']);s=p.lstat()
            require(p.is_absolute()and not any(a.is_symlink()for a in(p,*p.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid()and identity(s)==expected['identity']and s.st_size==expected['size_bytes'],'ordinary explicit metadata current7/no aliases')
            node=(s.st_dev,s.st_ino);require(node not in nodes,'distinct explicit metadata nodes');nodes.add(node)
            if not any(p.is_relative_to(root)for root in self.roots):total+=s.st_size
        unlinked={}
""",cc)
 c=splice(c,"budget=Budget(request['joint_archive_roots']);","budget=Budget(request['joint_archive_roots'],request['explicit_cumulative_metadata_file_pins']);",cc)
 for s in(b,h,c):ast.parse(s)
 for current,original,changes in[(b,b0,bc),(h,h0,hc),(c,c0,cc)]:inverse(current,original,changes)
 NEW.mkdir();copies=[];sources=[]
 for original in plan['complete_source_file_pins_candidate']:
  path=Path(original['path'])
  if path.parent==OLD:
   raw=b.encode()if path.name=='prepare_current_material_evidence_requests.py'else h.encode()if path.name=='run_current_material_lineage_evidence.py'else c.encode()if path.name=='current_material_lineage_evidence.py'else path.read_bytes()
   candidate=write(NEW/path.name,raw);copies.append(dict(predecessor_pin=original,candidate_pin=candidate,whole_bytes_unchanged=original['sha256']==candidate['sha256']));sources.append(candidate)
  else:sources.append(original)
 bp=write(NEW/Path(ready0['split_binder_source_pin']['path']).name,Path(ready0['split_binder_source_pin']['path']).read_bytes());copies.append(dict(predecessor_pin=ready0['split_binder_source_pin'],candidate_pin=bp,whole_bytes_unchanged=True))
 w0=Path(ready0['writer_source_pin']['path']).read_text();w=w0;wc=[]
 old="retained_corrected_aggregation_joint_archive_roots=plan['retained_corrected_aggregation_joint_archive_roots'],candidate_executed=False"
 new="retained_corrected_aggregation_joint_archive_roots=plan['retained_corrected_aggregation_joint_archive_roots'],retained_actual_GENDF_and_control_joint_roots=plan['retained_actual_GENDF_and_control_joint_roots'],retained_actual_GENDF_explicit_metadata_file_pins=plan['retained_actual_GENDF_explicit_metadata_file_pins'],retained_actual_GENDF_resource_authority_pins=plan['retained_actual_GENDF_resource_authority_pins'],retained_actual_GENDF_current_dependency_pins=plan['retained_actual_GENDF_current_dependency_pins'],candidate_executed=False"
 w=splice(w,old,new,wc)
 w=splice(w,"phase['output_pins']+plan['projection_current_live_pins']","phase['output_pins']+plan['retained_actual_GENDF_current_dependency_pins']+plan['projection_current_live_pins']",wc)
 ast.parse(w);inverse(w,w0,wc);wp=write(NEW/Path(ready0['writer_source_pin']['path']).name,w.encode())
 ip=write(NEW/'COMPLETE_COMPARE_V6_TO_V7_ACTUAL_GENDF_CUMULATIVE_RESOURCE_WHOLE_BYTE_INVERSE.json',dict(schema='COMPLETE_COMPARE_V6_TO_V7_ACTUAL_GENDF_CUMULATIVE_RESOURCE_WHOLE_BYTE_INVERSE_V1',source_only=True,original_builder_whole_bytes_base64=base64.b64encode(b0.encode()).decode(),builder_changes=bc,original_host_whole_bytes_base64=base64.b64encode(h0.encode()).decode(),host_changes=hc,original_child_whole_bytes_base64=base64.b64encode(c0.encode()).decode(),child_changes=cc,original_writer_whole_bytes_base64=base64.b64encode(w0.encode()).decode(),writer_changes=wc,source_copies=copies,all_four_whole_file_inverses_byte_equal=True,all_three_exact_historical_producer_terminal_contracts_unchanged=True,all_scientific_functions_math_Fortran_thresholds_whole_bytes_unchanged=True,all_original_caps_and_resource_classes_unchanged=True,actual_GENDF_independent_post_pin=None,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 authority=[sfpin,hfp,dynpin,reportpin,childpin,rootpin,argvpin,controlplanpin]+explicit
 deps=authority+report['fixed_current_pins']+report['complete_output_pins']
 candidate_root=ART/'axial-material-current-first-A-compare-three-after-GENDF-cumulative-20261014-v1';requestroot=REC/'first_A_compare_three_after_GENDF_cumulative_request_20261014_v1'
 priorroots=plan['retained_corrected_aggregation_joint_archive_roots'];closure=read(report['actual_material_observation_report_pin'])
 own8=[str(candidate_root),str(candidate_root.with_name(candidate_root.name+'-evidence')),str(Path(closure['actual_prior_A_cwd']).parent),str(NEW),str(requestroot),str(Path(report['actual_material_observation_report_pin']['path']).parent)]
 extracthost=read(plan['retained_current_corrected_aggregation_report_pin']);er=next(p for p in extracthost['fixed_current_pins']if p['path'].endswith('/Root_actual_current_material_evidence_summary.json')and 'fullfield-extract-six-roots' in p['path']);extractreport=read(er);own8+=[str(Path(er['path']).parent),str(Path(extractreport['actual_complete_child_receipt']['report']['path']).parent)]
 original16=union(own8+priorroots);require(len(original16)==16,'actual original compare16 roles')
 total=union(original16+retained);require(not any(Path(a).is_relative_to(Path(b))for a in total for b in total if a!=b),'all cumulative root paths disjoint')
 plan.update(schema='COMPARE_THREE_AFTER_ACTUAL_GENDF_CUMULATIVE_RESOURCE_SOURCE_ONLY_PLAN_V1',source_only=True,predecessor_v6_plan_pin=ready0['plan_pin'],complete_source_file_pins_candidate=sources,source_copies=copies,complete_byte_inverse_pin=ip,candidate_scientific_child_pin=pin(NEW/'current_material_lineage_evidence.py'),retained_actual_GENDF_and_control_joint_roots=retained,retained_actual_GENDF_explicit_metadata_file_pins=explicit,retained_actual_GENDF_resource_authority_pins=authority,retained_actual_GENDF_current_dependency_pins=deps,original_compare_sixteen_root_projection=original16,planned_complete_cumulative_compare_roots=total,planned_cumulative_compare_three_root_count=len(total),planned_actual_output_root=str(candidate_root),planned_actual_request_root=str(requestroot),actual_GENDF_independent_post_pin=None,actual_OVERV_control_report_pin=None,actual_compare_three_report_pin=None,actual_request_pin=None,future_Source_freeze_pin=None,future_Host_freeze_pin=None,future_dynamic_interface_pin=None,physics_qualified=False)
 pp=write(NEW/'COMPARE_THREE_EXACT_CURRENT_PROJECTION_SOURCE_PLAN.json',plan);ready=copy.deepcopy(ready0)
 for key in('host_source_pin','builder_source_pin','scientific_child_source_pin','split_binder_source_pin','aggregation_engine_source_pin'):ready[key]=pin(NEW/Path(ready0[key]['path']).name)
 ready.update(schema='COMPARE_THREE_AFTER_ACTUAL_GENDF_CUMULATIVE_RESOURCE_SOURCE_ONLY_READY_V1',plan_pin=pp,inverse_pin=ip,writer_source_pin=wp,Source_author_pin=pin(__file__),actual_compare_three_report_pin=None,actual_request_pin=None,planned_cumulative_joint_root_count=len(total),actual_GENDF_independent_post_pin=None,actual_OVERV_control_report_pin=None)
 rp=write(NEW/'SOURCE_REVIEW_READY.json',ready);fd=os.open(NEW,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='COMPARE_AFTER_ACTUAL_GENDF_CUMULATIVE_RESOURCE_SOURCE_ONLY_READY_NOT_PUBLISHED',ready_pin=rp,plan_pin=pp,inverse_pin=ip,writer_source_pin=wp,Source_author_pin=pin(__file__),planned_cumulative_joint_root_count=len(total),explicit_cumulative_metadata_file_count=len(explicit),actual_GENDF_independent_post_pin=None,actual_OVERV_control_report_pin=None,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
