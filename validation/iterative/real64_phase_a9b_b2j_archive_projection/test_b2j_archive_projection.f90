program TEST_B2J_ARCHIVE_PROJECTION
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite, &
      ieee_quiet_nan, ieee_value
  use SPOR64_B2J, only : SPOR64_B2J_ADMISSION_FAILED, &
      SPOR64_B2J_ARCHIVE_PROJECTED, SPOR64_B2J_PROJECT_ARCHIVE
  use B2J_FIXTURE_SUPPORT
  implicit none

  integer, parameter :: NREJECTION=12
  character(len=1024) :: axial_path, archive_path, axial_track_path
  integer :: b2c_calls, b2i_calls, b2j_calls, rejection_count
  integer :: reconstruction_slices, region_bit_checks
  integer :: nonregion_bit_checks, mirror_bit_checks
  integer :: leakage_bit_checks, deep_copy_checks, replacement_checks
  integer :: source_absences, qfiss_absences, system_absences
  integer :: fresh_zero_write_rejections, collision_rejections
  integer, allocatable :: rank(:), offset(:), basis_offset(:)
  integer, allocatable :: keyflx(:,:)
  real(real32), allocatable :: basis32(:), seed_leak32(:,:)
  real(real64), allocatable :: coordinates64(:), canonical_leak64(:)
  real(real64), allocatable :: projected64(:,:,:)
  real(real64), allocatable :: seed_flux64(:,:,:), seed_source64(:,:,:)
  real(real64) :: canonical_rho64, archive_keff64
  type(c_ptr) :: axial_base, archive_base, axial_track_base
  type(c_ptr) :: axial_closed, archive_closed

  if (command_argument_count() /= 3) error stop &
    'expected state1_axial.xsm, state1_snapshots.xsm, and axial track paths'
  call get_command_argument(1,axial_path)
  call get_command_argument(2,archive_path)
  call get_command_argument(3,axial_track_path)

  call LCMOP(axial_base,trim(axial_path),2,2,0)
  call LCMOP(archive_base,trim(archive_path),2,2,0)
  call LCMOP(axial_track_base,trim(axial_track_path),2,2,0)
  call B2J_REQUIRE_ASSOCIATED(axial_base,'real axial XSM')
  call B2J_REQUIRE_ASSOCIATED(archive_base,'real archive XSM')
  call B2J_REQUIRE_ASSOCIATED(axial_track_base,'real axial-track XSM')

  call B2J_BUILD_CLOSED_PAIR(axial_base,archive_base,axial_track_base, &
      axial_closed,archive_closed,b2c_calls,b2i_calls)
  call LOAD_INDEPENDENT_ORACLE()

  b2j_calls=0
  rejection_count=0
  reconstruction_slices=B2J_NGRP*B2J_NSNAP
  region_bit_checks=0
  nonregion_bit_checks=0
  mirror_bit_checks=0
  leakage_bit_checks=0
  deep_copy_checks=0
  replacement_checks=0
  source_absences=0
  qfiss_absences=0
  system_absences=0
  fresh_zero_write_rejections=0
  collision_rejections=0

  call RUN_POSITIVE()
  call RUN_REJECTION(1)
  call RUN_REJECTION(2)
  call RUN_REJECTION(3)
  call RUN_REJECTION(4)
  call RUN_REJECTION(5)
  call RUN_REJECTION(6)
  call RUN_REJECTION(7)
  call RUN_REJECTION(8)
  call RUN_REJECTION(9)
  call RUN_REJECTION(10)
  call RUN_REJECTION(11)
  call RUN_REJECTION(12)
  call VERIFY_INPUT_PAIR_UNCHANGED()

  if (b2j_calls /= NREJECTION+1) error stop 'B2J call inventory differs'
  if (rejection_count /= NREJECTION) &
    error stop 'B2J rejection inventory differs'
  if (fresh_zero_write_rejections /= NREJECTION-1) &
    error stop 'fresh zero-write rejection inventory differs'
  if (collision_rejections /= 1) &
    error stop 'collision rejection inventory differs'
  if (reconstruction_slices /= B2J_NGRP*B2J_NSNAP) &
    error stop 'independent reconstruction inventory differs'
  if (region_bit_checks /= B2J_NREG*B2J_NGRP*B2J_NSNAP) &
    error stop 'region bit-check inventory differs'
  if (nonregion_bit_checks /= &
      (B2J_NUNKNO-B2J_NREG)*B2J_NGRP*B2J_NSNAP) &
    error stop 'non-region bit-check inventory differs'
  if (mirror_bit_checks /= B2J_NUNKNO*B2J_NGRP*B2J_NSNAP) &
    error stop 'mirror bit-check inventory differs'
  if (leakage_bit_checks /= B2J_NGRP*B2J_NSNAP) &
    error stop 'leakage closure inventory differs'
  if (deep_copy_checks /= 2*B2J_NSNAP) &
    error stop 'deep-copy inventory differs'
  if (replacement_checks /= B2J_NSNAP) &
    error stop 'B2H replacement inventory differs'
  if (source_absences /= 2*B2J_NSNAP) &
    error stop 'source absence inventory differs'
  if (qfiss_absences /= 2*B2J_NSNAP) &
    error stop 'QFISS absence inventory differs'
  if (system_absences /= 1) error stop 'SYSTEM absence inventory differs'

  call LCMCL(archive_closed,2)
  call LCMCL(axial_closed,2)
  call LCMCL(axial_track_base,1)
  call LCMCL(archive_base,1)
  call LCMCL(axial_base,1)

  write(*,'(A)') 'B2J ARCHIVE-PROJECTION PASS'
  write(*,'(A,I0,A,I0,A,I0)') 'B2J CALLS=',b2j_calls, &
      ' COMMITS=1 REJECTIONS=',rejection_count
  write(*,'(A,I0,A,I0)') 'B2J FRESH-ZERO-WRITE-REJECTIONS=', &
      fresh_zero_write_rejections,' COLLISION-NO-NEW-WRITES=', &
      collision_rejections
  write(*,'(A,I0,A,I0)') 'B2J INDEPENDENT-B*A-SLICES=', &
      reconstruction_slices,' AX-L-LEAKAGE-BITS=',leakage_bit_checks
  write(*,'(A,I0,A,I0,A,I0)') 'B2J REGION64-BITS=',region_bit_checks, &
      ' NONREGION64-BITS=',nonregion_bit_checks, &
      ' MIRROR32-BITS=',mirror_bit_checks
  write(*,'(A,I0,A,I0)') 'B2J TWO-LIST-DEEP-COPIES=',deep_copy_checks, &
      ' B2H-REPLACEMENTS=',replacement_checks
  write(*,'(A,I0,A,I0,A,I0)') 'B2J PLANE-SOURCE-ABSENCES=', &
      source_absences,' PLANE-QFISS-ABSENCES=',qfiss_absences, &
      ' ARCHIVE-SYSTEM-ABSENCES=',system_absences
  write(*,'(A,I0,A,I0,A,I0)') 'B2J PRODUCTION-B2C-CALLS=',b2c_calls, &
      ' B2I-CALLS=',b2i_calls,' B2H-COMMITTED-PLANES=',B2J_NSNAP
  write(*,'(A)') &
      'B2J REAL-XSM-INPUTS=3 DRAGON-EXECUTIONS=0 TRANSPORT-SOLVES=0'
  write(*,'(A)') &
      'B2J SYSTEM=ABSENT SOURCE=ABSENT QFISS=NOT-BUILT CONT=NOT-EXECUTED'

contains

  subroutine LOAD_INDEPENDENT_ORACLE()
    integer :: dims(4), ig, ip, ir, a, nmode, index_b, index_a
    integer :: length, record_type
    real(real64) :: value
    real(real64) :: group64(B2J_NUNKNO)
    type(c_ptr) :: tracks, fluxes, track, plane, authority
    type(c_ptr) :: authority_flux, authority_source

    call B2J_REQUIRE_CHARACTER(axial_closed,'SPOT-X-STATE',12,'CLOSED')
    call B2J_REQUIRE_RECORD(axial_closed,'SPOT-X-DIMS',4,1)
    call B2J_REQUIRE_RECORD(axial_closed,'SPOT-X-RANK',B2J_NGRP,1)
    call B2J_REQUIRE_RECORD(axial_closed,'SPOT-X-OFF',B2J_NGRP+1,1)
    call B2J_REQUIRE_RECORD(axial_closed,'SPOT-X-BOFF',B2J_NGRP+1,1)
    call LCMGET(axial_closed,'SPOT-X-DIMS',dims)
    if (any(dims(1:3) /= [1,B2J_NGRP,B2J_NSNAP])) &
      error stop 'canonical dimensions differ'
    allocate(rank(B2J_NGRP),offset(B2J_NGRP+1), &
        basis_offset(B2J_NGRP+1))
    call LCMGET(axial_closed,'SPOT-X-RANK',rank)
    call LCMGET(axial_closed,'SPOT-X-OFF',offset)
    call LCMGET(axial_closed,'SPOT-X-BOFF',basis_offset)
    call B2J_REQUIRE_RECORD(axial_closed,'SPOT-X-BASIS', &
        basis_offset(B2J_NGRP+1),2)
    call B2J_REQUIRE_RECORD(axial_closed,'SPOT-X-A',dims(4),4)
    allocate(basis32(basis_offset(B2J_NGRP+1)))
    allocate(coordinates64(dims(4)))
    allocate(canonical_leak64(B2J_NGRP*B2J_NSNAP))
    allocate(projected64(B2J_NREG,B2J_NGRP,B2J_NSNAP))
    call LCMGET(axial_closed,'SPOT-X-BASIS',basis32)
    call LCMGET(axial_closed,'SPOT-X-A',coordinates64)
    call LCMGET(axial_closed,'SPOT-X-L',canonical_leak64)
    call LCMGET(axial_closed,'SPOT-X-RHO',canonical_rho64)
    call LCMGET(archive_closed,'SPOT-ITER-K',archive_keff64)
    if (.not. all(ieee_is_finite(basis32)) .or. &
        .not. all(ieee_is_finite(coordinates64)) .or. &
        .not. all(ieee_is_finite(canonical_leak64))) &
      error stop 'canonical reconstruction payload is nonfinite'

    projected64=0.0_real64
    do ig=1,B2J_NGRP
      nmode=rank(ig)
      do ip=1,B2J_NSNAP
        do ir=1,B2J_NREG
          value=0.0_real64
          do a=1,nmode
            index_b=basis_offset(ig)+(a-1)*B2J_NREG+ir
            index_a=offset(ig)+(ip-1)*nmode+a
            value=value+real(basis32(index_b),real64)* &
                coordinates64(index_a)
          end do
          projected64(ir,ig,ip)=value
        end do
      end do
    end do
    if (.not. all(ieee_is_finite(projected64)) .or. &
        any(projected64 <= 0.0_real64)) &
      error stop 'independent B*A oracle is not positive finite'

    allocate(keyflx(B2J_NREG,B2J_NSNAP))
    allocate(seed_leak32(B2J_NGRP,B2J_NSNAP))
    allocate(seed_flux64(B2J_NUNKNO,B2J_NGRP,B2J_NSNAP))
    allocate(seed_source64(B2J_NUNKNO,B2J_NGRP,B2J_NSNAP))
    tracks=LCMGID(archive_closed,'TRACK')
    fluxes=LCMGID(archive_closed,'FLUX')
    call B2J_REQUIRE_ASSOCIATED(tracks,'closed TRACK list')
    call B2J_REQUIRE_ASSOCIATED(fluxes,'closed FLUX list')
    do ip=1,B2J_NSNAP
      track=LCMGIL(tracks,ip)
      plane=LCMGIL(fluxes,ip)
      call B2J_REQUIRE_RECORD(track,'KEYFLX$ANIS',B2J_NREG,1)
      call LCMGET(track,'KEYFLX$ANIS',keyflx(:,ip))
      call REQUIRE_VALID_KEY_MAP(keyflx(:,ip))
      call B2J_REQUIRE_RECORD(plane,'SPOT-LEAK1D',B2J_NGRP,2)
      call LCMGET(plane,'SPOT-LEAK1D',seed_leak32(:,ip))
      do ig=1,B2J_NGRP
        if (B2J_BITS64(real(seed_leak32(ig,ip),real64)) /= &
            B2J_BITS64(canonical_leak64((ip-1)*B2J_NGRP+ig))) &
          error stop 'sealed leakage is not the canonical AX slice'
      end do
      authority=LCMGID(plane,'SPOT-R64')
      authority_flux=LCMGID(authority,'FLUX')
      authority_source=LCMGID(authority,'SOUR')
      call B2J_REQUIRE_ASSOCIATED(authority_flux,'seed authority FLUX')
      call B2J_REQUIRE_ASSOCIATED(authority_source,'seed authority SOUR')
      do ig=1,B2J_NGRP
        call LCMLEL(authority_flux,ig,length,record_type)
        if (length /= B2J_NUNKNO .or. record_type /= 4) &
          error stop 'seed authority FLUX schema differs'
        call LCMGDL(authority_flux,ig,group64)
        seed_flux64(:,ig,ip)=group64
        call LCMLEL(authority_source,ig,length,record_type)
        if (length /= B2J_NUNKNO .or. record_type /= 4) &
          error stop 'seed authority SOUR schema differs'
        call LCMGDL(authority_source,ig,group64)
        seed_source64(:,ig,ip)=group64
      end do
    end do
  end subroutine LOAD_INDEPENDENT_ORACLE


  subroutine RUN_POSITIVE()
    integer :: status
    type(c_ptr) :: output

    call LCMOP(output,'B2J-POS',0,1,0)
    call B2J_REQUIRE_EMPTY_ROOT(output)
    b2j_calls=b2j_calls+1
    call SPOR64_B2J_PROJECT_ARCHIVE(output,axial_closed, &
        axial_track_base,archive_closed,status)
    if (status /= SPOR64_B2J_ARCHIVE_PROJECTED) &
      error stop 'valid B2i pair did not project'
    call VERIFY_PROJECTED_ARCHIVE(output)
    call VERIFY_INPUT_PAIR_UNCHANGED()
    call LCMCL(output,2)
  end subroutine RUN_POSITIVE


  subroutine VERIFY_PROJECTED_ARCHIVE(output)
    type(c_ptr), intent(in) :: output
    integer :: listdim, nplane, epoch, ip
    real(real64) :: rho, output_keff
    type(c_ptr) :: authority
    type(c_ptr) :: input_tracks, input_libraries, input_fluxes
    type(c_ptr) :: output_tracks, output_libraries, output_fluxes
    type(c_ptr) :: input_item, output_item

    call B2J_REQUIRE_EXACT_INVENTORY(output, &
        [character(len=12) :: 'SIGNATURE','LISTDIM','SPOT-ITER-K', &
         'TRACK','MICROLIB2','FLUX','SPOT-R64'])
    call B2J_REQUIRE_CHARACTER(output,'SIGNATURE',12,'L_ARCHIVE')
    call B2J_REQUIRE_RECORD(output,'LISTDIM',1,1)
    call LCMGET(output,'LISTDIM',listdim)
    if (listdim /= B2J_NSNAP) error stop 'projected plane count differs'
    call LCMGET(output,'SPOT-ITER-K',output_keff)
    if (B2J_BITS64(output_keff) /= B2J_BITS64(archive_keff64)) &
      error stop 'projected archive K bits differ'
    call B2J_REQUIRE_ABSENT(output,'SYSTEM')
    system_absences=system_absences+1

    authority=LCMGID(output,'SPOT-R64')
    call B2J_REQUIRE_EXACT_INVENTORY(authority, &
        [character(len=12) :: 'RHO','NPLANE','STATE','EPOCH'])
    call B2J_REQUIRE_CHARACTER(authority,'STATE',12,'PROJECTED')
    call LCMGET(authority,'RHO',rho)
    call LCMGET(authority,'NPLANE',nplane)
    call LCMGET(authority,'EPOCH',epoch)
    if (B2J_BITS64(rho) /= B2J_BITS64(canonical_rho64)) &
      error stop 'projected root RHO bits differ'
    if (nplane /= B2J_NSNAP .or. epoch /= 1) &
      error stop 'projected root lifecycle differs'

    input_tracks=LCMGID(archive_closed,'TRACK')
    input_libraries=LCMGID(archive_closed,'MICROLIB2')
    input_fluxes=LCMGID(archive_closed,'FLUX')
    output_tracks=LCMGID(output,'TRACK')
    output_libraries=LCMGID(output,'MICROLIB2')
    output_fluxes=LCMGID(output,'FLUX')
    call B2J_REQUIRE_DISTINCT(input_tracks,output_tracks,'TRACK list')
    call B2J_REQUIRE_DISTINCT(input_libraries,output_libraries, &
        'MICROLIB2 list')
    call B2J_REQUIRE_DISTINCT(input_fluxes,output_fluxes,'FLUX list')

    do ip=1,B2J_NSNAP
      input_item=LCMGIL(input_tracks,ip)
      output_item=LCMGIL(output_tracks,ip)
      call VERIFY_TRACK_DEEP_COPY(input_item,output_item,1000+ip)
      deep_copy_checks=deep_copy_checks+1

      input_item=LCMGIL(input_libraries,ip)
      output_item=LCMGIL(output_libraries,ip)
      call VERIFY_LIBRARY_DEEP_COPY(input_item,output_item,2000+ip)
      deep_copy_checks=deep_copy_checks+1

      input_item=LCMGIL(input_fluxes,ip)
      output_item=LCMGIL(output_fluxes,ip)
      call B2J_REQUIRE_DISTINCT(input_item,output_item,'FLUX plane')
      call B2J_REQUIRE_RECORD(input_item,'B2I-SENT',1,1)
      call B2J_REQUIRE_ABSENT(output_item,'B2I-SENT')
      call B2J_REQUIRE_ABSENT(output_item,'B2I-DEEP')
      replacement_checks=replacement_checks+1
      call VERIFY_PROJECTED_PLANE(output_item,input_item,ip)
    end do
  end subroutine VERIFY_PROJECTED_ARCHIVE


  subroutine VERIFY_TRACK_DEEP_COPY(input,output,sentinel)
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
  end subroutine VERIFY_TRACK_DEEP_COPY


  subroutine VERIFY_LIBRARY_DEEP_COPY(input,output,sentinel)
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
    call B2J_COMPARE_INTEGER_RECORD(input_macro,output_macro,'STATE-VECTOR')
    input_groups=LCMGID(input_macro,'GROUP')
    output_groups=LCMGID(output_macro,'GROUP')
    call B2J_REQUIRE_DISTINCT(input_groups,output_groups,'MACROLIB GROUP')
    do ig=1,B2J_NGRP
      call B2J_REQUIRE_DIRECTORY_ITEM(input_groups,ig)
      call B2J_REQUIRE_DIRECTORY_ITEM(output_groups,ig)
    end do
    call B2J_VERIFY_DEEP_SENTINEL(input,output,sentinel)
  end subroutine VERIFY_LIBRARY_DEEP_COPY


  subroutine VERIFY_PROJECTED_PLANE(output,seed,ip)
    type(c_ptr), intent(in) :: output, seed
    integer, intent(in) :: ip
    integer :: ig, iu, ir, mapped_region, length, record_type, epoch
    real(real64) :: rho, expected64, found64(B2J_NUNKNO)
    real(real32) :: mirror32(B2J_NUNKNO), leakage32(B2J_NGRP)
    real(real32) :: seed_mirror32(B2J_NUNKNO)
    type(c_ptr) :: authority, authority_flux, mirror_flux, seed_mirror_flux

    call B2J_REQUIRE_EXACT_INVENTORY(output, &
        [character(len=12) :: 'SPOT-R64','FLUX','SIGNATURE', &
         'STATE-VECTOR','EPS-CONVERGE','IMERGE-LEAK','KEYFLX','OPTION', &
         'LINK.MACRO','LINK.TRACK','LINK.SYSTEM','SPOT-LEAK1D'])
    call B2J_REQUIRE_ABSENT(output,'SOUR')
    source_absences=source_absences+1
    call B2J_REQUIRE_ABSENT(output,'QFISS')
    qfiss_absences=qfiss_absences+1
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
    call B2J_REQUIRE_ABSENT(authority,'SOUR')
    source_absences=source_absences+1
    call B2J_REQUIRE_ABSENT(authority,'QFISS')
    qfiss_absences=qfiss_absences+1
    call B2J_REQUIRE_ABSENT(authority,'SPOT-QFISS')
    call B2J_REQUIRE_ABSENT(authority,'DSOUR')
    call LCMGET(authority,'RHO',rho)
    call LCMGET(authority,'EPOCH',epoch)
    if (B2J_BITS64(rho) /= B2J_BITS64(canonical_rho64) .or. epoch /= 1) &
      error stop 'projected plane lifecycle differs'
    call LCMGET(output,'SPOT-LEAK1D',leakage32)
    do ig=1,B2J_NGRP
      if (B2J_BITS32(leakage32(ig)) /= &
          B2J_BITS32(real(canonical_leak64( &
          (ip-1)*B2J_NGRP+ig),real32))) &
        error stop 'projected leakage mirror bits differ'
      if (B2J_BITS64(real(leakage32(ig),real64)) /= &
          B2J_BITS64(canonical_leak64((ip-1)*B2J_NGRP+ig))) &
        error stop 'projected leakage does not close with AX L'
      leakage_bit_checks=leakage_bit_checks+1
    end do

    authority_flux=LCMGID(authority,'FLUX')
    mirror_flux=LCMGID(output,'FLUX')
    seed_mirror_flux=LCMGID(seed,'FLUX')
    call B2J_REQUIRE_ASSOCIATED(authority_flux,'projected authority FLUX')
    call B2J_REQUIRE_ASSOCIATED(mirror_flux,'projected mirror FLUX')
    call B2J_REQUIRE_ASSOCIATED(seed_mirror_flux,'seed mirror FLUX')
    do ig=1,B2J_NGRP
      call LCMLEL(authority_flux,ig,length,record_type)
      if (length /= B2J_NUNKNO .or. record_type /= 4) &
        error stop 'projected authority FLUX schema differs'
      call LCMLEL(mirror_flux,ig,length,record_type)
      if (length /= B2J_NUNKNO .or. record_type /= 2) &
        error stop 'projected mirror FLUX schema differs'
      call LCMGDL(authority_flux,ig,found64)
      call LCMGDL(mirror_flux,ig,mirror32)
      call LCMGDL(seed_mirror_flux,ig,seed_mirror32)
      do iu=1,B2J_NUNKNO
        mapped_region=0
        do ir=1,B2J_NREG
          if (keyflx(ir,ip) == iu) mapped_region=ir
        end do
        if (mapped_region > 0) then
          expected64=projected64(mapped_region,ig,ip)
          region_bit_checks=region_bit_checks+1
        else
          expected64=seed_flux64(iu,ig,ip)
          nonregion_bit_checks=nonregion_bit_checks+1
          if (B2J_BITS64(found64(iu)) == &
              B2J_BITS64(real(seed_mirror32(iu),real64))) &
            error stop 'non-region value came from REAL32 mirror'
        end if
        if (B2J_BITS64(found64(iu)) /= B2J_BITS64(expected64)) &
          error stop 'projected authority FLUX bits differ'
        if (B2J_BITS32(mirror32(iu)) /= &
            B2J_BITS32(real(found64(iu),real32))) &
          error stop 'projected mirror is not authority downcast'
        mirror_bit_checks=mirror_bit_checks+1
      end do
    end do
  end subroutine VERIFY_PROJECTED_PLANE


  subroutine RUN_REJECTION(case_id)
    integer, intent(in) :: case_id
    character(len=12) :: axial_name, archive_name, output_name
    integer :: status, marker
    logical :: owns_axial, owns_archive
    type(c_ptr) :: axial_input, archive_input, output

    axial_input=axial_closed
    archive_input=archive_closed
    owns_axial=.false.
    owns_archive=.false.
    write(axial_name,'("B2J-XA",I2.2)') case_id
    write(archive_name,'("B2J-XR",I2.2)') case_id
    write(output_name,'("B2J-XO",I2.2)') case_id

    select case(case_id)
    case(1)
      continue
    case(2:4)
      call B2J_CLONE_OBJECT(axial_closed,axial_name,axial_input)
      owns_axial=.true.
      call MUTATE_AXIAL_REJECTION(axial_input,case_id)
    case(5:12)
      call B2J_CLONE_OBJECT(archive_closed,archive_name,archive_input)
      owns_archive=.true.
      call MUTATE_ARCHIVE_REJECTION(archive_input,case_id)
    case default
      error stop 'unknown B2J rejection case'
    end select

    call LCMOP(output,output_name,0,1,0)
    call B2J_REQUIRE_EMPTY_ROOT(output)
    if (case_id == 1) then
      marker=271828
      call LCMPUT(output,'SENTINEL',1,1,marker)
    end if
    b2j_calls=b2j_calls+1
    call SPOR64_B2J_PROJECT_ARCHIVE(output,axial_input, &
        axial_track_base,archive_input,status)
    if (status /= SPOR64_B2J_ADMISSION_FAILED) &
      error stop 'invalid B2i pair was accepted'
    if (case_id == 1) then
      call B2J_REQUIRE_ONLY_SENTINEL(output,271828)
      collision_rejections=collision_rejections+1
    else
      call B2J_REQUIRE_EMPTY_ROOT(output)
      fresh_zero_write_rejections=fresh_zero_write_rejections+1
    end if
    rejection_count=rejection_count+1

    call LCMCL(output,2)
    if (owns_archive) call LCMCL(archive_input,2)
    if (owns_axial) call LCMCL(axial_input,2)
  end subroutine RUN_REJECTION


  subroutine MUTATE_AXIAL_REJECTION(axial,case_id)
    type(c_ptr), intent(in) :: axial
    integer, intent(in) :: case_id
    integer :: epoch
    real(real64) :: rho, leakage(B2J_NGRP*B2J_NSNAP)

    select case(case_id)
    case(2)
      epoch=1
      call LCMPUT(axial,'SPOT-X-EPOCH',1,1,epoch)
    case(3)
      call LCMGET(axial,'SPOT-X-RHO',rho)
      rho=nearest(rho,1.0_real64)
      call LCMPUT(axial,'SPOT-X-RHO',1,4,rho)
    case(4)
      call LCMGET(axial,'SPOT-X-L',leakage)
      leakage(1)=nearest(leakage(1),1.0_real64)
      call LCMPUT(axial,'SPOT-X-L',size(leakage),4,leakage)
    case default
      error stop 'unknown axial rejection mutation'
    end select
  end subroutine MUTATE_AXIAL_REJECTION


  subroutine MUTATE_ARCHIVE_REJECTION(archive,case_id)
    type(c_ptr), intent(in) :: archive
    integer, intent(in) :: case_id
    character(len=12) :: state
    integer :: marker, snapshot, macro_state(B2J_NSTATE)
    integer :: length, record_type
    real(real32) :: volume(B2J_NREG), eps(5)
    real(real64) :: group64(B2J_NUNKNO)
    type(c_ptr) :: root_authority, list, item, macro, authority, source

    select case(case_id)
    case(5)
      marker=161803
      call LCMPUT(archive,'EXTRA',1,1,marker)
    case(6)
      root_authority=LCMGID(archive,'SPOT-R64')
      state='PROJECTED'
      call LCMPTC(root_authority,'STATE',12,state)
    case(7)
      list=LCMGID(archive,'MICROLIB2')
      item=LCMGIL(list,1)
      macro=LCMGID(item,'MACROLIB')
      call LCMGET(macro,'STATE-VECTOR',macro_state)
      macro_state(13)=1
      call LCMPUT(macro,'STATE-VECTOR',B2J_NSTATE,1,macro_state)
    case(8)
      list=LCMGID(archive,'SYSTEM')
      item=LCMGIL(list,2)
      snapshot=1
      call LCMPUT(item,'SPOT-L1-SNAP',1,1,snapshot)
    case(9)
      list=LCMGID(archive,'TRACK')
      item=LCMGIL(list,2)
      call LCMGET(item,'VOLUME',volume)
      volume(1)=nearest(volume(1),1.0_real32)
      call LCMPUT(item,'VOLUME',B2J_NREG,2,volume)
    case(10)
      list=LCMGID(archive,'FLUX')
      item=LCMGIL(list,1)
      authority=LCMGID(item,'SPOT-R64')
      marker=314159
      call LCMPUT(authority,'QFISS',1,1,marker)
    case(11)
      ! B2J preflight admits this schema; B2H rejects plane 2 after plane 1
      ! was staged.  The final caller output must nevertheless remain empty.
      list=LCMGID(archive,'FLUX')
      item=LCMGIL(list,2)
      call LCMGET(item,'EPS-CONVERGE',eps)
      eps(1)=nearest(eps(1),1.0_real32)
      call LCMPUT(item,'EPS-CONVERGE',5,2,eps)
    case(12)
      ! The nonfinite source is detected by B2H only on plane 3, proving
      ! that both earlier private stages are destroyed on rejection.
      list=LCMGID(archive,'FLUX')
      item=LCMGIL(list,3)
      authority=LCMGID(item,'SPOT-R64')
      source=LCMGID(authority,'SOUR')
      call LCMLEL(source,1,length,record_type)
      if (length /= B2J_NUNKNO .or. record_type /= 4) &
        error stop 'source mutation target schema differs'
      call LCMGDL(source,1,group64)
      group64(1)=ieee_value(0.0_real64,ieee_quiet_nan)
      call LCMPDL(source,1,B2J_NUNKNO,4,group64)
    case default
      error stop 'unknown archive rejection mutation'
    end select
  end subroutine MUTATE_ARCHIVE_REJECTION


  subroutine VERIFY_INPUT_PAIR_UNCHANGED()
    integer :: epoch, nplane, ip, ig, iu
    real(real64) :: rho, group64(B2J_NUNKNO), found_keff
    real(real64), allocatable :: found_coordinates(:), found_leakage(:)
    type(c_ptr) :: root_authority, tracks, libraries, systems, fluxes
    type(c_ptr) :: plane, authority, flux, source

    call B2J_REQUIRE_CHARACTER(axial_closed,'SPOT-X-STATE',12,'CLOSED')
    call LCMGET(axial_closed,'SPOT-X-EPOCH',epoch)
    if (epoch /= 0) error stop 'input AX epoch changed'
    allocate(found_coordinates(size(coordinates64)))
    allocate(found_leakage(size(canonical_leak64)))
    call LCMGET(axial_closed,'SPOT-X-A',found_coordinates)
    call LCMGET(axial_closed,'SPOT-X-L',found_leakage)
    call LCMGET(axial_closed,'SPOT-X-RHO',rho)
    if (any(B2J_BITS64(found_coordinates) /= B2J_BITS64(coordinates64))) &
      error stop 'input AX coordinates changed'
    if (any(B2J_BITS64(found_leakage) /= B2J_BITS64(canonical_leak64))) &
      error stop 'input AX leakage changed'
    if (B2J_BITS64(rho) /= B2J_BITS64(canonical_rho64)) &
      error stop 'input AX RHO changed'

    call B2J_REQUIRE_EXACT_INVENTORY(archive_closed, &
        [character(len=12) :: 'SIGNATURE','LISTDIM','SPOT-ITER-K', &
         'TRACK','MICROLIB2','SYSTEM','FLUX','SPOT-R64'])
    call LCMGET(archive_closed,'SPOT-ITER-K',found_keff)
    if (B2J_BITS64(found_keff) /= B2J_BITS64(archive_keff64)) &
      error stop 'input archive K changed'
    root_authority=LCMGID(archive_closed,'SPOT-R64')
    call B2J_REQUIRE_CHARACTER(root_authority,'STATE',12,'CLOSED')
    call LCMGET(root_authority,'NPLANE',nplane)
    call LCMGET(root_authority,'EPOCH',epoch)
    call LCMGET(root_authority,'RHO',rho)
    if (nplane /= B2J_NSNAP .or. epoch /= 0 .or. &
        B2J_BITS64(rho) /= B2J_BITS64(canonical_rho64)) &
      error stop 'input archive root lifecycle changed'

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
      call LCMGET(authority,'RHO',rho)
      if (epoch /= 0 .or. B2J_BITS64(rho) /= B2J_BITS64(canonical_rho64)) &
        error stop 'input plane lifecycle changed'
      flux=LCMGID(authority,'FLUX')
      source=LCMGID(authority,'SOUR')
      do ig=1,B2J_NGRP
        call LCMGDL(flux,ig,group64)
        do iu=1,B2J_NUNKNO
          if (B2J_BITS64(group64(iu)) /= &
              B2J_BITS64(seed_flux64(iu,ig,ip))) &
            error stop 'input authority FLUX changed'
        end do
        call LCMGDL(source,ig,group64)
        do iu=1,B2J_NUNKNO
          if (B2J_BITS64(group64(iu)) /= &
              B2J_BITS64(seed_source64(iu,ig,ip))) &
            error stop 'input authority SOUR changed'
        end do
      end do
    end do
  end subroutine VERIFY_INPUT_PAIR_UNCHANGED


  subroutine REQUIRE_VALID_KEY_MAP(map)
    integer, intent(in) :: map(B2J_NREG)
    logical :: seen(B2J_NUNKNO)
    integer :: ir

    seen=.false.
    do ir=1,B2J_NREG
      if (map(ir) < 1 .or. map(ir) > B2J_NUNKNO) &
        error stop 'TRACK key map is out of range'
      if (seen(map(ir))) error stop 'TRACK key map is not unique'
      seen(map(ir))=.true.
    end do
  end subroutine REQUIRE_VALID_KEY_MAP

end program TEST_B2J_ARCHIVE_PROJECTION
