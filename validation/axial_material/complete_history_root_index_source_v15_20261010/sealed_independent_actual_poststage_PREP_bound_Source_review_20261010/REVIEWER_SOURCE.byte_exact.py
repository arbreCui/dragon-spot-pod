"""Finite Source/META-only independent actual PREP binding review; no candidate execution."""
import ast
import hashlib
import json
import os
import stat
import sys
import tempfile
from pathlib import Path

P=Path('/private/tmp/spot_V25_poststage_temporaries_ACTUAL_READY_PREP_Source_ROOT_20261010')
A=Path('/private/tmp/axmat_V25_poststage_temporaries_complete_UNREADY_Source_v2ept7ev')
F=Path('/private/tmp/axmat_V25_poststage_temporaries_complete_Source_independent_V2_20261010')
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
TERMINAL=B/'Root_actual_V25_poststage_PREP_Source_binding_tool_terminal_return.json'
Q=Path(tempfile.mkdtemp(prefix='axmat_V25_actual_poststage_PREP_bound_Source_independent_',dir='/private/tmp'))
checks=[];errors=[];pins={};occurrences={};retained={}
ROLES={'canonical':'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_poststage_temporaries.py','prepare_host':'combined_prepare_host.py','prepare_writer':'write_actual_prepare_terminal.py'}

def ck(name,value):
    ok=type(value)is bool and value is True;checks.append(dict(check=name,passed=ok))
    if not ok:raise ValueError(name)

def identity(p):
    s=Path(p).lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p):
    p=Path(p);before=identity(p)
    if not(p.is_absolute()and not any(x.is_symlink()for x in(p,*p.parents))and stat.S_ISREG(before[2])and before[3]==1):raise ValueError('ordinary Source/small META fullpin required '+str(p))
    with p.open('rb')as stream:d=hashlib.file_digest(stream,'sha256').hexdigest()
    if identity(p)!=before:raise ValueError('fullEOF7ID changed '+str(p))
    value=dict(path=str(p),sha256=d,size_bytes=before[4],identity=before)
    if str(p)in pins and pins[str(p)]!=value:raise ValueError('repeated actual input changed '+str(p))
    pins[str(p)]=value;return value

def strict(raw):
    def pairs(rows):
        d={}
        for k,v in rows:
            if k in d:raise ValueError('duplicate Source/META key')
            d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in()).throw(ValueError(x)))

def load(p):
    old=pin(p);value=strict(Path(p).read_bytes())
    if pin(p)!=old:raise ValueError('parse pin changed')
    return value

def tree(root):
    dirs={'.':identity(root)};files={}
    for p in sorted(root.rglob('*'),key=lambda p:str(p.relative_to(root))):
        rel=str(p.relative_to(root));s=p.lstat()
        if stat.S_ISDIR(s.st_mode):dirs[rel]=identity(p)
        elif stat.S_ISREG(s.st_mode):files[rel]=pin(p)
        else:raise ValueError('nonordinary Source member')
    return dict(directories=dirs,files=files)

def all_defs(raw):
    s=raw.decode();tree=ast.parse(s)
    nodes=sorted((n for n in ast.walk(tree)if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))),key=lambda n:(n.lineno,n.col_offset))
    return[(type(n).__name__,n.name,ast.dump(n,include_attributes=False),ast.get_source_segment(s,n))for n in nodes]

def reverse(raw,rows):
    for row in reversed(rows):
        a,b=row['old'].encode(),row['new'].encode()
        if raw.count(b)!=row['count']:raise ValueError('declared complete inverse occurrence '+row['label'])
        raw=raw.replace(b,a)
    return raw

def forward(raw,rows):
    for row in rows:
        a,b=row['old'].encode(),row['new'].encode()
        if raw.count(a)!=row['count']:raise ValueError('declared complete forward occurrence '+row['label'])
        raw=raw.replace(a,b)
    return raw

def constants(raw):
    c={}
    def literal(n):
        if isinstance(n,ast.Name)and n.id in c:return c[n.id]
        if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='Path'and len(n.args)==1:return Path(literal(n.args[0]))
        if isinstance(n,ast.BinOp)and isinstance(n.op,ast.Div):return Path(literal(n.left))/literal(n.right)
        if isinstance(n,ast.BinOp)and isinstance(n.op,(ast.Mult,ast.Pow)):
            a,b=literal(n.left),literal(n.right)
            if type(a)is not int or type(b)is not int or a<0 or b<0 or a>2**40 or b>(40 if isinstance(n.op,ast.Pow)else 2**40):raise ValueError('own bounded Source cap AST')
            return a*b if isinstance(n.op,ast.Mult)else a**b
        if isinstance(n,ast.Tuple):return tuple(literal(x)for x in n.elts)
        return ast.literal_eval(n)
    for n in ast.parse(raw).body:
        if isinstance(n,ast.Assign)and len(n.targets)==1:
            try:
                v=literal(n.value);t=n.targets[0]
                if isinstance(t,ast.Name):c[t.id]=v
                elif isinstance(t,ast.Tuple)and all(isinstance(x,ast.Name)for x in t.elts):
                    for k,z in zip(t.elts,v):c[k.id]=z
            except (ValueError,TypeError):pass
    return c

def retained_copy(src,relative):
    src=Path(src);dst=Q/relative;dst.parent.mkdir(parents=True,exist_ok=True)
    wanted=pin(src)
    with src.open('rb')as f,dst.open('xb')as g:
        while True:
            raw=f.read(2**20)
            if not raw:break
            g.write(raw)
    saved=pin(dst)
    if(saved['sha256'],saved['size_bytes'])!=(wanted['sha256'],wanted['size_bytes']):raise ValueError('finite Source retention not exact')
    retained[relative]=dict(original=wanted,saved=saved)

try:
    before=tree(P);am=load(A/'MANIFEST.json');pm=load(P/'MANIFEST.json');fm=load(F/'MANIFEST.json');peer=load(F/'REVIEW.json');ai=load(A/'COMPLETE_SOURCE_INVERSES.json');bi=load(P/'Root_actual_Q_bound_complete_PREP_Source_inverse.json');root=load(TERMINAL);tr=root['terminal_tool_return'];stdout=strict(tr['output'])
    ck('actual Root91304c genuine strict0 CLOSED raw Source binding terminal',pin(TERMINAL)['sha256']=='c3cb0eb7ec35e33f83f64bd0f2f2adcddb35eb4112fab4a686b7353345cb39c2'and root['schema']=='ROOT_ACTUAL_V25_POSTSTAGE_PREP_SOURCE_BINDING_TOOL_TERMINAL_RETURN_V1'and root['source_only']is True and root['closed']is True and root['observed_terminal']is True and root['session_repolled_after_close']is False and tr['chunk_id']=='91304c'and type(tr['exit_code'])is int and tr['exit_code']==0 and 'session_id'not in tr and root['business_or_science_executed']is False and root['new_qualification_created']is False)
    ck('actual complete READY5members manifest6files exact fullEOF7ID dirs',pin(P/'MANIFEST.json')['sha256']=='531b0b25f527f3f96767d6629ede54df3bac98ac205e762db859bb5ffe7507ef'and pm['source_only']is True and pm['executed_project']is False and pm['member_count']==len(pm['members'])==5 and set(before['files'])==set(pm['members'])|{'MANIFEST.json'}and len(before['files'])==6 and before['directories']==pm['directories']and all(before['files'][rel]==v for rel,v in pm['members'].items()))
    ck('actual Root terminal fullpin output matches all ready roles manifest and Q',stdout['source_only']is True and stdout['business_or_science_executed']is False and stdout['manifest']==pin(P/'MANIFEST.json')and all(stdout[k]==pin(P/ROLES[role])for k,role in [('canonical','canonical'),('host','prepare_host'),('writer','prepare_writer')])and stdout['actual_Q']==bi['actual_Q'])
    author_before=tree(A)
    ck('complete original author38files5dirs all manifest pins retained unchanged',pin(A/'MANIFEST.json')['sha256']=='9085afa282c04c927118323d101c9d23ffce51ebcdd2f2ddda7e4b8d0500d6bd'and len(author_before['files'])==38 and len(author_before['directories'])==5 and set(author_before['files'])==set(am['members'])|{'MANIFEST.json'}and author_before['directories']==am['directories']and all(author_before['files'][rel]==v for rel,v in am['members'].items()))
    ck('qualified658 prior independent Source checks strict unique currentauthor',peer['schema']=='INDEPENDENT_V25_POSTSTAGE_TEMPORARIES_COMPLETE_SOURCE_REVIEW_V1'and peer['status']=='PASS_COMPLETE_POSTSTAGE_TEMPORARIES_SOURCE_ONLY_UNREADY_NO_EXECUTION'and peer['source_only']is True and peer['all_checks_typed_true']is True and peer['check_count']==len(peer['checks'])==len({x['check']for x in peer['checks']})==658 and all(type(x['passed'])is bool and x['passed']is True for x in peer['checks'])and peer['blockers']==[]and peer['qualified_complete_Source_manifest_pin']==pin(A/'MANIFEST.json')and fm['review_pin']==pin(F/'REVIEW.json'))
    for n in('ACTUAL_SOURCE_SEAL_TOOL_RETURN.json','ACTUAL_SOURCE_POSTSEAL_TOOL_RETURN.json'):
        w=load(Path(str(F)+'_seal_receipt')/n);t=w['terminal_tool_return'];o=strict(t['output'])
        if not(w['closed']is True and w['observed_terminal']is True and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and o['manifest_pin']==pin(F/'MANIFEST.json')and o['review_pin']==pin(F/'REVIEW.json')and o['qualified_complete_Source_manifest_pin']==pin(A/'MANIFEST.json')and o['check_count']==658):raise ValueError('original658 peer actual seal/postseal coupling')
    ck('prior qualified658 actual peer seal and postseal true output coupled',True)
    for role,rel in ai['role_filenames'].items():
        raw=(A/rel).read_bytes();original=(A/('ORIGINAL_PARENT_SOURCE/'+role+'.full.py')).read_bytes();restored=reverse(raw,ai['exact_finite_transforms'][role]);definitions=all_defs(raw)
        if restored!=original or forward(original,ai['exact_finite_transforms'][role])!=raw or ast.dump(ast.parse(restored),include_attributes=False)!=ast.dump(ast.parse(original),include_attributes=False):raise ValueError('whole mother role byte/AST inverse '+role)
        if pin(A/rel)!=peer['qualified_role_Source_pins'][role]:raise ValueError('prior role fullpin '+role)
        originalactual=pin(ai['parent_Source_pins'][role]['path'])
        if originalactual!=ai['parent_Source_pins'][role]or originalactual['sha256']!=hashlib.sha256(original).hexdigest():raise ValueError('actual original full Source parent '+role)
        occurrences[role]=dict(author_definition_occurrences=len(definitions),all_occurrences_including_duplicate_names=True)
    ck('all seven complete mother roles fullbyte AST inverse original actual Source no physics caps changes',True)
    for role,rel in ROLES.items():
        raw=(P/rel).read_bytes();parent=(A/ai['role_filenames'][role]).read_bytes();original=(A/('ORIGINAL_PARENT_SOURCE/'+role+'.full.py')).read_bytes();inv=bi['complete_original_source_inverses'][role]
        restored=reverse(raw,inv['READY_to_UNREADY']);full=reverse(restored,inv['UNREADY_to_original'])
        if restored!=parent or full!=original or forward(parent,inv['READY_to_UNREADY'])!=raw or inv['UNREADY_to_original']!=ai['exact_finite_transforms'][role]:raise ValueError('actual complete two layer binding inverse '+role)
        if ast.dump(ast.parse(full),include_attributes=False)!=ast.dump(ast.parse(original),include_attributes=False)or all_defs(raw)!=all_defs(parent):raise ValueError('every actual READY role complete definition occurrence '+role)
        occurrences[role]['READY_definition_occurrences']=len(all_defs(raw));occurrences[role]['READY_and_UNREADY_all_definition_AST_bytes_equal']=True
    ck('actual all three ready roles two-layer full byte AST inverse and every duplicate definition preserved',True)
    raw=(P/ROLES['canonical']).read_bytes();s=raw.decode();t=ast.parse(raw);c=constants(raw);hc=constants((P/ROLES['prepare_host']).read_bytes());wc=constants((P/ROLES['prepare_writer']).read_bytes())
    business=bi['all_six_future_business_pins']
    ck('six real future PREP BUILD INPUT native business pins remain None',len(business)==6 and all(v is None and c[k]is None for k,v in business.items())and bi['candidate_guard_API_compiler_or_numeric_executed']is False and bi['installed']is False)
    run=next(n for n in t.body if isinstance(n,ast.FunctionDef)and n.name=='run_build');deletes=[n for n in ast.walk(run)if isinstance(n,ast.Delete)];delete=deletes[0];deleted=[x.id for x in delete.targets];loads={name:[n.lineno for n in ast.walk(run)if isinstance(n,ast.Name)and isinstance(n.ctx,ast.Load)and n.id==name]for name in deleted};segment=ast.get_source_segment(s,run)
    ck('private release exactly stages audit commands after every original last load and result checks',len(deletes)==1 and deleted==['stages','audit','commands']and all(max(v)<delete.lineno for v in loads.values())and 'del stages,audit,commands;gc.collect()'in segment and segment.index("result.update(classification='COMPLETE_COMBINED_RUNTIME_LINK_IDENTITY_ONLY'")<segment.index('del stages,audit,commands;gc.collect()')<segment.index("environment(d,phase='run_finally')")<segment.index("mandatory complete post-seal tail failed"))
    ck('original fixed canonical family schema caps retained',c['FAMILY']=='SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V25'and c['PREFIX']=='AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V25'and(c['TOTAL_WALL'],c['STAGE_WALL'],c['RSS'],c['RESERVE'],c['HISTORY_CAP'],c['FREE_FLOOR'])==(1800,600,512,2147483648,103079215104,8589934592)and(hc['WHOLE_CAP'],hc['STAGE_CAP'],hc['RSS_CAP'],hc['ARCHIVE_CAP'])==(1800,600,512,2147483648))
    ck('genuine host MRO one child zero retries all whole and tail checks byte-preserved',all_defs((P/ROLES['prepare_host']).read_bytes())==all_defs((A/ai['role_filenames']['prepare_host']).read_bytes())and "full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)"in(P/ROLES['prepare_host']).read_text()and "children_at_once=1,retries=0"in(P/ROLES['prepare_host']).read_text()and 'mandatory complete post-seal tail failed'in segment)
    ck('new exact namespace routing only and three canonical SHA fields correctly bound',hc['TARGET_SHA']==pin(P/ROLES['canonical'])['sha256']==wc['FACTORY_SHA']and hc['TARGET']==wc['FACTORY']and str(hc['SOURCE_ARCHIVE'])==str(wc['D'])and all('poststage-temporaries'in str(hc[k])for k in('HOST','SOURCE','OUT','TERMINAL'))and all('poststage_temporaries'in str(wc[k])for k in('D','E','FACTORY'))and hc['ACTUAL_HELPER_Q_SHA']==c['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA']=='c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b')
    qpath=Path(bi['actual_Q']['path']);q=load(qpath);qcopy=load(P/'ACTUAL_V25_HELPER_ONLY_JOINT_Q.byte_exact.json')
    ck('actual original c6 joint Q reread fullpin byteexact ready copy scope unchanged',pin(qpath)==bi['actual_Q']==stdout['actual_Q']and q==qcopy and qpath.read_bytes()==(P/'ACTUAL_V25_HELPER_ONLY_JOINT_Q.byte_exact.json').read_bytes()and q['schema']=='AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_INACTIVE_AUDIT_HELPER_ACTUAL_JOINT_ADMISSION_V25'and q['status']=='QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V25'and q['fresh_runtime_INPUT_qualified']is False and q['new_combined_prepared']is False and q['whole_build_qualified']is False and q['AAA_accuracy_qualified']is False and q['ABA_admitted']is False)
    ck('original actual3b helper and real Q writer Source fullpins maintained',pin(q['helper']['path'])==q['helper']and q['helper']['sha256']=='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'and pin(q['Root_actual_Source_writer']['path'])==q['Root_actual_Source_writer'])
    proofnames=['FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN'];proof={k:c[k]for k in proofnames}
    ck('all three actual new Q proof bindings actual paths SHA7ID protected and read by original binder',all(pin(v['path'])==v and v in bi['all_read_Source_META_fullpins']for v in proof.values()))
    writer=load(proof[proofnames[0]]['path']);wr=writer['terminal_tool_return'];wo=strict(wr['output']);saved=load(proof[proofnames[1]]['path']);retention=load(proof[proofnames[2]]['path'])
    ck('genuine94520a Q writer strict0 CLOSED couples actualc6 Q and actual writer Source',writer['closed']is True and writer['actual_tool_terminal_return_observed']is True and writer['no_closed_session_repoll']is True and wr['chunk_id']=='94520a'and type(wr['exit_code'])is int and wr['exit_code']==0 and 'session_id'not in wr and wo['actual_metadata_Q']==bi['actual_Q']and wo['actual_Source_writer']==q['Root_actual_Source_writer'])
    ck('actual48 saved Q peer typed unique pass only original helpermetadata',saved['schema']=='INDEPENDENT_V25_ACTUAL_JOINT_HELPER_Q_SAVED_META_REVIEW_V1'and saved['status']=='PASS_ACTUAL_JOINT_HELPER_Q_METADATA_ONLY'and saved['source_only']is True and saved['all_checks_typed_true']is True and saved['check_count']==len(saved['checks'])==len({v['check']for v in saved['checks']})==48 and all(type(v['passed'])is bool and v['passed']is True for v in saved['checks'])and saved['blockers']==[]and saved['Root_actual_Q_pin']==bi['actual_Q']and saved['Root_actual_Q_writer_terminal_pin']==proof[proofnames[0]]and saved['Root_actual_Q_writer_Source_pin']==q['Root_actual_Source_writer'])
    for row in retention['complete_original_members'].values():
        if pin(row['original']['path'])!=row['original']or pin(row['saved']['path'])!=row['saved']or(row['original']['sha256'],row['original']['size_bytes'])!=(row['saved']['sha256'],row['saved']['size_bytes']):raise ValueError('actual Q savedpeer retention fullEOF')
    ck('Q savedpeer all10 retention original and saved exact fullEOF pins seal coupled',len(retention['complete_original_members'])==retention['complete_original_member_count']==10 and retention['new_qualification_created']is False and pin(retention['original_actual_peer_seal_receipt']['path'])==retention['original_actual_peer_seal_receipt']and pin(retention['saved_actual_peer_seal_receipt']['path'])==retention['saved_actual_peer_seal_receipt']and retention['original_actual_peer_seal_receipt']['sha256']==retention['saved_actual_peer_seal_receipt']['sha256'])
    readrows=bi['all_read_Source_META_fullpins'];ck('all68 actual Root binder read Source META fullEOF7ID preserved no graph trace gzip payload',len(readrows)==len({v['path']for v in readrows})==68 and all(not v['path'].endswith(('.gz','.sqlite','.db','.xsm','.bin'))and 'input_graph.json'not in v['path']and 'input_creation_python_open_trace'not in v['path']and pin(v['path'])==v for v in readrows))
    owners=bi['all_Q_and_proof_explicit_typed_owner_expected_files']
    ck('full340 typed owner ledger keeps real Q helper writer peer and retention evidence',len(owners)==340 and all(owners[v['path']]==v['sha256']for v in[bi['actual_Q'],q['helper'],q['Root_actual_Source_writer'],*proof.values()]))
    ck('new PREP namespaces and canonical currently uninstalled',all(not os.path.lexists(v)for v in(hc['HOST'],hc['SOURCE'],hc['OUT'],hc['TERMINAL'],wc['D'],wc['E'],wc['FACTORY'])))
    ck('original bound and mother Source complete files directories unchanged after review',tree(P)==before and tree(A)==author_before)
    for p in P.iterdir():retained_copy(p,'COMPLETE_REVIEWED_ACTUAL_BOUND_SOURCE/'+p.name)
    for role in ROLES:
        retained_copy(A/ai['role_filenames'][role],'EXACT_NECESSARY_AUTHOR_SOURCE/'+role+'.UNREADY.full.py')
        retained_copy(A/('ORIGINAL_PARENT_SOURCE/'+role+'.full.py'),'EXACT_NECESSARY_ORIGINAL_PARENT_SOURCE/'+role+'.full.py')
    for src,rel in[(A/'MANIFEST.json','FINITE_PROVENANCE/author_MANIFEST.byte_exact.json'),(A/'COMPLETE_SOURCE_INVERSES.json','FINITE_PROVENANCE/mother_COMPLETE_SOURCE_INVERSES.byte_exact.json'),(F/'REVIEW.json','FINITE_PROVENANCE/qualified658_REVIEW.byte_exact.json'),(F/'MANIFEST.json','FINITE_PROVENANCE/qualified658_MANIFEST.byte_exact.json'),(TERMINAL,'FINITE_PROVENANCE/Root_actual91304c_binding_tool.byte_exact.json')]:retained_copy(src,rel)
    ck('complete6 reviewed actual bound Source finite lossless original inverse provenance retained',len(retained)==17 and all(pin(v['original']['path'])==v['original']and pin(v['saved']['path'])==v['saved']for v in retained.values()))
except Exception as ex:errors.append(dict(type=type(ex).__name__,message=str(ex)))

blockers=[c['check']for c in checks if c['passed']is not True]+[x['message']for x in errors]
report=dict(schema='INDEPENDENT_ACTUAL_V25_POSTSTAGE_COMPLETE_PREP_BOUND_SOURCE_REVIEW_V1',status='PASS_ACTUAL_Q_BOUND_COMPLETE_PREP_SOURCE_ONLY_NOT_INSTALLED_OR_EXECUTED'if not blockers else'BLOCKED_ACTUAL_POSTSTAGE_PREP_BOUND_SOURCE_REVIEW',source_only=True,all_checks_typed_true=not blockers,check_count=len(checks),checks=checks,blockers=blockers,errors=errors,actual_Root_binding_terminal_chunk='91304c',actual_Root_binding_terminal_pin=pins.get(str(TERMINAL)),actual_complete_bound_Source_manifest_pin=pins.get(str(P/'MANIFEST.json')),actual_ready_role_Source_pins={k:pins.get(str(P/v))for k,v in ROLES.items()},qualified_complete_UNREADY_Source_manifest_pin=pins.get(str(A/'MANIFEST.json')),qualified658_Source_review_pin=pins.get(str(F/'REVIEW.json')),all_role_definition_occurrence_counts=occurrences,complete_bound_Source_snapshot_before_and_after=before,finite_retention_ledger=retained,all_actual_reviewed_Source_small_META_fullpins=list(pins.values()),no_RSS_or_allocator_reclamation_prediction=True,all_six_future_business_pins=None if blockers else bi['all_six_future_business_pins'],candidate_binder_helper_guard_API_compile_native_material_numeric_or_Rootwriter_executed=False,project_or_original_Source_or_progress_written=False,graph_trace_gzip_material_DB_binary_payload_read=False,new_installer_prelaunch_Source_still_required=True,new_actual_PREP_or_BUILD_or_INPUT_result=None,actual_native_RSS_result=None,whole_build_qualified=False,whole_INPUT_admitted=False,AAA_accuracy_qualified=False,ABA_admitted=False,scientific_qualification_created=False)
with(Q/'REVIEW.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
with(Q/'REVIEWER_SOURCE.byte_exact.py').open('xb')as f:f.write(Path(__file__).read_bytes())
print(json.dumps(dict(status=report['status'],source_only=True,report_pin=pin(Q/'REVIEW.json'),reviewer_Source_pin=pin(Q/'REVIEWER_SOURCE.byte_exact.py'),checks=len(checks),blockers=blockers),allow_nan=False),flush=True)
sys.exit(0 if not blockers else 1)
