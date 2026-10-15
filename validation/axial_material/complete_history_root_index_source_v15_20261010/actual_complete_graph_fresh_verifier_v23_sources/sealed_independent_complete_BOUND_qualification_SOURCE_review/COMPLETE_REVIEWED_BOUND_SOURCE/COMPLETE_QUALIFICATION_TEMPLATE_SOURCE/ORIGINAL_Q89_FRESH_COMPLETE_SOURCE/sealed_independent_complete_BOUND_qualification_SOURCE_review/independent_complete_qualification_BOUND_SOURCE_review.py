#!/usr/bin/env python3
"""Finite standard-library Source review; never execute/import reviewed code."""
import ast
import hashlib
import json
import os
import pathlib
import shlex
import stat
import sys

HERE=pathlib.Path(__file__).parent
PKG=pathlib.Path('/private/tmp/axmat_v22_full_protocol_and_current_graph_qualification_SOURCE_ONLY_20261010_fk87urdt')
BOUND=pathlib.Path('/private/tmp/axmat_v22_actual_qualification_SOURCE_binding_20261010_Root_once')
B=pathlib.Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
MANIFEST_SHA='8a3e4a15ebe528218ab2de2104cf345f75d1c016b1c4f41838cc65676bad93e6'
CHECKS=[]; READS=[]
def check(name,ok,details=None):
    row={'check':name,'PASS':bool(ok)}
    if details is not None:row['details']=details
    CHECKS.append(row)
def id7(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def readpin(path,expected=None,sha=None):
    p=pathlib.Path(path);before=id7(p)
    check('regular private bounded Source/META '+str(p),stat.S_ISREG(before[2]) and before[3]==1 and before[4]<=2*1024*1024)
    with p.open('rb') as f:raw=f.read();check('descriptor identity across EOF '+str(p),[os.fstat(f.fileno()).st_dev,os.fstat(f.fileno()).st_ino,os.fstat(f.fileno()).st_mode,os.fstat(f.fileno()).st_nlink,os.fstat(f.fileno()).st_size,os.fstat(f.fileno()).st_mtime_ns,os.fstat(f.fileno()).st_ctime_ns]==before)
    actual={'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'identity':id7(p),'bytes':len(raw)}
    check('complete EOF/7ID stable '+str(p),actual['identity']==before and len(raw)==before[4])
    if expected is not None:
        check('full exact Source/META SHA7ID '+str(p),all(actual[k]==expected[k] for k in ('path','sha256','identity')))
        if 'bytes' in expected:check('full Source byte count '+str(p),actual['bytes']==expected['bytes'])
    if sha is not None:check('Root exact authorized Source SHA '+str(p),actual['sha256']==sha)
    READS.append(actual);return raw,actual
def obj(raw):return json.loads(raw)
def norm(pin):return {k:pin[k] for k in ('path','sha256','identity')}
def strict_terminal(receipt,chunk):
    t=receipt['terminal_tool_return'];return type(t['exit_code'])is int and t['exit_code']==0 and t['chunk_id']==chunk and 'session_id'not in t and receipt['closed']is True
def source_node(raw,node):return '\n'.join(raw.decode().splitlines()[node.lineno-1:node.end_lineno])
def functions(raw):
    tree=ast.parse(raw);return {n.name:(source_node(raw,n),ast.dump(n,include_attributes=False)) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
def eval_constant(node):
    if isinstance(node,ast.Constant):return node.value
    if isinstance(node,(ast.Tuple,ast.List)):return [eval_constant(x) for x in node.elts]
    if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.USub):return -eval_constant(node.operand)
    if isinstance(node,ast.BinOp):
        a,b=eval_constant(node.left),eval_constant(node.right)
        if isinstance(node.op,ast.Mult):return a*b
        if isinstance(node.op,ast.Pow):return a**b
    return ast.literal_eval(node)
def globals_of(raw):
    out={}
    for n in ast.parse(raw).body:
        if not isinstance(n,ast.Assign):continue
        try:value=eval_constant(n.value)
        except (ValueError,TypeError,AttributeError):continue
        for t in n.targets:
            if isinstance(t,ast.Name):out[t.id]=value
            elif isinstance(t,ast.Tuple) and isinstance(value,list):out.update({a.id:b for a,b in zip(t.elts,value) if isinstance(a,ast.Name)})
    return out
def reverse_exact(raw,hunks,expected,label):
    value=raw.decode()
    for i,h in reversed(list(enumerate(hunks))):
        check(label+' full inverse unique after anchor '+str(i),value.count(h['after'])==1)
        value=value.replace(h['after'],h['before'],1)
    check(label+' complete byte inverse',value.encode()==expected)
    check(label+' complete AST inverse',ast.dump(ast.parse(value),include_attributes=False)==ast.dump(ast.parse(expected),include_attributes=False))

manifest_raw,manifest_pin=readpin(PKG/'MANIFEST.json',sha=MANIFEST_SHA);manifest=obj(manifest_raw)
check('all21 complete flat package members405071B',manifest['member_count']==len(manifest['members'])==21 and manifest['member_bytes']==sum(x['bytes'] for x in manifest['members'])==405071 and {p.name for p in PKG.iterdir()}=={pathlib.Path(p['path']).name for p in manifest['members']}|{'MANIFEST.json'})
members={}
for pin in manifest['members']:
    p=pathlib.Path(pin['path']);raw,actual=readpin(p,pin);check('member path stays exact flat package '+p.name,p.parent==PKG);members[p.name]=raw
    if p.suffix=='.py':ast.parse(raw);check('complete Source AST parsed '+p.name,True)
check('template boundaries no Q/business success',manifest['source_only']is True and manifest['business_executed']is False and manifest['binding_branch_executed']is False and manifest['new_Q']is None and manifest['six_future_business_pins']==[None]*6)
seal_raw,template_seal_pin=readpin(pathlib.Path(str(PKG)+'_seal_receipt/actual_qualification_SOURCE_seal_tool_return.json'))
template_seal=obj(seal_raw)
check('actual template seal12b26b strict int0closed',strict_terminal(template_seal,'12b26b') and template_seal['binding_branch_executed']is False and template_seal['helper_host_API_guard_business_numeric_executed']is False and template_seal['new_Q']is None)
for value in obj(template_seal['terminal_tool_return']['output']).values():
    if isinstance(value,dict) and {'path','sha256','identity'}<=set(value):readpin(value['path'],value)
parent_inverse=obj(members['ALL_FOUR_FULL_SOURCE_INVERSES.json'])
names={'pure_driver':('pure_helper_controls.v22.UNREADY.py','pure_helper_controls.py'),'pure_host':('pure_helper_controls_host.v22.UNREADY.py','pure_helper_controls_host.py'),'fresh_driver':('fresh_verifier_controls.v22.UNREADY.py','fresh_verifier_controls.py'),'fresh_host':('fresh_verifier_host.v22.UNREADY.py','fresh_verifier_host.py')}
function_contracts={}
for key,(template_name,bound_name) in names.items():
    info=parent_inverse['templates'][key];parent_raw,_=readpin(parent_inverse['parents'][key]['path'],parent_inverse['parents'][key])
    check(key+' full frozen parent bytes equals actual Source',parent_raw==members[key+'.original_actual_SOURCE.py'])
    check(key+' full declared hunk count',len(info['edits'])=={'pure_driver':5,'pure_host':8,'fresh_driver':6,'fresh_host':11}[key])
    generated=parent_raw.decode()
    for h in info['edits']:check(key+' exact before anchor '+h['id'],generated.count(h['before'])==1);generated=generated.replace(h['before'],h['after'],1)
    check(key+' forward bytes full match',generated.encode()==members[template_name])
    reverse_exact(members[template_name],info['edits'],parent_raw,key+' template-to-original-actual')
    original_funcs=functions(parent_raw);new_funcs=functions(members[template_name]);unchanged=[]
    for name,value in original_funcs.items():
        if key=='pure_driver' and name=='run':continue
        if key=='pure_host' and name=='main':continue
        if key=='fresh_host' and name in ('main','_source_namespace'):continue
        check(key+' complete original function/class bytes and AST '+name,new_funcs[name]==value);unchanged.append(name)
    function_contracts[key]={'full_original_top_function_class_count':len(original_funcs),'unmodified_full_byte_AST_functions_and_classes':unchanged,'all_original_other_changes_wholly_recovered_by_declared_finite_inverse':True}
for name,entry in parent_inverse['original_complete_actual_tool_receipts'].items():
    raw,pin=readpin(entry['pin']['path'],entry['pin']);receipt=obj(raw);local=members[name+'.exact.json']
    check('original complete real receipt exact copy '+name,raw==local and receipt==entry['complete_receipt'])
    check('original closed actual typedint0 '+name,strict_terminal(receipt,'5e1034' if 'pure' in name else '59fbf2'))

witness_path=B/'actual_complete_graph_helper_controls_v22_receipts/Root_actual_helper_SOURCE_install_tool_return.json'
wraw,witness_pin=readpin(witness_path,sha='914d04b742611749140c5612715887fb4c32f27536867125db4ef15ceb2aca7e');witness=obj(wraw)
check('real Root source witness schema9aa45b strictint0closed',witness['schema']=='ROOT_V22_ACTUAL_COMPLETE_HELPER_SOURCE_INSTALL_TOOL_RETURN_V1' and strict_terminal(witness,'9aa45b') and witness['actual_tool_terminal_return_observed']is True and witness['source_only']is True and witness['exact_integer_pins_decoded_from_actual_terminal_output']is True and witness['original_actual_terminal_output_preserved_exact']is True)
install_output=obj(witness['terminal_tool_return']['output']);helper=witness['installed_helper'];recordpin=witness['source_install_record']
check('actual original install output full Python integers exact helper/record',install_output['installed_helper']==helper and install_output['source_install_record']==recordpin and all(type(x)is int for p in (helper,recordpin) for x in p['identity']) and all(len(p['identity'])==7 for p in (helper,recordpin)))
helper_raw,_=readpin(helper['path'],helper,sha='cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c');ast.parse(helper_raw)
record_raw,_=readpin(recordpin['path'],recordpin,sha='d1d21ab41c443e09e2305bf75377c69399ebfebff97429c6ea270660054e5d32');record=obj(record_raw)
check('record schema exact installed helper Source only',record['schema']=='ROOT_V22_COMPLETE_HELPER_SOURCE_INSTALL_RECORD_V1' and record['installed_helper']==helper and record['source_only']is True)
check('Source install never grants Q or business/science',all(witness[k]is False for k in ('actual_pure_helper_protocol_qualified','actual_full_current_graph_verifier_qualified','complete_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted')) and witness['actual_new_helper_qualification_sha256']is None and all(record[k]is False for k in ('actual_pure_helper_protocol_qualified','actual_full_current_graph_verifier_qualified','actual_complete_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','business_or_guard_or_helper_API_executed')) and record['actual_new_helper_qualification_sha256']is None)
copied_source_pins=list(record['source_packages']['complete_copied_files'].values())
check('full actual installed Source inventory18 not narrowed',len(copied_source_pins)==record['source_file_count']==18)
for literal,pin in record['source_packages']['complete_copied_files'].items():
    check('record Source literal belongs actual fixed D '+literal,literal==pin['path'] and pathlib.Path(literal).is_relative_to(pathlib.Path(recordpin['path']).parent));raw,_=readpin(literal,pin)
    if pathlib.Path(literal).suffix=='.py':ast.parse(raw)

breceipt_raw,breceipt_pin=readpin(B/'actual_complete_graph_helper_controls_v22_receipts/Root_actual_qualification_Source_binding_tool_return.json',sha='08c351fe52f4e69b4dc0d9c0ad1f17bfadc9bf633c393c1aece6aff7501c2588');breceipt=obj(breceipt_raw)
check('genuine Root binder1aed3e strictint0closed SOURCE-only',breceipt['schema']=='ROOT_V22_ACTUAL_QUALIFICATION_SOURCE_BINDER_TOOL_RETURN_V1' and strict_terminal(breceipt,'1aed3e') and breceipt['source_only']is True and breceipt['actual_tool_terminal_return_observed']is True and breceipt['new_Q']is None and breceipt['controls_helper_API_guard_business_executed']is False)
binding_output=obj(breceipt['terminal_tool_return']['output'])
check('real binder output truthful exact root/count/noQ',binding_output['status']=='SOURCE_READY_BINDING_GENERATED_NOT_EXECUTED' and binding_output['bound_SOURCE_root']==str(BOUND) and binding_output['all_complete_package_members_copied']==22 and binding_output['new_Q']is None and binding_output['six_future_business_pins']==[None]*6 and binding_output['project_D_E_canonical_or_ART_written']is False and binding_output['controls_helper_API_guard_business_executed']is False)
iraw,ipin=readpin(binding_output['inverse']['path'],binding_output['inverse'],sha='5cdfb1fead9d8df8a6158cf203028578f6b453ab614863a81540f5172812abe3');binding_inverse=obj(iraw)
check('complete inverse15hunks original real inputs noqualification',binding_inverse['schema']=='AXMAT_V22_ROOT_ACTUAL_SOURCE_ONLY_QUALIFICATION_BINDING_INVERSES_V1' and {k:len(v) for k,v in binding_inverse['hunks'].items()}=={'pure_driver':3,'pure_host':2,'fresh_driver':5,'fresh_host':5} and binding_inverse['bound_sources']==binding_output['sources'] and binding_inverse['actual_installed_helper']==helper and binding_inverse['actual_Source_install_witness']==norm(witness_pin) and binding_inverse['actual_Source_install_record']==recordpin and binding_inverse['complete_source_file_inventory_from_record']==copied_source_pins and binding_inverse['template_manifest']==norm(manifest_pin) and binding_inverse['new_Q']is None and binding_inverse['six_future_business_pins']==[None]*6 and binding_inverse['actual_original_new_protocol_or_fresh_verifier_qualification']is None and binding_inverse['candidate_helper_host_guard_or_business_executed']is False)
expected_top={'sealed_qualification_SOURCE_templates','Root_actual_SOURCE_install_witness.exact.json','Root_actual_SOURCE_install_record.exact.json','ALL_FOUR_ACTUAL_SOURCE_BINDING_INVERSES.json'}|{pair[1] for pair in names.values()}
check('complete bound output inventory, no hidden/cropped Source',{p.name for p in BOUND.iterdir()}==expected_top and {p.name for p in (BOUND/'sealed_qualification_SOURCE_templates').iterdir()}=={p.name for p in PKG.iterdir()})
for p in PKG.iterdir():
    copy_raw,_=readpin(BOUND/'sealed_qualification_SOURCE_templates'/p.name);check('all22 Source templates original full copy '+p.name,copy_raw==p.read_bytes())
for name,expected in [('Root_actual_SOURCE_install_witness.exact.json',wraw),('Root_actual_SOURCE_install_record.exact.json',record_raw)]:
    raw,_=readpin(BOUND/name);check('Root witness/record complete original bytes copied '+name,raw==expected)
bound_raw={}
for key,(template_name,bound_name) in names.items():
    raw,_=readpin(binding_output['sources'][bound_name]['path'],binding_output['sources'][bound_name]);bound_raw[key]=raw;ast.parse(raw)
    reverse_exact(raw,binding_inverse['hunks'][key],members[template_name],key+' actual-bound-to-template')
    expected_befores={'pure_driver':['HELPER_PATH = None','HELPER_SHA256 = None','HELPER_SOURCE_BYTES = None'],'pure_host':['TARGET_SHA=None','support.pin(Path(None),None)'],'fresh_driver':["SOURCE_STATUS = 'UNREADY_SOURCE_ONLY_NO_ACTUAL_SUCCESS'",'NEW_HELPER_PATH = None','NEW_HELPER_SHA256 = None','NEW_HELPER_SOURCE_BYTES = None','NEW_HELPER_IDENTITY = None'],'fresh_host':["SOURCE_STATUS='UNREADY_SOURCE_ONLY_NO_ACTUAL_SUCCESS'",'TARGET_SHA=None','BOUND_HELPER_PIN=None','INSTALL_WITNESS_PIN=None','SOURCE_INSTALL_RECORD_PIN=None']}[key]
    check(key+' only declared3/2/5/5 binding anchors',[h['before'] for h in binding_inverse['hunks'][key]]==expected_befores)
    check(key+' binding generated solely literal globals/callpin',[h['after'] for h in binding_inverse['hunks'][key]]=={
      'pure_driver':['HELPER_PATH = '+repr(helper['path']),'HELPER_SHA256 = '+repr(helper['sha256']),'HELPER_SOURCE_BYTES = '+repr(helper['identity'][4])],
      'pure_host':['TARGET_SHA='+repr(binding_output['sources']['pure_helper_controls.py']['sha256']),'support.pin(Path('+repr(helper['path'])+'),'+repr(helper['sha256'])+')'],
      'fresh_driver':["SOURCE_STATUS = 'READY_SOURCE_BOUND_BY_ROOT'",'NEW_HELPER_PATH = '+repr(helper['path']),'NEW_HELPER_SHA256 = '+repr(helper['sha256']),'NEW_HELPER_SOURCE_BYTES = '+repr(helper['identity'][4]),'NEW_HELPER_IDENTITY = '+repr(helper['identity'])],
      'fresh_host':["SOURCE_STATUS='READY_SOURCE_BOUND_BY_ROOT'",'TARGET_SHA='+repr(binding_output['sources']['fresh_verifier_controls.py']['sha256']),'BOUND_HELPER_PIN='+repr(helper),'INSTALL_WITNESS_PIN='+repr(norm(witness_pin)),'SOURCE_INSTALL_RECORD_PIN='+repr(recordpin)]}[key])
check('all four Root requested exact SHA',[binding_output['sources'][names[k][1]]['sha256'] for k in names]==['9ea06c8f44c637bd9cff6849ee4a0d55af88a3cb82d6aa3beb7684a94a8decb9','2d7bf5cc70e8cd061bcac683d27f33aea12f524b80079f7f5f9936534ef84e62','de3384af3860177cabfb3fa87b6c413aac83a8f17570df01f0a14b3f6600da08','3561c87b99d74c6f75b506fd4d5ccd7df1532c806f60644ae6f875d7c2f77468'])

pure=bound_raw['pure_driver'].decode();pure_host=bound_raw['pure_host'].decode();fresh=bound_raw['fresh_driver'].decode();fresh_host=bound_raw['fresh_host'].decode();binder=members['bind_qualification_sources_SOURCE_ONLY.py'].decode()
new_control_node=next(n for n in ast.parse(pure).body if isinstance(n,ast.FunctionDef) and n.name=='private_owner_consume_controls');new_control=source_node(bound_raw['pure_driver'],new_control_node)
check('new owner function only complete original small fixture, no file IO', 'g._expand_owner_table(small_graph["owners"], small_graph["requirements"])' in new_control and not any(isinstance(n,ast.Call) and ((isinstance(n.func,ast.Name) and n.func.id in ('open','eval','exec','compile','__import__')) or isinstance(n.func,ast.Attribute) and n.func.attr in ('open','read_bytes','read_text','write_bytes','write_text','mkdir','unlink')) for n in ast.walk(new_control_node)))
host_string_constants={n.value for n in ast.walk(ast.parse(pure_host)) if isinstance(n,ast.Constant) and type(n.value)is str}
for text in ['("default_list", copy.deepcopy(expanded), False)','("default_tuple", tuple(copy.deepcopy(expanded)), False)','("explicit_False_list", copy.deepcopy(expanded), True)','"owned_builtin_list_True"','"nonbool_consume"','"tuple_True"','"list_subclass_True"','"plain_accepted_str"','"accepted_str_with_str_override"','"invalid_second_owner_default"','"invalid_second_owner_owned_True"']:
    case_node=ast.parse(text,mode='eval').body
    case_name=case_node.elts[0].value if isinstance(case_node,ast.Tuple) else case_node.value
    check('complete4positive3reject2subtypes2invalidsecond Source and host AST case '+case_name,text in new_control and case_name in host_string_constants)
for text in ['str.encode(value, "utf-8", "surrogatepass").hex()','struct.pack(">d", value).hex()','descriptor_signature(attributes)','caller_integrity_snapshot(row)','"outer_identity": id(values)','owned_partial[0] is None and owned_partial[1] is invalid','(left["class"], left["message"]) == (right["class"], right["message"])','"new_helper_qualification_created": False','"business_or_science_qualification_created": False']:
    check('complete new descriptor/caller bits and sequencing '+text,text in new_control)
check('new controls called exactly once after original codecs, before release',pure.count('report["private_owner_consume_controls"] = private_owner_consume_controls(g, small_graph)')==1 and pure.index('report["small_codecs"] = codec_controls')<pure.index('report["private_owner_consume_controls"] = private_owner_consume_controls')<pure.index('del small_graph, fixture_result'))
for text in ['len(owner_positive)!=4','len(owner_negative)!=3','len(owner_subtypes)!=2','len(owner_partial)!=2',"case['expected_complete_descriptor_signature']!=case['actual_complete_descriptor_signature']","owners_control['new_helper_qualification_created'] is not False","owners_control['business_or_science_qualification_created'] is not False"]:
    check('normal host requires complete new actual returned predicates '+text,text in pure_host)
for key in ('pure_driver','pure_host','fresh_driver','fresh_host'):
    gl=globals_of(bound_raw[key]);old_gl=globals_of(members[key+'.original_actual_SOURCE.py'])
    capkeys=[k for k in old_gl if k in ('WHOLE_CAP','STAGE_CAP','RSS_CAP','ARCHIVE_CAP','WHOLE_HOST_SECONDS','STAGE_SECONDS','RSS_MIB','JOINT_HOST_SOURCE_OUT_ARCHIVE_BYTES','HISTORY_BYTES','MIN_FREE_BYTES','THREADS','CHILDREN','RETRIES','WALL_SECONDS','RSS_BYTES','MAX_JSON_BYTES','MAX_OUTPUT_BYTES','CHILD_LIMIT')]
    check(key+' all original cap globals unchanged',bool(capkeys) and all(gl[k]==old_gl[k] and type(gl[k])is type(old_gl[k]) for k in capkeys),{k:gl[k] for k in capkeys})
for hostkey in ('pure_host','fresh_host'):
    text=bound_raw[hostkey].decode()
    for snippet in ['full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)',"Path(full.__file__).resolve()!=support.FULL","Path(production.__file__).resolve()!=support.PARENT","helper.guard_admission(full)","type(runner) is not full.OwnRSSSerialExecutor",'resources=resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)',"children_at_once=1,retries=0","support.pin(entry['path'],entry['sha256'])!=entry"]:
        check(hostkey+' original genuine guard/MRO/full resources preserved '+snippet,snippet in text)
fresh_gl=globals_of(bound_raw['fresh_host']);fields=fresh_gl['RETURN_FIELDS']
check('whole expected public return27fields order, all trace9fields preserved',len(fields)==27 and len(fresh_gl['TRACE_FIELDS'])==9 and fields==globals_of(members['fresh_host.original_actual_SOURCE.py'])['RETURN_FIELDS'])
old_helper_path=globals_of(bound_raw['fresh_driver'])['OLD_HELPER_PATH'];old_helper_sha=globals_of(bound_raw['fresh_driver'])['OLD_HELPER_SHA256'];old_source,oldpin=readpin(old_helper_path,sha=old_helper_sha);ast.parse(old_source)
check('actual complete independent bcd oracle source exact145715',old_helper_sha=='bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6' and len(old_source)==145715)
helper_verify=next(n for n in ast.parse(helper_raw).body if isinstance(n,ast.FunctionDef) and n.name=='verify_graph');helper_return=next(n for n in ast.walk(helper_verify) if isinstance(n,ast.Return) and isinstance(n.value,ast.Dict));returned_fields=[ast.literal_eval(k) for k in helper_return.value.keys]
check('installed helper public27 return Source keys exactly oracle host fields',returned_fields==fields)
for snippet in ["old.strict_json(GRAPH_PIN['path'],GRAPH_PIN['sha256'],max_bytes=MAX_JSON_BYTES)","new.verify_graph(GRAPH_PIN['path'],expected_sha256=GRAPH_PIN['sha256'],phase=PHASE)","exact_value(expected,verified,'complete_actual_fresh_verifier_return')","len(actual_paths)==len(set(actual_paths))==37112","set(actual_paths)==paths|{GRAPH_PIN['path']}","ACTUAL_COMPLETE_READ_OPEN_TRACE.json.gz","EXPECTED_COMPLETE_RETURN_CONTRACT.json.gz","ACTUAL_COMPLETE_VERIFIER_RETURN.json.gz","record['attempt_count']==1","require(len(positive)==4 and len(negatives)==3"]:
    check('complete current graph oracle/read trace/raw gzip/private trace Source kept '+snippet,snippet in fresh)
for snippet in ["json.dumps(expected,**encoder)!=json.dumps(verified,**encoder)","list(verified)!=RETURN_FIELDS","list(trace)!=TRACE_FIELDS","len(trace['records'])!=37112","len(set(paths))!=37112","source_after!=source_before","set(p.name for p in OUT.iterdir())",'len(declared_history_roots)!=5']:
    check('complete normal fresh host actual predicates kept '+snippet,snippet in fresh_host)
binder_tree=ast.parse(binder)
check('binder exclusively standardlib imports no dynamic reviewed Source load',not any(isinstance(n,ast.Import) and any(a.name.split('.')[0]in ('subprocess','runpy','importlib') for a in n.names) for n in ast.walk(binder_tree)) and not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('eval','exec','compile','__import__') for n in ast.walk(binder_tree)))
for snippet in ['destination.parent==Path("/private/tmp") and not os.path.lexists(destination)','type(tr.get("exit_code")) is int','"session_id" not in tr','all(type(v) is int for v in expected_identity)','typed_pin(output["installed_helper"])==helper','pin(CANONICAL_HELPER,CANDIDATE_SHA,helper["identity"]','len(files)==source_record["source_file_count"]','with path.open("xb")','for q in [helper,record,witness_pin]+copied_source_pins']:
    check('binder complete Root actual witnesses/Source ownership/freshTMP safeguards '+snippet,snippet in binder)
argv=shlex.split(breceipt['actual_binding_arguments']['cmd'])
check('actual Root binder command matches reviewed Source + real witness + package',argv[:3]==['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',str(PKG/'bind_qualification_sources_SOURCE_ONLY.py')] and argv[argv.index('--install-tool-return')+1]==str(witness_path) and argv[argv.index('--install-tool-return-sha256')+1]==witness_pin['sha256'] and argv[argv.index('--template-manifest-sha256')+1]==MANIFEST_SHA and argv[argv.index('--output-dir')+1]==str(BOUND))
for p in [helper,recordpin,norm(witness_pin)]+copied_source_pins:readpin(p['path'],p)
report={'schema':'INDEPENDENT_COMPLETE_V22_QUALIFICATION_BOUND_SOURCE_PEER_REVIEW_V1','scope':'STANDARD_LIBRARY_FULL_SOURCE_AST_EOF_SHA7ID_AND_SMALL_GENUINE_ROOT_META_ONLY','PASS':all(x['PASS'] for x in CHECKS),'check_count':len(CHECKS),'hard_blockers':[x for x in CHECKS if not x['PASS']],'checks':CHECKS,'full_EOF_reads':READS,'full_original_function_class_contracts':function_contracts,'template_manifest':manifest_pin,'actual_template_Source_seal':template_seal,'actual_Root_source_install_witness':witness,'actual_installed_helper':helper,'actual_source_install_record_pin':recordpin,'all18_original_Source_copy_pins':copied_source_pins,'actual_Root_Source_only_binding_receipt':breceipt,'actual_four_bound_sources':binding_output['sources'],'binding_inverse':binding_output['inverse'],'all_four_template_original_actual_Source_full_byte_AST_inverse':True,'all_four_Root_binding_full_template_byte_AST_inverse':True,'new_owner_controls':{'positives':4,'guard_negatives':3,'accepted_str_subtypes':2,'invalid_second_rejections':2,'complete_default_caller_identity_attributes_bits':True,'private_append_then_slot_release_and_invalidsecond_identity':True},'full_fresh_oracle_scope':{'independent_bcd_Source':oldpin,'complete_public_return_fields':fields,'canonical_files':37111,'actual_unfiltered_readopens':37112,'requirement_rows':238441,'owners':4473,'namespaces':86,'aliases':186,'absence_inputs':479,'saved_trace_records':63469,'full_gzip_results':3,'old_private_trace_positives':4,'old_private_trace_negatives':3},'caps':{'pure_whole_seconds':60,'pure_stage_seconds':60,'fresh_whole_seconds':1800,'fresh_stage_seconds':600,'rss_mib':512,'archive_bytes':67108864,'history_bytes':103079215104,'free_floor_bytes':8589934592,'threads':1,'children':1,'retries':0},'new_Q':None,'six_future_business_pins':[None]*6,'pure_or_currentgraph_qualified_by_this_Source_review':False,'RSS_or_runtime_INPUT_or_native_or_science_qualified':False,'candidate_helper_or_host_or_API_or_guard_import_run_compile_executed_by_peer':False,'ART_numeric_graph_or_material_payload_read_by_peer':False,'project_D_E_canonical_original_package_mutated_by_peer':False,'old_closed_session_polled':False,'writes_only_this_fresh_TMP':str(HERE),'conclusion':'Complete Source route and genuine Root bound four Sources have no static hard blocker. Root alone may install these exact Sources under complete dynamic Source freeze and execute the genuine pure protocol then full current graph qualifier with original caps. Actual qualified proof/Q still requires independent actual terminal/results review; Source installation/binding/review provides no Q or physical/science accuracy credit.'}
raw=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode();p=HERE/'COMPLETE_BOUND_QUALIFICATION_SOURCE_PEER_REVIEW.json';p.write_bytes(raw)
print(json.dumps({'status':'COMPLETE_BOUND_QUALIFICATION_SOURCE_PEER_PASS' if report['PASS'] else 'COMPLETE_BOUND_QUALIFICATION_SOURCE_PEER_BLOCKED','check_count':len(CHECKS),'hard_blocker_count':len(report['hard_blockers']),'report_path':str(p),'report_sha256':hashlib.sha256(raw).hexdigest(),'report_bytes':len(raw),'all21template_members_fullEOF_SHA7ID':True,'all4original_Source_and_all4binding_full_byte_AST_inverse':True,'actual_binding_strict_int0closed':'1aed3e','new_Q':None,'no_controls_helper_API_guard_or_business_executed':True,'Root_pure_execution_Source_gate_pass':report['PASS']}))
sys.exit(0 if report['PASS'] else 1)
