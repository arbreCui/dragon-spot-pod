program check_one_map_xsm
  ! Independent Ganlib-only, read-only audit of one fixed-space SPOT map.
  !
  !   check_one_map_xsm basis_reference.xsm state1_system.xsm \
  !     state0_axial.xsm state1_axial.xsm state1_snapshots.xsm
  !
  ! No Dragon, SPOT, assembly, transport, or production convergence routine
  ! is linked or called.  The checker reads the five archived XSM objects,
  ! verifies the fixed POD package bit for bit, requires a live RADIAL-OP
  ! change, and independently recomputes the three canonical outer residuals
  ! plus the dimensional leakage-change diagnostic.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32,int64,real32,real64
  implicit none

  integer, parameter :: nstate=40
  integer, parameter :: max_xsm_path=72

  type :: group_data
    integer :: nreg=0
    integer :: nsnap=0
    integer :: nmode=0
    real(real32), allocatable :: volume(:)
    real(real32), allocatable :: basis(:)
    real(real32), allocatable :: coeff(:)
    real(real32), allocatable :: radial(:)
    real(real64), allocatable :: sigma(:)
    real(real64) :: rec_err=0.0_real64
    real(real64) :: ortho=0.0_real64
  end type group_data

  type :: system_data
    character(len=12) :: signature=''
    character(len=12) :: basis_type=''
    character(len=12) :: link_macro=''
    character(len=12) :: link_track=''
    character(len=12) :: link_basis=''
    integer :: state(nstate)=0
    integer :: fixb=-1
    integer :: fs_count=-1
    integer :: ngroup=0
    integer :: nsnap=0
    real(real32) :: removal_min=0.0_real32
    real(real64) :: radial_balance=0.0_real64
    real(real64) :: source_l2=0.0_real64
    real(real64) :: source_max=0.0_real64
    integer, allocatable :: rank_root(:)
    real(real64), allocatable :: sigma_root(:,:)
    type(group_data), allocatable :: group(:)
  end type system_data

  type :: canonical_state
    character(len=12) :: signature=''
    character(len=12) :: norm_id=''
    character(len=12) :: basis_type=''
    integer :: state(nstate)=0
    integer :: dims(4)=0
    integer :: fixb=-1
    integer, allocatable :: rank(:)
    integer, allocatable :: offset(:)
    integer, allocatable :: gram_offset(:)
    integer, allocatable :: basis_offset(:)
    real(real32), allocatable :: basis(:)
    real(real64), allocatable :: coordinates(:)
    real(real64), allocatable :: leakage(:)
    real(real64), allocatable :: height(:)
    real(real64), allocatable :: gram(:)
    real(real64), allocatable :: offspace(:)
    real(real32) :: keff=0.0_real32
    real(real64) :: rho=0.0_real64
    real(real64) :: norm=0.0_real64
    real(real64) :: gram_error=0.0_real64
    real(real64) :: saved_defect(4)=0.0_real64
    logical :: has_saved_defect=.false.
  end type canonical_state

  character(len=1024) :: paths(5)
  type(system_data) :: reference_system,current_system
  type(canonical_state) :: previous_state,current_state
  integer :: i

  if (command_argument_count() /= 5) call fail( &
    'FIVE ARGUMENTS EXPECTED: BASIS, SYSTEM1, STATE0, STATE1, SNAP1.')
  do i=1,5
    call get_command_argument(i,paths(i))
    if (len_trim(paths(i)) == 0) call fail('EMPTY XSM PATH ARGUMENT.')
    if (len_trim(paths(i)) > max_xsm_path) &
      call fail('XSM PATH ARGUMENT EXCEEDS GANLIB LIMIT.')
  enddo

  call load_system(trim(paths(1)),0,0,'POD-BUILT',.false., &
    reference_system,'BASIS REFERENCE')
  call load_system(trim(paths(2)),1,3,'POD-FIXED',.true., &
    current_system,'CURRENT SYSTEM')
  call compare_systems(reference_system,current_system)

  call load_canonical_state(trim(paths(3)),0,'POD-BUILT',.false., &
    previous_state,'STATE ZERO')
  call load_canonical_state(trim(paths(4)),1,'POD-FIXED',.true., &
    current_state,'STATE ONE')
  call compare_state_to_system(previous_state,reference_system,'STATE ZERO')
  call compare_state_to_system(current_state,current_system,'STATE ONE')
  call compare_states_and_defects(previous_state,current_state)
  call check_restart_archive(trim(paths(5)),previous_state,current_state)

  write(6,'(A)') 'ONE-MAP-XSM POD-PACKAGE BITWISE PASS'
  write(6,'(A)') 'ONE-MAP-XSM RADIAL-OP LIVE-CHANGE PASS'
  write(6,'(A)') 'ONE-MAP-XSM CANONICAL-LAYOUT BITWISE PASS'
  write(6,'(A)') 'ONE-MAP-XSM RAW-DEFECT BITWISE PASS'
  write(6,'(A)') 'ONE-MAP-XSM RESTART-ARCHIVE BITWISE PASS'
  write(6,'(A)') 'ONE-MAP-XSM COMPLETE'

contains

  subroutine load_system(path,expected_fixb,expected_fs_count,expected_type, &
      expect_basis_link,data,owner)
    character(len=*), intent(in) :: path,expected_type,owner
    integer, intent(in) :: expected_fixb,expected_fs_count
    logical, intent(in) :: expect_basis_link
    type(system_data), intent(out) :: data
    type(c_ptr) :: root,groups,group_ptr
    integer :: g,nreg0,nsnap0,nmode0,nsnap_root
    integer :: length_found,type_found
    character(len=128) :: label

    call LCMOP(root,path,2,2,0)
    call require_record(root,'SIGNATURE',3,3,owner)
    call LCMGTC(root,'SIGNATURE',12,data%signature)
    if (data%signature /= 'L_PIJ') &
      call fail(trim(owner)//' L_PIJ SIGNATURE EXPECTED.')

    call require_record(root,'STATE-VECTOR',nstate,1,owner)
    call LCMGET(root,'STATE-VECTOR',data%state)
    data%ngroup=data%state(8)
    if ((data%ngroup /= 370).or.(data%state(14) /= 1)) &
      call fail(trim(owner)//' INVALID SPOD STATE-VECTOR.')

    call require_record(root,'SPOT-FIXB',1,1,owner)
    call LCMGET(root,'SPOT-FIXB',data%fixb)
    if (data%fixb /= expected_fixb) &
      call fail(trim(owner)//' SPOT-FIXB MARKER IS INVALID.')
    call require_record(root,'SPOT-BTYPE',3,3,owner)
    call LCMGTC(root,'SPOT-BTYPE',12,data%basis_type)
    if (data%basis_type /= expected_type) &
      call fail(trim(owner)//' SPOT-BTYPE MARKER IS INVALID.')
    call require_record(root,'SPOT-FS-N',1,1,owner)
    call require_record(root,'SPOT-RBAL',1,4,owner)
    call require_record(root,'SPOT-Q-L2',1,4,owner)
    call require_record(root,'SPOT-Q-MAX',1,4,owner)
    call require_record(root,'SPOT-REM-MIN',1,2,owner)
    call LCMGET(root,'SPOT-FS-N',data%fs_count)
    call LCMGET(root,'SPOT-RBAL',data%radial_balance)
    call LCMGET(root,'SPOT-Q-L2',data%source_l2)
    call LCMGET(root,'SPOT-Q-MAX',data%source_max)
    call LCMGET(root,'SPOT-REM-MIN',data%removal_min)
    if ((data%fs_count /= expected_fs_count).or. &
        (.not.ieee_is_finite(data%radial_balance)).or. &
        (data%radial_balance < 0.0_real64).or. &
        (.not.ieee_is_finite(data%source_l2)).or. &
        (data%source_l2 < 0.0_real64).or. &
        (.not.ieee_is_finite(data%source_max)).or. &
        (data%source_max < 0.0_real64).or. &
        (.not.ieee_is_finite(data%removal_min)).or. &
        (data%removal_min <= 0.0_real32)) &
      call fail(trim(owner)//' INVALID RADIAL PHYSICS CONTRACT.')

    call require_record(root,'LINK.MACRO',3,3,owner)
    call require_record(root,'LINK.TRACK',3,3,owner)
    call LCMGTC(root,'LINK.MACRO',12,data%link_macro)
    call LCMGTC(root,'LINK.TRACK',12,data%link_track)
    if ((len_trim(data%link_macro) == 0).or. &
        (len_trim(data%link_track) == 0)) &
      call fail(trim(owner)//' EMPTY INPUT LINK MARKER.')
    call LCMLEN(root,'LINK.BASIS',length_found,type_found)
    if (expect_basis_link) then
      if ((length_found /= 3).or.(type_found /= 3)) &
        call fail(trim(owner)//' INVALID LINK.BASIS MARKER.')
      call LCMGTC(root,'LINK.BASIS',12,data%link_basis)
      if (len_trim(data%link_basis) == 0) &
        call fail(trim(owner)//' EMPTY LINK.BASIS MARKER.')
    else
      if (length_found /= 0) &
        call fail(trim(owner)//' UNEXPECTED LINK.BASIS MARKER.')
    endif

    call require_record(root,'POD-RANK-G',data%ngroup,1,owner)
    call require_record(root,'GROUP',data%ngroup,10,owner)
    allocate(data%rank_root(data%ngroup),data%group(data%ngroup))
    call LCMGET(root,'POD-RANK-G',data%rank_root)
    if (any(data%rank_root <= 0)) &
      call fail(trim(owner)//' NONPOSITIVE POD RANK.')
    groups=LCMGID(root,'GROUP')

    nsnap_root=0
    do g=1,data%ngroup
      write(label,'(A,1X,I0)') trim(owner)//' GROUP',g
      call require_directory_item(groups,g,label)
      group_ptr=LCMGIL(groups,g)

      call require_record(group_ptr,'NREG2D',1,1,label)
      call require_record(group_ptr,'NSNAP',1,1,label)
      call require_record(group_ptr,'POD-NMODE',1,1,label)
      call LCMGET(group_ptr,'NREG2D',nreg0)
      call LCMGET(group_ptr,'NSNAP',nsnap0)
      call LCMGET(group_ptr,'POD-NMODE',nmode0)
      if ((nreg0 /= 8).or.(nsnap0 /= 3).or.(nmode0 /= 1).or. &
          (data%rank_root(g) /= nmode0)) &
        call fail(trim(label)//' INVALID POD DIMENSIONS.')
      if (g == 1) then
        nsnap_root=nsnap0
      else if (nsnap0 /= nsnap_root) then
        call fail(trim(owner)//' NSNAP CHANGES BY GROUP.')
      endif

      data%group(g)%nreg=nreg0
      data%group(g)%nsnap=nsnap0
      data%group(g)%nmode=nmode0
      allocate(data%group(g)%volume(nreg0))
      allocate(data%group(g)%basis(nreg0*nmode0))
      allocate(data%group(g)%coeff(nmode0*nsnap0))
      allocate(data%group(g)%radial(nreg0*nsnap0))
      allocate(data%group(g)%sigma(nsnap0))

      call require_record(group_ptr,'VOL2D',nreg0,2,label)
      call require_record(group_ptr,'POD-BASIS',nreg0*nmode0,2,label)
      call require_record(group_ptr,'POD-COEFF',nmode0*nsnap0,2,label)
      call require_record(group_ptr,'POD-SIGMA',nsnap0,4,label)
      call require_record(group_ptr,'POD-REC-ERR',1,4,label)
      call require_record(group_ptr,'POD-ORTHO',1,4,label)
      call require_record(group_ptr,'RADIAL-OP',nreg0*nsnap0,2,label)
      call LCMGET(group_ptr,'VOL2D',data%group(g)%volume)
      call LCMGET(group_ptr,'POD-BASIS',data%group(g)%basis)
      call LCMGET(group_ptr,'POD-COEFF',data%group(g)%coeff)
      call LCMGET(group_ptr,'POD-SIGMA',data%group(g)%sigma)
      call LCMGET(group_ptr,'POD-REC-ERR',data%group(g)%rec_err)
      call LCMGET(group_ptr,'POD-ORTHO',data%group(g)%ortho)
      call LCMGET(group_ptr,'RADIAL-OP',data%group(g)%radial)
      if (any(.not.ieee_is_finite(data%group(g)%volume)).or. &
          any(data%group(g)%volume <= 0.0_real32).or. &
          any(.not.ieee_is_finite(data%group(g)%basis)).or. &
          any(.not.ieee_is_finite(data%group(g)%coeff)).or. &
          any(.not.ieee_is_finite(data%group(g)%sigma)).or. &
          any(.not.ieee_is_finite(data%group(g)%radial)).or. &
          (.not.ieee_is_finite(data%group(g)%rec_err)).or. &
          (.not.ieee_is_finite(data%group(g)%ortho))) &
        call fail(trim(label)//' NON-FINITE POD PACKAGE.')
    enddo

    call require_record(root,'POD-SIGMA-G', &
      nsnap_root*data%ngroup,4,owner)
    data%nsnap=nsnap_root
    allocate(data%sigma_root(nsnap_root,data%ngroup))
    call LCMGET(root,'POD-SIGMA-G',data%sigma_root)
    if (any(.not.ieee_is_finite(data%sigma_root))) &
      call fail(trim(owner)//' NON-FINITE ROOT POD-SIGMA-G.')
    do g=1,data%ngroup
      if (any(real64_bits(data%sigma_root(:,g)) /= &
              real64_bits(data%group(g)%sigma))) &
        call fail(trim(owner)//' GROUP/ROOT POD-SIGMA BITS DIFFER.')
    enddo
    call LCMCL(root,1)
  end subroutine load_system


  subroutine compare_systems(reference,current)
    type(system_data), intent(in) :: reference,current
    integer :: g
    logical :: radial_bits_changed,radial_value_changed
    character(len=128) :: label

    if ((reference%signature /= current%signature).or. &
        (reference%signature /= 'L_PIJ')) &
      call fail('SYSTEM SIGNATURES DIFFER.')
    if ((reference%fixb /= 0).or.(current%fixb /= 1)) &
      call fail('SYSTEM FIXED-BASIS MARKERS ARE INVALID.')
    if ((reference%basis_type /= 'POD-BUILT').or. &
        (current%basis_type /= 'POD-FIXED')) &
      call fail('SYSTEM BASIS-TYPE MARKERS ARE INVALID.')
    if (len_trim(reference%link_basis) /= 0) &
      call fail('REFERENCE SYSTEM HAS A BASIS LINK.')
    if (len_trim(current%link_basis) == 0) &
      call fail('CURRENT SYSTEM HAS NO BASIS LINK.')
    if ((reference%link_macro /= current%link_macro).or. &
        (reference%link_track /= current%link_track)) &
      call fail('SYSTEM INPUT LINK MARKERS DIFFER.')
    if (any(reference%state /= current%state)) &
      call fail('SYSTEM STATE-VECTOR RECORDS DIFFER.')
    if (reference%ngroup /= current%ngroup) &
      call fail('SYSTEM GROUP COUNTS DIFFER.')
    if (reference%nsnap /= current%nsnap) &
      call fail('SYSTEM SNAPSHOT COUNTS DIFFER.')
    if (any(reference%rank_root /= current%rank_root)) &
      call fail('ROOT POD-RANK-G RECORDS DIFFER.')
    if (any(real64_bits(reference%sigma_root) /= &
            real64_bits(current%sigma_root))) &
      call fail('ROOT POD-SIGMA-G RECORDS DIFFER BITWISE.')

    radial_bits_changed=.false.
    radial_value_changed=.false.
    do g=1,reference%ngroup
      write(label,'(A,I0)') 'GROUP ',g
      if (reference%group(g)%nreg /= current%group(g)%nreg) &
        call fail(trim(label)//' NREG2D RECORDS DIFFER.')
      if (reference%group(g)%nsnap /= current%group(g)%nsnap) &
        call fail(trim(label)//' NSNAP RECORDS DIFFER.')
      if (reference%group(g)%nmode /= current%group(g)%nmode) &
        call fail(trim(label)//' POD-NMODE RECORDS DIFFER.')
      if (any(real32_bits(reference%group(g)%volume) /= &
              real32_bits(current%group(g)%volume))) &
        call fail(trim(label)//' VOL2D RECORDS DIFFER BITWISE.')
      if (any(real32_bits(reference%group(g)%basis) /= &
              real32_bits(current%group(g)%basis))) &
        call fail(trim(label)//' POD-BASIS RECORDS DIFFER BITWISE.')
      if (any(real32_bits(reference%group(g)%coeff) /= &
              real32_bits(current%group(g)%coeff))) &
        call fail(trim(label)//' POD-COEFF RECORDS DIFFER BITWISE.')
      if (any(real64_bits(reference%group(g)%sigma) /= &
              real64_bits(current%group(g)%sigma))) &
        call fail(trim(label)//' POD-SIGMA RECORDS DIFFER BITWISE.')
      if (real64_bits(reference%group(g)%rec_err) /= &
          real64_bits(current%group(g)%rec_err)) &
        call fail(trim(label)//' POD-REC-ERR RECORDS DIFFER BITWISE.')
      if (real64_bits(reference%group(g)%ortho) /= &
          real64_bits(current%group(g)%ortho)) &
        call fail(trim(label)//' POD-ORTHO RECORDS DIFFER BITWISE.')
      if (any(real32_bits(reference%group(g)%radial) /= &
              real32_bits(current%group(g)%radial))) &
        radial_bits_changed=.true.
      if (any(reference%group(g)%radial /= current%group(g)%radial)) &
        radial_value_changed=.true.
    enddo
    if ((.not.radial_bits_changed).or.(.not.radial_value_changed)) &
      call fail('NO LIVE RADIAL-OP NUMERIC VALUE CHANGED.')
  end subroutine compare_systems


  subroutine load_canonical_state(path,expected_fixb,expected_type, &
      expect_saved_defect,data,owner)
    character(len=*), intent(in) :: path,expected_type,owner
    integer, intent(in) :: expected_fixb
    logical, intent(in) :: expect_saved_defect
    type(canonical_state), intent(out) :: data
    type(c_ptr) :: root
    integer :: g,ngrp,nsnap,ncoef,total_basis,total_gram

    call LCMOP(root,path,2,2,0)
    call require_record(root,'SIGNATURE',3,3,owner)
    call LCMGTC(root,'SIGNATURE',12,data%signature)
    if (data%signature /= 'L_FLUX') &
      call fail(trim(owner)//' L_FLUX SIGNATURE EXPECTED.')
    call require_record(root,'STATE-VECTOR',nstate,1,owner)
    call LCMGET(root,'STATE-VECTOR',data%state)

    call require_record(root,'SPOT-X-DIMS',4,1,owner)
    call LCMGET(root,'SPOT-X-DIMS',data%dims)
    ngrp=data%dims(2)
    nsnap=data%dims(3)
    ncoef=data%dims(4)
    if ((data%dims(1) /= 1).or.(ngrp /= 370).or. &
        (nsnap /= 3).or.(ncoef /= 1110).or.(data%state(1) /= ngrp)) &
      call fail(trim(owner)//' INVALID CANONICAL DIMENSIONS.')

    allocate(data%rank(ngrp))
    allocate(data%offset(ngrp+1))
    allocate(data%gram_offset(ngrp+1))
    allocate(data%basis_offset(ngrp+1))
    call require_record(root,'SPOT-X-RANK',ngrp,1,owner)
    call require_record(root,'SPOT-X-OFF',ngrp+1,1,owner)
    call require_record(root,'SPOT-X-GOFF',ngrp+1,1,owner)
    call require_record(root,'SPOT-X-BOFF',ngrp+1,1,owner)
    call LCMGET(root,'SPOT-X-RANK',data%rank)
    call LCMGET(root,'SPOT-X-OFF',data%offset)
    call LCMGET(root,'SPOT-X-GOFF',data%gram_offset)
    call LCMGET(root,'SPOT-X-BOFF',data%basis_offset)
    if (any(data%rank <= 0).or.(data%offset(1) /= 0).or. &
        (data%gram_offset(1) /= 0).or.(data%basis_offset(1) /= 0).or. &
        (data%offset(ngrp+1) /= ncoef)) &
      call fail(trim(owner)//' INVALID CANONICAL LAYOUT.')
    do g=1,ngrp
      if (data%offset(g+1)-data%offset(g) /= nsnap*data%rank(g)) &
        call fail(trim(owner)//' INVALID COORDINATE OFFSETS.')
      if (data%gram_offset(g+1)-data%gram_offset(g) /= &
          data%rank(g)*data%rank(g)) &
        call fail(trim(owner)//' INVALID GRAM OFFSETS.')
      if (data%basis_offset(g+1) <= data%basis_offset(g)) &
        call fail(trim(owner)//' INVALID BASIS OFFSETS.')
    enddo

    total_basis=data%basis_offset(ngrp+1)
    total_gram=data%gram_offset(ngrp+1)
    allocate(data%basis(total_basis))
    allocate(data%coordinates(ncoef))
    allocate(data%leakage(ngrp*nsnap))
    allocate(data%height(nsnap))
    allocate(data%gram(total_gram))
    allocate(data%offspace(ngrp*nsnap))
    call require_record(root,'SPOT-X-BASIS',total_basis,2,owner)
    call require_record(root,'SPOT-X-A',ncoef,4,owner)
    call require_record(root,'SPOT-X-L',ngrp*nsnap,4,owner)
    call require_record(root,'SPOT-X-H',nsnap,4,owner)
    call require_record(root,'SPOT-X-GRAM',total_gram,4,owner)
    call require_record(root,'K-EFFECTIVE',1,2,owner)
    call require_record(root,'SPOT-X-RHO',1,4,owner)
    call require_record(root,'SPOT-X-NORM',1,4,owner)
    call require_record(root,'SPOT-X-PERP',ngrp*nsnap,4,owner)
    call require_record(root,'SPOT-X-GERR',1,4,owner)
    call require_record(root,'SPOT-X-FIXB',1,1,owner)
    call require_record(root,'SPOT-X-NID',3,3,owner)
    call require_record(root,'SPOT-X-BTYP',3,3,owner)
    call LCMGET(root,'SPOT-X-BASIS',data%basis)
    call LCMGET(root,'SPOT-X-A',data%coordinates)
    call LCMGET(root,'SPOT-X-L',data%leakage)
    call LCMGET(root,'SPOT-X-H',data%height)
    call LCMGET(root,'SPOT-X-GRAM',data%gram)
    call LCMGET(root,'K-EFFECTIVE',data%keff)
    call LCMGET(root,'SPOT-X-RHO',data%rho)
    call LCMGET(root,'SPOT-X-NORM',data%norm)
    call LCMGET(root,'SPOT-X-PERP',data%offspace)
    call LCMGET(root,'SPOT-X-GERR',data%gram_error)
    call LCMGET(root,'SPOT-X-FIXB',data%fixb)
    call LCMGTC(root,'SPOT-X-NID',12,data%norm_id)
    call LCMGTC(root,'SPOT-X-BTYP',12,data%basis_type)

    if ((data%fixb /= expected_fixb).or. &
        (data%basis_type /= expected_type)) &
      call fail(trim(owner)//' CANONICAL BASIS MARKERS ARE INVALID.')
    if (data%norm_id /= 'NUFISS-UNIT') &
      call fail(trim(owner)//' NORMALIZATION ID IS INVALID.')
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
      call fail(trim(owner)//' NON-FINITE OR INVALID CANONICAL FIELD.')
    if (real64_bits(data%rho) /= &
        real64_bits(1.0_real64/real(data%keff,real64))) &
      call fail(trim(owner)//' INVERSE-EIGENVALUE IDENTITY FAILED.')

    data%has_saved_defect=expect_saved_defect
    if (expect_saved_defect) then
      call require_record(root,'SPOT-X-RRHO',1,4,owner)
      call require_record(root,'SPOT-X-RLEAK',1,4,owner)
      call require_record(root,'SPOT-X-DLEAK',1,4,owner)
      call require_record(root,'SPOT-X-RA',1,4,owner)
      call LCMGET(root,'SPOT-X-RRHO',data%saved_defect(1))
      call LCMGET(root,'SPOT-X-RLEAK',data%saved_defect(2))
      call LCMGET(root,'SPOT-X-DLEAK',data%saved_defect(3))
      call LCMGET(root,'SPOT-X-RA',data%saved_defect(4))
      if (any(.not.ieee_is_finite(data%saved_defect)).or. &
          any(data%saved_defect < 0.0_real64)) &
        call fail(trim(owner)//' INVALID SAVED MAP DEFECT.')
    else
      call require_absent(root,'SPOT-X-RRHO',owner)
      call require_absent(root,'SPOT-X-RLEAK',owner)
      call require_absent(root,'SPOT-X-DLEAK',owner)
      call require_absent(root,'SPOT-X-RA',owner)
    endif
    call LCMCL(root,1)
  end subroutine load_canonical_state


  subroutine compare_state_to_system(state0,system0,owner)
    type(canonical_state), intent(in) :: state0
    type(system_data), intent(in) :: system0
    character(len=*), intent(in) :: owner
    integer :: g,first,last

    if (state0%dims(2) /= system0%ngroup) &
      call fail(trim(owner)//' GROUP COUNT DIFFERS FROM SYSTEM.')
    if (any(state0%rank /= system0%rank_root)) &
      call fail(trim(owner)//' POD RANK DIFFERS FROM SYSTEM.')
    do g=1,system0%ngroup
      if (state0%dims(3) /= system0%group(g)%nsnap) &
        call fail(trim(owner)//' SNAPSHOT COUNT DIFFERS FROM SYSTEM.')
      first=state0%basis_offset(g)+1
      last=state0%basis_offset(g+1)
      if (last-first+1 /= &
          system0%group(g)%nreg*system0%group(g)%nmode) &
        call fail(trim(owner)//' BASIS EXTENT DIFFERS FROM SYSTEM.')
      if (any(real32_bits(state0%basis(first:last)) /= &
              real32_bits(system0%group(g)%basis))) &
        call fail(trim(owner)//' BASIS BITS DIFFER FROM SYSTEM.')
    enddo
  end subroutine compare_state_to_system


  subroutine compare_states_and_defects(previous,current)
    type(canonical_state), intent(in) :: previous,current
    real(real64) :: recomputed(4)

    if ((previous%signature /= 'L_FLUX').or. &
        (current%signature /= previous%signature)) &
      call fail('CANONICAL STATE SIGNATURES DIFFER.')
    if (any(previous%dims /= current%dims)) &
      call fail('CANONICAL STATE DIMENSIONS DIFFER.')
    if (any(previous%rank /= current%rank).or. &
        any(previous%offset /= current%offset).or. &
        any(previous%gram_offset /= current%gram_offset).or. &
        any(previous%basis_offset /= current%basis_offset)) &
      call fail('CANONICAL STATE LAYOUTS DIFFER.')
    if (any(real32_bits(previous%basis) /= &
            real32_bits(current%basis))) &
      call fail('CANONICAL BASIS CHANGED BITWISE.')
    if (any(real64_bits(previous%gram) /= &
            real64_bits(current%gram))) &
      call fail('CANONICAL GRAM MATRIX CHANGED BITWISE.')
    if (any(real64_bits(previous%height) /= &
            real64_bits(current%height))) &
      call fail('CANONICAL HEIGHT CHANGED BITWISE.')
    if ((previous%norm_id /= current%norm_id).or. &
        (current%norm_id /= 'NUFISS-UNIT')) &
      call fail('CANONICAL NORMALIZATION IDS DIFFER.')
    if ((previous%fixb /= 0).or.(current%fixb /= 1).or. &
        (previous%basis_type /= 'POD-BUILT').or. &
        (current%basis_type /= 'POD-FIXED')) &
      call fail('CANONICAL FIXED-BASIS MARKERS ARE INVALID.')
    if (.not.current%has_saved_defect) &
      call fail('STATE ONE HAS NO SAVED MAP DEFECT.')

    call recompute_map_defect(previous,current,recomputed)
    if (any(real64_bits(recomputed) /= &
            real64_bits(current%saved_defect))) &
      call fail('RECOMPUTED MAP DEFECT DIFFERS BITWISE.')
  end subroutine compare_states_and_defects


  subroutine check_restart_archive(path,previous,current)
    character(len=*), intent(in) :: path
    type(canonical_state), intent(in) :: previous,current
    type(c_ptr) :: root,fluxes,systems,flux_ptr,system_ptr
    integer :: listdim,isnap,ngrp,fs_equation
    real(real32) :: l1_error,fs_keff,fs_min,fs_qsum,fs_rbal
    real(real64) :: iter_keff
    real(real32), allocatable :: flux_leak(:),system_leak(:)
    character(len=12) :: signature
    character(len=80) :: owner

    ngrp=current%dims(2)
    call LCMOP(root,path,2,2,0)
    call require_record(root,'SIGNATURE',3,3,'RESTART ARCHIVE')
    call LCMGTC(root,'SIGNATURE',12,signature)
    if (signature /= 'L_ARCHIVE') &
      call fail('RESTART L_ARCHIVE SIGNATURE EXPECTED.')
    call require_record(root,'LISTDIM',1,1,'RESTART ARCHIVE')
    call LCMGET(root,'LISTDIM',listdim)
    if (listdim /= current%dims(3)) &
      call fail('RESTART ARCHIVE PLANE COUNT CHANGED.')
    call require_record(root,'TRACK',listdim,10,'RESTART ARCHIVE')
    call require_record(root,'MICROLIB2',listdim,10,'RESTART ARCHIVE')
    call require_record(root,'SYSTEM',listdim,10,'RESTART ARCHIVE')
    call require_record(root,'FLUX',listdim,10,'RESTART ARCHIVE')
    call require_record(root,'SPOT-ITER-K',1,4,'RESTART ARCHIVE')
    call require_record(root,'SPOT-L1-ERR',1,2,'RESTART ARCHIVE')
    call LCMGET(root,'SPOT-ITER-K',iter_keff)
    call LCMGET(root,'SPOT-L1-ERR',l1_error)
    if ((.not.ieee_is_finite(iter_keff)).or. &
        (real64_bits(iter_keff) /= &
         real64_bits(real(current%keff,real64)))) &
      call fail('RESTART ARCHIVE K-EFFECTIVE CHANGED.')
    if ((.not.ieee_is_finite(l1_error)).or.(l1_error < 0.0_real32).or. &
        (real32_bits(l1_error) /= &
         real32_bits(real(current%saved_defect(3),real32)))) &
      call fail('RESTART ARCHIVE LEAKAGE ERROR CHANGED.')

    fluxes=LCMGID(root,'FLUX')
    systems=LCMGID(root,'SYSTEM')
    allocate(flux_leak(ngrp),system_leak(ngrp))
    do isnap=1,listdim
      write(owner,'(A,I0)') 'RESTART PLANE ',isnap
      call require_directory_item(fluxes,isnap,trim(owner)//' FLUX')
      call require_directory_item(systems,isnap,trim(owner)//' SYSTEM')
      flux_ptr=LCMGIL(fluxes,isnap)
      system_ptr=LCMGIL(systems,isnap)
      call require_record(flux_ptr,'SIGNATURE',3,3,owner)
      call require_record(system_ptr,'SIGNATURE',3,3,owner)
      call LCMGTC(flux_ptr,'SIGNATURE',12,signature)
      if (signature /= 'L_FLUX') &
        call fail(trim(owner)//' L_FLUX SIGNATURE EXPECTED.')
      call LCMGTC(system_ptr,'SIGNATURE',12,signature)
      if (signature /= 'L_PIJ') &
        call fail(trim(owner)//' L_PIJ SIGNATURE EXPECTED.')

      call require_record(flux_ptr,'SPOT-LEAK1D',ngrp,2,owner)
      call require_record(system_ptr,'SPOT-LEAK1D',ngrp,2,owner)
      call LCMGET(flux_ptr,'SPOT-LEAK1D',flux_leak)
      call LCMGET(system_ptr,'SPOT-LEAK1D',system_leak)
      if (any(.not.ieee_is_finite(flux_leak)).or. &
          any(.not.ieee_is_finite(system_leak))) &
        call fail(trim(owner)//' NON-FINITE LEAKAGE.')
      if (any(real32_bits(flux_leak) /= real32_bits(real( &
          current%leakage((isnap-1)*ngrp+1:isnap*ngrp),real32)))) &
        call fail(trim(owner)//' RETURNED LEAKAGE BITS CHANGED.')
      if (any(real32_bits(system_leak) /= real32_bits(real( &
          previous%leakage((isnap-1)*ngrp+1:isnap*ngrp),real32)))) &
        call fail(trim(owner)//' INPUT LEAKAGE BITS CHANGED.')

      call require_record(flux_ptr,'SPOT-FS-EQN',1,1,owner)
      call require_record(flux_ptr,'SPOT-FS-K',1,2,owner)
      call require_record(flux_ptr,'SPOT-FS-MIN',1,2,owner)
      call require_record(flux_ptr,'SPOT-FS-QSUM',1,2,owner)
      call require_record(flux_ptr,'SPOT-FS-RBAL',1,2,owner)
      call LCMGET(flux_ptr,'SPOT-FS-EQN',fs_equation)
      call LCMGET(flux_ptr,'SPOT-FS-K',fs_keff)
      call LCMGET(flux_ptr,'SPOT-FS-MIN',fs_min)
      call LCMGET(flux_ptr,'SPOT-FS-QSUM',fs_qsum)
      call LCMGET(flux_ptr,'SPOT-FS-RBAL',fs_rbal)
      if ((fs_equation /= 1).or. &
          (real32_bits(fs_keff) /= real32_bits(previous%keff)).or. &
          (.not.ieee_is_finite(fs_min)).or.(fs_min <= 0.0_real32).or. &
          (.not.ieee_is_finite(fs_qsum)).or.(fs_qsum <= 0.0_real32).or. &
          (.not.ieee_is_finite(fs_rbal)).or.(fs_rbal < 0.0_real32)) &
        call fail(trim(owner)//' INVALID FIXED-SOURCE CONTRACT.')
    enddo
    deallocate(system_leak,flux_leak)
    call LCMCL(root,1)
  end subroutine check_restart_archive


  subroutine recompute_map_defect(previous,current,defect)
    type(canonical_state), intent(in) :: previous,current
    real(real64), intent(out) :: defect(4)
    integer :: ngrp,nsnap,igr,isnap,a,b,nmode
    integer :: index_a,index_b,index_g
    real(real64) :: r_rho,r_leak,d_leak,r_a
    real(real64) :: leak_scale_current,leak_scale_previous,leak_scale
    real(real64) :: numerator,denominator,delta

    ngrp=current%dims(2)
    nsnap=current%dims(3)
    r_rho=abs(current%rho-previous%rho)
    d_leak=maxval(abs(current%leakage-previous%leakage))
    leak_scale_current=maxval(abs(current%leakage))
    leak_scale_previous=maxval(abs(previous%leakage))
    leak_scale=max(leak_scale_current,leak_scale_previous)
    if (leak_scale == 0.0_real64) then
      if (d_leak /= 0.0_real64) &
        call fail('INVALID ZERO-LEAKAGE BRANCH.')
      r_leak=0.0_real64
    else
      r_leak=d_leak/leak_scale
    endif

    numerator=0.0_real64
    denominator=0.0_real64
    do igr=1,ngrp
      nmode=current%rank(igr)
      do isnap=1,nsnap
        do a=1,nmode
          index_a=current%offset(igr)+(isnap-1)*nmode+a
          delta=current%coordinates(index_a)- &
            previous%coordinates(index_a)
          do b=1,nmode
            index_b=current%offset(igr)+(isnap-1)*nmode+b
            index_g=current%gram_offset(igr)+(b-1)*nmode+a
            numerator=numerator+current%height(isnap)*delta* &
              current%gram(index_g)*(current%coordinates(index_b)- &
              previous%coordinates(index_b))
            denominator=denominator+current%height(isnap)* &
              current%coordinates(index_a)*current%gram(index_g)* &
              current%coordinates(index_b)
          enddo
        enddo
      enddo
    enddo
    if ((.not.ieee_is_finite(numerator)).or.(numerator < 0.0_real64).or. &
        (.not.ieee_is_finite(denominator)).or. &
        (denominator <= 0.0_real64)) &
      call fail('INVALID CANONICAL COORDINATE NORM.')
    r_a=sqrt(numerator/denominator)
    if ((.not.ieee_is_finite(r_rho)).or. &
        (.not.ieee_is_finite(r_leak)).or. &
        (.not.ieee_is_finite(d_leak)).or. &
        (.not.ieee_is_finite(r_a))) &
      call fail('NON-FINITE RECOMPUTED MAP DEFECT.')
    defect=(/r_rho,r_leak,d_leak,r_a/)
  end subroutine recompute_map_defect


  subroutine require_record(ptr,name,length_expected,type_expected,owner)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,owner
    integer, intent(in) :: length_expected,type_expected
    integer :: length_found,type_found

    call LCMLEN(ptr,name,length_found,type_found)
    if ((length_found /= length_expected).or. &
        (type_found /= type_expected)) then
      write(0,'(A,1X,A,4(1X,I0))') trim(owner)//' INVALID RECORD', &
        trim(name),length_found,type_found,length_expected,type_expected
      call fail('RECORD CONTRACT FAILURE.')
    endif
  end subroutine require_record


  subroutine require_absent(ptr,name,owner)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,owner
    integer :: length_found,type_found

    call LCMLEN(ptr,name,length_found,type_found)
    if (length_found /= 0) &
      call fail(trim(owner)//' UNEXPECTED RECORD '//trim(name)//'.')
  end subroutine require_absent


  subroutine require_directory_item(list_ptr,index0,owner)
    type(c_ptr), intent(in) :: list_ptr
    integer, intent(in) :: index0
    character(len=*), intent(in) :: owner
    integer :: length_found,type_found

    call LCMLEL(list_ptr,index0,length_found,type_found)
    if ((length_found /= -1).or.(type_found /= 0)) &
      call fail(trim(owner)//' LIST ITEM IS NOT A DIRECTORY.')
  end subroutine require_directory_item


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

    write(0,'(A)') 'ONE-MAP-XSM ERROR: '//trim(message)
    error stop 2
  end subroutine fail

end program check_one_map_xsm
