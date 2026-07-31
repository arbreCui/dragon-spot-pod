subroutine COMPILE_FAIL_REAL32_TERMINAL()
  use, intrinsic :: iso_fortran_env, only : real32
  use SPOR64_A9, only : SPOR64_A9_TERMINAL64
  implicit none

  logical :: accepted
  real(real32) :: eext32, eunk32, einr32, eps32

  eext32 = +0.0_real32
  eunk32 = +0.0_real32
  einr32 = +0.0_real32
  eps32 = 1.0_real32
  call SPOR64_A9_TERMINAL64(eext32,eunk32,einr32,eps32,eps32,eps32, &
      1,2,accepted)
end subroutine COMPILE_FAIL_REAL32_TERMINAL
