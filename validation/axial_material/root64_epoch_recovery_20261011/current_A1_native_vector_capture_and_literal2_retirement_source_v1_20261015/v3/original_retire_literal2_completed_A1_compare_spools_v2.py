"""Root may retire only two completed A1 comparison spools after current capture/post0."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import resource,subprocess,sys,time
import capture_source_common as c

BASE = Path(__file__).absolute().parent
SOURCE = BASE / 'retire_literal2_completed_A1_compare_spools.py'
PREFIX = Path('/Users/wen/spot/validation/artifacts/axial-material-current-three-plane-raw-macro-compare-after-GENDF-cumulative25-20261014-v1-evidence')
LITERALS = [
    ('A1/original_archive_index.sqlite', 'd600af50d3fa394eba033798af415afab71d8e10577feb0f0a545804a5a42734', [16777229,50187716,33188,1,52441088,1791980275784980202,1791980275784980202]),
    ('A1/original_words.bin', 'b1bddebf913115e3b13891082f98716eb1e46cd3f9205ccd291567d477fb696c', [16777229,50187719,33188,1,150267572,1791980275793600013,1791980275793600013]),
]
TARGETS = [dict(path=str(PREFIX / name), sha256=sha, size_bytes=ids[4], identity=ids) for name, sha, ids in LITERALS]

def require(value, message):
    if value is not True:
        raise RuntimeError(message)

def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def current(pin):
    q = Path(pin['path'])
    s = q.lstat()
    require(q.is_absolute() and stat.S_ISREG(s.st_mode) and s.st_nlink == 1 and
            s.st_uid == os.getuid() and identity(s) == pin['identity'] and
            s.st_size == pin['size_bytes'] and
            not any(p.is_symlink() for p in (q, *q.parents)), 'exact ordinary current7: ' + str(q))
    return q

def full(pin, parse=False):
    q = current(pin)
    sha = hashlib.sha256()
    size = 0
    parts = []
    fd = os.open(q, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        require(identity(os.fstat(fd)) == pin['identity'], 'opened exact7')
        while True:
            raw = os.read(fd, 2**20)
            if not raw:
                break
            sha.update(raw)
            size += len(raw)
            if parse:
                parts.append(raw)
        require(identity(os.fstat(fd)) == pin['identity'], 'after EOF exact7')
    finally:
        os.close(fd)
    current(pin)
    require(size == pin['size_bytes'] and sha.hexdigest() == pin['sha256'], 'complete EOF SHA: ' + str(q))
    return json.loads(b''.join(parts)) if parse else None

def argument_pin(path, sha, seven):
    ids = json.loads(seven)
    require(type(ids) is list and len(ids) == 7 and all(type(v) is int for v in ids), 'seven integer identity')
    return dict(path=str(path),sha256=sha,size_bytes=ids[4],identity=ids)

def snapshot(file, result):
    data = (json.dumps(result,indent=2,allow_nan=False) + '\n').encode()
    file.seek(0)
    file.write(data)
    file.truncate()
    file.flush()
    os.fsync(file.fileno())

def actual_pin(path):
    s = path.lstat()
    return dict(path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),size_bytes=s.st_size,identity=identity(s))

def closure(plan):
    p = plan['closure_pins']
    post = full(p['typed_post_review'], True)
    tools = full(p['typed_post_tools'], True)
    require(post['status'] == 'PASS_ACTUAL_SAVED_THREE_TYPED_PATH_FINITE_POSTVERIFICATION' and
            post['failure'] is None and type(post['actual_Root_integer_exit_code']) is int and
            post['actual_Root_integer_exit_code'] == 0, 'independent closed typed postverification')
    terminal = tools['actual_terminal_return']
    require(tools['observed_closed'] is True and type(tools['original_integer_exit_code']) is int and
            tools['original_integer_exit_code'] == 0 and type(terminal['exit_code']) is int and
            terminal['exit_code'] == 0 and terminal.get('session_id') is None and
            json.loads(tools['actual_full_stdout'])['review_pin'] == p['typed_post_review'], 'genuine typed post closed0')
    root = full(p['typed_root_tools'], True)
    terminal = root['actual_terminal_return']
    receipt = json.loads(terminal['output'])
    require(root['observed_closed'] is True and type(root['original_integer_exit_code']) is int and
            root['original_integer_exit_code'] == 0 and type(terminal['exit_code']) is int and
            terminal['exit_code'] == 0 and terminal.get('session_id') is None and
            receipt['report_pin'] == p['typed_host_report'], 'genuine owning Root closed0')
    host = full(p['typed_host_report'], True)
    result = full(p['typed_result'], True)
    watch = full(p['typed_watchdog'], True)
    full(p['typed_log'])
    old = full(p['original_spool_report'], True)
    require(host['status'] == receipt['status'] == 'ACTUAL_SAVED_THREE_MACRO_TYPED_PATH_COMPARISON_EXIT2_CLOSED_ONLY' and
            host['failure'] is None and host['secondary_failures'] == [] and
            host['final_report_resource_check_passed'] is True and type(watch['returncode']) is int and
            watch['returncode'] == 2 and watch['limit_failure'] is None, 'completed typed child2 with no limit failure')
    require(post['actual_Host_report_pin'] == p['typed_host_report'] and
            post['actual_child_report_pin'] == p['typed_result'] and
            post['actual_Root_true_tool_pin'] == p['typed_root_tools'] and
            post['actual_watchdog_full_pin'] == p['typed_watchdog'] and
            post['actual_log_full_pin'] == p['typed_log'], 'post binds owning closure metadata')
    require(len(result['comparisons']) == 3 and post['total_macro_record_comparisons'] == 58860 and
            post['total_compared_original_words'] == 6792456 and
            result['all_raw_word_mismatches'] == result['all_metadata_mismatches'] ==
            post['all_raw_word_mismatches'] == post['all_metadata_mismatches'] == 0 and
            result['all_three_original_producer_seals_preserved'] is True and
            result['comparison_contract'] == 'EXACT_TYPED_FULL_PATH_KIND_COUNT_WORDS_AND_ALL_RAW_BYTES', 'all three completed typed comparisons')
    for comp, pair in zip(result['comparisons'], plan['original_native_pairs']):
        require(comp['plane'] == pair['plane'] and comp['compared_all_macro_records'] == 19620 and
                comp['compared_original_payload_words'] == 2264152 and
                comp['raw_word_mismatches'] == comp['metadata_mismatches'] == 0 and
                comp['native_sqlite_pin'] == pair['sqlite_pin'] and comp['native_pool_pin'] == pair['native_pool_pin'] and
                all(comp[k] is True for k in ('path_sets_equal','all_original_records_and_typed_root_preserved',
                    'original_archive_not_redecoded','original_orders_not_sorted_or_rewritten')), 'completed original plane spool lifecycle')
        current(comp['detail_pin'])
        original = old['comparisons'][pair['plane'] - 1]
        require(original['archive_pin'] == pair['archive_pin'] and
                pair['sqlite_pin'] in original['all_output_pins'] and
                pair['native_pool_pin'] in original['all_output_pins'], 'original spool producer metadata preserved')
    require(old['all_raw_word_mismatches'] == 9501687 and
            result['original_Root_exit_code_retained'] == host['original_Root_exit_code_retained'] ==
            post['original_compare_Root_exit_code_retained'] == 1 and
            result['original_positional_mismatch_report_not_modified'] is True and
            post['original_compare_budget_failure_and_positional_reports_retained'] is True, 'historical ordinal failure unchanged')
    for data in (post, host, result, old):
        require(all(v is False for k,v in data.items() if k.endswith('_qualified') or
                    k.endswith('_verified') or k in ('ABA_admitted','goal_complete')), 'no scientific qualification')

def fresh_process_preflight(mode,ordinal):
    started=time.time_ns();checks=[]
    commands=[['/bin/ps','-axo','pid=,ppid=,stat=,command='],['/usr/sbin/lsof','-nP','-Fpcfn']+[p['path'] for p in TARGETS]]
    path=BASE/('ROOT_FRESH_PS_LSOF_'+mode.upper()+'_'+str(ordinal)+'.json')
    receipt=dict(schema='ACTUAL_LITERAL2_A1_FRESH_PROCESS_AND_OPEN_HANDLE_PREFLIGHT_V1',mode=mode,started_wall_time_ns=started,finished_wall_time_ns=None,actual_returns=checks,raw_observations_only=True,owning_retirement_assertions_follow=True,failure=None)
    with path.open('xb') as file:
        snapshot(file,receipt)
        try:
            for command in commands:
                observed=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=30,check=False)
                require(len(observed.stdout.encode())+len(observed.stderr.encode())<8*2**20,'bounded complete process/open-handle output')
                checks.append(dict(argv=command,original_integer_exit_code=observed.returncode,stdout=observed.stdout,stderr=observed.stderr));snapshot(file,receipt)
            receipt['finished_wall_time_ns']=time.time_ns();snapshot(file,receipt)
        except BaseException as error:receipt['failure']=repr(error);receipt['finished_wall_time_ns']=time.time_ns();snapshot(file,receipt);raise
    pp=actual_pin(path);ps,lsof=checks
    require(type(ps['original_integer_exit_code']) is int and ps['original_integer_exit_code']==0 and ps['stderr']=='','genuine fresh complete ps closed0')
    blocked=[]
    needles=('capture_A1_native_vectors.py','run_guarded_A1_native_vector_capture.py','run_full370_real_operator_control.py','run_guarded_full370_real_operator_control.py','run_one_actual_track_component.py','run_guarded_eight_fuel_finite18_SCAT.py','compare_eight_fuel_finite18_SCAT.py','compare_saved_three_macro_exact_typed_path_words.py')
    for line in ps['stdout'].splitlines():
        fields=line.split(None,3)
        if len(fields)!=4:continue
        pid,ppid,state,command=fields
        if not pid.isdecimal() or int(pid) in (os.getpid(),os.getppid()) or state.startswith('Z'):continue
        if any(n in command for n in needles):blocked.append(line)
    require(blocked==[],'no active original material/track/control reader: '+repr(blocked))
    require(type(lsof['original_integer_exit_code']) is int and lsof['original_integer_exit_code']==1 and lsof['stdout']==lsof['stderr']=='','fresh exact two paths have no open handles')
    return pp

def main():
    ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--mode',choices=['check','execute'],required=True)
    for n in ('source','plan'):
        ap.add_argument('--'+n+'-sha256',required=True);ap.add_argument('--'+n+'-seven-id',required=True)
    for n in ('capture-post-schema','capture-post-status'):ap.add_argument('--'+n,required=True)
    ap.add_argument('--review-pin');ap.add_argument('--readonly-receipt-pin');ap.add_argument('--readonly-tools-pin');a=ap.parse_args();started=time.monotonic()
    source_pin=argument_pin(SOURCE,a.source_sha256,a.source_seven_id);plan_pin=argument_pin(BASE/'PLAN.json',a.plan_sha256,a.plan_seven_id)
    require(Path(__file__).absolute()==SOURCE and all(os.environ.get(k)=='1' for k in c.THREADS) and not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile() is None,'literal reviewed Source/original singlethread Python')
    path=BASE/('READONLY_RETIREMENT_RECEIPT.json' if a.mode=='check' else 'EXECUTION_RETIREMENT_RECEIPT.json')
    result=dict(schema='LITERAL2_COMPLETED_A1_COMPARE_SPOOL_RETIREMENT_RECEIPT_V1',mode=a.mode,status='STARTED',failure=None,source_pin=source_pin,plan_pin=plan_pin,exact_target_pins=TARGETS,actual_released_pins=[],actual_released_bytes=0,original_caps=c.CAPS,completed_temporary_file_lifecycle_only=True,sameSHA_duplicate_claim=False,original_Root_exit_code_retained=1,old_reports_rewritten=False,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,**c.FALSE)
    # The literal4 primitive is retained: exclusive once claim before any guard,
    # complete target2 EOF before first unlink, immediate dirfd7, partial facts.
    with path.open('xb') as file:
        try:
            snapshot(file,result);full(source_pin);plan=full(plan_pin,True)
            require(plan['schema']=='A1_NATIVE_VECTOR_CAPTURE_AND_LITERAL2_RETIREMENT_SOURCE_ONLY_PLAN_V1' and plan['target_pins']==TARGETS and plan['planned_released_bytes']==202708660 and plan['original_caps']==c.CAPS and len(plan['complete_joint_roots'])==54,'exact literal two A1 inputs/completed root54/caps')
            c.check_finite(plan['finite_prerequisite_pins'],plan['finite_post_schema'],plan['finite_post_status'])
            sfpin=c.pin(BASE/'FINAL_SOURCE_FREEZE.json');sf=c.read(sfpin);peerpin=sf['same_round_Source_review_pin'];peer=c.read(peerpin)
            require(peer['status'].startswith('PASS') and peer.get('failure') is None and c.contains(peer,source_pin) and c.contains(peer,plan_pin),'same-round reviewed literal2 Source and plan')
            c.closed0(c.read(sf['same_round_Source_tools_pin']),'actual_review_return',peerpin,'review_pin')
            if a.mode=='execute':
                require(a.review_pin is not None and a.readonly_receipt_pin is not None and a.readonly_tools_pin is not None,'exact reviewed Source and genuine readonly0 required')
                require(json.loads(a.review_pin)==peerpin,'exact same Source review')
                rp=json.loads(a.readonly_receipt_pin);rt=json.loads(a.readonly_tools_pin);readonly=full(rp,True)
                require(rp['path']==str(BASE/'READONLY_RETIREMENT_RECEIPT.json') and readonly['status']=='READONLY_READY_EXACT_LITERAL2_A1' and readonly['failure'] is None and readonly['source_pin']==source_pin and readonly['plan_pin']==plan_pin and readonly['exact_target_pins']==TARGETS and readonly['actual_released_pins']==[] and readonly['actual_released_bytes']==0 and readonly['files_deleted'] is False,'exact successful readonly receipt no unlink')
                c.closed0(c.read(rt),'actual_terminal_return',rp,'receipt_pin');result.update(review_pin=peerpin,readonly_receipt_pin=rp,readonly_tools_pin=rt)
            capture={k:c.pin(p) for k,p in dict(host=c.OUT/'Root_actual_A1_native_vector_capture_summary.json',child=c.OUT/'inventories/ACTUAL_A1_NATIVE_26_REAL32_VECTOR_CAPTURE.json',compact=c.OUT/'inventories/A1_native_track_vectors_f4.bin',root_tools=BASE/'ROOT_CAPTURE_ACTUAL24_TRUE_TOOL_RETURNS.json',post=BASE/'actual_capture_postverify_20261015/REVIEW.json',post_tools=BASE/'actual_capture_postverify_20261015/TRUE_TOOL_RETURNS.json').items()}
            host,child=c.check_capture(capture,a.capture_post_schema,a.capture_post_status)
            require(child['original_A1_SQLite_pin']==TARGETS[0] and child['original_A1_pool_pin']==TARGETS[1] and host['actual_initial_parent_science_fullhash_pins']==TARGETS,'actual capture same exact two complete original A1 inputs')
            for p in host['complete_output_pins']:c.exact(p)
            result.update(capture_host_pin=capture['host'],capture_child_pin=capture['child'],compact_vector_full_pin=capture['compact'],capture_post_pin=capture['post'],capture_root_tools_pin=capture['root_tools'],capture_post_tools_pin=capture['post_tools'],capture_post_schema=a.capture_post_schema,capture_post_status=a.capture_post_status)
            closure(plan)
            original_retire=c.read(plan['actual_original_literal4_receipt_pin']);require(original_retire['status']=='RETIRED_EXACT_LITERAL4_COMPLETED_COMPARE_SPOOLS_ONLY' and original_retire['failure'] is None and original_retire['actual_released_bytes']==405417320,'old literal4 retained as unchanged historic operation')
            for p in original_retire['actual_released_pins']:require(not os.path.lexists(p['path']),'old literal4 absence retained')
            for p in plan['preserved_current7_pins']+plan['preserved_full_provenance_pins']:c.current(p)
            support=c.load(plan['original_support_Source_pin'],'literal2_original_support');helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'literal2_original_helper');factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'literal2_original_factory');fullguard,production=helper.modules();helper.guard_admission(fullguard)
            roots=plan['complete_joint_roots'];require(Path(sys.executable).resolve()==support.PYTHON and fullguard.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,) and Path(fullguard.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'original interpreter and unchanged guard MRO')
            require(roots[:-2]==plan['inherited_complete_joint_roots'] and len(set(roots))==54 and not any(Path(x).is_relative_to(Path(y)) for x in roots for y in roots if x!=y),'same54 whole cumulative roots no reset')
            joined=production.DiskResources(c.R/'validation',roots,8*2**30,2*2**30);history=factory.DynamicHistoryResources(c.ART,factory.history_roots([str(c.OUT)],c.ART),8*2**30,96*2**30,production.ResourceFailure)
            def resource_check():
                peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024);require(peak<512*2**20 and time.monotonic()-started<600,'original SELF512/stage600 within whole1800')
                h=history.check();f=joined.check();extra=0
                for p in plan['explicit_cumulative_metadata_file_pins']:
                    c.current(p)
                    if not any(Path(p['path']).is_relative_to(Path(root)) for root in roots):extra+=p['size_bytes']
                opened={}
                for n in os.listdir('/dev/fd'):
                    try:s=os.fstat(int(n))
                    except(ValueError,OSError):continue
                    if stat.S_ISREG(s.st_mode) and s.st_nlink==0:opened[s.st_dev,s.st_ino]=s.st_size
                require(h['artifact_bytes']+20971764748+64*2**20<96*2**30 and f['artifact_bytes']+extra+sum(opened.values())<2*2**30 and f['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'unchanged54/cumulative2/history96/cold/free8 with external/open-unlinked')
                return dict(original_history=h,complete_joint=f,explicit_external_metadata_bytes=extra,host_open_unlinked_bytes=sum(opened.values()),host_SELF_peak_bytes=peak,whole_elapsed_seconds=time.monotonic()-started)
            result['resources_before']=resource_check();require(result['resources_before']['original_history']['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,'original fullfresh2/cold/meta/history96 reservation');result['fresh_ps_lsof_pins']=[fresh_process_preflight(a.mode,1)]
            # Both full EOF checks precede the first unlink; no numerical decode.
            for p in TARGETS:full(p);resource_check()
            result['fresh_ps_lsof_pins'].append(fresh_process_preflight(a.mode,2));result['fresh_ps_lsof_checks_passed']=True;resource_check()
            result.update(preserved_current7_pins=plan['preserved_current7_pins'],preserved_full_provenance_pins=plan['preserved_full_provenance_pins'],closure_pins=plan['closure_pins'],actual_original_literal4_receipt_pin=plan['actual_original_literal4_receipt_pin'],complete_joint_roots=roots)
            snapshot(file,result)
            if a.mode=='execute':
                for p in TARGETS:
                    q=current(p);directory=os.open(q.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
                    try:
                        require(identity(os.stat(q.name,dir_fd=directory,follow_symlinks=False))==p['identity'],'immediate exact owned singlelink target7')
                        os.unlink(q.name,dir_fd=directory);result['actual_released_pins'].append(p);result['actual_released_bytes']+=p['size_bytes'];result['files_deleted']=True;os.fsync(directory)
                    finally:os.close(directory)
                    result['status']='PARTIAL_EXACT_LITERAL2_A1';snapshot(file,result)
                require(all(not os.path.lexists(p['path']) for p in TARGETS),'only two exact target roles absent')
                for p in plan['preserved_current7_pins']+plan['preserved_full_provenance_pins']:c.current(p)
                for p in capture.values():c.current(p)
                for p in host['complete_output_pins']:c.current(p)
                result['status']='RETIRED_EXACT_LITERAL2_COMPLETED_A1_COMPARE_SPOOLS_ONLY'
            else:result['status']='READONLY_READY_EXACT_LITERAL2_A1'
            result['resources_after']=resource_check();snapshot(file,result);resource_check()
        except BaseException as error:
            result['status']='FAILED_PARTIAL_EXACT_LITERAL2_A1' if result['actual_released_pins'] else 'FAILED_BEFORE_UNLINK';result['failure']=repr(error);snapshot(file,result);raise
    print(json.dumps(dict(status=result['status'],receipt_pin=actual_pin(path),actual_released_bytes=result['actual_released_bytes'],files_deleted=result['files_deleted'],physics_qualified=False)),flush=True)
if __name__=='__main__':main()
