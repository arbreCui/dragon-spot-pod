module SPOR64_A8
  ! The REAL64 flight solver: the SPOT door down to the
  ! characteristic sweep and its accelerated inner iteration.
  use, intrinsic :: iso_c_binding, only : c_associated, c_f_pointer, &
      c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use SPOR64_A8_ACA, only : MCGFCA64
  use SPOR64_RCONTRACT, only : SPOR64_ROUTE_CONTRACT
  use SPOR64_VERIFY, only : RECORD_MATCHES
  implicit none
  private

  integer, parameter :: NGRP = 370
  integer, parameter :: NALBEDO = 6
  integer, parameter :: NANI = 1
  integer, parameter :: NLIN = 1
  integer, parameter :: NFUNL = 1
  integer, parameter :: NDIM = 2
  integer, parameter :: STIS = 1
  integer, parameter :: IDIR = 0
  integer, parameter :: ISCH = 11
  integer, parameter :: KRYL = 10
  integer, parameter :: IAAC = 80
  integer, parameter :: ISCR = 0
  integer, parameter :: MAXI = 20
  ! Deep inner terminal of the REAL64-leakage contract.  KRYL and MAXI are
  ! the tracked GMRES restart length and Arnoldi-work cap.  A projected
  ! residual can only schedule a fresh TRUE check; it cannot accept a group.
  real(real64), parameter :: DP_MCCG_EPSI64 = 1.0e-13_real64
  integer, parameter :: MAXACC = 200
  logical, parameter :: LFORW = .true.

  integer, parameter :: kind_guard = 1 / merge(1, 0, &
      kind(1.0) == real32 .and. kind(0.0d0) == real64)

  public :: DOORFV64, MCCGF64, MCGFLX64, MCGMRE64, MCGFL164, MCGFCS64
  public :: SPOR64_A8_MUTABLE_PROBE, SPOR64_A8_CAPTURE_PROBE
  public :: SPOR64_A8_RANK_PROBE, SPOR64_A8_OPERATOR_PROBE

  interface
    subroutine LCMLEN(iplist, name, length, itylcm)
      import :: c_ptr
      type(c_ptr) :: iplist
      character(len=*) :: name
      integer :: length, itylcm
    end subroutine LCMLEN

    subroutine LCMGPD(iplist, name, address)
      import :: c_ptr
      type(c_ptr) :: iplist, address
      character(len=*) :: name
    end subroutine LCMGPD

    function LCMGIL(iplist, index) result(directory)
      import :: c_ptr
      type(c_ptr) :: iplist, directory
      integer :: index
    end function LCMGIL

    subroutine MCGSIG(iptrk, m, ngeff, nalbp, kpsys, sigal32, lvoid)
      import :: c_ptr, real32
      integer :: m, ngeff, nalbp
      type(c_ptr) :: iptrk, kpsys(ngeff)
      real(real32) :: sigal32(-6:m,ngeff)
      logical :: lvoid
    end subroutine MCGSIG

    subroutine PRINDM(title, values64, n)
      import :: real64
      character(len=6) :: title
      integer :: n
      real(real64) :: values64(n)
    end subroutine PRINDM

    subroutine MOCIK3(nani0, nfunl, nmod, isgnr, keyani)
      integer :: nani0, nfunl, nmod, isgnr(nmod,nfunl), keyani(nfunl)
    end subroutine MOCIK3

    subroutine MCGFCF(subffi, subffa, subldc, subsch, iftrak, nbtr, &
        nmax, ndim0, kpn0, k, nreg0, m, ngeff, nangl, nmu, nlf, nfunl0, &
        nmod, nlfx, nlin0, nfunlx, keyflx, keycur, nzon, nconv, caz0, &
        caz1, caz2, cpo32, zmu32, wzmu32, source64, sigal32, isgnr, &
        idir0, nsout0, nbatch, xsi64, response64)
      import :: real32, real64
      external :: subffi, subffa, subldc, subsch
      integer :: iftrak, nbtr, nmax, ndim0, kpn0, k, nreg0, m, ngeff
      integer :: nangl, nmu, nlf, nfunl0, nmod, nlfx, nlin0, nfunlx
      integer :: idir0, nsout0, nbatch
      integer :: keyflx(nreg0,nlin0,nfunl0), keycur(k-nreg0), nzon(k)
      integer :: isgnr(nmod,nfunlx)
      logical :: nconv(ngeff)
      real(real32) :: cpo32(nmu), zmu32(nmu), wzmu32(nmu)
      real(real32) :: sigal32(-6:m,ngeff)
      real(real64) :: caz0(nangl), caz1(nangl), caz2(nangl)
      real(real64) :: source64(kpn0,ngeff), xsi64(nsout0)
      real(real64) :: response64(kpn0,ngeff)
    end subroutine MCGFCF

    subroutine MCGFST(ngeff, kpsys, nconv, kpn0, k, nreg0, nani0, &
        nfunl0, npjjm, keyflx2, keycur, pjjind2, nzon, volume32, &
        source64, response64, idir0)
      import :: c_ptr, real32, real64
      integer :: ngeff, kpn0, k, nreg0, nani0, nfunl0, npjjm, idir0
      type(c_ptr) :: kpsys(ngeff)
      logical :: nconv(ngeff)
      integer :: keyflx2(nreg0,nfunl0), keycur(k-nreg0)
      integer :: pjjind2(npjjm,2), nzon(k)
      real(real32) :: volume32(k)
      real(real64) :: source64(kpn0,ngeff), response64(kpn0,ngeff)
    end subroutine MCGFST

    subroutine SPOMOC_CAPTURE64(ngeff, ngind, nun, qfr64, eval64, &
        source64, raw64, nconv)
      import :: real64
      integer, intent(in) :: ngeff, nun
      integer, intent(in) :: ngind(ngeff)
      real(real64), intent(in) :: qfr64(nun,ngeff), eval64(nun,ngeff)
      real(real64), intent(in) :: source64(nun,ngeff), raw64(nun,ngeff)
      logical, intent(in) :: nconv(ngeff)
    end subroutine SPOMOC_CAPTURE64

    subroutine SPOMOC_MCCGF_BEGIN(ngrp, ngeff, ngind, nun, ndim0, &
        cyclic, nlong, nreg0, nsou, nani0, nlin0, nfunl0, kryl0, &
        stis0, iaac0, iscr0, idifc0, paca0, idir0)
      integer, intent(in) :: ngrp, ngeff, nun, ndim0, nlong, nreg0
      integer, intent(in) :: nsou, nani0, nlin0, nfunl0, kryl0, stis0
      integer, intent(in) :: iaac0, iscr0, idifc0, paca0, idir0
      integer, intent(in) :: ngind(ngeff)
      logical, intent(in) :: cyclic
    end subroutine SPOMOC_MCCGF_BEGIN

    subroutine SPOMOC_SET_ROLE(role, iteration)
      integer :: role, iteration
    end subroutine SPOMOC_SET_ROLE

    subroutine SPOMOC_PUBLISH()
    end subroutine SPOMOC_PUBLISH
  end interface

contains

  subroutine SPOR64_A8_MUTABLE_PROBE(values64, ok)
    real(real64), contiguous, intent(inout) :: values64(:,:)
    logical, intent(out) :: ok
    ok = size(values64,1) > 0 .and. size(values64,2) > 0
  end subroutine SPOR64_A8_MUTABLE_PROBE

  subroutine SPOR64_A8_CAPTURE_PROBE(ngeff, ngind, nun, qfr64, &
      eval64, source64, raw64, nconv, ok)
    integer, intent(in) :: ngeff, nun
    integer, intent(in) :: ngind(ngeff)
    real(real64), intent(in) :: qfr64(nun,ngeff)
    real(real64), intent(in) :: eval64(nun,ngeff)
    real(real64), intent(in) :: source64(nun,ngeff)
    real(real64), intent(in) :: raw64(nun,ngeff)
    logical, intent(in) :: nconv(ngeff)
    logical, intent(out) :: ok
    ok = .false.
    if (ngeff <= 0 .or. nun <= 0) return
    ok = all(ngind > 0) .and. any(nconv) .and. &
        all(ieee_is_finite(qfr64)) .and. &
        all(ieee_is_finite(eval64)) .and. &
        all(ieee_is_finite(source64)) .and. &
        all(ieee_is_finite(raw64))
  end subroutine SPOR64_A8_CAPTURE_PROBE

  subroutine SPOR64_A8_RANK_PROBE(keyflx_base1, keyflx_trk3, &
      pjjind_trk2, ok)
    integer, contiguous, intent(in) :: keyflx_base1(:)
    integer, contiguous, intent(in) :: keyflx_trk3(:,:,:)
    integer, contiguous, intent(in) :: pjjind_trk2(:,:)
    logical, intent(out) :: ok
    integer :: nreg
    ok = .false.
    nreg = size(keyflx_base1)
    if (nreg <= 0) return
    if (size(keyflx_trk3,1) /= nreg) return
    if (size(keyflx_trk3,2) /= NLIN) return
    if (size(keyflx_trk3,3) /= NFUNL) return
    if (size(pjjind_trk2,1) /= 1) return
    if (size(pjjind_trk2,2) /= 2) return
    ok = all(keyflx_base1 == keyflx_trk3(:,1,1)) .and. &
        all(pjjind_trk2 == 1)
  end subroutine SPOR64_A8_RANK_PROBE

  subroutine SPOR64_A8_OPERATOR_PROBE(sc32, sigal32, ok)
    real(real32), intent(in) :: sc32(0:,:)
    real(real32), intent(in) :: sigal32(-NALBEDO:)
    logical, intent(out) :: ok
    ok = .false.
    if (size(sc32,1) <= 1 .or. size(sc32,2) /= 1) return
    if (ubound(sigal32,1) /= ubound(sc32,1)) return
    ok = all(ieee_is_finite(sc32)) .and. all(ieee_is_finite(sigal32))
  end subroutine SPOR64_A8_OPERATOR_PROBE
  subroutine MAP_INTEGER1(iplist, name, n, values, ok)
    type(c_ptr), intent(in) :: iplist
    character(len=*), intent(in) :: name
    integer, intent(in) :: n
    integer, contiguous, pointer, intent(out) :: values(:)
    logical, intent(out) :: ok
    integer :: shape1(1)
    type(c_ptr) :: address
    nullify(values)
    ok = RECORD_MATCHES(iplist, name, n, 1)
    if (.not. ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MAP_INTEGER1",'// &
        '"predicate_id":"A8_MAP_INTEGER1_RETURN_L0206",'// &
        '"original_return_source_line":206,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    call LCMGPD(iplist, name, address)
    if (.not. c_associated(address)) then
      ok = .false.
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MAP_INTEGER1",'// &
        '"predicate_id":"A8_MAP_INTEGER1_RETURN_L0210",'// &
        '"original_return_source_line":210,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    shape1(1) = n
    call c_f_pointer(address, values, shape1)
  end subroutine MAP_INTEGER1

  subroutine MAP_REAL321(iplist, name, n, values, ok)
    type(c_ptr), intent(in) :: iplist
    character(len=*), intent(in) :: name
    integer, intent(in) :: n
    real(real32), contiguous, pointer, intent(out) :: values(:)
    logical, intent(out) :: ok
    integer :: shape1(1)
    type(c_ptr) :: address
    nullify(values)
    ok = RECORD_MATCHES(iplist, name, n, 2)
    if (.not. ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MAP_REAL321",'// &
        '"predicate_id":"A8_MAP_REAL321_RETURN_L0226",'// &
        '"original_return_source_line":226,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    call LCMGPD(iplist, name, address)
    if (.not. c_associated(address)) then
      ok = .false.
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MAP_REAL321",'// &
        '"predicate_id":"A8_MAP_REAL321_RETURN_L0230",'// &
        '"original_return_source_line":230,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    shape1(1) = n
    call c_f_pointer(address, values, shape1)
  end subroutine MAP_REAL321

  subroutine MAP_INTEGER2(iplist, name, n1, n2, values, ok)
    type(c_ptr), intent(in) :: iplist
    character(len=*), intent(in) :: name
    integer, intent(in) :: n1, n2
    integer, contiguous, pointer, intent(out) :: values(:,:)
    logical, intent(out) :: ok
    integer :: shape2(2)
    type(c_ptr) :: address
    nullify(values)
    ok = RECORD_MATCHES(iplist, name, n1*n2, 1)
    if (.not. ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MAP_INTEGER2",'// &
        '"predicate_id":"A8_MAP_INTEGER2_RETURN_L0246",'// &
        '"original_return_source_line":246,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    call LCMGPD(iplist, name, address)
    if (.not. c_associated(address)) then
      ok = .false.
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MAP_INTEGER2",'// &
        '"predicate_id":"A8_MAP_INTEGER2_RETURN_L0250",'// &
        '"original_return_source_line":250,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    shape2(1) = n1
    shape2(2) = n2
    call c_f_pointer(address, values, shape2)
  end subroutine MAP_INTEGER2

  subroutine MAP_INTEGER3(iplist, name, n1, n2, n3, values, ok)
    type(c_ptr), intent(in) :: iplist
    character(len=*), intent(in) :: name
    integer, intent(in) :: n1, n2, n3
    integer, contiguous, pointer, intent(out) :: values(:,:,:)
    logical, intent(out) :: ok
    integer :: shape3(3)
    type(c_ptr) :: address
    nullify(values)
    ok = RECORD_MATCHES(iplist, name, n1*n2*n3, 1)
    if (.not. ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MAP_INTEGER3",'// &
        '"predicate_id":"A8_MAP_INTEGER3_RETURN_L0267",'// &
        '"original_return_source_line":267,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    call LCMGPD(iplist, name, address)
    if (.not. c_associated(address)) then
      ok = .false.
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MAP_INTEGER3",'// &
        '"predicate_id":"A8_MAP_INTEGER3_RETURN_L0271",'// &
        '"original_return_source_line":271,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    shape3(1) = n1
    shape3(2) = n2
    shape3(3) = n3
    call c_f_pointer(address, values, shape3)
  end subroutine MAP_INTEGER3

  subroutine DOORFV64(ipsys, npsys, iptrk, iftrak, impx, ngrp, nun, &
      keyflx_base1, title, leak1d64, full_source64, full_flux64, &
      contract, cutoff_delta64, ok)
    type(c_ptr), intent(in) :: ipsys, iptrk
    type(SPOR64_ROUTE_CONTRACT), intent(in) :: contract
    integer, intent(in) :: ngrp, nun, iftrak, impx
    real(real64), intent(in) :: leak1d64(:)
    integer, intent(in) :: npsys(ngrp), keyflx_base1(:)
    character(len=72), intent(in) :: title
    real(real64), intent(in) :: full_source64(nun,ngrp)
    real(real64), intent(inout) :: full_flux64(nun,ngrp)
    integer(int64), intent(out) :: cutoff_delta64
    logical, intent(out) :: ok

    integer :: first_group, ig, ii, ileng, itylcm, ngeff, nreg
    integer(int64) :: child_delta64
    logical :: child_ok
    logical, allocatable :: seen(:)
    integer, allocatable :: ngind(:)
    real(real64), allocatable :: fgar64(:), phiin_tail64(:,:)
    real(real64), allocatable :: qfr_tail64(:,:)
    type(c_ptr), allocatable :: kpsys_tail(:)

    cutoff_delta64 = 0_int64
    ok = .false.
    nreg = size(keyflx_base1)
    if (ngrp /= NGRP .or. nun <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"DOORFV64",'// &
        '"predicate_id":"A8_DOORFV64_RETURN_L0305",'// &
        '"original_return_source_line":305,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (nreg <= 0 .or. nreg > nun) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"DOORFV64",'// &
        '"predicate_id":"A8_DOORFV64_RETURN_L0306",'// &
        '"original_return_source_line":306,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. c_associated(ipsys) .or. .not. c_associated(iptrk)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"DOORFV64",'// &
        '"predicate_id":"A8_DOORFV64_RETURN_L0307",'// &
        '"original_return_source_line":307,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (iftrak <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"DOORFV64",'// &
        '"predicate_id":"A8_DOORFV64_RETURN_L0308",'// &
        '"original_return_source_line":308,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(full_source64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"DOORFV64",'// &
        '"predicate_id":"A8_DOORFV64_RETURN_L0309",'// &
        '"original_return_source_line":309,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(full_flux64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"DOORFV64",'// &
        '"predicate_id":"A8_DOORFV64_RETURN_L0310",'// &
        '"original_return_source_line":310,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    allocate(seen(nun))
    seen = .false.
    do ii = 1, nreg
      if (keyflx_base1(ii) < 1 .or. keyflx_base1(ii) > nun) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"DOORFV64",'// &
          '"predicate_id":"A8_DOORFV64_RETURN_L0315",'// &
          '"original_return_source_line":315,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      if (seen(keyflx_base1(ii))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"DOORFV64",'// &
          '"predicate_id":"A8_DOORFV64_RETURN_L0316",'// &
          '"original_return_source_line":316,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      seen(keyflx_base1(ii)) = .true.
    end do

    ngeff = count(npsys /= 0)
    if (ngeff <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"DOORFV64",'// &
        '"predicate_id":"A8_DOORFV64_RETURN_L0321",'// &
        '"original_return_source_line":321,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    first_group = ngrp - ngeff + 1
    if (first_group > 1) then
      if (any(npsys(:first_group-1) /= 0)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"DOORFV64",'// &
          '"predicate_id":"A8_DOORFV64_RETURN_L0324",'// &
          '"original_return_source_line":324,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
    end if
    do ig = first_group, ngrp
      if (npsys(ig) /= ig) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"DOORFV64",'// &
          '"predicate_id":"A8_DOORFV64_RETURN_L0327",'// &
          '"original_return_source_line":327,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
    end do

    allocate(ngind(ngeff), kpsys_tail(ngeff))
    allocate(qfr_tail64(nun,ngeff), phiin_tail64(nun,ngeff))
    do ii = 1, ngeff
      ig = first_group + ii - 1
      ngind(ii) = ig
      kpsys_tail(ii) = LCMGIL(ipsys, npsys(ig))
      if (.not. c_associated(kpsys_tail(ii))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"DOORFV64",'// &
          '"predicate_id":"A8_DOORFV64_RETURN_L0336",'// &
          '"original_return_source_line":336,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      call LCMLEN(kpsys_tail(ii), 'FUNKNO$USS', ileng, itylcm)
      if (ileng /= 0) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"DOORFV64",'// &
          '"predicate_id":"A8_DOORFV64_RETURN_L0338",'// &
          '"original_return_source_line":338,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      qfr_tail64(:,ii) = full_source64(:,ig)
      phiin_tail64(:,ii) = full_flux64(:,ig)
    end do

    if (impx > 3) then
      allocate(fgar64(nreg))
      do ii = 1, ngeff
        fgar64 = +0.0_real64
        do ig = 1, nreg
          fgar64(ig) = qfr_tail64(keyflx_base1(ig),ii)
        end do
        call PRINDM('QFR64 ', fgar64, nreg)
      end do
    end if

    child_delta64 = 0_int64
    call MCCGF64(kpsys_tail, iptrk, iftrak, impx, ngeff, ngind, nun, &
        keyflx_base1, leak1d64, qfr_tail64, phiin_tail64, title, &
        contract, child_delta64, child_ok)
    cutoff_delta64 = cutoff_delta64 + child_delta64
    if (.not. child_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"DOORFV64",'// &
        '"predicate_id":"A8_DOORFV64_RETURN_L0359",'// &
        '"original_return_source_line":359,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(phiin_tail64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"DOORFV64",'// &
        '"predicate_id":"A8_DOORFV64_RETURN_L0360",'// &
        '"original_return_source_line":360,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    do ii = 1, ngeff
      full_flux64(:,ngind(ii)) = phiin_tail64(:,ii)
    end do
    if (impx > 3) then
      do ii = 1, ngeff
        fgar64 = +0.0_real64
        do ig = 1, nreg
          fgar64(ig) = phiin_tail64(keyflx_base1(ig),ii)
        end do
        call PRINDM('FLUX64', fgar64, nreg)
      end do
    end if
    ok = .true.
  end subroutine DOORFV64

  subroutine MCCGF64(kpsys, iptrk, iftrak, impx, ngeff, ngind, nun, &
      keyflx_base1, leak1d64, qfr64, phiin64, title, contract, &
      cutoff_delta64, &
      ok)
    use GANLIB, only : A8_OWN_LCMGET => LCMGET
    integer, intent(in) :: iftrak, impx, ngeff, nun
    type(SPOR64_ROUTE_CONTRACT), intent(in) :: contract
    type(c_ptr), intent(in) :: kpsys(ngeff), iptrk
    integer, intent(in) :: ngind(ngeff), keyflx_base1(:)
    real(real64), intent(in) :: leak1d64(:)
    real(real64), intent(in) :: qfr64(nun,ngeff)
    real(real64), intent(inout) :: phiin64(nun,ngeff)
    character(len=72), intent(in) :: title
    integer(int64), intent(out) :: cutoff_delta64
    logical, intent(out) :: ok

    character(len=4) :: text4
    integer :: i, icom, ifmt, ios, ispec, itylcm, j, nalbg, nalbp
    integer :: nangl, nbatch, nbtr, ncomnt, ncor, nmax, nmu
    integer :: n2reg, n2sou, mxseg, mxsub, lc, lc0, lnconv, paca
    integer :: history_capacity
    integer :: nbmix, nlong, nreg, nsou
    integer(int64) :: child_delta64
    integer, allocatable :: itst(:), matalb_trk(:)
    integer, allocatable, target :: owned_state_vector(:)
    integer, allocatable, target :: owned_mccg_state(:), owned_icode_trk1(:)
    integer, allocatable, target :: owned_nzon_trk1(:), owned_keycur_trk1(:)
    integer, allocatable, target :: owned_keyflx_trk3(:,:,:)
    real(real32), allocatable, target :: owned_real_param32(:)
    real(real32), allocatable, target :: owned_wzmu32(:), owned_zmu32(:)
    real(real32), allocatable, target :: owned_volume_trk32(:)
    integer, contiguous, pointer :: icode_trk1(:), keycur_trk1(:)
    integer, contiguous, pointer :: mccg_state(:)
    integer, contiguous, pointer :: nzon_trk1(:), state_vector(:)
    integer, contiguous, pointer :: keyflx_trk3(:,:,:)
    logical :: child_ok, lvoid, map_ok
    logical, allocatable :: nconv(:), seen(:)
    real(real32), contiguous, pointer :: albedo_trk32(:), cpo_view32(:)
    real(real32), contiguous, pointer :: group_albedo32(:)
    real(real32), contiguous, pointer :: real_param32(:)
    real(real32), contiguous, pointer :: sc_record32(:), volume_trk32(:)
    real(real32), contiguous, pointer :: txsc_record32(:), wzmu32(:)
    real(real32), contiguous, pointer :: zmu32(:)
    real(real32), allocatable :: cpo32(:), sc_by_group32(:,:,:)
    real(real32), allocatable :: sigal32(:,:)
    real(real64) :: epsi64, temp64
    real(real64), allocatable :: caz1_track64(:), caz2_track64(:)
    real(real64), allocatable :: eps64(:), reps64(:,:)

    cutoff_delta64 = 0_int64
    ok = .false.
    nreg = size(keyflx_base1)
    if (ngeff <= 0 .or. ngeff > NGRP .or. nun <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0421",'// &
        '"original_return_source_line":421,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (nreg <= 0 .or. nreg > nun) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0422",'// &
        '"original_return_source_line":422,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (iftrak <= 0 .or. .not. c_associated(iptrk)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0423",'// &
        '"original_return_source_line":423,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    do i = 1, ngeff
      if (.not. c_associated(kpsys(i))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCCGF64",'// &
          '"predicate_id":"A8_MCCGF64_RETURN_L0425",'// &
          '"original_return_source_line":425,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
    end do
    if (ngind(1) /= NGRP-ngeff+1 .or. ngind(ngeff) /= NGRP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0427",'// &
        '"original_return_source_line":427,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    do i = 2, ngeff
      if (ngind(i) /= ngind(i-1)+1) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCCGF64",'// &
          '"predicate_id":"A8_MCCGF64_RETURN_L0429",'// &
          '"original_return_source_line":429,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
    end do
    if (.not. all(ieee_is_finite(qfr64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0431",'// &
        '"original_return_source_line":431,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(phiin64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0432",'// &
        '"original_return_source_line":432,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    call MAP_INTEGER1(iptrk, 'STATE-VECTOR', 40, state_vector, map_ok)
    if (.not. map_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0435",'// &
        '"original_return_source_line":435,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(owned_state_vector(40))
    call A8_OWN_LCMGET(iptrk, 'STATE-VECTOR', owned_state_vector)
    state_vector => owned_state_vector
    call MAP_INTEGER1(iptrk, 'MCCG-STATE', 40, mccg_state, map_ok)
    if (.not. map_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0437",'// &
        '"original_return_source_line":437,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(owned_mccg_state(40))
    call A8_OWN_LCMGET(iptrk, 'MCCG-STATE', owned_mccg_state)
    mccg_state => owned_mccg_state
    call MAP_REAL321(iptrk, 'REAL-PARAM', 4, real_param32, map_ok)
    if (.not. map_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0439",'// &
        '"original_return_source_line":439,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(owned_real_param32(4))
    call A8_OWN_LCMGET(iptrk, 'REAL-PARAM', owned_real_param32)
    real_param32 => owned_real_param32
    nbmix = state_vector(4)
    nsou = state_vector(5)
    if (nbmix <= 0) then
      block
        use GANLIB, only : A8_DIAG_LCMINF => LCMINF, &
            A8_DIAG_LCMLEN => LCMLEN, A8_DIAG_LCMGET => LCMGET
        integer :: diag_state_length, diag_state_type, diag_list_length
        integer :: diag_state_owned40(40)
        logical :: diag_empty, diag_memory, diag_snapshot_verified
        character(len=72) :: diag_object_name
        character(len=12) :: diag_directory_name

        call A8_DIAG_LCMINF(iptrk,diag_object_name,diag_directory_name, &
            diag_empty,diag_list_length,diag_memory)
        call A8_DIAG_LCMLEN(iptrk,'STATE-VECTOR', &
            diag_state_length,diag_state_type)
        diag_snapshot_verified = diag_state_length == 40 .and. &
            diag_state_type == 1
        if (diag_snapshot_verified) then
          call A8_DIAG_LCMGET(iptrk,'STATE-VECTOR',diag_state_owned40)
          write(6,'(*(G0))') &
              '{"schema":"ACTUAL_SPOR64_A8_MCCGF442_STATE_FAILURE_SNAPSHOT_V1",', &
              '"original_return_source_line":442,"nbmix":',nbmix, &
              ',"nsou":',nsou,',"nreg":',nreg,',"nun":',nun, &
              ',"actual_STATE_length":',diag_state_length, &
              ',"actual_STATE_type":',diag_state_type, &
              ',"actual_LCMINF_memory_object":', &
              trim(merge('true ','false',diag_memory)), &
              ',"snapshot_verified":true,"fresh_STATE4":',diag_state_owned40(4), &
              ',"fresh_STATE5":',diag_state_owned40(5),'}'
        else
          write(6,'(*(G0))') &
              '{"schema":"ACTUAL_SPOR64_A8_MCCGF442_STATE_FAILURE_SNAPSHOT_V1",', &
              '"original_return_source_line":442,"nbmix":',nbmix, &
              ',"nsou":',nsou,',"nreg":',nreg,',"nun":',nun, &
              ',"actual_STATE_length":',diag_state_length, &
              ',"actual_STATE_type":',diag_state_type, &
              ',"actual_LCMINF_memory_object":', &
              trim(merge('true ','false',diag_memory)), &
              ',"snapshot_verified":false,"fresh_STATE4":null,"fresh_STATE5":null}'
        end if
        flush(6)
      end block
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0442",'// &
        '"original_return_source_line":442,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (state_vector(1) /= nreg .or. state_vector(2) /= nun) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0443",'// &
        '"original_return_source_line":443,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (state_vector(3) /= 1) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0444",'// &
        '"original_return_source_line":444,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (nsou <= 0 .or. state_vector(6) /= NANI) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0445",'// &
        '"original_return_source_line":445,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (state_vector(9) /= 0 .or. state_vector(14) /= 4) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0446",'// &
        '"original_return_source_line":446,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (state_vector(16) /= 2 .or. state_vector(22) /= 1) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0447",'// &
        '"original_return_source_line":447,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (state_vector(27) < 0 .or. state_vector(39) /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0448",'// &
        '"original_return_source_line":448,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (state_vector(40) /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0449",'// &
        '"original_return_source_line":449,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (mccg_state(2) /= 4 .or. mccg_state(3) /= KRYL) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0450",'// &
        '"original_return_source_line":450,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (mccg_state(4) /= 0 .or. mccg_state(5) <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0451",'// &
        '"original_return_source_line":451,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (mccg_state(6) <= 0 .or. mccg_state(7) /= IAAC) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0452",'// &
        '"original_return_source_line":452,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (mccg_state(8) /= ISCR .or. mccg_state(9) /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0453",'// &
        '"original_return_source_line":453,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    paca = mccg_state(10)
    lc0 = mccg_state(17)
    if (paca /= 3 .and. paca /= 4) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0456",'// &
        '"original_return_source_line":456,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (mccg_state(12) /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0457",'// &
        '"original_return_source_line":457,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (paca == 3) then
      if (lc0 <= 0) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCCGF64",'// &
          '"predicate_id":"A8_MCCGF64_RETURN_L0459",'// &
          '"original_return_source_line":459,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
    else
      if (lc0 /= 0) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCCGF64",'// &
          '"predicate_id":"A8_MCCGF64_RETURN_L0461",'// &
          '"original_return_source_line":461,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
    end if
    if (mccg_state(13) /= MAXI .or. mccg_state(15) /= STIS) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0463",'// &
        '"original_return_source_line":463,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (mccg_state(16) /= NFUNL .or. mccg_state(18) /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0464",'// &
        '"original_return_source_line":464,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (mccg_state(19) /= NFUNL .or. mccg_state(20) /= NLIN) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0465",'// &
        '"original_return_source_line":465,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (1 + 10*mccg_state(15) + 100*(mccg_state(20)-1) /= ISCH) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0466",'// &
        '"original_return_source_line":466,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    lc = mccg_state(6)
    nmu = mccg_state(2)
    nmax = mccg_state(5)
    if (lc <= 0 .or. nmu <= 0 .or. nmax <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0470",'// &
        '"original_return_source_line":470,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    nbatch = state_vector(27)
    if (nbatch == 0) nbatch = 1
    if (nbatch < 1) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0473",'// &
        '"original_return_source_line":473,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (transfer(real_param32(1), 0_int32) /= &
        contract%eps_mccg_bits) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0475",'// &
        '"original_return_source_line":475,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(real_param32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0476",'// &
        '"original_return_source_line":476,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (transfer(real_param32(2), 0_int32) /= 0_int32) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0477",'// &
        '"original_return_source_line":477,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (transfer(real_param32(3), 0_int32) /= 0_int32) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0478",'// &
        '"original_return_source_line":478,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (transfer(real_param32(4), 0_int32) /= 0_int32) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0479",'// &
        '"original_return_source_line":479,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    epsi64 = real(real_param32(1), real64)
    if (.not. ieee_is_finite(epsi64) .or. epsi64 <= 0.0_real64) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0481",'// &
        '"original_return_source_line":481,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    ! Data-keyed: the REAL64-leakage mode always carries a physically
    ! nonzero leakage vector; the legacy mode passes exact zeros and
    ! keeps the tracked terminal byte-identically.
    if (any(leak1d64 /= 0.0_real64)) epsi64 = DP_MCCG_EPSI64
    ! Isolated snapshot sensitivity: stricter work target, never a relaxed gate.
    epsi64 = min(epsi64, 2.5e-10_real64)
    write(6,'(A,ES24.16)') ' AXMAT-INNER-WORK-TARGET=',epsi64

    ! V$MCCG is the tracking authority for the long-vector extent.  The
    ! present isotropic, non-TIBERE route has one unknown per region or
    ! outer surface, exactly as in the frozen pin case.
    call LCMLEN(iptrk, 'V$MCCG', nlong, itylcm)
    if (nlong <= 0 .or. itylcm /= 2) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0494",'// &
        '"original_return_source_line":494,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (int(nlong,int64) /= int(nreg,int64)+int(nsou,int64) .or. &
        nun /= nlong) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0496",'// &
        '"original_return_source_line":496,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    rewind(iftrak, iostat=ios)
    if (ios /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0499",'// &
        '"original_return_source_line":499,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    read(iftrak, iostat=ios) text4, ncomnt, nbtr, ifmt
    if (ios /= 0 .or. ncomnt < 0 .or. nbtr <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0501",'// &
        '"original_return_source_line":501,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (impx > 9) write(6,'(A,A4,A,I0)') &
        ' MCCGF64: TRACK=', text4, ' FORMAT=', ifmt
    do icom = 1, ncomnt
      read(iftrak, iostat=ios)
      if (ios /= 0) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCCGF64",'// &
          '"predicate_id":"A8_MCCGF64_RETURN_L0506",'// &
          '"original_return_source_line":506,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
    end do
    read(iftrak, iostat=ios) i, ispec, n2reg, n2sou, nalbg, ncor, &
        nangl, mxsub, mxseg
    if (ios /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0510",'// &
        '"original_return_source_line":510,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (i /= NDIM .or. n2reg /= nreg .or. n2sou /= nsou) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0511",'// &
        '"original_return_source_line":511,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (ncor /= 1 .or. nangl <= 0 .or. mxsub <= 0 .or. mxseg /= nmax) &
        then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0513",'// &
        '"original_return_source_line":513,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (nalbg < 0 .or. ispec < 0 .or. len_trim(text4) > 4) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0514",'// &
        '"original_return_source_line":514,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    call SPOMOC_MCCGF_BEGIN(NGRP, ngeff, ngind, nun, NDIM, .false., &
        nlong, nreg, nsou, NANI, NLIN, NFUNL, KRYL, STIS, IAAC, ISCR, &
        0, paca, IDIR)

    allocate(matalb_trk(-nsou:nreg))
    read(iftrak, iostat=ios)
    if (ios /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0522",'// &
        '"original_return_source_line":522,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    read(iftrak, iostat=ios) (matalb_trk(j), j=-nsou,nreg)
    if (ios /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0524",'// &
        '"original_return_source_line":524,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    read(iftrak, iostat=ios)
    if (ios /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0526",'// &
        '"original_return_source_line":526,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    read(iftrak, iostat=ios)
    if (ios /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0528",'// &
        '"original_return_source_line":528,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    call MAP_REAL321(iptrk, 'XMU$MCCG', nmu, cpo_view32, map_ok)
    if (.not. map_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0531",'// &
        '"original_return_source_line":531,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(cpo32(nmu), caz1_track64(nangl), caz2_track64(nangl))
    cpo32 = cpo_view32
    read(iftrak, iostat=ios) &
        (caz1_track64(j), caz2_track64(j), j=1,nangl)
    if (ios /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0536",'// &
        '"original_return_source_line":536,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(caz1_track64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0537",'// &
        '"original_return_source_line":537,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(caz2_track64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0538",'// &
        '"original_return_source_line":538,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(cpo32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0539",'// &
        '"original_return_source_line":539,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    call MAP_REAL321(iptrk, 'WZMU$MCCG', nmu, wzmu32, map_ok)
    if (.not. map_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0542",'// &
        '"original_return_source_line":542,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(owned_wzmu32(nmu))
    call A8_OWN_LCMGET(iptrk, 'WZMU$MCCG', owned_wzmu32)
    wzmu32 => owned_wzmu32
    call MAP_REAL321(iptrk, 'ZMU$MCCG', nmu, zmu32, map_ok)
    if (.not. map_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0544",'// &
        '"original_return_source_line":544,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(owned_zmu32(nmu))
    call A8_OWN_LCMGET(iptrk, 'ZMU$MCCG', owned_zmu32)
    zmu32 => owned_zmu32
    call MAP_REAL321(iptrk, 'V$MCCG', nlong, volume_trk32, map_ok)
    if (.not. map_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0546",'// &
        '"original_return_source_line":546,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(owned_volume_trk32(nlong))
    call A8_OWN_LCMGET(iptrk, 'V$MCCG', owned_volume_trk32)
    volume_trk32 => owned_volume_trk32
    call MAP_INTEGER1(iptrk, 'NZON$MCCG', nlong, nzon_trk1, map_ok)
    if (.not. map_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0548",'// &
        '"original_return_source_line":548,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(owned_nzon_trk1(nlong))
    call A8_OWN_LCMGET(iptrk, 'NZON$MCCG', owned_nzon_trk1)
    nzon_trk1 => owned_nzon_trk1
    call MAP_INTEGER3(iptrk, 'KEYFLX$ANIS', nreg, NLIN, NFUNL, &
        keyflx_trk3, map_ok)
    if (.not. map_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0551",'// &
        '"original_return_source_line":551,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(owned_keyflx_trk3(nreg,NLIN,NFUNL))
    call A8_OWN_LCMGET(iptrk, 'KEYFLX$ANIS', owned_keyflx_trk3)
    keyflx_trk3 => owned_keyflx_trk3
    call MAP_INTEGER1(iptrk, 'KEYCUR$MCCG', nlong-nreg, keycur_trk1, &
        map_ok)
    if (.not. map_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0554",'// &
        '"original_return_source_line":554,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(owned_keycur_trk1(nlong-nreg))
    call A8_OWN_LCMGET(iptrk, 'KEYCUR$MCCG', owned_keycur_trk1)
    keycur_trk1 => owned_keycur_trk1
    if (.not. all(keyflx_base1 == keyflx_trk3(:,1,1))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0555",'// &
        '"original_return_source_line":555,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(wzmu32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0556",'// &
        '"original_return_source_line":556,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(zmu32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0557",'// &
        '"original_return_source_line":557,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(volume_trk32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0558",'// &
        '"original_return_source_line":558,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (any(volume_trk32 <= 0.0_real32)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0559",'// &
        '"original_return_source_line":559,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (any(nzon_trk1(:nreg) < 0) .or. &
        any(nzon_trk1(:nreg) > nbmix)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0561",'// &
        '"original_return_source_line":561,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (any(nzon_trk1(nreg+1:) < -NALBEDO) .or. &
        any(nzon_trk1(nreg+1:) > -1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0563",'// &
        '"original_return_source_line":563,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (any(matalb_trk(1:nreg) /= nzon_trk1(1:nreg))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0564",'// &
        '"original_return_source_line":564,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    allocate(seen(nun))
    seen = .false.
    do i = 1, nreg
      j = keyflx_trk3(i,1,1)
      if (j < 1 .or. j > nun) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCCGF64",'// &
          '"predicate_id":"A8_MCCGF64_RETURN_L0570",'// &
          '"original_return_source_line":570,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      if (seen(j)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCCGF64",'// &
          '"predicate_id":"A8_MCCGF64_RETURN_L0571",'// &
          '"original_return_source_line":571,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      seen(j) = .true.
    end do
    do i = 1, nlong-nreg
      j = keycur_trk1(i)
      if (j < 1 .or. j > nun) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCCGF64",'// &
          '"predicate_id":"A8_MCCGF64_RETURN_L0576",'// &
          '"original_return_source_line":576,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      if (seen(j)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCCGF64",'// &
          '"predicate_id":"A8_MCCGF64_RETURN_L0577",'// &
          '"original_return_source_line":577,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      seen(j) = .true.
    end do
    if (.not. all(seen)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0580",'// &
        '"original_return_source_line":580,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    call MAP_INTEGER1(iptrk, 'ICODE', NALBEDO, icode_trk1, map_ok)
    if (.not. map_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0583",'// &
        '"original_return_source_line":583,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(owned_icode_trk1(NALBEDO))
    call A8_OWN_LCMGET(iptrk, 'ICODE', owned_icode_trk1)
    icode_trk1 => owned_icode_trk1
    call MAP_REAL321(iptrk, 'ALBEDO', NALBEDO, albedo_trk32, map_ok)
    if (.not. map_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0585",'// &
        '"original_return_source_line":585,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(albedo_trk32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0586",'// &
        '"original_return_source_line":586,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    call LCMLEN(kpsys(1), 'ALBEDO', nalbp, itylcm)
    if (nalbp < 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0588",'// &
        '"original_return_source_line":588,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (any(icode_trk1 > nalbp)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0589",'// &
        '"original_return_source_line":589,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(sc_by_group32(0:nbmix,1,ngeff))
    do i = 1, ngeff
      if (.not. RECORD_MATCHES(kpsys(i), 'DRAGON-TXSC', nbmix+1, 2)) &
          then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCCGF64",'// &
          '"predicate_id":"A8_MCCGF64_RETURN_L0593",'// &
          '"original_return_source_line":593,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      if (.not. RECORD_MATCHES(kpsys(i), 'DRAGON-S0XSC', nbmix+1, 2)) &
          then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCCGF64",'// &
          '"predicate_id":"A8_MCCGF64_RETURN_L0595",'// &
          '"original_return_source_line":595,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      if (nalbp == 0) then
        call LCMLEN(kpsys(i), 'ALBEDO', j, itylcm)
        if (j /= 0) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCCGF64",'// &
            '"predicate_id":"A8_MCCGF64_RETURN_L0598",'// &
            '"original_return_source_line":598,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
      else
        call MAP_REAL321(kpsys(i), 'ALBEDO', nalbp, group_albedo32, &
            map_ok)
        if (.not. map_ok) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCCGF64",'// &
            '"predicate_id":"A8_MCCGF64_RETURN_L0602",'// &
            '"original_return_source_line":602,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        if (.not. all(ieee_is_finite(group_albedo32))) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCCGF64",'// &
            '"predicate_id":"A8_MCCGF64_RETURN_L0603",'// &
            '"original_return_source_line":603,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
      end if
      call MAP_REAL321(kpsys(i), 'DRAGON-TXSC', nbmix+1, &
          txsc_record32, map_ok)
      if (.not. map_ok) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCCGF64",'// &
          '"predicate_id":"A8_MCCGF64_RETURN_L0607",'// &
          '"original_return_source_line":607,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      if (.not. all(ieee_is_finite(txsc_record32))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCCGF64",'// &
          '"predicate_id":"A8_MCCGF64_RETURN_L0608",'// &
          '"original_return_source_line":608,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      call MAP_REAL321(kpsys(i), 'DRAGON-S0XSC', nbmix+1, &
          sc_record32, map_ok)
      if (.not. map_ok) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCCGF64",'// &
          '"predicate_id":"A8_MCCGF64_RETURN_L0611",'// &
          '"original_return_source_line":611,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      sc_by_group32(:,1,i) = sc_record32
    end do
    if (.not. all(ieee_is_finite(sc_by_group32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0614",'// &
        '"original_return_source_line":614,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    allocate(sigal32(-NALBEDO:nbmix,ngeff))
    call MCGSIG(iptrk, nbmix, ngeff, nalbp, kpsys, sigal32, lvoid)
    if (.not. all(ieee_is_finite(sigal32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0618",'// &
        '"original_return_source_line":618,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    history_capacity = 2*MAXI + 1
    if (history_capacity < 1) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0621",'// &
        '"original_return_source_line":621,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(reps64(history_capacity,ngeff),eps64(ngeff),itst(ngeff))
    allocate(nconv(ngeff))
    reps64 = +0.0_real64
    eps64 = +0.0_real64
    itst = 0
    nconv = .true.
    lnconv = ngeff

    write(6,'(A,A,A,I0,A,I0,A,I0,A,I0)') &
        ' MCCGF64-CENSUS: BEGIN TITLE="', trim(title), '" NUN=', nun, &
        ' NGEFF=', ngeff, ' KRYL=', KRYL, ' MAXI=', MAXI
    flush(6)
    child_delta64 = 0_int64
    call MCGFLX64(kpsys, iptrk, iftrak, impx, ngeff, ngind, nun, nreg, &
        nbmix, nlong, nbtr, nmax, nmu, nangl, nbatch, lc, lc0, paca, &
        matalb_trk, &
        keyflx_trk3, &
        keycur_trk1, nzon_trk1, volume_trk32, caz1_track64, &
        caz2_track64, cpo32, zmu32, wzmu32, sc_by_group32, sigal32, &
        leak1d64, &
        qfr64, phiin64, epsi64, reps64, eps64, itst, nconv, lnconv, &
        child_delta64, child_ok)
    cutoff_delta64 = cutoff_delta64 + child_delta64
    if (.not. child_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0645",'// &
        '"original_return_source_line":645,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (lnconv /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0646",'// &
        '"original_return_source_line":646,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    do i = 1, ngeff
      temp64 = eps64(i)
      if (.not. ieee_is_finite(temp64)) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCCGF64",'// &
          '"predicate_id":"A8_MCCGF64_RETURN_L0650",'// &
          '"original_return_source_line":650,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
    end do
    if (impx > 1) call PRINDM('EPS64 ', eps64, ngeff)
    if (.not. all(ieee_is_finite(phiin64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCCGF64",'// &
        '"predicate_id":"A8_MCCGF64_RETURN_L0653",'// &
        '"original_return_source_line":653,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (impx > 3) write(6,'(A,1X,A)') ' MCCGF64:', trim(title)
    write(6,'(A,A,A)') ' MCCGF64-CENSUS: END TITLE="', trim(title), '"'
    flush(6)
    ok = .true.
  end subroutine MCCGF64

  subroutine MCGFCS64(n, ndim0, nzon, qn64, fi64, m, nani0, nlin0, &
      nfunl0, sc32, leak64, s64, kpn0, nreg0, iprint, keyflx3, keycur, &
      ibc, sigal32, stis0, ok)
    integer, intent(in) :: n, ndim0, m, nani0, nlin0, nfunl0
    integer, intent(in) :: kpn0, nreg0, iprint, stis0
    integer, intent(in) :: nzon(n), keycur(n-nreg0), ibc(n-nreg0)
    integer, intent(in) :: keyflx3(nreg0,nlin0,nfunl0)
    real(real64), intent(in) :: qn64(kpn0), fi64(kpn0)
    real(real64), intent(in) :: leak64
    real(real64), intent(inout) :: s64(kpn0)
    real(real32), intent(in) :: sc32(0:m,nani0)
    real(real32), intent(in) :: sigal32(-NALBEDO:m)
    logical, intent(out) :: ok

    integer :: ibm, ind, ind2, ir, isur, isur2

    ok = .false.
    if (n <= 0 .or. m <= 0 .or. kpn0 <= 0 .or. nreg0 <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFCS64",'// &
        '"predicate_id":"A8_MCGFCS64_RETURN_L0677",'// &
        '"original_return_source_line":677,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (nreg0 >= n .or. kpn0 /= n) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFCS64",'// &
        '"predicate_id":"A8_MCGFCS64_RETURN_L0678",'// &
        '"original_return_source_line":678,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (ndim0 /= NDIM) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFCS64",'// &
        '"predicate_id":"A8_MCGFCS64_RETURN_L0679",'// &
        '"original_return_source_line":679,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (nani0 /= NANI .or. nlin0 /= NLIN .or. nfunl0 /= NFUNL) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFCS64",'// &
        '"predicate_id":"A8_MCGFCS64_RETURN_L0680",'// &
        '"original_return_source_line":680,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (stis0 /= STIS) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFCS64",'// &
        '"predicate_id":"A8_MCGFCS64_RETURN_L0681",'// &
        '"original_return_source_line":681,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(qn64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFCS64",'// &
        '"predicate_id":"A8_MCGFCS64_RETURN_L0682",'// &
        '"original_return_source_line":682,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(fi64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFCS64",'// &
        '"predicate_id":"A8_MCGFCS64_RETURN_L0683",'// &
        '"original_return_source_line":683,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(s64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFCS64",'// &
        '"predicate_id":"A8_MCGFCS64_RETURN_L0684",'// &
        '"original_return_source_line":684,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(sc32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFCS64",'// &
        '"predicate_id":"A8_MCGFCS64_RETURN_L0685",'// &
        '"original_return_source_line":685,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(sigal32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFCS64",'// &
        '"predicate_id":"A8_MCGFCS64_RETURN_L0686",'// &
        '"original_return_source_line":686,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    do ir = 1, n
      ibm = nzon(ir)
      if (ibm < 0) then
        if (ibm < -NALBEDO) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGFCS64",'// &
            '"predicate_id":"A8_MCGFCS64_RETURN_L0691",'// &
            '"original_return_source_line":691,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        isur = ir - nreg0
        if (isur < 1 .or. isur > n-nreg0) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGFCS64",'// &
            '"predicate_id":"A8_MCGFCS64_RETURN_L0693",'// &
            '"original_return_source_line":693,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        isur2 = ibc(isur)
        if (isur2 < 1 .or. isur2 > n-nreg0) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGFCS64",'// &
            '"predicate_id":"A8_MCGFCS64_RETURN_L0695",'// &
            '"original_return_source_line":695,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        ind = keycur(isur)
        ind2 = keycur(isur2)
        if (ind < 1 .or. ind > kpn0) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGFCS64",'// &
            '"predicate_id":"A8_MCGFCS64_RETURN_L0698",'// &
            '"original_return_source_line":698,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        if (ind2 < 1 .or. ind2 > kpn0) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGFCS64",'// &
            '"predicate_id":"A8_MCGFCS64_RETURN_L0699",'// &
            '"original_return_source_line":699,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        s64(ind) = real(sigal32(ibm), real64) * fi64(ind2)
      else
        if (ibm > m) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGFCS64",'// &
            '"predicate_id":"A8_MCGFCS64_RETURN_L0702",'// &
            '"original_return_source_line":702,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        if (ir > nreg0) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGFCS64",'// &
            '"predicate_id":"A8_MCGFCS64_RETURN_L0703",'// &
            '"original_return_source_line":703,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        ind = keyflx3(ir,1,1)
        if (ind < 1 .or. ind > kpn0) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGFCS64",'// &
            '"predicate_id":"A8_MCGFCS64_RETURN_L0705",'// &
            '"original_return_source_line":705,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        s64(ind) = qn64(ind) + &
            (real(sc32(ibm,1), real64) - leak64) * fi64(ind)
      end if
    end do
    if (.not. all(ieee_is_finite(s64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFCS64",'// &
        '"predicate_id":"A8_MCGFCS64_RETURN_L0710",'// &
        '"original_return_source_line":710,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (iprint > 6) call PRINDM('S64   ', s64, kpn0)
    ok = .true.
  end subroutine MCGFCS64

  subroutine MCGFL164(kpsys, iptrk, iftrak, iprint, ngeff, ngind, nun, &
      nreg, nbmix, nlong, nbtr, nmax, nmu, nangl, nbatch, lc, lc0, &
      paca, &
      matalb_trk, keyflx_trk3, &
      keycur_trk1, nzon_trk1, volume_trk32, caz1_track64, &
      caz2_track64, cpo32, zmu32, wzmu32, sc_by_group32, sigal32, &
      leak1d64, &
      qfr64, phiin64, source64, response64, nconv, epsacc64, &
      cutoff_delta64, ok)
    use GANLIB, only : A8_OWN_LCMGET => LCMGET
    integer, intent(in) :: iftrak, iprint, ngeff, nun, nreg, nbmix
    integer, intent(in) :: nlong, nbtr, nmax
    integer, intent(in) :: nmu, nangl, nbatch, lc, lc0, paca
    real(real64), intent(in) :: leak1d64(:)
    type(c_ptr), intent(in) :: kpsys(ngeff), iptrk
    real(real64) :: leak_slot64(ngeff)
    integer, intent(in) :: ngind(ngeff)
    integer, intent(in) :: matalb_trk(-(nlong-nreg):nreg)
    integer, intent(in) :: keyflx_trk3(nreg,NLIN,NFUNL)
    integer, intent(in) :: keycur_trk1(nlong-nreg), nzon_trk1(nlong)
    real(real32), intent(in) :: volume_trk32(nlong), cpo32(nmu)
    real(real32), intent(in) :: zmu32(nmu), wzmu32(nmu)
    real(real32), intent(in) :: sc_by_group32(0:nbmix,1,ngeff)
    real(real32), intent(in) :: sigal32(-NALBEDO:nbmix,ngeff)
    real(real64), intent(in) :: caz1_track64(nangl)
    real(real64), intent(in) :: caz2_track64(nangl)
    real(real64), intent(in) :: qfr64(nun,ngeff), phiin64(nun,ngeff)
    real(real64), intent(inout) :: source64(nun,ngeff)
    real(real64), intent(out) :: response64(nun,ngeff)
    logical, intent(in) :: nconv(ngeff)
    real(real64), intent(in) :: epsacc64
    integer(int64), intent(out) :: cutoff_delta64
    logical, intent(out) :: ok

    character(len=4) :: text4
    external :: MCGFFAR, MCGFFAL, MCGFFIR64_RANK_ADAPTER, MCGSCA
    integer :: i, icom, ifmt, ios, ispec, ncomnt, ncor
    integer :: n2reg, n2sou, nalbg, nangl_check, mxsub, mxseg, nsou
    integer :: isgnr(4,NFUNL), keyani(NFUNL)
    integer(int64) :: child_delta64
    integer, contiguous, pointer :: bc_index_trk1(:), im(:), iperm(:)
    integer, contiguous, pointer :: im0_view(:), ju(:), mcu(:)
    integer, contiguous, pointer :: mcu0_view(:), pjjind_trk2(:,:)
    integer, allocatable, target :: im0_data(:), mcu0_data(:)
    integer, allocatable, target :: owned_bc_index_trk1(:)
    integer, allocatable, target :: owned_pjjind_trk2(:,:)
    integer, allocatable, target :: owned_im(:), owned_mcu(:)
    integer, allocatable, target :: owned_iperm(:), owned_ju(:)
    logical :: child_ok, map_ok
    real(real32), contiguous, pointer :: record32(:)
    real(real32), allocatable :: cf32(:,:), cq32(:,:), diagf32(:,:)
    real(real32), allocatable :: diagq32(:,:), iludf32(:,:), ilucf32(:,:)
    real(real64), allocatable :: caz0_inactive64(:), xsi_inactive64(:)

    cutoff_delta64 = 0_int64
    ok = .false.
    response64 = 0.0_real64
    if (ngeff <= 0 .or. ngeff > NGRP .or. nun <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0767",'// &
        '"original_return_source_line":767,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (nreg <= 0 .or. nbmix <= 0 .or. nlong <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0768",'// &
        '"original_return_source_line":768,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (nlong <= nreg .or. nun /= nlong) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0769",'// &
        '"original_return_source_line":769,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    nsou = nlong - nreg
    if (nbtr <= 0 .or. nmax <= 0 .or. nmu <= 0 .or. nangl <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0771",'// &
        '"original_return_source_line":771,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (nbatch <= 0 .or. lc <= 0 .or. iftrak <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0772",'// &
        '"original_return_source_line":772,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (paca /= 3 .and. paca /= 4) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0773",'// &
        '"original_return_source_line":773,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (paca == 3) then
      if (lc0 <= 0) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCGFL164",'// &
          '"predicate_id":"A8_MCGFL164_RETURN_L0775",'// &
          '"original_return_source_line":775,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
    else
      if (lc0 /= 0) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCGFL164",'// &
          '"predicate_id":"A8_MCGFL164_RETURN_L0777",'// &
          '"original_return_source_line":777,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
    end if
    if (.not. c_associated(iptrk)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0779",'// &
        '"original_return_source_line":779,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    do i = 1, ngeff
      if (.not. c_associated(kpsys(i))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCGFL164",'// &
          '"predicate_id":"A8_MCGFL164_RETURN_L0781",'// &
          '"original_return_source_line":781,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
    end do
    if (ngind(1) /= NGRP-ngeff+1 .or. ngind(ngeff) /= NGRP) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0783",'// &
        '"original_return_source_line":783,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    do i = 2, ngeff
      if (ngind(i) /= ngind(i-1)+1) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCGFL164",'// &
          '"predicate_id":"A8_MCGFL164_RETURN_L0785",'// &
          '"original_return_source_line":785,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
    end do
    if (.not. any(nconv)) then
      ok = .true.
      return
    end if
    if (.not. ieee_is_finite(epsacc64) .or. epsacc64 < 0.0_real64) &
        then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0792",'// &
        '"original_return_source_line":792,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(qfr64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0793",'// &
        '"original_return_source_line":793,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(phiin64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0794",'// &
        '"original_return_source_line":794,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(source64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0795",'// &
        '"original_return_source_line":795,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(volume_trk32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0796",'// &
        '"original_return_source_line":796,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(caz1_track64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0797",'// &
        '"original_return_source_line":797,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(caz2_track64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0798",'// &
        '"original_return_source_line":798,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(cpo32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0799",'// &
        '"original_return_source_line":799,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(zmu32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0800",'// &
        '"original_return_source_line":800,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(wzmu32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0801",'// &
        '"original_return_source_line":801,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(sc_by_group32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0802",'// &
        '"original_return_source_line":802,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(sigal32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0803",'// &
        '"original_return_source_line":803,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (any(matalb_trk(1:nreg) /= nzon_trk1(1:nreg))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0804",'// &
        '"original_return_source_line":804,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    call MAP_INTEGER1(iptrk, 'BC-REFL+TRAN', nlong-nreg, &
        bc_index_trk1, map_ok)
    if (.not. map_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0808",'// &
        '"original_return_source_line":808,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(owned_bc_index_trk1(nlong-nreg))
    call A8_OWN_LCMGET(iptrk, 'BC-REFL+TRAN', owned_bc_index_trk1)
    bc_index_trk1 => owned_bc_index_trk1
    if (any(bc_index_trk1 < 1) .or. &
        any(bc_index_trk1 > nlong-nreg)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0810",'// &
        '"original_return_source_line":810,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    call MAP_INTEGER2(iptrk, 'PJJIND$MCCG', NFUNL, 2, &
        pjjind_trk2, map_ok)
    if (.not. map_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0813",'// &
        '"original_return_source_line":813,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(owned_pjjind_trk2(NFUNL,2))
    call A8_OWN_LCMGET(iptrk, 'PJJIND$MCCG', owned_pjjind_trk2)
    pjjind_trk2 => owned_pjjind_trk2
    if (any(pjjind_trk2 /= 1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0814",'// &
        '"original_return_source_line":814,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    do i = 1, ngeff
      if (nconv(i)) then
        if (.not. RECORD_MATCHES(kpsys(i), 'PJJ$MCCG', &
            nreg*NFUNL, 2)) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGFL164",'// &
            '"predicate_id":"A8_MCGFL164_RETURN_L0818",'// &
            '"original_return_source_line":818,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
      end if
    end do

    do i = 1, ngeff
      if (nconv(i)) then
        call MCGFCS64(nlong, NDIM, nzon_trk1, qfr64(:,i), &
            phiin64(:,i), nbmix, NANI, NLIN, NFUNL, &
            sc_by_group32(:,:,i), leak1d64(ngind(i)), source64(:,i), &
            nun, nreg, iprint, &
            keyflx_trk3, keycur_trk1, bc_index_trk1, sigal32(:,i), &
            STIS, child_ok)
        if (.not. child_ok) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGFL164",'// &
            '"predicate_id":"A8_MCGFL164_RETURN_L0830",'// &
            '"original_return_source_line":830,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
      end if
    end do

    call MOCIK3(NANI-1, NFUNL, 4, isgnr, keyani)
    if (keyani(1) /= 0 .or. .not. all(isgnr(:,1) == 1)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0835",'// &
        '"original_return_source_line":835,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(caz0_inactive64(nangl), xsi_inactive64(nsou))
    caz0_inactive64 = +0.0_real64
    xsi_inactive64 = +0.0_real64

    rewind(iftrak, iostat=ios)
    if (ios /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0841",'// &
        '"original_return_source_line":841,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    read(iftrak, iostat=ios) text4, ncomnt, i, ifmt
    if (ios /= 0 .or. ncomnt < 0 .or. i /= nbtr) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0843",'// &
        '"original_return_source_line":843,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (iprint > 9) write(6,'(A,A4,A,I0)') &
        ' MCGFL164: TRACK=', text4, ' FORMAT=', ifmt
    do icom = 1, ncomnt
      read(iftrak, iostat=ios)
      if (ios /= 0) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCGFL164",'// &
          '"predicate_id":"A8_MCGFL164_RETURN_L0848",'// &
          '"original_return_source_line":848,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
    end do
    read(iftrak, iostat=ios) i, ispec, n2reg, n2sou, nalbg, ncor, &
        nangl_check, mxsub, mxseg
    if (ios /= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0852",'// &
        '"original_return_source_line":852,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (i /= NDIM .or. n2reg /= nreg .or. n2sou /= nsou) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0853",'// &
        '"original_return_source_line":853,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (ncor /= 1 .or. nangl_check /= nangl) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0854",'// &
        '"original_return_source_line":854,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (ispec < 0 .or. nalbg < 0 .or. mxsub <= 0 .or. mxseg /= nmax) &
        then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0856",'// &
        '"original_return_source_line":856,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    do icom = 1, 6
      read(iftrak, iostat=ios)
      if (ios /= 0) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCGFL164",'// &
          '"predicate_id":"A8_MCGFL164_RETURN_L0859",'// &
          '"original_return_source_line":859,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
    end do

    call MCGFCF(MCGFFIR64_RANK_ADAPTER, MCGFFAR, MCGFFAL, MCGSCA, &
        iftrak, nbtr, nmax, NDIM, nun, nlong, nreg, nbmix, ngeff, &
        nangl, nmu, NANI, NFUNL, 4, NANI, NLIN, NFUNL, keyflx_trk3, &
        keycur_trk1, nzon_trk1, nconv, caz0_inactive64, caz1_track64, &
        caz2_track64, cpo32, zmu32, wzmu32, source64, sigal32, isgnr, &
        IDIR, nsou, nbatch, xsi_inactive64, response64)
    if (.not. all(ieee_is_finite(response64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0868",'// &
        '"original_return_source_line":868,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    call MCGFST(ngeff, kpsys, nconv, nun, nlong, nreg, NANI, NFUNL, &
        NFUNL, keyflx_trk3(:,1,:), keycur_trk1, pjjind_trk2, &
        nzon_trk1, volume_trk32, source64, response64, IDIR)
    if (.not. all(ieee_is_finite(response64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0873",'// &
        '"original_return_source_line":873,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    call SPOMOC_CAPTURE64(ngeff, ngind, nun, qfr64, phiin64, source64, &
        response64, nconv)

    call MAP_INTEGER1(iptrk, 'IM$MCCG', nlong+1, im, map_ok)
    if (.not. map_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0879",'// &
        '"original_return_source_line":879,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(owned_im(nlong+1))
    call A8_OWN_LCMGET(iptrk, 'IM$MCCG', owned_im)
    im => owned_im
    call MAP_INTEGER1(iptrk, 'MCU$MCCG', lc, mcu, map_ok)
    if (.not. map_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0881",'// &
        '"original_return_source_line":881,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(owned_mcu(lc))
    call A8_OWN_LCMGET(iptrk, 'MCU$MCCG', owned_mcu)
    mcu => owned_mcu
    call MAP_INTEGER1(iptrk, 'PI$MCCG', nlong, iperm, map_ok)
    if (.not. map_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0883",'// &
        '"original_return_source_line":883,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(owned_iperm(nlong))
    call A8_OWN_LCMGET(iptrk, 'PI$MCCG', owned_iperm)
    iperm => owned_iperm
    call MAP_INTEGER1(iptrk, 'JU$MCCG', nlong, ju, map_ok)
    if (.not. map_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0885",'// &
        '"original_return_source_line":885,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    allocate(owned_ju(nlong))
    call A8_OWN_LCMGET(iptrk, 'JU$MCCG', owned_ju)
    ju => owned_ju

    if (paca == 3) then
      call MAP_INTEGER1(iptrk, 'IM0$MCCG', nlong+1, im0_view, map_ok)
      if (.not. map_ok) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCGFL164",'// &
          '"predicate_id":"A8_MCGFL164_RETURN_L0889",'// &
          '"original_return_source_line":889,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      allocate(im0_data(nlong+1))
      call A8_OWN_LCMGET(iptrk, 'IM0$MCCG', im0_data)
      im0_view => im0_data
      call MAP_INTEGER1(iptrk, 'MCU0$MCCG', lc0, mcu0_view, map_ok)
      if (.not. map_ok) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCGFL164",'// &
          '"predicate_id":"A8_MCGFL164_RETURN_L0891",'// &
          '"original_return_source_line":891,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      allocate(mcu0_data(lc0))
      call A8_OWN_LCMGET(iptrk, 'MCU0$MCCG', mcu0_data)
      mcu0_view => mcu0_data
      im0_data = im0_view
      mcu0_data = mcu0_view
    else
      allocate(im0_data(nlong+1),mcu0_data(0))
      im0_data = 0
    end if

    allocate(diagq32(nlong,ngeff), cq32(lc,ngeff))
    allocate(iludf32(nlong,ngeff), cf32(lc,ngeff))
    allocate(ilucf32(lc0,ngeff))
    allocate(diagf32(nlong,ngeff))
    ilucf32 = +0.0_real32
    do i = 1, ngeff
      call MAP_REAL321(kpsys(i), 'DIAGQ$MCCG', nlong, record32, map_ok)
      if (.not. map_ok) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCGFL164",'// &
          '"predicate_id":"A8_MCGFL164_RETURN_L0907",'// &
          '"original_return_source_line":907,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      diagq32(:,i) = record32
      call MAP_REAL321(kpsys(i), 'CQ$MCCG', lc, record32, map_ok)
      if (.not. map_ok) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCGFL164",'// &
          '"predicate_id":"A8_MCGFL164_RETURN_L0910",'// &
          '"original_return_source_line":910,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      cq32(:,i) = record32
      call MAP_REAL321(kpsys(i), 'ILUDF$MCCG', nlong, record32, map_ok)
      if (.not. map_ok) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCGFL164",'// &
          '"predicate_id":"A8_MCGFL164_RETURN_L0913",'// &
          '"original_return_source_line":913,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      iludf32(:,i) = record32
      if (paca == 3) then
        call MAP_REAL321(kpsys(i), 'ILUCF$MCCG', lc0, record32, map_ok)
        if (.not. map_ok) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGFL164",'// &
            '"predicate_id":"A8_MCGFL164_RETURN_L0917",'// &
            '"original_return_source_line":917,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        ilucf32(:,i) = record32
      end if
      call MAP_REAL321(kpsys(i), 'CF$MCCG', lc, record32, map_ok)
      if (.not. map_ok) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCGFL164",'// &
          '"predicate_id":"A8_MCGFL164_RETURN_L0921",'// &
          '"original_return_source_line":921,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      cf32(:,i) = record32
      call MAP_REAL321(kpsys(i), 'DIAGF$MCCG', nlong, record32, map_ok)
      if (.not. map_ok) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCGFL164",'// &
          '"predicate_id":"A8_MCGFL164_RETURN_L0924",'// &
          '"original_return_source_line":924,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      diagf32(:,i) = record32
    end do
    if (.not. all(ieee_is_finite(diagq32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0927",'// &
        '"original_return_source_line":927,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(cq32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0928",'// &
        '"original_return_source_line":928,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(iludf32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0929",'// &
        '"original_return_source_line":929,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(ilucf32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0930",'// &
        '"original_return_source_line":930,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(cf32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0931",'// &
        '"original_return_source_line":931,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(diagf32))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0932",'// &
        '"original_return_source_line":932,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    child_delta64 = 0_int64
    do i = 1, ngeff
      leak_slot64(i) = leak1d64(ngind(i))
    end do
    call MCGFCA64(nlong, ngeff, nun, nreg, nbmix, lc, lc0, LFORW, &
        paca, &
        keyflx_trk3(:,1,:), keycur_trk1, nzon_trk1, nconv, MAXACC, &
        epsacc64, response64, phiin64, sc_by_group32, leak_slot64, &
        im, mcu, iperm, ju, im0_data, mcu0_data, diagq32, cq32, &
        iludf32, ilucf32, cf32, diagf32, child_delta64, &
        child_ok)
    cutoff_delta64 = cutoff_delta64 + child_delta64
    if (.not. child_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0946",'// &
        '"original_return_source_line":946,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(response64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFL164",'// &
        '"predicate_id":"A8_MCGFL164_RETURN_L0947",'// &
        '"original_return_source_line":947,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    ok = .true.
  end subroutine MCGFL164

  subroutine MCGFLX64(kpsys, iptrk, iftrak, iprint, ngeff, ngind, nun, &
      nreg, nbmix, nlong, nbtr, nmax, nmu, nangl, nbatch, lc, lc0, &
      paca, &
      matalb_trk, keyflx_trk3, &
      keycur_trk1, nzon_trk1, volume_trk32, caz1_track64, &
      caz2_track64, cpo32, zmu32, wzmu32, sc_by_group32, sigal32, &
      leak1d64, &
      qfr64, phiin64, epsi64, reps64, eps64, itst, nconv, lnconv, &
      cutoff_delta64, ok)
    integer, intent(in) :: iftrak, iprint, ngeff, nun, nreg, nbmix
    integer, intent(in) :: nlong, nbtr, nmax
    integer, intent(in) :: nmu, nangl, nbatch, lc, lc0, paca
    real(real64), intent(in) :: leak1d64(:)
    type(c_ptr), intent(in) :: kpsys(ngeff), iptrk
    integer, intent(in) :: ngind(ngeff)
    integer, intent(in) :: matalb_trk(-(nlong-nreg):nreg)
    integer, intent(in) :: keyflx_trk3(nreg,NLIN,NFUNL)
    integer, intent(in) :: keycur_trk1(nlong-nreg), nzon_trk1(nlong)
    integer, intent(out) :: itst(ngeff)
    integer, intent(inout) :: lnconv
    real(real32), intent(in) :: volume_trk32(nlong), cpo32(nmu)
    real(real32), intent(in) :: zmu32(nmu), wzmu32(nmu)
    real(real32), intent(in) :: sc_by_group32(0:nbmix,1,ngeff)
    real(real32), intent(in) :: sigal32(-NALBEDO:nbmix,ngeff)
    real(real64), intent(in) :: caz1_track64(nangl)
    real(real64), intent(in) :: caz2_track64(nangl)
    real(real64), intent(in) :: qfr64(nun,ngeff), epsi64
    real(real64), intent(inout) :: phiin64(nun,ngeff)
    real(real64), intent(out) :: reps64(:,:), eps64(ngeff)
    logical, intent(inout) :: nconv(ngeff)
    integer(int64), intent(out) :: cutoff_delta64
    logical, intent(out) :: ok

    integer :: ii
    integer(int64) :: child_delta64
    logical :: child_ok
    real(real64), allocatable :: response64(:,:), source64(:,:)

    cutoff_delta64 = 0_int64
    ok = .false.
    if (ngeff <= 0 .or. ngeff > NGRP .or. nun <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFLX64",'// &
        '"predicate_id":"A8_MCGFLX64_RETURN_L0991",'// &
        '"original_return_source_line":991,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (nreg <= 0 .or. nbmix <= 0 .or. nlong <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFLX64",'// &
        '"predicate_id":"A8_MCGFLX64_RETURN_L0992",'// &
        '"original_return_source_line":992,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (nlong <= nreg .or. nun /= nlong) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFLX64",'// &
        '"predicate_id":"A8_MCGFLX64_RETURN_L0993",'// &
        '"original_return_source_line":993,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (KRYL /= 10 .or. MAXI /= 20) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFLX64",'// &
        '"predicate_id":"A8_MCGFLX64_RETURN_L0994",'// &
        '"original_return_source_line":994,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(reps64,1) /= 2*MAXI+1 .or. &
        size(reps64,2) /= ngeff) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFLX64",'// &
        '"predicate_id":"A8_MCGFLX64_RETURN_L0996",'// &
        '"original_return_source_line":996,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. ieee_is_finite(epsi64) .or. epsi64 <= 0.0_real64) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFLX64",'// &
        '"predicate_id":"A8_MCGFLX64_RETURN_L0997",'// &
        '"original_return_source_line":997,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(qfr64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFLX64",'// &
        '"predicate_id":"A8_MCGFLX64_RETURN_L0998",'// &
        '"original_return_source_line":998,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(phiin64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFLX64",'// &
        '"predicate_id":"A8_MCGFLX64_RETURN_L0999",'// &
        '"original_return_source_line":999,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. any(nconv)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFLX64",'// &
        '"predicate_id":"A8_MCGFLX64_RETURN_L1000",'// &
        '"original_return_source_line":1000,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    allocate(source64(nun,ngeff), response64(nun,ngeff))
    SOURCE64 = 0.0_REAL64
    reps64 = +0.0_real64
    eps64 = +0.0_real64
    itst = 0
    if (iprint > 5) then
      do ii = 1, ngeff
        call PRINDM('FI-0  ', phiin64(:,ii), nun)
      end do
    end if

    child_delta64 = 0_int64
    call MCGMRE64(kpsys, iptrk, iftrak, iprint, ngeff, ngind, nun, &
        nreg, nbmix, nlong, nbtr, nmax, nmu, nangl, nbatch, lc, lc0, &
        paca, &
        matalb_trk, keyflx_trk3, &
        keycur_trk1, nzon_trk1, volume_trk32, caz1_track64, &
        caz2_track64, cpo32, zmu32, wzmu32, sc_by_group32, sigal32, &
        leak1d64, &
        qfr64, phiin64, source64, response64, epsi64, reps64, eps64, &
        itst, nconv, lnconv, child_delta64, child_ok)
    cutoff_delta64 = cutoff_delta64 + child_delta64
    if (.not. child_ok) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFLX64",'// &
        '"predicate_id":"A8_MCGFLX64_RETURN_L1024",'// &
        '"original_return_source_line":1024,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(phiin64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGFLX64",'// &
        '"predicate_id":"A8_MCGFLX64_RETURN_L1025",'// &
        '"original_return_source_line":1025,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    ok = .true.
  end subroutine MCGFLX64
  subroutine MCGMRE64(kpsys, iptrk, iftrak, iprint, ngeff, ngind, nun, &
      nreg, nbmix, nlong, nbtr, nmax, nmu, nangl, nbatch, lc, lc0, &
      paca, &
      matalb_trk, keyflx_trk3, &
      keycur_trk1, nzon_trk1, volume_trk32, caz1_track64, &
      caz2_track64, cpo32, zmu32, wzmu32, sc_by_group32, sigal32, &
      leak1d64, &
      qfr64, phiin64, source64, response64, epsi64, reps64, eps64, &
      itst, nconv, lnconv, cutoff_delta64, ok)
    integer, intent(in) :: iftrak, iprint, ngeff, nun, nreg, nbmix
    integer, intent(in) :: nlong, nbtr, nmax
    integer, intent(in) :: nmu, nangl, nbatch, lc, lc0, paca
    real(real64), intent(in) :: leak1d64(:)
    type(c_ptr), intent(in) :: kpsys(ngeff), iptrk
    integer, intent(in) :: ngind(ngeff)
    integer, intent(in) :: matalb_trk(-(nlong-nreg):nreg)
    integer, intent(in) :: keyflx_trk3(nreg,NLIN,NFUNL)
    integer, intent(in) :: keycur_trk1(nlong-nreg), nzon_trk1(nlong)
    integer, intent(inout) :: itst(ngeff), lnconv
    real(real32), intent(in) :: volume_trk32(nlong), cpo32(nmu)
    real(real32), intent(in) :: zmu32(nmu), wzmu32(nmu)
    real(real32), intent(in) :: sc_by_group32(0:nbmix,1,ngeff)
    real(real32), intent(in) :: sigal32(-NALBEDO:nbmix,ngeff)
    real(real64), intent(in) :: caz1_track64(nangl)
    real(real64), intent(in) :: caz2_track64(nangl)
    real(real64), intent(in) :: qfr64(nun,ngeff), epsi64
    real(real64), intent(inout) :: phiin64(nun,ngeff)
    real(real64), intent(inout) :: source64(nun,ngeff)
    real(real64), intent(out) :: response64(nun,ngeff)
    real(real64), intent(inout) :: reps64(:,:), eps64(ngeff)
    logical, intent(inout) :: nconv(ngeff)
    integer(int64), intent(out) :: cutoff_delta64
    logical, intent(out) :: ok

    integer :: history_capacity, i, ii, iter, j, k, l, narnoldi
    integer :: restart_dimension
    integer, allocatable :: kmax(:)
    integer(int64) :: child_delta64
    logical :: child_ok, rhs_pending
    logical, allocatable :: krylov_active(:)
    real(real64) :: epsinto64, hr64, w1, w2, znu64
    real(real64), allocatable :: denom64(:), rho64(:)
    real(real64), allocatable :: rhs64(:,:), gar64(:,:), flout64(:,:)
    real(real64), allocatable :: residual64(:,:), g64(:,:), c64(:,:)
    real(real64), allocatable :: sn64(:,:), v64(:,:,:), h64(:,:,:)

    cutoff_delta64 = 0_int64
    ok = .false.
    response64 = +0.0_real64
    if (MAXI /= 20) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGMRE64",'// &
        '"predicate_id":"A8_MCGMRE64_RETURN_L1077",'// &
        '"original_return_source_line":1077,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (ngeff <= 0 .or. ngeff > NGRP .or. nun <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGMRE64",'// &
        '"predicate_id":"A8_MCGMRE64_RETURN_L1078",'// &
        '"original_return_source_line":1078,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (nreg <= 0 .or. nbmix <= 0 .or. nlong <= 0) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGMRE64",'// &
        '"predicate_id":"A8_MCGMRE64_RETURN_L1079",'// &
        '"original_return_source_line":1079,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (nlong <= nreg .or. nun /= nlong) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGMRE64",'// &
        '"predicate_id":"A8_MCGMRE64_RETURN_L1080",'// &
        '"original_return_source_line":1080,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (epsi64 <= 0.0_real64 .or. .not. ieee_is_finite(epsi64)) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGMRE64",'// &
        '"predicate_id":"A8_MCGMRE64_RETURN_L1081",'// &
        '"original_return_source_line":1081,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(qfr64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGMRE64",'// &
        '"predicate_id":"A8_MCGMRE64_RETURN_L1082",'// &
        '"original_return_source_line":1082,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(phiin64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGMRE64",'// &
        '"predicate_id":"A8_MCGMRE64_RETURN_L1083",'// &
        '"original_return_source_line":1083,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(source64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGMRE64",'// &
        '"predicate_id":"A8_MCGMRE64_RETURN_L1084",'// &
        '"original_return_source_line":1084,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    restart_dimension = KRYL
    history_capacity = 2*MAXI + 1
    if (restart_dimension <= 0 .or. restart_dimension > nun) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGMRE64",'// &
        '"predicate_id":"A8_MCGMRE64_RETURN_L1087",'// &
        '"original_return_source_line":1087,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (size(reps64,1) /= history_capacity .or. &
        size(reps64,2) /= ngeff) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGMRE64",'// &
        '"predicate_id":"A8_MCGMRE64_RETURN_L1089",'// &
        '"original_return_source_line":1089,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if

    epsinto64 = epsi64 / 100.0_real64
    allocate(denom64(ngeff), rho64(ngeff), kmax(ngeff))
    allocate(rhs64(nun,ngeff), gar64(nun,ngeff), flout64(nun,ngeff))
    allocate(residual64(nun,ngeff), g64(restart_dimension+1,ngeff))
    allocate(c64(restart_dimension+1,ngeff))
    allocate(sn64(restart_dimension+1,ngeff))
    allocate(v64(nun,ngeff,restart_dimension+1))
    allocate(h64(restart_dimension+1,restart_dimension,ngeff))
    allocate(krylov_active(ngeff))

    rho64 = +0.0_real64
    do ii = 1, ngeff
      denom64(ii) = sqrt(dot_product(qfr64(:,ii), qfr64(:,ii)))
      if (.not. ieee_is_finite(denom64(ii))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCGMRE64",'// &
          '"predicate_id":"A8_MCGMRE64_RETURN_L1104",'// &
          '"original_return_source_line":1104,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      nconv(ii) = nconv(ii) .and. denom64(ii) > 0.0_real64
      itst(ii) = 0
      eps64(ii) = +0.0_real64
    end do
    lnconv = count(nconv)
    if (lnconv == 0) then
      ok = .true.
      return
    end if
    rhs_pending = .true.
    iter = 0
    narnoldi = 0

    do while (lnconv /= 0)
      if (iter >= history_capacity) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCGMRE64",'// &
          '"predicate_id":"A8_MCGMRE64_RETURN_L1119",'// &
          '"original_return_source_line":1119,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      iter = iter + 1
      call SPOMOC_SET_ROLE(1, iter)
      child_delta64 = 0_int64
      call MCGFL164(kpsys, iptrk, iftrak, iprint, ngeff, ngind, nun, &
          nreg, nbmix, nlong, nbtr, nmax, nmu, nangl, nbatch, lc, &
          lc0, paca, matalb_trk, keyflx_trk3, &
          keycur_trk1, nzon_trk1, volume_trk32, caz1_track64, &
          caz2_track64, cpo32, zmu32, wzmu32, sc_by_group32, sigal32, &
          leak1d64, &
          qfr64, phiin64, source64, response64, nconv, epsinto64, &
          child_delta64, child_ok)
      cutoff_delta64 = cutoff_delta64 + child_delta64
      if (.not. child_ok) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCGMRE64",'// &
          '"predicate_id":"A8_MCGMRE64_RETURN_L1132",'// &
          '"original_return_source_line":1132,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      if (.not. all(ieee_is_finite(response64))) then
        write(6,'(A,I0,A)') &
          '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
          '"scope":"MCGMRE64",'// &
          '"predicate_id":"A8_MCGMRE64_RETURN_L1133",'// &
          '"original_return_source_line":1133,'// &
          '"actual_boolean_status_integer":',merge(1,0,ok),'}'
        flush(6)
        return
      end if
      if (iter == 1) call SPOMOC_PUBLISH()

      do ii = 1, ngeff
        reps64(iter,ii) = +0.0_real64
        if (.not. nconv(ii)) cycle
        residual64(:,ii) = response64(:,ii) - phiin64(:,ii)
        rho64(ii) = sqrt(dot_product(residual64(:,ii), &
            residual64(:,ii)))
        if (.not. ieee_is_finite(rho64(ii))) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGMRE64",'// &
            '"predicate_id":"A8_MCGMRE64_RETURN_L1142",'// &
            '"original_return_source_line":1142,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        reps64(iter,ii) = rho64(ii) / denom64(ii)
        if (.not. ieee_is_finite(reps64(iter,ii))) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGMRE64",'// &
            '"predicate_id":"A8_MCGMRE64_RETURN_L1144",'// &
            '"original_return_source_line":1144,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        eps64(ii) = reps64(iter,ii)
        itst(ii) = iter
        nconv(ii) = nconv(ii) .and. &
            rho64(ii) >= epsi64 * denom64(ii)
      end do
      lnconv = count(nconv)
      write(6,'(A,I0,A,I0,A,1P,E13.5)') &
          ' MCGMRE64-CENSUS: TRUE ITER=', iter, ' GROUPS=', lnconv, &
          ' MAX-EPS=', maxval(reps64(iter,:))
      flush(6)
      if (lnconv == 0) exit
      ! MAXI limits Arnoldi work only.  The check is deliberately after this
      ! fresh residual so the last permitted update can still be accepted.
      if (narnoldi >= MAXI) exit
      krylov_active = nconv

      h64 = +0.0_real64
      v64 = +0.0_real64
      c64 = +0.0_real64
      sn64 = +0.0_real64
      g64 = +0.0_real64
      kmax = 0
      do ii = 1, ngeff
        if (.not. krylov_active(ii)) cycle
        if (rho64(ii) <= 0.0_real64) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGMRE64",'// &
            '"predicate_id":"A8_MCGMRE64_RETURN_L1169",'// &
            '"original_return_source_line":1169,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        g64(1,ii) = rho64(ii)
        v64(:,ii,1) = residual64(:,ii) / rho64(ii)
      end do

      if (rhs_pending) then
        rhs64 = +0.0_real64
        call SPOMOC_SET_ROLE(2, iter)
        child_delta64 = 0_int64
        call MCGFL164(kpsys, iptrk, iftrak, iprint, ngeff, ngind, nun, &
            nreg, nbmix, nlong, nbtr, nmax, nmu, nangl, nbatch, lc, &
            lc0, paca, matalb_trk, &
            keyflx_trk3, keycur_trk1, nzon_trk1, volume_trk32, &
            caz1_track64, caz2_track64, cpo32, zmu32, wzmu32, &
            sc_by_group32, sigal32, leak1d64, qfr64, rhs64, source64, &
            flout64, krylov_active, epsinto64, child_delta64, child_ok)
        cutoff_delta64 = cutoff_delta64 + child_delta64
        if (.not. child_ok) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGMRE64",'// &
            '"predicate_id":"A8_MCGMRE64_RETURN_L1186",'// &
            '"original_return_source_line":1186,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        if (.not. all(ieee_is_finite(flout64))) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGMRE64",'// &
            '"predicate_id":"A8_MCGMRE64_RETURN_L1187",'// &
            '"original_return_source_line":1187,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        do ii = 1, ngeff
          if (krylov_active(ii)) rhs64(:,ii) = flout64(:,ii)
        end do
        rhs_pending = .false.
      end if

      k = 0
      do while (any(krylov_active) .and. k < restart_dimension .and. &
          narnoldi < MAXI)
        k = k + 1
        narnoldi = narnoldi + 1
        if (iter >= history_capacity) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGMRE64",'// &
            '"predicate_id":"A8_MCGMRE64_RETURN_L1199",'// &
            '"original_return_source_line":1199,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        iter = iter + 1
        gar64 = v64(:,:,k)
        call SPOMOC_SET_ROLE(3, iter)
        child_delta64 = 0_int64
        call MCGFL164(kpsys, iptrk, iftrak, iprint, ngeff, ngind, nun, &
            nreg, nbmix, nlong, nbtr, nmax, nmu, nangl, nbatch, lc, &
            lc0, paca, matalb_trk, &
            keyflx_trk3, keycur_trk1, nzon_trk1, volume_trk32, &
            caz1_track64, caz2_track64, cpo32, zmu32, wzmu32, &
            sc_by_group32, sigal32, leak1d64, qfr64, gar64, source64, &
            flout64, krylov_active, epsinto64, child_delta64, child_ok)
        cutoff_delta64 = cutoff_delta64 + child_delta64
        if (.not. child_ok) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGMRE64",'// &
            '"predicate_id":"A8_MCGMRE64_RETURN_L1212",'// &
            '"original_return_source_line":1212,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        if (.not. all(ieee_is_finite(flout64))) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGMRE64",'// &
            '"predicate_id":"A8_MCGMRE64_RETURN_L1213",'// &
            '"original_return_source_line":1213,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        v64(:,:,k+1) = v64(:,:,k) - flout64 + rhs64

        do ii = 1, ngeff
          reps64(iter,ii) = +0.0_real64
          if (.not. krylov_active(ii)) cycle
          kmax(ii) = k

          ! First modified Gram-Schmidt pass.
          do j = 1, k
            h64(j,k,ii) = dot_product(v64(:,ii,j), v64(:,ii,k+1))
            v64(:,ii,k+1) = v64(:,ii,k+1) - &
                h64(j,k,ii) * v64(:,ii,j)
          end do
          h64(k+1,k,ii) = sqrt(dot_product(v64(:,ii,k+1), &
              v64(:,ii,k+1)))
          if (.not. ieee_is_finite(h64(k+1,k,ii))) then
            write(6,'(A,I0,A)') &
              '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
              '"scope":"MCGMRE64",'// &
              '"predicate_id":"A8_MCGMRE64_RETURN_L1229",'// &
              '"original_return_source_line":1229,'// &
              '"actual_boolean_status_integer":',merge(1,0,ok),'}'
            flush(6)
            return
          end if

          ! Second modified Gram-Schmidt pass (reorthogonalization).
          do j = 1, k
            hr64 = dot_product(v64(:,ii,j), v64(:,ii,k+1))
            h64(j,k,ii) = h64(j,k,ii) + hr64
            v64(:,ii,k+1) = v64(:,ii,k+1) - hr64 * v64(:,ii,j)
          end do
          h64(k+1,k,ii) = sqrt(dot_product(v64(:,ii,k+1), &
              v64(:,ii,k+1)))
          if (.not. ieee_is_finite(h64(k+1,k,ii))) then
            write(6,'(A,I0,A)') &
              '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
              '"scope":"MCGMRE64",'// &
              '"predicate_id":"A8_MCGMRE64_RETURN_L1239",'// &
              '"original_return_source_line":1239,'// &
              '"actual_boolean_status_integer":',merge(1,0,ok),'}'
            flush(6)
            return
          end if
          if (h64(k+1,k,ii) > 0.0_real64) then
            v64(:,ii,k+1) = v64(:,ii,k+1) / h64(k+1,k,ii)
          end if

          ! Apply prior Givens rotations to the new Hessenberg column.
          do i = 1, k-1
            w1 = c64(i,ii) * h64(i,k,ii) - &
                sn64(i,ii) * h64(i+1,k,ii)
            w2 = sn64(i,ii) * h64(i,k,ii) + &
                c64(i,ii) * h64(i+1,k,ii)
            h64(i,k,ii) = w1
            h64(i+1,k,ii) = w2
          end do

          ! Form and apply the new Givens rotation.
          znu64 = sqrt(h64(k,k,ii)**2 + h64(k+1,k,ii)**2)
          if (.not. ieee_is_finite(znu64)) then
            write(6,'(A,I0,A)') &
              '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
              '"scope":"MCGMRE64",'// &
              '"predicate_id":"A8_MCGMRE64_RETURN_L1256",'// &
              '"original_return_source_line":1256,'// &
              '"actual_boolean_status_integer":',merge(1,0,ok),'}'
            flush(6)
            return
          end if
          if (znu64 > 0.0_real64) then
            c64(k,ii) = h64(k,k,ii) / znu64
            sn64(k,ii) = -h64(k+1,k,ii) / znu64
            h64(k,k,ii) = c64(k,ii) * h64(k,k,ii) - &
                sn64(k,ii) * h64(k+1,k,ii)
            h64(k+1,k,ii) = +0.0_real64
            w1 = c64(k,ii) * g64(k,ii) - sn64(k,ii) * g64(k+1,ii)
            w2 = sn64(k,ii) * g64(k,ii) + c64(k,ii) * g64(k+1,ii)
            g64(k,ii) = w1
            g64(k+1,ii) = w2
          end if

          rho64(ii) = abs(g64(k+1,ii))
          reps64(iter,ii) = rho64(ii) / denom64(ii)
          if (.not. ieee_is_finite(reps64(iter,ii))) then
            write(6,'(A,I0,A)') &
              '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
              '"scope":"MCGMRE64",'// &
              '"predicate_id":"A8_MCGMRE64_RETURN_L1271",'// &
              '"original_return_source_line":1271,'// &
              '"actual_boolean_status_integer":',merge(1,0,ok),'}'
            flush(6)
            return
          end if
          eps64(ii) = reps64(iter,ii)
          itst(ii) = iter
          krylov_active(ii) = krylov_active(ii) .and. &
              rho64(ii) >= epsi64 * denom64(ii)
        end do
      end do
      do ii = 1, ngeff
        k = kmax(ii)
        if (k == 0) cycle
        if (.not. all(ieee_is_finite(g64(1:k,ii)))) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGMRE64",'// &
            '"predicate_id":"A8_MCGMRE64_RETURN_L1281",'// &
            '"original_return_source_line":1281,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        if (.not. all(ieee_is_finite(h64(1:k,1:k,ii)))) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGMRE64",'// &
            '"predicate_id":"A8_MCGMRE64_RETURN_L1282",'// &
            '"original_return_source_line":1282,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        if (.not. all(ieee_is_finite(v64(:,ii,1:k)))) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGMRE64",'// &
            '"predicate_id":"A8_MCGMRE64_RETURN_L1283",'// &
            '"original_return_source_line":1283,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        if (abs(h64(k,k,ii)) <= 0.0_real64) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGMRE64",'// &
            '"predicate_id":"A8_MCGMRE64_RETURN_L1284",'// &
            '"original_return_source_line":1284,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
        g64(k,ii) = g64(k,ii) / h64(k,k,ii)
        do l = k-1, 1, -1
          if (abs(h64(l,l,ii)) <= 0.0_real64) then
            write(6,'(A,I0,A)') &
              '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
              '"scope":"MCGMRE64",'// &
              '"predicate_id":"A8_MCGMRE64_RETURN_L1287",'// &
              '"original_return_source_line":1287,'// &
              '"actual_boolean_status_integer":',merge(1,0,ok),'}'
            flush(6)
            return
          end if
          w1 = g64(l,ii) - &
              dot_product(h64(l,l+1:k,ii), g64(l+1:k,ii))
          g64(l,ii) = w1 / h64(l,l,ii)
        end do
        do j = 1, k
          phiin64(:,ii) = phiin64(:,ii) + &
              g64(j,ii) * v64(:,ii,j)
        end do
        if (.not. all(ieee_is_finite(phiin64(:,ii)))) then
          write(6,'(A,I0,A)') &
            '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
            '"scope":"MCGMRE64",'// &
            '"predicate_id":"A8_MCGMRE64_RETURN_L1296",'// &
            '"original_return_source_line":1296,'// &
            '"actual_boolean_status_integer":',merge(1,0,ok),'}'
          flush(6)
          return
        end if
      end do
      ! A Givens residual may stop work for one group inside this restart,
      ! but only a freshly evaluated physical residual may retire it.
      lnconv = count(nconv)
    end do

    lnconv = count(nconv)
    if (lnconv /= 0) then
      write(6,'(A,I0,A,I0,A,1P,E13.5)') &
          ' MCGMRE64: STRICT INNER TERMINAL FAILED; GROUPS=', lnconv, &
          ' ARNOLDI=', narnoldi, &
          ' MAX-EPS=', maxval(eps64,mask=nconv)
      flush(6)
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGMRE64",'// &
        '"predicate_id":"A8_MCGMRE64_RETURN_L1310",'// &
        '"original_return_source_line":1310,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(phiin64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGMRE64",'// &
        '"predicate_id":"A8_MCGMRE64_RETURN_L1312",'// &
        '"original_return_source_line":1312,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(source64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGMRE64",'// &
        '"predicate_id":"A8_MCGMRE64_RETURN_L1313",'// &
        '"original_return_source_line":1313,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    if (.not. all(ieee_is_finite(response64))) then
      write(6,'(A,I0,A)') &
        '{"schema":"ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1",'// &
        '"scope":"MCGMRE64",'// &
        '"predicate_id":"A8_MCGMRE64_RETURN_L1314",'// &
        '"original_return_source_line":1314,'// &
        '"actual_boolean_status_integer":',merge(1,0,ok),'}'
      flush(6)
      return
    end if
    ok = .true.
  end subroutine MCGMRE64

end module SPOR64_A8
