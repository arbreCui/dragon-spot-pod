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

  call check_angular_moments(2)
  call check_angular_moments(4)

  if (failures /= 0) then
    write(error_unit,'(a,i0)') 'LEVEL2 FAILURES: ',failures
    error stop 1
  endif
  write(*,'(a,1p,4e11.3)') 'LEVEL2 PASS: basis errors=', &
    err_boundary,err_boundary64,err_sweep,err_sweep64

contains
  subroutine check_angular_moments(boundary)
    ! Uniform manufactured angular solution. Reflective ends use an even
    ! polynomial; paired periodic ends also retain a nonzero P1 moment.
    ! Form q_l from the discrete SN collision equation, not by comparison
    ! with another call to the same transport kernel.
    integer, intent(in) :: boundary
    integer :: bc(2),m(2,1),map(2),l,z
    real :: h(2),t(0:1),s(0:1,3),b(1,1),v(1),zb(2),pol(3,nq),d(1,1)
    real :: q(1,3,2,1),f(1,3,2,1),j(3,1),edge(nq,1)
    real(dp) :: q64(1,3,2,1),f64(1,3,2,1),j64(3,1),edge64(nq,1)
    real(dp) :: coefficients(3),angular(nq),moments(3),source_moment(3)
    real(dp) :: e32,e64
    h=[0.5,1.5]
    t=[0.0,1.5]
    s=0.0
    s(1,:)=[0.25,0.125,-0.0625]
    b=1.0
    v=1.0
    d=0.0
    bc=boundary
    zb=1.0
    m=1
    map=1
    pol(1,:)=1.0
    pol(2,:)=mu
    pol(3,:)=0.5*(3.0*mu*mu-1.0)
    coefficients=[1.0_dp,0.0_dp,0.0625_dp]
    if (boundary==4) coefficients(2)=0.125_dp
    angular=matmul(transpose(real(pol,dp)),coefficients)
    do l=1,3
      moments(l)=sum(real(sn_weight,dp)*real(pol(l,:),dp)*angular)
      source_moment(l)=2.0_dp*real(t(1),dp)*coefficients(l)/real(2*l-1,dp) &
        -real(s(1,l),dp)*moments(l)
    enddo
    do z=1,2
      q64(1,:,z,1)=source_moment
    enddo
    q=real(q64)
    call SPOT1P(1,2,1,1,1,1,1,nq,3,.false.,map,h,m,t,s,b,v,d,bc,zb, &
      q,mu,sn_weight,pol,f,j,edge)
    call SPOT1P64(1,1,2,1,1,1,1,1,nq,3,.false.,map,h,m,t,s,b,v, &
      real(d,dp),bc,zb,q64,mu,sn_weight,pol,f64,j64,edge64)
    e32=0.0_dp
    e64=0.0_dp
    do z=1,2
      e32=max(e32,maxval(abs(real(f(1,:,z,1),dp)-moments)))
      e64=max(e64,maxval(abs(f64(1,:,z,1)-moments)))
    enddo
    call assert_true('SPOT1P manufactured raw P0/P1/P2 moments', &
      e32 <= 64.0_dp*real(epsilon(1.0),dp)*maxval(abs(moments)),failures)
    call assert_true('SPOT1P64 manufactured raw P0/P1/P2 moments', &
      e64 <= 64.0_dp*epsilon(1.0_dp)*maxval(abs(moments)),failures)
    write(*,'(A,I0,A,2ES12.4)') 'ANGULAR MOMENT BC=',boundary,' ERRORS=',e32,e64
  end subroutine check_angular_moments

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
