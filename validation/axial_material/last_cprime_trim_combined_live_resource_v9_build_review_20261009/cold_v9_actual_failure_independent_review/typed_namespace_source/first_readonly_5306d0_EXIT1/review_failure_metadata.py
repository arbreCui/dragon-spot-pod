"""Finite actual cold failure metadata review. No production import, call, or retry."""
from pathlib import Path
import hashlib, json, math, os, stat, struct

OUT=Path('/private/tmp/axmat_v9_actual_cold_failure_typed_namespace_postreview_20261009')
CFG=Path('/private/tmp/axmat_v9_cold_actual_finalization_postterminal_scope_20261009/finalization_config_ROOT_OBSERVED.json')
FULL=Path('/private/tmp/spot_v9_actual_finalization_full_source_independent_review_20261009/REPORT.json')
BEFORE=Path('/private/tmp/axmat_v9_finalization_after_R19_typed_readback_20261009/REPORT.json')
R9=Path('/Users/wen/spot/validation/axial_material/last_cprime_trim_combined_live_resource_v9_build_review_20261009')
EXEC=Path('/private/tmp/axmat-v9-cold-root-actual-execution-20261009')
FIELDS=('dev','ino','mode','size','mtime_ns','ctime_ns','nlink')
PINS=[]

def require(v,msg):
    if not v: raise ValueError(msg)

def identity(p):
    s=Path(p).lstat();return [getattr(s,'st_'+k) for k in FIELDS]

def raw(p,sha=None):
    p=Path(p);require(p.is_absolute() and '..' not in p.parts,'absolute path')
    for q in (p,*p.parents):
        s=q.lstat();require(not stat.S_ISLNK(s.st_mode),'no alias read')
        require(stat.S_ISREG(s.st_mode) if q==p else stat.S_ISDIR(s.st_mode),'regular source and real parents')
    before=identity(p);b=p.read_bytes();require(identity(p)==before,'stable read identity')
    h=hashlib.sha256(b).hexdigest();require(sha is None or h==sha,'full SHA pin '+str(p))
    PINS.append({'path':str(p),'sha256':h,'bytes':len(b),'identity':before});return b

def pairs(items):
    d={}
    for k,v in items:require(k not in d,'duplicate JSON key');d[k]=v
    return d

def finite(s):
    v=float(s);require(math.isfinite(v),'finite JSON');return v

def parse(b):
    def reject(s):raise ValueError('nonfinite JSON '+s)
    return json.loads(b,object_pairs_hook=pairs,parse_float=finite,parse_constant=reject)

def load(p,sha=None):return parse(raw(p,sha))

def typed(v):
    if v is None:return ['None']
    if type(v) is bool:return ['bool',v]
    if type(v) is int:return ['int',str(v)]
    if type(v) is float:return ['float64',struct.pack('!d',v).hex()]
    if type(v) is str:return ['str',v]
    if type(v) is list:return ['list',[typed(x) for x in v]]
    if type(v) is dict:return ['dict_ordered',[[typed(k),typed(x)] for k,x in v.items()]]
    raise TypeError(type(v))

def namespace(root):
    root=Path(root);files={};dirs=[];links={}
    for folder,ds,ns in os.walk(root,followlinks=False):
        for name in ds+ns:
            p=Path(folder)/name;r=str(p.relative_to(root));s=p.lstat()
            if stat.S_ISREG(s.st_mode):files[r]=identity(p)
            elif stat.S_ISDIR(s.st_mode):dirs.append(r)
            elif stat.S_ISLNK(s.st_mode):links[r]=os.readlink(p)
            else:raise ValueError('unsupported namespace '+str(p))
    return {'files':files,'directories':sorted(dirs),'symlinks':links}

def own_pid(w,failed):
    require(w['own_child_only'] is True and w['liveness_group_cleanup'] is True,'own child cleanup witnesses')
    require(type(w['pid']) is int and w['pid']>0 and type(w['returncode']) is int and w['rss_cap_mib']==512,'own child fields')
    require(w['rss_peak_observation_contract']=='EXACT_OWN_PID_DARWIN_WAIT4_BYTES_AND_LIVE_PS_V1','original own PID contract')
    sampled=w['sampled_peak_rss_mib']; observed=w['observed_peak_rss_mib']; count=w['live_rss_sample_count']; kernel=w['own_pid_wait4_peak_rss_mib']
    require(type(sampled) in (int,float) and math.isfinite(sampled) and sampled>=0,'finite sampled peak')
    require(type(observed) in (int,float) and math.isfinite(observed) and observed>=0,'finite observed peak')
    require(type(count) is int and count>=0 and (count!=0 or sampled==0),'real live sample count and absence')
    if failed:
        require(w['own_pid_wait4_observed'] is False,'failed missing wait4 preserved')
        require(all(w[k] is None for k in ('own_pid_wait4_pid','own_pid_wait4_status','own_pid_wait4_ru_maxrss_bytes','own_pid_wait4_peak_rss_mib')),'all four missing kernel fields None, never zero')
        require(w['limit_failure']=="RuntimeError('own-child 512 MiB RSS cap reached')" and w['returncode'] in (-15,-9) and sampled>=512,'actual original live RSS rejection')
        require(observed==sampled,'actual observed failure live peak')
        return 'ACTUAL_LIVE_RSS_REJECTION_NOT_NATIVE_PASS'
    require(w['own_pid_wait4_observed'] is True,'normal actual own PID wait4 observed')
    pid=w['own_pid_wait4_pid'];status=w['own_pid_wait4_status'];value=w['own_pid_wait4_ru_maxrss_bytes']
    require(type(pid) is int and pid==w['pid'] and type(status) is int and 0<=status<=65535,'real own PID and wait status')
    require((os.WIFEXITED(status) or os.WIFSIGNALED(status)) and os.waitstatus_to_exitcode(status)==w['returncode'],'exact own PID terminal return')
    require(type(value) in (int,float) and math.isfinite(value) and value>0 and value==int(value),'real Darwin byte maxRSS')
    require(type(kernel) in (int,float) and math.isfinite(kernel) and kernel>0 and kernel==value/(1024.*1024.),'Darwin byte to MiB exact')
    require(observed==max(sampled,kernel) and 0<observed<512 and w['returncode']==0 and w['limit_failure'] is None,'normal actual stage pass only')
    return 'PASS_REAL_OWN_PID_COMPLETION_PEAK_INITIAL_STAGE_ONLY'

def main():
    require(Path(__file__).parent==OUT,'fixed TMP only reader')
    c=load(CFG,'8f5936308ad6ee031fc4328423966b9f0db069d27b5c1ce932f41a72d8a87174')
    full=load(FULL,'ead5085edb5b09ab3a2de65102565bc7493672302c2f4873512b0b3c7594d85e')
    before=load(BEFORE,'529d43996dc14b7edf0fbe31dd7bd5853533204513b760994918db27c7154adf')
    admitted=load(R9/'Root_actual_full_V9_cold_finalization_independent_admission.json','b4ab1e5707dbe9bd5cbd150032265dfb1b8977ea7895204e8954510c38a0895f')
    roots=c['roots'];w=Path(roots['work']);t=Path(roots['terminal'])
    start_ns={k:namespace(v) for k,v in roots.items()}
    full_map={p['path']:p for p in full['all_fresh_pins']}
    before_map={p['path']:p for p in before['fresh_read_pins']}
    for key in ('source','control_terminal'):
        for name,prior_id in c['original_namespaces'][key]['files'].items():
            p=Path(roots[key])/name;q=full_map[str(p)]
            require(identity(p)==prior_id==q['identity'],'whole old namespace source/control seven identity')
            raw(p,q['sha256'])
    old_bytes=raw(w/'prepared.json','35f8100a753b149b6b100b8bc7154ca1b09f488a464a5068e0ffb826877d6ec7')
    cold_bytes=raw(w/'prepared_cold.json','1290a19501ba7801deafe351407b244bd32f71a6cf0d010d4a14fd64e61d8b3e')
    old=parse(old_bytes);cold=parse(cold_bytes);inverse=dict(cold);supervision=inverse.pop('own_child_supervision')
    require(set(cold)==set(old)|{'own_child_supervision'} and typed(inverse)==typed(old),'whole type order list float64 bit inverse')
    require((json.dumps(inverse,indent=2,allow_nan=False)+'\n').encode()==old_bytes,'whole exact original serialized inverse')
    require(typed(supervision)==typed(c['expected_supervision']),'original exact monitoring descriptors')
    for d in (supervision['binding'],supervision['controls']['seal'],supervision['controls']['terminal_evidence']):raw(d['path'],d['sha256'])
    raw(c['factory']['path'],c['factory']['sha256'])
    failed=load(t/'cold_failed_terminal_return.json','89e9c3d69d7d7e1f80934a5a3415525d3aba02d4808ea98e00ce775b67c80502')
    observer=load(R9/'Root_actual_V9_cold_failure_tool_return.json','5a8601cbf5ae42cd397afc59bb990a3f09b3645dc94d8ec1acc1c8c79026eaee')
    a=failed['actual_tool_result']
    require(a=={'initial_chunk_id':'cefa98','session_id':53935,'terminal_chunk_id':'afac4e','exit_code':1} and type(a['exit_code']) is int,'genuine Root original unique native failure exact four keys')
    require(failed['closed'] is True and type(failed['returncode']) is int and failed['returncode']==1 and failed['actual_tool_terminal_return_observed'] is True and failed['record_written_after_actual_terminal_return'] is True,'closed failure Root observation')
    require(observer['actual_tool_result']==dict(a,closed=True) and observer['successful_recorder_executed'] is False,'independent Root failure observer and no success recorder')
    require(failed['original_launch_command']==admitted['source_derived_unique_original_cold_CLI'],'exact original admitted native CLI')
    for record in (failed,observer):
        for k in ('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','scientific_qualification'):require(record[k] is False,'no native success or scientific credit')
    stdout=raw(failed['full_stdout']['path'],failed['full_stdout']['sha256']);stderr=raw(failed['full_stderr']['path'],failed['full_stderr']['sha256'])
    require(stdout==b'' and len(stderr)==3643 and failed['full_stdout']['bytes']==0 and failed['full_stderr']['bytes']==len(stderr),'full failed stdout zero and complete stderr actual bytes')
    require(stdout==raw(EXEC/'cold.stdout',failed['full_stdout']['sha256']) and stderr==raw(EXEC/'cold.stderr',failed['full_stderr']['sha256']),'exact raw business stdio preserved in Root terminal')
    require(stderr.endswith(b"RuntimeError: own-child 512 MiB RSS cap reached\n") and b'cold_launch_in_clean_process' in stderr and b'enforce_observed_peak' in stderr,'actual original source failure traceback')
    failure=load(failed['source_failure']['path'],failed['source_failure']['sha256'])
    status=load(failed['actual_run_status']['path'],failed['actual_run_status']['sha256'])
    stages=load(failed['actual_stages']['path'],failed['actual_stages']['sha256'])['stages']
    require(failure['classification']=='FAILED_COMBINED_COLD_NO_RETRY' and failure['error']=="RuntimeError('own-child 512 MiB RSS cap reached')",'source failure exact no retry')
    require(type(failure['actual_elapsed_seconds']) in (int,float) and 0<failure['actual_elapsed_seconds']<43200,'true failure elapsed finite original total cap')
    require(all(failure[k] is False for k in ('scientific_qualification','AAA_accuracy_qualified','ABA_admitted')),'failure no science flags')
    require(status['classification']=='FAILED_NO_RETRY' and status['case']=='AAA' and type(status['completed_maps']) is int and status['completed_maps']==0 and status['cases']=={} and status['prepared_sha256']==failed['original_prepared_cold']['sha256'],'actual failure AAA zero maps no case MET')
    require(status['error']=='own-child 512 MiB RSS cap reached' and status['reference_qualification'] is None,'original failure and no independent qualification')
    labels=['archives/pack_archives','training/common_basis','training/rank_precision','AAA/bootstrap/case_setup','AAA/bootstrap/white_tracking','AAA/bootstrap/make_route_contract','AAA/bootstrap/bootstrap_axial']
    require(type(stages) is list and len(stages)==7 and [s['label'] for s in stages]==labels,'exact actual initial stage order')
    reports=[]
    for i,s in enumerate(stages):
        failed_stage=i==6;folder=w/Path(s['label']).parent;name=Path(s['label']).name
        watch=load(folder/(name+'.watchdog.json'))
        require(watch['command']==s['command'],'stage/watch original command exact')
        require(s['status']==('FAILED' if failed_stage else 'PASS'),'actual stage outcome')
        require(type(s['wall_cap_seconds']) is float and s['wall_cap_seconds']==(4200.0 if failed_stage else 120.0),'every original stage cap exact')
        require(0<=watch['elapsed_seconds']<watch['wall_cap_seconds']<=s['wall_cap_seconds'],'actual watched elapsed within original cap')
        classification=own_pid(watch,failed_stage)
        log_bytes=raw(folder/(name+'.log'),None if failed_stage else s['log_sha256'])
        if failed_stage:
            require('log_sha256' not in s and 'resource_after' not in s and s['error']==status['error'],'failed stage missing success log/resource fields preserved absent')
            require(watch['pid']==35128 and watch['returncode']==-15 and watch['observed_peak_rss_mib']==513.890625 and watch['live_rss_sample_count']==580,'actual rejection peak PID sample facts')
            require(hashlib.sha256(log_bytes).hexdigest()==failed['failed_stage_full_log']['sha256'] and len(log_bytes)==failed['failed_stage_full_log']['bytes'],'complete actual failed log descriptor')
        compact={k:v for k,v in s.items() if k not in ('resource_before','resource_after')}
        reports.append({'stage_fields_preserved':compact,'original_resource_before_present':'resource_before' in s,'original_resource_after_present':'resource_after' in s,'watchdog_complete':watch,'own_pid_classification':classification,'log_actual_bytes':len(log_bytes),'log_actual_sha256':hashlib.sha256(log_bytes).hexdigest()})
    log=raw(failed['failed_stage_full_log']['path'],failed['failed_stage_full_log']['sha256']).decode()
    rows=[]
    for number,line in enumerate(log.splitlines(),1):
        if line.startswith('AXMAT-RANK1-CACHE PROGRESS '):
            parts=line.split();require(len(parts)==10,'complete progress row')
            integers=[int(x) for x in parts[2:5]]+[int(x) for x in parts[6:10]]
            residual=float(parts[5].replace('D','E'));require(math.isfinite(residual),'finite native progress')
            rows.append({'line':number,'text':line,'outer':integers[0],'group':integers[1],'inner':integers[2],'residual':residual,'builtblocks':integers[3],'reusedblocks':integers[4],'validated_hits':integers[5],'cache_bytes':integers[6]})
    require(len(rows)==19 and all(r['cache_bytes']==312518392 and r['builtblocks']==18130 for r in rows),'all actual partial progress same accounted cache bytes')
    require([rows[-1][k] for k in ('outer','group','inner','cache_bytes')]==[4,96,162,312518392],'actual final partial progress')
    require('AXMAT-RANK1-CACHE TERMINAL ' not in log and 'AXMAT-BOOTSTRAP-AXIAL-COMPLETE' not in log,'no cache or bootstrap completion marker')
    namespaces={}
    for key,root in roots.items():
        now=start_ns[key];base=c['original_namespaces'][key];old_files=dict(base['files']);old_links=dict(base['symlinks']);old_dirs=list(base['directories'])
        if key=='work':old_files['prepared_cold.json']=before_map[str(w/'prepared_cold.json')]['identity']
        if key=='terminal':
            for n in ('finalization.stdout','finalization.stderr','finalization_terminal_return.json'):old_files[n]=full_map[str(t/n)]['identity']
        require(set(old_files)<=set(now['files']) and all(now['files'][n]==v for n,v in old_files.items()),'every original current file seven identity exact '+key)
        require(set(old_dirs)<=set(now['directories']) and all(now['symlinks'].get(n)==v for n,v in old_links.items()),'old namespace dirs and links preserved '+key)
        added=set(now['files'])-set(old_files);new_dirs=set(now['directories'])-set(old_dirs);new_links={n:v for n,v in now['symlinks'].items() if n not in old_links}
        if key=='work':
            require(len(added)==41 and all(n=='cold_source_failure.json' or n.split('/')[0] in ('AAA','archives','training') for n in added),'all new actual failure files original output scope')
            require(new_dirs=={'AAA','AAA/bootstrap','archives','training'},'only expected original failure dirs')
            links={'training/training_snapshots.xsm':str(w/'archives/training_snapshots.xsm'),'archives/snapshot_A.xsm':cold['inputs']['snapshot_A']['path'],'archives/snapshot_B.xsm':cold['inputs']['snapshot_B']['path'],'AAA/bootstrap/case_snapshots.xsm':str(w/'archives/aaa_snapshots.xsm'),'AAA/bootstrap/initial_radial_track.bin':cold['inputs']['radial_track_A']['path']}
            require(new_links==links,'only original frozen explicit native input links')
        elif key=='terminal':require(added=={'cold_failed.stdout','cold_failed.stderr','cold_failed_terminal_return.json'} and not new_dirs and not new_links,'only Root actual failed terminal additions')
        else:require(not added and not new_dirs and not new_links,'source/control complete namespace invariant')
        namespaces[key]={'regular_files':len(now['files']),'all_prior_regular_seven_identities_exact':True,'old_directories_and_links_preserved':True,'actual_added_files':sorted(added),'actual_added_directories':sorted(new_dirs),'actual_added_links':new_links,'complete_actual_namespace':now}
    success_absent={'work':['cold_source_complete_result.json','cold_closeout_seal.json','complete_cold_closeout_seal.json','AAA/bootstrap/result.json','AAA/map001'],'terminal':['terminal_return.json']}
    for key,names in success_absent.items():require(all(not os.path.lexists(Path(roots[key])/n) for n in names),'actual success evidence absent '+key)
    require(all(identity(p['path'])==p['identity'] for p in PINS),'all metadata/source pin identities stable after review')
    require(all(namespace(root)==start_ns[key] for key,root in roots.items()),'complete four namespaces stable for whole review window')
    result={'schema':'AXMAT_V9_ACTUAL_COLD_FAILURE_TYPED_NAMESPACE_POSTREVIEW_V1','status':'PASS_ACTUAL_FAILURE_EVIDENCE_INPUT_INVARIANCE_ONLY_NO_NATIVE_SUCCESS_CREDIT','scope':'FINITE_METADATA_TYPED_ORIGINAL_SOURCE31_CONTROLS3_STDIO_STAGEWATCH_NAMESPACE_ONLY; GRAPH_PEER_OWNS_COMPLETE_GRAPH_AND_NEW_NUMERICAL_PAYLOAD_SEALS',
      'actual_original_native_failed_tool_result':a,'actual_original_native_closed':True,'Root_failed_terminal_sha256':'89e9c3d69d7d7e1f80934a5a3415525d3aba02d4808ea98e00ce775b67c80502','Root_failed_observer_sha256':'5a8601cbf5ae42cd397afc59bb990a3f09b3645dc94d8ec1acc1c8c79026eaee',
      'whole_prepared1290_and_original35f_bytes_unchanged':True,'whole_original_typed_order_float64bits_inverse_exact':True,'whole_original_serialized_byte_inverse_exact':True,'original_supervision_descriptors':supervision,
      'SOURCE31_fresh_fullSHA_and_seven_identity_preserved':True,'controlTerminal3_fresh_fullSHA_and_seven_identity_preserved':True,'actual_full_stdout_bytes':len(stdout),'actual_full_stderr_bytes':len(stderr),'source_failure_complete':failure,'actual_run_status_fields':{k:v for k,v in status.items() if k not in ('initial_resources','resource_roots')},
      'all_six_normal_initial_stages_have_real_own_PID_wait4':True,'failed_wait4_four_missing_fields_kept_None':True,'failed_stage_no_success_log_sha_or_resource_after_key_invented':True,'actual_stage_metadata_and_watchdogs':reports,'complete_four_current_namespaces':namespaces,'actual_success_paths_absent':success_absent,
      'actual_native_partial_progress_rows':rows,'memory_clue':{'observed_accounted_cache_bytes_all_rows':312518392,'observed_accounted_cache_mib':312518392/(1024.*1024.),'failed_real_live_RSS_mib':513.890625,'accounted_cache_is_not_process_RSS':True,'inference':'The reported cache allocation stays fixed through all19 partial progress rows; full process live RSS crosses512. This points to examining non-cache workspace lifetimes and transient arrays in the unchanged solver, but the log alone does not identify the allocation responsible.','native_cache_terminal_or_bootstrap_completion_observed':False},
      'fresh_fullSHA_metadata_source_pins':PINS,'new_canonical_35GB_scientific_payload_read':0,'new_native741MB_payload_hashed_by_this_reader':False,'project_written':False,'business_import_callback_API_executed':False,'native_executed_or_retried_by_reader':False,'native_RSS_verified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'scientific_qualification':False}
    p=OUT/'REPORT.json'
    with p.open('x') as f:json.dump(result,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
    b=p.read_bytes();print(json.dumps({'status':result['status'],'report':{'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)},'metadata_source_pins':len(PINS),'normal_initial_stages':6,'failed_stage':reports[-1]['watchdog_complete']['pid'],'native_success_credit':False},ensure_ascii=False))

if __name__=='__main__':main()
