"""Author-only Source/AST/bytes derivative. Never import or execute any role."""
import ast
import difflib
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import tarfile
import tempfile

OLD=Path('/private/tmp/axmat_complete_native_observation_N5_closed_PS_only_UNREADY_Source_ei2bldc9')
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
NEW=Path(tempfile.mkdtemp(prefix='axmat_complete_native_observation_N6_shared_original_libraries_UNREADY_Source_',dir='/private/tmp'))
CHECKS=[]
def check(v,label):
    if type(v)is not bool or not v:raise ValueError(label)
    CHECKS.append(dict(check=label,passed=True))
def fullpin(p):
    p=Path(p);s=p.lstat();i=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    if not stat.S_ISREG(s.st_mode)or s.st_nlink!=1 or any(q.is_symlink()for q in(p,*p.parents)):raise ValueError('author Source ordinary singlelink only')
    with p.open('rb')as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    z=p.lstat()
    if [z.st_dev,z.st_ino,z.st_mode,z.st_nlink,z.st_size,z.st_mtime_ns,z.st_ctime_ns]!=i:raise ValueError('author full EOF race')
    return dict(path=str(p),sha256=h,size_bytes=s.st_size,identity=i)
def dump(p,x):
    with Path(p).open('x')as f:json.dump(x,f,indent=2,allow_nan=False);f.write('\n')
def replace_once(s,a,b):
    if s.count(a)!=1:raise ValueError('one whole Source hunk '+a[:100])
    return s.replace(a,b,1)
before={str(q.relative_to(OLD)):fullpin(q)for q in sorted(OLD.rglob('*'))if q.is_file()}
mf=json.loads((OLD/'MANIFEST.json').read_bytes())
check(before['MANIFEST.json']['sha256']=='cd59bbcb952c5a444bcc970de1cf647df0abaac8388d47d6b929da0562111fec','actual frozen N5 manifest whole EOF')
for row in mf['members']:check(before[row['relative_path']]==row['fullpin'],'original N5 member '+row['relative_path'])
for q in sorted(OLD.rglob('*')):
    rel=q.relative_to(OLD);dst=NEW/rel
    if q.is_dir():dst.mkdir()
    elif rel.name!='MANIFEST.json' or rel.parent!=Path('.'):
        shutil.copy2(q,dst)
prov=NEW/'PREVIOUS_SEALED_N5_SOURCE_PROVENANCE';prov.mkdir()
shutil.copy2(OLD/'MANIFEST.json',prov/'MANIFEST.json')
changed=['complete_observation_BUILD5_AB_runtime.UNREADY.py','Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py','Root_observation_postclose_META_writer.UNREADY.py']
for f in changed:shutil.copy2(OLD/f,prov/f)

layout={'schema':'COMPLETE_AB_SINGLE_COPY_ORIGINAL_SHARED_LIBRARIES_AND_EXACT_PROCEDURE_FILE_LITERALS_V1','shared_directory':'shared_input_libraries','state_order':['A','B'],'seed_destination_order':['material.x2m','AxMatTone.c2m','geometry.dat','rnr_cc.c2m','rnr_interpol.c2m','DLIB_ACTUAL','DLIB8R1_370'],'original_procedure_copy_name':'AxMatTone.c2m.original','literal_replacements':[{'original':"FIL: 'DLIB_ACTUAL'",'derived':"FIL: '../shared_input_libraries/DLIB_ACTUAL'",'count':2},{'original':"FIL: 'DLIB8R1_370'",'derived':"FIL: '../shared_input_libraries/DLIB8R1_370'",'count':1}]}
constant='SHARED_INPUT_LIBRARY_LAYOUT = '+repr(layout)+'\n'
layout_test="require(b.get('material_input_layout')==SHARED_INPUT_LIBRARY_LAYOUT and all(type(row['count'])is int for row in b['material_input_layout']['literal_replacements']),'exact shared-library/procedure Source layout; no implicit old duplicate layout')"

runtime_helpers='''def original_shared_libraries(b):
    libraries={}
    for state in ('A','B'):
        for row in b['states'][state]['native_stage_inputs']:
            if row['destination']in('DLIB_ACTUAL','DLIB8R1_370'):
                previous=libraries.get(row['destination'])
                require(previous is None or previous==row['input_pin'],'same complete original library source for A and B')
                libraries[row['destination']]=row['input_pin']
    require(list(libraries)==['DLIB_ACTUAL','DLIB8R1_370'],'both complete original library roles ordered')
    return libraries

def prepare_shared_libraries(out,b,budget):
    shared=out/SHARED_INPUT_LIBRARY_LAYOUT['shared_directory'];require(not os.path.lexists(shared),'fresh one-copy original library directory');shared.mkdir()
    originals=original_shared_libraries(b);copies={}
    for name,p in originals.items():
        recheck(p,budget);dest=shared/name
        with Path(p['path']).open('rb')as src,dest.open('xb')as dst:shutil.copyfileobj(src,dst,2**20)
        actual=fullpin(dest,budget);require(actual['sha256']==p['sha256']and actual['size_bytes']==p['size_bytes'],'entire original library copied once without aliases');copies[name]=actual;recheck(p,budget)
    return dict(schema='ACTUAL_AB_SINGLE_COPY_COMPLETE_ORIGINAL_LIBRARY_EVIDENCE_V1',original_input_pins=originals,shared_copy_pins=copies,material_input_layout=SHARED_INPUT_LIBRARY_LAYOUT,shared_library_directory=str(shared),all_library_bytes_preserved_without_symlinks_or_hardlinks=True,actual_state_library_full_EOF_observations={})

def recheck_shared_libraries(shared,budget):
    originals={name:recheck(p,budget)for name,p in shared['original_input_pins'].items()}
    copies={name:recheck(p,budget)for name,p in shared['shared_copy_pins'].items()}
    return dict(original_library_full_EOF_pins=originals,shared_library_full_EOF_pins=copies)

def derive_original_procedure(raw):
    require(type(raw)is bytes and len(raw)<=2**20,'small complete pinned procedure Source only')
    result=raw
    for row in SHARED_INPUT_LIBRARY_LAYOUT['literal_replacements']:
        old=row['original'].encode('ascii');new=row['derived'].encode('ascii')
        require(raw.count(old)==row['count']and raw.count(new)==0 and len(new.split(b"'")[1])<=64,'all and only original FIL literal occurrences fit actual NAMFIL64')
        result=result.replace(old,new)
    restored=result
    for row in SHARED_INPUT_LIBRARY_LAYOUT['literal_replacements']:
        old=row['original'].encode('ascii');new=row['derived'].encode('ascii');require(restored.count(new)==row['count'],'derived complete FIL occurrence count');restored=restored.replace(new,old)
    require(restored==raw,'entire procedure reverse replacement exactly original Source bytes')
    return result

def copy_state_seeds(folder,seeds,shared,budget):
    require([row['destination']for row in seeds]==SHARED_INPUT_LIBRARY_LAYOUT['seed_destination_order'],'all seven original seed roles in original order')
    copies=[];mapping=[];procedure=None
    for row in seeds:
        p=row['input_pin'];name=row['destination'];recheck(p,budget);original_procedure_pin=None
        if name in('DLIB_ACTUAL','DLIB8R1_370'):
            require(p==shared['original_input_pins'][name],'same original library role source');actual=recheck(shared['shared_copy_pins'][name],budget)
        else:
            dest=folder/name;require(not os.path.lexists(dest),'fresh material seed Source')
            if name=='AxMatTone.c2m':
                original=folder/SHARED_INPUT_LIBRARY_LAYOUT['original_procedure_copy_name'];require(not os.path.lexists(original),'fresh retained complete original procedure')
                with Path(p['path']).open('rb')as src,original.open('xb')as dst:shutil.copyfileobj(src,dst,2**20)
                original_procedure_pin=fullpin(original,budget);require(original_procedure_pin['sha256']==p['sha256']and original_procedure_pin['size_bytes']==p['size_bytes'],'complete original procedure independently retained')
                raw=original.read_bytes();derived=derive_original_procedure(raw)
                with dest.open('xb')as dst:dst.write(derived)
                actual=fullpin(dest,budget)
                procedure=dict(schema='ACTUAL_COMPLETE_ORIGINAL_PROCEDURE_THREE_FIL_LITERAL_PATH_REPLACEMENTS_V1',original_input_pin=p,retained_original_procedure_pin=original_procedure_pin,actual_consumed_derived_procedure_pin=actual,original_complete_ASCII_Source=raw.decode('ascii'),derived_complete_ASCII_Source=derived.decode('ascii'),exact_literal_replacements=SHARED_INPUT_LIBRARY_LAYOUT['literal_replacements'],whole_reverse_replacement_equals_original_bytes=True,all_numeric_and_non_FIL_Source_bytes_unchanged=True,actual_genuine_material_CWD=str(folder),relative_shared_library_targets={name:str((folder/('../shared_input_libraries/'+name)).resolve())for name in shared['shared_copy_pins']},ILIBRARYNAME_filename_provenance_changes_are_preserved_not_claimed_equal=True)
                require(procedure['relative_shared_library_targets']=={name:p['path']for name,p in shared['shared_copy_pins'].items()},'actual A/B relative file paths resolve only to original shared copies')
            else:
                with Path(p['path']).open('rb')as src,dest.open('xb')as dst:shutil.copyfileobj(src,dst,2**20)
                actual=fullpin(dest,budget);require(actual['sha256']==p['sha256']and actual['size_bytes']==p['size_bytes'],'all other original seed Source bytes unchanged')
        copies.append(actual);mapping.append(dict(destination=name,original_input_pin=p,actual_consumed_pin=actual,retained_original_procedure_pin=original_procedure_pin))
        recheck(p,budget)
    require(procedure is not None,'complete original and actual consumed procedure evidence')
    copies.append(procedure['retained_original_procedure_pin'])
    return copies,mapping,procedure

'''

raws={f:(OLD/f).read_text()for f in changed};s=raws[changed[0]]
s=replace_once(s,'No old binary/object/archive, no deck construction, no payload truncation.','No old binary/object/archive or material deck construction; only three procedure FIL path literals change. No payload truncation.')
s=replace_once(s,'def validate_request(b,author):\n',constant+'\ndef validate_request(b,author):\n    '+layout_test+'\n')
s=replace_once(s,"inputs=b['states'][state]['native_stage_inputs'];require(type(inputs)is list and {row['destination']for row in inputs}==required and len(inputs)==len(required)","inputs=b['states'][state]['native_stage_inputs'];require(type(inputs)is list and [row['destination']for row in inputs]==SHARED_INPUT_LIBRARY_LAYOUT['seed_destination_order']and {row['destination']for row in inputs}==required and len(inputs)==len(required)")
s=replace_once(s,'def collect_state(folder,state,deck_pin,exe_pin,stage,budget):',runtime_helpers+'def collect_state(folder,state,deck_pin,exe_pin,stage,budget):')
s=replace_once(s,"bp=fullpin(control/'ACTUAL_COMPLETE_NATIVE_SOURCE_BINARY_LINK_EVIDENCE.json',budget);states={}","bp=fullpin(control/'ACTUAL_COMPLETE_NATIVE_SOURCE_BINARY_LINK_EVIDENCE.json',budget);states={};shared=prepare_shared_libraries(out,b,budget);resources.check()")
old_block="""            for row in seeds:
                recheck(row['input_pin'],budget);dest=folder/row['destination'];require(not os.path.lexists(dest),'fresh immutable material input copy')
                with Path(row['input_pin']['path']).open('rb')as src,dest.open('xb')as dst:shutil.copyfileobj(src,dst,2**20)
                actual=fullpin(dest,budget);require(actual['sha256']==row['input_pin']['sha256']and actual['size_bytes']==row['input_pin']['size_bytes'],'original material seed bytes unchanged');seedCopies.append(actual)
"""
s=replace_once(s,old_block,"            shared_before=recheck_shared_libraries(shared,budget);seedCopies,seedMapping,procedureEvidence=copy_state_seeds(folder,seeds,shared,budget)\n")
s=replace_once(s,"            for p in seedCopies:recheck(p,budget)\n", "            for p in seedCopies:recheck(p,budget)\n            shared_after=recheck_shared_libraries(shared,budget);require(shared_before==shared_after,'all original and shared library whole EOF7IDs unchanged across actual state')\n")
s=replace_once(s,"            states[state]['actual_material_seed_copy_pins']=seedCopies\n", "            states[state]['actual_material_seed_copy_pins']=seedCopies\n            states[state]['actual_material_seed_role_mapping']=seedMapping;states[state]['actual_original_and_consumed_procedure_Source_evidence']=procedureEvidence\n            shared['actual_state_library_full_EOF_observations'][state]=dict(before_actual_material_stage=shared_before,after_actual_material_stage=shared_after)\n")
s=replace_once(s,"require(not any(Path(v).is_relative_to(folder)for v in closure['actual_open_regular_paths']),'all own process material state handles closed before next state')", "require(not any(Path(v).is_relative_to(folder)or Path(v).is_relative_to(Path(shared['shared_library_directory']))for v in closure['actual_open_regular_paths']),'all own process material state and shared library handles closed before next state')")
s=replace_once(s,"schema='ACTUAL_COMPLETE_AXOBSCTXv2_AB_OBSERVATION_MANIFEST_V1',source_only=False,state_order=['A','B'],states=states,", "schema='ACTUAL_COMPLETE_AXOBSCTXv2_AB_OBSERVATION_MANIFEST_V1',source_only=False,state_order=['A','B'],states=states,material_input_layout=SHARED_INPUT_LIBRARY_LAYOUT,actual_shared_input_library_evidence=shared,")
(NEW/changed[0]).write_text(s)

s=raws[changed[1]];s=replace_once(s,'def main():\n',constant+'\ndef main():\n')
s=replace_once(s,"states=states,namespaces={k:getattr(a,k)","states=states,material_input_layout=SHARED_INPUT_LIBRARY_LAYOUT,namespaces={k:getattr(a,k)")
(NEW/changed[1]).write_text(s)
s=raws[changed[2]];s=replace_once(s,'def main():\n',constant+'\ndef main():\n')
s=replace_once(s,"    needed={'material.x2m'",'    '+layout_test+"\n    needed={'material.x2m'")
s=replace_once(s,"type(stage)is list and len(stage)==7 and {r['destination']for r in stage}==needed","type(stage)is list and len(stage)==7 and [r['destination']for r in stage]==SHARED_INPUT_LIBRARY_LAYOUT['seed_destination_order']and {r['destination']for r in stage}==needed")
(NEW/changed[2]).write_text(s)

post_helpers='''def verify_complete_shared_library_and_procedure_evidence(b,m):
    require(b.get('material_input_layout')==SHARED_INPUT_LIBRARY_LAYOUT and m.get('material_input_layout')==SHARED_INPUT_LIBRARY_LAYOUT,'exact bound and actual shared-library/procedure contract')
    shared=m['actual_shared_input_library_evidence'];out=Path(b['namespaces']['output']);directory=out/SHARED_INPUT_LIBRARY_LAYOUT['shared_directory']
    require(shared['schema']=='ACTUAL_AB_SINGLE_COPY_COMPLETE_ORIGINAL_LIBRARY_EVIDENCE_V1'and shared['material_input_layout']==SHARED_INPUT_LIBRARY_LAYOUT and shared['shared_library_directory']==str(directory)and shared['all_library_bytes_preserved_without_symlinks_or_hardlinks']is True,'actual original two libraries once with no aliases')
    originals=shared['original_input_pins'];copies=shared['shared_copy_pins'];require(list(originals)==list(copies)==['DLIB_ACTUAL','DLIB8R1_370'],'all original shared-library roles in order')
    for name in originals:
        check(originals[name]);check(copies[name]);require(copies[name]['path']==str(directory/name)and copies[name]['sha256']==originals[name]['sha256']and copies[name]['size_bytes']==originals[name]['size_bytes'],'actual shared copy complete original bytes and path')
    require({p.name for p in directory.iterdir()}==set(copies),'shared namespace has only two original ordinary libraries')
    observations=shared['actual_state_library_full_EOF_observations'];require(list(observations)==['A','B'],'both actual states have original/shared full EOF observations')
    expected=dict(original_library_full_EOF_pins=originals,shared_library_full_EOF_pins=copies)
    for state in ('A','B'):
        observed=observations[state];require(observed==dict(before_actual_material_stage=expected,after_actual_material_stage=expected),'all four actual state boundary original/shared EOF7ID observations identical')
        row=m['states'][state];folder=out/state;seeds=b['states'][state]['native_stage_inputs'];mapping=row['actual_material_seed_role_mapping'];require(type(mapping)is list and len(mapping)==7 and [item['destination']for item in mapping]==SHARED_INPUT_LIBRARY_LAYOUT['seed_destination_order'],'all seven consumed seed roles remain explicit and ordered')
        require([item['original_input_pin']for item in mapping]==[seed['input_pin']for seed in seeds],'each consumed seed original source exact binding')
        for item in mapping:
            require(set(item)=={'destination','original_input_pin','actual_consumed_pin','retained_original_procedure_pin'},'exact full seed provenance row');check(item['original_input_pin']);check(item['actual_consumed_pin']);name=item['destination']
            if name in copies:
                require(item['original_input_pin']==originals[name]and item['actual_consumed_pin']==copies[name]and item['retained_original_procedure_pin']is None,'complete shared-library role without duplicate files')
            elif name=='AxMatTone.c2m':
                check(item['retained_original_procedure_pin']);require(item['actual_consumed_pin']['path']==str(folder/name)and item['retained_original_procedure_pin']['path']==str(folder/SHARED_INPUT_LIBRARY_LAYOUT['original_procedure_copy_name'])and item['retained_original_procedure_pin']['sha256']==item['original_input_pin']['sha256']and item['retained_original_procedure_pin']['size_bytes']==item['original_input_pin']['size_bytes'],'separate whole original and consumed procedure file identities')
            else:
                require(item['actual_consumed_pin']['path']==str(folder/name)and item['retained_original_procedure_pin']is None and item['actual_consumed_pin']['sha256']==item['original_input_pin']['sha256']and item['actual_consumed_pin']['size_bytes']==item['original_input_pin']['size_bytes'],'all other original seed bytes unchanged')
        procedure=row['actual_original_and_consumed_procedure_Source_evidence'];item=mapping[1];require(procedure['schema']=='ACTUAL_COMPLETE_ORIGINAL_PROCEDURE_THREE_FIL_LITERAL_PATH_REPLACEMENTS_V1'and procedure['original_input_pin']==item['original_input_pin']and procedure['retained_original_procedure_pin']==item['retained_original_procedure_pin']and procedure['actual_consumed_derived_procedure_pin']==item['actual_consumed_pin']and procedure['exact_literal_replacements']==SHARED_INPUT_LIBRARY_LAYOUT['literal_replacements'],'actual complete procedure Source provenance coupled')
        require(item['original_input_pin']['size_bytes']<=2**20 and item['actual_consumed_pin']['size_bytes']<=2**20,'small pinned complete procedure Source only')
        original=Path(item['original_input_pin']['path']).read_bytes();retained=Path(item['retained_original_procedure_pin']['path']).read_bytes();derived=Path(item['actual_consumed_pin']['path']).read_bytes();require(retained==original and procedure['original_complete_ASCII_Source']==original.decode('ascii')and procedure['derived_complete_ASCII_Source']==derived.decode('ascii'),'whole actual original/retained/derived Source text exact')
        expected_derived=original
        for replacement in SHARED_INPUT_LIBRARY_LAYOUT['literal_replacements']:
            old=replacement['original'].encode('ascii');new=replacement['derived'].encode('ascii');require(original.count(old)==replacement['count']and original.count(new)==0 and len(new.split(b"'")[1])<=64,'every original exact FIL occurrence and actual NAMFIL64 bound');expected_derived=expected_derived.replace(old,new)
        require(derived==expected_derived,'entire consumed Source only three exact FIL path substitutions')
        inverse=derived
        for replacement in SHARED_INPUT_LIBRARY_LAYOUT['literal_replacements']:
            old=replacement['original'].encode('ascii');new=replacement['derived'].encode('ascii');require(inverse.count(new)==replacement['count'],'every actual derived FIL occurrence');inverse=inverse.replace(new,old)
        require(inverse==original and procedure['whole_reverse_replacement_equals_original_bytes']is True and procedure['all_numeric_and_non_FIL_Source_bytes_unchanged']is True and procedure['ILIBRARYNAME_filename_provenance_changes_are_preserved_not_claimed_equal']is True,'full Source byte inverse and honest actual library-name provenance change')
        require(procedure['actual_genuine_material_CWD']==str(folder)and procedure['relative_shared_library_targets']=={name:p['path']for name,p in copies.items()}and all((folder/('../shared_input_libraries/'+name)).resolve()==Path(p['path'])for name,p in copies.items()),'same genuine A/B cwd and actual shared targets')
        require(row['actual_material_seed_copy_pins']==[item['actual_consumed_pin']for item in mapping]+[mapping[1]['retained_original_procedure_pin']],'all seven consumed role pins plus retained original procedure; no missing role')
        closure=row['actual_no_open_state_handles_observation'];require(closure['all_regular_and_open_unlinked_counted']is True and not any(Path(v).is_relative_to(folder)or Path(v).is_relative_to(directory)for v in closure['actual_open_regular_paths']),'state and original shared-library handles closed before next state')

'''
s=raws[changed[3]];s=replace_once(s,'def main():\n',constant+'\n'+post_helpers+'def main():\n')
s=replace_once(s,'    fullstates={}\n','    verify_complete_shared_library_and_procedure_evidence(b,m)\n    fullstates={}\n')
(NEW/changed[3]).write_text(s)

source_evidence=NEW/'N6_FINITE_ACTUAL_SMALL_SOURCE_AND_META_PROVENANCE';source_evidence.mkdir()
for f in ['Root_actual_duplicate_library_copy_layout_META_budget_20261010.json','Root_actual_duplicate_library_copy_layout_META_budget_tool_terminal_return.json']:
    shutil.copy2(B/f,source_evidence/f)
for state in ('A','B'):
    dst=source_evidence/state;dst.mkdir()
    for name in ('material.x2m','AxMatTone.c2m'):
        q=Path('/Users/wen/spot/validation/artifacts/axial-material-inputs-20261003')/state/name
        shutil.copy2(q,dst/name)
        check(fullpin(q)['sha256']==fullpin(dst/name)['sha256'],'actual authorized small Source full EOF '+state+'/'+name)
dump(source_evidence/'ACTUAL_ORIGINAL_SMALL_DECK_AND_PROCEDURE_SOURCE_PINS.json',{state:{name:fullpin(Path('/Users/wen/spot/validation/artifacts/axial-material-inputs-20261003')/state/name)for name in('material.x2m','AxMatTone.c2m')}for state in('A','B')})

roles=ast.literal_eval(next(n.value for n in ast.parse((NEW/changed[2]).read_bytes()).body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='ROLES'for t in n.targets)))
inverse={};definitions={}
for f in changed:
    a=raws[f].encode();c=(NEW/f).read_bytes();x=a.decode().splitlines(keepends=True);y=c.decode().splitlines(keepends=True);hunks=[]
    for tag,i,j,k,l in difflib.SequenceMatcher(None,x,y,autojunk=False).get_opcodes():
        if tag!='equal':hunks.append(dict(original_start_line_0=i,original_end_line_0=j,derived_start_line_0=k,derived_end_line_0=l,original_complete_hunk=''.join(x[i:j]),derived_complete_hunk=''.join(y[k:l])))
    restored=list(y)
    for h in reversed(hunks):restored[h['derived_start_line_0']:h['derived_end_line_0']]=h['original_complete_hunk'].splitlines(keepends=True)
    check(''.join(restored).encode()==a,'whole byte Source inverse '+f)
    original_tree=ast.parse(a);new_tree=ast.parse(c);olddefs=[n for n in original_tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))];newdefs=[n for n in new_tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
    check(len({n.name for n in olddefs})==len(olddefs)and len({n.name for n in newdefs})==len(newdefs),'unique role definition names '+f)
    om={n.name:n for n in olddefs};nm={n.name:n for n in newdefs};same=[];modified=[]
    for name,n in om.items():
        check(name in nm,'no original definition omitted '+f+':'+name)
        if ast.dump(n,include_attributes=False)==ast.dump(nm[name],include_attributes=False):same.append(name)
        else:modified.append(name)
    inverse[f]=dict(original_Source_pin=before[f],derived_Source_pin=fullpin(NEW/f),whole_byte_inverse_hunks=hunks,whole_restored_original_sha256=hashlib.sha256(a).hexdigest(),whole_original_AST_dump=ast.dump(original_tree,include_attributes=False),whole_derived_AST_dump=ast.dump(new_tree,include_attributes=False))
    definitions[f]=dict(unchanged_original_definition_names=same,changed_original_definition_names=modified,added_definition_names=[n for n in nm if n not in om])
    check(ast.dump(next(n for n in original_tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='CAPS'for t in n.targets)),include_attributes=False)==ast.dump(next(n for n in new_tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='CAPS'for t in n.targets)),include_attributes=False),'nine original caps full AST '+f)
    check(ast.dump(next(n for n in original_tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='FUTURE'for t in n.targets)),include_attributes=False)==ast.dump(next(n for n in new_tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='FUTURE'for t in n.targets)),include_attributes=False),'all future None and false full AST '+f)
check(definitions[changed[0]]['changed_original_definition_names']==['validate_request','run'],'runtime changes only request validation and original A/B seed layout')
check(definitions[changed[1]]['changed_original_definition_names']==['main']and definitions[changed[2]]['changed_original_definition_names']==['main']and definitions[changed[3]]['changed_original_definition_names']==['main'],'request/binder/postclose changes confined original entry bodies plus explicit full evidence helper')
for f,p in before.items():
    if f not in changed and f!='MANIFEST.json':check(fullpin(NEW/f)['sha256']==p['sha256']and fullpin(NEW/f)['size_bytes']==p['size_bytes'],'all other N5 member bytes exact '+f)
for f in roles.values():ast.parse((NEW/f).read_bytes())if f.endswith('.py')else None
check(len(roles)==14,'all fourteen original Source roles retained')
check(definitions[changed[0]]['unchanged_original_definition_names']and 'joint_bytes'in definitions[changed[0]]['unchanged_original_definition_names']and 'compile_all'in definitions[changed[0]]['unchanged_original_definition_names']and 'collect_state'in definitions[changed[0]]['unchanged_original_definition_names'],'complete N5 PS-only accounting five native groups event collector unchanged')
with tarfile.open(NEW/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz','r:gz')as t:
    idx=json.loads((NEW/'COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json').read_bytes());rows={r['relative_path']:r for r in idx['members']};members=t.getmembers();check(len(members)==len(rows)==1365,'whole original1365 compile Source tar membership')
    for m in members:
        raw=t.extractfile(m).read();r=rows[m.name]['full_original_Source_pin']
        if len(raw)!=r['size_bytes']or hashlib.sha256(raw).hexdigest()!=r['sha256']:raise ValueError('archive Source mismatch '+m.name)
    check(True,'complete1365 Source member EOF SHA bytes and gzip CRC reached')
    names=['Dragon/src/LIBINP.f','Dragon/src/LIBNRG.F','Ganlib/src/REDGET.f90','Ganlib/src/redget_c.c','Ganlib/src/xsm_c.c','Ganlib/src/kdi_c.c','Ganlib/src/kdi.h']
    folder=source_evidence/'ACTUAL_ORIGINAL_LIBRARY_FILENAME_SOURCE';folder.mkdir()
    for name in names:(folder/Path(name).name).write_bytes(t.extractfile(name).read())
check({str(q.relative_to(OLD)):fullpin(q)for q in sorted(OLD.rglob('*'))if q.is_file()}==before,'whole original N5 before after exact7ID and EOF unchanged')
dump(NEW/'COMPLETE_N6_FOUR_ROLE_WHOLE_BYTE_AST_SOURCE_INVERSE.json',dict(schema='COMPLETE_N6_FOUR_ROLE_WHOLE_SOURCE_INVERSE_V1',source_only=True,coordinate_convention='zero-based half-open complete original/derived lines',roles=inverse,definition_proof=definitions,all_other_N5_members_exact_bytes=True))
namespaces=json.loads((OLD/'N5_FUTURE_ROOT_NAMESPACE_AND_SOURCE_ADMISSION_CONTRACT.UNREADY.json').read_bytes())['required_new_v5_namespaces'];namespaces={k:v.replace('-v5-','-v6-').replace('_v5_','_v6_')for k,v in namespaces.items()}
dump(NEW/'N6_FUTURE_ROOT_NAMESPACE_AND_SHARED_LIBRARY_CONTRACT.UNREADY.json',dict(source_only=True,status='UNREADY_N6_REQUIRES_NEW_INDEPENDENT_SOURCE_REVIEW_ROOT_ADMISSION_REQUEST_AND_BINDING',required_new_v6_namespaces=namespaces,material_input_layout=layout,N5_and_N4_actual_Source_admissions_do_not_admit_N6=True,actual_independent_N6_Source_peer=None,actual_N6_Source_admission=None,actual_N6_Root_Source_admission_terminal=None,actual_N6_request=None,actual_N6_Source_binding=None,actual_N6_runtime_terminal=None,actual_N6_observation_manifest=None,actual_N6_storage_RSS_and_physical_qualification=None,nine_original_caps_unchanged=True,all_original129_plus_current_actual_extra_input_roles_preserved=True,actual_new_input_count_is_actual_request_evidence_not_guessed=True,shared_new_layout_storage_or_RSS_or_science_PASS_created=False,compiler_descendant_RSS_scope_still_not_certified=True,ILIBRARYNAME_filename_Source_metadata_changes_are_saved_not_normalized=True))
(NEW/'N6_ROOT_NEXT_STEPS_SOURCE_ONLY.txt').write_text('N6 is UNREADY Source only. N4/N5 Source admission and runtime evidence cannot admit it.\n1. Independent review this whole manifest/14 actual role pins and complete four-role inverse; retain true Source review/seal/postseal.\n2. Root stdlib Source admission must read this N6 manifest and that exact independent review, use actual 14 role pins, original CAPS/FUTURE, and new v6 E.\n3. Root runs Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py with actual peer/admission/typed CLOSED0 admission receipt, exact original six canonical tools, and all five required_new_v6_namespaces. Original129 cannot refresh; original2 libraries hash full EOF for actual pins. New material_input_layout is explicit. No native action in this step.\n4. Root runs bind_complete_observation_SOURCE_only.UNREADY.py --source-manifest-sha256 <actual N6 MF> --request <actual new request> --request-sha256 <actual new SHA> --output-source-dir <v6 D>. Source binding only; all native/RSS/science pins None.\n5. Independent actual bound Source review; Root freezes complete D/E. Run Root_bound_complete_observation_genuine_host.py once with original one-thread env/SPOT_AXMAT_OBSERVATION=ADMITTED_SOURCE_ONLY/required monitor access, serial after other numerical jobs. Whole original four libraries plus link, original caps, A closure before B. Shared libraries copied once; all seven seed roles in each state and original c2m retained. Actual full EOF7IDs of original/shared libraries at A before/after and B before/after, no open shared/state handles at each closure.\n6. After actual Root typed CLOSED, save true raw terminal first in H before E freeze. Then Root_observation_postclose_META_writer.UNREADY.py with exact Root terminal/result/binding pins and fresh E output. Preserves complete H/O/C/D/E views, E own append, strict all actual Source/objects/ar/link/deck/procedure/sharedlibs/event/outputs. Nonzero is honest failure, zero never certifies native bits/aggregation/physics.\nShared layout is a plan, not actual storage/RSS measurement: 2GiB remains hard. Expected new native products/snapshots/archive sizes are unknown. No cleanup or payload omission is authorized.\n')
shutil.copy2(Path(__file__),NEW/'AUTHOR_EXECUTED_N6_SOURCE_ONLY.py')
dump(NEW/'AUTHOR_N6_SOURCE_ONLY_REPORT.json',dict(schema='AUTHOR_N6_COMPLETE_SHARED_ORIGINAL_LIBRARIES_SOURCE_REVIEW_V1',status='SOURCE_ONLY_AUTHOR_PASS_UNREADY_NOT_INDEPENDENT_OR_RUNTIME_OR_SCIENCE',source_only=True,all_checks_typed_true=True,check_count=len(CHECKS),checks=CHECKS,blockers=[],actual_parent_N5_manifest_pin=before['MANIFEST.json'],qualified_role_Source_pins={k:fullpin(NEW/v)for k,v in roles.items()},whole_original_compile_Source_count=1365,changed_roles=changed,definition_proof=definitions,actual_candidate_or_guard_or_API_or_native_or_material_executed=False,actual_storage_or_RSS_or_physical_qualification=False,actual_independent_Source_review=None,actual_Root_Source_admission=None,actual_runtime_terminal=None,actual_scientific_qualification=None,remaining_actual_unknowns=['complete actual own RSS512/storage2GiB/five group600/whole1800 may honestly fail','complete observer snapshots/new native product sizes','new actual native walker controls and complete oldcontext aggregation','Source-binary actual linkage/physical neutron balance/AAA7of8/ABA not started'] ))
dump(NEW/'PREVIOUS_N5_ACTUAL_FULL_EOF_MEMBER_PINS_AND_UNCHANGED_RETENTION.json',dict(source_only=True,parent_manifest_pin=before['MANIFEST.json'],whole_parent_before_after_pin_map=before,all_parent_files_immutable=True,changed_roles=changed))
print(json.dumps(dict(status='AUTHOR_COMPLETE_N6_SOURCE_ONLY_CHECK_CLOSED_NOT_BUSINESS',source_only=True,package=str(NEW),author_review_pin=fullpin(NEW/'AUTHOR_N6_SOURCE_ONLY_REPORT.json'),complete_inverse_pin=fullpin(NEW/'COMPLETE_N6_FOUR_ROLE_WHOLE_BYTE_AST_SOURCE_INVERSE.json'),check_count=len(CHECKS),runtime_pin=fullpin(NEW/changed[0]),actual_candidate_or_guard_API_or_native_or_material_execution=False),allow_nan=False))
