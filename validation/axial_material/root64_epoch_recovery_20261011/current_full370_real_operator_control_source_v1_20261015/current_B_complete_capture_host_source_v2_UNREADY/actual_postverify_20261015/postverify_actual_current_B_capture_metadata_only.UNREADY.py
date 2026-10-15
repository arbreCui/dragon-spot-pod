"""Post Source only: blinded output SHA and saved execution/manifest metadata.

No helper imports, numerical parsing, context decoding, native child or cleanup.
The independent actual executor must be distinct from this Source author.
"""
import argparse, hashlib, json, os, re, resource, shutil, stat, sys, time
from pathlib import Path

BASE=Path(__file__).absolute().parent
PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
OUT=ROOT/'validation/artifacts/axial-material-inputs-20261003/A/b63'
SOURCE_AUTHOR='/root/b_capture_actual_post_source'
ORIGINAL_TEMPLATE_AUTHOR='/root/b_capture_source_peer'
EXPECTED_EXECUTOR='/root/b2_build_source_peer'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(three_plane_qualified=False,GLOBAL_qualified=False,rank_qualified=False,online_BOOT_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,historical_unsaved_context_recovered=False,reaction_multiplicity_qualified=False,physical_neutron_balance_qualified=False,coupled_370group_reference_qualified=False,scientific_accuracy_qualified=False,B_full_extraction_completed=False,B_six_phase_construction_completed=False,B_OVERV_control_completed=False,physics_qualified=False,compiled_IO_semantics_qualified=False)
START=time.monotonic()

def need(value,message):
    if value is not True:raise RuntimeError(message)

def budget():
    need(time.monotonic()-START<600,'metadata post600s')
    need(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)<512*2**20,'metadata post512MiB')

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def current(p):
    budget();q=Path(p['path']);s=q.lstat()
    need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid() and identity(s)==p['identity']and s.st_size==p['size_bytes']and len(p['identity'])==7 and all(type(x)is int for x in p['identity']),'exact ordinary output/Source/control current7')
    return q

def full(p):
    q=current(p);h=hashlib.sha256()
    with q.open('rb')as f:
        need(identity(os.fstat(f.fileno()))==p['identity'],'opened blinded file7')
        while True:
            b=f.read(2**20)
            if not b:break
            h.update(b);budget()
        need(identity(os.fstat(f.fileno()))==p['identity'],'blinded file EOF7')
    need(h.hexdigest()==p['sha256'],'blind fullEOF SHA');current(p);return q

def pin(q):
    q=Path(q);s=q.lstat();h=hashlib.sha256()
    need(q.is_relative_to(OUT)or s.st_size<8*2**20,'only whole new outputs or small Source/control are read')
    with q.open('rb')as f:
        need(identity(os.fstat(f.fileno()))==identity(s),'opened new-output7')
        while True:
            b=f.read(2**20)
            if not b:break
            h.update(b);budget()
        need(identity(os.fstat(f.fileno()))==identity(s),'new-output EOF7')
    p=dict(path=str(q),sha256=h.hexdigest(),size_bytes=s.st_size,identity=identity(s));current(p);return p

def meta(p):
    need(p['size_bytes']<8*2**20,'control metadata8MiB');return json.loads(full(p).read_bytes())

def saved_resources(v):
    need(v['host_SELF_peak_bytes']<512*2**20 and 0<=v['whole_elapsed_seconds']<1800 and v['entire_capture_output_bytes']<640*2**20,'saved original host/capture limits')
    h=v['original_history'];j=v['complete_joint']
    need(h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['artifact_bytes']+v['explicit_external_metadata_bytes']+v['host_open_unlinked_bytes']<2*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'saved original history/cumulative/cold/metadata/free limits')

def file_tree_pins():
    """Only fresh capture outputs are blindly read. Nothing is decoded."""
    rows=[]
    if not os.path.lexists(OUT):return rows
    need(OUT.is_dir()and not any(q.is_symlink()for q in(OUT,*OUT.parents)),'literal ordinary capture output root')
    for q in sorted(OUT.rglob('*')):
        budget();s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'no partial capture alias')
        if stat.S_ISREG(s.st_mode):
            need(s.st_uid==os.getuid()and s.st_nlink==1,'owned ordinary new output');p=pin(q);full(p);rows.append(p)
        else:need(stat.S_ISDIR(s.st_mode),'only ordinary capture files and directories')
    return rows

def current_metadata_role(p,build):
    """The same exact readonly roles are checked, without importing a helper."""
    q=Path(p['path']);s=q.lstat();budget()
    need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and identity(s)==p['identity']and s.st_size==p['size_bytes']and len(p['identity'])==7 and all(type(x)is int for x in p['identity']),'exact inherited metadata current7')
    if p in build['readonly_system_SDK_header_pins']:
        root=Path(build['readonly_system_SDK_root']);rs=root.lstat()
        need(str(root)=='/Library/Developer/CommandLineTools/SDKs/MacOSX27.0.sdk'and stat.S_ISDIR(rs.st_mode)and rs.st_uid==0 and identity(rs)==build['readonly_system_SDK_root_identity']and not any(x.is_symlink()for x in(root,*root.parents))and str(q)in{str(root/'usr/include'/n)for n in('stdio.h','stdlib.h','stdint.h')}and s.st_uid==0 and s.st_nlink==1,'only three frozen SDK header current7 roles; payloads unread')
    elif p in build['readonly_system_tool_metadata_pins']:
        need(str(q)in('/bin/ps','/usr/sbin/lsof')and s.st_uid==0 and s.st_nlink==1 and bool(s.st_mode&0o111),'only exact frozen readonly PS/lsof role')
    elif p==build['C_compiler_pin']:
        need(str(q)=='/Library/Developer/CommandLineTools/usr/bin/clang'and s.st_uid==0 and s.st_nlink==1 and bool(s.st_mode&0o111),'only exact frozen readonly current clang role')
    elif str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15':
        need(p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and s.st_uid==os.getuid()and s.st_nlink==p['identity'][3]==2,'only exact frozen original gfortran link exception')
    else:need(s.st_uid==os.getuid()and s.st_nlink==1,'unchanged owned ordinary metadata role')

def tree_bytes(roots):
    """Current metadata-only byte count; never opens any old payload."""
    result=0;seen=set()
    for root in roots:
        root=Path(root);need(root.is_absolute()and root.is_dir()and not any(q.is_symlink()for q in(root,*root.parents)),'literal present counted root')
        for q in root.rglob('*'):
            budget();s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'no alias in counted roots')
            if stat.S_ISREG(s.st_mode):
                need((s.st_dev,s.st_ino)not in seen,'no repeated regular-file inode in counted roots');seen.add((s.st_dev,s.st_ino));result+=s.st_size
    return result

def own_open_unlinked_bytes():
    rows={}
    for name in os.listdir('/dev/fd'):
        try:s=os.fstat(int(name))
        except(ValueError,OSError):continue
        if stat.S_ISREG(s.st_mode)and s.st_nlink==0:rows[s.st_dev,s.st_ino]=s.st_size
    return sum(rows.values())

def save_report(report,prospective_joint_bytes=None):
    report.update(metadata_only=True,Source_author_task=SOURCE_AUTHOR,original_template_Source_author_task=ORIGINAL_TEMPLATE_AUTHOR,actual_executor_task=EXPECTED_EXECUTOR,actual_post_not_executed_by_Source_author=True,helper_imported=False,Source_GEN_or_publication_executed=False,native_or_compiler_executed=False,scientific_numeric_body_decoded=False,context_or_XSM_header_decoded=False,reviewer_Source_pin=pin(Path(__file__).absolute()),wall_seconds=time.monotonic()-START)
    b=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(b)<6*2**20,'post report6MiB')
    need(sum(p.lstat().st_size for p in PACKAGE.rglob('*')if p.is_file())+len(b)<16*2**20,'Source/metadata16MiB including post report')
    if prospective_joint_bytes is not None:need(prospective_joint_bytes+len(b)<2*2**30,'complete current joint plus new post report2GiB')
    with (BASE/'REVIEW.json').open('xb')as f:f.write(b);f.flush();os.fsync(f.fileno())
    budget();print(json.dumps(dict(status=report['status'],review_pin=pin(BASE/'REVIEW.json'))),flush=True)

def main():
    ap=argparse.ArgumentParser(allow_abbrev=False)
    for n in('Root-tools-pin','Host-pin','manifest-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
    a=ap.parse_args();need(a.executor_task_name==EXPECTED_EXECUTOR and a.executor_task_name!=SOURCE_AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'exact independent executor and single immutable post')
    pRoot=json.loads(a.Root_tools_pin);pHost=json.loads(a.Host_pin);pManifest=json.loads(a.manifest_pin)
    raw=meta(pRoot);host=None if pHost is None else meta(pHost);manifest=None if pManifest is None else meta(pManifest);actual=raw['actual_terminal_return']
    need(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and type(actual['exit_code'])is int and actual['exit_code']==raw['original_integer_exit_code']and actual.get('session_id')is None,'genuine closed integer Root return, never live handle inference')
    need(raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False,'original PS guard permission and single actual execution')
    code=raw['original_integer_exit_code']
    if code!=0:
        if pHost is not None:
            need(pHost['path']==str(OUT/'Root_actual_current_B_complete_capture_summary.json')and host['schema']=='ACTUAL_CURRENT_B_COMPLETE_NATIVE_CAPTURE_ROOT_REPORT_V1','actual failed Root report role if emitted')
        if pManifest is not None:need(pManifest['path']==str(OUT/'CURRENT_FORMAL_COMPLETE_B_MATERIAL_OBSERVATION_MANIFEST.json'),'actual manifest role if emitted, no completion inferred')
        partial=file_tree_pins();records=None if host is None else host['records'];checks=None if host is None else host['actual_watchdog_checks'];childcodes=[]
        for check in checks or []:
            observed=check['actual_watchdog'];need(type(observed['returncode'])is int,'only actual saved typed child return retained')
            need(meta(check['actual_watchdog_pin'])==observed,'actual failed-stage watchdog bytes equal saved Host metadata')
            if check['actual_log_pin']is not None:full(check['actual_log_pin'])
            childcodes.append(observed['returncode'])
        report=dict(schema='CURRENT_B_CAPTURE_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_manifest_pin=pManifest,actual_Root_integer_exit_code=code,actual_Host_status=None if host is None else host['status'],actual_Host_failure=None if host is None else host['failure'],actual_stage_records=records,actual_watchdog_checks=checks,actual_recorded_child_integer_exit_codes=childcodes,child_exit_code_inferred_from_Root_return=False,absent_watchdog_child_code_invented=False,new_partial_output_blind_fullEOF_SHA_current7_twice_pins=partial,success_or_complete_capture_inferred=False,actual_B_native_capture_closed0=False,**FALSE)
        save_report(report);return
    need(pHost is not None and pManifest is not None,'Root0 requires genuine Host and manifest exact PF arguments')
    need(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and raw['original_integer_exit_code']==0 and type(actual['exit_code'])is int and actual['exit_code']==0 and actual.get('session_id')is None,'actual closed Root typed0, no live-handle inference')
    need(raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False,'actual original PS permission/no retry')
    result=json.loads(actual['output'].strip().splitlines()[-1]);need(result['report_pin']==pHost and result['manifest_pin']==pManifest and result['actual_B_native_capture_closed0']is True,'genuine Root output binds report and manifest exact PFs')
    need(host['schema']=='ACTUAL_CURRENT_B_COMPLETE_NATIVE_CAPTURE_ROOT_REPORT_V1'and host['status']=='ACTUAL_CURRENT_B_FULL55_CONTEXT_8TREE_4PRODUCT_CAPTURE_CLOSED0_ONLY'and host['failure']is None and host['secondary_failures']==[]and host['final_report_resource_check_passed']is True and host['original_caps']==CAPS,'actual B capture original Root report')
    sf=meta(host['source_freeze_pin']);hf=meta(host['host_freeze_pin']);plan=meta(host['control_plan_pin']);binding=meta(host['actual_B_input_binding_pin']);build=meta(plan['actual_B_IO_build_plan_pin'])
    need(sf['control_plan_pin']==host['control_plan_pin']and hf['selected_source_freeze_pin']==host['source_freeze_pin']and hf['original_caps']==CAPS and host['original_guard_class']=='OwnRSSSerialExecutor'and host['original_guard_MRO_unchanged']is True,'same frozen Source/host/original guard')
    need(sf['schema']=='CURRENT_B_COMPLETE_CAPTURE_SOURCE_FREEZE_V1'and sf['source_only']is True and sf['native_executed']is False and hf['schema']=='CURRENT_B_COMPLETE_CAPTURE_HOST_FREEZE_V1'and hf['source_only']is True and hf['native_executed']is False and len(sf['complete_source_file_pins'])==8,'same exact eight frozen Source roles and Source-only publication')
    peer=meta(sf['independent_Source_review_pin']);peer_tools=meta(sf['independent_Source_review_tools_pin']);peer_actual=peer_tools['actual_review_return'];gen=meta(sf['Root_Source_generation_true_tools_pin']);gen_actual=gen['actual_Source_preparation_return'];ready_pin=pin(PACKAGE/'SOURCE_REVIEW_READY.json');ready=meta(ready_pin)
    need(peer_tools['observed_closed']is True and type(peer_tools['original_integer_exit_code'])is int and peer_tools['original_integer_exit_code']==0 and type(peer_actual['exit_code'])is int and peer_actual['exit_code']==0 and peer_actual.get('session_id')is None and json.loads(peer_actual['output'].strip().splitlines()[-1])['review_pin']==sf['independent_Source_review_pin'],'genuine independent Source review0 binds exact review PF')
    need(peer['source_only']is True and peer['status']=='PASS_SOURCE_ONLY_CURRENT_B_COMPLETE_CAPTURE'and peer['failure']is None and peer['control_plan_pin']==host['control_plan_pin']and peer['complete_source_file_pins']==sf['complete_source_file_pins'],'same-round complete independent Source review')
    need(gen['observed_closed']is True and type(gen['original_integer_exit_code'])is int and gen['original_integer_exit_code']==0 and type(gen_actual['exit_code'])is int and gen_actual['exit_code']==0 and gen_actual.get('session_id')is None and json.loads(gen_actual['output'].strip().splitlines()[-1])['ready_pin']==ready_pin,'genuine Root Source preparation0 binds same READY')
    need(ready['control_plan_pin']==host['control_plan_pin']and ready['complete_source_file_pins']==sf['complete_source_file_pins']and ready['host_source_pin']==hf['host_source_pin']and ready['contract_Source_pin']==hf['contract_Source_pin'],'same READY exact full Source/host/contract roles')
    for p in sf['complete_source_file_pins']:full(p);full(p)
    cli=meta(pin(PACKAGE/'FINAL_ROOT_REVIEWABLE_CLI.json'))
    import shlex
    need(shlex.split(raw['exact_executed_command'])==cli['argv']and shlex.split(cli['command'])==cli['argv']and len(cli['argv'])==24 and cli['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated'and cli['source_freeze_pin']==host['source_freeze_pin']and cli['host_freeze_pin']==host['host_freeze_pin']and hf['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated','actual exact published24argv and identical freeze PFs')
    roots=plan['complete_joint_roots'];latest=meta(plan['latest_complete_plan_pin'])
    need(host['complete_joint_roots']==roots==latest['complete_joint_roots']+[str(OUT)]and len(roots)==len(set(roots))and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y),'entire dynamic latest prefix plus complete own capture root')
    need(build['complete_joint_roots']==roots[:-1][:len(build['complete_joint_roots'])]and any(PACKAGE.is_relative_to(Path(r))for r in roots[:-1]),'entire original build prefix and counted Source remain in dynamic current roots')
    need(plan['bounded_new_capture_output_reservation_bytes']==640*2**20 and plan['bounded_new_Source_metadata_reservation_bytes']==16*2**20 and plan['full_extraction_scope_deferred_not_reduced']is True and plan['new_B_upper_size_forecast_claimed']is False,'capture hard bound without reduced extraction or forecast claim')
    need(len(host['records'])==len(host['actual_watchdog_checks'])==1,'one actual B native child')
    record=host['records'][0];watch=host['actual_watchdog_checks'][0];w=watch['actual_watchdog']
    need(record['status']=='PASS'and record['command']==w['command']and type(w['returncode'])is int and w['returncode']==0 and w['limit_failure']is None and w['own_child_only']is True and w['liveness_group_cleanup']is True and w['rss_cap_mib']==512 and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600,'actual original child0/RSS/wall/liveness closure')
    need(watch['actual_stage_record_label']==record['label']and watch['actual_watchdog_pin']['path']==str(OUT/(record['label']+'.watchdog.json'))and watch['actual_log_pin']['path']==str(OUT/(record['label']+'.log'))and watch['actual_log_pin']['sha256']==record['log_sha256']and meta(watch['actual_watchdog_pin'])==w,'actual original record.label watchdog/log')
    log=full(watch['actual_log_pin']);marker=False;normal=False
    with log.open('rb')as f:
        for line in f:
            marker=marker or re.match(rb'^>\|AXMAT-MATERIAL-B-COMPLETE(?:\s|$)',line)is not None
            normal=normal or b'normal end of execution for dragon'in line
    need(marker and normal,'executed >| completion marker and normal native terminal; no numerical log parsing')
    need(manifest['schema']=='ACTUAL_CURRENT_FORMAL_COMPLETE_OBSERVATION_MANIFEST_V1'and manifest['state_order']==['B']and set(manifest['states'])=={'B'}and manifest['actual_B_observation_executed']is True and manifest['actual_A_observation_executed']is False and manifest['current_B_case_input_binding_pin']==host['actual_B_input_binding_pin']and manifest['original_caps']==CAPS and manifest['library_copy_created']is False,'actual original B-only manifest')
    state=manifest['states']['B'];saved=host['actual_B_state'];need(state==dict(saved,actual_owning_report_pin=pHost),'manifest exact Host state plus immutable owning report PF')
    need(state['current_B_case_input_binding_pin']==host['actual_B_input_binding_pin']and state['actual_executable_pin']==host['new_IO_runtime_pin']==plan['new_IO_runtime_pin']and state['actual_genuine_material_stage']==record and state['actual_command']==record['command'],'exact actual state/build runtime/child record')
    need(state['actual_material_deck_pin']==binding['derived_B_material_deck_pin']and state['original_B_material_deck_pin']==binding['original_B_material_deck_pin']and binding['original_B_native_stage_inputs']==plan['original_B_native_stage_inputs']and state['source_and_input_before_after_checks_completed']is True,'live derived B input with original historical role preserved')
    need(len(binding['original_B_native_stage_inputs'])==7 and [r['destination']for r in binding['original_B_native_stage_inputs']]==['material.x2m','AxMatTone.c2m','geometry.dat','rnr_cc.c2m','rnr_interpol.c2m','DLIB_ACTUAL','DLIB8R1_370']and binding['original_caps']==CAPS and binding['library_copy_created']is False and binding['historical_B_context_claimed']is False,'all original seven B inputs and no SCI copy/history relabelling')
    for row in binding['original_B_native_stage_inputs']:current(row['input_pin'])
    for p in binding['actual_consumed_readonly_cwd_role_pins'].values():current(p)
    current(plan['new_IO_runtime_pin'])
    need(host['all_old_cwd_entries_current7_before']==host['all_old_cwd_entries_current7_after']==state['all_old_cwd_entries_current7_before']==state['all_old_cwd_entries_current7_after']==binding['all_old_cwd_entries_current7_before_child']==plan['all_old_cwd_entries_current7_before_child'],'all old cwd current7 preserved before/after')
    cwd=Path(binding['actual_native_cwd']);now={p.name:identity(p.lstat())for p in cwd.iterdir()if p.name!='b63'};need(now==host['all_old_cwd_entries_current7_before'],'all old cwd identities still current; no old-output mutation/new scratch')
    products=state['actual_material_product_pins'];contexts=state['complete_context_pins'];trees=state['complete_state_snapshot_inputs'];events=state['actual_all_event_headers_in_original_execution_order']
    need([Path(p['path']).name for p in products]==['m.xsm','u.asc','a.asc','t.asc']and len(contexts)==len(events)==55 and len(trees)==8,'all4 complete products/55 events/8 whole XSM trees')
    need([e['event']for e in events]==list(range(1,56))and [e['complete_context_pin']for e in events]==contexts,'consecutive original event order and exact full context PFs')
    for n,p in enumerate(contexts,1):need(p['path']==str(OUT/('axobs-'+format(n,'06d')+'.context.bin')),'literal consecutive complete observer context names')
    snapshots=[e['actual_snapshot_pin']for e in events if e['actual_snapshot_pin']is not None]
    need(snapshots==[r['input_pin']for r in trees]and state['complete_observed_file_pins']==contexts+snapshots,'all whole native snapshot roles retained')
    for row in trees:
        need(row['input_pin']['path']==str(OUT/('axobs-'+format(row['event'],'06d')+'-'+row['role']+'.xsm'))and row['root_prefix']==[]and row['logical_prefix']==([]if row['role']=='final-complete-micro'else['MACROLIB']),'exact original native/logical snapshot role distinction')
    need(all(type(e['event'])is int and type(e['libmix'])is int for e in events)and all(e['libmix']>=events[i-1]['libmix']for i,e in enumerate(events)if i),'saved typed event order/libmix metadata only')
    need(any(e['label']=='TONDRV_FINAL_AFTER_SHIBA'for e in events)and any(e['label']=='TONDRV_ACTUAL_SPH_CALL_DECISION'for e in events)and state['all_actual_events_and_snapshots_saved']is True and state['actual_material_child_closed_before_manifest']is True and state['all_producer_file_handles_closed_before_next_state']is True,'actual complete final/SPH decision capture after child closure')
    expected_observer={Path(p['path']).name for p in contexts+snapshots};need({p.name for p in OUT.glob('axobs-*')}==expected_observer,'no missing/unrecorded observer file namespace')
    newpins=file_tree_pins()
    table={p['path']:p for p in newpins}
    for p in products+contexts+snapshots+[pHost,pManifest,host['actual_B_input_binding_pin'],watch['actual_watchdog_pin'],watch['actual_log_pin']]:need(table[p['path']]==p,'all actual captured operand/control fullPFs blind-SHA match')
    for p in newpins:full(p)
    ownbytes=sum(p['size_bytes']for p in newpins);need(ownbytes<640*2**20,'entire output including native products/context/trees/CLE caches/log/watch/report/manifest640MiB')
    saved_resources(host['resources_before']);saved_resources(host['resources_after'])
    joint=tree_bytes(roots)
    extra=0
    for p in hf['explicit_cumulative_metadata_file_pins']:
        q=Path(p['path']);current_metadata_role(p,build)
        if not any(q.is_relative_to(Path(r))for r in roots):extra+=p['size_bytes']
    unlinked=own_open_unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current complete cumulative2GiB and free8GiB reserve including own open-unlinked')
    need(host['resources_before']['complete_joint']['resource_roots']==host['resources_after']['complete_joint']['resource_roots']==roots,'actual original resource facts counted same full dynamic roots before/after')
    prospective=host['resources_before']['complete_joint']['artifact_bytes']+host['resources_before']['explicit_external_metadata_bytes']+host['resources_before']['host_open_unlinked_bytes']
    need(prospective+640*2**20+16*2**20<2*2**30 and binding['prospective_existing_joint_bytes']==prospective and binding['complete_latest_prefix_roots']==roots[:-1],'actual pre-native original full640MiB+Source16 reserve and complete current prefix')
    for _ in range(2):
        for p in plan['inherited_metadata_current7_pins']:current_metadata_role(p,build)
    for key in FALSE:need(host[key]is False,'all Host scientific/completion qualification flags remain false')
    for item in(host,manifest,state):
        for k in FALSE:
            if k in item:need(item[k]is False,'no extraction/OVERV/online/physics/AAA/ABA qualification minted')
    for p in(pRoot,pHost,pManifest,host['source_freeze_pin'],host['host_freeze_pin'],host['control_plan_pin']):full(p)
    report=dict(schema='RECORDED_CURRENT_B_COMPLETE_CAPTURE_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_CURRENT_B_FULL4PRODUCT_55CONTEXT_8TREE_CAPTURE_CHILD0_METADATA_ONLY',failure=None,metadata_only=True,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_manifest_pin=pManifest,actual_Root_integer_exit_code=0,actual_child_integer_exit_code=0,actual_stage_record=record,actual_watchdog_check=watch,complete_joint_roots=roots,original_caps=CAPS,actual4_material_product_pins=products,actual55_complete_context_pins=contexts,actual8_complete_snapshot_input_rows=trees,new_output_blind_fullEOF_SHA_current7_twice_pins=newpins,entire_capture_output_bytes=ownbytes,actual_B_input_binding_pin=host['actual_B_input_binding_pin'],new_runtime_current7_only_pin=plan['new_IO_runtime_pin'],original7_B_inputs_and_readonly_CWD_current7_only=True,historical_original_deck_seed_pin_not_live_identity=True,all_old_cwd_current7_preserved=True,current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_own_open_unlinked_bytes=unlinked,actual_Source_review_pin=sf['independent_Source_review_pin'],actual_Source_review_tools_pin=sf['independent_Source_review_tools_pin'],actual_Root_Source_generation_tools_pin=sf['Root_Source_generation_true_tools_pin'],same8_frozen_Source_roles_rechecked_whole_twice=True,dynamic_complete_prefix_verified_without_fixed_root_count=True,original_host_resource_facts_before=host['resources_before'],original_host_resource_facts_after=host['resources_after'],original_resource_caps_preserved_without_reconstruction=True,Source_author_task=SOURCE_AUTHOR,original_template_Source_author_task=ORIGINAL_TEMPLATE_AUTHOR,actual_executor_task=a.executor_task_name,actual_post_not_executed_by_Source_author=True,helper_imported=False,Source_GEN_or_publication_executed=False,native_or_compiler_executed=False,scientific_numeric_body_decoded=False,context_or_XSM_header_decoded=False,full_extraction_scope_deferred_not_reduced=True,reviewer_Source_pin=pin(Path(__file__).absolute()),wall_seconds=time.monotonic()-START,**FALSE)
    save_report(report,joint+extra+unlinked)

if __name__=='__main__':main()
