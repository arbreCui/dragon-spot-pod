"""Original serial guard: actual full370 library origin and two component suites only."""
import argparse,hashlib,importlib.util,json,os,resource,shutil,stat,struct,sys,time
from pathlib import Path
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
BASE=Path(__file__).absolute().parent
CAPS={'whole_seconds': 1800, 'stage_seconds': 600, 'rss_mib': 512, 'fresh_bytes': 2147483648, 'history_bytes': 103079215104, 'cold_reserve_bytes': 20971764748, 'metadata_reserve_bytes': 67108864, 'free_floor_bytes': 8589934592, 'threads': 1, 'children_at_once': 1, 'retries': 0}
FALSE={'historical_whole_ASCII_file_reconstruction_qualified':False,'whole_original_NJOY_build_reproduced':False,'current_SPH_MASK_context_applied':False,'physical_neutron_balance_qualified':False,'physics_qualified': False, 'historical_machine_bit_replay': False, 'historical_native_RAM_bits_verified': False, 'original_XSM_memory_bits_verified': False, 'complete_reaction_authority_qualified': False, 'full_reference_qualified': False, 'formal_H150_NZ48_full_controls_qualified': False, 'AAA_qualified': False, 'ABA_admitted': False, 'goal_complete': False}
def require(ok,text):
 if type(ok)is not bool or not ok:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current7(p):
 q=Path(p['path']);s=q.lstat();compiler=q==Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15')and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and p['identity'][3]==2 and s.st_nlink==2
 require(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and(s.st_nlink==1 or compiler)and identity(s)==p['identity'],'exactcurrent7, sole original compiler two-link role')
 return s
def source_module(p,name):
 current7(p);require(hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'],'exact Source bytes')
 spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);current7(p);return m
def metadata(p):
 current7(p);raw=Path(p['path']).read_bytes();require(hashlib.sha256(raw).hexdigest()==p['sha256'],'exact metadata bytes');v=json.loads(raw);current7(p);return v


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

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('source-freeze','host-freeze'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 args=ap.parse_args();start=time.monotonic()
 def argument(role):
  n=role.replace('-','_');q=Path(getattr(args,n+'_summary'));s=q.lstat();p=dict(path=str(q),sha256=getattr(args,n+'_sha256'),size_bytes=s.st_size,identity=json.loads(getattr(args,n+'_seven_id')));return metadata(p),p
 sf,psf=argument('source-freeze');hf,phf=argument('host-freeze')
 require(sf['schema']=='ORIGINAL_A11_COMPONENT_SOURCE_ONLY_FREEZE_V1'and hf['schema']=='ORIGINAL_A11_COMPONENT_HOST_SOURCE_ONLY_FREEZE_V1'and sf['source_only']is True and sf['compiler_executed']is False and hf['selected_source_freeze_pin']==psf and hf['host_source_pin']['path']==str(Path(__file__).absolute())and sf['original_caps']==CAPS and hf['original_caps']==CAPS,'exact same-round Source-only package/host/original caps')
 plan=metadata(sf['control_plan_pin']);out=Path(plan['planned_actual_output_root']);require(out.parent==R/'validation/artifacts'and not os.path.lexists(out),'fresh control namespace; no retry')
 c=source_module(plan['original_Common_Source_pin'],'a11_original_common');support=source_module(plan['original_support_Source_pin'],'a11_original_support')
 require(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in c.THREADS)and Path(sys.executable).resolve()==support.PYTHON,'original interpreter/unoptimized/unprofiled/single thread')
 helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'a11_original_helper');factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'a11_original_factory');full,production=helper.modules();guard_files=helper.guard_admission(full)
 require(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'original actual OwnRSS class/MRO')
 roots=plan['complete_joint_roots'];require(len(roots)==38 and len(set(roots))==38 and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'complete retained36 plus Source/output')
 joined=production.DiskResources(R/'validation',roots,8*2**30,2*2**30);history=factory.DynamicHistoryResources(c.ART,factory.history_roots([str(out)],c.ART),8*2**30,96*2**30,production.ResourceFailure)
 initial=factory.DynamicHistoryResources(c.ART,factory.history_roots([],c.ART),8*2**30,96*2**30,production.ResourceFailure).check();require(initial['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,'original fullfresh2/cold/meta/history96 reservation')
 class Resources:
  def check(self):
   peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024);require(peak<512*2**20 and time.monotonic()-start<1800,'original whole1800/hostSELF512')
   h=history.check();f=joined.check();require(h['artifact_bytes']+20971764748+64*2**20<96*2**30 and f['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original history96/cold/free8 reservations')
   extra=0
   for p in plan['explicit_cumulative_metadata_file_pins']:
    current7(p)
    if not any(Path(p['path']).is_relative_to(Path(root))for root in roots):extra+=p['size_bytes']
   require(f['artifact_bytes']+extra<2*2**30,'original cumulative2GiB including external metadata');return dict(original_history=h,complete_joint=f,explicit_external_metadata_bytes=extra,host_SELF_peak_bytes=peak,whole_elapsed_seconds=time.monotonic()-start)
 resources=Resources();before=resources.check();fixed=unique(hf['dependencies']+[psf,phf,hf['host_source_pin']]+[c.pin(p)for p in guard_files]);owned=[]
 for p in fixed:current7(p);c.same_pin(p['path'],p)
 out.mkdir();runtime=out/'runtime';runtime.mkdir();component=out/'component';component.mkdir();(out/'a11-component').mkdir()
 shutil.copy2(support.BOUNDED,runtime/'run_bounded_dragon.py');owned.append(c.pin(runtime/'run_bounded_dragon.py'));require(owned[0]['sha256']==plan['original_bounded_Source_pin']['sha256'],'whole original bounded Source copied')
 runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-start),'a11-component',resources);require(type(runner)is full.OwnRSSSerialExecutor and runner.resources is resources,'same actual original owning runner')
 first=FirstFailure();watches=[];after=None;verified=False;result=None;inputpin=outputpin=detailpin=None
 def check_all():
  for p in fixed:
   current7(p)
   if p not in(plan['actual_current_SCI1_pin'],plan['actual_current_SCI2_context_only_pin']):c.same_pin(p['path'],p)
  for p in owned:current7(p);c.same_pin(p['path'],p)
  return resources.check()
 def run(label,cmd):
  check_all();runner.execute(component,label,cmd,600);watches.append(helper.check_watch(out,runner.records[-1]));check_all()
 try:
  codec=source_module(plan['original_NX_core_byte_reader_pin'],'a11_original_bounded_NX');evidence=metadata(plan['actual_GENDF_evidence_pin']);prior=metadata(plan['actual_prior_binary_bypass79_report_pin']);records=prior['temperature_diagnostics'];require(len(records)==79 and sum(r['original_NX_words']for r in records)==9294,'same original all79/9294 actual domain')
  table={r['nuclide']:r for r in evidence['actual_extractions']};cache={};native_input=component/'input79.bin';expected=[];sci=codec.BoundedSCI(plan['actual_current_SCI1_pin'],resources.check)
  try:
   with native_input.open('xb')as f:
    f.write(b'NXA11I01'+struct.pack('<2i',370,79))
    for row in records:
     resources.check();name=row['nuclide'];p=table[name]['actual_complete_extraction_pin']
     if name not in cache:cache.clear();cache[name]=metadata(p)
     matches=[s for s in cache[name]['actual_P0_sections']if s['mf']==3 and s['mt']==5 and s['temperature_K']==row['temperature_K']];require(len(matches)==1,'exact original saved MF3 MT5 temperature')
     sigma=codec.finite_vector(matches[0]);require(hashlib.sha256(struct.pack('<370d',*sigma)).hexdigest()==row['sigma5_all370_binary64_sha256'],'same all370 original vector bits')
     leaf=row['original_NX_leaf'];raw=sci.raw(leaf['offset_words'],leaf['words']);require(len(raw)==4*row['original_NX_words']and hashlib.sha256(raw).hexdigest()==row['original_NX_raw_sha256'],'exact selected original SCI NX bytes')
     padded=raw+b'\0'*(4*(370-row['original_NX_words']));ni=list(codec.NAMES).index(name)+1;header=struct.pack('<iid',ni,row['original_NX_words'],row['temperature_K']);f.write(header+struct.pack('<370d',*sigma)+padded)
     expected.append((row,sigma,padded));
    f.flush();os.fsync(f.fileno())
  finally:sci.close()
  inputpin=c.pin(native_input);owned.append(inputpin);check_all()
  obj=component/'original_a11_component.o';exe=component/'original_a11_component';native_output=component/'output79.bin'
  flags=['-J'+str(runtime),*plan['compile_flags_except_private_J_directory']]
  run('compile_original_a11',[plan['compiler_pin']['path'],*flags,'-c',plan['native_formatter_Source_pin']['path'],'-o',str(obj)]);owned.append(c.pin(obj));owned +=[c.pin(p)for p in runtime.glob('*.mod')]
  run('link_original_a11',[plan['compiler_pin']['path'],*flags,str(obj),'-o',str(exe)]);owned.append(c.pin(exe))
  run('native_original_a11',[str(exe),str(native_input),str(native_output)]);outputpin=c.pin(native_output);owned.append(outputpin)
  require(len(runner.records)==3 and all(r['status']=='PASS'for r in runner.records),'three original compile/link/native stages, no retry')
  detail=component/'all_original_NX_word_formatter_details.jsonl';total=before_count=after_count=changed=0;temperatures=[]
  with native_output.open('rb')as f,detail.open('x')as details:
   require(f.read(16)==b'NXA11O01'+struct.pack('<2i',370,79),'native exact output scope')
   for row,sigma,padded in expected:
    head=f.read(16);ni,nstored,t=struct.unpack('<iid',head);require(ni==list(codec.NAMES).index(row['nuclide'])+1 and nstored==row['original_NX_words']and t==row['temperature_K'],'native exact original record')
    bm=am=0
    for group in range(370):
     raw=f.read(43);require(len(raw)==43,'complete native word record');ig,x,field,parsed,bef,aft,exp=struct.unpack('<id11sdiii',raw)
     expectedword=struct.unpack_from('<i',padded,4*group)[0];require(ig==group+1 and struct.pack('<d',x)==struct.pack('<d',sigma[group])and exp==expectedword,'native source vector and expected SCI word exact')
     require(bef==struct.unpack('<i',struct.pack('<f',x))[0]and aft==struct.unpack('<i',struct.pack('<f',parsed))[0],'native default REAL32 cast verified independently')
     if group<nstored:
      total+=1;bm+=bef!=exp;am+=aft!=exp;changed+=bef!=aft
      details.write(json.dumps(dict(nuclide=row['nuclide'],temperature_K=t,group_one_based=ig,input_binary64_hex=struct.pack('<d',x).hex(),original_a11_character11=field.decode('ascii'),native_E11_parsed_binary64_hex=struct.pack('<d',parsed).hex(),before_raw32_hex=struct.pack('<i',bef).hex(),after_raw32_hex=struct.pack('<i',aft).hex(),original_SCI_NX_raw32_hex=struct.pack('<i',exp).hex(),before_equal_SCI=bef==exp,after_equal_SCI=aft==exp),separators=(',',':'))+'\n')
     else:require(exp==0 and aft==0,'absent trailing NX groups preserve zero; no missing-word repair')
    before_count+=bm;after_count+=am;temperatures.append(dict(nuclide=row['nuclide'],temperature_K=t,stored_NX_words=nstored,before_mismatching_words=bm,after_mismatching_words=am))
   require(f.read(1)==b'','native output exact EOF');details.flush();os.fsync(details.fileno())
  detailpin=c.pin(detail);owned.append(detailpin);require(total==9294 and before_count==sum(r['mismatching_raw_words']for r in records),'same complete real binary-bypass mismatch count')
  result=dict(schema='ACTUAL_ORIGINAL_A11_E11_REAL32_NX_COMPONENT_RESULT_V1',status='ALL79_ORIGINAL_NX_WORDS_EXPLAINED_BY_ORIGINAL_FORMATTER_COMPONENT'if after_count==0 else'ORIGINAL_FORMATTER_COMPONENT_REMAINS_MISMATCHED',stored_original_NX_words=total,temperature_records=79,before_mismatching_words=before_count,after_mismatching_words=after_count,formatter_changed_raw32_words=changed,all79_original_NX_formatter_component_equal=after_count==0,temperature_results=temperatures,private_input_full_pin=inputpin,private_native_output_full_pin=outputpin,complete_word_detail_full_pin=detailpin,actual_prior_binary_bypass79_report_pin=plan['actual_prior_binary_bypass79_report_pin'],original_formatter_statement_proof_pin=plan['original_formatter_statement_proof_pin'],**FALSE)
  report=component/'ACTUAL_ORIGINAL_A11_NX_COMPONENT_RESULT.json';c.write(report,result);owned.append(c.pin(report));check_all();require(after_count==0,'actual original formatter component does not explain every stored word');verified=True
 except BaseException as error:first.capture(error,'execute_or_component_report')
 try:after=check_all()
 except BaseException as error:first.capture(error,'after_check')
 good=first.error is None and verified;target=out/'Root_actual_original_a11_NX_component_summary.json';summary=None
 try:
  summary=dict(schema='ACTUAL_ORIGINAL_A11_NX_COMPONENT_GUARDED_REPORT_V1',status='ACTUAL_ORIGINAL_A11_NX_COMPONENT_THREE_STAGES_CLOSED0_ONLY'if good else'ACTUAL_ORIGINAL_A11_NX_COMPONENT_FAILED_NO_RETRY',failure=None if first.error is None else safe_repr(first.error),secondary_failures=first.secondary,records=runner.records,actual_watchdog_checks=watches,fixed_current_pins=fixed,complete_output_pins=[c.pin(p)for p in sorted(out.rglob('*'))if p.is_file()],actual_component_result=result,resources_before=before,resources_after=after,original_guard_MRO_unchanged=True,original_caps=CAPS,wall_seconds=time.monotonic()-start,final_report_resource_check_passed=False,**FALSE)
  c.write(target,summary);summary['resources_after_including_summary_bytes']=check_all();summary['final_report_resource_check_passed']=True;rewrite_summary(c,target,c.pin(target),summary);check_all()
 except BaseException as error:
  first.capture(error,'publication')
  if summary is not None and target.exists():
   try:summary.update(status='ACTUAL_ORIGINAL_A11_NX_COMPONENT_FAILED_NO_RETRY',failure=safe_repr(first.error),secondary_failures=first.secondary,final_report_resource_check_passed=False);rewrite_summary(c,target,c.pin(target),summary)
   except BaseException as late:first.capture(late,'failed_report_publication')
 first.reraise();require(good,'actual original formatter component only');print(json.dumps(dict(status=summary['status'],report_pin=c.pin(target),**FALSE)),flush=True)
if __name__=='__main__':main()
