"""Isolated stdlib AST/source/metadata fixtures. No business modules/API/native/ART.
The synthetic test namespaces are not real module identity or tool-return evidence.
"""
import ast,copy,hashlib,json,os,re,stat,sys,tempfile,difflib,gc
from pathlib import Path
from types import SimpleNamespace
D=Path('/private/tmp/axmat-cold-owned-specs-input-intake-path-stable-draft-20261007')
BASE=Path('/private/tmp/prepare_combined_physical_dedup_file_snapshot_cold_AAA_full_draft_20261007.py')
COLD=D/'prepare_historical_input_owned_specs_physical_dedup_file_snapshot_cold_AAA_full_draft_20261007.py'
HELPER=D/'cold_component_input_consumer.py'
ROOT=Path('/Users/wen/spot')
REPORT=D/'source_only_review_report.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def defs(s):return {n.name:ast.get_source_segment(s,n)for n in ast.parse(s).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
def literal_nodes(s):return {n.targets[0].id:n.value for n in ast.parse(s).body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
def lit(s,name):return ast.literal_eval(literal_nodes(s)[name])
def extract(s,names,ns):
 nodes=[n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)and n.name in names]
 if {n.name for n in nodes}!=set(names):raise ValueError('isolated definition missing')
 exec(compile(ast.Module(body=nodes,type_ignores=[]),'<isolated pure source fixture>','exec'),ns)
def rejected(label,fn):
 try:fn()
 except (ValueError,TypeError,KeyError,FileNotFoundError,PermissionError):negative.append(label)
 else:raise AssertionError('accepted '+label)
old,new,h=BASE.read_text(),COLD.read_text(),HELPER.read_text()
for source in (old,new,h):ast.parse(source)
proof=json.loads((D/'full_33cd_source_inverse.json').read_text());restored=new
for row in reversed(proof['inverse_regions']):
 assert restored.count(row['candidate'])==1
 restored=restored.replace(row['candidate'],row['original'],1)
assert restored==old and sha(BASE)=='33cd2b3a0e4676c3f3d1c679a217f17532f0550524af357847f9d8de5e5960ca'
od,nd=defs(old),defs(new);same=sorted(k for k in od if od[k]==nd[k]);changed=sorted(set(od)-set(same))
positive=['whole39-region byte inverse to frozen33cd','both new sources AST-valid','all original definitions retained']
negative=[]
for key in ('BUDGETS','ORIGINAL_COLD_RESERVE_BYTES','ORIGINAL_COMPLETE_12_MAP_CASE_BYTES','ORIGINAL_COMPLETE_SNAPSHOT_BYTES',
            'HOST_SHA','CONTROLS_SHA','BASE_CONTROLLER_SHA','DECK_HOOK','CONSTRUCTOR_BEFORE','CONSTRUCTOR_AFTER'):
 assert ast.dump(literal_nodes(old)[key])==ast.dump(literal_nodes(new)[key])
positive.append('original cold budgets,reserve,work forecast,host/controls/deck hook/sole constructor literals exact')
assert lit(new,'DRAFT_STATUS').startswith('UNREADY')
unknown=[key for key in ('FORMAL_FACTORY','COMBINED_RUNTIME','COMBINED_RUNTIME_SHA','DECK_HELPER','PRIVATE_INPUT_CONSUMER',
 'PRIVATE_INPUT_CONSUMER_SHA','COMPONENT_INTAKE_DESCRIPTOR','COMPONENT_INTAKE_DESCRIPTOR_SHA')if lit(new,key)is None]
assert len(unknown)==8
# Functions are extracted into isolated synthetic namespaces; no project module import.
ns=dict(Path=Path,hashlib=hashlib,ast=ast,re=re,os=os,sys=sys)
for key in ('BASE_CONTROLLER_SHA','BASE_RUNTIME_SHA','DECK_HOOK','CONSTRUCTOR_BEFORE','CONSTRUCTOR_AFTER'):
 ns[key]=lit(new,key)
extract(new,('nonzero_sha','definition_sources','render_controller'),ns)
controller=ROOT/'validation/artifacts/axial-material-production-qualified-AB-rank1-factor-cache-20261007/runtime/production_runner.py'
original=controller.read_text();candidate,cp=ns['render_controller'](original,'b'*64)
r=candidate
for before,after in reversed(cp['replacements']):r=r.replace(after,before,1)
assert r==original and sha(controller)==ns['BASE_CONTROLLER_SHA']
a,b=defs(original),defs(candidate)
assert {k for k in a if a[k]!=b[k]}=={'prepare','run'}
assert b['SerialExecutor']==a['SerialExecutor']and b['qualify_aba']==a['qualify_aba']and b['resource_monitor']==a['resource_monitor']
assert candidate.count('runtime / "cold_component_input_consumer.py"')==1
assert candidate.index('runtime / "cold_component_input_consumer.py"')<candidate.index('info["local_files"] =')
positive+=['actual844 whole controller inverse','Serial/qualify/resource/all scientific definitions exact','four real copies before original local inventory']
# Generated rank1 admission changes only metadata acquisition; every observer/math callback exact.
ha,hb=lit(old,'ADMISSION_HOST'),lit(new,'ADMISSION_HOST');ad,bd=defs(ha),defs(hb)
assert set(ad)==set(bd)and {k for k in ad if ad[k]!=bd[k]}=={'metadata'}
assert 'factory.completed_components()'not in hb and "factory.materialize_metadata(data,item,phase='private-rank1/metadata')"in hb
positive+=['all generated callbacks except metadata byte exact','no component API call in generated metadata acquisition']
# Normal -c program must compile before any canonical input is loaded.
cmdns=dict(Path=Path,FORMAL_FACTORY=Path('/isolated/formal/cold.py'),factory_source_descriptor=lambda:dict(sha256='c'*64))
extract(new,('normal_factory_command',),cmdns)
cmd=cmdns['normal_factory_command']('/isolated/python','r=1')
compile(cmd[2],'<synthetic normal-c program>','exec')
assert cmd[:2]==['/isolated/python','-c']and cmd[2].index('sys.flags.optimize')<cmd[2].index('p=Path(')
positive.append('normal-c command compiles; optimize/ENV guard before project read')
# UNREADY rejects before a data/source byte read, including explicit optimize/PYTHONOPTIMIZE.
for source,fname,status in ((new,'require_input_ready',lit(new,'DRAFT_STATUS')),(h,'input_guard',lit(h,'STATUS'))):
 fakeos=SimpleNamespace(environ={})
 fake=dict(sys=SimpleNamespace(flags=SimpleNamespace(optimize=0)),os=fakeos,DRAFT_STATUS=status,STATUS=status)
 extract(source,(fname,),fake)
 rejected(fname+' UNREADY before reads',fake[fname])
 fake['sys'].flags.optimize=1;rejected(fname+' optimize nonzero',fake[fname]);fake['sys'].flags.optimize=0
 fakeos.environ['PYTHONOPTIMIZE']='0';rejected(fname+' PYTHONOPTIMIZE even0',fake[fname])
# Whole intake descriptor has no own-SHA cycle: caller independently supplies descriptor after parsing.
assert "if 'binding_descriptor' in value:"in nd['component_intake']
assert 'dict(value,binding_descriptor=dict(path=str(COMPONENT_INTAKE_DESCRIPTOR)'in nd['component_intake']
positive.append('INPUT binding independent SHA is injected outside immutable JSON; no self-hash cycle')
# Strict byte reader / ordinary namespace tiny tests, no production payloads.
hns=dict(Path=Path,hashlib=hashlib,os=os,stat=stat,re=re,sys=sys)
extract(h,('nonzero_sha','normal','digest','require','expected_union','inventory_shape','post_graph_metadata'),hns)
with tempfile.TemporaryDirectory(prefix='axmat-cold-input-tiny-',dir='/private/tmp')as t:
 base=Path(t);p=base/'input.bin';p.write_bytes(b'original bytes\x00')
 wanted=hashlib.sha256(p.read_bytes()).hexdigest();assert hns['digest'](p)==(wanted,15)
 assert hns['require'](p,wanted)==p
 rejected('same-size byte mutation',lambda:(p.write_bytes(b'changed! bytes\x00'),hns['require'](p,wanted)))
 p.write_bytes(b'original bytes\x00');alias=base/'alias';alias.symlink_to(p)
 rejected('ordinary endpoint alias',lambda:hns['digest'](alias))
 folder=base/'parent';folder.mkdir();(folder/'v').write_bytes(b'v');paralias=base/'parent_alias';paralias.symlink_to(folder,target_is_directory=True)
 rejected('ordinary ancestor alias',lambda:hns['digest'](paralias/'v'))
 rejected('ordinary nonregular file',lambda:hns['digest'](folder))
 class G:
  @staticmethod
  def _alias_map(rows):return {r['path']:r for r in rows}
  @staticmethod
  def _resolve(path,aliases,kind=None):
   literal=str(path)
   return aliases[literal]['target']if literal in aliases else str(Path(path))
  @staticmethod
  def _scan_namespace(root,aliases):
   r=Path(root);files=set();dirs=set();links={}
   for path in r.rglob('*'):
    rel=str(path.relative_to(r))
    if path.is_symlink():links[rel]=os.readlink(path)
    elif path.is_dir():dirs.add(rel)
    elif path.is_file():files.add(rel)
   return dict(canonical_root=str(r),files=files,directories=dirs,symlinks=links)
  @staticmethod
  def _absence_phase(values,aliases,expected=None):
   for path in values:
    if os.path.lexists(path):raise ValueError('absent endpoint appeared')
 g=G();s=base/'binding.py';s.write_bytes(b'impl');d=base/'descriptor.json';d.write_bytes(b'{}')
 binding=dict(intake_proof_files={str(p):wanted},binding_source=dict(path=str(s),sha256='d'*64),binding_descriptor=dict(path=str(d),sha256='e'*64))
 value=dict(descriptor_files={str(p):wanted},input_aliases={str(alias):dict(target=str(p),kind='file',text=str(p),sha256=wanted)})
 out=hns['expected_union'](g,value,binding,dict(additional_expected_files={str(alias):wanted}))
 assert set(out)=={str(p),str(s),str(d)}
 rejected('conflicting logical owner SHA via canonical alias',lambda:hns['expected_union'](g,value,binding,dict(additional_expected_files={str(alias):'a'*64})))
 reject_binding=copy.deepcopy(binding);reject_binding['binding_source']['path']=str(p)
 rejected('conflicting implementation owner SHA',lambda:hns['expected_union'](g,value,reject_binding,dict(additional_expected_files={})))
 hns['inventory_shape'](g,folder,dict(files={'v':'f'*64},directories=[],symlinks={}))
 (folder/'empty').mkdir();rejected('extra empty namespace directory',lambda:hns['inventory_shape'](g,folder,dict(files={'v':'f'*64},directories=[],symlinks={})))
 (folder/'empty').rmdir()
 absent=str(base/'missing');graph=dict(aliases=[],absence_inputs={absent:{}},absence_observations={},namespaces=[dict(root=str(folder),canonical_root=str(folder),files={'v':'f'*64},directories=[],symlinks={})])
 hns['post_graph_metadata'](g,graph)
 (folder/'extra').write_bytes(b'x');rejected('post additional-read historical namespace mutation',lambda:hns['post_graph_metadata'](g,graph));(folder/'extra').unlink()
 Path(absent).write_bytes(b'x');rejected('post additional-read absence appeared',lambda:hns['post_graph_metadata'](g,graph))
positive+=['fresh bounded byte reader exact','canonical alias typed owner union and conflict rejection','historical post-read aliases/namespace/absence extension']
# Calls explicitly forbidden in the private consumer; genuine capture work and guard calls are named INPUT predicates.
ht=ast.parse(h)
for n in ast.walk(ht):
 if isinstance(n,ast.Call):
  if isinstance(n.func,ast.Attribute):assert n.func.attr not in ('modules','production_admission','diagnostic_admission','run','prepare','Popen','execve')
  elif isinstance(n.func,ast.Name):assert n.func.id not in ('eval','subprocess')
positive.append('consumer source has no business/API/child/producer.modules call')
# m.files carries all 10 durable intake bytes plus independently pinned binding/source.
assert "intake['intake_proof_files'].items()"in nd['declare']and "intake['binding_source'],intake['binding_descriptor']"in nd['declare']
assert "choices=[runtime/(name+'.py')]"in nd['input_consumer']
positive+=['new binding inputs owned in cold declaration and host module inventory','SOURCE/WORK helper chosen by actual normally bound controller']
report=dict(schema='AXMAT_COLD_COMPLETE_INPUT_INTAKE_SOURCE_ONLY_REVIEW_V1',cold=dict(path=str(COLD),sha256=sha(COLD)),consumer=dict(path=str(HELPER),sha256=sha(HELPER)),
 base=proof['original'],full_inverse_regions=len(proof['inverse_regions']),unchanged_definitions=same,changed_definitions=changed,added_definitions=sorted(set(nd)-set(od)),
 controller_inverse=cp,positive_checks=positive,negative_checks=negative,unbound_fields=unknown,
 actual_business_or_API_or_constructor_or_child_or_native_executed=False,new_ART_roots_created=False,
 actual_cold_fixture_or_metadata_RSS_proved=False,original_96GiB_storage_refusal_not_changed=True)
REPORT.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
print(json.dumps(dict(cold=report['cold'],consumer=report['consumer'],positive=len(positive),negative=len(negative),report=dict(path=str(REPORT),sha256=sha(REPORT)))))
