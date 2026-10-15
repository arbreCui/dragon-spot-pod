"""Complete genuine cp314 SciPy INPUT admission for the new cold environment.

Only normal imports are permitted. This helper never calls a numerical SciPy
function, a project API, a constructor, a solver, or a child. Complete package
bytes and its exact namespace are freshly checked on each explicit admission;
no cross-phase filesystem cache or MRO/fixture/scientific credit is supplied.
"""
import copy
import hashlib
import importlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import stat
import sys

ROOT = Path('/Users/wen/spot')
DEPENDENCY_ROOT = ROOT/'validation/artifacts/axial-material-cold-cp314-scipy-dependency-20261008'
TARGET = DEPENDENCY_ROOT/'target'
MANIFEST = DEPENDENCY_ROOT/'environment_manifest.json'
MANIFEST_SHA = '1038450822d73d1b20c369b639d4991021bfb3121df83eb1a02b1dcf8f9c514b'
SCHEMA = 'AXMAT_GENUINE_SCIPY_CP314_COMPLETE_DEPENDENCY_INPUT_V1'
WHEEL_SHA = '3fd1fcdab3ea951b610dc4cef356d416d5802991e7e32b5254828d342f7b7e0b'
WHEEL_NAME = 'scipy-1.17.1-cp314-cp314-macosx_14_0_arm64.whl'
THREADS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
           'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
PYTHON = '/opt/homebrew/Cellar/python@3.14/3.14.4_1/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
NUMPY_ROOT = '/opt/homebrew/lib/python3.14/site-packages/numpy'


def valid_sha(value):
    if not isinstance(value,str) or re.fullmatch('[0-9a-f]{64}',value) is None or value=='0'*64:
        raise ValueError('independently fixed nonzero SHA256 required')
    return value


def ordinary(path, *, directory=False):
    p=Path(path)
    if not p.is_absolute() or '..' in p.parts:
        raise ValueError('ordinary absolute dependency path required')
    for ancestor in reversed((p,*p.parents)):
        info=ancestor.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise ValueError('dependency path or ancestor is an alias: '+str(ancestor))
        if ancestor!=p and not stat.S_ISDIR(info.st_mode):
            raise ValueError('dependency ancestor is not a directory')
    info=p.lstat()
    if not (stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)):
        raise ValueError('ordinary dependency endpoint kind differs')
    return p


def identity(info):
    return (info.st_dev,info.st_ino,info.st_size,info.st_mtime_ns,info.st_ctime_ns,info.st_mode,info.st_nlink)


def digest(path):
    p=ordinary(path);before=p.lstat()
    descriptor=os.open(p,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0))
    try:
        first=os.fstat(descriptor)
        if not stat.S_ISREG(first.st_mode) or identity(before)!=identity(first):
            raise ValueError('dependency pathname/opened file identity changed')
        h=hashlib.sha256();count=0
        with os.fdopen(descriptor,'rb',closefd=False) as stream:
            while block:=stream.read(8*2**20):
                h.update(block);count+=len(block)
        last=os.fstat(descriptor);after=p.lstat()
        if (identity(first)!=identity(last) or identity(last)!=identity(after)
                or count!=first.st_size or not stat.S_ISREG(after.st_mode)):
            raise ValueError('dependency file or pathname changed while reading')
        return h.hexdigest()
    finally:
        os.close(descriptor)


def require(path, expected):
    p=ordinary(path)
    if digest(p)!=valid_sha(expected):
        raise ValueError('complete dependency bytes changed: '+str(p))
    return p


def strict_json(path, expected):
    p=require(path,expected)
    def pairs(rows):
        result={}
        for key,value in rows:
            if key in result:raise ValueError('duplicate dependency JSON key')
            result[key]=value
        return result
    def invalid(value):
        raise ValueError('nonfinite dependency JSON value: '+value)
    with p.open('rb') as stream:
        raw=stream.read()
    if hashlib.sha256(raw).hexdigest()!=expected:
        raise ValueError('dependency document changed between pinned reads')
    value=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=invalid)
    json.dumps(value,allow_nan=False)
    return value


def add_expected(files,path,expected):
    path=str(Path(path));valid_sha(expected)
    if not Path(path).is_absolute() or '..' in Path(path).parts:
        raise ValueError('typed absolute expected dependency path required')
    if path in files and files[path]!=expected:
        raise ValueError('dependency expected SHA conflict: '+path)
    files[path]=expected


def exact_namespace(expected):
    if (type(expected) is not dict or set(expected)!=set(('root','files','directories','symlinks'))
            or expected['root']!=str(TARGET) or expected['symlinks']!={}
            or type(expected['files']) is not dict or type(expected['directories']) is not list):
        raise ValueError('complete ordinary SciPy target namespace required')
    ordinary(TARGET,directory=True)
    files={};directories=[]
    for p in sorted(TARGET.rglob('*')):
        rel=p.relative_to(TARGET).as_posix();info=p.lstat()
        if stat.S_ISDIR(info.st_mode):
            ordinary(p,directory=True);directories.append(rel)
        elif stat.S_ISREG(info.st_mode):
            files[rel]=digest(p)
        else:
            raise ValueError('SciPy target contains alias/nonregular member')
    directories.sort()
    if files!=expected['files'] or directories!=expected['directories']:
        raise ValueError('complete SciPy package namespace changed')
    return dict(regular_files=len(files),directories=len(directories),symlinks=0)


def normal_import_admission(manifest, files):
    if (sys.flags.optimize!=0 or 'PYTHONOPTIMIZE' in os.environ
            or str(Path(sys.executable).resolve())!=PYTHON
            or platform.python_version()!='3.14.4'
            or os.environ.get('PYTHONPATH')!=str(TARGET)
            or str(TARGET) not in sys.path
            or any(os.environ.get(k)!='1' for k in THREADS)
            or os.environ.get('PYTHONDONTWRITEBYTECODE')!='1'):
        raise ValueError('explicit original producer/threads and exact SciPy PYTHONPATH required')
    expected=TARGET/'scipy/__init__.py'
    old=sys.modules.get('scipy')
    if old is not None and (getattr(old,'__file__',None)!=str(expected)
            or old.__spec__ is None or old.__spec__.origin!=str(expected)):
        raise ValueError('foreign preexisting SciPy normal binding')
    spec=importlib.util.find_spec('scipy')
    if spec is None or spec.origin!=str(expected):
        raise ValueError('normal SciPy resolution differs from declared target')
    np=importlib.import_module('numpy')
    if np.__version__!='2.4.4' or str(Path(np.__file__).parent.resolve())!=NUMPY_ROOT:
        raise ValueError('original NumPy2.4.4 path/version changed')
    scipy=importlib.import_module('scipy')
    integrate=importlib.import_module('scipy.integrate')
    special=importlib.import_module('scipy.special')
    if scipy.__version__!='1.17.1' or scipy.__file__!=str(expected):
        raise ValueError('declared genuine SciPy version/source changed')
    for module_name,module in list(sys.modules.items()):
        if module_name!='scipy' and not module_name.startswith('scipy.'):
            continue
        source=getattr(module,'__file__',None)
        if source is None:continue
        p=ordinary(source)
        if not p.is_relative_to(TARGET) or files.get(str(p)) is None:
            raise ValueError('loaded SciPy module lacks an independent expected owner')
        require(p,files[str(p)])
        if module.__spec__ is None or module.__spec__.origin!=str(p):
            raise ValueError('actual SciPy module spec/source identity differs')
    for module,name in ((integrate,'quad'),(integrate,'quad_vec'),(special,'exprel'),(special,'hyp1f1')):
        if not callable(getattr(module,name,None)):
            raise ValueError('genuine required SciPy public symbol absent')
    return dict(python='3.14.4',numpy='2.4.4',scipy='1.17.1',
        actual_scipy_root=str(TARGET/'scipy'),actual_PYTHONPATH=str(TARGET),
        required_symbols=['scipy.integrate.quad','scipy.integrate.quad_vec','scipy.special.exprel','scipy.special.hyp1f1'],
        numerical_functions_called=False,project_API_or_constructor_or_child_called=False,
        MRO_or_fixture_or_scientific_credit=False)


def dependency_admission(*, require_import=True):
    m=strict_json(MANIFEST,MANIFEST_SHA)
    if (type(m) is not dict or m['schema']!=SCHEMA
            or m['classification']!='GENUINE_COMPLETE_PACKAGE_CODE_ENVIRONMENT_INPUT_ONLY'
            or m['dependency_root']!=str(DEPENDENCY_ROOT) or m['target_root']!=str(TARGET)
            or m['python_executable']!=PYTHON or m['python_version']!='3.14.4'
            or m['numpy_version']!='2.4.4' or m['numpy_root']!=NUMPY_ROOT
            or m['expected_PYTHONPATH']!=str(TARGET)
            or m['wheel']!=dict(path=str(DEPENDENCY_ROOT/'wheels'/WHEEL_NAME),sha256=WHEEL_SHA)
            or m['upstream']!=dict(project_page='https://pypi.org/project/scipy/1.17.1/',
                filename=WHEEL_NAME,sha256=WHEEL_SHA,version='1.17.1',python_tag='cp314',
                abi_tag='cp314',platform_tag='macosx_14_0_arm64')
            or type(m['files']) is not dict
            or any(m[k] is not False for k in ('original_numpy_or_python_modified',
                'installation_scripts_executed','project_API_or_controller_or_constructor_executed',
                'cold_MRO_or_fixture_credit','native_transport_executed','AAA_accuracy_qualified',
                'ABA_admitted','scientific_qualification'))):
        raise ValueError('genuine whole cp314 dependency INPUT manifest changed')
    expected={str(TARGET/name):wanted for name,wanted in m['target_namespace']['files'].items()}
    add_expected(expected,m['wheel']['path'],m['wheel']['sha256'])
    if expected!=m['files']:
        raise ValueError('complete manifest file map differs from full package plus wheel')
    before=exact_namespace(m['target_namespace'])
    for path,wanted in expected.items():require(path,wanted)
    imported=normal_import_admission(m,expected) if require_import else None
    after=exact_namespace(m['target_namespace'])
    require(MANIFEST,MANIFEST_SHA)
    if before!=after:raise ValueError('SciPy complete namespace changed during admission')
    add_expected(expected,MANIFEST,MANIFEST_SHA)
    return dict(schema='AXMAT_COMPLETE_SCIPY_CODE_ENVIRONMENT_INPUT_ADMISSION_V1',
        admission='SCIPY_CODE_ENVIRONMENT_INPUT_ONLY',
        manifest=dict(path=str(MANIFEST),sha256=MANIFEST_SHA),files=expected,
        target_namespace=m['target_namespace'],expected_PYTHONPATH=str(TARGET),
        normal_import=imported,whole_manifest_is_immutable_INPUT=True,
        native_transport_or_fixture_or_scientific_credit=False)


def expanded_environment(original, original_descriptor, admitted, helper_descriptor):
    if (original['schema']!='AXMAT_EXACT_OFFLINE_REPLAY_ENVIRONMENT_V1'
            or original['python_version']!='3.14.4' or original['numpy_version']!='2.4.4'
            or original['executable']!=PYTHON or original['numpy_root']!=NUMPY_ROOT
            or len(original['files'])!=430
            or admitted['admission']!='SCIPY_CODE_ENVIRONMENT_INPUT_ONLY'):
        raise ValueError('complete unmodified original producer environment required')
    if strict_json(original_descriptor['path'],original_descriptor['sha256'])!=original:
        raise ValueError('passed original environment differs from complete pinned document')
    require(helper_descriptor['path'],helper_descriptor['sha256'])
    result=copy.deepcopy(original);files=result['files']
    for path,wanted in admitted['files'].items():add_expected(files,path,wanted)
    add_expected(files,helper_descriptor['path'],helper_descriptor['sha256'])
    result['cold_scipy_dependency']=dict(manifest=admitted['manifest'],
        original_environment=original_descriptor,helper=helper_descriptor,
        expected_PYTHONPATH=str(TARGET),whole_target_namespace=admitted['target_namespace'],
        original_430_expected_entries_retained_unchanged=True,
        additional_dependency_only_no_science_or_fixture_credit=True)
    restored=copy.deepcopy(result);restored['files']=copy.deepcopy(original['files'])
    del restored['cold_scipy_dependency']
    if restored!=original:
        raise ValueError('environment changed outside explicit complete dependency extension')
    return result
