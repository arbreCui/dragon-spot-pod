program compile_fail_real32_actual
  use, intrinsic :: iso_fortran_env, only : real32
  use SPOR64_A2, only : MCGFL1R64_POST_STIS_RAW_FACADE_LOCKED
  implicit none

  integer, parameter :: m = 0, nreg = 1, n = 2
  integer, parameter :: kpn = 2, ng = 1, ngeff = 1
  integer :: ibc(1), keycur(1), keyflx(1,1,1), ngind(1), nzon(n)
  integer :: status
  logical :: nconv(1)
  real(real32) :: fi(kpn,1), qn(kpn,1), raw(kpn,1)
  real(real32) :: s(kpn,1), sc(0:m,1,1), sigal(-6:m,1)

  ibc = 1
  keycur = 2
  keyflx = 1
  ngind = 1
  nconv = .true.
  nzon = [0, -1]
  fi = 1.0_real32
  qn = 1.0_real32
  raw = 0.0_real32
  s = 0.0_real32
  sc = 1.0_real32
  sigal = 1.0_real32

  call MCGFL1R64_POST_STIS_RAW_FACADE_LOCKED(n, 2, nzon, qn, fi, m, 1, &
      1, 1, sc, s, kpn, nreg, keyflx, keycur, ibc, sigal, 1, .false., &
      .false., 0, ng, ngeff, ngind, nconv, response, raw, status)

contains

  subroutine response(local_ngeff, local_ngind, local_nconv, local_kpn, &
      source, raw_response, local_status)
    integer, intent(in) :: local_ngeff, local_kpn, local_ngind(:)
    logical, intent(in) :: local_nconv(:)
    real(real32), intent(in) :: source(:,:)
    real(real32), intent(inout) :: raw_response(:,:)
    integer, intent(out) :: local_status

    raw_response = source
    local_status = local_ngeff + local_kpn + size(local_ngind) + &
        size(local_nconv) - 5
  end subroutine response

end program compile_fail_real32_actual
