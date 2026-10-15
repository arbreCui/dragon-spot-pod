"""Parameterized oldv10 PROJECT release draft; true v13HF+CLI required. No import action."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import shlex

ROOT=Path('/Users/wen/spot');REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011';ART=ROOT/'validation/artifacts';PKG=Path(__file__).absolute().parent
BASE=REC/'storage_release_closed_v7_v8_project_pair_20261013/project_pair_release_common.py'
BASE_PIN=dict(path=str(BASE),sha256='b0a0a3d1f4eacfe8c9b91378b89aff1071a3907c2027a3fec857e160ae6e0b7d',size_bytes=18001,identity=[16777229,49980314,33188,1,18001,1791847138307427020,1791847138307427020])
def _read_base():
    ident=lambda x:[x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
    before=BASE.lstat()
    if not stat.S_ISREG(before.st_mode) or ident(before)!=BASE_PIN['identity']:raise RuntimeError('exact original readonly helpers all7ID')
    fd=os.open(BASE,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        if ident(os.fstat(fd))!=ident(before):raise RuntimeError('helper changed at Source open')
        raw=b''
        while True:
            block=os.read(fd,65536)
            if not block:break
            raw+=block
        if ident(os.fstat(fd))!=ident(before):raise RuntimeError('helper changed at Source EOF')
    finally:os.close(fd)
    if ident(BASE.lstat())!=ident(before) or len(raw)!=18001 or hashlib.sha256(raw).hexdigest()!=BASE_PIN['sha256']:raise RuntimeError('actual complete readonly Source helper')
    spec=importlib.util.spec_from_file_location('original_readonly_single_candidate_helpers',BASE);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
b=_read_base();pin=b.pin;same=b.same;read=b.read;identity=b.identity;guard=b.guard;write_new=b.write_new;update_owned=b.update_owned
BRANCH=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v10'
TARGET=BRANCH/'AAA/projected_boot.xsm';BYTES=749355952
TARGET_SELECTED_PIN={'path': '/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v10/AAA/projected_boot.xsm', 'sha256': 'ea56e0e58889469c81e1519713ca0df93a3ebb5f2b1a1fbd2e20b5d8be72833a', 'size_bytes': 749355952, 'identity': [16777229, 50015491, 33152, 1, 749355952, 1791871337358403803, 1791871337358403803]}
V13_HF=REC/'aaa_three_plane_streaming_pipeline_source_v13/COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json'
V13_OUT=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261013-v13'
FUTURE_V13_HF_PIN=None;FUTURE_V13_CLI_PIN=None
SOURCE_NAMES=('single_project_release_common.py','prepare_single_project_after_actual_v13_HF.py','verify_or_execute_single_project.py')
SF=PKG/'COMPLETE_SINGLE_OLD_V10_PROJECT_RELEASE_SOURCE_FREEZE.json'
FINAL=PKG/'EXACT_SINGLE_OLD_V10_PRIVATE_PROJECT_RELEASE_MANIFEST.json'
RECEIPTS=REC/'storage_release_old_v10_single_PROJECT_actual_receipts_20261013'
SURVEY_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/readonly_old_v10_private_PROJECT_candidate_survey_20261013/FULL_CURRENT_GATE_UNION_AND_EXACT_OLD_V10_CANDIDATE_READONLY_REVIEW.json', 'sha256': '200e8824fdf3a7d0e06e2410e6edd8f680459d936d34defa71cfda88bdd03c5b', 'size_bytes': 4390616, 'identity': [16777229, 50036080, 33188, 1, 4390616, 1791884498865465885, 1791884498865465885]}

def receipt_pin_no_admission(p):
    # Bounded failure evidence only; never grants business/resource admission.
    p=Path(p);before=p.lstat()
    if not stat.S_ISREG(before.st_mode)or before.st_nlink!=1 or before.st_uid!=os.getuid()or before.st_size>64*2**20:raise RuntimeError('bounded exclusive own receipt only')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb')as f:
        if identity(os.fstat(f.fileno()))!=identity(before):raise RuntimeError('receipt opened7ID')
        digest=hashlib.file_digest(f,'sha256').hexdigest()
        if identity(os.fstat(f.fileno()))!=identity(before):raise RuntimeError('receipt EOF7ID')
    if identity(p.lstat())!=identity(before):raise RuntimeError('receipt path7ID')
    return dict(path=str(p),sha256=digest,size_bytes=before.st_size,identity=identity(before))

def update_owned(p,v,old):
    # A failed original cap still gets truthful same-FD failure evidence. This
    # never resumes business or treats the failed cap as PASS.
    if str(v.get('status','')).startswith('STOPPED_'):
        if receipt_pin_no_admission(p)!=old:raise RuntimeError('old owned failure receipt changed')
    else:same(old)
    fd=os.open(p,os.O_RDWR|os.O_NOFOLLOW)
    with os.fdopen(fd,'r+',encoding='utf-8')as f:
        before=identity(os.fstat(f.fileno()))
        if before!=old['identity']or before[3]!=1 or Path(p).lstat().st_uid!=os.getuid():raise RuntimeError('same owned report FD/UID before write')
        f.seek(0);f.truncate(0);json.dump(v,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
        after=identity(os.fstat(f.fileno()));path_id=identity(Path(p).lstat())
        if after!=path_id or after[:4]!=before[:4]:raise RuntimeError('same report FD/path must retain inode/mode/nlink')
    return receipt_pin_no_admission(p)


def external(path,sha,seven):
    p=pin(path)
    if p['sha256']!=sha or p['identity']!=json.loads(seven):raise RuntimeError('external exact SHA/all7ID selection '+str(path))
    return p

def source_gate(selected):
    if selected['path']!=str(SF):raise RuntimeError('exact final own Source-only freeze required; draft cannot execute')
    f=read(selected)
    if f['schema']!='COMPLETE_SINGLE_OLD_V10_PROJECT_PARAMETERIZED_RELEASE_SOURCE_FREEZE_V1' or f['deletion_executed']is not False or f['v13_business_qualification_claimed']is not False or f['future_v13_host_freeze_pin']is not None or f['future_v13_CLI_pin']is not None or [p['path']for p in f['Source_pins']]!=[str(PKG/n)for n in SOURCE_NAMES]or f['original_readonly_helper_pin']!=BASE_PIN or f['actual_readonly_candidate_survey_pin']!=SURVEY_PIN:raise RuntimeError('strict complete actual Source freeze, no future prefill')
    for p in f['Source_pins']+[BASE_PIN,SURVEY_PIN,f['original_resource_factory_pin']]+f['actual_current_v13_source_preparation_pins']:same(p)
    if f['original_resource_factory_pin']['path']!=str(b.FACTORY)or f['original_caps']!=dict(SELF_mib=512,whole_seconds=1800,stage_seconds=600,threads=1,children_at_once=1,fresh_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20):raise RuntimeError('original complete resources preserved')
    return f


def old_closed_proofs():
    summarypin=pin(BRANCH/'Root_actual_three_plane_engineering_summary.json');d=read(summarypin)
    toolpin=pin(REC/'ACTUAL_PIPELINE_V10_TRUE_TOOL_RETURNS_20261013.json');t=read(toolpin)
    rawpin=pin(BRANCH/'Root_actual_complete_execution_record_before_final_publication.json');raw=read(rawpin)
    if d['schema']!='ACTUAL_INDEPENDENT_AAA3_INITIAL_GLOBAL_PROJECT_BOOT_ENGINEERING_ROOT_V1' or d['status']!='FAILED_UNQUALIFIED_NO_RETRY' or d['failure']!='RuntimeError: original SELF 512MiB cap' or d['after_check_error']!='RuntimeError: original SELF 512MiB cap' or d['engineering_three_plane_closed0']is not False or d['actual_terminal']is not None or len(d['records'])!=46 or d['output_pins']!=[]or t['observed_closed']is not True or type(t['original_integer_exit_code'])is not int or t['original_integer_exit_code']!=1 or t['terminal']['exit_code']!=1:raise RuntimeError('oldv10 genuine failed aggregate Root closed1 required')
    if raw['records']!=d['records']or TARGET_SELECTED_PIN not in raw['owned_runtime_pins']:raise RuntimeError('target genuine original prepublication owned fullpin')
    rows={r['label']:r for r in d['records']}
    if rows['AAA/global_positive']['status']!='PASS'or rows['AAA/project_positive']['status']!='PASS'or d['records'][-1]['label']!='AAA/pair_case_rank_mismatch':raise RuntimeError('oldv10 GLOBAL PROJECT single PASS and true failed suffix preserved')
    closures=[]
    for r in d['records']:
        wp=pin(BRANCH/(r['label']+'.watchdog.json'));w=read(wp);lp=pin(BRANCH/(r['label']+'.log'))
        expected=0 if r['status']=='PASS'else 1
        if r['status']not in('PASS','FAILED')or type(w['returncode'])is not int or w['returncode']!=expected or w['own_child_only']is not True or w['liveness_group_cleanup']is not True or w['command']!=r['command']or w['limit_failure']is not None or w['rss_cap_mib']!=512 or not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 or not 0<=w['sampled_peak_rss_mib']<512:raise RuntimeError('all46 actual oldv10 children genuinely closed at original caps')
        if r['status']=='PASS'and lp['sha256']!=r['log_sha256']:raise RuntimeError('successful original oldv10 stage log bytes changed')
        closures.append(dict(label=r['label'],status=r['status'],watchdog_pin=wp,log_pin=lp,actual_returncode=w['returncode']))
    return dict(old_v10_summary_pin=summarypin,old_v10_true_Root_exit1_tool_pin=toolpin,old_v10_complete_prepublication_raw_pin=rawpin,all46_actual_v10_child_closures=closures,GLOBAL_PROJECT_individual_PASS_preserved=True,old_BOOT_unqualified=True,old_full_PROJECT_GLOBAL_tree_raw_replay_unavailable_after_release=True,old_math_or_producer_invalidity_not_inferred=True)


def current_protection(hfpin,clipin):
    # Re-prove every observed physical gate before extending to actual new v13.
    # The survey's immutable fullpins are starting evidence, not future authority.
    survey=read(SURVEY_PIN);table={};roles={};origins=[];events=[]
    def add(row,role):
        old=b.norm(row);new=pin(old['path'])
        if new!=old:
            if old['sha256']!=new['sha256']or old['size_bytes']!=new['size_bytes']or old['identity'][0]!=16777234 or new['identity'][0]!=16777229 or old['identity'][1:]!=new['identity'][1:]:raise RuntimeError('only explicit historical device change allowed')
            events.append(dict(historical_pin=old,current_pin=new,only_device_changed=True))
        if new['path']in table and table[new['path']]!=new:raise RuntimeError('inconsistent current mandatory fullpin')
        table[new['path']]=new;roles.setdefault(role,set()).add(new['path']);return new
    def rows(value,role):
        for p in b.nested(value):add(p,role)
    def metadata(row,role):
        row=add(row,role);d=read(row);origins.append(dict(role=role,pin=row));return d
    if survey['candidate_current_full_EOF_pin']!=TARGET_SELECTED_PIN or survey['target_path_and_inode_disjoint_from_complete_selected_mandatory_union']is not True or survey['direct_typed_TARGET_pin_occurrences_in_all_selected_Source_JSON']!=[]:raise RuntimeError('real readonly oldv10 observed candidate authority')
    for row in survey['all_current_protected_EOF_pins']:add(row,'previous_selected_gate_union_reproved_current')
    # Mandatory true external v13 args. No Source constant is filled with their
    # future values; the final manifest binds them only after actual preparation.
    hf=metadata(hfpin,'actual_final_v13_HF');cli=metadata(clipin,'actual_final_v13_exact_CLI')
    if hfpin['path']!=str(V13_HF)or Path(hf['host_source']['path']).parent!=V13_HF.parent or hf.get('actual_pipeline_executed')is not False or hf.get('prepared_only')is not True or not isinstance(hf.get('dependencies'),list)or not hf['dependencies']:raise RuntimeError('actual final unexecuted complete v13 Host Source freeze required')
    rows([hf['host_source']]+hf['dependencies'],'actual_final_v13_direct_mandatory_dependencies')
    rows(hf.get('selected_serializer_bundle_pin'),'actual_v13_serializer_bundle_authority')
    for name in('ROOT_V13_COMPLETE_SOURCE_INTEGRATION_READONLY_REVIEW_20261013.json','ROOT_ACTUAL_V13_SOURCE_PREPARATION_TRUE_TOOL_RETURN_20261013.json'):
        add(pin(REC/name),'actual_Root_v13_Source_preparation_and_review')
    bundle=metadata(hf['selected_serializer_bundle_pin'],'actual_v13_complete_serializer_bundle')
    rows(bundle['selected_derived_source_pins'],'actual_v13_bundle_declared_gate/'+'selected_derived_source_pins')
    rows(bundle['original_source_lineage_pins'],'actual_v13_bundle_declared_gate/'+'original_source_lineage_pins')
    rows(bundle['complete_byte_inverse_pin'],'actual_v13_bundle_declared_gate/'+'complete_byte_inverse_pin')
    rows(bundle['original_v12_host_source_freeze_pin'],'actual_v13_bundle_declared_gate/'+'original_v12_host_source_freeze_pin')
    rows(bundle['closed_actual_finite_report_pins'],'actual_v13_bundle_declared_gate/'+'closed_actual_finite_report_pins')
    rows(bundle['actual_true_tool_returns_pin'],'actual_v13_bundle_declared_gate/'+'actual_true_tool_returns_pin')
    rows(bundle['actual_finite_argv_pin'],'actual_v13_bundle_declared_gate/'+'actual_finite_argv_pin')
    rows(bundle['finite_fixture_source_and_first_failure_pins'],'actual_v13_bundle_declared_gate/'+'finite_fixture_source_and_first_failure_pins')
    rows(bundle['historical_v12_failure_and_root_source_review_pins'],'actual_v13_bundle_declared_gate/'+'historical_v12_failure_and_root_source_review_pins')
    rows(bundle['final_report_pin'],'actual_v13_bundle_declared_gate/'+'final_report_pin')
    rootreview=metadata(pin(REC/'ROOT_V13_COMPLETE_SOURCE_INTEGRATION_READONLY_REVIEW_20261013.json'),'Root_actual_v13_review_semantics')
    roottruth=metadata(pin(REC/'ROOT_ACTUAL_V13_SOURCE_PREPARATION_TRUE_TOOL_RETURN_20261013.json'),'Root_actual_v13_prepare_semantics')
    if rootreview.get('host_freeze_pin')!=hfpin or rootreview.get('CLI_pin')!=clipin or rootreview.get('business_executed')is not False or roottruth.get('observed_closed')is not True or roottruth.get('original_integer_exit_code')!=0 or roottruth.get('genuine_actual_tool_return',{}).get('exit_code')!=0 or roottruth.get('numerical_business_executed')is not False:raise RuntimeError('Root true Source preparation/review bound to exact real v13')
    prepared=json.loads(roottruth['genuine_actual_tool_return']['output'])
    if prepared.get('host_freeze_pin')!=hfpin or prepared.get('CLI_pin')!=clipin:raise RuntimeError('Root exact actual Sourceprep return HF/CLI mismatch')
    peer=metadata(pin(REC/'independent_v13_final_serializer_integration_source_review_20261013/REVIEW.json'),'independent_true_v13_final_integration_review')
    peertruth=metadata(pin(REC/'independent_v13_final_serializer_integration_source_review_20261013/TRUE_TOOL_RETURNS.json'),'independent_true_v13_final_integration_tools')
    if peer.get('host_freeze_pin')!=hfpin or peer.get('CLI_pin')!=clipin or peer.get('failure')is not None or peer.get('total_v13_dependency_rows')!=354 or peer.get('candidate_import_compiler_or_child_started')is not False or peertruth.get('observed_closed')is not True or peertruth.get('original_integer_exit_code')!=0 or peertruth.get('actual_review_return',{}).get('exit_code')!=0:raise RuntimeError('independent actual closed Source integration differs')
    argv=cli['argv'];host=hf['host_source']['path']
    if argv.count(host)!=1 or argv[argv.index('--host-freeze-summary')+1]!=hfpin['path']or argv[argv.index('--host-freeze-sha256')+1]!=hfpin['sha256']or json.loads(argv[argv.index('--host-freeze-seven-id')+1])!=hfpin['identity']:raise RuntimeError('actual complete v13 CLI owns exact mandatory HF fullpin')
    for field in('selected_actual_build70_report','selected_original_actual69_handle_lifetime_report','selected_original_actual69_v4_report'):
        if field in hf:
            d=metadata(hf[field],'actual_v13_selected_gate/'+field)
            rows(d.get('fixed_current_pins',[]),'actual_v13_prerequisite_fixed');rows(d.get('output_pins',[]),'actual_v13_prerequisite_outputs')
    for path in sorted(V13_HF.parent.rglob('*')):
        if path.is_file():add(pin(path),'actual_frozen_v13_complete_Source_files')
    # Any new support/Common/serializer bundle must be directly bound by the
    # final HF; its owning manifests are explicit Source-only mandatory inputs.
    for row in hf['dependencies']:
        if Path(row['path']).suffix=='.json':
            d=read(row)
            if isinstance(d,dict)and (d.get('source_only')is True or row==hf.get('selected_serializer_bundle_pin')):
                for field in('host_source','dependencies','files','Source_pins','complete_source_file_pins','fixed_source_files','fixed_current_pins','bundle_file_pins','source_file_pins','original_source_pins','original_sources','original_pins','complete_source_pins','external_original_input_pins'):
                    if field in d:rows(d[field],'actual_v13_Source_manifest_direct_gate/'+field)
    for version in('v11','v12'):
        out=ART/('axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-'+version)
        add(pin(out/'AAA/projected_boot.xsm'),'must_keep_'+version+'_PROJECT')
        if version=='v12':
            for path in sorted(out.rglob('*')):
                if path.is_file():add(pin(path),'all_v12_curveproof_and_outputs_protected')
    proof=old_closed_proofs()
    for field in('old_v10_summary_pin','old_v10_true_Root_exit1_tool_pin','old_v10_complete_prepublication_raw_pin'):add(proof[field],'actual_oldv10_closed_failure_documents')
    retained=[pin(p)for p in sorted(BRANCH.rglob('*'))if p.is_file()and p!=TARGET]
    if len(retained)!=267:raise RuntimeError('all267 other oldv10 ordinary files must remain')
    for row in retained:add(row,'all267_other_oldv10_files_preserved')
    for row in[BASE_PIN,SURVEY_PIN,pin(b.FACTORY)]:add(row,'immutable_readonly_original_helpers_and_evidence')
    return sorted(table.values(),key=lambda p:p['path']),dict(selected_live_metadata_origins=origins,roles={k:sorted(v)for k,v in roles.items()},explicit_only_device_current_reattestations=events,actual_v13_HF_pin=hfpin,actual_v13_CLI_pin=clipin,real_old_closed_history_proofs=proof,historical_closed_output_pins_not_promoted_to_current_DAG=True,new_v13_direct_gate_union_reproved=True),retained

def owned_disjoint(row,protected):
    if row!=TARGET_SELECTED_PIN or row['identity'][3]!=1 or not stat.S_ISREG(row['identity'][2]) or TARGET.lstat().st_uid!=os.getuid():raise RuntimeError('one exact ordinary current-user-owned candidate only')
    paths={p['path'] for p in protected};inodes={tuple(p['identity'][:2]) for p in protected}
    if row['path'] in paths or tuple(row['identity'][:2]) in inodes:raise RuntimeError('candidate current live/protected dependency')
    same(row)

def writer_gate():
    old_closed_proofs()
    if os.path.lexists(V13_OUT):raise RuntimeError('cleanup must precede v13 business output namespace, no concurrent delta')
    proc=subprocess.run(['/bin/ps','-axo','pid=,command='],text=True,capture_output=True,timeout=20)
    if proc.returncode!=0:raise RuntimeError('real current host metadata unavailable')
    hostpaths=[str(REC/('aaa_three_plane_streaming_pipeline_source_'+v)/'run_actual_three_plane_pipeline.py')for v in('v10','v11','v12','v13')]
    for line in proc.stdout.splitlines():
        fields=line.strip().split(None,1)
        if len(fields)!=2 or int(fields[0])==os.getpid():continue
        command=fields[1]
        if any(p in command for p in hostpaths)or(str(ART)in command and('/runtime/Dragon'in command or'run_bounded_dragon.py'in command)):raise RuntimeError('active original business writer; no release')
    opened=subprocess.run(['/usr/sbin/lsof','-nP','+D',str(BRANCH)],text=True,capture_output=True,timeout=30)
    if opened.returncode not in(0,1)or opened.stdout.strip()or opened.stderr.strip():raise RuntimeError('oldv10 namespace has open handle/writer or lsof unavailable')

def inventory():
    files={};links={};dirs={};stack=[BRANCH]
    while stack:
        p=stack.pop();st=p.lstat()
        if not stat.S_ISDIR(st.st_mode):raise RuntimeError('ordinary oldv10 directory')
        dirs[str(p)]=identity(st);fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:
            with os.scandir(fd) as entries:
                for e in entries:
                    q=p/e.name;st=e.stat(follow_symlinks=False)
                    if stat.S_ISDIR(st.st_mode):stack.append(q)
                    elif stat.S_ISREG(st.st_mode):files[str(q)]=identity(st)
                    elif stat.S_ISLNK(st.st_mode):links[str(q)]=dict(identity=identity(st),target=os.readlink(q))
                    else:raise RuntimeError('special oldv10 entry')
        finally:os.close(fd)
        guard()
    return dict(ordinary_file_identities=files,symlinks=links,directory_identities=dirs)

def budget():
    f=read(pin(SF));same(f['original_resource_factory_pin'])
    return b.budget()
