"""Finite SOURCE-only prelaunch retarget audit; never imports/calls reviewed source."""
import ast,hashlib,json,stat
from pathlib import Path
P=Path(__file__).parent
OLD=Path('/private/tmp/spot_v22_native_prelaunch_ROOT.py')
NEW=Path('/private/tmp/spot_v22_native_prelaunch_ROOT_v2.py')
WRITER=Path('/private/tmp/spot_v22_native_postclose_META_ROOT_v2.py')
C=[]
def pin(p):
 s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 assert stat.S_ISREG(before[2]) and before[3]==1 and p.resolve()==p
 with p.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
 t=p.lstat();after=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
 assert before==after
 return dict(path=str(p),sha256=digest,size_bytes=before[4],identity=before)
def check(value,label):
 assert value,label
 C.append(dict(check=label,passed=True))
op=pin(OLD);np=pin(NEW);wp=pin(WRITER)
o=OLD.read_text();n=NEW.read_text();ot=ast.parse(o);nt=ast.parse(n)
check(op['sha256']=='39ab4d3b57f002b1830488b614ce21ebe3420ccad9756498c8745737043f8e91' and op['size_bytes']==4070,'original complete prelaunch Source pin')
check(np['sha256']=='f46c69c5ffb35d4f559ce60371d8302ad8132d58b62e9301d97c6423d5097196' and np['size_bytes']==4070,'actual v2 complete prelaunch Source pin')
check(wp['sha256']=='dcdfbe2eda413f8958ec2c3a3ef4f8ae59507793706d385a3fab030c9bbc4dfc','retarget to independently reviewed v2 metadata writer')
check((P/'original_prelaunch_SOURCE.py').read_bytes()==OLD.read_bytes(),'full original prelaunch Source copied')
check((P/'prelaunch_v2_SOURCE.py').read_bytes()==NEW.read_bytes(),'full new prelaunch Source copied')
before="WRITER_SHA='dcdfbe2eda413f8958ec2c3a3ef4f8ae59507793706d385a3fab030c9bbc4dfc'"
after="WRITER_SHA='5f302e44a094c20682e1708f3cd714f4e7bedf7da12de1c775ccca7b8338ea5b'"
check(n.count(before)==1 and o.count(after)==1,'one exact writer SHA binding hunk')
reverse=n.replace(before,after,1)
check(reverse==o,'whole byte inverse exact original preflight')
check(ast.dump(ast.parse(reverse),include_attributes=False)==ast.dump(ot,include_attributes=False),'whole AST inverse exact original preflight')
of=[x for x in ot.body if isinstance(x,ast.FunctionDef)]
nf=[x for x in nt.body if isinstance(x,ast.FunctionDef)]
check(len(of)==len(nf)==1 and of[0].name==nf[0].name=='main','one original main definition')
check(ast.get_source_segment(o,of[0])==ast.get_source_segment(n,nf[0]),'complete main byteexact')
check(ast.dump(of[0],include_attributes=False)==ast.dump(nf[0],include_attributes=False),'complete main ASTexact')
for term in [
 'not sys.flags.optimize','sys.getprofile() is None',
 'hashlib.sha256(SOURCE.read_bytes()).hexdigest()==WRITER_SHA',
 "spec_from_file_location('Root_native_prelaunch_metadata_functions',SOURCE)",
 "not any(os.path.lexists(p) for p in (m.H,m.O,m.C))",
 "d==freeze['complete_D']","len(binding['complete_input_pins'])==129",
 "binding['original_caps']==m.CAPS",
 "Root_bound_complete_native_genuine_host.py","Root_bound_complete_native_checker.py",
 "support.OLD_HELPER,support.OLD_HELPER_SHA",
 "support.RESOURCE_FACTORY,support.RESOURCE_SHA",
 "full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)",
 "Path(full.__file__).resolve()==support.FULL",
 "Path(production.__file__).resolve()==support.PARENT",
 "(m.H,m.O,m.C,support.OUT,support.TERMINAL)",
 '8*2**30,96*2**30,production.ResourceFailure',
 "actual['artifact_bytes']+2*2**30<96*2**30",
 "actual['disk_free_bytes']-2*2**30>=8*2**30",
 'm.bytes_in([d,e])<2*2**30',
 'assert before==e and m.snapshot(m.D)==d',
 'full129_material_payloads_not_rehashed_by_this_preflight=True',
 'complete129_payloads_will_be_fresh_EOF_verified_by_genuine_host_before_and_after=True',
 'native_executed=False','no_runtime_E_append=True',
 "Path('/private/tmp/spot_v22_native_complete_prelaunch_frozen_D_E_ROOT_20261010_7f9a7f.json')",
 'assert m.snapshot(m.E)==e and m.snapshot(m.D)==d',
 "if __name__=='__main__':main()",
]:check(term in n,'unchanged Source contract '+term)
for forbidden in ['subprocess','run_stage','runner.run','Popen','numeric','decode_stream']:
 check(forbidden not in n,'no new actual native or payload call '+forbidden)
check(pin(OLD)==op and pin(NEW)==np and pin(WRITER)==wp,'all Source pins unchanged fullEOF final')
report=dict(schema='INDEPENDENT_V22_NATIVE_PRELAUNCH_V2_FINITE_SOURCE_REVIEW_V1',
 status='PASS_SINGLE_LITERAL_NATIVE_PRELAUNCH_V2_SOURCE_ONLY',
 all_checks_typed_true=True,blockers=[],checks=C,check_count=len(C),
 original_prelaunch_pin=op,prelaunch_v2_pin=np,reviewed_metadata_writer_pin=wp,
 single_writer_SHA_literal_only=True,whole_byte_AST_inverse_exact=True,
 complete_main_byte_AST_exact=True,
 original_MRO_resource_freeze_env_scopes_unchanged=True,
 material_input_129_count_retained_without_rehash_in_preflight=True,
 genuine_host_before_after_full129_payload_hash_requirement_unchanged=True,
 reviewer_executed_prelaunch_or_guard_or_native=False,
 source_only=True,actual_prelaunch_run_qualified=False,
 native_executed=False,native_RSS_verified=False,
 actual_native_byte_qualification_sha256=None,
 scientific_accuracy_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
with (P/'REVIEW.json').open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
(P/'REPORT.txt').write_text('PASS: prelaunch v2 has exactly one writer SHA literal retarget. Full byte/AST inverse restores original39ab4d/4070 B; complete main unchanged. Original full D/E freeze, exact host/checker/binding, original genuine MRO/resource/history/reserve/env and source-only preflight scope remain. No reviewed preflight, guard or native executed; no 129 material payload read; all actual/native/science qualification remains false/unknown.\n')
members={}
for q in sorted(P.rglob('*')):
 assert not q.is_symlink()
 if q.is_file():members[str(q.relative_to(P))]=pin(q)
with (P/'MANIFEST.json').open('x') as f:json.dump(dict(schema='INDEPENDENT_NATIVE_PRELAUNCH_V2_FINITE_SOURCE_MANIFEST_V1',members=members,member_count=len(members),member_bytes=sum(v['size_bytes'] for v in members.values()),manifest_excluded_from_own_members=True,source_only=True),f,indent=2,allow_nan=False);f.write('\n')
for k,q in members.items():assert pin(P/k)==q
print(json.dumps(dict(status=report['status'],check_count=len(C),manifest=pin(P/'MANIFEST.json'),review=pin(P/'REVIEW.json'),complete_files=len(members)+1,prelaunch_v2=np,reviewer_executed_prelaunch_or_guard_or_native=False)))
