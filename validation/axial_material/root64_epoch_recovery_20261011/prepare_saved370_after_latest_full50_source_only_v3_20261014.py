"""Source-only saved370 entry; actual full50 closure is mandatory, not supplied yet."""
import argparse,ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'saved_full370_terminal_audit_host_source_v2'
NEW=R/'saved_full370_after_latest_full50_source_v3_20261014'
NEW_OUT='/Users/wen/spot/validation/artifacts/axial-material-AAA-saved-full370-after-latest-full50-20261014-v3'
NEW_TMP='/private/tmp/SPOT_AAA_full370_after_latest_full50_ACTUAL_ONCE_20261014_v3'
ACTUAL_KEYS=('report','Host_freeze','CLI','Root_tools','Root_argv','post_review','post_tools')
POST_FIELDS=('report','Host_freeze','CLI','Root_tools','Root_argv','ordered50_verified','expected33_verified')
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat()
 if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('only bounded ordinary Source/metadata EOF')
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  if ident(os.fstat(f.fileno()))!=ident(s):raise RuntimeError('opened7')
  data=f.read()
  if ident(os.fstat(f.fileno()))!=ident(s):raise RuntimeError('EOF7')
 if ident(p.lstat())!=ident(s):raise RuntimeError('after7')
 return dict(path=str(p),sha256=hashlib.sha256(data).hexdigest(),size_bytes=len(data),identity=ident(s))
def full(p):
 if not isinstance(p,dict)or set(p)!={'path','sha256','size_bytes','identity'}or not isinstance(p['identity'],list)or len(p['identity'])!=7 or any(type(x)is not int for x in p['identity'])or type(p['size_bytes'])is not int or p['size_bytes']!=p['identity'][4]:raise RuntimeError('unknown future fullpin is not an authority')
 return p
def read(p):
 full(p)
 if pin(p['path'])!=p:raise RuntimeError('exact Source metadata PF')
 return json.loads(Path(p['path']).read_bytes())
def write(p,v):
 data=v if isinstance(v,bytes)else(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
 with os.fdopen(os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644),'wb')as f:f.write(data);f.flush();os.fsync(f.fileno())
 return pin(p)
ADMISSION='''def verify_latest_full50_authority(binding):
 """Only exact closed0 upstream facts; no science payload reader or qualification here."""
 import shlex
 selected=binding['actual_latest_full50_authority_pins'];contract=binding['actual_latest_full50_post_contract']
 if set(selected)!=set(('report','Host_freeze','CLI','Root_tools','Root_argv','post_review','post_tools')):raise RuntimeError('seven exact actual upstream authorities')
 if set(contract)!=set(('schema','status','fields'))or not isinstance(contract['schema'],str)or not contract['schema']or not isinstance(contract['status'],str)or not contract['status']or not isinstance(contract['fields'],dict)or set(contract['fields'])!=set(('report','Host_freeze','CLI','Root_tools','Root_argv','ordered50_verified','expected33_verified'))or any(not isinstance(v,str)or not v for v in contract['fields'].values()):raise RuntimeError('exact Source-approved latest full50 post protocol; None refused')
 values={}
 for key,row in selected.items():
  if not isinstance(row,dict)or set(row)!=set(('path','sha256','size_bytes','identity'))or pin(row['path'])!=row:raise RuntimeError('exact selected actual full50 authority fullpin')
  values[key]=json.loads(Path(row['path']).read_text())
 def terminal0(value):
  if not isinstance(value,dict)or type(value.get('exit_code'))is not int or value['exit_code']!=0 or value.get('session_id')is not None:raise RuntimeError('genuine full50 closed integer0/no session')
 report=values['report'];root=values['Root_tools'];argv=values['Root_argv'];post=values['post_review'];pt=values['post_tools'];cli=values['CLI'];hf=values['Host_freeze']
 terminal0(root['actual_terminal_return'])
 if root.get('observed_closed')is not True or type(root.get('original_integer_exit_code'))is not int or root['original_integer_exit_code']!=0 or not isinstance(argv.get('exact_argv'),list)or len(argv['exact_argv'])!=96 or shlex.split(root['exact_executed_command'])!=argv['exact_argv']or root['exact_executed_command']!=argv['exact_command']or cli['exact_reviewable_argv']!=argv['exact_argv']or argv['Host_freeze_pin']!=selected['Host_freeze']or argv['interface_pin']!=selected['CLI']:raise RuntimeError('latest actual full50 Root0/exact96/own HF CLI')
 if report.get('schema')!='ACTUAL_INDEPENDENT_AAA3_INITIAL_GLOBAL_PROJECT_BOOT_ENGINEERING_ROOT_V1'or report.get('status')!='ACTUAL_THREE_PLANE_ENGINEERING_CLOSED0_ONLY'or report.get('failure')is not None or report.get('after_check_error')is not None or report.get('engineering_three_plane_closed0')is not True or report.get('all_new_storage_entry_controls_closed')is not True or len(report['records'])!=50 or report['first_failure_secondary_errors']!=[]or type(report.get('SELF_peak_bytes'))is not int or not 0<=report['SELF_peak_bytes']<512*2**20 or type(report.get('wall_seconds'))not in (int,float)or not 0<report['wall_seconds']<1800:raise RuntimeError('actual original complete50 engineering closure; no prior singleBOOT or Source qualification')
 if pt.get('observed_closed')is not True or type(pt.get('original_integer_exit_code'))is not int or pt['original_integer_exit_code']!=0:raise RuntimeError('actual independent full50 post closed0')
 for key in ('actual_review_return','actual_postverification_return'):
  result=pt[key];terminal0(result)
  if json.loads(result['output'].strip().splitlines()[-1])['review_pin']!=selected['post_review']:raise RuntimeError('genuine independent post stdout exact PF')
 if post.get('schema')!=contract['schema']or post.get('status')!=contract['status']or post.get('failure')is not None:raise RuntimeError('exact actual full50 post contract')
 for key in ('report','Host_freeze','CLI','Root_tools','Root_argv'):
  if post[contract['fields'][key]]!=selected[key]:raise RuntimeError('post binds exact actual '+key)
 if post[contract['fields']['ordered50_verified']]is not True or post[contract['fields']['expected33_verified']]is not True:raise RuntimeError('independent actual original50 order and33 exact refusal messages')
 return dict(actual_full50_authority_pins=selected,actual_original50_post_verified=True,qualification_granted_by_saved_source=False)

'''
def validate_spec(spec):
 if spec.get('schema')!='SAVED370_AFTER_LATEST_FULL50_SOURCE_ONLY_SPEC_V3'or spec.get('source_only')is not True or any(spec.get(k)is not False for k in ('compiler_executed','numerical_executed','pipeline_executed','files_deleted')):raise RuntimeError('exact saved Source-only spec')
 for p in spec['actual_latest_full50_authority_pins'].values():full(p)
 c=spec['actual_latest_full50_post_contract']
 if not isinstance(c,dict)or set(c)!={'schema','status','fields'}or not isinstance(c['schema'],str)or not c['schema']or not isinstance(c['status'],str)or not c['status']or not isinstance(c['fields'],dict)or set(c['fields'])!=set(POST_FIELDS)or any(not isinstance(x,str)or not x for x in c['fields'].values()):raise RuntimeError('future actual post protocol None remains blocked')
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for x in ('summary','sha256','seven-id'):ap.add_argument('--binding-spec-'+x,required=True)
 a=ap.parse_args();p=pin(a.binding_spec_summary)
 if p['sha256']!=a.binding_spec_sha256 or p['identity']!=json.loads(a.binding_spec_seven_id):raise RuntimeError('actual Source binding spec full7')
 spec=read(p);validate_spec(spec)
 if spec['preparer_source_pin']!=pin(__file__):raise RuntimeError('actual selected Source preparer')
 if NEW.exists()or Path(NEW_OUT).exists()or Path(NEW_TMP).exists():raise RuntimeError('one new Source namespace; future output roots absent')
 oldhost=OLD/'run_actual_saved_full370_terminal_source_original_guard.py';before=oldhost.read_bytes();text=before.decode();changes=[]
 for old,new in [("OUT=ART/'axial-material-AAA-saved-full370-terminal-source-diagnostic-current-mount-guarded-20261013-v2'","OUT=Path("+repr(NEW_OUT)+")"),("TMP_OUT=Path('/private/tmp/SPOT_AAA_full370_terminal_source_CURRENT_MOUNT_ACTUAL_ONCE_20261013_v2')","TMP_OUT=Path("+repr(NEW_TMP)+")"),("def main():\n",ADMISSION+"def main():\n"),(" verify(freeze['fixed_source_files']);binding=json.loads(BIND.read_text())"," verify(freeze['fixed_source_files']);binding=json.loads(BIND.read_text())\n upstream_actual_admission=verify_latest_full50_authority(binding)")]:
  if text.count(old)!=1:raise RuntimeError('one exact saved Host Source splice')
  text=text.replace(old,new,1);changes.append(dict(before=old,after=new))
 restored=text
 for row in reversed(changes):restored=restored.replace(row['after'],row['before'],1)
 if restored.encode()!=before:raise RuntimeError('whole original guard Host inverse')
 ast.parse(text);binding=read(spec['selected_original_binding_pin']);binding['actual_latest_full50_authority_pins']=spec['actual_latest_full50_authority_pins'];binding['actual_latest_full50_post_contract']=spec['actual_latest_full50_post_contract'];binding['planned_science_command']=binding['planned_science_command'][:-1]+[NEW_TMP]
 # Pure Source metadata gate only: the scientific reader is never loaded here.
 namespace={'Path':Path,'json':json,'pin':pin};exec(compile(ADMISSION,'<pure-latest-full50-saved-source-admission>','exec'),namespace);namespace['verify_latest_full50_authority'](binding)
 NEW.mkdir();host=write(NEW/oldhost.name,text.encode());bp=write(NEW/'CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json',binding)
 ip=write(NEW/'COMPLETE_SAVED370_V2_TO_V3_SOURCE_BYTE_INVERSE.json',dict(original_pin=pin(oldhost),candidate_pin=host,changes=changes,whole_inverse_bytes_equal=True,all_original_guard_math_scientific1129_MRO_caps_and_TMP_accounting_bytes_unchanged=True))
 plan=write(NEW/'SAVED370_SOURCE_REVIEW_READY.json',dict(source_only=True,host_source=host,input_binding_pin=bp,inverse_pin=ip,original_source_freeze_pin=spec['selected_original_Host_freeze_pin'],preparer_source_pin=pin(__file__),actual_binding_spec_pin=p,actual_latest_full50_authority_pins=spec['actual_latest_full50_authority_pins'],actual_latest_full50_post_contract=spec['actual_latest_full50_post_contract'],planned_output_root=NEW_OUT,planned_TMP_output_root=NEW_TMP,actual_Host_freeze_pin=None,actual_CLI_pin=None,actual_saved370_report_pin=None,compiler_executed=False,numerical_executed=False,pipeline_executed=False,files_deleted=False))
 print(json.dumps(dict(source_only=True,host_source=host,input_binding_pin=bp,inverse_pin=ip,ready_pin=plan,compiler_executed=False,numerical_executed=False,pipeline_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
