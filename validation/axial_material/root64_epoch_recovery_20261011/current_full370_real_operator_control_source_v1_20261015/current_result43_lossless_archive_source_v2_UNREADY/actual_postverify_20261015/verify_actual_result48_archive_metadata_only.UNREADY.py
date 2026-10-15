"""Draft for a separate executor after real archive closure; never decompresses or unlinks."""
import argparse,hashlib,json,os,resource,shlex,stat,sys,time
from pathlib import Path

BASE=Path(__file__).absolute().parent
PACKAGE=BASE.parent
SOURCE_AUTHOR='/root/formal_goal_remaining_audit'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,
 history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,
 free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
SYSTEM={'/bin/ps':'a06fe087161557f1f8c030672eaedcd90bc6a8e92b8f2d44e07cffedc3349205',
 '/usr/sbin/lsof':'deff85c7b4750a948a69fcd48eae3b394a37575e5048e5eb4a35b7a0482c3dc8'}
FALSE=dict(result_values_decoded=False,numerical_executed=False,compiler_executed=False,
 worker_or_guard_helpers_imported=False,PS_executed=False,lsof_executed=False,
 compression_repeated=False,decompression_repeated=False,files_deleted=False,
 old_plain_payload_body_opened=False,old_plain_payload_SHA_recomputed=False,
 physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)

def require(v,m):
 if type(v)is not bool or not v:raise RuntimeError(m)
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p,metadata_role=False):
 require(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['size_bytes'])is int
  and len(p['identity'])==7 and all(type(v)is int for v in p['identity']),'complete integer fullPF')
 q=Path(p['path']);s=q.lstat();ordinary=s.st_uid==os.getuid()and s.st_nlink==1
 tool=metadata_role and str(q)in SYSTEM and s.st_uid==0 and s.st_nlink==1 and p['sha256']==SYSTEM[str(q)]
 compiler=metadata_role and str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15'
 compiler=compiler and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and s.st_nlink==p['identity'][3]==2
 require(q.is_absolute()and not any(a.is_symlink()for a in(q,*q.parents))and stat.S_ISREG(s.st_mode)
  and ids(s)==p['identity']and s.st_size==p['size_bytes']and(ordinary or tool or compiler),'exact current7 and explicit role owner/link exception')
 return q
def blind(p,budget):
 q=current(p);h=hashlib.sha256();n=0;fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  require(ids(os.fstat(fd))==p['identity'],'opened exact7')
  while b:=os.read(fd,2**20):h.update(b);n+=len(b);budget()
  require(ids(os.fstat(fd))==p['identity'],'wholeEOF opened7')
 finally:os.close(fd)
 current(p);require(n==p['size_bytes']and h.hexdigest()==p['sha256'],'wholeEOF SHA/length exact')
def read(p,budget):
 require(p['size_bytes']<8*2**20,'bounded report metadata8MiB');blind(p,budget)
 v=json.loads(Path(p['path']).read_bytes());blind(p,budget);return v
def newpin(q,budget):
 s=q.lstat();h=hashlib.sha256()
 with q.open('rb')as f:
  while b:=f.read(2**20):h.update(b);budget()
 require(ids(q.lstat())==ids(s),'own metadata stable')
 return dict(path=str(q),sha256=h.hexdigest(),size_bytes=s.st_size,identity=ids(s))
def genuine(d,key,expected,role):
 r=d[key];require(d['observed_closed']is True and type(d['original_integer_exit_code'])is int
  and d['original_integer_exit_code']==0 and type(r['exit_code'])is int and r['exit_code']==0
  and 'session_id'not in r and json.loads(r['output'].splitlines()[-1])[role]==expected,'genuine closed typed0 exact stdout PF')
def contains(v,p):return v==p or type(v)is dict and any(contains(x,p)for x in v.values())or type(v)is list and any(contains(x,p)for x in v)
def resource_facts(d):
 require(d['SELF_peak_bytes']<512*2**20 and d['original_elapsed_seconds']<1800,'original host SELF/wall')
 h=d['original_history'];f=d['complete_joint']
 require(f['artifact_bytes']+d['explicit_external_metadata_bytes']+d['own_open_unlinked_bytes']<2*2**30
  and h['artifact_bytes']+20971764748+64*2**20<96*2**30
  and f['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'actual saved joint/history/cold/free original caps')

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--Root-tools-pin',required=True)
 ap.add_argument('--Host-pin',required=True);ap.add_argument('--executor-task-name',required=True)
 a=ap.parse_args();started=time.monotonic()
 require(a.executor_task_name!=SOURCE_AUTHOR and a.executor_task_name.startswith('/root/'),'separate actual executor required; Source author must not self-run this post')
 def budget():
  peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
  require(peak<512*2**20 and time.monotonic()-started<600,'post SELF512/stage600')
 pRoot=json.loads(a.Root_tools_pin);pHost=json.loads(a.Host_pin);root=read(pRoot,budget);host=read(pHost,budget)
 require(root['observed_closed']is True and type(root['original_integer_exit_code'])is int,'actual closure exists, no mid-run success')
 if root['original_integer_exit_code']!=0:
  raise RuntimeError('actual archive nonzero; preserve raw/partial files and author a bounded failurefacts assessment from actual keys')
 genuine(root,'actual_terminal_return',pHost,'report_pin')
 require(root['actual_execution_permission_mode']=='require_escalated','unchanged PS guard original permission role')
 require(host['schema']=='ACTUAL_RESULT43_LOSSLESS_ARCHIVE_GUARDED_HOST_REPORT_V1'
  and host['status']=='ACTUAL_ALL48_ARCHIVED_ROUNDTRIP_CLOSED0_PLAIN_RETAINED'
  and host['failure']is None and host['archive_complete']is True and host['retries']==0
  and host['original_caps']==CAPS and host['final_report_resource_check_passed']is True
  and host['original_guard_class_and_MRO_unchanged']is True and host['plain_retirement_allowed']is False,
  'actual original guarded complete archive only; no plain retirement')
 sf=read(host['source_freeze_pin'],budget);hf=read(host['host_freeze_pin'],budget)
 plan=read(host['binding_pin'],budget);out=Path(plan['planned_actual_output_root'])
 require(pHost['path']==str(out/'Root_actual_result43_lossless_archive_summary.json')
  and host['complete_joint_roots']==plan['complete_joint_roots']
  and len(plan['complete_joint_roots'])==65 and plan['complete_joint_roots'][-1]==str(out), 'actual65 whole prefix and owning output')
 cliPin=newpin(PACKAGE/'FINAL_ROOT_REVIEWABLE_CLI.json',budget);cli=read(cliPin,budget)
 require(shlex.split(root['exact_executed_command'])==cli['argv']and len(cli['argv'])==24
  and cli['exec_command_sandbox_permissions']=='require_escalated'
  and cli['source_freeze_pin']==host['source_freeze_pin']and cli['host_freeze_pin']==host['host_freeze_pin'],'exact published24 argv and SF/HF')
 peer=read(hf['independent_Source_review_pin'],budget);pt=read(hf['independent_Source_review_tools_pin'],budget)
 genuine(pt,'actual_review_return',hf['independent_Source_review_pin'],'review_pin')
 require(peer['source_only']is True and peer['failure']is None and peer['status'].startswith('PASS')
  and peer['binding_pin']==host['binding_pin']and all(contains(peer,p)for p in sf['complete_source_file_pins']),'actual Sourcepeer0 whole Source scope')
 for p in hf['selected_Source_pins']:blind(p,budget);blind(p,budget)
 require(host['all48_original_plain_current7_retained']is True and len(host['records'])==1
  and host['records'][0]['status']=='PASS','one original child0, all plaintext still present')
 w=host['actual_watchdog'];require(type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None
  and w['rss_cap_mib']==512 and w['own_child_only']is True and w['liveness_group_cleanup']is True
  and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 and 0<=w['sampled_peak_rss_mib']<512,'actual child512/600/liveness0')
 child=read(host['actual_child_receipt']['report_pin'],budget)
 require(child['status']=='ALL48_BYTE_SHA_LENGTH_ROUNDTRIP_CLOSED0_PLAIN_RETAINED'
  and child['failure']is None and child['completed_count']==48 and child['binding_pin']==host['binding_pin'],'actual complete48 child report')
 index=read(child['index_pin'],budget);rows=index['entries'];originals=plan['all48_plain_pins']
 require(index['schema']=='RESULT43_LOSSLESS_ORIGINAL_PATH_ARCHIVE_LOOKUP_V1'
  and index['status']=='ALL48_STREAMED_ROUNDTRIP_SHA_LENGTH_EXACT_PLAIN_PRESERVED'
  and index['binding_pin']==host['binding_pin']and len(rows)==len(originals)==48
  and index['ordered_original_plain_total_bytes']==sum(p['size_bytes']for p in originals)==805236925
  and index['historical_completed_A_guard_role_count']==30 and index['compression_ratio_assumed']is False,'exact full48 ordered archive lookup, no summary substitute')
 archivePins=[];entryPins=[];old30=[];new5=[]
 for ordinal,(row,p)in enumerate(zip(rows,originals)):
  require(row['ordinal']==ordinal and row['original_plain_full_pin']==p
   and row['compression_input_SHA']==row['streamed_decompressed_SHA']==p['sha256']
   and row['compression_input_length']==row['streamed_decompressed_length']==p['size_bytes']
   and row['exact_original_plain_bytes_recoverable']is True and row['original_plain_preserved']is True
   and row['result_values_decoded']is False and row['mtime']==0 and row['filename_field']==''and row['compresslevel']==6,
   'actual original byte-stream and decompressed SHA/length proof; metadata assessment only')
  current(p);pgz=row['compressed_archive_full_pin'];require(Path(pgz['path']).parent==out/'archives','compressed file belongs to sole output')
  blind(pgz,budget);blind(pgz,budget);archivePins.append(pgz)
  entry=read(row['entry_pin'],budget);require({k:v for k,v in row.items()if k!='entry_pin'}==entry,'durable original per-file entry exactly equals lookup')
  entryPins.append(row['entry_pin']);current(p)
  require(row['historical_completed_A_guard_role']==(p['path']in plan['historical_completed_guard_role_paths'])
   and row['completed_A2_new_JSONL_role']==(p in plan['completed_A2_new5_JSONL_pins']),'exact old30 and new5 lifecycle roles')
  if row['historical_completed_A_guard_role']:old30.append(p)
  if row['completed_A2_new_JSONL_role']:new5.append(p)
 require(len(old30)==30 and len(new5)==5 and sum(p['size_bytes']for p in archivePins)==index['total_gzip_bytes']==child['total_gzip_bytes']<184*2**20,'all gzip payload184MiB bound')
 for _ in range(2):
  for p in originals+plan['retained_native_current7_pins']:current(p)
  for p in plan['explicit_cumulative_metadata_file_pins']:current(p,True)
  for p in plan['actual_retired_early14_pins']:require(not os.path.lexists(p['path']),'only real early14 roles absent')
 resource_facts(host['resources_before']);resource_facts(host['resources_after']);resource_facts(host['resources_after_including_summary_bytes'])
 outputs=[];ownTotal=0
 for q in sorted(out.rglob('*')):
  s=q.lstat();require(not stat.S_ISLNK(s.st_mode),'own output no aliases')
  if stat.S_ISREG(s.st_mode):
   ownTotal+=s.st_size
   if q.suffix!='.gz':
    p=newpin(q,budget);blind(p,budget);blind(p,budget);outputs.append(p)
 require(ownTotal<192*2**20 and len(archivePins)==48,'own output192MiB includes archives/all metadata/runtime')
 for key in('physics_qualified','AAA_qualified','ABA_admitted','goal_complete','result_values_decoded','numerical_executed','files_deleted'):
  require(host[key]is False and child[key]is False and index[key]is False,'byte archival only; physical/goal flags false')
 selfPin=newpin(Path(__file__).absolute(),budget)
 review=dict(schema='RECORDED_RESULT48_LOSSLESS_ARCHIVE_METADATA_POSTVERIFY_V1',
  status='PASS_ACTUAL_ALL48_STREAMED_SHA_LENGTH_ARCHIVE_METADATA_ONLY_PLAINTEXT_RETAINED',failure=None,metadata_only=True,
  Source_author_task=SOURCE_AUTHOR,Source_author_also_authored_archive_workflow=True,actual_executor_task=a.executor_task_name,
  independent_execution_from_Source_author_as_required_by_Root=True,independent_numerical_or_decompression_recomparison=False,
  actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=0,actual_child_integer_exit_code=0,
  Source_freeze_pin=host['source_freeze_pin'],Host_freeze_pin=host['host_freeze_pin'],actual_CLI_pin=cliPin,
  Source_peer_pin=hf['independent_Source_review_pin'],Source_peer_tools_pin=hf['independent_Source_review_tools_pin'],
  execution_binding_pin=host['binding_pin'],actual_child_report_pin=host['actual_child_receipt']['report_pin'],actual_archive_index_pin=child['index_pin'],
  ordered48_original_plain_full_pins=originals,ordered48_compressed_archive_full_pins=archivePins,ordered48_entry_pins=entryPins,
  original_plain_bytes=805236925,gzip_bytes=sum(p['size_bytes']for p in archivePins),own_output_bytes=ownTotal,
  original48_current7_verified_twice_only=True,compressed48_fullEOF_SHA_current7_verified_twice=True,
  Root_actual_streamed_decompression_proofs_matched_original_fullPF=True,old30_historical_guard_pins=old30,new5_completed_A2_result_pins=new5,
  all48_plain_current7_retained=True,all66_native_current7_retained=True,complete_joint_roots=plan['complete_joint_roots'],
  original_caps=CAPS,actual_original_watchdog=w,actual_original_runner_record=host['records'][0],
  new_non_gzip_output_fullEOF_pins=outputs,reviewer_Source_pin=selfPin,wall_seconds=time.monotonic()-started,**FALSE)
 target=BASE/'REVIEW.json';raw=(json.dumps(review,indent=2,allow_nan=False)+'\n').encode();require(len(raw)<8*2**20,'compact own review8MiB')
 with target.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 budget();print(json.dumps(dict(status=review['status'],review_pin=newpin(target,budget))),flush=True)

if __name__=='__main__':main()
