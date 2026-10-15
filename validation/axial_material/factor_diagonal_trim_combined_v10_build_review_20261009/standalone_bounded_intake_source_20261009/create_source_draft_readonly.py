from pathlib import Path
import ast
import difflib
import hashlib
import json
import os

R=Path('/Users/wen/spot'); A=R/'validation/artifacts'
D=Path('/private/tmp/axmat-factor-diagonal-trim-v10-bounded-runtime-input-intake-source-draft-20261009')
B=R/'validation/axial_material/cold_owned_specs_last_cprime_trim_component_input_intake_binding_20261009.json'
binding=json.loads(B.read_text())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
H9=next(Path(p) for p in binding['intake_proof_files'] if p.endswith('/host.py'))
P9=next(Path(p) for p in binding['intake_proof_files'] if p.endswith('/postterminal_recorder.py'))
assert sha(H9)==binding['intake_proof_files'][str(H9)]=='180053eb92dbe4ff05ee87db75056ee2debca057aecd1b314e6ed648a9096aae'
assert sha(P9)==binding['intake_proof_files'][str(P9)]=='5bd181e59b3229398ec7725e8513da5cf055791400522935f5ebfc2b9bd0d03e'
F=R/'validation/axial_material/prepare_historical_input_owned_specs_factor_diagonal_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v10.py'
F_SHA='c55ca2680d9e1326979649f835d9612a8fd80df5aecee1adc25765c419329efc'
OUT=A/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-factor-diagonal-trim-live-resource-scopes-v10-20261009'
TERM=A/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-owned-specs-factor-diagonal-trim-live-resource-scopes-v10-20261009'
NEWBASE=Path('/private/tmp/axmat-factor-diagonal-trim-v10-standalone-bounded-runtime-api-intake-20261009')
EVIDENCE=A/'axial-material-owned-specs-factor-diagonal-trim-v10-standalone-bounded-runtime-api-intake-evidence-20261009'
HOST=D/'axmat_factor_diagonal_trim_v10_standalone_bounded_runtime_api_intake_host_20261009.py'
RECORDER=D/'axmat_factor_diagonal_trim_v10_standalone_bounded_runtime_api_intake_postterminal_recorder_20261009.py'
STDOUT=Path('/private/tmp/axmat-factor-diagonal-trim-v10-standalone-bounded-runtime-api-intake-host-20261009.stdout')
STDERR=STDOUT.with_suffix('.stderr')
KNOWN={'DECL_SHA':'32370a3b0daee193b48a70de428397ccb3a65793fbefc4f5d60b8698d592356a',
    'SEAL_SHA':'3d1094466cb03a08d3bdb08eee0a1f4f3c2b75bb676400beaf5fe7a4892001b5',
    'RUN_SHA':'aec9364827742e68d545ef7ea63ad7d656201c9de13938a1ddceb4b13bbc2bd9',
    'PREP_SHA':'defbc6c30603c334f7c1f8c883c4fb4af6c8fb6cc7ea2ae8df41591be0872658'}
pinfiles={F:F_SHA,OUT/'declaration.json':KNOWN['DECL_SHA'],OUT/'seal.json':KNOWN['SEAL_SHA'],
    TERM/'terminal_return.json':KNOWN['RUN_SHA'],TERM/'declaration_terminal_return.json':KNOWN['PREP_SHA'],
    OUT/'runtime/Dragon':'39a372accd844132ca811ef04b984d8663a353068e19035795d4a028ea108256'}
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p,wanted=None):
    assert p.is_file() and not p.is_symlink()
    before=identity(p.stat());digest=sha(p);after=identity(p.stat());assert before==after
    if wanted is not None:assert digest==wanted,(p,digest,wanted)
    return dict(path=str(p),sha256=digest,identity=after)
actualpins=[pin(p,w) for p,w in pinfiles.items()]
decl=json.loads((OUT/'declaration.json').read_text())
PYTHON=decl['build_python_executable']
assert PYTHON=='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12'
F_tree=ast.parse(F.read_text()); prefix=next(ast.literal_eval(n.value) for n in F_tree.body
    if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='PREFIX' for x in n.targets))
for p in [NEWBASE,EVIDENCE,STDOUT,STDERR]:assert not os.path.lexists(p),p
hostold=H9.read_text(); recold=P9.read_text()
def line(source,key):
    rows=[x for x in source.splitlines(keepends=True) if x.startswith(key+'=')]
    assert len(rows)==1,(key,rows)
    return rows[0]
def swap(source,changes,label):
    edits=[]
    for key,new in changes:
        old=line(source,key);new=new+'\n';assert source.count(old)==1
        source=source.replace(old,new,1);edits.append(dict(region=label+':'+key,old=old,new=new))
    return source,edits
host,he=swap(hostold,[
    ('DRAFT_STATUS',"DRAFT_STATUS='UNREADY_SOURCE_ONLY_V10_STANDALONE_INPUT_DRAFT'"),
    ('FACTORY','FACTORY=Path('+repr(str(F))+')'),('FACTORY_SHA','FACTORY_SHA='+repr(F_SHA)),
    ('OUT','OUT=Path('+repr(str(OUT))+')'),('TERM','TERM=Path('+repr(str(TERM))+')'),
    ('SEAL_SHA','SEAL_SHA='+repr(KNOWN['SEAL_SHA'])),('RUN_SHA','RUN_SHA='+repr(KNOWN['RUN_SHA'])),
    ('PREP_SHA','PREP_SHA='+repr(KNOWN['PREP_SHA'])),('BASE','BASE=Path('+repr(str(NEWBASE))+')'),
    ('DECL_SHA','DECL_SHA='+repr(KNOWN['DECL_SHA']))],'host_identity')
old='if DRAFT_STATUS!="READY_REVIEWED_TRIM_V9_STANDALONE_INPUT_ONLY":'
new='if DRAFT_STATUS!="READY_REVIEWED_FACTOR_DIAGONAL_TRIM_V10_STANDALONE_INPUT_ONLY":'
assert host.count(old)==1;host=host.replace(old,new,1);he.append(dict(region='host_ready_status_label',old=old,new=new))
rec,re=swap(recold,[
    ('DRAFT_STATUS',"DRAFT_STATUS='UNREADY_SOURCE_ONLY_V10_POSTTERMINAL_RECORDER_DRAFT'"),
    ('BASE','BASE=Path('+repr(str(NEWBASE))+')'),('OUT','OUT=Path('+repr(str(EVIDENCE))+')'),
    ('HOST','HOST=Path('+repr(str(HOST))+')'),('HOST_SHA','HOST_SHA=None'),
    ('COMPONENT_TERM','COMPONENT_TERM=Path('+repr(str(TERM))+')'),
    ('DECL_SHA','DECL_SHA='+repr(KNOWN['DECL_SHA'])),('SEAL_SHA','SEAL_SHA='+repr(KNOWN['SEAL_SHA'])),
    ('RUN_SHA','RUN_SHA='+repr(KNOWN['RUN_SHA'])),('PREP_SHA','PREP_SHA='+repr(KNOWN['PREP_SHA'])),
    ('API_RETURN_SHA','API_RETURN_SHA=None'),
    ('CMD','CMD=['+repr(PYTHON)+','+repr(str(F))+",'admit','--sha256',SEAL_SHA,'--terminal-evidence',str(COMPONENT_TERM/'terminal_return.json'),'--terminal-evidence-sha256',RUN_SHA]")],
    'recorder_identity')
old9='AXMAT_HISTORICAL_INPUT_OWNED_SPECS_LAST_CPRIME_TRIM_COMBINED_PHYSICAL_DEDUP_RUNTIME_LIVE_RESOURCE_SCOPES_V9_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1'
schema=prefix+'_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1'
assert rec.count(old9)==1;rec=rec.replace(old9,schema,1);re.append(dict(region='recorder_actual_body_schema_identity',old=old9,new=schema))
old="stdout=Path('/private/tmp/axmat-trim-v9-standalone-bounded-runtime-api-intake-host-20261009.stdout');"
new='stdout=Path('+repr(str(STDOUT))+');'
assert rec.count(old)==1;rec=rec.replace(old,new,1);re.append(dict(region='recorder_host_stdout_identity',old=old,new=new))
def inverse(new,edits,old):
    for e in reversed(edits):
        assert new.count(e['new'])==1,e['region'];new=new.replace(e['new'],e['old'],1)
    assert new==old
inverse(host,he,hostold);inverse(rec,re,recold)
for text in [host,rec]:ast.parse(text)
for p,text in [(HOST,host),(RECORDER,rec)]:
    with p.open('x') as f:f.write(text)
for p,old,new in [(D/'host_identity_only.diff',hostold,host),(D/'recorder_identity_only.diff',recold,rec)]:
    p.write_text(''.join(difflib.unified_diff(old.splitlines(keepends=True),new.splitlines(keepends=True),fromfile='V9_actual_mother',tofile='V10_UNREADY_SOURCE_DRAFT')))
sourceproof=dict(schema='AXMAT_V10_STANDALONE_INTAKE_SOURCE_ONLY_EXACT_IDENTITY_RETARGET_V1',status='UNREADY_SOURCE_DRAFT',
    host=dict(mother=pin(H9),candidate=pin(HOST),edits=he,complete_source_inverse_byteexact=True),
    recorder=dict(mother=pin(P9),candidate=pin(RECORDER),edits=re,complete_source_inverse_byteexact=True),
    allowed_changes='Only explicit version/path/actual-component-pin/readiness identity bindings; whole executable body restored by complete inverse',
    helper=pin(Path('/private/tmp/axmat_root_historical_owned_specs_combined_runtime_actual_bound_recorder_20261007.py'),
        '0b8a9a0a3b71bdea15269a14e54011d142e00c92979fbedef8ade3bcac7ec047'),
    actual_combined_component_pins=actualpins,binding_locator=pin(B),
    host_API_command=[PYTHON,str(F),'admit','--sha256',KNOWN['SEAL_SHA'],'--terminal-evidence',str(TERM/'terminal_return.json'),'--terminal-evidence-sha256',KNOWN['RUN_SHA']],
    API_command_token_count=9,standard_three_keyword_arguments=['seal_sha','terminal_evidence','terminal_evidence_sha256'],
    host_launch_source_command=[PYTHON,str(HOST)],host_stdout_path=str(STDOUT),host_stderr_path=str(STDERR),
    host_complete_environment=dict(PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=None,PYTHONOPTIMIZE=None,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',NUMEXPR_NUM_THREADS='1'),
    environment_boundary='Standalone combined intake is original buildPython3.12; later coldproducerPython3.14 is separate and not silently transplanted',
    caps=dict(total_wall_seconds=1800,stage_wall_seconds=600,RSS_cap_mib=512,threads=1,children=1,retries=0),
    retained_host_guards=['Canonical formal producer fullSHA+require_ready; full declaration/seal/RootRUN/PREP requirements','Exact genuine OwnRSSSerialExecutor.__bases__=(current SerialExecutor,) and original direct supervisor/parent source pins','Same copied genuine bounded helper/constructor/resources; serial onechild ownPID RSS/liveness cleanup','Original standard9token CLI admit; whole typed INPUT-only API return and full actual command/stage/watch/cleanup','Original all physics/native/science false flags,full1800/600/512+allinput/resource gates'],
    retained_recorder_guards=['No producer API/child/coldcontroller run; pinned pure recorder helper byteexact','CLI actual tool facts supplied byRoot only after truehostexit0; exact source/result/watch/stdout/body andwhole API logSHA','Payload9 copied exact, independent Root10 receipt,whole inventory/namespace andcomplete original pins','Unknown HOST_SHA/API_RETURN_SHA remainNone; DRAFT_UNREADY guard prevents execution'],
    future_actual_tool=dict(initial_chunk_id=None,session_id=None,terminal_chunk_id=None,actual_exit_code=None,actual_terminal_return_observed=None,
        actual_full_host_stdout_sha256=None,actual_full_host_stderr_sha256=None,actual_API_whole_return_sha256=None,
        actual_watchdog_sha256=None,actual_child_pid=None,actual_child_returncode=None,actual_child_peak_RSS_mib=None,
        actual_host_elapsed_seconds=None,actual_recorded_root_receipt_sha256=None),
    prospective_new_evidence_root=str(EVIDENCE),prospective_runtime_output_root=str(NEWBASE),
    future_roots_and_streams_absent={str(p):not os.path.lexists(p) for p in [NEWBASE,EVIDENCE,STDOUT,STDERR]},
    host_requires_separate_source_review_and_READY_revision_before_execution=True,recorder_only_bind_after_actual_success=True,
    project_written=False,business_roots_created=False,business_imported=False,host_executed=False,recorder_executed=False,
    original_mothers_not_modified=True,cold_controller_prepared=False,AAA_accuracy_qualified=False,ABA_admitted=False)
(D/'SOURCE_IDENTITY_INVERSE_AND_FUTURE_NONE.json').write_text(json.dumps(sourceproof,ensure_ascii=False,indent=2)+'\n')
(D/'STOPPED_handoff.json').write_text(json.dumps(dict(status='UNREADY_SOURCE_ONLY',candidate_host=pin(HOST),candidate_recorder=pin(RECORDER),
    source_inverse_report=pin(D/'SOURCE_IDENTITY_INVERSE_AND_FUTURE_NONE.json'),future_actual_tool=sourceproof['future_actual_tool'],
    project_written=False,host_executed=False,recorder_executed=False),indent=2)+'\n')
print(json.dumps(dict(status='UNREADY_SOURCE_ONLY',host_sha256=sha(HOST),recorder_sha256=sha(RECORDER),
    source_inverse_sha256=sha(D/'SOURCE_IDENTITY_INVERSE_AND_FUTURE_NONE.json'),host_edit_regions=len(he),recorder_edit_regions=len(re),
    build_python=PYTHON,API_argv_tokens=9,host_executed=False,recorder_executed=False,project_written=False)))
