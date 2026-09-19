program test_b1hom64
  use, intrinsic :: iso_c_binding, only : c_null_ptr
  implicit none
  integer, parameter :: nunk=2,ngro=2,ipas=1,nbm=1,nfissi=1
  integer :: mat(ipas),keyflx(ipas),i
  real :: vol(ipas),dhom(ngro),gamma(ngro),b2(4),leak1d(ngro)
  double precision :: flux(nunk,ngro,2),before(nunk,ngro,2)
  double precision :: expected(nunk,ngro,2),refkef,alam1,scale

  mat=1
  keyflx=1
  vol=1.0
  leak1d=0.0
  refkef=1.0d0
  alam1=0.875d0
  b2=0.0
  flux=reshape([ &
    1.0000000000000002d0,2.0000000000000004d0, &
    3.0000000000000004d0,4.0000000000000009d0, &
    5.0000000000000009d0,6.0000000000000009d0, &
    7.0000000000000009d0,8.0000000000000018d0],shape(flux))
  before=flux

  call B1HOM64(c_null_ptr,.false.,nunk,'B1  ','DIFF',ngro,ipas,nbm, &
               nfissi,vol,mat,keyflx,flux,refkef,0,dhom,gamma,alam1, &
               1,b2,leak1d)
  if (any(flux /= before)) error stop 'DIFF changed the live flux pair'
  if (alam1 /= 0.875d0) error stop 'DIFF changed the incoming eigenvalue'

  b2=0.0
  flux=before
  expected=before
  do i=1,ngro
    expected(:,i,2)=expected(:,i,2)+0.5d0*real(i,8)*0.25d0* &
                      expected(:,i,1)
    scale=real(2*i+1,8)/expected(keyflx(1),i,1)
    expected(:,i,:)=expected(:,i,:)*scale
  enddo

  call B1HOM64(c_null_ptr,.false.,nunk,'B1  ','K   ',ngro,ipas,nbm, &
               nfissi,vol,mat,keyflx,flux,refkef,0,dhom,gamma,alam1, &
               1,b2,leak1d)
  if (maxval(abs(flux-expected)) > 2.0d-14) &
    error stop 'REAL64 B1 update differs from its defining algebra'
  if (all(flux == dble(real(flux)))) &
    error stop 'REAL64 B1 update was quantized to REAL32'
  if (abs(alam1-1.25d0) > 0.0d0) error stop 'eigenvalue was not returned'

  b2=0.0
  flux=before
  expected=before
  dhom=[0.125,0.375]
  gamma=[2.0,3.0]
  do i=1,ngro
    expected(:,i,2)=expected(:,i,2)+0.5d0*real(dhom(i),8)* &
                      expected(:,i,1)
    scale=real(2*i+1,8)/expected(keyflx(1),i,1)
    expected(:,i,:)=expected(:,i,:)*scale
  enddo
  call B1HOM64(c_null_ptr,.false.,nunk,'LKRD','K   ',ngro,ipas,nbm, &
               nfissi,vol,mat,keyflx,flux,refkef,0,dhom,gamma,alam1, &
               1,b2,leak1d)
  if (maxval(abs(flux-expected)) > 2.0d-14) &
    error stop 'LKRD did not use the prescribed leakage coefficients'
  if (any(dhom /= [0.125,0.375])) &
    error stop 'LKRD changed the prescribed leakage coefficients'

  print '(A)', &
    'B1HOM64 PASS: two-layer B1 source correction and normalization stay REAL64.'
end program test_b1hom64

subroutine B1HXS1(ipmacr,ngro,nbm,ian,nfissi,ijj0,ijj1,njj0,njj1,idel)
  use, intrinsic :: iso_c_binding, only : c_ptr
  implicit none
  type(c_ptr), intent(in) :: ipmacr
  integer, intent(in) :: ngro,nbm,ian,nfissi
  integer, intent(out) :: ijj0(ngro),ijj1(ngro),njj0(ngro),njj1(ngro)
  integer, intent(out) :: idel(2)
  ijj0=1
  ijj1=1
  njj0=1
  njj1=1
  idel=1
end subroutine B1HXS1

subroutine B1HXS2(nunkno,ipmacr,ipas,ngro,nbm,ian,nfissi,vol,mat, &
                   keyflx,flux,lfissi,ijj0,ijj1,njj0,njj1,idel,phi, &
                   sa,st,sfnu,xhi,scat0,scat1,ngroin,inorm)
  use, intrinsic :: iso_c_binding, only : c_ptr
  implicit none
  type(c_ptr), intent(in) :: ipmacr
  integer, intent(in) :: nunkno,ipas,ngro,nbm,ian,nfissi,inorm
  integer, intent(in) :: mat(ipas),keyflx(ipas)
  integer, intent(inout) :: ijj0(ngro),ijj1(ngro),njj0(ngro),njj1(ngro)
  integer, intent(inout) :: idel(2)
  integer, intent(out) :: ngroin
  real, intent(in) :: vol(ipas),flux(nunkno,ngro)
  real, intent(out) :: sa(ngro),st(ngro),sfnu(ngro),xhi(ngro)
  real, intent(out) :: scat0(*),scat1(*)
  double precision, intent(out) :: phi(ngro)
  logical, intent(out) :: lfissi
  sa=0.0
  st=1.0
  sfnu=1.0
  xhi=0.5
  scat0(1)=0.0
  scat1(1)=0.0
  phi=1.0d0
  lfissi=.true.
  ngroin=ngro
end subroutine B1HXS2

subroutine B1DIF(option,calculation_type,ngro,st,sfnu,xhi,leak1d, &
                 ijj0,ijj1,njj0,njj1,scat0,scat1,refkef,lfissi,impx, &
                 dhom,gamma,b2,alam1,caet,a2,phi)
  implicit none
  character(len=4), intent(in) :: option,calculation_type
  integer, intent(in) :: ngro,impx
  integer, intent(in) :: ijj0(ngro),ijj1(ngro),njj0(ngro),njj1(ngro)
  real, intent(in) :: st(ngro),sfnu(ngro),xhi(ngro),leak1d(ngro)
  real, intent(in) :: scat0(*),scat1(*)
  double precision, intent(in) :: refkef
  logical, intent(in) :: lfissi
  real, intent(inout) :: dhom(ngro),gamma(ngro)
  double precision, intent(inout) :: b2,phi(ngro)
  double precision, intent(inout) :: alam1
  double precision, intent(out) :: caet,a2
  integer :: i
  do i=1,ngro
    if (option /= 'LKRD') dhom(i)=real(i)*0.25
    gamma(i)=1.0
    phi(i)=real(2*i+1,8)
  enddo
  if (calculation_type /= 'DIFF') b2=b2+0.5d0
  if (calculation_type /= 'DIFF') alam1=1.25d0
  caet=1.0d0
  a2=0.0d0
end subroutine B1DIF

subroutine XABORT(message)
  implicit none
  character(len=*), intent(in) :: message
  write(*,'(A)') trim(message)
  error stop 'unexpected XABORT'
end subroutine XABORT
