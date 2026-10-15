from pathlib import Path
import ast,hashlib,json,stat,tempfile
D=Path('/private/tmp/axmat_v20_normal_PREP_host_source_binding_20261010')
W=Path('/private/tmp/axmat_v20_PREP_metadata_writer_source_binding_20261010')
PREV=Path('/private/tmp/axmat_v20_complete_strict_JSON_raw_last_use_independent_SOURCE_review_20261010_q9gayqpd')
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
H=D/'combined_prepare_host.py'
PH=B/'actual_complete_combined_prepare_v19_sources/combined_prepare_host.py'
WR=W/'write_actual_prepare_terminal.py'
PW=B/'actual_complete_combined_prepare_v19_receipts/write_actual_prepare_terminal.py'
READY=Path('/private/tmp/axmat_v20_complete_READY_source_binding_20261010/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v20.py')
fixed={
H:'a9d4a1eadae7f6f346138029ea4bbd5e9a5c26c0b5efbb8d256c08b06e757de1',
PH:'f5c947297b3bd0a82b2e76099d9d8412892455c37bef4034d71b4157ad098580',
D/'Root_finite_host_source_inverse.json':'12d6b5b7033e0a782bb638b682bf455f3fe2a5361e3465371b9c0d756a328ffc',
D/'Root_bound_SOURCE_manifest.json':'4a8615febac1838bd019c75404e33a33e46f3d8aec2a3857496d29772e6bbdd4',
WR:'af0c633fa31f29517fa5b8d8dbebdd16d7d255a1c3203047ecd79ef02722b539',
PW:'7c69f1479af9a6527c6db3785f97a790269c3a0069a958391fdd467a3802df32',
W/'Root_finite_metadata_writer_source_inverse.json':'47b00b8ffec4ce32ad6d6d48fb193f1aa273fd56888cca4fc2caee644f3c49f2',
W/'sealed_manifest.json':'f03f745149d61300f7774627b26be48cb8c5dde64b7c9e7686cdc8d0c3b6d439',
READY:'566939e3fbc7eddcc2b5af324a6dd11e97f83b033994e36389f7819d06084de3',
PREV/'REVIEW.json':'a8377b1b5413bad1405676c11b8c1b5e3883f7a439c4b963ba00ff77024af010',
PREV/'sealed_manifest.json':'dde6d9472dfb9371a1c598a37ce888d7db3dd8b139385856666529bfd3374bfa',
}
data={};pins={}
def readpin(p,h):
 p=Path(p);assert '/validation/artifacts/' not in str(p)
 a=p.lstat();assert stat.S_ISREG(a.st_mode) and a.st_nlink==1
 b=p.read_bytes();z=p.lstat()
 id7=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 assert id7(a)==id7(z) and hashlib.sha256(b).hexdigest()==h,(str(p),'whole pin')
 return b,dict(path=str(p),sha256=h,identity=id7(a))
for p,h in fixed.items():data[p],pins[p]=readpin(p,h)
hm=json.loads(data[D/'Root_bound_SOURCE_manifest.json'])
wm=json.loads(data[W/'sealed_manifest.json'])
assert len(hm['members'])==8 and len(wm['members'])==3
for root,manifest,mp in ((D,hm,D/'Root_bound_SOURCE_manifest.json'),(W,wm,W/'sealed_manifest.json')):
 actual_files={str(x) for x in root.iterdir() if x.is_file()}
 assert actual_files=={r['path'] for r in manifest['members']}|{str(mp)}
 for r in manifest['members']:
  p=Path(r['path']);assert p.parent==root
  b,z=readpin(p,r['sha256']);assert z==r
  if p in pins:assert pins[p]==z
  else:data[p]=b;pins[p]=z;fixed[p]=r['sha256']
 assert manifest['SOURCE_only'] is True and manifest['business_executed'] is False
hp=json.loads(data[D/'Root_finite_host_source_inverse.json'])
wp=json.loads(data[W/'Root_finite_metadata_writer_source_inverse.json'])
ht=data[H].decode();pt=data[PH].decode();wt=data[WR].decode();pwt=data[PW].decode()
for t in (ht,pt,wt,pwt,data[READY].decode()):ast.parse(t)
assert hp['factory_sha256']==fixed[READY] and hp['factory_candidate']==str(READY)
assert hp['host_sha256']==fixed[H] and hp['host_candidate']==str(H)
assert hp['parent_host']==str(PH) and hp['parent_host_sha256']==fixed[PH]
assert len(hp['changes'])==9
inv=ht
for r in reversed(hp['changes']):
 assert r['occurrences']==1 and inv.count(r['new'])==1
 inv=inv.replace(r['new'],r['old'],1)
assert inv==pt
assert wp['parent']==pins[PW] and wp['candidate']==pins[WR]
assert len(wp['finite_edits'])==3 and sum(r['count'] for r in wp['finite_edits'])==12
winv=wt
for r in reversed(wp['finite_edits']):
 assert type(r['count']) is int and winv.count(r['new'])==r['count']
 winv=winv.replace(r['new'],r['old'],r['count'])
assert winv==pwt and wp['full_byte_inverse_sha256']==fixed[PW]
class NormalizeWriter(ast.NodeTransformer):
 def visit_Constant(self,n):
  if isinstance(n.value,str):
   n.value=n.value.replace('v20','v19').replace('V20','V19').replace(fixed[READY],'34efcc340b87257929e9d4cb06631455549327436d2bbdc5561639b6535e140b')
  return n
assert ast.dump(NormalizeWriter().visit(ast.parse(wt)),include_attributes=False)==ast.dump(ast.parse(pwt),include_attributes=False)
caps=dict(whole_wall_cap_seconds=1800,stage_wall_cap_seconds=600,rss_mib=512,archive_reserve_bytes=2*2**30,history_bytes=96*2**30,min_free_bytes=8*2**30,threads=1,children=1,retries=0)
for k,v in caps.items():assert hp[k]==v
for fragment in ("WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30","helper.guard_admission(full)","full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)","Path(full.__file__).resolve()!=support.FULL or Path(production.__file__).resolve()!=support.PARENT","resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)","type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources","runner.execute(HOST/'run','prepare',command,STAGE_CAP)","remaining=WHOLE_CAP-(time.monotonic()-started)","[support.pin(p) for p in sorted(SOURCE_ARCHIVE.rglob('*')) if p.is_file()]","if support.pin(entry['path'],entry['sha256'])!=entry","threads=1,children_at_once=1,retries=0,profile_used=False,supervisor_class_or_MRO_modified=False"):
 assert fragment in ht,fragment
assert ht.count('support.archive_bytes((HOST,SOURCE,OUT,SOURCE_ARCHIVE))')==2
assert "SOURCE_ARCHIVE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_combined_prepare_v20_sources')" in ht
assert "TARGET_SHA='"+fixed[READY]+"'" in ht
assert "command=[str(support.PYTHON),str(TARGET),'prepare-build']" in ht
assert "if any(os.path.lexists(p) for p in (HOST,SOURCE,OUT,TERMINAL))" in ht
wchecks={
'strict_root_real_typed_exit0_closed':"actual['closed'] is not True or type(observed.get('exit_code')) is not int or observed['exit_code']!=0 or 'session_id' in observed",
'watch_ownchild_cleanup':"w['own_child_only'] is not True or w['liveness_group_cleanup'] is not True",
'original_PREP_caps':'!=(1800,600,512,2*2**30,1,1,0)',
'all_original_input_revalidation':"for q in h['input_sources']+[h['original_helper'],h['resource_factory']]:",
'full_SOURCE_inventory':"if source_inventory!=d['source_inventory']",
'honest_merged_stdout_scope':"full_stdout_scope='ACTUAL_CANONICAL_CHILD_MERGED_STDOUT_STDERR'",
'honest_outer_stderr_scope':"full_stderr_scope='ACTUAL_EXTERNAL_ROOT_HOST_STDERR'",
'separate_child_stderr_not_invented':"separate_child_stderr_captured=False,independent_child_stderr_empty_verified=False",
'full_joint_scope':"for root in (H,S,O,T,D,E)",
'no_build_credit':"new_five_stage_build_executed=False,whole_combined_INPUT_admitted=False,new_native_transport_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False,goal_complete=False"}
for k,x in wchecks.items():assert x in wt,k
assert "FACTORY_SHA = '"+fixed[READY]+"'" in wt or "FACTORY_SHA='"+fixed[READY]+"'" in wt
assert "if not total<2*2**30:" in wt
for p,h in fixed.items():
 _,z=readpin(p,h);assert z==pins[p]
out=Path(tempfile.mkdtemp(prefix='axmat_v20_bound_normal_PREP_host_and_metadata_writer_SOURCE_append_review_20261010_',dir='/private/tmp'))
review=dict(schema='AXMAT_V20_BOUND_NORMAL_PREP_HOST_AND_METADATA_WRITER_FINITE_SOURCE_APPEND_REVIEW_V1',status='PASS_SOURCE_ONLY_RUNTIME_REQUIRED',prior_sealed_complete_UNREADY_READY_review=pins[PREV/'REVIEW.json'],prior_sealed_complete_review_manifest=pins[PREV/'sealed_manifest.json'],prior_package_never_modified=True,SOURCE_inputs=list(pins.values()),all_whole_SHA7ID_before_after_equal=True,actual_bound_host_a9d4_9_whole_inverse_to_f5c_exact=True,actual_READY5669_PIN_exact=True,parent_f5c_normal_genuine_host_body_guards_MRO_resource_API_caps_unchanged=True,SOURCE_ARCHIVE_all_beforeafter_files_PIN_and_2x_joint_byte_count_preserved=True,host_cap=caps,source_archive_fresh_family20=hp['source_archive'],fixed_prepare_argv_and600_commandcap_and1800_whole_preserved=True,writer_af0_3records12_literal_occurrences_whole_inverse_to7c69_exact=True,writer_AST_exact_after_only_string_literal_normalization=True,writer_preserved_gates={k:True for k in wchecks},bound_host_source_package_full8_members_SHA7ID_verified=True,writer_package_full3_members_plus_manifest_SHA7ID_verified=True,helpers_qualifications_not_repeated=True,project_module_API_guard_resource_host_generator_writer_or_business_numeric_executed=False,ART_raw_or_history_payload_not_read=True,canonical_ART_or_prior_frozen_packages_written=False,new_actual_PREP_build_wholeINPUT_native_AAA_ABA_credit=False,RSS_cause_or_predicted_PASS_claimed=False,no_blocker=True)
p=out/'REVIEW.json';p.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
(out/'REPORT.txt').write_text('V20 真正bound normal PREP host 与metadata writer有限SOURCE追加审查通过，无 blocker。\n前完整c7cf+READY5669审查包已封存，本派生追加包引用前包而不修改它。\n实际host a9d4 全9项整字节inverse回f5c，真实READY5669 SHA精确绑定，原genuineguard/MRO/resource/API/完整范围/固定prepare argv保持。\n原1800 whole/600 PREP child秒、512MiB/2GiB/history96/free8GiB/1thread/1child/0retry保持；SOURCE_ARCHIVE20所有源文件前后PIN与H+SOURCE+OUT+SOURCE_ARCHIVE两次联计保持。\nwriter af0的3条记录共12个字符串literal替换，全inverse回7c69；归一化这些literal后整个AST完全一致。\nwriter真实Root typed EXIT0 closed gate、真实watch/输入前后全pins/SOURCE inventory/全部namespace及caps保持。child stdout+stderr merged与真实外部stderr scope保留，separate-child及独立empty-stderr字段false，未造stderr事实。\n全host binding包8 members及writer3 members+manifest逐全SHA7ID验证并前后不变。未重复helpers实际资格，不import或执行host/generator/writer/API/guard/业务/数值，不读ART raw或历史payload、不写canonical/ART/原封存包。\n这里只是SOURCE许可；V20实际PREP/build/fullINPUT/native/AAA/ABA未得到本审查成功信用，实际RSS原因与是否PASS未知。\n',encoding='utf-8')
print(json.dumps(dict(directory=str(out),review_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),SOURCE_file_count=len(pins),status=review['status'],no_blocker=True,business_executed=False)))
