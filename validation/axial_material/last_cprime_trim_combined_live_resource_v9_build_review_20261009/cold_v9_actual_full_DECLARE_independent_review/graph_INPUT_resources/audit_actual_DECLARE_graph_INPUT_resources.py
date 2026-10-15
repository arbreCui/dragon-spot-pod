# Pure read-only metadata review. Never imports/calls the producer/business API.
# This module is prepared before terminal recording; actual_input_binding.json
# remains absent until Root provides true closed host zero + saved payload pins.
import ast, base64, copy, hashlib, importlib.util, json, math, os, stat, shutil, struct, time
from pathlib import Path
TMP = Path('/private/tmp/axmat_v9_actual_cold_DECLARE_graph_INPUT_resource_independent_review_20261009')
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

def own_json(item):
    return read_json(item['path'],item['sha256'])

def check_namespace(item):
    root=Path(item['root']); expected=item['inventory']; files={}; links={}; dirs=[]
    assert root.resolve(strict=True)==root
    for base,foldernames,filenames in os.walk(root,followlinks=False):
        base=Path(base)
        for name in foldernames[:]:
            p=base/name; rel=str(p.relative_to(root))
            if p.is_symlink(): links[rel]=os.readlink(p); foldernames.remove(name)
            else: dirs.append(rel)
        for name in filenames:
            p=base/name; rel=str(p.relative_to(root))
            if p.is_symlink(): links[rel]=os.readlink(p)
            else:
                wanted=expected['files'][rel]
                if str(p) not in PINS: pin(p,wanted)
                assert PINS[str(p)]['sha256']==wanted
                files[rel]=wanted
    assert files==expected['files'] and links==expected['symlinks'] and sorted(dirs)==expected['directories']
    return dict(root=str(root),files=len(files),directories=len(dirs),symlinks=len(links),inventory_sha256=digest(expected))

def main():
    plan=read_json('/private/tmp/axmat_v9_cold_actual_DECLARE_readonly_scope_plan_20261009/PLAN.json','59781ef14365a7b17d37d3992eeaf7bc7fd1967c249ad7a381e103e12a41ce52')
    source=Path(plan['source_root']); output=Path(plan['future_output_root']); control=Path(plan['future_control_terminal_root'])
    coldterm=Path(plan['declaration_terminal_root'])
    for k in ('formal_factory','formal_consumer','formal_intake_binding'): pin(plan[k]['path'],plan[k]['sha256'])
    assert not os.path.lexists(output) and not os.path.lexists(control)
    observation_path=ROOT/'validation/axial_material/last_cprime_trim_combined_live_resource_v9_build_review_20261009/Root_actual_V9_cold_declare_tool_return.json'
    observation=read_json(observation_path)
    receipt=read_json(coldterm/'declaration_terminal_return.json','d0ba07a475355ec69aefc933cdbde49ab88b71b689d6b8e8c796b18ad44cd73c')
    actual=receipt['actual_tool_result']
    assert actual==observation['actual_tool_result']==dict(closed=True,exit_code=0,initial_chunk_id='25de2d',session_id=18187,terminal_chunk_id='de668b')
    assert type(actual['exit_code']) is int and type(receipt['returncode']) is int and receipt['returncode']==0
    assert receipt['record_producer']=='root' and receipt['record_written_after_actual_terminal_return'] is True and receipt['actual_tool_terminal_return_observed'] is True
    assert receipt['scientific_qualification'] is False and receipt['transport_started'] is False
    assert receipt['source']==plan['formal_factory']
    for key in ('declaration','factory_seal','source_equivalence','full_stdout','full_stderr'): pin(receipt[key]['path'],receipt[key]['sha256'])
    assert PINS[receipt['full_stderr']['path']]['size']==0
    stdout=read_json(receipt['full_stdout']['path'],receipt['full_stdout']['sha256'])
    assert stdout['classification']=='DECLARED_COMBINED_PHYSICAL_DEDUP_FILE_SNAPSHOT_COLD_INPUT_ONLY'
    assert stdout['declaration']==receipt['declaration'] and stdout['factory_seal']==receipt['factory_seal']
    decl=own_json(receipt['declaration']); seal=own_json(receipt['factory_seal'])
    assert seal['schema']=='AXMAT_COMBINED_PHYSICAL_DEDUP_FILE_SNAPSHOT_COLD_FACTORY_SEAL_V1'
    assert sorted(p.name for p in source.iterdir())==plan['expected_SOURCE_files']
    assert set(seal['files'])==set(plan['expected_SOURCE_files'])-{'factory_seal.json'}
    for name,wanted in seal['files'].items(): pin(source/name,wanted)
    source_pins={str(p):PINS[str(p)] for p in source.iterdir()}
    env=read_json(source/'analysis_environment.json')
    assert receipt['command']==[env['executable'],plan['formal_factory']['path'],'declare','--factory-sha256',plan['formal_factory']['sha256']]
    m=own_json(decl['rank1_factor_cache_revision']); specbody=own_json(decl['case_spec'])
    assert m['whole_component_return_encoding']=='COMPLETE_EXTERNAL_API_JSON_POINTER_MATERIALIZED_AFTER_FRESH_GRAPH'
    assert m['component_API_reexecution_in_cold_process'] is False and m['whole_component_returns_preserved'] is True
    intake=m['component_input_intake']; rawapi=own_json(intake['api_return'])
    # The actual consumer's unchanged strict_json uses _unique_sorted_object.
    # Reproduce that complete JSON serialization boundary with stdlib only.
    api=json.loads(json.dumps(rawapi,sort_keys=True,allow_nan=False))
    assert m['whole_component_body_source']==intake['api_return']
    assert len(api)==65 and typed_equal(specbody['rank1_factor_cache_trial']['actual_combined_runtime_admission'],api)
    assert digest(api)=='3507c79c48e3470ad1171cf351959a793bddc7e7e0668275001f24f8d7de3377'
    joint=read_json('/private/tmp/axmat_v9_actual_whole_INPUT_joint_scope_binding_review_20261009/REPORT.json','c6fd4d225d4de4ca82149e20af13143f5a593ac67479453f9d696dc07ed11fda')
    assert joint['status']=='PASS'
    jointreceipt=read_json('/private/tmp/axmat_v9_actual_whole_INPUT_joint_scope_binding_review_20261009/actual_readonly_tool_return.json','8be8a730b272ff6853f43678a6e42c36506ea8eed4bb1232333aee4cd97b9e4a')
    # Original immutable source proof and genuine tool receipts are preserved;
    # current checks below are fresh readonly observations, not that old phase.
    sourceproof=read_json('/private/tmp/spot_v9_actual_bound_INPUT_source_witness_math_independent_review_20261009/REPORT.json','c19a572f913f06339e6d8fdb16d143f15eab3b2aa2ae5268e77335b7562a4147')
    assert sourceproof['status']=='PASS'
    sourcereceipt=read_json('/private/tmp/spot_v9_actual_bound_INPUT_source_witness_math_independent_review_20261009/actual_readonly_tool_return.json','d73ea46c5ac23bbe664aba1a80098ca694a4ca7a3bc32431d9a8dd61091a8b78')
    graphproof=read_json('/private/tmp/axmat_v9_actual_bounded_INPUT_graph_descriptor_independent_review_20261009/complete_graph_and_whole_returned_INPUT_review.json','defdf82d849912f795fae8a8fea856bb20c475771cdb41d67a11ffe2a49f78f8')
    assert list(rawapi)==graphproof['field_names']
    specs=read_json(ROOT/'validation/axial_material/combined_runtime_complete_historical_input_specs_20261007.json',INPUT_SPECS_SHA)
    seven=specs['metadata']['historical_actual_components']
    assert len(seven)==7 and typed_equal(api['actual_components'],seven)
    assert digest(seven)=='a0b0445e79f91f5d3767ee57719937a5188608f6a22f77d62b17c5036950e130'
    trim=own_json(api['actual_last_cprime_trim_component_INPUT'])
    assert len(trim)==73 and digest(trim)=='4a2c2026b0571bd5fa4b147d547d27f056421d77f838c8ac7c2855c68941fcdd'
    for k in ('AAA_accuracy_qualified','ABA_admitted','native_transport_executed','combined_runtime_native_RSS_proved','production_pipeline_prepared','trim_native_RSS_proof_obtained','original_component_APIs_executed_now'):
        assert api[k] is False
    assert m['input_aliases']==api['input_aliases']
    for item in intake['helper_sources'].values(): pin(item['path'],item['sha256'])
    for path,wanted in intake['intake_proof_files'].items(): pin(path,wanted)
    intake_ns=[check_namespace(item) for item in intake['intake_namespaces']]
    graphitem=intake['complete_historical_input_graph']; graphpath=Path(graphitem['path'])
    graph=read_json(graphpath,GRAPH_SHA)
    assert graphitem['sha256']==GRAPH_SHA and graphitem['content_sha256']==WIRE_SHA
    assert PINS[str(graphpath)]['size']==64644869<67108864
    wire=dict(graph); wire.pop('content_sha256'); assert digest(wire)==graph['content_sha256']==WIRE_SHA
    assert independent_legacy_digest(graph)==graph['wire_encoding']['decoded_content_sha256']==LEGACY_SHA
    rows=0; duplicates=0; previous=None; rowhash=hashlib.sha256(); roles={}; categories={}
    table=graph['requirements']
    assert table['columns']==['path','canonical_path','owner','category','binding_role'] and table['duplicate_edges_retained'] is True
    for row in decode_rows(table):
        p,c,o,k,r=row; key=(table['paths'][c],table['owners'][o],table['paths'][p],table['categories'][k],table['binding_roles'][r])
        assert previous is None or previous<=key
        duplicates+=previous==key; previous=key; rows+=1
        rowhash.update(json.dumps(row,separators=(',',':')).encode()+b'\n')
        roles[table['binding_roles'][r]]=roles.get(table['binding_roles'][r],0)+1
        categories[table['categories'][k]]=categories.get(table['categories'][k],0)+1
    assert rows==235528
    canonical={r['path']:r['sha256'] for r in graph['canonical_files']}
    assert len(canonical)==35647
    assert set(canonical).issubset(api['descriptor_files']) and len(api['descriptor_files'])==35675
    for path,wanted in api['descriptor_files'].items(): assert m['files'][path]==wanted
    for path,wanted in canonical.items(): assert m['files'][path]==wanted
    aliases={r['path']:{k:v for k,v in r.items() if k!='path'} for r in graph['aliases']}
    assert len(aliases)==186 and typed_equal(aliases,api['input_aliases'])
    assert len(graph['namespaces'])==86 and len(graph['absence_inputs'])==445 and len(graph['live_resource_roots'])==231
    beforecanonical={path:identity(path) for path in canonical}
    storage=own_json(decl['rank1_factor_cache_resource_admission'])
    assert typed_equal(decl['resource_roots'],m['component_resource_roots']) and typed_equal(decl['resource_roots'],storage['resource_roots'])
    currentroots=dynamic_roots(decl['resource_roots'],ART)
    assert currentroots==decl['resource_roots'] and set(graph['live_resource_roots']).issubset(currentroots)
    for p in (source,output,coldterm,control): assert str(p) in currentroots
    resourcebefore=resource_inventory(currentroots,ART); freebefore=shutil.disk_usage(ART).free
    reserve=storage['fresh_AAA_reserve_bytes']; parentbytes=storage['original_complete_12_map_case_bytes']
    assert parentbytes==13265348616 and reserve==20971764748==math.ceil(1.5*parentbytes)+2**30
    assert storage['unchanged_history_cap_bytes']==96*2**30 and storage['unchanged_min_free_bytes']==8*2**30
    assert resourcebefore['artifact_bytes']+reserve<96*2**30 and freebefore-reserve>=8*2**30
    assert storage['forecast_bytes']==storage['resources_before']['artifact_bytes']+reserve
    assert storage['original_case_budgets']==decl['budgets']==plan['original_budgets']
    old=ART/'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005'
    derivedparent=sum(p.stat().st_size for p in old.rglob('*') if p.is_file() and not p.is_symlink())
    assert derivedparent==parentbytes
    pin(ROOT/'validation/axial_material/prepare_qualified_AB_moment_order_production.py','fe81150fbf270cac44e241ad64f352cf2f623fa65f7ccb4a9b0ded0a4f2c2d41')
    print('Independent actualDECLARE fullgraph begins; roots',len(currentroots),'current regular',resourcebefore['regular_files'],flush=True)
    pin(HELPER,HELPER_SHA)
    hs=importlib.util.spec_from_file_location('independent_reviewed_input_metadata_graph',HELPER); module=importlib.util.module_from_spec(hs); hs.loader.exec_module(module)
    assert module.MAX_JSON_BYTES==67108864 and module.CONSUMER_PHASES==()
    streams=dict(files=0,bytes=0); streamhash=hashlib.sha256(); originalstream=module._stream
    def fresh_stream(*args,**kwargs):
        record,payload=originalstream(*args,**kwargs);streams['files']+=1;streams['bytes']+=record['size_bytes']
        streamhash.update(json.dumps(record,sort_keys=True,separators=(',',':')).encode()+b'\n')
        if streams['files']%5000==0: print('Full canonical fresh reads',streams['files'],flush=True)
        return record,payload
    module._stream=fresh_stream
    verified=module.verify_graph(str(graphpath),expected_sha256=GRAPH_SHA,phase='independent_actual_V9_cold_DECLARE_full_metadata_postcheck_not_original_phase_trace')
    assert verified['classification']=='FRESH_INPUT_BYTES_NAMESPACES_ALIASES_VERIFIED_ONLY'
    for k,want in [('canonical_files_read',35647),('actual_bytes_read',35803098221),('logical_owner_requirements',235528),('exhaustive_namespaces_checked',86),('explicit_aliases_checked',186),('declared_absence_inputs_checked_before_and_after_bytes',445)]: assert verified[k]==want
    assert typed_equal(verified['typed_snapshot'],graph['typed_snapshot'])
    for k in ('live_subprocesses_reexecuted','science_qualification_created','live_resources_verified','external_declaration_exit0_verified'): assert verified[k] is False
    assert streams==dict(files=35648,bytes=35803098221+64644869)
    for path,wanted in m['files'].items():
        if path in canonical: continue
        if path in PINS: assert PINS[path]['sha256']==wanted
        else: pin(path,wanted)
    print('All metadata dependency endpoints checked',len(m['files']),'additional',len(set(m['files'])-set(canonical)),flush=True)
    assert beforecanonical=={path:identity(path) for path in canonical}
    resourceafter=resource_inventory(currentroots,ART); freeafter=shutil.disk_usage(ART).free
    assert resourcebefore==resourceafter and currentroots==dynamic_roots(decl['resource_roots'],ART)
    assert resourceafter['artifact_bytes']+reserve<96*2**30 and freeafter-reserve>=8*2**30
    assert not os.path.lexists(output) and not os.path.lexists(control)
    assert sorted(p.name for p in source.iterdir())==plan['expected_SOURCE_files']
    for path,record in PINS.items(): assert identity(path)==record['identity'],path
    result=dict(schema='AXMAT_V9_ACTUAL_COLD_DECLARE_COMPLETE_GRAPH_WHOLE_INPUT_RESOURCE_POSTREVIEW_V1',status='PASS',scope='Actual DECLARE whole INPUT, complete graph/all metadata endpoints/dynamic resources. SOURCE/inverse/env/parent metadata complementary peer report required before whole DECLARE admission.',
      actual_declare_tool=actual,actual_declare_receipt=PINS[str(coldterm/'declaration_terminal_return.json')],Root_observation=PINS[str(observation_path)],
      SOURCE31_full_SHA_identity_before_after=True,SOURCE31_pins=source_pins,
      whole65_all_builtin_fields_type_insertion_order_float64_bits_and_values_equal=True,whole65_sha256=digest(api),whole7_sha256=digest(seven),whole_trim73_sha256=digest(trim),
      unchanged_API_raw_original65_field_order_bound_to_prior_full_source_proof=True,consumer_strict_JSON_full_recursive_sorted_object_order_materialization_boundary_reproduced=True,case_spec_complete65_sorted_materialization_exact_all_types_order_values_floatbits=True,
      preserved_first_reader_failure='first_reader_587a53_exit1/actual_tool_return.json',first_reader_failure_was_crossfile_raw_API_insertion_vs_strict_JSON_sorted_materialization_order_not_changed_business=True,
      previous_complete_INPUT_source_proof=PINS['/private/tmp/spot_v9_actual_bound_INPUT_source_witness_math_independent_review_20261009/REPORT.json'],previous_complete_INPUT_joint=PINS['/private/tmp/axmat_v9_actual_whole_INPUT_joint_scope_binding_review_20261009/REPORT.json'],
      canonical_count=35647,canonical_bytes=35803098221,logical_requirement_rows=rows,duplicate_requirement_rows=duplicates,requirement_row_sha256=rowhash.hexdigest(),requirement_role_counts=roles,requirement_category_counts=categories,
      graph_pin=PINS[str(graphpath)],graph_wire_content_sha256=WIRE_SHA,decoded_legacy_content_sha256=LEGACY_SHA,graph_limit_bytes=67108864,graph_limit_retained=True,
      graph_namespaces86_aliases186_absences445_before_after=True,returned_descriptor_union_count=len(api['descriptor_files']),compact_metadata_dependency_count=len(m['files']),additional_dependency_count=len(set(m['files'])-set(canonical)),all_dependency_full_SHA=True,
      full_puremetadata_graph_verification={k:v for k,v in verified.items() if k!='typed_snapshot'},fresh_canonical_sequence_sha256=streamhash.hexdigest(),streams=streams,
      graph_beforeafter_canonical_identity_digest=digest(beforecanonical),intake_namespace_postcheck=intake_ns,
      declared_resource_count=len(decl['resource_roots']),current_dynamic_resource_count=len(currentroots),current_dynamic_resources_before=resourcebefore,current_dynamic_resources_after=resourceafter,resources_metadata_before_after_equal=True,
      resource_disk_free_bytes_before=freebefore,resource_disk_free_bytes_after=freeafter,original_parent_case_bytes_derived=derivedparent,fresh_reserve_bytes=reserve,history_budget_bytes=96*2**30,free_floor_bytes=8*2**30,
      original_DECLARE_transient_phase_trace_durably_saved=False,independent_graph_trace_is_postterminal_not_original_DECLARE_trace=True,old_resources_filecount_not_fixed_current_gate=True,
      reviewed_pins=PINS,readonly_review_elapsed_seconds=time.monotonic()-START,only_TMP_evidence_written=True,business_factory_consumer_API_PREP_RUN_native_called=False,prepare_output_absent=True,new_controls_absent=True,
      native_RSS_credit=False,AAA_accuracy_qualified=False,ABA_admitted=False,scientific_qualification=False)
    with (TMP/'REPORT.json').open('x') as stream: json.dump(result,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps({k:result[k] for k in ('status','canonical_count','canonical_bytes','logical_requirement_rows','compact_metadata_dependency_count','declared_resource_count','current_dynamic_resource_count','readonly_review_elapsed_seconds')},sort_keys=True),flush=True)

if __name__=='__main__': main()
