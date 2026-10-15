"""Independent finite Source/META review; never imports or executes reviewed Source."""
import ast,hashlib,json,math,os,re,stat
from pathlib import Path
P=Path('/private/tmp/axmat_v25_complete_canonical_TRUE_snapshot_jointQ_UNREADY_SOURCE_bwo0x_85')
OUT=Path(__file__).parent
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
checks=[];inputs={}
def check(label,value,evidence=None):
    if type(value)is not bool:raise TypeError('review predicate not exact bool '+label)
    if any(r['check']==label for r in checks):raise ValueError('duplicate review label')
    checks.append(dict(check=label,passed=value,evidence=evidence))
    if not value:raise AssertionError(label)
def identity(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);before=identity(p)
    assert p.is_absolute() and stat.S_ISREG(before[2]) and not p.is_symlink()
    with p.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    assert identity(p)==before
    v=dict(path=str(p),sha256=h,size_bytes=before[4],identity=before)
    if str(p)in inputs:assert inputs[str(p)]==v
    inputs[str(p)]=v;return v
def pairs(rows):
    v={}
    for k,x in rows:
        if k in v:raise ValueError('duplicate metadata key')
        v[k]=x
    return v
def load(p):
    pin(p);v=json.loads(Path(p).read_bytes(),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in()).throw(ValueError(x)))
    def finite(x):
        if type(x)is float:assert math.isfinite(x)
        elif type(x)is list:
            for a in x:finite(a)
        elif type(x)is dict:
            for a in x.values():finite(a)
    finite(v);return v
def inventory(root):
    files={};dirs={}
    for folder,dnames,names in os.walk(root,followlinks=False):
        q=Path(folder);assert stat.S_ISDIR(q.lstat().st_mode)and not q.is_symlink()
        dirs[str(q.relative_to(root))]=identity(q)
        for n in names:files[str((q/n).relative_to(root))]=pin(q/n)
    return dict(files=files,directories=dirs)
def shape_pin(v):
    ids=v.get('identity',v.get('identity7'));assert type(ids)is list and len(ids)==7 and all(type(x)is int for x in ids)
    assert type(v['path'])is str and type(v['sha256'])is str and re.fullmatch('[0-9a-f]{64}',v['sha256'])
    if 'size_bytes'in v:assert type(v['size_bytes'])is int and v['size_bytes']==ids[4]
    return dict(path=v['path'],sha256=v['sha256'],size_bytes=ids[4],identity=ids)
def defs(s):return {n.name:ast.get_source_segment(s,n)for n in ast.parse(s).body if isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef))}
def reverse(s,rows):
    for r in reversed(rows):
        assert type(r['count'])is int and r['count']>0 and s.count(r['new'])==r['count'],r.get('label')
        s=s.replace(r['new'],r['old'])
    return s
def assignments(s):return {n.targets[0].id:n.value for n in ast.parse(s).body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
def closed(v,chunk):return type(v)is dict and v.get('chunk_id')==chunk and type(v.get('exit_code'))is int and v['exit_code']==0 and 'session_id'not in v
def dump(p,v):
    with p.open('x')as f:json.dump(v,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
mp=pin(P/'MANIFEST.json');m=load(P/'MANIFEST.json');before=inventory(P)
check('fixed complete author manifest SHA',mp['sha256']=='9e9a77669309071065c189ad02ee455709ca81db376de818825d99d8cf22f6e9')
check('full finite 38 members 39 files four directories exact',len(m['members'])==38 and set(before['files'])==set(m['members'])|{'MANIFEST.json'}and len(before['directories'])==4)
check('all complete member EOF SHA byte counts seven integer identities',all(shape_pin(v)==before['files'][n]for n,v in m['members'].items()))
check('all directories exact identities including root',before['directories']==m['directories'])
check('complete byte count 2000575 exact',sum(v['size_bytes']for n,v in before['files'].items()if n!='MANIFEST.json')==m['complete_member_bytes']==2000575)
py=[];jsons=[]
for n in before['files']:
    if n.endswith('.py'):ast.parse((P/n).read_text());py.append(n)
    elif n.endswith('.json'):load(P/n);jsons.append(n)
check('every Source complete EOF AST and every JSON strict finite decode',len(py)>0 and len(jsons)>0,dict(Source_files=len(py),JSON_files=len(jsons)))
check('author manifest no future Q or business admission supplied',m['source_only']is True and all(m[k]is None for k in ['new_Q_binding_sha256','external_actual_new_Q_root_writer_terminal_binding_pin','external_actual_new_Q_saved48_peer_binding_pin','external_actual_new_Q_saved48_retention_binding_pin'])and m['candidate_helper_guard_API_compiler_or_numeric_executed']is False and m['project_canonical_frozen_Source_ART_written']is False)
roles={'canonical':'canonical.V25.UNREADY.full.py','prepare_host':'host_and_postclose_templates/prepare_host.V25.UNREADY.full.py','prepare_writer':'host_and_postclose_templates/prepare_writer.V25.UNREADY.full.py','build_host':'host_and_postclose_templates/build_host.V25.UNREADY.full.py','build_writer':'host_and_postclose_templates/build_writer.V25.UNREADY.full.py','PREP_binder':'bind_actual_V25_Q_to_complete_PREP_SOURCE.UNREADY.py','BUILD_binder':'bind_actual_V25_closed_PREP_to_complete_BUILD_SOURCE.UNREADY.py'}
rolepins={k:pin(P/n)for k,n in roles.items()};texts={k:(P/n).read_text()for k,n in roles.items()}
check('all seven actual full role pins coupled manifest',rolepins==m['seven_primary_role_Source_pins'])
inv=load(P/'COMPLETE_SOURCE_INVERSES.json');binv=load(P/'COMPLETE_SOURCE_BINDER_INVERSES.json');constants=load(P/'ROOT_BINDING_SOURCE_CONSTANTS.json')
for role,rows in inv['exact_finite_transforms'].items():
    parent=(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text();restored=reverse(texts[role],rows)
    check(role+' full byte inverse',restored==parent,dict(hunks=len(rows)))
    check(role+' complete AST and every definition inverse',ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False)and defs(restored)==defs(parent),dict(definitions=len(defs(parent))))
    check(role+' original actual Source fullpin and retained full bytes',pin(Path(constants['original_sources'][role]['path']))==constants['original_sources'][role]and hashlib.sha256(parent.encode()).hexdigest()==constants['original_sources'][role]['sha256'])
check('canonical all 70 original definitions retained',len(defs((P/'ORIGINAL_PARENT_SOURCE/canonical.full.py').read_text()))==70)
for role in ('PREP_binder','BUILD_binder'):
    row=binv['roles'][role];parent=(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text();restored=reverse(texts[role],[row['whole_exact_inverse']])
    check(role+' whole byte and AST inverse',restored==parent and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False))
    legacy=binv['roles'][role]['original_legacy_definition_bytes_exact']
    check(role+' all declared retained legacy definitions byte exact',all(defs(texts[role])[k]==defs(parent)[k]for k in legacy),dict(legacy_definitions=legacy,read_adapter_changed_honestly=(role=='BUILD_binder')))
    check(role+' original Source actual SHA seven identity',pin(Path(constants['original_sources'][role]['path']))==constants['original_sources'][role])
    check(role+' no runtime import eval compile of reviewed sources',not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id in ('eval','exec','compile','__import__')for n in ast.walk(ast.parse(texts[role]))))
    check(role+' complete package fullpin read registry and prewrite stability',all(x in texts[role]for x in ["files!=set(m['members'])|{'MANIFEST.json'}","dirs!=set(m['directories'])","source_pin(HERE/rel)!=wanted","tuple(READ_PINS.items())"]))
    check(role+' fresh TMP only Source output',"output.is_relative_to(Path('/private/tmp'))"in texts[role]and'os.path.lexists(output)'in texts[role]and'output.mkdir()'in texts[role])
canon=texts['canonical'];a=assignments(canon)
business=['FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']
check('all six future business pins plus Q and three proof bindings None',all(isinstance(a[k],ast.Constant)and a[k].value is None for k in business+['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA','FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN']))
check('three fresh inactive audit snapshots only private change',len([n for n in ast.walk(ast.parse(canon))if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr=='snapshot'])==3 and all(len(n.args)==0 and len(n.keywords)==1 and n.keywords[0].arg=='_consume'and isinstance(n.keywords[0].value,ast.Constant)and n.keywords[0].value.value is True for n in ast.walk(ast.parse(canon))if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr=='snapshot'))
for fn in ['record_actual_trim_component','create_complete_input_graph','complete_input_phase']:
    body=defs(canon)[fn]
    check(fn+' private snapshot after owned fresh with and last-use retains full trace','with g.ReadOpenAudit()as audit:'in body and body.index('with g.ReadOpenAudit()as audit:')<body.index('audit.snapshot(_consume=True)')and'audit'not in body[body.index('audit.snapshot(_consume=True)')+len('audit.snapshot(_consume=True)'):].replace('del audit','').replace('trace,audit','trace,').replace(',audit,',',').replace(',audit;', ';'))
check('prepare extra typed source owner and current ordinary paths retain every Q dependency','**helper_Q_admission()'in defs(canon)['prepare_build']and"owner='NEW SOURCE-owned historical INPUT reuse implementation'"in defs(canon)['create_complete_input_graph']and'expected_files=extra'in defs(canon)['create_complete_input_graph']and'*helper_Q_admission()'in defs(canon)['current_new_owned_paths'])
reader=['helper_Q_check','helper_Q_fullpin','helper_Q_verify_META','helper_Q_exact','helper_Q_closed0','helper_Q_collect_refs','helper_Q_admission']
check('both Source binders carry complete identical actual Q reader',all(defs(texts[r])[name]==defs(canon)[name]for r in ('PREP_binder','BUILD_binder')for name in reader))
check('strict Q boolean typed pin identity and float bits/order checks',all(x in canon for x in ['if type(value)is not bool','all(type(x)is int for x in ids)','a.hex()==b.hex()','list(a)==list(b)if ordered else set(a)==set(b)']))
check('all original protocol owner new snapshot fresh and source archive scopes retained',all(x in defs(canon)['helper_Q_admission']for x in ['all original thirteen protocol fields/order','[4,3,2,2]','[5,13,3]','[184,199]','records=37112,attempts=37112,canonical_files=37111','complete_node_count','779371','21411449','nonfinite_clone_after_clear','no_transactional_private_mode_promise','no_cross_process_PID_FD_inode_normalization','all27_return_fields']))
check('all new external Q reads fixed actual paths and recursive owners',all(x in defs(canon)['helper_Q_admission']for x in ["helper_Q_verify_META(FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN)","helper_Q_verify_META(FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN)","helper_Q_verify_META(FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN)","helper_Q_collect_refs(value,external)","complete[p]=row"]))
check('actual 94520a writer and saved48 17e611 821784 strict closed coupling',all(x in defs(canon)['helper_Q_admission']for x in ["helper_Q_closed0(qt['terminal_tool_return'],'94520a')","helper_Q_closed0(reviewtool['actual_success_tool_return'],'17e611')","helper_Q_closed0(seal['terminal_tool_return'],'821784')","peer['check_count']==len(peer['checks'])==48","observed['actual_metadata_Q']","members['REVIEW.json']['original']"]))
check('UNREADY canonical rejects before project load','helper_Q_admission()'in defs(canon)['require_ready']and"DRAFT_STATUS != 'READY_REVIEWED_V25_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'"in defs(canon)['require_ready']and "if __name__=='__main__':\n    require_ready()"in canon)
for role in ('prepare_host','prepare_writer','build_host','build_writer'):
    tree=ast.parse(texts[role]);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main')
    check(role+' UNREADY guard first main statement',isinstance(fn.body[0],ast.If)and any(isinstance(n,ast.Name)and n.id=='SOURCE_BINDING_STATUS'for n in ast.walk(fn.body[0]))and any(isinstance(n,ast.Raise)for n in ast.walk(fn.body[0])))
    aa=assignments(texts[role]);unknown=[k for k in aa if k.startswith('FUTURE_V25_')]
    check(role+' all future globals None before reads',bool(unknown)and all(isinstance(aa[k],ast.Constant)and aa[k].value is None for k in unknown))
check('original complete genuine PREP BUILD caps and MRO retained',all(x in texts['prepare_host']and x in texts['build_host']for x in ['1800,600,512,2*2**30','OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)','DynamicHistoryResources','8*2**30,96*2**30','retries=0','children_at_once=1']))
check('all original five stages build writer branches preserved',"['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']"in texts['build_writer']and"choices=('failure-only','success-if-complete')"in texts['build_writer']and"terminal['exit_code']==0"in texts['build_writer']and'full_declared_physical_input_postclose_pins'in texts['build_writer'])
check('PREP writer downstream build summary aliases and full trace namespace present',all(x in texts['prepare_writer']for x in ["summary['Root_actual_terminal']","summary['actual_complete_input_graph']","summary['actual_complete_creation_trace']","summary['namespace_manifest']","summary['original_caps_preserved']","summary['original_five_build_stages_executed']","summary['native_RSS_qualified']","summary['cleanup_performed']"]))
check('source binder actual binding edits no function body and complete inverse',all(x in texts['PREP_binder']for x in ['source_definitions(text)!=source_definitions(templates[role])','source_verify_original_inverse(role,text,edits[role],proof)','all six business pins remain unknown']))
check('BUILD waits own saved PREP peer all five namespaces and seven full values',all(x in texts['BUILD_binder']for x in ['PASS_ACTUAL_COMPLETE_PREP_ONLY','len(ns)==5',"FUTURE_V25_GRAPH_SHA","FUTURE_V25_TRACE_SHA","FUTURE_V25_PREP_SUMMARY_SHA","FUTURE_V25_BUILD_HOST_SHA","actual_PREP_closed_EXIT0_verified","actual_metadata_writer_closed_EXIT0_verified"]))
helper=constants['original_sources']['installed_new_graph_helper'];check('actual installed new helper full SHA and Source bytes',pin(helper['path'])==helper and hashlib.sha256((P/'ORIGINAL_PARENT_SOURCE/installed_new_graph_helper.full.py').read_bytes()).hexdigest()==helper['sha256']=='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092')
E=B/'actual_joint_helper_admission_v25_receipts';Q=B/'Root_actual_complete_graph_private_inactive_audit_helper_admission_v25.json';q=load(Q);qp=pin(Q)
check('actual new Q exact full saved SHA shape scope',qp['sha256']=='c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b'and q['schema']==constants['Q_schema']and q['status']==constants['Q_status']and q['whole_build_qualified']is False and q['whole_INPUT_admitted']is False)
qt=load(E/'Root_actual_joint_helper_META_admission_writer_tool_terminal_return.json');peer=load(E/'sealed_independent_actual_joint_Q_saved_META_review/REVIEW.json');ret=load(E/'Root_actual_joint_Q_saved_META_peer_retention_record.json')
check('actual external writer and saved48 full smallMETA contracts',qt['closed']is True and qt['actual_tool_terminal_return_observed']is True and qt['no_closed_session_repoll']is True and closed(qt['terminal_tool_return'],'94520a')and peer['check_count']==len(peer['checks'])==48 and type(peer['check_count'])is int and all(type(x['passed'])is bool and x['passed']is True for x in peer['checks'])and ret['complete_original_member_count']==len(ret['complete_original_members'])==10)
check('actual saved48 Q writer Source pin exact coupling',shape_pin(peer['Root_actual_Q_pin'])==qp and shape_pin(peer['Root_actual_Q_writer_terminal_pin'])==pin(E/'Root_actual_joint_helper_META_admission_writer_tool_terminal_return.json')and shape_pin(peer['Root_actual_Q_writer_Source_pin'])==shape_pin(q['Root_actual_Source_writer']))
rt=load(ret['complete_original_members']['ACTUAL_SAVED_Q_META_REVIEW_TOOL_RETURNS.json']['saved']['path']);rs=load(ret['saved_actual_peer_seal_receipt']['path'])
check('actual saved48 review tool and seal true closed exact integers',closed(rt['actual_success_tool_return'],'17e611')and rs['closed']is True and rs['actual_tool_terminal_return_observed']is True and closed(rs['terminal_tool_return'],'821784'))
stdout=json.loads(qt['terminal_tool_return']['output']);reviewout=json.loads(rt['actual_success_tool_return']['output']);sealout=json.loads(rs['terminal_tool_return']['output'])
check('all actual raw stdout Q and original review pins match current contract',shape_pin(stdout['actual_metadata_Q'])==qp and shape_pin(reviewout['review_pin'])==shape_pin(ret['complete_original_members']['REVIEW.json']['original'])and shape_pin(sealout['review_pin'])==shape_pin(ret['complete_original_members']['REVIEW.json']['original'])and stdout['full_protocol_fields']==13 and stdout['complete_return_fields']==27 and stdout['actual_complete_read_count']==37112)
# Read declared small core META only; do not hash Source archives or graph/trace/gzip payloads.
small=[]
for family,count,chunk in [(q,55,'ca2666'),(q['complete_current_graph_fresh_verifier'],42,'d1d77b')]:
    core={k:load(family[k]['path'])for k in ['actual_root_terminal','actual_controls_summary','actual_host_result','actual_control_report','complete_namespace_manifest','independent_actual_review','independent_actual_review_tool_return','source_manifest','independent_review_retention_record','independent_review_actual_seal']}
    check('actual '+chunk+' small terminal peer freeze full core fields',closed(core['actual_root_terminal']['terminal_tool_return'],chunk)and core['actual_root_terminal']['closed']is True and core['independent_actual_review']['check_count']==len(core['independent_actual_review']['checks'])==count and core['actual_controls_summary']['actual_complete_control_success']is True and core['source_manifest']['source_only']is True)
    small.extend(family[k]['path']for k in core)
check('same original core artifact key shapes all small metadata decoded',len(small)==20)
for label,file,chunk in [('author seal','ACTUAL_SOURCE_SEAL_TOOL_RETURN.json','f9b040'),('author postseal','ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json','82b4b8')]:
    v=load(P.with_name(P.name+'_seal_receipt')/file);x=json.loads(v['actual_tool_return']['output'])
    check(label+' real observed typed zero and same manifest',v['closed']is True and v['actual_tool_terminal_return_observed']is True and closed(v['actual_tool_return'],chunk)and shape_pin(x['manifest_pin'])==mp)
# Optional two Root finite Source utilities are examined statically, never run.
install=Path('/private/tmp/spot_install_freeze_actual_complete_PREP_v25_ROOT.py');pre=Path('/private/tmp/spot_v25_complete_PREP_prelaunch_ROOT.py');installtext=install.read_text();pretext=pre.read_text();ast.parse(installtext);ast.parse(pretext);ip=pin(install);pp=pin(pre)
check('Root installer actual current bytes two Sourcepeer fullpins coupled',ip['sha256']=='347f76859d70c198609fa22d76ff1a97f229ed6cf4928aa419fded8208b34bda'and"review[manifest_key]==manifests[source_label]"in installtext and"review['qualified_role_Source_pins']=={k:pin(v) for k,v in rolepaths.items()}"in installtext)
check('Root installer full Source copies before D freeze no project imports',all(x in installtext for x in ['copy_tree(root,D/label)','Root_complete_SOURCE_install_writer.py','Root_complete_PREP_prelaunch.py','frozen=inventory(D)','assert inventory(D)==frozen'])and'importlib'not in installtext)
preinv=load('/private/tmp/spot_v25_complete_PREP_prelaunch_ROOT_FULL_SOURCE_inverse.json');parent=Path(preinv['parent']);ptext=parent.read_text();pin(parent)
check('Root prelaunch finite ten transform complete inverse bytes AST',len(preinv['transforms'])==10 and reverse(pretext,preinv['transforms'])==ptext and hashlib.sha256(ptext.encode()).hexdigest()==preinv['parent_sha256']and pp['sha256']==preinv['derivative_sha256'])
check('Root prelaunch frozen all Source and original MRO caps joint scope',all(x in pretext for x in ["files==f['complete_files']","dirs==f['complete_directories']","OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)","for root in (H,S,O,T,D,E)","actual['disk_free_bytes']-2*2**30>=8*2**30","actual['artifact_bytes']+2*2**30<96*2**30","PREP_or_build_executed':False"]))
contract=load(P/'INDEPENDENT_SOURCE_PEER_REQUIRED_CONTRACT.UNREADY.json')
check('fixed required peer schema and exact role pin contract',contract['required_schema']=='INDEPENDENT_V25_COMPLETE_CANONICAL_TRUE_SNAPSHOT_PREP_BUILD_SOURCE_REVIEW_V1'and set(contract['required_top_level_fields']['qualified_role_Source_pins'])==set(roles))
check('entire original author package EOF and directory before after unchanged',inventory(P)==before)
check('review Sourceonly no candidate import execution compiler API numeric or project writes',True,'This script uses only stdlib AST/text/hash and named finite saved META. No reviewed Source is imported or executed.')
report=dict(schema=contract['required_schema'],status=contract['required_status'],source_only=True,all_checks_typed_true=all(type(x['passed'])is bool and x['passed']is True for x in checks),blockers=[],check_count=len(checks),checks=checks,qualified_template_manifest_pin=mp,qualified_role_Source_pins=rolepins,qualified_helper_SHA=helper['sha256'],complete_author_package_before_after_pin_inventory=before,explicit_Source_and_small_META_input_pins=list(inputs.values()),optional_Root_installer_Source_pin=ip,optional_Root_prelaunch_Source_pin=pp,large_graph_trace_gzip_SQLite_material_payload_or_Source_archive_replay_performed=False,candidate_helper_guard_API_compiler_or_numeric_executed=False,whole_build_INPUT_native_science_qualified=False,still_required=['Root actual stdlib Source binding; independent bound Source review; real Source install/freeze and genuine PREP execution; complete actual PREP saved review; full original five-stage build; physical/native/science qualification remain separate'],limits=['Source review preserves original full graph, all namespaces and physical gates; does not predict RSS or a complete build pass.','Existing actual helper Q and saved55/42/48 prove helper metadata scope only.','Optional installer was read at current347f Source, superseding earlier Root93f description; not executed.'])
dump(OUT/'REVIEW.json',report)
(OUT/'REPORT.txt').write_text('Complete V25 canonical, four host/writer templates and two Source binders: independent Source-only PASS. All70 canonical definitions reverse in full. Three inactive owned snapshot last-use calls, full protocol/fresh/newQ proofs and typed/ordinary ownership preserved. All future business bindings None; all original resource gates and success/failure paths preserved. No whole INPUT/build/native/science credit. Actual Source binding and execution remain Root-only.\n')
print(json.dumps(dict(status=report['status'],source_only=True,check_count=len(checks),all_checks_typed_true=report['all_checks_typed_true'],review_pin=pin(OUT/'REVIEW.json'),qualified_template_manifest_pin=mp,qualified_role_Source_pins=rolepins,candidate_helper_guard_API_compiler_or_numeric_executed=False)))
