"""UNREADY extract-only Source/control contract; no worker or decoder on import."""
import hashlib,importlib.util,json,os,stat,sys
from pathlib import Path
R=Path('/Users/wen/spot');BASE=Path(__file__).absolute().parent
IO=BASE.parent/'current_extra_reaction_source_v2/B_only_observer_IO_source_v1'
OUT=R/'validation/artifacts/axial-material-current-B55-OVERV-original-native-integer-control-20261015-v1'
OUTPUT_BOUND=16*2**20;SOURCE_BOUND=16*2**20
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(physics_qualified=False,historical_machine_bit_replay=False,historical_native_RAM_bits_verified=False,original_XSM_memory_bits_verified=False,complete_reaction_authority_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,A_control_reused=False)
def need(v,m):
 if v is not True:raise RuntimeError(m)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and identity(s)==p['identity']and s.st_size==p['size_bytes'],'exact ordinary Source/control/input current7');return q
def pin(q):
 q=Path(q);s=q.lstat();h=hashlib.sha256()
 with q.open('rb')as f:
  need(identity(os.fstat(f.fileno()))==identity(s),'opened Source/control current7')
  while True:
   b=f.read(2**20)
   if not b:break
   h.update(b)
  need(identity(os.fstat(f.fileno()))==identity(s),'EOF Source/control current7')
 p=dict(path=str(q),sha256=h.hexdigest(),size_bytes=s.st_size,identity=identity(s));current(p);return p
def metadata(p):
 q=current(p);need(p['size_bytes']<8*2**20,'bounded metadata8MiB');raw=q.read_bytes();need(hashlib.sha256(raw).hexdigest()==p['sha256'],'metadata complete SHA');v=json.loads(raw);current(p);return v
def source(p,name):
 need(pin(p['path'])==p,'whole frozen Source fullPF');spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);current(p);return m
def unique(rows):
 t={}
 for p in rows:
  if p['path']in t:need(t[p['path']]==p,'same path one fullPF')
  t[p['path']]=p
 return list(t.values())
def write(q,v):
 raw=(json.dumps(v,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20,'metadata report6MiB')
 if Path(q).is_relative_to(BASE):need(sum(x.stat().st_size for x in BASE.rglob('*')if x.is_file())+len(raw)<SOURCE_BOUND,'whole Source/metadata16MiB including new output')
 with Path(q).open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
def genuine(v,key,p,outkey):
 t=v[key];need(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==0 and type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None,'genuine closed typed0')
 need(json.loads(t['output'].strip().splitlines()[-1])[outkey]==p,'genuine return exact artifact PF')
def admit(packet):
 need(packet['schema']=='CURRENT_B55_OVERV_CONTROL_PENDING_ACTUAL_BINDINGS_V1'and packet['actual_business_preconditions_closed']is True and packet['actual_B_extraction_and_post_roles_audited']is True and packet['original_caps']==CAPS,'future NULL current B extraction/control bindings remain UNREADY')
 bridge=source(packet['B55_metadata_and_commands_Source_pin'],'B55_current_metadata_bridge');interface=source(packet['B55_input_interface_Source_pin'],'B55_current_input_interface')
 descriptor,selected=bridge.admit_actual_B55_metadata(packet,metadata,current,interface)
 latest=metadata(packet['latest_complete_plan_pin']);roots=packet['complete_joint_roots'];capture_binding=metadata(packet['actual_B_input_binding_pin']);prefix=capture_binding['complete_latest_prefix_roots']+[capture_binding['actual_output_root']]
 need(latest['complete_joint_roots']==roots[:-1]and roots[:-1][:len(prefix)]==prefix and roots[-1]==str(OUT)and len(roots)==len(set(roots))and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'whole exact latest capture/extraction/failure prefix plus one owning control root')
 need(packet['planned_actual_output_root']==str(OUT)and not os.path.lexists(OUT)and any(BASE.is_relative_to(Path(p))for p in roots[:-1]),'fresh once counted owning control root; Source counted under original FTOP')
 need(packet['bounded_new_control_output_reservation_bytes']==OUTPUT_BOUND and packet['bounded_new_Source_metadata_reservation_bytes']==SOURCE_BOUND and packet['future_aggregate_budget_added_to_this_stage']is False,'only complete current B55 control16MiB+Source16MiB')
 build=metadata(packet['original_guard_build_plan_pin']);bm=source(packet['original_guard_build_contract_Source_pin'],'B55_original_guard_build_contract');bm.admit_lifecycle(build)
 for p in packet['explicit_cumulative_metadata_file_pins']:bm.current_metadata_role(p,build)
 for p in packet['inherited_metadata_current7_pins']:bm.current_metadata_role(p,build)
 for p in [packet['original_compiler_pin'],*packet['original_four_archive_pins']]:bm.current_metadata_role(p,build)
 need(packet['original_Common_Source_pin']==build['original_Common_Source_pin']and packet['original_support_Source_pin']==build['original_support_Source_pin']and packet['original_bounded_Source_pin']==build['original_bounded_Source_pin'],'unchanged original private guard Source roles')
 return build,bm,descriptor,selected,bridge,capture_binding,latest
