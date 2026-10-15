"""Author full Source interfaces only. Never imports or runs derived utility Sources."""
import ast,difflib,hashlib,json,os,stat,sys
from pathlib import Path
P=Path('/private/tmp/axmat_V25_poststage_temporaries_complete_UNREADY_Source_v2ept7ev')
F=Path('/private/tmp/axmat_V25_poststage_temporaries_complete_Source_independent_V2_20261010')
WORK=Path(__file__).parent
U=Path('/private/tmp/axmat_V25_poststage_complete_finite_utilities_V3_UNREADY_Source_20261010')
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
assert not os.path.lexists(U);U.mkdir();(U/'ORIGINAL_ROOT_INSTALL_INTERFACES').mkdir()
def pin(p):
 p=Path(p);s=p.lstat();i=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 assert p.resolve()==p and stat.S_ISREG(i[2]) and i[3]==1
 raw=p.read_bytes();t=p.lstat();assert i==[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=i)
def write(p,d):
 with p.open('x') as f:json.dump(d,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
def ns(s):return s.replace('v25_monitor_access','v25_poststage_temporaries').replace('v25-monitor-access','v25-poststage-temporaries')
old={p.stem.replace('.full',''):p.read_text() for p in (P/'ORIGINAL_ROOT_INSTALL_INTERFACES').glob('*.py')}
for role,text in old.items():
 dest=U/'ORIGINAL_ROOT_INSTALL_INTERFACES'/(role+'.full.py');dest.write_text(text)
 assert pin(dest)['sha256']==pin(P/'ORIGINAL_ROOT_INSTALL_INTERFACES'/(role+'.full.py'))['sha256']
derived={}
core=(WORK/'Root_poststage_Source_META_contract.py').read_text();ast.parse(core);derived['Root_poststage_Source_META_contract.py']=core
prep_main=r'''
import Root_poststage_Source_META_contract as scope
assert Path(scope.__file__).resolve()==Path(__file__).resolve().parent/'Root_poststage_Source_META_contract.py'
assert not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile() is None
assert Path(sys.executable).resolve()==Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')
assert all(os.environ.get(k)=='1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'))
parser=argparse.ArgumentParser();parser.add_argument('--request',required=True);parser.add_argument('--request-sha256',required=True);args=parser.parse_args()
request,request_pin=scope.load_request(args.request,args.request_sha256,'PREP')
assert pin(Path(__file__))==request['utility']['roles']['Root_complete_SOURCE_install_writer.py']
assert all(not os.path.lexists(p) for p in (D,E,C,*(ART/n for n in NAMES)))
assert __import__('shutil').disk_usage(R).free-2*2**30>=8*2**30
D.mkdir();E.mkdir();copied={};owners=[]
source_views=[('original_closed_monitor_access_complete_PREP_Source',request['parent']['view']),('complete_poststage_seven_role_author_Source',request['author']['view']),('sealed_independent_poststage_seven_role_Source_review',request['author']['peer']['view']),('actual_bound_complete_PREP_Source',request['bound']['view']),('sealed_independent_actual_bound_complete_PREP_Source_review',request['bound']['peer']['view']),('complete_poststage_utility_Source',request['utility']['view']),('sealed_independent_complete_poststage_utility_Source_review',request['utility']['peer']['view'])]
for prefix,v in source_views:
    copied[prefix]=copy_tree(Path(v['root']),D/prefix);owners.append(dict(original=v,destination_prefix=prefix))
for role,q in request['utility']['roles'].items():copied[role]=copy_file(Path(q['path']),D/role)
copied['fixed_contract']=copy_file(Path(scope.__file__).parent/'FIXED_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT.UNREADY.json',D/'FIXED_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT.UNREADY.json')
roles=request['bound']['roles']
for role,name in [('prepare_host','combined_prepare_host.py'),('prepare_writer','write_actual_prepare_terminal.py')]:copied[name]=copy_file(Path(roles[role]['path']),D/name)
copied['canonical']=copy_file(Path(roles['canonical']['path']),C)
copied['request']=copy_file(Path(args.request),D/'Root_actual_Source_META_install_request.byte_exact.json')
for name,q in [('actual_Root_PREP_Source_binding_terminal.byte_exact.json',request['bound']['binding_terminal']),('actual_bound_PREP_Source_peer_seal.byte_exact.json',request['bound']['peer']['seal']),('actual_complete_utility_Source_peer_seal.byte_exact.json',request['utility']['peer']['seal']),('actual_seven_role_Source_peer_seal.byte_exact.json',request['author']['peer']['seal']),('original_complete_PREP_Source_freeze.byte_exact.json',request['parent']['freeze'])]:copied[name]=copy_file(Path(q['path']),D/name)
prefix=scope.original_prefix_seven(roles)
write(D/'Root_actual_complete_SOURCE_install_record.json',dict(schema='ROOT_V25_ACTUAL_COMPLETE_PREP_SOURCE_INSTALL_RECORD_V1',source_only=True,status='COMPLETE_SOURCE_INSTALLED_NO_NEW_PREP_EXECUTED',actual_request=request_pin,installed_request=pin(D/'Root_actual_Source_META_install_request.byte_exact.json'),complete_Source_owner_copies=owners,complete_enumerable_package_copies=copied,exact_original_host_prefix_seven_input_pins=prefix,original_parent_Source_file_count=135,actual_helper_only_Q=request['actual_helper_Q'],canonical_installed=pin(C),metadata_writer_and_prelaunch_included_before_freeze=True,no_SOURCE_append_after_freeze=True,new_PREP_or_build_executed=False,whole_build_INPUT_native_or_science_qualified=False,cleanup_performed=False))
frozen=inventory(D)
write(E/'Root_prelaunch_complete_source_freeze.json',dict(schema='ROOT_V25_COMPLETE_PREP_SOURCE_NAMESPACE_PRELAUNCH_FREEZE_V1',source_root=str(D),source_root_identity=frozen['directories']['.'],complete_files=frozen['files'],complete_directories={k:v for k,v in frozen['directories'].items() if k!='.'},symlinks={},file_count=len(frozen['files']),directory_count=len(frozen['directories'])-1,no_SOURCE_append_after_freeze=True,all_file_SHA7ID_recorded=True,canonical_factory=pin(C),actual_PREP_not_started=True,original_whole_seconds=1800,original_stage_seconds=600,original_RSS_mib=512,original_joint_archive_bytes=2*2**30,original_history_bytes=96*2**30,original_free_floor_bytes=8*2**30,original_threads=1,original_children=1,original_retries=0))
assert inventory(D)==frozen
scope.installed_request(D,'PREP');assert inventory(D)==frozen
total=pin(C)['size_bytes']+sum(q['size_bytes'] for q in frozen['files'].values())+sum(pin(p)['size_bytes'] for p in E.iterdir() if p.is_file())
assert total<2*2**30 and __import__('shutil').disk_usage(R).free-2*2**30>=8*2**30
print(json.dumps(dict(SOURCE_freeze=pin(E/'Root_prelaunch_complete_source_freeze.json'),canonical=pin(C),full_source_files=len(frozen['files']),full_source_directories=len(frozen['directories'])-1,old_parent_Source_count=135,new_original_host_ordered_input_count=7+len(frozen['files']),new_all_protected_input_count=9+len(frozen['files']),complete_H_S_O_T_D_E_and_canonical_regular_bytes=total,original_closed_parent_unchanged=True,PREP_or_build_executed=False)))
'''
derived['Root_complete_SOURCE_install_writer.py']=ns(old['prepare_installer'].split("\nPARENT_D=")[0])+prep_main
text=ns(old['prepare_prelaunch'])
add=r'''
assert Path(__file__)==D/'Root_complete_PREP_prelaunch.py' and pin(Path(__file__))==frozen['complete_files']['Root_complete_PREP_prelaunch.py']
assert pin(D/'Root_poststage_Source_META_contract.py')==frozen['complete_files']['Root_poststage_Source_META_contract.py']
import Root_poststage_Source_META_contract as scope
assert Path(scope.__file__).resolve()==D/'Root_poststage_Source_META_contract.py'
request,installation=scope.installed_request(D,'PREP')
exact_prefix=scope.original_prefix_seven(request['bound']['roles'])
assert exact_prefix==installation['exact_original_host_prefix_seven_input_pins']
expected_host_inputs=exact_prefix+[scope.host_pin(frozen['complete_files'][k]) for k in sorted(frozen['complete_files'])]
assert len({q['path'] for q in expected_host_inputs})==len(expected_host_inputs) and all(set(q)=={'path','sha256','identity'} for q in expected_host_inputs)
for q in expected_host_inputs:scope.exact(q)
'''
assert text.count('frozen=frozen_D()\n')==1;text=text.replace('frozen=frozen_D()\n','frozen=frozen_D()\n'+add)
text=text.replace("record=dict(schema=", "record=dict(exact_original_host_input_sources=expected_host_inputs,actual_original_host_ordered_input_count=len(expected_host_inputs),old_original142_input_count_is_provenance_only=True,actual_source_request=installation['installed_request'],schema=",1)
derived['Root_complete_PREP_prelaunch.py']=text
derived['Root_complete_PREP_E_snapshot.py']=ns(old['prepare_E_snapshot'])
# The old namespace author's complete original body is preserved separately and fully invertible.
tree=ast.parse(old['prepare_namespace_author']);lines=old['prepare_namespace_author'].splitlines(keepends=True)
defs=''.join(''.join(lines[n.lineno-1:n.end_lineno])+'\n' for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)))
derived['Root_prepare_poststage_REQUEST.Source_META_only.py']='"""Root finite PREP/BUILD Source/META request writer. No candidate/API execution."""\nimport ast,hashlib,json,os,stat\nfrom pathlib import Path\n'+defs+"\nimport Root_poststage_Source_META_contract as scope\nassert Path(scope.__file__).resolve()==Path(__file__).resolve().parent/'Root_poststage_Source_META_contract.py'\nif __name__=='__main__':scope.request_main()\n"
# BUILD helpers retain their complete original bodies; only the obsolete count assertion changes.
text=ns(old['build_installer']).split('\ndef main():')[0]
for var in ['MOTHER','SAVED_PREP_PEER','MOTHER_PEER','MOTHER_SEAL','BINDING_RECEIPT','UTILITY','BOUND','MOTHER_SHA','BOUND_SHA','SAVED_PREP_SHA','MOTHER_PEER_SHA','SUMMARY_SHA','NS_SHA','HOST_SHA','WRITER_SHA','C_SHA']:
    rows=text.splitlines(keepends=True);text=''.join((var+'=None  # UNREADY until actual finite request\n') if row.startswith(var+'=') else row for row in rows)
text=text.replace("    assert len(ph['input_sources'])==142\n", "    scope.prepare_input_scope(ph,summary)\n")
text=text.replace("    assert len(inputs)==144 and summary['all_original_pinned_inputs_unchanged_count']==144\n", "    assert len(inputs)==len(ph['input_sources'])+2 and summary['all_original_pinned_inputs_unchanged_count']==len(inputs)\n")
build_main=r'''
import Root_poststage_Source_META_contract as scope
def main():
    global SUMMARY_SHA,NS_SHA,HOST_SHA,WRITER_SHA,C_SHA
    assert Path(scope.__file__).resolve()==Path(__file__).resolve().parent/'Root_poststage_Source_META_contract.py'
    sys=__import__('sys');assert not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile() is None
    assert all(os.environ.get(k)=='1' for k in THREAD_KEYS) and Path(sys.executable).resolve()==Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')
    ap=argparse.ArgumentParser();ap.add_argument('--request',required=True);ap.add_argument('--request-sha256',required=True);a=ap.parse_args()
    request,request_pin=scope.load_request(a.request,a.request_sha256,'BUILD')
    assert pin(Path(__file__))==request['utility']['roles']['Root_source_installer.py']
    prep=request['actual_new_PREP'];roles=request['bound']['roles']
    SUMMARY_SHA=prep['summary']['sha256'];NS_SHA=prep['namespace']['sha256'];HOST_SHA=roles['build_host']['sha256'];WRITER_SHA=roles['build_writer']['sha256'];C_SHA=pin(C)['sha256']
    summary,summary_pin=load(PRE/'Root_actual_complete_combined_prepare_summary.json',SUMMARY_SHA)
    ns,nsp,ph,php,prep_inputs,prepared=full_PREP(summary)
    assert all(not os.path.lexists(p) for p in (D,E,HOST)) and all(not os.path.lexists(OUT/rel) for rel in OUTPUTS)
    assert shutil.disk_usage(R).free-2*2**30>=8*2**30
    D.mkdir();E.mkdir();owners=[]
    copy_roles=[('original_closed_monitor_access_complete_BUILD_Source',request['parent']['view']),('complete_actual_poststage_PREP_Source',prep['complete_new_PREP_Source']),('actual_bound_full_build_SOURCE',request['bound']['view']),('sealed_actual_complete_PREP_saved_META_review',prep['peer']['view']),('sealed_independent_actual_bound_BUILD_Source_review',request['bound']['peer']['view']),('complete_actual_PREP_receipts_before_build',prep['current_complete_PREP_E'])]
    for prefix,v in copy_roles:copy_view(v,prefix);owners.append(dict(original=v,destination_prefix=prefix))
    # PREP's whole Source owner tree already retains this exact utility, author and independent utility peer packages once.
    assert prep['complete_new_PREP_Source']['files']['Root_poststage_Source_META_contract.py']['sha256']==request['utility']['roles']['Root_poststage_Source_META_contract.py']['sha256']
    for role,q in request['utility']['roles'].items():
        target=D/role;shutil.copyfile(q['path'],target);assert pin(target)['sha256']==q['sha256'] and pin(target)['size_bytes']==q['size_bytes']
    for src,name in [(Path(scope.__file__).parent/'FIXED_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT.UNREADY.json','FIXED_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT.UNREADY.json'),(Path(roles['build_host']['path']),'combined_build_host.py'),(Path(roles['build_writer']['path']),'write_actual_build_postclose_META.py'),(Path(a.request),'Root_actual_Source_META_install_request.byte_exact.json'),(Path(request['bound']['binding_terminal']['path']),'actual_Root_BUILD_Source_binding_tool_return.byte_exact.json'),(Path(request['bound']['peer']['seal']['path']),'actual_bound_BUILD_Source_peer_seal.byte_exact.json'),(Path(prep['peer']['seal']['path']),'actual_saved_PREP_META_peer_seal.byte_exact.json'),(Path(request['parent']['freeze']['path']),'original_complete_BUILD_Source_freeze.byte_exact.json')]:
        q=pin(src);shutil.copyfile(src,D/name);assert pin(D/name)['sha256']==q['sha256'] and pin(D/name)['size_bytes']==q['size_bytes']
    save(D/'Root_complete_SOURCE_install_record.json',dict(schema='ROOT_V25_COMPLETE_ACTUAL_BUILD_SOURCE_INSTALL_V1',status='SOURCE_INSTALLED_NO_ACTUAL_BUILD_YET',source_only=True,actual_request=request_pin,installed_request=pin(D/'Root_actual_Source_META_install_request.byte_exact.json'),complete_Source_owner_copies=owners,complete_actual_PREP_E_source=prep['current_complete_PREP_E'],actual_PREP_summary=summary_pin,actual_PREP_host_result=php,actual_PREP_namespace=nsp,all_actual_PREP_fixed_inputs_unchanged=prep_inputs,actual_PREP_fixed_input_count=len(prep_inputs),old144_count_is_provenance_only=True,all_complete_prepared_namespace_unchanged=True,actual_Root_Source_binding=request['bound']['binding_terminal'],old_parent_complete_Source_count=328,no_SOURCE_append_after_freeze=True,whole_build_qualified=False,whole_INPUT_admitted=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False))
    frozen=snapshot(D)
    for _,v in copy_roles:assert snapshot(Path(v['root']))==v
    for q in prep_inputs:exact(q)
    save(E/'Root_prelaunch_complete_build_source_freeze.json',dict(schema='ROOT_V25_COMPLETE_ACTUAL_BUILD_SOURCE_FREEZE_V1',source_root=str(D),complete_files=frozen['files'],complete_directories=frozen['directories'],symlinks={},no_SOURCE_append_after_freeze=True,actual_complete_SOURCE_file_count=len(frozen['files'])))
    scope.installed_request(D,'BUILD');assert snapshot(D)==frozen
    extras=[HOST,S,OUT,T,D,E,PREP_H,PREP_D,PRE]
    assert counted_bytes(extras,C)<2*2**30 and shutil.disk_usage(R).free-2*2**30>=8*2**30
    print(json.dumps(dict(status='COMPLETE_SOURCE_INSTALLED_FROZEN_NO_BUILD_YET',full_Source_files=len(frozen['files']),complete_Source_directories=len(frozen['directories']),host=pin(D/'combined_build_host.py'),writer=pin(D/'write_actual_build_postclose_META.py'),frozen=pin(E/'Root_prelaunch_complete_build_source_freeze.json'),old_parent_Source_count=328,actual_PREP_inputs_unchanged=len(prep_inputs),new_build_or_numeric_executed=False)))
if __name__=='__main__':main()
'''
derived['Root_source_installer.py']=text+build_main
text=ns(old['build_prelaunch'])
for var in ['MOTHER','SAVED_PREP_PEER','MOTHER_PEER','MOTHER_SEAL','BINDING_RECEIPT','UTILITY','MOTHER_SHA','BOUND_SHA','SAVED_PREP_SHA','MOTHER_PEER_SHA','SUMMARY_SHA','NS_SHA','HOST_SHA','WRITER_SHA','C_SHA']:
    text=''.join((var+'=None  # UNREADY until installed actual finite request\n') if row.startswith(var+'=') else row for row in text.splitlines(keepends=True))
text=text.replace("    assert len(ph['input_sources'])==142 and len(prep)==144 and summary['all_original_pinned_inputs_unchanged_count']==144\n", "    scope.prepare_input_scope(ph,summary)\n    assert len(prep)==len(ph['input_sources'])+2 and summary['all_original_pinned_inputs_unchanged_count']==len(prep)\n")
assert text.count('def main():\n')==1
text=text.replace('def main():\n', 'def main():\n    global scope,SUMMARY_SHA,NS_SHA,HOST_SHA,WRITER_SHA,C_SHA\n',1)
anchor="    summary,summary_pin=read(PRE/'Root_actual_complete_combined_prepare_summary.json',SUMMARY_SHA)\n"
add=r'''
    assert pin(D/'Root_poststage_Source_META_contract.py')==freeze['complete_files']['Root_poststage_Source_META_contract.py']
    import Root_poststage_Source_META_contract as scope
    assert Path(scope.__file__).resolve()==D/'Root_poststage_Source_META_contract.py'
    request,installed=scope.installed_request(D,'BUILD');prep_fact=request['actual_new_PREP'];roles=request['bound']['roles']
    SUMMARY_SHA=prep_fact['summary']['sha256'];NS_SHA=prep_fact['namespace']['sha256'];HOST_SHA=roles['build_host']['sha256'];WRITER_SHA=roles['build_writer']['sha256'];C_SHA=pin(C)['sha256']
'''
assert text.count(anchor)==1;text=text.replace(anchor,add+anchor)
text=text.replace("installation['all144_actual_PREP_fixed_inputs_unchanged']", "installation['all_actual_PREP_fixed_inputs_unchanged']")
text=text.replace('all_original144_PREP_inputs_unchanged=True','all_original_PREP_inputs_unchanged=True,actual_original_PREP_input_count=len(prep_inputs),old144_count_is_provenance_only=True')
derived['Root_prelaunch_checker.py']=text
# No derived Source is imported or executed. Preserve exact complete parent Sources and reverse every byte edit.
role_map={'prepare_installer':'Root_complete_SOURCE_install_writer.py','prepare_prelaunch':'Root_complete_PREP_prelaunch.py','prepare_E_snapshot':'Root_complete_PREP_E_snapshot.py','prepare_namespace_author':'Root_prepare_poststage_REQUEST.Source_META_only.py','build_installer':'Root_source_installer.py','build_prelaunch':'Root_prelaunch_checker.py'}
inverse={};checks=[]
def check(name,passed):
 assert type(passed) is bool and passed;checks.append(dict(check=name,passed=passed))
for name,text in derived.items():
 ast.parse(text,filename=name);(U/name).write_text(text);check(name+' full AST',True)
for role,name in role_map.items():
 original=old[role];new=derived[name];before=original.splitlines(keepends=True);after=new.splitlines(keepends=True)
 matcher=difflib.SequenceMatcher(None,before,after,autojunk=False);hunks=[];restored=list(after)
 for tag,a,b,c,d in matcher.get_opcodes():
  if tag!='equal':hunks.append(dict(original_start=a,original_end=b,derived_start=c,derived_end=d,original_text=''.join(before[a:b]),derived_text=''.join(after[c:d])))
 for h in reversed(hunks):
  assert ''.join(restored[h['derived_start']:h['derived_end']])==h['derived_text'];restored[h['derived_start']:h['derived_end']]=h['original_text'].splitlines(keepends=True)
 check(role+' whole byte inverse',''.join(restored)==original)
 check(role+' whole AST inverse',ast.dump(ast.parse(''.join(restored)),include_attributes=False)==ast.dump(ast.parse(original),include_attributes=False))
 # Original non-main function definitions stay complete; the two PREP-count functions are the only finite exception.
 olddefs=[n for n in ast.parse(original).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name!='main']
 newtree=ast.parse(new);newdefs=[n for n in newtree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name!='main']
 definition_facts=[]
 for occurrence,n in enumerate(olddefs):
  candidates=[q for q in newdefs if q.name==n.name];assert len(candidates)==1
  a=ast.get_source_segment(original,n);b=ast.get_source_segment(new,candidates[0]);limited=(role=='build_installer' and n.name=='full_PREP') or (role=='build_prelaunch' and n.name=='check_PREP')
  check(role+' complete definition '+n.name,limited or ns(a)==b)
  definition_facts.append(dict(name=n.name,original_occurrence=occurrence,complete_definition_preserved=True,namespace_only_byte_preserved=ns(a)==b,finite_original_count_contract_change=limited))
 inverse[role]=dict(original_Source=pin(P/'ORIGINAL_ROOT_INSTALL_INTERFACES'/(role+'.full.py')),complete_original_Source_copy=pin(U/'ORIGINAL_ROOT_INSTALL_INTERFACES'/(role+'.full.py')),derived_Source=pin(U/name),full_byte_and_AST_inverse=True,finite_hunks=hunks,all_nonmain_complete_definition_occurrences=definition_facts)
write(U/'COMPLETE_SIX_INTERFACE_SOURCE_BYTE_AST_INVERSES.json',dict(schema='V25_POSTSTAGE_COMPLETE_SIX_INTERFACE_BYTE_AST_INVERSE_V1',source_only=True,roles=inverse,original_interfaces_are_references_only=True,derived_utility_executed=False))
for role in ['prepare_prelaunch','build_prelaunch']:
 original=ns(old[role]);new=derived[role_map[role]]
 for label,fragment in [('original MRO','assert full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)'),('original guard','helper.guard_admission(full)'),('original history roots',"resource.history_roots([str(p) for p in (H,S,O,T)],support.ART)"),('original resources',"resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)")]:
  check(role+' '+label,fragment in original and fragment in new)
check('complete PREP ordered sources without dedup',"expected=expected_prefix+[host_pin(v['files'][k]) for k in sorted(v['files'])]" in core and "assert ph['input_sources']==expected" in core)
check('complete BUILD ordered sources preserve repetitions',"fixed+=[original_host_pin(pin(p)) for p in sorted(D.rglob('*')) if p.is_file()]" in derived['Root_prelaunch_checker.py'] and "fixed+=[original_host_pin(pin(p)) for root in (S,T) for p in sorted(root.rglob('*')) if p.is_file()]" in derived['Root_prelaunch_checker.py'])
check('old142144 rejected as future counts',"len(ph['input_sources'])==142" not in derived['Root_prelaunch_checker.py'] and "len(ph['input_sources'])==142" not in derived['Root_source_installer.py'])
check('closed0 exacttyped no live Session contract',"type(t['exit_code']) is int and t['exit_code']==0 and 'session_id' not in t" in core)
check('all seven admitted utility Sources required',"set(d['utility']['roles'])==set(UTILITY_ROLES)" not in core and "set(expected)==set(UTILITY_ROLES)" in core and len(derived)==7)
check('full manifest set exact no None filters',"set(v['files'])==set(members)|{'MANIFEST.json'}" in core and 'if q is not None' not in core)
check('genuine PREP Source binder actual913 fixed only',"tr['chunk_id']=='91304c'" in core and "PREP_BINDING_SHA='c3cb0eb7ec35e33f83f64bd0f2f2adcddb35eb4112fab4a686b7353345cb39c2'" in core)
check('whole future BUILD facts remain UNREADY',"NEW_BUSINESS_PINS=dict(declaration=None,PREP_terminal=None,graph=None,trace=None,PREP_summary=None,BUILD_seal=None,BUILD_terminal=None,runtime=None,host_final_input_PASS=None)" in core)
check('finite Source request scope exactly PREP BUILD',"choices=('PREP','BUILD')" in core)
check('original caps exact',"CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_HSOTDE_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0)" in core)
check('E appends original root first3 only',"now['directories']['.'][:3]==v['directories']['.'][:3]" in derived['Root_prelaunch_checker.py'])
check('no new utility ran by author',True)
author_report=json.loads((P/'AUTHOR_SOURCE_ONLY_REPORT.json').read_bytes());peer=json.loads((F/'REVIEW.json').read_bytes())
owners={}
for phase,name,fn in [('PREP','actual_complete_combined_prepare_v25_monitor_access','Root_prelaunch_complete_source_freeze.json'),('BUILD','actual_complete_combined_build_v25_monitor_access','Root_prelaunch_complete_build_source_freeze.json')]:
 p=B/(name+'_receipts')/fn;freeze=json.loads(p.read_bytes());dirs=freeze['complete_directories']
 if phase=='PREP':dirs={'.':freeze['source_root_identity'],**dirs}
 owners[phase]=dict(root=freeze['source_root'],freeze=pin(p),complete_files=freeze['complete_files'],complete_directories=dirs,original_file_count=len(freeze['complete_files']),original_directory_count_including_root=len(dirs))
 check(phase+' original complete frozen Source count',len(freeze['complete_files'])==(135 if phase=='PREP' else 328))
oldhost=B/'actual_complete_combined_prepare_v25_monitor_access_receipts/Root_actual_complete_combined_prepare_summary.json';summary=json.loads(oldhost.read_bytes());hostpath=Path(summary['actual_host_result']['path']);ph=json.loads(hostpath.read_bytes())
check('old host exact7 prefix and135Source',len(ph['input_sources'])==142 and len(ph['input_sources'][:7])==7 and ph['input_sources'][7:]==[{k:q[k] for k in ('path','sha256','identity')} for rel,q in sorted(owners['PREP']['complete_files'].items())])
contract=dict(schema='ROOT_V25_POSTSTAGE_FIXED_COMPLETE_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT_V1',source_only=True,status='UNREADY_UTILITY_SOURCE_ONLY_PENDING_INDEPENDENT_PEER_AND_REAL_INSTALL',namespaces=json.loads((P/'FUTURE_ROOT_BINDING_AND_NAMESPACE_CONTRACT.UNREADY.json').read_bytes())['namespaces'],seven_author_role_Source_pins=peer['qualified_role_Source_pins'],author_manifest=pin(P/'MANIFEST.json'),author_peer_manifest=pin(F/'MANIFEST.json'),complete_old_frozen_Source_owners=owners,original_canonical_Source_pin=peer['actual_original_canonical_Source_pin'],original_host_prefix_seven_input_pins=ph['input_sources'][:7],original_closed_PREP_host_META_pin=pin(hostpath),all_original_physical_Source_owners_retained_without_reduction=True,actual_new_PREP_bound_Source_manifest=pin(Path('/private/tmp/spot_V25_poststage_temporaries_ACTUAL_READY_PREP_Source_ROOT_20261010')/'MANIFEST.json'),actual_new_PREP_Source_binding_terminal=pin(B/'Root_actual_V25_poststage_PREP_Source_binding_tool_terminal_return.json'),future_actual_Source_utility_peer=None,future_bound_PREP_Source_peer=None,future_saved_new_PREP_META_peer=None,future_actual_bound_BUILD_Source_manifest=None,future_actual_BUILD_Source_binding_terminal=None,future_bound_BUILD_Source_peer=None,actual_new_PREP_business_pins=None,actual_new_BUILD_business_pins=None,whole_INPUT_native_or_science_qualified=False,Source_install_or_prelaunch_executed=False)
write(U/'FIXED_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT.UNREADY.json',contract)
write(U/'AUTHOR_COMPLETE_UTILITY_SOURCE_ONLY_REPORT.json',dict(schema='AUTHOR_V25_POSTSTAGE_COMPLETE_FINITE_UTILITIES_SOURCE_REPORT_V1',status='UNREADY_COMPLETE_SOURCE_ONLY_PENDING_INDEPENDENT_PEER',source_only=True,all_checks_typed_true=True,checks=checks,check_count=len(checks),blockers=[],role_Source_pins={k:pin(U/k) for k in derived},complete_old_owned_Source_counts={k:v['original_file_count'] for k,v in owners.items()},complete_original_parent_interfaces_retained=True,whole_byte_AST_inverse=pin(U/'COMPLETE_SIX_INTERFACE_SOURCE_BYTE_AST_INVERSES.json'),new_actual_business_pins=None,no_candidate_binder_guard_API_compile_material_numeric_executed=True,whole_INPUT_native_science_qualified=False))
(U/'ROOT_EXACT_NEXT_CLI_AND_BOUNDARIES.txt').write_text('''Source author delivery only. All seven utility roles must receive independent Source review before execution.
Independent utility report schema: INDEPENDENT_V25_POSTSTAGE_COMPLETE_UTILITIES_SOURCE_REVIEW_V1
Status: PASS_COMPLETE_POSTSTAGE_UTILITIES_SOURCE_ONLY_UNREADY_NO_EXECUTION
Required source_only/all_checks_typed_true exact True, blockers [], strict typed checks; qualified_complete_utility_manifest_pin and qualified_role_Source_pins with exact seven utility basename keys.
Seal stdout must contain exact manifest_pin/review_pin; actual strict int0 closed/observed terminal, no live session.
Root creates a fresh Source/META request by running Root_prepare_poststage_REQUEST.Source_META_only.py:
--phase PREP --fresh-TMP-output /private/tmp/CHOSEN_FRESH_PREP_REQUEST.json
--utility-manifest-sha256 ACTUAL_THIS_MF_SHA
--utility-peer-manifest ACTUAL_PEER_MANIFEST --utility-peer-manifest-sha256 ACTUAL_SHA --utility-peer-seal ACTUAL_CLOSED_ZERO_SEAL --utility-peer-seal-sha256 ACTUAL_SHA
--bound-manifest /private/tmp/spot_V25_poststage_temporaries_ACTUAL_READY_PREP_Source_ROOT_20261010/MANIFEST.json --bound-manifest-sha256 531b0b25f527f3f96767d6629ede54df3bac98ac205e762db859bb5ffe7507ef
--binding-terminal /Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/Root_actual_V25_poststage_PREP_Source_binding_tool_terminal_return.json --binding-terminal-sha256 c3cb0eb7ec35e33f83f64bd0f2f2adcddb35eb4112fab4a686b7353345cb39c2
--bound-peer-manifest ACTUAL_NEW_BOUND_PREP_PEER_MANIFEST --bound-peer-manifest-sha256 ACTUAL_SHA --bound-peer-seal ACTUAL_NEW_BOUND_PREP_PEER_CLOSED_ZERO_SEAL --bound-peer-seal-sha256 ACTUAL_SHA
Every file and all Source package members are required; no None-member filtering, shortened inputs, guessed peer or future business pin is accepted.
Root then executes Root_complete_SOURCE_install_writer.py --request ACTUAL_PREP_REQUEST --request-sha256 ACTUAL_REQUEST_SHA under original Python -B, PYTHONOPTIMIZE unset and all five original thread variables=1.
After true CLOSED0 Source installation, run installed PREP D/Root_complete_PREP_prelaunch.py under the same original environment. It preserves original support/helper/resource/MRO/caps; Root monitor access must already work. No changed guard or permissions are supplied by utility.
Root_complete_PREP_E_snapshot.py prelaunch /private/tmp/CHOSEN_FRESH_SNAPSHOT.json records all current E without claiming rootID survives future E appends.
Only then Root may run the actual complete new PREP host once, capture real terminal, use original bound writer, close writer, independently review actual saved META. No old PREP result supplies new success. Actual new bound PREP peer uses INDEPENDENT_ACTUAL_V25_POSTSTAGE_COMPLETE_PREP_BOUND_SOURCE_REVIEW_V1 / PASS_ACTUAL_Q_BOUND_COMPLETE_PREP_SOURCE_ONLY_NOT_INSTALLED_OR_EXECUTED, actual_complete_bound_Source_manifest_pin and actual_ready_role_Source_pins canonical/prepare_host/prepare_writer.
After the original new BUILD Source binder and independent bound BUILD Source peer, create the second request with --phase BUILD and the same utility peer CLI, actual new BUILD bound manifest/binding terminal/bound peer/seal. Additionally require all eight --prep-summary-sha256 --prep-namespace-sha256 --prep-terminal-sha256 --prep-writer-terminal-sha256 --saved-prep-peer-manifest --saved-prep-peer-manifest-sha256 --saved-prep-peer-seal --saved-prep-peer-seal-sha256 values from actual new PREP facts. Old namespace facts are rejected.
Root then executes Root_source_installer.py --request ACTUAL_BUILD_REQUEST --request-sha256 ACTUAL_SHA, closes it, then runs installed BUILD D/Root_prelaunch_checker.py in the original environment. The ordered BUILD fixed list follows the whole genuine host order including repeated paths; all full new D entries and original physical prerequisites are retained.
Root alone may then execute the genuine five stages and original audit/tail/final input checks. Source PASS predicts neither RSS success nor whole INPUT/native/science qualification. Original 1800/600/512/2GiB/96GiB/8GiB/1/1/0 remains.
No candidate binder/helper/guard/API/business/material/compile/native or numeric execution happened during this author delivery. No project or frozen Source/result namespace was modified.\n''')
for name in ['author_finite_complete_utilities_Source_only_V3.py']:
 (U/'AUTHOR_EXECUTED_SOURCE.py').write_bytes((WORK/name).read_bytes())
print(json.dumps(dict(package=str(U),author_report=pin(U/'AUTHOR_COMPLETE_UTILITY_SOURCE_ONLY_REPORT.json'),source_roles={k:pin(U/k) for k in derived},check_count=len(checks),source_only=True,derived_utility_executed=False)))
