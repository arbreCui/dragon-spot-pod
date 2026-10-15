"""Independent Source/serialization review and exact ten-control derivation.

This script executes extracted pure functions only. It starts no children,
uses no PS/lsof, and makes no Native, window, control, or science PASS claim.
"""
import ast
import copy
import difflib
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import stat
import sys
import time

HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'complete_history_root_index_source_v15_20261010'
ORIGINAL_D=BASE/'actual_invalid_prepost_d19_monitor_controls_sources_20261011'
ART=HERE.parent.parent/'artifacts'
START=time.monotonic()
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
FIELDS=('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
JOURNAL=ART/'axial-material-grouped-native-AB-d19-v2-20261011-host/runtime/ACTUAL_FAILURE_ONLY_MONITOR_EVENTS.jsonl'

def require(value,message):
    if type(value)is not bool or not value:raise ValueError(message)

def budget():
    require(time.monotonic()-START<600,'independent pure metadata600 cap')
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform!='darwin':peak*=1024
    require(peak<512*2**20,'independent pure self512 MiB cap')

def ident(s):return [getattr(s,k)for k in FIELDS]

def pin(path):
    path=Path(path);before=ident(path.lstat())
    require(path.is_absolute()and all(not p.is_symlink()for p in(path,*path.parents))and stat.S_ISREG(before[2])and before[3]==1,'ordinary singlelink full file')
    digest=hashlib.sha256();size=0
    with path.open('rb')as stream:
        require(ident(os.fstat(stream.fileno()))==before,'opened full pin unchanged')
        while True:
            budget();raw=stream.read(2**20)
            if not raw:break
            size+=len(raw);digest.update(raw)
        require(ident(os.fstat(stream.fileno()))==before,'EOF full pin unchanged')
    require(ident(path.lstat())==before and size==before[4],'closed full pin unchanged')
    return dict(path=str(path),size_bytes=size,sha256=digest.hexdigest(),identity=before)

def read(raw):
    def pairs(items):
        out={}
        for key,value in items:require(key not in out,'unique saved JSON keys');out[key]=value
        return out
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in()).throw(ValueError(s)))

def write(path,value):
    budget()
    with Path(path).open('x',encoding='utf-8')as stream:
        json.dump(value,stream,ensure_ascii=False,allow_nan=False,indent=2);stream.write('\n');stream.flush();os.fsync(stream.fileno())

def old_encode(event,account,check):
    raw=None;rounds=0
    for unused in range(8):
        check();rounds+=1
        candidate=(json.dumps(event,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8')
        size=len(candidate)
        if account['additional_record_bytes']==size:raw=candidate;break
        account['additional_record_bytes']=size
    require(raw is not None and len(raw)==account['additional_record_bytes'],'original exact fixed point within eight')
    return raw,rounds

def compare(event,new_encode,initial=0):
    a=copy.deepcopy(event);b=copy.deepcopy(event)
    aa=a['actual_diagnostic_write_byte_account_before'];bb=b['actual_diagnostic_write_byte_account_before']
    aa['additional_record_bytes']=initial;bb['additional_record_bytes']=initial
    before=(json.dumps(event,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8')
    old,rounds=old_encode(a,aa,budget);new=new_encode(b,bb,budget)
    require(old==new and a==b,'original/new complete bytes and final objects equal')
    require(len(new)==bb['additional_record_bytes'],'actual complete UTF8 integer exact')
    return dict(bytes=len(new),sha256=hashlib.sha256(new).hexdigest(),original_rounds=rounds)

def event(padding='',extra=None):
    account=dict(additional_record_bytes=0,actual_regular_joint_bytes=0,nested={'字':['🙂',-0.0,True,None]})
    return dict(event='fresh_frame_invalid_not_resource_PASS',padding=padding,extra=extra,
        actual_diagnostic_write_byte_account_before=account,resource_PASS=False)

def main():
    require(os.environ.get('PYTHONDONTWRITEBYTECODE')=='1'and all(os.environ.get(k)=='1'for k in THREADS),'pure single-thread environment')
    original=ORIGINAL_D/'fresh_frame_observation_adapter.py';candidate=HERE/'fresh_frame_observation_adapter.py'
    proof=HERE/'ACTUAL_PURE_SERIALIZATION_REVIEW.json';tools=HERE/'ACTUAL_PURE_SERIALIZATION_TRUE_TOOL_RETURNS.json'
    control=ORIGINAL_D/'fresh_frame_genuine_controls.py';binding=ORIGINAL_D/'Root_fresh_frame_controls_Source_binding.json'
    inputs=[original,candidate,HERE/'added_pure_encoder_Source.py',HERE/'frame_encoder_only.patch',proof,tools,control,binding,JOURNAL,Path(__file__).resolve()]
    pins=[pin(p)for p in inputs]
    require(pins[0]['sha256']=='a2b507e0f5e5470c227484f1d8a1e63367aed2313cb15695a9c46b57a2d444cc','actual original Source SHA')
    old=original.read_text();new=candidate.read_text();helper=inputs[2].read_text()
    oldloop="""            raw=None
            for serialization in range(8):
                budget()
                candidate=(json.dumps(event,ensure_ascii=False,allow_nan=False)+'\\n').encode('utf-8')
                size=len(candidate)
                if account['additional_record_bytes']==size:
                    raw=candidate;break
                account['additional_record_bytes']=size
"""
    newcall='            raw=complete_frame_self_accounted_UTF8(event,account,budget)\n'
    require(new.count(helper)==1 and new.count(newcall)==2 and new.replace(helper,'',1).replace(newcall,oldloop)==old,'full Source byte inverse exact')
    patch=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=str(original),tofile=str(candidate)))
    require(inputs[3].read_text()==patch,'whole patch exact')
    oldtree=ast.parse(old);newtree=ast.parse(new)
    defs={n.name:n for n in newtree.body if isinstance(n,ast.FunctionDef)}
    env={'json':json}
    exec(compile(ast.Module(body=[defs['require'],defs['complete_frame_self_accounted_UTF8']],type_ignores=[]),'<independent extracted pure encoder>','exec'),env)
    encode=env['complete_frame_self_accounted_UTF8']
    oldcaps=next(n.value for n in oldtree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='CAPS'for t in n.targets))
    require(eval(compile(ast.Expression(oldcaps),'<caps>','eval'),{})==CAPS,'nine exact original caps')
    # Both private callers make a fresh local dictionary from disk_account(0),
    # insert it at one exact key, then encode. No alias escapes before encoding.
    actual_local_account_assignments=[n for n in ast.walk(oldtree)if isinstance(n,ast.Assign)
        and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id=='account'
        and isinstance(n.value,ast.Call)and ast.unparse(n.value)=='monitor.disk_account(0)']
    require(len(actual_local_account_assignments)==2 and old.count("event['actual_diagnostic_write_byte_account_before']=account")==3,'actual fresh account call/insert sites inspected')
    actual_count=0;actual_bytes=0;maxrounds=0;events={}
    with JOURNAL.open('rb')as stream:
        for raw in stream:
            budget();e=read(raw)
            if e['event']not in('fresh_frame_complete_candidate','fresh_frame_invalid_not_resource_PASS'):continue
            require(all(type(k)is str for k in e)and all(type(k)is str for k in e['actual_diagnostic_write_byte_account_before']),'actual structural account keys strings')
            result=compare(e,encode)
            copy_e=copy.deepcopy(e);acc=copy_e['actual_diagnostic_write_byte_account_before'];acc['additional_record_bytes']=0
            require(encode(copy_e,acc,budget)==raw,'entire real saved UTF8 frame equals independent new encoding')
            actual_count+=1;actual_bytes+=len(raw);maxrounds=max(maxrounds,result['original_rounds']);events[e['event']]=events.get(e['event'],0)+1
    require(actual_count==86 and actual_bytes==38723036 and events==dict(fresh_frame_complete_candidate=65,fresh_frame_invalid_not_resource_PASS=21),'complete actual d19 sample scope')
    cases=[]
    for extra in('中文🙂\n\r\t\"\\é𝄞',[-0.0,0.0,5e-324,sys.float_info.max],{'2':2,2:3,2.5:4,None:5,False:6},[],{}):
        cases.append(compare(event(extra=extra),encode))
    for key in(2,2.5,True,None):
        e=event();e[key]=['字',-0.0];cases.append(compare(e,encode))
    base=compare(event(),encode)['bytes']
    for power in(3,4,5):
        for delta in range(-4,5):
            e=event('x'*max(0,10**power-base+delta))
            for initial in(0,9,99,999,10**12):
                result=compare(e,encode,initial);maxrounds=max(maxrounds,result['original_rounds']);cases.append(result)
    refusal_count=0
    for extra in(float('nan'),float('inf'),-float('inf'),{float('nan'):1},b'unsupported'):
        for fn in(old_encode,encode):
            e=event(extra=extra)
            try:fn(e,e['actual_diagnostic_write_byte_account_before'],budget)
            except(ValueError,TypeError):refusal_count+=1
            else:raise ValueError('nonfinite/unsupported value admitted')
    # Alias expansion is intentionally outside the actual two caller model.
    # Show that the helper is not a generic arbitrary-alias JSON replacement.
    alias_event=event();alias_event['unreachable_extra_alias']=alias_event['actual_diagnostic_write_byte_account_before']
    a=copy.deepcopy(alias_event);b=copy.deepcopy(alias_event)
    ar,_=old_encode(a,a['actual_diagnostic_write_byte_account_before'],budget)
    br=encode(b,b['actual_diagnostic_write_byte_account_before'],budget)
    require(ar!=br,'explicit generic alias limitation independently demonstrated')
    checks=[]
    for allowed in(0,1,3,10):
        e=event();n=[0]
        def refused():
            n[0]+=1
            if n[0]>allowed:raise TimeoutError('actual pure deadline callback refusal')
        try:encode(e,e['actual_diagnostic_write_byte_account_before'],refused)
        except TimeoutError:checks.append(dict(allowed_calls=allowed,actual_calls=n[0],propagated=True))
        else:raise ValueError('budget refusal swallowed')
    p=read(proof.read_bytes());t=read(tools.read_bytes())
    require(p['status']=='PASS_PURE_SERIALIZATION_ONLY'and p['actual_complete_candidate_and_invalid_records']==86,'author proof scope')
    require(t['closed']is True and t['observed_terminal']is True and t['session_repolled_after_close']is False and t['terminal_tool_return']['exit_code']==0,'saved actual author terminal observed0')
    terminal=read(t['terminal_tool_return']['output'])
    require(terminal['actual_review_pin']==pins[4]and terminal['status']==p['status'],'saved real tool stdout pins actual author proof')
    require([pin(p)for p in inputs]==pins,'all reviewed inputs current and unchanged full EOF')
    oldcontrol=control.read_text();oldsha=pins[0]['sha256'];newsha=pins[1]['sha256']
    target="ADAPTER_SHA='"+oldsha+"'"
    require(oldcontrol.count(target)==1,'sole original control adapter SHA literal')
    newcontrol=oldcontrol.replace(target,"ADAPTER_SHA='"+newsha+"'",1)
    newpath=HERE/'new_genuine_controls.py'
    with newpath.open('x',encoding='utf-8')as stream:stream.write(newcontrol);stream.flush();os.fsync(stream.fileno())
    require(newcontrol.replace("ADAPTER_SHA='"+newsha+"'",target,1)==oldcontrol,'complete 10-control byte inverse exact')
    ast.parse(newcontrol)
    cp=pin(newpath)
    with(HERE/'new_genuine_controls_only_SHA.patch').open('x',encoding='utf-8')as stream:
        stream.write(''.join(difflib.unified_diff(oldcontrol.splitlines(True),newcontrol.splitlines(True),fromfile=str(control),tofile=str(newpath))));stream.flush();os.fsync(stream.fileno())
    oldb=read(binding.read_bytes());order=oldb['case_execution_order']
    require(len(order)==10 and len(set(order))==10,'all ten ordered genuine controls retained')
    newD=BASE/'actual_native_frame_encoder_epoch_recovery_controls_sources_20261011'
    newE=BASE/'actual_native_frame_encoder_epoch_recovery_controls_receipts_20261011'
    ns={case:dict(host=str(ART/('axial-material-frame-encoder-epoch-recovery-'+case+'-20261011-host')),
        output=str(ART/('axial-material-frame-encoder-epoch-recovery-'+case+'-20261011-output')),
        control=str(ART/('axial-material-frame-encoder-epoch-recovery-'+case+'-20261011-control')),
        source=str(newD),receipts=str(newE))for case in order}
    require(not any(Path(v).exists()for row in ns.values()for v in row.values()),'proposed fresh case namespaces currently absent')
    authorbase=Path(oldb['original_N9_controls_Source_binding_pin']['path'])
    currentbase=pin(authorbase);base=read(authorbase.read_bytes())
    missing_roles=[k for k,pinvalue in base['actual_author_Source_contract'].items()if not Path(pinvalue['path']).is_file()]
    contract=dict(schema='EXACT_CURRENT_CONTROL_BINDING_REQUIREMENTS_EXTRACTED_FROM_UNCHANGED_SOURCE_V1',source_only=True,
        control_entry_Source_pin=cp,adapter_Source_pin=pins[1],
        binding_schema='ROOT_FRESH_FRAME_MONITOR_CONTROLS_SOURCE_BINDING_V1',policy=oldb['policy'],original_caps=CAPS,
        actual_control_execution=None,old_controls_qualification_inherited=False,
        original_N9_controls_Source_binding_historical_pin=oldb['original_N9_controls_Source_binding_pin'],
        original_N9_controls_Source_binding_current_file_pin=currentbase,
        currently_missing_author_Source_roles=missing_roles,
        required_actual_author_Source_contract_roles=list(base['actual_author_Source_contract']),
        required_current_pins=['adapter_Source_pin','control_entry_Source_pin','original_N9_controls_Source_binding_pin','owner_helper_Source_pin','actual_stdlib_subprocess_Source_pin','tool_pins'],
        original_source_binding_contract_checks='All author Source owners full EOF current; owner helper equals base author.owner_scope_helper; stdlib/tool pins equal newly current Source binding. Old identities are historical only.',
        review_schema='INDEPENDENT_FRESH_FRAME_MONITOR_CONTROLS_SOURCE_PRELAUNCH_REVIEW_V1',
        required_review=dict(source_only=True,all_checks_passed=True,blockers=[],new_Source_binding_pin='exact final current binding full pin',adapter_Source_pin='exact current adapter pin',control_entry_Source_pin='exact actual entry pin'),
        CLI=['--binding','ACTUAL_CURRENT_BINDING_PATH','--binding-sha256','ACTUAL_CURRENT_BINDING_SHA256','--independent-prelaunch-review','ACTUAL_NEW_CURRENT_REVIEW_PATH','--case','ONE_CASE_IN_ORDER'],
        case_execution_order=order,proposed_fresh_case_namespaces=ns,all_actual_cases_serial=True,
        no_namespace_literals_in_control_Source=True,namespace_changes_are_binding_data_only=True,
        actual_binding_created=False,actual_prelaunch_review_created=False,actual_control_execution_started=False)
    write(HERE/'NEW_GENUINE_CONTROLS_BYTE_INVERSE_AND_BINDING_CONTRACT.json',contract)
    result=dict(schema='INDEPENDENT_DURABLE_ENCODER_SOURCE_AND_PURE_REVIEW_V1',status='PASS_ACTUAL_CALLER_SCOPE_PURE_SOURCE_ONLY',
        reviewer_Source_pin=pins[-1],current_reviewed_input_pins=pins,
        full_original_Source_byte_inverse=True,exactly_two_eight_loop_replacements=True,
        sole_new_pure_helper=True,all_nine_original_caps_unchanged=True,
        PS_lsof_two_disk_accounts_fsync_full_frames_fixed2s_and_original_class_MRO_code_byte_unchanged=True,
        actual_d19_complete_records=actual_count,actual_d19_complete_bytes=actual_bytes,actual_event_counts=events,
        entire_saved_bytes_equal=True,independent_edge_comparisons=len(cases),maximum_original_fixed_point_rounds_observed=maxrounds,
        nonfinite_and_unsupported_refusals=refusal_count,budget_refusals=checks,
        actual_account_keys_are_strings=True,actual_account_is_new_local_and_inserted_once_before_encoding=True,
        standard_JSON_key_types_in_other_payloads_preserved=True,
        exact_integer_fixed_point_reason='For the actual owned account, every field except its one nonnegative integer is fixed. Encoded length is base+decimal_digits(integer). Fixed points converge within the original eight rounds for the original bounded record size; helper computes the same final integer and standard JSON fragments retain insertion order and spelling.',
        budget_reason='Same caller budget checks remain; helper adds checks before fragments, fixed-point work, integer commit and final return. It does not extend, reset or swallow the 2-second deadline; actual OS/account timing still requires real controls.',
        limitations=['Arbitrary extra aliases to the owned account change multiple serialized positions; independent negative comparison demonstrated non-equivalence. The two actual callers create a fresh local account and insert it once. Do not expose this helper as a generic arbitrary-event encoder.',
            'Pure equality and added deadline checks do not qualify real 2-second PS/lsof/full-account/persistence execution; all ten fresh genuine controls still must run.'],
        new_control_Source_pin=cp,control_changes=[dict(kind='literal_SHA_only',occurrences=1,before=oldsha,after=newsha)],
        full_ten_control_Source_byte_inverse=True,namespace_Source_literals_changed=0,
        actual_PS_lsof_or_child_executed=False,actual_genuine_controls_qualified=False,
        actual_fixed2s_observation_qualified=False,actual_native_build_qualified=False,scientific_accuracy_qualified=False,
        actual_goal_achieved=False,actual_elapsed_seconds=time.monotonic()-START)
    write(HERE/'INDEPENDENT_ENCODER_REVIEW.json',result)
    print(json.dumps(dict(status=result['status'],review_pin=pin(HERE/'INDEPENDENT_ENCODER_REVIEW.json'),new_control_Source_pin=cp,
        contract_pin=pin(HERE/'NEW_GENUINE_CONTROLS_BYTE_INVERSE_AND_BINDING_CONTRACT.json'),actual_records=actual_count,
        max_original_rounds=maxrounds,missing_original_author_Source_roles=len(missing_roles),actual_control_or_native_qualification=False),allow_nan=False),flush=True)

if __name__=='__main__':main()
