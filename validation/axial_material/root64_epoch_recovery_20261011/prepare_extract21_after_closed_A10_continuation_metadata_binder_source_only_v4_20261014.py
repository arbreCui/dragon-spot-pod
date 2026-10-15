"""Prepare the future split-authority metadata binder; never execute its main or science code."""
import ast,hashlib,json,os
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'bind_material_extract_request_preparation_after_actual_first_A_short_FIL_v10_source_only_v3_20261014.py'
OUT=R/'bind_material_extract_request_preparation_after_closed_short_FIL_A10_continuation_source_only_v4_20261014.py'
IV=R/'COMPLETE_EXTRACT21_V3_TO_SPLIT_A10_CONTINUATION_V4_WHOLE_BYTE_INVERSE_20261014.json'
C=R/'current_formal_short_FIL_A10_closed_capture_continuation_source_v3_20261014'
SPLIT=r''' prior=first['actual_original_authority_pins'];owner=Path(prior['original-phase']['path']).parent
 priorphase=exact(prior['original-phase']);priortools=exact(prior['original-Root-tools']);priorargv=exact(prior['original-Root-argv']);priorcli=exact(prior['original-CLI']);priorpost=exact(prior['failed-post']);priorpt=exact(prior['failed-post-tools'])
 priorcanonical={'actual_report_pin':prior['original-phase'],'actual_Host_freeze_pin':prior['original-host-freeze'],'actual_CLI_pin':prior['original-CLI'],'actual_Root_true_tool_return_pin':prior['original-Root-tools'],'actual_Root_argv_pin':prior['original-Root-argv']}
 q=priortools['actual_terminal_return']
 if priortools['observed_closed']is not True or type(priortools['original_integer_exit_code'])is not int or priortools['original_integer_exit_code']!=1 or type(q['exit_code'])is not int or q['exit_code']!=1 or q.get('session_id')is not None or shlex.split(priortools['exact_executed_command'])!=priorargv['exact_argv']or priorargv['exact_argv']!=priorcli['exact_argv']or len(priorargv['exact_argv'])!=32:raise RuntimeError('original A10 genuine Root1/exact32 retained')
 if priorpost['schema']!='INDEPENDENT_MATERIAL_FIRST_A_SHORT_FIL_V10_ACTUAL_OBSERVATION_POSTVERIFICATION_V1'or priorpost['status']!='PASS_ACTUAL_MATERIAL_FIRST_A_SHORT_FIL_V10_STAGE0_CAPTURE_RELEASE_BLOCKED_FACTUAL_POSTVERIFICATION'or priorpost['failure']is not None or priorpost['actual_material_stage_closed0']is not True or priorpost['actual_stage_statuses']!=['PASS']or priorpost['actual_context_collection_source_function_verified']is not True or any(priorpost[k]!=v for k,v in priorcanonical.items())or any(priorpost[k]is not False for k in('business_executed','compiler_executed','numerical_executed','files_deleted')):raise RuntimeError('exact prior child0 cached collection factual post0; no A10 Root0 claim')
 for k in('actual_review_return','actual_postverification_return'):
  term0(priorpt[k])
  if json.loads(priorpt[k]['output'].strip().splitlines()[-1])['review_pin']!=prior['failed-post']:raise RuntimeError('original factual post0 stdout fullPF')
 if priorpt['observed_closed']is not True or type(priorpt['original_integer_exit_code'])is not int or priorpt['original_integer_exit_code']!=0 or priorphase['status']!='FAILED_CURRENT_OBSERVATION_NO_RETRY'or priorphase['failure']!='RuntimeError: both real process metadata tools fully pinned'or priorphase['actual_closed_owned_library_copy_release_pin']is not None or priorpost['actual_observation_manifest_pin']is not None or priorpost['actual_closed_owned_library_copy_release_pin']is not None:raise RuntimeError('original failed phase and absent manifest/release retained')
 if phase['original_failed_phase_pin']!=prior['original-phase']or phase['original_Root_true_tool_pin']!=prior['original-Root-tools']or phase['original_Root_exit_code_retained']!=1 or phase['original_Root_failure_retained']!=priorphase['failure']or phase['cached_actual_collection_post_pin']!=prior['failed-post']or phase['original_capture_collector_not_reexecuted']is not True or phase['completion_only_existing_closed_stage']is not True or phase['Dragon_or_compiler_or_material_child_launched_by_continuation']is not False or phase['new_scientific_outputs_created']is not False or phase['actual_prior_material_stage_record_reused_wholebytes']is not True or phase['records']!=priorphase['records']or phase['actual_prior_A_cwd']!=str(owner/'A')or phase['original_release_owner_output_root']!=str(owner):raise RuntimeError('new completion has only exact original stage/owner/Source provenance')
 if type(post['actual_Root_integer_exit_code'])is not int or post['actual_Root_integer_exit_code']!=0 or type(post['actual_original_Root_integer_exit_code'])is not int or post['actual_original_Root_integer_exit_code']!=1 or post['actual_material_stage_closed0']is not True or type(post['actual_new_material_child_launch_count'])is not int or post['actual_new_material_child_launch_count']!=0 or post['actual_original_fullfresh2_reserve_admitted']is not True or type(post['actual_fullfresh2_margin_bytes'])is not int or post['actual_fullfresh2_margin_bytes']<=0 or any(post['actual_original_failed_A10_authority_pins'][k]!=v for k,v in priorcanonical.items()):raise RuntimeError('strict separate continuation Root0/post0, original Root1, no new child')
 family=phase['resources_after_full_family'];margin=96*2**30-family['artifact_bytes']-20971764748-64*2**20-2*2**30
 if type(family['artifact_bytes'])is not int or family['artifact_budget_bytes']!=96*2**30 or family['min_free_bytes']!=8*2**30 or family['resource_scope_policy']!='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'or margin<=0 or margin!=post['actual_fullfresh2_margin_bytes']or family['disk_free_bytes']-20971764748-2*2**30<8*2**30:raise RuntimeError('actual direct original full-family cold/meta/fresh2/free8 snapshot; no next budget grant')
'''
def pin(p):
 p=Path(p);s=p.stat();return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),size_bytes=s.st_size,identity=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns])
def write(p,v):
 raw=v.encode()if isinstance(v,str)else(json.dumps(v,indent=2,allow_nan=False)+'\n').encode()
 with p.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 return pin(p)
def main():
 if OUT.exists()or IV.exists():raise RuntimeError('unique v4 Source')
 cp=pin(C/'ROOT_REVIEWABLE_EXACT_CLOSED_A10_CONTINUATION_ARGV_20261014.json');hp=pin(C/'COMPLETE_SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_HOST_SOURCE_FREEZE.json');cli=json.loads(Path(cp['path']).read_bytes())
 if cli['Host_freeze_pin']!=hp or len(cli['exact_argv'])!=62:raise RuntimeError('actual published continuation HF/CLI62')
 a=OLD.read_text();z=a;changes=[]
 def change(old,new):
  nonlocal z
  if z.count(old)!=1:raise RuntimeError('one exact original Source block '+old)
  z=z.replace(old,new,1);changes.append(dict(before=old,after=new))
 tree=ast.parse(z)
 for name,value in [('FIRST_CLI','Path('+repr(cp['path'])+')'),('FIRST_HF_PIN',repr(hp)),('FIRST_CLI_SHA',repr(cp['sha256'])),('POST_SCHEMA',repr('INDEPENDENT_SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_V3_ACTUAL_COMPLETION_POSTVERIFICATION_V1')),('POST_STATUS',repr('PASS_ACTUAL_SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_V3_COMPLETION_POSTVERIFICATION'))]:
  node=next(n for n in ast.parse(z).body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id==name);change(ast.get_source_segment(z,node),name+'='+value)
 change('AFTER_ACTUAL_FIRST_A_SHORT_FIL_V10_ARGV_20261014.json','AFTER_CLOSED_SHORT_FIL_A10_CONTINUATION_ARGV_20261014.json')
 oldline=next(line for line in z.splitlines()if "if root['observed_closed']"in line)
 newline=" if root['observed_closed']is not True or type(root['original_integer_exit_code'])is not int or root['original_integer_exit_code']!=0 or shlex.split(root['exact_executed_command'])!=ra['exact_argv']or len(ra['exact_argv'])!=62 or ra['exact_argv']!=first['exact_argv']or first['Host_freeze_pin']!=FIRST_HF_PIN or ra['exact_argv'][-2:]!=['--output-dir',first['output_root']]:raise RuntimeError('genuine independent continuation Root0/exact62/publicCLI/HF/output; original A10 remains Root1')"
 change(oldline,newline)
 anchor=" out=Path(first['output_root'])";change(anchor,anchor+'\n'+SPLIT.rstrip())
 change("pins['A-release']['path']!=str(out/'ACTUAL_CLOSED_OWNED_LIBRARY_COPY_RELEASE.json')","pins['A-release']['path']!=str(owner/'ACTUAL_CLOSED_OWNED_LIBRARY_COPY_RELEASE.json')")
 change("phase['actual_observer_build_report_pin']!=first['actual_observer75_report_pin']","phase['actual_observer_build_report_pin']!=priorcli['actual_observer75_report_pin']")
 change("state['actual_cwd']!=str(out/'A')","state['actual_cwd']!=str(owner/'A')")
 change("str(out/'s'/dict(DLIB_ACTUAL='A',DLIB8R1_370='B')[name])","str(owner/'s'/dict(DLIB_ACTUAL='A',DLIB8R1_370='B')[name])")
 change("str(out/'s')","str(owner/'s')")
 change('AFTER_ACTUAL_FIRST_A_SHORT_FIL_V10_ARGV_V1','AFTER_CLOSED_SHORT_FIL_A10_CONTINUATION_ARGV_V1')
 extra=" if release['owned_copy_pins_before_release']!=priorpost['actual_owned_library_copy_pins_current']or manifest['original_failed_phase_pin']!=prior['original-phase']or manifest['original_Root_true_tool_pin']!=prior['original-Root-tools']or manifest['completion_only_original_Root1_preserved']is not True:raise RuntimeError('only exact original private2 retired; original Root1 remains explicit')\n for k,v in priorpost['actual_collected_A_observation_state'].items():\n  if k not in('actual_owning_report_pin','actual_stage_label','actual_command')and state[k]!=v:raise RuntimeError('complete cached original collection metadata unchanged '+k)\n"
 anchor=" originals=release['original_live_input_pins'];released=release['owned_copy_pins_before_release'];shared=manifest['actual_shared_input_library_evidence']";change(anchor,extra+anchor)
 ast.parse(z)
 fs=lambda s:{n.name:ast.get_source_segment(s,n)for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)}
 if any(fs(a)[n]!=fs(z)[n]for n in fs(a)if n!='main'):raise RuntimeError('all metadata primitives wholebytes unchanged')
 op=write(OUT,z);ip=write(IV,dict(schema='COMPLETE_EXTRACT21_V3_TO_SPLIT_A10_CONTINUATION_V4_WHOLE_BYTE_INVERSE_V1',predecessor_source_pin=pin(OLD),candidate_source_pin=op,changes=changes,whole_file_before=a,whole_file_after=z,whole_file_inverse_byte_equal=True,selected_actual_continuation_CLI_pin=cp,selected_actual_continuation_Host_freeze_pin=hp,original_request_builder_and_evidence_and_extract_math_code_unchanged=True,planned_continuation_post_schema='INDEPENDENT_SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_V3_ACTUAL_COMPLETION_POSTVERIFICATION_V1',planned_continuation_post_status='PASS_ACTUAL_SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_V3_COMPLETION_POSTVERIFICATION',future_actual_continuation_report_pin=None,future_actual_continuation_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_continuation_Root_tools_pin=None,future_actual_continuation_Root_argv_pin=None,future_actual_continuation_post_pin=None,future_actual_continuation_post_tools_pin=None,binder_main_executed=False,request_preparer_executed=False,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 back=z
 for c in reversed(changes):
  if back.count(c['after'])!=1:raise RuntimeError('exact scoped byte reverse')
  back=back.replace(c['after'],c['before'],1)
 if back.encode()!=OLD.read_bytes():raise RuntimeError('complete Source inverse')
 print(json.dumps(dict(status='FUTURE_EXTRACT21_SPLIT_ORIGINAL_A10_ROOT1_AND_CONTINUATION_ROOT0_METADATA_BINDER_SOURCE_ONLY_READY',Source_pin=op,inverse_pin=ip,Source_author_pin=pin(__file__),selected_actual_CLI_pin=cp,selected_actual_Host_freeze_pin=hp,future_continuation_actual_authorities_all_None=True,binder_main_executed=False,request_preparer_executed=False,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
