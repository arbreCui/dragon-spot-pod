#!/usr/bin/env python3
"""Source-only bit Host freeze: inherit every preceding current Source pin."""
import argparse
import ast
import importlib.util
import json
from pathlib import Path
import stat

R=Path('/Users/wen/spot')
REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
HERE=Path(__file__).resolve().parent
HF=HERE/'COMPLETE_CONTROL_HOST_SOURCE_FREEZE.json'
CLI=HERE/'DECLARED_EXECUTION_INTERFACE.json'

def found(data,pin):
    if isinstance(data,dict):return data==pin or any(found(v,pin) for v in data.values())
    return isinstance(data,list) and any(found(v,pin) for v in data)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--peer-review',required=True)
    ap.add_argument('--peer-true-tools',required=True)
    a=ap.parse_args()
    spec=importlib.util.spec_from_file_location('cache336_Source_only_pin_helpers',REC/'prepare_native_rank1_cache336_source_v1_20261014.py')
    s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
    def load(path,wanted=None):
        raw,pin=s.read(path)
        if wanted is not None and pin!=wanted:raise RuntimeError('exact fullEOF Source metadata PF')
        return json.loads(raw),pin
    if HF.exists() or CLI.exists():raise RuntimeError('once new Source freeze/CLI, no overwrite')
    plan,pplan=load(HERE/'EXACT_CONTROL_HOST_SOURCE_ONLY_PLAN.json')
    ready,pready=load(HERE/'SOURCE_ONLY_READY.json')
    raw,host=s.read(ready['Host_pin']['path'])
    if host!=ready['Host_pin'] or host!=plan['Source_Host_pin'] or plan['kind']!='cache336' or \
       plan['source_only'] is not True or plan['compiler_executed'] is not False or plan['numerical_executed'] is not False:
        raise RuntimeError('own exact Source-only Host/plan selection')
    ast.parse(raw)
    if Path(plan['planned_output_root']).exists():raise RuntimeError('actual bit control OUT must remain absent')
    for key in ('future_actual_new_build70_report_pin','future_actual_control_object_pin',
                'future_actual_control_executable_pin','future_actual_control_report_pin'):
        if key not in plan or plan[key] is not None:raise RuntimeError('explicit unknown future actual pins')
    inverse,pinverse=load(ready['inverse_pin']['path'],ready['inverse_pin'])
    recovered=raw.decode().splitlines(keepends=True)
    for block in reversed(inverse['blocks']):
        i=block['new_start_line'];new=block['new'].splitlines(keepends=True)
        if recovered[i:i+len(new)]!=new:raise RuntimeError('exact positional inverse')
        recovered[i:i+len(new)]=block['old'].splitlines(keepends=True)
    oldraw,oldhost=s.read(inverse['original_host_pin']['path'])
    if ''.join(recovered).encode()!=oldraw or oldhost!=inverse['original_host_pin']:
        raise RuntimeError('whole original model5 Host bytes recovered')
    review,pr=load(a.peer_review);receipt,pt=load(a.peer_true_tools)
    if not review.get('status','').startswith('PASS') or review.get('failure') is not None or \
       review.get('source_only') is not True or review.get('compiler_executed') is not False or review.get('numerical_executed') is not False:
        raise RuntimeError('genuine independent exact Source-only review')
    actual=receipt['actual_review_return'];lines=[v for v in actual['output'].splitlines()if v.strip()]
    if receipt.get('observed_closed') is not True or type(actual.get('exit_code')) is not int or \
       actual['exit_code']!=0 or actual.get('session_id') is not None or not lines or json.loads(lines[-1]).get('review_pin')!=pr:
        raise RuntimeError('true independent closed integer0/no session/exact output review PF')
    own=[host,pplan,pready,pinverse,ready['preparer_pin'],s.read(__file__)[1],s.read(HERE/'TRUE_TOOL_RETURNS.json')[1]]
    for row in own:
        if not found(review,row):raise RuntimeError('review must bind each exact own Source/preparer/freezer/tool PF')
    bhf,pbhf=load(plan['selected_new_build_Host_freeze_pin_path'])
    sf,psf=load(plan['selected_new_Fortran_Source_freeze_pin_path'])
    if bhf['schema']!='COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_BUILD_HOST_SOURCE_ONLY_FREEZE_V1' or \
       any(bhf.get(k)is not False for k in ('compiler_executed','numerical_executed','Host_imported_or_executed')) or \
       bhf['selected_new_Fortran_Source_freeze_pin']!=psf or \
       sf['schema']!='COMPLETE_NATIVE_RANK1_CACHE336_DRIVER_AND_CONTROL_SOURCE_ONLY_FREEZE_V1' or \
       sf['source_only'] is not True or sf['compiled'] is not False or sf['numerical_executed'] is not False or \
       sf['new_control_expected_assertions']!=338 or sf['new_control_expected_calls']!=121 or \
       plan['control_Source_pin'] not in sf['files'] or plan['production_Source_pin'] not in sf['files'] or \
       plan['unchanged_math_Source_pin'] not in sf['original_source_pins']:
        raise RuntimeError('exact selected new Driver HostHF and shared reviewed Fortran/control SF')
    if psf not in bhf['dependencies']:raise RuntimeError('selected Driver HostHF itself binds exact Fortran SF')
    predecessor,ppred=load(plan['current_unchanged_model5_Host_freeze_pin']['path'],plan['current_unchanged_model5_Host_freeze_pin'])
    common,pcommon=load(plan['selected_new_Common_Source_freeze_pin']['path'],plan['selected_new_Common_Source_freeze_pin'])
    previous_bit,previous_bit_pin=load(plan['predecessor_bit_Host_freeze_pin']['path'],plan['predecessor_bit_Host_freeze_pin'])
    previous_cli,previous_cli_pin=load(plan['predecessor_bit_CLI_pin']['path'],plan['predecessor_bit_CLI_pin'])
    rows=(previous_bit['dependencies']+[previous_bit_pin,previous_cli_pin]+bhf['dependencies']+predecessor['dependencies']+[pbhf,psf,ppred,pr,pt,pcommon]+own+
      sf['files']+sf['original_source_pins']+sf['exact_source_evidence_pins']+common['files']+common['original_source_metadata_pins']+
      [plan['current_predecessor_build_plan_pin'],plan['unchanged_math_object_pin'],plan['original_common_Source_pin']])
    table={}
    for row in rows:
        if row['path'] in table and table[row['path']]!=row:raise RuntimeError('inconsistent complete current Source PF')
        table[row['path']]=row
    rows=list(table.values())
    for row in rows:
        st=Path(row['path']).lstat()
        if not stat.S_ISREG(st.st_mode) or s.identity(st)!=row['identity']:
            raise RuntimeError('complete inherited/own current7 changed: '+row['path'])
    data=dict(schema='COMPLETE_NATIVE_RANK1_CACHE336_BUDGET_BIT_CONTROL_HOST_SOURCE_ONLY_FREEZE_V1',
      status='COMPLETE_REVIEWED_SOURCE_ONLY_CACHE336_BUDGET_BIT_HOST_FROZEN',compiler_executed=False,
      numerical_executed=False,Host_imported_or_executed=False,host_source=host,control_host_plan_pin=pplan,
      dependencies=rows,selected_new_build_Host_freeze_pin=pbhf,selected_new_Fortran_Source_freeze_pin=psf,
      selected_control_Source_freeze_pin=psf,selected_new_Common_Source_freeze_pin=pcommon,
      selected_unchanged_math_object_pin=plan['unchanged_math_object_pin'],
      selected_unchanged_math_Source_pin=plan['unchanged_math_Source_pin'],
      selected_control_Fortran_Source_pin=plan['control_Source_pin'],
      final_independent_Host_Source_review_pin=pr,final_independent_Host_Source_true_tool_return_pin=pt,
      current_predecessor_model5_Host_freeze_pin=ppred,original_caps=plan['original_caps'],
      original_aux_cap_bytes=128*2**20,original_pending_metadata_bytes=8*2**20,
      original301_assertions_preserved=True,expected_actual_assertions=338,expected_actual_SPOT1P64_calls=121,
      math_module_recompiled=False,expected_guarded_stage_count=3,planned_output_root=plan['planned_output_root'],
      future_actual_new_build70_report_pin=None,future_actual_control_report_pin=None,
      inherited_current7_reobserved=True,science_EOF_not_repeated=True,
      component_only=True,reader_qualified=False,physics_qualified=False,GLOBAL_qualified=False,goal_complete=False)
    phf=s.put(HF,data)
    prefix=['/usr/bin/env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1',
      'OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1',
      'VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1',
      '/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',host['path']]
    pcl=s.put(CLI,dict(schema='DECLARED_CACHE336_BUDGET_BIT_CONTROL_EXECUTION_INTERFACE_V1',
      python_environment_and_Host_prefix=prefix,required_external_prefixes=['new-build70','source-freeze','host-freeze'],
      required_external_suffixes=['summary','sha256','seven-id'],
      mandatory_source_bindings=dict(source_freeze=psf,host_freeze=phf),
      future_actual_new_build70_report_pin=None,required_actual_new_build70_report_path=plan['new_build_expected_report_path'],
      planned_total_argv_count=30,compiler_executed=False,numerical_executed=False,
      requires_host_process_metadata_access=True,initial_fullfresh2_cold_meta_history96_reserve_required=True,
      physics_qualified=False))
    print(json.dumps(dict(status='SOURCE_ONLY_CACHE336_BIT_HOST_HF_CLI_CLOSED0',
      host_freeze_pin=phf,CLI_pin=pcl,dependencies=len(rows)),ensure_ascii=False),flush=True)

if __name__=='__main__':main()
