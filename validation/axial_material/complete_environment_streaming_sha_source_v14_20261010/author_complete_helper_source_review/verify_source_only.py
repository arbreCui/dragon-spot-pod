"""Pure AST/text/SHA/source identity audit. Never import/call the helper."""
import ast,hashlib,json,os,stat
from pathlib import Path
D=Path('/private/tmp/axmat_v14_complete_environment_streaming_sha_helper_compatible_source_draft_20261010')
P=Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_source_factor_production.py')
O=D/'complete_environment_streaming_sha_helper_v14.py'
source_paths=[P,O,D/'generate_private_helper_source.py',D/'source_complete_inverse_proof.json',
    Path('/Users/wen/miniforge3/envs/openmc-dev/lib/python3.12/hashlib.py'),
    Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py'),
    Path('/Users/wen/spot/validation/axial_material/sender_contiguous_flux_window_patch_v13.py'),
    Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-contiguous-flux-window-build-admission-v13-20261009/SPOT1P64.f90'),
    Path('/Users/wen/spot/validation/axial_material/qualify_refined_AAA_layered_full.py'),
    Path('/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py')]
seven=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
sha=lambda b:hashlib.sha256(b).hexdigest()
raw={};bindings=[]
for p in source_paths:
    path_before=os.lstat(p)
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        first=os.fstat(fd);assert stat.S_ISREG(first.st_mode)
        chunks=[]
        while True:
            b=os.read(fd,1024*1024)
            if not b:break
            chunks.append(b)
        blob=b''.join(chunks);last=os.fstat(fd)
    finally:os.close(fd)
    path_after=os.lstat(p)
    assert seven(path_before)==seven(first)==seven(last)==seven(path_after) and len(blob)==first.st_size,p
    raw[p]=blob
    bindings.append(dict(path=str(p),sha256=sha(blob),size_bytes=len(blob),path_identity_before=seven(path_before),
        fd_identity_before=seven(first),fd_identity_after=seven(last),path_identity_after=seven(path_after)))
assert sha(raw[P])=='619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'
assert sha(raw[O])=='839ea8cc88e4f10d36b6bd8fcb283c9c774702e4c3688fc8a66831431c1cb5fa'
assert sha(raw[source_paths[5]])=='d2d2c7616d329cd8ffbf30f749de6ef8ae08d294240b653cfe8b92a3fe1c8633'
assert sha(raw[source_paths[6]])=='77c037a14a3852f628344d9a7cdee3b09e757b00420bf78eddcc1f3a17a6f163'
assert sha(raw[source_paths[7]])=='0800cb54194a7736cb0309703dc2d1fe658171ce1496d6c22ac19fb0ebfcfff5'
parent=raw[P].decode();candidate=raw[O].decode();pt=ast.parse(parent);ct=ast.parse(candidate)
proof=json.loads(raw[D/'source_complete_inverse_proof.json']);inverse=candidate
for region in reversed(proof['regions']):
    assert inverse.count(region['after'])==1;inverse=inverse.replace(region['after'],region['before'],1)
assert inverse==parent and len(proof['regions'])==1
def definitions(tree,src):
    out={}
    def visit(node,prefix):
        for c in ast.iter_child_nodes(node):
            if isinstance(c,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                key=prefix+c.name;assert key not in out
                out[key]=dict(source=ast.get_source_segment(src,c),line=c.lineno,kind=type(c).__name__)
                visit(c,key+'.')
            else:visit(c,prefix)
    visit(tree,'');return out
pd=definitions(pt,parent);cd=definitions(ct,candidate)
assert set(pd)<=set(cd)
changed={name for name in pd if pd[name]['source']!=cd[name]['source']};assert changed=={'digest'}
added=sorted(set(cd)-set(pd));assert all(name.startswith('_env_stream_') or name=='complete_environment_digest_context' for name in added)
for name in ('environment','verify','inventory','verify_inventory','modules','guard_admission','check_watch'):
    assert pd[name]['source']==cd[name]['source'],name
def assignments(t,src):
    return {n.id:ast.get_source_segment(src,node)for node in t.body if isinstance(node,ast.Assign)
        for target in node.targets for n in ast.walk(target)if isinstance(n,ast.Name)}
pa=assignments(pt,parent);ca=assignments(ct,candidate)
assert set(pa)<=set(ca) and all(ca[name]==segment for name,segment in pa.items())
origimports=[ast.get_source_segment(parent,n)for n in pt.body if isinstance(n,(ast.Import,ast.ImportFrom))]
newimports=[ast.get_source_segment(candidate,n)for n in ct.body if isinstance(n,(ast.Import,ast.ImportFrom))]
assert all(n in newimports for n in origimports)
assert ast.get_source_segment(parent,pt.body[-1])==ast.get_source_segment(candidate,ct.body[-1])
digestnode=next(n for n in ct.body if isinstance(n,ast.FunctionDef)and n.name=='digest')
parentdigest=next(n for n in pt.body if isinstance(n,ast.FunctionDef)and n.name=='digest')
assert ast.get_source_segment(candidate,digestnode.body[-1])==ast.get_source_segment(parent,parentdigest.body[0])
assert not any(isinstance(n,ast.ClassDef) and n.name not in pd for n in ct.body)
mapping=[dict(name=name,status='ADDED_PRIVATE_DIGEST_SUPPORT' if name in added else 'MODIFIED_DIGEST_ONLY' if name=='digest' else 'BYTEEXACT_ORIGINAL',
    line=cd[name]['line'],sha256=sha(cd[name]['source'].encode()))for name in sorted(cd)]
report=dict(schema='AXMAT_V14_COMPLETE_ENVIRONMENT_STREAM_SHA_HELPER_PURE_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_UNREADY',
    parent=proof['parent'],candidate=proof['candidate'],region_count=1,complete_inverse_byteexact=True,
    original_all_defs=len(pd),byteexact_original_defs=len(pd)-1,modified_original_defs=['digest'],added_private_defs=added,
    definition_mapping=mapping,all_original_global_assignments_byteexact=True,all_original_imports_retained=True,original_cli_byteexact_retained=True,
    original_environment_verify_inventory_modules_guard_and_mathematics_byteexact=True,genuine_supervisor_class_or_MRO_modified=False,
    protocol=dict(context_API='complete_environment_digest_context(native_library_aliases=None)',buffer_bytes=4194304,
      stream_adapter='_env_stream_open(path) -> Path(path).open(rb, buffering=0)',
      default_outside_scope='Exact original fresh file_digest body; no memo or4MiB buffer reused',
      relative_inputs='Join with fixed entry cwd to an absolute literal preserving ..; original Path(path).open semantics; no resolve/abspath folding of memo/open keys',
      alias_semantics='Every actual symlink hop has fresh full7ID/readlink; target/fd full7ID; ordinary directories only dev/ino/mode to preserve unrelated writes',
      full_read='Single-thread readinto until0; exact integer0..buffer-capacity; short positive continues; exact bytecount equals fstat size; fd/path/alias before-after equal',
      same_scope_memo='Only repeated complete absolute literal plus its independently verified snapshot; no sameSHA/differentpath or cross-scope reuse',
      cleanup='Normal and exception finally release view, clear buffer/memo/alias snapshots, reset active state and release lock',
      guards='Reentry/concurrent scopes reject; PID/thread/cwd owner binding; all registered native aliases rechecked on normal exit; initial alias observation failures deferred to preserve old files-first guard'),
    necessary_factory_integration=[
      'Normal import only installed canonical validation/axial_material/complete_environment_streaming_sha_helper_v14.py; ROOT expression remains original __file__.parents[2]. Never import TMP or SOURCE copy as a complete business helper.',
      'Use with privatehelper.complete_environment_digest_context(d[native_library_aliases]): privatehelper.environment(d, require_build_interpreter=...). Pass every original declared native alias, including ones with no digest owner.',
      'Keep original parent helper() modules/classes/MRO/parent API calls and every per-stage boundary. No frozen helper globals or class monkeypatch.',
      'Declare/freeze/copy/pin new helper plus actual meaningful helper-only controls in new V14 factory; full original86 and unchanged resource/math scope remain required. All new success pins stay unknown until actual closed success.'
    ],
    source_identities=bindings,all_sources_seven_identity_before_after_equal=True,
    limits='No helper import/call, compiler, fixture, benchmark or large payload hashing occurred. Full EOF/buffer/memo behavior needs actual independent helper-only controls; timing benefit/RSS are unproved.',
    inherited_helper_cli_not_a_V14_entrypoint=True,source_status='UNREADY_SOURCE_ONLY_REQUIRES_ROOT_SOURCE_ADMISSION_AND_REAL_HELPER_CONTROLS',
    compiled=False,business_imported=False,business_called=False,fixtures_executed=False,benchmark_executed=False,project_written=False,
    new_compiled_or_runtime_or_whole_INPUT_success_pins=None,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
with (D/'REPORT.json').open('x')as f:json.dump(report,f,indent=2);f.write('\n')
with (D/'source_seven_identity_before_after.json').open('x')as f:json.dump(bindings,f,indent=2);f.write('\n')
print(json.dumps(dict(status=report['status'],candidate_sha256=sha(raw[O]),region_count=1,original_defs=len(pd),
    byteexact_defs=len(pd)-1,added_defs=len(added),report_sha256=sha((D/'REPORT.json').read_bytes()),
    proof_sha256=sha((D/'source_complete_inverse_proof.json').read_bytes()),all_source7IDs_equal=True,business_executed=False)))
