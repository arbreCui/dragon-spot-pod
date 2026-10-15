"""Root-only metadata and bounds for non-scientific FD startup controls; no import-time execution."""
import hashlib,importlib.util,json,os,stat,sys
from pathlib import Path
R=Path('/Users/wen/spot');BASE=Path(__file__).absolute().parent
OUT=R/'validation/artifacts/axial-material-current-readonly-FD-same-PID-exec-control-20261016-v1'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
OUTPUT_BOUND=32*2**20;SOURCE_BOUND=8*2**20
FALSE=dict(scientific_native_payload_opened=False,scientific_native_payload_hashed=False,production_FD_launcher_qualified=False,PACK_produced=False,new_B_formal13_compatible=False,online_BOOT_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
def need(v,m):
 if v is not True:raise RuntimeError(m)

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def current(p,system_compiler=None):
 q=Path(p['path']);s=q.lstat();fortran=q==Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15')and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and s.st_nlink==p['identity'][3]==2
 system=p==system_compiler and q==Path('/Library/Developer/CommandLineTools/usr/bin/clang')and s.st_uid==0 and s.st_nlink==1 and bool(s.st_mode&0o111)
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and(s.st_nlink==1 or fortran)and identity(s)==p['identity']and s.st_size==p['size_bytes']and(s.st_uid==os.getuid()or system),'exact frozen current7, only explicit existing compiler role may be system owned')
 return q

def pin_source(q):
 q=Path(q);s=q.lstat();h=hashlib.sha256()
 with q.open('rb')as f:
  need(identity(os.fstat(f.fileno()))==identity(s),'opened Source/metadata7')
  while True:
   b=f.read(2**20)
   if not b:break
   h.update(b)
  need(identity(os.fstat(f.fileno()))==identity(s),'EOF Source/metadata7')
 p=dict(path=str(q),sha256=h.hexdigest(),size_bytes=s.st_size,identity=identity(s));current(p);return p

def metadata(p):
 current(p);need(p['size_bytes']<8*2**20,'metadata8MiB');raw=Path(p['path']).read_bytes();need(hashlib.sha256(raw).hexdigest()==p['sha256'],'metadata wholeSHA');v=json.loads(raw);current(p);return v

def source_module(p,name):
 need(pin_source(p['path'])==p,'whole Source fullPF');spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);current(p);return m

def genuine(v,key,p,output_key,code=0):
 t=v[key];need(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==code and type(t['exit_code'])is int and t['exit_code']==code and t.get('session_id')is None,'genuine original closed typed return')
 need(json.loads(t['output'].strip().splitlines()[-1])[output_key]==p,'genuine return binds exact artifact PF')

def unique(rows):
 t={}
 for p in rows:
  if p['path']in t:need(t[p['path']]==p,'one exact fullPF per path')
  t[p['path']]=p
 return list(t.values())


_CONTEXT=None
def current_metadata_role(p,plan):
 global _CONTEXT
 if _CONTEXT is None:_CONTEXT=(metadata(plan['original_guard_build_plan_pin']),source_module(plan['original_guard_build_contract_Source_pin'],'FD_control_exact_B3_metadata_roles'))
 build,bm=_CONTEXT;bm.current_metadata_role(p,build)
def admit(plan):
 need(plan['schema']=='ROOT_NONSCIENTIFIC_READONLY_FD_SAME_PID_EXEC_CONTROL_PLAN_V1'and plan['actual_runtime_build_and_independent_post_closed']is True and plan['original_caps']==CAPS and plan['bounded_new_output_reservation_bytes']==OUTPUT_BOUND and plan['bounded_own_Source_metadata_receipts_bytes']==SOURCE_BOUND,'new fixture-only control exact caps and true prerequisites, NULL hard reject')
 p=metadata(plan['runtime_actual_post_pin']);tools=metadata(plan['runtime_actual_post_tools_pin']);root=metadata(plan['runtime_Root_tools_pin']);host=metadata(plan['runtime_Host_report_pin']);genuine(tools,'actual_review_return',plan['runtime_actual_post_pin'],'review_pin');genuine(root,'actual_terminal_return',plan['runtime_Host_report_pin'],'report_pin')
 need(p['schema']=='B_PLANE2_RUNTIME_COMPLETE71_BUILD_ACTUAL_METADATA_POSTVERIFY_V1'and p['status']=='PASS_ACTUAL_B_PLANE2_THREE_COMPILE_COMPLETE71_LINK_ROOT0_FOUR_CHILD0_METADATA_ONLY_NO_RUNTIME_QUALIFICATION'and p['failure']is None and type(p['actual_Root_integer_exit_code'])is int and p['actual_Root_integer_exit_code']==0 and p['actual_child_integer_exit_codes']==[0,0,0,0]and all(type(x)is int for x in p['actual_child_integer_exit_codes'])and p['actual_Host_report_pin']==plan['runtime_Host_report_pin']and p['actual_Root_tools_pin']==plan['runtime_Root_tools_pin'],'genuine runtime compile/link Root0 and separate actual metadata0, no old missing raw invented')
 need(p['actual_new_Dragon_pin']==plan['retained_new_runtime_pin']and p['new_runtime_compile_link_only_not_executed']is True and p['new_B_formal13_compatible']is p['online_BOOT_qualified']is p['physics_qualified']is False,'only build facts consumed; no context or science claim')
 need(plan['complete_joint_roots']==p['complete_joint_roots']+[str(OUT)]and len(plan['complete_joint_roots'])==len(set(plan['complete_joint_roots']))==85 and not any(Path(x).is_relative_to(Path(y))for x in plan['complete_joint_roots']for y in plan['complete_joint_roots']if x!=y)and any(BASE.is_relative_to(Path(x))for x in p['complete_joint_roots'])and not os.path.lexists(OUT),'entire latest84 plus one fresh whole control85, Source already counted under FTOP')
 need(host['records']==p['actual_four_stage_records']and len(host['records'])==4 and all(x['status']=='PASS'for x in host['records'])and host['actual_ordered71_link_inputs']==p['actual_ordered71_link_inputs'],'actual new complete71/four stage0 metadata')
 return p
def retained(plan):
 for p in plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']+plan['retained_B2_current_epoch_readonly_pins']+plan['selected31_current_epoch_readonly_pins']:current_metadata_role(p,plan)
 for p in plan['retained_failed_v1_current7_only_pins']+plan['retained_failed_pool_archive_current7_only_pins']:need(set(p)=={'path','size_bytes','identity'},'failed rows remain only three-field stat roles');current(p)
 need(len(plan['exact59_historical_absent_pins'])==59,'only known exact59 historical paths')
 for p in plan['exact59_historical_absent_pins']:need(not os.path.lexists(p['path']),'known history absent only')
