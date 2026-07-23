!-----------------------------------------------------------------------
!
! Purpose:
!   Solve the coupled one-dimensional SN equations in a radial POD
!   trial space and reconstruct the physical regional flux.
!
! The radial expansion for one energy group is
!
!        psi_i(z,mu) = sum_a B_i^a A_a(z,mu),
!
! where B is volume-orthonormal.  Material operators and sources are
! projected with the same volume inner product.  RANK therefore equals
! the number of axial modal unknowns; POD is not an input filter.
!
! This first clean implementation intentionally supports the constant
! diamond spatial approximation only.
!
!-----------------------------------------------------------------------
subroutine SPOT1P(nreg2d,nfloor,ielem,nmat,nsnap,nmode,ischm,npq,nsct, &
                  lfixup,mat1d,vol1d,mat,total,sgas,basis,vol2d, &
                  radial2d,ncode,zcode,qext,du,w,pl,flux,cour,xnei)
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none
  integer, parameter :: dp=kind(1.0d0)

  integer, intent(in) :: nreg2d,nfloor,ielem,nmat,nsnap,nmode,ischm,npq,nsct
  integer, intent(in) :: mat1d(nfloor),mat(nfloor,nreg2d),ncode(2)
  real, intent(in) :: vol1d(nfloor),total(0:nmat),sgas(0:nmat,nsct)
  real, intent(in) :: basis(nreg2d,nmode),vol2d(nreg2d),zcode(2)
  real, intent(in) :: radial2d(nreg2d,nsnap)
  real, intent(in) :: qext(ielem,nsct,nfloor,nreg2d)
  real, intent(in) :: du(npq),w(npq),pl(nsct,npq)
  real, intent(out) :: flux(ielem,nsct,nfloor,nreg2d)
  real, intent(out) :: cour(nfloor+1,nreg2d),xnei(npq,nreg2d)
  logical, intent(in) :: lfixup

  integer :: i,a,b,n,m,l,ifloor,iface,ibm,isnap,ico,row,opp,half
  integer :: npositive,nnegative,npair
  integer :: nstate,ier
  double precision :: vtot,wi,albedo_left,albedo_right
  double precision, allocatable :: weight(:),total_m(:,:,:)
  double precision, allocatable :: radial_m(:,:,:)
  double precision, allocatable :: scat_m(:,:,:,:),source_m(:,:,:)
  double precision, allocatable :: mn(:,:),dn(:,:),aa(:),bb(:,:)
  double precision, allocatable :: shoot(:,:),face(:,:,:),cell(:,:,:)
  double precision, allocatable :: modal_flux(:,:,:),modal_cour(:,:)
  integer, allocatable :: opposite(:)
  logical :: translation

  if (ielem /= 1 .or. ischm /= 1) &
    call XABORT('SPOT1P: ONLY CONSTANT DIAMOND SPATIAL APPROXIMATION IS SUPPORTED.')
  if (lfixup) &
    call XABORT('SPOT1P: NEGATIVE-FLUX FIXUP IS NOT IMPLEMENTED.')
  if (nmode <= 0 .or. nmode > nreg2d) &
    call XABORT('SPOT1P: INVALID POD MODE COUNT.')
  if (mod(npq,2) /= 0 .or. npq <= 0) &
    call XABORT('SPOT1P: AN EVEN SN ORDER IS REQUIRED.')
  if (any(vol1d <= 0.0) .or. any(vol2d <= 0.0)) &
    call XABORT('SPOT1P: NONPOSITIVE VOLUME.')
  if (any(.not.ieee_is_finite(du)) .or. &
      any(.not.ieee_is_finite(w)) .or. any(w <= 0.0)) &
    call XABORT('SPOT1P: INVALID SN QUADRATURE DATA.')

  half=npq/2
  npositive=count(du > 0.0)
  nnegative=count(du < 0.0)
  if (npositive /= half .or. nnegative /= half) &
    call XABORT('SPOT1P: INVALID SYMMETRIC SN DIRECTIONS.')
  allocate(opposite(npq))
  opposite=0
  do n=1,npq
    npair=0
    do m=1,npq
      ! Unary negation is exact for a finite stored IEEE real.  Compare
      ! representations so the pairing contains no numerical tolerance.
      if (transfer(du(m),0) == transfer(-du(n),0)) then
        npair=npair+1
        opposite(n)=m
      endif
    enddo
    if (npair /= 1) &
      call XABORT('SPOT1P: SN DIRECTION HAS NO UNIQUE EXACT OPPOSITE.')
  enddo
  do n=1,npq
    if (opposite(opposite(n)) /= n) &
      call XABORT('SPOT1P: SN OPPOSITE MAP IS NOT AN INVOLUTION.')
    if (count(opposite == n) /= 1) &
      call XABORT('SPOT1P: SN OPPOSITE MAP IS NOT ONE-TO-ONE.')
    if (transfer(w(opposite(n)),0) /= transfer(w(n),0)) &
      call XABORT('SPOT1P: OPPOSITE SN WEIGHTS DIFFER.')
  enddo
  translation=(ncode(1) == 4 .or. ncode(2) == 4)
  if (translation .and. (ncode(1) /= 4 .or. ncode(2) /= 4)) &
    call XABORT('SPOT1P: TRANSLATION BOUNDARIES MUST BE PAIRED.')
  if (.not.translation) then
    if (.not.(ncode(1) == 1 .or. ncode(1) == 2 .or. ncode(1) == 7)) &
      call XABORT('SPOT1P: UNSUPPORTED LEFT BOUNDARY CONDITION.')
    if (.not.(ncode(2) == 1 .or. ncode(2) == 2 .or. ncode(2) == 7)) &
      call XABORT('SPOT1P: UNSUPPORTED RIGHT BOUNDARY CONDITION.')
  endif

  allocate(weight(nreg2d),total_m(nmode,nmode,nfloor))
  allocate(radial_m(nmode,nmode,nfloor))
  allocate(scat_m(nmode,nmode,nsct,nfloor))
  allocate(source_m(nsct,nfloor,nmode),mn(npq,nsct),dn(nsct,npq))
  vtot=sum(real(vol2d,dp))
  weight=real(vol2d,dp)/vtot
  total_m=0.0d0
  radial_m=0.0d0
  scat_m=0.0d0
  source_m=0.0d0

  do ifloor=1,nfloor
    isnap=mat1d(ifloor)
    if (isnap < 1 .or. isnap > nsnap) &
      call XABORT('SPOT1P: INVALID SNAPSHOT INDEX.')
    do i=1,nreg2d
      ibm=mat(ifloor,i)
      if (ibm == 0) cycle
      if (ibm < 0 .or. ibm > nmat) &
        call XABORT('SPOT1P: MATERIAL INDEX OVERFLOW.')
      wi=weight(i)
      do a=1,nmode
        do b=1,nmode
          total_m(a,b,ifloor)=total_m(a,b,ifloor)+wi* &
            real(basis(i,a),dp)*real(total(ibm),dp)*real(basis(i,b),dp)
          radial_m(a,b,ifloor)=radial_m(a,b,ifloor)+wi* &
            real(basis(i,a),dp)*real(radial2d(i,isnap),dp)* &
            real(basis(i,b),dp)
          do l=1,nsct
            scat_m(a,b,l,ifloor)=scat_m(a,b,l,ifloor)+wi* &
              real(basis(i,a),dp)*real(sgas(ibm,l),dp)*real(basis(i,b),dp)
          enddo
        enddo
        do l=1,nsct
          source_m(l,ifloor,a)=source_m(l,ifloor,a)+wi* &
            real(basis(i,a),dp)*real(qext(1,l,ifloor,i),dp)
        enddo
      enddo
    enddo
  enddo

  do n=1,npq
    do l=1,nsct
      mn(n,l)=0.5d0*real(2*l-1,dp)*real(pl(l,n),dp)
      dn(l,n)=real(w(n),dp)*real(pl(l,n),dp)
    enddo
  enddo

  nstate=nmode*npq
  allocate(face(npq,nmode,nfloor+1),cell(npq,nmode,nfloor))
  allocate(modal_flux(nsct,nfloor,nmode),modal_cour(nfloor+1,nmode))

  if (translation) then
    albedo_left=real(zcode(1),dp)
    albedo_right=real(zcode(2),dp)
  else
    albedo_left=merge(1.0d0,real(zcode(1),dp),ncode(1) == 2)
    albedo_right=merge(1.0d0,real(zcode(2),dp),ncode(2) == 2)
    if (ncode(1) == 7) albedo_left=0.0d0
    if (ncode(2) == 7) albedo_right=0.0d0
  endif

  if (.not.translation) then
    ! Solve the two-point boundary-value problem directly.  The block
    ! tridiagonal system is algebraically identical to diamond differencing
    ! but remains stable when the axial mesh is refined.
    call boundary_solve(face,cell,albedo_left,albedo_right)
  else
    ! Translation boundaries couple the two end faces.  Retain the compact
    ! shooting construction for this uncommon cyclic case.
    allocate(aa(nstate),bb(nstate,nstate),shoot(nstate,nstate+1))
    face=0.0d0
    call sweep(face,cell)
    do a=1,nmode
      do n=1,npq
        aa(index_of(a,n))=face(n,a,nfloor+1)
      enddo
    enddo

    do ico=1,nstate
      face=0.0d0
      a=(ico-1)/npq+1
      n=mod(ico-1,npq)+1
      face(n,a,1)=1.0d0
      call sweep(face,cell)
      do b=1,nmode
        do m=1,npq
          row=index_of(b,m)
          bb(row,ico)=face(m,b,nfloor+1)-aa(row)
        enddo
      enddo
    enddo

    shoot=0.0d0
    do a=1,nmode
      do n=1,npq
        row=index_of(a,n)
        opp=opposite(n)
        if (du(n) > 0.0) then
          shoot(row,:nstate)=-albedo_left*bb(row,:)
          shoot(row,row)=shoot(row,row)+1.0d0
          shoot(row,nstate+1)=albedo_left*aa(row)
        else
          shoot(row,:nstate)=bb(row,:)
          shoot(row,row)=shoot(row,row)-albedo_right
          shoot(row,nstate+1)=-aa(row)
        endif
      enddo
    enddo

    call ALSBD(nstate,1,shoot,ier,nstate)
    if (ier /= 0) call XABORT('SPOT1P: SINGULAR MODAL BOUNDARY SYSTEM.')
    face=0.0d0
    do a=1,nmode
      do n=1,npq
        face(n,a,1)=shoot(index_of(a,n),nstate+1)
      enddo
    enddo
    call sweep(face,cell)
  endif

  modal_flux=0.0d0
  do a=1,nmode
    do ifloor=1,nfloor
      do l=1,nsct
        do n=1,npq
          modal_flux(l,ifloor,a)=modal_flux(l,ifloor,a)+dn(l,n)*cell(n,a,ifloor)
        enddo
      enddo
    enddo
  enddo
  modal_cour=0.0d0
  do a=1,nmode
    do iface=1,nfloor+1
      do n=1,npq
        modal_cour(iface,a)=modal_cour(iface,a)+real(w(n),dp)* &
          real(du(n),dp)*face(n,a,iface)
      enddo
    enddo
  enddo

  flux=0.0
  cour=0.0
  xnei=0.0
  do i=1,nreg2d
    do a=1,nmode
      do ifloor=1,nfloor
        do l=1,nsct
          flux(1,l,ifloor,i)=flux(1,l,ifloor,i)+ &
            basis(i,a)*real(modal_flux(l,ifloor,a))
        enddo
      enddo
      do iface=1,nfloor+1
        cour(iface,i)=cour(iface,i)+basis(i,a)*real(modal_cour(iface,a))
      enddo
      do n=1,npq
        xnei(n,i)=xnei(n,i)+basis(i,a)*real(face(n,a,1))
      enddo
    enddo
  enddo
  if (any(.not.ieee_is_finite(flux)) .or. &
      any(.not.ieee_is_finite(cour)) .or. &
      any(.not.ieee_is_finite(xnei))) &
    call XABORT('SPOT1P: NON-FINITE RECONSTRUCTED SOLUTION.')

  if (allocated(shoot)) deallocate(shoot,bb,aa)
  deallocate(opposite,modal_cour,modal_flux,cell,face)
  deallocate(dn,mn,source_m,scat_m,radial_m,total_m,weight)
  return

contains

  integer function index_of(imode,idir)
    integer, intent(in) :: imode,idir
    index_of=(imode-1)*npq+idir
  end function index_of

  subroutine boundary_solve(face_flux,cell_flux,left_albedo,right_albedo)
    double precision, intent(out) :: face_flux(npq,nmode,nfloor+1)
    double precision, intent(out) :: cell_flux(npq,nmode,nfloor)
    double precision, intent(in) :: left_albedo,right_albedo
    double precision, allocatable :: lower(:,:,:),diagonal(:,:,:)
    double precision, allocatable :: upper(:,:,:),right_hand(:,:)
    double precision, allocatable :: cprime(:,:,:),dprime(:,:)
    double precision, allocatable :: solution(:,:),augmented(:,:)
    double precision :: h,kvalue,svalue
    integer :: block,iz,ia,ib,in,jn,il,ir,ic,info

    allocate(lower(nstate,nstate,nfloor+1))
    allocate(diagonal(nstate,nstate,nfloor+1))
    allocate(upper(nstate,nstate,nfloor+1))
    allocate(right_hand(nstate,nfloor+1))
    allocate(cprime(nstate,nstate,nfloor+1))
    allocate(dprime(nstate,nfloor+1),solution(nstate,nfloor+1))
    allocate(augmented(nstate,2*nstate+1))
    lower=0.0d0
    diagonal=0.0d0
    upper=0.0d0
    right_hand=0.0d0

    do block=0,nfloor
      do ia=1,nmode
        do in=1,npq
          ir=index_of(ia,in)
          if (du(in) > 0.0) then
            if (block == 0) then
              diagonal(ir,ir,1)=1.0d0
              diagonal(ir,index_of(ia,opposite(in)),1)=-left_albedo
              cycle
            endif
            iz=block
          else
            if (block == nfloor) then
              diagonal(ir,ir,nfloor+1)=1.0d0
              diagonal(ir,index_of(ia,opposite(in)),nfloor+1)= &
                -right_albedo
              cycle
            endif
            iz=block+1
          endif

          h=real(vol1d(iz),dp)
          svalue=0.0d0
          do il=1,nsct
            svalue=svalue+mn(in,il)*source_m(il,iz,ia)
          enddo
          right_hand(ir,block+1)=h*svalue

          do ib=1,nmode
            do jn=1,npq
              ic=index_of(ib,jn)
              kvalue=0.0d0
              if (in == jn) kvalue=kvalue+total_m(ia,ib,iz)
              do il=1,nsct
                kvalue=kvalue-mn(in,il)*scat_m(ia,ib,il,iz)*dn(il,jn)
              enddo
              kvalue=kvalue+mn(in,1)*radial_m(ia,ib,iz)*dn(1,jn)
              if (du(in) > 0.0) then
                lower(ir,ic,block+1)=0.5d0*h*kvalue
                diagonal(ir,ic,block+1)=0.5d0*h*kvalue
              else
                diagonal(ir,ic,block+1)=0.5d0*h*kvalue
                upper(ir,ic,block+1)=0.5d0*h*kvalue
              endif
            enddo
          enddo
          if (du(in) > 0.0) then
            lower(ir,ir,block+1)=lower(ir,ir,block+1)-real(du(in),dp)
            diagonal(ir,ir,block+1)=diagonal(ir,ir,block+1)+real(du(in),dp)
          else
            diagonal(ir,ir,block+1)=diagonal(ir,ir,block+1)-real(du(in),dp)
            upper(ir,ir,block+1)=upper(ir,ir,block+1)+real(du(in),dp)
          endif
        enddo
      enddo
    enddo

    augmented=0.0d0
    augmented(:,:nstate)=diagonal(:,:,1)
    augmented(:,nstate+1:2*nstate)=upper(:,:,1)
    augmented(:,2*nstate+1)=right_hand(:,1)
    call ALSBD(nstate,nstate+1,augmented,info,nstate)
    if (info /= 0) call XABORT('SPOT1P: SINGULAR FIRST AXIAL BLOCK.')
    cprime(:,:,1)=augmented(:,nstate+1:2*nstate)
    dprime(:,1)=augmented(:,2*nstate+1)

    do block=2,nfloor+1
      augmented=0.0d0
      augmented(:,:nstate)=diagonal(:,:,block)- &
        matmul(lower(:,:,block),cprime(:,:,block-1))
      augmented(:,nstate+1:2*nstate)=upper(:,:,block)
      augmented(:,2*nstate+1)=right_hand(:,block)- &
        matmul(lower(:,:,block),dprime(:,block-1))
      call ALSBD(nstate,nstate+1,augmented,info,nstate)
      if (info /= 0) call XABORT('SPOT1P: SINGULAR AXIAL SCHUR BLOCK.')
      cprime(:,:,block)=augmented(:,nstate+1:2*nstate)
      dprime(:,block)=augmented(:,2*nstate+1)
    enddo

    solution(:,nfloor+1)=dprime(:,nfloor+1)
    do block=nfloor,1,-1
      solution(:,block)=dprime(:,block)- &
        matmul(cprime(:,:,block),solution(:,block+1))
    enddo
    do block=1,nfloor+1
      do ia=1,nmode
        do in=1,npq
          face_flux(in,ia,block)=solution(index_of(ia,in),block)
        enddo
      enddo
    enddo
    do iz=1,nfloor
      cell_flux(:,:,iz)=0.5d0*(face_flux(:,:,iz)+face_flux(:,:,iz+1))
    enddo

    deallocate(augmented,solution,dprime,cprime,right_hand)
    deallocate(upper,diagonal,lower)
  end subroutine boundary_solve

  subroutine sweep(face_flux,cell_flux)
    double precision, intent(inout) :: face_flux(npq,nmode,nfloor+1)
    double precision, intent(out) :: cell_flux(npq,nmode,nfloor)
    double precision, allocatable :: amat(:,:)
    double precision :: h,rhs
    integer :: iz,ia,ib,in,jn,il,ir,ic,info

    allocate(amat(nstate,nstate+1))
    cell_flux=0.0d0
    do iz=1,nfloor
      h=real(vol1d(iz),dp)
      amat=0.0d0
      do ia=1,nmode
        do in=1,npq
          ir=index_of(ia,in)
          do ib=1,nmode
            do jn=1,npq
              ic=index_of(ib,jn)
              if (in == jn) amat(ir,ic)=amat(ir,ic)+h*total_m(ia,ib,iz)
              do il=1,nsct
                amat(ir,ic)=amat(ir,ic)-h*mn(in,il)* &
                  scat_m(ia,ib,il,iz)*dn(il,jn)
              enddo
              amat(ir,ic)=amat(ir,ic)+h*mn(in,1)* &
                radial_m(ia,ib,iz)*dn(1,jn)
            enddo
          enddo
          amat(ir,ir)=amat(ir,ir)+2.0d0*real(du(in),dp)
          rhs=2.0d0*real(du(in),dp)*face_flux(in,ia,iz)
          do il=1,nsct
            rhs=rhs+h*mn(in,il)*source_m(il,iz,ia)
          enddo
          amat(ir,nstate+1)=rhs
        enddo
      enddo
      call ALSBD(nstate,1,amat,info,nstate)
      if (info /= 0) call XABORT('SPOT1P: SINGULAR LOCAL MODAL SYSTEM.')
      do ia=1,nmode
        do in=1,npq
          ir=index_of(ia,in)
          cell_flux(in,ia,iz)=amat(ir,nstate+1)
          face_flux(in,ia,iz+1)=2.0d0*cell_flux(in,ia,iz)- &
            face_flux(in,ia,iz)
        enddo
      enddo
    enddo
    deallocate(amat)
  end subroutine sweep

end subroutine SPOT1P
