"""Assemble a runnable Source-only current OVERV control; never compile or read payloads."""
import ast,base64,copy,hashlib,json,os
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
BASE=REC/'OVERV_original_guarded_integer_control_source_v3_20261014'
ORIGINAL=REC/'OVERV_original_mixed_precision_independent_control_source_v1_20261014'
ORACLE=REC/'OVERV_integer_rounding_oracle_source_v1_20261014'
MODEL=REC/'bq64_private_GANLIB_model_control_host_source_v5_20261013/run_guarded_model_controls.py'
COMMON=REC/'post_literal3_old_pack_current_catalog_common_source_v1_20261014/guarded_warm_A_common.py'
ART=Path('/Users/wen/spot/validation/artifacts')
def pin(p):
 p=Path(p);s=p.stat();b=p.read_bytes();ids=lambda z:[z.st_dev,z.st_ino,z.st_mode,z.st_nlink,z.st_size,z.st_mtime_ns,z.st_ctime_ns]
 if s.st_size>64*2**20 or ids(p.stat())!=ids(s):raise RuntimeError('bounded Source/metadata current7')
 return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ids(s))
def read(p):return json.loads(Path(p).read_bytes())
def write(p,v):
 b=v if type(v)is bytes else(json.dumps(v,indent=2,allow_nan=False)+'\n').encode()
 with p.open('xb')as f:f.write(b);f.flush();os.fsync(f.fileno())
 return pin(p)
HOST=r'''"""Three original guarded native stages and a separate exact integer current model."""
import argparse,hashlib,importlib.util,json,os,resource,shutil,sqlite3,stat,sys,time
from pathlib import Path
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
BASE=Path(__file__).absolute().parent
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(physics_qualified=False,historical_machine_bit_replay=False,historical_native_RAM_bits_verified=False,original_XSM_memory_bits_verified=False,complete_reaction_authority_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
def require(ok,text):
 if type(ok)is not bool or not ok:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current7(p):
 q=Path(p['path']);s=q.lstat();require(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_uid==os.getuid()and identity(s)==p['identity'],'literal ordinary frozen current7')
 require(s.st_nlink==1,'single-link ordinary data/Source role');return s
def source_module(p,name):
 current7(p);require(hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'],'exact Source bytes')
 spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);current7(p);return m
def metadata(p):
 current7(p);raw=Path(p['path']).read_bytes();require(hashlib.sha256(raw).hexdigest()==p['sha256'],'exact metadata bytes');v=json.loads(raw);current7(p);return v
def small_saved_input(descriptor,out,budget,adapter):
 sqlpin=descriptor['paired_SQLite_pin'];poolpin=descriptor['paired_original_pool_pin'];current7(sqlpin);current7(poolpin)
 sf=os.open(sqlpin['path'],os.O_RDONLY|os.O_NOFOLLOW);pf=os.open(poolpin['path'],os.O_RDONLY|os.O_NOFOLLOW);db=None
 try:
  require(identity(os.fstat(sf))==sqlpin['identity']and identity(os.fstat(pf))==poolpin['identity'],'opened SQL/pool full7')
  os.environ['SQLITE_TMPDIR']=str(out)
  db=sqlite3.connect(Path(sqlpin['path']).as_uri()+'?mode=ro&immutable=1',uri=True)
  db.execute('PRAGMA query_only=ON');db.execute('PRAGMA cache_size=-8192');db.execute('PRAGMA mmap_size=0');db.execute('PRAGMA temp_store=FILE')
  db.set_progress_handler(lambda:(budget(),0)[1],1000)
  require(tuple(r[1]for r in db.execute('PRAGMA table_info(records)'))==adapter.SQL_COLUMNS,'original saved native SQLite schema')
  validator=object.__new__(adapter.SavedNativeInput);validator.pool_pin=poolpin
  records=[];payloads=[]
  for path,count in [(('ENERGY',),371)]+[(('MACROLIB','GROUP',g,'OVERV'),8)for g in range(1,371)]:
   budget();key=adapter.path_key(path);result=db.execute('SELECT row FROM records WHERE key=?',(key,)).fetchone();require(result is not None,'exact current record path')
   row=adapter.strict_json(result[0]);validator.validate_row(row)
   require(row['path']==list(path)and row['kind']==2 and row['declared_count']==count and row['original_word_count']==count,'exact current REAL32 record shape')
   begin=row['native_payload_begin_byte'];size=row['native_payload_end_byte']-begin
   require(size==count*4,'whole bounded record bytes');raw=os.pread(pf,size,begin)
   require(len(raw)==size and hashlib.sha256(raw).hexdigest()==row['native_payload_sha256'],'actual complete tiny record hash')
   records.append(row);payloads.append(raw)
  require(sum(map(len,payloads))==1484+370*8*4,'exact 13324 payload bytes, no XSM tree decode')
  require(identity(os.fstat(sf))==sqlpin['identity']and identity(os.fstat(pf))==poolpin['identity'],'after bounded inputs7')
  current7(sqlpin);current7(poolpin)
  energy=out/'ENERGY371_original_words.bin';expected=out/'OVERV370x8_original_words.bin'
  for target,raw in[(energy,payloads[0]),(expected,b''.join(payloads[1:]))]:
   with target.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
  return dict(energy_path=str(energy),expected_path=str(expected),actual_original_record_metadata=records,actual_payload_bytes_read=13324,complete_SQLite_or_pool_body_EOF_repeated=False,original_XSM_opened=False)
 finally:
  if db is not None:db.close()
  os.close(pf);os.close(sf)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('source-freeze','host-freeze'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 args=ap.parse_args();start=time.monotonic()
 def argument(role):
  n=role.replace('-','_');q=Path(getattr(args,n+'_summary'));s=q.lstat();p=dict(path=str(q),sha256=getattr(args,n+'_sha256'),size_bytes=s.st_size,identity=json.loads(getattr(args,n+'_seven_id')));return metadata(p),p
 sf,psf=argument('source-freeze');hf,phf=argument('host-freeze')
 require(sf['schema']=='COMPLETE_ORIGINAL_OVERV_INTEGER_CONTROL_SOURCE_ONLY_FREEZE_V1'and hf['schema']=='COMPLETE_ORIGINAL_OVERV_INTEGER_CONTROL_HOST_SOURCE_ONLY_FREEZE_V1'and sf['source_only']is True and sf['compiler_executed']is False and hf['selected_source_freeze_pin']==psf,'exact Source-only package')
 require(hf['host_source_pin']['path']==str(Path(__file__).absolute())and sf['original_caps']==CAPS and hf['original_caps']==CAPS,'exact host/unchanged original caps')
 plan=metadata(sf['control_plan_pin']);out=Path(plan['planned_actual_output_root']);require(out.parent==R/'validation/artifacts'and not os.path.lexists(out),'fresh single control namespace')
 c=source_module(plan['original_Common_Source_pin'],'original_OVERV_common')
 require(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in c.THREADS),'original unoptimized/unprofiled single-thread host')
 support=source_module(plan['original_support_Source_pin'],'original_OVERV_support')
 require(Path(sys.executable).resolve()==support.PYTHON,'exact original Python')
 helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'original_OVERV_helper');factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'original_OVERV_resource_factory')
 full,production=helper.modules();guard_files=helper.guard_admission(full)
 require(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'genuine original OwnRSS class and MRO')
 require(c.FLAGS==plan['original_compile_flags'],'exact original nine compiler flags')
 for p in hf['dependencies']:
  if p in(plan['selected_final_snapshot_descriptor']['paired_SQLite_pin'],plan['selected_final_snapshot_descriptor']['paired_original_pool_pin']):current7(p)
  else:c.same_pin(p['path'],p)
 extraction=metadata(plan['actual_extraction_child_report_pin']);descriptor=plan['selected_final_snapshot_descriptor']
 require(descriptor in extraction['states']['A']and descriptor['event']==55 and descriptor['role']=='final-complete-micro'and descriptor['root_prefix']==[]and extraction['all_observed_native_tree_words_and_orders_preserved']is True,'exact already-extracted final descriptor, never another XSM decode')
 roots=plan['cumulative_joint_roots'];require(len(roots)==len(set(roots))and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'all retained disjoint stage roots')
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
 resources=Resources();before=resources.check();fixed=unique(hf['dependencies']+[psf,phf,hf['host_source_pin']]+[c.pin(p)for p in guard_files])
 out.mkdir();(out/'runtime').mkdir();(out/'build').mkdir();(out/'input').mkdir();(out/'control').mkdir();(out/'OVERV-original-control').mkdir()
 shutil.copy2(support.BOUNDED,out/'runtime/run_bounded_dragon.py');owned=[c.pin(out/'runtime/run_bounded_dragon.py')]
 require(owned[0]['sha256']==plan['original_bounded_Source_pin']['sha256'],'whole original bounded Source copy')
 runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-start),'OVERV-original-control',resources)
 require(type(runner)is full.OwnRSSSerialExecutor and runner.resources is resources and Path(runner.bounded.__file__).resolve()==out/'runtime/run_bounded_dragon.py','original owning runner binding')
 first=FirstFailure();watches=[];after=None;actual=None;verified=False;input_evidence=None
 def check_all():
  for p in fixed:
   if p not in(descriptor['paired_SQLite_pin'],descriptor['paired_original_pool_pin']):c.same_pin(p['path'],p)
  current7(descriptor['paired_SQLite_pin']);current7(descriptor['paired_original_pool_pin'])
  for p in owned:c.same_pin(p['path'],p)
  return resources.check()
 def run(cwd,label,command):
  check_all();runner.execute(cwd,label,command,600);watches.append(helper.check_watch(out,runner.records[-1]));check_all();return runner.records[-1]
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
 except BaseException as error:first.capture(error,'execute_or_oracle')
 try:after=check_all()
 except BaseException as error:first.capture(error,'after_check')
 good=first.error is None and verified;target=out/'Root_actual_OVERV_original_current_integer_control_summary.json';summary=None
 try:
  summary=dict(schema='ACTUAL_OVERV_ORIGINAL_MIXED_PRECISION_INTEGER_CONTROL_GUARDED_REPORT_V1',status='ACTUAL_CURRENT_OVERV_NATIVE_INTEGER_CONTROL_CLOSED0_ONLY'if good else'ACTUAL_OVERV_CONTROL_FAILED_UNQUALIFIED',failure=None if first.error is None else safe_repr(first.error),secondary_failures=first.secondary,records=runner.records,actual_watchdog_checks=watches,fixed_current_pins=fixed,output_pins=[c.pin(p)for p in sorted(out.rglob('*'))if p.is_file()],actual_bounded_input_evidence=input_evidence,actual_control_results=actual,actual_compile_command=compile_cmd,actual_link_command=link_cmd,original_guard_MRO_unchanged=True,original_caps=CAPS,resources_before=before,resources_after=after,wall_seconds=time.monotonic()-start,original_SOURCE_CONTEXT_NOT_SAVED_issue_not_deleted=True,final_report_resource_check_passed=False,**FALSE)
  c.write(target,summary);summary['resources_after_including_summary_bytes']=check_all();summary['final_report_resource_check_passed']=True;rewrite_summary(c,target,c.pin(target),summary);check_all()
 except BaseException as error:
  first.capture(error,'publication')
  if summary is not None and target.exists():
   try:
    summary.update(status='ACTUAL_OVERV_CONTROL_FAILED_UNQUALIFIED',failure=safe_repr(first.error),secondary_failures=first.secondary,final_report_resource_check_passed=False);rewrite_summary(c,target,c.pin(target),summary)
   except BaseException as late:first.capture(late,'failed_report_publication')
 first.reraise()
 require(good,'complete current guarded controls only')
 print(json.dumps(dict(status=summary['status'],report_pin=c.pin(target),**FALSE)),flush=True)
if __name__=='__main__':main()
'''
WRITER=r'''"""Once-only Source publication; no native control or scientific payload read."""
import argparse,hashlib,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
def require(ok,text):
 if type(ok)is not bool or not ok:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
 p=Path(path);s=p.lstat();require(p.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_size<64*2**20 and not any(a.is_symlink()for a in(p,*p.parents)),'ordinary bounded Source/metadata')
 with p.open('rb')as f:raw=f.read()
 require(identity(p.lstat())==identity(s),'current7');return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))
def exact(p):
 require(pin(p['path'])==p,'exact metadata fullPF');return json.loads(Path(p['path']).read_bytes())
def contains(v,p):return v==p or type(v)is dict and any(contains(x,p)for x in v.values())or type(v)is list and any(contains(x,p)for x in v)
def write(path,v):
 with path.open('xb')as f:f.write((json.dumps(v,indent=2,allow_nan=False)+'\n').encode());f.flush();os.fsync(f.fileno())
 return pin(path)
def terminal(t):
 require(type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None and type(t['output'])is str,'genuine closed typed terminal0')
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('peer-review','peer-tools','Source-generation-tools'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 a=ap.parse_args();proof={}
 for role in('peer-review','peer-tools','Source-generation-tools'):
  n=role.replace('-','_');p=pin(getattr(a,n+'_summary'));require(p['sha256']==getattr(a,n+'_sha256')and p['identity']==json.loads(getattr(a,n+'_seven_id')),'exact explicit authority triple');proof[role]=p
 ready_pin=pin(BASE/'SOURCE_REVIEW_READY.json');ready=exact(ready_pin);plan=exact(ready['plan_pin'])
 peer=exact(proof['peer-review']);tools=exact(proof['peer-tools']);terminal(tools['actual_review_return'])
 require(peer['source_only']is True and peer['failure']is None and all(peer[k]is False for k in('business_executed','compiler_executed','numerical_executed','files_deleted'))and tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int and tools['original_integer_exit_code']==0 and json.loads(tools['actual_review_return']['output'].strip().splitlines()[-1])['review_pin']==proof['peer-review'],'same-round genuine Source review0')
 selected=[ready[k]for k in('host_source_pin','control_Fortran_Source_pin','integer_oracle_Source_pin','plan_pin','inverse_pin','Source_author_pin','writer_source_pin')]+[ready_pin]
 require(all(contains(peer,p)for p in selected),'same-round eight selected control Source fullPFs')
 generation=exact(proof['Source-generation-tools']);terminal(generation['actual_Source_preparation_return'])
 require(generation['observed_closed']is True and type(generation['original_integer_exit_code'])is int and generation['original_integer_exit_code']==0 and json.loads(generation['actual_Source_preparation_return']['output'].strip().splitlines()[-1])['ready_pin']==ready_pin,'genuine Source preparation exactready')
 for p in selected:require(pin(p['path'])==p,'selected Source unchanged')
 require(all(plan[k]is None for k in('actual_energy_input_pin','actual_current_control_report_pin','actual_integer_oracle_output_pin','actual_control_object_pin','actual_control_executable_pin')),'no actual controls prefilled')
 deps=selected+list(proof.values())+plan['source_dependency_pins']
 table={}
 for p in deps:
  require(p['path']not in table or table[p['path']]==p,'one canonical current fullPF per path');table[p['path']]=p
 deps=list(table.values())
 for p in deps:
  q=Path(p['path']);s=q.lstat();require(stat.S_ISREG(s.st_mode)and identity(s)==p['identity']and not any(a.is_symlink()for a in(q,*q.parents)),'all actual dependency current7')
 sf=dict(schema='COMPLETE_ORIGINAL_OVERV_INTEGER_CONTROL_SOURCE_ONLY_FREEZE_V1',source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,control_plan_pin=ready['plan_pin'],control_Fortran_Source_pin=ready['control_Fortran_Source_pin'],integer_oracle_Source_pin=ready['integer_oracle_Source_pin'],original_caps=plan['original_caps'],complete_byte_inverse_pin=ready['inverse_pin'],selected_Source_pins=selected,same_round_Source_review_pin=proof['peer-review'],same_round_Source_tools_pin=proof['peer-tools'],actual_Source_generation_tool_pin=proof['Source-generation-tools'],actual_current_control_report_pin=None,historical_machine_bit_replay=False,physics_qualified=False)
 sp=write(BASE/'COMPLETE_ORIGINAL_OVERV_INTEGER_CONTROL_SOURCE_ONLY_FREEZE.json',sf)
 hf=dict(schema='COMPLETE_ORIGINAL_OVERV_INTEGER_CONTROL_HOST_SOURCE_ONLY_FREEZE_V1',source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,host_source_pin=ready['host_source_pin'],selected_source_freeze_pin=sp,original_caps=plan['original_caps'],dependencies=deps+[sp],actual_current_control_report_pin=None,historical_machine_bit_replay=False,physics_qualified=False)
 hp=write(BASE/'COMPLETE_ORIGINAL_OVERV_INTEGER_CONTROL_HOST_SOURCE_ONLY_FREEZE.json',hf)
 previous=exact(plan['original_recipe_pin']);argv=previous['argv_prefix'][:11]+[ready['host_source_pin']['path']]
 for role,p in(('source-freeze',sp),('host-freeze',hp)):argv+=['--'+role+'-summary',p['path'],'--'+role+'-sha256',p['sha256'],'--'+role+'-seven-id',json.dumps(p['identity'],separators=(',',':'))]
 require(len(argv)==24,'exact original env11 plus host and two required fullPF triples')
 cli=dict(schema='ROOT_REVIEWABLE_ORIGINAL_OVERV_INTEGER_CURRENT_CONTROL_ARGV_V1',argv=argv,source_freeze_pin=sp,host_freeze_pin=hp,host_source_pin=ready['host_source_pin'],planned_actual_output_root=plan['planned_actual_output_root'],is_complete_executable_argv=True,actual_control_report_pin=None,historical_machine_bit_replay=False,physics_qualified=False)
 cp=write(BASE/'ROOT_REVIEWABLE_ORIGINAL_OVERV_INTEGER_CURRENT_CONTROL_ARGV.json',cli)
 fd=os.open(BASE,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='ORIGINAL_OVERV_INTEGER_CURRENT_CONTROL_SOURCE_SF_HF_CLI24_PUBLISHED_ONLY',Source_freeze_pin=sp,Host_freeze_pin=hp,CLI_pin=cp,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,physics_qualified=False)),flush=True)
if __name__=='__main__':main()
'''
def main():
 if BASE.exists():raise RuntimeError('fresh Source-only namespace')
 model=MODEL.read_text();tree=ast.parse(model);borrowed=[];methods=[]
 for name in('rewrite_summary','unique','safe_repr','FirstFailure','log_rows'):
  node=next(n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))and n.name==name);source=ast.get_source_segment(model,node);methods.append(source);borrowed.append(dict(name=name,original_Source_line=node.lineno,whole_bytes=source))
 host=HOST.replace('def main():\n', '\n\n'.join(methods)+'\n\ndef main():\n',1);ast.parse(host)
 buildpostpin=pin(REC/'independent_material75_after_v18_saved370_v9_actual_build_postverify_20261014/REVIEW.json');buildpost=read(buildpostpin['path']);buildpin=buildpost['actual_report_pin'];build=read(buildpin['path'])
 extractionpostpin=pin(REC/'independent_six_root_first_A_fullfield_extraction_actual_evidence_postverify_20261014/REVIEW.json');extractionpost=read(extractionpostpin['path']);extractpin=extractionpost['actual_child_report_pin'];extract=read(extractpin['path'])
 final=next(row for row in extract['states']['A']if row['event']==55 and row['role']=='final-complete-micro')
 compile_record=next(row for row in build['records']if buildpost['actual_five_compiled_Source_pins'][2]['path']in row['command']);compiler_path=compile_record['command'][0];compiler=next(p for p in build['fixed_current_pins']if p['path']==compiler_path)
 archive_pins=[p for p in buildpost['actual_original70_link_input_pins']if p['path'].endswith('.a')]
 if [p['path']for p in archive_pins]!=[p for p in buildpost['actual75_link_command']if p.endswith('.a')]:raise RuntimeError('exact actual archive order in original70 and actual75 link')
 if len(archive_pins)!=4 or not all(p['path'].endswith('.a')for p in archive_pins):raise RuntimeError('actual original archive4 order')
 common_tree=ast.parse(COMMON.read_text());assign={}
 for n in common_tree.body:
  if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
   if n.targets[0].id in('SUPPORT','SUPPORT_SHA'):
    if isinstance(n.value,ast.Constant):assign[n.targets[0].id]=n.value.value
 # SUPPORT is an exact REC-relative Source expression, resolved without importing Common.
 support_node=next(n for n in common_tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='SUPPORT'for t in n.targets));support_path=eval(ast.unparse(support_node.value),{'REC':REC,'R':Path('/Users/wen/spot'),'ROOT':Path('/Users/wen/spot'),'Path':Path})
 support_text=Path(support_path).read_text();support_ast=ast.parse(support_text)
 bounded_node=next(n for n in support_ast.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='BOUNDED'for t in n.targets));bounded=eval(ast.unparse(bounded_node.value),{'REC':REC,'R':Path('/Users/wen/spot'),'ROOT':Path('/Users/wen/spot'),'Path':Path})
 gplan=read(REC/'current_eleven_saved_gendf_actual_cumulative_seventeen_roots_host_source_v11_20261014/CURRENT_ELEVEN_GENDF_HOST_SOURCE_PREPARATION_PLAN_v2.json')
 output=ART/'axial-material-new-OVERV-original-integer-current-control-20261014-v1'
 roots=[str(output),str(BASE),str(REC/'OVERV_original_guarded_integer_control_source_v2_20261014')]+gplan['complete_cumulative_seventeen_role_roots']
 if len(set(roots))!=20:raise RuntimeError('complete original retained17 plus new2 and preserved partial Source root')
 BASE.mkdir();fortran_pin=write(BASE/'OVERV_original_mixed_precision_control.f',(ORIGINAL/'OVERV_original_mixed_precision_control.f').read_bytes());hp=write(BASE/'run_guarded_OVERV_integer_current_control.py',host.encode())
 oracle_pin=pin(ORACLE/'OVERV_integer_rounding_oracle.py');adapter_pin=pin(REC/'current_material_evidence_compare_three_exact_historical_terminal_schema_source_v6_20261014/saved_native_data_access_adapter.UNREADY.py')
 plan=dict(schema='ORIGINAL_OVERV_GUARDED_INTEGER_CURRENT_CONTROL_SOURCE_ONLY_PLAN_V1',source_only=True,planned_actual_output_root=str(output),original_Common_Source_pin=pin(COMMON),original_support_Source_pin=pin(support_path),original_bounded_Source_pin=pin(bounded),original_compiler_pin=compiler,original_compile_flags=buildpost['actual_original_nine_flags'],original_compile_include_arguments=[v for v in compile_record['command']if v.startswith('-I')],original_four_archive_pins=archive_pins,actual_build75_report_pin=buildpin,actual_build75_post_pin=buildpostpin,actual_extraction_child_report_pin=extractpin,actual_extraction_post_pin=extractionpostpin,selected_final_snapshot_descriptor=final,original_saved_input_adapter_Source_pin=adapter_pin,cumulative_joint_roots=roots,explicit_cumulative_metadata_file_pins=gplan['cumulative_explicit_metadata_file_pins'],integer_oracle_Source_pin=oracle_pin,control_Fortran_Source_pin=fortran_pin,actual_energy_input_pin=None,actual_current_control_report_pin=None,actual_integer_oracle_output_pin=None,actual_control_object_pin=None,actual_control_executable_pin=None,physics_qualified=False,historical_machine_bit_replay=False)
 plan['original_caps']=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
 plan['original_recipe_pin']=gplan['predecessor_recipe_pin']
 guards=[]
 for key in('OLD_HELPER','RESOURCE_FACTORY','FULL','PARENT'):
  node=next(n for n in support_ast.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id==key for t in n.targets));path=eval(ast.unparse(node.value),{'REC':REC,'R':Path('/Users/wen/spot'),'ROOT':Path('/Users/wen/spot'),'Path':Path});guards.append(pin(path))
 plan['source_dependency_pins']=[pin(COMMON),pin(support_path),pin(bounded),pin(MODEL),adapter_pin,oracle_pin,pin(ORIGINAL/'COMPLETE_ORIGINAL_OVERV_ARITHMETIC_STATEMENT_SOURCE_BINDING.json'),buildpostpin,buildpin,extractionpostpin,extractpin,gplan['predecessor_recipe_pin'],compiler,*archive_pins,final['paired_SQLite_pin'],final['paired_original_pool_pin'],*guards,*gplan['cumulative_explicit_metadata_file_pins']]
 ast.parse(WRITER);writer_pin=write(BASE/'write_once_original_OVERV_integer_control_Source_HF_CLI.py',WRITER.encode())
 pp=write(BASE/'PLAN.json',plan)
 inverse=write(BASE/'COMPLETE_ORIGINAL_OVERV_CONTROL_SOURCE_BINDING_AND_GUARD_BYTE_INVERSE.json',dict(schema='COMPLETE_ORIGINAL_OVERV_CONTROL_SOURCE_BINDING_AND_GUARD_BYTE_INVERSE_V1',source_only=True,original_Fortran_Source_pin=pin(ORIGINAL/'OVERV_original_mixed_precision_control.f'),candidate_Fortran_Source_pin=fortran_pin,whole_Fortran_Source_byte_equal=True,integer_oracle_Source_pin=oracle_pin,integer_oracle_whole_bytes_unchanged=True,original_guard_prototype_Source_pin=pin(MODEL),borrowed_original_guard_methods=borrowed,all_borrowed_guard_method_whole_bytes_unchanged=True,original_arithmetic_Source_binding_pin=pin(ORIGINAL/'COMPLETE_ORIGINAL_OVERV_ARITHMETIC_STATEMENT_SOURCE_BINDING.json'),own_host_Source_pin=hp,new_host_is_specific_current_control_not_original_full_model_fixture=True,original_370x8_formula_and_4archives_nineflags_source_bindings_retained=True,original_caps_and_genuine_OwnRSS_class_MRO_unchanged=True,original_large_XSM_scientific_input_not_opened_by_control_reader=True,exact_guarded_payload_byte_count=13324,actual_current_control_report_pin=None,historical_machine_bit_replay=False,physics_qualified=False))
 ready=write(BASE/'SOURCE_REVIEW_READY.json',dict(schema='ORIGINAL_OVERV_GUARDED_INTEGER_CURRENT_CONTROL_SOURCE_ONLY_READY_V1',source_only=True,host_source_pin=hp,control_Fortran_Source_pin=fortran_pin,integer_oracle_Source_pin=oracle_pin,plan_pin=pp,inverse_pin=inverse,Source_author_pin=pin(__file__),writer_source_pin=writer_pin,future_Source_freeze_pin=None,future_Host_freeze_pin=None,future_CLI_pin=None,actual_control_report_pin=None,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,physics_qualified=False))
 print(json.dumps(dict(status='ORIGINAL_OVERV_GUARDED_INTEGER_CURRENT_CONTROL_SOURCE_ONLY_READY',ready_pin=ready,plan_pin=pp,inverse_pin=inverse,host_source_pin=hp,Source_author_pin=pin(__file__),business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
