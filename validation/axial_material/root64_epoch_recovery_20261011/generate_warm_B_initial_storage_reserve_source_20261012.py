#!/usr/bin/env python3
"""Prepare an explicitly pinned B host that reserves its output before launch.

No existing result or source is overwritten. All old runtime, physical input,
control and numerical bindings stay exact; the initial admission becomes stricter.
This source-only package cannot start a job while the original budget is full.
"""
import json
from pathlib import Path
from generate_independent_plane3_A_source_20261012 import read,transform

REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=REC/'native_warm_B_bounded_host_source_v1'
OUT=REC/'native_warm_B_initial_storage_reserve_source_v2'

def main():
    assert not OUT.exists()
    original_init='    resources=Resources();before=resources.check()\n'
    new_init=original_init+'''    # Reserve the declared complete fresh 2GiB only at initial admission.
    # During execution, the unchanged history monitor counts actual growth.
    if before['artifact_bytes']+20971764748+64*2**20+2*2**30>=96*2**30:
        raise RuntimeError('history96GiB original cold reserve plus initial fresh2GiB')
'''
    original_admit='    args=parser.parse_args();start=time.monotonic()\n'
    new_admit=original_admit+'''    freeze_path=c.BASE/'COMPLETE_WARM_B_INITIAL_STORAGE_SOURCE_FREEZE.json'
    if Path(args.source_freeze_summary)!=freeze_path:
        raise RuntimeError('exact independent current Source freeze path required')
    source_freeze,source_pin=c.load_json_exact(freeze_path,args.source_freeze_sha256,args.source_freeze_seven_id)
    if source_freeze['schema']!='CURRENT_WARM_B_INITIAL_STORAGE_SOURCE_FREEZE_ONLY_V2':
        raise RuntimeError('exact Source-only freeze schema required')
    source_rows=source_freeze['fixed_source_files']
    source_paths=[Path(r['path'])for r in source_rows]
    required={'guarded_warm_B_common.py','run_current_native_warm_B.py',
              'run_current_warm_B_entry_controls.py','verify_native_B_archive64.f90',
              'COMPLETE_INITIAL_STORAGE_HOST_SOURCE_BYTE_INVERSE.json'}
    if len(set(source_paths))!=len(source_paths) or any(p.parent!=c.BASE for p in source_paths) or not required<=set(p.name for p in source_paths):
        raise RuntimeError('complete exact independent current Source package required')
    c.verify_rows(source_rows)
'''
    sources=[
      transform(OLD/'guarded_warm_B_common.py','guarded_warm_B_common.py',[
        ("BIND = BASE/'CURRENT_WARM_B_COMPLETE_HOST_SOURCE_BINDING.json'",
         "BIND = REC/'native_warm_B_bounded_host_source_v1/CURRENT_WARM_B_COMPLETE_HOST_SOURCE_BINDING.json'",1),
        (original_init,new_init,1)]),
      transform(OLD/'run_current_native_warm_B.py','run_current_native_warm_B.py',[
        ("axial-material-new-REAL64-native-warm-B-20261012-v1",
         "axial-material-new-REAL64-native-warm-B-20261012-v2-initial-storage-reserve",1),
        ("('seventeen','entry-controls')","('seventeen','entry-controls','source-freeze')",1),
        (original_admit,new_admit,1),
        ("    fixed+=[p17,proute]+seventeen['fixed_current_pins']+seventeen['output_pins']+route['fixed_current_pins']+route['output_pins']\n",
         "    fixed+=source_rows+[source_pin,p17,proute]+seventeen['fixed_current_pins']+seventeen['output_pins']+route['fixed_current_pins']+route['output_pins']\n",1)]),
      transform(OLD/'run_current_warm_B_entry_controls.py','run_current_warm_B_entry_controls.py',[]),
      transform(OLD/'verify_native_B_archive64.f90','verify_native_B_archive64.f90',[])]
    OUT.mkdir()
    proofs=[]
    for name,b,proof in sources:
        p=OUT/name
        with p.open('xb') as f:f.write(b)
        _,proof['new_source']=read(p)
        proofs.append(proof)
    _,binding_pin=read(OLD/'CURRENT_WARM_B_COMPLETE_HOST_SOURCE_BINDING.json')
    report=dict(schema='INITIAL_FRESH_OUTPUT_HISTORY_RESERVE_SOURCE_ONLY_V2',sources=proofs,
      unchanged_runtime_and_physical_binding_pin=binding_pin,
      history_cap_bytes=96*2**30,cold_reserve_bytes=20971764748,
      metadata_reserve_bytes=64*2**20,fresh_output_cap_bytes=2*2**30,
      initial_fresh_reservation_once=True,unchanged_actual_growth_monitor_during_execution=True,
      initial_admission_before_runtime_directory_or_business_child=True,
      old_B_failure_preserved=True,automatic_business_retry=False,source_only=True,
      transport_executed=False,B_producer_qualified=False,GLOBAL_qualified=False,
      online_BOOT_qualified=False,AAA_qualified=False,ABA_admitted=False)
    with (OUT/'COMPLETE_INITIAL_STORAGE_HOST_SOURCE_BYTE_INVERSE.json').open('x') as f:
        json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n')
    print(json.dumps(dict(path=str(OUT),source_files=len(sources),source_only=True)))

if __name__=='__main__':main()
