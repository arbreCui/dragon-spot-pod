#!/usr/bin/env python3
"""One exact diagnostic PROJECT release, gated by future real closed0 evidence.

Default is readonly. No retry or alternative target. All other diagnostic files
and the complete original v11 state remain protected. No numerical work.
"""
import argparse, hashlib, importlib.util, json, os, shlex, stat, subprocess, time
from pathlib import Path
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
ART=R/'validation/artifacts';PKG=Path(__file__).resolve().parent
DIAG=ART/'axial-material-v11-pair-rank-type-pretransport-combination-memory-diagnostic-20261013-v2'
TARGET=DIAG/'AAA/projected_boot.xsm';REPORT=DIAG/'DIAGNOSTIC_REVIEW.json';BYTES=749355952
SOURCE_HF=PKG/'COMPLETE_SINGLE_DIAGNOSTIC_PROJECT_RELEASE_SOURCE_ONLY_FREEZE.json'
RECEIPTS=REC/'diagnostic_v2_single_PROJECT_release_actual_receipts_20261013'
BASE=REC/'storage_release_closed_v7_v8_project_pair_20261013/project_pair_release_common.py'
BASE_SHA='b0a0a3d1f4eacfe8c9b91378b89aff1071a3907c2027a3fec857e160ae6e0b7d'
# Bootstrap verifies the complete original Source PF before passive import.
BASE_ID=[16777229, 49980314, 33188, 1, 18001, 1791847138307427020, 1791847138307427020]
before=BASE.lstat()
ident=lambda q:[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]
if ident(before)!=BASE_ID or not stat.S_ISREG(before.st_mode)or any(x.is_symlink()for x in(BASE,*BASE.parents)):raise RuntimeError('exact original helper Source all7')
fd=os.open(BASE,os.O_RDONLY|os.O_NOFOLLOW)
with os.fdopen(fd,'rb')as stream:
 if ident(os.fstat(stream.fileno()))!=BASE_ID or hashlib.file_digest(stream,'sha256').hexdigest()!=BASE_SHA or ident(os.fstat(stream.fileno()))!=BASE_ID:raise RuntimeError('original readonly helper exact fullEOF/all7')
if ident(BASE.lstat())!=BASE_ID:raise RuntimeError('original helper Source after7ID')
spec=importlib.util.spec_from_file_location('original_readonly_cleanup_helpers',BASE)
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)

def external(path,sha,seven):
 p=b.pin(path)
 if p['sha256']!=sha or p['identity']!=json.loads(seven):raise RuntimeError('mandatory real external all7 fullPF')
 return p

def unique(rows):
 table={}
 for row in rows:
  if row['path']in table and table[row['path']]!=row:raise RuntimeError('same path inconsistent current fullPF')
  table[row['path']]=row
 return list(table.values())

def inventory():
 files={};dirs={};stack=[DIAG]
 while stack:
  folder=stack.pop();before=folder.lstat()
  if not stat.S_ISDIR(before.st_mode)or before.st_uid!=os.getuid():raise RuntimeError('own ordinary diagnostic directory')
  dirs[str(folder)]=b.identity(before);fd=os.open(folder,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
  try:
   if b.identity(os.fstat(fd))!=dirs[str(folder)]:raise RuntimeError('directory changed at open')
   with os.scandir(fd)as entries:
    for entry in entries:
     path=folder/entry.name;s=entry.stat(follow_symlinks=False)
     if stat.S_ISDIR(s.st_mode):stack.append(path)
     elif stat.S_ISREG(s.st_mode):files[str(path)]=b.identity(s)
     else:raise RuntimeError('no symlink or special diagnostic input')
  finally:os.close(fd)
  if b.identity(folder.lstat())!=dirs[str(folder)]:raise RuntimeError('directory changed during inventory')
  b.guard()
 return dict(files=files,directories=dirs)

def no_live_writer(pid):
 ps=subprocess.run(['/bin/ps','-axo','pid=,pgid=,command='],capture_output=True,text=True,timeout=20)
 if ps.returncode:raise RuntimeError('real host process metadata unavailable')
 needles=[str(DIAG),str(REC/'v11_pair_rank_type_pretransport_combination_memory_diagnostic_source_v2/run_single_pair_rank_type_memory_diagnostic.py'),
  str(REC/'aaa_three_plane_streaming_pipeline_source_v11/run_actual_three_plane_pipeline.py')]
 for line in ps.stdout.splitlines():
  fields=line.strip().split(None,2)
  if len(fields)==3 and int(fields[0])!=os.getpid()and(int(fields[1])==pid or any(x in fields[2]for x in needles)):
   raise RuntimeError('actual owner/runtime/ownchild still live; no unlink')
 ls=subprocess.run(['/usr/sbin/lsof','-nP','+D',str(DIAG)],capture_output=True,text=True,timeout=30)
 # lsof exit1 with no output is its real no-open-file observation. All other
 # errors refuse; do not infer absence from inaccessible process metadata.
 if ls.returncode not in(0,1)or ls.stderr.strip()or ls.stdout.strip():raise RuntimeError('diagnostic namespace has open handle or lsof unavailable')
 b.guard();return dict(real_process_metadata_read=True,original_child_pgid_absent=True,lsof_returncode=ls.returncode,no_open_namespace_handles=True)

def gates(a):
 fp=external(a.source_freeze_summary,a.source_freeze_sha256,a.source_freeze_seven_id);f=b.read(fp)
 if fp['path']!=str(SOURCE_HF)or f['schema']!='EXACT_SINGLE_DIAGNOSTIC_V2_PROJECT_RELEASE_SOURCE_ONLY_FREEZE_V1' or f['future_diagnostic_report_pin']is not None or f['future_Root_true_receipt_pin']is not None or f['deletion_executed']is not False:raise RuntimeError('own immutable Source-only authority, no futurePF')
 for row in f['Source_pins']+f['dependencies']:b.same(row)
 dp=external(a.diagnostic_report_summary,a.diagnostic_report_sha256,a.diagnostic_report_seven_id)
 tp=external(a.root_true_receipt_summary,a.root_true_receipt_sha256,a.root_true_receipt_seven_id)
 if dp['path']!=str(REPORT):raise RuntimeError('exact actual v2 diagnostic report only')
 d=b.read(dp);t=b.read(tp);terminal=t.get('terminal',{})
 if t.get('schema')!='ROOT_ACTUAL_SINGLE_PAIR_RANK_TYPE_DIAGNOSTIC_V2_TRUE_TOOL_RETURNS_V1' or t.get('observed_closed')is not True or type(terminal.get('exit_code'))is not int or terminal['exit_code']!=0 or type(t.get('original_integer_exit_code'))is not int or t['original_integer_exit_code']!=0 or t.get('actual_report_pin')!=dp or t.get('executed_exact_cli_pin')!=f['diagnostic_CLI_pin']:raise RuntimeError('real Root closed0 receipt tied to actual report/exact CLI')
 cli=b.read(f['diagnostic_CLI_pin'])
 if t.get('executed_command')!=shlex.join(cli['argv']):raise RuntimeError('Root actual command equals complete reviewed diagnostic argv')
 if d.get('schema')!='ACTUAL_SINGLE_ORIGINAL_PAIR_RANK_TYPE_COMBINATION_MEMORY_DIAGNOSTIC_V1' or d.get('status')!='SINGLE_PRETRANSPORT_DIAGNOSTIC_COMPLETE_ONLY' or d.get('primary_error')is not None or d.get('after_check_errors')!=[] or d.get('monitor_errors')!=[] or d.get('cap_observations')!=[] or d.get('child_execute_error')!='RuntimeError: own-child stage failed; no retry':raise RuntimeError('only truly complete diagnostic may release; failed parent never success')
 if d.get('old45_only_historical_baseline')is not True or d.get('old45_reexecuted')is not False or d.get('old45_counted_as_new_PASS')is not False or d.get('old45_prefix_unchanged')is not True or type(d.get('new_actual_stage_count'))is not int or d['new_actual_stage_count']!=1 or d.get('new_actual_stage_indices')!=[45] or d.get('final_all7_completed')is not True or d.get('originals_and_owned_copies_deleted')is not False:raise RuntimeError('historical45/new1 complete actual scope')
 if any(d.get(k)is not False for k in ['original_v11_closed50_succeeded','engineering_qualified','AAA_qualified','ABA_admitted','goal_complete']):raise RuntimeError('no original pipeline50 or physics qualification inherited')
 if type(d.get('SELF_peak_bytes'))is not int or not 0<=d['SELF_peak_bytes']<512*2**20 or type(d.get('wall_seconds'))not in(int,float)or not 0<d['wall_seconds']<1800:raise RuntimeError('true diagnostic parent original SELF/whole caps')
 if d.get('original_limit_values')!=f['diagnostic_original_limits']or d.get('exact_original_guard_class_MRO_serializer_rusage_unmodified')is not True:raise RuntimeError('exact original diagnostic resource contract')
 authority=b.read(f['diagnostic_input_authority_pin']);hf=b.read(f['diagnostic_HF_pin'])
 raw=b.read(authority['old_raw_record_pin']);oldledger=b.read(authority['old_stage_ledger_pin'])
 if len(raw['records'])!=45 or oldledger!={'stages':raw['records']}or len(raw['fixed_current_pins'])!=2643 or len(raw['owned_runtime_pins'])!=163 or d['historical_current_owned_pins']!=raw['owned_runtime_pins']:raise RuntimeError('complete real original current2643/owned163/historical45 retained')
 if d['original_historical_raw45_pin']!=authority['old_raw_record_pin']or d['original_historical_stage45_pin']!=authority['old_stage_ledger_pin']:raise RuntimeError('exact old raw/ledger provenance')
 closure=d['new_actual_refusal'];expected=authority['expected_abort']
 if closure.get('case')!='pair_rank_type'or closure.get('expected_abort')!=expected or closure.get('original_execution_record_index')!=45 or closure.get('original_execution_record_label')!='AAA/pair_rank_type'or type(closure.get('actual_exit_code'))is not int or closure['actual_exit_code']!=1 or any(closure.get(k)is not True for k in ['actual_abort_message_exact','all_actual_assertions_completed','no_positive_solver_or_seal_trace','pre_transport_abort_at_frozen_validation_branch']):raise RuntimeError('one exact pretransport refusal')
 lp=closure['actual_log_pin'];wp=closure['actual_watchdog_pin'];sp=closure['original_full46_ledger_pin']
 if [lp['path'],wp['path'],sp['path']]!=[str(DIAG/'AAA/pair_rank_type.log'),str(DIAG/'AAA/pair_rank_type.watchdog.json'),str(DIAG/'AAA3-streaming/stages.json')]:raise RuntimeError('exact own diagnostic closure paths')
 w=b.read(wp);stages=b.read(sp);b.same(lp);text=Path(lp['path']).read_text()
 if len(stages['stages'])!=46 or stages['stages'][:45]!=raw['records']:raise RuntimeError('all historical records untouched and one appended actual record')
 row=stages['stages'][45]
 if row['label']!='AAA/pair_rank_type'or row['status']!='FAILED'or row.get('error')!='own-child stage failed; no retry'or 'log_sha256'in row or row['command']!=[str(DIAG/'runtime/Dragon')]or w['command']!=row['command']or type(w.get('returncode'))is not int or w['returncode']!=1 or w['limit_failure']is not None or type(w.get('pid'))is not int or w['pid']<=0:raise RuntimeError('real original new FAILED record and exact child closure')
 if w['rss_cap_mib']!=512 or w['own_child_only']is not True or w['liveness_group_cleanup']is not True or not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=row['wall_cap_seconds']<=600 or not 0<=w['sampled_peak_rss_mib']<512:raise RuntimeError('real child caps and group cleanup')
 forbidden=['SPOR64_BOOTB64-CENSUS:','ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1','ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE','ACTUAL-AAA3-NATIVE-GLOBAL-COMPLETE','SPOT-R64 B2I BOOTSTRAP COMMITTED','SPOT-X-REAL64-TERMINAL']
 if text.count(expected)!=1 or any(x in text for x in forbidden):raise RuntimeError('messageonce/no transport trace')
 inv=inventory();observed=d['observed_existing_outputs_before_receipt'];owned=d['new_owned_copy_and_archival_pins']
 outputs=unique(observed+owned+[dp]);outtable={r['path']:r for r in outputs}
 if set(outtable)!=set(inv['files']):raise RuntimeError('all diagnostic output files exact report/fullEOF inventory, no omission or extra')
 for row in outputs:
  if not Path(row['path']).is_relative_to(DIAG):raise RuntimeError('diagnostic output outside namespace')
  b.same(row)
 target=outtable.get(str(TARGET))
 if target is None or target not in owned or target['size_bytes']!=BYTES or target['identity'][3]!=1 or not stat.S_ISREG(target['identity'][2])or TARGET.lstat().st_uid!=os.getuid():raise RuntimeError('one actual UID-owned regular single-link target')
 # Original fixed/current-owned files and every other diagnostic output are
 # disjoint protected authorities. Released old proofPF is historical only.
 protected=unique(raw['fixed_current_pins']+raw['owned_runtime_pins']+hf['dependencies']+hf['source_files']+[f['diagnostic_HF_pin'],f['diagnostic_CLI_pin'],fp,tp]+f['Source_pins']+f['dependencies']+[r for r in outputs if r['path']!=str(TARGET)])
 if any(r['path']==str(TARGET)or r['identity'][:2]==target['identity'][:2]for r in protected):raise RuntimeError('target aliases any protected original or evidence file')
 for row in protected:b.same(row)
 for entry in authority['inputs']:
  original=entry['source_pin'];b.same(original)
  dst=DIAG/'runtime'/entry['destination_name']if entry['role']=='original_runtime'else DIAG/'AAA'/entry['destination_name']
  copied=outtable.get(str(dst))
  if copied is None or copied['sha256']!=original['sha256']or copied['size_bytes']!=original['size_bytes']or copied['identity'][3]!=1 or copied['identity'][:2]==original['identity'][:2]:raise RuntimeError('complete exact runtime/deck/9data original and independent readonly copy')
 project_original=next(x['source_pin']for x in authority['inputs']if x['destination_name']=='projected_boot.xsm')
 if target['sha256']!=project_original['sha256']:raise RuntimeError('PROJECT full bytes differ from retained original')
 # Complete current scratch receipts, raw bytes and original sole-child PID.
 scratchpaths=sorted(p for p in DIAG.iterdir()if p.name.startswith('Root_actual_closed_CLE_scratch_stash_')and p.suffix=='.json')
 if len(scratchpaths)!=1:raise RuntimeError('exact one original scratch archival receipt')
 scratch=b.read(outtable[str(scratchpaths[0])])
 if scratch['actual_stage_index']!=45 or scratch['actual_stage_label']!='AAA/pair_rank_type'or scratch['actual_pid']!=w['pid']or scratch['actual_returncode']!=1 or scratch['actual_log_full_pin']!=lp or scratch['actual_watchdog_full_pin']!=wp:raise RuntimeError('original actual scratch child closure')
 for entry in scratch['exact_preserved_scratch_files']:
  bef=entry['before_full_pin'];aft=entry['after_full_pin'];b.same(aft)
  if bef['sha256']!=aft['sha256']or bef['identity'][:6]!=aft['identity'][:6]or os.path.lexists(bef['path']):raise RuntimeError('original scratch raw inode/bytes preserved after rename')
 live=no_live_writer(w['pid']);before=b.budget()
 fresh=sum(r['size_bytes']for r in outputs)
 if fresh>=2*2**30 or fresh-BYTES+8*2**20>128*2**20 or before['artifact_bytes']+20971764748+64*2**20>=96*2**30 or before['disk_free_bytes']-20971764748-2*2**30<8*2**30:raise RuntimeError('all original storage/cold/free/phase caps before release')
 return dict(Source_pin=fp,diagnostic_report_pin=dp,Root_true_receipt_pin=tp,target=target,protected=protected,
  complete_before_inventory=inv,original_budget_before=before,actual_pid=w['pid'],live=live,
  retained_original_PROJECT_pin=project_original,diagnostic_scope_newactual1_historical45=True)

def main():
 parser=argparse.ArgumentParser()
 for prefix in ['source-freeze','diagnostic-report','root-true-receipt']:
  for suffix in ['summary','sha256','seven-id']:parser.add_argument('--'+prefix+'-'+suffix,required=True)
 parser.add_argument('--execute',action='store_true');a=parser.parse_args()
 value=None;receipt=None;stream=None;deleted=False;first_error=None;after_errors=[];result_pin=None
 try:
  admitted=gates(a)
  RECEIPTS.mkdir(exist_ok=True)
  if RECEIPTS.is_symlink()or RECEIPTS.lstat().st_uid!=os.getuid():raise RuntimeError('own ordinary receipt namespace')
  receipt=RECEIPTS/('ACTUAL_SINGLE_PROJECT_RELEASE_RECEIPT.json'if a.execute else'READONLY_SINGLE_PROJECT_RELEASE_REVIEW.json')
  fd=os.open(receipt,os.O_CREAT|os.O_EXCL|os.O_RDWR|os.O_NOFOLLOW,0o600)
  stream=os.fdopen(fd,'w+',encoding='utf-8');owner=b.identity(os.fstat(stream.fileno()))
  value=dict(schema='ACTUAL_EXACT_SINGLE_DIAGNOSTIC_V2_PROJECT_RELEASE_RECEIPT_V1',status='ADMITTED_NO_DELETION_YET',execute_requested=a.execute,
   authority_before_release=admitted,deleted_files=0,logical_bytes_released=0,first_error=None,after_check_errors=[],
   all_other_diagnostic_files_and_original_v11_inputs_retained=True,original_source_and_science_unchanged=True,
   diagnostic_historical45_not_new_business=True,original50_business_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
  def publish():
   before=os.fstat(stream.fileno());ps=receipt.lstat()
   if [before.st_dev,before.st_ino,before.st_mode,before.st_nlink]!=owner[:4]or [ps.st_dev,ps.st_ino,ps.st_mode,ps.st_nlink]!=owner[:4]or before.st_nlink!=1:raise RuntimeError('same owned receipt FD/path role changed')
   stream.seek(0);stream.truncate(0);json.dump(value,stream,indent=2,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())
  # The complete targetSHA/all7, original input and every retained authority,
  # real closure, original budget and inventory survive before any deletion.
  publish();b.guard()
  if a.execute:
   for row in admitted['protected']:b.same(row)
   b.same(admitted['target']);no_live_writer(admitted['actual_pid'])
   if inventory()!=admitted['complete_before_inventory']:raise RuntimeError('diagnostic tree changed before exact unlink')
   fd=os.open(TARGET.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
   try:
    if b.identity(os.fstat(fd))!=admitted['complete_before_inventory']['directories'][str(TARGET.parent)]:raise RuntimeError('exact original parentdirfd identity')
    s=os.stat(TARGET.name,dir_fd=fd,follow_symlinks=False)
    if b.identity(s)!=admitted['target']['identity']or s.st_uid!=os.getuid()or s.st_nlink!=1:raise RuntimeError('target UID/all7 changed immediately before unlink')
    if TARGET!=DIAG/'AAA/projected_boot.xsm':raise RuntimeError('only literal single-path whitelist')
    os.unlink(TARGET.name,dir_fd=fd);deleted=True
   finally:os.close(fd)
   value['deleted_files']=1;value['logical_bytes_released']=BYTES;value['status']='EXACT_ONE_UNLINK_DONE_POSTCHECK_PENDING';publish()
   if os.path.lexists(TARGET):raise RuntimeError('deleted owned copy reappeared; no retry')
   for row in admitted['protected']:b.same(row)
   new=inventory();old=admitted['complete_before_inventory']
   if new['files']!={p:i for p,i in old['files'].items()if p!=str(TARGET)}or set(new['directories'])!=set(old['directories']):raise RuntimeError('any other diagnostic file/entry changed')
   for path,prior in old['directories'].items():
    after=new['directories'][path]
    if path==str(TARGET.parent):
     if after[:3]!=prior[:3]or after[3]!=prior[3]-1 or after[4]!=prior[4]-32 or after[5]<prior[5]or after[6]<prior[6]:raise RuntimeError('exact APFS parent nlink-1/32B and stable inode/mode')
     value['observed_APFS_parent_directory_change']=dict(path=path,before=prior,after=after,nlink_delta=-1,size_delta_bytes=-32)
    elif after!=prior:raise RuntimeError('unaffected diagnostic directory all7 changed')
   no_live_writer(admitted['actual_pid']);after=b.budget()
   if admitted['original_budget_before']['artifact_bytes']-after['artifact_bytes']!=BYTES or admitted['original_budget_before']['regular_files']-after['regular_files']!=1:raise RuntimeError('ART true logical delta is not exact single749355952B')
   if after['original_initial_reserve_admitted']is not True:raise RuntimeError('next original fullfresh/cold/meta reserve remains insufficient')
   value.update(status='EXACT_SINGLE_DIAGNOSTIC_PROJECT_RELEASE_ALL_RETAINED_FULL_EOF_CLOSED',original_budget_after=after,
    confirmed_target_absent=True,full_DIAG_inventory_after=new,only_diagnostic_PROJECT_raw_copy_replay_unavailable=True)
  else:value['status']='READONLY_EXACT_SINGLE_DIAGNOSTIC_PROJECT_RELEASE_ADMITTED_NO_UNLINK'
  publish();b.guard()
 except BaseException as exc:
  first_error=type(exc).__name__+': '+str(exc)
  if value is not None:
   value.update(status='FAILED_OR_PARTIAL_RELEASE_EVIDENCE_RETAINED_NO_RETRY',first_error=first_error,after_check_errors=after_errors,deleted_files=int(deleted),logical_bytes_released=BYTES if deleted else 0)
   try:publish()
   except BaseException as later:after_errors.append(type(later).__name__+': '+str(later))
 finally:
  if stream is not None:stream.close()
  if receipt is not None and receipt.exists():
   try:result_pin=b.pin(receipt)
   except BaseException as later:after_errors.append(type(later).__name__+': '+str(later))
  print(json.dumps(dict(status=None if value is None else value['status'],first_error=first_error,
   after_check_errors=after_errors,receipt_pin=result_pin,deleted_files=int(deleted),
   logical_bytes_released=BYTES if deleted else 0,original_v11_qualified=False,AAA_qualified=False,ABA_admitted=False),allow_nan=False),flush=True)
  if first_error is not None or after_errors:raise SystemExit(1)

if __name__=='__main__':main()
