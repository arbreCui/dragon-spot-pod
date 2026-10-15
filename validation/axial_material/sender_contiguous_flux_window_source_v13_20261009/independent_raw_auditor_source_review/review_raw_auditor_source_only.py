"""Independent STDlib static review, never imports/executes the audited module."""
from pathlib import Path
import ast,hashlib,json,re
D=Path('/private/tmp/axmat_v13_sender_window_raw_auditor_source_independent_review_20261009')
AM=Path('/Users/wen/spot/validation/axial_material')
C=Path('/private/tmp/axmat_v13_flusp64_window_wrapper_control_source_draft_20261009')
AUD=AM/'sender_contiguous_flux_window_controls_audit_v13.py'
expected={AUD:'64262e89bd2adf13260a8d0f643c31d709f84665e5e9223cdd2969ab78a721e1',
 C/'flusp64_window_observer_controls.UNREADY.f90':'053747437865119be4fdd5d8eb466c96a85d8cf22f6d9cdcceebe19bc47352bb',
 C/'CONTROL_CONTRACT.json':'74ecac78a42fd13f5162cc52ad4d96cf6e94abd970406f4fede467696c4dcffd',
 C/'FLUSP64_REFERENCE.f':'52b1db5a5ea73de548e437386798099cdb28b7c28cd98f0de21e949973266043'}
fields=['st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns']
def fresh(p):
    before=p.stat();data=p.read_bytes();after=p.stat()
    a=[getattr(before,k) for k in fields];b=[getattr(after,k) for k in fields]
    assert a==b and after.st_nlink==1 and not p.is_symlink()
    h=hashlib.sha256(data).hexdigest()
    if p in expected: assert h==expected[p],(str(p),h)
    return data,{'path':str(p),'sha256':h,'size_bytes':len(data),'identity':dict(zip(fields,b))}
raw,pin=fresh(AUD);text=raw.decode();tree=ast.parse(text,filename=str(AUD))
pins=[pin];sources={}
for p in expected:
    if p!=AUD:
        b,a=fresh(p);pins.append(a);sources[p.name]=b
contract=json.loads(sources['CONTROL_CONTRACT.json'])
driver=sources['flusp64_window_observer_controls.UNREADY.f90'].decode()
reference=sources['FLUSP64_REFERENCE.f'].decode()
inventory=[]
for node in tree.body:
    if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
        segment=ast.get_source_segment(text,node)
        inventory.append({'name':node.name,'line':node.lineno,'last_line':node.end_lineno,
                          'sha256':hashlib.sha256(segment.encode()).hexdigest()})
assert [row['name'] for row in inventory]==['require','pin','identity','identity_snapshot','same_range','f32_word','f64_word',
 'fixture','layout','read_record','initial_flux','source_and_output','validate_contract','audit_sender_controls']
imports=[]
for node in tree.body:
    if isinstance(node,ast.Import): imports.extend(a.name for a in node.names)
    if isinstance(node,ast.ImportFrom): imports.append(node.module)
assert imports==['hashlib','json','math','pathlib','stat','struct']
assert not any(isinstance(node,(ast.ClassDef,ast.AsyncFunctionDef)) for node in tree.body)
assert not any(isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in {'exec','eval','compile','__import__'} for node in ast.walk(tree))
modes=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign)
           and any(isinstance(t,ast.Name) and t.id=='MODES' for t in n.targets))
assert tuple(c['name'] for c in contract['cases'])==modes and len(modes)==14
assert all(f"case('{name}')" in driver or name in driver for name in modes)
assert 'SUBROUTINE FLUSP64_REFERENCE(' in reference
clauses={
 'header18_and_exact_EOF':('struct.unpack("<18q", stream.read(144))','path.stat().st_size == offsets["size"]','header[:14] == wanted'),
 'signed_float32_words':('struct.unpack("<i", struct.pack("<f", value))[0]','str(len(integers)) + "q"'),
 'whole_title_maps':('stream.read(72) == TITLE','maps = f["active"] + [f["ng"] + 1 - g for g in f["active"]]'),
 'actual_pointer_relation':('caller > 0 and observed > 0','int(caller == observed) == direct','header[14:] == (0, 0, 0, 0)'),
 'full_initial_eight_planes':('for plane in range(1, 9):','for group in range(1, f["ng"] + 1):','(row + group + plane) % 17 == 0'),
 'B1_IR_order_and_duplicateKEY':('for mat, key in zip(mats, keys):','if not key or not mat or not merged[mat - 1]: continue',
     'values[key - 1] = values[key - 1] - float(dif) * float(f["b4"]) * old[key - 1]'),
 'complete_finite_source':('all(math.isfinite(x) for x in values)','stream.read(n * 8) == expected'),
 'full_output_xor_and_negative_zero':('0x800FFFFFFFFFFFFF | 0x3FF0000000000000','(row + col) % 11 == 0','stream.read(n * 8) == wanted_output'),
 'strict_step_order':('[row["step"] for row in case["steps"]] == list(range(1, f["nsteps"] + 1))',),
 'exact_real_executable':('watch["command"] == [str(controls_root.parent / "runtime/flusp64_window_observer_controls"), mode]',),
 'actual_typed_exit_and_caps':('type(watch["returncode"]) is int','watch["rss_cap_mib"] == 512',
     '0 <= watch["sampled_peak_rss_mib"] < 512','0 < watch["wall_cap_seconds"] <= 600'),
 'fullcarry_and_body_equal':('same_range(previous, input_path, offsets["flux"], 8 * 8 * state["nun"] * state["ng"])',
     'same_range(reference, candidate, 144, offsets["size"] - 144)'),
 'allreadonly_planes_inactive_FUN':('if plane != 7:','if group not in state["active"]:',),
 'negative_actual_abort':('MESSAGE in log and "ERROR STOP 92" not in log','and "OBSERVER_ONLY" not in log and not manifest_text'),
 'exact_70_fullbytes':('steps == 22 and observers == 34 and len(all_raw) == 70','== 288241824'),
 'fresh_unique_identity_closed_window':('info.st_nlink == 1','identity(path) == before','identity_snapshot(controls_root) == identities_before'),
 'release_credit_corrected':('"repeated_calls_and_active_set_transition_verified": True','"raw_identity_before_after_equal": True'),
 'no_real_kernel_or_science_credit':('"real_SPOT_receiver_calls_in_this_observer_executable": 0','"native_RSS_verified": False','"AAA_accuracy_qualified": False','"ABA_admitted": False')}
for label,strings in clauses.items():
    assert all(s in text for s in strings),label
assert 'repeated_calls_and_transition_release_verified' not in text
assert 'transfer(source(i,j),0_int64)' in driver and 'ishft(int(ngind(j),int64),20)+int(i,int64)' in driver
assert 'int(z\'800FFFFFFFFFFFFF\',int64)' in driver and "int(z'3FF0000000000000',int64)" in driver
assert 'expected_source(key(i),j)=expected_source(key(i),j)-' in driver
assert 'dble(difhet(imerg(mat(i)),g))*dble(b2(4))*flux(key(i),g,2)' in driver
raw_bytes=sum(r['size_bytes'] for c in contract['cases'] for r in c['raw_files'])
raw_count=sum(len(c['raw_files']) for c in contract['cases'])
assert raw_count==70 and raw_bytes==288241824
for case in contract['cases']:
    nun,ng=case['nun'],case['ngrp']
    for row in case['raw_files']:
        step=int(re.search(r'\.s(\d+)\.',row['name']).group(1))
        nactive=next(s['active_groups'] for s in case.get('steps',[]) if s['step']==step) if not case['negative'] else (8 if 'active' in case['name'] else 0)
        independent=8*(18+ng+14+4+7+4+3*ng+8*nun*ng+2*nactive+nun*nactive)+72
        assert row['size_bytes']==independent
assert contract['cases'][0]['nun']==1800 and contract['cases'][0]['ngrp']==370
assert all(r['size_bytes']==47970208 for r in contract['cases'][0]['raw_files'])
watch_source=Path('/Users/wen/spot/validation/axial_material/qualify_refined_AAA_layered_full.py')
serial_source=Path('/Users/wen/spot/validation/axial_material/production_runner.py')
parent_factory=AM/'prepare_qualified_AB_rank1_factor_cache_cross_group_identity_key_delta_production.py'
for p in [watch_source,serial_source,parent_factory]:
    b,a=fresh(p);pins.append(a)
    if p==parent_factory:
        parent_text=b.decode();assert 'threads=1,numeric_children_at_once=1,retries=0' in parent_text
        assert 'runner = full.OwnRSSSerialExecutor(OUT, remaining, FAMILY, resources)' in parent_text
        assert 'TOTAL_WALL, STAGE_WALL, RSS_CAP = 1800, 600, 512' in parent_text
for a in pins:
    b,z=fresh(Path(a['path']));assert z==a
with (D/'reviewed_raw_auditor_source_snapshot.py.txt').open('xb') as f:f.write(raw)
report={'schema':'AXMAT_V13_SENDER_WINDOW_RAW_AUDITOR_INDEPENDENT_SOURCE_REVIEW_V1','status':'PASS_SOURCE_CONTRACT_ONLY',
 'auditor_sha256':pin['sha256'],'driver_sha256':expected[C/'flusp64_window_observer_controls.UNREADY.f90'],
 'contract_sha256':expected[C/'CONTROL_CONTRACT.json'],'all_source_pins':pins,'AST_function_inventory':inventory,
 'complete_source_checks':list(clauses),'independent_raw_forecast':{'files':raw_count,'bytes':raw_bytes,'all_large_record_bytes':47970208,
 'large_eight_plane_bytes':42624000,'large_S2_bytes':5328000,'large_other_fields_bytes':18208},
 'concrete_findings_resolved_in_final_source':['Earlier pin had no identity window; final642 adds whole-tree seven-identity snapshot, unique nlink1 and per-fullhash before/after.',
 'Earlier release label overstated raw evidence; final642 labels actual repeated data and active-set transition only.',
 'Earlier executable-lastarg/stepcount checks have been replaced by exact executable path and complete step order.'],
 'remaining_blockers':[],
 'external_gates_required':['Current raw watchdog does not contain threads/child-count/retries fields: these remain genuine factory declaration/environment and serial source gates, with no fabricated watch keys.',
 'Source-admitted fullsender/reference/object identities and pre-sealed sender tree must remain part of Root fullfactory admission; this module does not grant production source identity by itself.'],
 'bounded_streaming_evidence':'initial_flux reads 1800-word group blocks, same_range at most1MiB; S2/output temporary lists at most1800 words, never all3million caller words.',
 'floating_bit_evidence':'All fixture arithmetic uses finite dyadic values; f32 signed bits packed as <i then <q match Fortran int32->int64 sign extension. S2 IR-loop preserves duplicate KEY accumulation order; output integer bitxor and negative zero are exact.',
 'actual_controls_or_compiler_exit':None,'actual_fixture_execution':False,'business_imported_or_called':False,'project_written':False,'Root_polled':False,
 'runtime_RSS_credit':False,'original_SPOT_math_calls_credited':0,'native_AAA_ABA_credit':False}
with (D/'REPORT.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
with (D/'REPORT.txt').open('x') as f:
 f.write('V13 wrapper原始字节审计器源码独审通过，仅SOURCE_CONTRACT。\n')
 f.write('最终64262e源码完整对应053747 driver/74ec contract；18字段、所有输入bits/title/maps、8planes、完整S2/输出/EOF逐项核对。\n')
 f.write('原B1顺序及重复KEY、负零、稀疏fallback/连续LOC、2步与4步carry、4真实XABORT负例均有明确门。\n')
 f.write('计划70 raw/288241824B；all 1800×370每record47970208B。原34observer不加2710真实SPOT数学调用。\n')
 f.write('新增全树7身份前后/unique nlink1和pin hash闭窗解决验证与hash之间变化；释放标签已改成实际数据transition。\n')
 f.write('线程1/单child/0retry来自原factory/SerialExecutor源门，不在旧watch里伪造字段。\n')
 f.write('未导入审计模块，未运行controls/fixture/编译/业务，也未写项目。所有实际输出与RSS/native资格仍None/false。\n')
print(json.dumps({'status':report['status'],'report_sha256':hashlib.sha256((D/'REPORT.json').read_bytes()).hexdigest(),
 'auditor_sha256':pin['sha256'],'functions':len(inventory),'raw_count':raw_count,'raw_bytes':raw_bytes}))
