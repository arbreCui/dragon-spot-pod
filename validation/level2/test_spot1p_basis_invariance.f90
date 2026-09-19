program test_spot1p_basis_invariance
  use, intrinsic :: iso_fortran_env, only : error_unit,real64
  implicit none
  integer, parameter :: dp=real64
  integer, parameter :: nr=2,nz=2,nm=2,nq=4,nl=1
  integer :: failures
  integer :: mat(nz,nr),mat1d(nz),ncode(2)
  real :: dz(nz),total(0:nm),scatter(0:nm,nl),vol(nr)
  real :: basis_ref(nr,nr),basis_changed(nr,nr),basis_physical(nr,nr)
  real :: transform(nr,nr)
  real :: zcode(2),mu(nq),sn_weight(nq),pl(nl,nq)
  real :: source(1,nl,nz,nr),radial(nr,1)
  real :: flux_ref(1,nl,nz,nr),flux_changed(1,nl,nz,nr)
  real :: flux_physical(1,nl,nz,nr)
  real :: current_ref(nz+1,nr),current_changed(nz+1,nr)
  real :: current_physical(nz+1,nr)
  real :: xnei_ref(nq,nr),xnei_changed(nq,nr)
  real :: xnei_physical(nq,nr)
  real(dp) :: source64(1,nl,nz,nr),radial64(nr,1)
  real(dp) :: flux64_ref(1,nl,nz,nr),flux64_changed(1,nl,nz,nr)
  real(dp) :: flux64_physical(1,nl,nz,nr)
  real(dp) :: current64_ref(nz+1,nr),current64_changed(nz+1,nr)
  real(dp) :: current64_physical(nz+1,nr)
  real(dp) :: xnei64_ref(nq,nr),xnei64_changed(nq,nr)
  real(dp) :: xnei64_physical(nq,nr)
  real(dp) :: err_boundary,err_boundary64,err_sweep,err_sweep64

  failures=0
  dz=[1.2,0.8]
  total=[0.0,1.10,0.82]
  scatter=0.0
  scatter(1,1)=0.23
  scatter(2,1)=0.11
  mat(:,1)=1
  mat(:,2)=2
  mat1d=1
  mu=[0.86113631,0.33998104,-0.33998104,-0.86113631]
  sn_weight=[0.34785485,0.65214515,0.65214515,0.34785485]
  pl=1.0
  vol=[1.0,3.0]
  radial(:,1)=[0.08,-0.03]
  source=0.0
  source(1,1,1,1)=1.0
  source(1,1,2,1)=0.7
  source(1,1,1,2)=0.4
  source(1,1,2,2)=1.3
  radial64=real(radial,dp)
  source64=real(source,dp)

  ! B_physical is the exact diagonal coordinate form used by SPOPHYS.  Mixing
  ! it with an orthogonal matrix gives a dense volume-orthonormal reference;
  ! the final nonsingular transform also scales and nonorthogonally mixes it.
  basis_physical=0.0
  basis_physical(1,1)=1.0/sqrt(vol(1)/sum(vol))
  basis_physical(2,2)=1.0/sqrt(vol(2)/sum(vol))
  basis_ref(1,:)=[basis_physical(1,1)/sqrt(2.0), &
                  basis_physical(1,1)/sqrt(2.0)]
  basis_ref(2,:)=[basis_physical(2,2)/sqrt(2.0), &
                 -basis_physical(2,2)/sqrt(2.0)]
  transform=reshape([2.0,-0.25,0.5,0.75],[nr,nr])
  basis_changed=matmul(basis_ref,transform)

  ncode=[1,1]
  zcode=0.0
  call SPOT1P(nr,nz,1,nm,1,nr,1,nq,nl,.false.,mat1d,dz,mat,total,scatter, &
               basis_ref,vol,radial,ncode,zcode,source,mu,sn_weight,pl, &
               flux_ref,current_ref,xnei_ref)
  call SPOT1P(nr,nz,1,nm,1,nr,1,nq,nl,.false.,mat1d,dz,mat,total,scatter, &
               basis_changed,vol,radial,ncode,zcode,source,mu,sn_weight,pl, &
               flux_changed,current_changed,xnei_changed)
  call SPOT1P(nr,nz,1,nm,1,nr,1,nq,nl,.false.,mat1d,dz,mat,total,scatter, &
               basis_physical,vol,radial,ncode,zcode,source,mu,sn_weight,pl, &
               flux_physical,current_physical,xnei_physical)
  err_boundary=maxval(abs(real(flux_changed,dp)-real(flux_ref,dp)))
  err_boundary=max(err_boundary, &
    maxval(abs(real(flux_physical,dp)-real(flux_ref,dp))))
  err_boundary=max(err_boundary, &
    maxval(abs(real(current_changed,dp)-real(current_ref,dp))))
  err_boundary=max(err_boundary, &
    maxval(abs(real(xnei_changed,dp)-real(xnei_ref,dp))))
  err_boundary=max(err_boundary, &
    maxval(abs(real(current_physical,dp)-real(current_ref,dp))))
  err_boundary=max(err_boundary, &
    maxval(abs(real(xnei_physical,dp)-real(xnei_ref,dp))))
  call assert_true('SPOT1P boundary solve is basis-transform invariant', &
                   err_boundary < 2.0e-5_dp,failures)

  call SPOT1P64(1,nr,nz,1,nm,1,nr,1,nq,nl,.false.,mat1d,dz,mat,total,scatter, &
                 basis_ref,vol,radial64,ncode,zcode,source64,mu,sn_weight,pl, &
                 flux64_ref,current64_ref,xnei64_ref)
  call SPOT1P64(1,nr,nz,1,nm,1,nr,1,nq,nl,.false.,mat1d,dz,mat,total,scatter, &
                 basis_changed,vol,radial64,ncode,zcode,source64,mu, &
                 sn_weight,pl,flux64_changed,current64_changed,xnei64_changed)
  call SPOT1P64(1,nr,nz,1,nm,1,nr,1,nq,nl,.false.,mat1d,dz,mat,total,scatter, &
                 basis_physical,vol,radial64,ncode,zcode,source64,mu, &
                 sn_weight,pl,flux64_physical,current64_physical, &
                 xnei64_physical)
  err_boundary64=maxval(abs(flux64_changed-flux64_ref))
  err_boundary64=max(err_boundary64,maxval(abs(flux64_physical-flux64_ref)))
  err_boundary64=max(err_boundary64,maxval(abs(current64_changed-current64_ref)))
  err_boundary64=max(err_boundary64,maxval(abs(xnei64_changed-xnei64_ref)))
  err_boundary64=max(err_boundary64, &
    maxval(abs(current64_physical-current64_ref)))
  err_boundary64=max(err_boundary64,maxval(abs(xnei64_physical-xnei64_ref)))
  call assert_true('SPOT1P64 boundary solve is basis-transform invariant', &
                   err_boundary64 < 5.0e-11_dp,failures)

  ! Paired translation boundaries exercise the local sweep matrix and its
  ! incoming-face right-hand side rather than the block boundary solver.
  ncode=[4,4]
  zcode=1.0
  call SPOT1P(nr,nz,1,nm,1,nr,1,nq,nl,.false.,mat1d,dz,mat,total,scatter, &
               basis_ref,vol,radial,ncode,zcode,source,mu,sn_weight,pl, &
               flux_ref,current_ref,xnei_ref)
  call SPOT1P(nr,nz,1,nm,1,nr,1,nq,nl,.false.,mat1d,dz,mat,total,scatter, &
               basis_changed,vol,radial,ncode,zcode,source,mu,sn_weight,pl, &
               flux_changed,current_changed,xnei_changed)
  call SPOT1P(nr,nz,1,nm,1,nr,1,nq,nl,.false.,mat1d,dz,mat,total,scatter, &
               basis_physical,vol,radial,ncode,zcode,source,mu,sn_weight,pl, &
               flux_physical,current_physical,xnei_physical)
  err_sweep=maxval(abs(real(flux_changed,dp)-real(flux_ref,dp)))
  err_sweep=max(err_sweep, &
    maxval(abs(real(flux_physical,dp)-real(flux_ref,dp))))
  err_sweep=max(err_sweep, &
    maxval(abs(real(current_changed,dp)-real(current_ref,dp))))
  err_sweep=max(err_sweep, &
    maxval(abs(real(xnei_changed,dp)-real(xnei_ref,dp))))
  err_sweep=max(err_sweep, &
    maxval(abs(real(current_physical,dp)-real(current_ref,dp))))
  err_sweep=max(err_sweep, &
    maxval(abs(real(xnei_physical,dp)-real(xnei_ref,dp))))
  call assert_true('SPOT1P sweep is basis-transform invariant', &
                   err_sweep < 2.0e-5_dp,failures)

  call SPOT1P64(1,nr,nz,1,nm,1,nr,1,nq,nl,.false.,mat1d,dz,mat,total,scatter, &
                 basis_ref,vol,radial64,ncode,zcode,source64,mu,sn_weight,pl, &
                 flux64_ref,current64_ref,xnei64_ref)
  call SPOT1P64(1,nr,nz,1,nm,1,nr,1,nq,nl,.false.,mat1d,dz,mat,total,scatter, &
                 basis_changed,vol,radial64,ncode,zcode,source64,mu, &
                 sn_weight,pl,flux64_changed,current64_changed,xnei64_changed)
  call SPOT1P64(1,nr,nz,1,nm,1,nr,1,nq,nl,.false.,mat1d,dz,mat,total,scatter, &
                 basis_physical,vol,radial64,ncode,zcode,source64,mu, &
                 sn_weight,pl,flux64_physical,current64_physical, &
                 xnei64_physical)
  err_sweep64=maxval(abs(flux64_changed-flux64_ref))
  err_sweep64=max(err_sweep64,maxval(abs(flux64_physical-flux64_ref)))
  err_sweep64=max(err_sweep64,maxval(abs(current64_changed-current64_ref)))
  err_sweep64=max(err_sweep64,maxval(abs(xnei64_changed-xnei64_ref)))
  err_sweep64=max(err_sweep64,maxval(abs(current64_physical-current64_ref)))
  err_sweep64=max(err_sweep64,maxval(abs(xnei64_physical-xnei64_ref)))
  call assert_true('SPOT1P64 sweep is basis-transform invariant', &
                   err_sweep64 < 5.0e-11_dp,failures)

  if (failures /= 0) then
    write(error_unit,'(a,i0)') 'LEVEL2 FAILURES: ',failures
    error stop 1
  endif
  write(*,'(a,1p,4e11.3)') 'LEVEL2 PASS: basis errors=', &
    err_boundary,err_boundary64,err_sweep,err_sweep64

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
end program test_spot1p_basis_invariance

subroutine XABORT(message)
  character(*), intent(in) :: message
  write(*,'(a)') 'XABORT: '//message
  error stop 2
end subroutine XABORT
