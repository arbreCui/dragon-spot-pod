program check_anderson1_trial_xsm
  ! Independent read-only Ganlib audit of the leakage-Anderson TRIAL pair.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32,int64,real32,real64
  implicit none

  integer, parameter :: nstate=40

  character(len=1024) :: paths(8)
  character(len=32) :: mode
  type(c_ptr) :: x4,x5,x6,snap6,trial_ax,trial_snap
  type(c_ptr) :: original_fluxes,trial_fluxes,original_systems,trial_systems
  type(c_ptr) :: original_plane,trial_plane,original_system,trial_system
  integer :: i,s,g,index_l,ngrp,nsnap,ncoef,narg,argument_offset
  integer :: dims4(4),dims5(4),dims6(4),dimst(4)
  integer :: rank_count,gram_count,basis_count
  integer, allocatable :: rank6(:),off6(:),goff6(:),boff6(:)
  real(real32) :: keff5,keff6,kefft
  real(real32), allocatable :: expected_l32(:),found_l32(:),original_l32(:)
  real(real64) :: rho5,rho6,rhot,numerator,denominator,gamma,weight6
  real(real64) :: iter_k6,iter_kt
  real(real64), allocatable :: h4(:),h5(:),h6(:)
  real(real64), allocatable :: a5(:),a6(:),at(:)
  real(real64), allocatable :: l4(:),l5(:),l6(:),lt(:),expected_l64(:)
  real(real64) :: f4,f5,delta
  logical :: returned_mode

  narg=command_argument_count()
  returned_mode=.false.
  argument_offset=0
  if (narg == 9) then
    call get_command_argument(1,mode)
    if (trim(mode) /= '--returned') error stop &
      'nine-argument mode requires --returned'
    returned_mode=.true.
    argument_offset=1
  else if (narg /= 6) then
    error stop &
      'expected x4 x5 x6 snap6 trial_ax trial_snap, optionally --returned and returned pair'
  endif
  do i=1,narg-argument_offset
    call get_command_argument(i+argument_offset,paths(i))
    if (len_trim(paths(i)) == 0.or.len_trim(paths(i)) > 72) &
      error stop 'XSM path is empty or exceeds GANLIB limit'
  enddo
  call LCMOP(x4,trim(paths(1)),2,2,0)
  call LCMOP(x5,trim(paths(2)),2,2,0)
  call LCMOP(x6,trim(paths(3)),2,2,0)
  call LCMOP(snap6,trim(paths(4)),2,2,0)
  call LCMOP(trial_ax,trim(paths(5)),2,2,0)
  call LCMOP(trial_snap,trim(paths(6)),2,2,0)
  call require_character(x4,'SIGNATURE','L_FLUX','x4 AX')
  call require_character(x5,'SIGNATURE','L_FLUX','x5 AX')
  call require_character(x6,'SIGNATURE','L_FLUX','x6 AX')
  call require_character(trial_ax,'SIGNATURE','L_FLUX','trial AX')
  call require_character(snap6,'SIGNATURE','L_ARCHIVE','x6 snapshots')
  call require_character(trial_snap,'SIGNATURE','L_ARCHIVE','trial snapshots')

  call read_integer_record(x4,'SPOT-X-DIMS',4,dims4,'x4 AX')
  call read_integer_record(x5,'SPOT-X-DIMS',4,dims5,'x5 AX')
  call read_integer_record(x6,'SPOT-X-DIMS',4,dims6,'x6 AX')
  call read_integer_record(trial_ax,'SPOT-X-DIMS',4,dimst,'trial AX')
  if (any(dims4 /= dims5).or.any(dims4 /= dims6).or. &
      any(dims4 /= dimst).or.dims4(1) /= 1) &
    error stop 'canonical dimensions differ'
  ngrp=dims4(2)
  nsnap=dims4(3)
  ncoef=dims4(4)
  if (ngrp /= 370.or.nsnap /= 3.or.ncoef <= 0) &
    error stop 'frozen SPOT dimensions differ'

  allocate(h4(nsnap),h5(nsnap),h6(nsnap))
  allocate(a5(ncoef),a6(ncoef),at(ncoef))
  allocate(l4(ngrp*nsnap),l5(ngrp*nsnap),l6(ngrp*nsnap))
  allocate(lt(ngrp*nsnap),expected_l64(ngrp*nsnap))
  allocate(expected_l32(ngrp*nsnap),found_l32(ngrp),original_l32(ngrp))
  call read_real64_record(x4,'SPOT-X-H',h4,'x4 AX')
  call read_real64_record(x5,'SPOT-X-H',h5,'x5 AX')
  call read_real64_record(x6,'SPOT-X-H',h6,'x6 AX')
  call read_real64_record(x5,'SPOT-X-A',a5,'x5 AX')
  call read_real64_record(x6,'SPOT-X-A',a6,'x6 AX')
  call read_real64_record(trial_ax,'SPOT-X-A',at,'trial AX')
  call read_real64_record(x4,'SPOT-X-L',l4,'x4 AX')
  call read_real64_record(x5,'SPOT-X-L',l5,'x5 AX')
  call read_real64_record(x6,'SPOT-X-L',l6,'x6 AX')
  call read_real64_record(trial_ax,'SPOT-X-L',lt,'trial AX')
  if (any(bits64(h4) /= bits64(h5)).or. &
      any(bits64(h4) /= bits64(h6)).or. &
      any(.not.ieee_is_finite(h4)).or.any(h4 <= 0.0_real64)) &
    error stop 'height metric differs or is invalid'

  numerator=0.0_real64
  denominator=0.0_real64
  do s=1,nsnap
    do g=1,ngrp
      index_l=(s-1)*ngrp+g
      f4=l5(index_l)-l4(index_l)
      f5=l6(index_l)-l5(index_l)
      delta=f5-f4
      denominator=denominator+h4(s)*delta**2
      numerator=numerator+h4(s)*delta*f5
    enddo
  enddo
  if ((.not.ieee_is_finite(denominator)).or.denominator <= 0.0_real64) &
    error stop 'leakage Anderson scalar system is invalid'
  gamma=numerator/denominator
  weight6=1.0_real64-gamma
  expected_l32=real(gamma*l5+weight6*l6,real32)
  expected_l64=real(expected_l32,real64)
  if (any(bits64(at) /= bits64(gamma*a5+weight6*a6))) &
    error stop 'trial modal coordinates differ from candidate'
  if (any(bits64(lt) /= bits64(expected_l64))) &
    error stop 'trial canonical leakage differs from publication'

  call require_character(trial_ax,'SPOT-X-STATE','TRIAL','trial AX')
  call require_character(trial_ax,'SPOT-X-CARR','X6-RAW-FLUX','trial AX')
  call require_absent(trial_ax,'SPOT-X-EPOCH','trial AX')
  call require_absent(trial_ax,'SPOT-X-RRHO','trial AX')
  call require_absent(trial_ax,'SPOT-X-RLEAK','trial AX')
  call require_absent(trial_ax,'SPOT-X-DLEAK','trial AX')
  call require_absent(trial_ax,'SPOT-X-RA','trial AX')
  call require_absent(trial_ax,'SPOT-X-PERP','trial AX')

  allocate(rank6(ngrp),off6(ngrp+1),goff6(ngrp+1),boff6(ngrp+1))
  call read_integer_record(x6,'SPOT-X-RANK',ngrp,rank6,'x6 AX')
  call read_integer_record(x6,'SPOT-X-OFF',ngrp+1,off6,'x6 AX')
  call read_integer_record(x6,'SPOT-X-GOFF',ngrp+1,goff6,'x6 AX')
  call read_integer_record(x6,'SPOT-X-BOFF',ngrp+1,boff6,'x6 AX')
  rank_count=size(rank6)
  gram_count=goff6(ngrp+1)
  basis_count=boff6(ngrp+1)
  if (rank_count /= ngrp.or.gram_count <= 0.or.basis_count <= 0) &
    error stop 'fixed-space layout is invalid'
  call compare_integer_record(x5,x6,'SPOT-X-RANK',ngrp)
  call compare_integer_record(x5,x6,'SPOT-X-OFF',ngrp+1)
  call compare_integer_record(x5,x6,'SPOT-X-GOFF',ngrp+1)
  call compare_integer_record(x5,x6,'SPOT-X-BOFF',ngrp+1)
  call compare_real32_record(x5,x6,'SPOT-X-BASIS',basis_count)
  call compare_real64_record(x5,x6,'SPOT-X-GRAM',gram_count)
  call compare_real64_record(x5,x6,'SPOT-X-H',nsnap)
  call compare_real64_record(x5,x6,'SPOT-X-GERR',1)
  call compare_integer_record(x5,x6,'SPOT-X-FIXB',1)
  call compare_character_record(x5,x6,'SPOT-X-NID')
  call compare_character_record(x5,x6,'SPOT-X-BTYP')
  call compare_integer_record(x6,trial_ax,'SPOT-X-RANK',ngrp)
  call compare_integer_record(x6,trial_ax,'SPOT-X-OFF',ngrp+1)
  call compare_integer_record(x6,trial_ax,'SPOT-X-GOFF',ngrp+1)
  call compare_integer_record(x6,trial_ax,'SPOT-X-BOFF',ngrp+1)
  call compare_real32_record(x6,trial_ax,'SPOT-X-BASIS',basis_count)
  call compare_real64_record(x6,trial_ax,'SPOT-X-GRAM',gram_count)
  call compare_real64_record(x6,trial_ax,'SPOT-X-H',nsnap)
  call compare_real64_record(x6,trial_ax,'SPOT-X-NORM',1)
  call compare_real64_record(x6,trial_ax,'SPOT-X-GERR',1)
  call compare_integer_record(x6,trial_ax,'SPOT-X-FIXB',1)
  call compare_character_record(x6,trial_ax,'SPOT-X-NID')
  call compare_character_record(x6,trial_ax,'SPOT-X-BTYP')

  call read_real32_scalar(x5,'K-EFFECTIVE',keff5,'x5 AX')
  call read_real32_scalar(x6,'K-EFFECTIVE',keff6,'x6 AX')
  call read_real32_scalar(trial_ax,'K-EFFECTIVE',kefft,'trial AX')
  call read_real64_scalar(x5,'SPOT-X-RHO',rho5,'x5 AX')
  call read_real64_scalar(x6,'SPOT-X-RHO',rho6,'x6 AX')
  call read_real64_scalar(trial_ax,'SPOT-X-RHO',rhot,'trial AX')
  if (bits32(keff5) /= bits32(keff6).or. &
      bits32(keff6) /= bits32(kefft).or. &
      bits64(rho5) /= bits64(rho6).or. &
      bits64(rho6) /= bits64(rhot).or. &
      bits64(rhot) /= bits64(1.0_real64/real(kefft,real64))) &
    error stop 'trial K-effective/rho identity differs'
  call compare_axial_raw_flux(x6,trial_ax,ngrp)

  call require_absent(trial_snap,'SPOT-R64','trial snapshots')
  call require_absent(trial_snap,'SPOT-L1-ERR','trial snapshots')
  call require_absent(trial_snap,'SPOT-PJ-PERP','trial snapshots')
  call require_absent(trial_snap,'SPOT-PROJECT','trial snapshots')
  call read_real64_scalar(snap6,'SPOT-ITER-K',iter_k6,'x6 snapshots')
  call read_real64_scalar(trial_snap,'SPOT-ITER-K',iter_kt, &
    'trial snapshots')
  if (bits64(iter_k6) /= bits64(iter_kt).or. &
      bits64(iter_kt) /= bits64(real(kefft,real64))) &
    error stop 'trial snapshot K-effective differs'

  original_fluxes=LCMGID(snap6,'FLUX')
  trial_fluxes=LCMGID(trial_snap,'FLUX')
  original_systems=LCMGID(snap6,'SYSTEM')
  trial_systems=LCMGID(trial_snap,'SYSTEM')
  do s=1,nsnap
    original_plane=LCMGIL(original_fluxes,s)
    trial_plane=LCMGIL(trial_fluxes,s)
    original_system=LCMGIL(original_systems,s)
    trial_system=LCMGIL(trial_systems,s)
    call require_absent(trial_plane,'SPOT-R64','trial snapshot FLUX')
    call read_real32_record(original_plane,'SPOT-LEAK1D',original_l32, &
      'x6 snapshot FLUX')
    call read_real32_record(trial_plane,'SPOT-LEAK1D',found_l32, &
      'trial snapshot FLUX')
    if (any(bits64(real(original_l32,real64)) /= &
        bits64(l6((s-1)*ngrp+1:s*ngrp)))) &
      error stop 'x6 snapshot leakage differs from canonical x6 L'
    if (any(bits32(found_l32) /= &
        bits32(expected_l32((s-1)*ngrp+1:s*ngrp)))) &
      error stop 'trial snapshot leakage differs from publication'
    if (any(bits64(real(found_l32,real64)) /= &
        bits64(lt((s-1)*ngrp+1:s*ngrp)))) &
      error stop 'trial snapshot and canonical leakage differ'
    call compare_real32_record(original_system,trial_system, &
      'SPOT-LEAK1D',ngrp)
    call compare_integer_record(original_system,trial_system, &
      'SPOT-L1-SNAP',1)
    call compare_plane_raw_flux(original_plane,trial_plane,ngrp)
  enddo

  write(*,'(A)') 'ANDERSON1-TRIAL FIXED-BUNDLE BITWISE PASS'
  write(*,'(A)') 'ANDERSON1-TRIAL A/RHO/L PUBLICATION BITWISE PASS'
  write(*,'(A)') 'ANDERSON1-TRIAL X6 RAW-FLUX CARRIER BITWISE PASS'
  write(*,'(A)') &
    'ANDERSON1-TRIAL LAGGED SYSTEM LEAKAGE RECORDS PRESERVED PASS'
  write(*,'(A)') 'ANDERSON1-TRIAL STALE-DIAGNOSTICS ABSENT PASS'
  write(*,'(A)') 'ANDERSON1-TRIAL COMPLETE NO-DRAGON NO-MAP'
  if (returned_mode) then
    call check_returned_pair(x6,trim(paths(7)),trim(paths(8)))
  endif

  call LCMCL(trial_snap,1)
  call LCMCL(trial_ax,1)
  call LCMCL(snap6,1)
  call LCMCL(x6,1)
  call LCMCL(x5,1)
  call LCMCL(x4,1)

contains

  subroutine check_returned_pair(reference,path_ax,path_snap)
    type(c_ptr), intent(in) :: reference
    character(len=*), intent(in) :: path_ax,path_snap
    type(c_ptr) :: returned_ax
    integer :: ig,isnap,a,b,nmode,index_a,index_b,index_g
    integer :: dims_r(4),fixb(1)
    integer, allocatable :: rank_r(:),off_r(:),goff_r(:),boff_r(:)
    real(real32) :: keff_r
    real(real64) :: rho_r,norm_r,gerr_r
    real(real64) :: defect(4),saved(4)
    real(real64) :: leak_scale,numerator_hg,denominator_hg,dcoord
    real(real64), allocatable :: a_r(:),l_r(:),h_r(:),gram_r(:),perp_r(:)

    call LCMOP(returned_ax,path_ax,2,2,0)
    call require_character(returned_ax,'SIGNATURE','L_FLUX','returned AX')
    call read_integer_record(returned_ax,'SPOT-X-DIMS',4,dims_r, &
      'returned AX')
    if (any(dims_r /= dimst)) &
      error stop 'returned canonical dimensions differ'

    allocate(rank_r(ngrp),off_r(ngrp+1),goff_r(ngrp+1), &
      boff_r(ngrp+1))
    call read_integer_record(returned_ax,'SPOT-X-RANK',ngrp,rank_r, &
      'returned AX')
    call read_integer_record(returned_ax,'SPOT-X-OFF',ngrp+1,off_r, &
      'returned AX')
    call read_integer_record(returned_ax,'SPOT-X-GOFF',ngrp+1,goff_r, &
      'returned AX')
    call read_integer_record(returned_ax,'SPOT-X-BOFF',ngrp+1,boff_r, &
      'returned AX')
    if (any(rank_r /= 1).or.off_r(1) /= 0.or.goff_r(1) /= 0.or. &
        boff_r(1) /= 0.or.off_r(ngrp+1) /= ncoef.or. &
        goff_r(ngrp+1) /= gram_count.or. &
        boff_r(ngrp+1) /= basis_count) &
      error stop 'returned fixed-rank layout is invalid'
    do ig=1,ngrp
      if (off_r(ig+1)-off_r(ig) /= nsnap.or. &
          goff_r(ig+1)-goff_r(ig) /= 1.or. &
          boff_r(ig+1) <= boff_r(ig)) &
        error stop 'returned rank-one offsets are invalid'
    enddo
    call compare_integer_record(reference,returned_ax,'SPOT-X-RANK',ngrp)
    call compare_integer_record(reference,returned_ax,'SPOT-X-OFF',ngrp+1)
    call compare_integer_record(reference,returned_ax,'SPOT-X-GOFF', &
      ngrp+1)
    call compare_integer_record(reference,returned_ax,'SPOT-X-BOFF', &
      ngrp+1)
    call compare_real32_record(reference,returned_ax,'SPOT-X-BASIS', &
      basis_count)
    call compare_real64_record(reference,returned_ax,'SPOT-X-GRAM', &
      gram_count)
    call compare_real64_record(reference,returned_ax,'SPOT-X-H',nsnap)
    call compare_real64_record(reference,returned_ax,'SPOT-X-GERR',1)
    call compare_integer_record(reference,returned_ax,'SPOT-X-FIXB',1)
    call compare_character_record(reference,returned_ax,'SPOT-X-NID')
    call compare_character_record(reference,returned_ax,'SPOT-X-BTYP')

    call require_absent(returned_ax,'SPOT-X-STATE','returned AX')
    call require_absent(returned_ax,'SPOT-X-CARR','returned AX')
    call require_absent(returned_ax,'SPOT-X-EPOCH','returned AX')
    call require_character(returned_ax,'SPOT-X-NID','NUFISS-UNIT', &
      'returned AX')
    call require_character(returned_ax,'SPOT-X-BTYP','POD-FIXED', &
      'returned AX')
    call read_integer_record(returned_ax,'SPOT-X-FIXB',1,fixb, &
      'returned AX')
    if (fixb(1) /= 1) error stop 'returned fixed-basis marker differs'

    allocate(a_r(ncoef),l_r(ngrp*nsnap),h_r(nsnap), &
      gram_r(gram_count),perp_r(ngrp*nsnap))
    call read_real64_record(returned_ax,'SPOT-X-A',a_r,'returned AX')
    call read_real64_record(returned_ax,'SPOT-X-L',l_r,'returned AX')
    call read_real64_record(returned_ax,'SPOT-X-H',h_r,'returned AX')
    call read_real64_record(returned_ax,'SPOT-X-GRAM',gram_r, &
      'returned AX')
    call read_real64_record(returned_ax,'SPOT-X-PERP',perp_r, &
      'returned AX')
    if (any(perp_r < 0.0_real64)) &
      error stop 'returned off-space norm is negative'
    call read_real64_scalar(returned_ax,'SPOT-X-NORM',norm_r, &
      'returned AX')
    call read_real64_scalar(returned_ax,'SPOT-X-GERR',gerr_r, &
      'returned AX')
    if (norm_r <= 0.0_real64.or.gerr_r < 0.0_real64) &
      error stop 'returned canonical norm metadata is invalid'

    call read_real32_scalar(returned_ax,'K-EFFECTIVE',keff_r, &
      'returned AX')
    call read_real64_scalar(returned_ax,'SPOT-X-RHO',rho_r, &
      'returned AX')
    if (keff_r <= 0.0_real32.or.rho_r <= 0.0_real64.or. &
        bits64(rho_r) /= bits64(1.0_real64/real(keff_r,real64))) &
      error stop 'returned K-effective/rho identity differs'

    call read_real64_scalar(returned_ax,'SPOT-X-RRHO',saved(1), &
      'returned AX')
    call read_real64_scalar(returned_ax,'SPOT-X-RLEAK',saved(2), &
      'returned AX')
    call read_real64_scalar(returned_ax,'SPOT-X-DLEAK',saved(3), &
      'returned AX')
    call read_real64_scalar(returned_ax,'SPOT-X-RA',saved(4), &
      'returned AX')
    if (any(saved < 0.0_real64)) &
      error stop 'returned saved defect is negative'

    defect(1)=abs(rho_r-rhot)
    defect(3)=maxval(abs(l_r-lt))
    leak_scale=max(maxval(abs(l_r)),maxval(abs(lt)))
    if (leak_scale == 0.0_real64) then
      if (defect(3) /= 0.0_real64) &
        error stop 'invalid returned zero-leakage branch'
      defect(2)=0.0_real64
    else
      defect(2)=defect(3)/leak_scale
    endif
    numerator_hg=0.0_real64
    denominator_hg=0.0_real64
    do ig=1,ngrp
      nmode=rank_r(ig)
      do isnap=1,nsnap
        do a=1,nmode
          index_a=off_r(ig)+(isnap-1)*nmode+a
          dcoord=a_r(index_a)-at(index_a)
          do b=1,nmode
            index_b=off_r(ig)+(isnap-1)*nmode+b
            index_g=goff_r(ig)+(b-1)*nmode+a
            numerator_hg=numerator_hg+h_r(isnap)*dcoord* &
              gram_r(index_g)*(a_r(index_b)-at(index_b))
            denominator_hg=denominator_hg+h_r(isnap)*a_r(index_a)* &
              gram_r(index_g)*a_r(index_b)
          enddo
        enddo
      enddo
    enddo
    if (numerator_hg < 0.0_real64.or. &
        (.not.ieee_is_finite(numerator_hg)).or. &
        denominator_hg <= 0.0_real64.or. &
        (.not.ieee_is_finite(denominator_hg))) &
      error stop 'returned HG coordinate norm is invalid'
    defect(4)=sqrt(numerator_hg/denominator_hg)
    if (any(.not.ieee_is_finite(defect)).or. &
        any(bits64(defect) /= bits64(saved))) &
      error stop 'returned recomputed defect differs bitwise'

    call check_returned_snapshot(path_snap,keff_r,l_r,saved)
    call LCMCL(returned_ax,1)
    write(*,'(A)') 'ANDERSON1-RETURNED FIXED-BUNDLE BITWISE PASS'
    write(*,'(A)') 'ANDERSON1-RETURNED STATE-CONTRACT PASS'
    write(*,'(A)') 'ANDERSON1-RETURNED RAW-DEFECT BITWISE PASS'
    write(*,'(A)') 'ANDERSON1-RETURNED RESTART-ARCHIVE BITWISE PASS'
    write(*,'(A)') 'ANDERSON1-RETURNED RAW-RADIAL-POSITIVITY PASS'
    write(*,'(A)') 'ANDERSON1-RETURNED COMPLETE'
  end subroutine check_returned_pair

  subroutine check_returned_snapshot(path,returned_keff,returned_l,saved)
    character(len=*), intent(in) :: path
    real(real32), intent(in) :: returned_keff
    real(real64), intent(in) :: returned_l(:),saved(4)
    type(c_ptr) :: root,tracks,fluxes,systems
    type(c_ptr) :: track_ptr,flux_ptr,system_ptr,radial_fluxes
    integer :: listdim,isnap,ig,nreg,nunk
    integer :: track_state(nstate),equation(1)
    integer, allocatable :: keys(:)
    real(real32) :: l1_error,fs_keff,fs_min,fs_qsum,fs_rbal
    real(real64) :: iter_keff
    real(real32), allocatable :: flux_l(:),system_l(:),radial_flux(:)
    character(len=80) :: owner

    call LCMOP(root,path,2,2,0)
    call require_character(root,'SIGNATURE','L_ARCHIVE', &
      'returned snapshots')
    call read_integer_record(root,'LISTDIM',1,equation, &
      'returned snapshots')
    listdim=equation(1)
    if (listdim /= nsnap) error stop 'returned snapshot count differs'
    call require_record(root,'TRACK',listdim,10,'returned snapshots')
    call require_record(root,'MICROLIB2',listdim,10,'returned snapshots')
    call require_record(root,'SYSTEM',listdim,10,'returned snapshots')
    call require_record(root,'FLUX',listdim,10,'returned snapshots')
    call read_real64_scalar(root,'SPOT-ITER-K',iter_keff, &
      'returned snapshots')
    call read_real32_scalar(root,'SPOT-L1-ERR',l1_error, &
      'returned snapshots')
    if (bits64(iter_keff) /= &
        bits64(real(returned_keff,real64)).or.l1_error < 0.0_real32.or. &
        bits32(l1_error) /= bits32(real(saved(3),real32))) &
      error stop 'returned snapshot root diagnostics differ'

    tracks=LCMGID(root,'TRACK')
    fluxes=LCMGID(root,'FLUX')
    systems=LCMGID(root,'SYSTEM')
    allocate(flux_l(ngrp),system_l(ngrp))
    do isnap=1,listdim
      write(owner,'(A,I0)') 'returned snapshot plane ',isnap
      call require_directory_item(tracks,isnap,trim(owner)//' TRACK')
      call require_directory_item(fluxes,isnap,trim(owner)//' FLUX')
      call require_directory_item(systems,isnap,trim(owner)//' SYSTEM')
      track_ptr=LCMGIL(tracks,isnap)
      flux_ptr=LCMGIL(fluxes,isnap)
      system_ptr=LCMGIL(systems,isnap)
      call read_integer_record(track_ptr,'STATE-VECTOR',nstate, &
        track_state,owner)
      nreg=track_state(1)
      nunk=track_state(2)
      if (nreg <= 0.or.nunk <= 0) &
        error stop 'returned radial dimensions are invalid'
      allocate(keys(nreg),radial_flux(nunk))
      call read_integer_record(track_ptr,'KEYFLX$ANIS',nreg,keys,owner)
      if (any(keys < 1).or.any(keys > nunk)) &
        error stop 'returned radial scalar keys are invalid'

      call require_character(flux_ptr,'SIGNATURE','L_FLUX',owner)
      call require_character(system_ptr,'SIGNATURE','L_PIJ',owner)
      call require_record(flux_ptr,'FLUX',ngrp,10,owner)
      radial_fluxes=LCMGID(flux_ptr,'FLUX')
      do ig=1,ngrp
        call require_list_item(radial_fluxes,ig,nunk,2,owner)
        call LCMGDL(radial_fluxes,ig,radial_flux)
        if (any(.not.ieee_is_finite(radial_flux)).or. &
            any(radial_flux(keys) <= 0.0_real32)) &
          error stop 'returned raw radial scalar flux is not positive'
      enddo

      call read_real32_record(flux_ptr,'SPOT-LEAK1D',flux_l,owner)
      call read_real32_record(system_ptr,'SPOT-LEAK1D',system_l,owner)
      if (any(bits32(flux_l) /= bits32(real(returned_l( &
          (isnap-1)*ngrp+1:isnap*ngrp),real32)))) &
        error stop 'returned FLUX leakage differs from canonical L'
      if (any(bits32(system_l) /= bits32(real(lt( &
          (isnap-1)*ngrp+1:isnap*ngrp),real32)))) &
        error stop 'returned SYSTEM leakage differs from trial L'

      call read_integer_record(flux_ptr,'SPOT-FS-EQN',1,equation,owner)
      call read_real32_scalar(flux_ptr,'SPOT-FS-K',fs_keff,owner)
      call read_real32_scalar(flux_ptr,'SPOT-FS-MIN',fs_min,owner)
      call read_real32_scalar(flux_ptr,'SPOT-FS-QSUM',fs_qsum,owner)
      call read_real32_scalar(flux_ptr,'SPOT-FS-RBAL',fs_rbal,owner)
      if (equation(1) /= 1.or.bits32(fs_keff) /= bits32(kefft).or. &
          fs_min <= 0.0_real32.or.fs_qsum <= 0.0_real32.or. &
          fs_rbal < 0.0_real32) &
        error stop 'returned fixed-source contract is invalid'
      deallocate(radial_flux,keys)
    enddo
    deallocate(system_l,flux_l)
    call LCMCL(root,1)
  end subroutine check_returned_snapshot

  subroutine require_directory_item(list_ptr,index0,owner)
    type(c_ptr), intent(in) :: list_ptr
    integer, intent(in) :: index0
    character(len=*), intent(in) :: owner
    integer :: length_found,type_found
    call LCMLEL(list_ptr,index0,length_found,type_found)
    if (length_found /= -1.or.type_found /= 0) then
      write(*,'(A)') trim(owner)
      error stop 'list item is not a directory'
    endif
  end subroutine require_directory_item

  subroutine require_list_item(list_ptr,index0,length_expected, &
      type_expected,owner)
    type(c_ptr), intent(in) :: list_ptr
    integer, intent(in) :: index0,length_expected,type_expected
    character(len=*), intent(in) :: owner
    integer :: length_found,type_found
    call LCMLEL(list_ptr,index0,length_found,type_found)
    if (length_found /= length_expected.or.type_found /= type_expected) then
      write(*,'(A)') trim(owner)
      error stop 'list item contract failed'
    endif
  end subroutine require_list_item

  subroutine require_record(object,name,length_expected,type_expected,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,owner
    integer, intent(in) :: length_expected,type_expected
    integer :: length_found,type_found
    call LCMLEN(object,name,length_found,type_found)
    if (length_found /= length_expected.or.type_found /= type_expected) then
      write(*,'(A,1X,A)') trim(owner),trim(name)
      error stop 'required GANLIB record differs'
    endif
  end subroutine require_record

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

  subroutine require_character(object,name,expected,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,expected,owner
    character(len=12) :: found
    call require_record(object,name,3,3,owner)
    call LCMGTC(object,name,12,found)
    if (found /= expected) error stop 'required character record differs'
  end subroutine require_character

  subroutine read_integer_record(object,name,n,value,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,owner
    integer, intent(in) :: n
    integer, intent(out) :: value(n)
    call require_record(object,name,n,1,owner)
    call LCMGET(object,name,value)
  end subroutine read_integer_record

  subroutine read_real32_record(object,name,value,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,owner
    real(real32), intent(out) :: value(:)
    call require_record(object,name,size(value),2,owner)
    call LCMGET(object,name,value)
    if (any(.not.ieee_is_finite(value))) error stop 'nonfinite real32 record'
  end subroutine read_real32_record

  subroutine read_real64_record(object,name,value,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,owner
    real(real64), intent(out) :: value(:)
    call require_record(object,name,size(value),4,owner)
    call LCMGET(object,name,value)
    if (any(.not.ieee_is_finite(value))) error stop 'nonfinite real64 record'
  end subroutine read_real64_record

  subroutine read_real32_scalar(object,name,value,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,owner
    real(real32), intent(out) :: value
    call require_record(object,name,1,2,owner)
    call LCMGET(object,name,value)
    if (.not.ieee_is_finite(value)) error stop 'nonfinite real32 scalar'
  end subroutine read_real32_scalar

  subroutine read_real64_scalar(object,name,value,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,owner
    real(real64), intent(out) :: value
    call require_record(object,name,1,4,owner)
    call LCMGET(object,name,value)
    if (.not.ieee_is_finite(value)) error stop 'nonfinite real64 scalar'
  end subroutine read_real64_scalar

  subroutine compare_integer_record(left,right,name,n)
    type(c_ptr), intent(in) :: left,right
    character(len=*), intent(in) :: name
    integer, intent(in) :: n
    integer, allocatable :: lv(:),rv(:)
    allocate(lv(n),rv(n))
    call read_integer_record(left,name,n,lv,'comparison left')
    call read_integer_record(right,name,n,rv,'comparison right')
    if (any(lv /= rv)) error stop 'integer records differ'
    deallocate(rv,lv)
  end subroutine compare_integer_record

  subroutine compare_real32_record(left,right,name,n)
    type(c_ptr), intent(in) :: left,right
    character(len=*), intent(in) :: name
    integer, intent(in) :: n
    real(real32), allocatable :: lv(:),rv(:)
    allocate(lv(n),rv(n))
    call read_real32_record(left,name,lv,'comparison left')
    call read_real32_record(right,name,rv,'comparison right')
    if (any(bits32(lv) /= bits32(rv))) error stop 'real32 records differ'
    deallocate(rv,lv)
  end subroutine compare_real32_record

  subroutine compare_real64_record(left,right,name,n)
    type(c_ptr), intent(in) :: left,right
    character(len=*), intent(in) :: name
    integer, intent(in) :: n
    real(real64), allocatable :: lv(:),rv(:)
    allocate(lv(n),rv(n))
    call read_real64_record(left,name,lv,'comparison left')
    call read_real64_record(right,name,rv,'comparison right')
    if (any(bits64(lv) /= bits64(rv))) error stop 'real64 records differ'
    deallocate(rv,lv)
  end subroutine compare_real64_record

  subroutine compare_character_record(left,right,name)
    type(c_ptr), intent(in) :: left,right
    character(len=*), intent(in) :: name
    character(len=12) :: lv,rv
    call require_record(left,name,3,3,'comparison left')
    call require_record(right,name,3,3,'comparison right')
    call LCMGTC(left,name,12,lv)
    call LCMGTC(right,name,12,rv)
    if (lv /= rv) error stop 'character records differ'
  end subroutine compare_character_record

  subroutine compare_axial_raw_flux(left,right,groups)
    type(c_ptr), intent(in) :: left,right
    integer, intent(in) :: groups
    type(c_ptr) :: left_flux,right_flux
    integer :: ig,nleft,nright,tleft,tright
    real(real32), allocatable :: lv(:),rv(:)
    left_flux=LCMGID(left,'FLUX')
    right_flux=LCMGID(right,'FLUX')
    do ig=1,groups
      call LCMLEL(left_flux,ig,nleft,tleft)
      call LCMLEL(right_flux,ig,nright,tright)
      if (nleft <= 0.or.nleft /= nright.or.tleft /= 2.or.tright /= 2) &
        error stop 'axial raw FLUX layout differs'
      allocate(lv(nleft),rv(nright))
      call LCMGDL(left_flux,ig,lv)
      call LCMGDL(right_flux,ig,rv)
      if (any(bits32(lv) /= bits32(rv))) &
        error stop 'axial raw FLUX carrier differs'
      deallocate(rv,lv)
    enddo
  end subroutine compare_axial_raw_flux

  subroutine compare_plane_raw_flux(left,right,groups)
    type(c_ptr), intent(in) :: left,right
    integer, intent(in) :: groups
    type(c_ptr) :: left_flux,right_flux
    integer :: ig,nleft,nright,tleft,tright
    real(real32), allocatable :: lv(:),rv(:)
    left_flux=LCMGID(left,'FLUX')
    right_flux=LCMGID(right,'FLUX')
    do ig=1,groups
      call LCMLEL(left_flux,ig,nleft,tleft)
      call LCMLEL(right_flux,ig,nright,tright)
      if (nleft <= 0.or.nleft /= nright.or.tleft /= 2.or.tright /= 2) &
        error stop 'plane raw FLUX layout differs'
      allocate(lv(nleft),rv(nright))
      call LCMGDL(left_flux,ig,lv)
      call LCMGDL(right_flux,ig,rv)
      if (any(bits32(lv) /= bits32(rv))) &
        error stop 'plane raw FLUX carrier differs'
      deallocate(rv,lv)
    enddo
  end subroutine compare_plane_raw_flux

  pure elemental integer(int32) function bits32(value)
    real(real32), intent(in) :: value
    bits32=transfer(value,0_int32)
  end function bits32

  pure elemental integer(int64) function bits64(value)
    real(real64), intent(in) :: value
    bits64=transfer(value,0_int64)
  end function bits64

end program check_anderson1_trial_xsm
