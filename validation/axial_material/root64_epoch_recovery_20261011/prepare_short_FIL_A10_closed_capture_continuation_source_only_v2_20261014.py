"""Unique continuation Source v2: exact labelled mirrors, bound lsof, explicit full-family after snapshot."""
import ast,hashlib,json,os
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011');OLD=R/'current_formal_short_FIL_A10_closed_capture_continuation_source_v1_20261014';OUT=R/'current_formal_short_FIL_A10_closed_capture_continuation_source_v2_20261014'
HOST='complete_closed_short_FIL_A10_capture_and_release.py';WRITER='write_once_closed_A10_continuation_HF_CLI.py'
def pin(p):
 p=Path(p);s=p.stat();return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),size_bytes=s.st_size,identity=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns])
def write(p,v):
 raw=v.encode()if isinstance(v,str)else(json.dumps(v,indent=2,allow_nan=False)+'\n').encode()
 with p.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 return pin(p)
def main():
 if OUT.exists():raise RuntimeError('unique Source v2')
 a=(OLD/HOST).read_text();z=a;changes=[]
 def change(old,new):
  nonlocal z
  if z.count(old)!=1:raise RuntimeError('one exact Source block '+old)
  z=z.replace(old,new,1);changes.append(dict(before=old,after=new))
 change("fixed=list(d['fixed_current_pins']);lsof=c.pin('/usr/sbin/lsof');require", "fixed=list(d['fixed_current_pins']);lsof=hf['selected_actual_lsof_tool_pin'];c.same_pin(lsof['path'],lsof);require")
 change('check_current();out.mkdir();newwatch=[]','check_current();out.mkdir();(out/\'A\').mkdir();newwatch=[];mirror_fullpins=[]')
 change('target=out/oldpath.name',"target=out/(records[0]['label']+suffix)")
 change("if suffix=='.watchdog.json':newwatch.append(dict(path=pp['path'],sha256=pp['sha256']))","mirror_fullpins.append(pp)\n        if suffix=='.watchdog.json':newwatch.append(pp)")
 change('release_receipt=None;failure=None;first=None;tb=None;after=None','release_receipt=None;failure=None;first=None;tb=None;after=None;full_after=None')
 change("require(after['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,'after exact release original real fullfresh2 reserve')","full_after=history.check()\n        require(full_after['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,'after exact release original real fullfresh2 reserve')")
 change("output_pins=outputs_original+[fullpin(p,budget)for p in out.iterdir()if p.is_file()]","output_pins=outputs_original+mirror_fullpins")
 change('resources_before=before,resources_after=after,actual_full_A_observation_executed','resources_before=before,resources_after=after,resources_after_full_family=full_after,actual_full_A_observation_executed')
 ast.parse(z)
 wa=(OLD/WRITER).read_text();wz=wa.replace('closed-capture-continuation-20261014-v1','closed-capture-continuation-20261014-v2')
 old="for p in oldhf['dependencies']+phase['fixed_current_pins']+phase['output_pins']+own+list(pins.values())+[original_phase,oldhfpin,oldclipin,post['actual_Root_true_tool_return_pin'],post['actual_Root_argv_pin'],pin('/usr/sbin/lsof')]:add(p)"
 new="lsof=plan['selected_actual_lsof_tool_pin'];require(pin(lsof['path'])==lsof and contains(peer,lsof),'same-round exact lsof Source/current pin')\n for p in oldhf['dependencies']+phase['fixed_current_pins']+phase['output_pins']+own+list(pins.values())+[original_phase,oldhfpin,oldclipin,post['actual_Root_true_tool_return_pin'],post['actual_Root_argv_pin'],lsof]:add(p)"
 if wz.count(old)!=1:raise RuntimeError('one Source-bound lsof publication insertion')
 wz=wz.replace(old,new,1)
 old="selected_original_CLI_pin=oldclipin,same_round_independent_Source_review_pin=";new="selected_original_CLI_pin=oldclipin,selected_actual_lsof_tool_pin=lsof,same_round_independent_Source_review_pin="
 if wz.count(old)!=1:raise RuntimeError('one exact HF lsof binding')
 wz=wz.replace(old,new,1);ast.parse(wz)
 funcs=lambda s:{n.name:ast.get_source_segment(s,n)for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)}
 for name,body in funcs(a).items():
  if name!='main'and funcs(z)[name]!=body:raise RuntimeError('all original nonmain functions wholebytes')
 OUT.mkdir();hp=write(OUT/HOST,z);cp=write(OUT/'current_material_prerequisite_admission.py',(OLD/'current_material_prerequisite_admission.py').read_text());wp=write(OUT/WRITER,wz)
 entries=[]
 for name,before,after,cs in [(HOST,a,z,changes),(WRITER,wa,wz,[dict(before=wa,after=wz)])]:
  back=after
  for c in reversed(cs):
   if back.count(c['after'])!=1:raise RuntimeError('unique complete inverse')
   back=back.replace(c['after'],c['before'],1)
  if back.encode()!=before.encode():raise RuntimeError('whole inverse')
  entries.append(dict(predecessor_pin=pin(OLD/name),candidate_pin=pin(OUT/name),changes=cs,whole_file_inverse_byte_equal=True))
 iv=write(OUT/'COMPLETE_SHORT_FIL_A10_CONTINUATION_V1_TO_V2_WHOLE_BYTE_INVERSE.json',dict(schema='COMPLETE_SHORT_FIL_A10_CONTINUATION_V1_TO_V2_WHOLE_BYTE_INVERSE_V1',entries=entries,predecessor_main_inverse_pin=pin(OLD/'COMPLETE_SHORT_FIL_A10_CONTINUATION_WHOLE_MAIN_BYTE_INVERSE.json'),all_original_nonmain_collect_release_functions_wholebytes_equal=True,Source_only=True))
 plan=json.loads((OLD/'CONTINUATION_SOURCE_PLAN.json').read_bytes());plan.update(source_revision=2,host_source_pin=hp,helper_source_pin=cp,inverse_pin=iv,predecessor_plan_pin=pin(OLD/'CONTINUATION_SOURCE_PLAN.json'),selected_actual_lsof_tool_pin=pin('/usr/sbin/lsof'),explicit_labelled_mirror_paths=['A/material.log','A/material.watchdog.json'],mirror_output_fullpins_exact_count=2,watch_authority_is_complete_new_fullPF=True,fullfresh2_after_uses_direct_original_full_family_history_snapshot=True,future_actual_completion_output_root='/Users/wen/spot/validation/artifacts/axial-material-current-formal-material-short-FIL-A10-closed-capture-continuation-20261014-v2')
 pp=write(OUT/'CONTINUATION_SOURCE_PLAN.json',plan);ready=write(OUT/'SOURCE_REVIEW_READY.json',dict(schema='SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_SOURCE_ONLY_READY_V1',source_revision=2,host_source_pin=hp,helper_source_pin=cp,plan_pin=pp,inverse_pin=iv,writer_source_pin=wp,Source_author_pin=pin(__file__),predecessor_ready_pin=pin(OLD/'SOURCE_REVIEW_READY.json'),selected_actual_lsof_tool_pin=plan['selected_actual_lsof_tool_pin'],future_actual_own_HF_pin=None,future_actual_own_CLI_pin=None,future_actual_completion_report_pin=None,future_actual_release_pin=None,Source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 fd=os.open(OUT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='CLOSED_A10_CONTINUATION_V2_CANDIDATE_AND_WRITER_SOURCE_ONLY_READY',host_source_pin=hp,helper_source_pin=cp,plan_pin=pp,inverse_pin=iv,writer_source_pin=wp,ready_pin=ready,Source_author_pin=pin(__file__),selected_actual_lsof_tool_pin=plan['selected_actual_lsof_tool_pin'],business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
