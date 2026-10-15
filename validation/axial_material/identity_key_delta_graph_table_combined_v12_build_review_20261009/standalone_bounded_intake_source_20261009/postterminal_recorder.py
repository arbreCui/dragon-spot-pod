"""Root postterminal recorder; no producer/API, child, or cold controller is run.
Actual tool facts are supplied only after the observed host terminal return.
Original pinned recorder pure file/JSON/inventory helpers are reused unchanged.
"""
import argparse,importlib.util,hashlib,shutil,sys
from pathlib import Path
DRAFT_STATUS='READY_REVIEWED_ROOT_POSTTERMINAL_INTAKE_RECORD_ONLY'
if DRAFT_STATUS!="READY_REVIEWED_ROOT_POSTTERMINAL_INTAKE_RECORD_ONLY":raise ValueError("UNREADY: source only; no observed new host return")
HELPER=Path('/private/tmp/axmat_root_historical_owned_specs_combined_runtime_actual_bound_recorder_20261007.py')
HELPER_SHA='0b8a9a0a3b71bdea15269a14e54011d142e00c92979fbedef8ade3bcac7ec047'
if hashlib.sha256(HELPER.read_bytes()).hexdigest()!=HELPER_SHA:raise ValueError('reviewed pure recorder helper changed')
s=importlib.util.spec_from_file_location('actual_root_pure_recorder_helpers',HELPER)
r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
BASE=Path('/private/tmp/axmat-owned-specs-identity-key-delta-graph-table-v12-standalone-bounded-runtime-api-intake-20261009')
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-owned-specs-identity-key-delta-graph-table-v12-standalone-bounded-runtime-api-intake-evidence-20261009')
HOST=Path('/Users/wen/spot/validation/axial_material/identity_key_delta_graph_table_combined_v12_build_review_20261009/standalone_bounded_intake_source_20261009/host.py')
HOST_SHA='5af2c2abed88ec4dd416607be45ba433f3ff1732a97a04aa884e097b8d457cd9'
COMPONENT_TERM=Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-combined-terminal-v12-20261009')
DECL_SHA='410720642a1952480ad9190ed48292e96cf9f17d8ab02967b5503713caa09f5d'
SEAL_SHA='1f0ddf9751140abc2eb114918695b33007725cd34839e278b2e4b04f9c779dfa'
RUN_SHA='396697c31e8112040b7fab32f452e5fabd8592ec41379d3daf2eda1519df7b28'
PREP_SHA='f431490002fb5e2d4de0cee17979c5ef5b5725740f16fea85fdcfd3fd502ddb5'
API_RETURN_SHA='65fc18ba1fab484b91c626a48d79a55a9bd5f21b65a391d18b9c4313e2333536'
CMD=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','/Users/wen/spot/validation/axial_material/prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.py','admit','--sha256',SEAL_SHA,'--terminal-evidence',str(COMPONENT_TERM/'terminal_return.json'),'--terminal-evidence-sha256',RUN_SHA]
for value in (DECL_SHA,SEAL_SHA,RUN_SHA,PREP_SHA,API_RETURN_SHA):
 if type(value)is not str or len(value)!=64 or any(c not in '0123456789abcdef'for c in value)or value=='0'*64:raise ValueError('UNREADY: exact actual component and host stream pins required')
FALSE=('cold_controller_imported','cold_controller_bound','cold_prepared','physics_or_native_transport_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted')
p=argparse.ArgumentParser();p.add_argument('--actual-exit-code',type=int,required=True);p.add_argument('--initial-chunk',required=True);p.add_argument('--session-id',type=int,required=True);p.add_argument('--terminal-chunk',required=True);p.add_argument('--observed-after-tool-return',action='store_true',required=True)
a=p.parse_args();facts=r.actual_tool_facts(a.actual_exit_code,a.initial_chunk,a.session_id,a.terminal_chunk,a.observed_after_tool_return,a.observed_after_tool_return)
if a.actual_exit_code!=0:raise ValueError('only observed successful intake host accepted')
if r.sha(HOST)!=HOST_SHA:raise ValueError('reviewed host changed')
x=r.strict(BASE/'result.json');w=r.strict(BASE/'intake/admit.watchdog.json');st_doc=r.strict(BASE/'STANDALONE_BOUNDED_RUNTIME_API_INTAKE/stages.json')
if type(st_doc)is not dict or set(st_doc)!={'stages'} or type(st_doc['stages'])is not list:raise ValueError('exact original complete stage wrapper required')
st=st_doc['stages']
body=r.strict(BASE/'intake/admit.log')
if (x['schema']!='AXMAT_OWNED_SPECS_STANDALONE_BOUNDED_RUNTIME_API_INTAKE_ACTUAL_HOST_V1' or x['actual_command']!=CMD or x['watchdog']!=w or x['stage_records']!=st or len(st)!=1 or st[0]['status']!='PASS' or st[0]['command']!=CMD or w['command']!=CMD or type(w['returncode'])is not int or w['returncode']!=0 or w['limit_failure']is not None or not 0<w['sampled_peak_rss_mib']<512 or w['own_child_only']is not True or w['liveness_group_cleanup']is not True or x['whole_elapsed_seconds']>=1800 or (x['total_wall_cap_seconds'],x['stage_wall_cap_seconds'],x['RSS_cap_mib'],x['threads'],x['children_at_once'],x['retries'])!=(1800,600,512,1,1,0) or any(x[k]is not False for k in FALSE) or x['child_stderr_combined_into_actual_log']is not True or x['separate_child_stderr_observation_claimed']is not False):raise ValueError('complete actual guarded intake contract differs')
if (body['schema']!='AXMAT_OWNED_SPECS_IDENTITY_KEY_DELTA_GRAPH_TABLE_COMBINED_RUNTIME_V12_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1' or body['admission']!='COMBINED_RUNTIME_INPUT_ONLY' or body['original_component_APIs_executed_now']is not False or body['production_pipeline_prepared']is not False or any(body[k]is not False for k in ('native_transport_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted'))):raise ValueError('whole actual INPUT-only API required')
for key in ('producer','declaration','build_seal','actual_run','actual_PREP','actual_API_whole_merged_stream','actual_API_whole_return','supervisor_source','parent_source','bounded_helper'):
 if r.pin(x[key]['path'])!=x[key]:raise ValueError('actual source/result binding changed: '+key)
if r.sha(BASE/'intake/admit.log')!=API_RETURN_SHA or st[0]['log_sha256']!=r.sha(BASE/'intake/admit.log'):raise ValueError('whole merged actual API bytes changed')
stdout=Path('/private/tmp/axmat-owned-specs-identity-key-delta-graph-table-v12-standalone-bounded-runtime-api-intake-host-20261009.stdout');stderr=stdout.with_suffix('.stderr')
if r.strict(stdout)!=x or stderr.stat().st_size!=0:raise ValueError('actual complete host stream differs')
if OUT.exists() or OUT.is_symlink():raise ValueError('exclusive new evidence family required')
r.normal(OUT,missing=True);OUT.mkdir()
payload={'host.py':HOST,'postterminal_recorder.py':Path(__file__).resolve(),'host.stdout':stdout,'host.stderr':stderr,'result.json':BASE/'result.json','runtime/run_bounded_dragon.py':BASE/'runtime/run_bounded_dragon.py','intake/admit.log':BASE/'intake/admit.log','intake/admit.watchdog.json':BASE/'intake/admit.watchdog.json','STANDALONE_BOUNDED_RUNTIME_API_INTAKE/stages.json':BASE/'STANDALONE_BOUNDED_RUNTIME_API_INTAKE/stages.json'}
original={}
for name,src in payload.items():
 pin=r.pin(src);dst=OUT/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 if r.sha(dst)!=pin['sha256']:raise ValueError('copy differs')
 original[name]=pin
inv,size=r.inventory(OUT)
receipt=dict(schema='AXMAT_OWNED_SPECS_STANDALONE_BOUNDED_RUNTIME_API_INTAKE_ROOT_ACTUAL_RETURN_V1',actual_tool=facts,actual_exit_code=a.actual_exit_code,record_written_after_actual_tool_return=True,actual_host_command=[CMD[0],str(HOST)],actual_API_command=CMD,host_source=r.pin(OUT/'host.py'),host_stdout=r.pin(OUT/'host.stdout'),host_stderr=r.pin(OUT/'host.stderr'),actual_host_result=r.pin(OUT/'result.json'),whole_API_return=r.pin(OUT/'intake/admit.log'),actual_watchdog=r.pin(OUT/'intake/admit.watchdog.json'),actual_stage_records=r.pin(OUT/'STANDALONE_BOUNDED_RUNTIME_API_INTAKE/stages.json'),source_payload_pins=original,payload_inventory=inv,payload_bytes=size,actual_bounded_runtime_input_admission_observed=True,child_stderr_combined_into_actual_log=True,separate_child_stderr_observation_claimed=False,whole_elapsed_seconds=x['whole_elapsed_seconds'],sampled_API_child_peak_RSS_mib=w['sampled_peak_rss_mib'],total_wall_cap_seconds=1800,stage_wall_cap_seconds=600,RSS_cap_mib=512,threads=1,children_at_once=1,retries=0,**{k:False for k in FALSE})
r.write(OUT/'Root_terminal_return.json',receipt)
print(r.pin(OUT/'Root_terminal_return.json'),size,flush=True)
