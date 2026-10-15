from pathlib import Path
import ast,hashlib,json
base=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010');old=base/'actual_component_execution_receipts/formal_admission_host.py';assert hashlib.sha256(old.read_bytes()).hexdigest()=='95fd82a372cbd937a2becf5e8224c2e9f6443ba26feae8d2f720cbb3bf62604f'
s=old.read_text();proof=[]
def replace(a,b,n=1):
 global s
 assert s.count(a)==n,(a,s.count(a),n)
 s=s.replace(a,b);proof.append({'before':a,'after':b,'occurrences':n})
replace('One normal canonical read-only component admission, unchanged genuine guard.','One normal complete combined preparation under the unchanged genuine guard.')
replace("HOST=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-component-admission-host-v15-20261010')","HOST=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-combined-prepare-host-v15-20261010')\nTARGET=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_table_combined_runtime_v15.py')\nTARGET_SHA='0ea1e6295d8efb34bdccf1dcbde9e56654a5fcd6a190c372f181c5611564d382'\nSOURCE=Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-table-combined-source-v15-20261010')\nOUT=Path('/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-table-combined-runtime-v15-20261010')\nTERMINAL=Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-table-combined-terminal-v15-20261010')")
replace('WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,64*2**20','WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30')
replace("if os.path.lexists(HOST):raise ValueError('fresh one-use admission host required; no retry')","if any(os.path.lexists(p) for p in (HOST,SOURCE,OUT,TERMINAL)):raise ValueError('fresh combined preparation namespaces required; no retry')")
replace('inputs=[support_pin,support.pin(support.TARGET,support.TARGET_SHA),','inputs=[support_pin,support.pin(TARGET,TARGET_SHA),support.pin(support.TARGET,support.TARGET_SHA),')
replace('roots=resource.history_roots([str(HOST),str(support.SOURCE),str(support.OUT),str(support.TERMINAL)],support.ART)','roots=resource.history_roots([str(HOST),str(SOURCE),str(OUT),str(TERMINAL)],support.ART)')
replace("command=[str(support.PYTHON),str(support.TARGET),'admit','--sha256',SEAL_SHA,'--terminal-evidence',str(support.TERMINAL/'terminal_return.json'),'--terminal-evidence-sha256',TERM_SHA]","command=[str(support.PYTHON),str(TARGET),'prepare-build']")
replace("runner.execute(HOST/'run','admit',command,STAGE_CAP)","runner.execute(HOST/'run','prepare',command,STAGE_CAP)")
replace("log=HOST/'run/admit.log';watch_path=HOST/'run/admit.watchdog.json'","log=HOST/'run/prepare.log';watch_path=HOST/'run/prepare.watchdog.json'")
replace("        if admission['schema']!='AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_PRODUCTION_RUNTIME_INPUT_ADMISSION_V15' or admission['admission']!='SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_RUNTIME_INPUT_ONLY_V15' or admission['build_seal_sha256']!=SEAL_SHA:\n            raise ValueError('real complete normal canonical admission required')\n        if any(admission[k] is not False for k in ('native_RSS_proof_obtained','AAA_accuracy_qualified','ABA_admitted','actual_full_FLU_entry_executed','production_pipeline_prepared')):\n            raise ValueError('runtime INPUT only science boundaries required')","        declaration=OUT/'declaration.json';d=json.loads(declaration.read_text())\n        if admission!=dict(declaration=str(declaration),declaration_sha256=support.pin(declaration)['sha256']):raise ValueError('normal complete combined prepare return required')\n        if d['schema']!='AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TABLE_COMBINED_RUNTIME_V15_DECLARATION_V1' or len(d['stages'])!=5 or (d['total_wall_seconds'],d['stage_wall_seconds'],d['rss_cap_mib'],d['archive_reserve_bytes'])!=(1800,600,512,2*2**30):raise ValueError('original complete five stages and caps required')\n        if any(d[k] is not False for k in ('native_transport_executed','mathematical_controls_newly_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted','production_pipeline_prepared')):raise ValueError('combined prepare INPUT only boundaries required')\n        if os.path.lexists(TERMINAL) or (OUT/'seal.json').exists():raise ValueError('prepare cannot fabricate terminal or successful build')")
replace('archived=support.archive_bytes((HOST,))','archived=support.archive_bytes((HOST,SOURCE,OUT))')
replace("schema='AXMAT_V15_GENUINE_COMPONENT_ADMISSION_HOST_V1',status='ACTUAL_COMPONENT_RUNTIME_INPUT_ADMISSION_EXTERNAL_ROOT_REQUIRED'","schema='AXMAT_V15_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1',status='ACTUAL_COMPLETE_COMBINED_PREPARE_EXTERNAL_ROOT_REQUIRED'")
replace('actual_admission_stdout=support.pin(log),actual_watchdog=support.pin(watch_path)','actual_prepare_stdout=support.pin(log),actual_declaration=support.pin(declaration),actual_source_admission=support.pin(SOURCE/\'source_admission.json\'),actual_watchdog=support.pin(watch_path)')
replace('if support.archive_bytes((HOST,))>=ARCHIVE_CAP','if support.archive_bytes((HOST,SOURCE,OUT))>=ARCHIVE_CAP')
replace('actual_admission_stdout=support.pin(log),actual_external_Root_terminal_required=True','actual_prepare_stdout=support.pin(log),actual_external_Root_terminal_required=True')
replace('COMPONENT_ADMISSION','COMBINED_PREPARATION',2)
replace('FAILED_READONLY_ADMISSION_NO_RETRY','FAILED_COMPLETE_COMBINED_PREPARE_NO_RETRY')
p=base/'actual_combined_prepare_sources/combined_prepare_host.py';ast.parse(s);compile(s,str(p),'exec')
with p.open('x') as f:f.write(s)
inv=s
for v in reversed(proof):assert inv.count(v['after'])==v['occurrences'];inv=inv.replace(v['after'],v['before'])
assert inv==old.read_text()
record={'schema':'AXMAT_V15_COMBINED_PREPARE_HOST_FINITE_SOURCE_ADAPTATION','parent':{'path':str(old),'sha256':hashlib.sha256(old.read_bytes()).hexdigest()},'candidate':{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},'finite_replacements':proof,'full_inverse_byteexact':True,'original_genuine_guard_and_caps_preserved':True,'business_started':False}
with (p.parent/'source_adaptation_proof.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps({'candidate':record['candidate'],'finite_replacements':len(proof),'source_compile_only':True,'business_started':False}))
