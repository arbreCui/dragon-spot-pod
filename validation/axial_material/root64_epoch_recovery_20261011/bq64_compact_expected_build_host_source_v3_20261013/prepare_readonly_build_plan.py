#!/usr/bin/env python3
"""Prepare an exact Source-only relink plan; never import the new Host/Fortran."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

R=Path('/Users/wen/spot')
REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
HERE=Path(__file__).resolve().parent
TARGET=HERE/'EXACT_ORIGINAL70_TO_COMPACT_BQ64_BUILD_PLAN.json'
host_tree=ast.parse((HERE/'build_bq64_compact_expected_runtime.py').read_bytes())
out_node=next(n for n in host_tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='OUT'for t in n.targets))
OUT=R/ast.literal_eval(out_node.value.right)

def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def read(path,want=None,body=False):
    path=Path(path)
    before=identity(path.lstat())
    if not stat.S_ISREG(before[2]):raise RuntimeError('regular input required')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        if identity(os.fstat(fd))!=before:raise RuntimeError('opened7ID differs')
        sha=hashlib.sha256();pieces=[] if body else None
        while True:
            block=os.read(fd,2**20)
            if not block:break
            sha.update(block)
            if body:pieces.append(block)
        if identity(os.fstat(fd))!=before:raise RuntimeError('EOF7ID differs')
    finally:os.close(fd)
    if identity(path.lstat())!=before:raise RuntimeError('after7ID differs')
    row=dict(path=str(path),sha256=sha.hexdigest(),size_bytes=before[4],identity=before)
    if want is not None and row!=want:raise RuntimeError('exact bound input differs: '+str(path))
    return row,b''.join(pieces) if body else None

def main():
    if TARGET.exists() or OUT.exists() or OUT.is_symlink():raise RuntimeError('fresh plan/business namespace only')
    cli_pin,cli_raw=read(REC/'ROOT_EXACT_ACTUAL_PIPELINE_V14_ARGV_20261013.json',body=True)
    cli=json.loads(cli_raw)
    old_pin,old_raw=read(cli['mandatory_external_bindings']['build70']['path'],
                         cli['mandatory_external_bindings']['build70'],True)
    old=json.loads(old_raw)
    if old['schema']!='ACTUAL_NATIVE_RANK1_EXACT_BLOCK_CACHE_COMPLETE70_BUILD_ONLY_V2' or \
       old['status']!='ACTUAL_TWO_CACHE_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY' or \
       old['failure'] is not None or old['after_check_error'] is not None or \
       old['Dragon_linked'] is not True or old['final_report_resource_check_passed'] is not True or \
       len(old['records'])!=3:raise RuntimeError('exact actual closed old70 schema')
    original=old['records'][-1]['command'];ordered=original[3:-2]
    if ordered!=old['actual_complete70_link_inputs'] or len(ordered)!=70 or len(set(ordered))!=70 or \
       sum(p.endswith('.o')for p in ordered)!=66 or sum(p.endswith('.a')for p in ordered)!=4 or \
       [i for i,p in enumerate(ordered)if Path(p).name=='SPOR64_BOOTQ64.o']!=[40]:
        raise RuntimeError('exact actual70 and sole BOOTQ40 required')
    table={}
    for row in old['fixed_current_pins']+old['output_pins']:
        if row['path'] in table and table[row['path']]!=row:raise RuntimeError('inconsistent old70 full pins')
        table[row['path']]=row
    ordered_pins=[read(p,table[p])[0]for p in ordered]
    binding_path=REC/'current_mount_full_identity_common_source_v1/CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json'
    binding_pin,binding_raw=read(binding_path,body=True);binding=json.loads(binding_raw)
    old9=[]
    for prior in binding['seventeen_required_same_production_object_pins']:
        now=table[prior['path']]
        if prior['sha256']!=now['sha256'] or prior['size_bytes']!=now['size_bytes'] or prior['identity'][1:]!=now['identity'][1:]:
            raise RuntimeError('old9 byte and six-field current identity differs')
        if prior['identity'][0] not in (16777229,16777234) or now['identity'][0]!=16777229:
            raise RuntimeError('only explicit current mount device29/old34 identity view')
        read(now['path'],now);old9.append(now)
    if len(old9)!=9 or old9[5]!=ordered_pins[40]:raise RuntimeError('old core6 equals link40')
    original_q,_=read(REC/'bootstrap_qfiss_source_v2/SPOR64_BOOTQ64.f90')
    original_tree,_=read(REC/'new_source/SPOR64_BOOT64.f90')
    if original_q['sha256']!='7172121d57c3411c62845a81cc41886ee9759d4c168423b13541fc3a91afecd8' or \
       original_tree['sha256']!='cd19000790003d84645ea323ffa95766ba1478230c9c703d32b05b555f1425a7':
        raise RuntimeError('whole original production and comparator Source')
    first=old['records'][0]['command'];compiler=read(first[0],table[first[0]])[0]
    flags=first[1:10];includes=[p for p in first if p.startswith('-I')]
    if flags!=['-O2','-march=native','-ffp-contract=off','-fcheck=all','-fbacktrace','-g','-fPIC','-frecord-marker=4','-ffixed-line-length-none']:
        raise RuntimeError('original compiler flags')
    module_pins=[]
    for folder in includes:
        for path in sorted(Path(folder[2:]).glob('*.mod')):
            row=read(path,table.get(str(path)))[0]
            if row not in module_pins:module_pins.append(row)
    host_pin,host_raw=read(HERE/'build_bq64_compact_expected_runtime.py',body=True)
    tree=ast.parse(host_raw);compile(tree,host_pin['path'],'exec')
    env=['/usr/bin/env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1',
         'OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1']
    plan=dict(schema='EXACT_ORIGINAL70_TO_COMPACT_BQ64_BUILD_SOURCE_ONLY_PLAN_V1',
      source_only=True,compiler_executed=False,numerical_executed=False,new_Host_imported=False,
      original_actual_complete70_report_pin=old_pin,original_v14_exact_argv_provenance_pin=cli_pin,
      original_binding_provenance_pin=binding_pin,original_ordered70_input_pins=ordered_pins,
      original_complete70_link_command=original,original_compile_flags=flags,
      original_compile_include_arguments=includes,original_compile_module_full_EOF_pins=module_pins,
      original_compiler_pin=compiler,original_nine_core_object_pins=old9,original_BOOTQ_object_pin=old9[5],
      original_BOOTQ_Source_pin=original_q,original_BOOT64_Source_pin=original_tree,
      original_caps=old['original_caps'],replacement_zero_based_complete70_input_index=40,
      replacement_one_based_complete70_input_slot=41,replacement_one_based_core9_input_slot=6,
      unchanged_ordered_inputs=69,unchanged_archives=4,unchanged_core_objects=8,
      planned_output_root=str(OUT),planned_new_Source_path=str(REC/'bq64_compact_expected_composed_source_draft_v1_20261013/SPOR64_BOOTQ64.f90'),
      planned_new_Source_freeze_path=str(REC/'bq64_compact_expected_composed_source_draft_v1_20261013/COMPLETE_BQ64_COMPACT_EXPECTED_COMPOSED_SOURCE_FREEZE.json'),
      original_streaming_Common_pin=read(REC/'streaming_full_ledger_serializer_min5_source_bundle_v1_20261013/guarded_warm_A_common.py')[0],
      source_Host_pin_before_freeze=host_pin,host_ast_and_code_compile_only=True,
      actual_new_BOOTQ_object_pin=None,actual_new_Dragon_pin=None,actual_new_build_report_pin=None,
      actual_new_connected17_report_pin=None,actual_new_composed_controls_report_pin=None,
      actual_new_pipeline_report_pin=None,planned_environment=env,
      original17_preserved_as_old_reader_only=True,new_reader_requires_fresh_connected17=True,
      new_reader_requires_fresh_exact_graft_and_full_raw_controls=True,
      pipeline_requires_fresh_control_admission_and_storage_forecast_2032MiB=True,
      initial_original_history_cold_meta_fullfresh_reserve_not_yet_admitted=True,
      compile_qualified=False,new_reader_qualified=False,AAA_qualified=False,ABA_admitted=False)
    with TARGET.open('x',encoding='utf-8')as f:
        json.dump(plan,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    pin=read(TARGET)[0]
    print(json.dumps(dict(status='SOURCE_ONLY_READONLY_EXACT_ORDERED70_BUILD_PLAN_WRITTEN',plan_pin=pin,
      exact_ordered_inputs=len(ordered_pins),module_files=len(module_pins),old_core_inputs=len(old9),
      compiler_executed=False,numerical_executed=False,new_Host_imported=False)))

if __name__=='__main__':main()
