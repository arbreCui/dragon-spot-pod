"""Independent five-file Source review. No candidate/helper imports or payload IO."""
import ast,hashlib,json,os,resource,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
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

def unique(rows):
 table={}
 for p in rows:
  key=p['path'];need(key not in table or table[key]==p,'one exact PF per metadata path');table[key]=p
 return list(table.values())

def function_whole(text,name):
 node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)and n.name==name)
 return ''.join(text.splitlines(keepends=True)[node.lineno-1:node.end_lineno])

def main():
 pa=pin(PACKAGE/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json');need(pa['sha256']=='ac2c41f3cf600dce9106cf28dfe454030bad9a4b5ab84a77e619751d69013ceb'and pa['size_bytes']==6063,'exact pre-GEN separate author freeze');author=meta(pa)
 pr=pin(PACKAGE/'SOURCE_REVIEW_READY.json');need(pr['sha256']=='54a8e643e23be6ea45d2ba279cf862a4719500a055f088661a16a33fc0e0c82b'and pr['size_bytes']==6690,'exact actual ready');ready=meta(pr)
 pg=pin(PACKAGE/'ROOT_SOURCE_PREPARATION_TRUE_TOOL_RETURNS.json');need(pg['sha256']=='57613edd5249ca6a1cd8249f5881a75ae1c98c3005c4ddc4b9254187c51aace0'and pg['size_bytes']==2079,'exact genuine generation raw');gen=meta(pg);genuine(gen,'actual_Source_preparation_return',pr,'ready_pin')
 need(gen['actual_Source_preparation_permission_mode']=='require_escalated'and gen['actual_retried']is False and author['Source_only_frozen_before_Root_generation']is True and author['Source_preparer_or_publisher_executed_by_author']is False and author['product_byte_IO_gzip_or_compiler_executed_by_author']is False,'Source-only author and one true RootGEN0, no actual archive claim')
 table=ready['complete_source_file_pins'];need(len(table)==len({p['path']for p in table})==5 and table==author['whole_Source_file_pins']and ready['schema']=='CURRENT_B2_SINGLE_PHYSICAL_DIRECTORY_ARCHIVE_SOURCE_REVIEW_READY_V1'and ready['source_only']is True and ready['product_payload_opened']is False and ready['gzip_executed']is False,'entire five-Source table identical')
 texts={}
 for p in table:
  q=full(p);texts[q.name]=q.read_text();ast.parse(texts[q.name]);full(p)
 pb=ready['execution_binding_pin'];plan=meta(pb);pbound=ready['Root_completed_admission_binding_pin'];bound=meta(pbound);need(pbound==author['final_admission_binding_pin'],'same author final actual binding')
 template=meta(author['whole_NULL_admission_binding_template_pin']);mutable=set(author['Root_final_binding_fields_filled_after_genuine_comparison0']);need(set(bound)==set(template)and all(bound[k]==v for k,v in template.items()if k not in mutable),'only declared actual binding slots filled')
 added={'Source_only_current_cumulative_bytes_before_reservations','Source_generation_product_payload_opened','Source_generation_gzip_executed'};need(set(plan)==set(bound)|added and all(plan[k]==v for k,v in bound.items())and plan['Source_generation_product_payload_opened']is False and plan['Source_generation_gzip_executed']is False,'GEN only adds true stat snapshot; no scopes or counters rewritten')
 static=meta(author['source_static_evidence_pin']);original=static['original48_Source_pin'];old=full(original).read_text();arch=texts['archive_single_B2_physical_directory_slots.UNREADY.py'];oldfn=function_whole(old,'archive_one');newfn=function_whole(arch,'archive_one')
 need(newfn==oldfn and len(newfn.encode())==2311 and hashlib.sha256(newfn.encode()).hexdigest()=='db8a6b9fe2234c77f460274fe3d73d5fe43377089ef8341c305b8b20da892495','original48 archive_one wholebytes; every original/compressed/decompressed byte proof unchanged')
 caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
 need(plan['original_caps']==author['original_caps']==ready['original_caps']==caps and plan['schema']=='CURRENT_B2_SINGLE_PHYSICAL_DIRECTORY_LOSSLESS_ARCHIVE_BINDING_V1'and plan['prerequisite_binding_complete']is True and plan['draft_unready']is False and plan['Source_admission_ready']is False,'original caps and exact Source-only archival admission')
 h=meta(plan['actual_comparison_Host_report_pin']);raw=meta(plan['actual_comparison_Root_tools_pin']);post=meta(plan['actual_comparison_post_pin']);posttools=meta(plan['actual_comparison_post_tools_pin']);child=meta(plan['actual_comparison_child_report_pin']);prior=meta(plan['latest_complete_plan_pin']);genuine(raw,'actual_terminal_return',plan['actual_comparison_Host_report_pin'],'report_pin');genuine(posttools,'actual_review_return',plan['actual_comparison_post_pin'],'review_pin')
 need(h['status']=='ACTUAL_CURRENT_B55_NATIVEWARM_B2_COMPLETE_COMPARISON_EVIDENCE_CHILD2_CLOSED_ONLY'and h['failure']is None and h['complete_typed_word_comparison_completed']is True and h['final_report_resource_check_passed']is True and type(h['actual_child_integer_exit_code'])is int and h['actual_child_integer_exit_code']==2 and h['records'][0]['status']=='FAILED'and h['records'][0]['error']==h['original_runner_error']=='own-child stage failed; no retry'and h['control_plan_pin']==plan['latest_complete_plan_pin']and h['actual_child_report_pin']==plan['actual_comparison_child_report_pin'],'real v2 Root0 and expected original child2 FAILED/error preserved')
 need(post['schema']=='RECORDED_CURRENT_B55_NATIVEWARM_B2_COMPLETE_TYPED_COMPARISON_METADATA_POSTVERIFY_V2'and post['status']=='PASS_ACTUAL_CURRENT_B55_B2_COMPLETE_TYPED_COMPARISON_V2_ROOT0_CHILD2_METADATA_ONLY_DIFFERENCES_RECORDED'and post['failure']is None and post['actual_Host_report_pin']==plan['actual_comparison_Host_report_pin']and post['actual_Root_tools_pin']==plan['actual_comparison_Root_tools_pin']and post['actual_child_report_pin']==plan['actual_comparison_child_report_pin']and post['actual_Root_integer_exit_code']==0 and post['actual_child_integer_exit_code']==2,'real independent actual comparison metadata post0 identity')
 counts={k:child[k]for k in('compared_all_macro_records','compared_original_payload_words','raw_word_mismatches','metadata_mismatches')};need(counts==plan['actual_comparison_counts']==post['actual_comparison_counts']==dict(compared_all_macro_records=19620,compared_original_payload_words=2264152,raw_word_mismatches=0,metadata_mismatches=0)and child['path_sets_equal']is True and post['actual_exact_inventory_metadata_and_all_words_equal']is True,'real complete19620/all2264152 words and actual double0, not inferred equality')
 target=plan['actual_physical_directory_original_pin'];extractpost=meta(prior['actual_B2_complete_extraction_post_pin']);genuine(meta(prior['actual_B2_complete_extraction_post_tools_pin']),'actual_review_return',prior['actual_B2_complete_extraction_post_pin'],'review_pin');need(plan['all1_plain_pins']==[target]and target==extractpost['complete_physical_directory_slots_pin']and target['size_bytes']==plan['original_plain_total_bytes']==34371817 and target['sha256']=='b9b72ad2f281ca6b4c881fc3734412f68debcdd80ff03ceec4372b02786b4c60','only exact complete B2 physical directory ledger, original kept through this archive stage')
 failed=plan['retained_failed_v1_current7_only_pins'];ordinary=[q for q in prior['retained_current7_pins']if set(q)=={'path','sha256','size_bytes','identity'}];need(len(failed)==8 and failed==prior['retained_failed_v1_current7_only_pins']==post['retained_failed_v1_current7_only_pins']and [q for q in prior['retained_current7_pins']if q not in ordinary]==failed and all(set(q)=={'path','size_bytes','identity'}for q in failed),'all eight failed-v1 roles remain exactly current7-only; no invented SHA or fullPF')
 need(plan['prior_failed_v1_closure_pins']==post['prior_failed_v1_closure_pins']=={k:prior[k]for k in('actual_failed_v1_plan_pin','actual_failed_v1_Host_report_pin','actual_failed_v1_Root_tools_pin','actual_failed_v1_post_pin','actual_failed_v1_post_tools_pin','actual_failed_v1_final_CLI_pin')}and post['prior_v1_Root1_child_minus15_unknown_counts_equality_preserved']is True and post['prior_v1_partial_payload_body_not_opened_or_hashed_by_post']is True,'prior actual Root1/child-15/failurepost0 and unknown counts not overwritten by v2 success')
 expected=unique(ordinary+prior['retained_B2_current_epoch_readonly_pins']+post['new_complete_output_full_pins']);need(target in expected and plan['retained_current7_pins']==[p for p in expected if p!=target]and plan['retained_B2_current_epoch_readonly_pins']==prior['retained_B2_current_epoch_readonly_pins'],'all SQL/pools/native/other outputs and cold9 retained; target alone separated for archive')
 hf=meta(h['host_freeze_pin']);proofs=[plan[k]for k in('latest_complete_plan_pin','actual_comparison_Host_report_pin','actual_comparison_Root_tools_pin','actual_comparison_child_report_pin','actual_comparison_post_pin','actual_comparison_post_tools_pin')]+[h['host_freeze_pin'],h['source_freeze_pin'],prior['actual_B2_complete_extraction_post_pin'],prior['actual_B2_complete_extraction_post_tools_pin']];need(plan['base_explicit_cumulative_metadata_file_pins']==prior['explicit_cumulative_metadata_file_pins']and plan['explicit_cumulative_metadata_file_pins']==unique(prior['explicit_cumulative_metadata_file_pins']+hf['explicit_cumulative_metadata_file_pins']+proofs),'complete exact inherited+comparison metadata union, no roles omitted')
 roots=plan['complete_joint_roots'];out=Path(plan['planned_actual_output_root']);need(len(roots)==80 and roots[:-1]==plan['inherited_latest_complete_joint_roots']==prior['complete_joint_roots']==h['complete_joint_roots']and len(set(roots))==80 and roots[-1]==str(out)and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b)and not os.path.lexists(out)and any(PACKAGE.is_relative_to(Path(r))for r in roots[:-1]),'full original79 plus exactly fresh owning archive80, Source counted and no action started')
 need(plan['bounded_total_output_bytes']==8*2**20 and plan['bounded_archive_payload_bytes']==4*2**20 and plan['metadata_runtime_headroom_bytes']==4*2**20 and plan['bounded_Source_metadata_bytes']==16*2**20 and plan['future_consumer_must_use_exact_single_B2_physical_directory_archive_mapping']is True and plan['original_plain_retirement_in_this_stage']is False and plan['generic_missing_path_skip_authorized']is False and plan['compression_ratio_or_success_assumed']is False,'whole8=4payload+4meta and Source16 hard bounds; no delete/ratio/decoder or missing skip')
 build=meta(plan['original_guard_build_plan_pin']);retained=[target]+plan['retained_current7_pins']+plan['retained_B2_current_epoch_readonly_pins'];metadata=plan['explicit_cumulative_metadata_file_pins']
 need(not{p['path']for p in plan['retained_B2_current_epoch_readonly_pins']}&{p['path']for p in metadata},'nine large cold inputs not ordinary external metadata')
 for _ in range(2):
  for p in retained:current(p)
  for p in failed:need(set(p)=={'path','size_bytes','identity'},'failed row exact schema');current(p)
  for p in metadata:current_role(p,build)
 source_common=texts['B2_physical_directory_archive_common.UNREADY.py'];source_host=texts['run_guarded_single_B2_physical_directory_archive.UNREADY.py'];source_pub=texts['publish_single_B2_physical_directory_archive_CLI.UNREADY.py']
 for token in('current_failed_v1(p,self.binding)','self.joined.check()','self.history.check()','source_module(binding[\'original_production_inputs_Source_pin\']','s.st_nlink==0','20971764748') :need(token in source_common,'reviewed complete original resources path '+token)
 for token in("claim_before_metadata_or_result_body_IO=True","c.original_resource_modules(b)","helper.guard_admission(full)","full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)","runner=full.OwnRSSSerialExecutor(","runner.execute(stage,","runtime/'run_bounded_dragon.py'","resources.check()") :need(token in source_host,'reviewed claim/preload/original ownRSS/once child route '+token)
 need('os.unlink'not in arch+source_host and 'result_values_decoded=False'in arch and "compresslevel=6,mtime=0"in arch and 'self.resources.light()'in arch and 'self.c.ARCHIVE_CAP'in arch,'archive-only one serial stream, guards per chunk/write, original never deleted or decoded')
 need("PASS_SOURCE_ONLY_CURRENT_SINGLE_B2_PHYSICAL_DIRECTORY_LOSSLESS_ARCHIVE"in source_pub and "review['binding_pin']==ready['execution_binding_pin']"in source_pub and "review['complete_source_file_pins']==ready['complete_source_file_pins']"in source_pub,'publisher exact independent Source0 gate/schema')
 joint=counted_bytes(roots);external=sum(p['size_bytes']for p in metadata if not any(Path(p['path']).is_relative_to(Path(r))for r in roots));unlinked=unlinked_bytes();need(joint+external+unlinked+24*2**20<2*2**30,'fresh full80 stat scope plus entire8+Source16 within original2GiB; Root still must run original resource classes')
 for p in table:full(p)
 report=dict(schema='INDEPENDENT_CURRENT_SINGLE_B2_PHYSICAL_DIRECTORY_ARCHIVE_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_CURRENT_SINGLE_B2_PHYSICAL_DIRECTORY_LOSSLESS_ARCHIVE',source_only=True,failure=None,reviewer_task='/root/b2_build_source_peer',Source_author_task='/root/b_capture_source_peer',binding_pin=pb,complete_source_file_pins=table,actual_READY_pin=pr,actual_GEN_true_tools_pin=pg,Source_author_freeze_pin=pa,Root_completed_admission_binding_pin=pbound,whole_original48_archive_one_Source_pin=original,whole_original48_archive_one_bytes=2311,whole_original48_archive_one_SHA=hashlib.sha256(newfn.encode()).hexdigest(),original48_archive_one_wholebytes_equal=True,complete_joint_roots=roots,original_caps=caps,stage_total_output_bytes=8*2**20,stage_payload_bytes=4*2**20,stage_runtime_metadata_headroom_bytes=4*2**20,stage_Source_metadata_bound_bytes=16*2**20,actual_compare_counts=counts,actual_v2_Root0_child2_FAILED_and_double0_independent_post0_bound=True,prior_v1_Root1_child_minus15_unknown_counts_equality_and_failed8_current7_only_preserved=True,only_original_target_full_pin=target,all_SQL_pool_and_other_current7_outputs_retained=True,ordinary_retainer_role_count=len(plan['retained_current7_pins']),failed_v1_current7_only_role_count=len(failed),cold_readonly_role_count=9,complete_explicit_metadata_role_count=len(metadata),all_retained_roles_current7_verified_twice=True,original_claim_preload_PrivateOwnRSS_MRO_bounded_watchdog_and_caps_preserved=True,fresh_Source_only_stat_joint_bytes=joint,fresh_Source_only_stat_external_metadata_bytes=external,fresh_Source_only_open_unlinked_bytes=unlinked,fresh_remaining_after8_andSource16=2*2**30-joint-external-unlinked-24*2**20,Root_original_resource_classes_must_recheck_before_actual_IO=True,GEN_is_not_actual_archive_or_retirement=True,candidate_or_helpers_imported=False,compiler_or_native_or_scientific_code_executed=False,SQL_pool_JSONL_or_gzip_body_read=False,target_or_old_payload_SHA_read=False,gzip_executed=False,worker_executed=False,publisher_executed=False,files_deleted=False,plain_retirement_authorized=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,reviewer_Source_pin=pin(Path(__file__).absolute()))
 raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(counted_bytes([str(PACKAGE)])+len(raw)<16*2**20 and joint+external+unlinked+len(raw)<2*2**30,'review itself counted withinSource16 and complete joint2GiB')
 q=BASE/'REVIEW.json'
 with q.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 print(json.dumps(dict(status=report['status'],review_pin=pin(q))),flush=True)

if __name__=='__main__':main()
