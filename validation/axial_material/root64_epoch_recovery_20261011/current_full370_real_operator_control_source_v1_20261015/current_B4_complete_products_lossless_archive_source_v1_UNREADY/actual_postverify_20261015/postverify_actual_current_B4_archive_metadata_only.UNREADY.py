"""UNREADY independent metadata post for actual B4 complete product byte archives.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. New compressed outputs are blindly hashed; no original payload read, repeat decompression or value decoding.
The exact pre-GEN author freeze is bound below; actual execution remains NULL.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_B4_complete_products_lossless_archive_source_v1_UNREADY/AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json', 'sha256': '8f9b167e36d5c19e8dd4766a605564092c008215bc3e6662fdeb88693e027db4', 'size_bytes': 8593, 'identity': [16777229, 50872610, 33188, 1, 8593, 1792059728913961239, 1792059728913961239]}
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(result_values_decoded=False,numerical_executed=False,compiler_executed=False,native_executed=False,worker_or_guard_helpers_imported=False,PS_executed=False,lsof_executed=False,compression_repeated=False,decompression_repeated=False,files_deleted=False,old_plain_payload_body_opened=False,old_plain_payload_SHA_recomputed=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,plain_retirement_authorized=False)
START=time.monotonic()
def need(v,m):
 if type(v)is not bool or not v:raise RuntimeError(m)
def budget():
 need(time.monotonic()-START<600 and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)<512*2**20,'metadata post stage600/SELF512')
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 budget();q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_uid==os.getuid()and s.st_nlink==1 and ids(s)==p['identity']and s.st_size==p['size_bytes']and len(p['identity'])==7 and all(type(x)is int for x in p['identity']),'exact ordinary owned current7')
 return q
def full(p):
 q=current(p);h=hashlib.sha256();n=0
 with q.open('rb')as f:
  need(ids(os.fstat(f.fileno()))==p['identity'],'opened7')
  while b:=f.read(2**20):h.update(b);n+=len(b);budget()
  need(ids(os.fstat(f.fileno()))==p['identity'],'EOF7')
 need(n==p['size_bytes']and h.hexdigest()==p['sha256'],'blind whole-file SHA/length');current(p);return q
def pin(q):
 q=Path(q);s=q.lstat();h=hashlib.sha256()
 with q.open('rb')as f:
  need(ids(os.fstat(f.fileno()))==ids(s),'opened new file7')
  while b:=f.read(2**20):h.update(b);budget()
  need(ids(os.fstat(f.fileno()))==ids(s),'new file EOF7')
 p=dict(path=str(q),sha256=h.hexdigest(),size_bytes=s.st_size,identity=ids(s));current(p);return p
def meta(p):
 need(p['size_bytes']<8*2**20,'only bounded control metadata8MiB is decoded')
 q=full(p);v=json.loads(q.read_bytes());full(p);return v
def genuine(v,key,p,field):
 t=v[key];need(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==0 and type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None and json.loads(t['output'].strip().splitlines()[-1])[field]==p,'genuine closed typed0 and exact output artifact PF')
def current_role(p,build):
 budget();q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and ids(s)==p['identity']and s.st_size==p['size_bytes']and len(p['identity'])==7 and all(type(x)is int for x in p['identity']),'same exact inherited current7 without old payload read')
 if p in build['readonly_system_SDK_header_pins']:
  root=Path(build['readonly_system_SDK_root']);rs=root.lstat()
  need(str(root)=='/Library/Developer/CommandLineTools/SDKs/MacOSX27.0.sdk'and stat.S_ISDIR(rs.st_mode)and rs.st_uid==0 and ids(rs)==build['readonly_system_SDK_root_identity']and not any(x.is_symlink()for x in(root,*root.parents))and str(q)in{str(root/'usr/include'/n)for n in('stdio.h','stdlib.h','stdint.h')}and s.st_uid==0 and s.st_nlink==1,'only frozen selected readonly SDK headers current7')
 elif p in build['readonly_system_tool_metadata_pins']:
  need(str(q)in('/bin/ps','/usr/sbin/lsof')and s.st_uid==0 and s.st_nlink==1 and bool(s.st_mode&0o111),'only explicitly frozen readonly PS/lsof roles')
 elif p==build['C_compiler_pin']:
  need(str(q)=='/Library/Developer/CommandLineTools/usr/bin/clang'and s.st_uid==0 and s.st_nlink==1 and bool(s.st_mode&0o111),'only explicit frozen current readonly clang role')
 elif str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15':
  need(p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and s.st_uid==os.getuid()and s.st_nlink==p['identity'][3]==2,'only original frozen gfortran link exception')
 else:need(s.st_uid==os.getuid()and s.st_nlink==1,'same owned ordinary inherited role')
def all_output_pins(out):
 rows=[]
 if not os.path.lexists(out):return rows
 need(out.is_dir()and not any(x.is_symlink()for x in(out,*out.parents)),'literal fresh current B55 control output')
 for q in sorted(out.rglob('*')):
  s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'no new output alias')
  if stat.S_ISREG(s.st_mode):p=pin(q);full(p);rows.append(p)
  else:need(stat.S_ISDIR(s.st_mode),'ordinary new output files/directories only')
 return rows
def counted_bytes(roots):
 total=0
 for value in roots:
  root=Path(value);need(root.is_absolute()and not any(x.is_symlink()for x in(root,*root.parents)),'literal counted root')
  if not os.path.lexists(root):continue
  need(root.is_dir(),'counted root directory')
  for q in root.rglob('*'):
   budget();s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'no alias in full counted scope')
   if stat.S_ISREG(s.st_mode):total+=s.st_size
 return total
def unlinked_bytes():
 rows={}
 for name in os.listdir('/dev/fd'):
  try:s=os.fstat(int(name))
  except(ValueError,OSError):continue
  if stat.S_ISREG(s.st_mode)and s.st_nlink==0:rows[s.st_dev,s.st_ino]=s.st_size
 return sum(rows.values())
def archive_resources(v,roots,seconds):
 need(v['SELF_peak_bytes']<512*2**20 and 0<=v['original_elapsed_seconds']<seconds and v['complete_joint']['resource_roots']==roots,'actual original SELF/wall and dynamic complete current roots')
 h=v['original_history'];j=v['complete_joint']
 need(j['artifact_bytes']+v['explicit_external_metadata_bytes']+v['own_open_unlinked_bytes']<2*2**30 and h['artifact_bytes']+20971764748+64*2**20<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'actual original history/cumulative/cold/metadata/free caps')
def save(report,source_limit,joint_existing=None):
 report.update(metadata_only=True,Source_author_task=AUTHOR,actual_executor_task=EXECUTOR,actual_post_not_executed_by_Source_author=True,reviewer_Source_pin=pin(Path(__file__).absolute()),helper_or_candidate_module_imported=False,Source_GEN_or_publication_executed=False,native_or_compiler_or_worker_executed=False,scientific_values_or_SQLite_or_native_XSM_or_context_body_decoded=False,original_collect_or_snapshot_pair_readback_repeated=False,historical_issue_records_modified=False,wall_seconds=time.monotonic()-START,**FALSE)
 raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20,'post control report6MiB')
 need(counted_bytes([str(PACKAGE)])+len(raw)<source_limit,'entire Source/metadata bound including new post')
 if joint_existing is not None:need(joint_existing+len(raw)<2*2**30,'entire current cumulative2GiB including post')
 q=BASE/'REVIEW.json'
 with q.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 budget();print(json.dumps(dict(status=report['status'],review_pin=pin(q))),flush=True)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in('Root-tools-pin','Host-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();need(a.executor_task_name==EXECUTOR and a.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'exact separate executor and immutable single post')
 pRoot=json.loads(a.Root_tools_pin);pHost=json.loads(a.Host_pin);root=meta(pRoot);host=None if pHost is None else meta(pHost);actual=root['actual_terminal_return']
 need(root['observed_closed']is True and type(root['original_integer_exit_code'])is int and type(actual['exit_code'])is int and actual['exit_code']==root['original_integer_exit_code']and actual.get('session_id')is None and root['actual_execution_permission_mode']=='require_escalated'and root['actual_retried']is False,'genuine original typed closed Root terminal/PS permission/no retry')
 pb=pin(PACKAGE/'PLAN.json')if host is None else host['binding_pin'];b=meta(pb);out=Path(b['planned_actual_output_root']);roots=b['complete_joint_roots'];limit=b['bounded_total_output_bytes'];source_limit=b['bounded_Source_metadata_bytes']
 need(b['schema']=='CURRENT_B4_COMPLETE_PRODUCT_LOSSLESS_ARCHIVE_BINDING_V1'and b['original_caps']==CAPS and b['prerequisite_binding_complete']is True and b['draft_unready']is False and b['Source_admission_ready']is False and limit==64*2**20 and b['bounded_archive_payload_bytes']==56*2**20 and b['metadata_runtime_headroom_bytes']==8*2**20 and source_limit==16*2**20 and roots[-1]==str(out),'actual current B4 binding/64 total56 payload8 metadata/Source16 and original caps')
 if pHost is not None:need(pHost['path']==str(out/'Root_actual_B4_products_lossless_archive_summary.json')and host['schema']=='ACTUAL_CURRENT_B4_LOSSLESS_ARCHIVE_GUARDED_HOST_REPORT_V1','actual B4 Host report role')
 newpins=all_output_pins(out);table={p['path']:p for p in newpins};ownbytes=sum(p['size_bytes']for p in newpins);code=root['original_integer_exit_code']
 if code!=0:
  observed=[]
  if host is not None and host['actual_watchdog']is not None:
   need(len(host['records'])>0,'actual failed watchdog has a recorded owning stage');wp=str(out/(host['records'][-1]['label']+'.watchdog.json'));w=meta(table[wp]);need(w==host['actual_watchdog']and type(w['returncode'])is int,'genuine saved failed-stage child return only');observed.append(w['returncode'])
  result=dict(schema='CURRENT_B4_ARCHIVE_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=code,actual_Host_status=None if host is None else host['status'],actual_Host_failure=None if host is None else host['failure'],actual_stage_records=None if host is None else host['records'],actual_recorded_child_integer_exit_codes=observed,absent_child_code_invented=False,child_code_inferred_from_Root_return=False,new_partial_output_blind_fullEOF_twice_pins=newpins,archive_success_or_roundtrip_inferred=False,execution_binding_pin=pb)
  save(result,source_limit);return
 need(host is not None,'Root0 requires genuine Host report PF');genuine(root,'actual_terminal_return',pHost,'report_pin')
 need(host['status']=='ACTUAL_CURRENT_B4_ALL_PRODUCTS_ARCHIVED_ROUNDTRIP_CLOSED0_ORIGINALS_RETAINED'and host['failure']is None and host['secondary_failures']==[]and host['archive_complete']is True and host['retries']==0 and host['original_caps']==CAPS and host['final_report_resource_check_passed']is True and host['original_guard_class_and_MRO_unchanged']is True and host['plain_retirement_allowed']is False and host['independent_archive_post0_required']is True and host['all4_original_products_current7_retained']is True,'actual original private OwnRSS closed0 complete B4 byte archive only; originals retained')
 sf=meta(host['source_freeze_pin']);hf=meta(host['host_freeze_pin']);core=meta(EXPECTED_CORE_AUTHOR_FREEZE);ready_pin=pin(PACKAGE/'SOURCE_REVIEW_READY.json');ready=meta(ready_pin)
 need(core['Source_only_frozen_before_Root_generation']is True and core['whole_Source_file_pins']==sf['complete_source_file_pins']and core['whole_original_archive_one_byte_stream_compression_and_decompression_proof_unchanged']is True,'exact whole five Source roles and original whole archive_one byte algorithm')
 need(ready['schema']=='CURRENT_B4_COMPLETE_PRODUCT_ARCHIVE_SOURCE_REVIEW_READY_V1'and ready['source_only']is True and ready['product_payload_opened']is False and ready['gzip_executed']is False and sf['schema']=='CURRENT_B4_LOSSLESS_ARCHIVE_SOURCE_FREEZE_V1'and sf['source_only']is True and sf['candidate_executed']is False and hf['schema']=='CURRENT_B4_LOSSLESS_ARCHIVE_HOST_FREEZE_V1'and hf['source_only']is True and hf['selected_source_freeze_pin']==host['source_freeze_pin']and ready['execution_binding_pin']==sf['execution_binding_pin']==pb and ready['complete_source_file_pins']==sf['complete_source_file_pins']and len(sf['complete_source_file_pins'])==5 and hf['host_source_pin']==ready['host_source_pin']and hf['common_source_pin']==ready['common_source_pin']and hf['original_caps']==CAPS,'same actual B4 READY.execution_binding_pin and exact Source/host/common publication')
 peer=meta(hf['independent_Source_review_pin']);pt=meta(hf['independent_Source_review_tools_pin']);gt=meta(hf['Root_Source_generation_true_tools_pin']);genuine(pt,'actual_review_return',hf['independent_Source_review_pin'],'review_pin');genuine(gt,'actual_Source_preparation_return',ready_pin,'ready_pin')
 need(peer['source_only']is True and peer['status']=='PASS_SOURCE_ONLY_CURRENT_B4_COMPLETE_PRODUCT_LOSSLESS_ARCHIVE'and peer['failure']is None and peer['binding_pin']==pb and peer['complete_source_file_pins']==sf['complete_source_file_pins']and sf['independent_Source_review_pin']==hf['independent_Source_review_pin']and sf['independent_Source_review_tools_pin']==hf['independent_Source_review_tools_pin']and sf['Root_Source_generation_true_tools_pin']==hf['Root_Source_generation_true_tools_pin'],'genuine same-round exact independent B4 Source review0 and Root SourceGEN0')
 for p in sf['complete_source_file_pins']:full(p);full(p)
 cli_pin=pin(PACKAGE/'FINAL_ROOT_REVIEWABLE_CLI.json');cli=meta(cli_pin)
 need(shlex.split(root['exact_executed_command'])==cli['argv']==shlex.split(cli['command'])and len(cli['argv'])==24 and cli['source_freeze_pin']==host['source_freeze_pin']and cli['host_freeze_pin']==host['host_freeze_pin']and cli['Root_actual_exec_command_sandbox_permissions_required']==hf['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated','actual exact complete published24 Root argv and freeze PFs')
 latest=meta(b['latest_complete_plan_pin']);need(host['complete_joint_roots']==roots==latest['complete_joint_roots']+[str(out)]and roots[:-1]==b['inherited_latest_complete_joint_roots']and len(roots)==len(set(roots))and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)and any(PACKAGE.is_relative_to(Path(x))for x in roots[:-1]),'whole dynamic then-latest prefix plus one B4 output root; Source stays counted, no fixed ordinal')
 build=meta(b['original_guard_build_plan_pin']);capture=meta(b['actual_B_capture_Host_report_pin']);manifest=meta(b['actual_B_manifest_pin']);input_binding=meta(b['actual_B_input_binding_pin']);extract=meta(b['actual_B_extraction_child_report_pin']);state=capture['actual_B_state']
 originals=b['all4_product_pins'];retained=b['retained_native_current7_pins'];inputs=b['original_B_native_and_readonly_input_current7_pins']
 need(originals==state['actual_material_product_pins']and len(originals)==len({p['path']for p in originals})==4 and [Path(p['path']).name for p in originals]==['m.xsm','u.asc','a.asc','t.asc']and all(Path(p['path']).parent==Path(input_binding['actual_output_root'])for p in originals)and manifest['state_order']==['B']and manifest['states']['B']['actual_owning_report_pin']==b['actual_B_capture_Host_report_pin']and manifest['current_B_case_input_binding_pin']==b['actual_B_input_binding_pin'],'exact four complete current B capture products in producer order, no historical A/48/JSONL labels')
 need(retained==state['complete_context_pins']+[x['input_pin']for x in state['complete_state_snapshot_inputs']]+[p for x in extract['states']['B']for p in(x['paired_SQLite_pin'],x['paired_original_pool_pin'])]and len(retained)==79 and len(inputs)==11 and not{p['path']for p in originals}&{p['path']for p in retained},'all55contexts/eight native XSM/sixteen SQL-pool files retained separately and all11 original B inputs current7-only')
 need(len(host['records'])==1 and host['records'][0]['status']=='PASS','one actual original guarded archive child0, no retry');record=host['records'][0];wp=table[str(out/(record['label']+'.watchdog.json'))];lp=table[str(out/(record['label']+'.log'))];w=meta(wp)
 need(w==host['actual_watchdog']and type(w['returncode'])is int and w['returncode']==0 and w['command']==record['command']and w['limit_failure']is None and w['rss_cap_mib']==512 and w['own_child_only']is True and w['liveness_group_cleanup']is True and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 and lp['sha256']==record['log_sha256'],'actual private OwnRSS child0/record.label log/watch/original PS/RSS/wall/liveness closure')
 claim=meta(pin(PACKAGE/'ROOT_ARCHIVE_EXECUTION_CLAIM.json'));command=record['command']
 need(len(command)==9 and command[:4]==[b['original_complete_ENV_Python_B_prefix'][-2],'-B',str(PACKAGE/'archive_B4_products_serial.UNREADY.py'),'--binding-pin']and json.loads(command[4])==pb and command[5]=='--common-source-pin'and json.loads(command[6])==hf['common_source_pin']and command[7:] ==['--expected-parent-pid',str(claim['PID'])],'exact original child argv/whole binding/common Source and owning Root PID')
 logpath=full(lp);need(lp['size_bytes']<8*2**20,'bounded complete JSON child receipt log');lines=logpath.read_text().splitlines();need(len(lines)==1,'one genuine complete archive child receipt');receipt=json.loads(lines[0]);need(receipt==host['actual_child_receipt'],'actual original child receipt matches Host')
 childpin=receipt['report_pin'];child=meta(childpin)
 need(childpin['path']==str(out/'ACTUAL_CURRENT_B4_LOSSLESS_ARCHIVE_REPORT.json')and child['schema']=='ACTUAL_CURRENT_B4_SERIAL_LOSSLESS_ARCHIVE_REPORT_V1'and child['status']=='ALL4_COMPLETE_B_PRODUCT_BYTE_SHA_LENGTH_ROUNDTRIP_CLOSED0_ORIGINALS_RETAINED'and child['failure']is None and child['completed_count']==4 and type(child['completed_count'])is int and child['binding_pin']==pb and child['all4_original_products_current7_retained']is True and child['all79_context_snapshot_and_saved_pair_files_current7_retained']is True,'actual serial complete four-product child report and retained source scope')
 indexpin=child['index_pin'];index=meta(indexpin);rows=index['entries'];originalbytes=sum(p['size_bytes']for p in originals)
 need(indexpin['path']==str(out/'CURRENT_B4_LOSSLESS_ARCHIVE_INDEX.json')and index['schema']=='CURRENT_B4_COMPLETE_PRODUCT_LOSSLESS_ORIGINAL_PATH_ARCHIVE_LOOKUP_V1'and index['status']=='ALL4_COMPLETE_B_PRODUCTS_STREAMED_ROUNDTRIP_SHA_LENGTH_EXACT_ORIGINALS_RETAINED'and index['binding_pin']==pb and len(rows)==index['ordered_original_product_count']==4 and type(index['ordered_original_product_count'])is int and index['ordered_original_product_total_bytes']==child['original_product_total_bytes']==b['original4_product_total_bytes']==originalbytes and index['compression_ratio_assumed']is False and index['all4_original_products_retained']is True and index['requires_independent_post0_before_separate_original_product_retirement']is True,'exact four-product original-path archive lookup and actual byte totals; not old48 facts')
 archives=[];entrypins=[];proofs=[]
 for ordinal,(row,p)in enumerate(zip(rows,originals)):
  need(type(row['ordinal'])is int and row['ordinal']==ordinal and row['original_plain_full_pin']==p and row['actual_B_capture_product_name']==Path(p['path']).name and row['original_product_is_complete']is True and row['compression_input_SHA']==row['streamed_decompressed_SHA']==p['sha256']and row['compression_input_length']==row['streamed_decompressed_length']==p['size_bytes']and type(row['compression_input_length'])is int and type(row['streamed_decompressed_length'])is int and row['exact_original_plain_bytes_recoverable']is True and row['original_plain_preserved']is True and row['result_values_decoded']is False and row['scientific_values_decoded']is False and row['filename_field']==''and type(row['mtime'])is int and row['mtime']==0 and type(row['compresslevel'])is int and row['compresslevel']==6,'actual Root-streamed input/decompressed SHA/length equal exact original fullPF; metadata proof only')
  pgz=row['compressed_archive_full_pin'];need(pgz['path']==str(out/'archives'/(str(ordinal).zfill(3)+'_'+Path(p['path']).name+'.gz'))and table[pgz['path']]==pgz,'whole new compressed product PF matches independent blind SHA twice')
  entrypin=row['entry_pin'];need(entrypin['path']==str(out/('archive_entry_'+str(ordinal).zfill(3)+'.json'))and meta(entrypin)=={k:v for k,v in row.items()if k!='entry_pin'}and table[entrypin['path']]==entrypin,'complete durable per-product entry exactly equals index metadata')
  current(p);archives.append(pgz);entrypins.append(entrypin);proofs.append({k:row[k]for k in('ordinal','original_plain_full_pin','compressed_archive_full_pin','compression_input_SHA','compression_input_length','streamed_decompressed_SHA','streamed_decompressed_length','exact_original_plain_bytes_recoverable','original_plain_preserved')})
 gzipbytes=sum(p['size_bytes']for p in archives);need(gzipbytes==index['total_gzip_bytes']==child['total_gzip_bytes']<b['bounded_archive_payload_bytes']and ownbytes<limit,'all4 gzip payload56MiB and entire own64MiB including metadata/runtime')
 need({p['path']for p in newpins if Path(p['path']).suffix=='.gz'}=={p['path']for p in archives},'all and only four new compressed files accounted')
 for p in [pHost,childpin,indexpin,wp,lp]+archives+entrypins:need(table[p['path']]==p,'all actual complete archive controls/outputs blind-SHA matched')
 childclaim=meta(table[str(out/'CHILD_ARCHIVE_CLAIM.json')]);need(type(childclaim['PID'])is int and type(childclaim['parent_PID'])is int and childclaim['PID']==w['pid']and childclaim['parent_PID']==claim['PID']and childclaim['retries']==0,'actual sole archive child/owning parent PID and no retry')
 for _ in range(2):
  for p in originals+retained+inputs:current(p)
  for p in b['explicit_cumulative_metadata_file_pins']:current_role(p,build)
 for key in('resources_before','resources_after','resources_after_including_summary_bytes'):archive_resources(host[key],roots,1800)
 archive_resources(child['resources_after'],roots,600)
 before=host['resources_before'];existing=before['complete_joint']['artifact_bytes']+before['explicit_external_metadata_bytes']+before['own_open_unlinked_bytes'];need(existing+limit+source_limit<2*2**30 and before['original_history']['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,'actual original prelaunch all4 coexist with full64/Source16/current2GiB/history96 reservation, no compression assumption')
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in b['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(root))for root in roots));unlinked=unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current original full cumulative/cold/free reserves including own open-unlinked')
 for item in(host,child,index):
  for key in('physics_qualified','AAA_qualified','ABA_admitted','goal_complete','result_values_decoded','numerical_executed','compiler_executed','native_executed','files_deleted','plain_retirement_authorized'):need(item[key]is False,'complete byte archival cannot issue scientific/control/retirement/goal qualifications')
 need(b['all48_or_JSONL_old_scope_reused_as_current_fact']is False and b['product_formats_decoded_or_claimed']is False and b['original_plain_retirement_in_this_stage']is False and b['future_aggregate_budget_added_to_this_stage']is False,'current exact B4 scope only; no old48/A2/early14 relabelling or retirement/aggregate admission')
 result=dict(schema='RECORDED_CURRENT_B4_COMPLETE_PRODUCT_LOSSLESS_ARCHIVE_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_ALL4_COMPLETE_B_PRODUCTS_STREAMED_SHA_LENGTH_ARCHIVE_METADATA_ONLY_ORIGINALS_RETAINED',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=0,actual_child_integer_exit_code=0,Source_freeze_pin=host['source_freeze_pin'],Host_freeze_pin=host['host_freeze_pin'],execution_binding_pin=pb,actual_child_report_pin=childpin,actual_archive_index_pin=indexpin,ordered4_original_product_full_pins=originals,ordered4_compressed_archive_full_pins=archives,ordered4_entry_pins=entrypins,actual_four_streamed_SHA_and_length_proof_records=proofs,original_product_bytes=originalbytes,gzip_bytes=gzipbytes,entire_archive_output_bytes=ownbytes,original4_current7_verified_twice_only=True,compressed4_fullEOF_SHA_current7_verified_twice=True,Root_actual_streamed_decompression_proofs_matched_original_fullPF=True,independent_decompression_or_numeric_recomparison=False,all4_original_products_current7_retained=True,all79_native_context_tree_and_SQL_pool_current7_retained=True,all11_originalB_input_current7_retained=True,retained79_native_context_tree_SQL_pool_current7_pins=retained,original11_B_input_current7_pins=inputs,original_guard_class_and_MRO_unchanged=True,actual_original_runner_record=record,actual_original_watchdog=w,actual_watchdog_pin=wp,actual_child_receipt_log_pin=lp,complete_joint_roots=roots,current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked,original_caps=CAPS,actual_original_host_resources_before=host['resources_before'],actual_original_host_resources_after=host['resources_after'],actual_original_host_resources_after_including_summary=host['resources_after_including_summary_bytes'],actual_child_resource_facts=child['resources_after'],all_new_output_blind_fullEOF_SHA_current7_twice_pins=newpins,actual_CLI_pin=cli_pin,actual_Source_peer_pin=hf['independent_Source_review_pin'],actual_Source_peer_tools_pin=hf['independent_Source_review_tools_pin'],actual_Root_Source_generation_tools_pin=hf['Root_Source_generation_true_tools_pin'],core_Source_author_freeze_pin=EXPECTED_CORE_AUTHOR_FREEZE,Source_author_also_authored_archive_workflow=False,old48_JSONL_A2_early14_fixed_labels_used_as_current_facts=False)
 save(result,source_limit,joint+extra+unlinked)
if __name__=='__main__':main()
