"""SOURCE-only finite V19 retarget; generation requires a real Root closed PREP summary."""
import ast
import hashlib
import json
from pathlib import Path
import re
import stat
import sys

BASE = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
DEST = Path(__file__).parent
OLD = BASE/'actual_complete_combined_build_v17_sources/combined_build_host.py'
OLD_SHA = 'cf2c3fd0e9404a3c2858c398d0457a2a6ece38b675e74c143564dac5894002f9'
OLD_INVERSE = BASE/'actual_complete_combined_build_v17_sources/Root_finite_build_host_source_inverse.json'
OLD_INVERSE_SHA = '29a05241b38bcd4d878d058dc27b023a07e8356993c53ff033575ed16d50a6d6'
ANCESTOR = BASE/'actual_complete_combined_prepare_v17_sources/combined_prepare_host.py'
ANCESTOR_SHA = '37d432b8c91ddec6816fed6f7cea11fbfcba7071655ea64bc0f3c562288185d3'
TARGET = Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py')
TARGET_SHA = '34efcc340b87257929e9d4cb06631455549327436d2bbdc5561639b6535e140b'
RECEIPTS = BASE/'actual_complete_combined_prepare_v19_receipts'
SUMMARY = RECEIPTS/'Root_actual_complete_combined_prepare_summary.json'
ROOT_TERMINAL = RECEIPTS/'Root_actual_prepare_tool_terminal_return.json'
NAMESPACE = RECEIPTS/'Root_actual_complete_prepare_namespace_manifest.json'
ART = '/Users/wen/spot/validation/artifacts/'
SOURCE = ART+'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v19-20261010'
OUT = ART+'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v19-20261010'
TERMINAL = ART+'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v19-20261010'
BUILD_HOST = ART+'axial-material-complete-combined-build-host-v19-20261010'
SOURCE_ARCHIVE = BASE/'actual_complete_combined_build_v19_sources'
DRAFT_STATUS = 'UNREADY_SOURCE_TEMPLATE_AWAIT_REAL_ROOT_V19_CLOSED_SUCCESSFUL_PREP'
# The first eleven mappings are fixed SOURCE bindings; six mappings require actual closed PREP evidence.
FIXED = [
('axial-material-complete-combined-build-host-v17-20261010','axial-material-complete-combined-build-host-v19-20261010',1),
('prepare_sender_window_root_index_graph_trace_table_combined_runtime_v17.py','prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py',2),
('feebcbb5894797d9f748a7b43e817b30da90e64068f17f141135121462ef234c',TARGET_SHA,1),
('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v17-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v19-20261010',1),
('axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v17-20261010','axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v19-20261010',4),
('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v17-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v19-20261010',1),
('actual_complete_combined_build_v17_sources','actual_complete_combined_build_v19_sources',1),
('SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V17','SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V19',1),
('AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V17_DECLARATION_V1','AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V19_DECLARATION_V1',1),
('AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V17_BUILD_SEAL_V1','AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V19_BUILD_SEAL_V1',1),
('AXMAT_V17_GENUINE_COMPLETE_COMBINED_BUILD_HOST_V1','AXMAT_V19_GENUINE_COMPLETE_COMBINED_BUILD_HOST_V1',1)]
DYNAMIC_SOURCE_TOKENS = [
('cb1984ee991230e9b56a9783acafe36bfb9063b4b641ebe64387d3e60c29fb30','actual_declaration',2),
('c743c01c3f40ac32e06a4f3371c82dfa4b84314b0c85509aa1710216afe569b2','actual_prep_terminal',2),
('actual_complete_combined_prepare_v17_receipts','actual_root_receipts_directory',2),
('07494a308553d0e42f861732f7f2c782bc0f77e7668aa307551fcc82c27bbf3e','actual_Root_summary',1),
('968801a327739feab4eafa5e77bb500dbf2f6f6c7a7303bf51fb528e7b4875a4','actual_complete_input_graph',1),
('6fb8fa8b22eee736c84dd8af4b06953635cc0a270fde51ad48062da3bd0e6b2e','actual_complete_creation_trace',1)]
FUTURE_BUSINESS_KEYS = [
'FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA',
'FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA',
'FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']

def pin(path, expected=None):
    path = Path(path)
    if '/validation/artifacts/' in str(path):
        raise ValueError('generator reads SOURCE/Root closed metadata only, never ART')
    if not path.is_absolute() or path.resolve() != path:
        raise ValueError('absolute ordinary no-alias source path required')
    first = path.lstat()
    if not stat.S_ISREG(first.st_mode) or first.st_nlink != 1:
        raise ValueError('ordinary unique source file required')
    data = path.read_bytes()
    last = path.lstat()
    fields = lambda s: [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    if fields(first) != fields(last) or len(data) != last.st_size:
        raise ValueError('complete SOURCE EOF pin changed during read')
    actual = hashlib.sha256(data).hexdigest()
    if expected is not None and actual != expected:
        raise ValueError('fixed SOURCE SHA mismatch')
    return data, dict(path=str(path),sha256=actual,identity=fields(last))

def original_source_checks():
    data, old_pin = pin(OLD,OLD_SHA)
    proof_data, inverse_pin = pin(OLD_INVERSE,OLD_INVERSE_SHA)
    ancestor_data, ancestor_pin = pin(ANCESTOR,ANCESTOR_SHA)
    target_data, target_pin = pin(TARGET,TARGET_SHA)
    old = data.decode()
    ip = json.loads(proof_data)
    if ip['finite_change_count'] != 13 or ip['host_sha256'] != OLD_SHA or ip['parent_sha256'] != ANCESTOR_SHA:
        raise ValueError('original thirteen-change full inverse required')
    inverse = old
    for record in reversed(ip['changes']):
        if inverse.count(record['after']) != record['count']:
            raise ValueError('old inverse count mismatch')
        inverse = inverse.replace(record['after'],record['before'])
    if inverse.encode() != ancestor_data:
        raise ValueError('complete original cf2c to 37d inverse mismatch')
    for before, _, count in FIXED + DYNAMIC_SOURCE_TOKENS:
        if old.count(before) != count:
            raise ValueError('fixed finite substitution count mismatch')
    vals = {}
    for n in ast.parse(target_data.decode()).body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            try: vals[n.targets[0].id]=ast.literal_eval(n.value)
            except (ValueError,TypeError): pass
    if vals['DRAFT_STATUS'] != 'READY_REVIEWED_V19_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY':
        raise ValueError('actual installed canonical SOURCE binding required')
    if any(vals[k] is not None for k in FUTURE_BUSINESS_KEYS):
        raise ValueError('all six future factory business pins remain None')
    labels = next(ast.literal_eval(n.value) for n in ast.parse(old).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='EXPECTED_LABELS' for t in n.targets))
    if labels != ['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']:
        raise ValueError('all five original stages required')
    compile(old,str(OLD),'exec')
    return old,ip,[old_pin,inverse_pin,ancestor_pin,target_pin]

def metadata_reference(ref, expected_path):
    if ref['path'] != str(expected_path) or re.fullmatch('[0-9a-f]{64}',ref['sha256']) is None:
        raise ValueError('fixed complete Root metadata reference required')
    data, actual = pin(expected_path,ref['sha256'])
    if actual != ref:
        raise ValueError('full seven-field Root metadata reference mismatch')
    return json.loads(data), actual

def output_reference(ref, expected_path):
    if set(ref) != {'path','sha256','identity'} or ref['path'] != expected_path:
        raise ValueError('complete actual Root writer output pin required')
    if re.fullmatch('[0-9a-f]{64}',ref['sha256']) is None or not isinstance(ref['identity'],list) or len(ref['identity'])!=7:
        raise ValueError('actual Root output hash and seven identity fields required')
    if any(type(x) is not int for x in ref['identity']):
        raise ValueError('actual Root output pins must be typed')
    if ref['identity'][4] <= 0 or ref['identity'][3]!=1 or not stat.S_ISREG(ref['identity'][2]):
        raise ValueError('ordinary complete actual output metadata required')
    return ref

def write_new(path,data):
    with Path(path).open('xb') as f: f.write(data)

def main():
    old, old_inverse, sources = original_source_checks()
    if sys.argv[1:] == ['--check-source-only']:
        value = dict(status='SOURCE_DESIGN_ONLY_AWAIT_REAL_ROOT_CLOSED_V19_PREP',
            complete_original_cf2c_inverse_to_37d=True,original_thirteen_change_proof=old_inverse,
            checked_source_pins=sources,fixed_retarget_count=11,closed_actual_binding_retarget_count=6,
            all_five_original_stages=True,outer_seconds=1800,inner_seconds=600,rss_mib=512,
            archive_bytes=2*2**30,history_bytes=96*2**30,min_free_bytes=8*2**30,
            threads=1,children=1,retries=0,scope=['HOST','SOURCE','OUT','TERMINAL','new_SOURCE_ARCHIVE'],
            actual_V19_declaration_sha256=None,actual_V19_prep_terminal_sha256=None,
            actual_V19_Root_prepare_summary_sha256=None,actual_V19_complete_graph_sha256=None,
            actual_V19_creation_trace_sha256=None,host_generated=False,business_executed=False,
            numeric_payload_read=False,ART_read_or_written=False,native_executed=False,
            AAA_accuracy_qualified=False,ABA_admitted=False)
        report = DEST/'SOURCE_DESIGN_REPORT.json'
        write_new(report,(json.dumps(value,indent=2,allow_nan=False)+'\n').encode())
        print(json.dumps(dict(status=value['status'],report=str(report),report_sha256=hashlib.sha256(report.read_bytes()).hexdigest(),host_generated=False,business_executed=False)))
        return
    # Only the pinned real Root closed-success summary below can enable metadata-only host generation.
    if len(sys.argv)!=3 or Path(sys.argv[1])!=SUMMARY or re.fullmatch('[0-9a-f]{64}',sys.argv[2]) is None:
        raise ValueError('one actual fixed Root closed PREP summary path and full SHA required; no placeholder binding')
    summary_data, summary_pin = pin(SUMMARY,sys.argv[2])
    s = json.loads(summary_data)
    if s['schema']!='ROOT_V19_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1' or s['status']!='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD':
        raise ValueError('actual V19 PREP success summary required')
    terminal, terminal_pin = metadata_reference(s['Root_actual_terminal'],ROOT_TERMINAL)
    tr = terminal['terminal_tool_return']
    if terminal['closed'] is not True or type(tr.get('exit_code')) is not int or tr['exit_code']!=0 or 'session_id' in tr:
        raise ValueError('real Root typed EXIT0 closed terminal required')
    if terminal.get('exit_code',0)!=0 or terminal.get('session_repolled_after_close',False) is not False:
        raise ValueError('Root successful closed terminal with no repoll required')
    if s['Root_actual_terminal']!=s['actual_root_terminal']:
        raise ValueError('Root terminal aliases must be the same complete actual pin')
    cap_keys=('whole_wall_cap_seconds','stage_wall_cap_seconds','rss_mib','joint_archive_cap_bytes','history_cap_bytes','free_floor_bytes','threads','children','retries')
    if tuple(s[k] for k in cap_keys)!=(1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0):
        raise ValueError('all original complete PREP caps required')
    if s['original_caps_preserved'] is not True or not 0<=s['sampled_peak_rss_mib']<512 or not 0<s['child_seconds']<=600 or not s['child_seconds']<=s['whole_seconds']<1800 or not 0<s['joint_archive_bytes']<2*2**30:
        raise ValueError('actual original bounded PREP metadata required')
    for key in ('original_five_build_stages_executed','whole_combined_INPUT_admitted','new_native_transport_executed','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','cleanup_performed','goal_complete'):
        if s[key] is not False:
            raise ValueError('PREP only boundaries required')
    namespace, namespace_pin = metadata_reference(s['namespace_manifest'],NAMESPACE)
    if namespace['schema']!='ROOT_V19_ACTUAL_COMPLETE_PREPARE_ALL_NAMESPACES_V1' or namespace['no_build_or_native_credit'] is not True:
        raise ValueError('actual closed complete namespace freeze required')
    ns = {x['root']:x for x in namespace['namespaces']}
    expected_roots={ART+'axial-material-complete-combined-prepare-host-v19-20261010',SOURCE,OUT,TERMINAL,str(BASE/'actual_complete_combined_prepare_v19_sources')}
    if len(ns)!=len(namespace['namespaces']) or set(ns)!=expected_roots:
        raise ValueError('all five complete actual H/S/O/T/D namespaces required')
    desired = {
        'actual_declaration':output_reference(s['actual_declaration'],OUT+'/declaration.json'),
        'actual_complete_input_graph':output_reference(s['actual_complete_input_graph'],OUT+'/input_graph.json'),
        'actual_complete_creation_trace':output_reference(s['actual_complete_creation_trace'],OUT+'/input_creation_python_open_trace.json'),
        'actual_prep_terminal':output_reference(s['formal_PREP_terminal'],TERMINAL+'/declaration_terminal_return.json')}
    for key,ref in desired.items():
        folder = TERMINAL if key=='actual_prep_terminal' else OUT
        relative = ref['path'][len(folder)+1:]
        if ns[folder]['files'][relative]!=ref:
            raise ValueError('actual summary and complete namespace output binding disagree')
    recorded_sources = {p['path']:p for p in namespace['all_original_inputs_fresh_full_EOF_SHA7ID_unchanged']}
    if recorded_sources[str(TARGET)]!=sources[-1] or namespace['canonical_factory']!=sources[-1]:
        raise ValueError('canonical factory SOURCE pin must match actual PREP source')
    changes = list(FIXED)
    dynamic = {k:v['sha256'] for k,v in desired.items()}
    dynamic['actual_root_receipts_directory']='actual_complete_combined_prepare_v19_receipts'
    dynamic['actual_Root_summary']=summary_pin['sha256']
    changes += [(before,dynamic[key],count) for before,key,count in DYNAMIC_SOURCE_TOKENS]
    text = old
    records = []
    for before,after,count in changes:
        if text.count(before)!=count:
            raise ValueError('finite source substitution no longer exact')
        text = text.replace(before,after)
        records.append(dict(before=before,after=after,count=count))
    inverse = text
    for r in reversed(records):
        if inverse.count(r['after'])!=r['count']:
            raise ValueError('complete V19 to cf2c inverse occurrence mismatch')
        inverse = inverse.replace(r['after'],r['before'])
    if inverse!=old:
        raise ValueError('entire V19 host inverse to cf2c required')
    compile(text,str(DEST/'combined_build_host.py'),'exec')
    for ref in sources+[summary_pin,terminal_pin,namespace_pin]:
        _,again = pin(ref['path'],ref['sha256'])
        if again!=ref:
            raise ValueError('all SOURCE and actual Root metadata inputs remain fresh and exact')
    proof = dict(schema='AXMAT_V19_FINITE_BUILD_HOST_SOURCE_INVERSE_V1',status='SOURCE_ONLY_NOT_EXECUTED',
        parent_path=str(OLD),parent_sha256=OLD_SHA,host_path=str(DEST/'combined_build_host.py'),
        host_sha256=hashlib.sha256(text.encode()).hexdigest(),finite_change_count=len(records),changes=records,
        full_byte_inverse_to_unchanged_cf2c_parent=True,original_cf2c_to_37d_thirteen_change_inverse=old_inverse,
        checked_source_pins=sources,actual_Root_closed_PREP_summary=summary_pin,
        actual_Root_closed_terminal=terminal_pin,actual_Root_complete_namespace_freeze=namespace_pin,
        actual_output_pins_bound_by_closed_Root_metadata_without_ART_read=desired,
        genuine_guard_and_MRO_unchanged=True,outer_whole_command_seconds=1800,
        original_inner_stages=5,original_inner_stage_seconds=600,original_rss_mib=512,
        original_archive_cap_bytes=2*2**30,history_bytes=96*2**30,min_free_bytes=8*2**30,
        threads=1,children_at_once=1,retries=0,
        archive_scope_includes_H_SOURCE_OUT_TERMINAL_new_SOURCE_ARCHIVE=True,
        new_source_archive=str(SOURCE_ARCHIVE),business_host_namespace=BUILD_HOST,
        host_executed=False,business_executed=False,ART_read_or_written=False,numeric_payload_read=False,
        native_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False)
    for p in (DEST/'combined_build_host.py',DEST/'Root_finite_build_host_source_inverse.json'):
        if p.exists(): raise ValueError('source candidate output must be fresh')
    write_new(DEST/'combined_build_host.py',text.encode())
    write_new(DEST/'Root_finite_build_host_source_inverse.json',(json.dumps(proof,indent=2,allow_nan=False)+'\n').encode())
    print(json.dumps(dict(status='SOURCE_ONLY_NOT_EXECUTED',host_candidate=proof['host_path'],
        host_sha256=proof['host_sha256'],finite_change_count=len(records),full_inverse_cf2c_37d=True,
        actual_Root_summary_sha256=summary_pin['sha256'],business_executed=False)))

if __name__=='__main__': main()
