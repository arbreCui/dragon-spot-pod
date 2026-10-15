"""Prepared only; requires genuine externally selected actual receipt full pins."""
from pathlib import Path
import argparse,hashlib,json,os,stat,subprocess,time,resource,shlex
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011');S=REC/'v11_pair_rank_type_pretransport_combination_memory_diagnostic_source_v2';A=REC/'v11_pair_rank_type_pretransport_combination_memory_diagnostic_v2_author_review_20261013';OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-v11-pair-rank-type-pretransport-combination-memory-diagnostic-20261013-v2');D=REC/'independent_single_pair_rank_type_v2_actual_postverify_20261013';START=time.monotonic();full={};checks=0
def require(ok,why):
 global checks
 checks+=1
 if not ok:raise AssertionError(why)
 if time.monotonic()-START>=1800 or resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20:raise RuntimeError('original readonly review SELF512/whole1800')
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p,wanted=None):
 p=Path(p);i=identity(p.lstat());require(stat.S_ISREG(i[2]),'ordinaryfile')
 if str(p)in full:
  q=full[str(p)];require(q['identity']==i and(wanted is None or q==wanted),'unchanged completecurrentPF');return q
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();n=0
 try:
  require(identity(os.fstat(fd))==i,'sameFD before')
  while True:
   b=os.read(fd,2**20)
   if not b:break
   h.update(b);n+=len(b)
  require(identity(os.fstat(fd))==i,'sameFD fullEOF')
 finally:os.close(fd)
 require(identity(p.lstat())==i and n==i[4],'fullpath all7EOF')
 q=dict(path=str(p),sha256=h.hexdigest(),size_bytes=n,identity=i);require(wanted is None or q==wanted,'exactfullPF');full[str(p)]=q;return q
def read(p):
 q=pin(p);b=Path(p).read_bytes();require(hashlib.sha256(b).hexdigest()==q['sha256']and identity(Path(p).lstat())==q['identity'],'completeJSON currentPF');return json.loads(b)
def ext(path,sha,seven):
 q=pin(path);require(q['sha256']==sha and q['identity']==json.loads(seven),'mandatoryactual externalselectedSHA/all7');return q,read(path)
def main():
 p=argparse.ArgumentParser()
 for prefix in('report','root-receipt'):
  for suffix in('path','sha256','seven-id'):p.add_argument('--'+prefix+'-'+suffix,required=True)
 args=p.parse_args();rp,report=ext(args.report_path,args.report_sha256,args.report_seven_id);tp,tool=ext(args.root_receipt_path,args.root_receipt_sha256,args.root_receipt_seven_id)
 require(rp['path']==str(OUT/'DIAGNOSTIC_REVIEW.json'),'onlycurrentv2actualreport')
 require(tool['observed_closed']is True and tool['original_integer_exit_code']==0 and tool['terminal']['exit_code']==0,'Root realterminalclosed0diagnostic only')
 require(tool['initial']['chunk_id']=='7bcd4d'and tool['initial']['session_id']==16524,'exactRoot actuallaunch')
 cli=read(A/'ROOT_EXACT_SINGLE_DIAGNOSTIC_ARGV_SOURCE_ONLY.json');hf=read(S/'COMPLETE_DIAGNOSTIC_HOST_SOURCE_FREEZE.json');authority=read(S/'INPUT_AUTHORITY.json')
 require(tool['schema']=='ROOT_ACTUAL_SINGLE_PAIR_RANK_TYPE_DIAGNOSTIC_V2_TRUE_TOOL_RETURNS_V1'and tool['actual_report_pin']==rp and tool['executed_exact_cli_pin']==pin(A/'ROOT_EXACT_SINGLE_DIAGNOSTIC_ARGV_SOURCE_ONLY.json')and shlex.split(tool['executed_command'])==cli['argv'],'Root exactactualCMD CLIandreport fullPF')
 require(report['status']=='SINGLE_PRETRANSPORT_DIAGNOSTIC_COMPLETE_ONLY'and report['primary_error']is None and report['after_check_errors']==[]and report['monitor_errors']==[]and report['cap_observations']==[],'actualallerrorsnone')
 require(report['child_execute_error']=='RuntimeError: own-child stage failed; no retry'and report['new_actual_stage_count']==1 and report['new_actual_stage_indices']==[45],'one newtrueexpectednegative')
 require(report['old45_only_historical_baseline']is True and report['old45_reexecuted']is False and report['old45_counted_as_new_PASS']is False and report['old45_prefix_unchanged']is True and report['original_v11_closed50_succeeded']is False,'old45 neverchanged/reexecuted/qualified')
 require(report['final_all7_completed']is True and report['exact_original_guard_class_MRO_serializer_rusage_unmodified']is True,'originalguard/fullpins actualcompleted')
 require(all(report[k]is False for k in('engineering_qualified','AAA_qualified','ABA_admitted','goal_complete')),'diagnostic only no qualification')
 limits=dict(child_stage_seconds=600,whole_seconds=1800,SELF_bytes=512*2**20,child_rss_mib=512,history_bytes=96*2**30,fresh_bytes=2*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,min_free_bytes=8*2**30)
 require(report['original_limit_values']==limits and 0<report['wall_seconds']<1800 and 0<=report['SELF_peak_bytes']<512*2**20,'unchanged actualcaps')
 old=read(authority['old_raw_record_pin']['path']);oldledger=read(authority['old_stage_ledger_pin']['path']);newledger=read(OUT/'AAA3-streaming/stages.json');records=newledger['stages']
 require(oldledger=={'stages':old['records']}and len(old['records'])==45 and len(records)==46 and records[:45]==old['records'],'genuine completeunmodified historical45 allresources+new1')
 record=records[45];w=read(OUT/'AAA/pair_rank_type.watchdog.json');logpin=pin(OUT/'AAA/pair_rank_type.log');log=Path(logpin['path']).read_text()
 require(record['label']=='AAA/pair_rank_type'and record['status']=='FAILED'and record['error']=='own-child stage failed; no retry'and'log_sha256'not in record,'real newnegative fieldshape')
 require(record['command']==w['command']==[str(OUT/'runtime/Dragon')]and type(w['returncode'])is int and w['returncode']==1 and w['limit_failure']is None,'genuine exactnewchildexit1 command')
 require(w['rss_cap_mib']==512 and w['own_child_only']is True and w['liveness_group_cleanup']is True and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=record['wall_cap_seconds']<=600 and 0<=w['sampled_peak_rss_mib']<512,'genuine childcaps/watchclosed')
 forbidden=['SPOR64_BOOTB64-CENSUS:','ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1','ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE','ACTUAL-AAA3-NATIVE-GLOBAL-COMPLETE','SPOT-R64 B2I BOOTSTRAP COMMITTED','SPOT-X-REAL64-TERMINAL']
 require(log.count(authority['expected_abort'])==1 and all(x not in log for x in forbidden),'expectedabortexactly1 no positivesolvertrace')
 refusal=report['new_actual_refusal'];require(refusal['actual_log_pin']==logpin and refusal['actual_watchdog_pin']==pin(OUT/'AAA/pair_rank_type.watchdog.json')and refusal['original_full46_ledger_pin']==pin(OUT/'AAA3-streaming/stages.json')and refusal['original_execution_record_index']==45 and refusal['all_actual_assertions_completed']is True,'actualrefusalowns exactlogwatchledger PF')
 require(report['historical_current_owned_pins']==old['owned_runtime_pins']and len(report['historical_current_owned_pins'])==163,'alloldowned163 protected')
 for q in [hf['host_source']]+hf['source_files']+hf['dependencies']+old['fixed_current_pins']+report['historical_current_owned_pins']+report['new_owned_copy_and_archival_pins']+report['observed_existing_outputs_before_receipt']+[authority['old_raw_record_pin'],authority['old_stage_ledger_pin']]:pin(q['path'],q)
 for entry in authority['inputs']:
  pin(entry['source_pin']['path'],entry['source_pin']);target=OUT/'runtime'/entry['destination_name']if entry['role']=='original_runtime'else OUT/'AAA'/entry['destination_name'];q=next(x for x in report['new_owned_copy_and_archival_pins']if x['path']==str(target))
  require(q['sha256']==entry['source_pin']['sha256']and q['size_bytes']==entry['source_pin']['size_bytes']and q['identity'][:2]!=entry['source_pin']['identity'][:2]and q['identity'][3]==1,'all12true independent owncopy unchanged')
 sample=record['resource_before'];require(sample['artifact_budget_bytes']==96*2**30 and sample['min_free_bytes']==8*2**30 and sample['fresh_output']['artifact_budget_bytes']==2*2**30,'newactualresource snapshotoriginal caps')
 require(sample['artifact_bytes']+20971764748+64*2**20<96*2**30 and sample['fresh_output']['artifact_bytes']<2*2**30 and sample['fresh_output']['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'newactualresource snapshot truthfulbudget')
 require(all(0<=m['ru_maxrss_bytes']<512*2**20 and m['elapsed_seconds']<1800 for m in report['measurements']),'all truephase measurements limits')
 proc=subprocess.run(['/bin/ps','-axo','pid=,pgid='],capture_output=True,text=True,timeout=2);require(proc.returncode==0 and not any(int(line.split()[1])==w['pid']for line in proc.stdout.splitlines()if len(line.split())==2),'real ownchildgroup absent independentread')
 for q in full.values():require(identity(Path(q['path']).lstat())==q['identity'],'all originalSource/input/ownedcurrent7 stable afterEOF')
 phases={}
 for m in report['measurements']:phases[m['phase']]=max(phases.get(m['phase'],0),m['ru_maxrss_bytes'])
 result=dict(schema='INDEPENDENT_V2_SINGLE_ACTUAL_PRETRANSPORT_DIAGNOSTIC_POSTVERIFY_V1',status='PASS_ACTUAL_SINGLE_DIAGNOSTIC_ONLY_NOT_50_OR_SCIENCE',actual_report_fullpin=rp,actual_Root_true_tool_receipt_fullpin=tp,all_verified_source_input_owned_output_fullpins=list(full.values()),checks=checks,unique_EOF_files=len(full),unique_EOF_bytes=sum(q['size_bytes']for q in full.values()),Root_terminal_exit_code=0,actual_guard_child_returncode=1,old45_allrecords_unchanged=True,newactual_stage_count=1,exactabort_once=True,no_positive_solver_trace=True,original_caps_unchanged=True,actual_self_peak_bytes=report['SELF_peak_bytes'],actual_phase_peak_bytes=phases,actual_child_peak_RSS_MiB=w['sampled_peak_rss_mib'],real_group_absent=True,Root_exact_CMD_and_CLI_and_report_current_fullPF_verified=True,compiler_or_guard_or_Dragon_executed_by_reviewer=False,Source_or_record_modified=False,cleanup_executed=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 D.mkdir()
 with(D/'REVIEW.json').open('x')as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(dict(status=result['status'],review_pin=pin(D/'REVIEW.json'),checks=checks,unique_EOF=len(full),actual_SELF=report['SELF_peak_bytes'],actualphase=phases)))
if __name__=='__main__':main()
