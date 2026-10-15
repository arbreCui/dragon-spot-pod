import ast, os, stat, json, hashlib, base64, copy
from pathlib import Path
from types import SimpleNamespace

R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
O=R/'independent_two_controlsHost_v3_Source_review_20261013'
cache={};allchecks=[];results=[]
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(p):return {k:p[k]for k in ('path','sha256','size_bytes','identity')}
def pin(path):
    p=Path(path);before=identity(p.lstat())
    if not stat.S_ISREG(before[2]):raise AssertionError('ordinary Source/meta')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb')as f:
        if identity(os.fstat(f.fileno()))!=before:raise AssertionError('open7')
        raw=f.read()
        if identity(os.fstat(f.fileno()))!=before:raise AssertionError('EOF7')
    if identity(p.lstat())!=before:raise AssertionError('after7')
    row=dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before)
    cache[str(p)]=(row,raw);return row,raw
def same(row):
    p=norm(row);a=cache.get(p['path'])or pin(p['path'])
    if a[0]!=p:raise AssertionError('exact Source/meta PF '+p['path'])
    return a[1]
def read(p):
    row,raw=pin(p);return json.loads(raw),row
def require(ok,name):
    if not ok:raise AssertionError(name)
    allchecks.append(name)
def refusal(fn,name):
    try:fn()
    except RuntimeError:allchecks.append(name);return
    raise AssertionError('missing refusal '+name)

specs=[('model','bq64_private_GANLIB_model_control_host_source_v3_20261013','run_guarded_model_controls.py','08763b0d7f675ea230204bb48957ef4fa3f1193e830b8ad22963ca280154efad',24876),('public','public_read_compact_bq_admission_control_host_source_v3_20261013','run_guarded_public_controls.py','de496ab261d6b2b014fa1c94f448d27191af31a773ad4de96fc8c47f05701cda',24940)]
function_dump=None
for kind,dirname,filename,sha,size in specs:
    begin=len(allchecks);D=R/dirname;source,raw=pin(D/filename);text=raw.decode();tree=ast.parse(text)
    require((source['sha256'],source['size_bytes'])==(sha,size),'exact final '+kind+' Host Source SHA/size')
    plan,pp=read(D/'EXACT_CONTROL_HOST_SOURCE_ONLY_PLAN.json')
    require(norm(plan['host_source_pin'])==source and plan['kind']==kind,'own plan exact final Host PF/kind')
    require(plan['source_only']is True and all(plan[k]is False for k in ('compiler_executed','numerical_executed','Host_imported','compile_qualified','reader_qualified','AAA_qualified','ABA_admitted')),'plan Source-only unqualified fields')
    require(all(plan[k]is None for k in ('future_actual_new_build70_report_pin','future_actual_control_object_pin','future_actual_control_executable_pin','future_actual_control_report_pin','future_actual_stale_manifests')),'actual future control/newbuild pins remain None')
    for k in ('selected_control_Source_freeze_pin','control_Source_pin','production_Source_pin','control_plan_pin','selected_new_build_Host_freeze_pin','selected_new_build_Host_source_pin','selected_new_Fortran_Source_freeze_pin','selected_new_build_plan_pin'):same(plan[k])
    hf=json.loads(same(plan['selected_new_build_Host_freeze_pin']));buildplan=json.loads(same(plan['selected_new_build_plan_pin']));sf=json.loads(same(plan['selected_control_Source_freeze_pin']));controlplan=json.loads(same(plan['control_plan_pin']))
    require(len(hf['dependencies'])==2532 and norm(hf['host_source'])==norm(plan['selected_new_build_Host_source_pin']),'selected original buildHF2532 and exact Host Source')
    require(plan['original_ordered70_paths']==[x['path']for x in buildplan['original_ordered70_input_pins']]and plan['original_nine_core_pins']==buildplan['original_nine_core_object_pins'],'original70 / exact original9 preserved in PLAN')
    require(plan['original_nine_core_paths']==[x['path']for x in plan['original_nine_core_pins']]and plan['original_four_archive_paths']==[x for x in plan['original_ordered70_paths']if x.endswith('.a')],'exact9 paths and original4 archives order')
    require(plan['original_caps']==buildplan['original_caps'] and plan['original_compile_flags']==buildplan['original_compile_flags']and plan['original_compile_include_arguments']==buildplan['original_compile_include_arguments'],'original caps/flags/include arrays exact')
    require(plan['direct_auxiliary_cap_bytes']==128*2**20 and plan['pending_metadata_bytes']==8*2**20 and plan['fresh_full2GiB_initial_reservation_required']is True,'direct128MiB pending8MiB plus original fullfresh2')
    require(norm(plan['control_Source_pin']) in [norm(x)for x in sf['files']],'actual control Source in complete selectedSF files')
    require((norm(plan['selected_control_Source_freeze_pin'])if kind=='model'else norm(sf['candidate_fortran_source_freeze_pin']))==norm(plan['selected_new_Fortran_Source_freeze_pin']),'controlSF productionSF equals selected exact candidateSF')
    for x in plan['original_nine_core_pins']:
        require(identity(Path(x['path']).lstat())==x['identity'],'original9 current7 '+x['path'])
    constants={}
    for node in tree.body:
        if isinstance(node,ast.Assign)and len(node.targets)==1 and isinstance(node.targets[0],ast.Name)and isinstance(node.value,ast.Constant):constants[node.targets[0].id]=node.value.value
    require(constants['KIND']==kind and str(Path(plan['planned_output_root']).relative_to('/Users/wen/spot'))in text and 'v3' in plan['planned_output_root'],'Source constants/PLAN unique v3 OUT')
    require(not Path(plan['planned_output_root']).exists() and not Path(plan['planned_output_root']).is_symlink(),'own business OUT absent at Source review')
    require("c.closed_report(base,helper,Path(pbase['path']).parent,2)"in text and "base.get('actual_host_Source_freeze_pin')!=selected_build_hf"in text and "base.get('actual_new_Source_freeze_pin')!=production_sf"in text,'actual closed2 selects exact external buildHF and FortranSF')
    require("hf_table.get(selected['path'])!=selected"in text and "base_fixed_table.get(row['path'])!=row"in text,'ownHF and actualbuild fixed rows bind both selected freezes')
    require("new_object not in base['output_pins']"in text and 'expected_new[40]'in text and "core[5]=new[40]"in text,'actual new BOOTQ PF and70slot40/core6 anchored')
    inv,ip=read(D/'COMPLETE_CONTROL_HOST_V1_TO_V3_WHOLE_BYTE_INVERSE.json');require(norm(inv['new_source_pin'])==source,'wholeinverse exact current Source PF')
    restored=raw
    for b in sorted(inv['blocks'],key=lambda x:x['candidate_offset'],reverse=True):
        start,end=b['candidate_offset'],b['candidate_end'];require(hashlib.sha256(raw[start:end]).hexdigest()==b['candidate_piece_sha256'],'inverse selected complete block bytes')
        restored=restored[:start]+base64.b64decode(b['original_bytes_base64'])+restored[end:]
    require(restored==same(inv['original_source_pin']),'whole v1→v3 inverse restores actual original Source EOF')
    evidence=[]
    for name in ('AUTHOR_EXTRACTED_FUNCTIONS_FINITE_SOURCE_BOUNDARY_REVIEW.json','AUTHOR_DIRECT_AUXILIARY_BOUNDARY_SOURCE_REVIEW.json','HOST_SOURCE_REVIEW_READY.json','ROOT_BUILD_V3_GUARD_PUBLICATION_SOURCE_PROVENANCE.json'):
        _,p=read(D/name);evidence.append(p)
    fns=[x for x in tree.body if isinstance(x,(ast.FunctionDef,ast.ClassDef))]
    dump=[ast.dump(x,include_attributes=False)for x in fns]
    if function_dump is None:function_dump=dump
    else:require(dump==function_dump,'both final Host procedure ASTs identical; only declared constants/docs differ')
    picked=[x for x in fns if x.name in ('safe_repr','FirstFailure','make_commands','public_oracle','model_oracle')]
    ns={'Path':Path,'OUT':Path(plan['planned_output_root']),'KIND':kind,'stat':stat}
    exec(compile(ast.Module(body=picked,type_ignores=[]),'<finite extracted functions only>','exec'),ns)
    ff=ns['FirstFailure']();original=ValueError('independent-original');late=RuntimeError('independent-publication')
    try:raise original
    except BaseException as exc:original_tb=exc.__traceback__;ff.capture(exc,'execute')
    ff.capture(late,'publication')
    require(ff.error is original and ff.traceback is original_tb and len(ff.secondary)==1,'finite first object+original tb survives later publication')
    try:ff.reraise()
    except BaseException as exc:
        chain=[];tb=exc.__traceback__
        while tb:chain.append(tb);tb=tb.tb_next
        require(exc is original and original_tb in chain,'finite reraise preserves exact original object+tb')
    bnew=list(plan['original_ordered70_paths']);bnew[40]=plan['new_build_expected_BOOTQ_object_path'];compiler=plan['original_compiler_pin']['path']
    expectedcompile=[compiler,*plan['original_compile_flags'],*plan['new_build_compile_include_arguments'],'-J'+plan['new_build_expected_build_directory'],'-c',plan['production_Source_pin']['path'],'-o',plan['new_build_expected_BOOTQ_object_path']]
    base=dict(actual_complete70_link_inputs=bnew,records=[dict(command=expectedcompile),dict(command=[compiler,'-O2','-ffp-contract=off',*bnew,'-o',plan['new_build_expected_Dragon_path']])]);common=SimpleNamespace(FLAGS=plan['original_compile_flags'])
    comp,link,exe,core=ns['make_commands'](common,base,plan,plan['control_Source_pin'])
    expectedcore=[]if kind=='model'else list(plan['original_nine_core_paths']);
    if kind=='public':expectedcore[5]=bnew[40]
    require(core==expectedcore and link[4:4+len(core)]==core and link[-6:-2]==plan['original_four_archive_paths'],'finite private only4 archives/public exact9 core6 plus4 archives')
    require(comp[-3]==plan['control_Source_pin']['path']and comp[-1]==str(ns['OUT']/'build/control.o'),'finite control compile exact Source/output')
    for pos,value,name in [(0,'wrongcompiler','compiler'),(1,'-O0','flags'),(-3,'wrongproductionSource','productionSource'),(-1,plan['original_ordered70_paths'][40],'oldoutput')]:
        changed=copy.deepcopy(base);changed['records'][0]['command'][pos]=value
        refusal(lambda:ns['make_commands'](common,changed,plan,plan['control_Source_pin']),'finite compile '+name+' boundary refuses')
    changed=copy.deepcopy(base);changed['actual_complete70_link_inputs'][40]=plan['original_ordered70_paths'][40]
    refusal(lambda:ns['make_commands'](common,changed,plan,plan['control_Source_pin']),'finite oldBOOTQ slot40 refuses')
    changed=copy.deepcopy(base);changed['records'][1]['command'][3:5]=reversed(changed['records'][1]['command'][3:5])
    refusal(lambda:ns['make_commands'](common,changed,plan,plan['control_Source_pin']),'finite reordered70 link refuses')
    require("first.capture(error,'execute_or_oracle')"in text and "first.capture(error,'after_check')"in text and "first.capture(error,'publication')"in text and "first.capture(late,'failed_report_publication')"in text,'first failure covers execute/oracle/after/full publication/failed rewrite')
    publication=next(x for x in ast.walk(tree)if isinstance(x,ast.Try)and any(isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='summary'for t in n.targets)for n in x.body))
    pub=ast.get_source_segment(text,publication)
    require("summary=dict("in pub and "c.write(target,summary)"in pub and "rewrite_summary(c,target,c.pin(target),summary)"in pub and "check()"in pub,'entire summary construction/fullpins/stats/write/finalcheck protected')
    require('first.reraise()'in text and "actual_model_controls_passed=False,actual_seven_genuine_public_READ_controls_passed=False"in pub and "final_report_resource_check_passed=False"in pub,'failed publication demotes successful flags and reraises first failure')
    require("result=self.base.check()"in text and "result['control_direct_auxiliary']=direct_aux_inventory(self.root)"in text and "total+AUX_PENDING>AUX_CAP"in text,'direct separate auxiliary pass preserves original independent resource base')
    require('OUT,1800-(time.monotonic()-start)'in text and 'command,600)'in text and "before['artifact_bytes']+20971764748+64*2**20+2*2**30>=96*2**30"in text,'original stage600/whole1800 includes admission/report; fullfresh2 history96 cold reserve')
    if kind=='model':
        require(plan['planned_total_guarded_stages']==3 and plan['planned_run_phases']==[dict(case='private_GANLIB_model',phase='single',expected_actual_assertions=36,expected_compact_physical_bytes=948232)],'model1 phase/3 stages exact36/948232 plan')
        require("models[0]['size_bytes']!=948232"in text and "actual['assertions']!=36"in text,'actual model36 plus compact physical948232 bounded32MiB')
    else:
        require(plan['planned_run_phases']==controlplan['planned_phase_oracles']and plan['planned_total_guarded_stages']==11 and len(plan['planned_run_phases'])==9,'public genuine7 controls9 phases11 guardedstages exact c991 oracles')
        require("type(observed)is not int"in text and "observed!=value"in text,'all public status/counters actual exact integers reject bool')
        require("c.write(mf,dict(schema='ACTUAL_PUBLIC_READ_STALE_BEFORE_FULL_EOF_SHA_ALL7_V1'"in text and "c.verify_rows([state['manifest_pin'],state['bundle_pin'],state['stale_pin']])"in text,'stale fsynced manifest binds successfulprepare bundle+sentinel all7 before/read/after')
        require("(cwd/other).exists()or(cwd/other).is_symlink()"in text and "actual_two_files_full_EOF_SHA_all7_unchanged=True"in text,'stale actual other absence and file preservation only after successful fullPF verification')
        labels=[d['case']+'/control_'+d['phase']for d in plan['planned_run_phases']]
        require(len(set(labels))==9,'all public phase log paths unique via original executor directory-relative recordlabel')
    require("old17_PASS_inherited=False"in text and "private_model_does_not_independently_qualify_public_reader=True"in text and "physics_qualified=False,new_reader_qualified=False"in text,'source scope model/private controls never become fullreader/physics/AAA qualification')
    for p,_ in list(cache.values()):
        if identity(Path(p['path']).lstat())!=p['identity']:raise AssertionError('final all Source/meta7')
    results.append(dict(schema='INDEPENDENT_COMPACT_BQ_CONTROL_HOST_SOURCE_ONLY_REVIEW_V1',kind=kind,status='PASS_SOURCE_ONLY_UNIMPORTED_UNQUALIFIED',failure=None,source_pin=source,Host_source_pin=source,plan_pin=pp,selected_new_build_Host_freeze_pin=norm(plan['selected_new_build_Host_freeze_pin']),selected_new_Fortran_Source_freeze_pin=norm(plan['selected_new_Fortran_Source_freeze_pin']),whole_byte_inverse_pin=ip,author_evidence_pins=evidence,source_only=True,Host_imported=False,Host_main_executed=False,compiler_executed=False,compiled=False,numerical_executed=False,numeric=False,business_executed=False,finite_AST_functions_only=True,finite_observations_in_memory_not_actual_controls=True,science_EOF_repeated=False,full_active2532_evidence_inherited_from_exact_build_SF_HF_review_and_actual7030_postrelease=True,reader_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,future_actual_new_build70_report_pin=None,future_actual_control_report_pin=None,all_file_descriptors_closed=True,checks=allchecks[begin:]))
for result in results:
    result['direct_runtime_execution_admitted']=False
    result['current_runtime_limitation']='Root actual build admission refused before compiler/child/OUT: unchanged old Common current catalog still selects ten exact released files. This Source-only report reviews retained v3 Host bytes and finite controls; future execution needs independently reviewed postrelease catalog/Common role revision and a genuine successful new closed2 build. No historical release targets were reopened.'
O.mkdir();pins=[]
for result in results:
    p=O/(result['kind']+'_REVIEW.json');p.write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n');pins.append(pin(p)[0])
print(json.dumps(dict(status='PASS_TWO_FINAL_CONTROL_HOSTS_SOURCE_ONLY',failure=None,review_pins=pins,model_source_pin=results[0]['source_pin'],model_plan_pin=results[0]['plan_pin'],public_source_pin=results[1]['source_pin'],public_plan_pin=results[1]['plan_pin'],Host_imported=False,Host_main_executed=False,compiler_executed=False,numerical_executed=False,all_file_descriptors_closed=True),ensure_ascii=False))
