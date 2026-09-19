!DECK SPOPHYS
subroutine SPOPHYS(nentry,hentry,ientry,jentry,kentry)
  ! Build a diagnostic full physical radial trial space from an already
  ! assembled SPOD system.  The input system is copied exactly before the
  ! POD basis records are replaced by
  !
  !             B(i,a) = delta(i,a)/sqrt(w(i)),
  !             w(i)   = V(i)/sum_j V(j).
  !
  ! This is a deterministic coordinate change, not a production SPOD option.
  ! It has no user-adjustable input or tolerance, flux fixup, or physical
  ! correction.  Its invariant bound is derived from the REAL32 record format.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_fortran_env, only : int64
  implicit none

  integer, parameter :: nstate=40
  double precision, parameter :: invariant_roundoff_factor=64.0d0
  integer, intent(in) :: nentry,ientry(nentry),jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)

  integer :: isys(nstate),osys(nstate)
  integer :: ngrp,maxmix,igr,nreg2d,nsnap,nmode_old
  integer :: nreg2d_ref,nsnap_ref,rank_min,rank_max
  integer :: i,j,a,k,ilong,itylcm,indic,nitma,s0_length
  integer :: tx_length,sigma_group_length,basis_old_length,coeff_old_length
  integer :: radial_length,basis_new_length,coeff_new_length
  integer :: sigma_first,sigma_last
  integer :: input_fixb,physical_marker
  integer, allocatable :: rank_old(:),rank_new(:)
  real :: flott
  real, allocatable :: volume(:),volume_ref(:),basis_old(:,:),coeff_old(:,:)
  real, allocatable :: basis_new(:,:),coeff_new(:,:)
  real, allocatable :: radial(:),radial_copy(:),tx(:),tx_copy(:)
  real, allocatable :: s0(:),s0_copy(:)
  double precision :: dflott,vtot,inner,norm_ref,norm_diff
  double precision :: ortho_group,complete_group,equiv_group
  double precision :: ortho_max,complete_max,equiv_max,machine_epsilon
  double precision :: invariant_tolerance
  double precision :: rec_error_old,ortho_old
  double precision, allocatable :: weight(:),shape_old(:,:),shape_new(:,:)
  double precision, allocatable :: sigma_old(:),sigma_copy(:)
  double precision, allocatable :: sigma_group_old(:),sigma_group_copy(:)
  character(len=4) :: text4
  character(len=12) :: signature,input_basis_type,group_basis_type
  character(len=12) :: root_basis_type
  character(len=32) :: owner
  type(c_ptr) :: jpin,jpout,kpin,kpout

  if (nentry /= 2) call XABORT('SPOPHYS: TWO ENTRIES EXPECTED.')
  if (any((ientry /= 1).and.(ientry /= 2))) &
    call XABORT('SPOPHYS: LCM ENTRIES EXPECTED.')
  if ((jentry(1) /= 0).or.(jentry(2) /= 2)) &
    call XABORT('SPOPHYS: NEW OUTPUT AND READ-ONLY INPUT EXPECTED.')

  call require_record(kentry(2),'SIGNATURE',3,3,'INPUT SYSTEM')
  call LCMGTC(kentry(2),'SIGNATURE',12,signature)
  if (signature /= 'L_PIJ') &
    call XABORT('SPOPHYS: INPUT '//trim(hentry(2))//' IS NOT L_PIJ.')
  call require_record(kentry(2),'STATE-VECTOR',nstate,1,'INPUT SYSTEM')
  call LCMGET(kentry(2),'STATE-VECTOR',isys)
  ngrp=isys(8)
  maxmix=isys(10)
  if ((ngrp <= 0).or.(maxmix <= 0)) &
    call XABORT('SPOPHYS: INVALID SYSTEM DIMENSIONS.')
  if (maxmix == huge(maxmix)) &
    call XABORT('SPOPHYS: CROSS-SECTION LENGTH OVERFLOWS INTEGER.')
  tx_length=maxmix+1
  call require_record(kentry(2),'POD-RANK-G',ngrp,1,'INPUT SYSTEM')
  call require_record(kentry(2),'GROUP',ngrp,10,'INPUT SYSTEM')
  call require_record(kentry(2),'SPOT-FIXB',1,1,'INPUT SYSTEM')
  call require_record(kentry(2),'SPOT-BTYPE',3,3,'INPUT SYSTEM')
  call LCMGET(kentry(2),'SPOT-FIXB',input_fixb)
  call LCMGTC(kentry(2),'SPOT-BTYPE',12,input_basis_type)
  if (.not.((input_fixb == 0 .and. input_basis_type == 'POD-BUILT').or. &
            (input_fixb == 1 .and. input_basis_type == 'POD-FIXED'))) &
    call XABORT('SPOPHYS: INCONSISTENT INPUT BASIS LIFECYCLE.')
  call LCMLEN(kentry(2),'SPOT-PHYS',ilong,itylcm)
  if (ilong /= 0) then
    if ((ilong /= 1).or.(itylcm /= 1)) &
      call XABORT('SPOPHYS: INVALID INPUT PHYSICAL-BASIS MARKER.')
    call LCMGET(kentry(2),'SPOT-PHYS',physical_marker)
    if (physical_marker == 1) &
      call XABORT('SPOPHYS: INPUT IS ALREADY A PHYSICAL BASIS.')
    call XABORT('SPOPHYS: INVALID INPUT PHYSICAL-BASIS MARKER.')
  endif
  allocate(rank_old(ngrp),rank_new(ngrp))
  call LCMGET(kentry(2),'POD-RANK-G',rank_old)
  if (any(rank_old <= 0)) call XABORT('SPOPHYS: INVALID INPUT POD RANK.')

  ! No option follows the operator name.  In particular, there is no user
  ! coefficient or tolerance hidden in this diagnostic transformation.
  call REDGET(indic,nitma,flott,text4,dflott)
  if ((indic /= 3).or.(text4 /= ';')) &
    call XABORT('SPOPHYS: ; CHARACTER EXPECTED.')

  call LCMEQU(kentry(2),kentry(1))
  call require_record(kentry(1),'SIGNATURE',3,3,'OUTPUT SYSTEM')
  call LCMGTC(kentry(1),'SIGNATURE',12,signature)
  if (signature /= 'L_PIJ') call XABORT('SPOPHYS: INVALID OUTPUT COPY.')
  call require_record(kentry(1),'STATE-VECTOR',nstate,1,'OUTPUT SYSTEM')
  call LCMGET(kentry(1),'STATE-VECTOR',osys)
  if (any(osys /= isys)) call XABORT('SPOPHYS: STATE-VECTOR COPY FAILED.')
  call require_record(kentry(1),'GROUP',ngrp,10,'OUTPUT SYSTEM')

  jpin=LCMGID(kentry(2),'GROUP')
  jpout=LCMGID(kentry(1),'GROUP')
  call LCMLEL(jpin,1,ilong,itylcm)
  if ((ilong /= -1).or.(itylcm /= 0)) &
    call XABORT('SPOPHYS: FIRST INPUT GROUP IS NOT A DIRECTORY.')
  kpin=LCMGIL(jpin,1)
  call require_record(kpin,'NREG2D',1,1,'FIRST INPUT GROUP')
  call require_record(kpin,'NSNAP',1,1,'FIRST INPUT GROUP')
  call LCMGET(kpin,'NREG2D',nreg2d_ref)
  call LCMGET(kpin,'NSNAP',nsnap_ref)
  if ((nreg2d_ref <= 0).or.(nsnap_ref <= 0)) &
    call XABORT('SPOPHYS: INVALID FIRST GROUP DIMENSIONS.')
  allocate(volume_ref(nreg2d_ref))
  sigma_group_length=checked_product(nsnap_ref,ngrp,'ROOT POD SPECTRUM')
  call require_record(kentry(2),'POD-SIGMA-G',sigma_group_length,4, &
    'INPUT SYSTEM')
  allocate(sigma_group_old(sigma_group_length))
  allocate(sigma_group_copy(sigma_group_length))
  call LCMGET(kentry(2),'POD-SIGMA-G',sigma_group_old)
  if (any(.not.ieee_is_finite(sigma_group_old)).or. &
      any(sigma_group_old < 0.0d0)) &
    call XABORT('SPOPHYS: INVALID GROUP SINGULAR VALUES.')
  ortho_max=0.0d0
  complete_max=0.0d0
  equiv_max=0.0d0
  machine_epsilon=real(epsilon(1.0),kind(machine_epsilon))
  invariant_tolerance=invariant_roundoff_factor*machine_epsilon
  group_basis_type='PHYSICAL-ID'
  root_basis_type='POD-FIXED'

  do igr=1,ngrp
    write(owner,'(A,I0)') 'GROUP ',igr
    call LCMLEL(jpin,igr,ilong,itylcm)
    if ((ilong /= -1).or.(itylcm /= 0)) &
      call XABORT('SPOPHYS: INPUT GROUP ITEM IS NOT A DIRECTORY.')
    call LCMLEL(jpout,igr,ilong,itylcm)
    if ((ilong /= -1).or.(itylcm /= 0)) &
      call XABORT('SPOPHYS: OUTPUT GROUP ITEM IS NOT A DIRECTORY.')
    kpin=LCMGIL(jpin,igr)
    kpout=LCMGIL(jpout,igr)

    call require_record(kpin,'NREG2D',1,1,owner)
    call require_record(kpin,'NSNAP',1,1,owner)
    call require_record(kpin,'POD-NMODE',1,1,owner)
    call LCMGET(kpin,'NREG2D',nreg2d)
    call LCMGET(kpin,'NSNAP',nsnap)
    call LCMGET(kpin,'POD-NMODE',nmode_old)
    if ((nreg2d <= 0).or.(nsnap <= 0).or.(nmode_old <= 0).or. &
        (nmode_old > nreg2d)) &
      call XABORT('SPOPHYS: INVALID GROUP POD DIMENSIONS.')
    if (rank_old(igr) /= nmode_old) &
      call XABORT('SPOPHYS: POD-RANK-G IS INCONSISTENT.')
    if ((nreg2d /= nreg2d_ref).or.(nsnap /= nsnap_ref)) then
      call XABORT('SPOPHYS: GROUP RADIAL DIMENSIONS DIFFER.')
    endif

    basis_old_length=checked_product(nreg2d,nmode_old,'INPUT POD BASIS')
    coeff_old_length=checked_product(nmode_old,nsnap,'INPUT POD COEFFICIENTS')
    radial_length=checked_product(nreg2d,nsnap,'RADIAL OPERATOR')
    basis_new_length=checked_product(nreg2d,nreg2d,'PHYSICAL BASIS')
    coeff_new_length=checked_product(nreg2d,nsnap,'PHYSICAL COEFFICIENTS')

    call require_record(kpin,'VOL2D',nreg2d,2,owner)
    call require_record(kpin,'POD-BASIS',basis_old_length,2,owner)
    call require_record(kpin,'POD-COEFF',coeff_old_length,2,owner)
    call require_record(kpin,'POD-SIGMA',nsnap,4,owner)
    call require_record(kpin,'POD-REC-ERR',1,4,owner)
    call require_record(kpin,'POD-ORTHO',1,4,owner)
    call require_record(kpin,'RADIAL-OP',radial_length,2,owner)
    call require_record(kpin,'DRAGON-TXSC',tx_length,2,owner)
    call LCMLEN(kpin,'DRAGON-S0XSC',s0_length,itylcm)
    if ((itylcm /= 2).or.(s0_length <= 0).or. &
        (mod(s0_length,tx_length) /= 0)) &
      call XABORT('SPOPHYS: INVALID DRAGON-S0XSC RECORD.')

    allocate(volume(nreg2d),basis_old(nreg2d,nmode_old))
    allocate(coeff_old(nmode_old,nsnap),basis_new(nreg2d,nreg2d))
    allocate(coeff_new(nreg2d,nsnap),weight(nreg2d))
    allocate(shape_old(nreg2d,nsnap),shape_new(nreg2d,nsnap))
    allocate(sigma_old(nsnap),sigma_copy(nsnap))
    allocate(radial(radial_length),radial_copy(radial_length))
    allocate(tx(tx_length),tx_copy(tx_length))
    allocate(s0(s0_length),s0_copy(s0_length))

    call LCMGET(kpin,'VOL2D',volume)
    call LCMGET(kpin,'POD-BASIS',basis_old)
    call LCMGET(kpin,'POD-COEFF',coeff_old)
    call LCMGET(kpin,'POD-SIGMA',sigma_old)
    call LCMGET(kpin,'POD-REC-ERR',rec_error_old)
    call LCMGET(kpin,'POD-ORTHO',ortho_old)
    call LCMGET(kpin,'RADIAL-OP',radial)
    call LCMGET(kpin,'DRAGON-TXSC',tx)
    call LCMGET(kpin,'DRAGON-S0XSC',s0)
    if (any(.not.ieee_is_finite(volume)).or.any(volume <= 0.0).or. &
        any(.not.ieee_is_finite(basis_old)).or. &
        any(.not.ieee_is_finite(coeff_old)).or. &
        any(.not.ieee_is_finite(sigma_old)).or.any(sigma_old < 0.0d0).or. &
        (.not.ieee_is_finite(rec_error_old)).or.(rec_error_old < 0.0d0).or. &
        (.not.ieee_is_finite(ortho_old)).or.(ortho_old < 0.0d0).or. &
        any(.not.ieee_is_finite(radial)).or. &
        any(.not.ieee_is_finite(tx)).or.any(.not.ieee_is_finite(s0))) &
      call XABORT('SPOPHYS: NON-FINITE OR INVALID INPUT RECORD.')
    sigma_first=(igr-1)*nsnap+1
    sigma_last=igr*nsnap
    if (.not.same_double_bits(sigma_old, &
        sigma_group_old(sigma_first:sigma_last))) &
      call XABORT('SPOPHYS: ROOT/GROUP POD SPECTRA DIFFER.')
    do k=2,nsnap
      if (sigma_old(k) > sigma_old(k-1)) &
        call XABORT('SPOPHYS: INPUT POD SPECTRUM IS NOT ORDERED.')
    enddo

    if (igr == 1) then
      volume_ref=volume
    else if (.not.same_real_bits(volume,volume_ref)) then
      call XABORT('SPOPHYS: GROUP RADIAL VOLUMES DIFFER.')
    endif

    vtot=sum(real(volume,dp))
    if ((.not.ieee_is_finite(vtot)).or.(vtot <= 0.0d0)) &
      call XABORT('SPOPHYS: INVALID RADIAL VOLUME SUM.')
    weight=real(volume,dp)/vtot
    if (any(.not.ieee_is_finite(weight)).or.any(weight <= 0.0d0)) &
      call XABORT('SPOPHYS: INVALID RADIAL WEIGHTS.')

    shape_old=matmul(real(basis_old,dp),real(coeff_old,dp))
    if (any(.not.ieee_is_finite(shape_old))) &
      call XABORT('SPOPHYS: NON-FINITE RECONSTRUCTED SNAPSHOT.')
    basis_new=0.0
    coeff_new=0.0
    do i=1,nreg2d
      basis_new(i,i)=real(1.0d0/sqrt(weight(i)))
      do k=1,nsnap
        coeff_new(i,k)=real(sqrt(weight(i))*shape_old(i,k))
      enddo
    enddo
    if (any(.not.ieee_is_finite(basis_new)).or. &
        any(.not.ieee_is_finite(coeff_new))) &
      call XABORT('SPOPHYS: NON-FINITE PHYSICAL BASIS.')
    shape_new=matmul(real(basis_new,dp),real(coeff_new,dp))

    ortho_group=0.0d0
    complete_group=0.0d0
    do a=1,nreg2d
      do j=1,nreg2d
        inner=sum(weight*real(basis_new(:,a),dp)* &
                  real(basis_new(:,j),dp))
        if (a == j) inner=inner-1.0d0
        ortho_group=max(ortho_group,abs(inner))
      enddo
    enddo
    do i=1,nreg2d
      do j=1,nreg2d
        inner=sum(real(basis_new(i,:),dp)*real(basis_new(j,:),dp))*weight(j)
        if (i == j) inner=inner-1.0d0
        complete_group=max(complete_group,abs(inner))
      enddo
    enddo
    norm_ref=0.0d0
    norm_diff=0.0d0
    do k=1,nsnap
      norm_ref=norm_ref+sum(weight*shape_old(:,k)*shape_old(:,k))
      norm_diff=norm_diff+sum(weight*(shape_new(:,k)-shape_old(:,k))**2)
    enddo
    if ((.not.ieee_is_finite(norm_ref)).or.(norm_ref < 0.0d0).or. &
        (.not.ieee_is_finite(norm_diff)).or.(norm_diff < 0.0d0)) &
      call XABORT('SPOPHYS: INVALID SNAPSHOT EQUIVALENCE NORM.')
    if (norm_ref == 0.0d0) then
      if (norm_diff /= 0.0d0) &
        call XABORT('SPOPHYS: ZERO SNAPSHOT CHANGED BY TRANSFORM.')
      equiv_group=0.0d0
    else
      equiv_group=sqrt(norm_diff/norm_ref)
    endif
    if ((.not.ieee_is_finite(ortho_group)).or. &
        (.not.ieee_is_finite(complete_group)).or. &
        (.not.ieee_is_finite(equiv_group))) &
      call XABORT('SPOPHYS: NON-FINITE BASIS INVARIANT.')
    if (ortho_group > invariant_tolerance) &
      call XABORT('SPOPHYS: PHYSICAL BASIS ORTHOGONALITY EXCEEDS ROUNDOFF.')
    if (complete_group > invariant_tolerance) &
      call XABORT('SPOPHYS: PHYSICAL BASIS COMPLETENESS EXCEEDS ROUNDOFF.')
    if (equiv_group > invariant_tolerance) &
      call XABORT('SPOPHYS: SNAPSHOT EQUIVALENCE EXCEEDS ROUNDOFF.')
    ortho_max=max(ortho_max,ortho_group)
    complete_max=max(complete_max,complete_group)
    equiv_max=max(equiv_max,equiv_group)

    ! POD-REC-ERR remains the error against the unavailable original
    ! snapshots.  PHYS-SNAP separately records the roundoff-only error of
    ! this coordinate change.  The physical operators and cross sections
    ! remain the exact records produced by SPOASM.
    call LCMPUT(kpout,'POD-NMODE',1,1,nreg2d)
    call LCMPUT(kpout,'POD-BASIS',basis_new_length,2,basis_new)
    call LCMPUT(kpout,'POD-COEFF',coeff_new_length,2,coeff_new)
    call LCMPUT(kpout,'POD-REC-ERR',1,4,rec_error_old)
    call LCMPUT(kpout,'POD-ORTHO',1,4,ortho_group)
    call LCMPUT(kpout,'PHYS-ORTHO',1,4,ortho_group)
    call LCMPUT(kpout,'PHYS-COMP',1,4,complete_group)
    call LCMPUT(kpout,'PHYS-SNAP',1,4,equiv_group)
    call LCMPUT(kpout,'PHYS-TOL',1,4,invariant_tolerance)
    call LCMPTC(kpout,'SPOT-BTYPE',12,group_basis_type)
    rank_new(igr)=nreg2d

    call require_record(kpout,'POD-NMODE',1,1,owner)
    call require_record(kpout,'POD-BASIS',basis_new_length,2,owner)
    call require_record(kpout,'POD-COEFF',coeff_new_length,2,owner)
    call require_record(kpout,'POD-SIGMA',nsnap,4,owner)
    call require_record(kpout,'POD-REC-ERR',1,4,owner)
    call require_record(kpout,'POD-ORTHO',1,4,owner)
    call require_record(kpout,'PHYS-ORTHO',1,4,owner)
    call require_record(kpout,'PHYS-COMP',1,4,owner)
    call require_record(kpout,'PHYS-SNAP',1,4,owner)
    call require_record(kpout,'PHYS-TOL',1,4,owner)
    call require_record(kpout,'SPOT-BTYPE',3,3,owner)

    ! Verify exact preservation after the basis records have been replaced.
    call require_record(kpout,'RADIAL-OP',radial_length,2,owner)
    call require_record(kpout,'DRAGON-TXSC',tx_length,2,owner)
    call require_record(kpout,'DRAGON-S0XSC',s0_length,2,owner)
    call LCMGET(kpout,'RADIAL-OP',radial_copy)
    call LCMGET(kpout,'DRAGON-TXSC',tx_copy)
    call LCMGET(kpout,'DRAGON-S0XSC',s0_copy)
    call LCMGET(kpout,'POD-SIGMA',sigma_copy)
    if ((.not.same_real_bits(radial_copy,radial)).or. &
        (.not.same_real_bits(tx_copy,tx)).or. &
        (.not.same_real_bits(s0_copy,s0))) &
      call XABORT('SPOPHYS: PHYSICAL OPERATOR COPY CHANGED.')
    if (.not.same_double_bits(sigma_copy,sigma_old)) &
      call XABORT('SPOPHYS: SNAPSHOT SPECTRUM COPY CHANGED.')

    deallocate(s0_copy,s0,tx_copy,tx,radial_copy,radial)
    deallocate(sigma_copy,sigma_old)
    deallocate(shape_new,shape_old,weight,coeff_new,basis_new)
    deallocate(coeff_old,basis_old,volume)
  enddo

  call LCMPUT(kentry(1),'POD-RANK-OLD',ngrp,1,rank_old)
  call LCMPUT(kentry(1),'POD-RANK-G',ngrp,1,rank_new)
  call LCMPUT(kentry(1),'SPOT-FIXB',1,1,(/1/))
  call LCMPUT(kentry(1),'SPOT-PHYS',1,1,(/1/))
  call LCMPUT(kentry(1),'SPOT-PH-ORT',1,4,ortho_max)
  call LCMPUT(kentry(1),'SPOT-PH-CMP',1,4,complete_max)
  call LCMPUT(kentry(1),'SPOT-PH-SNP',1,4,equiv_max)
  call LCMPUT(kentry(1),'SPOT-PH-TOL',1,4,invariant_tolerance)
  call LCMPTC(kentry(1),'SPOT-BTYPE',12,root_basis_type)
  call require_record(kentry(1),'POD-RANK-OLD',ngrp,1,'OUTPUT SYSTEM')
  call require_record(kentry(1),'POD-RANK-G',ngrp,1,'OUTPUT SYSTEM')
  call require_record(kentry(1),'POD-SIGMA-G',sigma_group_length,4, &
    'OUTPUT SYSTEM')
  call require_record(kentry(1),'SPOT-FIXB',1,1,'OUTPUT SYSTEM')
  call require_record(kentry(1),'SPOT-PHYS',1,1,'OUTPUT SYSTEM')
  call require_record(kentry(1),'SPOT-PH-ORT',1,4,'OUTPUT SYSTEM')
  call require_record(kentry(1),'SPOT-PH-CMP',1,4,'OUTPUT SYSTEM')
  call require_record(kentry(1),'SPOT-PH-SNP',1,4,'OUTPUT SYSTEM')
  call require_record(kentry(1),'SPOT-PH-TOL',1,4,'OUTPUT SYSTEM')
  call require_record(kentry(1),'SPOT-BTYPE',3,3,'OUTPUT SYSTEM')
  call LCMGET(kentry(1),'POD-SIGMA-G',sigma_group_copy)
  if (.not.same_double_bits(sigma_group_copy,sigma_group_old)) &
    call XABORT('SPOPHYS: ROOT SNAPSHOT SPECTRUM COPY CHANGED.')

  rank_min=minval(rank_old)
  rank_max=maxval(rank_old)
  write(6,'(A,5I8)') &
    'SPOPHYS GROUPS/NREG2D OLD-RANK-MIN/MAX NEW-RANK ', &
    ngrp,nreg2d_ref,rank_min,rank_max,nreg2d_ref
  write(6,'(A,1P,4E13.5)') &
    'SPOPHYS MAX ORTHO/COMP/SNAPSHOT-EQUIV/EPS ', &
    ortho_max,complete_max,equiv_max,machine_epsilon
  write(6,'(A)') 'SPOPHYS PRESERVE RADIAL-OP/XS EXACT'
  write(6,'(A,1P,E13.5)') 'SPOPHYS INVARIANT FAIL-CLOSED TOL ', &
    invariant_tolerance
  write(6,'(A)') 'SPOPHYS BASIS POD-FIXED/PHYSICAL-ID'

  deallocate(sigma_group_copy,sigma_group_old)
  deallocate(volume_ref,rank_new,rank_old)
  return

contains

  logical function same_real_bits(left,right)
    real, intent(in) :: left(:),right(:)

    if (size(left) /= size(right)) then
      same_real_bits=.false.
    else
      same_real_bits=all(transfer(left,0,size(left)) == &
        transfer(right,0,size(right)))
    endif
  end function same_real_bits

  logical function same_double_bits(left,right)
    double precision, intent(in) :: left(:),right(:)

    if (size(left) /= size(right)) then
      same_double_bits=.false.
    else
      same_double_bits=all(transfer(left,0_int64,size(left)) == &
        transfer(right,0_int64,size(right)))
    endif
  end function same_double_bits

  integer function checked_product(left,right,label) result(product)
    integer, intent(in) :: left,right
    character(len=*), intent(in) :: label
    integer(int64) :: wide_product
    character(len=131) :: message

    if ((left <= 0).or.(right <= 0)) then
      write(message,'(A,A,A)') 'SPOPHYS: INVALID ',trim(label),' DIMENSION.'
      call XABORT(message)
    endif
    wide_product=int(left,int64)*int(right,int64)
    if (wide_product > int(huge(product),int64)) then
      write(message,'(A,A,A)') 'SPOPHYS: ',trim(label), &
        ' LENGTH OVERFLOWS INTEGER.'
      call XABORT(message)
    endif
    product=int(wide_product)
  end function checked_product

  subroutine require_record(ip,name,expected_length,expected_type,record_owner)
    type(c_ptr), intent(in) :: ip
    character(len=*), intent(in) :: name,record_owner
    integer, intent(in) :: expected_length,expected_type
    integer :: length_found,type_found
    character(len=131) :: message

    call LCMLEN(ip,name,length_found,type_found)
    if ((length_found /= expected_length).or.(type_found /= expected_type)) then
      write(message,'(A,A,A,A,A,I0,A,I0,A,I0,A,I0)') &
        'SPOPHYS: ',trim(record_owner),' RECORD ',trim(name), &
        ' HAS LENGTH/TYPE ',length_found,'/',type_found, &
        '; EXPECTED ',expected_length,'/',expected_type
      call XABORT(message)
    endif
  end subroutine require_record

end subroutine SPOPHYS
