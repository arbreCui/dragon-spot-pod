program B2C_SYNTHETIC_PUBLICATION_DRIVER
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_positive_inf, &
      ieee_quiet_nan, ieee_value
  use B2C_SYNTHETIC_PUBLICATION
  implicit none

  integer :: accepted_token, status, ledger(B2C_LEDGER_SIZE)
  integer :: ledger_length, status_trace(3), status_trace_length
  integer :: ig, iu
  integer(int64) :: conversion_count
  logical :: collisions(B2C_COLLISIONS), expect_failure
  real(real32), parameter :: sentinel32 = -1234.5_real32
  real(real64), parameter :: sentinel64 = -9876.25_real64
  real(real64), parameter :: real32_max64 = &
      real(huge(0.0_real32),real64)
  real(real64) :: terminal_flux64(B2C_NUNKNO,B2C_NGRP)
  real(real64) :: terminal_source64(B2C_NUNKNO,B2C_NGRP)
  real(real64) :: authority_flux64(B2C_NUNKNO,B2C_NGRP)
  real(real64) :: authority_source64(B2C_NUNKNO,B2C_NGRP)
  real(real32) :: legacy_flux32(B2C_NUNKNO,B2C_NGRP)
  real(real32) :: legacy_source32(B2C_NUNKNO,B2C_NGRP)
  character(len=32) :: scenario

  if (command_argument_count() /= 1) error stop 'one scenario expected'
  call get_command_argument(1,scenario)

  accepted_token = B2C_SYNTHETIC_ACCEPTED_TOKEN
  collisions = .false.
  expect_failure = .true.
  do ig = 1, B2C_NGRP
    do iu = 1, B2C_NUNKNO
      terminal_flux64(iu,ig) = real(10000 + 31*ig + iu,real64) * &
          2.0_real64**(-23) + real(iu,real64) * 2.0_real64**(-47)
      terminal_source64(iu,ig) = real(20000 + 37*ig + 3*iu,real64) * &
          2.0_real64**(-24) + real(ig,real64) * 2.0_real64**(-49)
    end do
  end do

  select case (trim(scenario))
  case ('wrong-token')
    accepted_token = B2C_SYNTHETIC_ACCEPTED_TOKEN - 1
  case ('collision-spot')
    collisions(1) = .true.
  case ('collision-sour')
    collisions(2) = .true.
  case ('collision-aflux')
    collisions(3) = .true.
  case ('collision-dflux')
    collisions(4) = .true.
  case ('collision-adflux')
    collisions(5) = .true.
  case ('nan-flux')
    terminal_flux64(1,1) = ieee_value(0.0_real64,ieee_quiet_nan)
  case ('inf-source')
    terminal_source64(2,3) = ieee_value(0.0_real64,ieee_positive_inf)
  case ('over-positive')
    terminal_flux64(3,5) = 2.0_real64 * real32_max64
  case ('over-negative')
    terminal_source64(4,7) = -2.0_real64 * real32_max64
  case ('boundary')
    terminal_flux64(1,1) = real32_max64
    terminal_flux64(2,1) = -real32_max64
    terminal_source64(3,1) = real32_max64
    terminal_source64(4,1) = -real32_max64
    expect_failure = .false.
  case ('normal')
    expect_failure = .false.
  case default
    error stop 'unknown scenario'
  end select

  ledger = -1
  status_trace = -1
  authority_flux64 = sentinel64
  authority_source64 = sentinel64
  legacy_flux32 = sentinel32
  legacy_source32 = sentinel32
  call B2C_SYNTHETIC_PUBLISH(accepted_token,collisions,terminal_flux64, &
      terminal_source64,status,ledger,ledger_length,status_trace, &
      status_trace_length,conversion_count,authority_flux64, &
      authority_source64,legacy_flux32,legacy_source32)

  if (expect_failure) then
    if (status /= B2C_SYNTHETIC_PREFLIGHT_FAILED) &
        error stop 'failure status differs'
    if (ledger_length /= 0 .or. status_trace_length /= 0) &
        error stop 'failure mutated ledger'
    if (conversion_count /= 0_int64) error stop 'failure converted payload'
    if (any(authority_flux64 /= sentinel64)) &
        error stop 'failure mutated authority flux'
    if (any(authority_source64 /= sentinel64)) &
        error stop 'failure mutated authority source'
    if (any(legacy_flux32 /= sentinel32)) &
        error stop 'failure mutated legacy flux'
    if (any(legacy_source32 /= sentinel32)) &
        error stop 'failure mutated legacy source'
  else
    if (status /= B2C_SYNTHETIC_HOST_COMMITTED) &
        error stop 'success status differs'
    if (ledger_length /= B2C_LEDGER_SIZE) error stop 'ledger length differs'
    if (any(ledger /= [(ig,ig=1,B2C_LEDGER_SIZE)])) &
        error stop 'publication order differs'
    if (status_trace_length /= 3) error stop 'status trace length differs'
    if (any(status_trace /= [B2C_SYNTHETIC_CHILD_PUBLISHED, &
        B2C_SYNTHETIC_DRIVER_COMMITTED,B2C_SYNTHETIC_HOST_COMMITTED])) &
        error stop 'status trace differs'
    if (conversion_count /= &
        int(2*B2C_NUNKNO*B2C_NGRP,int64)) error stop 'conversion count differs'
    do ig = 1, B2C_NGRP
      do iu = 1, B2C_NUNKNO
        if (transfer(authority_flux64(iu,ig),0_int64) /= &
            transfer(terminal_flux64(iu,ig),0_int64)) &
            error stop 'authority flux lost REAL64 bits'
        if (transfer(authority_source64(iu,ig),0_int64) /= &
            transfer(terminal_source64(iu,ig),0_int64)) &
            error stop 'authority source lost REAL64 bits'
        if (transfer(legacy_flux32(iu,ig),0_int32) /= &
            transfer(real(terminal_flux64(iu,ig),real32),0_int32)) &
            error stop 'legacy flux conversion differs'
        if (transfer(legacy_source32(iu,ig),0_int32) /= &
            transfer(real(terminal_source64(iu,ig),real32),0_int32)) &
            error stop 'legacy source conversion differs'
      end do
    end do
  end if

  write(*,'(A,1X,A)') 'B2C-SYNTHETIC-PASS',trim(scenario)
end program B2C_SYNTHETIC_PUBLICATION_DRIVER
