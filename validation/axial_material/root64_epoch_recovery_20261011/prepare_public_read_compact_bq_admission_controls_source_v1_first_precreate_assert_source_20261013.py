#!/usr/bin/env python3
"""Writes an exclusive Source-only public READ control package; runs no child."""
import base64
import difflib
import hashlib
import json
import os
from pathlib import Path
import stat

REC = Path(__file__).resolve().parent
PACKAGE = REC / 'public_read_compact_bq_admission_controls_source_v1_20261013'
MOTHER = REC / 'root64_connected17_compile_namespace_repair_v3/test_ROOT64_full_connected17_namespace_repair_v3.f90'
CANDIDATE = REC / 'bq64_compact_expected_composed_source_draft_v1_20261013'


def ids(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def read_pin(path):
    p=Path(path);before=p.lstat()
    assert stat.S_ISREG(before.st_mode) and not p.is_symlink()
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        assert ids(os.fstat(fd))==ids(before)
        pieces=[]
        while True:
            b=os.read(fd,1048576)
            if not b:break
            pieces.append(b)
        data=b''.join(pieces)
        assert len(data)==before.st_size and ids(os.fstat(fd))==ids(before)
    finally:os.close(fd)
    assert ids(p.lstat())==ids(before)
    return data,dict(path=str(p),sha256=hashlib.sha256(data).hexdigest(),size_bytes=len(data),identity=ids(before))


def put(name,data):
    path=PACKAGE/name;raw=data.encode() if isinstance(data,str) else data
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    try:
        assert os.write(fd,raw)==len(raw)
        os.fsync(fd)
    finally:os.close(fd)
    actual,pin=read_pin(path);assert actual==raw and pin['identity'][3]==1
    return pin


def jput(name,data):
    return put(name,json.dumps(data,indent=2,ensure_ascii=False)+'\n')


EXTRA_ROUTINES = '''  ! Seven controls call the genuine public entry through the unchanged
  ! current factory read_q helper. The private matcher is never a test oracle.
  subroutine run_public_read_admission(name,narg)
    character(len=*),intent(in) :: name
    integer,intent(in) :: narg
    character(len=40),parameter :: names(7)=[character(len=40) :: &
        'public_read_positive_all3','public_read_GLOBAL64_lowbit', &
        'public_read_SEED_lowbit','public_read_GLOBAL64_extra_inventory', &
        'public_read_SEED_extra_inventory','public_read_stale_BQ_SRC', &
        'public_read_stale_BQ_MAC']
    character(len=40) :: control_phase
    character(len=11) :: stale_name,other_name
    type(connected_fixture) :: f
    type(c_ptr) :: auth,child,list,bundle,stale
    real(real64),allocatable :: q(:,:)
    real(real64) :: rho,expected_rho,value,values(NU)
    integer :: which,p,g,rs,before_reads,control_reads,base_reads
    logical :: exists,other_exists
    which=0
    do p=1,size(names)
      if(name==names(p))which=p
    enddo
    call insist(which>0,'one exact public READ admission case')
    control_phase='single'
    if(which>=6)then
      call insist(narg==2,'stale control needs prepare/read phase')
      call get_command_argument(2,control_phase)
      call insist(control_phase=='prepare'.or.control_phase=='read','exact stale prepare/read phase')
      if(which==6)then
        stale_name='BQ64-SRC-ST';other_name='BQ64-MAC-ST'
      else
        stale_name='BQ64-MAC-ST';other_name='BQ64-SRC-ST'
      endif
      inquire(file=other_name,exist=other_exists)
      call insist(.not.other_exists,'other private stage absent before stale control')
      if(control_phase=='prepare')then
        inquire(file=stale_name,exist=exists)
        call insist(.not.exists,'stale sentinel must be newly owned')
        inquire(file='coherent_complete_context.xsm',exist=exists)
        call insist(.not.exists,'persisted fixture must be fresh')
        call build_connected(f,.false.)
        call export_and_readback(f,.false.)
        call insist(actual_q_read_calls==6,'six actual baseline public reads before stale creation')
        call close_connected(f)
        stale=c_null_ptr
        call LCMOP(stale,stale_name,0,2,0)
        call LCMPUT(stale,'SENTINEL',4,1,[17,370,6,1])
        call LCMPTC(stale,'CASE',40,name)
        call LCMCL(stale,1)
        ! No public READ is called after the sentinel is created in this phase.
        control_reads=0;base_reads=actual_q_read_calls;rs=0
      else
        inquire(file=stale_name,exist=exists)
        call insist(exists,'Host-pinned stale sentinel required')
        inquire(file='coherent_complete_context.xsm',exist=exists)
        call insist(exists,'Host-pinned persisted full fixture required')
        ! The second process only opens existing authority read-only. It never
        ! rebuilds a baseline while the stale file is present.
        bundle=c_null_ptr
        call LCMOP(bundle,'coherent_complete_context.xsm',2,2,0)
        call public_read_load_saved_fixture(bundle,f)
        call insist(actual_q_read_calls==0,'no factory baseline reads in stale read phase')
        before_reads=actual_q_read_calls
        call read_q(f,1,q,rho,rs)
        call insist(actual_q_read_calls==before_reads+1,'genuine public READ called once after owning Native gate')
        call insist(rs==SPOR64_BOOTQ64_PREFLIGHT_FAILED,'genuine public READ refuses preexisting private stage')
        call insist(.not.allocated(q),'stale refusal returns no REAL64 array')
        call insist(same64([rho],[0.0_real64]),'stale refusal returns unchanged positive-zero rho')
        call LCMCL(bundle,1)
        ! Never close/delete daughter pointers of the read-only owning bundle.
        control_reads=1;base_reads=0
      endif
      inquire(file=stale_name,exist=exists)
      inquire(file=other_name,exist=other_exists)
      call insist(exists.and..not.other_exists,'stale retained;other stage never created')
    else
      call insist(narg==1,'non-stale public READ controls have exactly one argument')
      inquire(file='BQ64-SRC-ST',exist=exists)
      inquire(file='BQ64-MAC-ST',exist=other_exists)
      call insist(.not.exists.and..not.other_exists,'fresh private stage names before valid factory')
      call build_connected(f,.false.)
      call insist(actual_q_read_calls==3,'three genuine baseline public READ calls')
      base_reads=actual_q_read_calls;before_reads=actual_q_read_calls
      if(which==1)then
        do p=1,NP
          call read_q(f,p,q,rho,rs)
          call insist(rs==SPOR64_BOOTQ64_LOADED.and.allocated(q),'genuine all3 public READ positive')
          call insist(all(shape(q)==[NU,NG]),'positive all370 complete REAL64 shape')
          list=LCMGID(f%sources(p),'ROOT-QFISS64')
          do g=1,NG
            call LCMGDL(list,g,values)
            call insist(same64(q(:,g),values),'all370 complete public q raw words match independent stored oracle')
          enddo
          auth=LCMGID(f%sources(p),'SPOT-R64');call LCMGET(auth,'RHO',expected_rho)
          call insist(same64([rho],[expected_rho]),'public rho raw bits equal independent stored oracle')
          deallocate(q)
        enddo
        call insist(actual_q_read_calls==before_reads+NP,'exact three direct positive public calls')
        control_reads=NP
      else
        auth=LCMGID(f%sources(1),'SPOT-R64')
        if(which==2.or.which==4)then
          child=LCMGID(auth,'GLOBAL64')
        else
          child=LCMGID(auth,'SEED')
        endif
        select case(which)
        case(2)
          call insist(RECORD_MATCHES(child,'NORM64',1,4),'genuine copied GLOBAL64 scalar metadata')
          call LCMGET(child,'NORM64',value);value=bump64(value)
          call LCMPUT(child,'NORM64',1,4,value)
        case(3)
          call insist(RECORD_MATCHES(child,'ROOT-FLUX64',NG,10),'genuine copied SEED native full list')
          list=LCMGID(child,'ROOT-FLUX64');call LCMGDL(list,NG,values)
          values(1)=bump64(values(1));call LCMPDL(list,NG,NU,4,values)
        case(4,5)
          call LCMPUT(child,'UNKNOWN',1,1,991)
        end select
        call read_q(f,1,q,rho,rs)
        call insist(actual_q_read_calls==before_reads+1,'genuine public READ reached after owning Native gate')
        call insist(rs==SPOR64_BOOTQ64_PREFLIGHT_FAILED,'genuine public READ refuses full authority tamper')
        call insist(.not.allocated(q),'authority refusal has no REAL64 output')
        call insist(same64([rho],[0.0_real64]),'authority refusal preserves positive-zero rho')
        control_reads=1
      endif
      call close_connected(f)
      inquire(file='BQ64-SRC-ST',exist=exists)
      inquire(file='BQ64-MAC-ST',exist=other_exists)
      call insist(.not.exists.and..not.other_exists,'ordinary private stage handles closed/deleted at original boundary')
    endif
    write(output_unit,'(A,I0,A,I0,A,I0,A)') &
        '{"case":"'//trim(name)//'","phase":"'//trim(control_phase)// &
        '","schema":"GENUINE_PUBLIC_READ_COMPACT_BQ_ADMISSION_CONTROL_V1",'// &
        '"actual_public_read_status":',rs,',"actual_control_public_read_calls":',control_reads, &
        ',"actual_baseline_public_read_calls":',base_reads, &
        ',"all_actual_assertions_completed":true,"synthetic_fixture":true,'// &
        '"private_matcher_used_as_assertion_oracle":false,"physics_qualified":false,'// &
        '"reader_qualified":false,"AAA_qualified":false,"ABA_admitted":false}'
    flush(output_unit)
  end subroutine run_public_read_admission

  subroutine public_read_load_saved_fixture(bundle,saved)
    type(c_ptr),intent(in) :: bundle
    type(connected_fixture),intent(out) :: saved
    type(c_ptr) :: list
    integer :: p
    saved%radial%flux=LCMGID(bundle,'NATIVE')
    saved%radial%track=LCMGID(bundle,'TRACK')
    saved%radial%system=LCMGID(bundle,'SYSTEM')
    saved%radial%material=LCMGID(bundle,'MATERIAL')
    saved%radial%route=LCMGID(bundle,'RCON')
    saved%ax=LCMGID(bundle,'AX');saved%axtrack=LCMGID(bundle,'AXTRACK')
    saved%axsystem=LCMGID(bundle,'AXSYSTEM');saved%axmacro=LCMGID(bundle,'AXMACRO')
    saved%archive=LCMGID(bundle,'ARCHIVE');saved%global=LCMGID(bundle,'GLOBAL64')
    saved%projected=LCMGID(bundle,'PROJECTED')
    list=LCMGID(bundle,'MACROS')
    do p=1,NP
      saved%macros(p)=LCMGIL(list,p)
    enddo
    list=LCMGID(bundle,'SOURCES')
    do p=1,NP
      saved%sources(p)=LCMGIL(list,p)
    enddo
  end subroutine public_read_load_saved_fixture

'''


def main():
    original,motherpin=read_pin(MOTHER)
    assert motherpin['sha256']=='1b782030e20d4a254052937fd37ff6ef0e145969604e6ef6d365957ea29a9af3'
    sfbytes,sfpin=read_pin(CANDIDATE/'COMPLETE_BQ64_COMPACT_EXPECTED_COMPOSED_SOURCE_FREEZE.json')
    sf=json.loads(sfbytes)
    assert sfpin['sha256']=='3fdfdeb7618485ccd9f7376c29905d38bd9010c25137379c57f6b0d7481de2e3'
    assert sf['source_only'] is True and sf['compiled'] is False and sf['numerical_executed'] is False
    planbytes,oldplanpin=read_pin(CANDIDATE/'PUBLIC_READ_ADMISSION_CONTROL_PLAN_V2.json')
    oldplan=json.loads(planbytes)
    assert oldplan['actual_current_expected_three_planes_namespace_repaired_factory_pin']==motherpin
    old=original.decode();new=old;splices=[]
    def splice(before,after):
        nonlocal new
        assert new.count(before)==1
        new=new.replace(before,after,1);splices.append((before,after))
    splice('program test_ROOT64_full_connected17_v2\n',
           'program test_public_read_compact_bq_admission_v1\n')
    anchor='  call get_command_argument(1,selected_case)\n'
    splice(anchor,anchor+'''  if(index(trim(selected_case),'public_read_')==1)then
    call run_public_read_admission(trim(selected_case),narg)
    stop
  endif
''')
    splice('contains\n\n  subroutine build_connected(',
           'contains\n\n'+EXTRA_ROUTINES+'  subroutine build_connected(')
    splice('end program test_ROOT64_full_connected17_v2\n',
           'end program test_public_read_compact_bq_admission_v1\n')
    inverse=new
    for before,after in reversed(splices):
        assert inverse.count(after)==1
        inverse=inverse.replace(after,before,1)
    assert inverse.encode()==original
    old_helpers=old[old.index('  subroutine build_connected('):old.index('end program test_ROOT64_full_connected17_v2')]
    assert old_helpers in new
    assert max(map(len,new.splitlines()))<=132
    # The load block is the exact existing persisted read-back pointer sequence.
    start='    saved%radial%flux=LCMGID(bundle,\'NATIVE\')\n'
    finish="    enddo\n    call assert_connected(saved)"
    old_loader=old[old.index(start):old.index(finish,old.index(start))+len('    enddo\n')]
    assert old_loader in EXTRA_ROUTINES
    PACKAGE.mkdir(exist_ok=False)
    sourcepin=put('test_public_read_compact_bq_admission_v1.f90',new)
    diffpin=put('CURRENT_FACTORY_TO_PUBLIC_READ_CONTROL_SOURCE.diff',''.join(difflib.unified_diff(
        old.splitlines(True),new.splitlines(True),fromfile=str(MOTHER),tofile=sourcepin['path'])))
    inversepin=jput('COMPLETE_CURRENT_FACTORY_TO_PUBLIC_READ_CONTROL_WHOLE_BYTE_INVERSE.json',{
        'schema':'PUBLIC_READ_CONTROL_CURRENT_FACTORY_COMPLETE_WHOLE_BYTE_INVERSE_V1',
        'original_current_factory_source_pin':motherpin,'new_control_source_pin':sourcepin,
        'literal_splices':[{'before':a,'after':b}for a,b in splices],
        'whole_byte_inverse_observed':True,'restored_sha256':motherpin['sha256'],
        'entire_original_factory_and_math_helpers_contiguous_bytes_retained':True,
        'original17_case_array_dispatch_case_routines_oracles_bytes_retained':True,
        'persisted_fixture_pointer_loader_original_block_whole_bytes_identical':True,
        'new_control_routines_private_to_standalone_program':True,
        'compiled':False,'numerical_executed':False})
    cases=oldplan['cases']
    phases=[{'case':c['name'],'phase':phase,'expected_actual_public_read_status':
                0 if phase=='prepare' else c['expected_public_read_status'],
             'expected_actual_control_public_read_calls':
                0 if phase=='prepare' else 3 if c['name']=='public_read_positive_all3' else 1,
             'expected_actual_baseline_public_read_calls':
                6 if phase=='prepare' else 0 if phase=='read' else 3}
            for c in cases for phase in (['prepare','read']if'stale_name'in c else['single'])]
    planpin=jput('EXACT_GENUINE_PUBLIC_READ_SEVEN_CASE_NINE_PHASE_CONTROL_PLAN.json',{
        'schema':'EXACT_GENUINE_PUBLIC_READ_COMPACT_BQ_ADMISSION_CONTROL_SOURCE_PLAN_V1',
        'source_only':True,'compiled':False,'numerical_executed':False,
        'new_control_source_pin':sourcepin,'current_actual_factory_source_pin':motherpin,
        'candidate_fortran_source_freeze_pin':sfpin,'selected_source_admission_plan_pin':oldplanpin,
        'source_byte_inverse_pin':inversepin,'logical_control_count':7,'actual_run_phase_count':9,
        'cases':cases,'planned_phase_oracles':phases,
        'exact_stale_between_phase_host_contract':{
            'prepare_child_closed0_and_original_guard_watch_required':True,
            'before_manifest_observed_fullEOF_and_all7_after_prepare':
                ['coherent_complete_context.xsm','exact selected BQ64-SRC-ST or BQ64-MAC-ST'],
            'both_selected_files_regular_single_link_no_symlink_required':True,
            'other_BQ_stage_must_be_absent_before_and_after':True,
            'read_phase_before_inputs_exact_same_fullEOF_SHA_all7_required':True,
            'read_child_closed0_and_original_guard_watch_required':True,
            'read_phase_after_selected_two_files_exact_same_fullEOF_SHA_all7_required':True,
            'immutable_host_manifest_fullEOF_SHA_all7_unchanged_required':True,
            'no_delete_or_rebuild_between_phases':True,
            'read_phase_must_call_public_read_exact_once_after_native_gate':True,
            'read_phase_has_no_build_connected_or_assert_connected':True,
            'prepare_creates_stale_only_after_six_genuine_baseline_reads':True},
        'original17_source_and_names_oracles_retained_unchanged':True,
        'private_model_never_assertion_oracle_for_public_READ':True,
        'genuine_new_production_object_required':True,
        'original_nine_core_objects_one_based_slot6_replaced_only':True,
        'old_other_eight_core_and_original_four_archives_exact_required':True,
        'qualification_is_synthetic_protocol_only':True,
        'requires_original17_actual_requalification_plus_these_seven_before_full50':True,
        'original_guards':{'SELF_MiB':512,'child_MiB':512,'stage_s':600,'whole_s':1800,
            'fresh_GiB':2,'free_GiB':8,'history_GiB':96,'aux_MiB':128},
        'future_compile_command':None,'future_link_command':None,
        'future_control_object_pin':None,'future_control_executable_pin':None,
        'future_actual_nine_phase_report_pin':None,'future_stale_host_manifests':None,
        'reader_qualified':False,'physics_qualified':False,'AAA_qualified':False,'ABA_admitted':False})
    authorpin=jput('AUTHOR_SOURCE_ONLY_PUBLIC_READ_CONTROL_BYTE_AUDIT.json',{
        'schema':'PUBLIC_READ_CONTROL_SOURCE_ONLY_COMPLETE_BYTE_AUDIT_V1',
        'status':'PASS_SOURCE_ONLY_BYTE_INVERSE_UNCOMPILED_UNQUALIFIED','failure':None,
        'source_pin':sourcepin,'actual_current_factory_pin':motherpin,
        'whole_inverse_proved':True,'all_original_helpers_math_and_case_oracles_byte_unchanged':True,
        'saved_loader_block_byte_identical':True,'stale_read_no_baseline_rebuild':True,
        'control_count':7,'phase_count':9,'compiled':False,'numerical_executed':False})
    readypin=jput('PUBLIC_READ_CONTROL_SOURCE_REVIEW_READY.json',{
        'schema':'PUBLIC_READ_COMPACT_BQ_CONTROL_SOURCE_REVIEW_READY_V1',
        'source_only':True,'compiled':False,'numerical_executed':False,
        'files':[sourcepin,diffpin,inversepin,planpin,authorpin],
        'original_current_factory_source_pin':motherpin,'candidate_fortran_source_freeze_pin':sfpin,
        'control_plan_pin':planpin,'complete_byte_inverse_pin':inversepin,
        'future_independent_source_review_pin':None,'future_object_pin':None,
        'future_executable_pin':None,'future_actual_control_report_pin':None,
        'reader_qualified':False,'AAA_qualified':False,'ABA_admitted':False})
    assert read_pin(MOTHER)[1]==motherpin and read_pin(CANDIDATE/'COMPLETE_BQ64_COMPACT_EXPECTED_COMPOSED_SOURCE_FREEZE.json')[1]==sfpin
    print(json.dumps({'status':'SOURCE_ONLY_GENUINE_PUBLIC_READ_CONTROL_DRAFT_WRITTEN_UNCOMPILED_UNQUALIFIED',
        'source_review_ready_pin':readypin,'control_source_pin':sourcepin,'complete_byte_inverse_pin':inversepin,
        'control_plan_pin':planpin,'logical_control_count':7,'planned_phases':9,
        'compiled':False,'numerical_executed':False}))


if __name__=='__main__':
    main()
