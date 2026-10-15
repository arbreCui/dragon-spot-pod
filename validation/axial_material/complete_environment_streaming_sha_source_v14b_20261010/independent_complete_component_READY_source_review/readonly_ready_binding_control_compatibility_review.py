"""Independent stdlib source and sealed small helper-evidence review only.
No candidate/helper/gate imports/calls, no fixture/benchmark/component execution.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import stat

D=Path('/private/tmp/axmat_v14b_ready_binding_actual_helper_evidence_readonly_review_20261010')
R=Path('/private/tmp/axmat_v14b_complete_component_ready_source_binding_20261010')
C=R/'prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14b.py'
BP=R/'COMPLETE_SOURCE_BINDING_INVERSE.json'
B=Path('/private/tmp/axmat_v14b_streaming_sha_complete_component_source_draft_20261010')
A=Path('/Users/wen/spot/validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010/Root_actual_helper_controls_admission.json')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def jsonfile(path):return json.loads(Path(path).read_bytes())
def identity(s):return (s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
craw=C.read_bytes();text=craw.decode();binding=jsonfile(BP)
assert sha(craw)=='4fbd1b054c6516b410181144f088d540a64a8ab793d480fb2c89de0d1252199c'
assert sha(BP.read_bytes())=='7844ed97cad4688eec7ce22c3e35676ec94cef8cf702d5cbced2ff09bddb3b63'
assert len(binding['edits'])==4
inverse=text
for edit in reversed(binding['edits']):
    assert set(edit)=={'name','old','new','count'}and type(edit['count'])is int and edit['count']==1
    assert inverse.count(edit['new'])==1
    inverse=inverse.replace(edit['new'],edit['old'],1)
assert inverse.encode()==Path(binding['source_parent']['path']).read_bytes()
assert sha(inverse.encode())=='b6fb702ca9a8d803722d17a1082df74a2bd693aead99b691899d9335cc40bb4f'
def records(source,classes=False):
    values={}
    def walk(node,parent):
        if isinstance(node,(ast.FunctionDef,ast.ClassDef)):
            parent=parent+(node.name,)
            if classes or isinstance(node,ast.FunctionDef):values[parent]=ast.get_source_segment(source,node)
        for child in ast.iter_child_nodes(node):walk(child,parent)
    walk(ast.parse(source),())
    return values
before=records(inverse);after=records(text)
assert len(before)==len(after)==101 and before==after
chains={}
for name,expected in (('COMPLETE_INVERSE_PROOF.json','e1cbc96cd7c46dc99b2a0a477b609abf70ea0c4338d5d0ed8840165945e5f35a'),('COMPLETE_INVERSE_TO_D2_PROOF.json','d2d2c7616d329cd8ffbf30f749de6ef8ae08d294240b653cfe8b92a3fe1c8633')):
    proof=jsonfile(B/name);restored=inverse
    for edit in reversed(proof['edits']):
        assert restored.count(edit['new'])==edit['count'];restored=restored.replace(edit['new'],edit['old'],edit['count'])
    assert restored.encode()==Path(proof['parent']['path']).read_bytes()and sha(restored.encode())==expected
    chains[name]=dict(sha256=sha((B/name).read_bytes()),regions=len(proof['edits']),inverse_sha256=expected)
tree=ast.parse(text)
selected=('SOURCE_STATUS','STREAM_ENVIRONMENT_HELPER_SHA','STREAM_ENVIRONMENT_SOURCE_PROOF_SHA','STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA','FUTURE_ACTUAL_BUILD_TERMINAL_SHA','FUTURE_ACTUAL_BUILD_SEAL_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA','ORIGINAL_STAGE_COUNT','COMPLETE_STAGE_COUNT')
values={target.id:ast.literal_eval(node.value)for node in tree.body if isinstance(node,ast.Assign)for target in node.targets if isinstance(target,ast.Name)and target.id in selected}
assert values['SOURCE_STATUS']=='READY_SOURCE_ONLY_FOR_ROOT_REVIEWED_STREAMING_SHA_COMPONENT_EXECUTION_V14B'
assert values['STREAM_ENVIRONMENT_HELPER_SHA']=='7d740b177f5e1c728f0729df031248fbb396f6978b9a3d5c8776a0c270db48d3'
assert values['STREAM_ENVIRONMENT_SOURCE_PROOF_SHA']=='1809278680379d2ef6ee5c76218d4614abbbc1c9cbcf379674e7540485db86f2'
assert values['STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA']=='16d4548b1cc4ffe935bd8d28219e99a6e9da9af949e7577a82eb758e99d7f568'
assert all(value is None for key,value in values.items()if key.startswith('FUTURE_'))
assert values['ORIGINAL_STAGE_COUNT']==68 and values['COMPLETE_STAGE_COUNT']==86

araw=A.read_bytes();controls=json.loads(araw)
assert sha(araw)==values['STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA']
assert controls['schema']=='AXMAT_COMPLETE_ENVIRONMENT_STREAMING_SHA_HELPER_CONTROLS_ADMISSION_V14'and controls['status']=='PASS_COMPLETE_HELPER_CONTROLS_ONLY'
files=controls['files'];assert type(files)is dict and len(files)==145
sizes={literal:Path(literal).stat().st_size for literal in files}
assert sum(sizes.values())<64*2**20
verified={};all_bytes=0;hardlinks=[]
for literal,wanted in files.items():
    p=Path(literal)
    assert type(literal)is str and p.is_absolute()and '..'not in p.parts and re.fullmatch('[0-9a-f]{64}',wanted)and wanted!='0'*64
    first=p.stat();assert stat.S_ISREG(first.st_mode)
    raw=p.read_bytes();last=p.stat()
    assert identity(first)==identity(last)and len(raw)==first.st_size and sha(raw)==wanted
    verified[literal]=dict(sha256=wanted,bytes=len(raw));all_bytes+=len(raw)
    if first.st_nlink>1:hardlinks.append(dict(path=literal,nlink=first.st_nlink))
def owned_json(descriptor):
    assert set(descriptor)=={'path','sha256'}and files[descriptor['path']]==descriptor['sha256']
    return jsonfile(descriptor['path'])
inventories={};archive_bytes=0
for root_key,inventory_key in (('control_root','control_inventory'),('host_root','host_inventory')):
    root=Path(controls[root_key]);assert root.is_absolute()and '..'not in root.parts and not root.is_symlink()and root.is_dir()
    observed_files={};observed_links={};observed_directories=[]
    for parent,dirs,names in os.walk(root,followlinks=False):
        observed_directories.append(str(Path(parent).relative_to(root)))
        for name in [*dirs,*names]:
            p=Path(parent)/name;relative=str(p.relative_to(root))
            if p.is_symlink():observed_links[relative]=os.readlink(p)
            elif p.is_file():
                assert str(p)in verified and stat.S_ISREG(p.stat().st_mode)
                observed_files[relative]=verified[str(p)]['sha256'];archive_bytes+=p.stat().st_size
            else:assert p.is_dir()
    observed=dict(files=observed_files,symlinks=observed_links,directories=sorted(observed_directories))
    assert observed==controls[inventory_key];inventories[inventory_key]=observed
assert controls['control_root']!=controls['host_root']and archive_bytes<64*2**20
control_root=Path(controls['control_root'])
manifest=jsonfile(control_root/'raw_preservation_manifest.json')
assert manifest['schema']=='AXMAT_HELPER_ONLY_CONTROL_RAW_PRESERVATION_V1'
assert manifest['files']=={name:value for name,value in inventories['control_inventory']['files'].items()if name!='raw_preservation_manifest.json'}
assert manifest['component_native_AAA_ABA_credit']is False and manifest['original86_stage_count_increment']==0

helper_pin=controls['helper'];proof_pin=controls['source_patch_proof']
assert helper_pin==binding['actual_helper_source']and proof_pin==binding['actual_helper_proof']
assert files[helper_pin['path']]==values['STREAM_ENVIRONMENT_HELPER_SHA']and files[proof_pin['path']]==values['STREAM_ENVIRONMENT_SOURCE_PROOF_SHA']
proof=jsonfile(proof_pin['path']);helper_source=Path(helper_pin['path']).read_text();old_source=Path(proof['parent_helper']['path']).read_text()
restored=helper_source
for edit in reversed(proof['edits']):
    assert restored.count(edit['new'])==edit['count'];restored=restored.replace(edit['new'],edit['old'],edit['count'])
assert restored==old_source and sha(restored.encode())=='619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'
old_defs=records(old_source,True);new_defs=records(helper_source,True)
assert len(old_defs)==34 and set(old_defs)<=set(new_defs)
assert [key for key in old_defs if old_defs[key]!=new_defs[key]]==[('digest',)]
old_top={node.name for node in ast.parse(old_source).body if isinstance(node,ast.FunctionDef)}
new_top={node.name for node in ast.parse(helper_source).body if isinstance(node,ast.FunctionDef)}
assert sorted(new_top-old_top)==proof['added_definitions']and len(proof['added_definitions'])==13
semantics=dict(complete_full_SHA_per_unique_literal_per_environment=True,same_call_same_literal_memo_only=True,cross_stage_SHA_reuse=False,different_literal_SHA_reuse=False,full_seven_identity_rechecks_required=True,buffer_bytes=4194304)
assert all(proof[key]==value and controls[key]==value for key,value in semantics.items())
for key in ('same_seven_identity_mutation_rejected','native_alias_policy_preserved','default_environment_rejections_retained'):assert controls[key]is True
for key in ('mathematics_changed','MRO_modified','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'):assert controls[key]is False
assert controls['full86_component_qualified']is False and controls['actual_performance_comparison']['material_time_gain_proven']is False

receipt=owned_json(controls['actual_terminal_receipt']);result=owned_json(controls['actual_result']);host=owned_json(controls['actual_host_result']);journal=owned_json(controls['actual_stage_journal']);watch=owned_json(controls['actual_child_watchdog'])
assert receipt['schema']=='AXMAT_V14_HELPER_ONLY_ROOT_ACTUAL_TERMINAL_RECEIPT_V1'and receipt['action']=='fixtures'
assert type(receipt['terminal_result']['exit_code'])is int and receipt['terminal_result']['exit_code']==0 and receipt['session_closed']is True
stream_sizes={}
for stream in ('stdout','stderr'):
    desc=receipt[stream];assert set(desc)=={'path','sha256','size_bytes'}
    assert {key:desc[key]for key in ('path','sha256')}==controls['actual_full_'+stream]
    assert type(desc['size_bytes'])is int and desc['size_bytes']==Path(desc['path']).stat().st_size
    assert files[desc['path']]==desc['sha256'];stream_sizes[stream]=desc['size_bytes']
assert result['schema']=='AXMAT_V14_HELPER_ONLY_FIXTURE_RESULT_V1'and result['status']=='PASS_HELPER_PROTOCOL_ONLY'and result['action']=='fixtures'
assert {key:result['source'][key]for key in ('path','sha256')}==helper_pin
assert len(result['groups'])==21 and all(group['status']=='PASS_HELPER_PROTOCOL_ONLY'for group in result['groups'])
assert result['numeric_component_stage_count_increment']==0 and result['numerical_controls_compiler_or_API_invoked']is False
for key in ('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'):assert result[key]is False
for group in result['groups']:assert jsonfile(control_root/group['name']/'case_result.json')==group
for item in host['input_sources']:assert files[item['path']]==item['sha256']
for key in ('original_helper','resource_factory'):assert files[host[key]['path']]==host[key]['sha256']
for key,expected in (('actual_child_result',controls['actual_result']),('actual_watchdog',controls['actual_child_watchdog'])):assert {field:host[key][field]for field in ('path','sha256')}==expected
merged=host['actual_full_merged_stdout_stderr'];assert files[merged['path']]==merged['sha256'];child_stdout=jsonfile(merged['path'])
assert child_stdout['status']=='PASS_HELPER_PROTOCOL_ONLY'and child_stdout['action']=='fixtures'and child_stdout['result_sha256']==controls['actual_result']['sha256']and child_stdout['Root_actual_child_terminal_required_before_admission']is True
stdout=jsonfile(controls['actual_full_stdout']['path'])
assert stdout['status']=='PASS_HELPER_ONLY_ACTUAL_BOUNDED_HOST'and stdout['action']=='fixtures'and {key:stdout['host_result'][key]for key in ('path','sha256')}==controls['actual_host_result']and stdout['actual_external_Root_terminal_still_required']is True
stages=journal['stages']
assert host['schema']=='AXMAT_V14_HELPER_ONLY_GENUINE_SUPERVISOR_ACTUAL_HOST_V1'and host['status']=='PASS_HELPER_ONLY_ACTUAL_BOUNDED_HOST'and host['action']=='fixtures'
assert host['stage_records']==stages and host['watchdog']==watch and host['actual_command']==watch['command']
assert 0<=host['whole_elapsed_seconds']<host['whole_wall_cap_seconds']==120 and 0<=host['whole_archive_bytes']<host['archive_cap_bytes']==64*2**20
assert (host['rss_cap_mib'],host['threads'],host['children_at_once'],host['retries'])==(512,1,1,0)
for key in ('supervisor_class_or_MRO_modified','failed_V13_audit_reexecuted','numerical_component_or_transport_executed','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'):assert host[key]is False
assert isinstance(stages,list)and len(stages)==1 and all(stage['status']=='PASS'for stage in stages)
assert type(watch['returncode'])is int and watch['returncode']==0 and type(watch['pid'])is int and watch['pid']>0 and watch['command']==stages[-1]['command']
assert watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and watch['rss_cap_mib']==512
assert 0<=watch['sampled_peak_rss_mib']<512 and 0<watch['wall_cap_seconds']<=stages[-1]['wall_cap_seconds']<=120 and 0<=watch['elapsed_seconds']<watch['wall_cap_seconds']
assert C.read_bytes()==craw
report=dict(status='PASS_READONLY_READY_SOURCE_BINDING_AND_ACTUAL_HELPER_EVIDENCE_COMPATIBILITY_ONLY',candidate=dict(path=str(C),sha256=sha(craw),bytes=len(craw)),binding_proof=dict(path=str(BP),sha256=sha(BP.read_bytes())),binding_exact_constants_only=4,all101_definitions_including_nested_byteexact=True,complete_inverse_chain_ready_b6_e1_d2=chains,status_and_pins=values,actual_helper_controls_admission=dict(path=str(A),sha256=sha(araw),bytes=len(araw)),all_absolute_filepins=145,all_absolute_filepin_bytes_read=all_bytes,all_full_pin_checks_passed=True,whole_control_host_inventory_summaries={key:dict(files=len(v['files']),symlinks=len(v['symlinks']),directories=len(v['directories']))for key,v in inventories.items()},actual_control_host_bytes=archive_bytes,all_raw_manifest_and21_case_json_exact=True,legal_hardlink_literals=hardlinks,Root_terminal_schema_exit0_session_closed=True,Root_full_stream_actual_sizes=stream_sizes,host_status=host['status'],helper_groups=len(result['groups']),additional_alias_subcases=controls['additional_alias_subcases'],actual_host_elapsed_seconds=host['whole_elapsed_seconds'],watch_pid=watch['pid'],watch_elapsed_seconds=watch['elapsed_seconds'],watch_sample_peak_mib_as_recorded=watch['sampled_peak_rss_mib'],sample0_is_not_measured_zero_or_native_RSS_proof=True,helper_source34_original33_byteexact_digest1_and13_added=True,original86_12build_92recipe_math_MRO_budgets_unchanged=True,source_admission_schema_and_raw_receipt_fields_compatible=True,deterministic_gate_contract_incompatibilities=[],material_time_gain_proven=False,full86_component_executed_by_this_review=False,business_imports=False,business_calls=False,source_gate_invocations=False,helper_calls=False,fixture_execution=False,benchmark_execution=False,compile=False,canonical_or_candidate_write=False,old35GB_input_hashing=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
D.mkdir(parents=True,exist_ok=True);(D/'REPORT.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
print(json.dumps(report,indent=2,allow_nan=False))
