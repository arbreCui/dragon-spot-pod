"""Independent saved-evidence review; stream all complete journals once.

No PS, lsof, process launch, compiler, numerical solve, or D/E modification.
Large raw events are inspected one line at a time and never cloned into output.
"""
import collections
import errno
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import stat
import sys
import time

REC=Path(__file__).resolve().parent
BASE=REC.parent/'complete_history_root_index_source_v15_20261010'
D=BASE/'actual_frame_encoder_current_epoch_monitor_controls_sources_20261011'
E=BASE/'actual_frame_encoder_current_epoch_monitor_controls_receipts_20261011'
ART=REC.parent.parent/'artifacts'
ROOT_HOST=ART/'axial-material-frame-encoder-current-epoch-controls-Root-host-20261011'
FIELDS=('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
ORDER=['closed-before-first','exit7','transient','unlinked-duplicates','escaped','echild','unobserved-cache','deadline','persistent-topology','journal-failure']
NEGATIVE={'exit7','echild','unobserved-cache','deadline','persistent-topology','journal-failure'}
START=time.monotonic();CHECK_COUNT=0

def need(value,message):
    global CHECK_COUNT
    if type(value)is not bool or not value:raise ValueError(message)
    CHECK_COUNT+=1

def budget():
    need(time.monotonic()-START<600,'saved review metadata600 cap')
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform!='darwin':peak*=1024
    need(peak<512*2**20,'saved review self512 cap')

def ident(s):return [getattr(s,k)for k in FIELDS]

def pin(path):
    path=Path(path);before=ident(path.lstat())
    need(path.is_absolute()and all(not q.is_symlink()for q in(path,*path.parents))and stat.S_ISREG(before[2])and before[3]==1,'ordinary singlelink current saved evidence')
    h=hashlib.sha256();size=0
    with path.open('rb')as stream:
        need(ident(os.fstat(stream.fileno()))==before,'saved pin opened identity')
        while True:
            budget();raw=stream.read(2**20)
            if not raw:break
            h.update(raw);size+=len(raw)
        need(ident(os.fstat(stream.fileno()))==before,'saved pin full EOF identity')
    need(ident(path.lstat())==before and size==before[4],'saved pin current closed identity')
    return dict(path=str(path),sha256=h.hexdigest(),size_bytes=size,identity=before)

def strict(raw):
    def pairs(items):
        out={}
        for k,v in items:need(k not in out,'unique saved JSON keys');out[k]=v
        return out
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in()).throw(ValueError(s)))

def frozen_tree(root):
    files=[];dirs={};root=Path(root)
    for p in[root,*sorted(root.rglob('*'))]:
        budget();s=p.lstat();need(not stat.S_ISLNK(s.st_mode),'saved complete namespace has no alias')
        if stat.S_ISDIR(s.st_mode):dirs[str(p)]=ident(s)
        else:files.append(pin(p))
    return dict(files=files,directories=dirs)

def account_checks(account,increment):
    h=account['actual_original_history_check']
    values=[account['actual_regular_joint_bytes'],account['previous_complete_open_unlinked_bytes'],account['external_D_E_bytes'],h['artifact_bytes'],h['disk_free_bytes'],increment]
    need(all(type(v)is int and v>=0 for v in values),'actual account typed nonnegative bytes')
    need(values[0]+values[1]+increment<CAPS['joint_archive_bytes'],'actual account original joint2GiB')
    need(h['artifact_bytes']+account['external_D_E_bytes']+values[1]+increment<=CAPS['history_bytes'],'actual account original history96GiB')
    need(h['disk_free_bytes']-increment>=CAPS['free_floor_bytes'],'actual account original free8GiB')
    need(account['current_open_unlinked_verified']is False and account['failed_scan_never_replaced_by_this_account']is True,'pre/post disk account never substitutes for refused frame/unlinked PASS')
    need(account['clock']['whole_cap_satisfied']is True and account['clock']['stage_cap_satisfied']is True,'actual account original stage/whole clocks')

def ps_check(record):
    need(record['actual_returncode']==0 and record['streams_complete']is True,'actual complete EXIT0 full PS census')
    rows={}
    for line in record['actual_stdout'].splitlines():
        words=line.split();need(len(words)==4 and all(w.isdigit()for w in words[:3]),'full actual PS typed row')
        pid,ppid,pgid=map(int,words[:3]);need(pid>0 and str(pid)not in rows,'actual PS PID unique')
        rows[str(pid)]=dict(pid=pid,ppid=ppid,pgid=pgid,state=words[3])
    need(rows==record['complete_rows'],'full saved PS stdout parses to exact complete rows')
    need(type(record['actual_diagnostic_PID'])is int and record['actual_diagnostic_PID']not in record['actual_selected_PIDs'],'actual closed diagnostic individually excluded')

def owner_wait_checks(owner):
    w=owner['closed_wait']
    if w is None:return None
    need(w['closed_proven']is True and w['pid']==owner['pid']==w['actual_waitpid_pid'],'closed owner has actual exact PID wait tuple')
    status=w['actual_wait_status'];need(type(status)is int and(os.WIFEXITED(status)or os.WIFSIGNALED(status)),'actual owner terminal wait status')
    need(os.waitstatus_to_exitcode(status)==w['actual_exit_code'],'actual owner exit code derived from true wait status')
    return w['actual_exit_code']

def compact_event(e,raw,proofs,binding_pin,b):
    event=e['event'];frame=e.get('complete_frame')or{};start=e.get('fixed_window_started_monotonic');end=e.get('fixed_window_deadline_monotonic')
    row=dict(sequence=e['sequence'],event=event,start=start,end=end,ordinal=e.get('frame_ordinal'),
        error_type=(e.get('actual_error')or{}).get('type'),error_repr=(e.get('actual_error')or{}).get('repr'),
        scope_equal=frame.get('actual_pre_post_scope_equal'),unlinked_bytes=frame.get('actual_complete_unlinked_bytes'),
        unlinked_inodes=frame.get('actual_complete_unlinked_device_inode_count'),
        pre_selected=(frame.get('pre_PS')or{}).get('actual_selected_PIDs',[]),
        lsof_rc=(frame.get('lsof')or{}).get('actual_returncode'),
        lsof_returned=(frame.get('lsof')or{}).get('actual_returned_PIDs',[]),post_selected=(frame.get('post_PS')or{}).get('actual_selected_PIDs',[]),
        captured_escape_rows=[],actual_duplicate_unlinked_FDs=False)
    if event not in('fresh_frame_complete_candidate','fresh_frame_invalid_not_resource_PASS','fresh_frame_window_fatal_no_resource_PASS'):return row
    need(type(start)is float and type(end)is float and end==start+2,'every full frame original fixed total2s window')
    need(e['failed_frame_accepted']is False and e['resource_PASS']is False,'saved candidate/invalid/fatal never claims resource PASS')
    need(e['fresh_frame_policy']=='FRESH_COMPLETE_CURRENT_CENSUS_TOTAL_2S_V1'and e['fresh_frame_Source_contract']['adapter_Source_pin']==b['adapter_Source_pin']
        and e['fresh_frame_Source_contract']['new_Source_binding_pin']==binding_pin,'entire raw frame exact current Source binding')
    if event in('fresh_frame_complete_candidate','fresh_frame_invalid_not_resource_PASS'):
        need((json.dumps(e,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8')==raw,'complete raw UTF8 exact standard JSON serialization')
        account=e['actual_diagnostic_write_byte_account_before'];need(account['additional_record_bytes']==len(raw),'complete actual UTF8 self-accounted byte integer')
        account_checks(account,len(raw))
        ps_check(frame['pre_PS']);ps_check(frame['post_PS'])
        lsof=frame['lsof'];need(lsof['streams_complete']is True and type(lsof['actual_returncode'])is int,'entire actual closed lsof stdout/stderr')
        need(lsof['actual_argv']==[b['tool_pins']['lsof']['path'],'-nP','-F','pfnsiDtk','-a','-p',','.join(map(str,sorted(row['pre_selected'])))],'unchanged canonical actual lsof argv')
    if event=='fresh_frame_complete_candidate':
        need(row['lsof_rc']==0 and row['scope_equal']is True and set(row['lsof_returned'])==set(row['pre_selected'])and len(row['lsof_returned'])==len(set(row['lsof_returned'])),'candidate strict lsof0 complete unique selected PID scope')
        need(row['pre_selected']==row['post_selected'],'candidate exact pre/post selected scope')
        for pid,record in frame['post_PS']['complete_rows'].items():
            if int(pid)in row['post_selected']:row['captured_escape_rows'].append({k:record[k]for k in('pid','ppid','pgid')})
        records=[];record={}
        for line in frame['lsof']['actual_stdout'].splitlines():
            if line.startswith('f'):
                if record:records.append(record)
                record={'f':line[1:]}
            elif line and line[0]in'nsiDtk':record[line[0]]=line[1:]
        if record:records.append(record)
        counts=collections.Counter((r.get('D'),r.get('i'))for r in records if r.get('t')=='REG'and r.get('k')=='0'and r.get('s')=='29')
        row['actual_duplicate_unlinked_FDs']=any(all(key)and n>=2 for key,n in counts.items())
    if event=='fresh_frame_invalid_not_resource_PASS':
        key=(hashlib.sha256(raw).hexdigest(),len(raw),start)
        if key in proofs:
            proof=proofs[key];need(proof['actual_pre_and_post_full_accounts_completed']is True
                and proof['actual_original_disk_account_calls_completed']==2 and proof['failed_frame_accepted']is False and proof['resource_PASS']is False,'real completed two-call invalid proof remains refusal')
            times=[proof[k]for k in('actual_pre_append_full_account_started_monotonic','actual_pre_append_full_account_returned_monotonic','actual_post_append_full_account_started_monotonic','actual_post_append_full_account_returned_monotonic')]
            need(proof['fixed_window_deadline_monotonic']==end and all(type(v)is float and math.isfinite(v)for v in times)
                and start<=times[0]<=times[1]<=times[2]<=times[3]<end,'both genuine different pre/post full accounts completed inside same fixed2s')
            pre=proof['actual_pre_append_full_account'];post=proof['actual_post_append_full_account']
            need(e['actual_diagnostic_write_byte_account_before']==pre and pre['additional_record_bytes']==len(raw)and post['additional_record_bytes']==0,'actual entire saved invalid event pre-account equals completed proof; true post-account increment0')
            accounting=e['actual_private_invalid_append_accounting']
            need(accounting['actual_original_disk_account_calls_completed_before_append']==1 and accounting['postappend_completion_not_observed_at_prewrite']is True
                and accounting['outer_or_prior_account_reused']is False and accounting['same_fixed_total2s_window']is True
                and accounting['resource_PASS']is False,'prewrite raw truthful one actual call, no future postaccount/PASS fabrication')
            account_checks(pre,len(raw));account_checks(post,0);proof['independent_actual_raw_match_observed']=True
            row['matched_real_two_account_proof']=True
    return row

def main():
    need(all(os.environ.get(k)=='1'for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'))and os.environ.get('PYTHONDONTWRITEBYTECODE')=='1','pure saved-review thread1 environment')
    bp=pin(D/'Root_current_fresh_frame_controls_Source_binding.json');b=strict(Path(bp['path']).read_bytes());rp=pin(E/'Source_prelaunch_review.json');pre=strict(Path(rp['path']).read_bytes())
    source_review=strict((REC/'FINAL_ROOT_SERIAL_BOUNDARY_SOURCE_REVIEW.json').read_bytes())
    need(pin(source_review['reviewed_Root_serial_boundary_Source_pin']['path'])==source_review['reviewed_Root_serial_boundary_Source_pin'],'actual executed Root boundary unchanged after independent Source review')
    dfreeze=frozen_tree(D);efreeze=frozen_tree(E)
    need(b['case_execution_order']==ORDER and b['original_caps']==CAPS and b['old_controls_qualification_inherited']is False,'all ten exact original order/nine caps/no old Q')
    need(bp==pre['new_Source_binding_pin']and pin(b['adapter_Source_pin']['path'])==b['adapter_Source_pin']and pin(b['control_entry_Source_pin']['path'])==b['control_entry_Source_pin'],'current Source/prelaunch exact unchanged pins')
    sp=pin(ROOT_HOST/'Root_actual_controls_summary.json');summary=strict(Path(sp['path']).read_bytes())
    tp=pin(REC/'ACTUAL_CURRENT_TEN_CONTROLS_TRUE_TOOL_RETURNS.json');tools=strict(Path(tp['path']).read_bytes())
    need(tools['initial']['result']['session_id']==86660 and tools['terminal']['result']['exit_code']==0 and tools['terminal']['result']['chunk_id']=='d394d8','real initial Root session86660 and actual terminal d394d8 EXIT0')
    need(summary['failure']is None and summary['completed_cases']==10 and summary['all_ten_control_entries_closed0']is True
        and summary['original_order']==ORDER and[record['case']for record in summary['actual_case_records']]==ORDER,'real Root records all ten once/serial/closed0')
    need(summary['whole_seconds']<1800 and summary['Root_SELF_peak_bytes']<512*2**20,'actual entire Root whole1800/SELF512 satisfied')
    need(summary['complete_Native_qualified']is False and summary['scientific_accuracy_qualified']is False and summary['online_BOOT_qualified']is False and summary['goal_complete']is False,'real control closure not Native/online/science/goal completion')
    for checkpoint in summary['resource_checkpoints']:
        g=checkpoint['original'];need(g['complete_history']['artifact_bytes']+20971764748+64*2**20<96*2**30,'actual original Root checkpoint history/cold reserve')
        need(g['fresh_output']['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'actual original Root checkpoint filesystem floor/reserves')
    case_rows=[];total_journal_bytes=0;total_lines=0;total_proofs=0;all_saved_pins=[bp,rp,sp,tp];retained_cleanup_anomalies=[]
    for case,record in zip(ORDER,summary['actual_case_records']):
        budget();ns=b['case_namespaces'][case];host=Path(ns['host']);rootcase=ROOT_HOST/case
        need(record['returncode']==0 and record['actual_error']is None and record['actual_cleanup_errors']==[]
            and record['original_Popen_wait_return_observed']is True and record['actual_original_Popen_wait_return']==0
            and record['unknown_or_failed_wait_promoted_to_zero']is False,'real Root control entry wait0 with no failure normalization '+case)
        need(record['wall_seconds']<600 and record['Root_sampled_control_SELF_peak_mib']<512,'actual original Root child stage/SELF caps '+case)
        terminalpin=pin(rootcase/'Root_actual_terminal.json');terminal=strict(Path(terminalpin['path']).read_bytes());need(terminal==record,'actual case terminal file exact Root summary record '+case)
        for stream in('stdout','stderr'):need(pin(record[stream]['path'])==record[stream],'actual complete Root stream current pin '+case)
        fp=pin(host/'ACTUAL_FRESH_FRAME_CONTROL_FACTS.json');facts=strict(Path(fp['path']).read_bytes());stdout=Path(record['stdout']['path']).read_bytes().splitlines()
        last=strict(stdout[-1]);need(last['actual_facts_pin']==fp,'actual control stdout pins exact complete saved facts '+case)
        need(facts['case_id']==case and facts['original_caps']==CAPS and facts['new_Source_binding_pin']==bp
            and facts['independent_Source_prelaunch_review_pin']==rp and facts['adapter_Source_pin']==b['adapter_Source_pin']
            and facts['control_entry_Source_pin']==b['control_entry_Source_pin'],'exact complete current Source/case/caps coupling '+case)
        need(facts['complete_D_freeze']==dfreeze and facts['complete_E_freeze']==efreeze,'entire current D/E files/directory strict7ID unchanged '+case)
        expected=case in NEGATIVE;need(facts['actual_expected_negative']is expected and(facts['actual_error']is not None)==expected,'actual expected stage refusal/positive behavior '+case)
        stages=facts['actual_stage_records'];need(len(stages)==1 and stages[0]['status']==('FAILED'if expected else'PASS')and 0<stages[0]['wall_cap_seconds']<=600,'negative business remains FAILED; one genuine original stage '+case)
        need(facts['whole_seconds']<1800 and facts['old_controls_qualification_inherited']is False and facts['OS_rows_or_tool_outcomes_mocked']is False
            and facts['original_classes_MRO_modified']is False and facts['actual_native_build_or_AB_executed']is False and facts['scientific_qualification_created']is False,'original actual scope/no mocks/MRO change/Native or science '+case)
        owners=facts['actual_owner_state']['owners'];need(len(owners)==2 and{v['role']for v in owners}=={'business','watchdog'},'genuine one business plus original watchdog owner '+case)
        exits={owner['role']:owner_wait_checks(owner)for owner in owners};business=next(v for v in owners if v['role']=='business')
        proofs={};couplings=facts['actual_invalid_prepost_raw_couplings']
        for p in facts['actual_invalid_prepost_append_proofs']:
            key=(p['complete_appended_UTF8_sha256'],p['exact_complete_appended_UTF8_bytes'],p['fixed_window_started_monotonic']);need(key not in proofs,'unique actual invalid append proof');proofs[key]=p
        need(len(couplings)==len(proofs),'all actual completed invalid proofs have raw couplings '+case)
        events=[];journal_pins=[];line_count=0;byte_count=0;previous=0
        for jp in facts['actual_invalid_append_journal_snapshots']:
            need(pin(jp['path'])==jp,'actual complete journal snapshot current strict full EOF '+case);journal_pins.append(jp)
            digest=hashlib.sha256();counted=0
            with Path(jp['path']).open('rb')as stream:
                for raw in stream:
                    budget();need(raw.endswith(b'\n'),'entire actual saved journal complete newline');digest.update(raw);counted+=len(raw)
                    e=strict(raw);need(type(e['sequence'])is int and e['sequence']>previous,'actual saved sequence monotonic; unsaved gaps retained');previous=e['sequence']
                    events.append(compact_event(e,raw,proofs,bp,b));line_count+=1
            need(counted==jp['size_bytes']and digest.hexdigest()==jp['sha256']and pin(jp['path'])==jp,'whole journal streamed full EOF SHA unchanged '+case);byte_count+=counted
        need(all(p.get('independent_actual_raw_match_observed')is True for p in proofs.values()),'every completed two-account proof independently matched actual full raw UTF8 '+case)
        for coupling in couplings:
            key=(coupling['complete_appended_UTF8_sha256'],coupling['exact_complete_appended_UTF8_bytes'],coupling['fixed_window_started_monotonic']);need(key in proofs,'every source raw coupling independently has true proof '+case)
        invalid=[e for e in events if e['event']=='fresh_frame_invalid_not_resource_PASS'];candidates=[e for e in events if e['event']=='fresh_frame_complete_candidate'];fatal=[e for e in events if e['event']=='fresh_frame_window_fatal_no_resource_PASS'];trans=facts['actual_transitions']
        if case=='closed-before-first':need(exits['business']==0 and business['live_census_seen']is False and business['pid']not in facts['actual_owner_state']['last_actual_scope']['actual_selected_PIDs'],'real early wait0 owner excluded without live-census prerequisite')
        if case=='exit7':need(exits['business']==7 and stages[0]['status']=='FAILED','true raw wait exit7 kept failed')
        if case=='transient':
            targets={v['ready']['pid']for v in trans if v['event']=='actual_selected_descendant_before_transition'}
            matching=[e for e in invalid if any(p in e['pre_selected']for p in targets)and(e['lsof_rc']not in(None,0)or any(p not in e['lsof_returned']for p in targets))]
            need(any(e.get('matched_real_two_account_proof')and any(c['start']==e['start']and c['ordinal']>e['ordinal']for c in candidates)for e in matching),'actual transient selected descendant refused then new complete frame in same original window')
        if case=='unlinked-duplicates':
            need(any(c['unlinked_bytes']==29 and c['unlinked_inodes']==1 and c['actual_duplicate_unlinked_FDs']for c in candidates),'actual duplicate open-unlinked FDs counted once for29B')
            lastframe=facts['last_complete_resource_frame'];need(lastframe['complete_joint_HOCDE_bytes']>=lastframe['actual_complete_frame_journal_pin']['size_bytes']+lastframe['open_unlinked_bytes'],'actual accepted byte account includes its own complete journal')
        if case=='escaped':
            transition=next(v for v in trans if v['event']=='actual_escape_and_closed_leader');target=transition['actual_escape']['pid'];leader=transition['actual_owner_wait']['pid']
            need(any(e['scope_equal']is False and e.get('matched_real_two_account_proof')for e in invalid)
                and any(c['unlinked_bytes']==29 and any(row['pid']==target and row['pgid']==target and row['ppid']!=leader for row in c['captured_escape_rows'])for c in candidates),'real topology change refused then escaped/reparented FD captured by new frame')
        if case=='echild':need(exits['business']is None and business['last_wait'].get('actual_errno')==errno.ECHILD and any('no ECHILD-zero fallback'in(e['error_repr']or'')for e in fatal),'true ECHILD unknown never synthetic zero')
        if case=='unobserved-cache':need(exits['business']is None and any(v['event']=='actual_unobserved_original_poll_cache'for v in trans)and any('cached status requires actual recorded exit tuple'in(e['error_repr']or'')for e in fatal),'unobserved cached status refused with absent real close proof')
        if case=='deadline':
            barrier=next(v for v in trans if v['event']=='actual_control_barrier_exceeded_fixed_window')
            need(barrier['actual_monotonic']>=barrier['fixed_deadline']and any('fresh-frame fixed total2s observation deadline'in(e['error_repr']or'')for e in fatal),'actual deadline crossed and original fixed2s fatal refusal saved')
            if facts['actual_error']['type']=='builtins.PermissionError':
                need(exits['watchdog']==1 and any(e['event']=='original_terminate_group_exception'for e in events),'actual deadline cleanup PermissionError and watchdog EXIT1 retained')
                retained_cleanup_anomalies.append(dict(case=case,actual_error_type=facts['actual_error']['type'],actual_error_repr=facts['actual_error']['repr'],actual_watchdog_exit_code=1,original_fixed2s_refusal_preserved=True,original_cleanup_succeeded_claimed=False))
        if case=='persistent-topology':
            controlled={v['actual_wait']['pid']for v in trans if v['event']=='actual_each_frame_descendant_exit'};starts={e['start']for e in invalid}
            same=[e for e in invalid if e['start']==max(starts)and any(p in e['pre_selected']for p in controlled)]
            need(len(same)>=2 and not any(c['start']==same[0]['start']for c in candidates)
                and facts['actual_after_execute_observed_monotonic']>=same[0]['end']and facts['last_complete_resource_frame']['fixed_window_started_monotonic']!=same[0]['start'],'sustained actual controlled topology refused; no candidate/accepted publication at exhausted same2s')
            need(facts['actual_error']['repr']=="ValueError('fresh-frame fixed total2s observation deadline')"and facts['actual_persistent_negative_deadline_basis']=='actual_private_invalid_append_fixed_deadline_error_with_original_recording_errors_preserved','actual private invalid append deadline error/gaps kept without fabricated fatal line')
            need(bool(facts['actual_monitor_evidence']['additional_recording_errors'])and bool(facts['actual_monitor_evidence']['unpersisted_complete_events']),'real invalid append recording errors and unpersisted complete event retained')
        if case=='journal-failure':
            target=host/'runtime/ACTUAL_FAILURE_ONLY_MONITOR_EVENTS.jsonl';need(target.is_dir()and facts['actual_monitor_evidence']['journal_repaired_for_report']is False
                and bool(facts['actual_monitor_evidence']['actual_recording_errors'])and bool(facts['actual_monitor_evidence']['complete_unpersisted_events']),'actual journal directory failure remains unrepaired/refused with real complete unsaved events')
        namespace_pins=[];joint=0
        for key in('host','output','control'):
            inventory=frozen_tree(ns[key]);namespace_pins.extend(inventory['files']);joint+=sum(p['size_bytes']for p in inventory['files'])
        need(joint+sum(p['size_bytes']for p in dfreeze['files']+efreeze['files'])<2*2**30,'current entire saved HOCDE ordinary bytes original joint2GiB '+case)
        case_rows.append(dict(case=case,expected_negative_business=expected,actual_business_stage_status=stages[0]['status'],actual_business_exit_code=exits['business'],
            actual_watchdog_exit_code=exits['watchdog'],Root_control_entry_exit_code=0,facts_pin=fp,Root_terminal_pin=terminalpin,
            complete_HOC_file_pins=namespace_pins,complete_journal_pins=journal_pins,complete_journal_line_count=line_count,complete_journal_bytes=byte_count,
            independently_matched_two_full_account_proofs=len(proofs),actual_complete_candidate_count=len(candidates),actual_invalid_count=len(invalid),
            actual_fatal_count=len(fatal),expected_behavior_independently_verified=True,old_Q_inherited=False,negative_business_promoted_to_PASS=False))
        all_saved_pins.extend([fp,terminalpin,record['stdout'],record['stderr'],*journal_pins]);total_journal_bytes+=byte_count;total_lines+=line_count;total_proofs+=len(proofs)
        del facts,proofs,events
    need(frozen_tree(D)==dfreeze and frozen_tree(E)==efreeze,'all current frozen D/E files/directories unchanged throughout independent saved review')
    need(all(pin(p['path'])==p for p in all_saved_pins),'all actual inputs/evidence current full EOF unchanged at independent review close')
    budget()
    report=dict(schema='INDEPENDENT_ACTUAL_CURRENT_TEN_GENUINE_CONTROLS_SAVED_REVIEW_V1',status='PASS_TEN_EXPECTED_CONTROL_BEHAVIORS_WITH_RETAINED_DEADLINE_CLEANUP_FAILURE',
        all_expected_case_checks_passed=True,blockers=[],control_behavior_evidence_complete=True,
        actual_all_ten_Root_control_entries_closed0=True,actual_negative_business_stages_remain_FAILED=True,
        reviewer_Source_pin=pin(Path(__file__).resolve()),current_Source_binding_pin=bp,current_prelaunch_review_pin=rp,
        actual_Root_summary_pin=sp,actual_Root_true_tool_returns_pin=tp,actual_Root_initial_session_id=86660,actual_Root_terminal_chunk='d394d8',
        original_caps=CAPS,original_case_execution_order=ORDER,complete_D_freeze=dfreeze,complete_E_freeze=efreeze,
        actual_Root_wall_seconds=summary['whole_seconds'],actual_Root_control_SELF_peak_mib=max(v['Root_sampled_control_SELF_peak_mib']for v in summary['actual_case_records']),
        independently_streamed_complete_journal_bytes=total_journal_bytes,independently_streamed_complete_journal_records=total_lines,
        independently_matched_actual_two_full_account_proofs=total_proofs,actual_case_reviews=case_rows,
        retained_original_cleanup_anomalies=retained_cleanup_anomalies,all_original_cleanup_succeeded=False,
        original_exceptions_or_unknown_waits_normalized=False,actual_monitor_qualification_created=False,
        actual_Native_complete_build_qualified=False,actual_material_double_production_online_BOOT_qualified=False,
        actual_AAA_or_ABA_scientific_accuracy_qualified=False,actual_goal_achieved=False,
        scientific_scope='Saved real control behavior/byte accounting and refusal evidence only; no Native, online BOOT or physical accuracy credit.',
        actual_PS_lsof_or_child_executed_by_reviewer=False,raw_full_events_cloned_into_report=False,
        actual_check_count=CHECK_COUNT,actual_review_elapsed_seconds=time.monotonic()-START,
        actual_reviewer_self_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    out=REC/'INDEPENDENT_ACTUAL_TEN_CONTROLS_SAVED_REVIEW.json'
    with out.open('x',encoding='utf-8')as stream:json.dump(report,stream,ensure_ascii=False,indent=2,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())
    txt=REC/'INDEPENDENT_ACTUAL_TEN_CONTROLS_SAVED_REVIEW.txt'
    with txt.open('x',encoding='utf-8')as stream:
        stream.write('当前十项真实控制：预定行为独立核验通过。\n10个Root控制入口真实退出0，4个正控制业务PASS，6个负控制业务仍FAILED。\n完整journal逐行核验：'+str(total_lines)+'条，'+str(total_journal_bytes)+'字节；'+str(total_proofs)+'份真实前后两次全量account证明均匹配原完整UTF8记录，并在同一固定2秒窗口完成。\nD/E完整文件内容和7项身份、目录身份保持。原9项限制和10项顺序保持。\n必须保留：deadline原固定2秒拒绝有完整fatal记录；随后清理出现PermissionError(1)，watchdog真实退出1。没有将其改写成成功清理。ECHILD/无观察缓存的业务close proof仍为未知。\n这份审核只证明控制预定行为及如实拒绝，不新增完整Native、双精度生产到在线BOOT、AAA/ABA或科学精度通过。\n');stream.flush();os.fsync(stream.fileno())
    print(json.dumps(dict(status=report['status'],review_pin=pin(out),short_text_pin=pin(txt),actual_cases=10,
        streamed_journal_records=total_lines,streamed_journal_bytes=total_journal_bytes,matched_real_two_account_proofs=total_proofs,
        actual_original_cleanup_anomalies=retained_cleanup_anomalies,actual_Native_or_scientific_qualification=False),allow_nan=False),flush=True)

if __name__=='__main__':main()
