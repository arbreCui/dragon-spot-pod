program embed_rank3_closed_xsm
  ! Embed one CLOSED rank-2 canonical state in its nested rank-3 POD basis.
  !
  ! This is an offline Ganlib record transformation.  It does not call a
  ! transport, assembly, projection, or iteration routine.  The represented
  ! physical field is unchanged: modes one and two retain their exact stored
  ! bits and mode three is the positive-zero bit pattern.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  implicit none

  integer, parameter :: nstate=40, ngrp=370, nsnap=3, nreg=8
  integer, parameter :: rank2=2, rank3=3
  integer, parameter :: ncoef2=ngrp*nsnap*rank2
  integer, parameter :: ncoef3=ngrp*nsnap*rank3
  integer, parameter :: ngram2=ngrp*rank2*rank2
  integer, parameter :: ngram3=ngrp*rank3*rank3
  integer, parameter :: nbasis2=ngrp*nreg*rank2
  integer, parameter :: nbasis3=ngrp*nreg*rank3
  integer, parameter :: nplane=ngrp*nsnap
  integer, parameter :: max_path=72

  character(len=1024) :: ax_path, snap_path, basis_path, output_path
  character(len=12) :: marker
  character(len=80) :: label
  type(c_ptr) :: ax, snap, basis_root, output
  type(c_ptr) :: basis_groups, basis_group, snap_authority
  type(c_ptr) :: input_fluxes, output_fluxes
  integer :: ax_state(nstate), basis_state(nstate), output_state(nstate)
  integer :: dims2(4), dims3(4), dims_check(4)
  integer :: rank2_root(ngrp), rank3_root(ngrp), rank_check(ngrp)
  integer :: off2(ngrp+1), goff2(ngrp+1), boff2(ngrp+1)
  integer :: off3(ngrp+1), goff3(ngrp+1), boff3(ngrp+1)
  integer :: off_check(ngrp+1), goff_check(ngrp+1), boff_check(ngrp+1)
  integer :: g, p, i, a, b, old_index, new_index
  integer :: nreg_found, nsnap_found, nmode_found, fixb, epoch, snap_epoch
  integer :: listdim, reconstruction_count
  integer :: zero_status
  real(real32) :: keff32, output_keff32
  real(real32) :: group_basis(nreg,rank3), group_volume(nreg)
  real(real32), allocatable :: basis2_flat(:), basis3_flat(:)
  real(real32), allocatable :: basis_check(:), flux_input(:), flux_output(:)
  real(real64) :: keff64, output_keff64, snap_keff64
  real(real64) :: rho, output_rho, snap_rho, norm, output_norm
  real(real64) :: gram_error3, gram_error_check, weight_sum
  real(real64) :: gram_group(rank3,rank3), reconstructed2, reconstructed3
  real(real64), allocatable :: coord2(:), coord3(:), coord_check(:)
  real(real64), allocatable :: gram2_flat(:), gram3_flat(:), gram_check(:)
  real(real64), allocatable :: leakage(:), leakage_check(:)
  real(real64), allocatable :: height(:), height_check(:)
  real(real64), allocatable :: perp(:), perp_check(:)
  logical :: exists

  if (command_argument_count() /= 4) call fail( &
      'EXPECTED RANK2_AX RANK2_SNAP RANK3_BASIS FRESH_RANK3_AX.')
  call get_command_argument(1,ax_path)
  call get_command_argument(2,snap_path)
  call get_command_argument(3,basis_path)
  call get_command_argument(4,output_path)
  call validate_path(ax_path,'RANK2 AX INPUT')
  call validate_path(snap_path,'RANK2 SNAP INPUT')
  call validate_path(basis_path,'RANK3 BASIS INPUT')
  if (len_trim(output_path) == 0 .or. len_trim(output_path) > max_path) &
    call fail('OUTPUT PATH IS EMPTY OR EXCEEDS THE GANLIB LIMIT.')
  if (trim(output_path) == trim(ax_path) .or. &
      trim(output_path) == trim(snap_path) .or. &
      trim(output_path) == trim(basis_path)) &
    call fail('OUTPUT PATH MUST DIFFER FROM EVERY INPUT PATH.')
  inquire(file=trim(output_path),exist=exists)
  if (exists) call fail('OUTPUT PATH IS NOT FRESH.')

  call LCMOP(ax,trim(ax_path),2,2,0)
  call LCMOP(snap,trim(snap_path),2,2,0)
  call LCMOP(basis_root,trim(basis_path),2,2,0)

  ! Admit the fixed rank-2 CLOSED state and retain its physical quantities.
  call require_character(ax,'SIGNATURE','L_FLUX','RANK2 AX')
  call require_record(ax,'STATE-VECTOR',nstate,1,'RANK2 AX')
  call LCMGET(ax,'STATE-VECTOR',ax_state)
  if (ax_state(1) /= ngrp .or. ax_state(2) <= 0) &
    call fail('RANK2 AX HAS INVALID FLUX DIMENSIONS.')
  call require_character(ax,'SPOT-X-STATE','CLOSED','RANK2 AX')
  call require_record(ax,'SPOT-X-EPOCH',1,1,'RANK2 AX')
  call LCMGET(ax,'SPOT-X-EPOCH',epoch)
  if (epoch < 0) call fail('RANK2 AX HAS A NEGATIVE EPOCH.')
  call require_record(ax,'SPOT-X-DIMS',4,1,'RANK2 AX')
  call LCMGET(ax,'SPOT-X-DIMS',dims2)
  if (any(dims2 /= [1,ngrp,nsnap,ncoef2])) &
    call fail('RANK2 AX CANONICAL DIMENSIONS DIFFER.')
  call require_record(ax,'SPOT-X-RANK',ngrp,1,'RANK2 AX')
  call require_record(ax,'SPOT-X-OFF',ngrp+1,1,'RANK2 AX')
  call require_record(ax,'SPOT-X-GOFF',ngrp+1,1,'RANK2 AX')
  call require_record(ax,'SPOT-X-BOFF',ngrp+1,1,'RANK2 AX')
  call LCMGET(ax,'SPOT-X-RANK',rank2_root)
  call LCMGET(ax,'SPOT-X-OFF',off2)
  call LCMGET(ax,'SPOT-X-GOFF',goff2)
  call LCMGET(ax,'SPOT-X-BOFF',boff2)
  if (any(rank2_root /= rank2)) call fail('RANK2 AX IS NOT UNIFORM RANK TWO.')
  do g=1,ngrp+1
    if (off2(g) /= (g-1)*nsnap*rank2 .or. &
        goff2(g) /= (g-1)*rank2*rank2 .or. &
        boff2(g) /= (g-1)*nreg*rank2) &
      call fail('RANK2 AX HAS A NONCANONICAL OFFSET TABLE.')
  enddo
  call require_record(ax,'SPOT-X-BASIS',nbasis2,2,'RANK2 AX')
  call require_record(ax,'SPOT-X-A',ncoef2,4,'RANK2 AX')
  call require_record(ax,'SPOT-X-GRAM',ngram2,4,'RANK2 AX')
  allocate(basis2_flat(nbasis2),coord2(ncoef2),gram2_flat(ngram2))
  call LCMGET(ax,'SPOT-X-BASIS',basis2_flat)
  call LCMGET(ax,'SPOT-X-A',coord2)
  call LCMGET(ax,'SPOT-X-GRAM',gram2_flat)
  if (any(.not.ieee_is_finite(basis2_flat)) .or. &
      any(.not.ieee_is_finite(coord2)) .or. &
      any(.not.ieee_is_finite(gram2_flat))) &
    call fail('RANK2 AX HAS NON-FINITE CANONICAL DATA.')
  call require_record(ax,'SPOT-X-FIXB',1,1,'RANK2 AX')
  call LCMGET(ax,'SPOT-X-FIXB',fixb)
  if (fixb /= 1) call fail('RANK2 AX IS NOT A FIXED-BASIS STATE.')
  call require_character(ax,'SPOT-X-BTYP','POD-FIXED','RANK2 AX')
  call require_character(ax,'SPOT-X-NID','NUFISS-UNIT','RANK2 AX')
  call require_record(ax,'K-EFFECTIVE',1,2,'RANK2 AX')
  call require_record(ax,'SPOT-X-RHO',1,4,'RANK2 AX')
  call require_record(ax,'SPOT-X-L',nplane,4,'RANK2 AX')
  call require_record(ax,'SPOT-X-H',nsnap,4,'RANK2 AX')
  call require_record(ax,'SPOT-X-NORM',1,4,'RANK2 AX')
  call require_record(ax,'SPOT-X-PERP',nplane,4,'RANK2 AX')
  call require_record(ax,'SPOT-X-GERR',1,4,'RANK2 AX')
  call LCMGET(ax,'K-EFFECTIVE',keff32)
  call LCMGET(ax,'SPOT-X-RHO',rho)
  allocate(leakage(nplane),height(nsnap),perp(nplane))
  call LCMGET(ax,'SPOT-X-L',leakage)
  call LCMGET(ax,'SPOT-X-H',height)
  call LCMGET(ax,'SPOT-X-NORM',norm)
  ! PERP is inherited as the residual of this unchanged represented field.
  ! It is deliberately not advertised as a fresh optimal rank-3 projection;
  ! the first returned rank-3 SPOSTATE will recompute that diagnostic.
  call LCMGET(ax,'SPOT-X-PERP',perp)
  if (.not.ieee_is_finite(keff32) .or. keff32 <= +0.0_real32 .or. &
      .not.ieee_is_finite(rho) .or. rho <= +0.0_real64 .or. &
      .not.ieee_is_finite(norm) .or. norm <= +0.0_real64 .or. &
      any(.not.ieee_is_finite(leakage)) .or. &
      any(.not.ieee_is_finite(height)) .or. any(height <= +0.0_real64) .or. &
      any(.not.ieee_is_finite(perp)) .or. any(perp < +0.0_real64)) &
    call fail('RANK2 AX HAS INVALID PHYSICAL STATE DATA.')
  do i=1,4
    select case (i)
    case (1); marker='SPOT-X-RRHO'
    case (2); marker='SPOT-X-RLEAK'
    case (3); marker='SPOT-X-DLEAK'
    case (4); marker='SPOT-X-RA'
    end select
    call require_record(ax,trim(marker),1,4,'RANK2 AX')
  enddo

  call require_record(ax,'SPOT-X-KEFF',1,4,'RANK2 AX')
  call LCMGET(ax,'SPOT-X-KEFF',keff64)
  if (.not.ieee_is_finite(keff64) .or. keff64 <= +0.0_real64 .or. &
      real32_bits(real(keff64,real32)) /= real32_bits(keff32)) &
    call fail('RANK2 AX REAL64 EIGENVALUE MIRROR FAILED.')
  if (real64_bits(rho) /= real64_bits(1.0_real64/keff64)) &
    call fail('RANK2 AX INVERSE-EIGENVALUE IDENTITY FAILED.')

  ! The CLOSED snapshot archive is rank-neutral.  Check its shared lifecycle
  ! authority, but never copy or modify it.
  call require_character(snap,'SIGNATURE','L_ARCHIVE','RANK2 SNAP')
  call require_record(snap,'LISTDIM',1,1,'RANK2 SNAP')
  call require_record(snap,'SPOT-ITER-K',1,4,'RANK2 SNAP')
  call LCMGET(snap,'LISTDIM',listdim)
  call LCMGET(snap,'SPOT-ITER-K',snap_keff64)
  if (listdim /= nsnap .or. &
      real64_bits(snap_keff64) /= real64_bits(keff64)) &
    call fail('RANK2 SNAP DOES NOT MATCH THE AXIAL STATE.')
  snap_authority=require_directory(snap,'SPOT-R64','RANK2 SNAP')
  call require_character(snap_authority,'STATE','CLOSED', &
      'RANK2 SNAP AUTHORITY')
  call require_record(snap_authority,'EPOCH',1,1,'RANK2 SNAP AUTHORITY')
  call require_record(snap_authority,'RHO',1,4,'RANK2 SNAP AUTHORITY')
  call LCMGET(snap_authority,'EPOCH',snap_epoch)
  call LCMGET(snap_authority,'RHO',snap_rho)
  if (snap_epoch /= epoch .or. real64_bits(snap_rho) /= real64_bits(rho)) &
    call fail('RANK2 SNAP/AX CLOSED AUTHORITIES DIFFER.')

  ! Read the independently rebuilt, same-snapshot rank-3 POD package.
  call require_character(basis_root,'SIGNATURE','L_PIJ','RANK3 BASIS')
  call require_record(basis_root,'STATE-VECTOR',nstate,1,'RANK3 BASIS')
  call LCMGET(basis_root,'STATE-VECTOR',basis_state)
  if (basis_state(8) /= ngrp .or. basis_state(14) /= 1) &
    call fail('RANK3 BASIS HAS INVALID ROOT DIMENSIONS.')
  call require_record(basis_root,'SPOT-FIXB',1,1,'RANK3 BASIS')
  call LCMGET(basis_root,'SPOT-FIXB',fixb)
  if (fixb /= 0) call fail('RANK3 BASIS MUST BE POD-BUILT.')
  call require_character(basis_root,'SPOT-BTYPE','POD-BUILT','RANK3 BASIS')
  call require_record(basis_root,'POD-RANK-G',ngrp,1,'RANK3 BASIS')
  call LCMGET(basis_root,'POD-RANK-G',rank3_root)
  if (any(rank3_root /= rank3)) call fail('RANK3 BASIS IS NOT UNIFORM RANK THREE.')
  call require_record(basis_root,'GROUP',ngrp,10,'RANK3 BASIS')
  basis_groups=LCMGID(basis_root,'GROUP')
  if (.not.c_associated(basis_groups)) call fail('RANK3 BASIS GROUP LIST IS NULL.')

  dims3=[1,ngrp,nsnap,ncoef3]
  do g=1,ngrp+1
    off3(g)=(g-1)*nsnap*rank3
    goff3(g)=(g-1)*rank3*rank3
    boff3(g)=(g-1)*nreg*rank3
  enddo
  allocate(basis3_flat(nbasis3),coord3(ncoef3),gram3_flat(ngram3))
  basis3_flat=+0.0_real32
  coord3=+0.0_real64
  gram3_flat=+0.0_real64
  gram_error3=+0.0_real64

  do g=1,ngrp
    write(label,'(A,I0)') 'RANK3 BASIS GROUP ',g
    call require_list_directory(basis_groups,g,trim(label),basis_group)
    call require_record(basis_group,'NREG2D',1,1,trim(label))
    call require_record(basis_group,'NSNAP',1,1,trim(label))
    call require_record(basis_group,'POD-NMODE',1,1,trim(label))
    call LCMGET(basis_group,'NREG2D',nreg_found)
    call LCMGET(basis_group,'NSNAP',nsnap_found)
    call LCMGET(basis_group,'POD-NMODE',nmode_found)
    if (nreg_found /= nreg .or. nsnap_found /= nsnap .or. &
        nmode_found /= rank3) call fail(trim(label)//' DIMENSIONS DIFFER.')
    call require_record(basis_group,'VOL2D',nreg,2,trim(label))
    call require_record(basis_group,'POD-BASIS',nreg*rank3,2,trim(label))
    call LCMGET(basis_group,'VOL2D',group_volume)
    call LCMGET(basis_group,'POD-BASIS',group_basis)
    if (any(.not.ieee_is_finite(group_volume)) .or. &
        any(group_volume <= +0.0_real32) .or. &
        any(.not.ieee_is_finite(group_basis))) &
      call fail(trim(label)//' HAS INVALID POD DATA.')
    do a=1,rank2
      do i=1,nreg
        old_index=boff2(g)+(a-1)*nreg+i
        if (real32_bits(group_basis(i,a)) /= &
            real32_bits(basis2_flat(old_index))) &
          call fail(trim(label)//' PREFIX DIFFERS FROM RANK2 AX BITWISE.')
      enddo
    enddo
    basis3_flat(boff3(g)+1:boff3(g+1))= &
        reshape(group_basis,[nreg*rank3])

    weight_sum=sum(real(group_volume,real64))
    if (.not.ieee_is_finite(weight_sum) .or. weight_sum <= +0.0_real64) &
      call fail(trim(label)//' HAS INVALID VOLUME SUM.')
    gram_group=+0.0_real64
    do a=1,rank3
      do b=1,rank3
        do i=1,nreg
          gram_group(a,b)=gram_group(a,b)+ &
              real(group_volume(i),real64)/weight_sum* &
              real(group_basis(i,a),real64)* &
              real(group_basis(i,b),real64)
        enddo
        if (.not.ieee_is_finite(gram_group(a,b))) &
          call fail(trim(label)//' PRODUCED A NON-FINITE GRAM ENTRY.')
        new_index=goff3(g)+(b-1)*rank3+a
        gram3_flat(new_index)=gram_group(a,b)
        if (a <= rank2 .and. b <= rank2) then
          old_index=goff2(g)+(b-1)*rank2+a
          if (real64_bits(gram_group(a,b)) /= &
              real64_bits(gram2_flat(old_index))) &
            call fail(trim(label)//' GRAM PREFIX DIFFERS BITWISE.')
        endif
        if (a == b) then
          gram_error3=max(gram_error3,abs(gram_group(a,b)-1.0_real64))
        else
          gram_error3=max(gram_error3,abs(gram_group(a,b)))
        endif
      enddo
    enddo
    call require_spd(gram_group,trim(label))

    do p=1,nsnap
      do a=1,rank2
        old_index=off2(g)+(p-1)*rank2+a
        new_index=off3(g)+(p-1)*rank3+a
        coord3(new_index)=coord2(old_index)
        if (real64_bits(coord3(new_index)) /= real64_bits(coord2(old_index))) &
          call fail('RANK3 COORDINATE PREFIX COPY CHANGED A BIT.')
      enddo
      new_index=off3(g)+(p-1)*rank3+rank3
      coord3(new_index)=transfer(0_int64,+0.0_real64)
      if (real64_bits(coord3(new_index)) /= 0_int64) &
        call fail('RANK3 THIRD COORDINATE IS NOT POSITIVE ZERO.')
    enddo
  enddo

  ! Independent in-program reconstruction check using the production loop
  ! order.  The added third multiplication and addition must change no bit.
  reconstruction_count=0
  do g=1,ngrp
    do p=1,nsnap
      do i=1,nreg
        reconstructed2=+0.0_real64
        do a=1,rank2
          reconstructed2=reconstructed2+ &
              real(basis2_flat(boff2(g)+(a-1)*nreg+i),real64)* &
              coord2(off2(g)+(p-1)*rank2+a)
        enddo
        reconstructed3=+0.0_real64
        do a=1,rank3
          reconstructed3=reconstructed3+ &
              real(basis3_flat(boff3(g)+(a-1)*nreg+i),real64)* &
              coord3(off3(g)+(p-1)*rank3+a)
        enddo
        if (.not.ieee_is_finite(reconstructed2) .or. &
            reconstructed2 <= +0.0_real64 .or. &
            real64_bits(reconstructed3) /= real64_bits(reconstructed2)) &
          call fail('RANK3 EMBEDDING CHANGED A RECONSTRUCTED PHYSICAL VALUE.')
        reconstruction_count=reconstruction_count+1
      enddo
    enddo
  enddo
  if (reconstruction_count /= nreg*ngrp*nsnap) &
    call fail('RECONSTRUCTION COUNT DIFFERS.')

  ! All semantic checks precede the first caller-visible output mutation.
  call LCMOP(output,trim(output_path),0,2,0)
  call LCMEQU(ax,output)
  call replace_integer(output,'SPOT-X-DIMS',dims3)
  call replace_integer(output,'SPOT-X-RANK',rank3_root)
  call replace_integer(output,'SPOT-X-OFF',off3)
  call replace_integer(output,'SPOT-X-GOFF',goff3)
  call replace_integer(output,'SPOT-X-BOFF',boff3)
  call replace_real32(output,'SPOT-X-BASIS',basis3_flat)
  call replace_real64(output,'SPOT-X-A',coord3)
  call replace_real64(output,'SPOT-X-GRAM',gram3_flat)
  call LCMDEL(output,'SPOT-X-GERR')
  call LCMPUT(output,'SPOT-X-GERR',1,4,gram_error3)
  call LCMDEL(output,'SPOT-X-RRHO')
  call LCMDEL(output,'SPOT-X-RLEAK')
  call LCMDEL(output,'SPOT-X-DLEAK')
  call LCMDEL(output,'SPOT-X-RA')
  call LCMCL(output,1)

  ! Reopen the output read-only and verify both changed and inherited records.
  call LCMOP(output,trim(output_path),2,2,0)
  call require_character(output,'SIGNATURE','L_FLUX','RANK3 OUTPUT')
  call require_character(output,'SPOT-X-STATE','CLOSED','RANK3 OUTPUT')
  call require_character(output,'SPOT-X-BTYP','POD-FIXED','RANK3 OUTPUT')
  call require_character(output,'SPOT-X-NID','NUFISS-UNIT','RANK3 OUTPUT')
  call require_record(output,'STATE-VECTOR',nstate,1,'RANK3 OUTPUT')
  call LCMGET(output,'STATE-VECTOR',output_state)
  if (any(output_state /= ax_state)) &
    call fail('RANK3 OUTPUT CHANGED THE FLUX STATE VECTOR.')
  call require_record(output,'SPOT-X-EPOCH',1,1,'RANK3 OUTPUT')
  call LCMGET(output,'SPOT-X-EPOCH',snap_epoch)
  if (snap_epoch /= epoch) call fail('RANK3 OUTPUT CHANGED THE CLOSED EPOCH.')
  call require_record(output,'SPOT-X-DIMS',4,1,'RANK3 OUTPUT')
  call require_record(output,'SPOT-X-RANK',ngrp,1,'RANK3 OUTPUT')
  call require_record(output,'SPOT-X-OFF',ngrp+1,1,'RANK3 OUTPUT')
  call require_record(output,'SPOT-X-GOFF',ngrp+1,1,'RANK3 OUTPUT')
  call require_record(output,'SPOT-X-BOFF',ngrp+1,1,'RANK3 OUTPUT')
  call LCMGET(output,'SPOT-X-DIMS',dims_check)
  call LCMGET(output,'SPOT-X-RANK',rank_check)
  call LCMGET(output,'SPOT-X-OFF',off_check)
  call LCMGET(output,'SPOT-X-GOFF',goff_check)
  call LCMGET(output,'SPOT-X-BOFF',boff_check)
  if (any(dims_check /= dims3) .or. any(rank_check /= rank3_root) .or. &
      any(off_check /= off3) .or. any(goff_check /= goff3) .or. &
      any(boff_check /= boff3)) &
    call fail('RANK3 OUTPUT LAYOUT ROUND TRIP FAILED.')
  allocate(basis_check(nbasis3),coord_check(ncoef3),gram_check(ngram3))
  call require_record(output,'SPOT-X-BASIS',nbasis3,2,'RANK3 OUTPUT')
  call require_record(output,'SPOT-X-A',ncoef3,4,'RANK3 OUTPUT')
  call require_record(output,'SPOT-X-GRAM',ngram3,4,'RANK3 OUTPUT')
  call LCMGET(output,'SPOT-X-BASIS',basis_check)
  call LCMGET(output,'SPOT-X-A',coord_check)
  call LCMGET(output,'SPOT-X-GRAM',gram_check)
  if (any(real32_bits(basis_check) /= real32_bits(basis3_flat)) .or. &
      any(real64_bits(coord_check) /= real64_bits(coord3)) .or. &
      any(real64_bits(gram_check) /= real64_bits(gram3_flat))) &
    call fail('RANK3 OUTPUT CANONICAL ARRAYS CHANGED ON DISK.')
  zero_status=0
  do g=1,ngrp
    do p=1,nsnap
      if (real64_bits(coord_check(off3(g)+(p-1)*rank3+rank3)) /= 0_int64) &
        zero_status=zero_status+1
    enddo
  enddo
  if (zero_status /= 0) call fail('RANK3 OUTPUT CONTAINS A NON-POSITIVE ZERO MODE.')
  call require_record(output,'SPOT-X-GERR',1,4,'RANK3 OUTPUT')
  call LCMGET(output,'SPOT-X-GERR',gram_error_check)
  if (real64_bits(gram_error_check) /= real64_bits(gram_error3)) &
    call fail('RANK3 OUTPUT GRAM ERROR CHANGED ON DISK.')
  call require_absent(output,'SPOT-X-RRHO','RANK3 OUTPUT')
  call require_absent(output,'SPOT-X-RLEAK','RANK3 OUTPUT')
  call require_absent(output,'SPOT-X-DLEAK','RANK3 OUTPUT')
  call require_absent(output,'SPOT-X-RA','RANK3 OUTPUT')

  allocate(leakage_check(nplane),height_check(nsnap),perp_check(nplane))
  call require_record(output,'K-EFFECTIVE',1,2,'RANK3 OUTPUT')
  call require_record(output,'SPOT-X-RHO',1,4,'RANK3 OUTPUT')
  call require_record(output,'SPOT-X-L',nplane,4,'RANK3 OUTPUT')
  call require_record(output,'SPOT-X-H',nsnap,4,'RANK3 OUTPUT')
  call require_record(output,'SPOT-X-NORM',1,4,'RANK3 OUTPUT')
  call require_record(output,'SPOT-X-PERP',nplane,4,'RANK3 OUTPUT')
  call LCMGET(output,'K-EFFECTIVE',output_keff32)
  call LCMGET(output,'SPOT-X-RHO',output_rho)
  call LCMGET(output,'SPOT-X-L',leakage_check)
  call LCMGET(output,'SPOT-X-H',height_check)
  call LCMGET(output,'SPOT-X-NORM',output_norm)
  call LCMGET(output,'SPOT-X-PERP',perp_check)
  if (real32_bits(output_keff32) /= real32_bits(keff32) .or. &
      real64_bits(output_rho) /= real64_bits(rho) .or. &
      real64_bits(output_norm) /= real64_bits(norm) .or. &
      any(real64_bits(leakage_check) /= real64_bits(leakage)) .or. &
      any(real64_bits(height_check) /= real64_bits(height)) .or. &
      any(real64_bits(perp_check) /= real64_bits(perp))) &
    call fail('RANK3 OUTPUT CHANGED AN INHERITED PHYSICAL STATE RECORD.')
  call require_record(output,'SPOT-X-KEFF',1,4,'RANK3 OUTPUT')
  call LCMGET(output,'SPOT-X-KEFF',output_keff64)
  if (real64_bits(output_keff64) /= real64_bits(keff64)) &
    call fail('RANK3 OUTPUT CHANGED THE REAL64 EIGENVALUE.')

  ! LCMEQU must preserve the underlying warm axial flux bit for bit.
  call require_record(ax,'FLUX',ngrp,10,'RANK2 AX')
  call require_record(output,'FLUX',ngrp,10,'RANK3 OUTPUT')
  input_fluxes=LCMGID(ax,'FLUX')
  output_fluxes=LCMGID(output,'FLUX')
  if (.not.c_associated(input_fluxes) .or. .not.c_associated(output_fluxes)) &
    call fail('AXIAL FLUX LIST IS NULL.')
  allocate(flux_input(ax_state(2)),flux_output(ax_state(2)))
  do g=1,ngrp
    write(label,'(A,I0)') 'AXIAL FLUX GROUP ',g
    call require_list_record(input_fluxes,g,ax_state(2),2,trim(label)//' INPUT')
    call require_list_record(output_fluxes,g,ax_state(2),2,trim(label)//' OUTPUT')
    call LCMGDL(input_fluxes,g,flux_input)
    call LCMGDL(output_fluxes,g,flux_output)
    if (any(real32_bits(flux_input) /= real32_bits(flux_output))) &
      call fail(trim(label)//' CHANGED BITWISE.')
  enddo

  call LCMCL(output,1)
  call LCMCL(basis_root,1)
  call LCMCL(snap,1)
  call LCMCL(ax,1)

  write(*,'(A,I0,A,I0,A,I0)') 'RANK3-EMBED GROUPS=',ngrp, &
      ' PLANES=',nsnap,' REGIONS=',nreg
  write(*,'(A)') 'RANK3-EMBED PREFIX-BITWISE PASS'
  write(*,'(A)') 'RANK3-EMBED MODE3-POSITIVE-ZERO PASS'
  write(*,'(A,I0,A,I0,A)') 'RANK3-EMBED RECONSTRUCTION ', &
      reconstruction_count,'/',nreg*ngrp*nsnap,' BITWISE PASS'
  write(*,'(A)') 'RANK3-EMBED PHYSICAL-STATE-BITWISE PASS'
  write(*,'(A)') 'RANK3-EMBED SNAPSHOT-REUSED-READ-ONLY PASS'
  write(*,'(A)') 'RANK3-EMBED OLD-DEFECTS-REMOVED PASS'
  write(*,'(A)') 'RANK3-EMBED COMPLETE NO-TRANSPORT'

contains

  subroutine validate_path(path,label0)
    character(len=*), intent(in) :: path,label0
    logical :: found
    if (len_trim(path) == 0 .or. len_trim(path) > max_path) &
      call fail(trim(label0)//' PATH IS EMPTY OR EXCEEDS THE GANLIB LIMIT.')
    inquire(file=trim(path),exist=found)
    if (.not.found) call fail(trim(label0)//' DOES NOT EXIST.')
  end subroutine validate_path

  subroutine require_record(ptr,name,length_expected,type_expected,label0)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,label0
    integer, intent(in) :: length_expected,type_expected
    integer :: length_found,type_found
    call LCMLEN(ptr,name,length_found,type_found)
    if (length_found /= length_expected .or. type_found /= type_expected) &
      call fail(trim(label0)//' INVALID RECORD '//trim(name)//'.')
  end subroutine require_record

  subroutine require_absent(ptr,name,label0)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,label0
    integer :: length_found,type_found
    call LCMLEN(ptr,name,length_found,type_found)
    if (length_found /= 0) &
      call fail(trim(label0)//' UNEXPECTED RECORD '//trim(name)//'.')
  end subroutine require_absent

  subroutine require_character(ptr,name,expected,label0)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,expected,label0
    character(len=12) :: found
    call require_record(ptr,name,3,3,label0)
    found=' '
    call LCMGTC(ptr,name,12,found)
    if (found /= expected) &
      call fail(trim(label0)//' UNEXPECTED CHARACTER RECORD '//trim(name)//'.')
  end subroutine require_character

  function require_directory(ptr,name,label0) result(directory)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,label0
    type(c_ptr) :: directory
    call require_record(ptr,name,-1,0,label0)
    directory=LCMGID(ptr,name)
    if (.not.c_associated(directory)) &
      call fail(trim(label0)//' NULL DIRECTORY '//trim(name)//'.')
  end function require_directory

  subroutine require_list_directory(list,index0,label0,directory)
    type(c_ptr), intent(in) :: list
    integer, intent(in) :: index0
    character(len=*), intent(in) :: label0
    type(c_ptr), intent(out) :: directory
    integer :: length_found,type_found
    call LCMLEL(list,index0,length_found,type_found)
    if (length_found /= -1 .or. type_found /= 0) &
      call fail(trim(label0)//' IS NOT A DIRECTORY.')
    directory=LCMGIL(list,index0)
    if (.not.c_associated(directory)) call fail(trim(label0)//' IS NULL.')
  end subroutine require_list_directory

  subroutine require_list_record(list,index0,length_expected,type_expected, &
      label0)
    type(c_ptr), intent(in) :: list
    integer, intent(in) :: index0,length_expected,type_expected
    character(len=*), intent(in) :: label0
    integer :: length_found,type_found
    call LCMLEL(list,index0,length_found,type_found)
    if (length_found /= length_expected .or. type_found /= type_expected) &
      call fail(trim(label0)//' HAS AN INVALID LIST ITEM.')
  end subroutine require_list_record

  subroutine replace_integer(ptr,name,values)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name
    integer, intent(in) :: values(:)
    call LCMDEL(ptr,name)
    call LCMPUT(ptr,name,size(values),1,values)
  end subroutine replace_integer

  subroutine replace_real32(ptr,name,values)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name
    real(real32), intent(in) :: values(:)
    call LCMDEL(ptr,name)
    call LCMPUT(ptr,name,size(values),2,values)
  end subroutine replace_real32

  subroutine replace_real64(ptr,name,values)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name
    real(real64), intent(in) :: values(:)
    call LCMDEL(ptr,name)
    call LCMPUT(ptr,name,size(values),4,values)
  end subroutine replace_real64

  subroutine require_spd(matrix,label0)
    ! Match SPOSTATE's strict Cholesky admission: no fitted condition-number
    ! threshold, only finite strictly positive pivots.
    real(real64), intent(in) :: matrix(:,:)
    character(len=*), intent(in) :: label0
    real(real64) :: lower(size(matrix,1),size(matrix,2)),pivot
    integer :: row,col,k
    if (size(matrix,1) /= size(matrix,2)) &
      call fail(trim(label0)//' GRAM MATRIX IS NOT SQUARE.')
    lower=+0.0_real64
    do row=1,size(matrix,1)
      do col=1,row
        pivot=matrix(row,col)
        do k=1,col-1
          pivot=pivot-lower(row,k)*lower(col,k)
        enddo
        if (row == col) then
          if (.not.ieee_is_finite(pivot) .or. pivot <= +0.0_real64) &
            call fail(trim(label0)//' GRAM MATRIX IS NOT POSITIVE DEFINITE.')
          lower(row,col)=sqrt(pivot)
        else
          lower(row,col)=pivot/lower(col,col)
        endif
      enddo
    enddo
  end subroutine require_spd

  pure elemental integer(int32) function real32_bits(value)
    real(real32), intent(in) :: value
    real32_bits=transfer(value,0_int32)
  end function real32_bits

  pure elemental integer(int64) function real64_bits(value)
    real(real64), intent(in) :: value
    real64_bits=transfer(value,0_int64)
  end function real64_bits

  subroutine fail(message)
    character(len=*), intent(in) :: message
    write(0,'(A)') 'RANK3-EMBED ERROR: '//trim(message)
    error stop 2
  end subroutine fail

end program embed_rank3_closed_xsm
