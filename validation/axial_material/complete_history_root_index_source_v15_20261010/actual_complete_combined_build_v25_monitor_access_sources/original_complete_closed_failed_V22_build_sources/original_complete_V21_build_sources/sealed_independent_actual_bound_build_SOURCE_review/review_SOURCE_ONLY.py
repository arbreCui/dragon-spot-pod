"""Review fixed bound build SOURCE and permitted small Root META only, never ART or APIs."""
import ast
import hashlib
import json
import os
import stat
from pathlib import Path

P=Path('/private/tmp/axmat_v21_complete_build_host_actual_SOURCE_binding_20261010_9l6eaiab')
OUT=Path('/private/tmp/axmat_v21_actual_bound_complete_build_HOST_independent_SOURCE_review_20261010_f5v2c')
EXPECTED_MANIFEST='4005ae585a6c0a3bcd6f94f6ecc92a7dbca6fe75d23a562b9f54cc2a403bc088'


def pin(path):
    path=Path(path)
    if '/validation/artifacts/' in str(path):raise ValueError('SOURCE review must not read ART payloads')
    first=path.lstat();fields=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    if not stat.S_ISREG(first.st_mode) or first.st_nlink!=1 or path.resolve()!=path:raise ValueError('Ordinary complete singlelink SOURCE or permitted Root META required')
    with path.open('rb') as stream:
        if fields(os.fstat(stream.fileno()))!=fields(first):raise ValueError('SOURCE changed before open')
        data=stream.read()
        if fields(os.fstat(stream.fileno()))!=fields(first):raise ValueError('SOURCE changed during full EOF read')
    if fields(path.lstat())!=fields(first) or len(data)!=first.st_size:raise ValueError('SOURCE changed during read')
    return data,dict(path=str(path),sha256=hashlib.sha256(data).hexdigest(),identity=fields(first))


def undo(text,changes):
    for record in reversed(changes):
        if text.count(record['after'])!=record['count']:raise ValueError('Exact finite source inverse required')
        text=text.replace(record['after'],record['before'])
    return text


def functions(source):
    lines=source.splitlines(keepends=True)
    return {n.name:''.join(lines[n.lineno-1:n.end_lineno]) for n in ast.parse(source).body
            if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}


def assignment(tree,name):
    return next(n.value for n in tree.body if isinstance(n,ast.Assign)
                and any(any(isinstance(t,ast.Name) and t.id==name for t in ast.walk(target)) for target in n.targets))


def main():
    checks=[];additional_pins={}
    def check(name,value):
        if value is not True:raise ValueError('Bound build SOURCE check: '+name)
        checks.append(dict(name=name,value=True))
    mb,mp=pin(P/'Root_complete_bound_SOURCE_manifest.json');m=json.loads(mb)
    check('complete final bound SOURCE manifest SHA',mp['sha256']==EXPECTED_MANIFEST)
    check('complete bound manifest actual schema and scope',m['schema']=='AXMAT_V21_REAL_ROOT_PREP_BOUND_COMPLETE_BUILD_SOURCE_SEALED_MANIFEST_V1' and m['this_manifest_is_complete_bound_source_inventory'] is True and m['copied_design_manifest_is_lineage_only'] is True)
    members={Path(record['path']).name:record for record in m['members']}
    check('all actual19 members plus separate fullmanifest unique and complete',len(members)==len(m['members'])==m['member_count']==19 and set(path.name for path in P.iterdir())==set(members)|{'Root_complete_bound_SOURCE_manifest.json'})
    data={};before={}
    for name,record in members.items():
        b,q=pin(P/name);check('whole bound SOURCE EOF SHA7ID '+name,q==record)
        data[name]=b;before[name]=q
    before['Root_complete_bound_SOURCE_manifest.json']=mp
    host=data['combined_build_host.py'].decode();proof=json.loads(data['Root_finite_build_host_source_inverse.json'])
    check('actual fixed whole host ebe99 SOURCE SHA',before['combined_build_host.py']['sha256']=='ebe99a7aaf7abd4e073d0e206bea205344e186d5a3be144a012443f1cd51a196' and proof['host_sha256']==before['combined_build_host.py']['sha256'])
    check('exact21 finite host hunks no algorithm rewrite',len(proof['changes'])==proof['finite_change_count']==21)
    parent=data['frozen_cf2c_combined_build_host_v17.py'].decode();normal=data['frozen_37d_normal_prepare_host.py'].decode()
    restored=undo(host,proof['changes'])
    check('whole21 SOURCE byte inverse to unchanged cf2c',restored==parent)
    check('whole21 SOURCE AST inverse to unchanged cf2c',ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False))
    oldproof=proof['original_cf2c_to_37d_thirteen_change_inverse']
    check('original thirteen finite full ancestor inverse',len(oldproof['changes'])==oldproof['finite_change_count']==13 and undo(parent,oldproof['changes'])==normal)
    check('whole thirteen AST ancestor inverse',ast.dump(ast.parse(undo(parent,oldproof['changes'])),include_attributes=False)==ast.dump(ast.parse(normal),include_attributes=False))
    check('all original host definitions actual one main',list(functions(host))==list(functions(parent))==['main'])
    check('entire main body byte restored without selecting checks',functions(restored)['main']==functions(parent)['main'])
    htree,ptree=ast.parse(host),ast.parse(parent)
    for kind in (ast.If,ast.Raise,ast.Assert,ast.Return,ast.Call):
        check('all original host '+kind.__name__+' count retained',sum(isinstance(n,kind) for n in ast.walk(htree))==sum(isinstance(n,kind) for n in ast.walk(ptree)))
    check('all original host Call callee sequence retained',[ast.dump(n.func,include_attributes=False) for n in ast.walk(htree) if isinstance(n,ast.Call)]==[ast.dump(n.func,include_attributes=False) for n in ast.walk(ptree) if isinstance(n,ast.Call)])
    gen=data['generate_build_host.py'].decode();genparent=data['frozen_parent_generate_build_host_v20.py'].decode();gp=json.loads(data['source_inverse_proof.json'])
    check('full fixed admitted SOURCE generator d5d2 byteexact',before['generate_build_host.py']['sha256']=='d5d206232ad42927e235b0f947bd893b28eafcfcb593369b4dba7adb96a640e8')
    check('generator all fifteen full byte andAST inverse preserved',len(gp['changes'])==15 and undo(gen,gp['changes'])==genparent and ast.dump(ast.parse(undo(gen,gp['changes'])),include_attributes=False)==ast.dump(ast.parse(genparent),include_attributes=False))
    check('all actual generator6 original definitions preserved',list(functions(gen))==list(functions(genparent)) and len(functions(gen))==6)
    old_design=json.loads(data['design_sealed_manifest_exact_copy.json'])
    check('all twelve original Source design members retained byteexact',old_design['member_count']==len(old_design['members'])==12 and all(before[Path(ref['path']).name]['sha256']==ref['sha256'] and before[Path(ref['path']).name]['identity'][4]==ref['identity'][4] for ref in old_design['members']))
    check('original whole design manifest retained SHA e5bb',before['design_sealed_manifest_exact_copy.json']['sha256']=='e5bb1dcc8bcefd92b7ee66c8e5e39abb6d82e712eb928bd71cc6fb1d418445a1')
    for name in members:
        if name.endswith('.py'):
            compile(ast.parse(data[name].decode()),'<full SOURCE parse only '+name+'>','exec')
            check('entire SOURCE file parsed without import or execution '+name,True)
    def read_ref(ref):
        b,q=pin(ref['path']);check('complete pinned SOURCE or small actual Root META '+ref['path'],q==ref)
        if ref['path'] in additional_pins:check('repeated pinned SOURCE or Root META before pin exact '+ref['path'],additional_pins[ref['path']]==q)
        additional_pins[ref['path']]=q
        return b
    for ref in proof['checked_source_pins']:read_ref(ref)
    summary=json.loads(read_ref(proof['actual_Root_closed_PREP_summary']))
    terminal=json.loads(read_ref(proof['actual_Root_closed_terminal']))
    namespace=json.loads(read_ref(proof['actual_Root_complete_namespace_freeze']))
    check('same actual Root summary21ee and complete namespacef075 fixed',proof['actual_Root_closed_PREP_summary']['sha256']=='21ee531ce1a2032cb2d6fb86fe86603ae1a9bec3300ff982d033248ac9700344' and proof['actual_Root_complete_namespace_freeze']['sha256']=='f0759d38c8cc6c5340968ea6905b9537eeb5f80bafc71a452d76bfb12b58852f')
    check('actual PREP summary schema/status not build',summary['schema']=='ROOT_V21_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1' and summary['status']=='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD')
    tr=terminal['terminal_tool_return']
    check('true Root78a34b/session16256→e0647a strict0closed no repoll',terminal['initial_tool_return']['chunk_id']=='78a34b' and type(terminal['initial_tool_return']['session_id']) is int and terminal['initial_tool_return']['session_id']==16256 and tr['chunk_id']=='e0647a' and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr and terminal['closed'] is True and terminal['session_repolled_after_close'] is False)
    check('actual Root terminal aliases complete pin exact',summary['Root_actual_terminal']==summary['actual_root_terminal']==proof['actual_Root_closed_terminal'])
    required=[proof['actual_Root_closed_PREP_summary']['path'],proof['actual_Root_closed_PREP_summary']['sha256'],proof['actual_Root_closed_terminal']['sha256'],proof['actual_Root_complete_namespace_freeze']['sha256'],summary['actual_declaration']['sha256'],proof['actual_source_admission_output_pin_from_complete_namespace']['sha256'],summary['formal_PREP_terminal']['sha256'],summary['actual_complete_input_graph']['sha256'],summary['actual_complete_creation_trace']['sha256']]
    check('all nine actual required metadata args exact in order',proof['actual_required_metadata_argv']==required and proof['metadata_binding_parameter_count']==len(required)==9)
    ns={entry['root']:entry for entry in namespace['namespaces']}
    check('same full actual five H/S/O/T/D namespaces unique no businesscredit',len(ns)==len(namespace['namespaces'])==5 and namespace['schema']=='ROOT_V21_ACTUAL_COMPLETE_PREPARE_ALL_NAMESPACES_V1' and namespace['no_build_or_native_credit'] is True)
    desired=proof['actual_output_pins_bound_by_closed_Root_metadata_without_ART_read']
    check('all five actual prepared output pins complete keyset',set(desired)=={'actual_declaration','actual_complete_input_graph','actual_complete_creation_trace','actual_prep_terminal','actual_source_admission'})
    for key,ref in desired.items():
        path=Path(ref['path']);check('same complete actual namespace full pathSHA7ID '+key,ns[str(path.parent)]['files'][path.name]==ref and len(ref['identity'])==7 and all(type(x) is int for x in ref['identity']) and stat.S_ISREG(ref['identity'][2]) and ref['identity'][3]==1 and ref['identity'][4]>0)
    check('actual full source_admission from SOURCE unique path',desired['actual_source_admission']==proof['actual_source_admission_output_pin_from_complete_namespace'] and desired['actual_source_admission']['path']=='/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v21-20261010/source_admission.json')
    check('all actual prepared aliases exact',desired['actual_declaration']==summary['actual_declaration'] and desired['actual_complete_input_graph']==summary['actual_input_graph']==summary['actual_complete_input_graph'] and desired['actual_complete_creation_trace']==summary['actual_complete_creation_trace'] and desired['actual_prep_terminal']==summary['formal_PREP_terminal'])
    stage_labels=ast.literal_eval(assignment(htree,'EXPECTED_LABELS'));commands=ast.literal_eval(assignment(htree,'EXPECTED_COMMANDS'))
    check('full five original labels and five original static commands',stage_labels==['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit'] and len(commands)==5)
    old_commands=ast.literal_eval(assignment(ptree,'EXPECTED_COMMANDS'))
    adjusted=[]
    for row in old_commands:
        rewritten=[]
        for value in row:
            for change in proof['changes']:value=value.replace(change['before'],change['after'])
            rewritten.append(value)
        adjusted.append(rewritten)
    check('all five original complete static commands only exact21literal retarget',commands==adjusted)
    check('five tools/compiler and physical objects unchanged',commands[0][0]=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15' and commands[1][0]==commands[2][0]=='/usr/bin/nm' and commands[3][0]=='/usr/bin/otool' and commands[4][2]=='audit-build' and commands[0][1:-2]==old_commands[0][1:-2])
    for anchor in [
      "WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30",
      "support.pin(p) for p in sorted(SOURCE_ARCHIVE.rglob('*')) if p.is_file()",
      "for root in (SOURCE,TERMINAL) for p in sorted(root.rglob('*')) if p.is_file()",
      "full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)",
      "helper.guard_admission(full)",
      "roots=resource.history_roots([str(HOST),str(SOURCE),str(OUT),str(TERMINAL)],support.ART)",
      "resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)",
      "runner.execute(HOST/'run','build',command,WHOLE_CAP)",
      "for entry in inputs+[hpin,rpin]:",
      "support.archive_bytes((HOST,SOURCE,OUT,TERMINAL,SOURCE_ARCHIVE))",
      "('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')",
      "raw['before_binary_identity_gates'] is not True",
      "set(files)!=set(seal['files'])|{'seal.json'}",
      "inner_watches!=result['watchdogs'] or inner_watches[:-1]!=audit['previous_stage_watchdogs']",
      "corrected_runtime",
      "threads=1,children_at_once=1,retries=0",
      "whole_combined_INPUT_admitted=False",
      "native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False",
    ]:check('all original fullSOURCE inventory genuineguard stages seal tails caps predicate '+anchor,anchor in host)
    for constant in ('3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7','b6b3b1477835bd6e312ac833d4cc681e0b7ca15482964f88daf0edb581d60206','ad1d11d68f2ae052068bd6d752ce7b2d64c6cbfcf699713aa684cdc347655d7e'):
        check('original support/component successful prerequisite pin unchanged '+constant,constant in host and constant in parent)
    check('new qualified helper and Q actual full literal pins bound',all(value in host for value in ('combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py','dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7','Root_actual_complete_graph_private_verifier_helper_admission_v21.json','29ac1abd0df3ff9d1d71a3239842e1c97cb2619cc4627292b0d25f6e16218bb2')))
    check('old failed namespace/helper pins not reused',all(value not in host for value in ('combined-runtime-v20-20261010','build-host-v20-20261010','bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6','d49036e0a0fd396dd9550e81fd310b74442a867e7a4cc36ff2b16bf70a9c6bf8')))
    canonical=read_ref(proof['checked_source_pins'][-1]).decode();ct=ast.parse(canonical)
    future=[n for n in ct.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id.startswith('FUTURE_ACTUAL_COMBINED_')]
    future_native=assignment(ct,'FUTURE_ACTUAL_NATIVE_TERMINAL_SHA')
    check('all six future canonical business pins remain None',len(future)==5 and all(ast.literal_eval(n.value) is None for n in future) and ast.literal_eval(future_native) is None)
    old_canonical_path=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v20.py')
    old_canonical,old_pin=pin(old_canonical_path);additional_pins[str(old_canonical_path)]=old_pin
    check('unchanged exact old canonical SOURCE ancestor566939',old_pin['sha256']=='566939e3fbc7eddcc2b5af324a6dd11e97f83b033994e36389f7819d06084de3')
    ot=ast.parse(old_canonical)
    new_stage=next(n for n in ct.body if isinstance(n,ast.FunctionDef) and n.name=='stage_commands')
    old_stage=next(n for n in ot.body if isinstance(n,ast.FunctionDef) and n.name=='stage_commands')
    check('complete actual canonical stage_commands bytes andAST unchanged',functions(canonical)['stage_commands']==functions(old_canonical.decode())['stage_commands'] and ast.dump(new_stage,include_attributes=False)==ast.dump(old_stage,include_attributes=False))
    for name in ['NM','OTOOL','OLD','PHYSICAL','DEDUP','TRIM']:
        check('all original physical/tool canonical SOURCE AST unchanged '+name,ast.dump(assignment(ct,name),include_attributes=False)==ast.dump(assignment(ot,name),include_attributes=False))
    tools=json.loads(data['Root_actual_bound_SOURCE_tool_returns.json'])
    for key,chunk in [('actual_fresh_TMP_copy_terminal_return','69d1c2'),('actual_Source_render_terminal_return','9f0b06'),('actual_Source_self_review_terminal_return','a4ee72')]:
        tr_=tools[key];check('true actual SOURCE tool '+chunk+' strict0closed',tr_['chunk_id']==chunk and type(tr_['exit_code']) is int and tr_['exit_code']==0 and 'session_id' not in tr_)
    check('actual Source render true nine args exact all pins',tools['actual_Source_render_arguments']['argv'][1:]==required)
    check('actual SOURCE render host hash and21inverse truthful',json.loads(tools['actual_Source_render_terminal_return']['output'])['host_sha256']==before['combined_build_host.py']['sha256'] and json.loads(tools['actual_Source_render_terminal_return']['output'])['finite_change_count']==21)
    check('actual Source-only tool scope honest no executing boundhost',tools['render_generated_host_only_not_executed'] is True and tools['project_canonical_D_E_ART_not_written'] is True and tools['closed_Root_PREP_session_not_repolled'] is True)
    check('first Source self-review error honestly retained',type(tools['first_Source_self_review_terminal_return']['exit_code']) is int and tools['first_Source_self_review_terminal_return']['exit_code']==1 and 'first_Source_self_review_correction' in tools)
    review=json.loads(data['SOURCE_SELF_REVIEW.json'])
    check('author review honest Source-only scope and unknown future business',all(review[key] is False for key in ['normal_host_executed','project_guard_helper_driver_or_canonical_API_imported','business_or_numeric_or_build_executed','ART_glob_or_payload_read','closed_sessions_repolled','project_D_E_or_canonical_or_original_sealed_package_written','whole_build_INPUT_native_AAA_ABA_or_physics_qualified']))
    for name,expected in before.items():check('all complete bound member full EOF SHA7ID after independent review '+name,pin(P/name)[1]==expected)
    for path,expected in additional_pins.items():check('all bounded Source and Root META full EOF SHA7ID after independent review '+path,pin(Path(path))[1]==expected)
    check('complete bound package member namespace unchanged',set(path.name for path in P.iterdir())==set(members)|{'Root_complete_bound_SOURCE_manifest.json'})
    value={
      'schema':'AXMAT_V21_ACTUAL_BOUND_COMPLETE_BUILD_HOST_FINITE_INDEPENDENT_SOURCE_REVIEW_V1',
      'status':'SOURCE_PASS_ACTUAL_PREP_BOUND_HOST_UNEXECUTED_ROOT_NORMAL_BUILD_REQUIRED',
      'checks':checks,'all_checks_typed_true':True,'blockers':[],
      'complete_actual_bound_SOURCE_manifest':mp,'all_bound_SOURCE19_members_plus_manifest_full_EOF_SHA7ID_beforeafter':before,
      'all_bounded_Source_and_small_Root_META_pins_beforeafter':additional_pins,
      'host':before['combined_build_host.py'],'actual_source_render_chunk':'9f0b06',
      'actual_nine_PREP_metadata_arguments':required,
      'full21_host_byte_AST_inverse_cf2c_and13_inverse37d':True,
      'all_actual_one_main_definition_and_all_Call_If_Raise_Assert_Return_retained':True,
      'all6_generator_definitions_and_full15_inverse_retained':True,
      'all_original_design12members_exact_and_new_whole_bound19members_retained':True,
      'all_five_prepared_output_fullpins_match_same_true_Root_PREP_namespace':True,
      'source_inventory_dynamic_unfiltered_build_ARCHIVE_and_all_prepared_SOURCE_TERMINAL_retained':True,
      'all5_original_stage_commands_tools_physical_inputs_and_full_predicates_retained':True,
      'all_original_raw4logs_5watch_fullseal_runtime_identity_and4tails_retained':True,
      'genuine_original_guard_MRO_resources_and_1800_600_512_2GiB_96GiB_free8GiB_1_1_0_caps_retained':True,
      'all_future_business6pins_None':True,
      'actual_ART_declaration_values_NOT_independently_decoded_or_recomputed_by_this_SOURCE_review':True,
      'runtime_original_exact_fivecommand_gate_retained':True,
      'bound_host_or_generator_or_helper_guard_API_executed_by_reviewer':False,
      'ART_or_numeric_payload_read':False,'closed_sessions_repolled':False,
      'D_E_canonical_original_source_packages_written':False,
      'actual_BUILD_whole_INPUT_native_AAA_ABA_or_science_success_qualified':False,
    }
    with (OUT/'REVIEW.json').open('x') as stream:json.dump(value,stream,indent=2,allow_nan=False);stream.write('\n')
    _,review_pin=pin(OUT/'REVIEW.json')
    print(json.dumps(dict(status=value['status'],checks=len(checks),blockers=[],review=review_pin,
                          complete_Source_member_count=19,full_inverse_hunks=21,
                          actual9PREPpins=True,host_executed=False,ART_payload_read=False)))


if __name__=='__main__':main()
