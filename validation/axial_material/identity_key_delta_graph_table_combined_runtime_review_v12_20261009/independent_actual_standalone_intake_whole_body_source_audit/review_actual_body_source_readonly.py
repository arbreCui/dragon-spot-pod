"""Independent stdlib-only metadata reader. Never imports/calls production code.
No graph/scientific payload rescan, API, CLI, fixtures, native job or Root polling.
All writes are exclusively to this new /private/tmp evidence directory.
"""
import ast
import collections
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import struct

ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
REVIEW=ROOT/'validation/axial_material/identity_key_delta_graph_table_combined_runtime_review_v12_20261009'
DUR=ART/'axial-material-owned-specs-identity-key-delta-graph-table-v12-standalone-bounded-runtime-api-intake-evidence-20261009'
OUT=ART/'axial-material-owned-specs-identity-key-delta-graph-table-combined-runtime-v12-20261009'
SOURCE=ART/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-combined-source-v12-20261009'
TERM=ART/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-combined-terminal-v12-20261009'
FACTORY=ROOT/'validation/axial_material/prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.py'
GRAPH=ROOT/'validation/axial_material/combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py'
SPECS=ROOT/'validation/axial_material/combined_runtime_complete_historical_input_specs_20261007.json'
DEST=Path('/private/tmp/axmat_v12_actual_intake_whole_body_source_independent_readonly_20261009')
PINS={str(FACTORY):'5af1feebc7d40549750e1daec6148ae073a4c85c1eb3242485e6d9e80826861b',str(GRAPH):'e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28',str(SPECS):'2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa',str(DUR/'Root_terminal_return.json'):'449d08d08cdfe7cb19eaf3a882312f8d6c21725011650289608e4bae601178bf',str(DUR/'intake/admit.log'):'65fc18ba1fab484b91c626a48d79a55a9bd5f21b65a391d18b9c4313e2333536'}
checks={};observed={};documents={};findings=[]

def need(name,condition,detail=None):
 checks[name]=bool(condition)
 if not condition:
  findings.append(dict(check=name,detail=detail));raise AssertionError(name+': '+str(detail))
def signature(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def valid_sha(v):return type(v)is str and len(v)==64 and all(c in '0123456789abcdef'for c in v)
def ordinary(p):
 p=Path(p);need('absolute_normal:'+str(p),p.is_absolute()and os.path.normpath(str(p))==str(p)and '..'not in p.parts)
 for q in [*reversed(p.parents),p]:
  s=q.lstat();need('no_symlink:'+str(q),not stat.S_ISLNK(s.st_mode))
  if q!=p:need('directory_ancestor:'+str(q),stat.S_ISDIR(s.st_mode))
 return p

def fresh(p,expected=None,collect=False):
 p=ordinary(p);key=str(p)
 expected=expected or PINS.get(key)
 if key in observed:
  need('cached_reader_identity_still_current:'+key,signature(p.stat())==observed[key]['seven_identity'])
  if expected is not None:need('same_expected_sha:'+key,observed[key]['sha256']==expected)
  if not collect:return observed[key],None
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);parts=[] if collect else None;h=hashlib.sha256();n=0
 try:
  before=os.fstat(fd);need('regular_file:'+key,stat.S_ISREG(before.st_mode));need('metadata_read_bound:'+key,before.st_size<=70*2**20)
  while True:
   block=os.read(fd,2**20)
   if not block:break
   n+=len(block);h.update(block)
   if collect:parts.append(block)
  after=os.fstat(fd);need('fresh_identity_stable:'+key,signature(before)==signature(after)==signature(p.stat())and n==after.st_size)
 finally:os.close(fd)
 value=dict(path=key,sha256=h.hexdigest(),bytes=n,seven_identity=signature(after))
 if expected is not None:need('fresh_expected_sha:'+key,valid_sha(expected)and value['sha256']==expected)
 observed[key]=value
 return value,b''.join(parts)if collect else None

def strict(p,expected=None):
 key=str(p)
 if key in documents:
  fresh(p,expected);return documents[key]
 pin,raw=fresh(p,expected,True)
 def pairs(items):
  result={}
  for k,v in items:
   if k in result:raise ValueError('duplicate JSON key '+k)
   result[k]=v
  return result
 def reject(x):raise ValueError('nonfinite JSON constant '+x)
 def finite(x):
  value=float(x)
  if not math.isfinite(value):raise ValueError('nonfinite JSON number')
  return value
 result=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=reject,parse_float=finite)
 documents[key]=result;return result

def scalar_equal(a,b):
 if type(a)is not type(b):return False
 if type(a)is float:return struct.pack('>d',a)==struct.pack('>d',b)
 return a==b

def equal(a,b,order=True):
 todo=[(a,b,'')];count=0;types=collections.Counter();float_count=0;negative_zero=0
 while todo:
  x,y,p=todo.pop();count+=1;types[type(x).__name__]+=1
  if type(x)is not type(y):return False,dict(nodes=count,mismatch=p,reason='type',left=type(x).__name__,right=type(y).__name__)
  if type(x)is dict:
   if set(x)!=set(y):return False,dict(nodes=count,mismatch=p,reason='dict key set')
   if order and list(x)!=list(y):return False,dict(nodes=count,mismatch=p,reason='dict insertion order',left_keys=list(x),right_keys=list(y))
   todo.extend((x[k],y[k],p+'/'+k)for k in reversed(list(x)))
  elif type(x)is list:
   if len(x)!=len(y):return False,dict(nodes=count,mismatch=p,reason='list length')
   todo.extend((x[i],y[i],p+'/'+str(i))for i in range(len(x)-1,-1,-1))
  elif type(x)is float:
   float_count+=1;negative_zero+=int(x==0.0 and struct.pack('>d',x)==b'\x80'+b'\x00'*7)
   if not scalar_equal(x,y):return False,dict(nodes=count,mismatch=p,reason='float binary64 bits')
  elif not scalar_equal(x,y):return False,dict(nodes=count,mismatch=p,reason='scalar value')
 return True,dict(nodes=count,types=dict(types),float_binary64_count=float_count,negative_zero_count=negative_zero,dict_order_checked=order,list_order_checked=True,exact_scalar_types_checked=True)

def checked_equal(name,a,b,order=True):
 passed,detail=equal(a,b,order);need(name,passed,detail);return detail

def sorted_view(value):
 if type(value)is dict:return {k:sorted_view(value[k])for k in sorted(value)}
 if type(value)is list:return [sorted_view(v)for v in value]
 return value

def typed_sha(value):
 h=hashlib.sha256();todo=[('value',value)]
 while todo:
  role,v=todo.pop()
  if role=='key':h.update(b'K'+str(len(v.encode('utf-8'))).encode()+b':'+v.encode('utf-8'));continue
  if type(v)is dict:
   h.update(b'D'+str(len(v)).encode()+b':')
   for k in reversed(list(v)):todo.extend([('value',v[k]),('key',k)])
  elif type(v)is list:
   h.update(b'L'+str(len(v)).encode()+b':');todo.extend(('value',x)for x in reversed(v))
  elif type(v)is str:h.update(b'S'+str(len(v.encode('utf-8'))).encode()+b':'+v.encode('utf-8'))
  elif type(v)is float:h.update(b'F'+struct.pack('>d',v))
  elif type(v)is bool:h.update(b'T'if v else b'B')
  elif type(v)is int:h.update(b'I'+str(v).encode()+b';')
  elif v is None:h.update(b'N')
  else:raise TypeError(type(v))
 return h.hexdigest()

def descriptor(p):
 pin,_=fresh(p);return dict(path=pin['path'],sha256=pin['sha256'])

# Tiny whitelist interpreter reads ONLY source literals and the single return
# expression. It executes no function, import, control flow or source program.
def expression(node,env):
 if isinstance(node,ast.Constant):return node.value
 if isinstance(node,ast.Name):return env[node.id]
 if isinstance(node,(ast.List,ast.Tuple)):
  values=[expression(v,env)for v in node.elts];return tuple(values)if isinstance(node,ast.Tuple)else values
 if isinstance(node,ast.Dict):
  result={}
  for k,v in zip(node.keys,node.values):
   if k is None:result.update(expression(v,env))
   else:result[expression(k,env)]=expression(v,env)
  return result
 if isinstance(node,ast.Subscript):return expression(node.value,env)[expression(node.slice,env)]
 if isinstance(node,ast.BinOp):
  a,b=expression(node.left,env),expression(node.right,env)
  if isinstance(node.op,ast.Add):return a+b
  if isinstance(node.op,ast.Div)and isinstance(a,Path):return a/b
  if isinstance(node.op,ast.Mult):return a*b
  if isinstance(node.op,ast.Pow):return a**b
 if isinstance(node,ast.Call)and isinstance(node.func,ast.Name):
  name=node.func.id
  if name=='dict':
   result={}
   for arg in node.args:result.update(expression(arg,env))
   for kw in node.keywords:
    if kw.arg is None:result.update(expression(kw.value,env))
    else:result[kw.arg]=expression(kw.value,env)
   return result
  if name=='str'and len(node.args)==1:return str(expression(node.args[0],env))
  if name=='Path'and len(node.args)==1:return Path(expression(node.args[0],env))
  if name=='pin'and len(node.args)==1:
   # Recognize production's pin syntax; substitute independent reader metadata.
   return descriptor(expression(node.args[0],env))
 raise ValueError('Unsupported source expression '+ast.dump(node)[:200])

def source_constants(tree):
 env={}
 for node in tree.body:
  if isinstance(node,ast.Assign)and all(isinstance(t,ast.Name)for t in node.targets):
   try:value=expression(node.value,env)
   except (ValueError,KeyError,TypeError):continue
   for target in node.targets:env[target.id]=value
 return env

def function(tree,name):return next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name==name)

def namespace(root,wanted,include_directories=True):
 root=ordinary(root);files={};links={};dirs=[]
 for current,folders,names in os.walk(root,followlinks=False):
  rp=Path(current).relative_to(root)
  if rp.parts:dirs.append(str(rp))
  for name in folders+names:
   p=Path(current)/name
   if p.is_symlink():links[str(p.relative_to(root))]=os.readlink(p)
  for name in names:
   p=Path(current)/name
   if not p.is_symlink():files[str(p.relative_to(root))]=fresh(p,wanted['files'].get(str(p.relative_to(root))))[0]['sha256']
 actual=dict(files=files,symlinks=links)
 if include_directories:actual['directories']=sorted(dirs)
 checked_equal('exact_namespace:'+str(root),sorted_view(actual),sorted_view(wanted))
 return dict(root=str(root),file_count=len(files),regular_file_bytes=sum(observed[str(root/p)]['bytes']for p in files),directories=sorted(dirs),symlinks=links)

def inverse(candidate,regions,mother,name):
 restored=candidate
 for row in reversed(regions):
  old,new=row['old'],row['new'];label=row.get('region',row.get('name','unnamed'))
  need('unique_inverse:'+name+':'+label,restored.count(new)==1)
  restored=restored.replace(new,old,1)
 need('complete_inverse:'+name,restored==mother)
 return hashlib.sha256(restored.encode()).hexdigest()

root_receipt=strict(DUR/'Root_terminal_return.json')
body=strict(DUR/'intake/admit.log')
need('Root_actual_typed_zero',type(root_receipt['actual_exit_code'])is int and root_receipt['actual_exit_code']==0 and type(root_receipt['actual_tool']['exit_code'])is int and root_receipt['actual_tool']['exit_code']==0)
need('Root_postterminal_true',root_receipt['record_written_after_actual_tool_return']is True)
factory_pin,factory_raw=fresh(FACTORY,collect=True);factory_text=factory_raw.decode();tree=ast.parse(factory_text);env=source_constants(tree)
graph_pin,graph_raw=fresh(GRAPH,collect=True);graph_text=graph_raw.decode()
need('actual_source_factory5af',factory_pin['sha256']==PINS[str(FACTORY)])
need('actual_source_graph_e8',graph_pin['sha256']==PINS[str(GRAPH)])
need('host_actual_factory5af_binding',"FACTORY_SHA='"+factory_pin['sha256']+"'"in fresh(DUR/'host.py',root_receipt['host_source']['sha256'],True)[1].decode())
need('factory_actual_e8_binding',env['INPUT_HELPERS']['graph']==(GRAPH,graph_pin['sha256']))

# Immutable V12 declarations and sealed metadata are independently reread.
d=strict(OUT/'declaration.json','410720642a1952480ad9190ed48292e96cf9f17d8ab02967b5503713caa09f5d')
seal=strict(OUT/'seal.json',body['build_seal_sha256']);run=strict(body['actual_external_terminal_evidence']['path'],body['actual_external_terminal_evidence']['sha256'])
prep=strict(body['actual_prepare_terminal_evidence']['path'],body['actual_prepare_terminal_evidence']['sha256'])
for name,e in [('RUN',run),('PREP',prep)]:
 need(name+'_genuine_Root_closed_typed_zero',e['record_producer']=='root'and e['actual_tool_terminal_return_observed']is True and e['record_written_after_actual_terminal_return']is True and type(e['returncode'])is int and e['returncode']==0 and type(e['actual_tool_result']['exit_code'])is int and e['actual_tool_result']['exit_code']==0)
 checked_equal(name+'_actual_source5af',e['source'],descriptor(FACTORY))
 checked_equal(name+'_actual_declaration',e['declaration'],descriptor(OUT/'declaration.json'))
need('RUN_actual_build_seal',run['build_seal']==descriptor(OUT/'seal.json'))
need('RUN_prep_pin',run['prep_terminal_evidence']==body['actual_prepare_terminal_evidence'])
need('RUN_genuine_command',run['command']==[d['python_command'],str(FACTORY),'run-build','--sha256',observed[str(OUT/'declaration.json')]['sha256'],'--prep-sha256',body['actual_prepare_terminal_evidence']['sha256']])
need('PREP_genuine_command',prep['command']==[d['python_command'],str(FACTORY),'prepare-build'])
source_snapshot=strict(prep['source_inventory']['path'],prep['source_inventory']['sha256'])
checked_equal('SOURCE_snapshot_matches_declaration',source_snapshot,d['source_inventory'])
source_inventory=namespace(SOURCE,source_snapshot)
need('SOURCE_exact_11_names',set(source_snapshot['files'])=={'historical_input_combined_runtime_factory.py','input_specs.json','source_admission.json','trim_component_admission_INPUT.json','trim_component_API_python_open_trace.json','trim_component_API_absence_INPUT.json','runtime/graph.py','runtime/codec.py','runtime/current.py','runtime/checks.py','runtime/ordinary.py'})
need('SOURCE_factory_copy5af',source_snapshot['files']['historical_input_combined_runtime_factory.py']==factory_pin['sha256'])
need('SOURCE_graph_copy_e8',source_snapshot['files']['runtime/graph.py']==graph_pin['sha256'])
source_admission=strict(SOURCE/'source_admission.json',source_snapshot['files']['source_admission.json'])
for k in ('historical_whole_component_body','historical_PREP','actual_last_cprime_trim_component_INPUT'):
 checked_equal('SOURCE_declaration_PREP_metadata:'+k,source_admission[k],d[k]);checked_equal('PREP_declaration_metadata:'+k,prep[k],d[k])
for _,(path,sha)in env['INPUT_HELPERS'].items():fresh(path,sha)
for k in ('genuine_supervisor_source','genuine_parent_class_source','actual_local_supervisor_helper'):
 fresh(d[k]['path'],d[k]['sha256'])
 checked_equal('supervisor_parent_local_helper_preflight:'+k,d[k],d['actual_supervisor_constructor_preflight'][{'actual_local_supervisor_helper':'local_bounded_helper'}.get(k,k)])

# Genuine saved historical body; no component API is invoked or reconstructed.
specs=strict(SPECS);spec_copy=strict(SOURCE/'input_specs.json',PINS[str(SPECS)])
checked_equal('SOURCE_input_specs_entire_saved_value',spec_copy,specs)
bodies=sorted_view(specs['metadata']['historical_actual_components'])
need('genuine_seven_component_key_count',len(bodies)==7)
historical_decl=strict(specs['metadata']['declaration']['path'],specs['metadata']['declaration']['sha256'])
historical_stats=checked_equal('genuine2cad_body_equals_sorted_actual_historical_declaration_entire_body',bodies,sorted_view(historical_decl['actual_components']))
need('real_2cad_nested_body_already_sortedJSON_order',equal(specs['metadata']['historical_actual_components'],bodies)[0])
need('historical_raw_declaration_dict_order_is_original_boundary',list(historical_decl['actual_components'])!=list(bodies))
seven_stats=checked_equal('actual_intake_whole_seven_body_all_values_types_orders_floatbits',body['actual_components'],bodies)
checked_equal('historical_BODY_BINDING_genuine_source_literals',body['historical_whole_component_body'],env['BODY_BINDING'])

# V11 complete actual return, saved SOURCE input and all sealed count metadata.
trim_body=strict(SOURCE/'trim_component_admission_INPUT.json',source_snapshot['files']['trim_component_admission_INPUT.json'])
genuine_trim=strict(ROOT/'validation/axial_material/identity_key_delta_full_component_review_v11_20261009/admit.stdout')
trim_stats=checked_equal('actual_V11_trim_BODY_entire_admit_equals_saved_SOURCE',trim_body,genuine_trim)
checked_equal('actual_intake_trim_BODY_entire',body['actual_last_cprime_trim_admission'],trim_body)
TRIM=env['TRIM'];TRIM_SOURCE=env['TRIM_SOURCE']
trim_seal=strict(TRIM/'seal.json',env['TRIM_SEAL_SHA']);trim_d=strict(TRIM/'declaration.json',env['TRIM_DECL_SHA'])
trim_controls=strict(TRIM/'audit/controls.json',trim_seal['files']['audit/controls.json'])
trim_audit=strict(TRIM/'audit/result.json',trim_seal['files']['audit/result.json'])
trim_driver=strict(TRIM/'driver_result.json',trim_seal['files']['driver_result.json'])
trim_stages=strict(TRIM/(trim_d['family']+'/stages.json'),trim_seal['files'][trim_d['family']+'/stages.json'])['stages']
counts=trim_body['cache_unit_control_counts'];need('V11_complete30_integer_counts',len(counts)==30 and all(type(v)is int and v>=0 for v in counts.values()))
for name,value in [('controls',trim_controls['counts']),('audit',trim_audit['control_counts']),('driver',trim_driver['control_counts'])]:checked_equal('V11_whole30_counts_equal:'+name,counts,value)
count_keys=dict(total_declared_stages=68,original_factor_diagonal_45_stages_retained=45,additional_keycodec_driver_build_stages=2,additional_keycodec_execute_stages=21,inherited_last_cprime_stages_retained=40)
for k,v in count_keys.items():need('V11_stage_count:'+k,counts[k]==v)
need('sealed68_unique_stage_labels',len(trim_stages)==68 and len({r['label']for r in trim_stages})==68)
need('sealed68_actual_watchdog_descriptors',len(trim_driver['watchdogs'])==68 and trim_driver['watchdogs'][:-1]==trim_audit['previous_stage_watchdogs'])
for i,(stage,watch_descriptor)in enumerate(zip(trim_stages,trim_driver['watchdogs'])):
 wp=TRIM/(stage['label']+'.watchdog.json');rel=str(wp.relative_to(TRIM))
 need('V11_watchdog_descriptor_pin:'+str(i),watch_descriptor['path']==str(wp)and watch_descriptor['sha256']==trim_seal['files'][rel])
 w=strict(wp,trim_seal['files'][rel])
 expected_negative=stage['label'].startswith('controls/keycodec_negative_')
 need('V11_stage_status_matches_expected_rejection:'+str(i),stage['status']==('FAILED'if expected_negative else 'PASS'))
 need('V11_stage_watch_command:'+str(i),stage['command']==w['command'])
 need('V11_stage_typed_watch_return:'+str(i),type(w['returncode'])is int and w['returncode']==(23 if expected_negative else 0))
 need('V11_stage_guard_metadata:'+str(i),w['own_child_only']is True and w['liveness_group_cleanup']is True and w['limit_failure']is None and 0<=w['sampled_peak_rss_mib']<512)
 if 'peak_rss_mib'in watch_descriptor:need('V11_watchdog_peak_descriptor:'+str(i),scalar_equal(watch_descriptor['peak_rss_mib'],w['sampled_peak_rss_mib']))
 if 'elapsed_seconds'in watch_descriptor:need('V11_watchdog_elapsed_descriptor:'+str(i),scalar_equal(watch_descriptor['elapsed_seconds'],w['elapsed_seconds']))
keycodec=trim_controls['keycodec_controls'];need('sealed21_codec_metadata_status',keycodec['status']=='PASS'and keycodec['actual_codec_controls_passed']is True and keycodec['standalone_control_count']==21 and keycodec['expected_negative_actual_rejection_count']==20)
need('sealed_V11_source_namespace_no_links',trim_d['source_inventory']['symlinks']=={})
trim_source_inventory=namespace(TRIM_SOURCE,trim_d['source_inventory'],include_directories=False)
for k,const in [('build_seal_sha256','TRIM_SEAL_SHA')]:need('V11_full_body_pin:'+k,trim_body[k]==env[const])
for k,path,const in [('compiled_kernel',env['TRIM_OBJECT'],'TRIM_OBJECT_SHA'),('compiled_kernel_source',TRIM_SOURCE/'SPOT1P64.f90','TRIM_KERNEL_SHA'),('corrected_runtime',TRIM/'runtime/Dragon','TRIM_RUNTIME_SHA'),('source_admission',TRIM_SOURCE/'source_admission.json','TRIM_SOURCE_ADMISSION_SHA'),('actual_external_terminal_evidence',env['TRIM_TERMINAL']/'terminal_return.json','TRIM_TERMINAL_SHA')]:
 fresh(path,env[const]);checked_equal('V11_actual_full_body_fresh_pin:'+k,trim_body[k],descriptor(path))
checked_equal('V11_original92_whole_ancestry',sorted_view(trim_body['inherited_rank1_factor_cache_admission']),bodies['original92'])
checked_equal('V11_memory_whole_ancestry',sorted_view(trim_body['inherited_rank1_factor_cache_memory_admission']),bodies['dedup']['inherited_rank1_factor_cache_memory_admission'])

# Parent declarations/seals, exact SOURCE namespaces, original runtime/object pins.
records={r['label']:r for r in specs['metadata']['reached_component_records']}
parent_evidence=[]
for name,source_path in [('original92',env['OLD_SOURCE']),('physical',env['PHYSICAL_SOURCE']),('dedup',env['DEDUP_SOURCE']),('capture',env['CAPTURE_SOURCE'])]:
 record=records[name];pd=strict(record['declaration']['path'],record['declaration']['sha256']);ps=strict(record['seal']['path'],record['seal']['sha256'])
 inv=namespace(source_path,pd['source_inventory'],include_directories='directories'in pd['source_inventory'])
 b=bodies[name];core=[]
 for k in ('source_admission','compiled_kernel','compiled_kernel_source','corrected_runtime','actual_external_terminal_evidence'):
  if k in b and type(b[k])is dict and set(b[k])=={'path','sha256'}:
   fresh(b[k]['path'],b[k]['sha256']);core.append(dict(field=k,**b[k]))
 if name=='capture':
  for k in ('source','declaration','capture_seal','actual_external_terminal_evidence'):
   if k in b and set(b[k])=={'path','sha256'}:fresh(b[k]['path'],b[k]['sha256']);core.append(dict(field=k,**b[k]))
 parent_evidence.append(dict(label=name,declaration=record['declaration'],seal=record['seal'],source_inventory=inv,core_fresh_pins=core))
 for obj in pd.get('build_commands',[]):
  # Do not run commands; tokens are metadata only.
  pass
for k in ('OLD_FACTORY','PHYSICAL_FACTORY','DEDUP_FACTORY','CAPTURE_FACTORY','TRIM_FACTORY','HISTORICAL_FACTORY'):
 fresh(env[k],env[k+'_SHA'])
for path in d['actual_production_objects']:fresh(path,d['files'][path])
combined_runtime=descriptor(OUT/'runtime/Dragon');need('combined_runtime_sealed_sha',combined_runtime['sha256']==seal['files']['runtime/Dragon'])
link_identity=strict(OUT/'audit/binary_identity.json',seal['files']['audit/binary_identity.json'])
need('combined_actual_link_identity_PASS',link_identity['status']=='PASS'and link_identity['exact_original92_token_inverse']is True and link_identity['sole_object_changes']==['SPOT1P64.o','SPOASM.o'])
link=list(d['production_link_command']);link[link.index(str(env['TRIM_OBJECT']))]=str(env['OLD']/'build/SPOT1P64.o');link.remove(str(env['PHYSICAL_OBJECT']));link[-1]=str(env['OLD']/'runtime/Dragon')
checked_equal('entire_original92_link_inverse_tokens',link,strict(records['original92']['declaration']['path'])['build_commands'][2])

# Static reconstruction of all 65 fields from their actual byte-pinned authorities.
full_stdout=strict(run['full_stdout']['path'],run['full_stdout']['sha256']);fresh(run['full_stderr']['path'],run['full_stderr']['sha256'])
need('RUN_complete_stderr_empty',observed[run['full_stderr']['path']]['bytes']==0)
driver=strict(OUT/'driver_result.json',seal['files']['driver_result.json']);tail={key:full_stdout[key]for key in env['TAIL_FIELDS']}
checked_equal('RUN_full_stdout_complete_result_and_four_tails',full_stdout,dict(result=driver,**tail))
for k,v in tail.items():checked_equal('RUN_actual_fourtail:'+k,run[k],v)
terminal=dict(receipt=descriptor(body['actual_external_terminal_evidence']['path']),full_stdout=descriptor(run['full_stdout']['path']),full_stderr=descriptor(run['full_stderr']['path']),command=run['command'],schema=env['TERMINAL_SCHEMA'],**tail)
checked_equal('actual_intake_complete_external_terminal_validation',body['actual_external_terminal_validation'],terminal)
prep_validation=dict(receipt=body['actual_prepare_terminal_evidence'],source_inventory=prep['source_inventory'],full_stdout=prep['full_stdout'],full_stderr=prep['full_stderr'])
for k in ('full_stdout','full_stderr'):
 fresh(prep[k]['path'],prep[k]['sha256'])
need('PREP_complete_stderr_empty',observed[prep['full_stderr']['path']]['bytes']==0)
checked_equal('PREP_complete_stdout',strict(prep['full_stdout']['path']),dict(declaration=str(OUT/'declaration.json'),declaration_sha256=observed[str(OUT/'declaration.json')]['sha256']))
files=dict(d['files'])
def add_owner(path,sha):
 key=str(path);need('full_descriptor_union_no_conflict:'+key,key not in files or files[key]==sha);files[key]=sha
for name,sha in seal['files'].items():add_owner(OUT/name,sha)
add_owner(OUT/'seal.json',body['build_seal_sha256'])
for field in ('receipt','full_stdout','full_stderr'):add_owner(terminal[field]['path'],terminal[field]['sha256'])
add_owner(d['input_graph']['path'],d['input_graph']['sha256'])
for field in ('receipt','source_inventory','full_stdout','full_stderr'):add_owner(prep_validation[field]['path'],prep_validation[field]['sha256'])
d_local=dict(d,actual_prep_terminal_sha256=prep_validation['receipt']['sha256'])
return_node=[n for n in function(tree,'production_admission').body if isinstance(n,ast.Return)]
need('production65_single_source_return',len(return_node)==1 and isinstance(return_node[0].value,ast.Call)and isinstance(return_node[0].value.func,ast.Name)and return_node[0].value.func.id=='dict')
source_return=return_node[0].value
need('source_return_exact65_named_fields',len(source_return.keywords)==65 and all(k.arg is not None for k in source_return.keywords))
return_env=dict(env,d=d_local,seal_sha=body['build_seal_sha256'],bodies=bodies,trim_body=trim_body,terminal=terminal,descriptor_files=files)
expected=expression(source_return,return_env)
whole_body_stats=checked_equal('entire65_actual_intake_BODY_static_source_provenance_exact_typed_order_floatbits',body,expected)
need('whole65_field_order_exact_source',list(body)==[k.arg for k in source_return.keywords])
field_provenance=[]
for kw in source_return.keywords:
 stats=checked_equal('whole_field:'+kw.arg,body[kw.arg],expected[kw.arg])
 field_provenance.append(dict(field=kw.arg,source_expression=ast.get_source_segment(factory_text,kw.value),actual_typed_order_binary64_sha256=typed_sha(body[kw.arg]),expected_typed_order_binary64_sha256=typed_sha(expected[kw.arg]),coverage=stats))
formal_pin,_=fresh(REVIEW/'admit.stdout.json',PINS[str(DUR/'intake/admit.log')]);need('actual_api_identical_full_stream_to_genuine_formal_body',formal_pin['bytes']==observed[str(DUR/'intake/admit.log')]['bytes'])
need('actual_descriptor_count_from_full_union',len(files)==36804 and len(body['descriptor_files'])==36804)
need('actual_alias_count_from_declaration',len(body['input_aliases'])==186)

# Independently recheck the actual source archive and complete byte inverses.
producer_proof=strict(REVIEW/'Root_READY_producer_13_region_complete_inverse_proof.json')
for key in ('candidate','mother_UNREADY','mother_V11'):fresh(producer_proof[key]['path'],producer_proof[key]['sha256'])
need('factory_candidate_copy_is_actual5af',producer_proof['candidate']['sha256']==factory_pin['sha256'])
producer_inverse=inverse(factory_text,producer_proof['complete_regions'],fresh(producer_proof['mother_V11']['path'],collect=True)[1].decode(),'producer13')
need('producer13_exact_number',len(producer_proof['complete_regions'])==13)
for file in producer_proof['archived_files']:fresh(file['path'],file['sha256'])
helper_review=strict(producer_proof['helper_independent_review']['path'],producer_proof['helper_independent_review']['sha256'])
helper_base=ROOT/'validation/axial_material/identity_key_delta_source_v11_20261009'
helper_ready=strict(helper_base/'canonical_file_table_storage_Root_source_admission/Root_READY_candidate_inverse_proof.json')
helper_proof=strict(helper_base/'canonical_file_table_storage_Root_source_admission/Root_READY_complete_10_region_parent_inverse_proof.json')
arch=helper_base/'canonical_file_table_storage_owned_consume_final_source'
helper_regions=strict(arch/'complete_5_plus_3_source_region_edits.json',helper_proof['archived_files']['complete_5_plus_3_source_region_edits.json'])
for k in ('READY_candidate','UNREADY_source'):fresh(helper_ready[k]['path'],helper_ready[k]['sha256'])
original_helper=fresh(helper_review['original_parent']['path'],helper_review['original_parent']['sha256'],True)[1].decode()
helper_inverse=inverse(graph_text,helper_regions+helper_ready['ready_regions'],original_helper,'helper10')
need('helper10_exact_number',len(helper_regions)+len(helper_ready['ready_regions'])==10)
for name in ('FINAL_REPORT.json','PURE_CODEC_REPORT.json','actual_source_and_pure_codec_tool_return.json','actual_closeout_tool_return.json','combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py','source_inverse_proof.json'):
 if name in helper_proof['archived_files']:fresh(arch/name,helper_proof['archived_files'][name])
for k in ('native_RSS_proof_obtained','actual_full_FLU_entry_executed','production_pipeline_prepared','AAA_accuracy_qualified','ABA_admitted'):need('V11_no_native_accuracy_credit:'+k,trim_body[k]is False)
for k in ('original_component_APIs_executed_now','trim_API_executed_in_this_consumer','production_pipeline_prepared','native_transport_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted'):need('actual_whole_INPUT_only:'+k,body[k]is False)
need('original_capture_scope_remains_distinct',body['original_operator_capture_RSS_scope_not_transferred']is True and body['actual_components']['capture']['actual_native_RSS_under_512_guard_passed']is True)

report=dict(schema='AXMAT_V12_ACTUAL_STANDALONE_WHOLE_BODY_SOURCE_INDEPENDENT_READONLY_AUDIT_V1',status='PASS_COMPLETE_ACTUAL_65_FIELD_BODY_AND_SOURCE_PROVENANCE_METADATA_ONLY',actual_root=observed[str(DUR/'Root_terminal_return.json')],actual_whole_API=observed[str(DUR/'intake/admit.log')],actual_factory=factory_pin,actual_helper=graph_pin,whole_body_top_field_count=len(body),whole_body_coverage=whole_body_stats,whole_body_typed_order_floatbits_sha256=typed_sha(body),full_65_field_provenance=field_provenance,genuine_whole_seven_INPUT_body=dict(specs=observed[str(SPECS)],historical_declaration=observed[specs['metadata']['declaration']['path']],coverage=seven_stats,all_historical_7_keys=list(bodies),real_saved_sorted_JSON_boundary_verified=True,pre_sort_historical_declaration_coverage=historical_stats),actual_whole_V11_trim_body=dict(original_admit=observed[str(ROOT/'validation/axial_material/identity_key_delta_full_component_review_v11_20261009/admit.stdout')],saved_source_input=observed[str(SOURCE/'trim_component_admission_INPUT.json')],coverage=trim_stats,complete30_counts=counts,sorted_complete_counts_sha256=hashlib.sha256(json.dumps(counts,sort_keys=True,separators=(',',':')).encode()).hexdigest(),sealed68_stage_count=len(trim_stages),sealed68_stage_labels=[s['label']for s in trim_stages],keycodec21_metadata_passed=True),SOURCE11=source_inventory,V11_SOURCE=trim_source_inventory,parent_SOURCE_runtime_object_metadata=parent_evidence,complete65_descriptor_union_count=len(files),complete_declaration_alias_count=len(body['input_aliases']),source_archive_proof=dict(producer13_inverse_sha256=producer_inverse,helper10_inverse_sha256=helper_inverse,production_AST_only_no_program_execution=True,source_archive_files_freshly_read=True),checks=checks,observed_files=observed,findings=findings,known_pure_reviewer_errors=[dict(chunk_id='730510',exit_code=1,cause='First correction guessed mapping; actual_production_objects is literal path list with expected SHA in declaration files. Corrected to explicit declaration owner pins, no project mutation or business retry.'),dict(chunk_id='1bdf25',exit_code=1,cause='Initial reader treated actual_production_objects literal path list as descriptor list. Prior script/streams/actual receipt preserved. No business operation.'),dict(chunk_id='5aed6c',exit_code=1,cause='Initial independent reader required every sealed68 stage PASS. The 20 expected keycodec negative controls truthfully retain FAILED status and typed returncode23. Failed reader/script/streams/actual receipt preserved without alteration; no business execution.'),dict(chunk_id='106e96',exit_code=1,cause='Read-only discovery reader initially treated V11 driver watchdog descriptors as full watches and guessed nonexistent returncode; sealed full watchdog files then read by pinned path.'),dict(chunk_id='1c0cd3',exit_code=1,cause="Read-only discovery reader guessed nonexistent V11 declaration key 'stages'; actual stage metadata was then read from sealed family/stages.json. No business retry or project write.")],business_imports_or_calls=False,production_API_or_CLI_or_phase_or_helper_executed=False,production_verify_graph_executed=False,fixtures_executed=False,mathematical_controls_reparsed_or_rerun=False,graph_or_complete_scientific_descriptor_payload_reread=False,Root_handles_polled=False,project_files_written=False,new_native_run_executed=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,original_operator_capture_only_guard_not_transferred=True,limitations=['Fresh metadata/SOURCE/runtime/object provenance does not grant new native RSS, transport, AAA accuracy or ABA credit.','36776 scientific/graph canonical payload bytes are deliberately not reread here; root reviewer owns that complementary fresh admission.','The real capture parent retains its historical original-operator-only native guard; it is never transferred to the combined runtime.'])
need('TMP_report_destination',str(DEST).startswith('/private/tmp/')and DEST.is_dir())
p=DEST/'REPORT.json';p.write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
print(json.dumps(dict(report=str(p),report_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),status=report['status'],checks=len(checks),whole_body_nodes=whole_body_stats['nodes'],whole_body_float_count=whole_body_stats['float_binary64_count'],fresh_metadata_source_runtime_object_file_count=len(observed),script=str(Path(__file__)),script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),ensure_ascii=False))
