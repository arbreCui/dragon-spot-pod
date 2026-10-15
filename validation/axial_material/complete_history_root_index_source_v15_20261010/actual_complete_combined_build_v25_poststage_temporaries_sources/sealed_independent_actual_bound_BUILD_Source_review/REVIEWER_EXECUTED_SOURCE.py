"""Independent stdlib Source/small-META review; no candidate import or execution.
Physical graph/trace/gzip/native payload bytes are never read. Existing Root EOF
records are verified by current exact7ID only. This does not review our prior
saved-PREP report again or award business/scientific qualification.
"""
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import shlex
import stat
import tempfile

B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
P=Path('/private/tmp/spot_ROOT_actual_V25_poststage_complete_BUILD_BOUND_Source_20261010')
A=Path('/private/tmp/axmat_V25_poststage_temporaries_complete_UNREADY_Source_v2ept7ev')
PEER=Path('/private/tmp/axmat_V25_poststage_temporaries_complete_Source_independent_V2_20261010')
PREP_BOUND=Path('/private/tmp/spot_V25_poststage_temporaries_ACTUAL_READY_PREP_Source_ROOT_20261010')
D=B/'actual_complete_combined_prepare_v25_poststage_temporaries_sources'
E=B/'actual_complete_combined_prepare_v25_poststage_temporaries_receipts'
C=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_poststage_temporaries.py')
U=Path('/private/tmp/axmat_V25_poststage_complete_finite_utilities_V3_UNREADY_Source_20261010')
ROOT_RECEIPT=B/'Root_actual_V25_poststage_complete_BUILD_Source_binding_tool_terminal_return.json'
CAPS=[1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0]
BUSINESS=('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA')
READS={};CACHE={};CHECKS=[];DETAIL={};COPIES={}

def identity(p):
    s=Path(p).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def ordinary(p):
    p=Path(p)
    assert p.is_absolute() and '..' not in p.parts
    for q in [*reversed(p.parents),p]:
        i=identity(q)
        assert not stat.S_ISLNK(i[2]) and (q==p or stat.S_ISDIR(i[2]))
    return p

def readbytes(p):
    p=ordinary(p);i=identity(p)
    assert stat.S_ISREG(i[2])
    if str(p) in CACHE:
        assert READS[str(p)]['identity']==i
        return CACHE[str(p)]
    with p.open('rb') as f:
        data=f.read()
        assert f.read()==b''
    assert identity(p)==i
    q=dict(path=str(p),sha256=hashlib.sha256(data).hexdigest(),size_bytes=len(data),identity=i)
    assert len(data)==i[4]
    READS[str(p)]=q;CACHE[str(p)]=data
    return data

def pin(p):
    readbytes(p)
    return dict(READS[str(Path(p))])

def pairs(rows):
    d={}
    for k,v in rows:
        assert k not in d
        d[k]=v
    return d

def reject(value):
    raise ValueError('nonfinite META constant '+value)

def meta(p):
    d=json.loads(readbytes(p).decode(),object_pairs_hook=pairs,parse_constant=reject)
    def visit(v):
        if type(v) is float: assert math.isfinite(v)
        elif type(v) is dict:
            for w in v.values(): visit(w)
        elif type(v) is list:
            for w in v: visit(w)
    visit(d)
    return d

def normalized(q):
    i=q.get('identity',q.get('identity7'))
    assert type(q['path']) is str and Path(q['path']).is_absolute()
    assert type(q['sha256']) is str and len(q['sha256'])==64 and all(c in '0123456789abcdef' for c in q['sha256'])
    assert type(i) is list and len(i)==7 and all(type(n) is int for n in i)
    assert stat.S_ISREG(i[2]) and i[3]>=1
    assert q.get('size_bytes',i[4])==i[4]
    return dict(path=q['path'],sha256=q['sha256'],size_bytes=i[4],identity=i)

def exact(q):
    q=normalized(q)
    assert pin(q['path'])==q
    return q

def stat_exact(q):
    q=normalized(q);ordinary(q['path'])
    assert identity(q['path'])==q['identity']
    return q

def check(name,passed,details=None):
    assert type(name) is str and name not in {c['id'] for c in CHECKS}
    assert type(passed) is bool
    CHECKS.append(dict(id=name,passed=passed))
    if details is not None: DETAIL[name]=details

def runcheck(name,fn):
    try: details=fn();check(name,True,details)
    except Exception as e: check(name,False,dict(error=repr(e)))

def inventory(root,read=True):
    root=ordinary(root);dirs={'.':identity(root)};files={}
    assert stat.S_ISDIR(dirs['.'][2])
    for p in sorted(root.rglob('*'),key=lambda p:str(p.relative_to(root))):
        i=identity(p);rel=str(p.relative_to(root));assert not stat.S_ISLNK(i[2])
        if stat.S_ISDIR(i[2]): dirs[rel]=i
        else:
            assert stat.S_ISREG(i[2]) and i[3]==1
            files[rel]=pin(p) if read else dict(path=str(p),identity=i)
    assert all(identity(root/r)==i for r,i in dirs.items())
    return dict(files=files,directories=dirs)

def package(root,sha):
    m=meta(root/'MANIFEST.json');mp=pin(root/'MANIFEST.json');v=inventory(root)
    assert mp['sha256']==sha and m['source_only'] is True
    assert type(m['member_count']) is int and m['member_count']==len(m['members'])
    assert type(m['members']) is dict and set(v['files'])==set(m['members'])|{'MANIFEST.json'}
    assert m['directories']==v['directories']
    assert all(normalized(q)==v['files'][r] and q['path']==str(root/r) for r,q in m['members'].items())
    return dict(manifest=mp,view=v,metadata=m)

def text(p): return readbytes(p).decode('utf-8')
def dump(t): return ast.dump(ast.parse(t),include_attributes=False)

def reverse(t,rows):
    assert type(rows) is list
    for r in reversed(rows):
        assert set(r)=={'label','old','new','count'}
        assert type(r['count']) is int and r['count']>0 and t.count(r['new'])==r['count']
        t=t.replace(r['new'],r['old'])
    return t

def definitions(t):
    a=ast.parse(t)
    nodes=sorted((n for n in ast.walk(a) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))),key=lambda n:(n.lineno,n.col_offset,n.end_lineno))
    return [dict(kind=type(n).__name__,name=n.name,source=ast.get_source_segment(t,n),AST=ast.dump(n,include_attributes=False)) for n in nodes]

def assigns(t):
    d={}
    for n in ast.parse(t).body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            d[n.targets[0].id]=n.value
    return d

def literal(t,k): return ast.literal_eval(assigns(t)[k])

def closed(d):
    assert d['closed'] is True
    assert d.get('observed_terminal',d.get('actual_tool_terminal_return_observed',d.get('observed_after_actual_terminal_return',False))) is True
    tr=d.get('terminal_tool_return',d.get('actual_tool_return',d.get('exec_command_result')))
    assert type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr
    assert d.get('session_repolled_after_close',False) is False
    return tr,json.loads(tr['output'],object_pairs_hook=pairs,parse_constant=reject) if tr['output'].strip() else None

BOUND={};MOTHER={};MPREPORT={};INV={};READY={};SAVED={};SUMMARY={};NAMESPACE={};ROOTTOOL={}

def bound_package():
    global BOUND,INV
    BOUND=package(P,'7c9538b968b2173655b7608d708af39edebd1565920fdc7d62d12606c69fd6f1')
    assert len(BOUND['view']['files'])==5 and len(BOUND['view']['directories'])==1
    expected={'combined_build_host.py':'d5024a468b204d988fb8f929303481fdcd5e0c311b6a282536bc1dea5a979159','write_actual_build_postclose_META.py':'7a7c8d59ddea37397592591ba96d6ac7dbca1dda1acce7f9d12b9ae6dcaa278a'}
    for n,s in expected.items(): assert pin(P/n)['sha256']==s;ast.parse(text(P/n))
    INV=meta(P/'Root_actual_full_V25_build_Source_binding_inverse.json')
    assert INV['schema']=='ROOT_V25_ACTUAL_FULL_FIVE_STAGE_BUILD_SOURCE_BINDING_INVERSE_V1' and INV['source_only'] is True
    return dict(manifest=BOUND['manifest'],files=5,directories=1,roles={n:pin(P/n) for n in expected})

def mother_package():
    global MOTHER,MPREPORT
    MOTHER=package(A,'9085afa282c04c927118323d101c9d23ffce51ebcdd2f2ddda7e4b8d0500d6bd')
    assert len(MOTHER['view']['files'])==38 and len(MOTHER['view']['directories'])==5
    MPREPORT=meta(PEER/'REVIEW.json')
    assert MPREPORT['schema']=='INDEPENDENT_V25_POSTSTAGE_TEMPORARIES_COMPLETE_SOURCE_REVIEW_V1'
    assert MPREPORT['status']=='PASS_COMPLETE_POSTSTAGE_TEMPORARIES_SOURCE_ONLY_UNREADY_NO_EXECUTION'
    assert MPREPORT['source_only'] is True and MPREPORT['all_checks_typed_true'] is True and MPREPORT['blockers']==[]
    assert type(MPREPORT['check_count']) is int and MPREPORT['check_count']==658==len(MPREPORT['checks'])
    assert all(type(q['passed']) is bool and q['passed'] is True for q in MPREPORT['checks'])
    assert exact(MPREPORT['qualified_complete_Source_manifest_pin'])==MOTHER['manifest']
    return dict(mother=MOTHER['manifest'],qualified_existing_peer=pin(PEER/'REVIEW.json'),existing658_not_rerun=True)

def mother_seal():
    pp=package(PEER,'6e1627dae76811f4f2c845a10520c5fb5decee9adcbd0b5f03359c800b4b4367')
    s=meta(Path(str(PEER)+'_seal_receipt')/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json')
    tr,observed=closed(s)
    assert observed['manifest_pin']==pp['manifest'] and observed['review_pin']==pin(PEER/'REVIEW.json')
    return dict(peer_manifest=pp['manifest'],seal=pin(Path(str(PEER)+'_seal_receipt')/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json'),seal_chunk=tr['chunk_id'])

def all_seven_mother_inverse():
    proof=meta(A/'COMPLETE_SOURCE_INVERSES.json');counts={}
    assert set(proof['role_filenames'])==set(proof['exact_finite_transforms'])==set(MPREPORT['qualified_role_Source_pins'])
    for role,name in proof['role_filenames'].items():
        t=text(A/name);assert exact(MPREPORT['qualified_role_Source_pins'][role])==pin(A/name)
        original=text(A/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py'))
        restored=reverse(t,proof['exact_finite_transforms'][role])
        assert restored==original and dump(restored)==dump(original)
        assert pin(A/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py'))['sha256']==proof['parent_Source_pins'][role]['sha256']
        counts[role]=dict(hunks=len(proof['exact_finite_transforms'][role]),definitions_including_repeats=len(definitions(t)))
    return counts

def bound_two_layer_inverse():
    proof=meta(A/'COMPLETE_SOURCE_INVERSES.json');counts={}
    for role,name in [('build_host','combined_build_host.py'),('build_writer','write_actual_build_postclose_META.py')]:
        t=text(P/name);u=text(A/proof['role_filenames'][role]);i=INV['complete_original_source_inverses'][role]
        restored=reverse(t,i['READY_to_UNREADY']);assert restored==u and dump(restored)==dump(u)
        assert i['UNREADY_to_original']==proof['exact_finite_transforms'][role]
        original=text(A/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py'))
        r2=reverse(restored,i['UNREADY_to_original']);assert r2==original and dump(r2)==dump(original)
        assert i['complete_byte_inverse'] is True and i['complete_AST_inverse'] is True
        assert definitions(t)==definitions(u)
        counts[role]=dict(READY_to_UNREADY_hunks=len(i['READY_to_UNREADY']),UNREADY_to_original_hunks=len(i['UNREADY_to_original']),all_definition_occurrences=len(definitions(t)))
    return counts

def root_binding_receipt():
    global ROOTTOOL
    d=meta(ROOT_RECEIPT);tr,observed=closed(d);assert tr['chunk_id']=='ad2d02'
    assert d['source_only'] is True and d['business_or_science_executed'] is False and d['new_qualification_created'] is False
    assert observed==dict(source_only=True,host=pin(P/'combined_build_host.py'),writer=pin(P/'write_actual_build_postclose_META.py'),manifest=BOUND['manifest'],full_original_build_retained=True,project_executed=False)
    argv=shlex.split(d['actual_launch_arguments']['cmd']);bp=A/'bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py'
    assert str(bp) in argv and '-B' in argv and 'env'==argv[0] and argv[:3]==['env','-u','PYTHONOPTIMIZE']
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):assert k+'=1' in argv
    args=dict(zip(argv[argv.index(str(bp))+1::2],argv[argv.index(str(bp))+2::2]))
    assert args['--destination']==str(P) and args['--saved-prep-peer-report']==INV['actual_saved_PREP_peer']['path']
    assert args['--saved-prep-peer-report-sha256']==INV['actual_saved_PREP_peer']['sha256']
    assert args['--actual-Q-sha256']=='c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b' and args['--actual-canonical-sha256']==pin(C)['sha256']
    ct=text(C)
    for k,opt in [('FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN','--actual-new-Q-writer-terminal'),('FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN','--actual-Q-saved-peer'),('FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN','--actual-Q-saved-peer-retention')]:
        q=exact(literal(ct,k));assert args[opt]==q['path'] and args[opt+'-sha256']==q['sha256']
    assert len(args)==11
    ROOTTOOL=dict(receipt=pin(ROOT_RECEIPT),chunk=tr['chunk_id'],Source_only=True,actual_launch_arguments=d['actual_launch_arguments'],actual_raw_stdout=tr['output'])
    return ROOTTOOL

def current_saved_PREP_lineage_only():
    global SAVED,SUMMARY,NAMESPACE
    q=exact(INV['actual_saved_PREP_peer']);assert readbytes(P/'ACTUAL_SAVED_V25_PREP_PEER.byte_exact.json')==readbytes(q['path'])
    SAVED=meta(q['path']);assert SAVED['schema']=='INDEPENDENT_V25_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_V1' and SAVED['status']=='PASS_ACTUAL_COMPLETE_PREP_ONLY'
    assert SAVED['check_count']==31 and SAVED['all_checks_typed_true'] is True and SAVED['blockers']==[]
    for key in ('actual_PREP_closed_EXIT0_verified','actual_metadata_writer_closed_EXIT0_verified','all_complete_scope_verified','actual_PREP_metadata_only'):assert SAVED[key] is True
    for key in ('whole_combined_build_qualified','whole_combined_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified'):assert SAVED[key] is False
    for k,i in [('actual_Root_PREP_summary_pin','actual_closed_PREP_summary'),('actual_Root_PREP_terminal_pin','actual_Root_closed_terminal'),('actual_complete_namespace_manifest_pin','actual_complete_NAMESPACE')]:assert exact(SAVED[k])==exact(INV[i])
    SUMMARY=meta(INV['actual_closed_PREP_summary']['path']);NAMESPACE=meta(INV['actual_complete_NAMESPACE']['path'])
    td=meta(INV['actual_Root_closed_terminal']['path']);tr,_=closed(td);assert tr['chunk_id']=='d90987'
    assert SAVED['actual_PREP_terminal_chunk']=='d90987' and SAVED['actual_metadata_writer_terminal_chunk']=='4bfa1b'
    assert SUMMARY['status']=='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD'
    assert normalized(SUMMARY['actual_root_terminal'])==normalized(INV['actual_Root_closed_terminal']) and normalized(SUMMARY['namespace_manifest'])==normalized(INV['actual_complete_NAMESPACE'])
    return dict(existing_report_not_independently_requalified=True,Root_new_PREP_terminal='d90987',Root_new_PREP_META_writer='4bfa1b',bound_original_report=q)

def source_META_bound_reads():
    assert len(INV['all_Source_META_actual_fullpins'])==73
    for q in INV['all_Source_META_actual_fullpins']:exact(q)
    return dict(actual_full_EOF_Source_and_small_META_count=73,no_payload_files_in_this_list=True)

def outputs_current7ID_not_payload():
    ns={row['root']:row for row in NAMESPACE['namespaces']};out=INV['actual_output_fullpins'];assert set(out)=={'declaration','prep','graph','trace','source_admission'}
    for k,q in out.items():
        stat_exact(q);root=Path(q['path']).parent
        assert normalized(ns[str(root)]['files'][Path(q['path']).name])==normalized(q)
    for k,sk in [('declaration','actual_declaration'),('prep','formal_PREP_terminal'),('graph','actual_complete_input_graph'),('trace','actual_complete_creation_trace')]:assert normalized(SUMMARY[sk])==normalized(out[k])
    return dict(Root_complete_EOF_output_pins=out,independent_current7ID_only=True,independent_payload_EOF_or_decode=False)

def bound_values_actual_new_PREP():
    h=text(P/'combined_build_host.py');w=text(P/'write_actual_build_postclose_META.py')
    values={'FUTURE_V25_ACTUAL_Q_SHA':'c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b','FUTURE_V25_CANONICAL_SHA':pin(C)['sha256'],'FUTURE_V25_DECLARATION_SHA':INV['actual_output_fullpins']['declaration']['sha256'],'FUTURE_V25_PREP_SHA':INV['actual_output_fullpins']['prep']['sha256'],'FUTURE_V25_GRAPH_SHA':INV['actual_output_fullpins']['graph']['sha256'],'FUTURE_V25_TRACE_SHA':INV['actual_output_fullpins']['trace']['sha256'],'FUTURE_V25_PREP_SUMMARY_SHA':INV['actual_closed_PREP_summary']['sha256']}
    for k,v in values.items():assert literal(h,k)==v
    for k in ('FUTURE_V25_ACTUAL_Q_SHA','FUTURE_V25_CANONICAL_SHA','FUTURE_V25_DECLARATION_SHA','FUTURE_V25_PREP_SHA'):assert literal(w,k)==values[k]
    assert literal(w,'FUTURE_V25_BUILD_HOST_SHA')==pin(P/'combined_build_host.py')['sha256']
    for t in (h,w):assert literal(t,'SOURCE_BINDING_STATUS')=='READY_V25_ACTUAL_COMPLETE_PREP_AND_SOURCE_BOUND'
    return values

def new_PREP_Source_namespace_and_304_plus2():
    f=meta(E/'Root_prelaunch_complete_source_freeze.json');v=inventory(D)
    assert f['source_root']==str(D) and f['symlinks']=={} and f['no_SOURCE_append_after_freeze'] is True
    assert len(v['files'])==297 and len(v['directories'])==35
    assert f['source_root_identity']==v['directories']['.']
    assert f['complete_directories']=={r:i for r,i in v['directories'].items() if r!='.'} and set(f['complete_files'])==set(v['files'])
    assert all(normalized(q)==v['files'][r] for r,q in f['complete_files'].items())
    install=meta(D/'Root_actual_complete_SOURCE_install_record.json');assert len(install['complete_Source_owner_copies'])==7
    pre=meta(E/'Root_final_prelaunch_source_and_reserve_check.json');ordered=pre['exact_original_host_input_sources']
    prefix=install['exact_original_host_prefix_seven_input_pins'];assert len(prefix)==7
    assert len(ordered)==304 and pre['actual_original_host_ordered_input_count']==304
    expected=[normalized(q) for q in prefix]+[v['files'][r] for r in sorted(v['files'],key=lambda r:Path(r))]
    assert [normalized(q) for q in ordered]==expected
    for q in ordered:exact(q)
    assert SAVED['complete_actual_input_entries']==306
    for key in ('original_helper','original_resource_factory'):exact(pre[key])
    assert pre['genuine_supervisor_MRO_unchanged'] is True
    return dict(Source_files=297,Source_subdirectories=34,host_ordered_inputs=304,helper_resource_added=2,total_ordered_original_fullinputs=306,original_owner_count=7,ordered_inputs_including_repeats=ordered)

def ready_canonical_inverse_and_repeated_defs():
    global READY
    READY=meta(PREP_BOUND/'Root_actual_Q_bound_complete_PREP_Source_inverse.json');t=text(C);i=READY['complete_original_source_inverses']['canonical']
    u=text(A/'canonical.V25.UNREADY.full.py');original=text(A/'ORIGINAL_PARENT_SOURCE/canonical.full.py')
    restored=reverse(t,i['READY_to_UNREADY']);assert restored==u and dump(restored)==dump(u)
    r2=reverse(restored,i['UNREADY_to_original']);assert r2==original and dump(r2)==dump(original)
    assert definitions(t)==definitions(u)
    counts=[(r['kind'],r['name']) for r in definitions(t)]
    assert counts==[(r['kind'],r['name']) for r in definitions(original)]
    assert pin(C)['sha256']=='6693fb03a8c39d76e85719aec813ddee624cce2c6389218314b11efd76ac1649'
    assert READY['all_six_future_business_pins']=={k:None for k in BUSINESS}
    return dict(full_definition_occurrences=len(counts),all_duplicate_occurrences_preserved=True,ready_to_unready_hunks=len(i['READY_to_UNREADY']),unready_to_original_hunks=len(i['UNREADY_to_original']))

def canonical_last_use_two_AST_nodes_only():
    t=text(C);nodes=[n for n in ast.parse(t).body if isinstance(n,ast.FunctionDef) and n.name=='run_build'];assert len(nodes)==1
    n=nodes[0];tries=[z for z in n.body if isinstance(z,ast.Try)];assert len(tries)==2
    release=tries[0].body[-2:]
    assert isinstance(release[0],ast.Delete) and [q.id for q in release[0].targets]==['stages','audit','commands']
    assert ast.dump(release[1],include_attributes=False)==ast.dump(ast.parse('gc.collect()').body[0],include_attributes=False)
    del_line=release[0].lineno
    later=[z.id for z in ast.walk(n) if isinstance(z,ast.Name) and isinstance(z.ctx,ast.Load) and z.lineno>del_line and z.id in ('stages','audit','commands')]
    assert later==[]
    before=tries[0].body[-3];assert isinstance(before,ast.Expr) and isinstance(before.value,ast.Call) and isinstance(before.value.func,ast.Attribute) and before.value.func.attr=='update'
    assert {k.arg for k in before.value.keywords}=={'classification','watchdogs','corrected_runtime','fresh_cold_AAA_required'}
    assert len([q for q in ast.walk(n) if isinstance(q,ast.Delete)])==1
    return dict(last_use_private_names=['stages','audit','commands'],added_AST_nodes=2,post_delete_name_loads=[],no_RSS_or_allocator_prediction=True)

def no_future_business_fabricated():
    t=text(C)
    assert all(literal(t,k) is None for k in BUSINESS)
    assert INV['candidate_guard_API_compiler_numeric_executed'] is False and INV['whole_build_INPUT_native_science_qualified'] is False
    assert INV['all_original_full_five_stages_retained'] is True and INV['original_caps']==CAPS and all(type(v) is int for v in INV['original_caps'])
    return dict(six_future_business_pins={k:None for k in BUSINESS},actual_build_native_science_qualification=False)

def Q340_owner_exact_contract_current7ID():
    expected=INV['all_Q_and_proof_explicit_typed_owner_expected_files']
    assert len(expected)==340 and expected==READY['all_Q_and_proof_explicit_typed_owner_expected_files']
    refs={}
    def collect(v):
        if type(v) is dict:
            if {'path','sha256'}<=v.keys() and type(v.get('identity',v.get('identity7'))) is list:
                q=normalized(v);refs.setdefault(q['path'],[]).append(q)
            for z in v.values():collect(z)
        elif type(v) is list:
            for z in v:collect(z)
    for q in INV['all_Source_META_actual_fullpins']:
        if Path(q['path']).suffix=='.json':collect(meta(q['path']))
    rows={}
    for p,sha in expected.items():
        choices=[q for q in refs.get(p,[]) if q['sha256']==sha and q['identity']==identity(p)]
        assert choices
        q=choices[0];stat_exact(q);rows[p]=q
    return dict(all340_original_owner_expected_hashes_unchanged=True,current_exact7ID_pins=rows,archive_graph_trace_gzip_payload_independently_read=False)

def genuine_caps_MRO_stages_tails():
    h=text(P/'combined_build_host.py');w=text(P/'write_actual_build_postclose_META.py');c=text(C)
    assert "WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30" in h
    assert "WHOLE, STAGE, RSS, ARCHIVE, HISTORY, FREE = 1800, 600, 512, 2*2**30, 96*2**30, 8*2**30" in w
    assert "full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)" in h and "type(runner) is not full.OwnRSSSerialExecutor" in h
    assert "resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)" in h
    labels=literal(h,'EXPECTED_LABELS');assert labels==['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']==literal(w,'LABELS')
    assert literal(w,'TAIL_FIELDS')==('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')
    assert "len(inner)!=5" in h and "inner_watches!=result['watchdogs']" in h and "inner_watches[:-1]!=audit['previous_stage_watchdogs']" in h
    assert "inputs+[hpin,rpin]" in h and "original!=fixed_pins" in w
    assert "before['artifact_bytes']+ARCHIVE_CAP>=96*2**30" in h and "before['disk_free_bytes']-ARCHIVE_CAP<8*2**30" in h
    assert "watch['sampled_peak_rss_mib']<RSS_CAP" in h and 'supervisor_class_or_MRO_modified=False' in h
    return dict(original_caps=CAPS,labels=labels,all_function_byte_AST_inverse_is_primary_evidence=True)

def full_Root_binder_source_contract():
    t=text(A/'bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py')
    assert "INDEPENDENT_V25_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_V1" in t and "PASS_ACTUAL_COMPLETE_PREP_ONLY" in t
    assert "saved PREP peer three complete pins" in t and "all original complete PREP namespaces" in t
    assert "same actual new-Q external proof Source bindings" in t and "all six future business pins unknown" in t
    assert "actual Source binding no function change" in t and "actual Source/meta input unchanged" in t
    assert "for k in BUSINESS" in t and "len(ns)==5" in t
    assert "candidate_guard_API_compiler_numeric_executed=False" in t and "whole_build_INPUT_native_science_qualified=False" in t
    imported=[]
    for n in ast.walk(ast.parse(t)):
        if isinstance(n,ast.Import):imported.extend(z.name for z in n.names)
        elif isinstance(n,ast.ImportFrom):imported.append(n.module)
    assert set(imported)<= {'argparse','ast','hashlib','json','math','os','pathlib','re','stat','sys'}
    return dict(full_Root_binder_Source=pin(A/'bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py'),all_stdlib_imports=imported,original_complete_definition_occurrences=len(definitions(t)))

def downstream_utility_contract_compatible():
    t=text(U/'Root_poststage_Source_META_contract.py');fs={n.name:ast.get_source_segment(t,n) for n in ast.parse(t).body if isinstance(n,ast.FunctionDef)}
    for k in ('qualified_actual_bound_Source_manifest_pin','actual_bound_build_host_pin','actual_postclose_META_writer_pin','actual_Root_Source_binding_tool_receipt_pin'):assert k in fs['bound_facts']
    assert 'INDEPENDENT_V25_ACTUAL_BOUND_FULL_BUILD_POSTCLOSE_META_SOURCE_REVIEW_V1' in fs['bound_facts']
    assert 'PASS_ACTUAL_BOUND_FULL_BUILD_AND_POSTCLOSE_META_SOURCE_ONLY' in fs['bound_facts']
    assert "observed['manifest_pin']==mpin and observed['review_pin']==rp" in fs['peer']
    assert "type(members) is dict" in fs['package'] and "m['directories']==v['directories']" in fs['package']
    return dict(utility_contract_Source=pin(U/'Root_poststage_Source_META_contract.py'),required_schema_and_four_fullpins_supported=True)

def finite_namespace_exact_paths():
    h=text(P/'combined_build_host.py');w=text(P/'write_actual_build_postclose_META.py')
    assert 'v25-monitor-access-20261010' not in h and 'v25-monitor-access-20261010' not in w
    assert 'v25_monitor_access_sources' not in h and 'v25_monitor_access_sources' not in w
    for t in (h,w):assert C.name in t and 'actual_complete_combined_build_v25_poststage_temporaries_sources' in t
    assert 'actual_complete_combined_prepare_v25_poststage_temporaries_receipts/Root_actual_prepare_tool_terminal_return.json' in h
    assert 'actual_complete_combined_prepare_v25_poststage_temporaries_receipts/Root_actual_complete_combined_prepare_summary.json' in h
    # Exact inverse above proves all original recipes/order/flags and five command bodies retained.
    return dict(canonical=str(C),future_BUILD_D=str(B/'actual_complete_combined_build_v25_poststage_temporaries_sources'),all_original_physical_and_command_bodies_preserved=True)

TASKS=[('complete_actual_bound_package',bound_package),('qualified_complete_mother_Source_package',mother_package),('existing658_peer_true_seal_coupling',mother_seal),('complete_seven_role_mother_byte_AST_inverses',all_seven_mother_inverse),('actual_build_host_writer_two_layer_byte_AST_inverses_all_defs',bound_two_layer_inverse),('genuine_Root_ad2d02_binding_terminal_and_all_CLI_actual_pins',root_binding_receipt),('new_PREP_saved31_original_lineage_no_self_requalification',current_saved_PREP_lineage_only),('complete73_actual_Source_small_META_fullEOF',source_META_bound_reads),('new_PREP_five_outputs_original_EOF_claims_current7ID_only',outputs_current7ID_not_payload),('actual_new_PREP_bound_host_writer_Source_constants',bound_values_actual_new_PREP),('complete_new_PREP_Source_owners_ordered304_plus2_prerequisite',new_PREP_Source_namespace_and_304_plus2),('whole_actual_canonical_ready_inverse_and_duplicate_defs',ready_canonical_inverse_and_repeated_defs),('canonical_lastuse_only_two_AST_nodes_no_later_private_load',canonical_last_use_two_AST_nodes_only),('six_future_business_unknown_and_no_new_qualification',no_future_business_fabricated),('original_complete340_Q_proof_owners_exact_hash_current7ID',Q340_owner_exact_contract_current7ID),('genuine_MRO_all_caps_five_stages_full_tail_contract',genuine_caps_MRO_stages_tails),('complete_Root_binder_Source_schema_namespace_future_guards',full_Root_binder_source_contract),('downstream_utility_bound_facts_fullpin_and_seal_contract',downstream_utility_contract_compatible),('exact_poststage_future_BUILD_routes_keep_physical_body',finite_namespace_exact_paths)]
for name,fn in TASKS:runcheck(name,fn)

blockers=[q['id'] for q in CHECKS if q['passed'] is not True]
assert len({q['id'] for q in CHECKS})==len(CHECKS) and all(type(q['passed']) is bool for q in CHECKS)
F=Path(tempfile.mkdtemp(prefix='axmat_V25_poststage_actual_bound_BUILD_Source_independent_',dir='/private/tmp'))
def write(p,v):
    with p.open('x') as f:json.dump(v,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')

report=dict(schema='INDEPENDENT_V25_ACTUAL_BOUND_FULL_BUILD_POSTCLOSE_META_SOURCE_REVIEW_V1',status='PASS_ACTUAL_BOUND_FULL_BUILD_AND_POSTCLOSE_META_SOURCE_ONLY' if not blockers else 'BLOCKED_ACTUAL_BOUND_FULL_BUILD_SOURCE_ONLY',source_only=True,all_checks_typed_true=not blockers,all_checks_passed=not blockers,check_count=len(CHECKS),checks=CHECKS,blockers=blockers,qualified_actual_bound_Source_manifest_pin=pin(P/'MANIFEST.json'),actual_bound_build_host_pin=pin(P/'combined_build_host.py'),actual_postclose_META_writer_pin=pin(P/'write_actual_build_postclose_META.py'),actual_Root_Source_binding_tool_receipt_pin=pin(ROOT_RECEIPT),actual_existing_mother658_Source_peer_pin=pin(PEER/'REVIEW.json'),actual_existing_saved_PREP31_report_pin=INV.get('actual_saved_PREP_peer'),existing_saved_PREP_report_not_self_requalified=True,actual_Root_Source_binding_chunk='ad2d02',details=DETAIL,independent_complete_EOF_Source_small_META_pins=list(READS.values()),physical_graph_trace_gzip_native_material_or_DB_payload_read=False,Root_saved_payload_EOF_pins_verified_current7ID_only=True,candidate_binder_utility_helper_guard_API_compiler_numeric_executed=False,new_BUILD_or_business_result=None,new_whole_BUILD_RSS_result=None,whole_build_qualified=False,whole_combined_INPUT_admitted=False,native_transport_executed=False,native_RSS_qualified=False,physical_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,goal_complete=False,project_or_parent_package_mutated=False)
write(F/'REVIEW.json',report)
(F/'REVIEWER_EXECUTED_SOURCE.py').write_bytes(Path(__file__).read_bytes())
(F/'COMPLETE_REVIEWED_BOUND_SOURCE').mkdir()
for name in sorted(BOUND['view']['files']):
    dst=F/'COMPLETE_REVIEWED_BOUND_SOURCE'/name;dst.write_bytes(readbytes(P/name));COPIES[str(dst.relative_to(F))]=pin(P/name)
(F/'FINITE_COMPLETE_SOURCE_PROVENANCE').mkdir()
proof=meta(A/'COMPLETE_SOURCE_INVERSES.json')
copy_sources={'mother_MANIFEST.byte_exact.json':A/'MANIFEST.json','mother_COMPLETE_SOURCE_INVERSES.byte_exact.json':A/'COMPLETE_SOURCE_INVERSES.json','qualified_existing658_REVIEW.byte_exact.json':PEER/'REVIEW.json','qualified_existing658_MANIFEST.byte_exact.json':PEER/'MANIFEST.json','Root_actual_BUILD_binding_tool.byte_exact.json':ROOT_RECEIPT,'actual_ready_canonical.complete_Source.py':C,'actual_READY_PREP_Source_inverse.byte_exact.json':PREP_BOUND/'Root_actual_Q_bound_complete_PREP_Source_inverse.json','Root_poststage_Source_META_contract.complete_Source.py':U/'Root_poststage_Source_META_contract.py'}
for role,name in proof['role_filenames'].items():
    copy_sources['mother_'+role+'.complete_Source.py']=A/name
    copy_sources['original_'+role+'.complete_Source.py']=A/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')
for name,src in copy_sources.items():
    dst=F/'FINITE_COMPLETE_SOURCE_PROVENANCE'/name;dst.write_bytes(readbytes(src));COPIES[str(dst.relative_to(F))]=pin(src)
write(F/'FINITE_LOSSLESS_COMPLETE_SOURCE_COPY_LINEAGE.json',dict(schema='INDEPENDENT_FINITE_COMPLETE_SOURCE_COPY_LINEAGE_V1',source_only=True,complete_original_pins=COPIES,no_large_parent_history_clone=True))
(F/'OWN_REVIEW_ATTEMPT1_PROVENANCE').mkdir()
for oldname in ('REVIEW.json','REVIEWER_EXECUTED_SOURCE.py','ACTUAL_OWN_REVIEW_ATTEMPT1_TOOL_RETURN.json'):
    prior=Path('/private/tmp/axmat_V25_poststage_actual_bound_BUILD_Source_independent_ksqjn9l4')/oldname
    (F/'OWN_REVIEW_ATTEMPT1_PROVENANCE'/oldname).write_bytes(prior.read_bytes())
(F/'OWN_REVIEW_ATTEMPT1_PROVENANCE/COMPLETE_OWN_REVIEW_SOURCE_FINITE_INVERSE.json').write_bytes(Path('/private/tmp/spot_V25_own_PREP_freeze_root_shape_review_finite_inverse_20261010.json').read_bytes())
print(json.dumps(dict(package=str(F),review_pin=pin(F/'REVIEW.json'),check_count=len(CHECKS),all_checks_typed_true=not blockers,blockers=blockers,source_only=True),allow_nan=False))
raise SystemExit(1 if blockers else 0)
