module SPOR64_A3
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : real32, real64
  implicit none
  private

  integer, parameter :: kind_guard = 1 / merge(1, 0, &
      kind(1.0) == real32 .and. kind(1.0d0) == real64)

  integer, parameter, public :: SPOR64_A3_OK = 0
  integer, parameter, public :: SPOR64_A3_UNSUPPORTED = 1
  integer, parameter, public :: SPOR64_A3_INVALID = 2

  public :: MCGFCF_MCGFST_R64_COMPILE_ONLY_LOCKED

  abstract interface
    subroutine SPOR64_MCGSCH_STIS1_IFACE(n, k, m, nom, nzon, h, xst, b)
      import :: real32, real64
      integer :: n, k, m
      integer :: nom(n), nzon(k)
      real(real32) :: xst(0:m)
      real(real64) :: h(n), b(n)
    end subroutine SPOR64_MCGSCH_STIS1_IFACE
  end interface

  abstract interface
    subroutine SPOR64_MCGFFI_STIS1_IFACE(subsch, k, kpn, m, n, h, &
        nom, nzon, xst, source, nreg, keyflx, keycur, flux, scratch, &
        weight, omega2, idir, nsout, xsi)
      import :: real32, real64
      external :: subsch
      integer :: k, kpn, m, n, nreg, idir, nsout
      integer :: nom(n), nzon(k), keyflx(nreg,1), keycur(k-nreg)
      real(real32) :: xst(0:m)
      real(real64) :: h(n), source(kpn), weight, omega2(3), xsi(nsout)
      real(real64) :: flux(kpn), scratch(n)
    end subroutine SPOR64_MCGFFI_STIS1_IFACE
  end interface

  abstract interface
    subroutine SPOR64_MCGFFA_STIS1_IFACE(subsch, k, kpn, m, n, h, &
        nom, nzon, xst, source_plus, source_minus, nreg, nmu, nani, &
        nfunl, trhar, keyflx, keycur, imu, flux, scratch)
      import :: real32, real64
      external :: subsch
      integer :: k, kpn, m, n, nreg, nmu, nani, nfunl, imu
      integer :: nom(n), nzon(k), keyflx(nreg,nfunl), keycur(k-nreg)
      real(real32) :: xst(0:m), trhar(nmu,nfunl,2)
      real(real64) :: h(n), source_plus(n), source_minus(n)
      real(real64) :: flux(kpn), scratch(n)
    end subroutine SPOR64_MCGFFA_STIS1_IFACE
  end interface

  abstract interface
    subroutine SPOR64_MCGLDC_IFACE(subsch, k, kpn, m, n, h, nom, nzon, &
        weight, xst, source_plus, source_minus, derivative_plus, &
        derivative_minus, nreg, nmu, nani, nfunlx, trhar, keycur, imu, &
        scratch, flux, phi_volume, derivative_volume)
      import :: real32, real64
      external :: subsch
      integer :: k, kpn, m, n, nreg, nmu, nani, nfunlx, imu
      integer :: nom(n), nzon(k), keycur(k-nreg)
      real(real32) :: xst(0:m), trhar(nmu,nfunlx,2)
      real(real64) :: weight, h(n), source_plus(n), source_minus(n)
      real(real64) :: derivative_plus(n), derivative_minus(n)
      real(real64) :: scratch(0:5,n), flux(kpn)
      real(real64) :: phi_volume(nfunlx,nreg)
      real(real64) :: derivative_volume(2*nfunlx,nreg)
    end subroutine SPOR64_MCGLDC_IFACE
  end interface

  procedure(SPOR64_MCGFFI_STIS1_IFACE) :: MCGFFIR
  procedure(SPOR64_MCGFFA_STIS1_IFACE) :: MCGFFAR
  procedure(SPOR64_MCGLDC_IFACE) :: MCGFFAL
  procedure(SPOR64_MCGSCH_STIS1_IFACE) :: MCGSCA

  interface
    subroutine MCGFCF(subffi, subffa, subldc, subsch, iftrak, nbtr, &
        nmax, ndim, kpn, k, nreg, m, ngeff, nangl, nmu, nlf, nfunl, &
        nmod, nlfx, nlin, nfunlx, keyflx, keycur, nzon, nconv, caz0, &
        caz1, caz2, cpo, zmu, wzmu, source, sigal, isgnr, idir, nsout, &
        nbatch, xsi, raw_response)
      import :: real32, real64
      external :: subffi, subffa, subldc, subsch
      integer :: iftrak, nbtr, nmax, ndim, kpn, k, nreg, m
      integer :: ngeff, nangl, nmu, nlf, nfunl, nmod, nlfx
      integer :: nlin, nfunlx, idir, nsout, nbatch
      integer :: keyflx(nreg,nlin,nfunl), keycur(k-nreg)
      integer :: nzon(k), isgnr(nmod,nfunlx)
      logical :: nconv(ngeff)
      real(real32) :: cpo(nmu), zmu(nmu), wzmu(nmu)
      real(real32) :: sigal(-6:m,ngeff)
      real(real64) :: caz0(nangl), caz1(nangl), caz2(nangl)
      real(real64) :: source(kpn,ngeff), xsi(nsout)
      real(real64) :: raw_response(kpn,ngeff)
    end subroutine MCGFCF

    subroutine MCGFST(ngeff, kpsys, nconv, kpn, k, nreg, nani, nfunl, &
        npjjm, keyflx, keycur, pjjind, nzon, volume, source, &
        raw_response, idir)
      import :: c_ptr, real32, real64
      integer :: ngeff, kpn, k, nreg, nani, nfunl, npjjm, idir
      type(c_ptr) :: kpsys(ngeff)
      logical :: nconv(ngeff)
      integer :: keyflx(nreg,nfunl), keycur(k-nreg)
      integer :: pjjind(npjjm,2), nzon(k)
      real(real32) :: volume(k)
      real(real64) :: source(kpn,ngeff), raw_response(kpn,ngeff)
    end subroutine MCGFST

    subroutine SPOR64_A3_COMPILE_ONLY_LINK_FORBIDDEN()
    end subroutine SPOR64_A3_COMPILE_ONLY_LINK_FORBIDDEN
  end interface

contains

  subroutine MCGFCF_MCGFST_R64_COMPILE_ONLY_LOCKED(iftrak, nbtr, nmax, &
      ndim, kpn, k, nreg, m, ngeff, nangl, nmu, nlf, nfunl, nmod, nlfx, &
      nlin, nfunlx, keyflx, keycur, nzon, nconv, caz0, caz1, caz2, cpo, &
      zmu, wzmu, source, sigal, isgnr, idir, nsout, nbatch, xsi, &
      raw_response, kpsys, nani, npjjm, pjjind, volume, ng, ngind, &
      cyclic, lprism, stis, status)
    integer, intent(in) :: iftrak, nbtr, nmax, ndim, kpn, k, nreg, m
    integer, intent(in) :: ngeff, nangl, nmu, nlf, nfunl, nmod, nlfx
    integer, intent(in) :: nlin, nfunlx, idir, nsout, nbatch
    integer, intent(in) :: nani, npjjm, ng, stis
    integer, contiguous, target, intent(in) :: keyflx(:,:,:)
    integer, contiguous, intent(in) :: keycur(:), nzon(:), isgnr(:,:)
    integer, contiguous, intent(in) :: pjjind(:,:), ngind(:)
    logical, contiguous, intent(in) :: nconv(:)
    logical, intent(in) :: cyclic, lprism
    type(c_ptr), contiguous, intent(in) :: kpsys(:)
    real(real32), contiguous, intent(in) :: cpo(:), zmu(:), wzmu(:)
    real(real32), contiguous, intent(in) :: sigal(-6:,:), volume(:)
    real(real64), contiguous, intent(in) :: caz0(:), caz1(:), caz2(:)
    real(real64), contiguous, intent(in) :: source(:,:), xsi(:)
    real(real64), contiguous, intent(inout) :: raw_response(:,:)
    integer, intent(out) :: status

    integer :: group
    integer, contiguous, pointer :: keyflx_stis(:,:)

    status = SPOR64_A3_UNSUPPORTED
    if (ndim /= 2 .or. kpn /= 14 .or. k /= 14 .or. nreg /= 8) return
    if (nsout /= 6 .or. ng /= 370) return
    if (nani /= 1 .or. nlf /= 1 .or. nfunl /= 1) return
    if (nmod /= 4 .or. nlfx /= 1 .or. nlin /= 1 .or. nfunlx /= 1) return
    if (idir /= 0 .or. stis /= 1 .or. cyclic .or. lprism) return

    status = SPOR64_A3_INVALID
    if (m < 0 .or. ngeff <= 0 .or. ngeff > ng) return
    if (nbtr <= 0 .or. nmax <= 0 .or. nangl <= 0 .or. nmu <= 0) return
    if (nbatch <= 0 .or. npjjm /= 1) return

    if (size(keyflx,1) /= nreg .or. size(keyflx,2) /= nlin .or. &
        size(keyflx,3) /= nfunl) return
    if (size(keycur) /= k-nreg .or. size(nzon) /= k) return
    if (size(isgnr,1) /= nmod .or. size(isgnr,2) /= nfunlx) return
    if (size(pjjind,1) /= npjjm .or. size(pjjind,2) /= 2) return
    if (size(ngind) /= ngeff .or. size(nconv) /= ngeff) return
    if (size(kpsys) /= ngeff) return
    if (size(caz0) /= nangl .or. size(caz1) /= nangl .or. &
        size(caz2) /= nangl) return
    if (size(cpo) /= nmu .or. size(zmu) /= nmu .or. &
        size(wzmu) /= nmu) return
    if (size(sigal,1) /= m+7 .or. size(sigal,2) /= ngeff) return
    if (size(volume) /= k .or. size(xsi) /= nsout) return
    if (size(source,1) /= kpn .or. size(source,2) /= ngeff) return
    if (size(raw_response,1) /= kpn .or. &
        size(raw_response,2) /= ngeff) return

    if (.not. any(nconv)) return
    if (ngind(1) /= ng-ngeff+1 .or. ngind(ngeff) /= ng) return
    do group = 2, ngeff
      if (ngind(group) /= ngind(group-1)+1) return
    end do
    do group = 1, ngeff
      if (nconv(group) .and. .not. c_associated(kpsys(group))) return
    end do

    if (any(nzon(:nreg) < 0) .or. any(nzon(:nreg) > m)) return
    if (any(nzon(nreg+1:) >= 0) .or. any(nzon(nreg+1:) < -6)) return
    if (any(keyflx < 1) .or. any(keyflx > kpn)) return
    if (any(keycur < 1) .or. any(keycur > kpn)) return
    if (any(pjjind /= 1)) return

    keyflx_stis(1:nreg,1:nfunl) => keyflx

    call SPOR64_A3_COMPILE_ONLY_LINK_FORBIDDEN()
    call MCGFCF(MCGFFIR, MCGFFAR, MCGFFAL, MCGSCA, iftrak, nbtr, nmax, &
        ndim, kpn, k, nreg, m, ngeff, nangl, nmu, nlf, nfunl, nmod, &
        nlfx, nlin, nfunlx, keyflx, keycur, nzon, nconv, caz0, caz1, &
        caz2, cpo, zmu, wzmu, source, sigal, isgnr, idir, nsout, nbatch, &
        xsi, raw_response)
    call MCGFST(ngeff, kpsys, nconv, kpn, k, nreg, nani, nfunl, npjjm, &
        keyflx_stis, keycur, pjjind, nzon, volume, source, raw_response, &
        idir)
    status = SPOR64_A3_OK
  end subroutine MCGFCF_MCGFST_R64_COMPILE_ONLY_LOCKED

end module SPOR64_A3
