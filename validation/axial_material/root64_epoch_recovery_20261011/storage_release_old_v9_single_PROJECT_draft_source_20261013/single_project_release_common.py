"""Exact oldv9 private PROJECT only; real frozen v11 inputs required. No action on import."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess

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
BRANCH=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v9'
TARGET=BRANCH/'AAA/projected_boot.xsm';BYTES=749355952
TARGET_SELECTED_PIN=dict(path=str(TARGET),sha256='ea56e0e58889469c81e1519713ca0df93a3ebb5f2b1a1fbd2e20b5d8be72833a',size_bytes=BYTES,identity=[16777229,50012374,33152,1,BYTES,1791869646152430244,1791869646152430244])
V11_DIR=REC/'aaa_three_plane_streaming_pipeline_source_v11';V11_HF=V11_DIR/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json';V11_OUT=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v11'
V11_HF_SELECTED_PIN=dict(path=str(V11_HF),sha256='2597f653ebb8d24e454d0f129efb1db1f623073e4524b9ce0b560d54ade56736',size_bytes=163351,identity=[16777229,50017634,33188,1,163351,1791873144732798330,1791873144732798330])
V11_CLI_SELECTED_PIN=dict(path=str(REC/'ROOT_EXACT_ACTUAL_PIPELINE_V11_ARGV_20261013.json'),sha256='5a00c302d82b76ff7cb8776aa2bfc7db5aa126c9c4845e495f74ce5c776507d1',size_bytes=13380,identity=[16777229,50017635,33188,1,13380,1791873144733698750,1791873144733698750])
SOURCE_NAMES=('single_project_release_common.py','prepare_single_project_after_actual_v11_HF.py','verify_or_execute_single_project.py')
SF=PKG/'COMPLETE_SINGLE_OLD_V9_PROJECT_RELEASE_SOURCE_FREEZE.json'
FINAL=PKG/'EXACT_SINGLE_OLD_V9_PRIVATE_PROJECT_RELEASE_MANIFEST.json'
SURVEY_PIN=dict(path=str(REC/'readonly_old_v9_private_PROJECT_current_DAG_survey_20261013/SINGLE_V9_PROJECT_CURRENT_DAG_AND_BUDGET_READONLY_REVIEW.json'),sha256='dee6671f155807ce312f37d025c0f7db2ca4a0bdf1fd9ce733425953de74e347',size_bytes=3531818,identity=[16777229,50016782,33188,1,3531818,1791872302629510161,1791872302629510161])

def external(path,sha,seven):
    p=pin(path)
    if p['sha256']!=sha or p['identity']!=json.loads(seven):raise RuntimeError('external exact SHA/all7ID selection '+str(path))
    return p

def source_gate(selected):
    if selected['path']!=str(SF):raise RuntimeError('exact future complete single Source freeze')
    f=read(selected)
    if f['schema']!='COMPLETE_SINGLE_OLD_V9_PROJECT_RELEASE_SOURCE_FREEZE_V1' or f['deletion_executed'] is not False or f['v11_business_qualification_claimed'] is not False or [p['path'] for p in f['Source_pins']]!=[str(PKG/n) for n in SOURCE_NAMES] or f['original_readonly_helper_pin']!=BASE_PIN or f['actual_readonly_candidate_survey_pin']!=SURVEY_PIN or f['selected_actual_v11_HF_pin']!=V11_HF_SELECTED_PIN or f['selected_actual_v11_CLI_pin']!=V11_CLI_SELECTED_PIN:raise RuntimeError('strict complete current Source, never draft')
    if f['original_resource_factory_pin']['path']!=str(b.FACTORY):raise RuntimeError('exact original resource factory Source role')
    for p in f['Source_pins']+[BASE_PIN,SURVEY_PIN,V11_HF_SELECTED_PIN,V11_CLI_SELECTED_PIN,f['original_resource_factory_pin']]:same(p)
    if f['original_caps']!=dict(SELF_mib=512,whole_seconds=1800,stage_seconds=600,threads=1,children_at_once=1,fresh_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20):raise RuntimeError('original caps unchanged')
    return f

def old_closed_proofs():
    summarypin=pin(BRANCH/'Root_actual_three_plane_engineering_summary.json');d=read(summarypin)
    toolpin=pin(REC/'ACTUAL_PIPELINE_V9_AFTER_EXACT_TWO_RELEASE_TRUE_TOOL_RETURNS_20261013.json');t=read(toolpin)
    if d['schema']!='ACTUAL_INDEPENDENT_AAA3_INITIAL_GLOBAL_PROJECT_BOOT_ENGINEERING_ROOT_V1' or d['status']!='FAILED_UNQUALIFIED_NO_RETRY' or d['engineering_three_plane_closed0'] is not False or d['after_check_error'] is not None or len(d['records'])!=42 or t['observed_closed'] is not True or t['original_integer_exit_code']!=1 or t['terminal']['exit_code']!=1:raise RuntimeError('true oldv9 failed aggregate Root closure')
    rows={r['label']:r for r in d['records']}
    if rows['AAA/global_positive']['status']!='PASS' or rows['AAA/project_positive']['status']!='PASS' or d['records'][-1]['label']!='AAA/view_memory_output':raise RuntimeError('preserve individual GLOBAL PROJECT PASS, failedBOOT scope')
    if next(p for p in d['output_pins'] if p['path']==str(TARGET))!=TARGET_SELECTED_PIN:raise RuntimeError('exact original output authority')
    closures=[]
    for r in d['records']:
        wp=pin(BRANCH/(r['label']+'.watchdog.json'));w=read(wp);lp=pin(BRANCH/(r['label']+'.log'))
        expected=0 if r['status']=='PASS' else (-5 if r['label']=='AAA/view_memory_output' else 1)
        if r['status'] not in ('PASS','FAILED') or type(w['returncode']) is not int or w['returncode']!=expected or w['own_child_only'] is not True or w['liveness_group_cleanup'] is not True or w['command']!=r['command'] or w['limit_failure'] is not None or w['rss_cap_mib']!=512 or not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 or not 0<=w['sampled_peak_rss_mib']<512:raise RuntimeError('every oldv9 actual owned child closed with original return code and caps')
        if r['status']=='PASS' and lp['sha256']!=r['log_sha256']:raise RuntimeError('genuine successful oldv9 stage log unchanged')
        closures.append(dict(label=r['label'],status=r['status'],watchdog_pin=wp,log_pin=lp,actual_returncode=w['returncode']))
    v10out=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v10'
    sp10=pin(v10out/'Root_actual_three_plane_engineering_summary.json');d10=read(sp10);tp10=pin(REC/'ACTUAL_PIPELINE_V10_TRUE_TOOL_RETURNS_20261013.json');t10=read(tp10)
    if t10['observed_closed'] is not True or t10['original_integer_exit_code']!=1 or t10['terminal']['exit_code']!=1 or d10['schema']!='ACTUAL_INDEPENDENT_AAA3_INITIAL_GLOBAL_PROJECT_BOOT_ENGINEERING_ROOT_V1' or d10['status']!='FAILED_UNQUALIFIED_NO_RETRY' or d10['failure']!='RuntimeError: original SELF 512MiB cap' or d10['after_check_error']!='RuntimeError: original SELF 512MiB cap' or len(d10['records'])!=46 or d10['engineering_three_plane_closed0'] is not False or d10['output_pins']!=[]:raise RuntimeError('actual v10 failed Root closure before cleanup')
    return dict(old_v9_summary_pin=summarypin,old_v9_true_Root_exit1_tool_pin=toolpin,all42_actual_v9_child_closures=closures,closed_v10_summary_pin=sp10,closed_v10_Root_tool_pin=tp10,GLOBAL_PROJECT_individual_PASS_preserved=True,old_BOOT_unqualified=True,old_full_PROJECT_GLOBAL_tree_raw_replay_unavailable_after_release=True,old_math_or_producer_invalidity_not_inferred=True)

def current_protection(hfpin):
    table={};roles={};origins=[];events=[]
    def add(row,role):
        old=b.norm(row);new=pin(old['path'])
        if new!=old:
            if old['sha256']!=new['sha256'] or old['size_bytes']!=new['size_bytes'] or old['identity'][0]!=16777234 or new['identity'][0]!=16777229 or old['identity'][1:]!=new['identity'][1:]:raise RuntimeError('current dependency changed beyond exact device-only transition')
            events.append(dict(historical_pin=old,current_pin=new,only_device_changed=True))
        if new['path'] in table and table[new['path']]!=new:raise RuntimeError('ambiguous live fullpin')
        table[new['path']]=new;roles.setdefault(role,set()).add(new['path']);return new
    def meta(path,role):
        p=add(pin(path),role);d=read(p);origins.append(dict(role=role,pin=p));return d
    def rows(value,role):
        for row in b.nested(value):add(row,role)
    def source_dir(path,role,declared_inputs=True):
        b.ancestors(path)
        if not stat.S_ISDIR(path.lstat().st_mode):raise RuntimeError('actual completed Source directory required '+str(path))
        entries=sorted(str(p) for p in path.rglob('*') if p.is_file())
        for name in entries:
            p=add(pin(name),role)
            if declared_inputs and Path(name).suffix=='.json':rows(read(p),role+'_declared_Source_input_pins')
        if entries!=sorted(str(p) for p in path.rglob('*') if p.is_file()):raise RuntimeError('current Source still being written')
    cat=meta(REC/'current_mount_identity_reattestation_20261012/CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG.json','current_catalog')
    if len(cat['rows'])!=3040:raise RuntimeError('all3040 catalog rows')
    rows([r['current_pin'] for r in cat['rows']],'all3040_catalog_current_rows')
    common=meta(REC/'current_mount_full_identity_common_source_v1/CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json','current_Common')
    if len(common['fixed_current_pins'])!=2012:raise RuntimeError('all2012 Common rows')
    rows(common['fixed_current_pins'],'all2012_Common_current_rows')
    science=meta(REC/'saved_full370_terminal_audit_host_source_v2/CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json','saved_science_current_BIND')
    if len(science['fixed_current_pins'])!=3315 or len(science['science_original_input_pins'])!=1129:raise RuntimeError('science3315/1129')
    rows(science['fixed_current_pins'],'saved_science3315');rows(science['science_original_input_pins'],'science1129_original_inputs')
    for version in ('v10','v11'):
        path=REC/('aaa_three_plane_streaming_pipeline_source_'+version)/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json'
        p=add(pin(path),'current_'+version+'_HF')
        if version=='v11' and (p!=hfpin or p!=V11_HF_SELECTED_PIN):raise RuntimeError('externally selected actual current v11 HF mismatch')
        hf=read(p)
        if Path(hf['host_source']['path']).parent!=path.parent or len(hf['dependencies'])!={'v10':278,'v11':308}[version] or hf['actual_pipeline_executed'] is not False or hf['prepared_only'] is not True:raise RuntimeError('actual frozen current pipeline complete HF')
        rows([hf['host_source']]+hf['dependencies'],'current_'+version+'_actual_fixed_HF_dependencies_and_host')
        build=read(add(hf['selected_actual_build70_report'],'current_actual70_report'))
        rows(build['fixed_current_pins'],'current70_actual_fixed');rows(build['output_pins'],'current70_actual_outputs')
        # The HF declares physical inputs directly. Preserve every current
        # Source/proof byte without recursively promoting closed output arrays.
        source_dir(path.parent,'complete_'+version+'_Source_and_proof_files',declared_inputs=False)
    add(V11_CLI_SELECTED_PIN,'selected_actual_v11_exact_CLI')
    source_dir(REC/'aaa_pipeline_v11_author_finite_source_review_20261013','completed_actual_v11_author_Source_only_review',declared_inputs=False)
    for name in ('ROOT_FINITE_PIPELINE_V11_CLOSED_METADATA_LIFETIME_HOST_REVIEW_20261013.json','ROOT_PIPELINE_V11_SOURCE_REVIEW_TRUE_TOOL_RETURN_20261013.json'):
        add(pin(REC/name),'completed_actual_Root_v11_Source_only_review')
    if not (REC/'current_formal_material_authority_exact_cache70_source_v6').is_dir():raise RuntimeError('actual complete materialv6 Source required')
    for path in sorted(p for p in REC.glob('current_formal_material_authority_exact_cache70_source_v*') if p.is_dir()):source_dir(path,'all_current_material_Source_and_actual_inputs')
    source_dir(REC/'material_exact_cache70_v6_author_finite_source_review_20261013','completed_actual_materialv6_author_Source_only_review',declared_inputs=False)
    source_dir(REC/'current_eleven_saved_gendf_current_mount_host_source_v4','current_GENDF_v4_Source_and_actual_inputs')
    source_dir(REC/'reaction_genDF_current_mount_stream_source_v2','current_GENDF_parser_v2_Source_and_actual_inputs')
    ref=REC/'full370_unreduced_eigen_reference_source_v2'
    for p in sorted(ref.iterdir()):add(pin(p),'current_independent_reference_complete_Source')
    plan=meta(ref/'CURRENT_FORMAL_FULL370_INPUT_PLAN_SOURCE_ONLY.json','current_reference_actual_input_plan')
    rows([plan[k] for k in ('protected_formal_and_producer_plan_pin','current_case_spec_pin','current_prepared_pin','current_axial_track_pin','additional_current_input_pins')],'current_reference_actual_fixed_inputs')
    formal=read(add(plan['protected_formal_and_producer_plan_pin'],'formal_and_producer_input_plan'));rows(formal['formal_inputs'],'formal_original_live_inputs')
    for row in formal['producers']:rows([row[k] for k in ('report','archive','radial_binary_track')],'all3_actual_native_producer_inputs')
    # Closed summaries themselves may be current provenance. Never recurse
    # their historical output_pins into the mandatory physical input table.
    proof=old_closed_proofs()
    for field in ('old_v9_summary_pin','old_v9_true_Root_exit1_tool_pin','closed_v10_summary_pin','closed_v10_Root_tool_pin'):add(proof[field],'selected_real_closed_history_documents')
    for row in proof['all42_actual_v9_child_closures']:add(row['watchdog_pin'],'old_v9_closed_watchdogs');add(row['log_pin'],'old_v9_retained_logs')
    v10out=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v10'
    for path in sorted(v10out.rglob('*')):
        if path.is_file():add(pin(path),'all_closed_v10_actual_files_retained_history_not_new_input_authority')
    add(BASE_PIN,'original_readonly_helpers_Source');add(SURVEY_PIN,'actual_readonly_candidate_survey');add(pin(b.FACTORY),'original_resource_factory_Source')
    # Preserve all242 remaining v9 files; target alone is excluded from this
    # live/protection union with its exact raw-replay cost explicitly recorded.
    retained=[pin(p) for p in sorted(BRANCH.rglob('*')) if p.is_file() and p!=TARGET]
    if len(retained)!=242:raise RuntimeError('exact all242 other oldv9 ordinary files retained')
    for row in retained:add(row,'all242_remaining_oldv9_files_preserved')
    return sorted(table.values(),key=lambda p:p['path']),dict(selected_live_metadata_origins=origins,roles={k:sorted(v) for k,v in roles.items()},explicit_only_device_current_reattestations=events,actual_v11_HF_pin=hfpin,real_old_closed_history_proofs=proof,historical_closed_output_pins_not_promoted_to_current_DAG=True),retained

def owned_disjoint(row,protected):
    if row!=TARGET_SELECTED_PIN or row['identity'][3]!=1 or not stat.S_ISREG(row['identity'][2]) or TARGET.lstat().st_uid!=os.getuid():raise RuntimeError('one exact ordinary current-user-owned candidate only')
    paths={p['path'] for p in protected};inodes={tuple(p['identity'][:2]) for p in protected}
    if row['path'] in paths or tuple(row['identity'][:2]) in inodes:raise RuntimeError('candidate current live/protected dependency')
    same(row)

def writer_gate():
    old_closed_proofs()
    if os.path.lexists(V11_OUT):raise RuntimeError('cleanup must precede v11 ART business namespace creation, no concurrent delta')
    proc=subprocess.run(['/bin/ps','-axo','pid=,command='],text=True,capture_output=True,timeout=20)
    if proc.returncode!=0:raise RuntimeError('current own business process metadata unavailable')
    hostpaths=[str(REC/('aaa_three_plane_streaming_pipeline_source_'+v)/'run_actual_three_plane_pipeline.py') for v in ('v9','v10','v11')]
    for line in proc.stdout.splitlines():
        fields=line.strip().split(None,1)
        if len(fields)!=2 or int(fields[0])==os.getpid():continue
        command=fields[1]
        if any(p in command for p in hostpaths) or (str(ART) in command and ('/runtime/Dragon' in command or 'run_bounded_dragon.py' in command)):raise RuntimeError('active original numerical writer; postpone single cleanup')

def inventory():
    files={};links={};dirs={};stack=[BRANCH]
    while stack:
        p=stack.pop();st=p.lstat()
        if not stat.S_ISDIR(st.st_mode):raise RuntimeError('ordinary oldv9 directory')
        dirs[str(p)]=identity(st);fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:
            with os.scandir(fd) as entries:
                for e in entries:
                    q=p/e.name;st=e.stat(follow_symlinks=False)
                    if stat.S_ISDIR(st.st_mode):stack.append(q)
                    elif stat.S_ISREG(st.st_mode):files[str(q)]=identity(st)
                    elif stat.S_ISLNK(st.st_mode):links[str(q)]=dict(identity=identity(st),target=os.readlink(q))
                    else:raise RuntimeError('special oldv9 entry')
        finally:os.close(fd)
        guard()
    return dict(ordinary_file_identities=files,symlinks=links,directory_identities=dirs)

def budget():
    f=read(pin(SF));same(f['original_resource_factory_pin'])
    return b.budget()
