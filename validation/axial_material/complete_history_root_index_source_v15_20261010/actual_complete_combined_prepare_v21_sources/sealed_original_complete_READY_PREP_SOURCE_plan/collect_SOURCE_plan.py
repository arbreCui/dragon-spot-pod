"""Finite SOURCE plan only; no READY candidate, binder, host or API execution."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

OUT=Path(__file__).parent
P=Path('/private/tmp/axmat_v21_complete_runtime_UNREADY_source_design_20261010')
BASE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
OLD_D=BASE/'actual_complete_combined_prepare_v20_sources'
OLD_GENERATOR=BASE/'actual_complete_combined_prepare_v18_sources/sealed_READY_source_binding/source_binding_generator.py'
OLD_Q=BASE/'Root_actual_complete_graph_helper_controls_admission_v17.json'
pins=[]
checks=[]

def check(name,value):
 if type(value)is not bool or not value:raise AssertionError(name)
 checks.append(dict(name=name,value=value))
def identity(path):
 s=path.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def read(path,sha=None,ident=None):
 before=identity(path)
 check('ordinary private SOURCE/META '+str(path),stat.S_ISREG(before[2])and before[3]==1 and not path.is_symlink())
 raw=path.read_bytes();after=identity(path)
 check('complete EOF SOURCE SHA7ID stable '+str(path),before==after and len(raw)==before[4])
 digest=hashlib.sha256(raw).hexdigest()
 if sha is not None:check('exact SOURCE SHA '+str(path),digest==sha)
 if ident is not None:check('exact SOURCE7ID '+str(path),before==ident)
 pin=dict(path=str(path),sha256=digest,identity=before,size_bytes=len(raw));pins.append(pin)
 return raw,pin
def assignments(tree):return {n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
def defs(tree):return {n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}

mr,mp=read(P/'sealed_manifest.json','d11f2dd71e1cc87d85d51345ace6dfa42b727f4065043efa8b44c2db0270f7ce')
m=json.loads(mr)
check('complete sealed V21 UNREADY10member SOURCE package',m['member_count']==10 and sorted(x.name for x in P.iterdir())==sorted([x['relative']for x in m['files']]+['sealed_manifest.json']))
raws={}
for entry in m['files']:
 raw,pin=read(P/entry['relative'],entry['sha256'],entry['identity7']);raws[entry['relative']]=raw
 check('complete old frozen member length '+entry['relative'],pin['size_bytes']==entry['size_bytes'])
raw=raws['prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.UNREADY.py']
t=ast.parse(raw);g=assignments(t);d=defs(t)
check('full candidate75969 original181071 bytes',hashlib.sha256(raw).hexdigest()=='75969eafb9e1eead11e25d8838c6e3be13ea64babdc56ee222252a5e11bded62' and len(raw)==181071)
check('all original70 top definitions retained',len(d)==70)
future=['FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']
check('six future business/native pins allNone',all(ast.literal_eval(g[name])is None for name in future))
check('unknown helper qualification pinNone',ast.literal_eval(g['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA'])is None)
graph_node=dict(zip([k.value for k in g['INPUT_HELPERS'].keys],g['INPUT_HELPERS'].values))['graph']
check('graph newhelper SHA remainsNone',isinstance(graph_node,ast.Tuple)and graph_node.elts[1].value is None)
q_occurrences=[n for n in ast.walk(t)if isinstance(n,ast.Name)and n.id=='FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA']
check('canonical Q onlyassignment andnonzero gate no Qobjectread',len(q_occurrences)==2 and sum(isinstance(n,ast.Call)and ast.unparse(n.func)=='nonzero_sha'and len(n.args)==1 and ast.unparse(n.args[0])=='FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA'for n in ast.walk(t))==1)

gr,gp=read(OLD_GENERATOR,'4d54cc988d47918017bdabcf082918bf528cf0ef2a94000a7a082cec68989f0f')
qr,qp=read(OLD_Q,'d49036e0a0fd396dd9550e81fd310b74442a867e7a4cc36ff2b16bf70a9c6bf8')
q=json.loads(qr)
check('original Qsmall metadata only exact historical schema/status',q['schema']=='AXMAT_ROOT_COMPLETE_GRAPH_HELPER_ACTUAL_CONTROLS_ADMISSION_V17' and q['status']=='QUALIFIED_PURE_COMPLETE_GRAPH_HELPER_METADATA_PROTOCOL_ONLY_V17')
host,hostpin=read(OLD_D/'combined_prepare_host.py','a9d4a1eadae7f6f346138029ea4bbd5e9a5c26c0b5efbb8d256c08b06e757de1')
host_generator,hgpin=read(OLD_D/'sealed_normal_PREP_host_source_binding/generate_prepare_host.py','099c61aaf99433a11b23453c0995aafb60c96d8dd48de8c20eeaeca1fa2cf477')
writer,writerpin=read(OLD_D/'sealed_metadata_writer_source_binding/write_actual_prepare_terminal.py','af0c633fa31f29517fa5b8d8dbebdd16d7d255a1c3203047ecd79ef02722b539')
old_directory=identity(OLD_D)
old_names=sorted(str(x.relative_to(OLD_D))for x in OLD_D.rglob('*')if x.is_file())
check('old37SOURCE shape exact allfiles',len(old_names)==37)
old_source_pins=[]
for name in old_names:
 _,pin=read(OLD_D/name);old_source_pins.append(dict(relative=name,**pin))

hs=host.decode();ht=ast.parse(host);hdefs=defs(ht)
inp=next(n for n in ast.walk(ht)if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='inputs'for x in n.targets))
old_helper_call="support.pin(Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py'),'bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6')"
old_q_call="support.pin(Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/Root_actual_complete_graph_helper_controls_admission_v17.json'),'d49036e0a0fd396dd9550e81fd310b74442a867e7a4cc36ff2b16bf70a9c6bf8')"
check('original PREP2 exact pin anchors once',hs.count(old_helper_call)==1 and hs.count(old_q_call)==1 and inp.lineno==36)
new_helper_call="support.pin(Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py'),'dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7')"
old_ready=ast.literal_eval(g['DRAFT_STATUS'])
ready_status='READY_REVIEWED_V21_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'
check('exactexisting require_ready READY string',ready_status in ast.get_source_segment(raw.decode(),d['require_ready']))
ready_hunks=[
 dict(kind='truthful qualification/source-only docstring only',before=raw.decode().splitlines()[0],after=None,required_after='Root actual Q schema/status/path/SHA and successful original60 protocol+fullfresh+savedreviews must be actual before wording claims them. This V21 business family remains unexecuted; six futurebusiness pinsNone.'),
 dict(kind='DRAFT_STATUS exactexisting READY',before='DRAFT_STATUS = '+repr(old_ready),after='DRAFT_STATUS = '+repr(ready_status),binding_branch_not_executed=True),
 dict(kind='INPUT_HELPERS graph Source SHA binding',before="'graph': (ROOT/'validation/axial_material/combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py',None)",after="'graph': (ROOT/'validation/axial_material/combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py','dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7')",actual_SOURCE_only_not_newQ=True),
 dict(kind='actual new Q SHA mandatory binding',before='FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA = None',after=None,actual_newQ_path=None,actual_newQ_sha256=None,required_after='same global set to exact lowercase fullSHA of Root actual new helper Q provided later; no placeholder accepted')]
for h in ready_hunks:check('unique exact planned READY anchor '+h['kind'],raw.decode().count(h['before'])==1)
host_retargets=[
 ('axial-material-complete-combined-prepare-host-v20-20261010','axial-material-complete-combined-prepare-host-v21-20261010'),
 ('prepare_sender_window_root_index_graph_trace_table_combined_runtime_v20.py','prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.py'),
 ('566939e3fbc7eddcc2b5af324a6dd11e97f83b033994e36389f7819d06084de3',None),
 ('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v20-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v21-20261010'),
 ('axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v20-20261010','axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v21-20261010'),
 ('axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v20-20261010','axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v21-20261010'),
 ('actual_complete_combined_prepare_v20_sources','actual_complete_combined_prepare_v21_sources'),
 ('AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V20_DECLARATION_V1','AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V21_DECLARATION_V1'),
 ('AXMAT_V20_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1','AXMAT_V21_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1')]
for old,new in host_retargets:check('unique9normal host retarget anchor '+old,hs.count(old)==1)
host_hunks=[dict(before=old,after=new,actual_READY_factory_SHA_required=new is None)for old,new in host_retargets]+[dict(before=old_helper_call,after=new_helper_call),dict(before=old_q_call,after=None,actual_newQ_path=None,actual_newQ_sha256=None,required_after='support.pin(Path(actualRootQpath),actualRootQsha) rendered from real future Rootargv')]

original_Q_reader_source='\n'.join(gr.decode().splitlines()[59:92])+'\n'
report={
 'schema':'AXMAT_V21_EXACT_READY_AND_GENUINE_PREP_SOURCE_PLAN_V1',
 'status':'UNREADY_WAITING_REAL_NEW_Q_AND_SAVED_REVIEWS_SOURCE_PLAN_ONLY',
 'candidate':m['candidate'],'sealed_UNREADY_manifest':mp,
 'original_READY_generator_SOURCE':gp,'original_Q_metadata':qp,
 'original_READY_Q_reader_complete_SOURCE_lines60_to92':original_Q_reader_source,
 'original_Q_contract_keys':list(q),
 'original_Q_reference_names':['helper','actual_root_terminal','actual_controls_summary','actual_host_result','actual_control_report','complete_namespace_manifest','independent_actual_review','independent_actual_review_tool_return','source_manifest'],
 'original_Q_reader_contract':{
  'schema_status_historical_only':{'schema':q['schema'],'status':q['status']},
  'reference_rules':'Full ordinary nonalias EOF SHA/bytes/exact7ID for nonART SOURCE/smallMETA; ART references only bound by full actual Q in this SOURCE task, never read ART/numeric.',
  'scope_false_keys':['supervisor_class_or_MRO_modified','profile_used','fresh_production_graph_created','fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'],
  'full_protocol_true_keys':['original_and_fresh_small_producer_values_types_order_floatbits_exact','all_caller_mutable_identity_and_subtype_attributes_unchanged','complete_old_graph_two_normal_strict_entrances_exact','new_creation_trace_not_substituted_into_old_graph','full_json_types_order_floatbits_and_values_retained','default_source_nonmutation'],
  'original_counts_required':{'accepted_str_subtype_groups':2,'small_codec_rejections':61,'complete_old_trace':62332,'complete_old_requirement_rows':237767,'complete_old_canonical_files':36776,'complete_new_creation_trace_records':63379},
  'original_caps':q['original_caps'],
  'terminal_rules':'terminal_return_observed/session_closed true; retries0; exactinteger exit0 and no live session. Original d1734f/session59994/e2794c identifiers prove OLD q only and must never be copied as new actual evidence.',
  'savedreview_rules':'Original schema/source inverse/helperSHA matched complete saved review; future Root newQ must retain honest corresponding current saved reviews and actual newhelper SHA, not hardcode historical PASS strings.'},
 'actual_newQ':None,'accepted_future_newQ_schema':None,'accepted_future_newQ_status':None,
 'newQ_future_required_evidence':['actual original60 fullpure protocol Roottyped0CLOSED + savedreview','actual V21b completecurrentfresh27fields/37112reads/4positive3reject/3completegzip Roottyped0CLOSED + savedreview','same actualcanonical dc01 147870bytes/exact7ID and Sourceproofs','all newbusiness/native/AAA/ABA/science flagsfalse'],
 'canonical_existing_Q_read_scope':'Only nonzero global SHA guard exists. Canonical does not read/validate the Q object. Do not claim a new canonical Q predicate or expand original functions.',
 'exact_canonical_READY_hunks':ready_hunks,
 'normal_PREP_direct_parent_host':hostpin,'normal_PREP_parent_generator':hgpin,
 'normal_PREP_metadata_writer_Source_parent':writerpin,
 'normal_PREP_exact11atomic_hunks_plan':host_hunks,
 'normal_PREP_original2helperQpins_SOURCE_line':inp.lineno,
 'normal_PREP_original_inputs_complete_assignment':ast.get_source_segment(hs,inp),
 'old_PREP_SOURCE_37_complete_inventory':old_source_pins,
 'old_PREP_input_shape':{'SOURCEfiles':37,'inputs_base_count':5,'helper_and_Q_count':2,'input_sources_count':44,'hpin_rpin_extra_fresh_checks':2,'total_original_freshly_rechecked_inputs':46},
 'future_SOURCE_inventory_policy':'Retain all UNREADY+READY+sourceinverse+actualRootSOURCEtoolreturns+independentreviews+normalhost+metadatawriter+installationrecord SOURCE evidence. Full dynamically observed Source namespace must be preserved/frozen and all members pinned; 37 and46 are old actual shape, never a truncation limit for V21.',
 'budgets':{'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'HOST_SOURCE_OUT_SOURCEarchive_joint_reserve_bytes':2*2**30,'wholeINPUT_metadata_bytes':64*2**20,'history_bytes':96*2**30,'free_floor_bytes':8*2**30,'threads':1,'children':1,'retries':0},
 'next_exact_steps':['Root completes both actual saved evidence reviews and seals actual newQ','Explicit RootnewQ path+SHA/schema/status/actualhelper proof allows metadata-only binding design; no current bindingbranch exists or ran','Bind only4canonical global/doc hunks; prove entire byte inverse to75969 and all70definitions unchanged, six businesspinsNone','Retarget originala9d4 genuine PREP host only9namespace/SHA+2helperQfullpin anchors; fullbyte inverse to a9d4, genuineguard/MRO/caps/calls unchanged','Retarget actualmetadatawriterSource with originalwhole namespace/pins capture unchanged and preserve full SOURCE packages','Independent finiteSOURCE review; Root actualSOURCEinstall and fullEOFSHA7ID prelaunch resources/absences','Only then one fresh bounded PREP; actual buildseal/wholeINPUT/native success remainunknown until separate real stages'],
 'full_original_five_build_stages_retained':True,'two_complete_fresh_graph_and_specs_reads_retained':True,
 'all70definitions_remain_source_unmodified':True,
 'checks':checks,'SOURCE_pins_before_after':pins[:],
 'six_future_business_pins':{name:None for name in future},
 'READY_source_generated':False,'binder_generated_or_run':False,'canonical_project_ART_or_frozen_written':False,
 'business_helper_guard_API_called':False,'ART_graph_numeric_payload_or_history_read':False,
 'old_failed_namespaces_modified':False,'newQ_qualified_or_bound':False,
 'whole_business_INPUT_qualified':False,'native_RSS_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'physical_balance_qualified':False}
for pin in list(pins):
 _,after=read(Path(pin['path']),pin['sha256'],pin['identity']);check('finite Source/META final reread unchanged '+pin['path'],after==pin)
check('oldcompleteSource namespace stillsame37 files anddirectory',identity(OLD_D)==old_directory and sorted(str(x.relative_to(OLD_D))for x in OLD_D.rglob('*')if x.is_file())==old_names)
report['checks']=checks
with (OUT/'SOURCE_PLAN.json').open('x')as stream:json.dump(report,stream,indent=2,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())
print(json.dumps({'status':report['status'],'report_path':str(OUT/'SOURCE_PLAN.json'),'report_sha256':hashlib.sha256((OUT/'SOURCE_PLAN.json').read_bytes()).hexdigest(),'checks':len(checks),'canonical_bindings_planned':4,'genuine_host_atomic_retargets_planned':11,'old_SOURCE_files':37,'old_full_input_checks':46,'newQ':None,'READY_generated':False,'helper_guard_API_called':False},allow_nan=False))
