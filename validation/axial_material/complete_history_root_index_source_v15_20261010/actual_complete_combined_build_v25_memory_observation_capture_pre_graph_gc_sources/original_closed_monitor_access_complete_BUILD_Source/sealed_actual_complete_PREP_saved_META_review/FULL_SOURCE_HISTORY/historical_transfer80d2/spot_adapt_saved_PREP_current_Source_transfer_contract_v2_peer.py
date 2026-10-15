"""Source-only complete historical transfer/current retention contract adapter.
No candidate or saved PREP evidence reviewer is imported or executed here.
"""
import ast,hashlib,json,os,stat
from pathlib import Path
OLD=Path('/private/tmp/axmat_v25_monitor_access_complete_PREP_saved_META_reviewer_UNREADY_20261010')
NEW=Path('/private/tmp/axmat_v25_monitor_access_complete_PREP_saved_META_reviewer_CURRENT_RETAINED_SOURCE_V2_UNREADY_20261010')
ADDITION='''def complete_installation_references(install,freeze,current_D):
    # Transfer-time clone observations are preserved as historical META.
    # Original Source and every retained current file remain full-EOF checked.
    copies=install['complete_enumerable_package_copies']
    need(type(copies) is dict and 'whole_previous_frozen_Source' in copies,'one explicit original complete Source transfer history')
    history=copies['whole_previous_frozen_Source']
    need(type(history) is dict and set(history)=={'original_inventory','complete_file_copies','saved_inventory'},'complete old Source transfer exact inventories and copies')
    old=history['original_inventory'];saved=history['saved_inventory'];rows=history['complete_file_copies']
    oldroot=B/'actual_complete_combined_prepare_v25_sources'
    moved=('combined_prepare_host.py','write_actual_prepare_terminal.py','Root_complete_SOURCE_install_writer.py','Root_complete_PREP_prelaunch.py','Root_actual_complete_SOURCE_install_record.json')
    for inv,root,label in ((old,oldroot,'original'),(saved,D,'historical saved')):
        need(type(inv) is dict and set(inv)=={'root','files','directories','symlinks'} and inv['root']==str(root) and inv['symlinks']=={},label+' exact whole Source transfer inventory')
        need(type(inv['files']) is dict and len(inv['files'])==93 and type(inv['directories']) is dict and len(inv['directories'])==8 and '.' in inv['directories'],label+' complete original93 files and7 child directories')
        for rel,ident in inv['directories'].items():
            need(type(rel) is str and type(ident) is list and len(ident)==7 and all(type(x) is int for x in ident) and stat.S_ISDIR(ident[2]),label+' whole directory7ID '+rel)
    need(type(rows) is dict and set(rows)==set(old['files'])==set(saved['files']) and set(old['directories'])==set(saved['directories']),'all93 Source transfers and full directory domains exactly preserved')
    need(set(moved).issubset(rows),'exact five declared top files have transfer observations')
    current_old=walk(oldroot)
    need(set(current_old['files'])==set(old['files']) and all(exact(current_old['files'][rel],old['files'][rel]) for rel in old['files']) and set(current_old['directories'])==set(old['directories'])-{'.'} and exact(current_old['root_identity'],old['directories']['.']) and all(exact(current_old['directories'][rel],old['directories'][rel]) for rel in current_old['directories']) and current_old['symlinks']=={},'whole original93 Source files and7 directories current EOF7ID unchanged')
    for rel,ident in saved['directories'].items():
        if rel!='.':need(rel in freeze['complete_directories'] and exact(ident,freeze['complete_directories'][rel]),'all7 untouched cloned Source directories match final freeze '+rel)
    for rel,row in rows.items():
        need(type(rel) is str and Path(rel).is_absolute() is False and '..' not in Path(rel).parts and type(row) is dict and set(row)=={'original','saved'},'one exact safe whole Source transfer row '+rel)
        original=supplied(row['original'],'original Source transfer current fullpin '+rel)
        need(original['path']==str(oldroot/rel) and exact(original,old['files'][rel]),'original Source row matches complete original inventory '+rel)
        historical=row['saved']
        need(type(historical) is dict and set(historical)=={'path','sha256','size_bytes','identity'} and historical['path']==str(D/rel),'historical cloned Source exact four-field declared path '+rel)
        hi=historical['identity']
        need(type(hi) is list and len(hi)==7 and all(type(x) is int for x in hi) and stat.S_ISREG(hi[2]) and hi[3]==1 and type(historical['size_bytes']) is int and historical['size_bytes']==hi[4],'historical cloned Source complete typed size7ID '+rel)
        need(type(historical['sha256']) is str and historical['sha256']==original['sha256'] and historical['size_bytes']==original['size_bytes'] and exact(historical,saved['files'][rel]),'historical transfer whole SHA and size match complete original '+rel)
        retained_rel='original_closed_failed_v25_top_sources/'+rel if rel in moved else rel
        need(retained_rel in freeze['complete_files'] and retained_rel in current_D['files'],'every original complete Source currently retained in final freeze '+rel)
        current=supplied(freeze['complete_files'][retained_rel],'retained current complete Source '+rel)
        need(current['path']==str(D/retained_rel) and exact(current,current_D['files'][retained_rel]),'retained Source current full EOF SHA7ID exact final namespace '+rel)
        need(current['sha256']==original['sha256'] and current['size_bytes']==original['size_bytes'],'every retained complete Source no truncation or byte change '+rel)
        if rel in moved:
            need(exact(current['identity'][:6],hi[:6]) and current['identity'][6]>hi[6],'explicit five-file rename preserves inode mode links bytes mtime and records actual ctime update '+rel)
        else:need(exact(current,historical),'all88 untouched saved Source transfer pins remain current '+rel)
    # Every other proof is a current reference and keeps the original full
    # recursive validation. No historical subtree is silently discarded.
    for key,value in install.items():
        if key=='complete_enumerable_package_copies':
            for name,record in copies.items():
                if name!='whole_previous_frozen_Source':references(record,'complete current Source installation proof '+name)
        else:references(value,'complete unchanged Source installation proof '+key)


'''
def ids(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 i=ids(p);assert stat.S_ISREG(i[2]) and i[3]==1
 with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 assert ids(p)==i;return dict(path=str(p),sha256=h,size_bytes=i[4],identity=i)
def segment(s,n):return ''.join(s.splitlines(keepends=True)[n.lineno-1:n.end_lineno])
def write(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n')
p=OLD/'review_actual_complete_PREP_saved_META_stdlib.py';op=pin(p)
assert op['sha256']=='e42751c558903972e5530685d3a93f2ab231b8b2feb624c59ec5eb642a0efb0f'
old=p.read_text();anchor='def terminal(doc,label,wanted=None):';before="    references(install,'complete unchanged Source installation proofs')\n";after="    complete_installation_references(install,freeze,observed[str(D)])\n"
assert old.count(anchor)==1 and old.count(before)==1
new=old.replace(anchor,ADDITION+anchor,1).replace(before,after,1);nt=ast.parse(new);ot=ast.parse(old)
assert new.count(ADDITION)==1 and new.count(after)==1
inverse=new.replace(after,before,1).replace(ADDITION,'',1)
assert inverse==old and ast.dump(ast.parse(inverse),include_attributes=False)==ast.dump(ot,include_attributes=False)
od={n.name:n for n in ot.body if isinstance(n,ast.FunctionDef)};nd={n.name:n for n in nt.body if isinstance(n,ast.FunctionDef)}
assert len(od)==21 and len(nd)==22 and set(nd)==set(od)|{'complete_installation_references'}
assert all(segment(new,nd[k])==segment(old,v) for k,v in od.items() if k!='review')
assert segment(new,nd['review']).replace(after,before,1)==segment(old,od['review'])
assert all(ast.dump(n,include_attributes=False)==ast.dump(m,include_attributes=False) for n,m in zip([x for x in ot.body if not isinstance(x,ast.FunctionDef)],[x for x in nt.body if not isinstance(x,ast.FunctionDef)]))
at=ast.parse(ADDITION);assert len(at.body)==1 and isinstance(at.body[0],ast.FunctionDef)
assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('exec','eval','compile','__import__') for n in ast.walk(at))
assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('Popen','run','exec_module','unlink','rename','write_bytes','write_text') for n in ast.walk(at))
assert not os.path.lexists(NEW);NEW.mkdir();out=NEW/p.name;out.write_text(new)
(NEW/('original_'+p.name)).write_bytes(p.read_bytes());assert pin(p)==op
for n in ('ACTUAL_PREP_REVIEW_INPUTS.UNREADY.json','seal_actual_complete_PREP_saved_META_review_stdlib.py','SOURCE_ONLY_SEVEN_DIRECTORY_INVERSE.json'):
 beforep=pin(OLD/n);(NEW/n).write_bytes((OLD/n).read_bytes());assert pin(OLD/n)==beforep
(NEW/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
checks=[dict(check=k,passed=True) for k in ('complete_e427_original_Source_full_EOF_unchanged','one_new_stdlib_only_readonly_historical_transfer_validator','only_review_install_references_call_replaced','all20_other_functions_complete_byte_unchanged','review_entire_function_inverse_one_call_only','all_original_globals_schemas_Q_helper_physics_caps_monitoring_credit_logic_unchanged','complete_byte_and_AST_inverse_toe427','all18_futurepins_and_twochunks_and_laterE_None','actual_saved_PREP_reviewer_not_executed')]
c=json.loads((NEW/'ACTUAL_PREP_REVIEW_INPUTS.UNREADY.json').read_bytes());assert c['actual_terminal_chunks']=={'PREP':None,'metadata_writer':None} and c['later_E_files_after_writer_joint_sample'] is None
assert all(c[k] is None for k in c if k.startswith('actual_') and k!='actual_terminal_chunks')
v=dict(schema='INDEPENDENT_V25_SAVED_PREP_COMPLETE_CURRENT_RETAINED_SOURCE_CONTRACT_SOURCE_REVIEW_V1',status='SOURCE_ONLY_CONTRACT_ADAPTED_ACTUAL_SAVED_PREP_REVIEW_NOT_EXECUTED',source_only=True,all_checks_typed_true=True,check_count=len(checks),checks=checks,blockers=[],parent_reviewer_pin=op,derived_reviewer_pin=pin(out),full_parent_copy_pin=pin(NEW/('original_'+p.name)),complete_byte_inverse=True,complete_AST_inverse=True,one_new_helper_full_Source=ADDITION,exact_call_inverse=dict(old_statement=before,new_statement=after),prior_path_only_inverse_pin=pin(NEW/'SOURCE_ONLY_SEVEN_DIRECTORY_INVERSE.json'),all20_other_original_functions_byte_unchanged=True,review_only_one_call_change=True,all18_actualpins_remain_None=True,candidate_helper_API_compiler_native_material_numeric_or_saved_PREP_review_executed=False,actual_saved_PREP_review_terminal=None,actual_PASS_saved_PREP_report=None,whole_INPUT_BUILD_native_or_science_qualified=False)
write(NEW/'COMPLETE_HISTORICAL_TRANSFER_CURRENT_RETENTION_SOURCE_INVERSE.json',v)
print(json.dumps(dict(source_only=True,status=v['status'],reviewer_pin=pin(out),inverse_pin=pin(NEW/'COMPLETE_HISTORICAL_TRANSFER_CURRENT_RETENTION_SOURCE_INVERSE.json'),check_count=len(checks),all_checks_typed_true=True,actual_saved_PREP_review_terminal=None,actual_PASS_saved_PREP_report=None)))
