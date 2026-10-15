"""Fixed TMP-only finalization metadata reader; no business imports or calls."""
from pathlib import Path
import hashlib,json,math,os,stat,struct,sys

BASE=Path('/private/tmp/axmat_v9_cold_actual_finalization_postterminal_scope_20261009')
FIELDS=('dev','ino','mode','size','mtime_ns','ctime_ns','nlink')
PINS=[]
def check(v,message):
 if not v:raise ValueError(message)
def identity(p):
 s=p.lstat();return [getattr(s,'st_'+k) for k in FIELDS]
def raw(p,wanted=None):
 p=Path(p);check(p.is_absolute() and '..' not in p.parts,'absolute path')
 for q in (p,*p.parents):
  s=q.lstat();check(not stat.S_ISLNK(s.st_mode) and (stat.S_ISREG(s.st_mode) if q==p else stat.S_ISDIR(s.st_mode)),'nonalias regular source')
 before=identity(p);b=p.read_bytes();check(before==identity(p),'read identity changed');h=hashlib.sha256(b).hexdigest()
 if wanted is not None:check(type(wanted)is str and len(wanted)==64 and h==wanted,'known pin changed '+str(p))
 PINS.append(dict(path=str(p),sha256=h,bytes=len(b)));return b
def pairs(items):
 d={}
 for k,v in items:check(k not in d,'duplicate key');d[k]=v
 return d
def strict(p,wanted=None):
 def finite(t):
  v=float(t);check(math.isfinite(v),'nonfinite JSON float');return v
 def reject(t):raise ValueError('nonfinite JSON constant '+t)
 v=json.loads(raw(p,wanted),object_pairs_hook=pairs,parse_float=finite,parse_constant=reject);check(type(v)is dict,'object required');return v
def typed(v):
 if v is None:return ['None']
 if type(v)is bool:return ['bool',v]
 if type(v)is int:return ['int',str(v)]
 if type(v)is float:return ['float64',struct.pack('!d',v).hex()]
 if type(v)is str:return ['str',v]
 if type(v)is list:return ['list',[typed(x) for x in v]]
 if type(v)is dict:return ['dict_ordered',[[typed(k),typed(x)] for k,x in v.items()]]
 raise ValueError('unexpected metadata type')
def typed_sha(v):return hashlib.sha256(json.dumps(typed(v),ensure_ascii=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def namespace(root):
 files={};dirs=[];links={}
 for folder,ds,ns in os.walk(root,followlinks=False):
  for n in ds+ns:
   p=Path(folder)/n;r=str(p.relative_to(root));s=p.lstat()
   if stat.S_ISLNK(s.st_mode):links[r]=os.readlink(p)
   elif stat.S_ISDIR(s.st_mode):dirs.append(r)
   elif stat.S_ISREG(s.st_mode):files[r]=identity(p)
   else:raise ValueError('unsupported namespace type')
 return dict(files=files,directories=sorted(dirs),symlinks=links)
def main():
 check(Path(__file__).resolve().parent==BASE and len(sys.argv)==2,'fixed TMP-only reader')
 c=strict(sys.argv[1]);f=c['future_actual'];a=f['actual_tool_result']
 check(c['status']=='ROOT_TRUE_FINALIZATION_EXIT0_READY_FOR_READONLY_REVIEW' and f['Root_actual_closed_EXIT0_observed']is True and type(a)is dict,'UNREADY no actual finalization terminal')
 check(set(a)=={'initial_chunk_id','session_id','terminal_chunk_id','exit_code'} and type(a['exit_code'])is int and a['exit_code']==0 and all(type(a[k])is str and a[k] for k in ('initial_chunk_id','terminal_chunk_id')) and (a['session_id']is None or type(a['session_id'])is int and a['session_id']>0),'genuine builtin-int Root EXIT0 four-key tool')
 for p,h in c['known_files'].items():raw(p,h)
 old_path=Path(c['work'])/'prepared.json';cold_path=Path(c['work'])/'prepared_cold.json';old_bytes=raw(old_path,c['original_prepared_sha256']);old=strict(old_path,c['original_prepared_sha256']);new=strict(cold_path,f['prepared_cold_sha256'])
 check(old['classification']=='PREPARED_NO_TRANSPORT' and 'own_child_supervision' not in old and set(new)==set(old)|{'own_child_supervision'},'only own_child_supervision may be added')
 inverse=dict(new);supervision=inverse.pop('own_child_supervision')
 check(typed(inverse)==typed(old) and typed_sha(inverse)==c['original_prepared_typed_order_floatbits_sha256'],'whole original type/order/list/value/float64bits inverse')
 reconstructed=(json.dumps(inverse,indent=2,allow_nan=False)+'\n').encode()
 check(reconstructed==old_bytes,'full serialization byte inverse to original prepared')
 check(typed(supervision)==typed(c['expected_supervision']),'complete exact descriptor structure/order/values')
 for d in (supervision['binding'],supervision['controls']['seal'],supervision['controls']['terminal_evidence']):raw(d['path'],d['sha256'])
 e=strict(f['finalization_Root_receipt']['path'],f['finalization_Root_receipt']['sha256'])
 check(e['schema']=='AXMAT_ROOT_ACTUAL_COLD_FINALIZATION_RETURN_V1' and e['record_producer']=='root' and e['actual_tool_terminal_return_observed']is True and e['record_written_after_actual_terminal_return']is True and e['actual_tool_result']==a and type(e['actual_tool_result']['exit_code'])is int and type(e['returncode'])is int and e['returncode']==0 and e['command']==c['launch_command'] and e['source']==c['factory'] and e['scientific_qualification']is False and e['transport_started']is False,'genuine Root actual finalization witness')
 terminal=Path(c['terminal']);out=Path(e['full_stdout']['path']);err=Path(e['full_stderr']['path']);check(out.parent==err.parent==terminal and Path(f['finalization_Root_receipt']['path'])==terminal/'finalization_terminal_return.json' and len({out,err,Path(f['finalization_Root_receipt']['path'])})==3,'distinct independent original terminal stdout/stderr')
 value=strict(out,e['full_stdout']['sha256']);raw(err,e['full_stderr']['sha256'])
 expected=dict(classification='PREPARED_COLD_INPUT_AND_ACTUAL_NEW_BINDING_CONTROLS_ONLY',original_prepared=dict(path=str(old_path),sha256=c['original_prepared_sha256']),prepared=dict(path=str(cold_path),sha256=f['prepared_cold_sha256']),scientific_qualification=False,AAA_accuracy_qualified=False,ABA_admitted=False)
 check(value==expected and all(type(value[k])is bool for k in ('scientific_qualification','AAA_accuracy_qualified','ABA_admitted')) and e['prepared_cold']==expected['prepared'] and e['actual_stdout_result']==value and e['input_declaration_terminal_evidence']==c['declaration_terminal'],'whole actual stdout and terminal prepared/decl descriptors')
 namespaces={}
 for key,root in c['roots'].items():
  n=namespace(Path(root));previous=c['original_namespaces'][key];added=set(n['files'])-set(previous['files']);allowed={'prepared_cold.json'} if key=='work' else {'finalization.stdout','finalization.stderr','finalization_terminal_return.json'} if key=='terminal' else set()
  check(added==allowed and not(set(previous['files'])-set(n['files'])) and all(n['files'][p]==v for p,v in previous['files'].items()) and n['directories']==previous['directories'] and n['symlinks']==previous['symlinks'],'whole original namespace preservation and exact finalization increment '+key);namespaces[key]=dict(regular_files=len(n['files']),new_files=sorted(added),original_all_seven_fields_exact=True)
 for p,h in c['known_files'].items():raw(p,h)
 report=dict(status='PASS_ACTUAL_FINALIZATION_METADATA_ONLY_NO_NATIVE_CREDIT',prepared=expected['prepared'],original_prepared=expected['original_prepared'],whole_original_typed_order_float64bits_inverse_exact=True,whole_original_serialized_byte_inverse_exact=True,only_own_child_supervision_added=True,supervision=supervision,namespaces=namespaces,actual_Root_tool=a,reference250_legacy_and_separate2000_eight_gate_contract_unchanged=True,scientific_qualification=False,AAA_accuracy_qualified=False,ABA_admitted=False,native_executed_by_reader=False,business_import_callback_API_executed=False,source_scope_read_pins=PINS)
 p=BASE/'actual_finalization_readonly_REPORT.json';check(not p.exists(),'one actual report');p.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+'\n');print(json.dumps(dict(status=report['status'],report=dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()),science_credit=False)))
if __name__=='__main__':main()
