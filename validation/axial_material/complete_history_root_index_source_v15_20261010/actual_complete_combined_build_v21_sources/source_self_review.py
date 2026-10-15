import pathlib,json,hashlib,stat,ast
P=pathlib.Path('/private/tmp/axmat_v21_complete_build_host_actual_SOURCE_binding_20261010_9l6eaiab')
def pin(p,sha=None):
 p=pathlib.Path(p);s=p.lstat();i=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns];assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
 b=p.read_bytes();t=p.lstat();assert i==[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
 h=hashlib.sha256(b).hexdigest()
 if sha:assert h==sha,(str(p),h)
 return b,dict(path=str(p),sha256=h,identity=i)
source_pins=[]
def read(ref):
 b,q=pin(ref['path'],ref['sha256']);assert q=={k:ref[k] for k in ('path','sha256','identity')};source_pins.append(q);return b
host,hpin=pin(P/'combined_build_host.py','ebe99a7aaf7abd4e073d0e206bea205344e186d5a3be144a012443f1cd51a196')
proof,ppin=pin(P/'Root_finite_build_host_source_inverse.json');d=json.loads(proof)
assert d['finite_change_count']==len(d['changes'])==21 and d['host_sha256']==hpin['sha256']
cf2,cf2pin=pin(d['parent_path'],d['parent_sha256']);source_pins.append(cf2pin)
rest=host.decode()
for c in reversed(d['changes']):
 assert rest.count(c['after'])==c['count'];rest=rest.replace(c['after'],c['before'])
assert rest.encode()==cf2 and ast.dump(ast.parse(rest),include_attributes=False)==ast.dump(ast.parse(cf2),include_attributes=False)
oldp=d['original_cf2c_to_37d_thirteen_change_inverse'];old,oldpin=pin(oldp['parent_path'],oldp['parent_sha256']);source_pins.append(oldpin)
rest=cf2.decode()
for c in reversed(oldp['changes']):
 assert rest.count(c['after'])==c['count'];rest=rest.replace(c['after'],c['before'])
assert len(oldp['changes'])==13 and rest.encode()==old
for ref in d['checked_source_pins']:read(ref)
summary=json.loads(read(d['actual_Root_closed_PREP_summary']))
terminal=json.loads(read(d['actual_Root_closed_terminal']))
namespace=json.loads(read(d['actual_Root_complete_namespace_freeze']))
assert summary['schema']=='ROOT_V21_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1' and summary['status']=='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD'
tr=terminal['terminal_tool_return']
assert type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr and terminal['closed'] is True and tr['chunk_id']=='e0647a'
assert terminal['initial_tool_return']['chunk_id']=='78a34b' and terminal['initial_tool_return']['session_id']==16256
assert terminal.get('session_repolled_after_close',False) is False
assert summary['Root_actual_terminal']==summary['actual_root_terminal']==d['actual_Root_closed_terminal']
assert d['metadata_binding_parameter_count']==9 and len(d['actual_required_metadata_argv'])==9
argv=d['actual_required_metadata_argv'];assert argv==[
'/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_combined_prepare_v21_receipts/Root_actual_complete_combined_prepare_summary.json',
'21ee531ce1a2032cb2d6fb86fe86603ae1a9bec3300ff982d033248ac9700344',
'830ac8ced4c40156a2126a1844d0b8124fd5b1cdae3fcbe7e51e597a747673cf',
'f0759d38c8cc6c5340968ea6905b9537eeb5f80bafc71a452d76bfb12b58852f',
'80d67cd194eed1d229e46cd5512df9ba4b00954e7f6e7b36dd8ea6902851d6af',
'80a8b58f41ae3c0fb16afc60a6a71ebe308c25314a42dab1a1fd55dd09d6584e',
'7e340a31596aa58518ebde4231bd3542554acb0a4ea1888f1df7ea14bec50dcf',
'd5622ad2b2661a336134cb97a2bbf113bfb76327a467149644e539a0009c2779',
'06fb0e5b3abe6efd38a0656e0b1e3572581ceab018825cd07be3f52683876244']
ns={n['root']:n for n in namespace['namespaces']};assert len(ns)==len(namespace['namespaces'])==5 and namespace['no_build_or_native_credit'] is True
for key,ref in d['actual_output_pins_bound_by_closed_Root_metadata_without_ART_read'].items():
 p=pathlib.Path(ref['path']);assert ns[str(p.parent)]['files'][p.name]==ref
 assert len(ref['identity'])==7 and all(type(x) is int for x in ref['identity']) and stat.S_ISREG(ref['identity'][2]) and ref['identity'][3]==1 and ref['identity'][4]>0
desired=d['actual_output_pins_bound_by_closed_Root_metadata_without_ART_read']
assert desired['actual_source_admission']==d['actual_source_admission_output_pin_from_complete_namespace']
assert [desired[k]['sha256'] for k in ('actual_declaration','actual_source_admission','actual_prep_terminal','actual_complete_input_graph','actual_complete_creation_trace')]==argv[4:]
canonref=d['checked_source_pins'][-1];canonical=read(canonref).decode()
assert canonref['sha256']=='023abc88dd60e89cb49ebacb881f555850b7732149b14caf14503bd135a391e5'
ct=ast.parse(canonical);ht=ast.parse(host)
def assigned(tree,name):
 return next(n for n in tree.body if isinstance(n,ast.Assign) and any(any(isinstance(x,ast.Name) and x.id==name for x in ast.walk(t)) for t in n.targets))
vals={}
for n in ct.body:
 if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
  try:vals[n.targets[0].id]=ast.literal_eval(n.value)
  except (ValueError,TypeError):pass
assert vals['DRAFT_STATUS']=='READY_REVIEWED_V21_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'
future=['FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']
assert all(vals[k] is None for k in future)
labels=ast.literal_eval(assigned(ht,'EXPECTED_LABELS').value);commands=ast.literal_eval(assigned(ht,'EXPECTED_COMMANDS').value)
assert labels==['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit'] and len(commands)==5
baseline,bpin=pin(P/'frozen_parent_combined_build_host_v20.py','d5fa7063b8031d5efecd50e157062e7b2faae771788fe105f2d8486d37f19128')
bt=ast.parse(baseline);bcommands=ast.literal_eval(assigned(bt,'EXPECTED_COMMANDS').value)
expected_commands=json.loads(json.dumps(bcommands).replace('combined-runtime-v20-20261010','combined-runtime-v21-20261010').replace('prepare_sender_window_root_index_graph_trace_table_combined_runtime_v20.py','prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.py').replace('5459b71f65f0dcd61e753648f7b93285beb65e3c194498e3da74793d94516421',argv[4]).replace('a92a3149791b99a88d4938d2c32e592de0f4b7c43083b6ba245df3138a222533',argv[6]))
assert commands==expected_commands
oldcanonical_path=pathlib.Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v20.py')
oldcanonical,ocpin=pin(oldcanonical_path,'566939e3fbc7eddcc2b5af324a6dd11e97f83b033994e36389f7819d06084de3');source_pins.append(ocpin)
oldct=ast.parse(oldcanonical)
cstage=next(n for n in ct.body if isinstance(n,ast.FunctionDef) and n.name=='stage_commands')
ostage=next(n for n in oldct.body if isinstance(n,ast.FunctionDef) and n.name=='stage_commands')
assert ast.dump(cstage,include_attributes=False)==ast.dump(ostage,include_attributes=False)
assert ast.get_source_segment(canonical,cstage)==ast.get_source_segment(oldcanonical.decode(),ostage)
for name in ('NM','OTOOL','OLD','PHYSICAL','DEDUP','TRIM'):
 assert ast.dump(assigned(ct,name),include_attributes=False)==ast.dump(assigned(oldct,name),include_attributes=False)
hsource=host.decode()
needed=[
"runner.execute(HOST/'run','build',command,WHOLE_CAP)",
"full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)",
"support.archive_bytes((HOST,SOURCE,OUT,TERMINAL,SOURCE_ARCHIVE))",
"for entry in inputs+[hpin,rpin]:",
"all exact five original supervised commands must pass once",
"complete raw metadata before all identity gates required",
"complete original OUT seal required",
"all original actual post-seal budget tails required",
"original single-thread Python required",
"fresh one-use whole build host required; no retry",
"no prior build execution or build retry allowed"]
assert all(x in hsource for x in needed)
assert "WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30" in hsource
assert "dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7" in hsource and "29ac1abd0df3ff9d1d71a3239842e1c97cb2619cc4627292b0d25f6e16218bb2" in hsource
assert "combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py" in hsource and "Root_actual_complete_graph_private_verifier_helper_admission_v21.json" in hsource
assert "bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6" not in hsource and "d49036e0a0fd396dd9550e81fd310b74442a867e7a4cc36ff2b16bf70a9c6bf8" not in hsource
gen,gpin=pin(P/'generate_build_host.py','d5d206232ad42927e235b0f947bd893b28eafcfcb593369b4dba7adb96a640e8')
gp=json.loads((P/'source_inverse_proof.json').read_bytes());gparent,gppin=pin(P/'frozen_parent_generate_build_host_v20.py','c8cf1a7c0a3e60c4cfb2edfc88e496e9fedccb25330c11c5bbb7421d23c52f72')
rest=gen.decode()
for c in reversed(gp['changes']):assert rest.count(c['after'])==c['count'];rest=rest.replace(c['after'],c['before'])
assert rest.encode()==gparent and len(gp['changes'])==15
for ref in source_pins:
 _,again=pin(ref['path'],ref['sha256']);assert again==ref
assert pin(P/'combined_build_host.py')[1]==hpin and pin(P/'Root_finite_build_host_source_inverse.json')[1]==ppin
review=dict(schema='AXMAT_V21_ACTUAL_ROOT_PREP_BOUND_COMPLETE_BUILD_HOST_SOURCE_SELF_REVIEW_V1',status='SOURCE_ONLY_BOUND_HOST_REVIEW_PASS_PENDING_INDEPENDENT_REVIEW_AND_REAL_BUILD',host=hpin,generator=gpin,proof=ppin,host_full_byte_and_AST_inverse21_to_cf2c_and13_to37d_exact=True,generator_full_byte_inverse15_to_c8cf_exact=True,Root_actual_closed_PREP_metadata_bound=True,Root_actual_terminal=tr,nine_required_metadata_arguments_exact=argv,all_prepared_five_outputs_exact_path_SHA7ID_match_same_complete_Root_namespace=True,source_admission_in_SOURCE_dynamic_inventory=True,canonical_installed_READY_source=canonref,all_six_future_business_pins_None=True,new_helper_and_joint_Q_four_literals_bound=True,all_five_original_stage_labels=labels,all_five_original_static_commands_exact_version_and_real_PREP_pin_retarget=True,canonical_stage_commands_original_function_bytes_and_AST_unchanged=True,canonical_original_NM_OTOOL_OLD_PHYSICAL_DEDUP_TRIM_AST_unchanged=True,actual_prepared_declaration_or_graph_or_trace_ART_payload_not_read=True,actual_declaration_command_values_not_independently_parsed_by_this_SOURCE_review=True,original_raw_four_logs_before_identity_all5watch_fullseal_runtimeidentity_4tails_preserved=True,dynamic_build_SOURCE_archive_and_prepared_SOURCE_TERMINAL_inventories_preserved=True,genuine_support_guard_MRO_resources_outer1800_inner600_RSS512_archive2GiB_history96GiB_free8GiB_1thread1child0retry_unchanged=True,fresh_failed_v20_namespaces_not_reused=True,all_explicit_SOURCE_and_Root_META_input_pins_fresh_full_EOF_SHA7ID_before_after_equal=True,input_source_and_Root_meta_pins=source_pins,scope='Source-only render and author self-review; Root PREP saved evidence independent admission and third-party build SOURCE review remain external requirements',normal_host_executed=False,project_guard_helper_driver_or_canonical_API_imported=False,business_or_numeric_or_build_executed=False,ART_glob_or_payload_read=False,closed_sessions_repolled=False,project_D_E_or_canonical_or_original_sealed_package_written=False,whole_build_INPUT_native_AAA_ABA_or_physics_qualified=False)
(P/'SOURCE_SELF_REVIEW.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
(P/'SOURCE_SELF_REVIEW.txt').write_text('仅标准库 Source render 与作者有限源码自审通过，未执行生成后的 host / 项目 API / guard / 构建 / 数值。\n新 host ebe99a7aaf7abd4e073d0e206bea205344e186d5a3be144a012443f1cd51a196：21 项整字节及 AST 逆回 cf2c，再原13项逆回37d；generator15项全字节逆回c8cf。\n九个真实 argv 与同一 Root V21 PREP summary/整数0closed终端/完整五namespace逐项匹配，五prepared输出path/fullSHA/typed7ID完整；source_admission来自SOURCE目录。\n真实canonicalREADY Source023abc已安装，六未来业务pins仍None。new helperdc01/new联合Q29ac四literal均绑定，原component/support/guard/MRO/资源不变。\n五stage和静态commands完整等于原V20命令必要版本及真PREP pin retarget；canonical stage_commands函数与旧Source整字节及AST一致，NM/OTOOL/OLD/PHYSICAL/DEDUP/TRIM全AST一致。此Source自审未解析ART declaration命令值，运行时仍保留原全部exact5commands gate。\nouter1800/inner600/RSS512/联合HOST+SOURCE+OUT+TERMINAL+buildSourceArchive2GiB/history96GiB/free8GiB/1thread/1child/0retry，完整raw4logs-before-identity/5watch/fullseal/runtimeidentity/4tails与动态SOURCE inventory原样。\nSource与Root META显式输入完整EOF/SHA/7ID前后不变；原sealed设计包、D/E、canonical和ART未改。\nRoot需另行完成真实PREP保存独审、第三方Source review、全SOURCE安装freeze和真正一次新目录build；此包不授build/wholeINPUT/native/AAA/ABA/physics资格。\n复制设计包旧sealed_manifest只用于lineage，新完整绑定清单另封存。\n')
print(json.dumps({'directory':str(P),'host_sha256':hpin['sha256'],'self_review_sha256':hashlib.sha256((P/'SOURCE_SELF_REVIEW.json').read_bytes()).hexdigest(),'status':review['status'],'full_host_inverse_hunks':21,'full_generator_inverse_hunks':15,'Source_and_Root_META_pins':len({r['path'] for r in source_pins}),'ART_payload_read':False,'normal_host_executed':False}))
