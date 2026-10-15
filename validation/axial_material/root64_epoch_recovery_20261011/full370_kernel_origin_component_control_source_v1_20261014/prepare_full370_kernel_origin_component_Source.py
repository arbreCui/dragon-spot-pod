"""Prepare exact Source only; no compiler, tests, old scientific payload or deletion."""
import ast,base64,hashlib,json,os,resource,stat,time
from pathlib import Path
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
BASE=Path(__file__).absolute().parent
REF=REC/'full370_unreduced_eigen_reference_source_v2'
OLD=REC/'OVERV_original_guarded_integer_control_source_v3_20261014'
SAVED=REC/'saved_three_macro_exact_typed_path_join_source_v1_20261014'
OUT=R/'validation/artifacts/axial-material-current-full370-kernel-origin-component-controls-20261014-v1'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(physics_qualified=False,historical_machine_bit_replay=False,historical_native_RAM_bits_verified=False,original_XSM_memory_bits_verified=False,complete_reaction_authority_qualified=False,full_reference_qualified=False,formal_H150_NZ48_full_controls_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
def require(ok,text):
 if type(ok)is not bool or not ok:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat();require(p.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid()and s.st_size<64*2**20 and not any(x.is_symlink()for x in(p,*p.parents)),'ordinary bounded current Source/metadata')
 with p.open('rb')as f:
  require(identity(os.fstat(f.fileno()))==identity(s),'opened7');raw=f.read();require(identity(os.fstat(f.fileno()))==identity(s),'EOF7')
 require(identity(p.lstat())==identity(s),'after7');return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))
def exact(p):
 require(pin(p['path'])==p,'exact current fullPF');return json.loads(Path(p['path']).read_bytes())
def write(p,v):
 raw=v if type(v)is bytes else(json.dumps(v,indent=2,allow_nan=False)+'\n').encode()
 with p.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 return pin(p)
HOST_HEAD='''"""Original serial guard: actual full370 library origin and two component suites only."""
import argparse,hashlib,importlib.util,json,os,resource,shutil,stat,sys,time
from pathlib import Path
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
BASE=Path(__file__).absolute().parent
CAPS=CAPS_LITERAL
FALSE=FALSE_LITERAL
def require(ok,text):
 if type(ok)is not bool or not ok:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current7(p):
 q=Path(p['path']);s=q.lstat();system_tool=q==Path('/usr/bin/clang++')and s.st_uid==0 and s.st_nlink>=1 and bool(s.st_mode&0o111);require(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and((s.st_uid==os.getuid()and s.st_nlink==1)or system_tool)and identity(s)==p['identity'],'literal ordinary frozen current7 with exact preexisting compiler tool role');return s
def source_module(p,name):
 current7(p);require(hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'],'exact Source bytes')
 spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);current7(p);return m
def metadata(p):
 current7(p);raw=Path(p['path']).read_bytes();require(hashlib.sha256(raw).hexdigest()==p['sha256'],'exact metadata bytes');v=json.loads(raw);current7(p);return v
'''
HOST_MAIN='''
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('source-freeze','host-freeze'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 args=ap.parse_args();start=time.monotonic()
 def argument(role):
  n=role.replace('-','_');q=Path(getattr(args,n+'_summary'));s=q.lstat();p=dict(path=str(q),sha256=getattr(args,n+'_sha256'),size_bytes=s.st_size,identity=json.loads(getattr(args,n+'_seven_id')));return metadata(p),p
 sf,psf=argument('source-freeze');hf,phf=argument('host-freeze')
 require(sf['schema']=='COMPLETE_FULL370_KERNEL_ORIGIN_COMPONENT_CONTROL_SOURCE_ONLY_FREEZE_V1'and hf['schema']=='COMPLETE_FULL370_KERNEL_ORIGIN_COMPONENT_CONTROL_HOST_SOURCE_ONLY_FREEZE_V1'and sf['source_only']is True and sf['compiler_executed']is False and hf['selected_source_freeze_pin']==psf,'exact Source-only package')
 require(hf['host_source_pin']['path']==str(Path(__file__).absolute())and sf['original_caps']==CAPS and hf['original_caps']==CAPS,'exact host/unchanged original caps')
 plan=metadata(sf['control_plan_pin']);out=Path(plan['planned_actual_output_root']);require(out.parent==R/'validation/artifacts'and not os.path.lexists(out),'fresh single control namespace, zero retry')
 c=source_module(plan['original_Common_Source_pin'],'full370_kernel_original_common')
 require(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in c.THREADS),'original unoptimized/unprofiled single-thread host')
 support=source_module(plan['original_support_Source_pin'],'full370_kernel_original_support')
 require(Path(sys.executable).resolve()==support.PYTHON,'exact original Python')
 helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'full370_kernel_original_helper');factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'full370_kernel_original_resource_factory')
 full,production=helper.modules();guard_files=helper.guard_admission(full)
 require(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'genuine original OwnRSS class and MRO')
 for p in hf['dependencies']:current7(p);c.same_pin(p['path'],p)
 roots=plan['complete_joint_roots'];require(len(roots)==len(set(roots))and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'all retained disjoint stage roots')
 joined=production.DiskResources(R/'validation',roots,8*2**30,2*2**30)
 history=factory.DynamicHistoryResources(c.ART,factory.history_roots([str(out)],c.ART),8*2**30,96*2**30,production.ResourceFailure)
 allfamily=factory.DynamicHistoryResources(c.ART,factory.history_roots([],c.ART),8*2**30,96*2**30,production.ResourceFailure)
 initial=allfamily.check();require(initial['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,'genuine complete-family fullfresh2/cold/meta reservation')
 class Resources:
  def check(self):
   peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
   require(peak<512*2**20 and time.monotonic()-start<1800,'original whole1800 and host SELF512')
   h=history.check();f=joined.check();require(h['artifact_bytes']+20971764748+64*2**20<96*2**30 and f['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original cold/history96/free8 reserves')
   extra=0
   for p in plan['explicit_cumulative_metadata_file_pins']:
    current7(p)
    if not any(Path(p['path']).is_relative_to(Path(root))for root in roots):extra+=p['size_bytes']
   require(f['artifact_bytes']+extra<2*2**30,'same cumulative joint2GiB including exact external metadata')
   return dict(original_history=h,complete_joint=f,explicit_external_metadata_bytes=extra,host_SELF_peak_bytes=peak,whole_elapsed_seconds=time.monotonic()-start)
 resources=Resources();before=resources.check();fixed=unique(hf['dependencies']+[psf,phf,hf['host_source_pin']]+[c.pin(p)for p in guard_files]);owned=[]
 out.mkdir();(out/'runtime').mkdir();(out/'component').mkdir();(out/'kernel-component').mkdir()
 shutil.copy2(support.BOUNDED,out/'runtime/run_bounded_dragon.py');owned.append(c.pin(out/'runtime/run_bounded_dragon.py'))
 require(owned[0]['sha256']==plan['original_bounded_Source_pin']['sha256'],'whole original bounded Source copy')
 runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-start),'kernel-component',resources)
 require(type(runner)is full.OwnRSSSerialExecutor and runner.resources is resources and Path(runner.bounded.__file__).resolve()==out/'runtime/run_bounded_dragon.py','original owning runner binding')
 first=FirstFailure();watches=[];after=None;actual=None;verified=False
 def check_all():
  for p in fixed:current7(p);c.same_pin(p['path'],p)
  for p in owned:current7(p);c.same_pin(p['path'],p)
  return resources.check()
 def run(label,command):
  check_all();runner.execute(out/'component',label,command,600);watches.append(helper.check_watch(out,runner.records[-1]));check_all();return runner.records[-1]
 library=out/'component/libcurrent_full370_white_accumulate.dylib'
 command=[plan['compiler_pin']['path'],*plan['original_clang_flags'],plan['accumulator_Source_pin']['path'],'-o',str(library)]
 expected_command=metadata(plan['original_compile_watchdog_pin'])['command'];require(command[:6]==expected_command[:6],'exact compiler and flags from genuine prior watchdog')
 reports=[]
 try:
  run('compile_full370_library',command);owned.append(c.pin(library))
  for label,test,report_name in [('full_angular_p2',plan['angular_test_Source_pin'],'FULL_ANGULAR_P2_COMPONENT_REPORT.json'),('layered_multigroup',plan['multigroup_test_Source_pin'],'LAYERED_MULTIGROUP_COMPONENT_REPORT.json')]:
   report=out/'component'/report_name
   cmd=[str(support.PYTHON),'-B',plan['component_launcher_Source_pin']['path'],'--plan',sf['control_plan_pin']['path'],'--test',test['path'],'--report',str(report)]
   if label=='layered_multigroup':cmd+=['--library',str(library),'--old-library',plan['actual_original_zonal_library_pin']['path']]
   cmd+=['-v'];run(label,cmd);p=c.pin(report);owned.append(p);result=metadata(p)
   require(type(result['tests_run'])is int and result['tests_run']==6 and result['passed']is True and result['failures']==[]and result['errors']==[]and result['full_reference_qualified']is False,'six genuine component tests with no reference qualification')
   reports.append(dict(label=label,report_pin=p,tests_run=6,passed=True))
  require(len(runner.records)==3 and all(r['status']=='PASS'for r in runner.records),'exact three original native stages')
  actual=dict(component_reports=reports,all_three_stages_PASS=True,two_suites_twelve_component_tests_PASS=True,complete_actual_source_pins=plan['complete_cpp_Source_pins'],actual_library_pin=c.pin(library),**FALSE);verified=True
 except BaseException as error:first.capture(error,'execute_or_component_report')
 try:after=check_all()
 except BaseException as error:first.capture(error,'after_check')
 good=first.error is None and verified;target=out/'Root_actual_full370_kernel_origin_component_summary.json';summary=None
 try:
  summary=dict(schema='ACTUAL_FULL370_KERNEL_ORIGIN_COMPONENT_GUARDED_REPORT_V1',status='ACTUAL_FULL370_LIBRARY_AND_TWELVE_COMPONENT_CONTROLS_CLOSED0_ONLY'if good else'ACTUAL_FULL370_KERNEL_COMPONENT_FAILED_UNQUALIFIED',failure=None if first.error is None else safe_repr(first.error),after_check_error=None,secondary_failures=first.secondary,records=runner.records,actual_watchdog_checks=watches,fixed_current_pins=fixed,output_pins=[c.pin(p)for p in sorted(out.rglob('*'))if p.is_file()],actual_control_results=actual,actual_compile_command=command,original_guard_MRO_unchanged=True,original_caps=CAPS,resources_before=before,resources_after=after,wall_seconds=time.monotonic()-start,component_only=True,synthetic_fixture_scope='angular8azimuth128states; layeredH150NZ3; all370 columns',formal_H150_NZ48_11364tracks_181824actions_controls_executed=False,final_report_resource_check_passed=False,**FALSE)
  c.write(target,summary);summary['resources_after_including_summary_bytes']=check_all();summary['final_report_resource_check_passed']=True;rewrite_summary(c,target,c.pin(target),summary);check_all()
  if good:
   origin=dict(schema='ACTUAL_FULL370_WHITE_ACCUMULATOR_LIBRARY_ORIGIN_V1',library_pin=c.pin(library),complete_source_pins=plan['complete_cpp_Source_pins'],actual_build_report_pin=c.pin(target),actual_command=command,original_caps=CAPS,compiler_pin=plan['compiler_pin'],original_compile_watchdog_pin=plan['original_compile_watchdog_pin'],component_reports=reports,complete_local_project_include_closure=True,system_Cxx_headers_transitive_EOF_claimed=False,component_only=True,**FALSE)
   origin_path=out/'ACTUAL_FULL370_WHITE_ACCUMULATOR_LIBRARY_ORIGIN.json';c.write(origin_path,origin);owned.append(c.pin(origin_path));check_all()
 except BaseException as error:
  first.capture(error,'publication')
  if summary is not None and target.exists():
   try:
    summary.update(status='ACTUAL_FULL370_KERNEL_COMPONENT_FAILED_UNQUALIFIED',failure=safe_repr(first.error),secondary_failures=first.secondary,final_report_resource_check_passed=False);rewrite_summary(c,target,c.pin(target),summary)
   except BaseException as late:first.capture(late,'failed_report_publication')
 first.reraise();require(good,'complete current guarded components only')
 print(json.dumps(dict(status=summary['status'],report_pin=c.pin(target),origin_pin=c.pin(origin_path),library_pin=c.pin(library),**FALSE)),flush=True)
if __name__=='__main__':main()
'''
LAUNCHER='''"""Select exact v2 imports explicitly, then execute unchanged six-test Source bytes."""
import argparse,hashlib,importlib.util,json,os,runpy,stat,sys
from pathlib import Path
sys.dont_write_bytecode=True
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def exact(p):
 q=Path(p['path']);s=q.lstat()
 if not q.is_absolute()or any(a.is_symlink()for a in(q,*q.parents))or not stat.S_ISREG(s.st_mode)or s.st_nlink!=1 or identity(s)!=p['identity']:raise RuntimeError('exact component ordinary current7')
 raw=q.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=p['sha256']or identity(q.lstat())!=p['identity']:raise RuntimeError('exact component full Source bytes')
 return raw
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--plan',required=True);ap.add_argument('--test',required=True);a,remaining=ap.parse_known_args()
 plan=json.loads(Path(a.plan).read_bytes());bindings=plan['explicit_component_import_bindings'];tests=[plan['angular_test_Source_pin'],plan['multigroup_test_Source_pin']]
 test=next(p for p in tests if p['path']==a.test)
 for row in bindings:
  name=row['module'];p=row['pin'];exact(p)
  if name in sys.modules:raise RuntimeError('component module already imported '+name)
  spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m)
  if Path(m.__file__).absolute()!=Path(p['path']):raise RuntimeError('actual component module binding '+name)
 exact(test);sys.argv=[a.test,*remaining]
 try:runpy.run_path(a.test,run_name='__main__')
 finally:
  exact(test)
  for row in bindings:
   exact(row['pin'])
   if Path(sys.modules[row['module']].__file__).absolute()!=Path(row['pin']['path']):raise RuntimeError('component module changed '+row['module'])
if __name__=='__main__':main()
'''
def main():
 start=time.monotonic();require(sorted(p.name for p in BASE.iterdir())==[Path(__file__).name],'one fresh Source author only')
 oldplan=json.loads((OLD/'PLAN.json').read_bytes());savedpin=pin(SAVED/'PLAN.json');saved=exact(savedpin)
 actualsavedpin=pin(R/'validation/artifacts/axial-material-current-saved-three-macro-typed-path-compare-20261014-v1/Root_actual_saved_three_macro_typed_path_comparison_summary.json');actualsaved=exact(actualsavedpin)
 require(actualsaved['failure']is None,'retained prior owning summary metadata, no extra kernel mathematical admission')
 compilewatch=pin(R/'validation/artifacts/axial-material-layered-white-radial-transfer-component-20261011/component/compile.watchdog.json');watch=exact(compilewatch);cmd=watch['command']
 require(type(watch['returncode'])is int and watch['returncode']==0 and watch['limit_failure']is None and cmd[6].endswith('/native_layered_white_transfer.cpp')and cmd[7]=='-o'and len(cmd)==9,'genuine original clang command structure')
 compilerpath=Path(cmd[0]);compilerstat=compilerpath.lstat();require(compilerpath==Path('/usr/bin/clang++')and stat.S_ISREG(compilerstat.st_mode)and compilerstat.st_uid==0 and compilerstat.st_nlink>=1 and bool(compilerstat.st_mode&0o111),'exact preexisting system compiler executable role')
 # /usr/bin clang is root-owned; record its complete PF separately.
 def toolpin(p):
  p=Path(p);s=p.lstat();require(p==Path('/usr/bin/clang++')and stat.S_ISREG(s.st_mode)and s.st_uid==0 and s.st_nlink>=1 and not any(x.is_symlink()for x in(p,*p.parents))and s.st_size<64*2**20,'bounded exact preexisting system compiler tool')
  raw=p.read_bytes();require(identity(p.lstat())==identity(s),'tool after7');return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))
 compiler=toolpin(compilerpath);oldlib=pin(R/'validation/artifacts/axial-material-native-layered-zonal-support-permission-20261011-qc7x4oa3/component/liblayered_zonal.dylib')
 original=(OLD/'run_guarded_OVERV_integer_current_control.py').read_text();tree=ast.parse(original);names=['rewrite_summary','unique','safe_repr','FirstFailure'];borrowed=[];chunks=[]
 for name in names:
  node=next(n for n in tree.body if getattr(n,'name',None)==name);text=ast.get_source_segment(original,node);chunks.append(text);borrowed.append(dict(name=name,complete_UTF8_base64=base64.b64encode(text.encode()).decode(),sha256=hashlib.sha256(text.encode()).hexdigest()))
 host=HOST_HEAD.replace('CAPS_LITERAL',repr(CAPS)).replace('FALSE_LITERAL',repr(FALSE))+'\n\n'+'\n\n'.join(chunks)+'\n'+HOST_MAIN;ast.parse(host);hp=write(BASE/'run_guarded_full370_kernel_origin_components.py',host.encode())
 ast.parse(LAUNCHER);launcher=write(BASE/'run_exact_v2_component_tests.py',LAUNCHER.encode())
 tests=[];copies=[]
 for name in('test_native_full_angular_p2.py','test_native_layered_multigroup.py'):
  src=pin(R/'validation/iterative'/name);raw=Path(src['path']).read_bytes();target=write(BASE/name,raw);require(src['sha256']==target['sha256'],'wholebyte test copy');tests.append(target);copies.append(dict(original_pin=src,candidate_pin=target,whole_bytes_equal=True,complete_UTF8_base64=base64.b64encode(raw).decode()))
 cppnames=['current_full370_white_accumulate.cpp','native_layered_white_transfer.cpp','native_layered_multigroup.cpp','native_layered_transport.cpp','native_layered_geometry.hpp','native_oblique_geometry_core.hpp'];cpp=[pin(REF/name)for name in cppnames]
 for p in cpp:
  local=[v for v in __import__('re').findall(r'^#include "([^"]+)"',Path(p['path']).read_text(),__import__('re').M)]
  require(all(str(REF/name)in[q['path']for q in cpp]for name in local),'complete local C++ include closure')
 bindings=[]
 for module,directory in [('native_oblique_streaming',REF),('native_layered_transport',REF),('native_layered_multigroup',REF),('native_full_angular_p2',REF),('native_layered_zonal',R/'validation/iterative'),('native_layered_reference',R/'validation/iterative')]:bindings.append(dict(module=module,pin=pin(directory/(module+'.py'))))
 authority=pin(REF/'current_formal_input_authority.py')
 require('ACTUAL_FULL370_WHITE_ACCUMULATOR_LIBRARY_ORIGIN_V1'in Path(authority['path']).read_text(),'actual KernelBinding authority read')
 guarddeps=[]
 wanted=['prepare_qualified_AB_source_factor_production.py','moment_order_complete_history_resource_trie_20261010.py','qualify_refined_AAA_layered_full.py','production_runner.py']
 for p in oldplan['source_dependency_pins']:
  if Path(p['path']).name in wanted:require(pin(p['path'])==p,'exact original current guard Source');guarddeps.append(p)
 fulltext=Path(next(p['path']for p in guarddeps if Path(p['path']).name=='qualify_refined_AAA_layered_full.py')).read_text();ft=ast.parse(fulltext)
 fenv={'ROOT':R,'ART':R/'validation/artifacts','Path':Path}
 for n in ft.body:
  if isinstance(n,ast.Assign):
   for t in n.targets:
    if isinstance(t,ast.Name)and t.id in('OUT','ROOT','ARTIFACTS_ROOT'):
     try:fenv[t.id]=eval(compile(ast.Expression(n.value),'<original-full-path>','eval'),{'__builtins__':{}},fenv)
     except NameError:pass
 guardfolder=fenv['OUT']/'preflight/live_guard';guardpin=pin(guardfolder/'guard_controls.json');guard=exact(guardpin);guarddeps+=[guardpin,pin(guardfolder/'tested_driver_source.py'),*[pin(guardfolder/n)for n in guard['control_files']]]
 prodinputs=pin(R/'validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_inputs.py');guarddeps.append(prodinputs)
 plan=dict(schema='FULL370_KERNEL_ORIGIN_COMPONENT_CONTROL_SOURCE_ONLY_PLAN_V1',source_only=True,planned_actual_output_root=str(OUT),original_caps=CAPS,original_Common_Source_pin=saved['original_Common_Source_pin'],original_support_Source_pin=saved['original_support_Source_pin'],original_bounded_Source_pin=saved['original_bounded_Source_pin'],original_guard_prototype_Source_pin=pin(OLD/'run_guarded_OVERV_integer_current_control.py'),original_compile_watchdog_pin=compilewatch,original_clang_flags=cmd[1:6],compiler_pin=compiler,accumulator_Source_pin=cpp[0],complete_cpp_Source_pins=cpp,actual_original_zonal_library_pin=oldlib,angular_test_Source_pin=tests[0],multigroup_test_Source_pin=tests[1],component_launcher_Source_pin=launcher,explicit_component_import_bindings=bindings,KernelBinding_authority_Source_pin=authority,original_cumulative_plan_pin=savedpin,actual_prior_saved_comparison_report_pin=actualsavedpin,complete_joint_roots=saved['complete_joint_roots']+[str(BASE),str(OUT)],explicit_cumulative_metadata_file_pins=saved['explicit_cumulative_metadata_file_pins'],original_recipe_pin=pin(OLD/'ROOT_REVIEWABLE_ORIGINAL_OVERV_INTEGER_CURRENT_CONTROL_ARGV.json'),actual_library_pin=None,actual_kernel_origin_pin=None,actual_component_control_report_pin=None,complete_local_project_cpp_include_closure=True,system_Cxx_headers_transitive_EOF_claimed=False,actual_test_scope_is_component_only=True,formal_H150_NZ48_11364tracks_181824actions_controls_executed=False,**FALSE)
 deps=[plan[k]for k in('original_Common_Source_pin','original_support_Source_pin','original_bounded_Source_pin','original_guard_prototype_Source_pin','original_compile_watchdog_pin','compiler_pin','actual_original_zonal_library_pin','KernelBinding_authority_Source_pin','original_cumulative_plan_pin','actual_prior_saved_comparison_report_pin','original_recipe_pin')]+cpp+[r['pin']for r in bindings]+guarddeps+plan['explicit_cumulative_metadata_file_pins']
 table={}
 for p in deps:require(p['path']not in table or table[p['path']]==p,'consistent exact dependency');table[p['path']]=p
 plan['source_dependency_pins']=list(table.values())
 writer=(OLD/'write_once_original_OVERV_integer_control_Source_HF_CLI.py').read_text()
 writer=writer.replace("'host_source_pin','control_Fortran_Source_pin','integer_oracle_Source_pin','plan_pin','inverse_pin','Source_author_pin','writer_source_pin'","'host_source_pin','component_launcher_Source_pin','angular_test_Source_pin','multigroup_test_Source_pin','plan_pin','inverse_pin','Source_author_pin','writer_source_pin'")
 writer=writer.replace("('actual_energy_input_pin','actual_current_control_report_pin','actual_integer_oracle_output_pin','actual_control_object_pin','actual_control_executable_pin')","('actual_library_pin','actual_kernel_origin_pin','actual_component_control_report_pin')")
 writer=writer.replace("control_Fortran_Source_pin=ready['control_Fortran_Source_pin'],integer_oracle_Source_pin=ready['integer_oracle_Source_pin'],",'')
 writer=writer.replace('COMPLETE_ORIGINAL_OVERV_INTEGER_CONTROL_SOURCE_ONLY_FREEZE','COMPLETE_FULL370_KERNEL_ORIGIN_COMPONENT_CONTROL_SOURCE_ONLY_FREEZE').replace('COMPLETE_ORIGINAL_OVERV_INTEGER_CONTROL_HOST_SOURCE_ONLY_FREEZE','COMPLETE_FULL370_KERNEL_ORIGIN_COMPONENT_CONTROL_HOST_SOURCE_ONLY_FREEZE').replace('ROOT_REVIEWABLE_ORIGINAL_OVERV_INTEGER_CURRENT_CONTROL_ARGV','ROOT_REVIEWABLE_FULL370_KERNEL_ORIGIN_COMPONENT_CONTROL_ARGV').replace('ORIGINAL_OVERV_INTEGER_CURRENT_CONTROL_SOURCE_SF_HF_CLI24_PUBLISHED_ONLY','FULL370_KERNEL_ORIGIN_COMPONENT_SOURCE_SF_HF_CLI24_PUBLISHED_ONLY').replace('actual_current_control_report_pin','actual_component_control_report_pin').replace("previous['argv_prefix'][:11]","previous['argv'][:11]").replace('same-round eight selected control Source fullPFs','same-round nine selected kernel component Source fullPFs')
 writer=writer.replace("sf=dict(schema=", "sf=dict(component_only=True,formal_H150_NZ48_full_controls_qualified=False,schema=")
 ast.parse(writer);wp=write(BASE/'write_once_full370_kernel_origin_components_SF_HF_CLI.py',writer.encode());pp=write(BASE/'PLAN.json',plan)
 inverse=write(BASE/'COMPLETE_FULL370_KERNEL_COMPONENT_SOURCE_BINDING_BYTE_INVERSE.json',dict(schema='COMPLETE_FULL370_KERNEL_COMPONENT_SOURCE_BINDING_BYTE_INVERSE_V1',source_only=True,original_guard_prototype_Source_pin=plan['original_guard_prototype_Source_pin'],borrowed_original_guard_methods=borrowed,all_four_borrowed_guard_definitions_whole_bytes_unchanged=True,test_wholebyte_copy_proofs=copies,complete_local_cpp_Source_pins=cpp,explicit_v2_import_bindings=bindings,host_source_pin=hp,component_launcher_Source_pin=launcher,KernelBinding_authority_Source_pin=authority,unchanged_original_caps=CAPS,retained_prior_joint_roots_count=30,new_joint_roots_count=32,actual_component_report_pin=None,**FALSE))
 ready=write(BASE/'SOURCE_REVIEW_READY.json',dict(schema='FULL370_KERNEL_ORIGIN_COMPONENT_CONTROL_SOURCE_ONLY_READY_V1',source_only=True,host_source_pin=hp,component_launcher_Source_pin=launcher,angular_test_Source_pin=tests[0],multigroup_test_Source_pin=tests[1],plan_pin=pp,inverse_pin=inverse,Source_author_pin=pin(__file__),writer_source_pin=wp,future_Source_freeze_pin=None,future_Host_freeze_pin=None,future_CLI_pin=None,actual_kernel_origin_pin=None,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,**FALSE))
 require(time.monotonic()-start<600 and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss<512*2**20,'Sourcegen same stage/SELF cap')
 print(json.dumps(dict(status='FULL370_KERNEL_ORIGIN_COMPONENT_SOURCE_ONLY_READY',ready_pin=ready,plan_pin=pp,inverse_pin=inverse,host_source_pin=hp,writer_source_pin=wp,Source_author_pin=pin(__file__),business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
