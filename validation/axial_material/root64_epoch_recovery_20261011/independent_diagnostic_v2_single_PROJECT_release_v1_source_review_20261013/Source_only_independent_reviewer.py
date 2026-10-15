from pathlib import Path
import ast,hashlib,json,os,stat,time,resource,shlex
REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011');S=REC/'diagnostic_v2_single_PROJECT_release_source_v1';A=REC/'diagnostic_v2_single_PROJECT_release_v1_author_review_20261013';D=REC/'independent_diagnostic_v2_single_PROJECT_release_v1_source_review_20261013';START=time.monotonic();checks=[];full={}
def req(v,msg):
 assert type(v)is bool and v,msg;checks.append(msg)
 if time.monotonic()-START>=1800 or resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20:raise RuntimeError('readonly review original SELF512/whole1800')
def ident(q):return[q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]
def pin(p,expected=None):
 p=Path(p);i=ident(p.lstat());req(stat.S_ISREG(i[2])and i[0]==16777229,'ordinary currentdevice29')
 if str(p)in full:
  q=full[str(p)];req(q['identity']==i and(expected is None or q==expected),'cached actualcurrentPF');return q
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();n=0
 try:
  req(ident(os.fstat(fd))==i,'sameFDbefore')
  while True:
   b=os.read(fd,2**20)
   if not b:break
   h.update(b);n+=len(b)
  req(ident(os.fstat(fd))==i,'sameFDfullEOF')
 finally:os.close(fd)
 req(ident(p.lstat())==i and n==i[4],'pathall7fullEOF');q=dict(path=str(p),sha256=h.hexdigest(),size_bytes=n,identity=i);req(expected is None or q==expected,'exactfullPF');full[str(p)]=q;return q
def read(p):
 q=pin(p);b=Path(p).read_bytes();req(hashlib.sha256(b).hexdigest()==q['sha256']and ident(Path(p).lstat())==q['identity'],'wholeJSONcurrentPF');return json.loads(b)
handoff=read(A/'FINAL_FROZEN_SOURCE_HANDOFF.json');req(pin(A/'FINAL_FROZEN_SOURCE_HANDOFF.json')['sha256']=='ec5f8b1d072461e4fc1e607e6cd690422cc58e4df68f814f7690317afac32673','authorfrozenhandoff exactSHA')
for q in handoff['all_Source_tree_fullpins']+[handoff[k]for k in('CLI_pin','Source_freeze_pin','author_review_pin')]:pin(q['path'],q)
hf=read(S/'COMPLETE_SINGLE_DIAGNOSTIC_PROJECT_RELEASE_SOURCE_ONLY_FREEZE.json');plan=read(S/'PLAN_SOURCE_ONLY.json');cli=read(A/'ROOT_REVIEWABLE_REQUIRED_ACTUAL_GATES_RELEASE_ARGV_SOURCE_ONLY.json')
req(pin(S/'COMPLETE_SINGLE_DIAGNOSTIC_PROJECT_RELEASE_SOURCE_ONLY_FREEZE.json')['sha256']=='361a7f59777bbe46979ccd70a2b4d93e85727dbd91cda38f3f8246dc7817790f','exactfrozenreleaseSourceHF')
req(len(hf['dependencies'])==2818 and len(hf['Source_pins'])==2,'complete2818deps+2Source')
for q in hf['Source_pins']+hf['dependencies']+[hf[k]for k in('diagnostic_HF_pin','diagnostic_CLI_pin','diagnostic_input_authority_pin')]:pin(q['path'],q)
req(hf['future_diagnostic_report_pin']is None and hf['future_Root_true_receipt_pin']is None and hf['deletion_executed']is False and cli['future_actual_parameters']is None and cli['incomplete_until_real_external_report_and_Root_receipt_fullpins_supplied']is True,'Source only mandatoryfuturePF notguessed')
target=Path(plan['exact_only_target']);req(str(target)=='/Users/wen/spot/validation/artifacts/axial-material-v11-pair-rank-type-pretransport-combination-memory-diagnostic-20261013-v2/AAA/projected_boot.xsm'and plan['exact_logical_bytes']==749355952,'only newv2ownedtarget literal749355952')
source=(S/'release_single_diagnostic_project.py').read_text();tree=ast.parse(source)
def fn(name):return next(n for n in ast.walk(tree)if isinstance(n,ast.FunctionDef)and n.name==name)
def text(name):return ast.get_source_segment(source,fn(name))
gate=text('gates');main=text('main');inventory=text('inventory');live=text('no_live_writer');publish=text('publish')
req("TARGET=DIAG/'AAA/projected_boot.xsm'"in source and 'BYTES=749355952'in source,'target no parameter substitution')
req("['source-freeze','diagnostic-report','root-true-receipt']"in main and "required=True"in main and "parser.add_argument('--execute',action='store_true')"in main,'allrealexternalthreeflags/defaultreadonly explicitexecute')
req("t.get('schema')!='ROOT_ACTUAL_SINGLE_PAIR_RANK_TYPE_DIAGNOSTIC_V2_TRUE_TOOL_RETURNS_V1'"in gate and "t.get('actual_report_pin')!=dp"in gate and "t.get('executed_exact_cli_pin')!=f['diagnostic_CLI_pin']"in gate and "t.get('executed_command')!=shlex.join(cli['argv'])"in gate,'realRootreceipt strictclosed0 exactreportCLI/CMD schema')
req("type(terminal.get('exit_code'))is not int"in gate and "terminal['exit_code']!=0"in gate and "type(t.get('original_integer_exit_code'))is not int"in gate,'integerclosed0 no boolsuccess')
req("d.get('status')!='SINGLE_PRETRANSPORT_DIAGNOSTIC_COMPLETE_ONLY'"in gate and "d.get('primary_error')is not None"in gate and "d.get('after_check_errors')!=[]"in gate and "d.get('cap_observations')!=[]"in gate,'faileddiag noteligible')
req("oldledger!={'stages':raw['records']}"in gate and "stages['stages'][:45]!=raw['records']"in gate and "len(stages['stages'])!=46"in gate and "d['new_actual_stage_count']!=1"in gate,'exact45history/new1 actualscope')
req("row['status']!='FAILED'"in gate and "w['returncode']!=1"in gate and "text.count(expected)!=1"in gate and 'any(x in text for x in forbidden)'in gate,'genuineexit1 exactabortonce/nopositive trace')
req("d['SELF_peak_bytes']<512*2**20"in gate and "d['wall_seconds']<1800"in gate and "w['rss_cap_mib']!=512"in gate and "<=600"in gate,'originalparent+childcaps no relaxation')
req('raw[\'fixed_current_pins\']+raw[\'owned_runtime_pins\']'in gate and "for row in protected:b.same(row)"in gate and "[r for r in outputs if r['path']!=str(TARGET)]"in gate,'alloriginal fixed/currentowned+otherdiag Sourceevidence protected wholeEOF')
req("set(outtable)!=set(inv['files'])"in gate and "for row in outputs:"in gate and "b.same(row)"in gate,'actualreportoutputinventory exact no omittedextrafiles')
req("target not in owned"in gate and "target['identity'][3]!=1"in gate and "TARGET.lstat().st_uid!=os.getuid()"in gate and "r['identity'][:2]==target['identity'][:2]"in gate,'target actualowned UID/singlelink/inode disjoint allprotected')
req("copied['sha256']!=original['sha256']"in gate and "b.same(original)"in gate and "target['sha256']!=project_original['sha256']"in gate,'all12readonly copies/originals +originalv11PROJECT retained')
req("['/bin/ps','-axo','pid=,pgid=,command=']"in live and "['/usr/sbin/lsof','-nP','+D',str(DIAG)]"in live and "ls.stderr.strip()or ls.stdout.strip()"in live and "int(fields[1])==pid"in live,'actualps+PID+writer+lsof absence required no permissionfallback')
unlinks=[n for n in ast.walk(tree)if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr=='unlink'];req(len(unlinks)==1 and ast.unparse(unlinks[0])=='os.unlink(TARGET.name, dir_fd=fd)','unique literal parentdirfd unlink only')
req("os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW"in main and "os.stat(TARGET.name,dir_fd=fd,follow_symlinks=False)"in main and "b.identity(s)!=admitted['target']['identity']"in main and "b.identity(os.fstat(fd))!=admitted['complete_before_inventory']['directories'][str(TARGET.parent)]"in main,'openedparentfd/all7target immediatelybefore unlink')
req(main.index('publish();b.guard()')<main.index('os.unlink(')and 'os.O_CREAT|os.O_EXCL|os.O_RDWR|os.O_NOFOLLOW'in main and 'os.fsync(stream.fileno())'in publish,'complete exactevidencefsync sameownedreceiptFD beforedelete')
req("admitted['original_budget_before']['artifact_bytes']-after['artifact_bytes']!=BYTES"in main and "admitted['original_budget_before']['regular_files']-after['regular_files']!=1"in main and "after['original_initial_reserve_admitted']is not True"in main,'exactactualARTbytes/filedelta+restoredfullinitialreserves')
req("after[3]!=prior[3]-1"in main and "after[4]!=prior[4]-32"in main and "elif after!=prior"in main and "new['files']!={p:i for p,i in old['files'].items()if p!=str(TARGET)}"in main,'only targetentry/APFSnaturalparent -1/-32 otherfiles/dirs7 unchanged')
outer=next(n for n in fn('main').body if isinstance(n,ast.Try));final='\n'.join(ast.unparse(n)for n in outer.finalbody);req('first_error ='not in final,'finally never overwrites primarycause')
req("FAILED_OR_PARTIAL_RELEASE_EVIDENCE_RETAINED_NO_RETRY"in main and "deleted_files=int(deleted)"in main and 'if first_error is not None or after_errors:raise SystemExit(1)'in main,'truthfulpartialactualdeletion firsterror+latererror exit1 noretry')
req("fresh-BYTES+8*2**20>128*2**20"in gate and "+20971764748+64*2**20>=96*2**30"in gate and "-20971764748-2*2**30<8*2**30"in gate,'remaining128/public8/originalcoldhistoryfreefullfresh no relaxed constants')
base=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/storage_release_closed_v7_v8_project_pair_20261013/project_pair_release_common.py');bt=base.read_text();ast.parse(bt);pin(base);req('512*2**20'in bt and '1800'in bt,'originalhelperactualselfwhole guards retained')
actual=read(Path(target).parent.parent/'DIAGNOSTIC_REVIEW.json');tp=pin(REC/'ACTUAL_SINGLE_PAIR_RANK_TYPE_COMBINATION_V2_ROOT_TRUE_TOOL_RETURNS_20261013.json');truth=read(tp['path']);diagnostic_cli=read(hf['diagnostic_CLI_pin']['path']);req(truth['executed_command']==shlex.join(diagnostic_cli['argv']),'actualRootCMD exactstrict gate compatible')
req(actual['status']=='SINGLE_PRETRANSPORT_DIAGNOSTIC_COMPLETE_ONLY'and actual['new_actual_stage_count']==1,'currentactualRoot external report genuine requiredstate')
targetpin=pin(target);original_authority=read(hf['diagnostic_input_authority_pin']['path']);original=next(r['source_pin']for r in original_authority['inputs']if r['destination_name']=='projected_boot.xsm');pin(original['path'],original)
req(targetpin in actual['new_owned_copy_and_archival_pins']and targetpin['sha256']==original['sha256']and targetpin['identity'][:2]!=original['identity'][:2],'actualnewcopy target disjoint retainedoldoriginal')
req(not any(q['path']==str(target)or q['identity'][:2]==targetpin['identity'][:2]for q in hf['dependencies']),'candidatefrozenSource dependenciesexclude deletetarget')
for q in full.values():req(ident(Path(q['path']).lstat())==q['identity'],'allsourceinputs stableall7 atfinal')
result=dict(schema='INDEPENDENT_EXACT_DIAGNOSTIC_V2_SOLE_PROJECT_RELEASE_SOURCE_REVIEW_V1',status='SOURCE_ONLY_FINITE_REVIEW_PASS_ROOT_MAY_APPLY_MANDATORY_ACTUAL_GATES',checks=len(checks),unique_EOF_files=len(full),unique_EOF_bytes=sum(q['size_bytes']for q in full.values()),all_verified_current_fullpins=list(full.values()),Source_handoff_pin=pin(A/'FINAL_FROZEN_SOURCE_HANDOFF.json'),release_HF_pin=pin(S/'COMPLETE_SINGLE_DIAGNOSTIC_PROJECT_RELEASE_SOURCE_ONLY_FREEZE.json'),CLI_pin=pin(A/'ROOT_REVIEWABLE_REQUIRED_ACTUAL_GATES_RELEASE_ARGV_SOURCE_ONLY.json'),actual_current_diagnostic_target_pin=targetpin,retained_original_v11_PROJECT_pin=original,actual_root_report_and_CMD_compatible=True,mandatoryreportRootreceipt_futurePF_not_prefilled=True,all_sources_originaldata_and_otherdiagnostic_outputs_protected=True,uid_singlelink_disjoint_inode_all7_parentdirfd_verified_inSource=True,predelete_fullreceipt_fsync_and_exactspace_parentdelta_postchecks_verified=True,firsterror_not_masked_partialfailure_true_exit1=True,candidate_imported=False,release_or_guard_or_Dragon_executed=False,Source_modified=False,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,wall_seconds=time.monotonic()-START,engineering_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,all_checks=checks)
D.mkdir()
with(D/'REVIEW.json').open('x')as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],checks=len(checks),EOF=len(full),bytes=result['unique_EOF_bytes'],review_pin=pin(D/'REVIEW.json'),target_current_fullpin=targetpin)))
