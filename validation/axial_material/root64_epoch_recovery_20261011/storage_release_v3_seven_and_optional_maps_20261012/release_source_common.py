"""Finite protected Source DAG and inventories. No deletion or business launch."""
import importlib.util
import json
import os
from pathlib import Path
import stat
ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts';REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011';PACKAGE=Path(__file__).resolve().parent
PRIOR=REC/'storage_release_source_factor_early_maps_20261012/prepare_or_execute_exact_six_early_maps.py'
spec=importlib.util.spec_from_file_location('retained_previous_release_protection',PRIOR);previous=importlib.util.module_from_spec(spec);spec.loader.exec_module(previous);c=previous.c
FAILED=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v3';FACTOR=ART/'axial-material-production-qualified-AB-source-factor-20261006'
NAMES=['axial_macro.xsm','axial_track.xsm','basis.xsm','global_rcon.xsm','native_A1.xsm','native_A2.xsm','native_A3.xsm']
BATCHES={'failed-v3-seven':dict(branch=FAILED,targets=[FAILED/'AAA'/n for n in NAMES],count=7,bytes=499457228,manifest='EXACT_7_FAILED_V3_INPUT_COPY_MANIFEST.json'), 'optional-map003004-six':dict(branch=FACTOR,targets=sorted(FACTOR/'AAA'/n/f for n in ['map003','map004']for f in ['closed_snapshots.xsm','candidate_snapshots.xsm','candidate_radial.xsm']),count=6,bytes=1427734232,manifest='EXACT_6_OPTIONAL_MAP003004_RAW_MANIFEST.json')}

def inventory(branch):
 files={};links={};dirs={};stack=[branch]
 while stack:
  p=stack.pop();c.ancestors(p);s=p.lstat()
  if not stat.S_ISDIR(s.st_mode):raise RuntimeError('ordinary closed branch directory required')
  dirs[str(p)]=c.identity(s);fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
  try:
   with os.scandir(fd)as entries:
    for entry in entries:
     q=p/entry.name;s=entry.stat(follow_symlinks=False)
     if stat.S_ISDIR(s.st_mode):stack.append(q)
     elif stat.S_ISREG(s.st_mode):files[str(q)]=c.identity(s)
     elif stat.S_ISLNK(s.st_mode):links[str(q)]=dict(identity=c.identity(s),target=os.readlink(q))
     else:raise RuntimeError('unexpected closed branch special file')
  finally:os.close(fd)
  c.guard()
 return dict(ordinary_file_identities=files,symlinks=links,directory_identities=dirs)

def protect():
 old,coverage=previous.protection_and_source_review();table={r['path']:r for r in old};origins=[]
 def add(row):
  row=c.normalize(row);prior=table.get(row['path'])
  if prior is not None and prior!=row:raise RuntimeError('ambiguous mandatory current live pin '+row['path'])
  table[row['path']]=row
 def meta(path,fields=None):
  row=c.pin(path);value=c.read_pinned_json(row);add(row);origins.append(row)
  if fields is None:c.add_nested_pins(value,table)
  else:
   for key in fields:c.add_nested_pins(value[key],table)
  return value,row
 hf,hfp=meta(REC/'aaa_three_plane_streaming_pipeline_source_v4/COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json')
 # The complete actual current pin is discovered below and frozen literally
 # in each manifest. Execution requires Root to select that manifest SHA/7ID.
 if hf['schema']!='COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V4':raise RuntimeError('exact current pipeline4 Source schema')
 build,bp=meta(hf['selected_actual_build69_report']['path'],['fixed_current_pins','output_pins'])
 if bp!=hf['selected_actual_build69_report']or not bp['sha256'].startswith('97e74e')or build['failure']is not None or build['after_check_error']is not None or len(build['records'])!=10 or any(r['status']!='PASS'for r in build['records']):raise RuntimeError('true actual69v4 successful origin')
 sf,sfp=meta(hf['selected_fortran_freeze']['path'])
 if sfp!=hf['selected_fortran_freeze']or sf['source_revision'] is None:raise RuntimeError('true current SF2 exact origin')
 cause,cp=meta(sf['actual_closed_failure_readonly_cause_receipt']['path'],['full_original_Source_pins','actual_signature_records','route_contract_flu_option_declaration_Source_pin'])
 # The failed report is protected as historical evidence; its old owned/input
 # arrays are not new mandatory live pins. The invalid PACK is an explicit
 # retained SF2 causal input and cannot be a release target.
 bad=next(r['full_EOF_pin']for r in cause['actual_signature_records']if r['full_EOF_pin']['path']==str(FAILED/'AAA/initial_pack.xsm'));add(bad)
 meta(REC/'aaa_three_plane_streaming_host_source_v4/COMPLETE_BUILD_HOST_SOURCE_FREEZE.json')
 material=REC/'current_formal_material_authority_source_v1'
 v4,vp=meta(material/'CURRENT_FORMAL_MATERIAL_AUTHORITY_SELECTED_PLAN_V4.json')
 if vp['sha256']!='93dd205dc1e1cdeb7dcc7bb5fd52cad113f01b5e0b82a666fd0ea623a3ad41f7'or v4['current_actual69_build_report_pin']!=bp:raise RuntimeError('stable actual selected material v4 plan')
 for name in ['SELECTED_CURRENT69_V4_PLAN_FULL_BYTE_INVERSE.json','COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json','COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json','CURRENT_FORMAL_COMPLETE_AB_ORIGINAL_MATERIAL_SEED_PLAN_SOURCE_ONLY.json','CURRENT_COMPLETE_MATERIAL_AUTHORITY_ENGINEERING_SOURCE_HANDOFF.json','CURRENT_FORMAL_MATERIAL_AUTHORITY_SOURCE_PLAN.json','CURRENT_SELECTED_ACTUAL_ORIGIN_AND_EXACT_COMPILE_SOURCE_BINDING_REPAIR.json']:
  meta(material/name)
 for p in sorted(material.iterdir()):
  if p.is_file():add(c.pin(p))
 science=REC/'saved_full370_terminal_audit_host_source_v1'
 meta(science/'COMPLETE_SAVED_FULL370_GUARD_HOST_SOURCE_FREEZE.json')
 sci,scirow=meta(science/'CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json')
 if len(sci['science_original_input_pins'])!=1129:raise RuntimeError('entire actual1129 scientific input set required')
 # Original SHA-only Source inverse references are represented by their current
 # metadata file above. Current live compiler Sources come from explicit full
 # pins; no stale coherent before/after pin is promoted from a history report.
 rows=sorted(table.values(),key=lambda r:r['path'])
 for r in rows:c.same(r)
 return rows,dict(prior_current_protection_coverage=coverage,selected_current_metadata_origin_pins=origins,current_pipeline4_host_freeze_pin=hfp,current_actual69v4_report_pin=bp,current_SF2_pin=sfp,current_material_v4_plan_pin=vp,all1129_science_inputs_explicitly_included=True,invalid_v3_PACK_explicit_full_pin_retained=bad,failed_report_owned_copy_arrays_are_historical_only=True,current_mandatory_DAG_fields_not_whole_history_recursion=True)

def disjoint(targets,protected):
 paths={r['path']for r in protected};ids={tuple(r['identity'][:2])for r in protected}
 for r in targets:
  if not stat.S_ISREG(r['identity'][2])or r['identity'][3]!=1 or r['path']in paths or tuple(r['identity'][:2])in ids:raise RuntimeError('target intersects mandatory current Source or physical input')
  c.same(r)

def proof(batch):
 if batch=='failed-v3-seven':
  p=c.pin(FAILED/'Root_actual_three_plane_engineering_summary.json');d=c.read_pinned_json(p)
  if d['status']!='FAILED_UNQUALIFIED_NO_RETRY'or d['failure']!='RuntimeError: exact character record SIGNATURE'or d['actual_terminal']is not None or d['after_check_error']is not None or len(d['records'])!=8:raise RuntimeError('exact closed failed v3 Source-readback outcome')
  pins=[p,c.pin(REC/'ACTUAL_AAA3_PIPELINE_V3_TRUE_CLOSED_TOOL_RETURNS_20261012.json')]
  for r in d['records']:
   wp=FAILED/(r['label']+'.watchdog.json');lp=FAILED/(r['label']+'.log');w=c.read_pinned_json(c.pin(wp));pins.extend([c.pin(wp),c.pin(lp)])
   if w['command']!=r['command']or w['limit_failure']is not None or w['liveness_group_cleanup']is not True or w['own_child_only']is not True or w['rss_cap_mib']!=512 or type(w['returncode'])is not int or w['returncode']!=(0 if r['status']=='PASS'else 1)or not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 or not 0<=w['sampled_peak_rss_mib']<512:raise RuntimeError('all actual v3 children closed original limits')
   logpin=c.pin(lp)
   if r['status']=='PASS':
    if logpin['sha256']!=r['log_sha256']:raise RuntimeError('actual successful full merged log authority')
   else:
    cases=[case for case in d['actual_operator_refusals']if case['original_execution_record_label']==r['label']]
    if len(cases)!=1 or cases[0]['actual_log_pin']!=logpin or cases[0]['actual_watchdog_pin']!=c.pin(wp) or cases[0]['actual_exit_code']!=1 or Path(lp).read_text().count(cases[0]['expected_abort'])!=1:raise RuntimeError('actual original FAILED record retains its separate complete refusal log/watchdog pins')
  return dict(proof_pins=pins,branch_status=d['status'],failure=d['failure'],all8_children_really_closed=True,no_positive_pipeline_or_physics_terminal=True)
 p=c.pin(FACTOR/'AAA/run_status.json');d=c.read_pinned_json(p)
 if d['classification']!='WAITING_REFERENCE'or d['completed_maps']!=12 or d['reference_qualification']is not None or d['cases']['AAA']['classification']!='VALID_MET'or d['cases']['AAA']['final_directory']!=str(FACTOR/'AAA/map012'):raise RuntimeError('true completed12/WAITING_REFERENCE old branch')
 pins=[p]
 for n in ['map003','map004']:
  p=c.pin(FACTOR/'AAA'/n/'result.json');d=c.read_pinned_json(p)
  if d['classification']!='SEALED_STAGE_OUTPUTS':raise RuntimeError('genuine superseded sealed intermediate map')
  pins.append(p)
 return dict(proof_pins=pins,branch_status='WAITING_REFERENCE',completed_maps=12,raw_targets_are_failed=False,map005_through012_bootstrap_training_all_results_retained=True)
