"""Once Source HF/CLI publication after independent Source0; no science import/run."""
import argparse,ast,hashlib,json,os,shlex,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
HERE=R/'saved_full370_after_latest_full50_source_v3_20261014'
OLD=R/'saved_full370_terminal_audit_host_source_v2'
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat()
 if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('bounded ordinary Source metadata only')
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('opened7')
  b=f.read()
  if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('EOF7')
 if identity(p.lstat())!=identity(s):raise RuntimeError('after7')
 return b,dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=identity(s))
def read(p):
 b,q=pin(p['path'])
 if q!=p:raise RuntimeError('exact metadata PF')
 return json.loads(b)
def collect(v):
 if isinstance(v,dict):
  if set(v)=={'path','sha256','size_bytes','identity'}:yield v
  else:
   for x in v.values():yield from collect(x)
 elif isinstance(v,list):
  for x in v:yield from collect(x)
def unique(rows):
 t={}
 for p in rows:
  if p['path']in t and t[p['path']]!=p:raise RuntimeError('inconsistent PF')
  t[p['path']]=p
 return list(t.values())
def current7(rows):
 for p in unique(rows):
  if identity(Path(p['path']).lstat())!=p['identity']:raise RuntimeError('current7: '+p['path'])
def write(p,d):
 b=(json.dumps(d,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
 with os.fdopen(os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644),'wb')as f:f.write(b);f.flush();os.fsync(f.fileno())
 return pin(p)[1]
def external(a,k):
 b,p=pin(getattr(a,k+'_summary'))
 if p['sha256']!=getattr(a,k+'_sha256')or p['identity']!=json.loads(getattr(a,k+'_seven_id')):raise RuntimeError('external complete PF')
 return json.loads(b),p
def terminal0(t,k):
 r=t[k]
 if type(r.get('exit_code'))is not int or r['exit_code']!=0 or r.get('session_id')is not None or t.get('observed_closed')is not True or type(t.get('original_integer_exit_code'))is not int or t['original_integer_exit_code']!=0:raise RuntimeError('genuine closed integer0 tool')
 return r
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for k in ('peer-review','peer-tools','Source-generation-tools'):
  for x in ('summary','sha256','seven-id'):ap.add_argument('--'+k+'-'+x,required=True)
 a=ap.parse_args();review,pr=external(a,'peer_review');tools,pt=external(a,'peer_tools');gen,pg=external(a,'Source_generation_tools')
 result=terminal0(tools,'actual_review_return')
 if json.loads(result['output'].strip().splitlines()[-1])['review_pin']!=pr or review.get('failure','MISSING')is not None or review.get('source_only')is not True or not review.get('status','').startswith('PASS')or review.get('numerical_executed')is not False:raise RuntimeError('exact independent Source0 review')
 generated=terminal0(gen,'actual_Source_preparation_return');observed=json.loads(generated['output'].strip().splitlines()[-1])
 raw,host=pin(HERE/'run_actual_saved_full370_terminal_source_original_guard.py');ast.parse(raw);readyraw,pready=pin(HERE/'SAVED370_SOURCE_REVIEW_READY.json');ready=json.loads(readyraw);binding=read(ready['input_binding_pin']);inv=read(ready['inverse_pin'])
 if any(observed.get(k)is not False for k in('compiler_executed','numerical_executed','pipeline_executed','files_deleted'))or any(observed[k]!=ready[v]for k,v in(('host_source','host_source'),('input_binding_pin','input_binding_pin'),('inverse_pin','inverse_pin')))or observed['ready_pin']!=pready or host!=ready['host_source']:raise RuntimeError('genuine Source-generation exact candidate PFs')
 restored=raw.decode()
 for c in reversed(inv['changes']):
  if restored.count(c['after'])!=1:raise RuntimeError('exact inverse uniqueness')
  restored=restored.replace(c['after'],c['before'],1)
 oldraw,oldhost=pin(OLD/'run_actual_saved_full370_terminal_source_original_guard.py')
 if restored.encode()!=oldraw or inv['original_pin']!=oldhost or inv['candidate_pin']!=host or inv.get('whole_inverse_bytes_equal')is not True:raise RuntimeError('whole original guard/MRO/science/TMP/caps source inverse')
 own=[host,pready,ready['input_binding_pin'],ready['inverse_pin'],ready['preparer_source_pin'],ready['actual_binding_spec_pin'],pin(__file__)[1],pg]
 reviewed=list(collect(review))
 if any(p not in reviewed for p in own):raise RuntimeError('peer review exact candidate/preparer/writer/source-generation PFs')
 spec=read(ready['actual_binding_spec_pin']);upstream=ready['actual_latest_full50_authority_pins']
 if upstream!=binding['actual_latest_full50_authority_pins']or upstream!=spec['actual_latest_full50_authority_pins']or ready['actual_latest_full50_post_contract']!=binding['actual_latest_full50_post_contract']:raise RuntimeError('one exact upstream success authority declaration')
 # Execute only the already independently reviewed pure metadata admission.
 tree=ast.parse(raw);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='verify_latest_full50_authority');ns={'Path':Path,'json':json,'pin':lambda p:pin(p)[1]};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<pure-reviewed-upstream-admission>','exec'),ns);ns['verify_latest_full50_authority'](binding)
 oldsfraw,oldsfpin=pin(OLD/'COMPLETE_SAVED_FULL370_GUARD_HOST_SOURCE_FREEZE.json');oldsf=json.loads(oldsfraw)
 fixed=unique(oldsf['fixed_source_files']+own+[oldsfpin,pr,pt]+list(upstream.values()));current7(fixed)
 HF=HERE/'COMPLETE_SAVED_FULL370_GUARD_HOST_SOURCE_FREEZE.json';CLI=HERE/'ROOT_REVIEWABLE_EXACT_SAVED_FULL370_V3_ARGV_SOURCE_ONLY.json'
 if HF.exists()or CLI.exists()or Path(ready['planned_output_root']).exists()or Path(ready['planned_TMP_output_root']).exists():raise RuntimeError('one fresh HF CLI and unexecuted output namespaces')
 frozen=dict(oldsf);frozen.update(fixed_source_files=fixed,input_binding_pin=ready['input_binding_pin'],host_pin=host,actual_Source_revision=3,predecessor_original_saved_v2_Host_freeze_pin=oldsfpin,actual_latest_full50_authority_pins=upstream,actual_latest_full50_post_contract=ready['actual_latest_full50_post_contract'],independent_Source_review_pin=pr,independent_Source_tools_pin=pt,actual_Source_generation_tools_pin=pg,own_once_writer_Source_pin=pin(__file__)[1],science_executed=False,actual_saved370_report_pin=None,original_guard_science1129_TMP_budget_MRO_math_wholebytes_unchanged=True)
 hf=write(HF,frozen)
 oldcli=json.loads((OLD/'ROOT_REVIEWABLE_EXACT_SAVED_FULL370_V2_ARGV_SOURCE_ONLY.json').read_bytes());args=oldcli['argv'][:11]+[host['path'],'--freeze-sha256',hf['sha256'],'--freeze-seven-id',json.dumps(hf['identity'],separators=(',',':'))]
 if len(args)!=16:raise RuntimeError('exact original saved Host16 argv')
 interface=dict(oldcli);interface.update(schema='SOURCE_ONLY_REAL_SAVED_FULL370_AFTER_ACTUAL_V18_ARGV_V3',argv=args,exact_reviewable_argv=args,shell_safe_command=shlex.join(args),Source_freeze_pin=hf,host_pin=host,input_binding_pin=ready['input_binding_pin'],planned_actual_ART_output=ready['planned_output_root'],planned_actual_TMP_output=ready['planned_TMP_output_root'],actual_latest_full50_authority_pins=upstream,actual_Source_revision=3,science_imported_or_executed=False,actual_saved370_report_pin=None)
 current7(fixed);cli=write(CLI,interface);print(json.dumps(dict(host_source=host,host_freeze_pin=hf,CLI_pin=cli,current_fixed_count=len(fixed),actual_argv_count=16,compiler_executed=False,numerical_executed=False,pipeline_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
