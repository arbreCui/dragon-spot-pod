# Pure read-only metadata review. Never imports/calls the producer/business API.
# This module is prepared before terminal recording; actual_input_binding.json
# remains absent until Root provides true closed host zero + saved payload pins.
import ast, base64, copy, hashlib, json, math, os, stat, shutil, struct, time
from pathlib import Path
TMP = Path('/private/tmp/axmat_v9_actual_cold_PREP_graph_resource_independent_review_20261009')
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

def main():
    plan=read_json('/private/tmp/axmat_v9_cold_actual_DECLARE_readonly_scope_plan_20261009/PLAN.json','59781ef14365a7b17d37d3992eeaf7bc7fd1967c249ad7a381e103e12a41ce52')
    source=Path(plan['source_root']);output=Path(plan['future_output_root']);term=Path(plan['declaration_terminal_root']);control=Path(plan['future_control_terminal_root'])
    prior=read_json('/private/tmp/axmat_v9_actual_cold_DECLARE_graph_INPUT_resource_independent_review_20261009/REPORT.json','31f29c1b5642ad86d980623363a29cb15f19c2f7094bb95a4fa6393e2651f8d0')
    priorreceipt=read_json('/private/tmp/axmat_v9_actual_cold_DECLARE_graph_INPUT_resource_independent_review_20261009/actual_readonly_tool_return.json','29130c3bd1315061174d540308b331b9838fa57f69618847251e3fd1583f8b4c')
    assert prior['status']=='PASS' and priorreceipt['actual_tool_result']==dict(initial_chunk_id='a52ae6',session_id=41407,terminal_chunk_id='0a5fda',exit_code=0,closed=True)
    rdir=ROOT/'validation/axial_material/last_cprime_trim_combined_live_resource_v9_build_review_20261009'
    rootobs=read_json(rdir/'Root_actual_V9_cold_prepare_tool_return.json','c1e24c926bb6aedd909f641717b3a4ec60970ec418aa3f3dfa023b696dd18f16')
    expectedtool=dict(initial_chunk_id='1a53dd',session_id=2047,terminal_chunk_id='d7ffa4',exit_code=0)
    assert rootobs['actual_tool_result']==dict(expectedtool,closed=True) and type(rootobs['actual_tool_result']['exit_code']) is int
    assert rootobs['actual_success_recorder_tool']==dict(chunk_id='15dda0',exit_code=0,closed=True)
    receipt=read_json(term/'prepare_terminal_return.json','2bcce12bb05d50b7dabce828f14dc7bd1dbff2a3383af5ac0ab81dbc10d8050a')
    assert receipt['actual_tool_result']==expectedtool and type(receipt['returncode']) is int and receipt['returncode']==0
    assert receipt['record_producer']=='root' and receipt['actual_tool_terminal_return_observed'] is True and receipt['record_written_after_actual_terminal_return'] is True
    assert receipt['transport_started'] is False and receipt['scientific_qualification'] is False
    assert receipt['source']==plan['formal_factory']
    assert rootobs['launch_command']==receipt['command'] and len(receipt['command'])==9
    assert rootobs['actual_execve_syscall_argv_trace'] is None
    app=owned_json(rootobs['app_actual_completed_command_execution'])
    admission=owned_json(rootobs['full_DECLARE_independent_admission'])
    assert admission['whole_scope_complementary_reports_pass'] is True and admission['graph_report_sha256']==PINS['/private/tmp/axmat_v9_actual_cold_DECLARE_graph_INPUT_resource_independent_review_20261009/REPORT.json']['sha256']
    for k in ('formal_factory','formal_consumer','formal_intake_binding'):pin(plan[k]['path'],plan[k]['sha256'])
    for record in rootobs['copied_pure_Root_provenance']:pin(record['path'],record['sha256'])
    termnames=sorted(p.name for p in term.iterdir());assert termnames==['declaration.stderr','declaration.stdout','declaration_terminal_return.json','prepare.stderr','prepare.stdout','prepare_terminal_return.json']
    for p in term.iterdir():pin(p)
    for k in ('full_stdout','full_stderr','prepared','input_declaration_terminal_evidence'):pin(receipt[k]['path'],receipt[k]['sha256'])
    assert PINS[receipt['full_stdout']['path']]['size']==365 and PINS[receipt['full_stderr']['path']]['size']==0
    prepared=owned_json(receipt['prepared']);assert receipt['prepared']['sha256']=='35f8100a753b149b6b100b8bc7154ca1b09f488a464a5068e0ffb826877d6ec7'
    stdout=owned_json(receipt['full_stdout']);assert stdout==dict(classification='PREPARED_NO_TRANSPORT',prepared=str(output/'prepared.json'),sha256=receipt['prepared']['sha256'])
    assert prepared['classification']=='PREPARED_NO_TRANSPORT' and 'own_child_supervision' not in prepared
    decl=read_json(source/'declaration.json','6d937be82fb66c21f110241bd2658a37b793bdaf098e19b7bb50b596c9cad00c')
    seal=read_json(source/'factory_seal.json','810f8b897d31d48128eda6a5349e3ff55c2d47c71695dab51db0055e4551d5ce')
    assert sorted(p.name for p in source.iterdir())==plan['expected_SOURCE_files']
    for name,sha in seal['files'].items():pin(source/name,sha)
    for path,record in prior['SOURCE31_pins'].items():assert identity(path)==record['identity']
    assert len(prepared['local_files'])==43
    currentlocal={str(p.relative_to(output)) for p in output.rglob('*') if p.is_file() and not p.is_symlink()}
    assert currentlocal==set(prepared['local_files'])|{'prepared.json'}
    for name,wanted in prepared['local_files'].items():
        assert not Path(name).is_absolute() and '..' not in Path(name).parts;pin(output/name,wanted)
    for k in ('cases','budgets','production_config','inputs','case_spec','rank_addendum','declaration','resource_roots'):
        expected=dict(path=str(source/'declaration.json'),sha256=PINS[str(source/'declaration.json')]['sha256']) if k=='declaration' else sorted_object_boundary(decl[k])
        assert typed_equal(prepared[k],expected),k
    assert prepared['budgets']==plan['original_budgets']
    m=owned_json(decl['rank1_factor_cache_revision']);case=owned_json(decl['case_spec']);storage=owned_json(decl['rank1_factor_cache_resource_admission'])
    intake=m['component_input_intake'];rawapi=owned_json(intake['api_return']);api=sorted_object_boundary(rawapi)
    assert len(api)==65 and typed_equal(case['rank1_factor_cache_trial']['actual_combined_runtime_admission'],api)
    assert digest(api)==prior['whole65_sha256'] and list(rawapi)==read_json('/private/tmp/axmat_v9_actual_bounded_INPUT_graph_descriptor_independent_review_20261009/complete_graph_and_whole_returned_INPUT_review.json','defdf82d849912f795fae8a8fea856bb20c475771cdb41d67a11ffe2a49f78f8')['field_names']
    specs=read_json(ROOT/'validation/axial_material/combined_runtime_complete_historical_input_specs_20261007.json',INPUT_SPECS_SHA)
    assert typed_equal(api['actual_components'],specs['metadata']['historical_actual_components']) and len(api['actual_components'])==7
    trim=owned_json(api['actual_last_cprime_trim_component_INPUT']);assert len(trim)==73 and digest(trim)==prior['whole_trim73_sha256']
    for key in ('AAA_accuracy_qualified','ABA_admitted','native_transport_executed','combined_runtime_native_RSS_proved','production_pipeline_prepared','trim_native_RSS_proof_obtained'):assert api[key] is False
    graphpath=Path(intake['complete_historical_input_graph']['path']);graph=read_json(graphpath,GRAPH_SHA)
    assert PINS[str(graphpath)]['size']==64644869<67108864 and graph['content_sha256']==WIRE_SHA
    wire=dict(graph);wire.pop('content_sha256');assert digest(wire)==WIRE_SHA
    assert independent_legacy_digest(graph)==graph['wire_encoding']['decoded_content_sha256']==LEGACY_SHA
    rows=0;rowhash=hashlib.sha256();previous=None;duplicates=0
    table=graph['requirements'];assert table['columns']==['path','canonical_path','owner','category','binding_role'] and table['duplicate_edges_retained'] is True
    for row in decode_rows(table):
        p,c,o,k,r=row;key=(table['paths'][c],table['owners'][o],table['paths'][p],table['categories'][k],table['binding_roles'][r]);assert previous is None or previous<=key
        duplicates+=previous==key;previous=key;rows+=1;rowhash.update(json.dumps(row,separators=(',',':')).encode()+b'\n')
    assert rows==235528 and rowhash.hexdigest()==prior['requirement_row_sha256']
    canonical={r['path']:r['sha256'] for r in graph['canonical_files']};assert len(canonical)==35647 and sum(r['size_bytes']for r in graph['canonical_files'])==35803098221
    beforecanon={p:identity(p) for p in canonical}
    assert digest(beforecanon)==prior['graph_beforeafter_canonical_identity_digest']
    for p,record in beforecanon.items():assert stat.S_ISREG(record[2]) and Path(p).resolve(strict=True)==Path(p)
    assert len(m['files'])==37339
    dependencybefore={}
    for p,wanted in m['files'].items():
        if p in canonical:assert canonical[p]==wanted;expected=beforecanon[p]
        else:
            old=prior['reviewed_pins'][p];assert old['sha256']==wanted;expected=old['identity']
        assert identity(p)==expected and Path(p).resolve(strict=True)==Path(p);dependencybefore[p]=expected
    for p,wanted in api['descriptor_files'].items():assert m['files'][p]==wanted
    assert len(api['descriptor_files'])==35675
    before_ns=[current_graph_namespace(row,canonical) for row in graph['namespaces']];assert len(before_ns)==86
    before_aliasabsence=aliases_and_absences(graph,canonical)
    roots=dynamic_roots(prepared['resource_roots'],ART)
    assert roots==prepared['resource_roots']==decl['resource_roots']==m['component_resource_roots']==storage['resource_roots']
    assert len(graph['live_resource_roots'])==231 and set(graph['live_resource_roots']).issubset(roots)
    for p in (source,output,term,control):assert str(p) in roots
    resbefore=resource_inventory(roots,ART);freebefore=shutil.disk_usage(ART).free
    reserve=storage['fresh_AAA_reserve_bytes'];assert reserve==20971764748==math.ceil(1.5*storage['original_complete_12_map_case_bytes'])+2**30
    assert storage['original_complete_12_map_case_bytes']==13265348616 and storage['unchanged_history_cap_bytes']==96*2**30 and storage['unchanged_min_free_bytes']==8*2**30
    assert resbefore['artifact_bytes']+reserve<96*2**30 and freebefore-reserve>=8*2**30
    print('ActualPREP inherited35GB fullBYTE proof + full35647 fresh identities validated; canonical payload content reads0',flush=True)
    # Repeat complete metadata boundaries to bind the full postreview window.
    assert before_ns==[current_graph_namespace(row,canonical) for row in graph['namespaces']]
    assert before_aliasabsence==aliases_and_absences(graph,canonical)
    assert beforecanon=={p:identity(p) for p in canonical}
    assert dependencybefore=={p:identity(p) for p in m['files']}
    resafter=resource_inventory(roots,ART);freeafter=shutil.disk_usage(ART).free
    assert resbefore==resafter and roots==dynamic_roots(prepared['resource_roots'],ART)
    assert resafter['artifact_bytes']+reserve<96*2**30 and freeafter-reserve>=8*2**30
    assert sorted(p.name for p in term.iterdir())==termnames and sorted(p.name for p in source.iterdir())==plan['expected_SOURCE_files']
    assert not os.path.lexists(control)
    for name in ('own_rss_binding.json','prepared_cold.json','binding_controls','AAA','ABA','training','archives','cold_source_failure.json','cold_closeout_seal.json'):assert not os.path.lexists(output/name),name
    for p,record in PINS.items():assert identity(p)==record['identity']
    result=dict(schema='AXMAT_V9_ACTUAL_COLD_PREP_COMPLETE_INHERITED_BYTES_FRESH_GRAPH_RESOURCE_POSTREVIEW_V1',status='PASS',scope='Full graph, whole65+7+73, prepared inputs/local43+prepared/streams, complete metadata identity and dynamic resources; complementary source/deck/control report still required for whole actualPREP admission.',
        actual_PREP_Root_tool=rootobs['actual_tool_result'],actual_success_recorder_tool=rootobs['actual_success_recorder_tool'],Root_observer=PINS[str(rdir/'Root_actual_V9_cold_prepare_tool_return.json')],actual_prepare_receipt=PINS[str(term/'prepare_terminal_return.json')],prepared=PINS[str(output/'prepared.json')],
        earlier_fullBYTE_proof=PINS['/private/tmp/axmat_v9_actual_cold_DECLARE_graph_INPUT_resource_independent_review_20261009/REPORT.json'],earlier_fullBYTE_true_tool=priorreceipt['actual_tool_result'],earlier_fullBYTE_35803098221_identity_exact_retained=True,
        fresh_canonical_payload_content_reads=0,canonical_files=35647,inherited_canonical_bytes=35803098221,complete_canonical_before_after_seven_field_identity_digest=digest(beforecanon),
        requirement_rows=rows,duplicate_requirement_rows=duplicates,requirement_row_sha256=rowhash.hexdigest(),graph_full_json_pin=PINS[str(graphpath)],graph64MiB_limit_retained=True,wire_content_sha256=WIRE_SHA,decoded_legacy_semantic_sha256=LEGACY_SHA,
        namespaces_before_after86=before_ns,aliases_absences_before_after=before_aliasabsence,full_metadata_dependency_count=37339,full_metadata_dependency_before_after_identity_digest=digest(dependencybefore),descriptor_union35675_retained=True,
        original_graph_all_owner_coverage_typed_schema_dtype_layout_trace_content_pins_unmodified=True,original_fullBYTE_read_trace_inherited_not_faked_new_byte_trace=True,
        whole65_complete_type_order_values_floatbits_equal=True,original_API_raw65_order_unchanged=True,consumer_strict_sorted_JSON_complete_materialization_boundary_exact=True,whole65_semantic_sha256=digest(api),whole7_semantic_sha256=digest(api['actual_components']),whole_trim73_semantic_sha256=digest(trim),
        prepared_original_cases_budgets_config_inputs_sources_descriptor_resource_fields_complete_equal=True,controller_dump_JSON_sorted_object_boundary_applied_to_full_declared_metadata=True,SOURCE31_fullSHA_and_identity_unchanged=True,new_OUTPUT43localfiles_plus_prepared44_full_SHA=True,terminal_exact6_fullSHA=True,full_stdout_bytes=365,full_stderr_bytes=0,
        declared_roots_count=len(prepared['resource_roots']),dynamic_current_roots_count=len(roots),current_resources_before=resbefore,current_resources_after=resafter,resource_before_after_complete_inventory_equal=True,disk_free_before=freebefore,disk_free_after=freeafter,
        history_budget_bytes=96*2**30,min_free_bytes=8*2**30,original_parent_case_bytes=13265348616,fresh_AAA_reserve_bytes=reserve,strict_reservation_gate_passed=True,historical_resources_counts_not_fixed_current_gate=True,
        actual_execve_syscall_argv_trace_saved=False,source_derived_handoff_separate_from_actual_observed_CLI=True,future_binding_controls_and_cold_outputs_absent=True,
        standardlib_readonly_only_no_business_or_graph_helper_import=True,project_formal_ART_written=False,only_TMP_evidence_written=True,elapsed_seconds=time.monotonic()-START,native_RSS_credit=False,AAA_accuracy_qualified=False,ABA_admitted=False,scientific_qualification=False,full_read_pins=PINS)
    with (TMP/'REPORT.json').open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:result[k]for k in ('status','canonical_files','inherited_canonical_bytes','fresh_canonical_payload_content_reads','requirement_rows','full_metadata_dependency_count','dynamic_current_roots_count','elapsed_seconds')},sort_keys=True),flush=True)

if __name__=='__main__':main()
