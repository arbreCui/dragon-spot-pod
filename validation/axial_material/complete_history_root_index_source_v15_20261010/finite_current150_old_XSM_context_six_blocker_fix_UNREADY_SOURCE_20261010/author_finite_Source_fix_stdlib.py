"""Source-only author. Does not import/run/compile any candidate or API."""
import ast
import difflib
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import tarfile

P=Path(__file__).resolve().parent
ORIGINAL=Path('/private/tmp/axmat_COMPLETE_oldXSM_context_aware_aggregation_UNREADY_SOURCE_20261010_s7ik4_qc')
BLOCKED=Path('/private/tmp/axmat_INDEPENDENT_complete_old_XSM_context_SOURCE_review_ajgu183t')
BLOCKED_SEAL=BLOCKED.with_name(BLOCKED.name+'_seal_receipt')
SOURCE_SEAL=ORIGINAL.with_name(ORIGINAL.name+'_seal_receipt')
CHECKS=[]
def require(v,m):
    if type(v)is not bool or not v:raise ValueError(m)
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    s=p.lstat();require(stat.S_ISREG(s.st_mode)and s.st_nlink==1,'unaliased Source/META')
    with p.open('rb')as f:
        require(identity(os.fstat(f.fileno()))==identity(s),'open identity')
        raw=f.read();require(identity(os.fstat(f.fileno()))==identity(s),'EOF identity')
    require(identity(p.lstat())==identity(s),'path identity')
    return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s)),raw
def inventory(root):
    files={};dirs={}
    for p in [root,*sorted(root.rglob('*'))]:
        s=p.lstat();require(not stat.S_ISLNK(s.st_mode),'no Source symlink')
        rel=str(p.relative_to(root))
        if stat.S_ISDIR(s.st_mode):dirs[rel]=identity(s)
        else:files[rel]=pin(p)[0]
    return dict(root=str(root),files=files,directories=dirs)
def check(label,condition):
    require(type(condition)is bool,'exact check type');CHECKS.append(dict(check=label,passed=condition))
    require(condition,label)
def save(n,obj):(P/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
before={k:inventory(r)for k,r in [('original',ORIGINAL),('blocked',BLOCKED),('blocked_seal',BLOCKED_SEAL),('original_seal',SOURCE_SEAL)]}
check('original complete195 Source files manifest2c0b pinned',len(before['original']['files'])==195 and before['original']['files']['MANIFEST.json']['sha256']=='2c0b20393b5ab202be815be6524d417c7c18ea91da719b05dc678948f920dd89')
check('original blocked Source peer manifest d8a7 and report ddac pinned',before['blocked']['files']['MANIFEST.json']['sha256']=='d8a7e3a44c2e8503432da7fa35f86cd0db045febc15c709d6fdb3018d6503be2'and before['blocked']['files']['REVIEW.json']['sha256']=='ddac74725050ee420a8e2dfa78a9f9c69cf97abfe3516e7c9f96338011147eb1')
old={rel:pin(ORIGINAL/rel)[1]for rel in before['original']['files']}
manifest=json.loads(old['MANIFEST.json'])
check('whole original194 member EOF SHA7ID all manifest directories match',all(before['original']['files'][m['relative_path']]=={k:m[k]for k in ('path','sha256','size_bytes','identity')}for m in manifest['members'])and all(identity(Path(d['path']).lstat())==d['identity']for d in manifest['directories']))
# Preserve the complete current Source tree for its unchanged relative paths;
# preserve complete ORIGINAL bytes independently in a verified lossless tar.
for rel,raw in old.items():
    if rel=='MANIFEST.json':continue
    target=P/rel;target.parent.mkdir(parents=True,exist_ok=True);require(not target.exists(),'fresh derived Source file');target.write_bytes(raw)
(P/'ORIGINAL_COMPLETE_SOURCE_MANIFEST.json').write_bytes(old['MANIFEST.json'])
engine='complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py'
extractor='complete_observed_old_post_final_XSM_extractor.UNREADY.py'
binder='bind_complete_context_aware_and_oldXSM_SOURCE_only.UNREADY.py'
changes={
 engine:[
  ("require(type(pins)is list and pins,'actual full context list required')","require(type(pins)is list and len(pins)>0,'actual full context list required')"),
  ("require(calls,'actual complete LIBMIX calls required')","require(type(calls)is dict and len(calls)>0,'actual complete LIBMIX calls required')"),
  ("require(track and masks,'real MAT and final-mask events required, no inferred ones')","require(type(track)is list and len(track)>0 and type(masks)is list and len(masks)>0,'real MAT and final-mask events required, no inferred ones')"),
  ("historical_context_missing_is_not_silently_supplied=True,genuine_supervisor_watch_verified_here=False, **FALSE)","historical_context_missing_is_not_silently_supplied=True, **FALSE)")],
 extractor:[("require(type(inputs)is list and inputs,'complete observed snapshot list')","require(type(inputs)is list and len(inputs)>0,'complete observed snapshot list')")],
 binder:[("require(type(observations[state])is list and observations[state],'all original physical-order snapshots')","require(type(observations[state])is list and len(observations[state])>0,'all original physical-order snapshots')")]
}
inverse=[]
def definitions(tree):
    result={}
    def visit(body,prefix=''):
        for n in body:
            if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                key=prefix+n.name;result[key]=ast.dump(n,include_attributes=False);visit(n.body,key+'.')
    visit(tree.body);return result
def stmts(tree,kind):return [ast.dump(n,include_attributes=False)for n in ast.walk(tree)if isinstance(n,kind)]
terminal_audit=[];kwarg_audit=[];all_definition_facts={}
for name,edits in changes.items():
    original=old[name];new=original.decode()
    for a,b in edits:
        check(name+' unique finite source anchor '+str(len(new[:new.index(a)].splitlines())+1),new.count(a)==1)
        new=new.replace(a,b,1)
    raw=new.encode();(P/name).write_bytes(raw)
    old_lines=original.decode().splitlines(keepends=True);new_lines=new.splitlines(keepends=True)
    hunks=[dict(tag=tag,old_start0=a,old_end0=b,new_start0=c,new_end0=d,old_full_lines=old_lines[a:b],new_full_lines=new_lines[c:d])for tag,a,b,c,d in difflib.SequenceMatcher(None,old_lines,new_lines,autojunk=False).get_opcodes()if tag!='equal']
    restored=list(new_lines)
    for h in reversed(hunks):
        check(name+' inverse exact candidate hunk '+str(h['new_start0']),restored[h['new_start0']:h['new_end0']]==h['new_full_lines'])
        restored[h['new_start0']:h['new_end0']]=h['old_full_lines']
    check(name+' complete original bytes recovered',''.join(restored).encode()==original)
    bt,at=ast.parse(original),ast.parse(raw);bd,ad=definitions(bt),definitions(at)
    changed=[k for k in bd if bd[k]!=ad.get(k)]
    check(name+' all original definitions retained exact names',set(bd)==set(ad))
    # All actual control-flow branches and arithmetic expressions remain exact.
    check(name+' all If Assert Raise BinOp UnaryOp mathematical nodes retained',all(stmts(bt,t)==stmts(at,t)for t in (ast.If,ast.Assert,ast.Raise,ast.BinOp,ast.UnaryOp)))
    br=[n for n in ast.walk(bt)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='require']
    ar=[n for n in ast.walk(at)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='require']
    check(name+' all require predicates count and original error texts retained',len(br)==len(ar)and all(ast.dump(x.args[1],include_attributes=False)==ast.dump(y.args[1],include_attributes=False)for x,y in zip(br,ar)))
    for n in ar:
        a=n.args[0]
        def leaves(v):
            return [z for x in v.values for z in leaves(x)]if isinstance(v,ast.BoolOp)else[v]
        suspicious=[ast.unparse(z)for z in leaves(a)if isinstance(z,(ast.Name,ast.Subscript,ast.List,ast.Dict))]
        if suspicious:
            terminal_audit.append(dict(file=name,line=n.lineno,condition=ast.unparse(a),raw_truth_operands=suspicious,reason='Nonboolean falsy short-circuit is malformed input rejected by strict require. No legitimate nonempty list/dict is the terminal returned value.'))
    check(name+' no Name Subscript list dict terminal operand in all require predicates',all(not isinstance(n.args[0].values[-1]if isinstance(n.args[0],ast.BoolOp)else n.args[0],(ast.Name,ast.Subscript,ast.List,ast.Dict))for n in ar))
    false_keys=set()
    for n in at.body:
        if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='FALSE'for t in n.targets):
            false_keys={k.arg for k in n.value.keywords}if isinstance(n.value,ast.Call)else set(ast.literal_eval(n.value))
    for n in ast.walk(at):
        if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='dict'and any(k.arg is None and isinstance(k.value,ast.Name)and k.value.id=='FALSE'for k in n.keywords):
            collision=false_keys&{k.arg for k in n.keywords if k.arg}
            check(name+' dict expandedFALSE collision-free '+str(n.lineno),not collision)
            kwarg_audit.append(dict(file=name,line=n.lineno,explicit_keys=[k.arg for k in n.keywords if k.arg],expanded_FALSE_full_keys=sorted(false_keys),duplicate_keys=[]))
    inverse.append(dict(candidate=name,original_pin=before['original']['files'][name],candidate_pin=pin(P/name)[0],complete_zero_based_hunks=hunks,all_original_full_bytes_restored=True,changed_definitions=changed,all_unchanged_definition_AST_exact=[k for k in bd if k not in changed],original_definition_count=len(bd),candidate_definition_count=len(ad)))
    all_definition_facts[name]=dict(definition_count=len(bd),changed=changed,unchanged=[k for k in bd if k not in changed])
check('only six finite corrections across exact three Source roles',sum(len(d['complete_zero_based_hunks'])for d in inverse)==6 and set(changes)=={engine,extractor,binder})
unchanged=[r for r in old if r!='MANIFEST.json'and r not in changes]
check('all191 other original Source members byteexact unchanged',len(unchanged)==191 and all((P/r).read_bytes()==old[r]for r in unchanged))
check('original MANIFEST complete bytes preserved as historical Source', (P/'ORIGINAL_COMPLETE_SOURCE_MANIFEST.json').read_bytes()==old['MANIFEST.json'])
e_tree=ast.parse((P/engine).read_bytes());old_e_tree=ast.parse(old[engine])
get_false=lambda t:next(x.value for x in t.body if isinstance(x,ast.Assign)and any(isinstance(z,ast.Name)and z.id=='FALSE'for z in x.targets))
check('original full FALSE global and all default unknown globals unchanged',ast.dump(get_false(e_tree),include_attributes=False)==ast.dump(get_false(old_e_tree),include_attributes=False)and all(ast.dump(x,include_attributes=False)==ast.dump(y,include_attributes=False)for x,y in zip([x for x in old_e_tree.body if isinstance(x,ast.Assign)],[x for x in e_tree.body if isinstance(x,ast.Assign)])))
before_report=next(n for n in ast.walk(old_e_tree)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='dict'and n.lineno==1756)
after_report=next(n for n in ast.walk(e_tree)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='dict'and n.lineno==1756)
keys=lambda n:{k.arg for k in n.keywords if k.arg}|{k.arg for k in get_false(e_tree).keywords}
check('final report full declared field union and false value preserved no records removed',keys(before_report)==keys(after_report)and 'genuine_supervisor_watch_verified_here'in {k.arg for k in get_false(e_tree).keywords})
# Safe isolated language facts only: no candidate AST compiled/evaluated/run.
demonstration=[dict(kind='list',size=n,result_type='bool',result=(type(v)is list and len(v)>0))for n,v in [(0,[]),(1,[object()])]]
demonstration += [dict(kind='dict',size=n,result_type='bool',result=(type(v)is dict and len(v)>0))for n,v in [(0,{}),(1,{'k':object()})]]
check('standalone Python type+len bool semantics legal nonempty true empty false without candidate evaluation',all(type(x['result'])is bool and x['result']==(x['size']>0)for x in demonstration))
archives=[]
for label,root,key in [('ORIGINAL_COMPLETE_SOURCE',ORIGINAL,'original'),('ORIGINAL_BLOCKED_SOURCE_PEER',BLOCKED,'blocked'),('ORIGINAL_BLOCKED_SOURCE_PEER_TRUE_SEAL',BLOCKED_SEAL,'blocked_seal'),('ORIGINAL_AUTHOR_SOURCE_TRUE_SEAL',SOURCE_SEAL,'original_seal')]:
    archive=P/(label+'.tar.gz');view=before[key]
    with tarfile.open(archive,'w:gz',compresslevel=9)as out:
        for rel in view['directories']:
            path=root/rel;info=out.gettarinfo(str(path),arcname=rel);require(info.isdir(),'complete directory entry');out.addfile(info)
        for rel,expected in view['files'].items():
            path=root/rel;require(pin(path)[0]==expected,'archive original pin before read')
            info=out.gettarinfo(str(path),arcname=rel);require(info.isfile(),'wholeSource regular archive')
            with path.open('rb')as stream:out.addfile(info,stream)
            require(pin(path)[0]==expected,'archive original pin after read')
    seenfiles={};seendirs=[]
    with tarfile.open(archive,'r:gz')as inp:
        for member in inp:
            if member.isdir():seendirs.append(member.name);continue
            require(member.isfile(),'no archive link/special entry');f=inp.extractfile(member)
            digest=hashlib.sha256();total=0
            while True:
                b=f.read(2**20)
                if not b:break
                total+=len(b);digest.update(b)
            require(member.name not in seenfiles,'all archive members unique');seenfiles[member.name]=dict(sha256=digest.hexdigest(),size_bytes=total)
    check(label+' whole lossless Source archive all files manifests dirs fullEOF verified',set(seenfiles)==set(view['files'])and set(seendirs)==set(view['directories'])and all(seenfiles[n]=={k:expected[k]for k in ('sha256','size_bytes')}for n,expected in view['files'].items()))
    archives.append(dict(role=label,archive_pin=pin(archive)[0],original_inventory=view,complete_files=len(view['files']),complete_directories=len(view['directories']),all_member_bytes_SHA_EOF_verified=True,all_original_manifests_preserved=True,no_Source_members_omitted=True))
after={k:inventory(r)for k,r in [('original',ORIGINAL),('blocked',BLOCKED),('blocked_seal',BLOCKED_SEAL),('original_seal',SOURCE_SEAL)]}
check('all original Source peer and true seal members dirs beforeafter completely unchanged',before==after)
save('COMPLETE_SIX_HUNK_SOURCE_INVERSE_AND_DEFINITION_PROOF.json',dict(schema='COMPLETE_CONTEXT_SIX_BLOCKER_FINITE_SOURCE_INVERSE_V1',source_only=True,derivations=inverse,all191_other_Source_bytes_unchanged=True,all_branch_and_arithmetic_statements_unchanged=True,require_error_texts_unchanged=True,final_report_full_field_union_unchanged=True,report_fixed_field_order_note='The old duplicate-key dict call could not create a runtime report. Its duplicated explicit False keyword is removed; the same False field remains once at its original FALSE expansion position. All other keywords and record algorithms retain their order.',actual_binding=None,new_Q=None))
save('COMPLETE_ORIGINAL_SOURCE_PEER_AND_TRUE_SEAL_LOSSLESS_ARCHIVES.json',dict(source_only=True,archives=archives,before=before,after=after))
save('ALL_THREE_STRICT_REQUIRE_AND_FALSE_KWARG_SOURCE_AUDIT.json',dict(source_only=True,raw_truth_operands_remaining=terminal_audit,all_remaining_raw_falsy_operands_reject_invalid_inputs=True,no_legal_nonempty_list_or_dict_terminal_conditions=True,all_dict_FALSE_call_sites=kwarg_audit,isolated_language_demonstration=demonstration,candidate_executed=False,all_original_error_texts_retained=True))
(P/'AUTHOR_SCOPE_AND_ONLY_SIX_CORRECTIONS.txt').write_text('Finite UNREADY Source derivative. Only six Source hunks in three roles: engine four, old-XSM extractor one, Source binder one. Five exact-bool conditions now use explicit type and len>0; the final duplicate keyword is removed only from that report dict call, while the same False field remains in the unchanged FALSE expansion. No physics/arithmetic/control branch or record algorithm changes. All original191 unchanged members and the full original194+MANIFEST Source archive are retained; full BLOCKED Source peer and its genuine seal/postseal receipts are complete lossless archives. Historical author reports/inverses are preserved as historical evidence, not a current independent PASS.\n\nNo candidate/helper/guard/API/compile/DB/material execution. The original UNREADY statuses, all unknown future pins, caps and complete scopes remain. Author static checks cannot confer independent Source admission, new Q, runtime/RSS or science. Root must obtain a genuine independent finite whole-source review before any Source-only binding. Then separately observed context/native/extraction controls and genuine execution are required.\n',encoding='utf8')
check('all author finite checks uniquely labeled and typed true',len({x['check']for x in CHECKS})==len(CHECKS)and all(x['passed']is True for x in CHECKS))
save('AUTHOR_FINITE_COMPLETE_SOURCE_REVIEW.json',dict(schema='AUTHOR_COMPLETE_CONTEXT_SIX_BLOCKER_FINITE_UNREADY_SOURCE_REVIEW_V1',status='AUTHOR_STATIC_SOURCE_CHECKS_COMPLETE_NOT_INDEPENDENT_ADMISSION',source_only=True,check_count=len(CHECKS),checks=CHECKS,all_checks_typed_true=True,changed_roles={name:pin(P/name)[0]for name in changes},parent_manifest_pin=before['original']['files']['MANIFEST.json'],parent_blocked_peer_pin=before['blocked']['files']['REVIEW.json'],parent_blocked_peer_manifest_pin=before['blocked']['files']['MANIFEST.json'],all_original_scopes_and_caps_unchanged=True,all_future_unknown_pins_unchanged=True,actual_candidate_execution=None,actual_independent_review=None,actual_binding=None,new_Q=None,scientific_qualification_created=False))
print(json.dumps(dict(source_only=True,status='AUTHOR_STATIC_UNREADY_SOURCE_DERIVED_NO_EXECUTION_OR_QUALIFICATION',review=pin(P/'AUTHOR_FINITE_COMPLETE_SOURCE_REVIEW.json')[0],check_count=len(CHECKS),changed_roles={name:pin(P/name)[0]for name in changes},all_original_Source_archives_verified=True,actual_independent_review=None,new_Q=None)),flush=True)
