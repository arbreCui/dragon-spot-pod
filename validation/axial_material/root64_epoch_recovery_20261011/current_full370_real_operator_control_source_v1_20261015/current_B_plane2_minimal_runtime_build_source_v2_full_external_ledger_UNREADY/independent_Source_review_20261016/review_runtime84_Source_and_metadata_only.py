"""Independent reviewer. Standard-library Source, JSON metadata and lstat only.

Never import the candidate, its helpers, compilers, or any native/scientific reader.
Only named small Source/metadata files receive full-byte reads; compiled inputs,
native files and failed fragments receive current7 checks, never payload reads.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import time

D = Path(__file__).absolute().parent.parent
P = Path(__file__).absolute().parent
START = time.monotonic()
ALLOWED_SYSTEM = []

def need(value, message):
    if value is not True:
        raise RuntimeError(message)

def ids(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def current(p):
    q = Path(p['path'])
    s = q.lstat()
    compiler = str(q) == '/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15' and p.get('sha256') == '0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492' and s.st_nlink == p['identity'][3] == 2
    need(q.is_absolute() and stat.S_ISREG(s.st_mode) and (s.st_nlink == 1 or compiler) and ids(s) == p['identity'] and s.st_size == p['size_bytes'] and not any(x.is_symlink() for x in (q, *q.parents)), 'exact current7 without aliases: ' + str(q))
    need(s.st_uid == os.getuid() or (s.st_uid == 0 and p in ALLOWED_SYSTEM), 'only explicitly frozen original system roles: ' + str(q))
    return q

def full(q):
    q = Path(q)
    s = q.lstat()
    need(s.st_size < 8 * 2**20 and stat.S_ISREG(s.st_mode), 'small named Source/metadata only')
    a = q.read_bytes()
    b = q.read_bytes()
    need(a == b and ids(s) == ids(q.lstat()), 'two stable whole small-file reads')
    p = dict(path=str(q), sha256=hashlib.sha256(a).hexdigest(), size_bytes=len(a), identity=ids(s))
    current(p)
    return p

def meta(p):
    need(Path(p['path']).suffix == '.json', 'only declared JSON metadata')
    need(full(p['path']) == p, 'exact small metadata fullPF')
    return json.loads(Path(p['path']).read_text())

def here(name, sha):
    p = full(D / name)
    need(p['sha256'] == sha, 'Root-supplied frozen artifact SHA: ' + name)
    return p, meta(p)

def genuine(v, key, artifact, output_key, code=0):
    t = v[key]
    need(v['observed_closed'] is True and type(v['original_integer_exit_code']) is int and v['original_integer_exit_code'] == code and type(t['exit_code']) is int and t['exit_code'] == code and t.get('session_id') is None, 'genuine closed typed tool return')
    need(json.loads(t['output'].strip().splitlines()[-1])[output_key] == artifact, 'genuine stdout exact artifact PF')

def unique(rows):
    table = {}
    for p in rows:
        if p['path'] in table:
            need(table[p['path']] == p, 'same role path keeps complete pin')
        table[p['path']] = p
    return table

def scan(root):
    root = Path(root)
    if not root.exists():
        return 0
    total = 0
    for e in os.scandir(root):
        s = e.stat(follow_symlinks=False)
        need(not stat.S_ISLNK(s.st_mode), 'complete owning scope rejects symlinks')
        if stat.S_ISDIR(s.st_mode):
            total += scan(e.path)
        elif stat.S_ISREG(s.st_mode):
            total += s.st_size
    return total

def main():
    global ALLOWED_SYSTEM
    author_pin, author = here('AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json', '66c575ca49945f375ccbf527ddd919706accdfbedfbac46cd71f07f6792f6882')
    ready_pin, ready = here('SOURCE_REVIEW_READY.json', 'edbd8241ee9c28d0d282ad9dad2678fa30c5d4c6536dec2de9b5eb0abe3af4ec')
    gen_pin, gen = here('ROOT_SOURCE_GENERATION_TRUE_TOOL_RETURNS.json', '9c128eb7cea07c9b011634760818da3df37718aea90d1587a67f0f1fc039b1b0')
    genuine(gen, 'actual_terminal_return', ready_pin, 'ready_pin')
    need(gen['actual_retried'] is False and gen['compiler_executed'] is False and gen['native_executed'] is False and gen['Root_pre_read_check_failure_is_not_GEN_or_candidate_execution'] is True, 'one Source GEN0; separate pre-read failure preserved')
    view = meta(ready['control_plan_pin'])
    need(ready['control_plan_pin']['sha256'] == '5720ab0a064bf75321f56d7e77c292145d439d3e98850948acd7ebca79b7540b' and view['admission_packet_pin'] == author['immutable_admission_packet_pin'], 'compact PLAN exact frozen packet dependency')
    packet = meta(view['admission_packet_pin'])
    plan = dict(packet, **view)
    build = meta(plan['original_guard_build_plan_pin'])
    ALLOWED_SYSTEM = build['readonly_system_SDK_header_pins'] + build['readonly_system_tool_metadata_pins'] + [build['C_compiler_pin']]
    sdk = Path(build['readonly_system_SDK_root'])
    need(ids(sdk.lstat()) == build['readonly_system_SDK_root_identity'] and sdk.lstat().st_uid == 0 and not any(x.is_symlink() for x in (sdk, *sdk.parents)), 'original exact SDK directory delegation')
    sources = ready['complete_source_file_pins']
    need(len(sources) == 7 and sources == author['whole_Source_file_pins'] and ready['source_only'] is True and ready['Source_or_compiler_business_executed'] is False, 'exact complete seven Source table')
    source_text = {}
    for p in sources:
        need(full(p['path']) == p, 'all seven frozen Source whole bytes')
        source_text[Path(p['path']).name] = Path(p['path']).read_text()
        if p['path'].endswith('.py'):
            ast.parse(source_text[Path(p['path']).name])
    old = D.parent / 'current_B_plane2_minimal_runtime_build_source_v1_UNREADY'
    insertion = "need(json.loads(a.admission_packet_pin)==author['immutable_admission_packet_pin'],'exact author-frozen immutable admission packet fullPF');"
    for name, text in source_text.items():
        original = (old / name).read_text()
        if name == 'prepare_B_plane2_minimal_runtime_Source.UNREADY.py':
            need(text.count(insertion) == 1 and text.replace(insertion, '', 1) == original, 'GEN only exact packet fullPF equality added')
        else:
            need(text == original, 'other six Sources whole unchanged')
    evidence = meta(author['Source_static_whole_reverse_and_scope_pin'])
    for pair in evidence['all_seven_Source_wholecopy_pairs']:
        need(full(pair['old_pin']['path']) == pair['old_pin'] and full(pair['new_pin']['path']) == pair['new_pin'] and Path(pair['old_pin']['path']).read_bytes() == Path(pair['new_pin']['path']).read_bytes(), 'final ledger sibling wholecopy of all seven prior frozen Sources')
    roots = plan['complete_joint_roots']
    out = Path(plan['planned_actual_output_root'])
    need(len(roots) == len(set(roots)) == 84 and not os.path.lexists(out) and str(out) == roots[-1] and not any(Path(a).is_relative_to(Path(b)) for a in roots for b in roots if a != b), 'fresh sole output84 and whole latest prefix')
    br = meta(plan['epoch_bridge_report_pin'])
    bt = meta(plan['epoch_bridge_Root_tools_pin'])
    bp = meta(plan['epoch_bridge_corrected_post_pin'])
    bpt = meta(plan['epoch_bridge_corrected_post_tools_pin'])
    genuine(bt, 'actual_terminal_return', plan['epoch_bridge_report_pin'], 'report_pin')
    genuine(bpt, 'actual_review_return', plan['epoch_bridge_corrected_post_pin'], 'review_pin')
    need(bp['schema'] == 'A1_A3_FORMAL31_CURRENT_EPOCH_BRIDGE_ACTUAL_METADATA_POSTVERIFY_V1' and bp['status'] == 'PASS_ACTUAL_A1_A3_SELECTED18_FORMAL13_CURRENT_EPOCH_ROOT0_CURRENT7_METADATA_ONLY_NO_COMPATIBILITY_QUALIFICATION' and bp['failure'] is None and bp['actual_Root_integer_exit_code'] == 0 and bp['actual_child_integer_exit_code'] is None and bp['actual_children_started'] == 0, 'genuine corrected selected31 bridge0/post0, no child')
    need('/actual_postverify_corrected_exact_two_formal_metadata_overlap_20261016/' in plan['epoch_bridge_corrected_post_pin']['path'] and bp['actual_bridge_report_pin'] == plan['epoch_bridge_report_pin'] and bp['actual_Root_tools_pin'] == plan['epoch_bridge_Root_tools_pin'] and bp['binding_pin'] == plan['epoch_bridge_binding_pin'] and bp['actual_Source_author_freeze_pin'] == plan['epoch_bridge_author_freeze_pin'], 'only corrected exact two-role metadata overlap result')
    need(br['ordered_role_pairs'] == bp['ordered_role_pairs'] and plan['selected31_current_epoch_readonly_pins'] == [x['current_epoch_full_pin'] for x in bp['ordered_role_pairs']] and bp['actual_selected_role_count'] == 31 and bp['actual_selected_blind_verified_bytes'] == 680089850 and roots == bp['complete_joint_roots'] + [str(out)], 'selected31 complete real byte facts and entire83 to84')
    for k in ('retained_archive_metadata_current7_pins', 'retained_B2_current_epoch_readonly_pins', 'retained_failed_v1_current7_only_pins', 'retained_failed_pool_archive_current7_only_pins', 'exact59_historical_absent_pins'):
        need(plan[k] == bp[k], 'precise latest lifecycle role inheritance: ' + k)
    need(plan['retained_current7_pins'] == bp['retained_all_current7_pins'] and plan['bridge_explicit_cumulative_metadata_file_pins'] == bp['explicit_cumulative_metadata_file_pins'] and len(plan['exact59_historical_absent_pins']) == 59, 'current role table and exact59 unchanged')
    need(bp['historical_independent_genuine_typed0_asserted'] is False and bp['new_B_bearing_context_compatibility_or_lineage_proved'] is False and bp['online_BOOT_qualified'] is False, 'no old independent raw invention or compatibility inheritance')
    op = meta(plan['original_owned70_plan_pin'])
    oh = meta(plan['original_owned70_report_pin'])
    ot = meta(plan['original_owned70_Root_tools_pin'])
    opp = meta(plan['original_owned70_post_pin'])
    opt = meta(plan['original_owned70_post_tools_pin'])
    need(ot['observed_closed'] is True and type(ot['original_integer_exit_code']) is int and ot['original_integer_exit_code'] == 1 and type(ot['actual_terminal_return']['exit_code']) is int and ot['actual_terminal_return']['exit_code'] == 1 and ot['actual_terminal_return'].get('session_id') is None, 'historical Root1 parser failure preserved')
    genuine(opt, 'actual_review_return', plan['original_owned70_post_pin'], 'review_pin')
    need(opp['actual_Root_exit_code'] == 1 and opp['actual_stage_statuses'] == ['PASS'] * 3 and opp['failure'] is None and opp['actual_report_pin'] == plan['original_owned70_report_pin'] and opp['actual_Root_true_tool_return_pin'] == plan['original_owned70_Root_tools_pin'], 'old three stage0 facts independently postverified, no Root0')
    old70 = plan['original_current70_ordered_input_pins']
    need(old70 == op['current_owned_runtime_ordered70_pins'] == opp['actual_ordered70_input_pins'] and [x['path'] for x in old70] == oh['actual_ordered70_link_inputs'] and len(old70) == 70, 'complete actual owned70 authority')
    need(plan['original_current_compile_command'] == oh['records'][0]['command'] and plan['original_current70_link_command'] == oh['records'][1]['command'], 'original exact compile/link commands')
    paths = [x['path'] for x in old70]
    fc = plan['original_Fortran_compiler_pin']['path']
    flags = ['-O2', '-march=native', '-ffp-contract=off', '-fcheck=all', '-fbacktrace', '-g', '-fPIC', '-frecord-marker=4', '-ffixed-line-length-none']
    need(plan['original_current_compile_command'][1:10] == flags and plan['original_current70_link_command'] == [fc, '-O2', '-ffp-contract=off', *paths, '-o', plan['historical_original_Dragon_output_path']], 'same original flags, compiler and ordered full link')
    need(Path(paths[14]).name == 'KDRDRV.o' and Path(paths[66]).name == 'APACKX64.o' and next(i for i, x in enumerate(paths) if x.endswith('.a')) == 58 and sum(x.endswith('.o') for x in paths) == 66 and sum(x.endswith('.a') for x in paths) == 4, 'exact baseline positions and all four archives')
    new = paths[:]
    new[14] = str(out / 'sources/build/KDRDRV.o')
    new[66] = str(out / 'sources/build/APACKX64.o')
    insert = str(out / 'sources/build/B2PLNX64.o')
    ordered71 = new[:58] + [insert] + new[58:]
    inverse = [x for x in ordered71 if x != insert]
    inverse[14], inverse[66] = paths[14], paths[66]
    inc = ['-I' + str(out / 'sources/build')] + plan['original_compile_include_arguments']
    compiles = [[fc, *flags, *inc, '-J' + str(out / 'sources/build'), '-c', str(out / 'sources' / s), '-o', str(out / 'sources/build' / o)] for s, o in [('APACKX64.f90', 'APACKX64.o'), ('B2PLNX64.UNREADY.f90', 'B2PLNX64.o'), ('KDRDRV.F', 'KDRDRV.o')]]
    need(inverse == paths and len(ordered71) == 71 and plan['planned_ordered71_link_inputs'] == ordered71 and plan['exact_four_stage_commands'] == compiles + [[fc, '-O2', '-ffp-contract=off', *ordered71, '-o', str(out / 'sources/runtime/Dragon')]], 'independent exact four command reconstruction and whole71 inverse')
    original_source = D.parent.parent / 'aaa_three_plane_streaming_source_v2'
    apack = source_text['APACKX64.f90']
    need(apack.count("'R64WARM-B-V1 '") == 1 and apack.replace("'R64WARM-B-V1 '", "'R64-A2-WARM1 '", 1) == (original_source / 'APACKX64.f90').read_text(), 'APACK exactly middle case literal, all mathematics unchanged')
    dispatch = "      ELSE IF(HMODUL.EQ.'B2PLNX64:') THEN\n         CALL B2PLNX64(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)\n"
    kdr = source_text['KDRDRV.F']
    need(kdr.count(dispatch) == 1 and kdr.replace(dispatch, '', 1) == (original_source / 'KDRDRV.F').read_text(), 'single new dispatch branch whole inverse')
    caller = source_text['B2PLNX64.UNREADY.f90']
    need(caller == (D.parent / 'current_nativeWarmB2_plane2_online_context_source_v1_UNREADY/B2PLNX64.UNREADY.f90').read_text() and 'integer,parameter::NP=3,NG=370,NS=40' in caller and '\n  p=2\n' in caller and caller.count('call SPOR64_BOOTQ64_BUILD(') == caller.count('call SPOR64_BOOTB64_INGRESS(') == 1 and 'B2PLNX64-STRICT-PLANE2-UNSEALED' in caller, 'whole original B plane2 caller, complete NP3/16 operands, unsealed')
    ledger = unique(plan['explicit_cumulative_metadata_file_pins'])
    history = {x['path'] for x in plan['readonly_history_code_and_selected_native_pins']}
    external = [x for x in plan['compile_and_link_input_pins'] if not any(Path(x['path']).is_relative_to(Path(r)) for r in roots) and x['path'] not in history]
    need(len(plan['compile_and_link_input_pins']) == 178 and len(external) == 69 and sum(x['size_bytes'] for x in external) == 36068911 and external == plan['readonly_project_library_and_compiler_input_pins'] == plan['all69_external_compile_toolchain_full_pins'] and all(ledger[x['path']] == x for x in external), 'all69 external libraries/modules/compiler exact fullPF accounted')
    need(all(x in plan['compile_and_link_input_pins'] for x in plan['all_declared_compile_module_full_pins']) and len(plan['all_declared_compile_module_full_pins']) == 107, 'whole compile module dependencies included')
    for row in plan['original_compile_include_directory_identities']:
        q = Path(row['path'])
        need(ids(q.lstat()) == row['identity'] and stat.S_ISDIR(q.lstat().st_mode) and not any(x.is_symlink() for x in (q, *q.parents)), 'original include directory current7')
    need(sorted(str(q) for row in plan['original_compile_include_directory_identities'] for q in Path(row['path']).glob('*.mod')) == sorted(plan['compile_module_search_directory_file_inventory']), 'whole original module search inventory')
    current_roles = unique(list(ledger.values()) + plan['compile_and_link_input_pins'] + plan['whole_byte_build_source_copy_pins'] + plan['retained_current7_pins'] + plan['retained_archive_metadata_current7_pins'] + plan['retained_B2_current_epoch_readonly_pins'] + plan['selected31_current_epoch_readonly_pins'])
    for p in current_roles.values():
        current(p)
    failed = plan['retained_failed_v1_current7_only_pins'] + plan['retained_failed_pool_archive_current7_only_pins']
    need(len(failed) == 15 and all(set(x) == {'path', 'size_bytes', 'identity'} for x in failed), 'failed8+7 strictly stat-only schema')
    for p in failed:
        current(p)
    for p in plan['exact59_historical_absent_pins']:
        need(not os.path.lexists(p['path']) and not any(x.is_symlink() for x in Path(p['path']).parents), 'exact59 historical absences')
    for k in ('future_actual_new_three_object_pins', 'future_actual_new_Dragon_pin', 'future_actual_build_report_pin', 'future_actual_build_Root_tools_pin', 'future_actual_build_metadata_post_pin', 'future_actual_build_metadata_post_tools_pin', 'actual_new_module_ABI'):
        need(plan[k] is None, 'future actual remains NULL: ' + k)
    caps = dict(whole_seconds=1800, stage_seconds=600, rss_mib=512, fresh_bytes=2*2**30, history_bytes=96*2**30, cold_reserve_bytes=20971764748, metadata_reserve_bytes=64*2**20, free_floor_bytes=8*2**30, threads=1, children_at_once=1, retries=0)
    need(plan['original_caps'] == ready['original_caps'] == author['original_caps'] == caps and view['bounded_new_output_reservation_bytes'] == 32*2**20 and view['bounded_new_Source_metadata_reservation_bytes'] == 8*2**20, 'original full caps and exact32+8 local bounds')
    host = source_text['run_guarded_B_plane2_minimal_runtime_build.UNREADY.py']
    for fragment in ("plan=m.load_plan(sf['control_plan_pin'])", 'full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)', "full.OwnRSSSerialExecutor(m.OUT,1800-(time.monotonic()-start)", 'runner.execute(m.OUT/\'sources/build\',label,cmd,600)', 'host_SELF_peak_bytes=peak', 'Root_same_PID_PS=', 'record[\'label\']', 'len(runner.records)==4 and len(watches)==4', 'hf[\'explicit_cumulative_metadata_file_pins\']', 'host_open_unlinked_bytes=sum(unlinked.values())'):
        need(fragment in host, 'original sole supervisor/resource/watch linkage: ' + fragment)
    need(host.index("with(BASE/'ROOT_EXECUTION_CLAIM_RECEIPT.json').open('x')") < host.index('sf,psf=raw_metadata_argument') < host.index('spec.loader.exec_module(m)'), 'claim before metadata and helper import')
    joint_bytes = sum(scan(r) for r in roots)
    external_bytes = sum(x['size_bytes'] for x in ledger.values() if not any(Path(x['path']).is_relative_to(Path(r)) for r in roots))
    need(joint_bytes + external_bytes + 32*2**20 + 8*2**20 < 2*2**30 and scan(D) + 300000 < 8*2**20, 'current stat-only scope and compact reviewer fit original bounds; runtime original class still mandatory')
    for p in sources:
        need(full(p['path']) == p, 'second final whole Source freeze check')
    report = dict(schema='INDEPENDENT_SOURCE_ONLY_B_PLANE2_MINIMAL_RUNTIME_BUILD_REVIEW_V1', status='PASS_SOURCE_ONLY_B_PLANE2_MINIMAL_RUNTIME_COMPLETE71_BUILD', source_only=True, failure=None, executor_task_name='/root/b2_build_source_peer', control_plan_pin=ready['control_plan_pin'], complete_source_file_pins=sources, author_freeze_pin=author_pin, immutable_admission_packet_pin=view['admission_packet_pin'], ready_pin=ready_pin, actual_Source_GEN_tools_pin=gen_pin, actual_Source_GEN_original_integer_exit_code=0, Source_GEN_pre_read_failure_preserved_separately=True, old_owned70_Root_integer_exit_code=1, old_owned70_actual_stage_statuses=opp['actual_stage_statuses'], old_owned70_report_pin=plan['original_owned70_report_pin'], old_owned70_post_pin=plan['original_owned70_post_pin'], selected31_corrected_post_pin=plan['epoch_bridge_corrected_post_pin'], original_input_count=70, planned_link_input_count=71, preserved_other_original_input_count=68, replaced_original70_indices=[14,66], new_input_before_original70_index=58, planned_compile_count=3, planned_link_count=1, new_explicit_object_count=67, archive_count=4, exact_four_stage_commands=view['exact_four_stage_commands'], complete_joint_roots=roots, original_caps=caps, bounded_output_bytes=32*2**20, bounded_own_Source_bytes=8*2**20, complete_external_compile_toolchain_input_count=69, complete_external_compile_toolchain_input_bytes=36068911, every_external_input_fullPF_in_ledger=True, complete_explicit_ledger_count=len(ledger), current7_role_count=len(current_roles), retained_failed_stat_only_count=15, exact_historical_absent_count=59, whole_seven_Source_freeze_verified_twice=True, compact_PLAN_packet_exact_fullPF_gate_verified=True, APACK_single_case_literal_whole_inverse=True, KDR_single_dispatch_whole_inverse=True, original_plane2_caller_wholebytes=True, original_module_search_inventory_current=True, original_supervisor_and_caps_Source_verified=True, current_stat_only_joint_bytes=joint_bytes, current_exact_explicit_external_bytes=external_bytes, reviewer_performed_original_runtime_resource_class=False, compiler_executed=False, native_executed=False, helper_executed=False, compiled_input_body_read=False, scientific_payload_read=False, candidate_executed=False, B_context_executed=False, GLOBAL_or_PROJECT_produced=False, new_B_formal13_compatible=False, online_BOOT_qualified=False, physics_qualified=False, AAA_qualified=False, ABA_admitted=False, all_transitive_inputs_recertified=False, goal_complete=False, elapsed_review_seconds=time.monotonic()-START)
    q = P / 'REVIEW.json'
    with q.open('x') as f:
        json.dump(report, f, indent=2, allow_nan=False)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
    print(json.dumps(dict(status=report['status'], review_pin=full(q))), flush=True)

if __name__ == '__main__':
    main()
