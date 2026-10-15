# Pure read-only actual-binding graph/independent expected-owner union review.
# No producer or graph helper import; no API/constructor/phase invocation.
import ast, base64, copy, hashlib, json, math, os, stat, shutil, struct, time
from pathlib import Path
TMP = Path('/private/tmp/axmat_v9_actual_cold_binding_graph_resource_independent_review_20261009')
T = Path('/private/tmp/axmat-last-cprime-trim-combined-live-resource-v9-root-execution-20261009')
ROOT = Path('/Users/wen/spot')
ART = ROOT/'validation/artifacts'
HELPER = ROOT/'validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py'
HELPER_SHA = '1d7c4d7a9ecc4546ceb4c7e0b81562329f874ca5302621ef5fc026f62c7f7643'
GRAPH_SHA = '0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3'
WIRE_SHA = 'f91b0168754de2d1e207eda794bd5b4ecd143f84c53f58c27fbb7d45e24ff946'
LEGACY_SHA = 'e9634f406032b9872240ae0be7abd28159389146fa020494d03a4787264b05d2'
FACTORY_SHA = '44789bc288715c34d08dbfa91b9c05dfc78166c2b8fa048bbe0207b273419a46'
DECL_SHA = '7bc3d176f58ad6ee92d640c799b3f8d79923c65b2bf27c3b545c511e282b53e0'
PREP_SHA = '0297aa6543c36ca3f452b1948e0d034e218f71c253b08cd671c3c83cb01262fb'
SEAL_SHA = 'ece13c5594c48bb22af8d507f1f40ef88457efa824e28200c6ddfced70cf3aed'
RUN_SHA = '709a9592c8b4a56cba99c61b628db8fed91d0c49d76d75c360591f11fa1b9d27'
INPUT_SPECS_SHA = '2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa'
PREFIX = 'AXMAT_HISTORICAL_INPUT_OWNED_SPECS_LAST_CPRIME_TRIM_COMBINED_PHYSICAL_DEDUP_RUNTIME_LIVE_RESOURCE_SCOPES_V9'
PINS = {}
START = time.monotonic()
def identity(path):
    s = Path(path).lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]

def pin(path, sha=None):
    path = Path(path)
    before = identity(path)
    assert stat.S_ISREG(before[2]) and path.parent.resolve(strict=True) == path.parent
    h = hashlib.sha256()
    with path.open('rb') as stream:
        s = os.fstat(stream.fileno())
        assert [s.st_dev, s.st_ino] == before[:2]
        while block := stream.read(4 * 1024**2):
            h.update(block)
    assert identity(path) == before
    record = dict(path=str(path), identity=before, size=before[3], sha256=h.hexdigest())
    if sha:
        assert record['sha256'] == sha, str(path)
    PINS[str(path)] = record
    return record

def read_json(path, sha=None):
    record = pin(path, sha)
    def pairs(items):
        result = {}
        for key, value in items:
            assert key not in result, ('duplicate key', str(path), key)
            result[key] = value
        return result
    def floating(text):
        value = float(text)
        assert math.isfinite(value)
        return value
    def reject(text):
        raise ValueError('nonfinite JSON literal: ' + text)
    value = json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=pairs, parse_float=floating, parse_constant=reject)
    assert identity(path) == record['identity']
    return value

def canonical_pieces(value):
    return json.JSONEncoder(sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).iterencode(value)

def digest(value):
    result = hashlib.sha256()
    for text in canonical_pieces(value):
        result.update(text.encode('utf-8'))
    return result.hexdigest()

def decode_rows(table):
    codec = table['rows']
    assert type(codec) is dict and set(codec) == {'schema', 'encoding', 'row_count', 'column_count', 'data'}
    assert codec['schema'] == 'AXMAT_COMPLETE_FIVE_COLUMN_REQUIREMENT_ROWS_V1'
    assert codec['encoding'] == 'CANONICAL_UNSIGNED_LEB128_BASE64'
    assert type(codec['row_count']) is int and codec['row_count'] == 235528
    assert type(codec['column_count']) is int and codec['column_count'] == 5
    assert type(codec['data']) is str and len(codec['data']) % 4 == 0
    raw = base64.b64decode(codec['data'].encode('ascii'), validate=True)
    assert base64.b64encode(raw).decode('ascii') == codec['data']
    assert codec['row_count'] * 5 <= len(raw)
    limits = [len(table['paths']), len(table['paths']), len(table['owners']), len(table['categories']), len(table['binding_roles'])]
    offset = 0
    for _ in range(codec['row_count']):
        row = []
        for limit in limits:
            value = 0
            shift = 0
            groups = 0
            while True:
                assert offset < len(raw)
                byte = raw[offset]
                offset += 1
                groups += 1
                value |= (byte & 127) << shift
                assert value < limit
                if byte < 128:
                    assert groups == 1 or byte != 0
                    break
                shift += 7
                assert shift < max(1, limit.bit_length())
            row.append(value)
        yield tuple(row)
    assert offset == len(raw)

def independent_legacy_digest(graph):
    value = dict(graph)
    value.pop('content_sha256')
    value.pop('wire_encoding')
    value['schema'] = 'AXMAT_COMBINED_RUNTIME_VERIFIED_INPUT_GRAPH_V5'
    table = dict(value['requirements'])
    table['schema'] = 'AXMAT_COMBINED_RUNTIME_COMPLETE_TYPED_REQUIREMENT_TABLE_V1'
    h = hashlib.sha256()
    def emit(item):
        for piece in canonical_pieces(item):
            h.update(piece.encode('utf-8'))
    h.update(b'{')
    for index, key in enumerate(sorted(value)):
        if index:
            h.update(b',')
        emit(key)
        h.update(b':')
        if key != 'requirements':
            emit(value[key])
            continue
        h.update(b'{')
        for column, field in enumerate(sorted(table)):
            if column:
                h.update(b',')
            emit(field)
            h.update(b':')
            if field != 'rows':
                emit(table[field])
                continue
            h.update(b'[')
            for row_index, row in enumerate(decode_rows(table)):
                if row_index:
                    h.update(b',')
                h.update(('[' + ','.join(map(str, row)) + ']').encode('ascii'))
            h.update(b']')
        h.update(b'}')
    h.update(b'}')
    return h.hexdigest()

def root_validation(roots, art):
    assert type(roots) is list and roots and all(type(p) is str for p in roots)
    paths = [Path(p) for p in roots]
    assert len(paths) == len(set(paths))
    for p in paths:
        assert p.is_absolute() and '..' not in p.parts and art in p.parents
        for ancestor in [p] + list(p.parents):
            if os.path.lexists(ancestor):
                s = ancestor.lstat()
                assert stat.S_ISDIR(s.st_mode) and not stat.S_ISLNK(s.st_mode), str(ancestor)
            if ancestor == art:
                break
    for i, p in enumerate(paths):
        assert not any(p in q.parents or q in p.parents for q in paths[i+1:])
    return paths

def dynamic_roots(declared, art):
    return sorted(set(declared) | {str(p) for p in art.glob('axial-material-*')})

def resource_inventory(roots, art):
    # Reproduce the inherited no-follow apparent-byte scope using only stdlib.
    # Regular hard links count per path, matching the original resource contract.
    root_validation(roots, art)
    total = 0
    regular = 0
    directories = 0
    symlinks_ignored = 0
    h = hashlib.sha256()
    def emit(kind, path, s):
        record = [kind, str(path), s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]
        h.update(json.dumps(record,separators=(',',':')).encode() + b'\n')
    def visit(path):
        nonlocal total, regular, directories, symlinks_ignored
        fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            s = os.fstat(fd)
            emit('directory',path,s)
            directories += 1
            with os.scandir(fd) as iterator:
                entries = sorted(iterator, key=lambda e:e.name)
            for entry in entries:
                p = path / entry.name
                s = entry.stat(follow_symlinks=False)
                if stat.S_ISDIR(s.st_mode):
                    visit(p)
                elif stat.S_ISREG(s.st_mode):
                    emit('regular',p,s)
                    total += s.st_size
                    regular += 1
                elif stat.S_ISLNK(s.st_mode):
                    emit('ignored_symlink',p,s)
                    symlinks_ignored += 1
                else:
                    emit('other_ignored',p,s)
        finally:
            os.close(fd)
    absent_roots = []
    for path in map(Path,roots):
        if os.path.lexists(path):
            visit(path)
        else:
            absent_roots.append(str(path))
    assert roots == dynamic_roots(roots, art)
    root_validation(roots, art)
    return dict(artifact_bytes=total,regular_files=regular,directories=directories,symlinks_ignored=symlinks_ignored,absent_declared_roots=absent_roots,
                full_path_identity_inventory_sha256=h.hexdigest(),scope='Original complete axial-family live resource roots; no symlink following; apparent bytes per regular path')

def typed_equal(left, right):
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return list(left) == list(right) and all(typed_equal(left[key], right[key]) for key in left)
    if type(left) is list:
        return len(left) == len(right) and all(typed_equal(a, b) for a, b in zip(left, right))
    if type(left) is float:
        return math.isfinite(left) and math.isfinite(right) and struct.pack('!d', left) == struct.pack('!d', right)
    assert type(left) in (str, int, bool, type(None))
    return left == right

def owned_json(item): return read_json(item['path'],item['sha256'])
def sorted_object_boundary(value): return json.loads(json.dumps(value,sort_keys=True,allow_nan=False))

def current_graph_namespace(row,canonical):
    root=Path(row['canonical_root']); assert Path(row['root']).resolve(strict=True)==root and root.resolve(strict=True)==root
    assert row['namespace_exhaustive'] is True
    files={};dirs=[];links={}
    for base,names,leaves in os.walk(root,followlinks=False):
        base=Path(base)
        for name in names[:]:
            p=base/name;rel=str(p.relative_to(root))
            if p.is_symlink():
                target=p.resolve(strict=True); links[rel]=dict(kind='dir',target=str(target),text=os.readlink(p));names.remove(name)
            else: dirs.append(rel)
        for name in leaves:
            p=base/name;rel=str(p.relative_to(root))
            if p.is_symlink():
                target=p.resolve(strict=True);links[rel]=dict(kind='file' if target.is_file() else 'dir',target=str(target),text=os.readlink(p))
            else:
                assert str(p) in canonical and row['files'][rel]==canonical[str(p)]
                assert stat.S_ISREG(p.lstat().st_mode) and p.resolve(strict=True)==p
                files[rel]=canonical[str(p)]
    assert files==row['files'] and sorted(dirs)==row['directories'] and links==row['symlinks'],row['root']
    return dict(root=row['root'],canonical_root=str(root),files=len(files),directories=len(dirs),symlinks=len(links),expected_namespace_sha256=digest(row))

def aliases_and_absences(graph,canonical):
    observed=[]
    for row in graph['aliases']:
        p=Path(row['path']);assert p.is_symlink() and os.readlink(p)==row['text']
        resolved=p.resolve(strict=True);assert str(resolved)==row['target']
        assert row['kind']=='file' and resolved.is_file() and row['sha256']==canonical[str(resolved)]
        observed.append(dict(path=str(p),identity=identity(p),text=os.readlink(p),target=str(resolved)))
    absent=[]
    for p,expected in graph['absence_observations'].items():
        assert p in graph['absence_inputs'] and not os.path.lexists(p)
        assert expected['missing_errno']==2 and expected['observation']=='EXACT_DECLARED_ENOENT_ONLY' and expected['regular_input_bytes']==0
        for ancestor in expected['existing_ancestors']:
            literal=Path(ancestor['literal_component']);actual=literal.resolve(strict=True)
            assert str(actual)==ancestor['canonical_path']
            s=actual.lstat();wanted=ancestor['identity']
            assert dict(device=s.st_dev,inode=s.st_ino,mode=s.st_mode,rdev=s.st_rdev,major=os.major(s.st_rdev),minor=os.minor(s.st_rdev))==wanted
        assert not os.path.lexists(expected['first_missing_component'])
        absent.append(expected)
    assert len(observed)==186 and len(absent)==445
    return dict(alias_identity_digest=digest(observed),absence_observations_digest=digest(absent),aliases=186,absence_inputs=445)

def expected_add(files, path, wanted):
    # Expected SHA is only supplied by immutable literal/declared maps, not
    # synthesized from the current module/file being checked.
    path = str(Path(path))
    assert Path(path).is_absolute() and '..' not in Path(path).parts
    assert type(wanted) is str and len(wanted) == 64 and wanted != '0'*64
    assert all(c in '0123456789abcdef' for c in wanted)
    assert path not in files or files[path] == wanted, ('expected conflict', path)
    files[path] = wanted

def static_constants(factory_path):
    text = Path(factory_path).read_text()
    tree = ast.parse(text)
    result = {}
    def value(node):
        if isinstance(node, ast.Constant): return node.value
        if isinstance(node, ast.Name): return result[node.id]
        if isinstance(node, (ast.List, ast.Tuple)):
            values = [value(item) for item in node.elts]
            return values if isinstance(node, ast.List) else tuple(values)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            return value(node.left)/value(node.right)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'Path' and len(node.args)==1 and not node.keywords:
            return Path(value(node.args[0]))
        raise ValueError('not a literal/path constant')
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
            try: result[node.targets[0].id] = value(node.value)
            except (ValueError, KeyError, TypeError): pass
    inventory=read_json(TMP/'readonly_binding_gate_source_inventory.json')
    for name, row in inventory.items():
        fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
        assert ast.get_source_segment(text,fn)==row['full_source'],name
    guard=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='guard_owner_files')
    literal=next(n.value for n in guard.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='expected_project_sources' for t in n.targets))
    expected26=ast.literal_eval(literal)
    assert typed_equal(expected26,read_json(TMP/'literal_expected_guard_26_sources.json')) and len(expected26)==26
    return result, expected26

def independent_guard_expected(constants, expected26):
    # Full inverse of F59 guard_owner_files owner construction, using only
    # sealed JSON/source literals and stdlib. No guard/module callable runs.
    guardfolder=constants['FULL']/'preflight/live_guard'
    guardpath=guardfolder/'guard_controls.json'
    guardsha='ae4d7e86423a187c29efd5bf87d54053081d7b7fcf18ac88cd9e49639cb07454'
    guard=read_json(guardpath,guardsha)
    files={}
    expected_add(files,guardpath,guardsha)
    expected_add(files,guardfolder/'tested_driver_source.py',guard['source_sha256'])
    tested=[dict(path=str(guardpath),sha256=guardsha),dict(path=str(guardfolder/'tested_driver_source.py'),sha256=guard['source_sha256'])]
    for name, wanted in guard['control_files'].items():
        assert not Path(name).is_absolute() and '..' not in Path(name).parts
        expected_add(files,guardfolder/name,wanted)
        tested.append(dict(path=str(guardfolder/name),sha256=wanted))
    for path,wanted in ((constants['BASE_CONTROLLER'],constants['BASE_CONTROLLER_SHA']),
        (ROOT/'validation/axial_material/qualify_refined_AAA_layered_full.py','70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'),
        (ROOT/'validation/axial_material/prepare_qualified_AB_source_factor_production.py','619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'),
        (ROOT/'validation/axial_material/prepare_qualified_AB_moment_order_production.py','fe81150fbf270cac44e241ad64f352cf2f623fa65f7ccb4a9b0ded0a4f2c2d41')):
        expected_add(files,path,wanted)
    source_decl=constants['FULL']/'declaration.json'
    source_decl_sha='f032eee5a6dfb9844a57043d1a357a8bfe383f2d6c2c71761841717f3ed6c94b'
    source_owners=read_json(source_decl,source_decl_sha)['files']
    project_sources={p:s for p,s in source_owners.items() if Path(p).is_relative_to(ROOT/'validation') and Path(p).suffix=='.py'}
    assert project_sources==expected26 and len(project_sources)==26
    expected_add(files,source_decl,source_decl_sha)
    for path,wanted in expected26.items(): expected_add(files,path,wanted)
    scipy=read_json(constants['SCIPY_MANIFEST'],constants['SCIPY_MANIFEST_SHA'])
    scipyfiles={str(constants['SCIPY_TARGET_ROOT']/name):wanted for name,wanted in scipy['target_namespace']['files'].items()}
    expected_add(scipyfiles,scipy['wheel']['path'],scipy['wheel']['sha256'])
    assert scipyfiles==scipy['files'] and len(scipyfiles)==1424
    expected_add(scipyfiles,constants['SCIPY_MANIFEST'],constants['SCIPY_MANIFEST_SHA'])
    for path,wanted in scipyfiles.items(): expected_add(files,path,wanted)
    for name in ('SCIPY_HELPER','FROZEN_FAILED_PREP_FACTORY','PHYSICAL_BASIS_HELPER','OWN_PID_SUPERVISOR','FROZEN_CANONICAL_COLD_FAILURE'):
        expected_add(files,constants[name],constants[name+'_SHA'])
    expected_add(files,ROOT/'validation/axial_material/prepare_historical_input_owned_specs_physical_dedup_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak.py','75373e45c4e355dd7778767eb90c7bc8711062c876acd8827f3ad5dbd13ad80d')
    prep_failure=ART/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-file-snapshot-terminal-scipy-env-physical-basis-own-pid-peak-20261008/preparation_failure_terminal_return.json'
    expected_add(files,prep_failure,'c0bc6c0cd6df5b057467029e90b6376716cc16aeedc5dd9ddc0432b866db24d1')
    expected_add(files,ROOT/'validation/axial_material/prepare_historical_input_owned_specs_physical_dedup_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak_v2.py','ef216ef58c201df31c661c7f7828ff7f2d201444b55c5f2418d96d6f68d96cf5')
    bind_failure=ART/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-file-snapshot-terminal-scipy-env-physical-basis-own-pid-peak-v2-20261008/binding_failure_terminal_return.json'
    expected_add(files,bind_failure,'71aac4433c2c0c503aefad8f72742c1864fb0d3a1127a254fd12cd5e0cfe282d')
    old_bind=read_json(bind_failure,files[str(bind_failure)])
    for key in ('full_stdout','full_stderr','input_declaration_terminal_evidence','input_preparation_terminal_evidence','prepared'):
        expected_add(files,old_bind[key]['path'],old_bind[key]['sha256'])
    old_prep=read_json(prep_failure,files[str(prep_failure)])
    for key in ('full_stdout','full_stderr','declaration_terminal_evidence'):
        expected_add(files,old_prep[key]['path'],old_prep[key]['sha256'])
    old_cold=read_json(constants['FROZEN_CANONICAL_COLD_FAILURE'],constants['FROZEN_CANONICAL_COLD_FAILURE_SHA'])
    for key in ('full_stdout','full_stderr','failure','run_status','actual_stages'):
        expected_add(files,old_cold[key]['path'],old_cold[key]['sha256'])
    return files,tested,dict(original_project_sources=26,scipy_package_wheel_and_manifest=1425,guard_control_files=len(guard['control_files']),
        complete_failed_binding_receipt_payloads=5,complete_failed_preparation_receipt_payloads=3,complete_failed_cold_receipt_payloads=5,
        old_failure_facts_not_promoted_to_current_fixture_PASS=True,guard_expected_count=len(files),guard_expected_digest=digest(files))

def main():
    plan=read_json('/private/tmp/axmat_v9_cold_actual_DECLARE_readonly_scope_plan_20261009/PLAN.json','59781ef14365a7b17d37d3992eeaf7bc7fd1967c249ad7a381e103e12a41ce52')
    binding_plan=read_json(TMP/'PLAN.json','58e22ea801a420a8ed29e2e109761b1614c1e8649842b5eac1a50073657e4b16')
    assert all(v is None for v in binding_plan['future_actual'].values())
    source=Path(plan['source_root']);output=Path(plan['future_output_root']);term=Path(plan['declaration_terminal_root']);control=Path(plan['future_control_terminal_root'])
    rdir=ROOT/'validation/axial_material/last_cprime_trim_combined_live_resource_v9_build_review_20261009'
    prior=read_json('/private/tmp/axmat_v9_actual_cold_DECLARE_graph_INPUT_resource_independent_review_20261009/REPORT.json','31f29c1b5642ad86d980623363a29cb15f19c2f7094bb95a4fa6393e2651f8d0')
    priorprep=read_json('/private/tmp/axmat_v9_actual_cold_PREP_graph_resource_independent_review_20261009/REPORT.json','2c124560cb591339ee1dbc0b43471db3d28a6b65a843c0381d7cf37607fea39d')
    priorprepreceipt=read_json('/private/tmp/axmat_v9_actual_cold_PREP_graph_resource_independent_review_20261009/actual_readonly_tool_return.json','66dbf89138ae4af595ed0c3f30392400e67eb4947e77adba756d25958c6e00bc')
    assert prior['status']==priorprep['status']=='PASS'
    assert priorprepreceipt['actual_tool_result']==dict(initial_chunk_id='ff7547',session_id=8846,terminal_chunk_id='dc11fe',exit_code=0,closed=True)
    rootobs=read_json(rdir/'Root_actual_V9_cold_binding_tool_return.json','c24ff19a49b77d904057faeb694faaeeaaa181c621850f62353f7a43c839ad98')
    expectedtool=dict(initial_chunk_id='ce453a',session_id=31625,terminal_chunk_id='13d167',exit_code=0)
    assert rootobs['actual_tool_result']==dict(expectedtool,closed=True) and type(rootobs['actual_tool_result']['exit_code']) is int
    assert rootobs['actual_success_recorder_tool']==dict(chunk_id='2169ff',exit_code=0,closed=True)
    receipt=read_json(term/'binding_terminal_return.json','d26300e92fc469bc1674f5c788b8806656791da817019d99d12daf6f912af1b1')
    assert receipt['actual_tool_result']==expectedtool and type(receipt['returncode']) is int and receipt['returncode']==0
    assert receipt['record_producer']=='root' and receipt['actual_tool_terminal_return_observed'] is True and receipt['record_written_after_actual_terminal_return'] is True
    assert receipt['transport_started'] is False and receipt['scientific_qualification'] is False
    assert receipt['source']==plan['formal_factory'] and receipt['command']==rootobs['launch_command'] and len(receipt['command'])==9
    assert rootobs['actual_execve_syscall_argv_trace'] is None
    prep_admission=owned_json(rootobs['completed_qualified_PREP_admission'])
    assert rootobs['completed_qualified_PREP_admission']['sha256']=='8fd5bd7965cb61030ce5423b642d5356267818694dc90935ba62f09c0f9e33c3'
    assert prep_admission['schema']=='AXMAT_ROOT_V9_ACTUAL_COLD_PREP_FULL_COMPLEMENTARY_ADMISSION_V1'
    assert prep_admission['status']=='QUALIFIED_COMPLETE_ACTUAL_PREP_INPUT_ONLY_READY_FOR_UNIQUE_CANONICAL_BINDING'
    assert prep_admission['source_report_sha256']=='4abf92d49fc9f8a50f9e410ad8c7c311f0790fb7451a8e6cc98a48b56ea25f24'
    assert prep_admission['graph_report_sha256']==PINS['/private/tmp/axmat_v9_actual_cold_PREP_graph_resource_independent_review_20261009/REPORT.json']['sha256']
    assert prep_admission['joint_scope_sha256']=='df1f768e051618f1f7f1134d398aaa6ee1cc9d965094c7f0c0e938e64ae1e208'
    assert prep_admission['actual_PREP_tool']==dict(initial_chunk_id='1a53dd',session_id=2047,terminal_chunk_id='d7ffa4',exit_code=0,closed=True)
    assert prep_admission['original_all_caps_retained'] is True
    for row in rootobs['copied_pure_Root_provenance']:pin(row['path'],row['sha256'])
    for key in ('formal_factory','formal_consumer','formal_intake_binding'):pin(plan[key]['path'],plan[key]['sha256'])
    assert plan['formal_factory']['sha256']=='59d0c9b0f0a3b9ca6764f628ade537ec9b09eaa6edfe69e734994a7323adbfc8'
    constants,expected26=static_constants(plan['formal_factory']['path'])
    binding=owned_json(receipt['binding'])
    assert receipt['binding']==rootobs['actual_binding']==dict(path=str(output/'own_rss_binding.json'),sha256='4e8de93043fa08ac0c6e1f1702b69606a6bf0b155c30007c356ec4837919c930')
    assert PINS[str(output/'own_rss_binding.json')]['size']==60598579
    stdout=owned_json(receipt['full_stdout']);pin(receipt['full_stderr']['path'],receipt['full_stderr']['sha256'])
    assert PINS[receipt['full_stdout']['path']]['size']==2682 and PINS[receipt['full_stderr']['path']]['size']==0
    assert typed_equal(stdout,receipt['actual_stdout_result']) and typed_equal(stdout,rootobs['actual_stdout_result'])
    assert stdout['classification']=='PREPARED_NEW_CANONICAL_BINDING_INPUT_ONLY_NO_FIXTURE_CREDIT' and stdout['binding']==receipt['binding']
    assert stdout['new_binding_fixtures_executed'] is False and stdout['scientific_qualification'] is False
    for k in ('new_binding_controls_executed','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','scientific_qualification'):assert rootobs[k] is False
    termnames=sorted(p.name for p in term.iterdir())
    assert termnames==sorted([phase+suffix for phase in ('declaration','prepare','binding') for suffix in ('.stdout','.stderr','_terminal_return.json')])
    for p in term.iterdir():pin(p)
    # SOURCE/OUTPUT retained exact metadata and original complete local43.
    decl=read_json(source/'declaration.json','6d937be82fb66c21f110241bd2658a37b793bdaf098e19b7bb50b596c9cad00c')
    seal=read_json(source/'factory_seal.json','810f8b897d31d48128eda6a5349e3ff55c2d47c71695dab51db0055e4551d5ce')
    assert sorted(p.name for p in source.iterdir())==plan['expected_SOURCE_files']
    for name,sha in seal['files'].items():pin(source/name,sha)
    for path,record in prior['SOURCE31_pins'].items():assert identity(path)==record['identity']
    prepared=read_json(output/'prepared.json','35f8100a753b149b6b100b8bc7154ca1b09f488a464a5068e0ffb826877d6ec7')
    assert len(prepared['local_files'])==43 and prepared['classification']=='PREPARED_NO_TRANSPORT' and 'own_child_supervision' not in prepared
    currentlocal={str(p.relative_to(output)) for p in output.rglob('*') if p.is_file() and not p.is_symlink()}
    assert currentlocal==set(prepared['local_files'])|{'prepared.json','own_rss_binding.json'}
    for name,wanted in prepared['local_files'].items():
        assert not Path(name).is_absolute() and '..' not in Path(name).parts
        pin(output/name,wanted)
    for key in ('cases','budgets','production_config','inputs','case_spec','rank_addendum','declaration','resource_roots'):
        expected=dict(path=str(source/'declaration.json'),sha256=PINS[str(source/'declaration.json')]['sha256']) if key=='declaration' else sorted_object_boundary(decl[key])
        assert typed_equal(prepared[key],expected),key
    assert prepared['budgets']==plan['original_budgets']
    m=owned_json(decl['rank1_factor_cache_revision']);case=owned_json(decl['case_spec']);storage=owned_json(decl['rank1_factor_cache_resource_admission'])
    intake=m['component_input_intake'];rawapi=owned_json(intake['api_return']);api=sorted_object_boundary(rawapi)
    old_rawproof=read_json('/private/tmp/axmat_v9_actual_bounded_INPUT_graph_descriptor_independent_review_20261009/complete_graph_and_whole_returned_INPUT_review.json','defdf82d849912f795fae8a8fea856bb20c475771cdb41d67a11ffe2a49f78f8')
    assert len(api)==65 and list(rawapi)==old_rawproof['field_names']
    assert typed_equal(case['rank1_factor_cache_trial']['actual_combined_runtime_admission'],api)
    assert digest(api)==prior['whole65_sha256']==priorprep['whole65_semantic_sha256']
    specs=read_json(ROOT/'validation/axial_material/combined_runtime_complete_historical_input_specs_20261007.json',INPUT_SPECS_SHA)
    assert typed_equal(api['actual_components'],specs['metadata']['historical_actual_components']) and len(api['actual_components'])==7
    trim=owned_json(api['actual_last_cprime_trim_component_INPUT']);assert len(trim)==73 and digest(trim)==prior['whole_trim73_sha256']
    assert typed_equal(sorted_object_boundary(trim),api['actual_last_cprime_trim_admission'])
    whole=api['actual_components'];memory=whole['dedup']['inherited_rank1_factor_cache_memory_admission']
    expected_returns=dict(original92=whole['original92'],memory438=memory,physical=whole['physical'],dedup=whole['dedup'],capture=whole['capture'],combined=api,last_cprime_trim=api['actual_last_cprime_trim_admission'])
    assert typed_equal(binding['actual_component_returns'],expected_returns)
    assert api['inherited_rank1_cache_admission']==whole['original92'] and api['inherited_physical_admission']==whole['physical']
    assert api['inherited_dedup_admission']==whole['dedup'] and api['original_operator_capture_dependency']==whole['capture'] and api['inherited_rank1_factor_cache_memory_admission']==memory
    for key in ('AAA_accuracy_qualified','ABA_admitted','native_transport_executed','combined_runtime_native_RSS_proved','production_pipeline_prepared','trim_native_RSS_proof_obtained'):assert api[key] is False
    # Full graph wire/decoded semantics/order/duplicate rows are unpruned.
    graphpath=Path(intake['complete_historical_input_graph']['path']);graph=read_json(graphpath,GRAPH_SHA)
    assert PINS[str(graphpath)]['size']==64644869<67108864 and graph['content_sha256']==WIRE_SHA
    wire=dict(graph);wire.pop('content_sha256');assert digest(wire)==WIRE_SHA
    assert independent_legacy_digest(graph)==graph['wire_encoding']['decoded_content_sha256']==LEGACY_SHA
    rows=0;rowhash=hashlib.sha256();previous=None;duplicates=0
    table=graph['requirements'];assert table['columns']==['path','canonical_path','owner','category','binding_role'] and table['duplicate_edges_retained'] is True
    for row in decode_rows(table):
        p,c,o,k,r=row;key=(table['paths'][c],table['owners'][o],table['paths'][p],table['categories'][k],table['binding_roles'][r]);assert previous is None or previous<=key
        duplicates+=previous==key;previous=key;rows+=1;rowhash.update(json.dumps(row,separators=(',',':')).encode()+b'\n')
    assert rows==235528 and rowhash.hexdigest()==priorprep['requirement_row_sha256']==prior['requirement_row_sha256']
    canonical={r['path']:r['sha256'] for r in graph['canonical_files']};assert len(canonical)==35647 and sum(r['size_bytes']for r in graph['canonical_files'])==35803098221
    beforecanon={p:identity(p) for p in canonical}
    assert digest(beforecanon)==prior['graph_beforeafter_canonical_identity_digest']==priorprep['complete_canonical_before_after_seven_field_identity_digest']
    for p,record in beforecanon.items():assert stat.S_ISREG(record[2]) and Path(p).resolve(strict=True)==Path(p)
    assert len(m['files'])==37339
    dependencybefore={}
    for p,wanted in m['files'].items():
        if p in canonical:assert canonical[p]==wanted;expected=beforecanon[p]
        else:
            old=prior['reviewed_pins'][p];assert old['sha256']==wanted;expected=old['identity']
        assert identity(p)==expected and Path(p).resolve(strict=True)==Path(p);dependencybefore[p]=expected
    assert digest(dependencybefore)==priorprep['full_metadata_dependency_before_after_identity_digest']
    assert len(api['descriptor_files'])==35675
    for p,wanted in api['descriptor_files'].items():assert m['files'][p]==wanted
    before_ns=[current_graph_namespace(row,canonical) for row in graph['namespaces']];assert len(before_ns)==86
    before_aliasabsence=aliases_and_absences(graph,canonical)
    # Exact expected-owner map is independently assembled in original order.
    guardexpected,tested,guardproof=independent_guard_expected(constants,expected26)
    for p,wanted in guardexpected.items():assert m['files'][p]==wanted,p
    assert typed_equal(binding['tested_guard_files'],tested)
    env=read_json(source/'analysis_environment.json',seal['files']['analysis_environment.json']);assert len(env['files'])==1860
    expectedfiles=dict(m['files'])
    # materialize_metadata uses the original metadata.files object as
    # context.additional_expected_files. Its two independently declared
    # descriptors are appended before prepare_binding copies m.files.
    # Preserve this original source alias update and exact insertion order.
    aliasproof=read_json(TMP/'complete_original_metadata_alias_owner_order_source_supplement.json')
    assert aliasproof['factory']==plan['formal_factory']
    factorytext=Path(plan['formal_factory']['path']).read_text();factorytree=ast.parse(factorytext)
    for name,wanted in aliasproof['complete_original_alias_source_functions'].items():
        fn=next(n for n in factorytree.body if isinstance(n,ast.FunctionDef)and n.name==name)
        assert ast.get_source_segment(factorytext,fn)==wanted
    expected_add(expectedfiles,decl['rank1_factor_cache_revision']['path'],decl['rank1_factor_cache_revision']['sha256'])
    expected_add(expectedfiles,output/'runtime'/Path(constants['PRIVATE_INPUT_CONSUMER']).name,constants['PRIVATE_INPUT_CONSUMER_SHA'])
    for name,wanted in prepared['local_files'].items():expected_add(expectedfiles,output/name,wanted)
    for path,wanted in env['files'].items():expected_add(expectedfiles,path,wanted)
    expected_add(expectedfiles,plan['formal_factory']['path'],plan['formal_factory']['sha256'])
    expected_add(expectedfiles,output/'prepared.json','35f8100a753b149b6b100b8bc7154ca1b09f488a464a5068e0ffb826877d6ec7')
    for key in ('case_spec','rank_addendum','declaration'):expected_add(expectedfiles,prepared[key]['path'],prepared[key]['sha256'])
    for item in prepared['inputs'].values():expected_add(expectedfiles,item['path'],item['sha256'])
    for path,wanted in guardexpected.items():expected_add(expectedfiles,path,wanted)
    for name,wanted in seal['files'].items():expected_add(expectedfiles,source/name,wanted)
    expected_add(expectedfiles,source/'factory_seal.json','810f8b897d31d48128eda6a5349e3ff55c2d47c71695dab51db0055e4551d5ce')
    dterm=read_json(term/'declaration_terminal_return.json','d0ba07a475355ec69aefc933cdbde49ab88b71b689d6b8e8c796b18ad44cd73c')
    expected_add(expectedfiles,term/'declaration_terminal_return.json','d0ba07a475355ec69aefc933cdbde49ab88b71b689d6b8e8c796b18ad44cd73c')
    for key in ('full_stdout','full_stderr'):expected_add(expectedfiles,dterm[key]['path'],dterm[key]['sha256'])
    assert typed_equal(binding['files'],expectedfiles)
    assert str(output/'own_rss_binding.json') not in expectedfiles
    assert str(term/'binding_terminal_return.json') not in expectedfiles
    assert all(str(term/name) not in expectedfiles for name in ('binding.stdout','binding.stderr'))
    additional={p:sha for p,sha in expectedfiles.items() if p not in m['files']}
    extra_before={}
    for p,wanted in additional.items():extra_before[p]=pin(p,wanted)['identity']
    assert len(expectedfiles)==37395 and len(additional)==56
    assert typed_equal(binding['producer_environment'],env)
    assert typed_equal(binding['resource_info'],{k:prepared[k]for k in ('artifact_root','resource_roots','case_spec')})
    assert binding['input_declaration_terminal_evidence']==dict(path=str(term/'declaration_terminal_return.json'),sha256='d0ba07a475355ec69aefc933cdbde49ab88b71b689d6b8e8c796b18ad44cd73c')
    moduleowners=binding['module_owners'];assert type(moduleowners) is dict and moduleowners
    moduleproof=[]
    for name,row in moduleowners.items():
        assert type(name) is str and set(row)=={'path','sha256'}
        path=Path(row['path']);assert path.is_relative_to(ROOT/'validation') and path.resolve(strict=True)==path
        assert expectedfiles[str(path)]==row['sha256'],name
        assert identity(path)==dependencybefore.get(str(path),extra_before.get(str(path))),name
        moduleproof.append([name,row['path'],row['sha256']])
    assert moduleowners['__main__']==dict(path=str(output/'runtime/combined_cold_own_rss_controls.py'),sha256=constants['CONTROLS_SHA'])
    runtime=output/'runtime';runtime_expected={name.removeprefix('runtime/'):sha for name,sha in prepared['local_files'].items() if name.startswith('runtime/')}
    assert len(runtime_expected)==31 and typed_equal(binding['runtime_namespace'],dict(files={name:runtime_expected[name]for name in sorted(runtime_expected)},directories=[]))
    assert all(p.is_file() and not p.is_symlink() for p in runtime.iterdir()) and set(p.name for p in runtime.iterdir())==set(runtime_expected)
    required_preload=['production_inputs','snapshot_control_preflight','qualified_snapshot_ingestion','numerical_layout_admission','rank1_factor_cache_admission','white_receiver_tracking','physical_common_basis_admission']
    assert list(binding['runtime_module_owners'])==required_preload
    for name,row in binding['runtime_module_owners'].items():
        assert row==dict(path=str(runtime/(name+'.py')),sha256=runtime_expected[name+'.py']) and moduleowners[name]==row
    # Root dynamic complete-family union is current and bounded, not a replay of
    # obsolete observed file count/byte totals. Own binding + receipt now count.
    roots=dynamic_roots(prepared['resource_roots'],ART)
    assert roots==prepared['resource_roots']==decl['resource_roots']==m['component_resource_roots']==storage['resource_roots']
    assert len(graph['live_resource_roots'])==231 and set(graph['live_resource_roots']).issubset(roots)
    assert len(roots)==236 and all(str(p) in roots for p in (source,output,term,control))
    resbefore=resource_inventory(roots,ART);freebefore=shutil.disk_usage(ART).free
    reserve=storage['fresh_AAA_reserve_bytes'];assert reserve==20971764748==math.ceil(1.5*storage['original_complete_12_map_case_bytes'])+2**30
    assert storage['original_complete_12_map_case_bytes']==13265348616 and storage['unchanged_history_cap_bytes']==96*2**30 and storage['unchanged_min_free_bytes']==8*2**30
    assert resbefore['artifact_bytes']+reserve<96*2**30 and freebefore-reserve>=8*2**30
    print('Actual binding independent expected37395 owner union exact; all35647 inherited byte identities and complete graph metadata validated',flush=True)
    assert before_ns==[current_graph_namespace(row,canonical) for row in graph['namespaces']]
    assert before_aliasabsence==aliases_and_absences(graph,canonical)
    assert beforecanon=={p:identity(p) for p in canonical}
    assert dependencybefore=={p:identity(p) for p in m['files']}
    assert extra_before=={p:identity(p) for p in additional}
    resafter=resource_inventory(roots,ART);freeafter=shutil.disk_usage(ART).free
    assert resbefore==resafter and roots==dynamic_roots(prepared['resource_roots'],ART)
    assert resafter['artifact_bytes']+reserve<96*2**30 and freeafter-reserve>=8*2**30
    assert sorted(p.name for p in term.iterdir())==termnames and sorted(p.name for p in source.iterdir())==plan['expected_SOURCE_files']
    assert not os.path.lexists(control)
    for name in ('prepared_cold.json','binding_controls','AAA','ABA','training','archives','cold_source_failure.json','cold_closeout_seal.json'):assert not os.path.lexists(output/name),name
    for p,record in PINS.items():assert identity(p)==record['identity']
    result=dict(schema='AXMAT_V9_ACTUAL_COLD_BINDING_COMPLETE_EXPECTED_OWNER_UNION_GRAPH_RESOURCE_POSTREVIEW_V1',status='PASS',
        scope='Complete independent expected-owner union, whole65/original7/trim73/new sevenDICT returns, full unchanged graph semantic+identity/namespace/alias/absence, complete dynamic resource window; complementary source/MRO/codehash report required for whole binding admission.',
        actual_binding_Root_tool=rootobs['actual_tool_result'],actual_success_recorder_tool=rootobs['actual_success_recorder_tool'],Root_observer=PINS[str(rdir/'Root_actual_V9_cold_binding_tool_return.json')],actual_binding_receipt=PINS[str(term/'binding_terminal_return.json')],actual_binding=PINS[str(output/'own_rss_binding.json')],prior_full_PREP_admission=PINS[rootobs['completed_qualified_PREP_admission']['path']],
        inherited_actual_fullBYTE_REPORT=PINS['/private/tmp/axmat_v9_actual_cold_DECLARE_graph_INPUT_resource_independent_review_20261009/REPORT.json'],inherited_recent_fullPREP_REPORT=PINS['/private/tmp/axmat_v9_actual_cold_PREP_graph_resource_independent_review_20261009/REPORT.json'],inherited_recent_fullPREP_tool=priorprepreceipt['actual_tool_result'],
        canonical_files=35647,inherited_canonical_bytes=35803098221,fresh_canonical_payload_content_reads=0,complete_canonical_before_after_seven_field_identity_digest=digest(beforecanon),
        requirement_rows=rows,duplicate_requirement_rows=duplicates,requirement_row_sha256=rowhash.hexdigest(),graph_full_json_pin=PINS[str(graphpath)],original64MiB_cap_retained=True,wire_content_sha256=WIRE_SHA,decoded_legacy_semantic_sha256=LEGACY_SHA,
        namespaces_before_after86=before_ns,aliases_absences_before_after=before_aliasabsence,metadata_dependency_count=37339,metadata_before_after_identity_digest=digest(dependencybefore),API_descriptor_union35675_retained=True,full_dtype_layout_owner_trace_graph_content_unchanged=True,
        whole65_complete_type_order_values_floatbits_equal=True,original_API_raw65_order_unchanged=True,strict_sorted_consumer_materialization_boundary_exact=True,whole65_semantic_sha256=digest(api),whole_original7_semantic_sha256=digest(api['actual_components']),whole_trim73_semantic_sha256=digest(trim),new_actual_component_returns7_source_order=list(expected_returns),new_actual_component_returns7_complete_type_order_floatbits_equal=True,
        complete_guard_literal_manifest_failure_expected_proof=guardproof,expected_files_count=len(expectedfiles),new_expected_files_count=len(additional),expected_files_complete_insertion_order_equal=True,expected_files_whole_sha256=digest(expectedfiles),additional_expected_files=additional,additional_before_after_identity_digest=digest(extra_before),
        all_module_owners_count=len(moduleowners),all_module_owners_expected_independent=True,all_module_owner_rows_sha256=digest(moduleproof),no_arbitrary_current_module_fresh_SHA_used_as_expected=True,binding_self_file_excluded=True,new_binding_receipt_and_streams_not_backfilled_into_prior_expected_owner_map=True,
        source31_full_SHA_and_identity_unchanged=True,new_OUTPUT43_local_files_prepared_and_binding45_full_SHA=True,runtime_namespace31_and_7preload_exact=True,terminal_exact9_fullSHA=True,full_stdout_bytes=2682,full_stderr_bytes=0,
        prepared_cases_budgets_config_inputs_and_resource_info_complete_unchanged=True,declared_roots_count=len(prepared['resource_roots']),dynamic_current_roots_count=len(roots),current_resources_before=resbefore,current_resources_after=resafter,resources_before_after_complete_inventory_equal=True,disk_free_before=freebefore,disk_free_after=freeafter,history_budget_bytes=96*2**30,min_free_bytes=8*2**30,original_parent_case_bytes=13265348616,fresh_AAA_reserve_bytes=reserve,strict_reservation_gate_passed=True,old_observed_filecounts_not_current_fixed_gate=True,
        actual_execve_syscall_argv_trace_saved=False,source_derived_handoff_separate_from_actual_observed_CLI=True,future_controls_prepared_cold_and_native_outputs_absent=True,new_binding_fixtures_executed=False,standardlib_readonly_only_no_business_or_graph_helper_import=True,project_formal_ART_written=False,only_TMP_evidence_written=True,elapsed_seconds=time.monotonic()-START,native_RSS_credit=False,AAA_accuracy_qualified=False,ABA_admitted=False,scientific_qualification=False,full_read_pins=PINS)
    with (TMP/'REPORT.json').open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:result[k]for k in ('status','canonical_files','inherited_canonical_bytes','fresh_canonical_payload_content_reads','requirement_rows','expected_files_count','new_expected_files_count','all_module_owners_count','dynamic_current_roots_count','elapsed_seconds')},sort_keys=True),flush=True)

if __name__=='__main__':main()
