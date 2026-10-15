"""Independent finite directory-isolation Source review; no candidate runs.

Root supplies a closed actual Source manifest/inverse and four actual Source
pins. We read full bytes and AST, and permit only the named global directory
assignments plus their derived canonical SHA. No schema, physical input,
helper Q/proofs, owner list, monitoring, MRO or runtime predicate may change.
All new PREP/build/native/science success remains unknown/False.
"""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

R=Path('/Users/wen/spot')
B=R/'validation/axial_material/complete_history_root_index_source_v15_20261010'
OLD_D=B/'actual_complete_combined_prepare_v25_sources'
OLD_C=R/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25.py'
ORIGINALS=dict(canonical=OLD_C,prepare_host=OLD_D/'combined_prepare_host.py',prepare_writer=OLD_D/'write_actual_prepare_terminal.py',prelaunch=OLD_D/'Root_complete_PREP_prelaunch.py')
ALLOWED=dict(canonical={'SOURCE','OUT','TERMINAL','FORMAL_FACTORY'},prepare_host={'HOST','TARGET','SOURCE','OUT','TERMINAL','SOURCE_ARCHIVE','FUTURE_V25_CANONICAL_SHA'},prepare_writer={'D','E','H','S','O','T','FACTORY','FUTURE_V25_CANONICAL_SHA'},prelaunch={'D','E','C','H','S','O','T'})
Q_SHA='c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b'
HELPER_SHA='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'
OLD_CANONICAL_SHA='7861841e839562234154bfd6e035025a3c5ed381d3c46a7be32f73b2abeb4bed'
PRIOR_PEER_SHA='14de4e9534e3bc2b561bca247950eed07954351a7c0f943c0d796e3609ae02eb'
FUTURE_BUSINESS=('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA')
CHECKS=[]
PINS={}


def pin_from_cache(p):
    return PINS[str(p)]


def need(value,label):
    if type(value) is not bool or value is not True: raise ValueError(label)
    CHECKS.append(dict(check=label,passed=True))


def identity(p):
    s=Path(p).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def pin(p):
    p=Path(p);i=identity(p)
    need(p.is_absolute() and '..' not in p.parts and stat.S_ISREG(i[2]) and i[3]==1,'ordinary absolute single-link Source/META '+str(p))
    with p.open('rb') as f: sha=hashlib.file_digest(f,'sha256').hexdigest()
    need(identity(p)==i,'complete Source EOF stable '+str(p))
    v=dict(path=str(p),sha256=sha,size_bytes=i[4],identity=i)
    if str(p) in PINS: need(PINS[str(p)]==v,'all repeated Source pins unchanged '+str(p))
    else:PINS[str(p)]=v
    return v


def fullpin(ref,label):
    need(type(ref) is dict and set(ref)=={'path','sha256','size_bytes','identity'},label+' exact four fields')
    need(type(ref['identity']) is list and len(ref['identity'])==7 and all(type(x) is int for x in ref['identity']),label+' seven exact integer identities')
    need(type(ref['size_bytes']) is int and ref['size_bytes']==ref['identity'][4] and type(ref['sha256']) is str and len(ref['sha256'])==64,label+' typed whole byte size and SHA')
    current=pin(ref['path']);need(current==ref,label+' actual full EOF SHA7ID')
    return current


def pairs(items):
    d={}
    for k,v in items:
        if k in d:raise ValueError('duplicate Source META JSON key')
        d[k]=v
    return d


def meta(p):
    before=pin(p)
    v=json.loads(Path(p).read_bytes(),object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError('nonfinite Source META')))
    need(pin(p)==before,'complete Source META bytes unchanged '+str(p))
    return v


def source(p):
    before=pin(p);text=Path(p).read_text(encoding='utf-8');tree=ast.parse(text,filename=str(p))
    need(pin(p)==before,'whole Source AST bytes unchanged '+str(p))
    return text,tree


def assignments(tree):
    result={}
    for node in tree.body:
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
            name=node.targets[0].id
            need(name not in result,'unique top-level Source global '+name)
            result[name]=node
    return result


def literal_path(expr,assign,seen=None):
    if isinstance(expr,ast.Constant) and type(expr.value) is str:return expr.value
    if isinstance(expr,ast.Name):
        seen=set() if seen is None else set(seen)
        if expr.id in seen:raise ValueError('cyclic Source path declaration')
        seen.add(expr.id);return literal_path(assign[expr.id].value,assign,seen)
    if isinstance(expr,ast.Call) and isinstance(expr.func,ast.Name) and expr.func.id=='Path' and len(expr.args)==1 and not expr.keywords:return Path(literal_path(expr.args[0],assign,seen))
    if isinstance(expr,ast.BinOp) and isinstance(expr.op,ast.Div):return Path(literal_path(expr.left,assign,seen))/literal_path(expr.right,assign,seen)
    raise ValueError('Source directory value is not the original literal Path composition')


def statement(text,node):
    lines=text.splitlines(keepends=True)
    return ''.join(lines[node.lineno-1:node.end_lineno])


def inverse_role(role,oldpath,newpath):
    old,ot=source(oldpath);new,nt=source(newpath);oa=assignments(ot);na=assignments(nt)
    need(set(oa)==set(na),'all global Source assignments retained '+role)
    changed={name for name in oa if ast.dump(oa[name],include_attributes=False)!=ast.dump(na[name],include_attributes=False)}
    need(changed==ALLOWED[role],'only exact directory/SHA global changes '+role)
    rows=[];recovered=new
    for name in sorted(changed,key=lambda n:na[n].lineno,reverse=True):
        before=statement(old,oa[name]);after=statement(new,na[name])
        need(recovered.count(after)==1 and old.count(before)==1,'unique finite literal Source replacement '+role+' '+name)
        recovered=recovered.replace(after,before,1)
        rows.append(dict(global_name=name,old_statement=before,new_statement=after,whole_single_statement_inverse=True))
        if name!='FUTURE_V25_CANONICAL_SHA':
            op=Path(literal_path(oa[name].value,oa));np=Path(literal_path(na[name].value,na))
            need(op.is_absolute() and np.is_absolute() and op!=np and '..' not in np.parts,'exact original/new absolute Source path '+role+' '+name)
            need('v25_monitor_access' in np.name or 'v25-monitor-access' in np.name,'exact new isolated family basename '+role+' '+name)
    need(recovered==old,'complete byte inverse to frozen original '+role)
    need(ast.dump(ast.parse(recovered),include_attributes=False)==ast.dump(ot,include_attributes=False),'complete all-node AST inverse '+role)
    olddefs=[n for n in ot.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))];newdefs=[n for n in nt.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
    need(len(olddefs)==len(newdefs) and all(ast.dump(x,include_attributes=False)==ast.dump(y,include_attributes=False) and statement(old,x)==statement(new,y) for x,y in zip(olddefs,newdefs)),'all entire function/class bodies byte-exact '+role)
    return dict(original=pin(oldpath),derived=pin(newpath),exact_finite_source_changes=rows,whole_byte_inverse=True,whole_AST_inverse=True,all_function_and_class_bodies_byte_exact=True,definition_count=len(olddefs)),na


def manifest_scope(path):
    root=Path(path).parent;m=meta(path);members=m.get('members',m.get('complete_members'))
    need(type(members) is dict and bool(members),'complete actual Source manifest members')
    files={};dirs={'.':identity(root)}
    for folder,subdirs,names in os.walk(root,followlinks=False):
        for name in subdirs:
            p=Path(folder)/name;need(not p.is_symlink() and p.is_dir(),'ordinary sealed Source directory');dirs[str(p.relative_to(root))]=identity(p)
        for name in names:
            p=Path(folder)/name;files[str(p.relative_to(root))]=pin(p)
    need(set(files)==set(members)|{Path(path).name},'complete Source package no omission or append')
    for rel,row in members.items():need(row['path']==str(root/rel) and fullpin(row,'actual Source manifest member')==files[rel],'all complete declared Source member fullpins '+rel)
    if 'directories' in m:need(dirs==m['directories'],'complete Source manifest directory7IDs')
    if 'member_count' in m:need(type(m['member_count']) is int and m['member_count']==len(members),'exact complete Source member count')
    return m


def closed(doc,label):
    need(doc['closed'] is True,label+' true closed wrapper')
    keys=[key for key in ('terminal_tool_return','actual_tool_return','exec_command_result') if key in doc]
    need(len(keys)==1,label+' one actual tool return')
    tr=doc[keys[0]]
    need(type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr,label+' genuine integer EXIT0')
    return tr


def review(args):
    output=Path(args.output);need(output.is_relative_to(Path('/private/tmp')) and not os.path.lexists(output),'fresh finite independent Source review output')
    cp=pin(args.inputs);need(cp['sha256']==args.inputs_sha256,'Root actual closed Source input contract whole SHA')
    inputs=meta(args.inputs)
    need(inputs['schema']=='ROOT_V25_MONITOR_ACCESS_ACTUAL_DIRECTORY_SOURCE_REVIEW_INPUTS_V1' and inputs['status']=='ACTUAL_SOURCE_DERIVATION_CLOSED_ONLY_NO_BUSINESS_EXECUTION','actual finite Source proof inputs not unknown business success')
    mp=fullpin(inputs['actual_derived_Source_manifest_pin'],'actual derived complete Source manifest')
    ip=fullpin(inputs['actual_derived_Source_inverse_pin'],'actual Root full byte inverse')
    package=manifest_scope(mp['path']);actual_inverse=meta(ip['path'])
    need(package['schema']=='ROOT_V25_COMPLETE_PREP_NAMESPACE_ONLY_SOURCE_MANIFEST_V1' and package['status']=='SOURCE_ONLY_NAMESPACE_ISOLATION_REQUIRES_INDEPENDENT_REVIEW' and package['source_only'] is True and type(package['complete_members_count']) is int and package['complete_members_count']==16 and type(package['full_files_count_including_manifest']) is int and package['full_files_count_including_manifest']==17 and set(package['directories'])=={'.','original_parents'},'exact complete17 Source files and one child directory scope')
    author=meta(fullpin(inputs['actual_Source_author_tool_return_pin'],'actual Source author receipt')['path']);authortr=closed(author,'actual Source directory derivation');authorstdout=json.loads(authortr['output'])
    need(authorstdout['inverse']==ip and authorstdout['canonical']==package['canonical_pin'] and authorstdout['source_only'] is True,'actual closed author stdout exact inverse and canonical pins')
    sourceseal=meta(fullpin(inputs['actual_Source_seal_tool_return_pin'],'actual Root Source genuine seal')['path']);sealtr=closed(sourceseal,'actual sealed Root directory Source');sealstdout=json.loads(sealtr['output'])
    need(sealstdout['manifest']==mp and type(sealstdout['source_files']) is int and sealstdout['source_files']==17 and type(sealstdout['source_subdirectories']) is int and sealstdout['source_subdirectories']==1 and sealstdout['source_only'] is True,'actual Root seal stdout coupled exact full Source manifest')
    pp=fullpin(inputs['prior_complete_bound_Source_peer_report_pin'],'prior complete original Source peer');need(pp['sha256']==PRIOR_PEER_SHA,'same original complete bound41 Source peer')
    peer=meta(pp['path'])
    need(peer['schema']=='INDEPENDENT_V25_ACTUAL_BOUND_COMPLETE_PREP_SOURCE_REVIEW_V1' and peer['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_BUSINESS_QUALIFICATION' and peer['source_only'] is True and peer['all_checks_typed_true'] is True and peer['blockers']==[] and type(peer['check_count']) is int and peer['check_count']==len(peer['checks'])==41 and all(type(row['passed']) is bool and row['passed'] is True for row in peer['checks']),'original complete bound41 Source proofs reused without business credit')
    prior_manifest=fullpin(inputs['prior_complete_bound_Source_peer_manifest_pin'],'prior Source peer complete manifest');manifest_scope(prior_manifest['path'])
    priorseal=meta(fullpin(inputs['prior_complete_bound_Source_peer_seal_pin'],'prior Source peer genuine seal')['path']);tr=closed(priorseal,'original bound Source peer seal');stdout=json.loads(tr['output'])
    need(stdout['review_pin']==pp and stdout['manifest_pin']==prior_manifest,'true prior sealed Source peer scope coupled')
    actualroles=inputs['actual_derived_role_Source_pins'];need(set(actualroles)==set(ORIGINALS),'all four actual complete derived Source roles')
    proof={};trees={}
    for role,old in ORIGINALS.items():
        np=fullpin(actualroles[role],'actual derived '+role)
        need(Path(np['path']).parent==Path(mp['path']).parent,'all actual derived roles inside full sealed Source package')
        proof[role],trees[role]=inverse_role(role,old,Path(np['path']))
        rr=actual_inverse['roles'][role]
        need(fullpin(rr['original'],'Root inverse original complete '+role)==proof[role]['original'] and fullpin(rr['derived'],'Root inverse derived complete '+role)==np,'Root actual inverse original/derived fullpins match independent '+role)
        copy=fullpin(rr['full_original_copy'],'complete original preserved Source copy '+role)
        need(copy['sha256']==proof[role]['original']['sha256'] and copy['size_bytes']==proof[role]['original']['size_bytes'],'complete original Source copy no truncation '+role)
        recovered=Path(np['path']).read_text();original=Path(old).read_text()
        for row in reversed(rr['finite_replacements']):
            need(type(row['count']) is int and row['count']==1 and recovered.count(row['new'])==1,'Root finite inverse replacement unique '+role)
            recovered=recovered.replace(row['new'],row['old'],1)
        need(recovered==original,'Root declared entire inverse independently reconstructed '+role)
    need(proof['canonical']['original']['sha256']==OLD_CANONICAL_SHA,'complete old786 installed canonical unchanged')
    new_sha=proof['canonical']['derived']['sha256']
    for role in ('prepare_host','prepare_writer'):need(ast.literal_eval(trees[role]['FUTURE_V25_CANONICAL_SHA'].value)==new_sha,'only derived canonical Source hash changed '+role)
    ca,ha,wa,pa=(trees[k] for k in ('canonical','prepare_host','prepare_writer','prelaunch'))
    path_of=lambda values,name: str(Path(literal_path(values[name].value,values)))
    for label,refs in [('C',[(ca,'FORMAL_FACTORY'),(ha,'TARGET'),(wa,'FACTORY'),(pa,'C')]),('S',[(ca,'SOURCE'),(ha,'SOURCE'),(wa,'S'),(pa,'S')]),('O',[(ca,'OUT'),(ha,'OUT'),(wa,'O'),(pa,'O')]),('T',[(ca,'TERMINAL'),(ha,'TERMINAL'),(wa,'T'),(pa,'T')]),('H',[(ha,'HOST'),(wa,'H'),(pa,'H')]),('D',[(ha,'SOURCE_ARCHIVE'),(wa,'D'),(pa,'D')]),('E',[(wa,'E'),(pa,'E')])]:
        values=[path_of(x,n) for x,n in refs];need(len(set(values))==1,'all derived literal '+label+' paths consistent')
    need(ast.literal_eval(ca['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA'].value)==Q_SHA and ast.literal_eval(ha['FUTURE_V25_ACTUAL_Q_SHA'].value)==Q_SHA,'actual helper Q c6 is unchanged')
    need(HELPER_SHA in Path(actualroles['canonical']['path']).read_text(),'same actual helper3b Source pin retained')
    for name in FUTURE_BUSINESS:need(isinstance(ca[name].value,ast.Constant) and ca[name].value.value is None,'all future business pins still None '+name)
    need(ast.literal_eval(ca['PREFIX'].value)=='AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V25' and ast.literal_eval(ca['FAMILY'].value)=='SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V25','original V25 schemas and stage family unchanged')
    need(actual_inverse['source_only'] is True and actual_inverse['source_namespace_only_change'] is True and actual_inverse['actual_Q_sha256']==Q_SHA and actual_inverse['actual_helper_sha256']==HELPER_SHA and actual_inverse['candidate_import_API_compile_numeric_or_PREP_executed'] is False,'Root finite Source inverse scope no business execution')
    for key in ('actual_new_PREP_terminal','actual_new_PREP_saved_peer','actual_new_BUILD_terminal'):need(actual_inverse[key] is None and package[key] is None,'all future actual execution pins unknown '+key)
    root=Path(mp['path']).parent
    it,itree=source(root/'Root_complete_SOURCE_install_writer.py');iot,iotree=source(root/'original_parents/Root_complete_SOURCE_install_writer.py')
    defs=[n for n in itree.body if isinstance(n,ast.FunctionDef)];olddefs=[n for n in iotree.body if isinstance(n,ast.FunctionDef)]
    need(len(defs)==len(olddefs)==8 and all(statement(it,n)==statement(iot,o) and ast.dump(n,include_attributes=False)==ast.dump(o,include_attributes=False) for n,o in zip(defs,olddefs)),'installer all8 original full functions byte and AST unchanged')
    need({a.name for n in itree.body if isinstance(n,ast.Import) for a in n.names}=={'argparse','hashlib','json','os','stat','sys'} and all(n.module=='pathlib' for n in itree.body if isinstance(n,ast.ImportFrom)),'new installer imports only original stdlib')
    need(not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('exec','eval','compile','__import__') for n in ast.walk(itree)) and not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('Popen','run','execute','exec_module','load_module') for n in ast.walk(itree)),'installer no candidate imports compilers helper/native/numeric execution')
    expected_installer_clauses=["copied['whole_previous_frozen_Source']=copy_tree(PARENT_D,D)","before_parent['files']==ancestor_freeze['complete_files']","before_parent['directories']=={'.':ancestor_freeze['source_root_identity'],**ancestor_freeze['complete_directories']}","(D/name).rename(original_top/name)","copied['finite_namespace_Source']=copy_tree(N,D/'sealed_namespace_only_complete_PREP_Source')","copied['finite_namespace_Source_peer']=copy_tree(peer_root,D/'sealed_independent_namespace_only_complete_PREP_Source_review')","assert inventory(PARENT_D)==before_parent","assert pin(PARENT_C)==ancestor_freeze['canonical_factory']","assert inventory(N)==source_inventory and inventory(peer_root)==peer_inventory","assert pin(Path(qp['path']))==qp and pin(Path(hp['path']))==hp","metadata_writer_and_prelaunch_included_before_freeze=True","no_SOURCE_append_after_freeze=True","original_whole_seconds=1800,original_stage_seconds=600,original_RSS_mib=512","original_joint_archive_bytes=2*2**30,original_history_bytes=96*2**30,original_free_floor_bytes=8*2**30","original_threads=1,original_children=1,original_retries=0","assert inventory(D)==frozen","assert total<2*2**30"]
    for clause in expected_installer_clauses:need(clause in it,'complete Source installer invariants '+clause)
    rename_stmt=next(n for n in itree.body if isinstance(n,ast.For) and any(isinstance(c,ast.Call) and isinstance(c.func,ast.Attribute) and c.func.attr=='rename' for c in ast.walk(n)))
    need(ast.literal_eval(rename_stmt.iter)==('combined_prepare_host.py','write_actual_prepare_terminal.py','Root_complete_SOURCE_install_writer.py','Root_complete_PREP_prelaunch.py','Root_actual_complete_SOURCE_install_record.json'),'new clone preserves original complete five top Sources in dedicated subdirectory')
    freeze_index=it.index("frozen=inventory(D)")
    need(all(it.index(clause)<freeze_index for clause in ("copied['finite_namespace_Source']=copy_tree", "copied['finite_namespace_Source_peer']=copy_tree", "copied['canonical']=copy_file", "write(D/'Root_actual_complete_SOURCE_install_record.json'")),'complete Source copies and all records before final freeze')
    need(not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('unlink','rmdir','remove','rmtree') for n in ast.walk(itree)),'installer deletes no original or new Source file')
    ss,st=source(root/'Root_complete_PREP_E_snapshot.py');osrc,ost=source(root/'original_parents/Root_complete_PREP_E_snapshot.py')
    olde='actual_complete_combined_prepare_v25_receipts';newe='actual_complete_combined_prepare_v25_monitor_access_receipts'
    need(ss.count(newe)==1 and ss.replace(newe,olde,1)==osrc,'complete E snapshot Source exact one-path inverse')
    need(len([n for n in st.body if isinstance(n,ast.FunctionDef)])==3 and all(statement(ss,n)==statement(osrc,o) for n,o in zip([n for n in st.body if isinstance(n,ast.FunctionDef)],[n for n in ost.body if isinstance(n,ast.FunctionDef)])),'all3 complete original snapshot function bodies unchanged')
    for clause in ('second==ns and secondroot==rootid','assert namespace()==(ns,rootid)','all_current_E_files_full_EOF_SHA_size_exact_seven_int_ID_verified=True','E_root_is_not_claimed_unchanged_after_genuine_future_appends=True','whole_INPUT_build_native_or_science_credit=False'):need(clause in ss,'complete E snapshot Source invariant '+clause)
    for name in ('spot_derive_v25_monitor_access_complete_PREP_Source_ROOT.py','spot_prepare_namespace_complete_Source_install_utilities_ROOT.py'):
        _,at=source(root/name)
        need(not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('exec','eval','compile','__import__') for n in ast.walk(at)) and not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('Popen','run','execute','exec_module','load_module') for n in ast.walk(at)),'whole author Source no candidate helper compile/numeric invocation '+name)
    # Root inverse is an actual pinned Source artifact. Independent complete
    # reverse transforms above, rather than trusting its success label, prove
    # all logic and the complete340 owner/proof definitions are unchanged.
    for role in proof:need(proof[role]['whole_byte_inverse'] is True and proof[role]['whole_AST_inverse'] is True,'all four full logic/body/schema/caps/monitor/MRO invariants via inverse '+role)
    for p,v in dict(PINS).items():need(pin(p)==v,'final all Source META full EOF SHA7ID unchanged '+p)
    report=dict(schema='INDEPENDENT_V25_ACTUAL_BOUND_COMPLETE_PREP_SOURCE_REVIEW_V1',status='SOURCE_ONLY_PASS_NO_EXECUTION_OR_BUSINESS_QUALIFICATION',qualification_scope='DIRECTORY_ISOLATION_SOURCE_ONLY_COMPLETE_BYTE_INVERSE_TO_PRIOR_BOUND41',source_only=True,all_checks_typed_true=True,check_count=len(CHECKS),checks=CHECKS,blockers=[],qualified_bound_manifest_pin=mp,qualified_role_Source_pins={k:actualroles[k] for k in ('canonical','prepare_host','prepare_writer')},qualified_prelaunch_Source_pin=actualroles['prelaunch'],qualified_Source_installer_pin=pin_from_cache(root/'Root_complete_SOURCE_install_writer.py'),qualified_E_snapshot_Source_pin=pin_from_cache(root/'Root_complete_PREP_E_snapshot.py'),prior_complete_bound41_Source_peer_report_pin=pp,prior_complete_bound41_Source_peer_manifest_pin=prior_manifest,prior_complete_bound41_Source_peer_seal_pin=inputs['prior_complete_bound_Source_peer_seal_pin'],actual_Root_Source_inverse_pin=ip,independent_complete_source_inverses=proof,complete_unique_Source_META_file_count=len(PINS),complete_full_EOF_Source_META_pins=list(PINS.values()),candidate_helper_guard_API_compiler_native_or_numeric_executed=False,source_monitor_caps_MRO_physics_thresholds_and340_owners_unchanged=True,actual_NEW_PREP_terminal=None,actual_NEW_PREP_summary=None,actual_NEW_metadatawriter_terminal=None,actual_NEW_BUILD_terminal=None,new_business_or_science_qualification_created=False,whole_build_qualified=False,whole_INPUT_admitted=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,physical_balance_qualified=False,goal_complete=False)
    output.mkdir()
    with (output/'REVIEW.json').open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
    with (output/'INDEPENDENT_COMPLETE_DIRECTORY_BYTE_INVERSES.json').open('x') as f:json.dump(proof,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(source_only=True,status=report['status'],qualification_scope=report['qualification_scope'],check_count=report['check_count'],all_checks_typed_true=True,review=str(output/'REVIEW.json'),qualified_bound_manifest_pin=mp,qualified_role_Source_pins=report['qualified_role_Source_pins'],all_future_NEW_PREP_BUILD_native_science_unknown=True),allow_nan=False))


def main():
    a=argparse.ArgumentParser();a.add_argument('--inputs',required=True);a.add_argument('--inputs-sha256',required=True);a.add_argument('--output',required=True);args=a.parse_args()
    if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or sys.getprofile() is not None:raise ValueError('original nonoptimized unprofiled independent Source reviewer')
    review(args)


if __name__=='__main__':main()
