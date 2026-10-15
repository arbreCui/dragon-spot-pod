"""Independent frozen Source/data verification; no candidate import or execution."""
from pathlib import Path
import ast,hashlib,json,os,resource,shlex,stat,time
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
V1=REC/'saved_full370_terminal_audit_host_source_v1'
V2=REC/'saved_full370_terminal_audit_host_source_v2'
OUT=Path(__file__).resolve().parent
start=time.monotonic(); checks=0; verified={}
def require(condition,label):
 global checks
 checks+=1
 if not condition:raise RuntimeError(label)
def seven(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);before=seven(p.lstat());require(stat.S_ISREG(before[2]),'non-symlink regular leaf '+str(p))
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 with os.fdopen(fd,'rb') as f:
  require(seven(os.fstat(f.fileno()))==before,'opened seven fields '+str(p))
  sha=hashlib.file_digest(f,'sha256').hexdigest()
  require(seven(os.fstat(f.fileno()))==before,'same-fd complete EOF '+str(p))
 require(seven(p.lstat())==before,'after path seven fields '+str(p))
 return dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)
def verify(row):
 if row['path'] in verified:
  require(verified[row['path']]==row,'duplicate exact declared fullpin '+row['path']);return
 actual=pin(row['path']);require(actual==row,'actual fullEOF SHA/7ID '+row['path']);verified[row['path']]=actual
def write(p,obj):
 with Path(p).open('x') as f:json.dump(obj,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def current_only_device(old,new):
 return (old['path'],old['sha256'],old['size_bytes'],old['identity'][1:])==(new['path'],new['sha256'],new['size_bytes'],new['identity'][1:]) and old['identity'][0] in(16777234,16777229) and new['identity'][0]==16777229
def load(name):return json.loads((V2/name).read_text())
hf=load('COMPLETE_SAVED_FULL370_GUARD_HOST_SOURCE_FREEZE.json');hfp=pin(V2/'COMPLETE_SAVED_FULL370_GUARD_HOST_SOURCE_FREEZE.json')
require(hfp['sha256']=='043b1a3232709edfe65f1b4f3f686365fe996239c97eb03f14c0df4deddd57ec' and hfp['identity']==[16777229,49960806,33188,1,10755,1791827862059747688,1791827862059747688],'external actual final HF fullpin')
binding=load('CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json');sf=load('COMPLETE_SAVED_FULL370_SCIENCE_SOURCE_FREEZE.json');mapping=load('COMPLETE_SAVED_FULL370_EXPLICIT_CURRENT_MOUNT_INPUT_MAPPING.json');cli=load('ROOT_REVIEWABLE_EXACT_SAVED_FULL370_V2_ARGV_SOURCE_ONLY.json')
old=json.loads((V1/'CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json').read_text());draft=load('PRELIMINARY_ALL_LIVE_INPUTS_FULL_EOF_CURRENT_MAPPING.json');inverse=load('COMPLETE_SAVED_FULL370_SOURCE_AND_HOST_BYTE_INVERSE_DRAFT.json')
require(hf['schema']=='COMPLETE_SAVED_FULL370_TERMINAL_SOURCE_GUARD_HOST_FREEZE_ONLY_V2','actual intended HF schema')
require(sf['schema']=='COMPLETE_SAVED_FULL370_SCIENCE_SOURCE_CURRENT_MOUNT_FREEZE_ONLY_V2','actual SF schema')
require(binding['schema']=='CURRENT_SAVED_FULL370_TERMINAL_SOURCE_ORIGINAL_GUARD_INPUT_BINDING_EXPLICIT_CURRENT_MOUNT_V2','actual BIND schema')
require(mapping['schema']=='SAVED_FULL370_EXPLICIT_CURRENT_MOUNT_REATTESTATION_SOURCE_V2','actual mapping schema accepted by host')
for row in binding['fixed_current_pins']+hf['fixed_source_files']+[hfp]:verify(row)
for key in ('input_binding_pin','host_pin','selected_actual_science_source_freeze_pin','selected_actual_current_mapping_pin','original_unmodified_v1_source_freeze_current_pin'):verify(hf[key])
for key in ('source_pin','science_manifest_pin','original_science_current_pin','original_manifest_current_pin','explicit_current_mapping_pin','input_binding_pin','source_inverse_draft_pin'):verify(sf[key])
for key in ('science_source_pin','science_manifest_pin','formal_prepared_pin','formal_case_spec_pin','original_v1_binding_current_pin','complete_current_mount_mapping_pin'):verify(binding[key])
for key in ('Source_freeze_pin','host_pin','selected_actual_science_source_freeze_pin','input_binding_pin','current_mapping_pin'):verify(cli[key])
catalog=mapping['selected_actual_catalog_pin'];verify(catalog)
require(catalog['sha256']=='77d7e680863e87bcff590cfab4be023a306ca6b7981eb00290440ff8e24e1ab2','selected actual current catalog SHA')
require(hf['input_binding_pin']==sf['input_binding_pin']==cli['input_binding_pin']==pin(V2/'CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json'),'actual BIND consistently selected')
require(hf['host_pin']==cli['host_pin']==pin(V2/'run_actual_saved_full370_terminal_source_original_guard.py'),'actual host consistently selected')
require(hf['selected_actual_science_source_freeze_pin']==cli['selected_actual_science_source_freeze_pin']==pin(V2/'COMPLETE_SAVED_FULL370_SCIENCE_SOURCE_FREEZE.json'),'actual SF consistently selected')
require(hf['selected_actual_current_mapping_pin']==sf['explicit_current_mapping_pin']==binding['complete_current_mount_mapping_pin']==cli['current_mapping_pin']==pin(V2/'COMPLETE_SAVED_FULL370_EXPLICIT_CURRENT_MOUNT_INPUT_MAPPING.json'),'actual mapping consistently selected')
require(sf['source_pin']==binding['science_source_pin']==pin(V2/'audit_saved_terminal_source_all370.py') and sf['science_manifest_pin']==binding['science_manifest_pin']==pin(V2/'ACTUAL_INPUT_PIN_PLAN_UNRUN.json'),'actual selected scientific Source and manifest')
require(mapping['rows']==draft['rows'] and not mapping['errors'] and len(mapping['rows'])==3301,'final current rows exact preliminary3301 and no errors')
require(mapping['source_draft_predecessor_current_pin']==pin(V2/'PRELIMINARY_ALL_LIVE_INPUTS_FULL_EOF_CURRENT_MAPPING.json'),'final mapping pins actual unmodified draft predecessor')
require(len(mapping['historical_non_live_declarations'])==4,'four historical origins completely declared')
fixed={p['path']:p for p in binding['fixed_current_pins']};historical=[];current={}
require(len(fixed)==len(binding['fixed_current_pins'])==3315,'complete current binding unique3315 fullpins')
for row in mapping['rows']:
 oldp=row['historical_pin'];newp=row['current_pin'];verify(newp)
 require(current_only_device(oldp,newp),'only actual device transition '+newp['path'])
 require(row['mandatory'] is True and fixed.get(newp['path'])==newp,'all3301 mandatory in actual fixed '+newp['path'])
 require(newp['path'] not in current,'current mapping unique '+newp['path'])
 current[newp['path']]=newp;historical.append(oldp)
for declaration in mapping['historical_non_live_declarations']:
 oldp=declaration['historical_pin'];historical.append(oldp)
 require(not os.path.lexists(oldp['path']),'historical path still genuinely absent '+oldp['path'])
 require(declaration['current_pin'] is None and declaration['current_file_exists'] is False and declaration['in_scientific_1129_inputs'] is False and declaration['original_v1_mandatory'] is True,'historical origin not fabricated current')
 require(oldp['path'] not in fixed,'missing historical not current mandatory '+oldp['path'])
 require(declaration['new_mandatory_reclassification_authorized'] is False and declaration['owning_Root_must_review_explicit_new_current_classification_before_invocation'] is True,'does not claim Root approved classification')
 require(declaration['mandatory_for_new_current_saved_science_execution'] is False and declaration['old_historical_content_currently_rehashed'] is False and declaration['old_inode_or_other_identity_fields_reconstructed_or_promoted_to_current'] is False and declaration['explicit_new_Source_package_proposed_classification']=='historical_non_live_Source_generation_origin_only','honest explicit proposed historical Source classification')
require(sorted(historical,key=lambda p:p['path'])==sorted(old['fixed_current_pins'],key=lambda p:p['path']) and len({p['path']for p in historical})==3305,'entire original3305 accounted exactly')
require(binding['historical_non_live_Source_origins']==mapping['historical_non_live_declarations'] and binding['historical_non_live_Source_origins_explicitly_reclassified'] is True,'binding explicit proposed new classification declared')
require(binding['Root_review_of_explicit_source_origin_reclassification_required_before_invocation'] is True and hf['owning_Root_review_of_explicit_four_Source_origin_classifications_required_before_invocation'] is True and cli['Root_must_review_explicit_four_nonlive_Source_origin_current_classification'] is True,'Root review prerequisite disclosed in BIND HF CLI')
require(binding['original_nonlive_source_fields_are_historical_only_not_current_PF'] is True and binding['fresh_current_input_declaration_changes_four_Source_origin_mandatory_classifications'] is True and mapping['new_current_dataset_declaration_not_unmodified_v1_execution_identity'] is True and hf['current_dataset_is_new_declaration_not_unmodified_old3305_mandatory_identity'] is True,'new current dataset not falsely original unchanged execution identity')
science1=(V1/'audit_saved_terminal_source_all370.py').read_bytes();science2=(V2/'audit_saved_terminal_source_all370.py').read_bytes()
require(science1==science2 and len(science2)==29339 and hashlib.sha256(science2).hexdigest()=='2027ec61895902575165869d753926808e882e5233e89c26a3ca9c973408024f','science29339 bytes unchanged actual SHA')
m1=(V1/'ACTUAL_INPUT_PIN_PLAN_UNRUN.json').read_text();m2=(V2/'ACTUAL_INPUT_PIN_PLAN_UNRUN.json').read_text();mc=inverse['manifest_only_literal_rebind']
require(m2.count(mc['new_literal'])==1 and m2.replace(mc['new_literal'],mc['old_literal'])==m1,'manifest whole inverse one Source path')
manifest=json.loads(m2);old_manifest=json.loads(m1)
require(manifest['inputs']==old_manifest['inputs'] and len(manifest['inputs'])==1129 and manifest['roles']==old_manifest['roles'],'all scientific inputs1129 and roles unchanged')
require(manifest['source']==dict(path=sf['source_pin']['path'],sha256=sf['source_pin']['sha256']),'science self manifest exact actual Source binding')
require(len(sf['actual_current1129_input_pins'])==len(binding['science_original_input_pins'])==1129 and sf['actual_current1129_input_pins']==binding['science_original_input_pins'],'SF and binding scientific current1129 exact')
require({p['path']:p['sha256']for p in binding['science_original_input_pins']}==manifest['inputs'],'all1129 scientific actual SHA and unique path coverage')
for oldp,newp in zip(old['science_original_input_pins'],binding['science_original_input_pins']):
 verify(newp);require(current_only_device(oldp,newp) and current.get(newp['path'])==newp,'each scientific input original only device change')
require(sf['complete_scientific_input_bytes']==sum(p['size_bytes']for p in binding['science_original_input_pins'])==102109901,'scientific input exact102109901 bytes')
host1=(V1/'run_actual_saved_full370_terminal_source_original_guard.py').read_text();host2=(V2/'run_actual_saved_full370_terminal_source_original_guard.py').read_text();restored=host2
require(len(inverse['complete_host_literal_changes'])==6,'complete six host change statements')
for change in reversed(inverse['complete_host_literal_changes']):
 require(restored.count(change['new_literal'])==1,'unique exact complete host delta '+change['label']);restored=restored.replace(change['new_literal'],change['old_literal'])
require(restored==host1,'whole original host byte inverse restored')
require(hashlib.sha256(host2.encode()).hexdigest()=='ee1e1b7512cbd8a9cd7a68633bd307d82e1dfdd5956486670244117ec7d89883','host unchanged since independent draft review')
oldhf=json.loads((V1/'COMPLETE_SAVED_FULL370_GUARD_HOST_SOURCE_FREEZE.json').read_text())
require(hf['original_unmodified_v1_source_freeze_current_pin']['sha256']=='4d055da1ac86aa69fabfcfe85b113a7b332d72c4017cc7a5d1a67174cf036817','unmodified historical Source HF current fullpin')
for oldp in oldhf['fixed_source_files']:
 actual=pin(oldp['path']);require(current_only_device(oldp,actual),'original HF Source entry only device transition '+oldp['path']);require(actual in hf['fixed_source_files'] and fixed.get(actual['path'])==actual,'original HF actual Source remains mandatory')
require(binding['original_v1_binding_current_pin']==pin(V1/'CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json'),'actual original binding available unmodified current')
for field in ('original_science_source_pin','original_input_plan_pin'):require(binding[field]==old[field],'old nonlive origin fields unchanged explicitly historical '+field)
science_command=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',binding['science_source_pin']['path'],'--manifest',binding['science_manifest_pin']['path'],'--manifest-sha256',binding['science_manifest_pin']['sha256'],'--source-sha256',binding['science_source_pin']['sha256'],'--out','/private/tmp/SPOT_AAA_full370_terminal_source_CURRENT_MOUNT_ACTUAL_ONCE_20261013_v2']
require(binding['planned_science_command']==science_command,'exact one complete science command Source manifest output')
expected_argv=['env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1','/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',hf['host_pin']['path'],'--freeze-sha256',hfp['sha256'],'--freeze-seven-id',json.dumps(hfp['identity'],separators=(',',':'))]
require(cli['argv']==expected_argv and all(isinstance(arg,str)for arg in cli['argv']),'actual CLI all strings exact env Source HF real SHA7ID')
require(json.loads(cli['argv'][-1])==hfp['identity'] and all(type(n)is int for n in json.loads(cli['argv'][-1])),'argv7ID exact integer digits no JS floating conversion')
require(cli['shell_safe_command']==shlex.join(expected_argv) and shlex.split(cli['shell_safe_command'])==expected_argv,'shell-safe exact command roundtrip')
require(cli['planned_actual_TMP_output']==science_command[-1] and cli['planned_actual_ART_output']=='/Users/wen/spot/validation/artifacts/axial-material-AAA-saved-full370-terminal-source-diagnostic-current-mount-guarded-20261013-v2','output plans exact fresh Source host namespaces')
require(not os.path.lexists(cli['planned_actual_TMP_output']) and not os.path.lexists(cli['planned_actual_ART_output']),'no business outputs exist actual source-only state')
require(cli['requires_actual_three_plane_GLOBAL_and_online_BOOT_closed0_before_invocation'] is True and cli['no_upstream_qualification_granted'] is True,'true upstream Root order gate preserved')
require(hf['science_source_imported'] is False and hf['science_executed'] is False and sf['candidate_imported_or_executed'] is False and binding['candidate_imported_or_executed'] is False,'metadata no scientific execution claimed')
for obj in (hf,sf,binding):
 for k in ('AAA_qualified','ABA_admitted'):require(obj[k] is False,'no qualification inherited '+k)
require(hf['goal_complete'] is False and sf['goal_complete'] is False and binding['new_v8_future_report_pin_invented'] is False and hf['future_v8_or_other_business_output_PF_invented'] is False,'no goal or future v8 qualification fabricated')
require(sf['known_NDIM3_axes']==[0,2,6] and sf['unknown_NDIM3_axes']==[1,3,4,5,7,8] and(sf['groups'],sf['regions'],sf['axial_cells'],sf['SN'],sf['rank'])==(370,8,48,32,1),'original scientific scope unknown six moments preserved')
writers=[]
for p in sorted((V2/'Source_only_writers').iterdir()):
 require(p.is_file() and p.suffix=='.py','durable Source writer file');q=pin(p);verify(q);require(fixed.get(str(p))==q,'durable writer is actual mandatory fixed source '+str(p));writers.append(q)
 tree=ast.parse(p.read_text());require(not any(isinstance(n,(ast.Import,ast.ImportFrom)) and any(alias.name.split('.')[0]in('subprocess','numpy','importlib') for alias in n.names)for n in ast.walk(tree)),'writer no candidate/science/compiler importing modules '+p.name)
 require(not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id in('eval','exec','compile','__import__')for n in ast.walk(tree)),'writer no dynamic candidate execution '+p.name)
require(len(writers)==3,'three durable non-TMP writer Sources')
finalizer_receipt=load('ACTUAL_SOURCE_ONLY_FINALIZER_TRUE_CLOSED_TOOL_RETURN.json');require(finalizer_receipt['chunk_id']=='969b38' and finalizer_receipt['exit_code']==0,'actual source-only finalizer true closed0 receipt')
actual_finalizer=json.loads(finalizer_receipt['output']);require(actual_finalizer['science_executed'] is False and actual_finalizer['Source_only'] is True,'finalizer actual no science claim')
for field in ('science_source','science_manifest','host','input_binding','current_mapping','science_freeze','host_freeze','real_Source_only_CLI'):verify(actual_finalizer[field])
for row in (pin(V2/'ROOT_REVIEWABLE_EXACT_SAVED_FULL370_V2_ARGV_SOURCE_ONLY.json'),pin(V2/'ACTUAL_SOURCE_ONLY_FINALIZER_TRUE_CLOSED_TOOL_RETURN.json')):verify(row)
# Observe Source package actual invariance again, without reading candidate code as executable.
for row in list(verified.values()):require(seven(Path(row['path']).lstat())==row['identity'],'all current declared files unchanged after full review '+row['path'])
report=dict(schema='INDEPENDENT_SAVED_FULL370_FINAL_CURRENT_MOUNT_FROZEN_SOURCE_REVIEW_V1',status='FINAL_FROZEN_SOURCE_REVIEW_PASS_ROOT_UPSTREAM_AND_CLASSIFICATION_GATES_STILL_REQUIRED',Source_blockers=[],release_prerequisites=['Owning Root must record explicit review of four historical nonlive Source-origin current classifications; no human reauthorization is required for this routine authorized metadata choice.','Owning Root must verify actual true successful current three-plane GLOBAL and online BOOT before diagnostic invocation. No upstream business evidence was assessed or invented by this review.'],host_freeze_pin=hfp,science_freeze_pin=pin(V2/'COMPLETE_SAVED_FULL370_SCIENCE_SOURCE_FREEZE.json'),input_binding_pin=pin(V2/'CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json'),current_mapping_pin=pin(V2/'COMPLETE_SAVED_FULL370_EXPLICIT_CURRENT_MOUNT_INPUT_MAPPING.json'),real_cli_pin=pin(V2/'ROOT_REVIEWABLE_EXACT_SAVED_FULL370_V2_ARGV_SOURCE_ONLY.json'),selected_actual_catalog_pin=catalog,unmodified_original_HF_current_pin=hf['original_unmodified_v1_source_freeze_current_pin'],source_only_writers_current_pins=writers,actual_unique_files_fullEOF=len(verified),actual_unique_bytes_fullEOF=sum(p['size_bytes']for p in verified.values()),current_live_original_mandatory_inputs=3301,current_binding_fixed_inputs=3315,original_historical_inputs_accounted=3305,historical_nonlive_source_only_no_current_PF=4,complete_science_inputs=1129,complete_science_bytes=102109901,science_Source_wholebytes_unchanged=True,host_complete_inverse_change_count=6,manifest_complete_inverse_change_count=1,all_current_PF_real_fullEOF_and_seven_fields=True,original_guard_MRO_and_resources_Source_unchanged=True,original_actual_TMP_plus_ART_counts_caps_math_thresholds_unchanged=True,late_summary_own_nlink1_samefd_fullEOF_failure_update_and_final_bytes_checked=True,argv_exact_real_HF_seven_integer_digits=True,historical_reattestation_not_science_execution=True,Root_approval_not_claimed=True,upstream_v8_future_PF_invented=False,candidate_imported=False,candidate_compiled=False,candidate_executed=False,science_numeric_result_produced=False,GLOBAL_or_BOOT_passed_by_this_review=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,checks=checks,elapsed_seconds=time.monotonic()-start,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
require(report['SELF_peak_bytes']<512*2**20 and report['elapsed_seconds']<1800,'finite review bounded');report['checks']=checks
write(OUT/'FINAL_POSTFREEZE_SOURCE_REVIEW.json',report)
print(json.dumps(dict(status=report['status'],report_pin=pin(OUT/'FINAL_POSTFREEZE_SOURCE_REVIEW.json'),checks=checks,files=report['actual_unique_files_fullEOF'],bytes=report['actual_unique_bytes_fullEOF'],Source_blockers=[],elapsed_seconds=report['elapsed_seconds'],SELF_peak_bytes=report['SELF_peak_bytes'])))
