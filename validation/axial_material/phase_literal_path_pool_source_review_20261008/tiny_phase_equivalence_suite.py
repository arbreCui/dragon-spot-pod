"""Isolated genuine tiny filesystem phases; no producer/business API or large input."""
from pathlib import Path
import ast,hashlib,json,os,sys,tempfile
BASE=Path('/private/tmp/axmat-phase-literal-path-pool-graph-draft-20261008')
PARENT=Path('/Users/wen/spot/validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_low_peak_json_20261008.py')
CANDIDATE=BASE/'combined_runtime_reviewed_metadata_historical_input_graph_pooled_phase_paths_20261008.py'

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

with tempfile.TemporaryDirectory(prefix='axmat-phase-pool-tiny-',dir='/private/tmp') as temporary:
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

    def phase(module,label,*,owner_values=None,namespace_values=None,alias_values=None,expect_failure=False):
        global active
        active=label
        try:
            value=module['_phase'](owners if owner_values is None else owner_values,
                namespaces if namespace_values is None else namespace_values,
                aliases if alias_values is None else alias_values,new_inputs,json_input=json_input)
            if expect_failure:raise AssertionError('negative accepted')
            return ('PASS',value)
        except module['InputGraphError'] as error:
            if not expect_failure:raise
            return ('REJECT',str(error))
        finally:
            active=None

    old_status,old=phase(OLD,'positive-old');new_status,new=phase(NEW,'positive-new')
    assert old_status==new_status=='PASS' and old==new
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
    assert all(len(ids)==1 for ids in groups.values()) and any(len(ids)>1 for ids in oldgroups.values())
    assert opens['positive-old']==opens['positive-new']=={path:1 for path in owned_paths}
    assert OLD['_coverage'](old[0],old[1],{})==NEW['_coverage'](new[0],new[1],{})
    results.append(dict(case='normal-alias-directoryalias-duplicateowner-three-namespaces-newrole-parentJSON',PASS=True,requirements=expected_count,canonical_files=len(owned_paths),fresh_open_counts=opens['positive-new'],all_requirement_dicts_distinct=True,all_equal_literal_string_ids_shared=True,all_nine_category_coverage_equal=True))

    def reject_pair(name,**kwargs):
        left=phase(OLD,name+'-old',expect_failure=True,**kwargs)
        right=phase(NEW,name+'-new',expect_failure=True,**kwargs)
        assert left==right and left[0]=='REJECT'
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
    assert second_old==second_new==old
    assert opens['second-positive-old']==opens['second-positive-new']=={path:1 for path in owned_paths}
    results.append(dict(case='later-restored-phase-fresh-full-open-once',PASS=True))

report=dict(schema='AXMAT_PHASE_LITERAL_PATH_POOL_TINY_GENUINE_PHASE_EQUIVALENCE_V1',status='PASS_SOURCE_ONLY_TINY_FILESYSTEM_NOT_BUSINESS',parent=dict(path=str(PARENT),sha256=hashlib.sha256(PARENT.read_bytes()).hexdigest()),candidate=dict(path=str(CANDIDATE),sha256=hashlib.sha256(CANDIDATE.read_bytes()).hexdigest()),cases=results,positive_cases=2,negative_cases=8,no_large_graph_or_business_API_or_ART_executed=True,source_only_no_RSS_qualification=True)
report_path=BASE/'tiny_phase_equivalence_report.json';report_path.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps(dict(report_path=str(report_path),report_sha256=hashlib.sha256(report_path.read_bytes()).hexdigest(),cases=len(results),candidate_sha256=report['candidate']['sha256'])))
