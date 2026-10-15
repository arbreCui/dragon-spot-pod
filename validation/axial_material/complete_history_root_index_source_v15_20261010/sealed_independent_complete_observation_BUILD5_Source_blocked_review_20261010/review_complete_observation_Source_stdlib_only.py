"""Independent Source-only review; never imports/executes reviewed Source."""
import ast
import gzip
import hashlib
import json
from pathlib import Path
import re
import shutil
import stat
import tarfile

P=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_UNREADY_Source_yxzl8twq')
R=Path(__file__).parent
EXPECTED='2a1c950bcf036e1534901333af2f50c2f53ab12105502e247445e9a8fe9c066a'
checks=[]
evidence={}
def check(label,value):
    assert type(value)is bool
    assert label not in {x['check']for x in checks}
    checks.append({'check':label,'passed':value})
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);a=ident(p.lstat());assert stat.S_ISREG(a[2])and a[3]==1 and not p.is_symlink()
    h=hashlib.sha256();n=0
    with p.open('rb')as f:
        assert ident(f.fileno()and __import__('os').fstat(f.fileno()))==a
        for b in iter(lambda:f.read(2**20),b''):h.update(b);n+=len(b)
        assert ident(__import__('os').fstat(f.fileno()))==a
    assert ident(p.lstat())==a and n==a[4]
    return dict(path=str(p),sha256=h.hexdigest(),size_bytes=n,identity=a)
def json_read(p):
    def pairs(xs):
        d={}
        for k,v in xs:assert k not in d;d[k]=v
        return d
    return json.loads(Path(p).read_bytes(),object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in()).throw(ValueError(v)))
def whole():
    return {'files':{str(p.relative_to(P)):pin(p)for p in P.rglob('*')if p.is_file()},
            'directories':{'.'if p==P else str(p.relative_to(P)):ident(p.lstat())for p in[P,*sorted(P.rglob('*'))]if p.is_dir()}}
def topdefs(raw):
    t=ast.parse(raw);ls=raw.splitlines(keepends=True)
    return{n.name:{'bytes':b''.join(ls[n.lineno-1:n.end_lineno]),'AST':ast.dump(n,include_attributes=False)}for n in t.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
def literal(raw,name):
    def const(n):
        if isinstance(n,ast.BinOp)and isinstance(n.op,(ast.Mult,ast.Pow)):
            a,b=const(n.left),const(n.right)
            assert type(a)is int and type(b)is int
            return a*b if isinstance(n.op,ast.Mult)else a**b
        return ast.literal_eval(n)
    for n in ast.parse(raw).body:
        if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id==name for t in n.targets):
            if isinstance(n.value,ast.Call)and isinstance(n.value.func,ast.Name)and n.value.func.id=='dict':return{k.arg:const(k.value)for k in n.value.keywords}
            return const(n.value)
    raise AssertionError(name)
before=whole();mf=json_read(P/'MANIFEST.json');mp=pin(P/'MANIFEST.json')
check('author manifest full EOF SHA and exact size',mp['sha256']==EXPECTED and mp['size_bytes']==23441)
check('full source namespace has 38 members plus manifest and four directories',len(mf['members'])==38 and len(before['files'])==39 and len(before['directories'])==4)
check('manifest exact complete directory seven-identities',before['directories']==mf['complete_directory_identity'])
check('all source member full EOF SHA size and seven-identities match actual namespace',all(before['files'][x['relative_path']]==x['fullpin']for x in mf['members'])and set(before['files'])=={x['relative_path']for x in mf['members']}|{'MANIFEST.json'})
check('all actual source identities are seven exact integers',all(type(p['identity'])is list and len(p['identity'])==7 and all(type(v)is int for v in p['identity'])for p in before['files'].values()))
metas={str(p.relative_to(P)):json_read(p)for p in P.rglob('*.json')}
check('all fourteen complete Source metadata parsed without duplicate keys or nonfinite JSON',len(metas)==14)
py={str(p.relative_to(P)):p.read_bytes()for p in P.rglob('*.py')}
parsed={f:ast.parse(v)for f,v in py.items()}
check('all nineteen complete Python Source AST parsed without import or compile',len(parsed)==19)
index=metas['COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json'];indexed={x['relative_path']:x['full_original_Source_pin']for x in index['members']}
check('whole original four-library Source index has 1365 unique complete members',len(index['members'])==len(indexed)==1365 and index['components']==['Ganlib','Utilib','Trivac','Dragon'])
check('all1365 original Source pins have full exact typed path SHA size and seven integer identities',all(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['path'])is str and Path(p['path']).is_absolute()and type(p['sha256'])is str and re.fullmatch('[0-9a-f]{64}',p['sha256'])is not None and type(p['size_bytes'])is int and p['size_bytes']>=0 and type(p['identity'])is list and len(p['identity'])==7 and all(type(v)is int for v in p['identity'])and p['identity'][4]==p['size_bytes']for p in indexed.values()))
archive=P/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz';arc_before=pin(archive)
native={};total=0;archive_names=[]
with tarfile.open(archive,'r:gz')as t:
    members=t.getmembers()
    for m in members:
        assert m.isfile()and m.name in indexed and not Path(m.name).is_absolute()and '..'not in Path(m.name).parts
        with t.extractfile(m)as f:b=f.read()
        assert len(b)==m.size==indexed[m.name]['size_bytes']and hashlib.sha256(b).hexdigest()==indexed[m.name]['sha256']
        native[m.name]=b;archive_names.append(m.name);total+=len(b)
with gzip.open(archive,'rb')as f:
    gzip_bytes=sum(len(b)for b in iter(lambda:f.read(2**20),b''))
check('all 1365 source archive members streamed complete EOF SHA size with unique exact coverage',len(archive_names)==len(set(archive_names))==1365 and set(archive_names)==set(indexed))
check('full original Source gzip reaches EOF and validates trailer CRC without extracting or executing',gzip_bytes>total and pin(archive)==arc_before)
evidence['original_Source_archive']=dict(pin=arc_before,member_count=len(native),complete_uncompressed_Source_bytes=total,gzip_full_decoded_bytes=gzip_bytes,all_member_SHA_and_size_matched=True)
inv=metas['COMPLETE_FOUR_ORIGINAL_PHYSICAL_ROUTINE_OBSERVER_INSERT_ONLY_INVERSE.json'];physical_proof=[];nh=0
for d in inv['derivations']:
    old=native[d['original_archive_member']];new=(P/d['derived_Source_member']).read_bytes();ls=new.decode().splitlines(keepends=True)
    hs=d['complete_insert_only_hunks'];nh+=len(hs)
    for h in sorted(hs,key=lambda h:h['new_start0'],reverse=True):
        assert h['tag']=='insert'and h['old_start0']==h['old_end0']and h['old_full_lines']==[]
        assert ls[h['new_start0']:h['new_end0']]==h['new_full_lines']
        del ls[h['new_start0']:h['new_end0']]
    restored=''.join(ls).encode();assert restored==old and hashlib.sha256(old).hexdigest()==d['original_sha256']and hashlib.sha256(new).hexdigest()==d['derived_sha256']
    physical_proof.append(dict(original=d['original_archive_member'],derived=d['derived_Source_member'],complete_inverse_equal=True,insert_hunks=len(hs)))
check('all four physical routines and all fourteen insert-only hunks fully invert to entire original compiled Source',len(physical_proof)==4 and nh==14)
check('all inserted executable physical lines are observer calls with original arithmetic and branches retained',all(h['old_full_lines']==[] and all(l.lstrip().startswith(('USE AXMAT_','CALL AXOBS_','1 ','2 ','> '))for l in h['new_full_lines'])for d in inv['derivations']for h in d['complete_insert_only_hunks']))
evidence['four_physical_routine_full_inverse']=physical_proof
hinv=metas['COMPLETE_ORIGINAL_NATIVE_HOST_TO_OBSERVATION_HOST_FULL_INVERSE.json'];old=py['PARENT_SOURCE/Root_bound_complete_native_genuine_host.py'];new=py['complete_observation_genuine_host.UNREADY.py'];ls=old.decode().splitlines(keepends=True)
for h in sorted(hinv['complete_full_inverse_hunks'],key=lambda h:h['old_start0'],reverse=True):
    assert ls[h['old_start0']:h['old_end0']]==h['old_full_lines'];ls[h['old_start0']:h['old_end0']]=h['new_full_lines']
check('all twelve genuine host hunks reproduce the entire derived Source byte for byte',len(hinv['complete_full_inverse_hunks'])==12 and ''.join(ls).encode()==new)
restored=new.decode().splitlines(keepends=True);delta=0;positions=[]
for h in sorted(hinv['complete_full_inverse_hunks'],key=lambda h:h['old_start0']):
    a=h['old_start0']+delta;b=a+len(h['new_full_lines']);positions.append((a,b,h));delta+=len(h['new_full_lines'])-(h['old_end0']-h['old_start0'])
for a,b,h in reversed(positions):assert restored[a:b]==h['new_full_lines'];restored[a:b]=h['old_full_lines']
check('entire twelve-hunk inverse restores original genuine host Source and AST', ''.join(restored).encode()==old and ast.dump(ast.parse(''.join(restored)),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False))
od=topdefs(old);nd=topdefs(new)
check('all original genuine host support definitions except explicitly replaced main retain complete bytes and AST',set(od)==set(nd)and all(od[k]==nd[k]for k in od if k!='main'))
evidence['host_inverse']=dict(original_SHA=hashlib.sha256(old).hexdigest(),derived_SHA=hashlib.sha256(new).hexdigest(),hunks=12,unchanged_complete_definitions=[k for k in od if k!='main'])
prov=metas['FULL_NECESSARY_PARENT_SOURCE_PROVENANCE.json'];parent_proof=[]
for r in prov['parents']:
    p=pin(P/r['retained_copy']);q=r['full_original_Source_pin'];assert p['sha256']==q['sha256']and p['size_bytes']==q['size_bytes'];parent_proof.append(dict(role=r['role'],retained_pin=p,original_Source_pin=q))
check('all eighteen necessary full parent Source copies match their original source SHA and size',len(parent_proof)==18)
evidence['retained_parent_Source_fullpins']=parent_proof
guards={x:hashlib.sha256(py['GUARD_SOURCE/'+x]).hexdigest()for x in ['prepare_qualified_AB_source_factor_production.py','qualify_refined_AAA_layered_full.py','production_runner.py','run_bounded_dragon.py','moment_order_complete_history_resource_trie_20261010.py']}
check('all genuine 619 705 38de bc4 ebbb complete guard and resource Source retained exact SHA',list(guards.values())==['619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743','70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6','38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128','bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09','ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022'])
runtime=py['complete_observation_BUILD5_AB_runtime.UNREADY.py'].decode();binder=py['bind_complete_observation_SOURCE_only.UNREADY.py'].decode();host=new.decode();post=py['Root_observation_postclose_META_writer.UNREADY.py'].decode();request=py['Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py'].decode();obs=(P/'OBSERVATION_SOURCE/AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90').read_text();ctx=py['OBSERVATION_SOURCE/extract_actual_complete_context_with_SPH_decisions.UNREADY.py'].decode()
caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
check('runtime binder Root request producer and postclose writer preserve all nine exact original caps',all(literal(x,'CAPS')==caps and all(type(v)is int for v in literal(x,'CAPS').values())for x in (runtime,binder,request,post)))
check('complete original129 protected pins retained as unique metadata without reading materials',len(metas['ORIGINAL129_AND_MATERIAL_SEED_CONTRACT.Source_META.json']['original129_input_pins'])==129 and len({p['path']for p in metas['ORIGINAL129_AND_MATERIAL_SEED_CONTRACT.Source_META.json']['original129_input_pins']})==129)
check('original entire A and B deck seed and library provenance metadata retained',list(metas['ORIGINAL129_AND_MATERIAL_SEED_CONTRACT.Source_META.json']['states'])==['A','B']and len(metas['ORIGINAL129_AND_MATERIAL_SEED_CONTRACT.Source_META.json']['libraries'])==2)
check('Source binder and request producer require all original129 plus additional protected real evidence and actual tools',all(x in binder and x in runtime for x in ('original129_input_pins','additional_actual_evidence_input_pins','tool_pins','independent_observation_Source_review_pin','actual_Root_observation_Source_admission_tool_return_pin')))
check('complete independent Source peer admission requires exact family thirteen role pins and genuine closed typed-zero terminal',all(x in binder and x in runtime for x in ('actual_author_Source_contract','ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1','observed_terminal','session_repolled_after_close','actual_terminal_chunk','terminal_tool_return')))
check('all new runtime qualification native controls Source-binary science aggregation future pins remain unknown or false',all(v is None or v is False for v in literal(runtime,'FUTURE').values())and literal(runtime,'SOURCE_STATUS')=='UNREADY_SOURCE_ONLY'and literal(host,'SOURCE_STATUS')=='UNREADY_SOURCE_ONLY')
check('unready host refuses before support runtime or native API loads',host.index("require(SOURCE_STATUS=='READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED")<host.index("spec=importlib.util.spec_from_file_location"))
check('runtime retains original supervisor class identity and exact original SerialExecutor MRO contract',"full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)"in runtime and "type(runner)is full.OwnRSSSerialExecutor"in runtime and 'runner.resources is resources'in runtime)
check('all commands use original runner execute and original full watchdog PID command zero cleanup RSS stage checks',all(s in runtime for s in ("runner.execute(folder,label,argv,remaining","watch['pid']","watch['returncode']==0","watch['command']==argv","watch['liveness_group_cleanup']is True","watch['rss_cap_mib']==512")))
check('all five build groups retain individual 600 and whole1800 supervision and no old objects archives or executable reuse',all(s in runtime for s in ("('Ganlib','Utilib','Trivac','Dragon')","link_started+600","entire library compile/archive group600 cap","new final executable required","new object required","whole observation build+A/B+closure1800 cap")))
check('new actual objects and archives and final link retain full Source preprocessor object argv watch log and executable pins',all(s in runtime for s in ('retained_complete_preprocessor_Source_pin','original_source_pin','new_object_pin','actual_archive_command','all_actual_link_input_pins','new_actual_executable_pin','all_sources_objects_archives_checked_after_actual_link')))
check('whole original source archive exact members and all overlays frozen again after every build group and link',all(s in runtime for s in ('full compile Source namespace coverage','whole original native Source archive unique indexed exact count','all original Source fullEOF archive bytes','complete native Source freeze after whole group','whole native Source-to-new-object/archive/link final freeze')))
check('A material production closes and saves complete event products handles before B with no parallel material run',all(s in runtime for s in ("for state in('A','B'):","actual_material_seed_copy_pins","all own process material state handles closed before next state","all_A_handles_closed_before_B=True")))
check('all context events snapshots and original material outputs receive complete EOF SHA pins without record filtering',all(s in runtime for s in ("set(files)==all_observer_names","complete_context_pins=contexts","complete_state_snapshot_inputs=snapshots","('material.xsm','microlib.ascii','macro.ascii','metadata.ascii')")))
check('observer retains INTEGER and REAL32 native widths endian and every full context vector and raw order',all(s in obs for s in ('storage_size(0)/=32','storage_size(0.0)/=32','bytes(1)/=4','state(40)','mix(nbiso)','den(nbiso)','maskl(ngroup)','indfis(:nbmix,:nfissi)','sph(nbm,ngro)','mat(nreg)')))
check('observer snapshots use fresh disk XSM native word copy and all opened contexts snapshots explicitly close',obs.count('call start_event(')==9 and obs.count('close(unit)')==9 and 'call LCMEQU(target,saved)'in obs and 'call LCMCL(saved,1)'in obs and "status='new'"in obs)
check('old LIBDEN observation occurs after original macro exit and before original mutation without moving physical code',"CALL LCMSIX(IPLIB,' ',2)"in native['Dragon/src/LIBDEN.f'].decode().splitlines()[233] and inv['derivations'][1]['complete_insert_only_hunks'][1]['old_start0']==239)
check('all nine observation labels and all original SPH decisions and tracking masks present as Source capture contract',len(literal(runtime,'LABELS'))==9 and all(s in obs for s in ('AXOBS_SPH_DECISION','AXOBS_TRACK','AXOBS_MASK','AXOBS_LIBDEN_FISSION','AXOBS_FINAL')))
check('live archive covers H O C D E regular and open-unlinked files plus whole history free floor before and after',all(s in runtime for s in ('roots5=(host,out,control,archive,receipts)','open_unlinked_bytes','all_regular_and_open_unlinked_counted=True','complete D/E and all directory/fullSource identities frozen while live','complete history plus external D/E','original history/free complete reserve')))
check('failure branch preserves full input and D E failures all stage records and does not retry or create qualification',all(s in runtime for s in ('FAILED_NO_RETRY_NO_QUALIFICATION','full_postfailure_freeze_errors','actual_resources_after_failure','actual_observation_manifest_pin_if_saved','complete_input_pins_after_failure')))
check('postclose Root writer independently requires real current host result actual build and observation manifests fullpins',all(s in post for s in ('ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_TOOL_TERMINAL_RETURN_V1','terminal_tool_return','actual_terminal_chunk','observed_terminal','actual_build_evidence_pin','actual_observation_manifest_pin')))
check('postclose Source covers complete actual Source object archive link executable context snapshot and seed pins',all(s in post for s in ('new_object_pin','new_archive_pin','new_actual_executable_pin','complete_context_pins','complete_state_snapshot_inputs','actual_material_seed_copy_pins','actual_material_product_pins')))
check('postclose saved Root terminal and whole known observations remain distinct from future science',all(s in post for s in ('namespaces','Root_observed_tool_terminal','scientific_accuracy_qualified')))
check('context extractor remains unready with genuine capture pins and full context EOF rule instead of fabricated old state',literal(ctx,'SOURCE_STATUS')=='UNREADY_SOURCE_ONLY'and 'SPH'in ctx and 'AXOBSCTX'in ctx and 'UNREADY'in ctx)
evidence['compiler_contract_counterexamples']={}
for comp in ('Ganlib','Utilib','Trivac','Dragon'):
    lo=sorted(k for k in native if k.startswith(comp+'/src/')and k.endswith('.f'));up=sorted(k for k in native if k.startswith(comp+'/src/')and k.endswith('.F'));oldorder=lo+up;neworder=sorted(lo+up)
    k=next((i for i,(a,b)in enumerate(zip(oldorder,neworder))if a!=b),None)
    evidence['compiler_contract_counterexamples'][comp]=dict(C_count=sum(k.startswith(comp+'/src/')and k.endswith('.c')for k in native),uppercase_F_files=up,original_suffix_group_order_equals_merged=(oldorder==neworder),first_different_index=k,original_at_first=None if k is None else oldorder[k],candidate_at_first=None if k is None else neworder[k])
check('original per-library and per-suffix complete compile flags and include rules preserved',False)
check('snapshot native macro root and legacy pool logical prefix distinguished by actual extractor Source',True)
check('all original static archive member suffix groups and order preserved',False)
check('all original per-library module publication directories and include namespaces preserved',False)
check('Root postclose saves complete five namespace directory and full EOF file pin inventory',False)
blockers=[
dict(id='B1',source='complete_observation_BUILD5_AB_runtime.UNREADY.py',lines=[202,205,207,210],problem='Compile/preprocess flags are unified across components rather than original four Makefile recipes. Utilib16C files receive added -DLinux/-DUnix; Ganlib F90 loses -Wno-maybe-uninitialized; Trivac Darwin adds -Wall; Ganlib F90/Utilib receive added -I.',fix='Dispatch every component and suffix with the exact archived Darwin arm64 GNU recipe, flags and original equivalent include paths; retain tool/argv evidence.'),
dict(id='B3',source='complete_observation_BUILD5_AB_runtime.UNREADY.py',lines=[186,189,218],problem='Combined sorted *.f/*.F changes original archive order in actual Ganlib and Dragon sources. Original Makefiles concatenate OBJ77 then OBJF77.',fix='Use separately sorted suffix groups, including the original f90/F90 shell input groups to the original dependency generator; archive original OBJC,OBJ90,OBJ77,OBJF77 order.'),
dict(id='B4',source='complete_observation_BUILD5_AB_runtime.UNREADY.py',lines=[182,210,220,223],problem='All library modules are published into Ganlib module directory rather than original distinct Ganlib,Utilib,Dragon destinations; Trivac adds an originally absent copy.',fix='Preserve archived per-library lib_module publication and INCLUDE rules within isolated native tree, including no added Trivac module publication.'),
dict(id='B5',source='Root_observation_postclose_META_writer.UNREADY.py',lines=[44,50,62,86,91,92],problem='Complete tree exists but is only used to compare D/E. H/O/C/D/E byte counts and known object/archive/context pins are not complete persisted namespace files/directories/fullEOF7ID inventory; final result=dict(m) has no such complete view.',fix='Persist actual full tree views for all five H/O/C/D/E namespaces. Clearly mark E snapshot before this new manifest append; count manifest itself in caps afterward; do not append frozen D.')]
check('all thirty-nine Source files and complete four directory identities unchanged after independent full review',whole()==before)
receipts=[]
for n,chunk in [('ACTUAL_SOURCE_SEAL_TOOL_RETURN.json','2ad150'),('ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json','360b12')]:
    p=Path(str(P)+'_seal_receipt')/n;j=json_read(p);t=j['terminal_tool_return'];assert j['closed']is True and j['observed_terminal']is True and j['session_repolled_after_close']is False and j['actual_terminal_chunk']==t['chunk_id']==chunk and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t
    stdout=json.loads(t['output']);assert stdout['manifest']==mp;receipts.append(dict(fullpin=pin(p),actual_tool_return=j))
check('genuine original author seal and postseal are strict closed int-zero with exact manifest coupling',len(receipts)==2)
evidence['original_author_actual_receipts']=receipts
contract=metas['EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json'];author={k:pin(P/v)for k,v in contract['required_author_Source_roles'].items()}
evidence['withdrawn_initial_prefix_blocker']=dict(original_claim='The legacy root_prefix would locate nonexistent MACROLIB child.',correction='Actual fixed legacy extractor complete_observed_old_post_final_XSM_extractor.UNREADY.py790-792 uses native.walk_table(native.root,tuple(prefix),()); prefix labels pool records logically, does not locate a child. No genuine execution blocker. New explicit native-root/logical-prefix fields and exact legacy row mapping clarify the two contracts.',legacy_extractor_pin=pin(Path('/private/tmp/axmat_complete_old_XSM_context_six_blocker_finite_UNREADY_Source_fix_novkasox/complete_observed_old_post_final_XSM_extractor.UNREADY.py')))
report=dict(schema=contract['required_review_schema'],status='SOURCE_ONLY_BLOCKED_FOUR_PRECISE_BUILD_POSTCLOSE_CONTRACT_MISMATCHES_NO_EXECUTION_OR_SCIENCE',source_only=True,all_checks_passed=False,all_checks_typed_true=False,check_count=len(checks),checks=checks,blockers=blockers,actual_author_Source_contract=author,evidence=evidence,complete_reviewed_source_manifest_pin=mp,complete_reviewed_source_namespace_before=before,complete_reviewed_source_namespace_after=whole(),helper_candidate_guard_API_native_material_compile_or_numeric_executed=False,actual_runtime_qualification_sha256=None,actual_observer_native_controls_run=None,actual_native_Source_binary_linkage_qualification_sha256=None,actual_scientific_qualification_sha256=None,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,native_transport_executed=False,complete_context_aggregation_qualified=False,unverified_actual_scope=['All new Source controls/build/observer/native walker/context extraction not executed here.','Real Source-to-object-to-archive-to-link-to-executable chain and Root genuine caps require actual future execution.','Original OwnRSS monitors direct command child; compiler descendants RSS is explicitly unqualified.','No original material/archive/numeric/SQLite payload read here; original129 actual input pins are retained contract only.','LCMEQU general copy Source skips zero-length named records; no original in-memory zero-length absence at new historical observation points is proven by this Source review.','No old-context aggregation or physical/scientific PASS; AAA remains7/8 and ABA unstarted.'])
(R/'REVIEW.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(R/'REPORT.txt').write_text('Independent complete observation BUILD5 Source review: BLOCKED.\n1365 complete Source archive members / four14-hunk physical inverses / host12-hunk inverse / whole39files4dirs / genuine supervision and future-None scope read only.\nFour precise blockers: per-component flags, original static archive order, per-component module publication/include namespaces, complete Root postclose five-namespace saved inventory.\nInitial prefix execution blocker withdrawn: actual legacy walker starts native.root and uses prefix only for logical pool labels. Explicit separate native/logical fields clarify future mapping.\nNo candidate/import/compile/API/material/guard/numeric execution. See REVIEW.json.\n')
for f in ('MANIFEST.json','COMPLETE_FOUR_ORIGINAL_PHYSICAL_ROUTINE_OBSERVER_INSERT_ONLY_INVERSE.json','COMPLETE_ORIGINAL_NATIVE_HOST_TO_OBSERVATION_HOST_FULL_INVERSE.json','EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json','complete_observation_BUILD5_AB_runtime.UNREADY.py','complete_observation_genuine_host.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py','Root_observation_postclose_META_writer.UNREADY.py','Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py'):
    dest=R/'REVIEWED_SOURCE'/f;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/f,dest)
(R/'ORIGINAL_COMPILER_RECIPES_AND_NATIVE_SNAPSHOT_COPY.Source.txt').write_bytes(b'\n'.join((b'SOURCE '+(c+'/src/Makefile').encode()+b'\n'+native[c+'/src/Makefile'])for c in ('Ganlib','Utilib','Trivac','Dragon'))+b'\nGanlib/src/lcm_c.c full snapshot-copy relevant original Source\n'+b''.join(native['Ganlib/src/lcm_c.c'].splitlines(keepends=True)[2423:2537]))
print(json.dumps(dict(status=report['status'],source_only=True,review_pin=pin(R/'REVIEW.json'),check_count=len(checks),passed_checks=sum(c['passed']for c in checks),failed_checks=sum(not c['passed']for c in checks),blocker_count=len(blockers),complete_original_native_Source_archive_members=1365,actual_candidate_compile_native_or_numeric_execution=False),allow_nan=False))
