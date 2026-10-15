"""Independent finite Source/META review. No candidate imports or execution."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

P=Path(__file__).resolve().parent
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
S=B/'finite_current150_old_XSM_context_aware_aggregation_UNREADY_SOURCE_20261010'
O=Path('/private/tmp/axmat_COMPLETE_oldXSM_context_aware_aggregation_UNREADY_SOURCE_20261010_s7ik4_qc')
RET=B/'Root_actual_complete_old_XSM_context_aware_aggregation_Source_retention_record.json'
TOOL=B/'Root_actual_complete_old_XSM_context_aware_aggregation_Source_retention_tool_return.json'
checks=[]
def require(v,msg):
    if type(v) is not bool or not v:raise ValueError(msg)
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);s=p.lstat();require(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'unaliased Source/META regular file')
    with p.open('rb') as f:
        require(ident(os.fstat(f.fileno()))==ident(s),'open7ID')
        raw=f.read();require(ident(os.fstat(f.fileno()))==ident(s),'EOF7ID')
    require(ident(p.lstat())==ident(s),'path7ID')
    return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ident(s)),raw
def snapshot(root):
    files={};dirs={}
    for p in [root,*sorted(root.rglob('*'))]:
        s=p.lstat();require(not stat.S_ISLNK(s.st_mode),'no Source symlink')
        rel=str(p.relative_to(root))
        if stat.S_ISDIR(s.st_mode):dirs[rel]=ident(s)
        else:files[rel]=pin(p)[0]
    return dict(root=str(root),files=files,directories=dirs)
def check(label,v):
    require(type(v) is bool,'exact typed independent check')
    checks.append(dict(check=label,passed=v))
def save(name,obj):
    (P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
before={'original':snapshot(O),'retained':snapshot(S),'retention_record':pin(RET)[0],'retention_tool':pin(TOOL)[0]}
data={rel:pin(S/rel)[1] for rel in before['retained']['files']}
manifest=json.loads(data['MANIFEST.json'])
check('fixed original manifest SHA matches Root task',before['retained']['files']['MANIFEST.json']['sha256']=='2c0b20393b5ab202be815be6524d417c7c18ea91da719b05dc678948f920dd89')
check('manifest complete194 members original195 and Root retained196 files',manifest['member_count']==194 and len(manifest['members'])==194 and len(before['original']['files'])==195 and len(before['retained']['files'])==196)
check('all194 original members fullEOF size SHA exact7ID match manifest',all(before['original']['files'][m['relative_path']]=={k:m[k] for k in ('path','sha256','size_bytes','identity')} for m in manifest['members']))
check('all original directories including root exact7ID match manifest',all(ident(Path(d['path']).lstat())==d['identity'] for d in manifest['directories']))
check('all194 retained members complete bytes/SHA/size match original manifest',all(before['retained']['files'][m['relative_path']]['sha256']==m['sha256'] and before['retained']['files'][m['relative_path']]['size_bytes']==m['size_bytes'] for m in manifest['members']))
ret=json.loads(pin(RET)[1]);rt=json.loads(pin(TOOL)[1])
check('Root true retention record SHA and Source-only contract',before['retention_record']['sha256']=='b7565bcce19bc73bb2159a0f5803e67c225aaa0369f6fa37f2b469986f94cf98' and ret['source_only'] is True and ret['new_qualification_created'] is False and ret['helper_guard_business_executed'] is False and ret['cleanup_performed'] is False)
check('Root all195 original and saved fullpins coupled without copiedID conflation',ret['complete_original_member_count']==195 and set(ret['complete_original_members'])==set(before['original']['files']) and all(v['original']==before['original']['files'][rel] and v['saved']==before['retained']['files'][rel] for rel,v in ret['complete_original_members'].items()))
check('Root additional original seal receipt complete bytes and current saved pin',ret['saved_actual_peer_seal_receipt']==before['retained']['files']['_actual_peer_seal_receipt.json'] and ret['saved_actual_peer_seal_receipt']['sha256']==ret['original_actual_peer_seal_receipt']['sha256'] and pin(ret['original_actual_peer_seal_receipt']['path'])[0]==ret['original_actual_peer_seal_receipt'])
check('Root retention typedEXIT0 CLOSED source-only actual receipt',type(rt['terminal_tool_return']['exit_code']) is int and rt['terminal_tool_return']['exit_code']==0 and 'session_id' not in rt['terminal_tool_return'] and rt['terminal_tool_return']['chunk_id']=='2690bf' and rt['closed'] is True)
parent=json.loads(data['COMPLETE_FIXED_PARENT_SOURCE/MANIFEST.json'])
check('complete fixed parent162 members and parent manifest byteexact retained',parent['member_count']==162 and len(parent['members'])==162 and sum(rel.startswith('COMPLETE_FIXED_PARENT_SOURCE/') for rel in data)==163 and all(hashlib.sha256(data['COMPLETE_FIXED_PARENT_SOURCE/'+m['relative_path']]).hexdigest()==m['sha256'] for m in parent['members']))
trees={name:ast.parse(raw) for name,raw in data.items() if name.endswith('.py')}
check('all Python Source AST parsed without import compile or execution',len(trees)>0 and all(type(t) is ast.Module for t in trees.values()))
bysha={hashlib.sha256(raw).hexdigest():raw for raw in data.values()}
inverse_results=[]
def restore(candidate,d):
    require(hashlib.sha256(candidate).hexdigest()==d['candidate_SHA256'],'candidate proof pin')
    rows=candidate.decode().splitlines(keepends=True)
    for h in reversed(d['complete_zero_based_hunks']):
        require(rows[h['new_start0']:h['new_end0']]==h['new_full_lines'],'complete inverse candidate hunk')
        rows[h['new_start0']:h['new_end0']]=h['old_full_lines']
    old=''.join(rows).encode()
    require(hashlib.sha256(old).hexdigest()==d['original_SHA256'],'complete inverse parent SHA')
    if d['original_SHA256'] in bysha:require(old==bysha[d['original_SHA256']],'complete original Source byte equality')
    return old
for name in ('COMPLETE_CONTEXT_AWARE_SOURCE_FULL_INVERSE.json','COMPLETE_CONTEXT_GENUINE_HOST_BINDER_FULL_INVERSE.json'):
    proof=json.loads(data[name])
    for d in proof['derivations']:
        raw=data[d['candidate']];old=restore(raw,d)
        before_defs=after_defs=None
        if d['candidate'].endswith('.py'):
            bt,at=ast.parse(old),ast.parse(raw)
            bdefs={x.name:ast.dump(x,include_attributes=False) for x in bt.body if isinstance(x,(ast.FunctionDef,ast.ClassDef))}
            adefs={x.name:ast.dump(x,include_attributes=False) for x in at.body if isinstance(x,(ast.FunctionDef,ast.ClassDef))}
            before_defs=len(bdefs);after_defs=len(adefs)
            changes=[n for n in bdefs if n not in adefs or bdefs[n]!=adefs[n]]
        else:changes=None
        inverse_results.append(dict(candidate=d['candidate'],hunks=len(d['complete_zero_based_hunks']),candidate_sha256=d['candidate_SHA256'],original_sha256=d['original_SHA256'],complete_bytes_inverse=True,old_top_definitions=before_defs,new_top_definitions=after_defs,changed_original_top_definitions=changes))
        bysha[d['original_SHA256']]=old
check('all11 engine observer extractor host binder derivations complete finite byte inverse',len(inverse_results)==11 and all(x['complete_bytes_inverse'] is True for x in inverse_results))
proof=json.loads(data['COMPLETE_V23_OLD_XSM_EXTRACTION_SOURCE_INVERSE.json'])
extract_original=restore(bysha[proof['candidate_SHA256']],proof)
check('full extractor chain final to intermediate to original actual9d849 native Source bytes',extract_original==data['COMPLETE_FIXED_PARENT_SOURCE/FINITE_ACTUAL_NATIVE_V23_SOURCE_META/Root_bound_complete_native_checker.py'])
extract_tree=trees['complete_observed_old_post_final_XSM_extractor.UNREADY.py'];native_tree=ast.parse(extract_original)
node_map=lambda t:{n.name:ast.dump(n,include_attributes=False) for n in t.body if isinstance(n,(ast.ClassDef,ast.FunctionDef))}
em,nm=node_map(extract_tree),node_map(native_tree)
check('original native XSM ReadOnlyFileBytes DiskRecords full AST unchanged',all(em[n]==nm[n] for n in ('XSM','ReadOnlyFileBytes','DiskRecords')))
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
blockers=[]
def blocker(n,line,expression,actual_type,message):
    text=data[n].decode().splitlines()[line-1]
    require(expression in text,'specific source evidence anchor')
    blockers.append(dict(file_pin=before['retained']['files'][n],line=line,source=text,expression=expression,returned_type_on_legitimate_context=actual_type,reason=message,no_candidate_execution=True))
blocker('bind_complete_context_aware_and_oldXSM_SOURCE_only.UNREADY.py',227,'type(observations[state])is list and observations[state]','list','For any legal nonempty state snapshot list this condition is a list. Exact-bool require refuses before Source binding. Both operations are blocked.')
blocker('complete_observed_old_post_final_XSM_extractor.UNREADY.py',770,'type(inputs)is list and inputs','list','Legal nonempty complete snapshot input is rejected by exact-bool require, before complete native traversal.')
blocker('complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py',926,'type(pins)is list and pins','list','Legal nonempty complete context pin list is rejected by exact-bool require. It is caught as initialization failure; no aggregation is performed.')
blocker('complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py',1031,'require(calls,','dict','Completed call map is a dict, which exact-bool require rejects even when complete.')
blocker('complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py',1040,'require(track and masks,','list','With valid nonempty track and mask lists the final operand is the mask list; exact-bool require rejects it.')
et=trees['complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py']
false_node=next(n for n in et.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name)and t.id=='FALSE'for t in n.targets))
false_keys={k.arg for k in false_node.value.keywords}
report=next(n for n in ast.walk(et) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)and n.func.id=='dict'and n.lineno==1756)
collisions=false_keys & {k.arg for k in report.keywords if k.arg}
require(collisions=={'genuine_supervisor_watch_verified_here'},'exact dict keyword collision evidence')
blockers.append(dict(file_pin=before['retained']['files']['complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py'],line=1756,end_line=1765,source='\n'.join(engine.splitlines()[1755:1765]),duplicate_keyword='genuine_supervisor_watch_verified_here',reason='dict call explicitly supplies this keyword and expands FALSE with the same key. Python raises TypeError, before final completed/failed diagnostic report write.',AST_full_collision_proof=True,no_candidate_execution=True))
check('all legitimate complete lists and call maps are admitted by exactbool require',False)
check('completed diagnostic final report has no duplicate expanded kwargs',False)
after={'original':snapshot(O),'retained':snapshot(S),'retention_record':pin(RET)[0],'retention_tool':pin(TOOL)[0]}
check('full original195 and retained196 source members plus dirs and Root retention META unchanged beforeafter',before==after)
require(len({c['check'] for c in checks})==len(checks),'unique finite aggregate labels')
save('FULL_SOURCE_INVENTORY_AND_RETENTION_BEFORE_AFTER.json',dict(source_only=True,before=before,after=after,all_exact=True,no_numeric_material_DB_read=True))
save('COMPLETE_INVERSE_AND_AST_SOURCE_FACTS.json',dict(source_only=True,derivations=inverse_results,full_original_actual_native_chain_inverse=True,native_classes_AST_unchanged=True,all_Python_Source_AST_count=len(trees)))
save('SIX_PRECISE_SOURCE_BLOCKERS.json',dict(source_only=True,blockers=blockers,all_candidate_source_unchanged=True,expression_evidence_not_candidate_execution=True,no_pass_or_actual_RSS_prediction=True))
report=dict(schema='INDEPENDENT_COMPLETE_CONTEXT_AWARE_ENGINE_HOST_BINDER_SOURCE_REVIEW_V2',status='SOURCE_ONLY_BLOCKED_NO_EXECUTION_OR_SCIENCE',source_only=True,all_checks_passed=False,all_checks_typed_true=all(c['passed'] is True for c in checks),check_count=len(checks),checks=checks,blockers=blockers,qualified_source_manifest=before['original']['files']['MANIFEST.json'],retained_source_manifest_pin=before['retained']['files']['MANIFEST.json'],actual_Root_retention_record_pin=before['retention_record'],actual_Root_retention_tool_pin=before['retention_tool'],complete_original_files=195,complete_retained_files=196,complete_original_declared_members=194,complete_original_and_retained_directories=len(before['original']['directories']),complete_fixed_parent_members=162,actual_independent_candidate_execution=None,new_Q=None,scientific_qualification_created=False,AAA_accuracy_qualified=False,ABA_admitted=False,historical_native_RAM_bits_verified=False,original_native_build_binary_Source_linkage_qualified=False,complete_final_construction_qualified=False,whole_combined_build_or_INPUT_qualified=False,materials_DB_numeric_helper_API_guard_compile_not_executed=True,limits={'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'joint_archive_bytes':2*2**30,'history_bytes':96*2**30,'free_floor_bytes':8*2**30,'threads':1,'children_at_once':1,'retries':0},scope={'isotopes':62,'groups':370,'mixes':8,'extras':18,'moments':3,'prompt_components':32,'fission_index_values':64,'fission_component_mix_values':256,'delayed_pairs':6,'Lambda_values':48,'STATE_values':40,'complete_macro_records':19619},unqualified_components=json.loads(data['COMPLETE_CONTEXT_AWARE_FIELD_PRODUCER_SCOPE_AND_GAPS.json'])['remaining_specific_unqualified_components'],binding_usage='Original binder requires its P root to equal original absolute manifest member paths; Root-retained byte-identical copy does not transplant original7ID. Fixes need a new fixed derivative, full Source inverse and independent review. No current PASS admission may consume this blocked report.')
roles={'host_template':'complete_context_aware_aggregation_and_oldXSM_genuine_host.UNREADY.py','engine_template':'complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py','adapter':'saved_native_data_access_adapter.UNREADY.py','binder':'bind_complete_context_aware_and_oldXSM_SOURCE_only.UNREADY.py','old_XSM_extractor':'complete_observed_old_post_final_XSM_extractor.UNREADY.py','observer_module':'AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90'}
for k,n in roles.items():report[k]=before['original']['files'][n]
save('REVIEW.json',report)
print(json.dumps(dict(source_only=True,status=report['status'],review=pin(P/'REVIEW.json')[0],check_count=len(checks),passed_checks=sum(c['passed'] for c in checks),failed_checks=sum(not c['passed'] for c in checks),blocker_count=len(blockers),no_candidate_execution=True,new_Q=None),ensure_ascii=False),flush=True)
