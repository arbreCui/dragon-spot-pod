"""Unique Source v2: restore the original single-link predicate, retaining four selectors."""
import ast, importlib.util, json, os, stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
spec=importlib.util.spec_from_file_location('source_utilities',R/'prepare_literal2_before_material75_v12_input_duplicates_source_only_v1_20261014.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
pin,read,write,identity=h.pin,h.read,h.write,h.identity
OLD=R/'storage_release_literal4_before_short_FIL_material_retry_source_v1_20261014'
OUT=R/'storage_release_literal4_before_short_FIL_material_retry_source_v2_20261014'
NAMES=h.NAMES
SFNAME='COMPLETE_LITERAL4_BEFORE_SHORT_FIL_MATERIAL_RETRY_SOURCE_FREEZE.json'
PLANNAME='EXACT_LITERAL4_BEFORE_SHORT_FIL_MATERIAL_RETRY_ROLE_SOURCE_PLAN.json'
IVNAME='COMPLETE_LITERAL4_V1_TO_V2_SINGLELINK_WHOLE_BYTE_INVERSE.json'
def segment(s,name):
 return ast.get_source_segment(s,next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)and n.name==name))
def ancestors(p):
 for q in [p,*p.parents]:
  if q.is_symlink():raise RuntimeError('metadata fixture nonsymlink ancestors')
def main():
 if OUT.exists():raise RuntimeError('unique Source namespace')
 oldsfpin=pin(OLD/SFNAME);sf=read(oldsfpin);oldplanpin=pin(OLD/PLANNAME);plan=read(oldplanpin)
 a=(OLD/NAMES[0]).read_text();oldfunc=segment(a,'disjoint')
 if oldfunc.count('s.st_nlink!=4')!=1:raise RuntimeError('exact old physical singlelink defect')
 newfunc=oldfunc.replace('s.st_nlink!=4','s.st_nlink!=1',1)
 z=a.replace(oldfunc,newfunc,1);ast.parse(z)
 if segment(z,'disjoint').count('!=4')!=3 or segment(z,'disjoint').count('s.st_nlink!=1')!=1:raise RuntimeError('three selector cardinalities4 and original singlelink1')
 oldbase=R/'storage_release_literal1_before_material_first_A_v14_ax_source_v2_20261014'
 primitive=segment((oldbase/NAMES[0]).read_text(),'disjoint')
 expected=primitive.replace('len(TARGETS)!=1','len(TARGETS)!=4').replace('len(TARGET_PATHS)!=1','len(TARGET_PATHS)!=4').replace("len({tuple(p['identity'][:2])for p in TARGET_SELECTED_PINS})!=1","len({tuple(p['identity'][:2])for p in TARGET_SELECTED_PINS})!=4")
 if newfunc!=expected:raise RuntimeError('original complete physical guard; only three counts changed')
 targets=sf['literal4_fullpins']
 if len(targets)!=4 or sum(p['size_bytes']for p in targets)!=1014071384:raise RuntimeError('same exact4 scope')
 def metadata_same(p):
  s=Path(p['path']).lstat()
  if identity(s)!=p['identity']:raise RuntimeError('actual target stat7 current')
 from types import SimpleNamespace
 env=dict(TARGETS=[Path(p['path'])for p in targets],TARGET_PATHS={p['path']for p in targets},TARGET_SELECTED_PINS=targets,BYTES=1014071384,b=SimpleNamespace(ancestors=ancestors),identity=identity,os=os,stat=stat,same=metadata_same)
 exec(compile(ast.Module(body=[next(n for n in ast.parse(z).body if isinstance(n,ast.FunctionDef)and n.name=='disjoint')],type_ignores=[]),'actual_source_disjoint_metadata_only','exec'),env)
 env['disjoint']([])
 OUT.mkdir();entries=[]
 for name in NAMES:
  before=(OLD/name).read_text();after=z if name==NAMES[0]else before
  cp=write(OUT/name,after)
  changes=[dict(before=oldfunc,after=newfunc)]if name==NAMES[0]else []
  back=after
  for change in reversed(changes):
   if back.count(change['after'])!=1:raise RuntimeError('exact reverse')
   back=back.replace(change['after'],change['before'],1)
  if back.encode()!=before.encode():raise RuntimeError('whole inverse')
  entries.append(dict(predecessor_pin=pin(OLD/name),candidate_pin=cp,changes=changes,whole_file_inverse_byte_equal=True))
 iv=write(OUT/IVNAME,dict(schema='COMPLETE_LITERAL4_V1_TO_V2_SINGLELINK_WHOLE_BYTE_INVERSE_V1',entries=entries,predecessor_full_inverse_pin=sf['strict_low_level_Source_provenance_pin'],only_one_physical_nlink_predicate_restored=True,three_count4_predicates_unchanged=True,all_other_script_bytes_unchanged=True,actual_disjoint_AST_extracted_metadata_only_called_with_empty_protected=True,target_full_EOF_read_by_this_preparation=False,compiler_executed=False,business_executed=False,numerical_executed=False,deletion_executed=False))
 plan.update(source_revision=2,predecessor_plan_pin=oldplanpin,predecessor_Source_freeze_pin=oldsfpin,complete_v1_to_v2_inverse_pin=iv,source_namespace=str(OUT),actual_disjoint_metadata_fixture_passed=True,fixture_same_function_uses_actual_stat7_only_not_full_EOF=True)
 pp=write(OUT/PLANNAME,plan)
 sf.update(Source_pins=[pin(OUT/n)for n in NAMES],exact_role_plan_pin=pp,strict_low_level_Source_provenance_pin=iv,Source_preparer_pin=pin(__file__),predecessor_Source_freeze_pin=oldsfpin,source_revision=2)
 sp=write(OUT/SFNAME,sf)
 fd=os.open(OUT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='EXACT4_SHORT_FIL_RETRY_V2_SOURCE_ONLY_SINGLELINK_FIXED',Source_freeze_pin=sp,Source_pins=sf['Source_pins'],plan_pin=pp,inverse_pin=iv,preparer_pin=pin(__file__),predecessor_Source_freeze_pin=oldsfpin,target_count=4,target_bytes=1014071384,actual_disjoint_metadata_only_fixture_passed=True,target_full_EOF_read=False,manifest_prepared=False,compiler_executed=False,numerical_executed=False,business_executed=False,deletion_executed=False)),flush=True)
if __name__=='__main__':main()
