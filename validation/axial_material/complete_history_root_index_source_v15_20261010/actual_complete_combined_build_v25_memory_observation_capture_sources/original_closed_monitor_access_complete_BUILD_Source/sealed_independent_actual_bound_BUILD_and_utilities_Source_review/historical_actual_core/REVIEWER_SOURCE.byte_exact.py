"""Independent immutable Source / saved-META review. Never imports project code.

All source is parsed as data; large graph, trace, gzip and archive endpoints are
hashed through complete EOF, never decoded. Only fresh private TMP is written.
"""
import argparse
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import sys

CHECKS = []
READ_PINS = {}
DECODED = {}
ART = Path('/Users/wen/spot/validation/artifacts')
BASE = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
Q = BASE/'Root_actual_complete_graph_private_inactive_audit_helper_admission_v25.json'
CAPS = [1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0]

def check(label, value, detail=None):
    passed = type(value) is bool and value is True
    row = dict(label=label, passed=passed)
    if detail is not None: row['detail']=detail
    CHECKS.append(row)
    return passed

def identity(path):
    s=Path(path).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def ordinary(path):
    p=Path(path)
    if not p.is_absolute() or '..' in p.parts: raise ValueError('ordinary absolute path required')
    for a in [*reversed(p.parents),p]:
        i=identity(a)
        if stat.S_ISLNK(i[2]) or (a!=p and not stat.S_ISDIR(i[2])): raise ValueError('alias ancestor: '+str(a))
    return p

def pin(path):
    p=ordinary(path); before=identity(p)
    if not stat.S_ISREG(before[2]): raise ValueError('regular Source / META endpoint required')
    with p.open('rb') as f: sha=hashlib.file_digest(f,'sha256').hexdigest()
    if identity(p)!=before: raise ValueError('changed during complete EOF: '+str(p))
    row=dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)
    old=READ_PINS.get(str(p))
    if old is not None and old!=row: raise ValueError('repeated read changed: '+str(p))
    READ_PINS[str(p)]=row
    return row

def fullpin(row):
    if type(row) is not dict: raise ValueError('full pin not a dict')
    i=row.get('identity',row.get('identity7'))
    if type(i) is not list or len(i)!=7 or any(type(v) is not int for v in i): raise ValueError('seven exact integer identity')
    if 'identity' in row and 'identity7' in row and row['identity']!=row['identity7']: raise ValueError('identity aliases differ')
    if type(row.get('path')) is not str or re.fullmatch('[0-9a-f]{64}',row.get('sha256','')) is None: raise ValueError('full pin path / SHA')
    if not stat.S_ISREG(i[2]) or i[4]<0: raise ValueError('regular pin identity required')
    if 'size_bytes' in row and (type(row['size_bytes']) is not int or row['size_bytes']!=i[4]): raise ValueError('pin size identity differs')
    return dict(path=row['path'],sha256=row['sha256'],size_bytes=i[4],identity=i)

def verify(row,label):
    q=fullpin(row)
    check(label+'.full_EOF_SHA7ID',pin(q['path'])==q)
    return q

def pairs(rows):
    d={}
    for k,v in rows:
        if k in d: raise ValueError('duplicate JSON key '+k)
        d[k]=v
    return d

def reject_constant(v): raise ValueError('nonfinite JSON constant '+v)

def strict(raw):
    v=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=reject_constant)
    def finite(x):
        if type(x) is float and not math.isfinite(x): raise ValueError('nonfinite JSON float')
        if type(x) is dict:
            for a in x.values(): finite(a)
        if type(x) is list:
            for a in x: finite(a)
    finite(v); return v

def read(path):
    p=ordinary(path)
    if p.is_relative_to(ART) and p.name not in ('result.json','ACTUAL_REPORT.json','ACTUAL_PRIVATE_INACTIVE_AUDIT_SNAPSHOT_CONTROLS.json','source_admission.json'):
        raise ValueError('large ART payload decoding forbidden: '+str(p))
    if any(x in p.name for x in ('input_graph','input_creation_python_open_trace')) or p.suffix in ('.gz','.xz','.zip','.sqlite','.db'):
        raise ValueError('large payload decoding forbidden: '+str(p))
    before=pin(p); v=strict(p.read_bytes())
    if pin(p)!=before: raise ValueError('changed during JSON parse')
    DECODED[str(p)]=before
    return v

def typed_equal(a,b,ordered=True):
    if type(a) is not type(b): return False
    if type(a) is dict: return (list(a)==list(b) if ordered else set(a)==set(b)) and all(typed_equal(a[k],b[k],ordered) for k in a)
    if type(a) is list: return len(a)==len(b) and all(typed_equal(x,y,ordered) for x,y in zip(a,b))
    if type(a) is float: return a.hex()==b.hex() and math.isfinite(a) and math.isfinite(b)
    return a==b

def refs(value, result=None):
    if result is None: result={}
    if type(value) is dict:
        if 'path' in value and 'sha256' in value and ('identity' in value or 'identity7' in value):
            q=fullpin(value); old=result.get(q['path'])
            if old is not None and old!=q: raise ValueError('conflicting recursively declared endpoint '+q['path'])
            result[q['path']]=q
        for v in value.values(): refs(v,result)
    elif type(value) is list:
        for v in value: refs(v,result)
    return result

def manifest(root,label):
    root=ordinary(root); m=read(root/'MANIFEST.json')
    files={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
    dirs={'.'}|{str(p.relative_to(root)) for p in root.rglob('*') if p.is_dir()}
    check(label+'.complete_file_set',files==set(m['members'])|{'MANIFEST.json'})
    check(label+'.complete_directory_set',dirs==set(m['directories']))
    check(label+'.member_count_exact_int',type(m['member_count']) is int and m['member_count']==len(m['members']))
    for name,q in m['members'].items():
        check(label+'.member_path.'+name,fullpin(q)['path']==str(root/name))
        verify(q,label+'.member.'+name)
    for name,q in m['directories'].items():
        check(label+'.directory.'+name,identity(root/name)==q)
    check(label+'.source_only',m.get('source_only') is True)
    return m,pin(root/'MANIFEST.json')

def definitions(text):
    return {n.name:ast.get_source_segment(text,n) for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}

def assignments(text):
    return {n.targets[0].id:n.value for n in ast.parse(text).body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}

def inverse(text,rows,label):
    for i,r in enumerate(reversed(rows)):
        check(label+'.inverse_count.'+str(i),type(r['count']) is int and text.count(r['new'])==r['count'])
        text=text.replace(r['new'],r['old'])
    return text

def hunk_inverse(text,rows,label):
    lines=text.splitlines(keepends=True)
    for i,r in enumerate(reversed(rows)):
        start,end=r['new_start0'],r['new_end0']
        check(label+'.hunk_complete_new_lines.'+str(i),lines[start:end]==r['new_full_lines'])
        lines[start:end]=r['old_full_lines']
    return ''.join(lines)

def closed0(t,label,chunk=None):
    check(label+'.strict_integer_EXIT0_CLOSED',type(t) is dict and type(t.get('exit_code')) is int and t['exit_code']==0 and 'session_id' not in t)
    if chunk is not None: check(label+'.actual_chunk',t.get('chunk_id')==chunk)

def checks_report(r,label,count=None):
    check(label+'.all_checks_typed_true',r.get('all_checks_typed_true') is True)
    check(label+'.blockers_empty',r.get('blockers')==[])
    rows=r.get('checks',[])
    check(label+'.exact_count',type(r.get('check_count')) is int and r['check_count']==len(rows) and (count is None or count==len(rows)))
    for i,row in enumerate(rows): check(label+'.saved_check.'+str(i),type(row.get('passed')) is bool and row['passed'] is True)

def false_fields(v,fields,label):
    for k in fields: check(label+'.'+k,v.get(k) is False)

def q_review(bound_inverse,canonical_text):
    q=read(Q); qp=pin(Q)
    check('Q.schema',q['schema']=='AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_INACTIVE_AUDIT_HELPER_ACTUAL_JOINT_ADMISSION_V25')
    check('Q.status',q['status']=='QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V25')
    check('Q.helper_only_scope',q['scope']=='HELPER_METADATA_ORIGINAL_COMPLETE_PROTOCOL_AND_SAME_CURRENT_GRAPH_VERIFIER_ONLY_NO_WHOLE_INPUT_BUILD_NATIVE_OR_SCIENCE')
    false_fields(q,['supervisor_class_or_MRO_modified','profile_used','fresh_production_graph_created','fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','whole_build_qualified','whole_INPUT_admitted','physical_balance_qualified','canonical_wired'],'Q')
    declared=q['Root_finite_joint_META_full_EOF_SHA7ID_verified_unique_inputs']
    owners={fullpin(v)['path']:fullpin(v) for v in declared}
    check('Q.exact310_unique_declared_inputs',len(declared)==len(owners)==310)
    for path,wanted in refs(q).items(): check('Q.recursive_endpoint_owned.'+path,owners.get(path)==wanted)
    for i,wanted in enumerate(declared): verify(wanted,'Q.complete_declared_input.'+str(i))
    protocol=q['full_protocol']
    fields=['original_and_fresh_small_producer_values_types_order_floatbits_exact','all_caller_mutable_identity_and_subtype_attributes_unchanged','accepted_str_subtype_groups','small_codec_rejections','complete_original_graph_counts','complete_old_graph_two_normal_strict_entrances_exact','complete_old_legacy_semantic_sha256','complete_old_wire_content_sha256','complete_new_creation_trace_records','complete_new_creation_trace_actual_attempts','new_creation_trace_not_substituted_into_old_graph','full_json_types_order_floatbits_and_values_retained','default_source_nonmutation']
    check('Q.original_complete13_protocol_fields_order',list(protocol)==fields)
    for k in fields:
        if k in ('accepted_str_subtype_groups','small_codec_rejections','complete_original_graph_counts','complete_old_legacy_semantic_sha256','complete_old_wire_content_sha256','complete_new_creation_trace_records','complete_new_creation_trace_actual_attempts'): continue
        check('Q.original_protocol.'+k,protocol[k] is True)
    for k,v in [('accepted_str_subtype_groups',2),('small_codec_rejections',61),('complete_new_creation_trace_records',63379),('complete_new_creation_trace_actual_attempts',175886)]:
        check('Q.original_protocol_count.'+k,type(protocol[k]) is int and protocol[k]==v)
    for k,v in [('canonical_files',36776),('requirements',237767),('read_trace_records',62332)]: check('Q.original_graph_count.'+k,type(protocol['complete_original_graph_counts'][k]) is int and protocol['complete_original_graph_counts'][k]==v)
    owner=q['private_owner_consume_controls']
    check('Q.complete_original_owner_controls_counts',[len(owner[k]) for k in ['positive_controls','private_guard_rejections','accepted_str_subclass_equivalence_controls','partial_invalid_second_owner_rejections']]==[4,3,2,2])
    false_fields(owner,['new_helper_qualification_created','business_or_science_qualification_created'],'Q.owner')
    snapshot=read(verify(q['private_inactive_audit_snapshot_controls_order_preserved_artifact'],'Q.ordered_snapshot_artifact')['path'])
    check('Q.whole_snapshot_ordered_artifact_exact',typed_equal(snapshot,q['private_inactive_audit_snapshot_controls'],False))
    check('Q.complete_new_snapshot_cases',[len(snapshot[k]) for k in ['positive_controls','private_guard_rejections','last_use_failure_controls']]==[5,13,3])
    check('Q.clone_after_clear_failure_honestly_declared',snapshot['last_use_failure_controls'][2]['private_clone_failure_after_clear_consumption_observed'] is True and snapshot['last_use_failure_controls'][2]['no_transactional_private_mode_promise'] is True)
    false_fields(snapshot,['native_or_numeric_component_executed','helper_qualification_created','business_or_science_qualification_created'],'Q.snapshot')
    fresh=q['complete_current_graph_fresh_verifier']
    check('Q.complete27_return_fields',len(fresh['all27_return_fields'])==27 and len(set(fresh['all27_return_fields']))==27)
    check('Q.same_genuine_full_fresh_read_count',typed_equal(fresh['complete_actual_read_counts'],dict(records=37112,attempts=37112,canonical_files=37111,external_graph_reads=1,no_subprocess_reexecuted=True)))
    for family,name,chunk,count in [(q,'pure','ca2666',55),(fresh,'fresh','d1d77b',42)]:
        core={k:read(verify(family[k],'Q.'+name+'.'+k)['path']) for k in ['actual_root_terminal','actual_controls_summary','actual_host_result','actual_control_report','complete_namespace_manifest','independent_actual_review','independent_actual_review_tool_return','source_manifest','independent_review_retention_record','independent_review_actual_seal']}
        terminal=core['actual_root_terminal']; closed0(terminal['terminal_tool_return'],'Q.'+name+'.Root_terminal',chunk)
        check('Q.'+name+'.closed_observed',terminal['closed'] is True and terminal['actual_tool_terminal_return_observed'] is True and terminal['new_actual_helper_qualification'] is None)
        summary=core['actual_controls_summary']
        check('Q.'+name+'.actual_complete_success',summary['actual_closed'] is True and type(summary['actual_exit_code']) is int and summary['actual_exit_code']==0 and summary['actual_complete_control_success'] is True and summary['actual_failure'] is None)
        checks_report(core['independent_actual_review'],'Q.'+name+'.independent_saved',count)
        watch=core['actual_host_result']['watchdog']
        check('Q.'+name+'.genuine_saved_child_watch',type(watch['returncode']) is int and watch['returncode']==0 and watch['limit_failure'] is None and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True and 0<=watch['sampled_peak_rss_mib']<512)
        for k in ['profile_used','supervisor_class_or_MRO_modified']: check('Q.'+name+'.host_'+k,core['actual_host_result'][k] is False)
        seal=core['independent_review_actual_seal']; closed0(seal.get('terminal_tool_return',seal.get('exec_command_result',seal.get('actual_tool_return'))),'Q.'+name+'.actual_saved_seal')
        check('Q.'+name+'.saved_review_SCOPE',core['independent_actual_review']['source_only'] is True and core['independent_actual_review']['new_actual_helper_qualification'] is None)
        check('Q.'+name+'.original_complete_lossless_source_archives',[x['complete_file_count_including_manifest'] for x in core['source_manifest']['lossless_complete_Source_archives'].values()]==[184,199])
    ca=assignments(canonical_text)
    proofkeys=['FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN']
    external={k:ast.literal_eval(ca[k]) for k in proofkeys}
    for k,w in external.items(): verify(w,'Q.external.'+k)
    qt=read(external[proofkeys[0]]['path']); saved=read(external[proofkeys[1]]['path']); retention=read(external[proofkeys[2]]['path'])
    closed0(qt['terminal_tool_return'],'Q.actual_new_writer','94520a')
    check('Q.actual_new_writer_observed',qt['closed'] is True and qt['actual_tool_terminal_return_observed'] is True and qt['no_closed_session_repoll'] is True)
    raw=strict(qt['terminal_tool_return']['output'].encode())
    check('Q.actual_new_writer_raw_Q_pin',fullpin(raw['actual_metadata_Q'])==qp)
    check('Q.actual_new_writer_complete_scope',[raw[k] for k in ['full_protocol_fields','complete_return_fields','actual_complete_read_count','pure_saved_review_checks','fresh_saved_review_checks']]==[13,27,37112,55,42])
    checks_report(saved,'Q.actual_new_saved48',48)
    check('Q.actual_saved48_status',saved['schema']=='INDEPENDENT_V25_ACTUAL_JOINT_HELPER_Q_SAVED_META_REVIEW_V1' and saved['status']=='PASS_ACTUAL_JOINT_HELPER_Q_METADATA_ONLY')
    check('Q.saved48_Q_pin',fullpin(saved['Root_actual_Q_pin'])==qp)
    check('Q.saved48_writer_terminal_pin',fullpin(saved['Root_actual_Q_writer_terminal_pin'])==fullpin(external[proofkeys[0]]))
    check('Q.saved48_full_scope',saved['qualification_scope']==q['scope'] and saved['actual_saved_helper_metadata_qualification_verified'] is True)
    false_fields(saved,['whole_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','candidate_helper_writer_guard_API_or_numeric_executed','large_graph_trace_gzip_SQLite_material_or_Source_archive_member_payload_read'],'Q.saved48')
    check('Q.saved48_complete_retention',retention['schema']=='ROOT_COMPLETE_FINITE_SOURCE_REVIEW_PACKAGE_RETENTION_V1' and retention['source_only'] is True and retention['complete_original_member_count']==10 and len(retention['complete_original_members'])==10 and retention['new_qualification_created'] is False and retention['helper_guard_business_executed'] is False)
    for rel,r in retention['complete_original_members'].items():
        verify(r['original'],'Q.retained_original.'+rel); verify(r['saved'],'Q.retained_saved.'+rel)
        check('Q.retained_exact_bytes.'+rel,fullpin(r['original'])['sha256']==fullpin(r['saved'])['sha256'])
    qdeps=dict(owners); qdeps[str(Q)]=qp
    for v in [*external.values(),saved,retention,raw]:
        for path,w in refs(v).items():
            check('Q.external_ref_conflicts_absent.'+path,path not in qdeps or qdeps[path]==w)
            qdeps[path]=w
    check('Q.bound_declared_dependency_SCOPE_exact',bound_inverse['all_Q_and_proof_explicit_typed_owner_expected_files']=={path:w['sha256'] for path,w in qdeps.items()})
    return qp,external

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--mother',required=True); ap.add_argument('--bound',required=True); ap.add_argument('--bind-terminal',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    mother=ordinary(a.mother); bound=ordinary(a.bound); output=Path(a.output)
    if not output.is_absolute() or not output.is_relative_to(Path('/private/tmp')) or output.exists(): raise ValueError('fresh private TMP output required')
    if sys.flags.optimize or sys.getprofile() is not None or os.environ.get('PYTHONOPTIMIZE'): raise ValueError('unprofiled nonoptimized review required')
    result={}
    reviewer_source_pin=pin(Path(__file__).absolute())
    try:
        mm,mp=manifest(mother,'mother'); bm,bp=manifest(bound,'bound')
        ns=read(mother/'V25_MONITOR_ACCESS_EXACT_BUILD_NAMESPACE_FULL_BYTE_INVERSES.json')
        original_mf=read(verify(ns['original_frozen_mother_manifest_pin'],'original_mother_manifest')['path'])
        oldroot=Path(ns['original_frozen_mother_manifest_pin']['path']).parent
        manifest(oldroot,'original_complete_mother')
        for i,row in enumerate(ns['complete_changed_member_derivations']):
            rel=row['relative_path']; original_pin=verify(row['original_fullpin'],'namespace.original.'+rel); verify(row['derived_fullpin'],'namespace.derived.'+rel)
            text=(mother/rel).read_text(); restored=hunk_inverse(text,row['full_byte_inverse_hunks'],'namespace.'+rel)
            check('namespace.complete_byte_inverse.'+rel,restored.encode()==Path(original_pin['path']).read_bytes())
            if rel.endswith('.py'): check('namespace.complete_AST_inverse.'+rel,ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(Path(original_pin['path']).read_bytes()),include_attributes=False))
        for rel in ns['unchanged_original_mother_members']:
            check('mother.unchanged_original_member.'+rel,(mother/rel).read_bytes()==(oldroot/rel).read_bytes())
        proof=read(mother/'COMPLETE_SOURCE_INVERSES.json')
        rolepaths={'canonical':'canonical.V25.UNREADY.full.py','prepare_host':'host_and_postclose_templates/prepare_host.V25.UNREADY.full.py','prepare_writer':'host_and_postclose_templates/prepare_writer.V25.UNREADY.full.py','build_host':'host_and_postclose_templates/build_host.V25.UNREADY.full.py','build_writer':'host_and_postclose_templates/build_writer.V25.UNREADY.full.py'}
        for role,rel in rolepaths.items():
            text=(mother/rel).read_text(); restored=inverse(text,proof['exact_finite_transforms'][role],'mother_original.'+role); parent=(mother/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text()
            check('mother.original_complete_byte_inverse.'+role,restored==parent)
            check('mother.original_complete_AST_inverse.'+role,ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False))
        bproof=read(mother/'COMPLETE_SOURCE_BINDER_INVERSES.json')
        for role,name in [('PREP_binder','bind_actual_V25_Q_to_complete_PREP_SOURCE.UNREADY.py'),('BUILD_binder','bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py')]:
            text=(mother/name).read_text()
            if role=='BUILD_binder': text=inverse(text,ns['exact_namespace_transform_rows'][role],'mother_binder_namespace')
            whole=bproof['roles'][role]['whole_exact_inverse']
            check('mother.binder_complete_candidate_match.'+role,text==whole['new'])
            check('mother.binder_complete_original_match.'+role,whole['old']==(mother/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text())
        inv=read(bound/'Root_actual_full_V25_build_Source_binding_inverse.json')
        check('bound.inverse_schema',inv['schema']=='ROOT_V25_ACTUAL_FULL_FIVE_STAGE_BUILD_SOURCE_BINDING_INVERSE_V1')
        check('bound.source_only',inv['source_only'] is True)
        check('bound.original_caps_exact',typed_equal(inv['original_caps'],CAPS))
        false_fields(inv,['candidate_guard_API_compiler_numeric_executed','whole_build_INPUT_native_science_qualified'],'bound')
        check('bound.five_original_stages_retained',inv['all_original_full_five_stages_retained'] is True)
        rolepins={}
        for role,name in [('build_host','combined_build_host.py'),('build_writer','write_actual_build_postclose_META.py')]:
            text=(bound/name).read_text(); template=(mother/rolepaths[role]).read_text(); rp=inv['complete_original_source_inverses'][role]
            restored=inverse(text,rp['READY_to_UNREADY'],'bound_ready.'+role)
            check('bound.complete_template_byte_inverse.'+role,restored==template)
            check('bound.function_bodies_whole_unchanged.'+role,definitions(text)==definitions(template))
            parent=inverse(restored,rp['UNREADY_to_original'],'bound_original.'+role)
            original=(mother/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text()
            check('bound.complete_original_byte_inverse.'+role,parent==original)
            check('bound.complete_original_AST_inverse.'+role,ast.dump(ast.parse(parent),include_attributes=False)==ast.dump(ast.parse(original),include_attributes=False))
            check('bound.inverse_ledger_exact.'+role,rp['UNREADY_to_original']==proof['exact_finite_transforms'][role])
            for k,v in assignments(text).items():
                if k.startswith('FUTURE_V25_'): check('bound.actual_nonplaceholder.'+role+'.'+k,isinstance(v,ast.Constant) and type(v.value) is str and re.fullmatch('[0-9a-f]{64}',v.value) is not None and v.value!='0'*64)
            check('bound.ready_status.'+role,ast.literal_eval(assignments(text)['SOURCE_BINDING_STATUS'])=='READY_V25_ACTUAL_COMPLETE_PREP_AND_SOURCE_BOUND')
            rolepins[role]=pin(bound/name)
        bt=read(a.bind_terminal); tr=bt.get('terminal_tool_return',bt.get('actual_tool_return',bt.get('exec_command_result')))
        if tr is None and 'chunk_id' in bt: tr=bt
        closed0(tr,'Root.actual_Source_bind')
        observed=strict(tr['output'].encode())
        check('Root.actual_bind_source_only_scope',observed['source_only'] is True and observed['project_executed'] is False and observed['full_original_build_retained'] is True)
        for k,w in [('host',rolepins['build_host']),('writer',rolepins['build_writer']),('manifest',bp)]: check('Root.actual_bind_raw_pin.'+k,fullpin(observed[k])==w)
        verify(inv['actual_saved_PREP_peer'],'PREP.actual_saved_peer'); peer=read(inv['actual_saved_PREP_peer']['path']); checks_report(peer,'PREP.independent_saved')
        check('PREP.saved_peer_schema_status',peer['schema']=='INDEPENDENT_V25_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_V1' and peer['status']=='PASS_ACTUAL_COMPLETE_PREP_ONLY')
        for k in ['actual_PREP_closed_EXIT0_verified','actual_metadata_writer_closed_EXIT0_verified','all_complete_scope_verified','actual_PREP_metadata_only']: check('PREP.saved_peer.'+k,peer[k] is True)
        false_fields(peer,['whole_combined_build_qualified','whole_combined_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified'],'PREP.saved_peer')
        check('PREP.saved_peer_byte_exact_copy',(bound/'ACTUAL_SAVED_V25_PREP_PEER.byte_exact.json').read_bytes()==Path(inv['actual_saved_PREP_peer']['path']).read_bytes())
        coupling=[('actual_closed_PREP_summary','actual_Root_PREP_summary_pin'),('actual_Root_closed_terminal','actual_Root_PREP_terminal_pin'),('actual_complete_NAMESPACE','actual_complete_namespace_manifest_pin')]
        for ik,pk in coupling: verify(inv[ik],'PREP.bound_'+ik); check('PREP.three_real_pins_coupled.'+ik,fullpin(inv[ik])==fullpin(peer[pk]))
        summary=read(inv['actual_closed_PREP_summary']['path']); term=read(inv['actual_Root_closed_terminal']['path']); namespace=read(inv['actual_complete_NAMESPACE']['path'])
        check('PREP.actual_success_status',summary['status']=='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD')
        capnames=['whole_wall_cap_seconds','stage_wall_cap_seconds','rss_mib','joint_archive_cap_bytes','history_cap_bytes','free_floor_bytes','threads','children','retries']
        check('PREP.all_original_caps_exact',typed_equal([summary[k] for k in capnames],CAPS))
        check('PREP.actual_measured_bounds',0<summary['child_seconds']<=600 and summary['child_seconds']<=summary['whole_seconds']<1800 and 0<=summary['sampled_peak_rss_mib']<512 and 0<summary['joint_archive_bytes']<2*2**30)
        closed0(term['terminal_tool_return'],'PREP.real_Root_terminal','505668')
        check('PREP.real_terminal_no_repoll',term['closed'] is True and term.get('session_repolled_after_close',False) is False)
        false_fields(summary,['new_five_stage_build_executed','original_five_build_stages_executed','whole_combined_INPUT_admitted','new_native_transport_executed','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','cleanup_performed','goal_complete'],'PREP.summary')
        check('PREP.namespace_no_build_science_credit',namespace['no_build_or_native_credit'] is True)
        expectednames=['axial-material-complete-combined-prepare-host-v25-monitor-access-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-monitor-access-20261010','axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-monitor-access-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-monitor-access-20261010']
        nsroots={row['root']:row for row in namespace['namespaces']}
        check('PREP.full_five_namespace_scope',set(nsroots)=={str(ART/n) for n in expectednames}|{str(BASE/'actual_complete_combined_prepare_v25_monitor_access_sources')})
        for name,row in inv['actual_output_fullpins'].items():
            w=verify(row,'PREP.bound_output.'+name); root=next(Path(r) for r in nsroots if Path(w['path']).is_relative_to(Path(r)))
            check('PREP.namespace_output_coupled.'+name,fullpin(nsroots[str(root)]['files'][str(Path(w['path']).relative_to(root))])==w)
        canonical=verify(namespace['canonical_factory'],'PREP.actual_canonical'); canonical_text=Path(canonical['path']).read_text(); ca=assignments(canonical_text)
        check('PREP.canonical_new_namespace',canonical['path'].endswith('prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_monitor_access.py'))
        for k in ['FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']: check('canonical.future_business_unknown.'+k,isinstance(ca[k],ast.Constant) and ca[k].value is None)
        qp,external=q_review(inv,canonical_text)
        hostassign=assignments((bound/'combined_build_host.py').read_text()); writerassign=assignments((bound/'write_actual_build_postclose_META.py').read_text())
        expect={'FUTURE_V25_ACTUAL_Q_SHA':qp['sha256'],'FUTURE_V25_CANONICAL_SHA':canonical['sha256'],'FUTURE_V25_DECLARATION_SHA':fullpin(inv['actual_output_fullpins']['declaration'])['sha256'],'FUTURE_V25_PREP_SHA':fullpin(inv['actual_output_fullpins']['prep'])['sha256'],'FUTURE_V25_GRAPH_SHA':fullpin(inv['actual_output_fullpins']['graph'])['sha256'],'FUTURE_V25_TRACE_SHA':fullpin(inv['actual_output_fullpins']['trace'])['sha256'],'FUTURE_V25_PREP_SUMMARY_SHA':fullpin(inv['actual_closed_PREP_summary'])['sha256'],'FUTURE_V25_BUILD_HOST_SHA':rolepins['build_host']['sha256']}
        for role,aa in [('build_host',hostassign),('build_writer',writerassign)]:
            for k,v in aa.items():
                if k.startswith('FUTURE_V25_'): check('bound.actual_real_value.'+role+'.'+k,ast.literal_eval(v)==expect[k])
        for q in inv['all_Source_META_actual_fullpins']: verify(q,'bound.full_current_binding_input.'+q['path'])
        # Repeated copies of historic declaration endpoint pins are not parsed.
        # Every originally read current Source / META pin is rechecked below.
        result.update(qualified_template_manifest_pin=mp,qualified_bound_manifest_pin=bp,qualified_actual_bound_Source_manifest_pin=bp,qualified_role_Source_pins=rolepins,actual_bound_build_host_pin=rolepins['build_host'],actual_postclose_META_writer_pin=rolepins['build_writer'],actual_Root_Source_binding_tool_receipt_pin=pin(a.bind_terminal),actual_Root_Source_binding_terminal_pin=pin(a.bind_terminal),actual_Q_pin=qp,actual_canonical_pin=canonical,actual_PREP_summary_pin=fullpin(inv['actual_closed_PREP_summary']),actual_PREP_terminal_pin=fullpin(inv['actual_Root_closed_terminal']),actual_PREP_namespace_pin=fullpin(inv['actual_complete_NAMESPACE']),actual_PREP_saved_peer_pin=fullpin(inv['actual_saved_PREP_peer']),actual_external_Q_proof_pins=external,complete_original_Source_inverse_verified=True,all_original_five_stages_and_caps_retained=True)
    except Exception as error:
        check('review.completed_without_Source_META_contract_exception',False,repr(error))
    for path,wanted in list(READ_PINS.items()):
        try: check('final_unchanged.full_EOF_SHA7ID.'+path,pin(path)==wanted)
        except Exception as error: check('final_unchanged.full_EOF_SHA7ID.'+path,False,repr(error))
    blockers=[r for r in CHECKS if not r['passed']]
    result.update(schema='INDEPENDENT_V25_ACTUAL_BOUND_FULL_BUILD_POSTCLOSE_META_SOURCE_REVIEW_V1',status='PASS_ACTUAL_BOUND_FULL_BUILD_AND_POSTCLOSE_META_SOURCE_ONLY' if not blockers else 'BLOCKED_ACTUAL_BOUND_FULL_BUILD_AND_POSTCLOSE_META_SOURCE_ONLY',source_only=True,scope='COMPLETE_BOUND_FIVE_STAGE_BUILD_SOURCE_AND_ACTUAL_PREP_Q_SAVED_META_ONLY',all_checks_typed_true=not blockers,blockers=blockers,check_count=len(CHECKS),checks=CHECKS,actual_reviewer_Source_pin=reviewer_source_pin,all_actual_source_META_full_EOF_SHA7ID_pins=list(READ_PINS.values()),decoded_Source_META_pins=list(DECODED.values()),whole_build_qualified=False,whole_INPUT_admitted=False,native_RSS_verified=False,physical_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,goal_complete=False,candidate_helper_guard_API_compiler_numeric_executed=False,large_graph_trace_gzip_archive_payload_decoded=False,project_modified=False,actual_BUILD_terminal=None,actual_BUILD_postclose_manifest=None)
    output.mkdir(); (output/'REVIEW.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    (output/'REVIEWER_SOURCE.byte_exact.py').write_bytes(Path(__file__).read_bytes())
    print(json.dumps(dict(status=result['status'],check_count=len(CHECKS),blocker_count=len(blockers),blockers=blockers,review_pin=pin(output/'REVIEW.json'),source_only=True,project_executed=False),allow_nan=False))

if __name__=='__main__': main()
