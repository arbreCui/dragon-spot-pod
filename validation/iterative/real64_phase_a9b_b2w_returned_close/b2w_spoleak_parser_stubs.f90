module B2W_SPOLEAK_PROBES
  use, intrinsic :: iso_fortran_env, only : int32, real32
  implicit none
  private

  integer, save, public :: redget_calls=0
  integer, save, public :: redput_calls=0
  integer(int32), save, public :: returned_error_bits=0_int32
  public :: RESET_SPOLEAK_PROBES

contains

  subroutine RESET_SPOLEAK_PROBES()
    redget_calls=0
    redput_calls=0
    returned_error_bits=0_int32
  end subroutine RESET_SPOLEAK_PROBES

end module B2W_SPOLEAK_PROBES


subroutine REDGET(indic,nitma,flott,text,dflott)
  use B2W_SPOLEAK_PROBES, only : redget_calls
  implicit none
  integer, intent(out) :: indic, nitma
  real, intent(out) :: flott
  character(len=*), intent(out) :: text
  double precision, intent(out) :: dflott

  redget_calls=redget_calls+1
  nitma=0
  flott=0.0
  dflott=0.0d0
  text=' '
  select case(redget_calls)
  case(1)
    indic=-2
  case(2)
    indic=3
    text=';'
  case default
    error stop 'unexpected SPOLEAK REDGET call'
  end select
end subroutine REDGET


subroutine REDPUT(indic,nitma,flott,text,dflott)
  use B2W_SPOLEAK_PROBES, only : redput_calls, returned_error_bits
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32
  implicit none
  integer, intent(in) :: indic, nitma
  real, intent(in) :: flott
  character(len=*), intent(in) :: text
  double precision, intent(in) :: dflott

  if (indic /= 2) error stop 'SPOLEAK REDPUT type differs'
  if (nitma /= 0) error stop 'SPOLEAK REDPUT integer payload differs'
  if (len(text) < 1) error stop 'SPOLEAK REDPUT text dummy is invalid'
  if (transfer(dflott,0_int64) /= 0_int64) &
    error stop 'SPOLEAK REDPUT real64 payload differs'
  redput_calls=redput_calls+1
  if (redput_calls /= 1) error stop 'unexpected SPOLEAK REDPUT call'
  returned_error_bits=transfer(real(flott,real32),0_int32)
end subroutine REDPUT
