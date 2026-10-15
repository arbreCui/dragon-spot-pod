#!/usr/bin/env python3
"""Source-only producer for postverification after the genuine v18 terminal.

The static v16 contract supplies only original50 labels/exact33 messages.
Current v18 frozen authorities and original owned-runtime Root1 supplemental
facts are bound explicitly. This Source preparation never reads running OUT.

All future authorities are required external fullpins. Never import/run the
business Host, compiler, transport or cleanup. A successful engineering gate
requires the genuine terminal0, exact50, all33 intended exit1 and sealed full
pair readback. A genuine failed terminal is reported with non-PASS status and
its real failure; it never gains an engineering or physics gate.
"""
import argparse,ast,collections,hashlib,importlib.util,json,math,os,resource,shlex,stat,time
from pathlib import Path

REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
HERE=REC/'aaa_three_plane_A8_owned_MAP_pipeline_source_v18_20261014'
CURRENT_HF_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/aaa_three_plane_A8_owned_MAP_pipeline_source_v18_20261014/COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json', 'sha256': '37ca44143c9179e00dd290b26cda61c56ef3a9d1c93df6be9011fe51578ae94c', 'size_bytes': 1722775, 'identity': [16777229, 50120631, 33188, 1, 1722775, 1791947567522486241, 1791947567522486241]}
CURRENT_CLI_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/aaa_three_plane_A8_owned_MAP_pipeline_source_v18_20261014/DECLARED_EXECUTION_INTERFACE.json', 'sha256': 'c7f6db729fda6dd336dc8f9865d40f7b718dda354447e8914db9e61347c7a044', 'size_bytes': 57358, 'identity': [16777229, 50120632, 33188, 1, 57358, 1791947567524356662, 1791947567524356662]}
CURRENT_PLAN_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/aaa_three_plane_A8_owned_MAP_pipeline_source_v18_20261014/ACTUAL_OWNED_RUNTIME_BOUND_V17_SOURCE_PREPARATION_PLAN.json', 'sha256': 'eb4d36e1a4daa5082fd7c2150a60faa32974f85b37251bbb9527b579592a4aa0', 'size_bytes': 1692307, 'identity': [16777229, 50120455, 33188, 1, 1692307, 1791947315796575469, 1791947315796575469]}
CONTRACT_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/independent_v16_actual_terminal_postverification_preparation_20261014/TERMINAL_POSTVERIFICATION_SOURCE_CONTRACT.json', 'sha256': 'b3395e79e57715fd62bc2e43f0a9cb4fff3cbab41e3e332fec67548e715266f8', 'size_bytes': 10327, 'identity': [16777229, 50087490, 33188, 1, 10327, 1791919976589153023, 1791919976589153023]}
START=time.monotonic()

def guard():
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20 or time.monotonic()-START>=1800:
        raise RuntimeError('original independent SELF512/whole1800 bound')

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def ancestors(p):
    p=Path(p)
    if not p.is_absolute()or '..'in p.parts:raise RuntimeError('canonical absolute path')
    for q in reversed(p.parents):
        if not stat.S_ISDIR(q.lstat().st_mode):raise RuntimeError('ordinary no-symlink ancestor '+str(q))

def norm(p):return{k:p[k]for k in ('path','sha256','size_bytes','identity')}

def seven(p):
    p=norm(p);q=Path(p['path']);ancestors(q);s=q.lstat()
    if not stat.S_ISREG(s.st_mode)or identity(s)!=p['identity']or s.st_size!=p['size_bytes']:
        raise RuntimeError('current7 changed '+str(q))
    guard()

def eof(path,expected=None,retain=False):
    q=Path(path);ancestors(q);a=q.lstat();ident=identity(a)
    if not stat.S_ISREG(a.st_mode):raise RuntimeError('regular fullEOF file')
    if retain and a.st_size>64*2**20:raise RuntimeError('bounded metadata64MiB')
    h=hashlib.sha256();n=0;parts=[];fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        if identity(os.fstat(fd))!=ident:raise RuntimeError('fullEOF opened7 changed')
        while True:
            raw=os.read(fd,1024*1024)
            if not raw:break
            h.update(raw);n+=len(raw)
            if retain:parts.append(raw)
            guard()
        if identity(os.fstat(fd))!=ident:raise RuntimeError('fullEOF FD changed')
    finally:os.close(fd)
    if identity(q.lstat())!=ident or n!=a.st_size:raise RuntimeError('fullEOF after7 changed')
    p=dict(path=str(q),sha256=h.hexdigest(),size_bytes=n,identity=ident)
    if expected is not None and p!=norm(expected):raise RuntimeError('exact fullEOF mismatch '+str(q))
    return p,b''.join(parts)if retain else None

def load(p):
    _,raw=eof(p['path'],p,True);return json.loads(raw)

def unique(rows):
    table={}
    for r in rows:
        p=norm(r)
        if p['path']in table and table[p['path']]!=p:raise RuntimeError('inconsistent fullPF '+p['path'])
        table[p['path']]=p
    return list(table.values())

def inventory(root):
    files={};dirs={};stack=[root]
    while stack:
        q=stack.pop();ancestors(q);s=q.lstat();before=identity(s)
        if not stat.S_ISDIR(s.st_mode):raise RuntimeError('ordinary OUT directory')
        dirs[str(q)]=before;fd=os.open(q,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:
            if identity(os.fstat(fd))!=before:raise RuntimeError('directory opened7')
            with os.scandir(fd)as it:
                for e in it:
                    p=q/e.name;a=e.stat(follow_symlinks=False)
                    if stat.S_ISDIR(a.st_mode):stack.append(p)
                    elif stat.S_ISREG(a.st_mode):
                        if a.st_nlink!=1 or a.st_uid!=os.getuid():raise RuntimeError('actual owning file UID/singlelink')
                        files[str(p)]=identity(a)
                    else:raise RuntimeError('OUT symlink/special entry')
            if identity(os.fstat(fd))!=before or identity(q.lstat())!=before:raise RuntimeError('directory after7')
        finally:os.close(fd)
        guard()
    return dict(files=files,directories=dirs)

def finite(v):return type(v)in(int,float)and math.isfinite(v)

def actual_stage(root,record,index,expected_refusal,source_abort_strings):
    wp,_=eof(root/(record['label']+'.watchdog.json'));w=load(wp)
    lp,log=eof(root/(record['label']+'.log'),retain=True)
    if w['command']!=record['command']or w['rss_cap_mib']!=512 or w['own_child_only']is not True or \
       w['liveness_group_cleanup']is not True or type(w['returncode'])is not int or \
       type(w['pid'])is not int or w['pid']<=0 or \
       not finite(w['sampled_peak_rss_mib'])or not 0<=w['sampled_peak_rss_mib']or \
       not finite(w['elapsed_seconds'])or not 0<w['elapsed_seconds']or \
       not finite(w['wall_cap_seconds'])or not 0<w['wall_cap_seconds']<=600:
        raise RuntimeError('true own-child watch/command/caps')
    intended=expected_refusal is not None
    if intended:
        r=expected_refusal
        if record['status']!='FAILED'or w['returncode']!=1 or w['limit_failure']is not None or \
           r['actual_exit_code']!=1 or r['original_execution_record_index']!=index or \
           r['original_execution_record_label']!=record['label']or norm(r['actual_log_pin'])!=lp or norm(r['actual_watchdog_pin'])!=wp or \
           any(r[k]is not True for k in ('actual_abort_message_exact','pre_transport_abort_at_frozen_validation_branch',
             'no_positive_solver_or_seal_trace','all_actual_assertions_completed'))or \
           r['expected_abort']not in source_abort_strings or log.count(r['expected_abort'].encode())!=1 or \
           not w['elapsed_seconds']<w['wall_cap_seconds']<=record['wall_cap_seconds']<=600:
            raise RuntimeError('exact frozen intended refusal1, before positive solver/seal')
        forbidden=(b'SPOR64_BOOTB64-CENSUS:',b'ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1',
          b'ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE',b'ACTUAL-AAA3-NATIVE-GLOBAL-COMPLETE',
          b'SPOT-R64 B2I BOOTSTRAP COMMITTED',b'SPOT-X-REAL64-TERMINAL',b'FLU2DR-TERM')
        if 'entry_invocation'in r:forbidden+= (b'kernel error',b'INCONSISTENT CALL',b'TARGET GUARD RETURNED')
        if any(x in log for x in forbidden):raise RuntimeError('positive trace in intended pre-kernel refusal')
    elif record['status']=='PASS':
        if w['returncode']!=0 or w['limit_failure']is not None or record['log_sha256']!=lp['sha256']or \
           not w['elapsed_seconds']<w['wall_cap_seconds']<=record['wall_cap_seconds']<=600:
            raise RuntimeError('actual PASS stage closed0/no limit/full log')
    elif record['status']!='FAILED' or w['returncode']==0:
        raise RuntimeError('unqualified actual unexpected failure shape')
    return dict(index=index,label=record['label'],status=record['status'],intended_refusal=intended,
      watch_pin=wp,log_pin=lp,actual_watch=w),log

def resource_snapshot(s,root):
    if s['artifact_budget_bytes']!=96*2**30 or s['min_free_bytes']!=8*2**30 or \
       type(s['artifact_bytes'])is not int or not 0<=s['artifact_bytes']<=96*2**30 or s['disk_free_bytes']<8*2**30:
        raise RuntimeError('original family96/free8 recorded resources')
    f=s['fresh_output']
    if f['artifact_budget_bytes']!=2*2**30 or f['resource_roots']!=[str(root)]or \
       type(f['artifact_bytes'])is not int or not 0<=f['artifact_bytes']<=2*2**30 or f['disk_free_bytes']<8*2**30:
        raise RuntimeError('same physical fresh2 recorded resources')

def closed_provenance(summary,hf,fixed):
    cache=summary['actual_cache336_driver_and_budget_bit_admission'];compact=summary['actual_compact_expected_reader_admission']
    if cache['complete70_replacement_zero_based_index']!=37 or cache['actual_assertions']!=338 or cache['actual_calls']!=121 or \
       cache['bit_actual_compiler_executed']is not True or cache['bit_actual_compile_link_stage_count']!=2 or \
       cache['new_driver_build_report_pin']!=hf['selected_actual_cache336_build_report_pin']or \
       cache['new_Driver_Fortran_Source_freeze_pin']!=hf['selected_cache336_Fortran_Source_freeze_pin']or \
       cache['new_Driver_Host_freeze_pin']!=hf['selected_cache336_build_Host_freeze_pin']or \
       cache['budget_bit_report_pin']!=hf['selected_actual_cache336_budget_bit_report_pin']or \
       cache['budget_bit_Host_freeze_pin']!=hf['selected_cache336_budget_bit_Host_freeze_pin']or \
       cache['retained_compact_build_report_pin']!=hf['selected_actual_new_build70_report_pin']or \
       cache['retained_compact_Fortran_Source_freeze_pin']!=hf['selected_new_Fortran_Source_freeze_pin']or \
       compact['new_build70_report_pin']!=hf['selected_actual_new_build70_report_pin']:
        raise RuntimeError('separate Driver37 → retained compact40 lineage and actual338/121')
    build=load(cache['new_driver_build_report_pin']);bits=load(cache['budget_bit_report_pin'])
    post=load(hf['selected_cache336_bits_actual_post_review_pin'])
    disparity=post['known_summary_metadata_discrepancy']
    if cache['bit_known_summary_metadata_discrepancy']!=disparity or bits['compiler_executed']is not False or \
       disparity['field']!='compiler_executed'or disparity['reported_value']is not False or disparity['actual_value']is not True or \
       disparity['actual_report_pin']!=cache['budget_bit_report_pin']or disparity['actual_Host_Source_pin']!=load(cache['budget_bit_Host_freeze_pin'])['host_source']or \
       post['actual_compiler_executed']is not True or post['actual_compile_link_stage_count']!=2 or post['actual_watch_stage_count']!=3:
        raise RuntimeError('explicit original sealed Bit compiler metadata discrepancy')
    old70=build['original_ordered70_input_pins'];new70=build['actual_complete70_link_inputs']
    if len(old70)!=70 or len(new70)!=70 or [i for i,(p,q)in enumerate(zip(old70,new70))if p['path']!=q]!=[37]or \
       new70[40]!=load(hf['selected_actual_new_build70_report_pin'])['actual_complete70_link_inputs'][40]or \
       new70[57]!=build['original_ordered70_input_pins'][57]['path']:
        raise RuntimeError('final70 onlyDriver37; compactBOOTQ40 and unchanged math57')
    for p in old70+build['original_nine_core_object_pins']:
        if fixed.get(p['path'])!=norm(p):raise RuntimeError('all old70 and current9 exact in actual fixed')
        eof(p['path'],p)
    return cache,compact,old70,disparity

def genuine_terminal(result,code):
    if type(result.get('exit_code'))is not int or result['exit_code']!=code or result.get('session_id')is not None or not isinstance(result.get('output'),str):
        raise RuntimeError('genuine original typed closed terminal '+str(code))

def actual_post_tool(tools,review):
    if tools.get('observed_closed')is not True or type(tools.get('original_integer_exit_code'))is not int or tools['original_integer_exit_code']!=0:
        raise RuntimeError('actual independent original closed0 post')
    for k in ('actual_review_return','actual_postverification_return'):
        r=tools[k];genuine_terminal(r,0);lines=r['output'].strip().splitlines()
        if not lines or json.loads(lines[-1])['review_pin']!=review:raise RuntimeError('exact original post stdout review fullPF')

def owned_provenance(summary,hf,fixed,plan):
    # Original Root1 remains a real Host parser failure. Only the three child
    # stages and independent original-helper complete readback are closed0.
    import re
    keys=('selected_actual_owned_runtime_report_pin','selected_owned_runtime_Host_freeze_pin','selected_owned_Fortran_Source_freeze_pin',
      'selected_owned_runtime_plan_pin','selected_owned_runtime_CLI_pin','selected_owned_runtime_Root_tools_pin','selected_owned_runtime_Root_argv_pin',
      'selected_owned_runtime_post_review_pin','selected_owned_runtime_post_tools_pin')
    authorities={k:norm(hf[k])for k in keys};data={k:load(v)for k,v in authorities.items()}
    for p in authorities.values():
        if fixed.get(p['path'])!=p:raise RuntimeError('owned selected authority absent from current full50 fixed')
    pr,ph,ps,pp,pc,pt,pa,pv,pvt=[authorities[k]for k in keys]
    rep,own,sf,rplan,cli,rt,argv,post,tools=[data[k]for k in keys]
    if sf['schema']!='COMPLETE_SPOR64_A8_18_CALLER_OWNED_MAP_LIFETIME_FORTRAN_SOURCE_ONLY_FREEZE_V1'or \
       sf['replacement_zero_based_link_index']!=1 or sf['caller_owned_site_count']!=18 or sf['original_module6092_wholebyte_equality_required']is not True or \
       len(sf['Source_flags'])!=9 or any(v is not True for v in sf['Source_flags'].values())or \
       own['selected_diag_Fortran_Source_freeze_pin']!=ps or rep['actual_diagnostic_Fortran_Source_freeze_pin']!=ps or rep['actual_host_Source_freeze_pin']!=ph:
        raise RuntimeError('actual owned18 Source flag9 and only1 frozen ABI contract')
    if post['schema']!='INDEPENDENT_A8_18_OWNED_MAP_LIFETIME_V2_ACTUAL_RUNTIME_POSTVERIFICATION_V1'or \
       post['status']!='PASS_ACTUAL_A8_18_OWNED_MAP_LIFETIME_V2_THREE_STAGE0_COMPLETE_PAIR_FACTS_POSTVERIFIED_HOST_COMPLETION_PARSER_FAILURE_RETAINED'or \
       post['failure']is not None or post['verification_failure']is not None or \
       any(post[k]is not False for k in ('business_executed','compiler_executed','numerical_executed','files_deleted','full50_executed','engineering_qualified','physics_qualified'))or \
       post['actual_owner_bit_control_results']is not None or post['actual_report_pin']!=pr or post['actual_Host_freeze_pin']!=ph or \
       post['actual_CLI_pin']!=pc or post['actual_Root_true_tool_return_pin']!=pt or post['actual_Root_exact_argv_pin']!=pa or post['actual_Fortran_Source_freeze_pin']!=ps or \
       type(post['actual_Root_exit_code'])is not int or post['actual_Root_exit_code']!=1 or post['actual_Root_closed']is not True or \
       post['actual_stage_count']!=3 or post['actual_stage_statuses']!=['PASS','PASS','PASS']or type(post['actual_BOOT_exit_code'])is not int or post['actual_BOOT_exit_code']!=0 or \
       any(post[k]is not True for k in ('actual_single_BOOT_completed','all_three_watches_closed_without_limit_failure','actual_terminal_pair_full370x3_readback_verified','only_ordered70_index1_changed','actual_other69_ordered70_inputs_full_EOF_unchanged','actual_module6092_fullSHA_matches_original')):
        raise RuntimeError('strict transparent Root1/3child0/complete pair independent post0')
    actual_post_tool(tools,pv);genuine_terminal(rt['actual_terminal_return'],1)
    if rt['observed_closed']is not True or type(rt['original_integer_exit_code'])is not int or rt['original_integer_exit_code']!=1 or \
       shlex.split(rt['exact_executed_command'])!=argv['exact_argv']or argv['exact_argv']!=cli['exact_reviewable_argv']or len(argv['exact_argv'])!=42 or \
       argv['interface_pin']!=pc or argv['Host_freeze_pin']!=ph or rep['failure']!=post['actual_summary_failure']or not isinstance(rep['failure'],str)or rep['first_failure_secondary_errors']!=[]or \
       rep['actual_outcome']is not None or [r['status']for r in rep['records']]!=['PASS','PASS','PASS']:
        raise RuntimeError('sealed original parser failure and genuine actual threePASS kept')
    oldroot=Path(pr['path']).parent;oldw=[];oldlog=None
    for i,record in enumerate(rep['records']):
        w,log=actual_stage(oldroot,record,i,None,set());oldw.append(w)
        if i==2:oldlog=log
    if any(x['actual_watch']['returncode']!=0 or x['actual_watch']['limit_failure']is not None for x in oldw):raise RuntimeError('all original owned runtime child watches0')
    lines=oldlog.decode('utf-8',errors='strict').splitlines();pattern=r'^>\|ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE[ \t]+\|>0031$'
    completions=[s for s in lines if re.fullmatch(pattern,s)]
    listing=[s for s in lines if 'ECHO "ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE"'in s]
    seals=[json.loads(s)for s in lines if s.startswith('{"schema":"ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1"')]
    if len(completions)!=1 or completions!=post['actual_completion_stdout_lines']or len(listing)!=1 or listing!=post['actual_completion_deck_listing_lines_not_execution_evidence']or \
       len(seals)!=1 or seals[0]!=post['actual_Fortran_complete_copy_readback']:
        raise RuntimeError('one executed decorated completion excludes decklisting and one real seal')
    seal=seals[0]
    if seal['status']!='PASS'or (seal['groups'],seal['planes'],seal['epoch'])!=(370,3,0)or seal['all_payload_bits_equal']is not True or seal['complete_lifecycle_checked']is not True or \
       post['actual_terminal_pair_readback']!=post['complete_terminal_readback']:
        raise RuntimeError('all370×3 original seal bits and whole-field independent helper return')
    readback=post['actual_terminal_pair_readback'];planes=readback['planes']
    if readback['rank_values']!=370 or readback['rank1_all_groups']is not True or len(planes)!=3 or [p['plane']for p in planes]!=[1,2,3]or \
       any(p['groups']!=370 or p['unknowns']!=14 or p['fission_components']!=32 or p['flux_values']!=370*14 or p['source_values']!=370*14 or p['SYSTEM_full370_SPOT_S0_PHYS_checked']is not True for p in planes):
        raise RuntimeError('original full370×3 pair readback contract, no second old tree read')
    new70=post['actual_ordered70_input_pins'];old70=rplan['current_ordered70_input_pins'];core=rplan['current_nine_core_object_pins']
    if len(new70)!=70 or len(old70)!=70 or len({p['path']for p in new70})!=70 or \
       [i for i,(a,b)in enumerate(zip(old70,new70))if norm(a)!=norm(b)]!=[1]or new70[1]!=post['actual_new_object1_pin']or \
       new70!=hf['current_owned_runtime_ordered70_pins']or new70!=plan['current_owned_runtime_ordered70_pins']or rep['actual_ordered70_link_inputs']!=[p['path']for p in new70]or \
       [p for p in new70 if p['path'].endswith('.a')]!=rplan['original_four_archive_pins']:
        raise RuntimeError('genuine final runtime70 only1, separate Driver37/Q40/math57/archive chain')
    mod=post['actual_Module_ABI_pin'];oldmod=post['original_Module_ABI_pin']
    if oldmod!=rplan['selected_original_A8_module_pin']or mod['size_bytes']!=6092 or mod['sha256']!=oldmod['sha256']or oldmod['size_bytes']!=6092:
        raise RuntimeError('actual module6092 whole-byte ABI equality')
    for p in unique(new70+core+[mod,oldmod,sf['diagnostic_source_pin']]+sf['files']):
        if fixed.get(p['path'])!=norm(p):raise RuntimeError('actual only1/runtime69/module/Source fullPF not current fixed')
        eof(p['path'],p)
    for k in ('actual_terminal_axial_pin','actual_terminal_archive_pin'):seven(post[k])
    ck=('selected_exact18_manifest_pin','selected_exact18_release_receipt_pin','selected_exact18_Root_tools_pin','selected_exact18_Root_argv_pin','selected_exact18_post_review_pin','selected_exact18_post_tools_pin','selected_exact18_release_Source_freeze_pin')
    cp={k:norm(hf[k])for k in ck};cv={k:load(p)for k,p in cp.items()}
    manifest,receipt,roottools,rargv,rpost,rtools,rsf=[cv[k]for k in ck];pm,prec,prtools,parg,pref,preft,prsf=[cp[k]for k in ck]
    expected=rsf['literal18_fullpins'];contract=hf['exact18_release_contract']
    if len(expected)!=18 or sum(p['size_bytes']for p in expected)!=1604468368 or len({p['path']for p in expected})!=18 or \
       manifest['schema']!=contract['manifest_schema']or manifest['selected_Source_freeze_pin']!=prsf or manifest['target_full_EOF_pins']!=expected or \
       receipt['schema']!=contract['receipt_schema']or receipt['status']!=contract['receipt_status']or rsf['schema']!=contract['Source_freeze_schema']or \
       receipt['manifest_pin']!=pm or receipt['deleted_files']!=18 or receipt['logical_bytes_released']!=1604468368 or receipt['next_target_intent']is not None or \
       len(receipt['deletion_records'])!=18 or any(r['original_fullpin']!=p or any(r[k]is not True for k in ('actual_unlink_returned','target_directory_fsync_attempted','target_directory_fsync_returned','confirmed_absent'))for r,p in zip(receipt['deletion_records'],expected)):
        raise RuntimeError('exact18 whole-PF ordered historical retirement, no generic missing skip')
    actual_post_tool(rtools,pref);genuine_terminal(roottools['actual_terminal_return'],0)
    if roottools['observed_closed']is not True or type(roottools['original_integer_exit_code'])is not int or roottools['original_integer_exit_code']!=0 or \
       shlex.split(roottools['exact_executed_command'])!=rargv['execute_argv']or len(rargv['execute_argv'])!=17 or rargv['execute_argv'].count('--execute')!=1 or rargv['execute_argv'][-1]!='--execute'or rargv['manifest_pin']!=pm or \
       rpost['schema']!='INDEPENDENT_LITERAL18_CAPTURE_AND_OWNED_DUPLICATE_NINES_ACTUAL_EXACT_RELEASE_POSTVERIFICATION_V1'or \
       rpost['status']!='PASS_ACTUAL_LITERAL18_CAPTURE_AND_OWNED_DUPLICATE_NINES_EXACT_RELEASE_POSTVERIFICATION'or rpost['failure']is not None or \
       any(rpost[k]is not False for k in ('business_executed','compiler_executed','numerical_executed','deletion_executed_by_reviewer'))or \
       rpost['actual_release_receipt_pin']!=prec or rpost['actual_Root_true_tool_pin']!=prtools or rpost['actual_manifest_pin']!=pm:
        raise RuntimeError('actual exact18 Root0 and independent post0 authorities')
    retired={p['path']for p in expected}
    if any(Path(p).exists()or Path(p).is_symlink()or p in fixed for p in retired):raise RuntimeError('only18 absent bodies strictly historical and excluded from current fixed')
    original9=hf['retained_original_science_nine_input_pins']
    if len(original9)!=9 or original9!=plan['retained_original_science_nine_input_pins']or any(p['path']in retired or fixed.get(p['path'])!=norm(p)for p in original9):
        raise RuntimeError('exact original science9 current, none borrowed from retired copies')
    for p in original9:seven(p)
    fact=summary['actual_A8_owned_MAP_runtime_admission']
    expected_fact=dict(actual_runtime_report_pin=pr,actual_Root_true_tool_return_pin=pt,actual_Root_exact_argv_pin=pa,actual_post_review_pin=pv,actual_post_tools_pin=pvt,
      actual_owned_Fortran_Source_freeze_pin=ps,actual_owned_Host_freeze_pin=ph,actual_object1_pin=new70[1],actual_module6092_pin=mod,actual_ordered70_input_pins=new70,
      single_boot_completed=True,full50_executed=False,engineering_qualified=False,physics_qualified=False,actual_owner_bit_control_results=None,
      actual_exact18_role_retirement_proof_pins={k:hf[k]for k in ck},retained_original_science9_pins=original9)
    if fact!=expected_fact:raise RuntimeError('exact published owned runtime admission facts not reconstructed or promoted')
    return dict(actual_admission=fact,current70_fullpins=new70,original_science9_pins=original9,retired18_historical_fullpins=expected,
      original_owned_Runtime_Root_exit_code=1,original_owned_Runtime_three_child_exit_codes=[0,0,0],original_owned_Host_parser_failure=rep['failure'],
      original_seal=seal,independent_original_helper_complete_readback_post_pin=pv,exact18_release_receipt_pin=prec,exact18_post_review_pin=pref,
      prior_sealed_pair_tree_not_read_again=True,actual_owner_bit_control_results=None)

def sealed_pair(summary,root,hf,fixed,bootlog):
    result=summary['actual_terminal']
    if not isinstance(result,dict):raise RuntimeError('real full sealed terminal required')
    ax=result['AX_full_pin'];arc=result['ARCHIVE_full_pin']
    if ax['path']!=str(root/'AAA/closed_boot_axial.xsm')or arc['path']!=str(root/'AAA/closed_boot_archive.xsm'):
        raise RuntimeError('exact final owning sealed pair only')
    eof(ax['path'],ax);eof(arc['path'],arc)
    readbacks=[]
    for line in bootlog.decode('utf-8',errors='strict').splitlines():
        if line.startswith('{"schema":"ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1"'):readbacks.append(json.loads(line))
    if len(readbacks)!=1:raise RuntimeError('one genuine complete Fortran seal/copy readback')
    r=readbacks[0]
    if r!=result['actual_Fortran_complete_copy_readback']or r['status']!='PASS'or \
       r['all_payload_bits_equal']is not True or r['complete_lifecycle_checked']is not True or \
       (r['groups'],r['planes'],r['epoch'])!=(370,3,0)or r['AAA_qualified']is not False or r['ABA_admitted']is not False:
        raise RuntimeError('complete all-field pair bits before private stage disposal')
    plan=load(hf['actual_prerequisite_bound_Source_plan_pin'])
    candidates=[h['candidate_pin']for h in plan['helper_byte_equality']if Path(h['candidate_pin']['path']).name=='actual_inputs_and_readback.py']
    if len(candidates)!=1 or fixed.get(candidates[0]['path'])!=norm(candidates[0]):raise RuntimeError('exact bounded read-only pair helper')
    helper=candidates[0];eof(helper['path'],helper)
    parser=Path('/Users/wen/spot/validation/axial_material/snapshot_control_preflight.py')
    if str(parser)not in fixed:raise RuntimeError('frozen bounded XSM parser in fixed authority')
    eof(parser,fixed[str(parser)])
    # Only this known read-only helper is imported after its exact Source pin.
    # It contains bounded pread/parser checks; no Host or solver is imported.
    spec=importlib.util.spec_from_file_location('v18_frozen_readonly_pair_data',helper['path']);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    observed=module.final_readback(Path(ax['path']),Path(arc['path']))
    observed=json.loads(json.dumps(observed,allow_nan=False))
    if observed!=result['actual_terminal']:raise RuntimeError('every complete terminal/tree/typed/mirror field differs')
    planes=observed['planes']
    if len(planes)!=3 or [p['plane']for p in planes]!=[1,2,3]or observed['rank1_all_groups']is not True or observed['rank_values']!=370 or \
       any(p['groups']!=370 or p['unknowns']!=14 or p['flux_values']!=370*14 or p['source_values']!=370*14 or \
         p['SYSTEM_full370_SPOT_S0_PHYS_checked']is not True or p['fission_components']!=32 for p in planes):
        raise RuntimeError('actual full370×3 typed flux/source and physical system fields')
    eof(ax['path'],ax);eof(arc['path'],arc)
    return result,helper,observed

def main():
    ap=argparse.ArgumentParser(allow_abbrev=False)
    for name in ('report','Root-tools','Root-argv','Host-freeze','CLI'):
        for suffix in ('summary','sha256','seven-id'):ap.add_argument('--'+name+'-'+suffix,required=True)
    ap.add_argument('--review-directory',required=True);a=ap.parse_args()
    def external(name):
        attr=name.replace('-','_');p,_=eof(getattr(a,attr+'_summary'))
        if p['sha256']!=getattr(a,attr+'_sha256')or p['identity']!=json.loads(getattr(a,attr+'_seven_id')):raise RuntimeError('exact external PF '+name)
        return p
    pins={n:external(n)for n in ('report','Root-tools','Root-argv','Host-freeze','CLI')}
    summary=load(pins['report']);tool=load(pins['Root-tools']);argv=load(pins['Root-argv']);hf=load(pins['Host-freeze']);cli=load(pins['CLI'])
    terminal=tool['actual_terminal_return'];initial=tool['actual_initial_return'];rc=terminal['exit_code']
    if type(rc)is not int or terminal.get('session_id')is not None or tool['observed_closed']is not True or \
       type(tool['original_integer_exit_code'])is not int or tool['original_integer_exit_code']!=rc or \
       not isinstance(terminal['output'],str)or not isinstance(initial['output'],str):raise RuntimeError('true completed original Root terminal required')
    if pins['Host-freeze']['path']!=str(HERE/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json')or pins['CLI']['path']!=str(HERE/'DECLARED_EXECUTION_INTERFACE.json')or \
       pins['Host-freeze']!=CURRENT_HF_PIN or pins['CLI']!=CURRENT_CLI_PIN or hf['schema']!='COMPLETE_ACTUAL_AAA3_A8_OWNED_MAP_PIPELINE_HOST_SOURCE_FREEZE_V17'or cli['selected_own_Host_freeze_pin']!=pins['Host-freeze']:
        raise RuntimeError('exact current v18 own frozen Host3955/interface')
    actual_argv=argv['exact_argv']
    if argv['interface_pin']!=pins['CLI']or argv['Host_freeze_pin']!=pins['Host-freeze']:raise RuntimeError('actual current Root argv exact frozen authority')
    if shlex.split(tool['exact_executed_command'])!=actual_argv or actual_argv!=cli['exact_reviewable_argv']or len(actual_argv)!=96 or \
       len(cli['mandatory_external_prefixes'])!=14 or actual_argv[:9]!=['/usr/bin/env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1',
       'OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1']or \
       actual_argv[9:12]!=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',hf['host_source']['path']]:
        raise RuntimeError('genuine exact96 environment/ownHost execution')
    bindings=cli['mandatory_external_fullpin_bindings']
    for i,prefix in enumerate(cli['mandatory_external_prefixes']):
        q=bindings[prefix];triplet=['--'+prefix+'-summary',q['path'],'--'+prefix+'-sha256',q['sha256'],'--'+prefix+'-seven-id',json.dumps(q['identity'],separators=(',',':'))]
        if actual_argv[12+6*i:18+6*i]!=triplet:raise RuntimeError('all14 exact external bindings and order')
        seven(q)
    if cli['original_limits']!=dict(stage_seconds=600,whole_seconds=1800,SELF_bytes=512*2**20,
       own_child_bytes=512*2**20,fresh_bytes=2*2**30,history_bytes=96*2**30,
       cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,min_free_bytes=8*2**30,
       threads=1,serial_business_children=1,automatic_retry=False):raise RuntimeError('unchanged original literal caps')
    contract=load(CONTRACT_PIN)
    if contract['schema']!='PREPARED_V16_FUTURE_TERMINAL_READONLY_POSTVERIFICATION_CONTRACT_V1':
        raise RuntimeError('unchanged original50/33 static Source contract; predecessor authority historical only')
    root=Path(pins['report']['path']).parent
    if str(root)!=cli['output_root']:raise RuntimeError('exact v18 declared own OUT')
    own_host,_=eof(hf['host_source']['path'],hf['host_source'],True)
    plan=load(hf['actual_prerequisite_bound_Source_plan_pin'])
    if hf['actual_prerequisite_bound_Source_plan_pin']!=CURRENT_PLAN_PIN or len(hf['dependencies'])!=3955 or plan['actual_Source_revision']!=18 or len(plan['retained_original_science_nine_input_pins'])!=9:
        raise RuntimeError('exact current v18 own3955 Source dependencies and retained original science9')
    fixed=unique(summary['fixed_current_pins']);ft={p['path']:p for p in fixed};outputs=unique(summary['output_pins']);ot={p['path']:p for p in outputs};owned=unique(summary['owned_runtime_pins'])
    for p in unique(hf['dependencies']+[hf['host_source']]+plan['dependencies']):
        if ft.get(p['path'])!=norm(p):raise RuntimeError('entire current ownHF3955 and Source plan dependencies exact in actual fixed')
    for p in fixed:seven(p)
    for p in outputs:seven(p)
    for p in owned:
        if ot.get(p['path'])!=p and rc==0:raise RuntimeError('successful actual owned PF absent from outputs')
        seven(p)
    before=inventory(root);physical=[]
    for path in sorted(before['files']):physical.append(eof(path,ot.get(path,pins['report']if path==pins['report']['path']else None))[0])
    registered=set(ot)|{pins['report']['path']}
    if rc==0 and set(before['files'])!=registered:raise RuntimeError('whole successful actual OUT exactly published outputs+summary')
    unpublished=[p for p in physical if p['path']not in registered]
    rawpin=summary['complete_unmodified_execution_records_pin'];raw=load(rawpin);stagepin,_=eof(root/'AAA3-streaming/stages.json');stages=load(stagepin)
    records=raw['records'];compact=[{k:v for k,v in r.items()if k not in('resource_before','resource_after')}for r in records]
    if raw['schema']!='ACTUAL_AAA3_COMPLETE_EXECUTION_PREPUBLICATION_RECORD_V1'or \
       raw['engineering_three_plane_closed0']is not False or raw['exact_publication_pending']is not True or \
       stages!={'stages':records}or summary['records']!=compact or len(records)>50 or \
       raw['actual_terminal']!=summary['actual_terminal']or raw['actual_cache336_driver_and_budget_bit_admission']!=summary['actual_cache336_driver_and_budget_bit_admission']or raw['actual_A8_owned_MAP_runtime_admission']!=summary['actual_A8_owned_MAP_runtime_admission']:
        raise RuntimeError('full unmodified records and compact resource-only projection')
    source_raw=eof(own_host['path'],own_host,True)[1];tree=ast.parse(source_raw);abort_strings={n.value for n in ast.walk(tree)if isinstance(n,ast.Constant)and isinstance(n.value,str)}
    labels=contract['original50_ordered_labels'];messages=contract['exact33_refusal_messages']
    if len(labels)!=50 or len(set(labels))!=50 or len(messages)!=33 or [r['label']for r in records]!=labels[:len(records)]:
        raise RuntimeError('exact original50 ordered labels, including genuine failed prefix')
    refusal_list=summary['actual_operator_refusals'];by={r['original_execution_record_index']:r for r in refusal_list}
    names=[r['case']for r in refusal_list]
    if len(set(names))!=len(names)or any(r['case']not in messages or r['expected_abort']!=messages[r['case']]for r in refusal_list)or \
       (rc==0 and set(names)!=set(messages)):
        raise RuntimeError('unique case → exact frozen33 refusal message mapping')
    if [{k:v for k,v in r.items()if k!='record'}for r in raw['actual_operator_refusals']]!=refusal_list or \
       raw['actual_complete_readback_proofs']!=summary['actual_complete_readback_proofs']:
        raise RuntimeError('exact raw full refusal and readback facts')
    if len(by)!=len(refusal_list):raise RuntimeError('one unique exact intended refusal per actual record')
    watches=[];positive_logs={};unexpected=[]
    for i,r in enumerate(records):
        w,log=actual_stage(root,r,i,by.get(i),abort_strings);watches.append(w)
        if r['status']=='FAILED'and i not in by:unexpected.append(i)
        if Path(r['label']).name in ('global_positive','project_positive','BOOT_positive'):positive_logs[Path(r['label']).name]=log
    counts=collections.Counter(r['status']for r in records)
    no_limits=all(w['actual_watch']['limit_failure']is None for w in watches)
    cache,compact_provenance,old70,discrepancy=closed_provenance(summary,hf,ft)
    owned_proof=owned_provenance(summary,hf,ft,plan)
    for p in fixed:
        if Path(p['path']).suffix.lower()in('.o','.a','.f','.f90','.py','.c','.h'):eof(p['path'],p)
    healthy=summary['parent_memory_observation']['first_observation_error']is None
    journalpin=summary['parent_memory_observation']['journal_pin'];journal=load(journalpin)
    if journal['first_observation_error']is not None or len(journal['records'])!=summary['parent_memory_observation']['records']:healthy=False
    engineering=False;pair=None;helper=None;readback=None;failure=None
    if rc==0:
        if summary['status']!='ACTUAL_THREE_PLANE_ENGINEERING_CLOSED0_ONLY'or summary['engineering_three_plane_closed0']is not True or \
           len(records)!=50 or counts!={'PASS':17,'FAILED':33}or len(by)!=33 or unexpected or not no_limits or \
           summary['failure']is not None or summary['after_check_error']is not None or summary['first_failure_secondary_errors']!=[]or \
           raw['failure']is not None or raw['after_check_error']is not None or raw['first_failure_secondary_errors']!=[]or not healthy:
            raise RuntimeError('only genuine complete50=17PASS+33exact1 after final checks qualifies engineering')
        for label,marker in [('global_positive',b'ACTUAL-AAA3-NATIVE-GLOBAL-COMPLETE'),('project_positive',b'ACTUAL-AAA3-SINGLE-PRIVATE-PROJECT-COMPLETE'),('BOOT_positive',b'ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE')]:
            log=positive_logs[label]
            if marker not in log or b'normal end of execution'not in log:raise RuntimeError('full successful GLOBAL/PROJECT/BOOT log')
        pair,helper,readback=sealed_pair(summary,root,hf,ft,positive_logs['BOOT_positive'])
        if type(summary['SELF_peak_bytes'])is not int or not 0<=summary['SELF_peak_bytes']<512*2**20 or \
           not finite(summary['wall_seconds'])or not 0<summary['wall_seconds']<1800 or \
           summary['original_guard_class']!='OwnRSSSerialExecutor'or summary['original_guard_MRO_unchanged']is not True or \
           any(w['actual_watch']['sampled_peak_rss_mib']>=512 or w['actual_watch']['elapsed_seconds']>=600 for w in watches):
            raise RuntimeError('original SELF/own-child512 stage600 whole1800')
        for r in records:
            for key in ('resource_before','resource_after'):resource_snapshot(r[key],root)
        resource_snapshot(summary['resources_before'],root);resource_snapshot(summary['resources_after'],root)
        caps=cli['original_limits'];reserve=caps['history_bytes']-summary['resources_before']['artifact_bytes']-caps['cold_reserve_bytes']-caps['metadata_reserve_bytes']-caps['fresh_bytes']
        if reserve<=0 or sum(i[4]for i in before['files'].values())>2*2**30:raise RuntimeError('original initial/full physical fresh2 reservation')
        engineering=True
    else:
        failure=summary['failure']or summary['after_check_error']
        if failure is None:
            lines=terminal['output'].strip().splitlines()
            if 'Traceback (most recent call last):'not in terminal['output']or not lines:raise RuntimeError('failed terminal requires its real original traceback')
            failure=lines[-1]
        if not isinstance(failure,str)or not failure:raise RuntimeError('real failed pipeline cause')
    for p in fixed:seven(p)
    for p in physical+list(pins.values())+[rawpin,stagepin,journalpin,own_host]:seven(p)
    if inventory(root)!=before:raise RuntimeError('entire actual OUT current7/inventory changed during post')
    directory=Path(a.review_directory);ancestors(directory)
    if directory.parent!=REC or directory.exists():raise RuntimeError('one unique direct REC post directory')
    guard();directory.mkdir()
    report=dict(schema='READONLY_ACTUAL_V18_FULL50_ENGINEERING_POSTVERIFICATION_V1',
      status='PASS_ACTUAL_V18_FULL50_ENGINEERING_POSTVERIFICATION'if engineering else'REPORTED_ACTUAL_V18_FAILURE_UNQUALIFIED',
      failure=failure,actual_report_pin=pins['report'],actual_Host_freeze_pin=pins['Host-freeze'],actual_Root_true_tool_return_pin=pins['Root-tools'],actual_Root_argv_pin=pins['Root-argv'],actual_CLI_pin=pins['CLI'],
      actual_Root_initial_return=initial,actual_Root_terminal_return=terminal,actual_Root_exact_executed_command=tool['exact_executed_command'],actual_Root_exit_code=rc,
      actual_ordered_label_and_refusal_Source_contract_pin=CONTRACT_PIN,original50_ordered_labels=labels,exact33_refusal_messages=messages,
      actual_ordered50_labels_verified=(len(records)==50 and [r['label']for r in records]==labels),actual_exact33_case_message_mapping_verified=(len(by)==33 and set(names)==set(messages)),
      actual_Root_resources_before=summary['resources_before'],actual_Root_resources_after=summary['resources_after'],
      actual_Root_fresh_phase_peaks=summary['actual_fresh_peaks_by_phase'],actual_Root_SELF_peak_bytes=summary['SELF_peak_bytes'],actual_Root_wall_seconds=summary['wall_seconds'],
      original_runtime_caps=cli['original_limits'],Root_resource_snapshots_are_preserved_original_facts=True,current_budget_measurement_executed=False,
      independent_business_executed=False,independent_compiler_executed=False,independent_numerical_executed=False,independent_deletion_executed=False,
      actual_engineering_three_plane_closed0=engineering,actual_stage_count=len(records),actual_positive_count=counts['PASS'],actual_exact_refusal_count=len(by),
      all_actual_child_watch_limit_failures_absent=no_limits,actual_complete_pair_payload_bits_equal=engineering,
      all_current_output_pins_full_EOF_SHA_all7=True,actual_all_physical_output_fullpins=physical,unpublished_failed_output_fullpins=unpublished,
      actual_fixed_current_count=len(fixed),all_fixed_HF3955_current7_reobserved_twice=True,fixed_science_inputs_full_EOF_not_repeated=True,
      raw_execution_records_pin=rawpin,actual_stages_pin=stagepin,exact_compact_summary_records_equal_unmodified_raw=True,
      actual_watch_and_log_rows=watches,actual_unexpected_failed_record_indices=unexpected,actual_operator_refusals=refusal_list,
      actual_terminal=pair,sealed_Root_terminal_fact=summary['actual_terminal'],actual_pair_bit_verification_performed=engineering,
      actual_pair_bounded_full_readback=readback,actual_readonly_pair_helper_pin=helper,
      actual_Driver37_compact40_math57_admission=cache,actual_original_compact_reader_admission=compact_provenance,
      actual_A8_owned_MAP_runtime_admission=summary['actual_A8_owned_MAP_runtime_admission'],actual_owned_Runtime_only1_and_exact18_originalSCI9_proof=owned_proof,
      exact_338_assertions_121_calls_admitted=True,known_Bit_summary_metadata_discrepancy=discrepancy,
      original50_source_math_and_caps_unchanged=True,all_current_original70_object_archive_full_EOF_pins=old70,
      no_preseal_engineering_qualification=True,physical_EOF_SHA_distinct_from_logical_tree_digest=True,
      original_Root_first_error_and_traceback_raw_preserved=terminal,original_secondary_errors=summary['first_failure_secondary_errors'],
      late_failure_cannot_be_promoted_by_earlier_seal_or_summary=True,actual_parent_journal_pin=journalpin,parent_observation_healthy=healthy,
      readonly=True,Source_modified=False,actual_pipeline_rerun=False,solver_or_compiler_invoked=False,files_deleted=False,
      physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,angular_sixmoments_status='UNKNOWN',
      postverification_Source_pin=eof(Path(__file__).absolute())[0],all_file_descriptors_closed=True,
      limitation='Engineering only after real terminal0/complete50/three370-group sealed pair bit and whole-field checks. Fixed scientific input bodies were not rehashed; current7 twice preserves prior full-EOF authority. No independent physics qualification.')
    path=directory/'REVIEW.json';fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    with os.fdopen(fd,'w')as f:json.dump(report,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    dfd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:os.fsync(dfd)
    finally:os.close(dfd)
    p,_=eof(path);guard();print(json.dumps(dict(status=report['status'],review_pin=p,failure=failure,actual_engineering_three_plane_closed0=engineering),ensure_ascii=False),flush=True)

if __name__=='__main__':main()
