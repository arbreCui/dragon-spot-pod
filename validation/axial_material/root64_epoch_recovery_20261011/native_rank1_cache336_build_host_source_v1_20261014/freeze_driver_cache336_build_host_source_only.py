#!/usr/bin/env python3
"""Freeze Source-only Driver37 build after exact independent Source review."""
import argparse
import ast
import importlib.util
import json
from pathlib import Path
import stat

R=Path('/Users/wen/spot')
REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
HERE=Path(__file__).resolve().parent
HF=HERE/'COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_BUILD_HOST_SOURCE_FREEZE.json'
CLI=HERE/'ROOT_REVIEWABLE_EXACT_CACHE336_DRIVER_BUILD_ARGV.json'

def found(data,pin):
    if isinstance(data,dict):
        return data==pin or any(found(v,pin) for v in data.values())
    return isinstance(data,list) and any(found(v,pin) for v in data)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--peer-review',required=True)
    ap.add_argument('--peer-true-tools',required=True)
    a=ap.parse_args()
    spec=importlib.util.spec_from_file_location('cache336_source_only_helpers',REC/'prepare_native_rank1_cache336_source_v1_20261014.py')
    s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
    def load(path,wanted=None):
        raw,pin=s.read(path)
        if wanted is not None and pin!=wanted:
            raise RuntimeError('exact metadata/Source fullEOF pin required')
        return json.loads(raw),pin
    def typed0(actual):
        return type(actual.get('exit_code')) is int and actual['exit_code']==0 and actual.get('session_id') is None
    def true_review(receipt,review_pin):
        actual=receipt['actual_review_return']
        lines=[v for v in actual['output'].splitlines() if v.strip()]
        if receipt.get('observed_closed') is not True or not typed0(actual) or not lines or json.loads(lines[-1]).get('review_pin')!=review_pin:
            raise RuntimeError('genuine independent closed tool integer0/output exact review pin')
    if HF.exists() or CLI.exists():
        raise RuntimeError('once fresh freeze/interface, no overwrite')
    plan,pplan=load(HERE/'EXACT_COMPACT70_TO_CACHE336_DRIVER_BUILD_PLAN.json')
    ready,pready=load(HERE/'SOURCE_ONLY_READY.json')
    raw,host=s.read(ready['Host_pin']['path'])
    if host!=ready['Host_pin'] or plan['Source_Host_pin']!=host:
        raise RuntimeError('own exact Host Source selection')
    ast.parse(raw)
    if Path(plan['planned_output_root']).exists():
        raise RuntimeError('actual build output must be absent during Source freeze')
    inverse,pinverse=load(ready['whole_byte_inverse_pin']['path'],ready['whole_byte_inverse_pin'])
    recovered=raw.decode().splitlines(keepends=True)
    for block in reversed(inverse['blocks']):
        i=block['new_start_line'];new=block['new'].splitlines(keepends=True)
        if recovered[i:i+len(new)]!=new:
            raise RuntimeError('exact Host positional whole-byte inverse')
        recovered[i:i+len(new)]=block['old'].splitlines(keepends=True)
    oldraw,oldhost=s.read(inverse['original_host_pin']['path'])
    if ''.join(recovered).encode()!=oldraw or oldhost!=inverse['original_host_pin']:
        raise RuntimeError('Host inverse whole old build4 Source recovery')
    review,pr=load(a.peer_review);true,pt=load(a.peer_true_tools)
    if not review.get('status','').startswith('PASS') or review.get('failure') is not None or review.get('source_only') is not True or review.get('compiler_executed') is not False or review.get('numerical_executed') is not False:
        raise RuntimeError('independent Source-only review PASS required')
    true_review(true,pr)
    own=[host,pplan,pready,pinverse,s.read(__file__)[1],ready['preparer_pin'],
      s.read(HERE/'TRUE_TOOL_RETURNS.json')[1]]
    for row in own:
        if not found(review,row):
            raise RuntimeError('independent review must bind every exact own Host/plan/inverse/freezer Source')
    sf,psf=load(plan['selected_new_Fortran_Source_freeze_path'])
    if sf['schema']!='COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_AND_CONTROL_SOURCE_ONLY_FREEZE_V1' or \
       sf['source_only'] is not True or sf['compiled'] is not False or sf['numerical_executed'] is not False or \
       sf['Driver_single_literal_368_to336'] is not True or sf['public_Driver_ABI_unchanged'] is not True or \
       sf['original_math_modified'] is not False:
        raise RuntimeError('exact reviewed one-literal Fortran/math Source freeze')
    old,pold=load(plan['original_actual_complete70_report_pin']['path'],plan['original_actual_complete70_report_pin'])
    oldhf,poldhf=load(plan['selected_previous_complete70_Host_freeze_pin']['path'],plan['selected_previous_complete70_Host_freeze_pin'])
    oldsf,poldsf=load(plan['selected_previous_compact_Fortran_Source_freeze_pin']['path'],plan['selected_previous_compact_Fortran_Source_freeze_pin'])
    oldcli,poldcli=load(REC/'bq64_compact_expected_build_host_source_v4_20261013/ROOT_REVIEWABLE_EXACT_BUILD_ARGV.json')
    root_tools,proot=load(REC/'ROOT_ACTUAL_COMPACT_BQ_BUILD_V4_TRUE_TOOL_RETURNS_20261013.json')
    oldpost,poldpost=load(REC/'independent_bq64_compact_build_v4_actual_postverify_20261013/REVIEW.json')
    oldposttools,poldposttools=load(REC/'independent_bq64_compact_build_v4_actual_postverify_20261013/TRUE_TOOL_RETURNS.json')
    if not typed0(root_tools['actual_terminal_return']) or oldpost['actual_build_report_pin']!=pold or \
       oldpost['actual_build_true_tool_return_pin']!=proot or \
       oldpost['failure'] is not None or oldpost['actual_genuine_terminal_integer_exit_code']!=0 or \
       oldpost['actual_stage_count']!=2 or old['actual_host_Source_freeze_pin']!=poldhf or \
       old['actual_new_Source_freeze_pin']!=poldsf:
        raise RuntimeError('genuine actual compact70 predecessor and exact selected freezes')
    true_review(oldposttools,poldpost)
    common,pcommon=load(plan['selected_new_Common_Source_freeze_pin']['path'],plan['selected_new_Common_Source_freeze_pin'])
    rows=oldhf['dependencies']+[poldhf,poldsf,poldcli,pold,proot,poldpost,poldposttools]+old['fixed_current_pins']+old['output_pins']+own+[pr,pt,psf,pcommon]+sf['files']+sf['original_source_pins']+sf['exact_source_evidence_pins']+common['files']+common['original_source_metadata_pins']
    table={}
    for row in rows:
        if row['path'] in table and table[row['path']]!=row:
            raise RuntimeError('inconsistent complete inherited Source pin')
        table[row['path']]=row
    rows=list(table.values())
    # Exact inherited SHA authority is its already passed freeze/postverification.
    # Only current7 is reobserved here, avoiding another scientific-input EOF sweep.
    for row in rows:
        st=Path(row['path']).lstat()
        if not stat.S_ISREG(st.st_mode) or s.identity(st)!=row['identity']:
            raise RuntimeError('inherited/own current7 changed: '+row['path'])
    production=[row for row in sf['files'] if Path(row['path']).name=='SPOT_GLOBAL_NATIVE_DRIVER64.f']
    if len(production)!=1:
        raise RuntimeError('exact single new Driver Source')
    data=dict(schema='COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_BUILD_HOST_SOURCE_ONLY_FREEZE_V1',
      status='COMPLETE_REVIEWED_DRIVER37_BUILD_HOST_SOURCE_ONLY_FROZEN',compiler_executed=False,
      numerical_executed=False,Host_imported_or_executed=False,host_source=host,build_plan_pin=pplan,
      dependencies=rows,selected_original_actual_complete70_report_pin=pold,
      selected_new_Fortran_Source_freeze_pin=psf,selected_previous_complete70_Host_freeze_pin=poldhf,
      selected_previous_compact_Fortran_Source_freeze_pin=poldsf,
      selected_new_Common_Source_freeze_pin=pcommon,final_independent_Host_Source_review_pin=pr,
      final_independent_Host_Source_true_tool_return_pin=pt,new_production_Fortran_Source_pin=production[0],
      replacement_zero_based_complete70_input_index=37,original_other69_inputs_and_four_archive_order_preserved=True,
      all_current9_core_unchanged=True,retained_current_BOOTQ_zero_based_index=40,
      retained_math_SPOT1P64_zero_based_index=57,original_caps=plan['original_caps'],
      planned_output_root=plan['planned_output_root'],future_actual_object_pin=None,
      future_actual_Dragon_pin=None,future_actual_build_report_pin=None,
      inherited_dependencies_current7_reobserved=True,scientific_EOF_not_repeated=True,
      source_guard_actual_runtime_full_verification_required=True,compile_qualified=False,
      new_cache_budget_control_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False)
    phf=s.put(HF,data)
    argv=list(oldcli['argv'][:12])
    if len(argv)!=12 or argv[-2:]!=['-B',oldhf['host_source']['path']] or \
       argv[:9]!=['/usr/bin/env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1',
         'OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1',
         'VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1']:
        raise RuntimeError('exact original explicit thread1/no bytecode/no optimize interpreter prefix')
    argv[-1]=host['path']
    for name,pin in [('original70',pold),('source-freeze',psf),('host-freeze',phf)]:
        argv+=['--'+name+'-summary',pin['path'],'--'+name+'-sha256',pin['sha256'],
          '--'+name+'-seven-id',json.dumps(pin['identity'],separators=(',',':'))]
    pcl=s.put(CLI,dict(schema='ROOT_REVIEWABLE_EXACT_CACHE336_DRIVER37_BUILD_ARGV_V1',argv=argv,
      mandatory_external_bindings=dict(original70=pold,source_freeze=psf,host_freeze=phf),
      compiler_executed=False,numerical_executed=False,requires_host_process_metadata_access=True,
      initial_history_cold_meta_fullfresh2_admission_required=True,physics_qualified=False))
    print(json.dumps(dict(status='SOURCE_ONLY_DRIVER336_BUILD_HOST_HF_CLI_CLOSED0',
      host_freeze_pin=phf,CLI_pin=pcl,dependencies=len(rows)),ensure_ascii=False),flush=True)

if __name__=='__main__':
    main()
