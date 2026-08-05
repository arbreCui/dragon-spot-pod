module COMPILE_FAIL_B2C_REAL32_TERMINAL
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, real32
  use SPOR64_B2C, only : SPOR64_B2C_PUBLISH
  implicit none
contains
  subroutine COMPILE_WRONG_B2C_CALL(ipflux)
    type(c_ptr), intent(in) :: ipflux
    integer :: status, keyflx(8)
    real(real32) :: leak1d(370), eps
    real(real32) :: flux32(14,370), source32(14,370)
    character(len=4), parameter :: option = 'B0  '
    character(len=12), parameter :: macro_name = 'MACRO0'
    character(len=12), parameter :: track_name = 'TRACK'
    character(len=12), parameter :: system_name = 'SYSTEM'

    keyflx = [(status,status=1,8)]
    leak1d = 0.0_real32
    eps = transfer(int(z'348637bd',int32),0.0_real32)
    flux32 = 0.0_real32
    source32 = 0.0_real32
    call SPOR64_B2C_PUBLISH(ipflux,4,flux32,source32,keyflx,leak1d, &
        eps,eps,eps,option,macro_name,track_name,system_name,status)
  end subroutine COMPILE_WRONG_B2C_CALL
end module COMPILE_FAIL_B2C_REAL32_TERMINAL
