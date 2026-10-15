"""UNREADY production PACK-only metadata contract; no compiler, native or file import action."""
import hashlib,importlib.util,json,os,stat,sys
from pathlib import Path
R=Path('/Users/wen/spot');BASE=Path(__file__).absolute().parent
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-current-B-small-axial-engineering-continuation-20261016-v1')
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
OUTPUT_BOUND=128*2**20;SOURCE_BOUND=8*2**20
FALSE=dict(GLOBAL_or_PROJECT_produced=False,all_transitive_inputs_recertified=False,new_B_formal13_compatible=False,online_BOOT_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
_CONTEXT=None
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

def current_metadata_role(p,plan):
 global _CONTEXT
 if _CONTEXT is None:_CONTEXT=(metadata(plan['original_guard_build_plan_pin']),source_module(plan['original_guard_build_contract_Source_pin'],'FD_control_exact_B3_metadata_roles'))
 build,bm=_CONTEXT;bm.current_metadata_role(p,build)

def retained(plan):
 for p in plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']+plan['retained_B2_current_epoch_readonly_pins']+plan['selected31_current_epoch_readonly_pins']:current_metadata_role(p,plan)
 for p in plan['retained_failed_v1_current7_only_pins']+plan['retained_failed_pool_archive_current7_only_pins']:need(set(p)=={'path','size_bytes','identity'},'failed rows remain only three-field stat roles');current(p)
 need(len(plan['exact59_historical_absent_pins'])==59,'only known exact59 historical paths')
 for p in plan['exact59_historical_absent_pins']:need(not os.path.lexists(p['path']),'known history absent only')


EXPECTED_CONFIG={'axial_acce_accel': 0, 'axial_acce_free': 3, 'cells_per_zone': 16, 'eps_axial': 5e-08, 'eps_mccg': 2.5e-08, 'eps_radial': 2.5e-07, 'maxinr': 740, 'maxout': 500, 'radial_acce_accel': 3, 'radial_acce_free': 3, 'rank': 1, 'sn': 32, 'zone_height_cm': 50.0}
def admit_prior_frozen_configuration_metadata(plan):
 need(plan['schema']=='CURRENT_A1_B2_A3_SMALL_B_AXIAL_ENGINEERING_CONTEXT_PLAN_V1'and plan['actual_PACK_Root0_and_independent_post0_closed']is True and plan['original_caps']==CAPS and plan['bounded_new_output_reservation_bytes']==OUTPUT_BOUND and plan['bounded_own_Source_metadata_receipts_bytes']==SOURCE_BOUND,'genuine PACK0/post0/full87 conditional128+Source8 required')
 four=[plan[k]for k in('PACK_Root_report_pin','PACK_Root_tools_pin','PACK_actual_post_pin','PACK_actual_post_tools_pin')];need(all(p is not None for p in four),'four true current PACK closure PFs cannot be NULL')
 r=metadata(four[0]);raw=metadata(four[1]);p=metadata(four[2]);pt=metadata(four[3]);genuine(raw,'actual_terminal_return',four[0],'report_pin');genuine(pt,'actual_review_return',four[2],'review_pin')
 need(r['schema']=='ROOT_CURRENT_A1_B2_A3_COMPLETE18_PACK_READONLY_FD_REPORT_V1'and r['status']=='PASS_ACTUAL_A1_B2_A3_COMPLETE18_PACK_ONLY_NATIVE0_INDEPENDENT_READBACK0'and r['failure']is None and r['final_report_resource_check_passed']is True,'actual full independent PACK18 readback Root0')
 need(p['schema']=='A1_B2_A3_COMPLETE18_PACK_FD_ACTUAL_METADATA_POSTVERIFY_V1'and p['status']=='PASS_ACTUAL_A1_B2_A3_COMPLETE18_PACK_ROOT0_CHILD0_ROOT_SCIENTIFIC_READBACK_RECORDED_METADATA_ONLY'and p['metadata_only']is True and p['failure']is None and p['actual_Host_report_pin']==four[0]and p['actual_Root_tools_pin']==four[1]and type(p['actual_Root_integer_exit_code'])is int and p['actual_Root_integer_exit_code']==0 and type(p['actual_child_integer_exit_code'])is int and p['actual_child_integer_exit_code']==0 and p['Root_recorded_full18_and_three_RCON_and_strict_plane_readback_verified']is True,'independent PACK0/post0 genuine prior stages, not inferred compatibility')
 need(plan['PACK_full_pin']==r['actual_complete_PACK_pin']==p['actual_complete_PACK_pin']and plan['ordered_three_plane_RCON_pins']==r['actual_ordered_three_RCON_pins']==p['actual_ordered_three_RCON_pins']and len(p['actual_independent_complete18_tree_proofs'])==18 and len(p['actual_independent_three_RCON_tree_proofs'])==3 and len(p['actual_independent_strict_plane_case_epoch_type4_keff_proofs'])==3,'exact newly produced PACK and original A1/B2/A3 plane contracts')
 f=metadata(plan['formal_prepared_current_epoch_full_pin']);di=metadata(plan['formal_deck_inputs_current_epoch_full_pin']);spec=metadata(plan['formal_case_spec_current_epoch_full_pin'])
 need(f['production_config']==di['config']==plan['production_config']==EXPECTED_CONFIG and di['shared_basis_required']is True and di['training_slots']==spec['basis']['training_slots']==['A','B','A']and spec['basis']['requested_rank']==1 and spec['basis']['fixed_once_for_both_cases']is True,'exact frozen48cell SN32 rank1 parameters, fresh common basis trained once from current A1/B2/A3')
 need([(x['plane'],x['material'],x['expected_case'])for x in plan['producers']]==[(1,'A','R64WARM-A-V1 '),(2,'B','R64WARM-B-V1 '),(3,'A','R64-A3-WARM1 ')]and plan['global_case_name']=='PIN-ABA'and plan['old_allA_basis_or_context_reused']is False,'new B-bearing engineering only; global declaration is not native plane case')
 for role,name in(('white_tracking','white_tracking'),('make_route_contract','make_route_contract')):
  candidate=plan['small_tool_saved_SHA_and_current7_candidate_roles'][role];need(set(candidate)=={'path','sha256','size_bytes','identity'}and candidate['path']==f['runtime_sources'][name]['path']and candidate['sha256']==f['runtime_sources'][name]['sha256'],'exact old declared tool SHA plus candidate current7, not preclaimed Root proof');current(candidate)
 need(plan['small_tools_current_epoch_EOF_proof_not_yet_executed']is True,'new exact Root byteproof must run after claim before small tool invocation')
 retained(plan);return p

def admit(plan):
 need(plan['schema']=='CURRENT_B_SMALL_AXIAL_ENGINEERING_CONTINUATION_PLAN_V1'and plan['actual_prior_Root1_and_independent_failure_post0_closed']is True and plan['original_caps']==CAPS and plan['bounded_new_output_reservation_bytes']==OUTPUT_BOUND and plan['bounded_own_Source_metadata_receipts_bytes']==SOURCE_BOUND,'real prior failurefacts0 and full88 conditional128+Source8 required')
 previous=metadata(plan['prior_failed_execution_plan_pin']);admit_prior_frozen_configuration_metadata(previous)
 four=[plan[k]for k in('prior_failed_Root_report_pin','prior_failed_Root_tools_pin','prior_failure_actual_post_pin','prior_failure_actual_post_tools_pin')];need(all(p is not None for p in four),'prior real Root1/child0/failurepost0 proof cannot remain NULL')
 h=metadata(four[0]);raw=metadata(four[1]);p=metadata(four[2]);pt=metadata(four[3]);genuine(pt,'actual_review_return',four[2],'review_pin');terminal=raw['actual_terminal_return'];cli=metadata(plan['prior_exact_executed_Root_CLI_pin'])
 need(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and raw['original_integer_exit_code']==1 and type(terminal['exit_code'])is int and terminal['exit_code']==1 and terminal.get('session_id')is None and raw['actual_retried']is False and raw['exact_executed_command']==cli['command'],'actual original Root1 command preserved, no invented success stdout')
 need(h['schema']=='ROOT_CURRENT_B_SMALL_AXIAL_ENGINEERING_CONTEXT_REPORT_V1'and h['status']=='FAILED_CURRENT_B_SMALL_AXIAL_ENGINEERING_CONTEXT_NO_RETRY'and h['failure']=="Refusal('host marker missing: ROUTE CONTRACT SEALED:')"and h['plan_pin']==plan['prior_failed_execution_plan_pin']and h['source_pin']==previous['host_source_pin']and h['complete_source_file_pins']==previous['complete_source_file_pins'],'exact original marker failure retains original Source and PLAN')
 need(p['schema']=='CURRENT_B_SMALL_ENGINEERING_CONTEXT_ACTUAL_FAILURE_FACTS_METADATA_POST_V1'and p['status']=='PASS_FAILURE_FACTS_ONLY'and p['failure']is None and p['actual_Host_report_pin']==four[0]and p['actual_Root_tools_pin']==four[1]and type(p['actual_Root_integer_exit_code'])is int and p['actual_Root_integer_exit_code']==1 and p['actual_Host_status']==h['status']and p['actual_Host_failure']==h['failure']and p['success_or_context_or_online_qualification_inferred']is False,'genuine independent failure-facts-only0 never makes failed original Root0')
 need(h['actual_child_integer_exit_codes']==p['actual_child_integer_exit_codes']==[0,0,0,0]and [x['status']for x in h['original_stage_records']]==['PASS','PASS','PASS','FAILED']and p['original_stage_records']==h['original_stage_records']and p['actual_stage_checks']==h['actual_stage_checks']and h['original_stage_records'][3]['error']=='host marker missing: ROUTE CONTRACT SEALED:','four real original child0, original last host-marker FAILED intact')
 need([x['stage_label']for x in h['actual_stage_checks']]==['train','rank','white_tracking','make_route_contract']and h['actual_complete_engineering_scientific_readback']is None and h['actual_complete_scientific_output_pins']==[]and p['Root_saved_scientific_readback']is None and p['Root_saved_scientific_output_pins']==[],'no initial/axial or completed scientific result falsely inferred')
 for e in h['actual_stage_checks']:
  w=e['actual_watchdog'];need(type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None and w['own_child_only']is True and w['liveness_group_cleanup']is True,'four original mature native child0 closures')
 need(h['actual_fresh_complete370_rank_admission']['classification']=='VALID_RANK_INPUT_PRECISION'and h['actual_fresh_complete370_rank_admission']['requested_rank']==1 and len(h['actual_fresh_complete370_rank_admission']['groups'])==370 and p['Root_saved_rank_admission']==h['actual_fresh_complete370_rank_admission'],'prior one genuinely trained new A1/B2/A3 shared basis/rank0 retained')
 need(h['actual_Root_small_tools_fullEOF_and_stable7_verified_pins']==p['Root_saved_small_tool_proofs']==plan['small_tool_saved_SHA_and_current7_candidate_roles'],'real old tool EOF7 proof retained, neither tool repeated')
 need(plan['complete_joint_roots']==h['complete_joint_roots']+[str(OUT)]and h['complete_joint_roots']==previous['complete_joint_roots']and len(plan['complete_joint_roots'])==len(set(plan['complete_joint_roots']))==88 and not any(Path(a).is_relative_to(Path(b))for a in plan['complete_joint_roots']for b in plan['complete_joint_roots']if a!=b)and not os.path.lexists(OUT),'entire old87 including failed output plus new88, no aliases or generic skip')
 expected=['basis.xsm','axial_track_unmarked.xsm','axial_track.xsm','axial_macro.xsm','global_rcon.xsm','plane3_rcon.xsm','radial1.bin','radial2.bin','radial3.bin'];saved={Path(x['path']).name:x for x in h['whole_new_output_pins']if Path(x['path']).name in expected}
 need(plan['ordered_reused_nine_complete_full_pins']==[saved[n]for n in expected]and len(saved)==9 and sum(x['size_bytes']for x in plan['ordered_reused_nine_complete_full_pins'])==35653716,'exact nine Root-recorded full EOF files, never partial or old allA substitute')
 for row in plan['ordered_reused_nine_complete_full_pins']:current(row)
 need(plan['production_config']==previous['production_config']==EXPECTED_CONFIG and plan['PACK_full_pin']==previous['PACK_full_pin']and plan['ordered_three_plane_RCON_pins']==previous['ordered_three_plane_RCON_pins']and plan['old_allA_basis_or_context_reused']is False,'continuation keeps same newly trained B material/basis/configuration')
 retained(plan);return h,p
