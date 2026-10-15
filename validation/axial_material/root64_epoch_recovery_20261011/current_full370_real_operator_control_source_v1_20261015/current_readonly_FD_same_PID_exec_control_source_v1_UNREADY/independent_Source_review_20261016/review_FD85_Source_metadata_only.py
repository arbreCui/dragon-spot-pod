"""Independent Source/JSON metadata/current7 reviewer. No candidate/helper import.

Does not compile, create fixtures, execute the probe, read scientific payloads,
or read object/compiler/native file contents.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import time

D=Path(__file__).absolute().parent.parent
P=Path(__file__).absolute().parent
START=time.monotonic()
SYSTEM=[]
def need(v,m):
    if v is not True:raise RuntimeError(m)
def ids(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
    q=Path(p['path']);s=q.lstat()
    fc=str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15' and p.get('sha256')=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492' and s.st_nlink==p['identity'][3]==2
    need(q.is_absolute() and stat.S_ISREG(s.st_mode) and (s.st_nlink==1 or fc) and ids(s)==p['identity'] and s.st_size==p['size_bytes'] and not any(x.is_symlink()for x in(q,*q.parents)),'exact current7 '+str(q))
    need(s.st_uid==os.getuid() or(s.st_uid==0 and p in SYSTEM),'only exact original delegated system roles')
def full(q):
    q=Path(q);s=q.lstat();need(s.st_size<8*2**20 and stat.S_ISREG(s.st_mode),'only named small Source/metadata full reads')
    a=q.read_bytes();b=q.read_bytes();need(a==b and ids(s)==ids(q.lstat()),'stable small whole bytes twice')
    p=dict(path=str(q),sha256=hashlib.sha256(a).hexdigest(),size_bytes=len(a),identity=ids(s));current(p);return p
def meta(p):
    need(Path(p['path']).suffix=='.json' and full(p['path'])==p,'exact JSON metadata fullPF')
    return json.loads(Path(p['path']).read_text())
def genuine(t,key,p,field):
    v=t[key];need(t['observed_closed']is True and type(t['original_integer_exit_code'])is int and t['original_integer_exit_code']==0 and type(v['exit_code'])is int and v['exit_code']==0 and v.get('session_id')is None and json.loads(v['output'].strip().splitlines()[-1])[field]==p,'genuine typed closed0 exact artifact')
def unique(rows):
    t={}
    for p in rows:
        if p['path']in t:need(t[p['path']]==p,'same exact fullPF for one path')
        t[p['path']]=p
    return t
def scan(q):
    q=Path(q)
    if not q.exists():return 0
    n=0
    for e in os.scandir(q):
        s=e.stat(follow_symlinks=False);need(not stat.S_ISLNK(s.st_mode),'no aliases in complete owning scope')
        if stat.S_ISDIR(s.st_mode):n+=scan(e.path)
        elif stat.S_ISREG(s.st_mode):n+=s.st_size
    return n
def main():
    global SYSTEM
    pa=full(D/'AUTHOR_SOURCE_FREEZE.json');need(pa['sha256']=='1dd24e717df4b3f9c881708896320b6836998dd9c44ed793597fa28f127f2780','final author pin')
    a=meta(pa);pp=a['plan_pin'];need(pp['sha256']=='81cb450d8c8888a29523ce59e195da1988f464965d98b7f00a527ee78b7b94b2','final PLAN pin');p=meta(pp)
    need(a['source_only']is True and a['Source_author_executed_compiler_helper_probe_or_scientific_payload']is False and a['Source_generation_or_publisher_required']is False and a['whole_Source_file_pins']==p['complete_source_file_pins'] and len(p['complete_source_file_pins'])==4 and p['host_source_pin']==a['host_source_pin'],'exact four Sources without GEN/pub framework')
    texts={}
    for x in p['complete_source_file_pins']:
        need(full(x['path'])==x,'all four Source wholebytes');name=Path(x['path']).name;texts[name]=Path(x['path']).read_text()
        if name.endswith('.py'):ast.parse(texts[name])
    need(meta(a['Source_static_evidence_pin'])['schema']=='NONSCIENTIFIC_FD_EXEC_CONTROL_SOURCE_ONLY_STATIC_EVIDENCE_V1','frozen static evidence schema')
    r=meta(p['runtime_actual_post_pin']);rt=meta(p['runtime_actual_post_tools_pin']);rh=meta(p['runtime_Host_report_pin']);rr=meta(p['runtime_Root_tools_pin'])
    genuine(rt,'actual_review_return',p['runtime_actual_post_pin'],'review_pin');genuine(rr,'actual_terminal_return',p['runtime_Host_report_pin'],'report_pin')
    need(r['schema']=='B_PLANE2_RUNTIME_COMPLETE71_BUILD_ACTUAL_METADATA_POSTVERIFY_V1' and r['status']=='PASS_ACTUAL_B_PLANE2_THREE_COMPILE_COMPLETE71_LINK_ROOT0_FOUR_CHILD0_METADATA_ONLY_NO_RUNTIME_QUALIFICATION' and r['failure']is None and type(r['actual_Root_integer_exit_code'])is int and r['actual_Root_integer_exit_code']==0 and r['actual_child_integer_exit_codes']==[0,0,0,0] and all(type(x)is int for x in r['actual_child_integer_exit_codes']) and r['actual_Host_report_pin']==p['runtime_Host_report_pin'] and r['actual_Root_tools_pin']==p['runtime_Root_tools_pin'],'genuine runtime build0/post0 only')
    need(rh['records']==r['actual_four_stage_records'] and len(r['actual_ordered71_link_inputs'])==71 and r['actual_original_owned_runtime_Root_integer_exit_code']==1 and r['actual_new_Dragon_pin']==p['retained_new_runtime_pin'] and r['new_runtime_compile_link_only_not_executed']is True,'complete71 new runtime and oldRoot1 facts preserved')
    roots=p['complete_joint_roots'];out=Path(p['planned_actual_output_root'])
    need(len(roots)==len(set(roots))==85 and roots==r['complete_joint_roots']+[str(out)] and not os.path.lexists(out) and not any(Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y),'full84 plus one fresh control85, no overlapping roots')
    need(p['schema']=='ROOT_NONSCIENTIFIC_READONLY_FD_SAME_PID_EXEC_CONTROL_PLAN_V1' and p['actual_runtime_build_and_independent_post_closed']is True and p['fixture_lengths']==[257,521,1031] and p['fixture_complete_bytes']==1809 and p['fixed_readonly_fd_numbers']==[101,102,103] and p['expected_child_integer_exit_codes']==a['expected_actual_child_codes']==[0,0,71,1,1] and p['expected_original_record_statuses']==['PASS','PASS','FAILED','FAILED','FAILED'],'precise tiny fixtures and original negative statuses')
    caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
    need(p['original_caps']==a['original_caps']==caps and p['bounded_new_output_reservation_bytes']==32*2**20 and p['bounded_own_Source_metadata_receipts_bytes']==8*2**20,'all original caps and local32/8 unchanged')
    build=meta(p['original_guard_build_plan_pin']);SYSTEM=build['readonly_system_SDK_header_pins']+build['readonly_system_tool_metadata_pins']+[build['C_compiler_pin']]
    sdk=Path(build['readonly_system_SDK_root']);need(ids(sdk.lstat())==build['readonly_system_SDK_root_identity'] and sdk.lstat().st_uid==0,'exact original SDK role delegation')
    ledger=unique(p['explicit_cumulative_metadata_file_pins']);oldpacket=meta(p['runtime_immutable_admission_packet_pin']);ext=oldpacket['all69_external_compile_toolchain_full_pins']
    need(len(ext)==69 and sum(x['size_bytes']for x in ext)==36068911 and all(ledger[x['path']]==x for x in ext),'all existing69 external compile/toolchain roles still accounted')
    need(p['exact59_historical_absent_pins']==r['exact59_historical_absent_pins'] and len(p['exact59_historical_absent_pins'])==59 and p['selected31_current_epoch_readonly_pins']==r['selected31_current_epoch_readonly_pins'],'latest exact lifecycle only')
    live=unique(list(ledger.values())+p['retained_current7_pins']+p['retained_archive_metadata_current7_pins']+p['retained_B2_current_epoch_readonly_pins']+p['selected31_current_epoch_readonly_pins']+[p['retained_new_runtime_pin'],p['Fortran_compiler_pin']])
    for x in live.values():current(x)
    failed=p['retained_failed_v1_current7_only_pins']+p['retained_failed_pool_archive_current7_only_pins'];need(len(failed)==15 and all(set(x)=={'path','size_bytes','identity'}for x in failed),'old failed8+7 only stat3')
    for x in failed:current(x)
    for x in p['exact59_historical_absent_pins']:need(not os.path.lexists(x['path']) and not any(q.is_symlink()for q in Path(x['path']).parents),'exact59 known absences only')
    need(p['retained_current7_pins']==list(unique(r['retained_all_current7_pins']+r['all_new_owning_output_blind_fullEOF_SHA_current7_twice_pins']).values()),'all prior current roles plus all18 runtime outputs preserved')
    for key in ('future_actual_Root_control_report_pin','future_actual_Root_control_tools_pin','future_actual_independent_control_post_pin','future_actual_independent_control_post_tools_pin','future_production_FD_launcher_Source_pin','future_PACK_pin'):need(p[key]is None,'future actual remains NULL')
    need(p['future_actual_FD_contract_control_pass']is None and p['production_native_paths_or_payloads_are_not_fixture_inputs']is True and p['production_launcher_must_not_have_negative_case_modes']is True,'control cannot authorize future production launcher')
    host=texts['run_readonly_FD_exec_contract_control_Root_only.UNREADY.py'];launcher=texts['open_fixture_FDs_then_same_PID_exec.UNREADY.py'];native=texts['readonly_fd_native_startup_control.UNREADY.f90'];contract=texts['readonly_FD_exec_control_contract.UNREADY.py']
    host_fragments=("full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)","full.OwnRSSSerialExecutor(m.OUT,1800-(time.monotonic()-start)","runner.execute(directory,label,cmd,600)","record['status']=='FAILED'", "expected!=0 or c.pin(lp)['sha256']==record['log_sha256']", "actual_original_record_status=record['status']", "(257,521,1031)", "bytes(65+(i*19+j*7)%26 for j in range(n))", "[0,0,71,1,1]", "receipt['PID']==w['pid']==receipt['process_group']", "w['command']==cmd==record['command']", "native_exec_reached']is False", "full.OwnRSSSerialExecutor", "open_unlinked_bytes=sum(unlinked.values())", "m.retained(plan)")
    for x in host_fragments:need(x in host,'original guard/real command/refusal facts: '+x)
    need(host.index("with(BASE/'ROOT_CONTROL_EXECUTION_CLAIM.json').open('x')")<host.index('initial(ps)')<host.index('spec.loader.exec_module(m)'),'claim before metadata or helper import')
    need(host.count('runner.execute(')==1 and "compile_cmd=[x for x in compile_cmd if x!='-c']"in host and "compile_cmd[-1]=str(probe)"in host and "for name,code in(('positive',0),('closed_fd',71),('wrong7',1),('duplicate_inode',1))"in host,'one compile/link invocation plus four controls, no retry')
    for x in ("FD_NUMBERS=(101,102,103)","os.O_RDONLY|os.O_NOFOLLOW","FD_SLOT_ALREADY_OCCUPIED","identity(st)==p['identity']","node not in seen","os.dup2(fd,target,inheritable=True)","os.get_inheritable(target)is True","rows[0]['identity'][6]-=1","rows=[rows[0],rows[0],rows[2]]","os.close(FD_NUMBERS[-1])","os.execv(str(q),native_argv)","native_exec_reached=False"):
        need(x in launcher,'exact samePID readonly FD launcher control: '+x)
    lt=ast.parse(launcher);need(not any(isinstance(n,ast.Import)and any(a.name=='subprocess'for a in n.names)for n in ast.walk(lt)) and launcher.count('os.execv(')==1 and 'os.fork('not in launcher and 'os.spawn'not in launcher,'no launcher subchild; samePID native replacement')
    for x in ('fixed_fds(3)=[101,102,103]','lengths(3)=[257,521,1031]','pid==expected_pid.and.grp==expected_grp.and.pid==grp',"name='/dev/fd/'//trim(number)//c_null_char","mode='rb'//c_null_char",'c_fopen(name,mode)','c_fread(c_loc(buf(1))','c_fseek(stream,17_c_long,0_c_int)','c_fseek(stream,0_c_long,0_c_int)','wrote==-1_c_long.and.err==9','INHERITED_FD_PRESENT','CLOSE_REOPENED_STREAM_KEEP_ORIGINAL','ORIGINAL_INHERITED_FD_REMAINS_PRESENT','FD_READONLY_EXEC_NATIVE_POSITIVE_V1'):
        need(x in native,'GNU/libc full fixture read/seek/readonly facts: '+x)
    need(max(map(len,native.splitlines()))<=132 and 'bind(C,name="__error")'in native and "sys.platform=='darwin'"in host,'declared Darwin errno constants checked by owning Host and free-form Fortran widths')
    need("scientific_native_payload_opened=False"in contract and 'production_FD_launcher_qualified=False'in contract and 'PACK_produced=False'in contract,'no production or scientific qualification')
    template_pin=full(D/'ROOT_REVIEWABLE_CLI_PENDING_GENUINE_SOURCE_PEER0.json');template=meta(template_pin);argv=template['argv']
    need(len(argv)==20 and argv[:11]==p['original_complete_ENV_Python_B_prefix'] and argv[11]==p['host_source_pin']['path'] and argv[12]=='--source-pin' and json.loads(argv[13])==p['host_source_pin'] and argv[14]=='--plan-pin' and json.loads(argv[15])==pp and argv[16:]==['--Source-review-pin','__GENUINE_INDEPENDENT_SOURCE_REVIEW_FULL_PIN__','--Source-review-tools-pin','__GENUINE_INDEPENDENT_SOURCE_REVIEW_TOOLS_FULL_PIN__'] and template['actual_independent_Source_review_pin']is None and template['actual_independent_Source_review_tools_pin']is None and template['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated','exact20 argv only two genuine peer placeholders, no GEN/pub')
    joint=sum(scan(q)for q in roots);extra=sum(x['size_bytes']for x in ledger.values()if not any(Path(x['path']).is_relative_to(Path(q))for q in roots))
    need(joint+extra+32*2**20+8*2**20<2*2**30 and scan(D)+150000<8*2**20,'stat-only current full85 plus32/8 fits; original runtime resource class remains mandatory')
    for x in p['complete_source_file_pins']:need(full(x['path'])==x,'whole four Source final freeze stable')
    result=dict(schema='INDEPENDENT_SOURCE_ONLY_NONSCIENTIFIC_FD_EXEC_CONTRACT_CONTROL_REVIEW_V1',status='PASS_SOURCE_ONLY_NONSCIENTIFIC_READONLY_FD_SAME_PID_EXEC_CONTROL',source_only=True,failure=None,executor_task_name='/root/b2_build_source_peer',source_pin=p['host_source_pin'],plan_pin=pp,complete_source_file_pins=p['complete_source_file_pins'],author_freeze_pin=pa,Root_CLI_template_pin=template_pin,actual_runtime_Root_tools_pin=p['runtime_Root_tools_pin'],actual_runtime_Host_report_pin=p['runtime_Host_report_pin'],actual_runtime_post_pin=p['runtime_actual_post_pin'],actual_runtime_post_tools_pin=p['runtime_actual_post_tools_pin'],expected_actual_child_codes=[0,0,71,1,1],expected_original_record_statuses=['PASS','PASS','FAILED','FAILED','FAILED'],three_negative_original_FAILED_records_preserved_by_Source=True,negative_log_fullPF_saved_without_missing_record_log_SHA_requirement=True,one_compile_link_and_four_distinct_controls=True,complete_fixture_bytes=1809,fixture_lengths=[257,521,1031],fixed_fd_numbers=[101,102,103],same_PID_process_group_exec_and_real_launcher_watch_command_Source_verified=True,O_RDONLY_NOFOLLOW_open_exact7_distinct_device_inode_and_inheritable_dup_verified=True,GNU_startup_libc_fopen_rb_fullfixture_EOF_seek_and_EBADF_Source_verified=True,all_previous_runtime_outputs_and_current_roles_preserved=True,complete_joint_roots=roots,original_caps=caps,bounded_output_bytes=32*2**20,bounded_Source_bytes=8*2**20,all69_external_compile_toolchain_bytes=36068911,complete_explicit_metadata_role_count=len(ledger),retained_failed_stat_only_count=15,exact_historical_absent_count=59,current_stat_only_joint_bytes=joint,current_exact_explicit_external_bytes=extra,whole_four_Source_verified_twice=True,reviewer_ran_original_runtime_resource_class=False,candidate_executed=False,helper_executed=False,compiler_executed=False,fixture_created=False,probe_executed=False,compiled_or_scientific_payload_body_read=False,production_FD_launcher_qualified=False,PACK_produced=False,new_B_formal13_compatible=False,online_BOOT_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,elapsed_review_seconds=time.monotonic()-START)
    q=P/'REVIEW.json'
    with q.open('x')as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    print(json.dumps(dict(status=result['status'],review_pin=full(q))),flush=True)
if __name__=='__main__':main()
