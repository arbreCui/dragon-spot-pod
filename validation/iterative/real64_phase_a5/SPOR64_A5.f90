module SPOR64_A5
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : real32, real64
  use SPOR64_A4, only : SPOR64_A4_CONTEXT, &
      MCGFL1R64_A2_A3_HOST_CLOSURE_COMPILE_ONLY_LOCKED, &
      SPOR64_A4_INVALID, SPOR64_A4_OK, SPOR64_A4_RESPONSE_FAILED, &
      SPOR64_A4_UNSUPPORTED
  implicit none
  private

  integer, parameter :: kind_guard = 1 / merge(1, 0, &
      kind(1.0) == real32 .and. kind(1.0d0) == real64)

  integer, parameter, public :: SPOR64_A5_OK = SPOR64_A4_OK
  integer, parameter, public :: SPOR64_A5_UNSUPPORTED = &
      SPOR64_A4_UNSUPPORTED
  integer, parameter, public :: SPOR64_A5_INVALID = SPOR64_A4_INVALID
  integer, parameter, public :: SPOR64_A5_RESPONSE_FAILED = &
      SPOR64_A4_RESPONSE_FAILED

  public :: MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED

contains

  subroutine MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED(n, &
      ndim, nzon, qn, fi, m, nani, nlin, nfunl, sc, source, kpn, nreg, &
      keyflx, keycur, ibc, sigal, stis, cyclic, lprism, idir, ng, ngeff, &
      ngind, nconv, iftrak, nbtr, n2max, nbatch, kpsys, caz1, caz2, zmu, &
      wzmu, volume, raw_response, status)
    integer, intent(in) :: n, ndim, m, nani, nlin, nfunl
    integer, intent(in) :: kpn, nreg, stis, idir, ng, ngeff
    integer, intent(in) :: iftrak, nbtr, n2max, nbatch
    integer, contiguous, intent(in) :: nzon(:), keycur(:), ibc(:)
    integer, contiguous, target, intent(in) :: keyflx(:,:,:)
    integer, contiguous, intent(in) :: ngind(:)
    logical, intent(in) :: cyclic, lprism
    logical, contiguous, intent(in) :: nconv(:)
    type(c_ptr), contiguous, intent(in) :: kpsys(:)
    real(real32), contiguous, intent(in) :: sc(0:,:,:), sigal(-6:,:)
    real(real32), contiguous, intent(in) :: zmu(:), wzmu(:), volume(:)
    real(real64), contiguous, intent(in) :: qn(:,:), fi(:,:)
    real(real64), contiguous, intent(in) :: caz1(:), caz2(:)
    real(real64), contiguous, intent(inout) :: source(:,:)
    real(real64), contiguous, intent(inout) :: raw_response(:,:)
    integer, intent(out) :: status

    integer :: group, population_status
    type(SPOR64_A4_CONTEXT) :: context

    context%enabled = .false.
    status = SPOR64_A5_UNSUPPORTED
    if (n /= 14 .or. ndim /= 2 .or. kpn /= 14 .or. nreg /= 8) return
    if (nani /= 1 .or. nlin /= 1 .or. nfunl /= 1 .or. stis /= 1) return
    if (idir /= 0 .or. ng /= 370 .or. cyclic .or. lprism) return

    status = SPOR64_A5_INVALID
    if (m < 0 .or. ngeff <= 0 .or. ngeff > ng) return
    if (iftrak <= 0 .or. nbtr <= 0 .or. n2max <= 0) return
    if (nbatch <= 0) return
    if (size(ngind) /= ngeff .or. size(nconv) /= ngeff) return
    if (size(kpsys) /= ngeff) return
    if (size(caz1) <= 0 .or. size(caz2) /= size(caz1)) return
    if (size(zmu) <= 0 .or. size(wzmu) /= size(zmu)) return
    if (size(volume) /= n) return
    if (.not. any(nconv)) return
    if (ngind(1) /= ng-ngeff+1 .or. ngind(ngeff) /= ng) return
    do group = 2, ngeff
      if (ngind(group) /= ngind(group-1)+1) return
    end do
    do group = 1, ngeff
      if (nconv(group) .and. .not. c_associated(kpsys(group))) return
    end do

    call populate_context(iftrak, nbtr, n2max, nbatch, kpsys, caz1, &
        caz2, zmu, wzmu, volume, n-nreg, context, population_status)
    if (population_status /= SPOR64_A5_OK) then
      status = population_status
      return
    end if

    context%enabled = .true.
    call MCGFL1R64_A2_A3_HOST_CLOSURE_COMPILE_ONLY_LOCKED(n, ndim, nzon, &
        qn, fi, m, nani, nlin, nfunl, sc, source, kpn, nreg, keyflx, &
        keycur, ibc, sigal, stis, cyclic, lprism, idir, ng, ngeff, ngind, &
        nconv, context, raw_response, status)
    context%enabled = .false.
  end subroutine MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED

  subroutine populate_context(iftrak, nbtr, n2max, nbatch, kpsys, caz1, &
      caz2, zmu, wzmu, volume, nsout, context, status)
    integer, intent(in) :: iftrak, nbtr, n2max, nbatch, nsout
    type(c_ptr), contiguous, intent(in) :: kpsys(:)
    real(real32), contiguous, intent(in) :: zmu(:), wzmu(:), volume(:)
    real(real64), contiguous, intent(in) :: caz1(:), caz2(:)
    type(SPOR64_A4_CONTEXT), intent(out) :: context
    integer, intent(out) :: status

    integer :: allocation_status

    context%enabled = .false.
    status = SPOR64_A5_INVALID
    allocate(context%isgnr(4,1), context%pjjind(1,2), &
        context%kpsys(size(kpsys)), context%cpo(size(zmu)), &
        context%zmu(size(zmu)), context%wzmu(size(wzmu)), &
        context%volume(size(volume)), context%caz0(size(caz1)), &
        context%caz1(size(caz1)), context%caz2(size(caz2)), &
        context%xsi(nsout), stat=allocation_status)
    if (allocation_status /= 0) return

    context%iftrak = iftrak
    context%nbtr = nbtr
    context%nmax = n2max
    context%nbatch = nbatch
    context%kpsys = kpsys
    context%caz1 = caz1
    context%caz2 = caz2
    context%zmu = zmu
    context%wzmu = wzmu
    context%volume = volume

    ! Canonical storage for three unread formals; the integer arrays are
    ! the exact order-zero MOCIK3/MCGPJJ identities.
    context%caz0 = 0.0_real64
    context%cpo = 0.0_real32
    context%xsi = 0.0_real64
    context%isgnr = 1
    context%pjjind = 1
    status = SPOR64_A5_OK
  end subroutine populate_context

end module SPOR64_A5
