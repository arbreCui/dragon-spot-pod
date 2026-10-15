"""Finite Source/META AST/full-byte review. Never load/execute any candidate."""
import ast,hashlib,json,os,stat
from pathlib import Path
P=Path(__file__).resolve().parent;B=P/'COMPLETE_FIXED_PARENT_SOURCE';checks=[]
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def check(label,value):
    assert type(value)is bool
    checks.append(dict(check=f'{len(checks)+1:05d} '+label,passed=value))
    assert value,label
def read(p):
    s=p.lstat();check('regular singlelink '+str(p.relative_to(P)),stat.S_ISREG(s.st_mode)and s.st_nlink==1)
    raw=p.read_bytes();check('fullEOF '+str(p.relative_to(P)),len(raw)==s.st_size and identity(p.lstat())==identity(s));return raw
def pin(p):
    s=p.lstat();raw=p.read_bytes();assert identity(p.lstat())==identity(s)
    return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),
        identity=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns])
before={str(p):pin(p)for p in sorted(P.rglob('*'))if p.is_file()}
provenance=json.loads(read(P/'COMPLETE_PARENT_PROVENANCE.json'))
manifest=json.loads(read(B/'MANIFEST.json'))
check('complete parent manifest653ce5 retained',pin(B/'MANIFEST.json')['sha256']=='653ce5d8b88a1341acd631891ab8d60b113bf099de4a701dbf086b4bf0dfe2fb')
check('all original162 parent members retained',manifest['member_count']==162 and len(manifest['members'])==162)
mother=Path('/private/tmp/axmat_COMPLETE_aggregation_engine_GENUINE_HOST_UNREADY_SOURCE_20261010_lvgdx_oz')
for m in manifest['members']:
    original=Path(m['path']);copied=B/original.relative_to(mother)
    raw=read(copied)
    check('parent copy full SHA '+str(copied.relative_to(B)),hashlib.sha256(raw).hexdigest()==m['sha256']and len(raw)==m['size_bytes'])
for path in sorted(P.rglob('*')):
    s=path.lstat();check('no alias/special '+str(path.relative_to(P)),not stat.S_ISLNK(s.st_mode)and(stat.S_ISREG(s.st_mode)or stat.S_ISDIR(s.st_mode)))
    if path.suffix=='.py':
        raw=read(path);tree=ast.parse(raw.decode());check('full AST '+str(path.relative_to(P)),isinstance(tree,ast.Module))
def reverse(raw,item):
    lines=raw.decode().splitlines(keepends=True)
    for h in reversed(item['complete_zero_based_hunks']):
        check('inverse full new hunk '+item['candidate']+str(h['new_start0']),lines[h['new_start0']:h['new_end0']]==h['new_full_lines'])
        lines[h['new_start0']:h['new_end0']]=h['old_full_lines']
    old=''.join(lines).encode();check('inverse full original SHA '+item['candidate'],hashlib.sha256(old).hexdigest()==item['original_SHA256'])
    return old
hostproof=json.loads(read(P/'COMPLETE_CONTEXT_GENUINE_HOST_BINDER_FULL_INVERSE.json'))
intermediate=None
for item in hostproof['derivations']:
    raw=read(P/item['candidate']);check('final candidate SHA '+item['candidate'],hashlib.sha256(raw).hexdigest()==item['candidate_SHA256'])
    old=reverse(raw,item)
    if item['candidate']=='complete_observed_old_post_final_XSM_extractor.UNREADY.py':intermediate=old
    else:
        name='complete_final_MICROLIB_MACROLIB_aggregation_genuine_host.UNREADY.py'if 'genuine_host' in item['candidate']else'bind_complete_aggregation_SOURCE_only.UNREADY.py'
        check('whole fixed host/binder restored '+name,old==read(B/name))
proof=json.loads(read(P/'COMPLETE_V23_OLD_XSM_EXTRACTION_SOURCE_INVERSE.json'))
check('native intermediate actually available',type(intermediate)is bytes)
item=dict(candidate='complete_observed_old_post_final_XSM_extractor.UNREADY.py',original_SHA256=proof['original_SHA256'],complete_zero_based_hunks=proof['complete_zero_based_hunks'])
check('native intermediate original author SHA',hashlib.sha256(intermediate).hexdigest()==proof['candidate_SHA256'])
original=reverse(intermediate,item)
native=read(B/'FINITE_ACTUAL_NATIVE_V23_SOURCE_META/Root_bound_complete_native_checker.py')
check('whole frozen V23 native Source restored',original==native)
proof=json.loads(read(P/'COMPLETE_CONTEXT_AWARE_SOURCE_FULL_INVERSE.json'))
for item in proof['derivations']:
    raw=read(P/item['candidate']);check('full derivative SHA '+item['candidate'],hashlib.sha256(raw).hexdigest()==item['candidate_SHA256'])
    old=reverse(raw,item)
    name={'complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py':'complete_final_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py',
        'AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90':'AXMAT_OBSERVATION_MOD.UNREADY.f90',
        'TONDRV.context_observe.UNREADY.f':'TONDRV.observe.UNREADY.f',
        'extract_actual_complete_context_with_SPH_decisions.UNREADY.py':'extract_actual_observation_context.UNREADY.py'}.get(item['candidate'],item['candidate'])
    check('whole original parent Source restored '+name,old==read(B/name))
def definitions(raw):
    tree=ast.parse(raw.decode());lines=raw.decode().splitlines(keepends=True)
    return {n.name:(ast.dump(n,include_attributes=False),''.join(lines[n.lineno-1:n.end_lineno]).encode())for n in tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef))}
old=definitions(native);new=definitions(read(P/'complete_observed_old_post_final_XSM_extractor.UNREADY.py'))
for name,definition in old.items():
    if name not in('Budget','main'):check('native original full def AST+bytes '+name,name in new and new[name]==definition)
old=definitions(read(B/'complete_final_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py'))
new=definitions(read(P/'complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py'))
for name,definition in old.items():
    if name!='main':check('engine original full def AST+bytes '+name,name in new and new[name]==definition)
for filename in('complete_observed_old_post_final_XSM_extractor.UNREADY.py','complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py',
        'complete_context_aware_aggregation_and_oldXSM_genuine_host.UNREADY.py'):
    tree=ast.parse(read(P/filename));assign={n.targets[0].id:ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)and len(n.targets)==1 and
        isinstance(n.targets[0],ast.Name)and n.targets[0].id in('SOURCE_STATUS','SOURCE_BINDING_SHA256','ROOT_BOUND_BINDING_SHA256','BOUND_ADAPTER_PIN','TARGET','OBSERVATION_OPERATION')}
    check('default UNREADY '+filename,assign['SOURCE_STATUS']=='UNREADY_SOURCE_ONLY')
    for key,value in assign.items():
        if key!='SOURCE_STATUS':check('future global None '+filename+key,value is None)
engine=(P/'complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py').read_text()
extractor=(P/'complete_observed_old_post_final_XSM_extractor.UNREADY.py').read_text()
host=(P/'complete_context_aware_aggregation_and_oldXSM_genuine_host.UNREADY.py').read_text()
binder=(P/'bind_complete_context_aware_and_oldXSM_SOURCE_only.UNREADY.py').read_text()
for phrase in('ContextAwareConstruction(saved,evidence,context','self.old_state[8]==1','self.nfiss0*4','LIBDEN_LAMBDA_UNDEFINED_OLD_SLOTS',
    'self.maskl[src]and self.fp.nonzero','full original scatter mathematical scope','range(7)','array(\'I\',[0])*256',
    'array(\'I\',[0])*48','ROOT_MIXTURESVOL_BEFORE','TONDRV_ACTUAL_SPH_CALL_DECISION',
    'same genuinely observed final full micro','full original physical path/key/type/count order','no incomplete original call at complete EOF',
    'self.scalar_intermediate','SOURCE_CONTEXT_NOT_SAVED','raise SystemExit(2 if error is None else 1)'):
    check('explicit full context implementation anchor '+phrase,phrase in engine)
for phrase in('native.walk_table(native.root,tuple(prefix),())','for state in (\'A\',\'B\')','rows.close()',
    "os.environ['SQLITE_TMPDIR']=str(sqltemp)","all_inputs=binding['complete_input_pins']",'raise SystemExit(2)'):
    check('full native extraction entry anchor '+phrase,phrase in extractor)
for phrase in('ROOT_ACTUAL_COMPLETE_CONTEXT_AWARE_MICRO_MACRO_BINDING_V2','OwnRSSSerialExecutor','type(runner)is not full.OwnRSSSerialExecutor',
    'full.OwnRSSSerialExecutor(host,remaining','observed_stage','STAGE_CAP','failure_post_inputs','source_directories','receipt_directories','len(runner.records)==1'):
    check('original genuine supervision retained '+phrase,phrase in host)
for phrase in('old_XSM_extraction','context_aggregation','shape_only','all_snapshot_pairs','actual_context_states',
    'OBSERVATION_OPERATION=operation','ROOT_BOUND_BINDING_SHA256=binding_sha','len(original)==129',
    'PREP cannot stand for BUILD','session_repolled_after_close','observed_terminal','terminal[\'exit_code\']'):
    check('strict Source binder entry anchor '+phrase,phrase in binder)
for p in('context_aware_complete_construction_fragment.UNREADY.py','context_state_check_fragment.UNREADY.py'):
    tree=ast.parse(read(P/p));check('fragments contain no import or standalone candidate execution '+p,
        not any(isinstance(n,(ast.Import,ast.ImportFrom))for n in ast.walk(tree))and all(isinstance(n,(ast.Expr,ast.ClassDef,ast.FunctionDef))for n in tree.body))
for path,expected in before.items():check('complete beforeafter Source/META pin '+str(Path(path).relative_to(P)),pin(Path(path))==expected)
report=dict(schema='AUTHOR_COMPLETE_OLD_XSM_CONTEXT_AWARE_SOURCE_STATIC_REVIEW_V2',
    status='SOURCE_ONLY_STATIC_CHECKS_COMPLETE_UNREADY_NO_EXECUTION_OR_QUALIFICATION',source_only=True,
    check_count=len(checks),checks=checks,all_checks_typed_true=True,all_check_labels_unique=len({r['check']for r in checks})==len(checks),
    default_UNREADY=True,all_future_actual_context_pins_and_Q_None=True,all_complete_fixed_parent_members=162,
    exact_scope=[62,370,8,18,3,32,256,64,6,12,48],complete_scope_unproved_not_reduced=True,
    source_candidates={name:pin(P/name)for name in('complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py',
        'complete_observed_old_post_final_XSM_extractor.UNREADY.py','complete_context_aware_aggregation_and_oldXSM_genuine_host.UNREADY.py',
        'bind_complete_context_aware_and_oldXSM_SOURCE_only.UNREADY.py','AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90')},
    static_review_is_not_independent_peer_or_admission=True,semantic_and_runtime_qualification_not_claimed=True,
    actual_candidate_execution=None,actual_MAT_SPH_oldmacro_observation=None,actual_native_extraction=None,actual_aggregation=None,
    new_Q=None,science_flags_false=True,remaining_specific_gaps=json.loads((P/'COMPLETE_CONTEXT_AWARE_FIELD_PRODUCER_SCOPE_AND_GAPS.json').read_text())['remaining_specific_unqualified_components'],
    no_material_DB_numeric_API_guard_candidate_or_compile_execution=True)
out=P/'AUTHOR_COMPLETE_OLD_XSM_CONTEXT_AWARE_SOURCE_STATIC_REVIEW.json';out.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
print(json.dumps(dict(source_only=True,check_count=len(checks),all_checks_typed_true=True,report=pin(out),candidate_executed=False),allow_nan=False))
