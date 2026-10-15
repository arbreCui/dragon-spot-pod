"""Read actual PREP43 and frozen SOURCE31; never execute business code or phases."""
import ast
import copy
import hashlib
import json
import struct
from pathlib import Path

D=Path(__file__).resolve().parent
ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
S=ART/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-cold-source-v12-20261009'
W=ART/'axial-material-owned-specs-identity-key-delta-graph-table-cold-runtime-v12-20261009'
T=ART/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-cold-terminal-v12-20261009'
R=ROOT/'validation/axial_material/identity_key_delta_graph_table_combined_runtime_review_v12_20261009'
PINS={}

def pin(path,wanted=None):
    path=Path(path);assert path.is_file()and not path.is_symlink(),path
    before=path.stat();h=hashlib.sha256()
    with path.open('rb')as stream:
        for block in iter(lambda:stream.read(1<<20),b''):h.update(block)
    after=path.stat();assert(before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns)
    item=dict(path=str(path),sha256=h.hexdigest(),bytes=before.st_size)
    if wanted is not None:assert item['sha256']==wanted,(path,item['sha256'],wanted)
    PINS[str(path)]=item;return item

def read(path,wanted=None):
    pin(path,wanted);return json.loads(Path(path).read_text())

def exact(a,b):
    if type(a)is not type(b):return False
    if isinstance(a,float):return struct.pack('>d',a)==struct.pack('>d',b)
    if isinstance(a,dict):return a.keys()==b.keys()and all(exact(a[k],b[k])for k in a)
    if isinstance(a,list):return len(a)==len(b)and all(exact(x,y)for x,y in zip(a,b))
    return a==b

prior=read(D/'REPORT_SOURCE31.json','b6791ae7541eac08d718de7a114fecd02dc85719ab101dfd7f106c6c4404a525')
assert prior['status']=='PASS_ACTUAL_DECLARATION_SOURCE31_INPUT_POINTERS_AND_SOURCE_INVERSES_ONLY'
seal=read(S/'factory_seal.json','d182259bb17b580bbe45fe1853168c188515ef0b5ef654cfe7a72b668c32f3d5')
assert {p.name for p in S.iterdir()}==set(seal['files'])|{'factory_seal.json'}
for name,wanted in seal['files'].items():pin(S/name,wanted)
assert len(seal['files'])==30
decl=read(S/'declaration.json','758db9578a8b259afd8da2faf1f50614e6d4f581a0922d22083824350fdfd75d')
prepared=read(W/'prepared.json','ec3db7fcf10c2fc4b63b6dc89283f29b2067dc97aebb29b67e5aaa1731b5429c')
root=read(R/'Root_actual_cold_prepare_tool_terminal_return.json')
typed=read(R/'Root_actual_cold_prepare_tool_input.json')
assert root['actual_initial_tool_result']==typed['actual_initial_tool_result']and root['actual_terminal_tool_result']==typed['actual_terminal_tool_result']
assert root['actual_tool']==dict(initial_chunk_id='872a6e',session_id=5541,terminal_chunk_id='afa282',exit_code=0)
assert typed['actual_initial_tool_result']['session_id']==5541 and typed['actual_initial_tool_result']['chunk_id']=='872a6e'
assert typed['actual_terminal_tool_result']['chunk_id']=='afa282'and type(typed['actual_terminal_tool_result']['exit_code'])is int and typed['actual_terminal_tool_result']['exit_code']==0 and 'session_id'not in typed['actual_terminal_tool_result']
assert root['session_closed']is True and root['actual_tool_terminal_return_observed']is True
assert root['prepared']==dict(path=str(W/'prepared.json'),sha256=PINS[str(W/'prepared.json')]['sha256'])
for key in ['full_stdout','full_stderr']:pin(root[key]['path'],root[key]['sha256'])
assert Path(root['full_stderr']['path']).read_bytes()==b''
wrapper=json.loads(Path(root['full_stdout']['path']).read_text())
assert wrapper==dict(classification='PREPARED_NO_TRANSPORT',prepared=str(W/'prepared.json'),sha256=PINS[str(W/'prepared.json')]['sha256'])
assert prepared['classification']==wrapper['classification']and prepared!=wrapper
assert root['local_files']==prepared['local_files']and len(prepared['local_files'])==43
for relative,wanted in prepared['local_files'].items():
    assert not Path(relative).is_absolute()and '..'not in Path(relative).parts
    pin(W/relative,wanted)
actual_local=set()
for directory in ['runtime','decks']:
    for path in (W/directory).iterdir():
        assert path.is_file()and not path.is_symlink(),path
        actual_local.add(str(path.relative_to(W)))
actual_local.add('declaration.json')
assert actual_local==set(prepared['local_files'])
assert (W/'declaration.json').read_bytes()==(S/'declaration.json').read_bytes()

m=read(S/'rank1_factor_cache_admission.json')
assert (W/'runtime/rank1_factor_cache_admission.json').read_bytes()==(S/'rank1_factor_cache_admission.json').read_bytes()
source_copies=[]
for relative in prepared['local_files']:
    if relative.startswith('runtime/')and (S/Path(relative).name).exists():
        assert (W/relative).read_bytes()==(S/Path(relative).name).read_bytes()
        source_copies.append(relative)
assert len(source_copies)==18
for name,item in prepared['runtime_sources'].items():
    pin(item['path'],item['sha256'])
    assert prepared['local_files']['runtime/'+name]==item['sha256']
    assert (W/'runtime'/name).read_bytes()==Path(item['path']).read_bytes()
assert prepared['runtime_sources']['Dragon']==m['combined_runtime']
declterm=read(T/'declaration_terminal_return.json','66c0647d69ba276460a84a09cee6502b272ded07c5b24b5f3509a64ae47d0b2c')
assert prepared['declaration']==declterm['declaration']
assert prepared['case_spec']==decl['case_spec']and prepared['rank_addendum']==decl['rank_addendum']and prepared['inputs']==decl['inputs']
assert prepared['budgets']==decl['budgets']==prior['original_budget_fields']and prepared['production_config']==decl['production_config']==prior['original_production_config']
assert prepared['resource_roots']==decl['resource_roots']and prepared['artifact_root']==str(ART)

parent_path=Path(m['parent_prepared']['path']);parent=read(parent_path,m['parent_prepared']['sha256']);old=parent_path.parent
assert prepared.keys()==parent.keys()
inverse=copy.deepcopy(prepared)
changed=[('experiment_id',),('case_spec',),('declaration',),('rank_addendum',),('resource_roots',),('preflight_resources',),('local_files',),('runtime_sources',),('inputs','material_results'),('producer_admission','online_receiver_sha256')]
for path in changed:
    a,b=inverse,parent
    for key in path[:-1]:a,b=a[key],b[key]
    a[path[-1]]=copy.deepcopy(b[path[-1]])
assert exact(inverse,parent)
assert prepared['snapshot_control_audits']==parent['snapshot_control_audits']
assert prepared['producer_admission']['states']==parent['producer_admission']['states']and prepared['producer_admission']['coupled_qualified']is False
runtime_inverse=copy.deepcopy(prepared['runtime_sources']);runtime_inverse['Dragon']=parent['runtime_sources']['Dragon'];assert runtime_inverse==parent['runtime_sources']

manifest=read(W/'decks/production_inputs.json');proof=read(W/'decks/deferred_snapshot_inverse.json')
assert manifest['runner_deferred_snapshot_inputs']==proof
assert manifest['config']==prepared['production_config']and manifest['case_slots']==dict(AAA=list('AAA'),ABA=list('ABA'))
assert proof['original_budgets']==prepared['budgets']and proof['AAA_accuracy_qualified']is False and proof['ABA_admitted']is False
deck_inverses={}
for name,item in proof['independent_deck_inverses'].items():
    candidate=(W/'decks'/name).read_text();restored=candidate
    assert hashlib.sha256(candidate.encode()).hexdigest()==item['candidate_file_snapshot_sha256']==manifest['deck_sha256'][name]
    for operation in item['inverse_operations']:
        assert restored.count(operation['remove'])==1
        restored=restored.replace(operation['remove'],operation['restore'],1)
    assert hashlib.sha256(restored.encode()).hexdigest()==item['original_sha256']
    original=old/'decks'/name;pin(original,item['original_sha256']);assert restored.encode()==original.read_bytes()
    deck_inverses[name]=dict(original_sha256=item['original_sha256'],candidate_sha256=item['candidate_file_snapshot_sha256'],complete_byte_inverse=True,original_scientific_order_retained=True,inverse_regions=len(item['inverse_operations']))
assert set(deck_inverses)=={'bootstrap_axial.x2m','picard_axial.x2m'}
other_decks=[]
for relative in prepared['local_files']:
    if relative.startswith('decks/')and relative.endswith('.x2m')and Path(relative).name not in deck_inverses:
        original=old/relative;pin(original,parent['local_files'][relative]);assert original.read_bytes()==(W/relative).read_bytes();other_decks.append(relative)
parent_manifest=read(old/'decks/production_inputs.json',parent['local_files']['decks/production_inputs.json'])
restored_manifest=copy.deepcopy(manifest);del restored_manifest['runner_deferred_snapshot_inputs']
for name,item in proof['independent_deck_inverses'].items():restored_manifest['deck_sha256'][name]=item['original_sha256']
assert exact(restored_manifest,parent_manifest)
assert prepared['preflight_resources']['artifact_budget_bytes']==96*2**30 and prepared['preflight_resources']['min_free_bytes']==8*2**30
assert prepared['preflight_resources']['artifact_bytes']<96*2**30 and prepared['preflight_resources']['disk_free_bytes']>8*2**30
assert m['new_binding_controls_not_yet_executed']is True
for obj in [m,root]:
    for key in ['AAA_accuracy_qualified','ABA_admitted']:assert obj[key]is False

report=dict(schema='AXMAT_V12_SOURCE31_AND_ACTUAL_PREP43_INDEPENDENT_READONLY_REVIEW_V1',status='PASS_ACTUAL_SOURCE_DECLARATION_AND_PREP43_NO_BINDING_NATIVE_OR_SCIENCE',
    frozen_SOURCE31_review=PINS[str(D/'REPORT_SOURCE31.json')],full_SOURCE31_namespace_rehashed_unchanged=True,
    actual_prepare_tool=root['actual_tool'],actual_prepare_typed_terminal_closed_exit0=True,Root_prepare_receipt=PINS[str(R/'Root_actual_cold_prepare_tool_terminal_return.json')],
    full_stdout_wrapper_path_SHA_and_classification_match_prepared=True,stdout_wrapper_not_mistaken_for_full_prepared_document=True,full_stderr_empty=True,
    prepared=PINS[str(W/'prepared.json')],prepared_classification='PREPARED_NO_TRANSPORT',prepared_local_files=43,prepared_all43_full_hashes_verified=True,
    whole_prepared_local_namespace_exact_runtime_decks_and_declaration=True,source_to_runtime_byte_copies=source_copies,runtime_source_copies_byteexact=True,
    original_prepared_schema_and_full_body_after10_explicit_metadata_inverse_changes_exact=True,prepared_inverse_changed_paths=changed,
    original_physical_A_B_snapshot_track_payload_controls_and_producer_states_exact=True,only_online_receiver_and_explicit_source_resource_local_identity_changes=True,
    deck_inverse=deck_inverses,other_decks_byteexact=other_decks,entire_production_inputs_manifest_complete_inverse_to_original=True,
    all_current_SOURCE_metadata_pointers_and_schema_verified_by_unchanged_SOURCE31=True,true_declaration_terminal66c_bound=True,
    budgets=prepared['budgets'],production_config=prepared['production_config'],original_512_96GiB_8GiB_threads1_child1_retries0_retained=True,
    actual_preparation_observed=True,cold_prepared=True,prepare_binding_result_not_observed_or_claimed=True,controls_qualified=False,
    native_RSS_verified=False,actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False,
    no_business_import=True,no_business_call=True,no_fixture_or_phase_execution=True,no_Root_poll=True,no_project_write=True,no35GB_historical_payload_mass_hash=True,evidence_pins=PINS)
text=json.dumps(report,ensure_ascii=False,indent=2)+'\n';(D/'REPORT_SOURCE31_PREP43.json').write_text(text)
print(json.dumps(dict(status=report['status'],report=str(D/'REPORT_SOURCE31_PREP43.json'),report_sha256=hashlib.sha256(text.encode()).hexdigest(),locals=43,source_files=31,source_copies=len(source_copies),decks=len(deck_inverses)+len(other_decks),binding_claimed=False),ensure_ascii=False))
