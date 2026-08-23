program test_a89_runtime_geometry
  ! No-transport shape test for the runtime-geometry A8/A9 boundary.
  use, intrinsic :: iso_c_binding, only : c_null_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use SPOR64_A8, only : SPOR64_A8_OPERATOR_PROBE, SPOR64_A8_RANK_PROBE
  use SPOR64_A9, only : FLU2DR64_CORE, SPOR64_A9_STATE_PROBE
  implicit none

  call run_case(8,8,6,'PIN-8')
  call run_case(132,6,12,'D4A-132')
  write(*,'(A)') &
      'A8/A9 RUNTIME-GEOMETRY PASS: pin and D4-A (132,144,12) tuple; no transport.'

contains

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
    title = 'SYNTHETIC NO-TRANSPORT'
    cutoff_visit64 = -1_int64
    accepted = .true.
    core_ok = .true.

    call FLU2DR64_CORE(c_null_ptr,c_null_ptr,0,0,title, &
        keyflx,matcod,vol32,xstrc32,xsdia0_32,keycur,matalb_surface, &
        albedo32,surfac32,njj_off,ijj_off,ipos_off,nscat_off, &
        scat_off32,fixed_source64,initial_flux64,leak1d64, &
        tol64,tol64,tol64,terminal_flux64,terminal_source64, &
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
