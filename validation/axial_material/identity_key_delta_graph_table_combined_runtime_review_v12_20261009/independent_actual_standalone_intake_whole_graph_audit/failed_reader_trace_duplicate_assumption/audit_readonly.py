"""Independent stdlib whole-input graph/metadata audit. No business import or call.
Historical bytes are credited only to the recorded genuine isolated API phase;
this reviewer independently checks full mappings, codec, metadata and new endpoints.
"""
import ast,base64,collections,hashlib,json,math,os,shutil,stat,struct,time
from pathlib import Path
TMP=Path('/private/tmp/axmat_v12_actual_durable_whole_INPUT_graph_descriptor_independent_review_20261009')
ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts';AM=ROOT/'validation/axial_material'
R=AM/'identity_key_delta_graph_table_combined_runtime_review_v12_20261009'
A=ART/'axial-material-owned-specs-identity-key-delta-graph-table-v12-standalone-bounded-runtime-api-intake-evidence-20261009'
OUT=ART/'axial-material-owned-specs-identity-key-delta-graph-table-combined-runtime-v12-20261009'
TERM=ART/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-combined-terminal-v12-20261009'
F=AM/'prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.py'
G=AM/'combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py'
F_SHA='5af1feebc7d40549750e1daec6148ae073a4c85c1eb3242485e6d9e80826861b'
G_SHA='e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28'
API_SHA='65fc18ba1fab484b91c626a48d79a55a9bd5f21b65a391d18b9c4313e2333536'
GRAPH_SHA='4ba5f793ca13018d2d9ac5d29d76827a1503b0368c7e5c9f70ba08e0435f0c9e'
ROOT_SHA='449d08d08cdfe7cb19eaf3a882312f8d6c21725011650289608e4bae601178bf'
CATEGORIES=('code_environment','original92_build','memory_build','dedup_build','physical_build','capture','component_ancestry','component_terminals','source_namespace')
ROLES=('EXPECTED_INPUT_BYTES','OWNED_EXHAUSTIVE_NAMESPACE_BYTES','OWNED_EXHAUSTIVE_NAMESPACE_ALIAS_TARGET_BYTES','NEWLY_DECLARED_INPUT_ONLY')
PINS={};START=time.monotonic()
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
    assert type(codec['row_count']) is int and codec['row_count'] >= 0
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
    for path in map(Path,roots):
        visit(path)
    return dict(artifact_bytes=total,regular_files=regular,directories=directories,symlinks_ignored=symlinks_ignored,
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

def valid_sha(value):
    return type(value) is str and len(value)==64 and all(c in '0123456789abcdef' for c in value)

def resolve_declared(path, aliases, kind=None):
    assert type(path) is str and os.path.isabs(path) and os.path.normpath(path)==path
    current=Path('/');parts=list(Path(path).parts[1:]);seen=set()
    while parts:
        current=current/parts.pop(0);s=current.lstat()
        if stat.S_ISLNK(s.st_mode):
            key=str(current);assert key in aliases and key not in seen,key;seen.add(key)
            a=aliases[key];assert os.readlink(current)==a['text'],key
            target=os.path.normpath(os.path.join(str(current.parent),a['text']))
            actual=str(Path(target).resolve(strict=True));assert actual==a['target'],key
            current=Path(actual)
        if parts:assert current.is_dir(),str(current)
    if kind=='file':assert stat.S_ISREG(current.lstat().st_mode)
    if kind=='directory':assert stat.S_ISDIR(current.lstat().st_mode)
    assert not current.is_symlink()
    return str(current)

def scan_namespace(ns, aliases):
    root=Path(resolve_declared(ns['root'],aliases,'directory'))
    assert str(root)==ns['canonical_root']
    files=set();directories=set();links={};meta=[]
    for current,dirs,names in os.walk(root,followlinks=False):
        current=Path(current)
        for name in sorted(dirs+names):
            p=current/name;rel=str(p.relative_to(root));s=p.lstat();meta.append([rel,identity(p)])
            if stat.S_ISLNK(s.st_mode):links[rel]=os.readlink(p)
            elif stat.S_ISDIR(s.st_mode):directories.add(rel)
            else:assert stat.S_ISREG(s.st_mode);files.add(rel)
    assert files==set(ns['files']) and directories==set(ns['directories'])
    assert links=={k:v['text'] for k,v in ns['symlinks'].items()},ns['root']
    return digest([identity(root),sorted(meta)])

def absence_check(path, expected, aliases):
    parts=Path(path).parts[1:];current=Path('/');anc=[]
    def observed(p):
        s=p.lstat();return dict(device=s.st_dev,inode=s.st_ino,mode=s.st_mode,rdev=s.st_rdev,major=os.major(s.st_rdev),minor=os.minor(s.st_rdev))
    anc.append(dict(literal_component='/',canonical_path='/',identity=observed(current)))
    for i,part in enumerate(parts):
        p=current/part
        try:s=p.lstat()
        except FileNotFoundError:
            assert expected['first_missing_component']==str(p)
            assert expected['canonical_absent_path']==str(p.joinpath(*parts[i+1:]))
            assert expected['existing_ancestors']==anc and expected['missing_errno']==2
            assert expected['path']==path and expected['regular_input_bytes']==0
            assert expected['observation']=='EXACT_DECLARED_ENOENT_ONLY'
            assert expected['scope']=='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION'
            return
        assert i<len(parts)-1,path
        current=Path(resolve_declared(str(p),aliases,'directory'))
        anc.append(dict(literal_component='/'+'/'.join(parts[:i+1]),canonical_path=str(current),identity=observed(current)))
    raise AssertionError(('declared absence exists',path))

def graph_restore(storage):
    assert type(storage) is dict and set(storage)=={'schema','graph'}
    assert storage['schema']=='AXMAT_COMPLETE_INPUT_GRAPH_CANONICAL_FILE_TABLE_STORAGE_V1'
    g=storage['graph'];table=g['canonical_files']
    assert type(table) is dict and set(table)=={'columns','rows'}
    assert table['columns']==['path','sha256','size_bytes'] and type(table['rows']) is list
    pins=[]
    for i,row in enumerate(table['rows']):
        assert type(row) is list and len(row)==3 and type(row[0]) is str and valid_sha(row[1])
        assert type(row[2]) is int and row[2]>=0
        pins.append(dict(zip(table['columns'],row)));table['rows'][i]=None
    table['rows'].clear();g['canonical_files']=pins
    assert g['schema']=='AXMAT_COMBINED_RUNTIME_VERIFIED_INPUT_GRAPH_REQUIREMENTS_VARINT_WIRE_V1'
    assert g['consumer_scope'] is None and g['scope']=='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION'
    assert digest({k:v for k,v in g.items() if k!='content_sha256'})==g['content_sha256']
    assert independent_legacy_digest(g)==g['wire_encoding']['decoded_content_sha256']
    return g

def expand_owners(g):
    t=g['requirements'];o=g['owners'];names=t['owners']+o['extra_owner_names'];p=t['paths'];hashes=o['expected_sha256s'];pairs=o['expected_file_pins']
    assert o['schema']=='AXMAT_COMBINED_RUNTIME_COMPLETE_EXPECTED_OWNER_TABLE_V1'
    assert o['columns']==['owner','category','expected_file_pin_indices','optional_new_input_path_indices']
    assert o['duplicate_descriptors_retained'] is True and o['expected_hashes_come_from_typed_owners_not_observed_files'] is True
    assert hashes==sorted(set(hashes)) and all(valid_sha(h) for h in hashes)
    assert pairs==[list(x) for x in sorted(set(map(tuple,pairs)))]
    result=[];used=set();used_names=set()
    for row in o['rows']:
        assert type(row) is list and len(row) in (3,4)
        assert type(row[0]) is int and 0<=row[0]<len(names)
        assert type(row[1]) is int and 0<=row[1]<len(CATEGORIES)
        expected={};used_names.add(names[row[0]])
        for ix in row[2]:
            assert type(ix) is int and 0<=ix<len(pairs)
            pi,hi=pairs[ix];assert type(pi) is int and type(hi) is int and 0<=pi<len(p) and 0<=hi<len(hashes)
            assert p[pi] not in expected;expected[p[pi]]=hashes[hi];used.add(ix)
        owner=dict(owner=names[row[0]],category=CATEGORIES[row[1]],expected_files=expected)
        if len(row)==4:
            owner['newly_declared_input_paths']=[p[i] for i in row[3]]
            assert owner['newly_declared_input_paths']==sorted(set(owner['newly_declared_input_paths']))
        result.append(owner)
    assert used==set(range(len(pairs)))
    assert o['extra_owner_names']==sorted(used_names-set(t['owners']))
    assert set(hashes)=={h for owner in result for h in owner['expected_files'].values()}
    return result

def expected_rows(g,owners,aliases):
    for owner in owners:
        for path,sha in owner['expected_files'].items():
            yield (path,resolve_declared(path,aliases,'file'),owner['owner'],owner['category'],ROLES[0],sha)
    for ns in g['namespaces']:
        for rel,sha in ns['files'].items():
            path=os.path.join(ns['root'],rel);yield(path,resolve_declared(path,aliases,'file'),ns['owner'],ns['category'],ROLES[1],sha)
        for rel,link in ns['symlinks'].items():
            if link['kind']=='file' and 'sha256' in link:
                path=os.path.join(ns['root'],rel);yield(path,resolve_declared(path,aliases,'file'),ns['owner'],ns['category'],ROLES[2],link['sha256'])
    for path,value in g['newly_declared_input_paths'].items():
        yield(path,resolve_declared(path,aliases,'file'),value['owner'],value['category'],ROLES[3],g['newly_declared_input_pins'][path])
    for owner in owners:
        for path in owner.get('newly_declared_input_paths',[]):
            yield(path,resolve_declared(path,aliases,'file'),owner['owner'],owner['category'],ROLES[3],g['newly_declared_input_pins'][path])

def graph_check(g):
    assert g['closure_categories']==list(CATEGORIES)
    for key in ('science_qualification_created','live_resources_verified','external_declaration_exit0_verified'):assert g[key] is False
    assert g['fresh_reader_contract']['max_json_bytes']==67108864
    assert g['fresh_reader_contract']['canonical_union_fresh_bytes_required_every_phase'] is True
    assert g['read_trace']['coverage']=='PYTHON_AUDIT_OPEN_ATTEMPTS_ONLY'
    t=g['requirements'];assert t['columns']==['path','canonical_path','owner','category','binding_role']
    assert t['categories']==list(CATEGORIES) and t['binding_roles']==list(ROLES)
    assert t['paths']==sorted(set(t['paths'])) and t['owners']==sorted(set(t['owners']))
    aliases={a['path']:a for a in g['aliases']};assert len(aliases)==len(g['aliases'])
    for a in aliases.values():assert resolve_declared(a['path'],aliases,a['kind'])==a['target']
    ns_before={n['root']:scan_namespace(n,aliases) for n in g['namespaces']}
    for path,v in g['absence_inputs'].items():
        assert v['binding_role']=='NEWLY_DECLARED_ABSENCE_INPUT_ONLY'
        absence_check(path,g['absence_observations'][path],aliases)
    owners=expand_owners(g);expected_counts=collections.Counter();expected_sha={}
    for wanted in expected_rows(g,owners,aliases):
        edge=wanted[:5];expected_counts[edge]+=1
        assert edge not in expected_sha or expected_sha[edge]==wanted[5];expected_sha[edge]=wanted[5]
    canonical={r['path']:r for r in g['canonical_files']}
    assert list(canonical)==sorted(canonical) and len(canonical)==len(g['canonical_files'])
    union={};category_paths={c:set() for c in CATEGORIES};category_names={c:set() for c in CATEGORIES}
    row_hash=hashlib.sha256();role_counts=collections.Counter();literal={};count=0;previous=None
    for indices in decode_rows(t):
        row=(t['paths'][indices[0]],t['paths'][indices[1]],t['owners'][indices[2]],t['categories'][indices[3]],t['binding_roles'][indices[4]])
        assert expected_counts[row]>0,('requirement row mismatch',count);expected_counts[row]-=1
        order=(row[1],row[2],row[0],row[3],row[4]);assert previous is None or previous<=order;previous=order
        sha=expected_sha[row];assert row[1] in canonical and canonical[row[1]]['sha256']==sha
        assert row[1] not in union or union[row[1]]==sha;union[row[1]]=sha
        literal[row[0]]=row[1];category_paths[row[3]].add(row[1]);category_names[row[3]].add(row[2]);role_counts[row[4]]+=1
        row_hash.update(json.dumps(indices,separators=(',',':')).encode()+b'\n');count+=1
    assert all(v==0 for v in expected_counts.values()) and set(union)==set(canonical)
    assert t['paths']==sorted(set(literal)|set(literal.values()))
    coverage={c:dict(canonical_files=len(category_paths[c]),bytes=sum(canonical[p]['size_bytes'] for p in category_paths[c]),owners=sorted(category_names[c])) for c in CATEGORIES}
    assert coverage==g['coverage']
    roots=g['live_resource_roots'];trace=g['read_trace'];assert trace['subprocess_records']==[] and g['live_io_requirements']==[]
    counts={k:0 for k in g['trace_coverage']};counts['unique_records']=len(trace['records']);seen=set()
    for r in trace['records']:
        assert r['kind']=='path' and r['access']=='read' and type(r['attempt_count']) is int and r['attempt_count']>0
        rid=json.dumps({k:v for k,v in r.items() if k!='attempt_count'},sort_keys=True,separators=(',',':'));assert rid not in seen;seen.add(rid)
        n=r['attempt_count'];counts['actual_read_open_attempts']+=n;p=r['path']
        if p in g['absence_inputs']:
            assert not r['flags']&(os.O_CREAT|os.O_TRUNC|os.O_APPEND|os.O_EXCL|os.O_DIRECTORY);counts['explicit_declared_absent_file_attempts']+=n;continue
        try:q=resolve_declared(p,aliases);mode=Path(q).lstat().st_mode
        except FileNotFoundError:
            assert r['flags']&os.O_DIRECTORY and any(p==root or p.startswith(root+'/') for root in roots)
            counts['explicit_live_resource_directory_attempts']+=n;continue
        if stat.S_ISREG(mode):assert q in canonical;counts['owned_file_attempts']+=n
        elif stat.S_ISDIR(mode):
            if any(q==root or q.startswith(root+'/') for root in ns_before):counts['owned_namespace_directory_attempts']+=n
            else:assert any(p==root or p.startswith(root+'/') for root in roots);counts['explicit_live_resource_directory_attempts']+=n
        else:raise AssertionError(('unowned trace',p))
    assert counts==g['trace_coverage']
    return aliases,ns_before,canonical,dict(requirement_rows=count,row_sequence_sha256=row_hash.hexdigest(),role_counts=dict(role_counts),owner_descriptors=len(owners),coverage_sha256=digest(coverage),trace_coverage=counts)

def namespace_tree(path):
    files={};dirs=[];links={}
    for current,folders,names in os.walk(path,followlinks=False):
        current=Path(current)
        if current!=path:dirs.append(str(current.relative_to(path)))
        for name in folders+names:
            p=current/name
            if p.is_symlink():links[str(p.relative_to(path))]=os.readlink(p)
        for name in names:
            p=current/name
            if not p.is_symlink():files[str(p.relative_to(path))]=identity(p)
    return dict(files=files,symlinks=links,directories=sorted(dirs))

def main():
    root=read_json(A/'Root_terminal_return.json',ROOT_SHA)
    assert root['actual_tool']==dict(initial_chunk_id='3900c7',session_id=49432,terminal_chunk_id='bbe76b',exit_code=0)
    assert type(root['actual_exit_code']) is int and root['actual_exit_code']==0
    assert root['record_written_after_actual_tool_return'] is True and root['actual_bounded_runtime_input_admission_observed'] is True
    actual=namespace_tree(A);pv=root['payload_inventory'];assert set(pv)=={'files','symlinks','directories'}
    assert len(pv['files'])==9 and len(actual['files'])==10 and set(actual['files'])==set(pv['files'])|{'Root_terminal_return.json'}
    assert actual['symlinks']==pv['symlinks']=={} and actual['directories']==sorted(pv['directories'])
    assert set(root['source_payload_pins'])==set(pv['files'])
    for name,sha in pv['files'].items():
        pin(A/name,sha);sp=root['source_payload_pins'][name];pin(sp['path'],sp['sha256']);assert sp['sha256']==sha
    assert sum(actual['files'][name][3] for name in pv['files'])==root['payload_bytes']==26415645
    for key in ('host_source','host_stdout','host_stderr','actual_host_result','whole_API_return','actual_watchdog','actual_stage_records'):
        d=root[key];pin(d['path'],d['sha256'])
    tool=read_json(R/'Root_actual_standalone_host_tool_terminal_input.json','0f61ab74d2f038ae6bb33a379b29555871a70ae5fe3c72779ed83702b661a6a3')
    assert type(tool['actual_tool_result']['exit_code']) is int and tool['actual_tool_result']['exit_code']==0 and tool['actual_tool_result']['chunk_id']=='bbe76b'
    assert tool['actual_initial_tool_result']['session_id']==49432
    obs=read_json(R/'Root_actual_standalone_host_tool_terminal_return.json');assert obs['actual_host_success_observed'] is True and obs['actual_closed_session_id']==49432
    recorder=read_json(R/'Root_actual_standalone_postterminal_recorder_tool_return.json');assert type(recorder['returncode']) is int and recorder['returncode']==0
    assert recorder['actual_tool_terminal_return_observed'] is True
    host=read_json(A/'result.json');stdout=read_json(A/'host.stdout');assert typed_equal(host,stdout)
    assert (A/'host.stderr').stat().st_size==0
    stages=read_json(A/'STANDALONE_BOUNDED_RUNTIME_API_INTAKE/stages.json')['stages'];watch=read_json(A/'intake/admit.watchdog.json')
    assert typed_equal(stages,json.loads(json.dumps(host['stage_records'],sort_keys=True,allow_nan=False))) and len(stages)==1 and typed_equal(watch,host['watchdog'])
    cmd=root['actual_API_command'];assert cmd==host['actual_command']==watch['command']==stages[0]['command']
    assert len(cmd)==9 and cmd[1]==str(F) and cmd[2]=='admit'
    assert stages[0]['status']=='PASS' and stages[0]['label']=='intake/admit' and stages[0]['log_sha256']==API_SHA
    assert type(watch['returncode']) is int and watch['returncode']==0 and watch['limit_failure'] is None
    assert watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True
    assert type(watch['pid']) is int and watch['pid']>0 and watch['sampled_peak_rss_mib']==498.75<512
    assert 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600
    assert host['whole_elapsed_seconds']==root['whole_elapsed_seconds']==53.15720783296274<1800
    for k,v in dict(total_wall_cap_seconds=1800,stage_wall_cap_seconds=600,RSS_cap_mib=512,threads=1,children_at_once=1,retries=0).items():assert root[k]==host[k]==v
    for k in ('cold_controller_imported','cold_controller_bound','cold_prepared','physics_or_native_transport_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted'):assert root[k] is host[k] is False
    assert root['child_stderr_combined_into_actual_log'] is host['child_stderr_combined_into_actual_log'] is True
    assert root['separate_child_stderr_observation_claimed'] is host['separate_child_stderr_observation_claimed'] is False
    pin(F,F_SHA);pin(G,G_SHA)
    body=read_json(A/'intake/admit.log',API_SHA);assert len(body)==65
    assert pin(R/'admit.stdout.json')['sha256']==API_SHA
    decl=read_json(OUT/'declaration.json','410720642a1952480ad9190ed48292e96cf9f17d8ab02967b5503713caa09f5d')
    seal=read_json(OUT/'seal.json','1f0ddf9751140abc2eb114918695b33007725cd34839e278b2e4b04f9c779dfa')
    run=read_json(TERM/'terminal_return.json','396697c31e8112040b7fab32f452e5fabd8592ec41379d3daf2eda1519df7b28')
    prep=read_json(TERM/'declaration_terminal_return.json','f431490002fb5e2d4de0cee17979c5ef5b5725740f16fea85fdcfd3fd502ddb5')
    graph=graph_restore(read_json(OUT/'input_graph.json',GRAPH_SHA));assert PINS[str(OUT/'input_graph.json')]['size']<67108864
    assert body['historical_input_graph']==decl['input_graph']
    assert graph['typed_snapshot']['actual_last_cprime_trim_component_INPUT']==body['actual_last_cprime_trim_component_INPUT']
    assert graph['typed_snapshot']['historical_whole_component_body']==body['historical_whole_component_body']
    assert graph['typed_snapshot']['original_component_APIs_executed_now'] is False and graph['typed_snapshot']['failed_historical_combined_RUN_promoted'] is False
    aliases,ns_before,canonical,graphproof=graph_check(graph)
    expected=dict(decl['files'])
    def add(p,h):
        p=str(p);assert valid_sha(h) and (p not in expected or expected[p]==h);expected[p]=h
    for name,h in seal['files'].items():add(OUT/name,h)
    add(OUT/'seal.json',cmd[4]);add(TERM/'terminal_return.json',cmd[8]);add(OUT/'input_graph.json',GRAPH_SHA)
    for k in ('full_stdout','full_stderr'):add(run[k]['path'],run[k]['sha256'])
    add(TERM/'declaration_terminal_return.json',body['actual_prepare_terminal_evidence']['sha256'])
    for k in ('source_inventory','full_stdout','full_stderr'):add(prep[k]['path'],prep[k]['sha256'])
    assert body['descriptor_files']==expected and len(expected)==36804
    assert set(decl['files'])==set(canonical) and all(decl['files'][p]==r['sha256'] for p,r in canonical.items())
    assert body['input_aliases']=={p:{k:v for k,v in a.items() if k!='path'} for p,a in aliases.items()}
    endpoints={p:identity(p) for p in expected};assert all(stat.S_ISREG(i[2]) for i in endpoints.values())
    assert all(endpoints[p][3]==r['size_bytes'] for p,r in canonical.items())
    # Only supplemental endpoints are read here. The recorded genuine API's
    # complete fresh phase, not reviewer stat values, supplies historical SHA.
    extras=set(expected)-set(canonical)
    for p in sorted(extras):pin(p,expected[p])
    declared=graph['live_resource_roots'];current=dynamic_roots(declared,ART)
    before=resource_inventory(current,ART);free_before=shutil.disk_usage(ART).free
    for resource in [host['resources_before'],host['resources_after'],stages[0]['resource_before'],stages[0]['resource_after']]:
        assert resource['declared_resource_roots']==decl['resource_roots']
        assert set(declared)<=set(resource['resource_roots']) and resource['artifact_budget_bytes']==96*2**30 and resource['min_free_bytes']==8*2**30
        assert resource['artifact_bytes']<96*2**30 and resource['disk_free_bytes']>=8*2**30
    after=resource_inventory(current,ART);free_after=shutil.disk_usage(ART).free
    assert before==after and current==dynamic_roots(declared,ART)
    assert before['artifact_bytes']+2*2**30<96*2**30 and min(free_before,free_after)-2*2**30>=8*2**30
    for p,i in endpoints.items():assert identity(p)==i,p
    assert ns_before=={n['root']:scan_namespace(n,aliases) for n in graph['namespaces']}
    for path in graph['absence_inputs']:absence_check(path,graph['absence_observations'][path],aliases)
    for a in aliases.values():assert resolve_declared(a['path'],aliases,a['kind'])==a['target']
    assert namespace_tree(A)==actual
    for p,r in PINS.items():assert identity(p)==r['identity'],p
    phase_function=next(n for n in ast.parse(F.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='complete_input_phase')
    phase_source=ast.get_source_segment(F.read_text(),phase_function)
    assert 'verify_graph' in phase_source and 'graph_input_bindings' in phase_source
    report=dict(schema='AXMAT_V12_ACTUAL_DURABLE_WHOLE_INPUT_GRAPH_DESCRIPTOR_READONLY_REVIEW_V1',status='PASS_GRAPH_DESCRIPTOR_DURABLE_SCOPE_ONLY',
        actual_Root_receipt=PINS[str(A/'Root_terminal_return.json')],actual_host_tool_int0_closed=True,actual_postrecorder_int0_closed=True,
        durable_payload_files=9,durable_total_files=10,durable_directories=3,payload_bytes=26415645,exact_namespace_and_source_payload_pins=True,
        whole_API_pin=PINS[str(A/'intake/admit.log')],whole_API_field_count=65,host_stdout_entire_JSON_equals_result=True,host_stderr_bytes=0,
        actual_stage_count=1,actual_watchdog=watch,whole_elapsed_seconds=host['whole_elapsed_seconds'],original_caps_unchanged=True,
        descriptor_count=len(expected),descriptor_map_sha256=digest(expected),descriptor_identity_sequence_sha256=digest(endpoints),all_descriptor_seven_identities_stable=True,
        canonical_count=len(canonical),canonical_logical_bytes=sum(r['size_bytes'] for r in canonical.values()),historical_canonical_bytes_rehashed_by_this_reader=False,
        historical_byte_authority='Actual isolated canonical F12 complete_input_phase -> genuine verify_graph/_phase under successful watched CLI; independent full owner/descriptor/namespace metadata reconciliation here.',
        metadata_checks_are_not_a_second_business_phase=True,additional_descriptor_endpoints_fresh_full_SHA_count=len(extras),additional_descriptor_paths=sorted(extras),
        namespace_count=len(graph['namespaces']),alias_count=len(aliases),absence_count=len(graph['absence_inputs']),graph_proof=graphproof,
        graph_pin=PINS[str(OUT/'input_graph.json')],stored_bytes=PINS[str(OUT/'input_graph.json')]['size'],original_read_bound_bytes=67108864,
        decoded_wire_content_sha256=graph['content_sha256'],decoded_legacy_semantic_sha256=graph['wire_encoding']['decoded_content_sha256'],
        declared_resource_root_count=len(declared),declared_roots_sha256=digest(declared),current_resource_root_count=len(current),current_roots_sha256=digest(current),
        full_dynamic_resource_inventory_before=before,full_dynamic_resource_inventory_after=after,free_before=free_before,free_after=free_after,
        historical_resource_filecount_not_used_as_current_requirement=True,current_root_meta_stable=True,
        scope_requires_complementary_whole65_7INPUT_30counts_SOURCE_fullbody_review=True,
        business_imports_or_calls=False,project_written=False,files_deleted=0,cold_prepared=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,
        all_small_full_SHA_pins=PINS,audit_source_pin=pin(__file__),elapsed_seconds=time.monotonic()-START)
    with (TMP/'REPORT.json').open('x') as stream:json.dump(report,stream,ensure_ascii=False,indent=2,allow_nan=False)
    print(json.dumps(dict(status=report['status'],canonical=len(canonical),descriptors=len(expected),requirements=graphproof['requirement_rows'],report=str(TMP/'REPORT.json'),sha256=hashlib.sha256((TMP/'REPORT.json').read_bytes()).hexdigest())))

if __name__=='__main__':main()
