program test_a89_runtime_geometry
  ! No-transport shape test for the runtime-geometry A8/A9 boundary.
  use, intrinsic :: iso_c_binding, only : c_null_ptr, c_ptr
  use GANLIB
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_quiet_nan, ieee_value
  use SPOR64_RCONTRACT, only : SPOR64_ROUTE_CONTRACT, &
      SPOR64_RCONTRACT_LOAD
  use SPOR64_A8, only : SPOR64_A8_OPERATOR_PROBE, SPOR64_A8_RANK_PROBE
  use SPOR64_A8_ACA, only : MCGPRA64
  use SPOR64_A9, only : FLU2DR64_CORE, FLU2AC64, &
      SPOR64_A9_STATE_PROBE, SPOR64_A9_TERMINAL64
  implicit none

  call test_paca3_preconditioner()
  call test_flu2ac64()
  call run_case(8,8,6,'PIN-8')
  call run_case(132,6,12,'D4A-132')
  write(*,'(A)') &
      'A8/A9 RUNTIME-GEOMETRY PASS: pin and D4-A (132,144,12) tuple; no transport.'

contains

  subroutine test_paca3_preconditioner()
    integer, parameter :: n=2, lc=2, lc0=2
    integer :: im(n+1), mcu(lc), im0(n+1), mcu0(lc0), ju(n)
    real(real32) :: diagm32(n), cm32(lc), iludf32(n), ilucf32(lc0)
    real(real32) :: diagf32(n), cf32(lc)
    real(real64) :: xin64(n), xout64(n), expected64(n), work64(n)
    logical :: ok

    im = [0,1,2]
    mcu = [2,1]
    im0 = [0,1,2]
    mcu0 = [2,1]
    ju = [1,3]
    diagm32 = [2.0_real32,3.0_real32]
    cm32 = [0.5_real32,-0.25_real32]
    iludf32 = [0.5_real32,0.25_real32]
    ilucf32 = [0.2_real32,0.1_real32]
    diagf32 = +0.0_real32
    cf32 = cm32
    xin64 = [1.0_real64,2.0_real64]
    xout64 = +0.0_real64

    work64(1) = real(diagm32(1),real64)*xin64(1) + &
        real(cm32(1),real64)*xin64(2)
    work64(2) = real(diagm32(2),real64)*xin64(2) + &
        real(cm32(2),real64)*xin64(1)
    expected64(2) = (work64(2)-real(ilucf32(2),real64)*work64(1))* &
        real(iludf32(2),real64)
    expected64(1) = (work64(1)-real(ilucf32(1),real64)*expected64(2))* &
        real(iludf32(1),real64)

    call MCGPRA64(.true.,3,3,.false.,n,lc,im,mcu,ju,diagm32,cm32, &
        iludf32,ilucf32,diagf32,xin64,xout64,lc0,im0,mcu0,cf32,ok)
    call require(ok,'PACA3 MSRLUS2 path accepted')
    call require(all(abs(xout64-expected64) <= 1.0e-15_real64), &
        'PACA3 MSRLUS2 path preserves legacy operation order')

    xout64 = 99.0_real64
    call MCGPRA64(.true.,3,3,.false.,n,lc,im,mcu,ju,diagm32,cm32, &
        iludf32,ilucf32,diagf32,xin64,xout64,1,im0,mcu0,cf32,ok)
    call require(.not. ok,'PACA3 inconsistent LC0 rejected')
    write(*,'(A)') 'PASS: PACA3 REAL64 preconditioner and shape guard'
  end subroutine test_paca3_preconditioner

  subroutine make_a89_contract(contract_out,eps_radial_bits)
    type(SPOR64_ROUTE_CONTRACT), intent(out) :: contract_out
    integer(int32), intent(in) :: eps_radial_bits
    type(c_ptr) :: root
    real(real32) :: eps32(3)
    character(len=12) :: sig12, name12
    character(len=4) :: option4
    logical :: loaded
    call LCMOP(root,'A89RC',0,1,0)
    sig12 = 'L_RCONTRACT'
    name12 = 'A89-TEST'
    option4 = 'B0  '
    eps32 = transfer(eps_radial_bits,0.0_real32)
    call LCMPTC(root,'SIGNATURE',12,sig12)
    call LCMPTC(root,'CASE-NAME',12,name12)
    call LCMPUT(root,'EPS-TERMINAL',3,2,eps32)
    call LCMPUT(root,'FLU-CAPS',2,1,[500,740])
    call LCMPUT(root,'FLU-ACCE',2,1,[3,3])
    call LCMPTC(root,'FLU-OPTION',4,option4)
    call SPOR64_RCONTRACT_LOAD(root,contract_out,loaded)
    if (.not. loaded) error stop 'a89 contract failed to load'
    call LCMCL(root,2)
  end subroutine make_a89_contract

  subroutine test_flu2ac64()
    real(real64) :: flux64(1,2,3), flux_before64(1,2,3)
    real(real64) :: akeep64(3), akeep_before64(3), zmu64
    real(real64) :: residual_before64, residual_after64
    integer(int64) :: inactive_before64(3), inactive_after64(3)
    logical :: accepted, ok

    flux64(1,1,:) = ieee_value(0.0_real64,ieee_quiet_nan)
    flux64(1,2,:) = [0.0_real64, 1.0_real64, 0.0_real64]
    akeep64 = [1.0_real64, 2.0_real64, 1.0_real64]
    flux_before64 = flux64
    inactive_before64 = transfer(flux64(1,1,:),inactive_before64)
    residual_before64 = sum((flux64(:,2,3)-flux64(:,2,2))**2)
    call SPOR64_A9_TERMINAL64(0.0_real64,residual_before64, &
        0.0_real64,0.25_real64,0.25_real64,0.25_real64,1,4,accepted)
    call require(.not. accepted, &
        'raw outer defect rejects before variational acceleration')
    call FLU2AC64(2,1,2,flux64,akeep64,zmu64,ok)
    residual_after64 = sum((flux64(:,2,3)-flux64(:,2,2))**2)
    call require(ok,'FLU2AC64 positive factor accepted')
    call require(zmu64 == 0.5_real64,'FLU2AC64 exact positive factor')
    inactive_after64 = transfer(flux64(1,1,:),inactive_after64)
    call require(all(inactive_after64 == inactive_before64), &
        'FLU2AC64 ignores and preserves groups below IG0')
    call require(flux64(1,2,2) == 0.5_real64 .and. &
        flux64(1,2,3) == 0.5_real64, &
        'FLU2AC64 minimizes the active residual')
    call require(akeep64(2) == 1.5_real64 .and. &
        akeep64(3) == 1.5_real64, &
        'FLU2AC64 updates the eigenvalue history')
    call require(residual_after64 <= residual_before64, &
        'FLU2AC64 L2 residual is nonincreasing')
    call require(residual_after64 == 0.0_real64 .and. .not. accepted, &
        'zero extrapolated difference cannot override the raw gate')

    flux64(1,1,:) = [0.0_real64, 1.0_real64, 2.0_real64]
    flux64(1,2,:) = [3.0_real64, 4.0_real64, 5.0_real64]
    akeep64 = [1.0_real64, 2.0_real64, 3.0_real64]
    flux_before64 = flux64
    akeep_before64 = akeep64
    call FLU2AC64(2,1,1,flux64,akeep64,zmu64,ok)
    call require(ok,'FLU2AC64 zero curvature accepted')
    call require(zmu64 == 1.0_real64, &
        'FLU2AC64 zero curvature uses identity')
    call require(all(flux64 == flux_before64), &
        'FLU2AC64 zero curvature preserves flux bits')
    call require(all(akeep64 == akeep_before64), &
        'FLU2AC64 zero curvature preserves eigenvalue bits')

    flux64(1,1,:) = [0.0_real64, 1.0_real64, 3.0_real64]
    flux64(1,2,:) = [0.0_real64, 1.0_real64, 3.0_real64]
    akeep64 = [1.0_real64, 2.0_real64, 4.0_real64]
    flux_before64 = flux64
    akeep_before64 = akeep64
    call FLU2AC64(2,1,1,flux64,akeep64,zmu64,ok)
    call require(ok,'FLU2AC64 nonpositive factor accepted')
    call require(zmu64 == 1.0_real64, &
        'FLU2AC64 nonpositive factor uses identity')
    call require(all(flux64 == flux_before64), &
        'FLU2AC64 nonpositive factor preserves flux bits')
    call require(all(akeep64 == akeep_before64), &
        'FLU2AC64 nonpositive factor preserves eigenvalue bits')

    write(*,'(A)') 'PASS: FLU2AC64 exact residual-minimizing kernel'
  end subroutine test_flu2ac64

  subroutine run_case(nreg,nmat,nsurf,label)
    integer, intent(in) :: nreg, nmat, nsurf
    character(len=*), intent(in) :: label
    integer, parameter :: ngrp=370, nslice=8, ncode=6
    integer :: i, nunkno
    integer(int64) :: cutoff_visit64
    integer, allocatable :: keyflx(:), keyflx3(:,:,:), pjjind2(:,:)
    integer, allocatable :: matcod(:), keycur(:), matalb_surface(:)
    integer, allocatable :: njj_off(:,:), ijj_off(:,:), ipos_off(:,:)
    integer, allocatable :: nscat_off(:)
    real(real32) :: tol32
    type(SPOR64_ROUTE_CONTRACT) :: a89_contract
    real(real64) :: tol64
    real(real32), allocatable :: sc32(:,:), sigal32(:)
    real(real32), allocatable :: vol32(:), xstrc32(:,:), xsdia0_32(:,:)
    real(real32), allocatable :: albedo32(:), surfac32(:), scat_off32(:,:)
    real(real64), allocatable :: state64(:,:,:), fixed_source64(:,:)
    real(real64), allocatable :: initial_flux64(:,:), terminal_flux64(:,:)
    real(real64), allocatable :: terminal_source64(:,:), leak1d64(:)
    logical :: accepted, core_ok, probe_ok
    character(len=72) :: title

    nunkno = nreg+nsurf

    allocate(keyflx(nreg),keyflx3(nreg,1,1),pjjind2(1,2))
    keyflx = [(i,i=1,nreg)]
    keyflx3(:,1,1) = keyflx
    pjjind2 = 1
    call SPOR64_A8_RANK_PROBE(keyflx,keyflx3,pjjind2,probe_ok)
    call require(probe_ok,trim(label)//' A8 rank probe')

    allocate(sc32(0:nmat,1),sigal32(-ncode:nmat))
    sc32 = 0.0_real32
    sigal32 = 0.0_real32
    call SPOR64_A8_OPERATOR_PROBE(sc32,sigal32,probe_ok)
    call require(probe_ok,trim(label)//' A8 operator probe')

    allocate(state64(nunkno,ngrp,nslice))
    state64 = 1.0_real64
    call SPOR64_A9_STATE_PROBE(state64,probe_ok)
    call require(probe_ok,trim(label)//' A9 state probe')

    allocate(matcod(nreg),keycur(nsurf),matalb_surface(nsurf))
    allocate(njj_off(nmat,ngrp),ijj_off(nmat,ngrp), &
        ipos_off(nmat,ngrp),nscat_off(ngrp))
    allocate(vol32(nreg),xstrc32(0:nmat,ngrp), &
        xsdia0_32(0:nmat,ngrp),albedo32(ncode),surfac32(nsurf))
    allocate(scat_off32(nmat*ngrp,ngrp))
    allocate(fixed_source64(nunkno,ngrp),initial_flux64(nunkno,ngrp), &
        terminal_flux64(nunkno,ngrp),terminal_source64(nunkno,ngrp), &
        leak1d64(ngrp))

    do i = 1, nreg
      matcod(i) = 1 + mod(i-1,nmat)
    end do
    keycur = [(nreg+i,i=1,nsurf)]
    matalb_surface = [(-(1+mod(i-1,ncode)),i=1,nsurf)]
    njj_off = 0
    ijj_off = 0
    ipos_off = 0
    nscat_off = 0
    vol32 = 1.0_real32
    xstrc32 = 0.0_real32
    xsdia0_32 = 0.0_real32
    albedo32 = 0.0_real32
    surfac32 = 1.0_real32
    scat_off32 = 0.0_real32
    fixed_source64 = 1.0_real64
    initial_flux64 = 1.0_real64
    terminal_flux64 = 17.0_real64
    terminal_source64 = 19.0_real64
    leak1d64 = 0.0_real64
    tol32 = transfer(int(z'348637bd',int32),0.0_real32)
    tol64 = real(tol32,real64)
    call make_a89_contract(a89_contract,transfer(tol32,0_int32))
    title = 'SYNTHETIC NO-TRANSPORT'
    cutoff_visit64 = -1_int64
    accepted = .true.
    core_ok = .true.

    call FLU2DR64_CORE(c_null_ptr,c_null_ptr,0,0,title, &
        keyflx,matcod,vol32,xstrc32,xsdia0_32,keycur,matalb_surface, &
        albedo32,surfac32,njj_off,ijj_off,ipos_off,nscat_off, &
        scat_off32,fixed_source64,initial_flux64,leak1d64, &
        tol64,tol64,tol64,a89_contract,terminal_flux64, &
        terminal_source64, &
        cutoff_visit64,accepted,core_ok)
    call require(.not. accepted,trim(label)//' null core not accepted')
    call require(.not. core_ok,trim(label)//' null core fail closed')
    call require(cutoff_visit64 == 0_int64, &
        trim(label)//' null core cutoff reset')
    call require(all(terminal_flux64 == 0.0_real64), &
        trim(label)//' null core flux reset')
    call require(all(terminal_source64 == 0.0_real64), &
        trim(label)//' null core source reset')

    write(*,'(A,1X,A,3(A,I0))') 'PASS:',trim(label), &
        ' NREG=',nreg,' NMAT=',nmat,' NUNKNO=',nunkno
  end subroutine run_case


  subroutine require(condition,label)
    logical, intent(in) :: condition
    character(len=*), intent(in) :: label

    if (.not. condition) then
      write(*,'(A,1X,A)') 'FAIL:',trim(label)
      error stop 1
    end if
  end subroutine require

end program test_a89_runtime_geometry
