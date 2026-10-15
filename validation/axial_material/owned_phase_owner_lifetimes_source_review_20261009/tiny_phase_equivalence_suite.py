"""Isolated genuine tiny filesystem phases; no producer/business API or large input."""
from pathlib import Path
import ast,hashlib,json,os,sys,tempfile,weakref,copy
BASE=Path('/private/tmp/axmat-owned-phase-owner-lifetimes-graph-draft-20261009')
PARENT=Path('/Users/wen/spot/validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_same_literal_phase_identity_20261008.py')
CANDIDATE=BASE/'combined_runtime_reviewed_metadata_historical_input_graph_owned_phase_owner_lifetimes_20261009.py'

def selected_namespace(path):
    tree=ast.parse(path.read_bytes())
    permitted=(ast.Import,ast.ImportFrom,ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef,ast.Assign)
    statements=[node for node in tree.body if isinstance(node,permitted)]
    namespace={'__name__':'isolated_tiny_graph_'+path.stem}
    exec(compile(ast.Module(body=statements,type_ignores=[]),str(path),'exec'),namespace)
    return namespace

OLD=selected_namespace(PARENT);NEW=selected_namespace(CANDIDATE)
active=None
opens={}
owned_paths=set()

def audit(event,args):
    if active is not None and event=='open' and isinstance(args[0],str) and args[0] in owned_paths:
        counts=opens.setdefault(active,{})
        counts[args[0]]=counts.get(args[0],0)+1
sys.addaudithook(audit)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def independent_text(value):return value.encode('utf-8').decode('utf-8')
results=[]

with tempfile.TemporaryDirectory(prefix='axmat-owned-phase-lifetimes-tiny-',dir='/private/tmp') as temporary:
    root=Path(temporary);regular=root/'regular';regular.mkdir();(regular/'empty').mkdir()
    a=regular/'α.dat';a.write_bytes(b'alpha\x00\xff')
    b=regular/'b.dat';b.write_bytes(b'beta\x01')
    parent=regular/'parent.json';parent.write_bytes(b'{"signed":-0.0,"value":[1,true,"same"]}')
    extra=root/'new.dat';extra.write_bytes(b'explicit new input')
    link=regular/'link.dat';link.symlink_to(a.name)
    directory_alias=root/'directory_alias';directory_alias.symlink_to(regular.name,target_is_directory=True)
    filemap={str(path):sha(path) for path in (a,b,parent)}
    aliases=OLD['_alias_map'](OLD['capture_aliases']([str(link),str(directory_alias)]))
    aliases[str(link)]['sha256']=sha(a)
    owners=[dict(owner='owner-'+category,category=category,
        expected_files={independent_text(path):digest for path,digest in filemap.items()})
        for category in OLD['CLOSURE_CATEGORIES']]
    owners.append(dict(owner='literal-file-alias',category='code_environment',expected_files={str(link):sha(a)}))
    owners.append(dict(owner='new-role-repeat',category='source_namespace',expected_files={},newly_declared_input_paths=[str(extra)]))
    new_inputs=OLD['_new_inputs']({str(extra):dict(owner='explicit-new-owner',category='source_namespace',reason='isolated tiny newly declared input')})
    relative={path.name:sha(path) for path in (a,b,parent)}
    link_specs={'link.dat':dict(text=a.name,target=str(a),kind='file',sha256=sha(a))}
    namespace=OLD['explicit_sealed_namespace'](str(regular),relative,link_specs,owner='namespace-one',category='source_namespace',directories=['empty'],aliases=list(aliases.values()))
    duplicate=json.loads(json.dumps(namespace));duplicate['owner']='namespace-two'
    aliased_namespace=json.loads(json.dumps(namespace));aliased_namespace['root']=str(directory_alias);aliased_namespace['owner']='directory-alias-namespace'
    namespaces=[namespace,duplicate,aliased_namespace]
    json_input=dict(path=str(parent),sha256=sha(parent))
    owned_paths={str(path) for path in (a,b,parent,extra)}

    def phase(module,label,*,owner_values=None,namespace_values=None,alias_values=None,expect_failure=False,released=False):
        global active
        active=label
        try:
            phase_owners=owners if owner_values is None else owner_values
            extra_keywords={}
            if released:
                phase_owners=module['_owned_phase_owner_stream'](module['_owners'](phase_owners))
                extra_keywords['release_owned_owners']=True
            value=module['_phase'](phase_owners,
                namespaces if namespace_values is None else namespace_values,
                aliases if alias_values is None else alias_values,new_inputs,json_input=json_input,**extra_keywords)
            if expect_failure:raise AssertionError('negative accepted')
            return ('PASS',value)
        except module['InputGraphError'] as error:
            if not expect_failure:raise
            return ('REJECT',str(error))
        finally:
            active=None

    old_status,old=phase(OLD,'positive-old');new_status,new=phase(NEW,'positive-new')
    released_status,released=phase(NEW,'positive-released',released=True)
    assert old_status==new_status==released_status=='PASS' and old==new==released
    assert OLD['_canonical_json'](old)==NEW['_canonical_json'](new)
    expected_count=sum(len(owner['expected_files'])+len(owner.get('newly_declared_input_paths',[])) for owner in owners)+sum(len(ns['files'])+sum(1 for value in ns['symlinks'].values() if value['kind']=='file' and 'sha256' in value)for ns in namespaces)+len(new_inputs)
    assert len(old[0])==len(new[0])==expected_count==42
    assert len({id(record)for record in new[0]})==len(new[0])
    original_second=dict(new[0][1]);new[0][0]['owner']='mutable-record-independence-test';assert new[0][1]==original_second
    new[0][0]['owner']=old[0][0]['owner']
    assert old==new
    groups={}
    oldgroups={}
    for record in new[0]:groups.setdefault(record['path'],set()).add(id(record['path']))
    for record in old[0]:oldgroups.setdefault(record['path'],set()).add(id(record['path']))
    assert all(len(ids)==1 for ids in groups.values()) and all(len(ids)==1 for ids in oldgroups.values())
    ordinary_records=[record for record in new[0] if record['path']==record['canonical_path']]
    assert ordinary_records and all(record['path'] is record['canonical_path'] for record in ordinary_records)
    assert all(record['path'] is record['canonical_path'] for record in old[0] if record['path']==record['canonical_path'])
    alias_records=[record for record in new[0] if record['path']!=record['canonical_path']]
    assert alias_records and all(record['path'] is not record['canonical_path'] for record in alias_records)
    for record in alias_records:
        ordinary=next(item for item in ordinary_records if item['path']==record['canonical_path'])
        assert record['canonical_path'] is not ordinary['path']  # no pool across distinct literal paths
    assert opens['positive-old']==opens['positive-new']==opens['positive-released']=={path:1 for path in owned_paths}
    assert len({id(record) for record in released[0]})==42
    assert [record['binding_role'] for record in released[0]][28:40]==['OWNED_EXHAUSTIVE_NAMESPACE_BYTES','OWNED_EXHAUSTIVE_NAMESPACE_BYTES','OWNED_EXHAUSTIVE_NAMESPACE_BYTES','OWNED_EXHAUSTIVE_NAMESPACE_ALIAS_TARGET_BYTES']*3
    assert [record['binding_role'] for record in released[0]][40:]==['NEWLY_DECLARED_INPUT_ONLY']*2
    assert OLD['_coverage'](old[0],old[1],{})==NEW['_coverage'](new[0],new[1],{})
    results.append(dict(case='normal-alias-directoryalias-duplicateowner-three-namespaces-newrole-parentJSON',PASS=True,requirements=expected_count,canonical_files=len(owned_paths),fresh_open_counts=opens['positive-new'],all_requirement_dicts_distinct=True,all_equal_literal_string_ids_shared=True,ordinary_equal_canonical_is_same_literal_object=True,alias_values_unchanged_and_not_cross_literal_pooled=True,all_nine_category_coverage_equal=True))

    def reject_pair(name,**kwargs):
        left=phase(OLD,name+'-old',expect_failure=True,**kwargs)
        right=phase(NEW,name+'-new',expect_failure=True,**kwargs)
        released_error=phase(NEW,name+'-released',expect_failure=True,released=True,**kwargs)
        assert left==right==released_error and left[0]=='REJECT'
        results.append(dict(case=name,PASS=True,original_and_candidate_same_exception_type_and_message=True,message=right[1]))

    a.write_bytes(b'changed same content length?')
    reject_pair('changed-input-bytes');a.write_bytes(b'alpha\x00\xff')
    link.unlink();link.symlink_to(b.name)
    reject_pair('changed-literal-alias-target');link.unlink();link.symlink_to(a.name)
    unknown=regular/'unknown.dat';unknown.write_bytes(b'unknown')
    reject_pair('unknown-regular-namespace-member');unknown.unlink()
    (regular/'empty-extra').mkdir();reject_pair('extra-empty-directory');(regular/'empty-extra').rmdir()
    conflicting=[dict(owner='conflict',category='code_environment',expected_files={str(a):'0'*64})]+owners
    reject_pair('conflicting-expected-owner',owner_values=conflicting)
    missing=[dict(owner='missing',category='code_environment',expected_files={str(root/'missing.dat'):'0'*64})]+owners
    reject_pair('missing-owned-endpoint',owner_values=missing)
    no_parent=[dict(owner=owner['owner'],category=owner['category'],expected_files={path:digest for path,digest in owner['expected_files'].items()if path!=str(parent)},**({'newly_declared_input_paths':owner['newly_declared_input_paths']}if'newly_declared_input_paths'in owner else{}))for owner in owners]
    reject_pair('parent-json-not-explicit-owner',owner_values=no_parent,namespace_values=[])
    # A fresh later phase observes a mutation; string sharing is not an FS cache.
    b.write_bytes(b'late phase changed')
    reject_pair('later-phase-byte-mutation');b.write_bytes(b'beta\x01')
    second_old=phase(OLD,'second-positive-old')[1];second_new=phase(NEW,'second-positive-new')[1]
    second_released=phase(NEW,'second-positive-released',released=True)[1]
    assert second_old==second_new==second_released==old
    assert opens['second-positive-old']==opens['second-positive-new']==opens['second-positive-released']=={path:1 for path in owned_paths}
    results.append(dict(case='later-restored-phase-fresh-full-open-once',PASS=True))

    unknown_new_owner=owners+[dict(owner='unknown-new-owner',category='source_namespace',expected_files={},newly_declared_input_paths=[str(root/'not-declared-new.dat')])]
    unknown_priority=regular/'priority-unknown.dat';unknown_priority.write_bytes(b'unknown-priority')
    reject_pair('namespace-refusal-still-precedes-later-owner-new-role',owner_values=unknown_new_owner)
    unknown_priority.unlink()
    reject_pair('later-owner-new-path-still-requires-explicit-role',owner_values=unknown_new_owner)

    # Direct _phase remains compatible and leaves caller-owned containers intact.
    external_before=OLD['_canonical_json'](owners)
    external_map_ids=[id(owner['expected_files']) for owner in owners]
    repeated=phase(NEW,'external-list-reuse')[1]
    assert repeated==old and NEW['_canonical_json'](owners)==external_before
    assert [id(owner['expected_files']) for owner in owners]==external_map_ids
    results.append(dict(case='direct-phase-external-list-and-map-reuse',PASS=True,unmodified_external_containers=True))

    # Tiny lifetime fixture only: weak-referenceable dict subclasses measure
    # actual descriptor release, not production RSS or plain JSON admission.
    class TrackedMap(dict): pass
    tracked=[dict(owner='tracked-'+str(i),category='code_environment',expected_files=TrackedMap({str(a):sha(a)})) for i in range(17)]
    tracked.append(dict(owner='tracked-new-role',category='source_namespace',expected_files=TrackedMap({}),newly_declared_input_paths=[str(extra)]))
    weak_maps=[weakref.ref(owner['expected_files']) for owner in tracked]
    stream=NEW['_owned_phase_owner_stream'](tracked)
    del tracked
    observations=[]
    progressive=[]
    def lifetime_profile(frame,event,arg):
        if event=='call' and frame.f_code is NEW['_path'].__code__ and frame.f_back.f_code.co_name=='add' and not observations:
            progressive.append(sum(ref() is not None for ref in weak_maps))
        if event=='call' and frame.f_code is NEW['_scan_namespace'].__code__:
            observations.append(dict(alive_expected_maps=sum(ref() is not None for ref in weak_maps)))
    sys.setprofile(lifetime_profile)
    try:
        released_lifetime=NEW['_phase'](stream,namespaces,aliases,new_inputs,json_input=json_input,release_owned_owners=True)
    finally:
        sys.setprofile(None)
    assert observations and all(value['alive_expected_maps']==0 for value in observations)
    assert all(ref() is None for ref in weak_maps)
    assert progressive==list(range(18,1,-1)),progressive
    assert len(released_lifetime[0])==17+12+1+1
    assert len({id(record) for record in released_lifetime[0]})==len(released_lifetime[0])
    results.append(dict(case='owned-stream-expected-maps-released-before-first-namespace-and-all-byte-reads',PASS=True,weakref_dict_fixture_only=True,tracked_maps=18,progressive_alive_map_counts_at_each_expected_add=progressive,namespace_call_observations=observations,no_RSS_savings_claimed=True))

    def post_read_refusal(name,mutate,restore):
        outcomes=[]
        for module,released in ((OLD,False),(NEW,False),(NEW,True)):
            triggered=[]
            def observer(frame,event,arg):
                if event=='return' and frame.f_code is module['_stream'].__code__ and frame.f_locals['canonical']==str(parent) and not triggered:
                    mutate();triggered.append(True)
            sys.setprofile(observer)
            try:
                outcome=phase(module,name+('-released' if released else '-'+('old' if module is OLD else 'new')),expect_failure=True,released=released)
            finally:
                sys.setprofile(None);restore()
            assert triggered==[True]
            outcomes.append(outcome)
        assert outcomes[0]==outcomes[1]==outcomes[2]
        results.append(dict(case=name,PASS=True,original_and_candidate_same_exception_type_and_message=True,message=outcomes[0][1],triggered_after_last_fresh_union_read=True))
    post_unknown=regular/'post_read_unknown.dat'
    post_read_refusal('post-read-namespace-added-file',lambda:post_unknown.write_bytes(b'post-read-unknown'),lambda:post_unknown.unlink())
    def retarget():link.unlink();link.symlink_to(b.name)
    def restore_link():link.unlink();link.symlink_to(a.name)
    post_read_refusal('post-read-alias-retarget',retarget,restore_link)
    restored=phase(NEW,'restored-after-postread-rejections',released=True)[1]
    assert restored==old and opens['restored-after-postread-rejections']=={path:1 for path in owned_paths}
    results.append(dict(case='restored-after-post-read-gates-fresh-full-byte-read',PASS=True))

    # Genuine tiny full graph create/verify: all nine closure classes, aliases,
    # namespace, expected/new bytes, an actual recorded open and exact ordering.
    with OLD['ReadOpenAudit']() as trace:
        assert a.read_bytes()==b'alpha\x00\xff'
    actual_trace=trace.snapshot()
    graph_kwargs=dict(typed_snapshot={'finite':-0.0,'records':[1,True,'x']},owners=owners,namespaces=namespaces,aliases=list(aliases.values()),read_trace=actual_trace,newly_declared_input_paths={str(extra):dict(owner='explicit-new-owner',category='source_namespace',reason='isolated tiny newly declared input')})
    graph_old=OLD['create_graph'](**graph_kwargs)
    graph_new=NEW['create_graph'](**graph_kwargs)
    assert graph_old==graph_new and OLD['_canonical_json'](graph_old)==NEW['_canonical_json'](graph_new)
    before=NEW['_canonical_json'](graph_new)
    def verified(module,label,graph,**kwargs):
        global active
        active=label
        try:return module['verify_graph'](graph,**kwargs)
        finally:active=None
    verified_old=verified(OLD,'verify-mapping-old',graph_old)
    verified_new=verified(NEW,'verify-mapping-new',graph_new)
    assert verified_old==verified_new
    assert opens['verify-mapping-old']==opens['verify-mapping-new']=={path:1 for path in owned_paths}
    assert verified_new['logical_owner_requirements']==42 and verified_new['canonical_files_read']==4
    assert before==NEW['_canonical_json'](graph_new)
    stored=root/'stored_graph.json';stored.write_bytes(before)
    left=verified(OLD,'verify-stored-old',stored,expected_sha256=sha(stored))
    right=verified(NEW,'verify-stored-new',stored,expected_sha256=sha(stored))
    assert left==right==verified_new
    assert opens['verify-stored-old']==opens['verify-stored-new']=={path:1 for path in owned_paths}
    results.append(dict(case='genuine-small-create-and-mapping-or-pinned-path-verify-full-equivalence',PASS=True,logical_requirements=42,canonical_files=4,actual_read_open_trace=True,external_graph_unmodified=True,all_saved_graph_and_return_JSON_bytes_equal=True))

    def rejected_verify(name,mutation=None):
        values=[]
        for module in (OLD,NEW):
            value=copy.deepcopy(graph_old)
            if mutation is not None:
                mutation(value)
                value['content_sha256']=module['_content_digest'](value)
            try:module['verify_graph'](value)
            except Exception as error:values.append((type(error).__name__,str(error)))
            else:raise AssertionError(name+' accepted')
        assert values[0]==values[1]
        results.append(dict(case=name,PASS=True,original_and_candidate_same_exception_type_and_message=True,message=values[0][1]))
    a.write_bytes(b'late verify mutation');rejected_verify('verify-later-byte-mutation');a.write_bytes(b'alpha\x00\xff')
    rejected_verify('verify-malformed-owner-index-before-files',lambda graph:graph['owners']['rows'][0].__setitem__(0,-1))
    rejected_verify('verify-new-input-role-changed',lambda graph:graph['newly_declared_input_paths'][str(extra)].__setitem__('binding_role','EXPECTED_INPUT_BYTES'))
    rejected_verify('verify-complete-requirement-row-changed',lambda graph:graph['requirements']['rows'][0].__setitem__(4,(graph['requirements']['rows'][0][4]+1)%4))
    assert verified(OLD,'verify-restored-old',graph_old)==verified(NEW,'verify-restored-new',graph_new)==verified_new
    assert opens['verify-restored-old']==opens['verify-restored-new']=={path:1 for path in owned_paths}
    results.append(dict(case='verify-restored-phase-after-refusal-still-fresh-full-read',PASS=True))
    # No active consumer phase exists in the unchanged library. Do not fabricate
    # one by changing globals. Assert the exact lineage function and rejection.
    scope=dict(schema=OLD['CONSUMER_CONTRACT_SCHEMA'],phase='inactive-consumer',parent_input_graph=json_input,dependency_selection=OLD['CONSUMER_SELECTION'],full_original_input_semantics_replayed=False,complete_global_closure_claimed=False)
    errors=[]
    for module in (OLD,NEW):
        try:module['_consumer_contract'](scope)
        except module['InputGraphError'] as error:errors.append(str(error))
        else:raise AssertionError('inactive consumer accepted')
    assert len(errors)==2 and errors[0]==errors[1] and OLD['CONSUMER_PHASES']==NEW['CONSUMER_PHASES']==()
    ptext=PARENT.read_text();ctext=CANDIDATE.read_text()
    def function(text,name):return ast.get_source_segment(text,next(node for node in ast.parse(text).body if isinstance(node,ast.FunctionDef) and node.name==name))
    assert function(ptext,'_consumer_lineage')==function(ctext,'_consumer_lineage')
    assert 'else:\n        # Consumer lineage still needs the complete unmodified owner maps.\n        phase_owners = owners' in function(ctext,'verify_graph')
    assert '_consumer_lineage(graph, owners, namespaces, aliases, new_inputs, fresh_parent=fresh_parent)' in function(ctext,'verify_graph')
    results.append(dict(case='inactive-consumer-contract-refusal-and-full-lineage-source-retention',PASS=True,no_consumer_globals_changed=True,no_successful_consumer_execution_claimed=True,lineage_function_byte_unchanged=True))
    for name,payload in [('duplicate-key',b'{"a":1,"a":2}'),('nonfinite',b'{"a":NaN}'),('overflow-float',b'{"a":1e999}'),('invalid-UTF8',b'{"a":"\xff"}')]:
        strict_file=root/(name+'.json');strict_file.write_bytes(payload)
        errors=[]
        for module in (OLD,NEW):
            try:module['strict_json'](strict_file,sha(strict_file))
            except Exception as error:errors.append((type(error).__name__,str(error)))
            else:raise AssertionError(name+' accepted')
        assert errors[0]==errors[1]
        results.append(dict(case='strict-JSON-'+name,PASS=True,original_and_candidate_same_exception_type_and_message=True,message=errors[0][1]))

report=dict(schema='AXMAT_OWNED_PHASE_OWNER_LIFETIMES_TINY_GENUINE_PHASE_EQUIVALENCE_V1',status='PASS_SOURCE_ONLY_TINY_FILESYSTEM_NOT_BUSINESS',parent=dict(path=str(PARENT),sha256=hashlib.sha256(PARENT.read_bytes()).hexdigest()),candidate=dict(path=str(CANDIDATE),sha256=hashlib.sha256(CANDIDATE.read_bytes()).hexdigest()),cases=results,positive_cases=sum(not case.get("original_and_candidate_same_exception_type_and_message",False) for case in results),negative_cases=sum(case.get("original_and_candidate_same_exception_type_and_message",False) for case in results),no_large_graph_or_business_API_or_ART_executed=True,source_only_no_RSS_qualification=True)
report_path=BASE/'tiny_phase_equivalence_report.json';report_path.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps(dict(report_path=str(report_path),report_sha256=hashlib.sha256(report_path.read_bytes()).hexdigest(),cases=len(results),candidate_sha256=report['candidate']['sha256'])))
