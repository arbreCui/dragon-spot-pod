program test_spopod
  use, intrinsic :: iso_fortran_env, only : error_unit
  implicit none
  integer, parameter :: dp=kind(1.0d0)
  integer :: failures

  failures=0
  call test_full_rank_reconstruction(failures)
  call test_rank_is_mode_count(failures)
  call test_identical_snapshots(failures)
  call test_legacy_matches_promoted_inputs(failures)
  call test_real64_flux_perturbation(failures)
  call test_real64_volume_perturbation(failures)

  if (failures /= 0) then
    write(error_unit,'(a,i0)') 'LEVEL1 FAILURES: ',failures
    error stop 1
  endif
  write(*,'(a)') 'LEVEL1 PASS: volume-weighted modal POD algebra.'

contains

  subroutine test_full_rank_reconstruction(failures)
    integer, intent(inout) :: failures
    real :: phi(4,3),vol(4),basis(4,3),coeff(3,3)
    real(dp) :: sigma(3),rec_err,ortho_err,shape(4,3),recon(4,3)
    real(dp) :: weight(4),inner
    integer :: nmode,k,a,b

    phi=reshape([1.0,0.8,1.2,1.1, &
                 0.7,1.3,1.0,0.9, &
                 1.4,0.9,0.8,1.2],[4,3])
    vol=[0.5,1.0,1.5,2.0]
    call SPOPOD(4,3,phi,vol,0,nmode,basis,coeff,sigma, &
                rec_err,ortho_err,0,1)
    call assert_int('rank zero keeps numerical snapshot rank',nmode,3,failures)
    call assert_true('full-rank reconstruction error',rec_err < 2.0e-7_dp,failures)
    call assert_true('volume orthogonality diagnostic',ortho_err < 2.0e-7_dp,failures)

    weight=real(vol,dp)/sum(real(vol,dp))
    do k=1,3
      shape(:,k)=real(phi(:,k),dp)/sum(weight*real(phi(:,k),dp))
      recon(:,k)=matmul(real(basis(:,:nmode),dp),real(coeff(:nmode,k),dp))
    enddo
    call assert_true('full basis reconstructs normalized snapshots', &
      maxval(abs(recon-shape)) < 5.0e-7_dp,failures)
    do a=1,nmode
      do b=1,nmode
        inner=sum(weight*real(basis(:,a),dp)*real(basis(:,b),dp))
        if (a == b) inner=inner-1.0_dp
        call assert_true('explicit volume orthogonality',abs(inner)<5.0e-7_dp,failures)
      enddo
    enddo
    do k=1,3
      do a=1,nmode
        inner=sum(weight*real(basis(:,a),dp)*shape(:,k))
        call assert_close('coefficient is volume projection',inner, &
          real(coeff(a,k),dp),5.0e-7_dp,failures)
      enddo
    enddo
  end subroutine test_full_rank_reconstruction

  subroutine test_rank_is_mode_count(failures)
    integer, intent(inout) :: failures
    real :: phi(4,3),vol(4),basis(4,3),coeff(3,3)
    real(dp) :: sigma(3),rec_err,ortho_err
    integer :: nmode
    phi=reshape([1.0,0.8,1.2,1.1, &
                 0.7,1.3,1.0,0.9, &
                 1.4,0.9,0.8,1.2],[4,3])
    vol=[0.5,1.0,1.5,2.0]
    call SPOPOD(4,3,phi,vol,1,nmode,basis,coeff,sigma, &
                rec_err,ortho_err,0,1)
    call assert_int('requested rank is axial mode count',nmode,1,failures)
    call assert_true('rank-one truncation is non-exact',rec_err > 1.0e-8_dp,failures)
    call assert_true('rank-one basis remains orthonormal',ortho_err < 2.0e-7_dp,failures)
  end subroutine test_rank_is_mode_count

  subroutine test_identical_snapshots(failures)
    integer, intent(inout) :: failures
    real :: phi(3,3),vol(3),basis(3,3),coeff(3,3)
    real(dp) :: sigma(3),rec_err,ortho_err
    integer :: nmode
    phi(:,1)=[1.0,2.0,3.0]
    phi(:,2)=2.0*phi(:,1)
    phi(:,3)=0.25*phi(:,1)
    vol=[1.0,2.0,1.0]
    call SPOPOD(3,3,phi,vol,0,nmode,basis,coeff,sigma, &
                rec_err,ortho_err,0,1)
    call assert_int('scaled copies have one physical mode',nmode,1,failures)
    call assert_true('one mode exactly reconstructs scaled copies',rec_err<5.0e-7_dp,failures)
  end subroutine test_identical_snapshots

  subroutine test_legacy_matches_promoted_inputs(failures)
    integer, intent(inout) :: failures
    real :: phi(4,3),vol(4),basis(4,3),coeff(3,3)
    real :: basis64(4,3),coeff64(3,3)
    real(dp) :: sigma(3),rec_err,ortho_err,sigma64(3),rec64,ortho64
    integer :: nmode,nmode64,rank_req
    phi=reshape([1.0,0.8,1.2,1.1, &
                 0.7,1.3,1.0,0.9, &
                 1.4,0.9,0.8,1.2],[4,3])
    vol=[0.5,1.0,1.5,2.0]
    do rank_req=0,3
      call SPOPOD(4,3,phi,vol,rank_req,nmode,basis,coeff,sigma, &
                  rec_err,ortho_err,0,1)
      call SPOPOD64(4,3,real(phi,dp),real(vol,dp),rank_req, &
                    nmode64,basis64,coeff64,sigma64,rec64,ortho64,0,1)
      call assert_true('legacy and promoted REAL64 input results agree exactly', &
        nmode==nmode64 .and. all(basis==basis64) .and. &
        all(coeff==coeff64) .and. all(sigma==sigma64) .and. &
        rec_err==rec64 .and. ortho_err==ortho64,failures)
    enddo
  end subroutine test_legacy_matches_promoted_inputs

  subroutine test_real64_flux_perturbation(failures)
    integer, intent(inout) :: failures
    real(dp), parameter :: delta=1.0e-9_dp
    real(dp) :: phi(3,2),vol(3),sigma(2),rec_err,ortho_err
    real :: basis(3,2),coeff(2,2),rounded_phi(3,2)
    integer :: nmode
    phi=1.0_dp
    phi(:,2)=[1.0_dp+delta,1.0_dp-delta,1.0_dp]
    vol=1.0_dp
    rounded_phi=real(phi)
    call assert_true('flux perturbation is below REAL input resolution', &
      all(rounded_phi==1.0),failures)
    call SPOPOD(3,2,rounded_phi,real(vol),0,nmode,basis,coeff,sigma, &
                rec_err,ortho_err,0,1)
    call assert_int('rounded snapshots have one numerical mode',nmode,1,failures)
    call SPOPOD64(3,2,phi,vol,0,nmode,basis,coeff,sigma, &
                  rec_err,ortho_err,0,1)
    call assert_int('REAL64 keeps the distinct snapshot mode',nmode,2,failures)
    call assert_true('REAL64 singular value retains sub-REAL flux change', &
      sigma(2)>0.1_dp*delta .and. sigma(2)<delta,failures)
    call assert_true('original REAL coefficient output keeps the small mode', &
      maxval(abs(coeff(2,:)))>0.0,failures)
  end subroutine test_real64_flux_perturbation

  subroutine test_real64_volume_perturbation(failures)
    integer, intent(inout) :: failures
    real(dp), parameter :: delta=1.0e-9_dp
    real(dp) :: phi(3,1),vol(3),weight(3),shape(3),expected
    real(dp) :: sigma(1),rounded_sigma(1),rec_err,ortho_err
    real :: basis(3,1),coeff(1,1)
    integer :: nmode
    phi(:,1)=[1.0_dp,2.0_dp,4.0_dp]
    vol=[1.0_dp+delta,1.0_dp,1.0_dp]
    call assert_true('volume perturbation is below REAL input resolution', &
      all(real(vol)==1.0),failures)
    call SPOPOD(3,1,real(phi),real(vol),0,nmode,basis,coeff, &
                rounded_sigma,rec_err,ortho_err,0,1)
    call SPOPOD64(3,1,phi,vol,0,nmode,basis,coeff,sigma, &
                  rec_err,ortho_err,0,1)
    weight=vol/sum(vol)
    shape=phi(:,1)/sum(weight*phi(:,1))
    expected=sqrt(sum(weight*shape*shape))
    call assert_close('REAL64 volume uses original weighted SVD formula', &
      sigma(1),expected,20.0_dp*epsilon(1.0_dp),failures)
    call assert_true('REAL64 singular value retains sub-REAL volume change', &
      abs(sigma(1)-rounded_sigma(1))>1.0e-11_dp,failures)
  end subroutine test_real64_volume_perturbation

  subroutine assert_true(label,condition,failures)
    character(*), intent(in) :: label
    logical, intent(in) :: condition
    integer, intent(inout) :: failures
    if (condition) then
      write(*,'(a)') 'PASS: '//label
    else
      write(error_unit,'(a)') 'FAIL: '//label
      failures=failures+1
    endif
  end subroutine assert_true

  subroutine assert_int(label,actual,expected,failures)
    character(*), intent(in) :: label
    integer, intent(in) :: actual,expected
    integer, intent(inout) :: failures
    call assert_true(label,actual == expected,failures)
  end subroutine assert_int

  subroutine assert_close(label,actual,expected,tolerance,failures)
    character(*), intent(in) :: label
    real(dp), intent(in) :: actual,expected,tolerance
    integer, intent(inout) :: failures
    call assert_true(label,abs(actual-expected) <= tolerance,failures)
  end subroutine assert_close
end program test_spopod

subroutine XABORT(message)
  character(*), intent(in) :: message
  write(*,'(a)') 'XABORT: '//message
  error stop 2
end subroutine XABORT
