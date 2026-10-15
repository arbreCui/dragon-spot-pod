"""Only two literal closed-run private PROJECT intermediates; no import-time action."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import stat
import sys
import time

sys.dont_write_bytecode=True
ROOT=Path('/Users/wen/spot'); ART=ROOT/'validation/artifacts'
REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
PKG=Path(__file__).absolute().parent
BRANCHES=[ART/('axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-'+v) for v in ('v7','v8')]
TARGETS=[p/'AAA/projected_boot.xsm' for p in BRANCHES]
BYTES=1498711904
MANIFEST=PKG/'EXACT_TWO_CLOSED_FAILED_RUN_PROJECT_PRIVATE_COPY_MANIFEST.json'
SOURCE_NAMES=['project_pair_release_common.py','prepare_exact_project_pair_manifest.py','verify_or_execute_exact_project_pair.py']
HF9=REC/'aaa_three_plane_streaming_pipeline_source_v9/COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json'
BIND=REC/'current_mount_full_identity_common_source_v1/CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json'
CATALOG=REC/'current_mount_identity_reattestation_20261012/CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG.json'
V9_CLOSURE=REC/'ACTUAL_PIPELINE_V9_PRELAUNCH_HISTORY_REFUSAL_TRUE_TOOL_RETURNS_20261013.json'
V9_OUT=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v9'
FACTORY=ROOT/'validation/axial_material/moment_order_complete_history_resource_trie_20261010.py'
START=time.monotonic()

def guard():
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20:raise RuntimeError('original SELF512MiB limit reached')
    if time.monotonic()-START>=1800:raise RuntimeError('original whole1800 second limit reached')

def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def ancestors(p):
    p=Path(p)
    if not p.is_absolute() or '..' in p.parts:raise RuntimeError('canonical absolute path required')
    for q in reversed(p.parents):
        if not stat.S_ISDIR(q.lstat().st_mode):raise RuntimeError('non-directory or symlink ancestor '+str(q))

def pin(p):
    p=Path(p);ancestors(p);before=p.lstat()
    if not stat.S_ISREG(before.st_mode):raise RuntimeError('regular nonsymlink required '+str(p))
    h=hashlib.sha256();n=0;fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        if identity(os.fstat(fd))!=identity(before):raise RuntimeError('changed at open')
        while True:
            b=os.read(fd,1024*1024)
            if not b:break
            h.update(b);n+=len(b);guard()
        eof=identity(os.fstat(fd))
    finally:os.close(fd)
    after=identity(p.lstat())
    if identity(before)!=eof or eof!=after or n!=before.st_size:raise RuntimeError('full EOF/7ID changed '+str(p))
    return dict(path=str(p),sha256=h.hexdigest(),size_bytes=n,identity=after)

def norm(r):
    return dict(path=r['path'],sha256=r['sha256'],size_bytes=r.get('size_bytes',r.get('bytes')),identity=r.get('identity',r.get('seven_id')))

def same(r):
    r=norm(r)
    if pin(r['path'])!=r:raise RuntimeError('full EOF SHA/7ID mismatch '+r['path'])
    return r

def read(r):
    r=same(r);raw=Path(r['path']).read_bytes()
    if len(raw)!=r['size_bytes'] or hashlib.sha256(raw).hexdigest()!=r['sha256'] or identity(Path(r['path']).lstat())!=r['identity']:raise RuntimeError('JSON changed during read')
    return json.loads(raw)

def nested(v):
    if isinstance(v,dict):
        if 'path' in v and 'sha256' in v and ('identity' in v or 'seven_id' in v):yield norm(v);return
        for x in v.values():yield from nested(x)
    elif isinstance(v,list):
        for x in v:yield from nested(x)

def write_new(p,v):
    raw=(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())

def update_owned(p,v,old):
    same(old)
    if old['identity'][3]!=1:raise RuntimeError('owned receipt must retain one link')
    temp=p.with_suffix('.pending');write_new(temp,v);os.replace(temp,p);return pin(p)

def protection():
    """Explicit reachable roles, all catalog current rows, no historical tree closure."""
    table={};origins=[];roles={};reattest=[];cache={}
    def actual(path):
        path=str(path)
        if path not in cache:cache[path]=pin(path)
        elif identity(Path(path).lstat())!=cache[path]['identity']:raise RuntimeError('protected identity changed within audit')
        return cache[path]
    catpin=actual(CATALOG);cat=read(catpin)
    if cat['schema']!='CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG_V1' or cat['status']!='ACTUAL_CURRENT_MOUNT_COMPLETE_PF_CATALOG_CLOSED0_ONLY' or len(cat['rows'])!=3040 or cat['mandatory_failures']!=[] or cat['explicit_device_transition']!={'historical':16777234,'current':16777229,'only_device_field_may_change':True}:raise RuntimeError('exact actual complete current catalog required')
    mapping={}
    for entry in cat['rows']:
        old=norm(entry['historical_pin']);new=norm(entry['current_pin'])
        if old['path']!=new['path'] or old['sha256']!=new['sha256'] or old['size_bytes']!=new['size_bytes'] or old['identity'][1:]!=new['identity'][1:] or old['identity'][0] not in (16777234,16777229) or new['identity'][0]!=16777229:raise RuntimeError('catalog transition exceeds only device field')
        key=json.dumps(old,sort_keys=True)
        if key in mapping and mapping[key]!=new:raise RuntimeError('conflicting catalog rows')
        mapping[key]=new
    def add(row,role):
        old=norm(row);new=actual(old['path'])
        if new!=old:
            mapped=mapping.get(json.dumps(old,sort_keys=True))
            if mapped is not None:
                if mapped!=new:raise RuntimeError('catalog mapped current fullpin changed')
                reason='EXACT_SELECTED_CURRENT_CATALOG_ROW'
            elif old['path']==new['path'] and old['sha256']==new['sha256'] and old['size_bytes']==new['size_bytes'] and old['identity'][0]==16777234 and new['identity'][0]==16777229 and old['identity'][1:]==new['identity'][1:]:reason='ADDITIONAL_EXPLICIT_FULL_EOF_ONLY_DECLARED_DEVICE_TRANSITION'
            else:raise RuntimeError('live dependency changed beyond exact current mount device '+old['path'])
            event=dict(historical_pin=old,current_pin=new,scope=reason)
            if event not in reattest:reattest.append(event)
        existing=table.get(new['path'])
        if existing is not None and existing!=new:raise RuntimeError('conflicting protected fullpin')
        table[new['path']]=new;roles.setdefault(role,set()).add(new['path']);return new
    def meta(path,role):
        row=add(actual(path),role);d=read(row);origins.append(dict(role=role,pin=row));return d
    def rows(values,role):
        for row in nested(values):add(row,role)
    def directory(path,role):
        for p in sorted(path.iterdir()):
            if stat.S_ISREG(p.lstat().st_mode):add(actual(p),role)
            elif p.is_dir():continue
            else:raise RuntimeError('Source directory unexpected symlink/special')
    add(catpin,'current_catalog_file')
    rows([x['current_pin'] for x in cat['rows']],'catalog_all3040_current_rows')
    common=meta(BIND,'current_Common_BIND')
    if len(common['fixed_current_pins'])!=2012:raise RuntimeError('all2012 current Common fixed pins')
    rows(common['fixed_current_pins'],'current_Common_BIND2012')
    hf=meta(HF9,'current_v9_HF')
    if len(hf['dependencies'])!=257:raise RuntimeError('all257 current v9 dependencies')
    rows([hf['host_source']]+hf['dependencies'],'current_v9_257deps_and_host')
    buildpin=add(hf['selected_actual_build70_report'],'actual_current70_report')
    build=read(buildpin)
    if build['failure'] is not None or build['after_check_error'] is not None or any(x['status']!='PASS' for x in build['records']):raise RuntimeError('actual current70 PASS origin required')
    rows(build['fixed_current_pins'],'actual_current70_fixed');rows(build['output_pins'],'actual_current70_outputs')
    science=REC/'saved_full370_terminal_audit_host_source_v2'
    b=meta(science/'CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json','saved_full370_current_BIND')
    if len(b['fixed_current_pins'])!=3315 or len(b['science_original_input_pins'])!=1129:raise RuntimeError('complete3315 live science protection required')
    rows(b['fixed_current_pins'],'saved_full370_current3315');rows(b['science_original_input_pins'],'saved_full370_science1129')
    for name in ('COMPLETE_SAVED_FULL370_GUARD_HOST_SOURCE_FREEZE.json','COMPLETE_SAVED_FULL370_SCIENCE_SOURCE_FREEZE.json'):
        d=meta(science/name,'saved_full370_current_freezes')
        for field in ('fixed_source_files','files','source_files'):
            if field in d:rows(d[field],'saved_full370_current_frozen_Source')
    directory(science,'saved_full370_current_package')
    material=REC/'current_formal_material_authority_handle_lifetime69_source_v2'
    directory(material,'current_material_v2_actual_Source_files')
    for name in ('COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json','COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json'):
        d=meta(material/name,'current_material_v2_freezes')
        for field in ('host_source','dependencies','files','original_math_sources','current_plan_pin','complete_math_inverse_proof_pins','selected_actual69_report_pin','selected_source_freeze_pin','selected_actual69_independent_review_pin','current_actual69_Fortran_freeze_pin','current_actual69_build_host_freeze_pin','actual69_tool_terminal_receipt_pin','independent_material_source_review_pin','selected_plan_full_byte_inverse_pin','native_handle_driver_Source_freeze_pin','native_handle_driver_Source_pin'):
            if field in d:rows(d[field],'current_material_v2_frozen_live_pins')
    for name in ('CURRENT_FORMAL_MATERIAL_AUTHORITY_SELECTED_HANDLE69_PLAN.json','CURRENT_FORMAL_COMPLETE_AB_ORIGINAL_MATERIAL_SEED_PLAN_SOURCE_ONLY.json'):
        d=meta(material/name,'current_material_v2_live_plans');rows(d,'current_material_v2_live_plan_pins')
    formal=meta(REC/'aaa_three_plane_streaming_source_v1/PROTECTED_FORMAL_AND_PRODUCER_INPUTS.json','formal_and_producer_current_plan')
    rows(formal,'formal_and_producer_plan_live_inputs')
    gd=REC/'current_eleven_saved_gendf_host_source_v3'
    directory(gd,'GENDF_v3_source');directory(REC/'reaction_genDF_stream_source_v1','GENDF_original_parser_source')
    for name in ('COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json','COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json'):
        d=meta(gd/name,'GENDF_v3_freezes')
        for field in ('host_source','dependencies','selected_source_freeze_pin','complete_source_file_pins','static_input_pins','selected_genDF_source_plan_pin','current_plan_pin','complete_byte_inverse_pin','independent_finite_Source_review_pin','original_immutable_compiler_role_pin'):
            if field in d:rows(d[field],'GENDF_v3_live_fixed_pins')
    d=meta(REC/'reaction_genDF_stream_source_v1/CURRENT_ELEVEN_NONZERO_NX_SAVED_GENDF_SOURCE_PLAN.json','GENDF_eleven_original_plan');rows(d['inputs'],'GENDF_eleven_original_inputs');rows(d['source_pin'],'GENDF_original_parser')
    ref=REC/'full370_unreduced_eigen_reference_source_v2';directory(ref,'independent_ref_v2_source')
    d=meta(ref/'CURRENT_FORMAL_FULL370_INPUT_PLAN_SOURCE_ONLY.json','independent_ref_v2_plan')
    for field in ('protected_formal_and_producer_plan_pin','current_case_spec_pin','current_prepared_pin','current_axial_track_pin','additional_current_input_pins'):rows(d[field],'independent_ref_v2_live_inputs')
    add(actual(FACTORY),'original_resource_factory')
    add(actual(V9_CLOSURE),'actual_v9_prelaunch_closed_tool_receipt')
    return sorted(table.values(),key=lambda x:x['path']),dict(selected_metadata_origins=origins,explicit_current_mount_only_device_reattestations=reattest,roles={k:sorted(v) for k,v in roles.items()},all3040_catalog_current_rows_included=True,all2012_Common_BIND_pins_included=True,all3315_saved_full370_current_pins_included=True,all257_v9_dependencies_included=True,no_historical_resource_tree_promoted_to_live=True,all_business_and_physics_qualification_flags_unchanged=True)

def inventory():
    files={};links={};dirs={};stack=list(BRANCHES)
    while stack:
        p=stack.pop();ancestors(p);s=p.lstat()
        if not stat.S_ISDIR(s.st_mode):raise RuntimeError('ordinary closed branch directory required')
        dirs[str(p)]=identity(s);fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:
            with os.scandir(fd) as it:
                for e in it:
                    q=p/e.name;s=e.stat(follow_symlinks=False)
                    if stat.S_ISDIR(s.st_mode):stack.append(q)
                    elif stat.S_ISREG(s.st_mode):files[str(q)]=identity(s)
                    elif stat.S_ISLNK(s.st_mode):links[str(q)]=dict(identity=identity(s),target=os.readlink(q))
                    else:raise RuntimeError('unexpected special closed-branch file')
        finally:os.close(fd)
        guard()
    return dict(ordinary_file_identities=files,symlinks=links,directory_identities=dirs)

def closed_proofs(targets):
    proofs=[]
    for version,branch,target in zip(('v7','v8'),BRANCHES,targets):
        sp=pin(branch/'Root_actual_three_plane_engineering_summary.json');d=read(sp)
        if d['schema']!='ACTUAL_INDEPENDENT_AAA3_INITIAL_GLOBAL_PROJECT_BOOT_ENGINEERING_ROOT_V1' or d['status']!='FAILED_UNQUALIFIED_NO_RETRY' or d['failure']!='RuntimeError: exact refusal reason and original child limits' or d['after_check_error'] is not None or d['actual_terminal'] is not None or len(d['records'])!=41 or d['engineering_three_plane_closed0'] is not False:raise RuntimeError('exact closed failed overall run required')
        if next(x for x in d['output_pins'] if x['path']==target['path'])!=target:raise RuntimeError('current target fullpin differs from failed summary output authority')
        selected={x['label']:x for x in d['records']}
        if selected['AAA/global_positive']['status']!='PASS' or selected['AAA/project_positive']['status']!='PASS' or d['records'][-1]['label']!='AAA/view_missing_operand':raise RuntimeError('preserve actual GLOBAL/PROJECT PASS and exact failed prefix provenance')
        watches=[]
        for r in d['records']:
            wp=pin(branch/(r['label']+'.watchdog.json'));w=read(wp);lp=pin(branch/(r['label']+'.log'))
            expected=0 if r['status']=='PASS' else 1
            if r['status'] not in ('PASS','FAILED') or type(w['returncode']) is not int or w['returncode']!=expected or w['command']!=r['command'] or w['liveness_group_cleanup'] is not True or w['own_child_only'] is not True or w['limit_failure'] is not None or w['rss_cap_mib']!=512 or not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 or not 0<=w['sampled_peak_rss_mib']<512:raise RuntimeError('all41 own children must be genuinely closed within original caps')
            if r['status']=='PASS' and lp['sha256']!=r['log_sha256']:raise RuntimeError('retained whole successful stage log changed')
            watches.append(dict(label=r['label'],status=r['status'],actual_exit_code=w['returncode'],watchdog_pin=wp,log_pin=lp))
        name='ACTUAL_PIPELINE_V7_TRUE_TOOL_RETURNS_20261012.json' if version=='v7' else 'ACTUAL_PIPELINE_V8_TRUE_TOOL_RETURNS_20261013.json'
        tp=pin(REC/name);t=read(tp)
        if t['observed_closed'] is not True or t['original_integer_exit_code']!=1 or t['terminal']['exit_code']!=1:raise RuntimeError('Root true actual exit1 closure required')
        owner=pin(REC/('aaa_three_plane_streaming_pipeline_source_'+version)/'run_actual_three_plane_pipeline.py')
        text=Path(owner['path']).read_text()
        if "'projected_boot.xsm'" not in text or 'project_positive' not in text:raise RuntimeError('actual own PROJECT output Source required')
        proofs.append(dict(failed_overall_summary_pin=sp,Root_true_closed_exit1_tool_receipt_pin=tp,actual_owning_pipeline_Source_pin=owner,all41_actual_child_closures=watches,GLOBAL_and_PROJECT_individual_stages_PASS=True,online_BOOT_not_qualified=True,raw_role='CLOSED_FAILED_OVERALL_RUN_PRIVATE_DEEP_PROJECT_INTERMEDIATE',old_run_raw_path_replay_unavailable_after_release=True,producer_or_mathematical_invalidity_not_inferred=True))
    return proofs

def disjoint(targets,protected):
    if [r['path'] for r in targets]!=[str(x) for x in TARGETS] or sum(r['size_bytes'] for r in targets)!=BYTES:raise RuntimeError('literal exact two candidates and bytes only')
    for row in targets:owned_disjoint(row,protected)

def owned_disjoint(row,protected):
    paths={r['path'] for r in protected};inodes={tuple(r['identity'][:2]) for r in protected}
    if row['path'] not in [str(x) for x in TARGETS] or row['identity'][3]!=1 or not stat.S_ISREG(row['identity'][2]) or row['path'] in paths or tuple(row['identity'][:2]) in inodes:raise RuntimeError('candidate is not private regular nlink1 disjoint from current live DAG')
    same(row)

def writer_gate():
    d=read(pin(V9_CLOSURE))
    if d['observed_closed'] is not True or d['original_integer_exit_code']!=1 or d['terminal']['exit_code']!=1 or d['no_business_child_launched'] is not True or d['no_v9_output_created'] is not True or os.path.lexists(V9_OUT):raise RuntimeError('v9 must remain true closed prelaunch refusal with no business child or output')

def budget():
    spec=importlib.util.spec_from_file_location('original_exact_pair_history_factory',FACTORY);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    observer=m.DynamicHistoryResources(ART,m.history_roots([],ART),8*2**30,96*2**30);d=observer.check();guard()
    d.update(original_cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,initial_fresh_reserve_bytes=2*2**30)
    d['remaining_after_original_initial_reserves_bytes']=96*2**30-d['artifact_bytes']-20971764748-64*2**20-2*2**30
    d['original_initial_reserve_admitted']=d['remaining_after_original_initial_reserves_bytes']>0
    return d
