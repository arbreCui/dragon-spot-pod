"""Pure source composition. AST parse/inverse only; no business imports."""
import ast,hashlib,json
from pathlib import Path
D=Path('/private/tmp/axmat_v13_full_sender_window_component_source_draft_20261009')
P=Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_rank1_factor_cache_cross_group_identity_key_delta_production.py')
O=D/'prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py'
original=P.read_text();assert hashlib.sha256(original.encode()).hexdigest()=='f136baab5047a8727cfd2c0abb5399acf617c25c4f4e7692242419e6f9daef4e'
text=original;regions=[]
def region(name,before,after,count=1):
 global text
 assert text.count(before)==count,(name,text.count(before),count)
 text=text.replace(before,after,count)
 regions.append({'name':name,'before':before,'after':after,'count':count})
def function(name,replacements):
 tr=ast.parse(text);nodes=[n for n in tr.body if isinstance(n,ast.FunctionDef)and n.name==name];assert len(nodes)==1
 before=ast.get_source_segment(text,nodes[0]);after=before
 for old,new in replacements:
  assert after.count(old)==1,(name,old,after.count(old))
  after=after.replace(old,new,1)
 region('function_'+name,before,after)

region('topdoc',ast.get_docstring(ast.parse(text)),
 'Source-only complete V13 sender contiguous FUN window component.\n\n'
 'The complete original68 build/cache/codec stages must reexecute, followed by\n'
 'four new sender builds and14 real wrapper dispatch controls, total86 stages.\n'
 'The observer SPOF64 substitutes only in the unit executable; production links\n'
 'the actual full sender and unchanged real SPOF64. Original mathematical inputs,\n'
 'FP order, cache models, thresholds, budgets and genuine OwnRSS remain mandatory.\n'
 'This draft is UNREADY: unknown source/contract/auditor pins block all execution.\n'
 'No component result grants native RSS, convergence, independent accuracy or ABA.')
for key,old,new in (
 ('SOURCE','axial-material-qualified-AB-rank1-factor-cache-cross-group-identity-key-delta-build-admission-v11-20261009','axial-material-qualified-AB-sender-contiguous-flux-window-build-admission-v13-20261009'),
 ('OUT','axial-material-rank1-factor-cache-cross-group-identity-key-delta-build-v11-20261009','axial-material-sender-contiguous-flux-window-build-v13-20261009'),
 ('TERMINAL','axial-material-qualified-AB-rank1-factor-cache-cross-group-identity-key-delta-build-terminal-v11-20261009','axial-material-qualified-AB-sender-contiguous-flux-window-build-terminal-v13-20261009')):
 region('root_'+key,f'{key} = ART / "{old}"',f'{key} = ART / "{new}"')
region('family','FAMILY = "RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_V11"','FAMILY = "SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_V13"')
region('status','SOURCE_STATUS = "READY_SOURCE_ONLY_FOR_ROOT_REVIEWED_COMPONENT_EXECUTION"','SOURCE_STATUS = "UNREADY_SOURCE_ONLY_REQUIRES_FROZEN_SENDER_CONTROL_AND_AUDITOR"')
for old,new in (
 ('AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1','AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_ACTUAL_EXTERNAL_TERMINAL_RETURN_V13'),
 ('AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_DECLARATION_V1','AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_DECLARATION_V13'),
 ('AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_SEAL_V1','AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_SEAL_V13'),
 ('AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1','AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_PRODUCTION_RUNTIME_INPUT_ADMISSION_V13'),
 ('AXMAT_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_SOURCE_ADMISSION_V1','AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_SOURCE_ADMISSION_V13'),
 ('PASS_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_CONTROLS_ONLY','PASS_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_CONTROLS_ONLY'),
 ('COMPLETE_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_CONTROLS_ONLY','COMPLETE_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_CONTROLS_ONLY'),
 ('FAILED_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_NO_RETRY','FAILED_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_NO_RETRY')):
 region('active_schema_or_classification_'+old,old,new,text.count(old))
region('declaration_classification','DECLARED_RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_ONLY','DECLARED_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_ONLY_V13')
new_constants='''
# Immutable V11 cache/sender ancestry remains above; these are new private inputs.
SENDER_FACTORY_SOURCE_PARENT = ROOT / "validation/axial_material/prepare_qualified_AB_rank1_factor_cache_cross_group_identity_key_delta_production.py"
SENDER_FACTORY_SOURCE_PARENT_SHA = "f136baab5047a8727cfd2c0abb5399acf617c25c4f4e7692242419e6f9daef4e"
SENDER_PATCH_HELPER = ROOT / "validation/axial_material/sender_contiguous_flux_window_patch_v13.py"
SENDER_PATCH_HELPER_SHA = None
CANDIDATE_SENDER_SOURCE = ROOT / "validation/axial_material/sender_contiguous_flux_window_source_v13_20261009/FLU2DR64.f"
CANDIDATE_SENDER_SHA = None
SENDER_SOURCE_PROOF = CANDIDATE_SENDER_SOURCE.parent / "source_patch_proof.json"
SENDER_SOURCE_PROOF_SHA = None
SENDER_SOURCE_INPUT = CANDIDATE_SENDER_SOURCE.parent / "source_admission_INPUT.json"
SENDER_SOURCE_INPUT_SHA = None
SENDER_CONTROL_SOURCE = ROOT / "validation/axial_material/sender_contiguous_flux_window_observer_controls_v13.f90"
SENDER_CONTROL_SOURCE_SHA = None
SENDER_CONTROL_CONTRACT = CANDIDATE_SENDER_SOURCE.parent / "wrapper_control_contract.json"
SENDER_CONTROL_CONTRACT_SHA = None
SENDER_CONTROLS_AUDITOR = ROOT / "validation/axial_material/sender_contiguous_flux_window_controls_audit_v13.py"
SENDER_CONTROLS_AUDITOR_SHA = None
SENDER_CONTROL_LAYOUT = None  # Root must bind the complete frozen raw contract.
SENDER_MODES = ('all','suffix','interior','scalar_first','scalar_last','scalar_one',
    'sparse','empty_ileak0','empty_ileak3','transition',
    'unsupported_reference_active','unsupported_candidate_active',
    'unsupported_reference_empty','unsupported_candidate_empty')
SENDER_CASES = tuple(dict(name=name,args=[name],expected_returncode=0 if i<10 else 1,
    expected_message=None if i<10 else 'FLUSP64: UNSUPPORTED LEAKAGE MODEL.')
    for i,name in enumerate(SENDER_MODES))
ORIGINAL_STAGE_COUNT = 68
COMPLETE_STAGE_COUNT = 86
'''
region('new_sender_input_bindings','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA = None\n','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA = None\n'+new_constants)
function('require_ready',[(
 '        raise ValueError("independently frozen helper/control source pins are mandatory")',
 '        raise ValueError("independently frozen helper/control source pins are mandatory")\n'
 '    for value in (SENDER_PATCH_HELPER_SHA,CANDIDATE_SENDER_SHA,SENDER_SOURCE_PROOF_SHA,SENDER_SOURCE_INPUT_SHA,\n'
 '                  SENDER_CONTROL_SOURCE_SHA,SENDER_CONTROL_CONTRACT_SHA,SENDER_CONTROLS_AUDITOR_SHA):\n'
 '        if not re.fullmatch(r"[0-9a-f]{64}",value or "") or value=="0"*64:\n'
 '            raise ValueError("new sender source, complete contract and independent auditor pins are mandatory")\n'
 '    if type(SENDER_CONTROL_LAYOUT) is not dict:\n'
 '        raise ValueError("the complete frozen sender raw layout must be bound; no inferred defaults")')])
function('source_inputs',[(
 '    for path,wanted in expected.items():',
 '    expected.update(sender_source_admission()["source_inputs"])\n'
 '    expected.update({SENDER_FACTORY_SOURCE_PARENT:SENDER_FACTORY_SOURCE_PARENT_SHA,\n'
 '                     SENDER_CONTROL_SOURCE:SENDER_CONTROL_SOURCE_SHA,SENDER_CONTROL_CONTRACT:SENDER_CONTROL_CONTRACT_SHA,\n'
 '                     SENDER_CONTROLS_AUDITOR:SENDER_CONTROLS_AUDITOR_SHA})\n'
 '    for path,wanted in expected.items():')])
function('stage_commands',[(
 "        [d['build_python_executable'],str(Path(__file__).resolve()),'audit-build','--sha256',expected]]",
 "        *[[str(OUT/'runtime/flusp64_window_observer_controls'),*case['args']] for case in d['sender_control_contract']['cases']],\n"
 "        [d['build_python_executable'],str(Path(__file__).resolve()),'audit-build','--sha256',expected]]")])
function('stage_labels',[(
 "]+['audit/audit']",
 "]+['sender_controls/'+case['name']+'/execute' for case in d['sender_control_contract']['cases']]+['audit/audit']")])
function('prepare_build',[
 ("    forecast=archive_forecast(c,changed); shape=production_cache_shape_forecast(parent,c)",
  "    sender=sender_source_admission(); sender_contract=sender_control_contract()\n"
  "    forecast=complete_archive_forecast(c,changed,sender,sender_contract); shape=production_cache_shape_forecast(parent,c)"),
 ("    restore=list(link); restore[restore.index(str(OUT/'build/SPOT1P64.o'))]=str(KERNEL_OBJECT); restore[-1]=str(PARENT/'runtime/Dragon')",
  "    if link.count(str(SENDER_OBJECT))!=1:raise ValueError('exact old sender link token required')\n"
  "    link[link.index(str(SENDER_OBJECT))]=str(OUT/'build/FLU2DR64.o')\n"
  "    restore=list(link); restore[restore.index(str(OUT/'build/SPOT1P64.o'))]=str(KERNEL_OBJECT)\n"
  "    restore[restore.index(str(OUT/'build/FLU2DR64.o'))]=str(SENDER_OBJECT); restore[-1]=str(PARENT/'runtime/Dragon')"),
 ("    files=dict(old['files']); files.update(originals)",
  "    commands.insert(1,[*common,'-c',str(SOURCE/'FLU2DR64.f'),'-o',str(OUT/'build/FLU2DR64.o')])\n"
  "    commands.extend([\n"
  "      [*common,'-c',str(SOURCE/'FLUSP64.original_reference_unit.f'),'-o',str(OUT/'build/FLUSP64.original_reference_unit.o')],\n"
  "      [*common,'-c',str(SOURCE/'sender_window_controls.f90'),'-o',str(OUT/'build/sender_window_controls.o')],\n"
  "      [compiler,'-O2','-march=native','-ffp-contract=off','-g',str(OUT/'build/sender_window_controls.o'),\n"
  "       str(OUT/'build/FLU2DR64.o'),str(OUT/'build/FLUSP64.original_reference_unit.o'),str(OUT/'build/SPOT1P64.o'),\n"
  "       str(WHITE_OBJECT),str(ROOT/'lib/Darwin_arm64/libDragon.a'),str(ROOT/'Trivac/lib/Darwin_arm64/libTrivac.a'),\n"
  "       str(ROOT/'Utilib/lib/Darwin_arm64/libUtilib.a'),str(ROOT/'Ganlib/lib/Darwin_arm64/libGanlib.a'),\n"
  "       '-o',str(OUT/'runtime/flusp64_window_observer_controls')]])\n"
  "    files=dict(old['files']); files.update(originals)"),
 ("    for name in ('build','runtime','controls','audit',FAMILY):(OUT/name).mkdir()",
  "    for name in ('build','runtime','controls','sender_controls','audit',FAMILY):(OUT/name).mkdir()"),
 ("    if len(commands)!=8 or len(commands)+len(names)+1!=68:",
  "    if len(commands)!=12 or len(names)!=59 or len(commands)+len(names)+len(SENDER_CASES)+1!=86:"),
 ("    for name in names:(OUT/'controls'/name).mkdir()",
  "    for name in names:(OUT/'controls'/name).mkdir()\n"
  "    for case in SENDER_CASES:(OUT/'sender_controls'/case['name']).mkdir()\n"
  "    (SOURCE/'FLU2DR64.f').write_text(sender['sender_text'])\n"
  "    (SOURCE/'FLUSP64.original_reference_unit.f').write_text(sender['reference_wrapper_text'])\n"
  "    shutil.copy2(require(SENDER_CONTROL_SOURCE,SENDER_CONTROL_SOURCE_SHA),SOURCE/'sender_window_controls.f90')\n"
  "    shutil.copy2(require(SENDER_PATCH_HELPER,SENDER_PATCH_HELPER_SHA),SOURCE/'sender_patch_helper.py')\n"
  "    shutil.copy2(require(SENDER_SOURCE_PROOF,SENDER_SOURCE_PROOF_SHA),SOURCE/'sender_source_patch_proof.json')\n"
  "    shutil.copy2(require(SENDER_SOURCE_INPUT,SENDER_SOURCE_INPUT_SHA),SOURCE/'sender_source_only_INPUT.json')\n"
  "    shutil.copy2(require(SENDER_CONTROL_CONTRACT,SENDER_CONTROL_CONTRACT_SHA),SOURCE/'sender_control_contract.json')\n"
  "    shutil.copy2(require(SENDER_CONTROLS_AUDITOR,SENDER_CONTROLS_AUDITOR_SHA),SOURCE/'sender_controls_auditor.py')"),
 ("control_source_proof=changed['control_source_proof'],sole_new_production_objects=['SPOT1P64.o'],\n        unchanged_sender_object=pin(SENDER_OBJECT),",
  "control_source_proof=changed['control_source_proof'],sole_new_production_objects=['SPOT1P64.o','FLU2DR64.o'],\n"
  "        sender_window_source_admission=sender, sender_wrapper_control_contract=sender_contract,\n"
  "        full_component_factory_source_parent=pin(require(SENDER_FACTORY_SOURCE_PARENT,SENDER_FACTORY_SOURCE_PARENT_SHA)),\n"
  "        original_sender_ancestry=pin(SENDER_OBJECT),actual_new_sender_source=pin(SOURCE/'FLU2DR64.f'),"),
 ("files=files,build_commands=commands,production_link_command=commands[1],",
  "files=files,build_commands=commands,production_link_command=commands[2],\n"
  "        sender_source_admission=sender,sender_control_contract=sender_contract,original_stage_count=68,complete_stage_count=86,"),
])
function('declaration_admission',[
 ("d['production_link_command']!=d['build_commands'][1]","d['production_link_command']!=d['build_commands'][2]"),
 ("archive_forecast(c,changed)!=d['complete_archive_forecast']","complete_archive_forecast(c,changed,sender_source_admission(),sender_control_contract())!=d['complete_archive_forecast']"),
 ("    if d['control_contract']['original45_required'] is not True or len(stage_labels(d))!=68:",
  "    if d['sender_source_admission']!=sender_source_admission() or d['sender_control_contract']!=sender_control_contract():\n"
  "        raise ValueError('new complete sender source/receiver/wrapper contract changed')\n"
  "    if (SOURCE/'FLU2DR64.f').read_text()!=d['sender_source_admission']['sender_text'] or (SOURCE/'FLUSP64.original_reference_unit.f').read_text()!=d['sender_source_admission']['reference_wrapper_text']:\n"
  "        raise ValueError('private compiled sender/reference source bytes changed')\n"
  "    if (SOURCE/'sender_window_controls.f90').read_bytes()!=require(SENDER_CONTROL_SOURCE,SENDER_CONTROL_SOURCE_SHA).read_bytes():\n"
  "        raise ValueError('new actual wrapper driver bytes differ')\n"
  "    if d['original_stage_count']!=68 or d['complete_stage_count']!=86 or len(d['build_commands'])!=12:\n"
  "        raise ValueError('all original68 and18 new stages required')\n"
  "    if d['control_contract']['original45_required'] is not True or len(stage_labels(d))!=86:")])
function('expected_stage_exit',[("    return 0",
 "    if stage['label'].startswith('sender_controls/'):\n"
 "        cases={\"sender_controls/\"+c['name']+\"/execute\":c for c in SENDER_CASES}\n"
 "        if stage['label'] not in cases:raise ValueError('undeclared sender case stage')\n"
 "        return cases[stage['label']]['expected_returncode']\n"
 "    return 0")])
function('stage_outcome_valid',[("expected_stage_exit(stage)==23","expected_stage_exit(stage)!=0")])
function('check_watch',[("    if expected_stage_exit(stage)==23:return check_keycodec_negative_watch(stage)",
 "    if expected_stage_exit(stage)==1:return check_sender_negative_watch(stage)\n"
 "    if expected_stage_exit(stage)==23:return check_keycodec_negative_watch(stage)")])

def replace_function(name, after):
 tr=ast.parse(text);nodes=[n for n in tr.body if isinstance(n,ast.FunctionDef) and n.name==name];assert len(nodes)==1
 region('complete_function_'+name,ast.get_source_segment(text,nodes[0]),after)

source_gate=Path('/private/tmp/axmat_v13_sender_source_gate_draft_20261009/sender_source_admission.function.py').read_text()
assert hashlib.sha256(source_gate.encode()).hexdigest()=='c2a16a0c68e0caf413e4436379652ff65d41306b6442df6b78fd4b681e15cc9d'
source_gate=ast.get_source_segment(source_gate,next(n for n in ast.parse(source_gate).body if isinstance(n,ast.FunctionDef)))
region('new_sender_source_gate','def source_inputs():',source_gate+'\n\n\ndef source_inputs():')
contract_fragments=Path('/private/tmp/axmat_v13_sender_contract_forecast_watch_draft_20261009/sender_contract_forecast_watch.functions.py').read_text()
assert hashlib.sha256(contract_fragments.encode()).hexdigest()=='13565ffb14ccb4fc8886011ac6493373243fb0d0d7b6a44f3d3b0e9f8a987300'
fragment_tree=ast.parse(contract_fragments)
contract_fragments='\n\n\n'.join(ast.get_source_segment(contract_fragments,n) for n in fragment_tree.body if isinstance(n,ast.FunctionDef))
region('new_sender_contract_forecast_watch','def source_inputs():',contract_fragments+'\n\n\ndef source_inputs():')

sender_audit='''def sender_namespace_identities():
    root=OUT/'sender_controls'
    if root.is_symlink() or not root.is_dir():raise ValueError('owned complete sender tree required')
    identities={}
    for path in [root,*sorted(root.rglob('*'))]:
        if path.is_symlink():raise ValueError('no sender evidence symbolic link is eligible')
        info=path.stat()
        if not (stat.S_ISDIR(info.st_mode) or (stat.S_ISREG(info.st_mode) and info.st_nlink==1)):
            raise ValueError('sender evidence requires unique ordinary files and directories')
        identities[str(path.relative_to(root))]=[info.st_dev,info.st_ino,info.st_mode,info.st_nlink,
            info.st_size,info.st_mtime_ns,info.st_ctime_ns]
    return identities


def sender_raw_receipt(d):
    before=sender_namespace_identities()
    files=raw_inventory(OUT/'sender_controls')
    if sender_namespace_identities()!=before:raise ValueError('whole sender tree changed during raw archival hash')
    return dict(files=files,before_numeric_gates=True,declared_sender_control_contract=d['sender_control_contract'],
        raw_identity_before_after_equal=True,raw_identity_snapshot=before)


def sender_controls_audit(d):
    """Independent whole raw observer audit; this grants no real SPOT math credit."""
    contract=sender_control_contract()
    if d['sender_control_contract']!=contract:raise ValueError('entire declared sender contract changed')
    receipt=read(require(OUT/'raw_sender_controls_receipt.json'))
    before=sender_namespace_identities()
    if (receipt['files']!=raw_inventory(OUT/'sender_controls') or receipt['before_numeric_gates'] is not True
            or receipt['declared_sender_control_contract']!=contract or receipt['raw_identity_before_after_equal'] is not True
            or receipt['raw_identity_snapshot']!=before or sender_namespace_identities()!=before):
        raise ValueError('whole returned sender raw/log/watch/manifest bytes must precede every acceptance')
    module=load(require(SENDER_CONTROLS_AUDITOR,SENDER_CONTROLS_AUDITOR_SHA),'sender_contiguous_flux_window_controls_audit_v13')
    result=module.audit_sender_controls(OUT/'sender_controls',contract)
    positive=[c for c in contract['cases'] if not c['negative']]
    steps=[s for c in positive for s in c['steps']]
    expected_counts=dict(positive_cases=10,expected_guard_rejection_cases=4,positive_steps=22,
        reference_wrapper_calls=24,candidate_wrapper_calls=24,wrapper_calls_total=48,observer_calls_total=34,
        direct_candidate_steps=sum(s['expected_route']==1 for s in steps),
        sparse_fallback_steps=sum(s['expected_route']==2 for s in steps),empty_steps=sum(s['expected_route']==0 for s in steps),
        raw_file_count=70,raw_bytes=288241824,
        independently_verified_active_output_scalars=sum(2*c['nun']*s['active_groups'] for c in positive for s in c['steps']))
    if (result['schema']!='AXMAT_FLUSP64_WINDOW_COMPLETE_RAW_OBSERVER_CONTROLS_AUDIT_V13'
            or result['status']!='PASS' or result['counts']!=expected_counts
            or len(result['cases'])!=14 or [c['name'] for c in result['cases']]!=list(SENDER_MODES)
            or any(result[k] is not True for k in ('complete_raw_scope_verified','all_successful_caller_bits_equal_to_original',
                'all_sources_independently_reconstructed','actual_contiguous_alias_and_sparse_nonalias_verified',
                'all_other_caller_planes_and_inactive_output_unchanged','repeated_calls_and_active_set_transition_verified',
                'raw_identity_before_after_equal')) or result['raw_identity_snapshot']!=before
            or any(result[k] is not False for k in ('solver_math_credit','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'))
            or result['real_SPOT_receiver_calls_in_this_observer_executable']!=0):
        raise ValueError('all fourteen whole raw routing/alias/bit controls must independently pass without solver credit')
    wanted={c['name']+'/'+r['name']:r for c in contract['cases'] for r in c['raw_files']}
    if set(result['all_raw_files'])!=set(wanted):raise ValueError('all seventy raw sender files required')
    for name,row in result['all_raw_files'].items():
        path=OUT/'sender_controls'/name
        if row!=dict(path=str(path),bytes=path.stat().st_size,sha256=digest(require(path))) or row['bytes']!=wanted[name]['size_bytes']:
            raise ValueError('whole sender raw bytes/pins differ from independent actual audit')
    for actual,case in zip(result['cases'],contract['cases']):
        if (actual['actual_returncode']!=case['expected_returncode']
                or actual['status']!=('EXPECTED_REJECTION' if case['negative'] else 'PASS')
                or set(actual['raw_files'])!={r['name'] for r in case['raw_files']}):
            raise ValueError('every exact positive and real expected negative case must close')
        for basename,row in actual['raw_files'].items():
            if row!=result['all_raw_files'][case['name']+'/'+basename]:raise ValueError('case raw ownership differs')
        for field,basename in (('actual_log','execute.log'),('actual_watchdog','execute.watchdog.json'),('actual_manifest','wrapper_manifest.jsonl')):
            path=OUT/'sender_controls'/case['name']/basename
            if actual[field]!=dict(path=str(path),bytes=path.stat().st_size,sha256=digest(require(path))):
                raise ValueError('case log/watch/manifest identity differs')
    if sender_namespace_identities()!=before:raise ValueError('whole sender tree changed during factory independent acceptance')
    return result


def component_controls_audit(d):
    # The original 68-stage audit body and all numerical/FP/cache fixtures remain
    # byte-for-byte unchanged. Sender stub calls belong only to the new scope.
    original=control_audit(d)
    if original['counts']['total_declared_stages']!=68:raise ValueError('original complete68 count changed')
    sender=sender_controls_audit(d)
    result=copy.deepcopy(original)
    result['original_68_control_counts']=copy.deepcopy(original['counts'])
    result['counts']['total_declared_stages']=86
    result['sender_window_controls']=sender
    result['sender_window_control_counts']=copy.deepcopy(sender['counts'])
    result['sender_window_controls_passed']=True
    result['sender_window_source_admission']=d['sender_source_admission']
    return result
'''
region('new_sender_raw_component_audit','def binary_audit(d):',sender_audit+'\n\ndef binary_audit(d):')

function('binary_audit',[
 ("'keycodec_executable':OUT/'runtime/keycodec_controls'}",
  "'keycodec_executable':OUT/'runtime/keycodec_controls',\n"
  "        'new_sender':OUT/'build/FLU2DR64.o','sender_reference_wrapper':OUT/'build/FLUSP64.original_reference_unit.o',\n"
  "        'sender_observer_driver':OUT/'build/sender_window_controls.o',\n"
  "        'sender_window_executable':OUT/'runtime/flusp64_window_observer_controls'}"),
 ("    for symbol in ('_spot1p64_','_flu2dr64_','_flu_'):",
  "    for name,symbols_required in (('new_sender',('_flu2dr64_','_flusp64_')),\n"
  "            ('sender_reference_wrapper',('_flusp64_reference_',)),('sender_observer_driver',('_spof64_',)),\n"
  "            ('sender_window_executable',('_flusp64_','_flusp64_reference_','_spof64_','_spot1p64_'))):\n"
  "        if any(symbols(name).count(sym)!=1 for sym in symbols_required):\n"
  "            raise ValueError('fresh actual sender/wrapper-reference/observer symbols must be uniquely compiled/linked')\n"
  "    for name,file in (('new_sender','FLU2DR64.f'),('sender_reference_wrapper','FLUSP64.original_reference_unit.f'),\n"
  "            ('sender_observer_driver','sender_window_controls.f90')):\n"
  "        if str(SOURCE/file) not in Path(raw[name+'_debug']['path']).read_text():\n"
  "            raise ValueError('every new sender unit must name its exact declared private source')\n"
  "    if digest(paths['new_sender'])==SENDER_OBJECT_SHA:raise ValueError('old sender object may never stand for the new full source')\n"
  "    for symbol in ('_spot1p64_','_flu2dr64_','_flusp64_','_spof64_','_flu_'):") ,
 ("('_spot1p64_original_','_spot1p64_dense_')):\n        raise ValueError('production must exclude every unit reference routine')",
  "('_spot1p64_original_','_spot1p64_dense_','_flusp64_reference_')):\n        raise ValueError('production must exclude every unit reference routine')"),
 ("    link=list(d['build_commands'][1]);old=read(PARENT/'declaration.json')['build_commands'][2]",
  "    link=list(d['build_commands'][2]);old=read(PARENT/'declaration.json')['build_commands'][2]"),
 ("    if link.count(str(OUT/'build/SPOT1P64.o'))!=1 or str(KERNEL_OBJECT) in link or str(OUT/'build/SPOT1P64.dense_reference.o') in link:\n        raise ValueError('sole new production kernel precedence/reference exclusion differs')",
  "    if (link.count(str(OUT/'build/SPOT1P64.o'))!=1 or link.count(str(OUT/'build/FLU2DR64.o'))!=1\n"
  "            or str(KERNEL_OBJECT) in link or str(SENDER_OBJECT) in link\n"
  "            or any(str(OUT/name) in link for name in ('build/SPOT1P64.dense_reference.o','build/SPOT1P64.original_reference.o',\n"
  "                'build/FLUSP64.original_reference_unit.o','build/sender_window_controls.o'))):\n"
  "        raise ValueError('only the new kernel and actual new full sender production overrides are allowed')"),
 ("    if link.index(str(OUT/'build/SPOT1P64.o'))>=link.index(str(ROOT/'lib/Darwin_arm64/libDragon.a')):raise ValueError('override must precede original archive')",
  "    if any(link.index(str(OUT/'build'/name))>=link.index(str(ROOT/'lib/Darwin_arm64/libDragon.a')) for name in ('SPOT1P64.o','FLU2DR64.o')):\n"
  "        raise ValueError('both actual overrides must precede original archive')"),
 ("    link[link.index(str(OUT/'build/SPOT1P64.o'))]=str(KERNEL_OBJECT);link[-1]=str(PARENT/'runtime/Dragon')",
  "    unitlink=d['build_commands'][-1]\n"
  "    if (unitlink.count(str(OUT/'build/FLU2DR64.o'))!=1 or unitlink.count(str(OUT/'build/FLUSP64.original_reference_unit.o'))!=1\n"
  "            or unitlink.count(str(OUT/'build/sender_window_controls.o'))!=1\n"
  "            or any(token in unitlink for token in (str(SENDER_OBJECT),str(SOURCE/'SPOF64.o'),str(OUT/'build/SPOF64.o')))\n"
  "            or any(sym in symbols('sender_window_executable') for sym in ('_spot1p64_original_','_spot1p64_dense_'))):\n"
  "        raise ValueError('observer stub/reference wrapper are unit-only; actual new fullsender required')\n"
  "    link[link.index(str(OUT/'build/SPOT1P64.o'))]=str(KERNEL_OBJECT)\n"
  "    link[link.index(str(OUT/'build/FLU2DR64.o'))]=str(SENDER_OBJECT);link[-1]=str(PARENT/'runtime/Dragon')"),
 ("        actual_objects={key:pin(path) for key,path in paths.items()},unchanged_sender_object=pin(SENDER_OBJECT),",
  "        actual_objects={key:pin(path) for key,path in paths.items()},original_sender_ancestry=pin(SENDER_OBJECT),\n"
  "        actual_full_sender_source=pin(SOURCE/'FLU2DR64.f'),actual_sender_source_proof=pin(SOURCE/'sender_source_patch_proof.json'),\n"
  "        actual_new_sender_compiled_and_linked=True,actual_sender_wrapper_observer_separate_unit_only=True,"),
])

function('audit_build',[
 ("    controls = control_audit(d)","    controls = component_controls_audit(d)"),
 ("        control_counts=controls[\"counts\"], previous_stage_watchdogs=watches,",
  "        control_counts=controls[\"counts\"], original_68_control_counts=controls['original_68_control_counts'],\n"
  "        sender_window_control_counts=controls['sender_window_control_counts'],sender_window_controls_passed=True,\n"
  "        sender_window_source_admission=d['sender_source_admission'],actual_new_sender_compiled_and_linked=True,\n"
  "        sender_wrapper_observer_real_SPOT_credit=0,previous_stage_watchdogs=watches,"),
])

function('run_build',[
 ("\"build/keycodec_controls.o\",\"runtime/keycodec_controls\")",
  "\"build/keycodec_controls.o\",\"runtime/keycodec_controls\",\"build/FLU2DR64.o\",\n"
  "            \"build/FLUSP64.original_reference_unit.o\",\"build/sender_window_controls.o\",\"runtime/flusp64_window_observer_controls\")"),
 ("sole_new_production_overrides=[\"SPOT1P64.o\"], inherited_sender_override=pin(SENDER_OBJECT),",
  "sole_new_production_overrides=[\"SPOT1P64.o\",\"FLU2DR64.o\"], original_sender_ancestry=pin(SENDER_OBJECT),\n"
  "            actual_sender_source=pin(SOURCE/'FLU2DR64.f'),actual_sender_source_proof=pin(SOURCE/'sender_source_patch_proof.json'),"),
 ("                    raise ValueError('keycodec negative unexpectedly returned success; no retry')",
  "                    raise ValueError('keycodec negative unexpectedly returned success; no retry')\n"
  "            for case in d['sender_control_contract']['cases']:\n"
  "                environment(d)\n"
  "                command=[str(OUT/'runtime/flusp64_window_observer_controls'),*case['args']]\n"
  "                if case['expected_returncode']==0:\n"
  "                    runner.execute(OUT/'sender_controls'/case['name'],'execute',command,STAGE_WALL)\n"
  "                else:\n"
  "                    try:runner.execute(OUT/'sender_controls'/case['name'],'execute',command,STAGE_WALL)\n"
  "                    except RuntimeError:\n"
  "                        stage=read(OUT/FAMILY/'stages.json')['stages'][-1]\n"
  "                        if stage['label']!='sender_controls/'+case['name']+'/execute':raise\n"
  "                        check_sender_negative_watch(stage)\n"
  "                    else:raise ValueError('sender unsupported leakage unexpectedly returned success; no retry')"),
 ("                before_numeric_gates=True, declared_control_contract=d[\"control_contract\"]))",
  "                before_numeric_gates=True, declared_control_contract=d[\"control_contract\"]))\n"
  "            write_new(OUT/'raw_sender_controls_receipt.json',sender_raw_receipt(d))"),
 ("        audit = read(OUT / \"audit/result.json\")",
  "        audit = read(OUT / \"audit/result.json\")\n"
  "        if (audit['sender_window_controls_passed'] is not True or audit['actual_new_sender_compiled_and_linked'] is not True\n"
  "                or audit['original_68_control_counts']['total_declared_stages']!=68\n"
  "                or audit['control_counts']['total_declared_stages']!=86 or audit['sender_wrapper_observer_real_SPOT_credit']!=0):\n"
  "            raise ValueError('complete original68 and14 new actual fullsender wrapper controls required')"),
 ("control_counts=audit[\"control_counts\"], runtime_sha256=digest(OUT / \"runtime/Dragon\"),",
  "control_counts=audit[\"control_counts\"],original_68_control_counts=audit['original_68_control_counts'],\n"
  "            sender_window_control_counts=audit['sender_window_control_counts'],sender_window_controls_passed=True,\n"
  "            actual_new_sender_compiled_and_linked=True,sender_wrapper_observer_real_SPOT_credit=0,\n"
  "            runtime_sha256=digest(OUT / \"runtime/Dragon\"),"),
])

function('production_admission',[
 ("    controls = control_audit(d)","    controls = component_controls_audit(d)"),
 ("controls['counts']['total_declared_stages']!=68","controls['counts']['total_declared_stages']!=86 or controls['original_68_control_counts']['total_declared_stages']!=68"),
 ("    binary = read(require(OUT / \"audit/binary_identity.json\"))",
  "    if (result['sender_window_controls_passed'] is not True or audit['sender_window_controls_passed'] is not True\n"
  "            or result['actual_new_sender_compiled_and_linked'] is not True or audit['actual_new_sender_compiled_and_linked'] is not True\n"
  "            or result['original_68_control_counts']!=controls['original_68_control_counts']\n"
  "            or audit['original_68_control_counts']!=controls['original_68_control_counts']\n"
  "            or result['sender_window_control_counts']!=controls['sender_window_control_counts']\n"
  "            or audit['sender_window_control_counts']!=controls['sender_window_control_counts']\n"
  "            or audit['sender_window_source_admission']!=sender_source_admission()\n"
  "            or result['sender_wrapper_observer_real_SPOT_credit']!=0 or audit['sender_wrapper_observer_real_SPOT_credit']!=0):\n"
  "        raise ValueError('all original68 and new complete sender raw scopes must be freshly admitted independently')\n"
  "    binary = read(require(OUT / \"audit/binary_identity.json\"))"),
 ("            or binary[\"executable_definitions_verified\"] is not True):",
  "            or binary[\"executable_definitions_verified\"] is not True\n"
  "            or binary['actual_new_sender_compiled_and_linked'] is not True\n"
  "            or binary['actual_sender_wrapper_observer_separate_unit_only'] is not True\n"
  "            or binary['actual_full_sender_source']!=pin(SOURCE/'FLU2DR64.f')\n"
  "            or binary['actual_sender_source_proof']!=pin(SOURCE/'sender_source_patch_proof.json')\n"
  "            or binary['original_sender_ancestry']!=pin(SENDER_OBJECT)):") ,
 ("identity[\"sole_new_production_overrides\"] != [\"SPOT1P64.o\"]",
  "identity[\"sole_new_production_overrides\"] != [\"SPOT1P64.o\",\"FLU2DR64.o\"]"),
 ("or identity[\"inherited_sender_override\"] != pin(SENDER_OBJECT)",
  "or identity['original_sender_ancestry'] != pin(SENDER_OBJECT)\n"
  "            or identity['actual_sender_source']!=pin(SOURCE/'FLU2DR64.f')\n"
  "            or identity['actual_sender_source_proof']!=pin(SOURCE/'sender_source_patch_proof.json')\n"
  "            or binary['actual_objects']['new_sender']!=pin(OUT/'build/FLU2DR64.o')\n"
  "            or identity['files']['build/FLU2DR64.o']!=digest(OUT/'build/FLU2DR64.o')"),
 ("admission=\"RANK1_FACTOR_CACHE_FACTOR_DIAGONAL_TRIM_RUNTIME_INPUT_ONLY\"",
  "admission=\"SENDER_CONTIGUOUS_FLUX_WINDOW_RUNTIME_INPUT_ONLY_V13\""),
 ("        compiled_kernel_source=pin(SOURCE / \"SPOT1P64.f90\"),",
  "        compiled_kernel_source=pin(SOURCE / \"SPOT1P64.f90\"),\n"
  "        compiled_sender_source=pin(SOURCE/'FLU2DR64.f'),compiled_sender=pin(OUT/'build/FLU2DR64.o'),\n"
  "        sender_source_proof=pin(SOURCE/'sender_source_patch_proof.json'),sender_source_only_INPUT=pin(SOURCE/'sender_source_only_INPUT.json'),\n"
  "        sender_window_source_admission=d['sender_source_admission'],sender_window_controls_passed=True,\n"
  "        sender_wrapper_raw_controls=controls['sender_window_controls'],sender_window_control_counts=controls['sender_window_control_counts'],\n"
  "        original_68_control_counts=controls['original_68_control_counts'],\n"
  "        sender_wrapper_observer_real_SPOT_credit=0,actual_new_sender_compiled_and_linked=True,"),
 ("        corrected_sender_retained=True, white_closure_unchanged=True, collision_self_operator_unchanged=True,",
  "        corrected_sender_transport_math_retained=True,sender_output_storage_window_changed=True,\n"
  "        original_sender_ancestry=pin(SENDER_OBJECT),white_closure_unchanged=True, collision_self_operator_unchanged=True,"),
])

def save_draft():
 ast.parse(text)
 inverse=text
 for e in reversed(regions):
  assert inverse.count(e['after'])==e['count'],e['name']
  inverse=inverse.replace(e['after'],e['before'],e['count'])
 assert inverse==original
 O.write_text(text)
 (D/'composition_regions.json').write_text(json.dumps(regions,indent=2)+'\n')
 print(json.dumps({'status':'COMPLETE_SOURCE_COMPOSITION_UNREADY_NOT_EXECUTABLE','candidate_sha256':hashlib.sha256(text.encode()).hexdigest(),'regions':len(regions),'whole_inverse_byteexact':True,'business_executed':False}))

if __name__=='__main__':save_draft()
