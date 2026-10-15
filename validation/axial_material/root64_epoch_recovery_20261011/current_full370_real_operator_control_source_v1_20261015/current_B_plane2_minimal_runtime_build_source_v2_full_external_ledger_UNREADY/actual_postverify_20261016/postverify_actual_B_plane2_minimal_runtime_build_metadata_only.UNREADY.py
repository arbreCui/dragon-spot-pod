"""UNREADY independent metadata post for the actual three-compile complete71-link build metadata control.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. Only Source and saved metadata are read. Original products and gzip files get current7 only; no repeated decompression or value decoding.
The exact pre-GEN author freeze is bound below; actual execution remains NULL.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_B_plane2_minimal_runtime_build_source_v2_full_external_ledger_UNREADY/AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json', 'sha256': '66c575ca49945f375ccbf527ddd919706accdfbedfbac46cd71f07f6792f6882', 'size_bytes': 8854, 'identity': [16777229, 50954565, 33188, 1, 8854, 1792081541316673502, 1792081541316673502]}
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(compiler_executed=False,native_executed=False,children_started_by_post=False,worker_or_guard_helpers_imported=False,original_plain_payload_body_opened=False,original_plain_payload_SHA_recomputed=False,gzip_payload_body_opened_by_post=False,compression_repeated=False,decompression_repeated=False,restored_product_file_written=False,scientific_values_decoded=False,files_deleted=False,retirement_authorized=False,paired_SQL_pool_archive_complete=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
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
def member0_resource_facts(v,roots):
 need(v['SELF_peak_bytes']<512*2**20 and 0<=v['original_elapsed_seconds']<600 and v['complete_joint_root_count']==len(roots)and v['non_scalar_resource_inventories_omitted']is True,'actual original Root-only SELF512/stage600 and scalar snapshots for entire bound root topology')
 h=v['original_history'];j=v['complete_joint']
 need(j['artifact_bytes']+v['explicit_external_metadata_bytes']+v['own_open_unlinked_bytes']<2*2**30 and h['artifact_bytes']+20971764748+64*2**20<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'actual saved original cumulative/history/cold/metadata/free caps')
def save(report,source_limit,joint_existing=None):
 report.update(metadata_only=True,Source_author_task=AUTHOR,actual_executor_task=EXECUTOR,actual_post_not_executed_by_Source_author=True,reviewer_Source_pin=pin(Path(__file__).absolute()),helper_or_candidate_module_imported=False,Source_GEN_or_publication_executed=False,native_or_compiler_or_worker_executed=False,scientific_values_or_SQLite_or_native_XSM_or_context_body_decoded=False,original_collect_or_snapshot_pair_readback_repeated=False,historical_issue_records_modified=False,wall_seconds=time.monotonic()-START,**FALSE)
 raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20,'post control report6MiB')
 need(counted_bytes([str(PACKAGE)])+len(raw)<source_limit,'entire Source/metadata bound including new post')
 if joint_existing is not None:need(joint_existing+len(raw)<2*2**30,'entire current cumulative2GiB including post')
 q=BASE/'REVIEW.json'
 with q.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 budget();print(json.dumps(dict(status=report['status'],review_pin=pin(q))),flush=True)


R=ROOT
OUT=R / 'validation/artifacts/axial-material-current-B-plane2-minimal-runtime-complete71-build-only-20261016-v1'
FLAGS=['-O2', '-march=native', '-ffp-contract=off', '-fcheck=all', '-fbacktrace', '-g', '-fPIC', '-frecord-marker=4', '-ffixed-line-length-none']

def unique(rows):
 t={}
 for p in rows:
  if p['path']in t:need(t[p['path']]==p,'one exact fullPF per path')
  t[p['path']]=p
 return list(t.values())

def load_plan(p):
    view = meta(p)
    need(view['schema'] == 'B_PLANE2_RUNTIME_SOURCE_ONLY_PLAN_V1', 'exact compact PLAN schema')
    packet = meta(view['admission_packet_pin'])
    need(packet['schema'] == 'ROOT_B_PLANE2_MINIMAL_RUNTIME_BUILD_CURRENT_ADMISSION_PACKET_V1', 'exact immutable complete admission packet')
    return dict(packet, **view)

def admit_lifecycle(plan):
    need(plan['actual_business_preconditions_closed'] is True, 'corrected actual bridge0/post0 and latest83 budget remain NULL hard reject')
    b = meta(plan['epoch_bridge_binding_pin'])
    r = meta(plan['epoch_bridge_report_pin'])
    raw = meta(plan['epoch_bridge_Root_tools_pin'])
    p = meta(plan['epoch_bridge_corrected_post_pin'])
    pt = meta(plan['epoch_bridge_corrected_post_tools_pin'])
    genuine(raw, 'actual_terminal_return', plan['epoch_bridge_report_pin'], 'report_pin')
    genuine(pt, 'actual_review_return', plan['epoch_bridge_corrected_post_pin'], 'review_pin')
    need(p['schema'] == 'A1_A3_FORMAL31_CURRENT_EPOCH_BRIDGE_ACTUAL_METADATA_POSTVERIFY_V1' and p['status'] == 'PASS_ACTUAL_A1_A3_SELECTED18_FORMAL13_CURRENT_EPOCH_ROOT0_CURRENT7_METADATA_ONLY_NO_COMPATIBILITY_QUALIFICATION' and (p['failure'] is None) and (p['actual_Root_integer_exit_code'] == 0) and (type(p['actual_Root_integer_exit_code']) is int) and (p['actual_bridge_report_pin'] == plan['epoch_bridge_report_pin']) and (p['actual_Root_tools_pin'] == plan['epoch_bridge_Root_tools_pin']) and (p['binding_pin'] == plan['epoch_bridge_binding_pin']), 'genuine corrected selected31 metadata post0 binds unchanged Root0')
    need('/actual_postverify_corrected_exact_two_formal_metadata_overlap_20261016/' in plan['epoch_bridge_corrected_post_pin']['path'] and p['actual_Source_author_freeze_pin'] == plan['epoch_bridge_author_freeze_pin'] and (p['all31_current_epoch_roles_current7_verified_twice'] is True) and (p['all_retained_roles_current7_verified_twice'] is True) and (p['actual_selected_role_count'] == 31) and (p['actual_selected_blind_verified_bytes'] == 680089850), 'exact corrected post namespace and whole31 bytes, no old failed post promotion')
    need(r['ordered_role_pairs'] == p['ordered_role_pairs'] and len(r['ordered_role_pairs']) == 31 and ([x['current_epoch_full_pin'] for x in p['ordered_role_pairs']] == plan['selected31_current_epoch_readonly_pins']) and all((x['blind_complete_SHA_and_length_equal'] is True and x['before_open_EOF_after_current7_stable'] is True for x in p['ordered_role_pairs'])), 'whole original31 current epoch byte bindings only')
    need(r['new_B_bearing_context_compatibility_or_lineage_proved'] is False and p['new_B_bearing_context_compatibility_or_lineage_proved'] is False and (p['online_BOOT_qualified'] is False) and (p['historical_independent_genuine_typed0_asserted'] is False), 'bytebridge is not formal compatibility or invented old independent success')
    need(plan['complete_joint_roots'] == p['complete_joint_roots'] + [str(OUT)] and p['complete_joint_roots'] == b['complete_joint_roots'] and (len(plan['complete_joint_roots']) == 84) and (len(set(plan['complete_joint_roots'])) == 84) and (not any((Path(x).is_relative_to(Path(y)) for x in plan['complete_joint_roots'] for y in plan['complete_joint_roots'] if x != y))) and (plan['original_caps'] == p['original_caps'] == CAPS), 'entire latest83 plus one new whole build84, no subset or cap change')
    for key in ('retained_archive_metadata_current7_pins', 'retained_B2_current_epoch_readonly_pins', 'retained_failed_v1_current7_only_pins', 'retained_failed_pool_archive_current7_only_pins', 'exact59_historical_absent_pins'):
        need(plan[key] == p[key], 'same exact latest retained and historical roles')
    need(plan['retained_current7_pins'] == p['retained_all_current7_pins'] and plan['bridge_explicit_cumulative_metadata_file_pins'] == p['explicit_cumulative_metadata_file_pins'], 'latest complete current and explicit metadata roles inherited verbatim')
    need(any((BASE.is_relative_to(Path(x)) for x in p['complete_joint_roots'])) and os.path.lexists(OUT), 'Source remains within existing FTOP and actual build owning root is now present')
    op = meta(plan['original_owned70_plan_pin'])
    h = meta(plan['original_owned70_report_pin'])
    hr = meta(plan['original_owned70_Root_tools_pin'])
    hp = meta(plan['original_owned70_post_pin'])
    ht = meta(plan['original_owned70_post_tools_pin'])
    genuine(ht, 'actual_review_return', plan['original_owned70_post_pin'], 'review_pin')
    v = hr['actual_terminal_return']
    need(hr['observed_closed'] is True and type(hr['original_integer_exit_code']) is int and (hr['original_integer_exit_code'] == 1) and (type(v['exit_code']) is int) and (v['exit_code'] == 1) and (v.get('session_id') is None), 'old original Root1 completion parser failure retained, never rewritten0')
    need(hp['schema'] == 'INDEPENDENT_A8_18_OWNED_MAP_LIFETIME_V2_ACTUAL_RUNTIME_POSTVERIFICATION_V1' and hp['status'] == 'PASS_ACTUAL_A8_18_OWNED_MAP_LIFETIME_V2_THREE_STAGE0_COMPLETE_PAIR_FACTS_POSTVERIFIED_HOST_COMPLETION_PARSER_FAILURE_RETAINED' and (hp['failure'] is None) and (hp['actual_Root_exit_code'] == 1) and (hp['actual_report_pin'] == plan['original_owned70_report_pin']) and (hp['actual_Root_true_tool_return_pin'] == plan['original_owned70_Root_tools_pin']) and (hp['actual_stage_statuses'] == ['PASS', 'PASS', 'PASS']), 'genuine old post0 preserves Root1 and actual three child stage0 facts')
    rows = plan['original_current70_ordered_input_pins']
    need(rows == op['current_owned_runtime_ordered70_pins'] == hp['actual_ordered70_input_pins'] and [x['path'] for x in rows] == h['actual_ordered70_link_inputs'] and (len(rows) == len({x['path'] for x in rows}) == 70), 'exact actual latest70 complete saved inputs not original cache70')
    need(h['records'][0]['status'] == h['records'][1]['status'] == 'PASS' and h['records'][1]['command'] == plan['original_current70_link_command'] and (h['records'][0]['command'] == plan['original_current_compile_command']), 'actual old compile/link0 commands only; old business status stays unchanged')
    return p

def commands(plan):
 old=plan['original_current70_link_command'];rows=plan['original_current70_ordered_input_pins'];paths=[p['path']for p in rows];first=plan['original_current_compile_command'];fc=plan['original_Fortran_compiler_pin']['path']
 need(old==[fc,'-O2','-ffp-contract=off',*paths,'-o',plan['historical_original_Dragon_output_path']]and first[0]==fc and first[1:10]==FLAGS and [x for x in first if x.startswith('-I')]==plan['original_compile_include_arguments'],'exact original compiler, flags and include order authority')
 need([Path(paths[i]).name for i in(14,66)]==['KDRDRV.o','APACKX64.o']and next(i for i,x in enumerate(paths)if x.endswith('.a'))==58 and sum(x.endswith('.o')for x in paths)==66 and sum(x.endswith('.a')for x in paths)==4,'actual complete70 positions14/66 and archive58, original66objects+4archives')
 inc=['-I'+str(OUT/'sources/build')]+plan['original_compile_include_arguments'];sources=['APACKX64.f90','B2PLNX64.UNREADY.f90','KDRDRV.F'];objects=['APACKX64.o','B2PLNX64.o','KDRDRV.o'];compiles=[[fc,*FLAGS,*inc,'-J'+str(OUT/'sources/build'),'-c',str(OUT/'sources'/s),'-o',str(OUT/'sources/build'/o)]for s,o in zip(sources,objects)]
 replaced=list(paths);replaced[14]=str(OUT/'sources/build/KDRDRV.o');replaced[66]=str(OUT/'sources/build/APACKX64.o');insert=str(OUT/'sources/build/B2PLNX64.o');new=replaced[:58]+[insert]+replaced[58:]
 inverse=[x for x in new if x!=insert];inverse[14]=paths[14];inverse[66]=paths[66]
 need(inverse==paths and len(new)==len(set(new))==71 and sum(x.endswith('.o')for x in new)==67 and sum(x.endswith('.a')for x in new)==4 and [(i,a,z)for i,(a,z)in enumerate(zip(paths,replaced))if a!=z]==[(14,paths[14],replaced[14]),(66,paths[66],replaced[66])],'whole71 inverse to70: two replacements, one insertion, other68 unchanged and all archive order retained')
 return dict(compile_commands=compiles,link_command=[fc,'-O2','-ffp-contract=off',*new,'-o',str(OUT/'sources/runtime/Dragon')],ordered71_link_inputs=new,old_link_argv_inverse_equal=True)

def build_resource_facts(v,roots):
 h=v['original_history'];j=v['complete_joint'];ps=v['Root_same_PID_PS']
 need(j['resource_root_count']==len(roots)==84 and type(v['host_SELF_peak_bytes'])is int and v['host_SELF_peak_bytes']<512*2**20 and 0<=v['whole_elapsed_seconds']<1800,'actual full84/RootSELF512/whole1800 compact saved resource facts')
 need(type(ps['returncode'])is int and ps['returncode']==0 and ps['stderr']==''and len(ps['stdout'])<1024 and ps['stdout'].strip().isdigit()and int(ps['stdout'].strip())*1024<512*2**20,'saved same-PID original PS RSS result, never reexecuted')
 need(j['artifact_bytes']+v['explicit_external_metadata_bytes']+v['host_open_unlinked_bytes']<2*2**30 and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original history96/joint2/cold/meta64/free8 include exact external/openunlinked')

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for name in('Root-tools-pin','Host-pin','executor-task-name'):ap.add_argument('--'+name,required=True)
 a=ap.parse_args();need(a.executor_task_name==EXECUTOR and a.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'independent once-only build metadata post, never author self-run')
 need(type(EXPECTED_CORE_AUTHOR_FREEZE)is dict,'exact final full-external-ledger author freeze PF')
 pRoot=json.loads(a.Root_tools_pin);pHost=json.loads(a.Host_pin);raw=meta(pRoot);terminal=raw['actual_terminal_return'];host=None if pHost is None else meta(pHost)
 need(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and type(terminal['exit_code'])is int and terminal['exit_code']==raw['original_integer_exit_code']and terminal.get('session_id')is None and raw['actual_retried']is False,'genuine original typed closed Root integer/no session/no retry')
 author=meta(EXPECTED_CORE_AUTHOR_FREEZE);ready=meta(pin(PACKAGE/'SOURCE_REVIEW_READY.json'));plan=load_plan(ready['control_plan_pin']);source_limit=plan['bounded_new_Source_metadata_reservation_bytes'];need(source_limit==8*2**20 and plan['bounded_new_output_reservation_bytes']==32*2**20 and plan['original_caps']==CAPS and plan['planned_actual_output_root']==str(OUT),'exact small PLAN expanded immutable packet and original caps/Source8/output32')
 cliPin=pin(PACKAGE/'FINAL_ROOT_REVIEWABLE_CLI.json');cli=meta(cliPin);need(cli['schema']=='B_PLANE2_RUNTIME_BUILD_FINAL_REVIEWABLE_ROOT_CLI_V1'and raw['actual_execution_permission_mode']=='require_escalated'and raw['exact_executed_command']==cli['command']and shlex.split(cli['command'])==cli['argv']and len(cli['argv'])==24,'genuine final original full24 CLI and required permission, even for recorded failure')
 need(author['schema']=='B_PLANE2_MINIMAL_RUNTIME_BUILD_AUTHOR_SOURCE_FREEZE_V2_FULL_EXTERNAL_LEDGER'and author['Source_only_frozen_before_Root_generation']is True and author['compiler_or_native_executed_by_author']is False and author['immutable_admission_packet_pin']==plan['admission_packet_pin']and author['whole_Source_file_pins']==ready['complete_source_file_pins']and len(author['whole_Source_file_pins'])==7,'final author-packet samePF and seven exact Source bytes; no v1/interim execution inferred')
 for p in author['whole_Source_file_pins']:full(p)
 if host is not None:need(pHost['path']==str(OUT/'Root_actual_B_plane2_minimal_runtime_build_summary.json')and host['schema']=='ACTUAL_B_PLANE2_MINIMAL_RUNTIME_THREE_COMPILE_COMPLETE71_LINK_REPORT_V1','same actual emitted owning build report role')
 code=raw['original_integer_exit_code']
 if code!=0:
  result=dict(schema='B_PLANE2_RUNTIME_BUILD_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=code,actual_Host_status=None if host is None else host['status'],actual_Host_failure=None if host is None else host['failure'],actual_stage_records=None if host is None else host['records'],actual_watchdog_checks=None if host is None else host['actual_watchdog_checks'],compile_link_success_or_online_qualification_inferred=False,partial_objects_or_Dragon_body_opened_or_hashed=False)
  save(result,source_limit);return
 need(host is not None,'Root0 requires actual emitted build report PF');genuine(raw,'actual_terminal_return',pHost,'report_pin');stdout=json.loads(terminal['output'].strip().splitlines()[-1])
 need(raw['actual_execution_permission_mode']=='require_escalated'and pHost['path']==str(OUT/'Root_actual_B_plane2_minimal_runtime_build_summary.json')and host['schema']=='ACTUAL_B_PLANE2_MINIMAL_RUNTIME_THREE_COMPILE_COMPLETE71_LINK_REPORT_V1'and host['status']=='ACTUAL_B_PLANE2_MINIMAL_RUNTIME_FOUR_STAGE0_BUILD_ONLY'and host['failure']is None and host['secondary_failures']==[]and host['final_report_resource_check_passed']is True and host['original_guard_class']=='OwnRSSSerialExecutor'and host['original_guard_MRO_unchanged']is True and host['original_caps']==CAPS and stdout['new_binary_actual_compile_link_only']is True,'genuine Root0 exact original OwnRSS class/MRO four-stage compile-link closure only')
 sf=meta(host['source_freeze_pin']);hf=meta(host['host_freeze_pin']);need(sf['schema']=='B_PLANE2_RUNTIME_SOURCE_FREEZE_V1'and hf['schema']=='B_PLANE2_RUNTIME_HOST_FREEZE_V1'and sf['source_only']is True and sf['business_executed']is False and hf['selected_source_freeze_pin']==host['source_freeze_pin']and sf['control_plan_pin']==host['control_plan_pin']==ready['control_plan_pin']and sf['complete_source_file_pins']==ready['complete_source_file_pins']==author['whole_Source_file_pins']and len(sf['complete_source_file_pins'])==7,'exact complete seven author-frozen Sources and Source/Host/PLAN binding')
 peerpin=sf['independent_Source_review_pin'];peertools_pin=sf['independent_Source_review_tools_pin'];peer=meta(peerpin);peertools=meta(peertools_pin);genuine(peertools,'actual_review_return',peerpin,'review_pin')
 need(peer['status']=='PASS_SOURCE_ONLY_B_PLANE2_MINIMAL_RUNTIME_COMPLETE71_BUILD'and peer['source_only']is True and peer['failure']is None and peer['control_plan_pin']==host['control_plan_pin']and peer['complete_source_file_pins']==sf['complete_source_file_pins'],'actual complete owning Source review0 distinct from runtime qualification')
 need(cli['source_freeze_pin']==host['source_freeze_pin']and cli['host_freeze_pin']==host['host_freeze_pin']and hf['host_source_pin']==ready['host_source_pin']and hf['contract_Source_pin']==ready['contract_Source_pin']and hf['original_caps']==CAPS and hf['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated'and hf['compiler_executed']is False,'same exact Source and Host freeze roles and original admission only')
 need(hf['explicit_cumulative_metadata_file_pins']==unique(plan['explicit_cumulative_metadata_file_pins']+[peerpin,peertools_pin,host['source_freeze_pin'],host['control_plan_pin']]),'entire ordered deduplicated published metadata and toolchain ledger retained, no subset or overlap deduction')
 admit_lifecycle(plan);expected=commands(plan);stages=expected['compile_commands']+[expected['link_command']];need(stages==plan['exact_four_stage_commands']and len(stages)==len(host['records'])==len(host['actual_watchdog_checks'])==host['build_stage_count']==4,'exact three compile and one link stage commands once each')
 labels=['compile_APACKX64','compile_B2PLNX64','compile_KDRDRV','link_complete71_Dragon'];childcodes=[]
 for record,wrapped,command,label in zip(host['records'],host['actual_watchdog_checks'],stages,labels):
  w=wrapped['actual_watchdog'];need(record['label'].split('/')[-1]==label and record['status']=='PASS'and record['command']==w['command']==command and type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None and w['rss_cap_mib']==512 and w['own_child_only']is True and w['liveness_group_cleanup']is True and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600,'actual original per-label own-child0/RSS512/stage600/liveness group closure')
  need(wrapped['actual_stage_record_label']==record['label']and wrapped['actual_watchdog_pin']['path']==str(OUT/(record['label']+'.watchdog.json'))and wrapped['actual_log_pin']['path']==str(OUT/(record['label']+'.log'))and wrapped['actual_log_pin']['sha256']==record['log_sha256']and meta(wrapped['actual_watchdog_pin'])==w,'actual standalone watcher/log metadata use exact record.label and fullPF')
  childcodes.append(w['returncode'])
 link=expected['ordered71_link_inputs'];old70=plan['original_current70_ordered_input_pins'];need(host['actual_ordered71_link_inputs']==plan['planned_ordered71_link_inputs']==link and len(link)==len(set(link))==71 and host['new_explicit_object_count']==67 and host['original_explicit_object_count']==66 and host['archive_count']==4 and host['old_link_argv_inverse_equal']is True and expected['old_link_argv_inverse_equal']is True,'full ordered71 inverse to true70 only replacements14/66 and insertion58; original68 and four archives unchanged')
 build=meta(plan['original_guard_build_plan_pin']);coverage=meta(author['Source_static_whole_reverse_and_scope_pin']);codeinputs=unique(plan['compile_and_link_input_pins']);ext=plan['all69_external_compile_toolchain_full_pins'];table={p['path']:p for p in hf['explicit_cumulative_metadata_file_pins']};history_roots=[str(q)for q in(ROOT/'validation/artifacts').glob('axial-material-*')];coverage_rows=coverage['all_declared_compile_toolchain_support_and_new_Source_current7_coverage'];covered={x['full_pin']['path']:x['full_pin']for x in coverage_rows}
 need(coverage['schema']=='B_PLANE2_RUNTIME_V2_ALL_DECLARED_INPUT_EXTERNAL_LEDGER_COVERAGE_SOURCE_ONLY_V1'and len(codeinputs)==coverage['code_input_count']==178 and len(coverage_rows)==len(covered)==191 and all(covered[p['path']]==p for p in codeinputs+plan['whole_byte_build_source_copy_pins'])and plan['all69_external_compile_toolchain_inputs_explicitly_counted']is True and coverage['complete69_external_full_pins']==ext and len(ext)==len({p['path']for p in ext})==coverage['external_compile_toolchain_input_count']==69 and sum(p['size_bytes']for p in ext)==coverage['external_compile_toolchain_input_bytes']==36068911,'all178 declared code inputs plus exact Source/support coverage and all69 external compile/toolchain inputs; no compiler/body read')
 for row in coverage_rows:
  p=row['full_pin'];inside=any(Path(p['path']).is_relative_to(Path(r))for r in plan['complete_joint_roots']);old=any(Path(p['path']).is_relative_to(Path(r))for r in history_roots);need(inside or old or table.get(p['path'])==p,'every exact declared compiler/support input covered by full joint/history or actual explicit ledger');current_role(p,build)
 need(ext==unique(plan['readonly_project_library_and_compiler_input_pins'])and all(not any(Path(p['path']).is_relative_to(Path(r))for r in plan['complete_joint_roots']+history_roots)and table.get(p['path'])==p for p in ext)and plan['original_Fortran_compiler_pin']in ext and plan['original_Fortran_compiler_pin']['size_bytes']==2648040,'all69 existing external roles including exact gfortran are full deduplicated explicit bytes; original metadata64 is reserve, not omitted external limit')
 retained=unique(plan['compile_and_link_input_pins']+plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']+plan['retained_B2_current_epoch_readonly_pins']+plan['selected31_current_epoch_readonly_pins']+hf['explicit_cumulative_metadata_file_pins'])
 for _ in range(2):
  for p in retained:current_role(p,build)
  for p in plan['retained_failed_v1_current7_only_pins']+plan['retained_failed_pool_archive_current7_only_pins']:need(set(p)=={'path','size_bytes','identity'},'exact failed stat3 roles only');current(p)
  need(len(plan['exact59_historical_absent_pins'])==len({p['path']for p in plan['exact59_historical_absent_pins']})==59,'only exact declared59 historical paths')
  for p in plan['exact59_historical_absent_pins']:need(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'no generic missing skip, exact retired history only')
  for p in sf['complete_source_file_pins']:full(p)
 for row in plan['original_compile_include_directory_identities']:
  p=Path(row['path']);st=p.lstat();need(stat.S_ISDIR(st.st_mode)and ids(st)==row['identity']and not any(q.is_symlink()for q in(p,*p.parents)),'original complete include directory identity/order still exact')
 need(sorted(str(p)for row in plan['original_compile_include_directory_identities']for p in Path(row['path']).glob('*.mod'))==sorted(plan['compile_module_search_directory_file_inventory']),'entire original module inventory current7, never implicit new ABI search path')
 whole=host['whole_new_output_pins'];need(len(whole)==len({p['path']for p in whole})and all(Path(p['path']).is_relative_to(OUT)for p in whole),'only exact fresh owning output fullPFs')
 first=all_output_pins(OUT);need({p['path']:p for p in first}=={p['path']:p for p in whole+[pHost]},'entire actual new owning output blind fullEOF SHA exactly twice/current7, including summary exactly once')
 need(sorted(str(q)for q in OUT.rglob('*')if q.is_file())==[p['path']for p in first],'same entire output inventory after the two blind SHA passes')
 for p in first:current(p)
 seen={p['path']:p for p in first};objects=host['actual_new_three_object_pins'];runtime=host['actual_new_Dragon_pin'];need([p['path']for p in objects]==[str(OUT/'sources/build'/n)for n in('APACKX64.o','B2PLNX64.o','KDRDRV.o')]and all(seen[p['path']]==p and p['size_bytes']>0 for p in objects)and runtime==seen[str(OUT/'sources/runtime/Dragon')]and runtime['size_bytes']>0,'three new emitted object PFs and new linked Dragon PF, no runtime execution or inherited ABI pass')
 copies=[]
 for p in plan['whole_byte_build_source_copy_pins']:
  q=seen[str(OUT/'sources'/Path(p['path']).name)];need((q['sha256'],q['size_bytes'])==(p['sha256'],p['size_bytes']),'all three Source copies wholebytes');copies.append(q)
 need(len(copies)==3 and seen[str(OUT/'runtime/run_bounded_dragon.py')]['sha256']==plan['original_bounded_Source_pin']['sha256'],'three Source copies and original bounded runner Source')
 roots=plan['complete_joint_roots'];need(len(roots)==84 and roots[-1]==str(OUT),'whole original83 plus one new buildroot84');build_resource_facts(host['resources_before'],roots);build_resource_facts(host['resources_after'],roots)
 own=sum(p['size_bytes']for p in first);need(own<32*2**20 and counted_bytes([str(PACKAGE)])<source_limit,'entire sources/objects/modules/runtime/log/watch/summary32MiB and Source8')
 need(type(host['actual_original_owned_runtime_Root_integer_exit_code'])is int and host['actual_original_owned_runtime_Root_integer_exit_code']==1 and host['actual_original_owned_runtime_compile_link_children_exit0_only']is True,'old owned-runtime Root1 preserved; only its actual compile/link child0 premises consumed')
 for k in('B_context_executed','new_B_formal13_compatible','GLOBAL_or_PROJECT_produced','online_BOOT_qualified','all_transitive_inputs_recertified','physics_qualified','AAA_qualified','ABA_admitted','goal_complete'):need(host[k]is False and stdout[k]is False,'build-only closure cannot issue Bformal/context/online/transitive/physics qualification')
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in hf['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(r))for r in roots));unlinked=unlinked_bytes();need(host['resources_before']['explicit_external_metadata_bytes']==host['resources_after']['explicit_external_metadata_bytes']==extra and joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'all current84 plus explicit external/openunlinked and reserve/free original caps including post')
 result=dict(schema='B_PLANE2_RUNTIME_COMPLETE71_BUILD_ACTUAL_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_B_PLANE2_THREE_COMPILE_COMPLETE71_LINK_ROOT0_FOUR_CHILD0_METADATA_ONLY_NO_RUNTIME_QUALIFICATION',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=0,actual_child_integer_exit_codes=childcodes,source_freeze_pin=host['source_freeze_pin'],host_freeze_pin=host['host_freeze_pin'],control_plan_pin=host['control_plan_pin'],admission_packet_pin=plan['admission_packet_pin'],actual_core_author_freeze_pin=EXPECTED_CORE_AUTHOR_FREEZE,actual_all_declared_input_coverage_metadata_pin=author['Source_static_whole_reverse_and_scope_pin'],all69_external_compile_toolchain_full_pins=ext,all69_external_compile_toolchain_bytes=36068911,all_declared_compile_toolchain_support_inputs_covered_without_payload_rehash=True,actual_CLI_pin=cliPin,actual_Source_review_pin=peerpin,actual_Source_review_tools_pin=peertools_pin,actual_four_stage_records=host['records'],actual_four_watchdog_checks=host['actual_watchdog_checks'],actual_ordered71_link_inputs=link,original_current70_ordered_input_pins=old70,whole71_inverse_restore_two_and_remove_one_equals70=True,original_other68_and_all_four_archives_current7_verified_twice=True,actual_new_three_object_pins=objects,actual_new_Dragon_pin=runtime,new_runtime_compile_link_only_not_executed=True,all_new_owning_output_blind_fullEOF_SHA_current7_twice_pins=first,whole_new_output_bytes=own,whole_three_copied_Source_pins=copies,actual_original_owned_runtime_Root_integer_exit_code=1,actual_original_owned_runtime_compile_link_children_exit0_only=True,original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,retained_all_current7_pins=plan['retained_current7_pins'],retained_archive_metadata_current7_pins=plan['retained_archive_metadata_current7_pins'],selected31_current_epoch_readonly_pins=plan['selected31_current_epoch_readonly_pins'],exact59_historical_absent_pins=plan['exact59_historical_absent_pins'],all_retained_roles_current7_verified_twice=True,complete_joint_roots=roots,original_caps=CAPS,local_Source_bound_bytes=source_limit,local_new_output_bound_bytes=32*2**20,actual_resources_before=host['resources_before'],actual_resources_after=host['resources_after'],actual_final_report_resource_check_passed=True,current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked,new_B_formal13_compatible=False,B_context_executed=False,GLOBAL_or_PROJECT_produced=False,online_BOOT_qualified=False,all_transitive_inputs_recertified=False,physics_qualified=False)
 save(result,source_limit,joint+extra+unlinked)
if __name__=='__main__':main()
