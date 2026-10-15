"""Root-only selected historical B2 roles: blind EOF SHA and a separate current7.
No decoding, original report changes, producer execution, or scientific admission.
"""
import argparse,hashlib,importlib.util,json,os,resource,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent
CHUNK=2**20
def need(v,m):
 if v is not True:raise RuntimeError(m)
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid()and ids(s)==p['identity']and s.st_size==p['size_bytes'],'literal owned metadata/Source exact current7');return q
def small(p):
 q=current(p);need(p['size_bytes']<8*2**20,'metadata/Source below8MiB');raw=q.read_bytes();need(len(raw)==p['size_bytes']and hashlib.sha256(raw).hexdigest()==p['sha256'],'whole small metadata/Source SHA');current(p);return raw
def meta(p):return json.loads(small(p))
def true0(p,key,field,want):
 d=meta(p);r=d[key];need(d['observed_closed']is True and type(d['original_integer_exit_code'])is int and d['original_integer_exit_code']==0 and type(r['exit_code'])is int and r['exit_code']==0 and 'session_id'not in r and json.loads(r['output'].splitlines()[-1])[field]==want,'actual typed closed0 exact metadata PF');return d
def main():
 started=time.monotonic();ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('binding','source','review','review-tools'):ap.add_argument('--'+role+'-pin',required=True)
 a=ap.parse_args()
 def selfcheck():
  peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
  need(peak<512*2**20 and time.monotonic()-started<600,'Root SELF512/stage600 from original start within whole1800')
  total=0
  for q in BASE.rglob('*'):
   s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'own Source has no alias')
   if stat.S_ISREG(s.st_mode):total+=s.st_size
  need(total<16*2**20,'entire new bridge Source/metadata16MiB');return peak
 selfcheck();claim=BASE/'ROOT_CURRENT_EPOCH_BINDING_ONCE_CLAIM.json'
 fd=os.open(claim,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 with os.fdopen(fd,'w')as f:json.dump(dict(schema='ROOT_B2_EPOCH_BRIDGE_ONCE_CLAIM_V1',PID=os.getpid(),started=started,claim_before_helpers_or_payload_IO=True,argv=sys.argv),f);f.write('\n');f.flush();os.fsync(f.fileno())
 pb=json.loads(a.binding_pin);ps=json.loads(a.source_pin);pr=json.loads(a.review_pin);pt=json.loads(a.review_tools_pin)
 need(ps['path']==str(Path(__file__).absolute()),'same frozen executing Source');small(ps);b=meta(pb);peer=meta(pr);tools=meta(pt);t=tools['actual_review_return']
 need(tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int and tools['original_integer_exit_code']==0 and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and json.loads(t['output'].splitlines()[-1])['review_pin']==pr,'independent actual Source review typed0')
 need(peer['status']=='PASS_SOURCE_ONLY_B2_CURRENT_EPOCH_BLIND_BINDING_V1'and peer['failure']is None and peer['source_only']is True and peer['source_pin']==ps and peer['binding_pin']==pb,'same exact reviewed Source/binding, no business PASS inferred')
 need(b['schema']=='SOURCE_ONLY_NATIVE_WARM_B2_CURRENT_EPOCH_BRIDGE_BINDING_V1'and b['actual_old_B2_closure_roles_bound']is True and b['new_owning_data_root_created']is False and b['future_current_epoch_bridge_report_pin']is None,'Source binding; future actual bridge not minted')
 need(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')),'unoptimized unprofiled original thread1')
 old=meta(b['old_Host_current_metadata_pin']);raw=meta(b['old_true_tool_returns_current_metadata_pin']);review=meta(b['old_independent_review_current_metadata_pin']);terminal=raw['B_v3_terminal'];independent=raw['B_v3_independent_review']
 need(type(terminal['exit_code'])is int and terminal['exit_code']==0 and 'session_id'not in terminal and terminal['chunk_id']=='b77b5f'and type(independent['exit_code'])is int and independent['exit_code']==0 and 'session_id'not in independent and independent['chunk_id']=='fe36fd','genuine original B_v3 terminal0 and independent review0 raw objects; no synthetic canonical fields')
 result=json.loads(terminal['output'].splitlines()[-1]);witness=json.loads(independent['output'].splitlines()[-1])
 need(result==dict(status='ACTUAL_SINGLE_PLANE2_E0_WARM_B_NATIVE_PRODUCER_CLOSED0_ONLY',failure=None,records=4)and old['schema']=='ACTUAL_CURRENT_SINGLE_PLANE_WARM_B_NATIVE_PRODUCER_ROOT_V1'and old['status']==result['status']and old['failure']is None and len(old['records'])==4 and all(r['status']=='PASS'for r in old['records']),'old actual independent plane2/e0 producer four complete stages')
 need(witness['actual_report_pin']==review['actual_report_pin']==b['historical_old_Host_full_pin']and witness['terminal']==review['full_native_terminal']==old['actual_native_terminal']and review['schema']=='ROOT_INDEPENDENT_CURRENT_B_V3_FULLFILE_REVIEW_V1'and review['status']==witness['status']=='PASS_SINGLE_PLANE_B_ONLY'and review['output_pin']==old['actual_output_pin'],'old independent report exactly binds unchanged historical Host/output/terminal')
 oldhp=b['historical_old_Host_full_pin'];newhp=b['old_Host_current_metadata_pin'];need(newhp['sha256']==oldhp['sha256']and newhp['size_bytes']==oldhp['size_bytes']and newhp['identity'][1:]==oldhp['identity'][1:],'historical Host bytes and six nondevice fields preserved; original report not edited')
 recorded=old['owned_runtime_pins']+[old['actual_output_pin'],old['actual_SALT_binary_track_pin']]
 need(len(b['ordered_role_specs'])==9 and all(row['historical_full_pin']in recorded for row in b['ordered_role_specs']),'exact nine direct owned input/runtime/output roles from genuine old producer; no transitive recertification')
 common=b['frozen_original_B4_common_Source_pin'];small(common);spec=importlib.util.spec_from_file_location('B2_epoch_original_frozen_resource_support',common['path']);c=importlib.util.module_from_spec(spec);sys.modules[spec.name]=c;spec.loader.exec_module(c)
 rb=dict(b['original_resource_binding']);need(rb['complete_joint_roots']==b['complete_joint_roots']and len(rb['complete_joint_roots'])==75 and b['original_caps']==c.CAPS and c.CAPS['stage_seconds']==600,'entire latest75 roots and unchanged original caps')
 rows=rb['explicit_cumulative_metadata_file_pins']+[pb,ps,pr,pt];by={}
 for p in rows:need(p['path']not in by or by[p['path']]==p,'one exact metadata PF per path');by[p['path']]=p
 rb['explicit_cumulative_metadata_file_pins']=list(by.values());resources=c.Resources(rb,started,600);last=0.0;snapshots=[]
 def checkpoint(force=False):
  nonlocal last
  selfcheck();resources.light()
  if force or time.monotonic()-last>=5:
   state=resources.check();history=state['original_history']['resource_roots']
   need(all(any(Path(row['historical_full_pin']['path']).is_relative_to(Path(r))for r in history)for row in b['ordered_role_specs']),'every selected old readonly role is covered by original history scope, not silently added to fresh data roots')
   snapshots.append(dict(history_artifact_bytes=state['original_history']['artifact_bytes'],history_root_count=len(history),complete_joint_bytes=state['complete_joint']['artifact_bytes'],explicit_external_metadata_bytes=state['explicit_external_metadata_bytes'],own_open_unlinked_bytes=state['own_open_unlinked_bytes'],disk_free_bytes=state['complete_joint']['disk_free_bytes'],SELF_peak_bytes=state['SELF_peak_bytes'],elapsed_seconds=state['original_elapsed_seconds'],selected_old_readonly_roles_covered_in_history=True))
   last=time.monotonic()
 checkpoint(True);pairs=[]
 for row in b['ordered_role_specs']:
  oldpin=row['historical_full_pin'];q=Path(oldpin['path']);s=q.lstat();before=ids(s)
  need(before==row['expected_start_current7']and before[1:]==oldpin['identity'][1:]and oldpin['identity'][0]==16777234 and before[0]==16777229 and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid()and not any(x.is_symlink()for x in(q,*q.parents))and s.st_size==oldpin['size_bytes'],'only explicit device epoch changed; all six other historical fields fixed, old PF unchanged')
  h=hashlib.sha256();n=0;fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW)
  try:
   need(ids(os.fstat(fd))==before,'opened current7')
   while block:=os.read(fd,CHUNK):checkpoint();h.update(block);n+=len(block)
   need(ids(os.fstat(fd))==before,'complete EOF stable current7')
  finally:os.close(fd)
  need(ids(q.lstat())==before and n==oldpin['size_bytes']and h.hexdigest()==oldpin['sha256'],'blind complete SHA/length same saved original; no decoding')
  pairs.append(dict(role=row['role'],historical_full_pin=oldpin,current_epoch_full_pin=dict(path=oldpin['path'],sha256=h.hexdigest(),size_bytes=n,identity=before),blind_complete_SHA_and_length_equal=True,before_open_EOF_after_current7_stable=True))
 checkpoint(True);rolemap={r['role']:r for r in pairs};need(len(rolemap)==len(pairs),'unique selected role names')
 need(rolemap['B2_archive']['historical_full_pin']==old['actual_output_pin']and rolemap['B2_track']['historical_full_pin']==old['actual_SALT_binary_track_pin'],'genuine producer exact output/track roles')
 material=rolemap['B2_owned_material']['current_epoch_full_pin'];b63=b['historical_current_B63_original_m_pin'];need(material['sha256']==b63['sha256']and material['size_bytes']==b63['size_bytes'],'current blindly verified B2 material matches B63 recorded original m bytes; B63 absent original not opened/stat')
 member=meta(b['actual_B63_member0_report_pin']);need(member['original_member0_saved_full_pin']==b63 and member['streamed_complete_member0_verified']is True and member['streamed_decompressed_SHA']==b63['sha256']and member['streamed_decompressed_length']==b63['size_bytes'],'separate genuine archived B63 restoration evidence; not repeated by this bridge')
 true0(b['actual_B63_member0_tools_pin'],'actual_terminal_return','report_pin',b['actual_B63_member0_report_pin']);true0(b['actual_B63_member0_post_tools_pin'],'actual_review_return','review_pin',b['actual_B63_member0_post_pin']);memberpost=meta(b['actual_B63_member0_post_pin']);need(memberpost['actual_member0_Root_report_pin']==b['actual_B63_member0_report_pin']and memberpost['actual_Root_tools_pin']==b['actual_B63_member0_tools_pin']and memberpost['Root_actual_complete_member0_stream_verified']is True,'same actual independently postverified archived B63 original-m recovery')
 for record in old['records']:
  label=record['label'];wp=next(p for p in b['old_watchdog_current_metadata_pins']if Path(p['path']).name==Path(label+'.watchdog.json').name);watch=meta(wp)
  need(watch['command']==record['command']and type(watch['returncode'])is int and watch['returncode']==0 and watch['limit_failure']is None and watch['rss_cap_mib']==512 and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and 0<=watch['sampled_peak_rss_mib']<512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600,'old genuine four watchdogs retain original closure')
 report=dict(schema='ROOT_NATIVE_WARM_B2_CURRENT_EPOCH_BLIND_FULLFILE_BINDING_REPORT_V1',status='PASS_B2_SELECTED_READONLY_ROLES_CURRENT_EPOCH_BLIND_SHA_ONLY',failure=None,binding_pin=pb,source_pin=ps,independent_Source_review_pin=pr,old_Host_current_metadata_pin=b['old_Host_current_metadata_pin'],historical_old_Host_full_pin=b['historical_old_Host_full_pin'],old_true_tool_returns_current_metadata_pin=b['old_true_tool_returns_current_metadata_pin'],old_independent_review_current_metadata_pin=b['old_independent_review_current_metadata_pin'],genuine_old_Root_terminal_chunk='b77b5f',genuine_old_independent_review_chunk='fe36fd',ordered_role_pairs=pairs,current_epoch_B2_archive_pin=rolemap['B2_archive']['current_epoch_full_pin'],explicit_cumulative_metadata_file_pins=rb['explicit_cumulative_metadata_file_pins'],complete_joint_roots=b['complete_joint_roots'],original_caps=c.CAPS,resources=snapshots,selected_roles_only_not_4790_transitive_recertification=True,original_4790_transitive_current_recertification_performed=False,current_B63_original_m_body_or_stat_opened=False,blind_verified_B2_material_equals_recorded_B63_m_SHA_length=True,complete_B2_archive_MICROLIB2_MACROLIB_physical_tree_comparison_executed=False,actual_lineage_qualified=False,online_BOOT_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,children_started=0,decoder_executed=False,native_executed=False,files_deleted=False,Root_SELF_peak_bytes=selfcheck(),Root_elapsed_seconds=time.monotonic()-started,final_report_resource_check_passed=False)
 for row in pairs:current(row['current_epoch_full_pin'])
 q=BASE/'ROOT_CURRENT_EPOCH_B2_BLIND_BINDING_REPORT.json';need(not os.path.lexists(q),'report once');owned_report_identity=None
 def write_report(first):
  nonlocal owned_report_identity
  raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<2*2**20,'bridge report2MiB')
  oldsize=0 if first else q.lstat().st_size;need(sum(p.lstat().st_size for p in BASE.rglob('*')if p.is_file())-oldsize+len(raw)<16*2**20,'whole own Source16 before report publication')
  if not first:need(ids(q.lstat())==owned_report_identity,'same just-created own report current7 before rewrite')
  fd=os.open(q,os.O_WRONLY|os.O_NOFOLLOW|(os.O_CREAT|os.O_EXCL if first else 0),0o600)
  with os.fdopen(fd,'wb')as f:
   if not first:need(ids(os.fstat(f.fileno()))==owned_report_identity,'same own report opened7');f.truncate(0)
   f.write(raw);f.flush();os.fsync(f.fileno())
  owned_report_identity=ids(q.lstat())
 write_report(True);checkpoint(True);report['resources']=snapshots;report['final_report_resource_check_passed']=True;write_report(False);checkpoint(True)
 for row in pairs:current(row['current_epoch_full_pin'])
 small(ps);small(pb);raw=q.read_bytes();s=q.lstat();prpt=dict(path=str(q),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ids(s));need(prpt['size_bytes']==s.st_size,'final report fullPF');selfcheck()
 print(json.dumps(dict(status=report['status'],report_pin=prpt,selected_roles_only=True,all4790_transitive_recertified=False,lineage_qualified=False,online_BOOT_qualified=False)),flush=True)
if __name__=='__main__':main()
