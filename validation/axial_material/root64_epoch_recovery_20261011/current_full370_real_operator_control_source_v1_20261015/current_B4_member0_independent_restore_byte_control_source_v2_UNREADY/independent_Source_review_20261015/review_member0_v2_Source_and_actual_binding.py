"""Source/metadata admission review only. Never import or execute the verifier."""
import ast, hashlib, json, pathlib, shlex, stat
HERE=pathlib.Path(__file__).absolute().parent
BASE=HERE.parent
def ids(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def small(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_size<8*1024*1024
 raw=p.read_bytes();h=hashlib.sha256(raw).hexdigest();assert h==hashlib.sha256(p.read_bytes()).hexdigest()and ids(s)==ids(p.lstat())
 return raw,dict(path=str(p),sha256=h,size_bytes=s.st_size,identity=ids(s))
def meta(p):
 raw,pf=small(pathlib.Path(p['path']));assert pf==p;return json.loads(raw)
def current(p):
 s=pathlib.Path(p['path']).lstat();assert stat.S_ISREG(s.st_mode)and s.st_nlink==1 and ids(s)==p['identity']and s.st_size==p['size_bytes']
def genuine(v,key,code,chunk,payload_role,pf):
 t=v[key];assert v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==code
 assert type(t['exit_code'])is int and t['exit_code']==code and 'session_id'not in t and t['chunk_id']==chunk
 if payload_role:assert json.loads(t['output'].strip().splitlines()[-1])[payload_role]==pf
def main():
 ar,ap=small(BASE/'AUTHOR_SOURCE_ONLY_FREEZE.json');assert ap['sha256']=='04e03f4a8e20fc032043722f6db3632b922b765316310b3ada2cd3a47e5930c3'and ap['size_bytes']==2944
 a=json.loads(ar);assert a['schema']=='B4_MEMBER0_ROOT_ONLY_VERIFIER_V2_SOURCE_AUTHOR_FREEZE_V1'and a['Source_author_task']=='/root/b_capture_source_peer'and a['Source_only_frozen']is True
 sp=a['algorithm_Source_pin'];sr,actual=small(pathlib.Path(sp['path']));assert actual==sp and sp['sha256']=='13abb0af78c2b83885fb732339004b3e73bafd887a1ab254485021d91d827df3'and sp['size_bytes']==18469
 source=sr.decode();ast.parse(source)
 b=meta(a['bound_actual_metadata_pin']);inverse=meta(a['inverse_and_static_scope_pin']);cli=meta(a['reviewable_CLI_pin'])
 v1raw,v1pf=small(pathlib.Path(inverse['original_v1_Source_pin']['path']));assert v1pf==inverse['original_v1_Source_pin']and v1pf['sha256']=='9db28de32457c18c7fe946de3bb2691ebbd2d567c9e3bd3dbcb6a781a9a4b8c5'
 change=inverse['only_algorithm_replacement'];assert source.count(change['after'])==1 and source.replace(change['after'],change['before']).encode()==v1raw
 assert "supplement['recorded_complete_member000']['original_plain_full_pin']==original"in change['after']
 assert "type(supplement['supplemental_actual_recorded_child_integer_exit_codes'])is list"in change['after']and "==[1]"in change['after']and "all(type(code)is int"in change['after']
 assert b['schema']=='ROOT_CURRENT_B4_MEMBER0_RESTORATION_BYTE_CONTROL_BINDING_V1'and b['actual_preconditions_closed']is True and b['actual_failed_archive_and_post_roles_audited']is True
 archive=meta(b['original_B4_execution_binding_pin']);common_raw,commonpf=small(pathlib.Path(b['frozen_B4_common_Source_pin']['path']));assert commonpf==b['frozen_B4_common_Source_pin']and commonpf['sha256']=='eef80ab201b2ffc91217a4c6275f68f18212f6a34d7eef735ccd359b65aae57d'
 common=common_raw.decode();ast.parse(common);assert len(b['complete_joint_roots'])==73 and b['complete_joint_roots']==archive['complete_joint_roots']
 assert b['original_caps']==archive['original_caps']and b['Root_stage_seconds']==600 and b['new_Source_metadata_hard_bound_bytes']==16*1024*1024
 assert b['only_member0_restore_bytes_control']is True and b['all4_archive_completed']is False and b['original_m_xsm_body_must_not_be_opened']is True and b['new_owning_ledger_root_created']is False
 cp=b['actual_failed_archive_closure_pins'];d={k:meta(p)for k,p in cp.items()}
 genuine(d['Root_tools'],'actual_terminal_return',1,'434819',None,None)
 genuine(d['post_tools'],'actual_review_return',0,'f67eab','review_pin',cp['post'])
 genuine(d['supplement_tools'],'actual_review_return',0,'cd7af3','review_pin',cp['supplement'])
 assert d['Root_tools']['actual_execution_permission_mode']=='require_escalated'and d['Root_tools']['actual_retried']is False
 originalcli=meta(b['original_B4_final_CLI_pin']);assert shlex.split(d['Root_tools']['exact_executed_command'])==originalcli['argv']and len(originalcli['argv'])==24
 host=d['Host'];watch=d['watchdog'];post=d['post'];supplement=d['supplement'];first=d['first_failure']
 assert host['binding_pin']==b['original_B4_execution_binding_pin']and host['complete_joint_roots']==b['complete_joint_roots']and host['archive_complete']is False and host['all4_original_products_current7_retained']is True
 assert host['actual_watchdog']is None and post['actual_recorded_child_integer_exit_codes']==[]and post['actual_Root_integer_exit_code']==1
 assert len(host['records'])==1 and host['records'][0]['status']=='FAILED'and host['records'][0]['error']=='own-child stage failed; no retry'
 assert cp['watchdog']['path']==str(pathlib.Path(archive['planned_actual_output_root'])/(host['records'][0]['label']+'.watchdog.json'))and watch['command']==host['records'][0]['command']
 assert type(watch['returncode'])is int and watch['returncode']==1 and watch['limit_failure']is None
 sk=b['actual_failure_supplement_key_projection'];assert all(type(v)is str for v in sk.values())
 assert supplement['schema']==sk['schema']=='SUPPLEMENTAL_B4_ACTUAL_FAILURE_CHILD1_MEMBER0_METADATA_FACTS_V1'
 assert supplement['status']==sk['status']=='PASS_SUPPLEMENTAL_B4_FAILURE_CHILD1_MEMBER0_RECORDED_FACTS_METADATA_ONLY'and supplement['failure']is None and supplement['metadata_only']is True
 for field,expected in [('Host_pin_field',cp['Host']),('Root_tools_pin_field',cp['Root_tools']),('original_failure_post_pin_field',cp['post']),('original_failure_post_tools_pin_field',cp['post_tools']),('first_failure_pin_field',cp['first_failure']),('watchdog_pin_field',cp['watchdog']),('entry0_pin_field',b['retained_member0_entry_pin']),('gzip0_pin_field',b['complete_member0_gzip_pin'])]:assert supplement[sk[field]]==expected
 codes=supplement['supplemental_actual_recorded_child_integer_exit_codes'];assert type(codes)is list and codes==[1]and all(type(x)is int for x in codes)
 original=b['original_member0_saved_full_pin'];entry=meta(b['retained_member0_entry_pin']);assert supplement['recorded_complete_member000']==entry and entry['original_plain_full_pin']==original==archive['all4_product_pins'][0]
 assert entry['compressed_archive_full_pin']==b['complete_member0_gzip_pin']and entry['compression_input_SHA']==entry['streamed_decompressed_SHA']==original['sha256']and entry['compression_input_length']==entry['streamed_decompressed_length']==original['size_bytes']==76594248
 assert first['phase']=='ARCHIVE_1'and first['completed_entry_pins']==[b['retained_member0_entry_pin']]and first['original_product_files_deleted']is False
 assert supplement['original_prior_post_recorded_child_integer_exit_codes']==[]and supplement['streamed_decompressed_bytes_independently_recomputed_by_supplement']is False and supplement['future_Root_independent_single_member_stream_control_pin']is None and supplement['archive_all4_complete']is False
 assert cli['Source_pin']==sp and cli['binding_pin']==a['bound_actual_metadata_pin']and shlex.split(cli['command'])==cli['argv']and cli['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated'
 assert cli['argv'][-5]==str(pathlib.Path(sp['path']))and cli['argv'][-4]=='--binding-pin'and json.loads(cli['argv'][-3])==a['bound_actual_metadata_pin']and cli['argv'][-2]=='--source-pin'and json.loads(cli['argv'][-1])==sp
 assert cli['argv'][:11]==['/usr/bin/env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1','/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B']and len(cli['argv'])==16
 assert 'c.admit('not in source and 'resources=c.Resources(archive_binding,started,600)'in source and 'last_full_completed=time.monotonic()'in source and 'time.monotonic()-last_full_completed>=5.0'in source
 assert source.count('blind_gzip_sha()')==3 and 'budget();chunk=f.read(2**20)'in source and 'budget();chunk=stream.read(2**20)'in source
 assert 'post[k[\'recorded_child_codes_field\']]==[]'in source and 'self.joined=production.DiskResources'in common and 'own_open_unlinked_bytes'in common
 for p in archive['all4_product_pins']+archive['retained_native_current7_pins']+archive['original_B_native_and_readonly_input_current7_pins']+[b['complete_member0_gzip_pin']]:current(p)
 assert not (BASE/'ROOT_MEMBER0_CONTROL_CLAIM.json').exists()and not(BASE/'ROOT_MEMBER0_INDEPENDENT_RESTORE_BYTE_CONTROL_REPORT.json').exists()
 review=dict(schema='INDEPENDENT_B4_MEMBER0_VERIFIER_V2_SOURCE_AND_ACTUAL_BINDING_REVIEW_V1',status='PASS_SOURCE_ONLY_B4_MEMBER0_RESTORE_BYTE_CONTROL_V2',failure=None,source_only=True,algorithm_Source_pin=sp,author_freeze_pin=ap,actual_binding_pin=a['bound_actual_metadata_pin'],exact_Root_CLI_pin=a['reviewable_CLI_pin'],whole_inverse_v1_Source_pin=v1pf,all_other_algorithm_bytes_exact_v1=True,actual_supplement_pin=cp['supplement'],actual_supplement_tools_pin=cp['supplement_tools'],genuine_supplement_typed0_chunk='cd7af3',original_Root1_child1_old_post0_preserved=True,old_post_child_codes_empty_preserved=True,new_supplement_child_codes_strict_integer_list=[1],nested_original_pin_exactly_bound=True,original_73_roots_and_all_caps_unchanged=True,only_Root_may_execute_once=True,Root_actual_execution_permission_mode_required='require_escalated',execution_Source_preconditions_admitted=True,actual_Root_byte_control_executed=False,member0_restoration_success_claimed=False,Source_author_task='/root/b_capture_source_peer',independent_reviewer_task='/root/b2_build_source_peer',candidate_or_helpers_imported=False,gzip_or_original_body_opened=False,Source_GEN_or_publication_executed=False,compiler_native_or_child_executed=False,files_deleted=False,all4_archive_complete=False,retirement_authorized=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 target=HERE/'REVIEW.json'
 with target.open('x')as f:json.dump(review,f,indent=2);f.write('\n')
 print(json.dumps(dict(status=review['status'],review_pin=small(target)[1])))
if __name__=='__main__':main()
