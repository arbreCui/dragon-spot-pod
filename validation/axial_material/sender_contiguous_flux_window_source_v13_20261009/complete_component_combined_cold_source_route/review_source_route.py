"""Read immutable current sources and record a plan; no business execution."""
import ast,hashlib,json
from pathlib import Path
D=Path('/private/tmp/axmat_v13_sender_fun_window_source_route_readonly_20261009')
R=Path('/Users/wen/spot/validation/axial_material')
C=R/'prepare_qualified_AB_rank1_factor_cache_cross_group_identity_key_delta_production.py'
G=R/'prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.py'
F=R/'prepare_owned_specs_identity_key_delta_graph_table_cold_runtime_v12.py'
S=Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-rank1-factor-cache-build-admission-20261007/FLU2DR64.f')
expected={C:'f136baab5047a8727cfd2c0abb5399acf617c25c4f4e7692242419e6f9daef4e',
 G:'5af1feebc7d40549750e1daec6148ae073a4c85c1eb3242485e6d9e80826861b',
 F:'7037cf10b98e0f5098a87bb87808940a85132abce48e6156db7b136eddcfbf71',
 S:'bb901bfed9a4199a5b4c98c58c93bf3b3dda597fd2047bfed6d267c8dcadac81'}
source_pins=[];function_inventory={}
for p,sha in expected.items():
 actual=hashlib.sha256(p.read_bytes()).hexdigest();assert actual==sha
 source_pins.append(dict(path=str(p),sha256=sha,size_bytes=p.stat().st_size))
 if p.suffix=='.py':
  text=p.read_text();t=ast.parse(text);function_inventory[str(p)]={n.name:{'line':n.lineno,'end_line':n.end_lineno,
   'sha256':hashlib.sha256(ast.get_source_segment(text,n).encode()).hexdigest()}
   for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
ct=C.read_text();gt=G.read_text();ft=F.read_text();sender=S.read_text()
for text in ('unchanged_sender_object=pin(SENDER_OBJECT)',"sole_new_production_overrides=[\"SPOT1P64.o\"]",
 "identity[\"inherited_sender_override\"] != pin(SENDER_OBJECT)"):
 assert text in ct,text
assert "sender=OLD/'build/FLU2DR64.o'" in gt
assert "sole_object_changes=['SPOT1P64.o','SPOASM.o']" in gt
assert 'SUBROUTINE FLUSP64(' in sender and 'FUN(NUN,NGRP)' in sender and 'F2(NUN,NGEFF),S2(NUN,NGEFF)' in sender
assert sender.count('CALL FLUSP64(')==4
plan=[
 {'step':1,'scope':'native source patch only','required':[
  '固定bb901完整旧FLU2DR64.f为祖先，给新完整sender源、逐区域diff和完整逆向；暂不赋实际控制或RSS成功。',
  'SPOT1P64 top0800、祖先5e/343e、白边界、算术表达式与循环/归约次序保持原层证据；sender新增proof为独立层，不改祖先sender_changed=False子proof。',
  '最终窗口API/eligibility/shape由实际native patch决定；保持外部生产调用约定或完整证明每个显式caller变更。']},
 {'step':2,'scope':'fresh V13 component','required':[
  '全新SOURCE/OUT/TERM/FAMILY/schema，UNKNOWN实际success pins None、UNREADY；旧sender对象74b仅作为historical input。',
  'prepare_build L673：按原-O2/-march=native/-ffp-contract=off等flags私有重新编译SOURCE/FLU2DR64.f→OUT/build/FLU2DR64.o；原SPOT0800及三个cache候选/reference源也全部重编并执行。',
  '生产link显式替换SPOT1P64.o和FLU2DR64.o，并改输出；两个候选均在libDragon.a之前。完整token逆向回原92链接，拒绝旧sender或unit/reference sender进入生产。',
  'L647/663/673/801/1671/1719/1954：声明、实际命令、标签、runner顺序、watch、audit、seal、external terminal、admission同步新全阶段计数。原68全部实际重跑，新sender compile/wrapper build/execute另加；68不是新总数。',
  '可以保持原cache control_audit L1363与完整30-count原范围；新增sender_control_audit及全局stage_count。若counts总阶段字段扩展，显式记录original68 retained与new total，不能把旧68自称new all。',
  'source_admission L757和runtime/build_identity L1740新增candidate_sender_source/object/patch/control原始证据，sole overrides变SPOT1P64+FLU2DR64。binary_audit L1626增加新sender nm/otool/DWARF单位身份、_flu2dr64_/_flusp64_唯一实际定义及生产reference排除。',
  'production_admission L1954重新验完整new SOURCE/OUT sealed namespace、所有old68+new stages、真实拒绝23、完整Root exit0及4tail；公开new sender源/对象/proof/control descriptors。旧corrected_sender_retained字面须明确其含义只是数学修正继承，不能继续宣称旧sender byteexact。',
  '1800总/600阶段/512MiB/2GiB reservation/history96GiB/free8GiB/thread1/child1/retry0及genuine OwnRSS/MRO不改。']},
 {'step':3,'scope':'new real sender wrapper controls','required':[
  '原68是cache/direct-kernel controls，不覆盖sender窗口；旧source_factor control_source L404仅抽两source arithmetic块，也不覆盖FUN工作区。',
  'fresh wrapper exe必须执行从真实candidate sender编译/提取且完整body有字节来源证明的变更窗口路径，old reference只允许独立unit符号重命名；toy arithmetic或Fortran自称PASS不足。',
  '按actual patch eligibility覆盖empty/single(first middle last)/sparse/all-active/不同连续调用窗口；四个真实FLUSP64 caller形态中适用路径均要覆盖。',
  '保留ILEAK0和3、B2zero/nonzero及KEYFLX/MAT/IMERG zero跳过分支；inactive FUN列、SUN/FLUOLD及原caller FLUX planes原bits保持，活动FUN结果与旧完整reference逐位相等。',
  '包含原真实receiver fixture集成；若dispatch stub用于窗口unit测试，明确仅为dispatch范围，另保留原68真实kernel+wrapper到实际receiver路径验证，不能把stub当完整FLU。',
  '归档固定input、old/full原raw结果、新raw结果、actual allocated/bounds/alias-workspace证据和全stage stdout/watch，再由独立Python读取逐位审核。仅声明缩小shape不能证明无隐式数组copy或生产RSS。']},
 {'step':4,'scope':'fresh V13 combined','required':[
  'trim_component_contract L455、input L593和record L679接完整new component三参数API，全sender descriptors/sourceproof/control/expanded stages，而非按旧factor-label授资格。',
  'combined_link_command L308加入旧FLU2DR64→new实际sender唯一token替换；prepare_build L841不再OLD sender；调用L804/886/974、objects L847–848、binary L956、admission L1092/sole_object_changes同步。',
  '生产变化集合为SPOT1P64/SPOASM/FLU2DR64；selector/archives/flags/libs顺序保持，完整inverse回old92。新sender本体和全部control证据进入current_new_owned_paths L1366/完整graph所有owners。',
  '新SOURCE/OUT/TERM/PREFIX，真实component pins仅在new component actual0后绑定；全新的五stage link/metadata/audit+admit0及4tail后，才提供combined运行input。',
  '保留V12 graph-table helper e8f纯lossless storage及完整whole INPUT graph/7body/alias/absence/resource scopes，不提高64MiB readcap或滤掉输入。']},
 {'step':5,'scope':'fresh whole INPUT standalone then cold','required':[
  'standalone fresh host/intake root/recorder retarget新factory；new DECL/PREP/SEAL/RUN/HOST/API_RETURN/descriptors/counts/inventory未知None，旧65fc durable是历史输入，不能作为V13返回。',
  '原P12 intake1800/600/512/thread1/child1/retry0、完整7 INPUT phases/MRO/图不改；实际host0完整return和新durable完整10files后做whole INPUT独审，新counts按事实derive。',
  '新C/B/F与cold SOURCE/WORK/CONTROL_TERM/COLD_TERM完全fresh；C完整source_and_controls/paths检新sender proof，B新完整10map/ns/graph/helpers/Csha/counts，F只绑定已实际见证事实。',
  'cold P14、analysis P12、八预算120/4200/600/300/4200/120/100/43200、ownRSS512、controls60/120、单线程单child零retry、正常module/class与无overlay保持；7futurecold、FORMAL_FACTORY_SHA、BINDING_CONTROLS_ACTUAL未知None。',
  '真实declare/prepare/binding+new positive/oversize/short controls/Root TERM后finalize，新的唯一AAA尝试。V12失败目录永久NORETRY，只保留failure历史input。',
  '链接/unit/input通过不授native RSS/完整耦合/独立精度/ABA；仍要求actual native<512、完整AAA收敛及原八精度gate，再解除ABA guard。']}
]
preserve=['patch_admission','cache_accounting','production_cache_shape_forecast','control_audit','stage_outcome_valid',
 'read_raw_fixture','raw_inventory','check_watch','external_terminal_admission']
retained={name:function_inventory[str(C)][name]for name in preserve if name in function_inventory[str(C)]}
report={'status':'SOURCE_ONLY_MINIMAL_ROUTE_REVIEW_COMPLETE','no_new_business_source_generated':True,
 'business_import_call_compile_run':False,'Root_session_poll':False,'project_write':False,
 'baseline_source_pins':source_pins,'critical_blocker':'Current component and combined both explicitly retain old sender object; retargeting trim identities alone leaves V13 unimplemented.',
 'sender_actual_source_patch_not_yet_reviewed':True,'new_success_pins_all_unknown':True,
 'minimum_full_route':plan,'candidate_inverse_required':{
  'native_sender':'complete bytes inverse to bb901 ancestor with finite classified edits',
  'new_component_factory':'whole source inverse to f136 with finite identity/build/link/sender gates edits; numerical cache model/fixtures/source proofs byteexact',
  'new_combined_factory':'whole source inverse to5af; added sender link/source/gate and identities only; graph/math/scope/budget unchanged',
  'new_cold_C_B_F_host':'whole source inverse toV12 current frozen sources with explicit identity and new sender evidence gates only; exact functions/templates/MRO/budgets outside classified regions'},
 'cache_body_functions_expected_retained':retained,'baseline_top_level_function_byte_inventory':function_inventory,
 'native_RSS_verified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False}
q=D/'REPORT.json';q.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':report['status'],'report':str(q),'report_sha256':hashlib.sha256(q.read_bytes()).hexdigest(),
 'no_business_execution':True,'new_success_pins_bound':0},sort_keys=True))
