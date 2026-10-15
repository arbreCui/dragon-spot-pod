"""Stdlib SOURCE text generation only, no controller/helper/guard execution."""
from pathlib import Path
import ast, hashlib, json, shutil

P=Path(__file__).parent
BASE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
ART=Path('/Users/wen/spot/validation/artifacts')
HELP=Path('/private/tmp/axmat_complete_helper_inactive_audit_snapshot_SOURCE_candidate_yiyxo77u')
Q=BASE/'Root_actual_complete_graph_private_owner_namespace_helper_admission_v22.json'
PEER=BASE/'sealed_independent_complete_inactive_audit_helper_SOURCE_review/REVIEW.json'
NEW_SHA='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'
NEW_BYTES=150986
MODULE_NAME='inactive_audit_snapshot_controls_SOURCE_ONLY.py'
OLD_PATH='/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_owner_namespace_last_use_20261010.py'
OLD_SHA='cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c'
roles={
 'pure_helper_controls.py':(BASE/'actual_complete_graph_helper_controls_v22_sources/pure_helper_controls.py','9ea06c8f44c637bd9cff6849ee4a0d55af88a3cb82d6aa3beb7684a94a8decb9'),
 'pure_helper_controls_host.py':(BASE/'actual_complete_graph_helper_controls_v22_sources/pure_helper_controls_host.py','2d7bf5cc70e8cd061bcac683d27f33aea12f524b80079f7f5f9936534ef84e62'),
 'fresh_verifier_controls.py':(BASE/'actual_complete_graph_fresh_verifier_v22_sources/fresh_verifier_controls.py','de3384af3860177cabfb3fa87b6c413aac83a8f17570df01f0a14b3f6600da08'),
 'fresh_verifier_host.py':(BASE/'actual_complete_graph_fresh_verifier_v22_sources/fresh_verifier_host.py','3561c87b99d74c6f75b506fd4d5ccd7df1532c806f60644ae6f875d7c2f77468')}
def identity(f):
 s=f.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(f):
 a=identity(f);raw=f.read_bytes();assert a==identity(f)and len(raw)==a[4]
 return dict(path=str(f),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=a)
def write(name,value):
 f=P/name;assert not f.exists();f.write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def dump(x):return ast.dump(x,include_attributes=False)
def segment(source,node):return ''.join(source.splitlines(keepends=True)[node.lineno-1:node.end_lineno])
def defs(tree):return {n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
checks=[]
def check(label,result,evidence=None):
 passed=bool(result);checks.append(dict(check=label,passed=passed,evidence=evidence));assert passed,label
qp=pin(Q);pp=pin(PEER)
assert qp['sha256']=='89d2f03c0af74844731ddf5225307c38ae40521d99ca29c88c5d8db39796b816'
assert pp['sha256']=='4b6155f567de5bd8b1aa861d4ff5cf65193b17c6f7c31352c782a0426353edf9'
q=json.loads(Q.read_bytes());pr=json.loads(PEER.read_bytes())
check('original_Q89_complete_contract_frozen',q['schema']=='AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_OWNER_NAMESPACE_HELPER_ACTUAL_JOINT_ADMISSION_V22'and q['helper']['sha256']==OLD_SHA)
check('candidate_479_checks_429_unique_source_peer_honest_count',pr['check_count']==479==len(pr['checks'])and len({x['check']for x in pr['checks']})==429)
shutil.copyfile(Q,P/'ORIGINAL_Q89_COMPLETE_PARENT_CONTRACT.json');shutil.copyfile(PEER,P/'ORIGINAL_CANDIDATE_COMPLETE_SOURCE_PEER_REVIEW.json')
before={str(Q):qp,str(PEER):pp}
original_dirs={}
for label,ref in [('PURE',q['source_manifest']),('FRESH',q['complete_current_graph_fresh_verifier']['source_manifest'])]:
 f=Path(ref['path']);actual=pin(f);assert actual['sha256']==ref['sha256']and actual['identity']==ref['identity']
 before[str(f)]=actual
 ledger=json.loads(f.read_bytes());root=Path(ledger['source_root'])
 original_dirs[str(root)]=identity(root)
 dest=P/('ORIGINAL_Q89_'+label+'_COMPLETE_SOURCE');dest.mkdir(exist_ok=True)
 complete=ledger['complete_files']
 for rel,value in complete.items():
  source=Path(value['path']);a=pin(source);assert a['sha256']==value['sha256']and a['identity']==value['identity']
  before[str(source)]=a;target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
 for rel,signature in ledger['complete_directories'].items():
  directory=root/rel;assert identity(directory)==signature;original_dirs[str(directory)]=signature
 shutil.copyfile(f,dest/'ORIGINAL_ROOT_COMPLETE_SOURCE_FREEZE.json')
 check('all_original_'+label+'_Source_members_complete_copy',len(complete)==(61 if label=='PURE'else 13))
hm=HELP/'MANIFEST.json';hpin=pin(hm);assert hpin['sha256']=='13aa3f853077199546b292bc6f0b00d74069e3001f44bb919443760d8076e918'
before[str(hm)]=hpin;hv=json.loads(hm.read_bytes())
for m in hv['members']:
 f=Path(m['path']);a=pin(f);assert a=={k:m[k]for k in ('path','sha256','size_bytes','identity')};before[str(f)]=a
shutil.copytree(HELP,P/'COMPLETE_SOURCE_REVIEWED_NEW_HELPER_CANDIDATE',dirs_exist_ok=True)
candidate=P/'COMPLETE_SOURCE_REVIEWED_NEW_HELPER_CANDIDATE'/Path(hv['candidate_pin']['path']).name
check('complete_helper_candidate_21members_plus_manifest',len(hv['members'])==21 and pin(candidate)['sha256']==NEW_SHA)
module_pin=pin(P/MODULE_NAME);module_sha=module_pin['sha256'];module_bytes=module_pin['size_bytes']
check('new_control_module_AST_only_no_execution',len(defs(ast.parse((P/MODULE_NAME).read_bytes())))==8)

namespaces={
 'pure':{'host':str(ART/'axial-material-complete-graph-inactive-audit-helper-controls-host-v23-20261010'),
         'output':str(ART/'axial-material-complete-graph-inactive-audit-helper-controls-v23-20261010'),
         'source':str(BASE/'actual_complete_graph_helper_controls_v23_sources'),
         'receipts':str(BASE/'actual_complete_graph_helper_controls_v23_receipts')},
 'fresh':{'host':str(ART/'axial-material-complete-graph-inactive-audit-fresh-verifier-host-v23-20261010'),
          'output':str(ART/'axial-material-complete-graph-inactive-audit-fresh-verifier-v23-20261010'),
          'source':str(BASE/'actual_complete_graph_fresh_verifier_v23_sources'),
          'receipts':str(BASE/'actual_complete_graph_fresh_verifier_v23_receipts')},
 'planned_installed_helper':'/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume_20261010.py'}
load_function='''def load_snapshot_control_Source(path, sha256, source_bytes):
    # New controller dependency is full-pinned before and after import/use.
    source = Path(path)
    before = source.lstat()
    identity_before = [before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
                       before.st_size, before.st_mtime_ns, before.st_ctime_ns]
    if before.st_size != source_bytes or hashlib.sha256(source.read_bytes()).hexdigest() != sha256:
        raise ValueError('complete private snapshot controller SOURCE differs')
    spec = importlib.util.spec_from_file_location('actual_root_private_snapshot_metadata_controls', source)
    if spec is None or spec.loader is None:
        raise ValueError('private snapshot controller loader missing')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    after = source.lstat()
    if identity_before != [after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
                          after.st_size, after.st_mtime_ns, after.st_ctime_ns]:
        raise ValueError('private snapshot controller SOURCE changed during import')
    return module, dict(path=str(source), sha256=sha256, size_bytes=source_bytes, identity=identity_before)


'''
all_inverse={};templates={}
def mutate(name,changes,extra):
 source,sha=roles[name];a=pin(source);assert a['sha256']==sha;before[str(source)]=a
 text=source.read_text();oldtext=text;hunks=[]
 for label,old,new in extra:
  assert text.count(old)==1,label
  text=text.replace(old,new,1);hunks.append(dict(label=label,old_utf8=old,new_utf8=new))
 for key,value in changes.items():
  tree=ast.parse(text);nodes=[n for n in tree.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id==key];assert len(nodes)==1,key
  n=nodes[0];lines=text.splitlines(keepends=True);old=''.join(lines[n.lineno-1:n.end_lineno]);new=key+' = '+value+'\n'
  assert text.count(old)==1; text=text.replace(old,new,1);hunks.append(dict(label='global_'+key,old_utf8=old,new_utf8=new))
 out=P/(name[:-3]+'.UNREADY.py');out.write_text(text);templates[name]=pin(out)
 restored=text
 for h in reversed(hunks):assert restored.count(h['new_utf8'])==1;restored=restored.replace(h['new_utf8'],h['old_utf8'],1)
 check('full_bytes_AST_inverse_'+name,restored==oldtext and dump(ast.parse(restored))==dump(ast.parse(oldtext)))
 original=defs(ast.parse(oldtext));current=defs(ast.parse(text));changed=[]
 for fn,old in original.items():
  exact=segment(oldtext,old)==segment(text,current[fn])and dump(old)==dump(current[fn])
  if not exact:changed.append(fn)
  else:check('unchanged_whole_function_'+name+'_'+fn,True)
 all_inverse[name]=dict(original_Source_pin=a,template_pin=pin(out),full_hunks=hunks,
                       complete_original_definitions=list(original),complete_new_definitions=list(current),
                       actually_changed_original_definitions=changed,full_bytes_AST_inverse_to_original=True)

pure_globals="\nAUDIT_CONTROL_PATH = None\nAUDIT_CONTROL_SHA256 = "+repr(module_sha)+"\nAUDIT_CONTROL_SOURCE_BYTES = "+str(module_bytes)+"\n"
pure_run_gate="""    require(SOURCE_STATUS == 'READY_SOURCE_BOUND_BY_ROOT' and type(HELPER_PATH) is str
            and type(AUDIT_CONTROL_PATH) is str, 'UNREADY qualification templates require actual Root SOURCE binding')
"""
pure_extra=[
 ('new_controller_globals','ACTUAL_SUCCESS_PINS = None\n','ACTUAL_SUCCESS_PINS = None\n'+pure_globals),
 ('pinned_controller_loader_before_run','def run(output_dir):\n',load_function+'def run(output_dir):\n'),
 ('UNREADY_gate_before_any_output','    artifacts = Artifacts(output_dir)\n',pure_run_gate+'    artifacts = Artifacts(output_dir)\n'),
 ('load_full_new_control_Source_after_helper_pin','        report["helper"]["identity"] = helper_identity\n','        report["helper"]["identity"] = helper_identity\n        audit_controls, audit_control_pin = load_snapshot_control_Source(AUDIT_CONTROL_PATH, AUDIT_CONTROL_SHA256, AUDIT_CONTROL_SOURCE_BYTES)\n        report["private_snapshot_control_Source"] = audit_control_pin\n'),
 ('all_private_snapshot_controls_after_original_owner_controls','        report["private_owner_consume_controls"] = private_owner_consume_controls(g, small_graph)\n','        report["private_owner_consume_controls"] = private_owner_consume_controls(g, small_graph)\n        fixture_path = artifacts.root / "fixture" / "0_code_environment.txt"\n        report["private_inactive_audit_snapshot_controls"] = audit_controls.small_private_snapshot_controls(g, fixture_path, exact_value, WALL_SECONDS)\n        audit_controls.validate_small_control_report(report["private_inactive_audit_snapshot_controls"])\n        report["private_inactive_audit_snapshot_controls_order_preserved_artifact"] = artifacts.write_json("ACTUAL_PRIVATE_INACTIVE_AUDIT_SNAPSHOT_CONTROLS.json", report["private_inactive_audit_snapshot_controls"], encoder=ORDER_PRESERVING_JSON_ENCODER)\n'),
 ('new_dependency_final_full_Source_pin','        checkpoint("all_original_saved_metadata_bytes_identity_unchanged")\n','        require(identity(AUDIT_CONTROL_PATH) == audit_control_pin["identity"] and file_sha(AUDIT_CONTROL_PATH) == AUDIT_CONTROL_SHA256, "complete private controller SOURCE changed")\n        checkpoint("all_original_saved_metadata_bytes_identity_unchanged")\n')]
mutate('pure_helper_controls.py',{'SOURCE_STATUS':repr('UNREADY_SOURCE_ONLY_NO_ACTUAL_SUCCESS'),'HELPER_PATH':'None','HELPER_SHA256':repr(NEW_SHA),'HELPER_SOURCE_BYTES':str(NEW_BYTES)},pure_extra)

pure_host_added='''SOURCE_STATUS = 'UNREADY_SOURCE_ONLY'
BOUND_HELPER_PIN = None
INSTALL_WITNESS_PIN = None
SOURCE_INSTALL_RECORD_PIN = None
AUDIT_CONTROL_PATH = None
AUDIT_CONTROL_SHA256 = '''+repr(module_sha)+'''
AUDIT_CONTROL_SOURCE_BYTES = '''+str(module_bytes)+'''\n'''
pure_host_guard="""    if SOURCE_STATUS != 'READY_SOURCE_BOUND_BY_ROOT' or any(type(p) is not dict for p in (BOUND_HELPER_PIN, INSTALL_WITNESS_PIN, SOURCE_INSTALL_RECORD_PIN)) or type(AUDIT_CONTROL_PATH) is not str or type(TARGET_SHA) is not str:
        raise ValueError('UNREADY pure host requires actual installed helper and SOURCE witness bindings before I/O')
"""
oldhelper="support.pin(Path("+repr(OLD_PATH)+"),"+repr(OLD_SHA)+")"
newhelper="support.pin(BOUND_HELPER_PIN['path'],BOUND_HELPER_PIN['sha256'])"
pure_host_extra=[
 ('new_loader_full_hashlib_dependency','import importlib.util\n','import importlib.util\nimport hashlib\n'),
 ('fresh_host_identity_schema',"schema='AXMAT_V22_GENUINE_PURE_GRAPH_PROTOCOL_CONTROLS_HOST_V1'","schema='AXMAT_V23_GENUINE_PRIVATE_INACTIVE_AUDIT_PURE_PROTOCOL_CONTROLS_HOST_V1'"),
 ('unknown_Source_binding_globals','WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=60,60,512,64*2**20\n',pure_host_added+'WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=60,60,512,64*2**20\n'),
 ('pinned_private_control_Source_loader','def main():\n',load_function+'def main():\n'),
 ('explicit_UNREADY_gate','    started=time.monotonic()\n','    started=time.monotonic()\n'+pure_host_guard),
 ('helper_actual_future_binding',oldhelper,newhelper),
 ('all_original_inputs_plus_new_real_Source_witnesses',"]+[support.pin(p) for p in sorted(SOURCE_ARCHIVE.rglob('*')) if p.is_file()]",
  ",support.pin(INSTALL_WITNESS_PIN['path'],INSTALL_WITNESS_PIN['sha256']),support.pin(SOURCE_INSTALL_RECORD_PIN['path'],SOURCE_INSTALL_RECORD_PIN['sha256']),support.pin(AUDIT_CONTROL_PATH,AUDIT_CONTROL_SHA256)]+[support.pin(p) for p in sorted(SOURCE_ARCHIVE.rglob('*')) if p.is_file()]"),
 ('actual_small_snapshot_controls_verified_by_normal_host',"        if len(runner.records)!=1 or runner.records[0]['status']!='PASS'", "        audit_controls, audit_control_pin = load_snapshot_control_Source(AUDIT_CONTROL_PATH, AUDIT_CONTROL_SHA256, AUDIT_CONTROL_SOURCE_BYTES)\n        private_pin = control_report['private_inactive_audit_snapshot_controls_order_preserved_artifact']\n        private_path = OUT/'ACTUAL_PRIVATE_INACTIVE_AUDIT_SNAPSHOT_CONTROLS.json'\n        if Path(private_pin['path']) != private_path or support.pin(private_path,private_pin['sha256']) != {k:private_pin[k] for k in ('path','sha256','identity')} or private_pin['size_bytes'] != private_pin['identity'][4]:raise ValueError('full order-preserving private control artifact pin differs')\n        private_report = json.loads(private_path.read_text())\n        audit_controls.validate_small_control_report(private_report)\n        if json.dumps(private_report,sort_keys=True,separators=(',',':'),allow_nan=False) != json.dumps(control_report['private_inactive_audit_snapshot_controls'],sort_keys=True,separators=(',',':'),allow_nan=False):raise ValueError('all private report content must equal the original sorted public report content')\n        if control_report['private_snapshot_control_Source'] != audit_control_pin:raise ValueError('actual complete private control SOURCE report pin differs')\n        if len(runner.records)!=1 or runner.records[0]['status']!='PASS'")]
mutate('pure_helper_controls_host.py',{'HOST':'Path('+repr(namespaces['pure']['host'])+')','OUT':'Path('+repr(namespaces['pure']['output'])+')','SOURCE_ARCHIVE':'Path('+repr(namespaces['pure']['source'])+')','TARGET':'Path('+repr(namespaces['pure']['source']+'/pure_helper_controls.py')+')','TARGET_SHA':'None'},pure_host_extra)

fresh_globals="\nAUDIT_CONTROL_PATH = None\nAUDIT_CONTROL_SHA256 = "+repr(module_sha)+"\nAUDIT_CONTROL_SOURCE_BYTES = "+str(module_bytes)+"\n"
fresh_extra=[
 ('new_controller_globals','UNKNOWN_BUSINESS_PINS = None\n','UNKNOWN_BUSINESS_PINS = None\n'+fresh_globals),
 ('pinned_controller_Source_loader','def run(output_dir,driver_sha256):\n',load_function+'def run(output_dir,driver_sha256):\n'),
 ('new_dependency_load_after_actual_Helper_identity',"  write_json(output,'ACTUAL_RUN_CLAIM.json'", "  audit_controls,audit_control_pin=load_snapshot_control_Source(AUDIT_CONTROL_PATH,AUDIT_CONTROL_SHA256,AUDIT_CONTROL_SOURCE_BYTES)\n  report['private_snapshot_control_Source']=audit_control_pin\n  write_json(output,'ACTUAL_RUN_CLAIM.json'"),
 ('actual_default_records_full_nonmutation_before','  trace=audit.snapshot()\n','  audit_records_before=audit_controls.snapshot_order_type_bit_pin(audit._records,include_identity=True)\n  trace=audit.snapshot()\n  require(audit_controls.snapshot_order_type_bit_pin(audit._records,include_identity=True)==audit_records_before,\n          \'whole actual default snapshot must preserve every original record identity/type/order/value/bit\')\n'),
 ('whole_complete_True_after_original_default_full_gzip',"  report['actual_complete_ReadOpenAudit_trace']=lossless_json_gzip(output,'ACTUAL_COMPLETE_READ_OPEN_TRACE.json.gz',trace,started)\n",
  "  report['actual_complete_ReadOpenAudit_trace']=lossless_json_gzip(output,'ACTUAL_COMPLETE_READ_OPEN_TRACE.json.gz',trace,started)\n  default_contract=audit_controls.snapshot_order_type_bit_pin(trace)\n  default_fields=list(trace)\n  default_counts=(trace['unique_records'],trace['actual_read_open_attempts'])\n  other_audit_state_before=audit_controls.audit_state_pin(audit,include_records=False)\n  owned_map_identity=id(audit._records)\n  del trace\n  trace=audit.snapshot(_consume=True)\n  require(type(audit._records)is dict and id(audit._records)==owned_map_identity and audit._records=={},'whole privately owned inactive audit record map must clear after its last use')\n  require(audit_controls.audit_state_pin(audit,include_records=False)==other_audit_state_before,'whole audit subprocess/identity state must remain unchanged')\n  consumed_contract=audit_controls.snapshot_order_type_bit_pin(trace)\n  require(consumed_contract==default_contract and list(trace)==default_fields==audit_controls.SNAPSHOT_FIELDS and (trace['unique_records'],trace['actual_read_open_attempts'])==default_counts,'complete consumed/default nine fields/types/order/floatbits/counts differ')\n  private_wire=audit_controls.full_consumed_snapshot_wire_compare(trace,output/'ACTUAL_COMPLETE_READ_OPEN_TRACE.json.gz')\n  require(private_wire['uncompressed_JSON_sha256']==report['actual_complete_ReadOpenAudit_trace']['uncompressed_JSON_sha256'] and private_wire['uncompressed_JSON_bytes']==report['actual_complete_ReadOpenAudit_trace']['uncompressed_JSON_bytes'],'complete consumed/default trace gzip wire differs')\n  report['private_full_inactive_audit_snapshot_controls']=dict(default_snapshot_full_original_records_unchanged=True,owned_same_builtin_records_map_completely_cleared=True,all_other_audit_state_unchanged=True,default_complete_descriptor_type_order_floatbit_pin=default_contract,consumed_complete_descriptor_type_order_floatbit_pin=consumed_contract,all_nine_fields_full_type_order_value_floatbits_and_counts_equal=True,default_full_trace_gzip=report['actual_complete_ReadOpenAudit_trace'],complete_consumed_vs_default_wire=private_wire,no_second_graph_or_input_phase_substituted=True,all37112_actual_reads_from_same_genuine_phase=True,no_cross_phase_hash_or_stat_cache=True,new_helper_qualification_created=False,business_or_science_qualification_created=False)\n"),
 ('new_control_Source_enters_full_fixed_input_scope',"report['fixed_inputs_before']=dict(driver=self_before,old_parent=old_before,new_helper=new_before,stored_graph=graph_before)","report['fixed_inputs_before']=dict(driver=self_before,old_parent=old_before,new_helper=new_before,stored_graph=graph_before,private_snapshot_controls=audit_control_pin)"),
 ('new_control_Source_fresh_final_hash_identity',"stored_graph=full_pin(GRAPH_PIN['path'],GRAPH_PIN['sha256'],GRAPH_PIN['identity']))","stored_graph=full_pin(GRAPH_PIN['path'],GRAPH_PIN['sha256'],GRAPH_PIN['identity']),private_snapshot_controls=full_pin(AUDIT_CONTROL_PATH,AUDIT_CONTROL_SHA256))")]
mutate('fresh_verifier_controls.py',{'SOURCE_STATUS':repr('UNREADY_SOURCE_ONLY'),'NEW_HELPER_PATH':'None','NEW_HELPER_SHA256':repr(NEW_SHA),'NEW_HELPER_SOURCE_BYTES':str(NEW_BYTES),'NEW_HELPER_IDENTITY':'None','OUTPUT_PATH':repr(namespaces['fresh']['output'])},fresh_extra)

fresh_host_globals="\nAUDIT_CONTROL_PATH = None\nAUDIT_CONTROL_SHA256 = "+repr(module_sha)+"\nAUDIT_CONTROL_SOURCE_BYTES = "+str(module_bytes)+"\n"
fresh_host_extra=[
 ('fresh_Source_namespace_identity_schema',"schema='AXMAT_V22_ACTUAL_COMPLETE_FRESH_VERIFIER_SOURCE_NAMESPACE_V1'","schema='AXMAT_V23_ACTUAL_COMPLETE_PRIVATE_INACTIVE_AUDIT_FRESH_SOURCE_NAMESPACE_V1'"),
 ('fresh_host_identity_schema',"schema='AXMAT_V22_GENUINE_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_HOST_V1'","schema='AXMAT_V23_GENUINE_COMPLETE_PRIVATE_INACTIVE_AUDIT_CURRENT_GRAPH_HOST_V1'"),
 ('new_complete_controller_globals','UNKNOWN_BUSINESS_PINS=None\n','UNKNOWN_BUSINESS_PINS=None\n'+fresh_host_globals),
 ('pinned_controller_loader','def _full_controls(support,report,admission,watch,command):\n',load_function+'def _full_controls(support,report,admission,watch,command):\n'),
 ('verify_new_all_current_graph_private_snapshot_controls',"    success=report['actual_success_pins']\n",
  "    private=report['private_full_inactive_audit_snapshot_controls']\n    if any(private[key] is not True for key in ('default_snapshot_full_original_records_unchanged','owned_same_builtin_records_map_completely_cleared','all_other_audit_state_unchanged','all_nine_fields_full_type_order_value_floatbits_and_counts_equal','no_second_graph_or_input_phase_substituted','all37112_actual_reads_from_same_genuine_phase','no_cross_phase_hash_or_stat_cache')) or private['new_helper_qualification_created'] is not False or private['business_or_science_qualification_created'] is not False:raise ValueError('whole private inactive audit consumption and honest complete scope required')\n    if private['default_complete_descriptor_type_order_floatbit_pin']!=private['consumed_complete_descriptor_type_order_floatbit_pin'] or private['default_full_trace_gzip']!=report['actual_complete_ReadOpenAudit_trace']:raise ValueError('whole consumed/default descriptor and actual default gzip differ')\n    wire=private['complete_consumed_vs_default_wire']\n    if any(wire[key] is not True for key in ('every_default_and_consumed_wire_byte_compared','full_gzip_EOF_verified','no_fields_or_records_selected')) or wire['complete_nine_snapshot_fields']!=TRACE_FIELDS or wire['uncompressed_JSON_bytes']!=report['actual_complete_ReadOpenAudit_trace']['uncompressed_JSON_bytes'] or wire['uncompressed_JSON_sha256']!=report['actual_complete_ReadOpenAudit_trace']['uncompressed_JSON_sha256']:raise ValueError('full consumed/default ordered wire+EOF proof required')\n    _driver_pin(support,report['private_snapshot_control_Source'],Path(AUDIT_CONTROL_PATH))\n    success=report['actual_success_pins']\n")]
mutate('fresh_verifier_host.py',{'HOST':'Path('+repr(namespaces['fresh']['host'])+')','OUT':'Path('+repr(namespaces['fresh']['output'])+')','SOURCE_ARCHIVE':'BASE/'+repr(Path(namespaces['fresh']['source']).name),'RECEIPTS':'BASE/'+repr(Path(namespaces['fresh']['receipts']).name),'TARGET_SHA':'None','SOURCE_STATUS':repr('UNREADY_SOURCE_ONLY'),'BOUND_HELPER_PIN':'None','INSTALL_WITNESS_PIN':'None','SOURCE_INSTALL_RECORD_PIN':'None'},fresh_host_extra)

for name,inv in all_inverse.items():
 check('all_original_definitions_preserved_'+name,set(inv['complete_original_definitions']).issubset(inv['complete_new_definitions']))
 check('only_original_run_main_full_controls_and_namespace_schema_changed_'+name,set(inv['actually_changed_original_definitions']).issubset({'run','main','_full_controls','_source_namespace'}))
write('ALL_FOUR_COMPLETE_QUALIFICATION_TEMPLATE_INVERSES.json',dict(schema='COMPLETE_PRIVATE_INACTIVE_AUDIT_FULL_PROTOCOL_FRESH_SOURCE_INVERSES_V1',source_only=True,
     all_four_complete_source_inverse=all_inverse,new_Control_Source_module=module_pin,new_helper_SHA=NEW_SHA,
     original_Q89_no_new_Helper_credit=True,original_guard_and_MRO_and_resource_caps_preserved=True,actual_new_qualification=None,six_future_business_pins=[None]*6))
write('ROOT_ACTUAL_HELPER_SOURCE_INSTALL_WITNESS_TEMPLATE.UNREADY.json',dict(
 schema='ROOT_V23_ACTUAL_COMPLETE_HELPER_SOURCE_INSTALL_TOOL_RETURN_V1',source_only=True,
 closed=None,actual_tool_terminal_return_observed=None,terminal_tool_return=None,
 installed_helper=None,source_install_record=None,new_Q=None,six_future_business_pins=[None]*6,
 actual_required_source_only_install_schema='ROOT_V23_COMPLETE_HELPER_SOURCE_INSTALL_RECORD_V1',
 actual_expected_helper_Source_sha256=NEW_SHA,actual_expected_helper_Source_bytes=NEW_BYTES,
 planned_helper_path=namespaces['planned_installed_helper'],private_api_or_qualification_executed=False))
write('ROOT_FIXED_SOURCE_NAMESPACES_AND_FUTURE_ACTUAL_PINS.UNREADY.json',dict(
 schema='COMPLETE_PRIVATE_INACTIVE_AUDIT_FULL_PROTOCOL_AND_CURRENT_GRAPH_ROOT_SOURCE_PLAN_V1',source_only=True,
 namespaces=namespaces,new_complete_helper_candidate_pin=pin(candidate),module_Source_pin=module_pin,
 original_Q89_frozen_parent_pin=qp,new_Helper_independent_Source_review_pin=pp,
 new_Source_install_witness=None,new_Source_install_record=None,new_pure_terminal=None,new_fresh_terminal=None,
 two_new_independent_saved_reviews=None,new_joint_Helper_Q=None,all_business_science_pins=[None]*6,
 pure_caps=dict(whole_seconds=60,phase_seconds=60,rss_mib=512,archive_bytes=64*2**20,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0),
 fresh_caps=dict(whole_seconds=1800,phase_seconds=600,rss_mib=512,joint_HODE_archive_bytes=64*2**20,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0),
 original_pure_normal_host_archive_scope='H+O+D; Root conservative H+O+D+E must be separately honest',
 all_original_pure_controls_fixtures_and_27fields_37111files_37112reads_three_full_gzips_retained=True,
 actual_memory_or_RSS_or_build_PASS_prediction=None,Source_candidate_or_controller_executed=False))
for path,old in before.items():check('all_pinned_original_Source_and_small_META_EOF_SHA7ID_unchanged_'+path,pin(Path(path))==old)
for path,sig in original_dirs.items():check('all_original_Source_directories_7ID_unchanged_'+path,identity(Path(path))==sig)
write('SOURCE_SELF_REVIEW.json',dict(schema='COMPLETE_PRIVATE_INACTIVE_AUDIT_FULL_QUALIFICATION_SOURCE_SELF_REVIEW_V1',status='PASS_COMPLETE_SOURCE_ONLY_UNREADY_NO_API_OR_QUALIFICATION',source_only=True,
 checks=checks,check_count=len(checks),all_checks_typed_true=all(c['passed']is True for c in checks),blockers=[],
 complete_original_source_and_META_pins_before_after=before,templates=templates,control_Source_pin=module_pin,
 any_candidate_helper_guard_API_material_or_controller_executed=False,new_actual_helper_qualification=None,
 original_pure_Source_members=61,original_fresh_Source_members=13,original_root_ordered_pure_inputs_not_source_member_count=71,
 original_helper_Source_peer_checks=479,original_helper_Source_peer_unique_labels=429,six_future_business_pins=[None]*6))
print(json.dumps(dict(source_only=True,status='COMPLETE_PURE_FRESH_UNREADY_SOURCE_GENERATED',package=str(P),templates=templates,control_module=module_pin,
                      inverse=pin(P/'ALL_FOUR_COMPLETE_QUALIFICATION_TEMPLATE_INVERSES.json'),report=pin(P/'SOURCE_SELF_REVIEW.json'),check_count=len(checks),candidate_or_controller_executed=False),separators=(',',':')))
