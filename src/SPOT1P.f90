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
! where B is any full-rank radial basis.  Material operators, sources,
! and the streaming mass matrix are projected with the same volume inner
! product.  RANK therefore equals
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

  integer :: i,a,b,n,m,l,ifloor,iface,ibm,isnap,half
  integer :: npositive,nnegative,npair
  double precision :: vtot,wi,scale,albedo_left,albedo_right
  double precision, allocatable :: weight(:),mass_m(:,:),total_m(:,:,:)
  double precision, allocatable :: radial_m(:,:,:)
  double precision, allocatable :: scat_m(:,:,:,:),source_m(:,:,:)
  double precision, allocatable :: mn(:,:),dn(:,:)
  double precision, allocatable :: face(:,:,:),cell(:,:,:)
  double precision, allocatable :: modal_flux(:,:,:),modal_cour(:,:)
  integer, allocatable :: opposite(:)
  logical :: translation,diagonal_basis,mode_separable

  if (ielem /= 1 .or. ischm /= 1) &
    call XABORT('SPOT1P: ONLY CONSTANT DIAMOND SPATIAL APPROXIMATION IS SUPPORTED.')
  if (lfixup) &
    call XABORT('SPOT1P: NEGATIVE-FLUX FIXUP IS NOT IMPLEMENTED.')
  if (nmode <= 0 .or. nmode > nreg2d) &
    call XABORT('SPOT1P: INVALID POD MODE COUNT.')
  if (mod(npq,2) /= 0 .or. npq <= 0) &
    call XABORT('SPOT1P: AN EVEN SN ORDER IS REQUIRED.')
  if (any(vol1d <= 0.0) .or. any(vol2d <= 0.0) .or. &
      any(.not.ieee_is_finite(vol1d)) .or. &
      any(.not.ieee_is_finite(vol2d)) .or. &
      any(.not.ieee_is_finite(basis))) &
    call XABORT('SPOT1P: INVALID VOLUME OR BASIS.')
  if (any(.not.ieee_is_finite(total)) .or. &
      any(.not.ieee_is_finite(sgas)) .or. &
      any(.not.ieee_is_finite(radial2d)) .or. &
      any(.not.ieee_is_finite(qext)) .or. &
      any(.not.ieee_is_finite(pl)) .or. &
      any(.not.ieee_is_finite(zcode))) &
    call XABORT('SPOT1P: NON-FINITE OPERATOR OR SOURCE DATA.')
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

  allocate(weight(nreg2d),mass_m(nmode,nmode))
  allocate(total_m(nmode,nmode,nfloor))
  allocate(radial_m(nmode,nmode,nfloor))
  allocate(scat_m(nmode,nmode,nsct,nfloor))
  allocate(source_m(nsct,nfloor,nmode),mn(npq,nsct),dn(nsct,npq))
  vtot=sum(real(vol2d,dp))
  if ((.not.ieee_is_finite(vtot)) .or. vtot <= 0.0d0) &
    call XABORT('SPOT1P: INVALID RADIAL VOLUME SUM.')
  weight=real(vol2d,dp)/vtot
  mass_m=0.0d0
  total_m=0.0d0
  radial_m=0.0d0
  scat_m=0.0d0
  source_m=0.0d0

  ! SPOPHYS produces this exact diagonal coordinate map.  Detect the
  ! algebraic structure from B itself so correctness does not depend on a
  ! provenance flag and avoid forming O(NREG2D*NMODE**2) projections.
  diagonal_basis=nmode == nreg2d
  if (diagonal_basis) then
    do i=1,nreg2d
      do a=1,nmode
        if (i == a) then
          if (basis(i,a) == 0.0) diagonal_basis=.false.
        else
          if (basis(i,a) /= 0.0) diagonal_basis=.false.
        endif
      enddo
    enddo
  endif

  if (diagonal_basis) then
    do i=1,nreg2d
      wi=weight(i)
      scale=real(basis(i,i),dp)
      mass_m(i,i)=wi*scale*scale
    enddo
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
        scale=real(basis(i,i),dp)
        total_m(i,i,ifloor)=wi*scale*real(total(ibm),dp)*scale
        radial_m(i,i,ifloor)=wi*scale* &
          real(radial2d(i,isnap),dp)*scale
        do l=1,nsct
          scat_m(i,i,l,ifloor)=wi*scale*real(sgas(ibm,l),dp)*scale
          source_m(l,ifloor,i)=wi*scale*real(qext(1,l,ifloor,i),dp)
        enddo
      enddo
    enddo
  else
    do i=1,nreg2d
      wi=weight(i)
      do b=1,nmode
        do a=1,nmode
          mass_m(a,b)=mass_m(a,b)+wi*real(basis(i,a),dp)* &
            real(basis(i,b),dp)
        enddo
      enddo
    enddo
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
                real(basis(i,a),dp)*real(sgas(ibm,l),dp)* &
                real(basis(i,b),dp)
            enddo
          enddo
          do l=1,nsct
            source_m(l,ifloor,a)=source_m(l,ifloor,a)+wi* &
              real(basis(i,a),dp)*real(qext(1,l,ifloor,i),dp)
          enddo
        enddo
      enddo
    enddo
  endif

  ! The boundary and local systems split by radial mode exactly whenever
  ! every stored off-diagonal projected coefficient is zero.
  mode_separable=.true.
  separability: do a=1,nmode
    do b=1,nmode
      if (a == b) cycle
      if (mass_m(a,b) /= 0.0d0 .or. &
          any(total_m(a,b,:) /= 0.0d0) .or. &
          any(radial_m(a,b,:) /= 0.0d0) .or. &
          any(scat_m(a,b,:,:) /= 0.0d0)) then
        mode_separable=.false.
        exit separability
      endif
    enddo
  enddo separability

  do n=1,npq
    do l=1,nsct
      mn(n,l)=0.5d0*real(2*l-1,dp)*real(pl(l,n),dp)
      dn(l,n)=real(w(n),dp)*real(pl(l,n),dp)
    enddo
  enddo

  allocate(face(npq,nmode,nfloor+1),cell(npq,nmode,nfloor))
  allocate(modal_flux(nsct,nfloor,nmode),modal_cour(nfloor+1,nmode))
  face=0.0d0
  cell=0.0d0

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
    if (mode_separable) then
      do a=1,nmode
        call boundary_solve(a,a,face,cell,albedo_left,albedo_right)
      enddo
    else
      call boundary_solve(1,nmode,face,cell,albedo_left,albedo_right)
    endif
  else
    ! Translation boundaries couple the two end faces.  Retain the compact
    ! shooting construction for this uncommon cyclic case.
    if (mode_separable) then
      do a=1,nmode
        call translation_solve(a,a,face,cell,albedo_left,albedo_right)
      enddo
    else
      call translation_solve(1,nmode,face,cell,albedo_left,albedo_right)
    endif
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

  deallocate(opposite,modal_cour,modal_flux,cell,face)
  deallocate(dn,mn,source_m,scat_m,radial_m,total_m,mass_m,weight)
  return

contains

  subroutine boundary_solve(first_mode,last_mode,face_flux,cell_flux, &
                            left_albedo,right_albedo)
    integer, intent(in) :: first_mode,last_mode
    double precision, intent(inout) :: face_flux(npq,nmode,nfloor+1)
    double precision, intent(inout) :: cell_flux(npq,nmode,nfloor)
    double precision, intent(in) :: left_albedo,right_albedo
    double precision, allocatable :: lower(:,:,:),diagonal(:,:,:)
    double precision, allocatable :: upper(:,:,:),right_hand(:,:)
    double precision, allocatable :: cprime(:,:,:),dprime(:,:)
    double precision, allocatable :: solution(:,:),augmented(:,:)
    double precision :: h,kvalue,svalue
    integer :: block,iz,ia,ib,in,jn,il,ir,ic,info,local_state

    local_state=(last_mode-first_mode+1)*npq
    allocate(lower(local_state,local_state,nfloor+1))
    allocate(diagonal(local_state,local_state,nfloor+1))
    allocate(upper(local_state,local_state,nfloor+1))
    allocate(right_hand(local_state,nfloor+1))
    allocate(cprime(local_state,local_state,nfloor+1))
    allocate(dprime(local_state,nfloor+1),solution(local_state,nfloor+1))
    allocate(augmented(local_state,2*local_state+1))
    lower=0.0d0
    diagonal=0.0d0
    upper=0.0d0
    right_hand=0.0d0

    do block=0,nfloor
      do ia=first_mode,last_mode
        do in=1,npq
          ir=(ia-first_mode)*npq+in
          if (du(in) > 0.0) then
            if (block == 0) then
              diagonal(ir,ir,1)=1.0d0
              diagonal(ir,(ia-first_mode)*npq+opposite(in),1)= &
                -left_albedo
              cycle
            endif
            iz=block
          else
            if (block == nfloor) then
              diagonal(ir,ir,nfloor+1)=1.0d0
              diagonal(ir,(ia-first_mode)*npq+opposite(in),nfloor+1)= &
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

          do ib=first_mode,last_mode
            do jn=1,npq
              ic=(ib-first_mode)*npq+jn
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
            ic=(ib-first_mode)*npq+in
            if (du(in) > 0.0) then
              lower(ir,ic,block+1)=lower(ir,ic,block+1)- &
                real(du(in),dp)*mass_m(ia,ib)
              diagonal(ir,ic,block+1)=diagonal(ir,ic,block+1)+ &
                real(du(in),dp)*mass_m(ia,ib)
            else
              diagonal(ir,ic,block+1)=diagonal(ir,ic,block+1)- &
                real(du(in),dp)*mass_m(ia,ib)
              upper(ir,ic,block+1)=upper(ir,ic,block+1)+ &
                real(du(in),dp)*mass_m(ia,ib)
            endif
          enddo
        enddo
      enddo
    enddo

    augmented=0.0d0
    augmented(:,:local_state)=diagonal(:,:,1)
    augmented(:,local_state+1:2*local_state)=upper(:,:,1)
    augmented(:,2*local_state+1)=right_hand(:,1)
    call ALSBD(local_state,local_state+1,augmented,info,local_state)
    if (info /= 0) call XABORT('SPOT1P: SINGULAR FIRST AXIAL BLOCK.')
    cprime(:,:,1)=augmented(:,local_state+1:2*local_state)
    dprime(:,1)=augmented(:,2*local_state+1)

    do block=2,nfloor+1
      augmented=0.0d0
      augmented(:,:local_state)=diagonal(:,:,block)- &
        matmul(lower(:,:,block),cprime(:,:,block-1))
      augmented(:,local_state+1:2*local_state)=upper(:,:,block)
      augmented(:,2*local_state+1)=right_hand(:,block)- &
        matmul(lower(:,:,block),dprime(:,block-1))
      call ALSBD(local_state,local_state+1,augmented,info,local_state)
      if (info /= 0) call XABORT('SPOT1P: SINGULAR AXIAL SCHUR BLOCK.')
      cprime(:,:,block)=augmented(:,local_state+1:2*local_state)
      dprime(:,block)=augmented(:,2*local_state+1)
    enddo

    solution(:,nfloor+1)=dprime(:,nfloor+1)
    do block=nfloor,1,-1
      solution(:,block)=dprime(:,block)- &
        matmul(cprime(:,:,block),solution(:,block+1))
    enddo
    do block=1,nfloor+1
      do ia=first_mode,last_mode
        do in=1,npq
          face_flux(in,ia,block)= &
            solution((ia-first_mode)*npq+in,block)
        enddo
      enddo
    enddo
    do iz=1,nfloor
      cell_flux(:,first_mode:last_mode,iz)=0.5d0* &
        (face_flux(:,first_mode:last_mode,iz)+ &
         face_flux(:,first_mode:last_mode,iz+1))
    enddo

    deallocate(augmented,solution,dprime,cprime,right_hand)
    deallocate(upper,diagonal,lower)
  end subroutine boundary_solve

  subroutine translation_solve(first_mode,last_mode,face_flux,cell_flux, &
                               left_albedo,right_albedo)
    integer, intent(in) :: first_mode,last_mode
    double precision, intent(inout) :: face_flux(npq,nmode,nfloor+1)
    double precision, intent(inout) :: cell_flux(npq,nmode,nfloor)
    double precision, intent(in) :: left_albedo,right_albedo
    double precision, allocatable :: affine(:),response(:,:),system(:,:)
    integer :: local_state,ico,ia,ib,in,jn,row,info

    local_state=(last_mode-first_mode+1)*npq
    allocate(affine(local_state),response(local_state,local_state))
    allocate(system(local_state,local_state+1))

    face_flux(:,first_mode:last_mode,:)=0.0d0
    call sweep(first_mode,last_mode,face_flux,cell_flux)
    do ia=first_mode,last_mode
      do in=1,npq
        row=(ia-first_mode)*npq+in
        affine(row)=face_flux(in,ia,nfloor+1)
      enddo
    enddo

    do ico=1,local_state
      face_flux(:,first_mode:last_mode,:)=0.0d0
      ia=first_mode+(ico-1)/npq
      in=mod(ico-1,npq)+1
      face_flux(in,ia,1)=1.0d0
      call sweep(first_mode,last_mode,face_flux,cell_flux)
      do ib=first_mode,last_mode
        do jn=1,npq
          row=(ib-first_mode)*npq+jn
          response(row,ico)=face_flux(jn,ib,nfloor+1)-affine(row)
        enddo
      enddo
    enddo

    system=0.0d0
    do ia=first_mode,last_mode
      do in=1,npq
        row=(ia-first_mode)*npq+in
        if (du(in) > 0.0) then
          system(row,:local_state)=-left_albedo*response(row,:)
          system(row,row)=system(row,row)+1.0d0
          system(row,local_state+1)=left_albedo*affine(row)
        else
          system(row,:local_state)=response(row,:)
          system(row,row)=system(row,row)-right_albedo
          system(row,local_state+1)=-affine(row)
        endif
      enddo
    enddo

    call ALSBD(local_state,1,system,info,local_state)
    if (info /= 0) call XABORT('SPOT1P: SINGULAR MODAL BOUNDARY SYSTEM.')
    face_flux(:,first_mode:last_mode,:)=0.0d0
    do ia=first_mode,last_mode
      do in=1,npq
        row=(ia-first_mode)*npq+in
        face_flux(in,ia,1)=system(row,local_state+1)
      enddo
    enddo
    call sweep(first_mode,last_mode,face_flux,cell_flux)

    deallocate(system,response,affine)
  end subroutine translation_solve

  subroutine sweep(first_mode,last_mode,face_flux,cell_flux)
    integer, intent(in) :: first_mode,last_mode
    double precision, intent(inout) :: face_flux(npq,nmode,nfloor+1)
    double precision, intent(inout) :: cell_flux(npq,nmode,nfloor)
    double precision, allocatable :: amat(:,:)
    double precision :: h,rhs
    integer :: iz,ia,ib,in,jn,il,ir,ic,info,local_state

    local_state=(last_mode-first_mode+1)*npq
    allocate(amat(local_state,local_state+1))
    cell_flux(:,first_mode:last_mode,:)=0.0d0
    do iz=1,nfloor
      h=real(vol1d(iz),dp)
      amat=0.0d0
      do ia=first_mode,last_mode
        do in=1,npq
          ir=(ia-first_mode)*npq+in
          rhs=0.0d0
          do ib=first_mode,last_mode
            do jn=1,npq
              ic=(ib-first_mode)*npq+jn
              if (in == jn) amat(ir,ic)=amat(ir,ic)+h*total_m(ia,ib,iz)
              do il=1,nsct
                amat(ir,ic)=amat(ir,ic)-h*mn(in,il)* &
                  scat_m(ia,ib,il,iz)*dn(il,jn)
              enddo
              amat(ir,ic)=amat(ir,ic)+h*mn(in,1)* &
                radial_m(ia,ib,iz)*dn(1,jn)
            enddo
            ic=(ib-first_mode)*npq+in
            amat(ir,ic)=amat(ir,ic)+2.0d0*real(du(in),dp)* &
              mass_m(ia,ib)
            rhs=rhs+2.0d0*real(du(in),dp)*mass_m(ia,ib)* &
              face_flux(in,ib,iz)
          enddo
          do il=1,nsct
            rhs=rhs+h*mn(in,il)*source_m(il,iz,ia)
          enddo
          amat(ir,local_state+1)=rhs
        enddo
      enddo
      call ALSBD(local_state,1,amat,info,local_state)
      if (info /= 0) call XABORT('SPOT1P: SINGULAR LOCAL MODAL SYSTEM.')
      do ia=first_mode,last_mode
        do in=1,npq
          ir=(ia-first_mode)*npq+in
          cell_flux(in,ia,iz)=amat(ir,local_state+1)
          face_flux(in,ia,iz+1)=2.0d0*cell_flux(in,ia,iz)- &
            face_flux(in,ia,iz)
        enddo
      enddo
    enddo
    deallocate(amat)
  end subroutine sweep

end subroutine SPOT1P
