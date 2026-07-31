subroutine MCGFFIR64_RANK_ADAPTER(SUBSCH, K, KPN, M, N, H, NOM, NZON, &
    XST, S, NREG, KEYFLX_TRK3, KEYCUR, F, B, W, OMEGA2, IDIR, NSOUT, XSI)
  use, intrinsic :: iso_fortran_env, only : real32, real64
  implicit none

  integer, parameter :: kind_guard = 1 / merge(1, 0, &
      kind(0.0d0) == real64)

  external :: SUBSCH
  integer :: K, KPN, M, N, NREG, IDIR, NSOUT
  integer :: NOM(N), NZON(K), KEYFLX_TRK3(NREG,1,1)
  integer :: KEYCUR(K-NREG)
  real(real32) :: XST(0:M)
  real(real64) :: H(N), S(KPN), F(KPN), B(N)
  real(real64) :: W, OMEGA2(3), XSI(NSOUT)

  interface
    subroutine MCGFFIR(SUBSCH, K, KPN, M, N, H, NOM, NZON, XST, S, &
        NREG, KEYFLX, KEYCUR, F, B, W, OMEGA2, IDIR, NSOUT, XSI)
      import :: real32, real64, kind_guard
      integer, parameter :: checked_real64_kind = kind_guard
      external :: SUBSCH
      integer :: K, KPN, M, N, NREG, IDIR, NSOUT
      integer :: NOM(N), NZON(K), KEYFLX(NREG,1), KEYCUR(K-NREG)
      real(real32) :: XST(0:M)
      real(real64) :: H(N), S(KPN), F(KPN), B(N)
      real(real64) :: W, OMEGA2(3), XSI(NSOUT)
    end subroutine MCGFFIR
  end interface

  call MCGFFIR(SUBSCH, K, KPN, M, N, H, NOM, NZON, XST, S, NREG, &
      KEYFLX_TRK3(:,:,1), KEYCUR, F, B, W, OMEGA2, IDIR, NSOUT, XSI)
end subroutine MCGFFIR64_RANK_ADAPTER
