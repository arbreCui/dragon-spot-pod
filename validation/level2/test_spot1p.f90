program test_spot1p
  use, intrinsic :: iso_fortran_env, only : error_unit
  implicit none
  integer, parameter :: dp=kind(1.0d0)
  integer, parameter :: nr=2,nz=2,nm=2,nq=4,nl=1
  integer :: failures,i
  integer :: mat(nz,nr),mat_one(nz,1),mat1d(nz),ncode(2)
  real :: dz(nz),total(0:nm),scatter(0:nm,nl),basis(nr,nr),vol(nr)
  real :: zcode(2),mu(nq),weight(nq),pl(nl,nq)
  real :: source(1,nl,nz,nr),flux(1,nl,nz,nr),current(nz+1,nr),xnei(nq,nr)
  real :: source_one(1,nl,nz,1),flux_one(1,nl,nz,1)
  real :: current_one(nz+1,1),xnei_one(nq,1),basis_one(1,1),vol_one(1)
  real :: radial(nr,1),radial_one(1,1)
  real(dp) :: max_error

  failures=0
  dz=[1.2,0.8]
  total=[0.0,1.10,0.82]
  scatter=0.0
  scatter(1,1)=0.23
  scatter(2,1)=0.11
  mat(:,1)=1
  mat(:,2)=2
  mat1d=1
  ncode=[1,1]
  zcode=0.0
  mu=[0.86113631,0.33998104,-0.33998104,-0.86113631]
  weight=[0.34785485,0.65214515,0.65214515,0.34785485]
  pl=1.0
  vol=1.0
  radial(:,1)=[0.08,-0.03]

  ! This rotated full basis forces non-diagonal projected material matrices.
  ! With full radial rank it must still reproduce two independent channels.
  basis(:,1)=[1.0,1.0]
  basis(:,2)=[1.0,-1.0]
  source=0.0
  source(1,1,1,1)=1.0
  source(1,1,2,1)=0.7
  source(1,1,1,2)=0.4
  source(1,1,2,2)=1.3

  call SPOT1P(nr,nz,1,nm,1,nr,1,nq,nl,.false.,mat1d,dz,mat,total,scatter, &
               basis,vol,radial,ncode,zcode,source,mu,weight,pl, &
               flux,current,xnei)

  basis_one=1.0
  vol_one=1.0
  max_error=0.0d0
  do i=1,nr
    mat_one(:,1)=mat(:,i)
    radial_one(1,1)=radial(i,1)
    source_one(:,:,:,1)=source(:,:,:,i)
    call SPOT1P(1,nz,1,nm,1,1,1,nq,nl,.false.,mat1d,dz,mat_one, &
                 total,scatter,basis_one,vol_one,radial_one,ncode,zcode, &
                 source_one,mu,weight,pl,flux_one,current_one,xnei_one)
    max_error=max(max_error,maxval(abs(real(flux(:,:,:,i),dp)- &
                                       real(flux_one(:,:,:,1),dp))))
    max_error=max(max_error,maxval(abs(real(current(:,i),dp)- &
                                       real(current_one(:,1),dp))))
    max_error=max(max_error,maxval(abs(real(xnei(:,i),dp)- &
                                       real(xnei_one(:,1),dp))))
  enddo
  call assert_true('full modal rank equals independent radial channels', &
                   max_error < 2.0e-5_dp,failures)
  call assert_true('manufactured scalar flux remains positive', &
                   minval(flux(1,1,:,:)) > 0.0,failures)

  if (failures /= 0) then
    write(error_unit,'(a,i0)') 'LEVEL2 FAILURES: ',failures
    error stop 1
  endif
  write(*,'(a,1p,e11.4)') 'LEVEL2 PASS: full-rank modal equivalence; max error=',max_error

contains
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
end program test_spot1p

subroutine XABORT(message)
  character(*), intent(in) :: message
  write(*,'(a)') 'XABORT: '//message
  error stop 2
end subroutine XABORT
