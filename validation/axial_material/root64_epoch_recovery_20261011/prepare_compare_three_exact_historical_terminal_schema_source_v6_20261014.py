"""Exact three historical producer metadata schemas; no scientific execution."""
import ast,base64,copy,hashlib,json,os,stat
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=REC/'current_material_evidence_compare_three_exact_current_projection_source_v5_20261014'
NEW=REC/'current_material_evidence_compare_three_exact_historical_terminal_schema_source_v6_20261014'
def require(ok,text):
 if not ok:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat();require(s.st_size<64*2**20 and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and not any(a.is_symlink()for a in(p,*p.parents)),'bounded ordinary Source/metadata')
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  require(identity(os.fstat(f.fileno()))==identity(s),'open7');h=hashlib.file_digest(f,'sha256').hexdigest();require(identity(os.fstat(f.fileno()))==identity(s),'EOF7')
 require(identity(p.lstat())==identity(s),'current7');return dict(path=str(p),sha256=h,size_bytes=s.st_size,identity=identity(s))
def read(p):
 require(pin(p['path'])==p,'exact selected metadata PF');return json.loads(Path(p['path']).read_bytes())
def write(p,v):
 raw=v if type(v)is bytes else(json.dumps(v,indent=2,allow_nan=False)+'\n').encode()
 with p.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 return pin(p)
def splice(text,before,after,changes):
 require(text.count(before)==1,'one exact schema metadata splice');changes.append(dict(before=before,after=after));return text.replace(before,after,1)
def back(candidate,original,changes):
 for c in reversed(changes):
  require(candidate.count(c['after'])==1,'one complete inverse splice');candidate=candidate.replace(c['after'],c['before'],1)
 require(candidate==original,'whole original file inverse')
def main():
 require(not NEW.exists(),'fresh Source-only namespace')
 oldready=read(pin(OLD/'SOURCE_REVIEW_READY.json'));plan=read(oldready['plan_pin']);formal=read(oldready['current_formal_plan_pin'])
 schemas=('ACTUAL_CURRENT_SINGLE_PLANE_WARM_A_NATIVE_PRODUCER_ROOT_V1','ACTUAL_CURRENT_SINGLE_PLANE_WARM_A2_NATIVE_PRODUCER_ROOT_V1','ACTUAL_CURRENT_SINGLE_PLANE_WARM_A3_NATIVE_PRODUCER_ROOT_V1')
 contracts=[]
 for row,wanted in zip(formal['producers'],schemas):
  report=read(row['report']);require(report['schema']==wanted and 'after_check_error'not in report and report['failure']is None and len(report['records'])==4 and all(r['status']=='PASS'for r in report['records'])and report['actual_native_terminal']==row['native_readback'],'exact immutable three historical terminal schemas and absence fact')
  contracts.append(dict(actual_original_report_pin=row['report'],actual_original_schema=wanted,after_check_error_field_present=False))
 require(len(contracts)==3,'three exact reports only')
 pairs=repr(tuple((r['actual_original_report_pin'],r['actual_original_schema'])for r in contracts))
 builder0=Path(oldready['builder_source_pin']['path']).read_text();builder=builder0;bc=[]
 original="                require(len(report['records'])==4 and report['failure']is None and report['after_check_error']is None and\n"
 candidate="                require((row['report'],report['schema'])in "+pairs+" and 'after_check_error'not in report,\n                  'exact original producer fullPF/schema retains historically absent after_check_error')\n                require(len(report['records'])==4 and report['failure']is None and\n"
 builder=splice(builder,original,candidate,bc)
 child0=Path(oldready['scientific_child_source_pin']['path']).read_text();child=child0;cc=[]
 original="    require(value['failure']is None and value['after_check_error']is None,'actual producer host terminal')"
 candidate="    historical_terminal=(report_pin,value['schema'])in "+pairs+"\n    if historical_terminal:\n        require('after_check_error'not in value,'exact historical producer terminal field absence, never invented None')\n    else:\n        require(value['after_check_error']is None,'actual producer host after-check terminal')\n    require(value['failure']is None,'actual producer host terminal')"
 child=splice(child,original,candidate,cc)
 for s in(builder,child):ast.parse(s)
 back(builder,builder0,bc);back(child,child0,cc)
 NEW.mkdir();copies=[];sources=[]
 for before in plan['complete_source_file_pins_candidate']:
  path=Path(before['path'])
  if path.parent==OLD:
   require(pin(path)==before,'current original Source PF')
   raw=builder.encode()if path.name=='prepare_current_material_evidence_requests.py'else child.encode()if path.name=='current_material_lineage_evidence.py'else path.read_bytes()
   after=write(NEW/path.name,raw);copies.append(dict(predecessor_pin=before,candidate_pin=after,whole_bytes_unchanged=before['sha256']==after['sha256']));sources.append(after)
  else:sources.append(before)
 binder_before=oldready['split_binder_source_pin'];bp=write(NEW/Path(binder_before['path']).name,Path(binder_before['path']).read_bytes());copies.append(dict(predecessor_pin=binder_before,candidate_pin=bp,whole_bytes_unchanged=True))
 fp=write(NEW/Path(oldready['current_formal_plan_pin']['path']).name,Path(oldready['current_formal_plan_pin']['path']).read_bytes())
 projection=read(oldready['current_producer_projection_pin']);projection['current_formal_plan_pin']=fp
 projection_pin=write(NEW/Path(oldready['current_producer_projection_pin']['path']).name,projection)
 childpin=pin(NEW/'current_material_lineage_evidence.py')
 writer0=Path(oldready['writer_source_pin']['path']).read_text();writer=writer0;wc=[]
 a="require(next(p for p in source if Path(p['path']).name=='current_material_lineage_evidence.py')['sha256']=='e921ad84a4b1241827b24d1c3a7fc8e06710098e9fd34bde4e3bd5eec2d10d4d','whole scientific child unchanged')"
 b="require(next(p for p in source if Path(p['path']).name=='current_material_lineage_evidence.py')==plan['candidate_scientific_child_pin'],'exact child only historical-terminal metadata admission delta')"
 writer=splice(writer,a,b,wc)
 ast.parse(writer);back(writer,writer0,wc)
 wp=write(NEW/Path(oldready['writer_source_pin']['path']).name,writer.encode())
 inverse=write(NEW/'COMPLETE_COMPARE_V5_TO_V6_EXACT_HISTORICAL_TERMINAL_SOURCE_BYTE_INVERSE.json',dict(schema='COMPLETE_COMPARE_V5_TO_V6_EXACT_HISTORICAL_TERMINAL_SOURCE_BYTE_INVERSE_V1',source_only=True,original_builder_whole_bytes_base64=base64.b64encode(builder0.encode()).decode(),builder_changes=bc,original_child_whole_bytes_base64=base64.b64encode(child0.encode()).decode(),child_changes=cc,original_writer_whole_bytes_base64=base64.b64encode(writer0.encode()).decode(),writer_changes=wc,source_copies=copies,exact_historical_producer_terminal_contracts=contracts,all_three_whole_file_inverses_byte_equal=True,all_other_child_scientific_methods_and_math_Fortran_thresholds_whole_bytes_unchanged=True,original_owning_stage_records_watch_log_caps_and_native_terminal_checks_preserved=True,original_reports_not_modified=True,no_generic_optional_field_or_missing_skip=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 replace={oldready['current_formal_plan_pin']['path']:fp,oldready['current_producer_projection_pin']['path']:projection_pin}
 plan['projection_metadata_authority_pins']=[replace.get(p['path'],p)for p in plan['projection_metadata_authority_pins']]
 plan.update(schema='COMPARE_THREE_EXACT_HISTORICAL_TERMINAL_SOURCE_ONLY_PLAN_V1',source_only=True,predecessor_v5_plan_pin=oldready['plan_pin'],complete_source_file_pins_candidate=sources,source_copies=copies,complete_byte_inverse_pin=inverse,current_formal_plan_pin=fp,current_producer_projection_pin=projection_pin,candidate_scientific_child_pin=childpin,exact_historical_producer_terminal_contracts=contracts,actual_compare_three_report_pin=None,actual_request_pin=None,all_runtime_source_bytes_unchanged=False,only_builder_and_owning_stage_exact_historical_metadata_admission_changed=True,future_Source_freeze_pin=None,future_Host_freeze_pin=None,future_dynamic_interface_pin=None,physics_qualified=False)
 pp=write(NEW/'COMPARE_THREE_EXACT_CURRENT_PROJECTION_SOURCE_PLAN.json',plan)
 ready=copy.deepcopy(oldready)
 for key in('host_source_pin','builder_source_pin','scientific_child_source_pin','split_binder_source_pin','aggregation_engine_source_pin'):
  ready[key]=pin(NEW/Path(oldready[key]['path']).name)
 ready.update(schema='COMPARE_THREE_EXACT_HISTORICAL_TERMINAL_SOURCE_ONLY_READY_V1',Source_author_pin=pin(__file__),current_formal_plan_pin=fp,current_producer_projection_pin=projection_pin,plan_pin=pp,inverse_pin=inverse,writer_source_pin=wp,actual_compare_three_report_pin=None,actual_request_pin=None)
 rp=write(NEW/'SOURCE_REVIEW_READY.json',ready)
 fd=os.open(NEW,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='COMPARE_V6_EXACT_HISTORICAL_TERMINAL_SOURCE_ONLY_READY_NOT_PUBLISHED',ready_pin=rp,plan_pin=pp,inverse_pin=inverse,writer_source_pin=wp,Source_author_pin=pin(__file__),actual_compare_three_report_pin=None,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
