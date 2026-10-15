"""Only derive SOURCE text/AST templates; never import a helper or guard."""
import ast
import hashlib
import json
from pathlib import Path
OUT=Path(__file__).parent
PREVIOUS=Path('/private/tmp/axmat_next_helper_UNREADY_qualification_templates_20261010_angular_FPmRlZ')
BASE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
raw=(PREVIOUS/'pure_helper_controls_host.original.txt').read_bytes()
if hashlib.sha256(raw).hexdigest()!='de72db68baa9b91fee8aad1965605ab25c9cb11ed2ea3013c3a1f04d52a41fb2':raise ValueError('exact genuine original host SOURCE required')
(OUT/'pure_helper_controls_host.original.txt').write_bytes(raw)
old=raw.decode();host=old;hunks=[]
def replace(before,after):
 global host
 if host.count(before)!=1:raise ValueError('unique original host SOURCE anchor required: '+before[:80])
 host=host.replace(before,after,1);hunks.append(dict(before=before,after=after))
replace('import time\n','import time\nimport gzip\nimport hashlib\nimport math\nimport stat\n')
replace('"""One pure complete metadata helper control, unchanged genuine guard."""','"""UNREADY complete current graph fresh verifier, unchanged genuine guard."""')
replace("HOST=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-trace-table-helper-controls-host-v17-20261010')","HOST=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-fresh-verifier-host-v21-20261010')")
replace("OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-trace-table-helper-controls-v17-20261010')","OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-fresh-verifier-v21-20261010')")
replace("SOURCE_ARCHIVE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_graph_helper_controls_v17_sources')","SOURCE_ARCHIVE=BASE/'actual_complete_graph_fresh_verifier_v21_sources'\nRECEIPTS=BASE/'actual_complete_graph_fresh_verifier_v21_receipts'")
replace("TARGET=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_graph_helper_controls_v17_sources/pure_helper_controls.py')","TARGET=SOURCE_ARCHIVE/'fresh_verifier_controls.py'")
replace("TARGET_SHA='da4bd8438cb5007e8e7a5817ba9e198237aa93766af769898d971adf9708e68e'","TARGET_SHA=None\nSOURCE_STATUS='UNREADY_SOURCE_ONLY_NO_ACTUAL_SUCCESS'\nBOUND_HELPER_PIN=None\nINSTALL_WITNESS_PIN=None\nSOURCE_INSTALL_RECORD_PIN=None\nUNKNOWN_Q=None\nUNKNOWN_BUSINESS_PINS=None\nGRAPH_PATH=Path('/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v20-20261010/input_graph.json')\nGRAPH_SHA='dfaaaff743d8edf4c94b262c5ee8104f606eddecaf39260010167f0884c6d976'\nGRAPH_IDENTITY=[16777229,49377441,33188,1,45530035,1791587709451819342,1791587709451819342]")
replace('WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=60,60,512,64*2**20','WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,64*2**20')
review=json.loads((PREVIOUS/'SOURCE_REVIEW.json').read_text())
fields=review['complete_public_return_fields_order']
trace=['schema','coverage','records','subprocess_records','unique_records','actual_read_open_attempts','record_storage','success_of_open_attempt_is_not_observed','native_libc_HDF5_loader_and_directory_stat_are_not_traced']
extra=(OUT/'host_extra_definitions.txt').read_text()
replace('\ndef main():',"\nRETURN_FIELDS="+repr(fields)+"\nTRACE_FIELDS="+repr(trace)+"\n\n"+extra+'\ndef main():')
replace('    started=time.monotonic()\n','    started=time.monotonic()\n    if SOURCE_STATUS!=\'READY_SOURCE_BOUND_BY_ROOT\' or any(type(p) is not dict for p in (BOUND_HELPER_PIN,INSTALL_WITNESS_PIN,SOURCE_INSTALL_RECORD_PIN)) or type(TARGET_SHA) is not str or len(TARGET_SHA)!=64:\n        raise ValueError(\'UNREADY host requires actual Root SOURCE bindings before I/O or guard import\')\n')
replace("    inputs=[support.pin(TARGET,TARGET_SHA)","    source_before=_source_namespace(support)\n    if support.pin(BOUND_HELPER_PIN['path'],BOUND_HELPER_PIN['sha256'])!=BOUND_HELPER_PIN or support.pin(INSTALL_WITNESS_PIN['path'],INSTALL_WITNESS_PIN['sha256'])!=INSTALL_WITNESS_PIN or support.pin(SOURCE_INSTALL_RECORD_PIN['path'],SOURCE_INSTALL_RECORD_PIN['sha256'])!=SOURCE_INSTALL_RECORD_PIN:\n        raise ValueError('actual installed helper and closed exact-integer SOURCE witness pins changed')\n    inputs=[support.pin(TARGET,TARGET_SHA)")
before=host[host.index('    inputs='):host.index('\n    helper,hpin=')]
after="    inputs=[support.pin(TARGET,TARGET_SHA),support.pin(BOUND_HELPER_PIN['path'],BOUND_HELPER_PIN['sha256']),support.pin(Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py'),'bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6'),support.pin(GRAPH_PATH,GRAPH_SHA),support_pin,support.pin(support.TARGET,support.TARGET_SHA),support.pin(support.OUT/'seal.json',SEAL_SHA),support.pin(support.TERMINAL/'terminal_return.json',TERM_SHA),INSTALL_WITNESS_PIN,SOURCE_INSTALL_RECORD_PIN]+source_before['files']"
replace(before,after)
replace("roots=resource.history_roots([str(HOST),str(OUT),str(support.SOURCE),str(support.OUT),str(support.TERMINAL)]", "declared_history_roots=(HOST,OUT,support.SOURCE,support.OUT,support.TERMINAL)\n    if len(declared_history_roots)!=5 or any(path==support.ART or not path.is_relative_to(support.ART) for path in declared_history_roots):\n        raise ValueError('all five declared history roots must remain strict ART descendants')\n    roots=resource.history_roots([str(path) for path in declared_history_roots]")
replace("for name in ('runtime','run','GRAPH_PROTOCOL_CONTROLS')", "for name in ('runtime','run','COMPLETE_FRESH_VERIFIER')")
replace("runner=full.OwnRSSSerialExecutor(HOST,remaining,'GRAPH_PROTOCOL_CONTROLS',resources)", "runner=full.OwnRSSSerialExecutor(HOST,remaining,'COMPLETE_FRESH_VERIFIER',resources)")
if host.count("'GRAPH_PROTOCOL_CONTROLS'"):raise ValueError('stage literal not fully retargeted')
replace("command=[str(support.PYTHON),'-B',str(TARGET),'--output-dir',str(OUT)]","command=[str(support.PYTHON),'-B',str(TARGET),'--output-dir',str(OUT),'--driver-sha256',TARGET_SHA]")
start=host.index('        admission=json.loads(log.read_text());watch=json.loads(watch_path.read_text())')
end=host.index("        if len(runner.records)!=1",start)
replace(host[start:end],"        admission=_json_object(log);watch=_json_object(watch_path)\n        control_report=_json_object(OUT/'ACTUAL_REPORT.json')\n        actual_full_controls=_full_controls(support,control_report,admission,watch,command)\n        report_pin=actual_full_controls['actual_report']\n")
replace("        after=resources.check();elapsed=time.monotonic()-started;archived=support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE))", "        if type(watch['pid']) is not int or watch['pid']<=0 or watch['rss_cap_mib']!=RSS_CAP or not _finite_number(watch['sampled_peak_rss_mib'],0,RSS_CAP) or not _finite_number(watch['elapsed_seconds'],0,STAGE_CAP) or not _finite_number(watch['wall_cap_seconds'],0,STAGE_CAP+1) or not 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=runner.records[0]['wall_cap_seconds']<=STAGE_CAP:\n            raise ValueError('actual genuine600-second watched child contract differs')\n        source_after=_source_namespace(support)\n        if source_after!=source_before:raise ValueError('complete SOURCE directories/files/SHA7identity changed')\n        after=resources.check();elapsed=time.monotonic()-started;archived=support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE,RECEIPTS))")
replace("schema='AXMAT_V17_GENUINE_PURE_GRAPH_PROTOCOL_CONTROLS_HOST_V1',status='ACTUAL_PURE_GRAPH_PROTOCOL_CONTROLS_EXTERNAL_ROOT_REQUIRED'", "schema='AXMAT_V21_GENUINE_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_HOST_V1',status='ACTUAL_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_EXTERNAL_ROOT_REQUIRED',actual_full_controls=actual_full_controls,source_namespace_before=source_before,source_namespace_after=source_after,installed_helper=BOUND_HELPER_PIN,actual_closed_SOURCE_install_witness=INSTALL_WITNESS_PIN,source_install_record=SOURCE_INSTALL_RECORD_PIN,actual_host_PID=os.getpid(),helper_metadata_qualified=False,whole_business_INPUT_qualified=False,physical_balance_qualified=False,UNKNOWN_Q=None,UNKNOWN_BUSINESS_PINS=None")
replace("actual_control_report=report_pin,actual_admission_stdout=support.pin(log)", "actual_control_report=report_pin,actual_merged_child_stdout_stderr=support.pin(log),independent_child_stdout_captured=False,independent_child_stderr_captured=False")
replace("actual_host_result=support.pin(HOST/'result.json'),actual_admission_stdout=support.pin(log)", "actual_host_result=support.pin(HOST/'result.json'),actual_merged_child_stdout_stderr=support.pin(log),independent_child_stdout_captured=False,independent_child_stderr_captured=False")
replace("if support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE))>=ARCHIVE_CAP", "if support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE,RECEIPTS))>=ARCHIVE_CAP")
replace("status='FAILED_PURE_GRAPH_PROTOCOL_CONTROLS_NO_RETRY'", "status='FAILED_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_NO_RETRY'")
restored=host
for hunk in reversed(hunks):
 if restored.count(hunk['after'])!=1:raise ValueError('unique full host inverse anchor required')
 restored=restored.replace(hunk['after'],hunk['before'],1)
if restored.encode()!=raw or ast.dump(ast.parse(restored),include_attributes=False)!=ast.dump(ast.parse(raw),include_attributes=False):raise ValueError('full original genuine host SOURCE inverse failed')
ast.parse(host)
(OUT/'fresh_verifier_host.UNREADY.py').write_text(host)
(OUT/'host_template_complete_source_inverse.json').write_text(json.dumps(dict(schema='AXMAT_V21_FRESH_HOST_COMPLETE_ORIGINAL_GENUINE_SOURCE_INVERSE_V1',status='SOURCE_TEMPLATE_ONLY_UNREADY_NO_ACTUAL_HOST',original_path=str(BASE/'actual_complete_graph_helper_controls_v17_sources/pure_helper_controls_host.py'),original_sha256=hashlib.sha256(raw).hexdigest(),original_bytes=len(raw),template_sha256=hashlib.sha256(host.encode()).hexdigest(),template_bytes=len(host.encode()),complete_bytes_inverse=True,complete_AST_inverse=True,ordered_hunks=hunks,genuine619_705_38de_guard_modules_MRO_resources_original_calls_retained=True,original_normal_no_argument_host_cli_retained=True,new_limits=dict(whole=1800,stage=600,rss=512,joint64MiB=True,history96GiB=True,free8GiB=True,threads=1,children=1,retries=0),unknown_actual_pins_None=True,external_actual_Root_freeze_and_terminal_required=True,actual_host_run=False),indent=2)+'\n')
driver=(PREVIOUS/'fresh_verifier_controls.UNREADY.py').read_text()
original_driver=driver
driver_hunks=[dict(before='NEW_HELPER_SOURCE_BYTES = None',after='NEW_HELPER_SOURCE_BYTES = None\nNEW_HELPER_IDENTITY = None\nUNKNOWN_Q = None\nUNKNOWN_BUSINESS_PINS = None'),dict(before="  new,new_before=load_pinned(NEW_HELPER_PATH,NEW_HELPER_SHA256,NEW_HELPER_SOURCE_BYTES,'axmat_fresh_control_actual_new_helper')",after="  new,new_before=load_pinned(NEW_HELPER_PATH,NEW_HELPER_SHA256,NEW_HELPER_SOURCE_BYTES,'axmat_fresh_control_actual_new_helper')\n  require(type(NEW_HELPER_IDENTITY) is list and len(NEW_HELPER_IDENTITY)==7 and all(type(v) is int for v in NEW_HELPER_IDENTITY) and new_before['identity']==NEW_HELPER_IDENTITY,'Root actual installed helper exact seven-integer identity required')")]
for hunk in driver_hunks:
 if driver.count(hunk['before'])!=1:raise ValueError('unique driver SOURCE anchor required')
 driver=driver.replace(hunk['before'],hunk['after'],1)
driver_restored=driver
for hunk in reversed(driver_hunks):
 if driver_restored.count(hunk['after'])!=1:raise ValueError('unique full driver SOURCE inverse required')
 driver_restored=driver_restored.replace(hunk['after'],hunk['before'],1)
if driver_restored!=original_driver or ast.dump(ast.parse(driver_restored),include_attributes=False)!=ast.dump(ast.parse(original_driver),include_attributes=False):raise ValueError('complete original UNREADY driver bytes/AST inverse differs')
ast.parse(driver)
(OUT/'fresh_verifier_controls.original_UNREADY.txt').write_text(original_driver)
(OUT/'fresh_verifier_controls.UNREADY.py').write_text(driver)
(OUT/'driver_template_complete_source_inverse.json').write_text(json.dumps(dict(schema='AXMAT_V21_FRESH_DRIVER_COMPLETE_PREVIOUS_UNREADY_SOURCE_INVERSE_V1',status='SOURCE_TEMPLATE_ONLY_UNREADY_NO_ACTUAL_DRIVER',original_sha256=hashlib.sha256(original_driver.encode()).hexdigest(),template_sha256=hashlib.sha256(driver.encode()).hexdigest(),complete_bytes_inverse=True,complete_AST_inverse=True,ordered_hunks=driver_hunks,actual_helper_bindings_None=True,UNKNOWN_Q=None,UNKNOWN_BUSINESS_PINS=None,actual_driver_run=False),indent=2)+'\n')
print(json.dumps(dict(status='DERIVED_SOURCE_TEMPLATES_UNREADY',host_inverse_hunks=len(hunks),host_complete_bytes_AST_inverse=True,host_sha256=hashlib.sha256(host.encode()).hexdigest(),driver_sha256=hashlib.sha256(driver.encode()).hexdigest(),helper_API_guard_business_executed=False)))
