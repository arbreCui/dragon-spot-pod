from pathlib import Path
import ast,difflib,hashlib,json,os,stat,struct
D=Path('/private/tmp/axmat_v14_helper_protocol_formal_admission_readonly_review_20261010')
S=Path('/Users/wen/spot/validation/axial_material/complete_environment_streaming_sha_source_v14_20261010')
A=S/'Root_actual_helper_controls_admission.json'
F=Path('/private/tmp/axmat_v14_streaming_sha_component_source_draft_receipt_size_fix_20261010/prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14.py')
M=Path('/private/tmp/axmat_v14_streaming_sha_component_source_draft_hardlink_and_defs_fix_20261010')/F.name
pins={}
def ident(p):
 x=Path(p).lstat();return [x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def pin(p,want=None):
 p=Path(p);i=ident(p);assert stat.S_ISREG(i[2]);h=sha(p);assert ident(p)==i
 if want is not None:assert h==want,(p,h,want)
 pins[str(p)]={'path':str(p),'sha256':h,'identity':i};return pins[str(p)]
def uq(items):
 d={}
 for k,v in items:assert k not in d;d[k]=v
 return d
def read(p,want=None):
 pin(p,want);return json.loads(Path(p).read_text(),object_pairs_hook=uq,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def equal(a,b):
 assert type(a) is type(b)
 if isinstance(a,dict):
  assert a.keys()==b.keys()
  for k in a:equal(a[k],b[k])
 elif isinstance(a,list):
  assert len(a)==len(b)
  for x,y in zip(a,b):equal(x,y)
 elif isinstance(a,float):assert struct.pack('>d',a)==struct.pack('>d',b)
 else:assert a==b
def namespace(p):
 d={'files':{},'symlinks':{},'directories':[]};ids={}
 for parent,dirs,names in os.walk(p,followlinks=False):
  d['directories'].append(str(Path(parent).relative_to(p)))
  for name in dirs+names:
   q=Path(parent)/name;i=ident(q);rel=str(q.relative_to(p));ids[rel]=i
   if stat.S_ISLNK(i[2]):d['symlinks'][rel]=os.readlink(q)
   elif stat.S_ISREG(i[2]):d['files'][rel]=pin(q)['sha256']
   else:assert stat.S_ISDIR(i[2])
 d['directories'].sort();return d,ids
a=read(A,'1537bc75d4f6c3b06cffbfcf7bd4f0dd0ffefa2f151e19381c71361430ff8fa0')
assert a['schema']=='AXMAT_COMPLETE_ENVIRONMENT_STREAMING_SHA_HELPER_CONTROLS_ADMISSION_V14'
assert a['status']=='PASS_COMPLETE_HELPER_CONTROLS_ONLY'
assert type(a['actual_tool_exit_code']) is int and a['actual_tool_exit_code']==0 and a['actual_tool_session_closed'] is True
assert a['meaningful_control_groups']==21 and a['buffer_bytes']==4194304
for k in ('complete_full_SHA_per_unique_literal_per_environment','same_call_same_literal_memo_only','full_seven_identity_rechecks_required','same_seven_identity_mutation_rejected','native_alias_policy_preserved','default_environment_rejections_retained','outside_context_default_digest_behavior_unchanged'):assert a[k] is True
for k in ('cross_stage_SHA_reuse','different_literal_SHA_reuse','mathematics_changed','MRO_modified','actual_positive_RSS_sample_observed','full86_component_qualified','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'):assert a[k] is False
assert type(a['files']) is dict and len(a['files'])==117 and str(A) not in a['files']
for literal,want in a['files'].items():
 assert Path(literal).is_absolute() and '..' not in Path(literal).parts and len(want)==64
 pin(literal,want)
inventories={};identities={};total=0
for rootkey,invkey in [('control_root','control_inventory'),('host_root','host_inventory')]:
 p=Path(a[rootkey]);assert not p.is_symlink() and p.is_dir()
 inv,ids=namespace(p);equal(inv,a[invkey]);inventories[invkey]=inv;identities[rootkey]=ids
 for rel,h in inv['files'].items():assert a['files'][str(p/rel)]==h;total+=ident(p/rel)[4]
assert total==a['complete_control_plus_host_bytes']==21572739 and total<64*2**20
cr=Path(a['control_root']);hr=Path(a['host_root'])
for name in ('hardlink.bin','first.bin'):
 p=cr/'identical_SHA_distinct_files_and_hardlink_literals'/name;assert ident(p)[3]==2
assert ident(cr/'identical_SHA_distinct_files_and_hardlink_literals/hardlink.bin')[:2]==ident(cr/'identical_SHA_distinct_files_and_hardlink_literals/first.bin')[:2]
assert inventories['control_inventory']['symlinks']['preserved_namespace_link_word_change/namespace/link']=='missing.bin'
assert (cr/'preserved_namespace_link_word_change/namespace/link').is_symlink() and not (cr/'preserved_namespace_link_word_change/namespace/link').exists()
docs={}
for k in ('helper','source_patch_proof','actual_terminal_receipt','actual_result','actual_host_result','actual_stage_journal','actual_child_watchdog','actual_full_stdout','actual_full_stderr','independent_full_actual_evidence_review','independent_actual_review_tool_return'):
 r=a[k];assert set(r)=={'path','sha256'} and a['files'][r['path']]==r['sha256'];pin(r['path'],r['sha256'])
 if k not in ('helper','actual_full_stderr'):docs[k]=read(r['path'],r['sha256'])
receipt=docs['actual_terminal_receipt'];assert receipt['action']=='fixtures' and receipt['session_closed'] is True
assert type(receipt['terminal_result']['exit_code']) is int and receipt['terminal_result']['exit_code']==0
assert receipt['terminal_result']['chunk_id']=='9c9d85';equal(receipt['call_history'][-1],receipt['terminal_result'])
for k,doc in [('stdout','actual_full_stdout'),('stderr','actual_full_stderr')]:
 r=receipt[k];equal({q:r[q] for q in ('path','sha256')},a[doc]);assert type(r['size_bytes']) is int and r['size_bytes']==ident(r['path'])[4]
assert receipt['stderr']['size_bytes']==0
result=docs['actual_result'];host=docs['actual_host_result'];watch=docs['actual_child_watchdog'];journal=docs['actual_stage_journal']
assert result['status']=='PASS_HELPER_PROTOCOL_ONLY' and len(result['groups'])==21
for g in result['groups']:equal(g,read(cr/g['name']/'case_result.json'));assert g['status']=='PASS_HELPER_PROTOCOL_ONLY'
equal(journal['stages'],host['stage_records']);equal(watch,host['watchdog']);assert len(journal['stages'])==1
assert watch['returncode']==0 and type(watch['returncode']) is int and watch['limit_failure'] is None
assert watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True
assert watch['rss_cap_mib']==512 and 0<watch['wall_cap_seconds']<=journal['stages'][0]['wall_cap_seconds']<=120
assert watch['sampled_peak_rss_mib']==a['sampled_peak_rss_mib_as_recorded']==0.0
assert host['whole_elapsed_seconds']==a['whole_elapsed_seconds'] and a['whole_elapsed_seconds']<120
own=docs['independent_full_actual_evidence_review'];ownreceipt=docs['independent_actual_review_tool_return']
assert own['status']=='PASS_HELPER_PROTOCOL_ONLY' and own['groups']==21
assert ownreceipt['exit_code']==0 and type(ownreceipt['exit_code']) is int and ownreceipt['closed'] is True
assert ownreceipt['initial_chunk_id']=='c0c38a' and ownreceipt['terminal_chunk_id']=='d200ce'
assert ownreceipt['report']['sha256']==a['independent_full_actual_evidence_review']['sha256']
equal(a['RSS_interpretation'],own['RSS_interpretation'])
equal(a['actual_performance_comparison']['independent_summary'],own['historical_environment_summary'])
assert a['actual_performance_comparison']['material_time_gain_proven'] is False
h=a['actual_performance_comparison']['Root_actual_terminal'];r=read(h['path'],h['sha256']);assert r['terminal_result']['exit_code']==0 and r['session_closed'] is True

# Pure source compatibility: do not execute/import the proposed gate.
pin(F,'e1cbc96cd7c46dc99b2a0a477b609abf70ea0c4338d5d0ed8840165945e5f35a')
pin(M,'c505c5637a7027008e30f125ee0b9c949b25de5f2c8a019ae6712f6a5a4d54c0')
ft=F.read_text();mt=M.read_text()
old="""            or receipt['action'] != 'fixtures' or receipt['stdout'] != controls['actual_full_stdout']
            or receipt['stderr'] != controls['actual_full_stderr']):"""
new="""            or receipt['action'] != 'fixtures' or {key: receipt['stdout'][key] for key in ('path', 'sha256')} != controls['actual_full_stdout']
            or type(receipt['stdout']['size_bytes']) is not int
            or receipt['stdout']['size_bytes'] != require(controls['actual_full_stdout']['path'], controls['actual_full_stdout']['sha256']).stat().st_size
            or {key: receipt['stderr'][key] for key in ('path', 'sha256')} != controls['actual_full_stderr']
            or type(receipt['stderr']['size_bytes']) is not int
            or receipt['stderr']['size_bytes'] != require(controls['actual_full_stderr']['path'], controls['actual_full_stderr']['sha256']).stat().st_size):"""
assert ft.count(new)==mt.count(old)==1 and ft.replace(new,old)==mt
proof=read(F.parent/'COMPLETE_INVERSE_PROOF.json');parent=Path(proof['parent']['path']);pin(parent,proof['parent']['sha256'])
inverse=ft
for edit in reversed(proof['edits']):
 assert inverse.count(edit['new'])==edit['count'];inverse=inverse.replace(edit['new'],edit['old'])
assert inverse==parent.read_text()
def scope(t):
 return {n.name:ast.get_source_segment(t,n) for n in ast.parse(t).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
fs=scope(ft);ms=scope(mt);ps=scope(parent.read_text())
assert set(fs)==set(ms) and [k for k in fs if fs[k]!=ms[k]]==['stream_environment_helper_source_admission']
for n in ['control_audit','stage_commands','stage_labels','component_controls_audit','sender_controls_audit','keycodec_controls_audit','binary_audit','archive_forecast','check_watch']:assert fs[n]==ps[n]
tree=ast.parse(ft);assignments={n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
for n in ('STREAM_ENVIRONMENT_HELPER_SHA','STREAM_ENVIRONMENT_SOURCE_PROOF_SHA','STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA','FUTURE_ACTUAL_BUILD_TERMINAL_SHA'):assert isinstance(assignments[n],ast.Constant) and assignments[n].value is None
assert ast.literal_eval(assignments['SOURCE_STATUS']).startswith('UNREADY')
gate=fs['stream_environment_helper_source_admission']
required_controls={n.slice.value for n in ast.walk(ast.parse(gate)) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='controls' and isinstance(n.slice,ast.Constant) and isinstance(n.slice.value,str)}
assert required_controls<=set(a)
assert "receipt['stdout']['size_bytes']" in gate and "receipt['stderr']['size_bytes']" in gate
assert "controls['schema'] != 'AXMAT_COMPLETE_ENVIRONMENT_STREAMING_SHA_HELPER_CONTROLS_ADMISSION_V14'" in gate
for key,ids in identities.items():assert namespace(Path(a[key]))[1]==ids
for p,row in pins.items():assert ident(p)==row['identity'] and sha(p)==row['sha256']
source_evidence={'schema':'AXMAT_V14_FORMAL_HELPER_ADMISSION_AND_RECEIPT_COMPATIBILITY_SOURCE_EVIDENCE_V1','files':list(pins.values()),'exact_inventories':inventories,'literal_7identities':identities,'e1_to_c505_inverse_regions':[{'old':old,'new':new,'count':1}],'e1_to_V13_complete_inverse_regions':len(proof['edits']),'original_86_math_and_stage_functions_byteexact':True,'new_three_pins_unknown':True,'required_admission_fields':sorted(required_controls),'gate_executed':False,'initial_small_inspection_error':{'chunk_id':'bc9bcd','exit_code':1,'reason':'The readonly display assumed an inventories field; actual schema has control_inventory and host_inventory. No helper/factory/control was executed or changed.'}}
(D/'EVIDENCE.json').write_text(json.dumps(source_evidence,indent=2)+'\n')
report={'schema':'AXMAT_V14_FORMAL_HELPER_PROTOCOL_ADMISSION_READONLY_REVIEW_V1','status':'PASS_HELPER_PROTOCOL_ADMISSION_ONLY','admission_sha256':sha(A),'admission_files':117,'whole_control_inventory_files':len(inventories['control_inventory']['files']),'whole_host_inventory_files':len(inventories['host_inventory']['files']),'full_SHA_each_hardlink_literal_separately':True,'broken_link_fixture_preserved':True,'complete_bytes':total,'actual_closed_Root_exit_code':0,'independent_actual_reader_exit_code':0,'tiny_RSS_zero_not_measured_peak':True,'no_material_time_gain_proven':True,'e1cb_receipt_fields_source_compatible':True,'e1cb_entire_inverse_to_c505':True,'e1cb_entire_inverse_to_V13':True,'original_86_math_and_stages_unchanged':True,'factory_UNREADY_three_new_pins_None':True,'helper_or_factory_loaded_or_gate_executed':False,'fixtures_or_history_rerun':False,'historical_28GB_read':False,'project_written':False,'full86_component_qualified':False,'native_RSS_verified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'fresh_full_pin_count':len(pins),'evidence_sha256':sha(D/'EVIDENCE.json')}
(D/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
(D/'REPORT.txt').write_text('正式辅助协议凭证独立只读核验通过：117个完整字节引脚、两完整命名空间、21控制与真实Root/独审退出闭环均保持；两hardlink字面独立hash，故意broken link保持。\ne1cb仅对真实stdout/stderr的path+sha投影并校验size，完整逆回c505及V13，数学/86原控制未改；三个新pin仍None，工厂仍UNREADY且未执行门。\n仅helper协议资格，无明显计时收益，RSS0.0不是实测进程峰；不授86/native/AAA/ABA。\n')
print(json.dumps({'status':report['status'],'REPORT_sha256':sha(D/'REPORT.json'),'EVIDENCE_sha256':sha(D/'EVIDENCE.json'),'full_pins':len(pins)},indent=2))
