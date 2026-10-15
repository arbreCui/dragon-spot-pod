"""Inspect only this finite SOURCE package; no generator/template import/call."""
import ast
import hashlib
import json
from pathlib import Path
OUT=Path(__file__).parent
checks=[];pins=[]
def check(name,condition):
 if type(condition) is not bool or not condition:raise AssertionError(name)
 checks.append(dict(name=name,value=condition,type='bool'))
def read(name):
 p=OUT/name;s=p.lstat();identity=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns];raw=p.read_bytes();a=p.lstat()
 check('complete SOURCE read and exact identity '+name,identity==[a.st_dev,a.st_ino,a.st_mode,a.st_nlink,a.st_size,a.st_mtime_ns,a.st_ctime_ns] and len(raw)==s.st_size)
 pins.append(dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),identity=identity));return raw
def same(a,b):return ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False)
def defs(tree):return {n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
def assignments(tree):
 return {n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
def calls(node,name):return [n for n in ast.walk(node) if isinstance(n,ast.Call) and ast.unparse(n.func)==name]
hostraw=read('fresh_verifier_host.UNREADY.py');host=ast.parse(hostraw);hd=defs(host);ha=assignments(host)
original=read('pure_helper_controls_host.original.txt');ot=ast.parse(original)
proof=json.loads(read('host_template_complete_source_inverse.json'));restored=hostraw.decode()
for h in reversed(proof['ordered_hunks']):
 check('host inverse anchor unique',restored.count(h['after'])==1);restored=restored.replace(h['after'],h['before'],1)
check('23 bounded complete genuine-host inverse hunks',len(proof['ordered_hunks'])==23)
check('all genuine original bytes recovered',restored.encode()==original)
check('all genuine original AST recovered',same(ast.parse(restored),ot))
check('original genuine host SOURCE exact expected SHA',hashlib.sha256(original).hexdigest()=='de72db68baa9b91fee8aad1965605ab25c9cb11ed2ea3013c3a1f04d52a41fb2')
for name in ('helper.modules','helper.guard_admission','resource.DynamicHistoryResources','runner.execute','support.load'):
 check('original genuine call retained '+name,[ast.dump(n,include_attributes=False) for n in calls(ot,name)]==[ast.dump(n,include_attributes=False) for n in calls(host,name)])
check('only stage label differs in genuine executor constructor',len(calls(host,'full.OwnRSSSerialExecutor'))==len(calls(ot,'full.OwnRSSSerialExecutor'))==1 and len(calls(host,'full.OwnRSSSerialExecutor')[0].args)==4 and ast.unparse(calls(host,'full.OwnRSSSerialExecutor')[0].args[-1])=='resources')
check('original normal host zero-extra-arg CLI retained',"len(sys.argv)!=1" in hostraw.decode())
check('original actual type runner and resource identity retained',"type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources" in hostraw.decode())
check('normal host entirely UNREADY',ast.literal_eval(ha['SOURCE_STATUS'])=='UNREADY_SOURCE_ONLY_NO_ACTUAL_SUCCESS' and all(isinstance(ha[n],ast.Constant) and ha[n].value is None for n in ('TARGET_SHA','BOUND_HELPER_PIN','INSTALL_WITNESS_PIN','SOURCE_INSTALL_RECORD_PIN','UNKNOWN_Q','UNKNOWN_BUSINESS_PINS')))
check('host UNREADY preflight before imports and SOURCE reads',isinstance(hd['main'].body[1],ast.If) and 'SOURCE_STATUS' in ast.unparse(hd['main'].body[1].test) and isinstance(hd['main'].body[1].body[0],ast.Raise))
check('host original limits512 history96 free8 one child no retries retained',all(v in hostraw.decode() for v in ('WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,64*2**20','8*2**30,96*2**30,production.ResourceFailure','before[\'artifact_bytes\']+ARCHIVE_CAP>=96*2**30','before[\'disk_free_bytes\']-ARCHIVE_CAP<8*2**30','threads=1,children_at_once=1,retries=0')))
check('genuine whole resource scans exactly two',len(calls(host,'resources.check'))==2)
check('source namespace complete before after and all7id pins',len(calls(host,'_source_namespace'))==2 and 'source_after!=source_before' in hostraw.decode() and "for entry in inputs+[hpin,rpin]" in hostraw.decode() and "support.pin(entry['path'],entry['sha256'])!=entry" in hostraw.decode())
check('SOURCE dirs and nonsymlink regular private files enumerated',all(v in hostraw.decode() for v in ('os.walk(root,followlinks=False)','directories=directories,files=files,symlinks=[]','st_nlink!=1')))
check('real PID watch and host parent binding declared',"claim['PID']==report['PID']==admission['PID']==watch['pid']" in hostraw.decode() and "claim['parent_PID']==report['parent_PID']==admission['parent_PID']==os.getpid()" in hostraw.decode())
check('stream accounting honestly merged',"actual_merged_child_stdout_stderr=support.pin(log)" in hostraw.decode() and 'independent_child_stdout_captured=False,independent_child_stderr_captured=False' in hostraw.decode())
check('all complete gz outputs directly decompressed and parsed',len(calls(host,'_gzip_object'))==3 and "digest.hexdigest()!=pin['uncompressed_JSON_sha256']" in hostraw.decode() and 'json.load(stream,parse_constant=_fail_constant)' in hostraw.decode())
check('full trace exactly37112 and all records inspected',"len(trace['records'])!=37112" in hostraw.decode() and "for record in trace['records']" in hostraw.decode() and "record['attempt_count']!=1" in hostraw.decode())
check('current graph and metadata only full scope',all(v in hostraw.decode() for v in ('238441','37111','4473','63469','INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION','consumer_scope=None')))
check('no outer closed terminal fabricated',all(v in hostraw.decode() for v in ('external_Root_closed_terminal_required=True','actual_external_Root_terminal_required=True','helper_metadata_qualified=False','UNKNOWN_Q=None','UNKNOWN_BUSINESS_PINS=None')))
driverraw=read('fresh_verifier_controls.UNREADY.py');dt=ast.parse(driverraw);da=assignments(dt);dd=defs(dt)
driver_original=read('fresh_verifier_controls.original_UNREADY.txt');driverproof=json.loads(read('driver_template_complete_source_inverse.json'));driver_restored=driverraw.decode()
for h in reversed(driverproof['ordered_hunks']):
 check('driver SOURCE inverse anchor unique',driver_restored.count(h['after'])==1);driver_restored=driver_restored.replace(h['after'],h['before'],1)
check('all previous UNREADY driver bytes AST recovered',driver_restored.encode()==driver_original and same(ast.parse(driver_restored),ast.parse(driver_original)) and len(driverproof['ordered_hunks'])==6)
check('new driver unknown helper and output pins None',all(isinstance(da[k],ast.Constant) and da[k].value is None for k in ('NEW_HELPER_PATH','NEW_HELPER_SHA256','NEW_HELPER_SOURCE_BYTES','NEW_HELPER_IDENTITY','OUTPUT_PATH','UNKNOWN_Q','UNKNOWN_BUSINESS_PINS')))
check('driver unready qualification remains None',ast.literal_eval(da['SOURCE_STATUS'])=='UNREADY_SOURCE_ONLY_NO_ACTUAL_SUCCESS' and ast.literal_eval(da['ACTUAL_SUCCESS_PINS']) is None)
verify=calls(dt,'new.verify_graph');check('one unchanged public direct verify call',len(verify)==1 and len(verify[0].args)==1 and [k.arg for k in verify[0].keywords]==['expected_sha256','phase'])
check('driver full installed helper exact7integer identity required',"new_before['identity']==NEW_HELPER_IDENTITY" in driverraw.decode() and 'all(type(v) is int for v in NEW_HELPER_IDENTITY)' in driverraw.decode())
expected=[n for n in ast.walk(dd['expected_return_from_old']) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='expected' for t in n.targets)][0].value
check('all27 full public return fields match host contract',[k.value for k in expected.keys]==ast.literal_eval(ha['RETURN_FIELDS']) and len(expected.keys)==27)
check('all9 complete actual trace fields match host contract',len(ast.literal_eval(ha['TRACE_FIELDS']))==9)
check('driver full private4 positive3reject control retained','len(positive)==4 and len(negatives)==3' in driverraw.decode())
genraw=read('bind_fresh_verifier_sources.py');gt=ast.parse(genraw);gd=defs(gt);ga=assignments(gt)
check('generator uses only standard library imports',all((n.module if isinstance(n,ast.ImportFrom) else n.names[0].name).split('.')[0] in {'argparse','ast','hashlib','json','math','os','pathlib','stat'} for n in gt.body if isinstance(n,(ast.Import,ast.ImportFrom))))
check('generator never imports helper guard or starts business child',not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in {'exec_module','module_from_spec','Popen','execute','verify_graph','guard_admission','modules'} for n in ast.walk(gt)))
check('generator never references full graph or numeric artifact inputs',b'input_graph.json' not in genraw and b'validation/artifacts/' in genraw and len(calls(gt,'pin'))>0)
check('generator real witness argv only no exactwitness hardcoded',all(v in genraw.decode() for v in ("'--install-tool-return'","'--install-tool-return-sha256'","'--template-manifest-sha256'")) and b'f8e83e8' not in genraw and b'0a9fd961' not in genraw and b'exact_integer.json' not in genraw)
check('generator strict actual observed typed0 and no session binding',all(v in genraw.decode() for v in ("witness['closed'] is True","witness['actual_tool_terminal_return_observed'] is True","type(terminal.get('exit_code')) is int","terminal['exit_code']==0","'session_id' not in terminal","math.isfinite(terminal['wall_time_seconds'])")))
check('generator exact integer correction and actual helper source pins required',all(v in genraw.decode() for v in ("witness['exact_integer_pins_decoded_from_actual_terminal_output'] is True","witness['original_actual_terminal_output_preserved_exact'] is True","helper['sha256'],helper['identity']","record['sha256'],record['identity']")))
check('generator strict source-only runtime qualification flags',all(v in genraw.decode() for v in ("witness['actual_pure_helper_protocol_qualified'] is False","witness['actual_full_current_graph_verifier_qualified'] is False","witness['actual_new_helper_qualification_sha256'] is None")))
check('generator unknownQ business values not retargeted',ast.literal_eval(ga['UNKNOWN_Q']) is None and ast.literal_eval(ga['UNKNOWN_BUSINESS_PINS']) is None)
check('generator own binding full SOURCE bytes AST inverse declared',all(v in genraw.decode() for v in ('restored.encode()==raw','ast.dump(ast.parse(restored)','ast.dump(ast.parse(raw)','complete_UNREADY_driver_bytes_AST_inverse=True','complete_UNREADY_host_bytes_AST_inverse=True')))
check('generator full SOURCE freeze saved outside namespace',"write_json(RECEIPTS/'Root_generated_full_SOURCE_namespace_freeze.json'" in genraw.decode() and 'source_files=[pin(p) for p in sorted(SOURCES.iterdir())]' in genraw.decode())
check('generator external Root runtime close and review required',all(v in genraw.decode() for v in ('Root_must_source_review_and_externally_pin_host_before_execution=True','Root_must_record_real_closed_terminal_after_host=True','external_Root_terminal_fabricated=False','actual_runtime_executed=False')))
for name in ('derive_source_templates.py','host_extra_definitions.txt'):ast.parse(read(name))
review=dict(schema='AXMAT_V21_COMPLETE_FRESH_VERIFIER_BINDING_FINITE_SOURCE_REVIEW_V1',status='FINITE_SOURCE_PASS_DRIVER_HOST_GENERATOR_UNREADY_NOT_EXECUTED',checks=checks,all_checks_typed_true=True,SOURCE_pins=pins,host_original_complete_inverse_hunks=23,host_original_bytes_AST_inverse=True,driver_complete_return_fields=27,full_actual_trace_fields=9,normal_host_extra_arguments=0,install_witness_read=False,current37k_graph_read=False,numeric_payload_read=False,helper_guard_API_or_generator_main_called=False,actual_helper_binding_SHA=None,actual_helper_binding_bytes=None,UNKNOWN_Q=None,UNKNOWN_BUSINESS_PINS=None,helper_metadata_qualified=False,whole_business_INPUT=False,native=False,AAA=False,ABA=False,physics_balance=False,actual_RSS_compliance_proven=False)
(OUT/'SOURCE_REVIEW.json').write_text(json.dumps(review,indent=2)+'\n')
print(json.dumps(dict(status=review['status'],all_checks_typed_true=True,checks=len(checks),host_complete_original_bytes_AST_inverse=True,inverse_hunks=23,install_witness_read=False,current37k_graph_read=False,helper_guard_API_generator_main_called=False)))
