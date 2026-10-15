"""Storage audit only: bytes, retained metadata and inert NPZ headers; no science imports."""
import ast, hashlib, io, json, os, re, stat, struct, time, zipfile
from pathlib import Path

ROOT=Path('/Users/wen/spot')
N=ROOT/'validation/artifacts/native-layered-full-20261001'
OUT=Path('/private/tmp/spot_storage_eighteenth_native_layered_raw_independent_review_20261009')
def sig(s): return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def sha(b): return hashlib.sha256(b).hexdigest()
def jsonbytes(d): return json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def raw(p):
    p=Path(p); a=p.lstat(); assert stat.S_ISREG(a.st_mode) and p.resolve()==p
    with p.open('rb') as f: b=f.read()
    assert sig(p.lstat())==sig(a)
    return b
def read(p): return json.loads(raw(p))
def hashed(p):
    p=Path(p); a=p.lstat(); assert stat.S_ISREG(a.st_mode) and p.resolve()==p
    with p.open('rb') as f: h=hashlib.file_digest(f,'sha256').hexdigest()
    assert sig(p.lstat())==sig(a)
    return {'path':str(p),'sha256':h,'bytes':a.st_size,'identity':sig(a)}
def npy_header(f):
    assert f.read(6)==b'\x93NUMPY'; ver=tuple(f.read(2)); assert ver in ((1,0),(2,0),(3,0))
    fmt='<H' if ver==(1,0) else '<I'; length=struct.unpack(fmt,f.read(struct.calcsize(fmt)))[0]
    d=ast.literal_eval(f.read(length).decode('utf-8' if ver==(3,0) else 'latin1'))
    assert set(d)=={'descr','fortran_order','shape'} and d['fortran_order'] is False
    assert not 'O' in str(d['descr']); return d
def npz_headers(p,expected,tracks=None):
    with zipfile.ZipFile(p) as z:
        assert set(z.namelist())=={k+'.npy' for k in expected}
        for name,shape in expected.items():
            with z.open(name+'.npy') as f:
                h=npy_header(f); assert tuple(h['shape'])==tuple(shape),(str(p),name,h)
                if name=='original_tracks' and tracks is not None:
                    assert h['descr'] in ('<i8','<i4')
                    payload=f.read(); fmt='q' if h['descr']=='<i8' else 'i'
                    assert list(struct.unpack('<'+fmt*len(tracks),payload))==tracks

started=time.monotonic()
seal=raw(N/'result.sha256'); assert sha(seal)=='6ab0927cb9570715607c260873e907d6b6a429327773909ceb4b2e4f0af3ac2d'
old={}
for line in seal.decode().splitlines():
    digest,rel=line.split('  ',1); assert re.fullmatch('[0-9a-f]{64}',digest) and rel not in old
    assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
    old[rel]=digest
assert len(old)==25713
plan=read(N/'plan.json'); cases=[c for c in plan['batches'] if not c['preflight']]
assert len(cases)==1080 and len({c['id'] for c in cases})==1080
rawnames={f'raw_g{g}_o{o}_m{m}.npz' for g in (51,61,98) for o in (1,-1) for m in (-1,1)}
candidate={str(N/'primary'/c['id']/f) for c in cases for f in rawnames}; assert len(candidate)==12960
candidate_rows=[]
for pstr in sorted(candidate):
    p=Path(pstr); s=p.lstat(); assert stat.S_ISREG(s.st_mode) and s.st_nlink==1 and p.resolve()==p
    candidate_rows.append([pstr,s.st_size,s.st_blocks*512,sig(s),old[str(p.relative_to(N))]])
candidate_original_identities={r[0]:r[3] for r in candidate_rows}
retained=[]
for rel,expected in old.items():
    p=N/rel
    if str(p) in candidate: continue
    r=hashed(p); assert r['sha256']==expected,(rel,'retained original seal mismatch'); retained.append(r)
assert len(retained)==12753
all_current={str(p.relative_to(N)) for p in N.rglob('*') if p.is_file() and not p.is_symlink()}
assert all_current==set(old)|{'result.sha256'},('current exact family pathset',len(all_current))
frozen=read(N/'frozen_inputs.json'); assert len(frozen)==303
for rel,h in frozen.items(): assert rel in old and old[rel]==h and str(N/rel) not in candidate
admission=read(N/'admission.json'); assert admission['full_execution_admitted'] is True
for field,rel in [('plan_sha256','plan.json'),('frozen_inputs_sha256','frozen_inputs.json'),('full_jobs_sha256','full_jobs.json')]:
    assert admission[field]==old[rel]
filemap={}; totals={k:0 for k in ['physical_states','physical_coordinate_evaluations','physical_piece_column_updates','matched_regression_states','matched_regression_input_evaluations']}
npzchecked=0
for c in cases:
    name=c['id']; folder=N/'primary'/name; r=read(folder/'result.json'); nt=c['stop']-c['first']; nz=c['nz']; k=14*nz+10; nout=14*nz+16
    assert r['case']==c and r['all_checks_passed'] is True and r['full_cell_face_regression_byte_exact'] is True
    assert r['original_records']==nt and r['physical_states']==nt*24 and r['physical_coordinate_evaluations']==nt*24*k
    assert r['matched_regression_states']==nt*24 and r['matched_regression_input_evaluations']==nt*24*14
    for key in totals: totals[key]+=r[key]
    a=read(N/'receipts/primary'/f'{name}.json'); b=read(N/'receipts/replay'/f'{name}.json')
    assert a['all_scientific_bytes_identical'] is False and b['all_scientific_bytes_identical'] is True and a['files']==b['files']
    assert set(a['files'])==rawnames|{'operators.npz','controls.npz','result.json'}
    assert {p.name for p in folder.iterdir() if p.is_file()}==set(a['files'])
    for fn,d in a['files'].items():
        p=folder/fn; assert p.stat().st_size==d['bytes'] and old[str(p.relative_to(N))]==d['sha256']
        filemap[f'{name}/{fn}']=d
    for phase in ('primary','replay'):
        u=read(N/'runs'/f'{phase}_{name}_resources.json')
        assert u['elapsed_seconds']<600 and u['peak_rss_mib']<512 and u['output_bytes']==sum(d['bytes'] for d in a['files'].values())
    tracks=list(range(c['first'],c['stop']))
    npz_headers(folder/'operators.npz',{'original_tracks':(nt,),'operators':(2,3,2,2,nout,k),'jx':(2,3,2,2,8*nz,k),'abs_jx':(2,3,2,2,8*nz,k)},tracks)
    npz_headers(folder/'controls.npz',{'original_tracks':(nt,),'checks':(nt,3,2,2,2,11),'convergence':(nt,3,2,2,3),'regression_hashes':(nt,3,2,2,2),'old_recovery':(nt,3,2,2,2,2),'reference_errors':(nt,2,3,2),'geometry_counts':(nt,2,2,2,3)},tracks)
    npzchecked+=2
expected_totals=dict(physical_states=6545664,physical_coordinate_evaluations=279281664,physical_piece_column_updates=2453859601920,matched_regression_states=6545664,matched_regression_input_evaluations=91639296)
assert totals==expected_totals
replay=read(N/'verification/replay.json'); assert replay['all_scientific_bytes_identical'] is True and replay['files']==filemap and len(filemap)==16200
families=sorted({c['id'].rsplit('_b',1)[0] for c in cases}); assert len(families)==24
traces=0
for family in families:
    cs=[c for c in cases if c['id'].rsplit('_b',1)[0]==family]; assert len(cs)==45
    assert [t for c in cs for t in range(c['first'],c['stop'])]==list(range(11364))
    d=read(N/'verification'/family/'result.json')
    assert d['scope']=='complete original inventory' and d['all_checks_passed'] is True and d['all_original_indices_once'] is True and d['all_declared_indices_once'] is True
    assert d['original_tracks']==11364 and d['raw_files']==540 and d['physical_states']==11364*12 and len(d['independent_traces'])==12
    assert d['source_coordinates']==11364*12*(14*cs[0]['nz']+10) and d['elapsed_seconds']<600 and d['peak_rss_mib']<512
    expected_files={'operators.npz','result.json'}|{f'g{g}_o{o}_m{m}.npz' for g in (51,61,98) for o in (1,-1) for m in (-1,1)}
    assert {p.name for p in (N/'verification'/family).iterdir() if p.is_file()}==expected_files
    traces+=len(d['independent_traces'])
for family in sorted({f[3:] for f in families}):
    d=read(N/'white'/family/'result.json')
    assert d['all_checks_passed'] is True and d['original_tracks']==11364 and d['physical_axial_incoming_zero'] is True and d['geometric_normalizer_used'] is True and len(d['groups'])==3
watchcount=0; fullwatchcount=0; watchsum=hashlib.sha256()
for jobfile in ['preflight_jobs.json','audit_preflight_jobs.json','action_preflight_jobs.json','full_jobs.json']:
    jobs=read(N/jobfile)
    if jobfile=='full_jobs.json': assert len(jobs)==2191
    for job in jobs:
        w=read(N/'runs'/f'{job["name"]}_watchdog.json')
        assert type(w['returncode']) is int and w['returncode']==0 and w['limit_failure'] is None and w['elapsed_seconds']<600 and w['sampled_peak_rss_mib']<512
        assert w['command'][1:]==[str(N/'build'/job['script']),str(N),*job.get('args',[])]
        watchsum.update(jsonbytes([job['name'],w])); watchcount+=1
        if jobfile=='full_jobs.json': fullwatchcount+=1
assert watchcount==2219 and fullwatchcount==2191
final=read(N/'verification/result.json')
assert final['full_batches']==1080 and final['scientific_replay_files']==16200 and final['independent_audits']==24 and final['independent_full_traces']==288
assert final['counts']==totals and final['full_native_physical_operator_qualified'] is True and final['full_native_white_qualified'] is True and final['full_previous_zero_gradient_regression_completed'] is True
assert final['production_changed'] is False and final['coupled_eigenproblem_qualified'] is False
preflight=set()
for c in plan['batches']:
    if c['preflight']:
        preflight.update(str(N/'primary'/c['id']/fn) for fn in rawnames)
assert len(preflight)==12 and not candidate&preflight and all(Path(p).is_file() for p in preflight)
mapping_paths=set(ROOT.glob('validation/storage_cleanup*/*manifest*.json'))
mapping_paths.update([ROOT/'validation/storage_review_20261008/first_batch_24_files.json',ROOT/'validation/storage_review_20261008/second_batch_replay_arrays.json',ROOT/'validation/storage_review_more_20261008/exact_retirement_manifest.json'])
mapping_paths={p for p in mapping_paths if p.name in ('manifest.json','cache_manifest.json','audit_metadata_manifest.json','runtime_retirement_manifest.json','exact_retirement_manifest.json','first_batch_24_files.json','second_batch_replay_arrays.json')}
mapping_pins=[]; hits=[]; prefix_hits=[]
def strings(d):
    if isinstance(d,dict):
        for k,v in d.items():
            yield str(k); yield from strings(v)
    elif isinstance(d,list):
        for v in d: yield from strings(v)
    elif isinstance(d,str): yield d
for p in sorted(mapping_paths):
    rec=hashed(p); d=read(p); ss=list(strings(d)); direct=set(ss)&candidate
    assert not direct,(str(p),'previous restore/current source master intersects',direct)
    mentions=sorted({s for s in ss if 'native-layered-full-20261001/primary/' in s})
    prefix_hits.extend([{'manifest':str(p),'mention':s} for s in mentions]); mapping_pins.append(rec)
for r in retained: assert sig(Path(r['path']).lstat())==r['identity'],r['path']
for p,s in candidate_original_identities.items(): assert sig(Path(p).lstat())==s,p
keydocs=[ROOT/'validation/iterative/native_layered_full_result.md',ROOT/'validation/iterative/native_layered_full_execution.md',N/'result.sha256',N/'execution_checkpoint.json']
report={'schema':'SPOT_R18_NATIVE_LAYERED_DERIVED_RAW_RETAINED_RESULTS_INDEPENDENT_REVIEW_V1','status':'PASS','scope':'READ_ONLY_RETAINED_RESULT_SOURCE_RECOMPUTABILITY_AND_PRIOR_RESTORE_MAPPING_AUDIT; CURRENT_DEPENDENCY_AND_RAW_FRESH_SHA_PEER_SCOPE_REQUIRED','files_deleted':0,'project_written':False,'business_executed':False,'current_native_executed':False,'candidate_count':len(candidate),'candidate_logical_bytes':sum(r[1] for r in candidate_rows),'candidate_allocated_bytes':sum(r[2] for r in candidate_rows),'candidate_sorted_paths_sha256':sha(jsonbytes(sorted(candidate))),'candidate_table_including_old_expected_SHA_and_current_stat_digest':sha(jsonbytes(candidate_rows)),'raw_fresh_SHA_content_reads_in_this_reader':0,'raw_old_expected_SHA_receipt_and_seal_agreement':True,'retained_seal_entry_fullSHA_count':len(retained),'retained_seal_fullSHA_bytes':sum(r['bytes'] for r in retained),'retained_seal_evidence_digest':sha(jsonbytes(retained)),'original_seal_sha256':sha(seal),'exact_current_family_pathset_original_seal_plus_manifest':True,'retained_batch_operators_controls_result_complete':1080,'primary_replay_receipt_pairs_all15_equal':1080,'full_NPZ_structural_headers_and_original_track_vectors_checked':npzchecked,'independent_audits_complete':24,'independent_full_trace_outputs_preserved':traces,'full_jobs_watchdog_true_typed_zero':fullwatchcount,'all_scheduled_watchdogs_including_preflight_true_typed_zero':watchcount,'watchdog_evidence_digest':watchsum.hexdigest(),'retained_preflight_raw_count':len(preflight),'retained_preflight_raw_paths':sorted(preflight),'frozen_local_input_files_fullSHA':303,'prior_restore_mapping_manifest_pins':mapping_pins,'previous_restore_master_or_exact_candidate_path_intersections':hits,'previous_mapping_raw_prefix_mentions':prefix_hits,'final_result_original_flags':final,'documentation_pins':[hashed(p) for p in keydocs],'stale_original_checkpoint_preserved_not_reinterpreted':read(N/'execution_checkpoint.json'),'recompute_contract':{'raw_is_exact_duplicate':False,'operators_controls_are_lossless_substitute_for_raw':False,'raw_immediate_historical_fullseal_or_verify_no_longer_works_after_retirement':True,'historical_full_raw_audit_requires_recomputation':True,'retained_build_inputs_plan_original_commands_available':True,'original_primary_xb_cannot_overwrite_retained_operators_controls_results':True,'recompute_in_separate_scratch_root_using_frozen_inputs_build_plan_and_admission':True,'only_after_full_raw_size_SHA_match_old_receipt_can_restore_old_paths':True,'actual_recompute_or_future_byte_identical_reproducibility_not_demonstrated':True,'no_new_lossless_restore_archive_required_by_explicit_cleanup_scope':True},'qualification_boundary':{'original_fixed_source_component_success_preserved':True,'new_physics_or_coupled_eigenproblem_credit':False,'AAA_ABA_accuracy_credit':False,'old_scheduler_interruption_cause_remains_unknown':True},'elapsed_readonly_seconds':time.monotonic()-started}
with (OUT/'REPORT.json').open('x') as f: json.dump(report,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
text='独立只读核对通过（保留结果与恢复依赖范围；待另一路当前依赖及候选全文 SHA 合并）。\n'+f'候选为旧 native-layered full_jobs 的 {len(candidate)} 份派生 raw_g 数组，{sum(r[2] for r in candidate_rows)/2**30:.6f} GiB 分配空间。\n'+f'已完整 SHA 读取保留的 {len(retained)} 个旧封存条目（{sum(r["bytes"] for r in retained)} B），包括全部 1080 批 operators/controls/result、2160 主/重放收据、24 独立审查/288 全场样例、6 白边界最终结果、输入、源码、构建及所有日志。\n'+'2191 full_jobs 与全部 2219 监控收据均保持原 typed 0；陈旧 execution_checkpoint 的 running/unsealed 原记录仍保留，未替换为成功。额外 preflight 12 raw 样例全部保留。\n'+'这些 raw 不是重复副本，operators/controls 也不是其无损替代。清退会失去旧 raw 的直接逐字节重验；须在隔离目录按保留的完整输入、原代码/构建/plan/admission 重算，逐份长度与 SHA 匹配原收据后才可恢复旧路径。原 primary 用 xb，不能直接覆盖剩余最终文件。未来重算逐字节相同尚未实证。\n'+'前轮精确恢复 manifest 全部检查：没有候选 raw 被列为既删文件的保留主本。原组件成功与耦合特征问题未合格等科学范围不变；本次没有新科学信用。\n'+'没有删除、没有项目写入、没有业务 import/API/native。当前候选 raw 正文未在本 reader 再读，旧收据/封存摘要与现存长度均一致；候选 fresh 全 SHA 由互补审查提供。\n'
with (OUT/'REPORT.txt').open('x') as f:f.write(text)
print(json.dumps({'status':'PASS','scope':report['scope'],'report':str(OUT/'REPORT.json'),'report_sha256':sha(raw(OUT/'REPORT.json')),'candidate_count':len(candidate),'candidate_allocated_bytes':report['candidate_allocated_bytes'],'retained_fullSHA_files':len(retained),'retained_fullSHA_bytes':report['retained_seal_fullSHA_bytes'],'elapsed_seconds':report['elapsed_readonly_seconds'],'files_deleted':0,'project_written':False}))
