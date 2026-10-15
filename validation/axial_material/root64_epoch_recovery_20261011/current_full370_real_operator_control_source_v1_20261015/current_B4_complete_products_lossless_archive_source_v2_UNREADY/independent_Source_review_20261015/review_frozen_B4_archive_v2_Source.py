"""Independent Source/metadata review only. No project import or result-body IO."""
import ast
import builtins
import hashlib
import json
import os
import shlex
import stat
import symtable
from pathlib import Path

D=Path(__file__).absolute().parent.parent
HERE=Path(__file__).absolute().parent
V1=D.parent/'current_B4_complete_products_lossless_archive_source_v1_UNREADY'
EXPECTED={
 'B4_archive_common.UNREADY.py':'31987f2c8c6fab6abf307e83770900633d5ff60f4ebb3dc8c1390467c7b087e3',
 'archive_B4_products_serial.UNREADY.py':'d572005cb090ec9bc23a9fff2c28f5b98f31210058e5ccbe3a3186ad436342df',
 'run_guarded_B4_products_lossless_archive.UNREADY.py':'e4df5461f073608f4339b07b258625859ee632dc847bd20e1da14f018d360ca1',
 'prepare_B4_products_archive_Source.UNREADY.py':'89245acf85d8f3f5c896754e6b29f49a5b7d035987fb473dfb38784e7d86a068',
 'publish_B4_products_archive_CLI.UNREADY.py':'8f23bee1cb7949184662f550dacf0811c61b67a93285f7b76fa0be69d20ce14f'}
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,
 history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,
 free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)

def need(ok,msg):
 if not ok:raise RuntimeError(msg)

def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def current(p,owned=True):
 need(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'},'exact PF shape')
 need(type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity']),'typed integer PF')
 q=Path(p['path']);s=q.lstat()
 need(q.is_absolute() and stat.S_ISREG(s.st_mode) and not any(x.is_symlink() for x in(q,*q.parents)) and ids(s)==p['identity'] and s.st_size==p['size_bytes'],'literal exact current7')
 if owned:need(s.st_uid==os.getuid() and s.st_nlink==1,'private owned nlink1 current7')
 return s

def pin(q):
 q=Path(q);s=q.lstat();need(stat.S_ISREG(s.st_mode)and s.st_nlink==1,'review metadata/Source ordinary file')
 raw=q.read_bytes();need(ids(q.lstat())==ids(s),'review read stable7')
 return dict(path=str(q.absolute()),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ids(s))

def read(p):
 current(p);need(p['size_bytes']<8*2**20,'small metadata/Source only')
 raw=Path(p['path']).read_bytes();need(len(raw)==p['size_bytes']and hashlib.sha256(raw).hexdigest()==p['sha256'],'metadata/Source fullEOF SHA');current(p)
 return raw

def meta(p):return json.loads(read(p))

def typed_tool(p,key,role,expected,code=0):
 x=meta(p);r=x[key]
 need(x['observed_closed']is True and type(x['original_integer_exit_code'])is int and x['original_integer_exit_code']==code and type(r['exit_code'])is int and r['exit_code']==code and 'session_id'not in r,'genuine closed typed tool return')
 if role is not None:need(json.loads(r['output'].splitlines()[-1])[role]==expected,'actual stdout exact complete PF')
 return x

def fn(text,name):
 node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)and n.name==name)
 return ''.join(text.splitlines(True)[node.lineno-1:node.end_lineno])

def selected(text,*parts):
 for part in parts:need(part in text,'reviewed exact Source control: '+part)

def main():
 need(not (HERE/'REVIEW.json').exists(),'independent review once')
 ready_pin=pin(D/'SOURCE_REVIEW_READY.json');ready=meta(ready_pin)
 need(ready_pin['sha256']=='e69cb93f063cd4578032f678bf9b6eec0701168ba5e24071eade26006d977fba','Root supplied READY')
 generation_pin=pin(D/'ROOT_SOURCE_GENERATION_CANONICAL_TRUE_TOOL_RETURNS.json')
 need(generation_pin['sha256']=='d9d7f4af4331441cbd45177c0b918f9ae0f60aa206c82cf7d0d56520661aec1c','Root supplied canonical GEN')
 generation=typed_tool(generation_pin,'actual_Source_preparation_return','ready_pin',ready_pin)
 original_gen=meta(generation['preserved_original_raw_pin'])
 need(generation['actual_Source_preparation_return']==original_gen['actual_generation_return'] and original_gen['actual_generation_return']['chunk_id']=='280a09','canonical GEN is same original real object; no new GEN')
 author_pin=pin(D/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json');author=meta(author_pin)
 need(author_pin['sha256']=='fa605cbbe239a766bc3e10beae2cfa380ff90b2274900ac9a57cb0decb89b819'and author['Source_only_frozen_before_Root_generation']is True and author['Source_preparer_or_publisher_executed_by_author']is False,'original author freeze')
 sourcepins=ready['complete_source_file_pins'];need(sourcepins==author['whole_Source_file_pins']and len(sourcepins)==len(EXPECTED),'complete five Source table')
 sources={}
 for p in sourcepins:
  name=Path(p['path']).name;need(name in EXPECTED and p['sha256']==EXPECTED[name],'whole pre-reviewed Source unchanged')
  text=read(p).decode();ast.parse(text);table=symtable.symtable(text,p['path'],'exec');tops=set(table.get_identifiers());unbound=set()
  def walk(s):
   for k in s.get_identifiers():
    y=s.lookup(k)
    if y.is_referenced()and y.is_global()and k not in tops and k not in vars(builtins):unbound.add(k)
   for child in s.get_children():walk(child)
  walk(table);need(not unbound,'no unbound global candidates');sources[name]=text
 for role,name in [('host_source_pin','run_guarded_B4_products_lossless_archive.UNREADY.py'),('common_source_pin','B4_archive_common.UNREADY.py'),('worker_source_pin','archive_B4_products_serial.UNREADY.py'),('writer_source_pin','publish_B4_products_archive_CLI.UNREADY.py')]:
  need(ready[role]==next(p for p in sourcepins if Path(p['path']).name==name),'exact READY Source role')
 common=sources['B4_archive_common.UNREADY.py'];worker=sources['archive_B4_products_serial.UNREADY.py'];host=sources['run_guarded_B4_products_lossless_archive.UNREADY.py'];publisher=sources['publish_B4_products_archive_CLI.UNREADY.py']
 oldworker=(V1/'archive_B4_products_serial.UNREADY.py').read_text()
 algorithm=fn(worker,'archive_one');need(algorithm==fn(oldworker,'archive_one')and hashlib.sha256(algorithm.encode()).hexdigest()=='db8a6b9fe2234c77f460274fe3d73d5fe43377089ef8341c305b8b20da892495','archive_one whole original byte algorithm')
 selected(common,'OUT_CAP=96*2**20','ARCHIVE_CAP=88*2**20','SOURCE_CAP=16*2**20','bm.current_metadata_role(p,build)','source_module(binding[\'original_production_inputs_Source_pin\'],\'production_inputs\')','self.metadata_context=metadata_role_context(binding)','peak<512*2**20','resources_after_original_classes_forced_fresh')
 selected(worker,"enumerate(b['live_original_product_pins'],start=1)",'entries=[reused];completed_bytes=0',"original_plain_preserved_at_entry_creation=oldentry['original_plain_preserved'],original_plain_preserved=False",'len(entries)==4',"c.pin(b['reused_member0_gzip_pin']['path'])==b['reused_member0_gzip_pin']",'newly_archived_count=3,reused_complete_archive_count=1')
 need('shutil.copy'not in worker and 'os.link'not in worker and 'os.unlink'not in worker,'reuse old member0 without copies/links/deletion')
 selected(host,"claim=BASE/'ROOT_ARCHIVE_EXECUTION_CLAIM.json'","resources=c.Resources(b,started,1800)","runner.execute(stage,'serial_B4_complete_product_byte_archive',command,600)","runner.records[0]['label']+'.watchdog.json'",'original_resource_modules(b)','full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-started)')
 need(host.index("with claim.open('x')")<host.index('c=bootstrap')<host.index('c.original_resource_modules(b)'),'Root claim before all project helpers/preload')
 selected(publisher,"actual_Source_preparation_return","PASS_SOURCE_ONLY_CURRENT_B4_COMPLETE_PRODUCT_ARCHIVE_REUSE_MEMBER0_V2","review['complete_source_file_pins']==ready['complete_source_file_pins']")
 bp=ready['execution_binding_pin'];b=meta(bp);authbind=meta(ready['author_admission_binding_pin'])
 need(ready['author_admission_binding_pin']==author['whole_admission_binding_pin'],'same author admission binding')
 changed={k for k in set(b)|set(authbind) if b.get(k)!=authbind.get(k)}
 need(changed<= {'Source_only_current_cumulative_bytes_before_reservations','Source_generation_product_payload_opened','Source_generation_gzip_executed'},'GEN did not alter closure/math/binding')
 need(b['prerequisite_binding_complete']is True and b['draft_unready']is False and b['Source_admission_ready']is False and b['separate_member0_stream0_peer0_and_exact2_cleanup0_post0_bound']is True,'all actual prerequisites closed; Source-only boundary')
 need(b['original_caps']==ready['original_caps']==CAPS and b['bounded_total_output_bytes']==96*2**20 and b['bounded_archive_payload_bytes']==88*2**20 and b['bounded_Source_metadata_bytes']==16*2**20,'original caps/96 total88payload8meta/Source16')
 need('all4_complete_original_products_retained'not in b and b['all4_original_products_retained']is False,'no stale current all4-live assertion')
 products=b['all4_product_pins'];need(len(products)==4 and [Path(p['path']).name for p in products]==['m.xsm','u.asc','a.asc','t.asc'] and b['retired_original_product_pins']==products[:1]and b['live_original_product_pins']==products[1:],'exact producer order four; one retired three live')
 cp=b['actual_exact2_cleanup_closure_pins'];plan=meta(cp['plan']);receipt=meta(cp['execution_receipt']);post=meta(cp['post'])
 typed_tool(cp['Root_tools'],'actual_terminal_return','receipt_pin',cp['execution_receipt']);typed_tool(cp['post_tools'],'actual_review_return','review_pin',cp['post'])
 need(receipt['schema']=='CURRENT_B4_EXACT2_PARTIAL_ARCHIVE_RECOVERY_RECEIPT_V1'and receipt['mode']=='execute'and receipt['status']=='RETIRED_CURRENT_B4_EXACT2_RECOVERY_COMPLETE_RESULT_BYTES_PRESERVED'and receipt['failure']is None and receipt['plan_pin']==cp['plan']and receipt['actual_released_pins']==plan['exact_target_pins']and receipt['actual_released_pins'][0]==products[0]and len(receipt['actual_released_pins'])==2 and receipt['actual_released_bytes']==101693287 and receipt['resources_after_original_classes_forced_fresh']is True,'genuine exact2 Root0 final fresh receipt')
 rp=b['actual_exact2_cleanup_post_projection'];need(post['schema']==rp['schema']and post['status']==rp['status']and post['failure']is None and post['metadata_only']is True and post[rp['execution_receipt_pin_field']]==cp['execution_receipt']and post[rp['Root_tools_pin_field']]==cp['Root_tools']and post[rp['released_pins_field']]==receipt['actual_released_pins']and post[rp['released_bytes_field']]==receipt['actual_released_bytes'],'same genuine exact2 independent post0')
 for p in receipt['actual_released_pins']:need(not os.path.lexists(p['path']),'exact2 targets actually absent; never read absent original body')
 for p in products[1:]+b['retained_native_current7_pins']+b['original_B_native_and_readonly_input_current7_pins']:current(p)
 need(len(b['retained_native_current7_pins'])==79 and len(b['original_B_native_and_readonly_input_current7_pins'])==11,'all79native/11input retainers current7 only')
 ep=b['reused_member0_entry_pin'];gp=b['reused_member0_gzip_pin'];entry=meta(ep);current(gp)
 need(entry['ordinal']==0 and entry['original_plain_full_pin']==products[0]and entry['compressed_archive_full_pin']==gp and entry['original_plain_preserved']is True and entry['exact_original_plain_bytes_recoverable']is True and entry['compression_input_SHA']==entry['streamed_decompressed_SHA']==products[0]['sha256']and entry['compression_input_length']==entry['streamed_decompressed_length']==products[0]['size_bytes'],'retained original member0 entry creation history; gzip current7 only')
 vp=plan['actual_single_member_verification_closure_pins'];verify=meta(vp['Root_report']);peer=meta(vp['post'])
 typed_tool(vp['Root_tools'],'actual_terminal_return','report_pin',vp['Root_report']);typed_tool(vp['post_tools'],'actual_review_return','review_pin',vp['post'])
 vr=plan['actual_single_member_Root_key_projection'];pr=plan['actual_single_member_post_key_projection']
 need(verify['schema']==vr['schema']and verify['status']==vr['status']and verify['failure']is None and verify[vr['entry_pin_field']]==ep and verify[vr['original_pin_field']]==products[0]and verify[vr['gzip_pin_field']]==gp and verify[vr['decompressed_SHA_field']]==products[0]['sha256']and verify[vr['decompressed_length_field']]==products[0]['size_bytes']and verify[vr['streamed_complete_field']]is True and verify['children_started']==0 and verify['all4_archive_complete']is False,'genuine separate single-member Root0; no child0 invented')
 need(peer['schema']==pr['schema']and peer['status']==pr['status']and peer['failure']is None and peer['metadata_only']is True and peer[pr['Root_report_pin_field']]==vp['Root_report']and peer[pr['Root_tools_pin_field']]==vp['Root_tools']and peer[pr['entry_pin_field']]==ep and peer[pr['original_pin_field']]==products[0]and peer[pr['gzip_pin_field']]==gp and peer[pr['separate_Root_stream_proof_matched_field']]is True,'genuine separate member0 metadata post0')
 failed=plan['actual_failed_archive_closure_pins'];failurehost=meta(failed['Host']);failurepost=meta(failed['post']);typed_tool(failed['Root_tools'],'actual_terminal_return',None,None,1);typed_tool(failed['post_tools'],'actual_review_return','review_pin',failed['post'])
 need(failurehost['actual_watchdog']is None and failurepost['actual_recorded_child_integer_exit_codes']==[]and failurepost['actual_Root_integer_exit_code']==1,'old failure Root1/HostNULL/post[] preserved')
 sup=meta(b['actual_failed_archive_supplemental_post_pin']);typed_tool(b['actual_failed_archive_supplemental_post_tools_pin'],'actual_review_return','review_pin',b['actual_failed_archive_supplemental_post_pin'])
 sr=b['actual_failed_archive_supplemental_post_projection']
 need(sup['schema']==sr['schema']and sup['status']==sr['status']and sup['failure']is None and sup['metadata_only']is True and sup[sr['Host_pin_field']]==failed['Host']and sup[sr['Root_tools_pin_field']]==failed['Root_tools']and sup[sr['member0_entry_pin_field']]==ep and sup[sr['member0_gzip_pin_field']]==gp and type(sup['supplemental_actual_recorded_child_integer_exit_codes'])is list and sup['supplemental_actual_recorded_child_integer_exit_codes']==[1]and all(type(v)is int for v in sup['supplemental_actual_recorded_child_integer_exit_codes']),'separate standalone child1 supplement0 preserves original []')
 prefix=b['inherited_latest_complete_joint_roots'];roots=b['complete_joint_roots'];old=meta(b['failed_archive_v1_plan_pin']);latest=meta(b['latest_complete_plan_pin'])
 need(prefix==old['complete_joint_roots']==latest['complete_joint_roots']==plan['complete_joint_roots']and len(prefix)==73 and len(roots)==74 and roots==prefix+[b['planned_actual_output_root']]and len(roots)==len(set(roots))and not any(Path(a).is_relative_to(Path(z))for a in roots for z in roots if a!=z),'complete exact dynamic73 to fresh74; failed root retained')
 need(not os.path.lexists(b['planned_actual_output_root']),'new owning OUT still fresh before actual')
 extra=0
 for p in b['explicit_cumulative_metadata_file_pins']:
  current(p,False)
  if not any(Path(p['path']).is_relative_to(Path(r))for r in roots):extra+=p['size_bytes']
 cumulative=0
 for root in roots:
  q=Path(root)
  if not q.exists():continue
  for p in q.rglob('*'):
   s=p.lstat();need(not stat.S_ISLNK(s.st_mode),'complete roots no symlink aliases')
   if stat.S_ISREG(s.st_mode):cumulative+=s.st_size
 headroom=2*2**30-cumulative-extra-96*2**20-16*2**20
 need(headroom>0,'current static full-prefix metadata plus96+Source16 fits2GiB; Root must refresh actual gate')
 for p in sourcepins:read(p)
 report=dict(schema='INDEPENDENT_CURRENT_B4_ARCHIVE_REUSE_MEMBER0_SOURCE_REVIEW_V2',status='PASS_SOURCE_ONLY_CURRENT_B4_COMPLETE_PRODUCT_ARCHIVE_REUSE_MEMBER0_V2',failure=None,source_only=True,binding_pin=bp,complete_source_file_pins=sourcepins,Source_review_ready_pin=ready_pin,author_source_freeze_pin=author_pin,Root_Source_generation_true_tools_pin=generation_pin,preserved_original_GEN_tools_pin=generation['preserved_original_raw_pin'],actual_exact2_cleanup_closure_pins=cp,actual_member0_verification_closure_pins=vp,old_failure_Root1_HostNULL_priorpost_empty_child_list_preserved=True,separate_supplemental_child1_list_preserved=True,archive_one_wholebytes_v1=True,archive_one_SHA256=hashlib.sha256(algorithm.encode()).hexdigest(),all5_Source_AST_and_unbound_global_checks_passed=True,reused_member0_entry_pin=ep,reused_member0_gzip_pin=gp,final_product_count=4,reused_complete_count=1,newly_compressed_count=3,retired_original_product_pins=products[:1],live_original_product_pins=products[1:],entry0_original_plain_preserved_only_at_creation=True,complete_joint_roots=roots,original_caps=CAPS,archive_total_output_cap_bytes=96*2**20,new_payload_cap_bytes=88*2**20,metadata_headroom_bytes=8*2**20,Source_cap_bytes=16*2**20,static_cumulative_root_bytes=cumulative,static_external_metadata_bytes=extra,static_remaining_after96MiB_and_Source16MiB=headroom,Root_must_refresh_original_resource_gate_before_actual=True,product_or_gzip_body_read=False,project_helper_imported=False,GEN_or_publisher_or_archive_or_decoder_executed=False,files_deleted=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 q=HERE/'REVIEW.json'
 with q.open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(dict(status=report['status'],review_pin=pin(q),source_only=True)),flush=True)

if __name__=='__main__':main()
