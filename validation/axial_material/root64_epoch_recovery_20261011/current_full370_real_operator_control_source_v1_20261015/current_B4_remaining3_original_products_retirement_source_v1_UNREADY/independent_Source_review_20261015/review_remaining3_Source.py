"""Independent Source and small metadata/current7 only. No project imports/body IO."""
import ast,builtins,hashlib,json,os,stat,symtable
from pathlib import Path
D=Path(__file__).absolute().parent.parent
HERE=Path(__file__).absolute().parent
def need(v,m):
 if not v:raise RuntimeError(m)
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p,owned=True):
 need(set(p)=={'path','sha256','size_bytes','identity'}and type(p['size_bytes'])is int and len(p['identity'])==7 and all(type(v)is int for v in p['identity']),'typed fullPF')
 q=Path(p['path']);s=q.lstat();need(q.is_absolute()and stat.S_ISREG(s.st_mode)and ids(s)==p['identity']and s.st_size==p['size_bytes']and not any(x.is_symlink()for x in(q,*q.parents)),'exact current7')
 if owned:need(s.st_uid==os.getuid()==501 and s.st_nlink==1,'owned501 nlink1')
def pin(q):
 q=Path(q);s=q.lstat();raw=q.read_bytes();need(ids(q.lstat())==ids(s),'stable own metadata/Source');return dict(path=str(q.absolute()),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ids(s))
def read(p):
 current(p);need(p['size_bytes']<8*2**20,'small metadata/Source only');raw=Path(p['path']).read_bytes();need(len(raw)==p['size_bytes']and hashlib.sha256(raw).hexdigest()==p['sha256'],'fullEOF metadata/Source');current(p);return raw
def meta(p):return json.loads(read(p))
def truth(p,key,field,want):
 x=meta(p);r=x[key];need(x['observed_closed']is True and type(x['original_integer_exit_code'])is int and x['original_integer_exit_code']==0 and type(r['exit_code'])is int and r['exit_code']==0 and 'session_id'not in r and json.loads(r['output'].splitlines()[-1])[field]==want,'genuine original typed closed0 exact PF');return x
def main():
 need(not(HERE/'REVIEW.json').exists(),'review once')
 ap=pin(D/'AUTHOR_SOURCE_FREEZE.json');need(ap['sha256']=='d7d378b14041490a31e082b7d48c358c40566c8c360affa5ee09968179952f2d','Root supplied author freeze');a=meta(ap);pp=a['whole_plan_pin'];need(pp['sha256']=='4d1df816c26c8008f83dc9e3235cc41320290ae057fd7067ce451f72de0eefa6','Root supplied PLAN');p=meta(pp)
 need(a['source_only']is True and a['author_STOP_WRITES']is True and p['Source_admission_ready']is True and p['draft_unready']is False and p['source_only']is True,'frozen Source-only admission')
 sp=a['whole_Source_file_pins'];need(len(sp)==2,'complete two Source table');code={}
 for q in sp:
  text=read(q).decode();ast.parse(text);t=symtable.symtable(text,q['path'],'exec');top=set(t.get_identifiers());unknown=set()
  def walk(s):
   for name in s.get_identifiers():
    sym=s.lookup(name)
    if sym.is_referenced()and sym.is_global()and name not in top and name not in vars(builtins):unknown.add(name)
   for child in s.get_children():walk(child)
  walk(t);need(not unknown,'no unbound global candidates');code[Path(q['path']).name]=text
 workerpin=next(q for q in sp if Path(q['path']).name=='retire_remaining3_archived_B_products.UNREADY.py');pubpin=next(q for q in sp if Path(q['path']).name=='write_once_remaining3_B_products_reviewable_CLI.UNREADY.py')
 need(workerpin['sha256']=='5a31fea62b8df0fcb2de90e0defabc83e5cfb0aee87316bfe6088d20fb50e46d'and pubpin['sha256']=='7d6e4b682e3113b2540078d8570a0e254e20ea00def6a58ad7e48dfd2cff4e73','exact reviewed Source bytes')
 inverse=meta(a['whole_EX2_inverse_evidence_pin']);need(inverse['new_remaining3_Source_pins']==sp,'inverse covers exact both Sources')
 for old,new in zip(inverse['old_EX2_Source_pins'],sp):
  text=code[Path(new['path']).name]
  for row in reversed(inverse['exact_literal_offset_replacements'][Path(new['path']).name]):
   at=row['replacement_character_offset'];n=row['new_literal'];need(text[at:at+len(n)]==n,'exact reverse replacement offset');text=text[:at]+row['old_literal']+text[at+len(n):]
  need(text.encode()==read(old),'whole frozen EX2 inverse; original lifecycle guard unchanged')
 w=code[Path(workerpin['path']).name];pub=code[Path(pubpin['path']).name]
 for part in ["if target:require(owned",'bm.current_metadata_role(p,build)','peak<512*2**20','time.monotonic()-started<600',"state.update(last=time.monotonic()",'module(plan[\'original_production_inputs_Source_pin\'],\'production_inputs\',budget)',"['/usr/sbin/lsof','-n','-P','-Fpcfn','--']",'os.stat(q.name,dir_fd=fd,follow_symlinks=False)',"os.unlink(q.name,dir_fd=fd);os.fsync(fd)","budget(True);d['resources_after']=state['latest'];d['resources_after_original_classes_forced_fresh']=True",'len(d[\'actual_released_pins\'])==3']:
  need(part in w,'required original worker control: '+part)
 need(w.index("with receipt.open('xb')")<w.index("module(bmpin,")and w.index("module(plan['original_production_inputs_Source_pin']")<w.index("production=module("),'exclusive receipt before helper imports and original preload order')
 for text in [w,pub]:
  for part in ['independent_readonly_post0_required_before_execute','actual_readonly_Root_integer_exit_code','actual_readonly_tools_pin','actual_released_bytes','resources_after_original_classes_forced_fresh']:
   need(part in text,'readonly independent post gate in both publisher and worker')
 inherited=meta(p['inherited_complete_archive_plan_pin']);roots=p['complete_joint_roots'];caps=inherited['original_caps'];need(p['original_caps']==a['original_caps']==caps and caps==dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0),'all original caps unchanged')
 need(roots==p['actual_archive_complete_prefix']==inherited['complete_joint_roots']==a['complete_joint_roots']and len(roots)==74 and len(roots)==len(set(roots))and p['no_new_output_root']is True and not any(Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y),'full74 prefix no new root/nesting/reset')
 targets=p['exact_target_pins'];originals=inherited['all4_product_pins'];historical=p['historical_retired_first_product_pin'];need(targets==inherited['live_original_product_pins']==originals[1:]and [Path(x['path']).name for x in targets]==['u.asc','a.asc','t.asc']and len(targets)==3 and sum(x['size_bytes']for x in targets)==p['target_total_bytes']==p['planned_released_bytes']==346861973 and historical==originals[0]and inherited['retired_original_product_pins']==[historical]and not os.path.lexists(historical['path']),'only exact remaining3 targets; first original only historical absent')
 for q in targets:current(q)
 cp=p['actual_archive_closure_pins'];host=meta(cp['Host']);child=meta(cp['child_report']);index=meta(cp['index']);post=meta(cp['post']);raw=truth(cp['Root_tools'],'actual_terminal_return','report_pin',cp['Host']);truth(cp['post_tools'],'actual_review_return','review_pin',cp['post'])
 need(raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False and host['status']=='ACTUAL_CURRENT_B4_ALL_PRODUCTS_ARCHIVE_REUSE_MEMBER0_CLOSED0_ONE_RETIRED_THREE_LIVE'and host['failure']is None and host['archive_complete']is True and host['final_report_resource_check_passed']is True and host['binding_pin']==p['inherited_complete_archive_plan_pin']and host['original_caps']==caps and host['complete_joint_roots']==roots and host['actual_child_receipt']['report_pin']==cp['child_report']and len(host['records'])==1 and host['records'][0]['status']=='PASS','actual full4 Root0 and one genuine child0')
 watch=host['actual_watchdog'];need(type(watch['returncode'])is int and watch['returncode']==0 and watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and watch['rss_cap_mib']==512 and 0<=watch['sampled_peak_rss_mib']<512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600,'original private OwnRSS actual child0')
 need(child['status']=='ALL4_COMPLETE_B_PRODUCT_BYTE_PROOF_CLOSED0_ONE_RETIRED_THREE_LIVE'and child['failure']is None and child['completed_count']==4 and child['newly_archived_count']==3 and child['reused_complete_archive_count']==1 and child['index_pin']==cp['index']and child['binding_pin']==p['inherited_complete_archive_plan_pin'],'actual complete child4 reused1/new3')
 rows=index['entries'];need(index['schema']=='CURRENT_B4_COMPLETE_PRODUCT_LOSSLESS_ORIGINAL_PATH_ARCHIVE_LOOKUP_V2'and index['binding_pin']==p['inherited_complete_archive_plan_pin']and len(rows)==4 and [r['original_plain_full_pin']for r in rows]==[historical]+targets==originals,'ordered historicalfirst1 plus remaining3 exactly original4')
 gzip=[];entry=[]
 for ordinal,(row,original)in enumerate(zip(rows,originals)):
  need(row['ordinal']==ordinal and row['compression_input_SHA']==row['streamed_decompressed_SHA']==original['sha256']and row['compression_input_length']==row['streamed_decompressed_length']==original['size_bytes']and row['exact_original_plain_bytes_recoverable']is True,'full4 recorded stream byte proofs')
  saved=meta(row['entry_pin']);need(saved['original_plain_full_pin']==original and saved['compressed_archive_full_pin']==row['compressed_archive_full_pin']and saved['original_plain_preserved']is True,'entry creation history stable')
  if ordinal==0:need(row['original_plain_preserved']is False and row['original_plain_preserved_at_entry_creation']is True and row['entry_pin']==inherited['reused_member0_entry_pin']and row['compressed_archive_full_pin']==inherited['reused_member0_gzip_pin'],'historical first member reused whole at old path')
  else:need(row['original_plain_preserved']is True,'current remaining3 original retained')
  gzip.append(row['compressed_archive_full_pin']);entry.append(row['entry_pin']);current(gzip[-1])
 need(gzip==p['retained_all4_gzip_pins']and entry==p['retained_all4_entry_pins'],'exact4 gzip/entry retention')
 r=p['actual_archive_post_key_projection'];need(post['schema']==r['schema']and post['status']==r['status']and post['failure']is None and post['metadata_only']is True and post[r['Host_pin_field']]==cp['Host']and post[r['Root_tools_pin_field']]==cp['Root_tools']and post[r['child_report_pin_field']]==cp['child_report']and post[r['index_pin_field']]==cp['index']and post[r['ordered_original_pins_field']]==originals and post[r['ordered_archive_pins_field']]==gzip and post[r['ordered_entry_pins_field']]==entry and post[r['Root_streamed_proofs_field']]is True and type(post[r['Root_exit_field']])is int and post[r['Root_exit_field']]==0 and type(post[r['child_exit_field']])is int and post[r['child_exit_field']]==0,'genuine independent full4 archive metadata post0 exact field projection')
 need(p['retained_native_current7_pins']==inherited['retained_native_current7_pins']and len(p['retained_native_current7_pins'])==79 and p['original_B_native_and_readonly_input_current7_pins']==inherited['original_B_native_and_readonly_input_current7_pins']and len(p['original_B_native_and_readonly_input_current7_pins'])==11,'all79native and11inputs retained')
 retained=p['retained_native_current7_pins']+p['original_B_native_and_readonly_input_current7_pins']+p['retained_archive_metadata_current7_pins']+gzip+entry+p['explicit_cumulative_metadata_file_pins']
 need(not {x['path']for x in targets}&{x['path']for x in retained}and historical['path']not in{x['path']for x in retained},'targets exclude all results/docs/meta; historical absent original never current7')
 for q in retained:current(q,False)
 need(p['independent_readonly_post0_required_before_execute']is True and p['forced_fresh_original_resource_classes_after_final_unlink']is True and p['bounded_own_Source_metadata_receipts_bytes']==16*2**20,'readonly post0 before unlink and forced fresh after last unlink mandatory')
 for q in sp:read(q)
 report=dict(schema='INDEPENDENT_CURRENT_B4_REMAINING3_RETIREMENT_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_CURRENT_B4_REMAINING3_ORIGINAL_PRODUCTS_RETIREMENT_V1',failure=None,source_only=True,source_pin=workerpin,plan_pin=pp,complete_source_file_pins=sp,author_source_freeze_pin=ap,whole_EX2_inverse_evidence_pin=a['whole_EX2_inverse_evidence_pin'],both_Source_whole_EX2_inverse_verified=True,AST_and_unbound_global_checks_passed=True,actual_archive_closure_pins=cp,exact_target_pins=targets,planned_released_bytes=346861973,historical_retired_first_product_pin=historical,historical_first_product_not_current7_or_body_read=True,retained_all4_gzip_pins=gzip,retained_all4_entry_pins=entry,retained_archive_index_pin=cp['index'],complete_joint_roots=roots,original_caps=caps,all79native11inputs_and_documents_retained=True,independent_readonly_post0_required_before_execute=True,original_PS_lsof_dirfd7_unlinklogs_fsync_forcedfresh_controls_preserved=True,metadata_only=True,product_or_gzip_body_read=False,project_helpers_or_worker_or_PS_or_lsof_or_pub_or_GEN_executed=False,files_deleted=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 q=HERE/'REVIEW.json'
 with q.open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(dict(status=report['status'],review_pin=pin(q),source_only=True)),flush=True)
if __name__=='__main__':main()
