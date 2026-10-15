"""Actual pure serialization evidence only; never a Native or resource PASS.

No adapter import, PS/lsof, child, compiler, numeric solver, directory scan,
resource method, journal append, or deadline extension is performed here.
"""
import ast
import collections
import copy
import difflib
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import stat
import struct
import sys
import time

HERE=Path(__file__).resolve().parent
ORIGINAL=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_invalid_prepost_d19_monitor_controls_sources_20261011/fresh_frame_observation_adapter.py')
JOURNAL=Path('/Users/wen/spot/validation/artifacts/axial-material-grouped-native-AB-d19-v2-20261011-host/runtime/ACTUAL_FAILURE_ONLY_MONITOR_EVENTS.jsonl')
THREAD_KEYS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
STARTED=time.monotonic()
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)

def need(value,message):
    if type(value)is not bool or not value:raise ValueError(message)

def bounded():
    need(time.monotonic()-STARTED<600,'pure verifier original metadata wall limit')
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform!='darwin':peak*=1024
    need(peak<512*2**20,'pure verifier original 512 MiB self limit')

def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(path):
    path=Path(path);before=identity(path.lstat())
    need(path.is_absolute()and all(not q.is_symlink()for q in(path,*path.parents))
        and stat.S_ISREG(before[2])and before[3]==1,'real singlelink complete source or input')
    digest=hashlib.sha256();size=0
    with path.open('rb')as stream:
        need(identity(os.fstat(stream.fileno()))==before,'input opened identity')
        while True:
            bounded();raw=stream.read(2**20)
            if not raw:break
            digest.update(raw);size+=len(raw)
        need(identity(os.fstat(stream.fileno()))==before,'input EOF identity')
    need(identity(path.lstat())==before and size==before[4],'complete input unchanged')
    return dict(path=str(path),size_bytes=size,sha256=digest.hexdigest(),identity=before)

def strict(raw):
    def pairs(items):
        out={}
        for key,value in items:
            need(key not in out,'no duplicate saved JSON keys');out[key]=value
        return out
    return json.loads(raw,object_pairs_hook=pairs,
        parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))

def original_size_loop(event,account,budget):
    raw=None
    for serialization in range(8):
        budget()
        candidate=(json.dumps(event,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8')
        size=len(candidate)
        if account['additional_record_bytes']==size:
            raw=candidate;break
        account['additional_record_bytes']=size
    need(raw is not None and len(raw)==account['additional_record_bytes'],
        'original complete exact self-accounted JSON-line size stabilized')
    return raw

def synthetic(padding='',extra=None):
    account=dict(actual_regular_joint_bytes=0,additional_record_bytes=0,
        previous_complete_open_unlinked_bytes=0,
        actual_original_history_check=dict(artifact_bytes=0,disk_free_bytes=10*2**30),
        external_D_E_bytes=0)
    event=dict(event='fresh_frame_invalid_not_resource_PASS',padding=padding,
        actual_diagnostic_write_byte_account_before=account,
        failed_frame_accepted=False,resource_PASS=False)
    if extra is not None:event['extra']=extra
    return event

def compare(event,encoder,check_saved=None):
    first=copy.deepcopy(event);second=copy.deepcopy(event)
    a=first['actual_diagnostic_write_byte_account_before']
    b=second['actual_diagnostic_write_byte_account_before']
    a['additional_record_bytes']=0;b['additional_record_bytes']=0
    entered=time.monotonic();old=original_size_loop(first,a,bounded)
    old_seconds=time.monotonic()-entered
    entered=time.monotonic();new=encoder(second,b,bounded)
    new_seconds=time.monotonic()-entered
    need(old==new,'complete UTF8 bytes differ from original eight-loop algorithm')
    need(first==second and len(new)==b['additional_record_bytes'],
        'exact original output fields and self-accounted integer')
    if check_saved is not None:need(new==check_saved,'actual complete saved frame bytes changed')
    return dict(size_bytes=len(new),sha256=hashlib.sha256(new).hexdigest(),
        original_loop_seconds=old_seconds,new_encoder_seconds=new_seconds)

def main():
    need(os.environ.get('PYTHONDONTWRITEBYTECODE')=='1'
        and all(os.environ.get(k)=='1'for k in THREAD_KEYS),'exact single-thread pure verifier environment')
    files=[ORIGINAL,HERE/'fresh_frame_observation_adapter.py',HERE/'frame_encoder_only.patch',
        HERE/'added_pure_encoder_Source.py',Path(__file__).resolve(),JOURNAL]
    before=[pin(p)for p in files]
    need(before[0]['sha256']=='a2b507e0f5e5470c227484f1d8a1e63367aed2313cb15695a9c46b57a2d444cc',
        'actual original adapter SHA')
    original=ORIGINAL.read_text();candidate=files[1].read_text();helper=files[3].read_text()
    old="""            raw=None
            for serialization in range(8):
                budget()
                candidate=(json.dumps(event,ensure_ascii=False,allow_nan=False)+'\\n').encode('utf-8')
                size=len(candidate)
                if account['additional_record_bytes']==size:
                    raw=candidate;break
                account['additional_record_bytes']=size
"""
    new='            raw=complete_frame_self_accounted_UTF8(event,account,budget)\n'
    need(candidate.count(helper)==1 and candidate.count(new)==2,'one pure helper and exactly two loop replacements')
    inverse=candidate.replace(helper,'',1).replace(new,old)
    need(inverse==original,'byte-exact whole original Source inverse')
    expected_patch=''.join(difflib.unified_diff(original.splitlines(True),candidate.splitlines(True),
        fromfile=str(ORIGINAL),tofile=str(files[1])))
    need(files[2].read_text()==expected_patch,'durable patch is exact whole-source diff')
    tree=ast.parse(candidate);orig_tree=ast.parse(original)
    definitions={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
    original_definitions={n.name:n for n in orig_tree.body if isinstance(n,ast.FunctionDef)}
    need(set(definitions)==set(original_definitions)|{'complete_frame_self_accounted_UTF8'},
        'exact sole new top-level function')
    original_caps=next(n.value for n in orig_tree.body if isinstance(n,ast.Assign)
        and any(isinstance(t,ast.Name)and t.id=='CAPS'for t in n.targets))
    need(eval(compile(ast.Expression(original_caps),'<original caps>','eval'),{})==CAPS,
        'all nine original caps unchanged')
    module=ast.Module(body=[definitions['require'],definitions['complete_frame_self_accounted_UTF8']],type_ignores=[])
    env={'json':json};exec(compile(module,'<pure extracted encoder only>','exec'),env)
    encoder=env['complete_frame_self_accounted_UTF8']
    rows=[];other=[];counts=collections.Counter();raw_bytes=0
    with JOURNAL.open('rb')as stream:
        for raw in stream:
            bounded();event=strict(raw);counts[event['event']]+=1
            if event['event']in('fresh_frame_complete_candidate','fresh_frame_invalid_not_resource_PASS'):
                result=compare(event,encoder,raw);result.update(sequence=event['sequence'],event=event['event'])
                need(event['failed_frame_accepted']is False and event['resource_PASS']is False,
                    'candidate and invalid saved events never grant resource PASS')
                rows.append(result);raw_bytes+=len(raw)
            else:other.append(dict(sequence=event['sequence'],event=event['event'],size_bytes=len(raw)))
    need(len(rows)==86 and [r['sequence']for r in rows]==list(range(1,87))
        and counts['fresh_frame_complete_candidate']==65
        and counts['fresh_frame_invalid_not_resource_PASS']==21,
        'all actual 86 complete candidate and invalid frames without selection holes')
    boundary=[]
    base=compare(synthetic(),encoder)['size_bytes']
    for power in (3,4,5,6):
        for delta in range(-4,5):
            padding=max(0,10**power-base+delta)
            result=compare(synthetic('x'*padding),encoder)
            result.update(decimal_boundary=10**power,delta=delta);boundary.append(result)
    unicode=compare(synthetic('中文🙂\n\r\t\"\\é𝄞',dict(
        signed_zero=-0.0,positive_zero=0.0,minimum_subnormal=5e-324,
        largest_finite=sys.float_info.max,nested={'中文':['🙂',None,True,False]})),encoder)
    e=synthetic(extra=-0.0);raw=encoder(e,e['actual_diagnostic_write_byte_account_before'],bounded)
    need(b'"extra": -0.0'in raw and struct.pack('>d',strict(raw)['extra'])==struct.pack('>d',-0.0),
        'signed zero bytes and IEEE sign retained')
    nonfinite=[]
    for value in (float('nan'),float('inf'),-float('inf')):
        for name,fn in (('original',original_size_loop),('new',encoder)):
            e=synthetic(extra=value)
            try:fn(e,e['actual_diagnostic_write_byte_account_before'],bounded)
            except ValueError:nonfinite.append(dict(encoder=name,refused=True))
            else:raise ValueError('nonfinite serialization admitted')
    class ActualBudgetRefusal(RuntimeError):pass
    deadlines=[]
    for allowed_calls in (0,1,3,10):
        e=synthetic();calls=[0];snapshot=e['actual_diagnostic_write_byte_account_before']['additional_record_bytes']
        def refuse():
            calls[0]+=1
            if calls[0]>allowed_calls:raise ActualBudgetRefusal('same fixed deadline has expired')
        try:encoder(e,e['actual_diagnostic_write_byte_account_before'],refuse)
        except ActualBudgetRefusal:
            need(e['actual_diagnostic_write_byte_account_before']['additional_record_bytes']==snapshot,
                'budget refusal before integer commit is not swallowed or retried')
            deadlines.append(dict(allowed_calls=allowed_calls,actual_calls=calls[0],refusal_propagated=True))
        else:raise ValueError('deadline/control refusal swallowed')
    # Count actual encoder work: the complete_frame value is serialized once,
    # and the full event is never passed to dumps again. No payload stub used.
    with JOURNAL.open('rb')as stream:e=strict(next(stream))
    calls=[]
    class CountJSON:
        @staticmethod
        def dumps(value,**kwargs):
            calls.append(dict(keys=list(value)if type(value)is dict else None,
                complete_frame='complete_frame'in value if type(value)is dict else False))
            return json.dumps(value,**kwargs)
    env['json']=CountJSON
    count_raw=encoder(e,e['actual_diagnostic_write_byte_account_before'],bounded)
    env['json']=json
    need(sum(r['complete_frame']for r in calls)==1 and all(len(r['keys'])==1 for r in calls),
        'complete frame encoded once and no full-event dumps repeat')
    need(len(count_raw)==e['actual_diagnostic_write_byte_account_before']['additional_record_bytes'],
        'counted encoder retains complete exact byte accounting')
    after=[pin(p)for p in files]
    need(before==after,'all complete Source, patch, verifier, and actual log pins unchanged')
    bounded();peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform!='darwin':peak*=1024
    result=dict(schema='ACTUAL_DURABLE_FRAME_ENCODER_PURE_SERIALIZATION_REVIEW_V1',
        status='PASS_PURE_SERIALIZATION_ONLY',complete_input_pins=after,
        byte_exact_original_Source_inverse=True,sole_new_pure_helper=True,
        exactly_two_full_event_eight_loop_replacements=True,original_caps=CAPS,
        original_PS_lsof_prepost_disk_accounts_persistence_and_fixed2s_budget_unchanged=True,
        actual_saved_event_log_total_records=sum(counts.values()),
        actual_complete_candidate_and_invalid_records=86,
        actual_complete_candidate_and_invalid_bytes=raw_bytes,
        actual_cleanup_records_left_unchanged=other,actual_record_comparisons=rows,
        UTF8_float_signed_zero_control=unicode,digit_boundary_controls=boundary,
        nonfinite_refusals=nonfinite,deadline_refusals=deadlines,
        actual_encoder_pair_dump_count=len(calls),actual_complete_frame_value_encodings=1,
        actual_full_event_repeated_encodings=0,original_algorithm_bytes_equal_on_every_record=True,
        actual_elapsed_seconds=time.monotonic()-STARTED,actual_self_peak_rss_bytes=peak,
        actual_PS_lsof_or_native_child_executed=False,actual_compiler_or_numeric_child_executed=False,
        actual_native_complete_build_qualified=False,actual_fresh2s_observation_window_qualified=False,
        actual_material_production_or_online_qualified=False,scientific_accuracy_qualified=False,
        actual_goal_achieved=False)
    path=HERE/'ACTUAL_PURE_SERIALIZATION_REVIEW.json'
    with path.open('x',encoding='utf-8')as stream:json.dump(result,stream,indent=2,ensure_ascii=False,allow_nan=False);stream.write('\n')
    print(json.dumps(dict(status=result['status'],actual_review_pin=pin(path),
        actual_frame_record_count=86,actual_whole_log_record_count=sum(counts.values()),
        actual_complete_frame_bytes=raw_bytes,byte_exact_whole_Source_inverse=True,
        original_algorithm_bytes_equal_on_every_record=True,
        original_PS_lsof_prepost_disk_accounts_persistence_and_fixed2s_budget_unchanged=True,
        actual_native_complete_build_qualified=False,actual_fresh2s_observation_window_qualified=False,
        actual_goal_achieved=False),allow_nan=False),flush=True)

if __name__=='__main__':main()
