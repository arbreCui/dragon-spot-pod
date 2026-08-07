program PREPARE_B2L_PROJECTED
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use SPOR64_B2C, only : SPOR64_B2C_HOST_COMMITTED, &
      SPOR64_B2C_PUBLISH
  use SPOR64_B2I, only : SPOR64_B2I_BOOTSTRAP_COMMITTED, &
      SPOR64_B2I_SEAL_BOOTSTRAP
  use SPOR64_B2J, only : SPOR64_B2J_ARCHIVE_PROJECTED, &
      SPOR64_B2J_PROJECT_ARCHIVE
  implicit none

  integer, parameter :: NGRP=370
  integer, parameter :: NREG=8
  integer, parameter :: NSNAP=3
  integer, parameter :: NUNKNO=14
  integer, parameter :: NMAT=8
  integer(int32), parameter :: FROZEN_TOL_BITS=int(z'348637bd',int32)

  character(len=1024) :: axial_path, archive_path, track_path, output_path
  integer :: b2c_calls, b2i_calls, b2j_calls, full_copy_items, status
  logical :: output_exists
  type(c_ptr) :: axial_base, archive_base, axial_track_base
  type(c_ptr) :: candidate, axial_closed, archive_closed, projected

  if (command_argument_count() /= 4) error stop &
      'expected AX, archive, axial-track, and projected-output paths'
  call get_command_argument(1,axial_path)
  call get_command_argument(2,archive_path)
  call get_command_argument(3,track_path)
  call get_command_argument(4,output_path)
  inquire(file=trim(output_path),exist=output_exists)
  if (output_exists) error stop 'PROJECTED output path already exists'

  call LCMOP(axial_base,trim(axial_path),2,2,0)
  call LCMOP(archive_base,trim(archive_path),2,2,0)
  call LCMOP(axial_track_base,trim(track_path),2,2,0)
  call REQUIRE_ASSOCIATED(axial_base,'frozen axial state')
  call REQUIRE_ASSOCIATED(archive_base,'frozen plane archive')
  call REQUIRE_ASSOCIATED(axial_track_base,'frozen axial track')

  call BUILD_FULL_CANDIDATE(archive_base,candidate,b2c_calls, &
      full_copy_items)
  call LCMOP(axial_closed,'B2L-AX-CLOSE',0,1,0)
  call LCMOP(archive_closed,'B2L-AR-CLOSE',0,1,0)
  call REQUIRE_ASSOCIATED(axial_closed,'fresh closed AX output')
  call REQUIRE_ASSOCIATED(archive_closed,'fresh closed archive output')

  b2i_calls=1
  call SPOR64_B2I_SEAL_BOOTSTRAP(axial_closed,archive_closed, &
      axial_base,axial_track_base,candidate,status)
  if (status /= SPOR64_B2I_BOOTSTRAP_COMMITTED) &
      error stop 'production B2i rejected the full real candidate'

  call LCMOP(projected,trim(output_path),0,2,0)
  call REQUIRE_ASSOCIATED(projected,'fresh persistent PROJECTED output')
  call REQUIRE_EMPTY_XSM_ROOT(projected)
  b2j_calls=1
  call SPOR64_B2J_PROJECT_ARCHIVE(projected,axial_closed, &
      axial_track_base,archive_closed,status)
  if (status /= SPOR64_B2J_ARCHIVE_PROJECTED) &
      error stop 'production B2j rejected the full closed archive'

  ! B2j owns the final visible mutation.  Closing the persistent object is
  ! the only operation permitted after its archive commit returns.
  call LCMCL(projected,1)
  call LCMCL(archive_closed,2)
  call LCMCL(axial_closed,2)
  call LCMCL(candidate,2)
  call LCMCL(axial_track_base,1)
  call LCMCL(archive_base,1)
  call LCMCL(axial_base,1)

  if (b2c_calls /= NSNAP .or. b2i_calls /= 1 .or. b2j_calls /= 1) &
      error stop 'production call inventory differs'
  if (full_copy_items /= 3*NSNAP) &
      error stop 'full-copy item inventory differs'

  write(*,'(A)') 'B2L FULL PROJECTED PREPARATION PASS'
  write(*,'(A,I0,A,I0,A,I0)') 'B2L PRODUCTION-B2C-CALLS=',b2c_calls, &
      ' B2I-CALLS=',b2i_calls,' B2J-CALLS=',b2j_calls
  write(*,'(A,I0)') 'B2L FULL-TRACK-LIBRARY-SYSTEM-COPIES=', &
      full_copy_items
  write(*,'(A)') 'B2L POST-B2J-MUTATIONS=0 PROJECTED-SYSTEM=ABSENT'

contains

  subroutine BUILD_FULL_CANDIDATE(real_archive,output,b2c_count,copy_count)
    type(c_ptr), intent(in) :: real_archive
    type(c_ptr), intent(out) :: output
    integer, intent(out) :: b2c_count, copy_count

    character(len=12) :: signature
    integer :: listdim, ip
    real(real64) :: iter_keff
    type(c_ptr) :: source_tracks, source_libraries, source_systems
    type(c_ptr) :: source_fluxes, output_tracks, output_libraries
    type(c_ptr) :: output_systems, output_fluxes
    type(c_ptr) :: source_item, output_item

    call REQUIRE_CHARACTER(real_archive,'SIGNATURE','L_ARCHIVE')
    call REQUIRE_RECORD(real_archive,'LISTDIM',1,1)
    call REQUIRE_RECORD(real_archive,'SPOT-ITER-K',1,4)
    call LCMGET(real_archive,'LISTDIM',listdim)
    call LCMGET(real_archive,'SPOT-ITER-K',iter_keff)
    if (listdim /= NSNAP) error stop 'frozen archive plane count differs'
    if (.not. ieee_is_finite(iter_keff) .or. iter_keff <= 0.0_real64) &
        error stop 'frozen archive K is invalid'

    source_tracks=LCMGID(real_archive,'TRACK')
    source_libraries=LCMGID(real_archive,'MICROLIB2')
    source_systems=LCMGID(real_archive,'SYSTEM')
    source_fluxes=LCMGID(real_archive,'FLUX')
    call REQUIRE_ASSOCIATED(source_tracks,'real TRACK list')
    call REQUIRE_ASSOCIATED(source_libraries,'real MICROLIB2 list')
    call REQUIRE_ASSOCIATED(source_systems,'real SYSTEM list')
    call REQUIRE_ASSOCIATED(source_fluxes,'real FLUX list')

    call LCMOP(output,'B2L-FULL-IN',0,1,0)
    call REQUIRE_ASSOCIATED(output,'fresh full candidate')
    signature='L_ARCHIVE'
    call LCMPTC(output,'SIGNATURE',12,signature)
    call LCMPUT(output,'LISTDIM',1,1,listdim)
    call LCMPUT(output,'SPOT-ITER-K',1,4,iter_keff)
    output_tracks=LCMLID(output,'TRACK',NSNAP)
    output_libraries=LCMLID(output,'MICROLIB2',NSNAP)
    output_systems=LCMLID(output,'SYSTEM',NSNAP)
    output_fluxes=LCMLID(output,'FLUX',NSNAP)
    call REQUIRE_ASSOCIATED(output_tracks,'fresh TRACK list')
    call REQUIRE_ASSOCIATED(output_libraries,'fresh MICROLIB2 list')
    call REQUIRE_ASSOCIATED(output_systems,'fresh SYSTEM list')
    call REQUIRE_ASSOCIATED(output_fluxes,'fresh FLUX list')

    b2c_count=0
    copy_count=0
    do ip=1,NSNAP
      call REQUIRE_DIRECTORY_ITEM(source_tracks,ip)
      call REQUIRE_DIRECTORY_ITEM(source_libraries,ip)
      call REQUIRE_DIRECTORY_ITEM(source_systems,ip)
      call REQUIRE_DIRECTORY_ITEM(source_fluxes,ip)

      source_item=LCMGIL(source_tracks,ip)
      output_item=LCMDIL(output_tracks,ip)
      call LCMEQU(source_item,output_item)
      copy_count=copy_count+1

      source_item=LCMGIL(source_libraries,ip)
      output_item=LCMDIL(output_libraries,ip)
      call LCMEQU(source_item,output_item)
      copy_count=copy_count+1

      source_item=LCMGIL(source_systems,ip)
      output_item=LCMDIL(output_systems,ip)
      call LCMEQU(source_item,output_item)
      copy_count=copy_count+1

      source_item=LCMGIL(source_fluxes,ip)
      output_item=LCMDIL(output_fluxes,ip)
      call PUBLISH_FULL_FLUX(source_item,output_item,b2c_count)
    end do
  end subroutine BUILD_FULL_CANDIDATE


  subroutine PUBLISH_FULL_FLUX(history,target,b2c_count)
    type(c_ptr), intent(in) :: history, target
    integer, intent(inout) :: b2c_count

    character(len=4), parameter :: option='B0  '
    character(len=12), parameter :: macro_name='MACRO0'
    character(len=12), parameter :: track_name='TRACK'
    character(len=12), parameter :: system_name='SYSTEM'
    character(len=12) :: published_name
    integer :: ig, status
    integer :: keyflx(NREG), imerge(NMAT)
    real(real32) :: flux32(NUNKNO), source32(NUNKNO)
    real(real32) :: leakage32(NGRP), epsilon32
    real(real64) :: flux64(NUNKNO,NGRP), source64(NUNKNO,NGRP)
    type(c_ptr) :: history_flux, history_source, published

    call REQUIRE_RECORD(history,'FLUX',NGRP,10)
    call REQUIRE_RECORD(history,'SOUR',NGRP,10)
    call REQUIRE_RECORD(history,'KEYFLX',NREG,1)
    call REQUIRE_RECORD(history,'IMERGE-LEAK',NMAT,1)
    call REQUIRE_RECORD(history,'SPOT-LEAK1D',NGRP,2)
    history_flux=LCMGID(history,'FLUX')
    history_source=LCMGID(history,'SOUR')
    call REQUIRE_ASSOCIATED(history_flux,'historical FLUX list')
    call REQUIRE_ASSOCIATED(history_source,'historical SOUR list')
    call LCMGET(history,'KEYFLX',keyflx)
    call LCMGET(history,'IMERGE-LEAK',imerge)
    call LCMGET(history,'SPOT-LEAK1D',leakage32)
    if (any(imerge /= 1)) error stop 'historical merge map differs'
    if (.not. all(ieee_is_finite(leakage32))) &
        error stop 'historical leakage is nonfinite'

    do ig=1,NGRP
      call LCMGDL(history_flux,ig,flux32)
      call LCMGDL(history_source,ig,source32)
      if (.not. all(ieee_is_finite(flux32)) .or. &
          .not. all(ieee_is_finite(source32))) &
          error stop 'historical terminal payload is nonfinite'
      flux64(:,ig)=real(flux32,real64)
      source64(:,ig)=real(source32,real64)
    end do

    epsilon32=transfer(FROZEN_TOL_BITS,0.0_real32)
    write(published_name,'("B2L-B2C",I2.2)') b2c_count+1
    call LCMOP(published,published_name,0,1,0)
    call REQUIRE_ASSOCIATED(published,'B2C publication stage')
    call REQUIRE_EMPTY_ROOT(published)
    b2c_count=b2c_count+1
    call SPOR64_B2C_PUBLISH(published,4,flux64,source64,keyflx,1,imerge, &
        leakage32,epsilon32,epsilon32,epsilon32,option,macro_name, &
        track_name,system_name,status)
    if (status /= SPOR64_B2C_HOST_COMMITTED) &
        error stop 'production B2c rejected full candidate FLUX'
    call LCMEQU(published,target)
    call LCMCL(published,2)
  end subroutine PUBLISH_FULL_FLUX


  subroutine REQUIRE_DIRECTORY_ITEM(list,index)
    type(c_ptr), intent(in) :: list
    integer, intent(in) :: index
    integer :: length, record_type

    call LCMLEL(list,index,length,record_type)
    if (length /= -1 .or. record_type /= 0) &
        error stop 'expected directory list item'
  end subroutine REQUIRE_DIRECTORY_ITEM


  subroutine REQUIRE_RECORD(root,name,expected_length,expected_type)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: length, record_type

    call LCMLEN(root,name,length,record_type)
    if (length /= expected_length .or. record_type /= expected_type) &
        error stop 'record schema differs'
  end subroutine REQUIRE_RECORD


  subroutine REQUIRE_CHARACTER(root,name,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, expected
    character(len=12) :: found

    call REQUIRE_RECORD(root,name,3,3)
    call LCMGTC(root,name,12,found)
    if (found /= expected) error stop 'character record differs'
  end subroutine REQUIRE_CHARACTER


  subroutine REQUIRE_ASSOCIATED(pointer,owner)
    type(c_ptr), intent(in) :: pointer
    character(len=*), intent(in) :: owner

    if (.not. c_associated(pointer)) then
      write(*,'(A)') trim(owner)
      error stop 'required GANLIB pointer is absent'
    end if
  end subroutine REQUIRE_ASSOCIATED


  subroutine REQUIRE_EMPTY_ROOT(root)
    type(c_ptr), intent(in) :: root
    character(len=72) :: object_file
    character(len=12) :: object_name
    integer :: object_length
    logical :: empty, is_lcm

    call REQUIRE_ASSOCIATED(root,'empty-root candidate')
    call LCMINF(root,object_file,object_name,empty,object_length,is_lcm)
    if (.not. is_lcm .or. .not. empty .or. object_length /= -1 .or. &
        trim(object_name) /= '/') error stop 'publication root is not empty'
  end subroutine REQUIRE_EMPTY_ROOT


  subroutine REQUIRE_EMPTY_XSM_ROOT(root)
    type(c_ptr), intent(in) :: root
    character(len=72) :: object_file
    character(len=12) :: object_name
    integer :: object_length
    logical :: empty, memory_backed

    call REQUIRE_ASSOCIATED(root,'empty XSM-root candidate')
    call LCMINF(root,object_file,object_name,empty,object_length, &
        memory_backed)
    if (memory_backed .or. .not. empty .or. object_length /= -1 .or. &
        trim(object_name) /= '/') error stop 'output is not a fresh XSM root'
  end subroutine REQUIRE_EMPTY_XSM_ROOT

end program PREPARE_B2L_PROJECTED
