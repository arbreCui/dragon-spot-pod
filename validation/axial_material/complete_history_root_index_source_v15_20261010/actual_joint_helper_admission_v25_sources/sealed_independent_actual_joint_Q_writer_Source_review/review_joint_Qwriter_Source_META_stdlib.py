"""Independent finite Source/META review. Never imports or executes the writer.

Reads the reviewed 32 KiB Source and the explicit saved small JSON metadata.
Large graph/trace/SQLite/material/transport payloads and compressed archives are
not opened. Their already independent saved evidence is checked by immutable
metadata bindings, while the future writer's whole-byte verification is read
as Source. This review creates no helper, build, INPUT, native, or science Q.
"""
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import struct

P = Path(__file__).parent
SOURCE = Path('/private/tmp/spot_write_actual_v25_joint_inactive_audit_helper_Q_ROOT.py')
EXPECTED = '82a13aca3646491213a787c08ac9d611944f982943f34e4cbc18ec2695c84b71'
B = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
A = Path('/Users/wen/spot/validation/artifacts')
checks = []
input_pins = {}

def check(label, value, evidence=None):
    if type(value) is not bool or value is not True:
        raise ValueError(label)
    if any(r['check'] == label for r in checks):
        raise ValueError('duplicate review label')
    row = dict(check=label, passed=value)
    if evidence is not None:
        row['evidence'] = evidence
    checks.append(row)

def ident(p):
    s = p.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def small_pin(p):
    p = Path(p)
    before = ident(p)
    if not stat.S_ISREG(before[2]) or before[4] > 4 * 2**20:
        raise ValueError('review only regular Source or explicit small META')
    data = p.read_bytes()
    if ident(p) != before:
        raise ValueError('review input changed')
    return dict(path=str(p), sha256=hashlib.sha256(data).hexdigest(), size_bytes=len(data), identity=before), data

def pairs(rows):
    result = {}
    for k, v in rows:
        if k in result:
            raise ValueError('duplicate JSON key')
        result[k] = v
    return result

def read(p, expected=None):
    pin, data = small_pin(p)
    if expected is not None and pin['sha256'] != expected:
        raise ValueError('explicit saved META SHA mismatch: ' + str(p))
    d = json.loads(data, object_pairs_hook=pairs, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    if small_pin(p)[0] != pin:
        raise ValueError('JSON read changed file')
    input_pins[str(p)] = pin
    return d

def pinshape(v, allow_missing_size=False):
    return (type(v) is dict and type(v.get('path')) is str and type(v.get('sha256')) is str
            and len(v['sha256']) == 64 and all(c in '0123456789abcdef' for c in v['sha256'])
            and ((allow_missing_size and 'size_bytes' not in v) or (type(v.get('size_bytes')) is int and v['size_bytes'] >= 0))
            and type(v.get('identity', v.get('identity7'))) is list
            and len(v.get('identity', v.get('identity7'))) == 7
            and all(type(x) is int for x in v.get('identity', v.get('identity7')))
            and ('size_bytes' not in v or v.get('identity', v.get('identity7'))[4] == v['size_bytes']))

def normalized_pin_shape_only(v):
    """Matches future verify's four-field output using saved metadata only.

Does not read or hash the referenced payload. Real future verify obtains this
size from the actual file's fresh lstat; this review only checks its contract.
"""
    return dict(path=v['path'],sha256=v['sha256'],identity=v.get('identity',v.get('identity7')),size_bytes=v.get('identity',v.get('identity7'))[4])

def exact(a, b, ordered=True):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return (list(a) == list(b) if ordered else set(a) == set(b)) and all(exact(a[k], b[k], ordered) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(exact(x, y, ordered) for x, y in zip(a, b))
    if type(a) is float:
        return math.isfinite(a) and math.isfinite(b) and struct.pack('>d', a) == struct.pack('>d', b)
    return a == b

source_pin, raw = small_pin(SOURCE)
text = raw.decode('utf-8')
tree = ast.parse(raw)
input_pins[str(SOURCE)] = source_pin
check('01_complete_current_writer_Source_EOF_SHA_AST', source_pin['sha256'] == EXPECTED)
imports = {n.names[0].name for n in tree.body if isinstance(n, ast.Import)} | {n.module for n in tree.body if isinstance(n, ast.ImportFrom)}
check('02_only_standard_library_imports_no_project_load_or_execution', imports == {'argparse','gzip','hashlib','json','math','os','stat','struct','sys','tarfile','pathlib'} and not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in {'exec','eval','compile','__import__'} for n in ast.walk(tree)))
defs = {n.name:n for n in tree.body if isinstance(n, ast.FunctionDef)}
check('03_all_original_writer_functions_present', set(defs) == {'check','identity','pin','verify','pairs','nonfinite','read','exact','closed0','archive','retention','owner_controls','family','main'})
calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'check']
check('04_all_78_check_predicates_are_boolean_source_expressions', len(calls) == 78 and all(isinstance(n.args[0], (ast.Compare, ast.BoolOp, ast.UnaryOp)) or (isinstance(n.args[0], ast.Call) and isinstance(n.args[0].func, ast.Name) and n.args[0].func.id in {'exact','all'}) for n in calls))
check('05_exact_bool_gate_and_no_list_or_dict_truthiness_as_direct_check', 'if type(value) is not bool or not value:' in text)
check('06_current_view_files_list_and_directories_dict_contract', "for item in view['files']: verify(item)" in text and "for item in view['files']}" in text and "view['files'].values()" not in text and "view['directories'].items()" in text)
check('07_duplicate_key_nonfinite_JSON_rejected_and_exact_recursive_float64_bits', all(s in text for s in ["object_pairs_hook=pairs, parse_constant=nonfinite", "if type(a) is not type(b): return False", "struct.pack('>d', a) == struct.pack('>d', b)"]))
check('08_strict_exit_integer0_closed_noSession_and_real_chunk', "type(value['exit_code']) is int" in text and "'session_id' not in value" in text and "value['chunk_id'] == chunk" in text and "t['closed'] is True" in text and "t['actual_tool_terminal_return_observed'] is True" in text)
check('09_Source_and_saved_META_before_after_complete_EOF_SHA_identity', 'while data := f.read(1024 * 1024): h.update(data)' in text and "check(pin(item['path']) == item" in text and 'INPUTS' in text)
check('10_whole_tar_gzip_Source_bytes_members_dirs_EOF_CRC_not_extract_execute', all(s in text for s in ["'r|gz'",'member.isdir()', 'member.isfile()',"member.name.startswith('/')", "'..' not in Path(member.name).parts",'seen == set(files) and seen_dirs == dirs',"with gzip.open(entry['compressed_archive']['path'], 'rb') as f:","while f.read(1024 * 1024): pass"]) and '.extractall(' not in text)
check('11_original_HOD_exact_files_dirs_and_literal_fixture_aliases', all(s in text for s in ["if name != 'E':", "actual_files == expected_files", "actual_dirs == set(view['directories'])", "os.readlink(p) == item['symlink_target_text']", "verify(item['actual_resolved_target_full_EOF_pin'])"]))
check('12_E_append_honestly_not_claimed_frozen_after_saved_peer_append', "if name != 'E':" in text)
check('13_source_pin_CLI_fresh_exclusive_Q_and_fsync_only_final_write', "parser.add_argument('--source-sha256', required=True)" in text and "check(not Q.exists(), 'fresh Q only')" in text and "with Q.open('x')" in text and 'os.fsync(f.fileno())' in text)
check('14_new_helper_scope_and_no_canonical_or_whole_science_credit', 'AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_INACTIVE_AUDIT_HELPER_ACTUAL_JOINT_ADMISSION_V25' in text and 'QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V25' in text and 'NO_WHOLE_INPUT_BUILD_NATIVE_OR_SCIENCE' in text and "**{k:False for k in FALSE_KEYS}" in text)
check('15_Source_couples_all_four_summary_receipts', all("verify(s['"+k+"'])" in text for k in ['namespace_manifest','actual_prelaunch','Root_actual_bundle','Source_postclose_writer']))
check('16_peer_full_copy_original_saved_fullpins_and_actual_seals_preserved', all(s in text for s in ["d['complete_original_members'].values()", "verify(v['original']); verify(v['saved'])", "('original_actual_peer_seal_receipt', 'saved_actual_peer_seal_receipt')"]))
snapshot_fields = ast.literal_eval(next(n.value for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SNAPSHOT_FIELDS' for t in n.targets)))
fresh_fields = ast.literal_eval(next(n.value for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FRESH_FIELDS' for t in n.targets)))
seeds = ast.literal_eval(next(n.value for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SEEDS' for t in n.targets)))
check('17_whole_nine_snapshot_and_27_fresh_fields_retained_in_order', len(snapshot_fields)==9 and len(fresh_fields)==27 and len(set(snapshot_fields))==9 and len(set(fresh_fields))==27)
check('18_original_caps_Source_60_60_and_1800_600_512_64MiB_96GiB_8GiB_1_1_0', all(s in text for s in ["(60, 60) if kind == 'pure' else (1800, 600)","64 * 2**20","96 * 2**30","8 * 2**30","host['threads'] == host['children_at_once'] == 1","host['retries'] == 0"]))
families = {}
for kind, seed in seeds.items():
    base, art, summary_sha, ns_sha, peer_sha, rt_sha, chunk, peer_chunk = seed
    e=B/(base+'_receipts'); h=A/(art+'-host-v25-20261010'); o=A/(art+'-v25-20261010')
    summary = read(e/'Root_actual_complete_qualification_postclose_summary.json', summary_sha)
    ns = read(e/'Root_actual_complete_qualification_postclose_namespace_manifest.json', ns_sha)
    host = read(h/'result.json'); report = read(o/'ACTUAL_REPORT.json')
    freeze = read(e/'Root_final_complete_qualification_SOURCE_freeze.json')
    saved = e/('sealed_independent_actual_complete_v25_'+kind+'_saved_Source_META_review')
    peer = read(saved/'REVIEW.json', peer_sha)
    retention = read(e/('Root_actual_complete_v25_'+kind+'_saved_Source_META_peer_retention_record.json'), rt_sha)
    terminal = read(summary['actual_terminal_receipt']['path'])
    seal = read(retention['saved_actual_peer_seal_receipt']['path'])
    bundle = read(summary['Root_actual_bundle']['path']); prelaunch = read(summary['actual_prelaunch']['path'])
    prefix=kind+'_'
    check(prefix+'19_all_current_small_Metadata_schemas_and_family_match', summary['schema']=='ROOT_V25_ACTUAL_COMPLETE_HELPER_QUALIFICATION_POSTCLOSE_SUMMARY_V1' and summary['kind']==kind and ns['schema']=='ROOT_V25_ACTUAL_COMPLETE_HELPER_QUALIFICATION_POSTCLOSE_FULL_EOF_NAMESPACE_V1' and ns['kind']==kind and freeze['schema']=='ROOT_V25_COMPLETE_PRIVATE_INACTIVE_AUDIT_QUALIFICATION_SOURCE_FREEZE_V1' and freeze['kind']==kind and retention['schema']=='ROOT_COMPLETE_FINITE_SOURCE_REVIEW_PACKAGE_RETENTION_V1' and prelaunch['schema']=='ROOT_V25_ACTUAL_COMPLETE_HELPER_QUALIFICATION_PRELAUNCH_V1' and bundle['schema']=='ROOT_V25_ACTUAL_COMPLETE_QUALIFICATION_CLOSED_TOOL_BUNDLE_V1')
    check(prefix+'20_actual_Root_terminal_strict0closed_and_bound_exact_chunk', terminal['schema']=='ROOT_V25_ACTUAL_COMPLETE_HELPER_QUALIFICATION_TOOL_TERMINAL_RETURN_V1' and terminal['closed'] is True and terminal['actual_tool_terminal_return_observed'] is True and type(terminal['terminal_tool_return']['exit_code']) is int and terminal['terminal_tool_return']['exit_code']==0 and 'session_id' not in terminal['terminal_tool_return'] and terminal['terminal_tool_return']['chunk_id']==chunk and summary['actual_terminal_chunk_id']==chunk and summary['actual_complete_control_success'] is True and summary['actual_failure'] is None)
    check(prefix+'21_all_HODE_file_rows_lists_all_pin_types_and_directories_dicts', set(ns['views'])=={'H','O','D','E'} and all(type(v['files']) is list and all(pinshape(x) for x in v['files']) and type(v['directories']) is dict and all(type(x) is list and len(x)==7 and all(type(i)is int for i in x) for x in v['directories'].values()) for v in ns['views'].values()))
    links = ns['views']['O'].get('original_fixture_symlinks',[])
    check(prefix+'22_all_literal_symlink_rows_exact_typed_link_and_target_pins', type(links)is list and len(links)==(2 if kind=='pure' else 0) and all(type(x['path']) is str and type(x['symlink_target_text'])is str and len(x['identity'])==7 and all(type(i)is int for i in x['identity']) and pinshape(x['actual_resolved_target_full_EOF_pin']) for x in links))
    check(prefix+'23_original_D9_or10_full_Source_rows_and_all_summary_pins', len(ns['views']['D']['files'])==(9 if kind=='pure' else 10) and all(pinshape(summary[x])for x in ['actual_terminal_receipt','namespace_manifest','actual_prelaunch','Root_actual_bundle','Source_postclose_writer']))
    archives=freeze['lossless_complete_Source_archives']
    check(prefix+'24_all_184_and199_whole_archive_metadata_member_shapes', type(archives)is dict and [len(x['full_decompressed_members'])for x in archives.values()]==[184,199] and all(type(x['full_decompressed_members'])is dict and type(x['full_decompressed_directories'])is list and len(x['full_decompressed_members'])==x['complete_file_count_including_manifest'] and len(x['full_decompressed_directories'])==x['complete_directory_count_including_root'] and pinshape(x['compressed_archive']) and all(type(v['size_bytes'])is int and type(v['sha256'])is str and len(v['sha256'])==64 for v in x['full_decompressed_members'].values()) and x['all_member_bytes_and_SHA_verified_after_decompression']is True and x['no_original_member_omission']is True and x['runtime_Source_entrypoints_are_separate_original_bytes']is True for x in archives.values()))
    check(prefix+'25_all_original_Q_helper_canonical_pin_rows_remain_saved', type(freeze['original_helper_Q_canonical_fullEOF_unchanged'])is list and all(pinshape(x)for x in freeze['original_helper_Q_canonical_fullEOF_unchanged']) and freeze['actual_installed_helper']['sha256']=='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092')
    check(prefix+'26_all_retention_members_original_saved_exact_metadata_copies', type(retention['complete_original_members'])is dict and len(retention['complete_original_members'])==retention['complete_original_member_count'] and all(pinshape(x['original'])and pinshape(x['saved'])and x['original']['sha256']==x['saved']['sha256']and x['original']['size_bytes']==x['saved']['size_bytes']for x in retention['complete_original_members'].values()) and retention['source_only']is True and retention['new_qualification_created']is False and retention['helper_guard_business_executed']is False)
    st=seal.get('terminal_tool_return',seal.get('exec_command_result',seal.get('actual_tool_return')))
    check(prefix+'27_genuine_actual_peer_seal_keys_strict0closed_observed', seal['closed']is True and type(st['exit_code'])is int and st['exit_code']==0 and 'session_id'not in st and (seal.get('actual_tool_terminal_return_observed')is True or seal.get('actual_observed_terminal')is True) and pinshape(retention['original_actual_peer_seal_receipt'])and pinshape(retention['saved_actual_peer_seal_receipt']))
    expected_count=55 if kind=='pure' else 42
    check(prefix+'28_genuine_complete_55_or42_saved_peer_typed_checks_scope', peer['schema']=='INDEPENDENT_V25_ACTUAL_SUCCESS_PRIVATE_INACTIVE_AUDIT_'+kind.upper()+'_SAVED_SOURCE_META_REVIEW_V1' and peer['source_only']is True and peer['all_checks_typed_true']is True and peer['blockers']==[] and type(peer['check_count'])is int and peer['check_count']==len(peer['checks'])==expected_count and all(type(x['passed'])is bool and x['passed']is True for x in peer['checks'])and peer['new_actual_helper_qualification']is None)
    tool=read(saved/('ACTUAL_INDEPENDENT_SOURCE_META_INSPECTION_AND_REVIEW_TOOL_RETURNS.json'if kind=='pure'else'ACTUAL_SAVED_SOURCE_META_REVIEW_TOOL_RETURN.json'))
    tr=next(x['actual_tool_return']for x in tool['records']if x['key']=='v25_actual_complete_pure_saved_Source_META_review_attempt1')if kind=='pure'else tool['terminal_tool_return']
    check(prefix+'29_genuine_peer_review_terminal_source_chunk_strict0', type(tr['exit_code'])is int and tr['exit_code']==0 and 'session_id'not in tr and tr['chunk_id']==peer_chunk)
    w=host['watchdog']; whole,stage=(60,60)if kind=='pure'else(1800,600)
    check(prefix+'30_genuine_host_watch_caps_measurements_and_no_MRO_override', type(w['returncode'])is int and w['returncode']==0 and w['own_child_only']is True and w['liveness_group_cleanup']is True and w['limit_failure']is None and host['supervisor_class_or_MRO_modified']is False and host['profile_used']is False and host['whole_wall_cap_seconds']==whole and host['stage_wall_cap_seconds']==stage and host['rss_cap_mib']==512 and host['archive_cap_bytes']==64*2**20 and host['threads']==host['children_at_once']==1 and host['retries']==0 and summary['whole_host_seconds']==host['whole_seconds']<whole and summary['actual_child_seconds']==w['elapsed_seconds']<stage and summary['actual_own_child_sampled_peak_RSS_MiB']==w['sampled_peak_rss_mib']<512)
    check(prefix+'31_actual_history_free_space_and_original_archive_cap', all(x['artifact_budget_bytes']==96*2**30 and x['min_free_bytes']==8*2**30 and x['artifact_bytes']<96*2**30 and x['disk_free_bytes']>=8*2**30 for x in [host['resources_before'],host['resources_after']]) and summary['original_normal_archive_under_cap']is True and summary['normal_HOD_bytes']<64*2**20 and summary['complete_HODE_bytes']<64*2**20)
    check(prefix+'32_all_host_input_and_runtime_support_optional_size_pin_shapes', type(host['input_sources'])is list and all(pinshape(x,True)for x in host['input_sources']) and all(pinshape(host[x],True)for x in ['original_helper','resource_factory','actual_watchdog','actual_control_report']))
    check(prefix+'33_scope_stays_no_new_Q_INPUT_build_native_or_science', summary['new_actual_helper_qualification']is None and summary['whole_INPUT_admitted']is False and summary['actual_complete_build_qualified']is False and summary['AAA_accuracy_qualified']is False and summary['ABA_admitted']is False)
    families[kind]=dict(report=report,peer=peer,summary=summary,namespace=ns,freeze=freeze)

install=read(B/'actual_complete_graph_helper_controls_v23_receipts/Root_actual_complete_helper_SOURCE_install_record.json','079d4dfec16d0df86459abc2fc9238f7aabade38fca8c7adc0659a50f37dc5cf')
it=read(B/'actual_complete_graph_helper_controls_v23_receipts/Root_actual_complete_helper_SOURCE_install_tool_return.json','a305a84b712276aecadd5ebc7fced99d0d58b68a061e228747f0ccfbeed63c12')
pure=families['pure']['report'];fresh=families['fresh']['report']
check('34_true_V23_Source_install_schemas_helper_chain_strict0_not_qualification', install['schema']=='ROOT_V23_COMPLETE_HELPER_SOURCE_INSTALL_RECORD_V1'and it['schema']=='ROOT_V23_ACTUAL_COMPLETE_HELPER_SOURCE_INSTALL_TOOL_RETURN_V1'and it['source_only']is True and it['closed']is True and it['actual_tool_terminal_return_observed']is True and type(it['terminal_tool_return']['exit_code'])is int and it['terminal_tool_return']['exit_code']==0 and it['terminal_tool_return']['chunk_id']=='10a0e4'and it['new_Q']is None and exact(install['installed_helper'],it['installed_helper'])and pinshape(install['installed_helper'],True)and install['installed_helper']['sha256']=='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'and normalized_pin_shape_only(install['installed_helper'])['size_bytes']==150986)
check('35_both_real_families_have_exact_same_installed_helper_fourfield_pin', pinshape(pure['helper'],True)and pure['helper']['source_bytes']==150986 and exact(normalized_pin_shape_only(pure['helper']),normalized_pin_shape_only(install['installed_helper']))and exact(normalized_pin_shape_only(fresh['actual_success_pins']['helper']),normalized_pin_shape_only(install['installed_helper'])))
fixture=read(A/'axial-material-complete-graph-inactive-audit-helper-controls-v25-20261010/small_fixture_controls.json');small=read(A/'axial-material-complete-graph-inactive-audit-helper-controls-v25-20261010/small_codec_and_rejection_controls.json')
check('36_original_five_stages_fixture37_reject18_arguments_codec61', pure['status']=='ACTUAL_PURE_HELPER_CONTROLS_PASS_NO_RUNTIME_OR_SCIENCE_ADMISSION'and len(pure['stages'])==5 and fixture['producer_full_exact_values_types_order_floatbits']is True and fixture['caller_full_value_and_mutable_identity_preserved']is True and len(fixture['rejections'])==37 and len(fixture['complete_rejected_arguments'])==18 and small['all_default_inputs_unmodified']is True and small['all_lossless_missing_null_order_type_floatbit_duplicate_controls']is True and small['ordinary_and_both_storage_strict_dispatches']is True and len(small['rejections'])==pure['small_codecs']['rejections']==61)
old=pure['full_old_saved_graph'];meta=old['complete_original_metadata'];trace=pure['full_new_creation_trace']
check('37_original_complete_graph_and_new63379_trace_full_scope', exact(meta,old['normal_strict_file_entrance_full_semantics_and_counts'])and exact(meta,old['normal_strict_payload_entrance_full_semantics_and_counts'])and meta['complete_counts']['canonical_files']==36776 and meta['complete_counts']['requirements']==237767 and meta['complete_counts']['read_trace_records']==62332 and trace['full_record_count']==63379 and trace['actual_attempt_count']==175886 and trace['exact_full_roundtrip']is True and trace['persisted_full_trace_exact_order_type_floatbit_inverse']is True and trace['default_source_nonmutation']is True)
oc=pure['private_owner_consume_controls']
check('38_original_owner4positive3reject2subtypes2invalid_second', [len(oc[k])for k in ['positive_controls','private_guard_rejections','accepted_str_subclass_equivalence_controls','partial_invalid_second_owner_rejections']]==[4,3,2,2]and oc['schema']=='AXMAT_V22_PRIVATE_OWNER_CONSUME_ACTUAL_CONTROL_V1'and all(exact(x['expected_complete_descriptor_signature'],x['actual_complete_descriptor_signature'])and x['full_normalized_descriptor_types_order_values_attrs_floatbits_equal_default']is True for x in oc['positive_controls']))
snap=read(pure['private_inactive_audit_snapshot_controls_order_preserved_artifact']['path'])
check('39_ordered_artifact_vs_sorted_aggregate_only_semantic_matching', exact(snap,pure['private_inactive_audit_snapshot_controls'],False)and not exact(snap,pure['private_inactive_audit_snapshot_controls'],True)and snap['schema']=='PRIVATE_INACTIVE_READ_OPEN_AUDIT_COMPLETE_SNAPSHOT_CONTROLS_V1')
check('40_all5positive13reject3lastuse_complete_new_snapshot_controls', [len(snap[k])for k in ['positive_controls','private_guard_rejections','last_use_failure_controls']]==[5,13,3]and all(x['default_and_explicitFalse_complete_state_unchanged']is True and x['all_nine_fields_nested_types_order_values_attrs_floatbits_equal_default']is True for x in snap['positive_controls'])and all(x['rejected']is True and x['class_name']=='InputGraphError'and x['complete_audit_state_identity_type_order_value_bits_unchanged']is True for x in snap['private_guard_rejections']))
check('41_all_five_positive_full_ordered_nine_field_type_value_floatbits', all(list(x['actual_full_expected_snapshot'])==snapshot_fields and exact(x['actual_full_expected_snapshot'],x['actual_full_consumed_snapshot']if i<3 else x['actual_full_default_snapshot'])for i,x in enumerate(snap['positive_controls'])))
check('42_nontransactional_clone_failure_after_clear_preserved', [x['case']for x in snap['last_use_failure_controls']]==['invalid_second_row_before_clear','missing_attempt_count_before_clear','nonfinite_clone_after_clear']and all(x['original_error_class_and_message_retained']is True and x['no_transactional_private_mode_promise']is True and x['both_callers_unchanged_before_clear_or_default']is(i<2)and x['private_clone_failure_after_clear_consumption_observed']is(i==2)for i,x in enumerate(snap['last_use_failure_controls'])))
check('43_same_genuine_single_Popen_observation_retained_no_normalization', snap['actual_child_returncode']==0 and snap['actual_same_observation_full_record_role_comparison']is True and snap['no_cross_process_PID_FD_inode_normalization']is True and list(snap['actual_single_Popen_observation'])==snapshot_fields and snap['native_or_numeric_component_executed']is False and snap['helper_qualification_created']is False)
check('44_original13_full_protocol_Q_fields_Source_complete', len(next(n for n in ast.walk(defs['main'])if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='full_protocol'for t in n.targets)).value.keywords)==13 and "check(len(full_protocol) == 13"in text)
check('45_fresh_full27fields_37112_reads_original4positive3reject', fresh['complete_return_fields_retained']==fresh_fields and exact(fresh['actual_complete_trace_counts'],dict(records=37112,attempts=37112,canonical_files=37111,external_graph_reads=1,no_subprocess_reexecuted=True))and len(fresh['private_trace_controls']['positive_controls'])==4 and len(fresh['private_trace_controls']['rejections'])==3 and fresh['complete_expected_coverage_tracecoverage_scope_snapshot_and_counts_equal']is True)
fc=fresh['private_full_inactive_audit_snapshot_controls']
check('46_fresh_same_phase_full779371_nodes_and_nine_fields21411449_bytes', exact(fc['default_complete_descriptor_type_order_floatbit_pin'],fc['consumed_complete_descriptor_type_order_floatbit_pin'])and fc['default_complete_descriptor_type_order_floatbit_pin']['complete_node_count']==779371 and fc['complete_consumed_vs_default_wire']['complete_nine_snapshot_fields']==snapshot_fields and fc['complete_consumed_vs_default_wire']['uncompressed_JSON_bytes']==21411449 and fc['complete_consumed_vs_default_wire']['every_default_and_consumed_wire_byte_compared']is True and fc['complete_consumed_vs_default_wire']['full_gzip_EOF_verified']is True and fc['no_second_graph_or_input_phase_substituted']is True and fc['all37112_actual_reads_from_same_genuine_phase']is True and fc['no_cross_phase_hash_or_stat_cache']is True)
check('47_all_three_original_full_gzip_pins_and_saved_EOF_scope_retained', all(pinshape(fresh[k])and fresh[k]['complete_JSON_wire_gzip_decompression_EOF_SHA_verified']is True and fresh[k]['no_fields_or_records_filtered']is True for k in ['expected_complete_return_contract','actual_complete_verifier_return','actual_complete_ReadOpenAudit_trace'])and fresh['expected_complete_return_contract']['sha256']==fresh['actual_complete_verifier_return']['sha256']and fresh['expected_complete_return_contract']['uncompressed_JSON_sha256']==fresh['actual_complete_verifier_return']['uncompressed_JSON_sha256'])
check('48_actual_Q_target_not_yet_created_no_execution_by_reviewer', not (B/'Root_actual_complete_graph_private_inactive_audit_helper_admission_v25.json').exists())
check('49_all_Read_inputs_fresh_before_after_fixed', all(small_pin(path)[0]==v for path,v in input_pins.items()))
copy=P/'REVIEWED_ROOT_V25_JOINT_Qwriter_SOURCE.py'
with copy.open('xb')as f:f.write(raw)
check('50_reviewed_full_Source_copy_byte_AST_exact', small_pin(copy)[1]==raw and ast.dump(ast.parse(copy.read_bytes()),include_attributes=True)==ast.dump(tree,include_attributes=True))
report=dict(schema='INDEPENDENT_ROOT_V25_JOINT_INACTIVE_AUDIT_HELPER_Q_WRITER_SOURCE_REVIEW_V1',status='SOURCE_ONLY_PASS_NO_WRITER_EXECUTION_OR_QUALIFICATION',source_only=True,all_checks_typed_true=True,blockers=[],check_count=len(checks),checks=checks,qualified_Root_writer_Source_pin=source_pin,reviewed_Source_copy_pin=small_pin(copy)[0],explicit_small_Source_META_input_pins=list(input_pins.values()),review_scope='complete current writer Source and finite saved metadata shapes; no writer or other candidate execution',candidate_helper_guard_controller_reader_API_or_numeric_executed=False,large_graph_trace_material_SQLite_or_gzip_payload_read=False,compressed_Source_archive_member_reverification_by_this_reviewer=False,Source_archive_member_reverification_is_required_in_reviewed_future_writer=True,actual_saved_independent_Source_archive_reviews_consumed=dict(pure=55,fresh=42,auxiliary_pure_small_controls=136),qualification_created=False,whole_build_qualified=False,whole_INPUT_admitted=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,prior_checkpoint_correction='The initial 333694 Source still used dict .values() for actual list view.files. Root corrected it before this current complete finite review; initial checkpoint was incomplete and is not a Source PASS.',own_shape_inspection_correction='Actual 679cbe EXIT1 only looked for nested producer view as a top-level function; actual 39c2dc corrected AST traversal. Reviewed writer/candidate/API were never executed.',scope_boundaries=['This is a Source readiness review of the exact 82a13aca writer, not execution or new Q.','Persisted JSON controls do not independently reconstruct live API object identity; original genuine controls and full independent saved peers are preserved.','E root directory identity changes honestly after postclose metadata and peer retention; original members remain bound, E root is not claimed unchanged.','Whole-byte archive, original HODE/runtime input rechecks in the future writer remain Root-only actual metadata execution.'])
with (P/'REVIEW.json').open('x')as f:json.dump(report,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
with (P/'REPORT.txt').open('x')as f:f.write('Independent complete current V25 joint Q writer Source/META review: PASS_SOURCE_ONLY\n'+str(len(checks))+' finite unique typed-boolean aggregate checks; no hard Source blocker found for the fixed current bytes.\nWriter SHA '+EXPECTED+'; '+str(len(raw))+' bytes.\nNo writer/helper/guard/API/numeric execution, no new qualification.\nOriginal13 protocol fields, owner4/3/2/2, snapshot5/13/3 with nontransactional clone failure, fresh27/37112/4+3/full9 same-phase wire and exact real CLOSED0/save peers remain.\nOriginal caps and 184/199 logical Source scope, D9/10, all original HODE pins and two literal fixture aliases remain.\nOld333 checkpoint lacked full file-list shape; Root corrected .values before this exact current review. Own nested-view inspection EXIT1 and its corrected EXIT0 are honestly retained in actual tool records.\nLarge graph/trace/material/DB/gzip payloads not opened; Source-archive and original whole-byte rechecks remain necessary Root-only metadata execution.\n')
print(json.dumps(dict(status=report['status'],source_only=True,check_count=len(checks),review_pin=small_pin(P/'REVIEW.json')[0],writer_pin=source_pin,all_checks_typed_true=True,candidate_or_writer_or_API_or_numeric_executed=False)))
