program LEGACY_B2C_ABI_CALLER
  use, intrinsic :: iso_c_binding, only : c_null_ptr
  use, intrinsic :: iso_fortran_env, only : real32, real64
  use SPOR64_B2C, only : SPOR64_B2C_PREFLIGHT_FAILED, &
      SPOR64_B2C_PUBLISH
  implicit none

  integer, parameter :: NGRP=370, NREG=8, NMAT=8, NUNKNO=14
  character(len=12), parameter :: MACRO_NAME='MACRO0'
  character(len=12), parameter :: TRACK_NAME='TRACK'
  character(len=12), parameter :: SYSTEM_NAME='SYSTEM'
  integer :: status
  integer :: keyflx(NREG), imerge(NMAT)
  real(real32) :: leakage32(NGRP), eps32
  real(real64) :: flux64(NUNKNO,NGRP), source64(NUNKNO,NGRP)

  flux64=0.0_real64
  source64=0.0_real64
  keyflx=[1,2,3,4,5,6,7,8]
  imerge=1
  leakage32=0.0_real32
  eps32=0.0_real32
  call SPOR64_B2C_PUBLISH(c_null_ptr,0,flux64,source64,keyflx,1, &
      imerge,leakage32,eps32,eps32,eps32,'B0  ',MACRO_NAME, &
      TRACK_NAME,SYSTEM_NAME,status)
  if (status /= SPOR64_B2C_PREFLIGHT_FAILED) &
    error stop 'legacy B2C ABI status differs'
  write(*,'(A)') 'B2P LEGACY-PARENT-MOD-CALLER PASS'
end program LEGACY_B2C_ABI_CALLER
