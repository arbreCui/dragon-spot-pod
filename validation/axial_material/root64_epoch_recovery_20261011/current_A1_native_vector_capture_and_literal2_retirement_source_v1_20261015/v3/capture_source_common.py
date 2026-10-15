"""Literal A1 capture metadata helpers; no import-time business or science reads."""
import hashlib,importlib.util,json,os,stat,sys
from pathlib import Path
sys.dont_write_bytecode=True
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011';ART=R/'validation/artifacts';BASE=Path(__file__).absolute().parent;TOP=BASE.parent
V6=REC/'one_actual_track_H150_NZ48_full370_component_source_v1_20261014/v6'
FINITE=REC/'current_eight_fuel_finite18_SCAT_producer_source_v1_20261015';FINITE_ENTRY=FINITE/'v6';FINITE_OUT=ART/'axial-material-current-eight-fuel-finite18-SCAT-producer-20261015-v2'
OLD_RETIRE=REC/'literal4_completed_compare_spool_retirement_20261014_v1'
OUT=ART/'axial-material-current-A1-native-vector-capture-and-literal2-retirement-20261015-v1'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2147483648,history_bytes=103079215104,cold_reserve_bytes=20971764748,metadata_reserve_bytes=67108864,free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
FALSE=dict(physics_qualified=False,scientific_accuracy_qualified=False,complete_reaction_authority_qualified=False,physical_neutron_balance_qualified=False,unreduced_reference_qualified=False,full_reference_qualified=False,formal_H150_NZ48_full_controls_qualified=False,historical_machine_bit_replay=False,historical_native_RAM_bits_verified=False,original_XSM_memory_bits_verified=False,finite18_replayed=False,temperature_interpolation_replayed=False,current_SPH_MASK_context_applied=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
SCIENCE_PATHS={str(ART/'axial-material-current-three-plane-raw-macro-compare-after-GENDF-cumulative25-20261014-v1-evidence/A1'/n) for n in('original_archive_index.sqlite','original_words.bin')}
VECTOR_PATHS=[(('TRACK',1,name),count) for name,count in(('XMU$MCCG',4),('ZMU$MCCG',4),('WZMU$MCCG',4),('V$MCCG',14))]
def require(ok,msg):
 if type(ok) is not bool or not ok:raise RuntimeError(msg)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();compiler=str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15' and p.get('sha256')=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492' and p['identity'][3]==2
 require(q.is_absolute() and '..' not in q.parts and stat.S_ISREG(s.st_mode) and s.st_nlink==(2 if compiler else 1) and not any(a.is_symlink() for a in(q,*q.parents)) and identity(s)==p['identity'] and s.st_uid==os.getuid() and s.st_size==p['size_bytes'],'exact current ordinary7 '+str(q));return q
def metadata_limit(q):
 large={ART/'axial-material-current-all34-original-ASCII-infinite-SCAT-producer-20261015-v1/Root_actual_all34_original_ASCII_infinite_SCAT_summary.json',ART/'axial-material-current-all34-original-ASCII-infinite-SCAT-producer-20261015-v1/inventories/ACTUAL_ALL34_ORIGINAL_ASCII_INFINITE_SCAT_EVIDENCE.json',FINITE_OUT/'Root_actual_eight_fuel_finite18_SCAT_summary.json',FINITE_OUT/'inventories/ACTUAL_EIGHT_FUEL_FINITE18_SCAT_EVIDENCE.json'}
 return 64*2**20 if Path(q) in large else 8*2**20
def pin(q):
 q=Path(q);s=q.lstat();require(str(q) not in SCIENCE_PATHS and s.st_size<metadata_limit(q),'Source/metadata only pin; old A1 body prohibited');p=dict(path=str(q),sha256=hashlib.sha256(q.read_bytes()).hexdigest(),size_bytes=s.st_size,identity=identity(s));current(p);return p
def exact(p):
 q=current(p);require(str(q) not in SCIENCE_PATHS and p['size_bytes']<metadata_limit(q),'Source/metadata only exact read');raw=q.read_bytes();require(hashlib.sha256(raw).hexdigest()==p['sha256'],'complete Source/metadata SHA');current(p);return raw
def read(p):return json.loads(exact(p))
def load(p,name):
 exact(p);require(name not in sys.modules,'fresh pinned Source module');spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);require(Path(m.__file__).absolute()==Path(p['path']),'exact Source module origin');exact(p);return m
def write(q,v):
 with Path(q).open('x') as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 return pin(q)
def unique(rows):
 table={}
 for p in rows:
  if p['path'] in table:require(table[p['path']]==p,'one consistent fullPF per path')
  table[p['path']]=p
 return list(table.values())
def contains(v,p):return v==p or type(v) is dict and any(contains(x,p) for x in v.values()) or type(v) is list and any(contains(x,p) for x in v)
def closed0(v,key,p,outkey):
 t=v[key];require(v['observed_closed'] is True and type(v['original_integer_exit_code']) is int and v['original_integer_exit_code']==0 and type(t['exit_code']) is int and t['exit_code']==0 and t.get('session_id') is None and json.loads(t['output'].strip().splitlines()[-1])[outkey]==p,'genuine original typed closed0/stdout exact fullPF')
def check_finite(proof,schema,status):
 h=read(proof['host']);e=read(proof['child']);post=read(proof['post']);require(h['status']=='ACTUAL_EIGHT_FUEL_64T_FINITE18_P0_WORDS_CLOSED0_ONLY' and h['failure'] is None and h['final_report_resource_check_passed'] is True and h['original_caps']==CAPS and h['actual_evidence']==e and len(h['records'])==8 and len(h['actual_child_receipts'])==8 and all(r['status']=='PASS' for r in h['records']),'actual finite18 closed owning output')
 require(e['status']=='EIGHT_FUEL_64T_FINITE18_P0_RAW_WORDS_EQUAL' and e['eight_fuel_finite18_P0_producer_raw_words_replayed'] is True and e['aggregation_metadata_only'] is True and e['compared_completed_child_reports']==8 and len(e['original_completed_child_report_pins'])==8 and e['compared_original_archives']==16 and e['compared_unique_nuclides']==8 and e['compared_temperature_records']==64 and e['compared_finite_dilution_nodes']==1152 and e['compared_original_leaf_records']==3456,'actual finite18 complete narrow producer proof')
 closed0(read(proof['root_tools']),'actual_terminal_return',proof['host'],'report_pin');require(post['schema']==schema and post['status']==status and status.startswith('PASS') and post['failure'] is None and all(contains(post,proof[k]) for k in('host','child','root_tools')),'actual independent finite post supplied after it exists');closed0(read(proof['post_tools']),'actual_review_return',proof['post'],'review_pin')
 for v in(h,e,post):require(all(v.get(k,False) is False for k in('physics_qualified','full_reference_qualified','AAA_qualified','ABA_admitted','goal_complete')),'no finite producer physics inheritance')
 require(not any(p['path'] in SCIENCE_PATHS for p in h['fixed_current_pins']),'completed finite actual has no A1 pair live dependencies')
 return proof
def check_capture(proof,schema,status):
 h=read(proof['host']);e=read(proof['child']);post=read(proof['post'])
 require(h['schema']=='ACTUAL_A1_NATIVE_VECTOR_CAPTURE_GUARDED_REPORT_V1' and h['status']=='ACTUAL_A1_NATIVE_VECTOR_CAPTURE_26R4_104B_CLOSED0_ONLY' and h['failure'] is None and h['secondary_failures']==[] and h['final_report_resource_check_passed'] is True and h['actual_evidence']==e and h['original_caps']==CAPS and len(h['records'])==1 and h['records'][0]['status']=='PASS','one original guarded actual current capture closed0')
 require(e['schema']=='ACTUAL_A1_NATIVE_26_REAL32_VECTOR_CAPTURE_V1' and e['status']=='A1_NATIVE_26_REAL32_WORDS_104B_CAPTURE_CLOSED0_ONLY' and e['captured_original_record_count']==4 and e['captured_REAL32_words']==26 and e['captured_bytes']==104 and e['original_small_vectors_called_unchanged'] is True and e['native_engines_started']==0 and e['original_XSM_redecoded'] is False and e['compact_vector_full_pin']==proof['compact'],'actual four original native records only')
 raw=exact(proof['compact']);require(len(raw)==104 and proof['compact']['path']==str(OUT/'inventories/A1_native_track_vectors_f4.bin'),'exact private complete104B capture')
 rows=e['native_vector_record_descriptors'];require(len(rows)==4,'exact original descriptor4')
 for d,(path,count),offset in zip(rows,VECTOR_PATHS,(0,16,32,48)):
  require(d['name']==path[-1] and d['path']==list(path) and d['kind']==2 and d['words']==count and d['offset_bytes']==offset and d['captured_bytes']==4*count and d['captured_word_encoding']=='little_endian_REAL32' and d['captured_payload_sha256']==d['native_payload_sha256']==d['original_native_row']['native_payload_sha256']==hashlib.sha256(raw[offset:offset+4*count]).hexdigest() and d['original_native_row']['path']==list(path) and d['original_native_row']['kind']==2 and d['original_native_row']['original_word_count']==count and d['original_native_row']['declared_count']==count,'unchanged original row/hash and exact compact raw slice')
 closed0(read(proof['root_tools']),'actual_terminal_return',proof['host'],'report_pin')
 require(post['schema']==schema and post['status']==status and status.startswith('PASS') and post['failure'] is None and all(contains(post,proof[k]) for k in ('host','child','compact','root_tools')),'genuine independent actual capture post supplied after it exists')
 closed0(read(proof['post_tools']),'actual_review_return',proof['post'],'review_pin')
 for v in (h,e,post):require(all(v.get(k,False) is False for k in ('physics_qualified','full_reference_qualified','AAA_qualified','ABA_admitted','goal_complete')),'no current tiny vector physics qualification')
 for p in h['complete_output_pins']:current(p)
 return h,e
def snapshot(file,result):
 data=(json.dumps(result,indent=2,allow_nan=False)+'\n').encode();file.seek(0);file.write(data);file.truncate();file.flush();os.fsync(file.fileno())
