#!/usr/bin/env python3
"""Finite read-only survey. No production import, child, compilation or deletion."""
import ast
import gc
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import stat
import time

ROOT=Path('/Users/wen/spot'); REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'; ART=ROOT/'validation/artifacts'
HERE=Path(__file__).absolute().parent
START=time.monotonic(); seen={}; actual_eof_bytes=0
TARGETS=[ART/('axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-'+v)/'AAA/projected_boot.xsm' for v in ('v11','v12')]
TARGET_NAMES={str(p) for p in TARGETS}
def identity(s): return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def guard():
    if time.monotonic()-START>=1800: raise RuntimeError('finite survey whole1800')
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20: raise RuntimeError('finite survey SELF512MiB')
def pin(p):
    global actual_eof_bytes
    p=Path(p); key=str(p); before=p.lstat()
    if not stat.S_ISREG(before.st_mode): raise RuntimeError('ordinary nonsymlink '+key)
    if key in seen:
        if identity(before)!=seen[key]['identity']: raise RuntimeError('previous EOF changed '+key)
        return seen[key]
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    h=hashlib.sha256(); count=0
    try:
        if identity(os.fstat(fd))!=identity(before): raise RuntimeError('FD opening all7 '+key)
        while True:
            block=os.read(fd,2**20)
            if not block: break
            h.update(block); count+=len(block); guard()
        if identity(os.fstat(fd))!=identity(before): raise RuntimeError('FD EOF all7 '+key)
    finally: os.close(fd)
    if identity(p.lstat())!=identity(before) or count!=before.st_size: raise RuntimeError('path after EOF all7 '+key)
    out=dict(path=key,sha256=h.hexdigest(),size_bytes=count,identity=identity(before)); seen[key]=out;actual_eof_bytes+=count;return out
def read(p):
    row=pin(p); d=json.loads(Path(p).read_text())
    if identity(Path(p).lstat())!=row['identity']: raise RuntimeError('JSON changed '+str(p))
    return d
def typed(v,at='$'):
    if isinstance(v,dict):
        if isinstance(v.get('path'),str) and isinstance(v.get('sha256'),str) and isinstance(v.get('identity'),list) and len(v['identity'])==7:
            yield at,v
        for k,x in v.items(): yield from typed(x,at+'.'+k)
    elif isinstance(v,list):
        for i,x in enumerate(v): yield from typed(x,at+'['+str(i)+']')
def string_hits(v,at='$'):
    if isinstance(v,str):
        for target in TARGET_NAMES:
            if target in v: yield dict(json_location=at,target=target,exact_path_string=v==target)
    elif isinstance(v,dict):
        for k,x in v.items(): yield from string_hits(x,at+'.'+k)
    elif isinstance(v,list):
        for i,x in enumerate(v): yield from string_hits(x,at+'['+str(i)+']')
def verify_declared(rows):
    for row in rows:
        actual=pin(row['path'])
        if actual!=row: raise RuntimeError('current declared pin mismatch '+row['path'])
def directory_files(root):
    out=[]; dirs=[]; links=[]; stack=[root]
    while stack:
        p=stack.pop();st=p.lstat()
        if not stat.S_ISDIR(st.st_mode): raise RuntimeError('directory changed '+str(p))
        dirs.append(dict(path=str(p),identity=identity(st)))
        fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:
            with os.scandir(fd) as entries:
                for e in entries:
                    q=p/e.name;s=e.stat(follow_symlinks=False)
                    if stat.S_ISDIR(s.st_mode):stack.append(q)
                    elif stat.S_ISREG(s.st_mode):out.append(q)
                    elif stat.S_ISLNK(s.st_mode):links.append(dict(path=str(q),identity=identity(s)))
                    else:raise RuntimeError('special entry '+str(q))
        finally: os.close(fd)
        guard()
    return sorted(out),sorted(dirs,key=lambda r:r['path']),links
def source_tree(root):
    files,dirs,links=directory_files(root)
    if links:raise RuntimeError('Source package symlink '+str(root))
    if root.name=='streaming_serializer_min5_finite_proof_v2_20261013':
        # Closed proof reports and finite Source/provenance are selected. The
        # 90 generated serializer fixtures are retained but are not Source.
        files=[p for p in files if p.parent==root or p.name=='REVIEW.json']
    rows=[pin(p)for p in files]
    # Python parsed as data only. No module is imported or executed.
    for p in files:
        if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p))
    return files,rows

groups={
 'current_v13_HF_and_Source':REC/'aaa_three_plane_streaming_pipeline_source_v13',
 'streaming_serializer_bundle':REC/'streaming_full_ledger_serializer_min5_source_bundle_v1_20261013',
 'finite_input_and_closed_proof_evidence':REC/'streaming_serializer_min5_finite_proof_v2_20261013',
 'saved_full370_v2':REC/'saved_full370_terminal_audit_host_source_v2',
 'current_material_v7':REC/'current_formal_material_authority_exact_cache70_source_v7',
 'planned_material_v13_readonly_binding':REC/'material_v7_to_planned_v13_readonly_binding_plan_20261013',
 'GENDF_v4':REC/'current_eleven_saved_gendf_current_mount_host_source_v4',
 'independent_reference_v2':REC/'full370_unreduced_eigen_reference_source_v2',
}
packages={};occurrences=[];all_json_occurrences=[];package_snapshots={}
for group,root in groups.items():
    files,rows=source_tree(root);packages[group]=rows;package_snapshots[group]=[str(p)for p in files]
    for p in files:
        if p.suffix=='.json':
            d=read(p)
            for at,row in typed(d):
                if row['path']in TARGET_NAMES:occurrences.append(dict(group=group,document_pin=seen[str(p)],json_location=at,target_pin=row))
            hits=list(string_hits(d))
            if hits:all_json_occurrences.append(dict(group=group,document_pin=seen[str(p)],exact_target_path_occurrences=hits))
            del d
    gc.collect();guard()

hf=read(groups['current_v13_HF_and_Source']/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json')
verify_declared([hf['host_source']]+hf['dependencies'])
if len(hf['dependencies'])!=354:raise RuntimeError('exact current v13 direct354 Source dependencies')
current_v13_summary=read(ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261013-v13/Root_actual_three_plane_engineering_summary.json')
saved_binding=read(groups['saved_full370_v2']/'CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json')
old_manifest=read(REC/'storage_release_old_v10_single_PROJECT_source_v3_20261013/EXACT_SINGLE_OLD_V10_PRIVATE_PROJECT_RELEASE_MANIFEST.json')
selected_gates={
 'v13_HF_direct_host_and354': [hf['host_source']]+hf['dependencies'],
 'actual_v13_fixed_current_pins':current_v13_summary['fixed_current_pins'],
 'saved_full370_v2_fixed_current3315':saved_binding['fixed_current_pins'],
 'saved_full370_v2_scientific1129':saved_binding['science_original_input_pins'],
}
for name in ('COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_FREEZE.json','COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_FREEZE.json','COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json'):
    d=read(groups['current_material_v7']/name); selected_gates['material_v7_'+name]=[d['host_source']]+d['dependencies'];del d
d=read(groups['GENDF_v4']/'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json')
selected_gates['GENDF_v4_direct_host_and67']=[d['host_source']]+d['dependencies'];del d
d=read(groups['independent_reference_v2']/'CURRENT_FORMAL_FULL370_INPUT_PLAN_SOURCE_ONLY.json')
selected_gates['independent_reference_v2_direct_input_plan_pins']=[r for _,r in typed(d)];del d
gate_membership={}
for name,rows in selected_gates.items():
    hits=[row for row in rows if row['path']in TARGET_NAMES]
    gate_membership[name]=dict(row_count=len(rows),candidate_direct_mandatory_occurrences=hits)
    if hits:raise RuntimeError('candidate directly mandatory in selected current gate '+name)
old_protected=[r for r in old_manifest['current_protected_full_EOF_pins']if r['path']in TARGET_NAMES]
old_roles={k:[p for p in paths if p in TARGET_NAMES]for k,paths in old_manifest['Source_DAG_provenance']['roles'].items()if any(p in TARGET_NAMES for p in paths)}
if len(old_protected)!=2:raise RuntimeError('historical previous explicit two protected PROJECT rows')

# These are current Source writers/reviews, not future v14 admission.
root_sources=[REC/'prepare_v13_streaming_serializer_pipeline_source_only_20261013.py',REC/'ROOT_EXACT_ACTUAL_PIPELINE_V13_ARGV_20261013.json',REC/'ROOT_V13_COMPLETE_SOURCE_INTEGRATION_READONLY_REVIEW_20261013.json',REC/'ROOT_ACTUAL_V13_SOURCE_PREPARATION_TRUE_TOOL_RETURN_20261013.json']
for p in root_sources:pin(p)
future_v14_paths=sorted(str(p)for p in REC.glob('*v14*'))
root_source_text_mentions=[]
for p in root_sources:
    text=p.read_text()
    for target in TARGET_NAMES:
        if target in text:root_source_text_mentions.append(dict(source_pin=seen[str(p)],target=target))

old_branches={};target_rows=[]
for version,target in zip(('v11','v12'),TARGETS):
    branch=target.parent.parent;files,dirs,links=directory_files(branch)
    if links:raise RuntimeError('old failed branch symlink')
    rows=[pin(p)for p in files];row=seen[str(target)]
    if row['size_bytes']!=749355952 or row['sha256']!='ea56e0e58889469c81e1519713ca0df93a3ebb5f2b1a1fbd2e20b5d8be72833a' or row['identity'][3]!=1 or target.lstat().st_uid!=os.getuid():raise RuntimeError('exact private current own target')
    previous=next(r for r in old_protected if r['path']==str(target))
    if previous!=row:raise RuntimeError('previous protected physical pin changed')
    summary=read(branch/'Root_actual_three_plane_engineering_summary.json');raw=read(branch/'Root_actual_complete_execution_record_before_final_publication.json');stages=read(branch/'AAA3-streaming/stages.json')
    toolname='ACTUAL_PIPELINE_V11_TRUE_TOOL_RETURNS_20261013.json'if version=='v11'else'ACTUAL_PIPELINE_V12_PARENT_PHASE_ROOT_TRUE_TOOL_RETURNS_20261013.json'
    tool=read(REC/toolname)
    if tool.get('observed_closed')is not True or tool.get('original_integer_exit_code')!=1:raise RuntimeError('genuine failed Root closed1 '+version)
    if summary['status']!='FAILED_UNQUALIFIED_NO_RETRY' or summary['engineering_three_plane_closed0']is not False or summary['actual_terminal']is not None or summary['output_pins']!=[] or summary['failure']!='RuntimeError: original SELF 512MiB cap':raise RuntimeError('true failed aggregate '+version)
    if [{k:v for k,v in r.items()if k not in('resource_before','resource_after')}for r in raw['records']]!=summary['records'] or stages!={'stages':raw['records']} or row not in raw['owned_runtime_pins']:raise RuntimeError('complete actual raw/stages and owned target '+version)
    by_label={r['label']:r for r in summary['records']}
    if by_label['AAA/global_positive']['status']!='PASS'or by_label['AAA/project_positive']['status']!='PASS':raise RuntimeError('retain actual individual GLOBAL/PROJECT PASS')
    closure=[]
    for record in summary['records']:
        w=read(branch/(record['label']+'.watchdog.json'));expected=0 if record['status']=='PASS'else 1
        if w['returncode']!=expected or w['limit_failure']is not None or w['own_child_only']is not True or w['liveness_group_cleanup']is not True or w['command']!=record['command']:raise RuntimeError('closed old stage '+record['label'])
        closure.append(dict(label=record['label'],returncode=w['returncode'],watchdog_pin=seen[str(branch/(record['label']+'.watchdog.json'))]))
    old_branches[version]=dict(target_full_EOF_pin=row,complete_regular_files=len(rows),complete_regular_bytes=sum(r['size_bytes']for r in rows),all_directory_identities=dirs,all_other_full_EOF_pins=[r for r in rows if r['path']!=str(target)],true_Root_exit1_tool_pin=seen[str(REC/toolname)],actual_summary_pin=seen[str(branch/'Root_actual_three_plane_engineering_summary.json')],actual_raw_pin=seen[str(branch/'Root_actual_complete_execution_record_before_final_publication.json')],all_actual_children_closed_at_original_caps=closure,GLOBAL_PROJECT_individual_PASS_preserved=True,failed_boot_not_qualified=True,old_full_PROJECT_GLOBAL_raw_replay_lost_after_future_release=True)
    target_rows.append(row);del summary,raw,stages,tool;gc.collect();guard()

# A single traversal produces both ALL ART and exact original axial-family
# logical regular-file totals. Symlinks are counted as entries, never followed.
direct_before=sorted((e.name,identity(e.stat(follow_symlinks=False)))for e in os.scandir(ART))
totals=dict(all_ART_regular_bytes=0,all_ART_regular_files=0,axial_family_regular_bytes=0,axial_family_regular_files=0,symlink_entries_not_followed=0,directory_count=0)
scan_target_ids={};root_names=set();stack=[(ART,False)]
while stack:
    directory,in_family=stack.pop();fd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:
        totals['directory_count']+=1
        with os.scandir(fd)as entries:
            for entry in entries:
                p=directory/entry.name;s=entry.stat(follow_symlinks=False)
                family=in_family or(directory==ART and entry.name.startswith('axial-material-'))
                if stat.S_ISDIR(s.st_mode):
                    if directory==ART and family:root_names.add(str(p))
                    stack.append((p,family))
                elif stat.S_ISREG(s.st_mode):
                    totals['all_ART_regular_bytes']+=s.st_size;totals['all_ART_regular_files']+=1
                    if family:totals['axial_family_regular_bytes']+=s.st_size;totals['axial_family_regular_files']+=1
                    if str(p)in TARGET_NAMES:scan_target_ids[str(p)]=identity(s)
                elif stat.S_ISLNK(s.st_mode):totals['symlink_entries_not_followed']+=1
                else:raise RuntimeError('special ART entry '+str(p))
    finally:os.close(fd)
    guard()
direct_after=sorted((e.name,identity(e.stat(follow_symlinks=False)))for e in os.scandir(ART))
if direct_after!=direct_before:raise RuntimeError('ART direct entries changed during same-pass traversal')
for row in target_rows:
    if scan_target_ids[row['path']]!=row['identity']or identity(Path(row['path']).lstat())!=row['identity']:raise RuntimeError('target changed during same-pass accounting')
for group,root in groups.items():
    files,_,links=directory_files(root)
    if root.name=='streaming_serializer_min5_finite_proof_v2_20261013':files=[p for p in files if p.parent==root or p.name=='REVIEW.json']
    if links or[str(p)for p in files]!=package_snapshots[group]:raise RuntimeError('Source package file set changed')
for row in seen.values():
    if identity(Path(row['path']).lstat())!=row['identity']:raise RuntimeError('observed physical row changed before publication '+row['path'])
history=96*2**30;cold=20971764748;metadata=64*2**20;fresh=2*2**30;free=shutil.disk_usage(ART).free
remaining=history-totals['axial_family_regular_bytes']-cold-metadata-fresh
bytes_pair=sum(r['size_bytes']for r in target_rows)
budget=dict(**totals,original_dynamic_axial_family_roots=sorted(root_names),history_cap_bytes=history,cold_reserve_bytes=cold,metadata_reserve_bytes=metadata,full_original_initial_fresh_reserve_bytes=fresh,global_free_floor_bytes=8*2**30,actual_filesystem_free_bytes=free,current_remaining_after_original_initial_reserves_bytes=remaining,current_initial_reserve_admitted=remaining>0 and free>=8*2**30,predicted_pair_release_bytes=bytes_pair,predicted_after_pair_axial_family_regular_bytes=totals['axial_family_regular_bytes']-bytes_pair,predicted_after_pair_remaining_after_original_initial_reserves_bytes=remaining+bytes_pair,predicted_pair_can_restore_full_original_initial_reserve=remaining+bytes_pair>0 and free>=8*2**30,predicted_if_v11_only_remaining_bytes=remaining+target_rows[0]['size_bytes'],predicted_if_v12_only_remaining_bytes=remaining+target_rows[1]['size_bytes'],prediction_not_actual_deletion=True)
report=dict(schema='READONLY_V11_V12_PRIVATE_PROJECT_CURRENT_GATE_DEPENDENCY_AND_STORAGE_SURVEY_V1',status='READONLY_CANDIDATES_ONLY_FINAL_V14_FREEZE_AND_ROOT_RELEASE_GATES_REQUIRED',failure=None,source_only_readonly=True,candidate_imported=False,compiler_or_numerical_executed=False,delete_move_truncate_executed=False,process_or_open_handle_absence_proven=False,process_metadata_not_requested=True,finite_actual_EOF_file_count=len(seen),finite_actual_EOF_bytes=actual_eof_bytes,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,elapsed_seconds=time.monotonic()-START,survey_Source_pin=pin(Path(__file__)),all_current_selected_package_Source_pins=packages,current_v13_host_freeze_pin=seen[str(groups['current_v13_HF_and_Source']/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json')],current_v13_complete_direct354_dependency_pins=hf['dependencies'],current_v13_actual_summary_pin=seen[str(ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261013-v13/Root_actual_three_plane_engineering_summary.json')],direct_current_gate_membership=gate_membership,all_typed_target_pin_occurrences_in_selected_Source_JSON=occurrences,all_exact_target_path_occurrences_in_selected_Source_JSON=all_json_occurrences,previous_explicitly_protected_target_pins=old_protected,previous_explicit_protection_roles=old_roles,previous_protected_manifest_pin=seen[str(REC/'storage_release_old_v10_single_PROJECT_source_v3_20261013/EXACT_SINGLE_OLD_V10_PRIVATE_PROJECT_RELEASE_MANIFEST.json')],historical_protection_not_silently_reduced=True,finite_input_tables_role='immutable past finite observation/replay evidence; bundle explicitly states not a new business dependency graph; releasing raw PROJECT invalidates exact old fixture/raw-tree replay, not recorded finite exit0 or science qualification',old_failed_branch_evidence=old_branches,Root_current_Source_writer_and_review_pins=[seen[str(p)]for p in root_sources],Root_Source_exact_target_path_mentions=root_source_text_mentions,Root_future_v14_paths_currently_present=future_v14_paths,future_v14_dependency_absence_or_qualification_proven=False,current_same_pass_storage_budget_and_conditional_release_prediction=budget,release_requires_future_final_v14_exact_DAG_disjointness_and_new_current_pins=True,release_requires_Root_actual_no_writer_or_open_handle_gate=True,release_requires_exact_two_named_owned_nlink1_unlink_and_protected_recheck=True,current_v13_failure_partial_Q_MAC_and_all299_outputs_retained=True,all_old_result_docs_logs_v12_memory_journal_curves_and_scientific_inputs_preserved=True,engineering_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
HERE.mkdir(exist_ok=True)
with(HERE/'REVIEW.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
txt='只读 v11 / v12 私有 PROJECT 释放候选调查\n\n每个候选 749355952 字节，合计 '+str(bytes_pair)+' 字节。仅候选，未删除。\n当前 v13 354 直接依赖、实际 fixed、saved full370 当前/科学集合、material v7 三个 Host、GENDF v4、独立参考计划均无候选直接必需行。\n旧 v10 清理历史曾显式保留两文件，v12 整目录属于曲线证据；本报告没有静默改减该保护。finite 记录中的候选属于已完成观察/旧原始回放证据；释放会丢失旧 PROJECT/GLOBAL 全树与旧 finite fixture 的精确路径回放，保留真实结果和曲线。\n同一不跟随符号链接遍历：全部 ART '+str(totals['all_ART_regular_bytes'])+' 字节 / '+str(totals['all_ART_regular_files'])+' 常规文件；原轴向家族 '+str(totals['axial_family_regular_bytes'])+' 字节。\n当前扣除原 cold、64MiB metadata、完整 2GiB 新输出预留后剩余 '+str(remaining)+' 字节；若未来严格释放两文件，预测剩余 '+str(remaining+bytes_pair)+' 字节。预测不是已释放或业务准入。\n仍须最终 v14 冻结依赖独立审查、Root 真实无写者/无打开句柄、精确候选身份与保留集合重查及真实删除回执。没有请求进程权限，没有证明无打开句柄。v13 的 Q/MAC 和全部 299 输出保留；所有物理/AAA/ABA 准入仍未通过。\n'
with(HERE/'REPORT.txt').open('x')as f:f.write(txt);f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=report['status'],review_pin=pin(HERE/'REVIEW.json'),report_pin=pin(HERE/'REPORT.txt'),candidate_pins=target_rows,budget=budget,typed_target_occurrences=len(occurrences),SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,elapsed_seconds=time.monotonic()-START),allow_nan=False))
