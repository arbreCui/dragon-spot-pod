"""One pure parser metadata probe. Never imports a factory or runs business APIs."""
import argparse
import ast
import gc
import hashlib
import json
import math
import os
import resource
import stat
import sys
import time
from pathlib import Path

THREAD_KEYS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
SAFE_BUILTINS={name:getattr(__import__('builtins'),name) for name in ('ValueError','TypeError','OverflowError','RecursionError','RuntimeError','KeyError','Exception','str','bool','int','float','dict','list','tuple','set','frozenset','isinstance','type','len','all','any','enumerate','sorted','sum','zip','min','max','abs','bytes','range','id')}
FORBIDDEN_NAMES={'open','eval','exec','compile','__import__','input','globals','locals','vars','getattr','setattr','delattr','breakpoint','print','exit','quit'}

def identity(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def sha_value(value):
 assert type(value) is str and len(value)==64 and all(c in '0123456789abcdef' for c in value)
 return value

def verified(path, expected, collect=False):
 p=Path(path);assert p.is_absolute() and str(p)==path and '..' not in p.parts and p.parent.resolve(strict=True)==p.parent
 before=identity(p);assert stat.S_ISREG(before[2])
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();length=0;payload=None
 with os.fdopen(fd,'rb') as stream:
  s=os.fstat(stream.fileno());assert [s.st_dev,s.st_ino]==before[:2]
  if collect:
   payload=stream.read();length=len(payload);h.update(payload)
  else:
   while block:=stream.read(1024**2):h.update(block);length+=len(block)
 assert identity(p)==before and length==before[3] and h.hexdigest()==sha_value(expected)
 return dict(path=path,identity=before,size=length,sha256=h.hexdigest()),payload

def atomic(path,value,replace=False):
 p=Path(path);temporary=p.with_name(p.name+'.pending-'+str(os.getpid()))
 data=(json.dumps(value,sort_keys=True,allow_nan=False)+'\n').encode()
 with temporary.open('xb') as out:out.write(data);out.flush();os.fsync(out.fileno())
 if replace:os.replace(temporary,p)
 else:
  try:os.link(temporary,p)
  finally:temporary.unlink()

def event(case,phase,sequence):
 value=dict(schema='ISOLATED_METADATA_PARSER_REAL_PHASE_OBSERVATION_V1',worker_pid=os.getpid(),phase=phase,sequence=sequence,monotonic=time.monotonic(),scope='PARSER_METADATA_DIAGNOSTIC_ONLY')
 atomic(case/'latest_phase.json',value,replace=True)
 print(json.dumps(value),flush=True)

def extract_parser(payload):
 source=payload.decode('utf-8');tree=ast.parse(source)
 matches=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='strict_json_bytes']
 assert len(matches)==1
 node=matches[0]
 assert len(node.args.args)==1 and node.args.args[0].arg=='raw' and not node.args.posonlyargs and not node.args.kwonlyargs and node.args.vararg is None and node.args.kwarg is None and not node.args.defaults and not node.decorator_list
 for item in ast.walk(node):
  assert not isinstance(item,(ast.Import,ast.ImportFrom,ast.Global,ast.ClassDef,ast.AsyncFunctionDef,ast.Await,ast.Yield,ast.YieldFrom))
  if isinstance(item,ast.Name):assert item.id not in FORBIDDEN_NAMES,item.id
  if isinstance(item,ast.Attribute):assert not item.attr.startswith('__'),item.attr
  if isinstance(item,(ast.Assign,ast.AnnAssign,ast.AugAssign)):
   targets=item.targets if isinstance(item,ast.Assign) else [item.target]
   for target in targets:
    assert not (isinstance(target,ast.Attribute) and isinstance(target.value,ast.Name) and target.value.id in ('json','math'))
 namespace={'json':json,'math':math,'__builtins__':SAFE_BUILTINS}
 exec(compile(ast.Module(body=[node],type_ignores=[]),'<isolated strict_json_bytes AST only>','exec'),namespace)
 assert set(namespace)=={'json','math','__builtins__','strict_json_bytes'}
 body=''.join(source.splitlines(keepends=True)[node.lineno-1:node.end_lineno])
 return namespace['strict_json_bytes'],namespace,hashlib.sha256(body.encode()).hexdigest()

def plain_types_and_order(value):
 counts={};mutable=set();shape=hashlib.sha256()
 def walk(item):
  kind=type(item);assert kind in (dict,list,str,int,float,bool,type(None)),kind
  label=kind.__name__;counts[label]=counts.get(label,0)+1;shape.update(label.encode()+b':')
  if kind in (dict,list):
   assert id(item) not in mutable,'mutable JSON containers were aliased';mutable.add(id(item));shape.update(str(len(item)).encode()+b'[')
   if kind is dict:
    for key,part in item.items():
     assert type(key) is str;shape.update(json.dumps(key,ensure_ascii=True,separators=(',',':')).encode());walk(part)
   else:
    for part in item:walk(part)
   shape.update(b']')
  elif kind is float:assert math.isfinite(item)
 walk(value)
 mutable.clear()
 return counts,shape.hexdigest()

def maxrss():
 raw=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 divisor=1024**2 if sys.platform=='darwin' else 1024 if sys.platform.startswith('linux') else None
 return dict(raw=raw,platform=sys.platform,unit='bytes' if sys.platform=='darwin' else 'KiB' if divisor else 'unknown',MiB=None if divisor is None else raw/divisor,supplement_only_not_own_PID_ps_gate=True)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--source',required=True);parser.add_argument('--source-sha',required=True);parser.add_argument('--data',required=True);parser.add_argument('--data-sha',required=True);parser.add_argument('--case-dir',required=True)
 a=parser.parse_args();case=Path(a.case_dir)
 assert case.is_absolute() and str(case)==a.case_dir and case.resolve(strict=True)==case
 assert sys.version_info[:2]==(3,12) and __debug__ and sys.dont_write_bytecode
 assert all(os.environ.get(k)=='1' for k in THREAD_KEYS) and 'PYTHONPATH' not in os.environ and 'PYTHONOPTIMIZE' not in os.environ
 source_before,source_payload=verified(a.source,a.source_sha,collect=True)
 function,namespace,function_sha=extract_parser(source_payload);del source_payload
 event(case,'stdlib_and_parser_AST_loaded',1);time.sleep(.2)
 data_before,raw=verified(a.data,a.data_sha,collect=True)
 event(case,'raw_verified_before_parse',2);time.sleep(.2)
 parse_before_maxrss=maxrss()
 event(case,'parse_active',3)
 started=time.monotonic();value=function(raw);parse_seconds=time.monotonic()-started
 parse_after_maxrss=maxrss()
 assert set(namespace)=={'json','math','__builtins__','strict_json_bytes'}
 event(case,'parse_return_value_and_raw_retained',4);time.sleep(.2)
 del raw
 event(case,'parsed_value_retained_raw_released',5);time.sleep(.2)
 event(case,'plain_type_order_and_full_output_digest',6)
 types,shape=plain_types_and_order(value);h=hashlib.sha256();encoded_bytes=0
 for piece in json.JSONEncoder(sort_keys=False,separators=(',',':'),ensure_ascii=True,allow_nan=False).iterencode(value):
  b=piece.encode('utf-8');h.update(b);encoded_bytes+=len(b)
 event(case,'parsed_value_retained_after_validation',7);time.sleep(.2)
 data_after,_=verified(a.data,a.data_sha);source_after,_=verified(a.source,a.source_sha)
 assert source_before==source_after and data_before==data_after
 event(case,'after_fresh_pins_value_retained',8);time.sleep(.2)
 supplemental=maxrss()
 del value;gc.collect()
 event(case,'parsed_value_released_with_explicit_gc',9);time.sleep(.2)
 value=dict(schema='ISOLATED_COMPLETE_METADATA_PARSER_CHILD_REPORT_V1',classification='PARSED_METADATA_DIAGNOSTIC_ONLY',worker_pid=os.getpid(),source_before=source_before,source_after=source_after,extracted_function_sha256=function_sha,data_before=data_before,data_after=data_after,plain_builtin_type_counts=types,type_and_insertion_order_shape_sha256=shape,whole_insertion_order_JSON_output_sha256=h.hexdigest(),whole_insertion_order_JSON_output_bytes=encoded_bytes,mutable_container_independence=True,parse_seconds=parse_seconds,rusage_before_parse=parse_before_maxrss,rusage_immediately_after_parse=parse_after_maxrss,rusage_maxrss=supplemental,rusage_scope='Historical whole-process high-water counters, not allocation sizes or a ps RSS gate. Digest/type validation and fresh-file checks occur after the parse-return event.',thread_environment={k:os.environ[k] for k in THREAD_KEYS},python_executable=sys.executable,bytecode_disabled=sys.dont_write_bytecode,optimization_disabled=__debug__,parser_globals=['json','math','restricted builtins','AST extracted strict_json_bytes'],business_import_or_API_or_constructor_or_PREP_RUN=False,native_or_science_credit=False)
 atomic(case/'child_report.json',value)
 event(case,'child_report_atomically_complete',10)
 print(json.dumps(dict(schema='ISOLATED_PARSER_FINAL_REPORT_POINTER_V1',report=str(case/'child_report.json'),classification='PARSER_METADATA_DIAGNOSTIC_ONLY')),flush=True)

if __name__=='__main__':main()
