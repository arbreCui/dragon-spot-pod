module COMPILE_B2C_POSITIVE
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, real32, real64
  use SPOR64_B2C, only : SPOR64_B2C_PUBLISH
  implicit none
contains
  subroutine COMPILE_EXACT_B2C_CALL(ipflux)
    type(c_ptr), intent(in) :: ipflux
    integer :: status, keyflx(8)
    real(real32) :: leak1d(370), eps
    real(real64) :: flux64(14,370), source64(14,370)
    character(len=4), parameter :: option = 'B0  '
    character(len=12), parameter :: macro_name = 'MACRO0'
    character(len=12), parameter :: track_name = 'TRACK'
    character(len=12), parameter :: system_name = 'SYSTEM'

    keyflx = [(status,status=1,8)]
    leak1d = 0.0_real32
    eps = transfer(int(z'348637bd',int32),0.0_real32)
    flux64 = 0.0_real64
    source64 = 0.0_real64
    call SPOR64_B2C_PUBLISH(ipflux,4,flux64,source64,keyflx,leak1d, &
        eps,eps,eps,option,macro_name,track_name,system_name,status)
  end subroutine COMPILE_EXACT_B2C_CALL
end module COMPILE_B2C_POSITIVE
