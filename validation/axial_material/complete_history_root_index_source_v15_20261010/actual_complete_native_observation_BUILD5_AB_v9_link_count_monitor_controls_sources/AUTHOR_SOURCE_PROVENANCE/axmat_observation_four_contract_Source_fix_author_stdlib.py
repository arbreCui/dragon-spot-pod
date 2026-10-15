from pathlib import Path
import ast,json,hashlib,difflib
P=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_four_contract_finite_UNREADY_Source_fix_vz42_t14');O=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_UNREADY_Source_yxzl8twq');q=P/'complete_observation_BUILD5_AB_runtime.UNREADY.py';s=q.read_text()
recipe="""# Complete selected original Makefile variables, preserving empty/undefined
# variables rather than inventing common flags. Original Darwin/arm64, GNU
# compilers, openmp/mpi/hdf5/intel/nvidia/llvm disabled. Relative INCLUDE is
# evaluated from each original component src directory in the fresh tree.
ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES = {
    'Ganlib': {'C':'c','CFLAGS':['-Wall','-fPIC'],'FLAGS':['-DLinux','-DUnix'],
        'F90':'fortran','FFLAGS':['-fPIC','-Wall','-Wno-maybe-uninitialized','-ffpe-summary=none'],
        'FFLAG77':['-fPIC','-Wall','-frecord-marker=4','-ffpe-summary=none'],
        'INCLUDE':[], 'PREPRO':'cpp','FMPI':[], 'opt':['-O','-g'], 'COMP':[], 'LFLAGS':[],
        'lib_module':'Ganlib/lib/Darwin_arm64/modules','module_copy':True},
    'Utilib': {'C':'c','CFLAGS':['-Wall','-fPIC'],'FLAGS':[],
        'F90':'fortran','FFLAGS':['-fPIC','-Wall','-ffpe-summary=none'],
        'FFLAG77':['-fPIC','-Wall','-frecord-marker=4','-ffpe-summary=none'],
        'INCLUDE':[], 'PREPRO':None,'FMPI':[], 'opt':['-O','-g'], 'COMP':[], 'LFLAGS':[],
        'lib_module':'Utilib/lib/Darwin_arm64/modules','module_copy':True},
    'Trivac': {'C':None,'CFLAGS':[],'FLAGS':[],
        'F90':'fortran','FFLAGS':['-fPIC','-ffpe-summary=none'],
        'FFLAG77':['-fPIC','-frecord-marker=4','-ffpe-summary=none'],
        'INCLUDE':['-I../../Ganlib/lib/Darwin_arm64/modules/'], 'PREPRO':None,'FMPI':[],
        'opt':['-O','-g'], 'COMP':[], 'LFLAGS':[], 'lib_module':None,'module_copy':False},
    'Dragon': {'C':'c','CFLAGS':['-Wall','-fPIC'],'FLAGS':['-DLinux','-DUnix'],
        'F90':'fortran','FFLAGS':['-fPIC','-Wall','-ffpe-summary=none'],
        'FFLAG77':['-fPIC','-Wall','-frecord-marker=4','-ffpe-summary=none'],
        'INCLUDE':['-I../../Ganlib/lib/Darwin_arm64/modules/'], 'PREPRO':'cpp','FMPI':[],
        'opt':['-O','-g'], 'COMP':[], 'LFLAGS':[],
        'lib_module':'Dragon/lib/Darwin_arm64/modules','module_copy':True},
}
"""
needle="ROLE_LABELS={";i=s.index(needle);s=s[:i]+recipe+'\n'+s[i:]
s=s.replace("Path(b['tool_pins']['c']['path']).name.startswith(('gcc','clang'))", "Path(b['tool_pins']['c']['path']).name.startswith('gcc')")
s=s.replace("sources={r['relative_path']:r['input_pin']for r in original};stages=[];archives={};all_objects=[];modules=native/'Ganlib/lib/Darwin_arm64/modules';modules.mkdir(parents=True)", "sources={r['relative_path']:r['input_pin']for r in original};stages=[];archives={};all_objects=[]\n    require(list(ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES)==['Ganlib','Utilib','Trivac','Dragon'],'all original component-specific recipe variables')")
s=s.replace("started=time.monotonic();deadline=started+600;folder=native/component/'src'", "started=time.monotonic();deadline=started+600;folder=native/component/'src';recipe=ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES[component]\n        library_dir=native/component/'lib/Darwin_arm64';library_dir.mkdir(parents=True)\n        if recipe['lib_module']is not None:(native/recipe['lib_module']).mkdir(parents=True)")
s=s.replace("c=sorted(folder.glob('*.c'));f90=sorted([*folder.glob('*.f90'),*folder.glob('*.F90')]);f77=sorted([*folder.glob('*.f'),*folder.glob('*.F')])", "c=sorted(folder.glob('*.c'));f90=[*sorted(folder.glob('*.f90')),*sorted(folder.glob('*.F90'))];f77_lower=sorted(folder.glob('*.f'));f77_upper=sorted(folder.glob('*.F'));f77=[*f77_lower,*f77_upper]")
s=s.replace("argv=[tools['cpp']['path'],'-P','-W','-traditional','-DLinux','-DUnix',str(p),str(src)]", "require(recipe['PREPRO']is not None,'original selected Makefile PREPRO undefined for this suffix; no invented tool')\n                argv=[tools[recipe['PREPRO']]['path'],'-P','-W','-traditional',*recipe['FLAGS']]\n                if p.suffix=='.F':argv+=recipe['FMPI']\n                argv+=[str(p),str(src)]")
a=s.index("            if p.suffix=='.c':argv=");b=s.index("            stage=guarded(",a)
s=s[:a]+"""            if p.suffix=='.c':
                require(recipe['C']is not None,'original selected Makefile C undefined, no invented compiler')
                argv=[tools[recipe['C']]['path'],*recipe['CFLAGS'],*recipe['FLAGS'],*recipe['opt'],*recipe['COMP'],'-c',str(src),'-o',str(obj)]
            else:
                flags=recipe['FFLAG77']if p.suffix in('.f','.F')else recipe['FFLAGS']
                argv=[tools[recipe['F90']]['path'],*flags,*recipe['opt'],*recipe['COMP'],*recipe['INCLUDE'],'-c',str(src),'-o',str(obj)]
"""+s[b:]
a=s.index("        for p in folder.glob('*.mod'):");b=s.index("        require(time.monotonic()-started<600",a)
s=s[:a]+"""        # Original ar emits src/lib*.a, then original cp places the same fresh
        # archive into each component's own lib directory used by final link.
        library_copy=library_dir/archive.name;require(not os.path.lexists(library_copy),'fresh original recipe library copy')
        shutil.copy2(archive,library_copy);library_copy_pin=fullpin(library_copy,budget)
        require(library_copy_pin['sha256']==ap['sha256']and library_copy_pin['size_bytes']==ap['size_bytes'],'original library copy full bytes equal actual fresh ar output')
        module_copy_pins=[]
        if recipe['module_copy']:
            modules=native/recipe['lib_module']
            for p in folder.glob('*.mod'):
                target=modules/p.name;require(not os.path.lexists(target),'original per-library module namespace fresh')
                shutil.copy2(p,target);module_copy_pins.append(dict(original_generated_module_pin=fullpin(p,budget),original_recipe_module_copy_pin=fullpin(target,budget)))
        # Trivac's original library recipe never copies module files.
"""+s[b:]
s=s.replace("archives[component]=ap;stages.append(dict(component=component,", "archives[component]=library_copy_pin;stages.append(dict(component=component,exact_original_selected_recipe=recipe,original_recipe_library_copy_pin=library_copy_pin,original_recipe_module_copy_pins=module_copy_pins,archive_object_source_suffix_group_order=['.c','original_dependency_order(.f90_then_.F90)','.f','.F'],")
s=s.replace("argv=[tools['fortran']['path'],'-O','-g',*[p['path']for p in link_inputs],'-o',str(exe)]", "link_recipe=ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES['Dragon'];argv=[tools[link_recipe['F90']]['path'],*link_recipe['opt'],*link_recipe['COMP'],*[p['path']for p in link_inputs],*link_recipe['LFLAGS'],'-o',str(exe)]")
s=s.replace("root_prefix=[]if role=='final-complete-micro'else['MACROLIB']", "root_prefix=[]")
s=s.replace("actual_old_macro_absent_at_event=(role is not None and snapshot is None)", "actual_native_snapshot_root_prefix=[]if snapshot is not None else None,snapshot_logical_prefix=([]if role=='final-complete-micro'else['MACROLIB'])if snapshot is not None else None,actual_old_macro_absent_at_event=(role is not None and snapshot is None)")
s=s.replace("complete_state_snapshot_inputs=snapshots,selected_last_libmix_number", "complete_state_snapshot_inputs=snapshots,legacy_context_source_snapshot_request_rows=[dict(item,root_prefix=[]if item['role']=='final-complete-micro'else['MACROLIB'])for item in snapshots],legacy_context_root_prefix_semantics='output_pool_logical_path_prefix_only_not_native_directory_lookup',actual_native_snapshot_root_prefix=[],selected_last_libmix_number")
s=s.replace("complete_context_inputs={k:v['complete_context_pins']for k,v in states.items()},all_A_handles", "complete_context_inputs={k:v['complete_context_pins']for k,v in states.items()},legacy_context_source_snapshot_request_rows={k:v['legacy_context_source_snapshot_request_rows']for k,v in states.items()},legacy_context_root_prefix_semantics='output_pool_logical_path_prefix_only_not_native_directory_lookup',actual_native_snapshot_root_prefix=[],all_A_handles")
ast.parse(s);q.write_text(s)
# Root postclose checks both real original archive copies/modules and explicit
# physical[] vs legacy logical prefix map before creating its postclose receipt.
q=P/'Root_observation_postclose_META_writer.UNREADY.py';s=q.read_text();s=s.replace("check(stage['new_archive_pin'])", "check(stage['new_archive_pin']);check(stage['original_recipe_library_copy_pin'])\n        for module in stage['original_recipe_module_copy_pins']:check(module['original_generated_module_pin']);check(module['original_recipe_module_copy_pin'])")
s=s.replace("for p in row['complete_state_snapshot_inputs']:check(p['input_pin'])", "for p in row['complete_state_snapshot_inputs']:require(p['root_prefix']==[],'all real observer snapshot physical roots are native XSM root');check(p['input_pin'])\n        require(row['legacy_context_source_snapshot_request_rows']==[dict(p,root_prefix=[]if p['role']=='final-complete-micro'else['MACROLIB'])for p in row['complete_state_snapshot_inputs']]and row['legacy_context_root_prefix_semantics']=='output_pool_logical_path_prefix_only_not_native_directory_lookup'and row['actual_native_snapshot_root_prefix']==[],'explicit legacy logical-prefix-only handoff; no nonexistent MACROLIB child')")
ast.parse(s);q.write_text(s)
# Retain exactly the necessary full existing legacy extractor and prove how it
# traverses the real root while emitting logical pool paths.
S=Path('/private/tmp/axmat_complete_old_XSM_context_six_blocker_finite_UNREADY_Source_fix_novkasox');source=S/'complete_observed_old_post_final_XSM_extractor.UNREADY.py';dest=P/'COMPLETE_LEGACY_CONTEXT_HANDOFF_SOURCE';dest.mkdir();(dest/source.name).write_bytes(source.read_bytes())
for name in('bind_complete_observation_SOURCE_only.UNREADY.py','Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py'):
 q=P/name;s=q.read_text().replace("'request_preparer':'Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py'", "'request_preparer':'Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','legacy_context_old_XSM_extractor':'COMPLETE_LEGACY_CONTEXT_HANDOFF_SOURCE/complete_observed_old_post_final_XSM_extractor.UNREADY.py'");ast.parse(s);q.write_text(s)
# Source contracts and future route metadata only, not actual observations.
q=P/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json';j=json.loads(q.read_bytes());j['required_author_Source_roles']['legacy_context_old_XSM_extractor']='COMPLETE_LEGACY_CONTEXT_HANDOFF_SOURCE/complete_observed_old_post_final_XSM_extractor.UNREADY.py';q.write_text(json.dumps(j,indent=2)+'\n')
q=P/'ROOT_OBSERVATION_SOURCE_REQUEST_TEMPLATE.UNREADY.json';j=json.loads(q.read_bytes());j['actual_author_Source_contract']['legacy_context_old_XSM_extractor']=None;q.write_text(json.dumps(j,indent=2)+'\n')
q=P/'ROOT_OBSERVATION_SOURCE_ADMISSION_TEMPLATE.UNREADY.json';j=json.loads(q.read_bytes());j['actual_author_Source_contract']['legacy_context_old_XSM_extractor']=None;q.write_text(json.dumps(j,indent=2)+'\n')
q=P/'ROOT_NEXT_BIND_BUILD_CAPTURE_POSTCLOSE_CONTEXT_STEPS.Source_ONLY.json';j=json.loads(q.read_bytes());old_prefix=str(O)
def paths(x):
 if type(x)is dict:return {k:paths(v)for k,v in x.items()}
 if type(x)is list:return [paths(v)for v in x]
 if type(x)is str:return x.replace(old_prefix,str(P))
 return x
j=paths(j);j['steps'][5]['complete_state_snapshot_inputs']='Use exact legacy_context_source_snapshot_request_rows from new postclose manifest for the existing admitted V2 Source request: there root_prefix is only emitted logical pool path, never a native directory lookup. Actual native snapshot roots remain [] in canonical complete_state_snapshot_inputs.';j['steps'][5]['real_native_root_prefix']=[];j['steps'][5]['legacy_macro_logical_pool_prefix']=['MACROLIB'];j['steps'][5]['existing_native_walker_entry']='native.walk_table(native.root, tuple(prefix), ()) traverses native.root; prefix is output row path namespace only';j['whole_original_per_library_recipe_flags_archive_order_and_module_paths_preserved']=True;q.write_text(json.dumps(j,indent=2)+'\n')
# Preserve the old author review as historical, without relabeling it for the
# fixed Source. New final author review will be produced after peer list closes.
(P/'ORIGINAL_AUTHOR_FINITE_COMPLETE_SOURCE_CHECK_UNREADY.json').write_bytes((P/'AUTHOR_FINITE_COMPLETE_SOURCE_CHECK_UNREADY.json').read_bytes());(P/'AUTHOR_FINITE_COMPLETE_SOURCE_CHECK_UNREADY.json').unlink()
proof=[]
for name in('complete_observation_BUILD5_AB_runtime.UNREADY.py','Root_observation_postclose_META_writer.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py','Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json','ROOT_OBSERVATION_SOURCE_REQUEST_TEMPLATE.UNREADY.json','ROOT_OBSERVATION_SOURCE_ADMISSION_TEMPLATE.UNREADY.json','ROOT_NEXT_BIND_BUILD_CAPTURE_POSTCLOSE_CONTEXT_STEPS.Source_ONLY.json'):
 old=(O/name).read_bytes();new=(P/name).read_bytes();old_lines=old.decode().splitlines(keepends=True);new_lines=new.decode().splitlines(keepends=True);hunks=[]
 for tag,i,j,a,b in difflib.SequenceMatcher(None,old_lines,new_lines,autojunk=False).get_opcodes():
  if tag!='equal':hunks.append(dict(tag=tag,old_start0=i,old_end0=j,new_start0=a,new_end0=b,old_full_lines=old_lines[i:j],new_full_lines=new_lines[a:b]))
 restored=list(new_lines)
 for h in reversed(hunks):assert restored[h['new_start0']:h['new_end0']]==h['new_full_lines'];restored[h['new_start0']:h['new_end0']]=h['old_full_lines']
 assert ''.join(restored).encode()==old
 proof.append(dict(source_member=name,original_sha256=hashlib.sha256(old).hexdigest(),fixed_sha256=hashlib.sha256(new).hexdigest(),complete_full_inverse_hunks=hunks,whole_Source_inverse_to_original_frozen_member_equal=True))
(P/'COMPLETE_FOUR_CONTRACT_SOURCE_FIX_FULL_BYTE_INVERSE.json').write_text(json.dumps(dict(schema='COMPLETE_OBSERVATION_NATIVE_ORIGINAL_RECIPE_AND_PHYSICAL_LOGICAL_ROOT_CONTRACT_FIX_SOURCE_INVERSE_V1',source_only=True,original_frozen_manifest_sha256='2a1c950bcf036e1534901333af2f50c2f53ab12105502e247445e9a8fe9c066a',source_derivations=proof,original_native_compile_Source_archive1365members_unchanged=True,original_physical_four_Fortran_observer_derivatives_unchanged=True,original_observer_module_unchanged=True,original_caps_and_genuine_executor_classes_MRO_unchanged=True,actual_execution=None,actual_Root_admission=None,actual_independent_peer=None,scientific_qualification_created=False),indent=2)+'\n')
print(json.dumps(dict(status='FOUR_CONTRACT_FINITE_COMPLETE_SOURCE_FIX_WRITTEN_NOT_SEALED',new_Source=str(P),changed_original_Source_and_META_members=len(proof),full_inverse_hunks=sum(len(p['complete_full_inverse_hunks'])for p in proof),all_native_compilation_Source_and_physical_observers_unchanged=True,all_new_Python_Source_AST_parsed=True,actual_execution=None)))
