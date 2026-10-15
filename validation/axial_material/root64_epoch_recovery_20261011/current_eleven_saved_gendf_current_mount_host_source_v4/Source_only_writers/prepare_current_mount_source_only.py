"""Prepare new current metadata Source, without importing any candidate or parser."""
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import resource
import shlex
import stat
import time

R=Path('/Users/wen/spot')
REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
OLD=REC/'current_eleven_saved_gendf_host_source_v3'
BASE=Path(__file__).resolve().parent.parent
GEN=REC/'reaction_genDF_current_mount_stream_source_v2'
OLD_GEN=REC/'reaction_genDF_stream_source_v1'
COMMON=REC/'current_mount_full_identity_common_source_v1'
OUTPUT=R/'validation/artifacts/axial-material-current-eleven-saved-gendf-current-mount-20261013-v4'
START=time.monotonic()
ROWS={}

def demand(ok,message):
    if not ok:raise RuntimeError(message)

def identity(p):
    s=Path(p).lstat()
    return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(path):
    path=Path(path);before=identity(path)
    demand(path.is_absolute() and not any(p.is_symlink()for p in(path,*path.parents)), 'literal no-alias full-file Source/input')
    demand(stat.S_ISREG(before[2]),'regular Source/input')
    with path.open('rb')as f:
        s=os.fstat(f.fileno());opened=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
        demand(opened==before,'opened full7ID')
        sha=hashlib.file_digest(f,'sha256').hexdigest()
        s=os.fstat(f.fileno());after=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
        demand(after==before==identity(path),'fullEOF unchanged7ID')
    return dict(path=str(path),sha256=sha,size_bytes=before[4],identity=before)

def reattest(old):
    demand(set(old)=={'path','sha256','size_bytes','identity'},'full old typed PF')
    key=(old['path'],old['sha256'],old['size_bytes'],tuple(old['identity']))
    if key in ROWS:return copy.deepcopy(ROWS[key]['current_pin'])
    now=pin(old['path'])
    demand((old['path'],old['sha256'],old['size_bytes'],old['identity'][1:])==
           (now['path'],now['sha256'],now['size_bytes'],now['identity'][1:]),'old bytes/size/six non-device fields unchanged: '+old['path'])
    demand(old['identity'][0]in(16777234,16777229)and now['identity'][0]==16777229,'exact declared actual current mount')
    ROWS[key]=dict(historical_pin=copy.deepcopy(old),current_pin=now,only_device_reattestation=True,prior_stage_reexecuted=False)
    return copy.deepcopy(now)

def map_pins(value):
    if isinstance(value,dict):
        if set(value)=={'path','sha256','size_bytes','identity'}:return reattest(value)
        return {k:map_pins(v)for k,v in value.items()}
    if isinstance(value,list):return[map_pins(v)for v in value]
    return value

def write(path,value):
    with Path(path).open('x')as f:
        json.dump(value,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())

def source(path,text):
    ast.parse(text)
    with Path(path).open('x')as f:f.write(text);f.flush();os.fsync(f.fileno())

old_sf=json.loads((OLD/'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json').read_text())
old_hf=json.loads((OLD/'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json').read_text())
old_plan=json.loads((OLD_GEN/'CURRENT_ELEVEN_NONZERO_NX_SAVED_GENDF_SOURCE_PLAN.json').read_text())
old_prep=json.loads((OLD/'CURRENT_ELEVEN_GENDF_HOST_SOURCE_PREPARATION_PLAN.json').read_text())
common_binding=json.loads((COMMON/'CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json').read_text())
common_sf=json.loads((COMMON/'COMPLETE_CURRENT_MOUNT_FULL_IDENTITY_COMMON_SOURCE_FREEZE.json').read_text())
catalog=json.loads(Path(common_binding['current_mount_full_identity_catalog_pin']['path']).read_text())
demand(not GEN.exists() and not OUTPUT.exists() and not OUTPUT.with_name(OUTPUT.name+'-evidence').exists(),'fresh Source and planned execution namespaces')
GEN.mkdir()
mapped_plan=map_pins(old_plan)
static=[reattest(p)for p in old_sf['static_input_pins']]
dependencies=[reattest(p)for p in old_hf['dependencies']]
old_sfp=reattest(old_hf['selected_source_freeze_pin'])
old_hfp=pin(OLD/'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json')
for p in old_sf['complete_source_file_pins']:reattest(p)
for field in ('current_plan_pin','complete_byte_inverse_pin','independent_finite_Source_review_pin','original_immutable_compiler_role_pin'):reattest(old_sf[field])
for p in common_binding['fixed_current_pins']:demand(pin(p['path'])==p,'complete current Common binding fullEOF')
for row in catalog['rows']:demand(pin(row['current_pin']['path'])==row['current_pin'],'all selected catalog rows fullEOF')
for p in common_sf['complete_package_file_pins_before_manifest']:demand(pin(p['path'])==p,'complete Common Source package fullEOF')
compiler=reattest(old_sf['original_immutable_compiler_role_pin'])
demand(compiler==common_binding['compiler'] and compiler['identity'][3]==2,'one exact real current compiler link2 role')
demand(all(p['identity'][3]==(2 if p==compiler else 1)for p in static+dependencies),'no other link-count relaxation')

parser_raw=(OLD_GEN/'extract_binary_gendf_reactions.py').read_bytes()
(GEN/'extract_binary_gendf_reactions.py').write_bytes(parser_raw)
parserpin=pin(GEN/'extract_binary_gendf_reactions.py')
demand(parserpin['sha256']==old_plan['source_pin']['sha256'] and parserpin['size_bytes']==old_plan['source_pin']['size_bytes'],'whole unchanged parser bytes')
mapped_plan['source_pin']=parserpin
write(GEN/'CURRENT_ELEVEN_NONZERO_NX_SAVED_GENDF_SOURCE_PLAN.json',mapped_plan)
planpin=pin(GEN/'CURRENT_ELEVEN_NONZERO_NX_SAVED_GENDF_SOURCE_PLAN.json')

host_old=(OLD/'run_current_eleven_gendf_extraction.py').read_text()
child_old=(OLD/'extract_current_eleven_saved_gendf.py').read_text()
host_changes=[
    ('current_Common_path',"COMMON=REC/'native_warm_A_bounded_host_source_v3/guarded_warm_A_common.py'", "COMMON=REC/'current_mount_full_identity_common_source_v1/guarded_warm_A_common.py'"),
    ('current_Source_schema','COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE_V3','COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE_CURRENT_MOUNT_V4'),
    ('current_host_schema','COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE_V3','COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE_CURRENT_MOUNT_V4'),
    ('explicit_actual_mount_provenance',"      native_engines_started=0,original_input_or_library_writes=0,**FALSE)", "      native_engines_started=0,original_input_or_library_writes=0,\n      explicit_current_mount_input_reattestation_provenance=c.current_metadata_reattestation_provenance(),\n      current_input_reattestation_source_pin=sf['explicit_current_input_reattestation_pin'],**FALSE)"),
]
child_changes=[
    ('one_real_current_compiler_device','identity=[16777234,1171728,33133,2,2648040,1754637485000000000,1778162641926218060]', 'identity=[16777229,1171728,33133,2,2648040,1754637485000000000,1778162641926218060]'),
    ('current_Source_schema','COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE_V3','COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE_CURRENT_MOUNT_V4'),
]
inverse=[]
for name,old,changes in(('run_current_eleven_gendf_extraction.py',host_old,host_changes),('extract_current_eleven_saved_gendf.py',child_old,child_changes)):
    text=old
    for label,before,after in changes:
        demand(text.count(before)==1,'one exact original Source literal:'+label)
        text=text.replace(before,after,1)
    source(BASE/name,text)
    restored=text
    for label,before,after in reversed(changes):
        demand(restored.count(after)==1,'one exact new Source literal:'+label)
        restored=restored.replace(after,before,1)
    demand(restored==old,'full scientific/guard code bytes inverse exact')
    inverse.append(dict(file=name,old_current_pin=pin(OLD/name),new_source_pin=pin(BASE/name),literal_changes=[dict(label=l,old_literal=a,new_literal=b,count=1)for l,a,b in changes],complete_inverse_equal=True))

cli_builder='''"""Print a concrete Root CLI only with an actual closed first-A report fullpin.
Never launches the host, parser, compiler or native solver.
"""
import argparse,hashlib,json,os,shlex,stat
from pathlib import Path
BASE=Path(__file__).resolve().parent
def pin(p):
 p=Path(p);s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 if not p.is_absolute()or not stat.S_ISREG(s.st_mode)or s.st_nlink!=1 or any(v.is_symlink()for v in(p,*p.parents)):raise RuntimeError('literal regular fullpin')
 with p.open('rb')as f:
  s=os.fstat(f.fileno());opened=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
  if opened!=before:raise RuntimeError('open7ID')
  sha=hashlib.file_digest(f,'sha256').hexdigest();s=os.fstat(f.fileno());after=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 if after!=before or [getattr(p.lstat(),k)for k in('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')]!=before:raise RuntimeError('fullEOF7ID')
 return dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)
p=argparse.ArgumentParser()
for suffix in('summary','sha256','seven-id'):p.add_argument('--material-observation-report-'+suffix,required=True)
a=p.parse_args();actual=pin(a.material_observation_report_summary)
if actual['sha256']!=a.material_observation_report_sha256 or actual['identity']!=json.loads(a.material_observation_report_seven_id):raise RuntimeError('externally supplied actual material report fullpin')
d=json.loads(Path(actual['path']).read_text())
if d.get('schema')!='ACTUAL_CURRENT_FORMAL_A_MATERIAL_OBSERVATION_EXECUTION_V1'or d.get('status')!='ACTUAL_ONE_A_MATERIAL_STAGE_CLOSED0_EVIDENCE_ONLY'or d.get('failure')is not None or d.get('after_check_error')is not None or d.get('actual_full_A_observation_executed')is not True or d.get('actual_B_observation_executed')is not False:raise RuntimeError('one actual closed first A observation report required')
recipe=json.loads((BASE/'ROOT_REVIEWABLE_CURRENT_GENDF_V4_CLI_SOURCE_ONLY.json').read_text())
for wanted in(recipe['selected_source_freeze_pin'],recipe['selected_host_freeze_pin'],recipe['host_source_pin']):
 if pin(wanted['path'])!=wanted:raise RuntimeError('frozen current Source exact fullpin')
argv=recipe['argv_prefix']+['--material-observation-report-summary',actual['path'],'--material-observation-report-sha256',actual['sha256'],'--material-observation-report-seven-id',json.dumps(actual['identity'],separators=(',',':'))]+recipe['final_output_option']
print(json.dumps(dict(schema='CONCRETE_CURRENT_GENDF_V4_ROOT_CLI_ONLY_NOT_EXECUTED',argv=argv,shell_safe_command=shlex.join(argv),actual_material_observation_report_pin=actual,requires_Root_true_BOOT_saved_science_and_full_actual_material_review=True,host_or_parser_launched=False),indent=2))
'''
source(BASE/'build_root_reviewable_actual_gendf_cli.py',cli_builder)
all_sources=[pin(BASE/'extract_current_eleven_saved_gendf.py'),pin(BASE/'run_current_eleven_gendf_extraction.py'),parserpin,pin(BASE/'build_root_reviewable_actual_gendf_cli.py'),pin(__file__)]
metadata=dict(schema='COMPLETE_GENDF_V3_TO_CURRENT29_INPUT_REATTESTATION_SOURCE_ONLY_V1',
    original_selected_v3_source_freeze_current_pin=old_sfp,original_selected_v3_host_freeze_current_pin=old_hfp,
    original_GENDF_plan_current_pin=pin(OLD_GEN/'CURRENT_ELEVEN_NONZERO_NX_SAVED_GENDF_SOURCE_PLAN.json'),
    rows=list(ROWS.values()),selected_current_Common_Source_freeze_pin=pin(COMMON/'COMPLETE_CURRENT_MOUNT_FULL_IDENTITY_COMMON_SOURCE_FREEZE.json'),
    selected_current_Common_binding_pin=pin(COMMON/'CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json'),
    selected_current_mount_catalog_pin=common_binding['current_mount_full_identity_catalog_pin'],
    complete_current_Common_binding_rows_fullEOF=len(common_binding['fixed_current_pins']),
    complete_selected_catalog_rows_fullEOF=len(catalog['rows']),
    only_old_device_field_reattested=True,old_sources_and_reports_modified=False,
    business_stages_reexecuted_by_metadata_view=False,new_science_or_physical_qualification_inferred=False,
    parser_imported_or_executed=False,compiler_or_native_engine_started=False,source_only=True)
write(BASE/'COMPLETE_CURRENT_GENDF_INPUT_METADATA_REATTESTATION_SOURCE_ONLY.json',metadata)
metadata_pin=pin(BASE/'COMPLETE_CURRENT_GENDF_INPUT_METADATA_REATTESTATION_SOURCE_ONLY.json')
write(BASE/'COMPLETE_CURRENT_MOUNT_SOURCE_BYTE_INVERSE.json',dict(
    schema='COMPLETE_CURRENT_GENDF_V4_SOURCE_BYTE_INVERSE_ONLY',complete_source_inverse=inverse,
    original_parser_current_pin=pin(OLD_GEN/'extract_binary_gendf_reactions.py'),new_parser_source_pin=parserpin,
    parser_complete_bytes_identical=True,original_all_eleven_plan=metadata['original_GENDF_plan_current_pin'],
    new_all_eleven_plan=planpin,eleven_GENDF_paths_SHA_sizes_and_six_nondevice_fields_unchanged=True,
    all_original_scientific_math_and_guard_budget_code_restored_by_exact_inverse=True,
    original_caps=old_sf['original_caps'],actual_material_report_pin_not_invented=True,
    source_only=True,candidate_imported_or_executed=False,parser_executed=False,native_engines_started=0))
inverse_pin=pin(BASE/'COMPLETE_CURRENT_MOUNT_SOURCE_BYTE_INVERSE.json')
prep=dict(schema='CURRENT_ELEVEN_GENDF_CURRENT_MOUNT_SOURCE_PREPARATION_PLAN_V4',
    status='SOURCE_ONLY_ACTUAL_CURRENT_METADATA_AND_UNCHANGED_MATH_NOT_EXECUTED',
    complete_source_file_pins=all_sources,selected_genDF_source_plan_pin=planpin,
    current_case_spec_pin=reattest(old_prep['current_case_spec_pin']),
    original_immutable_compiler_role_pin=compiler,original_caps=old_sf['original_caps'],
    eleven_saved_binary_input_pins=[p['preserved_binary_GENDf_input_pin']for p in mapped_plan['inputs']],
    original_saved_binary_input_bytes=sum(p['preserved_binary_GENDf_input_pin']['size_bytes']for p in mapped_plan['inputs']),
    selected_current_Common_Source_pin=pin(COMMON/'guarded_warm_A_common.py'),
    selected_current_Common_binding_pin=metadata['selected_current_Common_binding_pin'],
    complete_current_input_reattestation_pin=metadata_pin,complete_scoped_byte_inverse_pin=inverse_pin,
    required_actual_predecessor='Root supplies exact first actual closed current oneA material report after true AAA3 GLOBAL/BOOT and saved full370 diagnostic closure. Mandatory external summary/SHA/seven-id, never future PF.',
    original_DiskResources_ART_role_count=3,complete_source_tree_role_count=2,
    planned_actual_output_root=str(OUTPUT),planned_actual_evidence_root=str(OUTPUT.with_name(OUTPUT.name+'-evidence')),
    candidate_imported_or_executed=False,parser_executed=False,compiler_or_native_engine_started=False,
    complete_reaction_authority_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
write(BASE/'CURRENT_ELEVEN_GENDF_HOST_SOURCE_PREPARATION_PLAN.json',prep)
prep_pin=pin(BASE/'CURRENT_ELEVEN_GENDF_HOST_SOURCE_PREPARATION_PLAN.json')
finite=dict(schema='FINITE_AUTHOR_CURRENT_GENDF_V4_SOURCE_PRE_FREEZE_REVIEW_ONLY',
    status='SOURCE_ONLY_CURRENT_METADATA_FULL_EOF_AND_BYTE_INVERSE_PASS',
    exact_current_reattestation_rows=len(ROWS),full_current_Common_binding_rows=2012,full_selected_catalog_rows=len(catalog['rows']),
    parser_complete_bytes_identical=True,full_host_four_literal_inverse=True,full_child_two_literal_inverse=True,
    original_eleven_GENDF_input_paths_and_SHA_unchanged=True,original_eleven_GENDF_input_bytes=154650680,
    original_guard_MRO_Source_math_caps_and_no_retry_preserved=True,
    original_compiler_current_fullpin=compiler,original_single_immutable_compiler_nlink2_exception_preserved=True,
    all_other_immutable_and_owned_roles_singlelink=True,
    science_parser_imported_or_executed=False,compiler_or_native_engine_started=False,
    independent_Root_review_required_before_any_execution=True,actual_material_receipt_not_predicted=True,
    source_tree_roles_disjoint=True,whole_owning_report_postwrite_samefd_failure_code_unchanged=True,
    complete_reaction_authority_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,
    wall_seconds=time.monotonic()-START,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
write(BASE/'FINITE_AUTHOR_SOURCE_PRE_FREEZE_REVIEW.json',finite)
finite_pin=pin(BASE/'FINITE_AUTHOR_SOURCE_PRE_FREEZE_REVIEW.json')

sf=copy.deepcopy(old_sf)
sf.update(schema='COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE_CURRENT_MOUNT_V4',
    complete_source_file_pins=all_sources,selected_genDF_source_plan_pin=planpin,static_input_pins=static,
    current_plan_pin=prep_pin,complete_byte_inverse_pin=inverse_pin,
    independent_finite_Source_review_pin=reattest(old_sf['independent_finite_Source_review_pin']),
    original_immutable_compiler_role_pin=compiler,explicit_current_input_reattestation_pin=metadata_pin,
    author_finite_source_review_pin=finite_pin,
    historical_v3_source_review_does_not_certify_current_v4_execution=True,
    independent_Root_current_Source_review_required_before_invocation=True,
    original_selected_v3_source_freeze_current_pin=old_sfp,
    current_Common_Source_freeze_pin=metadata['selected_current_Common_Source_freeze_pin'],
    every_current_pin_exact_fullEOF_SHA_and_true7ID=True,
    future_material_or_other_business_output_pins_invented=False)
write(BASE/'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json',sf)
sfp=pin(BASE/'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json')
newdeps=dependencies+static+[planpin,metadata_pin,inverse_pin,prep_pin,finite_pin,old_sfp,old_hfp]+all_sources+common_sf['complete_package_file_pins_before_manifest']+[metadata['selected_current_Common_Source_freeze_pin']]
table={}
for value in newdeps:
    demand(value['path']not in table or table[value['path']]==value,'new exact current dependency consistency')
    table[value['path']]=value
hf=copy.deepcopy(old_hf)
hf.update(schema='COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE_CURRENT_MOUNT_V4',
    host_source=pin(BASE/'run_current_eleven_gendf_extraction.py'),selected_source_freeze_pin=sfp,
    dependencies=list(table.values()),selected_current_Common_Source_pin=pin(COMMON/'guarded_warm_A_common.py'),
    explicit_current_input_reattestation_pin=metadata_pin,
    independent_Root_current_Source_review_required_before_invocation=True,
    future_material_or_other_business_output_pins_invented=False)
write(BASE/'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json',hf)
hfp=pin(BASE/'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json')
prefix=['env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1','/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',hf['host_source']['path']]
for label,pf in(('source-freeze',sfp),('host-freeze',hfp)):
    prefix+=['--'+label+'-summary',pf['path'],'--'+label+'-sha256',pf['sha256'],'--'+label+'-seven-id',json.dumps(pf['identity'],separators=(',',':'))]
write(BASE/'ROOT_REVIEWABLE_CURRENT_GENDF_V4_CLI_SOURCE_ONLY.json',dict(
    schema='CURRENT_GENDF_V4_REVIEWABLE_CLI_RECIPE_REQUIRES_ACTUAL_MATERIAL_REPORT',argv_prefix=prefix,
    selected_source_freeze_pin=sfp,selected_host_freeze_pin=hfp,host_source_pin=hf['host_source'],
    required_actual_material_observation_report_parameters=['--material-observation-report-summary','--material-observation-report-sha256','--material-observation-report-seven-id'],
    actual_material_observation_report_pin=None,actual_full_executable_argv=None,
    final_output_option=['--output-dir',str(OUTPUT)],
    actual_receipt_required_cli_builder_source_pin=pin(BASE/'build_root_reviewable_actual_gendf_cli.py'),
    needs_true_AAA3_GLOBAL_and_BOOT_saved_full370_and_actual_first_A_material_closure=True,
    source_only=True,host_imported_or_executed=False,parser_imported_or_executed=False,
    compiler_or_native_engine_started=False,future_business_output_PF_invented=False))
for p in all_sources+list(table.values())+[sfp,hfp]:demand(pin(p['path'])==p,'postfreeze fullEOF exact current Source/input')
print(json.dumps(dict(status='CURRENT_GENDF_V4_SOURCE_ONLY_PACKAGE_FROZEN_NOT_EXECUTED',source_freeze_pin=sfp,host_freeze_pin=hfp,CLI_recipe_pin=pin(BASE/'ROOT_REVIEWABLE_CURRENT_GENDF_V4_CLI_SOURCE_ONLY.json'),exact_old_to_current_reattestation_rows=len(ROWS),eleven_GENDF_bytes=154650680,parser_or_host_imported_or_executed=False,compiler_or_native_engine_started=False,author_SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),allow_nan=False))
