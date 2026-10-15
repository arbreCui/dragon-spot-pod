"""Generate finite SOURCE design metadata; never import/call/compile reviewed code."""
from pathlib import Path
import ast
import hashlib
import json
import stat

PACKAGE=Path(__file__).parent
WRAPPER=PACKAGE/'transfer_full_AB_rawrecord_UNREADY.py'
NR=Path('/Users/wen/dragon-5.1/Dragon/irena_core/colorset_rebuild_20260527/ce_compare/fullpitch_pnl_s30_b0_closure_v1_20260907/native_records.py')
SR=Path('/Users/wen/dragon-5.1/Dragon/irena_core/colorset_rebuild_20260527/ce_compare/mc2027_csd_rr_evidence_v1_20260909/paper_parallel_20260910/finegroup_acceptance/stream_records.py')
checks=[]
def checked(name,value):
 if type(value)is not bool or not value:raise ValueError(name)
 checks.append({'name':name,'value':True})
def pin(path):
 s=path.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 checked('ordinary bounded SOURCE only '+str(path),stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_size<2*2**20)
 with path.open('rb')as f:
  raw=f.read();checked('complete SOURCE EOF '+str(path),f.read(1)==b'')
 t=path.lstat();after=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
 checked('SOURCE stable full EOF exact7ID '+str(path),before==after and len(raw)==before[4])
 return raw,{'path':str(path),'sha256':hashlib.sha256(raw).hexdigest(),'size_bytes':len(raw),'identity':before}
def write_json(name,value):
 with(PACKAGE/name).open('x')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
def defs(raw):return [n.name for n in ast.parse(raw).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]

nr,nrpin=pin(NR);sr,srpin=pin(SR)
before,beforepin=pin(WRAPPER)
candidate=before.decode()
nr_old="'native_records': (Path('"+str(NR)+"'), 'TO_BE_BOUND_BY_SOURCE_GENERATOR')"
sr_old="'stream_records': (Path('"+str(SR)+"'), 'TO_BE_BOUND_BY_SOURCE_GENERATOR')"
hunks=[{'old':nr_old,'new':nr_old.replace('TO_BE_BOUND_BY_SOURCE_GENERATOR',nrpin['sha256'])},{'old':sr_old,'new':sr_old.replace('TO_BE_BOUND_BY_SOURCE_GENERATOR',srpin['sha256'])}]
for h in hunks:
 checked('unique full reader SOURCE pin retarget',candidate.count(h['old'])==1)
 candidate=candidate.replace(h['old'],h['new'],1)
restored=candidate
for h in reversed(hunks):
 checked('unique full reader pin inverse',restored.count(h['new'])==1)
 restored=restored.replace(h['new'],h['old'],1)
checked('complete 2hunk byte inverse',restored.encode()==before)
checked('complete 2hunk AST inverse',ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(before),include_attributes=False))
with(PACKAGE/'wrapper_before_reader_pin_SOURCE.txt').open('xb')as f:f.write(before)
with WRAPPER.open('wb')as f:f.write(candidate.encode())
with(PACKAGE/'original_native_records_full.SOURCE.py').open('xb')as f:f.write(nr)
with(PACKAGE/'original_stream_records_full.SOURCE.py').open('xb')as f:f.write(sr)
wrapper,wrapperpin=pin(WRAPPER)
tree=ast.parse(wrapper)
source=wrapper.decode()
g={n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
future=['SOURCE_QUALIFICATION_SHA256','ACTUAL_ROOT_BINDING_RECEIPT_SHA256','ACTUAL_TRANSFER_QUALIFICATION_SHA256','REACTION_MULTIPLICITY_QUALIFICATION_SHA256','ACTUAL_SCIENTIFIC_REFERENCE_SHA256']
checked('all actual qualification/runtime/science pins None',all(ast.literal_eval(g[x])is None for x in future))
checked('SOURCE status is still UNREADY',ast.literal_eval(g['SOURCE_STATUS'])=='UNREADY_SOURCE_ONLY_ROOT_TRUE_BINDING_AND_GENUINE_SUPERVISOR_REQUIRED')
checked('complete declared dimensions370/8/3/32',ast.literal_eval(g['EXPECTED_DIMENSIONS'])==(370,8,3,32))
calls=[n for n in ast.walk(tree)if isinstance(n,ast.Call)]
decode_calls=[n for n in calls if isinstance(n.func,ast.Attribute)and isinstance(n.func.value,ast.Name)and n.func.value.id=='first_reader'and n.func.attr=='decode']
stream_calls=[n for n in calls if isinstance(n.func,ast.Attribute)and isinstance(n.func.value,ast.Name)and n.func.value.id=='second_reader'and n.func.attr=='decode_stream']
checked('one full native decode(raw) exact API/default',len(decode_calls)==1 and len(decode_calls[0].args)==1 and isinstance(decode_calls[0].args[0],ast.Name)and decode_calls[0].args[0].id=='raw'and decode_calls[0].keywords==[])
checked('one full stream decode(binaryiterator) exact default, no selector',len(stream_calls)==1 and len(stream_calls[0].args)==1 and isinstance(stream_calls[0].args[0],ast.Name)and stream_calls[0].args[0].id=='binary_lines'and stream_calls[0].keywords==[])
checked('no reaction subset function called',not any(isinstance(n.func,(ast.Attribute,ast.Name))and (n.func.attr if isinstance(n.func,ast.Attribute)else n.func.id)=='reaction_selection'for n in calls))
checked('no numpy/scipy dense arrays or scattering expansion called',not any(isinstance(n.func,ast.Attribute)and n.func.attr in ('scatter','zeros','ones','asarray','solve','normalize')for n in calls))
checked('no subprocess/multiprocessing/project API imported',all(not isinstance(n,ast.ImportFrom)and all(a.name in ('argparse','gc','hashlib','importlib.util','itertools','json','math','os','re','stat','struct','sys','time')for a in n.names)if isinstance(n,ast.Import)else n.module=='pathlib'for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom))))
checked('old thread five single-thread variables retained',ast.literal_eval(g['THREAD_KEYS'])==('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'))
transfer_node=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='transfer_state')
deleted_first=next(n.lineno for n in ast.walk(transfer_node)if isinstance(n,ast.Delete)and any(isinstance(t,ast.Name)and t.id=='records'for t in n.targets))
deleted_raw=next(n.lineno for n in ast.walk(transfer_node)if isinstance(n,ast.Delete)and any(isinstance(t,ast.Name)and t.id=='raw'for t in n.targets))
deleted_second=next(n.lineno for n in ast.walk(transfer_node)if isinstance(n,ast.Delete)and any(isinstance(t,ast.Name)and t.id=='second_records'for t in n.targets))
checked('release first complete records before second full decoder',decode_calls[0].lineno<deleted_raw<deleted_first<stream_calls[0].lineno<deleted_second)
for anchor in ("records = first_reader.decode(raw)","second_records, second_stats = second_reader.decode_stream(binary_lines)","stats['all_records_validated'] == stats['retained_records'] == len(records) == expected_records", "payload.read(len(chunk)) == chunk", "struct.pack('<fd', x, x)","struct.pack('<d', x)", "payload.read(1) == b''", "actual is None", "missing_real_record_no_substitution", "raw_unreferenced_padding_retained_without_interpretation", "contiguous_packing_required_or_assumed", "SIGNATURE_not_L_MACROLIB", "8*32", "for moment in range(3)", "for destination in range(1,371)", "for state in ('A','B')", "original child600 stage", "genuine_supervisor_watch_verified_here':False", "external_actual_ROOT_EXIT0_closed_and_genuine512_watch_review_still_required':True"):
 checked('full scope/bit/rejection/admission source anchor '+anchor,anchor in source)
false_science=ast.literal_eval(g['FALSE_SCIENCE'])
checked('all scientific/physics/AAA/ABA/build scope flags typedFalse',all(type(v)is bool and v is False for v in false_science.values())and {'AAA_accuracy_qualified','ABA_admitted','physical_neutron_balance_qualified','scientific_accuracy_qualified'}<=set(false_science))
for raw,name,required in ((nr,'native_records',{'decode','macro','field','scatter'}),(sr,'stream_records',{'decode_stream','reaction_selection'})):
 checked('all original reader definitions retained '+name,required<=set(defs(raw)))
 _,again=pin(NR if name=='native_records'else SR)
 checked('original complete reader SOURCE unchanged '+name,again==(nrpin if name=='native_records'else srpin))
with(PACKAGE/'full_reader_SOURCE_pin_inverse.json').open('x')as f:json.dump({'schema':'CURRENT150_AB_RAWRECORD_WRAPPER_TWO_KNOWN_READER_SOURCE_PIN_INVERSE_V1','before':beforepin,'after':wrapperpin,'hunks':hunks,'full_byte_AST_inverse':True,'known_original_reader_SOURCE':{'native_records':nrpin,'stream_records':srpin},'no_actual_input_or_success_binding':True,'SOURCE_only':True},f,indent=2);f.write('\n')

caps={'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'joint_archive_bytes':2*2**30,'history_bytes':96*2**30,'free_floor_bytes':8*2**30,'threads':1,'children_at_once':1,'retries':0}
input_template={s:{'path':'/Users/wen/spot/validation/artifacts/axial-material-inputs-20261003/'+s+'/macro.ascii','sha256':None,'size_bytes':None,'identity':None}for s in ('A','B')}
binding={'schema':'ROOT_ACTUAL_CURRENT150_AB_FULL_RAWRECORD_TRANSFER_SOURCE_BINDING_V1','status':'UNREADY_TEMPLATE_NOT_ACTUAL_ROOT_BINDING','source_only':True,'scientific_qualification_created':False,'source_qualification_sha256':None,'original_caps':caps,'python':{'path':'/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','sha256':None,'size_bytes':None,'identity':None},'inputs':input_template,'readers':{'native_records':nrpin,'stream_records':srpin},'public_reader_calls':['native_records.decode(raw_bytes)','stream_records.decode_stream(binary_iterator)'],'full_default_retention':True,'final_READY_wrapper_SHA_in_this_binding':None,'final_READY_wrapper_SHA_must_be_pinned_externally_by_real_genuine_host':True,'cannot_run_this_unknown_pin_template':True}
write_json('ROOT_BINDING_TEMPLATE.UNREADY.json',binding)

layout={'schema':'CURRENT150_AB_COMPLETE_RAWRECORD_DATA_LAYOUT_SOURCE_DESIGN_V1','status':'UNEXECUTED_COMPLETE_LAYOUT_SOURCE_ONLY','rawrecord_order':'original physical raw headers and original decoder insertion order; never sorted or filtered','states_order':['A','B'],'per_state_outputs':[
 {'path':'original_macro.ascii','encoding':'exact original complete ASCII bytes; full EOF/SHA7ID provenance','scope':'all header/name/width/padding/payload/closing bytes'},
 {'path':'complete_raw_header_span_inventory.jsonl','encoding':'one row per physical header including all closes','fields':['entry','physical_header_index','record_index for record','path plus explicit str/int types','level','flags','kind','declared_count','raw_begin_byte','raw_end_byte','raw_span_sha256','original_character_bytes/width'],'scope':'contiguous full original byte coverage; no string-padding/header loss'},
 {'path':'complete_typed_record_index.jsonl','encoding':'one row per complete decoded record in original key insertion order','fields':['original complete record metadata','typed_payload_begin_byte','typed_payload_end_byte','typed_payload_sha256','python_value_type','payload_encoding'],'scope':'all roots/GROUPs/moments/components/unknown extra records'},
 {'path':'complete_typed_payload.bin','magic':'AXMAT_FULL_TYPED_LCM_V1 followed by zero byte','record_payload_encodings':{'kind0/10/99':'original count in index; no bytes','kind1':'each exact arbitrary signed integer as ASCII decimal plus newline; kind/count preserved','kind2':'12 bytes per value: little-endian IEEE REAL32 then exact ASCII-decoded Python IEEE float64; original signed zeros retained; overflow rejected','kind4':'8 bytes per value: little-endian IEEE float64','kind3':'decoded ASCII string; exact original widths/padding remain in original raw span'},'scope':'both independent readers compare every byte and every complete key/kind/type/count/order; no monolithic serialized numeric JSON'},
 {'path':'full_required_field_contract.jsonl','encoding':'every required root/group/state/fission/moment field outcome, no samples','scope':'actual missing/wrongkind/wrongcount stays a real recorded gap, never filled'},
 {'path':'full_sparse_reference_spans.jsonl','encoding':'all370 destination×3moment×8mixture spans or explicit full-field gap','scope':'source=IJJS-jnd+1, rawindex=IPOS+jnd-1; no assumed contiguous packing or removal of padding'},
 {'path':'small_state_metadata.json','encoding':'bounded2MiB small count/provenance/gap summary; complete record data stored in the separate files above','scope':'full40 STATE vector and all actual GROUP field names; all physical/scientific admissions false'},
 ],'top_outputs':['complete_payload_manifest.json','ACTUAL_TRANSFER_REPORT.json or retained FAILED_TRANSFER_REPORT.json'],'same_input_scope':{'groups':370,'mixtures':8,'moments':3,'fission_components':32,'fission_memory_index':'(component-1)*8+mixture; mixture inner/component outer from original LIBDEN/MGXEXP/SPOLIB SOURCE; root FISSIONINDEX and pergroup NUSIGF/CHI all retained'},'true_missing_semantics':'all true physical reaction channels/multiplicity and transport correction require separate exact producer/data evidence; no Sigma_total-minus-production absorption claim','ASCII_bit_limit':'typed IEEE bits of the stored full ASCII are retained/compared; this is not independent evidence of all original XSM/LCM in-memory bits','state_lifetime':'full first decoder raw/dict -> spool -> release -> full second default decode -> complete compare -> release -> next state','no_dense_scattering_or_graph_materialization':True,'physical_boundary_for_future_reference':'current150cm; same A/B temperatures/compositions/geometry, white radial albedo1, axial vacuum; original3% unchanged','all_raw_bit_and_transfer_actual_success_fields':None,'all_scientific_flags':false_science}
write_json('COMPLETE_DATA_LAYOUT.json',layout)

steps=[
 'SOURCE ONLY: independent peer must review this entire UNREADY wrapper, all original reader SOURCE bytes/pins, full layout and actual Source AST results. No parser/payload/native/physics has run.',
 'Root first closes the current business stage. No simultaneous business/numeric child. It declares one fresh HOST/OUT and D/E SOURCE/receipts namespace; no reuse/retry.',
 'Root performs actual standard-library full EOF/SHA/exact7ID pins of both actual existing macro.ascii inputs, both original reader files, fixed Python executable and SOURCE qualification receipt. No new materials, TONE or library processing; do not pin a historical substituted macro.',
 'Root creates a true binding record from ROOT_BINDING_TEMPLATE.UNREADY.json with exact real values. The binding must not contain a final READY wrapper SHA: doing so would make a circular hash dependency. Freeze this immutable binding, then compute its actual SHA.',
 'Root makes a separate READY SOURCE derivative of the fixed UNREADY wrapper by exactly three global-line bindings: SOURCE_STATUS to READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED, SOURCE_QUALIFICATION_SHA256 to the true Source qualification SHA, ACTUAL_ROOT_BINDING_RECEIPT_SHA256 to the actual immutable binding SHA. All functions/caps/data layout unchanged; actual transfer/reaction/scientific success pins remain None. Fresh peer verifies complete three-hunk byte+AST inverse before any execution.',
 'Root freezes complete SOURCE archive before launch. Existing genuine619/705/38de supervisor/resource classes and MRO must be retained; no replacement fake watcher. Actual host alone binds final READY wrapper SHA externally, all Source/binding/input/Python/library environment pins and full original caps.',
 'Planned caps unchanged: whole1800s/one stage600s/RSS512MiB/one numeric child/one thread/no retry; joint HOST+OUT+SOURCE+D/E receipts+runtime source2GiB, history96GiB/free8GiB. Unknown actual resource admission remains None. All history_roots arguments must be strict ART descendants; D/E outsideART are counted separately in joint archive bytes, never injected as illegal history_roots.',
 'Root launches the future fixed wrapper only as the genuine single own child: Python -B READY_WRAPPER --binding ACTUAL_BINDING --binding-sha256 REAL_SHA --output-dir ONE_USE_OUT --expected-parent-pid REAL_GENUINE_HOST_PID. Use the original five thread variables set1 and original unoptimized/unprofiled environment. This SOURCE package runs no command and manufactures no PID or tool closure.',
 'The actual transfer archives A raw bytes, inventories all spans, executes native_records.decode(raw bytes), spools every record and required-field/sparse outcomes, releases first objects, executes stream_records.decode_stream(binary iterator) with no selector, compares all spooled bytes/types/order, releases second objects, then processes B identically. Both readers retain every record; no complete A/B pair is held simultaneously.',
 'Needed actual software controls under the same declared child/caps before admission: a separately declared small full-record protocol fixture with every LCM kind, nested str/int key order, both signed zeros, REAL32/REAL64 and padded characters; malformed duplicate/truncated/nonfinite payload rejects; missing/partial moment/fission/TRANC field reports a gap without synthesis. These SOURCE plans are not executed evidence and must not replace either full A/B run.',
 'Root waits for a true terminal typed integer exit code and CLOSED/no live session. On any source/payload/parser/resource failure, retain complete actual failure/partial raw outputs and stop, no same-namespace retry. No PASS/RSS/closure can be inferred from Source checks.',
 'After actual typed EXIT0, a finite independent saved-evidence review must verify genuine watcher/ownPID/parentPID/MRO/caps/cleanup, both original input+allSource fullEOF SHA7ID before/after, complete output manifest, all full default records/types/order/bit/padding/header/span coverage and actual metadata gaps. Root outer terminal and actual full joint/history/free resource counts are external receipts, never fabricated by the wrapper.',
 'Only actual complete software raw transfer may be admitted. True reaction-event/multiplicity and transport-correction semantics, original native LCMMemory bit equivalence, complete370x8x3/32fission finite150coupled transport and original3%AAA/ABA gates remain unqualified. Real missing records stop scientific input admission; never fill zeros, truncate dimensions, clip, renormalize or fit CE.',
]
with(PACKAGE/'ROOT_FUTURE_TRUE_STEPS.txt').open('x')as f:f.write('\n\n'.join(steps)+'\n')
future_controls={'schema':'CURRENT150_AB_RAWRECORD_FUTURE_PROTOCOL_CONTROLS_SOURCE_PLAN_V1','status':'UNEXECUTED_SOURCE_PLAN_NOT_ACTUAL_PROTOCOL_PASS','positive_scope':['all LCM0/10/99/1/2/3/4 record kinds','nested original str/int key order','REAL32 plus parser64 and REAL64 both signed zero bits','raw padded4-byte character chunks','complete raw header/closing spans','all raw referenced spans and unused padding retained'],'negative_scope':['duplicate key rejects','truncated numeric/character/header/closing rejects','nonfinite real rejects','nonrepresentable REAL32 rejects without repair','missing or partial moment/32component/TRANC produces actual scientific gap; raw full scope retained'],'run_only_by_future_root_genuine_single_child':True,'all_actual_pass_fail_receipts':None,'scientific_accuracy_balance_AAA_ABA_qualified':False}
write_json('FUTURE_PROTOCOL_CONTROLS.UNEXECUTED.json',future_controls)
report={'schema':'CURRENT150_AB_FULL_RAWRECORD_WRAPPER_FINITE_SOURCE_CHECK_REPORT_V1','status':'UNREADY_SOURCE_DESIGN_AST_HASH_CHECKS_ONLY_NOT_PEER_ADMISSION_OR_RUNTIME','wrapper':wrapperpin,'all_source_checks':checks,'all_checks_typed_true':True,'blockers':[],'complete_original_readers':{'native_records':nrpin,'stream_records':srpin},'wrapper_complete_definitions':defs(wrapper),'original_reader_definitions':{'native_records':defs(nr),'stream_records':defs(sr)},'declared_original_caps':caps,'future_qualification_fields':{x:None for x in future},'root_default_full_reader_binding_design':binding,'unready_wrapper_imported_or_called':False,'reader_imported_or_called':False,'compile_run_business_native_numeric_executed':False,'material_payload_read':False,'canonical_or_frozen_namespace_written':False,'actual_runtime_Scientific_success_created':False}
write_json('SOURCE_CHECKS.json',report)
print(json.dumps({'status':report['status'],'package':str(PACKAGE),'wrapper':wrapperpin,'checks':len(checks),'actual_reader_or_wrapper_API_executed':False,'material_payload_read':False,'future_success_pins_bound':False}))
