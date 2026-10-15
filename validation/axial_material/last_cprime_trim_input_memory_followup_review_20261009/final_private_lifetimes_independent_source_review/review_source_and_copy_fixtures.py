import ast
import hashlib
import json
import os
import stat
from pathlib import Path

OUT=Path('/private/tmp/axmat_current_predicates_final_private_last_uses_independent_review_20261009')
AUTHOR=Path('/private/tmp/axmat_current_predicates_final_private_last_uses_source_candidate_20261009')
PARENT=Path('/Users/wen/spot/validation/axial_material/combined_runtime_current_predicates_private_declaration_lifetimes_20261009.py')
CAND=AUTHOR/'combined_runtime_current_predicates_final_private_last_uses_20261009.py'
PINS={}
def read(p,expected=None):
    s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
    assert stat.S_ISREG(s.st_mode) and p.parent.resolve(strict=True)==p.parent
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
        fs=os.fstat(f.fileno());assert [fs.st_dev,fs.st_ino]==before[:2];raw=f.read()
    fs=p.lstat();assert [fs.st_dev,fs.st_ino,fs.st_mode,fs.st_size,fs.st_mtime_ns,fs.st_ctime_ns,fs.st_nlink]==before
    sha=hashlib.sha256(raw).hexdigest()
    if expected:assert sha==expected
    PINS[str(p)]=dict(path=str(p),identity=before,size=len(raw),sha256=sha)
    return raw
def body(raw,n):return b''.join(raw.splitlines(keepends=True)[n.lineno-1:n.end_lineno])

old=read(PARENT,'2d9bf60b5a27d8cc32de5cc231e20b6caf65fa85f8c66d770124e0a0f1809b8f')
new=read(CAND,'fd3bdb5543044fc71f0acb9799b1c6fcf7709cbbf22342f0931a299af59cee19')
insertions=(b"    del declarations['capture'], cd\n",b"    del declarations['physical'], pd\n")
assert all(new.count(line)==1 for line in insertions)
inverse=new
for line in insertions:inverse=inverse.replace(line,b'',1)
assert inverse==old and len(new)-len(old)==73
ot=ast.parse(old);nt=ast.parse(new);assert len(ot.body)==len(nt.body)
olddefs=[n.name for n in ot.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
newdefs=[n.name for n in nt.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))];assert olddefs==newdefs
inventory=[]
for a,b in zip(ot.body,nt.body):
    target=isinstance(a,ast.FunctionDef) and a.name=='check_current_predicate_subset'
    if target:
        assert ast.dump(a.args)==ast.dump(b.args)
        assert body(new,b).replace(insertions[0],b'',1).replace(insertions[1],b'',1)==body(old,a)
        dels=[i for i in b.body if isinstance(i,ast.Delete) and ast.unparse(i) in ("del declarations['capture'], cd","del declarations['physical'], pd")]
        assert len(dels)==2
        stripped=ast.FunctionDef(name=b.name,args=b.args,body=[i for i in b.body if i not in dels],decorator_list=b.decorator_list,returns=b.returns,type_comment=b.type_comment,type_params=b.type_params)
        assert ast.dump(stripped,include_attributes=False)==ast.dump(a,include_attributes=False)
        for index,deletion in enumerate(dels):
            at=b.body.index(deletion)
            prior=b.body[at-1]
            if index==0:
                assert isinstance(prior,ast.Expr) and ast.unparse(prior.value).startswith('observed.append(')
                assert isinstance(b.body[at+1],ast.Assign) and ast.unparse(b.body[at+1])=="pd = declarations['physical']"
                forbidden={'cd'}
            else:
                assert isinstance(prior,ast.For) and ast.unparse(prior.iter)=="pd['control_contract']['negative_cases']"
                forbidden={'pd'}
            for following in b.body[at+1:]:
                assert not any(isinstance(i,ast.Name) and isinstance(i.ctx,ast.Load) and i.id in forbidden for i in ast.walk(following))
                assert not any(isinstance(i,ast.Subscript) and isinstance(i.value,ast.Name) and i.value.id=='declarations' and isinstance(i.slice,ast.Constant) and i.slice.value==('capture' if index==0 else 'physical') for i in ast.walk(following))
    else:
        assert body(old,a)==body(new,b) and ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False)
    inventory.append(dict(kind=type(a).__name__,name=getattr(a,'name',None),target=target,non_target_exact=not target))
author_suite=read(AUTHOR/'tiny_suite.py','74562749d09fea4ea981b96ed4181436629b93355e7f68ce668f480354d44ee8')
author_report=read(AUTHOR/'tiny_report.json','dde6ca600ec65b83acf6715d58edb57dc2fd4700130d550e5ca12a4a83080b5a')
read(AUTHOR/'actual_source_tiny_tool_return.json','7f6f833bebfc84260ec876cd0bb499c7fd73488d86a7eb062c3e67464b4585bc')
assert json.loads(author_report)['case_count']==67
extension='''
# Independent added boundary cases, after all 67 author cases.
assert len(rows)==67
data=fixture_data();data['declarations']['/fixture/declarations/capture.json']['native_dependency_alias_bindings']={}
rows.append(check('independent_empty_capture_aliases',data=data)[0])
data=fixture_data();del data['declarations']['/fixture/declarations/capture.json']['native_dependency_alias_bindings']
rows.append(check('independent_missing_capture_bindings',data=data,expected_exception='KeyError')[0])
data=fixture_data();del data['declarations']['/fixture/declarations/physical.json']['prior_constructor_failure_input']['missing_paths']
rows.append(check('independent_missing_physical_missing_paths',data=data,expected_exception='KeyError')[0])
data=fixture_data();del data['declarations']['/fixture/declarations/physical.json']['control_contract']['negative_cases']
rows.append(check('independent_missing_physical_negative_cases',data=data,expected_exception='KeyError')[0])
data=fixture_data();data['declarations']['/fixture/declarations/physical.json']['control_contract']['negative_cases']=[dict(name=None)]
rows.append(check('independent_negative_name_none',data=data,expected_exception='TypeError')[0])
data=fixture_data();data['declarations']['/fixture/declarations/physical.json']['control_contract']['negative_cases']=[dict(name='')]
rows.append(check('independent_negative_name_empty',data=data)[0])
data=fixture_data();data['specs']['reached_component_records']=list(reversed(data['specs']['reached_component_records']))
rows.append(check('independent_reverse_record_order',data=data)[0])
data=fixture_data();data['specs']['reached_component_records']=[r for r in data['specs']['reached_component_records']if r['label']=='original_capture16f']
rows.append(check('independent_only_original_capture16f',data=data,expected_exception='KeyError')[0])
rows.append(check('independent_policy_none',policy=None,expected_exception='ValueError')[0])
rows.append(check('independent_physical_absence_before_provider_error',flags={'present_path':'/fixture/missing2','resource_for_rejected':True},expected_exception='AssertionError')[0])
assert len(rows)==77

'''
marker=b'\ndef pin(path):\n';assert author_suite.count(marker)==1
suite=author_suite.replace(marker,extension.encode()+marker)
with (OUT/'tiny_suite.py').open('xb') as f:f.write(suite)
with (OUT/CAND.name).open('xb') as f:f.write(new)
assert (OUT/CAND.name).read_bytes()==new
report=dict(schema='AXMAT_FINAL_PRIVATE_LAST_USES_INDEPENDENT_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY',parent=PINS[str(PARENT)],candidate=PINS[str(CAND)],only_two_insertions_full_inverse_exact=True,added_bytes=73,top_level_nodes=len(ot.body),actual_top_level_def_count=len(olddefs),actual_top_level_def_names=olddefs,all_non_target_statements_and_defs_byte_AST_exact=True,target_function_original_guards_reads_errors_return_signature_AST_exact=True,only_plain_private_dictionary_and_local_refs_deleted_after_last_use=True,no_future_reference_to_deleted_private_owners=True,original_six_private_deletions_unchanged=True,source_inventory=inventory,fixture_author_pins=PINS,fixture_copy_preserves_all_67_author_cases=True,additional_cases=10,fixture_copy_only_new_cases_and_own_output_directory=True,business_provider_formal_module_or_main_loaded=False,actual_RSS_or_native_or_science_credit=False,fixture_execution=None)
with (OUT/'source_review.json').open('x') as f:json.dump(report,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps(dict(status=report['status'],defs=len(olddefs),new_cases=10,total_cases_planned=77,source_report_sha256=hashlib.sha256((OUT/'source_review.json').read_bytes()).hexdigest(),no_business=True)))
