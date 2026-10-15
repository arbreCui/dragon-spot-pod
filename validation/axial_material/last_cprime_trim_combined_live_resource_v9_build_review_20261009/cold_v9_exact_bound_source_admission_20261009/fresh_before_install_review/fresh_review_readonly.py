from pathlib import Path
import hashlib,json,os,stat
H=Path(__file__).resolve().parent
prior=Path('/private/tmp/spot_v9_qualified_INPUT_bound_cold_final_source_independent_review_20261009')
checked={};total=0
def fresh(p,sha,size=None,want_json=False):
 global total
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)and p.resolve(strict=True)==p
 h=hashlib.sha256();count=0;parts=[]
 with p.open('rb')as f:
  while b:=f.read(1024*1024):
   h.update(b);count+=len(b)
   if want_json:parts.append(b)
 assert h.hexdigest()==sha,(str(p),'sha256 mismatch')
 assert p.lstat()==s
 if size is not None:assert count==size
 total+=count;checked[str(p)]=dict(sha256=sha,bytes=count,dev=s.st_dev,ino=s.st_ino,mode=s.st_mode,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns,nlink=s.st_nlink)
 if want_json:return json.loads(b''.join(parts))
source_report=fresh(prior/'independent_final_source_review.json','7a5e209e965bc440d364fcb486939de47f8d96834bb03feb9c654213bf429dc3',want_json=True)
receipt=fresh(prior/'actual_readonly_tool_return.json','41fa934146e64184fa50ccdd05dcb4127c0fc839f7da78e52def12dded10d087',want_json=True)
assert source_report['status']=='PASS'and receipt['actual_tool_result']==dict(initial_chunk_id='6f9b18',session_id=None,terminal_chunk_id='6f9b18',exit_code=0,closed=True)
rows=source_report['all_fresh_pins'];assert len(rows)==len({x['path']for x in rows})==source_report['source_pin_count_derived_not_frozen_to_68']
for x in rows:fresh(x['path'],x['sha256'],x['bytes'])
A=Path('/Users/wen/spot/validation/axial_material');R=A/'last_cprime_trim_combined_live_resource_v9_build_review_20261009'
adm=fresh(R/'Root_actual_whole_INPUT_independent_admission.json','26b6bd4f61e40ba6ecff162360c31c6a14321a1ad7de36b2d82efce8e0b63c65',want_json=True)
assert adm['status']=='QUALIFIED_COMPLETE_INPUT_ONLY_NO_COLD_OR_SCIENCE_CREDIT'and adm['qualified_whole65_whole7_trim73_and_complete_graph_scope']is True
for x in adm['preserved_review_files']:fresh(x['path'],x['sha256'],x['size'])
for key in('joint_independent_report','whole_API_return','durable_ROOT_receipt'):
 x=adm[key];fresh(x['path'],x['sha256'])
C=Path('/private/tmp/axmat-last-cprime-trim-cold-v9-qualified-input-bound-candidate-20261009')
cands={'prepare_historical_input_owned_specs_physical_last_cprime_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak.py':'59d0c9b0f0a3b9ca6764f628ade537ec9b09eaa6edfe69e734994a7323adbfc8','cold_component_input_consumer_last_cprime_trim_own_pid_peak.py':'2fa0cb00ec458e9bbbbdf2f15db703a1c0547b08d35f585b6c7e6e6274d06d59','cold_owned_specs_last_cprime_trim_component_input_intake_binding_20261009.json':'b37b9d5adda1fb4a5ffe0f4a4914d513f38f6f68d480be6145f8d4af041572dc'}
for name,sha in cands.items():fresh(C/name,sha)
absent=source_report['formal_paths_all_absent'];assert len(absent)==7 and all(not os.path.lexists(p)for p in absent.values())
for p,x in checked.items():
 s=Path(p).lstat();assert(s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink)==(x['dev'],x['ino'],x['mode'],x['bytes'],x['mtime_ns'],x['ctime_ns'],x['nlink'])
report=dict(status='PASS_FRESH_BEFORE_EXACT_SOURCE_INSTALL_ONLY',final_source_report_sha256='7a5e209e965bc440d364fcb486939de47f8d96834bb03feb9c654213bf429dc3',final_source_actual_tool=receipt['actual_tool_result'],existing_final_source_receipt_sha256='41fa934146e64184fa50ccdd05dcb4127c0fc839f7da78e52def12dded10d087',derived_source_pin_count=len(rows),all101_original_pins_fresh_complete_SHA=True,whole_INPUT_admission_sha256='26b6bd4f61e40ba6ecff162360c31c6a14321a1ad7de36b2d82efce8e0b63c65',whole_INPUT_all_preserved_review_file_pin_count=len(adm['preserved_review_files']),whole_INPUT_preserved_reviews_and_actual_receipt_API_joint_freshSHA=True,candidate_pins=cands,all_three_formal_and_four_future_roots_absent=absent,fresh_distinct_file_count=len(checked),actual_fresh_fullread_bytes_including_repeated_identity_pins=total,fresh_file_metadata_stable_before_after=True,formal_installed=False,DECLARE_PREP_API_RUN_native_executed=False,project_written=False,full35GB_numerical_data_reread=False,all80defs_inverse_repeated=False,cold_actual_outcomes_None=True,scope='Fresh readonly admission of exact reviewed three sources only; no future DECLARE/PREP/native or science credit',prior_readonly_syntax_failure='first_readonly_reader_syntax_failure.json',pins=checked)
with(H/'fresh_before_install_review.json').open('x')as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=report['status'],derived_pins=len(rows),fresh_distinct_files=len(checked),fullread_bytes=total,whole_INPUT_preserved_reviews=len(adm['preserved_review_files']),three_formal_four_roots_absent=True,report_sha256=hashlib.sha256((H/'fresh_before_install_review.json').read_bytes()).hexdigest(),only_readonly=True)),flush=True)
