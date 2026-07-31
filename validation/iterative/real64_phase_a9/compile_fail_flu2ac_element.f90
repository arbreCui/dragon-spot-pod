subroutine COMPILE_FAIL_FLU2AC_ELEMENT()
  use, intrinsic :: iso_fortran_env, only : real64
  use SPOR64_A9, only : FLU2AC64
  implicit none

  logical :: ok
  real(real64) :: akeep64(3), flux64(1,1,3), zmu64

  akeep64 = 1.0_real64
  flux64 = 1.0_real64
  call FLU2AC64(1,1,1,flux64(1,1,1),akeep64(1),zmu64,ok)
end subroutine COMPILE_FAIL_FLU2AC_ELEMENT
