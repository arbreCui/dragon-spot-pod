"""Finite actual two-role READY Source binding review, no candidate execution.
Qualified single-reader/P4/V3 Source semantics are prerequisites. Physical graph,
trace, gzip and material payloads are current7ID only, with Root EOF provenance.
The one exact declaration META is independently bounded to 16MiB before EOF.
"""
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import sys
import tempfile

BOUND=Path('/private/tmp/spot_Root_actual_V25_memory_observation_capture_BUILD_bound_Source_20261011')
AUTHOR=Path('/private/tmp/axmat_P4_BUILD_exact_declaration_reader_minimal_UNREADY_Source_66od7kgz')
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
WRAPPER=B/'Root_actual_memory_observation_capture_BUILD_Source_binding_reader_fixed_tool_terminal_return_20261011.json'
RESOURCE=Path('/Users/wen/miniforge3/envs/openmc-dev/lib/python3.12/lib-dynload/resource.cpython-312-darwin.so')
DECLARATION=Path('/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-memory-observation-capture-20261010/declaration.json')
MAX=16*2**20
CHECKS=[];BLOCKERS=[];FULL={};ROOT_PAYLOAD={};REGISTRY={};SOURCE_AST={}
def ids(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def ident(p):return ids(Path(p).lstat())
def ck(name,v,e=None):
    assert type(v)is bool and name not in {c['check']for c in CHECKS}
    d=dict(check=name,passed=v)
    if e is not None:d['evidence']=e
    CHECKS.append(d)
    if not v:BLOCKERS.append(dict(check=name,reason=e))
    return v
def read(p):
    p=Path(p);i=ident(p)
    assert p.is_absolute()and p.resolve()==p and stat.S_ISREG(i[2])and 0<=i[4]<=MAX
    if p==RESOURCE:assert i[3]>=1 and i[4]==53552
    else:assert i[3]==1
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        assert ids(os.fstat(fd))==i
        rem=MAX+1;parts=[]
        while rem:
            b=os.read(fd,min(rem,65536))
            if not b:break
            parts.append(b);rem-=len(b)
        b=b''.join(parts);assert len(b)<=MAX and len(b)==i[4]and ids(os.fstat(fd))==i and ident(p)==i
    finally:os.close(fd)
    q=dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=i)
    if p==RESOURCE:assert q['sha256']=='cbd0358d5dfb6a5271a7e645118a36d0537b49e84452a2bcd7d26a73eb131164'
    if str(p)in FULL:assert FULL[str(p)]==q
    FULL[str(p)]=q
    if p.suffix=='.py':SOURCE_AST[str(p)]=hashlib.sha256(ast.dump(ast.parse(b),include_attributes=False).encode()).hexdigest()
    return b,q
def strict(b):
    def pairs(rows):
        d={}
        for k,v in rows:
            if k in d:raise ValueError('duplicate META key')
            d[k]=v
        return d
    def bad(x):raise ValueError('nonfinite constant '+x)
    d=json.loads(b.decode('utf8'),object_pairs_hook=pairs,parse_constant=bad)
    def finite(x):
        if type(x)is float:assert math.isfinite(x)
        elif type(x)is dict:
            for v in x.values():finite(v)
        elif type(x)is list:
            for v in x:finite(v)
    finite(d);return d
def collect(d):
    if type(d)is dict:
        i=d.get('identity',d.get('identity7'))
        if type(d.get('path'))is str and type(d.get('sha256'))is str and type(i)is list and len(i)==7 and all(type(x)is int for x in i):
            q=dict(path=d['path'],sha256=d['sha256'],size_bytes=d.get('size_bytes',i[4]),identity=i)
            if type(q['size_bytes'])is int and q['size_bytes']==i[4]:REGISTRY.setdefault((q['path'],q['sha256']),[]).append(q)
        for v in d.values():collect(v)
    elif type(d)is list:
        for v in d:collect(v)
def jr(p):
    b,q=read(p);d=strict(b);collect(d);return d,q
def exact(q):
    b,p=read(q['path']);assert p==q;return b
def fullpin(q):
    assert type(q)is dict and type(q.get('path'))is str and type(q.get('sha256'))is str
    i=q.get('identity',q.get('identity7'))
    assert type(i)is list and len(i)==7 and all(type(v)is int for v in i)
    if 'identity'in q and 'identity7'in q:assert q['identity']==q['identity7']
    assert stat.S_ISREG(i[2])and i[4]>=0
    if 'size_bytes'in q:assert type(q['size_bytes'])is int and q['size_bytes']==i[4]
    return dict(path=q['path'],sha256=q['sha256'],size_bytes=i[4],identity=i)
def closed(d):
    t=d.get('terminal_tool_return',d.get('actual_tool_return',d.get('exec_command_result')))
    return d.get('closed')is True and d.get('observed_terminal')is True and type(t)is dict and type(t.get('exit_code'))is int and t['exit_code']==0 and 'session_id'not in t and d.get('session_repolled_after_close',False)is False
def astsame(a,b):return ast.dump(ast.parse(a),include_attributes=False)==ast.dump(ast.parse(b),include_attributes=False)
def definitions(s):
    return [(n.name,ast.get_source_segment(s,n),ast.dump(n,include_attributes=False))for n in ast.walk(ast.parse(s))if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
def literal_values(s):
    out={}
    for n in ast.parse(s).body:
        if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            try:out[n.targets[0].id]=ast.literal_eval(n.value)
            except (ValueError,TypeError):pass
    return out
def reverse(s,rows):
    counts=[]
    for q in reversed(rows):
        assert set(q)=={'label','old','new','count'}and type(q['count'])is int and q['count']>0
        n=s.count(q['new']);assert n==q['count'];counts.append(dict(label=q['label'],actual=n,expected=q['count']))
        s=s.replace(q['new'],q['old'])
    return s,counts
def payload_id(q,origin):
    p=Path(q['path']);i=ident(p)
    ok=p.is_absolute()and p.resolve()==p and stat.S_ISREG(i[2])and i==q['identity']and q['size_bytes']==i[4]
    ROOT_PAYLOAD[str(p)]=dict(Root_actual_complete_EOF_fullpin=q,current7ID=i,independently_read_to_EOF=False,full_EOF_owner=origin)
    return ok
def physical(p,size):
    n=Path(p).name.lower()
    return size>MAX or n.endswith(('.gz','.gzip','.h5','.hdf5','.zip','.tar','.npy','.npz'))or n in {'input_graph.json','input_creation_python_open_trace.json'}or (Path(p).suffix!='.py'and any(w in n for w in ('wire_graph','saved_graph','creation_trace.encoded','material_payload')))
def write(p,b):
    fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    try:
        off=0
        while off<len(b):n=os.write(fd,b[off:]);assert n>0;off+=n
        os.fsync(fd)
    finally:os.close(fd)
def wj(p,d):write(p,(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())

def main():
    out=Path(tempfile.mkdtemp(prefix='axmat_P4_ACTUAL_BOUND_BUILD_Source_INDEPENDENT_',dir='/private/tmp'))
    src,sp=read(Path(__file__));write(out/'REVIEWER_EXECUTED_SOURCE.py',src)
    mf=None;hp=None;wp=None;rp=None;view={};inverse_results={};qmeta={};payloads={}
    try:
        m,mf=jr(BOUND/'MANIFEST.json');ck('actual_bound_manifest_expected_SHA',mf['sha256']=='04937e4bd32ef5f7f518bf3aefce9c633825ca95295f2af39159d50c725a3e33',mf)
        files={};raw={};dirs={'.':ident(BOUND)}
        for f in sorted(BOUND.rglob('*')):
            i=ident(f);assert not stat.S_ISLNK(i[2]);rel=str(f.relative_to(BOUND))
            if stat.S_ISDIR(i[2]):dirs[rel]=i
            else:raw[rel],files[rel]=read(f)
        view=dict(root=str(BOUND),files=files,directories=dirs,symlinks={})
        ck('complete_actual_5file_1dir_manifest_domain_and7IDs',len(files)==5 and len(dirs)==1 and set(files)==set(m['members'])|{'MANIFEST.json'}and dirs==m['directories']and type(m['member_count'])is int and m['member_count']==4 and m['source_only']is True and m['executed_project']is False)
        for rel,q in m['members'].items():ck('actual_complete_bound_member_EOF_SHA7ID:'+rel,q==files[rel],q)
        hp=files['combined_build_host.py'];wp=files['write_actual_build_postclose_META.py']
        ck('actual_host_and_writer_expected_Source_SHAs',hp['sha256']=='b2054db37dca3fd3a0e22d2ace74498c6e6745f7a10c82253124e7de4e188816'and wp['sha256']=='984a149cb3b250e1f0d5da48f3b32c8e846914f8e685444d0013186bac0d334e')
        rootwrapper,rp=jr(WRAPPER);ck('real_Root_c787b4_CLOSED_strict_int0_no_session',closed(rootwrapper)and rootwrapper['terminal_tool_return']['chunk_id']=='c787b4',rp)
        observed=strict(rootwrapper['terminal_tool_return']['output'].encode())
        ck('real_Root_terminal_outputs_exact_actual_bound_package_pins',observed['manifest']==mf and observed['host']==hp and observed['writer']==wp and observed['source_only']is True and observed['project_executed']is False and rootwrapper['actual_BUILD_or_candidate_executed']is False and rootwrapper['new_native_or_scientific_qualification']is False)
        inv=strict(raw['Root_actual_full_V25_build_Source_binding_inverse.json']);collect(inv)
        ck('actual_inverse_only_Source_binding_scope',inv['source_only']is True and inv['candidate_guard_API_compiler_numeric_executed']is False and inv['whole_build_INPUT_native_science_qualified']is False and inv['all_original_full_five_stages_retained']is True and inv['original_caps']==[1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0]and all(type(v)is int for v in inv['original_caps']))
        am,ap=jr(AUTHOR/'MANIFEST.json');ck('qualified_author_current_MF_unchanged',ap['sha256']=='cedc1311c69b4e09d589a145a0757288658585c8939186a5cfc29fa682b506fe')
        prior,priorpin=jr(Path('/private/tmp/axmat_P4_BUILD_DECLARATION_READER_INDEPENDENT_64gzkt4i/REVIEW.json'))
        ck('actual_single_reader_331_qualified_Source_prerequisite_same_author',prior['qualified_complete_Source_manifest_pin']==ap and prior['schema']=='INDEPENDENT_V25_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_REVIEW_V1'and prior['status']=='PASS_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_ONLY_UNREADY_NO_EXECUTION'and prior['all_checks_typed_true']is True and prior['blockers']==[])
        proof,proofpin=jr(AUTHOR/'COMPLETE_SOURCE_INVERSES.json')
        texts={};globals_by_role={}
        for role,fname in {'build_host':'combined_build_host.py','build_writer':'write_actual_build_postclose_META.py'}.items():
            s=raw[fname].decode();texts[role]=s;globals_by_role[role]=literal_values(s)
            b,tp=read(AUTHOR/'host_and_postclose_templates'/(role+'.V25.UNREADY.full.py'));template=b.decode()
            rows=inv['complete_original_source_inverses'][role];unready,c1=reverse(s,rows['READY_to_UNREADY']);original,c2=reverse(unready,rows['UNREADY_to_original']);parent,pp=read(AUTHOR/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py'))
            ck('whole_READY_to_current_qualified_UNREADY_bytes_AST:'+role,unready==template and astsame(unready,template),c1)
            ck('actual_consumed_UNREADY_inverse_rows_same_current_proof:'+role,rows['UNREADY_to_original']==proof['exact_finite_transforms'][role])
            ck('whole_READY_to_OriginalParent_bytes_AST:'+role,original.encode()==parent and astsame(original,parent),c2)
            ck('all_functions_classes_complete_bytes_AST_unchanged_by_binding:'+role,definitions(s)==definitions(template))
            ck('READY_status_and_only_literal_global_binding_hunks:'+role,globals_by_role[role]['SOURCE_BINDING_STATUS']=='READY_V25_ACTUAL_COMPLETE_PREP_AND_SOURCE_BOUND'and all(q['count']==1 and (q['label'].startswith('actual_FUTURE_V25_')or q['label']=='actual_complete_PREP_and_Source_bound')for q in rows['READY_to_UNREADY']))
            inverse_results[role]=dict(actual_ready_Source_pin=files[fname],qualified_current_UNREADY_Source_pin=tp,originalParent_retained_Source_pin=pp,READY_to_UNREADY_counts=c1,UNREADY_to_OriginalParent_counts=c2,all_functions_classes_whole_bytes_and_AST_unchanged=True)
        explicit=inv['all_Source_META_actual_fullpins'];ck('explicit_Source_META_pin_list_unique_complete',len({q['path']for q in explicit})==len(explicit)and len(explicit)==147)
        for q in explicit:
            b,qactual=read(q['path']);ck('explicit_Source_META_full_EOF_SHA_same7ID:'+q['path'],qactual==q,q)
            if Path(q['path']).suffix=='.json':
                body=strict(b);collect(body);qmeta[q['path']]=body
        summary_path=inv['actual_closed_PREP_summary']['path'];ns_path=inv['actual_complete_NAMESPACE']['path'];summary=qmeta[summary_path];namespace=qmeta[ns_path]
        peer=strict(raw['ACTUAL_SAVED_V25_PREP_PEER.byte_exact.json']);peer_bytes=exact(inv['actual_saved_PREP_peer']);collect(peer)
        ck('same_actual_P4_31check_saved_review_copy_fullbytes',peer_bytes==raw['ACTUAL_SAVED_V25_PREP_PEER.byte_exact.json']and peer['schema']=='INDEPENDENT_V25_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_V1'and peer['status']=='PASS_ACTUAL_COMPLETE_PREP_ONLY'and peer['all_checks_typed_true']is True and peer['blockers']==[]and len(peer['checks'])==31 and all(type(c['passed'])is bool and c['passed']is True for c in peer['checks']))
        ck('same_actual_PREP_peer_three_summary_terminal_namespace_fullpins',peer['actual_Root_PREP_summary_pin']==inv['actual_closed_PREP_summary']and peer['actual_Root_PREP_terminal_pin']==inv['actual_Root_closed_terminal']and peer['actual_complete_namespace_manifest_pin']==inv['actual_complete_NAMESPACE'])
        ck('same_actual_P4_PREP_CLOSED0_only',summary['status']=='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD'and fullpin(summary['namespace_manifest'])==inv['actual_complete_NAMESPACE']and fullpin(summary['actual_root_terminal'])==inv['actual_Root_closed_terminal'])
        outrefs=inv['actual_output_fullpins'];owners={r['root']:r for r in namespace['namespaces']}
        for name,q in outrefs.items():
            owner=owners[str(Path(q['path']).parent)]
            ck('Root_complete_output_namespace_fullpin_coupling:'+name,fullpin(owner['files'][Path(q['path']).name])==q)
            if name in {'graph','trace'}:ck('Root_EOF_payload_only_current7ID:'+name,payload_id(q,'Actual Root closed PREP full-EOF namespace + summary + original 31-check saved META review'),q)
            else:
                body,qp=jr(q['path']);ck('actual_output_Source_META_full_EOF_SHA7ID:'+name,qp==q)
        declaration=qmeta[str(DECLARATION)]
        ck('exact_declaration_META_16MiB_full_EOF_strict_SHA7ID_coupled',FULL[str(DECLARATION)]==outrefs['declaration']==fullpin(summary['actual_declaration'])and FULL[str(DECLARATION)]['size_bytes']<=MAX)
        ck('declaration_diagnostic_forecast_not_new_RSS_runtime_cap',declaration['build_memory_diagnostic_output_contract']['max_bytes']==1048576 and declaration['complete_archive_forecast']['diagnostic_max_bytes']==1048576 and type(declaration['complete_archive_forecast']['total_bound'])is int and declaration['complete_archive_forecast']['total_bound']<2*2**30)
        qpath=B/'Root_actual_complete_graph_private_inactive_audit_helper_admission_v25.json';Q=qmeta[str(qpath)]
        ck('actual_Q_and_original_helper_fullpins_exact',FULL[str(qpath)]['sha256']=='c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b'and FULL['/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume_20261010.py']['sha256']=='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092')
        envpath=B/'Root_actual_Darwin_resource_SELF_rusage_diagnostic_environment_witness.json';env=qmeta[str(envpath)];envtool=qmeta[env['actual_environment_tool_terminal_fullpin']['path']]
        ck('actual_resource_environment_dependency_strict0_and_correct_highwater_scope',closed(envtool)and env['schema']=='ROOT_ACTUAL_DARWIN_RESOURCE_SELF_RUSAGE_DIAGNOSTIC_ENVIRONMENT_WITNESS_V1'and env['platform']=='darwin'and env['diagnostic_dependency_verified']is True and type(env['self_ru_maxrss_native_bytes_observed'])is int and env['ru_maxrss_semantics']=='DARWIN_RUSAGE_SELF_NATIVE_BYTES_PROCESS_HISTORICAL_HIGH_WATER_NOT_CURRENT_RSS_OR_GUARD_PEAK'and all(env[k]is False for k in ('whole_BUILD_qualified','whole_INPUT_qualified','native_or_science_qualified')))
        envobserved=strict(envtool['terminal_tool_return']['output'].encode())
        ck('actual_environment_raw_query_observation_matches_saved_witness',all(envobserved[k]==env[k]for k in ('actual_python_fullpin','actual_resource_module_fullpin','self_ru_maxrss_native_bytes_observed','ru_maxrss_semantics','platform')))
        canonical_path=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_memory_observation_capture.py');canonical=read(canonical_path)[0].decode();cv=literal_values(canonical)
        business=('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA')
        ck('actual_canonical_same_Q_environment_and_all6business_None',cv['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA']==FULL[str(qpath)]['sha256']and cv['FUTURE_ACTUAL_DIAGNOSTIC_RESOURCE_ENVIRONMENT_WITNESS_PIN']==FULL[str(envpath)]and all(k in cv and cv[k]is None for k in business))
        external=('FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN')
        ck('actual_canonical_three_Q_external_proof_fullpins_current',all(cv[k]==FULL[cv[k]['path']]for k in external))
        expected_host=dict(FUTURE_V25_ACTUAL_Q_SHA=FULL[str(qpath)]['sha256'],FUTURE_V25_CANONICAL_SHA=FULL[str(canonical_path)]['sha256'],FUTURE_V25_DECLARATION_SHA=outrefs['declaration']['sha256'],FUTURE_V25_PREP_SHA=outrefs['prep']['sha256'],FUTURE_V25_GRAPH_SHA=outrefs['graph']['sha256'],FUTURE_V25_TRACE_SHA=outrefs['trace']['sha256'],FUTURE_V25_PREP_SUMMARY_SHA=inv['actual_closed_PREP_summary']['sha256'])
        expected_writer={k:v for k,v in expected_host.items()if k in {'FUTURE_V25_ACTUAL_Q_SHA','FUTURE_V25_CANONICAL_SHA','FUTURE_V25_DECLARATION_SHA','FUTURE_V25_PREP_SHA'}};expected_writer['FUTURE_V25_BUILD_HOST_SHA']=hp['sha256']
        ck('all7actual_host_READY_SHA_globals_exact_current_evidence',all(globals_by_role['build_host'][k]==v for k,v in expected_host.items()))
        ck('all5actual_writer_READY_SHA_globals_exact_current_evidence',all(globals_by_role['build_writer'][k]==v for k,v in expected_writer.items()))
        deps=inv['all_Q_and_proof_explicit_typed_owner_expected_files'];dep_results={}
        for path,sha in deps.items():
            size=ident(path)[4]
            if physical(path,size):
                candidates=REGISTRY.get((path,sha),[]);matched=[q for q in candidates if q['identity']==ident(path)]
                ck('explicit_Q_Root_EOF_payload_current7ID:'+path,bool(matched),dict(expected_sha256=sha,Root_fullpin_metadata_candidates=len(candidates),current7ID=ident(path)))
                if matched:payload_id(matched[0],'Actual Root c787b4 Source binder expected owner SHA + original Q/pure/fresh saved full-EOF metadata')
                dep_results[path]=dict(expected_sha256=sha,current7ID=ident(path),independently_read_to_EOF=False)
            else:
                b,qp=read(path);ck('explicit_Q_Source_small_META_expected_EOF_SHA:'+path,qp['sha256']==sha,qp);dep_results[path]=qp
        ck('original_five_stages_9caps_complete_Source_preserved_by_whole_inverse',inv['all_original_full_five_stages_retained']is True and all(x['all_functions_classes_whole_bytes_and_AST_unchanged']is True for x in inverse_results.values()))
        ck('explicit_all147_SourceMETA_final7ID_unchanged',all(ident(q['path'])==q['identity']for q in explicit))
        ck('actual_bound_complete_final_files_dirs7IDs_unchanged',all(read(q['path'])[1]==q for q in files.values())and all(ident(BOUND/k)==v for k,v in dirs.items()))
    except Exception as exc:ck('finite_actual_two_role_Source_review_completed',False,dict(type=type(exc).__name__,message=str(exc)))
    passed=not BLOCKERS and all(type(c['passed'])is bool and c['passed']is True for c in CHECKS)
    report=dict(schema='INDEPENDENT_V25_ACTUAL_BOUND_FULL_BUILD_MEMORY_OBSERVATION_POSTCLOSE_META_SOURCE_REVIEW_V1',status='PASS_ACTUAL_BOUND_FULL_BUILD_MEMORY_OBSERVATION_AND_POSTCLOSE_META_SOURCE_ONLY'if passed else 'FAIL_ACTUAL_TWO_ROLE_BUILD_SOURCE_BINDING_ONLY',source_only=True,scope='Actual two-role READY literal binding, complete inverse bytes/AST and current explicit Source/META evidence only. Qualified old memory and P4 namespace semantics are prerequisites, not re-reviewed.',check_count=len(CHECKS),checks=CHECKS,all_checks_typed_true=passed,blockers=BLOCKERS,qualified_actual_bound_Source_manifest_pin=mf,actual_bound_build_host_pin=hp,actual_postclose_META_writer_pin=wp,actual_Root_Source_binding_tool_receipt_pin=rp,actual_bound_complete_package_view=view,whole_two_role_inverse_results=inverse_results,full_EOF_Source_and_small_META_pins=FULL,Root_actual_full_EOF_payload_pins_verified_current7ID_only=ROOT_PAYLOAD,complete_Source_AST_SHA256=SOURCE_AST,large_business_graph_trace_gzip_material_payload_independently_read_to_EOF=False,only_exact_declaration_16MiB_META_full_EOF_allowed=True,explicit_all_Source_META_actual_pin_count=147,actual_Root_binding_terminal_chunk='c787b4',candidate_API_guard_resource_helper_BUILD_native_or_science_executed=False,whole_BUILD_INPUT_RSS_native_or_science_qualified=False,new_runtime_or_science_gates_added_or_weakened=False,reviewer_original_Source_pin=sp)
    wj(out/'REVIEW.json',report)
    print(json.dumps(dict(root=str(out),review_pin=read(out/'REVIEW.json')[1],source_only=True,status=report['status'],check_count=len(CHECKS),blockers=BLOCKERS,qualified_actual_bound_Source_manifest_pin=mf),sort_keys=True,allow_nan=False))
    return 0 if passed else 1
if __name__=='__main__':
    assert not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')
    sys.exit(main())
