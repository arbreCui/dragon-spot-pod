"""Source-only installed6a full fresh protocol; original genuine guard unchanged."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import time
import gzip
import hashlib
import math
import stat
BASE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
SUPPORT=BASE/'actual_prepare_sources/prepare_cli_host_v15.py'
SUPPORT_SHA='3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'
HOST = Path('/Users/wen/spot/validation/artifacts/axial-material-stable-wire-sort-complete-fresh-host-v28-20261011-dwah5ubd')
OUT = Path('/Users/wen/spot/validation/artifacts/axial-material-stable-wire-sort-complete-fresh-v28-20261011-dwah5ubd')
SOURCE_ARCHIVE = Path('/private/tmp/SPOT_stable_wire_v28_fullfresh_source_only_dwah5ubd/sources')
RECEIPTS = Path('/private/tmp/SPOT_stable_wire_v28_fullfresh_source_only_dwah5ubd/receipts')
TARGET=SOURCE_ARCHIVE/'fresh_verifier_controls.py'
TARGET_SHA = 'b77f3530253d2fe7a70001cb23cf28482fd6e671e544f74f531fb22e70ae02a9'
SOURCE_STATUS = 'READY_SOURCE_BOUND_BY_ROOT'
BOUND_HELPER_PIN = {'path': '/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_read_open_short_index_stable_wire_sort_20261011.py', 'sha256': '6a0b6816cbc8c4ce026018bf1952ffcc720c8a0efe6b4c3c39c4c1040da28ff3', 'identity': [16777229, 49645417, 33188, 1, 152950, 1791696656438509035, 1791696656438509035]}
INSTALL_WITNESS_PIN = {'path': '/private/tmp/Root_stable_wire_source_install_actual_tool_returns_20261011.json', 'sha256': '7c8897152c3cb390f30ff0ac6b3acb3669159d06753168c92317d091fd7a7309', 'identity': [16777229, 49645429, 33188, 1, 1397, 1791696674759719679, 1791696674759719679]}
SOURCE_INSTALL_RECORD_PIN = {'path': '/Users/wen/spot/validation/artifacts/axial-material-stable-wire-sort-source-install-20261011/ACTUAL_SOURCE_INSTALL_WITNESS.json', 'sha256': '8a7ec7765b0ecd4acd43d17d70daeb5b2409daffd9caf301757685d7ec8fff38', 'identity': [16777229, 49645418, 33188, 1, 158516, 1791696656847741398, 1791696656847741398]}
PRIOR_ACTUAL_6A_PURE_PROTOCOL_PINS = {'host_result': {'path': '/Users/wen/spot/validation/artifacts/axial-material-stable-wire-sort-original-pure-controls-host-v27-20261011-odcl3yl4/result.json', 'sha256': '0aaed12e13c6109345ab859305d0fbef73a73b8a056343a02e1b0ffd07e974f6', 'identity': [16777229, 49648052, 33188, 1, 625706, 1791698090465023371, 1791698090465023371]}, 'control_report': {'path': '/Users/wen/spot/validation/artifacts/axial-material-stable-wire-sort-original-pure-controls-v27-20261011-odcl3yl4/ACTUAL_REPORT.json', 'sha256': 'b167686da6d8e73123285dc355fd7e3686481b67b82359202c27f28f9fa4ae0f', 'identity': [16777229, 49648041, 33188, 1, 4002456, 1791698089581686097, 1791698089581686097]}, 'actual_launch_and_closed_tool_returns': {'path': '/private/tmp/Root_v27_pure_protocol_actual_tool_returns_20261011.json', 'sha256': '83cda24cd118a688362eb4f3207d22c459378ca840b2849059ca1a4812cbd45a', 'identity': [16777229, 49648134, 33188, 1, 1214, 1791698103755175345, 1791698103755175345]}, 'Root_external_closed_binding': {'path': '/Users/wen/spot/validation/artifacts/axial-material-stable-wire-sort-original-pure-controls-root-closure-v27-20261011-v3/ROOT_EXTERNAL_CLOSED_BINDING.json', 'sha256': '418da5c9433ee53ed7f2993cbde62bae78fd3ccfb1aa5ad9ddd4d13d5bd966e9', 'identity': [16777229, 49648905, 33188, 1, 184890, 1791698556603299604, 1791698556603299604]}, 'Root_external_binding_tool_returns': {'path': '/private/tmp/Root_v27_pure_external_closure_v3_actual_tool_returns_20261011.json', 'sha256': '192359997ecad586f2e4e5719f623bad329a9006fb13a0d61ec5a3fc938d07de', 'identity': [16777229, 49648958, 33188, 1, 16911, 1791698613695273043, 1791698613695273043]}}
SUPPORTING_ACTUAL_EVIDENCE_PINS = [{'path': '/private/tmp/SPOT_stable_wire_v27_pure_protocol_odcl3yl4/sources/pure_helper_controls.py', 'sha256': '7ae39903114ec50ab77b203edd7cf88f16690c0519af3e2e8877dbe28d8700a8', 'identity': [16777229, 49646973, 33188, 1, 72784, 1791697609382535577, 1791697609382535577]}, {'path': '/private/tmp/SPOT_stable_wire_v27_pure_protocol_odcl3yl4/sources/pure_helper_controls_host.py', 'sha256': '17b433555b65347ee93e7f3c6499a6b1dd3e0d54bd23a691148eaf948bb9aff7', 'identity': [16777229, 49646974, 33188, 1, 29499, 1791697609392600562, 1791697609392600562]}, {'path': '/private/tmp/SPOT_stable_wire_v27_pure_protocol_odcl3yl4/sources/inactive_audit_snapshot_controls_SOURCE_ONLY.py', 'sha256': 'd439eb9641f45e09c17814a38a16dc7e2cbb6120fc09119df901e415daf28483', 'identity': [16777229, 49646970, 33188, 1, 23962, 1791697609379226943, 1791697609379226943]}, {'path': '/private/tmp/SPOT_stable_wire_v27_pure_protocol_odcl3yl4/sources/read_open_short_index_state_controls.py', 'sha256': 'c3a81b4cfd93f40e458e999305e6917227ad3fbb08d4b6116ed6cddf281d6f95', 'identity': [16777229, 49646971, 33188, 1, 14682, 1791697609379463152, 1791697609379463152]}, {'path': '/private/tmp/SPOT_stable_wire_v27_pure_protocol_odcl3yl4/sources/wire67_saved_evidence_review.py', 'sha256': 'f133f92b39c5376dd719eb3942ac7049c34a850c500afd79028b63f12b9a207c', 'identity': [16777229, 49646972, 33188, 1, 43643, 1791697609379680986, 1791697609379680986]}, {'path': '/private/tmp/SPOT_stable_wire_v27_pure_protocol_odcl3yl4/FINAL_REVIEW_EVIDENCE_MANIFEST.json', 'sha256': 'b82954b000645076077fb6357033694dc8d6c8c2859c3020f5d75cb7e38dc018', 'identity': [16777229, 49647241, 33188, 1, 16516, 1791697801881380345, 1791697801881380345]}, {'path': '/private/tmp/SPOT_stable_wire_v27_pure_protocol_odcl3yl4/FINAL_SOURCE_ONLY_MANIFEST.json', 'sha256': 'aa708a61344f004454e2fd84111c8cd3672da36720f9ebb4f4a317ade835b661', 'identity': [16777229, 49646978, 33188, 1, 3846, 1791697609433991462, 1791697609433991462]}, {'path': '/private/tmp/SPOT_stable_wire_v27_pure_protocol_odcl3yl4/SOURCE_ONLY_CONTRACT.json', 'sha256': '1e9480f07b6195a710269d1506712f885e22d2de4defd5804e793b8290120086', 'identity': [16777229, 49646976, 33188, 1, 16807, 1791697609419071965, 1791697609419071965]}, {'path': '/private/tmp/SPOT_stable_wire_v27_pure_protocol_odcl3yl4/SOURCE_DERIVATION_FULL_INVERSE.json', 'sha256': '9a88c5375e1bcc1e7489230c18a2fa9b6522f09cdb60e5c43ea9bef8257c6083', 'identity': [16777229, 49646975, 33188, 1, 22184, 1791697609418622464, 1791697609418622464]}, {'path': '/private/tmp/SPOT_stable_wire_v27_pure_protocol_odcl3yl4/SOURCE_FAMILY_DECLARATION.json', 'sha256': '125791e54eae926f2d63ede6c0bac245cbe680c62689f7e5a5cc0101d17eedc9', 'identity': [16777229, 49646977, 33188, 1, 2873, 1791697609419211715, 1791697609419211715]}, {'path': '/private/tmp/SPOT_stable_wire_v27_pure_protocol_odcl3yl4/STATIC_SOURCE_AND_GUARD_REVIEW.json', 'sha256': 'acabec328da8425b5568d34ce0f3e06096bfaaa320cb4ba669cc0721346f01b5', 'identity': [16777229, 49647185, 33188, 1, 2899, 1791697745871937602, 1791697745871937602]}, {'path': '/private/tmp/SPOT_stable_wire_v27_pure_protocol_odcl3yl4/ACTUAL_STATIC_SOURCE_REVIEW_TOOL_RETURN.json', 'sha256': 'b68702333e307ddba3f447da543ffc912aab8f8f943252f62663fe5e0536dd40', 'identity': [16777229, 49647192, 33188, 1, 2600, 1791697751272147740, 1791697751272147740]}, {'path': '/private/tmp/SPOT_stable_wire_v27_pure_protocol_odcl3yl4/REPORT_SOURCE_ONLY.txt', 'sha256': 'e27fb4438f6c3e9ee328d1078617dc8e64fe911798fa8b34a6a355da7b9db862', 'identity': [16777229, 49647186, 33188, 1, 4409, 1791697745872055102, 1791697745872055102]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-full370-reaction-coverage-and-input-memory-20261011/actual_complete_fresh_input/ACTUAL_V3_COMPLETE_VERIFY_GRAPH_PROFILE.json', 'sha256': '30e2dad228114d38dfec9da733a86cde889e7f23c24bf642aea62bbaa357789e', 'identity': [16777229, 49645772, 33188, 1, 1550460, 1791696970138674919, 1791696970138674919]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-full370-reaction-coverage-and-input-memory-20261011/actual_complete_fresh_input/ACTUAL_V3_FRESH_READ_OPEN_SNAPSHOT.json', 'sha256': '8553ccfdc833f57f20a7a7e161fa12d25959fa02cd6fd10be85c4481537e0018', 'identity': [16777229, 49645771, 33188, 1, 17777330, 1791696970132014775, 1791696970132014775]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-full370-reaction-coverage-and-input-memory-20261011/actual_complete_fresh_input/FRESH_COMPLETE_V3_PROFILE_DRIVER.py', 'sha256': 'd53bf4229146f2f5663b103722f72ee85249ac426e8d1a857164c5c71cdd35f3', 'identity': [16777229, 49645773, 33188, 1, 18854, 1791696970139454338, 1791696970139454338]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-full370-reaction-coverage-and-input-memory-20261011/actual_complete_fresh_input/FRESH_DRIVER_SOURCE_DERIVATION.json', 'sha256': 'f49d8a603167a47d6c51cc38258bc58ffdbc4a644197e3c12c2995d90292d637', 'identity': [16777229, 49645774, 33188, 1, 14633, 1791696970139675963, 1791696970139675963]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-full370-reaction-coverage-and-input-memory-20261011/actual_complete_fresh_input/ACTUAL_FRESH_V3_PRELAUNCH_MANIFEST.json', 'sha256': '78ab50dd6106f66e19192a66dd7e6322d3d0201c5a0ca6a6e004b26eeacef371', 'identity': [16777229, 49645775, 33188, 1, 3517, 1791696970139828589, 1791696970139828589]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-full370-reaction-coverage-and-input-memory-20261011/actual_complete_fresh_input/ACTUAL_FRESH_V3_LAUNCH_TOOL_RETURN.json', 'sha256': '60fd9fa5ed7163b6abf936af99463d547f0dc56b1776c8e396c778c86a976bb0', 'identity': [16777229, 49645776, 33188, 1, 130, 1791696970139963464, 1791696970139963464]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-full370-reaction-coverage-and-input-memory-20261011/actual_complete_fresh_input/ACTUAL_FRESH_V3_CLOSED_TOOL_RETURN.json', 'sha256': '5550a8eefecb62d3a9c2509c83b5d9e3cc74fa3ecd0b2cf59e9234ad77b68e61', 'identity': [16777229, 49645777, 33188, 1, 581, 1791696970140088506, 1791696970140088506]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-full370-reaction-coverage-and-input-memory-20261011/actual_complete_fresh_input/FINAL_FRESH_COMPLETE_V3_EVIDENCE_MANIFEST.json', 'sha256': '267f2060d270404112722ea256433398b8a850185843670400a66cdbebcf2224', 'identity': [16777229, 49646087, 33188, 1, 13092, 1791697256451076720, 1791697256451076720]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-full370-reaction-coverage-and-input-memory-20261011/actual_complete_fresh_input/FRESH_COMPLETE_V3_SCOPE_REPORT.txt', 'sha256': '65aa86824627aa93e57ef6028db6b75bf2cbe5b72dd7aa9ea0e24bc36ab2355a', 'identity': [16777229, 49646088, 33188, 1, 5817, 1791697256451272137, 1791697256451272137]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-full370-reaction-coverage-and-input-memory-20261011/ACTUAL_RESULT_PUBLICATION_WITNESS.json', 'sha256': '28ea9eef081e9f35a0134c28bb639589d2cc671e551310f2d25bedb0422ce2ad', 'identity': [16777229, 49645780, 33188, 1, 205089, 1791696970977366451, 1791696970977366451]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-full370-reaction-coverage-and-input-memory-20261011/ADDITIONAL_ACTUAL_RESULT_PUBLICATION_WITNESS.json', 'sha256': '2185e68f6cb0b15b865ee31591eab74df77c7c3fecd5bd418a3810d053cb6e55', 'identity': [16777229, 49646092, 33188, 1, 171383, 1791697257238834691, 1791697257238834691]}, {'path': '/private/tmp/Root_v27_independent_source_review_20261011.json', 'sha256': 'bcc874295ff418ee1d17c516d015b2eccbb4d7b30117e9e0dcb6ef149505f028', 'identity': [16777229, 49647944, 33188, 1, 19224, 1791698060242987809, 1791698060242987809]}]
UNKNOWN_Q=None
UNKNOWN_BUSINESS_PINS=None

AUDIT_CONTROL_PATH = '/private/tmp/SPOT_stable_wire_v28_fullfresh_source_only_dwah5ubd/sources/inactive_audit_snapshot_controls_SOURCE_ONLY.py'
AUDIT_CONTROL_SHA256 = 'd439eb9641f45e09c17814a38a16dc7e2cbb6120fc09119df901e415daf28483'
AUDIT_CONTROL_SOURCE_BYTES = 23962
GRAPH_PATH=Path('/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-memory-observation-capture-pre-graph-gc-20261010/input_graph.json')
GRAPH_SHA='a91c1e63bd768575e715e735886f168b9af6722fddf2bb002317376da5d63ad1'
GRAPH_IDENTITY=[16777229, 49537790, 33188, 1, 45841587, 1791657732241195952, 1791657732241195952]
SEAL_SHA='b6b3b1477835bd6e312ac833d4cc681e0b7ca15482964f88daf0edb581d60206'
TERM_SHA='ad1d11d68f2ae052068bd6d752ce7b2d64c6cbfcf699713aa684cdc347655d7e'
WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,64*2**20

RETURN_FIELDS=['schema', 'classification', 'consumer_scope', 'consumer_selected_literal_and_canonical_paths', 'consumer_complete_namespace_root_sequence', 'scope', 'phase', 'graph_content_sha256', 'fresh_reader_contract', 'canonical_files_read', 'actual_bytes_read', 'byte_count_scope', 'logical_owner_requirements', 'exhaustive_namespaces_checked', 'explicit_aliases_checked', 'coverage', 'trace_coverage', 'live_io_scope', 'live_subprocesses_reexecuted', 'declared_absence_inputs_checked_before_and_after_bytes', 'absence_inputs_are_not_regular_bytes_or_science', 'caller_must_recheck_current_OS_identity_and_live_probe_results', 'typed_snapshot', 'science_qualification_created', 'live_resources_verified', 'external_declaration_exit0_verified', 'caller_must_verify_live_environment_modules_PID_time_and_resources']
TRACE_FIELDS=['schema', 'coverage', 'records', 'subprocess_records', 'unique_records', 'actual_read_open_attempts', 'record_storage', 'success_of_open_attempt_is_not_observed', 'native_libc_HDF5_loader_and_directory_stat_are_not_traced']

def _fail_constant(value):
    raise ValueError('nonfinite JSON metadata is rejected: '+value)

def _json_object(path):
    with Path(path).open('r') as stream:value=json.load(stream,parse_constant=_fail_constant)
    if type(value) is not dict:raise ValueError('complete object metadata required')
    return value

def _finite_number(value,low,high):
    return type(value) in (int,float) and math.isfinite(value) and low<=value<high

def _source_namespace(support):
    root=SOURCE_ARCHIVE
    if not stat.S_ISDIR(root.lstat().st_mode) or root.is_symlink():raise ValueError('normal SOURCE directory required')
    directories=[];files=[]
    for parent,dirs,names in os.walk(root,followlinks=False):
        dirs.sort();names.sort();directory=Path(parent)
        if directory.is_symlink():raise ValueError('SOURCE alias directory prohibited')
        directories.append(dict(path=str(directory),identity=support.identity(directory)))
        for name in dirs:
            if (directory/name).is_symlink():raise ValueError('SOURCE symlink prohibited')
        for name in names:
            path=directory/name
            if not stat.S_ISREG(path.lstat().st_mode) or path.lstat().st_nlink!=1 or path.is_symlink():raise ValueError('SOURCE namespace contains a nonregular/nonprivate member')
            files.append(support.pin(path))
    if not files or not any(Path(p['path'])==TARGET for p in files) or not any(Path(p['path']).resolve()==Path(__file__).resolve() for p in files):raise ValueError('complete actual driver and host SOURCE required')
    return dict(schema='AXMAT_V25_ACTUAL_COMPLETE_PRIVATE_INACTIVE_AUDIT_FRESH_SOURCE_NAMESPACE_V1',root=str(root),directories=directories,files=files,symlinks=[],complete_dynamic_before_after=True,Root_external_freeze_and_host_source_pin_required=True)

def _driver_pin(support,pin,path):
    actual=support.pin(path,pin['sha256'])
    if actual!={key:pin[key] for key in ('path','sha256','identity')} or type(pin.get('size_bytes')) is not int or pin['size_bytes']!=actual['identity'][4]:raise ValueError('complete driver-produced output/input SHA7identity differs')
    return actual

def _gzip_object(support,pin,path):
    actual=_driver_pin(support,pin,path)
    if pin.get('complete_JSON_wire_gzip_decompression_EOF_SHA_verified') is not True or pin.get('no_fields_or_records_filtered') is not True:raise ValueError('complete gzip wire evidence required')
    digest=hashlib.sha256();count=0
    with gzip.open(path,'rb') as stream:
        while True:
            block=stream.read(2**20)
            if not block:break
            digest.update(block);count+=len(block)
    if type(pin.get('uncompressed_JSON_bytes')) is not int or count!=pin['uncompressed_JSON_bytes'] or digest.hexdigest()!=pin['uncompressed_JSON_sha256']:raise ValueError('full gzip decompression EOF/SHA differs')
    with gzip.open(path,'rt',encoding='ascii') as stream:value=json.load(stream,parse_constant=_fail_constant)
    if type(value) is not dict or support.pin(path,pin['sha256'])!=actual:raise ValueError('complete gzip JSON object or byte identity changed')
    return value,actual

def load_snapshot_control_Source(path, sha256, source_bytes):
    # New controller dependency is full-pinned before and after import/use.
    source = Path(path)
    before = source.lstat()
    identity_before = [before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
                       before.st_size, before.st_mtime_ns, before.st_ctime_ns]
    if before.st_size != source_bytes or hashlib.sha256(source.read_bytes()).hexdigest() != sha256:
        raise ValueError('complete private snapshot controller SOURCE differs')
    spec = importlib.util.spec_from_file_location('actual_root_private_snapshot_metadata_controls', source)
    if spec is None or spec.loader is None:
        raise ValueError('private snapshot controller loader missing')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    after = source.lstat()
    if identity_before != [after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
                          after.st_size, after.st_mtime_ns, after.st_ctime_ns]:
        raise ValueError('private snapshot controller SOURCE changed during import')
    return module, dict(path=str(source), sha256=sha256, size_bytes=source_bytes, identity=identity_before)


def _full_controls(support,report,admission,watch,command):
    expected='ACTUAL_COMPLETE_FRESH_HELPER_VERIFIER_CONTROL_RETURNED_PENDING_EXTERNAL_ROOT'
    if admission['status']!=expected or Path(admission['report']['path'])!=OUT/'ACTUAL_REPORT.json':raise ValueError('actual complete fresh verifier stdout required')
    report_pin=_driver_pin(support,admission['report'],OUT/'ACTUAL_REPORT.json')
    if report['schema']!='AXMAT_NEXT_HELPER_COMPLETE_FRESH_VERIFIER_CONTROL_V1' or report['status']!=expected or type(report['actual_success_pins']) is not dict:raise ValueError('actual full fresh report required')
    scope=('business_component_executed','numeric_or_native_executed','whole_business_INPUT_qualified','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','helper_metadata_qualified')
    if any(report.get(k) is not False for k in scope) or report.get('actual_external_genuine_host_and_Root_closed_exit0_required') is not True:raise ValueError('metadata-only scope and external actual Root terminal required')
    if (report['whole_host_seconds'],report['stage_seconds'],report['rss_mib'],report['joint_HOST_SOURCE_OUT_archive_bytes'],report['history_bytes'],report['min_free_bytes'],report['threads'],report['children'],report['retries'])!=(1800,600,512,64*2**20,96*2**30,8*2**30,1,1,0):raise ValueError('complete unchanged control resource contract required')
    claim=_json_object(OUT/'ACTUAL_RUN_CLAIM.json')
    if any(type(v) is not int for v in (watch.get('pid'),claim.get('PID'),claim.get('parent_PID'),report.get('PID'),report.get('parent_PID'),admission.get('PID'),admission.get('parent_PID'))) or not watch['pid']>0 or not claim['PID']==report['PID']==admission['PID']==watch['pid'] or not claim['parent_PID']==report['parent_PID']==admission['parent_PID']==os.getpid():raise ValueError('actual normal host and watched child PID binding required')
    if claim['phase']!='helper_complete_fresh_verifier_control' or (claim['threads'],claim['children'],claim['retries'])!=(1,1,0):raise ValueError('actual driver claim contract differs')
    if report['fixed_inputs_before']!=report['fixed_inputs_after']:raise ValueError('all actual driver fixed inputs changed')
    for key,pin in report['fixed_inputs_before'].items():_driver_pin(support,pin,Path(pin['path']))
    helper=report['fixed_inputs_before']['new_helper'];graph=report['fixed_inputs_before']['stored_graph'];driver=report['fixed_inputs_before']['driver']
    if {k:helper[k] for k in ('path','sha256','identity')}!=BOUND_HELPER_PIN or helper!=claim['helper'] or graph!=claim['graph'] or driver!=claim['driver'] or Path(driver['path'])!=TARGET or driver['sha256']!=TARGET_SHA or Path(graph['path'])!=GRAPH_PATH or graph['sha256']!=GRAPH_SHA or graph['identity']!=GRAPH_IDENTITY:raise ValueError('actual installed helper/full storedgraph/driver identity differs')
    small=report['private_trace_controls'];positive=small['positive_controls'];negative=small['rejections']
    if len(positive)!=4 or {c['case'] for c in positive}!={'default_list','default_tuple','explicit_False_list','probe_owned_builtin_list_True'} or len(negative)!=3 or {c['case'] for c in negative}!={'nonbool_consume','tuple_True','list_subclass_True'}:raise ValueError('all new private trace controls required')
    for case in positive:
        if case['full_normalized_return_type_order_value_floatbits_and_bytes_equal_old_bcd'] is not True or (case.get('caller_full_identity_type_order_value_floatbits_unchanged') is not True and case.get('owned_list_completely_cleared') is not True):raise ValueError('complete private trace equivalence/nonmutation control failed')
    if any(c['rejected'] is not True or c['class_name']!='InputGraphError' or c['caller_type_identity_nested_value_order_floatbits_unchanged'] is not True for c in negative) or small['old60pure_control_functions_not_changed'] is not True or small['augmented_records_are_not_claimed_as_actual_full_verifier_trace'] is not True:raise ValueError('all private rejects and honest small codec trace required')
    metadata=report['independent_full_saved_graph_metadata']
    wanted=dict(requirement_row_count=238780,requirement_column_count=5,canonical_files=37445,owners=4473,namespaces=86,aliases=186,saved_trace_records=64108,absence_inputs=479,closure_categories=9,scope='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION',consumer_scope=None,newly_declared_input_paths={},newly_declared_input_pins={})
    if any(metadata.get(k)!=v or type(metadata.get(k)) is not type(v) for k,v in wanted.items()) or len(metadata['complete_coverage_fields'])!=9:raise ValueError('all complete current storedgraph scope/counts required')
    expected,expected_pin=_gzip_object(support,report['expected_complete_return_contract'],OUT/'EXPECTED_COMPLETE_RETURN_CONTRACT.json.gz')
    verified,verified_pin=_gzip_object(support,report['actual_complete_verifier_return'],OUT/'ACTUAL_COMPLETE_VERIFIER_RETURN.json.gz')
    encoder=dict(ensure_ascii=True,sort_keys=False,separators=(',',':'),allow_nan=False)
    if json.dumps(expected,**encoder)!=json.dumps(verified,**encoder) or list(verified)!=RETURN_FIELDS or report['complete_return_fields_retained']!=RETURN_FIELDS or report['complete_expected_coverage_tracecoverage_scope_snapshot_and_counts_equal'] is not True:raise ValueError('full public expected/actual return field/type/order/value equality required')
    if report['expected_complete_return_contract']['uncompressed_JSON_sha256']!=report['actual_complete_verifier_return']['uncompressed_JSON_sha256']:raise ValueError('complete expected/actual return wire SHA differs')
    if verified['schema']!='AXMAT_COMBINED_RUNTIME_FRESH_INPUT_GRAPH_VERIFICATION_V2' or verified['classification']!='FRESH_INPUT_BYTES_NAMESPACES_ALIASES_VERIFIED_ONLY' or verified['consumer_scope'] is not None or verified['scope']!='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION' or verified['phase']!='helper_complete_fresh_verifier_control' or verified['canonical_files_read']!=37445 or verified['logical_owner_requirements']!=238780 or verified['exhaustive_namespaces_checked']!=86 or verified['explicit_aliases_checked']!=186 or verified['declared_absence_inputs_checked_before_and_after_bytes']!=479 or len(verified['coverage'])!=9 or any(verified[k] is not False for k in ('science_qualification_created','live_resources_verified','external_declaration_exit0_verified','live_subprocesses_reexecuted')):raise ValueError('complete current fresh verifier returned scope required')
    del expected,verified
    trace,trace_pin=_gzip_object(support,report['actual_complete_ReadOpenAudit_trace'],OUT/'ACTUAL_COMPLETE_READ_OPEN_TRACE.json.gz')
    if list(trace)!=TRACE_FIELDS or trace['schema']!='AXMAT_READ_OPEN_ATTEMPT_TRACE_V1' or trace['coverage']!='PYTHON_AUDIT_OPEN_ATTEMPTS_ONLY' or trace['subprocess_records']!=[] or type(trace['records']) is not list or len(trace['records'])!=37446:raise ValueError('all actual unfiltered37446 read-open records required')
    paths=[]
    for record in trace['records']:
        if type(record) is not dict or record['event']!='open' or record['kind']!='path' or record['access']!='read' or record['observation']!='OPEN_ATTEMPT' or type(record['attempt_count']) is not int or record['attempt_count']!=1:raise ValueError('every real canonical/graph read-only open attempt must be retained')
        paths.append(record['path'])
    if len(set(paths))!=37446 or paths.count(str(GRAPH_PATH))!=1 or type(trace['unique_records']) is not int or trace['unique_records']!=37446 or type(trace['actual_read_open_attempts']) is not int or trace['actual_read_open_attempts']!=37446 or trace['record_storage']!='EXACT_RECORD_DEDUPLICATION_WITH_ACTUAL_ATTEMPT_COUNTS' or trace['success_of_open_attempt_is_not_observed'] is not True or trace['native_libc_HDF5_loader_and_directory_stat_are_not_traced'] is not True:raise ValueError('full real trace counts/attempts and honest observation scope required')
    if report['actual_complete_trace_counts']!=dict(records=37446,attempts=37446,canonical_files=37445,external_graph_reads=1,no_subprocess_reexecuted=True):raise ValueError('complete reported actual trace counts differ')
    del trace,paths
    if set(p.name for p in OUT.iterdir())!={'ACTUAL_RUN_CLAIM.json','ACTUAL_REPORT.json','private_trace_fixture.txt','EXPECTED_COMPLETE_RETURN_CONTRACT.json.gz','ACTUAL_COMPLETE_VERIFIER_RETURN.json.gz','ACTUAL_COMPLETE_READ_OPEN_TRACE.json.gz'} or any(not stat.S_ISREG(p.lstat().st_mode) or p.is_symlink() for p in OUT.iterdir()):raise ValueError('full exact fresh output namespace required')
    private=report['private_full_inactive_audit_snapshot_controls']
    if any(private[key] is not True for key in ('default_snapshot_full_original_records_unchanged','owned_same_builtin_records_map_completely_cleared','all_other_audit_state_unchanged','all_nine_fields_full_type_order_value_floatbits_and_counts_equal','no_second_graph_or_input_phase_substituted','all37446_actual_reads_from_same_genuine_phase','no_cross_phase_hash_or_stat_cache')) or private['new_helper_qualification_created'] is not False or private['business_or_science_qualification_created'] is not False:raise ValueError('whole private inactive audit consumption and honest complete scope required')
    if private['default_complete_descriptor_type_order_floatbit_pin']!=private['consumed_complete_descriptor_type_order_floatbit_pin'] or private['default_full_trace_gzip']!=report['actual_complete_ReadOpenAudit_trace']:raise ValueError('whole consumed/default descriptor and actual default gzip differ')
    wire=private['complete_consumed_vs_default_wire']
    if any(wire[key] is not True for key in ('every_default_and_consumed_wire_byte_compared','full_gzip_EOF_verified','no_fields_or_records_selected')) or wire['complete_nine_snapshot_fields']!=TRACE_FIELDS or wire['uncompressed_JSON_bytes']!=report['actual_complete_ReadOpenAudit_trace']['uncompressed_JSON_bytes'] or wire['uncompressed_JSON_sha256']!=report['actual_complete_ReadOpenAudit_trace']['uncompressed_JSON_sha256']:raise ValueError('full consumed/default ordered wire+EOF proof required')
    _driver_pin(support,report['private_snapshot_control_Source'],Path(AUDIT_CONTROL_PATH))
    success=report['actual_success_pins']
    if success['helper']!=helper or success['graph']!=graph or success['full_return']!=report['actual_complete_verifier_return'] or success['full_trace']!=report['actual_complete_ReadOpenAudit_trace']:raise ValueError('all full actual success pins required')
    return dict(actual_report=report_pin,actual_claim=support.pin(OUT/'ACTUAL_RUN_CLAIM.json'),actual_host_PID=os.getpid(),actual_child_PID=watch['pid'],actual_claim_parent_and_watch_PID_match=True,complete_expected_return=expected_pin,complete_actual_return=verified_pin,complete_actual_unfiltered_trace=trace_pin,complete_private_controls=True,complete_current_graph_verifier_returned=True,external_Root_closed_terminal_required=True)

def main():
    started=time.monotonic()
    if SOURCE_STATUS!='READY_SOURCE_BOUND_BY_ROOT' or any(type(p) is not dict for p in (BOUND_HELPER_PIN,INSTALL_WITNESS_PIN,SOURCE_INSTALL_RECORD_PIN)) or type(TARGET_SHA) is not str or len(TARGET_SHA)!=64:
        raise ValueError('UNREADY host requires actual Root SOURCE bindings before I/O or guard import')
    if len(sys.argv)!=1 or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or sys.getprofile() is not None:
        raise ValueError('fixed unprofiled nonoptimized read-only admission host required')
    import hashlib
    if hashlib.sha256(SUPPORT.read_bytes()).hexdigest()!=SUPPORT_SHA:
        raise ValueError('fixed normal support source required')
    spec=importlib.util.spec_from_file_location('axmat_v15_normal_readonly_admission_support',SUPPORT)
    support=importlib.util.module_from_spec(spec);sys.modules[spec.name]=support;spec.loader.exec_module(support)
    support_pin=support.pin(SUPPORT,SUPPORT_SHA)
    if any(os.environ.get(k)!='1' for k in support.THREAD_KEYS) or Path(sys.executable).resolve()!=support.PYTHON:
        raise ValueError('original single-thread Python required')
    if os.path.lexists(HOST) or os.path.lexists(OUT):raise ValueError('fresh one-use controls host and output required; no retry')
    source_before=_source_namespace(support)
    if support.pin(BOUND_HELPER_PIN['path'],BOUND_HELPER_PIN['sha256'])!=BOUND_HELPER_PIN or support.pin(INSTALL_WITNESS_PIN['path'],INSTALL_WITNESS_PIN['sha256'])!=INSTALL_WITNESS_PIN or support.pin(SOURCE_INSTALL_RECORD_PIN['path'],SOURCE_INSTALL_RECORD_PIN['sha256'])!=SOURCE_INSTALL_RECORD_PIN:
        raise ValueError('actual installed helper and closed exact-integer SOURCE witness pins changed')
    # Ordinary saved receipts and complete control report are full EOF pinned.
    # Purpose-built protocol fixture symlinks remain in Root's lstat closure;
    # no regular-file Source pin follows or relabels those symlinks here.
    prior_pins=list(PRIOR_ACTUAL_6A_PURE_PROTOCOL_PINS.values())+SUPPORTING_ACTUAL_EVIDENCE_PINS
    if [support.pin(p['path'],p['sha256']) for p in prior_pins]!=prior_pins:
        raise ValueError('actual closed6a protocol/finite observation evidence changed')
    prior_host=_json_object(PRIOR_ACTUAL_6A_PURE_PROTOCOL_PINS['host_result']['path'])
    prior_control=_json_object(PRIOR_ACTUAL_6A_PURE_PROTOCOL_PINS['control_report']['path'])
    prior_tool=_json_object(PRIOR_ACTUAL_6A_PURE_PROTOCOL_PINS['actual_launch_and_closed_tool_returns']['path'])
    prior_closed=_json_object(PRIOR_ACTUAL_6A_PURE_PROTOCOL_PINS['Root_external_closed_binding']['path'])
    if prior_host['status']!='ACTUAL_PURE_GRAPH_PROTOCOL_CONTROLS_EXTERNAL_ROOT_REQUIRED' or prior_host['complete_original_pure_controls_retained'] is not True or any(prior_host[k] is not False for k in ('helper_admission_created','new_Q_created','whole_family_memory_pass','profile_used','supervisor_class_or_MRO_modified','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted')):
        raise ValueError('saved genuine6a pure protocol and honest prior scope required')
    if (prior_host['whole_wall_cap_seconds'],prior_host['stage_wall_cap_seconds'],prior_host['rss_cap_mib'],prior_host['archive_cap_bytes'],prior_host['threads'],prior_host['children_at_once'],prior_host['retries'])!=(60,60,512,64*2**20,1,1,0) or prior_control['status']!='ACTUAL_PURE_HELPER_CONTROLS_PASS_NO_RUNTIME_OR_SCIENCE_ADMISSION' or {k:prior_control['helper'][k] for k in ('path','sha256','identity')}!=BOUND_HELPER_PIN:
        raise ValueError('complete original actual60/60 installed6a pure protocol binding required')
    if prior_tool['initial']['chunk_id']!='68ece3' or type(prior_tool['initial']['session_id']) is not int or prior_tool['initial']['session_id']!=62042 or prior_tool['closed']['chunk_id']!='3a9510' or type(prior_tool['closed']['exit_code']) is not int or prior_tool['closed']['exit_code']!=0:
        raise ValueError('one real Root pure protocol launch/closed0 required')
    prior_terminal=json.loads(prior_tool['closed']['output'],parse_constant=_fail_constant)
    if prior_terminal['status']!=prior_host['status'] or prior_terminal['actual_host_result']!=PRIOR_ACTUAL_6A_PURE_PROTOCOL_PINS['host_result']:
        raise ValueError('actual complete untruncated pure terminal host binding required')
    if prior_closed['schema']!='SPOT_ROOT_ACTUAL_V27_PURE_PROTOCOL_EXTERNAL_CLOSED_BINDING_V1' or prior_closed['status']!='ROOT_BOUND_ACTUAL_PURE_PROTOCOL_PASS_NO_Q_OR_SCIENTIFIC_ADMISSION' or any(prior_closed[k] is not False for k in ('new_Q_created','whole_522_to_512_memory_pass','Native_started','AAA_accuracy_qualified','ABA_admitted')):
        raise ValueError('actual external Root pure closure remains finite evidence only')
    for field,key in (('actual_host_result','host_result'),('actual_control_report','control_report'),('actual_genuine_tool_returns','actual_launch_and_closed_tool_returns')):
        if {k:prior_closed[field][k] for k in ('path','sha256','identity')}!=PRIOR_ACTUAL_6A_PURE_PROTOCOL_PINS[key]:raise ValueError('actual Root closure full ordinary evidence bindings differ')
    # A saved pure control result and the earlier sampled fresh observation
    # never replace this new phase's actual complete graph and canonical reads.
    del prior_host,prior_control,prior_tool,prior_closed,prior_terminal
    inputs=[support.pin(TARGET,TARGET_SHA),support.pin(BOUND_HELPER_PIN['path'],BOUND_HELPER_PIN['sha256']),support.pin(Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py'),'bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6'),support.pin(GRAPH_PATH,GRAPH_SHA),support_pin,support.pin(support.TARGET,support.TARGET_SHA),support.pin(support.OUT/'seal.json',SEAL_SHA),support.pin(support.TERMINAL/'terminal_return.json',TERM_SHA),INSTALL_WITNESS_PIN,SOURCE_INSTALL_RECORD_PIN]+source_before['files']+prior_pins
    helper,hpin=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'axmat_v15_admission_original619')
    resource,rpin=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'axmat_v15_admission_real_resource_module')
    full,production=helper.modules();helper.guard_admission(full)
    if full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,) or Path(full.__file__).resolve()!=support.FULL or Path(production.__file__).resolve()!=support.PARENT:
        raise ValueError('unchanged genuine supervisor required')
    declared_history_roots=(HOST,OUT,support.SOURCE,support.OUT,support.TERMINAL)
    if len(declared_history_roots)!=5 or any(path==support.ART or not path.is_relative_to(support.ART) for path in declared_history_roots):
        raise ValueError('all five declared history roots must remain strict ART descendants')
    roots=resource.history_roots([str(path) for path in declared_history_roots],support.ART)
    resources=resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)
    runner=None
    try:
        before=resources.check()
        if before['artifact_bytes']+ARCHIVE_CAP>=96*2**30 or before['disk_free_bytes']-ARCHIVE_CAP<8*2**30:
            raise ValueError('complete original resource reserve required')
        HOST.mkdir()
        for name in ('runtime','run','COMPLETE_FRESH_VERIFIER'):(HOST/name).mkdir()
        shutil.copy2(support.BOUNDED,HOST/'runtime/run_bounded_dragon.py')
        remaining=WHOLE_CAP-(time.monotonic()-started)
        if remaining<=0:raise ValueError('whole admission budget exhausted')
        runner=full.OwnRSSSerialExecutor(HOST,remaining,'COMPLETE_FRESH_VERIFIER',resources)
        if type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources:raise ValueError('genuine runner binding required')
        command=[str(support.PYTHON),'-B',str(TARGET),'--output-dir',str(OUT),'--driver-sha256',TARGET_SHA]
        runner.execute(HOST/'run','admit',command,STAGE_CAP)
        log=HOST/'run/admit.log';watch_path=HOST/'run/admit.watchdog.json'
        admission=_json_object(log);watch=_json_object(watch_path)
        control_report=_json_object(OUT/'ACTUAL_REPORT.json')
        actual_full_controls=_full_controls(support,control_report,admission,watch,command)
        report_pin=actual_full_controls['actual_report']
        if len(runner.records)!=1 or runner.records[0]['status']!='PASS' or type(watch['returncode']) is not int or watch['returncode']!=0 or watch['command']!=command or watch['limit_failure'] is not None or watch['own_child_only'] is not True or watch['liveness_group_cleanup'] is not True or not 0<=watch['sampled_peak_rss_mib']<RSS_CAP:
            raise ValueError('one genuine bounded read-only child PASS required')
        if type(watch['pid']) is not int or watch['pid']<=0 or watch['rss_cap_mib']!=RSS_CAP or not _finite_number(watch['sampled_peak_rss_mib'],0,RSS_CAP) or not _finite_number(watch['elapsed_seconds'],0,STAGE_CAP) or not _finite_number(watch['wall_cap_seconds'],0,STAGE_CAP+1) or not 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=runner.records[0]['wall_cap_seconds']<=STAGE_CAP:
            raise ValueError('actual genuine600-second watched child contract differs')
        source_after=_source_namespace(support)
        if source_after!=source_before:raise ValueError('complete SOURCE directories/files/SHA7identity changed')
        after=resources.check();elapsed=time.monotonic()-started;archived=support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE,RECEIPTS))
        if not elapsed<WHOLE_CAP or not archived<ARCHIVE_CAP:raise ValueError('unchanged admission host caps exceeded')
        for entry in inputs+[hpin,rpin]:
            if support.pin(entry['path'],entry['sha256'])!=entry:raise ValueError('normal complete pinned inputs changed')
        value=dict(schema='AXMAT_V28_GENUINE_COMPLETE_SHORT_INDEX_STABLE_WIRE_SORT_PRIVATE_INACTIVE_AUDIT_CURRENT_GRAPH_HOST_V1',prior_actual_6a_pure_protocol_closed_pins=PRIOR_ACTUAL_6A_PURE_PROTOCOL_PINS,supporting_finite_actual_evidence_pins=SUPPORTING_ACTUAL_EVIDENCE_PINS,new_Q_created=False,whole_522_to_512_memory_pass=False,status='ACTUAL_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_EXTERNAL_ROOT_REQUIRED',actual_full_controls=actual_full_controls,source_namespace_before=source_before,source_namespace_after=source_after,installed_helper=BOUND_HELPER_PIN,actual_closed_SOURCE_install_witness=INSTALL_WITNESS_PIN,source_install_record=SOURCE_INSTALL_RECORD_PIN,actual_host_PID=os.getpid(),helper_metadata_qualified=False,whole_business_INPUT_qualified=False,physical_balance_qualified=False,UNKNOWN_Q=None,UNKNOWN_BUSINESS_PINS=None,input_sources=inputs,original_helper=hpin,resource_factory=rpin,actual_canonical_command=command,actual_control_report=report_pin,actual_merged_child_stdout_stderr=support.pin(log),independent_child_stdout_captured=False,independent_child_stderr_captured=False,actual_watchdog=support.pin(watch_path),watchdog=watch,stage_records=runner.records,resources_before=before,resources_after=after,whole_seconds=elapsed,archive_before_result_bytes=archived,whole_wall_cap_seconds=WHOLE_CAP,stage_wall_cap_seconds=STAGE_CAP,rss_cap_mib=RSS_CAP,archive_cap_bytes=ARCHIVE_CAP,threads=1,children_at_once=1,retries=0,profile_used=False,supervisor_class_or_MRO_modified=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
        support.write_new(HOST/'result.json',value)
        if support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE,RECEIPTS))>=ARCHIVE_CAP or time.monotonic()-started>=WHOLE_CAP:raise ValueError('final admission host caps exceeded')
        print(json.dumps(dict(status=value['status'],actual_host_result=support.pin(HOST/'result.json'),actual_merged_child_stdout_stderr=support.pin(log),independent_child_stdout_captured=False,independent_child_stderr_captured=False,actual_external_Root_terminal_required=True),allow_nan=False),flush=True)
    except BaseException as error:
        if HOST.is_dir():support.write_new(HOST/'failed_host_result.json',dict(status='FAILED_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_NO_RETRY',error=repr(error),stage_records=[] if runner is None else runner.records,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False))
        raise

if __name__=='__main__':main()
