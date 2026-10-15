"""Three original guarded native stages and a separate exact integer current model."""
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
def rewrite_summary(c,path,previous,data):
    if previous['identity'][3] != 1 or previous['path'] != str(path):
        raise RuntimeError('only owning single-link summary can be rewritten')
    c.same_pin(path,previous)
    fd = os.open(path,os.O_WRONLY|os.O_NOFOLLOW)
    try:
        s = os.fstat(fd)
        if [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns] != previous['identity']:
            raise RuntimeError('owned summary opened7ID changed')
        with os.fdopen(fd,'w',encoding='utf-8') as stream:
            fd = None
            stream.seek(0)
            stream.truncate(0)
            json.dump(data,stream,indent=2,ensure_ascii=False,allow_nan=False)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        if fd is not None:
            os.close(fd)
    if c.identity(path)[:4] != previous['identity'][:4]:
        raise RuntimeError('own summary physical role changed')

def unique(rows):
    table={}
    for row in rows:
        if row['path']in table and table[row['path']]!=row:
            raise RuntimeError('inconsistent complete PF for same input path')
        table[row['path']]=row
    return list(table.values())

def safe_repr(error):
    try:return repr(error)
    except BaseException:return '<exception repr unavailable>'

class FirstFailure:
    def __init__(self):
        self.error=None;self.traceback=None;self.secondary=[]
    def capture(self,error,where):
        if self.error is None:
            self.error=error;self.traceback=error.__traceback__
        else:self.secondary.append(dict(where=where,error=safe_repr(error)))
    def reraise(self):
        if self.error is not None:raise self.error.with_traceback(self.traceback)

def log_rows(c,root,record):
    path=root/(record['label']+'.log')
    pf=c.pin(path)
    if pf['sha256']!=record['log_sha256']:raise RuntimeError('actual closed stage full log SHA')
    rows=[]
    with path.open('r',encoding='utf-8',errors='strict')as stream:
        for line in stream:
            if len(line)>65536:raise RuntimeError('control JSON/log line bound')
            line=line.strip()
            if line.startswith('{')and line.endswith('}'):
                value=json.loads(line)
                if isinstance(value,dict):rows.append(value)
    c.same_pin(path,pf)
    return rows,pf

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
