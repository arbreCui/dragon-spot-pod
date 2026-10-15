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

P=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_E_fullpin_same_sort_finite_UNREADY_Source_fix_pb5gkdac')
R=Path(__file__).parent
EXPECTED='5313b65cc109d93816137f8c53e6cdcfbf6d5044310762ac65a20a2f76330593'
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
check('author manifest full EOF SHA and exact size',mp['sha256']==EXPECTED and mp['size_bytes']==54504)
check('full source namespace has 80 members plus manifest and ten directories',len(mf['members'])==80 and len(before['files'])==81 and len(before['directories'])==10)
check('manifest exact complete directory seven-identities',before['directories']==mf['complete_directory_identity'])
check('all source member full EOF SHA size and seven-identities match actual namespace',all(before['files'][x['relative_path']]==x['fullpin']for x in mf['members'])and set(before['files'])=={x['relative_path']for x in mf['members']}|{'MANIFEST.json'})
check('all actual source identities are seven exact integers',all(type(p['identity'])is list and len(p['identity'])==7 and all(type(v)is int for v in p['identity'])for p in before['files'].values()))
metas={str(p.relative_to(P)):json_read(p)for p in P.rglob('*.json')}
check('all forty-four complete Source metadata parsed without duplicate keys or nonfinite JSON',len(metas)==44)
py={str(p.relative_to(P)):p.read_bytes()for p in P.rglob('*.py')}
parsed={f:ast.parse(v)for f,v in py.items()}
check('all twenty-nine complete Python Source AST parsed without import or compile',len(parsed)==29)
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
# Only this reviewer's standard-library AST and byte comparison code executes.
O=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_UNREADY_Source_yxzl8twq')
original_review=metas['ORIGINAL_BLOCKED_INDEPENDENT_SOURCE_REVIEW/REVIEW.json']
check('original independent BLOCKED forty-nine-check report preserved with exact actual bytes',hashlib.sha256((P/'ORIGINAL_BLOCKED_INDEPENDENT_SOURCE_REVIEW/REVIEW.json').read_bytes()).hexdigest()=='c6abb4d1c4a30e20ca1eaf1ee8e54b9e3509a8961872bf8a4b261a031f0f01e4'and original_review['all_checks_passed']is False and len(original_review['blockers'])==4)
fix=metas['COMPLETE_FOUR_CONTRACT_SOURCE_FIX_FULL_BYTE_INVERSE.json'];proof=[];total_hunks=0
for d in fix['source_derivations']:
    source_member=d['source_member'];old=(O/source_member).read_bytes();new=(P/source_member).read_bytes();hs=d['complete_full_inverse_hunks'];total_hunks+=len(hs)
    assert hashlib.sha256(old).hexdigest()==d['original_sha256']and hashlib.sha256(new).hexdigest()==d['fixed_sha256']
    restored=new.decode().splitlines(keepends=True)
    for h in sorted(hs,key=lambda h:h['new_start0'],reverse=True):
        assert restored[h['new_start0']:h['new_end0']]==h['new_full_lines'];restored[h['new_start0']:h['new_end0']]=h['old_full_lines']
    assert ''.join(restored).encode()==old
    olddefs=topdefs(old)if source_member.endswith('.py')else{};newdefs=topdefs(new)if source_member.endswith('.py')else{}
    unchanged=[k for k in olddefs if k in newdefs and olddefs[k]==newdefs[k]]
    changed=[k for k in olddefs if k not in unchanged]
    proof.append(dict(source_member=source_member,original_full_Source_pin=pin(O/source_member),fixed_full_Source_pin=pin(P/source_member),hunks=len(hs),whole_byte_inverse_equal=True,unchanged_complete_definitions=unchanged,changed_complete_definitions=changed))
check('all eight fixed members thirty full hunks invert entire N2 source to the original frozen Source',len(proof)==8 and total_hunks==30)
evidence['all_eight_complete_source_fix_inverse']=proof
einv=metas['PREVIOUS_SEALED_FIX_SOURCE_PROVENANCE/FULL_ROOT_POSTCLOSE_SINGLE_HUNK_NLINK_SOURCE_INVERSE.json'];hs=einv['whole_byte_inverse_hunks'];old=(P/'PREVIOUS_SEALED_FIX_SOURCE_PROVENANCE/PREVIOUS_FULL_ROOT_POSTCLOSE_SOURCE.py').read_bytes();new=(P/'PREVIOUS_SEALED_E_APPEND_FIX_SOURCE_PROVENANCE/PREVIOUS_FULL_ROOT_POSTCLOSE_SOURCE.py').read_bytes();ls=new.decode().splitlines(keepends=True)
for h in reversed(hs):assert ls[h['new_start0']:h['new_end0']]==h['new_full_lines'];ls[h['new_start0']:h['new_end0']]=h['old_full_lines']
check('N2 sole E directory nlink correction full-byte inverse restores previous sealed postclose source',len(hs)==1 and ''.join(ls).encode()==old and hashlib.sha256(old).hexdigest()==einv['original_full_Source_sha256']and hashlib.sha256(new).hexdigest()==einv['corrected_full_Source_sha256'])
evidence['N2_single_nlink_hunk']=einv
fixed_members={d['source_member']for d in fix['source_derivations']}
originalmf=metas['ORIGINAL_BLOCKED_COMPLETE_SOURCE_MANIFEST.json']
original_rows=[x for x in originalmf['members']if x['relative_path']not in fixed_members and x['relative_path']!='AUTHOR_FINITE_COMPLETE_SOURCE_CHECK_UNREADY.json']
check('all original unchanged Source members full bytes preserved rather than selected definitions only',all(pin(P/x['relative_path'])['sha256']==x['fullpin']['sha256']and pin(P/x['relative_path'])['size_bytes']==x['fullpin']['size_bytes']for x in original_rows))
legacy=py['COMPLETE_LEGACY_CONTEXT_HANDOFF_SOURCE/complete_observed_old_post_final_XSM_extractor.UNREADY.py']
check('full original legacy old XSM extractor and all original native walker definitions retained',legacy==Path('/private/tmp/axmat_complete_old_XSM_context_six_blocker_finite_UNREADY_Source_fix_novkasox/complete_observed_old_post_final_XSM_extractor.UNREADY.py').read_bytes()and "native.walk_table(native.root,tuple(prefix),())"in legacy.decode())
# Independently selected from every complete archived Darwin/arm64 GNU Makefile;
# these are literal data comparisons, not evaluation of native Makefile code.
expected_recipes={
 'Ganlib':dict(C='c',CFLAGS=['-Wall','-fPIC'],FLAGS=['-DLinux','-DUnix'],F90='fortran',FFLAGS=['-fPIC','-Wall','-Wno-maybe-uninitialized','-ffpe-summary=none'],FFLAG77=['-fPIC','-Wall','-frecord-marker=4','-ffpe-summary=none'],INCLUDE=[],PREPRO='cpp',FMPI=[],opt=['-O','-g'],COMP=[],LFLAGS=[],lib_module='Ganlib/lib/Darwin_arm64/modules',module_copy=True),
 'Utilib':dict(C='c',CFLAGS=['-Wall','-fPIC'],FLAGS=[],F90='fortran',FFLAGS=['-fPIC','-Wall','-ffpe-summary=none'],FFLAG77=['-fPIC','-Wall','-frecord-marker=4','-ffpe-summary=none'],INCLUDE=[],PREPRO=None,FMPI=[],opt=['-O','-g'],COMP=[],LFLAGS=[],lib_module='Utilib/lib/Darwin_arm64/modules',module_copy=True),
 'Trivac':dict(C=None,CFLAGS=[],FLAGS=[],F90='fortran',FFLAGS=['-fPIC','-ffpe-summary=none'],FFLAG77=['-fPIC','-frecord-marker=4','-ffpe-summary=none'],INCLUDE=['-I../../Ganlib/lib/Darwin_arm64/modules/'],PREPRO=None,FMPI=[],opt=['-O','-g'],COMP=[],LFLAGS=[],lib_module=None,module_copy=False),
 'Dragon':dict(C='c',CFLAGS=['-Wall','-fPIC'],FLAGS=['-DLinux','-DUnix'],F90='fortran',FFLAGS=['-fPIC','-Wall','-ffpe-summary=none'],FFLAG77=['-fPIC','-Wall','-frecord-marker=4','-ffpe-summary=none'],INCLUDE=['-I../../Ganlib/lib/Darwin_arm64/modules/'],PREPRO='cpp',FMPI=[],opt=['-O','-g'],COMP=[],LFLAGS=[],lib_module='Dragon/lib/Darwin_arm64/modules',module_copy=True)}
check('all four complete component recipe dictionaries equal actual archived selected original flags and variables',literal(runtime,'ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES')==expected_recipes)
check('each native compiler and preprocessor argument uses its original component and suffix flags',all(s in runtime for s in ("tools[recipe['PREPRO']]['path']","*recipe['FLAGS']","argv+=recipe['FMPI']","*recipe['CFLAGS']","recipe['FFLAG77']if p.suffix in('.f','.F')else recipe['FFLAGS']","*recipe['INCLUDE']","*recipe['opt']","*recipe['COMP']")))
check('undefined original C or preprocessing tools are refused rather than supplied as invented recipe defaults',"require(recipe['PREPRO']is not None"in runtime and "require(recipe['C']is not None"in runtime)
check('all original source suffix group inputs and complete archive order are retained',"f90=[*sorted(folder.glob('*.f90')),*sorted(folder.glob('*.F90'))]"in runtime and "f77=[*f77_lower,*f77_upper]"in runtime and "objects_order=[p.with_suffix('.o')for p in [*c,*ordered90,*f77]]"in runtime)
check('original component module and library publication paths and final link copies restored',all(s in runtime for s in ("library_dir=native/component/'lib/Darwin_arm64'","modules=native/recipe['lib_module']","if recipe['module_copy']:","component!='Utilib'or bool(generated_modules)","archives[component]=library_copy_pin","*link_recipe['LFLAGS']")))
check('original module and library copy full SHA pins saved and independently rechecked after close',all(s in runtime and s in post for s in ('original_recipe_library_copy_pin','original_recipe_module_copy_pins','original_generated_module_pin','original_recipe_module_copy_pin')))
check('all physical inserted executable lines stay within original fixed/free form compiler limits',all(len(line)<= (132 if f.suffix=='.f90'else 72)for f in(P/'OBSERVATION_SOURCE').glob('*.f*')for line in f.read_text().splitlines()if not(line.startswith('*')or line.lstrip().startswith('!'))))
check('four original full Source blockers are repaired within N2 without changing physics',literal(runtime,'ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES')==expected_recipes and 'Root_complete_postclose_HOCDE_namespace_views=namespace_views'in post)
check('native root prefix and legacy pool prefix now explicit and exact lossless five-to-four field handoff',all(s in runtime and s in post for s in ('legacy_context_source_snapshot_request_rows','legacy_context_root_prefix_semantics','actual_native_snapshot_root_prefix'))and "root_prefix=[],logical_prefix=[]if role=='final-complete-micro'else['MACROLIB']"in runtime)
check('full five namespace directory and every regular file EOF pins are saved before own E append',"namespace_views={key:tree(Path(b['namespaces'][key]))for key in namespace_keys}"in post and "Root_complete_postclose_HOCDE_namespace_views=namespace_views"in post and 'E_view_before_this_manifest_append=True'in post)
check('whole five namespace views are re-read after own E append with H O C D exact unchanged',"after_views={key:tree(Path(b['namespaces'][key]))for key in namespace_keys}"in post and "all(after_views[key]==namespace_views[key]for key in namespace_keys[:-1])"in post)
check('E exact directory set and append parent dev inode mode with other complete seven identities enforced',"set(after_views['receipts']['directories'])==set(namespace_views['receipts']['directories'])"in post and "current[:3]==identity[:3]"in post and "else current==identity"in post)
check('own new E manifest fullpin and own bytes remain counted in original joint history and free caps',all(s in post for s in ('out_pin=fullpin(out)','joint_after=sum','joint_after<2*2**30','resource_after[\'artifact_bytes\']+outside_after<96*2**30','Root_postclose_original_dynamic_history_resource_after=resource_after')))
check('all fourteen author Source roles include full legacy extractor without future fabricated actual pins',len(metas['EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json']['required_author_Source_roles'])==14 and all(mf[k]is None for k in ('actual_peer_review','actual_Root_Source_admission','actual_Root_runtime_terminal','actual_observation_manifest','actual_native_Source_binary_linkage','actual_new_native_controls','actual_new_native_objects_archives_executable')))
same=metas['PREVIOUS_SEALED_E_APPEND_FIX_SOURCE_PROVENANCE/FULL_ROOT_POSTCLOSE_SINGLE_HUNK_SAME_SORT_SOURCE_INVERSE.json'];hs=same['whole_byte_inverse_hunks'];old=(P/'PREVIOUS_SEALED_E_APPEND_FIX_SOURCE_PROVENANCE/PREVIOUS_FULL_ROOT_POSTCLOSE_SOURCE.py').read_bytes();new=(P/'Root_observation_postclose_META_writer.UNREADY.py').read_bytes();ls=new.decode().splitlines(keepends=True)
for h in reversed(hs):assert ls[h['new_start0']:h['new_end0']]==h['new_full_lines'];ls[h['new_start0']:h['new_end0']]=h['old_full_lines']
check('N3 only E fullpin same-sort hunk inverts complete postclose Source to sealed N2',len(hs)==1 and ''.join(ls).encode()==old and hashlib.sha256(old).hexdigest()==same['original_full_Source_sha256']and hashlib.sha256(new).hexdigest()==same['corrected_full_Source_sha256'])
evidence['N3_single_same_sort_hunk']=same
check('postclose E exact gain compares all after and expected complete fullpins with the same string ordering',"sorted(after_views['receipts']['files'],key=lambda p:p['path'])==sorted([*namespace_views['receipts']['files'],out_pin],key=lambda p:p['path'])"in post)
example=['/future_E/a/file.json','/future_E/a-.json','/future_E/own_manifest.json']
check('legal nested E Path and string ordering difference is resolved without dropping fullpin fields',sorted([str(p)for p in sorted(map(Path,example))])==sorted(example))
evidence['stdlib_only_E_file_order_counterexample']=dict(paths=example,tree_Path_component_order=[str(p)for p in sorted(map(Path,example))],normalized_after_and_expected_order=sorted(example),actual_read_only_stdlib_tool_chunk='1938da',candidate_or_filesystem_fixture_executed=False)
blockers=[]
evidence['Root_runtime_terminal_storage_contract']='Postclose requires E == host original freeze and E may gain only this manifest. Actual future Root CLOSED terminal can be stored in H before postclose; then complete H fullpins and joint/history scope count it. Do not append terminal to E before this writer without a separately reviewed exact append contract.'

check('all eighty-one Source files and complete ten directory identities unchanged after independent full review',whole()==before)
receipts=[]
for n,chunk in [('ACTUAL_SOURCE_SEAL_TOOL_RETURN.json','31aab5'),('ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json','80aacf')]:
    p=Path(str(P)+'_seal_receipt')/n;j=json_read(p);t=j['terminal_tool_return'];assert j['closed']is True and j['observed_terminal']is True and j['session_repolled_after_close']is False and j['actual_terminal_chunk']==t['chunk_id']==chunk and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t
    stdout=json.loads(t['output']);assert stdout['sealed_manifest_pin']==mp;receipts.append(dict(fullpin=pin(p),actual_tool_return=j))
check('genuine original author seal and postseal are strict closed int-zero with exact manifest coupling',len(receipts)==2)
evidence['original_author_actual_receipts']=receipts
contract=metas['EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json'];author={k:pin(P/v)for k,v in contract['required_author_Source_roles'].items()}
evidence['withdrawn_initial_prefix_blocker']=dict(original_claim='The legacy root_prefix would locate nonexistent MACROLIB child.',correction='Actual fixed legacy extractor complete_observed_old_post_final_XSM_extractor.UNREADY.py790-792 uses native.walk_table(native.root,tuple(prefix),()); prefix labels pool records logically, does not locate a child. No genuine execution blocker. New explicit native-root/logical-prefix fields and exact legacy row mapping clarify the two contracts.',legacy_extractor_pin=pin(Path('/private/tmp/axmat_complete_old_XSM_context_six_blocker_finite_UNREADY_Source_fix_novkasox/complete_observed_old_post_final_XSM_extractor.UNREADY.py')))
report=dict(schema=contract['required_review_schema'],status=('SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'if not blockers else 'SOURCE_ONLY_BLOCKED_POSTCLOSE_E_ORDER_COMPARISON_NO_EXECUTION_OR_SCIENCE'),source_only=True,all_checks_passed=(not blockers),all_checks_typed_true=all(c['passed']for c in checks),check_count=len(checks),checks=checks,blockers=blockers,actual_author_Source_contract=author,evidence=evidence,complete_reviewed_source_manifest_pin=mp,complete_reviewed_source_namespace_before=before,complete_reviewed_source_namespace_after=whole(),helper_candidate_guard_API_native_material_compile_or_numeric_executed=False,actual_runtime_qualification_sha256=None,actual_observer_native_controls_run=None,actual_native_Source_binary_linkage_qualification_sha256=None,actual_scientific_qualification_sha256=None,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,native_transport_executed=False,complete_context_aggregation_qualified=False,unverified_actual_scope=['All new Source controls/build/observer/native walker/context extraction not executed here.','Real Source-to-object-to-archive-to-link-to-executable chain and Root genuine caps require actual future execution.','Original OwnRSS monitors direct command child; compiler descendants RSS is explicitly unqualified.','No original material/archive/numeric/SQLite payload read here; original129 actual input pins are retained contract only.','LCMEQU general copy Source skips zero-length named records; no original in-memory zero-length absence at new historical observation points is proven by this Source review.','No old-context aggregation or physical/scientific PASS; AAA remains7/8 and ABA unstarted.'])
(R/'REVIEW.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(R/'REPORT.txt').write_text(report['status']+'\nComplete native1365/physics14/host12 Source retained; four old fixes fully reviewed; actual run/native/science remain unqualified. See REVIEW.json.\n')
for f in ('MANIFEST.json','COMPLETE_FOUR_ORIGINAL_PHYSICAL_ROUTINE_OBSERVER_INSERT_ONLY_INVERSE.json','COMPLETE_ORIGINAL_NATIVE_HOST_TO_OBSERVATION_HOST_FULL_INVERSE.json','EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json','complete_observation_BUILD5_AB_runtime.UNREADY.py','complete_observation_genuine_host.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py','Root_observation_postclose_META_writer.UNREADY.py','Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py'):
    dest=R/'REVIEWED_SOURCE'/f;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/f,dest)
(R/'ORIGINAL_COMPILER_RECIPES_AND_NATIVE_SNAPSHOT_COPY.Source.txt').write_bytes(b'\n'.join((b'SOURCE '+(c+'/src/Makefile').encode()+b'\n'+native[c+'/src/Makefile'])for c in ('Ganlib','Utilib','Trivac','Dragon'))+b'\nGanlib/src/lcm_c.c full snapshot-copy relevant original Source\n'+b''.join(native['Ganlib/src/lcm_c.c'].splitlines(keepends=True)[2423:2537]))
print(json.dumps(dict(status=report['status'],source_only=True,review_pin=pin(R/'REVIEW.json'),check_count=len(checks),passed_checks=sum(c['passed']for c in checks),failed_checks=sum(not c['passed']for c in checks),blocker_count=len(blockers),complete_original_native_Source_archive_members=1365,actual_candidate_compile_native_or_numeric_execution=False),allow_nan=False))
