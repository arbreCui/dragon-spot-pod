"""Exact eight old private copies. Future true v9 closure required; no import action."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess

ROOT=Path('/Users/wen/spot');REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011';ART=ROOT/'validation/artifacts'
PKG=Path(__file__).absolute().parent
BASE_PATH=REC/'storage_release_closed_v7_v8_project_pair_20261013/project_pair_release_common.py'
BASE_PIN=dict(path=str(BASE_PATH),sha256='b0a0a3d1f4eacfe8c9b91378b89aff1071a3907c2027a3fec857e160ae6e0b7d',size_bytes=18001,identity=[16777229,49980314,33188,1,18001,1791847138307427020,1791847138307427020])
def _bootstrap():
    before=BASE_PATH.lstat();identity=lambda q:[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]
    if not stat.S_ISREG(before.st_mode) or identity(before)!=BASE_PIN['identity']:raise RuntimeError('externally fixed original readonly base Source all7ID')
    fd=os.open(BASE_PATH,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        if identity(os.fstat(fd))!=identity(before):raise RuntimeError('base changed at Source open')
        data=b''
        while True:
            chunk=os.read(fd,65536)
            if not chunk:break
            data+=chunk
        if identity(os.fstat(fd))!=identity(before):raise RuntimeError('base Source changed at EOF')
    finally:os.close(fd)
    if identity(BASE_PATH.lstat())!=identity(before) or len(data)!=18001 or hashlib.sha256(data).hexdigest()!=BASE_PIN['sha256']:raise RuntimeError('base exact immutable fullEOF Source')
    spec=importlib.util.spec_from_file_location('original_readonly_exact_pair_helpers',BASE_PATH);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
b=_bootstrap()
pin=b.pin;same=b.same;read=b.read;identity=b.identity;guard=b.guard;write_new=b.write_new;update_owned=b.update_owned
NAMES=('initial_pack.xsm','axial_macro.xsm','axial_track.xsm','basis.xsm')
BRANCHES=[ART/('axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-'+v) for v in ('v5','v6')]
TARGETS=[branch/'AAA'/name for branch in BRANCHES for name in NAMES]
BYTES=998909696
V9_OUT=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v9'
V9_SUMMARY=V9_OUT/'Root_actual_three_plane_engineering_summary.json'
V9_TRUE_TOOL=REC/'ACTUAL_PIPELINE_V9_AFTER_EXACT_TWO_RELEASE_TRUE_TOOL_RETURNS_20261013.json'
MANIFEST=PKG/'EXACT_EIGHT_CLOSED_FAILED_V5_V6_PRIVATE_COPY_MANIFEST.json'
SF=PKG/'COMPLETE_EXACT_EIGHT_RELEASE_SOURCE_ONLY_FREEZE.json'
SOURCE_NAMES=('exact_eight_release_common.py','prepare_exact_eight_after_true_v9_closure.py','verify_or_execute_exact_eight.py')
SURVEY_PIN=dict(path=str(REC/'readonly_failed_v5_v6_candidate_survey_20261013/FINITE_EIGHT_FAILED_PRIVATE_COPY_CANDIDATE_REVIEW.json'),sha256='891fdfbac2daac8eb09f09f742035454c8f872f57ec2d28a8768f63233bc5bf8',size_bytes=212760,identity=[16777229,50011747,33188,1,212760,1791869336415739055,1791869336415739055])

def external(path,sha,seven):
    actual=pin(path)
    if actual['sha256']!=sha or actual['identity']!=json.loads(seven):raise RuntimeError('mandatory external SHA/all7ID mismatch '+str(path))
    return actual

def Source_gate(selected):
    if selected['path']!=str(SF):raise RuntimeError('exact Source-only freeze path')
    freeze=read(selected)
    if freeze['schema']!='COMPLETE_EXACT_EIGHT_FAILED_V5_V6_SOURCE_ONLY_RELEASE_FREEZE_V1' or freeze['final_manifest_created'] is not False or freeze['v9_terminal_prefilled'] is not False or freeze['deletion_executed'] is not False:raise RuntimeError('unexecuted Source-only freeze')
    if [p['path'] for p in freeze['Source_pins']]!=[str(PKG/n) for n in SOURCE_NAMES] or freeze['external_readonly_helper_pin']!=BASE_PIN or freeze['readonly_candidate_survey_pin']!=SURVEY_PIN:raise RuntimeError('exact three Source files and external fixed authority')
    for row in freeze['Source_pins']+[BASE_PIN,SURVEY_PIN]:same(row)
    if freeze['original_caps']!=dict(SELF_mib=512,whole_seconds=1800,stage_seconds=600,threads=1,children_at_once=1,fresh_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20):raise RuntimeError('original complete caps')
    return freeze

def writer_gate(toolpin,summarypin):
    if toolpin['path']!=str(V9_TRUE_TOOL) or summarypin['path']!=str(V9_SUMMARY):raise RuntimeError('exact future Root true terminal and actual v9 summary paths')
    tool=read(toolpin);summary=read(summarypin)
    terminal=tool.get('terminal',{});exit_code=terminal.get('exit_code')
    if tool.get('observed_closed') is not True or type(exit_code) is not int or exit_code not in (0,1) or tool.get('original_integer_exit_code')!=exit_code:raise RuntimeError('future v9 genuine true tool terminal exit0 or1 required')
    if summary.get('schema')!='ACTUAL_INDEPENDENT_AAA3_INITIAL_GLOBAL_PROJECT_BOOT_ENGINEERING_ROOT_V1' or not isinstance(summary.get('records'),list) or not summary['records'] or type(summary.get('engineering_three_plane_closed0')) is not bool:raise RuntimeError('actual v9 summary schema and records')
    if exit_code==0:
        if summary['engineering_three_plane_closed0'] is not True or summary.get('failure') is not None or summary.get('after_check_error') is not None:raise RuntimeError('exit0 Root actual summary must agree')
    elif summary['engineering_three_plane_closed0'] is not False:raise RuntimeError('exit1 must retain unqualified engineering status')
    closures=[]
    for record in summary['records']:
        label=record['label']
        if not isinstance(label,str) or '..' in Path(label).parts or Path(label).is_absolute():raise RuntimeError('canonical own stage label')
        wp=pin(V9_OUT/(label+'.watchdog.json'));w=read(wp);lp=pin(V9_OUT/(label+'.log'))
        if record['status'] not in ('PASS','FAILED') or type(w.get('returncode')) is not int or w.get('liveness_group_cleanup') is not True or w.get('own_child_only') is not True or w.get('command')!=record['command'] or w.get('rss_cap_mib')!=512:raise RuntimeError('every actual v9 ownchild genuinely closed')
        if record['status']=='PASS' and (w['returncode']!=0 or w.get('limit_failure') is not None or not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 or not 0<=w['sampled_peak_rss_mib']<512 or record.get('log_sha256')!=lp['sha256']):raise RuntimeError('v9 actual positive closure/caps unchanged')
        closures.append(dict(label=label,status=record['status'],watchdog_pin=wp,log_pin=lp,actual_returncode=w['returncode'],limit_failure=w.get('limit_failure')))
    # True parent closure plus every owned-child cleanup is checked, then inspect
    # current process metadata to refuse any live v9 host/runtime command.
    proc=subprocess.run(['/bin/ps','-axo','pid=,command='],text=True,capture_output=True,timeout=20)
    if proc.returncode!=0:raise RuntimeError('cannot read current host process metadata for v9 no-writer gate')
    needles=[str(REC/'aaa_three_plane_streaming_pipeline_source_v9/run_actual_three_plane_pipeline.py'),str(V9_OUT/'runtime/')]
    live=[]
    for line in proc.stdout.splitlines():
        fields=line.strip().split(None,1)
        if len(fields)==2 and int(fields[0])!=os.getpid() and any(n in fields[1] for n in needles):live.append(dict(pid=int(fields[0]),command=fields[1]))
    if live:raise RuntimeError('actual v9 owner/runtime remains live; no cleanup')
    outputs=summary.get('output_pins')
    if not isinstance(outputs,list) or not outputs:raise RuntimeError('all true v9 output fullpins required')
    for row in outputs:
        path=Path(row['path'])
        if not path.is_relative_to(V9_OUT):raise RuntimeError('v9 output pin leaves own namespace')
        same(row)
    return dict(Root_true_terminal_exit_code=exit_code,Root_true_tool_receipt_pin=toolpin,actual_v9_summary_pin=summarypin,all_actual_v9_stage_closures=closures,all_actual_v9_output_pins=outputs,engineering_status_preserved=summary['engineering_three_plane_closed0'],no_live_v9_host_or_runtime_command=True,future_success_not_assumed=True)

def current_protection_without_v9_terminal():
    core,dag=b.protection();table={r['path']:r for r in core};extra=[];events=[];roots=[]
    # Explicit current GENDF namespaces have different names from old v3.
    required=[REC/'current_eleven_saved_gendf_current_mount_host_source_v4',REC/'reaction_genDF_current_mount_stream_source_v2']
    for p in required:
        if not p.is_dir() or p.is_symlink():raise RuntimeError('mandatory actual current GENDF Source namespace absent')
    dynamic=sorted(p for p in REC.glob('current_formal_material_authority_exact_cache70_source_v*') if p.is_dir())
    if not dynamic:raise RuntimeError('actual newcurrent70 material Source namespace required')
    roots=required+dynamic
    def add(wanted):
        wanted=b.norm(wanted);actual=pin(wanted['path'])
        if actual!=wanted:
            if wanted['path']!=actual['path'] or wanted['sha256']!=actual['sha256'] or wanted['size_bytes']!=actual['size_bytes'] or wanted['identity'][0]!=16777234 or actual['identity'][0]!=16777229 or wanted['identity'][1:]!=actual['identity'][1:]:raise RuntimeError('additional current live Source dependency changed beyond explicit device34to29')
            events.append(dict(historical_pin=wanted,current_full_EOF_pin=actual,only_declared_device_transition=True))
        old=table.get(actual['path'])
        if old is not None and old!=actual:raise RuntimeError('conflicting live protected fullpin')
        table[actual['path']]=actual
    for path in roots:
        entries=sorted(str(p) for p in path.rglob('*') if p.is_file());origins=[]
        for name in entries:
            row=pin(name);add(row);origins.append(row)
            if Path(name).suffix=='.json':
                value=read(row)
                for wanted in b.nested(value):add(wanted)
        if entries!=sorted(str(p) for p in path.rglob('*') if p.is_file()):raise RuntimeError('current Source directory changed during closure')
        extra.append(dict(namespace=str(path),all_current_Source_and_metadata_full_EOF_pins=origins))
    for row in [BASE_PIN,SURVEY_PIN]:add(row)
    dag.update(additional_exact_current_source_namespaces=extra,additional_explicit_current_device_only_reattestations=events,v9_terminal_not_claimed_by_this_Source_only_collection=True)
    return sorted(table.values(),key=lambda r:r['path']),dag

def protection(toolpin,summarypin):
    current,dag=current_protection_without_v9_terminal();table={r['path']:r for r in current}
    closure=writer_gate(toolpin,summarypin)
    selected=[toolpin,summarypin]+closure['all_actual_v9_output_pins']
    for row in closure['all_actual_v9_stage_closures']:selected.extend([row['watchdog_pin'],row['log_pin']])
    for row in selected:
        same(row);old=table.get(row['path'])
        if old is not None and old!=row:raise RuntimeError('conflicting actual v9 protected fullpin')
        table[row['path']]=row
    dag.update(actual_closed_v9_protection=closure,all_actual_v9_current_output_pins_protected=True)
    return sorted(table.values(),key=lambda r:r['path']),dag

def owned_disjoint(row,protected):
    paths={r['path'] for r in protected};inodes={tuple(r['identity'][:2]) for r in protected}
    if row['path'] not in [str(p) for p in TARGETS] or not stat.S_ISREG(row['identity'][2]) or row['identity'][3]!=1 or row['path'] in paths or tuple(row['identity'][:2]) in inodes:raise RuntimeError('exact current owned disjoint regular nlink1 candidate')
    same(row)

def closed_old_proofs():
    survey=read(SURVEY_PIN);proofs=survey['closed_failed_v5_v6_proofs'];candidates=survey['candidates']
    if survey['deletion_executed'] is not False or len(candidates)!=8 or survey['total_candidate_logical_bytes']!=BYTES or [r['current_fullpin']['path'] for r in candidates]!=[str(p) for p in TARGETS]:raise RuntimeError('finite exact eight readonly survey authority')
    for proof in proofs:
        summary=read(proof['failed_overall_summary_pin']);tool=read(proof['Root_true_closed_exit1_tool_pin']);same(proof['actual_owning_Source_pin']);same(proof['independent_native_PACK_readback_pin'])
        if summary['status']!='FAILED_UNQUALIFIED_NO_RETRY' or summary['engineering_three_plane_closed0'] is not False or summary['after_check_error'] is not None or len(summary['records'])!=33 or summary['records'][-1]['label']!='AAA/global_positive':raise RuntimeError('old failed aggregate unchanged')
        terminal=tool['final'] if proof['version']=='v5' else tool['terminal']
        if terminal['exit_code']!=1:raise RuntimeError('genuine old failedRoot terminal')
        for record in proof['all33_actual_child_closure_and_log_pins']:
            w=read(record['watchdog_pin']);same(record['log_pin'])
            if w['returncode']!=record['actual_returncode'] or w['limit_failure']!=record['limit_failure'] or w['liveness_group_cleanup'] is not True or w['own_child_only'] is not True:raise RuntimeError('old actual closed watchdog unchanged')
    for row in candidates:same(row['current_fullpin'])
    return proofs,[r['current_fullpin'] for r in candidates]

def disjoint(targets,protected):
    if [p['path'] for p in targets]!=[str(p) for p in TARGETS] or len(targets)!=8 or sum(p['size_bytes'] for p in targets)!=BYTES:raise RuntimeError('exact eight literal candidates only')
    for row in targets:owned_disjoint(row,protected)

def inventory():
    files={};links={};dirs={};stack=list(BRANCHES)
    while stack:
        path=stack.pop();before=path.lstat()
        if not stat.S_ISDIR(before.st_mode):raise RuntimeError('ordinary old branch directory')
        dirs[str(path)]=identity(before);fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:
            with os.scandir(fd) as entries:
                for entry in entries:
                    q=path/entry.name;s=entry.stat(follow_symlinks=False)
                    if stat.S_ISDIR(s.st_mode):stack.append(q)
                    elif stat.S_ISREG(s.st_mode):files[str(q)]=identity(s)
                    elif stat.S_ISLNK(s.st_mode):links[str(q)]=dict(identity=identity(s),target=os.readlink(q))
                    else:raise RuntimeError('unexpected special old branch entry')
        finally:os.close(fd)
        guard()
    return dict(ordinary_file_identities=files,symlinks=links,directory_identities=dirs)

def budget():return b.budget()
