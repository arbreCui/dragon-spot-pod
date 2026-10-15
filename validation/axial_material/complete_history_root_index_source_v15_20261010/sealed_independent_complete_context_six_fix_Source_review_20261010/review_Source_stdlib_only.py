"""Independent finite Source/META review. Never imports or executes candidates."""
import ast
import difflib
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import tarfile
import tempfile

ROOT = Path('/Users/wen/spot')
B = ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010'
S = Path('/private/tmp/axmat_complete_old_XSM_context_six_blocker_finite_UNREADY_Source_fix_novkasox')
T = B/'finite_current150_old_XSM_context_six_blocker_fix_UNREADY_SOURCE_20261010'
OLD = Path('/private/tmp/axmat_COMPLETE_oldXSM_context_aware_aggregation_UNREADY_SOURCE_20261010_s7ik4_qc')
OLD_SAVED = B/'finite_current150_old_XSM_context_aware_aggregation_UNREADY_SOURCE_20261010'
OLD_PEER = B/'sealed_independent_old_XSM_context_Source_BLOCKED_review_20261010'
RECORD = B/'Root_actual_old_XSM_context_six_blocker_fix_Source_retention_record.json'
TOOL = B/'Root_actual_old_XSM_context_six_blocker_fix_Source_retention_tool_return.json'
SEAL = Path(str(S)+'_seal_receipt')
P = Path(tempfile.mkdtemp(prefix='axmat_independent_complete_context_six_fix_Source_review_',dir='/private/tmp'))
checks = []
blockers = []

def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def require(condition,message):
    if type(condition) is not bool or not condition:
        raise ValueError(message)

def full_pin(path):
    path = Path(path)
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,'regular single-link Source')
    h = hashlib.sha256(); size = 0
    with path.open('rb') as stream:
        require(identity(os.fstat(stream.fileno())) == identity(before),'opened Source identity')
        while True:
            raw = stream.read(2**20)
            if not raw: break
            h.update(raw); size += len(raw)
        require(identity(os.fstat(stream.fileno())) == identity(before),'complete Source unchanged')
    require(identity(path.lstat()) == identity(before) and size == before.st_size,'path Source unchanged')
    return dict(path=str(path),sha256=h.hexdigest(),size_bytes=size,identity=identity(before))

def snapshot(root):
    result=dict(root=str(root),files={},directories={})
    for path in [root,*sorted(root.rglob('*'))]:
        s=path.lstat(); rel='.' if path == root else str(path.relative_to(root))
        require(not stat.S_ISLNK(s.st_mode),'no Source symlinks')
        if stat.S_ISDIR(s.st_mode):result['directories'][rel]=identity(s)
        else:result['files'][rel]=full_pin(path)
    return result

def check(label,value):
    require(type(value) is bool,'typed finite review check')
    require(label not in {r['check'] for r in checks},'unique finite check labels')
    checks.append(dict(check=label,passed=value))
    if not value:blockers.append(dict(check=label,reason='Independent Source/META contract failed; no candidate execution.'))

def save(name,obj):
    path=P/name
    with path.open('x') as stream:json.dump(obj,stream,ensure_ascii=False,indent=2);stream.write('\n')

before={
    'original':snapshot(S),'retained':snapshot(T),'old_original':snapshot(OLD),
    'old_retained':snapshot(OLD_SAVED),'old_peer':snapshot(OLD_PEER),'new_source_seal':snapshot(SEAL),
    'Root_retention_record':full_pin(RECORD),'Root_retention_tool':full_pin(TOOL),
}
manifest=json.loads((S/'MANIFEST.json').read_bytes())
data={rel:(S/rel).read_bytes() for rel in before['original']['files']}
old_data={rel:(OLD/rel).read_bytes() for rel in before['old_original']['files']}
ret=json.loads(RECORD.read_bytes());rt=json.loads(TOOL.read_bytes())
check('current complete Source manifest exact Root-request SHA',before['original']['files']['MANIFEST.json']['sha256']=='c8bb4b0738e6dfdf45e81724fcd2644bcf5c9740c5ad8f8ed87de5c003144815')
check('current full209 members plus manifest210 files ten directories exact inventory',manifest['member_count']==209 and len(manifest['members'])==209 and len(before['original']['files'])==210 and len(before['original']['directories'])==10 and set(before['original']['files'])=={m['relative_path'] for m in manifest['members']}|{'MANIFEST.json'})
check('all209 current Source full EOF size SHA seven exact integer IDs match manifest',all(before['original']['files'][m['relative_path']]=={k:v for k,v in m.items() if k!='relative_path'} for m in manifest['members']))
check('all current Source directories IDs match sealed manifest',len(manifest['directories'])==10 and all(before['original']['directories'][d['relative_path']]==d['identity'] for d in manifest['directories']))
check('Root retained full210 Source plus true seal211 files no members omitted',len(before['retained']['files'])==211 and set(before['retained']['files'])==set(before['original']['files'])|{'_actual_peer_seal_receipt.json'} and len(before['retained']['directories'])==10 and all(before['retained']['files'][rel]['sha256']==pin['sha256'] and before['retained']['files'][rel]['size_bytes']==pin['size_bytes'] for rel,pin in before['original']['files'].items()))
check('Root actual new retention record exact requested SHA and source-only',before['Root_retention_record']['sha256']=='b34a04f79e0f4db892942375157bb687edccf7910d6c50bb50a2de0544e0e51a' and ret['source_only'] is True and ret['complete_original_member_count']==210)
check('Root all210 original and saved coupled pins use their genuine different seven IDs',set(ret['complete_original_members'])==set(before['original']['files']) and all(v['original']==before['original']['files'][rel] and v['saved']==before['retained']['files'][rel] for rel,v in ret['complete_original_members'].items()))
check('Root true retention tool is exact integer EXIT0 CLOSED genuine2b1ec5',rt['closed'] is True and type(rt['actual_tool_return']['exit_code']) is int and rt['actual_tool_return']['exit_code']==0 and rt['actual_tool_return']['chunk_id']=='2b1ec5' and 'session_id' not in rt['actual_tool_return'])
check('true source seal copied by Root has same complete bytes and pin',ret['saved_actual_peer_seal_receipt']==before['retained']['files']['_actual_peer_seal_receipt.json'] and ret['original_actual_peer_seal_receipt']==full_pin(SEAL/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json') and ret['saved_actual_peer_seal_receipt']['sha256']==ret['original_actual_peer_seal_receipt']['sha256'])
seal_truth=json.loads((SEAL/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json').read_bytes())
post_truth=json.loads((SEAL/'ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json').read_bytes())
check('author genuine once seal6356f9 and postseal dfc9df independently pinned closed0',all(x['closed'] is True and x['source_only'] is True and type(x['terminal_tool_return']['exit_code']) is int and x['terminal_tool_return']['exit_code']==0 and 'session_id' not in x['terminal_tool_return'] and x['candidate_executed'] is False for x in (seal_truth,post_truth)) and seal_truth['terminal_tool_return']['chunk_id']=='6356f9' and post_truth['terminal_tool_return']['chunk_id']=='dfc9df')

old_manifest=json.loads(old_data['MANIFEST.json'])
check('old complete194 members195 files ten dirs exact SHA sealed source family',len(old_manifest['members'])==194 and len(before['old_original']['files'])==195 and before['old_original']['files']['MANIFEST.json']['sha256']=='2c0b20393b5ab202be815be6524d417c7c18ea91da719b05dc678948f920dd89' and all(before['old_original']['files'][m['relative_path']]=={k:v for k,v in m.items() if k!='relative_path'} for m in old_manifest['members']))
check('old Root retained full195 plus actual seal196 unchanged exact bytes',len(before['old_retained']['files'])==196 and set(before['old_retained']['files'])==set(old_data)|{'_actual_peer_seal_receipt.json'} and all(before['old_retained']['files'][rel]['sha256']==pin['sha256'] and before['old_retained']['files'][rel]['size_bytes']==pin['size_bytes'] for rel,pin in before['old_original']['files'].items()))
changed=list(manifest['changed_roles'])
check('exact three runtime roles fixed original hashes now match new declared pins',len(changed)==3 and set(changed)=={'complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py','complete_observed_old_post_final_XSM_extractor.UNREADY.py','bind_complete_context_aware_and_oldXSM_SOURCE_only.UNREADY.py'} and all(manifest['changed_roles'][n]==before['original']['files'][n] for n in changed))
check('all191 other original members and original manifest retained complete byte exact',all(data[n]==raw for n,raw in old_data.items() if n!='MANIFEST.json' and n not in changed) and data['ORIGINAL_COMPLETE_SOURCE_MANIFEST.json']==old_data['MANIFEST.json'] and sum(n!='MANIFEST.json' and n not in changed for n in old_data)==191)
archives=json.loads(data['COMPLETE_ORIGINAL_SOURCE_PEER_AND_TRUE_SEAL_LOSSLESS_ARCHIVES.json'])
archive_results=[]
for item in archives['archives']:
    ap=Path(item['archive_pin']['path']);expected=item['original_inventory'];actual={};dirs=[]
    require(full_pin(ap)==item['archive_pin'],'Source archive full pin')
    with tarfile.open(ap,'r:gz') as tar:
        for member in tar:
            name=member.name.rstrip('/') or '.'
            require(name not in actual and name not in dirs,'unique Source tar member')
            require(not member.issym() and not member.islnk(),'no tar aliases')
            if member.isdir():dirs.append(name);continue
            require(member.isfile() and name in expected['files'],'complete declared Source archive file')
            stream=tar.extractfile(member);h=hashlib.sha256();size=0
            while True:
                raw=stream.read(2**20)
                if not raw:break
                h.update(raw);size+=len(raw)
            stream.close();ep=expected['files'][name]
            require(size==member.size==ep['size_bytes'] and h.hexdigest()==ep['sha256'],'Source archived member complete EOF SHA size')
            actual[name]=dict(size_bytes=size,sha256=h.hexdigest())
    with gzip.open(ap,'rb') as stream:
        while stream.read(2**20):pass
    require(set(actual)==set(expected['files']) and set(dirs)==set(expected['directories']),'all Source archived members directories retained')
    archive_results.append(dict(role=item['role'],archive_pin=item['archive_pin'],files=actual,directories=dirs,full_gzip_EOF_CRC_ISIZE_verified=True))
check('all four Source provenance archives preserve full files dirs manifests streaming EOF SHA and gzip trailer',len(archive_results)==4 and [len(x['files']) for x in archive_results]==[195,35,4,2])
check('full archived old Source exactly equals independently read old195 file bytes and original directories',all(archive_results[0]['files'][n]['sha256']==p['sha256'] and archive_results[0]['files'][n]['size_bytes']==p['size_bytes'] for n,p in before['old_original']['files'].items()) and set(archive_results[0]['directories'])==set(before['old_original']['directories']))
old_review=json.loads((OLD_PEER/'REVIEW.json').read_bytes());old_blockers=json.loads((OLD_PEER/'SIX_PRECISE_SOURCE_BLOCKERS.json').read_bytes())
check('prior independent BLOCKED review full forty checks retains precisely six blockers and38passes',old_review['schema']=='INDEPENDENT_COMPLETE_CONTEXT_AWARE_ENGINE_HOST_BINDER_SOURCE_REVIEW_V2' and old_review['status']=='SOURCE_ONLY_BLOCKED_NO_EXECUTION_OR_SCIENCE' and old_review['source_only'] is True and len(old_review['checks'])==old_review['check_count']==40 and sum(c['passed'] is True for c in old_review['checks'])==38 and len(old_review['blockers'])==len(old_blockers['blockers'])==6)
check('archived original independent BLOCKED review and Root saved counterpart byte exact',archive_results[1]['files']['REVIEW.json']['sha256']==before['old_peer']['files']['REVIEW.json']['sha256'] and archive_results[1]['files']['SIX_PRECISE_SOURCE_BLOCKERS.json']['sha256']==before['old_peer']['files']['SIX_PRECISE_SOURCE_BLOCKERS.json']['sha256'])

parent=json.loads(old_data['COMPLETE_FIXED_PARENT_SOURCE/MANIFEST.json'])
check('complete fixed parent162 members and original manifest preserved current full Source',parent['member_count']==162 and len(parent['members'])==162 and sum(n.startswith('COMPLETE_FIXED_PARENT_SOURCE/')for n in data)==163 and all(hashlib.sha256(data['COMPLETE_FIXED_PARENT_SOURCE/'+m['relative_path']]).hexdigest()==m['sha256'] and len(data['COMPLETE_FIXED_PARENT_SOURCE/'+m['relative_path']])==m['size_bytes']for m in parent['members']))
old_bysha={hashlib.sha256(raw).hexdigest():raw for raw in old_data.values()}
original_chain_results=[]
def recover_original_source(candidate,d):
    require(hashlib.sha256(candidate).hexdigest()==d['candidate_SHA256'],'full original chain candidate SHA')
    rows=candidate.decode().splitlines(True)
    for h in reversed(d['complete_zero_based_hunks']):
        require(rows[h['new_start0']:h['new_end0']]==h['new_full_lines'],'full original chain hunk bytes')
        rows[h['new_start0']:h['new_end0']]=h['old_full_lines']
    original=''.join(rows).encode()
    require(hashlib.sha256(original).hexdigest()==d['original_SHA256'],'complete original chain parent SHA')
    if d['original_SHA256']in old_bysha:require(original==old_bysha[d['original_SHA256']],'original whole parent Source bytes')
    old_bysha[d['original_SHA256']]=original
    return original
for name in ('COMPLETE_CONTEXT_AWARE_SOURCE_FULL_INVERSE.json','COMPLETE_CONTEXT_GENUINE_HOST_BINDER_FULL_INVERSE.json'):
    for d in json.loads(old_data[name])['derivations']:
        orig=recover_original_source(old_data[d['candidate']],d)
        original_chain_results.append(dict(candidate=d['candidate'],candidate_SHA256=d['candidate_SHA256'],original_SHA256=d['original_SHA256'],complete_hunk_count=len(d['complete_zero_based_hunks']),whole_bytes_inverse_verified=True))
check('all eleven original engine observer extractor host binder full byte inverse contracts retained',len(original_chain_results)==11 and all(x['whole_bytes_inverse_verified']is True for x in original_chain_results))
native_proof=json.loads(old_data['COMPLETE_V23_OLD_XSM_EXTRACTION_SOURCE_INVERSE.json'])
native_source=recover_original_source(old_bysha[native_proof['candidate_SHA256']],native_proof)
check('complete old extractor original native chain recovers exact actual9d849 Source',native_source==data['COMPLETE_FIXED_PARENT_SOURCE/FINITE_ACTUAL_NATIVE_V23_SOURCE_META/Root_bound_complete_native_checker.py'])
def top_nodes(raw):return {n.name:ast.dump(n,include_attributes=False)for n in ast.parse(raw).body if isinstance(n,(ast.ClassDef,ast.FunctionDef))}
native_nodes=top_nodes(native_source);current_nodes=top_nodes(data['complete_observed_old_post_final_XSM_extractor.UNREADY.py'])
check('all three original native walker classes unchanged full current AST',all(current_nodes[n]==native_nodes[n] for n in('XSM','ReadOnlyFileBytes','DiskRecords')))

proof=json.loads(data['COMPLETE_SIX_HUNK_SOURCE_INVERSE_AND_DEFINITION_PROOF.json'])
inverse_results=[]
def definitions(tree):
    result={}
    def walk(node,prefix=''):
        for n in ast.iter_child_nodes(node):
            if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                name=prefix+n.name;result[name]=ast.dump(n,include_attributes=False);walk(n,name+'.')
            else:walk(n,prefix)
    walk(tree);return result
for d in proof['derivations']:
    name=d['candidate'];raw=data[name];orig=old_data[name]
    require(d['candidate_pin']==before['original']['files'][name] and d['original_pin']==before['old_original']['files'][name],'exact original/new Source pins')
    oldrows=orig.decode().splitlines(True);newrows=raw.decode().splitlines(True)
    actual_hunks=[dict(tag=tag,old_start0=a,old_end0=b,new_start0=c,new_end0=e,old_full_lines=oldrows[a:b],new_full_lines=newrows[c:e]) for tag,a,b,c,e in difflib.SequenceMatcher(a=oldrows,b=newrows,autojunk=False).get_opcodes() if tag!='equal']
    require(actual_hunks==d['complete_zero_based_hunks'],'all byte difference hunks exact')
    restored=newrows[:]
    for h in reversed(actual_hunks):restored[h['new_start0']:h['new_end0']]=h['old_full_lines']
    require(''.join(restored).encode()==orig,'all original Source bytes reverse recovered')
    od,nd=definitions(ast.parse(orig)),definitions(ast.parse(raw))
    require(set(od)==set(nd),'every Source definition retained')
    diff=[n for n in od if od[n]!=nd[n]]
    require(diff==d['changed_definitions'],'only declared changed definitions')
    actual_unchanged={n for n in od if od[n]==nd[n]}
    require(set(d['all_unchanged_definition_AST_exact'])<=actual_unchanged,'every author-listed unchanged AST verified plus all nested functions')
    inverse_results.append(dict(candidate=name,original_pin=d['original_pin'],candidate_pin=d['candidate_pin'],complete_hunks=actual_hunks,full_original_byte_inverse=True,definition_count=len(od),changed_definitions=diff,unchanged_definition_count=len(od)-len(diff),author_listed_definition_count=d['original_definition_count'],additional_unchanged_nested_AST_verified=sorted(actual_unchanged-set(d['all_unchanged_definition_AST_exact'])),definition_scope_note='Independent recursive AST walk also includes definitions nested under try/with/conditional statements. Full byte inverse covers every Source statement regardless of inventory count.'))
check('all six independently recomputed hunks inverse engine4 extractor1 binder1 no other Source byte change',[len(x['complete_hunks']) for x in inverse_results]==[4,1,1] and [x['definition_count'] for x in inverse_results]==[73,49,12])
check('all physics record branch arithmetic classes and129 unchanged nested definitions exact AST',sum(x['unchanged_definition_count'] for x in inverse_results)==129 and all('ContextAwareConstruction' not in x['changed_definitions'] and 'CompleteConstruction' not in x['changed_definitions'] and 'Binary32Model' not in x['changed_definitions'] and 'XSM' not in x['changed_definitions'] for x in inverse_results))
trees={n:ast.parse(raw) for n,raw in data.items() if n.endswith('.py')}
check('all complete Python Source AST parsed no candidate import compile or execution',len(trees)>0 and all(type(x) is ast.Module for x in trees.values()))
source_require_audit=[];false_calls=[];fixes=[]
bool_names={'complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py':{'mat','required','zero'},'complete_observed_old_post_final_XSM_extractor.UNREADY.py':{'ended'},'bind_complete_context_aware_and_oldXSM_SOURCE_only.UNREADY.py':{'zero'}}
allowed_nonbool={('complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py',1011):{'pending'},('complete_observed_old_post_final_XSM_extractor.UNREADY.py',251):{'name'},('bind_complete_context_aware_and_oldXSM_SOURCE_only.UNREADY.py',243):{"ctx['complete_context_pins']"}}
def bool_expr(n,names):
    if isinstance(n,ast.Compare):return True
    if isinstance(n,ast.Constant):return type(n.value) is bool
    if isinstance(n,ast.UnaryOp)and isinstance(n.op,ast.Not):return True
    if isinstance(n,ast.Name):return n.id in names
    if isinstance(n,ast.BoolOp):return all(bool_expr(x,names) for x in n.values)
    if isinstance(n,ast.IfExp):return bool_expr(n.body,names)and bool_expr(n.orelse,names)
    if isinstance(n,ast.Call):
        if isinstance(n.func,ast.Name):return n.func.id in {'all','any','bool','isinstance'}
        if isinstance(n.func,ast.Attribute):return n.func.attr in {'is_absolute','is_relative_to','isfinite','S_ISREG','S_ISLNK'}
    return False
for name in changed:
    tree=trees[name]
    rd=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='require')
    rsource=ast.unparse(rd)
    require('type(' in rsource and 'is not bool' in rsource,'same exactbool require')
    oldt=ast.parse(old_data[name]);before_calls=[n for n in ast.walk(oldt) if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='require']
    after_calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='require']
    require(len(before_calls)==len(after_calls),'all require callsites retained')
    before_byline={n.lineno:n for n in before_calls}
    for call in sorted(after_calls,key=lambda n:n.lineno):
        expr=call.args[0];oldcall=before_byline[call.lineno]
        require(ast.dump(ast.Tuple(elts=call.args[1:],ctx=ast.Load()),include_attributes=False)==ast.dump(ast.Tuple(elts=oldcall.args[1:],ctx=ast.Load()),include_attributes=False),'every original strict error argument unchanged')
        if ast.dump(expr,include_attributes=False)!=ast.dump(oldcall.args[0],include_attributes=False):
            fixes.append(dict(file=name,line=call.lineno,old_condition=ast.unparse(oldcall.args[0]),new_condition=ast.unparse(expr),error_arguments_unchanged=True))
            require(bool_expr(expr,bool_names[name]),'fixed entry returns builtin bool from compares')
        raws=[]
        def operands(n):
            if isinstance(n,ast.BoolOp):
                for value in n.values:operands(value)
            elif not bool_expr(n,bool_names[name]):raws.append(ast.unparse(n))
        operands(expr)
        if raws:
            require(set(raws)==allowed_nonbool.get((name,call.lineno),set()),'no unreviewed strict require nonboolean terminal')
            require(isinstance(expr,ast.BoolOp)and isinstance(expr.op,ast.And)and bool_expr(expr.values[-1],bool_names[name]),'nonempty legitimate leading containers terminate in genuine bool')
        source_require_audit.append(dict(file=name,line=call.lineno,condition=ast.unparse(expr),nonboolean_leading_operands=raws,legal_nonempty_scope_returns_bool=True,malformed_empty_scope_is_rejected_without_candidate_execution=True))
    false=next((n for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='FALSE'for t in n.targets)),None)
    if false is not None:
        require(isinstance(false.value,ast.Call)and isinstance(false.value.func,ast.Name)and false.value.func.id=='dict','FALSE Source constructor')
        keys={k.arg for k in false.value.keywords};require(all(isinstance(k.value,ast.Constant)and k.value.value is False for k in false.value.keywords),'all FALSE flags remain literal False')
        for call in ast.walk(tree):
            if isinstance(call,ast.Call)and isinstance(call.func,ast.Name)and call.func.id=='dict'and any(k.arg is None and isinstance(k.value,ast.Name)and k.value.id=='FALSE'for k in call.keywords):
                explicit=[k.arg for k in call.keywords if k.arg];collision=keys&set(explicit)
                false_calls.append(dict(file=name,line=call.lineno,explicit_keys=explicit,expanded_FALSE_keys=sorted(keys),collisions=sorted(collision)))
                require(not collision and len(explicit)==len(set(explicit)),'all dict FALSE sites disjoint')
check('all five exactbool entry fixes independently detected source domains and all errors retained',len(fixes)==5 and sorted(x['line'] for x in fixes)==[227,770,926,1031,1040])
check('all three full strict require scans no legal nonempty list dict terminal omitted',len(source_require_audit)>200 and sum(bool(x['nonboolean_leading_operands'])for x in source_require_audit)==3)
field_def=next(n for n in ast.walk(trees['complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py'])if isinstance(n,ast.FunctionDef)and n.name=='field')
field_calls=[n for n in ast.walk(trees['complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py'])if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='field']
ended_assignments=[n.value for n in ast.walk(trees['complete_observed_old_post_final_XSM_extractor.UNREADY.py'])if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='ended'for t in n.targets)]
check('remaining OR mat and AND ended Source names have complete genuine boolean domains',field_def.args.args[-1].arg=='mat'and isinstance(field_def.args.defaults[-1],ast.Constant)and field_def.args.defaults[-1].value is False and bool(field_calls)and all(len(n.args)<5 and all(k.arg!='mat'or(isinstance(k.value,ast.Constant)and type(k.value.value)is bool)for k in n.keywords)for n in field_calls)and bool(ended_assignments)and all(bool_expr(x,set())for x in ended_assignments))
check('all seven complete dict FALSE sites no overlap and unchanged literal False flags',len(false_calls)==7 and all(x['collisions']==[] for x in false_calls))
engine_name='complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py'
oldtree=ast.parse(old_data[engine_name]);newtree=trees[engine_name]
def report_union(tree):
    false=next(n.value for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='FALSE'for t in n.targets))
    call=next(n for n in ast.walk(tree)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='dict'and n.lineno==1756)
    explicit={k.arg:ast.dump(k.value,include_attributes=False)for k in call.keywords if k.arg}
    expanded={k.arg:ast.dump(k.value,include_attributes=False)for k in false.keywords}
    return explicit|expanded,set(explicit)&set(expanded)
ou,oc=report_union(oldtree);nu,nc=report_union(newtree)
check('duplicate False removal keeps completed report full field union and exact False semantic',oc=={'genuine_supervisor_watch_verified_here'} and nc==set()and ou==nu)

# Prior independently specified full-family Source invariants are re-evaluated
# against every current Source byte, after the complete inverse established scope.
engine=data['complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py'].decode()
host=data['complete_context_aware_aggregation_and_oldXSM_genuine_host.UNREADY.py'].decode()
binder=data['bind_complete_context_aware_and_oldXSM_SOURCE_only.UNREADY.py'].decode()
observer=data['AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90'].decode()
extract=data['complete_observed_old_post_final_XSM_extractor.UNREADY.py'].decode()
adapter=data['saved_native_data_access_adapter.UNREADY.py'].decode()
tondrv=data['TONDRV.context_observe.UNREADY.f'].decode()
libden=data['COMPLETE_FIXED_PARENT_SOURCE/DIRECT_OBSERVATION_API_SOURCE/LIBDEN.f'].decode()
check('whole1800 stage600 RSS512 joint2GiB history96 free8 threads1 child1 retry0 Source retains original caps',all(x in engine for x in ('whole_seconds=1800','stage_seconds=600','rss_mib=512','joint_archive_bytes=2*2**30','history_bytes=96*2**30','free_floor_bytes=8*2**30','threads=1','children_at_once=1','retries=0')) and 'WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30' in host)
check('original normal support genuine guard MRO OwnRSS and dynamic five ART history roots preserved',all(x in host for x in ('3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7','helper.guard_admission(full)','full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)','resource.history_roots([str(host),str(out),str(control),str(support.OUT),str(support.TERMINAL)],support.ART)','resources=resource.DynamicHistoryResources','resources.check()')))
check('complete original129 plus every actual evidence and Source D E full beforeafter protects metadata pins',all(x in host for x in ('len(b[\'original129_input_pins\'])==129','source_inputs=complete_source_inputs','receipt_inputs=complete_source_inputs','complete_directory_identity(archive)','complete_directory_identity(receipts)','full_postclose_input_and_D_E_check_errors')) and 'complete=original+additional' in binder)
check('full joint HOCDE SQL journal spool and open-unlinked byte accounting Source preserved',all(x in engine for x in ("('host','output','control','source','receipts')",'s.st_nlink==0','total+=sum(unlinked.values())')) and all(x in extract for x in ('s.st_nlink==0','total+=sum(unlinked.values())')) and 'support.archive_bytes(roots5)' in host)
check('original8MiB SQLite FILE temp zero mmap read-only adapter and serial A closed before B',all(x in adapter for x in ('PRAGMA cache_size=-8192','PRAGMA mmap_size=0','PRAGMA temp_store=FILE','mode=ro','PRAGMA query_only=ON')) and 'for item in reversed(opened):item.close()' in engine and 'saved.close()' in engine and "for state in ('A','B'):" in engine)
check('observer preserves all ordered context events and all old pre post final native snapshots version2',all(x in observer for x in ("'AXOBSCTX',2_c_int32_t","'oldmacro-pre-LIBMIX'","'oldmacro-LIBDEN'","'postmacro-LIBMIX'","'final-complete-micro'",'call LCMEQU(target,saved)')) and "for p in ctx['complete_context_pins']:shape_only(p)" in binder)
check('TONDRV new SPH decision sits immediately before original true branch and full factor capture precedes TONCMI',tondrv.index('CALL AXOBS_SPH_DECISION')<tondrv.index('IF(NBNRS.GT.1) THEN') and 'CALL AXOBS_SPH' in data['TONSPH.observe.UNREADY.f'].decode() and 'CALL TONCMI' in data['TONSPH.observe.UNREADY.f'].decode())
check('actual KSPH INRS false and true decisions coupled to2960 factor words without h1 assumption',all(x in engine for x in ("[e['dimensions']['INRS']for e in decisions]==list(range(1,nres+1))","if e['dimensions']['NBNRS']>1","[e['dimensions']['INRS']for e in sph]==selected",'all2960_factor_words=True','factors_assumed_one=False')))
check('MAT full raw stream and actual mix density MASK MASKL derivation are preserved without all-mask assumption',all(x in engine for x in ('FULL_ORIGINAL_CONTEXT_WORDS','MAT-eliminated isotope flags remain zero','Source exact MAT/LSHI/group-range mask derivation','self.mix==b[\'fields\'][\'MIX\']and self.density==b[\'fields\'][\'DEN\']','self.maskk==(old_saved is not None)==(pre_saved is not None)')))
check('old pre post final full record type count bits physical order coupling preserved',all(x in engine for x in ('same_snapshots(pre_saved,old_saved','same_snapshots(post_saved,saved','original_word_count','complete original snapshot byte mismatch','full original physical path/key/type/count order','FULL_ORIGINAL_OBSERVED_SNAPSHOT_RECORD')))
check('all complete context and snapshot lists tied to saved extraction META with no final pool substitute',all(x in engine for x in ("cov['states'][state]['all_snapshot_pairs']==actual['all_snapshot_pairs']","cov['states'][state]['complete_context_pins']==actual['complete_context_pins']","cov['actual_closed_extraction_receipt_independently_reviewed']is True","final_pair['sqlite_pin']==source['sqlite_pin']","final_pair['native_pool_pin']==source['native_pool_pin']")))
check('full original370 by8 P0 P1 P2 scope all19619 macro records retained or unknown',all(x in engine for x in ('self.macro_records == 19619','370*370*8*3','original_scope=[370,8,3,32,64,62,18,6,48]','UNQUALIFIED_NOT_DROPPED','PHASE_FAILED')))
check('scatter SIGS independent of SCAT FACT order and LOGL newGAF before old restoration match source',all(x in engine for x in ('self.fp.multiply(sigma[dest],den)','self.fp.multiply(self.fp.multiply(scat[cursor],den),fact)','Source LOGL is evaluated on new GAF before restoring old SCAT','LIBDEN_CHECK_ACTUAL_DESTINATION_WRITE_ORDER')) and 'GA2(IOF)*DEN(ISOT)*FACT' in libden)
check('scalar NTOT H C transport and masked old DIFF reciprocal roundtrip all preserved',all(x in engine for x in ("names=('NTOT0','NTOT1','STRD','H-FACTOR','C-FACTOR','OVERV','TRANC')","self.fp.divide(0x3f800000,self.fp.multiply(0x40400000,old[m]))","LIBDEN_SCALAR_ACTUAL_CONTEXT_")))
check('all18 edit names duplicate order original goto720 special fields and EXIST carry retained',all(x in engine for x in ('len(self.extra_names)==18','for ordinal,name in enumerate(self.extra_names,1)','ACTUAL_CONTEXT_EXTRA_GOTO720','LIBDEN_EXTRA_','ACTUAL_EXIST_ORDER',"if old is not None:exists=True")))
check('full actual NFISS0 pre mutation INDFIS and density-unfiltered allocation preserved not final self proof',all(x in engine for x in ('INDFIS_DEFINED_PRE_MUTATION','validate_old_indfis','density_zero_not_filtered=True',"self.nfiss0=f['dimensions']['NFISS0']",'slot+1>self.nfiss0*4')) and 'IF(KFIS.GT.NFISS0*NESP)' in libden)
check('full32 prompt256 and all six delayed pairs old init exact unknown masks retained',all(x in engine for x in ('for delayed in range(7):',"nus=array('I',[0])*256;chis=array('I',[0])*256;known=array('B',[0])*256",'LIBDEN_OLD_INIT_PROMPT_ALL6_DELAYED256','original Source initialization does not define every component')))
check('all48 Lambda old initialization slot1-only missing branch and last mix writes preserved',all(x in engine for x in ("expected=array('I',[0])*48;known=array('B',[0])*48","if old is None:known[:6]=array('B',[1])*6",'LIBDEN_LAMBDA48_ACTUAL_OLD_INITIALIZATION_LAST_WRITE','other old slots undefined')))
check('full STATE40 old maxima and TIMESTAMP old overwrite and volume flux last-write retained',all(x in engine for x in ('max(self.nbm0,8)','state[10:]','LIBDEN_OLD_STATE40_MAXIMA_ACTUAL_FLAGS','LIBMIX_OLD_TIMESTAMP_LIBDEN_WRITE','ROOT_MIXTURESVOL_BEFORE','LIBDEN_FLUX_LAST_WRITE_ALL_GROUPS')))
check('native all nine kinds containers DOUBLE complete words preserved with unchanged native walker',"kind in (0, 1, 2, 3, 4, 5, 6, 10, 99)" in extract and 'words % 2 == 0' in extract and 'original_word_count' in adapter and 'ORIGINAL_PRESENT_NO_PROVED_AGGREGATION_RULE' in engine)
check('unresolved character double-libm uninitialized words remain explicit unqualified gaps',all(x in engine for x in ('LCMPTC one-character machine padding','DOUBLE sqrt/libm rounded constants require independent model/runtime controls','uninitialized OLDTIM tail','other old slots undefined')))
check('all business science Q default None or False and diagnostic EXIT2 are honest Source boundary',all(x in engine for x in ('SOURCE_STATUS = \'UNREADY_SOURCE_ONLY\'','SOURCE_BINDING_SHA256 = None','BOUND_ADAPTER_PIN = None','new_aggregation_qualification_sha256=None','actual_scientific_qualification_sha256=None','raise SystemExit(2 if error is None else 1)')) and 'raise SystemExit(2)' in extract)
check('normal host deliberate childEXIT2 saved failure branch retains all protected sources and no retry',all(x in host for x in ('The complete diagnostic intentionally exits2','failure_post_inputs','full_postclose_input_and_D_E_checked','FAILED_COMPLETE_FINAL_AGGREGATION_NO_RETRY_NO_QUALIFICATION')))


roles={'host_template':'complete_context_aware_aggregation_and_oldXSM_genuine_host.UNREADY.py','engine_template':engine_name,'adapter':'saved_native_data_access_adapter.UNREADY.py','binder':'bind_complete_context_aware_and_oldXSM_SOURCE_only.UNREADY.py','old_XSM_extractor':'complete_observed_old_post_final_XSM_extractor.UNREADY.py','observer_module':'AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90'}
after={
    'original':snapshot(S),'retained':snapshot(T),'old_original':snapshot(OLD),
    'old_retained':snapshot(OLD_SAVED),'old_peer':snapshot(OLD_PEER),'new_source_seal':snapshot(SEAL),
    'Root_retention_record':full_pin(RECORD),'Root_retention_tool':full_pin(TOOL),
}
check('full beforeafter seven ID and complete EOF SHA all new old Source peers Root pins unchanged',before==after)
save('FULL_INPUT_SOURCE_META_INVENTORIES_BEFORE_AFTER.json',dict(source_only=True,before=before,after=after,all_exact=True,no_material_DB_numeric_payload_read=True))
save('COMPLETE_SOURCE_ARCHIVE_STREAM_EOF_AND_SIX_HUNK_INVERSE.json',dict(source_only=True,archives=archive_results,derivations=inverse_results,complete_eleven_original_derivations=original_chain_results,original_native_walker_full_AST_unchanged=True,all_complete_source_preserved=True,old_independent_38_of40_Source_scope_preserved_by_full_byte_inverse=True))
save('FULL_THREE_ROLE_STRICT_REQUIRE_AND_FALSE_KWARG_AUDIT.json',dict(source_only=True,all_strict_require=source_require_audit,five_fixes=fixes,all_dict_FALSE_calls=false_calls,no_candidate_execution=True,no_import_compile_API_guard_numeric_execution=True))
all_true=all(x['passed']is True for x in checks)
review=dict(schema='INDEPENDENT_COMPLETE_CONTEXT_AWARE_ENGINE_HOST_BINDER_SOURCE_REVIEW_V2',status='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'if all_true else 'SOURCE_ONLY_BLOCKED_NO_EXECUTION_OR_SCIENCE',source_only=True,all_checks_passed=all_true,all_checks_typed_true=all_true,check_count=len(checks),checks=checks,blockers=blockers,qualified_source_manifest=before['original']['files']['MANIFEST.json'],retained_source_manifest_pin=before['retained']['files']['MANIFEST.json'],actual_Root_retention_record_pin=before['Root_retention_record'],actual_Root_retention_tool_pin=before['Root_retention_tool'],old_BLOCKED_independent_report_pin=before['old_peer']['files']['REVIEW.json'],complete_original_files=210,complete_retained_files=211,complete_original_declared_members=209,complete_original_and_retained_directories=10,complete_fixed_parent_members=162,complete_six_hunk_inverse=True,unchanged_original_member_count=191,original38_of40_Source_scope_preserved=True,all_five_strictbool_entries_fixed=True,all_three_roles_fully_scanned=True,all7_FALSE_expansion_sites_collision_free=True,actual_independent_candidate_execution=None,new_Q=None,scientific_qualification_created=False,AAA_accuracy_qualified=False,ABA_admitted=False,historical_native_RAM_bits_verified=False,original_native_build_binary_Source_linkage_qualified=False,complete_final_construction_qualified=False,whole_combined_build_or_INPUT_qualified=False,materials_DB_numeric_helper_API_guard_compile_not_executed=True,limits={'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'joint_archive_bytes':2*2**30,'history_bytes':96*2**30,'free_floor_bytes':8*2**30,'threads':1,'children_at_once':1,'retries':0},scope={'isotopes':62,'groups':370,'mixes':8,'extras':18,'moments':3,'prompt_components':32,'fission_index_values':64,'fission_component_mix_values':256,'delayed_pairs':6,'Lambda_values':48,'STATE_values':40,'complete_macro_records':19619},unqualified_components=json.loads(data['COMPLETE_CONTEXT_AWARE_FIELD_PRODUCER_SCOPE_AND_GAPS.json'])['remaining_specific_unqualified_components'],binding_usage='Source-only PASS may support future Root Source admission only against the exact new original manifest and all pinned roles. It does not prove actual context observation, native extraction, Source-to-binary linkage, new full-prefix walker/math/resource/malformed controls, actual aggregation, reaction balance, reference, AAA or ABA. Genuine Root material and bounded execution and independent saved evidence remain required.')
for key,name in roles.items():review[key]=before['original']['files'][name]
save('REVIEW.json',review)
copydir=P/'EXACT_REVIEWED_THREE_ROLE_SOURCE';copydir.mkdir()
for name in changed:
    with (copydir/name).open('xb')as stream:stream.write(data[name])
shutil.copyfile(__file__,P/'review_Source_stdlib_only.py')
save('REQUEST_AND_SCOPE.json',dict(source_only=True,Root_request_manifest_sha256='c8bb4b0738e6dfdf45e81724fcd2644bcf5c9740c5ad8f8ed87de5c003144815',inputs='Complete Source packages, original Source provenance archives and exact smallMETA only',candidate_execution=False,project_writes=False,scope=review['scope'],future_controls_required=review['binding_usage']))
with(P/'REPORT.txt').open('x')as stream:
    stream.write(review['status']+'\nFinite independent full Source/META review. Six entry corrections preserve all original191 other Source members and the full old Source/peer/seal archives. Five exactbool entrances and all three require scanners, all seven FALSE expansions audited. No runtime or scientific qualification.\n')
print(json.dumps(dict(source_only=True,status=review['status'],review_root=str(P),review=full_pin(P/'REVIEW.json'),check_count=len(checks),all_checks_passed=all_true,blockers=blockers,candidate_execution=False,new_Q=None)),flush=True)
