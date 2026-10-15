"""Read full EOF Source/data pins, validate inverse/AST, freeze before own file.

Never imports the material/helper/control Sources, never JSON-decodes a whole
graph, never executes a child or graph verifier. Three graph files are hashed
as raw immutable historical data only. Original frozen recovery files stay
unchanged; this explicitly new child namespace has its independent closure.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import resource
import stat
import sys
import time

ROOT=Path('/Users/wen/spot');REC=ROOT/'validation/axial_material/q_epoch_recovery_20261011';OWN=Path(__file__).resolve().parent
START=time.monotonic();ATTEMPTS=[]

def safety(event,args):
    if event in ('subprocess.Popen','os.fork','os.forkpty','os.posix_spawn','os.system','os.exec','os.spawn'):
        ATTEMPTS.append(event);raise RuntimeError('Source-only freeze forbids all process creation')
    if event=='open'and isinstance(args[0],(str,bytes)):
        p=Path(os.fsdecode(args[0])).absolute();flags=args[2]
        if isinstance(flags,int)and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)and not p.is_relative_to(OWN):
            raise RuntimeError('only new independent Source closure can be written')

sys.addaudithook(safety)

def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(path):
    p=Path(path)
    for a in (p,*p.parents):assert not a.is_symlink()
    before=p.lstat();assert stat.S_ISREG(before.st_mode)and before.st_nlink==1
    h=hashlib.sha256();n=0
    with p.open('rb')as f:
        assert identity(os.fstat(f.fileno()))==identity(before)
        while True:
            b=f.read(1048576)
            if not b:break
            h.update(b);n+=len(b)
        assert identity(os.fstat(f.fileno()))==identity(before)
    assert identity(p.lstat())==identity(before)and n==before.st_size
    assert time.monotonic()-START<60 and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss<512*2**20
    return dict(path=str(p),size_bytes=n,sha256=h.hexdigest(),identity=identity(before))

def put(name,value):
    with (OWN/name).open('x')as f:json.dump(value,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')

assert sys.dont_write_bytecode and not sys.flags.optimize
proof=json.loads((OWN/'COMPLETE_NEW_EPOCH_SOURCE_DERIVATION.json').read_bytes())
driver=(OWN/'complete_new_epoch_pure_controls.py').read_bytes();back=driver
for c in reversed(proof['driver_full_inverse']['exact_changes']):
    a,b=c['exact_before'].encode(),c['exact_after'].encode();assert back.count(b)==1;back=back.replace(b,a)
assert back==(REC/'candidate_source/pure_helper_controls_NEW_EPOCH_CANDIDATE.py').read_bytes()
host=(OWN/'complete_new_epoch_pure_host.py').read_bytes();back=host
for c in reversed(proof['host_prefreeze_repairs']['exact_repairs']):
    a,b=c['exact_before'].encode(),c['exact_after'].encode();assert back.count(b)==1;back=back.replace(b,a)
for c in reversed(proof['host_full_inverse']['exact_changes']):
    a,b=c['exact_before'].encode(),c['exact_after'].encode();assert back.count(b)==1;back=back.replace(b,a)
assert back==(OWN/'ORIGINAL_COMPLETE_PURE_HOST_BASIS.py').read_bytes()
source_ast=[]
for p in sorted(OWN.glob('*.py')):
    tree=ast.parse(p.read_bytes());source_ast.append(dict(path=str(p),full_ast_parse=True,top_level_functions=[n.name for n in tree.body if isinstance(n,ast.FunctionDef)]))
frozen=json.loads((REC/'COMPLETE_RECOVERY_NAMESPACE_BEFORE_OWN_FREEZE.json').read_bytes())
print('OLD_FREEZE_KEYS',list(frozen),flush=True)
missing=[json.loads(x)for x in (ROOT/'validation/artifacts/axial-material-input-epoch-recovery-v2-20261011/missing_endpoint_candidates.ndjson').read_text().splitlines()]
decl=json.loads((ROOT/'validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v31-installed6a-20261011/declaration.json').read_bytes());canonical=set(decl['files'])
unknown=[dict(path=j['path'],sha256=j['expected_sha256'],historical_pin=j['historical_pin'])for j in missing if j['path']in canonical and not j['matching_current_byte_copies']]
assert len(canonical)==37590 and len(unknown)==53
required=[Path(p)for p in proof['complete_supplement_runtime_input_paths']]
required += [ROOT/'validation/axial_material/combined_runtime_complete_input_graph_read_open_short_index_stable_wire_sort_20261011.py',REC/'preserved_source_basis/ORIGINAL_COMPLETE_INACTIVE_SNAPSHOT_CONTROLS.py',REC/'small_data_actual_v2/ACTUAL_SMALL_DATA_RESULT.json',REC/'ACTUAL_SMALL_DATA_V2_CLOSED0_TOOL_RETURN.json',ROOT/'validation/artifacts/axial-material-owned-specs-identity-key-delta-graph-table-combined-runtime-v12-20261009/input_graph.json',ROOT/'validation/artifacts/axial-material-sender-window-root-index-graph-table-combined-runtime-v15-20261010/input_creation_python_open_trace.json',ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010/actual_prepare_sources/prepare_cli_host_v15.py',ROOT/'validation/axial_material/prepare_qualified_AB_source_factor_production.py',ROOT/'validation/axial_material/moment_order_complete_history_resource_trie_20261010.py',ROOT/'validation/axial_material/qualify_refined_AAA_layered_full.py',ROOT/'validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py',ROOT/'validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/run_bounded_dragon.py']
dependencies=[pin(p)for p in dict.fromkeys(required)]
put('ROOT_CURRENT_BINDING_INPUT_CHECKLIST.json',dict(schema='SPOT_NEW_EPOCH_FULL_PURE_ACTUAL_CURRENT_INPUT_PIN_CHECKLIST_V1',complete_runtime_input_pins=dependencies,all_pins_actual_current_full_EOF=True,historical_codec_graphs_hashed_raw_not_decoded=True,old_original_canonical_unknown_bytes_still_unresolved=unknown,original_canonical_count=37590,unknown_canonical_count=53,current_complete_fresh_qualified=False,new_Q_created=False,host_and_driver_current_Source=proof['host'],Root_actual_review_and_binding_not_yet_created=True))
files=[pin(p)for p in sorted(OWN.iterdir())if p.is_file()]
assert sum(p['size_bytes']for p in files)<64*2**20 and not ATTEMPTS
freeze=dict(schema='SPOT_NEW_EPOCH_COMPLETE_FULL_PURE_SOURCE_NAMESPACE_BEFORE_OWN_FREEZE_V1',status='COMPLETE_CANDIDATE_SOURCES_FROZEN_PENDING_ROOT_REVIEW_AND_ACTUAL_RUN',root=str(OWN),files=files,own_file_exception='COMPLETE_CURRENT_CANDIDATE_SOURCE_FREEZE.json created after these files; no source qualification claimed by its self record',source_AST_checks=source_ast,driver_whole_original_inverse=True,host_whole_original_inverse=True,all_original_five_full_stage_and_function_bodies_retained=True,new_full_index_wire67_full238780_and_five_absence_cases_callable=True,original_pure_caps=dict(whole_seconds=60,stage_seconds=60,rss_mib=512,archive_bytes=64*2**20,threads=1,children_at_once=1,retries=0),all480_production_absences_verified=False,current_complete_fresh_host_prepared=False,current_Q_writer_prepared=False,old37590_scope_unknown_canonical_byte_inputs=53,no_regular_byte_input_converted_to_absence=True,full_graph_decoded=False,graph_or_control_Source_imported=False,PS_native_numeric_or_children_started=False,seconds=time.monotonic()-START,own_peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
put('COMPLETE_CURRENT_CANDIDATE_SOURCE_FREEZE.json',freeze)
print(json.dumps(dict(status=freeze['status'],freeze=pin(OWN/'COMPLETE_CURRENT_CANDIDATE_SOURCE_FREEZE.json'),regular_files_before_own_freeze=len(files),source_py_files=len(source_ast),raw_full_EOF_runtime_inputs=len(dependencies),host=pin(OWN/'complete_new_epoch_pure_host.py'),driver=pin(OWN/'complete_new_epoch_pure_controls.py'),new_Q_created=False,full_control_executed=False),allow_nan=False),flush=True)
