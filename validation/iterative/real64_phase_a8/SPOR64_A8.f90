module SPOR64_A8
  use, intrinsic :: iso_c_binding, only : c_associated, c_f_pointer, &
      c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use SPOR64_A8_ACA, only : MCGFCA64
  implicit none
  private

  integer, parameter :: NGRP = 370
  integer, parameter :: NREG = 8
  integer, parameter :: NSOUT = 6
  integer, parameter :: NLONG = 14
  integer, parameter :: KPN = 14
  integer, parameter :: NBMIX = 8
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
  integer, parameter :: PACA = 4
  integer, parameter :: MAXI = 20
  integer, parameter :: NSTART = 10
  integer, parameter :: MAXIT = 19
  integer, parameter :: MAXACC = 200
  logical, parameter :: LFORW = .true.

  integer, parameter :: kind_guard = 1 / merge(1, 0, &
      kind(1.0) == real32 .and. kind(0.0d0) == real64)
  integer, parameter :: epsi_bits_guard = 1 / merge(1, 0, &
      transfer(1.0e-5_real32, 0_int32) == int(z'3727c5ac', int32))

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
    ok = .false.
    if (size(keyflx_base1) /= NREG) return
    if (size(keyflx_trk3,1) /= NREG) return
    if (size(keyflx_trk3,2) /= NLIN) return
    if (size(keyflx_trk3,3) /= NFUNL) return
    if (size(pjjind_trk2,1) /= 1) return
    if (size(pjjind_trk2,2) /= 2) return
    ok = all(keyflx_base1 == keyflx_trk3(:,1,1)) .and. &
        all(pjjind_trk2 == 1)
  end subroutine SPOR64_A8_RANK_PROBE

  subroutine SPOR64_A8_OPERATOR_PROBE(sc32, sigal32, ok)
    real(real32), intent(in) :: sc32(0:NBMIX,1)
    real(real32), intent(in) :: sigal32(-NSOUT:NBMIX)
    logical, intent(out) :: ok
    ok = all(ieee_is_finite(sc32)) .and. all(ieee_is_finite(sigal32))
  end subroutine SPOR64_A8_OPERATOR_PROBE

  logical function RECORD_MATCHES(iplist, name, expected_length, &
      expected_type) result(matches)
    type(c_ptr), intent(in) :: iplist
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: length, itylcm
    matches = .false.
    if (.not. c_associated(iplist)) return
    call LCMLEN(iplist, name, length, itylcm)
    matches = length == expected_length .and. itylcm == expected_type
  end function RECORD_MATCHES

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
    if (.not. ok) return
    call LCMGPD(iplist, name, address)
    if (.not. c_associated(address)) then
      ok = .false.
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
    if (.not. ok) return
    call LCMGPD(iplist, name, address)
    if (.not. c_associated(address)) then
      ok = .false.
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
    if (.not. ok) return
    call LCMGPD(iplist, name, address)
    if (.not. c_associated(address)) then
      ok = .false.
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
    if (.not. ok) return
    call LCMGPD(iplist, name, address)
    if (.not. c_associated(address)) then
      ok = .false.
      return
    end if
    shape3(1) = n1
    shape3(2) = n2
    shape3(3) = n3
    call c_f_pointer(address, values, shape3)
  end subroutine MAP_INTEGER3

  subroutine DOORFV64(ipsys, npsys, iptrk, iftrak, impx, ngrp, nun, &
      keyflx_base1, title, full_source64, full_flux64, cutoff_delta64, &
      ok)
    type(c_ptr), intent(in) :: ipsys, iptrk
    integer, intent(in) :: ngrp, nun, iftrak, impx
    integer, intent(in) :: npsys(ngrp), keyflx_base1(NREG)
    character(len=72), intent(in) :: title
    real(real64), intent(in) :: full_source64(nun,ngrp)
    real(real64), intent(inout) :: full_flux64(nun,ngrp)
    integer(int64), intent(out) :: cutoff_delta64
    logical, intent(out) :: ok

    integer :: first_group, ig, ii, ileng, itylcm, ngeff
    integer(int64) :: child_delta64
    logical :: child_ok
    logical, allocatable :: seen(:)
    integer, allocatable :: ngind(:)
    real(real64), allocatable :: fgar64(:), phiin_tail64(:,:)
    real(real64), allocatable :: qfr_tail64(:,:)
    type(c_ptr), allocatable :: kpsys_tail(:)

    cutoff_delta64 = 0_int64
    ok = .false.
    if (ngrp /= NGRP .or. nun /= KPN) return
    if (.not. c_associated(ipsys) .or. .not. c_associated(iptrk)) return
    if (iftrak <= 0) return
    if (.not. all(ieee_is_finite(full_source64))) return
    if (.not. all(ieee_is_finite(full_flux64))) return

    allocate(seen(nun))
    seen = .false.
    do ii = 1, NREG
      if (keyflx_base1(ii) < 1 .or. keyflx_base1(ii) > nun) return
      if (seen(keyflx_base1(ii))) return
      seen(keyflx_base1(ii)) = .true.
    end do

    ngeff = count(npsys /= 0)
    if (ngeff <= 0) return
    first_group = ngrp - ngeff + 1
    if (first_group > 1) then
      if (any(npsys(:first_group-1) /= 0)) return
    end if
    do ig = first_group, ngrp
      if (npsys(ig) /= ig) return
    end do

    allocate(ngind(ngeff), kpsys_tail(ngeff))
    allocate(qfr_tail64(nun,ngeff), phiin_tail64(nun,ngeff))
    do ii = 1, ngeff
      ig = first_group + ii - 1
      ngind(ii) = ig
      kpsys_tail(ii) = LCMGIL(ipsys, npsys(ig))
      if (.not. c_associated(kpsys_tail(ii))) return
      call LCMLEN(kpsys_tail(ii), 'FUNKNO$USS', ileng, itylcm)
      if (ileng /= 0) return
      qfr_tail64(:,ii) = full_source64(:,ig)
      phiin_tail64(:,ii) = full_flux64(:,ig)
    end do

    if (impx > 3) then
      allocate(fgar64(NREG))
      do ii = 1, ngeff
        fgar64 = +0.0_real64
        do ig = 1, NREG
          fgar64(ig) = qfr_tail64(keyflx_base1(ig),ii)
        end do
        call PRINDM('QFR64 ', fgar64, NREG)
      end do
    end if

    child_delta64 = 0_int64
    call MCCGF64(kpsys_tail, iptrk, iftrak, impx, ngeff, ngind, nun, &
        keyflx_base1, qfr_tail64, phiin_tail64, title, child_delta64, &
        child_ok)
    cutoff_delta64 = cutoff_delta64 + child_delta64
    if (.not. child_ok) return
    if (.not. all(ieee_is_finite(phiin_tail64))) return

    do ii = 1, ngeff
      full_flux64(:,ngind(ii)) = phiin_tail64(:,ii)
    end do
    if (impx > 3) then
      do ii = 1, ngeff
        fgar64 = +0.0_real64
        do ig = 1, NREG
          fgar64(ig) = phiin_tail64(keyflx_base1(ig),ii)
        end do
        call PRINDM('FLUX64', fgar64, NREG)
      end do
    end if
    ok = .true.
  end subroutine DOORFV64

  subroutine MCCGF64(kpsys, iptrk, iftrak, impx, ngeff, ngind, nun, &
      keyflx_base1, qfr64, phiin64, title, cutoff_delta64, ok)
    integer, intent(in) :: iftrak, impx, ngeff, nun
    type(c_ptr), intent(in) :: kpsys(ngeff), iptrk
    integer, intent(in) :: ngind(ngeff), keyflx_base1(NREG)
    real(real64), intent(in) :: qfr64(nun,ngeff)
    real(real64), intent(inout) :: phiin64(nun,ngeff)
    character(len=72), intent(in) :: title
    integer(int64), intent(out) :: cutoff_delta64
    logical, intent(out) :: ok

    character(len=4) :: text4
    integer :: i, icom, ifmt, ios, ispec, itylcm, j, nalbg, nalbp
    integer :: nangl, nbatch, nbtr, ncomnt, ncor, nmax, nmu
    integer :: n2reg, n2sou, mxseg, mxsub, lc, lnconv
    integer(int64) :: child_delta64
    integer, allocatable :: itst(:), matalb_trk(:)
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
    if (ngeff <= 0 .or. ngeff > NGRP .or. nun /= KPN) return
    if (iftrak <= 0 .or. .not. c_associated(iptrk)) return
    do i = 1, ngeff
      if (.not. c_associated(kpsys(i))) return
    end do
    if (ngind(1) /= NGRP-ngeff+1 .or. ngind(ngeff) /= NGRP) return
    do i = 2, ngeff
      if (ngind(i) /= ngind(i-1)+1) return
    end do
    if (.not. all(ieee_is_finite(qfr64))) return
    if (.not. all(ieee_is_finite(phiin64))) return

    call MAP_INTEGER1(iptrk, 'STATE-VECTOR', 40, state_vector, map_ok)
    if (.not. map_ok) return
    call MAP_INTEGER1(iptrk, 'MCCG-STATE', 40, mccg_state, map_ok)
    if (.not. map_ok) return
    call MAP_REAL321(iptrk, 'REAL-PARAM', 4, real_param32, map_ok)
    if (.not. map_ok) return
    if (state_vector(1) /= NREG .or. state_vector(2) /= KPN) return
    if (state_vector(3) /= 1 .or. state_vector(4) /= NBMIX) return
    if (state_vector(5) /= NSOUT .or. state_vector(6) /= NANI) return
    if (state_vector(9) /= 0 .or. state_vector(14) /= 4) return
    if (state_vector(16) /= 2 .or. state_vector(22) /= 1) return
    if (state_vector(27) /= 0 .or. state_vector(39) /= 0) return
    if (state_vector(40) /= 0) return
    if (mccg_state(2) /= 4 .or. mccg_state(3) /= KRYL) return
    if (mccg_state(4) /= 0 .or. mccg_state(5) /= 17) return
    if (mccg_state(6) /= 32 .or. mccg_state(7) /= IAAC) return
    if (mccg_state(8) /= ISCR .or. mccg_state(9) /= 0) return
    if (mccg_state(10) /= PACA .or. mccg_state(12) /= 0) return
    if (mccg_state(13) /= MAXI .or. mccg_state(15) /= STIS) return
    if (mccg_state(16) /= NFUNL .or. mccg_state(18) /= 0) return
    if (mccg_state(19) /= NFUNL .or. mccg_state(20) /= NLIN) return
    if (1 + 10*mccg_state(15) + 100*(mccg_state(20)-1) /= ISCH) return
    lc = mccg_state(6)
    nmu = mccg_state(2)
    nmax = mccg_state(5)
    if (lc <= 0 .or. nmu <= 0 .or. nmax <= 0) return
    nbatch = state_vector(27)
    if (nbatch == 0) nbatch = 1
    if (nbatch < 1) return
    if (transfer(real_param32(1), 0_int32) /= int(z'3727c5ac',int32)) &
        return
    if (.not. all(ieee_is_finite(real_param32))) return
    if (transfer(real_param32(2), 0_int32) /= 0_int32) return
    if (transfer(real_param32(3), 0_int32) /= 0_int32) return
    if (transfer(real_param32(4), 0_int32) /= 0_int32) return
    epsi64 = real(real_param32(1), real64)
    if (.not. ieee_is_finite(epsi64) .or. epsi64 <= 0.0_real64) return

    rewind(iftrak, iostat=ios)
    if (ios /= 0) return
    read(iftrak, iostat=ios) text4, ncomnt, nbtr, ifmt
    if (ios /= 0 .or. ncomnt < 0 .or. nbtr <= 0) return
    if (impx > 9) write(6,'(A,A4,A,I0)') &
        ' MCCGF64: TRACK=', text4, ' FORMAT=', ifmt
    do icom = 1, ncomnt
      read(iftrak, iostat=ios)
      if (ios /= 0) return
    end do
    read(iftrak, iostat=ios) i, ispec, n2reg, n2sou, nalbg, ncor, &
        nangl, mxsub, mxseg
    if (ios /= 0) return
    if (i /= NDIM .or. n2reg /= NREG .or. n2sou /= NSOUT) return
    if (ncor /= 1 .or. nangl <= 0 .or. mxsub <= 0 .or. mxseg <= 0) &
        return
    if (nalbg < 0 .or. ispec < 0 .or. len_trim(text4) > 4) return

    call SPOMOC_MCCGF_BEGIN(NGRP, ngeff, ngind, nun, NDIM, .false., &
        NLONG, NREG, NSOUT, NANI, NLIN, NFUNL, KRYL, STIS, IAAC, ISCR, &
        0, PACA, IDIR)

    allocate(matalb_trk(-NSOUT:NREG))
    read(iftrak, iostat=ios)
    if (ios /= 0) return
    read(iftrak, iostat=ios) (matalb_trk(j), j=-NSOUT,NREG)
    if (ios /= 0) return
    read(iftrak, iostat=ios)
    if (ios /= 0) return
    read(iftrak, iostat=ios)
    if (ios /= 0) return

    call MAP_REAL321(iptrk, 'XMU$MCCG', nmu, cpo_view32, map_ok)
    if (.not. map_ok) return
    allocate(cpo32(nmu), caz1_track64(nangl), caz2_track64(nangl))
    cpo32 = cpo_view32
    read(iftrak, iostat=ios) &
        (caz1_track64(j), caz2_track64(j), j=1,nangl)
    if (ios /= 0) return
    if (.not. all(ieee_is_finite(caz1_track64))) return
    if (.not. all(ieee_is_finite(caz2_track64))) return
    if (.not. all(ieee_is_finite(cpo32))) return

    call MAP_REAL321(iptrk, 'WZMU$MCCG', nmu, wzmu32, map_ok)
    if (.not. map_ok) return
    call MAP_REAL321(iptrk, 'ZMU$MCCG', nmu, zmu32, map_ok)
    if (.not. map_ok) return
    call MAP_REAL321(iptrk, 'V$MCCG', NLONG, volume_trk32, map_ok)
    if (.not. map_ok) return
    call MAP_INTEGER1(iptrk, 'NZON$MCCG', NLONG, nzon_trk1, map_ok)
    if (.not. map_ok) return
    call MAP_INTEGER3(iptrk, 'KEYFLX$ANIS', NREG, NLIN, NFUNL, &
        keyflx_trk3, map_ok)
    if (.not. map_ok) return
    call MAP_INTEGER1(iptrk, 'KEYCUR$MCCG', NLONG-NREG, keycur_trk1, &
        map_ok)
    if (.not. map_ok) return
    if (.not. all(keyflx_base1 == keyflx_trk3(:,1,1))) return
    if (.not. all(ieee_is_finite(wzmu32))) return
    if (.not. all(ieee_is_finite(zmu32))) return
    if (.not. all(ieee_is_finite(volume_trk32))) return
    if (any(volume_trk32 <= 0.0_real32)) return
    if (any(nzon_trk1(:NREG) < 0) .or. &
        any(nzon_trk1(:NREG) > NBMIX)) return
    if (any(nzon_trk1(NREG+1:) < -NSOUT) .or. &
        any(nzon_trk1(NREG+1:) > -1)) return
    if (any(matalb_trk(1:NREG) /= nzon_trk1(1:NREG))) return

    allocate(seen(KPN))
    seen = .false.
    do i = 1, NREG
      j = keyflx_trk3(i,1,1)
      if (j < 1 .or. j > KPN) return
      if (seen(j)) return
      seen(j) = .true.
    end do
    do i = 1, NLONG-NREG
      j = keycur_trk1(i)
      if (j < 1 .or. j > KPN) return
      if (seen(j)) return
      seen(j) = .true.
    end do
    if (.not. all(seen)) return

    call MAP_INTEGER1(iptrk, 'ICODE', NSOUT, icode_trk1, map_ok)
    if (.not. map_ok) return
    call MAP_REAL321(iptrk, 'ALBEDO', NSOUT, albedo_trk32, map_ok)
    if (.not. map_ok) return
    if (.not. all(ieee_is_finite(albedo_trk32))) return
    call LCMLEN(kpsys(1), 'ALBEDO', nalbp, itylcm)
    if (nalbp < 0) return
    if (any(icode_trk1 > nalbp)) return
    allocate(sc_by_group32(0:NBMIX,1,ngeff))
    do i = 1, ngeff
      if (.not. RECORD_MATCHES(kpsys(i), 'DRAGON-TXSC', NBMIX+1, 2)) &
          return
      if (.not. RECORD_MATCHES(kpsys(i), 'DRAGON-S0XSC', NBMIX+1, 2)) &
          return
      if (nalbp == 0) then
        call LCMLEN(kpsys(i), 'ALBEDO', j, itylcm)
        if (j /= 0) return
      else
        call MAP_REAL321(kpsys(i), 'ALBEDO', nalbp, group_albedo32, &
            map_ok)
        if (.not. map_ok) return
        if (.not. all(ieee_is_finite(group_albedo32))) return
      end if
      call MAP_REAL321(kpsys(i), 'DRAGON-TXSC', NBMIX+1, &
          txsc_record32, map_ok)
      if (.not. map_ok) return
      if (.not. all(ieee_is_finite(txsc_record32))) return
      call MAP_REAL321(kpsys(i), 'DRAGON-S0XSC', NBMIX+1, &
          sc_record32, map_ok)
      if (.not. map_ok) return
      sc_by_group32(:,1,i) = sc_record32
    end do
    if (.not. all(ieee_is_finite(sc_by_group32))) return

    allocate(sigal32(-NSOUT:NBMIX,ngeff))
    call MCGSIG(iptrk, NBMIX, ngeff, nalbp, kpsys, sigal32, lvoid)
    if (.not. all(ieee_is_finite(sigal32))) return

    allocate(reps64(MAXI,ngeff), eps64(ngeff), itst(ngeff))
    allocate(nconv(ngeff))
    reps64 = +0.0_real64
    eps64 = +0.0_real64
    itst = 0
    nconv = .true.
    lnconv = ngeff

    child_delta64 = 0_int64
    call MCGFLX64(kpsys, iptrk, iftrak, impx, ngeff, ngind, nun, nbtr, &
        nmax, nmu, nangl, nbatch, lc, matalb_trk, keyflx_trk3, &
        keycur_trk1, nzon_trk1, volume_trk32, caz1_track64, &
        caz2_track64, cpo32, zmu32, wzmu32, sc_by_group32, sigal32, &
        qfr64, phiin64, epsi64, reps64, eps64, itst, nconv, lnconv, &
        child_delta64, child_ok)
    cutoff_delta64 = cutoff_delta64 + child_delta64
    if (.not. child_ok) return

    do i = 1, ngeff
      temp64 = eps64(i)
      if (.not. ieee_is_finite(temp64)) return
      if (itst(i) == MAXI .and. temp64 > epsi64 .and. impx > 0) then
        write(6,'(A,I0)') ' MCCGF64: INNER CAP REACHED FOR GROUP ', &
            ngind(i)
      end if
    end do
    if (impx > 1) call PRINDM('EPS64 ', eps64, ngeff)
    if (.not. all(ieee_is_finite(phiin64))) return
    if (impx > 3) write(6,'(A,1X,A)') ' MCCGF64:', trim(title)
    ok = .true.
  end subroutine MCCGF64

  subroutine MCGFCS64(n, ndim0, nzon, qn64, fi64, m, nani0, nlin0, &
      nfunl0, sc32, s64, kpn0, nreg0, iprint, keyflx3, keycur, ibc, &
      sigal32, stis0, ok)
    integer, intent(in) :: n, ndim0, m, nani0, nlin0, nfunl0
    integer, intent(in) :: kpn0, nreg0, iprint, stis0
    integer, intent(in) :: nzon(n), keycur(n-nreg0), ibc(n-nreg0)
    integer, intent(in) :: keyflx3(nreg0,nlin0,nfunl0)
    real(real64), intent(in) :: qn64(kpn0), fi64(kpn0)
    real(real64), intent(inout) :: s64(kpn0)
    real(real32), intent(in) :: sc32(0:m,nani0)
    real(real32), intent(in) :: sigal32(-NSOUT:m)
    logical, intent(out) :: ok

    integer :: ibm, ind, ind2, ir, isur, isur2

    ok = .false.
    if (n /= NLONG .or. ndim0 /= NDIM .or. m /= NBMIX) return
    if (nani0 /= NANI .or. nlin0 /= NLIN .or. nfunl0 /= NFUNL) return
    if (kpn0 /= KPN .or. nreg0 /= NREG .or. stis0 /= STIS) return
    if (.not. all(ieee_is_finite(qn64))) return
    if (.not. all(ieee_is_finite(fi64))) return
    if (.not. all(ieee_is_finite(s64))) return
    if (.not. all(ieee_is_finite(sc32))) return
    if (.not. all(ieee_is_finite(sigal32))) return

    do ir = 1, n
      ibm = nzon(ir)
      if (ibm < 0) then
        if (ibm < -NSOUT) return
        isur = ir - nreg0
        if (isur < 1 .or. isur > n-nreg0) return
        isur2 = ibc(isur)
        if (isur2 < 1 .or. isur2 > n-nreg0) return
        ind = keycur(isur)
        ind2 = keycur(isur2)
        if (ind < 1 .or. ind > kpn0) return
        if (ind2 < 1 .or. ind2 > kpn0) return
        s64(ind) = real(sigal32(ibm), real64) * fi64(ind2)
      else
        if (ibm > m) return
        if (ir > nreg0) return
        ind = keyflx3(ir,1,1)
        if (ind < 1 .or. ind > kpn0) return
        s64(ind) = qn64(ind) + &
            real(sc32(ibm,1), real64) * fi64(ind)
      end if
    end do
    if (.not. all(ieee_is_finite(s64))) return
    if (iprint > 6) call PRINDM('S64   ', s64, kpn0)
    ok = .true.
  end subroutine MCGFCS64

  subroutine MCGFL164(kpsys, iptrk, iftrak, iprint, ngeff, ngind, nun, &
      nbtr, nmax, nmu, nangl, nbatch, lc, matalb_trk, keyflx_trk3, &
      keycur_trk1, nzon_trk1, volume_trk32, caz1_track64, &
      caz2_track64, cpo32, zmu32, wzmu32, sc_by_group32, sigal32, &
      qfr64, phiin64, source64, response64, nconv, epsacc64, &
      cutoff_delta64, ok)
    integer, intent(in) :: iftrak, iprint, ngeff, nun, nbtr, nmax
    integer, intent(in) :: nmu, nangl, nbatch, lc
    type(c_ptr), intent(in) :: kpsys(ngeff), iptrk
    integer, intent(in) :: ngind(ngeff), matalb_trk(-NSOUT:NREG)
    integer, intent(in) :: keyflx_trk3(NREG,NLIN,NFUNL)
    integer, intent(in) :: keycur_trk1(NLONG-NREG), nzon_trk1(NLONG)
    real(real32), intent(in) :: volume_trk32(NLONG), cpo32(nmu)
    real(real32), intent(in) :: zmu32(nmu), wzmu32(nmu)
    real(real32), intent(in) :: sc_by_group32(0:NBMIX,1,ngeff)
    real(real32), intent(in) :: sigal32(-NSOUT:NBMIX,ngeff)
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
    integer :: n2reg, n2sou, nalbg, nangl_check, mxsub, mxseg
    integer :: isgnr(4,NFUNL), keyani(NFUNL)
    integer(int64) :: child_delta64
    integer, contiguous, pointer :: bc_index_trk1(:), im(:), iperm(:)
    integer, contiguous, pointer :: ju(:), mcu(:), pjjind_trk2(:,:)
    logical :: child_ok, map_ok
    real(real32), contiguous, pointer :: record32(:)
    real(real32), allocatable :: cf32(:,:), cq32(:,:), diagf32(:,:)
    real(real32), allocatable :: diagq32(:,:), iludf32(:,:)
    real(real64), allocatable :: caz0_inactive64(:), xsi_inactive64(:)

    cutoff_delta64 = 0_int64
    ok = .false.
    response64 = 0.0_real64
    if (ngeff <= 0 .or. ngeff > NGRP .or. nun /= KPN) return
    if (nbtr <= 0 .or. nmax <= 0 .or. nmu <= 0 .or. nangl <= 0) return
    if (nbatch <= 0 .or. lc <= 0 .or. iftrak <= 0) return
    if (.not. c_associated(iptrk)) return
    do i = 1, ngeff
      if (.not. c_associated(kpsys(i))) return
    end do
    if (ngind(1) /= NGRP-ngeff+1 .or. ngind(ngeff) /= NGRP) return
    do i = 2, ngeff
      if (ngind(i) /= ngind(i-1)+1) return
    end do
    if (.not. any(nconv)) then
      ok = .true.
      return
    end if
    if (.not. ieee_is_finite(epsacc64) .or. epsacc64 < 0.0_real64) &
        return
    if (.not. all(ieee_is_finite(qfr64))) return
    if (.not. all(ieee_is_finite(phiin64))) return
    if (.not. all(ieee_is_finite(source64))) return
    if (.not. all(ieee_is_finite(volume_trk32))) return
    if (.not. all(ieee_is_finite(caz1_track64))) return
    if (.not. all(ieee_is_finite(caz2_track64))) return
    if (.not. all(ieee_is_finite(cpo32))) return
    if (.not. all(ieee_is_finite(zmu32))) return
    if (.not. all(ieee_is_finite(wzmu32))) return
    if (.not. all(ieee_is_finite(sc_by_group32))) return
    if (.not. all(ieee_is_finite(sigal32))) return
    if (any(matalb_trk(1:NREG) /= nzon_trk1(1:NREG))) return

    call MAP_INTEGER1(iptrk, 'BC-REFL+TRAN', NLONG-NREG, &
        bc_index_trk1, map_ok)
    if (.not. map_ok) return
    if (any(bc_index_trk1 < 1) .or. &
        any(bc_index_trk1 > NLONG-NREG)) return
    call MAP_INTEGER2(iptrk, 'PJJIND$MCCG', NFUNL, 2, &
        pjjind_trk2, map_ok)
    if (.not. map_ok) return
    if (any(pjjind_trk2 /= 1)) return
    do i = 1, ngeff
      if (nconv(i)) then
        if (.not. RECORD_MATCHES(kpsys(i), 'PJJ$MCCG', &
            NREG*NFUNL, 2)) return
      end if
    end do

    do i = 1, ngeff
      if (nconv(i)) then
        call MCGFCS64(NLONG, NDIM, nzon_trk1, qfr64(:,i), &
            phiin64(:,i), NBMIX, NANI, NLIN, NFUNL, &
            sc_by_group32(:,:,i), source64(:,i), KPN, NREG, iprint, &
            keyflx_trk3, keycur_trk1, bc_index_trk1, sigal32(:,i), &
            STIS, child_ok)
        if (.not. child_ok) return
      end if
    end do

    call MOCIK3(NANI-1, NFUNL, 4, isgnr, keyani)
    if (keyani(1) /= 0 .or. .not. all(isgnr(:,1) == 1)) return
    allocate(caz0_inactive64(nangl), xsi_inactive64(NSOUT))
    caz0_inactive64 = +0.0_real64
    xsi_inactive64 = +0.0_real64

    rewind(iftrak, iostat=ios)
    if (ios /= 0) return
    read(iftrak, iostat=ios) text4, ncomnt, i, ifmt
    if (ios /= 0 .or. ncomnt < 0 .or. i /= nbtr) return
    if (iprint > 9) write(6,'(A,A4,A,I0)') &
        ' MCGFL164: TRACK=', text4, ' FORMAT=', ifmt
    do icom = 1, ncomnt
      read(iftrak, iostat=ios)
      if (ios /= 0) return
    end do
    read(iftrak, iostat=ios) i, ispec, n2reg, n2sou, nalbg, ncor, &
        nangl_check, mxsub, mxseg
    if (ios /= 0) return
    if (i /= NDIM .or. n2reg /= NREG .or. n2sou /= NSOUT) return
    if (ncor /= 1 .or. nangl_check /= nangl) return
    if (ispec < 0 .or. nalbg < 0 .or. mxsub <= 0 .or. mxseg <= 0) &
        return
    do icom = 1, 6
      read(iftrak, iostat=ios)
      if (ios /= 0) return
    end do

    call MCGFCF(MCGFFIR64_RANK_ADAPTER, MCGFFAR, MCGFFAL, MCGSCA, &
        iftrak, nbtr, nmax, NDIM, KPN, NLONG, NREG, NBMIX, ngeff, &
        nangl, nmu, NANI, NFUNL, 4, NANI, NLIN, NFUNL, keyflx_trk3, &
        keycur_trk1, nzon_trk1, nconv, caz0_inactive64, caz1_track64, &
        caz2_track64, cpo32, zmu32, wzmu32, source64, sigal32, isgnr, &
        IDIR, NSOUT, nbatch, xsi_inactive64, response64)
    if (.not. all(ieee_is_finite(response64))) return

    call MCGFST(ngeff, kpsys, nconv, KPN, NLONG, NREG, NANI, NFUNL, &
        NFUNL, keyflx_trk3(:,1,:), keycur_trk1, pjjind_trk2, &
        nzon_trk1, volume_trk32, source64, response64, IDIR)
    if (.not. all(ieee_is_finite(response64))) return

    call SPOMOC_CAPTURE64(ngeff, ngind, nun, qfr64, phiin64, source64, &
        response64, nconv)

    call MAP_INTEGER1(iptrk, 'IM$MCCG', NLONG+1, im, map_ok)
    if (.not. map_ok) return
    call MAP_INTEGER1(iptrk, 'MCU$MCCG', lc, mcu, map_ok)
    if (.not. map_ok) return
    call MAP_INTEGER1(iptrk, 'PI$MCCG', NLONG, iperm, map_ok)
    if (.not. map_ok) return
    call MAP_INTEGER1(iptrk, 'JU$MCCG', NLONG, ju, map_ok)
    if (.not. map_ok) return

    allocate(diagq32(NLONG,ngeff), cq32(lc,ngeff))
    allocate(iludf32(NLONG,ngeff), cf32(lc,ngeff))
    allocate(diagf32(NLONG,ngeff))
    do i = 1, ngeff
      call MAP_REAL321(kpsys(i), 'DIAGQ$MCCG', NLONG, record32, map_ok)
      if (.not. map_ok) return
      diagq32(:,i) = record32
      call MAP_REAL321(kpsys(i), 'CQ$MCCG', lc, record32, map_ok)
      if (.not. map_ok) return
      cq32(:,i) = record32
      call MAP_REAL321(kpsys(i), 'ILUDF$MCCG', NLONG, record32, map_ok)
      if (.not. map_ok) return
      iludf32(:,i) = record32
      call MAP_REAL321(kpsys(i), 'CF$MCCG', lc, record32, map_ok)
      if (.not. map_ok) return
      cf32(:,i) = record32
      call MAP_REAL321(kpsys(i), 'DIAGF$MCCG', NLONG, record32, map_ok)
      if (.not. map_ok) return
      diagf32(:,i) = record32
    end do
    if (.not. all(ieee_is_finite(diagq32))) return
    if (.not. all(ieee_is_finite(cq32))) return
    if (.not. all(ieee_is_finite(iludf32))) return
    if (.not. all(ieee_is_finite(cf32))) return
    if (.not. all(ieee_is_finite(diagf32))) return

    child_delta64 = 0_int64
    call MCGFCA64(NLONG, ngeff, KPN, NREG, NBMIX, lc, LFORW, PACA, &
        keyflx_trk3(:,1,:), keycur_trk1, nzon_trk1, nconv, MAXACC, &
        epsacc64, response64, phiin64, sc_by_group32, im, mcu, iperm, &
        ju, diagq32, cq32, iludf32, cf32, diagf32, child_delta64, &
        child_ok)
    cutoff_delta64 = cutoff_delta64 + child_delta64
    if (.not. child_ok) return
    if (.not. all(ieee_is_finite(response64))) return
    ok = .true.
  end subroutine MCGFL164

  subroutine MCGFLX64(kpsys, iptrk, iftrak, iprint, ngeff, ngind, nun, &
      nbtr, nmax, nmu, nangl, nbatch, lc, matalb_trk, keyflx_trk3, &
      keycur_trk1, nzon_trk1, volume_trk32, caz1_track64, &
      caz2_track64, cpo32, zmu32, wzmu32, sc_by_group32, sigal32, &
      qfr64, phiin64, epsi64, reps64, eps64, itst, nconv, lnconv, &
      cutoff_delta64, ok)
    integer, intent(in) :: iftrak, iprint, ngeff, nun, nbtr, nmax
    integer, intent(in) :: nmu, nangl, nbatch, lc
    type(c_ptr), intent(in) :: kpsys(ngeff), iptrk
    integer, intent(in) :: ngind(ngeff), matalb_trk(-NSOUT:NREG)
    integer, intent(in) :: keyflx_trk3(NREG,NLIN,NFUNL)
    integer, intent(in) :: keycur_trk1(NLONG-NREG), nzon_trk1(NLONG)
    integer, intent(out) :: itst(ngeff)
    integer, intent(inout) :: lnconv
    real(real32), intent(in) :: volume_trk32(NLONG), cpo32(nmu)
    real(real32), intent(in) :: zmu32(nmu), wzmu32(nmu)
    real(real32), intent(in) :: sc_by_group32(0:NBMIX,1,ngeff)
    real(real32), intent(in) :: sigal32(-NSOUT:NBMIX,ngeff)
    real(real64), intent(in) :: caz1_track64(nangl)
    real(real64), intent(in) :: caz2_track64(nangl)
    real(real64), intent(in) :: qfr64(nun,ngeff), epsi64
    real(real64), intent(inout) :: phiin64(nun,ngeff)
    real(real64), intent(out) :: reps64(MAXI,ngeff), eps64(ngeff)
    logical, intent(inout) :: nconv(ngeff)
    integer(int64), intent(out) :: cutoff_delta64
    logical, intent(out) :: ok

    integer :: ii
    integer(int64) :: child_delta64
    logical :: child_ok
    real(real64), allocatable :: response64(:,:), source64(:,:)

    cutoff_delta64 = 0_int64
    ok = .false.
    if (ngeff <= 0 .or. ngeff > NGRP .or. nun /= KPN) return
    if (KRYL /= 10 .or. MAXI /= 20) return
    if (.not. ieee_is_finite(epsi64) .or. epsi64 <= 0.0_real64) return
    if (.not. all(ieee_is_finite(qfr64))) return
    if (.not. all(ieee_is_finite(phiin64))) return
    if (.not. any(nconv)) return

    allocate(source64(KPN,ngeff), response64(KPN,ngeff))
    SOURCE64 = 0.0_REAL64
    reps64 = +0.0_real64
    eps64 = +0.0_real64
    itst = 0
    if (iprint > 5) then
      do ii = 1, ngeff
        call PRINDM('FI-0  ', phiin64(:,ii), KPN)
      end do
    end if

    child_delta64 = 0_int64
    call MCGMRE64(kpsys, iptrk, iftrak, iprint, ngeff, ngind, nun, &
        nbtr, nmax, nmu, nangl, nbatch, lc, matalb_trk, keyflx_trk3, &
        keycur_trk1, nzon_trk1, volume_trk32, caz1_track64, &
        caz2_track64, cpo32, zmu32, wzmu32, sc_by_group32, sigal32, &
        qfr64, phiin64, source64, response64, epsi64, reps64, eps64, &
        itst, nconv, lnconv, child_delta64, child_ok)
    cutoff_delta64 = cutoff_delta64 + child_delta64
    if (.not. child_ok) return
    if (.not. all(ieee_is_finite(phiin64))) return
    ok = .true.
  end subroutine MCGFLX64
  subroutine MCGMRE64(kpsys, iptrk, iftrak, iprint, ngeff, ngind, nun, &
      nbtr, nmax, nmu, nangl, nbatch, lc, matalb_trk, keyflx_trk3, &
      keycur_trk1, nzon_trk1, volume_trk32, caz1_track64, &
      caz2_track64, cpo32, zmu32, wzmu32, sc_by_group32, sigal32, &
      qfr64, phiin64, source64, response64, epsi64, reps64, eps64, &
      itst, nconv, lnconv, cutoff_delta64, ok)
    integer, intent(in) :: iftrak, iprint, ngeff, nun, nbtr, nmax
    integer, intent(in) :: nmu, nangl, nbatch, lc
    type(c_ptr), intent(in) :: kpsys(ngeff), iptrk
    integer, intent(in) :: ngind(ngeff), matalb_trk(-NSOUT:NREG)
    integer, intent(in) :: keyflx_trk3(NREG,NLIN,NFUNL)
    integer, intent(in) :: keycur_trk1(NLONG-NREG), nzon_trk1(NLONG)
    integer, intent(inout) :: itst(ngeff), lnconv
    real(real32), intent(in) :: volume_trk32(NLONG), cpo32(nmu)
    real(real32), intent(in) :: zmu32(nmu), wzmu32(nmu)
    real(real32), intent(in) :: sc_by_group32(0:NBMIX,1,ngeff)
    real(real32), intent(in) :: sigal32(-NSOUT:NBMIX,ngeff)
    real(real64), intent(in) :: caz1_track64(nangl)
    real(real64), intent(in) :: caz2_track64(nangl)
    real(real64), intent(in) :: qfr64(nun,ngeff), epsi64
    real(real64), intent(inout) :: phiin64(nun,ngeff)
    real(real64), intent(inout) :: source64(nun,ngeff)
    real(real64), intent(out) :: response64(nun,ngeff)
    real(real64), intent(inout) :: reps64(MAXI,ngeff), eps64(ngeff)
    logical, intent(inout) :: nconv(ngeff)
    integer(int64), intent(out) :: cutoff_delta64
    logical, intent(out) :: ok

    integer :: i, ii, iter, j, k, l
    integer, allocatable :: kmax(:)
    integer(int64) :: child_delta64
    logical :: child_ok, rhs_pending
    real(real64) :: epsinto64, hr64, w1, w2, znu64
    real(real64), allocatable :: denom64(:), rho64(:)
    real(real64), allocatable :: rhs64(:,:), gar64(:,:), flout64(:,:)
    real(real64), allocatable :: residual64(:,:), g64(:,:), c64(:,:)
    real(real64), allocatable :: sn64(:,:), v64(:,:,:), h64(:,:,:)

    cutoff_delta64 = 0_int64
    ok = .false.
    response64 = +0.0_real64
    if (MAXI /= 20 .or. NSTART /= 10 .or. MAXIT /= 19) return
    if (ngeff <= 0 .or. ngeff > NGRP .or. nun /= KPN) return
    if (epsi64 <= 0.0_real64 .or. .not. ieee_is_finite(epsi64)) return
    if (.not. all(ieee_is_finite(qfr64))) return
    if (.not. all(ieee_is_finite(phiin64))) return
    if (.not. all(ieee_is_finite(source64))) return

    epsinto64 = epsi64 / 100.0_real64
    allocate(denom64(ngeff), rho64(ngeff), kmax(ngeff))
    allocate(rhs64(nun,ngeff), gar64(nun,ngeff), flout64(nun,ngeff))
    allocate(residual64(nun,ngeff), g64(NSTART+1,ngeff))
    allocate(c64(NSTART+1,ngeff), sn64(NSTART+1,ngeff))
    allocate(v64(nun,ngeff,NSTART+1))
    allocate(h64(NSTART+1,NSTART,ngeff))

    rho64 = +0.0_real64
    do ii = 1, ngeff
      denom64(ii) = sqrt(dot_product(qfr64(:,ii), qfr64(:,ii)))
      if (.not. ieee_is_finite(denom64(ii))) return
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

    do while (lnconv /= 0 .and. iter < MAXIT)
      iter = iter + 1
      call SPOMOC_SET_ROLE(1, iter)
      child_delta64 = 0_int64
      call MCGFL164(kpsys, iptrk, iftrak, iprint, ngeff, ngind, nun, &
          nbtr, nmax, nmu, nangl, nbatch, lc, matalb_trk, keyflx_trk3, &
          keycur_trk1, nzon_trk1, volume_trk32, caz1_track64, &
          caz2_track64, cpo32, zmu32, wzmu32, sc_by_group32, sigal32, &
          qfr64, phiin64, source64, response64, nconv, epsinto64, &
          child_delta64, child_ok)
      cutoff_delta64 = cutoff_delta64 + child_delta64
      if (.not. child_ok) return
      if (.not. all(ieee_is_finite(response64))) return
      if (iter == 1) call SPOMOC_PUBLISH()

      do ii = 1, ngeff
        reps64(iter,ii) = +0.0_real64
        if (.not. nconv(ii)) cycle
        residual64(:,ii) = response64(:,ii) - phiin64(:,ii)
        rho64(ii) = sqrt(dot_product(residual64(:,ii), &
            residual64(:,ii)))
        if (.not. ieee_is_finite(rho64(ii))) return
        reps64(iter,ii) = rho64(ii) / denom64(ii)
        if (.not. ieee_is_finite(reps64(iter,ii))) return
        eps64(ii) = reps64(iter,ii)
        itst(ii) = iter
        nconv(ii) = nconv(ii) .and. &
            rho64(ii) >= epsi64 * denom64(ii)
      end do
      lnconv = count(nconv)
      if (lnconv == 0) exit

      h64 = +0.0_real64
      v64 = +0.0_real64
      c64 = +0.0_real64
      sn64 = +0.0_real64
      g64 = +0.0_real64
      kmax = 0
      do ii = 1, ngeff
        if (.not. nconv(ii)) cycle
        if (rho64(ii) <= 0.0_real64) return
        g64(1,ii) = rho64(ii)
        v64(:,ii,1) = residual64(:,ii) / rho64(ii)
      end do

      if (rhs_pending) then
        rhs64 = +0.0_real64
        call SPOMOC_SET_ROLE(2, iter)
        child_delta64 = 0_int64
        call MCGFL164(kpsys, iptrk, iftrak, iprint, ngeff, ngind, nun, &
            nbtr, nmax, nmu, nangl, nbatch, lc, matalb_trk, &
            keyflx_trk3, keycur_trk1, nzon_trk1, volume_trk32, &
            caz1_track64, caz2_track64, cpo32, zmu32, wzmu32, &
            sc_by_group32, sigal32, qfr64, rhs64, source64, flout64, &
            nconv, epsinto64, child_delta64, child_ok)
        cutoff_delta64 = cutoff_delta64 + child_delta64
        if (.not. child_ok) return
        if (.not. all(ieee_is_finite(flout64))) return
        do ii = 1, ngeff
          if (nconv(ii)) rhs64(:,ii) = flout64(:,ii)
        end do
        rhs_pending = .false.
      end if

      k = 0
      do while (lnconv /= 0 .and. k < NSTART .and. iter < MAXIT)
        k = k + 1
        iter = iter + 1
        gar64 = v64(:,:,k)
        call SPOMOC_SET_ROLE(3, iter)
        child_delta64 = 0_int64
        call MCGFL164(kpsys, iptrk, iftrak, iprint, ngeff, ngind, nun, &
            nbtr, nmax, nmu, nangl, nbatch, lc, matalb_trk, &
            keyflx_trk3, keycur_trk1, nzon_trk1, volume_trk32, &
            caz1_track64, caz2_track64, cpo32, zmu32, wzmu32, &
            sc_by_group32, sigal32, qfr64, gar64, source64, flout64, &
            nconv, epsinto64, child_delta64, child_ok)
        cutoff_delta64 = cutoff_delta64 + child_delta64
        if (.not. child_ok) return
        if (.not. all(ieee_is_finite(flout64))) return
        v64(:,:,k+1) = v64(:,:,k) - flout64 + rhs64

        do ii = 1, ngeff
          reps64(iter,ii) = +0.0_real64
          if (.not. nconv(ii)) cycle
          kmax(ii) = k

          ! First modified Gram-Schmidt pass.
          do j = 1, k
            h64(j,k,ii) = dot_product(v64(:,ii,j), v64(:,ii,k+1))
            v64(:,ii,k+1) = v64(:,ii,k+1) - &
                h64(j,k,ii) * v64(:,ii,j)
          end do
          h64(k+1,k,ii) = sqrt(dot_product(v64(:,ii,k+1), &
              v64(:,ii,k+1)))
          if (.not. ieee_is_finite(h64(k+1,k,ii))) return

          ! Second modified Gram-Schmidt pass (reorthogonalization).
          do j = 1, k
            hr64 = dot_product(v64(:,ii,j), v64(:,ii,k+1))
            h64(j,k,ii) = h64(j,k,ii) + hr64
            v64(:,ii,k+1) = v64(:,ii,k+1) - hr64 * v64(:,ii,j)
          end do
          h64(k+1,k,ii) = sqrt(dot_product(v64(:,ii,k+1), &
              v64(:,ii,k+1)))
          if (.not. ieee_is_finite(h64(k+1,k,ii))) return
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
          if (.not. ieee_is_finite(znu64)) return
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
          if (.not. ieee_is_finite(reps64(iter,ii))) return
          eps64(ii) = reps64(iter,ii)
          itst(ii) = iter
          nconv(ii) = nconv(ii) .and. &
              rho64(ii) >= epsi64 * denom64(ii)
        end do
        lnconv = count(nconv)
      end do
      do ii = 1, ngeff
        k = kmax(ii)
        if (k == 0) cycle
        if (.not. all(ieee_is_finite(g64(1:k,ii)))) return
        if (.not. all(ieee_is_finite(h64(1:k,1:k,ii)))) return
        if (.not. all(ieee_is_finite(v64(:,ii,1:k)))) return
        if (abs(h64(k,k,ii)) <= 0.0_real64) return
        g64(k,ii) = g64(k,ii) / h64(k,k,ii)
        do l = k-1, 1, -1
          if (abs(h64(l,l,ii)) <= 0.0_real64) return
          w1 = g64(l,ii) - &
              dot_product(h64(l,l+1:k,ii), g64(l+1:k,ii))
          g64(l,ii) = w1 / h64(l,l,ii)
        end do
        do j = 1, k
          phiin64(:,ii) = phiin64(:,ii) + &
              g64(j,ii) * v64(:,ii,j)
        end do
        if (.not. all(ieee_is_finite(phiin64(:,ii)))) return
      end do
    end do

    lnconv = count(nconv)
    if (.not. all(ieee_is_finite(phiin64))) return
    if (.not. all(ieee_is_finite(source64))) return
    if (.not. all(ieee_is_finite(response64))) return
    ok = .true.
  end subroutine MCGMRE64

end module SPOR64_A8
