from pathlib import Path
import ast,hashlib,json,os,stat
D=Path(__file__).parent
def identity(path):
    x=Path(path).lstat();return [x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def record(path):
    before=identity(path);assert stat.S_ISREG(before[2])
    value=sha(path);assert before==identity(path)
    return dict(path=str(path),sha256=value,size_bytes=before[4],identity=before)
def read(path):return json.loads(Path(path).read_text())
host=D/'metadata_timing_host.UNREADY.py';driver=D/'metadata_timing_driver.UNREADY.py'
report=read(D/'REPORT.json');proof=read(D/'HOST_COMPLETE_SOURCE_INVERSE.json')
assert sha(host)=='bcf0be9eccc649087fe4f6b6d0e4d94907b1b06e4006500615931b7027f5fee3'
assert sha(driver)=='8ea23702654f46446a39faed9118232ed8a374e75878355291661f75e918866d'
for path in (host,driver):
    tree=ast.parse(path.read_text());compile(tree,str(path),'exec')
    assignments={}
    for node in tree.body:
        if isinstance(node,ast.Assign):
            for target in node.targets:
                if isinstance(target,ast.Name):assignments[target.id]=node.value
    for name in ('TARGET_FACTORY','TARGET_FACTORY_SHA256'):
        assert ast.literal_eval(assignments[name]) is None
    if path==host:
        for name in ('DRIVER','DRIVER_SHA256'):assert ast.literal_eval(assignments[name]) is None
    assert ast.literal_eval(assignments['STATUS']).startswith('UNREADY')
    # A guarded future main may import approved real modules or invoke four
    # approved metadata functions. None is executed by this AST-only reader.
    assert isinstance(tree.body[-1],ast.If)
    assert ast.unparse(tree.body[-1].test)=="__name__ == '__main__'"
    assert len(tree.body[-1].body)==1
    assert ast.unparse(tree.body[-1].body[0])=='main()'
    for node in tree.body[:-1]:
        assert isinstance(node,(ast.Expr,ast.Import,ast.ImportFrom,ast.Assign,ast.FunctionDef,ast.ClassDef))
source=host.read_text()
for edit in reversed(proof['edits']):
    assert source.count(edit['new'])==edit['count'];source=source.replace(edit['new'],edit['old'])
assert source==Path(proof['parent_host']['path']).read_text()
assert report['source_inputs_not_reduced_to_three'] and report['all_four_metadata_functions_static_readonly']
pins=[record(Path(proof['parent_host']['path'])),record(host),record(driver),record(Path(report['frozen_target_candidate']['path'])),
      record(Path(report['canonical_target_required']))]
assert pins[-1]['sha256']==pins[-2]['sha256']=='4fbd1b054c6516b410181144f088d540a64a8ab793d480fb2c89de0d1252199c'
input_sources=[
('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_source_factor_production.py','619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'),
('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_rank1_factor_cache_cross_group_identity_key_delta_production.py','f136baab5047a8727cfd2c0abb5399acf617c25c4f4e7692242419e6f9daef4e'),
('/Users/wen/spot/validation/axial_material/qualify_refined_AAA_layered_full.py','70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'),
('/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py','38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128'),
('/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/run_bounded_dragon.py','bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09'),
('/Users/wen/spot/validation/axial_material/complete_environment_streaming_sha_helper_v14b.py','7d740b177f5e1c728f0729df031248fbb396f6978b9a3d5c8776a0c270db48d3'),
('/Users/wen/spot/validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010/source_patch_proof.json','1809278680379d2ef6ee5c76218d4614abbbc1c9cbcf379674e7540485db86f2'),
('/Users/wen/spot/validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010/Root_actual_helper_controls_admission.json','16d4548b1cc4ffe935bd8d28219e99a6e9da9af949e7577a82eb758e99d7f568')]
for path,want in input_sources:
    row=record(Path(path));assert row['sha256']==want;pins.append(row)
for row in pins:assert identity(row['path'])==row['identity']
contract={'schema':'AXMAT_V14B_BOUNDED_READONLY_METADATA_DIAGNOSTIC_SOURCE_CONTRACT_V1','status':'UNREADY',
    'prospective_canonical_target':report['canonical_target_required'],'target_path_and_SHA_bound_in_draft':None,
    'Root_install_driver_location':'/Users/wen/spot/validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010/actual_metadata_sources/metadata_timing_driver.py',
    'driver_path_and_SHA_bound_in_host':None,'four_calls_each_once':report['profile_exactly_four_direct_calls_each_once'],
    'nested_admission_calls_will_be_observed_not_memoized':True,'no_function_global_monkeypatch_or_class_overlay':True,
    'target_code_whitelist_and_forbidden_canonical_function_call_guard':True,
    'profile_records_full_definition_pins_call_return_counts_edges_inclusive_exclusive_ns':True,
    'profile_not_unbiased_timer':'Passive profiling overhead remains; exclusive excludes selected canonical Python children only.',
    'complete_output_files':['sender_source_admission.return.json','sender_control_contract.return.json','stream_environment_helper_source_admission.return.json','source_inputs.return.json','result.json','raw_preservation_manifest.json'],
    'actual_expected_output_bytes':None,'all_return_fields_kept':True,
    'future_whole_elapsed_or_RSS':None,'future_actual_Root_return':None,'future_actual_profile_values':None,
    'caps':report['caps'],'old86_numerical_count_increment':0,'genuine_supervisor_chain':['619','705','38de','bc4','f136'],
    'genuine_host_checks_original_guard_and_direct_MRO':True,'archive_tail_checked_at_host_epoch':True,
    'new_roots':[report['new_host_root'],report['new_driver_root']],
    'component_native_AAA_ABA_credit':False,'source_metadata_called_now':False,'project_written':False}
(D/'SOURCE_CONTRACT.json').write_text(json.dumps(contract,indent=2)+'\n')
evidence={'schema':'AXMAT_V14B_METADATA_SOURCE_AST_AND_FULL_BYTE_EVIDENCE_V1','status':'SOURCE_ONLY_UNREADY_NOT_EXECUTED',
    'fresh_full_source_pins_and_7identity':pins,'source_only_AST_compile_not_execution':True,
    'only_four_pure_read_paths_allowed':True,'all_source_inputs_call_paths_metadata_only':True,
    'host_original_support_functions_exact_count':report['host_original_support_defs_preserved'],
    'normal_canonical_import_future':True,'MRO_and_math_not_modified':True,
    'no_helper_metadata_business_API_fixture_benchmark_called':True,'Root_polled':False,'project_written':False,
    'readonly_source_checker_failure_preserved':{'initial_chunk_id':'d2680c','exit_code':1,'closed':True,
        'cause':'Pure AST checker incorrectly treated original_wrapper.replace string operation as filesystem replace; tightened string variable whitelist only.',
        'business_driver_or_host_executed':False}}
(D/'SOURCE_EVIDENCE.json').write_text(json.dumps(evidence,indent=2)+'\n')
receipt={'schema':'AXMAT_V14B_BOUNDED_METADATA_SOURCE_GENERATION_ACTUAL_TOOL_RETURNS_V1','status':'SOURCE_ONLY_UNREADY_NOT_EXECUTED',
    'initial_pure_checker':{'chunk_id':'d2680c','exit_code':1,'exit_code_type':'int','closed':True},
    'preserve_original_source_and_streams':{'chunk_id':'14cf37','exit_code':0,'exit_code_type':'int','closed':True},
    'final_source_generation_and_AST_precheck':{'chunk_id':'8c524a','exit_code':0,'exit_code_type':'int','closed':True},
    'source_generator':record(D/'generate_host_source_and_review.py'),'stdout':record(D/'source_v2.stdout'),
    'stderr':record(D/'source_v2.stderr'),'host':record(host),'driver':record(driver),'REPORT':record(D/'REPORT.json'),
    'metadata_API_or_fixture_or_benchmark_executed':False,'project_written':False,'Root_polled':False}
assert receipt['stderr']['size_bytes']==0
(D/'actual_source_tool_terminal_returns.json').write_text(json.dumps(receipt,indent=2)+'\n')
manifest={'schema':'AXMAT_V14B_BOUNDED_METADATA_SOURCE_COMPLETE_SMALL_MANIFEST_V1','status':'SOURCE_ONLY_UNREADY_NOT_EXECUTED',
    'files':[record(p) for p in sorted(D.iterdir()) if p.is_file() and p.name!='EVIDENCE_MANIFEST.json'],
    'project_source_evidence_bound_not_copied':True,'future_actuals_None':True,'no_execution_or_science_credit':True}
(D/'EVIDENCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({name:sha(D/name) for name in ['metadata_timing_driver.UNREADY.py','metadata_timing_host.UNREADY.py','REPORT.json','HOST_COMPLETE_SOURCE_INVERSE.json','SOURCE_CONTRACT.json','SOURCE_EVIDENCE.json','actual_source_tool_terminal_returns.json','EVIDENCE_MANIFEST.json']},indent=2))
