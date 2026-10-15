"""Read fixed Source and saved META only; do not execute any reviewed code."""
from pathlib import Path
import ast,hashlib,json,os,stat
OUT=Path('/private/tmp/axmat_v22c_fullbuild_actual_sealed_peer_shape_SOURCE_review_5ihu8mkh')
BASE=Path('/private/tmp/axmat_v22_fullbuild_Root_Source_binder_independent_review_05fs3v3d')
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
E=B/'actual_complete_combined_prepare_v22_receipts'
NEW=Path('/private/tmp/spot_bind_v22_original_full_build_host_ROOT_v22c.py')
OLD=Path('/private/tmp/spot_bind_v22_original_full_build_host_ROOT_v22b.py')
PROOF=Path('/private/tmp/spot_v22_full_build_binder_actual_sealed_peer_shape_Source_inverse.json')
PEER=E/'sealed_independent_actual_complete_PREP_saved_META_review/REVIEW.json'
checks=[];pins={}
def check(n,v):
 assert type(v)is bool;checks.append(dict(check=n,passed=v))
 if not v:raise ValueError(n)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def read(p):
 s=p.lstat();i=identity(s);check('regular explicit Source/META '+str(p),stat.S_ISREG(s.st_mode)and s.st_nlink==1)
 with p.open('rb')as f:
  check('exact open native7ID '+str(p),identity(os.fstat(f.fileno()))==i)
  raw=f.read();check('complete EOF '+str(p),len(raw)==s.st_size and f.read(1)==b'')
  check('fd after unchanged '+str(p),identity(os.fstat(f.fileno()))==i)
 check('path after unchanged '+str(p),identity(p.lstat())==i)
 pins[str(p)]=dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=i)
 return raw
parent=json.loads(read(BASE/'REVIEW.json'));manifest=json.loads(read(BASE/'MANIFEST.json'))
check('sealed parent Source peer exact manifest',pins[str(BASE/'MANIFEST.json')]['sha256']=='f73ada79985a54f7ac42a7f14ad2661b6887f907e4efda854cf31f9eabe76511')
check('parent complete369 Source checks passed',parent['PASS']is True and parent['all_checks_passed']is True and parent['blockers']==[] and len(parent['checks'])+len(parent['complete_prior_source_checks'])==369)
for v in manifest['members']:
 read(Path(v['path']));check('entire parent sealedSource pin '+v['relative_path'],pins[v['path']]=={k:w for k,w in v.items()if k!='relative_path'})
 check('entire parent Source retained byteexact '+v['relative_path'],(OUT/'PARENT_FULL_SCOPE_SOURCE_PEER'/v['relative_path']).read_bytes()==Path(v['path']).read_bytes())
for v in parent['full_explicit_SOURCE_META_reads'].values():
 read(Path(v['path']));check('whole prior actual source/meta unchanged '+v['path'],pins[v['path']]==v)
old=read(OLD);new=read(NEW);proofraw=read(PROOF);proof=json.loads(proofraw)
check('new frozen v22c72b196 Source',pins[str(NEW)]['sha256']=='72b19614ca141555bfbe7ab70f74092cc5cc5407f8f69c530f2893ad5f0a315c')
check('original frozen v22b170fc2 Source',pins[str(OLD)]['sha256']=='170fc2abf3d3f1ba47e6aef233845d6335f844cdcdf89ce9786ce382c8231cd2')
check('single new correction hunk',len(proof['finite_hunks'])==1)
h=proof['finite_hunks'][0];a=old.decode();b=new.decode()
check('original unique hunk count',a.count(h['before'])==h['count']==1)
check('new unique hunk count',b.count(h['after'])==1)
check('complete finite Source forward text',a.replace(h['before'],h['after'])==b)
back=b.replace(h['after'],h['before']);check('complete byte inverse',back.encode()==old)
check('complete AST inverse',ast.dump(ast.parse(back),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False))
oldtree=ast.parse(old);newtree=ast.parse(new)
olddefs={n.name:n for n in oldtree.body if isinstance(n,ast.FunctionDef)};newdefs={n.name:n for n in newtree.body if isinstance(n,ast.FunctionDef)}
check('complete six original functions retained',list(newdefs)==list(olddefs)and len(newdefs)==6)
for name in newdefs:
 check('all original Source function AST '+name,ast.dump(newdefs[name],include_attributes=False)==ast.dump(olddefs[name],include_attributes=False))
 check('all original Source function byte '+name,ast.get_source_segment(b,newdefs[name])==ast.get_source_segment(a,olddefs[name]))
def assignment(tree,name):return next(n.value for n in tree.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id==name)
check('complete original21host substitutions unchanged',ast.dump(assignment(newtree,'changes'),include_attributes=False)==ast.dump(assignment(oldtree,'changes'),include_attributes=False))
pr=read(PEER);peer=json.loads(pr)
check('actual sealed savedPREP peer exact678bc8',pins[str(PEER)]['sha256']==proof['actual_REPORT_sha256']=='678bc8e4a9e1ec795db09e40355991730670bfcb94a72a9204af3b333822f3df')
check('actual savedPREP strict schema',peer['schema']=='INDEPENDENT_V22_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_V1')
check('actual savedPREP scope and exact status',peer['actual_PREP_metadata_only']is True and peer['status']=='PASS_ACTUAL_COMPLETE_PREP_ONLY')
check('actual savedPREP typed overall and empty blockers',peer['all_checks_typed_true']is True and type(peer['blockers'])is list and not peer['blockers'])
check('complete 10170 actual saved checks allbooltrue',type(peer['check_count'])is int and peer['check_count']==len(peer['checks'])==10170 and all(c['passed']is True for c in peer['checks']))
for name in ('actual_PREP_closed_EXIT0_verified','actual_metadata_writer_closed_EXIT0_verified','all_complete_scope_verified'):
 check('genuine actual saved closure/scope '+name,peer[name]is True)
check('actual root toolchunk retained',peer['actual_PREP_terminal_chunk']=='fc5201'and peer['actual_metadata_writer_terminal_chunk']=='34125a')
flags=('whole_combined_build_qualified','whole_combined_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified')
for name in flags:check('all original6scope False '+name,peer[name]is False)
required={
 'actual_Root_PREP_summary_pin':E/'Root_actual_complete_combined_prepare_summary.json',
 'actual_Root_PREP_terminal_pin':E/'Root_actual_prepare_tool_terminal_return.json',
 'actual_complete_namespace_manifest_pin':E/'Root_actual_complete_prepare_namespace_manifest.json'}
for name,p in required.items():
 read(p);ref=peer[name]
 check('actual peer full4field samePREP '+name,ref==pins[str(p)]and set(ref)=={'path','sha256','size_bytes','identity'}and type(ref['size_bytes'])is int and len(ref['identity'])==7 and all(type(v)is int for v in ref['identity']))
for name,anchor in [
 ('status shape Source strict',"assert peer['status']=='PASS_ACTUAL_COMPLETE_PREP_ONLY'"),
 ('all typed Source strict',"assert peer['all_checks_typed_true'] is True"),
 ('blockers shape Source strict',"assert type(peer['blockers']) is list and not peer['blockers']"),
 ('actual Root EXIT0 Source strict',"assert peer['actual_PREP_closed_EXIT0_verified'] is True"),
 ('metadata writer EXIT0 Source strict',"assert peer['actual_metadata_writer_closed_EXIT0_verified'] is True"),
 ('all complete scope Source strict',"assert peer['all_complete_scope_verified'] is True"),
 ('same actual summary Source strict',"assert peer['actual_Root_PREP_summary_pin']==sp"),
 ('same actual terminal Source strict',"assert peer['actual_Root_PREP_terminal_pin']==pin(E/'Root_actual_prepare_tool_terminal_return.json')"),
 ('same complete namespace Source strict',"assert peer['actual_complete_namespace_manifest_pin']==pin(E/'Root_actual_complete_prepare_namespace_manifest.json')"),
 ]:check(name,anchor in b)
check('strict Source refusal before destination creation',b.index("assert peer['status']=='PASS_ACTUAL_COMPLETE_PREP_ONLY'")<b.index('dest.mkdir()'))
check('strict no any business/native/guard stage call',not any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr in ('execute','run','Popen','exec_module','system')for n in ast.walk(newtree)))
for p,v in list(pins.items()):read(Path(p));check('whole Source/META beforeafter unchanged '+p,pins[p]==v)
report=dict(schema='INDEPENDENT_V22C_ACTUAL_SEALED_PREP_PEER_SHAPE_FULLBUILD_SOURCE_REVIEW_V1',status='SOURCE_ONLY_PASS_NO_BUSINESS_EXECUTION',
 source_only=True,PASS=True,all_checks_passed=True,blockers=[],checks=checks,check_count=len(checks),
 complete_prior_369_SOURCE_review=parent,qualified_generator=pins[str(NEW)],complete_inverse_proof=pins[str(PROOF)],actual_sealed_savedPREP_peer=pins[str(PEER)],
 actual_savedPREP_peer_matches_this_summary_terminal_and_namespace=True,complete_10170_saved_peer_checks_typed_true=True,
 full_explicit_SOURCE_META_reads=pins,all_original6functions_and21hosthunks_and_caps_unchanged=True,
 expected_whole_host_source_sha256=parent['independent_static_expected_host_sha256'],original_caps=parent['original_caps'],
 no_generator_or_host_or_helper_or_guard_or_reader_or_API_or_business_executed=True,no_ART_numeric_payload_read=True,
 actual_bound_source_generated_here=False,actual_new_fullbuild_or_INPUT_or_native_or_scientific_qualification=None,
 subsequent_steps=['Root metadata-only generator with true report path/SHA and absent freshTMP under unoptimized Python.',
 'Independent actual generated completehost Source/inverse review; complete newD install/freeze; actual prelaunch fullSource/input/resource checks.',
 'One genuine original full5stage run; actual integer0CLOSED and complete saved evidence independent review required. WholeINPUT/native/science remain separate.'])
(OUT/'REVIEW.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(source_only=True,PASS=True,checks=len(checks),prior_source_checks=369,
 review_sha256=hashlib.sha256((OUT/'REVIEW.json').read_bytes()).hexdigest(),actual_source_binder_executed=False),indent=2))
