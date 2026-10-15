"""Standard-library SOURCE author. Never imports or executes the project."""
import ast
import hashlib
import json
from pathlib import Path
import stat

HERE = Path(__file__).resolve().parent
BASE = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
PLAN_PATH = Path('/private/tmp/axmat_v22_joint_helper_Q_UNREADY_SOURCE_design_20261010_s3vgnwa3/EXACT_FUTURE_CANONICAL_GENUINE_PREP_SOURCE_LOCATIONS.json')
Q_WRITER = PLAN_PATH.parent/'write_actual_joint_helper_admission_v22.FINAL.UNREADY.py'
Q_WRITER_SHA = '59590a6f123d26519fd68e7f9042c44c9fb3e1c1c477470728b1765789efc444'
WRITER_PARENT = BASE/'actual_complete_combined_prepare_v21_sources/metadata_writer_SOURCE_binding/write_actual_prepare_terminal.py'
HELPER_PATH = Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_owner_namespace_last_use_20261010.py')
HELPER_SHA = 'cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c'
HELPER_IDENTITY = [16777229,49393808,33188,1,148965,1791600075411912623,1791600075411921373]
BUSINESS = ('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA')
UNREADY_DOC = ('UNREADY V22 complete sender/root-index full graph private owner and namespace last-use helper Source template. The cf0 helper has its own actual original producer/codec protocol and complete current-graph verifier trials, but this runtime template binds no new helper joint-admission Q. The new helper SHA and new Q SHA remain None until Root supplies the actual new jointly admitted Q and its saved independent META review. All original PREP, complete five-stage build, whole INPUT admission, two complete fresh graph/specs phases, full graph/trace, historical seven-key bodies, aliases, namespaces, nine coverage categories, physical inputs, genuine guard/MRO and original budgets remain required. Actual V15 complete86 component INPUT prerequisites remain unchanged. This fresh V22 business family has executed no PREP/build/whole INPUT/native/AAA/ABA or physical validation; all six future business success pins remain None. No Source binding predicts business RSS or future PASS.')
READY_DOC = ('READY Source-bound V22 complete sender/root-index full graph private owner and namespace last-use helper revision. Root actual new joint helper Q binds the same cf0 installed helper to two distinct successful bounded trials: the original full60-second producer/codec protocol with the additional private owner controls, and complete current-graph fresh verifier, each with its actual closed integer-zero terminal and complete saved independent review. This qualification covers helper metadata protocol and complete input verification only. The original strict reader last-use change preserves UTF-8 decoding, JSON hooks and finite-value checks. All original PREP, complete five-stage build, whole INPUT admission, two complete fresh graph/specs phases, full graph/trace, historical seven-key bodies, aliases, namespaces, nine coverage categories, physical inputs, genuine guard/MRO and original budgets remain required. Actual V15 complete86 component INPUT prerequisites remain unchanged. This fresh V22 business family has executed no PREP/build/whole INPUT/native/AAA/ABA or physical validation; all six future business success pins remain None. No Source binding predicts business RSS or future PASS.')

def ident(p):
    s=Path(p).lstat(); return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p):
    p=Path(p); before=ident(p)
    assert stat.S_ISREG(before[2])
    raw=p.read_bytes()
    assert ident(p)==before
    return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),identity=before,size_bytes=len(raw)),raw

def write_json(name,value):
    with (HERE/name).open('x') as f: json.dump(value,f,indent=2,allow_nan=False); f.write('\n')

def defs(text):
    return {n.name:ast.get_source_segment(text,n) for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}

def apply_edits(text,edits):
    for e in edits:
        assert text.count(e['old'])==1,(e['label'],'forward',text.count(e['old']))
        text=text.replace(e['old'],e['new'],1)
    return text

def inverse(text,edits):
    for e in reversed(edits):
        assert text.count(e['new'])==1,(e['label'],'inverse',text.count(e['new']))
        text=text.replace(e['new'],e['old'],1)
    return text

def edit(label,old,new): return dict(label=label,old=old,new=new)

def main():
    pp,pr=pin(PLAN_PATH); plan=json.loads(pr)
    cp,cr=pin(plan['canonical_parent']['path']); hp,hr=pin(plan['genuine_PREP_host_parent']['path']); wp,wr=pin(WRITER_PARENT)
    qp,qr=pin(Q_WRITER); gp,gr=pin(HELPER_PATH)
    assert qp['sha256']==Q_WRITER_SHA and gp['sha256']==HELPER_SHA and gp['identity']==HELPER_IDENTITY
    for actual,key in ((cp,'canonical_parent'),(hp,'genuine_PREP_host_parent')):
        assert actual==plan[key]
    originals={'canonical':cr.decode(),'host':hr.decode(),'writer':wr.decode()}
    for name,raw in (('canonical',cr),('host',hr),('writer',wr)):
        with (HERE/(name+'.V21.parent.full.py')).open('xb') as f: f.write(raw)
    with (HERE/'EXACT_PARENT_SOURCE_PLAN.full.json').open('xb') as f: f.write(pr)
    canon_edits=[]
    for row in plan['canonical_exact_anchors']:
        old=row['whole_exact_source_anchor']; label=row.get('global_name','docstring')
        if label=='docstring': new=repr(UNREADY_DOC)
        elif label=='DRAFT_STATUS': new="DRAFT_STATUS = 'UNREADY_V22_COMPLETE_NEW_HELPER_ACTUAL_Q_UNBOUND'"
        elif label=="INPUT_HELPERS['graph']": new="(ROOT/'validation/axial_material/combined_runtime_complete_input_graph_private_owner_namespace_last_use_20261010.py',None)"
        elif label=='FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA': new='FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA = None'
        else: new=old.replace('_V21','_V22').replace('_v21','_v22').replace('-v21-','-v22-')
        canon_edits.append(edit(label,old,new))
    host_edits=[]
    for row in plan['host_exact_11_atomic_anchors']:
        old=row['whole_exact_source_anchor']; label=row.get('global_name',f"schema_or_pin_line_{row['line']}")
        if label=='TARGET_SHA': new='TARGET_SHA=None'
        elif "combined_runtime_complete_input_graph_private_verifier_trace_consume" in old:
            new="support.pin(Path("+repr(str(HELPER_PATH))+"),"+repr(HELPER_SHA)+")"
        elif 'Root_actual_complete_graph_private_verifier_helper_admission_v21' in old:
            new='support.pin(ACTUAL_HELPER_Q_PATH,ACTUAL_HELPER_Q_SHA)'
        else: new=old.replace('_V21','_V22').replace('_v21','_v22').replace('-v21-','-v22-')
        host_edits.append(edit(label,old,new))
    caps='WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30'
    host_edits.append(edit('disclosed_unbound_Q_globals',caps,caps+"\nSOURCE_BINDING_STATUS='UNREADY_V22_ACTUAL_Q_AND_TARGET_SOURCE_UNBOUND'\nACTUAL_HELPER_Q_PATH=None\nACTUAL_HELPER_Q_SHA=None"))
    host_edits.append(edit('disclosed_pre_project_load_UNREADY_guard','def main():\n    started=time.monotonic()',"def main():\n    if SOURCE_BINDING_STATUS!='READY_V22_ACTUAL_Q_AND_TARGET_SOURCE_BOUND' or TARGET_SHA is None or ACTUAL_HELPER_Q_PATH is None or ACTUAL_HELPER_Q_SHA is None:\n        raise ValueError('UNREADY Source template: actual new helper Q and full READY canonical Source must be bound before any project load')\n    started=time.monotonic()"))
    writer_edits=[]
    olddoc='"""Root metadata only, after a genuine, closed, successful V21 PREP tool return."""'
    newdoc='"""UNREADY V22 Root PREP metadata writer Source template; only Root after actual Q binding and genuine CLOSED EXIT0 PREP may execute the bound writer."""'
    writer_edits.append(edit('writer_doc',olddoc,newdoc))
    wt=originals['writer']
    for name in ('D','E','H','S','O','T','FACTORY','FACTORY_SHA'):
        node=next(n for n in ast.parse(wt).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
        old=ast.get_source_segment(wt,node)
        new=name+'=None' if name=='FACTORY_SHA' else old.replace('_v21','_v22').replace('-v21-','-v22-')
        writer_edits.append(edit(name,old,new))
    for old in ('AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V21_ACTUAL_EXTERNAL_PREP_RETURN_V1','ROOT_V21_ACTUAL_COMPLETE_PREPARE_ALL_NAMESPACES_V1','ROOT_V21_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1'):
        writer_edits.append(edit('writer_schema_'+old,repr(old),repr(old.replace('_V21','_V22'))))
    writer_edits.append(edit('writer_binding_status','FACTORY_SHA=None',"FACTORY_SHA=None\nSOURCE_BINDING_STATUS='UNREADY_V22_ACTUAL_Q_AND_CANONICAL_SOURCE_UNBOUND'"))
    writer_edits.append(edit('writer_pre_META_read_UNREADY_guard','def main():\n    actual=json.loads',"def main():\n    if SOURCE_BINDING_STATUS!='READY_V22_ACTUAL_Q_AND_CANONICAL_SOURCE_BOUND' or FACTORY_SHA is None:\n        raise ValueError('UNREADY Source template: no Root PREP result metadata reads before actual Q and canonical Source binding')\n    actual=json.loads"))
    transforms={'canonical':canon_edits,'host':host_edits,'writer':writer_edits}
    templates={name:apply_edits(originals[name],edits) for name,edits in transforms.items()}
    checks=[]
    def check(label,ok):
        assert ok,label; checks.append(dict(check=label,pass_=True))
    for name,edits in transforms.items():
        text=templates[name]; recovered=inverse(text,edits)
        check(name+'_complete_byte_inverse',recovered.encode()==originals[name].encode())
        check(name+'_complete_AST_inverse',ast.dump(ast.parse(recovered),include_attributes=False)==ast.dump(ast.parse(originals[name]),include_attributes=False))
        check(name+'_complete_defs_retained',list(defs(text))==list(defs(originals[name])))
        for fn,body in defs(originals[name]).items():
            changed={'canonical':{'require_ready'},'host':{'main'},'writer':{'main'}}[name]
            check(name+'_'+fn+'_bytes_exact_or_fully_disclosed_inverse',fn in changed or defs(text)[fn]==body)
        with (HERE/(name+'.V22.UNREADY.full.py')).open('x') as f:f.write(text)
    check('canonical70definitions',len(defs(originals['canonical']))==70)
    check('host1definition',len(defs(originals['host']))==1)
    check('writer7definitions',len(defs(originals['writer']))==7)
    cn=ast.parse(templates['canonical'])
    assignments={t.id:n.value for n in cn.body if isinstance(n,ast.Assign) for t in n.targets if isinstance(t,ast.Name)}
    for name in BUSINESS: check(name+'_still_None',isinstance(assignments[name],ast.Constant) and assignments[name].value is None)
    check('new_helper_admission_unknown_None',assignments['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA'].value is None)
    for key in ('TOTAL_WALL, STAGE_WALL, RSS = 1800, 600, 512','RESERVE, HISTORY_CAP, FREE_FLOOR = 2*2**30, 96*2**30, 8*2**30'):
        check('original_canonical_caps_'+key,key in templates['canonical'])
    for token in ("support.OLD_HELPER_SHA","helper.guard_admission(full)","full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)","resource.history_roots([str(HOST),str(SOURCE),str(OUT),str(TERMINAL)],support.ART)","resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)","support.archive_bytes((HOST,SOURCE,OUT,SOURCE_ARCHIVE))","for p in sorted(SOURCE_ARCHIVE.rglob('*')) if p.is_file()"):
        check('host_preserved_'+token,templates['host'].count(token)==originals['host'].count(token))
    for token in ('complete_namespace(root) for root in (H,S,O,T,D)','for root in (H,S,O,T,D,E)','source_inventory!=d[\'source_inventory\']','all_original_inputs_fresh_full_EOF_SHA7ID_unchanged','actual_root_host_launchargs','ACTUAL_CANONICAL_CHILD_MERGED_STDOUT_STDERR','actual_complete_creation_trace'):
        check('writer_preserved_'+token,templates['writer'].count(token)==originals['writer'].count(token))
    for p,prior in ((PLAN_PATH,pp),(Path(cp['path']),cp),(Path(hp['path']),hp),(WRITER_PARENT,wp),(Q_WRITER,qp),(HELPER_PATH,gp)):
        after,_=pin(p); check('parent_Source_full_EOF_SHA7ID_unchanged_'+str(p),after==prior)
    owners=defs(qr.decode())['validate_private_owner_controls']
    with (HERE/'validate_private_owner_controls.META_source_only.txt').open('x') as f:f.write(owners+'\n')
    proof={'schema':'V22_COMPLETE_CANONICAL_GENUINE_PREP_FINITE_UNREADY_SOURCE_INVERSES_V1','source_only':True,'all_checks_passed':True,'blockers':[], 'parent_sources':{'canonical':cp,'host':hp,'writer':wp},'plan_source':pp,'new_installed_helper_Source_only':gp,'new_helper_Q_path':None,'new_helper_Q_sha256':None,'six_future_business_pins':{n:None for n in BUSINESS},'exact_finite_transforms':transforms,'definitions':{n:list(defs(t)) for n,t in originals.items()},'original_check_call_order_preserved_after_finite_inverse':True,'changes_disclosed':{'canonical':'Exactly11 doc/globals/family/require_ready own-version anchors. Only require_ready own status literal differs; remaining69 definitions byte exact. No physics change.','host':'Exactly11 retarget anchors plus2 disclosed private Source binding additions. Main original ordered statements all restored by full inverse.','writer':'Exactly12 complete metadata-writer retarget anchors plus2 disclosed private Source binding additions. Six original non-main functions byte exact.'},'original_complete_genuine_PREP_caps':plan['genuine_PREP_caps'],'Source_inventory':'Complete original dynamic inventory; never substitute predicted fixed source count. Full metadata writer included before Root D freeze.','business_or_helper_or_guard_or_API_executed':False,'ART_payload_read':False}
    write_json('COMPLETE_SOURCE_INVERSES.json',proof)
    write_json('COMPLETE_SOURCE_SELF_REVIEW.json',{'schema':'V22_COMPLETE_CANONICAL_GENUINE_PREP_UNREADY_SOURCE_SELF_REVIEW_V1','status':'SOURCE_ONLY_PASS_UNREADY_NO_EXECUTION_OR_SCIENCE','source_only':True,'all_checks_passed':True,'blockers':[], 'check_count':len(checks),'checks':[{'check':x['check'],'pass':x['pass_']} for x in checks], 'future_new_helper_Q':None,'actual_new_business_success_pins':{n:None for n in BUSINESS}})
    write_json('ROOT_BINDING_SOURCE_CONSTANTS.json',{'schema':'V22_COMPLETE_PREP_FIXED_ROOT_SOURCE_BINDING_CONSTANTS_V1','UNREADY_DOC':UNREADY_DOC,'READY_DOC':READY_DOC,'helper':gp,'original_sources':{'canonical':cp,'host':hp,'writer':wp},'expected_Q_path':str(BASE/'Root_actual_complete_graph_private_owner_namespace_helper_admission_v22.json'),'expected_Q_sha256':None,'canonical_install_path':'/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v22.py','source_archive':str(BASE/'actual_complete_combined_prepare_v22_sources'),'receipt_archive':str(BASE/'actual_complete_combined_prepare_v22_receipts'),'caps':plan['genuine_PREP_caps'],'six_future_business_pins':{n:None for n in BUSINESS}})
    print(json.dumps({'source_only':True,'all_checks_passed':True,'check_count':len(checks),'canonical':pin(HERE/'canonical.V22.UNREADY.full.py')[0],'host':pin(HERE/'host.V22.UNREADY.full.py')[0],'writer':pin(HERE/'writer.V22.UNREADY.full.py')[0],'new_Q':None,'project_execution':False},allow_nan=False))

if __name__=='__main__': main()
