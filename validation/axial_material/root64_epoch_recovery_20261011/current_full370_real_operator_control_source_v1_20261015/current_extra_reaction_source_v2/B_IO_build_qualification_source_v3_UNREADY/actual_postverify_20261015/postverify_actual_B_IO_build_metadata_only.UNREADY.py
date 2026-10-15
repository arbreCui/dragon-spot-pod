"""Separate executor after actual compile/link closure. Never executes compiler/runtime/helpers."""
import argparse,hashlib,json,os,resource,shlex,stat,struct,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
AUTHOR_TASK='/root/b2_post_metadata_source'
FALSE=dict(B_native_executed=False,B_observation_context_produced=False,compiled_IO_semantics_qualified=False,
 original_binary_qualified=False,historical_C_compiler_restored=False,original_compiled_archive_ABI_or_features_reconstructed=False,
 compiler_or_nm_or_runtime_executed_by_post=False,worker_or_resource_helpers_imported=False,old_SCI_or_tool_body_opened_or_hashed=False,
 scientific_arrays_decoded=False,build_repeated=False,files_deleted=False,system_C_headers_transitive_EOF_claimed=False,new_compiled_ABI_or_IO_semantics_qualified=False,SDK_header_payloads_opened_or_hashed_by_post=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
def need(v,m):
 if type(v)is not bool or not v:raise RuntimeError(m)
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def cur(p,tool=False):
 q=Path(p['path']);s=q.lstat();ordinary=s.st_uid==os.getuid()and s.st_nlink==1
 fortran=tool and str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15'and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and s.st_nlink==p['identity'][3]==2
 system=tool and str(q)in('/Library/Developer/CommandLineTools/usr/bin/clang','/bin/ps','/usr/sbin/lsof')and s.st_uid==0 and s.st_nlink==1
 need(q.is_absolute()and stat.S_ISREG(s.st_mode)and ids(s)==p['identity']and s.st_size==p['size_bytes']
  and(ordinary or fortran or system)and not any(x.is_symlink()for x in(q,*q.parents)),'exact current7 and frozen role owner/link scope')
 return q
def full(p,budget):
 q=cur(p);h=hashlib.sha256();n=0
 with q.open('rb')as f:
  need(ids(os.fstat(f.fileno()))==p['identity'],'opened7')
  while b:=f.read(2**20):h.update(b);n+=len(b);budget()
  need(ids(os.fstat(f.fileno()))==p['identity'],'EOF7')
 cur(p);need(n==p['size_bytes']and h.hexdigest()==p['sha256'],'new output or metadata blindEOF SHA')
def read(p,budget):
 need(p['size_bytes']<8*2**20,'metadata8MiB');full(p,budget);v=json.loads(Path(p['path']).read_bytes());full(p,budget);return v
def pin(q,budget):
 s=q.lstat();h=hashlib.sha256()
 with q.open('rb')as f:
  while b:=f.read(2**20):h.update(b);budget()
 need(ids(q.lstat())==ids(s),'own metadata stable')
 return dict(path=str(q),sha256=h.hexdigest(),size_bytes=s.st_size,identity=ids(s))
def genuine(d,key,p,role):
 r=d[key];need(d['observed_closed']is True and type(d['original_integer_exit_code'])is int
  and d['original_integer_exit_code']==0 and type(r['exit_code'])is int and r['exit_code']==0
  and 'session_id'not in r and json.loads(r['output'].splitlines()[-1])[role]==p,'actual original closed0 exact stdoutPF')
def readonly_SDK_current(plan,evidence):
 root=Path(plan['readonly_system_SDK_root']);s=root.lstat()
 need(str(root)=='/Library/Developer/CommandLineTools/SDKs/MacOSX27.0.sdk'and root.is_absolute()and stat.S_ISDIR(s.st_mode)and s.st_uid==0 and ids(s)==plan['readonly_system_SDK_root_identity']and not any(x.is_symlink()for x in(root,*root.parents)),'exact Root-resolved canonical readonly system SDK directory current7, no alias exception')
 need(evidence['schema']=='ROOT_CURRENT_SYSTEM_SDK_RESOLUTION_SOURCE_EVIDENCE_V1'and evidence['canonical_sdk_root']==str(root)and evidence['canonical_sdk_root_identity']==plan['readonly_system_SDK_root_identity']and evidence['selected_header_pins']==plan['readonly_system_SDK_header_pins']and evidence['readonly_system_SDK']is True and evidence['transitive_system_headers_fullEOF_claimed']is False and evidence['compiler_executed']is False and evidence['ABI_qualified']is False and evidence['physics_qualified']is False,'actual frozen SDK Source evidence only, no transitive system-header or compiled ABI qualification')
 names={str(root/'usr/include'/name)for name in('stdio.h','stdlib.h','stdint.h')};pins=plan['readonly_system_SDK_header_pins']
 need(len(pins)==len({p['path']for p in pins})==3 and {p['path']for p in pins}==names,'exact three selected SDK Source roles, no generic system-owner allowance')
 for p in pins:
  q=Path(p['path']);s=q.lstat()
  need(q.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_uid==0 and s.st_nlink==1 and ids(s)==p['identity']and s.st_size==p['size_bytes']and not any(x.is_symlink()for x in(q,*q.parents)),'only frozen readonly SDK headers current7, no header body read or SHA replay')
 need(plan['explicit_new_clang_IO_compiler_route']is True and plan['C_compiler_pin']['path']=='/Library/Developer/CommandLineTools/usr/bin/clang'and plan['historical_C_compiler_restored']is False and plan['original_compiled_archive_ABI_or_features_reconstructed']is False and plan['system_C_headers_transitive_EOF_claimed']is False,'new explicit CLT clang plus SDK route stays separate from historical gcc/archive qualification')
def resource_facts(d):
 h=d['original_history'];j=d['complete_joint']
 need(d['host_SELF_peak_bytes']<512*2**20 and d['whole_elapsed_seconds']<1800
  and j['artifact_bytes']+d['explicit_external_metadata_bytes']+d['host_open_unlinked_bytes']<2*2**30
  and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30
  and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'actual original host/joint/history/cold/free caps')

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--Root-tools-pin',required=True);ap.add_argument('--Host-pin',required=True);ap.add_argument('--executor-task-name',required=True)
 a=ap.parse_args();started=time.monotonic();need(a.executor_task_name.startswith('/root/')and a.executor_task_name!=AUTHOR_TASK,'separate temp executor, not Source author')
 def budget():
  peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
  need(peak<512*2**20 and time.monotonic()-started<600,'postSELF512/stage600')
 pRoot=json.loads(a.Root_tools_pin);pHost=json.loads(a.Host_pin);raw=read(pRoot,budget);host=read(pHost,budget)
 need(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int
  and type(raw['actual_terminal_return']['exit_code'])is int and raw['actual_terminal_return']['exit_code']==raw['original_integer_exit_code'],'real terminal only, actual integer retained')
 sf=read(host['source_freeze_pin'],budget);hf=read(host['host_freeze_pin'],budget);plan=read(host['control_plan_pin'],budget)
 out=Path(plan['planned_actual_output_root']);need(pHost['path']==str(out/'Root_actual_B_IO_build_summary.json'),'literal owning Host report')
 need(host['schema']=='ACTUAL_B_IO_FOUR_COMPILE_ONE_LINK_QUALIFICATION_REPORT_V1','actual frozen main report schema')
 caps=host['original_caps'];need(caps==plan['original_caps']and caps['whole_seconds']==1800 and caps['stage_seconds']==600
  and caps['rss_mib']==512 and caps['fresh_bytes']==2*2**30 and caps['history_bytes']==96*2**30
  and caps['threads']==caps['children_at_once']==1 and caps['retries']==0,'original full caps')
 need(len(plan['complete_joint_roots'])==68 and plan['complete_joint_roots'][-1]==str(out),'whole68 prefix owning output')
 latest=read(plan['latest_complete_plan_pin'],budget)
 need(latest['complete_joint_roots']==plan['complete_joint_roots'][:-1]and len(latest['complete_joint_roots'])==67,'complete prior failed67 prefix retained before one fresh owning B3 root')
 sdk=read(plan['system_SDK_Source_evidence_pin'],budget)
 for _ in range(2):readonly_SDK_current(plan,sdk)
 need(sum(q.lstat().st_size for q in PACKAGE.rglob('*')if q.is_file())<16*2**20,'entire Source and metadata namespace16MiB')
 for _ in range(2):
  for p in plan['compile_and_link_input_pins']+plan['original_SCI_current7_only_pins']:cur(p,True)
  for p in plan['historical48_plain_full_pins']:need(not os.path.lexists(p['path']),'only genuinely retired historical48 absent')
  for p in plan['current48_compressed_archive_pins']:cur(p)
 need(len(plan['compile_and_link_input_pins'])==180 and len(plan['historical48_plain_full_pins'])==48,'actual current180 build inputs vs historical48 role separation')
 newpins=host['whole_new_output_pins'];seen={p['path']:p for p in newpins}
 need(len(seen)==len(newpins),'unique owning output PFs')
 for p in newpins:
  need(Path(p['path']).is_relative_to(out),'new product only owning scope');full(p,budget);full(p,budget)
 code=raw['original_integer_exit_code']
 if code!=0:
  report=dict(schema='B_IO_BUILD_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,
   actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=code,
   actual_failed_Host_status=host['status'],actual_Host_failure=host['failure'],actual_stage_records=host['records'],
   actual_watchdog_checks=host['actual_watchdog_checks'],new_partial_output_fullEOF_pins=newpins,success_or_native_qualification_inferred=False,**FALSE)
 else:
  genuine(raw,'actual_terminal_return',pHost,'report_pin')
  need(raw['actual_execution_permission_mode']=='require_escalated','original PS guard permission role')
  need(host['status']=='ACTUAL_B_IO_BUILD_FIVE_STAGE0_CLOSED_ONLY'and host['failure']is None
   and host['final_report_resource_check_passed']is True and host['original_guard_MRO_unchanged']is True
   and host['original_guard_class']=='OwnRSSSerialExecutor'and host['build_stage_count']==5,'actual five-stage guarded build only')
  peer=read(sf['independent_Source_review_pin'],budget);peerTools=read(sf['independent_Source_review_tools_pin'],budget)
  genuine(peerTools,'actual_review_return',sf['independent_Source_review_pin'],'review_pin')
  need(peer['source_only']is True and peer['failure']is None and peer['status'].startswith('PASS'),'actual independent B Source review0')
  need(len(sf['complete_source_file_pins'])==33,'same frozen B3 complete33 Source roles')
  for p in sf['complete_source_file_pins']:full(p,budget);full(p,budget)
  cliPin=pin(PACKAGE/'FINAL_ROOT_REVIEWABLE_CLI.json',budget);cli=read(cliPin,budget)
  need(shlex.split(raw['exact_executed_command'])==cli['argv']and len(cli['argv'])==24,'actual complete published24 argv')
  expected=plan['exact_five_stage_commands'];need(len(expected)==len(host['records'])==len(host['actual_watchdog_checks'])==5,'exact5 stages once')
  for ordinal,(record,watch,command)in enumerate(zip(host['records'],host['actual_watchdog_checks'],expected)):
   w=watch['actual_watchdog'];need(record['command']==w['command']==command and record['status']=='PASS'
    and type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None
    and w['own_child_only']is True and w['liveness_group_cleanup']is True and w['rss_cap_mib']==512
    and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600,'actual original child0/wall/RSS/liveness per stage')
   need(watch['actual_stage_record_label']==record['label']
    and watch['actual_watchdog_pin']['path']==str(out/(record['label']+'.watchdog.json'))
    and watch['actual_log_pin']['path']==str(out/(record['label']+'.log'))
    and watch['actual_log_pin']['sha256']==record['log_sha256'],'original record.label stage-prefixed monitor/log')
   need(read(watch['actual_watchdog_pin'],budget)==w,'actual watchdog bytes equal Host metadata')
   if ordinal in(1,2,3):
    i=command.index('-include');need(command[i+1]==str(out/'sources/B_IO_ABI_ASSERTIONS.h'),'same exact ABI assertions compiled in each of3 C translation units')
    need(command.count('-isysroot')==1 and command[command.index('-isysroot')+1]==plan['readonly_system_SDK_root'],'same exact canonical SDK explicitly in all three actual C compile commands')
  link=expected[-1];need(sum(v.endswith('.o')for v in link)==74 and sum(v.endswith('.a')for v in link)==4
   and host['original_explicit_object_count']==71 and host['new_explicit_object_count']==74
   and host['archive_count']==4 and host['old_link_argv_inverse_equal']is True,'original71+4→new74+4 link input scope')
  need(len(plan['whole_byte_build_source_copy_pins'])==6,'whole6 build Source/header copies')
  copied=[]
  for p in plan['whole_byte_build_source_copy_pins']:
   q=seen[str(out/'sources'/Path(p['path']).name)];need(q['sha256']==p['sha256']and q['size_bytes']==p['size_bytes'],'whole build Source/header copy preserved');copied.append(q)
  runtime=seen[str(out/'sources/runtime/Dragon')]
  with cur(runtime).open('rb')as f:header=f.read(32)
  need(len(header)==32,'new runtime MachO header');mh=struct.unpack('<IiiIIIII',header)
  need(mh[0]==0xfeedfacf and mh[1]==0x100000c and mh[3]==2,'new arm64 MachO64 executable emitted; not executed or ABI-complete qualification')
  resource_facts(host['resources_before']);resource_facts(host['resources_after'])
  ownbytes=sum(q.lstat().st_size for q in out.rglob('*')if q.is_file());need(ownbytes<32*2**20,'all sources/objects/runtime/log/watch/report32MiB')
  for key in FALSE:
   if key in host:need(host[key]is False,'build closure must not mint native/physics/historical compiler qualifications')
  report=dict(schema='RECORDED_B_IO_FIVE_STAGE_BUILD_METADATA_POSTVERIFY_V1',
   status='PASS_ACTUAL_B_IO_FOUR_COMPILE_ONE_LINK_STAGE0_METADATA_ONLY_NO_NATIVE_QUALIFICATION',failure=None,
   actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=0,actual_child_integer_exit_codes=[0]*5,
   Source_freeze_pin=host['source_freeze_pin'],Host_freeze_pin=host['host_freeze_pin'],control_plan_pin=host['control_plan_pin'],actual_CLI_pin=cliPin,
   actual_Source_peer_pin=sf['independent_Source_review_pin'],actual_Source_peer_tools_pin=sf['independent_Source_review_tools_pin'],
   actual5_stage_records=host['records'],actual5_watchdog_checks=host['actual_watchdog_checks'],new_output_fullEOF_SHA_current7_twice_pins=newpins,
   old180_compile_link_inputs_and2_SCI_current7_only=True,historical48_plain_roles_absent_not_current_inputs=True,
   same3C_ABI_assertion_include_scope=True,same3C_explicit_canonical_SDK_scope=True,SDK_Source_evidence_pin=plan['system_SDK_Source_evidence_pin'],readonly_system_SDK_root=plan['readonly_system_SDK_root'],readonly_system_SDK_root_identity=plan['readonly_system_SDK_root_identity'],selected_readonly_system_SDK_header_current7_pins=plan['readonly_system_SDK_header_pins'],SDK_selected_headers_current7_only=True,original_explicit_objects=71,new_explicit_objects=74,archive_count=4,
   whole_copied_Source_and_header_pins=copied,new_runtime_full_pin=runtime,new_runtime_MachO_header_hex=header.hex(),
   new_runtime_architecture='Darwin_arm64_MachO64_executable',new_runtime_not_executed=True,owning_output_bytes=ownbytes,
   complete_joint_roots=plan['complete_joint_roots'],original_caps=caps,resources_before=host['resources_before'],resources_after=host['resources_after'],**FALSE)
 report.update(metadata_only=True,Source_author_task=AUTHOR_TASK,original_template_Source_author_task='/root/formal_goal_remaining_audit',v2_adaptation_Source_author_task=AUTHOR_TASK,v3_adaptation_Source_author_task=AUTHOR_TASK,Source_author_did_not_author_B_build_workflow=False,post_Source_author_also_authored_B3_build_contract=True,
  actual_executor_task=a.executor_task_name,actual_post_not_executed_by_Source_author=True,
  wall_seconds=time.monotonic()-started,reviewer_Source_pin=pin(Path(__file__).absolute(),budget))
 target=BASE/'REVIEW.json';b=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(b)<8*2**20,'own post report8MiB')
 with target.open('xb')as f:f.write(b);f.flush();os.fsync(f.fileno())
 budget();need(sum(q.lstat().st_size for q in PACKAGE.rglob('*')if q.is_file())<16*2**20,'entire Source and metadata namespace16MiB after post report');print(json.dumps(dict(status=report['status'],review_pin=pin(target,budget))),flush=True)

if __name__=='__main__':main()
