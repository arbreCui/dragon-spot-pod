module SPOR64_A9
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use SPOR64_A8, only : DOORFV64
  implicit none
  private

  integer, parameter :: NGRP = 370
  integer, parameter :: NREG = 8
  integer, parameter :: NSOUT = 6
  integer, parameter :: NUNKNO = 14
  integer, parameter :: NMAT = 8
  integer, parameter :: NSLICE = 8
  integer, parameter :: MAXOUT = 500
  integer, parameter :: MAXINR = 740
  integer, parameter :: NCTOT = 6
  integer, parameter :: NCPTM = 3
  integer, parameter :: IINR_STRICT = 1
  integer, parameter :: IINR_NEAR = 2
  integer, parameter :: IINR_CAP = 3

  integer, parameter :: kind_guard = 1 / merge(1, 0, &
      kind(1.0) == real32 .and. kind(0.0d0) == real64)
  real(real32), parameter :: FROZEN_TOL32 = &
      transfer(int(z'348637bd',int32),0.0_real32)
  real(real64), parameter :: FROZEN_TOL64 = &
      real(FROZEN_TOL32,real64)
  integer(int64), parameter :: FROZEN_TOL64_BITS = &
      transfer(FROZEN_TOL64,0_int64)

  public :: FLU2DR64_CORE, FLUBAL64, FLU2AC64
  public :: SPOR64_A9_TERMINAL64
  public :: SPOR64_A9_STATE_PROBE, SPOR64_A9_OPERATOR_PROBE
  public :: SPOR64_A9_COUNTER_PROBE

  interface
    subroutine ALSBD(n,is,b,ier,maxn)
      import :: real64
      integer :: n, is, ier, maxn
      real(real64) :: b(maxn,*)
    end subroutine ALSBD
  end interface

contains

  subroutine FLU2DR64_CORE(jpsys_group,iptrk,iftrak,impx,title, &
      keyflx_base1,matcod,vol32,xstrc32,xsdia0_32,keycur, &
      matalb_surface,albedo32,surfac32,njj_off,ijj_off,ipos_off, &
      nscat_off,scat_off32,fixed_source64,initial_flux64, &
      leak1d64,epsinr64,epsunk64,epsout64,terminal_flux64, &
      terminal_source64,cutoff_visit64,accepted,ok)
    type(c_ptr), intent(in) :: jpsys_group, iptrk
    integer, intent(in) :: iftrak, impx
    character(len=72), intent(in) :: title
    integer, intent(in) :: keyflx_base1(NREG), matcod(NREG)
    integer, intent(in) :: keycur(NSOUT), matalb_surface(NSOUT)
    integer, intent(in) :: njj_off(NMAT,NGRP), ijj_off(NMAT,NGRP)
    integer, intent(in) :: ipos_off(NMAT,NGRP), nscat_off(NGRP)
    real(real32), intent(in) :: vol32(NREG)
    real(real32), intent(in) :: xstrc32(0:NMAT,NGRP)
    real(real32), intent(in) :: xsdia0_32(0:NMAT,NGRP)
    real(real32), intent(in) :: albedo32(NSOUT), surfac32(NSOUT)
    real(real32), intent(in) :: scat_off32(NMAT*NGRP,NGRP)
    real(real64), intent(in) :: fixed_source64(NUNKNO,NGRP)
    real(real64), intent(in) :: initial_flux64(NUNKNO,NGRP)
    real(real64), intent(in) :: leak1d64(NGRP)
    real(real64), intent(in) :: epsinr64, epsunk64, epsout64
    real(real64), intent(out) :: terminal_flux64(NUNKNO,NGRP)
    real(real64), intent(out) :: terminal_source64(NUNKNO,NGRP)
    integer(int64), intent(out) :: cutoff_visit64
    logical, intent(out) :: accepted, ok

    integer :: akeep_index, allocation_status, ig, igdeb, igdeb_entry
    integer :: iinr_state
    integer :: ir, it, jt, jg, jnd, ibm, ind, p
    integer :: npsys(NGRP)
    integer(int64) :: cutoff_delta64
    logical :: accel_ok, balance_ok, child_ok, inner_finished
    logical :: norm_ok, operator_ok
    logical :: seen_unknown(NUNKNO)
    real(real64) :: akeep64(NSLICE), einr64, einr_last64
    real(real64) :: eext64, eunk64, group_error64, zmu64
    real(real64), allocatable :: flux64(:,:,:)
    real(real64) :: xcsou64(NGRP)

    terminal_flux64 = +0.0_real64
    terminal_source64 = +0.0_real64
    cutoff_visit64 = 0_int64
    accepted = .false.
    ok = .false.

    if (.not. c_associated(jpsys_group) .or. &
        .not. c_associated(iptrk)) return
    if (iftrak <= 0) return
    if (transfer(epsinr64,0_int64) /= FROZEN_TOL64_BITS) return
    if (transfer(epsunk64,0_int64) /= FROZEN_TOL64_BITS) return
    if (transfer(epsout64,0_int64) /= FROZEN_TOL64_BITS) return
    if (.not. all(ieee_is_finite(leak1d64))) return
    if (.not. all(ieee_is_finite(initial_flux64))) return
    if (.not. all(ieee_is_finite(fixed_source64))) return
    if (any(fixed_source64 < 0.0_real64)) return
    if (.not. all(ieee_is_finite(vol32)) .or. &
        any(vol32 <= 0.0_real32)) return
    if (.not. all(ieee_is_finite(xstrc32))) return
    if (.not. all(ieee_is_finite(xsdia0_32))) return
    if (.not. all(ieee_is_finite(albedo32))) return
    if (.not. all(ieee_is_finite(surfac32)) .or. &
        any(surfac32 <= 0.0_real32)) return

    seen_unknown = .false.
    do ir = 1, NREG
      if (keyflx_base1(ir) < 1 .or. keyflx_base1(ir) > NUNKNO) return
      if (seen_unknown(keyflx_base1(ir))) return
      seen_unknown(keyflx_base1(ir)) = .true.
      if (matcod(ir) < 1 .or. matcod(ir) > NMAT) return
    end do
    do ir = 1, NSOUT
      if (keycur(ir) < 1 .or. keycur(ir) > NUNKNO) return
      if (seen_unknown(keycur(ir))) return
      seen_unknown(keycur(ir)) = .true.
      if (matalb_surface(ir) > -1 .or. &
          matalb_surface(ir) < -NSOUT) return
    end do
    if (.not. all(seen_unknown)) return

    call VALIDATE_OFFGROUP32(njj_off,ijj_off,ipos_off,nscat_off, &
        scat_off32,operator_ok)
    if (.not. operator_ok) return

    ! The owner storage is defined first.  Only the present outer flux is an
    ! ingress value; every other live slice is populated by the legacy copy
    ! order before it is used.
    allocate(flux64(NUNKNO,NGRP,NSLICE),stat=allocation_status)
    if (allocation_status /= 0) return
    flux64 = +0.0_real64
    flux64(:,:,2) = initial_flux64
    akeep64 = +0.0_real64
    do akeep_index = 5, 7
      akeep64(akeep_index) = 1.0_real64
    end do

    do it = 1, MAXOUT
      flux64(:,:,4) = fixed_source64
      xcsou64 = +0.0_real64
      do ig = 1, NGRP
        do ir = 1, NREG
          ind = keyflx_base1(ir)
          xcsou64(ig) = xcsou64(ig) + flux64(ind,ig,4) * &
              real(vol32(ir),real64)
        end do
      end do
      if (.not. all(ieee_is_finite(xcsou64))) return

      ! NBS is absent on the frozen route.  Preserve the legacy scan even
      ! though the admitted first-group integral proves IGDEB=1.
      igdeb = NGRP + 1
      do ig = 1, NGRP
        if (xcsou64(ig) > 0.0_real64) then
          igdeb = ig
          exit
        end if
      end do
      if (igdeb /= 1 .or. xcsou64(1) <= 0.0_real64) return

      flux64(:,:,6) = flux64(:,:,2)
      iinr_state = 0
      einr_last64 = +0.0_real64
      inner_finished = .false.

      do jt = 1, MAXINR
        flux64(:,igdeb:NGRP,7) = flux64(:,igdeb:NGRP,6)
        flux64(:,igdeb:NGRP,8) = flux64(:,igdeb:NGRP,4)

        ! Frozen isotropic ITPIJ=1 source construction.  Destination groups
        ! and regions ascend; the packed source group descends exactly as in
        ! FLU2DR.  Self scattering is already represented inside MCCG.
        do ig = igdeb, NGRP
          do ir = 1, NREG
            ibm = matcod(ir)
            ind = keyflx_base1(ir)
            jg = ijj_off(ibm,ig)
            do jnd = 1, njj_off(ibm,ig)
              p = ipos_off(ibm,ig) + ijj_off(ibm,ig) - jg
              if (jg /= ig) then
                flux64(ind,ig,8) = flux64(ind,ig,8) + &
                    real(scat_off32(p,ig),real64) * flux64(ind,jg,7)
              end if
              jg = jg - 1
            end do
          end do
        end do
        if (.not. all(ieee_is_finite(flux64(:,igdeb:NGRP,8)))) return

        npsys = 0
        do ig = igdeb, NGRP
          npsys(ig) = ig
        end do
        cutoff_delta64 = 0_int64
        call DOORFV64(jpsys_group,npsys,iptrk,iftrak,impx,NGRP,NUNKNO, &
            keyflx_base1,title,leak1d64,flux64(:,:,8),flux64(:,:,7), &
            cutoff_delta64,child_ok)
        if (cutoff_delta64 < 0_int64) return
        if (cutoff_visit64 > huge(cutoff_visit64)-cutoff_delta64) return
        cutoff_visit64 = cutoff_visit64 + cutoff_delta64
        if (.not. child_ok) return
        if (.not. all(ieee_is_finite(flux64(:,igdeb:NGRP,7)))) return

        call FLUBAL64(matcod,vol32,keyflx_base1,xstrc32,xsdia0_32, &
            leak1d64,xcsou64,igdeb,keycur,matalb_surface,albedo32, &
            surfac32,njj_off,ijj_off,ipos_off,nscat_off,scat_off32, &
            flux64(:,:,7),balance_ok)
        if (.not. balance_ok) return

        if (mod(jt-1,NCTOT) >= NCPTM) then
          call FLU2AC64(NGRP,NUNKNO,igdeb,flux64(:,:,5:7), &
              akeep64(5:7),zmu64,accel_ok)
          if (.not. accel_ok) return
        else
          zmu64 = 1.0_real64
        end if

        einr64 = +0.0_real64
        igdeb_entry = igdeb
        do ig = igdeb_entry, NGRP
          call SCALAR_GROUP_NORM64(flux64(:,ig,6),flux64(:,ig,7), &
              keyflx_base1,group_error64,norm_ok)
          if (.not. norm_ok) return
          flux64(:,ig,5) = flux64(:,ig,6)
          flux64(:,ig,6) = flux64(:,ig,7)
          if (group_error64 < epsinr64 .and. igdeb == ig) then
            igdeb = igdeb + 1
          end if
          einr64 = max(einr64,group_error64)
        end do
        einr_last64 = einr64

        if (einr64 < epsinr64) then
          iinr_state = IINR_STRICT
          inner_finished = .true.
          exit
        end if
        ! This inherited near condition only schedules the next outer visit;
        ! SPOR64_A9_TERMINAL64 never treats it as acceptance.
        if (igdeb > 1 .and. einr64 < 10.0_real64*epsinr64) then
          iinr_state = IINR_NEAR
          inner_finished = .true.
          exit
        end if
      end do
      if (.not. inner_finished) iinr_state = IINR_CAP

      flux64(:,:,3) = flux64(:,:,7)
      flux64(:,:,4) = flux64(:,:,8)
      eext64 = +0.0_real64
      akeep64(3) = 1.0_real64

      if (mod(it-1,NCTOT) >= NCPTM) then
        call FLU2AC64(NGRP,NUNKNO,1,flux64(:,:,1:3), &
            akeep64(1:3),zmu64,accel_ok)
        if (.not. accel_ok) return
      else
        zmu64 = 1.0_real64
      end if

      eunk64 = +0.0_real64
      do ig = 1, NGRP
        call SCALAR_GROUP_NORM64(flux64(:,ig,2),flux64(:,ig,3), &
            keyflx_base1,group_error64,norm_ok)
        if (.not. norm_ok) return
        flux64(:,ig,1) = flux64(:,ig,2)
        flux64(:,ig,2) = flux64(:,ig,3)
        eunk64 = max(eunk64,group_error64)
      end do
      akeep64(1) = akeep64(2)
      akeep64(2) = akeep64(3)

      call SPOR64_A9_TERMINAL64(eext64,eunk64,einr_last64, &
          epsout64,epsunk64,epsinr64,iinr_state,it,accepted)
      if (accepted) then
        if (.not. all(ieee_is_finite(flux64(:,:,3)))) then
          accepted = .false.
          return
        end if
        if (.not. all(ieee_is_finite(flux64(:,:,4)))) then
          accepted = .false.
          return
        end if
        terminal_flux64 = flux64(:,:,3)
        terminal_source64 = flux64(:,:,4)
        ok = .true.
        return
      end if
    end do

    ! Exhausting MAXOUT is a normal mathematical return.  It is not an
    ! accepted state and A9a has no publication capability.
    accepted = .false.
    ok = .true.
  end subroutine FLU2DR64_CORE

  subroutine FLUBAL64(matcod,vol32,keyflx_base1,xstrc32,xsdia0_32, &
      leak1d64,xcsou64,igdeb,keycur,matalb_surface,albedo32,surfac32, &
      njj_off,ijj_off,ipos_off,nscat_off,scat_off32,flux64,ok)
    integer, intent(in) :: matcod(NREG), keyflx_base1(NREG), igdeb
    integer, intent(in) :: keycur(NSOUT), matalb_surface(NSOUT)
    integer, intent(in) :: njj_off(NMAT,NGRP), ijj_off(NMAT,NGRP)
    integer, intent(in) :: ipos_off(NMAT,NGRP), nscat_off(NGRP)
    real(real32), intent(in) :: vol32(NREG)
    real(real32), intent(in) :: xstrc32(0:NMAT,NGRP)
    real(real32), intent(in) :: xsdia0_32(0:NMAT,NGRP)
    real(real64), intent(in) :: leak1d64(NGRP)
    real(real32), intent(in) :: albedo32(NSOUT), surfac32(NSOUT)
    real(real32), intent(in) :: scat_off32(NMAT*NGRP,NGRP)
    real(real64), intent(in) :: xcsou64(NGRP)
    real(real64), contiguous, intent(inout) :: flux64(:,:)
    logical, intent(out) :: ok

    integer :: ier, ifscat, igr, ioff, ir, isur, jgr, ngreb
    integer :: ibm, ind, p
    real(real64), allocatable :: rebal64(:,:)

    ok = .false.
    if (igdeb < 1 .or. igdeb > NGRP) return
    if (size(flux64,1) /= NUNKNO .or. size(flux64,2) /= NGRP) return
    if (.not. all(ieee_is_finite(xcsou64))) return
    if (.not. all(ieee_is_finite(flux64))) return
    if (.not. all(ieee_is_finite(vol32))) return
    if (.not. all(ieee_is_finite(xstrc32))) return
    if (.not. all(ieee_is_finite(xsdia0_32))) return
    if (.not. all(ieee_is_finite(albedo32))) return
    if (.not. all(ieee_is_finite(surfac32))) return

    ngreb = NGRP - igdeb + 1
    allocate(rebal64(NGRP,NGRP+1))
    rebal64 = +0.0_real64

    do igr = igdeb, NGRP
      ioff = igr - igdeb + 1
      rebal64(ioff,ngreb+1) = xcsou64(igr)

      do isur = 1, NSOUT
        if (-matalb_surface(isur) < 1 .or. &
            -matalb_surface(isur) > NSOUT) return
        if (keycur(isur) < 1 .or. keycur(isur) > NUNKNO) return
        rebal64(ioff,ioff) = rebal64(ioff,ioff) + &
            (1.0_real64-real(albedo32(-matalb_surface(isur)),real64)) * &
            flux64(keycur(isur),igr) * real(surfac32(isur),real64)
      end do

      do ir = 1, NREG
        ibm = matcod(ir)
        if (ibm < 1 .or. ibm > NMAT) return
        ind = keyflx_base1(ir)
        if (ind < 1 .or. ind > NUNKNO) return
        ifscat = ijj_off(ibm,igr) - njj_off(ibm,igr) + 1

        ! Already-converged groups contribute to the right-hand side.
        do jgr = ifscat, min(igdeb-1,ijj_off(ibm,igr))
          p = ipos_off(ibm,igr) + ijj_off(ibm,igr) - jgr
          if (p < 1 .or. p > nscat_off(igr)) return
          rebal64(ioff,ngreb+1) = rebal64(ioff,ngreb+1) + &
              flux64(ind,jgr) * real(scat_off32(p,igr),real64) * &
              real(vol32(ir),real64)
        end do

        ! Non-converged groups form the active matrix in ascending group
        ! order, which is the legacy FLUBAL accumulation order.
        do jgr = max(ifscat,igdeb), ijj_off(ibm,igr)
          p = ipos_off(ibm,igr) + ijj_off(ibm,igr) - jgr
          if (p < 1 .or. p > nscat_off(igr)) return
          if (jgr == igr) then
            rebal64(ioff,ioff) = rebal64(ioff,ioff) + &
                flux64(ind,igr) * &
                (real(xstrc32(ibm,igr),real64) - &
                 real(xsdia0_32(ibm,igr),real64) + &
                 leak1d64(igr)) * &
                real(vol32(ir),real64)
          else
            rebal64(ioff,jgr-igdeb+1) = &
                rebal64(ioff,jgr-igdeb+1) - flux64(ind,jgr) * &
                real(scat_off32(p,igr),real64) * &
                real(vol32(ir),real64)
          end if
        end do
      end do
    end do

    if (.not. all(ieee_is_finite(rebal64(:ngreb,:ngreb+1)))) return
    call ALSBD(ngreb,1,rebal64,ier,NGRP)
    if (ier /= 0) return
    if (.not. all(ieee_is_finite(rebal64(:ngreb,ngreb+1)))) return

    do igr = igdeb, NGRP
      ioff = igr - igdeb + 1
      do ind = 1, NUNKNO
        flux64(ind,igr) = flux64(ind,igr) * &
            rebal64(ioff,ngreb+1)
      end do
    end do
    if (.not. all(ieee_is_finite(flux64(:,igdeb:NGRP)))) return
    ok = .true.
  end subroutine FLUBAL64

  subroutine FLU2AC64(ng,nun,ig0,flux64,akeep64,zmu64,ok)
    integer, intent(in) :: ng, nun, ig0
    real(real64), contiguous, intent(inout) :: flux64(:,:,:)
    real(real64), contiguous, intent(inout) :: akeep64(:)
    real(real64), intent(out) :: zmu64
    logical, intent(out) :: ok

    integer :: ig, ir
    real(real64) :: denom64, dmu64, nom64, r1_64, r2_64

    zmu64 = 1.0_real64
    ok = .false.
    if (ng < 1 .or. nun < 1) return
    if (ig0 < 1 .or. ig0 > ng) return
    if (size(flux64,1) /= nun .or. size(flux64,2) /= ng .or. &
        size(flux64,3) /= 3) return
    if (size(akeep64) /= 3) return
    if (.not. all(ieee_is_finite(flux64))) return
    if (.not. all(ieee_is_finite(akeep64))) return

    nom64 = +0.0_real64
    denom64 = +0.0_real64
    do ig = ig0, ng
      do ir = 1, nun
        r1_64 = flux64(ir,ig,2) - flux64(ir,ig,1)
        r2_64 = flux64(ir,ig,3) - flux64(ir,ig,2)
        nom64 = nom64 + r1_64*(r2_64-r1_64)
        denom64 = denom64 + (r2_64-r1_64)*(r2_64-r1_64)
      end do
    end do
    if (.not. ieee_is_finite(nom64)) return
    if (.not. ieee_is_finite(denom64)) return

    ! Exact zero is not a fitted cutoff.  It avoids an undefined division
    ! and retains the legacy no-acceleration state with ZMU=1.
    if (denom64 <= 0.0_real64) then
      ok = .true.
      return
    end if
    dmu64 = -nom64/denom64
    if (.not. ieee_is_finite(dmu64)) return
    if (dmu64 > 0.0_real64) then
      zmu64 = dmu64
      do ig = ig0, ng
        do ir = 1, nun
          flux64(ir,ig,3) = flux64(ir,ig,2) + dmu64 * &
              (flux64(ir,ig,3)-flux64(ir,ig,2))
          flux64(ir,ig,2) = flux64(ir,ig,1) + dmu64 * &
              (flux64(ir,ig,2)-flux64(ir,ig,1))
        end do
      end do
      akeep64(3) = akeep64(2) + dmu64*(akeep64(3)-akeep64(2))
      akeep64(2) = akeep64(1) + dmu64*(akeep64(2)-akeep64(1))
    end if
    if (.not. all(ieee_is_finite(flux64))) return
    if (.not. all(ieee_is_finite(akeep64))) return
    ok = .true.
  end subroutine FLU2AC64

  pure subroutine SPOR64_A9_TERMINAL64(eext64,eunk64,einr_last64, &
      epsout64,epsunk64,epsinr64,iinr_state,outer_iteration,accepted)
    real(real64), intent(in) :: eext64, eunk64, einr_last64
    real(real64), intent(in) :: epsout64, epsunk64, epsinr64
    integer, intent(in) :: iinr_state, outer_iteration
    logical, intent(out) :: accepted

    accepted = eext64 < epsout64 .and. eunk64 < epsunk64 .and. &
        einr_last64 < epsinr64 .and. iinr_state == IINR_STRICT .and. &
        outer_iteration >= 2
  end subroutine SPOR64_A9_TERMINAL64

  subroutine SPOR64_A9_STATE_PROBE(state64,ok)
    real(real64), contiguous, intent(in) :: state64(:,:,:)
    logical, intent(out) :: ok

    ok = size(state64,1) == NUNKNO .and. size(state64,2) == NGRP .and. &
        size(state64,3) == NSLICE
    if (ok) ok = all(ieee_is_finite(state64))
  end subroutine SPOR64_A9_STATE_PROBE

  subroutine SPOR64_A9_OPERATOR_PROBE(operator32,ok)
    real(real32), contiguous, intent(in) :: operator32(:,:)
    logical, intent(out) :: ok

    ok = size(operator32) > 0
    if (ok) ok = all(ieee_is_finite(operator32))
  end subroutine SPOR64_A9_OPERATOR_PROBE

  subroutine SPOR64_A9_COUNTER_PROBE(counter64,ok)
    integer(int64), intent(in) :: counter64
    logical, intent(out) :: ok

    ok = counter64 >= 0_int64
  end subroutine SPOR64_A9_COUNTER_PROBE

  subroutine SCALAR_GROUP_NORM64(present64,new64,keyflx_base1, &
      group_error64,ok)
    real(real64), intent(in) :: present64(NUNKNO), new64(NUNKNO)
    integer, intent(in) :: keyflx_base1(NREG)
    real(real64), intent(out) :: group_error64
    logical, intent(out) :: ok

    integer :: ind, ir
    real(real64) :: difference64, denominator64

    group_error64 = +0.0_real64
    denominator64 = +0.0_real64
    ok = .false.
    do ir = 1, NREG
      ind = keyflx_base1(ir)
      if (ind < 1 .or. ind > NUNKNO) return
      difference64 = abs(present64(ind)-new64(ind))
      group_error64 = max(group_error64,difference64)
      denominator64 = max(denominator64,abs(new64(ind)))
    end do
    if (.not. ieee_is_finite(group_error64)) return
    if (.not. ieee_is_finite(denominator64)) return
    if (denominator64 <= 0.0_real64) return
    group_error64 = group_error64/denominator64
    if (.not. ieee_is_finite(group_error64)) return
    ok = .true.
  end subroutine SCALAR_GROUP_NORM64

  subroutine VALIDATE_OFFGROUP32(njj_off,ijj_off,ipos_off,nscat_off, &
      scat_off32,ok)
    integer, intent(in) :: njj_off(NMAT,NGRP), ijj_off(NMAT,NGRP)
    integer, intent(in) :: ipos_off(NMAT,NGRP), nscat_off(NGRP)
    real(real32), intent(in) :: scat_off32(NMAT*NGRP,NGRP)
    logical, intent(out) :: ok

    integer :: ibm, ifscat, ig, last_position

    ok = .false.
    do ig = 1, NGRP
      if (nscat_off(ig) < 0 .or. nscat_off(ig) > NMAT*NGRP) return
      if (nscat_off(ig) > 0) then
        if (.not. all(ieee_is_finite( &
            scat_off32(1:nscat_off(ig),ig)))) return
      end if
      do ibm = 1, NMAT
        if (njj_off(ibm,ig) < 0) return
        if (njj_off(ibm,ig) == 0) cycle
        if (ipos_off(ibm,ig) < 1) return
        last_position = ipos_off(ibm,ig) + njj_off(ibm,ig) - 1
        if (last_position > nscat_off(ig)) return
        if (ijj_off(ibm,ig) < 1 .or. ijj_off(ibm,ig) > NGRP) return
        ifscat = ijj_off(ibm,ig) - njj_off(ibm,ig) + 1
        if (ifscat < 1) return
      end do
    end do
    ok = .true.
  end subroutine VALIDATE_OFFGROUP32

end module SPOR64_A9
