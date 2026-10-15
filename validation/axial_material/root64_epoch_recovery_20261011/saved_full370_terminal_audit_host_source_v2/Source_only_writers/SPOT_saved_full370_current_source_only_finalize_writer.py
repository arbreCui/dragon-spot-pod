import ast,hashlib,json,os,shlex,stat,time
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011');OLD=REC/'saved_full370_terminal_audit_host_source_v1';NEW=REC/'saved_full370_terminal_audit_host_source_v2'
PY=Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')
def sid(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);before=sid(p.lstat());assert stat.S_ISREG(before[2]),str(p)
    count=0;h=hashlib.sha256()
    with p.open('rb')as f:
        assert sid(os.fstat(f.fileno()))==before
        while True:
            raw=f.read(2**20)
            if not raw:break
            h.update(raw);count+=len(raw)
        assert count==before[4]and sid(os.fstat(f.fileno()))==before
    assert sid(p.lstat())==before
    return dict(path=str(p),sha256=h.hexdigest(),size_bytes=count,identity=before)
def write(p,value):
    if isinstance(value,dict):value=(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    if isinstance(value,str):value=value.encode()
    with p.open('xb')as f:f.write(value);f.flush();os.fsync(f.fileno())
old=json.loads((OLD/'CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json').read_text())
draft=NEW/'PRELIMINARY_ALL_LIVE_INPUTS_FULL_EOF_CURRENT_MAPPING.json';mapping=json.loads(draft.read_text())
assert len(old['fixed_current_pins'])==3305 and len(mapping['rows'])==3301 and len(mapping['historical_non_live_declarations'])==4 and not mapping['errors']
for row in mapping['rows']:
    historical=row['historical_pin'];current=row['current_pin']
    assert pin(current['path'])==current
    assert(historical['path'],historical['sha256'],historical['size_bytes'],historical['identity'][1:])==(current['path'],current['sha256'],current['size_bytes'],current['identity'][1:])
    assert historical['identity'][0]in(16777234,16777229)and current['identity'][0]==16777229
allold=[r['historical_pin']for r in mapping['rows']]+[r['historical_pin']for r in mapping['historical_non_live_declarations']]
assert sorted(allold,key=lambda p:p['path'])==sorted(old['fixed_current_pins'],key=lambda p:p['path'])
science={r['historical_pin']['path']:r['current_pin']for r in mapping['rows']}
scientific=[science[p['path']]for p in old['science_original_input_pins']]
assert len(scientific)==1129
manifest=json.loads((NEW/'ACTUAL_INPUT_PIN_PLAN_UNRUN.json').read_text());original_manifest=json.loads((OLD/'ACTUAL_INPUT_PIN_PLAN_UNRUN.json').read_text())
assert manifest['inputs']==original_manifest['inputs']and len(manifest['inputs'])==1129
assert {r['path']:r['sha256']for r in scientific}==manifest['inputs']
source=pin(NEW/'audit_saved_terminal_source_all370.py');assert source['sha256']=='2027ec61895902575165869d753926808e882e5233e89c26a3ca9c973408024f'and(OLD/'audit_saved_terminal_source_all370.py').read_bytes()==(NEW/'audit_saved_terminal_source_all370.py').read_bytes()
old_source_proof=json.loads((OLD/'COMPLETE_SAVED_FULL370_SOURCE_AND_HOST_DERIVATION.json').read_text())
v1bytes=(OLD/'ACTUAL_INPUT_PIN_PLAN_UNRUN.json').read_bytes()
restored_tmp_plan=v1bytes.replace(old_source_proof['new_literal'].encode(),old_source_proof['old_literal'].encode())
assert hashlib.sha256(restored_tmp_plan).hexdigest()==old['original_input_plan_pin']['sha256']
assert source['sha256']==old['original_science_source_pin']['sha256']
mapping['schema']='SAVED_FULL370_EXPLICIT_CURRENT_MOUNT_REATTESTATION_SOURCE_V2'
mapping['source_draft_predecessor_current_pin']=pin(draft)
mapping['new_current_dataset_declaration_not_unmodified_v1_execution_identity']=True
mapping['executable_host_freeze_declared']=False
mapping['current_input_binding_reclassification_scope']='3301 genuine live original fixed rows remain mandatory; four absent prior TMP Source-generation origins remain fully recorded historical PF only, never current PF or current mandatory execution dependencies. All1129 scientific inputs unchanged.'
mapping['original_missing_mandatory_not_silently_dropped']=True
for row in mapping['historical_non_live_declarations']:
    assert not Path(row['historical_pin']['path']).exists()and not Path(row['historical_pin']['path']).is_symlink()
    assert row['current_pin']is None and row['in_scientific_1129_inputs']is False
    row['new_mandatory_reclassification_authorized']=False
    row['explicit_new_Source_package_proposed_classification']='historical_non_live_Source_generation_origin_only'
    row['mandatory_for_new_current_saved_science_execution']=False
    row['old_historical_content_currently_rehashed']=False
    row['old_inode_or_other_identity_fields_reconstructed_or_promoted_to_current']=False
    row['owning_Root_must_review_explicit_new_current_classification_before_invocation']=True
mapping_path=NEW/'COMPLETE_SAVED_FULL370_EXPLICIT_CURRENT_MOUNT_INPUT_MAPPING.json';write(mapping_path,mapping)
mapping_pin=pin(mapping_path)
baseline_freeze=OLD/'COMPLETE_SAVED_FULL370_GUARD_HOST_SOURCE_FREEZE.json';baseline_freeze_pin=pin(baseline_freeze)
assert baseline_freeze_pin['sha256']=='4d055da1ac86aa69fabfcfe85b113a7b332d72c4017cc7a5d1a67174cf036817'
baseline=json.loads(baseline_freeze.read_text());baseline_rows=[]
for row in baseline['fixed_source_files']:
    actual=pin(row['path']);assert actual['sha256']==row['sha256']and actual['size_bytes']==row['size_bytes']and actual['identity'][1:]==row['identity'][1:]and actual['identity'][0]==16777229
    baseline_rows.append(actual)
host=NEW/'run_actual_saved_full370_terminal_source_original_guard.py';host_pin=pin(host);ast.parse(host.read_text())
inverse=NEW/'COMPLETE_SAVED_FULL370_SOURCE_AND_HOST_BYTE_INVERSE_DRAFT.json';proof=json.loads(inverse.read_text());assert proof['complete_host_inverse_equal']and len(proof['complete_host_literal_changes'])==6
text=host.read_text()
for row in reversed(proof['complete_host_literal_changes']):
    assert text.count(row['new_literal'])==1;text=text.replace(row['new_literal'],row['old_literal'])
assert text==(OLD/'run_actual_saved_full370_terminal_source_original_guard.py').read_text()
oldpin=pin(OLD/'CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json')
binding=dict(old)
binding['schema']='CURRENT_SAVED_FULL370_TERMINAL_SOURCE_ORIGINAL_GUARD_INPUT_BINDING_EXPLICIT_CURRENT_MOUNT_V2'
binding['science_original_input_pins']=scientific
binding['science_source_pin']=source
binding['science_manifest_pin']=pin(NEW/'ACTUAL_INPUT_PIN_PLAN_UNRUN.json')
binding['formal_prepared_pin']=science[old['formal_prepared_pin']['path']]
binding['formal_case_spec_pin']=science[old['formal_case_spec_pin']['path']]
binding['planned_science_command']=[str(PY),'-B',source['path'],'--manifest',binding['science_manifest_pin']['path'],'--manifest-sha256',binding['science_manifest_pin']['sha256'],'--source-sha256',source['sha256'],'--out','/private/tmp/SPOT_AAA_full370_terminal_source_CURRENT_MOUNT_ACTUAL_ONCE_20261013_v2']
binding['original_v1_binding_current_pin']=oldpin
binding['complete_current_mount_mapping_pin']=mapping_pin
binding['historical_non_live_Source_origins_explicitly_reclassified']=True
binding['historical_non_live_Source_origins']=mapping['historical_non_live_declarations']
binding['Root_review_of_explicit_source_origin_reclassification_required_before_invocation']=True
binding['all_original3305_declarations_accounted']=True
binding['actual_live_original_mandatory_input_count']=3301
binding['historical_nonlive_original_Source_origin_count']=4
binding['all1129_scientific_input_path_SHA_pairs_exactly_preserved']=True
binding['original_nonlive_source_fields_are_historical_only_not_current_PF']=True
binding['fresh_current_input_declaration_changes_four_Source_origin_mandatory_classifications']=True
binding['current_metadata_view_is_reattestation_not_execution']=True
binding['historical_science_or_guard_stage_reexecuted_by_reattestation']=False
binding['upstream_three_plane_or_BOOT_qualification_granted_by_this_Source']=False
binding['new_v8_future_report_pin_invented']=False
fixed={r['current_pin']['path']:r['current_pin']for r in mapping['rows']}
extra=baseline_rows+[baseline_freeze_pin,oldpin,source,binding['science_manifest_pin'],host_pin,mapping_pin,pin(draft),pin(inverse),mapping['selected_actual_catalog_pin'],pin(Path(__file__).resolve()),pin(NEW/'Source_only_writers/SPOT_saved_full370_current_source_only_rebind.py'),pin(NEW/'Source_only_writers/SPOT_saved_full370_current_source_only_draft_writer.py')]
for row in extra:
    assert pin(row['path'])==row
    if row['path']in fixed:assert fixed[row['path']]==row
    fixed[row['path']]=row
binding['fixed_current_pins']=[fixed[p]for p in sorted(fixed)]
binding_path=NEW/'CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json';write(binding_path,binding);binding_pin=pin(binding_path)
science_sf=dict(schema='COMPLETE_SAVED_FULL370_SCIENCE_SOURCE_CURRENT_MOUNT_FREEZE_ONLY_V2',source_pin=source,science_manifest_pin=binding['science_manifest_pin'],original_science_current_pin=pin(OLD/'audit_saved_terminal_source_all370.py'),original_manifest_current_pin=pin(OLD/'ACTUAL_INPUT_PIN_PLAN_UNRUN.json'),actual_current1129_input_pins=scientific,complete_scientific_input_bytes=sum(r['size_bytes']for r in scientific),scientific_Source_complete_bytes_unchanged=True,manifest_only_self_source_path_literal_rebound=True,all1129_original_input_path_SHA_pairs_exactly_preserved=True,explicit_current_mapping_pin=mapping_pin,input_binding_pin=binding_pin,source_inverse_draft_pin=pin(inverse),source_only=True,candidate_imported_or_executed=False,compiler_or_transport_executed=False,known_NDIM3_axes=[0,2,6],unknown_NDIM3_axes=[1,3,4,5,7,8],groups=370,regions=8,axial_cells=48,SN=32,rank=1,all32_fission_components_and_P0_P1_P2_preserved=True,no_clip_no_drop_no_local_renormalization=True,original_physics_thresholds_changed=False,full_neutron_balance_qualified=False,full_eigen_reference_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
sfpath=NEW/'COMPLETE_SAVED_FULL370_SCIENCE_SOURCE_FREEZE.json';write(sfpath,science_sf);sfpin=pin(sfpath)
fixedsource=[pin(NEW/name)for name in ('audit_saved_terminal_source_all370.py','ACTUAL_INPUT_PIN_PLAN_UNRUN.json','run_actual_saved_full370_terminal_source_original_guard.py','CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json','COMPLETE_SAVED_FULL370_EXPLICIT_CURRENT_MOUNT_INPUT_MAPPING.json','COMPLETE_SAVED_FULL370_SCIENCE_SOURCE_FREEZE.json','COMPLETE_SAVED_FULL370_SOURCE_AND_HOST_BYTE_INVERSE_DRAFT.json','PRELIMINARY_ALL_LIVE_INPUTS_FULL_EOF_CURRENT_MAPPING.json')]+baseline_rows+[baseline_freeze_pin]
freeze=dict(schema='COMPLETE_SAVED_FULL370_TERMINAL_SOURCE_GUARD_HOST_FREEZE_ONLY_V2',fixed_source_files=fixedsource,input_binding_pin=binding_pin,host_pin=host_pin,selected_actual_science_source_freeze_pin=sfpin,selected_actual_current_mapping_pin=mapping_pin,original_unmodified_v1_source_freeze_current_pin=baseline_freeze_pin,source_only=True,science_source_imported=False,science_executed=False,compiler_or_transport_executed=False,upstream_three_plane_or_BOOT_qualification_granted=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,workflow_order='Root invokes only after true three-plane publication and online BOOT; not qualification granted by this freeze',resources='original stage600/whole1800/SELF-and-child512MiB/one-thread/one-child/no-retry; initial fresh2GiB/cold96GiB/free8GiB plus cold reserve20971764748 and metadata64MiB; actual TMP bytes explicitly added to ART history/fresh totals and both filesystem floors; scientific output64MiB unchanged; summary bytes forced original postwrite resources.check()',current_dataset_is_new_declaration_not_unmodified_old3305_mandatory_identity=True,complete_original3305_accounting=dict(actual_live_mandatory=3301,historical_nonlive_Source_origins_no_current_PF=4,scientific_current_inputs=1129),owning_Root_review_of_explicit_four_Source_origin_classifications_required_before_invocation=True,future_v8_or_other_business_output_PF_invented=False)
freeze_path=NEW/'COMPLETE_SAVED_FULL370_GUARD_HOST_SOURCE_FREEZE.json';write(freeze_path,freeze);freezepin=pin(freeze_path)
argv=['env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1',str(PY),'-B',str(host),'--freeze-sha256',freezepin['sha256'],'--freeze-seven-id',json.dumps(freezepin['identity'],separators=(',',':'))]
cli=dict(schema='SOURCE_ONLY_REAL_CURRENT_SAVED_FULL370_V2_ARGV_UNEXECUTED',argv=argv,shell_safe_command=shlex.join(argv),Source_freeze_pin=freezepin,host_pin=host_pin,selected_actual_science_source_freeze_pin=sfpin,input_binding_pin=binding_pin,current_mapping_pin=mapping_pin,planned_actual_ART_output='/Users/wen/spot/validation/artifacts/axial-material-AAA-saved-full370-terminal-source-diagnostic-current-mount-guarded-20261013-v2',planned_actual_TMP_output=binding['planned_science_command'][-1],every_PF_is_actual_Source_or_current_input_not_future_business_output=True,science_imported_or_executed=False,no_upstream_qualification_granted=True,requires_actual_three_plane_GLOBAL_and_online_BOOT_closed0_before_invocation=True,Root_must_review_explicit_four_nonlive_Source_origin_current_classification=True)
cli_path=NEW/'ROOT_REVIEWABLE_EXACT_SAVED_FULL370_V2_ARGV_SOURCE_ONLY.json';write(cli_path,cli)
for row in binding['fixed_current_pins']+fixedsource+[freezepin]:assert pin(row['path'])==row
print(json.dumps(dict(status='SAVED_FULL370_NEW_CURRENT_DATASET_SOURCE_ONLY_FREEZES_AND_REAL_CLI_WRITTEN_UNEXECUTED',science_source=source,science_manifest=binding['science_manifest_pin'],host=host_pin,input_binding=binding_pin,current_mapping=mapping_pin,science_freeze=sfpin,host_freeze=freezepin,real_Source_only_CLI=pin(cli_path),original3305_accounted=3305,current_original_mandatory=3301,historical_nonlive_origins=4,all1129_scientific_inputs_preserved=True,science_executed=False,Source_only=True),allow_nan=False))
