"""Isolated source-body fixtures only; no project module/business import."""
from pathlib import Path
from types import SimpleNamespace
import ast
import copy
import hashlib
import json
import weakref

HERE = Path(__file__).resolve().parent
PARENT = Path('/Users/wen/spot/validation/axial_material/combined_runtime_current_predicates_private_declaration_lifetimes_20261009.py')
CANDIDATE = HERE/'combined_runtime_current_predicates_final_private_last_uses_20261009.py'
LABELS = ('source_factor','moment_order','original92','memory','dedup','physical','capture','original_capture16f')
THREADS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')


def fixture_data():
    records = []
    declarations = {}
    for label in LABELS:
        descriptor = dict(path='/fixture/declarations/'+label+'.json',sha256='fixture-sha-'+label)
        records.append(dict(label=label,declaration=descriptor))
        declarations[descriptor['path']] = dict(_fixture_label=label,build_python_executable='/fixture/python3.12',
            native_library_aliases={'/fixture/native-alias-'+label:'/fixture/native-target-'+label},
            numerical_loader_environment={'DYLD_FIXTURE':'original-value','OPENBLAS_CORETYPE':'original-core'})
    declarations['/fixture/declarations/capture.json']['native_dependency_alias_bindings'] = {
        '/fixture/capture-alias':dict(text='capture-target',target='/fixture/capture-target')}
    declarations['/fixture/declarations/physical.json']['prior_constructor_failure_input'] = dict(missing_paths=['/fixture/missing1','/fixture/missing2'])
    declarations['/fixture/declarations/physical.json']['control_contract'] = dict(negative_cases=[dict(name='one'),dict(name='two')])
    return dict(specs=dict(reached_component_records=records),declarations=declarations,
                environ={**{key:'1'for key in THREADS},'DYLD_FIXTURE':'original-value','OPENBLAS_CORETYPE':'original-core'})


class FreshPrivateDict(dict):
    pass


class Fixture:
    def __init__(self,data,flags):
        self.data=copy.deepcopy(data)
        self.flags=dict(flags)
        self.events=[]
        self.references=[]
        self.read_boundary_live=[]
        self.provider_boundary_live=[]
        self.lifecycle_boundaries=[]
        self.Path=self.make_path_class()
        self.native_resolutions={'/fixture/native-alias-'+label:'/fixture/native-target-'+label for label in LABELS}
        self.native_resolutions['/fixture/capture-alias']='/fixture/capture-target'

    def alive(self):
        return [label for label,reference in self.references if reference() is not None]

    def make_path_class(self):
        context=self
        class FixturePath:
            def __init__(self,value):
                self.value=str(value)
            def __str__(self):
                return self.value
            def __truediv__(self,other):
                return FixturePath(self.value.rstrip('/')+'/'+str(other))
            def __eq__(self,other):
                return isinstance(other,FixturePath)and self.value==other.value
            def resolve(self,strict=False):
                context.events.append(['path.resolve',self.value,bool(strict)])
                return FixturePath(context.native_resolutions.get(self.value,self.value))
            def is_symlink(self):
                context.events.append(['path.is_symlink',self.value])
                return self.value=='/fixture/capture-alias'and not context.flags.get('capture_not_symlink')
            def stat(self):
                context.events.append(['path.stat',self.value])
                context.lifecycle_boundaries.append(dict(boundary='work.stat_before_last_capture_append',live=context.alive()))
                if context.flags.get('working_stat_rejected'):
                    raise OSError('fixture work stat rejected')
                return SimpleNamespace(st_nlink=1)
            def exists(self):
                context.events.append(['path.exists',self.value])
                context.lifecycle_boundaries.append(dict(boundary='path.exists:'+self.value,live=context.alive()))
                return self.value==context.flags.get('present_path')
            def glob(self,pattern):
                context.events.append(['path.glob',self.value,pattern])
                return [FixturePath(self.value+'/map001')]if context.flags.get('unexpected_cold_map')else []
        return FixturePath

    def strict_json(self,path,sha):
        label=path.rsplit('/',1)[-1].removesuffix('.json')
        self.events.append(['strict_json',path,sha])
        self.read_boundary_live.append(dict(reading_label=label,live_before_new_parse=self.alive()))
        if self.flags.get('reject_read')==label:
            raise ValueError('fixture immutable JSON read rejected: '+label)
        assert sha=='fixture-sha-'+label
        value=FreshPrivateDict(copy.deepcopy(self.data['declarations'][path]))
        self.references.append((label,weakref.ref(value)))
        return value

    def readlink(self,path):
        self.events.append(['os.readlink',str(path)])
        assert str(path)=='/fixture/capture-alias'
        return 'capture-target'

    def lexists(self,path):
        self.events.append(['os.path.lexists',str(path)])
        self.lifecycle_boundaries.append(dict(boundary='physical.lexists:'+str(path),live=self.alive()))
        return str(path)==self.flags.get('present_path')

    def make_provider(self):
        context=self
        class SerialExecutor:
            pass
        class OwnRSSSerialExecutor(SerialExecutor):
            pass
        class ResourceFailure(Exception):
            pass
        P=self.Path
        c=SimpleNamespace(SerialExecutor=SerialExecutor,ResourceFailure=ResourceFailure)
        full=SimpleNamespace(OwnRSSSerialExecutor=OwnRSSSerialExecutor,__file__='/fixture/full.py')
        if context.flags.get('wrong_MRO'):
            full.OwnRSSSerialExecutor=type('FixtureWrongMRO',(object,),{})
        if context.flags.get('wrong_full_source'):
            full.__file__='/fixture/foreign-full.py'
        h=SimpleNamespace(FULL_SOURCE=P('/fixture/full.py'))
        def history_roots(roots,art):
            context.events.append(['history_roots',list(roots),str(art)])
            return [P('/fixture/history-one'),P('/fixture/history-two')]
        b=SimpleNamespace(COLD=P('/fixture/cold'),history_roots=history_roots)
        def modules():
            context.events.append(['provider.modules'])
            return b,h,full,c
        def normal_path(path):
            context.events.append(['capture.normal_path',str(path)])
            if context.flags.get('capture_normal_rejected'):
                raise ValueError('fixture capture normal_path rejected')
            return P(path)
        def working_snapshot_admission(cd,require_present):
            context.events.append(['capture.working_snapshot_admission',cd['_fixture_label'],require_present])
            assert require_present is True
            if context.flags.get('working_snapshot_rejected'):
                raise ValueError('fixture working snapshot rejected')
            return P('/fixture/work.snapshot')
        capture=SimpleNamespace(normal_path=normal_path,working_snapshot_admission=working_snapshot_admission)
        def absent(path):
            context.events.append(['physical.absent',str(path)])
            assert str(path)!=context.flags.get('present_path')
        physical=SimpleNamespace(PRIOR_GUARDED_OUT=P('/fixture/physical-guarded'),PRIOR_ABI_OUT=P('/fixture/physical-abi'),
                                 OUT=P('/fixture/physical'),absent=absent)
        def load(path,sha,name):
            context.events.append(['provider.load',str(path),sha,name])
            context.provider_boundary_live.append(dict(name=name,live=self.alive()))
            if path=='capture-source':return capture
            assert path=='physical-source'
            return physical
        class Resources:
            def check(self):
                context.events.append(['resources.check'])
                context.lifecycle_boundaries.append(dict(boundary='resources.check',live=context.alive()))
                if context.flags.get('resource_check_rejected'):
                    raise ValueError('fixture resource check rejected')
                return dict(fixture_roots=['/fixture/history-one','/fixture/history-two'],scope='ISOLATED_FIXTURE_ONLY',within_caps=True)
        def resources_for(roots,error_type):
            context.events.append(['provider.resources_for',list(roots),error_type.__name__])
            context.lifecycle_boundaries.append(dict(boundary='provider.resources_for',live=context.alive()))
            if context.flags.get('resource_for_rejected'):
                raise ValueError('fixture resource provider rejected')
            return Resources()
        self.provider_fixed_objects=(b,h,full,c,capture,physical)
        return SimpleNamespace(modules=modules,load=load,resources_for=resources_for,CAPTURE_FACTORY='capture-source',CAPTURE_FACTORY_SHA='capture-sha',
                               PHYSICAL_FACTORY='physical-source',PHYSICAL_FACTORY_SHA='physical-sha')


def source_body(path):
    source=path.read_text()
    function=next(node for node in ast.parse(source).body if isinstance(node,ast.FunctionDef)and node.name=='check_current_predicate_subset')
    return ast.Module(body=[function],type_ignores=[])


def execute(path,data,flags=None,require_build_interpreter=True):
    fixture=Fixture(data,flags or {})
    namespace=dict(Path=fixture.Path,sys=SimpleNamespace(executable='/fixture/python3.12'),
        os=SimpleNamespace(environ=fixture.data['environ'],readlink=fixture.readlink,path=SimpleNamespace(lexists=fixture.lexists)),
        THREAD_KEYS=THREADS,ART=fixture.Path('/fixture/artifacts'))
    code=compile(source_body(path),'<isolated-current-predicate-'+('original'if path==PARENT else 'candidate')+'>','exec')
    exec(code,namespace)
    provider=fixture.make_provider()
    namespace_before={key:id(value)for key,value in namespace.items()}
    provider_before=[{key:id(value)for key,value in vars(obj).items()}for obj in (provider,*fixture.provider_fixed_objects)]
    before=json.dumps(fixture.data,sort_keys=True,separators=(',',':'))
    result=None
    exception=None
    try:
        result=namespace['check_current_predicate_subset'](SimpleNamespace(strict_json=fixture.strict_json),fixture.data['specs'],provider,
                                                         require_build_interpreter=require_build_interpreter)
    except Exception as error:
        exception=dict(type=type(error).__name__,args=list(error.args))
    assert json.dumps(fixture.data,sort_keys=True,separators=(',',':'))==before,'fixture caller input mutated'
    assert namespace_before=={key:id(value)for key,value in namespace.items()},'fixture globals mutated'
    assert provider_before==[{key:id(value)for key,value in vars(obj).items()}for obj in (provider,*fixture.provider_fixed_objects)],'fixture provider module identity/global changed'
    return dict(result=result,exception=exception,events=fixture.events,read_boundary_live=fixture.read_boundary_live,
                provider_boundary_live=fixture.provider_boundary_live,lifecycle_boundaries=fixture.lifecycle_boundaries,
                live_after_return_or_caught_error=fixture.alive(),caller_input_unchanged=True,
                caller_and_provider_module_globals_unchanged=True)


def check(name,data=None,flags=None,policy=True,expected_exception=None):
    data=fixture_data()if data is None else data
    old=execute(PARENT,data,flags,policy)
    new=execute(CANDIDATE,data,flags,policy)
    assert old['result']==new['result'],name
    assert old['exception']==new['exception'],name
    assert old['events']==new['events'],name
    if expected_exception is None:
        assert old['exception']is None,(name,old['exception'])
        for options in ({'separators':(',',':')},{'indent':2}):
            assert json.dumps(old['result'],**options).encode()==json.dumps(new['result'],**options).encode(),name
        assert all(old['result'][key]is False for key in ('science_qualification_created','AAA_accuracy_qualified','ABA_admitted'))
    else:
        assert old['exception']['type']==expected_exception,(name,old['exception'])
    # Every accepted or rejected read has exactly the original order and count.
    reads=[row for row in old['events']if row[0]=='strict_json']
    assert len(reads)==len(set(row[1]for row in reads))or name.startswith('duplicate_'),name
    row=dict(name=name,status='PASS',exception=old['exception'],strict_JSON_reads=len(reads),
             complete_event_sequence_sha256=hashlib.sha256(json.dumps(old['events'],separators=(',',':')).encode()).hexdigest(),
             ordinary_dict_return_equal=old['result']==new['result'],serialized_return_byte_equal=expected_exception is None,
             exact_read_and_guard_order_equal=True,caller_inputs_unchanged=True)
    return row,old,new


rows=[]
baseline_old=baseline_new=None
for policy in (True,False):
    row,old,new=check('eight_fixed_legal_declarations_policy_'+str(policy),policy=policy)
    rows.append(row)
    if policy is True:baseline_old,baseline_new=old,new

for label in LABELS:
    data=fixture_data()
    data['declarations']['/fixture/declarations/'+label+'.json']['numerical_loader_environment']['DYLD_FIXTURE']='rejected-value'
    row,_,_=check('loader_rejection_'+label,data=data,expected_exception=None if label=='original_capture16f'else 'AssertionError')
    rows.append(row)

for label in LABELS:
    if label=='original_capture16f':continue
    for kind in ('interpreter','native'):
        data=fixture_data()
        declaration=data['declarations']['/fixture/declarations/'+label+'.json']
        if kind=='interpreter':declaration['build_python_executable']='/fixture/rejected-interpreter'
        else:declaration['native_library_aliases']['/fixture/native-alias-'+label]='/fixture/rejected-native-target'
        row,_,_=check(kind+'_rejection_'+label,data=data,expected_exception='AssertionError')
        rows.append(row)

for label in LABELS:
    row,_,_=check('strict_JSON_read_rejection_'+label,flags={'reject_read':label},expected_exception='ValueError')
    rows.append(row)

data=fixture_data();data['environ'][THREADS[0]]='2'
rows.append(check('original_single_thread_rejection',data=data,expected_exception='AssertionError')[0])
rows.append(check('invalid_interpreter_policy_rejection',policy=1,expected_exception='ValueError')[0])
data=fixture_data();data['declarations']['/fixture/declarations/physical.json']['numerical_loader_environment']['DYLD_FIXTURE']='first-rejected-value';data['declarations']['/fixture/declarations/capture.json']['build_python_executable']='/fixture/later-rejected-interpreter'
rows.append(check('original_multiple_error_precedence',data=data,expected_exception='AssertionError')[0])

for flag,expected in (('capture_not_symlink','AssertionError'),('working_snapshot_rejected','ValueError'),('unexpected_cold_map','AssertionError')):
    rows.append(check(flag,flags={flag:True},expected_exception=expected)[0])
for path in ('/fixture/missing1','/fixture/physical-guarded/seal.json','/fixture/cold/AAA/bootstrap/result.json',
             '/fixture/physical/controls/negative_one/unexpected_return.txt',
             '/fixture/artifacts/axial-material-rank1-cache-native-angular-capture-20261007/seal.json'):
    rows.append(check('original_absence_rejection_'+path,flags={'present_path':path},expected_exception='AssertionError')[0])
for kind in ('text','target'):
    data=fixture_data();data['declarations']['/fixture/declarations/capture.json']['native_dependency_alias_bindings']['/fixture/capture-alias'][kind]='rejected-'+kind
    rows.append(check('capture_alias_'+kind+'_rejection',data=data,expected_exception='AssertionError')[0])

for label in ('capture','physical','dedup'):
    data=fixture_data();record=copy.deepcopy(next(row for row in data['specs']['reached_component_records']if row['label']==label));data['specs']['reached_component_records'].append(record)
    rows.append(check('duplicate_'+label+'_last_value_semantics',data=data)[0])
data=fixture_data();data['specs']['reached_component_records'][0]['label']=[]
rows.append(check('original_unhashable_label_error_precedence',data=data,expected_exception='TypeError')[0])
data=fixture_data();data['specs']['reached_component_records']=[]
rows.append(check('original_missing_capture_key_error',data=data,expected_exception='KeyError')[0])

assert [len(row['live_before_new_parse'])for row in baseline_old['read_boundary_live']]==[0,0,0,0,0,0,1,2]
assert [len(row['live_before_new_parse'])for row in baseline_new['read_boundary_live']]==[0,0,0,0,0,0,1,2]
assert all(set(row['live'])=={'capture','physical'}for row in baseline_old['provider_boundary_live'])
assert all(set(row['live'])=={'capture','physical'}for row in baseline_new['provider_boundary_live'])
assert baseline_old['live_after_return_or_caught_error']==baseline_new['live_after_return_or_caught_error']==[]
assert len([row for row in baseline_old['events']if row[0]=='strict_json'])==8



# The first 50 rows retain every pinned original case and event/exception digest.
prior_report=json.loads(Path('/private/tmp/axmat_private_declaration_lifetimes_source_draft_20261009/tiny_report.json').read_bytes())
assert len(rows)==50 and len(prior_report['cases'])==50
assert [row['name']for row in rows]==[row['name']for row in prior_report['cases']]
for old,new in zip(prior_report['cases'],rows):
    assert old['exception']==new['exception'],new['name']
    assert old['complete_event_sequence_sha256']==new['complete_event_sequence_sha256'],new['name']

def live_at(result,boundary):
    matches=[row['live']for row in result['lifecycle_boundaries']if row['boundary']==boundary]
    assert len(matches)==1,boundary
    return set(matches[0])

assert live_at(baseline_old,'work.stat_before_last_capture_append')=={'capture','physical'}
assert live_at(baseline_new,'work.stat_before_last_capture_append')=={'capture','physical'}
assert live_at(baseline_old,'physical.lexists:/fixture/missing1')=={'capture','physical'}
assert live_at(baseline_new,'physical.lexists:/fixture/missing1')=={'physical'}
assert live_at(baseline_new,'path.exists:/fixture/physical/controls/negative_two/unexpected_return.txt')=={'physical'}
memory_boundary='path.exists:/fixture/artifacts/axial-material-rank1-cache-native-angular-capture-20261007/seal.json'
for boundary in (memory_boundary,'provider.resources_for','resources.check'):
    assert live_at(baseline_old,boundary)=={'capture','physical'}
    assert live_at(baseline_new,boundary)==set()

for name,flags,kind in (
    ('last_capture_normal_failure',{'capture_normal_rejected':True},'ValueError'),
    ('last_capture_workstat_failure',{'working_stat_rejected':True},'OSError'),
    ('late_resource_provider_failure',{'resource_for_rejected':True},'ValueError'),
    ('late_resource_check_failure',{'resource_check_rejected':True},'ValueError'),
    ('original_MRO_failure',{'wrong_MRO':True},'AssertionError'),
    ('original_full_source_failure',{'wrong_full_source':True},'AssertionError'),
):
    row,old,new=check(name,flags=flags,expected_exception=kind);rows.append(row)
    if name.startswith('late_resource'):
        boundary='provider.resources_for'if name=='late_resource_provider_failure'else 'resources.check'
        assert live_at(old,boundary)=={'capture','physical'}
        assert live_at(new,boundary)==set()

data=fixture_data();data['specs']['reached_component_records']=[r for r in data['specs']['reached_component_records']if r['label']!='physical']
rows.append(check('after_capture_release_missing_physical_KeyError',data=data,expected_exception='KeyError')[0])
data=fixture_data();del data['declarations']['/fixture/declarations/physical.json']['control_contract']
rows.append(check('physical_lastuse_missing_control_contract_KeyError',data=data,expected_exception='KeyError')[0])
data=fixture_data();data['declarations']['/fixture/declarations/physical.json']['control_contract']['negative_cases']=None
rows.append(check('physical_lastuse_negative_cases_TypeError',data=data,expected_exception='TypeError')[0])
data=fixture_data();data['declarations']['/fixture/declarations/physical.json']['control_contract']['negative_cases']=[{}]
rows.append(check('physical_lastuse_negative_case_missing_name_KeyError',data=data,expected_exception='KeyError')[0])

# Del follows the completed loop even when no physical absence/control rows exist.
data=fixture_data();data['declarations']['/fixture/declarations/physical.json']['prior_constructor_failure_input']['missing_paths']=[]
data['declarations']['/fixture/declarations/physical.json']['control_contract']['negative_cases']=[]
row,old,new=check('empty_physical_absence_and_negative_rows',data=data);rows.append(row)
assert live_at(new,memory_boundary)==set()

# Simultaneous faults preserve the first original gate and complete event prefix.
data=fixture_data();data['declarations']['/fixture/declarations/capture.json']['native_dependency_alias_bindings']['/fixture/capture-alias']['text']='bad-first-text'
rows.append(check('capture_alias_before_physical_absence_error_priority',data=data,
    flags={'present_path':'/fixture/missing1'},expected_exception='AssertionError')[0])
data=fixture_data();data['declarations']['/fixture/declarations/physical.json']['control_contract']['negative_cases']=[{},dict(name='two')]
rows.append(check('negative_case_key_before_later_memory_absence_priority',data=data,
    flags={'present_path':'/fixture/artifacts/axial-material-rank1-cache-native-angular-capture-20261007/seal.json'},expected_exception='KeyError')[0])
rows.append(check('capture_snapshot_before_workstat_error_priority',flags={'working_snapshot_rejected':True,'working_stat_rejected':True},expected_exception='ValueError')[0])
rows.append(check('physical_absence_before_resource_error_priority',flags={'present_path':'/fixture/missing1','resource_check_rejected':True},expected_exception='AssertionError')[0])

for label in ('capture','physical'):
    data=fixture_data();data['specs']['reached_component_records']=[r for r in data['specs']['reached_component_records']if r['label']==label]
    rows.append(check('single_'+label+'_retains_original_missing_peer_error',data=data,expected_exception='KeyError')[0])

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


def pin(path):
    return dict(path=str(path),bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest())


report=dict(schema='AXMAT_FINAL_PRIVATE_LAST_USES_ISOLATED_SOURCE_DIFFERENTIAL_TINY_V1',status='PASS_ISOLATED_FIXTURES_ONLY_SOURCE_STOPPED',
    parent=pin(PARENT),candidate=pin(CANDIDATE),suite_source=pin(Path(__file__).resolve()),case_count=len(rows),cases=rows,
    fixed_legal_small_fixture_labels=list(LABELS),each_of_eight_decl_reads_once_in_base_case=True,
    seven_current_loader_refusals_equal=True,original_capture16f_loader_skip_preserved=True,
    all_original_exception_types_args_and_first_failure_event_sequences_equal=True,
    complete_ordinary_dict_outputs_and_JSON_bytes_equal=True,
    all_fixture_caller_inputs_unchanged=True,all_fixture_caller_and_provider_module_globals_unchanged=True,
    original_50_cases_preserved=True,original_50_case_source=pin(Path('/private/tmp/axmat_private_declaration_lifetimes_source_draft_20261009/tiny_suite.py')),
    original_50_case_report=pin(Path('/private/tmp/axmat_private_declaration_lifetimes_source_draft_20261009/tiny_report.json')),
    weakref_observation=dict(original=baseline_old['read_boundary_live'],candidate=baseline_new['read_boundary_live'],
        original_before_post_loop_load=baseline_old['provider_boundary_live'],candidate_before_post_loop_load=baseline_new['provider_boundary_live'],
        both_all_private_declarations_dead_after_return=True,
        observed_object_type='Fresh private dict subclass carrying weakref support; no objects retained by observer.',
        new_nonneeded_parsed_dicts_die_before_next_parse=True,
        parent_last_use_boundaries=baseline_old['lifecycle_boundaries'],candidate_last_use_boundaries=baseline_new['lifecycle_boundaries'],
        capture_released_before_first_physical_absence_check=True,physical_released_before_memory_literal_absences=True,
        both_released_before_resource_provider_and_check=True,
        measured_RSS_or_allocator_return_to_OS=False),
    isolation=dict(only_one_checked_function_definition_compiled=True,
        actual_project_module_imported=False,actual_current_predicate_API_called=False,
        real_graph_union_or_file_bytes_checked=False,real_declaration_or_live_environment_accepted=False,
        actual_business_constructor=False,actual_numeric_or_native_child=False,
        ART_or_formal_source_written=False,PREP_or_RUN_or_cold_executed=False),
    actual_RSS_measurement=False,complete_map=False,AAA_qualification=False,ABA_qualification=False,
    limitations='Fake paths/providers/reader/loader environment test the unchanged function control flow and output with fixed small data. This proves isolated semantics and private reference lifetime, not canonical environment validation, full input-union bytes, actual allocator/RSS savings, original audit completion or scientific qualification.')
(HERE/'tiny_report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps(dict(status=report['status'],cases=len(rows),weakref_live_before_reads_original=[0,0,0,0,0,0,1,2],
                     weakref_live_before_reads_candidate=[0,0,0,0,0,0,1,2],
                     final_resource_boundary_parent=['physical','capture'],final_resource_boundary_candidate=[],
                     report=pin(HERE/'tiny_report.json'))))
