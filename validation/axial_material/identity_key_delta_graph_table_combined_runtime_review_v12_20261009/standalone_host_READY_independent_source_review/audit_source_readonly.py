"""Independent stdlib source/data review; never imports or executes business code."""
import ast
import hashlib
import json
import math
import os
import stat
from pathlib import Path

DEST = Path('/private/tmp/axmat_v12_standalone_host_ready_independent_readonly_review_20261009')
ROOT = Path('/Users/wen/spot')
REVIEW = ROOT/'validation/axial_material/identity_key_delta_graph_table_combined_runtime_review_v12_20261009'
OUT = ROOT/'validation/artifacts/axial-material-owned-specs-identity-key-delta-graph-table-combined-runtime-v12-20261009'
TERM = ROOT/'validation/artifacts/axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-combined-terminal-v12-20261009'
LIMIT = 64 * 1024 * 1024
observed = {}
checks = {}

def check(name, value):
    if value is not True:
        raise ValueError(name)
    checks[name] = True

def fresh(path, expected=None, collect=False):
    path = Path(path)
    check('ordinary_absolute_path:'+str(path), path.is_absolute() and '..' not in path.parts)
    for ancestor in [*reversed(path.parents), path]:
        mode = ancestor.lstat().st_mode
        check('no_alias:'+str(ancestor), not stat.S_ISLNK(mode))
        if ancestor != path:
            check('directory_ancestor:'+str(ancestor), stat.S_ISDIR(mode))
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        first = os.fstat(fd)
        check('regular_file:'+str(path), stat.S_ISREG(first.st_mode))
        check('bounded_reader:'+str(path), not collect or first.st_size <= LIMIT)
        digest = hashlib.sha256()
        payload = []
        count = 0
        while raw := os.read(fd, 1024*1024):
            digest.update(raw)
            count += len(raw)
            if collect:
                check('bounded_actual_reader:'+str(path), count <= LIMIT)
                payload.append(raw)
        last = os.fstat(fd)
        fields = ('st_dev','st_ino','st_mode','st_size','st_mtime_ns','st_ctime_ns','st_nlink')
        check('stable_fresh_file:'+str(path), tuple(getattr(first,k) for k in fields) == tuple(getattr(last,k) for k in fields) and count == first.st_size)
        sha = digest.hexdigest()
        if expected is not None:
            check('exact_fresh_sha:'+str(path), sha == expected)
        observed[str(path)] = dict(path=str(path),sha256=sha,size_bytes=count)
        return b''.join(payload) if collect else sha
    finally:
        os.close(fd)

def strict(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate JSON key')
            result[key] = value
        return result
    def reject(value):
        raise ValueError('nonfinite JSON constant '+value)
    body = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs, parse_constant=reject)
    def finite(value):
        if isinstance(value,float) and not math.isfinite(value):
            raise ValueError('nonfinite JSON number')
        if isinstance(value,dict):
            for child in value.values(): finite(child)
        elif isinstance(value,list):
            for child in value: finite(child)
    finite(body)
    return body

def data(path, sha=None):
    return strict(fresh(path,sha,True))

def source(path, sha=None):
    return fresh(path,sha,True).decode('utf-8')

candidate_path = REVIEW/'standalone_intake_host.READY_REVIEW_CANDIDATE.py'
candidate_sha = '5af2c2abed88ec4dd416607be45ba433f3ff1732a97a04aa884e097b8d457cd9'
candidate = source(candidate_path,candidate_sha)
tree = ast.parse(candidate,filename=str(candidate_path))
proof = data(REVIEW/'Root_standalone_intake_host_READY_23_region_complete_inverse_proof.json','67c37c8dffe351d9d169ea8bd11a322b395a41df462915607a9f5562c897226a')
mother = source(proof['mother_UNREADY']['path'],proof['mother_UNREADY']['sha256'])
genuine = source(proof['mother_genuine_V10']['path'],'a5d00497e2419ddaf9d9de99da9a6e48659f8a7521c4476842e49741b847871a')
region = proof['Root_only_one_status_region']
check('one_ready_region_old_occurrence',mother.count(region['old'])==1)
check('one_ready_region_new_occurrence',candidate.count(region['new'])==1)
check('ready_candidate_exactly_one_status_line_change',mother.replace(region['old'],region['new'],1)==candidate)
regions = proof['complete_regions']
check('exact_23_region_count',len(regions)==23 and proof['complete_region_count']==23)
check('all_region_names_unique',len({x['region']for x in regions})==23)
inverse = candidate
inverse_observations = []
for row in reversed(regions):
    count = inverse.count(row['new'])
    check('single_inverse_region:'+row['region'],count==1)
    inverse = inverse.replace(row['new'],row['old'],1)
    inverse_observations.append(dict(region=row['region'],new_occurrences=count))
check('full_23_region_inverse_byte_exact_to_genuine_V10',inverse==genuine)
check('candidate_has_no_new_functions_classes',not any(isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))for x in tree.body))

assigned = {}
for node in tree.body:
    if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
        try: assigned[node.targets[0].id]=ast.literal_eval(node.value)
        except (ValueError,TypeError): pass
pins = dict(DECL_SHA='410720642a1952480ad9190ed48292e96cf9f17d8ab02967b5503713caa09f5d',SEAL_SHA='1f0ddf9751140abc2eb114918695b33007725cd34839e278b2e4b04f9c779dfa',RUN_SHA='396697c31e8112040b7fab32f452e5fabd8592ec41379d3daf2eda1519df7b28',PREP_SHA='f431490002fb5e2d4de0cee17979c5ef5b5725740f16fea85fdcfd3fd502ddb5')
for name,value in pins.items(): check('actual_combined_binding:'+name,assigned[name]==value)
declaration = data(OUT/'declaration.json',pins['DECL_SHA'])
seal = data(OUT/'seal.json',pins['SEAL_SHA'])
run = data(TERM/'terminal_return.json',pins['RUN_SHA'])
prep = data(TERM/'declaration_terminal_return.json',pins['PREP_SHA'])
check('ready_status_literal',assigned['DRAFT_STATUS']=='READY_REVIEWED_GRAPH_TABLE_V12_STANDALONE_INPUT_ONLY')
check('exact_Python312_literal',assigned['PYTHON']=='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')
factory_path = ROOT/'validation/axial_material/prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.py'
factory = source(factory_path,'5af1feebc7d40549750e1daec6148ae073a4c85c1eb3242485e6d9e80826861b')
genuine_factory_path = ROOT/'validation/axial_material/prepare_historical_input_owned_specs_factor_diagonal_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v10.py'
genuine_factory = source(genuine_factory_path,'c55ca2680d9e1326979649f835d9612a8fd80df5aecee1adc25765c419329efc')
factory_tree = ast.parse(factory)
genuine_factory_tree = ast.parse(genuine_factory)
function_names = ('production_admission','complete_input_phase','actual_components','input_modules','current_input_predicates','graph_input_bindings','modules')
function_proof = {}
for name in function_names:
    n1 = next(x for x in factory_tree.body if isinstance(x,ast.FunctionDef) and x.name==name)
    n0 = next(x for x in genuine_factory_tree.body if isinstance(x,ast.FunctionDef) and x.name==name)
    b1 = ast.get_source_segment(factory,n1)
    b0 = ast.get_source_segment(genuine_factory,n0)
    check('genuine_whole_input_function_exact:'+name,b1==b0)
    function_proof[name] = dict(byte_exact_to_V10=True,sha256=hashlib.sha256(b1.encode()).hexdigest())

root_receipt = data(REVIEW/'Root_actual_formal_admit_tool_terminal_return.json','86f4ea404d0304b22c819278723a8797b5a0cf53fce251cbae3d778a2f596459')
job = data(REVIEW/'Root_current_actual_formal_admit_job.json')
check('formal_admit_genuine_typed_zero',type(root_receipt['returncode'])is int and root_receipt['returncode']==0 and type(root_receipt['actual_tool_result']['exit_code'])is int and root_receipt['actual_tool_result']['exit_code']==0)
check('formal_admit_actual_observed_after_return',root_receipt['actual_tool_terminal_return_observed']is True and root_receipt['record_written_after_actual_terminal_return']is True)
check('formal_admit_closed_actual_session',root_receipt['actual_initial_tool_result']['session_id']==root_receipt['actual_closed_session_id']==34504 and job['actual_live_session_id']is None and job['actual_terminal_return']==root_receipt['actual_tool_result'])
check('formal_admit_exact_source_and_pins',root_receipt['source']==dict(path=str(factory_path),sha256=assigned['FACTORY_SHA']) and root_receipt['build_seal_sha256']==pins['SEAL_SHA'] and root_receipt['terminal_evidence_sha256']==pins['RUN_SHA'])
api = data(REVIEW/'admit.stdout.json','65fc18ba1fab484b91c626a48d79a55a9bd5f21b65a391d18b9c4313e2333536')
check('formal_admit_stderr_entire_empty',fresh(REVIEW/'admit.stderr.txt','e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',True)==b'')
check('whole_actual_input_return_schema',api['schema']=='AXMAT_OWNED_SPECS_IDENTITY_KEY_DELTA_GRAPH_TABLE_COMBINED_RUNTIME_V12_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1' and api['admission']=='COMBINED_RUNTIME_INPUT_ONLY')
check('whole_API_actual_prep_run_seal_binding',api['actual_external_terminal_evidence']==dict(path=str(TERM/'terminal_return.json'),sha256=pins['RUN_SHA']) and api['actual_prepare_terminal_evidence']==dict(path=str(TERM/'declaration_terminal_return.json'),sha256=pins['PREP_SHA']) and api['build_seal_sha256']==pins['SEAL_SHA'])
input_spec_path = ROOT/'validation/axial_material/combined_runtime_complete_historical_input_specs_20261007.json'
input_spec = data(input_spec_path,'2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa')
expected_body = input_spec['metadata']['historical_actual_components']
check('full_original_seven_key_body_byte_value_retained',len(expected_body)==7 and api['actual_components']==expected_body)
check('historical_body_binding_exhaustive',api['historical_whole_component_body']==dict(path=str(input_spec_path),sha256='2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa',encoding_schema='AXMAT_COMBINED_RUNTIME_LOSSLESS_TYPED_INPUT_METADATA_ENCODING_V1',pointer='/metadata/historical_actual_components',whole_seven_key_body_retained=True,original_component_API_execution_claimed=False,historical_FAILED_RUN_promoted=False))
input_flags = ('original_component_APIs_executed_now','production_pipeline_prepared','native_transport_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted')
check('whole_API_scope_input_only_all_native_science_false',all(api[k]is False for k in input_flags))
check('formal_receipt_does_not_claim_bounded_host_native_AAA_ABA',all(root_receipt[k]is False for k in ('bounded_whole_INPUT_intake_qualified','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted')))
check('proof_no_host_execution_or_qualification_claim',all(proof[k]is False for k in ('new_host_executed','new_bounded_INPUT_intake_qualified','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted')))

for key in ('genuine_supervisor_source','genuine_parent_class_source','actual_local_supervisor_helper'):
    fresh(declaration[key]['path'],declaration[key]['sha256'])
supervisor = source(declaration['genuine_supervisor_source']['path'],declaration['genuine_supervisor_source']['sha256'])
parent = source(declaration['genuine_parent_class_source']['path'],declaration['genuine_parent_class_source']['sha256'])
supervisor_class = next(x for x in ast.parse(supervisor).body if isinstance(x,ast.ClassDef)and x.name=='OwnRSSSerialExecutor')
check('genuine_supervisor_static_direct_base_SerialExecutor',len(supervisor_class.bases)==1 and isinstance(supervisor_class.bases[0],ast.Name)and supervisor_class.bases[0].id=='SerialExecutor')
parent_class = next(x for x in ast.parse(parent).body if isinstance(x,ast.ClassDef)and x.name=='SerialExecutor')
check('genuine_parent_static_class_present',parent_class.name=='SerialExecutor')
host_required = (
 "if full.OwnRSSSerialExecutor.__bases__!=(c.SerialExecutor,):",
 "f.pin(Path(full.__file__).resolve())!=d['genuine_supervisor_source']or f.pin(Path(c.__file__).resolve())!=d['genuine_parent_class_source']",
 "runner=full.OwnRSSSerialExecutor(BASE,1800-(time.monotonic()-STARTED),FAMILY,resources)",
 "runner.execute(BASE/'intake','admit',command,600)",
 "len(runner.records)!=1", "type(watch['returncode'])is not int", "watch['returncode']!=0",
 "not 0<=watch['sampled_peak_rss_mib']<512", "watch['limit_failure']is not None",
 "watch['own_child_only']is not True", "watch['liveness_group_cleanup']is not True", "not elapsed<1800",
 "threads=1,children_at_once=1,retries=0", "total_wall_cap_seconds=1800,stage_wall_cap_seconds=600,RSS_cap_mib=512",
 "f.absent(BASE)", "resources=f.resources_for(d['resource_roots'],c.ResourceFailure)",
 "if sys.flags.optimize!=0 or os.environ.get('PYTHONOPTIMIZE'):", "sys.dont_write_bytecode=True",
 "if any(os.environ.get(k)!='1'for k in THREAD_KEYS):", "type(runner)is not full.OwnRSSSerialExecutor or runner.resources is not resources",
 "cold_controller_imported=False,cold_controller_bound=False,cold_prepared=False,physics_or_native_transport_executed=False",
 "combined_runtime_native_RSS_proved=False,actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False",
 "child_stderr_combined_into_actual_log=True,separate_child_stderr_observation_claimed=False",
)
for fragment in host_required: check('original_host_guard_retained:'+fragment,fragment in candidate)
check('all_five_thread_environment_keys',assigned['THREAD_KEYS']==('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'))
check('host_has_one_actual_child_execute_call',sum(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and isinstance(n.func.value,ast.Name)and n.func.value.id=='runner'and n.func.attr=='execute'for n in ast.walk(tree))==1)
check('host_has_no_cold_controller_import',not any(isinstance(n,(ast.Import,ast.ImportFrom)) and 'cold' in ast.get_source_segment(candidate,n).lower()for n in ast.walk(tree)))
check('actual_supervisor_live_512_terminate_no_retry','if peak>=512:' in supervisor and 'self.bounded.terminate_group(process)'in supervisor and 'own-child stage failed; no retry'in supervisor)
check('actual_parent_minimum_stage_total_and_single_call','limit = min(float(cap), remaining)'in parent and 'self._process(command, directory, subprocess.DEVNULL, out, process_limit)'in parent)
check('original_resource_caps_retained','TOTAL_WALL, STAGE_WALL, RSS = 1800, 600, 512'in factory and 'RESERVE, HISTORY_CAP, FREE_FLOOR = 2*2**30, 96*2**30, 8*2**30'in factory)
check('declared_history_resources_96GiB_free8GiB',declaration['resource_scope_contract']['artifact_budget_GiB']==96 and declaration['resource_scope_contract']['min_free_GiB']==8 and declaration['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1')
helper_path = ROOT/'validation/axial_material/combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py'
helper = source(helper_path,'e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28')
helper_tree = ast.parse(helper)
max_node = next(x for x in helper_tree.body if isinstance(x,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='MAX_JSON_BYTES'for t in x.targets))
check('reader_original_64MiB_bound_literal',ast.get_source_segment(helper,max_node.value)=='64 * 1024 * 1024')
strict_node = next(x for x in helper_tree.body if isinstance(x,ast.FunctionDef)and x.name=='strict_json')
strict_source = ast.get_source_segment(helper,strict_node)
check('reader_same_actual_size_sha_alias_gates','max_bytes=MAX_JSON_BYTES'in strict_source and '_stream(canonical, collect=True, max_bytes=max_bytes)'in strict_source and 'pin["sha256"] == _sha(expected_sha256)'in strict_source and '_resolve(_path(path), declared, kind="file") == canonical'in strict_source)
check('reader_complete_owned_table_restoration_only_explicit_schema','result.get("schema") == CANONICAL_FILE_TABLE_STORAGE_SCHEMA'in strict_source and 'decode_canonical_file_table_storage(result, _consume=True)'in strict_source)
graph_path = Path(api['historical_input_graph']['path'])
check('actual_graph_physical_bytes_below_unmodified_bound',graph_path.lstat().st_size==66558943 and graph_path.lstat().st_size<LIMIT)

report = dict(schema='AXMAT_V12_FINAL_READY_STANDALONE_HOST_INDEPENDENT_STATIC_REVIEW_V1',status='PASS_SOURCE_ONLY_NOT_EXECUTED',candidate=observed[str(candidate_path)],inverse_region_count=23,full_inverse_exact_to_genuine_V10=True,only_Root_READY_change='DRAFT_STATUS one line',actual_four_combined_pins=pins,whole_INPUT_producer_function_proof=function_proof,formal_admit_genuine_typed_zero=True,formal_admit_full_stdout=observed[str(REVIEW/'admit.stdout.json')],formal_admit_full_stderr=observed[str(REVIEW/'admit.stderr.txt')],full_historical_seven_key_body_retained=True,original_caps=dict(total_wall_seconds=1800,stage_wall_seconds=600,rss_cap_mib=512,threads=1,children_at_once=1,retries=0,source_plus_out_cap_GiB=2,history_cap_GiB=96,filesystem_free_floor_GiB=8,max_graph_reader_bytes=LIMIT),checks=checks,observed_files=observed,inverse_observations=inverse_observations,findings=[],business_code_imported=False,business_code_executed=False,business_PREP_build_admit_repeated=False,pure59_controls_repeated=False,host_executed=False,runtime_MRO_executed_by_this_review=False,original_runtime_MRO_and_source_guards_retained=True,standalone_bounded_INPUT_intake_qualified=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,project_files_written=False,Root_sessions_polled=False,initial_read_only_discovery_tool_errors=[dict(chunk_id='337599',exit_code=1,reason='rg file-discovery pattern matched no file; preceding source reads succeeded; no business action')])
with (DEST/'REPORT.json').open('x') as stream:
    json.dump(report,stream,indent=2,allow_nan=False);stream.write('\n')
report_sha = hashlib.sha256((DEST/'REPORT.json').read_bytes()).hexdigest()
print(json.dumps(dict(status=report['status'],report_path=str(DEST/'REPORT.json'),report_sha256=report_sha,inverse_regions=23,whole_INPUT_functions=len(function_names),formal_full_stdout_bytes=observed[str(REVIEW/'admit.stdout.json')]['size_bytes'],findings=[]),allow_nan=False))
