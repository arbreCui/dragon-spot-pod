"""UNREADY Root-only exact native10 byte-preservation control.
No native/SCI decode, compression, restored large file, child, or deletion.
The original A Root1 and subsequent continuation0 remain separate facts.
The old B4 m restore is evidence only; B final55 receives a new byte proof.
"""
import argparse,hashlib,importlib.util,json,os,resource,stat,subprocess,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent
ART=Path('/Users/wen/spot/validation/artifacts')
READONLY_CONTEXT=None
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
def require(v,m):
 if type(v)is not bool or not v:raise RuntimeError(m)
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p,target=False):
 require(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['size_bytes'])is int
  and len(p['identity'])==7 and all(type(v)is int for v in p['identity']),'exact integer fullPF')
 q=Path(p['path']);s=q.lstat();owned=s.st_uid==501==os.getuid()and s.st_nlink==1
 require(q.is_absolute()and not any(a.is_symlink()for a in(q,*q.parents))and stat.S_ISREG(s.st_mode)
  and ids(s)==p['identity']and s.st_size==p['size_bytes'],'literal original role exact7')
 if target:require(owned,'only exact native/canonical/gzip byte roles owned501/nlink1; no readonly-role exception')
 elif not owned:
  require(READONLY_CONTEXT is not None,'specific frozen B3 readonly role context required')
  build,bm,buildpin,bmpin=READONLY_CONTEXT
  current(buildpin);current(bmpin);bm.current_metadata_role(p,build)
 return q
def current_failed_v1(p,plan):
 require(type(p)is dict and set(p)=={'path','size_bytes','identity'}and p in plan['retained_failed_v1_current7_only_pins'],'only exact failed-v1 current7-only role, never fullPF/SHA or deletion target')
 q=Path(p['path']);s=q.lstat()
 require(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==501==os.getuid()and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])and ids(s)==p['identity']and s.st_size==p['size_bytes'],'entire exact oldfailed file stable current7 only; no body read/hash or generic missing skip')
 return q
def current_failed_pool(p,plan):
 require(type(p)is dict and set(p)=={'path','size_bytes','identity'}and p in plan['retained_failed_pool_archive_current7_only_pins'],
  'only exact retained failed-pool metadata/runtime rows, never fullPF/SHA or deletion targets')
 q=Path(p['path']);s=q.lstat()
 require(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)
  and s.st_uid==501==os.getuid()and s.st_nlink==1 and type(p['size_bytes'])is int
  and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])
  and ids(s)==p['identity']and s.st_size==p['size_bytes'],'entire exact failed-pool retained row stable current7 only')
 return q
def unique(rows):
 out={}
 for p in rows:require(p['path']not in out or out[p['path']]==p,'same path same fullPF');out[p['path']]=p
 return list(out.values())

def own_source_bytes():
 total=0;pending=[BASE]
 while pending:
  q=pending.pop();s=q.lstat();require(stat.S_ISDIR(s.st_mode)and not q.is_symlink(),'own Source has no directory alias')
  with os.scandir(q)as entries:
   for e in entries:
    st=e.stat(follow_symlinks=False);require(not stat.S_ISLNK(st.st_mode),'entire Source no aliases')
    if stat.S_ISDIR(st.st_mode):pending.append(Path(e.path))
    elif stat.S_ISREG(st.st_mode):total+=st.st_size
    else:raise RuntimeError('own Source contains only ordinary files/directories')
 return total

def full(p,budget,parse=False):
 q=current(p);require(not parse or p['size_bytes']<8*2**20,'small metadata8MiB only')
 h=hashlib.sha256();n=0;parts=[]
 with os.fdopen(os.open(q,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  require(ids(os.fstat(f.fileno()))==p['identity'],'opened exact stable7')
  while True:
   budget();chunk=f.read(2**20)
   if not chunk:break
   n+=len(chunk);require(n<=p['size_bytes'],'fullEOF stream bounded by exact saved byte length');h.update(chunk)
   if parse:parts.append(chunk)
  require(ids(os.fstat(f.fileno()))==p['identity'],'fullEOF exact stable7')
 current(p);require(n==p['size_bytes']and h.hexdigest()==p['sha256'],'blind fullEOF SHA/length equals exact saved fullPF')
 return json.loads(b''.join(parts))if parse else dict(sha256=h.hexdigest(),size_bytes=n,full_EOF=True,stable_opened_and_EOF_identity=p['identity'])

def metadata(p,budget):return full(p,budget,True)
def module(p,name,budget):
 full(p,budget);spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);current(p);return m

def genuine_code(d,key,code):
 r=d[key];require(d['observed_closed']is True and type(d['original_integer_exit_code'])is int and d['original_integer_exit_code']==code and type(r['exit_code'])is int and r['exit_code']==code and r.get('session_id')is None,'genuine original closed typed integer tool return; no live session')
 return r

def genuine_post(tools,p):
 r=genuine_code(tools,'actual_review_return',0);require(json.loads(r['output'].strip().splitlines()[-1])['review_pin']==p,'genuine independent metadata post0 exact stdout review PF')

def historical_absence(plan):
 rows=plan['exact49_historical_absent_pins'];require(len(rows)==len({p['path']for p in rows})==49 and rows[-4:]==plan['exact4_retired_completed_spool_pins'],'only exact inherited45 plus just-completed4 historical paths')
 for p in rows:require(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),'precise closed historical absence only; no generic missing skip')

def compact(v):
 scalar=(str,int,float,bool,type(None));z={k:x for k,x in v.items()if isinstance(x,scalar)}
 return z

def main():
 global READONLY_CONTEXT
 started=time.monotonic();ap=argparse.ArgumentParser(allow_abbrev=False)
 for k in('plan','source','review','review-tools'):ap.add_argument('--'+k+'-pin',required=True)
 args=ap.parse_args()
 claim=BASE/'ROOT_NATIVE_EXACT10_BYTE_CONTROL_CLAIM.json'
 with claim.open('x')as f:
  json.dump(dict(schema='ROOT_EXCLUSIVE_NATIVE_EXACT10_BYTE_CONTROL_CLAIM_V1',Root_PID=os.getpid(),started_monotonic=started,argv=sys.argv,claim_before_project_helpers_and_payload_IO=True,children_started=0,retries=0),f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 import gzip
 state={};plan=None;snapshots=[];last_full_completed=0.0
 def light():
  peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
  require(peak<512*2**20 and time.monotonic()-started<600 and time.monotonic()-started<1800,'Root SELF512/stage600/whole1800 from first claim; no reset')
  require(own_source_bytes()<8*2**20,'whole new Source/claims/review/post/metadata8MiB')
  return peak
 def budget(force=False):
  nonlocal last_full_completed
  peak=light()
  if state and(force or time.monotonic()-last_full_completed>=5.0):
   sample=subprocess.run(['/bin/ps','-o','rss=','-p',str(os.getpid())],capture_output=True,text=True,timeout=2)
   require(sample.returncode==0 and sample.stderr==''and len(sample.stdout)<1024 and sample.stdout.strip().isdigit()and int(sample.stdout.strip())*1024<512*2**20,'original same-PID PS RSS guard; no child')
   h=state['history'].check();j=state['joint'].check();extra=0
   for p in plan['explicit_cumulative_metadata_file_pins']:
    current(p)
    if not any(Path(p['path']).is_relative_to(Path(r))for r in plan['complete_joint_roots']):extra+=p['size_bytes']
   for p in plan['retained_B2_current_epoch_readonly_pins']:
    current(p);require(any(Path(p['path']).is_relative_to(Path(r))for r in h['resource_roots']),'selected old B2 roles stay inside original history, not fresh external metadata')
   for p in plan['retained_failed_v1_current7_only_pins']:current_failed_v1(p,plan)
   for p in plan['retained_failed_pool_archive_current7_only_pins']:current_failed_pool(p,plan)
   historical_absence(plan);unlinked={}
   for fd in os.listdir('/dev/fd'):
    try:ss=os.fstat(int(fd))
    except(ValueError,OSError):continue
    if stat.S_ISREG(ss.st_mode)and ss.st_nlink==0:unlinked[ss.st_dev,ss.st_ino]=ss.st_size
   require(j['artifact_bytes']+extra+sum(unlinked.values())<2*2**30 and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'full83 actual joint/external/openunlinked/history96/cold/meta64/free8 original caps')
   light();last_full_completed=time.monotonic()
   v=dict(original_history=compact(h),complete_joint=compact(j),complete_joint_root_count=len(plan['complete_joint_roots']),external_metadata_bytes=extra,open_unlinked_bytes=sum(unlinked.values()),SELF_peak_bytes=peak,elapsed_seconds=time.monotonic()-started,actual_PS_return=dict(returncode=sample.returncode,stdout=sample.stdout,stderr=sample.stderr),non_scalar_resource_inventories_omitted=True)
   snapshots.append(v);state['latest']=v;return v
 ps=json.loads(args.source_pin);pp=json.loads(args.plan_pin);pr=json.loads(args.review_pin);pt=json.loads(args.review_tools_pin)
 require(ps['path']==str(Path(__file__).absolute())and pp['path']==str(BASE/'PLAN.json'),'exact executing Source and owning frozen PLAN')
 full(ps,budget);plan=metadata(pp,budget);review=metadata(pr,budget);tools=metadata(pt,budget);genuine_post(tools,pr)
 require(review['status']=='PASS_SOURCE_ONLY_NATIVE_EXACT10_BYTE_PRESERVATION_CONTROL'and review['failure']is None and review['source_only']is True and review['source_pin']==ps and review['plan_pin']==pp,'real independent same Source/PLAN metadata review0 before helpers or payload IO')
 require(plan['schema']=='ROOT_A_B_NATIVE_EXACT10_BYTE_PRESERVATION_CONTROL_PLAN_V1'and plan['Source_admission_ready']is True and plan['draft_unready']is False and plan['actual_prerequisites_closed']is True and plan['only_Root_native_byte_preservation_control']is True and plan['actual_exact4_execute0_independent_post0_complete']is True and plan['bounded_own_Source_metadata_receipts_bytes']==8*2**20 and plan['Root_stage_seconds']==600 and plan['Root_whole_seconds']==1800 and plan['resource_full_scan_interval_seconds']==5.0 and plan['resource_scan_last_recorded_after_completion']is True and plan['new_data_owning_root_created']is False and plan['original_caps']==CAPS,'NULL/unclosed draft never authorizes byte IO; exact original caps plus tightened Source8')
 roots=plan['complete_joint_roots'];require(len(roots)==len(set(roots))==83 and any(BASE.is_relative_to(Path(r))for r in roots)and all(Path(r).is_dir()for r in roots)and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b),'entire real83 prefix, no extra or reset data ownroot')
 require(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and Path(sys.executable).resolve()==Path(plan['original_complete_ENV_Python_B_prefix'][-2]).resolve()and all(os.environ.get(k)=='1'for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')),'original Python/unoptimized/unprofiled/thread1 environment')
 buildpin=plan['original_guard_build_plan_pin'];bmpin=plan['original_guard_build_contract_Source_pin'];build=metadata(buildpin,budget);bm=module(bmpin,'native_exact10_original_B3_metadata_roles',budget);READONLY_CONTEXT=(build,bm,buildpin,bmpin)
 module(plan['original_production_inputs_Source_pin'],'production_inputs',budget)
 production=module(plan['original_production_resource_Source_pin'],'native_exact10_original_production',budget)
 factory=module(plan['original_history_resource_Source_pin'],'native_exact10_original_history',budget)
 state.update(history=factory.DynamicHistoryResources(ART,factory.history_roots([],ART),8*2**30,96*2**30,production.ResourceFailure),joint=production.DiskResources(ART.parent,roots,8*2**30,2*2**30));before=budget(True)
 require(before['complete_joint']['artifact_bytes']+before['external_metadata_bytes']+before['open_unlinked_bytes']+8*2**20<2*2**30,'actual full83 plus all external/openunlinked and conservative Source8 reservation fit original2GiB')
 projection=metadata(plan['role_projection_pin'],budget)
 require(projection['schema']=='NATIVE_EXACT10_CANDIDATE_TO_EXACT_CANONICAL_BYTE_SOURCE_METADATA_PROJECTION_V1'and projection['source_only']is True and projection['metadata_only']is True and projection['formal_byte_control_admission']is False and projection['actual_prerequisite_closure_pins']==plan['actual_prerequisite_closure_pins']and plan['exact4_prerequisite_closure_pins']==plan['actual_prerequisite_closure_pins']['exact4_completed_spools_Root0_post0'],'projection is Source role metadata, not claimed prior byte proof')
 targets=plan['exact_ordered10_candidate_full_pins'];canonical=plan['retained_ordered7_canonical_native_full_pins'];all17=plan['all17_native_full_pins'];maps=plan['exact_ordered10_recovery_mappings']
 require(targets==projection['exact_ordered10_candidate_full_pins']and canonical==projection['retained_ordered7_canonical_native_full_pins']and all17==projection['all17_native_full_pins']==unique(targets+canonical)and maps==projection['exact_ordered10_recovery_mappings']and len(targets)==10 and len(canonical)==7 and len(all17)==17 and len(maps)==10 and [m['target_pin']for m in maps]==targets and len({p['path']for p in all17})==17 and sum(p['size_bytes']for p in targets)==plan['candidate_total_bytes']==232289584 and sum(p['size_bytes']for p in all17)==plan['all17_native_total_bytes']==368221520,'exact17 native roles and10 ordered candidate-to-recovery maps, no generic dedup')
 for p in all17:current(p,True)
 cp=plan['exact4_prerequisite_closure_pins'];receipt4=metadata(cp['receipt'],budget);root4=metadata(cp['Root_tools'],budget);post4=metadata(cp['post'],budget);post4tools=metadata(cp['post_tools'],budget);e4plan=metadata(cp['plan'],budget);genuine_code(root4,'actual_terminal_return',0);genuine_post(post4tools,cp['post'])
 require(json.loads(root4['actual_terminal_return']['output'].strip().splitlines()[-1])['receipt_pin']==cp['receipt'],'genuine exact4 Root0 stdout receipt')
 require(receipt4['mode']=='execute'and receipt4['failure']is None and receipt4['status']=='RETIRED_CURRENT_A_B_FINAL55_COMPLETED_SPOOL_EXACT4_DERIVED_TEMPORARIES_ONLY'and receipt4['plan_pin']==cp['plan']and receipt4['actual_released_pins']==receipt4['exact_target_pins']==plan['exact4_retired_completed_spool_pins']and receipt4['actual_released_bytes']==183292696 and receipt4['resources_after_original_classes_forced_fresh']is True and receipt4['files_deleted']is True,'genuine exact4 completed-spool cleanup, unrelated native remains live')
 require(post4['schema']=='CURRENT_A_B_FINAL55_COMPLETED_SPOOL_EXACT4_EXECUTION_METADATA_POSTVERIFY_V1'and post4['status']=='PASS_ACTUAL_A_B_FINAL55_COMPLETED_SPOOL_EXACT4_TEMPORARIES_RETIRED_NATIVE_AND_RESULTS_PRESERVED_METADATA_ONLY'and post4['failure']is None and post4['metadata_only']is True and type(post4['actual_Root_integer_exit_code'])is int and post4['actual_Root_integer_exit_code']==0 and post4['actual_execution_receipt_pin']==cp['receipt']and post4['actual_Root_tools_pin']==cp['Root_tools']and post4['plan_pin']==cp['plan']and post4['exact_four_targets_absent_verified_twice']is True and post4['all_retained_roles_current7_verified_twice']is True and post4['retained_all_current7_pins']==plan['retained_current7_pins']and post4['complete_joint_roots']==e4plan['complete_joint_roots']==roots,'actual independent exact4 metadata0 and exact latest live-retainer roles')
 proof=plan['actual_prerequisite_closure_pins'];posts={};reports={}
 specs=(('A_original_stage0_Root1','actual_report_pin','actual_Root_true_tool_return_pin',1),('A_continuation_Root0_no_new_child','actual_report_pin','actual_Root_true_tool_return_pin',0),('A_full_extract_Root0_child2','actual_report_pin','actual_Root_true_tool_return_pin',0),('B_full_capture_Root0_child0','actual_Host_report_pin','actual_Root_tools_pin',0),('B4_member0_old_Root0_no_child','actual_member0_Root_report_pin','actual_Root_tools_pin',0),('B4_all4_Root0_child0','actual_Host_report_pin','actual_Root_tools_pin',0))
 for name,reportkey,rootkey,code in specs:
  c=proof[name];post=metadata(c['post'],budget);report=metadata(c['Root_report'],budget);raw=metadata(c['Root_tools'],budget);ptools=metadata(c['post_tools'],budget);genuine_code(raw,'actual_terminal_return',code);genuine_post(ptools,c['post'])
  require(post['schema']==c['post_schema']and post['status']==c['post_status']and post['failure']is None and type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==code and post[reportkey]==c['Root_report']and post[rootkey]==c['Root_tools'],'real exact producer/extract/archive original Root state and independent post0 roles')
  posts[name]=post;reports[name]=report
 ao=posts['A_original_stage0_Root1'];ac=posts['A_continuation_Root0_no_new_child'];ax=posts['A_full_extract_Root0_child2'];bc=posts['B_full_capture_Root0_child0'];mp=posts['B4_member0_old_Root0_no_child'];b4=posts['B4_all4_Root0_child0']
 am=projection['A_material_saved_full_pin'];af=projection['A_final55_saved_full_pin'];ae=projection['A_early7_saved_full_pins'];bf=projection['B_final55_saved_full_pin'];be=projection['B_early7_saved_full_pins']
 require(ao['actual_material_stage_closed0']is True and ao['all_new_scene_files_full_EOF_read_once_with_pin_cache']is True and all(p in ao['actual_scene_full_EOF_pins']for p in [am,af]+ae)and reports['A_original_stage0_Root1']['status']=='FAILED_CURRENT_OBSERVATION_NO_RETRY'and reports['A_original_stage0_Root1']['failure']is not None,'A original Root1 release-blocked remains failed with true stage0 exact fullEOF native9')
 require(ac['actual_original_Root_integer_exit_code']==1 and ac['actual_new_material_child_launch_count']==0 and ac['original_capture_collector_reexecuted']is False and ac['actual_complete_state_snapshot_pin_count']==8 and ac['actual_complete_context_pin_count']==55,'separate A continuation0 exact8/55 without new material child or Root1 relabel')
 achild=metadata(proof['A_full_extract_Root0_child2']['child_report'],budget)
 require(ax['actual_child_report_pin']==proof['A_full_extract_Root0_child2']['child_report']and ax['actual_child_integer_exit_code']==2 and ax['actual_complete_snapshot_count']==8 and ax['actual_complete_context_count']==55 and [r['input_pin']for r in achild['states']['A']]==ae+[af],'real A full8 extraction original input PFs in exact order')
 require(bc['actual_child_integer_exit_code']==0 and all(p in bc['new_output_blind_fullEOF_SHA_current7_twice_pins']for p in be+[bf]),'real B capture native8 complete original blind2 saved PFs')
 gz=plan['existing_complete_B4_gzip_pin'];ep=plan['existing_B4_member0_entry_pin'];ip=plan['existing_B4_all4_lookup_index_pin'];oldm=plan['historical_B4_original_m_full_pin'];entry=metadata(ep,budget);index=metadata(ip,budget)
 require(mp['actual_child_integer_exit_code']is None and mp['Root_actual_complete_member0_stream_verified']is True and mp['original_member0_saved_full_pin']==oldm and mp['complete_member0_gzip_pin']==gz and mp['retained_member0_entry_pin']==ep and mp['actual_streamed_decompressed_SHA']==oldm['sha256']and mp['actual_streamed_decompressed_length']==oldm['size_bytes'],'old m Root0 stream proof retained as old-path evidence only, not new Bfinal control')
 require(b4['actual_child_integer_exit_code']==0 and b4['Root_recorded_stream_decompression_proofs_matched_original_fullPF']is True and b4['actual_archive_index_pin']==ip and b4['ordered4_original_product_full_pins'][0]==oldm and b4['ordered4_compressed_archive_full_pins'][0]==gz and b4['ordered4_entry_pins'][0]==ep and len(index['entries'])==4 and index['entries'][0]['entry_pin']==ep and index['entries'][0]['original_plain_full_pin']==oldm and index['entries'][0]['compressed_archive_full_pin']==gz and entry['original_plain_full_pin']==oldm and entry['compressed_archive_full_pin']==gz and entry['original_plain_preserved']is True and entry['exact_original_plain_bytes_recoverable']is True,'precise permanent B4 m gzip/entry/all4 index and old creation-history preserved')
 require(entry['compression_input_SHA']==entry['streamed_decompressed_SHA']==oldm['sha256']==bf['sha256']and entry['compression_input_length']==entry['streamed_decompressed_length']==oldm['size_bytes']==bf['size_bytes']==76594248 and gz['size_bytes']==33559716,'saved Bfinal and oldm exact SHA/length equality; fresh control still pending')
 for m in maps:
  if m['mode']=='retained_native_copy':
   c=m['canonical_pin'];require(c in canonical and (c['sha256'],c['size_bytes'])==(m['target_pin']['sha256'],m['target_pin']['size_bytes']),'each explicit native-copy role saved fullSHA/length equality')
  else:require(m['mode']=='existing_complete_gzip_member'and m['target_pin']==bf and m['canonical_gzip_pin']==gz and m['canonical_entry_pin']==ep and m['canonical_B4_lookup_index_pin']==ip and m['historical_original_member0_full_pin']==oldm,'only exact Bfinal mapped to complete archived oldm bytes')
 retained=unique(plan['retained_current7_pins']+plan['retained_archive_metadata_current7_pins']+plan['explicit_cumulative_metadata_file_pins']+plan['retained_B2_current_epoch_readonly_pins']+[gz,ep,ip])
 for p in retained:current(p)
 historical_absence(plan);budget(True)
 native_proofs=[]
 for p in all17:
  current(p,True);result=full(p,budget);native_proofs.append(dict(original_full_pin=p,blind_fullEOF_SHA_length=result))
 require(len(native_proofs)==17,'all candidates and every retained canonical fully blind-hashed; no numeric/native decode')
 gzip_before=full(gz,budget);budget(True);h=hashlib.sha256();n=0;complete=False
 with os.fdopen(os.open(current(gz,True),os.O_RDONLY|os.O_NOFOLLOW),'rb')as raw:
  require(ids(os.fstat(raw.fileno()))==gz['identity'],'opened Bfinal recovery gzip7')
  with gzip.GzipFile(fileobj=raw,mode='rb')as stream:
   while True:
    budget();chunk=stream.read(2**20)
    if not chunk:complete=True;break
    n+=len(chunk);require(n<=bf['size_bytes'],'Bfinal decompression bounded by exact saved original length');h.update(chunk)
  require(ids(os.fstat(raw.fileno()))==gz['identity'],'Bfinal recovery gzip fullEOF7')
 require(complete and n==bf['size_bytes']and h.hexdigest()==bf['sha256'],'new full stream-decompressed bytes match this Bfinal fullPF, not only historical m')
 budget(True);gzip_after=full(gz,budget);require(gzip_before==gzip_after,'complete gzip blind fullEOF SHA and stable7 unchanged before/after new Bfinal control')
 for p in all17:current(p,True)
 for p in retained:current(p)
 historical_absence(plan);full(ps,budget);metadata(pp,budget);after=budget(True)
 report=dict(schema='ROOT_A_B_NATIVE_EXACT10_BYTE_PRESERVATION_CONTROL_REPORT_V1',status='PASS_ROOT_NATIVE_EXACT10_COMPLETE_BYTE_PRESERVATION_CONTROL_NO_RETIREMENT',failure=None,source_pin=ps,plan_pin=pp,actual_Source_review_pin=pr,actual_Source_review_tools_pin=pt,role_projection_pin=plan['role_projection_pin'],exact_ordered10_candidate_full_pins=targets,retained_ordered7_canonical_native_full_pins=canonical,exact_ordered10_recovery_mappings=maps,all17_native_full_pins=all17,candidate_total_bytes=232289584,all17_native_total_bytes=368221520,all17_native_blind_fullEOF_SHA_length_proofs=native_proofs,all17_native_fullEOF_SHA_and_stable7_verified=True,all17_native_current7_verified_before_and_after=True,existing_complete_B4_gzip_pin=gz,existing_B4_member0_entry_pin=ep,existing_B4_all4_lookup_index_pin=ip,historical_B4_original_m_full_pin=oldm,new_B_final55_full_pin=bf,new_B_final55_streamed_decompressed_SHA=h.hexdigest(),new_B_final55_streamed_decompressed_length=n,new_B_final55_independent_complete_stream_verified=True,gzip_blind_fullEOF_before=gzip_before,gzip_blind_fullEOF_after=gzip_after,actual_prerequisite_closure_pins=proof,exact4_prerequisite_closure_pins=cp,old_A_Root_integer_exit_code=1,A_continuation_Root_integer_exit_code=0,A_continuation_new_material_children_started=0,old_B4_member0_proof_relabelled_as_new_B_final55_control=False,all_retained_roles_current7_verified=True,retained_current7_pins=plan['retained_current7_pins'],retained_archive_metadata_current7_pins=plan['retained_archive_metadata_current7_pins'],retained_B2_current_epoch_readonly_pins=plan['retained_B2_current_epoch_readonly_pins'],retained_failed_v1_current7_only_pins=plan['retained_failed_v1_current7_only_pins'],retained_failed_pool_archive_current7_only_pins=plan['retained_failed_pool_archive_current7_only_pins'],exact49_historical_absent_pins=plan['exact49_historical_absent_pins'],complete_joint_roots=roots,original_caps=CAPS,new_data_owning_root_created=False,bounded_own_Source_metadata_receipts_bytes=8*2**20,resources_before=before,resources_after=after,original_resource_scalar_snapshots=snapshots,Root_SELF_peak_bytes=light(),Root_elapsed_seconds=time.monotonic()-started,final_report_resource_check_passed=False,children_started=0,actual_child_integer_exit_code=None,restored_large_file_written=False,native_or_scientific_values_decoded=False,compiler_executed=False,native_executed=False,compression_executed=False,files_deleted=False,retirement_authorized=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 target=BASE/'ROOT_NATIVE_EXACT10_BYTE_PRESERVATION_CONTROL_REPORT.json'
 def emit(rewrite=False):
  raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();require(len(raw)<2*2**20,'compact own report below2MiB');oldsize=target.lstat().st_size if rewrite else 0
  require(own_source_bytes()-oldsize+len(raw)<8*2**20,'whole Source/review/metadata/report8MiB including write')
  if rewrite:
   previous=target.lstat()
   with os.fdopen(os.open(target,os.O_WRONLY|os.O_NOFOLLOW),'wb')as f:
    require(ids(os.fstat(f.fileno()))==ids(previous)and previous.st_uid==501==os.getuid()and previous.st_nlink==1,'rewrite only own exact one-link report');f.seek(0);f.truncate(0);f.write(raw);f.flush();os.fsync(f.fileno())
   require(ids(target.lstat())[:4]==ids(previous)[:4],'same own report inode/link role')
  else:
   with target.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
  fd=os.open(BASE,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
  try:os.fsync(fd)
  finally:os.close(fd)
 emit();report['resources_after_including_summary_bytes']=budget(True);report['final_report_resource_check_passed']=True;emit(True);budget(True)
 result=full(dict(path=str(target),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),size_bytes=target.lstat().st_size,identity=ids(target.lstat())),budget)
 reportpin=dict(path=str(target),sha256=result['sha256'],size_bytes=result['size_bytes'],identity=ids(target.lstat()))
 print(json.dumps(dict(status=report['status'],report_pin=reportpin,native_candidate_count=10,canonical_native_count=7,children_started=0,files_deleted=False,retirement_authorized=False)),flush=True)

if __name__=='__main__':main()
