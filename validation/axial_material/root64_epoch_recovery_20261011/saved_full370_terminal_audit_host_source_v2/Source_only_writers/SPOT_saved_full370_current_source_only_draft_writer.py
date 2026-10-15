import ast,hashlib,json,os,stat
from pathlib import Path
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=REC/'saved_full370_terminal_audit_host_source_v1';NEW=REC/'saved_full370_terminal_audit_host_source_v2'
def sid(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);before=sid(p.lstat());assert stat.S_ISREG(before[2])
    with p.open('rb')as f:
        assert sid(os.fstat(f.fileno()))==before
        h=hashlib.file_digest(f,'sha256').hexdigest()
        assert sid(os.fstat(f.fileno()))==before
    assert sid(p.lstat())==before
    return dict(path=str(p),sha256=h,size_bytes=before[4],identity=before)
def write(p,raw):
    if isinstance(raw,dict):raw=(json.dumps(raw,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    if isinstance(raw,str):raw=raw.encode()
    with p.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
SCIENCE=OLD/'audit_saved_terminal_source_all370.py';SOURCE_SHA='2027ec61895902575165869d753926808e882e5233e89c26a3ca9c973408024f'
assert pin(SCIENCE)['sha256']==SOURCE_SHA
science=SCIENCE.read_bytes();ast.parse(science)
write(NEW/SCIENCE.name,science);assert (NEW/SCIENCE.name).read_bytes()==science
PLAN=OLD/'ACTUAL_INPUT_PIN_PLAN_UNRUN.json';raw=PLAN.read_bytes();oldlit=('"source": {\n    "path": "'+str(SCIENCE)+'",').encode();newlit=('"source": {\n    "path": "'+str(NEW/SCIENCE.name)+'",').encode()
assert raw.count(oldlit)==1
newraw=raw.replace(oldlit,newlit);assert newraw.replace(newlit,oldlit)==raw
assert json.loads(newraw)['inputs']==json.loads(raw)['inputs']
write(NEW/PLAN.name,newraw)
HOST=OLD/'run_actual_saved_full370_terminal_source_original_guard.py';old=HOST.read_text();new=old;changes=[]
def change(label,a,b):
    global new
    assert new.count(a)==1,(label,new.count(a))
    new=new.replace(a,b);changes.append(dict(label=label,old_literal=a,new_literal=b,literal_count=1))
change('fresh_output_namespaces',"OUT=ART/'axial-material-AAA-saved-full370-terminal-source-diagnostic-guarded-20261012'\nTMP_OUT=Path('/private/tmp/SPOT_AAA_full370_terminal_source_ACTUAL_ONCE_20261012')", "OUT=ART/'axial-material-AAA-saved-full370-terminal-source-diagnostic-current-mount-guarded-20261013-v2'\nTMP_OUT=Path('/private/tmp/SPOT_AAA_full370_terminal_source_CURRENT_MOUNT_ACTUAL_ONCE_20261013_v2')")
change('schema_source_version',"if freeze['schema']!='COMPLETE_SAVED_FULL370_TERMINAL_SOURCE_GUARD_HOST_FREEZE_ONLY_V1':", "if freeze['schema']!='COMPLETE_SAVED_FULL370_TERMINAL_SOURCE_GUARD_HOST_FREEZE_ONLY_V2':")
change('schema_actual_report_version',"schema='ACTUAL_ROOT_GUARDED_SAVED_FULL370_TERMINAL_SOURCE_DIAGNOSTIC_V1'", "schema='ACTUAL_ROOT_GUARDED_SAVED_FULL370_TERMINAL_SOURCE_DIAGNOSTIC_V2'")
additional='''def verify_current_mount_derivation(binding):
 """Actual frozen per-input declarations; no stat or old metadata rewriting."""
 selected=binding['complete_current_mount_mapping_pin']
 if pin(selected['path'])!=selected:raise RuntimeError('exact current mapping fullpin')
 mapping=json.loads(Path(selected['path']).read_text())
 if mapping['schema']!='SAVED_FULL370_EXPLICIT_CURRENT_MOUNT_REATTESTATION_SOURCE_V2':raise RuntimeError('current mapping schema')
 if binding.get('historical_non_live_Source_origins_explicitly_reclassified')is not True:raise RuntimeError('owning Root must explicitly classify absent historical Source origins before frozen CLI release')
 if mapping['errors']or len(mapping['rows'])!=3301 or len(mapping['historical_non_live_declarations'])!=4:raise RuntimeError('complete original3305 lineage accounting')
 original=binding['original_v1_binding_current_pin']
 if pin(original['path'])!=original:raise RuntimeError('actual original unmodified binding fullpin')
 original_binding=json.loads(Path(original['path']).read_text())
 if len(original_binding['fixed_current_pins'])!=3305:raise RuntimeError('original complete fixed list')
 historical=[];current=[]
 for row in mapping['rows']:
  old=row['historical_pin'];now=row['current_pin']
  if pin(now['path'])!=now:raise RuntimeError('every current mapping row actual fullEOF/7ID')
  if(old['path'],old['sha256'],old['size_bytes'],old['identity'][1:])!=(now['path'],now['sha256'],now['size_bytes'],now['identity'][1:])or old['identity'][0]not in(16777234,16777229)or now['identity'][0]!=16777229:raise RuntimeError('only explicitly attested device transition')
  historical.append(old);current.append(now)
 for declaration in mapping['historical_non_live_declarations']:
  old=declaration['historical_pin']
  if declaration['current_pin']is not None or declaration['in_scientific_1129_inputs']is not False or declaration['original_v1_mandatory']is not True:raise RuntimeError('absent Source-only origins remain historical and never gain current PF')
  if old not in original_binding['fixed_current_pins']:raise RuntimeError('exact absent historical original PF')
  if old['path']in[p['path']for p in binding['fixed_current_pins']]:raise RuntimeError('absent origins cannot be used as mandatory current execution inputs')
  historical.append(old)
 if sorted(historical,key=lambda p:p['path'])!=sorted(original_binding['fixed_current_pins'],key=lambda p:p['path']):raise RuntimeError('all original3305 declarations accounted without omission')
 if any(p not in binding['fixed_current_pins']for p in current):raise RuntimeError('all3301 current declarations remain mandatory')
 if len(binding['science_original_input_pins'])!=1129 or any(p not in current for p in binding['science_original_input_pins']):raise RuntimeError('all1129 scientific current inputs retained')
 verify(current)
 return dict(mapping_pin=selected,original_unmodified_v1_binding_current_pin=original,actual_fullEOF_current_declarations=3301,original_historical_declarations=3305,complete_scientific_inputs=1129,absent_historical_Source_only_origins=mapping['historical_non_live_declarations'],only_device_reattestation=True,system_stat_or_original_metadata_modified=False,new_scientific_execution_or_physics_qualification_inferred=False)

def replace_just_created_owned_report(p,wanted,d):
 """Honest failure publication after a forced final cap check, own file only."""
 p=Path(p)
 if p!=OUT/'Root_actual_saved_full370_diagnostic_summary.json'or wanted['identity'][3]!=1 or pin(p)!=wanted:raise RuntimeError('only exact just-created regular owned summary may be replaced')
 raw=(json.dumps(d,indent=2,allow_nan=False)+'\\n').encode()
 fd=os.open(p,os.O_RDWR|os.O_NOFOLLOW)
 with os.fdopen(fd,'r+b')as f:
  s=os.fstat(f.fileno());opened=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
  if opened!=wanted['identity']or not stat.S_ISREG(s.st_mode)or s.st_nlink!=1:raise RuntimeError('owned failure summary same opened7ID')
  if hashlib.file_digest(f,'sha256').hexdigest()!=wanted['sha256']:raise RuntimeError('owned failure summary same-fd fullEOF SHA')
  s=os.fstat(f.fileno());after=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
  if after!=opened or identity(p)!=opened:raise RuntimeError('owned failure summary unchanged through fullEOF')
  f.seek(0);f.write(raw);f.truncate();f.flush();os.fsync(f.fileno())
  s=os.fstat(f.fileno());closed=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
  if closed[:4]!=opened[:4]or s.st_size!=len(raw):raise RuntimeError('owned failure summary replacement ownership/length')
 if identity(p)!=closed:raise RuntimeError('owned failure summary final path7ID')
 actual=pin(p)
 if actual['sha256']!=hashlib.sha256(raw).hexdigest():raise RuntimeError('owned failure summary completed fullEOF bytes')
 return actual

'''
change('explicit_complete_current_mapping_and_owned_late_failure_functions','def tmp_inventory():',additional+'def tmp_inventory():')
change('strict_actual_current_mapping_admission'," verify(fixed)\n if pin(SUPPORT)['sha256']!=SUPPORT_SHA:"," verify(fixed)\n metadata_reattestation=verify_current_mount_derivation(binding)\n if pin(SUPPORT)['sha256']!=SUPPORT_SHA:")
change('bounded_full_final_report_and_honest_failure'," write(OUT/'Root_actual_saved_full370_diagnostic_summary.json',report);print(json.dumps(dict(status=report['status'],failure=failure,records=len(runner.records))))\n return 0 if failure is None else 1",''' report['explicit_current_mount_input_reattestation_provenance']=metadata_reattestation
 report['final_report_bytes_in_original_resources']=True
 report['postwrite_cap_PASS_requires_actual_true_closed0']=True
 summary=OUT/'Root_actual_saved_full370_diagnostic_summary.json';write(summary,report);summary_pin=pin(summary)
 try:
  verify(fixed);verify(outputs);resources.check()
 except BaseException as final_error:
  failure=repr(final_error)
  report['status']='FAILED_SAVED_FULL370_DIAGNOSTIC_NO_RETRY';report['failure']=failure
  report['after_check_error']=failure;report['late_postwrite_cap_error']=failure
  report['wall_seconds']=time.monotonic()-start;report['SELF_peak_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
  replace_just_created_owned_report(summary,summary_pin,report)
 print(json.dumps(dict(status=report['status'],failure=failure,records=len(runner.records))))
 return 0 if failure is None else 1''')
ast.parse(new)
restored=new
for row in reversed(changes):
    assert restored.count(row['new_literal'])==1,row['label']
    restored=restored.replace(row['new_literal'],row['old_literal'])
assert restored==old
write(NEW/HOST.name,new)
proof=dict(schema='SAVED_FULL370_V2_COMPLETE_SOURCE_BYTE_INVERSE_DRAFT_V1',original_science_current_pin=pin(SCIENCE),new_science_current_pin=pin(NEW/SCIENCE.name),science_Source_wholebytes_identical=True,science_Source_sha256=SOURCE_SHA,original_manifest_current_pin=pin(PLAN),new_manifest_current_pin=pin(NEW/PLAN.name),manifest_only_literal_rebind=dict(old_literal=oldlit.decode(),new_literal=newlit.decode(),count=1,complete_inverse_equal=True),all1129_input_path_SHA_pairs_exactly_unchanged=True,original_host_current_pin=pin(HOST),new_host_current_pin=pin(NEW/HOST.name),complete_host_literal_changes=changes,complete_host_inverse_equal=True,original_guard_MRO_support_helper_resources_science_math_unchanged=True,known_axes=[0,2,6],unknown_axes=[1,3,4,5,7,8],groups=370,regions=8,axial_cells=48,rank=1,SN32=True,original_stage_seconds=600,original_whole_seconds=1800,own_child_and_SELF_cap_bytes=512*2**20,threads=1,children=1,scientific_results_cap_bytes=64*2**20,TMP_plus_ART_both_history_and_fresh_counting_unchanged=True,historical_nonlive_Source_origin_resolution_pending=True,host_executable_freeze_written=False,actual_cli_written=False,upstream_future_report_PF_fabricated=False,science_candidate_imported_or_executed=False,compiler_or_transport_executed=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
write(NEW/'COMPLETE_SAVED_FULL370_SOURCE_AND_HOST_BYTE_INVERSE_DRAFT.json',proof)
print(json.dumps(dict(status='CURRENT_FULL370_SOURCE_CANDIDATES_DRAFT_ONLY_PENDING_NONLIVE_SOURCE_LINEAGE_REVIEW',science=pin(NEW/SCIENCE.name),manifest=pin(NEW/PLAN.name),host=pin(NEW/HOST.name),proof=pin(NEW/'COMPLETE_SAVED_FULL370_SOURCE_AND_HOST_BYTE_INVERSE_DRAFT.json'),complete_inverse=True,science_imported_or_executed=False,host_executable_freeze=False),allow_nan=False))
