#!/usr/bin/env python3
"""Freeze the reviewed exact build interface; never compile or import its Host."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

R=Path('/Users/wen/spot')
REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
HERE=Path(__file__).resolve().parent
HF=HERE/'COMPLETE_BQ64_COMPACT_EXPECTED_BUILD_HOST_SOURCE_FREEZE.json'
CLI=HERE/'ROOT_REVIEWABLE_EXACT_BUILD_ARGV.json'

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def read(path,wanted=None,body=False):
    path=Path(path);before=identity(path.lstat())
    if not stat.S_ISREG(before[2]):raise RuntimeError('regular Source/evidence required')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        if identity(os.fstat(fd))!=before:raise RuntimeError('opened7ID changed')
        h=hashlib.sha256();chunks=[] if body else None
        while True:
            chunk=os.read(fd,2**20)
            if not chunk:break
            h.update(chunk)
            if body:chunks.append(chunk)
        if identity(os.fstat(fd))!=before:raise RuntimeError('EOF7ID changed')
    finally:os.close(fd)
    if identity(path.lstat())!=before:raise RuntimeError('after7ID changed')
    row=dict(path=str(path),sha256=h.hexdigest(),size_bytes=before[4],identity=before)
    if wanted is not None and row!=wanted:raise RuntimeError('exact Source/evidence pin differs: '+str(path))
    return row,b''.join(chunks)if body else None

def load(path,wanted=None):
    pin,raw=read(path,wanted,True);return json.loads(raw),pin

def unique(rows):
    table={}
    for row in rows:
        if row['path']in table and table[row['path']]!=row:raise RuntimeError('inconsistent complete Source closure')
        table[row['path']]=row
    return list(table.values())

def write(path,data):
    with path.open('x',encoding='utf-8')as f:
        json.dump(data,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())

def main():
    if HF.exists()or CLI.exists():raise RuntimeError('once fresh freeze, no overwrite')
    plan,pplan=load(HERE/'EXACT_ORIGINAL70_TO_COMPACT_BQ64_BUILD_PLAN.json')
    host,raw=read(HERE/'build_bq64_compact_expected_runtime.py',plan['source_Host_pin_before_freeze'],True)
    tree=ast.parse(raw);compile(tree,host['path'],'exec')
    out_node=next(n for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='OUT'for t in n.targets))
    out=R/ast.literal_eval(out_node.value.right)
    if plan['planned_output_root']!=str(out)or out.exists()or out.is_symlink():raise RuntimeError('exact fresh Host/plan output agreement')
    old,pold=load(plan['original_actual_complete70_report_pin']['path'],plan['original_actual_complete70_report_pin'])
    sf,psf=load(plan['planned_new_Source_freeze_path'])
    if sf['schema']!='COMPLETE_BQ64_COMPACT_EXPECTED_COMPOSED_FORTRAN_SOURCE_ONLY_FREEZE_V1'or \
       sf['source_only']is not True or sf['compiled']is not False or sf['numerical_executed']is not False or \
       sf['replacement_zero_based_complete70_index']!=40 or sf['public_BUILD_entire_original_bytes_unchanged']is not True:
        raise RuntimeError('reviewed exact candidate Source-only Fortran freeze')
    parent_hf_path=REC/'aaa_three_plane_streaming_pipeline_source_v14/COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json'
    parent,parent_pin=load(parent_hf_path)
    review_dir=REC/'independent_bq64_compact_build_host_v3_and_public_READ_plan_Source_review_20261013'
    review,review_pin=load(review_dir/'REVIEW.json')
    review_true,review_true_pin=load(review_dir/'TRUE_TOOL_RETURN.json')
    if review_pin['sha256']!='24eeda9b70d5f266871de48e5c2f77af035b06298aa6f154921ed0fa4fa076ce':
        raise RuntimeError('exact independent final Source review')
    rows=unique(parent['dependencies']+[parent_pin,parent['host_source'],host,pplan,psf,pold]+
      old['fixed_current_pins']+old['output_pins']+plan['original_ordered70_input_pins']+
      plan['original_nine_core_object_pins']+plan['original_compile_module_full_EOF_pins']+
      [plan['original_compiler_pin'],plan['original_streaming_Common_pin']]+
      sf['files']+sf['original_source_pins']+[sf['complete_byte_inverse_pin'],sf['control_plan_pin'],
      sf['genuine_public_READ_control_plan_pin'],sf['independent_candidate_source_review_pin'],
      sf['independent_candidate_source_true_tool_return_pin'],sf['Source_pinned_bounded_design_report_pin'],
      sf['Source_pinned_bounded_design_true_tool_return_pin'],sf['preparer_source_pin']]+
      [review_pin,review_true_pin]+[read(p)[0]for p in sorted(HERE.iterdir())if p.is_file()])
    for row in rows:read(row['path'],row)
    current=dict(schema='COMPLETE_BQ64_COMPACT_EXPECTED_BUILD_HOST_SOURCE_ONLY_FREEZE_V1',
      status='COMPLETE_REVIEWED_SOURCE_ONLY_ONE_BOOTQ_BUILD_INTERFACE_FROZEN',
      compiler_executed=False,numerical_executed=False,Host_imported_or_executed=False,
      host_source=host,build_plan_pin=pplan,dependencies=rows,
      selected_original_actual_complete70_report_pin=pold,selected_new_Fortran_Source_freeze_pin=psf,
      final_independent_Host_Source_review_pin=review_pin,final_independent_Host_Source_true_tool_return_pin=review_true_pin,
      new_production_Fortran_Source_pin=next(p for p in sf['files']if p['path']==plan['planned_new_Source_path']),
      replacement_zero_based_complete70_input_index=40,replacement_one_based_old9_core_slot=6,
      original_other69_inputs_and_four_archive_order_preserved=True,
      old17_is_only_old_reader_premise=True,new_reader_requires_fresh_controls=True,
      original_caps=plan['original_caps'],planned_output_root=str(out),
      future_actual_object_pin=None,future_actual_Dragon_pin=None,future_actual_build_report_pin=None,
      compile_qualified=False,new_reader_qualified=False,AAA_qualified=False,ABA_admitted=False)
    write(HF,current);phf=read(HF)[0]
    argv=plan['planned_environment']+['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',host['path']]
    for name,pin in [('original70',pold),('source-freeze',psf),('host-freeze',phf)]:
        argv+=['--'+name+'-summary',pin['path'],'--'+name+'-sha256',pin['sha256'],
               '--'+name+'-seven-id',json.dumps(pin['identity'],separators=(',',':'))]
    write(CLI,dict(schema='ROOT_EXACT_REVIEWABLE_COMPACT_BQ_ONE_OBJECT_ORDERED70_BUILD_ARGV_V1',argv=argv,
      mandatory_external_bindings=dict(original70=pold,source_freeze=psf,host_freeze=phf),
      compiler_executed=False,numerical_executed=False,requires_host_process_metadata_access=True,
      initial_history_cold_meta_fullfresh2_admission_required=True,physics_qualified=False))
    print(json.dumps(dict(status='SOURCE_ONLY_COMPLETE_COMPACT_BQ_BUILD_HOST_FREEZE_AND_ARGV_WRITTEN',
      host_freeze_pin=phf,argv_pin=read(CLI)[0],dependencies=len(rows),compiler_executed=False,numerical_executed=False)))

if __name__=='__main__':main()
