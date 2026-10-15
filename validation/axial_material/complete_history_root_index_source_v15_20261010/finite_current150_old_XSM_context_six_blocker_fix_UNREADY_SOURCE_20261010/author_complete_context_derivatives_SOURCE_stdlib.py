"""Standard library Source author only. Never import/run/compile candidates."""
import ast,difflib,hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parent;B=P/'COMPLETE_FIXED_PARENT_SOURCE';inverses=[]
def derive(name,old,new):
    if name.endswith('.py'):ast.parse(new)
    a=old.splitlines(keepends=True);b=new.splitlines(keepends=True)
    hunks=[dict(tag=t,old_start0=i,old_end0=j,new_start0=k,new_end0=l,old_full_lines=a[i:j],new_full_lines=b[k:l])
        for t,i,j,k,l in difflib.SequenceMatcher(a=a,b=b,autojunk=False).get_opcodes()if t!='equal']
    back=b[:]
    for x in reversed(hunks):
        assert back[x['new_start0']:x['new_end0']]==x['new_full_lines'];back[x['new_start0']:x['new_end0']]=x['old_full_lines']
    assert ''.join(back)==old
    (P/name).write_text(new)
    inverses.append(dict(candidate=name,original_SHA256=hashlib.sha256(old.encode()).hexdigest(),candidate_SHA256=hashlib.sha256(new.encode()).hexdigest(),
        complete_zero_based_hunks=hunks,all_original_full_Source_bytes_restored=True))
def replace_once(s,a,b):assert s.count(a)==1,(a,s.count(a));return s.replace(a,b)
old=(B/'complete_final_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py').read_text();new=old
fragment=(P/'context_aware_complete_construction_fragment.UNREADY.py').read_text()+'\n'+(P/'context_state_check_fragment.UNREADY.py').read_text()
new=replace_once(new,'def main():',fragment+'\n\ndef main():')
new=replace_once(new,"states.append(state_check(adapter,binding,state,output,budget))","states.append(context_state_check(adapter,binding,state,output,budget))")
new=new.replace('ROOT_ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_BINDING_V1','ROOT_ACTUAL_COMPLETE_CONTEXT_AWARE_MICRO_MACRO_BINDING_V2')
new=replace_once(new,"        historical_context_missing_is_not_silently_supplied=True, **FALSE)",
    "        historical_context_missing_is_not_silently_supplied=True,genuine_supervisor_watch_verified_here=False, **FALSE)")
derive('complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py',old,new)
old=(B/'AXMAT_OBSERVATION_MOD.UNREADY.f90').read_text();new=old
new=replace_once(new,"write(unit) 'AXOBSCTX',1_c_int32_t", "write(unit) 'AXOBSCTX',2_c_int32_t")
new=replace_once(new,'    integer :: unit,state(40),macro_length,macro_kind',
    '    integer :: unit,state(40),macro_length,macro_kind,volume_length,volume_kind\n    real :: actual_root_volume(nbmix)')
new=replace_once(new,"    write(unit) merge(1,0,mask),merge(1,0,maskl)\n    close(unit)\n    call snapshot('oldmacro-pre-LIBMIX',iplib,.false.)",
    "    write(unit) merge(1,0,mask),merge(1,0,maskl)\n    call LCMLEN(iplib,'MIXTURESVOL',volume_length,volume_kind)\n    write(unit) volume_length,volume_kind\n    if(volume_length>0)then\n      if(volume_length/=nbmix.or.volume_kind/=2) &\n        call XABORT('AXOBS: full root volume shape differs; no truncation')\n      call LCMGET(iplib,'MIXTURESVOL',actual_root_volume)\n      write(unit) actual_root_volume\n    endif\n    close(unit)\n    call snapshot('oldmacro-pre-LIBMIX',iplib,.false.)")
new=replace_once(new,'  public :: AXOBS_LIBMIX_END, AXOBS_TRACK, AXOBS_MASK, AXOBS_SPH, AXOBS_FINAL',
    '  public :: AXOBS_LIBMIX_END, AXOBS_TRACK, AXOBS_MASK, AXOBS_SPH, AXOBS_FINAL\n  public :: AXOBS_SPH_DECISION')
routine='''  subroutine AXOBS_SPH_DECISION(nbiso,nbmix,ngro,inrs,nbnrs,nres2,ksph,lshi2)
    integer,intent(in) :: nbiso,nbmix,ngro,inrs,nbnrs,nres2,ksph,lshi2(nbiso)
    integer :: unit
    if(.not.enabled())return
    call start_event('TONDRV_ACTUAL_SPH_CALL_DECISION',unit)
    write(unit) nbiso,nbmix,ngro,inrs,nbnrs,nres2,ksph,lshi2
    close(unit)
  end subroutine

'''
new=replace_once(new,'  subroutine AXOBS_FINAL(iplib)',routine+'  subroutine AXOBS_FINAL(iplib)')
derive('AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90',old,new)
old=(B/'TONDRV.observe.UNREADY.f').read_text();new=replace_once(old,'         IF(NBNRS.GT.1) THEN',
    '         CALL AXOBS_SPH_DECISION(NBISO,NBMIX,NGRO,INRS,\n     >   NBNRS,NRES2,KSPH,LSHI2)\n         IF(NBNRS.GT.1) THEN')
derive('TONDRV.context_observe.UNREADY.f',old,new)
for name in('LIBMIX.observe.UNREADY.f','LIBDEN.observe.UNREADY.f','TONSPH.observe.UNREADY.f','saved_native_data_access_adapter.UNREADY.py'):
    old=(B/name).read_text();derive(name,old,old)
old=(B/'extract_actual_observation_context.UNREADY.py').read_text();new=replace_once(old,"        elif label in ('LIBMIX_AFTER','TONDRV_FINAL_AFTER_SHIBA'):",
    "        elif label=='TONDRV_ACTUAL_SPH_CALL_DECISION':\n            field('NBISO,NBMIX,NGRO,INRS,NBNRS,NRES2,KSPH',7,dimension=True)\n            require(tuple(dimensions[k]for k in('NBISO','NBMIX','NGRO'))==(62,8,370),'complete SPH decision scope')\n            field('LSHI2',62)\n        elif label in ('LIBMIX_AFTER','TONDRV_FINAL_AFTER_SHIBA'):")
new=replace_once(new,'require(version==1 and event>=1','require(version==2 and event>=1')
new=replace_once(new,"            field('MASK',n);field('MASKL',g)",
    "            field('MASK',n);field('MASKL',g)\n            field('MIXTURESVOL_LENGTH,MIXTURESVOL_KIND',2,dimension=True)\n            if dimensions['MIXTURESVOL_LENGTH']>0:\n                require(dimensions['MIXTURESVOL_LENGTH']==8 and dimensions['MIXTURESVOL_KIND']==2,'full observed root volume shape')\n                field('ROOT_MIXTURESVOL_BEFORE',8,'REAL32')")
derive('extract_actual_complete_context_with_SPH_decisions.UNREADY.py',old,new)
(P/'COMPLETE_CONTEXT_AWARE_SOURCE_FULL_INVERSE.json').write_text(json.dumps(dict(schema='COMPLETE_CONTEXT_AWARE_ENGINE_OBSERVER_FULL_SOURCE_INVERSE_V2',source_only=True,
    derivations=inverses,actual_observation=None,actual_old_XSM_extraction=None,actual_aggregation=None,
    actual_new_controls=None,new_qualification=None,compiled_Source_binary_link=None),indent=2)+'\n')
print(json.dumps(dict(source_only=True,all_derivatives=len(inverses),all_hunks=sum(len(x['complete_zero_based_hunks'])for x in inverses),
    no_candidate_native_material_API_guard_compile_execution=True)))
