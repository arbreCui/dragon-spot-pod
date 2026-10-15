import ast,hashlib,json,posixpath,re,stat,tarfile
from pathlib import Path

P=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_E_fullpin_same_sort_finite_UNREADY_Source_fix_pb5gkdac')
OUT=Path(__file__).parent
CHECKS=[];PINS={}
def ck(k,v):
    CHECKS.append(dict(check=k,passed=type(v) is bool and v is True))
def ident(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);i=ident(p)
    if not stat.S_ISREG(i[2]) or p.resolve()!=p:raise ValueError('ordinary Source file')
    with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    if ident(p)!=i:raise ValueError('Source EOF changed')
    q=dict(path=str(p),sha256=h,size_bytes=i[4],identity=i);PINS[str(p)]=q;return q
def read(p):
    first=pin(p);d=json.loads(p.read_bytes())
    if pin(p)!=first:raise ValueError('Source META changed')
    return d
def expand(s,values):
    for unused in range(30):
        old=s
        s=re.sub(r'\$\(([A-Za-z_][A-Za-z_0-9]*)\)',lambda m:values.get(m[1],''),s)
        def functional(m):
            kind,args=m[1],m[2];a,b=args.split(',',1)
            if kind=='filter':return ' '.join(x for x in b.split() if x in a.split())
            return a if a in b else ''
        s=re.sub(r'\$\((filter|findstring) ([^()]*)\)',functional,s)
        if s==old:return s
    raise ValueError('Source make expansion depth')
def condition(line,values):
    op,body=line.split(None,1);body=body.strip()
    if not(body.startswith('(') and body.endswith(')')):raise ValueError('unexpected Source make conditional')
    body=body[1:-1];depth=0;split=None
    for i,c in enumerate(body):
        depth+=(c=='(')-(c==')')
        if c==',' and depth==0:split=i;break
    if split is None:raise ValueError('Source make conditional comma')
    a,b=expand(body[:split],values),expand(body[split+1:],values)
    return (a==b) if op=='ifeq' else (a!=b)
def make_selected(text):
    values=dict(ARCH='arm64',OS='Darwin',DIRNAME='Darwin_arm64',openmp='0',mpi='0',hdf5='0',intel='0',nvidia='0',llvm='0',MAKEFLAGS='',PY='declared_original_PY_no_shell_executed')
    stack=[];active=True;lines=[];assigns=[]
    for num,line in enumerate(text.splitlines(),1):
        stripped=line.strip()
        if stripped.startswith(('ifeq ','ifneq ')):
            cond=condition(stripped,values) if active else False
            stack.append((active,cond));active=active and cond;continue
        if stripped=='else':
            parent,cond=stack[-1];active=parent and not cond;continue
        if stripped=='endif':
            parent,cond=stack.pop();active=parent;continue
        if not active:continue
        lines.append((num,line))
        m=re.match(r'^\s*([A-Za-z_][A-Za-z_0-9]*)\s*(\+=|:=|=)\s*(.*)$',line)
        if m:
            key,op,value=m.groups()
            if key in ('ARCH','OS','DIRNAME','PY') or '$(shell' in value:continue
            value=expand(value,values).strip()
            values[key]=(values.get(key,'')+' '+value).strip() if op=='+=' else value
            assigns.append(dict(line=num,key=key,operation=op,selected_value=values[key]))
    if stack:raise ValueError('unbalanced Source Makefile conditional')
    return values,lines,assigns
def astglobals(text):
    return {n.targets[0].id:n.value for n in ast.parse(text).body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
def defs(text):
    return {n.name:ast.get_source_segment(text,n) for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
def main():
    errors=[];evidence={}
    try:
        mf=read(P/'MANIFEST.json');mfp=pin(P/'MANIFEST.json');ck('N3_exact_requested_manifest_SHA',mfp['sha256']=='5313b65cc109d93816137f8c53e6cdcfbf6d5044310762ac65a20a2f76330593')
        members={r['relative_path']:r['fullpin'] for r in mf['members']}
        ck('complete_N3_Source_file_set',{str(x.relative_to(P)) for x in P.rglob('*') if x.is_file()}==set(members)|{'MANIFEST.json'})
        for rel,w in members.items():ck('complete_N3_member_full_EOF_SHA7ID.'+rel,pin(P/rel)==w)
        for rel,w in mf['complete_directory_identity'].items():ck('complete_N3_directory7ID.'+rel,ident(P/rel)==w)
        index=read(P/'COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json');rows={r['relative_path']:r for r in index['members']};ck('complete1365_index_unique',len(rows)==len(index['members'])==1365)
        archive=pin(P/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz');raws={};member_pins={}
        with tarfile.open(archive['path'],'r:gz') as tar:
            allmembers=tar.getmembers();ck('complete_archive1365_name_set',len(allmembers)==1365 and {r.name for r in allmembers}==set(rows))
            for m in allmembers:
                if not m.isfile():raise ValueError('unexpected Source tar nonregular member')
                stream=tar.extractfile(m);raw=stream.read();stream.close();sha=hashlib.sha256(raw).hexdigest();wanted=rows[m.name]['full_original_Source_pin']
                ck('Source_archive_member_EOF_SHA_size.'+m.name,len(raw)==wanted['size_bytes']==m.size and sha==wanted['sha256'])
                member_pins[m.name]=dict(archive_fullpin=archive,member_name=m.name,size_bytes=len(raw),sha256=sha)
                if m.name.endswith('Makefile') or m.name in ('Dragon/src/LIBMIX.f','Dragon/src/LIBDEN.f','Dragon/src/TONDRV.f','Dragon/src/TONSPH.f'):raws[m.name]=raw
        runtime=(P/'complete_observation_BUILD5_AB_runtime.UNREADY.py').read_text();rg=astglobals(runtime);recipes=ast.literal_eval(rg['ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES']);ck('four_recipe_order',list(recipes)==['Ganlib','Utilib','Trivac','Dragon'])
        selected={};makefiles={}
        for c,recipe in recipes.items():
            name=c+'/src/Makefile';text=raws[name].decode();vars,lines,assigns=make_selected(text)
            actual={k:vars.get(k,'').split() for k in ['CFLAGS','FLAGS','FFLAGS','FFLAG77','INCLUDE','FMPI','opt','COMP','LFLAGS']}
            actual.update(C='c' if vars.get('C')=='gcc' else None,F90='fortran' if vars.get('F90')=='gfortran' else None,PREPRO='cpp' if vars.get('PREPRO')=='cpp' else None,lib_module=posixpath.normpath(c+'/src/'+vars['lib_module']) if vars.get('lib_module') else None)
            copies=[dict(line=n,text=s) for n,s in lines if s.startswith('\t') and 'cp *.mod $(lib_module)' in s]
            actual['module_copy']=bool(copies)
            ck('selected_original_Makefile_recipe_exact.'+c,actual==recipe)
            archives=[dict(line=n,text=s) for n,s in lines if s.strip()=='ar rcs $@ $(OBJC) $(OBJ90) $(OBJ77) $(OBJF77)']
            ck('selected_original_ar_object_suffix_group_order.'+c,len(archives)==1)
            selected[c]=dict(recipe=actual,selected_original_variable_assignments=assigns,actual_selected_ar_lines=archives,actual_selected_module_copy_lines=copies,source_suffix_counts={s:sum(k.startswith(c+'/src/') and Path(k).suffix==s for k in rows) for s in ['.c','.f90','.F90','.f','.F']})
            out=OUT/(c+'_original_Makefile.byte_exact.txt');out.write_bytes(raws[name]);makefiles[c]=dict(archive_member_pin=member_pins[name],saved_Makefile_Source_pin=pin(out))
        ck('runtime_original_ar_order_formula',"objects_order=[p.with_suffix('.o')for p in [*c,*ordered90,*f77]]" in runtime and "f77=[*f77_lower,*f77_upper]" in runtime)
        ck('runtime_original_ar_rcs_and_objects_order',"argv=[tools['ar']['path'],'rcs',str(archive),*map(str,objects_order)]" in runtime)
        ck('runtime_original_separate_module_copy_namespaces',"modules=native/recipe['lib_module']" in runtime and "if recipe['module_copy']:" in runtime)
        ck('runtime_original_fixed_Ganlib_include',recipes['Trivac']['INCLUDE']==recipes['Dragon']['INCLUDE']==['-I../../Ganlib/lib/Darwin_arm64/modules/'] and recipes['Ganlib']['INCLUDE']==recipes['Utilib']['INCLUDE']==[])
        phys=read(P/'COMPLETE_FOUR_ORIGINAL_PHYSICAL_ROUTINE_OBSERVER_INSERT_ONLY_INVERSE.json');count=0
        for row in phys['derivations']:
            original=raws[row['original_archive_member']];derived=(P/row['derived_Source_member']).read_bytes();lines=derived.decode().splitlines(keepends=True)
            ck('physical_source_original_archive_SHA.'+row['original_archive_member'],hashlib.sha256(original).hexdigest()==row['original_sha256'])
            ck('physical_source_derived_SHA.'+row['derived_Source_member'],hashlib.sha256(derived).hexdigest()==row['derived_sha256'])
            for h in reversed(row['complete_insert_only_hunks']):
                ck('physical_insert_only.'+row['derived_Source_member']+'.'+str(h['new_start0']),h['tag']=='insert' and h['old_start0']==h['old_end0'] and h['old_full_lines']==[] and lines[h['new_start0']:h['new_end0']]==h['new_full_lines'])
                lines[h['new_start0']:h['new_end0']]=[];count+=1
            ck('physical_full_byte_inverse.'+row['derived_Source_member'],''.join(lines).encode()==original)
        ck('complete_four_physical_routines14_insertions',len(phys['derivations'])==4 and count==14)
        hi=read(P/'COMPLETE_ORIGINAL_NATIVE_HOST_TO_OBSERVATION_HOST_FULL_INVERSE.json');parent=(P/'PARENT_SOURCE/Root_bound_complete_native_genuine_host.py').read_text();host=(P/'complete_observation_genuine_host.UNREADY.py').read_text();lines=parent.splitlines(keepends=True)
        ck('host_original_full_Source_SHA',hashlib.sha256(parent.encode()).hexdigest()==hi['original_Source_sha256'])
        for i,h in enumerate(reversed(hi['complete_full_inverse_hunks'])):
            ck('host_whole_original_hunk.'+str(i),lines[h['old_start0']:h['old_end0']]==h['old_full_lines'])
            lines[h['old_start0']:h['old_end0']]=h['new_full_lines']
        ck('host_complete12_hunk_derivation',len(hi['complete_full_inverse_hunks'])==12 and ''.join(lines)==host and hashlib.sha256(host.encode()).hexdigest()==hi['derived_Source_sha256'])
        pd,hd=defs(parent),defs(host)
        for n,v in pd.items():
            if n!='main':ck('host_original_guard_support_definition_exact.'+n,hd.get(n)==v)
        evidence=dict(actual_N3_manifest_pin=mfp,actual_runtime_Source_pin=pin(P/'complete_observation_BUILD5_AB_runtime.UNREADY.py'),actual_native_Source_archive_pin=archive,actual_native_Source_index_pin=pin(P/'COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json'),selected_original_Makefile_recipes=selected,full_actual_archive_makefile_Source_pins=makefiles,physics_inverse_META_pin=pin(P/'COMPLETE_FOUR_ORIGINAL_PHYSICAL_ROUTINE_OBSERVER_INSERT_ONLY_INVERSE.json'),host_inverse_META_pin=pin(P/'COMPLETE_ORIGINAL_NATIVE_HOST_TO_OBSERVATION_HOST_FULL_INVERSE.json'),physics_insert_only_hunks=14,host_full_inverse_hunks=12)
    except Exception as e:ck('review_without_Source_contract_exception',False);errors.append(repr(e))
    for path,w in list(PINS.items()):ck('final_Source_full_EOF_SHA7ID_unchanged.'+path,pin(path)==w)
    blocked=[r for r in CHECKS if not r['passed']]
    result=dict(schema='INDEPENDENT_N3_NATIVE_RECIPE_AND_PHYSICAL_SOURCE_SUPPORT_REVIEW_V1',status='PASS_SOURCE_ONLY' if not blocked else 'BLOCKED_SOURCE_ONLY',source_only=True,all_checks_typed_true=not blocked,blockers=blocked,errors=errors,check_count=len(CHECKS),checks=CHECKS,actual_complete_Source_input_pins=list(PINS.values()),selected_platform=dict(OS='Darwin',ARCH='arm64',openmp=0,mpi=0,hdf5=0,intel=0,nvidia=0,llvm=0),Makefile_or_dependency_generator_executed=False,candidate_guard_API_compiler_material_or_numeric_executed=False,project_modified=False,new_N4_source_read=False,actual_runtime=None,actual_Source_binary_linkage=None,scientific_qualification_created=False,**evidence)
    report=OUT/'REVIEW.json';report.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(status=result['status'],check_count=len(CHECKS),blockers=blocked,errors=errors,report_pin=pin(report),source_only=True)))
if __name__=='__main__':main()
