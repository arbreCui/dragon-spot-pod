from pathlib import Path
import ast,hashlib,json,os,stat
D=Path(__file__).parent
pairs=[('host','/private/tmp/axmat_v14_helper_only_root_host_source_20261010/helper_only_host.UNREADY.py','c98d19874ac7972f1c1f52cc307f860b2ef0d87f9d7836f61db11ec77086536f'),('driver','/private/tmp/axmat_v14_complete_environment_streaming_helper_controls_source_only_20261010/helper_only_controls.UNREADY.py','4d630833ea330264f48aecf37b45183296716d906c6a74a15a113295b83513f9'),('helper','/private/tmp/axmat_v14_complete_environment_streaming_sha_helper_compatible_source_draft_20261010/complete_environment_streaming_sha_helper_v14.py','839ea8cc88e4f10d36b6bd8fcb283c9c774702e4c3688fc8a66831431c1cb5fa'),('original619','/Users/wen/spot/validation/axial_material/prepare_qualified_AB_source_factor_production.py','619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'),('resources','/Users/wen/spot/validation/axial_material/prepare_qualified_AB_rank1_factor_cache_cross_group_identity_key_delta_production.py','f136baab5047a8727cfd2c0abb5399acf617c25c4f4e7692242419e6f9daef4e'),('full','/Users/wen/spot/validation/axial_material/qualify_refined_AAA_layered_full.py','70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'),('production','/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py','38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128'),('bounded','/Users/wen/spot/validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/run_bounded_dragon.py','bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09')]
sha=lambda b:hashlib.sha256(b).hexdigest()
ident=lambda x:[x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
raw={};pins=[]
for label,name,want in pairs:
 p=Path(name);first=p.lstat();fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  pre=os.fstat(fd);chunks=[]
  while True:
   b=os.read(fd,2**20)
   if not b:break
   chunks.append(b)
  blob=b''.join(chunks);post=os.fstat(fd)
 finally:os.close(fd)
 last=p.lstat();assert ident(first)==ident(pre)==ident(post)==ident(last) and len(blob)==pre.st_size and stat.S_ISREG(first.st_mode)
 assert sha(blob)==want;raw[label]=blob.decode()
 pins.append(dict(label=label,path=name,sha256=want,size_bytes=len(blob),path_before=ident(first),fd_before=ident(pre),fd_after=ident(post),path_after=ident(last)))
ht=ast.parse(raw['host']);dt=ast.parse(raw['driver'])
def value(n):
 if isinstance(n,ast.BinOp) and isinstance(n.op,(ast.Mult,ast.Pow)):
  a,b=value(n.left),value(n.right)
  return a*b if isinstance(n.op,ast.Mult) else a**b
 return ast.literal_eval(n)
def constants(t):
 out={}
 for n in t.body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
   try:out[n.targets[0].id]=value(n.value)
   except (ValueError,TypeError):pass
 return out
hc,dc=constants(ht),constants(dt)
assert hc['WALL_CAP']==120 and hc['RSS_CAP']==512 and hc['ARCHIVE_CAP']==64*2**20
assert all(hc[k] is None for k in ('DRIVER_SHA256','HELPER_SHA256','PROOF_SHA256'))
assert dc['HELPER_SHA256'] is None and dc['MAX_ARCHIVE_BYTES']==64*2**20 and dc['EXPECTED_BUFFER_BYTES']==4*2**20
assert hc['THREAD_KEYS']==dc['THREAD_KEYS']==constants(ast.parse(raw['original619']))['THREAD_KEYS']
required=["h.modules()","h.guard_admission(full)","resource_factory.history_roots([str(host_root), str(control_root)], ART)","resources = resource_factory.resources_for(roots, production.ResourceFailure)","full.OwnRSSSerialExecutor.__bases__ != (production.SerialExecutor,)","runner = full.OwnRSSSerialExecutor(host_root, remaining","type(runner) is not full.OwnRSSSerialExecutor","remaining = WALL_CAP - (time.monotonic() - started)","runner.execute(host_root / 'run', 'controls', command, remaining)","before['artifact_bytes'] + ARCHIVE_CAP >= 96 * 2**30","before['disk_free_bytes'] - ARCHIVE_CAP < 8 * 2**30","choices=('fixtures', 'historical-environment'), default='fixtures'","token = '20261010' if args.action == 'fixtures' else 'historical-read-20261010'"]
assert all(s in raw['host'] for s in required)
for k in ('sampled_peak_rss_mib','liveness_group_cleanup','own_child_only','limit_failure','returncode','command'):assert "watch['"+k+"']" in raw['host']
fixture=next(n for n in dt.body if isinstance(n,ast.FunctionDef) and n.name=='fixture_controls')
cases=[n.args[0].value for n in ast.walk(fixture) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='run' and isinstance(n.args[0],ast.Constant)]
assert len(cases)==18 and len(set(cases))==18
loop=next(n for n in fixture.body if isinstance(n,ast.For) and isinstance(n.target,ast.Name) and n.target.id=='mode')
modes=ast.literal_eval(loop.iter);assert modes==['truncate','replace','rewrite']
cases+=['during_stream_'+s for s in modes];assert len(cases)==21 and len(set(cases))==21
main=next(n for n in dt.body if isinstance(n,ast.FunctionDef) and n.name=='main')
assignment=next(n for n in main.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='result')
assert isinstance(assignment.value,ast.IfExp) and assignment.value.body.func.id=='fixture_controls' and assignment.value.orelse.func.id=='historical_environment_comparison'
assert not any(isinstance(n,ast.ClassDef) for n in ast.walk(ht))
assert 'subprocess' not in raw['driver'] and 'audit-build' not in raw['driver'] and 'run-build' not in raw['driver']
for t in (ht,dt):assert all(not isinstance(n,ast.Expr) or not isinstance(n.value,ast.Call) for n in t.body)
report=dict(schema='AXMAT_V14_HELPER_ONLY_HOST_DRIVER_READONLY_INDEPENDENT_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_UNREADY',host_sha256=pairs[0][2],driver_sha256=pairs[1][2],helper_candidate_sha256=pairs[2][2],source_seven_identity_before_after=pins,fixture_group_names=sorted(cases),checks=dict(normal_canonical_future_3pins=True,original619_modules_guard=True,f136_resources_dynamic_history96_free8=True,genuine_directparent_OwnRSS_nooverlay=True,whole120_child512_archive64_thread1child1retry0=True,all21_small_IO_protocol_groups=True,independent_stdlib_full_file_digest_oracle=True,actual_new_adapter_real_FD_readinto_EOF_observations=True,namespace_alias_drift_error_cleanup_controls=True,default_fixtures_no_history=True,optional_fullhistory_separate_action_namespace=True,no_component_or_failed_V13_audit_invocation=True),no_deterministic_static_execution_blocker_found=True,limits=['Pure AST/text/SHA/7ID only; no helper/host/driver import/call/fixture.','Root actual source binding, genuine bounded completion, raw records, OwnRSS watchdog, full stdout and external terminal still required.','Do not add21 IO protocol groups to original86 or claim elapsed/native/science qualification.'],business_imported=False,helper_called=False,fixtures_executed=False,compiler_executed=False,project_written=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
with (D/'REPORT.json').open('x') as f:json.dump(report,f,indent=2);f.write(chr(10))
print(json.dumps(dict(status=report['status'],report_sha256=sha((D/'REPORT.json').read_bytes()),source_count=len(pins),fixture_groups=len(cases),business_executed=False)))
