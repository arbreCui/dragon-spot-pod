"""UNREADY owning Root host for fresh B55 native/integer OVERV controls."""
import argparse,hashlib,importlib.util,json,os,resource,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent
def need(v,m):
 if v is not True:raise RuntimeError(m)
def frozen_arg(a,role):
 n=role.replace('-','_');ids=json.loads(getattr(a,n+'_seven_id'));q=Path(getattr(a,n+'_summary'));s=q.lstat();p=dict(path=str(q),sha256=getattr(a,n+'_sha256'),size_bytes=ids[4],identity=ids)
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==ids and s.st_size<8*2**20,'exact freeze current7')
 raw=q.read_bytes();need(hashlib.sha256(raw).hexdigest()==p['sha256'],'whole freeze SHA');return json.loads(raw),p
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('source-freeze','host-freeze'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 a=ap.parse_args();start=time.monotonic()
 with(BASE/'ROOT_EXECUTION_CLAIM_RECEIPT.json').open('x')as f:json.dump(dict(schema='ROOT_EXCLUSIVE_CURRENT_B55_OVERV_CONTROL_CLAIM_V1',Root_PID=os.getpid(),original_monotonic_start=start,argv=sys.argv,claim_before_metadata_EOF_project_import_or_SQL=True),f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 sf,psf=frozen_arg(a,'source-freeze');hf,phf=frozen_arg(a,'host-freeze');cp=hf['contract_Source_pin']
 need(Path(cp['path'])==BASE/'B55_owning_Source_contract.UNREADY.py'and hashlib.sha256(Path(cp['path']).read_bytes()).hexdigest()==cp['sha256'],'exact frozen owning contract')
 spec=importlib.util.spec_from_file_location('current_B55_owning_contract',cp['path']);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.current(cp)
 need(sf['schema']=='CURRENT_B55_OVERV_CONTROL_SOURCE_ONLY_FREEZE_V1'and sf['source_only']is True and sf['compiler_executed']is False and hf['schema']=='CURRENT_B55_OVERV_CONTROL_HOST_FREEZE_V1'and hf['selected_source_freeze_pin']==psf and hf['host_source_pin']['path']==str(Path(__file__).absolute())and hf['original_caps']==m.CAPS,'exact fresh current B55 Source-only publication')
 plan=m.metadata(sf['control_plan_pin']);build,bm,descriptor,selected,bridge,capture_binding,latest=m.admit(plan);out=m.OUT
 c=m.source(plan['original_Common_Source_pin'],'B55_original_common');support=m.source(plan['original_support_Source_pin'],'B55_original_support');m.source(plan['original_production_inputs_Source_pin'],'production_inputs')
 need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in c.THREADS)and Path(sys.executable).resolve()==support.PYTHON,'original exact Python and one-thread environment')
 helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'B55_original_helper');factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'B55_original_resource_factory');full,production=helper.modules();guard_files=helper.guard_admission(full)
 need(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'unchanged private original OwnRSS/SerialExecutor Source and MRO')
 need(c.FLAGS==plan['original_compile_flags'],'exact original nine Fortran flags')
 roots=plan['complete_joint_roots'];joined=production.DiskResources(m.R/'validation',roots,8*2**30,2*2**30);history=factory.DynamicHistoryResources(c.ART,factory.history_roots([],c.ART),8*2**30,96*2**30,production.ResourceFailure)
 class Resources:
  def check(self):
   peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024);need(peak<512*2**20 and time.monotonic()-start<1800,'original hostSELF512/whole1800 from initial claim')
   h=history.check();j=joined.check();own=0
   if out.exists():
    for q in out.rglob('*'):
     s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'no control output alias')
     if stat.S_ISREG(s.st_mode):own+=s.st_size
   need(own<m.OUTPUT_BOUND,'entire compile/object/runtime/input/native/oracle/log/watch/report16MiB')
   need(sum(q.stat().st_size for q in BASE.rglob('*')if q.is_file())<m.SOURCE_BOUND,'Source/metadata16MiB')
   extra=0
   for p in hf['explicit_cumulative_metadata_file_pins']:
    bm.current_metadata_role(p,build)
    if not any(Path(p['path']).is_relative_to(Path(root))for root in roots):extra+=p['size_bytes']
   unlinked={}
   for name in os.listdir('/dev/fd'):
    try:s=os.fstat(int(name))
    except(ValueError,OSError):continue
    if stat.S_ISREG(s.st_mode)and s.st_nlink==0:unlinked[s.st_dev,s.st_ino]=s.st_size
   need(j['artifact_bytes']+extra+sum(unlinked.values())<2*2**30 and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original joint2/history96/cold/meta/free8 including external metadata and open-unlinked')
   return dict(original_history=h,complete_joint=j,explicit_external_metadata_bytes=extra,host_open_unlinked_bytes=sum(unlinked.values()),entire_control_output_bytes=own,host_SELF_peak_bytes=peak,whole_elapsed_seconds=time.monotonic()-start)
 resources=Resources();before=resources.check();reservation=bridge.admit_control_only_stage(plan,capture_binding,latest,before)
 shared=m.source(plan['original_OVERV_shared_methods_Source_pin'],'B55_whole_original_shared_methods');require=shared.require;source_module=shared.source_module;small_saved_input=shared.small_saved_input;log_rows=shared.log_rows;FALSE=m.FALSE
 fixed=m.unique(sf['complete_source_file_pins']+[psf,phf,cp,sf['control_plan_pin'],plan['actual_B_extraction_Host_report_pin'],plan['actual_B_extraction_Root_tools_pin'],plan['actual_B_extraction_child_report_pin'],plan['actual_B_extraction_post_pin'],plan['actual_B_extraction_post_tools_pin'],plan['actual_B_manifest_pin'],plan['actual_B_input_binding_pin'],plan['original_Common_Source_pin'],plan['original_support_Source_pin'],plan['original_bounded_Source_pin'],plan['original_production_inputs_Source_pin'],plan['original_guard_build_contract_Source_pin'],plan['original_compiler_pin'],*plan['original_four_archive_pins']]+[c.pin(q)for q in guard_files+[support.OLD_HELPER,support.RESOURCE_FACTORY,support.FULL,support.PARENT]])
 owned=[]
 def check_all():
  for p in fixed:bm.current_metadata_role(p,build);c.same_pin(p['path'],p)
  m.current(descriptor['paired_SQLite_pin']);m.current(descriptor['paired_original_pool_pin'])
  for p in owned:m.current(p);c.same_pin(p['path'],p)
  for p in plan['inherited_metadata_current7_pins']:bm.current_metadata_role(p,build)
  return resources.check()
 check_all();out.mkdir();(out/'runtime').mkdir();(out/'build').mkdir();(out/'input').mkdir();(out/'control').mkdir();(out/'OVERV-original-control').mkdir()
 shutil.copy2(support.BOUNDED,out/'runtime/run_bounded_dragon.py');owned.append(c.pin(out/'runtime/run_bounded_dragon.py'));need(owned[-1]['sha256']==plan['original_bounded_Source_pin']['sha256'],'whole original owned bounded Source')
 runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-start),'OVERV-original-control',resources);need(type(runner)is full.OwnRSSSerialExecutor and runner.resources is resources and Path(runner.bounded.__file__).resolve()==out/'runtime/run_bounded_dragon.py','exact original private runner/resources/owned bounded Source')
 first=None;secondary=[];watches=[];after=None;actual=None;verified=False;input_evidence=None
 def run(cwd,label,command):
  check_all();runner.execute(cwd,label,command,600);record=runner.records[-1];wp=out/(record['label']+'.watchdog.json');lp=out/(record['label']+'.log');w=m.metadata(c.pin(wp))
  need(record['status']=='PASS'and type(w['returncode'])is int and w['returncode']==0 and w['command']==command and w['limit_failure']is None and w['own_child_only']is True and w['liveness_group_cleanup']is True and w['rss_cap_mib']==512 and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 and c.pin(lp)['sha256']==record['log_sha256'],'actual original once stage0/log/watch/PS/RSS/wall/group closure')
  watches.append(dict(actual_stage_record_label=record['label'],actual_watchdog_pin=c.pin(wp),actual_watchdog=w,actual_log_pin=c.pin(lp)));check_all();return record
 compiler=plan['original_compiler_pin']['path'];obj=str(out/'build/OVERV_control.o');exe=str(out/'runtime/OVERV_control_unqualified')
 compile_cmd=[compiler,*c.FLAGS,*plan['original_compile_include_arguments'],'-J'+str(out/'build'),'-c',sf['control_Fortran_Source_pin']['path'],'-o',obj]
 link_cmd=[compiler,'-O2','-ffp-contract=off',obj,*[p['path']for p in plan['original_four_archive_pins']],'-o',exe]
 try:
  adapter=source_module(plan['original_saved_input_adapter_Source_pin'],'OVERV_original_saved_adapter')
  input_evidence=small_saved_input(descriptor,out/'input',resources.check,adapter);energy=Path(input_evidence['energy_path']);expected=Path(input_evidence['expected_path']);owned+=[c.pin(energy),c.pin(expected)]
  run(out/'build','compile_control',compile_cmd);owned.append(c.pin(obj))
  run(out/'build','link_control',link_cmd);owned.append(c.pin(exe))
  record=run(out/'control','run_current_control',[exe,str(energy)]);rows,logpin=log_rows(c,out,record)
  require(len(rows)==372 and rows[-1]==dict(control_scope='ORIGINAL_OVERV_FALLBACK_ONLY',physics_qualified=False,historical_machine_bit_replay=False),'exact current native observation terminal scope')
  oracle=source_module(sf['integer_oracle_Source_pin'],'OVERV_integer_oracle');model=oracle.original_overv_model(energy.read_bytes())
  require(len(model)==372 and rows[:371]==model[:371],'all native constants and370x8 words match independent exact integer model')
  real=expected.read_bytes();require(len(real)==11840,'all370x8 actual saved OVERV words')
  expected_words=[real[i:i+4][::-1].hex().upper()for i in range(0,len(real),4)]
  native_words=[word for row in rows[1:371]for word in row['OVERV32_hex']]
  require(native_words==expected_words,'all370x8 current native control words match already-saved observations')
  oracle_path=out/'Independent_integer_oracle_current_rows.json';c.write(oracle_path,dict(rows=model,actual_energy_pin=c.pin(energy),**FALSE));owned.append(c.pin(oracle_path))
  actual=dict(actual_native_log_pin=logpin,actual_integer_oracle_output_pin=c.pin(oracle_path),all_three_stages_PASS=len(runner.records)==3 and all(r['status']=='PASS'for r in runner.records),all_constant64_and_overv370x8_current_words_match=True,original_whole_LIBDEN_procedure_executed=False,**FALSE)
  require(actual['all_three_stages_PASS']is True,'exact three original native stages');verified=True
 except BaseException as error:first=error
 if verified:
  model_words=[word for row in model[1:371]for word in row['OVERV32_hex']]
  actual.update(actual_current_energy_words_observed=input_evidence['actual_original_record_metadata'][0]['original_word_count'],actual_current_overv_words_compared=len(native_words),actual_current_overv_groups=len(rows[1:371]),actual_current_overv_mixtures=len(rows[1]['OVERV32_hex']),actual_native_vs_integer_model_and_saved_word_mismatches=sum(a!=b or a!=z for a,b,z in zip(native_words,model_words,expected_words)),actual_constant64_words_compared=len(rows[0]),actual_constant64_word_mismatches=sum(rows[0][k]!=model[0][k]for k in rows[0]))
 if runner.records and len(watches)<len(runner.records):
  try:
   record=runner.records[-1];q=out/(record['label']+'.watchdog.json');lp=out/(record['label']+'.log')
   if q.exists():watches.append(dict(actual_stage_record_label=record['label'],actual_watchdog_pin=c.pin(q),actual_watchdog=m.metadata(c.pin(q)),actual_log_pin=c.pin(lp)if lp.exists()else None))
  except BaseException as e:secondary.append(dict(where='failed-stage raw monitor',error=repr(e)))
 try:after=check_all()
 except BaseException as e:
  if first is None:first=e
  else:secondary.append(dict(where='after_check',error=repr(e)))
 good=first is None and verified;target=out/'Root_actual_current_B55_OVERV_control_summary.json'
 report=dict(schema='ACTUAL_CURRENT_B55_OVERV_ORIGINAL_NATIVE_INTEGER_CONTROL_GUARDED_REPORT_V1',status='ACTUAL_CURRENT_B55_OVERV_NATIVE_INTEGER_CONTROL_CLOSED0_ONLY'if good else'FAILED_CURRENT_B55_OVERV_CONTROL_NO_RETRY',failure=None if first is None else repr(first),secondary_failures=secondary,records=runner.records,actual_watchdog_checks=watches,fixed_current_pins=fixed,output_pins=[c.pin(q)for q in sorted(out.rglob('*'))if q.is_file()],actual_bounded_input_evidence=input_evidence,actual_control_results=actual,actual_compile_command=compile_cmd,actual_link_command=link_cmd,original_guard_MRO_unchanged=True,original_guard_class='OwnRSSSerialExecutor',original_caps=m.CAPS,resources_before=before,resources_after=after,actual_control_only_stage_reservation=reservation,complete_joint_roots=roots,source_freeze_pin=psf,host_freeze_pin=phf,control_plan_pin=sf['control_plan_pin'],actual_B_extraction_report_pin=plan['actual_B_extraction_child_report_pin'],actual_B_extraction_post_pin=plan['actual_B_extraction_post_pin'],selected_actual_B55_snapshot_descriptor=descriptor,selected_actual_B55_SQL_pool_pair=plan['selected_actual_B55_SQL_pool_pair'],actual_B_manifest_pin=plan['actual_B_manifest_pin'],actual_B_input_binding_pin=plan['actual_B_input_binding_pin'],original_SOURCE_CONTEXT_NOT_SAVED_issue_not_deleted=True,final_report_resource_check_passed=False,**m.FALSE)
 m.write(target,report)
 try:
  report['resources_after_including_summary_bytes']=check_all();report['final_report_resource_check_passed']=True;shared.rewrite_summary(c,target,c.pin(target),report);check_all()
 except BaseException as e:
  if first is None:first=e
  else:secondary.append(dict(where='final_report',error=repr(e)))
  report.update(status='FAILED_CURRENT_B55_OVERV_CONTROL_NO_RETRY',failure=repr(first),secondary_failures=secondary,final_report_resource_check_passed=False);shared.rewrite_summary(c,target,c.pin(target),report)
 if first is not None:raise first
 print(json.dumps(dict(status=report['status'],report_pin=c.pin(target),**m.FALSE)),flush=True)
if __name__=='__main__':main()
