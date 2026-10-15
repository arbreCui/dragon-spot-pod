# Pure read-only actual-binding graph/independent expected-owner union review.
# No producer or graph helper import; no API/constructor/phase invocation.
import ast, base64, copy, hashlib, json, math, os, stat, shutil, struct, time
from pathlib import Path
TMP = Path('/private/tmp/axmat_v9_actual_controls_graph_resource_scope_20261009')
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

def own_peak(w):
    required={'pid','returncode','sampled_peak_rss_mib','limit_failure','rss_cap_mib','own_pid_wait4_observed','own_pid_wait4_pid','own_pid_wait4_status','own_pid_wait4_ru_maxrss_bytes','own_pid_wait4_peak_rss_mib','observed_peak_rss_mib','live_rss_sample_count','rss_peak_observation_contract'}
    assert required.issubset(w) and w['rss_peak_observation_contract']=='EXACT_OWN_PID_DARWIN_WAIT4_BYTES_AND_LIVE_PS_V1'
    assert type(w['pid'])is int and w['pid']>0 and type(w['returncode'])is int and type(w['own_pid_wait4_observed'])is bool and w['rss_cap_mib']==512
    sampled=w['sampled_peak_rss_mib'];observed=w['observed_peak_rss_mib'];count=w['live_rss_sample_count'];kernel=w['own_pid_wait4_peak_rss_mib']
    assert all(type(v)in(int,float)and math.isfinite(v)and v>=0 for v in(sampled,observed))
    assert type(count)is int and count>=0 and (count!=0 or sampled==0)
    if w['own_pid_wait4_observed']:
        pid=w['own_pid_wait4_pid'];status=w['own_pid_wait4_status'];raw=w['own_pid_wait4_ru_maxrss_bytes']
        assert type(pid)is int and pid==w['pid'] and type(status)is int and 0<=status<=65535
        assert os.WIFEXITED(status)or os.WIFSIGNALED(status)
        assert os.waitstatus_to_exitcode(status)==w['returncode']
        assert type(raw)in(int,float)and math.isfinite(raw)and raw>0 and raw==int(raw)
        assert type(kernel)in(int,float)and math.isfinite(kernel)and kernel>0 and kernel==raw/(1024.*1024.)
    else:
        assert all(w[k]is None for k in('own_pid_wait4_pid','own_pid_wait4_status','own_pid_wait4_ru_maxrss_bytes','own_pid_wait4_peak_rss_mib'))
    assert observed==max(sampled,kernel if kernel is not None else 0.)
    if w['limit_failure']is None:assert w['returncode']==0 and w['own_pid_wait4_observed']is True and 0<observed<512
    else:assert w['limit_failure']=="RuntimeError('own-child 512 MiB RSS cap reached')"and w['returncode']in(-15,-9)and sampled>=512 and observed>=512
    return dict(pid=w['pid'],sampled_peak_rss_mib=sampled,kernel_peak_rss_mib=kernel,observed_peak_rss_mib=observed,live_sample_count=count,real_wait4_observed=w['own_pid_wait4_observed'],returncode=w['returncode'])

def main():
    plan=read_json(TMP/'PLAN.json','8655d07cb974d12b87b7b838e8c897adc73ba313fbab379f9c183df42913bb10')
    assert all(v is None for v in plan['future_actual'].values())
    baseplan=read_json('/private/tmp/axmat_v9_cold_actual_DECLARE_readonly_scope_plan_20261009/PLAN.json','59781ef14365a7b17d37d3992eeaf7bc7fd1967c249ad7a381e103e12a41ce52')
    source=Path(baseplan['source_root']);work=Path(plan['work_root']);term=Path(baseplan['declaration_terminal_root']);ct=Path(plan['control_terminal_root']);cr=Path(plan['controls_root'])
    G=Path('/private/tmp/axmat_v9_actual_cold_binding_graph_resource_independent_review_20261009')
    prior=read_json(G/'REPORT.json','03ebde650f63e045ae7a35f1018e02f787aac47fef28812a9a7a7fd719760e3c')
    priorreceipt=read_json(G/'actual_readonly_tool_return.json','34075c6b3c6f0e4197ab6e5ea93bd16b615ca25a3b38f6b57af87b6d8edaa1dd')
    assert prior['status']=='PASS'and priorreceipt['actual_tool_result']==dict(initial_chunk_id='9a9803',session_id=71255,terminal_chunk_id='c050ac',exit_code=0,closed=True)
    for path,row in prior['full_read_pins'].items():assert identity(path)==row['identity'],path
    rdir=ROOT/'validation/axial_material/last_cprime_trim_combined_live_resource_v9_build_review_20261009'
    obs=read_json(rdir/'Root_actual_V9_cold_controls_tool_return.json','f37d6f364d520c3f789dd71791d81f1f1e3e414dbfa3b6f88efa9c44439adfa1')
    tool=dict(initial_chunk_id='085698',session_id=92301,terminal_chunk_id='5c78de',exit_code=0)
    assert obs['actual_tool_result']==dict(tool,closed=True)and type(obs['actual_tool_result']['exit_code'])is int
    assert obs['actual_success_recorder_tool']==dict(chunk_id='0b84d1',exit_code=0,closed=True)
    rootbinding=owned_json(obs['qualified_complete_binding_admission']);assert obs['qualified_complete_binding_admission']['sha256']=='ae1577974abf75e738a3e74cc682ac3449ff3239ae617e1494dbeabeef33b726'
    for p in obs['copied_pure_Root_provenance']:pin(p['path'],p['sha256'])
    receipt=read_json(ct/'terminal_return.json','04f61e9377d468730ffd06cd3b511240d48ee881c5177b548c3b86e754c1747e')
    assert receipt['actual_tool_result']==tool and type(receipt['returncode'])is int and receipt['returncode']==0
    assert receipt['record_producer']=='root'and receipt['actual_tool_terminal_return_observed']is True and receipt['record_written_after_actual_terminal_return']is True
    assert receipt['scientific_qualification']is False and receipt['transport_started']is False
    assert sorted(p.name for p in ct.iterdir())==['controls.stderr','controls.stdout','terminal_return.json']
    stdout=owned_json(receipt['full_stdout']);pin(receipt['full_stderr']['path'],receipt['full_stderr']['sha256'])
    assert PINS[receipt['full_stdout']['path']]['size']==136307 and PINS[receipt['full_stderr']['path']]['size']==0
    binding=read_json(work/'own_rss_binding.json','4e8de93043fa08ac0c6e1f1702b69606a6bf0b155c30007c356ec4837919c930')
    assert receipt['binding']==dict(path=str(work/'own_rss_binding.json'),sha256=PINS[str(work/'own_rss_binding.json')]['sha256'])
    assert receipt['source']==binding['controls_source']and receipt['host']==binding['host']
    assert receipt['command']==[binding['producer_environment']['executable'],binding['controls_source']['path'],'run-controls','--binding',receipt['binding']['path'],'--binding-sha256',receipt['binding']['sha256']]
    assert receipt['command']==obs['source_derived_handoff_command']and obs['actual_execve_syscall_trace']is None
    for item in (plan['exact_actual_runtime_host'],plan['exact_actual_runtime_controls']):pin(item['path'],item['sha256'])
    seal=read_json(cr/'seal.json','339f8385c45e4a196dba39cc4c6bf0753acbdc13953179456630bc6735a9f746')
    assert receipt['control_seal']==dict(path=str(cr/'seal.json'),sha256=PINS[str(cr/'seal.json')]['sha256'])
    control_names=[];control_dirs=[];control_before={}
    for base,dirs,names in os.walk(cr,followlinks=False):
        assert not any((Path(base)/n).is_symlink()for n in dirs+names)
        for name in dirs:control_dirs.append(str((Path(base)/name).relative_to(cr)))
        for name in names:control_names.append(str((Path(base)/name).relative_to(cr)))
    assert sorted(control_names)==sorted(plan['expected_success_control_namespace']['files'])and sorted(control_dirs)==seal['namespace_directories']==['oversize','positive','short']
    assert set(control_names)==set(seal['files'])|{'seal.json'}and len(seal['files'])==9
    for name,wanted in seal['files'].items():control_before[name]=pin(cr/name,wanted)
    control_before['seal.json']=PINS[str(cr/'seal.json')]
    result=read_json(cr/'result.json',obs['actual_result_file']['sha256']);claim=read_json(cr/'claim.json',seal['files']['claim.json']);stages=read_json(cr/'stages.json',seal['files']['stages.json'])['stages']
    assert claim['binding']==receipt['binding']and claim['retries']==0 and claim['scientific_qualification']is False
    assert result['classification']=='PASS_NEW_CANONICAL_OWN_RSS_BINDING_CONTROLS_ONLY'and result['binding']==receipt['binding']and result['caps']==binding['caps']
    tail={k:stdout[k]for k in('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')}
    assert typed_equal(stdout,sorted_object_boundary(dict(result=result,**tail)))
    for k,v in tail.items():assert typed_equal(receipt[k],v)
    assert tail['actual_tail_check']=='PASS'and result['elapsed_before_closeout']<=tail['actual_elapsed_seconds']==91.97639445803361<120
    assert [o['mode']for o in result['observations']]==['positive','oversize','short']
    assert [s['label']for s in stages]==plan['expected_success_stages']['order']and [s['status']for s in stages]==['PASS','FAILED','PASS']
    watchsummaries=[]
    for stage,observation in zip(stages,result['observations']):
        mode=observation['mode'];command=[binding['producer_environment']['executable'],binding['controls_source']['path'],'fixture',mode]
        w=owned_json(observation['watchdog']);logpin=pin(observation['raw_log']['path'],observation['raw_log']['sha256'])
        assert observation['watchdog']['path']==str(cr/mode/'execute.watchdog.json')and logpin['path']==str(cr/mode/'execute.log')
        assert typed_equal(w,observation['watch'])and command==stage['command']==w['command']==observation['command']
        assert w['own_child_only']is True and w['liveness_group_cleanup']is True and observation['actual_group_no_longer_live']is True
        assert 0<w['wall_cap_seconds']<=stage['wall_cap_seconds']<=60 and 0<=w['elapsed_seconds']<w['wall_cap_seconds']
        peak=own_peak(w);peak['mode']=mode;watchsummaries.append(peak)
        rawlines=Path(logpin['path']).read_text().splitlines();assert rawlines
        assert json.loads(rawlines[0])==dict(kind='ACTUAL_OWN_CHILD_ALLOCATION_INTENT',mode=mode,pid=w['pid'],requested_bytes=(576 if mode=='oversize' else 16)*2**20)
        if mode in('positive','short'):
            assert stage['status']=='PASS'and observation['actual_expected_rejection']is None and stage['log_sha256']==logpin['sha256']
            assert 'POSITIVE_NEW_CANONICAL_OWN_CHILD_CONTROL_COMPLETE'in rawlines
            if mode=='short':assert w['own_pid_wait4_observed']is True and w['own_pid_wait4_peak_rss_mib']>=16
        else:assert stage['status']=='FAILED'and stage['error']==observation['actual_expected_rejection']=='own-child 512 MiB RSS cap reached'
    assert watchsummaries[1]['kernel_peak_rss_mib']is None and watchsummaries[2]['live_sample_count']==0 and watchsummaries[2]['kernel_peak_rss_mib']==36.75
    for k in('scientific_qualification','Dragon_started','transport_started','new_assembly_or_linear_solve','AAA_accuracy_qualified','ABA_admitted'):assert result[k]is False
    # Immutable whole binding/canonical/source fields remain complete.
    source_seal=read_json(source/'factory_seal.json','810f8b897d31d48128eda6a5349e3ff55c2d47c71695dab51db0055e4551d5ce')
    prepared=read_json(work/'prepared.json','35f8100a753b149b6b100b8bc7154ca1b09f488a464a5068e0ffb826877d6ec7')
    m=read_json(source/'rank1_factor_cache_admission.json',source_seal['files']['rank1_factor_cache_admission.json'])
    expected=dict(m['files']);expected.update(prior['additional_expected_files'])
    assert len(expected)==37395 and digest(expected)==prior['expected_files_whole_sha256']and typed_equal(binding['files'],expected)
    assert str(work/'own_rss_binding.json')not in expected and not any(str(cr/n)in expected for n in control_names)
    rawapi=owned_json(m['component_input_intake']['api_return']);api=sorted_object_boundary(rawapi);trim=owned_json(api['actual_last_cprime_trim_component_INPUT'])
    original7=api['actual_components'];expectedreturns=dict(original92=original7['original92'],memory438=original7['dedup']['inherited_rank1_factor_cache_memory_admission'],physical=original7['physical'],dedup=original7['dedup'],capture=original7['capture'],combined=api,last_cprime_trim=api['actual_last_cprime_trim_admission'])
    assert typed_equal(binding['actual_component_returns'],expectedreturns)and len(api)==65 and len(original7)==7 and len(trim)==73
    assert digest(api)==prior['whole65_semantic_sha256']and digest(trim)==prior['whole_trim73_semantic_sha256']
    assert len(binding['module_owners'])==391 and all(expected[r['path']]==r['sha256']for r in binding['module_owners'].values())
    graphpath=m['component_input_intake']['complete_historical_input_graph']['path'];graph=read_json(graphpath,GRAPH_SHA)
    assert PINS[graphpath]['size']==64644869<67108864 and graph['content_sha256']==WIRE_SHA
    wire=dict(graph);wire.pop('content_sha256');assert digest(wire)==WIRE_SHA and independent_legacy_digest(graph)==LEGACY_SHA
    rowhash=hashlib.sha256();rowcount=0
    for row in decode_rows(graph['requirements']):rowhash.update(json.dumps(row,separators=(',',':')).encode()+b'\n');rowcount+=1
    assert rowcount==235528 and rowhash.hexdigest()==prior['requirement_row_sha256']
    canonical={r['path']:r['sha256']for r in graph['canonical_files']};beforecanon={p:identity(p)for p in canonical}
    assert len(canonical)==35647 and digest(beforecanon)==prior['complete_canonical_before_after_seven_field_identity_digest']
    oldfull=read_json('/private/tmp/axmat_v9_actual_cold_DECLARE_graph_INPUT_resource_independent_review_20261009/REPORT.json','31f29c1b5642ad86d980623363a29cb15f19c2f7094bb95a4fa6393e2651f8d0')
    deps={}
    for p,wanted in m['files'].items():
        old=beforecanon[p]if p in canonical else oldfull['reviewed_pins'][p]['identity']
        assert wanted==(canonical[p]if p in canonical else oldfull['reviewed_pins'][p]['sha256'])and identity(p)==old
        deps[p]=old
    assert len(deps)==37339 and digest(deps)==prior['metadata_before_after_identity_digest']
    before_ns=[current_graph_namespace(r,canonical)for r in graph['namespaces']];before_aa=aliases_and_absences(graph,canonical)
    assert len(before_ns)==86 and len(api['descriptor_files'])==35675
    for p,wanted in api['descriptor_files'].items():assert expected[p]==wanted
    assert sorted(p.name for p in source.iterdir())==baseplan['expected_SOURCE_files']
    assert sorted(p.name for p in term.iterdir())==sorted([phase+suffix for phase in('declaration','prepare','binding')for suffix in('.stdout','.stderr','_terminal_return.json')])
    currentlocal={str(p.relative_to(work))for p in work.rglob('*')if p.is_file()and not p.is_symlink()}
    assert currentlocal==set(prepared['local_files'])|{'prepared.json','own_rss_binding.json'}|{'binding_controls/'+n for n in control_names}
    for name,wanted in prepared['local_files'].items():pin(work/name,wanted)
    # Distinct real epochs: result-snapshot before result/seal, tail after seal,
    # current inventory after Root CT3 addition. Never freeze historical count.
    roots=dynamic_roots(prepared['resource_roots'],ART);assert roots==prepared['resource_roots']==binding['resource_info']['resource_roots']and len(roots)==236
    assert len(graph['live_resource_roots'])==231 and set(graph['live_resource_roots']).issubset(roots)
    before=resource_inventory(roots,ART);freebefore=shutil.disk_usage(ART).free
    for epoch in(result['actual_resource_snapshot'],tail['actual_resources']):
        assert epoch['declared_resource_roots']==epoch['resource_roots']==roots
        assert epoch['artifact_budget_bytes']==96*2**30 and epoch['min_free_bytes']==8*2**30 and epoch['artifact_bytes']<96*2**30 and epoch['disk_free_bytes']>=8*2**30
        assert epoch['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'and 'reason'not in epoch
    before_result=result['actual_resource_snapshot'];after_seal=tail['actual_resources']
    result_and_seal=PINS[str(cr/'result.json')]['size']+PINS[str(cr/'seal.json')]['size']
    assert after_seal['artifact_bytes']-before_result['artifact_bytes']==result_and_seal and after_seal['regular_files']-before_result['regular_files']==2
    ctbytes=sum(p.stat().st_size for p in ct.iterdir());assert before['artifact_bytes']-after_seal['artifact_bytes']==ctbytes and before['regular_files']-after_seal['regular_files']==3
    controltreebytes=sum(r['size']for r in control_before.values())
    archive=controltreebytes+PINS[binding['host']['path']]['size']+PINS[binding['controls_source']['path']]['size']+PINS[str(work/'own_rss_binding.json')]['size']
    assert archive==tail['actual_archive_bytes']==61047970<64*2**20
    assert before['artifact_bytes']+20971764748<96*2**30 and freebefore-20971764748>=8*2**30
    print('Complete controls seal10/CT3, strict ownwait4, inherited canonical35647 identities and independent expected37395 union validated',flush=True)
    assert before_ns==[current_graph_namespace(r,canonical)for r in graph['namespaces']]
    assert before_aa==aliases_and_absences(graph,canonical)
    assert beforecanon=={p:identity(p)for p in canonical}and deps=={p:identity(p)for p in m['files']}
    after=resource_inventory(roots,ART);freeafter=shutil.disk_usage(ART).free
    assert before==after and roots==dynamic_roots(prepared['resource_roots'],ART)
    assert after['artifact_bytes']+20971764748<96*2**30 and freeafter-20971764748>=8*2**30
    for path,row in prior['full_read_pins'].items():assert identity(path)==row['identity']
    for path,row in PINS.items():assert identity(path)==row['identity']
    for name in('prepared_cold.json','AAA','ABA','training','archives','cold_source_failure.json','cold_closeout_seal.json'):assert not os.path.lexists(work/name)
    report=dict(schema='AXMAT_V9_ACTUAL_CONTROLS_COMPLETE_GRAPH_EXPECTED_OWNER_NAMESPACE_SEAL_RESOURCE_POSTREVIEW_V1',status='PASS',scope='Full graph/expected-owner union/immutable body/namespace/control-seal/resource temporal accounting; source/MRO/originalCode/env/provenance peer report remains required for whole control admission.',
        actual_Root_controls_tool=obs['actual_tool_result'],actual_Root_success_recorder_tool=obs['actual_success_recorder_tool'],actual_Root_observer=PINS[str(rdir/'Root_actual_V9_cold_controls_tool_return.json')],actual_control_terminal=PINS[str(ct/'terminal_return.json')],actual_control_seal=PINS[str(cr/'seal.json')],qualified_complete_binding_admission=PINS[obs['qualified_complete_binding_admission']['path']],inherited_complete_binding_graph_report=PINS[str(G/'REPORT.json')],inherited_true_graph_reader_tool=priorreceipt['actual_tool_result'],
        controls_exact_namespace_files=control_names,controls_exact_namespace_directories=sorted(control_dirs),controls_complete_seal9_plus_self_fullSHA=True,controls_result_stages3_and_complete_raw_logs_watch_fields=True,actual_stage_statuses=['PASS','FAILED','PASS'],actual_own_PID_peak_summaries=watchsummaries,short_genuine_wait4_kernel_at_least16MiB=True,oversize_actual_kernel_fields_retained_None_not_fabricated=True,normal_completion_missing_kernel_fields_never_defaulted_to0=True,
        canonical_files=35647,inherited_full_canonical_bytes=35803098221,new_canonical_payload_bytes_read=0,canonical_full_seven_field_beforeafter_digest=digest(beforecanon),requirement_rows235528=rowcount,requirement_row_sha256=rowhash.hexdigest(),graph_whole_pin=PINS[graphpath],all_graph_schema_typed_owners_dtype_layout_trace_content_retained=True,namespaces86_beforeafter=before_ns,aliases186_absences445_beforeafter=before_aa,metadata37339_beforeafter_identity_digest=digest(deps),descriptor_union35675_unchanged=True,
        full_expected_ownerunion37395_independent_proof_inherited_and_whole_source_map_current_equal=True,expected_map_sha256=digest(expected),module391_all_independent_expected_and_current_source_identities_preserved=True,whole65_original7_trim73_new7_complete_type_order_floatbits_equal=True,new_control_endpoints_separate_seal_not_backfilled_into_binding_map=True,binding_self_file_entry_absent=True,
        SOURCE31_OUTPUT45_base_TERM9_whole_original_byte_identity_unchanged=True,only_control_tree10_and_CT3_added=True,original_runtime31_flat_and_declared_sources_unchanged=True,
        resource_epochs=dict(result_snapshot_before_result_and_seal=dict(artifact_bytes=before_result['artifact_bytes'],regular_files=before_result['regular_files'],checked_unix=before_result['checked_unix']),after_seal_before_Root_CT=dict(artifact_bytes=after_seal['artifact_bytes'],regular_files=after_seal['regular_files'],checked_unix=after_seal['checked_unix']),Root_CT_added_exact_bytes=ctbytes,result_and_seal_added_exact_bytes=result_and_seal,current_postRoot_inventory=after),
        exact_archive_bytes=archive,archive_control_tree_bytes=controltreebytes,archive_host_controls_binding_exact_source_rule=True,all4_actual_tail_fields_complete_and_original_caps_pass=True,actual_elapsed_seconds=tail['actual_elapsed_seconds'],history_budget_bytes=96*2**30,min_free_bytes=8*2**30,control_archive_limit_bytes=64*2**20,whole_seconds=120,stage_seconds=60,rss_cap_mib=512,declared_dynamic_roots=236,original231_roots_retained=True,resource_beforeafter_complete_inventory_equal=True,resource_before=before,resource_after=after,disk_free_before=freebefore,disk_free_after=freeafter,original_future_AAA_reserve_bytes=20971764748,strong_future_AAA_reserve_gate_passed=True,old_filecounts_not_frozen_future_gate=True,
        source_derived_handoff_not_actual_execve_syscall_trace=True,future_prepared_cold_native_AAA_ABA_outputs_absent=True,business_or_graph_helper_imported=False,business_phase_API_constructor_or_native_executed=False,project_written=False,only_TMP_evidence_written=True,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,scientific_qualification=False,elapsed_seconds=time.monotonic()-START,full_read_pins=PINS)
    with(TMP/'REPORT.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(status='PASS',control_files=10,CT_files=3,canonical_files=35647,canonical_payload_read=0,expected_files=37395,rows=235528,current_resource_bytes=after['artifact_bytes'],current_resource_files=after['regular_files'],elapsed_seconds=report['elapsed_seconds']),sort_keys=True),flush=True)

if __name__=='__main__':main()
