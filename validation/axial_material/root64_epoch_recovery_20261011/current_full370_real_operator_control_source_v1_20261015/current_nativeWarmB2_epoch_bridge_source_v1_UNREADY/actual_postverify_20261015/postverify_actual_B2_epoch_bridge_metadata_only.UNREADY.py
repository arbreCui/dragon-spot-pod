"""UNREADY independent metadata post for an actual B2 current-epoch blind binding.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. Only Source/small saved metadata and current7 are read. No target/gzip body, worker, lsof, native child or cleanup runs here.
Only the frozen Root bridge records and current7 are verified; no payload SHA is repeated.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(target_payload_body_opened_or_hashed=False,gzip_payload_body_opened_or_hashed=False,worker_or_guard_helpers_imported=False,worker_executed=False,lsof_executed=False,PS_executed=False,native_executed=False,compiler_executed=False,compression_repeated=False,decompression_repeated=False,numerical_executed=False,JSONL_or_array_values_decoded=False,files_deleted=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
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
def readonly_resource_facts(v,roots):
 need(v['SELF_peak_bytes']<512*2**20 and 0<=v['elapsed_seconds']<600 and v['joint']['resource_roots']==roots,'actual same original SELF512/stage600 and complete joint root topology')
 h=v['history'];j=v['joint'];sample=v['actual_PS_return']
 need(type(sample['returncode'])is int and sample['returncode']==0 and sample['stderr']==''and type(sample['stdout'])is str and sample['stdout'].strip().isdigit()and int(sample['stdout'].strip())*1024<512*2**20,'actual saved original same-PID PS return/RSS facts, PS not repeated by post')
 need(j['artifact_bytes']+v['external_metadata_bytes']+v['open_unlinked_bytes']<2*2**30 and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'actual original joint/history/cold/metadata/free caps including external/open-unlinked')
def save(report,source_limit,joint_existing=None):
 report.update(metadata_only=True,Source_author_task=AUTHOR,actual_executor_task=EXECUTOR,actual_post_not_executed_by_Source_author=True,reviewer_Source_pin=pin(Path(__file__).absolute()),helper_or_candidate_module_imported=False,Source_GEN_or_publication_executed=False,native_or_compiler_or_worker_executed=False,scientific_values_or_SQLite_or_native_XSM_or_context_body_decoded=False,original_collect_or_snapshot_pair_readback_repeated=False,historical_issue_records_modified=False,wall_seconds=time.monotonic()-START,**FALSE)
 raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20,'post control report6MiB')
 need(counted_bytes([str(PACKAGE)])+len(raw)<source_limit,'entire Source/metadata bound including new post')
 if joint_existing is not None:need(joint_existing+len(raw)<2*2**30,'entire current cumulative2GiB including post')
 q=BASE/'REVIEW.json'
 with q.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 budget();print(json.dumps(dict(status=report['status'],review_pin=pin(q))),flush=True)
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_nativeWarmB2_epoch_bridge_source_v1_UNREADY/AUTHOR_SOURCE_ONLY_FREEZE.json', 'sha256': '4c1799708c49bf99fa439a3a91403605407fdeabf475eeccdd489c4007921e98', 'size_bytes': 3604, 'identity': [16777229, 50880150, 33188, 1, 3604, 1792064682428901038, 1792064682428901038]}
def bridge_resources(v):
 need(type(v['history_artifact_bytes'])is int and type(v['complete_joint_bytes'])is int and type(v['explicit_external_metadata_bytes'])is int and type(v['own_open_unlinked_bytes'])is int and v['SELF_peak_bytes']<512*2**20 and 0<=v['elapsed_seconds']<600 and v['selected_old_readonly_roles_covered_in_history']is True,'actual saved bridge SELF512/stage600 and original history coverage')
 need(v['history_artifact_bytes']+20971764748+64*2**20<96*2**30 and v['complete_joint_bytes']+v['explicit_external_metadata_bytes']+v['own_open_unlinked_bytes']<2*2**30 and v['disk_free_bytes']-20971764748-2*2**30>=8*2**30 and type(v['history_root_count'])is int and v['history_root_count']>0,'actual original history96/joint2/cold/meta/free8 preserved without reclassifying large readonly inputs')
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in('Root-tools-pin','bridge-report-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();need(a.executor_task_name==EXECUTOR and a.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'same exact independent executor, immutable one metadata post')
 pt=json.loads(a.Root_tools_pin);pr=json.loads(a.bridge_report_pin);tools=meta(pt);terminal=tools['actual_terminal_return'];report=None if pr is None else meta(pr)
 need(tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int and type(terminal['exit_code'])is int and terminal['exit_code']==tools['original_integer_exit_code']and terminal.get('session_id')is None and tools['actual_execution_permission_mode']=='require_escalated'and tools['actual_retried']is False,'genuine observed closed Root integer and original permission/no retry; no child inference')
 author=meta(EXPECTED_CORE_AUTHOR_FREEZE);ps=author['source_pin'];pb=author['binding_pin'];b=meta(pb);code=tools['original_integer_exit_code'];source_limit=16*2**20
 need(author['source_only']is True and author['author_STOP_WRITES']is True and b['schema']=='SOURCE_ONLY_NATIVE_WARM_B2_CURRENT_EPOCH_BRIDGE_BINDING_V1'and b['actual_old_B2_closure_roles_bound']is True and b['new_owning_data_root_created']is False and b['future_current_epoch_bridge_report_pin']is None,'same frozen Source and genuine old closure binding; future NULL never promoted')
 if code!=0:
  result=dict(schema='CURRENT_B2_EPOCH_BRIDGE_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_Root_tools_pin=pt,actual_bridge_report_pin=pr,actual_Root_integer_exit_code=code,actual_child_integer_exit_code=None,actual_saved_report_metadata=report,Root_only_bridge_closed0_inferred=False,source_pin=ps,binding_pin=pb)
  save(result,source_limit);return
 need(report is not None,'genuine Root0 bridge requires emitted report PF');genuine(tools,'actual_terminal_return',pr,'report_pin');stdout=json.loads(terminal['output'].strip().splitlines()[-1])
 need(pr['path']==str(PACKAGE/'ROOT_CURRENT_EPOCH_B2_BLIND_BINDING_REPORT.json')and report['schema']=='ROOT_NATIVE_WARM_B2_CURRENT_EPOCH_BLIND_FULLFILE_BINDING_REPORT_V1'and report['status']=='PASS_B2_SELECTED_READONLY_ROLES_CURRENT_EPOCH_BLIND_SHA_ONLY'and report['failure']is None and report['source_pin']==ps and report['binding_pin']==pb and report['original_caps']==b['original_caps']==CAPS and report['children_started']==0 and type(report['children_started'])is int and report['final_report_resource_check_passed']is True,'same actual Root-only selected bridge0/Source/binding/caps/final resource closure, no data child')
 need(stdout['selected_roles_only']is True and stdout['all4790_transitive_recertified']is False and stdout['lineage_qualified']is False and stdout['online_BOOT_qualified']is False,'actual Root stdout scope remains selected blind files only')
 cli_pin=pin(PACKAGE/'ROOT_REVIEWED_FINAL_CLI.json');cli=meta(cli_pin);template=meta(author['Root_CLI_template_pin']);argv=cli['argv'];need(cli['schema']=='ROOT_B2_CURRENT_EPOCH_BRIDGE_REVIEWED_FINAL_CLI_V1'and tools['exact_executed_command']==cli['command']and shlex.split(cli['command'])==argv and len(argv)==20 and argv[:16]==template['fixed_argv_prefix']and cli['required_permission']=='require_escalated'and argv[16]=='--review-pin'and argv[18]=='--review-tools-pin','genuine complete original20 Root argv and exact CLI.command string; no rebuilt environment')
 peerpin=json.loads(argv[17]);peertools_pin=json.loads(argv[19]);need(peerpin==cli['independent_Source_review_pin']==report['independent_Source_review_pin']and peertools_pin==cli['independent_Source_review_tools_pin'],'same actual Root Source review roles')
 peer=meta(peerpin);peertools=meta(peertools_pin);genuine(peertools,'actual_review_return',peerpin,'review_pin');need(peer['status']=='PASS_SOURCE_ONLY_B2_CURRENT_EPOCH_BLIND_BINDING_V1'and peer['failure']is None and peer['source_only']is True and peer['source_pin']==ps and peer['binding_pin']==pb,'genuine independent Source review0 of this exact Source/binding')
 full(ps);full(ps)
 claimpin=pin(PACKAGE/'ROOT_CURRENT_EPOCH_BINDING_ONCE_CLAIM.json');claim=meta(claimpin);need(claim['schema']=='ROOT_B2_EPOCH_BRIDGE_ONCE_CLAIM_V1'and claim['claim_before_helpers_or_payload_IO']is True and claim['argv']==argv[11:]and type(claim['PID'])is int and claim['PID']>0,'real Root-only once claim, created before helper or payload IO')
 old=meta(b['old_Host_current_metadata_pin']);oldraw=meta(b['old_true_tool_returns_current_metadata_pin']);oldpeer=meta(b['old_independent_review_current_metadata_pin']);oldterminal=oldraw['B_v3_terminal'];oldpost=oldraw['B_v3_independent_review']
 need(type(oldterminal['exit_code'])is int and oldterminal['exit_code']==0 and oldterminal.get('session_id')is None and oldterminal['chunk_id']=='b77b5f'and type(oldpost['exit_code'])is int and oldpost['exit_code']==0 and oldpost.get('session_id')is None and oldpost['chunk_id']=='fe36fd','preserve genuine old typed terminal0 and independent review0 raw evidence, no fabricated canonical alias')
 result=json.loads(oldterminal['output'].strip().splitlines()[-1]);witness=json.loads(oldpost['output'].strip().splitlines()[-1]);need(result==dict(status='ACTUAL_SINGLE_PLANE2_E0_WARM_B_NATIVE_PRODUCER_CLOSED0_ONLY',failure=None,records=4)and old['schema']=='ACTUAL_CURRENT_SINGLE_PLANE_WARM_B_NATIVE_PRODUCER_ROOT_V1'and old['status']==result['status']and old['failure']is None and len(old['records'])==4 and all(r['status']=='PASS'for r in old['records']),'original B2 warm producer four-stage0 facts retained')
 need(witness['actual_report_pin']==oldpeer['actual_report_pin']==b['historical_old_Host_full_pin']and witness['terminal']==oldpeer['full_native_terminal']==old['actual_native_terminal']and oldpeer['schema']=='ROOT_INDEPENDENT_CURRENT_B_V3_FULLFILE_REVIEW_V1'and oldpeer['status']==witness['status']=='PASS_SINGLE_PLANE_B_ONLY'and oldpeer['output_pin']==old['actual_output_pin'],'same historical full Host/output/native terminal and real independent review0')
 oldhp=b['historical_old_Host_full_pin'];newhp=b['old_Host_current_metadata_pin'];need(oldhp['path']==newhp['path']and oldhp['sha256']==newhp['sha256']and oldhp['size_bytes']==newhp['size_bytes']and oldhp['identity'][0]==16777234 and newhp['identity'][0]==16777229 and oldhp['identity'][1:]==newhp['identity'][1:],'unchanged historical Host fullPF retained; only separate metadata device epoch changed')
 pairs=report['ordered_role_pairs'];specs=b['ordered_role_specs'];need(len(pairs)==len(specs)==len({p['role']for p in pairs})==9,'all exact nine selected roles, no transitive4790 recertification')
 recorded=old['owned_runtime_pins']+[old['actual_output_pin'],old['actual_SALT_binary_track_pin']];total=0;by={}
 for row,spec in zip(pairs,specs):
  oldpin=row['historical_full_pin'];newpin=row['current_epoch_full_pin'];need(row['role']==spec['role']and oldpin==spec['historical_full_pin']and oldpin in recorded and row['blind_complete_SHA_and_length_equal']is True and row['before_open_EOF_after_current7_stable']is True and oldpin['path']==newpin['path']and oldpin['sha256']==newpin['sha256']and oldpin['size_bytes']==newpin['size_bytes']and oldpin['identity'][0]==16777234 and newpin['identity'][0]==16777229 and oldpin['identity'][1:]==newpin['identity'][1:]and newpin['identity']==spec['expected_start_current7'],'recorded whole blind SHA/length and all six nondevice fields equal; original oldPF preserved, post hashes no payload')
  current(newpin);total+=newpin['size_bytes'];by[row['role']]=row
 need(total==325123030 and by['B2_archive']['historical_full_pin']==old['actual_output_pin']and by['B2_track']['historical_full_pin']==old['actual_SALT_binary_track_pin']and report['current_epoch_B2_archive_pin']==by['B2_archive']['current_epoch_full_pin'],'complete selected role byte total and exact original archive/track shortcut roles')
 b63=b['historical_current_B63_original_m_pin'];material=by['B2_owned_material']['current_epoch_full_pin'];need(material['sha256']==b63['sha256']and material['size_bytes']==b63['size_bytes']and report['blind_verified_B2_material_equals_recorded_B63_m_SHA_length']is True and report['current_B63_original_m_body_or_stat_opened']is False,'real Root-blind material SHA/length equals saved B63 original m, historical absent path never opened or stat by post')
 member=meta(b['actual_B63_member0_report_pin']);membertools=meta(b['actual_B63_member0_tools_pin']);memberpost=meta(b['actual_B63_member0_post_pin']);memberpt=meta(b['actual_B63_member0_post_tools_pin']);genuine(membertools,'actual_terminal_return',b['actual_B63_member0_report_pin'],'report_pin');genuine(memberpt,'actual_review_return',b['actual_B63_member0_post_pin'],'review_pin')
 need(member['original_member0_saved_full_pin']==memberpost['original_member0_saved_full_pin']==b63 and member['streamed_complete_member0_verified']is True and member['streamed_decompressed_SHA']==b63['sha256']and member['streamed_decompressed_length']==b63['size_bytes']and memberpost['actual_member0_Root_report_pin']==b['actual_B63_member0_report_pin']and memberpost['actual_Root_tools_pin']==b['actual_B63_member0_tools_pin']and memberpost['Root_actual_complete_member0_stream_verified']is True,'genuine separate B63 member0 full recovery0/post0 record; no gzip replay or original m path probe')
 for record in old['records']:
  wp=next(p for p in b['old_watchdog_current_metadata_pins']if Path(p['path']).name==Path(record['label']+'.watchdog.json').name);w=meta(wp)
  need(w['command']==record['command']and type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None and w['rss_cap_mib']==512 and w['own_child_only']is True and w['liveness_group_cleanup']is True and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600,'four original saved watchdog0/RSS/wall/liveness closures unchanged')
 rb=b['original_resource_binding'];roots=b['complete_joint_roots'];latest=meta(b['latest_complete_plan_pin']);need(report['complete_joint_roots']==rb['complete_joint_roots']==roots==latest['complete_joint_roots']and len(roots)==75 and len(roots)==len(set(roots))and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)and b['new_Source_counted_in_existing_FTOP75']is True and any(PACKAGE.is_relative_to(Path(x))for x in roots),'whole then-latest75 prefix retained without new data root or input-body fresh reclassification')
 rows=rb['explicit_cumulative_metadata_file_pins']+[pb,ps,peerpin,peertools_pin];expected={}
 for p in rows:need(p['path']not in expected or expected[p['path']]==p,'one completePF per metadata path');expected[p['path']]=p
 need(report['explicit_cumulative_metadata_file_pins']==list(expected.values())and b63['path']not in expected and not{r['current_epoch_full_pin']['path']for r in pairs}&set(expected),'complete actual explicitmetadata union includes old Host/terminal/bindings/proofs; large cold readonly bodies are not ordinary metadata')
 build=meta(rb['original_guard_build_plan_pin'])
 for _ in range(2):
  for p in report['explicit_cumulative_metadata_file_pins']:current_role(p,build)
  for row in pairs:current(row['current_epoch_full_pin'])
 need(report['selected_roles_only_not_4790_transitive_recertification']is True and report['original_4790_transitive_current_recertification_performed']is False and report['Root_SELF_peak_bytes']<512*2**20 and 0<=report['Root_elapsed_seconds']<600 and len(report['resources'])>=2,'only selected current epoch record binding, original Root SELF/stage bound and real resource samples')
 last=-1
 for snap in report['resources']:bridge_resources(snap);need(snap['elapsed_seconds']>=last,'actual saved resource checkpoints in original-start order');last=snap['elapsed_seconds']
 for k in('complete_B2_archive_MICROLIB2_MACROLIB_physical_tree_comparison_executed','actual_lineage_qualified','online_BOOT_qualified','physics_qualified','AAA_qualified','ABA_admitted','goal_complete','decoder_executed','native_executed','files_deleted'):need(report[k]is False,'blind binding cannot issue extraction/decoder/lineage/online/physics/goal qualifications')
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in report['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(root))for root in roots));unlinked=unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current full75/cold/free reserves include Source and post metadata plus real explicitexternal/open-unlinked')
 result=dict(schema='CURRENT_NATIVE_WARM_B2_EPOCH_BRIDGE_ACTUAL_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_B2_SELECTED9_EPOCH_ROOT0_CURRENT7_METADATA_ONLY_NO_PAYLOAD_REPLAY',failure=None,actual_Root_tools_pin=pt,actual_bridge_report_pin=pr,actual_Root_integer_exit_code=code,actual_child_integer_exit_code=None,actual_children_started=report['children_started'],source_pin=ps,binding_pin=pb,actual_Source_author_freeze_pin=EXPECTED_CORE_AUTHOR_FREEZE,actual_Source_review_pin=peerpin,actual_Source_review_tools_pin=peertools_pin,actual_reviewable_CLI_pin=cli_pin,actual_Root_claim_pin=claimpin,ordered_role_pairs=pairs,actual_selected_role_count=len(pairs),actual_selected_blind_verified_bytes=total,current_epoch_B2_archive_pin=report['current_epoch_B2_archive_pin'],historical_old_Host_full_pin=oldhp,old_Host_current_metadata_pin=newhp,old_true_tool_returns_current_metadata_pin=b['old_true_tool_returns_current_metadata_pin'],old_independent_review_current_metadata_pin=b['old_independent_review_current_metadata_pin'],old_genuine_Root_terminal_integer_exit_code=oldterminal['exit_code'],old_genuine_independent_review_integer_exit_code=oldpost['exit_code'],old_historical_fullPFs_and_all_nondevice_fields_preserved=True,all9_current_epoch_roles_current7_verified_twice=True,Root_recorded_blind_fullEOF_SHA_and_length_proofs_verified_without_payload_replay=True,historical_B63_original_m_full_pin=b63,B63_original_m_path_probe_performed=False,actual_B2_material_matches_recorded_B63_original_m_SHA_length=True,actual_B63_member0_recovery_report_pin=b['actual_B63_member0_report_pin'],actual_B63_member0_recovery_post_pin=b['actual_B63_member0_post_pin'],explicit_cumulative_metadata_file_pins=report['explicit_cumulative_metadata_file_pins'],complete_joint_roots=roots,original_caps=CAPS,actual_Root_resource_snapshots=report['resources'],actual_final_report_resource_check_passed=report['final_report_resource_check_passed'],current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked,selected_roles_only_not_4790_transitive_recertification=True,original_4790_transitive_current_recertification_performed=False,physical_tree_or_lineage_comparison_executed=False,actual_lineage_qualified=False,online_BOOT_qualified=False,payload_SHA_repeated_by_post=False,decoder_executed=False)
 save(result,source_limit,joint+extra+unlinked)
if __name__=='__main__':main()
