"""Independent Source/small metadata/current7 review. Never execute candidate."""
import ast,hashlib,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
AUTHOR_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_nativeWarmB2_epoch_bridge_source_v1_UNREADY/AUTHOR_SOURCE_ONLY_FREEZE.json', 'sha256': '4c1799708c49bf99fa439a3a91403605407fdeabf475eeccdd489c4007921e98', 'size_bytes': 3604, 'identity': [16777229, 50880150, 33188, 1, 3604, 1792064682428901038, 1792064682428901038]}
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();assert q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and ids(s)==p['identity']and s.st_size==p['size_bytes'];return q

def full(p):
 q=current(p);assert p['size_bytes']<8*2**20;raw=q.read_bytes();assert hashlib.sha256(raw).hexdigest()==p['sha256'];current(p);return raw

def read(p):
 v=json.loads(full(p));full(p);return v

def pin(p):
 s=p.stat();raw=p.read_bytes();return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=s.st_size,identity=ids(s))

def true0(p,key,field,want):
 d=read(p);r=d[key];assert d['observed_closed']is True and type(d['original_integer_exit_code'])is int and d['original_integer_exit_code']==0 and type(r['exit_code'])is int and r['exit_code']==0 and r.get('session_id')is None and json.loads(r['output'].splitlines()[-1])[field]==want

a=read(AUTHOR_PIN);assert a['source_only']is True and a['author_STOP_WRITES']is True
ps=a['source_pin'];pb=a['binding_pin'];rawSource=full(ps);full(ps);text=rawSource.decode();tree=ast.parse(text);b=read(pb);cli=read(a['Root_CLI_template_pin']);lineage=read(a['lineage_role_audit_pin'])
assert ps['sha256']=='2e250212953d69ab925e7f8d3e57d87787727d384891d24fd090443db323a622'and b['schema']=='SOURCE_ONLY_NATIVE_WARM_B2_CURRENT_EPOCH_BRIDGE_BINDING_V1'and b['actual_old_B2_closure_roles_bound']is True
assert a['role_count']==9 and a['complete_root_count']==75 and a['original_caps']==b['original_caps']==CAPS
assert b['future_current_epoch_bridge_report_pin']is b['actual_bridge_Root_tools_pin']is b['actual_bridge_post_pin']is b['actual_bridge_post_tools_pin']is None
assert b['new_owning_data_root_created']is False and b['all4790_transitive_recertification_claimed']is False and b['author_payload_or_Generator_or_helper_or_native_executed']is False
roots=b['complete_joint_roots'];latest=read(b['latest_complete_plan_pin']);assert roots==latest['complete_joint_roots']and len(roots)==len(set(roots))==75 and any(Path(ps['path']).is_relative_to(Path(r))for r in roots)
rb=b['original_resource_binding'];assert rb['complete_joint_roots']==roots and rb['planned_actual_output_root'] in roots and rb['planned_actual_output_root']=='/Users/wen/spot/validation/artifacts/axial-material-current-B4-complete-product-lossless-archive-20261015-v1'
common=full(b['frozen_original_B4_common_Source_pin']).decode();full(b['frozen_original_B4_common_Source_pin']);assert b['frozen_original_B4_common_Source_pin']==a['resource_original_B4_common_whole_pin']and 'class Resources:'in common and 'history_roots([str(self.out)],ART)'in common
assert text.index('fd=os.open(claim,')<text.index('spec.loader.exec_module(c)')<text.index('resources=c.Resources(')<text.index('checkpoint(True);pairs=[]')<text.index('while block:=os.read(fd,CHUNK):')
assert 'CHUNK=2**20'in text and 'checkpoint();h.update(block)'in text and 'last=time.monotonic()'in text and 'time.monotonic()-last>=5'in text and 'current_B63_original_m_body_or_stat_opened=False'in text
imports={n.names[0].name.split('.')[0] for n in ast.walk(tree)if isinstance(n,ast.Import)}|{n.module.split('.')[0]for n in ast.walk(tree)if isinstance(n,ast.ImportFrom)}
assert imports<={'argparse','hashlib','importlib','json','os','resource','stat','sys','time','pathlib'}and not any(x in text for x in('subprocess','os.unlink(','os.remove(','sqlite3','gzip.open('))
old=read(b['old_Host_current_metadata_pin']);oldraw=read(b['old_true_tool_returns_current_metadata_pin']);oldpeer=read(b['old_independent_review_current_metadata_pin'])
terminal=oldraw['B_v3_terminal'];witness=oldraw['B_v3_independent_review'];assert terminal['chunk_id']=='b77b5f'and witness['chunk_id']=='fe36fd'and type(terminal['exit_code'])is int and terminal['exit_code']==0 and type(witness['exit_code'])is int and witness['exit_code']==0 and terminal.get('session_id')is None and witness.get('session_id')is None
assert json.loads(terminal['output'].splitlines()[-1])==dict(status='ACTUAL_SINGLE_PLANE2_E0_WARM_B_NATIVE_PRODUCER_CLOSED0_ONLY',failure=None,records=4)
w=json.loads(witness['output'].splitlines()[-1]);assert w['actual_report_pin']==oldpeer['actual_report_pin']==b['historical_old_Host_full_pin']and w['terminal']==oldpeer['full_native_terminal']==old['actual_native_terminal']and oldpeer['output_pin']==old['actual_output_pin']and oldpeer['status']==w['status']=='PASS_SINGLE_PLANE_B_ONLY'
h=b['historical_old_Host_full_pin'];cp=b['old_Host_current_metadata_pin'];assert h['sha256']==cp['sha256']=='48d3704a6bd7e6ac451bc81997ca1de46a26f9ae1552ced084ebdc6f332f2014'and h['size_bytes']==cp['size_bytes']==3564904 and h['identity'][1:]==cp['identity'][1:]and h['identity'][0]==16777234 and cp['identity'][0]==16777229
roles=b['ordered_role_specs'];assert [r['role']for r in roles]==['B2_archive','B2_owned_material','B2_owned_seed','B2_track','B2_owned_geometry','B2_runtime_Dragon','B2_owned_deck','B2_bounded','B2_native_readback_tool']
by={r['role']:r['historical_full_pin']for r in roles};assert by['B2_archive']==old['actual_output_pin']and by['B2_track']==old['actual_SALT_binary_track_pin']
for role in roles:
 p=role['historical_full_pin'];q=Path(p['path']);s=q.lstat();assert ids(s)==role['expected_start_current7']and ids(s)[1:]==p['identity'][1:]and s.st_dev==16777229 and p['identity'][0]==16777234 and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid()and role['current_epoch_full_pin']is None and role['scope']=='EXISTING_ART_HISTORY_READONLY_NOT_NEW_FRESH_DATA'
 assert q.is_relative_to(Path(cp['path']).parent)and not any(q.is_relative_to(Path(r))for r in roots)
 assert p in old['owned_runtime_pins']+[old['actual_output_pin'],old['actual_SALT_binary_track_pin']]
for record in old['records']:
 assert record['status']=='PASS';wanted=Path(cp['path']).parent/(record['label']+'.watchdog.json');pins=[p for p in b['old_watchdog_current_metadata_pins']if p['path']==str(wanted)];assert len(pins)==1;wd=read(pins[0]);assert wd['command']==record['command']and type(wd['returncode'])is int and wd['returncode']==0 and wd['limit_failure']is None and wd['rss_cap_mib']==512 and wd['own_child_only']is True and wd['liveness_group_cleanup']is True and 0<=wd['sampled_peak_rss_mib']<512 and 0<wd['elapsed_seconds']<wd['wall_cap_seconds']<=600
m=read(b['actual_B63_member0_report_pin']);mp=read(b['actual_B63_member0_post_pin']);true0(b['actual_B63_member0_tools_pin'],'actual_terminal_return','report_pin',b['actual_B63_member0_report_pin']);true0(b['actual_B63_member0_post_tools_pin'],'actual_review_return','review_pin',b['actual_B63_member0_post_pin'])
historic=b['historical_current_B63_original_m_pin'];assert historic==m['original_member0_saved_full_pin']and m['streamed_complete_member0_verified']is True and by['B2_owned_material']['sha256']==historic['sha256']==m['streamed_decompressed_SHA']and by['B2_owned_material']['size_bytes']==historic['size_bytes']==m['streamed_decompressed_length']and mp['actual_member0_Root_report_pin']==b['actual_B63_member0_report_pin']and mp['Root_actual_complete_member0_stream_verified']is True
assert historic['path']not in{p['path']for p in rb['explicit_cumulative_metadata_file_pins']}
for p in rb['explicit_cumulative_metadata_file_pins']:current(p)
assert cli['source_pin']==ps and cli['binding_pin']==pb and cli['actual_Source_review_pin']is cli['actual_Source_review_tools_pin']is None and cli['actual_execution_permission_mode_required']=='require_escalated'and cli['bridge_executed']is False
prefix=cli['fixed_argv_prefix'];assert len(prefix)==16 and prefix[11]==ps['path']and prefix[12]=='--binding-pin'and json.loads(prefix[13])==pb and prefix[14]=='--source-pin'and json.loads(prefix[15])==ps
for p in(ps,pb,AUTHOR_PIN):full(p);full(p)
report=dict(status='PASS_SOURCE_ONLY_B2_CURRENT_EPOCH_BLIND_BINDING_V1',schema='INDEPENDENT_B2_CURRENT_EPOCH_BRIDGE_SOURCE_ONLY_REVIEW_V1',failure=None,source_only=True,source_pin=ps,binding_pin=pb,author_freeze_pin=AUTHOR_PIN,lineage_role_audit_pin=a['lineage_role_audit_pin'],Root_CLI_template_pin=a['Root_CLI_template_pin'],old_genuine_Root_terminal_chunk='b77b5f',old_genuine_independent_review_chunk='fe36fd',old_Root_and_independent_review_integer_codes=[0,0],selected_historical_role_count=len(roles),selected_historical_readonly_bytes=sum(r['historical_full_pin']['size_bytes']for r in roles),selected_roles_current7_only_verified=True,old_device34_preserved_new29_separate_currentPF_still_NULL=True,all75_dynamic_joint_roots_preserved=True,original_caps=CAPS,original_full_history_cold_joint_guard_source_frozen=True,Root_actual_fresh_history_and_joint_checks_required=True,claim_precedes_helper_and_open_unlinked_check=True,one_MiB_blind_SHA_with_light_and_throttled_full_checks=True,new_owning_data_root_created=False,B63_original_retired_m_never_statted_or_opened=True,B63_separate_member0_restore_Root0_post0_chain_bound=True,all4790_transitive_recertified=False,lineage_qualified=False,actual_bridge_executed=False,actual_bridge_Root_integer_exit_code=None,large_payload_opened_or_SHA_recomputed=False,compiler_native_worker_helper_or_generator_executed=False,files_deleted=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
p=BASE/'REVIEW.json';assert not p.exists();p.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status=report['status'],review_pin=pin(p))))
