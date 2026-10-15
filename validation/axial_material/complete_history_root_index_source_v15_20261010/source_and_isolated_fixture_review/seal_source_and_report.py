"""Seal pure source/fixture results only; no business import or new fixtures."""
from pathlib import Path
import ast, hashlib, json

D = Path(__file__).parent
P = Path('/Users/wen/spot/validation/axial_material')
parent = P/'prepare_qualified_AB_moment_order_production.py'

def pin(path):
    path = Path(path)
    before = path.lstat()
    with path.open('rb') as stream: digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    after = path.lstat()
    fields = ['st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns']
    identity = [getattr(before, key) for key in fields]
    assert identity == [getattr(after, key) for key in fields]
    return dict(path=str(path), sha256=digest, size_bytes=before.st_size, identity=identity)

def save(name, data):
    with (D/name).open('x') as stream:
        json.dump(data, stream, indent=2, allow_nan=False); stream.write('\n')

proof = json.loads((D/'source_inverse_proof.json').read_text())
fixtures = json.loads((D/'fixture_results.json').read_text())
assert fixtures['status'] == 'PASS_PURE_FUNCTION_FIXTURES_ONLY' and fixtures['case_count'] == 401
assert pin(parent) == proof['original_source']
old = parent.read_text()
new = old
original_function = (D/'original_validate_history_roots.py.txt').read_text().rstrip('\n')
candidate_text = (D/'validate_history_roots_incremental_trie_candidate.py').read_text()
candidate_node = next(n for n in ast.parse(candidate_text).body if isinstance(n, ast.FunctionDef))
candidate_function = ast.get_source_segment(candidate_text, candidate_node)
assert old.count(original_function) == 1
new = old.replace(original_function, candidate_function, 1)
back = candidate_function
for edit in reversed(proof['edits']):
    assert back.count(edit['new']) == 1
    back = back.replace(edit['new'], edit['old'], 1)
assert back == original_function and new.replace(candidate_function, original_function, 1) == old
full = D/'moment_order_complete_history_resource_trie_20261010.UNREADY.py'
with full.open('x') as stream: stream.write(new)
ot = ast.parse(old); nt = ast.parse(new)
original_segments = [ast.get_source_segment(old,n) for n in ast.walk(ot) if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name!='validate_history_roots']
new_segments = [ast.get_source_segment(new,n) for n in ast.walk(nt) if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name!='validate_history_roots']
assert original_segments == new_segments
chain = [P/'prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14b.py',
         P/'prepare_qualified_AB_rank1_cache_production.py',parent]
source_pins = [pin(p) for p in chain]
cap_scan = old[old.index('class DynamicHistoryResources:'):old.index('\ndef read(path):')]
assert cap_scan == new[new.index('class DynamicHistoryResources:'):new.index('\ndef read(path):')]
assert '96 * 2**30' in cap_scan and '8 * 2**30' in cap_scan
receipt = dict(schema='AXMAT_HISTORY_ROOTS_ISOLATED_FIXTURE_ACTUAL_TOOL_TERMINAL_V1',
    actual_tool_result=dict(chunk_id='d352e9',exit_code=0,session_id=None,session_closed=True,output=''),
    actual_stdout=pin(D/'fixtures.stdout'), actual_stderr=pin(D/'fixtures.stderr'),
    harness=pin(D/'generate_and_compare.py'), source_inverse_proof=pin(D/'source_inverse_proof.json'),
    complete_fixture_result=pin(D/'fixture_results.json'), isolated_function_comparison_only=True,
    canonical_module_imported=False, business_API_called=False, resource_class_instantiated=False,
    project_written=False, performance_native_AAA_ABA_credit=False)
assert receipt['actual_stderr']['size_bytes'] == 0
save('actual_readonly_fixture_tool_return.json',receipt)
report = dict(schema='AXMAT_HISTORY_ROOTS_INCREMENTAL_TRIE_SOURCE_AND_FIXTURE_REVIEW_V1',
    status='PASS_SOURCE_AND_ISOLATED_VALIDATOR_FIXTURES_ONLY', source_status='UNREADY_NOT_INSTALLED',
    function_candidate=pin(D/'validate_history_roots_incremental_trie_candidate.py'),
    complete_module_candidate=pin(full), original_source=pin(parent), source_edits_exactly_two_regions=True,
    inverse_to_full_original_module_exact=True, all_other_41_function_class_segments_byteexact=True,
    original_class_check_init_source_and_MRO_unchanged=True, pure_fixture_cases=401,
    fixture_tool=dict(chunk_id='d352e9',exit_code=0,closed=True),
    fixture_report=pin(D/'fixture_results.json'), actual_tool_receipt=pin(D/'actual_readonly_fixture_tool_return.json'),
    full_source_inverse_proof=pin(D/'source_inverse_proof.json'), current_normal_source_chain_pins=source_pins,
    unchanged_constraints=[
      'base.resolve(strict=True) is performed before checking values, preserving base failures first',
      'nonempty isinstance(values,list), and isinstance(each_value,str), including existing subclass acceptance',
      'Path normalization, absolute, literal dotdot, root==resolved_base, strict lexical descendant guards unchanged',
      'all ancestor checks in original order: is_symlink, exists, is_dir; no stat or path-state cache',
      'valid nonexistent future roots accepted; root/ancestor file, hardlink-to-file, dangling symlink and loops refused',
      'each path filesystem validation precedes its overlap test; an early overlap still precedes later invalid values',
      'returned Path objects follow input order; no sorting, deduplication, root dropping, or field filtering',
      'original base-file/future-child edge behavior preserved, not silently repaired'],
    algorithm=dict(previous='accepted prior roots pairwise lexical relative checks',
        candidate='per-call local path-components trie with None terminator, after unchanged filesystem guards',
        prior_root_is_parent='terminator seen before consuming next component',
        prior_root_is_child_or_same='nonempty final trie node',
        scope='lexical overlap only; no symlink following or stat memo',
        accepted_nonoverlapping_N_roots_pair_count='N*(N-1)/2 originally; trie visits sum(Path.parts lengths)',
        additional_memory='linear path-component dictionaries, per call only; no global/cross-stage state',
        actual_full_prepare_speedup_measured=False),
    normal_module_integration=dict(source_level_blocker_found=False,
        prospective_canonical_path=str(P/'moment_order_complete_history_resource_trie_20261010.py'),
        same_canonical_directory_depth_required_for_ROOT_ART=True,
        actual_new_module_source=pin(full),
        steps=[
          'Root source-admits and installs this complete copy under the new canonical basename; only this function differs',
          'A future new component normally imports the pinned new path under a new unique module name',
          'Future resources constructor and resource-root validators explicitly call that module genuine DynamicHistoryResources/validate_history_roots',
          'actual_resource_class_factory path/SHA truthfully point to the new source; do not retain old fe811 descriptor',
          'Preserve all old parent_factory/predecessor admissions and their original sealed source identities',
          'Keep unchanged resource contract, full no-follow scan, repeated fresh guards, failure_type forwarding, original caps and OwnRSS process MRO',
          'No old module global function replacement, class substitution, cached inventory, or changes to prepared 4f namespace'],
        unchanged_public_class_bases='DynamicHistoryResources inherits object as in the original; all full class bodies byteexact',
        warning='The copied original CLI/constants retain their historical values; this candidate is for normal resource-module use only, never invoke its old business CLI.'),
    profile_context_not_unbiased_walltime=dict(validate_calls=39,selected_profile_seconds=151.54,
        check_calls=7,selected_profile_seconds_check=94.52,host_check_calls=28,host_profile_seconds=383.18,
        includes_profiler_and_possible_concurrent_child_time=True),
    business_or_project_script_executed=False, temporary_real_tree_fixtures_only=True, project_written=False,
    original_caps_changed=False, full86_component_qualified=False, actual_process_RSS_pass=False,
    native_AAA_ABA_credit=False)
save('REPORT.json',report)
with (D/'REPORT.txt').open('x') as stream:
    stream.write('仅SOURCE与独立纯函数fixture通过，候选尚未安装。原函数130–149行只改两处：每次调用的局部路径树初始化；完成原路径/祖先检查后以路径树判断重复及父子重叠。返回原顺序、全部原错误顺序和文件系统检查原样，不缓存stat、不筛根。\n401项真实临时树比较实际d352e9整数0 CLOSED，包括future根、目录/祖先链接、悬挂/环、硬链接文件、str边界、父子/重复以及提前错误优先序。所有结果与原函数类型/路径顺序/异常类及消息相同。\n已提供完整原moment模块的新TMP副本，仅目标函数两区变化，原其余41函数/类片段、DynamicHistoryResources全class/check/__init__源码及原96GiB/free8GiB不变。正常接入需新canonical basename/唯一module身份/真实资源class源描述；旧祖先准入链及已prepare的4f绝不能改或monkeypatch。原模块ROOT按文件深度推导，因此必须安装于原validation/axial_material目录。\n现有profile时间含观测器开销与并行，不是无偏正常时长；本轮未测完整prepare提速，更未授full86/native/RSS/AAA/ABA资格。\n')
manifest = dict(schema='AXMAT_HISTORY_ROOTS_CANDIDATE_SMALL_EVIDENCE_MANIFEST_V1',
    files=[pin(p) for p in sorted(D.iterdir()) if p.is_file() and p.name!='EVIDENCE_MANIFEST.json'])
manifest['file_count']=len(manifest['files']);manifest['total_bytes']=sum(row['size_bytes'] for row in manifest['files'])
save('EVIDENCE_MANIFEST.json',manifest)
print(json.dumps(dict(status=report['status'],REPORT=pin(D/'REPORT.json'),full_module=pin(full),
    actual_receipt=pin(D/'actual_readonly_fixture_tool_return.json'),manifest=pin(D/'EVIDENCE_MANIFEST.json')),indent=2))
