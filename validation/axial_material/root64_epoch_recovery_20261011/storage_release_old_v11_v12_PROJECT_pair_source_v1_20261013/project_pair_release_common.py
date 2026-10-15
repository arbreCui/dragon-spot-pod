"""Exact two closed failed-run PROJECT copies; future v14 proofs mandatory."""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

ROOT=Path('/Users/wen/spot');REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011';ART=ROOT/'validation/artifacts';PKG=Path(__file__).absolute().parent
BASE=REC/'storage_release_closed_v7_v8_project_pair_20261013/project_pair_release_common.py'
BASE_PIN=dict(path=str(BASE),sha256='b0a0a3d1f4eacfe8c9b91378b89aff1071a3907c2027a3fec857e160ae6e0b7d',size_bytes=18001,identity=[16777229,49980314,33188,1,18001,1791847138307427020,1791847138307427020])
def _base():
    ident=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    before=BASE.lstat()
    if not stat.S_ISREG(before.st_mode)or ident(before)!=BASE_PIN['identity']:raise RuntimeError('original helper opening all7ID')
    fd=os.open(BASE,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb')as f:
        if ident(os.fstat(f.fileno()))!=ident(before):raise RuntimeError('helper FD all7ID')
        digest=hashlib.file_digest(f,'sha256').hexdigest()
        if ident(os.fstat(f.fileno()))!=ident(before):raise RuntimeError('helper EOF all7ID')
    if ident(BASE.lstat())!=ident(before)or digest!=BASE_PIN['sha256']:raise RuntimeError('original helper exact bytes')
    spec=importlib.util.spec_from_file_location('original_readonly_pair_helpers',BASE);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
b=_base();pin=b.pin;same=b.same;read=b.read;identity=b.identity;guard=b.guard;write_new=b.write_new
BRANCHES=[ART/('axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-'+v)for v in('v11','v12')]
TARGETS=[p/'AAA/projected_boot.xsm'for p in BRANCHES];BYTES=1498711904
TARGET_SELECTED_PINS=[dict(path=str(TARGETS[0]),sha256='ea56e0e58889469c81e1519713ca0df93a3ebb5f2b1a1fbd2e20b5d8be72833a',size_bytes=749355952,identity=[16777229,50021102,33152,1,749355952,1791875213411752860,1791875213411752860]),dict(path=str(TARGETS[1]),sha256='ea56e0e58889469c81e1519713ca0df93a3ebb5f2b1a1fbd2e20b5d8be72833a',size_bytes=749355952,identity=[16777229,50033662,33152,1,749355952,1791883659443152378,1791883659443152378])]
SURVEY=REC/'readonly_v11_v12_private_PROJECT_dependency_survey_20261013/REVIEW.json'
SURVEY_PIN=dict(path=str(SURVEY),sha256='7cb7e01bae8cf84f24270df4086854405a67561c20996ead6d9e710a6cf0986a',size_bytes=668098,identity=[16777229,50047585,33188,1,668098,1791891645619713603,1791891645619713603])
OLD_MANIFEST=REC/'storage_release_old_v10_single_PROJECT_source_v3_20261013/EXACT_SINGLE_OLD_V10_PRIVATE_PROJECT_RELEASE_MANIFEST.json'
V13_OUT=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261013-v13'
FUTURE_V14_HF_PIN=None;FUTURE_V14_CLI_PIN=None
SOURCE_NAMES=('project_pair_release_common.py','prepare_exact_project_pair_manifest.py','verify_or_execute_exact_project_pair.py')
SF=PKG/'COMPLETE_EXACT_OLD_V11_V12_PROJECT_RELEASE_SOURCE_FREEZE.json'
FINAL=PKG/'EXACT_OLD_V11_V12_PRIVATE_PROJECT_PAIR_RELEASE_MANIFEST.json'
RECEIPTS=REC/'storage_release_old_v11_v12_PROJECT_pair_actual_receipts_20261013'
CAPS=dict(SELF_mib=512,whole_seconds=1800,stage_seconds=600,threads=1,children_at_once=1,fresh_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20)

def external(path,sha,seven):
    row=pin(path)
    if row['sha256']!=sha or row['identity']!=json.loads(seven):raise RuntimeError('external exact SHA/all7ID '+str(path))
    return row

def receipt_pin(p):
    # Only bounded failure evidence bypasses an already failed admission guard.
    # This never grants resource or business admission.
    p=Path(p);before=p.lstat()
    if not stat.S_ISREG(before.st_mode)or before.st_nlink!=1 or before.st_uid!=os.getuid()or before.st_size>64*2**20:raise RuntimeError('bounded own exclusive receipt')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb')as f:
        if identity(os.fstat(f.fileno()))!=identity(before):raise RuntimeError('receipt FD all7')
        sha=hashlib.file_digest(f,'sha256').hexdigest()
        if identity(os.fstat(f.fileno()))!=identity(before):raise RuntimeError('receipt EOF all7')
    if identity(p.lstat())!=identity(before):raise RuntimeError('receipt path all7')
    return dict(path=str(p),sha256=sha,size_bytes=before.st_size,identity=identity(before))

def update_owned(p,value,old):
    if str(value.get('status','')).startswith('STOPPED_'):
        if receipt_pin(p)!=old:raise RuntimeError('failure receipt changed')
    else:same(old)
    raw=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
    if len(raw)>64*2**20:raise RuntimeError('bounded receipt publication')
    fd=os.open(p,os.O_RDWR|os.O_NOFOLLOW)
    with os.fdopen(fd,'r+b')as f:
        before=identity(os.fstat(f.fileno()))
        if before!=old['identity']or before[3]!=1 or Path(p).lstat().st_uid!=os.getuid():raise RuntimeError('same owned receipt FD before write')
        f.seek(0);f.truncate(0);f.write(raw);f.flush();os.fsync(f.fileno())
        after=identity(os.fstat(f.fileno()))
        if after!=identity(Path(p).lstat())or after[:4]!=before[:4]:raise RuntimeError('same receipt inode/mode/nlink after write')
    return receipt_pin(p)

def source_gate(row):
    if row['path']!=str(SF):raise RuntimeError('exact own Source freeze required')
    d=read(row)
    if d['schema']!='COMPLETE_EXACT_OLD_V11_V12_PROJECT_PARAMETERIZED_SOURCE_FREEZE_V1'or d['deletion_executed']is not False or d['manifest_prepared']is not False or d['future_v14_HF_pin']is not None or d['future_v14_CLI_pin']is not None or d['original_caps']!=CAPS or d['original_readonly_helper_pin']!=BASE_PIN or d['actual_readonly_survey_pin']!=SURVEY_PIN or[p['path']for p in d['Source_pins']]!=[str(PKG/n)for n in SOURCE_NAMES]:raise RuntimeError('complete actual parameterized Source-only freeze')
    for p in d['Source_pins']+d['immutable_readonly_evidence_pins']+[BASE_PIN,SURVEY_PIN,d['original_resource_factory_pin']]:same(p)
    if d['original_resource_factory_pin']['path']!=str(b.FACTORY):raise RuntimeError('original unchanged history factory')
    return d

def inventory(roots=BRANCHES):
    files={};links={};dirs={};stack=list(roots)
    while stack:
        p=stack.pop();b.ancestors(p);before=p.lstat()
        if not stat.S_ISDIR(before.st_mode):raise RuntimeError('ordinary branch directory')
        dirs[str(p)]=identity(before);fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:
            if identity(os.fstat(fd))!=identity(before):raise RuntimeError('directory changed at FD open')
            with os.scandir(fd)as entries:
                for e in entries:
                    q=p/e.name;s=e.stat(follow_symlinks=False)
                    if stat.S_ISDIR(s.st_mode):stack.append(q)
                    elif stat.S_ISREG(s.st_mode):files[str(q)]=identity(s)
                    elif stat.S_ISLNK(s.st_mode):links[str(q)]=dict(identity=identity(s),target=os.readlink(q))
                    else:raise RuntimeError('branch special entry')
            if identity(os.fstat(fd))!=identity(before):raise RuntimeError('directory changed while scanning')
        finally:os.close(fd)
        guard()
    return dict(ordinary_file_identities=files,symlinks=links,directory_identities=dirs)

def closed_proofs():
    proofs=[]
    for version,branch,target in zip(('v11','v12'),BRANCHES,TARGET_SELECTED_PINS):
        sp=pin(branch/'Root_actual_three_plane_engineering_summary.json');d=read(sp);rp=pin(branch/'Root_actual_complete_execution_record_before_final_publication.json');raw=read(rp)
        tp=pin(REC/('ACTUAL_PIPELINE_V11_TRUE_TOOL_RETURNS_20261013.json'if version=='v11'else'ACTUAL_PIPELINE_V12_PARENT_PHASE_ROOT_TRUE_TOOL_RETURNS_20261013.json'));t=read(tp)
        if d['schema']!='ACTUAL_INDEPENDENT_AAA3_INITIAL_GLOBAL_PROJECT_BOOT_ENGINEERING_ROOT_V1'or d['status']!='FAILED_UNQUALIFIED_NO_RETRY'or d['failure']!='RuntimeError: original SELF 512MiB cap'or d['after_check_error']!='RuntimeError: original SELF 512MiB cap'or d['engineering_three_plane_closed0']is not False or d['actual_terminal']is not None or d['output_pins']!=[]or t['observed_closed']is not True or type(t['original_integer_exit_code'])is not int or t['original_integer_exit_code']!=1 or t['terminal']['exit_code']!=1:raise RuntimeError('true old aggregate failure and Root closed1')
        if[{k:v for k,v in r.items()if k not in('resource_before','resource_after')}for r in raw['records']]!=d['records']or read(pin(branch/'AAA3-streaming/stages.json'))!={'stages':raw['records']}or target not in raw['owned_runtime_pins']:raise RuntimeError('complete original raw ledger and actual owned PROJECT')
        rows={r['label']:r for r in d['records']}
        if len(rows)!=len(d['records'])or rows['AAA/global_positive']['status']!='PASS'or rows['AAA/project_positive']['status']!='PASS':raise RuntimeError('individual GLOBAL/PROJECT actual PASS retained')
        watches=[]
        for r in d['records']:
            wp=pin(branch/(r['label']+'.watchdog.json'));w=read(wp);lp=pin(branch/(r['label']+'.log'));expected=0 if r['status']=='PASS'else 1
            if r['status']not in('PASS','FAILED')or type(w['returncode'])is not int or w['returncode']!=expected or w['command']!=r['command']or w['own_child_only']is not True or w['liveness_group_cleanup']is not True or w['limit_failure']is not None or w['rss_cap_mib']!=512 or not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 or not 0<=w['sampled_peak_rss_mib']<512:raise RuntimeError('all actual old children closed at original limits')
            if r['status']=='PASS'and lp['sha256']!=r['log_sha256']:raise RuntimeError('old successful complete log changed')
            watches.append(dict(label=r['label'],status=r['status'],returncode=w['returncode'],watchdog_pin=wp,log_pin=lp))
        proofs.append(dict(version=version,summary_pin=sp,raw_pin=rp,Root_true_exit1_pin=tp,actual_stage_count=len(d['records']),actual_positive_closed0_count=sum(r['status']=='PASS'for r in d['records']),actual_expected_negative_closed1_count=sum(r['status']=='FAILED'for r in d['records']),all_actual_child_closures=watches,GLOBAL_PROJECT_individual_PASS_preserved=True,failed_BOOT_unqualified=True,full_PROJECT_GLOBAL_old_raw_replay_unavailable_after_release=True))
    return proofs

def review_gate(hfpin,clipin,reviewpin,toolpin):
    d=read(reviewpin);t=read(toolpin)
    if d.get('host_freeze_pin')!=hfpin or d.get('CLI_pin')!=clipin or d.get('failure')is not None or d.get('business_executed',d.get('candidate_import_compiler_or_child_started'))is not False or t.get('observed_closed')is not True or type(t.get('original_integer_exit_code'))is not int or t['original_integer_exit_code']!=0:raise RuntimeError('true Source review bound to exact v14HF/CLI')
    actual=t.get('actual_review_return')
    if not isinstance(actual,dict)or type(actual.get('exit_code'))is not int or actual['exit_code']!=0:raise RuntimeError('complete genuine Source audit tool0 required')
    result=json.loads(actual['output'])
    if result.get('review_pin')!=reviewpin:raise RuntimeError('actual tool0 output must select exact review PF')

def current_protection(sfpin,hfpin,clipin,review_inputs):
    frozen=source_gate(sfpin);survey=read(SURVEY_PIN);oldrow=next(p for p in frozen['immutable_readonly_evidence_pins']if p['path']==str(OLD_MANIFEST));old=read(oldrow)
    table={};roles={};origins=[];mapping={};reattests=[]
    def add(row,role):
        row=b.norm(row);actual=pin(row['path'])
        if actual!=row:
            selected=mapping.get(json.dumps(row,sort_keys=True))
            if selected is None or selected['current_pin']!=actual:raise RuntimeError('live pin not exact current or explicitly v14-mapped historical device '+row['path'])
            event=dict(historical_pin=row,current_pin=actual,scope=selected['scope'])
            if event not in reattests:reattests.append(event)
        if actual['path']in table and table[actual['path']]!=actual:raise RuntimeError('conflicting current physical fullpin')
        table[actual['path']]=actual;roles.setdefault(role,set()).add(actual['path']);return actual
    def rows(value,role):
        for row in b.nested(value):add(row,role)
    def metadata(row,role):
        row=add(row,role);origins.append(dict(role=role,pin=row));return read(row)
    oldtargets=[p for p in old['current_protected_full_EOF_pins']if p['path']in[str(x)for x in TARGETS]]
    if len(old['current_protected_full_EOF_pins'])!=5186 or oldtargets!=TARGET_SELECTED_PINS or survey['previous_explicitly_protected_target_pins']!=TARGET_SELECTED_PINS or survey['failure']is not None:raise RuntimeError('explicit previous5186/two historical classifications')
    for row in old['current_protected_full_EOF_pins']:
        if row['path']not in[str(x)for x in TARGETS]:add(row,'previous5184_retained_current_gate_science_Source_and_evidence')
    for group,values in survey['all_current_selected_package_Source_pins'].items():rows(values,'current_selected_Source/'+group)
    hf=metadata(hfpin,'actual_final_v14_HF');cli=metadata(clipin,'actual_final_v14_CLI')
    if hf.get('schema')!='COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V14'or hf.get('prepared_only')is not True or hf.get('actual_pipeline_executed')is not False or not isinstance(hf.get('dependencies'),list)or not hf['dependencies']:raise RuntimeError('real complete unexecuted v14 Source freeze')
    catpin=hf['current_mount_full_identity_catalog_pin']
    if catpin not in hf['dependencies']:raise RuntimeError('v14 must directly bind its exact current catalog PF')
    cat=metadata(catpin,'actual_v14_exact_current_mount_catalog')
    if cat['schema']!='CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG_V1'or cat['status']!='ACTUAL_CURRENT_MOUNT_COMPLETE_PF_CATALOG_CLOSED0_ONLY'or len(cat['rows'])!=3040 or cat['mandatory_failures']!=[]or cat['explicit_device_transition']!=dict(historical=16777234,current=16777229,only_device_field_may_change=True):raise RuntimeError('original exact declared current-mount transition')
    def mapped(old,new,scope):
        old=b.norm(old);new=b.norm(new)
        if new['identity'][0]!=16777229 or (old!=new and(old['path']!=new['path']or old['sha256']!=new['sha256']or old['size_bytes']!=new['size_bytes']or old['identity'][0]!=16777234 or old['identity'][1:]!=new['identity'][1:])):raise RuntimeError('explicit mapping may change only original declared device field')
        key=json.dumps(old,sort_keys=True);value=dict(current_pin=new,scope=scope)
        if key in mapping and mapping[key]['current_pin']!=new:raise RuntimeError('conflicting exact current mappings')
        mapping[key]=value
    for entry in cat['rows']:mapped(entry['historical_pin'],entry['current_pin'],'EXACT_V14_BOUND_CURRENT_CATALOG_ROW')
    for entry in hf.get('additional_exact_current_Source_dependency_reattestations',[]):
        if entry['whole_EOF_and_all_other6_identity_fields_identical']is not True or entry['exact_device_transition']!=[16777234,16777229]or entry['metadata_reattestation_only']is not True:raise RuntimeError('additional mapping must be explicitly declared by real v14 HF')
        mapped(entry['historical_dependency_fullpin'],entry['actual_current_dependency_fullpin'],'EXACT_V14_HF_ADDITIONAL_DECLARED_DEVICE_ONLY_ROW')
    rows([hf['host_source']]+hf['dependencies'],'actual_final_v14_direct_mandatory_host_and_all_dependencies')
    host=Path(hf['host_source']['path'])
    if host.parent!=Path(hfpin['path']).parent or host.name!='run_actual_three_plane_pipeline.py':raise RuntimeError('v14 exact host/freeze namespace')
    argv=cli['argv']
    if argv.count(str(host))!=1 or argv[argv.index('--host-freeze-summary')+1]!=hfpin['path']or argv[argv.index('--host-freeze-sha256')+1]!=hfpin['sha256']or json.loads(argv[argv.index('--host-freeze-seven-id')+1])!=hfpin['identity']:raise RuntimeError('real v14 CLI binds actual HF all7/SHA')
    for label,reviewpin,toolpin in review_inputs:
        review_gate(hfpin,clipin,reviewpin,toolpin);rows([reviewpin,toolpin],label+'_actual_Source_review_and_tool0')
    # Direct declared live fields only; complete_input_pins in closed finite
    # reports are historical fixture evidence, explicitly not a business DAG.
    livefields=('host_source','dependencies','files','Source_pins','fixed_source_files','fixed_current_pins','source_file_pins','complete_source_file_pins','selected_derived_source_pins','original_source_lineage_pins','original_v12_dependencies_as_unchanged_authority_and_provenance','static_input_pins','external_original_input_pins')
    for row in hf['dependencies']:
        if Path(row['path']).suffix=='.json':
            d=read(row)
            if isinstance(d,dict):
                for field in livefields:
                    if field in d:rows(d[field],'v14_explicit_manifest_live_field/'+field)
    current_v13=inventory([V13_OUT])
    if current_v13['symlinks']or len(current_v13['ordinary_file_identities'])!=299:raise RuntimeError('all actual v13 299 outputs retained without symlink')
    for path in sorted(current_v13['ordinary_file_identities']):add(pin(path),'all_v13_299_actual_failure_outputs_Q_MAC_and_empty_final_retained')
    before=inventory();retained=[]
    if before['symlinks']:raise RuntimeError('old closed-run symlink refused')
    for path in sorted(before['ordinary_file_identities']):
        if path not in[str(x)for x in TARGETS]:
            row=add(pin(path),'all_other_v11_v12_results_logs_curves_and_runtime_retained');retained.append(row)
    rows(frozen['Source_pins']+[sfpin,SURVEY_PIN,oldrow,BASE_PIN,frozen['original_resource_factory_pin']]+frozen['immutable_readonly_evidence_pins'],'own_exact_Source_and_actual_readonly_evidence')
    return sorted(table.values(),key=lambda r:r['path']),dict(metadata_origins=origins,roles={k:sorted(v)for k,v in roles.items()},actual_v14_HF_pin=hfpin,actual_v14_CLI_pin=clipin,actual_v14_bound_catalog_pin=catpin,explicit_device_only_current_reattestation_events=reattests,explicit_old_protection_5186_reclassification=dict(previous_count=5186,retained_count=5184,exact_two_reclassified_historical_failed_run_PROJECT_pins=TARGET_SELECTED_PINS,previous_roles=survey['previous_explicit_protection_roles'],not_science_or_current_business_dependency=True),finite_report_bodies_and_curveproof_preserved=True,finite_internal_complete_input_pins_remain_closed_historical_fixture_evidence_not_current_DAG=True,old_exact_fixture_and_PROJECT_GLOBAL_raw_replay_lost_after_release=True,current_v13_complete_before_inventory=current_v13,final_v14_direct_all_dependencies_actual_EOF_verified=True),retained,before

def disjoint(protected):
    paths={r['path']for r in protected};inodes={tuple(r['identity'][:2])for r in protected}
    if len(TARGET_SELECTED_PINS)!=2 or sum(r['size_bytes']for r in TARGET_SELECTED_PINS)!=BYTES:raise RuntimeError('literal exact pair')
    for target,row in zip(TARGETS,TARGET_SELECTED_PINS):
        if row['path']!=str(target)or row['path']in paths or tuple(row['identity'][:2])in inodes or row['identity'][3]!=1 or not stat.S_ISREG(row['identity'][2])or target.lstat().st_uid!=os.getuid():raise RuntimeError('exact own nlink1 target disjoint from final live DAG')
        same(row)
    if TARGET_SELECTED_PINS[0]['identity'][:2]==TARGET_SELECTED_PINS[1]['identity'][:2]:raise RuntimeError('two separate physical owned files required')

def future_out(hfpin):
    hf=read(hfpin);host=same(hf['host_source']);tree=ast.parse(Path(host['path']).read_text());values=[]
    for node in tree.body:
        if isinstance(node,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='OUT'for t in node.targets):
            v=node.value
            if isinstance(v,ast.Call)and isinstance(v.func,ast.Name)and v.func.id=='Path'and len(v.args)==1 and isinstance(v.args[0],ast.Constant)and isinstance(v.args[0].value,str):values.append(Path(v.args[0].value))
    if len(values)!=1 or values[0].parent!=ART or not values[0].name.startswith('axial-material-new-AAA3-streaming-actual-operator-global-BOOT-')or not values[0].name.endswith('-v14'):raise RuntimeError('actual Source literal fresh v14 output path')
    return values[0]

def writer_gate(hfpin,protected):
    if os.path.lexists(future_out(hfpin)):raise RuntimeError('v14 output must remain absent until release complete')
    proc=subprocess.run(['/bin/ps','-axo','pid=,command='],capture_output=True,text=True,timeout=20)
    if proc.returncode!=0 or proc.stderr.strip():raise RuntimeError('real host process metadata unavailable')
    hosts=[str(REC/('aaa_three_plane_streaming_pipeline_source_'+v)/'run_actual_three_plane_pipeline.py')for v in('v11','v12','v13','v14')]
    writers=[r['path']for r in protected if Path(r['path']).suffix=='.py'and any(word in Path(r['path']).name for word in('prepare_','finalize_','freeze_','write_'))]
    for line in proc.stdout.splitlines():
        fields=line.strip().split(None,1)
        if len(fields)!=2 or int(fields[0])==os.getpid():continue
        command=fields[1]
        # The owning terminal may retain its shell while this exact helper
        # runs. Only that parent wrapper is allowed; sibling writers are not.
        if int(fields[0])==os.getppid()and Path(command.split(None,1)[0]).name in('zsh','bash','sh')and str(Path(sys.argv[0]).absolute())in command:continue
        if any(p in command for p in hosts+writers+[str(PKG)])or(str(ART)in command and('/runtime/Dragon'in command or'run_bounded_dragon.py'in command)):raise RuntimeError('active business or selected Source writer')
    for branch in BRANCHES:
        opened=subprocess.run(['/usr/sbin/lsof','-nP','+D',str(branch)],capture_output=True,text=True,timeout=30)
        if opened.returncode not in(0,1)or opened.stdout.strip()or opened.stderr.strip():raise RuntimeError('old namespace open handle or unavailable real lsof')
    guard()

def budget():
    frozen=read(pin(SF));same(frozen['original_resource_factory_pin']);return b.budget()
