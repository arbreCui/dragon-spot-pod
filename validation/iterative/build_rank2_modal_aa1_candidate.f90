program build_rank2_modal_aa1_candidate
  ! Materialize one rank-two modal-projected Anderson(1) proposal without
  ! assembly, transport, or a nonlinear-map evaluation.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32,int64,real32,real64
  implicit none

  integer, parameter :: nstate=40,max_path=72

  type :: canonical_state
    type(c_ptr) :: root
    integer :: state(nstate)=0
    integer :: dims(4)=0
    integer :: fixb=-1
    integer, allocatable :: rank(:),offset(:),gram_offset(:),basis_offset(:)
    real(real32), allocatable :: basis(:)
    real(real64), allocatable :: coordinates(:),leakage(:),height(:),gram(:)
    real(real64), allocatable :: offspace(:)
    real(real32) :: keff=0.0_real32
    real(real64) :: rho=0.0_real64,norm=0.0_real64,gram_error=0.0_real64
    character(len=12) :: norm_id='',basis_type=''
  end type canonical_state

  character(len=1024) :: path(6)
  character(len=12) :: marker
  type(canonical_state) :: x0,x1,x2
  type(c_ptr) :: snap2,staged_ax,staged_snap,out_ax,out_snap,fluxes,plane
  integer :: i,igr,isnap,a,b,nmode,nreg2d
  integer :: index_a,index_b,index_g,index_l
  real(real64) :: update_sq(2),update_dot,denominator,beta,weight1
  real(real64) :: delta01_a,delta01_b,delta12_a,delta12_b
  real(real64) :: rho_star,rho_public,l_roundtrip,reconstructed
  real(real64) :: min_reconstructed,iter_keff
  real(real32) :: keff_public,projected
  real(real64), allocatable :: candidate_a(:),candidate_l(:)
  real(real32), allocatable :: published_l(:)

  if (command_argument_count() /= 6) error stop &
    'expected x0 x1 x2 x2_snap out_ax out_snap'
  do i=1,6
    call get_command_argument(i,path(i))
    if ((len_trim(path(i)) == 0).or.(len_trim(path(i)) > max_path)) &
      error stop 'XSM path is empty or exceeds GANLIB limit'
  enddo
  if (trim(path(5)) == trim(path(6))) &
    error stop 'candidate AX and snapshot paths must differ'
  call require_fresh_path(path(5))
  call require_fresh_path(path(6))

  call load_state(trim(path(1)),x0,'x0')
  call load_state(trim(path(2)),x1,'x1')
  call load_state(trim(path(3)),x2,'x2')
  call compare_fixed_space(x0,x1,'x0/x1')
  call compare_fixed_space(x1,x2,'x1/x2')
  call validate_snapshot(trim(path(4)),x1,x2,snap2)

  ! Reproduce the full Gram-height arithmetic of the frozen direction audit.
  update_sq=0.0_real64
  update_dot=0.0_real64
  do igr=1,x0%dims(2)
    nmode=x0%rank(igr)
    do isnap=1,x0%dims(3)
      do a=1,nmode
        index_a=x0%offset(igr)+(isnap-1)*nmode+a
        delta01_a=x1%coordinates(index_a)-x0%coordinates(index_a)
        delta12_a=x2%coordinates(index_a)-x1%coordinates(index_a)
        do b=1,nmode
          index_b=x0%offset(igr)+(isnap-1)*nmode+b
          index_g=x0%gram_offset(igr)+(b-1)*nmode+a
          delta01_b=x1%coordinates(index_b)-x0%coordinates(index_b)
          delta12_b=x2%coordinates(index_b)-x1%coordinates(index_b)
          update_sq(1)=update_sq(1)+x0%height(isnap)*delta01_a* &
            x0%gram(index_g)*delta01_b
          update_sq(2)=update_sq(2)+x0%height(isnap)*delta12_a* &
            x0%gram(index_g)*delta12_b
          update_dot=update_dot+x0%height(isnap)*delta01_a* &
            x0%gram(index_g)*delta12_b
        enddo
      enddo
    enddo
  enddo
  if (any(.not.ieee_is_finite(update_sq)).or. &
      any(update_sq <= 0.0_real64).or. &
      (.not.ieee_is_finite(update_dot))) &
    error stop 'invalid modal update geometry'
  denominator=update_sq(1)+update_sq(2)-2.0_real64*update_dot
  if ((.not.ieee_is_finite(denominator)).or. &
      (denominator <= 0.0_real64)) &
    error stop 'singular modal Anderson scalar system'
  beta=(update_sq(1)-update_dot)/denominator
  weight1=1.0_real64-beta
  if ((.not.ieee_is_finite(beta)).or.(.not.ieee_is_finite(weight1))) &
    error stop 'nonfinite modal Anderson weight'

  allocate(candidate_a(size(x1%coordinates)))
  allocate(candidate_l(size(x1%leakage)),published_l(size(x1%leakage)))
  candidate_a=weight1*x1%coordinates+beta*x2%coordinates
  candidate_l=weight1*x1%leakage+beta*x2%leakage
  published_l=real(candidate_l,real32)
  rho_star=weight1*x1%rho+beta*x2%rho
  if ((.not.ieee_is_finite(rho_star)).or.(rho_star <= 0.0_real64)) &
    error stop 'invalid affine inverse eigenvalue'
  keff_public=real(1.0_real64/rho_star,real32)
  if ((.not.ieee_is_finite(keff_public)).or. &
      (keff_public <= 0.0_real32)) &
    error stop 'invalid published effective eigenvalue'
  rho_public=1.0_real64/real(keff_public,real64)
  if (any(.not.ieee_is_finite(candidate_a)).or. &
      any(.not.ieee_is_finite(candidate_l)).or. &
      any(.not.ieee_is_finite(published_l)).or. &
      (.not.ieee_is_finite(rho_public)).or.(rho_public <= 0.0_real64)) &
    error stop 'nonfinite published proposal'
  l_roundtrip=maxval(abs(real(published_l,real64)-candidate_l))

  ! Reproduce SPOPROJ FIXB's B*a accumulation and final binary32 cast.
  min_reconstructed=huge(min_reconstructed)
  do igr=1,x2%dims(2)
    nmode=x2%rank(igr)
    nreg2d=(x2%basis_offset(igr+1)-x2%basis_offset(igr))/nmode
    do isnap=1,x2%dims(3)
      do i=1,nreg2d
        reconstructed=0.0_real64
        do a=1,nmode
          index_a=x2%offset(igr)+(isnap-1)*nmode+a
          index_b=x2%basis_offset(igr)+(a-1)*nreg2d+i
          reconstructed=reconstructed+ &
            real(x2%basis(index_b),real64)*candidate_a(index_a)
        enddo
        projected=real(reconstructed,real32)
        if ((.not.ieee_is_finite(projected)).or. &
            (projected <= 0.0_real32)) &
          error stop 'published reconstructed flux is not strictly positive'
        min_reconstructed=min(min_reconstructed,real(projected,real64))
      enddo
    enddo
  enddo

  ! AX is an explicitly labelled x2 raw-flux carrier.  Only the complete
  ! outer state (A,rho,L) and its binary32 effective eigenvalue are replaced.
  call LCMOP(staged_ax,' ',0,1,0)
  call LCMEQU(x2%root,staged_ax)
  call LCMPUT(staged_ax,'SPOT-X-A',size(candidate_a),4,candidate_a)
  call LCMPUT(staged_ax,'K-EFFECTIVE',1,2,keff_public)
  call LCMPUT(staged_ax,'SPOT-X-RHO',1,4,rho_public)
  call LCMPUT(staged_ax,'SPOT-X-L',size(published_l),4, &
    real(published_l,real64))
  call delete_if_present(staged_ax,'SPOT-X-RRHO')
  call delete_if_present(staged_ax,'SPOT-X-RLEAK')
  call delete_if_present(staged_ax,'SPOT-X-DLEAK')
  call delete_if_present(staged_ax,'SPOT-X-RA')
  call delete_if_present(staged_ax,'SPOT-X-PERP')
  call delete_if_present(staged_ax,'SPOT-X-EPOCH')
  call delete_if_present(staged_ax,'SPOT-GBAL')
  ! The physical GANLIB key is the 12-character truncation of the logical
  ! diagnostic name SPOT-GBAL-MAX.
  call delete_if_present(staged_ax,'SPOT-GBAL-MA')
  marker='PROPOSAL'
  call LCMPTC(staged_ax,'SPOT-X-STATE',12,marker)
  marker='X2-RAW-FLUX'
  call LCMPTC(staged_ax,'SPOT-X-CARR',12,marker)
  call LCMOP(out_ax,trim(path(5)),0,2,0)
  call LCMEQU(staged_ax,out_ax)
  call LCMCL(out_ax,1)
  call LCMCL(staged_ax,2)

  ! The x2 archive remains a carrier.  Publish only the root k identity and
  ! FLUX leakage consumed by the next assembly; preserve lagged SYSTEM data.
  call LCMOP(staged_snap,' ',0,1,0)
  call LCMEQU(snap2,staged_snap)
  iter_keff=real(keff_public,real64)
  call LCMPUT(staged_snap,'SPOT-ITER-K',1,4,iter_keff)
  call delete_if_present(staged_snap,'SPOT-L1-ERR')
  call delete_if_present(staged_snap,'SPOT-PJ-PERP')
  call delete_if_present(staged_snap,'SPOT-PROJECT')
  fluxes=LCMGID(staged_snap,'FLUX')
  do isnap=1,x2%dims(3)
    plane=LCMGIL(fluxes,isnap)
    index_l=(isnap-1)*x2%dims(2)+1
    call LCMPUT(plane,'SPOT-LEAK1D',x2%dims(2),2, &
      published_l(index_l:index_l+x2%dims(2)-1))
  enddo

  call LCMOP(out_snap,trim(path(6)),0,2,0)
  call LCMEQU(staged_snap,out_snap)
  call LCMCL(out_snap,1)
  call LCMCL(staged_snap,2)
  call LCMCL(snap2,1)
  call LCMCL(x2%root,1)
  call LCMCL(x1%root,1)
  call LCMCL(x0%root,1)

  write(*,'(A,ES24.16)') 'RANK2-MODAL-AA1 BETA-WEIGHT-X2 ',beta
  write(*,'(A,ES24.16)') 'RANK2-MODAL-AA1 WEIGHT-X1 ',weight1
  write(*,'(A,ES24.16)') 'RANK2-MODAL-AA1 DENOMINATOR ',denominator
  write(*,'(A,ES24.16)') 'RANK2-MODAL-AA1 RHO-AFFINE ',rho_star
  write(*,'(A,ES24.16)') 'RANK2-MODAL-AA1 K-PUBLISHED ', &
    real(keff_public,real64)
  write(*,'(A,ES24.16)') 'RANK2-MODAL-AA1 RHO-PUBLISHED ',rho_public
  write(*,'(A,ES24.16)') 'RANK2-MODAL-AA1 RHO-Q-DELTA ', &
    rho_public-rho_star
  write(*,'(A,ES24.16)') 'RANK2-MODAL-AA1 L-ROUNDTRIP-MAX ',l_roundtrip
  write(*,'(A,ES24.16)') 'RANK2-MODAL-AA1 MIN-PUBLISHED-BA ', &
    min_reconstructed
  write(*,'(A)') &
    'RANK2-MODAL-AA1 PROPOSAL COMPLETE NOT-EVALUATED NO-DRAGON NO-MAP'

contains

  subroutine load_state(file_name,data,owner)
    character(len=*), intent(in) :: file_name,owner
    type(canonical_state), intent(out) :: data
    integer :: ngrp,nsnap,ncoef,total_basis,total_gram,g,nreg
    call LCMOP(data%root,file_name,2,2,0)
    call require_character(data%root,'SIGNATURE','L_FLUX',owner)
    call require_record(data%root,'STATE-VECTOR',nstate,1,owner)
    call require_record(data%root,'SPOT-X-DIMS',4,1,owner)
    call LCMGET(data%root,'STATE-VECTOR',data%state)
    call LCMGET(data%root,'SPOT-X-DIMS',data%dims)
    ngrp=data%dims(2)
    nsnap=data%dims(3)
    ncoef=data%dims(4)
    if ((data%dims(1) /= 1).or.(ngrp /= 370).or.(nsnap /= 3).or. &
        (ncoef /= 2220).or.(data%state(1) /= ngrp)) &
      error stop 'invalid frozen rank-two dimensions'

    allocate(data%rank(ngrp),data%offset(ngrp+1))
    allocate(data%gram_offset(ngrp+1),data%basis_offset(ngrp+1))
    call require_record(data%root,'SPOT-X-RANK',ngrp,1,owner)
    call require_record(data%root,'SPOT-X-OFF',ngrp+1,1,owner)
    call require_record(data%root,'SPOT-X-GOFF',ngrp+1,1,owner)
    call require_record(data%root,'SPOT-X-BOFF',ngrp+1,1,owner)
    call LCMGET(data%root,'SPOT-X-RANK',data%rank)
    call LCMGET(data%root,'SPOT-X-OFF',data%offset)
    call LCMGET(data%root,'SPOT-X-GOFF',data%gram_offset)
    call LCMGET(data%root,'SPOT-X-BOFF',data%basis_offset)
    if (any(data%rank /= 2).or.(data%offset(1) /= 0).or. &
        (data%gram_offset(1) /= 0).or.(data%basis_offset(1) /= 0).or. &
        (data%offset(ngrp+1) /= ncoef)) &
      error stop 'invalid frozen rank-two layout'
    do g=1,ngrp
      if (data%offset(g+1)-data%offset(g) /= nsnap*data%rank(g)) &
        error stop 'invalid rank-two coordinate offsets'
      if (data%gram_offset(g+1)-data%gram_offset(g) /= &
          data%rank(g)*data%rank(g)) &
        error stop 'invalid rank-two Gram offsets'
      nreg=(data%basis_offset(g+1)-data%basis_offset(g))/data%rank(g)
      if ((nreg /= 8).or. &
          (data%basis_offset(g+1)-data%basis_offset(g) /= &
           nreg*data%rank(g))) &
        error stop 'invalid rank-two basis offsets'
    enddo
    total_basis=data%basis_offset(ngrp+1)
    total_gram=data%gram_offset(ngrp+1)
    allocate(data%basis(total_basis),data%coordinates(ncoef))
    allocate(data%leakage(ngrp*nsnap),data%height(nsnap))
    allocate(data%gram(total_gram),data%offspace(ngrp*nsnap))
    call require_record(data%root,'SPOT-X-BASIS',total_basis,2,owner)
    call require_record(data%root,'SPOT-X-A',ncoef,4,owner)
    call require_record(data%root,'SPOT-X-L',ngrp*nsnap,4,owner)
    call require_record(data%root,'SPOT-X-H',nsnap,4,owner)
    call require_record(data%root,'SPOT-X-GRAM',total_gram,4,owner)
    call require_record(data%root,'SPOT-X-PERP',ngrp*nsnap,4,owner)
    call require_record(data%root,'K-EFFECTIVE',1,2,owner)
    call require_record(data%root,'SPOT-X-RHO',1,4,owner)
    call require_record(data%root,'SPOT-X-NORM',1,4,owner)
    call require_record(data%root,'SPOT-X-GERR',1,4,owner)
    call require_record(data%root,'SPOT-X-FIXB',1,1,owner)
    call require_record(data%root,'SPOT-X-NID',3,3,owner)
    call require_record(data%root,'SPOT-X-BTYP',3,3,owner)
    call LCMGET(data%root,'SPOT-X-BASIS',data%basis)
    call LCMGET(data%root,'SPOT-X-A',data%coordinates)
    call LCMGET(data%root,'SPOT-X-L',data%leakage)
    call LCMGET(data%root,'SPOT-X-H',data%height)
    call LCMGET(data%root,'SPOT-X-GRAM',data%gram)
    call LCMGET(data%root,'SPOT-X-PERP',data%offspace)
    call LCMGET(data%root,'K-EFFECTIVE',data%keff)
    call LCMGET(data%root,'SPOT-X-RHO',data%rho)
    call LCMGET(data%root,'SPOT-X-NORM',data%norm)
    call LCMGET(data%root,'SPOT-X-GERR',data%gram_error)
    call LCMGET(data%root,'SPOT-X-FIXB',data%fixb)
    call LCMGTC(data%root,'SPOT-X-NID',12,data%norm_id)
    call LCMGTC(data%root,'SPOT-X-BTYP',12,data%basis_type)
    if ((data%fixb /= 1).or.(data%norm_id /= 'NUFISS-UNIT').or. &
        (data%basis_type /= 'POD-FIXED')) &
      error stop 'invalid fixed-basis state markers'
    if (any(.not.ieee_is_finite(data%basis)).or. &
        any(.not.ieee_is_finite(data%coordinates)).or. &
        any(.not.ieee_is_finite(data%leakage)).or. &
        any(.not.ieee_is_finite(data%height)).or. &
        any(data%height <= 0.0_real64).or. &
        any(.not.ieee_is_finite(data%gram)).or. &
        any(.not.ieee_is_finite(data%offspace)).or. &
        any(data%offspace < 0.0_real64).or. &
        (.not.ieee_is_finite(data%keff)).or.(data%keff <= 0.0_real32).or. &
        (.not.ieee_is_finite(data%rho)).or.(data%rho <= 0.0_real64).or. &
        (.not.ieee_is_finite(data%norm)).or.(data%norm <= 0.0_real64).or. &
        (.not.ieee_is_finite(data%gram_error)).or. &
        (data%gram_error < 0.0_real64)) &
      error stop 'nonfinite canonical rank-two state'
    if (any(bits64(data%leakage) /= &
            bits64(real(real(data%leakage,real32),real64)))) &
      error stop 'canonical leakage is not promoted binary32'
    if (bits64(data%rho) /= &
        bits64(1.0_real64/real(data%keff,real64))) &
      error stop 'inverse-eigenvalue identity differs'
  end subroutine load_state

  subroutine compare_fixed_space(left,right,owner)
    type(canonical_state), intent(in) :: left,right
    character(len=*), intent(in) :: owner
    if (any(left%state /= right%state).or.any(left%dims /= right%dims).or. &
        any(left%rank /= right%rank).or.any(left%offset /= right%offset).or. &
        any(left%gram_offset /= right%gram_offset).or. &
        any(left%basis_offset /= right%basis_offset).or. &
        any(bits32(left%basis) /= bits32(right%basis)).or. &
        any(bits64(left%height) /= bits64(right%height)).or. &
        any(bits64(left%gram) /= bits64(right%gram)).or. &
        (bits64(left%gram_error) /= bits64(right%gram_error)).or. &
        (left%fixb /= right%fixb).or.(left%norm_id /= right%norm_id).or. &
        (left%basis_type /= right%basis_type)) then
      write(*,'(A,1X,A)') 'fixed-space mismatch',trim(owner)
      error stop 'fixed rank-two package changed'
    endif
  end subroutine compare_fixed_space

  subroutine validate_snapshot(file_name,previous,current,root)
    character(len=*), intent(in) :: file_name
    type(canonical_state), intent(in) :: previous,current
    type(c_ptr), intent(out) :: root
    type(c_ptr) :: local_fluxes,local_systems,local_plane,local_system
    integer :: s,first,plane_id
    integer :: local_listdim
    real(real64) :: local_iter
    real(real32), allocatable :: local_l(:),local_system_l(:)

    call LCMOP(root,file_name,2,2,0)
    call require_character(root,'SIGNATURE','L_ARCHIVE','x2 snapshots')
    call require_record(root,'LISTDIM',1,1,'x2 snapshots')
    call LCMGET(root,'LISTDIM',local_listdim)
    if (local_listdim /= current%dims(3)) &
      error stop 'x2 snapshot count differs'
    call require_record(root,'SPOT-ITER-K',1,4,'x2 snapshots')
    call LCMGET(root,'SPOT-ITER-K',local_iter)
    if (bits64(local_iter) /= bits64(real(current%keff,real64))) &
      error stop 'x2 snapshot effective eigenvalue differs'
    call require_absent(root,'SPOT-R64','x2 snapshots')
    call require_record(root,'FLUX',local_listdim,10,'x2 snapshots')
    call require_record(root,'SYSTEM',local_listdim,10,'x2 snapshots')
    local_fluxes=LCMGID(root,'FLUX')
    local_systems=LCMGID(root,'SYSTEM')
    allocate(local_l(current%dims(2)),local_system_l(current%dims(2)))
    do s=1,local_listdim
      local_plane=LCMGIL(local_fluxes,s)
      local_system=LCMGIL(local_systems,s)
      call require_record(local_plane,'SPOT-LEAK1D',current%dims(2),2, &
        'x2 snapshot FLUX')
      call require_record(local_system,'SPOT-LEAK1D',current%dims(2),2, &
        'x2 snapshot SYSTEM')
      call require_record(local_system,'SPOT-L1-SNAP',1,1, &
        'x2 snapshot SYSTEM')
      call LCMGET(local_plane,'SPOT-LEAK1D',local_l)
      call LCMGET(local_system,'SPOT-LEAK1D',local_system_l)
      call LCMGET(local_system,'SPOT-L1-SNAP',plane_id)
      first=(s-1)*current%dims(2)+1
      if (any(bits32(local_l) /= bits32(real( &
          current%leakage(first:first+current%dims(2)-1),real32)))) &
        error stop 'x2 snapshot FLUX leakage differs from x2 state'
      if (any(bits32(local_system_l) /= bits32(real( &
          previous%leakage(first:first+current%dims(2)-1),real32)))) &
        error stop 'x2 lagged SYSTEM leakage differs from x1 state'
      if (plane_id /= s) error stop 'x2 lagged SYSTEM snapshot id differs'
    enddo
    deallocate(local_system_l,local_l)
  end subroutine validate_snapshot

  subroutine require_fresh_path(file_name)
    character(len=*), intent(in) :: file_name
    logical :: exists
    inquire(file=trim(file_name),exist=exists)
    if (exists) error stop 'output XSM path already exists'
  end subroutine require_fresh_path

  subroutine require_record(object,name,length_expected,type_expected,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,owner
    integer, intent(in) :: length_expected,type_expected
    integer :: length_found,type_found
    call LCMLEN(object,name,length_found,type_found)
    if ((length_found /= length_expected).or. &
        (type_found /= type_expected)) then
      write(*,'(A,1X,A)') trim(owner),trim(name)
      error stop 'required GANLIB record differs'
    endif
  end subroutine require_record

  subroutine require_character(object,name,expected,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,expected,owner
    character(len=12) :: found
    call require_record(object,name,3,3,owner)
    call LCMGTC(object,name,12,found)
    if (found /= expected) error stop 'required character record differs'
  end subroutine require_character

  subroutine require_absent(object,name,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,owner
    integer :: length_found,type_found
    call LCMLEN(object,name,length_found,type_found)
    if (length_found /= 0) then
      write(*,'(A,1X,A)') trim(owner),trim(name)
      error stop 'GANLIB record must be absent'
    endif
  end subroutine require_absent

  subroutine delete_if_present(object,name)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name
    integer :: length_found,type_found
    call LCMLEN(object,name,length_found,type_found)
    if (length_found /= 0) call LCMDEL(object,name)
  end subroutine delete_if_present

  pure elemental integer(int32) function bits32(value)
    real(real32), intent(in) :: value
    bits32=transfer(value,0_int32)
  end function bits32

  pure elemental integer(int64) function bits64(value)
    real(real64), intent(in) :: value
    bits64=transfer(value,0_int64)
  end function bits64

end program build_rank2_modal_aa1_candidate
