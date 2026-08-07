program TEST_B2J_XSM_TARGET
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_quiet_nan, ieee_value
  use SPOR64_B2J, only : SPOR64_B2J_ADMISSION_FAILED, &
      SPOR64_B2J_ARCHIVE_PROJECTED, SPOR64_B2J_PROJECT_ARCHIVE
  use B2J_FIXTURE_SUPPORT
  implicit none

  integer, parameter :: EXPECTED_CALLS=6
  character(len=*), parameter :: POSITIVE_PATH='b2j_xsm_positive.xsm'
  character(len=*), parameter :: SENTINEL_PATH='b2j_xsm_sentinel.xsm'
  character(len=*), parameter :: TOMBSTONE_PATH='b2j_xsm_tombstone.xsm'
  character(len=*), parameter :: EARLY_PATH='b2j_xsm_early.xsm'
  character(len=*), parameter :: LATE2_PATH='b2j_xsm_late2.xsm'
  character(len=*), parameter :: LATE3_PATH='b2j_xsm_late3.xsm'

  character(len=1024) :: axial_path, archive_path, axial_track_path
  integer :: b2c_calls, b2i_calls, b2j_calls, commit_count
  integer :: rejection_count, reopen_checks, fresh_empty_checks
  integer :: deep_copy_checks, replacement_checks, mirror_bit_checks
  type(c_ptr) :: axial_base, archive_base, axial_track_base
  type(c_ptr) :: axial_closed, archive_closed

  if (command_argument_count() /= 3) error stop &
      'expected state1 AX, state1 archive, and axial-track paths'
  call get_command_argument(1,axial_path)
  call get_command_argument(2,archive_path)
  call get_command_argument(3,axial_track_path)

  call REQUIRE_TARGET_ABSENT(POSITIVE_PATH)
  call REQUIRE_TARGET_ABSENT(SENTINEL_PATH)
  call REQUIRE_TARGET_ABSENT(TOMBSTONE_PATH)
  call REQUIRE_TARGET_ABSENT(EARLY_PATH)
  call REQUIRE_TARGET_ABSENT(LATE2_PATH)
  call REQUIRE_TARGET_ABSENT(LATE3_PATH)

  call LCMOP(axial_base,trim(axial_path),2,2,0)
  call LCMOP(archive_base,trim(archive_path),2,2,0)
  call LCMOP(axial_track_base,trim(axial_track_path),2,2,0)
  call B2J_REQUIRE_ASSOCIATED(axial_base,'frozen AX')
  call B2J_REQUIRE_ASSOCIATED(archive_base,'frozen archive')
  call B2J_REQUIRE_ASSOCIATED(axial_track_base,'frozen axial track')
  call B2J_BUILD_CLOSED_PAIR(axial_base,archive_base,axial_track_base, &
      axial_closed,archive_closed,b2c_calls,b2i_calls)

  b2j_calls=0
  commit_count=0
  rejection_count=0
  reopen_checks=0
  fresh_empty_checks=0
  deep_copy_checks=0
  replacement_checks=0
  mirror_bit_checks=0

  call RUN_POSITIVE_XSM()
  call RUN_SENTINEL_REJECTION()
  call RUN_TOMBSTONE_REJECTION()
  call RUN_EARLY_REJECTION()
  call RUN_LATE_REJECTION(2,LATE2_PATH)
  call RUN_LATE_REJECTION(3,LATE3_PATH)
  call VERIFY_INPUT_PAIR_UNCHANGED()

  if (b2j_calls /= EXPECTED_CALLS) error stop 'B2J call count differs'
  if (commit_count /= 1 .or. rejection_count /= 5) &
      error stop 'B2J result count differs'
  if (reopen_checks /= EXPECTED_CALLS) &
      error stop 'XSM reopen count differs'
  if (fresh_empty_checks /= 3) &
      error stop 'fresh zero-write count differs'
  if (deep_copy_checks /= 2*B2J_NSNAP) &
      error stop 'deep-copy count differs'
  if (replacement_checks /= B2J_NSNAP) &
      error stop 'replacement count differs'
  if (mirror_bit_checks /= B2J_NUNKNO*B2J_NGRP*B2J_NSNAP) &
      error stop 'mirror bit count differs'

  call LCMCL(archive_closed,2)
  call LCMCL(axial_closed,2)
  call LCMCL(axial_track_base,1)
  call LCMCL(archive_base,1)
  call LCMCL(axial_base,1)

  write(*,'(A)') 'B2L B2J-XSM-TARGET PASS'
  write(*,'(A)') 'B2L B2J-XSM-CALLS=6 COMMITS=1 REJECTIONS=5'
  write(*,'(A)') 'B2L B2J-XSM-REOPEN-CHECKS=6 PROJECTED=1 '// &
      'SENTINEL-ONLY=1 TOMBSTONED=1 FRESH-EMPTY=3'
  write(*,'(A)') 'B2L B2J-XSM-ROOT-ENTRIES=7 AUTHORITY-ENTRIES=4 '// &
      'SYSTEM-ABSENT=1'
  write(*,'(A)') &
      'B2L B2J-XSM-LATE-B2H-REJECTIONS=2 EARLY-REJECTIONS=3'
  write(*,'(A)') 'B2L B2J-XSM-DRAGON=0 ASM=0 FLU=0 CONT=0 '// &
      'SPOR64K=0 EMPIRICAL-CONTROLS=0'

contains

  subroutine RUN_POSITIVE_XSM()
    integer :: status
    type(c_ptr) :: output

    call OPEN_FRESH_XSM(POSITIVE_PATH,output)
    b2j_calls=b2j_calls+1
    call SPOR64_B2J_PROJECT_ARCHIVE(output,axial_closed, &
        axial_track_base,archive_closed,status)
    if (status /= SPOR64_B2J_ARCHIVE_PROJECTED) &
        error stop 'fresh XSM projection was rejected'
    commit_count=commit_count+1
    call LCMCL(output,1)
    call OPEN_READ_ONLY_XSM(POSITIVE_PATH,output)
    reopen_checks=reopen_checks+1
    call VERIFY_PROJECTED_XSM(output)
    call LCMCL(output,1)
  end subroutine RUN_POSITIVE_XSM


  subroutine RUN_SENTINEL_REJECTION()
    integer, parameter :: SENTINEL=271828
    integer :: status
    type(c_ptr) :: output

    call OPEN_FRESH_XSM(SENTINEL_PATH,output)
    call LCMPUT(output,'SENTINEL',1,1,SENTINEL)
    b2j_calls=b2j_calls+1
    call SPOR64_B2J_PROJECT_ARCHIVE(output,axial_closed, &
        axial_track_base,archive_closed,status)
    if (status /= SPOR64_B2J_ADMISSION_FAILED) &
        error stop 'nonempty XSM target was accepted'
    rejection_count=rejection_count+1
    call LCMCL(output,1)
    call OPEN_READ_ONLY_XSM(SENTINEL_PATH,output)
    reopen_checks=reopen_checks+1
    call B2J_REQUIRE_ONLY_SENTINEL(output,SENTINEL)
    call REQUIRE_NO_COMMIT_RECORDS(output)
    call LCMCL(output,1)
  end subroutine RUN_SENTINEL_REJECTION


  subroutine RUN_TOMBSTONE_REJECTION()
    integer, parameter :: SENTINEL=314159
    integer :: status
    type(c_ptr) :: output

    call OPEN_FRESH_XSM(TOMBSTONE_PATH,output)
    call LCMPUT(output,'SENTINEL',1,1,SENTINEL)
    call LCMDEL(output,'SENTINEL')
    call REQUIRE_TOMBSTONED_XSM(output)
    b2j_calls=b2j_calls+1
    call SPOR64_B2J_PROJECT_ARCHIVE(output,axial_closed, &
        axial_track_base,archive_closed,status)
    if (status /= SPOR64_B2J_ADMISSION_FAILED) &
        error stop 'tombstoned XSM target was accepted'
    rejection_count=rejection_count+1
    call LCMCL(output,1)
    call OPEN_READ_ONLY_XSM(TOMBSTONE_PATH,output)
    reopen_checks=reopen_checks+1
    call REQUIRE_TOMBSTONED_XSM(output)
    call REQUIRE_NO_COMMIT_RECORDS(output)
    call LCMCL(output,1)
  end subroutine RUN_TOMBSTONE_REJECTION


  subroutine RUN_EARLY_REJECTION()
    integer :: epoch, status
    type(c_ptr) :: invalid_axial, output

    call B2J_CLONE_OBJECT(axial_closed,'B2J-XSM-EARLY',invalid_axial)
    epoch=1
    call LCMPUT(invalid_axial,'SPOT-X-EPOCH',1,1,epoch)
    call OPEN_FRESH_XSM(EARLY_PATH,output)
    b2j_calls=b2j_calls+1
    call SPOR64_B2J_PROJECT_ARCHIVE(output,invalid_axial, &
        axial_track_base,archive_closed,status)
    if (status /= SPOR64_B2J_ADMISSION_FAILED) &
        error stop 'early-invalid input was accepted'
    rejection_count=rejection_count+1
    call LCMCL(output,1)
    call LCMCL(invalid_axial,2)
    call OPEN_READ_ONLY_XSM(EARLY_PATH,output)
    reopen_checks=reopen_checks+1
    call REQUIRE_FRESH_EMPTY_XSM(output)
    fresh_empty_checks=fresh_empty_checks+1
    call LCMCL(output,1)
  end subroutine RUN_EARLY_REJECTION


  subroutine RUN_LATE_REJECTION(plane,path)
    integer, intent(in) :: plane
    character(len=*), intent(in) :: path
    integer :: length, record_type, status
    real(real32) :: eps(5)
    real(real64) :: source_group(B2J_NUNKNO)
    type(c_ptr) :: invalid_archive, fluxes, item, authority, source
    type(c_ptr) :: output

    call B2J_CLONE_OBJECT(archive_closed,'B2J-XSM-LATE',invalid_archive)
    fluxes=LCMGID(invalid_archive,'FLUX')
    item=LCMGIL(fluxes,plane)
    if (plane == 2) then
      call LCMGET(item,'EPS-CONVERGE',eps)
      eps(1)=nearest(eps(1),1.0_real32)
      call LCMPUT(item,'EPS-CONVERGE',5,2,eps)
    else if (plane == 3) then
      authority=LCMGID(item,'SPOT-R64')
      source=LCMGID(authority,'SOUR')
      call LCMLEL(source,1,length,record_type)
      if (length /= B2J_NUNKNO .or. record_type /= 4) &
          error stop 'late plane-3 mutation schema differs'
      call LCMGDL(source,1,source_group)
      source_group(1)=ieee_value(0.0_real64,ieee_quiet_nan)
      call LCMPDL(source,1,B2J_NUNKNO,4,source_group)
    else
      error stop 'unknown late-rejection plane'
    end if

    call OPEN_FRESH_XSM(path,output)
    b2j_calls=b2j_calls+1
    call SPOR64_B2J_PROJECT_ARCHIVE(output,axial_closed, &
        axial_track_base,invalid_archive,status)
    if (status /= SPOR64_B2J_ADMISSION_FAILED) &
        error stop 'late B2H-invalid input was accepted'
    rejection_count=rejection_count+1
    call LCMCL(output,1)
    call LCMCL(invalid_archive,2)
    call OPEN_READ_ONLY_XSM(path,output)
    reopen_checks=reopen_checks+1
    call REQUIRE_FRESH_EMPTY_XSM(output)
    fresh_empty_checks=fresh_empty_checks+1
    call LCMCL(output,1)
  end subroutine RUN_LATE_REJECTION


  subroutine VERIFY_PROJECTED_XSM(output)
    type(c_ptr), intent(in) :: output
    integer :: epoch, listdim, nplane, ip
    real(real64) :: expected, found
    type(c_ptr) :: authority, input_tracks, output_tracks
    type(c_ptr) :: input_libraries, output_libraries
    type(c_ptr) :: input_fluxes, output_fluxes
    type(c_ptr) :: input_item, output_item

    call REQUIRE_XSM_ROOT(output,.false.)
    call B2J_REQUIRE_EXACT_INVENTORY(output, &
        [character(len=12) :: 'SIGNATURE','LISTDIM','SPOT-ITER-K', &
         'TRACK','MICROLIB2','FLUX','SPOT-R64'])
    call B2J_REQUIRE_CHARACTER(output,'SIGNATURE',12,'L_ARCHIVE')
    call B2J_REQUIRE_ABSENT(output,'SYSTEM')
    call LCMGET(output,'LISTDIM',listdim)
    if (listdim /= B2J_NSNAP) error stop 'projected LISTDIM differs'
    call LCMGET(archive_closed,'SPOT-ITER-K',expected)
    call LCMGET(output,'SPOT-ITER-K',found)
    if (B2J_BITS64(found) /= B2J_BITS64(expected)) &
        error stop 'projected K bits differ'

    authority=LCMGID(output,'SPOT-R64')
    call B2J_REQUIRE_EXACT_INVENTORY(authority, &
        [character(len=12) :: 'RHO','NPLANE','STATE','EPOCH'])
    call B2J_REQUIRE_CHARACTER(authority,'STATE',12,'PROJECTED')
    call LCMGET(authority,'NPLANE',nplane)
    call LCMGET(authority,'EPOCH',epoch)
    if (nplane /= B2J_NSNAP .or. epoch /= 1) &
        error stop 'projected root lifecycle differs'
    call LCMGET(axial_closed,'SPOT-X-RHO',expected)
    call LCMGET(authority,'RHO',found)
    if (B2J_BITS64(found) /= B2J_BITS64(expected)) &
        error stop 'projected RHO bits differ'

    input_tracks=LCMGID(archive_closed,'TRACK')
    output_tracks=LCMGID(output,'TRACK')
    input_libraries=LCMGID(archive_closed,'MICROLIB2')
    output_libraries=LCMGID(output,'MICROLIB2')
    input_fluxes=LCMGID(archive_closed,'FLUX')
    output_fluxes=LCMGID(output,'FLUX')
    call B2J_REQUIRE_DISTINCT(input_tracks,output_tracks,'TRACK list')
    call B2J_REQUIRE_DISTINCT(input_libraries,output_libraries, &
        'MICROLIB2 list')
    call B2J_REQUIRE_DISTINCT(input_fluxes,output_fluxes,'FLUX list')
    do ip=1,B2J_NSNAP
      input_item=LCMGIL(input_tracks,ip)
      output_item=LCMGIL(output_tracks,ip)
      call VERIFY_TRACK_COPY(input_item,output_item,1000+ip)
      deep_copy_checks=deep_copy_checks+1
      input_item=LCMGIL(input_libraries,ip)
      output_item=LCMGIL(output_libraries,ip)
      call VERIFY_LIBRARY_COPY(input_item,output_item,2000+ip)
      deep_copy_checks=deep_copy_checks+1
      input_item=LCMGIL(input_fluxes,ip)
      output_item=LCMGIL(output_fluxes,ip)
      call VERIFY_PROJECTED_PLANE(input_item,output_item)
      replacement_checks=replacement_checks+1
    end do
  end subroutine VERIFY_PROJECTED_XSM


  subroutine VERIFY_TRACK_COPY(input,output,sentinel)
    type(c_ptr), intent(in) :: input, output
    integer, intent(in) :: sentinel

    call B2J_REQUIRE_DISTINCT(input,output,'TRACK item')
    call B2J_COMPARE_CHARACTER_RECORD(input,output,'SIGNATURE',12)
    call B2J_COMPARE_CHARACTER_RECORD(input,output,'TRACK-TYPE',12)
    call B2J_COMPARE_CHARACTER_RECORD(input,output,'LINK.FTRACK',12)
    call B2J_COMPARE_INTEGER_RECORD(input,output,'STATE-VECTOR')
    call B2J_COMPARE_INTEGER_RECORD(input,output,'KEYFLX')
    call B2J_COMPARE_INTEGER_RECORD(input,output,'KEYFLX$ANIS')
    call B2J_COMPARE_REAL32_RECORD(input,output,'VOLUME')
    call B2J_VERIFY_DEEP_SENTINEL(input,output,sentinel)
  end subroutine VERIFY_TRACK_COPY


  subroutine VERIFY_LIBRARY_COPY(input,output,sentinel)
    type(c_ptr), intent(in) :: input, output
    integer, intent(in) :: sentinel
    integer :: ig
    type(c_ptr) :: input_macro, output_macro, input_groups, output_groups

    call B2J_REQUIRE_DISTINCT(input,output,'MICROLIB2 item')
    call B2J_COMPARE_CHARACTER_RECORD(input,output,'SIGNATURE',12)
    call B2J_COMPARE_INTEGER_RECORD(input,output,'STATE-VECTOR')
    input_macro=LCMGID(input,'MACROLIB')
    output_macro=LCMGID(output,'MACROLIB')
    call B2J_REQUIRE_DISTINCT(input_macro,output_macro,'MACROLIB')
    call B2J_COMPARE_CHARACTER_RECORD(input_macro,output_macro, &
        'SIGNATURE',12)
    call B2J_COMPARE_INTEGER_RECORD(input_macro,output_macro, &
        'STATE-VECTOR')
    input_groups=LCMGID(input_macro,'GROUP')
    output_groups=LCMGID(output_macro,'GROUP')
    call B2J_REQUIRE_DISTINCT(input_groups,output_groups,'MACROLIB GROUP')
    do ig=1,B2J_NGRP
      call B2J_REQUIRE_DIRECTORY_ITEM(input_groups,ig)
      call B2J_REQUIRE_DIRECTORY_ITEM(output_groups,ig)
    end do
    call B2J_VERIFY_DEEP_SENTINEL(input,output,sentinel)
  end subroutine VERIFY_LIBRARY_COPY


  subroutine VERIFY_PROJECTED_PLANE(seed,output)
    type(c_ptr), intent(in) :: seed, output
    integer :: epoch, ig, iu, length, record_type
    real(real32) :: mirror32(B2J_NUNKNO)
    real(real64) :: authority64(B2J_NUNKNO)
    type(c_ptr) :: authority, authority_flux, mirror_flux

    call B2J_REQUIRE_DISTINCT(seed,output,'FLUX plane')
    call B2J_REQUIRE_EXACT_INVENTORY(output, &
        [character(len=12) :: 'SPOT-R64','FLUX','SIGNATURE', &
         'STATE-VECTOR','EPS-CONVERGE','IMERGE-LEAK','KEYFLX','OPTION', &
         'LINK.MACRO','LINK.TRACK','LINK.SYSTEM','SPOT-LEAK1D'])
    call B2J_REQUIRE_ABSENT(output,'B2I-SENT')
    call B2J_REQUIRE_ABSENT(output,'B2I-DEEP')
    call B2J_REQUIRE_ABSENT(output,'SOUR')
    call B2J_REQUIRE_ABSENT(output,'QFISS')
    call B2J_REQUIRE_ABSENT(output,'SPOT-QFISS')
    call B2J_REQUIRE_ABSENT(output,'DSOUR')
    call B2J_COMPARE_CHARACTER_RECORD(seed,output,'SIGNATURE',12)
    call B2J_COMPARE_CHARACTER_RECORD(seed,output,'OPTION',4)
    call B2J_COMPARE_CHARACTER_RECORD(seed,output,'LINK.MACRO',12)
    call B2J_COMPARE_CHARACTER_RECORD(seed,output,'LINK.TRACK',12)
    call B2J_COMPARE_CHARACTER_RECORD(seed,output,'LINK.SYSTEM',12)
    call B2J_COMPARE_INTEGER_RECORD(seed,output,'STATE-VECTOR')
    call B2J_COMPARE_INTEGER_RECORD(seed,output,'IMERGE-LEAK')
    call B2J_COMPARE_INTEGER_RECORD(seed,output,'KEYFLX')
    call B2J_COMPARE_REAL32_RECORD(seed,output,'EPS-CONVERGE')
    call B2J_COMPARE_REAL32_RECORD(seed,output,'SPOT-LEAK1D')

    authority=LCMGID(output,'SPOT-R64')
    call B2J_REQUIRE_EXACT_INVENTORY(authority, &
        [character(len=12) :: 'RHO','FLUX','STATE','EPOCH'])
    call B2J_REQUIRE_CHARACTER(authority,'STATE',12,'PROJECTED')
    call LCMGET(authority,'EPOCH',epoch)
    if (epoch /= 1) error stop 'projected plane epoch differs'
    call B2J_REQUIRE_ABSENT(authority,'SOUR')
    call B2J_REQUIRE_ABSENT(authority,'QFISS')
    authority_flux=LCMGID(authority,'FLUX')
    mirror_flux=LCMGID(output,'FLUX')
    do ig=1,B2J_NGRP
      call LCMLEL(authority_flux,ig,length,record_type)
      if (length /= B2J_NUNKNO .or. record_type /= 4) &
          error stop 'projected authority FLUX schema differs'
      call LCMLEL(mirror_flux,ig,length,record_type)
      if (length /= B2J_NUNKNO .or. record_type /= 2) &
          error stop 'projected mirror FLUX schema differs'
      call LCMGDL(authority_flux,ig,authority64)
      call LCMGDL(mirror_flux,ig,mirror32)
      do iu=1,B2J_NUNKNO
        if (B2J_BITS32(mirror32(iu)) /= &
            B2J_BITS32(real(authority64(iu),real32))) &
            error stop 'projected mirror downcast bits differ'
        mirror_bit_checks=mirror_bit_checks+1
      end do
    end do
  end subroutine VERIFY_PROJECTED_PLANE


  subroutine VERIFY_INPUT_PAIR_UNCHANGED()
    integer :: epoch, ip
    type(c_ptr) :: authority, tracks, libraries, systems, fluxes, plane

    call B2J_REQUIRE_CHARACTER(axial_closed,'SPOT-X-STATE',12,'CLOSED')
    call LCMGET(axial_closed,'SPOT-X-EPOCH',epoch)
    if (epoch /= 0) error stop 'input AX epoch changed'
    call B2J_REQUIRE_EXACT_INVENTORY(archive_closed, &
        [character(len=12) :: 'SIGNATURE','LISTDIM','SPOT-ITER-K', &
         'TRACK','MICROLIB2','SYSTEM','FLUX','SPOT-R64'])
    authority=LCMGID(archive_closed,'SPOT-R64')
    call B2J_REQUIRE_CHARACTER(authority,'STATE',12,'CLOSED')
    call LCMGET(authority,'EPOCH',epoch)
    if (epoch /= 0) error stop 'input archive epoch changed'
    tracks=LCMGID(archive_closed,'TRACK')
    libraries=LCMGID(archive_closed,'MICROLIB2')
    systems=LCMGID(archive_closed,'SYSTEM')
    fluxes=LCMGID(archive_closed,'FLUX')
    do ip=1,B2J_NSNAP
      call B2J_REQUIRE_RECORD(LCMGIL(tracks,ip),'B2I-SENT',1,1)
      call B2J_REQUIRE_RECORD(LCMGIL(libraries,ip),'B2I-SENT',1,1)
      call B2J_REQUIRE_RECORD(LCMGIL(systems,ip),'B2I-SENT',1,1)
      plane=LCMGIL(fluxes,ip)
      call B2J_REQUIRE_RECORD(plane,'B2I-SENT',1,1)
      authority=LCMGID(plane,'SPOT-R64')
      call B2J_REQUIRE_CHARACTER(authority,'STATE',12,'SOLVED')
      call LCMGET(authority,'EPOCH',epoch)
      if (epoch /= 0) error stop 'input plane epoch changed'
    end do
  end subroutine VERIFY_INPUT_PAIR_UNCHANGED


  subroutine OPEN_FRESH_XSM(path,root)
    character(len=*), intent(in) :: path
    type(c_ptr), intent(out) :: root

    call LCMOP(root,path,0,2,0)
    call B2J_REQUIRE_ASSOCIATED(root,'fresh XSM target')
    call REQUIRE_FRESH_EMPTY_XSM(root)
  end subroutine OPEN_FRESH_XSM


  subroutine OPEN_READ_ONLY_XSM(path,root)
    character(len=*), intent(in) :: path
    type(c_ptr), intent(out) :: root

    call LCMOP(root,path,2,2,0)
    call B2J_REQUIRE_ASSOCIATED(root,'reopened XSM target')
  end subroutine OPEN_READ_ONLY_XSM


  subroutine REQUIRE_FRESH_EMPTY_XSM(root)
    type(c_ptr), intent(in) :: root

    call REQUIRE_XSM_ROOT(root,.true.)
    call REQUIRE_NO_COMMIT_RECORDS(root)
  end subroutine REQUIRE_FRESH_EMPTY_XSM


  subroutine REQUIRE_TOMBSTONED_XSM(root)
    type(c_ptr), intent(in) :: root

    ! XSM retains one physical directory slot after LCMDEL.  It must not be
    ! admitted as a fresh target even though the deleted key is inaccessible.
    call REQUIRE_XSM_ROOT(root,.false.)
    call B2J_REQUIRE_ABSENT(root,'SENTINEL')
  end subroutine REQUIRE_TOMBSTONED_XSM


  subroutine REQUIRE_XSM_ROOT(root,expected_empty)
    type(c_ptr), intent(in) :: root
    logical, intent(in) :: expected_empty
    character(len=72) :: object_file
    character(len=12) :: object_name
    integer :: object_length
    logical :: empty, memory_backed

    call B2J_REQUIRE_ASSOCIATED(root,'XSM root')
    call LCMINF(root,object_file,object_name,empty,object_length, &
        memory_backed)
    if (memory_backed .or. object_length /= -1 .or. &
        trim(object_name) /= '/' .or. empty .neqv. expected_empty) &
        error stop 'XSM root state differs'
  end subroutine REQUIRE_XSM_ROOT


  subroutine REQUIRE_NO_COMMIT_RECORDS(root)
    type(c_ptr), intent(in) :: root
    integer :: i
    character(len=12), parameter :: names(7) = &
        ['SIGNATURE   ','LISTDIM     ','SPOT-ITER-K ','TRACK       ', &
         'MICROLIB2   ','FLUX        ','SPOT-R64    ']

    do i=1,size(names)
      call B2J_REQUIRE_ABSENT(root,names(i))
    end do
    call B2J_REQUIRE_ABSENT(root,'SYSTEM')
  end subroutine REQUIRE_NO_COMMIT_RECORDS


  subroutine REQUIRE_TARGET_ABSENT(path)
    character(len=*), intent(in) :: path
    logical :: exists

    inquire(file=path,exist=exists)
    if (exists) error stop 'refusing to overwrite an XSM target'
  end subroutine REQUIRE_TARGET_ABSENT

end program TEST_B2J_XSM_TARGET
