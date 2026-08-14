program check_rank2_basis_xsm
  ! Independent Ganlib-only audit of a production rank-two POD rebuild.
  !
  !   check_rank2_basis_xsm SNAP REF CONTROL CANDIDATE
  !
  ! SNAP is the original offline snapshot archive, REF is the locked rank-one
  ! basis, CONTROL is a fresh rank-one replay, and CANDIDATE is the matching
  ! fresh rank-two replay.  This program does not call SVD, ASM, SPOT, or any
  ! transport routine.  All four XSM objects are opened read-only.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32,int64,real32,real64
  implicit none

  integer, parameter :: nstate=40
  integer, parameter :: expected_groups=370
  integer, parameter :: expected_regions=8
  integer, parameter :: expected_snapshots=3
  integer, parameter :: max_xsm_path=72

  type :: snapshot_data
    integer :: nreg=0
    integer :: nsnap=0
    integer :: ngroup=0
    real(real32), allocatable :: volume(:)
    real(real32), allocatable :: phi(:,:,:)
  end type snapshot_data

  type :: pod_group
    integer :: nreg=0
    integer :: nsnap=0
    integer :: nmode=0
    real(real32), allocatable :: volume(:)
    real(real32), allocatable :: basis(:)
    real(real32), allocatable :: coeff(:)
    real(real32), allocatable :: radial(:)
    real(real32), allocatable :: txsc(:)
    real(real32), allocatable :: s0xsc(:)
    real(real64), allocatable :: sigma(:)
    real(real64) :: rec_err=0.0_real64
    real(real64) :: ortho_err=0.0_real64
  end type pod_group

  type :: pod_system
    integer :: state(nstate)=0
    integer :: fixb=-1
    integer :: fs_count=-1
    integer :: removal_snapshot=-1
    integer :: removal_group=-1
    integer :: removal_mixture=-1
    integer :: ngroup=0
    integer :: nsnap=0
    character(len=12) :: signature=''
    character(len=12) :: basis_type=''
    character(len=12) :: link_macro=''
    character(len=12) :: link_track=''
    real(real32) :: removal_min=0.0_real32
    real(real64) :: radial_balance=0.0_real64
    real(real64) :: source_l2=0.0_real64
    real(real64) :: source_max=0.0_real64
    integer, allocatable :: rank_root(:)
    real(real64), allocatable :: sigma_root(:,:)
    type(pod_group), allocatable :: group(:)
  end type pod_system

  character(len=1024) :: path(4)
  type(snapshot_data) :: snapshots
  type(pod_system) :: reference,control,candidate
  real(real64), allocatable :: gram_defect(:),projection_defect(:)
  real(real64), allocatable :: spectral_tail(:),tail_delta(:),stored_error(:)
  integer :: i,worst_gram,worst_projection,worst_tail,worst_stored

  if (command_argument_count() /= 4) &
    call fail('EXPECTED SNAP REF CONTROL CANDIDATE.')
  do i=1,4
    call get_command_argument(i,path(i))
    if (len_trim(path(i)) == 0) call fail('EMPTY XSM PATH ARGUMENT.')
    if (len_trim(path(i)) > max_xsm_path) &
      call fail('XSM PATH ARGUMENT EXCEEDS GANLIB LIMIT.')
  enddo

  call load_snapshots(trim(path(1)),snapshots)
  call load_system(trim(path(2)),1,reference,'LOCKED RANK1 REFERENCE')
  call load_system(trim(path(3)),1,control,'FRESH RANK1 CONTROL')
  call load_system(trim(path(4)),2,candidate,'FRESH RANK2 CANDIDATE')

  call compare_rank1_replay(reference,control)
  call compare_rank_independent_fields(control,candidate)
  call check_rank1_prefix(control,candidate)
  call check_snapshot_geometry(snapshots,reference,'REFERENCE')
  call check_snapshot_geometry(snapshots,control,'CONTROL')
  call check_snapshot_geometry(snapshots,candidate,'CANDIDATE')

  allocate(gram_defect(candidate%ngroup))
  allocate(projection_defect(candidate%ngroup))
  allocate(spectral_tail(candidate%ngroup),tail_delta(candidate%ngroup))
  allocate(stored_error(candidate%ngroup))
  call verify_stored_pod_diagnostics(snapshots,reference, &
    'REFERENCE',.true.)
  call verify_stored_pod_diagnostics(snapshots,control, &
    'CONTROL',.true.)
  call verify_stored_pod_diagnostics(snapshots,candidate, &
    'CANDIDATE',.true.,gram_defect,projection_defect,spectral_tail, &
    tail_delta)

  worst_gram=maxloc(gram_defect,dim=1)
  worst_projection=maxloc(projection_defect,dim=1)
  worst_tail=maxloc(tail_delta,dim=1)
  do i=1,candidate%ngroup
    stored_error(i)=candidate%group(i)%rec_err
  enddo
  worst_stored=maxloc(stored_error,dim=1)
  call write_metric_group('RANK2 GRAM MAX DEFECT', &
    gram_defect(worst_gram),worst_gram)
  call write_metric_group('RANK2 PROJECTION RELATIVE DEFECT', &
    projection_defect(worst_projection),worst_projection)
  call write_metric('RANK2 SPECTRAL TAIL MIN',minval(spectral_tail))
  call write_metric('RANK2 SPECTRAL TAIL MAX',maxval(spectral_tail))
  call write_metric('RANK2 STORED ERROR MIN',minval(stored_error))
  call write_metric_group('RANK2 STORED ERROR MAX', &
    stored_error(worst_stored),worst_stored)
  call write_metric_group('RANK2 STORED/SPECTRAL MAX ABS DELTA', &
    tail_delta(worst_tail),worst_tail)
  write(6,'(A)') 'RANK2-BASIS FRESH-RANK1 BITWISE PASS'
  write(6,'(A)') 'RANK2-BASIS COMMON-FIELDS BITWISE PASS'
  write(6,'(A)') 'RANK2-BASIS MODE1-PREFIX BITWISE PASS'
  write(6,'(A)') 'RANK2-BASIS STORED-DIAGNOSTICS BITWISE PASS'
  write(6,'(A)') 'RANK2-BASIS CLASSIFICATION OFFLINE_RECONSTRUCTION_ONLY'
  write(6,'(A)') 'RANK2-BASIS COMPLETE'

contains

  subroutine load_snapshots(file_name,data)
    character(len=*), intent(in) :: file_name
    type(snapshot_data), intent(out) :: data
    type(c_ptr) :: root,archive,snapshot_list,tracks,flux_objects
    type(c_ptr) :: track_ptr,flux_ptr,group_flux
    integer :: listdim,isnap,g,r,length_found,type_found,nreg,nunk
    integer :: state(nstate)
    integer, allocatable :: key(:)
    real(real32), allocatable :: volume(:),unknown_flux(:)
    character(len=12) :: signature
    character(len=96) :: owner

    call LCMOP(root,file_name,2,2,0)
    call require_record(root,'SIGNATURE',3,3,'SNAPSHOT ARCHIVE')
    call LCMGTC(root,'SIGNATURE',12,signature)
    if (signature /= 'L_ARCHIVE') &
      call fail('SNAPSHOT L_ARCHIVE SIGNATURE EXPECTED.')
    archive=root
    call require_record(root,'LISTDIM',1,1,'SNAPSHOT ARCHIVE')
    call LCMGET(root,'LISTDIM',listdim)
    ! The immutable seed is a one-item backup wrapper; continued archives are
    ! direct.  Descend through the wrapper without modifying either form.
    if (listdim == 1) then
      call require_record(root,'SNAP',1,10,'SNAPSHOT WRAPPER')
      snapshot_list=LCMGID(root,'SNAP')
      call require_directory_item(snapshot_list,1,'SNAPSHOT WRAPPER ITEM')
      archive=LCMGIL(snapshot_list,1)
      call require_record(archive,'SIGNATURE',3,3,'INNER SNAPSHOT ARCHIVE')
      call LCMGTC(archive,'SIGNATURE',12,signature)
      if (signature /= 'L_ARCHIVE') &
        call fail('INNER SNAPSHOT L_ARCHIVE SIGNATURE EXPECTED.')
      call require_record(archive,'LISTDIM',1,1,'INNER SNAPSHOT ARCHIVE')
      call LCMGET(archive,'LISTDIM',listdim)
    endif
    if (listdim /= expected_snapshots) &
      call fail('SNAPSHOT ARCHIVE MUST CONTAIN THREE SNAPSHOTS.')
    call require_record(archive,'TRACK',listdim,10,'SNAPSHOT ARCHIVE')
    call require_record(archive,'FLUX',listdim,10,'SNAPSHOT ARCHIVE')
    tracks=LCMGID(archive,'TRACK')
    flux_objects=LCMGID(archive,'FLUX')
    data%nsnap=listdim
    data%nreg=expected_regions
    data%ngroup=expected_groups
    allocate(data%volume(data%nreg))
    allocate(data%phi(data%nreg,data%nsnap,data%ngroup))
    data%phi=0.0_real32

    do isnap=1,data%nsnap
      write(owner,'(A,I0)') 'SNAPSHOT ',isnap
      call require_directory_item(tracks,isnap,trim(owner)//' TRACK')
      call require_directory_item(flux_objects,isnap,trim(owner)//' FLUX')
      track_ptr=LCMGIL(tracks,isnap)
      flux_ptr=LCMGIL(flux_objects,isnap)
      call require_record(track_ptr,'STATE-VECTOR',nstate,1,owner)
      call LCMGET(track_ptr,'STATE-VECTOR',state)
      nreg=state(1)
      nunk=state(2)
      if ((nreg /= data%nreg).or.(nunk <= 0)) &
        call fail(trim(owner)//' INVALID RADIAL DIMENSIONS.')
      call require_record(track_ptr,'KEYFLX',nreg,1,owner)
      call require_record(track_ptr,'VOLUME',nreg,2,owner)
      allocate(key(nreg),volume(nreg))
      call LCMGET(track_ptr,'KEYFLX',key)
      call LCMGET(track_ptr,'VOLUME',volume)
      if (any(key < 0).or.any(key > nunk)) &
        call fail(trim(owner)//' INVALID RADIAL FLUX KEYS.')
      if (any(.not.ieee_is_finite(volume)).or. &
          any(volume <= 0.0_real32)) &
        call fail(trim(owner)//' INVALID RADIAL VOLUME.')
      if (isnap == 1) then
        data%volume=volume
      else if (any(real32_bits(volume) /= real32_bits(data%volume))) then
        call fail(trim(owner)//' VOLUME BITS DIFFER.')
      endif

      call require_record(flux_ptr,'FLUX',data%ngroup,10,owner)
      group_flux=LCMGID(flux_ptr,'FLUX')
      allocate(unknown_flux(nunk))
      do g=1,data%ngroup
        call LCMLEL(group_flux,g,length_found,type_found)
        if ((length_found /= nunk).or.(type_found /= 2)) &
          call fail(trim(owner)//' INVALID GROUP FLUX ITEM.')
        call LCMGDL(group_flux,g,unknown_flux)
        if (any(.not.ieee_is_finite(unknown_flux))) &
          call fail(trim(owner)//' NON-FINITE GROUP FLUX.')
        do r=1,nreg
          if (key(r) == 0) cycle
          data%phi(r,isnap,g)=unknown_flux(key(r))
          if (data%phi(r,isnap,g) <= 0.0_real32) &
            call fail(trim(owner)//' NONPOSITIVE ACTIVE REGIONAL FLUX.')
        enddo
      enddo
      deallocate(unknown_flux,volume,key)
    enddo
    call LCMCL(root,1)
  end subroutine load_snapshots

  subroutine load_system(file_name,expected_rank,data,owner)
    character(len=*), intent(in) :: file_name,owner
    integer, intent(in) :: expected_rank
    type(pod_system), intent(out) :: data
    type(c_ptr) :: root,groups,group_ptr
    integer :: g,nreg,nsnap,nmode,length_found,type_found
    character(len=96) :: label

    call LCMOP(root,file_name,2,2,0)
    call require_record(root,'SIGNATURE',3,3,owner)
    call LCMGTC(root,'SIGNATURE',12,data%signature)
    if (data%signature /= 'L_PIJ') &
      call fail(trim(owner)//' L_PIJ SIGNATURE EXPECTED.')
    call require_record(root,'STATE-VECTOR',nstate,1,owner)
    call LCMGET(root,'STATE-VECTOR',data%state)
    data%ngroup=data%state(8)
    if ((data%ngroup /= expected_groups).or.(data%state(14) /= 1)) &
      call fail(trim(owner)//' INVALID SPOD STATE-VECTOR.')
    call require_record(root,'SPOT-FIXB',1,1,owner)
    call LCMGET(root,'SPOT-FIXB',data%fixb)
    if (data%fixb /= 0) call fail(trim(owner)//' MUST BE POD-BUILT.')
    call require_record(root,'SPOT-BTYPE',3,3,owner)
    call LCMGTC(root,'SPOT-BTYPE',12,data%basis_type)
    if (data%basis_type /= 'POD-BUILT') &
      call fail(trim(owner)//' POD-BUILT TYPE EXPECTED.')
    call require_record(root,'LINK.MACRO',3,3,owner)
    call require_record(root,'LINK.TRACK',3,3,owner)
    call LCMGTC(root,'LINK.MACRO',12,data%link_macro)
    call LCMGTC(root,'LINK.TRACK',12,data%link_track)

    call require_record(root,'SPOT-FS-N',1,1,owner)
    call require_record(root,'SPOT-RBAL',1,4,owner)
    call require_record(root,'SPOT-Q-L2',1,4,owner)
    call require_record(root,'SPOT-Q-MAX',1,4,owner)
    call require_record(root,'SPOT-REM-MIN',1,2,owner)
    call require_record(root,'SPOT-REM-SNP',1,1,owner)
    call require_record(root,'SPOT-REM-GRP',1,1,owner)
    call require_record(root,'SPOT-REM-MIX',1,1,owner)
    call LCMGET(root,'SPOT-FS-N',data%fs_count)
    call LCMGET(root,'SPOT-RBAL',data%radial_balance)
    call LCMGET(root,'SPOT-Q-L2',data%source_l2)
    call LCMGET(root,'SPOT-Q-MAX',data%source_max)
    call LCMGET(root,'SPOT-REM-MIN',data%removal_min)
    call LCMGET(root,'SPOT-REM-SNP',data%removal_snapshot)
    call LCMGET(root,'SPOT-REM-GRP',data%removal_group)
    call LCMGET(root,'SPOT-REM-MIX',data%removal_mixture)
    if ((data%fs_count < 0).or. &
        (.not.ieee_is_finite(data%radial_balance)).or. &
        (.not.ieee_is_finite(data%source_l2)).or. &
        (.not.ieee_is_finite(data%source_max)).or. &
        (.not.ieee_is_finite(data%removal_min))) &
      call fail(trim(owner)//' NON-FINITE ROOT SCIENTIFIC FIELD.')

    call require_record(root,'POD-RANK-G',data%ngroup,1,owner)
    allocate(data%rank_root(data%ngroup),data%group(data%ngroup))
    call LCMGET(root,'POD-RANK-G',data%rank_root)
    if (any(data%rank_root /= expected_rank)) &
      call fail(trim(owner)//' ROOT POD RANK IS INVALID.')
    call require_record(root,'GROUP',data%ngroup,10,owner)
    groups=LCMGID(root,'GROUP')

    data%nsnap=0
    do g=1,data%ngroup
      write(label,'(A,I0)') trim(owner)//' GROUP ',g
      call require_directory_item(groups,g,label)
      group_ptr=LCMGIL(groups,g)
      call require_record(group_ptr,'NREG2D',1,1,label)
      call require_record(group_ptr,'NSNAP',1,1,label)
      call require_record(group_ptr,'POD-NMODE',1,1,label)
      call LCMGET(group_ptr,'NREG2D',nreg)
      call LCMGET(group_ptr,'NSNAP',nsnap)
      call LCMGET(group_ptr,'POD-NMODE',nmode)
      if ((nreg /= expected_regions).or. &
          (nsnap /= expected_snapshots).or.(nmode /= expected_rank)) &
        call fail(trim(label)//' INVALID POD DIMENSIONS.')
      if (g == 1) then
        data%nsnap=nsnap
      else if (nsnap /= data%nsnap) then
        call fail(trim(owner)//' SNAPSHOT COUNT CHANGES BY GROUP.')
      endif
      data%group(g)%nreg=nreg
      data%group(g)%nsnap=nsnap
      data%group(g)%nmode=nmode
      allocate(data%group(g)%volume(nreg))
      allocate(data%group(g)%basis(nreg*nmode))
      allocate(data%group(g)%coeff(nmode*nsnap))
      allocate(data%group(g)%radial(nreg*nsnap))
      allocate(data%group(g)%sigma(nsnap))
      call require_record(group_ptr,'VOL2D',nreg,2,label)
      call require_record(group_ptr,'POD-BASIS',nreg*nmode,2,label)
      call require_record(group_ptr,'POD-COEFF',nmode*nsnap,2,label)
      call require_record(group_ptr,'RADIAL-OP',nreg*nsnap,2,label)
      call require_record(group_ptr,'POD-SIGMA',nsnap,4,label)
      call require_record(group_ptr,'POD-REC-ERR',1,4,label)
      call require_record(group_ptr,'POD-ORTHO',1,4,label)
      call LCMGET(group_ptr,'VOL2D',data%group(g)%volume)
      call LCMGET(group_ptr,'POD-BASIS',data%group(g)%basis)
      call LCMGET(group_ptr,'POD-COEFF',data%group(g)%coeff)
      call LCMGET(group_ptr,'RADIAL-OP',data%group(g)%radial)
      call LCMGET(group_ptr,'POD-SIGMA',data%group(g)%sigma)
      call LCMGET(group_ptr,'POD-REC-ERR',data%group(g)%rec_err)
      call LCMGET(group_ptr,'POD-ORTHO',data%group(g)%ortho_err)

      call LCMLEN(group_ptr,'DRAGON-TXSC',length_found,type_found)
      if ((length_found <= 0).or.(type_found /= 2)) &
        call fail(trim(label)//' INVALID DRAGON-TXSC RECORD.')
      allocate(data%group(g)%txsc(length_found))
      call LCMGET(group_ptr,'DRAGON-TXSC',data%group(g)%txsc)
      call LCMLEN(group_ptr,'DRAGON-S0XSC',length_found,type_found)
      if ((length_found <= 0).or.(type_found /= 2)) &
        call fail(trim(label)//' INVALID DRAGON-S0XSC RECORD.')
      allocate(data%group(g)%s0xsc(length_found))
      call LCMGET(group_ptr,'DRAGON-S0XSC',data%group(g)%s0xsc)

      if (any(.not.ieee_is_finite(data%group(g)%volume)).or. &
          any(data%group(g)%volume <= 0.0_real32).or. &
          any(.not.ieee_is_finite(data%group(g)%basis)).or. &
          any(.not.ieee_is_finite(data%group(g)%coeff)).or. &
          any(.not.ieee_is_finite(data%group(g)%radial)).or. &
          any(.not.ieee_is_finite(data%group(g)%txsc)).or. &
          any(.not.ieee_is_finite(data%group(g)%s0xsc)).or. &
          any(.not.ieee_is_finite(data%group(g)%sigma)).or. &
          (.not.ieee_is_finite(data%group(g)%rec_err)).or. &
          (.not.ieee_is_finite(data%group(g)%ortho_err)).or. &
          (data%group(g)%rec_err < 0.0_real64).or. &
          (data%group(g)%ortho_err < 0.0_real64)) &
        call fail(trim(label)//' INVALID POD SCIENTIFIC FIELD.')
      if ((data%group(g)%sigma(1) <= 0.0_real64).or. &
          any(data%group(g)%sigma(2:) > &
              data%group(g)%sigma(:nsnap-1))) &
        call fail(trim(label)//' INVALID SINGULAR-VALUE ORDER.')
      if (expected_rank == 2) &
        call require_second_numerical_mode(data%group(g),label)
    enddo

    call require_record(root,'POD-SIGMA-G', &
      data%nsnap*data%ngroup,4,owner)
    allocate(data%sigma_root(data%nsnap,data%ngroup))
    call LCMGET(root,'POD-SIGMA-G',data%sigma_root)
    if (any(.not.ieee_is_finite(data%sigma_root))) &
      call fail(trim(owner)//' NON-FINITE ROOT POD SPECTRUM.')
    do g=1,data%ngroup
      if (any(real64_bits(data%sigma_root(:,g)) /= &
              real64_bits(data%group(g)%sigma))) &
        call fail(trim(owner)//' ROOT/GROUP POD-SIGMA BITS DIFFER.')
    enddo
    call LCMCL(root,1)
  end subroutine load_system

  subroutine require_second_numerical_mode(group0,owner)
    type(pod_group), intent(in) :: group0
    character(len=*), intent(in) :: owner
    real(real64) :: tolerance
    tolerance=real(max(group0%nreg,group0%nsnap),real64)* &
      epsilon(1.0_real64)*group0%sigma(1)
    if (group0%sigma(2) <= tolerance) &
      call fail(trim(owner)//' SECOND MODE IS BELOW PRODUCTION RANK RULE.')
  end subroutine require_second_numerical_mode

  subroutine compare_rank1_replay(reference0,control0)
    type(pod_system), intent(in) :: reference0,control0
    integer :: g
    character(len=96) :: owner
    call compare_root_science(reference0,control0, &
      'FRESH RANK1 ROOT FIELDS')
    if (any(reference0%rank_root /= control0%rank_root)) &
      call fail('FRESH RANK1 ROOT RANK DIFFERS FROM REFERENCE.')
    if (any(real64_bits(reference0%sigma_root) /= &
            real64_bits(control0%sigma_root))) &
      call fail('FRESH RANK1 ROOT SPECTRUM DIFFERS BITWISE.')
    do g=1,reference0%ngroup
      write(owner,'(A,I0)') 'FRESH RANK1 GROUP ',g
      call compare_common_group(reference0%group(g),control0%group(g), &
        owner)
      if (reference0%group(g)%nmode /= control0%group(g)%nmode) &
        call fail(trim(owner)//' MODE COUNTS DIFFER.')
      if (any(real32_bits(reference0%group(g)%basis) /= &
              real32_bits(control0%group(g)%basis))) &
        call fail(trim(owner)//' BASIS DIFFERS BITWISE.')
      if (any(real32_bits(reference0%group(g)%coeff) /= &
              real32_bits(control0%group(g)%coeff))) &
        call fail(trim(owner)//' COEFFICIENTS DIFFER BITWISE.')
      if (real64_bits(reference0%group(g)%rec_err) /= &
          real64_bits(control0%group(g)%rec_err)) &
        call fail(trim(owner)//' RECONSTRUCTION ERROR DIFFERS BITWISE.')
      if (real64_bits(reference0%group(g)%ortho_err) /= &
          real64_bits(control0%group(g)%ortho_err)) &
        call fail(trim(owner)//' ORTHOGONALITY ERROR DIFFERS BITWISE.')
    enddo
  end subroutine compare_rank1_replay

  subroutine compare_rank_independent_fields(control0,candidate0)
    type(pod_system), intent(in) :: control0,candidate0
    integer :: g
    character(len=96) :: owner
    call compare_root_science(control0,candidate0, &
      'RANK-INDEPENDENT ROOT FIELDS')
    if (any(real64_bits(control0%sigma_root) /= &
            real64_bits(candidate0%sigma_root))) &
      call fail('RANK1/RANK2 ROOT SPECTRA DIFFER BITWISE.')
    do g=1,control0%ngroup
      write(owner,'(A,I0)') 'RANK-INDEPENDENT GROUP ',g
      call compare_common_group(control0%group(g),candidate0%group(g), &
        owner)
    enddo
  end subroutine compare_rank_independent_fields

  subroutine compare_root_science(left,right,owner)
    type(pod_system), intent(in) :: left,right
    character(len=*), intent(in) :: owner
    if ((left%signature /= right%signature).or. &
        (left%basis_type /= right%basis_type).or. &
        (left%link_macro /= right%link_macro).or. &
        (left%link_track /= right%link_track).or. &
        (left%fixb /= right%fixb).or. &
        any(left%state /= right%state).or. &
        (left%ngroup /= right%ngroup).or.(left%nsnap /= right%nsnap).or. &
        (left%fs_count /= right%fs_count).or. &
        (left%removal_snapshot /= right%removal_snapshot).or. &
        (left%removal_group /= right%removal_group).or. &
        (left%removal_mixture /= right%removal_mixture)) &
      call fail(trim(owner)//' DIFFER.')
    if ((real32_bits(left%removal_min) /= &
         real32_bits(right%removal_min)).or. &
        (real64_bits(left%radial_balance) /= &
         real64_bits(right%radial_balance)).or. &
        (real64_bits(left%source_l2) /= real64_bits(right%source_l2)).or. &
        (real64_bits(left%source_max) /= &
         real64_bits(right%source_max))) &
      call fail(trim(owner)//' DIFFER BITWISE.')
  end subroutine compare_root_science

  subroutine compare_common_group(left,right,owner)
    type(pod_group), intent(in) :: left,right
    character(len=*), intent(in) :: owner
    if ((left%nreg /= right%nreg).or.(left%nsnap /= right%nsnap)) &
      call fail(trim(owner)//' DIMENSIONS DIFFER.')
    if (any(real32_bits(left%volume) /= real32_bits(right%volume))) &
      call fail(trim(owner)//' VOLUME DIFFERS BITWISE.')
    if (size(left%radial) /= size(right%radial)) &
      call fail(trim(owner)//' RADIAL-OP EXTENTS DIFFER.')
    if (any(real32_bits(left%radial) /= real32_bits(right%radial))) &
      call fail(trim(owner)//' RADIAL-OP DIFFERS BITWISE.')
    if (size(left%txsc) /= size(right%txsc)) &
      call fail(trim(owner)//' DRAGON-TXSC EXTENTS DIFFER.')
    if (any(real32_bits(left%txsc) /= real32_bits(right%txsc))) &
      call fail(trim(owner)//' DRAGON-TXSC DIFFERS BITWISE.')
    if (size(left%s0xsc) /= size(right%s0xsc)) &
      call fail(trim(owner)//' DRAGON-S0XSC EXTENTS DIFFER.')
    if (any(real32_bits(left%s0xsc) /= real32_bits(right%s0xsc))) &
      call fail(trim(owner)//' DRAGON-S0XSC DIFFERS BITWISE.')
    if (any(real64_bits(left%sigma) /= real64_bits(right%sigma))) &
      call fail(trim(owner)//' POD-SIGMA DIFFERS BITWISE.')
  end subroutine compare_common_group

  subroutine check_rank1_prefix(control0,candidate0)
    type(pod_system), intent(in) :: control0,candidate0
    integer :: g,i,k,nreg,nmode2
    character(len=96) :: owner
    do g=1,control0%ngroup
      write(owner,'(A,I0)') 'RANK2 MODE1 GROUP ',g
      nreg=control0%group(g)%nreg
      nmode2=candidate0%group(g)%nmode
      do i=1,nreg
        if (real32_bits(control0%group(g)%basis(i)) /= &
            real32_bits(candidate0%group(g)%basis(i))) &
          call fail(trim(owner)//' BASIS PREFIX DIFFERS BITWISE.')
      enddo
      do k=1,control0%group(g)%nsnap
        if (real32_bits(control0%group(g)%coeff(k)) /= &
            real32_bits(candidate0%group(g)%coeff((k-1)*nmode2+1))) &
          call fail(trim(owner)//' COEFFICIENT PREFIX DIFFERS BITWISE.')
      enddo
    enddo
  end subroutine check_rank1_prefix

  subroutine check_snapshot_geometry(snapshot0,system0,owner)
    type(snapshot_data), intent(in) :: snapshot0
    type(pod_system), intent(in) :: system0
    character(len=*), intent(in) :: owner
    integer :: g
    if ((snapshot0%nreg /= expected_regions).or. &
        (snapshot0%nsnap /= system0%nsnap).or. &
        (snapshot0%ngroup /= system0%ngroup)) &
      call fail(trim(owner)//' SNAPSHOT DIMENSIONS DIFFER.')
    do g=1,system0%ngroup
      if (any(real32_bits(snapshot0%volume) /= &
              real32_bits(system0%group(g)%volume))) &
        call fail(trim(owner)//' VOLUME DIFFERS FROM RAW SNAPSHOTS.')
    enddo
  end subroutine check_snapshot_geometry

  subroutine verify_stored_pod_diagnostics(snapshot0,system0,owner, &
      require_bitwise,gram_out,projection_out,tail_out,tail_delta_out)
    type(snapshot_data), intent(in) :: snapshot0
    type(pod_system), intent(in) :: system0
    character(len=*), intent(in) :: owner
    logical, intent(in) :: require_bitwise
    real(real64), intent(out), optional :: gram_out(:),projection_out(:)
    real(real64), intent(out), optional :: tail_out(:),tail_delta_out(:)
    real(real64), allocatable :: weight(:),shape(:,:),recon(:,:)
    real(real64) :: rec_err,ortho_err,projection_error,tail
    real(real64) :: norm_full,norm_diff,inner,projection
    real(real64) :: projection_num,projection_den,total
    integer :: g,i,j,k,a,nreg,nsnap,nmode,index_b,index_c
    character(len=96) :: label

    do g=1,system0%ngroup
      write(label,'(A,I0)') trim(owner)//' GROUP ',g
      nreg=system0%group(g)%nreg
      nsnap=system0%group(g)%nsnap
      nmode=system0%group(g)%nmode
      allocate(weight(nreg),shape(nreg,nsnap),recon(nreg,nsnap))
      weight=real(system0%group(g)%volume,real64)/ &
        sum(real(system0%group(g)%volume,real64))
      do k=1,nsnap
        inner=sum(weight*real(snapshot0%phi(:,k,g),real64))
        if ((.not.ieee_is_finite(inner)).or.(inner <= 0.0_real64)) &
          call fail(trim(label)//' INVALID SNAPSHOT NORMALIZATION.')
        shape(:,k)=real(snapshot0%phi(:,k,g),real64)/inner
      enddo

      recon=0.0_real64
      do k=1,nsnap
        do a=1,nmode
          index_c=(k-1)*nmode+a
          index_b=(a-1)*nreg+1
          recon(:,k)=recon(:,k)+real(system0%group(g)%basis( &
            index_b:index_b+nreg-1),real64)* &
            real(system0%group(g)%coeff(index_c),real64)
        enddo
      enddo
      norm_full=sqrt(sum(spread(weight,2,nsnap)*shape*shape))
      norm_diff=sqrt(sum(spread(weight,2,nsnap)* &
        (recon-shape)*(recon-shape)))
      if (norm_full <= 0.0_real64) &
        call fail(trim(label)//' ZERO SNAPSHOT NORM.')
      rec_err=norm_diff/norm_full

      ortho_err=0.0_real64
      do a=1,nmode
        do j=1,nmode
          inner=sum(weight*real(system0%group(g)%basis( &
            (a-1)*nreg+1:a*nreg),real64)* &
            real(system0%group(g)%basis((j-1)*nreg+1:j*nreg),real64))
          if (a == j) inner=inner-1.0_real64
          ortho_err=max(ortho_err,abs(inner))
        enddo
      enddo
      if ((.not.ieee_is_finite(rec_err)).or. &
          (.not.ieee_is_finite(ortho_err))) &
        call fail(trim(label)//' NON-FINITE RECOMPUTED DIAGNOSTIC.')
      if (require_bitwise) then
        if (real64_bits(rec_err) /= &
            real64_bits(system0%group(g)%rec_err)) &
          call fail(trim(label)//' RECONSTRUCTION ERROR DIFFERS BITWISE.')
        if (real64_bits(ortho_err) /= &
            real64_bits(system0%group(g)%ortho_err)) &
          call fail(trim(label)//' ORTHOGONALITY ERROR DIFFERS BITWISE.')
      endif

      projection_num=0.0_real64
      projection_den=0.0_real64
      do k=1,nsnap
        do a=1,nmode
          projection=0.0_real64
          do i=1,nreg
            projection=projection+weight(i)* &
              real(system0%group(g)%basis((a-1)*nreg+i),real64)* &
              shape(i,k)
          enddo
          inner=real(system0%group(g)%coeff((k-1)*nmode+a),real64)
          projection_num=projection_num+(inner-projection)**2
          projection_den=projection_den+projection**2
        enddo
      enddo
      if (projection_den <= 0.0_real64) &
        call fail(trim(label)//' ZERO PROJECTED COEFFICIENT NORM.')
      projection_error=sqrt(projection_num/projection_den)
      total=sum(system0%group(g)%sigma**2)
      if ((.not.ieee_is_finite(total)).or.(total <= 0.0_real64)) &
        call fail(trim(label)//' INVALID SPECTRAL NORM.')
      tail=sqrt(sum(system0%group(g)%sigma(nmode+1:)**2)/total)
      if (present(gram_out)) gram_out(g)=ortho_err
      if (present(projection_out)) projection_out(g)=projection_error
      if (present(tail_out)) tail_out(g)=tail
      if (present(tail_delta_out)) &
        tail_delta_out(g)=abs(rec_err-tail)
      deallocate(recon,shape,weight)
    enddo
  end subroutine verify_stored_pod_diagnostics

  subroutine require_record(ptr,name,length_expected,type_expected,owner)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,owner
    integer, intent(in) :: length_expected,type_expected
    integer :: length_found,type_found
    call LCMLEN(ptr,name,length_found,type_found)
    if ((length_found /= length_expected).or. &
        (type_found /= type_expected)) &
      call fail(trim(owner)//' INVALID RECORD '//trim(name)//'.')
  end subroutine require_record

  subroutine require_directory_item(list_ptr,index0,owner)
    type(c_ptr), intent(in) :: list_ptr
    integer, intent(in) :: index0
    character(len=*), intent(in) :: owner
    integer :: length_found,type_found
    call LCMLEL(list_ptr,index0,length_found,type_found)
    if ((length_found /= -1).or.(type_found /= 0)) &
      call fail(trim(owner)//' IS NOT A DIRECTORY.')
  end subroutine require_directory_item

  pure elemental integer(int32) function real32_bits(value)
    real(real32), intent(in) :: value
    real32_bits=transfer(value,0_int32)
  end function real32_bits

  pure elemental integer(int64) function real64_bits(value)
    real(real64), intent(in) :: value
    real64_bits=transfer(value,0_int64)
  end function real64_bits

  subroutine write_metric(label,value)
    character(len=*), intent(in) :: label
    real(real64), intent(in) :: value
    write(6,'(A,1X,ES25.17E3)') trim(label),value
  end subroutine write_metric

  subroutine write_metric_group(label,value,group_index)
    character(len=*), intent(in) :: label
    real(real64), intent(in) :: value
    integer, intent(in) :: group_index
    write(6,'(A,1X,ES25.17E3,1X,A,I0)') &
      trim(label),value,'GROUP=',group_index
  end subroutine write_metric_group

  subroutine fail(message)
    character(len=*), intent(in) :: message
    write(0,'(A)') 'RANK2-BASIS ERROR: '//trim(message)
    error stop 2
  end subroutine fail
end program check_rank2_basis_xsm
