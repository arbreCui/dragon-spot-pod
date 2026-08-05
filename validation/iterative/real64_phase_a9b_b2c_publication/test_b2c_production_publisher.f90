program TEST_B2C_PRODUCTION_PUBLISHER
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_quiet_nan, ieee_value
  use GANLIB
  use SPOR64_B2C, only : SPOR64_B2C_PREFLIGHT_FAILED, &
      SPOR64_B2C_HOST_COMMITTED, SPOR64_B2C_PUBLISH
  implicit none

  integer, parameter :: nstate = 40
  integer, parameter :: ngrp = 370
  integer, parameter :: nreg = 8
  integer, parameter :: nmat = 8
  integer, parameter :: nunkno = 14
  type(c_ptr) :: root, legacy_flux, legacy_source
  type(c_ptr) :: authority, authority_flux, authority_source
  integer :: ig, iu, status, accepted_token
  integer :: keyflx(nreg), state(nstate), expected_state(nstate)
  integer :: keep(3), found_keep(3)
  real(real32) :: eps, leak1d(ngrp), initial32(nunkno)
  real(real32) :: found32(nunkno), eps_found(5), leak_found(ngrp)
  real(real64) :: terminal_flux64(nunkno,ngrp)
  real(real64) :: terminal_source64(nunkno,ngrp), found64(nunkno)
  logical :: collision_case
  character(len=32) :: scenario
  character(len=4), parameter :: option_input = 'B0  '
  character(len=12), parameter :: macro_name = 'MACRO0'
  character(len=12), parameter :: track_name = 'TRACK'
  character(len=12), parameter :: system_name = 'SYSTEM'
  character(len=4) :: option

  if (command_argument_count() /= 1) error stop 'one scenario expected'
  call get_command_argument(1,scenario)

  eps = transfer(int(z'348637bd',int32),0.0_real32)
  keyflx = [(ig,ig=1,nreg)]
  keep = [17,23,31]
  do ig = 1, ngrp
    leak1d(ig) = real(ig,real32) * 2.0_real32**(-19)
    do iu = 1, nunkno
      initial32(iu) = -real(1000 + 7*ig + iu,real32) * &
          2.0_real32**(-20)
      terminal_flux64(iu,ig) = real(10000 + 31*ig + iu,real64) * &
          2.0_real64**(-23) + real(iu,real64) * 2.0_real64**(-47)
      terminal_source64(iu,ig) = real(20000 + 37*ig + 3*iu,real64) * &
          2.0_real64**(-24) + real(ig,real64) * 2.0_real64**(-49)
    end do
  end do

  accepted_token = 4
  collision_case = .false.
  select case (trim(scenario))
  case ('valid')
    continue
  case ('wrong-token')
    accepted_token = 3
  case ('existing-spot')
    collision_case = .true.
  case ('nan')
    terminal_flux64(1,1) = ieee_value(0.0_real64,ieee_quiet_nan)
  case ('range')
    terminal_source64(2,3) = &
        2.0_real64 * real(huge(0.0_real32),real64)
  case default
    error stop 'unknown scenario'
  end select

  call LCMOP(root,'B2C-PUBLISH-TEST',0,1,0)
  if (.not. c_associated(root)) error stop 'LCMOP failed'
  legacy_flux = LCMLID(root,'FLUX',ngrp)
  if (.not. c_associated(legacy_flux)) error stop 'FLUX creation failed'
  do ig = 1, ngrp
    do iu = 1, nunkno
      initial32(iu) = -real(1000 + 7*ig + iu,real32) * &
          2.0_real32**(-20)
    end do
    call LCMPDL(legacy_flux,ig,nunkno,2,initial32)
  end do
  state = 0
  state(1) = ngrp
  state(2) = nunkno
  state(3) = 1
  state(8) = 3
  state(9) = 3
  state(10) = 1
  state(11) = 740
  state(12) = 500
  state(17) = nmat
  state(18) = 1
  eps_found = [eps,eps,eps,0.0_real32,0.0_real32]
  call LCMPUT(root,'STATE-VECTOR',nstate,1,state)
  call LCMPUT(root,'EPS-CONVERGE',5,2,eps_found)
  call LCMPUT(root,'B2C-KEEP',3,1,keep)
  if (collision_case) then
    authority = LCMDID(root,'SPOT-R64')
    if (.not. c_associated(authority)) error stop 'collision setup failed'
    call LCMPUT(authority,'COLLISION-KEEP',3,1,keep)
  end if

  call SPOR64_B2C_PUBLISH(root,accepted_token,terminal_flux64, &
      terminal_source64,keyflx,leak1d,eps,eps,eps,option_input, &
      macro_name,track_name,system_name,status)

  if (trim(scenario) == 'valid') then
  if (status /= SPOR64_B2C_HOST_COMMITTED) &
      error stop 'publisher did not reach host commit'

  call require_record(root,'SPOT-R64',-1,0)
  authority = LCMGID(root,'SPOT-R64')
  if (.not. c_associated(authority)) error stop 'authority lookup failed'
  call require_record(authority,'FLUX',ngrp,10)
  call require_record(authority,'SOUR',ngrp,10)
  authority_flux = LCMGID(authority,'FLUX')
  authority_source = LCMGID(authority,'SOUR')
  if (.not. c_associated(authority_flux)) error stop 'authority FLUX absent'
  if (.not. c_associated(authority_source)) error stop 'authority SOUR absent'

  call require_record(root,'FLUX',ngrp,10)
  call require_record(root,'SOUR',ngrp,10)
  legacy_flux = LCMGID(root,'FLUX')
  legacy_source = LCMGID(root,'SOUR')
  if (.not. c_associated(legacy_flux)) error stop 'legacy FLUX absent'
  if (.not. c_associated(legacy_source)) error stop 'legacy SOUR absent'
  do ig = 1, ngrp
    call require_element(authority_flux,ig,nunkno,4)
    call require_element(authority_source,ig,nunkno,4)
    call require_element(legacy_flux,ig,nunkno,2)
    call require_element(legacy_source,ig,nunkno,2)
    call LCMGDL(authority_flux,ig,found64)
    do iu = 1, nunkno
      if (transfer(found64(iu),0_int64) /= &
          transfer(terminal_flux64(iu,ig),0_int64)) &
          error stop 'type-4 FLUX bits differ'
    end do
    call LCMGDL(authority_source,ig,found64)
    do iu = 1, nunkno
      if (transfer(found64(iu),0_int64) /= &
          transfer(terminal_source64(iu,ig),0_int64)) &
          error stop 'type-4 SOUR bits differ'
    end do
    call LCMGDL(legacy_flux,ig,found32)
    do iu = 1, nunkno
      if (transfer(found32(iu),0_int32) /= &
          transfer(real(terminal_flux64(iu,ig),real32),0_int32)) &
          error stop 'type-2 FLUX conversion differs'
    end do
    call LCMGDL(legacy_source,ig,found32)
    do iu = 1, nunkno
      if (transfer(found32(iu),0_int32) /= &
          transfer(real(terminal_source64(iu,ig),real32),0_int32)) &
          error stop 'type-2 SOUR conversion differs'
    end do
  end do

  expected_state = 0
  expected_state(1) = ngrp
  expected_state(2) = nunkno
  expected_state(3) = 1
  expected_state(8) = 3
  expected_state(9) = 3
  expected_state(10) = 1
  expected_state(11) = 740
  expected_state(12) = 500
  expected_state(17) = nmat
  expected_state(18) = 1
  call require_record(root,'STATE-VECTOR',nstate,1)
  call LCMGET(root,'STATE-VECTOR',state)
  if (any(state /= expected_state)) error stop 'STATE-VECTOR differs'
  call require_record(root,'EPS-CONVERGE',5,2)
  call LCMGET(root,'EPS-CONVERGE',eps_found)
  if (any(transfer(eps_found,0_int32,5) /= &
      [transfer(eps,0_int32),transfer(eps,0_int32), &
       transfer(eps,0_int32),0_int32,0_int32])) &
      error stop 'EPS-CONVERGE differs'
  call require_record(root,'KEYFLX',nreg,1)
  call LCMGET(root,'KEYFLX',state(1:nreg))
  if (any(state(1:nreg) /= keyflx)) error stop 'KEYFLX differs'
  call require_record(root,'OPTION',1,3)
  option = ' '
  call LCMGTC(root,'OPTION',4,option)
  if (option /= 'B0  ') error stop 'OPTION differs'
  call require_character(root,'LINK.MACRO','MACRO0')
  call require_character(root,'LINK.TRACK','TRACK')
  call require_character(root,'LINK.SYSTEM','SYSTEM')
  call require_record(root,'SPOT-LEAK1D',ngrp,2)
  call LCMGET(root,'SPOT-LEAK1D',leak_found)
  if (any(transfer(leak_found,0_int32,ngrp) /= &
      transfer(leak1d,0_int32,ngrp))) error stop 'SPOT-LEAK1D differs'

  call require_absent(root,'AFLUX')
  call require_absent(root,'DFLUX')
  call require_absent(root,'ADFLUX')
  call require_absent(authority,'STATE-VECTOR')
  call require_record(root,'B2C-KEEP',3,1)
  call LCMGET(root,'B2C-KEEP',found_keep)
  if (any(found_keep /= keep)) error stop 'unrelated record mutated'
  else
    if (status /= SPOR64_B2C_PREFLIGHT_FAILED) &
        error stop 'rejection status differs'
    call require_absent(root,'SOUR')
    call require_absent(root,'AFLUX')
    call require_absent(root,'DFLUX')
    call require_absent(root,'ADFLUX')
    call require_record(root,'FLUX',ngrp,10)
    legacy_flux = LCMGID(root,'FLUX')
    do ig = 1, ngrp
      call require_element(legacy_flux,ig,nunkno,2)
      call LCMGDL(legacy_flux,ig,found32)
      do iu = 1, nunkno
        initial32(iu) = -real(1000 + 7*ig + iu,real32) * &
            2.0_real32**(-20)
      end do
      if (any(transfer(found32,0_int32,nunkno) /= &
          transfer(initial32,0_int32,nunkno))) &
          error stop 'rejection mutated root FLUX'
    end do
    call require_record(root,'B2C-KEEP',3,1)
    call LCMGET(root,'B2C-KEEP',found_keep)
    if (any(found_keep /= keep)) error stop 'rejection mutated sentinel'
    if (collision_case) then
      call require_record(root,'SPOT-R64',-1,0)
      authority = LCMGID(root,'SPOT-R64')
      call require_absent(authority,'FLUX')
      call require_absent(authority,'SOUR')
      call require_record(authority,'COLLISION-KEEP',3,1)
      call LCMGET(authority,'COLLISION-KEEP',found_keep)
      if (any(found_keep /= keep)) error stop 'collision owner mutated'
    else
      call require_absent(root,'SPOT-R64')
    end if
  end if

  call LCMCL(root,2)
  write(*,'(A,1X,A)') 'B2C-PRODUCTION-PUBLISHER-PASS',trim(scenario)

contains

  subroutine require_record(owner,name,expected_length,expected_type)
    type(c_ptr), intent(in) :: owner
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: found_length, found_type

    call LCMLEN(owner,name,found_length,found_type)
    if (found_length /= expected_length .or. found_type /= expected_type) then
      write(0,'(A,1X,A,4(1X,I0))') 'record schema differs',trim(name), &
          found_length,found_type,expected_length,expected_type
      error stop 'record schema differs'
    end if
  end subroutine require_record


  subroutine require_element(owner,index,expected_length,expected_type)
    type(c_ptr), intent(in) :: owner
    integer, intent(in) :: index, expected_length, expected_type
    integer :: found_length, found_type

    call LCMLEL(owner,index,found_length,found_type)
    if (found_length /= expected_length .or. found_type /= expected_type) &
        error stop 'list element schema differs'
  end subroutine require_element


  subroutine require_absent(owner,name)
    type(c_ptr), intent(in) :: owner
    character(len=*), intent(in) :: name

    call require_record(owner,name,0,99)
  end subroutine require_absent


  subroutine require_character(owner,name,expected)
    type(c_ptr), intent(in) :: owner
    character(len=*), intent(in) :: name, expected
    character(len=12) :: found

    call require_record(owner,name,3,3)
    found = ' '
    call LCMGTC(owner,name,12,found)
    if (found /= expected) then
      write(0,'(A,1X,A)') 'character record differs',trim(name)
      error stop 'character record differs'
    end if
  end subroutine require_character

end program TEST_B2C_PRODUCTION_PUBLISHER
