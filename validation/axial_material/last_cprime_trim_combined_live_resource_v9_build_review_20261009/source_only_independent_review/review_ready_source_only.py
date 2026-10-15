"""Read/AST/inverse/metadata only; never execute factory/helper/recorder/watch."""
import ast
import hashlib
import json
import os
import stat
import sys
from pathlib import Path

ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts'
AUTHOR=Path('/private/tmp/axmat_last_cprime_trim_v9_ready_source_admission_candidate_20261009')
BASE=Path('/private/tmp/axmat_last_cprime_trim_v9_identity_source_draft_20261009')
OUT=Path('/private/tmp/axmat_v9_ready_source_independent_review_20261009')
FP=ROOT/'validation/axial_material/prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v8.py'
FC=AUTHOR/'prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v9.py'
RP=Path('/private/tmp/axmat-last-cprime-trim-combined-live-resource-v8-root-execution-20261009/record_root_terminal.py')
RC=AUTHOR/'record_root_terminal.py'
PINS={}
def read(p,expected=None):
    s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
    assert p.is_absolute() and p.parent.resolve(strict=True)==p.parent and stat.S_ISREG(s.st_mode)
    h=hashlib.sha256();parts=[]
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
        fs=os.fstat(f.fileno());assert [fs.st_dev,fs.st_ino]==before[:2]
        while b:=f.read(1024**2):h.update(b);parts.append(b)
    raw=b''.join(parts);s=p.lstat();assert before==[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink] and len(raw)==before[3]
    if expected:assert h.hexdigest()==expected
    PINS[str(p)]=dict(path=str(p),size=len(raw),sha256=h.hexdigest(),identity=before)
    return raw
def obj(p,expected=None):return json.loads(read(p,expected))
def write(name,value):
    with (OUT/name).open('x') as f:json.dump(value,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
def sourcepart(s,n):return ast.get_source_segment(s,n)
def invert(original,candidate,inverse):
    regions=inverse['regions'];prior=-1
    for region in regions:
        a,b=region['candidate_start'],region['candidate_end'];assert a>=prior and candidate[a:b]==region['replacement'];prior=b
    output=candidate
    for r in reversed(regions):output=output[:r['candidate_start']]+r['original']+output[r['candidate_end']:]
    assert output==original
    return len(regions)
def named_assigns(tree):
    result={}
    for n in tree.body:
        if isinstance(n,ast.Assign):
            for target in n.targets:
                if isinstance(target,ast.Name):result[target.id]=n
                elif isinstance(target,(ast.Tuple,ast.List)):
                    for t in target.elts:
                        if isinstance(t,ast.Name):result[t.id]=n
    return result
def scalar(node):
    if isinstance(node,ast.Constant):return node.value
    if isinstance(node,(ast.Tuple,ast.List)):return [scalar(n) for n in node.elts]
    if isinstance(node,ast.BinOp):
        a,b=scalar(node.left),scalar(node.right)
        if isinstance(node.op,ast.Pow):return a**b
        if isinstance(node.op,ast.Mult):return a*b
        if isinstance(node.op,ast.Add):return a+b
    raise ValueError('only literal constant scalar computation allowed')

assert sys.version_info[:2]==(3,12) and __debug__ and sys.dont_write_bytecode
parent=read(FP,'4fc0dc0e794962a371cae55ca210026b008b09879a332d497083f3c856e940a4').decode()
candidate=read(FC,'44789bc288715c34d08dbfa91b9c05dfc78166c2b8fa048bbe0207b273419a46').decode()
mother=read(BASE/FC.name,'f700f43b411904f002a59cddcd879e1aa4e92fa632417e7be0bd7292fbc32ada').decode()
recparent=read(RP,'0fce254f46ac85606569a0343920e6c49fa60dc9674eaeca363dacffec55de4e').decode()
reccandidate=read(RC,'b534c49f046d3869dba07e4101e907bd08de8c61599bc3a05a688a0733de5d9e').decode()
inverse=obj(BASE/'factory_source_inverse.json','b7abdbc9179b8bf0403f88269780253feac3cee0459c200fb5973342d67781a1')
recinverse=obj(BASE/'recorder_source_inverse.json','c23e182f8f7c6f63b5c201f0fa3c07a8aa02ec5a4968dfa672e61ae857620261')
readyinverse=obj(AUTHOR/'ready_vs_f700_complete_byte_inverse.json','e3eb1401ddb915161c3a4b619d0baf779a01e66c6e75eb5370998f66f88f8ba3')
ops=readyinverse['operations'];assert len(ops)==2
restored=candidate;last=-1
for op in ops:
    a,b=op['candidate_start'],op['candidate_end'];assert a>=last and candidate[a:b]==op['candidate_text'];last=b
for op in reversed(ops):restored=restored[:op['candidate_start']]+op['mother_text']+restored[op['candidate_end']:]
assert restored==mother
assert ast.get_source_segment(candidate,ast.parse(candidate).body[0])==ops[0]['candidate_text']
assert ops[1]['candidate_text']=="'READY_REVIEWED_TRIM_COMPONENT_INPUT_REUSE_FORMAL_FACTORY'"
assert invert(parent,mother,inverse)==9 and invert(recparent,reccandidate,recinverse)==2
mother_tree=ast.parse(mother)
for a,b in zip(mother_tree.body[1:],ast.parse(candidate).body[1:]):
    if isinstance(a,ast.Assign) and isinstance(a.targets[0],ast.Name) and a.targets[0].id=='DRAFT_STATUS':
        assert sourcepart(mother,a).split('=',1)[0]==sourcepart(candidate,b).split('=',1)[0]
    else:assert sourcepart(mother,a)==sourcepart(candidate,b) and ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False)
pt,ct=ast.parse(parent),ast.parse(candidate);rp,rc=ast.parse(recparent),ast.parse(reccandidate)
compile(ct,str(FC),'exec');compile(rc,str(RC),'exec')  # syntax only, not execution
allowed={'SOURCE','OUT','TERMINAL','FAMILY','PREFIX','FORMAL_FACTORY','INPUT_HELPERS'}
changed=[];exact_nodes=[]
assert len(pt.body)==len(ct.body)
for a,b in zip(pt.body,ct.body):
    if sourcepart(parent,a)!=sourcepart(candidate,b):
        if isinstance(a,ast.Expr) and isinstance(a.value,ast.Constant) and isinstance(a.value.value,str):changed.append('module_doc')
        else:
            assert isinstance(a,ast.Assign) and isinstance(b,ast.Assign) and len(a.targets)==len(b.targets)==1 and isinstance(a.targets[0],ast.Name) and a.targets[0].id in allowed
            assert [ast.dump(n) for n in a.targets]==[ast.dump(n) for n in b.targets];changed.append(a.targets[0].id)
    else:assert ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False);exact_nodes.append(type(a).__name__)
assert set(changed)==allowed|{'module_doc'} and len(changed)==8
pdf=[n for n in pt.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
cdf=[n for n in ct.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
assert len(pdf)==len(cdf)==65
definition_inventory=[]
for a,b in zip(pdf,cdf):
    assert a.name==b.name and sourcepart(parent,a)==sourcepart(candidate,b) and ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False)
    definition_inventory.append(dict(name=a.name,parent_line=a.lineno,candidate_line=b.lineno,source_sha256=hashlib.sha256(sourcepart(parent,a).encode()).hexdigest(),body_and_AST_exact=True))
pa,ca=named_assigns(pt),named_assigns(ct)
for key,node in pa.items():
    if key not in allowed:assert sourcepart(parent,node)==sourcepart(candidate,ca[key]) and ast.dump(node,include_attributes=False)==ast.dump(ca[key],include_attributes=False)
helpers_old=pa['INPUT_HELPERS'].value;helpers_new=ca['INPUT_HELPERS'].value
assert [scalar(k) for k in helpers_old.keys]==[scalar(k) for k in helpers_new.keys]==['graph','codec','current','checks','ordinary']
for key,a,b in zip(helpers_old.keys,helpers_old.values,helpers_new.values):
    if scalar(key)!='current':assert ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False)
    else:assert scalar(b.elts[1])=='fd3bdb5543044fc71f0acb9799b1c6fcf7709cbbf22342f0931a299af59cee19'
caps={}
for keys,expected in [(('TOTAL_WALL','STAGE_WALL','RSS'),[1800,600,512]),(('RESERVE','HISTORY_CAP','FREE_FLOOR'),[2*2**30,96*2**30,8*2**30])]:
    assert scalar(ca[keys[0]].value)==expected
    caps.update(zip(keys,expected))
assert scalar(ca['THREAD_KEYS'].value)==['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']
assert scalar(ca['TAIL_FIELDS'].value)==['actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources']
assert scalar(ca['INPUT_SPECS_SHA'].value)=='2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa'
funcs={n.name:n for n in cdf}
ready=sourcepart(candidate,funcs['require_ready']);assert "if DRAFT_STATUS != 'READY_REVIEWED_TRIM_COMPONENT_INPUT_REUSE_FORMAL_FACTORY':" in ready and "raise ValueError('UNREADY:" in ready and "if Path(__file__).absolute()!=FORMAL_FACTORY:" in ready
assert scalar(ca['DRAFT_STATUS'].value)==scalar(pa['DRAFT_STATUS'].value)=='READY_REVIEWED_TRIM_COMPONENT_INPUT_REUSE_FORMAL_FACTORY'
for name in ('prepare_build','run_build','declaration_admission','production_admission','load'):
    node=funcs[name];assert isinstance(node.body[0],ast.Expr) and ast.unparse(node.body[0])=='require_ready()'
audit=sourcepart(candidate,funcs['audit_build']);assert 'declaration_admission(' in audit
main=ct.body[-1];assert isinstance(main,ast.If) and ast.unparse(main.body[0])=='require_ready()'
run=sourcepart(candidate,funcs['run_build']);assert "runner.execute(OUT/'audit','audit',commands[-1],STAGE_WALL" in run
assert "len(stages)!=5" in run and "any(s['status']!='PASS' for s in stages)" in run
assert "complete=inventory(OUT);write_new(OUT/'seal.json'" in run and run.index("complete=inventory(OUT);write_new(OUT/'seal.json'")>run.index("write_new(OUT/'driver_result.json',result)")
assert "actual_tail_check='PASS'" in run and "AAA_accuracy_qualified=False,ABA_admitted=False" in run
prep=sourcepart(candidate,funcs['prepare_build']);assert 'declared=set(historical_roots)|{str(SOURCE),str(OUT),str(TERMINAL)}' in prep
assert 'b.validate_history_roots(b.history_roots(sorted(declared),ART),ART)' in prep
assert 'threads=1,numeric_children_at_once=1,retries=0' in prep and 'original_cold_reservation_bytes=20971764748,cold_reservation_reduced=False' in prep
assert 'full.OwnRSSSerialExecutor.__bases__!=(c.SerialExecutor,)' in sourcepart(candidate,funcs['modules'])

# Whole immutable input bodies are data only, not V9 business admission.
specpath=ROOT/'validation/axial_material/combined_runtime_complete_historical_input_specs_20261007.json'
specs=obj(specpath,'2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa')
historical=obj(ART/'axial-material-physical-dedup-combined-runtime-build-20261007/declaration.json','aa3e33a10b64deb947f82fd9f8b19559f9f700f58396e641a4e66def5d4b46a4')
seven=specs['metadata']['historical_actual_components'];assert seven==historical['actual_components'] and len(seven)==7
sevenkeys=['original92','physical','dedup','capture','mathematical_controls_inherited_not_newly_executed','capture_scope_is_original_operator_only','combined_runtime_RSS_not_proved']
assert set(seven)==set(sevenkeys)
trim_original=obj(ROOT/'validation/axial_material/last_cprime_trim_build_review_20261008/actual_complete_production_admission.json','fed2090ee0db4bb718c6c3fbbc9ed520ed9eeddda3fca6b2cadc2f4623edb114')
trim_v8=obj(ART/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-admission-owned-specs-last-cprime-trim-live-resource-scopes-v8-20261009/trim_component_admission_INPUT.json','a4662b853831357c299de0c28d1d19e2a869f81c6308081f6fa1d7833fd797bb')
assert trim_original==trim_v8
read(ROOT/'validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py','1d7c4d7a9ecc4546ceb4c7e0b81562329f874ca5302621ef5fc026f62c7f7643')
helper_inventory=[]
for key,value in zip(helpers_new.keys,helpers_new.values):
    assert isinstance(value,ast.Tuple) and len(value.elts)==2
    expr=value.elts[0];assert isinstance(expr,ast.BinOp) and isinstance(expr.op,ast.Div) and isinstance(expr.left,ast.Name) and expr.left.id=='ROOT'
    hp=ROOT/scalar(expr.right);read(hp,scalar(value.elts[1]));helper_inventory.append(dict(role=scalar(key),**PINS[str(hp)]))
formal_current=ROOT/'validation/axial_material/combined_runtime_current_predicates_final_private_last_uses_20261009.py'
source_current=Path('/private/tmp/axmat_current_predicates_final_private_last_uses_source_candidate_20261009/combined_runtime_current_predicates_final_private_last_uses_20261009.py')
assert read(formal_current,'fd3bdb5543044fc71f0acb9799b1c6fcf7709cbbf22342f0931a299af59cee19')==read(source_current,'fd3bdb5543044fc71f0acb9799b1c6fcf7709cbbf22342f0931a299af59cee19')
helper_review=obj(Path('/private/tmp/axmat_current_predicates_final_private_last_uses_independent_review_20261009/independent_review.json'),'8ec440f04c6074a40db120c838f3630f8cda46bc494d8a0dbfbc46332d50b8b2')
assert helper_review['status']=='PASS'
graph_source=read(ROOT/'validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py','1d7c4d7a9ecc4546ceb4c7e0b81562329f874ca5302621ef5fc026f62c7f7643').decode()
assert '64 * 1024 * 1024' in graph_source or '64*1024*1024' in graph_source or '64 * 2**20' in graph_source or '64*2**20' in graph_source or '67108864' in graph_source

assert len(rp.body)==len(rc.body)
rdefs=[n for n in rp.body if isinstance(n,ast.FunctionDef)];cdefs=[n for n in rc.body if isinstance(n,ast.FunctionDef)]
assert len(rdefs)==len(cdefs)==4
for a,b in zip(rdefs,cdefs):assert sourcepart(recparent,a)==sourcepart(reccandidate,b) and ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False)
assert "assert type(tool['exit_code'])is int and tool['exit_code']==0" in reccandidate
assert reccandidate.index("assert type(tool['exit_code'])is int and tool['exit_code']==0")<reccandidate.index('TERM.mkdir()')
assert "result['classification']=='COMPLETE_COMBINED_RUNTIME_LINK_IDENTITY_ONLY'and result['error']is None" in reccandidate
assert "e['actual_tail_check']=='PASS'and e['actual_elapsed_seconds']<1800 and 0<e['actual_archive_bytes']<2*2**30" in reccandidate
assert "planned_total_stages=5,compiled_or_numeric_stages_started=0" in reccandidate
config=obj(AUTHOR/'config.json','afc40f7a08839839eb724b8a3c6722f66f5d07cf71129a032ac065c0b7be634e')
oldconfig=obj(BASE/'config.json','1ebda93564e525fca46f7153243a6a0084ee4f0375b0d9678305ae2802e0234c')
assert set(config)==set(oldconfig)
assert {k for k in config if config[k]!=oldconfig[k]}=={'factorySha','source_review_status'}
for k in config:
    if k not in ('factorySha','source_review_status'):assert config[k]==oldconfig[k]
T=Path(config['T'])
assert set(p.name for p in T.iterdir())=={'config.json','record_root_terminal.py'}
assert read(T/'config.json','afc40f7a08839839eb724b8a3c6722f66f5d07cf71129a032ac065c0b7be634e')==read(AUTHOR/'config.json','afc40f7a08839839eb724b8a3c6722f66f5d07cf71129a032ac065c0b7be634e')
assert read(T/'record_root_terminal.py','b534c49f046d3869dba07e4101e907bd08de8c61599bc3a05a688a0733de5d9e')==read(RC,'b534c49f046d3869dba07e4101e907bd08de8c61599bc3a05a688a0733de5d9e')
handoff=read(AUTHOR/'SOURCE_ONLY_READY_CANDIDATE_handoff.txt','176b3ed0601378628e065804c0157fac8f8a7bc3858ef0c8536349342cc0d556')
authorreceipts=obj(AUTHOR/'actual_source_and_recipe_tool_receipts.json')
assert authorreceipts['fresh_static_source_recipe_audit_tool']['chunk_id']=='0c8fbe' and type(authorreceipts['fresh_static_source_recipe_audit_tool']['exit_code']) is int and authorreceipts['fresh_static_source_recipe_audit_tool']['exit_code']==0 and authorreceipts['fresh_static_source_recipe_audit_tool']['completed'] is True
assert authorreceipts['actual_factory_or_recorder_or_PREP_RUN_tool'] is None and authorreceipts['actual_formal_copy'] is None
recipe=obj(AUTHOR/'Root_source_admission_recipe.json')
assert recipe['candidate_factory']['sha256']==PINS[str(FC)]['sha256'] and recipe['known_formal_current_helper']['sha256']==PINS[str(formal_current)]['sha256']
assert recipe['actual_PREP_tool'] is recipe['actual_RUN_tool'] is recipe['actual_PREP'] is recipe['actual_RUN'] is recipe['actual_RSS_or_memory_benefit'] is recipe['actual_terminal'] is None
assert recipe['local_parser_candidate_integrated'] is False
future=('declarationSha','prepSha','sealSha','terminalSha','terminalPath','failed_terminal_sha')
assert all(config[k] is None for k in future)
assert config['factorySha']==PINS[str(FC)]['sha256'] and config['source_review_status']=='READY_SOURCE_CANDIDATE_PENDING_INDEPENDENT_REVIEW_AND_ROOT_FORMAL_COPY'
assert config['P']=='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12'
assert config['F']==str(ROOT/'validation/axial_material'/FC.name)
assert config['T']=='/private/tmp/axmat-last-cprime-trim-combined-live-resource-v9-root-execution-20261009'
assert config['R']=='/Users/wen/spot/validation/axial_material/last_cprime_trim_combined_live_resource_v9_build_review_20261009'
absence=[]
for key,var in [('SOURCE','SOURCE'),('OUT','OUT'),('TERM','TERMINAL')]:
    expression=ca[var].value;assert isinstance(expression,ast.BinOp) and isinstance(expression.op,ast.Div)
    path=ART/scalar(expression.right);assert str(path)==config[key] and path.name.endswith('-v9-20261009')
    assert not os.path.lexists(path);absence.append(str(path))
assert not os.path.lexists(config['F'])
assert formal_current.exists() and PINS[str(formal_current)]['sha256']=='fd3bdb5543044fc71f0acb9799b1c6fcf7709cbbf22342f0931a299af59cee19'

oldfailure=obj(ART/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-owned-specs-last-cprime-trim-live-resource-scopes-v8-20261009/terminal_return.json','d4cacd55b43b590647ca9c1e6ec1168c58f8ddea7ec52b925b9048c556497039')
assert oldfailure['returncode']==1 and not oldfailure['scientific_qualification']
assert all(oldfailure[k] is None for k in ('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources'))
assert 'd4cacd55b43b590647ca9c1e6ec1168c58f8ddea7ec52b925b9048c556497039' not in candidate
readonly_names=sorted(str(p) for p in ART.glob('axial-material-*') if p.is_dir())
v8_roots=[ART/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-admission-owned-specs-last-cprime-trim-live-resource-scopes-v8-20261009',ART/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v8-20261009',ART/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-owned-specs-last-cprime-trim-live-resource-scopes-v8-20261009']
assert all(str(p) in readonly_names for p in v8_roots)
for p,expected in list(PINS.items()):read(Path(p),expected['sha256']);assert PINS[p]==expected
write('all_definitions_exact.json',definition_inventory)
write('full_fresh_SHA_identity_pins.json',list(PINS.values()))
write('readonly_dynamic_history_names_not_admission.json',dict(names=readonly_names,readonly_name_count=len(readonly_names),all_old_V8_source_out_terminal_names_present=True,future_actual_V9_effective_resource_root_count=None,source_selection_unchanged=True,no_pruning=True,not_business_resource_admission=True))
report=dict(schema='AXMAT_V9_READY_SOURCE_ADMISSION_INDEPENDENT_SOURCE_METADATA_REVIEW_V1',status='PASS',scope='READY_SOURCE_BYTES_ONLY_ROOT_FORMAL_ADMISSION_ALLOWED_NO_ACTUAL_PREP_RUN',factory=PINS[str(FC)],parent_factory=PINS[str(FP)],identity_only_mother_factory=PINS[str(BASE/FC.name)],recorder=PINS[str(RC)],parent_recorder=PINS[str(RP)],ready_vs_identity_mother_exact_two_regions=True,identity_mother_vs_original_F8_exact_nine_regions=True,final_vs_F8_only_eight_identity_doc_top_nodes=changed,factory_65_top_definitions_byte_AST_exact=True,all_nested_definitions_contained_in_unchanged_top_bodies=True,nonidentity_assignments_and_all_other_nodes_exact=True,DRAFT_STATUS_same_as_original_F8_READY=True,original_strict_json_bytes_exact=True,local_immutable_sharing_parser_not_adopted=True,current_helper_formal_fresh_fd3_and_TMP_source_equal=True,current_helper_prior_independent_source_and_77_tiny_review_bound_not_rerun=PINS[str(Path('/private/tmp/axmat_current_predicates_final_private_last_uses_independent_review_20261009/independent_review.json'))],all5_formal_helpers_fresh_FULL_SHA=helper_inventory,graph_wire_full_schema_and_original_64MiB_limit_source_preserved=True,complete_original_historical_seven_body_same_whole_dict=True,historical_seven_keys=sevenkeys,whole_original_trim_fed209_equals_saved_V8_INPUT_dict=True,trim_contract_functions_and_math_guards_unchanged=True,original_caps=caps,threads1_onechild0retry_unchanged=True,MRO_supervisor_constructor_and_all_guard_timing_unchanged=True,exact5stages_allPASS_before_seal_and4afterseal_tails_unchanged=True,new_SOURCE_OUT_TERM_v9_bindings_match_config=True,formal_factory_and_new_family_roots_observed_absent=absence+[config['F']],all_future_config_actual_witness_fields_None=list(future),Root_T_prepared_only_config_and_recorder_exact=True,READY_status_and_formal_path_guard_before_CLI_and_entrypoint_business_static=True,recorder_only_T_and_PREFIX_two_inverse_regions=True,recorder4defs_exact_and_builtin_integer0_required=True,old_V8_failed_receipt_frozen_no_success_transfer=True,dynamic_history_original_union_function_source_unchanged=True,readonly_history_name_count=len(readonly_names),future_actual_resource_admission_or_root_count=None,author_real_source_only_receipts_checked=True,actual_factory_helper_or_recorder_imported_executed=False,watch_or_probe_started=False,formal_ART_written=False,PREP_RUN_API_ctor_native_called=False,AAA_ABA_combined_native_RSS_credit=False,actual_review_tool_terminal=None,limits=['This PASS binds only the exact READY candidate source and administrative config/recorder; Root may copy those exact bytes for formal source admission, but no actual PREP/RUN/API/constructor/source or dynamic resource admission occurred.','The unchanged formal-path gate rejects the TMP factory. A formal installation and all genuine new-family PREP/build/terminal witnesses are still required.','The reviewed helper last-use deletion has no actual memory/RSS benefit credit; original parser and all original resource limits stay unchanged.','Old V8 failed RUN retains returncode 1, absent seal and four None tails; no historical scientific outcome is promoted.'])
write('independent_review.json',report)
print(json.dumps(dict(status=report['status'],scope=report['scope'],defs=len(pdf),factory_SHA=PINS[str(FC)]['sha256'],recorder_SHA=PINS[str(RC)]['sha256'],readonly_history_names=len(readonly_names),report_sha256=hashlib.sha256((OUT/'independent_review.json').read_bytes()).hexdigest(),no_business=True)))
