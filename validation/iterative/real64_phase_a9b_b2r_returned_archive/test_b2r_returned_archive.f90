program TEST_B2R_RETURNED_ARCHIVE
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_null_ptr, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use SPOR64_B2R, only : SPOR64_B2R_COLLECT, &
      SPOR64_B2R_PREFLIGHT_FAILED, SPOR64_B2R_RETURNED
  implicit none

  integer, parameter :: NSNAP=3, NGRP=370, NUNK=14, NREG=8
  integer, parameter :: NSTATE=40, NMAT=8
  integer(int32), parameter :: EPS_BITS=int(z'348637bd',int32)
  integer :: status, rejection_count, object_counter, p
  character(len=1024) :: output_path
  logical :: output_exists
  real(real64) :: k64, rho64
  type(c_ptr) :: assembled, solved_by_plane(NSNAP)
  type(c_ptr) :: source_by_plane(NSNAP)
  type(c_ptr) :: solved_call(NSNAP), source_call(NSNAP)
  type(c_ptr) :: output, output_xsm

  if (command_argument_count() /= 1) &
    error stop 'expected one fresh OUTPUT XSM path'
  call get_command_argument(1,output_path)
  inquire(file=trim(output_path),exist=output_exists)
  if (output_exists) error stop 'OUTPUT XSM path already exists'

  object_counter=0
  rejection_count=0
  k64=nearest(1.25_real64,+1.0_real64)
  rho64=1.0_real64/k64
  if (transfer(rho64,0_int64) == &
      transfer(real(real(rho64,real32),real64),0_int64)) &
    error stop 'synthetic RHO lacks a REAL64-only witness'

  call BUILD_ASSEMBLED(assembled,k64,rho64)
  do p=1,NSNAP
    call BUILD_SOLVED(solved_by_plane(p),p,rho64)
    call BUILD_SOURCE(source_by_plane(p),p,k64,rho64)
  end do

  ! The two detached collections deliberately arrive in different orders.
  ! A conforming collector uses their PLANE labels, never caller positions.
  solved_call=[solved_by_plane(3),solved_by_plane(1),solved_by_plane(2)]
  source_call=[source_by_plane(2),source_by_plane(3),source_by_plane(1)]
  call VERIFY_CANONICAL_INPUTS(assembled,solved_by_plane,source_by_plane, &
      k64,rho64)

  call RUN_REJECTION_SET(assembled,solved_call,source_call,k64,rho64, &
      rejection_count)
  call VERIFY_CANONICAL_INPUTS(assembled,solved_by_plane,source_by_plane, &
      k64,rho64)

  call OPEN_FRESH('OUTPUT',output)
  call SPOR64_B2R_COLLECT(output,assembled,solved_call,source_call,status)
  if (status /= SPOR64_B2R_RETURNED) &
    error stop 'canonical label-reordered collection was rejected'
  call VERIFY_RETURNED_BRIEF(output,rho64)
  call VERIFY_CANONICAL_INPUTS(assembled,solved_by_plane,source_by_plane, &
      k64,rho64)

  call LCMOP(output_xsm,trim(output_path),0,2,0)
  if (.not. c_associated(output_xsm)) &
    error stop 'fresh OUTPUT XSM could not be created'
  call LCMEQU(output,output_xsm)
  call LCMCL(output_xsm,1)

  call LCMCL(output,2)
  do p=1,NSNAP
    call LCMCL(source_by_plane(p),2)
    call LCMCL(solved_by_plane(p),2)
  end do
  call LCMCL(assembled,2)

  write(*,'(A)') 'B2R RETURNED-ARCHIVE SYNTHETIC PASS'
  write(*,'(A)') 'B2R SOLVED-ORDER=3,1,2 SOURCE-ORDER=2,3,1'
  write(*,'(A,I0,A,I0)') 'B2R COLLECTOR-ACCEPTED=',1, &
      ' REJECTIONS=',rejection_count
  write(*,'(A)') 'B2R ROOT=RETURNED/1 ROOT-RHO=ABSENT ROOT-K=ABSENT'
  write(*,'(A)') 'B2R AX-NEXT=ABSENT CLOSED=ABSENT CHILD-PLANE=ABSENT'
  write(*,'(A)') 'B2R DRAGON=0 ASM=0 SPOASM=0 FLU=0 TRANSPORT=0 PICARD=0'

contains

  subroutine BUILD_ASSEMBLED(root,k_value,rho_value)
    type(c_ptr), intent(out) :: root
    real(real64), intent(in) :: k_value, rho_value
    integer :: ip, ig
    integer :: state(NSTATE), key(NREG)
    real(real32) :: leakage(NGRP), witness
    type(c_ptr) :: tracks, libraries, systems, seeds, item
    type(c_ptr) :: groups, group, authority, seed_authority

    call OPEN_FRESH('ASSEMBLED',root)
    call PUT_CHARACTER(root,'SIGNATURE',12,'L_ARCHIVE')
    call LCMPUT(root,'LISTDIM',1,1,NSNAP)
    call LCMPUT(root,'SPOT-ITER-K',1,4,k_value)
    tracks=LCMLID(root,'TRACK',NSNAP)
    libraries=LCMLID(root,'MICROLIB2',NSNAP)
    systems=LCMLID(root,'SYSTEM',NSNAP)
    seeds=LCMLID(root,'FLUX',NSNAP)
    if (.not. all([c_associated(tracks),c_associated(libraries), &
        c_associated(systems),c_associated(seeds)])) &
      error stop 'assembled list creation failed'

    do ip=1,NSNAP
      call PLANE_KEY(ip,key)
      call PLANE_LEAKAGE(ip,leakage)

      item=LCMDIL(tracks,ip)
      call REQUIRE_ASSOCIATED(item,'TRACK item')
      call PUT_CHARACTER(item,'SIGNATURE',12,'L_TRACK')
      call LCMPUT(item,'KEYFLX',NREG,1,key)
      call LCMPUT(item,'KEYFLX$ANIS',NREG,1,key)
      call LCMPUT(item,'B2R-ID',1,1,ip)

      item=LCMDIL(libraries,ip)
      call REQUIRE_ASSOCIATED(item,'MICROLIB2 item')
      call PUT_CHARACTER(item,'SIGNATURE',12,'L_LIBRARY')
      call LCMPUT(item,'B2R-ID',1,1,ip)

      item=LCMDIL(systems,ip)
      call REQUIRE_ASSOCIATED(item,'SYSTEM item')
      call PUT_CHARACTER(item,'SIGNATURE',12,'L_PIJ')
      call PUT_CHARACTER(item,'LINK.MACRO',12,'MACRO0')
      call PUT_CHARACTER(item,'LINK.TRACK',12,'TRACK')
      state=0
      state([1,2,3,5,6,11])=1
      state(7)=4
      state(8)=NGRP
      state(9)=NUNK
      state(10)=NMAT
      call LCMPUT(item,'STATE-VECTOR',NSTATE,1,state)
      call LCMPUT(item,'SPOT-LEAK1D',NGRP,2,leakage)
      call LCMPUT(item,'SPOT-L1-SNAP',1,1,ip)
      groups=LCMLID(item,'GROUP',NGRP)
      call REQUIRE_ASSOCIATED(groups,'SYSTEM GROUP list')
      do ig=1,NGRP
        group=LCMDIL(groups,ig)
        call REQUIRE_ASSOCIATED(group,'SYSTEM GROUP item')
        witness=real(ip*100000+ig,real32)
        call LCMPUT(group,'B2R-WITNESS',1,2,witness)
      end do
      authority=LCMDID(item,'SPOT-R64')
      call REQUIRE_ASSOCIATED(authority,'SYSTEM authority')
      call LCMPUT(authority,'RHO',1,4,rho_value)
      call PUT_CHARACTER(authority,'STATE',12,'ASSEMBLED')
      call LCMPUT(authority,'EPOCH',1,1,1)

      item=LCMDIL(seeds,ip)
      call REQUIRE_ASSOCIATED(item,'parent FLUX item')
      call LCMPUT(item,'B2R-PARENT',1,1,ip)
      seed_authority=LCMDID(item,'SPOT-R64')
      call REQUIRE_ASSOCIATED(seed_authority,'parent FLUX authority')
      call LCMPUT(seed_authority,'RHO',1,4,rho_value)
      call PUT_CHARACTER(seed_authority,'STATE',12,'PROJECTED')
      call LCMPUT(seed_authority,'EPOCH',1,1,1)
    end do

    authority=LCMDID(root,'SPOT-R64')
    call REQUIRE_ASSOCIATED(authority,'assembled root authority')
    call LCMPUT(authority,'RHO',1,4,rho_value)
    call LCMPUT(authority,'NPLANE',1,1,NSNAP)
    call PUT_CHARACTER(authority,'STATE',12,'ASSEMBLED')
    call LCMPUT(authority,'EPOCH',1,1,1)
  end subroutine BUILD_ASSEMBLED


  subroutine BUILD_SOLVED(root,plane,rho_value)
    type(c_ptr), intent(out) :: root
    integer, intent(in) :: plane
    real(real64), intent(in) :: rho_value
    integer :: g, state(NSTATE), imerge(NMAT), key(NREG)
    real(real32) :: eps(5), leakage(NGRP)
    real(real32) :: flux32(NUNK), source32(NUNK)
    real(real64) :: flux64(NUNK), source64(NUNK)
    type(c_ptr) :: authority, authority_flux, authority_source
    type(c_ptr) :: mirror_flux, mirror_source

    call OPEN_FRESH('SOLVED',root)
    call PLANE_KEY(plane,key)
    call PLANE_LEAKAGE(plane,leakage)
    state=0
    state(1)=NGRP
    state(2)=NUNK
    state(3)=1
    state(8)=3
    state(9)=3
    state(10)=1
    state(11)=740
    state(12)=500
    state(17)=NMAT
    state(18)=1
    eps=[transfer(EPS_BITS,0.0_real32), &
         transfer(EPS_BITS,0.0_real32), &
         transfer(EPS_BITS,0.0_real32),+0.0_real32,+0.0_real32]
    imerge=1

    call PUT_CHARACTER(root,'SIGNATURE',12,'L_FLUX')
    call LCMPUT(root,'STATE-VECTOR',NSTATE,1,state)
    call LCMPUT(root,'EPS-CONVERGE',5,2,eps)
    call LCMPUT(root,'IMERGE-LEAK',NMAT,1,imerge)
    call LCMPUT(root,'KEYFLX',NREG,1,key)
    call PUT_CHARACTER(root,'OPTION',4,'B0  ')
    call PUT_CHARACTER(root,'LINK.MACRO',12,'MACRO0')
    call PUT_CHARACTER(root,'LINK.TRACK',12,'TRACK')
    call PUT_CHARACTER(root,'LINK.SYSTEM',12,'SYSTEM')
    call LCMPUT(root,'SPOT-LEAK1D',NGRP,2,leakage)

    mirror_flux=LCMLID(root,'FLUX',NGRP)
    mirror_source=LCMLID(root,'SOUR',NGRP)
    authority=LCMDID(root,'SPOT-R64')
    call REQUIRE_ASSOCIATED(authority,'SOLVED authority')
    call LCMPUT(authority,'RHO',1,4,rho_value)
    call LCMPUT(authority,'PLANE',1,1,plane)
    authority_flux=LCMLID(authority,'FLUX',NGRP)
    authority_source=LCMLID(authority,'SOUR',NGRP)
    call REQUIRE_ASSOCIATED(mirror_flux,'SOLVED mirror FLUX')
    call REQUIRE_ASSOCIATED(mirror_source,'SOLVED mirror SOUR')
    call REQUIRE_ASSOCIATED(authority_flux,'SOLVED authority FLUX')
    call REQUIRE_ASSOCIATED(authority_source,'SOLVED authority SOUR')
    do g=1,NGRP
      call EXPECTED_VECTOR64(1,plane,g,flux64)
      call EXPECTED_VECTOR64(2,plane,g,source64)
      flux32=real(flux64,real32)
      source32=real(source64,real32)
      call LCMPDL(mirror_flux,g,NUNK,2,flux32)
      call LCMPDL(mirror_source,g,NUNK,2,source32)
      call LCMPDL(authority_flux,g,NUNK,4,flux64)
      call LCMPDL(authority_source,g,NUNK,4,source64)
    end do
    call PUT_CHARACTER(authority,'STATE',12,'SOLVED')
    call LCMPUT(authority,'EPOCH',1,1,1)
  end subroutine BUILD_SOLVED


  subroutine BUILD_SOURCE(root,plane,k_value,rho_value)
    type(c_ptr), intent(out) :: root
    integer, intent(in) :: plane
    real(real64), intent(in) :: k_value, rho_value
    integer :: g, state(NSTATE)
    real(real32) :: k32, q32(NUNK), qint(NGRP)
    real(real64) :: q64(NUNK)
    type(c_ptr) :: dsour_outer, dsour_inner, authority, qfiss

    call OPEN_FRESH('SOURCE',root)
    k32=real(k_value,real32)
    state=0
    state(1:3)=[NGRP,NUNK,1]
    call PUT_CHARACTER(root,'SIGNATURE',12,'L_SOURCE')
    call LCMPUT(root,'STATE-VECTOR',NSTATE,1,state)
    call LCMPUT(root,'SPOT-FROZEN',1,1,1)
    call LCMPUT(root,'SPOT-KEFF',1,2,k32)
    do g=1,NGRP
      qint(g)=real(plane*100000+g,real32)
    end do
    call LCMPUT(root,'SPOT-QINT',NGRP,2,qint)
    dsour_outer=LCMLID(root,'DSOUR',1)
    call REQUIRE_ASSOCIATED(dsour_outer,'SOURCE DSOUR outer')
    dsour_inner=LCMLIL(dsour_outer,1,NGRP)
    call REQUIRE_ASSOCIATED(dsour_inner,'SOURCE DSOUR inner')

    authority=LCMDID(root,'SPOT-R64')
    call REQUIRE_ASSOCIATED(authority,'SOURCE authority')
    call LCMPUT(authority,'RHO',1,4,rho_value)
    call LCMPUT(authority,'PLANE',1,1,plane)
    call PUT_CHARACTER(authority,'STATE',12,'FROZEN-QFIS')
    qfiss=LCMLID(authority,'QFISS',NGRP)
    call REQUIRE_ASSOCIATED(qfiss,'SOURCE QFISS')
    do g=1,NGRP
      call EXPECTED_VECTOR64(3,plane,g,q64)
      q32=real(q64,real32)
      call LCMPDL(dsour_inner,g,NUNK,2,q32)
      call LCMPDL(qfiss,g,NUNK,4,q64)
    end do
    call LCMPUT(authority,'EPOCH',1,1,1)
  end subroutine BUILD_SOURCE


  subroutine RUN_REJECTION_SET(parent,solved,source,k_value,rho_value,count)
    type(c_ptr), intent(in) :: parent, solved(NSNAP), source(NSNAP)
    real(real64), intent(in) :: k_value, rho_value
    integer, intent(inout) :: count
    type(c_ptr) :: trial_solved(NSNAP), trial_source(NSNAP)
    type(c_ptr) :: bad, bad_parent, authority, systems, system
    type(c_ptr) :: tracks, track
    type(c_ptr) :: outer, inner, output_bad
    integer :: marker, bad_key(NREG)
    real(real32) :: values32(NUNK), leakage(NGRP), bad_k32
    real(real64) :: bad_rho64

    trial_solved=solved
    trial_source=source
    call CLONE_ROOT(solved(1),'BAD-SOLVED',bad)
    authority=LCMGID(bad,'SPOT-R64')
    call LCMPUT(authority,'PLANE',1,1,3)
    trial_solved(2)=bad
    call EXPECT_REJECTION(parent,trial_solved,source,count)
    call LCMCL(bad,2)

    call CLONE_ROOT(parent,'BAD-PARENT',bad_parent)
    tracks=LCMGID(bad_parent,'TRACK')
    track=LCMGIL(tracks,1)
    call LCMGET(track,'KEYFLX',bad_key)
    bad_key(1:2)=[bad_key(2),bad_key(1)]
    call LCMPUT(track,'KEYFLX',NREG,1,bad_key)
    call EXPECT_REJECTION(bad_parent,solved,source,count)
    call LCMCL(bad_parent,2)

    trial_solved=solved
    trial_source=source
    call CLONE_ROOT(source(1),'BAD-SOURCE',bad)
    authority=LCMGID(bad,'SPOT-R64')
    call LCMPUT(authority,'PLANE',1,1,2)
    trial_source(3)=bad
    call EXPECT_REJECTION(parent,solved,trial_source,count)
    call LCMCL(bad,2)

    trial_solved=solved
    call CLONE_ROOT(solved(1),'BAD-SOLVED',bad)
    authority=LCMGID(bad,'SPOT-R64')
    call LCMPUT(authority,'PLANE',1,1,0)
    trial_solved(2)=bad
    call EXPECT_REJECTION(parent,trial_solved,source,count)
    call LCMCL(bad,2)

    trial_source=source
    call CLONE_ROOT(source(1),'BAD-SOURCE',bad)
    authority=LCMGID(bad,'SPOT-R64')
    call LCMPUT(authority,'PLANE',1,1,4)
    trial_source(3)=bad
    call EXPECT_REJECTION(parent,solved,trial_source,count)
    call LCMCL(bad,2)

    trial_solved=solved
    call CLONE_ROOT(solved(2),'BAD-SOLVED',bad)
    authority=LCMGID(bad,'SPOT-R64')
    bad_rho64=nearest(rho_value,+1.0_real64)
    call LCMPUT(authority,'RHO',1,4,bad_rho64)
    trial_solved(2)=bad
    call EXPECT_REJECTION(parent,trial_solved,source,count)
    call LCMCL(bad,2)

    trial_source=source
    call CLONE_ROOT(source(2),'BAD-SOURCE',bad)
    authority=LCMGID(bad,'SPOT-R64')
    call LCMPUT(authority,'EPOCH',1,1,2)
    trial_source(2)=bad
    call EXPECT_REJECTION(parent,solved,trial_source,count)
    call LCMCL(bad,2)

    trial_source=source
    call CLONE_ROOT(source(3),'BAD-SOURCE',bad)
    bad_k32=nearest(real(k_value,real32),+1.0_real32)
    call LCMPUT(bad,'SPOT-KEFF',1,2,bad_k32)
    trial_source(3)=bad
    call EXPECT_REJECTION(parent,solved,trial_source,count)
    call LCMCL(bad,2)

    trial_source=source
    call CLONE_ROOT(source(1),'BAD-SOURCE',bad)
    authority=LCMGID(bad,'SPOT-R64')
    call LCMDEL(authority,'QFISS')
    trial_source(1)=bad
    call EXPECT_REJECTION(parent,solved,trial_source,count)
    call LCMCL(bad,2)

    trial_source=source
    call CLONE_ROOT(source(1),'BAD-SOURCE',bad)
    outer=LCMGID(bad,'DSOUR')
    inner=LCMGIL(outer,1)
    call LCMGDL(inner,1,values32)
    values32(1)=nearest(values32(1),+1.0_real32)
    call LCMPDL(inner,1,NUNK,2,values32)
    trial_source(1)=bad
    call EXPECT_REJECTION(parent,solved,trial_source,count)
    call LCMCL(bad,2)

    trial_solved=solved
    call CLONE_ROOT(solved(1),'BAD-SOLVED',bad)
    call LCMGET(bad,'KEYFLX',bad_key)
    bad_key(1:2)=[bad_key(2),bad_key(1)]
    call LCMPUT(bad,'KEYFLX',NREG,1,bad_key)
    trial_solved(1)=bad
    call EXPECT_REJECTION(parent,trial_solved,source,count)
    call LCMCL(bad,2)

    call CLONE_ROOT(parent,'BAD-PARENT',bad_parent)
    systems=LCMGID(bad_parent,'SYSTEM')
    system=LCMGIL(systems,2)
    call LCMPUT(system,'SPOT-L1-SNAP',1,1,1)
    call EXPECT_REJECTION(bad_parent,solved,source,count)
    call LCMCL(bad_parent,2)

    call CLONE_ROOT(parent,'BAD-PARENT',bad_parent)
    systems=LCMGID(bad_parent,'SYSTEM')
    system=LCMGIL(systems,3)
    call LCMGET(system,'SPOT-LEAK1D',leakage)
    leakage(1)=nearest(leakage(1),+1.0_real32)
    call LCMPUT(system,'SPOT-LEAK1D',NGRP,2,leakage)
    call EXPECT_REJECTION(bad_parent,solved,source,count)
    call LCMCL(bad_parent,2)

    trial_source=source
    trial_source(1)=c_null_ptr
    call EXPECT_REJECTION(parent,solved,trial_source,count)

    call OPEN_FRESH('EMPTY-PARENT',bad_parent)
    call EXPECT_REJECTION(bad_parent,solved,source,count)
    call LCMCL(bad_parent,2)

    trial_solved=solved
    call OPEN_FRESH('EMPTY-SOLVED',bad)
    trial_solved(1)=bad
    call EXPECT_REJECTION(parent,trial_solved,source,count)
    call LCMCL(bad,2)

    trial_source=source
    call OPEN_FRESH('EMPTY-SOURCE',bad)
    trial_source(1)=bad
    call EXPECT_REJECTION(parent,solved,trial_source,count)
    call LCMCL(bad,2)

    call OPEN_FRESH('NONEMPTY',output_bad)
    marker=271828
    call LCMPUT(output_bad,'SENTINEL',1,1,marker)
    call SPOR64_B2R_COLLECT(output_bad,parent,solved,source,status)
    if (status /= SPOR64_B2R_PREFLIGHT_FAILED) &
      error stop 'nonempty output was not rejected'
    call REQUIRE_INTEGER(output_bad,'SENTINEL',marker)
    call LCMCL(output_bad,2)
    count=count+1

    call SPOR64_B2R_COLLECT(parent,parent,solved,source,status)
    if (status /= SPOR64_B2R_PREFLIGHT_FAILED) &
      error stop 'output/input alias was not rejected'
    count=count+1
  end subroutine RUN_REJECTION_SET


  subroutine EXPECT_REJECTION(parent,solved,source,count)
    type(c_ptr), intent(in) :: parent, solved(NSNAP), source(NSNAP)
    integer, intent(inout) :: count
    type(c_ptr) :: rejected
    integer :: local_status

    call OPEN_FRESH('REJECTED',rejected)
    call SPOR64_B2R_COLLECT(rejected,parent,solved,source,local_status)
    if (local_status /= SPOR64_B2R_PREFLIGHT_FAILED) &
      error stop 'malformed collector input was not rejected'
    if (.not. EMPTY_ROOT(rejected)) &
      error stop 'rejected collector call mutated its output'
    call LCMCL(rejected,2)
    count=count+1
  end subroutine EXPECT_REJECTION


  subroutine VERIFY_CANONICAL_INPUTS(parent,solved,source,k_value,rho_value)
    type(c_ptr), intent(in) :: parent, solved(NSNAP), source(NSNAP)
    real(real64), intent(in) :: k_value, rho_value
    integer :: ip, found_plane, found_epoch, snapshot
    real(real64) :: found64
    real(real32) :: found_k32
    type(c_ptr) :: authority, systems, system

    call REQUIRE_CHARACTER(parent,'SIGNATURE',12,'L_ARCHIVE')
    call REQUIRE_INTEGER(parent,'LISTDIM',NSNAP)
    call REQUIRE_REAL64_BITS(parent,'SPOT-ITER-K',k_value)
    authority=LCMGID(parent,'SPOT-R64')
    call REQUIRE_ASSOCIATED(authority,'assembled authority verification')
    call REQUIRE_CHARACTER(authority,'STATE',12,'ASSEMBLED')
    call REQUIRE_INTEGER(authority,'NPLANE',NSNAP)
    call REQUIRE_INTEGER(authority,'EPOCH',1)
    call LCMGET(authority,'RHO',found64)
    if (transfer(found64,0_int64) /= transfer(rho_value,0_int64)) &
      error stop 'assembled RHO mutated'
    systems=LCMGID(parent,'SYSTEM')
    call REQUIRE_ASSOCIATED(systems,'assembled SYSTEM list verification')
    do ip=1,NSNAP
      system=LCMGIL(systems,ip)
      call REQUIRE_ASSOCIATED(system,'assembled SYSTEM verification')
      call LCMGET(system,'SPOT-L1-SNAP',snapshot)
      if (snapshot /= ip) error stop 'assembled SYSTEM snapshot mutated'
      authority=LCMGID(system,'SPOT-R64')
      call REQUIRE_CHARACTER(authority,'STATE',12,'ASSEMBLED')
      call REQUIRE_INTEGER(authority,'EPOCH',1)

      authority=LCMGID(solved(ip),'SPOT-R64')
      call REQUIRE_CHARACTER(authority,'STATE',12,'SOLVED')
      call LCMGET(authority,'PLANE',found_plane)
      call LCMGET(authority,'EPOCH',found_epoch)
      if (found_plane /= ip .or. found_epoch /= 1) &
        error stop 'canonical SOLVED label mutated'
      call VERIFY_SOLVED_PAYLOAD(solved(ip),ip,rho_value)

      authority=LCMGID(source(ip),'SPOT-R64')
      call REQUIRE_CHARACTER(authority,'STATE',12,'FROZEN-QFIS')
      call LCMGET(authority,'PLANE',found_plane)
      call LCMGET(authority,'EPOCH',found_epoch)
      if (found_plane /= ip .or. found_epoch /= 1) &
        error stop 'canonical SOURCE label mutated'
      call LCMGET(source(ip),'SPOT-KEFF',found_k32)
      if (transfer(found_k32,0_int32) /= &
          transfer(real(k_value,real32),0_int32)) &
        error stop 'canonical SOURCE K mutated'
      call VERIFY_SOURCE_PAYLOAD(source(ip),ip,rho_value)
    end do
  end subroutine VERIFY_CANONICAL_INPUTS


  subroutine VERIFY_SOLVED_PAYLOAD(root,plane,rho_value)
    type(c_ptr), intent(in) :: root
    integer, intent(in) :: plane
    real(real64), intent(in) :: rho_value
    integer :: g
    real(real32) :: found32(NUNK), expected32(NUNK)
    real(real64) :: found64(NUNK), expected64(NUNK), found_rho
    type(c_ptr) :: authority, aflux, asour, mflux, msour

    authority=LCMGID(root,'SPOT-R64')
    aflux=LCMGID(authority,'FLUX')
    asour=LCMGID(authority,'SOUR')
    mflux=LCMGID(root,'FLUX')
    msour=LCMGID(root,'SOUR')
    call LCMGET(authority,'RHO',found_rho)
    if (transfer(found_rho,0_int64) /= transfer(rho_value,0_int64)) &
      error stop 'SOLVED RHO mutated'
    do g=1,NGRP
      call EXPECTED_VECTOR64(1,plane,g,expected64)
      call LCMGDL(aflux,g,found64)
      if (any(transfer(found64,0_int64,NUNK) /= &
          transfer(expected64,0_int64,NUNK))) &
        error stop 'SOLVED authority FLUX mutated'
      expected32=real(expected64,real32)
      call LCMGDL(mflux,g,found32)
      if (any(transfer(found32,0_int32,NUNK) /= &
          transfer(expected32,0_int32,NUNK))) &
        error stop 'SOLVED mirror FLUX mutated'
      call EXPECTED_VECTOR64(2,plane,g,expected64)
      call LCMGDL(asour,g,found64)
      if (any(transfer(found64,0_int64,NUNK) /= &
          transfer(expected64,0_int64,NUNK))) &
        error stop 'SOLVED authority SOUR mutated'
      expected32=real(expected64,real32)
      call LCMGDL(msour,g,found32)
      if (any(transfer(found32,0_int32,NUNK) /= &
          transfer(expected32,0_int32,NUNK))) &
        error stop 'SOLVED mirror SOUR mutated'
    end do
  end subroutine VERIFY_SOLVED_PAYLOAD


  subroutine VERIFY_SOURCE_PAYLOAD(root,plane,rho_value)
    type(c_ptr), intent(in) :: root
    integer, intent(in) :: plane
    real(real64), intent(in) :: rho_value
    integer :: g
    real(real32) :: found32(NUNK), expected32(NUNK)
    real(real64) :: found64(NUNK), expected64(NUNK), found_rho
    type(c_ptr) :: authority, qfiss, outer, inner

    authority=LCMGID(root,'SPOT-R64')
    qfiss=LCMGID(authority,'QFISS')
    outer=LCMGID(root,'DSOUR')
    inner=LCMGIL(outer,1)
    call LCMGET(authority,'RHO',found_rho)
    if (transfer(found_rho,0_int64) /= transfer(rho_value,0_int64)) &
      error stop 'SOURCE RHO mutated'
    do g=1,NGRP
      call EXPECTED_VECTOR64(3,plane,g,expected64)
      call LCMGDL(qfiss,g,found64)
      if (any(transfer(found64,0_int64,NUNK) /= &
          transfer(expected64,0_int64,NUNK))) &
        error stop 'SOURCE authority QFISS mutated'
      expected32=real(expected64,real32)
      call LCMGDL(inner,g,found32)
      if (any(transfer(found32,0_int32,NUNK) /= &
          transfer(expected32,0_int32,NUNK))) &
        error stop 'SOURCE DSOUR mutated'
    end do
  end subroutine VERIFY_SOURCE_PAYLOAD


  subroutine VERIFY_RETURNED_BRIEF(root,rho_value)
    type(c_ptr), intent(in) :: root
    real(real64), intent(in) :: rho_value
    integer :: ip
    real(real64) :: found_rho
    type(c_ptr) :: authority, fluxes, child, child_authority

    call REQUIRE_CHARACTER(root,'SIGNATURE',12,'L_ARCHIVE')
    call REQUIRE_INTEGER(root,'LISTDIM',NSNAP)
    call REQUIRE_ABSENT(root,'RHO')
    call REQUIRE_ABSENT(root,'SPOT-ITER-K')
    call REQUIRE_ABSENT(root,'AX_NEXT')
    call REQUIRE_ABSENT(root,'AX-NEXT')
    call REQUIRE_ABSENT(root,'CLOSED')
    authority=LCMGID(root,'SPOT-R64')
    call REQUIRE_CHARACTER(authority,'STATE',12,'RETURNED')
    call REQUIRE_INTEGER(authority,'NPLANE',NSNAP)
    call REQUIRE_INTEGER(authority,'EPOCH',1)
    call REQUIRE_ABSENT(authority,'RHO')
    fluxes=LCMGID(root,'FLUX')
    do ip=1,NSNAP
      child=LCMGIL(fluxes,ip)
      child_authority=LCMGID(child,'SPOT-R64')
      call REQUIRE_ABSENT(child_authority,'PLANE')
      call REQUIRE_CHARACTER(child_authority,'STATE',12,'SOLVED')
      call REQUIRE_INTEGER(child_authority,'EPOCH',1)
      call LCMGET(child_authority,'RHO',found_rho)
      if (transfer(found_rho,0_int64) /= transfer(rho_value,0_int64)) &
        error stop 'returned child RHO differs'
      call REQUIRE_RECORD(child_authority,'QFISS',NGRP,10)
      call REQUIRE_INTEGER(child,'SPOT-FS-EQN',1)
      call REQUIRE_RECORD(child,'SPOT-FS-K',1,2)
      call REQUIRE_RECORD(child,'SPOT-QFISS',1,10)
    end do
  end subroutine VERIFY_RETURNED_BRIEF


  subroutine EXPECTED_VECTOR64(field,plane,group,values)
    integer, intent(in) :: field, plane, group
    real(real64), intent(out) :: values(NUNK)
    integer :: i, base

    do i=1,NUNK
      select case(field)
      case(1)
        base=1000000+plane*100000+group*100+i
      case(2)
        base=4000000+plane*100000+group*100+i
      case(3)
        base=7000000+plane*100000+group*100+i
      case default
        error stop 'unknown synthetic field'
      end select
      values(i)=nearest(real(base,real64),+1.0_real64)
    end do
  end subroutine EXPECTED_VECTOR64


  subroutine PLANE_KEY(plane,key)
    integer, intent(in) :: plane
    integer, intent(out) :: key(NREG)
    integer :: i
    do i=1,NREG
      key(i)=mod(i+plane-2,NREG)+1
    end do
  end subroutine PLANE_KEY


  subroutine PLANE_LEAKAGE(plane,leakage)
    integer, intent(in) :: plane
    real(real32), intent(out) :: leakage(NGRP)
    integer :: g
    do g=1,NGRP
      leakage(g)=real(plane*100000+g,real32)
    end do
  end subroutine PLANE_LEAKAGE


  subroutine OPEN_FRESH(prefix,root)
    character(len=*), intent(in) :: prefix
    type(c_ptr), intent(out) :: root
    character(len=12) :: name
    object_counter=object_counter+1
    write(name,'("B2R",I6.6)') object_counter
    call LCMOP(root,name,0,1,0)
    call REQUIRE_ASSOCIATED(root,trim(prefix)//' memory root')
    if (.not. EMPTY_ROOT(root)) call FAIL(trim(prefix)//' root not fresh')
  end subroutine OPEN_FRESH


  subroutine CLONE_ROOT(source,label,copy)
    type(c_ptr), intent(in) :: source
    character(len=*), intent(in) :: label
    type(c_ptr), intent(out) :: copy
    call OPEN_FRESH(label,copy)
    call LCMEQU(source,copy)
  end subroutine CLONE_ROOT


  logical function EMPTY_ROOT(root)
    type(c_ptr), intent(in) :: root
    character(len=72) :: object_file
    character(len=12) :: object_name
    integer :: object_length
    logical :: empty, memory_backed
    EMPTY_ROOT=.false.
    if (.not. c_associated(root)) return
    call LCMINF(root,object_file,object_name,empty,object_length,memory_backed)
    EMPTY_ROOT=memory_backed .and. empty .and. object_length == -1 .and. &
        trim(object_name) == '/'
  end function EMPTY_ROOT


  subroutine REQUIRE_ASSOCIATED(ptr,label)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: label
    if (.not. c_associated(ptr)) call FAIL(trim(label)//' missing')
  end subroutine REQUIRE_ASSOCIATED


  subroutine REQUIRE_RECORD(root,name,expected_length,expected_type)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: actual_length, actual_type
    call LCMLEN(root,name,actual_length,actual_type)
    if (actual_length /= expected_length .or. actual_type /= expected_type) &
      call FAIL(trim(name)//' schema differs')
  end subroutine REQUIRE_RECORD


  subroutine REQUIRE_ABSENT(root,name)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer :: actual_length, actual_type
    call LCMLEN(root,name,actual_length,actual_type)
    if (actual_length /= 0) call FAIL(trim(name)//' unexpectedly present')
  end subroutine REQUIRE_ABSENT


  subroutine REQUIRE_INTEGER(root,name,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected
    integer :: found
    call REQUIRE_RECORD(root,name,1,1)
    call LCMGET(root,name,found)
    if (found /= expected) call FAIL(trim(name)//' value differs')
  end subroutine REQUIRE_INTEGER


  subroutine REQUIRE_REAL64_BITS(root,name,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    real(real64), intent(in) :: expected
    real(real64) :: found
    call REQUIRE_RECORD(root,name,1,4)
    call LCMGET(root,name,found)
    if (transfer(found,0_int64) /= transfer(expected,0_int64)) &
      call FAIL(trim(name)//' REAL64 bits differ')
  end subroutine REQUIRE_REAL64_BITS


  subroutine REQUIRE_CHARACTER(root,name,count,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, expected
    integer, intent(in) :: count
    character(len=72) :: found
    integer :: words
    words=(count+3)/4
    call REQUIRE_RECORD(root,name,words,3)
    found=' '
    call LCMGTC(root,name,count,found)
    if (found(1:count) /= expected) &
      call FAIL(trim(name)//' character value differs')
  end subroutine REQUIRE_CHARACTER


  subroutine PUT_CHARACTER(root,name,count,value)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, value
    integer, intent(in) :: count
    character(len=72) :: padded
    padded=' '
    padded(1:min(count,len_trim(value)))=value(1:min(count,len_trim(value)))
    call LCMPTC(root,name,count,padded)
  end subroutine PUT_CHARACTER


  subroutine FAIL(message)
    character(len=*), intent(in) :: message
    write(*,'(A)') 'B2R TEST FAILURE: '//trim(message)
    error stop 'B2R synthetic validation failed'
  end subroutine FAIL

end program TEST_B2R_RETURNED_ARCHIVE
