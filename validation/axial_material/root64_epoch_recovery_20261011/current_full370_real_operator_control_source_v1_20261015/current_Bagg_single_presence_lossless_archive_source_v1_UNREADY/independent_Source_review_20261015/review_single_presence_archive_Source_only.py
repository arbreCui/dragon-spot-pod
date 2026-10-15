"""Independent metadata and Source-only single presence archive review."""
import ast,hashlib,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent;D=BASE.parent
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();assert ids(s)==p['identity']and s.st_size==p['size_bytes']and stat.S_ISREG(s.st_mode)and q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents));return q

def full(p):
 q=current(p);assert p['size_bytes']<8*2**20;raw=q.read_bytes();assert hashlib.sha256(raw).hexdigest()==p['sha256'];current(p);return raw

def read(p):
 v=json.loads(full(p));full(p);return v

def pin(p):
 s=p.stat();raw=p.read_bytes();return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=s.st_size,identity=ids(s))

def zero(p,key,field,want):
 v=read(p);r=v[key];assert v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==0 and type(r['exit_code'])is int and r['exit_code']==0 and r.get('session_id')is None and json.loads(r['output'].splitlines()[-1])[field]==want;return v

def unique(rows):
 t={}
 for p in rows:assert p['path']not in t or t[p['path']]==p;t[p['path']]=p
 return list(t.values())

def segment(text,name):
 node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)and n.name==name);return ''.join(text.splitlines(keepends=True)[node.lineno-1:node.end_lineno])

authorpin=pin(D/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json');a=read(authorpin);ready_pin=pin(D/'SOURCE_REVIEW_READY.json');ready=read(ready_pin);pg=pin(D/'ROOT_SOURCE_PREPARATION_TRUE_TOOL_RETURNS.json');gen=zero(pg,'actual_Source_preparation_return','ready_pin',ready_pin)
assert ready_pin['sha256']=='69836f2c80334844df504e062f2048d13f2a5efd62e7dfece246ea7a96b934b8'and pg['sha256']=='c90da721791ff8a44847361162a182f8d392541e6a118916713ec4d57628543d'and gen['actual_Source_preparation_return']['chunk_id']=='2b8712'and gen['generation_retried']is False and gen['product_payload_opened']is gen['gzip_executed']is False
assert a['Source_only_frozen_before_Root_generation']is True and a['author_STOP_WRITES_to_core']is True and a['Source_preparer_or_publisher_executed_by_author']is False and a['product_byte_IO_gzip_or_compiler_executed_by_author']is False
assert ready['schema']=='CURRENT_BAGG_SINGLE_PRESENCE_ARCHIVE_SOURCE_REVIEW_READY_V1'and ready['source_only']is True and ready['complete_source_file_pins']==a['whole_Source_file_pins']and len(a['whole_Source_file_pins'])==5
sources={}
for p in ready['complete_source_file_pins']:raw=full(p);full(p);sources[Path(p['path']).name]=raw.decode();ast.parse(raw)
pp=ready['execution_binding_pin'];p=read(pp);inputpin=ready['Root_completed_admission_binding_pin'];binding=read(inputpin);template=read(a['whole_NULL_admission_binding_template_pin']);mutable=a['Root_final_binding_fields_filled_after_genuine_bridge0'];assert len(mutable)==7 and set(binding)==set(template)and all(binding[k]==v for k,v in template.items()if k not in mutable)
extra={'Source_only_current_cumulative_bytes_before_reservations','Source_generation_product_payload_opened','Source_generation_gzip_executed'};assert set(p)==set(binding)|extra and all(p[k]==v for k,v in binding.items())and p['Source_generation_product_payload_opened']is p['Source_generation_gzip_executed']is False
assert p['prerequisite_binding_complete']is True and p['draft_unready']is False and p['Source_admission_ready']is False and p['actual_current_epoch_B2_bridge_closed0_bound']is True
bridge=read(p['actual_current_epoch_B2_bridge_report_pin']);bt=zero(p['actual_current_epoch_B2_bridge_tools_pin'],'actual_terminal_return','report_pin',p['actual_current_epoch_B2_bridge_report_pin']);assert bt['actual_execution_permission_mode']=='require_escalated'and bridge['schema']=='ROOT_NATIVE_WARM_B2_CURRENT_EPOCH_BLIND_FULLFILE_BINDING_REPORT_V1'and bridge['status']=='PASS_B2_SELECTED_READONLY_ROLES_CURRENT_EPOCH_BLIND_SHA_ONLY'and bridge['failure']is None
assert p['explicit_cumulative_metadata_file_pins']==unique(p['base_explicit_cumulative_metadata_file_pins']+bridge['explicit_cumulative_metadata_file_pins']+[p['actual_current_epoch_B2_bridge_report_pin'],p['actual_current_epoch_B2_bridge_tools_pin']])and len(p['explicit_cumulative_metadata_file_pins'])==1042
old=read(p['latest_complete_plan_pin']);roots=p['complete_joint_roots'];assert p['inherited_latest_complete_joint_roots']==old['complete_joint_roots']==bridge['complete_joint_roots']and roots==old['complete_joint_roots']+[p['planned_actual_output_root']]and len(roots)==len(set(roots))==76
assert all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)and any(D.is_relative_to(Path(r))for r in roots)
assert p['original_caps']==ready['original_caps']==bridge['original_caps']==old['original_caps']and p['bounded_total_output_bytes']==32*2**20 and p['bounded_archive_payload_bytes']==24*2**20 and p['metadata_runtime_headroom_bytes']==8*2**20 and p['bounded_Source_metadata_bytes']==16*2**20 and p['Source_only_current_cumulative_bytes_before_reservations']+48*2**20<2*2**30
h=read(p['actual_Bagg_Host_report_pin']);post=read(p['actual_Bagg_post_pin']);child=read(p['actual_Bagg_child_report_pin']);zero(p['actual_Bagg_Root_tools_pin'],'actual_terminal_return','report_pin',p['actual_Bagg_Host_report_pin']);zero(p['actual_Bagg_post_tools_pin'],'actual_review_return','review_pin',p['actual_Bagg_post_pin'])
assert h['status']=='ACTUAL_CURRENT_B_COMPLETE_AGGREGATE_EVIDENCE_CHILD2_CLOSED_ONLY'and h['failure']is None and h['actual_child_integer_exit_code']==2 and h['records'][0]['status']=='FAILED'and h['original_runner_error']==h['records'][0]['error']=='own-child stage failed; no retry'and h['B_six_phase_construction_completed']is True and h['final_report_resource_check_passed']is True
assert post['status']=='PASS_ACTUAL_CURRENT_B_FULL8_SNAPSHOT55_CONTEXT_SIXPHASE_CONSTRUCTION_EVIDENCE_CHILD2_METADATA_ONLY'and post['actual_Host_report_pin']==p['actual_Bagg_Host_report_pin']and post['actual_child_report_pin']==p['actual_Bagg_child_report_pin']and post['actual_Root_integer_exit_code']==0 and post['actual_child_integer_exit_code']==2
original=p['actual_presence_original_pin'];assert p['all1_plain_pins']==[original]and original['size_bytes']==p['original_plain_total_bytes']==169615994 and original in child['states'][0]['complete_output_file_pins']and original in post['all_new_output_blind_fullEOF_SHA_current7_twice_pins']and Path(original['path']).name=='all_presence_branch_and_missing.jsonl'
assert p['retained_Bagg_output_current7_pins']==[q for q in post['all_new_output_blind_fullEOF_SHA_current7_twice_pins']if q!=original]and len(p['retained_Bagg_output_current7_pins'])==16
life=old['exact_B4_product_lifecycle_binding'];assert p['retained_native_current7_pins']==life['ordered_exact4_current_archive_pins']+life['ordered_exact4_current_entry_pins']+[life['complete4_archive']['index_pin']]+old['prospective_worker_live_input_pins']and p['retained_current7_pins']==unique(p['retained_Bagg_output_current7_pins']+p['retained_native_current7_pins'])
for row in p['all1_plain_pins']+p['retained_current7_pins']+p['explicit_cumulative_metadata_file_pins']:current(row)
assert p['future_consumer_must_use_exact_single_presence_archive_mapping']is True and p['original_plain_retirement_in_this_stage']is False and p['generic_missing_path_skip_authorized']is False and p['compression_ratio_or_success_assumed']is False and p['future_B2_extraction_budget_admitted']is False
s=read(a['whole_static_evidence_pin']);oldworker=full(s['original48_worker_Source_pin']).decode();full(s['original48_worker_Source_pin']);one=segment(sources['archive_single_Bagg_presence.UNREADY.py'],'archive_one');assert one==segment(oldworker,'archive_one')and hashlib.sha256(one.encode()).hexdigest()==a['original48_archive_one_SHA256']=='db8a6b9fe2234c77f460274fe3d73d5fe43377089ef8341c305b8b20da892495'
common=sources['presence_archive_common.UNREADY.py'];originalcommon=full(s['whole_B4v1_original_common_Source_pin']).decode()
for name in s['whole_unchanged_common_functions']:assert segment(common,name)==segment(originalcommon,name)
assert 'OUT_CAP=32*2**20'in common and 'ARCHIVE_CAP=24*2**20'in common and 'SOURCE_CAP=16*2**20'in common
host=sources['run_guarded_single_Bagg_presence_archive.UNREADY.py'];assert host.index("with claim.open('x')")<host.index('c=bootstrap(')<host.index('resources=c.Resources(')<host.index('runner=full.OwnRSSSerialExecutor(')and 'full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)'in host
for text in sources.values():assert not any(x in text for x in('os.unlink(','os.remove(','shutil.rmtree('))
for q in ready['complete_source_file_pins']:full(q);full(q)
r=dict(schema='INDEPENDENT_SINGLE_BAGG_PRESENCE_ARCHIVE_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_CURRENT_SINGLE_BAGG_PRESENCE_LOSSLESS_ARCHIVE',failure=None,source_only=True,binding_pin=pp,complete_source_file_pins=ready['complete_source_file_pins'],Root_completed_admission_binding_pin=inputpin,actual_Source_generation_tools_pin=pg,actual_Source_generation_return_integer=0,actual_Source_generation_terminal_chunk='2b8712',author_Source_freeze_pin=authorpin,complete_prefix_root_count=76,original_caps=p['original_caps'],bounded_total_output_bytes=32*2**20,bounded_archive_payload_bytes=24*2**20,bounded_runtime_metadata_headroom_bytes=8*2**20,bounded_Source_metadata_bytes=16*2**20,Source_only_existing_measured_bytes=p['Source_only_current_cumulative_bytes_before_reservations'],exact_complete_presence_pin=original,other16_Bagg_outputs_and_all_input_native_archive_entry_index_current7_preserved=True,complete_bridge_explicit_metadata_union_count=1042,bridge_Root0_actual_report_pin=p['actual_current_epoch_B2_bridge_report_pin'],old48_archive_one_whole_function_bytes_exact=True,original_OwnRSS_private_class_and_MRO_preserved=True,claim_precedes_helpers_and_payload=True,original_Bagg_Root0_evidence_child2_FAILED_error_preserved=True,Source_or_GEN_or_pub_or_gzip_or_helper_executed_by_reviewer=False,target_or_gzip_or_old_science_body_read_or_hashed=False,files_deleted=False,original_plain_retirement_authorized=False,compression_success_assumed=False,future_B2_extraction_budget_admitted=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
f=BASE/'REVIEW.json';assert not f.exists();f.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(dict(status=r['status'],review_pin=pin(f))))
