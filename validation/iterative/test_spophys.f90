program test_spophys
  use, intrinsic :: iso_c_binding, only : c_associated,c_ptr
  use, intrinsic :: iso_fortran_env, only : error_unit,int32,int64,real32,real64
  use GANLIB
  implicit none

  integer, parameter :: nstate=40,ngrp=2,nreg=3,nsnap=2,nmode=1,maxmix=2
  integer :: state(nstate),state_found(nstate),rank(ngrp),rank_found(ngrp)
  integer :: rank_previous(ngrp),fixb,physical,nmode_found,igr,ilong,itylcm
  integer :: i,k
  integer :: ientry(2),jentry(2)
  real(real32) :: volume(nreg),basis(nreg,nmode),coeff(nmode,nsnap)
  real(real32) :: basis_found(nreg,nreg),coeff_found(nreg,nsnap)
  real(real32) :: radial(nreg*nsnap),radial_found(nreg*nsnap)
  real(real32) :: tx(maxmix+1),tx_found(maxmix+1),s0(2*(maxmix+1))
  real(real32) :: s0_found(2*(maxmix+1)),shape_reference(nreg,nsnap)
  real(real32) :: shape_found(nreg,nsnap)
  real(real64) :: sigma_root(nsnap*ngrp),sigma_expected(nsnap*ngrp)
  real(real64) :: sigma(nsnap),sigma_found(nsnap),rec_old,rec_found
  real(real64) :: ortho_found,complete_found,equiv_found,tolerance
  real(real64) :: root_ortho,root_complete,root_equiv,root_tolerance
  real(real64) :: relative_error,weight64(nreg)
  character(len=12) :: signature,basis_type
  character(len=12) :: hentry(2)
  character(len=32) :: negative_case
  type(c_ptr) :: input,output,groups,group,kentry(2)

  call LCMOP(input,'SPOPHYS-IN',0,1,0)
  call LCMOP(output,'SPOPHYS-OUT',0,1,0)
  if (.not.c_associated(input).or..not.c_associated(output)) &
    error stop 'SPOPHYS TEST: LCM CREATE FAILED'

  signature='L_PIJ'
  call LCMPTC(input,'SIGNATURE',12,signature)
  state=0
  state(1)=1
  state(2)=1
  state(3)=1
  state(5)=1
  state(6)=1
  state(8)=ngrp
  state(9)=7
  state(10)=maxmix
  state(11)=1
  state(14)=1
  call LCMPUT(input,'STATE-VECTOR',nstate,1,state)
  rank=nmode
  call LCMPUT(input,'POD-RANK-G',ngrp,1,rank)
  fixb=0
  call LCMPUT(input,'SPOT-FIXB',1,1,fixb)
  basis_type='POD-BUILT'
  call LCMPTC(input,'SPOT-BTYPE',12,basis_type)

  ! The second singular value is outside the retained one-mode input basis,
  ! but it still belongs to the complete snapshot spectrum and must survive.
  sigma_root=[3.0_real64,1.0_real64,0.0_real64,0.0_real64]
  sigma_expected=sigma_root
  call LCMPUT(input,'POD-SIGMA-G',nsnap*ngrp,4,sigma_root)

  volume=[1.0_real32,2.0_real32,3.0_real32]
  weight64=real(volume,real64)/sum(real(volume,real64))
  groups=LCMLID(input,'GROUP',ngrp)
  do igr=1,ngrp
    group=LCMDIL(groups,igr)
    call LCMPUT(group,'NREG2D',1,1,nreg)
    call LCMPUT(group,'NSNAP',1,1,nsnap)
    call LCMPUT(group,'POD-NMODE',1,1,nmode)
    call LCMPUT(group,'VOL2D',nreg,2,volume)

    basis=0.0_real32
    basis(1,1)=real(1.0_real64/sqrt(weight64(1)),real32)
    if (igr == 1) then
      coeff(1,1)=0.8_real32
      coeff(1,2)=0.3_real32
    else
      coeff=0.0_real32
    endif
    call LCMPUT(group,'POD-BASIS',nreg*nmode,2,basis)
    call LCMPUT(group,'POD-COEFF',nmode*nsnap,2,coeff)
    sigma=sigma_root((igr-1)*nsnap+1:igr*nsnap)
    call LCMPUT(group,'POD-SIGMA',nsnap,4,sigma)
    rec_old=0.125_real64+real(igr,real64)*0.01_real64
    call LCMPUT(group,'POD-REC-ERR',1,4,rec_old)
    call LCMPUT(group,'POD-ORTHO',1,4,0.0_real64)

    do i=1,nreg*nsnap
      radial(i)=real(100*igr+i,real32)/17.0_real32
    enddo
    tx=[1.0_real32,2.0_real32,3.0_real32]+real(igr,real32)
    do i=1,size(s0)
      s0(i)=real(10*igr+i,real32)/13.0_real32
    enddo
    call LCMPUT(group,'RADIAL-OP',nreg*nsnap,2,radial)
    call LCMPUT(group,'DRAGON-TXSC',maxmix+1,2,tx)
    call LCMPUT(group,'DRAGON-S0XSC',size(s0),2,s0)
  enddo

  hentry=['PHYSICAL    ','ASSEMBLED   ']
  ientry=[1,1]
  jentry=[0,2]
  kentry=[output,input]
  call SPOPHYS(2,hentry,ientry,jentry,kentry)

  call require_record(output,'SIGNATURE',3,3,'ROOT SIGNATURE')
  call LCMGTC(output,'SIGNATURE',12,signature)
  call assert_true(signature == 'L_PIJ','OUTPUT SIGNATURE')
  call LCMGET(output,'STATE-VECTOR',state_found)
  call assert_true(all(state_found == state),'STATE-VECTOR COPY')
  call LCMGET(output,'SPOT-FIXB',fixb)
  call assert_true(fixb == 1,'ROOT FIXED-BASIS MARKER')
  call LCMGTC(output,'SPOT-BTYPE',12,basis_type)
  call assert_true(basis_type == 'POD-FIXED','ROOT BASIS LIFECYCLE')
  call LCMGET(output,'SPOT-PHYS',physical)
  call assert_true(physical == 1,'ROOT PHYSICAL PROVENANCE')
  call LCMGET(output,'POD-RANK-OLD',rank_previous)
  call assert_true(all(rank_previous == rank),'OLD RANK PROVENANCE')
  call LCMGET(output,'POD-RANK-G',rank_found)
  call assert_true(all(rank_found == nreg),'FULL PHYSICAL RANK')
  call LCMGET(output,'POD-SIGMA-G',sigma_root)
  call assert_true(same_real64_bits(sigma_root,sigma_expected), &
    'PRESERVED ROOT POD SPECTRUM')
  call LCMGET(output,'SPOT-PH-ORT',root_ortho)
  call LCMGET(output,'SPOT-PH-CMP',root_complete)
  call LCMGET(output,'SPOT-PH-SNP',root_equiv)
  call LCMGET(output,'SPOT-PH-TOL',root_tolerance)
  call assert_true(root_tolerance == &
    64.0_real64*real(epsilon(1.0_real32),real64),'ROUNDOFF-DERIVED TOLERANCE')
  call assert_true(max(root_ortho,root_complete,root_equiv) <= root_tolerance, &
    'ROOT INVARIANTS WITHIN TOLERANCE')

  groups=LCMGID(output,'GROUP')
  do igr=1,ngrp
    group=LCMGIL(groups,igr)
    call LCMGET(group,'POD-NMODE',nmode_found)
    call assert_true(nmode_found == nreg,'GROUP FULL PHYSICAL RANK')
    call LCMGTC(group,'SPOT-BTYPE',12,basis_type)
    call assert_true(basis_type == 'PHYSICAL-ID','GROUP PHYSICAL CONTENT')
    call LCMGET(group,'VOL2D',volume)
    weight64=real(volume,real64)/sum(real(volume,real64))
    call LCMGET(group,'POD-BASIS',basis_found)
    do i=1,nreg
      do k=1,nreg
        if (i == k) then
          call assert_true(transfer(basis_found(i,k),0_int32) == transfer( &
            real(1.0_real64/sqrt(weight64(i)),real32),0_int32), &
            'PHYSICAL IDENTITY DIAGONAL')
        else
          call assert_true(transfer(basis_found(i,k),0_int32) == 0_int32, &
            'PHYSICAL IDENTITY OFF-DIAGONAL')
        endif
      enddo
    enddo

    call LCMGET(group,'POD-COEFF',coeff_found)
    shape_found=matmul(basis_found,coeff_found)
    basis=0.0_real32
    basis(1,1)=real(1.0_real64/sqrt(weight64(1)),real32)
    if (igr == 1) then
      coeff(1,1)=0.8_real32
      coeff(1,2)=0.3_real32
    else
      coeff=0.0_real32
    endif
    shape_reference=matmul(basis,coeff)
    if (all(shape_reference == 0.0_real32)) then
      relative_error=sqrt(sum(weight64*sum( &
        real(shape_found,real64)**2,dim=2)))
    else
      relative_error=sqrt(sum(weight64*sum( &
        (real(shape_found,real64)-real(shape_reference,real64))**2,dim=2))/ &
        sum(weight64*sum(real(shape_reference,real64)**2,dim=2)))
    endif
    call assert_true(relative_error <= root_tolerance,'SNAPSHOT EQUIVALENCE')

    call LCMGET(group,'POD-SIGMA',sigma_found)
    sigma=sigma_expected((igr-1)*nsnap+1:igr*nsnap)
    call assert_true(same_real64_bits(sigma_found,sigma), &
      'PRESERVED GROUP POD SPECTRUM')
    call LCMGET(group,'POD-REC-ERR',rec_found)
    call LCMGET(group,'POD-ORTHO',ortho_found)
    call LCMGET(group,'PHYS-ORTHO',root_ortho)
    call LCMGET(group,'PHYS-COMP',complete_found)
    call LCMGET(group,'PHYS-SNAP',equiv_found)
    call LCMGET(group,'PHYS-TOL',tolerance)
    rec_old=0.125_real64+real(igr,real64)*0.01_real64
    call assert_true(transfer(rec_found,0_int64) == &
      transfer(rec_old,0_int64),'PRESERVED POD RECONSTRUCTION ERROR')
    call assert_true(transfer(ortho_found,0_int64) == &
      transfer(root_ortho,0_int64),'CURRENT ORTHOGONALITY METADATA')
    call assert_true(tolerance == root_tolerance,'GROUP INVARIANT TOLERANCE')
    call assert_true(max(ortho_found,complete_found,equiv_found) <= tolerance, &
      'GROUP INVARIANTS WITHIN TOLERANCE')

    call LCMGET(group,'RADIAL-OP',radial_found)
    call LCMGET(group,'DRAGON-TXSC',tx_found)
    call LCMGET(group,'DRAGON-S0XSC',s0_found)
    do i=1,nreg*nsnap
      radial(i)=real(100*igr+i,real32)/17.0_real32
    enddo
    tx=[1.0_real32,2.0_real32,3.0_real32]+real(igr,real32)
    do i=1,size(s0)
      s0(i)=real(10*igr+i,real32)/13.0_real32
    enddo
    call assert_true(same_real32_bits(radial_found,radial), &
      'RADIAL OPERATOR BITWISE PRESERVATION')
    call assert_true(same_real32_bits(tx_found,tx), &
      'TOTAL XS BITWISE PRESERVATION')
    call assert_true(same_real32_bits(s0_found,s0), &
      'SCATTER XS BITWISE PRESERVATION')
  enddo

  call LCMGTC(input,'SPOT-BTYPE',12,basis_type)
  call assert_true(basis_type == 'POD-BUILT','READ-ONLY INPUT UNCHANGED')
  call get_command_argument(1,negative_case)
  select case(trim(negative_case))
  case('bad-old-extent','bad-group-count')
    call LCMGET(output,'STATE-VECTOR',state_found)
    if(negative_case == 'bad-old-extent') state_found(9)=0
    if(negative_case == 'bad-group-count') state_found(8)=ngrp+1
    call LCMPUT(output,'STATE-VECTOR',nstate,1,state_found)
  case('bad-radial-volume')
    groups=LCMGID(output,'GROUP')
    group=LCMGIL(groups,1)
    call LCMGET(group,'VOL2D',volume)
    volume(1)=volume(1)*2.0_real32
    call LCMPUT(group,'VOL2D',nreg,2,volume)
  case('','bad-radial-s0-length','bad-radial-s0-type', &
       'bad-axial-xs-length','bad-axial-xs-type','bad-p0-total')
    continue
  case default
    error stop 'UNKNOWN NEGATIVE TEST CASE'
  end select
  call exercise_spoasm_round_trip(output,7,1,0)
  call exercise_spoasm_round_trip(output,14,1,0)
  call exercise_spoasm_round_trip(output,7,3,0)
  call exercise_spoasm_round_trip(output,7,3,1)
  call exercise_spoasm_round_trip(output,7,3,2)
  call LCMCL(output,2)
  call LCMCL(input,2)
  write(*,'(A)') 'SPOPHYS BEHAVIOR PASS: full physical fixed basis and metadata.'

contains

  subroutine exercise_spoasm_round_trip(physical_basis,axial_nunk,nanis,leak_mode)
    integer, parameter :: nunk=7,nmix2d=1,nfis=1
    type(c_ptr), intent(in) :: physical_basis
    integer, intent(in) :: axial_nunk,nanis,leak_mode
    type(c_ptr) :: tracking,macrolib,snapshots,assembled
    type(c_ptr) :: tracks,fluxes,systems,libraries
    type(c_ptr) :: track_item,flux_item,system_item,library_item
    type(c_ptr) :: flux_list,source_list,qfiss_outer,qfiss_inner
    type(c_ptr) :: r64_empty
    type(c_ptr) :: macro2,macro_groups,macro_group
    type(c_ptr) :: system_groups,system_group
    type(c_ptr) :: physical_groups,physical_group,assembled_groups
    type(c_ptr) :: assembled_group
    integer :: local_state(nstate),basis_state_before(nstate)
    integer :: basis_state_after(nstate),keyflx(nreg),matcod(nreg)
    integer :: rank_old_ref(ngrp),rank_old_new(ngrp)
    integer :: rank_ref(ngrp),rank_new(ngrp),marker,nmode_new,nsnap_new
    integer :: isnap,jgrp,ilm
    integer :: map_zero(1),map_one(1)
    real(real32) :: flux_vector(nunk),source_vector(nunk)
    real(real32) :: volume_local(nreg),tx_snapshot(nmix2d+1)
    real(real32) :: s0_snapshot(nmix2d+1),s0_physical(nmix2d+1)
    real(real32) :: leakage(ngrp),leak_value,expected_radial(nreg*nsnap)
    real(real32) :: axial_total(maxmix),axial_scatter(maxmix,3)
    real(real32) :: xs_zero(1),basis_ref(nreg,nreg),basis_new(nreg,nreg)
    real(real32) :: coeff_ref(nreg,nsnap),coeff_new(nreg,nsnap)
    real(real32) :: radial_ref(nreg*nsnap),radial_new(nreg*nsnap)
    real(real32) :: tx_new(maxmix+1),s0_new(maxmix+1,nanis)
    real(real64) :: sigma_ref(nsnap),sigma_new(nsnap)
    real(real64) :: sigma_root_ref(nsnap*ngrp),sigma_root_new(nsnap*ngrp)
    real(real64) :: pod_ref(2),pod_new(2),phys_ref(4),phys_new(4)
    real(real64) :: root_phys_ref(4),root_phys_new(4)
    character(len=12) :: text12
    character(len=2) :: moment

    call LCMGET(physical_basis,'STATE-VECTOR',basis_state_before)
    call LCMOP(tracking,'SPOASM-TRK',0,1,0)
    call LCMOP(macrolib,'SPOASM-MAC',0,1,0)
    call LCMOP(snapshots,'SPOASM-SNP',0,1,0)
    call LCMOP(assembled,'SPOASM-SYS',0,1,0)
    call assert_true(c_associated(tracking).and.c_associated(macrolib).and. &
      c_associated(snapshots).and.c_associated(assembled), &
      'SPOASM ROUND-TRIP LCM CREATE')

    text12='L_TRACK'
    call LCMPTC(tracking,'SIGNATURE',12,text12)
    local_state=0
    local_state(1)=nreg
    ! Only the target axial storage changes. Radial snapshot vectors and the
    ! immutable radial basis keep their original extents and numerical data.
    local_state(2)=axial_nunk
    local_state(4)=nmix2d*nsnap
    local_state(6)=nreg
    local_state(16)=nanis
    call LCMPUT(tracking,'STATE-VECTOR',nstate,1,local_state)

    text12='L_MACROLIB'
    call LCMPTC(macrolib,'SIGNATURE',12,text12)
    local_state=0
    local_state(1)=ngrp
    local_state(2)=maxmix
    local_state(3)=nanis
    if (negative_case == 'bad-p0-total'.and.nanis > 1) local_state(10)=1
    call LCMPUT(macrolib,'STATE-VECTOR',nstate,1,local_state)
    if (nanis > 1) then
      ! The corresponding radial APOL values below are T'=2, s0'=0.5.
      ! Different nonzero transport corrections leave removal = 1.5.
      axial_total=[2.25_real32,2.5_real32]
      axial_scatter(:,1)=[0.75_real32,1.0_real32]
      axial_scatter(:,2)=[0.125_real32,0.375_real32]
      axial_scatter(:,3)=[-0.25_real32,-0.125_real32]
      macro_groups=LCMLID(macrolib,'GROUP',ngrp)
      do jgrp=1,ngrp
        macro_group=LCMDIL(macro_groups,jgrp)
        call LCMPUT(macro_group,'NTOT0',maxmix,2,axial_total)
        do ilm=1,nanis
          write(moment,'(I2.2)') ilm-1
          call LCMPUT(macro_group,'SIGW'//moment,maxmix,2,axial_scatter(:,ilm))
        enddo
        if (negative_case == 'bad-axial-xs-length') &
          call LCMPUT(macro_group,'SIGW01',1,2,axial_scatter(:,2))
        if (negative_case == 'bad-axial-xs-type') &
          call LCMPUT(macro_group,'SIGW01',maxmix,1,[1,2])
      enddo
    endif

    text12='L_SNAP'
    call LCMPTC(snapshots,'SIGNATURE',12,text12)
    call LCMPUT(snapshots,'LISTDIM',1,1,nsnap)
    tracks=LCMLID(snapshots,'TRACK',nsnap)
    fluxes=LCMLID(snapshots,'FLUX',nsnap)
    systems=LCMLID(snapshots,'SYSTEM',nsnap)
    libraries=LCMLID(snapshots,'MICROLIB2',nsnap)
    call assert_true(c_associated(tracks).and.c_associated(fluxes).and. &
      c_associated(systems).and.c_associated(libraries), &
      'SPOASM ROUND-TRIP SNAPSHOT LISTS')

    keyflx=[1,2,3]
    matcod=1
    volume_local=[1.0_real32,2.0_real32,3.0_real32]
    tx_snapshot=[0.0_real32,2.0_real32]
    s0_snapshot=[0.0_real32,0.5_real32]
    s0_physical=s0_snapshot
    map_zero=0
    map_one=1
    xs_zero=0.0_real32

    do isnap=1,nsnap
      leak_value=0.0_real32
      if (leak_mode /= 0) leak_value=real(3-2*isnap,real32)*0.125_real32
      expected_radial((isnap-1)*nreg+1:isnap*nreg)=-1.25_real32-leak_value
      track_item=LCMDIL(tracks,isnap)
      local_state=0
      local_state(1)=nreg
      local_state(2)=nunk
      local_state(4)=nmix2d
      local_state(40)=0
      call LCMPUT(track_item,'STATE-VECTOR',nstate,1,local_state)
      call LCMPUT(track_item,'KEYFLX',nreg,1,keyflx)
      call LCMPUT(track_item,'MATCOD',nreg,1,matcod)
      call LCMPUT(track_item,'VOLUME',nreg,2,volume_local)

      flux_item=LCMDIL(fluxes,isnap)
      flux_list=LCMLID(flux_item,'FLUX',ngrp)
      source_list=LCMLID(flux_item,'SOUR',ngrp)
      qfiss_outer=LCMLID(flux_item,'SPOT-QFISS',1)
      qfiss_inner=LCMLIL(qfiss_outer,1,ngrp)
      r64_empty=LCMDID(flux_item,'SPOT-R64')
      call assert_true(c_associated(flux_list).and.c_associated(source_list) &
        .and.c_associated(qfiss_outer).and.c_associated(qfiss_inner).and. &
        c_associated(r64_empty), &
        'SPOASM ROUND-TRIP FLUX LISTS')
      marker=1
      call LCMPUT(flux_item,'SPOT-FS-EQN',1,1,marker)
      call LCMPUT(flux_item,'SPOT-FS-K',1,2,1.0_real32)
      if (leak_mode /= 0) then
        leakage=leak_value
        call LCMPUT(flux_item,'SPOT-LEAK1D',ngrp,2,leakage)
      endif
      do jgrp=1,ngrp
        do i=1,nunk
          flux_vector(i)=1.0_real32+ &
            real(8*isnap+2*jgrp+i,real32)/64.0_real32
        enddo
        source_vector=0.25_real32*flux_vector
        call LCMPDL(flux_list,jgrp,nunk,2,flux_vector)
        call LCMPDL(source_list,jgrp,nunk,2,source_vector)
        call LCMPDL(qfiss_inner,jgrp,nunk,2,source_vector)
      enddo

      system_item=LCMDIL(systems,isnap)
      local_state=0
      local_state(8)=ngrp
      local_state(9)=nunk
      call LCMPUT(system_item,'STATE-VECTOR',nstate,1,local_state)
      system_groups=LCMLID(system_item,'GROUP',ngrp)
      do jgrp=1,ngrp
        system_group=LCMDIL(system_groups,jgrp)
        call LCMPUT(system_group,'DRAGON-TXSC',nmix2d+1,2,tx_snapshot)
        s0_snapshot=s0_physical
        if (leak_mode == 2) s0_snapshot=s0_snapshot-leak_value
        call LCMPUT(system_group,'DRAGON-S0XSC', &
          nmix2d+1,2,s0_snapshot)
        if (leak_mode /= 0) &
          call LCMPUT(system_group,'SPOT-S0-PHYS',nmix2d+1,2,s0_physical)
        if (negative_case == 'bad-radial-s0-length') &
          call LCMPUT(system_group,'DRAGON-S0XSC',1,2,s0_snapshot)
        if (negative_case == 'bad-radial-s0-type') &
          call LCMPUT(system_group,'DRAGON-S0XSC',nmix2d+1,1,[0,1])
      enddo

      library_item=LCMDIL(libraries,isnap)
      macro2=LCMDID(library_item,'MACROLIB')
      local_state=0
      local_state(1)=ngrp
      local_state(2)=nmix2d
      local_state(3)=nanis
      local_state(4)=nfis
      call LCMPUT(macro2,'STATE-VECTOR',nstate,1,local_state)
      macro_groups=LCMLID(macro2,'GROUP',ngrp)
      do jgrp=1,ngrp
        macro_group=LCMDIL(macro_groups,jgrp)
        call LCMPUT(macro_group,'NUSIGF',nmix2d*nfis,2,xs_zero)
        call LCMPUT(macro_group,'CHI',nmix2d*nfis,2,xs_zero)
        call LCMPUT(macro_group,'NJJS00',nmix2d,1,map_zero)
        call LCMPUT(macro_group,'IJJS00',nmix2d,1,map_one)
        call LCMPUT(macro_group,'IPOS00',nmix2d,1,map_one)
        call LCMPUT(macro_group,'SCAT00',1,2,xs_zero)
      enddo
    enddo

    text12='L_PIJ'
    call LCMPTC(assembled,'SIGNATURE',12,text12)
    call SPOASM(assembled,macrolib,tracking,snapshots,physical_basis,1,0,nreg)
    call LCMGET(assembled,'STATE-VECTOR',local_state)
    call assert_true(local_state(9) == axial_nunk, &
      'SPOASM TARGET AXIAL STORAGE EXTENT')

    call require_record(assembled,'SIGNATURE',3,3, &
      'SPOASM ROUND-TRIP SIGNATURE')
    call LCMGTC(assembled,'SIGNATURE',12,text12)
    call assert_true(text12 == 'L_PIJ','SPOASM ROUND-TRIP L_PIJ')
    call LCMGET(assembled,'SPOT-FIXB',marker)
    call assert_true(marker == 1,'SPOASM ROUND-TRIP FIXB')
    call LCMGET(assembled,'SPOT-PHYS',marker)
    call assert_true(marker == 1,'SPOASM ROUND-TRIP PHYSICAL PROVENANCE')
    call LCMGTC(assembled,'SPOT-BTYPE',12,text12)
    call assert_true(text12 == 'POD-FIXED','SPOASM ROUND-TRIP ROOT TYPE')

    call LCMGET(physical_basis,'POD-RANK-OLD',rank_old_ref)
    call LCMGET(assembled,'POD-RANK-OLD',rank_old_new)
    call assert_true(all(rank_old_ref == nmode).and. &
      all(rank_old_new == rank_old_ref),'SPOASM ROUND-TRIP OLD RANK')
    call LCMGET(physical_basis,'POD-RANK-G',rank_ref)
    call LCMGET(assembled,'POD-RANK-G',rank_new)
    call assert_true(all(rank_ref == nreg).and.all(rank_new == rank_ref), &
      'SPOASM ROUND-TRIP FULL RANK')
    call LCMGET(physical_basis,'POD-SIGMA-G',sigma_root_ref)
    call LCMGET(assembled,'POD-SIGMA-G',sigma_root_new)
    call assert_true(same_real64_bits(sigma_root_new,sigma_root_ref), &
      'SPOASM ROUND-TRIP ROOT SPECTRUM')
    call LCMGET(physical_basis,'SPOT-PH-ORT',root_phys_ref(1))
    call LCMGET(physical_basis,'SPOT-PH-CMP',root_phys_ref(2))
    call LCMGET(physical_basis,'SPOT-PH-SNP',root_phys_ref(3))
    call LCMGET(physical_basis,'SPOT-PH-TOL',root_phys_ref(4))
    call LCMGET(assembled,'SPOT-PH-ORT',root_phys_new(1))
    call LCMGET(assembled,'SPOT-PH-CMP',root_phys_new(2))
    call LCMGET(assembled,'SPOT-PH-SNP',root_phys_new(3))
    call LCMGET(assembled,'SPOT-PH-TOL',root_phys_new(4))
    call assert_true(same_real64_bits(root_phys_new,root_phys_ref), &
      'SPOASM ROUND-TRIP ROOT INVARIANTS')

    physical_groups=LCMGID(physical_basis,'GROUP')
    assembled_groups=LCMGID(assembled,'GROUP')
    do jgrp=1,ngrp
      physical_group=LCMGIL(physical_groups,jgrp)
      assembled_group=LCMGIL(assembled_groups,jgrp)
      call LCMGET(assembled_group,'POD-NMODE',nmode_new)
      call LCMGET(assembled_group,'NSNAP',nsnap_new)
      call assert_true(nmode_new == nreg.and.nmode_new > nsnap_new.and. &
        nsnap_new == nsnap,'SPOASM ROUND-TRIP RANK EXCEEDS SNAPSHOTS')
      call LCMGTC(assembled_group,'SPOT-BTYPE',12,text12)
      call assert_true(text12 == 'PHYSICAL-ID', &
        'SPOASM ROUND-TRIP GROUP TYPE')

      call require_record(assembled_group,'POD-BASIS',nreg*nreg,2, &
        'SPOASM ROUND-TRIP BASIS EXTENT')
      call require_record(assembled_group,'POD-COEFF',nreg*nsnap,2, &
        'SPOASM ROUND-TRIP COEFFICIENT EXTENT')
      call LCMGET(physical_group,'POD-BASIS',basis_ref)
      call LCMGET(assembled_group,'POD-BASIS',basis_new)
      call LCMGET(physical_group,'POD-COEFF',coeff_ref)
      call LCMGET(assembled_group,'POD-COEFF',coeff_new)
      call assert_true(same_real32_bits(reshape(basis_new,[nreg*nreg]), &
        reshape(basis_ref,[nreg*nreg])),'SPOASM ROUND-TRIP BASIS')
      call assert_true(same_real32_bits(reshape(coeff_new,[nreg*nsnap]), &
        reshape(coeff_ref,[nreg*nsnap])),'SPOASM ROUND-TRIP COEFFICIENTS')

      call LCMGET(physical_group,'POD-SIGMA',sigma_ref)
      call LCMGET(assembled_group,'POD-SIGMA',sigma_new)
      call assert_true(same_real64_bits(sigma_new,sigma_ref), &
        'SPOASM ROUND-TRIP GROUP SPECTRUM')
      call LCMGET(physical_group,'POD-REC-ERR',pod_ref(1))
      call LCMGET(physical_group,'POD-ORTHO',pod_ref(2))
      call LCMGET(assembled_group,'POD-REC-ERR',pod_new(1))
      call LCMGET(assembled_group,'POD-ORTHO',pod_new(2))
      call assert_true(same_real64_bits(pod_new,pod_ref), &
        'SPOASM ROUND-TRIP POD DIAGNOSTICS')
      call LCMGET(physical_group,'PHYS-ORTHO',phys_ref(1))
      call LCMGET(physical_group,'PHYS-COMP',phys_ref(2))
      call LCMGET(physical_group,'PHYS-SNAP',phys_ref(3))
      call LCMGET(physical_group,'PHYS-TOL',phys_ref(4))
      call LCMGET(assembled_group,'PHYS-ORTHO',phys_new(1))
      call LCMGET(assembled_group,'PHYS-COMP',phys_new(2))
      call LCMGET(assembled_group,'PHYS-SNAP',phys_new(3))
      call LCMGET(assembled_group,'PHYS-TOL',phys_new(4))
      call assert_true(same_real64_bits(phys_new,phys_ref), &
        'SPOASM ROUND-TRIP GROUP INVARIANTS')

      call LCMGET(physical_group,'RADIAL-OP',radial_ref)
      call LCMGET(assembled_group,'RADIAL-OP',radial_new)
      call assert_true(same_real32_bits(radial_new,expected_radial), &
        'SPOASM ROUND-TRIP REBUILT RADIAL OPERATOR')
      call assert_true(.not.same_real32_bits(radial_new,radial_ref), &
        'SPOASM ROUND-TRIP DID NOT COPY RADIAL OPERATOR')
      call LCMGET(assembled_group,'DRAGON-TXSC',tx_new)
      call require_record(assembled_group,'DRAGON-S0XSC', &
        (maxmix+1)*nanis,2,'SPOASM AXIAL SCATTER MOMENT EXTENT')
      call LCMGET(assembled_group,'DRAGON-S0XSC',s0_new)
      if (nanis == 1) then
      call assert_true(same_real32_bits(tx_new, &
        [0.0_real32,2.0_real32,2.0_real32]), &
        'SPOASM ROUND-TRIP REBUILT TOTAL XS')
      call assert_true(same_real32_bits(s0_new(:,1), &
        [0.0_real32,0.5_real32,0.5_real32]), &
        'SPOASM ROUND-TRIP REBUILT SCATTER XS')
      else
        call assert_true(tx_new(1) == 0.0_real32.and. &
          all(s0_new(1,:) == 0.0_real32),'SPOASM VOID XS')
        call assert_true(same_real32_bits(tx_new(2:),axial_total), &
          'SPOASM PHYSICAL AXIAL TOTAL; NO APOL DOUBLE COUNT')
        do ilm=1,nanis
          call assert_true(same_real32_bits(s0_new(2:,ilm),axial_scatter(:,ilm)), &
            'SPOASM PHYSICAL AXIAL SCATTER MOMENT')
        enddo
      endif
    enddo

    call LCMGTC(physical_basis,'SPOT-BTYPE',12,text12)
    call assert_true(text12 == 'POD-FIXED', &
      'SPOASM ROUND-TRIP READ-ONLY BASIS')
    call LCMGET(physical_basis,'STATE-VECTOR',basis_state_after)
    call assert_true(all(basis_state_before == basis_state_after), &
      'SPOASM BASIS HEADER UNCHANGED')
    call LCMCL(assembled,2)
    call LCMCL(snapshots,2)
    call LCMCL(macrolib,2)
    call LCMCL(tracking,2)
    write(*,'(A)') &
      'SPOPHYS SPOASM ROUND-TRIP PASS: full rank 3 exceeds 2 snapshots.'
    write(*,'(A,I0)') 'SPOASM FIXB AXIAL-EXTENT REUSE PASS: ',axial_nunk
    if (nanis > 1) write(*,'(A,I0)') &
      'SPOASM AXIAL P2 FROM MACROLIB; RADIAL P0 UNCHANGED PASS: ',leak_mode
  end subroutine exercise_spoasm_round_trip

  subroutine require_record(root,name,expected_length,expected_type,label)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name,label
    integer, intent(in) :: expected_length,expected_type

    call LCMLEN(root,name,ilong,itylcm)
    if ((ilong /= expected_length).or.(itylcm /= expected_type)) then
      write(error_unit,'(A)') 'SPOPHYS TEST: '//label
      error stop 1
    endif
  end subroutine require_record

  subroutine assert_true(condition,label)
    logical, intent(in) :: condition
    character(len=*), intent(in) :: label

    if (.not.condition) then
      write(error_unit,'(A)') 'SPOPHYS TEST: '//label
      error stop 1
    endif
  end subroutine assert_true

  logical function same_real32_bits(left,right)
    real(real32), intent(in) :: left(:),right(:)

    same_real32_bits=size(left) == size(right)
    if (same_real32_bits) same_real32_bits=all(transfer(left,0_int32, &
      size(left)) == transfer(right,0_int32,size(right)))
  end function same_real32_bits

  logical function same_real64_bits(left,right)
    real(real64), intent(in) :: left(:),right(:)

    same_real64_bits=size(left) == size(right)
    if (same_real64_bits) same_real64_bits=all(transfer(left,0_int64, &
      size(left)) == transfer(right,0_int64,size(right)))
  end function same_real64_bits

end program test_spophys

subroutine REDGET(ityp,nitma,flott,text,dflot)
  implicit none
  integer :: ityp,nitma
  real :: flott
  character(len=*) :: text
  double precision :: dflot

  ityp=3
  nitma=0
  flott=0.0
  text=';'
  dflot=0.0d0
end subroutine REDGET
