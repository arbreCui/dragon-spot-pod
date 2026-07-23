program test_spopod
  use, intrinsic :: iso_fortran_env, only : error_unit
  implicit none
  integer, parameter :: dp=kind(1.0d0)
  integer :: failures

  failures=0
  call test_full_rank_reconstruction(failures)
  call test_rank_is_mode_count(failures)
  call test_identical_snapshots(failures)

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
