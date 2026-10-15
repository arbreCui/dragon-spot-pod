import pathlib,json,hashlib,os,stat,ast,tempfile
OLD=pathlib.Path('/private/tmp/SPOT_NEW6A_Q_ROOT_CLOSED_BINDING_SOURCE_ONLY_z5exjj8i');NEW=pathlib.Path(tempfile.mkdtemp(prefix='SPOT_NEW6A_Q_ROOT_ACTUAL_FROZEN_CLOSURE_SOURCE_ONLY_',dir='/private/tmp'));OM=json.loads((OLD/'FINAL_SOURCE_ONLY_MANIFEST.json').read_bytes());S=pathlib.Path(OM['Root_closure_Source']['path']).read_text();inputs={}
def ids(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=pathlib.Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and not any(q.is_symlink() for q in (p,*p.parents));h=hashlib.sha256();n=0
 with p.open('rb') as f:
  assert ids(os.fstat(f.fileno()))==ids(s)
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
  assert ids(os.fstat(f.fileno()))==ids(s)
 assert ids(p.lstat())==ids(s) and n==s.st_size;return dict(path=str(p),size_bytes=n,sha256=h.hexdigest(),identity=ids(s))
def verify(r):
 g=pin(r['path']);assert g=={k:r[k] for k in g}
 if g['path'] in inputs:assert inputs[g['path']]==g
 inputs[g['path']]=g;return g
def read(p):
 before=pin(p);d=json.loads(pathlib.Path(p).read_bytes());assert pin(p)==before;inputs[before['path']]=before;return d
WT=pathlib.Path('/private/tmp/Root_corrected_new6a_Q_v3_actual_tool_returns_20261011.json');PT=pathlib.Path('/private/tmp/Root_new6a_Q_independent_saved_review_actual_tool_returns_20261011.json');wt,pt=read(WT),read(PT);assert (wt['initial']['chunk_id'],wt['initial']['session_id'],wt['closed']['chunk_id'],wt['closed']['exit_code'])==('c81bec',24272,'11666a',0);assert (pt['initial']['chunk_id'],pt['initial']['session_id'],pt['closed']['chunk_id'],pt['closed']['exit_code'])==('a26eb5',97295,'fa8c25',0)
ws,ps=json.loads(wt['closed']['output']),json.loads(pt['closed']['output']);qp,qwp,rp,rwp=ws['actual_metadata_Q'],ws['actual_complete_resource_witness'],ps['review_pin'],ps['actual_peer_resource_witness']
for r in (qp,qwp,rp,rwp):verify(r)
q,qw,peer,pw=(read(r['path']) for r in (qp,qwp,rp,rwp));assert peer['check_count']==len(peer['checks'])==12601 and peer['all_checks_typed_true'] is True and all(type(r['passed']) is bool and r['passed'] is True for r in peer['checks']);assert len(q['complete_Root_metadata_EOF7ID_inputs'])==235 and q['complete_Root_metadata_EOF7ID_inputs']==peer['complete_actual_Q_declared_EOF7ID_input_pins'];assert ps['actual_metadata_Q']==qp and peer['actual_metadata_Q']==qp and pw['actual_saved_review']==rp
for r in q['complete_Root_metadata_EOF7ID_inputs']+peer['all_this_review_EOF7ID_input_pins']:verify(r)
for p in [*OLD.iterdir(),pathlib.Path(__file__),WT,PT]:verify(pin(p))
T=read('/private/tmp/Root_current_original_account_phase_timing_m9t382tr/CURRENT_ACCOUNT_TIMING.json')
for r in T['original_five_guard_pins']:verify(r)
for d in T['current_complete_D_E_freeze'].values():
 for r in d['files']:verify(r)
 for p,i in d['directories'].items():assert ids(pathlib.Path(p).lstat())==i
verify(T['original_failed_provenance_pin'])
changes=[]
def rep(a,b):
 global S
 assert S.count(a)==1,(a[:130],S.count(a));S=S.replace(a,b,1);changes.append(dict(before=a,after=b))
added='''
FINAL_FROZEN_INPUTS_PATH=Path(__file__).parent/'FINAL_ACTUAL_INPUTS_FROZEN_MANIFEST.json'

def read_actual_final_frozen_inputs():
    frozen_pin=pin(FINAL_FROZEN_INPUTS_PATH);frozen_doc=read(FINAL_FROZEN_INPUTS_PATH,frozen_pin)
    ck(frozen_doc['schema']=='SPOT_NEW6A_Q_ROOT_CLOSURE_ALL_ACTUAL_INPUTS_FROZEN_SOURCE_ONLY_V1' and frozen_doc['status']=='ACTUAL_INPUTS_FROZEN_WRITER0_PEER0_PENDING_ROOT_EXECUTION','actual final frozen Source-only input contract')
    ck(frozen_doc['Root_closure_Source']==pin(__file__) and frozen_doc['actual_Q_writer_Source']==EXPECTED_Q_WRITER and frozen_doc['actual_peer_Source']==EXPECTED_PEER_SOURCE and frozen_doc['metadata_contract_Source']==EXPECTED_CONTRACT,'actual final frozen Source exact bindings')
    for row in frozen_doc['complete_actual_EOF7ID_frozen_inputs']:verify(row)
    ck(frozen_doc['actual_Q_declared235_inputs_complete'] is True and frozen_doc['actual_peer_all12601_checks_complete'] is True,'complete actual all235/all12601 strict frozen inputs')
    return frozen_doc,frozen_pin
'''
rep('CHECKS=[];INPUTS={};COPY_ROWS={}', 'CHECKS=[];INPUTS={};COPY_ROWS={}\n'+added)
rep('wt=read(WRITER_TOOLS);pt=read(PEER_TOOLS);ws=closed0(wt);ps=closed0(pt)',"final_frozen_doc,final_frozen_pin=read_actual_final_frozen_inputs()\nwt=read(WRITER_TOOLS);pt=read(PEER_TOOLS);ws=closed0(wt);ps=closed0(pt)\nck(pin(WRITER_TOOLS)==final_frozen_doc['actual_writer_tool_returns'] and pin(PEER_TOOLS)==final_frozen_doc['actual_peer_tool_returns'],'actual frozen genuine tool document pins')\nck(pt['initial']['chunk_id']=='a26eb5' and pt['initial']['session_id']==97295 and pt['closed']['chunk_id']=='fa8c25','unique genuine actual peer initial/session/closed0')")
rep("q=read(QPIN['path'],QPIN);qw=read(QWIT['path'],QWIT);peer=read(RPIN['path'],RPIN);pw=read(RWIT['path'],RWIT)","ck([QPIN,QWIT,RPIN,RWIT]==final_frozen_doc['actual_current_Q_peer_and_witness_outputs'],'all four exact final frozen output identities')\nq=read(QPIN['path'],QPIN);qw=read(QWIT['path'],QWIT);peer=read(RPIN['path'],RPIN);pw=read(RWIT['path'],RWIT)")
rep("for row in [QPIN,QWIT,RPIN,RWIT,pin(WRITER_TOOLS),pin(PEER_TOOLS),EXPECTED_Q_WRITER,EXPECTED_CONTRACT,EXPECTED_PEER_SOURCE,EXPECTED_Q_MANIFEST,EXPECTED_PEER_MANIFEST,pin(__file__),PREPARER_SOURCE,ORIGINAL_RESOURCE_PREFIX]:add_copy(row)","for row in [QPIN,QWIT,RPIN,RWIT,pin(WRITER_TOOLS),pin(PEER_TOOLS),EXPECTED_Q_WRITER,EXPECTED_CONTRACT,EXPECTED_PEER_SOURCE,EXPECTED_Q_MANIFEST,EXPECTED_PEER_MANIFEST,pin(__file__),PREPARER_SOURCE,ORIGINAL_RESOURCE_PREFIX,final_frozen_pin]:add_copy(row)\nfor row in final_frozen_doc['additional_actual_Source_preparation_and_failed_draft_inputs']:add_copy(row)")
rep("[PEER_TOOLS,WRITER_TOOLS,PREPARER_SOURCE['path']]","[PEER_TOOLS,WRITER_TOOLS,PREPARER_SOURCE['path'],final_frozen_pin['path']]+[row['path'] for row in final_frozen_doc['additional_actual_Source_preparation_and_failed_draft_inputs']]")
rep("actual_Root_closure_Source=pin(__file__),complete_Q_declared235_EOF7ID_input_pins=","actual_Root_closure_Source=pin(__file__),actual_final_input_manifest=final_frozen_pin,complete_Q_declared235_EOF7ID_input_pins=")
# Corrected PREPARER_SOURCE refers to this actual final preparation Source.
tree=ast.parse(S);oldp=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PREPARER_SOURCE' for t in n.targets));rep('PREPARER_SOURCE='+repr(oldp),'PREPARER_SOURCE='+repr(pin(__file__)))
ast.parse(S);p=NEW/'ROOT_CLOSE_ACTUAL_NEW6A_Q_AFTER_GENUINE_PEER_REVIEW_CLOSED0.py';p.write_text(S);sp=pin(p)
r=S
for c in reversed(changes):assert r.count(c['after'])==1;r=r.replace(c['after'],c['before'],1)
assert r.encode()==pathlib.Path(OM['Root_closure_Source']['path']).read_bytes()
# Original resource functions are byte/AST identical. Only the new metadata stage is extended.
a=ast.parse(r);b=ast.parse(S);old={n.name:ast.dump(n,include_attributes=False) for n in a.body if isinstance(n,ast.FunctionDef)};new={n.name:ast.dump(n,include_attributes=False) for n in b.body if isinstance(n,ast.FunctionDef)};assert all(new[k]==v for k,v in old.items())
additional=[pin(x) for x in OLD.iterdir()]+[pin(__file__),oldp]
for x in additional:verify(x)
F=dict(schema='SPOT_NEW6A_Q_ROOT_CLOSURE_ALL_ACTUAL_INPUTS_FROZEN_SOURCE_ONLY_V1',status='ACTUAL_INPUTS_FROZEN_WRITER0_PEER0_PENDING_ROOT_EXECUTION',Root_closure_Source=sp,metadata_contract_Source=OM['metadata_contract_Source'],actual_Q_writer_Source=OM['actual_new_Q_writer_Source'],actual_peer_Source=OM['expected_peer_Source'],actual_writer_tool_returns=pin(WT),actual_peer_tool_returns=pin(PT),actual_current_Q_peer_and_witness_outputs=[qp,qwp,rp,rwp],actual_Q_declared235_inputs_complete=True,actual_peer_all12601_checks_complete=True,actual_peer_saved_check_count=12601,actual_writer_tool_chunks={'initial':'c81bec','session':24272,'closed':'11666a','exit_code':0},actual_peer_tool_chunks={'initial':'a26eb5','session':97295,'closed':'fa8c25','exit_code':0},complete_actual_EOF7ID_frozen_inputs=list(inputs.values()),additional_actual_Source_preparation_and_failed_draft_inputs=additional,original_Q_ancestry_and_failed7ed0a8_kept=True,original_resource_prefix_and_all_draft_functions_AST_identical=True,Source_only=True,Root_closure_publisher_factory_Native_or_PS_executed=False,whole_INPUT_or_science_or_BOOT_admitted=False)
f=NEW/'FINAL_ACTUAL_INPUTS_FROZEN_MANIFEST.json';f.write_text(json.dumps(F,ensure_ascii=False,indent=2)+'\n');fp=pin(f)
M=dict(status='SOURCE_ONLY_FINAL_ACTUAL_WRITER0_PEER0_FROZEN_ROOT_CLOSURE_PENDING_ROOT_REVIEW',Root_closure_Source=sp,final_actual_frozen_inputs_manifest=fp,old_UNREADY_Source_manifest=pin(OLD/'FINAL_SOURCE_ONLY_MANIFEST.json'),complete_whole_inverse_to_old_UNREADY_Source=True,Source_forward_changes=changes,all_old_draft_function_and_class_AST_identical=True,old_original_resource_prefix_full_inverse_sha256=OM['original_resource_prefix_whole_inverse_sha256'],actual235_Q_inputs_and12601peerchecks_frozen=True,original_600s_512MiB_joint2_history96_free8_4MiB_final_metadata_reservation_unchanged=True,original32MiB_copyforecast_reserved_and64MiB_archivecap_unchanged=True,actual_writer_tool_returns=pin(WT),actual_peer_tool_returns=pin(PT),actual_Q_and_peer_current_outputs=[qp,qwp,rp,rwp],Root_closure_schema='SPOT_ROOT_ACTUAL_NEW6A_Q_WRITER_AND_INDEPENDENT_SAVED_REVIEW_CLOSED_BINDING_V1',Root_closure_status='ROOT_CLOSED_ACTUAL_NEW6A_METADATA_Q_ONLY',all_seven_science_whole_flags_False=True,Source_only=True,Root_publisher_peer_factory_Native_or_PS_executed=False,actual_Root_closure_created=False,READY_factory_created=False,preparation_Source=pin(__file__))
mp=NEW/'FINAL_SOURCE_ONLY_MANIFEST.json';mp.write_text(json.dumps(M,ensure_ascii=False,indent=2)+'\n')
for x in inputs.values():assert pin(x['path'])==x
print(json.dumps(dict(Source_root=str(NEW),Source=sp,frozen_inputs_manifest=fp,Source_manifest=pin(mp),actual_frozen_input_count=len(inputs),actual235_all_held=True,Source_only=True,Rootpublisher_or_READYfactory_executed=False)))
