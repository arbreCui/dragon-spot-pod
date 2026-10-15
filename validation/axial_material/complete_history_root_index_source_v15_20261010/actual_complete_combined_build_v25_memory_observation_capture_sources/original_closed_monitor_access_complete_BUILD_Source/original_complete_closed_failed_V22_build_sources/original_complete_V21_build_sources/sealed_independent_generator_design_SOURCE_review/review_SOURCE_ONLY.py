"""Independent finite SOURCE AST/byte review; never run the reviewed generator or host."""
import ast
import hashlib
import json
import os
import stat
from pathlib import Path

PACKAGE=Path('/private/tmp/axmat_v21_complete_build_generator_SOURCE_ONLY_design_20261010_zmqkz714')
OUT=Path('/private/tmp/axmat_v21_complete_build_generator_independent_SOURCE_review_20261010_y84cv')
MANIFEST_SHA='e5bb1dcc8bcefd92b7ee66c8e5e39abb6d82e712eb928bd71cc6fb1d418445a1'


def ident(st):
    return [st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns]


def read(path):
    first=path.lstat()
    if not stat.S_ISREG(first.st_mode) or first.st_nlink!=1 or path.resolve()!=path:
        raise ValueError('ordinary exact SOURCE only')
    with path.open('rb') as stream:
        if ident(os.fstat(stream.fileno()))!=ident(first):raise ValueError('source pre-read identity changed')
        data=stream.read()
        if ident(os.fstat(stream.fileno()))!=ident(first):raise ValueError('source full read identity changed')
    if ident(path.lstat())!=ident(first) or len(data)!=first.st_size:
        raise ValueError('source full EOF identity changed')
    return data,dict(path=str(path),sha256=hashlib.sha256(data).hexdigest(),identity=ident(first))


def inverse(text,changes):
    for change in reversed(changes):
        if text.count(change['after'])!=change['count']:
            raise ValueError('finite source inverse count mismatch')
        text=text.replace(change['after'],change['before'])
    return text


def functions(source):
    lines=source.splitlines(keepends=True)
    return {node.name:''.join(lines[node.lineno-1:node.end_lineno])
            for node in ast.parse(source).body if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}


def assignments(tree):
    return {target.id:node.value for node in tree.body if isinstance(node,ast.Assign)
            for target in node.targets if isinstance(target,ast.Name)}


def main():
    checks=[]
    def check(name,value):
        if value is not True:raise ValueError('SOURCE check: '+name)
        checks.append(dict(name=name,value=True))
    manifest_bytes,manifest_pin=read(PACKAGE/'sealed_manifest.json')
    check('author whole manifest exact SHA',manifest_pin['sha256']==MANIFEST_SHA)
    manifest=json.loads(manifest_bytes)
    expected={Path(pin['path']).name:pin for pin in manifest['members']}
    check('complete author manifest unique member sequence',len(expected)==len(manifest['members'])==manifest['member_count']==12)
    inventory_before=sorted(str(path.relative_to(PACKAGE)) for path in PACKAGE.rglob('*'))
    check('complete namespace no unlisted members',set(inventory_before)==set(expected)|{'sealed_manifest.json'})
    data={};pins={}
    for name,pin in expected.items():
        bytes_,actual=read(PACKAGE/name)
        check('full SOURCE EOF SHA7ID original manifest '+name,actual==pin)
        data[name]=bytes_;pins[name]=actual
    pins['sealed_manifest.json']=manifest_pin
    source=data['generate_build_host.py'].decode()
    parent=data['frozen_parent_generate_build_host_v20.py'].decode()
    proof=json.loads(data['source_inverse_proof.json'])
    check('candidate full SOURCE SHA fixed d5d2',hashlib.sha256(source.encode()).hexdigest()=='d5d206232ad42927e235b0f947bd893b28eafcfcb593369b4dba7adb96a640e8')
    check('parent full SOURCE SHA fixed c8cf',hashlib.sha256(parent.encode()).hexdigest()=='c8cf1a7c0a3e60c4cfb2edfc88e496e9fedccb25330c11c5bbb7421d23c52f72')
    check('exact fifteen finite author hunks',len(proof['changes'])==proof['finite_generator_change_count']==15)
    restored=inverse(source,proof['changes'])
    check('complete fifteen hunk SOURCE byte inverse c8cf',restored.encode()==parent.encode())
    check('complete fifteen hunk SOURCE AST inverse c8cf',ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False))
    oldfn,newfn=functions(parent),functions(source)
    check('all actual six generator definitions and order preserved',list(oldfn)==list(newfn) and len(newfn)==6)
    changed=[]
    for name in oldfn:
        if oldfn[name]!=newfn[name]:changed.append(name)
        check('full definition restored bytes '+name,functions(restored)[name]==oldfn[name])
    check('only two necessary binding functions changed',changed==['original_source_checks','main'])
    check('four original source/reference/write functions byteexact',all(newfn[k]==oldfn[k] for k in ('pin','metadata_reference','output_reference','write_new')))
    for name in ['source_author.py','frozen_parent_combined_build_host_v20.py','frozen_cf2c_combined_build_host_v17.py','frozen_37d_normal_prepare_host.py','frozen_parent_generate_build_host_v20.py','generate_build_host.py']:
        tree=ast.parse(data[name].decode())
        compile(tree,'<independent SOURCE AST only '+name+'>','exec')
        check('entire SOURCE AST parsed without import or execution '+name,True)
    cf2=data['frozen_cf2c_combined_build_host_v17.py'].decode()
    normal=data['frozen_37d_normal_prepare_host.py'].decode()
    oldhost=data['frozen_parent_combined_build_host_v20.py'].decode()
    cf2proof=json.loads(data['frozen_cf2c_to_37d_source_inverse.json'])
    check('original cf2 to 37d full thirteen change proof',len(cf2proof['changes'])==cf2proof['finite_change_count']==13)
    check('original cf2 to 37d full byte inverse',inverse(cf2,cf2proof['changes']).encode()==normal.encode())
    check('original cf2 to 37d full AST inverse',ast.dump(ast.parse(inverse(cf2,cf2proof['changes'])),include_attributes=False)==ast.dump(ast.parse(normal),include_attributes=False))
    original_live_pins={}
    original_live_data={}
    for original in proof['checked_existing_SOURCE_inputs']:
        path=Path(original['path'])
        check('bounded explicit lineage SOURCE path no ART '+path.name,'/validation/artifacts/' not in str(path))
        bytes_,pin=read(path)
        check('explicit original SOURCE whole EOF SHA7ID '+str(path),pin==original)
        original_live_pins[str(path)]=pin;original_live_data[str(path)]=bytes_
    root=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
    hostproof_path=root/'actual_complete_combined_build_v20_sources/sealed_actual_bound_SOURCE_generation/Root_finite_build_host_source_inverse.json'
    hostproof=json.loads(original_live_data[str(hostproof_path)])
    check('old d5fa complete host proof seventeen hunks',len(hostproof['changes'])==hostproof['finite_change_count']==17)
    check('old d5fa whole host inverse to cf2',inverse(oldhost,hostproof['changes']).encode()==cf2.encode())
    check('old d5fa whole host AST inverse to cf2',ast.dump(ast.parse(inverse(oldhost,hostproof['changes'])),include_attributes=False)==ast.dump(ast.parse(cf2),include_attributes=False))
    c8proof=json.loads(data['frozen_v20_generator_source_inverse.json'])
    ancestor_path=root/'actual_complete_combined_build_v20_sources/sealed_actual_bound_SOURCE_generation/frozen_parent_generate_build_host_v19.py'
    check('old c8cf complete three change proof',len(c8proof['changes'])==c8proof['finite_change_count']==3)
    check('old c8cf complete source inverse to dc48',inverse(parent,c8proof['changes']).encode()==original_live_data[str(ancestor_path)])
    tree=ast.parse(source);globals_=assignments(tree)
    fixed=globals_['FIXED'];dynamic=globals_['DYNAMIC_SOURCE_TOKENS']
    check('full future host 15fixed and6dynamic finite SOURCE retargets',isinstance(fixed,ast.List) and len(fixed.elts)==15 and isinstance(dynamic,ast.List) and len(dynamic.elts)==6)
    fixed_literal_values={'TARGET_SHA':ast.literal_eval(globals_['TARGET_SHA']),'HELPER_SHA':ast.literal_eval(globals_['HELPER_SHA']),'HELPER_Q_SHA':ast.literal_eval(globals_['HELPER_Q_SHA'])}
    check('fixed actual READY runtime sha exact023abc',fixed_literal_values['TARGET_SHA']=='023abc88dd60e89cb49ebacb881f555850b7732149b14caf14503bd135a391e5')
    check('fixed actual dc01 qualified helper SHA exact',fixed_literal_values['HELPER_SHA']=='dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7')
    check('fixed actual joint Q29ac SHA exact',fixed_literal_values['HELPER_Q_SHA']=='29ac1abd0df3ff9d1d71a3239842e1c97cb2619cc4627292b0d25f6e16218bb2')
    for i,node in enumerate(fixed.elts+dynamic.elts):
        before=ast.literal_eval(node.elts[0]);count=ast.literal_eval(node.elts[2])
        check('full old host exact finite retarget anchor '+str(i),type(count) is int and cf2.count(before)==count)
        if i<15:
            after=node.elts[1]
            check('fixed retarget only ordinary SOURCE literal or exact SHA global '+str(i),isinstance(after,ast.Constant) and type(after.value) is str or isinstance(after,ast.Name) and after.id in fixed_literal_values)
    check('four helper/Q mappings added without altering original fixed list length',len(fixed.elts[-4:])==4)
    check('explicit UNREADY until real Root successful PREP',ast.literal_eval(globals_['DRAFT_STATUS'])=='UNREADY_SOURCE_TEMPLATE_AWAIT_REAL_ROOT_V21_CLOSED_SUCCESSFUL_PREP')
    futurekeys=ast.literal_eval(globals_['FUTURE_BUSINESS_KEYS'])
    check('all six original future business keys required',futurekeys==[
      'FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA',
      'FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA',
      'FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA'])
    anchors=[
      "if '/validation/artifacts/' in str(path):",
      "raise ValueError('generator reads SOURCE/Root closed metadata only, never ART')",
      "if len(sys.argv)!=10 or Path(sys.argv[1])!=SUMMARY",
      "re.fullmatch('[0-9a-f]{64}',value)",
      "s['schema']!='ROOT_V21_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1'",
      "s['status']!='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD'",
      "terminal['closed'] is not True or type(tr.get('exit_code')) is not int or tr['exit_code']!=0 or 'session_id' in tr",
      "terminal.get('session_repolled_after_close',False) is not False",
      "terminal_pin['sha256']!=sys.argv[3]",
      "namespace_pin['sha256']!=sys.argv[4]",
      "s['Root_actual_terminal']!=s['actual_root_terminal']",
      "namespace['schema']!='ROOT_V21_ACTUAL_COMPLETE_PREPARE_ALL_NAMESPACES_V1'",
      "namespace['no_build_or_native_credit'] is not True",
      "len(ns)!=len(namespace['namespaces']) or set(ns)!=expected_roots",
      "(1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0)",
      "s['original_caps_preserved'] is not True",
      "if any(type(x) is not int for x in ref['identity']):",
      "set(ref) != {'path','sha256','identity'}",
      "'actual_source_admission':output_reference(ns[SOURCE]['files']['source_admission.json'],SOURCE+'/source_admission.json')",
      "'actual_declaration':sys.argv[5]",
      "'actual_source_admission':sys.argv[6]",
      "'actual_prep_terminal':sys.argv[7]",
      "'actual_complete_input_graph':sys.argv[8]",
      "'actual_complete_creation_trace':sys.argv[9]",
      "if ns[folder]['files'][relative]!=ref:",
      "namespace['all_original_inputs_fresh_full_EOF_SHA7ID_unchanged']",
      "recorded_sources[str(TARGET)]!=sources[-1] or namespace['canonical_factory']!=sources[-1]",
      "for ref in sources+[summary_pin,terminal_pin,namespace_pin]:",
      "if again!=ref:",
      "if p.exists(): raise ValueError('source candidate output must be fresh')",
      "if any(vals[k] is not None for k in FUTURE_BUSINESS_KEYS):",
      "q['schema']!='AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_VERIFIER_HELPER_ACTUAL_JOINT_ADMISSION_V21'",
      "q['status']!='QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V21'",
      "if any(q[k] is not False for k in scope):",
      "len(helper_data)!=147870",
    ]
    for anchor in anchors:check('whole SOURCE metadata binding contract '+anchor,anchor in source)
    helper_scope=next(ast.literal_eval(node.value) for node in ast.walk(tree)
                      if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='scope' for t in node.targets))
    check('all eleven metadata-helper-only business/MRO flags false',helper_scope==('fresh_production_graph_created','fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','whole_build_qualified','whole_INPUT_admitted','physical_balance_qualified','supervisor_class_or_MRO_modified','profile_used'))
    cf2tree=ast.parse(cf2);hostvars=assignments(cf2tree)
    labels=ast.literal_eval(hostvars['EXPECTED_LABELS']);commands=ast.literal_eval(hostvars['EXPECTED_COMMANDS'])
    check('all five original genuine stages complete',labels==['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit'] and len(commands)==5)
    check('all five physical/compiler/tool commands retained',commands[0][0]=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15' and commands[1][0]==commands[2][0]=='/usr/bin/nm' and commands[3][0]=='/usr/bin/otool' and commands[4][2]=='audit-build')
    for anchor in [
      "full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)",
      "helper.guard_admission(full)",
      "resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)",
      "resource.history_roots([str(HOST),str(SOURCE),str(OUT),str(TERMINAL)],support.ART)",
      "support.archive_bytes((HOST,SOURCE,OUT,TERMINAL,SOURCE_ARCHIVE))",
      "[support.pin(p) for p in sorted(SOURCE_ARCHIVE.rglob('*')) if p.is_file()]",
      "[support.pin(p) for root in (SOURCE,TERMINAL) for p in sorted(root.rglob('*')) if p.is_file()]",
      "runner.execute(HOST/'run','build',command,WHOLE_CAP)",
      "EXPECTED_COMMANDS or any(s['status']!='PASS' for s in inner)",
      "type(iw['returncode']) is not int or iw['returncode']!=0",
      "raw['before_binary_identity_gates'] is not True",
      "set(files)!=set(seal['files'])|{'seal.json'}",
      "for entry in inputs+[hpin,rpin]:",
      "('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')",
      "'b6b3b1477835bd6e312ac833d4cc681e0b7ca15482964f88daf0edb581d60206'",
      "'ad1d11d68f2ae052068bd6d752ce7b2d64c6cbfcf699713aa684cdc347655d7e'",
      "'3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'",
    ]:check('complete original genuine host predicate/source inventory '+anchor,anchor in cf2)
    check('host full definitions actual one original main',list(functions(cf2))==['main'])
    imports=[node for node in tree.body if isinstance(node,(ast.Import,ast.ImportFrom))]
    check('generator imports only standard library',all((isinstance(node,ast.Import) and all(alias.name.split('.')[0] in {'ast','hashlib','json','re','stat','sys'} for alias in node.names)) or isinstance(node,ast.ImportFrom) and node.module=='pathlib' for node in imports))
    calls=[node for node in ast.walk(tree) if isinstance(node,ast.Call)]
    check('generator never invokes eval exec importlib helper guard business APIs',not any(isinstance(node.func,ast.Name) and node.func.id in {'eval','exec','__import__'} or isinstance(node.func,ast.Attribute) and node.func.attr in {'exec_module','spec_from_file_location','guard_admission','verify_graph','run_build'} for node in calls))
    report=json.loads(data['SOURCE_DESIGN_REPORT.json'])
    check('source design explicitly leaves future actual args unknown',report['mandatory_future_PREP_argument_values'] is None)
    check('source design truthful unexecuted business template',all(report[k] is False for k in ['business_executed','helper_API_or_guard_called','ART_read_or_written','canonical_or_D_or_E_written','normal_host_generated']))
    check('source design reports nine actual evidence parameters',len(report['required_metadata_argument_order'])==9)
    for name,pin in pins.items():
        _,again=read(PACKAGE/name)
        check('all author SOURCE full EOF SHA7ID after review '+name,again==pin)
    for name,pin in original_live_pins.items():
        _,again=read(Path(name))
        check('all bounded lineage SOURCE full EOF SHA7ID after review '+name,again==pin)
    check('whole author SOURCE namespace unchanged after review',sorted(str(path.relative_to(PACKAGE)) for path in PACKAGE.rglob('*'))==inventory_before)
    value={
      'schema':'AXMAT_V21_COMPLETE_BUILD_GENERATOR_FINITE_INDEPENDENT_SOURCE_REVIEW_V1',
      'status':'SOURCE_PASS_UNREADY_AWAIT_REAL_V21_PREP_NOT_EXECUTED',
      'checks':checks,'all_checks_typed_true':True,'blockers':[],
      'complete_author_manifest':manifest_pin,'author_all_full_SOURCE_pins_before_after':pins,
      'bounded_explicit_original_lineage_SOURCE_pins_before_after':original_live_pins,
      'full_generator_15hunk_byte_and_AST_inverse_to_c8cf':True,
      'all6_generator_definitions_preserved_inverse':True,
      'unchanged4_source_reference_write_functions_byteexact':True,
      'future_host_only21_finite_literal_retargets':True,
      'old_d5fa_host17_inverse_cf2_and_cf2_13_inverse_37d':True,
      'original_c8cf_3hunk_inverse_dc48':True,
      'required_future_actual_PREP_metadata_argument_count':9,
      'all5_original_stages_tools_watchdogs_seal_raw4logs_and_4tails_preserved':True,
      'normal_guard_MRO_history_roots_resources_caps_and_complete_SOURCE_inventory_retained':True,
      'all_unknown_future_PREP_metadata_arguments_left_unknown':True,
      'reviewed_binding_branch_or_check_source_only_branch_executed':False,
      'future_normal_host_rendered':False,'project_API_helper_guard_business_executed':False,
      'ART_graph_numeric_payload_read':False,'canonical_or_frozen_namespace_written':False,
      'future_actual_business_or_native_or_science_qualification_claimed':False,
      'initial_inventory_filename_assumption_TOOL_FAILURE_preserved':True,
    }
    with (OUT/'REVIEW.json').open('x') as stream:json.dump(value,stream,indent=2,allow_nan=False);stream.write('\n')
    _,review_pin=read(OUT/'REVIEW.json')
    print(json.dumps(dict(status=value['status'],checks=len(checks),blockers=[],review=review_pin,
                          complete_all_author_members=manifest['member_count'],all6definitions=True,
                          future_host_not_rendered=True,API_guard_business_executed=False)))


if __name__=='__main__':main()
