program TEST_B2K_SYSTEM_ASSEMBLY
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_quiet_nan, ieee_value
  use SPOR64_B2K, only : SPOR64_B2K_ADMISSION_FAILED, &
      SPOR64_B2K_ARCHIVE_ASSEMBLED, SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE
  use B2J_FIXTURE_SUPPORT
  use B2K_FIXTURE_SUPPORT
  implicit none

  integer, parameter :: NREJECTION=20
  character(len=1024) :: axial_path, archive_path, axial_track_path
  integer :: b2c_calls, b2i_calls, b2j_calls, b2k_calls
  integer :: restored_xs_bits, leakage_checks, txsc_checks
  integer :: s0phys_checks, s0used_checks, response_copy_bits
  integer :: flux64_copy_bits, flux32_copy_bits, rejection_count
  integer :: fresh_zero_write_rejections, collision_rejections
  integer :: post_commit_witnesses
  type(c_ptr) :: axial_base, archive_base, axial_track_base
  type(c_ptr) :: axial_closed, archive_closed, projected
  type(c_ptr) :: systems(B2J_NSNAP)

  if (command_argument_count() /= 3) error stop &
    'expected state1_axial.xsm, state1_snapshots.xsm, and track paths'
  call get_command_argument(1,axial_path)
  call get_command_argument(2,archive_path)
  call get_command_argument(3,axial_track_path)

  call LCMOP(axial_base,trim(axial_path),2,2,0)
  call LCMOP(archive_base,trim(archive_path),2,2,0)
  call LCMOP(axial_track_base,trim(axial_track_path),2,2,0)
  call B2J_REQUIRE_ASSOCIATED(axial_base,'real axial XSM')
  call B2J_REQUIRE_ASSOCIATED(archive_base,'real archive XSM')
  call B2J_REQUIRE_ASSOCIATED(axial_track_base,'real axial-track XSM')

  call B2K_PREPARE_PROJECTED_INPUT(axial_base,archive_base, &
      axial_track_base,axial_closed,archive_closed,projected, &
      b2c_calls,b2i_calls,b2j_calls,restored_xs_bits)
  call B2K_BUILD_FRESH_SYSTEMS(projected,systems)
  call B2K_REQUIRE_FORMULA_WITNESS()
  call B2K_VERIFY_CANDIDATE_FORMULAS(projected,systems, &
      leakage_checks,txsc_checks,s0phys_checks,s0used_checks)

  b2k_calls=0
  response_copy_bits=0
  flux64_copy_bits=0
  flux32_copy_bits=0
  rejection_count=0
  fresh_zero_write_rejections=0
  collision_rejections=0
  post_commit_witnesses=0

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
  call RUN_REJECTION(13)
  call RUN_REJECTION(14)
  call RUN_REJECTION(15)
  call RUN_REJECTION(16)
  call RUN_REJECTION(17)
  call RUN_REJECTION(18)
  call RUN_REJECTION(19)
  call RUN_REJECTION(20)
  call VERIFY_INPUTS_UNCHANGED()

  if (b2c_calls /= 3 .or. b2i_calls /= 1 .or. b2j_calls /= 1) &
    error stop 'upstream production-call inventory differs'
  if (b2k_calls /= NREJECTION+1) error stop 'B2K call inventory differs'
  if (rejection_count /= NREJECTION) &
    error stop 'B2K rejection inventory differs'
  if (fresh_zero_write_rejections /= NREJECTION-1) &
    error stop 'fresh zero-write rejection inventory differs'
  if (collision_rejections /= 1) &
    error stop 'collision rejection inventory differs'
  if (restored_xs_bits /= B2K_RESTORED_XS_BITS) &
    error stop 'restored cross-section inventory differs'
  if (leakage_checks /= B2J_NSNAP*B2J_NGRP) &
    error stop 'leakage formula inventory differs'
  if (txsc_checks /= B2J_NSNAP*B2J_NGRP*B2K_NSYSMIX .or. &
      s0phys_checks /= B2J_NSNAP*B2J_NGRP*B2K_NSYSMIX .or. &
      s0used_checks /= B2J_NSNAP*B2J_NGRP*B2K_NSYSMIX) &
    error stop 'system cross-section formula inventory differs'
  if (response_copy_bits /= 179820) &
    error stop 'complete response deep-copy inventory differs'
  if (post_commit_witnesses /= B2K_NGROUP_RECORDS) &
    error stop 'post-commit independence witness inventory differs'
  if (flux64_copy_bits /= B2J_NSNAP*B2J_NGRP*B2J_NUNKNO .or. &
      flux32_copy_bits /= B2J_NSNAP*B2J_NGRP*B2J_NUNKNO) &
    error stop 'projected FLUX deep-copy inventory differs'

  call B2K_CLOSE_SYSTEMS(systems)
  call LCMCL(projected,2)
  call LCMCL(archive_closed,2)
  call LCMCL(axial_closed,2)
  call LCMCL(axial_track_base,1)
  call LCMCL(archive_base,1)
  call LCMCL(axial_base,1)

  write(*,'(A)') 'B2K SYSTEM-ASSEMBLY PASS'
  write(*,'(A,I0,A,I0,A,I0)') 'B2K CALLS=',b2k_calls, &
      ' COMMITS=1 REJECTIONS=',rejection_count
  write(*,'(A,I0,A,I0)') 'B2K FRESH-ZERO-WRITE-REJECTIONS=', &
      fresh_zero_write_rejections,' COLLISION-NO-NEW-WRITES=', &
      collision_rejections
  write(*,'(A,I0,A,I0)') 'B2K RESTORED-REAL-XS-BITS=',restored_xs_bits, &
      ' PROJECTED-LEAKAGE-BITS=',leakage_checks
  write(*,'(A,I0,A,I0,A,I0)') 'B2K TXSC-BITS=',txsc_checks, &
      ' S0PHYS-BITS=',s0phys_checks,' S0USED-BITS=',s0used_checks
  write(*,'(A,I0)') 'B2K RESPONSE-DEEP-COPY-BITS=',response_copy_bits
  write(*,'(A,I0)') 'B2K POST-COMMIT-INDEPENDENCE-WITNESSES=', &
      post_commit_witnesses
  write(*,'(A,I0,A,I0)') 'B2K PROJECTED-FLUX64-BITS=', &
      flux64_copy_bits,' PROJECTED-FLUX32-BITS=',flux32_copy_bits
  write(*,'(A,I0,A,I0,A,I0)') 'B2K PRODUCTION-B2C-CALLS=',b2c_calls, &
      ' B2I-CALLS=',b2i_calls,' B2J-CALLS=',b2j_calls
  write(*,'(A)') &
      'B2K FRESH-SYSTEMS=3 OLD-SYSTEM-COPIES=0 FULL-SYSTEM-COPIES=3'
  write(*,'(A)') &
      'B2K REAL-XSM-INPUTS=3 DRAGON=0 ASM=0 TRANSPORT-SOLVES=0'
  write(*,'(A)') &
      'B2K QFISS=NOT-BUILT CONT=NOT-EXECUTED CONVERGENCE=NOT-EVALUATED'

contains

  subroutine RUN_POSITIVE()
    integer :: status
    type(c_ptr) :: output

    call LCMOP(output,'B2K-POS',0,1,0)
    call B2J_REQUIRE_EMPTY_ROOT(output)
    b2k_calls=b2k_calls+1
    call SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE(output,projected,systems,status)
    if (status /= SPOR64_B2K_ARCHIVE_ASSEMBLED) &
      error stop 'valid fresh SYSTEM set was not committed'
    call VERIFY_ASSEMBLED_ARCHIVE(output)
    call B2K_VERIFY_POST_COMMIT_INDEPENDENCE(systems(1), &
        LCMGIL(LCMGID(output,'SYSTEM'),1),post_commit_witnesses)
    call VERIFY_INPUTS_UNCHANGED()
    call LCMCL(output,2)
  end subroutine RUN_POSITIVE


  subroutine VERIFY_ASSEMBLED_ARCHIVE(output)
    type(c_ptr), intent(in) :: output
    integer :: ip, epoch, nplane
    real(real64) :: rho_in, rho_out
    type(c_ptr) :: root_in, root_out
    type(c_ptr) :: input_tracks, output_tracks
    type(c_ptr) :: input_libraries, output_libraries
    type(c_ptr) :: input_fluxes, output_fluxes, output_systems
    type(c_ptr) :: input_item, output_item, system_authority

    call B2J_REQUIRE_EXACT_INVENTORY(output, &
        [character(len=12) :: 'SIGNATURE','LISTDIM','SPOT-ITER-K', &
         'TRACK','MICROLIB2','FLUX','SYSTEM','SPOT-R64'])
    call B2J_COMPARE_CHARACTER_RECORD(projected,output,'SIGNATURE',12)
    call B2J_COMPARE_INTEGER_RECORD(projected,output,'LISTDIM')
    call B2J_COMPARE_REAL64_RECORD(projected,output,'SPOT-ITER-K')
    root_in=LCMGID(projected,'SPOT-R64')
    root_out=LCMGID(output,'SPOT-R64')
    call B2J_REQUIRE_EXACT_INVENTORY(root_out, &
        [character(len=12) :: 'RHO','NPLANE','STATE','EPOCH'])
    call B2J_REQUIRE_CHARACTER(root_out,'STATE',12,'ASSEMBLED')
    call LCMGET(root_in,'RHO',rho_in)
    call LCMGET(root_out,'RHO',rho_out)
    call LCMGET(root_out,'NPLANE',nplane)
    call LCMGET(root_out,'EPOCH',epoch)
    if (B2J_BITS64(rho_out) /= B2J_BITS64(rho_in)) &
      error stop 'assembled archive RHO bits differ'
    if (nplane /= B2J_NSNAP .or. epoch /= 1) &
      error stop 'assembled archive lifecycle differs'

    input_tracks=LCMGID(projected,'TRACK')
    output_tracks=LCMGID(output,'TRACK')
    input_libraries=LCMGID(projected,'MICROLIB2')
    output_libraries=LCMGID(output,'MICROLIB2')
    input_fluxes=LCMGID(projected,'FLUX')
    output_fluxes=LCMGID(output,'FLUX')
    output_systems=LCMGID(output,'SYSTEM')
    call B2J_REQUIRE_DISTINCT(input_tracks,output_tracks,'TRACK list')
    call B2J_REQUIRE_DISTINCT(input_libraries,output_libraries, &
        'MICROLIB2 list')
    call B2J_REQUIRE_DISTINCT(input_fluxes,output_fluxes,'FLUX list')
    do ip=1,B2J_NSNAP
      input_item=LCMGIL(input_tracks,ip)
      output_item=LCMGIL(output_tracks,ip)
      call B2J_VERIFY_DEEP_SENTINEL(input_item,output_item,1000+ip)
      input_item=LCMGIL(input_libraries,ip)
      output_item=LCMGIL(output_libraries,ip)
      call B2J_VERIFY_DEEP_SENTINEL(input_item,output_item,2000+ip)
      input_item=LCMGIL(input_fluxes,ip)
      output_item=LCMGIL(output_fluxes,ip)
      call VERIFY_PROJECTED_FLUX_COPY(input_item,output_item)
      output_item=LCMGIL(output_systems,ip)
      call B2K_VERIFY_SYSTEM_DEEP_COPY(systems(ip),output_item,ip, &
          response_copy_bits)
      system_authority=LCMGID(output_item,'SPOT-R64')
      call B2J_REQUIRE_EXACT_INVENTORY(system_authority, &
          [character(len=12) :: 'RHO','STATE','EPOCH'])
      call B2J_REQUIRE_CHARACTER(system_authority,'STATE',12,'ASSEMBLED')
      call LCMGET(system_authority,'RHO',rho_out)
      call LCMGET(system_authority,'EPOCH',epoch)
      if (B2J_BITS64(rho_out) /= B2J_BITS64(rho_in) .or. epoch /= 1) &
        error stop 'committed SYSTEM authority differs'
    end do
  end subroutine VERIFY_ASSEMBLED_ARCHIVE


  subroutine VERIFY_PROJECTED_FLUX_COPY(input,output)
    type(c_ptr), intent(in) :: input, output
    integer :: ig, length, record_type, epoch
    real(real32) :: input32(B2J_NUNKNO), output32(B2J_NUNKNO)
    real(real64) :: input64(B2J_NUNKNO), output64(B2J_NUNKNO)
    real(real64) :: rho_in, rho_out
    type(c_ptr) :: input_authority, output_authority
    type(c_ptr) :: input_flux, output_flux, input_mirror, output_mirror

    call B2J_REQUIRE_DISTINCT(input,output,'projected FLUX plane')
    call B2J_REQUIRE_EXACT_INVENTORY(output, &
        [character(len=12) :: 'SPOT-R64','FLUX','SIGNATURE', &
         'STATE-VECTOR','EPS-CONVERGE','IMERGE-LEAK','KEYFLX','OPTION', &
         'LINK.MACRO','LINK.TRACK','LINK.SYSTEM','SPOT-LEAK1D'])
    call B2J_COMPARE_CHARACTER_RECORD(input,output,'SIGNATURE',12)
    call B2J_COMPARE_CHARACTER_RECORD(input,output,'OPTION',4)
    call B2J_COMPARE_CHARACTER_RECORD(input,output,'LINK.MACRO',12)
    call B2J_COMPARE_CHARACTER_RECORD(input,output,'LINK.TRACK',12)
    call B2J_COMPARE_CHARACTER_RECORD(input,output,'LINK.SYSTEM',12)
    call B2J_COMPARE_INTEGER_RECORD(input,output,'STATE-VECTOR')
    call B2J_COMPARE_INTEGER_RECORD(input,output,'IMERGE-LEAK')
    call B2J_COMPARE_INTEGER_RECORD(input,output,'KEYFLX')
    call B2J_COMPARE_REAL32_RECORD(input,output,'EPS-CONVERGE')
    call B2J_COMPARE_REAL32_RECORD(input,output,'SPOT-LEAK1D')
    call B2J_REQUIRE_ABSENT(output,'SOUR')
    call B2J_REQUIRE_ABSENT(output,'QFISS')

    input_authority=LCMGID(input,'SPOT-R64')
    output_authority=LCMGID(output,'SPOT-R64')
    call B2J_REQUIRE_DISTINCT(input_authority,output_authority, &
        'projected FLUX authority')
    call B2J_REQUIRE_EXACT_INVENTORY(output_authority, &
        [character(len=12) :: 'RHO','FLUX','STATE','EPOCH'])
    call B2J_REQUIRE_CHARACTER(output_authority,'STATE',12,'PROJECTED')
    call LCMGET(input_authority,'RHO',rho_in)
    call LCMGET(output_authority,'RHO',rho_out)
    call LCMGET(output_authority,'EPOCH',epoch)
    if (B2J_BITS64(rho_out) /= B2J_BITS64(rho_in) .or. epoch /= 1) &
      error stop 'projected FLUX authority lifecycle changed'
    input_flux=LCMGID(input_authority,'FLUX')
    output_flux=LCMGID(output_authority,'FLUX')
    input_mirror=LCMGID(input,'FLUX')
    output_mirror=LCMGID(output,'FLUX')
    call B2J_REQUIRE_DISTINCT(input_flux,output_flux,'authority FLUX list')
    call B2J_REQUIRE_DISTINCT(input_mirror,output_mirror,'mirror FLUX list')
    do ig=1,B2J_NGRP
      call LCMLEL(input_flux,ig,length,record_type)
      if (length /= B2J_NUNKNO .or. record_type /= 4) &
        error stop 'input projected authority schema differs'
      call LCMGDL(input_flux,ig,input64)
      call LCMGDL(output_flux,ig,output64)
      if (any(B2J_BITS64(input64) /= B2J_BITS64(output64))) &
        error stop 'projected authority FLUX bits changed'
      flux64_copy_bits=flux64_copy_bits+B2J_NUNKNO
      call LCMGDL(input_mirror,ig,input32)
      call LCMGDL(output_mirror,ig,output32)
      if (any(B2J_BITS32(input32) /= B2J_BITS32(output32))) &
        error stop 'projected mirror FLUX bits changed'
      flux32_copy_bits=flux32_copy_bits+B2J_NUNKNO
    end do
  end subroutine VERIFY_PROJECTED_FLUX_COPY


  subroutine RUN_REJECTION(case_id)
    integer, intent(in) :: case_id
    character(len=12) :: output_name, clone_name
    integer :: status, marker
    logical :: owns_projected, owns_system
    type(c_ptr) :: projected_input, system_input(B2J_NSNAP)
    type(c_ptr) :: output, owned_candidate

    projected_input=projected
    system_input=systems
    owns_projected=.false.
    owns_system=.false.
    write(output_name,'("B2K-O",I2.2)') case_id
    write(clone_name,'("B2K-C",I2.2)') case_id

    select case(case_id)
    case(1)
      continue
    case(2:4,15:20)
      call B2J_CLONE_OBJECT(projected,clone_name,projected_input)
      owns_projected=.true.
      call MUTATE_PROJECTED(projected_input,case_id)
    case(5)
      system_input(2)=system_input(1)
    case(6:14)
      if (case_id == 14) then
        call B2J_CLONE_OBJECT(systems(3),clone_name,owned_candidate)
        system_input(3)=owned_candidate
      else
        call B2J_CLONE_OBJECT(systems(1),clone_name,owned_candidate)
        system_input(1)=owned_candidate
      end if
      owns_system=.true.
      call MUTATE_SYSTEM(owned_candidate,case_id)
    case default
      error stop 'unknown B2K rejection case'
    end select

    call LCMOP(output,output_name,0,1,0)
    call B2J_REQUIRE_EMPTY_ROOT(output)
    if (case_id == 1) then
      marker=271828
      call LCMPUT(output,'SENTINEL',1,1,marker)
    end if
    b2k_calls=b2k_calls+1
    call SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE(output,projected_input, &
        system_input,status)
    if (status /= SPOR64_B2K_ADMISSION_FAILED) &
      error stop 'invalid B2K input was accepted'
    if (case_id == 1) then
      call B2J_REQUIRE_ONLY_SENTINEL(output,271828)
      collision_rejections=collision_rejections+1
    else
      call B2J_REQUIRE_EMPTY_ROOT(output)
      fresh_zero_write_rejections=fresh_zero_write_rejections+1
    end if
    rejection_count=rejection_count+1

    call LCMCL(output,2)
    if (owns_system) call LCMCL(owned_candidate,2)
    if (owns_projected) call LCMCL(projected_input,2)
  end subroutine RUN_REJECTION


  subroutine MUTATE_PROJECTED(archive,case_id)
    type(c_ptr), intent(in) :: archive
    integer, intent(in) :: case_id
    character(len=12) :: state
    integer :: epoch, ip, mccg_state(B2J_NSTATE), length, record_type
    integer :: matcod(B2J_NREG)
    real(real32) :: volume_track32(B2J_NUNKNO)
    real(real64) :: authority_flux64(B2J_NUNKNO)
    type(c_ptr) :: authority, systems_list, item
    type(c_ptr) :: tracks, fluxes, plane, authority_flux

    authority=LCMGID(archive,'SPOT-R64')
    select case(case_id)
    case(2)
      state='ASSEMBLED'
      call LCMPTC(authority,'STATE',12,state)
    case(3)
      epoch=2
      call LCMPUT(authority,'EPOCH',1,1,epoch)
    case(4)
      systems_list=LCMLID(archive,'SYSTEM',B2J_NSNAP)
      do ip=1,B2J_NSNAP
        item=LCMDIL(systems_list,ip)
        call B2J_REQUIRE_ASSOCIATED(item,'forbidden projected SYSTEM')
      end do
    case(15:17)
      tracks=LCMGID(archive,'TRACK')
      item=LCMGIL(tracks,1)
      call B2J_REQUIRE_RECORD(item,'MCCG-STATE',B2J_NSTATE,1)
      call LCMGET(item,'MCCG-STATE',mccg_state)
      if (case_id == 15) mccg_state(11)=1
      if (case_id == 16) mccg_state(14)=0
      if (case_id == 17) mccg_state(17)=1
      call LCMPUT(item,'MCCG-STATE',B2J_NSTATE,1,mccg_state)
    case(18)
      fluxes=LCMGID(archive,'FLUX')
      plane=LCMGIL(fluxes,1)
      authority=LCMGID(plane,'SPOT-R64')
      authority_flux=LCMGID(authority,'FLUX')
      call LCMLEL(authority_flux,1,length,record_type)
      if (length /= B2J_NUNKNO .or. record_type /= 4) &
        error stop 'range mutation target schema differs'
      call LCMGDL(authority_flux,1,authority_flux64)
      authority_flux64(1)=2.0_real64*real(huge(0.0_real32),real64)
      call LCMPDL(authority_flux,1,B2J_NUNKNO,4,authority_flux64)
    case(19)
      tracks=LCMGID(archive,'TRACK')
      item=LCMGIL(tracks,1)
      call B2J_REQUIRE_RECORD(item,'MATCOD',B2J_NREG,1)
      call LCMGET(item,'MATCOD',matcod)
      if (matcod(1) == 1) then
        matcod(1)=2
      else
        matcod(1)=1
      end if
      call LCMPUT(item,'MATCOD',B2J_NREG,1,matcod)
    case(20)
      tracks=LCMGID(archive,'TRACK')
      item=LCMGIL(tracks,1)
      call B2J_REQUIRE_RECORD(item,'V$MCCG',B2J_NUNKNO,2)
      call LCMGET(item,'V$MCCG',volume_track32)
      volume_track32(1)=nearest(volume_track32(1),1.0_real32)
      call LCMPUT(item,'V$MCCG',B2J_NUNKNO,2,volume_track32)
    case default
      error stop 'unknown projected archive mutation'
    end select
  end subroutine MUTATE_PROJECTED


  subroutine MUTATE_SYSTEM(system,case_id)
    type(c_ptr), intent(in) :: system
    integer, intent(in) :: case_id
    integer :: marker, snapshot
    real(real32) :: leakage(B2J_NGRP), values32(32)
    type(c_ptr) :: groups, group

    groups=LCMGID(system,'GROUP')
    select case(case_id)
    case(6)
      marker=314159
      call LCMPUT(system,'B2I-SENT',1,1,marker)
    case(7)
      snapshot=2
      call LCMPUT(system,'SPOT-L1-SNAP',1,1,snapshot)
    case(8)
      call LCMGET(system,'SPOT-LEAK1D',leakage)
      leakage(1)=nearest(leakage(1),1.0_real32)
      call LCMPUT(system,'SPOT-LEAK1D',B2J_NGRP,2,leakage)
    case(9)
      group=LCMGIL(groups,1)
      call LCMGET(group,'DRAGON-TXSC',values32(1:B2K_NSYSMIX))
      values32(2)=nearest(values32(2),1.0_real32)
      call LCMPUT(group,'DRAGON-TXSC',B2K_NSYSMIX,2, &
          values32(1:B2K_NSYSMIX))
    case(10)
      group=LCMGIL(groups,1)
      call LCMGET(group,'SPOT-S0-PHYS',values32(1:B2K_NSYSMIX))
      values32(2)=nearest(values32(2),1.0_real32)
      call LCMPUT(group,'SPOT-S0-PHYS',B2K_NSYSMIX,2, &
          values32(1:B2K_NSYSMIX))
    case(11)
      group=LCMGIL(groups,1)
      call LCMGET(group,'DRAGON-S0XSC',values32(1:B2K_NSYSMIX))
      values32(2)=nearest(values32(2),1.0_real32)
      call LCMPUT(group,'DRAGON-S0XSC',B2K_NSYSMIX,2, &
          values32(1:B2K_NSYSMIX))
    case(12)
      group=LCMGIL(groups,1)
      call LCMDEL(group,'PJJ$MCCG')
    case(13)
      group=LCMGIL(groups,1)
      call LCMGET(group,'DIAGF$MCCG',values32(1:14))
      values32(1)=ieee_value(0.0_real32,ieee_quiet_nan)
      call LCMPUT(group,'DIAGF$MCCG',14,2,values32(1:14))
    case(14)
      group=LCMGIL(groups,B2J_NGRP)
      call LCMDEL(group,'PJJZI$MCCG')
    case default
      error stop 'unknown SYSTEM mutation'
    end select
  end subroutine MUTATE_SYSTEM


  subroutine VERIFY_INPUTS_UNCHANGED()
    integer :: ignored_leak, ignored_tx, ignored_phys, ignored_used, ip
    integer :: mccg_state(B2J_NSTATE), matcod(B2J_NREG)
    integer :: nzon(B2J_NUNKNO), ir
    real(real32) :: real_param32(4), volume32(B2J_NREG)
    real(real32) :: volume_track32(B2J_NUNKNO)
    type(c_ptr) :: authority, tracks, track

    call B2J_REQUIRE_EXACT_INVENTORY(projected, &
        [character(len=12) :: 'SIGNATURE','LISTDIM','SPOT-ITER-K', &
         'TRACK','MICROLIB2','FLUX','SPOT-R64'])
    authority=LCMGID(projected,'SPOT-R64')
    call B2J_REQUIRE_CHARACTER(authority,'STATE',12,'PROJECTED')
    call B2J_REQUIRE_ABSENT(projected,'SYSTEM')
    tracks=LCMGID(projected,'TRACK')
    do ip=1,B2J_NSNAP
      track=LCMGIL(tracks,ip)
      call B2J_REQUIRE_RECORD(track,'MCCG-STATE',B2J_NSTATE,1)
      call B2J_REQUIRE_RECORD(track,'REAL-PARAM',4,2)
      call B2J_REQUIRE_RECORD(track,'MATCOD',B2J_NREG,1)
      call B2J_REQUIRE_RECORD(track,'NZON$MCCG',B2J_NUNKNO,1)
      call B2J_REQUIRE_RECORD(track,'VOLUME',B2J_NREG,2)
      call B2J_REQUIRE_RECORD(track,'V$MCCG',B2J_NUNKNO,2)
      call LCMGET(track,'MCCG-STATE',mccg_state)
      call LCMGET(track,'REAL-PARAM',real_param32)
      call LCMGET(track,'MATCOD',matcod)
      call LCMGET(track,'NZON$MCCG',nzon)
      call LCMGET(track,'VOLUME',volume32)
      call LCMGET(track,'V$MCCG',volume_track32)
      if (mccg_state(11) /= 0 .or. mccg_state(14) /= 1 .or. &
          mccg_state(17) /= 0) &
        error stop 'projected MCCG state changed'
      if (B2J_BITS32(real_param32(1)) /= int(z'3727c5ac',int32) .or. &
          any(B2J_BITS32(real_param32(2:4)) /= 0_int32)) &
        error stop 'projected MCCG REAL-PARAM changed'
      if (any(nzon(1:B2J_NREG) /= matcod)) &
        error stop 'projected MATCOD/NZON map changed'
      do ir=1,B2J_NREG
        if (B2J_BITS32(volume32(ir)) /= &
            B2J_BITS32(volume_track32(ir))) &
          error stop 'projected VOLUME/V$MCCG map changed'
      end do
      call B2J_REQUIRE_ABSENT(systems(ip),'SPOT-R64')
      call B2J_REQUIRE_ABSENT(systems(ip),'B2I-SENT')
      call B2J_REQUIRE_ABSENT(systems(ip),'B2I-DEEP')
    end do
    call B2K_VERIFY_CANDIDATE_FORMULAS(projected,systems, &
        ignored_leak,ignored_tx,ignored_phys,ignored_used)
    if (ignored_leak /= B2J_NSNAP*B2J_NGRP .or. &
        ignored_tx /= B2J_NSNAP*B2J_NGRP*B2K_NSYSMIX .or. &
        ignored_phys /= ignored_tx .or. ignored_used /= ignored_tx) &
      error stop 'unchanged candidate formula inventory differs'
  end subroutine VERIFY_INPUTS_UNCHANGED

end program TEST_B2K_SYSTEM_ASSEMBLY
