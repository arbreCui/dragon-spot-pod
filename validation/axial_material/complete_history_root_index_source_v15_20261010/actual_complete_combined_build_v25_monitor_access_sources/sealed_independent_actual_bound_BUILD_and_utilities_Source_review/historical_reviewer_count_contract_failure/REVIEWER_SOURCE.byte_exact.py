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

def current_view(root,label):
    root=ordinary(root); before=identity(root); files={};dirs={'.':before}
    for p in sorted(root.rglob('*')):
        i=identity(p); rel=str(p.relative_to(root))
        if stat.S_ISLNK(i[2]): raise ValueError('Source / META alias in complete view')
        if stat.S_ISREG(i[2]): files[rel]=pin(p)
        elif stat.S_ISDIR(i[2]): dirs[rel]=i
        else: raise ValueError('nonregular Source / META entry')
    check(label+'.all_directories_current',all(identity(root/k)==i for k,i in dirs.items()))
    return dict(root=str(root),files=files,directories=dirs,symlinks={})

def anchor(text,old,label):
    check(label,text.count(old)==1)

def utility_review(root,core):
    mf,mp=manifest(root,'utility_complete')
    check('utility.complete302_files34_subdirs',len(mf['members'])+1==302 and len(mf['directories'])-1==34)
    false_fields(mf,['installer_prelaunch_or_guard_or_candidate_imported_or_executed','compiler_native_material_or_numeric_executed','project_D_E_C_ART_written','Source_or_science_qualification_self_granted','whole_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted'],'utility.MF')
    for k in ['actual_independent_Source_peer','actual_Root_installer_terminal','actual_Root_prelaunch_terminal','actual_BUILD_terminal','actual_native_binary']:check('utility.MF_future_actual_None.'+k,mf[k] is None)
    ast_count=0
    for rel in mf['members']:
        if rel.endswith('.py'):
            ast.parse((root/rel).read_bytes());check('utility.complete_python_AST.'+rel,True);ast_count+=1
    check('utility.complete116_python_AST_count',ast_count==116)
    seal_path=Path(str(root)+'_seal_receipt')/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json'
    seal=read(seal_path);closed0(seal['actual_tool_return'],'utility.author_actual_seal','cffae4')
    check('utility.author_seal_closed_observed',seal['closed'] is True and seal['observed_terminal'] is True and seal['source_only'] is True)
    sealraw=strict(seal['actual_tool_return']['output'].encode())
    check('utility.author_seal_actual_MF_coupling',fullpin(sealraw.get('manifest_pin',sealraw.get('manifest')))==mp)
    provenance=read(root/'ACTUAL_FINITE_SOURCE_INPUT_PROVENANCE.json')
    inverses=read(root/'COMPLETE_V22_UTILITY_SOURCE_BYTE_INVERSES.json')
    contract=read(root/'SOURCE_ONLY_CONTRACT.json')
    check('utility.contract_current_144',contract['current_actual_PREP_fixed_inputs']==144)
    check('utility.contract_original_caps',typed_equal(contract['original_caps'],CAPS))
    false_fields(contract,['whole_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','new_business_or_candidate_executed'],'utility.contract')
    for k in ['future_independent_Source_peer_manifest','future_independent_Source_peer_seal','future_Root_source_install_terminal','future_Root_prelaunch_terminal','future_actual_BUILD_terminal','future_actual_native_binary']: check('utility.future_actual_unknown.'+k,contract[k] is None)
    names={'original_complete_closed_failed_V22_D':('original_complete_closed_failed_V22_build_sources',123),'whole_monitor_access_mother_SOURCE':('complete_monitor_access_BUILD_mother_SOURCE',45),'whole_actual_bound_BUILD_SOURCE':('actual_bound_full_build_SOURCE',5),'whole_actual_PREP_saved_META_peer':('sealed_actual_complete_PREP_saved_META_review',83),'whole_actual_mother_Source_peer':('sealed_independent_monitor_access_BUILD_mother_Source_review',7),'current_actual_PREP_E_small_META':('complete_actual_PREP_receipts_before_build',12)}
    covered={}; copying={}; total=0
    for key,(dest,count) in names.items():
        saved=provenance['full_original_views'][key]
        actual=current_view(Path(saved['root']),'utility.original_full_view.'+key)
        check('utility.original_complete_view_unchanged.'+key,actual==saved)
        copied=provenance['full_byte_retained_copies'][key]
        check('utility.copied_original_root.'+key,copied['original_root']==saved['root'])
        check('utility.complete_copy_file_names.'+key,set(copied['files'])==set(saved['files']) and len(copied['files'])==count)
        check('utility.copied_complete_original_dirs.'+key,{str(p.relative_to(Path(copied['retained_root']))) for p in Path(copied['retained_root']).rglob('*') if p.is_dir()}==set(saved['directories'])-{'.'})
        for rel,w in saved['files'].items():
            verify(w,'utility.original_complete_member.'+key+'/'+rel)
            cw=verify(copied['files'][rel],'utility.retained_complete_member.'+key+'/'+rel)
            check('utility.full_byte_copy_equivalence.'+key+'/'+rel,w['sha256']==cw['sha256'] and fullpin(w)['size_bytes']==cw['size_bytes'])
            check('utility.copy_relative_location.'+key+'/'+rel,cw['path']==str(root/'INPUT_SOURCE_COPIES'/key/rel))
            covered['INPUT_SOURCE_COPIES/'+key+'/'+rel]=dict(destination_relative_path=dest+'/'+rel,original_fullpin=fullpin(w),author_retained_fullpin=cw)
            total+=1
        copying[key]=actual
    check('utility.all275_author_provenance_source_copies_covered',total==275 and set(covered)=={rel for rel in mf['members'] if rel.startswith('INPUT_SOURCE_COPIES/')})
    coverage=read(root/'COMPLETE_275_PROVENANCE_COPY_FUTURE_D_BYTE_COVERAGE.json')
    check('utility.explicit_complete275_coverage_count',type(coverage['complete_count']) is int and coverage['complete_count']==coverage['complete_destination_count']==len(coverage['rows'])==275)
    for i,row in enumerate(coverage['rows']):
        retained=fullpin(row['author_retained_byte_exact_Source_pin']); rel=str(Path(retained['path']).relative_to(root));want=covered[rel]
        check('utility.explicit275_original_match.'+str(i),fullpin(row['original_source_pin'])==want['original_fullpin'])
        check('utility.explicit275_retained_match.'+str(i),retained==want['author_retained_fullpin'])
        check('utility.explicit275_future_destination.'+str(i),row['future_Root_D_destination_path']==str(BASE/'actual_complete_combined_build_v25_monitor_access_sources'/want['destination_relative_path']))
        check('utility.explicit275_future_actual_pin_unknown.'+str(i),row['future_actual_destination_fullpin'] is None)
    check('utility.explicit275_destination_bijection',len({row['future_Root_D_destination_path'] for row in coverage['rows']})==275)
    for path,w in provenance['small_actual_META_pins'].items(): verify(w,'utility.original_small_meta.'+path)
    for i,w in enumerate(provenance['original_genuine_guard_source_pins']): verify(w,'utility.genuine_guard_complete_source.'+str(i))
    rolepins={};texts={}
    for name,row in inverses['roles'].items():
        old=verify(row['original_pin'],'utility.original_role.'+name); retained=verify(row['retained_original_pin'],'utility.original_retained_role.'+name); new=verify(row['new_pin'],'utility.actual_new_role.'+name)
        check('utility.current_role_path.'+name,new['path']==str(root/name))
        text=(root/name).read_text(); original=Path(old['path']).read_text();restored=text
        for i,h in enumerate(reversed(row['hunks'])):
            check('utility.full_inverse_anchor.'+name+'.'+str(i),restored.count(h['new'])==1)
            restored=restored.replace(h['new'],h['old'])
        check('utility.full_byte_inverse.'+name,restored==original and hashlib.sha256(restored.encode()).hexdigest()==old['sha256'])
        check('utility.full_AST_inverse.'+name,ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(original),include_attributes=False))
        check('utility.original_retained_bytes_exact.'+name,retained['sha256']==old['sha256'])
        defs=definitions(text); originals=definitions(original)
        for k,v in originals.items():
            if k!='main': check('utility.original_complete_nonmain_definition.'+name+'.'+k,defs.get(k)==v)
        check('utility.complete_original_nonmain_names.'+name,set(row['original_nonmain_functions_byte_exact'])==set(originals)-{'main'})
        for node in ast.walk(ast.parse(text)):
            if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute): check('utility.no_business_executor_call.'+name+'.'+str(node.lineno),node.func.attr not in ['execute','Popen','system','run','check_call','check_output'])
        rolepins[name]=new; texts[name]=text
    installer=texts['Root_source_installer.py']; pre=texts['Root_prelaunch_checker.py']
    for key in ['peer-manifest','peer-manifest-sha256','peer-seal-receipt','peer-seal-receipt-sha256']: check('utility.future_peer_arguments.'+key,key in installer)
    anchor(installer,"not any(os.path.lexists(p) for p in (D,E,HOST))",'utility.fresh_one_use_D_E_H')
    anchor(installer,"assert old['files']==oldfreeze['complete_files'] and old['directories']==oldfreeze['complete_directories']",'utility.whole_old123_frozen_exact')
    anchor(installer,"review['utility_Source_checks_typed_true'] is True",'utility.requires_actual_independent_utility_PASS')
    anchor(installer,"peer_seal_pin=seal_pair(Path(a.peer_seal_receipt),a.peer_seal_receipt_sha256,pin(peer_path),review_pin)",'utility.requires_true_actual_seal_full_coupling')
    anchor(installer,"for v in (old,mother,bound,saved,mpeer,peer,utility,pre,*prepared):assert snapshot(Path(v['root']))==v",'utility.all_source_copies_unchanged_after_install')
    anchor(installer,"frozen=snapshot(D)",'utility.complete_current_D_freeze')
    anchor(installer,"utility_selected={k:q for k,q in utility['files'].items() if not k.startswith('INPUT_SOURCE_COPIES/')}",'utility_provenance_source_not_double_copied_with_full275_equivalence')
    anchor(pre,"fixed=[original_host_pin(exact(q)) for q in ph['input_sources'][:7]]",'preflight.exact_first7_original_order')
    anchor(pre,"fixed+=[original_host_pin(pin(p)) for p in sorted(D.rglob('*')) if p.is_file()]",'preflight.complete_all_new_D_order')
    anchor(pre,"fixed+=[original_host_pin(exact(summary['actual_declaration'])),original_host_pin(exact(summary['formal_PREP_terminal'])),original_host_pin(exact(summary['actual_complete_input_graph'])),original_host_pin(exact(summary['actual_complete_creation_trace']))]",'preflight.full_original_graph_trace_pins_order')
    anchor(pre,"fixed+=[original_host_pin(pin(p)) for root in (S,T) for p in sorted(root.rglob('*')) if p.is_file()]",'preflight.complete_original_S_T_order_and_repeats')
    anchor(pre,"fixed+=[original_host_pin(exact(summary['actual_root_terminal'])),original_host_pin(summary_pin),original_host_pin(exact(ph['original_helper'])),original_host_pin(exact(ph['resource_factory']))]",'preflight.exact_terminal_summary_helper_resource_order')
    anchor(pre,"assert all(set(q)=={'path','sha256','identity'} for q in fixed)",'preflight.original_host3key_full_order_not_deduplicated')
    anchor(pre,"full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)",'preflight.original_genuine_MRO')
    anchor(pre,"resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)",'preflight.original_genuine_dynamic_resource_class_caps')
    anchor(pre,"now['files']=={**v['files'],out.name:own_pin}",'preflight.exact_only_self_E_append')
    anchor(pre,"now['directories']['.'][:3]==v['directories']['.'][:3]",'preflight.E_root_dev_inode_mode_stable_nlink_append_allowed')
    check('preflight.E_root_nlink_not_immutably_claimed',"now['directories']['.'][:4]" not in pre)
    check('preflight.own_frozen_source_verified',"Path(__file__)" in pre and "Root_prelaunch_checker.py" in pre and "freeze['complete_files']" in pre)
    old_imports=[ast.get_source_segment(Path(inverses['roles']['Root_prelaunch_checker.py']['original_pin']['path']).read_text(),n) for n in ast.parse(Path(inverses['roles']['Root_prelaunch_checker.py']['original_pin']['path']).read_text()).body if isinstance(n,(ast.Import,ast.ImportFrom))]
    check('utility_original_imports_bytes_retained',all(x in pre for x in old_imports))
    summary=read(BASE/'actual_complete_combined_prepare_v25_monitor_access_receipts/Root_actual_complete_combined_prepare_summary.json')
    ph=read(summary['actual_host_result']['path']); originals=ph['input_sources']+[ph['original_helper'],ph['resource_factory']]
    check('preflight.all144_original_order_and_repeats_available',len(ph['input_sources'])==142 and len(originals)==144)
    for i,w in enumerate(originals): verify(w,'preflight.complete144_current_fixed_input.'+str(i))
    binding=read(core['actual_Root_Source_binding_tool_receipt_pin']['path']); import shlex
    argv=shlex.split(binding['actual_launch_arguments']['cmd'])
    check('Root.actual_Source_binding_true_CLOSED_observed',binding['closed'] is True and binding['source_only'] is True)
    check('Root.actual_Source_binding_args_actual_mother',argv[2]==str(Path(core['qualified_template_manifest_pin']['path']).parent/'bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py'))
    check('Root.actual_Source_binding_args_actual_bound',argv[argv.index('--destination')+1]==str(Path(core['qualified_actual_bound_Source_manifest_pin']['path']).parent))
    check('Root.actual_Source_binding_args_actual_Q',argv[argv.index('--actual-Q-sha256')+1]==core['actual_Q_pin']['sha256'])
    check('Root.actual_Source_binding_args_actual_canonical',argv[argv.index('--actual-canonical-sha256')+1]==core['actual_canonical_pin']['sha256'])
    return dict(actual_Source_utility_manifest_pin=mp,actual_Root_source_installer_Source_pin=rolepins['Root_source_installer.py'],actual_Root_prelaunch_checker_Source_pin=rolepins['Root_prelaunch_checker.py'],utility_all275_author_provenance_bytes_destination_equivalence=covered,utility_original_nonmain_definitions_preserved=True,utility_full_byte_AST_inverses_verified=True,utility_all144_original_PREP_inputs_current_full_EOF_SHA7ID_verified=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--utility',required=True);ap.add_argument('--core',required=True);ap.add_argument('--core-tool',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    output=Path(a.output)
    if not output.is_absolute() or not output.is_relative_to(Path('/private/tmp')) or output.exists():raise ValueError('fresh private TMP')
    original_source_pin=pin(Path(__file__).absolute()); result={}
    try:
        core=read(a.core); checks_report(core,'historical_actual_core',23253)
        check('historical_core_status_actual',core['schema']=='INDEPENDENT_V25_ACTUAL_BOUND_FULL_BUILD_POSTCLOSE_META_SOURCE_REVIEW_V1' and core['status']=='PASS_ACTUAL_BOUND_FULL_BUILD_AND_POSTCLOSE_META_SOURCE_ONLY')
        ct=read(a.core_tool); closed0(ct['actual_tool_return'],'actual_core_review','6da22e')
        raw=strict(ct['actual_tool_return']['output'].encode());check('actual_core_raw_report_fullpin',fullpin(raw['review_pin'])==pin(a.core))
        result.update(utility_review(ordinary(a.utility),core))
    except Exception as error:check('utility_completed_without_contract_exception',False,repr(error))
    for path,w in list(READ_PINS.items()):
        try:check('addon_final_unchanged.full_EOF_SHA7ID.'+path,pin(path)==w)
        except Exception as error:check('addon_final_unchanged.full_EOF_SHA7ID.'+path,False,repr(error))
    blockers=[x for x in CHECKS if not x['passed']]
    result.update(schema='INDEPENDENT_V25_COMPLETE_BUILD_UTILITY_SOURCE_ADDON_REVIEW_V1',status='PASS_UTILITY_SOURCE_ONLY' if not blockers else 'BLOCKED_UTILITY_SOURCE_ONLY',source_only=True,all_checks_typed_true=not blockers,check_count=len(CHECKS),checks=CHECKS,blockers=blockers,original_bound_Source_review_report_pin=pin(a.core),actual_core_review_tool_pin=pin(a.core_tool),actual_reviewer_Source_pin=original_source_pin,full_current_Source_META_input_pins=list(READ_PINS.values()),candidate_guard_API_compiler_numeric_executed=False,whole_build_INPUT_native_science_qualified=False,project_modified=False)
    output.mkdir();(output/'REVIEW.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');(output/'REVIEWER_SOURCE.byte_exact.py').write_bytes(Path(__file__).read_bytes())
    print(json.dumps(dict(status=result['status'],check_count=len(CHECKS),blockers=blockers,review_pin=pin(output/'REVIEW.json'),source_only=True,project_executed=False),allow_nan=False))

if __name__=='__main__':main()
