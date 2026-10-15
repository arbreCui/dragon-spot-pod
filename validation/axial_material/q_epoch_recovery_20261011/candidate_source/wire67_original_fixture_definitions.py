"""All original 67 tiny-data fixtures; full real-edge run is separate."""
import inspect,json,struct
from pathlib import PurePosixPath
events=[]

class GuardViolation(BaseException):pass

def typed(value):
    k=type(value)
    if k is float:return ['float',struct.pack('>d',value).hex()]
    if k is dict:return ['dict',[[typed(a),typed(b)] for a,b in value.items()]]
    if k in (list,tuple):return [k.__name__,[typed(v) for v in value]]
    if isinstance(value,str):return [k.__name__,str.__str__(value),typed(vars(value)) if hasattr(value,'__dict__') else None]
    if k in (type(None),int,bool):return [k.__name__,value]
    if isinstance(value,PurePosixPath):return [k.__name__,str(value)]
    return [k.__name__,repr(value)]

def identities(value):
    if type(value) in (list,tuple):return [id(value),[identities(v) for v in value]]
    if type(value) is dict:return [id(value),[[identities(k),identities(v)] for k,v in value.items()]]
    return id(value)

class TaggedStr(str):
    def __new__(cls,value,tag):
        x=super().__new__(cls,value);x.tag=tag;return x
    def __lt__(self,other):
        events.append(['lt',self.tag,str.__str__(self),str.__str__(other) if isinstance(other,str) else repr(other)])
        return super().__lt__(other)
    def __str__(self):return 'custom __str__:'+str.__str__(self)

class Reiterable:
    def __init__(self,first,second):self.first=first;self.second=second;self.calls=0;self.length_calls=0
    def __iter__(self):self.calls+=1;return iter(self.first if self.calls==1 else self.second)
    def __len__(self):self.length_calls+=1;return len(self.second)

class RowList(list):pass

class RowTuple(tuple):pass

def state(value):
    if isinstance(value,Reiterable):return ['Reiterable',typed(value.first),typed(value.second),value.calls,value.length_calls]
    if inspect.isgenerator(value):return ['generator',inspect.getgeneratorstate(value)]
    return typed(value)

def attempt(module,build,method='_wire_requirement_table_compact'):
    global events
    value=build();before=state(value);before_ids=identities(value);events=[]
    try:
        answer=getattr(module,method)(value);outcome=dict(kind='return',complete_typed_return=typed(answer))
        try:outcome['complete_canonical_bytes_hex']=module._canonical_json(answer).hex()
        except GuardViolation:raise
        except BaseException as e:outcome['canonical_encoding_exception']=[type(e).__name__,str(e)]
    except GuardViolation:raise
    except BaseException as e:outcome=dict(kind='raise',exception_class=type(e).__name__,exception_message=str(e))
    return dict(outcome=outcome,comparison_events=list(events),caller_before=before,caller_after=state(value),caller_all_nested_identity_unchanged=before_ids==identities(value))

def wire_fixture_controls(old,new):
    base=('/pure/control/a','/pure/control/canonical','owner',old.CLOSURE_CATEGORIES[0],old.REQUIREMENT_ROLES[0])
    valid=[base,('/pure/control/b','/pure/control/canonical','owner',old.CLOSURE_CATEGORIES[1],old.REQUIREMENT_ROLES[0]),('/pure/control/a','/pure/control/canonical','ownerZ',old.CLOSURE_CATEGORIES[0],old.REQUIREMENT_ROLES[1]),base]
    fixtures=[('empty',lambda:[]),('complete_duplicates_and_key_ties',lambda:list(reversed(valid))),('tuple_container',lambda:tuple(valid)),('generator_original_exhaustion',lambda:(r for r in valid)),('row_list_rejected',lambda:[list(base)]),('list_subclass_shape_rejected',lambda:[RowList(base)]),('tuple_subclass_shape_rejected',lambda:[RowTuple(base)]),('empty_tuple_rejected',lambda:[()]),('short_tuple_rejected',lambda:[base[:-1]]),('long_tuple_rejected',lambda:[base+('extra',)]),('relative_path_rejected',lambda:[('relative',)+base[1:]]),('unnormalized_path_rejected',lambda:[('/pure/../control/a',)+base[1:]]),('nul_path_rejected',lambda:[('/pure/\x00/a',)+base[1:]]),('blank_owner_rejected',lambda:[base[:2]+(' ',)+base[3:]]),('bad_category_rejected',lambda:[base[:3]+('unknown',)+base[4:]]),('bad_role_rejected',lambda:[base[:4]+('unknown',)])]
    for field in range(5):
        fixtures.append(('accepted_str_subclass_field_'+str(field),lambda field=field:[tuple(TaggedStr(v,'field_'+str(i)) if i==field else v for i,v in enumerate(r)) for r in reversed(valid)]))
        for name,value in [('negative_zero',-0.0),('finite_float',1.25),('nan_payload',struct.unpack('>d',bytes.fromhex('7ff8000000000042'))[0]),('positive_inf',float('inf')),('negative_inf',-float('inf')),('bool',True),('none',None)]:
            fixtures.append((name+'_field_'+str(field),lambda field=field,value=value:[tuple(value if i==field else v for i,v in enumerate(base))]))
    fixtures.append(('accepted_PurePosixPath_nonexact_fields',lambda:[(PurePosixPath(base[0]),PurePosixPath(base[1]))+base[2:]]))
    for name,second in [('None',[None]),('short_tuple',[('/pure/control/a',)]),('list',[list(base)]),('valid_changed',[valid[1],base,base]),('invalid_nonexact',[('/pure/control/a','/pure/control/canonical','owner','unknown',old.REQUIREMENT_ROLES[0])])]:
        fixtures.append(('reiterable_second_pass_'+name,lambda second=second:Reiterable([base],second)))
    fixture_results=[]
    phase='fixtures_original_and_candidate'
    for name,build in fixtures:
        left=attempt(old,build);right=attempt(new,build)
        if left!=right:raise ValueError('wire fixture exact typed/state/exception/comparison difference: '+name)
        fixture_results.append(dict(case=name,old_equals_candidate_complete_return_or_exception=True,original_complete_evidence=left))
    json_fixtures=[('finite_types_order_floatbits',lambda:{'z':[True,1,1.0,-0.0,0.0,1e-300,None],'a':{'b':'text','a':[1.25]}}),('json_str_subclass',lambda:{'x':TaggedStr('text','json')}),('json_nonfinite_nan',lambda:{'x':float('nan')}),('json_nonfinite_inf',lambda:[float('inf')]),('json_nonfinite_negative_inf',lambda:[-float('inf')])]
    for name,build in json_fixtures:
        left=attempt(old,build,'_json_clone');right=attempt(new,build,'_json_clone')
        if left!=right:raise ValueError('unchanged full JSON protocol fixture differs: '+name)
        fixture_results.append(dict(case=name,old_equals_candidate_complete_return_or_exception=True,original_complete_evidence=left))
    assert len(fixture_results)==67
    assert sum(r['original_complete_evidence']['outcome']['kind']=='return' for r in fixture_results)==14
    assert sum(r['original_complete_evidence']['outcome']['kind']=='raise' for r in fixture_results)==53
    return fixture_results
