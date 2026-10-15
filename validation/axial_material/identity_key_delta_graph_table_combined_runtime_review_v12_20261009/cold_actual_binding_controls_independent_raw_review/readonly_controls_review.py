import ast
import hashlib
import json
import math
import os
from pathlib import Path
import stat

WORK=Path('/Users/wen/spot/validation/artifacts/axial-material-owned-specs-identity-key-delta-graph-table-cold-runtime-v12-20261009')
CONTROL=WORK/'binding_controls'
TERM=Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-cold-controls-terminal-v12-20261009')
OUTPUT=Path('/private/tmp/axmat_v12_actual_binding_controls_independent_raw_review_20261009')
SEAL_SHA='b90f8a781dc8ad0044b7f30e6e7169077f0124fce3d77b83cbc650781ed9e4e3'
TERM_SHA='5acffc484f1f78bc5df6520d98cc97f0234161ae8185b863384679d032a9e583'
CONTROL_SOURCE_SHA='d4da69dbf099f8527e50d837c27ec9fc94aa105e37530ccfe8c11d68a7767393'
HOST_SOURCE_SHA='dd2fad02343cb8ae9d4a4df428ddaf00885d6204d00cf8a2bdd5ac48e00ecaf7'
BOUNDED_SOURCE_SHA='bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09'
P14='/opt/homebrew/Cellar/python@3.14/3.14.4_1/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
MARKER='POSITIVE_NEW_CANONICAL_OWN_CHILD_CONTROL_COMPLETE'
REASON='own-child 512 MiB RSS cap reached'
PEAK_CONTRACT='EXACT_OWN_PID_DARWIN_WAIT4_BYTES_AND_LIVE_PS_V1'
seen={}
def require(value,label):
    if not value:raise ValueError(label)
def signature(info):
    return tuple(getattr(info,n)for n in ('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns'))
def ordinary(path):
    p=Path(path)
    require(p.is_absolute()and '..'not in p.parts,'absolute ordinary path')
    for x in [*reversed(p.parents),p]:
        info=x.lstat();require(not stat.S_ISLNK(info.st_mode),'no pathname aliases')
        if x!=p:require(stat.S_ISDIR(info.st_mode),'ordinary directory ancestors')
    return p
def read(path,expected=None):
    p=ordinary(path);before=signature(p.lstat());require(stat.S_ISREG(before[2]),'regular readonly input')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        require(signature(os.fstat(fd))==before,'opened pathname identity')
        chunks=[]
        while chunk:=os.read(fd,2**20):chunks.append(chunk)
        raw=b''.join(chunks);require(signature(os.fstat(fd))==before,'same bytes identity during read')
    finally:os.close(fd)
    require(signature(p.lstat())==before and len(raw)==before[4],'stable complete read')
    sha=hashlib.sha256(raw).hexdigest()
    if expected is not None:require(sha==expected,'expected SHA '+str(p))
    seen[str(p)]=dict(sha256=sha,bytes=len(raw),identity=list(before))
    return raw
def strict(raw):
    def members(rows):
        d={}
        for k,v in rows:require(k not in d,'duplicate JSON key');d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=members,parse_constant=lambda s:(_ for _ in()).throw(ValueError(s)))
def doc(path,sha=None):return strict(read(path,sha))
def finite_number(x):return type(x)in(int,float)and math.isfinite(x)
seal=doc(CONTROL/'seal.json',SEAL_SHA)
require(seal['schema']=='AXMAT_COMBINED_PHYSICAL_MEMORY_CANONICAL_GUARD_SEAL_V1','seal schema')
files={};directories=[]
for folder,dirs,names in os.walk(CONTROL,followlinks=False):
    for name in dirs:
        p=ordinary(Path(folder)/name);require(p.is_dir(),'ordinary control directory');directories.append(str(p.relative_to(CONTROL)))
    for name in names:
        p=Path(folder)/name;require(stat.S_ISREG(ordinary(p).lstat().st_mode),'control regular endpoint')
        relative=str(p.relative_to(CONTROL))
        if relative!='seal.json':files[relative]=read(p,seal['files'].get(relative))
require(set(files)==set(seal['files'])and len(files)==9,'complete nine-member success namespace')
require(sorted(directories)==sorted(seal['namespace_directories'])==['oversize','positive','short'],'complete three namespace directories')
claim=strict(files['claim.json']);result=strict(files['result.json']);stages=strict(files['stages.json'])['stages']
terminal=doc(TERM/'terminal_return.json',TERM_SHA)
require(terminal['actual_tool_result']==dict(initial_chunk_id='45095a',session_id=4925,terminal_chunk_id='1a4690',exit_code=0),'actual Root tool observation')
require(terminal['returncode']==0 and terminal['actual_tool_terminal_return_observed']is True and terminal['record_written_after_actual_terminal_return']is True,'actual terminal return')
require(terminal['control_seal']==dict(path=str(CONTROL/'seal.json'),sha256=SEAL_SHA),'actual new seal identity')
stdout=doc(terminal['full_stdout']['path'],terminal['full_stdout']['sha256'])
require(read(terminal['full_stderr']['path'],terminal['full_stderr']['sha256'])==b'','empty complete actual stderr')
require(stdout['result']==result,'whole actual stdout/result identity')
for key in ('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources'):
    require(stdout[key]==terminal[key],'whole actual stdout terminal tail '+key)
require(terminal['actual_tail_check']=='PASS'and finite_number(terminal['actual_elapsed_seconds'])and 0<terminal['actual_elapsed_seconds']<120,'whole actual original120 cap')
require(0<result['elapsed_before_closeout']<=terminal['actual_elapsed_seconds'],'before/all-closeout monotonic order')
require(result['classification']=='PASS_NEW_CANONICAL_OWN_RSS_BINDING_CONTROLS_ONLY','controls-only result')
require(result['caps']==dict(rss_cap_mib=512,control_stage_seconds=60,control_total_seconds=120,control_archive_reserve_bytes=64*2**20,cold_total_seconds=43200,min_free_bytes=8*2**30,history_cap_bytes=96*2**30,threads=1,children_at_once=1,retries=0),'entire original caps')
require(claim['retries']==0 and claim['binding']==result['binding']==terminal['binding'],'one claim and common binding')
require(type(claim['pid'])is int and claim['pid']>0,'actual host claim PID')
for key in ('positive_completed','actual_oversize_rejected','short_completed','own_children_no_longer_live'):require(result[key]is True,'whole three-control success '+key)
for key in ('scientific_qualification','Dragon_started','transport_started','new_assembly_or_linear_solve','AAA_accuracy_qualified','ABA_admitted'):require(result[key]is False,'no unrelated credit '+key)
require(result['short_allocation_bytes']==16*2**20 and result['rss_peak_observation_contract']==PEAK_CONTRACT,'short actual allocation contract')
source_raw=read(WORK/'runtime/combined_cold_own_rss_controls.py',CONTROL_SOURCE_SHA)
canonical=read('/Users/wen/spot/validation/axial_material/combined_cold_own_rss_controls_own_pid_peak_20261008.py',CONTROL_SOURCE_SHA)
require(source_raw==canonical,'whole genuine copied three-fixture source')
source=source_raw.decode();tree=ast.parse(source)
source_defs={n.name:ast.get_source_segment(source,n)for n in tree.body if isinstance(n,ast.FunctionDef)}
require(all(n in source_defs for n in ('fixture','run_controls','watch_admission')),'all actual control source definitions')
assign={n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)}
require(ast.get_source_segment(source,assign['OVERSIZE_BYTES'])=='576 * 2**20','real oversize576 MiB allocation source')
fixture=source_defs['fixture'];run=source_defs['run_controls']
require('payload = bytearray(nbytes)'in fixture and 'for offset in range(0, nbytes, 4096):'in fixture and 'payload[offset] = 1'in fixture,'actual full page touch source')
require("time.sleep(.8)"in fixture and "time.sleep(65)"in fixture and "if mode == 'short':"in fixture,'three original fixture behaviors')
require("executor = full.OwnRSSSerialExecutor(Path(b['work_root']),120,'binding_controls',resources)"in run and "executor.execute(directory,'execute',command,60,"in run,'genuine original120/60 constructor/call')
require("executor.bounded.process_group_exists(watch['pid'])"in run,'actual archived post-cleanup liveness observation source')
read(WORK/'runtime/combined_cold_own_rss_host.py',HOST_SOURCE_SHA)
read(WORK/'runtime/run_bounded_dragon.py',BOUNDED_SOURCE_SHA)
require(terminal['source']==dict(path=str(WORK/'runtime/combined_cold_own_rss_controls.py'),sha256=CONTROL_SOURCE_SHA),'actual source command pin')
require(terminal['host']==dict(path=str(WORK/'runtime/combined_cold_own_rss_host.py'),sha256=HOST_SOURCE_SHA),'actual host source pin')
expected_run=[P14,str(WORK/'runtime/combined_cold_own_rss_controls.py'),'run-controls','--binding',str(WORK/'own_rss_binding.json'),'--binding-sha256',result['binding']['sha256']]
require(terminal['command']==expected_run,'actual canonical P14 host command')
require(len(stages)==3 and [s['status']for s in stages]==['PASS','FAILED','PASS'],'three original exact statuses')
require([o['mode']for o in result['observations']]==['positive','oversize','short'],'three exact observation modes')
details=[];pids=[]
for mode,stage,observation in zip(('positive','oversize','short'),stages,result['observations']):
    watch=strict(files[mode+'/execute.watchdog.json']);raw_log=files[mode+'/execute.log']
    command=[P14,str(WORK/'runtime/combined_cold_own_rss_controls.py'),'fixture',mode]
    require(stage['label']=='binding_controls/'+mode+'/execute'and stage['command']==watch['command']==observation['command']==command,'actual mode command/stage')
    require(stage['wall_cap_seconds']==60 and 0<=stage['elapsed_seconds']<60 and 0<=watch['elapsed_seconds']<watch['wall_cap_seconds']<=60,'original60 actual stage cap')
    require(type(watch['pid'])is int and watch['pid']>0 and watch['pid']!=claim['pid'],'actual distinct own child PID');pids.append(watch['pid'])
    require(watch['rss_cap_mib']==512 and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and observation['actual_group_no_longer_live']is True,'all archived own-child group cleanup observations')
    require(observation['watch']==watch and observation['watchdog']==dict(path=str(CONTROL/mode/'execute.watchdog.json'),sha256=seal['files'][mode+'/execute.watchdog.json'])and observation['raw_log']==dict(path=str(CONTROL/mode/'execute.log'),sha256=seal['files'][mode+'/execute.log']),'whole raw watch/log identity')
    requested=16*2**20 if mode in ('positive','short')else 576*2**20
    lines=raw_log.splitlines();expected_allocation=dict(kind='ACTUAL_OWN_CHILD_ALLOCATION_INTENT',mode=mode,pid=watch['pid'],requested_bytes=requested)
    require(len(lines)==2 and strict(lines[0])==expected_allocation,'complete actual raw allocation PID/bytes')
    sampled=watch['sampled_peak_rss_mib'];observed=watch['observed_peak_rss_mib'];count=watch['live_rss_sample_count'];kernel=watch['own_pid_wait4_peak_rss_mib']
    require(finite_number(sampled)and sampled>=0 and finite_number(observed)and observed>=0 and type(count)is int and count>=0 and (count!=0 or sampled==0),'finite raw sample/actual count')
    require(watch['rss_peak_observation_contract']==PEAK_CONTRACT,'exact own-PID contract')
    if mode in ('positive','short'):
        require(lines[1]==MARKER.encode()and watch['returncode']==0 and watch['limit_failure']is None,'actual normal fixture marker/exit')
        require(observation['actual_expected_rejection']is None and stage['log_sha256']==seal['files'][mode+'/execute.log'],'normal stage raw identity')
        require(watch['own_pid_wait4_observed']is True and watch['own_pid_wait4_pid']==watch['pid'],'real returned own-PID')
        status=watch['own_pid_wait4_status'];raw=watch['own_pid_wait4_ru_maxrss_bytes']
        require(type(status)is int and os.WIFEXITED(status)and os.waitstatus_to_exitcode(status)==0,'actual wait4 exit status')
        require(type(raw)is int and raw>0 and kernel==raw/2**20 and observed==max(sampled,kernel)and 0<observed<512,'integer Darwin-byte own-PID kernel maximum')
        require(count==0 and sampled==0,'retain legitimate zero live samples')
    else:
        require(lines[1]==b'ACTUAL_OVERSIZE_ALLOCATION_TOUCHED_WAITING_FOR_ORIGINAL_RSS_GUARD','actual oversize fully touched allocation marker')
        require(watch['returncode']in(-15,-9)and watch['limit_failure']=="RuntimeError('own-child 512 MiB RSS cap reached')"and stage['error']==REASON and observation['actual_expected_rejection']==REASON,'actual original512 live rejection')
        require(count>0 and sampled>=512 and observed==sampled and watch['own_pid_wait4_observed']is False,'actual sampled oversize peak')
        require(all(watch[k]is None for k in ('own_pid_wait4_pid','own_pid_wait4_status','own_pid_wait4_ru_maxrss_bytes','own_pid_wait4_peak_rss_mib')),'no invented absent kernel receipt')
    details.append(dict(mode=mode,pid=watch['pid'],stage_status=stage['status'],returncode=watch['returncode'],requested_bytes=requested,live_sample_count=count,sampled_peak_rss_mib=sampled,own_pid_wait4_observed=watch['own_pid_wait4_observed'],own_pid_wait4_ru_maxrss_bytes=watch['own_pid_wait4_ru_maxrss_bytes'],own_pid_wait4_peak_rss_mib=kernel,observed_peak_rss_mib=observed,archived_group_cleanup_observed=True,full_raw_allocation_log_and_watch_equal=True))
require(len(set(pids))==3,'three unique actual own children')
for previous,current in zip(stages,stages[1:]):require(current['started_unix']>=previous['started_unix']+previous['elapsed_seconds'],'serial no overlapping stage starts')
binding=ordinary(WORK/'own_rss_binding.json');binding_size=binding.stat().st_size
controls_archive_bytes=sum((CONTROL/rel).stat().st_size for rel in seal['files'])+(CONTROL/'seal.json').stat().st_size
archive_bytes=controls_archive_bytes+(WORK/'runtime/combined_cold_own_rss_host.py').stat().st_size+(WORK/'runtime/combined_cold_own_rss_controls.py').stat().st_size+binding_size
require(archive_bytes==terminal['actual_archive_bytes']==61965994 and archive_bytes<64*2**20,'independent original exact archive accounting')
for path,pin in seen.items():require(signature(ordinary(path).lstat())==tuple(pin['identity']),'entire finite audit identity retained')
report=dict(schema='AXMAT_V12_INDEPENDENT_ACTUAL_THREE_BINDING_CONTROLS_READONLY_RAW_REVIEW_V1',status='PASS_RAW_THREE_FIXTURES_SEAL_STAGE_WATCH_ALLOCATION_OWN_PID_AND_ARCHIVE',control_seal=dict(path=str(CONTROL/'seal.json'),sha256=SEAL_SHA),actual_control_terminal=dict(path=str(TERM/'terminal_return.json'),sha256=TERM_SHA),actual_Root_tool=dict(initial_chunk_id='45095a',session_id=4925,terminal_chunk_id='1a4690',exit_code=0),complete_sealed_control_members=9,complete_sealed_control_directories=['oversize','positive','short'],stages=['PASS','FAILED','PASS'],details=details,total_wall_cap_seconds=120,stage_wall_cap_seconds=60,RSS_cap_mib=512,threads=1,children_at_once=1,retries=0,actual_elapsed_seconds=terminal['actual_elapsed_seconds'],actual_archive_bytes=archive_bytes,complete_controls_namespace_bytes=controls_archive_bytes,binding_size_only_checked=binding_size,binding_byte_hash_and_MRO_whole_INPUT_review_left_to_Root=True,no_current_process_liveness_poll=True,source_fixture_and_run_controls_byteexact_to_original=True,three_raw_source_allocation_modes_verified=True,zero_live_samples_valid_only_with_real_own_PID_wait4_for_positive_short=True,oversize_kernel_None_retained_without_synthetic_values=True,all_six_logs_and_watches_fresh_SHA_verified=True,file_pins=seen,project_written=False,only_TMP_report_written=True,business_imported=False,business_or_fixture_executed=False,session_polled=False,whole_35GB_INPUT_not_reread=True,native_transport_RSS_qualification=False,AAA_accuracy_qualified=False,ABA_admitted=False)
raw=(json.dumps(report,sort_keys=True,indent=2)+'\n').encode();path=OUTPUT/'REPORT.json'
with path.open('xb')as f:f.write(raw)
print(json.dumps(dict(status=report['status'],report_path=str(path),report_sha256=hashlib.sha256(raw).hexdigest(),report_bytes=len(raw),all9_control_seal_files_verified=True,actual_elapsed_seconds=report['actual_elapsed_seconds'],actual_archive_bytes=archive_bytes,details=details,source_audit_only_no_business_or_fixture_execution=True),sort_keys=True,indent=2))
