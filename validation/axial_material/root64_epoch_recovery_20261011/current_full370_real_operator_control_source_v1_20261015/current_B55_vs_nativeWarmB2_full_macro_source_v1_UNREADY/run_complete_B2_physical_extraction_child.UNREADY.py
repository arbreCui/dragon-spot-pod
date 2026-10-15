"""Root-owned complete B2 physical extraction child; complete evidence exits2."""
import argparse,hashlib,importlib.util,json,os,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent

def main():
 started=time.monotonic();ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--request-pin',required=True);ap.add_argument('--contract-source-pin',required=True);ap.add_argument('--expected-parent-pid',type=int,required=True);a=ap.parse_args()
 if os.getppid()!=a.expected_parent_pid:raise RuntimeError('one original owning parent')
 pc=json.loads(a.contract_source_pin);q=Path(pc['path']);s=q.lstat();seven=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 if q!=BASE/'B2_extract_Source_contract.UNREADY.py'or seven!=pc['identity']or hashlib.sha256(q.read_bytes()).hexdigest()!=pc['sha256']:raise RuntimeError('exact frozen local contract Source')
 # Exclusive claim precedes any project import/helper or payload opening.
 # Root output is read from the bounded, exact request metadata only.
 preq=json.loads(a.request_pin);rq=Path(preq['path']);rs=rq.lstat()
 if rs.st_size>=8*2**20 or preq['size_bytes']!=rs.st_size:raise RuntimeError('request metadata bounded before read')
 raw=rq.read_bytes()
 if len(raw)>=8*2**20 or hashlib.sha256(raw).hexdigest()!=preq['sha256']or[rs.st_dev,rs.st_ino,rs.st_mode,rs.st_nlink,rs.st_size,rs.st_mtime_ns,rs.st_ctime_ns]!=preq['identity']:raise RuntimeError('exact bounded request before claim')
 request=json.loads(raw);out=Path(request['owning_host_output_directory'])
 with(out/'CHILD_B2_EXTRACTION_ONCE_CLAIM.json').open('x')as f:json.dump(dict(schema='CURRENT_B2_COMPLETE_EXTRACTION_CHILD_ONCE_CLAIM_V1',PID=os.getpid(),parent_PID=os.getppid(),original_monotonic_start=started,claim_before_project_helpers_and_payload_IO=True,retries=0),f);f.write('\n');f.flush();os.fsync(f.fileno())
 spec=importlib.util.spec_from_file_location('B2_child_contract',q);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.current(pc);m.need(m.metadata(preq)==request,'same exact request after claim')
 rb=request['root_owning_runtime_Source_binding'];sf=m.metadata(rb['source_freeze_pin']);hf=m.metadata(rb['host_freeze_pin']);packet=m.metadata(sf['control_plan_pin'])
 m.need(sf['schema']=='COMPLETE_CURRENT_B2_PHYSICAL_TREE_SOURCE_ONLY_FREEZE_V1'and sf['candidate_executed']is False and hf['schema']=='CURRENT_B2_COMPLETE_EXTRACTION_HOST_FREEZE_V1'and hf['selected_source_freeze_pin']==rb['source_freeze_pin']and hf['contract_Source_pin']==pc and rb['parent_PID']==a.expected_parent_pid,'same original owning Source/host/request/parent chain')
 build,bm,archive,retirement,bridge=m.admit(packet,True);support=m.source(packet['original_support_Source_pin'],'B2_child_original_support');m.source(packet['original_production_inputs_Source_pin'],'production_inputs')
 m.need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and Path(sys.executable).resolve()==support.PYTHON and all(os.environ.get(k)=='1'for k in support.THREAD_KEYS),'original exact interpreter/thread1/unoptimized/unprofiled')
 table={p['path']:p for p in sf['complete_source_file_pins']};m.need(len(table)==len(sf['complete_source_file_pins'])and str(Path(__file__).absolute())in table,'complete unique Source table includes executing child')
 for p in table.values():m.need(m.pin(p['path'])==p,'whole complete frozen Source table')
 original=m.source(packet['original_budget_worker_Source_pin'],'B2_child_original_complete_Bagg_budget')
 resources=m.Resources(packet,build,bm,hf['explicit_cumulative_metadata_file_pins']+[preq],started,600)
 class StageBudget:
  def __init__(self):
   self.original=original.Budget(packet['complete_joint_roots'],packet['child_ordinary_explicit_metadata_pins']);self.original.start=started;self.last_resources=None
  def check(self):
   prior=self.original.last;self.original.check();resources.light()
   if self.original.last!=prior or self.last_resources is None:
    self.last_resources=resources.check();self.original.last=time.monotonic()
  def force(self):
   self.original.last=0.0;self.check()
 budget=StageBudget();budget.force()
 def check(p,callback):
  callback();original.check(p,callback);callback();return p
 def module(name,filename,source_table,callback):
  p=source_table.get(str(BASE/filename));m.need(type(p)is dict,'every whole Source dependency in exact table');check(p,callback);v=m.source(p,name);callback();return v
 def pin(path,callback):
  callback();p=original.pin(path,callback);callback();return p
 def admit_request(r,callback):
  callback();m.need(r==request and r['actual_current_epoch_B2_archive_pin']==packet['actual_current_epoch_B2_archive_pin']and r['historical_B2_archive_pin']==packet['historical_B2_archive_pin']and r['child_output_directory']==str(out/'evidence')and r['actual_latest_complete_prefix_plan_pin']==packet['actual_latest_complete_prefix_plan_pin'],'complete current B2 exact request, not AAA replacement or alternate saved pair')
  for k in('actual_B2_current_epoch_bridge_report_pin','actual_B2_current_epoch_bridge_post_pin','actual_presence_archive_post_pin','actual_presence_retirement_post_pin','actual_B2_lineage_metadata_audit_pin'):m.need(r[k]==packet[k],'same actual prerequisite role '+k)
  helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'B2_child_original_guard_helper');full,production=helper.modules();helper.guard_admission(full)
  m.need(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT and rb['original_guard_class']=='OwnRSSSerialExecutor'and rb['original_guard_MRO_unchanged']is True and rb['owned_bounded_pin']['sha256']==packet['original_bounded_Source_pin']['sha256'],'exact unchanged private guard origin/MRO and owned bounded copy')
  m.need(m.pin(rb['owned_bounded_pin']['path'])==rb['owned_bounded_pin'],'same owned bounded Source bytes');budget.force()
 ops=dict(require=m.need,check=check,pin=pin,current7=m.current,identity=m.identity,module=module,write=m.write,admit_B2_metadata_and_original_owning_guard=admit_request)
 algorithm=module('complete_B2_original_extract_algorithm','extract_complete_nativeWarmB2_physical_tree.UNREADY.py',table,budget.check)
 report_path=algorithm.extract_complete_B2(request,Path(request['child_output_directory']),budget,table,ops);report_pin=pin(report_path,budget.check);budget.force()
 print(json.dumps(dict(status='ACTUAL_COMPLETE_NATIVEWARM_B2_EXTRACTION_EVIDENCE_ONLY_EXIT2',report_pin=report_pin,resources_after=budget.last_resources,actual_parent_PID=os.getppid(),**m.FALSE)),flush=True)
 raise SystemExit(2)
if __name__=='__main__':main()
