module SPOR64_A4
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : real32, real64
  use SPOR64_A2, only : MCGFL1R64_POST_STIS_RAW_FACADE_LOCKED, &
      SPOR64_A2_INVALID, SPOR64_A2_OK, SPOR64_A2_RESPONSE_FAILED, &
      SPOR64_A2_UNSUPPORTED
  use SPOR64_A3, only : MCGFCF_MCGFST_R64_COMPILE_ONLY_LOCKED, &
      SPOR64_A3_INVALID, SPOR64_A3_OK
  implicit none
  private

  integer, parameter :: kind_guard = 1 / merge(1, 0, &
      kind(1.0) == real32 .and. kind(1.0d0) == real64)

  integer, parameter, public :: SPOR64_A4_OK = SPOR64_A2_OK
  integer, parameter, public :: SPOR64_A4_UNSUPPORTED = &
      SPOR64_A2_UNSUPPORTED
  integer, parameter, public :: SPOR64_A4_INVALID = SPOR64_A2_INVALID
  integer, parameter, public :: SPOR64_A4_RESPONSE_FAILED = &
      SPOR64_A2_RESPONSE_FAILED

  type, public :: SPOR64_A4_CONTEXT
    logical :: enabled = .false.
    integer :: iftrak = 0
    integer :: nbtr = 0
    integer :: nmax = 0
    integer :: nbatch = 0
    integer, allocatable :: isgnr(:,:), pjjind(:,:)
    type(c_ptr), allocatable :: kpsys(:)
    real(real32), allocatable :: cpo(:), zmu(:), wzmu(:), volume(:)
    real(real64), allocatable :: caz0(:), caz1(:), caz2(:), xsi(:)
  end type SPOR64_A4_CONTEXT

  public :: MCGFL1R64_A2_A3_HOST_CLOSURE_COMPILE_ONLY_LOCKED

contains

  subroutine MCGFL1R64_A2_A3_HOST_CLOSURE_COMPILE_ONLY_LOCKED(n, ndim, &
      nzon, qn, fi, m, nani, nlin, nfunl, sc, source, kpn, nreg, &
      keyflx, keycur, ibc, sigal, stis, cyclic, lprism, idir, ng, ngeff, &
      ngind, nconv, context, raw_response, status)
    integer, intent(in) :: n, ndim, m, nani, nlin, nfunl
    integer, intent(in) :: kpn, nreg, stis, idir, ng, ngeff
    integer, contiguous, intent(in) :: nzon(:), keycur(:), ibc(:)
    integer, contiguous, target, intent(in) :: keyflx(:,:,:)
    integer, contiguous, intent(in) :: ngind(:)
    logical, intent(in) :: cyclic, lprism
    logical, contiguous, intent(in) :: nconv(:)
    real(real64), contiguous, intent(in) :: qn(:,:), fi(:,:)
    real(real32), contiguous, intent(in) :: sc(0:,:,:), sigal(-6:,:)
    real(real64), contiguous, intent(inout) :: source(:,:)
    real(real64), contiguous, intent(inout) :: raw_response(:,:)
    type(SPOR64_A4_CONTEXT), intent(in) :: context
    integer, intent(out) :: status

    status = SPOR64_A4_UNSUPPORTED
    if (.not. context%enabled) return
    if (n /= 14 .or. ndim /= 2 .or. kpn /= 14 .or. nreg /= 8) return
    if (nani /= 1 .or. nlin /= 1 .or. nfunl /= 1 .or. stis /= 1) return
    if (idir /= 0 .or. ng /= 370 .or. cyclic .or. lprism) return

    status = SPOR64_A4_INVALID
    if (context%nbtr <= 0 .or. context%nmax <= 0) return
    if (context%nbatch <= 0) return
    if (.not. allocated(context%isgnr)) return
    if (.not. allocated(context%pjjind)) return
    if (.not. allocated(context%kpsys)) return
    if (.not. allocated(context%cpo)) return
    if (.not. allocated(context%zmu)) return
    if (.not. allocated(context%wzmu)) return
    if (.not. allocated(context%volume)) return
    if (.not. allocated(context%caz0)) return
    if (.not. allocated(context%caz1)) return
    if (.not. allocated(context%caz2)) return
    if (.not. allocated(context%xsi)) return

    if (size(context%isgnr,1) /= 4 .or. &
        size(context%isgnr,2) /= 1) return
    if (size(context%pjjind,1) /= 1 .or. &
        size(context%pjjind,2) /= 2) return
    if (size(context%kpsys) /= ngeff) return
    if (size(context%cpo) <= 0) return
    if (size(context%zmu) /= size(context%cpo)) return
    if (size(context%wzmu) /= size(context%cpo)) return
    if (size(context%volume) /= n) return
    if (size(context%caz0) <= 0) return
    if (size(context%caz1) /= size(context%caz0)) return
    if (size(context%caz2) /= size(context%caz0)) return
    if (size(context%xsi) /= n-nreg) return

    call MCGFL1R64_POST_STIS_RAW_FACADE_LOCKED(n, ndim, nzon, qn, fi, &
        m, nani, nlin, nfunl, sc, source, kpn, nreg, keyflx, keycur, &
        ibc, sigal, stis, cyclic, lprism, idir, ng, ngeff, ngind, nconv, &
        phase_a3_primary_response, raw_response, status)

  contains

    subroutine phase_a3_primary_response(local_ngeff, local_ngind, &
        local_nconv, local_kpn, local_source, local_raw_response, &
        response_status)
      integer, intent(in) :: local_ngeff, local_kpn
      integer, intent(in) :: local_ngind(:)
      logical, intent(in) :: local_nconv(:)
      real(real64), intent(in) :: local_source(:,:)
      real(real64), intent(inout) :: local_raw_response(:,:)
      integer, intent(out) :: response_status

      integer :: allocation_status
      real(real64), allocatable :: raw_a3(:,:), source_a3(:,:)

      response_status = SPOR64_A3_INVALID
      if (local_ngeff /= ngeff .or. local_kpn /= kpn) return
      if (size(local_ngind) /= size(ngind)) return
      if (size(local_nconv) /= size(nconv)) return
      if (size(local_source,1) /= kpn .or. &
          size(local_source,2) /= ngeff) return
      if (size(local_raw_response,1) /= kpn .or. &
          size(local_raw_response,2) /= ngeff) return
      if (any(local_ngind /= ngind)) return
      if (any(local_nconv .neqv. nconv)) return

      allocate(source_a3(kpn,ngeff), raw_a3(kpn,ngeff), &
          stat=allocation_status)
      if (allocation_status /= 0) return
      source_a3 = local_source
      raw_a3 = local_raw_response

      call MCGFCF_MCGFST_R64_COMPILE_ONLY_LOCKED(context%iftrak, &
          context%nbtr, context%nmax, ndim, local_kpn, n, nreg, m, &
          local_ngeff, size(context%caz0), size(context%cpo), nani, &
          nfunl, size(context%isgnr,1), nani, nlin, &
          size(context%isgnr,2), keyflx, keycur, nzon, nconv, &
          context%caz0, context%caz1, context%caz2, context%cpo, &
          context%zmu, context%wzmu, source_a3, sigal, context%isgnr, &
          idir, size(context%xsi), context%nbatch, context%xsi, raw_a3, &
          context%kpsys, nani, size(context%pjjind,1), context%pjjind, &
          context%volume, ng, ngind, cyclic, lprism, stis, &
          response_status)
      if (response_status == SPOR64_A3_OK) then
        local_raw_response = raw_a3
      end if
    end subroutine phase_a3_primary_response

  end subroutine MCGFL1R64_A2_A3_HOST_CLOSURE_COMPILE_ONLY_LOCKED

end module SPOR64_A4
