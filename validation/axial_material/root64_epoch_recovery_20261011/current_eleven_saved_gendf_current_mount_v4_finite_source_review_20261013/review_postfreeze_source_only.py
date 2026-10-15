"""Finite author audit of frozen current GENDF Sources; never import candidates."""
import ast
import hashlib
import json
import os
from pathlib import Path
import resource
import stat
import time

REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
BASE=REC/'current_eleven_saved_gendf_current_mount_host_source_v4'
GEN=REC/'reaction_genDF_current_mount_stream_source_v2'
OLD=REC/'current_eleven_saved_gendf_host_source_v3'
OLD_GEN=REC/'reaction_genDF_stream_source_v1'
COMMON=REC/'current_mount_full_identity_common_source_v1'
OUT=Path(__file__).resolve().parent
START=time.monotonic();checks=[];pins={}

def need(ok,name):
    if not ok:raise RuntimeError(name)
    checks.append(name)

def ident(p):
    s=Path(p).lstat()
    return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p):
    p=Path(p);before=ident(p)
    need(p.is_absolute()and not any(v.is_symlink()for v in(p,*p.parents)), 'literal absolute/no aliases:'+str(p))
    need(stat.S_ISREG(before[2]),'regular:'+str(p))
    with p.open('rb')as f:
        s=os.fstat(f.fileno());opened=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
        need(opened==before,'opened full7ID:'+str(p))
        sha=hashlib.file_digest(f,'sha256').hexdigest()
        s=os.fstat(f.fileno());after=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
        need(after==before==ident(p),'fullEOF full7ID:'+str(p))
    return dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)

def verify(p):
    need(p['path']not in pins or pins[p['path']]==p,'unique unambiguous current PF:'+p['path'])
    if p['path']not in pins:
        need(pin(p['path'])==p,'actual fullEOF exact SHA/all7ID:'+p['path'])
        pins[p['path']]=p

def read(path):return json.loads(Path(path).read_text())

sf=read(BASE/'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json')
hf=read(BASE/'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json')
cli=read(BASE/'ROOT_REVIEWABLE_CURRENT_GENDF_V4_CLI_SOURCE_ONLY.json')
inverse=read(BASE/'COMPLETE_CURRENT_MOUNT_SOURCE_BYTE_INVERSE.json')
mapping=read(BASE/'COMPLETE_CURRENT_GENDF_INPUT_METADATA_REATTESTATION_SOURCE_ONLY.json')
plan=read(GEN/'CURRENT_ELEVEN_NONZERO_NX_SAVED_GENDF_SOURCE_PLAN.json')
old_plan=read(OLD_GEN/'CURRENT_ELEVEN_NONZERO_NX_SAVED_GENDF_SOURCE_PLAN.json')
cb=read(COMMON/'CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json')
csf=read(COMMON/'COMPLETE_CURRENT_MOUNT_FULL_IDENTITY_COMMON_SOURCE_FREEZE.json')
catalog=read(cb['current_mount_full_identity_catalog_pin']['path'])
compiler=sf['original_immutable_compiler_role_pin']
need(sf['schema']=='COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE_CURRENT_MOUNT_V4','new current source schema')
need(hf['schema']=='COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE_CURRENT_MOUNT_V4','new current host schema')
need(compiler==cb['compiler']and compiler['identity']==[16777229,1171728,33133,2,2648040,1754637485000000000,1778162641926218060],'one actual compiler fullpin/link2 constant')
need(compiler['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492','original compiler fullSHA')
for row in mapping['rows']:
    old,now=row['historical_pin'],row['current_pin']
    need((old['path'],old['sha256'],old['size_bytes'],old['identity'][1:])==(now['path'],now['sha256'],now['size_bytes'],now['identity'][1:]), 'only actual old device changed:'+old['path'])
    need(old['identity'][0]in(16777234,16777229)and now['identity'][0]==16777229,'actual current dev29:'+old['path'])
    verify(now)
need(len(mapping['rows'])==51,'all 51 old protected fullPF reattestations')
for row in cb['fixed_current_pins']:verify(row)
for row in catalog['rows']:verify(row['current_pin'])
for row in csf['complete_package_file_pins_before_manifest']:verify(row)
for row in hf['dependencies']+sf['complete_source_file_pins']+sf['static_input_pins']+[cli['selected_source_freeze_pin'],cli['selected_host_freeze_pin'],sf['selected_genDF_source_plan_pin'],sf['explicit_current_input_reattestation_pin']]:verify(row)
need(len(cb['fixed_current_pins'])==2012 and len(catalog['rows'])==3040,'complete current Common/catalog rows covered')
need(all(p['identity'][3]==(2 if p==compiler else 1)for p in pins.values()),'only explicit exact compiler link2 all others link1')

for row in inverse['complete_source_inverse']:
    original=Path(row['old_current_pin']['path']).read_text()
    text=Path(row['new_source_pin']['path']).read_text();restored=text
    for change in reversed(row['literal_changes']):
        need(restored.count(change['new_literal'])==1,'single inverse literal:'+change['label'])
        restored=restored.replace(change['new_literal'],change['old_literal'],1)
    need(restored==original,'whole original guard and scientific code bytes restored:'+row['file'])
need((GEN/'extract_binary_gendf_reactions.py').read_bytes()==(OLD_GEN/'extract_binary_gendf_reactions.py').read_bytes(),'parser whole bytes preserved')
need(plan['schema']==old_plan['schema']=='READONLY_CURRENT_NONZERO_NX_GENDF_SOURCE_PLAN_V1','same original semantic GENDF plan schema')
need(plan['current_formal_case_sha256']==old_plan['current_formal_case_sha256']=='fbe3362e16c19c93b87de2ebf67607c5ac0a579daa1f7af5891aae9c9faa7b16','same exact formal physical case')
need(plan['actual_nonzero_NX_unique_references']==old_plan['actual_nonzero_NX_unique_references']==['U235','U238','Fe54','Fe56','Fe57','Fe58','Cr50','Cr52','Cr53','Cr54','Mn55'],'exact ordered all11 NX isotopes')
need(len(plan['inputs'])==11 and sum(r['preserved_binary_GENDf_input_pin']['size_bytes']for r in plan['inputs'])==154650680,'complete eleven original GENDF input size')
for old,new in zip(old_plan['inputs'],plan['inputs']):
    need(old['nuclide']==new['nuclide']and old['mat']==new['mat'],'same nuclide/MAT:'+old['nuclide'])
    for key in old:
        if key.endswith('_pin'):
            a,b=old[key],new[key]
            need((a['path'],a['sha256'],a['size_bytes'],a['identity'][1:])==(b['path'],b['sha256'],b['size_bytes'],b['identity'][1:]), 'unchanged GENDF/DRAGR/deck source provenance:'+old['nuclide']+'/'+key)
            verify(b)
        else:need(old[key]==new[key],'unchanged original plan field:'+old['nuclide']+'/'+key)
host=(BASE/'run_current_eleven_gendf_extraction.py').read_text()
child=(BASE/'extract_current_eleven_saved_gendf.py').read_text()
parser=(GEN/'extract_binary_gendf_reactions.py').read_text()
builder=(BASE/'build_root_reviewable_actual_gendf_cli.py').read_text()
for p in sf['complete_source_file_pins']:
    if p['path'].endswith('.py'):ast.parse(Path(p['path']).read_text())
caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
need(sf['original_caps']==hf['original_caps']==caps,'whole original 600/1800/512/1thread/1child/no retry/disk caps')
for literal in ["for prefix in('source-freeze','host-freeze','material-observation-report')", "p.add_argument('--'+prefix+'-'+suffix,required=True)", "ACTUAL_ONE_A_MATERIAL_STAGE_CLOSED0_EVIDENCE_ONLY", "c.closed_report(observed,helper,Path(pobserved['path']).parent,1)", "released['total_owned_bytes_released']!=979740136", "roots[:3]", "source_roots=[Path(value)for value in roots[3:]]", "fresh['artifact_bytes']+source_bytes+unlinked", "explicit_current_mount_input_reattestation_provenance=c.current_metadata_reattestation_provenance()", "descriptor=os.open(summary_path,os.O_WRONLY|os.O_NOFOLLOW)", "if actual_identity!=summary_first_pin['identity']", "stream.seek(0);stream.truncate(0)", "summary.update(status='FAILED_GENDF_EXTRACTION_NO_RETRY'", "resources.check()"]:
    need(literal in host,'required receipt/resources/provenance/failure boundary:'+literal)
for literal in ["expected==ORIGINAL_COMPILER_ROLE", "before.st_nlink==(2 if compiler_role else 1)", "compiler_role=(row==ORIGINAL_COMPILER_ROLE)", "budget.last=0.0;budget.check()", "parser.extract(row['preserved_binary_GENDf_input_pin'],row['mat'],[5],budget.check)"]:
    need(literal in child,'exact child roles/caps/parser boundary:'+literal)
for literal in ['incident_present', 'separable_spectrum_present', 'P0_vector64', 'math.fsum(row)', 'original_full_MF1_temperature_dilution_energy_grids', 'complete_reaction_authority_qualified\': False']:
    need(literal in parser,'unmodified full physics evidence/scope:'+literal)
need(cli['actual_material_observation_report_pin']is None and cli['actual_full_executable_argv']is None,'no future material fullpin/executable argv invented')
need(cli['required_actual_material_observation_report_parameters']==['--material-observation-report-summary','--material-observation-report-sha256','--material-observation-report-seven-id'],'all three actual report arguments mandatory')
need('--material-observation-report-'in builder and "p.add_argument('--material-observation-report-'+suffix,required=True)"in builder,'concrete CLI builder requires externally supplied actual report')
need('subprocess'not in builder and 'os.exec'not in builder and 'os.spawn'not in builder,'CLI builder never launches business')
for schema in (sf,hf):
    for field in ('candidate_executed','parser_executed','complete_reaction_authority_qualified','scientific_accuracy_qualified','AAA_qualified','ABA_admitted','goal_complete'):
        need(schema[field]is False,'Source scope explicitly false:'+field)
for path in (Path(cli['final_output_option'][1]),Path(cli['final_output_option'][1]+'-evidence')):need(not os.path.lexists(path),'actual execution namespaces still absent:'+str(path))
need(BASE!=GEN and not BASE.is_relative_to(GEN)and not GEN.is_relative_to(BASE),'two ordinary complete Source tree roles remain disjoint')

report=dict(schema='FINITE_AUTHOR_POSTFREEZE_CURRENT_GENDF_V4_SOURCE_REVIEW_20261013',
    status='SOURCE_ONLY_FROZEN_PACKAGE_FULL_EOF_REVIEW_PASS_ROOT_INDEPENDENT_REVIEW_REQUIRED',
    checks=len(checks),failed_checks=[],unique_fullEOF_files=len(pins),unique_fullEOF_bytes=sum(p['size_bytes']for p in pins.values()),
    complete_Common_fixed_rows=2012,complete_current_catalog_rows=3040,exact_old_to_current_reattestation_rows=51,
    original_GENDF_inputs=11,original_GENDF_input_bytes=154650680,original_parser_full_bytes_identical=True,
    only_current_metadata_schema_and_source_path_changes_in_host_child=True,original_scientific_numeric_code_and_caps_unchanged=True,
    one_exact_immutable_compiler_current29_nlink2_role=compiler,
    first_actual_current_A_material_report_required_not_predicted=True,
    five_joint_archive_roles_complete_no_exclusions=True,postwrite_samefd_failure_source_preserved=True,
    current_meta_provenance_honest_not_previous_execution_replay=True,
    parser_or_candidate_imported_or_executed=False,compiler_or_native_or_physics_started=False,
    Root_true_AAA3_GLOBAL_BOOT_savedfull370_actual_first_A_material_prerequisites_verified_by_this_review=False,
    DRAGR_packed_raw_words_replayed=False,current_SPH_MASK_context_applied=False,
    three_current_raw_MACRO_comparisons_performed=False,complete_reaction_authority_qualified=False,
    AAA_qualified=False,ABA_admitted=False,goal_complete=False,
    current_source_freeze_pin=cli['selected_source_freeze_pin'],current_host_freeze_pin=cli['selected_host_freeze_pin'],
    current_frozen_CLI_recipe_pin=pin(BASE/'ROOT_REVIEWABLE_CURRENT_GENDF_V4_CLI_SOURCE_ONLY.json'),
    limitations=['Source review only; Root independent current Source review and all actual predecessor closed terminals remain mandatory','Extraction will retain all370 P0/masks/grids for MT5 of all11 preserved NX nuclides. Its binary64 fsum is diagnostic evidence, not DRAGR packed-word replay, TONE/SPH/MASK authority, neutron balance or coupled accuracy','CLI builder prints a reviewable command and never executes. Root must verify its frozen recipe pin and actual predecessor report and external terminal before business launch'],
    wall_seconds=time.monotonic()-START,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
path=OUT/'REVIEW.json'
with path.open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=report['status'],checks=report['checks'],fullEOF_unique_files=report['unique_fullEOF_files'],fullEOF_unique_bytes=report['unique_fullEOF_bytes'],report_pin=pin(path),parser_or_candidate_executed=False),allow_nan=False))
