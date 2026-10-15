"""All-370-group read-only audit of the current sealed rank-one axial operator.

No FLU, transport, linear solve, replay, CE fitting, or group selection occurs.
Raw operands are losslessly archived and checked before any floating-point gate.
Derived rank-one tensors describe the existing local operator only. Saved Pn
moments are not used to invent a 32-direction solution or the internal slot-7
source. The original convergence loops chiefly test P0; this audit adds no
higher-moment convergence or accuracy qualification.
"""
import argparse
import ast
from array import array
from contextlib import contextmanager
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import platform
import re
import shutil
import struct
import sys
import time
import zlib

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
SOURCE = ART / 'axial-material-rank1-cache-axial-operator-audit-admission-20261007'
OUT = ART / 'axial-material-rank1-cache-axial-operator-audit-20261007'
TERMINAL = ART / 'axial-material-rank1-cache-axial-operator-audit-terminal-20261007'
PROD = ART / 'axial-material-production-qualified-AB-rank1-factor-cache-20261007'
FINAL = PROD / 'AAA/map012'
BUILD = ART / 'axial-material-rank1-factor-cache-build-20261007'
BUILD_SOURCE = ART / 'axial-material-qualified-AB-rank1-factor-cache-build-admission-20261007'
BUILDER = ROOT / 'validation/axial_material/prepare_qualified_AB_rank1_cache_production.py'
FULL_FACTORY = ROOT / 'validation/axial_material/qualify_refined_AAA_layered_full.py'
READER = PROD / 'runtime/snapshot_control_preflight.py'
PYTHON = Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python')
PYTHON_SHA = 'ba725dca52e02b5382d6acf3e6ac92afb0d65662f1ce8820d75a59a095490860'
BUILDER_SHA = '92d73658e349ea2b2816b2b770549ca22378c2595f2c9e5c9331bbf91c6abf8a'
FULL_FACTORY_SHA = '70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'
PREPARED_SHA = '7d2154e9c722eab23f4411c9a8588ed8250da658ae880298c24dfb53308656b5'
STATUS_SHA = '03b68ebd59c7bfff9eca8f02961e1ae528bf4debf815dd23ae0d0a2cdf03051d'
CONTROLLER_SHA = '844fe18738a2232d2947a8c65dc13afebcfbfd2e2afc9f0743c1c94c06fd0f7d'
READER_SHA = 'f60309e54947de8dc43e7080fd19ca6255652d840493db23b37ff7003c6a0819'
FINAL_SEAL_SHA = '64293bc1022a44d3cbf5e738bf1b79f4f2aa7b8958d572a59cc8c2b3ca968d59'
BUILD_SEAL_SHA = 'e86ee99baec88585c5965b67043658a519ebde61bb32d195fc35598970e4b39f'
BUILD_DECL_SHA = 'b21890289efc7c0c7f7ce3592dff9d1947b27a72f2e3dc082807dbea76ba311f'
COLD_TERMINAL = ART / 'axial-material-qualified-AAA-rank1-factor-cache-production-terminal-20261007/terminal_return.json'
COLD_TERMINAL_SHA = '942532d85e1b38c8eb74e63f9d442e717cc01e4d24ded8fa0ba5ac5be1cbeddc'
BUILD_TERMINAL = ART / 'axial-material-qualified-AB-rank1-factor-cache-build-terminal-20261007/terminal_return.json'
BUILD_TERMINAL_SHA = 'c5eecbff0064a9285460c98bc01bad26ab9180a4b4e38a6186be779378ba9d96'
THREADS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
NG, NR, NZ, NL, NMAT, NSNAP, NA, NUN = 370, 8, 48, 3, 24, 3, 32, 1800
STAGE_WALL, TOTAL_WALL, RSS_CAP, RESERVE = 60, 120, 512, 16 * 2**20
HISTORY_CAP, FREE_FLOOR = 96 * 2**30, 8 * 2**30
TERMINAL_SCHEMA = 'AXMAT_RANK1_AXIAL_OPERATOR_AUDIT_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1'
TAIL_FIELDS = ('full_closeout_tail_gate','actual_elapsed_through_full_closeout_seconds','actual_complete_archive_bytes','resources_after_full_closeout')
RAW_STORAGE_RECIPE = 'Original-byte SHA256 content address; zlib(level1) per unique original record; every owner readback decompresses and checks original length, bytes and SHA before parsing. XSM type4 length is in 4-byte words (two words per REAL64).'
TRACK_RECORDS = {'STATE-VECTOR':(40,1),'MAT1D':(NZ,1),'MATCOD':(NR*NZ,1),
 'KEYFLX':(NR*NZ,1),'KEYFLX$ANIS':(NR*NZ*NL,1),'VOL1D':(NZ,2),'AREA2D':(NR,2),
 'VOLUME':(NR*NZ,2),'U':(NA,2),'W':(NA,2),'PL':(NL*NA,2),'NCODE':(2,1),
 'ZCODE':(2,2),'AXMAT-WHITE':(4,1),'AXMAT-W-P':(2,4)}
SYSTEM_RECORDS = {'NREG2D':(1,1),'NSNAP':(1,1),'POD-NMODE':(1,1),'POD-BASIS':(NR,2),
 'VOL2D':(NR,2),'DRAGON-TXSC':(NMAT+1,2),'DRAGON-S0XSC':((NMAT+1)*NL,2),
 'RADIAL-OP':(NR*NSNAP,2),'RADIAL-OP64':(2*NR*NSNAP,4)}
# Optional macro members are explicitly inventoried; no missing record is guessed.
MACRO_NAMES = ['NTOT0'] + [prefix+f'{l:02d}' for l in range(NL) for prefix in ('NJJS','IJJS','IPOS','SCAT','SIGW')]
SCOPE = dict(transport_calls=0,linear_solves=0,replays=0,CE_fitting=False,
 AAA_accuracy_qualified=False,ABA_admitted=False,actual_slot7_source_available=False,
 actual_32_angle_cell_or_all_faces_available=False,full_angular_residual_claimed=False,
 original_EINN_EUNK_primarily_P0=True,final_Pn_is_not_internal_iterate=True,
 inherited_build_proof_is_input_provenance_only=True)

def digest(path):
    descriptor=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(descriptor,'rb') as stream:
        before=os.fstat(stream.fileno())
        result=hashlib.file_digest(stream,'sha256').hexdigest()
        after=os.fstat(stream.fileno())
        if (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns):
            raise ValueError('input changed during fresh byte hash')
        return result

def require(path, wanted=None):
    path = Path(path)
    if not path.is_absolute() or '..' in path.parts or path.is_symlink() or not path.is_file():
        raise ValueError('absolute regular non-symlink dependency required: ' + str(path))
    cursor=path.parent
    while cursor!=cursor.parent:
        if cursor.is_symlink() or not cursor.is_dir(): raise ValueError('input ancestor alias/non-directory')
        cursor=cursor.parent
    if wanted is not None and digest(path) != wanted:
        raise ValueError('declared dependency changed: ' + str(path))
    return path

def pin(path):
    path = require(Path(path).resolve())
    return dict(path=str(path), sha256=digest(path))

def read(path):
    return json.loads(Path(path).read_text())

def write_new(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')

def write_table(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, separators=(',', ':'), allow_nan=False)
        stream.write('\n')

def verify(files):
    for path, wanted in files.items():
        require(path, wanted)

def load(path, name):
    path = require(path).resolve()
    if name in sys.modules:
        obj = sys.modules[name]
        if Path(obj.__file__).resolve() != path:
            raise ValueError('actual imported dependency path differs')
        return obj
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    sys.modules[name] = obj
    spec.loader.exec_module(obj)
    if Path(obj.__file__).resolve() != path:
        raise ValueError('import identity changed')
    return obj

def environment(expected=None):
    require(PYTHON.resolve(), PYTHON_SHA)
    if (Path(sys.executable).resolve() != PYTHON.resolve() or sys.version_info[:2] != (3, 12)
            or any(os.environ.get(key) != '1' for key in THREADS)):
        raise ValueError('pinned Python3.12 and exactly one thread required')
    loader = {key: os.environ.get(key) for key in ('PYTHONPATH', 'DYLD_LIBRARY_PATH',
        'DYLD_INSERT_LIBRARIES', 'LD_LIBRARY_PATH')}
    current = dict(python_version=platform.python_version(), executable=pin(PYTHON.resolve()),
        invocation=str(PYTHON), byteorder=sys.byteorder, loader_environment=loader,
        thread_environment={key: os.environ[key] for key in THREADS})
    if current['byteorder'] != 'little' or (expected is not None and current != expected):
        raise ValueError('actual interpreter/loader/reader execution environment differs')
    return current

@contextmanager
def stream_xsm(path, reader):
    """Frozen _XSM parser, record-sized pread; no resident whole-file mapping."""
    descriptor=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(descriptor,'rb') as stream:
        before = os.fstat(stream.fileno())
        class Words:
            def __len__(self):
                return before.st_size
            def __getitem__(self, item):
                if not isinstance(item, slice) or item.step not in (None, 1):
                    raise ValueError('unsupported frozen reader byte access')
                first, stop, _ = item.indices(before.st_size)
                raw = os.pread(stream.fileno(), stop - first, first)
                if len(raw) != stop - first:
                    raise ValueError('incomplete original XSM byte read')
                return raw
        yield reader._XSM(Words())
        after = os.fstat(stream.fileno())
        if (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns):
            raise ValueError('immutable scientific input changed during read')

def handles(a, directory, name, count):
    raw = a.record(directory, name, count, 10)
    return [a.directory(offset)['***HANDLE***'] for offset in struct.unpack(f'<{count}i', raw)]

def typed(raw, code):
    result = array(code)
    if result.itemsize != (8 if code == 'd' else 4): raise ValueError('original little-endian word size differs')
    result.frombytes(raw)
    return result

class RawArchive:
    """Original-byte content address, lossless encoding, readback before gates."""
    def __init__(self):
        self.stream = (OUT / 'audit/raw_records.bin').open('x+b')
        self.seen, self.index = {}, {}
        self.all_decompression_checks_passed = True
    def add(self, label, raw, origin):
        sha = hashlib.sha256(raw).hexdigest()
        if sha not in self.seen:
            stored = zlib.compress(raw, level=1)
            if archive_bytes() + len(stored) >= RESERVE:
                raise ValueError('raw input archive exceeds the fixed activity reserve')
            offset = self.stream.tell(); self.stream.write(stored); self.stream.flush()
            self.seen[sha] = dict(offset_bytes=offset, original_length_bytes=len(raw), sha256=sha,
                stored_compressed_length_bytes=len(stored), codec='zlib-level1')
        self.index[label] = dict(self.seen[sha], original=origin)
        descriptor = self.seen[sha]
        try:
            stored = os.pread(self.stream.fileno(), descriptor['stored_compressed_length_bytes'], descriptor['offset_bytes'])
            if len(stored) != descriptor['stored_compressed_length_bytes']:
                raise ValueError('incomplete stored compressed original record')
            decoder = zlib.decompressobj()
            decoded = decoder.decompress(stored, descriptor['original_length_bytes'] + 1)
            if (not decoder.eof or decoder.unused_data or decoder.unconsumed_tail
                    or len(decoded) != descriptor['original_length_bytes'] or decoded != raw
                    or hashlib.sha256(decoded).hexdigest() != sha):
                raise ValueError('original record decompression byte/length/SHA identity failed')
        except BaseException:
            self.all_decompression_checks_passed = False
            raise
        return decoded
    def close(self):
        self.stream.close()
        write_table(OUT / 'audit/raw_record_index.json', dict(schema='AXMAT_RANK1_AXIAL_OPERATOR_RAW_RECORDS_V1',
            blob=pin(OUT / 'audit/raw_records.bin'), records=self.index, bit_patterns_preserved=True,
            codec=raw_codec(), storage_recipe=RAW_STORAGE_RECIPE, all_decompression_checks_passed=self.all_decompression_checks_passed,
            decode='Read offset_bytes/stored_compressed_length_bytes from blob, zlib-decompress, require original_length_bytes and original sha256 before interpreting any words.'))

def raw_record(a, owner, directory, name, raw, allow_absent=False):
    if name not in directory and allow_absent:
        return raw.add(owner + '/' + name, b'', dict(record=name, present=False))
    entry = directory[name]
    data = a.read(entry[0], entry[1])
    return raw.add(owner + '/' + name, data, dict(record=name, xsm_word_offset=entry[0], length_words=entry[1], type=entry[2]))


def raw_codec():
    return dict(codec='zlib-level1', runtime_version=zlib.ZLIB_RUNTIME_VERSION,
                compiled_version=zlib.ZLIB_VERSION, extension=pin(zlib.__file__))


def absent(path):
    if os.path.lexists(path): raise ValueError('one exclusive attempt only: ' + str(path))


def namespace(root):
    """Full names/kinds and exact aliases, without following directory links."""
    if root.is_symlink() or not root.is_dir(): raise ValueError('owned namespace root is aliased or absent')
    result = dict(directories=[], files=[], symlinks={})
    for folder, dirs, names in os.walk(root, followlinks=False):
        for name in dirs + names:
            path = Path(folder) / name; rel = str(path.relative_to(root))
            if path.is_symlink():
                if path.is_dir(): raise ValueError('directory alias in owned namespace')
                result['symlinks'][rel] = dict(literal_target=os.readlink(path),
                    target=str(path.resolve(strict=True)))
            elif path.is_dir(): result['directories'].append(rel)
            elif path.is_file(): result['files'].append(rel)
            else: raise ValueError('nonregular owned namespace member')
    result['directories'].sort(); result['files'].sort()
    return result


def add_expected(files, path, wanted):
    path = Path(path)
    if str(path) in files and files[str(path)] != wanted:
        raise ValueError('conflicting input owners for ' + str(path))
    files[str(require(path, wanted))] = wanted


def modules():
    """Actual canonical controller/class; no modified binding or API replay."""
    if str(PROD/'runtime') not in sys.path: sys.path.insert(0,str(PROD/'runtime'))
    c = load(require(PROD / 'runtime/production_runner.py', CONTROLLER_SHA), 'production_runner')
    full = load(require(FULL_FACTORY, FULL_FACTORY_SHA), 'rank1_operator_actual_guard')
    builder = load(require(BUILDER, BUILDER_SHA), 'rank1_operator_resource_factory')
    if full.OwnRSSSerialExecutor.__bases__ != (c.SerialExecutor,):
        raise ValueError('actual supervisor base must be the frozen current controller')
    guard_files = builder.helper().guard_admission(full)
    parent = builder.parent_factory()
    provenance = dict(controller=pin(PROD / 'runtime/production_runner.py'),
        actual_own_rss_source=pin(FULL_FACTORY), actual_serial_base_source=pin(PROD / 'runtime/production_runner.py'),
        dynamic_resource_factory=pin(BUILDER), actual_dynamic_resource_class_source=pin(parent.__file__),
        tested_guard_files=[pin(path) for path in guard_files], callable_overlay=False,
        original_class_body_unchanged=True)
    return c, full, builder, parent, provenance


def resources_for(d, failure=None):
    _, _, builder, parent, _ = modules()
    result = builder.DynamicHistoryResources(ART, d['resource_roots'], FREE_FLOOR, HISTORY_CAP, failure)
    if type(result) is not parent.DynamicHistoryResources:
        raise ValueError('actual inherited dynamic resource class required')
    return result


def input_plan():
    """Expected identities come from actual frozen receipts/member manifests."""
    files, owners = {}, {}
    for path, wanted in ((PROD/'prepared.json',PREPARED_SHA),(PROD/'AAA/run_status.json',STATUS_SHA),
        (FINAL/'result.json',FINAL_SEAL_SHA),(BUILD/'seal.json',BUILD_SEAL_SHA),
        (BUILD/'declaration.json',BUILD_DECL_SHA),(COLD_TERMINAL,COLD_TERMINAL_SHA),
        (BUILD_TERMINAL,BUILD_TERMINAL_SHA),(BUILDER,BUILDER_SHA),(FULL_FACTORY,FULL_FACTORY_SHA),
        (READER,READER_SHA),(PROD/'runtime/production_runner.py',CONTROLLER_SHA)):
        add_expected(files,path,wanted)
    prepared, status, cold, bt = map(read,(PROD/'prepared.json',PROD/'AAA/run_status.json',COLD_TERMINAL,BUILD_TERMINAL))
    if (status['classification'] != 'WAITING_REFERENCE' or status['completed_maps'] != 12
            or status['prepared_sha256'] != PREPARED_SHA or set(status['cases']) != {'AAA'}):
        raise ValueError('the actual completed cold AAA input is required')
    case = status['cases']['AAA']; maps = case['maps']
    if (case['classification'] != 'VALID_MET' or case['final_directory'] != str(FINAL)
            or len(maps) != 12 or [row['epoch'] for row in maps] != list(range(1,13))
            or [row['classification'] for row in maps] != ['VALID_NOT_MET']*11+['VALID_MET']):
        raise ValueError('all consecutive maps ending at the first MET are required')
    for receipt in (cold,bt):
        if (receipt['record_producer'] != 'root' or receipt['actual_tool_terminal_return_observed'] is not True
                or receipt['record_written_after_actual_terminal_return'] is not True
                or type(receipt['returncode']) is not int or receipt['returncode'] != 0):
            raise ValueError('actual frozen Root terminal-return input proof required')
        for field in ('source','full_stdout','full_stderr'):
            item=receipt[field]; add_expected(files,item['path'],item['sha256'])
    if (cold['prepared'] != dict(path=str(PROD/'prepared.json'),sha256=PREPARED_SHA)
            or cold['run_status'] != dict(path=str(PROD/'AAA/run_status.json'),sha256=STATUS_SHA)
            or cold['completed_maps'] != 12 or bt['build_seal'] != dict(path=str(BUILD/'seal.json'),sha256=BUILD_SEAL_SHA)):
        raise ValueError('actual production/build terminal inputs differ')
    for item in cold['all_complete_stage_seals']:
        add_expected(files,item['path'],item['sha256'])
    member = read(FINAL/'result.json')
    if member['classification'] != 'SEALED_STAGE_OUTPUTS': raise ValueError('actual final member seal required')
    final_namespace = namespace(FINAL)
    if set(final_namespace['files']) | set(final_namespace['symlinks']) != set(member['sha256']) | {'result.json'}:
        raise ValueError('actual sealed final namespace differs')
    for label, name in (('system','candidate_system.xsm'),('track','initial_axial_track.xsm'),('macro','initial_axial_macrolib.xsm')):
        literal=FINAL/name; actual=literal
        alias=None
        if literal.is_symlink():
            actual=PROD/'AAA/bootstrap'/name
            if os.readlink(literal) != str(actual) or literal.resolve(strict=True) != actual:
                raise ValueError('only the original final-to-bootstrap scientific alias is permitted')
            alias=dict(path=str(literal),literal_target=os.readlink(literal),target=str(actual))
        add_expected(files,actual,member['sha256'][name])
        owners[label]=dict(path=str(actual),sha256=member['sha256'][name],actual_sealed_member=str(literal),alias=alias)
    for key in ('case_spec','rank_addendum','production_config'):
        item=prepared.get(key)
        if isinstance(item,dict) and set(item) >= {'path','sha256'}:
            add_expected(files,item['path'],item['sha256'])
    for name,wanted in prepared['local_files'].items():
        if name.startswith('runtime/') and (name.endswith('.py') or name=='runtime/Dragon'):
            add_expected(files,PROD/name,wanted)
    add_expected(files,FINAL/'picard_axial.log',member['sha256']['picard_axial.log'])
    seal = read(BUILD/'seal.json'); bd = read(BUILD/'declaration.json')
    for name in ('audit/binary_identity.json','runtime/build_identity.json','driver_result.json','audit/result.json'):
        add_expected(files,BUILD/name,seal['files'][name])
    binary=read(BUILD/'audit/binary_identity.json'); identity=read(BUILD/'runtime/build_identity.json')
    if (binary['status'] != 'PASS' or any(binary[k] is not True for k in
        ('source_and_command_identity_verified','exact_parent_link_inverse_restoration','actual_private_object_definitions_verified','executable_definitions_verified'))
        or identity['sole_new_production_overrides'] != ['SPOT1P64.o','FLU2DR64.o']):
        raise ValueError('actual compiled private objects and unchanged link provenance required')
    for item in [*binary['actual_objects'].values(),*binary['raw_metadata'].values(),identity['inherited_Flu_override']]:
        add_expected(files,item['path'],item['sha256'])
    for name,wanted in bd['source_inventory']['files'].items(): add_expected(files,BUILD_SOURCE/name,wanted)
    sa=read(BUILD_SOURCE/'source_admission.json')
    for path,wanted in sa['actual_original_compiled_source_and_object_inputs'].items(): add_expected(files,path,wanted)
    # Every literal link operand has its original declaration-owned byte identity.
    link=bd['build_commands'][2]
    for item in link:
        if item.endswith(('.o','.a')):
            wanted=bd['files'].get(item) or seal['files'].get(str(Path(item).relative_to(BUILD)) if Path(item).is_relative_to(BUILD) else '')
            if wanted is None: raise ValueError('link operand has no original expected identity: '+item)
            add_expected(files,item,wanted)
    c,full,builder,parent,provenance=modules()
    for item in [*provenance['tested_guard_files'],provenance['actual_dynamic_resource_class_source']]:
        add_expected(files,item['path'],item['sha256'])
    imported={}
    for obj in list(sys.modules.values()):
        name=getattr(obj,'__file__',None)
        if name and Path(name).suffix=='.py' and Path(name).resolve().is_relative_to(ROOT):
            path=Path(name).resolve(); imported[str(path)]=digest(require(path))
    for path,wanted in imported.items(): add_expected(files,path,wanted)
    return dict(files=files,owners=owners,final_namespace=final_namespace,guard_provenance=provenance,
        code_environment_input_files=imported,actual_compiled_abi=dict(xsm_word_bytes=4,integer32_bytes=4,
        real32_bytes=4,real64_bytes=8,Fortran_array_order='F',type4_words_per_value=2,
        actual_objects=binary['actual_objects'],actual_link=link,inherited_selector=identity['inherited_Flu_override']),
        inherited_cold_proof_scope='Complete Root exit0/seal-metadata proof retained. This audit freshly hashes only its explicitly owned operator/code inputs; it does not re-run cold qualification or re-hash all 391 historical payloads.')


def record_specs(a, owner):
    """Exhaustive declared group selection; no energy selection is permitted."""
    yield owner+'/STATE-VECTOR',a.root,'STATE-VECTOR',(40,1),False
    if owner=='track':
        for name,spec in TRACK_RECORDS.items():
            if name!='STATE-VECTOR': yield owner+'/'+name,a.root,name,spec,False
        return
    yield owner+'/GROUP',a.root,'GROUP',(NG,10),False
    groups=handles(a,a.root,'GROUP',NG)
    if any(entry[1:] != (-1,0) for entry in groups): raise ValueError('original GROUP directory handle ABI differs')
    for group,entry in enumerate(groups,1):
        directory=a.directory(entry[0]); prefix=owner+f'/g{group:03d}'
        if owner=='system':
            for name,spec in SYSTEM_RECORDS.items(): yield prefix+'/'+name,directory,name,spec,False
        elif owner=='macro':
            for name in MACRO_NAMES:
                if name.startswith(('NJJS','IJJS','IPOS')): spec=(NMAT,1); optional=False
                elif name.startswith('SCAT'): spec=(None,2); optional=True
                else: spec=(NMAT,2); optional=True
                yield prefix+'/'+name,directory,name,spec,optional
        else: raise ValueError('unknown original scientific owner')


def original_record(a,label,directory,name,spec,optional):
    entry=directory.get(name)
    if entry is None:
        if not optional: raise ValueError('required original record is absent: '+label)
        return b'',dict(present=False,record=name)
    if entry[2]!=spec[1] or (spec[0] is not None and entry[1]!=spec[0]):
        raise ValueError('actual raw original record ABI differs: '+label)
    return a.read(entry[0],entry[1]),dict(present=True,record=name,xsm_word_offset=entry[0],length_words=entry[1],type=entry[2])


def forecast(owners):
    """Metadata/original bytes only: no float decode, projection or gates."""
    reader=load(require(READER,READER_SHA),'rank1_operator_original_reader')
    seen={}; index={}; stored_bytes=0; records=original_bytes=0; directory_inventory={}
    for owner,item in owners.items():
        with stream_xsm(item['path'],reader) as a:
            directory_inventory[owner]=dict(root={k:list(v) for k,v in a.root.items()})
            for label,directory,name,spec,optional in record_specs(a,owner):
                data,origin=original_record(a,label,directory,name,spec,optional)
                sha=hashlib.sha256(data).hexdigest()
                if sha not in seen:
                    length=len(zlib.compress(data,level=1))
                    seen[sha]=dict(offset_bytes=stored_bytes,original_length_bytes=len(data),sha256=sha,
                        stored_compressed_length_bytes=length,codec='zlib-level1')
                    stored_bytes+=length
                index[label]=dict(seen[sha],original=origin)
                records+=1; original_bytes+=len(data)
    index_bound=dict(schema='AXMAT_RANK1_AXIAL_OPERATOR_RAW_RECORDS_V1',
        blob=dict(path=str(OUT/'audit/raw_records.bin'),sha256='0'*64),records=index,bit_patterns_preserved=True,
        codec=raw_codec(),storage_recipe=RAW_STORAGE_RECIPE,all_decompression_checks_passed=True,
        decode='Read offset_bytes/stored_compressed_length_bytes from blob, zlib-decompress, require original_length_bytes and original sha256 before interpreting any words.')
    index_bytes=len(json.dumps(index_bound,separators=(',',':'),allow_nan=False).encode())+1
    parts=dict(raw_compressed_bytes=stored_bytes,raw_index_bytes=index_bytes,
        derived_tensor_bytes=NG*(1+5*NZ+NA*NZ)*8,derived_index_and_findings_bytes=8192*NG,
        directory_and_sign_inventory_bytes=192*records,closeout_and_monitor_bytes=256*1024,
        source_metadata_and_copied_runtime_reserve=2**20)
    total=sum(parts.values())
    if total>=RESERVE: raise ValueError('complete all-group archive forecast exceeds fixed combined 16 MiB reserve')
    return dict(parts=parts,total_reserved_bytes=total,original_record_count=records,
        unique_original_record_count=len(seen),original_bytes_without_deduplication=original_bytes,
        unique_original_bytes=sum(item['original_length_bytes'] for item in seen.values()),codec=raw_codec(),storage_recipe=RAW_STORAGE_RECIPE,
        float_values_decoded=False,scientific_checks_performed=False,root_record_tables=directory_inventory)


def terminal_contract():
    return dict(schema=TERMINAL_SCHEMA,root=str(TERMINAL),receipt=str(TERMINAL/'terminal_return.json'),
        source_and_out_reserve_bytes=RESERVE,archive_scope_roots=[str(SOURCE),str(OUT)],
        required_tail_fields=list(TAIL_FIELDS),actual_Root_exit0_required=True,self_produced_terminal_witness=False,
        run_command=[str(PYTHON),str(Path(__file__).resolve()),'run','--sha256','ACTUAL_DECLARATION_SHA256'])


def declare():
    for path in (SOURCE,OUT,TERMINAL): absent(path)
    env=environment(); plan=input_plan(); reservation=forecast(plan['owners'])
    _,_,builder,_,_=modules()
    roots=builder.history_roots([*read(PROD/'prepared.json')['resource_roots'],*read(BUILD/'declaration.json')['resource_roots'],
        str(SOURCE),str(OUT),str(TERMINAL)],ART)
    resource_scope=builder.resource_scope_contract()
    d=dict(schema='AXMAT_RANK1_AXIAL_OPERATOR_AUDIT_DECLARATION_V1',source=pin(Path(__file__).resolve()),
        **plan,environment=env,archive_plan=reservation,resource_roots=roots,
        resource_scope_contract=resource_scope,artifact_budget_bytes=HISTORY_CAP,min_free_bytes=FREE_FLOOR,
        budget=dict(stage_seconds=STAGE_WALL,total_seconds=TOTAL_WALL,rss_mib=RSS_CAP,children=1,threads=1,retries=0),
        archive_scope_roots=[str(SOURCE),str(OUT)],terminal_contract=terminal_contract(),scope=SCOPE,
        mathematical_scope='Rank-one tensor reconstruction and operator/ABI diagnostics only; no solution or current reference qualification.',
        white_assumption='Every floor uses the same local angular return kernel multiplied by B(row1)^2. A constant local side trace proportional to the volume mode is assumed. No nonlocal native surface-response equivalence is asserted.',
        missing_current_measurements=['actual final dispatch S2/qext REAL64','32-angle cell field','all shared 32-angle faces','pre/post normalization angular fields'])
    resources=resources_for(d); before=resources.check()
    if before['artifact_bytes']+RESERVE>=HISTORY_CAP or before['disk_free_bytes']-RESERVE<FREE_FLOOR:
        raise ValueError('complete declared family reservation does not fit')
    SOURCE.mkdir(); (SOURCE/'runtime').mkdir()
    shutil.copy2(READER,SOURCE/'runtime/snapshot_control_preflight.py')
    shutil.copy2(PROD/'runtime/run_bounded_dragon.py',SOURCE/'runtime/run_bounded_dragon.py')
    d['copied_runtime']={name:pin(SOURCE/'runtime'/name) for name in ('snapshot_control_preflight.py','run_bounded_dragon.py')}
    d['declaration_resource_admission']=before
    write_new(SOURCE/'declaration.json',d)
    write_new(SOURCE/'source_inventory.json',dict(files={str(p.relative_to(SOURCE)):digest(p) for p in SOURCE.rglob('*') if p.is_file()},symlinks={}))
    if source_bytes()>reservation['parts']['source_metadata_and_copied_runtime_reserve'] or archive_bytes()>=RESERVE:
        raise ValueError('actual SOURCE metadata/copied runtime exceeds original reservation')
    print(json.dumps(dict(classification='PREPARED_READ_ONLY_OPERATOR_INPUTS_NO_SCIENCE',declaration=pin(SOURCE/'declaration.json'),scope=SCOPE)))


def admission(expected, verify_input_bytes=True):
    d=read(require(SOURCE/'declaration.json',expected)); inventory=read(require(SOURCE/'source_inventory.json'))
    source_ns=namespace(SOURCE)
    if source_ns['symlinks'] or source_ns['directories']!=['runtime'] or set(source_ns['files'])!=set(inventory['files'])|{'source_inventory.json'}:
        raise ValueError('frozen new SOURCE namespace differs')
    verify({str(SOURCE/name):sha for name,sha in inventory['files'].items()})
    require(d['source']['path'],d['source']['sha256']); environment(d['environment'])
    if verify_input_bytes: verify(d['files'])
    if (d['schema']!='AXMAT_RANK1_AXIAL_OPERATOR_AUDIT_DECLARATION_V1' or d['scope']!=SCOPE
        or d['budget']!=dict(stage_seconds=60,total_seconds=120,rss_mib=512,children=1,threads=1,retries=0)
        or d['archive_scope_roots']!=[str(SOURCE),str(OUT)] or d['terminal_contract']!=terminal_contract()
        or d['archive_plan']['total_reserved_bytes']!=sum(d['archive_plan']['parts'].values())
        or d['archive_plan']['total_reserved_bytes']>=RESERVE or d['archive_plan']['codec']!=raw_codec()
        or source_bytes()>2**20 or namespace(FINAL)!=d['final_namespace']):
        raise ValueError('frozen scope/budget/codec/namespace changed')
    for item in d['owners'].values():
        if item['alias']:
            alias=item['alias']; p=Path(alias['path'])
            if not p.is_symlink() or os.readlink(p)!=alias['literal_target'] or str(p.resolve(strict=True))!=alias['target']:
                raise ValueError('original scientific input alias changed')
    _,_,builder,_,provenance=modules()
    if provenance!=d['guard_provenance'] or builder.resource_scope_contract()!=d['resource_scope_contract']:
        raise ValueError('actual class/guard/family budget contract differs')
    return d


def words(records,label,expected):
    raw,origin=records[label]
    if not origin['present']: raise ValueError('required typed record is absent: '+label)
    code={1:'i',2:'f',4:'d'}[expected]
    if origin['type']!=expected: raise ValueError('typed decoder ABI differs')
    return typed(raw,code)


def finite_inventory(records):
    report={}; failures=[]
    for label,(data,origin) in records.items():
        if not origin['present'] or origin['type'] not in (2,4): continue
        values=typed(data,'f' if origin['type']==2 else 'd')
        report[label]=signed_counts(values,32 if origin['type']==2 else 64)
        if report[label]['nonfinite']: failures.append(label)
    write_table(OUT/'audit/original_signed_inventory.json',dict(records=report,
        signed_coefficients_and_signed_zeros_preserved=True,nonnegative_gate_applied_to_all_Pn=False))
    if failures: raise ValueError('nonfinite raw operators after complete lossless archive: '+','.join(failures))


def validate_track(records):
    state=words(records,'track/STATE-VECTOR',1)
    expected={1:NR*NZ,2:NUN,4:NMAT,6:NR,7:NZ,8:NSNAP,9:1,10:1,11:NR*NZ*NL,12:(NZ+1)*NR,15:NA,16:NL,18:0,27:1}
    if any(state[i-1]!=value for i,value in expected.items()): raise ValueError('original production TRACK shape/ABI differs')
    result={name:words(records,'track/'+name,spec[1]) for name,spec in TRACK_RECORDS.items() if name!='STATE-VECTOR'}
    mat,keys,scalar=result['MATCOD'],result['KEYFLX$ANIS'],result['KEYFLX']
    if list(keys[:NR*NZ])!=list(scalar): raise ValueError('scalar KEYFLX differs from actual P0 anisotropic key')
    for radial in range(NR):
        for z in range(NZ):
            region=radial*NZ+z
            if not 1<=mat[region]<=NMAT: raise ValueError('original material mapping outside actual 24 materials')
            for order in range(NL):
                if keys[region+order*NR*NZ] != region*NL+order+1:
                    raise ValueError('actual radial/floor/moment Fortran unknown mapping differs')
    if any(not 1<=value<=NSNAP for value in result['MAT1D']): raise ValueError('snapshot map outside original three snapshots')
    if list(result['MAT1D'])!=[1]*16+[2]*16+[3]*16:
        raise ValueError('original three 50 cm zones/16 cells per zone differ')
    for radial in range(NR):
        for z in range(NZ):
            if mat[radial*NZ+z]!=(result['MAT1D'][z]-1)*NR+radial+1:
                raise ValueError('original three-zone by eight-region material24 mapping differs')
    if any(value<=0 for name in ('VOL1D','AREA2D','VOLUME') for value in result[name]):
        raise ValueError('physical original geometry volumes must remain positive')
    if sum(result['VOL1D'])!=150.0: raise ValueError('fixed original 150 cm height differs')
    if list(result['NCODE'])!=[1,1] or any(value!=0 for value in result['ZCODE']):
        raise ValueError('original true vacuum faces required, separate from radial white trace')
    if list(result['AXMAT-WHITE'])!=[1,1,8,3] or result['AXMAT-W-P'][0]!=6.0*0.61776479:
        raise ValueError('actual original fixed white marker/physical hexagon perimeter differs')
    mu,weight,pl=result['U'],result['W'],result['PL']
    if any(abs(value)>=1 or value==0 for value in mu) or any(value<=0 for value in weight):
        raise ValueError('actual SN32 directional and positive quadrature contract differs')
    opposite=[]
    for n,value in enumerate(mu):
        matches=[j for j,item in enumerate(mu) if struct.pack('<f',item)==struct.pack('<f',-value)]
        if len(matches)!=1: raise ValueError('one bit-exact opposite direction required')
        j=matches[0]
        if struct.pack('<f',weight[j])!=struct.pack('<f',weight[n]): raise ValueError('opposite quadrature weights differ')
        opposite.append(j)
    if any(opposite[opposite[n]]!=n for n in range(NA)) or sum(value>0 for value in mu)!=NA//2:
        raise ValueError('SN32 opposite map is not an involution')
    if abs(sum(weight)-2.0)>8*2**-23: raise ValueError('original white quadrature normalization exceeds its original REAL32 bound')
    if any(pl[n*NL]!=1.0 or struct.pack('<f',pl[n*NL+1])!=struct.pack('<f',mu[n]) for n in range(NA)):
        raise ValueError('actual stored P0/P1 basis differs from density/current convention')
    if any(struct.pack('<f',pl[n*NL+2])!=struct.pack('<f',pl[opposite[n]*NL+2]) for n in range(NA)):
        raise ValueError('stored P2 opposite direction parity differs')
    result['opposite']=opposite; result['state']=list(state)
    return result


def white_kernel(track,area):
    mu,w=track['U'],track['W']; s=[math.sqrt(1.0-value*value) for value in mu]
    normalization=sum(w[n]*s[n] for n in range(NA)); p=track['AXMAT-W-P'][0]/(math.pi*area)
    matrix=[[-p*s[n]*w[j]*s[j]/normalization+(p*s[j] if n==j else 0.0) for j in range(NA)] for n in range(NA)]
    column=[]; row=[]
    for j in range(NA):
        terms=[w[n]*matrix[n][j] for n in range(NA)]; value=sum(terms); scale=sum(abs(v) for v in terms)
        if abs(value)>64*2**-52*scale: raise ValueError('white weighted column conservation accounting failed')
        column.append(value)
    for values in matrix:
        value=sum(values); scale=sum(abs(v) for v in values)
        if abs(value)>64*2**-52*scale: raise ValueError('white constant angular nullspace accounting failed')
        row.append(value)
    return matrix,dict(s=s,normalization=normalization,prefactor=p,
        weighted_column_residuals=column,constant_right_null_residuals=row,
        formula='K(n,j)=-p*s(n)*w(j)*s(j)/sum(w*s)+delta(n,j)*p*s(j)',
        side_face_and_floor_dependent_native_trace_measured=False)


def derive_operator(group,records,track,mn,dn,white):
    prefix=f'system/g{group:03d}/'
    item={name:words(records,prefix+name,spec[1]) for name,spec in SYSTEM_RECORDS.items()}
    if any(item[name][0]!=value for name,value in (('NREG2D',NR),('NSNAP',NSNAP),('POD-NMODE',1))):
        raise ValueError('actual group kernel dimensions differ')
    if records[prefix+'VOL2D'][0]!=records['track/AREA2D'][0]: raise ValueError('actual group radial volumes differ from TRACK geometry')
    if not mirror_matches(item['RADIAL-OP64'],records[prefix+'RADIAL-OP'][0]):
        raise ValueError('actual REAL64 radial operator is not the exact REAL32 demotion mirror')
    basis,vol=item['POD-BASIS'],item['VOL2D']; area=sum(vol)
    if any(v<=0 for v in vol) or abs(area/(math.sqrt(3.0)*track['AXMAT-W-P'][0]**2/24.0)-1)>5e-6:
        raise ValueError('original kernel physical volume/perimeter gate failed')
    weight=[value/area for value in vol]; G=0.0
    for i in range(NR): G+=weight[i]*basis[i]*basis[i]
    if not math.isfinite(G) or G<=0: raise ValueError('actual rank-one Gram mass must be finite and strictly positive')
    factor=basis[0]*basis[0]; projected=[]; taus=[]; report_tau=[]; op_hash=hashlib.sha256()
    min_diag=math.inf; max_diag=-math.inf; positive_offdiag=negative_offdiag=0
    # Compare published self moments to original raw macro fields without
    # deleting deliberate ASMDRV transport/DIFFHET corrections or imposing a new gate.
    comparisons=[]
    for l in range(NL):
        label=f'macro/g{group:03d}/SIGW{l:02d}'; raw,origin=records[label]
        if origin['present']:
            values=typed(raw,'f'); self_values=item['DRAGON-S0XSC'][l*(NMAT+1)+1:(l+1)*(NMAT+1)]
            comparisons.append(dict(order=l,macro_field=label,exact_REAL32_equal=raw==struct.pack('<'+str(NMAT)+'f',*self_values),
                max_absolute_difference=max(abs(values[i]-self_values[i]) for i in range(NMAT)),
                difference_is_not_automatically_a_source_error=True))
        else: comparisons.append(dict(order=l,macro_field=label,present=False))
    for z in range(NZ):
        snap=track['MAT1D'][z]-1; T=R=0.0; S=[0.0]*NL
        for i in range(NR):
            material=track['MATCOD'][i*NZ+z]
            T+=weight[i]*basis[i]*item['DRAGON-TXSC'][material]*basis[i]
            R+=weight[i]*basis[i]*item['RADIAL-OP64'][snap*NR+i]*basis[i]
            for l in range(NL): S[l]+=weight[i]*basis[i]*item['DRAGON-S0XSC'][l*(NMAT+1)+material]*basis[i]
        projected.extend([T,R,*S])
        tau=[track['VOL1D'][z]*(T/G)/abs(mu) for mu in track['U']]; taus.extend(tau)
        report_tau.append(dict(floor=z+1,snapshot=snap+1,min=min(tau),max=max(tau),count_gt_two=sum(v>2 for v in tau)))
        # Assemble every actual floor/direction pair in original n,j,l order;
        # retain a digest plus exact factorized tensors instead of a 145 MiB
        # duplicate dense dump. No factorization or solve is performed.
        for n in range(NA):
            for j in range(NA):
                C=T if n==j else 0.0
                for l in range(NL): C-=mn[n][l]*S[l]*dn[l][j]
                C+=mn[n][0]*R*dn[0][j]; C+=factor*white[n][j]
                if not math.isfinite(C): raise ValueError('nonfinite derived actual operator')
                op_hash.update(struct.pack('<d',C))
                if n==j: min_diag=min(min_diag,C);max_diag=max(max_diag,C)
                elif C>0: positive_offdiag+=1
                elif C<0: negative_offdiag+=1
    payload=struct.pack('<'+str(1+len(projected)+len(taus))+'d',G,*projected,*taus)
    report=dict(group=group,Gram=G,white_trace_amplitude_squared=factor,
        original_signed_basis=signed_counts(basis,32),radial_REAL64_to_REAL32_mirror_exact=True,
        macro_vs_system_self_moments=comparisons,full_C_floor_n_j_SHA256=op_hash.hexdigest(),
        C_diagonal_min=min_diag,C_diagonal_max=max_diag,C_positive_offdiagonal_entries=positive_offdiag,
        C_negative_offdiagonal_entries=negative_offdiag,optical_scales=report_tau,
        pure_absorption_DD_factor_formula='(1-tau/2)/(1+tau/2)',
        tau_gt_two_is_actual_angular_negativity_proof=False)
    return payload,report


def worker(expected):
    # Parent has already fully hashed the same immutable inputs in run_entry.
    # This worker still verifies all owned SOURCE/code identities and each raw
    # input fresh; no cross-phase byte cache or input semantic snapshot is used.
    d=admission(expected); claim=read(require(OUT/'execution_claim.json'))
    if (claim['parent_pid']!=os.getppid() or claim['declaration_sha256']!=expected
            or claim['source']!=d['source'] or claim['retries']!=0 or claim['children']!=1):
        raise ValueError('sole actual declared parent/child handoff required')
    reader=load(require(SOURCE/'runtime/snapshot_control_preflight.py',READER_SHA),'rank1_operator_copied_reader')
    records={}; inventories={}; raw=RawArchive()
    try:
        for owner,item in d['owners'].items():
            with stream_xsm(item['path'],reader) as a:
                inventories[owner]=dict(root={k:list(v) for k,v in a.root.items()},groups=[])
                if owner!='track':
                    for entry in handles(a,a.root,'GROUP',NG):
                        inventories[owner]['groups'].append({k:list(v) for k,v in a.directory(entry[0]).items()})
                for label,directory,name,spec,optional in record_specs(a,owner):
                    original,origin=original_record(a,label,directory,name,spec,optional)
                    records[label]=(raw.add(label,original,origin),origin)
    finally: raw.close()
    plan=d['archive_plan']
    if (not raw.all_decompression_checks_passed or len(raw.index)!=plan['original_record_count']
        or len(raw.seen)!=plan['unique_original_record_count']
        or sum(row['original_length_bytes'] for row in raw.index.values())!=plan['original_bytes_without_deduplication']
        or sum(row['original_length_bytes'] for row in raw.seen.values())!=plan['unique_original_bytes']
        or (OUT/'audit/raw_records.bin').stat().st_size!=plan['parts']['raw_compressed_bytes']):
        raise ValueError('complete lossless archive differs from original-byte preflight')
    write_table(OUT/'audit/original_directory_inventory.json',dict(owners=inventories,
        all_370_group_directories_retained=True,original_absence_in_raw_index=True))
    write_new(OUT/'audit/boundary_controls.json',tiny_controls())
    finite_inventory(records);track=validate_track(records)
    system_state=words(records,'system/STATE-VECTOR',1);macro_state=words(records,'macro/STATE-VECTOR',1)
    if system_state[0]!=1 or macro_state[0]!=NG or macro_state[1]!=NMAT or macro_state[2]!=NL:
        raise ValueError('actual ITPIJ1/370/24/P0-P2 material system differs')
    # Original macro compressed records are not collapsed into selected groups.
    compressed=[]
    for group in range(1,NG+1):
        for l in range(NL):
            prefix=f'macro/g{group:03d}/'; njj=words(records,prefix+f'NJJS{l:02d}',1)
            ijj=words(records,prefix+f'IJJS{l:02d}',1);ipos=words(records,prefix+f'IPOS{l:02d}',1)
            values,origin=records[prefix+f'SCAT{l:02d}']; count=len(values)//4
            if any(n<0 for n in njj) or count!=sum(njj): raise ValueError('full original compressed SCAT count differs')
            for material,n in enumerate(njj):
                if n and not (1<=ipos[material]<=count and ipos[material]+n-1<=count and 1<=ijj[material]-n+1<=ijj[material]<=NG):
                    raise ValueError('actual full SCAT material/source-group mapping outside original bounds')
            compressed.append(dict(group=group,order=l,original_entries=count,present=origin['present'],
                NJJS=list(njj),IJJS=list(ijj),IPOS=list(ipos)))
    write_table(OUT/'audit/full_compressed_scattering_mapping.json',dict(rows=compressed,
        all_groups=list(range(1,NG+1)),orders=[0,1,2],source_group_formula='JG=IJJS(IBM)-JND+1; coefficient index=IPOS(IBM)+JND-1 (one based)',
        raw_stream_must_be_decoded_before_mapping=True,intergroup_source_not_replayed=True))
    mu,w,pl=track['U'],track['W'],track['PL']
    mn=[[0.5*(2*l+1)*pl[n*NL+l] for l in range(NL)] for n in range(NA)]
    dn=[[w[n]*pl[n*NL+l] for n in range(NA)] for l in range(NL)]
    white,white_report=white_kernel(track,sum(track['AREA2D']))
    write_new(OUT/'audit/geometry_angle_white.json',dict(track_STATE=track['state'],MAT1D=list(track['MAT1D']),MATCOD=list(track['MATCOD']),
        KEYFLX=list(track['KEYFLX']),KEYFLX_ANIS=list(track['KEYFLX$ANIS']),VOL1D=list(track['VOL1D']),AREA2D=list(track['AREA2D']),
        mu=list(mu),weights=list(w),P_l_column_major=list(pl),opposite_zero_based=track['opposite'],mn=mn,dn=dn,
        white_matrix=white,white_contract=white_report,NCODE=list(track['NCODE']),ZCODE=list(track['ZCODE']),
        incoming_boundary='mu>0: face0=0; mu<0: face48=0; true axial vacuum independent of radial white return',
        density_current_convention='Jz=sum(w*mu*face); no AREA multiplier',white_assumption=d['white_assumption']))
    reports=[]; index=[]
    with (OUT/'audit/derived_rank1_tensors.bin').open('xb') as stream:
        for group in range(1,NG+1):
            payload,report=derive_operator(group,records,track,mn,dn,white)
            index.append(dict(group=group,offset_bytes=stream.tell(),length_bytes=len(payload),sha256=hashlib.sha256(payload).hexdigest()))
            stream.write(payload); reports.append(report)
    log=Path(FINAL/'picard_axial.log').read_text()
    selectors=[list(map(int,m.groups())) for m in re.finditer(r'^AXMAT-MOMENT-ORDER SELECTOR\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$',log,re.M)]
    if not selectors or any(row!=[32,3,2,3,1] for row in selectors): raise ValueError('actual compiled FLU selector observer differs')
    write_table(OUT/'audit/derived_rank1_tensors.json',dict(schema='AXMAT_RANK1_AXIAL_OPERATOR_FACTORIZED_TENSOR_V1',
        blob=pin(OUT/'audit/derived_rank1_tensors.bin'),records=index,real64_little_endian=True,
        layout='Per group: G scalar; then 48 rows [T,R,S0,S1,S2]; then tau(z,n) z-major/angle-minor, all REAL64.',
        reconstruction='D=G*diag(mu); C(z,n,j)=delta(n,j)*T(z)-sum_l mn(n,l)*S_l(z)*dn(l,j)+mn(n,0)*R(z)*dn(0,j)+B(row1)^2*Kwhite(n,j); diamond blocks h*C/2 +/- D.',
        derived_values_not_new_native_equation_measurements=True,groups=reports))
    findings=dict(classification='COMPLETE_READ_ONLY_ALL370_AXIAL_OPERATOR_AUDIT_ONLY',groups=NG,radial_regions=NR,
        floors=NZ,materials=NMAT,rank=1,angles=NA,moments=[0,1,2],height_cm=150,
        raw_record_count=len(records),full_derived_C_entries=NG*NZ*NA*NA,
        original_raw_bits_checked_before_float_gate=True,all_370_groups_and_compressed_entries_retained=True,
        actual_ITPIJ=system_state[0],actual_selector_observer_count=len(selectors),actual_selector_rows=selectors,
        true_vacuum_mapping_verified=True,constant_local_white_trace_measured_against_native=False,
        physical_accuracy_gate_changed=False,missing_current_measurements=d['missing_current_measurements'],**SCOPE)
    write_new(OUT/'audit/findings.json',findings)
    # One parent final input/namespace verification follows the child. This
    # child does not repeat a whole-history resource tree scan after its body.
    print(json.dumps(findings))

def signed_counts(values, width):
    output = dict(positive=0, negative=0, positive_zero=0, negative_zero=0, nonfinite=0)
    for value in values:
        if not math.isfinite(value): key = 'nonfinite'
        elif value == 0: key = 'negative_zero' if math.copysign(1, value) < 0 else 'positive_zero'
        else: key = 'positive' if value > 0 else 'negative'
        output[key] += 1
    output['word_width_bits'] = width
    return output

def mirror_matches(values, raw):
    try:
        return all(struct.pack('<f', value) == raw[j * 4:(j + 1) * 4] for j, value in enumerate(values))
    except OverflowError:
        return False

def strict_json(path):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj: raise ValueError('duplicate terminal JSON key')
            obj[key] = value
        return obj
    def constant(value): raise ValueError('nonfinite terminal JSON constant: ' + value)
    obj = json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique, parse_constant=constant)
    if type(obj) is not dict: raise ValueError('complete actual stdout must be a single JSON object')
    json.dumps(obj,allow_nan=False)
    return obj


def watch(stage):
    path=OUT/'audit/operator.watchdog.json';w=read(require(path))
    if (stage['status']!='PASS' or w['returncode']!=0 or w['limit_failure'] is not None
        or w['command']!=stage['command'] or not 0<w['wall_cap_seconds']<=stage['wall_cap_seconds']<=STAGE_WALL
        or not 0<=w['elapsed_seconds']<w['wall_cap_seconds'] or not 0<=w['sampled_peak_rss_mib']<RSS_CAP
        or w['rss_cap_mib']!=RSS_CAP or w['own_child_only'] is not True or w['liveness_group_cleanup'] is not True):
        raise ValueError('actual sole read-only child supervision failed')
    require(OUT/'audit/operator.log',stage['log_sha256'])
    return pin(path)


def regular_bytes(root):
    total=0
    if not root.exists(): return total
    for folder,dirs,names in os.walk(root,followlinks=False):
        for name in dirs+names:
            path=Path(folder)/name
            if path.is_symlink(): raise ValueError('new archive contains an alias')
            if path.is_file(): total+=path.stat().st_size
            elif not path.is_dir(): raise ValueError('new archive contains nonregular member')
    return total


def source_bytes(): return regular_bytes(SOURCE)


def archive_bytes():
    return source_bytes()+regular_bytes(OUT)


def run(expected):
    started=time.monotonic()
    d=admission(expected);absent(OUT)
    _,full,_,_,_=modules();resources=resources_for(d)
    before=resources.check()
    if before['artifact_bytes']+RESERVE>=HISTORY_CAP or before['disk_free_bytes']-RESERVE<FREE_FLOOR:
        raise ValueError('actual complete family reservation no longer fits')
    OUT.mkdir();(OUT/'runtime').mkdir();(OUT/'audit').mkdir()
    shutil.copy2(SOURCE/'runtime/run_bounded_dragon.py',OUT/'runtime/run_bounded_dragon.py')
    write_new(OUT/'execution_claim.json',dict(parent_pid=os.getpid(),declaration_sha256=expected,
        source=d['source'],started_unix=time.time(),retries=0,children=1))
    result=dict(classification='READ_ONLY_AXIAL_OPERATOR_AUDIT_FAILED_NO_RETRY',declaration_sha256=expected,
        source=d['source'],completed_commands=0,error=None,archive_scope_roots=[str(SOURCE),str(OUT)],
        elapsed_seconds_scope='Whole run begins before admission; sealed elapsed_seconds includes end input verification through pre-closeout. External actual tail measures complete result/seal publication.',**SCOPE)
    failed=None
    try:
        remaining=TOTAL_WALL-(time.monotonic()-started)
        if remaining<=0: raise ValueError('whole 120-second wall bound exhausted before sole child')
        runner=full.OwnRSSSerialExecutor(OUT,remaining,'audit',resources)
        command=[str(PYTHON),str(Path(__file__).resolve()),'worker','--sha256',expected]
        runner.execute(OUT/'audit','operator',command,STAGE_WALL)
        stages=read(OUT/'audit/stages.json')['stages']
        if len(stages)!=1 or stages[0]['label']!='audit/operator' or stages[0]['command']!=command:
            raise ValueError('exactly one actual original bounded worker required')
        monitor=watch(stages[0]);findings=read(OUT/'audit/findings.json')
        if findings['classification']!='COMPLETE_READ_ONLY_ALL370_AXIAL_OPERATOR_AUDIT_ONLY' or findings['groups']!=NG:
            raise ValueError('complete all-group operator diagnostic required')
        result.update(classification=findings['classification'],completed_commands=1,
            findings=pin(OUT/'audit/findings.json'),actual_child_watchdog=monitor)
    except BaseException as error:
        failed=error;result['error']=repr(error)
    finally:
        try:
            admission(expected)
            elapsed=time.monotonic()-started;size=archive_bytes()
            result.update(elapsed_seconds=elapsed,actual_archive_bytes_before_closeout=size)
            if elapsed>=TOTAL_WALL or size>=RESERVE: raise ValueError('original whole wall/archive bound failed before closeout')
        except BaseException as error:
            failed=error;result.update(classification='READ_ONLY_AXIAL_OPERATOR_AUDIT_FAILED_NO_RETRY',error=repr(error))
        try:
            write_new(OUT/'result.json',result)
            members={str(p.relative_to(OUT)):digest(p) for p in OUT.rglob('*') if p.is_file() and not p.is_symlink()}
            write_new(OUT/'seal.json',dict(schema='AXMAT_RANK1_AXIAL_OPERATOR_AUDIT_SEAL_V1',files=members))
            snapshot=resources.check();size=archive_bytes();elapsed=time.monotonic()-started
            result.update(full_closeout_tail_gate='PASS',actual_elapsed_through_full_closeout_seconds=elapsed,
                actual_complete_archive_bytes=size,resources_after_full_closeout=snapshot)
            if elapsed>=TOTAL_WALL or size>=RESERVE: raise ValueError('original whole wall/archive bound failed after complete closeout')
        except BaseException as error:
            failed=error;result.update(classification='READ_ONLY_AXIAL_OPERATOR_AUDIT_FAILED_NO_RETRY',error=repr(error),full_closeout_tail_gate='FAIL')
            write_new(OUT/'closeout_failure.json',result)
    print(json.dumps(result))
    if failed is not None: raise failed


def external_file(value,wanted):
    path=Path(value)
    if (not isinstance(wanted,str) or not re.fullmatch('[0-9a-f]{64}',wanted)
        or not path.is_absolute() or '..' in path.parts or str(path)!=str(value)
        or path.parent!=TERMINAL or path.resolve(strict=True)!=path):
        raise ValueError('fixed independently pinned actual Root terminal file required')
    cursor=path
    while cursor!=cursor.parent:
        if cursor.is_symlink(): raise ValueError('external terminal ancestor is aliased')
        cursor=cursor.parent
    return require(path,wanted)


def diagnostic_admission(expected_seal,terminal_evidence,terminal_evidence_sha256):
    """Input/operator diagnostic only; Root must have observed actual exit0."""
    seal=read(require(OUT/'seal.json',expected_seal))
    if seal['schema']!='AXMAT_RANK1_AXIAL_OPERATOR_AUDIT_SEAL_V1': raise ValueError('actual completed audit seal required')
    current=namespace(OUT)
    if current['symlinks'] or current['directories']!=['audit','runtime'] or set(current['files'])!=set(seal['files'])|{'seal.json'}:
        raise ValueError('exact successful sealed namespace required; partial/tail failures reject')
    verify({str(OUT/name):sha for name,sha in seal['files'].items()})
    result=read(OUT/'result.json');d=admission(result['declaration_sha256'])
    if (result['classification']!='COMPLETE_READ_ONLY_ALL370_AXIAL_OPERATOR_AUDIT_ONLY'
        or result['completed_commands']!=1 or result['error'] is not None
        or result['archive_scope_roots']!=[str(SOURCE),str(OUT)] or any(result.get(k)!=v for k,v in SCOPE.items())):
        raise ValueError('actual complete zero-solve all-group diagnostic required')
    findings=read(OUT/'audit/findings.json')
    if (findings['classification']!=result['classification'] or findings['groups']!=NG
        or findings['raw_record_count']!=d['archive_plan']['original_record_count']
        or findings['full_derived_C_entries']!=NG*NZ*NA*NA
        or findings['original_raw_bits_checked_before_float_gate'] is not True
        or findings['all_370_groups_and_compressed_entries_retained'] is not True
        or result['findings']!=pin(OUT/'audit/findings.json') or any(findings.get(k)!=v for k,v in SCOPE.items())):
        raise ValueError('all original operands and explicit limited scope required')
    path=external_file(terminal_evidence,terminal_evidence_sha256)
    if path!=TERMINAL/'terminal_return.json': raise ValueError('fixed Root receipt required')
    e=strict_json(path);command=[str(PYTHON),str(Path(__file__).resolve()),'run','--sha256',result['declaration_sha256']]
    if (e['schema']!=TERMINAL_SCHEMA or e['record_producer']!='root'
        or e['actual_tool_terminal_return_observed'] is not True or e['record_written_after_actual_terminal_return'] is not True
        or type(e['returncode']) is not int or e['returncode']!=0 or e['command']!=command
        or e['source']!=d['source'] or e['declaration']!=pin(SOURCE/'declaration.json')
        or e['audit_seal']!=dict(path=str(OUT/'seal.json'),sha256=expected_seal)):
        raise ValueError('actual Root exit0/source/declaration/seal witness differs')
    stdout=external_file(e['full_stdout']['path'],e['full_stdout']['sha256'])
    stderr=external_file(e['full_stderr']['path'],e['full_stderr']['sha256'])
    if stdout==path or stderr in (path,stdout): raise ValueError('complete stdout/stderr must be independently retained')
    returned=strict_json(stdout);tail={key:returned[key] for key in TAIL_FIELDS}
    if returned!=dict(result,**tail) or any(e[key]!=tail[key] for key in TAIL_FIELDS):
        raise ValueError('complete actual stdout/Root tail differs from sealed result')
    elapsed,size,snap=tail[TAIL_FIELDS[1]],tail[TAIL_FIELDS[2]],tail[TAIL_FIELDS[3]]
    if (tail[TAIL_FIELDS[0]]!='PASS' or type(elapsed) not in (int,float) or not math.isfinite(elapsed)
        or not result['elapsed_seconds']<=elapsed<TOTAL_WALL or type(size) is not int or not 0<=size<RESERVE
        or size!=archive_bytes() or snap['artifact_budget_bytes']!=HISTORY_CAP or snap['min_free_bytes']!=FREE_FLOOR
        or type(snap['artifact_bytes']) is not int or not size<=snap['artifact_bytes']<=HISTORY_CAP
        or type(snap['disk_free_bytes']) is not int or snap['disk_free_bytes']<FREE_FLOOR or 'reason' in snap
        or snap['declared_resource_roots']!=d['resource_roots']
        or not set(d['resource_roots']).issubset(snap['resource_roots'])):
        raise ValueError('actual full-tail 120/16 MiB/96-family/free8 contract failed')
    stages=read(OUT/'audit/stages.json')['stages']
    if len(stages)!=1 or stages[0]['label']!='audit/operator' or stages[0]['command']!=[str(PYTHON),str(Path(__file__).resolve()),'worker','--sha256',result['declaration_sha256']]:
        raise ValueError('exact actual sole worker required')
    watch(stages[0])
    return dict(schema='AXMAT_RANK1_AXIAL_OPERATOR_AUDIT_ACTUAL_TERMINAL_ADMISSION_V1',
        classification='ADMITTED_COMPLETE_READ_ONLY_OPERATOR_DIAGNOSTIC_ONLY',audit_seal=pin(OUT/'seal.json'),
        actual_external_terminal_evidence=pin(path),full_stdout=pin(stdout),full_stderr=pin(stderr),
        findings=pin(OUT/'audit/findings.json'),scope=SCOPE)


def tiny_controls():
    """Pure memory controls only; never reads production operands or solves."""
    examples=[b'',struct.pack('<4I',0,0x80000000,0x7fc00001,0xffffffff),bytes(range(256))]
    for data in examples:
        stored=zlib.compress(data,level=1);decoder=zlib.decompressobj();decoded=decoder.decompress(stored,len(data)+1)
        if decoded!=data or not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
            raise AssertionError('pure bytecodec positive control')
    for stored,limit in [(zlib.compress(b'ab')[:-1],3),(zlib.compress(b'ab')+b'extra',3),(zlib.compress(b'ab'),1)]:
        decoder=zlib.decompressobj();decoded=decoder.decompress(stored,limit)
        if decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail and decoded==b'ab' and len(decoded)==2:
            raise AssertionError('pure bytecodec negative control did not reject')
    signed=signed_counts(typed(struct.pack('<4I',0,0x80000000,0x7fc00001,0xbf800000),'f'),32)
    if signed!=dict(positive=0,negative=1,positive_zero=1,negative_zero=1,nonfinite=1,word_width_bits=32):
        raise AssertionError('original signed/zero/nonfinite inventory control')
    if mirror_matches([1.0],struct.pack('<f',2.0)): raise AssertionError('radial mirror mutation accepted')
    if not mirror_matches([-0.0],struct.pack('<I',0x80000000)): raise AssertionError('negative zero mirror lost')
    return dict(classification='PURE_MEMORY_CODEC_AND_WORD_BOUNDARY_CONTROLS_ONLY',positive_cases=5,negative_cases=4,
        project_inputs_read=False,transport_calls=0,linear_solves=0,replays=0,scientific_qualification=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('declare','run','worker','admit-diagnostic','tiny-controls'))
    parser.add_argument('--sha256');parser.add_argument('--terminal-evidence',type=Path);parser.add_argument('--terminal-evidence-sha256')
    args=parser.parse_args()
    if args.action=='declare': declare()
    elif args.action=='tiny-controls': print(json.dumps(tiny_controls()))
    elif not args.sha256: parser.error('actual frozen declaration SHA (or successful seal for admit-diagnostic) required')
    elif args.action=='admit-diagnostic':
        if not args.terminal_evidence or not args.terminal_evidence_sha256: parser.error('actual Root exit0 terminal file and independently supplied SHA required')
        print(json.dumps(diagnostic_admission(args.sha256,args.terminal_evidence,args.terminal_evidence_sha256)))
    else: {'run':run,'worker':worker}[args.action](args.sha256)
