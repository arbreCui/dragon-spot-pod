#!/usr/bin/env python3
"""Create current Source-only bindings; do not inherit past execution qualification."""
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import sys
import time
sys.dont_write_bytecode=True
ROOT=Path('/Users/wen/spot');V=ROOT/'validation/axial_material';ART=ROOT/'validation/artifacts'
BASE=V/'complete_history_root_index_source_v15_20261010'
REC=V/'native_frame_encoder_epoch_recovery_20261011'
D=BASE/'actual_frame_encoder_current_epoch_monitor_controls_sources_20261011'
E=BASE/'actual_frame_encoder_current_epoch_monitor_controls_receipts_20261011'
OUT=ART/'axial-material-frame-encoder-current-epoch-binding-20261011'
OLD=BASE/'actual_invalid_prepost_d19_monitor_controls_sources_20261011/Root_fresh_frame_controls_Source_binding.json'
sys.path.insert(0,str(V))
from run_real64_common_rank2_training import TrainingResources
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)

def main():
    start=time.monotonic()
    if any(p.exists()or p.is_symlink()for p in(D,E,OUT)):raise RuntimeError('fresh namespaces required')
    guard=TrainingResources(OUT)
    def budget():
        if time.monotonic()-start>=600 or resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20:raise RuntimeError('original metadata600/SELF512 cap')
    def pin(p):
        budget();p=Path(p);s=p.lstat();ident=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
        h=hashlib.sha256()
        with p.open('rb')as f:
            for b in iter(lambda:f.read(1024*1024),b''):h.update(b);budget()
            s2=os.fstat(f.fileno())
        after=p.lstat()
        for item in(s2,after):
            if [item.st_dev,item.st_ino,item.st_mode,item.st_nlink,item.st_size,item.st_mtime_ns,item.st_ctime_ns]!=ident:raise RuntimeError('Source changed during EOF')
        return dict(path=str(p),sha256=h.hexdigest(),size_bytes=ident[4],identity=ident)
    def write(p,d):
        with p.open('x')as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    def check():
        r=guard.check()
        if r['complete_history']['artifact_bytes']+20971764748+64*2**20>=96*2**30:raise RuntimeError('original cold reserve/history scope')
        if r['fresh_output']['disk_free_bytes']-20971764748-2*2**30<8*2**30:raise RuntimeError('original free/reserve scope')
        return r
    before=check();old_pin=pin(OLD);old=json.loads(OLD.read_text());oldbase=json.loads(Path(old['original_N9_controls_Source_binding_pin']['path']).read_text())
    rp=pin(REC/'ACTUAL_N9_21_AUTHOR_SOURCE_RECOVERY.json');recovery=json.loads(Path(rp['path']).read_text())
    if recovery['missing_exact_roles'] or len(recovery['roles'])!=21:raise RuntimeError('all original author roles required')
    D.mkdir();E.mkdir();OUT.mkdir()
    author={};lineage=[]
    for row in recovery['roles']:
        actual=row['recovered_current_pin']
        if pin(actual['path'])!=actual:raise RuntimeError('recovered current author pin changed')
        dest=D/'original_author_sources'/row['role']/Path(actual['path']).name;dest.parent.mkdir(parents=True)
        shutil.copyfile(actual['path'],dest);new=pin(dest)
        if new['sha256']!=row['historical_original_pin']['sha256']or new['size_bytes']!=row['historical_original_pin']['size_bytes']:raise RuntimeError('full author bytes differ')
        author[row['role']]=new
        lineage.append(dict(role=row['role'],historical_pin=row['historical_original_pin'],actual_recovered_pin=actual,new_current_pin=new))
    adapter=D/'fresh_frame_observation_adapter.py';entry=D/'fresh_frame_genuine_controls.py'
    shutil.copyfile(REC/'fresh_frame_observation_adapter.py',adapter)
    shutil.copyfile(REC/'new_genuine_controls.py',entry)
    adapter_pin=pin(adapter);entry_pin=pin(entry)
    if adapter_pin['sha256']!='70d2a5abb8379e825d186b933ac4a55c7434b90984f9ca89c23dc442c8e857af'or entry_pin['sha256']!='05adf2836e260c56e5ab2b39ee146eae1e1c2082b1a7843f0a59f7f191c5ffe6':raise RuntimeError('actual independently reviewed Source bytes required')
    tools={}
    for role,p in oldbase['tool_pins'].items():
        current=pin(p['path'])
        if current['sha256']!=p['sha256']or current['size_bytes']!=p['size_bytes']:raise RuntimeError('original OS tool bytes changed')
        tools[role]=current
    stdlib=pin(oldbase['actual_stdlib_subprocess_Source_pin']['path'])
    if stdlib['sha256']!=oldbase['actual_stdlib_subprocess_Source_pin']['sha256']:raise RuntimeError('original stdlib Source differs')
    base=dict(schema='ROOT_ACTUAL_N8_MONITOR_CONTROLS_SOURCE_BINDING_V1',source_only=True,
        actual_author_Source_contract=author,actual_stdlib_subprocess_Source_pin=stdlib,
        tool_pins=tools,original_caps=CAPS,actual_control_execution=None,
        actual_monitor_controls_qualification=None,actual_native_or_scientific_qualification=None,
        scientific_qualification_created=False,old_qualification_inherited=False,
        current_binding_derivation='new full EOF pins for exactly preserved original Source bytes',
        historical_original_binding_current_pin=pin(old['original_N9_controls_Source_binding_pin']['path']),
        actual_same_byte_recovery_report_pin=rp,complete_Source_lineage=lineage)
    base_path=D/'Root_current_original_N9_Source_only_binding.json';write(base_path,base)
    order=old['case_execution_order'];namespaces={}
    for case in order:
        prefix='axial-material-frame-encoder-current-epoch-'+case+'-20261011'
        ns={k:str(ART/(prefix+'-'+suffix))for k,suffix in [('host','host'),('output','output'),('control','control')]}
        ns.update(source=str(D),receipts=str(E))
        if any(Path(ns[k]).exists()for k in('host','output','control')):raise RuntimeError('fresh case HOC required')
        namespaces[case]=ns
    binding=dict(schema='ROOT_FRESH_FRAME_MONITOR_CONTROLS_SOURCE_BINDING_V1',source_only=True,
        policy=old['policy'],original_caps=CAPS,actual_control_execution=None,
        old_controls_qualification_inherited=False,adapter_Source_pin=adapter_pin,
        control_entry_Source_pin=entry_pin,original_N9_controls_Source_binding_pin=pin(base_path),
        owner_helper_Source_pin=author['owner_scope_helper'],actual_stdlib_subprocess_Source_pin=stdlib,
        tool_pins=tools,case_namespaces=namespaces,case_execution_order=order,
        all_actual_cases_serial=True,shared_new_Source_and_receipts_frozen_before_any_case=True,
        original_caps_changed=False,Native_or_scientific_qualification_created=False,
        historical_d19_binding_current_pin=old_pin,
        actual_pure_review_current_pin=pin(REC/'ACTUAL_PURE_SERIALIZATION_REVIEW.json'),
        actual_independent_encoder_review_current_pin=pin(REC/'INDEPENDENT_ENCODER_REVIEW.json'),
        current_device_observed_not_normalized=True)
    bp=D/'Root_current_fresh_frame_controls_Source_binding.json';write(bp,binding)
    after=check()
    ledger=dict(schema='ACTUAL_CURRENT_MONITOR_SOURCE_BINDING_INSTALL_V1',source_only=True,
        current_binding_pin=pin(bp),original21_roles_preserved=True,
        old_binding_modified=False,old_qualification_inherited=False,
        actual_control_execution=None,actual_PS_lsof_or_compiler_executed=False,
        resources_before=before,resources_after=after,
        wall_seconds=time.monotonic()-start,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    write(OUT/'Root_actual_current_Source_binding_install.json',ledger)
    print(json.dumps(dict(status='CURRENT_SOURCE_ONLY_BINDING_CREATED_INDEPENDENT_PRELAUNCH_REQUIRED',binding_pin=pin(bp),source=str(D),receipts=str(E),control_execution=False)))

if __name__=='__main__':main()
