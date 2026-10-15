"""Independent full-EOF final manifest review. No candidate import or deletion."""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import time

ROOT=Path('/Users/wen/spot');REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011';ART=ROOT/'validation/artifacts'
PKG=REC/'storage_release_old_v9_single_PROJECT_draft_source_20261013';OUT=Path(__file__).parent
BASE=REC/'storage_release_closed_v7_v8_project_pair_20261013/project_pair_release_common.py'
raw=BASE.read_bytes()
if hashlib.sha256(raw).hexdigest()!='b0a0a3d1f4eacfe8c9b91378b89aff1071a3907c2027a3fec857e160ae6e0b7d':raise RuntimeError('original readonly helper Source changed')
spec=importlib.util.spec_from_file_location('independent_actual_single_manifest_readonly_utilities',BASE);b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
start=time.monotonic();counts={'full_EOF_calls':0,'full_EOF_bytes':0};original_pin=b.pin
def pin(path):
    row=original_pin(path);counts['full_EOF_calls']+=1;counts['full_EOF_bytes']+=row['size_bytes'];return row
b.pin=pin
def need(condition,message):
    if not condition:raise RuntimeError(message)
def selected(path,sha,seven):
    row=pin(path);need(row['sha256']==sha and row['identity']==seven,'external selected SHA/all7ID');return row
mp=selected(PKG/'EXACT_SINGLE_OLD_V9_PRIVATE_PROJECT_RELEASE_MANIFEST.json','ce25d26f0898bae8e198eb66db6edd551c7be66d1b1de8884237efdb664b5709',[16777229,50018279,33188,1,4229848,1791873572548256514,1791873572548256514]);m=b.read(mp)
sf=selected(PKG/'COMPLETE_SINGLE_OLD_V9_PROJECT_RELEASE_SOURCE_FREEZE.json','8d46ab326dffddca6524d9ecb3a418bd04b6469208777068f079a67d1efc88b8',[16777229,50018204,33188,1,4730,1791873517079681580,1791873517079681580]);f=b.read(sf)
need(m['schema']=='ROOT_EXACT_SINGLE_OLD_V9_PROJECT_RELEASE_MANIFEST_V1' and m['draft_only'] is False and m['action_executed'] is False and m['selected_complete_Source_freeze_pin']==sf,'actual unexecuted exact manifest only')
need(f['schema']=='COMPLETE_SINGLE_OLD_V9_PROJECT_RELEASE_SOURCE_FREEZE_V1' and f['deletion_executed'] is False and f['v11_business_qualification_claimed'] is False and m['Source_pins']==f['Source_pins'],'exact Source-only freeze')
for row in f['Source_pins']+[f['original_readonly_helper_pin'],f['original_resource_factory_pin'],f['actual_readonly_candidate_survey_pin']]:b.same(row)
for row in f['Source_pins']:ast.parse(Path(row['path']).read_bytes())
need(f['original_caps']==dict(SELF_mib=512,whole_seconds=1800,stage_seconds=600,threads=1,children_at_once=1,fresh_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20),'all original resource caps unchanged')
protected=m['current_protected_full_EOF_pins'];table={row['path']:row for row in protected}
need(len(protected)==5119 and len(table)==5119,'all5119 unique protected paths')
for row in protected:b.same(row)
def covered(row):
    old=b.norm(row);current=table.get(old['path']);need(current is not None,'mandatory missing protected path '+old['path'])
    if current!=old:need(old['identity'][0]==16777234 and current['identity'][0]==16777229 and old['identity'][1:]==current['identity'][1:] and old['sha256']==current['sha256'] and old['size_bytes']==current['size_bytes'],'only exact declared mount-device transition')
def rows(value):
    for row in b.nested(value):covered(row)
def meta(path):
    row=pin(path);covered(row);return b.read(row)
cat=meta(REC/'current_mount_identity_reattestation_20261012/CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG.json')
need(len(cat['rows'])==3040 and len({r['current_pin']['path'] for r in cat['rows']})==2989,'3040 rows/2989 unique current catalog')
rows([r['current_pin'] for r in cat['rows']])
common=meta(REC/'current_mount_full_identity_common_source_v1/CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json');need(len(common['fixed_current_pins'])==2012,'all2012 Common rows');rows(common['fixed_current_pins'])
science=meta(REC/'saved_full370_terminal_audit_host_source_v2/CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json');need(len(science['fixed_current_pins'])==3315 and len(science['science_original_input_pins'])==1129,'all science3315+1129');rows(science['fixed_current_pins']);rows(science['science_original_input_pins'])
hf11=selected(REC/'aaa_three_plane_streaming_pipeline_source_v11/COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json','2597f653ebb8d24e454d0f129efb1db1f623073e4524b9ce0b560d54ade56736',[16777229,50017634,33188,1,163351,1791873144732798330,1791873144732798330]);need(hf11==m['selected_actual_v11_HF_pin']==f['selected_actual_v11_HF_pin'],'real v11 HF selection')
cli11=selected(REC/'ROOT_EXACT_ACTUAL_PIPELINE_V11_ARGV_20261013.json','5a00c302d82b76ff7cb8776aa2bfc7db5aa126c9c4845e495f74ce5c776507d1',[16777229,50017635,33188,1,13380,1791873144733698750,1791873144733698750]);need(cli11==m['selected_actual_v11_CLI_pin']==f['selected_actual_v11_CLI_pin'],'real v11 CLI selection');covered(cli11)
for version,n in (('v10',278),('v11',308)):
    hf=meta(REC/('aaa_three_plane_streaming_pipeline_source_'+version)/'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json');need(len(hf['dependencies'])==n and hf['prepared_only'] is True and hf['actual_pipeline_executed'] is False,'frozen exact pipeline dependencies')
    rows([hf['host_source']]+hf['dependencies']);build=b.read(table[hf['selected_actual_build70_report']['path']]);rows(build['fixed_current_pins']);rows(build['output_pins'])
source_dirs=[REC/('aaa_three_plane_streaming_pipeline_source_'+v) for v in ('v10','v11')]+sorted(REC.glob('current_formal_material_authority_exact_cache70_source_v*'))+[REC/'current_eleven_saved_gendf_current_mount_host_source_v4',REC/'reaction_genDF_current_mount_stream_source_v2',REC/'full370_unreduced_eigen_reference_source_v2',REC/'aaa_pipeline_v11_author_finite_source_review_20261013',REC/'material_exact_cache70_v6_author_finite_source_review_20261013']
source_files=0
for directory in source_dirs:
    need(directory.is_dir(),'actual complete protected Source package');before=sorted(str(p) for p in directory.rglob('*') if p.is_file())
    for name in before:
        covered(pin(name));source_files+=1
        if Path(name).suffix=='.json' and ('current_formal_material_authority_exact_cache70_source_v' in str(directory) or directory.name in ('current_eleven_saved_gendf_current_mount_host_source_v4','reaction_genDF_current_mount_stream_source_v2')):rows(b.read(table[name]))
    need(before==sorted(str(p) for p in directory.rglob('*') if p.is_file()),'Source entries stayed fixed')
for name in ('ROOT_FINITE_PIPELINE_V11_CLOSED_METADATA_LIFETIME_HOST_REVIEW_20261013.json','ROOT_PIPELINE_V11_SOURCE_REVIEW_TRUE_TOOL_RETURN_20261013.json'):covered(pin(REC/name))
plan=meta(REC/'full370_unreduced_eigen_reference_source_v2/CURRENT_FORMAL_FULL370_INPUT_PLAN_SOURCE_ONLY.json');rows([plan[k] for k in ('protected_formal_and_producer_plan_pin','current_case_spec_pin','current_prepared_pin','current_axial_track_pin','additional_current_input_pins')]);formal=b.read(table[plan['protected_formal_and_producer_plan_pin']['path']]);rows(formal['formal_inputs'])
for row in formal['producers']:rows([row[k] for k in ('report','archive','radial_binary_track')])
target=m['target_full_EOF_pin'];branch=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v9';target_path=branch/'AAA/projected_boot.xsm'
need(m['target_count']==1 and m['target_logical_bytes']==749355952 and target==dict(path=str(target_path),sha256='ea56e0e58889469c81e1519713ca0df93a3ebb5f2b1a1fbd2e20b5d8be72833a',size_bytes=749355952,identity=[16777229,50012374,33152,1,749355952,1791869646152430244,1791869646152430244]),'one literal original private PROJECT only')
b.same(target);need(target['path'] not in table and tuple(target['identity'][:2]) not in {tuple(p['identity'][:2]) for p in protected} and target_path.lstat().st_uid==os.getuid() and target['identity'][3]==1 and stat.S_ISREG(target['identity'][2]),'exact owned regular nlink1 current union disjoint')
retained=m['retained_oldv9_full_EOF_pins'];need(len(retained)==242 and len({r['path'] for r in retained})==242,'all242 other v9 regular files')
for row in retained:b.same(row);covered(row)
files={};dirs={};links={};stack=[branch]
while stack:
    directory=stack.pop();dirs[str(directory)]=b.identity(directory.lstat());fd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:
        with os.scandir(fd) as entries:
            for entry in entries:
                path=directory/entry.name;st=entry.stat(follow_symlinks=False)
                if stat.S_ISDIR(st.st_mode):stack.append(path)
                elif stat.S_ISREG(st.st_mode):files[str(path)]=b.identity(st)
                elif stat.S_ISLNK(st.st_mode):links[str(path)]={'identity':b.identity(st),'target':os.readlink(path)}
                else:raise RuntimeError('unexpected special entry')
    finally:os.close(fd)
need(dict(ordinary_file_identities=files,symlinks=links,directory_identities=dirs)==m['complete_before_inventory'],'entire oldv9 inventory unchanged')
need(len(files)==243 and set(files)=={r['path'] for r in retained}|{str(target_path)},'exact243 before/242 retained')
d=meta(branch/'Root_actual_three_plane_engineering_summary.json');t=meta(REC/'ACTUAL_PIPELINE_V9_AFTER_EXACT_TWO_RELEASE_TRUE_TOOL_RETURNS_20261013.json')
need(t['observed_closed'] is True and t['original_integer_exit_code']==1 and t['terminal']['exit_code']==1 and len(d['records'])==42 and d['engineering_three_plane_closed0'] is False and d['after_check_error'] is None,'actual closed v9 failed aggregate')
selected_records={r['label']:r for r in d['records']};need(selected_records['AAA/global_positive']['status']==selected_records['AAA/project_positive']['status']=='PASS','individual GLOBAL PROJECT PASS preserved')
for r in d['records']:
    w=meta(branch/(r['label']+'.watchdog.json'));covered(pin(branch/(r['label']+'.log')));expected=0 if r['status']=='PASS' else (-5 if r['label']=='AAA/view_memory_output' else 1)
    need(w['returncode']==expected and w['liveness_group_cleanup'] is True and w['own_child_only'] is True and w['limit_failure'] is None and w['rss_cap_mib']==512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 and 0<=w['sampled_peak_rss_mib']<512,'all42 true original closed stages')
v10out=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v10'
for path in v10out.rglob('*'):
    if path.is_file():covered(pin(path))
d10=meta(v10out/'Root_actual_three_plane_engineering_summary.json');t10=meta(REC/'ACTUAL_PIPELINE_V10_TRUE_TOOL_RETURNS_20261013.json');need(t10['observed_closed'] is True and t10['original_integer_exit_code']==1 and t10['terminal']['exit_code']==1 and d10['failure']==d10['after_check_error']=='RuntimeError: original SELF 512MiB cap' and d10['output_pins']==[] and len(d10['records'])==46,'closed v10 truthful original SELF failure')
need(not os.path.lexists(ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v11'),'no v11 business namespace yet')
b.same(f['original_resource_factory_pin']);budget=b.budget();oldbudget=m['original_budget_before_preparation'];need(budget['artifact_bytes']==oldbudget['artifact_bytes'] and budget['regular_files']==oldbudget['regular_files'],'actual ART budget no new writer delta')
for row in protected+retained+f['Source_pins']+[mp,sf,hf11,cli11,target]:b.same(row)
report=dict(schema='INDEPENDENT_FINITE_SINGLE_OLD_V9_PROJECT_MANIFEST_REVIEW_V1',status='PASS_CURRENT_FULL_EOF_EXACT_ONE_FINAL_MANIFEST_NO_DELETION',manifest_pin=mp,Source_freeze_pin=sf,current_protected_unique=5119,all3040_catalog_rows_2989_unique=True,Common2012_rows=True,science3315_and1129=True,v10HF278_and_v11HF308=True,current_materialv6_GENDFv4_reference_complete_Source_and_actual_inputs=True,all_current_v11_Source_proofs_and_CLI_retained=True,all242_other_oldv9_files_and_all_closed_v10_files_full_EOF=True,oldv9_directory_count=len(dirs),ordinary_before=243,literal_owned_disjoint_candidate_pin=target,actual_history_artifact_bytes=budget['artifact_bytes'],actual_regular_files=budget['regular_files'],actual_remaining_initial_reserve_bytes=budget['remaining_after_original_initial_reserves_bytes'],hypothetical_after_exact_single_initial_reserve_bytes=budget['remaining_after_original_initial_reserves_bytes']+749355952,original_INITIAL_reserve_admitted=budget['original_initial_reserve_admitted'],all_original_resource_caps_preserved=True,individual_GLOBAL_PROJECT_PASS_preserved=True,only_oldv9_full_raw_replay_would_be_lost=True,historical_summary_output_pins_not_promoted_to_current_inputs=True,protected_Source_files_checked=source_files,complete_EOF_counts=counts,candidate_cleanup_Source_not_imported=True,compiler_or_business_executed=False,deletion_executed=False,goal_complete=False,elapsed_seconds=time.monotonic()-start)
b.write_new(OUT/'INDEPENDENT_CURRENT_UNION_FULL_EOF_FINAL_MANIFEST_REVIEW.json',report);b.guard()
print(json.dumps(dict(status=report['status'],review_pin=pin(OUT/'INDEPENDENT_CURRENT_UNION_FULL_EOF_FINAL_MANIFEST_REVIEW.json'),protected=5119,retained=242,target_bytes=749355952,actual_initial_reserve_bytes=report['actual_remaining_initial_reserve_bytes'],conditional_after_release_reserve_bytes=report['hypothetical_after_exact_single_initial_reserve_bytes'],full_EOF_calls=counts['full_EOF_calls'],full_EOF_bytes=counts['full_EOF_bytes'])))
