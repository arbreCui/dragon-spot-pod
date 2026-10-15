"""Independent Source/meta/current7 review; no publisher/worker/helper execution."""
import ast, hashlib, json, os, pathlib, stat
HERE=pathlib.Path(__file__).absolute().parent
BASE=HERE.parent
def ids(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=pathlib.Path(p['path']);s=q.lstat()
 assert q.is_absolute()and stat.S_ISREG(s.st_mode)and ids(s)==p['identity']and s.st_size==p['size_bytes']
 assert not any(x.is_symlink()for x in(q,*q.parents))
 return q
def small(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_size<8*1024*1024
 raw=p.read_bytes();h=hashlib.sha256(raw).hexdigest();assert h==hashlib.sha256(p.read_bytes()).hexdigest()and ids(s)==ids(p.lstat())
 return raw,dict(path=str(p),sha256=h,size_bytes=s.st_size,identity=ids(s))
def meta(p):
 raw,pf=small(pathlib.Path(p['path']));assert pf==p;return json.loads(raw)
def genuine(v,key,code,chunk,role=None,pf=None):
 t=v[key];assert v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==code
 assert type(t['exit_code'])is int and t['exit_code']==code and 'session_id'not in t and t['chunk_id']==chunk
 if role is not None:assert json.loads(t['output'].strip().splitlines()[-1])[role]==pf
def inverse(text,rows):
 for row in reversed(rows):
  n=row['replacement_character_offset'];old=row['old_literal'];new=row['new_literal']
  assert text[n:n+len(new)]==new
  text=text[:n]+old+text[n+len(new):]
 return text
def matches(text,p):
 raw=text.encode();assert len(raw)==p['size_bytes']and hashlib.sha256(raw).hexdigest()==p['sha256']
def main():
 ar,ap=small(BASE/'AUTHOR_SOURCE_FREEZE.json');assert ap['sha256']=='327b0ec8741cbeeba02a79643af0d141e9d42426f7ea72072ef9480e3b19ea1e'and ap['size_bytes']==19698
 a=json.loads(ar);assert a['schema']=='CURRENT_B4_EXACT2_RECOVERY_AUTHOR_SOURCE_FREEZE_V1'and a['source_only']is True and a['author_STOP_WRITES']is True
 pp=a['whole_plan_pin'];plan=meta(pp);assert pp['sha256']=='9da059569cbf23000829213e600172b31d0856c9c77637787113d227f643fb5a'and pp['size_bytes']==542359
 pins=a['whole_Source_file_pins'];assert len(pins)==2
 texts=[]
 for p in pins:
  raw,actual=small(pathlib.Path(p['path']));assert actual==p;source=raw.decode();ast.parse(source);texts.append(source)
 assert pins[0]['sha256']=='279a1190dfdff1ee308dad9a94c506d14a79a0ea8cee02ed0a12b531175d40ff'
 assert pins[1]['sha256']=='e8b5373bfd85a3cc050a0d8038d5f6f1f68f3272a7e5b368e5037eb9fe61e405'
 meta(a['reviewable_CLI_template_pin']);meta(a['static_evidence_pin'])
 chain=[meta(p)for p in a['whole_inverse_chain_pins']];assert len(chain)==3
 current_texts=texts[:];restored=[]
 for step,(new_key,old_key,rows_key)in zip(chain,[('after_Source_pins','before_Source_pins','exact_literal_offset_replacements'),('new_Source_pins','parent_Source_pins','exact_literal_replacements'),('new_Source_pins','original_Source_pins','exact_forward_literal_replacements')]):
  assert len(step[new_key])==len(step[old_key])==2
  for i in range(2):
   matches(current_texts[i],step[new_key][i]);name=pathlib.Path(step[new_key][i]['path']).name
   current_texts[i]=inverse(current_texts[i],step[rows_key][name]);matches(current_texts[i],step[old_key][i])
  restored.append(step[old_key])
 for i,p in enumerate(chain[-1]['original_Source_pins']):
  original,pf=small(pathlib.Path(p['path']));assert pf==p and current_texts[i].encode()==original
 caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
 archive=meta(plan['inherited_complete_archive_plan_pin']);roots=plan['complete_joint_roots']
 assert plan['schema']=='CURRENT_B4_EXACT2_PARTIAL_ARCHIVE_RECOVERY_PLAN_V1'and plan['Source_admission_ready']is True and plan['draft_unready']is False
 assert roots==plan['actual_archive_complete_prefix']==archive['complete_joint_roots']and len(roots)==len(set(roots))==73
 assert not any(pathlib.Path(x).is_relative_to(pathlib.Path(y))for x in roots for y in roots if x!=y)
 assert any(BASE.is_relative_to(pathlib.Path(x))for x in roots)and plan['no_new_output_root']is True and plan['original_caps']==archive['original_caps']==caps
 targets=plan['exact_target_pins'];assert targets==a['exact_target_pins']and len(targets)==2 and targets[0]==archive['all4_product_pins'][0]
 assert [p['size_bytes']for p in targets]==[76594248,25099039]and sum(p['size_bytes']for p in targets)==plan['planned_released_bytes']==plan['target_total_bytes']==101693287
 assert pathlib.Path(targets[0]['path']).name=='m.xsm'and targets[1]['path']==str(pathlib.Path(archive['planned_actual_output_root'])/'archives/001_u.asc.gz')
 cp=plan['actual_failed_archive_closure_pins'];d={k:meta(p)for k,p in cp.items()}
 genuine(d['Root_tools'],'actual_terminal_return',1,'434819')
 genuine(d['post_tools'],'actual_review_return',0,'f67eab','review_pin',cp['post'])
 assert d['Root_tools']['exact_executed_command']==meta(plan['actual_failed_archive_published_CLI_pin'])['command']
 assert d['Host']['status']=='FAILED_ARCHIVE_NO_RETRY_ALL_ORIGINALS_RETAINED'and d['Host']['actual_watchdog']is None and d['Host']['actual_child_receipt']is None and d['Host']['archive_complete']is False
 assert d['post']['actual_recorded_child_integer_exit_codes']==[]and d['post']['actual_Root_integer_exit_code']==1
 assert type(d['watchdog']['returncode'])is int and d['watchdog']['returncode']==1 and d['watchdog']['limit_failure']is None
 assert d['first_failure']['phase']=='ARCHIVE_1'and d['first_failure']['completed_entry_pins']==[plan['retained_member0_entry_pin']]
 partials={p['path']:p for p in d['post']['new_partial_output_blind_fullEOF_twice_pins']};assert targets[1]==partials[targets[1]['path']]
 sup=meta(plan['actual_failure_supplemental_post_pin']);st=meta(plan['actual_failure_supplemental_post_tools_pin']);projection=meta(plan['actual_failure_supplemental_field_projection_pin'])
 genuine(st,'actual_review_return',0,'cd7af3','review_pin',plan['actual_failure_supplemental_post_pin'])
 assert projection['supplement_report_pin']==plan['actual_failure_supplemental_post_pin']and projection['supplement_true_tools_pin']==plan['actual_failure_supplemental_post_tools_pin']
 assert sup['schema']==projection['supplement_schema']and sup['status']==projection['supplement_status']and sup['original_prior_post_recorded_child_integer_exit_codes']==[]and sup['supplemental_actual_recorded_child_integer_exit_codes']==[1]
 entry=meta(plan['retained_member0_entry_pin']);gz=plan['retained_member0_gzip_pin']
 assert sup['recorded_complete_member000']==entry and entry['original_plain_full_pin']==targets[0]and entry['compressed_archive_full_pin']==gz and sup['incomplete_gzip001_current7_only_pin']==targets[1]
 vp=plan['actual_single_member_verification_closure_pins'];v={k:meta(p)for k,p in vp.items()}
 genuine(v['Root_tools'],'actual_terminal_return',0,'5826fd','report_pin',vp['Root_report'])
 genuine(v['post_tools'],'actual_review_return',0,'9345ca','review_pin',vp['post'])
 vr=plan['actual_single_member_Root_key_projection'];pr=plan['actual_single_member_post_key_projection'];root=v['Root_report'];post=v['post']
 assert root['schema']==vr['schema']and root['status']==vr['status']and root['failure']is None and root[vr['entry_pin_field']]==plan['retained_member0_entry_pin']and root[vr['original_pin_field']]==targets[0]and root[vr['gzip_pin_field']]==gz
 assert root[vr['decompressed_SHA_field']]==targets[0]['sha256']and root[vr['decompressed_length_field']]==targets[0]['size_bytes']and root[vr['streamed_complete_field']]is True
 assert post['schema']==pr['schema']and post['status']==pr['status']and post['failure']is None and post[pr['Root_report_pin_field']]==vp['Root_report']and post[pr['Root_tools_pin_field']]==vp['Root_tools']and post[pr['entry_pin_field']]==plan['retained_member0_entry_pin']and post[pr['original_pin_field']]==targets[0]and post[pr['gzip_pin_field']]==gz and post[pr['separate_Root_stream_proof_matched_field']]is True
 assert post['actual_child_integer_exit_code']is None and post['actual_member0_children_started']==0 and post['all4_archive_complete']is False and post['retirement_authorized']is False
 assert plan['retained_other3_original_product_pins']==archive['all4_product_pins'][1:]and len(plan['retained_other3_original_product_pins'])==3
 assert plan['retained_native_current7_pins']==archive['retained_native_current7_pins']and len(plan['retained_native_current7_pins'])==79
 assert plan['original_B_native_and_readonly_input_current7_pins']==archive['original_B_native_and_readonly_input_current7_pins']and len(plan['original_B_native_and_readonly_input_current7_pins'])==11
 retained=plan['retained_other3_original_product_pins']+plan['retained_native_current7_pins']+plan['original_B_native_and_readonly_input_current7_pins']+plan['retained_archive_metadata_current7_pins']+[gz]+plan['explicit_cumulative_metadata_file_pins']
 assert not {p['path']for p in targets}&{p['path']for p in retained}
 for p in retained+targets:
  current(p)
 for p in targets:
  s=pathlib.Path(p['path']).lstat();assert s.st_uid==os.getuid()==501 and s.st_nlink==1
 worker,publisher=texts
 for code in texts:
  assert 'independent_readonly_post0_required_before_execute'in code and "genuine("in code and 'readonly-post-tools'in code
 assert "genuine(checkposttools,'actual_review_return',pcheckpost,'review_pin')"in worker and "genuine(cpt,'actual_review_return',checkpostpin,'review_pin')"in publisher
 for needle in ["['/bin/ps','-o','rss=','-p',str(os.getpid())]","command=['/usr/sbin/lsof','-n','-P','-Fpcfn','--']+[p['path']for p in targets]","r.returncode==1 and r.stdout==b''and r.stderr==b''","os.unlink(q.name,dir_fd=fd);os.fsync(fd)","d['actual_released_pins'].append(p)","budget(True);d['resources_after']=state['latest']","state.update(last=time.monotonic()"]:assert needle in worker
 assert worker.count('os.unlink(')==1 and 'subprocess.Popen'not in worker and 'gzip.'not in worker
 contract=plan['readonly_post_report_contract'];assert contract['schema']=='CURRENT_B4_EXACT2_READONLY_METADATA_POSTVERIFY_V1'and contract['status']=='PASS_CURRENT_B4_EXACT2_READONLY0_NO_UNLINK_METADATA_ONLY'
 assert plan['independent_readonly_post0_required_before_execute']is True and contract['required_actual_released_bytes']==0 and contract['required_files_deleted']is False
 joint=0
 for value in roots:
  rootpath=pathlib.Path(value)
  if not rootpath.exists():continue
  for p in rootpath.rglob('*'):
   s=p.lstat();assert not stat.S_ISLNK(s.st_mode)
   if stat.S_ISREG(s.st_mode):joint+=s.st_size
 extra=sum(p['size_bytes']for p in plan['explicit_cumulative_metadata_file_pins']if not any(pathlib.Path(p['path']).is_relative_to(pathlib.Path(r))for r in roots))
 assert joint+extra+16*1024*1024<2*2**30
 assert not(BASE/'READONLY_RECEIPT.json').exists()and not(BASE/'EXECUTION_RECEIPT.json').exists()
 report=dict(schema='INDEPENDENT_CURRENT_B4_EXACT2_RECOVERY_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_CURRENT_B4_EXACT2_RECOVERY',failure=None,source_only=True,source_pin=pins[0],plan_pin=pp,publisher_Source_pin=pins[1],complete_source_file_pins=pins,author_freeze_pin=ap,independent_reviewer_task='/root/b2_build_source_peer',whole_three_stage_literal_inverse_recovered_exact_old48_two_Source_pins=chain[-1]['original_Source_pins'],whole_inverse_stage_predecessor_pins=restored,exact_target_pins=targets,planned_released_bytes=101693287,all73_original_prefix_and_original_caps_preserved=True,actual_member0_Root0_and_post0_bound=True,actual_member0_Root_tools_pin=vp['Root_tools'],actual_member0_Root_report_pin=vp['Root_report'],actual_member0_post_pin=vp['post'],actual_member0_post_tools_pin=vp['post_tools'],original_all4_Root1_child1_old_post0_empty_codes_and_Host_NULL_preserved=True,retained_other3_originals=3,retained_native_context_snapshot_saved_pair_files=79,retained_original_inputs=11,retained_archive_metadata_pins=plan['retained_archive_metadata_current7_pins'],complete_gzip000_and_entry000_retained=True,readonly0_and_independent_readonly_post0_required_in_publisher_and_worker=True,readonly_post_report_contract=contract,Root_actual_exec_command_sandbox_permissions_required='require_escalated',current_stat_only_joint_bytes=joint,current_external_metadata_bytes=extra,current_joint_plus_external_plus_Source16_bytes=joint+extra+16*1024*1024,Root_actual_PS_history_free_open_unlinked_and_current_resource_rechecks_still_required=True,reviewer_product_or_gzip_body_opened_or_hashed=False,helper_worker_publisher_or_native_executed=False,Source_GEN_or_publication_executed=False,PS_or_lsof_executed=False,files_deleted=False,all4_archive_complete=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 target=HERE/'REVIEW.json'
 with target.open('x')as f:json.dump(report,f,indent=2);f.write('\n')
 print(json.dumps(dict(status=report['status'],review_pin=small(target)[1])))
if __name__=='__main__':main()
