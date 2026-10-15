"""Pure source generation. Never import the candidate or any business module."""
import ast, hashlib, json
from pathlib import Path

D=Path('/private/tmp/axmat_v14_complete_environment_streaming_sha_helper_compatible_source_draft_20261010')
P=Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_source_factor_production.py')
O=D/'complete_environment_streaming_sha_helper_v14.py'
parent=P.read_text()
assert hashlib.sha256(parent.encode()).hexdigest()=='619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'
node=next(n for n in ast.parse(parent).body if isinstance(n,ast.FunctionDef)and n.name=='digest')
before=ast.get_source_segment(parent,node)
addition=r'''# V14 private full-content verifier source candidate. It grants no build,
# native RSS or science credit. Use only the normally pinned canonical module
# under validation/axial_material: the original ROOT expression is unchanged.
from contextlib import contextmanager as _env_stream_contextmanager
import stat as _env_stream_stat
import threading as _env_stream_threading

_ENV_STREAM_SOURCE_STATUS = 'UNREADY_SOURCE_ONLY_REQUIRES_ROOT_SOURCE_ADMISSION_AND_REAL_HELPER_CONTROLS'
_ENV_STREAM_BUFFER_BYTES = 4 * 2**20
_ENV_STREAM_ACTIVE_CONTEXT = None
_ENV_STREAM_SCOPE_LOCK = _env_stream_threading.Lock()


def _env_stream_identity7(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink,
            info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def _env_stream_directory_identity(info):
    # Directory timestamps/size/nlink can change when an unrelated child is
    # written. Bind resolution identity without inventing an immutable namespace.
    return (info.st_dev, info.st_ino, info.st_mode)


def _env_stream_absolute_literal(path, allow_relative=False, cwd=None):
    path = Path(path)
    if not path.is_absolute():
        if not allow_relative:
            raise ValueError('environment digest memo requires an absolute literal path')
        # Joining preserves '..'; do not resolve or abspath-fold the open key.
        path = Path(os.getcwd() if cwd is None else cwd) / path
    return str(path)


def _env_stream_path_snapshot(literal, require_regular=True):
    """Fresh full alias resolution, with every actual link hop independently bound."""
    path = Path(literal)
    if not path.is_absolute():
        raise ValueError('absolute literal snapshot required')
    resolved = str(path.resolve(strict=True))
    pending = list(path.parts[1:])
    current = Path('/')
    directories = [(str(current), _env_stream_directory_identity(os.lstat(current)))]
    links = []
    seen_link_states = set()
    while pending:
        part = pending.pop(0)
        if part in ('', '.'):
            continue
        if part == '..':
            current = current.parent
            continue
        candidate = current / part
        info = os.lstat(candidate)
        if _env_stream_stat.S_ISLNK(info.st_mode):
            link_text = os.readlink(candidate)
            link_id = _env_stream_identity7(info)
            # Strict resolution catches cycles even if a racing link grows the
            # pending path. Its result is observational, never the memo/open key.
            candidate.resolve(strict=True)
            if (_env_stream_identity7(os.lstat(candidate)) != link_id
                    or os.readlink(candidate) != link_text):
                raise ValueError('literal alias changed while its hop was observed')
            link_state = (str(candidate), tuple(pending))
            if link_state in seen_link_states:
                raise ValueError('cyclic literal alias chain')
            seen_link_states.add(link_state)
            links.append((str(candidate), link_id, link_text))
            target = Path(link_text)
            if target.is_absolute():
                current = Path('/')
                target_parts = list(target.parts[1:])
            else:
                target_parts = list(target.parts)
            pending = target_parts + pending
            continue
        if pending and not _env_stream_stat.S_ISDIR(info.st_mode):
            raise ValueError('literal path ancestor is not a directory')
        current = candidate
        if _env_stream_stat.S_ISDIR(info.st_mode):
            directories.append((str(current), _env_stream_directory_identity(info)))
    if str(current) != resolved:
        raise ValueError('complete literal and actual strict resolution differ')
    info = os.lstat(current)
    if require_regular and not _env_stream_stat.S_ISREG(info.st_mode):
        raise ValueError('full-content environment digest requires a regular target')
    target_identity = (_env_stream_directory_identity(info)
        if _env_stream_stat.S_ISDIR(info.st_mode) else _env_stream_identity7(info))
    return dict(literal=literal, target_path=str(current), target_identity=target_identity,
                target_mode=info.st_mode, ordinary_directory_bindings=tuple(directories),
                alias_hops=tuple(links))


def _env_stream_new_state(native_library_aliases=None):
    if native_library_aliases is None:
        native_library_aliases = {}
    if type(native_library_aliases) is not dict:
        raise ValueError('explicit native-library alias mapping required')
    cwd = os.getcwd()
    expected_aliases = dict(native_library_aliases)
    aliases = {}
    alias_observation_errors = {}
    for name, target in expected_aliases.items():
        try:
            literal = _env_stream_absolute_literal(name, allow_relative=True, cwd=cwd)
            aliases[name] = _env_stream_path_snapshot(literal, require_regular=False)
        except Exception as error:
            # Entry observes aliases but must not preempt the original verify
            # files-first error order. Normal environment/exit still refuses.
            alias_observation_errors[name] = (type(error).__name__, str(error))
    return dict(pid=os.getpid(), thread_id=_env_stream_threading.get_ident(), cwd=cwd, memo={},
                native_alias_expected=expected_aliases, native_alias_snapshots=aliases,
                native_alias_observation_errors=alias_observation_errors,
                buffer=None, view=None, active=True)


def _env_stream_owner(state):
    if (state['active'] is not True
            or state['pid'] != os.getpid()
            or state['thread_id'] != _env_stream_threading.get_ident()
            or state['cwd'] != os.getcwd()):
        raise ValueError('one unchanged-thread/cwd environment digest scope required')


def _env_stream_buffer(state):
    _env_stream_owner(state)
    if state['buffer'] is None:
        state['buffer'] = bytearray(_ENV_STREAM_BUFFER_BYTES)
        state['view'] = memoryview(state['buffer'])
    if len(state['buffer']) != _ENV_STREAM_BUFFER_BYTES:
        raise ValueError('one fixed four-MiB full-content buffer required')
    return state['buffer'], state['view']


def _env_stream_recheck(state):
    _env_stream_owner(state)
    for literal, entry in state['memo'].items():
        if _env_stream_path_snapshot(literal) != entry['snapshot']:
            raise ValueError('complete hashed input identity changed before environment exit')
    if state['native_alias_observation_errors']:
        raise ValueError('complete native alias entry observation failed; no environment may accept it')
    for name, original in state['native_alias_snapshots'].items():
        current = _env_stream_path_snapshot(_env_stream_absolute_literal(name, allow_relative=True, cwd=state['cwd']), require_regular=False)
        if (current != original
                or current['target_path'] != state['native_alias_expected'][name]):
            raise ValueError('complete declared native alias changed before environment exit')


def _env_stream_clear(state):
    try:
        if state['view'] is not None:
            state['view'].release()
    finally:
        state['view'] = None
        if state['buffer'] is not None:
            state['buffer'].clear()
        state['buffer'] = None
        state['memo'].clear()
        state['native_alias_snapshots'].clear()
        state['native_alias_observation_errors'].clear()
        state['native_alias_expected'].clear()
        state['active'] = False


@_env_stream_contextmanager
def complete_environment_digest_context(native_library_aliases=None):
    """Only same-literal repetitions inside this one explicit call may reuse SHA.

    A real factory must pass declaration['native_library_aliases'], including
    aliases that have no digest owner. The original environment body stays exact.
    No existing frozen helper global or supervisor class is patched.
    """
    global _ENV_STREAM_ACTIVE_CONTEXT
    if not _ENV_STREAM_SCOPE_LOCK.acquire(blocking=False):
        raise ValueError('nested or concurrent environment digest scopes are forbidden')
    state = None
    try:
        if _ENV_STREAM_ACTIVE_CONTEXT is not None:
            raise ValueError('environment context state must start empty')
        state = _env_stream_new_state(native_library_aliases)
        _ENV_STREAM_ACTIVE_CONTEXT = state
        yield
        _env_stream_recheck(state)
    finally:
        try:
            if state is not None:
                _env_stream_clear(state)
        finally:
            _ENV_STREAM_ACTIVE_CONTEXT = None
            _ENV_STREAM_SCOPE_LOCK.release()


def _env_stream_open(path):
    # A helper-only driver can locally instrument this new adapter, without
    # mutating Path.open or any frozen ancestor helper/global.
    return Path(path).open('rb', buffering=0)


def _env_stream_full_digest(path, state, memoize):
    _env_stream_owner(state)
    literal = _env_stream_absolute_literal(path, allow_relative=True, cwd=state['cwd'])
    snapshot = _env_stream_path_snapshot(literal)
    if memoize and literal in state['memo']:
        entry = state['memo'][literal]
        if snapshot != entry['snapshot']:
            raise ValueError('same-call literal identity drift forbids digest reuse')
        _env_stream_owner(state)
        return entry['sha256']
    digestobj = hashlib.sha256()
    total = 0
    # Keep the caller's actual Path open semantics, including allowed aliases
    # and symlink-dir/../file. Resolution is only an independent identity proof.
    with _env_stream_open(path) as stream:
        before = os.fstat(stream.fileno())
        if (not _env_stream_stat.S_ISREG(before.st_mode)
                or _env_stream_identity7(before) != snapshot['target_identity']):
            raise ValueError('actual opened descriptor differs from the complete path target')
        buffer, view = _env_stream_buffer(state)
        while True:
            count = stream.readinto(buffer)
            if type(count) is not int or not 0 <= count <= len(buffer):
                raise ValueError('full-content readinto returned an invalid byte count')
            if count == 0:
                break
            total += count
            digestobj.update(view[:count])
        after = os.fstat(stream.fileno())
        if (total != before.st_size
                or _env_stream_identity7(after) != _env_stream_identity7(before)
                or _env_stream_path_snapshot(literal) != snapshot):
            raise ValueError('complete EOF byte count or descriptor/path/alias identities drifted')
    _env_stream_owner(state)
    value = digestobj.hexdigest()
    if memoize:
        state['memo'][literal] = dict(snapshot=snapshot, sha256=value)
    return value


def digest(path):
    state = _ENV_STREAM_ACTIVE_CONTEXT
    if state is not None:
        return _env_stream_full_digest(path, state, memoize=True)
    if _ENV_STREAM_SCOPE_LOCK.locked():
        raise ValueError('environment digest context initialization is still active')
    # Outside an explicit environment scope keep the original fresh behavior.
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()
'''
assert parent.count(before)==1
candidate=parent.replace(before,addition.rstrip(),1)
ast.parse(candidate)
inverse=candidate.replace(addition.rstrip(),before,1)
assert inverse==parent
with O.open('x')as f:f.write(candidate)
proof=dict(schema='AXMAT_V14_COMPLETE_ENVIRONMENT_STREAM_SHA_HELPER_SOURCE_INVERSE_V1',
    parent=dict(path=str(P),sha256=hashlib.sha256(parent.encode()).hexdigest()),
    candidate=dict(path=str(O),sha256=hashlib.sha256(candidate.encode()).hexdigest()),
    regions=[dict(name='digest_and_new_private_context_stream_identity_support',before=before,after=addition.rstrip())],
    complete_inverse_byteexact=True,business_imported=False,business_executed=False,
    source_status='UNREADY_SOURCE_ONLY_REQUIRES_ROOT_SOURCE_ADMISSION_AND_REAL_HELPER_CONTROLS')
with (D/'source_complete_inverse_proof.json').open('x')as f:json.dump(proof,f,indent=2);f.write('\n')
print(json.dumps(dict(status='COMPLETE_PRIVATE_HELPER_SOURCE_ONLY_UNREADY',candidate_sha256=proof['candidate']['sha256'],
    region_count=1,complete_inverse_byteexact=True,business_executed=False)))
