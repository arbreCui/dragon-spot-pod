"""Independent finite stdlib SOURCE AST/fullEOF hash audit; never import/run reviewed code."""
from pathlib import Path
import ast
import copy
import hashlib
import json
import stat

PACKAGE=Path('/private/tmp/axmat_v22_private_owner_namespace_last_use_helper_SOURCE_ONLY_20261010_5a6uelpn')
OUT=Path(__file__).parent
SEAL_RECEIPT=Path('/private/tmp/axmat_v22_private_owner_namespace_last_use_helper_SOURCE_ONLY_20261010_5a6uelpn_seal_receipt/actual_SOURCE_seal_tool_return.json')
INSTALLED_PARENT=Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py')
MANIFEST_SHA='6c72c1e785e079a10a39de75790473151be0633fbd23b1de9c8b4cc447b883fe'
CANDIDATE_SHA='cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c'
PARENT_SHA='dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7'
CANDIDATE='combined_runtime_complete_input_graph_private_owner_namespace_last_use_v22.UNREADY.py'
checks=[]

def check(name,value):
    if type(value)is not bool or not value:raise ValueError(name)
    checks.append(dict(name=name,value=True))

def identity(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def read_source(p):
    for component in [*reversed(p.parents),p]:
        check('ordinary SOURCE path component '+str(component),not stat.S_ISLNK(component.lstat().st_mode))
    before=identity(p)
    check('bounded ordinary singlelink SOURCE '+p.name,stat.S_ISREG(before[2])and before[3]==1 and before[4]<=2*2**20)
    with p.open('rb')as stream:
        raw=stream.read();check('full SOURCE EOF '+p.name,stream.read(1)==b'')
    check('full SOURCE EOF stable seven-part identity '+p.name,identity(p)==before and len(raw)==before[4])
    return raw,dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),identity=before)

def dump(node):return ast.dump(node,include_attributes=False)
def expr(text):return ast.parse(text,mode='eval').body
def segment(text,node):return ''.join(text.splitlines(keepends=True)[node.lineno-1:node.end_lineno])

manifest_raw,manifest_pin=read_source(PACKAGE/'MANIFEST.json');manifest=json.loads(manifest_raw)
check('exact Root supplied manifest SHA',manifest_pin['sha256']==MANIFEST_SHA)
check('complete manifest status still unready Source',manifest['status']=='SEALED_UNREADY_SOURCE_ONLY_NEEDS_NEW_ACTUAL_FULL_HELPER_QUALIFICATION')
check('complete twelve-member inventory plus manifest',manifest['member_count']==12 and len(manifest['members'])==12 and sorted(p.name for p in PACKAGE.iterdir())==sorted([Path(q['path']).name for q in manifest['members']]+['MANIFEST.json']))
raws={};pins={};trees={};meta={}
for expected in manifest['members']:
    p=Path(expected['path']);check('member strict package parent',p.parent==PACKAGE)
    raw,pin=read_source(p);check('whole member SHA/bytes/exact7ID '+p.name,pin==expected)
    raws[p.name]=raw;pins[p.name]=pin
    if p.suffix=='.py':
        trees[p.name]=ast.parse(raw,filename=p.name);check('complete SOURCE AST '+p.name,isinstance(trees[p.name],ast.Module))
    elif p.suffix=='.json':
        meta[p.name]=json.loads(raw);check('complete bounded SOURCE metadata '+p.name,type(meta[p.name])is dict)
check('all member bytes exact',sum(q['bytes']for q in pins.values())==manifest['member_bytes']==518226)
check('complete candidate exact expected SHA',pins[CANDIDATE]['sha256']==CANDIDATE_SHA)
check('complete frozen parent exact dc01 SHA',pins['parent_dc01.complete.frozen_SOURCE.py']['sha256']==PARENT_SHA)
installed_bytes,installed_pin=read_source(INSTALLED_PARENT)
check('current installed qualified parent Source still exact dc01',installed_pin['sha256']==PARENT_SHA and installed_bytes==raws['parent_dc01.complete.frozen_SOURCE.py'])
ast.parse(installed_bytes,filename=str(INSTALLED_PARENT))

proof=meta['COMPLETE_SOURCE_INVERSE.json'];restored=raws[CANDIDATE].decode()
check('exactly five disclosed source hunks',proof['edit_count']==5 and len(proof['edits'])==5)
for edit in reversed(proof['edits']):
    check('unique complete inverse anchor '+edit['id'],restored.count(edit['new'])==1)
    restored=restored.replace(edit['new'],edit['old'],1)
check('all five inverse hunks restore every parent byte',restored.encode()==raws['parent_dc01.complete.frozen_SOURCE.py'])
ptree=trees['parent_dc01.complete.frozen_SOURCE.py'];ctree=trees[CANDIDATE]
check('all inverse restores complete parent AST',dump(ast.parse(restored))==dump(ptree))
ptext=raws['parent_dc01.complete.frozen_SOURCE.py'].decode();ctext=raws[CANDIDATE].decode()
pdefs={n.name:n for n in ptree.body if isinstance(n,ast.FunctionDef)}
cdefs={n.name:n for n in ctree.body if isinstance(n,ast.FunctionDef)}
check('all79 top-level function names/order exact',len(pdefs)==len(cdefs)==79 and list(pdefs)==list(cdefs))
check('all92 including methods/nested exact count',sum(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))for n in ast.walk(ptree))==sum(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))for n in ast.walk(ctree))==92)
changed=[name for name in pdefs if segment(ptext,pdefs[name])!=segment(ctext,cdefs[name])]
check('only original two functions changed',changed==['_owners','verify_graph'])
unchanged=[]
for name in pdefs:
    if name in changed:continue
    a=segment(ptext,pdefs[name]).encode();b=segment(ctext,cdefs[name]).encode()
    check('whole unchanged function bytes and AST '+name,a==b and dump(pdefs[name])==dump(cdefs[name]))
    unchanged.append(dict(name=name,sha256=hashlib.sha256(a).hexdigest(),bytes=len(a)))
check('all77 unchanged function proof entries match independently',unchanged==proof['unchanged_77_function_fullbytes_and_AST']and len(unchanged)==77)
check('all imports/classes/globals/nonfunction AST exact',[dump(n)for n in ptree.body if not isinstance(n,ast.FunctionDef)]==[dump(n)for n in ctree.body if not isinstance(n,ast.FunctionDef)])
for name,values in meta['EXACT_FULL_FUNCTION_SOURCE_CONTRACTS.json'].items():
    check('entire original/candidate function contracts '+name,values['original']==segment(ptext,pdefs[name])and values['candidate']==segment(ctext,cdefs[name]))
check('verify_graph public signature exact',dump(pdefs['verify_graph'].args)==dump(cdefs['verify_graph'].args))
prets=[n for n in ast.walk(pdefs['verify_graph'])if isinstance(n,ast.Return)]
crets=[n for n in ast.walk(cdefs['verify_graph'])if isinstance(n,ast.Return)]
check('whole verify return expression bytes and AST exact',len(prets)==len(crets)==1 and segment(ptext,prets[0])==segment(ctext,crets[0])and dump(prets[0])==dump(crets[0]))
fields=[k.value for k in crets[0].value.keys]
check('all27 return fields and order exact',len(fields)==27 and fields==proof['verify_return_field_order'])

owner=cdefs['_owners'];owner_args=copy.deepcopy(owner.args)
check('owner new private keyword only defaultFalse',len(owner_args.kwonlyargs)==1 and owner_args.kwonlyargs[0].arg=='_consume'and len(owner_args.kw_defaults)==1 and dump(owner_args.kw_defaults[0])==dump(ast.Constant(value=False)))
owner_args.kwonlyargs=[];owner_args.kw_defaults=[]
check('owner every original argument/signature field preserved',dump(owner_args)==dump(pdefs['_owners'].args))
guard=owner.body[1]
check('consume opt-in strict bool and exact builtin list guard',isinstance(guard,ast.Expr)and isinstance(guard.value,ast.Call)and guard.value.func.id=='_require'and dump(guard.value.args[0])==dump(expr('type(_consume) is bool and (not _consume or type(values) is list)')))
owner_loop=next(n for n in owner.body if isinstance(n,ast.For))
old_owner_loop=next(n for n in pdefs['_owners'].body if isinstance(n,ast.For))
check('every original owner loop validator/normalizer/append executes unchanged before consume',[dump(n)for n in owner_loop.body[:-2]]==[dump(n)for n in old_owner_loop.body])
check('complete result append before old slot release',dump(owner_loop.body[-3])==dump(ast.parse('result.append(descriptor)').body[0]))
check('private row ending after append only',[dump(n)for n in owner_loop.body[-2:]]==[dump(n)for n in ast.parse('if _consume:\n    values[consumed_index] = None\nconsumed_index += 1').body])
check('private builtin list clears only after complete loop',dump(owner.body[-2])==dump(ast.parse('if _consume:\n    values.clear()').body[0]))
old_calls=[n for n in ast.walk(ptree)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='_owners']
new_calls=[n for n in ast.walk(ctree)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='_owners']
check('all four original owner callsites retained',len(old_calls)==len(new_calls)==4)
consume_calls=[n for n in new_calls if n.keywords]
check('only full verifier opts in for its fresh expanded owner list',len(consume_calls)==1 and dump(consume_calls[0])==dump(expr('_owners(_expand_owner_table(graph["owners"], graph["requirements"]), _consume=consumer is None)')))
for old_call,new_call in zip(old_calls,new_calls):
    if not new_call.keywords:check('original default/consumer owner call unchanged at'+str(new_call.lineno),dump(old_call)==dump(new_call))
expand=cdefs['_expand_owner_table']
check('full _expand_owner_table creates private builtin list and fresh complete descriptor dicts','    owners = []\n'in segment(ctext,expand)and 'owners.append(owner)'in segment(ctext,expand)and 'return owners'in segment(ctext,expand))
check('all namespace descriptors independently deep clone after original validation','return _json_clone(value)'in segment(ctext,cdefs['_namespace_descriptor'])and 'return {key: clone(item[key]) for key in sorted(item)}'in segment(ctext,cdefs['_json_clone']))

verifier=cdefs['verify_graph'];release_candidates=[n for n in verifier.body if isinstance(n,ast.If)and len(n.body)==1 and isinstance(n.body[0],ast.For)and len(n.body[0].body)==1 and isinstance(n.body[0].body[0],ast.Delete)]
check('only one namespace private release block',len(release_candidates)==1)
release=release_candidates[0];release_index=verifier.body.index(release)
check('namespace consumption only consumerNone and only three dead fields',dump(release.test)==dump(expr('consumer is None'))and [n.slice.value for n in release.body[0].body[0].targets]==['files','symlinks','directories'])
check('full phase and original second absence both before namespace release',any(isinstance(n,ast.Assign)and isinstance(n.value,ast.Call)and getattr(n.value.func,'id',None)=='_phase'for n in verifier.body[:release_index])and isinstance(verifier.body[release_index-1],ast.Expr)and isinstance(verifier.body[release_index-1].value,ast.Call)and verifier.body[release_index-1].value.func.id=='_absence_phase'and sum(isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)and getattr(n.value.func,'id',None)=='_absence_phase'for n in verifier.body[:release_index])==2)
check('no full check/trace skipped by release',getattr(verifier.body[release_index+1].targets[0],'id',None)=='rebuilt_requirements'and segment(ctext,cdefs['_phase'])==segment(ptext,pdefs['_phase'])and segment(ctext,cdefs['_trace_coverage'])==segment(ptext,pdefs['_trace_coverage']))
trace_namespace_refs=[n for n in ast.walk(cdefs['_trace_coverage'])if isinstance(n,ast.Name)and isinstance(n.ctx,ast.Load)and n.id=='namespaces']
trace_namespace_comps=[n for n in ast.walk(cdefs['_trace_coverage'])if isinstance(n,ast.ListComp)and any(isinstance(x,ast.Name)and x.id=='namespaces'for x in ast.walk(n))]
check('remaining full trace consumes namespaces only as all canonical roots',len(trace_namespace_refs)==len(trace_namespace_comps)==1 and dump(trace_namespace_comps[0])==dump(expr('[entry["canonical_root"] for entry in namespaces]')))
check('all original return count/root-sequence preserved','"exhaustive_namespaces_checked": len(namespaces)'in segment(ctext,crets[0])and '"consumer_complete_namespace_root_sequence": [value["root"] for value in namespaces] if consumer is not None else None'in segment(ctext,crets[0]))

# Independently project out precisely the disclosed private operations, no general rewrites.
projected=copy.deepcopy(ctree);projected_defs={n.name:n for n in projected.body if isinstance(n,ast.FunctionDef)}
po=projected_defs['_owners'];loop=next(n for n in po.body if isinstance(n,ast.For));loop.body=loop.body[:-2]
po.body=[po.body[0],po.body[2],loop,po.body[-1]];po.args.kwonlyargs=[];po.args.kw_defaults=[]
pv=projected_defs['verify_graph']
for node in ast.walk(pv):
    if isinstance(node,ast.Call)and isinstance(node.func,ast.Name)and node.func.id=='_owners':node.keywords=[]
pv.body=[n for n in pv.body if not(isinstance(n,ast.If)and len(n.body)==1 and isinstance(n.body[0],ast.For)and len(n.body[0].body)==1 and isinstance(n.body[0].body[0],ast.Delete))]
check('all complete original AST including predicates/call/return ordering restored by explicit private projection',dump(projected)==dump(ptree))

future=meta['FUTURE_REAL_QUALIFICATION_UNREADY.json'];self_review=meta['SOURCE_SELF_REVIEW.json']
for label,value in [('manifest',manifest),('future',future),('selfreview',self_review)]:
    check(label+' new Q and all six business pins still None',value['new_helper_Q']is None and value['six_future_business_pins']==[None]*6)
check('original selfreview all116 Source checks not runtime claims',len(self_review['checks'])==self_review['check_count']==116 and all(item['SOURCE_result']is True for item in self_review['checks'])and self_review['blockers']==[]and self_review['runtime_or_helper_API_or_guard_executed']is False)
check('all original full graph/negative/sourcing/trace/global caps unchanged by fullASTprojection',dump(projected)==dump(ptree)and segment(ctext,cdefs['_phase'])==segment(ptext,pdefs['_phase']))
receipt_raw,receipt_pin=read_source(SEAL_RECEIPT);receipt=json.loads(receipt_raw)
check('actual SOURCE seal receipt scope truthful',receipt['scope']=='STANDARD_LIBRARY_SOURCE_ONLY_NOT_HELPER_EXECUTION'and receipt['closed']is True and receipt['new_helper_Q']is None and receipt['candidate_helper_API_guard_business_or_numeric_run']is False)
terminal=receipt['terminal_tool_return']
check('actual Source seal strict int0 CLOSED without live session',type(terminal.get('exit_code'))is int and terminal['exit_code']==0 and terminal['chunk_id']=='a2971a'and 'session_id'not in terminal)
sealed=json.loads(terminal['output'])
check('actual seal output full manifest pin matches independently observed',sealed['manifest']==manifest_pin)
for key,name in [('candidate',CANDIDATE),('inverse','COMPLETE_SOURCE_INVERSE.json'),('report','REPORT.txt'),('SOURCE_review','SOURCE_SELF_REVIEW.json')]:
    check('actual seal output complete named Source pin '+key,sealed[key]==pins[name])
check('actual seal totals/status/unready/Q match',sealed['member_count']==12 and sealed['member_bytes']==518226 and sealed['UNREADY']is True and sealed['new_helper_Q']is None and sealed['business']is False)
check('actual sealed Source directory exact7ID still matches',sealed['sealed_directory_identity']==identity(PACKAGE))
for name,expected in pins.items():
    _,after=read_source(PACKAGE/name);check('final fullEOF unchanged original Source member '+name,after==expected)
for name,path,expected in [('manifest',PACKAGE/'MANIFEST.json',manifest_pin),('installed dc01',INSTALLED_PARENT,installed_pin),('actual Source seal receipt',SEAL_RECEIPT,receipt_pin)]:
    _,after=read_source(path);check('final fullEOF Source pin unchanged '+name,after==expected)

report=dict(schema='INDEPENDENT_V22_FULL_HELPER_LAST_USE_SOURCE_PEER_REVIEW_V1',
 status='SOURCE_ONLY_COMPLETE_REVIEW_NO_HARD_SOURCE_BLOCKER_NOT_Q_OR_RSS',
 package_manifest_pin=manifest_pin,all_twelve_member_pins=pins,installed_parent_Source_pin=installed_pin,
 actual_Source_seal_receipt_pin=receipt_pin,actual_Source_seal_chunk='a2971a',actual_Source_seal_strict_int0_closed=True,
 complete_all_Source_and_small_META_read=True,all_Python_complete_AST_parsed=True,
 all_five_hunks_full_byte_inverse=True,full_AST_inverse_and_private_projection=True,
 unchanged77_functions=unchanged,all79_function_names_order_preserved=True,all92_method_nested_count_preserved=True,
 original27_return_fields_exact_bytes_AST_order=fields,
 original_return_types_and_ranges_unchanged_by_design=True,
 default_and_consumer_owner_nonconsumption_preserved=True,
 private_complete_owner_consume_after_full_perrow_validation_normalization_append=True,
 private_namespace_release_after_complete_phase_second_absence=True,
 all_complete_trace_necessary_canonical_roots_count_and_consumer_fields_preserved=True,
 original_full_graph_negatives_source_owners_guards_caps_NOT_reduced=True,
 tuple_requirement_consumption_included=False,new_helper_Q=None,six_future_business_pins=[None]*6,
 candidate_or_qualified_helper_API_guard_business_numeric_import_compile_or_run_executed=False,
 actual_numeric_material_ART_payload_or_history_read=False,existing_Source_project_ART_DE_or_canonical_written=False,
 peak_source_line=None,RSS_prediction=None,runtime_or_scientific_success=None,
 source_hard_blockers=[],all_checks=checks,
 required_next_steps=[
  'Root installs exact Source only into a fresh qualification namespace; installed dc01 and original canonical/Q/frozen D/E stay immutable.',
  'Root runs the complete original accepted/rejected bounded protocol and new private consume controls with original types/order/bits/default nonmutation and unchanged caps.',
  'Root runs the complete fresh current graph against the original full oracle/all27fields, complete actual opens and lossless trace, fresh EOF pins and genuine original supervisor/caps.',
  'Independent saved actual protocol/current-graph review precedes a new Q; old29ac does not qualify this helper and Source-only checks imply neither RSS fitness nor business/scientific admission.',
 ])
with(OUT/'SOURCE_PEER_REVIEW.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(status=report['status'],report=str(OUT/'SOURCE_PEER_REVIEW.json'),static_checks=len(checks),manifest_sha256=MANIFEST_SHA,candidate_sha256=CANDIDATE_SHA,source_hard_blockers=[],actual_source_seal_chunk='a2971a',actual_source_seal_strict_int0_closed=True,new_helper_Q=None,business_or_helper_execution=False,actual_ART_payload_read=False)))
