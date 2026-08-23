program test_b2c_runtime_dimensions
  ! No-transport admission test for the REAL64 publication boundary.
  ! The 8-region case locks the existing pin-cell record arithmetic; the
  ! 132-region case proves that the same boundary uses runtime dimensions.
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use GANLIB
  use SPOR64_B2C, only : SPOR64_B2C_HOST_COMMITTED, &
      SPOR64_B2C_PREFLIGHT_FAILED, SPOR64_B2C_PUBLISH, &
      SPOR64_B2C_PUBLISH_CONT
  use SPOR64_VERIFY, only : EMPTY_MEMORY_ROOT
  implicit none

  call run_case(8,8,14,'B2C-PIN8',.false.)
  call run_case(132,6,144,'B2C-D4A132',.true.)
  call reject_duplicate_key()
  call reject_shape_mismatch()
  write(*,'(A)') &
      'B2C RUNTIME-DIMENSION PASS: pin and D4-A 144-unknown structural publication only.'

contains

  subroutine run_case(nreg,nmat,nunkno,name,continuation)
    integer, intent(in) :: nreg, nmat, nunkno
    character(len=*), intent(in) :: name
    logical, intent(in) :: continuation
    integer, parameter :: ngrp=370, nstate=40
    integer :: i, ig, actual_length, actual_type, status
    integer :: state(nstate)
    integer, allocatable :: keyflx(:), key_found(:)
    integer, allocatable :: imerge(:), imerge_found(:)
    real(real32) :: tol32, eps_found(5)
    real(real32), allocatable :: leakage32(:)
    real(real32), allocatable :: flux32(:), source32(:)
    real(real64), allocatable :: flux64(:,:), source64(:,:), leakage64(:)
    real(real64), allocatable :: flux_found64(:), source_found64(:)
    character(len=12) :: signature
    type(c_ptr) :: root, authority, authority_flux, authority_source
    type(c_ptr) :: legacy_flux, legacy_source
    type(c_ptr) :: seed, seed_authority, seed_flux
    real(real64) :: seed_rho64
    integer :: seed_plane, seed_epoch
    character(len=12) :: seed_state

    allocate(keyflx(nreg),key_found(nreg),imerge(nmat), &
        imerge_found(nmat),leakage32(ngrp),leakage64(ngrp))
    allocate(flux64(nunkno,ngrp),source64(nunkno,ngrp))
    allocate(flux32(nunkno),source32(nunkno))
    allocate(flux_found64(nunkno),source_found64(nunkno))

    do i = 1, nreg
      keyflx(i) = i
    end do
    imerge = 1
    do ig = 1, ngrp
      leakage32(ig) = real(ig,real32) * 1.0e-7_real32
      leakage64(ig) = real(leakage32(ig),real64)
      do i = 1, nunkno
        flux64(i,ig) = real(i,real64) + real(ig,real64) * 1.0e-6_real64
        source64(i,ig) = real(2*i,real64) + &
            real(ig,real64) * 5.0e-7_real64
      end do
    end do
    tol32 = transfer(int(z'348637bd',int32),0.0_real32)

    call LCMOP(root,name,0,1,0)
    call require(c_associated(root),'memory root creation')
    if (continuation) then
      call LCMOP(seed,'B2C-SEED',0,1,0)
      seed_authority = LCMDID(seed,'SPOT-R64')
      seed_rho64 = 0.75_real64
      seed_plane = 2
      seed_epoch = 7
      seed_state = 'PROJECTED'
      call LCMPUT(seed_authority,'RHO',1,4,seed_rho64)
      call LCMPUT(seed_authority,'PLANE',1,1,seed_plane)
      seed_flux = LCMLID(seed_authority,'FLUX',ngrp)
      do ig = 1, ngrp
        call LCMPDL(seed_flux,ig,nunkno,4,flux64(:,ig))
      end do
      call LCMPTC(seed_authority,'STATE',12,seed_state)
      call LCMPUT(seed_authority,'EPOCH',1,1,seed_epoch)
      call SPOR64_B2C_PUBLISH_CONT(root,seed,4,flux64,source64, &
          keyflx,1,imerge,leakage32,leakage64,tol32,tol32,tol32, &
          'B0  ','MACRO0      ','TRACK       ','SYSTEM      ',status)
    else
      call SPOR64_B2C_PUBLISH(root,4,flux64,source64,keyflx,1,imerge, &
          leakage32,tol32,tol32,tol32,'B0  ','MACRO0      ', &
          'TRACK       ','SYSTEM      ',status)
    end if
    call require(status == SPOR64_B2C_HOST_COMMITTED, &
        trim(name)//' publication status')

    signature = ' '
    call LCMGTC(root,'SIGNATURE',12,signature)
    call require(signature == 'L_FLUX',trim(name)//' signature')
    call LCMGET(root,'STATE-VECTOR',state)
    call require(state(1) == ngrp,trim(name)//' group count')
    call require(state(2) == nunkno,trim(name)//' unknown count')
    call require(all(state(8:10) == [3,3,1]), &
        trim(name)//' iteration state')
    call require(all(state(11:12) == [740,500]), &
        trim(name)//' iteration limits')
    call require(state(17) == nmat,trim(name)//' material count')
    call require(state(18) == 1,trim(name)//' merge count')
    call LCMGET(root,'EPS-CONVERGE',eps_found)
    do i = 1, 3
      call require(transfer(eps_found(i),0_int32) == &
          int(z'348637bd',int32),trim(name)//' frozen tolerance bits')
    end do
    call require(all(transfer(eps_found(4:5),[0_int32,0_int32]) == &
        [0_int32,0_int32]),trim(name)//' unused tolerance slots')

    call LCMLEN(root,'KEYFLX',actual_length,actual_type)
    call require(actual_length == nreg .and. actual_type == 1, &
        trim(name)//' KEYFLX shape')
    call LCMGET(root,'KEYFLX',key_found)
    call require(all(key_found == keyflx),trim(name)//' KEYFLX values')
    call LCMLEN(root,'IMERGE-LEAK',actual_length,actual_type)
    call require(actual_length == nmat .and. actual_type == 1, &
        trim(name)//' IMERGE shape')
    call LCMGET(root,'IMERGE-LEAK',imerge_found)
    call require(all(imerge_found == imerge),trim(name)//' IMERGE values')
    if (continuation) then
      call LCMLEN(root,'LEAK1D64',actual_length,actual_type)
      call require(actual_length == ngrp .and. actual_type == 4, &
          trim(name)//' REAL64 leakage shape')
    end if

    authority = LCMGID(root,'SPOT-R64')
    call require(c_associated(authority),trim(name)//' REAL64 authority')
    authority_flux = LCMGID(authority,'FLUX')
    authority_source = LCMGID(authority,'SOUR')
    legacy_flux = LCMGID(root,'FLUX')
    legacy_source = LCMGID(root,'SOUR')
    call require(c_associated(authority_flux) .and. &
        c_associated(authority_source),'REAL64 authority lists')
    call require(c_associated(legacy_flux) .and. &
        c_associated(legacy_source),'REAL32 mirror lists')

    do ig = 1, ngrp
      call LCMLEL(authority_flux,ig,actual_length,actual_type)
      call require(actual_length == nunkno .and. actual_type == 4, &
          trim(name)//' authority FLUX shape')
      call LCMLEL(authority_source,ig,actual_length,actual_type)
      call require(actual_length == nunkno .and. actual_type == 4, &
          trim(name)//' authority SOUR shape')
      call LCMLEL(legacy_flux,ig,actual_length,actual_type)
      call require(actual_length == nunkno .and. actual_type == 2, &
          trim(name)//' mirror FLUX shape')
      call LCMLEL(legacy_source,ig,actual_length,actual_type)
      call require(actual_length == nunkno .and. actual_type == 2, &
          trim(name)//' mirror SOUR shape')
      call LCMGDL(authority_flux,ig,flux_found64)
      call LCMGDL(authority_source,ig,source_found64)
      call LCMGDL(legacy_flux,ig,flux32)
      call LCMGDL(legacy_source,ig,source32)
      do i = 1, nunkno
        call require(transfer(flux_found64(i),0_int64) == &
            transfer(flux64(i,ig),0_int64),trim(name)//' REAL64 FLUX bits')
        call require(transfer(source_found64(i),0_int64) == &
            transfer(source64(i,ig),0_int64),trim(name)//' REAL64 SOUR bits')
        call require(transfer(flux32(i),0_int32) == &
            transfer(real(flux64(i,ig),real32),0_int32), &
            trim(name)//' REAL32 FLUX mirror bits')
        call require(transfer(source32(i),0_int32) == &
            transfer(real(source64(i,ig),real32),0_int32), &
            trim(name)//' REAL32 SOUR mirror bits')
      end do
    end do
    call LCMCL(root,2)
    if (continuation) call LCMCL(seed,2)
  end subroutine run_case


  subroutine reject_duplicate_key()
    integer, parameter :: ngrp=370, nreg=8, nmat=8, nunkno=14
    integer :: status
    integer :: keyflx(nreg), imerge(nmat)
    real(real32) :: leakage32(ngrp), tol32
    real(real64) :: flux64(nunkno,ngrp), source64(nunkno,ngrp)
    type(c_ptr) :: root

    keyflx = [1,2,3,4,5,6,7,7]
    imerge = 1
    leakage32 = 0.0_real32
    flux64 = 1.0_real64
    source64 = 2.0_real64
    tol32 = transfer(int(z'348637bd',int32),0.0_real32)
    call LCMOP(root,'B2C-BADKEY',0,1,0)
    call SPOR64_B2C_PUBLISH(root,4,flux64,source64,keyflx,1,imerge, &
        leakage32,tol32,tol32,tol32,'B0  ','MACRO0      ', &
        'TRACK       ','SYSTEM      ', &
        status)
    call require(status == SPOR64_B2C_PREFLIGHT_FAILED, &
        'duplicate KEYFLX rejection')
    call require(EMPTY_MEMORY_ROOT(root),'duplicate KEYFLX no-write rule')
    call LCMCL(root,2)
  end subroutine reject_duplicate_key


  subroutine reject_shape_mismatch()
    integer, parameter :: ngrp=370, nreg=8, nmat=8, nunkno=14
    integer :: status, i
    integer :: keyflx(nreg), imerge(nmat)
    real(real32) :: leakage32(ngrp), tol32
    real(real64) :: flux64(nunkno,ngrp), source64(nunkno-1,ngrp)
    type(c_ptr) :: root

    keyflx = [(i,i=1,nreg)]
    imerge = 1
    leakage32 = 0.0_real32
    flux64 = 1.0_real64
    source64 = 2.0_real64
    tol32 = transfer(int(z'348637bd',int32),0.0_real32)
    call LCMOP(root,'B2C-BADSHAP',0,1,0)
    call SPOR64_B2C_PUBLISH(root,4,flux64,source64,keyflx,1,imerge, &
        leakage32,tol32,tol32,tol32,'B0  ','MACRO0      ', &
        'TRACK       ','SYSTEM      ', &
        status)
    call require(status == SPOR64_B2C_PREFLIGHT_FAILED, &
        'mismatched terminal shape rejection')
    call require(EMPTY_MEMORY_ROOT(root),'mismatched shape no-write rule')
    call LCMCL(root,2)
  end subroutine reject_shape_mismatch


  subroutine require(condition,label)
    logical, intent(in) :: condition
    character(len=*), intent(in) :: label
    if (.not. condition) then
      write(*,'(A,1X,A)') 'FAIL:',trim(label)
      error stop 1
    end if
  end subroutine require

end program test_b2c_runtime_dimensions
