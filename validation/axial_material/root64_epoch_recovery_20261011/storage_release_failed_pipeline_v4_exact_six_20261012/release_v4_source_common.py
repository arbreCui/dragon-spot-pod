"""Exact failed-v4 protection and ownership. No import-time action or child."""
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys

sys.dont_write_bytecode=True
R=Path('/Users/wen/spot');ART=R/'validation/artifacts';REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
PACKAGE=Path(__file__).absolute().parent
LIBRARY=REC/'storage_release_20261012/storage_release_common.py'
spec=importlib.util.spec_from_file_location('exact_retained_storage_primitives',LIBRARY)
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
BRANCH=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v4'
ACTIVE=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v5'
PROGRESS=R/'validation/axial_material/SPOT_CURRENT_PROGRESS_20261011_2250.txt'
NAMES=['axial_macro.xsm','axial_track.xsm','basis.xsm','global_rcon.xsm','initial_pack.xsm','negative_pack.xsm']
TARGETS=[BRANCH/'AAA'/n for n in NAMES]
BYTES=970096676
MANIFEST=PACKAGE/'EXACT_SIX_FAILED_V4_OWNED_COPY_AND_PACK_MANIFEST.json'
PREVIOUS=REC/'storage_release_v3_seven_and_optional_maps_20261012/EXACT_7_FAILED_V3_INPUT_COPY_MANIFEST.json'


def inventory():
    files={};links={};dirs={};stack=[BRANCH]
    while stack:
        p=stack.pop();c.ancestors(p);s=p.lstat()
        if not stat.S_ISDIR(s.st_mode):raise RuntimeError('closed ordinary branch only')
        dirs[str(p)]=c.identity(s);fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:
            with os.scandir(fd)as entries:
                for e in entries:
                    q=p/e.name;s=e.stat(follow_symlinks=False)
                    if stat.S_ISDIR(s.st_mode):stack.append(q)
                    elif stat.S_ISREG(s.st_mode):files[str(q)]=c.identity(s)
                    elif stat.S_ISLNK(s.st_mode):links[str(q)]=dict(identity=c.identity(s),target=os.readlink(q))
                    else:raise RuntimeError('unexpected special file')
        finally:os.close(fd)
        c.guard()
    return dict(ordinary_file_identities=files,symlinks=links,directory_identities=dirs)


def protect():
    predecessor=c.read_pinned_json(c.pin(PREVIOUS));table={};origins=[]
    def add(row):
        row=c.normalize(row)
        if row['path']==str(PROGRESS)or Path(row['path']).is_relative_to(ACTIVE):return
        old=table.get(row['path'])
        if old is not None and old!=row:raise RuntimeError('conflicting current immutable pin '+row['path'])
        table[row['path']]=row
    def nested(value):
        temp={};c.add_nested_pins(value,temp)
        for row in temp.values():add(row)
    for row in predecessor['current_protected_full_EOF_pins']:add(row)
    add(c.pin(PREVIOUS))
    def meta(path,fields=None):
        row=c.pin(path);v=c.read_pinned_json(row);add(row);origins.append(row)
        if fields is None:nested(v)
        else:
            for key in fields:nested(v[key])
        return v,row
    hf,hfp=meta(REC/'aaa_three_plane_streaming_pipeline_source_v5/COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json')
    if hf['schema']!='COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V5':raise RuntimeError('current exact frozen v5 Source required')
    for row in hf['dependencies']:
        if Path(row['path']).name in('ACTUAL_SOURCE32_MUTATION_BRANCH_READONLY_LOCALIZATION_20261012.json','LPOD_ONLY_NEXT_CONTROL_SOURCE_REACHABILITY_20261012.json'):
            doc,p=meta(row['path'],['protected_small_closed_evidence_pins']if 'MUTATION_BRANCH'in row['path']else['full_Source_pins','current_original_A2_readonly_baseline'])
            if 'MUTATION_BRANCH'in row['path']and doc['observed_old_raw_files_are_historical_evidence_not_new_pipeline_required_inputs']is not True:
                raise RuntimeError('v4 raw observation cannot be silently discarded as current input')
        else:add(row)
    build,bp=meta(hf['selected_actual_build69_report']['path'],['fixed_current_pins','output_pins'])
    if bp!=hf['selected_actual_build69_report']or bp['sha256']!='97e74e45477d13086091b7867b1770999539bf9389bd4d122cd7d9ee30864573' or len(build['records'])!=10 or any(r['status']!='PASS'for r in build['records'])or build['failure']is not None or build['after_check_error']is not None:
        raise RuntimeError('true actual complete69v4 origin')
    sf,sfp=meta(hf['selected_fortran_freeze']['path'])
    if sfp!=hf['selected_fortran_freeze']:raise RuntimeError('exact current SF2')
    # SF2 retains the invalid v3 PACK as a real causal input. Its original raw
    # bytes remain protected. v5 source32 analysis retains small closed proofs;
    # old v4 raw observations are explicitly historical, not new live inputs.
    invalid=next(row for row in table.values()if row['path']==str(ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v3/AAA/initial_pack.xsm'))
    material=REC/'current_formal_material_authority_source_v1'
    material_rows=[]
    for p in sorted(material.iterdir()):
        if p.is_file():row=c.pin(p);add(row);material_rows.append(row)
    science=REC/'saved_full370_terminal_audit_host_source_v1'
    meta(science/'COMPLETE_SAVED_FULL370_GUARD_HOST_SOURCE_FREEZE.json')
    sci,sp=meta(science/'CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json')
    if len(sci['science_original_input_pins'])!=1129:raise RuntimeError('complete1129 original science inputs')
    for p in (PROGRESS,ACTIVE):
        if not os.path.lexists(p):raise RuntimeError('mutable retained progress/active branch must exist')
        c.ancestors(p)
    rows=sorted(table.values(),key=lambda r:r['path'])
    for row in rows:c.same(row)
    return rows,dict(predecessor_protected_manifest_pin=c.pin(PREVIOUS),current_pipeline5_freeze_pin=hfp,
      current_actual69v4_report_pin=bp,current_fortran_SF2_pin=sfp,selected_metadata_origin_pins=origins,
      complete_current_material_directory_file_pins=material_rows,all1129_saved_science_inputs_protected=True,
      invalid_v3_PACK_actual_causal_fullpin_retained=invalid,
      mutable_progress_and_active_v5_exist_without_immutable_file_pins=[str(PROGRESS),str(ACTIVE)],
      historical_v4_raw_observations_not_promoted_to_mandatory_pins=True)


def closed_proof():
    report=c.pin(BRANCH/'Root_actual_three_plane_engineering_summary.json');v=c.read_pinned_json(report)
    if v['schema']!='ACTUAL_INDEPENDENT_AAA3_INITIAL_GLOBAL_PROJECT_BOOT_ENGINEERING_ROOT_V1'or v['status']!='FAILED_UNQUALIFIED_NO_RETRY'or v['failure']!='RuntimeError: exact refusal reason and original child limits'or v['after_check_error']is not None or v['actual_terminal']is not None or len(v['records'])!=29:
        raise RuntimeError('exact failed v4 terminal/no retry proof')
    pins=[report];checks=[]
    for record in v['records']:
        wp=c.pin(BRANCH/(record['label']+'.watchdog.json'));lp=c.pin(BRANCH/(record['label']+'.log'));w=c.read_pinned_json(wp)
        expected=0 if record['status']=='PASS'else 1
        if record['status']not in('PASS','FAILED')or type(w['returncode'])is not int or w['returncode']!=expected or w['command']!=record['command']or w['limit_failure']is not None or w['own_child_only']is not True or w['liveness_group_cleanup']is not True or w['rss_cap_mib']!=512 or not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 or not 0<=w['sampled_peak_rss_mib']<512:
            raise RuntimeError('all29 real child closures and original caps')
        if record['status']=='PASS'and lp['sha256']!=record['log_sha256']:raise RuntimeError('complete successful log authority')
        if record['status']=='FAILED'and record['label']!='AAA/initial_source32':
            cases=[x for x in v['actual_operator_refusals']if x['original_execution_record_label']==record['label']]
            if len(cases)!=1 or cases[0]['actual_watchdog_pin']!=wp or cases[0]['actual_log_pin']!=lp or Path(lp['path']).read_text().count(cases[0]['expected_abort'])!=1:raise RuntimeError('exact prior negative refusal retained')
        if record['label']=='AAA/initial_source32'and Path(lp['path']).read_text().count('SPOASM: INVALID OFFLINE REAL64 SOURCE ITEM.')!=1:
            raise RuntimeError('exact final deep source32 rejection retained')
        pins.extend([wp,lp]);checks.append(dict(label=record['label'],status=record['status'],actual_exit_code=w['returncode']))
    for name in ('Root_actual_independent_three_plane_pack_readback.json','Root_actual_complete_execution_record_before_final_publication.json'):
        pins.append(c.pin(BRANCH/name))
    for n in (20,21,22):
        p=c.pin(BRANCH/('Root_actual_private_release_'+str(n).zfill(3)+'.json'));d=c.read_pinned_json(p)
        wanted=BRANCH/'AAA'/('native_A'+str(n-19)+'.xsm')
        if d['released_full_pin']['path']!=str(wanted)or os.path.lexists(wanted):raise RuntimeError('three copied native inputs already released, never count/delete twice')
        pins.append(p)
    return dict(report_pin=report,proof_pins=pins,all29_actual_child_results=checks,
      final_failure_is_wrong_expected_message_not_physical_transport_failure=True,
      all_original_source_refusal_evidence_retained=True,native_copies_already_absent_count=3)


def disjoint(targets,protected):
    paths={r['path']for r in protected};ids={tuple(r['identity'][:2])for r in protected}
    for row in targets:
        if row['path']not in[str(p)for p in TARGETS]or row['path']in paths or tuple(row['identity'][:2])in ids or row['identity'][3]!=1 or not stat.S_ISREG(row['identity'][2]):
            raise RuntimeError('target is not exact independent owned raw or intersects protected DAG')
        c.same(row)


def owning_provenance(targets):
    source=REC/'aaa_three_plane_streaming_pipeline_source_v4/run_actual_three_plane_pipeline.py';sp=c.pin(source);text=Path(source).read_text()
    for anchor in ["copy(formal[original],name)","'basis_reference.xsm','basis.xsm'","copy(c.pin(WORK/'initial_pack.xsm'),'negative_pack.xsm')","runner.execute(WORK,'mutate_'+mutation", "packed=data.packed_readback(WORK/'initial_pack.xsm',plan)"]:
        if anchor not in text:raise RuntimeError('full original v4 ownership/copy/mutation Source changed')
    plan=c.read_pinned_json(c.pin(REC/'aaa_three_plane_streaming_source_v1/PROTECTED_FORMAL_AND_PRODUCER_INPUTS.json'))
    formal={Path(p['path']).name:p for p in plan['formal_inputs']};mapping={'axial_macro.xsm':'initial_axial_macrolib.xsm','axial_track.xsm':'initial_axial_track.xsm','basis.xsm':'basis_reference.xsm','global_rcon.xsm':'route_contract.xsm'}
    originals=[]
    report=c.read_pinned_json(c.pin(BRANCH/'Root_actual_three_plane_engineering_summary.json'))
    for row in targets:
        actual=next(p for p in report['output_pins']if p['path']==row['path'])
        if actual!=row:raise RuntimeError('own failed v4 output pin changed')
        name=Path(row['path']).name
        if name in mapping:
            old=formal[mapping[name]];c.same(old)
            if old['sha256']!=row['sha256']or old['size_bytes']!=row['size_bytes']or old['identity'][:2]==row['identity'][:2]:raise RuntimeError('whole same-byte independent formal input copy')
            originals.append(dict(candidate_pin=row,retained_original_fullpin=old,role='WHOLE_OWNED_ACCESS_COPY'))
        else:originals.append(dict(candidate_pin=row,role='OWNED_PACK_OUTPUT'if name=='initial_pack.xsm'else'OWNED_FINAL_SOURCE32_MUTATED_PACK_CLONE',owning_stage='AAA/pack'if name=='initial_pack.xsm'else'AAA/mutate_source32',original_v4_host_source_pin=sp))
    return dict(original_v4_host_source_pin=sp,owned_roles=originals,initial_PACK_18_fulltree_readback_pin=c.pin(BRANCH/'Root_actual_independent_three_plane_pack_readback.json'),negative_source32_raw_historical_only=True)
