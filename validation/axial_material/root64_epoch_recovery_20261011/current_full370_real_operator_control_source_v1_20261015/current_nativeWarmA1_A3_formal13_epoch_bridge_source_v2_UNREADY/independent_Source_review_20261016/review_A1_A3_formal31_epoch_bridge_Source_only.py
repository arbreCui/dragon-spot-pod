"""Independent A1 A3 formal31 epoch bridge Source review. No candidate/helper imports or payload reads."""
import ast,hashlib,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent;D=BASE.parent
FULL={'path','sha256','size_bytes','identity'};ONLY={'path','size_bytes','identity'};SDK=[]
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p,target=False):
 assert type(p)is dict and set(p)in(FULL,ONLY)and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(v)is int for v in p['identity'])
 q=Path(p['path']);s=q.lstat();assert q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and ids(s)==p['identity']and s.st_size==p['size_bytes']and s.st_nlink==1
 assert s.st_uid==os.getuid()or(not target and p in SDK and s.st_uid==0)
 return q
def full(p):
 assert set(p)==FULL and p['size_bytes']<8*2**20
 q=current(p);b=q.read_bytes();assert len(b)==p['size_bytes']and hashlib.sha256(b).hexdigest()==p['sha256'];current(p);assert hashlib.sha256(q.read_bytes()).hexdigest()==p['sha256'];return b
def meta(p):return json.loads(full(p))
def pin(q):
 q=Path(q).absolute();s=q.lstat();assert stat.S_ISREG(s.st_mode)and s.st_size<8*2**20;b=q.read_bytes();assert ids(q.lstat())==ids(s);return dict(path=str(q),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=ids(s))
def zero(p,key,field,want):
 j=meta(p);r=j[key];assert j['observed_closed']is True and type(j['original_integer_exit_code'])is int and j['original_integer_exit_code']==0 and type(r['exit_code'])is int and r['exit_code']==0 and r.get('session_id')is None and json.loads(r['output'].splitlines()[-1])[field]==want;return j
ap=pin(D/'AUTHOR_SOURCE_FREEZE.json');a=meta(ap);assert ap['sha256']=='89bd98483f6a6c291a0f31d7bf6f3afc9c118fc126ec2af5108cff988b7e8f28'and a['Source_and_binding_frozen']is True and a['Source_author_stopped_editing']is True and a['actual_Root_or_independent_metadata_post_not_executed']is True
sp=a['source_pin'];bp=a['binding_pin'];source=full(sp).decode();b=meta(bp);assert sp['sha256']=='6f82e834f07839aeadd53dc752f8c5487974cbb506cadcec302f37c75a03bb8a'and sp['size_bytes']==21503 and bp['sha256']=='2ed5ab061157290a2304189ba69a79521756172996c571d22f1825c3b51455df';ast.parse(source)
for k,v in a.items():
 if type(v)is dict and set(v)==FULL:full(v)
inv=meta(a['whole_old_Source_inverse_pin']);assert inv['new_Source_pin']==sp and inv['inverse_recovers_whole_old_Source']is True and inv['candidate_or_helper_or_body_executed']is False
old=full(inv['old_Source_pin']).decode();restored=source
for x in reversed(inv['changes']):
 lo,hi=x['new_start'],x['new_end'];assert restored[lo:hi]==x['new_text'];restored=restored[:lo]+x['old_text']+restored[hi:]
assert restored==old

def function_text(s,name):
 n=next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)and n.name==name);return '\n'.join(s.splitlines()[n.lineno-1:n.end_lineno])
assert function_text(source,'admit_old_producers')==function_text(old,'admit_old_producers')
lo=' for row in rows:\n  oldpin=';hi=' checkpoint(True)\n report='
assert source[source.index(lo):source.index(hi,source.index(lo))]==old[old.index(lo):old.index(hi,old.index(lo))]
caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2147483648,history_bytes=103079215104,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864,free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
assert b['schema']=='SOURCE_ONLY_A1_A3_SELECTED18_FORMAL13_CURRENT_EPOCH_BRIDGE_BINDING_V1'and b['source_only']is True and b['Source_admission_ready']is True and b['draft_unready']is False and b['new_owning_data_root_created']is False and b['original_caps']==caps and b['bounded_own_Source_metadata_receipts_bytes']==8*2**20 and b['latest_native10_execute0_and_independent_post0_complete']is True
build=meta(b['original_guard_build_plan_pin']);SDK=build['readonly_system_SDK_header_pins'];assert len(SDK)==3
cp=b['latest_native10_retirement_closure_pins'];assert cp==a['actual_latest_native10_retirement_closure_pins'];r10=meta(b['latest_native10_retirement_plan_pin']);rec=meta(cp['receipt']);post=meta(cp['post']);zero(cp['Root_tools'],'actual_terminal_return','receipt_pin',cp['receipt']);zero(cp['post_tools'],'actual_review_return','review_pin',cp['post'])
assert rec['schema']=='CURRENT_A_B_NATIVE_EXACT10_REDUNDANT_ORIGINAL_RETIREMENT_RECEIPT_V1'and rec['mode']=='execute'and rec['status']=='RETIRED_CURRENT_A_B_NATIVE_EXACT10_ORIGINAL_BYTES_PRESERVED_IN_EXACT_RECOVERY_MAPS'and rec['failure']is None and rec['plan_pin']==b['latest_native10_retirement_plan_pin']and rec['actual_released_pins']==rec['exact_target_pins']==r10['exact_target_pins']and rec['actual_released_bytes']==232289584 and rec['files_deleted']is True and rec['resources_after_original_classes_forced_fresh']is True
contract=r10['execute_post_report_contract'];assert post['schema']==contract['schema']and post['status']==contract['status']and post['failure']is None and post['metadata_only']is True and post['actual_execution_receipt_pin']==cp['receipt']and post['actual_Root_tools_pin']==cp['Root_tools']and type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==0 and post['actual_released_pins']==r10['exact_target_pins']and post['actual_released_bytes']==232289584 and post['files_deleted']is True and post['files_deleted_by_post']is False and post['exact_ten_targets_absent_verified_twice']is True and post['native_original_complete_bytes_preserved_by_exact_recovery_maps']is True and post['all_canonical7_gzip_entry_index_current7_verified_twice']is True and post['all_retained_roles_current7_verified_twice']is True
roots=b['complete_joint_roots'];assert roots==post['complete_joint_roots']==r10['complete_joint_roots']and len(roots)==len(set(roots))==83 and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)
for k,j in(('retained_current7_pins','retained_all_current7_pins'),('retained_archive_metadata_current7_pins','retained_archive_metadata_current7_pins'),('retained_B2_current_epoch_readonly_pins','retained_B2_current_epoch_readonly_pins'),('retained_failed_v1_current7_only_pins','retained_failed_v1_current7_only_pins'),('retained_failed_pool_archive_current7_only_pins','retained_failed_pool_archive_current7_only_pins')):assert b[k]==post[j]
assert b['exact59_historical_absent_pins']==r10['exact49_historical_absent_pins']+r10['exact_target_pins']and len(b['exact59_historical_absent_pins'])==len({p['path']for p in b['exact59_historical_absent_pins']})==59

def pointer(v,parts):
 for x in parts:v=v[int(x)]if type(v)is list else v[x]
 return v
hosts={};producer_metadata=[];missing_raw=[]
for p in b['historical_producers']:
 h=meta(p['current_Host_metadata_pin']);raw=meta(p['current_Root_raw_metadata_pin']);hist=p['historical_Host_full_pin'];cur=p['current_Host_metadata_pin'];assert (cur['path'],cur['sha256'],cur['size_bytes'],cur['identity'][1:])==(hist['path'],hist['sha256'],hist['size_bytes'],hist['identity'][1:])
 terminal=pointer(raw,p['genuine_terminal_JSON_pointer']);assert type(terminal['exit_code'])is int and terminal['exit_code']==0 and terminal.get('session_id')is None and terminal['chunk_id']==p['genuine_terminal_chunk'];out=json.loads(terminal['output'].splitlines()[-1]);assert out==dict(status=p['expected_Host_status'],failure=None,records=4)and h['status']==out['status']and h['failure']is None and len(h['records'])==4 and all(x['status']=='PASS'for x in h['records'])
 nt=h['actual_native_terminal'];assert nt['schema']==p['expected_terminal_schema']and nt['status']=='PASS'and(nt['plane'],nt['epoch'],nt['groups'],nt['unknowns'],nt['full_native_read_status'])==(p['plane'],0,370,14,3)
 for k in('all370_ROOT_FLUX64_FLUX64_REF_bits_equal','full_source64_type4_finite_and_exact_mirror','archive_read_only','strict_terminal_gate_passed'):assert nt[k]is True
 for record in h['records']:
  wp=next(x for x in p['current_watchdog_metadata_pins']if x['path']==str(Path(cur['path']).parent/(record['label']+'.watchdog.json')));w=meta(wp);assert w['command']==record['command']and type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None and w['rss_cap_mib']==512 and w['own_child_only']is True and w['liveness_group_cleanup']is True and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600
 for q in p['current_log_metadata_pins']:full(q)
 meta(p['current_terminal_binding_metadata_pin']);meta(p['current_owning_binding_metadata_pin']);assert p['historical_independent_actual_review_raw_pin']is None and p['historical_independent_actual_review_genuine_typed0_asserted']is False and p['all_transitive_fixed_inputs_recertified']is False;missing_raw.append(p['tag'])
 if p['plane']==1:
  sr=meta(p['current_historical_Source_review_metadata_pin']);assert sr['schema']=='INDEPENDENT_FINAL_CURRENT_WARM_A_V3_EXACT_SCHEMA_SOURCE_REVIEW'and p['current_historical_independent_actual_review_metadata_pin']is None
 else:
  ir=meta(p['current_historical_independent_actual_review_metadata_pin']);handoff=meta(p['current_historical_independent_review_handoff_metadata_pin']);provenance=meta(p['current_historical_independent_review_copy_provenance_metadata_pin']);full(p['current_historical_independent_review_Source_metadata_pin']);assert ir['schema']=='INDEPENDENT_CLOSED_ACTUAL_A23_SINGLE_PLANE_SAVED_REPORT_REVIEW_V1'and ir['status']=='PASS_ACTUAL_A3_FOUR_STAGE_SAVED_PRODUCER_ONLY'and ir['actual_summary_pin']==hist and ir['actual_Root_terminal_chunk']==p['genuine_terminal_chunk']and ir['actual_native_terminal']==nt
  saved=ir['actual_Root_terminal_receipt_pin'];curraw=p['current_Root_raw_metadata_pin'];assert(curraw['path'],curraw['sha256'],curraw['size_bytes'],curraw['identity'][1:])==(saved['path'],saved['sha256'],saved['size_bytes'],saved['identity'][1:]);copyrow=next(x for x in provenance['files']if x['durable_copy']['path']==p['current_historical_independent_actual_review_metadata_pin']['path']);assert copyrow['original']['path']==handoff['A3_review_pin']['path']and copyrow['original']['sha256']==handoff['A3_review_pin']['sha256']==p['current_historical_independent_actual_review_metadata_pin']['sha256']and handoff['A3_actual_terminal_chunk']==p['genuine_terminal_chunk']
 hosts[p['tag']]=h
 for k,v in p.items():
  if k.startswith('current_')and type(v)is dict and set(v)==FULL:producer_metadata.append(v)
  elif k.startswith('current_')and type(v)is list:producer_metadata.extend(v)
assert set(hosts)=={'A1','A3'}and missing_raw==['A1','A3']
formal=meta(b['historical_formal_plan_current_metadata_pin']);assert formal['formal_configuration']==b['historical_formal_configuration']and len(formal['formal_inputs'])==13
rows=b['ordered_role_specs'];assert len(rows)==b['selected_total_role_count']==31 and b['selected_A1_A3_role_count']==18 and b['selected_formal_role_count']==13 and len({x['role']for x in rows})==len({x['historical_full_pin']['path']for x in rows})==31 and sum(x['family']=='FORMAL13'for x in rows)==13 and sum(x['family']=='A1'for x in rows)==sum(x['family']=='A3'for x in rows)==9 and sum(x['historical_full_pin']['size_bytes']for x in rows)==b['selected_total_recorded_bytes']==680089850
for row in rows:
 p=row['historical_full_pin'];expected=row['expected_start_current7'];assert set(p)==FULL and type(expected)is list and len(expected)==7 and all(type(x)is int for x in expected)and expected[1:]==p['identity'][1:]and p['identity'][0]==16777234 and expected[0]==16777229 and row['future_current_epoch_full_pin']is None
 src=formal if row['family']=='FORMAL13'else hosts[row['family']];assert pointer(src,row['historical_source_JSON_pointer'].strip('/').split('/'))==p
for k in('all_historical_transitive_fixed_inputs_recertified','new_B_bearing_context_compatibility_or_lineage_proved','online_BOOT_qualified','physics_qualified','AAA_qualified','ABA_admitted','goal_complete','Source_author_opened_payload_or_imported_helper_or_executed_business'):assert b[k]is False
for k in('future_Root_report_pin','future_Root_tools_pin','future_independent_post_pin','future_independent_post_tools_pin'):assert b[k]is None
retained=b['retained_current7_pins']+b['retained_archive_metadata_current7_pins']+b['explicit_cumulative_metadata_file_pins']+b['retained_B2_current_epoch_readonly_pins'];failed=b['retained_failed_v1_current7_only_pins']+b['retained_failed_pool_archive_current7_only_pins'];assert len(failed)==15 and all(set(p)==ONLY for p in failed)
for _ in range(2):
 for row in rows:
  q=Path(row['historical_full_pin']['path']);st=q.lstat();assert ids(st)==row['expected_start_current7']and stat.S_ISREG(st.st_mode)and st.st_nlink==1 and st.st_uid==os.getuid()and not any(x.is_symlink()for x in(q,*q.parents))
 for p in retained+failed+producer_metadata:current(p)
 for p in b['exact59_historical_absent_pins']:assert not os.path.lexists(p['path'])and not any(x.is_symlink()for x in Path(p['path']).parents)
keys={n.slice.value for n in ast.walk(ast.parse(source))if isinstance(n,ast.Subscript)and isinstance(n.value,ast.Name)and n.value.id=='b'and isinstance(n.slice,ast.Constant)and type(n.slice.value)is str};assert keys<=set(b)
for term in("os.O_EXCL|os.O_NOFOLLOW","claim_before_helpers_or_payload_IO=True","while block:=os.read(fd,CHUNK):checkpoint();h.update(block);n+=len(block)","ids(os.fstat(fd))==before","n==oldpin['size_bytes']","h.hexdigest()==oldpin['sha256']","last=time.monotonic()","time.monotonic()-last>=5","f.truncate(0)","report['final_report_resource_check_passed']=True","512*2**20","time.monotonic()-started<600","8*2**20"):
 assert term in source
assert source.index('ROOT_CURRENT_EPOCH_BINDING_ONCE_CLAIM.json')<source.index("latest_retirement_pins=admit_latest_native_retirement(b)")<source.index("build=meta(")and 'os.unlink('not in source
cli=meta(a['Root_CLI_NULL_peer_template_pin']);assert cli['source_pin']==sp and cli['binding_pin']==bp and cli['expected_Source_review_schema']=='INDEPENDENT_SOURCE_ONLY_A1_A3_FORMAL13_EPOCH_BRIDGE_REVIEW_V1'and cli['expected_Source_review_status']=='PASS_SOURCE_ONLY_A1_A3_SELECTED18_FORMAL13_CURRENT_EPOCH_BLIND_BINDING_V1'and cli['only_two_exact_future_Source_peer_placeholders_may_be_replaced']is True
for p in(sp,bp,ap):full(p)
r=dict(schema='INDEPENDENT_SOURCE_ONLY_A1_A3_FORMAL13_EPOCH_BRIDGE_REVIEW_V1',status='PASS_SOURCE_ONLY_A1_A3_SELECTED18_FORMAL13_CURRENT_EPOCH_BLIND_BINDING_V1',failure=None,source_only=True,source_pin=sp,binding_pin=bp,author_freeze_pin=ap,whole_old_Source_inverse_pin=a['whole_old_Source_inverse_pin'],whole_old_Source_inverse_and_old_producer_function_and31_blind_loop_verified=True,actual_latest_native10_retirement_closure_pins=cp,actual_R10_Root0_independent_post0_and_exact59_historical_absence_verified=True,selected_role_count=31,selected_A1_A3_role_count=18,selected_formal_role_count=13,selected_recorded_bytes=680089850,ordered_role_specs=rows,historical_metadata_fullSHA_and_old_terminal0_four_watchdog0_facts_verified=True,historical_independent_actual_success_raw_missing_and_not_fabricated=['A1','A3'],A1_Source_review_not_promoted_to_actual_post=True,A3_saved_report_and_durable_copy_handoff_not_promoted_to_genuine_raw=True,all31_current_stat7_only_twice_historical_six_nondevice_fields_preserved=True,no_new_epoch_fullPF_or_SHA_proof_minted_by_Source_review=True,complete_joint_roots=roots,original_caps=caps,Source_bound_bytes=8*2**20,no_new_data_owning_root=True,claim_before_helpers_payload_and_per_chunk_SELF_PS_resources_fullscope_verified=True,all_transitive_historical_fixed_inputs_recertified=False,new_B_bearing_context_compatibility_or_lineage_proved=False,online_BOOT_qualified=False,candidate_or_helper_or_PS_lsof_executed=False,native_SQL_pool_gzip_or_scientific_payload_body_opened_or_hashed=False,files_deleted=False,compiler_executed=False,native_executed=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
q=BASE/'REVIEW.json';assert not q.exists();raw=(json.dumps(r,indent=2)+'\n').encode();assert sum(q.stat().st_size for q in D.rglob('*')if q.is_file())+len(raw)<8*2**20;q.write_bytes(raw);print(json.dumps(dict(status=r['status'],review_pin=pin(q))))
