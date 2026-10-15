from pathlib import Path
import ast,difflib,hashlib,json,time,os
start=time.monotonic()
OUT=Path(__file__).parent
PARENT=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_saved_reaction_ledger_sources/saved_reaction_diagnostic_host.py')
PARENT_SHA='3064dbf8c2a332d456d2d892b55ad424b5086172bada81e55b83ba1966ff647a'
parent=PARENT.read_text();assert hashlib.sha256(parent.encode()).hexdigest()==PARENT_SHA
planpath=Path('/private/tmp/axmat_saved_source_phase_READY_wiring_SOURCE_only_20261010_u_k9f0xa/WIRING_PLAN.json')
assert hashlib.sha256(planpath.read_bytes()).hexdigest()=='bd86427d38677730da4738ddf9a6ac7fd43610a0075dbd760eb2ee3860db671e'
plan=json.loads(planpath.read_text())
helper=(OUT/'host_source_helpers.fragment.txt').read_text()
source=parent;changes=[]
def replace(before,after,count=1):
 global source
 assert source.count(before)==count,(before[:120],source.count(before),count)
 assert before!=after
 source=source.replace(before,after)
 changes.append({'before':before,'after':after,'occurrences':count})
replace('One complete saved reaction/flux diagnostic under the unchanged genuine guard.',
        'One complete saved source-phase diagnostic under the unchanged genuine guard; SOURCE candidate only until Root admission.')
replace('import importlib.util\n','import ast\nimport math\nimport stat\nimport struct\nimport importlib.util\n')
oldconstants='\n'.join(line for line in parent.splitlines() if line.startswith(('HOST=','TARGET=','TARGET_SHA=','OUTPUT=','SOURCE_ARCHIVE=')))
newconstants=(f"HOST=Path({plan['recommended_one_use_host_namespace']!r})\n"
    f"TARGET=Path({plan['canonical_driver_recommended_path']!r})\n"
    f"TARGET_SHA={plan['candidate_READY_source']['sha256']!r}\n"
    f"OUTPUT=Path({plan['fixed_output_namespace']!r})\n"
    f"SOURCE_ARCHIVE=Path({plan['recommended_root_source_archive']!r})\n"
    "ROOT_RECEIPTS=BASE/'actual_saved_source_phase_diagnostic_receipts'\n"
    f"PARENT_HOST=Path({str(PARENT)!r})\n"
    f"PARENT_HOST_SHA={PARENT_SHA!r}\n"
    "CONTRACT_SHA='1eb226b3d02da061c0c8e1750540f925c1ec9f6baf23afbbe0f6b24cd00fb991'\n"
    "IDENTITY_KEYS=('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')")
replace(oldconstants,newconstants)
replace('\ndef main():','\n'+helper+'\ndef main():')
replace("sys.getprofile() is not None:\n", "sys.getprofile() is not None or sys.gettrace() is not None:\n")
oldinput=next(line for line in parent.splitlines() if line.startswith('    inputs=['))
newinput="""    source_before=source_archive_pins(support)
    contract,contract_pin=admitted_input_contract(support,source_before)
    input_metadata_before=metadata_inputs(contract)
    target_observation=metadata_inputs({'evaluator':{'path':str(TARGET)}})['evaluator']
    inputs=[support.pin(TARGET,TARGET_SHA),support.pin(PARENT_HOST,PARENT_HOST_SHA),contract_pin,
            support_pin,support.pin(support.TARGET,support.TARGET_SHA),
            support.pin(support.OUT/'seal.json',SEAL_SHA),support.pin(support.TERMINAL/'terminal_return.json',TERM_SHA)]"""
replace(oldinput,newinput)
replace("        HOST.mkdir()\n", "        if joint_archive_bytes(support)>=ARCHIVE_CAP:raise ValueError('all SOURCE/Root receipt/canonical bytes must fit original compact reserve')\n        HOST.mkdir()\n")
replace("'SAVED_REACTION_DIAGNOSTIC'","'SAVED_SOURCE_PHASE_DIAGNOSTIC'",2)
replace("admission=json.loads(log.read_text());watch=json.loads(watch_path.read_text())", "admission=strict_metadata(log);watch=json.loads(watch_path.read_text())")
first="        report=json.loads((OUTPUT/'result.json').read_text());manifest=json.loads((OUTPUT/'payload_manifest.json').read_text())\n"
last="        if actual!={k:v['sha256'] for k,v in manifest['files'].items()}:raise ValueError('entire actual payload manifest required')\n"
a=source.index(first);b=source.index(last,a)+len(last);oldblock=source[a:b]
newblock="""        input_metadata_after=metadata_inputs(contract)
        require(metadata_inputs({'evaluator':{'path':str(TARGET)}})['evaluator']==target_observation,
                'canonical evaluator literal/target identity changed')
        phase_validation=validate_phase_payload(support,admission,contract,input_metadata_before,input_metadata_after,target_observation)
"""
replace(oldblock,newblock)
replace("archived=support.archive_bytes((HOST,OUTPUT,SOURCE_ARCHIVE))", "archived=joint_archive_bytes(support)")
replace("        for entry in inputs+[hpin,rpin]:\n", "        source_after=source_archive_pins(support)\n        if source_after!=source_before:raise ValueError('whole frozen SOURCE archive changed')\n        for entry in inputs+[hpin,rpin]:\n")
replace("schema='AXMAT_GENUINE_SAVED_FULL_GROUP_REACTION_DIAGNOSTIC_HOST_V1',status='ACTUAL_SAVED_FULL_GROUP_REACTION_DIAGNOSTIC_EXTERNAL_ROOT_REQUIRED'",
        "schema='AXMAT_GENUINE_SAVED_FULL_GROUP_SOURCE_PHASE_DIAGNOSTIC_HOST_V1',status='ACTUAL_SAVED_FULL_GROUP_SOURCE_PHASE_DIAGNOSTIC_EXTERNAL_ROOT_REQUIRED'")
replace("input_sources=inputs,original_helper=hpin", "input_sources=inputs,source_archive_before=source_before,source_archive_after=source_after,all1140_input_outer_metadata_before=input_metadata_before,all1140_input_outer_metadata_after=input_metadata_after,actual_complete_phase_payload_validation=phase_validation,joint_archive_roots=[str(HOST),str(OUTPUT),str(SOURCE_ARCHIVE),str(ROOT_RECEIPTS)],canonical_source_bytes_counted_outside_archive=TARGET.lstat().st_size,original_helper=hpin")
replace("        if support.archive_bytes((HOST,OUTPUT,SOURCE_ARCHIVE))>=ARCHIVE_CAP or time.monotonic()-started>=WHOLE_CAP:", "        if joint_archive_bytes(support)>=ARCHIVE_CAP or time.monotonic()-started>=WHOLE_CAP:")
replace("FAILED_SAVED_REACTION_DIAGNOSTIC_NO_RETRY", "FAILED_SAVED_SOURCE_PHASE_DIAGNOSTIC_NO_RETRY")
restored=source
for change in reversed(changes):
 assert restored.count(change['after'])==change['occurrences'],('inverse',change['after'][:100],restored.count(change['after']),change['occurrences'])
 restored=restored.replace(change['after'],change['before'])
assert restored==parent
parsed=ast.parse(source)
# The normal supervision/import/invocation mechanics remain complete source text.
unchanged_fragments=(
 "helper,hpin=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'axmat_v15_admission_original619')",
 "resource,rpin=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'axmat_v15_admission_real_resource_module')",
 'full,production=helper.modules();helper.guard_admission(full)',
 'full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)',
 "roots=resource.history_roots([str(HOST),str(OUTPUT),str(support.SOURCE),str(support.OUT),str(support.TERMINAL)],support.ART)",
 'resources=resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)',
 'WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=60,60,512,64*2**20',
 'runner=full.OwnRSSSerialExecutor(HOST,remaining,',
 'if type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources:',
 "command=[str(support.PYTHON),'-B',str(TARGET),'--evaluator-sha256',TARGET_SHA,'--out-root',str(OUTPUT)]",
 "runner.execute(HOST/'run','admit',command,STAGE_CAP)",
 "type(watch['returncode']) is not int or watch['returncode']!=0",
 "watch['own_child_only'] is not True or watch['liveness_group_cleanup'] is not True",
 "not 0<=watch['sampled_peak_rss_mib']<RSS_CAP",
 "threads=1,children_at_once=1,retries=0,profile_used=False,supervisor_class_or_MRO_modified=False")
for text in unchanged_fragments:assert text in source,text
assert not any(isinstance(node,ast.Assert) for node in ast.walk(parsed))
for node in parsed.body:
 assert not isinstance(node,(ast.ClassDef,ast.With,ast.For,ast.While,ast.Try)),type(node)
# Static future-only bindings and absent normal output observation.
assert plan['candidate_READY_source']['sha256']=='e4eed9d520499cf15dae35c56adb1b7a3dea54e67e73046dd828ee47a1225fcf'
for path in (plan['recommended_one_use_host_namespace'],plan['fixed_output_namespace']):assert not os.path.lexists(path)
name='saved_source_phase_diagnostic_host.CANDIDATE.py';(OUT/name).write_text(source)
sha=hashlib.sha256(source.encode()).hexdigest()
def write(name,value):(OUT/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
write('FINITE_INVERSE_PROOF.json',{'schema':'AXMAT_SAVED_SOURCE_PHASE_NORMAL_HOST_FINITE_INVERSE_SOURCE_ONLY_V1','parent':{'path':str(PARENT),'sha256':PARENT_SHA,'bytes':len(parent.encode())},'candidate':{'path':str(OUT/name),'sha256':sha,'bytes':len(source.encode())},'finite_replacements':changes,'replacement_count':len(changes),'full_inverse_byte_exact':True,'restored_parent_sha256':hashlib.sha256(restored.encode()).hexdigest(),'normal_supervisor_fragments_unchanged':list(unchanged_fragments),'helper_driver_numeric_imported_or_executed':False,'source_only_AST_parsed':True})
(OUT/'EXACT_PARENT_TO_CANDIDATE.patch').write_text(''.join(difflib.unified_diff(parent.splitlines(True),source.splitlines(True),fromfile='actual_saved_reaction_ledger_sources/saved_reaction_diagnostic_host.py',tofile=name)))
report={'schema':'AXMAT_SAVED_SOURCE_PHASE_NORMAL_HOST_CANDIDATE_SOURCE_REPORT_V1','status':'SOURCE_ONLY_CANDIDATE_NOT_ROOT_ADMITTED_NOT_EXECUTED','candidate_sha256':sha,'candidate_bytes':len(source.encode()),'finite_parent_sha256':PARENT_SHA,'finite_replacements':len(changes),'full_inverse_exact':True,'fixed_canonical_driver':plan['canonical_driver_recommended_path'],'fixed_canonical_driver_sha256':plan['candidate_READY_source']['sha256'],'fixed_HOST':plan['recommended_one_use_host_namespace'],'fixed_OUT':plan['fixed_output_namespace'],'fixed_D':plan['recommended_root_source_archive'],'fixed_Root_receipts_E':'/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_saved_source_phase_diagnostic_receipts','normal_host_canonical_install_recommended':str(Path(plan['recommended_root_source_archive'])/'saved_source_phase_diagnostic_host.py'),'SOURCE_archive_must_be_frozen_before_whole_actual_run':True,'Root_receipts_must_live_E_not_D_and_joint_counted':True,'original_full1140_contract_inputs_support_pin_called':False,'allow_literal_symlink_to_regular_target_preserved':True,'input_file_payload_SHA_read_only_by_fixed_admitted_child':True,'independent_host_stat_and_full_child_before_after_EOF_SHA_literal_target_fd7id_alias_size_checks':True,'output_full12files_11manifest_5bins_19820160bytes_verified':True,'all370_1800_384_392_three_moments_preserved':True,'word_equality_math_remains_unchanged_in_e4eed_child':True,'AAA_ABA_balance_multiplicity_sourcepartition_sameMG_compilation_identity_qualified':False,'limits_unchanged':{'whole':60,'stage':60,'RSS_MiB':512,'joint_archive_bytes':67108864,'history_bytes':103079215104,'free_bytes':8589934592,'threads':1,'children':1,'retries':0},'archive_scope':['HOST','OUT','entireD','RootE','canonicaldriver bytes outside roots'],'history_scope':'original ebbb complete dynamic ART roots; outside D/E archive jointly counted separately, not illegally inserted into ART-only history roots','resource_feasibility':'estimate only, actual RSS/time/archive receipts required','candidate_imported':False,'candidate_executed':False,'helper_imported':False,'driver_imported':False,'numeric_payload_read':False,'canonical_written':False,'future_actual_host_pin':None,'future_actual_terminal_pin':None,'future_actual_output_pins':None,'source_generation_seconds':time.monotonic()-start}
write('REPORT.json',report)
(OUT/'PREFLIGHT_ADVICE.txt').write_text('SOURCE候选尚未Root准入/实际运行。仅ROOT在V17全build实际关闭后安装driver e4eed与host固定SHA，执行一次。\n\n1. 将作者原包、独立SOURCE审查、READY接线包与本候选/finiteinverse完整归档至D，必须包含SHA锚58d1/a99/1eb/066/738/bd864/410/e4eed；input_contract.json只有一份原完整SHA。host安装D/saved_source_phase_diagnostic_host.py，canonical driver用计划原路径/e4eed。所有D文件在运行开始前冻结，运行凭证写E=B/actual_saved_source_phase_diagnostic_receipts。\n2. HOST与OUT必须同时fresh不存在；主host argv无参数；Root使用固定正常Python3.12 -B，PYTHONOPTIMIZE unset、PYTHONDONTWRITEBYTECODE=1及五个线程环境变量=1。SOURCE-only候选不是一次business retry许可。\n3. 原真实705/38de MRO、619 guard、bc bounded runner与ebbb resource helper完全按成熟3064 host调用。60s whole包含source/fullpin/standardlib contract admission、import、child、cleanup、payload verification与host result；60s stage/512MiB/1thread/1child/0retry不扩大。history96GiB/free8GiB维持原完整ART动态scope。D/E是ART之外路径，不传给只接受ARTdescendant的history_roots。\n4. 64MiB必须联合HOST+OUT+完整D+全部RootE+canonical290156B计数。E若实际另外选路径须在SOURCE候选的finite diff中显式绑定后再准入，不能漏计。host result及Root最终stdout/stderr/actualterminal/independentreview/newreceipts写完后，Root还需再次联合字节计数<64MiB、原history/free检查；不得把结束后的凭证写D改变已冻结source。\n5. host不对1140契约输入用regular-only support.pin；对其literal/target/alias独立stat，通过固定READY source AST与原JSON合同核对每role/path/SHA。child原成熟fresh_hash真正做每input全EOF SHA+literal/target/fd7ID/alias before/after；host完整核对全部1140输出receipt及outer before/after观察，不能以SOURCE observed metadata/SHA claim替代actual。\n6. 仅原typed-word检查通过可授保存work RHS/source phase字一致。完整sourcepartition/compiled byte identity/reactionmultiplicity/fullbalance/AAA/ABA/same-MG reference均仍false，不把科学未通过项改名为通过。\n7. 实际失败保留完整failed receipt，不复用namespace、不扩大cap/门槛。SOURCE预算估算不能代替真实RSS和whole时间测量。\n')
print(json.dumps({'directory':str(OUT),'candidate_sha256':sha,'candidate_bytes':len(source.encode()),'parent_sha256':PARENT_SHA,'finite_replacements':len(changes),'full_inverse_exact':True,'source_only':True,'driver_helper_numeric_imported_executed':False,'numeric_payload_read':False},indent=2))
