"""Bounded SOURCE/AST proof only. Never import or call candidate/helper/guard."""
import ast
import hashlib
import json
from pathlib import Path

OUT=Path(__file__).parent
PARENT=Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py')
checks=[]
pins=[]
def check(name,value):
 if type(value) is not bool or not value: raise AssertionError(name)
 checks.append(dict(name=name,value=value,type='bool'))
def read(path):
 path=Path(path);before=path.lstat()
 identity=lambda st:[st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns]
 raw=path.read_bytes();after=path.lstat()
 check('complete EOF and stable seven-integer SOURCE identity '+path.name,identity(before)==identity(after) and len(raw)==before.st_size)
 pins.append(dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),identity=identity(before)))
 return raw
def tree(raw):return ast.parse(raw)
def dump(node):return ast.dump(node,include_attributes=False)
def defs(t):return {n.name:n for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
def assignments(t):return {n.targets[0].id:n.value for n in t.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
def assigned(fn,name):
 values=[n.value for n in ast.walk(fn) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)]
 check('one SOURCE constructor assignment '+name,len(values)==1)
 return values[0]
def keys(node):return [ast.literal_eval(k) for k in node.keys]
def segment(raw,node):return ast.get_source_segment(raw.decode(),node)
def inverse(raw,hunks,original,label):
 restored=raw.decode()
 for h in reversed(hunks):
  check(label+' complete inverse unique anchor',restored.count(h['after'])==1)
  restored=restored.replace(h['after'],h['before'],1)
 check(label+' entire byte inverse',restored.encode()==original)
 check(label+' entire AST inverse',dump(tree(restored))==dump(tree(original)))

oldraw=read(PARENT)
check('old pinned bcd complete SOURCE',len(oldraw)==145715 and hashlib.sha256(oldraw).hexdigest()=='bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6')
old=tree(oldraw);od=defs(old);oa=assignments(old)
draw=read(OUT/'fresh_verifier_controls.v21b.READY_SOURCE.py');driver=tree(draw);dd=defs(driver);da=assignments(driver)
hraw=read(OUT/'fresh_verifier_host.v21b.READY_SOURCE.py');host=tree(hraw);hd=defs(host);ha=assignments(host)
previous_driver=read(OUT/'fresh_verifier_controls.py.previous_READY_SOURCE.txt')
previous_host=read(OUT/'fresh_verifier_host.py.previous_READY_SOURCE.txt')
check('actual previous ee552 driver SOURCE pin',hashlib.sha256(previous_driver).hexdigest()=='ee552f1458957281a695f84c8cd74fb8c25450228eaa6aec4bbd48601d29395a')
check('actual previous 3633 host SOURCE pin',hashlib.sha256(previous_host).hexdigest()=='3633e8ea03992293b6a481f49baa0c783a28446fbca2e37325177cd6c9e3fba2')
proof=json.loads(read(OUT/'V21B_COMPLETE_SOURCE_INVERSE_PROOF.json'))
inverse(draw,proof['ready_driver_ordered_hunks'],previous_driver,'ee552 driver')
inverse(hraw,proof['ready_host_ordered_hunks'],previous_host,'3633 host')
check('driver exactly four oracle hunks and one OUT namespace',len(proof['ready_driver_ordered_hunks'])==5)
check('host exactly four one-use namespace hunks and final driver SHA',len(proof['ready_host_ordered_hunks'])==5)
pd=defs(tree(previous_driver));ph=defs(tree(previous_host))
check('only one new oracle definition added',set(dd)==set(pd)|{'_old_parent_complete_return_constructors'})
for name,node in pd.items():
 if name!='expected_return_from_old':check('entire original driver definition unchanged '+name,segment(previous_driver,node)==segment(draw,dd[name]))
check('all original host definitions retained',set(hd)==set(ph))
for name,node in ph.items():check('entire original host definition unchanged '+name,segment(previous_host,node)==segment(hraw,hd[name]))

old_return=[n.value for n in od['verify_graph'].body if isinstance(n,ast.Return) and isinstance(n.value,ast.Dict)]
check('one old complete public return dict',len(old_return)==1)
old_return=old_return[0]
expected=assigned(dd['expected_return_from_old'],'expected')
previous_expected=assigned(pd['expected_return_from_old'],'expected')
check('full 27 public top-level fields exact original order',keys(expected)==keys(old_return)==keys(previous_expected)==ast.literal_eval(ha['RETURN_FIELDS']) and len(expected.keys)==27)
changed={'fresh_reader_contract','coverage','trace_coverage'}
for key,new_value,old_value in zip(keys(expected),expected.values,previous_expected.values):
 if key not in changed:check('original complete expected value AST unchanged '+key,dump(new_value)==dump(old_value))
check('typed_snapshot borrowed complete stored object unchanged',ast.unparse(dict(zip(keys(expected),expected.values))['typed_snapshot'])=="graph['typed_snapshot']")
old_vals=dict(zip(keys(old_return),old_return.values))
check('old typed_snapshot constructor is full deepcopy only',ast.unparse(old_vals['typed_snapshot'])=="copy.deepcopy(graph['typed_snapshot'])")
check('original public reader constructor deepcopy constant',ast.unparse(old_vals['fresh_reader_contract'])=='copy.deepcopy(FRESH_READER_CONTRACT)')
check('original public coverage and trace use generated constructors',ast.unparse(old_vals['coverage'])=='coverage' and ast.unparse(old_vals['trace_coverage'])=='trace_coverage')

ctor=dd['_old_parent_complete_return_constructors']
reader=assigned(ctor,'reader')
check('independent reader reconstructed from old constant exact call',ast.unparse(reader)=='copy.deepcopy(old.FRESH_READER_CONTRACT)')
reader_keys=keys(oa['FRESH_READER_CONTRACT'])
check('all ten old reader literal keys retained',len(reader_keys)==10 and reader_keys==['schema','chunk_bytes','max_json_bytes','canonical_union_fresh_bytes_required_every_phase','parent_json_read_once_in_its_existing_typed_union_owner','parent_json_parsed_from_same_phase_fresh_pinned_bytes','no_persistent_hash_or_stat_cache','no_input_scope_or_typed_edge_filtering','strict_utf8_duplicate_key_and_nonfinite_rejection','original_requirement_and_owner_tables_lossless_and_unchanged'])
check('entire reader dict equality checked before use',"reader == graph['fresh_reader_contract']" in ast.unparse(ctor))
categories=ast.literal_eval(oa['CLOSURE_CATEGORIES'])
check('all nine original category literal order',categories==('code_environment','original92_build','memory_build','dedup_build','physical_build','capture','component_ancestry','component_terminals','source_namespace'))
coverage=assigned(ctor,'coverage')
check('coverage reconstructed by complete old category sequence',isinstance(coverage,ast.DictComp) and ast.unparse(coverage.key)=='category' and ast.unparse(coverage.generators[0].iter)=='old.CLOSURE_CATEGORIES' and not coverage.generators[0].ifs)
old_inner=[n for n in ast.walk(od['_coverage']) if isinstance(n,ast.Dict) and all(isinstance(k,ast.Constant) for k in n.keys) and keys(n)==['canonical_files','bytes','owners']]
check('one complete original coverage inner literal',len(old_inner)==1)
check('coverage inner three keys original constructor order',keys(coverage.value)==keys(old_inner[0])==['canonical_files','bytes','owners'])
check('owners output originally sorted list not scalar count',ast.unparse(old_inner[0].values[2])=='sorted(names)')
check('owners copied as complete stored list without sort/filter',ast.unparse(coverage.value.values[2])=="copy.deepcopy(saved_coverage[category]['owners'])")
check('coverage numeric values copied completely without filtering',ast.unparse(coverage.value.values[0])=="saved_coverage[category]['canonical_files']" and ast.unparse(coverage.value.values[1])=="saved_coverage[category]['bytes']")
trace=assigned(ctor,'trace');old_counts=assigned(od['_trace_coverage'],'counts')
trace_keys=keys(old_counts)
check('all ten trace constructor keys in exact old order',keys(trace)==trace_keys and len(trace_keys)==10)
for key,value in zip(trace_keys,trace.values):check('complete saved trace counter '+key,ast.unparse(value)=="saved_trace["+repr(key)+"]")
source=ast.unparse(ctor)
check('complete coverage category set excludes extras',"set(saved_coverage) == set(old.CLOSURE_CATEGORIES)" in source)
check('all coverage inner descriptor keysets exclude extras',"set(descriptor) == {'canonical_files', 'bytes', 'owners'}" in source)
check('complete trace keyset excludes extras',"set(saved_trace) == set(trace)" in source)
check('full generated coverage and trace values checked',"coverage == saved_coverage and trace == saved_trace" in source)
check('no new helper oracle or sorting or filtering calls',not any(isinstance(n,ast.Call) and (ast.unparse(n.func).startswith('new.') or ast.unparse(n.func) in {'sorted','filter','old.verify_graph','old._coverage','old._trace_coverage'}) for n in ast.walk(ctor)))
check('old full branch checked both stored generated equalities',"coverage == graph['coverage']" in ast.unparse(od['verify_graph']) and "trace_coverage == graph['trace_coverage']" in ast.unparse(od['verify_graph']))
check('one unmodified new public full verifier call',ast.unparse(dd['run'])==ast.unparse(pd['run']))

for name in ('NEW_HELPER_PATH','NEW_HELPER_SHA256','NEW_HELPER_SOURCE_BYTES','NEW_HELPER_IDENTITY','SOURCE_STATUS','ACTUAL_SUCCESS_PINS','UNKNOWN_Q','UNKNOWN_BUSINESS_PINS'):
 check('actual READY driver binding or unknown unchanged '+name,dump(da[name])==dump(assignments(tree(previous_driver))[name]))
for name in ('BOUND_HELPER_PIN','INSTALL_WITNESS_PIN','SOURCE_INSTALL_RECORD_PIN','SOURCE_STATUS','UNKNOWN_Q','UNKNOWN_BUSINESS_PINS'):
 check('actual READY host binding or unknown unchanged '+name,dump(ha[name])==dump(assignments(tree(previous_host))[name]))
check('host final exact current driver SHA',ast.literal_eval(ha['TARGET_SHA'])==hashlib.sha256(draw).hexdigest())
for name in ('ACTUAL_SUCCESS_PINS','UNKNOWN_Q','UNKNOWN_BUSINESS_PINS'):check('driver no invented runtime success '+name,ast.literal_eval(da[name]) is None)
check('one-use driver v21b OUT path',ast.literal_eval(da['OUTPUT_PATH']).endswith('/axial-material-complete-graph-fresh-verifier-v21b-20261010'))
check('host all one-use v21b namespace literals',all(token in hraw.decode() for token in ('fresh-verifier-host-v21b-20261010','fresh-verifier-v21b-20261010','actual_complete_graph_fresh_verifier_v21b_sources','actual_complete_graph_fresh_verifier_v21b_receipts')))
check('all raw final guards/caps/math source unchanged by exact five hunk inverse',proof['only_expected_constructor_and_one_use_namespaces_and_required_driver_sha_changed'] is True)

# Text-render only using the already bound prior SOURCE literals. This neither
# reads the real witness nor executes/imports the future generator.
udraw=read(OUT/'fresh_verifier_controls.UNREADY.py')
uhraw=read(OUT/'fresh_verifier_host.UNREADY.py')
def replace_unique(raw,changes):
 text=raw.decode()
 for before,after in changes:
  check('SOURCE-only binding render unique anchor '+before.split('=')[0],text.count(before)==1)
  text=text.replace(before,after,1)
 return text.encode()
driver_render=replace_unique(udraw,[("SOURCE_STATUS = 'UNREADY_SOURCE_ONLY_NO_ACTUAL_SUCCESS'","SOURCE_STATUS = 'READY_SOURCE_BOUND_BY_ROOT'")]+[(name+' = None',name+' = '+repr(ast.literal_eval(da[name])) ) for name in ('NEW_HELPER_PATH','NEW_HELPER_SHA256','NEW_HELPER_SOURCE_BYTES','NEW_HELPER_IDENTITY','OUTPUT_PATH')])
check('future binder exact SOURCE literal render equals final ee552-inverse candidate',driver_render==draw)
host_render=replace_unique(uhraw,[("SOURCE_STATUS='UNREADY_SOURCE_ONLY_NO_ACTUAL_SUCCESS'","SOURCE_STATUS='READY_SOURCE_BOUND_BY_ROOT'")]+[(name+'=None',name+'='+repr(ast.literal_eval(ha[name]))) for name in ('TARGET_SHA','BOUND_HELPER_PIN','INSTALL_WITNESS_PIN','SOURCE_INSTALL_RECORD_PIN')])
check('future binder exact SOURCE literal render equals final 3633-inverse host',host_render==hraw)

origin=dict(parent_SOURCE_pin=pins[0],verify_graph_return=dict(line=old_return.lineno,end_line=old_return.end_lineno,keys=keys(old_return),AST=dump(old_return)),fresh_reader_contract=dict(line=oa['FRESH_READER_CONTRACT'].lineno,end_line=oa['FRESH_READER_CONTRACT'].end_lineno,keys=reader_keys,AST=dump(oa['FRESH_READER_CONTRACT'])),closure_categories=dict(line=oa['CLOSURE_CATEGORIES'].lineno,tuple=list(categories),AST=dump(oa['CLOSURE_CATEGORIES'])),coverage_inner=dict(line=old_inner[0].lineno,keys=keys(old_inner[0]),AST=dump(old_inner[0])),trace_counts=dict(line=old_counts.lineno,end_line=old_counts.end_lineno,keys=trace_keys,AST=dump(old_counts)))
review=dict(schema='AXMAT_V21B_OLD_BCD_FULL_CONSTRUCTOR_SOURCE_AST_PROOF_V1',status='FINITE_SOURCE_PASS_NO_RUNTIME_OR_QUALIFICATION',checks=checks,all_checks_typed_true=True,SOURCE_pins=pins,original_constructor_AST_origin=origin,previous_actual_ready_driver=proof['previous_ready_driver'],previous_actual_ready_host=proof['previous_ready_host'],final_ready_driver=proof['new_ready_driver'],final_ready_host=proof['new_ready_host'],source_only=True,helper_API_guard_business_executed=False,current_graph_payload_read=False,install_witness_read=False,ART_directory_read=False,old_full_API_run=False,new_helper_used_as_oracle=False,actual_success_pins=None,UNKNOWN_Q=None,UNKNOWN_BUSINESS_PINS=None,helper_metadata_qualified=False,whole_business_INPUT=False,native=False,AAA=False,ABA=False,physics_balance=False)
(OUT/'ORACLE_SOURCE_REVIEW.json').write_text(json.dumps(review,indent=2)+'\n')
print(json.dumps(dict(status=review['status'],checks=len(checks),all_checks_typed_true=True,original27fields_and_three_complete_constructor_AST_origins=True,complete_ee552_3633_bytes_AST_inverse=True,final_driver_sha256=hashlib.sha256(draw).hexdigest(),final_host_sha256=hashlib.sha256(hraw).hexdigest(),actual_success_pins=None,helper_API_guard_business_executed=False)))
