"""Finite SOURCE text/AST/hash builder. Never imports or executes reviewed files."""
import ast
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import stat

HERE=Path(__file__).absolute().parent
OLD=Path('/private/tmp/axmat_current150_AB_rawrecord_wrapper_UNREADY_SOURCE_20261010_angular_v3q9')
PEER=Path('/private/tmp/axmat_full_rawrecord_SOURCE_peer_20261010_4gZZp5')
PARENT_HOST=Path('/private/tmp/axmat_v21_COMPLETE_READY_runtime_genuine_PREP_closed_metadata_SOURCE_20261010_syx41/sealed_READY_runtime_and_PREP_binding/BOUND_READY_SOURCE/combined_prepare_host.py')
ROOT=Path('/Users/wen/spot')
BASE=ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010'
SOURCES={
 'original_normal_PREP_host_776b.SOURCE.py':(PARENT_HOST,'776bf8300f5c5a55c9e9f4929760b0db10b5f6d2392ea0971483364d19365405'),
 'original_normal_support_3c185.SOURCE.py':(BASE/'actual_prepare_sources/prepare_cli_host_v15.py','3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'),
 'original_genuine_helper_619.SOURCE.py':(ROOT/'validation/axial_material/prepare_qualified_AB_source_factor_production.py','619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'),
 'original_genuine_ownRSS_705.SOURCE.py':(ROOT/'validation/axial_material/qualify_refined_AAA_layered_full.py','70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'),
 'original_genuine_production_38de.SOURCE.py':(ROOT/'validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py','38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128'),
 'original_genuine_bounded_bc4.SOURCE.py':(ROOT/'validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/run_bounded_dragon.py','bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09'),
 'original_genuine_resource_ebbb.SOURCE.py':(ROOT/'validation/axial_material/moment_order_complete_history_resource_trie_20261010.py','ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022'),
 'material_audit.SOURCE.py':(ROOT/'validation/axial_material/material_audit.py',None),
 'material_inputs.SOURCE.py':(ROOT/'validation/axial_material/material_inputs.py',None),
}
CAP_EXPR="{'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'joint_archive_bytes':2*2**30,'history_bytes':96*2**30,'free_floor_bytes':8*2**30,'threads':1,'children_at_once':1,'retries':0}"
checks=[]

def check(name,value,detail=None):
    if type(value)is not bool or not value:raise ValueError('SOURCE check failed: '+name)
    row={'name':name,'pass':True}
    if detail is not None:row['detail']=detail
    checks.append(row)

def pin(path):
    s=path.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    check('ordinary SOURCE fullEOF '+str(path),stat.S_ISREG(s.st_mode)and s.st_nlink==1 and not path.is_symlink())
    with path.open('rb')as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
    t=path.lstat();after=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
    check('unchanged SOURCE full7ID '+str(path),before==after)
    return {'path':str(path),'sha256':sha,'size_bytes':s.st_size,'identity':before}

def write(path,value):
    raw=(json.dumps(value,allow_nan=False,ensure_ascii=True,indent=2)+'\n').encode()
    if path.exists():check('existing partial SOURCE output remains byteexact '+path.name,path.read_bytes()==raw)
    else:
        with path.open('xb')as f:f.write(raw)

def copy_exact(origin,dest):
    if dest.exists():check('existing partial SOURCE copy unchanged '+str(dest),dest.read_bytes()==origin.read_bytes())
    else:shutil.copyfile(origin,dest)

def globals_(tree):
    result={}
    for n in tree.body:
        if isinstance(n,ast.Assign):
            for t in n.targets:
                if isinstance(t,ast.Name):result[t.id]=n.value
    return result

def calls(tree):
    return [ast.unparse(n.func)for n in ast.walk(tree)if isinstance(n,ast.Call)]

def main():
    check('unsealed fresh owned SOURCE namespace only',not(HERE/'sealed_SOURCE_manifest.json').exists())
    old_manifest=pin(OLD/'sealed_SOURCE_manifest.json');check('actual old sealed full wrapper manifest',old_manifest['sha256']=='f862d822da445bb7674e246c985dc1c8e4caed1f5fcc68e7ace4e791a955d97c')
    old=json.loads((OLD/'sealed_SOURCE_manifest.json').read_text())
    check('complete old source count13plusmanifest',len(old['files'])==old['members_excluding_manifest']==13)
    original=HERE/'ORIGINAL_UNREADY_PACKAGE';original.mkdir(exist_ok=True)
    old_pins=[]
    for name,row in old['files'].items():
        current=pin(OLD/name);check('all original wrapper Source sealed actual identity '+name,current==row);old_pins.append(current)
        copy_exact(OLD/name,original/name);check('full old Source byteexact copy '+name,pin(original/name)['sha256']==row['sha256'])
    copy_exact(OLD/'sealed_SOURCE_manifest.json',original/'sealed_SOURCE_manifest.json')
    check('original old Source tree14 completely copied',len(list(original.iterdir()))==14)
    peer_manifest=pin(PEER/'SOURCE_PEER_SEAL.json');check('actual sealed independent378Sourcepeer',peer_manifest['sha256']=='8058f908bbc8d6e3eae8b997d9a7707640cddfc610c3c508621f8cb232e51b35')
    peer=json.loads((PEER/'SOURCE_PEER_SEAL.json').read_text());review=json.loads((PEER/'SOURCE_PEER_REVIEW.json').read_text())
    check('actual full prior378checks/no hard blocker',len(review['all_checks'])==378 and all(row['value']is True for row in review['all_checks'])and review['source_blockers_for_full_raw_transfer']==[])
    peer_dest=HERE/'ORIGINAL_SOURCE_PEER';peer_dest.mkdir(exist_ok=True)
    for name,row in peer['files'].items():
        current=pin(PEER/name);check('all old peer Source pinned '+name,current==row);copy_exact(PEER/name,peer_dest/name)
    copy_exact(PEER/'SOURCE_PEER_SEAL.json',peer_dest/'SOURCE_PEER_SEAL.json')
    check('full prior peer4copy',len(list(peer_dest.iterdir()))==4)
    origins=HERE/'ORIGINAL_GENUINE_AND_MATERIAL_SOURCE';origins.mkdir(exist_ok=True);source_origins={}
    for name,(path,sha)in SOURCES.items():
        current=pin(path);check('known genuineSource SHA '+name,sha is None or current['sha256']==sha);ast.parse(path.read_text())
        copy_exact(path,origins/name);check('full genuine/material Source byteexact '+name,pin(origins/name)['sha256']==current['sha256']);source_origins[name]=current
    wrapper_path=original/'transfer_full_AB_rawrecord_UNREADY.py';wrapper=wrapper_path.read_text();w=ast.parse(wrapper);wg=globals_(w)
    check('wrapper full body unchanged098b2',pin(wrapper_path)['sha256']=='098b2a463877767254441ad49dd61076c0adb3320adf2d6c521e7abebac44116')
    for name in ('SOURCE_QUALIFICATION_SHA256','ACTUAL_ROOT_BINDING_RECEIPT_SHA256','ACTUAL_TRANSFER_QUALIFICATION_SHA256','REACTION_MULTIPLICITY_QUALIFICATION_SHA256','ACTUAL_SCIENTIFIC_REFERENCE_SHA256'):check('original unknown global '+name,isinstance(wg[name],ast.Constant)and wg[name].value is None)
    check('both original default full APIs',calls(w).count('first_reader.decode')==1 and calls(w).count('second_reader.decode_stream')==1 and all(len(n.args)==1 and not n.keywords for n in ast.walk(w)if isinstance(n,ast.Call)and ast.unparse(n.func)in('first_reader.decode','second_reader.decode_stream')))
    check('no wrapper selective or dense/reaction helpers',not any(x.rsplit('.',1)[-1]in('reaction_selection','scatter','macro','matrix','solve')for x in calls(w)))
    check('original state and reader lifetimes/releases retained',"for state in ('A','B'):"in wrapper and wrapper.index('del records')<wrapper.index('second_reader.decode_stream')and 'del second_records, second_stats'in wrapper)
    doc=(original/'FUTURE_PROTOCOL_CONTROLS.UNEXECUTED.json').read_text();old_word='nonrepresentable REAL32 rejects without repair';new_word='REAL32 overflow or nonfinite resulting cast rejects without repair; ordinary finite REAL32 rounding and underflow remain accepted with parser64 bits retained'
    check('one exact wording hunk only',doc.count(old_word)==1);corrected=doc.replace(old_word,new_word,1)
    corrected_path=HERE/'FUTURE_PROTOCOL_CONTROLS.clarified.UNEXECUTED.json'
    if corrected_path.exists():check('existing corrected wording Source unchanged',corrected_path.read_text()==corrected)
    else:corrected_path.write_text(corrected)
    check('full wording byte inverse',corrected.replace(new_word,old_word,1)==doc)
    docproof={'schema':'RAWRECORD_REAL32_WORDING_ONLY_COMPLETE_BYTE_INVERSE_V1','original':old['files']['FUTURE_PROTOCOL_CONTROLS.UNEXECUTED.json'],'new':pin(HERE/'FUTURE_PROTOCOL_CONTROLS.clarified.UNEXECUTED.json'),'hunks':[[old_word,new_word]],'full_inverse_sha256':hashlib.sha256(doc.encode()).hexdigest(),'wrapper_BODY_and_ALL_original_SOURCE_files_unchanged':True,'runtime_or_parser_executed':False}
    write(HERE/'REAL32_wording_only_inverse.json',docproof)
    binder=(HERE/'generate_ROOT_actual_rawrecord_binding.py').read_text();b=ast.parse(binder);bg=globals_(b)
    host=(HERE/'full_AB_rawrecord_genuine_host_UNREADY.py').read_text();h=ast.parse(host);hg=globals_(h)
    protocol=(HERE/'full_rawrecord_protocol_controls_UNREADY.py').read_text();p=ast.parse(protocol);pg=globals_(p)
    for name,tree,g in (('binder',b,bg),('genuinehost',h,hg),('protocol',p,pg)):
        check(name+' original ninecaps1800/600/512/2GiB/96/free8/1/1/0',ast.dump(g['CAPS'],include_attributes=False)==ast.dump(ast.parse(CAP_EXPR,mode='eval').body,include_attributes=False))
        check(name+' no importtime reviewed calls',all(isinstance(n,(ast.Expr,ast.Import,ast.ImportFrom,ast.Assign,ast.FunctionDef,ast.If))for n in tree.body))
        check(name+' no reviewed library imports',not any(n.module and any(term in n.module for term in('native_records','stream_records','numpy','scipy','guard','production'))for n in tree.body if isinstance(n,ast.ImportFrom)))
        check(name+' no system/exec/eval/compile business launching',not any(x in('exec','eval','compile','os.system','subprocess.Popen','subprocess.run')for x in calls(tree)))
    for key,node in hg.items():
        if key in ('SOURCE_STATUS','SOURCE_ARCHIVE','RECEIPTS','HOST','OUT','CONTROL','TARGET','TARGET_SHA','PROTOCOL','PROTOCOL_SHA','BINDING','BINDING_SHA','SOURCE_ADMISSION_SHA')or 'QUALIFICATION_SHA256'in key or 'SCIENTIFIC_REFERENCE_SHA256'in key:check('host unknown actual pin '+key,isinstance(node,ast.Constant)and node.value is None)
    check('protocol actual success unknown',isinstance(pg['ACTUAL_PROTOCOL_QUALIFICATION_SHA256'],ast.Constant)and pg['ACTUAL_PROTOCOL_QUALIFICATION_SHA256'].value is None)
    check('binder never imports helper/guard/reader module',not any(x.startswith(('importlib.','support.','helper.','g.','nr.','sr.','first_reader.','second_reader.'))for x in calls(b)))
    check('real material origin—not guessed macroSHA',"audit['source_sha256'][macro_entries[state]['path']]==macro_entries[state]['sha256']"in binder and"results['inputs_manifest_sha256']==p['material_inputs']['sha256']"in binder)
    check('real current150sameTemp/ratios/all62originalrows',"geo['physical_z_edges_cm']==[0,50,100,150]"in binder and"len(rows)==62"in binder and"cfg['pu_A']==.21"in binder and"cfg['pu_B']==.2436"in binder and"temperature_K"in binder)
    check('original3percent1percentglobalnormalizationunchanged',"==.03"in binder and"==.01"in binder and"one global integrated nu-fission normalization; no per-layer or per-group scaling"in binder)
    check('full material Source union no sample/filter',"len(declared)==len(protected)"in binder and"set(protected)"in binder and"for row in declared:actual_pin(row)"in binder)
    check('fresh actual source peer typed0/no session required',"type(tr.get('exit_code'))is int"in binder and"tr['exit_code']==0"in binder and"'session_id'not in tr"in binder and"review['blockers']==[]"in binder)
    check('binding prohibits future success/sourcefakepasses',all(isinstance(bg[key],ast.Constant)and bg[key].value is None for key in('UNKNOWN_ACTUAL_TRANSFER_QUALIFICATION_SHA256','UNKNOWN_REACTION_MULTIPLICITY_QUALIFICATION_SHA256','UNKNOWN_SCIENTIFIC_REFERENCE_SHA256')))
    check('wrapper READYonly3globalhunks/fullbyteASTinverse',"wrapper_hunks=["in binder and"functions(ready)==functions(raw)"in binder and"inverse==raw"in binder)
    check('no binding/READYwrapper SHA hashcycle',"'ready_wrapper'"not in binder[binder.index("binding={'schema'"):binder.index('d.mkdir();e.mkdir()')])
    check('complete frozen new Source inventory/sourcecopy no omission',"for row in manifest['files']:"in binder and"for p in sorted(d.rglob('*'))if p.is_file()"in binder)
    check('protocol toy only APIs defaultfull',calls(p).count('nr.decode')>=1 and calls(p).count('sr.decode_stream')>=1 and all(not n.keywords for n in ast.walk(p)if isinstance(n,ast.Call)and ast.unparse(n.func)in('nr.decode','sr.decode_stream')))
    check('no protocol current material input accesses',not any(x in protocol for x in ('macro.ascii','material.xsm','MATERIAL =','INPUTS =')))
    fixture=next(n for n in p.body if isinstance(n,ast.FunctionDef)and n.name=='tiny_fixture')
    fixture_calls=[n for n in ast.walk(fixture)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='named']
    check('all original tiny LCM kinds0/10/99/1/2/3/4',set(ast.literal_eval(n.args[2])for n in fixture_calls)=={1,2,3,4,10,99}and"indexed(2,g,0,-1)"in protocol)
    check('exact tiny signature12char rawpadding',next(ast.literal_eval(n.args[4])for n in fixture_calls if ast.literal_eval(n.args[1])=='SIGNATURE')=='4 4 4\nL_MACROLIB   \n')
    check('tiny complete rawchar padded8chars',next(ast.literal_eval(n.args[4])for n in fixture_calls if ast.literal_eval(n.args[1])=='RAWCHAR')=='4 4\nAB      \n')
    check('tiny signedwide exact integer, signedfloatbits and underflow',"9007199254740993"in protocol and"1e-300 -1e-300"in protocol and"struct.pack('<d',a)==struct.pack('<d',b)"in protocol)
    check('full moment/fission andextra reactiontoyrawrecords',"for moment in (0,1,2):"in protocol and"'FISSIONINDEX',1,4"in protocol and"'NUSIGF',2,4"in protocol and"'EXTRA_RXN'"in protocol)
    main_p=next(n for n in p.body if isinstance(n,ast.FunctionDef)and n.name=='main')
    accepted=[n for n in ast.walk(main_p)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='accepted']
    rejects=[n for n in ast.walk(main_p)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='both_reject']
    check('five declared positives and ten declared actualnegativecontrols',len(accepted)==5 and len(rejects)==7 and"len(controls)==5 and len(rejects)==10"in protocol)
    check('all truncatednumeric/character/header/endcontrols',all(x in protocol for x in('truncated final numeric payload','truncated raw character payload','truncated malformed full header','missing terminal root close')))
    check('default bothreader negatives retained',"actual_observed_errors':details"in protocol and"(('native_default',lambda:nr.decode(malformed)),('stream_default',lambda:sr.decode_stream(io.BytesIO(malformed))))"in protocol)
    check('signedzero/order/REAL32overflow nofixupcontrols',all(x in protocol for x in('signed zero parser/REAL64 bit mutation rejected','key order mutation rejected','REAL32 overflow or nonfinite resulting cast rejected, finite ordinary rounding allowed')))
    check('missing data remains explicit scientificgap',"future_solver_scientific_input_admitted']is False"in protocol and"missing_real_record_no_substitution"in protocol and"complete_tiny_required_field_gap_inventory.jsonl"in protocol)
    check('exact host originalgenuinechain',all(x in calls(h)for x in('support.load','helper.modules','helper.guard_admission','full.OwnRSSSerialExecutor','resource.DynamicHistoryResources','resources.check','runner.execute')))
    check('no new mock/resource/guard/executor class',not any(isinstance(n,ast.ClassDef)for n in h.body))
    old_host=PARENT_HOST.read_text();guard_chunks=[
        "if len(sys.argv)!=1 or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or sys.getprofile() is not None:\n        raise ValueError('fixed unprofiled nonoptimized read-only admission host required')",
        "if hashlib.sha256(SUPPORT.read_bytes()).hexdigest()!=SUPPORT_SHA:\n        raise ValueError('fixed normal support source required')",
        "if any(os.environ.get(k)!='1' for k in support.THREAD_KEYS) or Path(sys.executable).resolve()!=support.PYTHON:\n        raise ValueError('original single-thread Python required')",
        "helper,hpin=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'axmat_v15_admission_original619')\n    resource,rpin=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'axmat_v15_admission_real_resource_module')\n    full,production=helper.modules();helper.guard_admission(full)",
        "if full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,) or Path(full.__file__).resolve()!=support.FULL or Path(production.__file__).resolve()!=support.PARENT:\n        raise ValueError('unchanged genuine supervisor required')",
        "if before['artifact_bytes']+ARCHIVE_CAP>=96*2**30 or before['disk_free_bytes']-ARCHIVE_CAP<8*2**30:\n            raise ValueError('complete original resource reserve required')",
        "remaining=WHOLE_CAP-(time.monotonic()-started)\n        if remaining<=0:raise ValueError('whole admission budget exhausted')",
    ]
    for i,chunk in enumerate(guard_chunks):check('original normal host exact genuine guard chunk '+str(i),old_host.count(chunk)==host.count(chunk)==1)
    check('strict5ARTroots runtimeassert excludesoutsideD/E',"for p in(host,out,control,support.OUT,support.TERMINAL)"in host and"roots=resource.history_roots([str(host),str(out),str(control),str(support.OUT),str(support.TERMINAL)],support.ART)"in host)
    check('original dynamic allfamily resourceSourceunchanged',source_origins['original_genuine_resource_ebbb.SOURCE.py']['sha256']=='ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022')
    check('jointHOSTOUTCONTROLD/E completebefore-between-after-final',"joint_paths=(host,out,control,archive,receipts)"in host and host.count('support.archive_bytes(joint_paths)')==4)
    executes=[n for n in ast.walk(h)if isinstance(n,ast.Call)and ast.unparse(n.func)=='runner.execute']
    check('exactly2serialstages/nochildpool/noretry',len(executes)==2 and"runner.execute(host/'protocol_run'"in host and host.index("runner.execute(host/'protocol_run'")<host.index("runner.execute(host/'transfer_run'")and"len(runner.records)==2"in host)
    check('actualPIDwatchcrosscheck finiteRSS/time sourceguard',"report['actual_child_PID']==watch['pid']"in host and"report['actual_parent_PID']==host_pid"in host and"math.isfinite(watch['sampled_peak_rss_mib'])"in host)
    check('complete namespacebeforeafterdirs/syms/source/receipts',"complete_source_inputs(support,archive)==source_inputs"in host and"complete_source_inputs(support,receipts)==receipt_inputs"in host and"not stat.S_ISLNK(s.st_mode)"in host)
    check('honest merged childstreams/externalRootclosure required',"child_separate_stderr_saved':False"in host and"external_actual_Root_typed_EXIT0_CLOSED_required=True"in host)
    check('genuine modules resourceMRO never patched',not any(isinstance(n,(ast.Assign,ast.AugAssign))and any(isinstance(t,ast.Attribute)and any(x in ast.unparse(t)for x in('full.','production.','resource.','helper.'))for t in(getattr(n,'targets',[])or[getattr(n,'target',None)]))for n in ast.walk(h)))
    old_lines=old_host.splitlines(keepends=True);new_lines=host.splitlines(keepends=True);opcodes=difflib.SequenceMatcher(a=old_lines,b=new_lines,autojunk=False).get_opcodes();hunks=[]
    for tag,a0,a1,b0,b1 in opcodes:
        if tag!='equal':hunks.append({'tag':tag,'original_line_interval':[a0,a1],'candidate_line_interval':[b0,b1],'original_bytes_utf8':''.join(old_lines[a0:a1]),'candidate_bytes_utf8':''.join(new_lines[b0:b1])})
    reconstructed=[]
    for tag,a0,a1,b0,b1 in opcodes:reconstructed.extend(new_lines[b0:b1]if tag=='equal'else old_lines[a0:a1])
    check('full finite normalhost byteinverse→776b',''.join(reconstructed)==old_host)
    check('full normalhost inverseAST original main',ast.dump(ast.parse(''.join(reconstructed)),include_attributes=False)==ast.dump(ast.parse(old_host),include_attributes=False))
    write(HERE/'full_genuine_host_adaptation_complete_inverse.json',{'schema':'CURRENT150_AB_NEW_GENUINE_HOST_COMPLETE_SOURCE_DELTA_INVERSE_V1','source_only':True,'original_host':source_origins['original_normal_PREP_host_776b.SOURCE.py'],'candidate_host':pin(HERE/'full_AB_rawrecord_genuine_host_UNREADY.py'),'difference_hunk_count':len(hunks),'all_full_hunks':hunks,'full_inverse_original_sha256':hashlib.sha256(''.join(reconstructed).encode()).hexdigest(),'full_inverse_byte_and_AST_equal':True,'genuine_original_guard_byte_chunks_preserved':guard_chunks,'intentional_scope_adaptation':'one prior PREP stage becomes two new software-only serial protocol/full raw transfer stages; full original genuine external classes/MRO/caps remain','actual_runtime_or_science_qualification_created':False})
    write(HERE/'SOURCE_origins_and_complete_copy_inventory.json',{'schema':'CURRENT150_AB_COMPLETE_ORIGINAL_SOURCE_COPY_PROVENANCE_V1','source_only':True,'old_complete_package_manifest':old_manifest,'old_full_source_members':old_pins,'old_sealed_independent_peer':peer_manifest,'genuine_and_material_source_origins':source_origins,'all_copies_byteexact':True,'no_reader_guard_API_or_business_import_call_compile':True})
    final_source_pins={name:pin(HERE/name)for name in('full_AB_rawrecord_genuine_host_UNREADY.py','full_rawrecord_protocol_controls_UNREADY.py','generate_ROOT_actual_rawrecord_binding.py')}
    write(HERE/'SOURCE_CHECKS.json',{'schema':'CURRENT150_AB_RAWRECORD_BINDER_GENUINEHOST_PROTOCOL_SOURCE_CHECKS_V1','status':'SOURCE_ONLY_STATIC_SELF_CHECKS_PASS_NOT_INDEPENDENT_OR_RUNTIME_ADMISSION','source_only':True,'checks':checks,'all_checks_passed':True,'check_count':len(checks),'final_source_pins':final_source_pins,'actual_protocol_positive_results':None,'actual_protocol_negative_results':None,'actual_material_SHA7ID_bindings_created':False,'actual_source_admission_created':False,'actual_READY_files_created':False,'actual_protocol_qualified':False,'actual_full_rawrecord_transfer_qualified':False,'scientific_accuracy_qualified':False,'physical_neutron_balance_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False})
    print(json.dumps({'source_only':True,'status':'FINITE_SOURCE_TEXT_AST_HASH_SELF_CHECKS_COMPLETE_NOT_RUNTIME','check_count':len(checks),'all_checks_passed':True,'wrapper_sha256':'098b2a463877767254441ad49dd61076c0adb3320adf2d6c521e7abebac44116','final_source_pins':final_source_pins,'actual_runtime_qualified':False,'all_scientific_qualifications':False},allow_nan=False),flush=True)

if __name__=='__main__':main()
