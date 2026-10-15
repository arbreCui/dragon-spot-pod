"""Independent full Source/finite META review. No reviewed module is imported."""
import ast
import base64
import hashlib
import json
from pathlib import Path
import stat

P=Path(__file__).parent
Q=Path('/private/tmp/axmat_complete_helper_inactive_audit_snapshot_SOURCE_candidate_yiyxo77u')
S=Path(str(Q)+'_seal_receipt')
CHECKS=[]


def check(name,condition,evidence=None):
    if type(condition) is not bool or not condition:
        raise ValueError(name)
    CHECKS.append(dict(check=name,passed=True,evidence=evidence))


def strict(raw):
    def pairs(items):
        d={}
        for k,v in items:
            if k in d:
                raise ValueError('duplicate META key '+k)
            d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,
        parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))


def seven(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def fullpin(path):
    b=path.lstat()
    check('real Source/META regular singleton '+str(path),stat.S_ISREG(b.st_mode) and b.st_nlink==1 and not path.is_symlink())
    raw=path.read_bytes();a=path.lstat()
    check('complete finite EOF/SHA7ID stable '+str(path),seven(a)==seven(b) and len(raw)==b.st_size)
    return dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=seven(a)),raw


def shape(pin):
    check('exact fullpin shape '+str(pin.get('path')),type(pin) is dict
        and set(pin)=={'path','sha256','size_bytes','identity'}
        and type(pin['path']) is str and Path(pin['path']).is_absolute()
        and type(pin['sha256']) is str and len(pin['sha256'])==64
        and all(c in '0123456789abcdef' for c in pin['sha256'])
        and type(pin['size_bytes']) is int and pin['size_bytes']>=0
        and type(pin['identity']) is list and len(pin['identity'])==7
        and all(type(v) is int and v>=0 for v in pin['identity'])
        and pin['identity'][3]==1 and pin['identity'][4]==pin['size_bytes'])


def dump(node):return ast.dump(node,include_attributes=False)


def source_span(raw,node):
    lines=raw.splitlines(keepends=True)
    start=min([node.lineno,*[d.lineno for d in getattr(node,'decorator_list',[])]])
    return b''.join(lines[start-1:node.end_lineno])


def write(name,value):
    with (P/name).open('x') as out:
        json.dump(value,out,ensure_ascii=False,indent=2,allow_nan=False);out.write('\n')


manifest_pin,manifest_raw=fullpin(Q/'MANIFEST.json')
check('fixed author manifest actual SHA',manifest_pin['sha256']=='13aa3f853077199546b292bc6f0b00d74069e3001f44bb919443760d8076e918')
m=strict(manifest_raw)
check('Source-only UNREADY package status',m['source_only'] is True and m['status']=='UNREADY_COMPLETE_SOURCE_ONLY_NO_HELPER_OR_BUSINESS_EXECUTION')
check('all21 members exact counts',type(m['member_count']) is int and m['member_count']==21==len(m['members']))
check('all21 unique full relative paths',len({e['relative_path'] for e in m['members']})==21)
files={};pins={};copy_dir=P/'COMPLETE_AUTHOR_SOURCE_PACKAGE_COPY';copy_dir.mkdir()
for e in m['members']:
    expected={k:e[k] for k in ('path','sha256','size_bytes','identity')};shape(expected)
    path=Q/e['relative_path'];check('relative path bound complete package '+e['relative_path'],str(path)==expected['path'])
    actual,raw=fullpin(path);check('all member full actual pin '+e['relative_path'],actual==expected)
    files[e['relative_path']]=raw;pins[str(path)]=actual
    copy=copy_dir/e['relative_path'];copy.parent.mkdir(parents=True,exist_ok=True)
    with copy.open('xb') as out:out.write(raw)
    check('full copied Source bytes '+e['relative_path'],copy.read_bytes()==raw)
with (copy_dir/'MANIFEST.json').open('xb') as out:out.write(manifest_raw)
check('complete namespace no omissions',set(str(f) for f in Q.rglob('*') if f.is_file())==set(pins)|{str(Q/'MANIFEST.json')})
dirs={str(p):seven(p.lstat()) for p in [Q,*Q.rglob('*')] if p.is_dir()}
check('whole namespace no aliases',all(not p.is_symlink() for p in Q.rglob('*')))
check('full original subdirectories',{str(p):seven(p.lstat()) for p in Q.rglob('*') if p.is_dir()}
      =={e['path']:e['identity'] for e in m['subdirectories']})
check('actual complete member byte total',sum(e['size_bytes'] for e in m['members'])==m['total_member_bytes'])

parsed={}
for name,raw in files.items():
    if name.endswith('.py'):
        parsed[name]=ast.parse(raw,filename=name)
        check('complete Python Source AST only '+name,True)
    elif name.endswith('.json'):
        strict(raw)
        check('complete finite JSON member parsed duplicate/nonfinite strict '+name,True)
check('all8 original Python members complete AST',len(parsed)==8==m['parsed_python_file_count'])
name='combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume.UNREADY.py'
candidate=files[name];parent=files['ORIGINAL_cf0_COMPLETE_HELPER.py'];canonical=files['ORIGINAL_09e_COMPLETE_CANONICAL.py']
check('full candidate actual SHA/size',hashlib.sha256(candidate).hexdigest()=='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092' and len(candidate)==150986)
check('full parent cf0 actual SHA',hashlib.sha256(parent).hexdigest()=='cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c')
check('complete canonical09e actual SHA',hashlib.sha256(canonical).hexdigest()=='09e53974005082a14d9675f69258549609a991f86ec231ab6b15edfe20dd265e')
inverse=strict(files['EXACT_COMPLETE_SOURCE_INVERSE.json']);restored=candidate
check('exact two inverse hunks count',len(inverse['hunks'])==2)
for h in reversed(inverse['hunks']):
    for k in ('old','new'):
        check('fullhunk UTF8/base64 exact '+str(h['index'])+'/'+k,
              h[k+'_utf8'].encode()==base64.b64decode(h[k+'_base64'],validate=True))
    new,old=h['new_utf8'].encode(),h['old_utf8'].encode()
    check('complete unique inverse hunk '+str(h['index']),restored.count(new)==1)
    restored=restored.replace(new,old,1)
check('full Source bytes inverse cf0',restored==parent)
check('full Source AST inverse cf0',dump(ast.parse(restored))==dump(parsed['ORIGINAL_cf0_COMPLETE_HELPER.py']))
ct,pt=parsed[name],parsed['ORIGINAL_cf0_COMPLETE_HELPER.py']
defs=lambda t:{n.name:n for n in t.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
cd,pd=defs(ct),defs(pt)
check('complete81 top definition domain',list(cd)==list(pd) and len(cd)==81)
definition_evidence=[]
for key in pd:
    if key=='ReadOpenAudit':continue
    check('all80 other complete function bytes '+key,source_span(candidate,cd[key])==source_span(parent,pd[key]))
    check('all80 other complete function AST '+key,dump(cd[key])==dump(pd[key]))
    definition_evidence.append(dict(name=key,complete_parent_sha256=hashlib.sha256(source_span(parent,pd[key])).hexdigest(),
                                   complete_candidate_sha256=hashlib.sha256(source_span(candidate,cd[key])).hexdigest()))
check('all unchanged globals/nondefinitions AST',
    [dump(n) for n in ct.body if not isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
    ==[dump(n) for n in pt.body if not isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))])
cm=defs(cd['ReadOpenAudit']);pm=defs(pd['ReadOpenAudit'])
check('all audit method domain unchanged',list(cm)==list(pm)==['__init__','__enter__','__exit__','snapshot'])
for key in ('__init__','__enter__','__exit__'):
    check('whole audit lifecycle bytes '+key,source_span(candidate,cm[key])==source_span(parent,pm[key]))
    check('whole audit lifecycle AST '+key,dump(cm[key])==dump(pm[key]))
new,old=cm['snapshot'],pm['snapshot']
check('old audit docstring unchanged',dump(cd['ReadOpenAudit'].body[0])==dump(pd['ReadOpenAudit'].body[0]))
check('new snapshot exact body7/old4',len(new.body)==7 and len(old.body)==4)
check('only kwonly private False added',new.args.vararg is None and new.args.kwarg is None
    and [x.arg for x in new.args.args]==['self'] and [x.arg for x in new.args.kwonlyargs]==['_consume']
    and len(new.args.kw_defaults)==1 and isinstance(new.args.kw_defaults[0],ast.Constant)
    and new.args.kw_defaults[0].value is False)
for newi,oldi,label in ((1,0,'inactive guard'),(3,1,'full normalized list initializer'),(4,2,'every full normalization/role loop'),(6,3,'complete default return')):
    check('default full original AST '+label,dump(new.body[newi])==dump(old.body[oldi]))
    check('default full original bytes '+label,source_span(candidate,new.body[newi])==source_span(parent,old.body[oldi]))
flag_expected=ast.parse('_require(type(_consume) is bool, "private read-open snapshot consume flag must be an exact bool")').body[0]
check('strict bool before any self/map access',dump(new.body[0])==dump(flag_expected))
guard_expected=ast.parse('''if _consume:
    _require(type(self) is ReadOpenAudit and type(self._records) is dict
        and self._active is False and self._recording is False
        and all(trace is not self for trace in _ACTIVE_TRACES),
        "private read-open snapshot consume requires an owned inactive builtin audit")''').body[0]
check('complete private type/inactive/registry identity guard',dump(new.body[2])==dump(guard_expected))
branch=new.body[5]
check('private exact controlled block four statements',isinstance(branch,ast.If) and dump(branch.test)==dump(ast.Name(id='_consume',ctx=ast.Load())) and len(branch.body)==4 and not branch.orelse)
ret_default=old.body[3].value;ret_private=branch.body[3].value
check('all nine snapshot return fields/order',isinstance(ret_private,ast.Dict) and [k.value for k in ret_private.keys]==[k.value for k in ret_default.keys] and len(ret_private.keys)==9)
fields=[k.value for k in ret_default.keys]
lookup=dict(zip(fields,ret_default.values))
for n,k in ((0,'unique_records'),(1,'actual_read_open_attempts')):
    assignment=branch.body[n]
    check('original whole count expression captured before clear '+k,isinstance(assignment,ast.Assign)
        and len(assignment.targets)==1 and isinstance(assignment.targets[0],ast.Name)
        and assignment.targets[0].id==k and dump(assignment.value)==dump(lookup[k]))
check('clear exact builtin original map only after counts',dump(branch.body[2])==dump(ast.parse('self._records.clear()').body[0]))
for key,value in zip(fields,ret_private.values):
    wanted=ast.Name(id=key,ctx=ast.Load()) if key in ('unique_records','actual_read_open_attempts') else lookup[key]
    check('every full private return expression '+key,dump(value)==dump(wanted))
check('no original loop final value deleted before clone',
    all(not (isinstance(n,ast.Delete) and any(isinstance(x,ast.Name) and x.id=='value' for x in n.targets)) for n in new.body))
check('two original full clone calls preserved order',
    [dump(n) for n in ret_private.values if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='_json_clone']
    ==[dump(n) for n in ret_default.values if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='_json_clone'])
verify=cd['verify_graph'];returns=[n for n in verify.body if isinstance(n,ast.Return)]
check('public verifier complete27 return fields/order',len(returns)==1 and isinstance(returns[0].value,ast.Dict) and len(returns[0].value.keys)==27)

canon_tree=parsed['ORIGINAL_09e_COMPLETE_CANONICAL.py'];callers={};caller_evidence=[]
for fn in canon_tree.body:
    if not isinstance(fn,ast.FunctionDef):continue
    calls=[n for n in ast.walk(fn) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='audit' and n.func.attr=='snapshot']
    if calls:
        callers[fn.name]=calls
        refs=[n for n in ast.walk(fn) if isinstance(n,ast.Name) and n.id=='audit']
        check('caller has only with-owner, snapshot receiver, delete '+fn.name,
            len(refs)==3 and sum(isinstance(n.ctx,ast.Store) for n in refs)==1
            and sum(isinstance(n.ctx,ast.Load) for n in refs)==1 and sum(isinstance(n.ctx,ast.Del) for n in refs)==1)
        check('canonical all callers still default '+fn.name,len(calls)==1 and not calls[0].args and not calls[0].keywords)
        caller_evidence.append(dict(name=fn.name,start_line=fn.lineno,end_line=fn.end_lineno,
            complete_source_utf8=source_span(canonical,fn).decode(),snapshot_line=calls[0].lineno,
            audit_references=[dict(line=n.lineno,context=type(n.ctx).__name__) for n in refs]))
check('all3 complete local callers enumerated',set(callers)=={'record_actual_trim_component','create_complete_input_graph','complete_input_phase'})
phase=next(n for n in canon_tree.body if isinstance(n,ast.FunctionDef) and n.name=='complete_input_phase')
withs=[n for n in ast.walk(phase) if isinstance(n,ast.With) and any(isinstance(x.optional_vars,ast.Name) and x.optional_vars.id=='audit' for x in n.items)]
check('complete phase fresh exact class constructor',len(withs)==1 and len(withs[0].items)==1
    and dump(withs[0].items[0].context_expr)==dump(ast.parse('g.ReadOpenAudit()',mode='eval').body))
check('verifier receives no audit argument',len(withs[0].body)==1 and isinstance(withs[0].body[0],ast.Assign)
    and not any(isinstance(n,ast.Name) and n.id=='audit' for n in ast.walk(withs[0].body[0])))
check('complete phase snapshot after with inactive',callers['complete_input_phase'][0].lineno>withs[0].end_lineno)
check('future private callsite exact unique Source anchor',canonical.count(b"trace=audit.snapshot();graph_path=d['input_graph']['path']")==1)
check('future private callsite not yet wired',not any(c.keywords for calls in callers.values() for c in calls))
check('helper no snapshot caller injection',not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='snapshot' for n in ast.walk(ct)))

receipts=[];receipt_copy=P/'ACTUAL_AUTHOR_SOURCE_RECEIPT_COPIES';receipt_copy.mkdir()
receipt_paths=[Q/n for n in ('ACTUAL_SOURCE_CANDIDATE_GENERATION_TOOL_RETURN.json',
    'ACTUAL_ORIGINAL_SOURCE_CONTEXT_READ_TOOL_RETURN.json','ACTUAL_SEALED_PARENT_SOURCE_MANIFEST_READ_TOOL_RETURN.json')]
receipt_paths += [S/'ACTUAL_SOURCE_ONLY_CANDIDATE_SEAL_TOOL_RETURN.json',S/'ACTUAL_POSTSEAL_FULL_EOF_TOOL_RETURN.json']
for path in receipt_paths:
    pin,raw=fullpin(path);v=strict(raw);t=v['terminal_tool_return']
    check('genuine Source actual typed0 CLOSED '+path.name,v['source_only'] is True and v['closed'] is True
        and v['actual_tool_terminal_return_observed'] is True and type(t['exit_code']) is int and t['exit_code']==0
        and 'session_id' not in t and v['candidate_or_helper_executed'] is False)
    with (receipt_copy/path.name).open('xb') as out:out.write(raw)
    receipts.append(dict(original_fullpin=pin,terminal_chunk=t['chunk_id'],terminal_exit_code=t['exit_code']))
sealed_output=strict(strict((S/'ACTUAL_SOURCE_ONLY_CANDIDATE_SEAL_TOOL_RETURN.json').read_bytes())['terminal_tool_return']['output'])
check('actual Source seal output binds full manifest',sealed_output['manifest']==manifest_pin)
check('actual Source seal output binds full candidate',sealed_output['candidate']==m['candidate_pin'])
check('actual Source seal full root directory stable',sealed_output['package_directory_identity_after_manifest']==seven(Q.lstat()))
review=strict(files['SOURCE_SELF_REVIEW.json'])
check('author actual all126 checks honest typed True',type(review['check_count']) is int and review['check_count']==126==len(review['checks'])
    and all(c['pass'] is True for c in review['checks']) and review['blockers']==[])
check('author all future qualification null',all(v is None for v in m['all_new_actual_qualification_pins'].values())
    and m['six_future_business_pins']==[None]*6 and m['observed_peak_line_or_RSS_PASS_prediction'] is None)
for expected in review['parent_Source_pins_before'].values():
    shape(expected);actual,_=fullpin(Path(expected['path']))
    check('actual project/old proposal Source fullpin unchanged '+expected['path'],actual==expected)
for path,expected in pins.items():
    actual,_=fullpin(Path(path));check('all21 original Source members still fullpin unchanged '+path,actual==expected)
check('original Source manifest unchanged after fullreview',fullpin(Q/'MANIFEST.json')[0]==manifest_pin)
check('all original Source dirs unchanged after review',dirs=={str(p):seven(p.lstat()) for p in [Q,*Q.rglob('*')] if p.is_dir()})

limits=[
 'Source ownership covers pinned complete_input_phase normal success only; private True requires fresh exclusive last-use caller contract.',
 'Exact class/map/state/registry guards are not external alias or foreign-map ownership detection; an aliased exact dict passes these guards and clear is externally visible.',
 'Unbound foreign receiver may access its _active attribute before exact class guard, preserving original inactive guard order; no arbitrary foreign-object side-effect-free promise.',
 'Count evaluation moved before full clones; private failure after clear is nontransactional and cannot return qualification.',
 'Final loop value retains one original record dict; normalized shallow rows retain nested data; subprocess records and Popen maps remain until original caller deletion.',
 'All original clone semantics, row/role/subprocess order and nested types remain; default map preservation is Source proof, not executed control evidence.',
 'No canonical call is wired; unchanged codec GRAPH_STORAGE_SOURCE_STATUS is not admission of changed helper.',
 'No observed peak-line cause, saved RSS success, future build prediction, whole INPUT/native/RAM/AAA/ABA/physics credit.'
]
controls=[
 'Run entire original genuine pure protocol incl all positive/negative owner/trace/rawgzip/Popen/FD/callable-identity fixtures under original60/512/64MiB caps.',
 'Add disjoint fresh exact-audit default/consume equality over all9 fields, all record/subprocess/nested types/keys/order/float bits; counts for empty/duplicates; default original map intact and consume cleared only original map.',
 'For real subprocess traces preserve actual FD/inode/PID observations: full value equivalence uses disjoint copied builtin states of the same saved real observations, or explicitly distinguishes independent-run observations; never normalize away identities to manufacture equality.',
 'Reject None/0/1/float/string flags, active audit, audit subclass, foreign receiver with builtin attributes, dict subclass/Mapping, active/recording non-False and stale active identity before map clear; preserve raw exception and object state.',
 'Demonstrate aliased exact maps/callables are outside private contract, not falsely rejected by an alias detector; default remains supported. Prove future private site still fresh/exclusive in full caller Source and actual frozen callable binding.',
 'Normalization/count failure before clear preserves map; complete clone failure after clear can consume private state, all real errors retained; no transactional promise or success receipt on failure.',
 'Complete current fresh graph: all37111 inputs+external graph37112 opens, full27 fields/type/order/bits, original4positive3reject/fullgzip streams, new consume site driver Source and allcaps/MRO/watchdog/stdout/stderr retained.',
 'New actual installed helper/witness and both real strict-int0 CLOSED host receipts, independent complete saved pure+fresh reviews, then new jointQ; oldcf0/Q cannot qualify new3b18. Canonical change needs fresh fullSource binding before its separate business build.'
]
report=dict(schema='INDEPENDENT_COMPLETE_HELPER_INACTIVE_AUDIT_SNAPSHOT_SOURCE_REVIEW_V1',
    status='SOURCE_ONLY_PASS_UNREADY_REQUIRES_NEW_FULL_QUALIFICATION',source_only=True,
    all_checks_passed=True,blockers=[],check_count=len(CHECKS),checks=CHECKS,
    qualified_source_manifest=manifest_pin,candidate=m['candidate_pin'],parent_helper=inverse['parent_helper_pin'],
    canonical_Source_09e_pin=next(v for v in review['parent_Source_pins_before'].values() if v['sha256'].startswith('09e539')),
    changed_top_definition='ReadOpenAudit',changed_method='snapshot',inverse_hunks=2,
    unchanged_complete_definitions=definition_evidence,
    all9_snapshot_return_fields=fields,all27_verifier_return_fields=[k.value for k in returns[0].value.keys],
    complete_local_caller_Source_evidence=caller_evidence,
    actual_author_SOURCE_only_receipts=receipts,precise_limits=limits,required_new_actual_controls=controls,
    canonical_private_call_wired=False,candidate_or_helper_executed=False,guard_or_business_executed=False,
    numerical_or_ART_payload_read=False,project_or_original_Source_changed=False,
    runtime_qualification_created=False,source_memory_release_amount_measured=None,
    future_RSS_or_build_pass_predicted=None,new_Q=None,six_future_business_pins=[None]*6,
    whole_INPUT_native_RAM_AAA_ABA_physics_qualified=False)
write('REVIEW.json',report)
write('FULL_MEMBER_AND_TOOL_PROVENANCE.json',dict(source_only=True,manifest_pin=manifest_pin,
    complete_original_member_pins=list(pins.values()),actual_Source_receipts=receipts,original_directory_identities=dirs))
pin,_=fullpin(P/'REVIEW.json')
print(json.dumps(dict(status=report['status'],source_only=True,check_count=report['check_count'],blockers=[],
    review_pin=pin,author_manifest_pin=manifest_pin,candidate=m['candidate_pin'],candidate_executed=False,new_Q=None),ensure_ascii=False,allow_nan=False))
