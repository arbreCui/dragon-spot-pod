"""Factual failed-run metadata assessment. No original scientific-body access."""
import hashlib,json,os,resource,shlex,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parents[1]
HERE=Path(__file__).absolute().parent
ART=Path('/Users/wen/spot/validation/artifacts/axial-material-current-eight-fuel-finite18-SCAT-producer-20261015-v1')
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2147483648,history_bytes=103079215104,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864,free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
FALSE=dict(business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,
 physics_qualified=False,scientific_accuracy_qualified=False,complete_reaction_authority_qualified=False,
 physical_neutron_balance_qualified=False,unreduced_reference_qualified=False,full_reference_qualified=False,
 finite18_replayed=False,temperature_interpolation_replayed=False,current_SPH_MASK_context_applied=False,
 AAA_qualified=False,ABA_admitted=False,goal_complete=False,finite_P0_raw_words_equal_qualified=False)
SCIENCE=set()
CHECKS=[]
def require(ok,msg):
 if type(ok) is not bool or not ok:raise RuntimeError(msg)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 require(type(p) is dict and set(p)=={'path','sha256','size_bytes','identity'} and type(p['path']) is str and type(p['sha256']) is str and len(p['sha256'])==64 and all(c in '0123456789abcdef' for c in p['sha256']) and type(p['size_bytes']) is int and type(p['identity']) is list and len(p['identity'])==7 and all(type(v) is int for v in p['identity']) and p['identity'][4]==p['size_bytes'],'complete strict PF')
 q=Path(p['path']);s=q.lstat();compiler=(q==Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15') and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492' and p['identity'][3]==2)
 require(q.is_absolute() and not any(v.is_symlink() for v in(q,*q.parents)) and stat.S_ISREG(s.st_mode) and s.st_nlink==(2 if compiler else 1) and identity(s)==p['identity'],'exact unchanged current7 '+str(q))
def allowed(q,size):
 require(str(q) not in SCIENCE and q.name not in('SCI1','SCI2') and not q.name.startswith('tape') and q.suffix not in('.gz','.npy','.npz'),'original science-body read prohibited')
 require(q.is_relative_to(ART) or q.suffix in('.py','.json','.txt','.f90','.in','.sha256','.log','.make'),'Source/bounded metadata/new output only')
 require(size<8*2**20,'bounded failed-run metadata/output')
def pin(q):
 q=Path(q);s=q.lstat();allowed(q,s.st_size);p=dict(path=str(q),sha256='0'*64,size_bytes=s.st_size,identity=identity(s));current(p)
 with q.open('rb') as f:
  require(identity(os.fstat(f.fileno()))==p['identity'],'opened metadata7');p['sha256']=hashlib.file_digest(f,'sha256').hexdigest();require(identity(os.fstat(f.fileno()))==p['identity'],'whole EOF metadata7')
 current(p);return p
def whole(p):
 current(p);q=Path(p['path']);allowed(q,p['size_bytes'])
 with q.open('rb') as f:
  require(identity(os.fstat(f.fileno()))==p['identity'],'opened fullPF metadata7');b=f.read();require(identity(os.fstat(f.fileno()))==p['identity'],'EOF metadata7')
 require(len(b)==p['size_bytes'] and hashlib.sha256(b).hexdigest()==p['sha256'],'whole failed-output EOF SHA/size');current(p);return b
def read(p):return json.loads(whole(p))
def get(q):
 p=pin(q);return read(p),p
def check(s):CHECKS.append(s)
def assess(start):
 tools,pTools=get(BASE/'ROOT_ACTUAL24_TRUE_TOOL_RETURNS.json')
 require(pTools['sha256']=='7e29f9c8114dfbf2661c27647faeaf4ea8da95f2ae0b7c12536b22bf118e509a' and pTools['size_bytes']==3667,'exact retained Root actual failed tool fullPF')
 t=tools['actual_terminal_return'];initial=tools['actual_initial_return']
 require(tools['observed_closed'] is True and type(tools['original_integer_exit_code']) is int and tools['original_integer_exit_code']==1 and type(t['exit_code']) is int and t['exit_code']==1 and t.get('session_id') is None and t['chunk_id']=='6bebf4' and type(t['output']) is str and t['output'].endswith('RuntimeError: own-child wall cap reached\n') and type(initial['session_id']) is int and initial['session_id']==64179 and initial.get('exit_code') is None,'original failed Root terminal remains integer1, original live session and failure preserved')
 h,H=get(ART/'Root_actual_eight_fuel_finite18_SCAT_summary.json')
 require(H['sha256']=='6242e5652e6017d44fd2d1d8016d837917219f4c4a0c342816cdcd80f8e5f001' and H['size_bytes']==1010379,'exact actual owning failed Host fullPF')
 require(h['schema']=='ACTUAL_EIGHT_FUEL_FINITE18_SCAT_GUARDED_REPORT_V1' and h['status']=='FAILED_EIGHT_FUEL_FINITE18_SCAT_NO_RETRY' and h['failure']=="RuntimeError('own-child wall cap reached')" and h['secondary_failures']==[] and h['actual_child_receipt'] is None and h['actual_evidence'] is None and h['actual_watchdog_checks']==[] and h['original_caps']==CAPS and h['original_guard_MRO_unchanged'] is True and h['final_report_resource_check_passed'] is True and h['native_engines_started']==h['original_ASCII_files_written']==0,'actual failed noRetry run and no complete numerical comparison evidence')
 for k in ('physics_qualified','scientific_accuracy_qualified','complete_reaction_authority_qualified','physical_neutron_balance_qualified','unreduced_reference_qualified','finite18_replayed','temperature_interpolation_replayed','current_SPH_MASK_context_applied','AAA_qualified','ABA_admitted','goal_complete','full_reference_qualified'):require(h[k] is False,'failed Host scope remains unqualified')
 sf=read(h['source_freeze_pin']);hf=read(h['host_freeze_pin']);plan=read(sf['control_plan_pin'])
 science=[plan['actual_current_SCI1_pin'],plan['actual_current_SCI2_pin']]+[v['current_original_input_full_pin'] for v in plan['inputs']];SCIENCE.update(p['path'] for p in science)
 require(h['source_freeze_pin']==pin(BASE/'FINAL_SOURCE_FREEZE.json') and h['host_freeze_pin']==pin(BASE/'FINAL_HOST_FREEZE.json') and hf['selected_source_freeze_pin']==h['source_freeze_pin'] and sf['original_caps']==hf['original_caps']==plan['original_caps']==CAPS,'same original selected Source/caps')
 argv,pArgv=get(BASE/'ROOT_EXACT_ACTUAL24_ARGV.json');cli,pCLI=get(BASE/'FINAL_ROOT_REVIEWABLE_CLI.json')
 require(argv==cli['argv']==shlex.split(tools['exact_executed_command']) and len(argv)==24 and cli['source_freeze_pin']==h['source_freeze_pin'] and cli['host_freeze_pin']==h['host_freeze_pin'],'actual failed exactCLI24 remains bound to unchanged original freezes')
 check('Genuine retained Root terminal integer1 and original failure; exact owning Host/Source/CLI fullPFs; no evidence or receipt and qualifications remain false')
 outputs=h['complete_output_pins']+[H]
 require(len(outputs)==len({p['path'] for p in outputs})==6 and {str(p) for p in ART.rglob('*') if p.is_file()}=={p['path'] for p in outputs},'all six failed-run actual outputs and no unlisted comparison report')
 for p in outputs:
  require(Path(p['path']).is_relative_to(ART),'exact new failed output role');whole(p)
 require(not os.path.lexists(ART/'inventories/ACTUAL_EIGHT_FUEL_FINITE18_SCAT_EVIDENCE.json'),'no completed finite comparison evidence file')
 fixed=h['fixed_current_pins'];require(len(fixed)==len({p['path'] for p in fixed})==417,'actual417 fixed input PFs')
 require(all(p in fixed for p in hf['dependencies']+[h['source_freeze_pin'],h['host_freeze_pin'],hf['host_source_pin'],plan['actual_current_SCI1_pin']]+[v['current_original_input_full_pin'] for v in plan['inputs']]),'all original declared inputs remain in actual fixed inventory')
 for p in fixed:current(p)
 for p in science:current(p)
 require(len(h['records'])==1,'one failed own child; no retry');stage=h['records'][0]
 require(stage['status']=='FAILED' and stage['error']=='own-child wall cap reached' and stage['wall_cap_seconds']==600.0 and stage['elapsed_seconds']>=600.0,'actual single original600-second stage failure')
 stages,pStages=get(ART/'gendf-stage/stages.json');require(stages['stages']==h['records'],'exact original failed stages ledger')
 watch,pWatch=get(ART/(stage['label']+'.watchdog.json'))
 require(watch['command']==stage['command'] and type(watch['pid']) is int and type(watch['returncode']) is int and watch['returncode']==-15 and watch['limit_failure']=="RuntimeError('own-child wall cap reached')" and 0<watch['wall_cap_seconds']<=600 and watch['elapsed_seconds']>=watch['wall_cap_seconds'] and watch['rss_cap_mib']==512 and 0<watch['sampled_peak_rss_mib']<512 and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True,'own-child recorded SIGTERM and group cleanup on original wall cap, no RSS limit failure')
 cmd=stage['command'];require(len(cmd)==7 and cmd[1]=='-B' and cmd[2]==str(BASE/'compare_eight_fuel_finite18_SCAT.py') and cmd[3]=='--binding-pin' and cmd[5]=='--expected-parent-pid' and int(cmd[6])>0,'same actual owning finite worker command')
 pBinding=json.loads(cmd[4]);binding=read(pBinding)
 require(pBinding['path']==str(ART/'ACTUAL_EIGHT_FUEL_FINITE18_SCAT_EXECUTION_BINDING.json') and binding['schema']=='EIGHT_FUEL_FINITE18_SCAT_EXECUTION_BINDING_V1' and binding['source_freeze_pin']==h['source_freeze_pin'] and binding['control_plan_pin']==sf['control_plan_pin'] and binding['SCI1_whole_PF_verified_by_original_parent_before_child'] is True and binding['original_caps']==CAPS and binding['complete_joint_roots']==plan['complete_joint_roots'] and binding['explicit_cumulative_metadata_file_pins']==hf['explicit_cumulative_metadata_file_pins'],'exact original failed execution binding')
 pLog=pin(ART/(stage['label']+'.log'));require(pLog['size_bytes']==0 and whole(pLog)==b'' and pLog['sha256']==hashlib.sha256(b'').hexdigest(),'empty original worker stdout, no complete comparison receipt')
 runtime=pin(ART/'runtime/run_bounded_dragon.py');require(runtime['sha256']==plan['original_bounded_Source_pin']['sha256'],'whole original bounded runtime Source copy retained')
 check('Every six actual failed outputs fullEOF SHA/current7 first pass; all417 fixed inputs and18 original science files current7-only; one failed stage, recorded own-child SIGTERM/cleanup, original binding and empty log')
 roots=plan['complete_joint_roots'];require(len(roots)==len(set(roots))==51 and roots[-2:]==[str(BASE.parent),str(ART)],'same original51 roots include failed Source/output')
 resources=[]
 for k in ('resources_before','resources_after','resources_after_including_summary_bytes'):
  res=h[k];j=res['complete_joint'];hist=res['original_history'];cumulative=j['artifact_bytes']+res['explicit_external_metadata_bytes']+res['host_open_unlinked_bytes']
  require(j['resource_roots']==roots and j['artifact_budget_bytes']==2*2**30 and hist['artifact_budget_bytes']==96*2**30 and res['host_SELF_peak_bytes']<512*2**20 and res['whole_elapsed_seconds']<1800 and cumulative<2*2**30 and hist['artifact_bytes']+CAPS['cold_reserve_bytes']+CAPS['metadata_reserve_bytes']<96*2**30 and j['disk_free_bytes']-CAPS['cold_reserve_bytes']-2*2**30>=8*2**30,'actual Host memory/disk/history/whole-time caps retained while child stage failed')
  resources.append(dict(role=k,host_SELF_peak_bytes=res['host_SELF_peak_bytes'],host_whole_elapsed_seconds=res['whole_elapsed_seconds'],joint_and_explicit_open_unlinked_bytes=cumulative,history_bytes=hist['artifact_bytes'],disk_free_bytes=j['disk_free_bytes']))
 require(h['resources_before']['original_history']['artifact_bytes']+CAPS['cold_reserve_bytes']+CAPS['metadata_reserve_bytes']+2*2**30<96*2**30 and h['wall_seconds']<1800,'original fullfresh initial reserve and failed Host whole elapsed bound')
 unused=pin(BASE/'actual_postverify_20261015/review_actual_post.py')
 require(not os.path.lexists(BASE/'actual_postverify_20261015/REVIEW.json') and not os.path.lexists(BASE/'actual_postverify_20261015/TRUE_TOOL_RETURNS.json'),'unused passing-post Source retained; no passing actual comparison audit attempted')
 for p in fixed:current(p)
 for p in science:current(p)
 for p in outputs:whole(p)
 require(read(H)==h and read(pTools)==tools and read(pWatch)==watch and read(pStages)==stages,'same actual failure metadata after dual output/fullPF checks')
 require(pin(unused['path'])==unused,'unused passing-post Source unchanged throughout assessment')
 peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024);require(peak<512*2**20 and time.monotonic()-start<600,'bounded factual metadata auditor512/600')
 check('Six actual new outputs dual EOF/fullPF;417 fixed current7 twice;science18 current7-only twice;actual original Host resource caps, unused passing-post Source unchanged and no science completion claim')
 return dict(actual_Root_true_tools_pin=pTools,actual_Root_failure_report_pin=H,
  actual_source_freeze_pin=h['source_freeze_pin'],actual_host_freeze_pin=h['host_freeze_pin'],actual_CLI_pin=pCLI,exact_executed_argv_pin=pArgv,
  original_Root_integer_exit_code=1,original_Root_terminal_chunk_id=t['chunk_id'],actual_root_status=h['status'],actual_root_failure=h['failure'],
  actual_own_child_status='FAILED',actual_own_child_recorded_returncode=-15,actual_own_child_pid=watch['pid'],
  actual_own_child_liveness_group_cleanup_recorded=True,actual_stage_limit_seconds=stage['wall_cap_seconds'],
  actual_stage_elapsed_seconds=stage['elapsed_seconds'],actual_watchdog_limit_seconds=watch['wall_cap_seconds'],
  actual_watchdog_elapsed_seconds=watch['elapsed_seconds'],actual_watchdog_peak_rss_mib=watch['sampled_peak_rss_mib'],
  actual_Host_wall_seconds=h['wall_seconds'],actual_watchdog_pin=pWatch,actual_stage_ledger_pin=pStages,
  actual_execution_binding_pin=pBinding,actual_empty_child_log_pin=pLog,actual_original_runtime_Source_pin=runtime,
  all_actual_six_output_full_pins=outputs,all_six_new_output_dual_EOF_fullPF_checks=True,
  actual_fixed_input_full_pins=fixed,actual_fixed_input_current7_count=417,actual_fixed_input_dual_current7_checks=True,
  original_science_dual_current7_only_pins=science,original_caps=CAPS,actual_Host_resource_metadata=resources,
  complete_joint_roots=roots,unused_success_post_Source_pin=unused,unused_success_post_executed=False,
  actual_complete_comparison_evidence_present=False,actual_complete_child_receipt_present=False,
  finite_comparison_coverage_unknown=True,actual_compared_words=None,actual_word_mismatch_count=None,
  actual_original_finite_P0_equality_unknown=True,actual_failed_pipeline_reclassified_as_success=False,
  post_auditor_SELF_peak_bytes=peak)
def main():
 start=time.monotonic();failure=None;facts={};target=HERE/'REVIEW.json';require(not os.path.lexists(target),'once factual failure report; retain any failed own audit')
 try:facts=assess(start)
 except BaseException as e:failure=repr(e)
 report=dict(schema='INDEPENDENT_FAILED_EIGHT_FUEL_FINITE18_SCAT_FACTUAL_METADATA_ASSESSMENT_V1',
  status='PASS_FACTS_ONLY_ACTUAL_FAILED_FINITE18_WALL_CAP_NO_COMPLETION_EVIDENCE' if failure is None else 'FAIL_FAILED_FINITE18_FACTUAL_METADATA_ASSESSMENT',
  failure=failure,metadata_only=True,audit_source_pin=pin(Path(__file__).absolute()),
  gzip_payload_read_by_peer=False,SCI_payload_read_by_peer=False,original_ASCII_payload_read_by_peer=False,
  sciencebody_imported_or_executed=False,business_rerun_by_peer=False,native_engines_started_by_peer=0,matrix_math_recomputed_by_peer=False,
  scope='Factual metadata assessment of original integer1 guarded run at child600 wall cap only. No complete finite comparison report exists; finite P0 equality and coverage remain unknown; no finite18/material/reaction/SPH/physics/reference/AAA/ABA qualification.',
  **FALSE,**facts,checks_completed=CHECKS,elapsed_seconds=time.monotonic()-start)
 with target.open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(dict(status=report['status'],review_pin=pin(target),**FALSE)),flush=True)
 require(failure is None,'factual failure assessment own failure retained: '+str(failure))
if __name__=='__main__':main()
