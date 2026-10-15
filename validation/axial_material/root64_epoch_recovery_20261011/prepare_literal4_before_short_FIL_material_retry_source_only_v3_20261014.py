"""Source v3: use the actual failed-post original library list directly; no MF or deletion."""
import ast,importlib.util,json,os
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
spec=importlib.util.spec_from_file_location('source_utilities',R/'prepare_literal2_before_material75_v12_input_duplicates_source_only_v1_20261014.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
pin,read,write=h.pin,h.read,h.write
OLD=R/'storage_release_literal4_before_short_FIL_material_retry_source_v2_20261014'
OUT=R/'storage_release_literal4_before_short_FIL_material_retry_source_v3_20261014'
SFNAME='COMPLETE_LITERAL4_BEFORE_SHORT_FIL_MATERIAL_RETRY_SOURCE_FREEZE.json'
PLANNAME='EXACT_LITERAL4_BEFORE_SHORT_FIL_MATERIAL_RETRY_ROLE_SOURCE_PLAN.json'
IVNAME='COMPLETE_LITERAL4_V2_TO_V3_ACTUAL_LIBRARY_LIST_WHOLE_BYTE_INVERSE.json'
def main():
 if OUT.exists():raise RuntimeError('unique Source namespace')
 oldsfpin=pin(OLD/SFNAME);sf=read(oldsfpin);oldplanpin=pin(OLD/PLANNAME);plan=read(oldplanpin)
 a=(OLD/h.NAMES[0]).read_text();old="for p in failed_post['actual_original_library_input_pins'].values():add(p,'two_original_scientific_libraries_current')";new="for p in failed_post['actual_original_library_input_pins']:add(p,'two_original_scientific_libraries_current')"
 if a.count(old)!=1:raise RuntimeError('one exact existing original library list traversal')
 z=a.replace(old,new,1);tree=ast.parse(z);const=lambda n:ast.literal_eval(next(x.value for x in tree.body if isinstance(x,ast.Assign)and isinstance(x.targets[0],ast.Name)and x.targets[0].id==n))
 failed=const('CLOSED_FAILED_A');d=read(failed['summary_pin']);p=read(failed['independent_postreview_pin']);targets=sf['literal4_fullpins'];targetpaths={q['path']:q for q in targets}
 for data,key,count in [(d,'fixed_current_pins',5719),(d,'output_pins',21),(d,'owned_input_copy_pins',12),(p,'actual_scene_full_EOF_pins',22),(p,'actual_original_library_input_pins',2)]:
  rows=data[key]
  if type(rows)is not list or len(rows)!=count or any(type(q)is not dict or set(q)!={'path','sha256','size_bytes','identity'}for q in rows):raise RuntimeError('actual selected metadata canonical list '+key)
 fun=ast.get_source_segment(z,next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='current_protection'));start=fun.index(" failed_actual=read(CLOSED_FAILED_A");end=fun.index(' for p in ROLE_KEEP_PINS',start);block=fun[start:end]
 kept=[];historical=[]
 def add(q,why):
  if q['path']in targetpaths:
   if q!=targetpaths[q['path']]:raise RuntimeError('exact target historical fullPF only')
   historical.append(q)
  else:kept.append(q)
 env=dict(CLOSED_FAILED_A=failed,read=read,add=add)
 exec(compile(ast.parse('if True:\n'+block),'actual_added_protection_block_metadata_only','exec'),env)
 if any(q not in kept for q in p['actual_original_library_input_pins'])or set(q['path']for q in historical)!=set(q['path']for q in targets[:2]):raise RuntimeError('original2 current and exact private2 historical')
 OUT.mkdir();entries=[]
 for name in h.NAMES:
  before=(OLD/name).read_text();after=z if name==h.NAMES[0]else before;cp=write(OUT/name,after);changes=[dict(before=old,after=new)]if name==h.NAMES[0]else []
  back=after
  for c in reversed(changes):
   if back.count(c['after'])!=1:raise RuntimeError('one inverse')
   back=back.replace(c['after'],c['before'],1)
  if back.encode()!=before.encode():raise RuntimeError('whole Source inverse')
  entries.append(dict(predecessor_pin=pin(OLD/name),candidate_pin=cp,changes=changes,whole_file_inverse_byte_equal=True))
 iv=write(OUT/IVNAME,dict(schema='COMPLETE_LITERAL4_V2_TO_V3_ACTUAL_LIBRARY_LIST_WHOLE_BYTE_INVERSE_V1',entries=entries,predecessor_full_inverse_pin=sf['strict_low_level_Source_provenance_pin'],only_actual_list_traversal_corrected=True,all_other_functions_and_two_scripts_wholebytes_unchanged=True,actual_added_current_protection_block_executed_metadata_only=True,selected_actual_field_list_counts=dict(fixed_current_pins=5719,output_pins=21,owned_input_copy_pins=12,actual_scene_full_EOF_pins=22,actual_original_library_input_pins=2),target_or_science_body_EOF_read=False,manifest_prepared=False,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False))
 plan.update(source_revision=3,predecessor_plan_pin=oldplanpin,predecessor_Source_freeze_pin=oldsfpin,complete_v2_to_v3_inverse_pin=iv,source_namespace=str(OUT),actual_added_current_protection_list_block_metadata_only_fixture_passed=True)
 pp=write(OUT/PLANNAME,plan)
 sf.update(Source_pins=[pin(OUT/n)for n in h.NAMES],exact_role_plan_pin=pp,strict_low_level_Source_provenance_pin=iv,Source_preparer_pin=pin(__file__),predecessor_Source_freeze_pin=oldsfpin,source_revision=3)
 sp=write(OUT/SFNAME,sf);fd=os.open(OUT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='EXACT4_SHORT_FIL_RETRY_V3_SOURCE_ONLY_ACTUAL_LIBRARY_LIST_FIXED',Source_freeze_pin=sp,Source_pins=sf['Source_pins'],plan_pin=pp,inverse_pin=iv,preparer_pin=pin(__file__),target_count=4,target_bytes=1014071384,actual_added_current_protection_metadata_fixture_passed=True,manifest_prepared=False,science_or_target_body_EOF_read=False,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False)),flush=True)
if __name__=='__main__':main()
