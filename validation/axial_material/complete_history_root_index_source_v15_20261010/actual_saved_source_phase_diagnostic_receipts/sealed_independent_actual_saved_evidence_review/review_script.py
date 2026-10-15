"""One finite standard-library saved-evidence audit. No business imports, payload decoding, replay, or physics."""
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import stat
import time

START=time.monotonic(); OUT=Path(__file__).parent
ROOT=Path('/Users/wen/spot'); B=ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010'
D=B/'actual_saved_source_phase_diagnostic_sources'; E=B/'actual_saved_source_phase_diagnostic_receipts'
H=ROOT/'validation/artifacts/axial-material-AAA-refined-all-group-saved-source-phase-consistency-host-20261010'
O=ROOT/'validation/artifacts/axial-material-AAA-refined-all-group-saved-source-phase-consistency-20261010'
DRIVER=ROOT/'validation/axial_material/refined_AAA_full_group_saved_source_phase_consistency_diagnostic_20261010.py'
IDS=('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')
checks={}; reads={}; input_reads={}; cache={}
def require(value,label):
    checks[label]=bool(value)
    if not value:raise ValueError(label)
def identity(value):return {k:getattr(value,k) for k in IDS}
def finite(value):return type(value) in (int,float) and math.isfinite(value)
def unique(pairs):
    r={}
    for k,v in pairs:
        if k in r:raise ValueError('duplicate JSON key '+k)
        r[k]=v
    return r

def fresh(path,expected=None,retain=False):
    path=Path(path)
    if time.monotonic()-START>=60:raise TimeoutError('finite administrative audit IO deadline')
    lb=identity(path.lstat());tb=identity(path.stat());alias=os.readlink(path) if stat.S_ISLNK(lb['st_mode']) else None
    if not stat.S_ISREG(tb['st_mode']):raise ValueError('regular hash target required '+str(path))
    digest=hashlib.sha256();count=0;pieces=[]
    with path.open('rb') as stream:
        fb=identity(os.fstat(stream.fileno()))
        if fb!=tb:raise ValueError('literal target/fd drift '+str(path))
        while True:
            raw=stream.read(2**20)
            if not raw:break
            digest.update(raw);count+=len(raw)
            if retain:pieces.append(raw)
        fa=identity(os.fstat(stream.fileno()))
    la=identity(path.lstat());ta=identity(path.stat());aa=os.readlink(path) if stat.S_ISLNK(la['st_mode']) else None
    if not(lb==la and tb==ta==fb==fa and alias==aa and count==tb['st_size']):raise ValueError('full EOF seven-ID/alias drift '+str(path))
    result={'path':str(path),'sha256':digest.hexdigest(),'size_bytes':count,'literal_7id_before':lb,'literal_7id_after':la,'target_7id_before':tb,'target_7id_after':ta,'fd_7id_before':fb,'fd_7id_after':fa,'literal_symlink_text':alias}
    if expected is not None and result['sha256']!=expected:raise ValueError('full EOF SHA mismatch '+str(path))
    reads[str(path)]=result
    if retain:cache[str(path)]=b''.join(pieces)
    return result

def metadata(path,expected=None):
    if str(path) not in cache:fresh(path,expected,True)
    elif expected is not None:require(reads[str(path)]['sha256']==expected,'metadata_cached_digest:'+str(path))
    return json.loads(cache[str(path)],object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite JSON '+x)))
def observed(record):return {'literal_7id':record['literal_7id_before'],'target_7id':record['target_7id_before'],'literal_symlink_text':record['literal_symlink_text']}
def support_match(record,pin):
    return record['path']==pin['path'] and record['sha256']==pin['sha256'] and [record['literal_7id_before'][k] for k in IDS]==pin['identity']
def root_match(record,pin):
    return record['path']==pin['path'] and record['sha256']==pin['sha256'] and record['size_bytes']==pin['size_bytes'] and record['literal_7id_before']==pin['literal_7id'] and record['target_7id_before']==pin['target_7id'] and record['literal_symlink_text']==pin['literal_symlink_text']
def catalog(root):
    require(root.is_dir() and not root.is_symlink(),'ordinary_namespace:'+str(root));files={};dirs=[]
    for parent,ds,fs in os.walk(root,followlinks=False):
        for name in ds:
            p=Path(parent)/name
            require(p.is_dir() and not p.is_symlink(),'ordinary_directory:'+str(p));dirs.append(str(p.relative_to(root)))
        for name in fs:
            p=Path(parent)/name
            require(stat.S_ISREG(p.lstat().st_mode),'ordinary_namespace_file:'+str(p));files[str(p.relative_to(root))]=identity(p.lstat())
    return {'files':files,'directories':sorted(dirs)}

review={'schema':'AXMAT_INDEPENDENT_ACTUAL_SAVED_SOURCE_PHASE_EVIDENCE_REVIEW_V1','scope':'READ_ONLY_FULL_EOF_BYTE_AND_RECEIPT_REVIEW_ONLY_NO_PHYSICS_REPLAY','business_module_imported':False,'business_API_called':False,'diagnostic_or_transport_launched':False,'numeric_payload_decoded_or_physics_computed':False,'numeric_payload_hashed_to_full_EOF':True,'modified_existing_D_H_O_E_or_source':False,'blocking_findings':[]}
try:
    snapshots_before={str(p):catalog(p) for p in (D,H,O,E)}
    summary=metadata(E/'Root_actual_complete_saved_source_phase_diagnostic_summary.json','37de4af5575f0f81ccc10a0ebf42ac14eca71af857a16f0ec06a6a30ee5189be')
    require(summary['schema']=='ROOT_ACTUAL_COMPLETE_SAVED_SOURCE_PHASE_DIAGNOSTIC_SUMMARY_V1','fixed_Root_summary_schema')
    for k in ('Root_actual_terminal','actual_host_result','actual_result','actual_manifest','actual_genuine_watchdog','namespace_and_full_input_freeze','actual_driver','actual_host_source'):
        pin=summary[k];r=fresh(pin['path'],pin['sha256'],True);require(root_match(r,pin),'Root_summary_actual_pin:'+k)
    terminal=metadata(E/'Root_actual_diagnostic_tool_terminal_return.json')
    require(type(terminal['exit_code']) is int and terminal['exit_code']==0 and terminal['closed'] is True and type(terminal['original_session_id']) is int and terminal['original_session_id']==54523 and terminal['session_repolled_after_close'] is False,'Root_actual_closed_integer0_session54523')
    tr=terminal['terminal_tool_return'];require(type(tr['exit_code']) is int and tr['exit_code']==0 and tr['chunk_id']=='c0567a' and 'session_id' not in tr,'actual_closed_c0567a_root_receipt')
    host=metadata(H/'result.json');payload=metadata(O/'result.json');manifest=metadata(O/'payload_manifest.json');freeze=metadata(E/'Root_actual_complete_source_phase_namespace_and_input_manifest.json')
    require(host['status']=='ACTUAL_SAVED_FULL_GROUP_SOURCE_PHASE_DIAGNOSTIC_EXTERNAL_ROOT_REQUIRED' and freeze['recorded_after_actual_exit0_closed'] is True,'host_scope_and_Root_after_close_freeze')
    namespace_evidence={r['root']:r for r in freeze['namespaces']};require(set(namespace_evidence)=={str(H),str(O),str(D)},'all_three_complete_saved_namespaces')
    for root in (H,O,D):
        recorded=namespace_evidence[str(root)];require(set(recorded['files'])==set(snapshots_before[str(root)]['files']) and sorted(recorded['directories'])==snapshots_before[str(root)]['directories'] and recorded['symlinks']=={},'complete_namespace_members:'+str(root))
        for rel,pin in recorded['files'].items():
            r=fresh(root/rel,pin['sha256']);require(root_match(r,pin),'complete_namespace_fullEOF_pin:'+str(root/rel))
    require(len(namespace_evidence[str(H)]['files'])==5 and len(namespace_evidence[str(O)]['files'])==12 and len(namespace_evidence[str(D)]['files'])==56,'H5_O12_frozenD56_complete_counts')
    bins={'raw_S2_all_unknowns_g_u':([370,1800],5328000),'published_work_source64_all_unknowns_g_u':([370,1800],5328000),'published_flux64_all_unknowns_g_u':([370,1800],5328000),'qext_all_moments_g_mode_l_z_r':([370,1,3,48,8],3409920),'source_projected_all_moments_g_l_z_mode':([370,3,48,1],426240)}
    names={n+'.bin' for n in bins}|{'execution_claim.json','layout.json','chronological_event_inventory.json','full_XSM_saved_record_identities.json','input_identities.json','result.json','payload_manifest.json'}
    require(set(namespace_evidence[str(O)]['files'])==names,'exact12_output_flatfiles')
    members={n:{'sha256':reads[str(O/n)]['sha256'],'size_bytes':reads[str(O/n)]['size_bytes']} for n in names if n!='payload_manifest.json'}
    require(manifest['schema']=='REFINED_AAA_SAVED_SOURCE_PHASE_PAYLOAD_MANIFEST_V1' and manifest['files']==members and len(members)==11,'complete11_member_full_EOF_manifest')
    require(type(manifest['payload_bytes_before_manifest']) is int and manifest['payload_bytes_before_manifest']==sum(v['size_bytes'] for v in members.values()),'manifest_all_member_bytes')
    layout=metadata(O/'layout.json');require(layout['dimensions']=={'groups':370,'unknowns':1800,'cells':384,'faces':392,'axial_cells':48,'angles':32,'radial_regions':8,'moments':3} and all(type(v) is int for v in layout['dimensions'].values()),'complete_saved_original_dimensions')
    require(layout['all_unknowns_layout']=={'flux_moments':[0,1152],'face_current':[1152,1544],'xnei':[1544,1800]} and set(layout['arrays'])==set(bins) and layout['original_float_precision_preserved'] is True,'all1800_positions_and_five_arrays')
    for n,(shape,size) in bins.items():
        a=layout['arrays'][n];r=reads[str(O/(n+'.bin'))]
        require(a['file']==n+'.bin' and a['dtype']=='<f8' and a['order']=='C' and a['shape']==shape and all(type(x) is int for x in a['shape']) and a['bytes']==r['size_bytes']==size and a['sha256']==r['sha256'],'full_binary_precision_shape_EOF:'+n)
    require(sum(reads[str(O/(n+'.bin'))]['size_bytes'] for n in bins)==19820160,'five_complete_binary19820160_bytes')
    input_receipts=metadata(O/'input_identities.json');contract=metadata(D/'sealed_original_full_source_review/input_contract.json','1eb226b3d02da061c0c8e1750540f925c1ec9f6baf23afbbe0f6b24cd00fb991')['inputs']
    require(len(contract)==1140 and set(input_receipts)=={'before','after','evaluator_before','evaluator_after'} and set(input_receipts['before'])==set(input_receipts['after'])==set(contract),'whole1140_input_receipt_scope')
    require(host['all1140_input_outer_metadata_before']==host['all1140_input_outer_metadata_after'] and set(host['all1140_input_outer_metadata_before'])==set(contract),'all1140_outer_before_after_identity_scope')
    root_rows=freeze['all1140_input_fresh_Root_EOF_and_literal_target_alias_seven_fields'];root_inputs={r['role']:r for r in root_rows};require(len(root_rows)==len(root_inputs)==1140 and set(root_inputs)==set(contract),'Root_afterclose_full1140_unique_role_scope')
    aliases=[]
    for role,c in contract.items():
        left=input_receipts['before'][role];right=input_receipts['after'][role]
        require(left==right and left['path']==c['path'] and left['sha256']==c['expected_sha256'] and left['size_bytes']==c['observed_metadata_7id']['st_size'],'actual_child_before_after_complete_record:'+role)
        require(set(left)=={'path','sha256','size_bytes','literal_7id_before','literal_7id_after','target_7id_before','target_7id_after','fd_7id_before','fd_7id_after','literal_symlink_text'},'child_fresh_receipt_exact_fieldset:'+role)
        for key in ('literal_7id_before','literal_7id_after','target_7id_before','target_7id_after','fd_7id_before','fd_7id_after'):
            require(set(left[key])==set(IDS) and all(type(v) is int for v in left[key].values()),'child_typed_sevenID:'+role+':'+key)
        require(left['literal_7id_before']==left['literal_7id_after'] and left['target_7id_before']==left['target_7id_after']==left['fd_7id_before']==left['fd_7id_after'] and left['size_bytes']==left['fd_7id_before']['st_size'],'child_before_after_literal_target_fd_EOF:'+role)
        require(observed(left)==host['all1140_input_outer_metadata_before'][role],'child_receipt_vs_host_outer_metadata:'+role)
        current=fresh(c['path'],c['expected_sha256']);input_reads[role]=current
        require(current==left and root_match(current,root_inputs[role]),'fresh_review_EOF_matches_child_and_Root_afterclose:'+role)
        if current['literal_symlink_text'] is not None:aliases.append({'role':role,'literal_symlink_text':current['literal_symlink_text']})
    require(sum(r['size_bytes'] for r in input_reads.values())==freeze['source_input_bytes']==summary['Root_after_all1140_full_EOF_input_bytes']==96042876,'all1140_complete_input96042876_bytes')
    for prefix in ('capture_source_','capture_return_','capture_field_'):require({r for r in contract if r.startswith(prefix)}=={prefix+f'{g:03d}' for g in range(1,371)},'all370_complete_input_family:'+prefix)
    require(input_receipts['evaluator_before']==input_receipts['evaluator_after']==reads[str(DRIVER)],'actual_evaluator_before_after_and_fresh_identity')
    claim=metadata(O/'execution_claim.json');watch=metadata(H/'run/admit.watchdog.json');admission=metadata(H/'run/admit.log');stdout=metadata(E/'parent_stdout.log');require((E/'parent_stderr.log').stat().st_size==0,'Root_parent_stderr_empty')
    expected_command=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',str(DRIVER),'--evaluator-sha256','e4eed9d520499cf15dae35c56adb1b7a3dea54e67e73046dd828ee47a1225fcf','--out-root',str(O)]
    require(watch==host['watchdog'] and watch['command']==host['actual_canonical_command']==expected_command,'actual_exact_command_and_watchdog')
    require(type(watch['returncode']) is int and watch['returncode']==0 and watch['limit_failure'] is None and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True and watch['rss_cap_mib']==512,'actual_genuine_ownchild_PASS_watchdog')
    require(all(type(v) is int and v>0 for v in (claim['PID'],claim['parent_PID'],host['actual_host_pid'],watch['pid'])) and claim['PID']==watch['pid']==host['actual_child_claim_PID'] and claim['parent_PID']==host['actual_host_pid']==host['actual_child_claim_parent_PID'] and host['actual_claim_watchdog_host_PID_binding_verified'] is True,'actual93514_child93507_host_PID_binding')
    require(claim['evaluator']==input_receipts['evaluator_before'] and claim['declared_limits']=={'whole_seconds':60.0,'stage_seconds':60.0,'own_rss_mib':512.0,'archive_bytes':67108864,'threads':1,'children':1,'retries':0},'unchanged_actual_execution_claim_limits')
    require(len(host['stage_records'])==1 and host['stage_records'][0]['status']=='PASS' and host['stage_records'][0]['command']==expected_command,'one_actual_serial_stage_PASS')
    stage=host['stage_records'][0];require(stage['log_sha256']==reads[str(H/'run/admit.log')]['sha256'],'actual_stage_log_fullEOF_pin')
    require(finite(host['whole_seconds']) and host['whole_seconds']==summary['whole_seconds']==2.801652417052537 and 0<host['whole_seconds']<60,'actual_whole2point80165_lt60')
    require(finite(watch['elapsed_seconds']) and watch['elapsed_seconds']==summary['child_seconds']==0.9526010419940576 and 0<=watch['elapsed_seconds']<watch['wall_cap_seconds']<=stage['wall_cap_seconds']<=60,'actual_child_and_original_stage_wall_cap')
    require(finite(watch['sampled_peak_rss_mib']) and watch['sampled_peak_rss_mib']==summary['sampled_peak_rss_mib']==90.625 and 0<=watch['sampled_peak_rss_mib']<512,'actual90point625_RSS_lt512')
    require((host['whole_wall_cap_seconds'],host['stage_wall_cap_seconds'],host['rss_cap_mib'],host['archive_cap_bytes'],host['threads'],host['children_at_once'],host['retries'])==(60,60,512,67108864,1,1,0),'original_host_60_512_64MiB_threads1_child1_retry0')
    require(host['profile_used'] is False and host['supervisor_class_or_MRO_modified'] is False,'normal_no_profile_no_MRO_modification')
    for name,snapshot in [('host_before',host['resources_before']),('host_after',host['resources_after']),('stage_before',stage['resource_before']),('stage_after',stage['resource_after'])]:
        require(snapshot['min_free_bytes']==8*2**30 and snapshot['artifact_budget_bytes']==96*2**30 and type(snapshot['artifact_bytes']) is int and 0<=snapshot['artifact_bytes']<=96*2**30 and type(snapshot['disk_free_bytes']) is int and snapshot['disk_free_bytes']>=8*2**30 and snapshot['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1','actual_unchanged_dynamic_history96_free8:'+name)
    for pin in freeze['unchanged_outer_source_pins']:
        r=fresh(pin['path'],pin['sha256']);require(root_match(r,pin),'actual_outer_source_unchanged:'+pin['path'])
    require(host['source_archive_before']==host['source_archive_after'] and len(host['source_archive_before'])==56,'frozenD56_host_beforeafter_identity')
    for path,pin in host['source_archive_before'].items():require(support_match(reads[path],pin),'frozenD_fullEOF_same_run_identity:'+path)
    rootD={r['path']:r for r in freeze['unchanged_all_source_archive_pins']};require(set(rootD)==set(host['source_archive_before']),'frozenD_root_afterclose_complete_set')
    for path,pin in rootD.items():require(root_match(reads[path],pin),'frozenD_current_matches_Root_afterclose:'+path)
    prior=metadata(D/'sealed_independent_normal_host_source_review/REVIEW.json','e715c1170aae24eb44e017956cbd1bf6f8eac7a929d5ab2cee2f22aaaf921faa');append=metadata(D/'sealed_independent_additional_PID_source_review/REVIEW.json','de395675763f92d42c6e71b0e8286356eccb32c50b3a2fd516700b823bd611b8');ready=metadata(D/'Root_single_SOURCE_STATUS_install_proof.json')
    require(prior['status']=='SOURCE_INTERFACE_NO_DETERMINISTIC_BLOCKER_FOUND' and len(prior['checks'])==131 and all(prior['checks'].values()) and append['status']=='TWO_HUNK_SOURCE_APPEND_NO_BLOCKER_FOUND' and len(append['checks'])==21 and all(append['checks'].values()) and append['full_inverse_to230'] is True,'reused_sealed131_and21_SOURCE_proofs_no_rerun')
    require(ready['single_SOURCE_STATUS_change_only'] is True and ready['all_15_function_class_source_segments_byte_exact'] is True and ready['full_byte_inverse_restores_original_sha256'] is True,'reused15_function_class_single_READY_full_inverse')
    for path,pin in prior['source_pins'].items():
        if pin['sha256'] in ('619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743','70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6','38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128','bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09','ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022'):
            r=fresh(path,pin['sha256']);require(r['size_bytes']==pin['bytes'],'genuine_current_source_chain:'+path)
    guardroot=ROOT/'validation/artifacts/axial-material-AAA-white-trace-refined-layered-full-20261005/preflight/live_guard';guard=metadata(guardroot/'guard_controls.json','ae4d7e86423a187c29efd5bf87d54053081d7b7fcf18ac88cd9e49639cb07454')
    require(guard['positive_child_completed'] is True and guard['actual_oversize_child_rejected'] is True and guard['terminated_own_child_not_live'] is True and guard['rss_cap_mib']==512 and len(guard['control_files'])==4,'actual_original_positive_and_oversize_guard_receipts')
    fresh(guardroot/'tested_driver_source.py',guard['source_sha256'],True)
    for name,sha in guard['control_files'].items():fresh(guardroot/name,sha)
    fullpath=ROOT/'validation/axial_material/qualify_refined_AAA_layered_full.py';fresh(fullpath,'70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6',True)
    def class_source(raw):
        text=raw.decode();return next(ast.get_source_segment(text,n) for n in ast.parse(text).body if isinstance(n,ast.ClassDef) and n.name=='OwnRSSSerialExecutor')
    require(class_source(cache[str(fullpath)])==class_source(cache[str(guardroot/'tested_driver_source.py')]),'unchanged_tested_actual_OwnRSS_class_source')
    chronology=metadata(O/'chronological_event_inventory.json');require(len(chronology['records'])==136 and len(chronology['group_final_contexts'])==370 and chronology['metric_selection'] is False and chronology['all_groups_last_context']==[3,1],'all136_chronological_dispatches_all370_contexts')
    require([r['dispatch'] for r in chronology['records']]==list(range(1,137)) and [c[0] for c in chronology['group_final_contexts']]==list(range(1,371)) and all(len(c)==9 and all(type(v) is int for v in c) and c[2:4]==[3,1] for c in chronology['group_final_contexts']),'complete_chronological_group_order_terminal_phase')
    saved=metadata(O/'full_XSM_saved_record_identities.json');owners={'production_closed_axial','production_candidate_axial','capture_candidate_axial'};require(len(saved['records'])==1110 and {(r['owner'],r['group']) for r in saved['records']}=={(o,g) for o in owners for g in range(1,371)},'all1110_original_XSM_owner_group_rows')
    require(all(set(r['records'])=={'FLUX64','FLUX','SOUR'} and all(r['records'][n]['length_words']==length and r['records'][n]['type']==kind for n,length,kind in [('FLUX64',3600,4),('FLUX',1800,2),('SOUR',1800,2)]) for r in saved['records']),'complete_XSM1800_native_type_and_word_counts')
    require(payload['classification']==admission['classification']=='COMPLETE_SAVED_ALL_GROUP_WORK_RHS_PHASE_IDENTITIES_NOT_PHYSICAL_BALANCE_QUALIFIED' and payload['all_complete_work_rhs_and_saved_source_phase_word_identities'] is True and payload['same_original_map012_saved_FLUX64_and_SOUR32_in_all_three_owners'] is True,'fixed_child_complete_software_saved_phase_identity_scope')
    require(payload['dimensions']==summary['dimensions']=={'groups':370,'unknowns_per_group':1800,'cells':384,'faces':392,'moments':3} and payload['checked_word_counts']==summary['checked_word_counts']=={'S2_qext_words':426240,'whole_R64_rhs_words':666000,'all_unknowns_flux_words':666000,'SOUR32_words_per_XSM_owner':666000,'projected_coefficients':53280},'actual_all_full_scope_counts_match')
    require(all(payload[k] is False for k in ('reaction_multiplicity_contract_qualified','source_fission_scatter_partition_qualified','final_flux_reconstructed_source_equals_actual_prior_iteration_work_rhs_assumed','entire_original_compilation_source_byte_identity_proved','full_physical_neutron_balance_qualified','scientific_accuracy_qualified','AAA_qualified','ABA_admitted','same_MG_unreduced_reference_qualified','transport_launched')),'all_scientific_and_native_qualifications_still_false')
    require(support_match(reads[str(H/'result.json')],stdout['actual_host_result']) and support_match(reads[str(H/'run/admit.log')],stdout['actual_diagnostic_stdout']) and stdout['actual_external_Root_terminal_required'] is True,'Root_stdout_actual_host_result_and_child_log_pins')
    snapshots_after={str(p):catalog(p) for p in (D,H,O,E)};require(snapshots_before==snapshots_after,'all_D_H_O_E_members_and_sevenIDs_unchanged_across_readonly_review')
    for rel in snapshots_before[str(E)]['files']:fresh(E/rel)
    joint=sum(v['st_size'] for s in snapshots_after.values() for v in s['files'].values())+DRIVER.stat().st_size
    require(joint<64*2**20 and host['joint_archive_roots']==[str(H),str(O),str(D),str(E)] and host['canonical_source_bytes_counted_outside_archive']==DRIVER.stat().st_size,'fresh_joint_H_O_D_E_pluscanonical_lt64MiB')
    post=metadata(E/'Root_actual_complete_source_phase_post_receipt_archive_check.json');require(post['checked_after_terminal_summary_manifest_and_human_REPORT'] is True and post['original_archive_cap_bytes']==64*2**20 and post['joint_scope']==[str(H),str(O),str(D),str(E),str(DRIVER)] and post['joint_bytes_before_this_check']+(E/'Root_actual_complete_source_phase_post_receipt_archive_check.json').stat().st_size==joint,'Root_actual_postreceipt_archive_check_matches_current_joint')
    free=shutil.disk_usage(ROOT/'validation/artifacts').free;require(free>=8*2**30,'fresh_global_free_disk_at_least8GiB')
    review.update(status='PASS_INDEPENDENT_ACTUAL_SAVED_SOURCE_PHASE_IMMUTABLE_EVIDENCE_ONLY',checks=checks,all1140_current_full_EOF_input_receipts=input_reads,complete_current_file_full_EOF_receipts=reads,complete_namespace_snapshots=snapshots_after,actual_Root_terminal_provenance='Saved Root receipt606de and parent direct actual c0567a integer0 observation; no repoll or guessed live state.',actual_Root_exit_code=0,actual_Root_closed=True,actual_original_session_id=54523,actual_Root_terminal_chunk='c0567a',actual_child_PID=93514,actual_host_PID=93507,actual_whole_seconds=host['whole_seconds'],actual_child_seconds=watch['elapsed_seconds'],actual_sampled_peak_rss_mib=watch['sampled_peak_rss_mib'],current_complete_input_roles=1140,current_complete_input_bytes=96042876,current_literal_aliases=aliases,complete_output_files=12,complete_manifest_members=11,complete_binary_files=5,complete_binary_bytes=19820160,frozen_D_source_files=56,fresh_joint_archive_bytes=joint,archive_cap_bytes=64*2**20,fresh_global_free_bytes=free,actual_history_before_bytes=host['resources_before']['artifact_bytes'],actual_history_after_bytes=host['resources_after']['artifact_bytes'],history_cap_bytes=96*2**30,history_scope='Saved genuine dynamic ART snapshots validated; this bounded review does not rescan entire history or execute resource helper.',original_caps_unchanged=True,source_reviews_reused={'single_READY_15_function_class_segments':True,'host_inverse_chain_counts':[2,16,15],'sealed131_review_sha256':'e715c1170aae24eb44e017956cbd1bf6f8eac7a929d5ab2cee2f22aaaf921faa','sealed21_append_sha256':'de395675763f92d42c6e71b0e8286356eccb32c50b3a2fd516700b823bd611b8','actual_final_host_sha256':'2b0e919aca6ac4e59a438ffe7d49fccc318bcc5821192a537472c06cbe0a3186','full_source_survey_rerun':False},software_evidence_credit='Original fixed child actually completed saved work-RHS/source-phase typed-word identities. Audit freshly confirms all complete files, all1140 inputs, actual receipts and immutable source chain; it performs no independent physical recalculation.',qualification={'reaction_multiplicity_contract_qualified':False,'source_fission_scatter_partition_qualified':False,'entire_original_compilation_source_byte_identity_proved':False,'full_physical_neutron_balance_qualified':False,'scientific_accuracy_qualified':False,'AAA_qualified':False,'ABA_admitted':False,'same_MG_unreduced_reference_qualified':False,'new_native_transport_executed':False,'goal_complete':False})
except BaseException as error:
    review.update(status='FAIL_FINITE_ACTUAL_EVIDENCE_REVIEW_STOPPED',error=repr(error),blocking_findings=[repr(error)],checks=checks,all1140_current_full_EOF_input_receipts=input_reads,complete_current_file_full_EOF_receipts=reads)
review['readonly_audit_seconds']=time.monotonic()-START
with (OUT/'REVIEW.json').open('x') as stream:json.dump(review,stream,indent=2,sort_keys=True,allow_nan=False);stream.write('\n')
report=('完整保存源相位实际证据只读复核：'+review['status']+'\n'
 'Root原c0567a/session54523实际integer0已关闭；复核不重轮询、不重跑诊断。\n'
 '完整12输出/11清单成员/5数组19,820,160B、D冻结56文件均全EOF SHA及7ID一致；1140原输入96,042,876B实际child前后、Root关闭后及本复核新鲜全EOF与literal/target/fd7ID/alias一致。\n'
 '实际child93514/host93507 PID绑定、one genuine serial PASS、whole2.801652s/child0.952601s/peak90.625MiB、原60s/512MiB/联合64MiB及history96GiB/free8GiB凭证一致。\n'
 '复用已封存15函数singleREADY及2+16+15 host逆变换源码证明，无业务导入/调用、数值解码、物理计算、重放、源修改或规范目录写入。\n'
 '只授软件保存工作源/源相位一致性证据；反应多重性、裂变散射分项、完整编译源身份、物理平衡、同能群参考、AAA、ABA及最终目标完成均false。\n')
if review['blocking_findings']:report+='阻碍：'+repr(review['blocking_findings'])+'\n'
with (OUT/'REPORT.txt').open('x') as stream:stream.write(report)
raw=(OUT/'REVIEW.json').read_bytes();print(json.dumps({'status':review['status'],'directory':str(OUT),'review_sha256':hashlib.sha256(raw).hexdigest(),'review_bytes':len(raw),'checks':len(checks),'fresh_current_input_roles':len(input_reads),'fresh_joint_archive_bytes':review.get('fresh_joint_archive_bytes'),'readonly_audit_seconds':review['readonly_audit_seconds'],'business_API_called':False,'diagnostic_or_transport_launched':False,'numeric_payload_decoded_or_physics_computed':False},indent=2))
if review['blocking_findings']:raise SystemExit(1)
