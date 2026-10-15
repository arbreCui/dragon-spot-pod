"""Root-only Source contract for three new Sources and complete71 link; no import action."""
import hashlib,importlib.util,json,os,stat,sys
from pathlib import Path
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
BASE=Path(__file__).absolute().parent;OUT=R/'validation/artifacts/axial-material-current-B-plane2-minimal-runtime-complete71-build-only-20261016-v1'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
OUTPUT_BOUND=32*2**20;SOURCE_BOUND=8*2**20
FLAGS=['-O2','-march=native','-ffp-contract=off','-fcheck=all','-fbacktrace','-g','-fPIC','-frecord-marker=4','-ffixed-line-length-none']
FALSE=dict(B_context_executed=False,new_B_formal13_compatible=False,GLOBAL_or_PROJECT_produced=False,online_BOOT_qualified=False,all_transitive_inputs_recertified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
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


_METADATA_CONTEXT=None
def current_metadata_role(p,plan):
 global _METADATA_CONTEXT
 if _METADATA_CONTEXT is None:
  build=metadata(plan['original_guard_build_plan_pin']);bm=source_module(plan['original_guard_build_contract_Source_pin'],'B_plane2_exact_original_B3_metadata_roles');_METADATA_CONTEXT=(build,bm)
 build,bm=_METADATA_CONTEXT;bm.current_metadata_role(p,build)
def write_once(q,v):
 raw=(json.dumps(v,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20,'each Source metadata6MiB')
 need(sum(x.lstat().st_size for x in BASE.rglob('*')if x.is_file())+len(raw)<SOURCE_BOUND,'entire new Source/metadata8MiB')
 with Path(q).open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
def load_plan(p):
 view=metadata(p);need(view['schema']=='B_PLANE2_RUNTIME_SOURCE_ONLY_PLAN_V1','exact compact PLAN schema')
 packet=metadata(view['admission_packet_pin']);need(packet['schema']=='ROOT_B_PLANE2_MINIMAL_RUNTIME_BUILD_CURRENT_ADMISSION_PACKET_V1','exact immutable complete admission packet')
 return dict(packet,**view)

def current_failed(p):
 need(set(p)=={'path','size_bytes','identity'},'only exact declared failed current7-only role, no fullPF or SHA claim');current(p)
def admit_retained(plan):
 for p in plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']+plan['retained_B2_current_epoch_readonly_pins']+plan['selected31_current_epoch_readonly_pins']:current_metadata_role(p,plan)
 for p in plan['retained_failed_v1_current7_only_pins']+plan['retained_failed_pool_archive_current7_only_pins']:current_failed(p)
 rows=plan['exact59_historical_absent_pins'];need(len(rows)==len({p['path']for p in rows})==59,'exact59 previously closed historical paths only')
 for p in rows:need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'exact59 historical absence, never generic missing-path acceptance')
def admit_lifecycle(plan):
 need(plan['actual_business_preconditions_closed']is True,'corrected actual bridge0/post0 and latest83 budget remain NULL hard reject')
 b=metadata(plan['epoch_bridge_binding_pin']);r=metadata(plan['epoch_bridge_report_pin']);raw=metadata(plan['epoch_bridge_Root_tools_pin']);p=metadata(plan['epoch_bridge_corrected_post_pin']);pt=metadata(plan['epoch_bridge_corrected_post_tools_pin'])
 genuine(raw,'actual_terminal_return',plan['epoch_bridge_report_pin'],'report_pin');genuine(pt,'actual_review_return',plan['epoch_bridge_corrected_post_pin'],'review_pin')
 need(p['schema']=='A1_A3_FORMAL31_CURRENT_EPOCH_BRIDGE_ACTUAL_METADATA_POSTVERIFY_V1'and p['status']=='PASS_ACTUAL_A1_A3_SELECTED18_FORMAL13_CURRENT_EPOCH_ROOT0_CURRENT7_METADATA_ONLY_NO_COMPATIBILITY_QUALIFICATION'and p['failure']is None and p['actual_Root_integer_exit_code']==0 and type(p['actual_Root_integer_exit_code'])is int and p['actual_bridge_report_pin']==plan['epoch_bridge_report_pin']and p['actual_Root_tools_pin']==plan['epoch_bridge_Root_tools_pin']and p['binding_pin']==plan['epoch_bridge_binding_pin'],'genuine corrected selected31 metadata post0 binds unchanged Root0')
 need('/actual_postverify_corrected_exact_two_formal_metadata_overlap_20261016/'in plan['epoch_bridge_corrected_post_pin']['path']and p['actual_Source_author_freeze_pin']==plan['epoch_bridge_author_freeze_pin']and p['all31_current_epoch_roles_current7_verified_twice']is True and p['all_retained_roles_current7_verified_twice']is True and p['actual_selected_role_count']==31 and p['actual_selected_blind_verified_bytes']==680089850,'exact corrected post namespace and whole31 bytes, no old failed post promotion')
 need(r['ordered_role_pairs']==p['ordered_role_pairs']and len(r['ordered_role_pairs'])==31 and [x['current_epoch_full_pin']for x in p['ordered_role_pairs']]==plan['selected31_current_epoch_readonly_pins']and all(x['blind_complete_SHA_and_length_equal']is True and x['before_open_EOF_after_current7_stable']is True for x in p['ordered_role_pairs']),'whole original31 current epoch byte bindings only')
 need(r['new_B_bearing_context_compatibility_or_lineage_proved']is False and p['new_B_bearing_context_compatibility_or_lineage_proved']is False and p['online_BOOT_qualified']is False and p['historical_independent_genuine_typed0_asserted']is False,'bytebridge is not formal compatibility or invented old independent success')
 need(plan['complete_joint_roots']==p['complete_joint_roots']+[str(OUT)]and p['complete_joint_roots']==b['complete_joint_roots']and len(plan['complete_joint_roots'])==84 and len(set(plan['complete_joint_roots']))==84 and not any(Path(x).is_relative_to(Path(y))for x in plan['complete_joint_roots']for y in plan['complete_joint_roots']if x!=y)and plan['original_caps']==p['original_caps']==CAPS,'entire latest83 plus one new whole build84, no subset or cap change')
 for key in('retained_archive_metadata_current7_pins','retained_B2_current_epoch_readonly_pins','retained_failed_v1_current7_only_pins','retained_failed_pool_archive_current7_only_pins','exact59_historical_absent_pins'):need(plan[key]==p[key],'same exact latest retained and historical roles')
 need(plan['retained_current7_pins']==p['retained_all_current7_pins']and plan['bridge_explicit_cumulative_metadata_file_pins']==p['explicit_cumulative_metadata_file_pins'],'latest complete current and explicit metadata roles inherited verbatim')
 need(any(BASE.is_relative_to(Path(x))for x in p['complete_joint_roots'])and not os.path.lexists(OUT),'Source within existing FTOP and new whole data root fresh once')
 op=metadata(plan['original_owned70_plan_pin']);h=metadata(plan['original_owned70_report_pin']);hr=metadata(plan['original_owned70_Root_tools_pin']);hp=metadata(plan['original_owned70_post_pin']);ht=metadata(plan['original_owned70_post_tools_pin'])
 genuine(ht,'actual_review_return',plan['original_owned70_post_pin'],'review_pin');v=hr['actual_terminal_return']
 need(hr['observed_closed']is True and type(hr['original_integer_exit_code'])is int and hr['original_integer_exit_code']==1 and type(v['exit_code'])is int and v['exit_code']==1 and v.get('session_id')is None,'old original Root1 completion parser failure retained, never rewritten0')
 need(hp['schema']=='INDEPENDENT_A8_18_OWNED_MAP_LIFETIME_V2_ACTUAL_RUNTIME_POSTVERIFICATION_V1'and hp['status']=='PASS_ACTUAL_A8_18_OWNED_MAP_LIFETIME_V2_THREE_STAGE0_COMPLETE_PAIR_FACTS_POSTVERIFIED_HOST_COMPLETION_PARSER_FAILURE_RETAINED'and hp['failure']is None and hp['actual_Root_exit_code']==1 and hp['actual_report_pin']==plan['original_owned70_report_pin']and hp['actual_Root_true_tool_return_pin']==plan['original_owned70_Root_tools_pin']and hp['actual_stage_statuses']==['PASS','PASS','PASS'],'genuine old post0 preserves Root1 and actual three child stage0 facts')
 rows=plan['original_current70_ordered_input_pins'];need(rows==op['current_owned_runtime_ordered70_pins']==hp['actual_ordered70_input_pins']and [x['path']for x in rows]==h['actual_ordered70_link_inputs']and len(rows)==len({x['path']for x in rows})==70,'exact actual latest70 complete saved inputs not original cache70')
 need(h['records'][0]['status']==h['records'][1]['status']=='PASS'and h['records'][1]['command']==plan['original_current70_link_command']and h['records'][0]['command']==plan['original_current_compile_command'],'actual old compile/link0 commands only; old business status stays unchanged')
 for p in plan['compile_and_link_input_pins']:current_metadata_role(p,plan)
 for p in plan['whole_byte_build_source_copy_pins']:need(pin_source(p['path'])==p,'new three Source full bytes only')
 admit_retained(plan);return p
def commands(plan):
 old=plan['original_current70_link_command'];rows=plan['original_current70_ordered_input_pins'];paths=[p['path']for p in rows];first=plan['original_current_compile_command'];fc=plan['original_Fortran_compiler_pin']['path']
 need(old==[fc,'-O2','-ffp-contract=off',*paths,'-o',plan['historical_original_Dragon_output_path']]and first[0]==fc and first[1:10]==FLAGS and [x for x in first if x.startswith('-I')]==plan['original_compile_include_arguments'],'exact original compiler, flags and include order authority')
 need([Path(paths[i]).name for i in(14,66)]==['KDRDRV.o','APACKX64.o']and next(i for i,x in enumerate(paths)if x.endswith('.a'))==58 and sum(x.endswith('.o')for x in paths)==66 and sum(x.endswith('.a')for x in paths)==4,'actual complete70 positions14/66 and archive58, original66objects+4archives')
 inc=['-I'+str(OUT/'sources/build')]+plan['original_compile_include_arguments'];sources=['APACKX64.f90','B2PLNX64.UNREADY.f90','KDRDRV.F'];objects=['APACKX64.o','B2PLNX64.o','KDRDRV.o'];compiles=[[fc,*FLAGS,*inc,'-J'+str(OUT/'sources/build'),'-c',str(OUT/'sources'/s),'-o',str(OUT/'sources/build'/o)]for s,o in zip(sources,objects)]
 replaced=list(paths);replaced[14]=str(OUT/'sources/build/KDRDRV.o');replaced[66]=str(OUT/'sources/build/APACKX64.o');insert=str(OUT/'sources/build/B2PLNX64.o');new=replaced[:58]+[insert]+replaced[58:]
 inverse=[x for x in new if x!=insert];inverse[14]=paths[14];inverse[66]=paths[66]
 need(inverse==paths and len(new)==len(set(new))==71 and sum(x.endswith('.o')for x in new)==67 and sum(x.endswith('.a')for x in new)==4 and [(i,a,z)for i,(a,z)in enumerate(zip(paths,replaced))if a!=z]==[(14,paths[14],replaced[14]),(66,paths[66],replaced[66])],'whole71 inverse to70: two replacements, one insertion, other68 unchanged and all archive order retained')
 return dict(compile_commands=compiles,link_command=[fc,'-O2','-ffp-contract=off',*new,'-o',str(OUT/'sources/runtime/Dragon')],ordered71_link_inputs=new,old_link_argv_inverse_equal=True)
