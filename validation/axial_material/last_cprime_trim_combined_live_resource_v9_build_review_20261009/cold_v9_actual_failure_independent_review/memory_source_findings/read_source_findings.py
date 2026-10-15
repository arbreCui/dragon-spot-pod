import hashlib,json,pathlib,os
D=pathlib.Path(__file__).parent
A=pathlib.Path('/Users/wen/spot/validation/axial_material')
B=pathlib.Path('/Users/wen/spot/validation/artifacts')
TS=B/'axial-material-qualified-AB-rank1-factor-cache-last-cprime-trim-build-admission-20261008'
sources={
 A/'prepare_historical_input_owned_specs_physical_last_cprime_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak.py':'59d0c9b0f0a3b9ca6764f628ade537ec9b09eaa6edfe69e734994a7323adbfc8',
 A/'prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v9.py':'44789bc288715c34d08dbfa91b9c05dfc78166c2b8fa048bbe0207b273419a46',
 TS/'SPOT1P64.f90':'343e731fa190d80f8d390831185aef11dabcab32f51a229a5761c827a4aeb1e1',
 TS/'rank1_factor_cache_last_cprime_trim_controls.f90':'5b59f7202f9724b667549027bfedfea89581cd3b63c53087b993a1bcf2fc4ab2',
 B/'axial-material-qualified-AB-rank1-factor-cache-build-admission-20261007/FLU2DR64.f':'bb901bfed9a4199a5b4c98c58c93bf3b3dda597fd2047bfed6d267c8dcadac81',
}
pins=[]
def ident(p):
 s=p.stat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
for p,h in sources.items():
 before=ident(p);raw=p.read_bytes();actual=hashlib.sha256(raw).hexdigest();assert actual==h,(str(p),actual);assert ident(p)==before
 pins.append(dict(path=str(p),sha256=actual,identity=before))
f=(TS/'SPOT1P64.f90').read_text();lines=f.splitlines()
regions={}
for name,lo,hi in [('factor_and_solve',131,239),('last_cprime_already_trimmed',318,356),('boundary_allocate',1141,1206),('cached_build_and_backsolve',1310,1424),('identity_key',956,1111)]:
 regions[name]={'source':str(TS/'SPOT1P64.f90'),'first_line':lo,'last_line':hi,'text_sha256':hashlib.sha256(('\n'.join(lines[lo-1:hi])+'\n').encode()).hexdigest()}
solve=f[f.index('  subroutine SPOT1P64_SOLVE64'):f.index('  end subroutine SPOT1P64_SOLVE64')]
assert 'factor(i,jcol)' in solve and 'do i=jcol+1,n' in solve
assert 'factor(i,k)' in solve and 'do k=i+1,n' in solve
assert 'factor(i,i)' not in solve and 'factor(n,n)' not in solve
report={'status':'PASS_SOURCE_FACTS_ONLY','scope':'READONLY_FORTRAN_SOURCE_NO_IMPORT_NO_BUILD_NO_BUSINESS','project_written':False,'files_deleted':0,'native_failure_facts_from_root_task_not_independent_failure_review':{'root':'cefa98/session53935->afac4e','returncode':1,'bootstrap_axial_own_peak_mib':513.890625,'completed_maps':0},'allocation_failure_line_located':False,'rss_reduction_demonstrated':False,'source_pins':pins,'source_regions':regions,'observed_cache_bytes_from_root_task':312518392,'observed_cache_entries_from_root_task':18130,'candidates':[
 {'name':'persistent_factor_dead_diagonal','source_lines':[184,239,1315,1365],'fact':'SOLVE reads strictly lower and strictly upper factor cells; divisions use separately retained pivot_value. Diagonal is read/changed during FACTOR and becomes dead only after FACTOR completes.','source_only_plan':'A new packed off-diagonal representation may retain every live factor cell and all pivot/pivot_value; reconstruct a full matrix before the unchanged original SOLVE loops. Do not replace SOLVE math or shorten matrix products.','conditional_nominal_bytes':8*32*49*370,'conditional_mib':8*32*49*370/2**20,'status':'NOT_IMPLEMENTED_REQUIRES_NEW_LAYOUT_CONTROLS_AND_ACTUAL_RSS','risk':'Current plan public factor shape and memory accounting/shape guards must remain adequately covered; control archive reads factor dimensions at line587. No bit-equivalence or RSS success claimed.'},
 {'name':'release_cached_build_dense_work_arrays_before_backsolve','source_lines':[1181,1183,1365,1390,1424],'source_only_plan':'After cached-build use completes, lower/diagonal/upper are no longer read by backsolve and can be individually released before backsolve, with final cleanup made allocation-safe. Fallback unchanged.','nominal_bytes':3*8*32*32*49,'nominal_mib':3*8*32*32*49/2**20,'risk':'The arrays overlap factor/cprime allocation before this proposed release, so peak reduction is unproven and cannot be expected to remove the existing observed cap overage.'},
 {'name':'reuse_diagonal_storage_for_cached_factor','conditional_nominal_bytes':8*32*32*49,'conditional_mib':8*32*32*49/2**20,'status':'LOW_BENEFIT_SOURCE_ONLY_DESIGN_NOT_IMPLEMENTED','risk':'Needs correct ownership transfer after assembly while preserving the original Schur assignment and every read of diagonal. No allocation/order proof yet.'}],
 'already_done_not_to_repeat':['Final unused Cprime block already removed for rank1 cached path (line345 and allocation1322).','rank1 identity temporary key already released immediately after guard (1108).','Rank1 cached path does not allocate the fallback dense local Cprime.','Snapshot transport is already file-backed; no new proposal to switch RAM snapshot to file.'],
 'must_keep':['Both complete immutable cache key phases; all bit guards and signed-zero checks.','All lower dictionary values/maps and full original matrix shapes/products.','Live factor off-diagonal, all pivot/pivot_value, all 48 live dense Cprime blocks.','Original FLUX eight-slot semantics and cache lifetime/reuse guards.','SN32/cells16/rank1/accel/eps/order/all physics/reference thresholds and cap512 unchanged.'],
 'limits':['Source inference only, not actual failure attribution.','Accounted cache bytes are not process RSS and cannot be subtracted to prove other allocations.','No new executable source, build, test, import or business run.','Reference remains UNREADY until a new genuinely successful complete AAA attempt.']}
for name,val in [('REPORT.json',json.dumps(report,ensure_ascii=False,indent=2)+'\n'),('REPORT.txt','V9 内存源码线索（源码事实，不是实测修复）\n\n已定位真实组合构建继承的 SPOT1P64.f90。最后一个 Cprime、临时 identity key 已提前释放，当前路径没有另一份本地 dense Cprime，不能重复宣称这些优化。\n\n较有价值的候选：完整 Factor64 完成后，原 Solve64 不再读取因子对角线；仅严格下/上三角与独立 pivot_value 活跃。32方向×49块×370组的死对角线名义 4,641,280 字节（4.426 MiB）。可考虑新存储表示后恢复完整矩阵再调用原算术循环，必须保留原形状/控制覆盖并重新验证，不等于已通过。\n\n小候选：cached build 完成后提前释放 lower/diagonal/upper，共1.148MiB；由于更早已与 cache 分配重叠，不能认定降低峰值。复用 diagonal 为 factor 仅0.383MiB且还需完整生命周期证明。\n\n当前513.890625MiB失败没有定位到实际分配语句。这里不承诺 RSS 下降、不改变512MiB、任何物理输入、浮点循环、参考门或数学。原V9失败不重试。暂停进一步分析，转存储审查。\n')]:
 with (D/name).open('x') as out:out.write(val);out.flush();os.fsync(out.fileno())
print(json.dumps({'status':report['status'],'report':str(D/'REPORT.json'),'sha256':hashlib.sha256((D/'REPORT.json').read_bytes()).hexdigest(),'source_count':len(pins)}))
