program check_one_map_xsm
  ! Independent Ganlib-only, read-only audit of one fixed-space SPOT map.
  !
  !   check_one_map_xsm basis_reference.xsm state1_system.xsm \
  !     state0_axial.xsm state1_axial.xsm state1_snapshots.xsm
  !   check_one_map_xsm --continued basis_reference.xsm \
  !     state2_system.xsm state1_axial.xsm state2_axial.xsm \
  !     state2_snapshots.xsm
  !   check_one_map_xsm --reencoded basis_reference.xsm \
  !     state1_system.xsm reencoded_parent.xsm state1_axial.xsm \
  !     state1_snapshots.xsm
  !   check_one_map_xsm --directions state6_axial.xsm \
  !     state7_axial.xsm state8_axial.xsm
  !   check_one_map_xsm --rank2-directions reencoded_parent.xsm \
  !     state1_axial.xsm state2_axial.xsm
  !   check_one_map_xsm --mode2 rank1_basis.xsm rank1_parent.xsm \
  !     rank2_system.xsm rank2_parent.xsm rank2_current.xsm
  !
  ! No Dragon, SPOT, assembly, transport, or production convergence routine
  ! is linked or called. The standard one-map modes read five archived XSM
  ! objects, verify the fixed POD package bit for bit, require a live
  ! RADIAL-OP change, and independently recompute the canonical defects.
  ! Direction mode reads three frozen canonical states and describes their
  ! two stored increments.
  ! Mode-2 mode exactly partitions one archived rank-2 update in its stored
  ! volume Gram metric; it does not evaluate another nonlinear map.
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
  character(len=32) :: mode
  type(system_data) :: reference_system,current_system,rank1_system
  type(canonical_state) :: previous_state,current_state
  type(canonical_state) :: rank1_parent_state
  type(canonical_state) :: direction_state(3)
  integer :: i,argument_offset
  logical :: continued,reencoded,direction_mode,mode2_mode
  logical :: reencoded_first_direction

  continued=.false.
  reencoded=.false.
  direction_mode=.false.
  mode2_mode=.false.
  reencoded_first_direction=.false.
  argument_offset=0
  if (command_argument_count() == 4) then
    call get_command_argument(1,mode)
    if (trim(mode) == '--rank2-directions') then
      reencoded_first_direction=.true.
    else if (trim(mode) /= '--directions') then
      call fail('ONLY --directions OR --rank2-directions IS ACCEPTED IN '// &
        'FOUR-ARGUMENT MODE.')
    endif
    direction_mode=.true.
    do i=1,3
      call get_command_argument(i+1,paths(i))
      if (len_trim(paths(i)) == 0) call fail('EMPTY XSM PATH ARGUMENT.')
      if (len_trim(paths(i)) > max_xsm_path) &
        call fail('XSM PATH ARGUMENT EXCEEDS GANLIB LIMIT.')
    enddo
  else if (command_argument_count() == 6) then
    call get_command_argument(1,mode)
    if (trim(mode) == '--continued') then
      continued=.true.
    else if (trim(mode) == '--reencoded') then
      reencoded=.true.
    else if (trim(mode) == '--mode2') then
      mode2_mode=.true.
      do i=1,5
        call get_command_argument(i+1,paths(i))
        if (len_trim(paths(i)) == 0) &
          call fail('EMPTY XSM PATH ARGUMENT.')
        if (len_trim(paths(i)) > max_xsm_path) &
          call fail('XSM PATH ARGUMENT EXCEEDS GANLIB LIMIT.')
      enddo
    else
      call fail('ONLY --continued, --reencoded OR --mode2 IS ACCEPTED IN '// &
        'SIX-ARGUMENT MODE.')
    endif
    if (.not.mode2_mode) argument_offset=1
  else if (command_argument_count() /= 5) then
    call fail('EXPECTED [--continued|--reencoded] BASIS, SYSTEM, '// &
      'PREVIOUS, CURRENT, SNAP.')
  endif
  if ((.not.direction_mode).and.(.not.mode2_mode)) then
    do i=1,5
      call get_command_argument(i+argument_offset,paths(i))
      if (len_trim(paths(i)) == 0) call fail('EMPTY XSM PATH ARGUMENT.')
      if (len_trim(paths(i)) > max_xsm_path) &
        call fail('XSM PATH ARGUMENT EXCEEDS GANLIB LIMIT.')
    enddo
  endif

  if (mode2_mode) then
    call load_system(trim(paths(1)),0,0,'POD-BUILT',.false., &
      rank1_system,'RANK1 BASIS')
    call load_canonical_state(trim(paths(2)),1,'POD-FIXED',.true., &
      rank1_parent_state,'RANK1 RAW PARENT')
    call load_system(trim(paths(3)),1,3,'POD-FIXED',.true., &
      current_system,'RANK2 SYSTEM')
    call load_canonical_state(trim(paths(4)),1,'POD-FIXED',.false., &
      previous_state,'RANK2 PARENT')
    call load_canonical_state(trim(paths(5)),1,'POD-FIXED',.true., &
      current_state,'RANK2 CURRENT')
    call compare_state_to_system(rank1_parent_state,rank1_system, &
      'RANK1 RAW PARENT')
    call compare_state_to_system(previous_state,current_system, &
      'RANK2 PARENT')
    call compare_state_to_system(current_state,current_system, &
      'RANK2 CURRENT')
    call compare_states_and_defects(previous_state,current_state,.false., &
      .true.)
    call report_rank2_mode_diagnostics(rank1_system,rank1_parent_state, &
      current_system,previous_state,current_state)
    write(6,'(A)') 'MODE2-DIAG COMPLETE'
    stop
  endif

  if (direction_mode) then
    call load_canonical_state(trim(paths(1)),1,'POD-FIXED', &
      .not.reencoded_first_direction,direction_state(1), &
      'DIRECTION STATE X1')
    call load_canonical_state(trim(paths(2)),1,'POD-FIXED',.true., &
      direction_state(2),'DIRECTION STATE X2')
    call load_canonical_state(trim(paths(3)),1,'POD-FIXED',.true., &
      direction_state(3),'DIRECTION STATE X3')
    if (reencoded_first_direction.and. &
        any(direction_state(1)%rank /= 2)) &
      call fail('RANK2-DIRECTION MODE REQUIRES RANK TWO.')
    call compare_states_and_defects(direction_state(1),direction_state(2), &
      .not.reencoded_first_direction,reencoded_first_direction)
    if (reencoded_first_direction) then
      write(6,'(A)') &
        'PICARD-DIRECTION MAP12 REENCODED-PARENT RAW-DEFECT BITWISE PASS'
    else
      write(6,'(A)') 'PICARD-DIRECTION MAP12 RAW-DEFECT BITWISE PASS'
    endif
    call compare_states_and_defects(direction_state(2), &
      direction_state(3),.true.,.false.)
    write(6,'(A)') 'PICARD-DIRECTION MAP23 RAW-DEFECT BITWISE PASS'
    call report_update_directions(direction_state(1),direction_state(2), &
      direction_state(3))
    write(6,'(A)') 'PICARD-DIRECTION COMPLETE'
    stop
  endif

  call load_system(trim(paths(1)),0,0,'POD-BUILT',.false., &
    reference_system,'BASIS REFERENCE')
  call load_system(trim(paths(2)),1,3,'POD-FIXED',.true., &
    current_system,'CURRENT SYSTEM')
  call compare_systems(reference_system,current_system)

  if (continued) then
    call load_canonical_state(trim(paths(3)),1,'POD-FIXED',.true., &
      previous_state,'PREVIOUS CONTINUED STATE')
  else if (reencoded) then
    call load_canonical_state(trim(paths(3)),1,'POD-FIXED',.false., &
      previous_state,'REENCODED PARENT STATE')
  else
    call load_canonical_state(trim(paths(3)),0,'POD-BUILT',.false., &
      previous_state,'STATE ZERO')
  endif
  call load_canonical_state(trim(paths(4)),1,'POD-FIXED',.true., &
    current_state,'CURRENT FIXED-BASIS STATE')
  call compare_state_to_system(previous_state,reference_system, &
    'PREVIOUS STATE')
  call compare_state_to_system(current_state,current_system, &
    'CURRENT STATE')
  call compare_states_and_defects(previous_state,current_state,continued, &
    reencoded)
  call check_restart_archive(trim(paths(5)),previous_state,current_state)

  if (reencoded) &
    write(6,'(A)') 'ONE-MAP-XSM REENCODED-PARENT NO-STALE-DEFECT PASS'
  write(6,'(A)') 'ONE-MAP-XSM POD-PACKAGE BITWISE PASS'
  write(6,'(A)') 'ONE-MAP-XSM RADIAL-OP LIVE-CHANGE PASS'
  write(6,'(A)') 'ONE-MAP-XSM RAW-RADIAL-POSITIVITY PASS'
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
      if ((nreg0 /= 8).or.(nsnap0 /= 3).or.(nmode0 <= 0).or. &
          (nmode0 > nsnap0).or. &
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
    integer :: g,ngrp,nsnap,ncoef,expected_ncoef,total_basis,total_gram

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
        (nsnap /= 3).or.(data%state(1) /= ngrp)) &
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
    if (any(data%rank <= 0).or.any(data%rank > nsnap)) &
      call fail(trim(owner)//' INVALID CANONICAL LAYOUT.')
    expected_ncoef=nsnap*sum(data%rank)
    if ((ncoef /= expected_ncoef).or.(data%offset(1) /= 0).or. &
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


  subroutine compare_states_and_defects(previous,current,continued_mode, &
      reencoded_mode)
    type(canonical_state), intent(in) :: previous,current
    logical, intent(in) :: continued_mode,reencoded_mode
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
    if (continued_mode.and.reencoded_mode) &
      call fail('PREVIOUS STATE MODE IS AMBIGUOUS.')
    if (continued_mode) then
      if ((previous%fixb /= 1).or. &
          (previous%basis_type /= 'POD-FIXED').or. &
          (.not.previous%has_saved_defect)) &
        call fail('PREVIOUS CONTINUED-STATE MARKERS ARE INVALID.')
    else if (reencoded_mode) then
      if ((previous%fixb /= 1).or. &
          (previous%basis_type /= 'POD-FIXED').or. &
          previous%has_saved_defect) &
        call fail('REENCODED PARENT-STATE MARKERS ARE INVALID.')
    else
      if ((previous%fixb /= 0).or. &
          (previous%basis_type /= 'POD-BUILT').or. &
          previous%has_saved_defect) &
        call fail('INITIAL PREVIOUS-STATE MARKERS ARE INVALID.')
    endif
    if ((current%fixb /= 1).or. &
        (current%basis_type /= 'POD-FIXED')) &
      call fail('CURRENT FIXED-BASIS MARKERS ARE INVALID.')
    if (.not.current%has_saved_defect) &
      call fail('CURRENT STATE HAS NO SAVED MAP DEFECT.')

    call recompute_map_defect(previous,current,recomputed)
    if (any(real64_bits(recomputed) /= &
            real64_bits(current%saved_defect))) &
      call fail('RECOMPUTED MAP DEFECT DIFFERS BITWISE.')
  end subroutine compare_states_and_defects


  subroutine check_restart_archive(path,previous,current)
    character(len=*), intent(in) :: path
    type(canonical_state), intent(in) :: previous,current
    type(c_ptr) :: root,tracks,fluxes,systems,track_ptr,flux_ptr,system_ptr
    type(c_ptr) :: radial_fluxes
    integer :: listdim,isnap,ngrp,fs_equation,g,r
    integer :: radial_state(nstate),radial_nreg,radial_nunk
    real(real32) :: l1_error,fs_keff,fs_min,fs_qsum,fs_rbal
    real(real64) :: iter_keff
    real(real32), allocatable :: flux_leak(:),system_leak(:)
    real(real32), allocatable :: radial_flux(:)
    integer, allocatable :: radial_key(:)
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

    tracks=LCMGID(root,'TRACK')
    fluxes=LCMGID(root,'FLUX')
    systems=LCMGID(root,'SYSTEM')
    allocate(flux_leak(ngrp),system_leak(ngrp))
    do isnap=1,listdim
      write(owner,'(A,I0)') 'RESTART PLANE ',isnap
      call require_directory_item(fluxes,isnap,trim(owner)//' FLUX')
      call require_directory_item(systems,isnap,trim(owner)//' SYSTEM')
      call require_directory_item(tracks,isnap,trim(owner)//' TRACK')
      track_ptr=LCMGIL(tracks,isnap)
      flux_ptr=LCMGIL(fluxes,isnap)
      system_ptr=LCMGIL(systems,isnap)
      call require_record(track_ptr,'STATE-VECTOR',nstate,1,owner)
      call LCMGET(track_ptr,'STATE-VECTOR',radial_state)
      radial_nreg=radial_state(1)
      radial_nunk=radial_state(2)
      if ((radial_nreg <= 0).or.(radial_nunk <= 0)) &
        call fail(trim(owner)//' INVALID RADIAL DIMENSIONS.')
      call require_record(track_ptr,'KEYFLX$ANIS',radial_nreg,1,owner)
      allocate(radial_key(radial_nreg),radial_flux(radial_nunk))
      call LCMGET(track_ptr,'KEYFLX$ANIS',radial_key)
      if (any(radial_key < 1).or.any(radial_key > radial_nunk)) &
        call fail(trim(owner)//' INVALID RADIAL FLUX KEYS.')
      call require_record(flux_ptr,'SIGNATURE',3,3,owner)
      call require_record(system_ptr,'SIGNATURE',3,3,owner)
      call LCMGTC(flux_ptr,'SIGNATURE',12,signature)
      if (signature /= 'L_FLUX') &
        call fail(trim(owner)//' L_FLUX SIGNATURE EXPECTED.')
      call LCMGTC(system_ptr,'SIGNATURE',12,signature)
      if (signature /= 'L_PIJ') &
        call fail(trim(owner)//' L_PIJ SIGNATURE EXPECTED.')
      call require_record(flux_ptr,'FLUX',ngrp,10,owner)
      radial_fluxes=LCMGID(flux_ptr,'FLUX')
      do g=1,ngrp
        call require_list_item(radial_fluxes,g,radial_nunk,2,owner)
        call LCMGDL(radial_fluxes,g,radial_flux)
        if (any(.not.ieee_is_finite(radial_flux))) &
          call fail(trim(owner)//' NON-FINITE RAW RADIAL FLUX.')
        do r=1,radial_nreg
          if (radial_flux(radial_key(r)) <= 0.0_real32) &
            call fail(trim(owner)//' NONPOSITIVE RAW RADIAL SCALAR FLUX.')
        enddo
      enddo

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
      deallocate(radial_flux,radial_key)
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


  subroutine report_rank2_mode_diagnostics(rank1_basis,rank1_parent, &
      rank2_system,rank2_parent,rank2_current)
    type(system_data), intent(in) :: rank1_basis,rank2_system
    type(canonical_state), intent(in) :: rank1_parent,rank2_parent
    type(canonical_state), intent(in) :: rank2_current
    integer :: g,s,i,a,b,nreg,nsnap,ngrp,index_a,index_b,index_g
    integer :: top_group,top_cell_group,top_cell_snap,hot_index,hot_ties
    integer :: max_delta_group(2),max_delta_snap(2),nterms
    real(real64) :: numerator,denominator,numerator_abs
    real(real64) :: numerator_part(3),current_part(3),parent_part(3)
    real(real64) :: term,delta_a,delta_b,weight_sum,weight
    real(real64) :: component_sum,closure,closure_bound
    real(real64) :: gamma_full,gamma_part,gamma_combine
    real(real64) :: projection_delta,projection_norm,plane1,plane2
    real(real64) :: gram_value,d_leak,leak_scale
    real(real64) :: max_delta(2),delta_value
    real(real64), allocatable :: group_num(:),snapshot_num(:),cell_num(:,:)

    ngrp=rank2_current%dims(2)
    nsnap=rank2_current%dims(3)
    if ((rank1_basis%ngroup /= ngrp).or. &
        (rank2_system%ngroup /= ngrp).or. &
        (rank1_basis%nsnap /= nsnap).or. &
        (rank2_system%nsnap /= nsnap)) &
      call fail('MODE2-DIAG SYSTEM DIMENSIONS DIFFER.')
    if (any(rank1_basis%rank_root /= 1).or. &
        any(rank1_parent%rank /= 1).or. &
        any(rank2_system%rank_root /= 2).or. &
        any(rank2_parent%rank /= 2).or. &
        any(rank2_current%rank /= 2)) &
      call fail('MODE2-DIAG RANK CONTRACT FAILED.')

    if ((real32_bits(rank1_parent%keff) /= &
         real32_bits(rank2_parent%keff)).or. &
        (real64_bits(rank1_parent%rho) /= &
         real64_bits(rank2_parent%rho)).or. &
        (real64_bits(rank1_parent%norm) /= &
         real64_bits(rank2_parent%norm)).or. &
        any(real64_bits(rank1_parent%height) /= &
            real64_bits(rank2_parent%height)).or. &
        any(real64_bits(rank1_parent%leakage) /= &
            real64_bits(rank2_parent%leakage))) &
      call fail('MODE2-DIAG RAW PARENT PHYSICAL STATE CHANGED.')
    write(6,'(A)') 'MODE2-DIAG RAW-PARENT RHO/NORM/LEAKAGE BITWISE PASS'

    do g=1,ngrp
      nreg=rank2_system%group(g)%nreg
      if ((rank1_basis%group(g)%nreg /= nreg).or. &
          (rank1_basis%group(g)%nmode /= 1).or. &
          (rank2_system%group(g)%nmode /= 2)) &
        call fail('MODE2-DIAG POD GROUP DIMENSIONS DIFFER.')
      if (any(real32_bits(rank1_basis%group(g)%volume) /= &
              real32_bits(rank2_system%group(g)%volume))) &
        call fail('MODE2-DIAG POD VOLUMES DIFFER.')
      if (any(real32_bits(rank1_basis%group(g)%basis) /= &
              real32_bits(rank2_system%group(g)%basis(1:nreg)))) &
        call fail('MODE2-DIAG MODE1 BASIS PREFIX DIFFERS.')
      do s=1,nsnap
        if (real32_bits(rank1_basis%group(g)%coeff(s)) /= &
            real32_bits(rank2_system%group(g)%coeff((s-1)*2+1))) &
          call fail('MODE2-DIAG MODE1 COEFFICIENT PREFIX DIFFERS.')
      enddo
      if (any(real64_bits(rank1_basis%group(g)%sigma) /= &
              real64_bits(rank2_system%group(g)%sigma))) &
        call fail('MODE2-DIAG POD SINGULAR VALUES DIFFER.')

      weight_sum=sum(real(rank2_system%group(g)%volume,real64))
      do a=1,2
        do b=1,2
          gram_value=0.0_real64
          do i=1,nreg
            gram_value=gram_value+ &
              real(rank2_system%group(g)%volume(i),real64)/weight_sum* &
              real(rank2_system%group(g)%basis((a-1)*nreg+i),real64)* &
              real(rank2_system%group(g)%basis((b-1)*nreg+i),real64)
          enddo
          index_g=rank2_current%gram_offset(g)+(b-1)*2+a
          if (real64_bits(gram_value) /= &
              real64_bits(rank2_current%gram(index_g))) &
            call fail('MODE2-DIAG GRAM RECOMPUTE DIFFERS BITWISE.')
        enddo
      enddo
    enddo
    if (any(real64_bits(rank1_basis%sigma_root) /= &
            real64_bits(rank2_system%sigma_root))) &
      call fail('MODE2-DIAG ROOT SINGULAR VALUES DIFFER.')
    write(6,'(A)') 'MODE2-DIAG MODE1 POD-PACKAGE PREFIX BITWISE PASS'
    write(6,'(A)') 'MODE2-DIAG GRAM FROM VOLUME/BASIS BITWISE PASS'

    projection_delta=0.0_real64
    projection_norm=0.0_real64
    do g=1,ngrp
      nreg=rank2_system%group(g)%nreg
      weight_sum=sum(real(rank2_system%group(g)%volume,real64))
      do s=1,nsnap
        index_a=rank1_parent%offset(g)+s
        do i=1,nreg
          weight=rank2_parent%height(s)* &
            real(rank2_system%group(g)%volume(i),real64)/weight_sum
          plane1=real(rank1_basis%group(g)%basis(i),real64)* &
            rank1_parent%coordinates(index_a)
          plane2=0.0_real64
          do a=1,2
            index_b=rank2_parent%offset(g)+(s-1)*2+a
            plane2=plane2+ &
              real(rank2_system%group(g)%basis((a-1)*nreg+i),real64)* &
              rank2_parent%coordinates(index_b)
          enddo
          projection_delta=projection_delta+weight*(plane2-plane1)**2
          projection_norm=projection_norm+weight*plane2**2
        enddo
      enddo
    enddo
    if ((.not.ieee_is_finite(projection_delta)).or. &
        (projection_delta < 0.0_real64).or. &
        (.not.ieee_is_finite(projection_norm)).or. &
        (projection_norm <= 0.0_real64)) &
      call fail('MODE2-DIAG INVALID PARENT PROJECTION NORM.')
    call write_real64_metric('MODE2-DIAG PARENT PROJECTION-RELATIVE', &
      sqrt(projection_delta/projection_norm))

    allocate(group_num(ngrp),snapshot_num(nsnap),cell_num(ngrp,nsnap))
    group_num=0.0_real64
    snapshot_num=0.0_real64
    cell_num=0.0_real64
    numerator=0.0_real64
    denominator=0.0_real64
    numerator_abs=0.0_real64
    numerator_part=0.0_real64
    current_part=0.0_real64
    parent_part=0.0_real64
    max_delta=0.0_real64
    max_delta_group=0
    max_delta_snap=0
    do g=1,ngrp
      do s=1,nsnap
        do a=1,2
          index_a=rank2_current%offset(g)+(s-1)*2+a
          delta_a=rank2_current%coordinates(index_a)- &
            rank2_parent%coordinates(index_a)
          if (abs(delta_a) > max_delta(a)) then
            max_delta(a)=abs(delta_a)
            max_delta_group(a)=g
            max_delta_snap(a)=s
          endif
          do b=1,2
            index_b=rank2_current%offset(g)+(s-1)*2+b
            index_g=rank2_current%gram_offset(g)+(b-1)*2+a
            delta_b=rank2_current%coordinates(index_b)- &
              rank2_parent%coordinates(index_b)
            term=rank2_current%height(s)*delta_a* &
              rank2_current%gram(index_g)*delta_b
            numerator=numerator+term
            numerator_abs=numerator_abs+abs(term)
            group_num(g)=group_num(g)+term
            snapshot_num(s)=snapshot_num(s)+term
            cell_num(g,s)=cell_num(g,s)+term
            if ((a == 1).and.(b == 1)) then
              numerator_part(1)=numerator_part(1)+term
            else if ((a == 2).and.(b == 2)) then
              numerator_part(2)=numerator_part(2)+term
            else
              numerator_part(3)=numerator_part(3)+term
            endif

            term=rank2_current%height(s)* &
              rank2_current%coordinates(index_a)* &
              rank2_current%gram(index_g)* &
              rank2_current%coordinates(index_b)
            denominator=denominator+term
            if ((a == 1).and.(b == 1)) then
              current_part(1)=current_part(1)+term
            else if ((a == 2).and.(b == 2)) then
              current_part(2)=current_part(2)+term
            else
              current_part(3)=current_part(3)+term
            endif

            term=rank2_parent%height(s)* &
              rank2_parent%coordinates(index_a)* &
              rank2_parent%gram(index_g)* &
              rank2_parent%coordinates(index_b)
            if ((a == 1).and.(b == 1)) then
              parent_part(1)=parent_part(1)+term
            else if ((a == 2).and.(b == 2)) then
              parent_part(2)=parent_part(2)+term
            else
              parent_part(3)=parent_part(3)+term
            endif
          enddo
        enddo
      enddo
    enddo
    if ((.not.ieee_is_finite(numerator)).or.(numerator <= 0.0_real64).or. &
        (.not.ieee_is_finite(denominator)).or. &
        (denominator <= 0.0_real64).or. &
        any(.not.ieee_is_finite(numerator_part)).or. &
        any(.not.ieee_is_finite(current_part)).or. &
        any(.not.ieee_is_finite(parent_part)).or. &
        any(numerator_part(1:2) < 0.0_real64).or. &
        any(current_part(1:2) < 0.0_real64).or. &
        any(parent_part(1:2) < 0.0_real64)) &
      call fail('MODE2-DIAG INVALID GRAM DECOMPOSITION.')
    if (real64_bits(sqrt(numerator/denominator)) /= &
        real64_bits(rank2_current%saved_defect(4))) &
      call fail('MODE2-DIAG R_A REPLAY DIFFERS BITWISE.')

    component_sum=sum(numerator_part)
    closure=abs(component_sum-numerator)
    nterms=4*ngrp*nsnap
    gamma_full=real(nterms-1,real64)*epsilon(1.0_real64)/ &
      (1.0_real64-real(nterms-1,real64)*epsilon(1.0_real64))
    gamma_part=real(2*ngrp*nsnap-1,real64)*epsilon(1.0_real64)/ &
      (1.0_real64-real(2*ngrp*nsnap-1,real64)*epsilon(1.0_real64))
    gamma_combine=2.0_real64*epsilon(1.0_real64)/ &
      (1.0_real64-2.0_real64*epsilon(1.0_real64))
    closure_bound=((1.0_real64+gamma_full)* &
      (1.0_real64+gamma_part)*(1.0_real64+gamma_combine)-1.0_real64)* &
      numerator_abs
    if (closure > closure_bound) &
      call fail('MODE2-DIAG ADDITIVE CLOSURE EXCEEDS ROUNDOFF BOUND.')
    write(6,'(A)') 'MODE2-DIAG R_A PRODUCTION-ORDER BITWISE PASS'
    write(6,'(A)') 'MODE2-DIAG ADDITIVE-CLOSURE ROUNDOFF-BOUND PASS'
    call write_real64_metric('MODE2-DIAG UPDATE NUMERATOR TOTAL',numerator)
    call write_real64_metric('MODE2-DIAG UPDATE NUMERATOR MODE1-DIAGONAL', &
      numerator_part(1))
    call write_real64_metric('MODE2-DIAG UPDATE NUMERATOR MODE2-DIAGONAL', &
      numerator_part(2))
    call write_real64_metric('MODE2-DIAG UPDATE NUMERATOR SIGNED-COUPLING', &
      numerator_part(3))
    call write_real64_metric('MODE2-DIAG UPDATE FRACTION MODE1-DIAGONAL', &
      numerator_part(1)/numerator)
    call write_real64_metric('MODE2-DIAG UPDATE FRACTION MODE2-DIAGONAL', &
      numerator_part(2)/numerator)
    call write_real64_metric('MODE2-DIAG UPDATE FRACTION SIGNED-COUPLING', &
      numerator_part(3)/numerator)
    call write_real64_metric('MODE2-DIAG UPDATE CLOSURE-ABS',closure)
    call write_real64_metric('MODE2-DIAG UPDATE CLOSURE-BOUND',closure_bound)
    call write_real64_metric('MODE2-DIAG CURRENT NORM-SQUARED',denominator)
    call write_real64_metric('MODE2-DIAG CURRENT FRACTION MODE2-DIAGONAL', &
      current_part(2)/sum(current_part))
    call write_real64_metric('MODE2-DIAG PARENT FRACTION MODE2-DIAGONAL', &
      parent_part(2)/sum(parent_part))
    call write_real64_metric('MODE2-DIAG R_A REPLAY', &
      sqrt(numerator/denominator))
    do s=1,nsnap
      write(6,'(A,1X,I0)') 'MODE2-DIAG SNAPSHOT',s
      call write_real64_metric('MODE2-DIAG SNAPSHOT UPDATE-FRACTION', &
        snapshot_num(s)/numerator)
    enddo

    top_group=1
    top_cell_group=1
    top_cell_snap=1
    do g=1,ngrp
      if (group_num(g) > group_num(top_group)) top_group=g
      do s=1,nsnap
        if (cell_num(g,s) > cell_num(top_cell_group,top_cell_snap)) then
          top_cell_group=g
          top_cell_snap=s
        endif
      enddo
    enddo
    write(6,'(A,1X,I0)') 'MODE2-DIAG TOP UPDATE GROUP',top_group
    call write_real64_metric('MODE2-DIAG TOP GROUP UPDATE-FRACTION', &
      group_num(top_group)/numerator)
    write(6,'(A,2(1X,I0))') 'MODE2-DIAG TOP UPDATE GROUP/SNAPSHOT', &
      top_cell_group,top_cell_snap
    call write_real64_metric('MODE2-DIAG TOP CELL UPDATE-FRACTION', &
      cell_num(top_cell_group,top_cell_snap)/numerator)
    do a=1,2
      write(6,'(A,3(1X,I0))') 'MODE2-DIAG MAX-DELTA MODE/GROUP/SNAPSHOT', &
        a,max_delta_group(a),max_delta_snap(a)
      call write_real64_metric('MODE2-DIAG MAX-ABS COORDINATE-DELTA', &
        max_delta(a))
    enddo

    d_leak=maxval(abs(rank2_current%leakage-rank2_parent%leakage))
    leak_scale=max(maxval(abs(rank2_current%leakage)), &
      maxval(abs(rank2_parent%leakage)))
    if ((real64_bits(d_leak) /= &
         real64_bits(rank2_current%saved_defect(3))).or. &
        (real64_bits(d_leak/leak_scale) /= &
         real64_bits(rank2_current%saved_defect(2)))) &
      call fail('MODE2-DIAG LEAKAGE DEFECT REPLAY DIFFERS BITWISE.')
    hot_index=0
    hot_ties=0
    do i=1,size(rank2_current%leakage)
      delta_value=rank2_current%leakage(i)-rank2_parent%leakage(i)
      if (abs(delta_value) == d_leak) then
        hot_ties=hot_ties+1
        if (hot_index == 0) hot_index=i
      endif
    enddo
    if ((hot_index == 0).or.(hot_ties == 0)) &
      call fail('MODE2-DIAG LEAKAGE HOTSPOT NOT FOUND.')
    g=mod(hot_index-1,ngrp)+1
    s=(hot_index-1)/ngrp+1
    write(6,'(A,3(1X,I0))') &
      'MODE2-DIAG LEAKAGE HOTSPOT GROUP/SNAPSHOT/TIES',g,s,hot_ties
    call write_real64_metric('MODE2-DIAG LEAKAGE HOTSPOT PARENT', &
      rank2_parent%leakage(hot_index))
    call write_real64_metric('MODE2-DIAG LEAKAGE HOTSPOT CURRENT', &
      rank2_current%leakage(hot_index))
    call write_real64_metric('MODE2-DIAG LEAKAGE HOTSPOT DELTA', &
      rank2_current%leakage(hot_index)-rank2_parent%leakage(hot_index))
    call write_real64_metric('MODE2-DIAG RHO SIGNED-DELTA', &
      rank2_current%rho-rank2_parent%rho)
    call write_real64_metric('MODE2-DIAG LEAKAGE SCALE',leak_scale)
    write(6,'(A)') 'MODE2-DIAG OFFLINE_MODE2_ANATOMY_ONLY'

    deallocate(cell_num,snapshot_num,group_num)
  end subroutine report_rank2_mode_diagnostics


  subroutine report_update_directions(x1,x2,x3)
    type(canonical_state), intent(in) :: x1,x2,x3
    integer :: igr,isnap,a,b,nmode,index_a,index_b,index_g,index_l
    integer :: l_hot_index(2),l_hot_ties(2)
    real(real64) :: a_state_sq(3),a_update_sq(2),a_dot
    real(real64) :: a_delta12_a,a_delta12_b,a_delta23_a,a_delta23_b
    real(real64) :: mode2_update_sq(2),mode2_dot
    real(real64) :: mode2_cosine,mode2_ratio
    real(real64) :: l_update_sq(2),l_dot,l_delta12,l_delta23
    real(real64) :: a_cosine,a_ratio,l_cosine,l_ratio
    real(real64) :: l_infinity(2),rho_delta(2)
    real(real64) :: aa1_denominator,aa1_beta,aa1_previous_weight
    real(real64) :: aa1_modal_residual_sq,aa1_modal_residual_norm
    logical :: rank2_metric

    a_state_sq=0.0_real64
    a_update_sq=0.0_real64
    a_dot=0.0_real64
    mode2_update_sq=0.0_real64
    mode2_dot=0.0_real64
    rank2_metric=all(x1%rank == 2)
    do igr=1,x1%dims(2)
      nmode=x1%rank(igr)
      do isnap=1,x1%dims(3)
        do a=1,nmode
          index_a=x1%offset(igr)+(isnap-1)*nmode+a
          a_delta12_a=x2%coordinates(index_a)-x1%coordinates(index_a)
          a_delta23_a=x3%coordinates(index_a)-x2%coordinates(index_a)
          do b=1,nmode
            index_b=x1%offset(igr)+(isnap-1)*nmode+b
            index_g=x1%gram_offset(igr)+(b-1)*nmode+a
            a_delta12_b=x2%coordinates(index_b)-x1%coordinates(index_b)
            a_delta23_b=x3%coordinates(index_b)-x2%coordinates(index_b)
            a_state_sq(1)=a_state_sq(1)+x1%height(isnap)* &
              x1%coordinates(index_a)*x1%gram(index_g)* &
              x1%coordinates(index_b)
            a_state_sq(2)=a_state_sq(2)+x1%height(isnap)* &
              x2%coordinates(index_a)*x1%gram(index_g)* &
              x2%coordinates(index_b)
            a_state_sq(3)=a_state_sq(3)+x1%height(isnap)* &
              x3%coordinates(index_a)*x1%gram(index_g)* &
              x3%coordinates(index_b)
            a_update_sq(1)=a_update_sq(1)+x1%height(isnap)* &
              a_delta12_a*x1%gram(index_g)*a_delta12_b
            a_update_sq(2)=a_update_sq(2)+x1%height(isnap)* &
              a_delta23_a*x1%gram(index_g)*a_delta23_b
            a_dot=a_dot+x1%height(isnap)*a_delta12_a* &
              x1%gram(index_g)*a_delta23_b
            if (rank2_metric.and.(a == 2).and.(b == 2)) then
              mode2_update_sq(1)=mode2_update_sq(1)+x1%height(isnap)* &
                a_delta12_a*x1%gram(index_g)*a_delta12_b
              mode2_update_sq(2)=mode2_update_sq(2)+x1%height(isnap)* &
                a_delta23_a*x1%gram(index_g)*a_delta23_b
              mode2_dot=mode2_dot+x1%height(isnap)*a_delta12_a* &
                x1%gram(index_g)*a_delta23_b
            endif
          enddo
        enddo
      enddo
    enddo
    if (any(.not.ieee_is_finite(a_state_sq)).or. &
        any(a_state_sq <= 0.0_real64).or. &
        any(.not.ieee_is_finite(a_update_sq)).or. &
        any(a_update_sq <= 0.0_real64).or. &
        (.not.ieee_is_finite(a_dot))) &
      call fail('INVALID MODAL UPDATE GEOMETRY.')
    a_cosine=a_dot/sqrt(a_update_sq(1)*a_update_sq(2))
    a_ratio=sqrt(a_update_sq(2)/a_update_sq(1))
    if ((.not.ieee_is_finite(a_cosine)).or. &
        (abs(a_cosine) > 1.0_real64).or. &
        (.not.ieee_is_finite(a_ratio))) &
      call fail('INVALID MODAL DIRECTION METRIC.')
    if (rank2_metric) then
      if (any(.not.ieee_is_finite(mode2_update_sq)).or. &
          any(mode2_update_sq <= 0.0_real64).or. &
          (.not.ieee_is_finite(mode2_dot))) &
        call fail('INVALID MODE2-DIAGONAL UPDATE GEOMETRY.')
      mode2_cosine=mode2_dot/ &
        sqrt(mode2_update_sq(1)*mode2_update_sq(2))
      mode2_ratio=sqrt(mode2_update_sq(2)/mode2_update_sq(1))
      if ((.not.ieee_is_finite(mode2_cosine)).or. &
          (abs(mode2_cosine) > 1.0_real64).or. &
          (.not.ieee_is_finite(mode2_ratio))) &
        call fail('INVALID MODE2-DIAGONAL DIRECTION METRIC.')

      aa1_denominator=a_update_sq(1)+a_update_sq(2)- &
        2.0_real64*a_dot
      if ((.not.ieee_is_finite(aa1_denominator)).or. &
          (aa1_denominator <= 0.0_real64)) &
        call fail('INVALID RANK2 MODAL-AA1 DENOMINATOR.')
      aa1_beta=(a_update_sq(1)-a_dot)/aa1_denominator
      aa1_previous_weight=1.0_real64-aa1_beta
      aa1_modal_residual_sq=aa1_previous_weight**2*a_update_sq(1)+ &
        aa1_beta**2*a_update_sq(2)+ &
        2.0_real64*aa1_previous_weight*aa1_beta*a_dot
      if ((.not.ieee_is_finite(aa1_beta)).or. &
          (.not.ieee_is_finite(aa1_modal_residual_sq)).or. &
          (aa1_modal_residual_sq < 0.0_real64)) &
        call fail('INVALID RANK2 MODAL-AA1 GEOMETRY.')
      aa1_modal_residual_norm=sqrt(aa1_modal_residual_sq)
    endif

    l_update_sq=0.0_real64
    l_dot=0.0_real64
    do isnap=1,x1%dims(3)
      do igr=1,x1%dims(2)
        index_l=(isnap-1)*x1%dims(2)+igr
        l_delta12=x2%leakage(index_l)-x1%leakage(index_l)
        l_delta23=x3%leakage(index_l)-x2%leakage(index_l)
        l_update_sq(1)=l_update_sq(1)+x1%height(isnap)* &
          l_delta12*l_delta12
        l_update_sq(2)=l_update_sq(2)+x1%height(isnap)* &
          l_delta23*l_delta23
        l_dot=l_dot+x1%height(isnap)*l_delta12*l_delta23
      enddo
    enddo
    if (any(.not.ieee_is_finite(l_update_sq)).or. &
        any(l_update_sq <= 0.0_real64).or. &
        (.not.ieee_is_finite(l_dot))) &
      call fail('INVALID LEAKAGE UPDATE GEOMETRY.')
    l_cosine=l_dot/sqrt(l_update_sq(1)*l_update_sq(2))
    l_ratio=sqrt(l_update_sq(2)/l_update_sq(1))
    if ((.not.ieee_is_finite(l_cosine)).or. &
        (abs(l_cosine) > 1.0_real64).or. &
        (.not.ieee_is_finite(l_ratio))) &
      call fail('INVALID LEAKAGE DIRECTION METRIC.')

    l_infinity(1)=maxval(abs(x2%leakage-x1%leakage))
    l_infinity(2)=maxval(abs(x3%leakage-x2%leakage))
    if ((real64_bits(l_infinity(1)) /= &
         real64_bits(x2%saved_defect(3))).or. &
        (real64_bits(l_infinity(2)) /= &
         real64_bits(x3%saved_defect(3)))) &
      call fail('LEAKAGE INFINITY DEFECT DIFFERS BITWISE.')
    l_hot_index=0
    l_hot_ties=0
    do index_l=1,size(x1%leakage)
      l_delta12=x2%leakage(index_l)-x1%leakage(index_l)
      l_delta23=x3%leakage(index_l)-x2%leakage(index_l)
      if (abs(l_delta12) == l_infinity(1)) then
        l_hot_ties(1)=l_hot_ties(1)+1
        if (l_hot_index(1) == 0) l_hot_index(1)=index_l
      endif
      if (abs(l_delta23) == l_infinity(2)) then
        l_hot_ties(2)=l_hot_ties(2)+1
        if (l_hot_index(2) == 0) l_hot_index(2)=index_l
      endif
    enddo
    if (any(l_hot_index == 0).or.any(l_hot_ties == 0)) &
      call fail('LEAKAGE INFINITY HOTSPOT NOT FOUND.')
    rho_delta=(/x2%rho-x1%rho,x3%rho-x2%rho/)

    write(6,'(A)') 'PICARD-DIRECTION FIXED-SPACE BITWISE PASS'
    write(6,'(A)') 'PICARD-DIRECTION MODAL METRIC GRAM-HEIGHT'
    call write_real64_metric('PICARD-DIRECTION MODAL STATE-NORM X1', &
      sqrt(a_state_sq(1)))
    call write_real64_metric('PICARD-DIRECTION MODAL STATE-NORM X2', &
      sqrt(a_state_sq(2)))
    call write_real64_metric('PICARD-DIRECTION MODAL STATE-NORM X3', &
      sqrt(a_state_sq(3)))
    call write_real64_metric('PICARD-DIRECTION MODAL UPDATE-NORM 12', &
      sqrt(a_update_sq(1)))
    call write_real64_metric('PICARD-DIRECTION MODAL UPDATE-NORM 23', &
      sqrt(a_update_sq(2)))
    call write_real64_metric('PICARD-DIRECTION MODAL DOT 12-23',a_dot)
    call write_real64_metric('PICARD-DIRECTION MODAL COSINE 12-23',a_cosine)
    call write_real64_metric('PICARD-DIRECTION MODAL NORM-RATIO 23/12', &
      a_ratio)
    call write_real64_metric('PICARD-DIRECTION MODAL SAVED-R_A 12', &
      x2%saved_defect(4))
    call write_real64_metric('PICARD-DIRECTION MODAL SAVED-R_A 23', &
      x3%saved_defect(4))
    if (a_dot < 0.0_real64) then
      write(6,'(A)') 'PICARD-DIRECTION MODAL GEOMETRY OBTUSE'
    else if (a_dot > 0.0_real64) then
      write(6,'(A)') 'PICARD-DIRECTION MODAL GEOMETRY ACUTE'
    else
      write(6,'(A)') 'PICARD-DIRECTION MODAL GEOMETRY ORTHOGONAL'
    endif
    if (rank2_metric) then
      write(6,'(A)') &
        'PICARD-DIRECTION MODE2-DIAGONAL GRAM-HEIGHT BASIS-DEPENDENT'
      call write_real64_metric( &
        'PICARD-DIRECTION MODE2-DIAGONAL UPDATE-NORM 12', &
        sqrt(mode2_update_sq(1)))
      call write_real64_metric( &
        'PICARD-DIRECTION MODE2-DIAGONAL UPDATE-NORM 23', &
        sqrt(mode2_update_sq(2)))
      call write_real64_metric( &
        'PICARD-DIRECTION MODE2-DIAGONAL DOT 12-23',mode2_dot)
      call write_real64_metric( &
        'PICARD-DIRECTION MODE2-DIAGONAL COSINE 12-23',mode2_cosine)
      call write_real64_metric( &
        'PICARD-DIRECTION MODE2-DIAGONAL NORM-RATIO 23/12',mode2_ratio)
      if (mode2_dot < 0.0_real64) then
        write(6,'(A)') &
          'PICARD-DIRECTION MODE2-DIAGONAL GEOMETRY OBTUSE'
      else if (mode2_dot > 0.0_real64) then
        write(6,'(A)') &
          'PICARD-DIRECTION MODE2-DIAGONAL GEOMETRY ACUTE'
      else
        write(6,'(A)') &
          'PICARD-DIRECTION MODE2-DIAGONAL GEOMETRY ORTHOGONAL'
      endif
      write(6,'(A)') 'RANK2-MODAL-AA1 METRIC FULL-GRAM-HEIGHT'
      write(6,'(A)') &
        'RANK2-MODAL-AA1 STATED-MODAL-LS UNIQUE-MINIMIZER UNCLIPPED'
      call write_real64_metric('RANK2-MODAL-AA1 BETA WEIGHT-X2', &
        aa1_beta)
      call write_real64_metric('RANK2-MODAL-AA1 WEIGHT-X1', &
        aa1_previous_weight)
      call write_real64_metric('RANK2-MODAL-AA1 DENOMINATOR', &
        aa1_denominator)
      call write_real64_metric('RANK2-MODAL-AA1 AFFINE-RESIDUAL-NORM', &
        aa1_modal_residual_norm)
      call write_real64_metric('RANK2-MODAL-AA1 AFFINE-RESIDUAL/CURRENT', &
        aa1_modal_residual_norm/sqrt(a_update_sq(2)))
      if ((aa1_beta >= 0.0_real64).and. &
          (aa1_beta <= 1.0_real64)) then
        write(6,'(A)') 'RANK2-MODAL-AA1 GEOMETRY CONVEX'
      else
        write(6,'(A)') 'RANK2-MODAL-AA1 GEOMETRY EXTRAPOLATED'
      endif
      write(6,'(A)') &
        'RANK2-MODAL-AA1 SAME-SCALAR COMPLETE-STATE-AFFINE-PROPOSAL'
      write(6,'(A)') &
        'RANK2-MODAL-AA1 OFFLINE-COEFFICIENT-ONLY NO-CANDIDATE NO-MAP'
    endif

    write(6,'(A)') &
      'PICARD-DIRECTION LEAKAGE-HEIGHT-L2 NON-PRODUCTION-DIAGNOSTIC'
    call write_real64_metric('PICARD-DIRECTION LEAKAGE UPDATE-NORM 12', &
      sqrt(l_update_sq(1)))
    call write_real64_metric('PICARD-DIRECTION LEAKAGE UPDATE-NORM 23', &
      sqrt(l_update_sq(2)))
    call write_real64_metric('PICARD-DIRECTION LEAKAGE DOT 12-23',l_dot)
    call write_real64_metric('PICARD-DIRECTION LEAKAGE COSINE 12-23', &
      l_cosine)
    call write_real64_metric('PICARD-DIRECTION LEAKAGE NORM-RATIO 23/12', &
      l_ratio)
    if (l_dot < 0.0_real64) then
      write(6,'(A)') 'PICARD-DIRECTION LEAKAGE GEOMETRY OBTUSE'
    else if (l_dot > 0.0_real64) then
      write(6,'(A)') 'PICARD-DIRECTION LEAKAGE GEOMETRY ACUTE'
    else
      write(6,'(A)') 'PICARD-DIRECTION LEAKAGE GEOMETRY ORTHOGONAL'
    endif
    write(6,'(A)') 'PICARD-DIRECTION LEAKAGE-INF PRODUCTION-DIAGNOSTIC'
    call write_real64_metric('PICARD-DIRECTION LEAKAGE D_L 12', &
      l_infinity(1))
    call write_real64_metric('PICARD-DIRECTION LEAKAGE D_L 23', &
      l_infinity(2))
    call write_real64_metric('PICARD-DIRECTION LEAKAGE D_L-RATIO 23/12', &
      l_infinity(2)/l_infinity(1))
    call report_leakage_hotspot('12',l_hot_index(1),l_hot_ties(1), &
      x1,x2,x3)
    call report_leakage_hotspot('23',l_hot_index(2),l_hot_ties(2), &
      x1,x2,x3)
    if (any(l_hot_ties > 1)) then
      write(6,'(A)') &
        'PICARD-DIRECTION LEAKAGE HOTSPOT LOCATION-NOT-UNIQUE'
    else if (l_hot_index(1) == l_hot_index(2)) then
      write(6,'(A)') 'PICARD-DIRECTION LEAKAGE HOTSPOT SAME-LOCATION'
    else
      write(6,'(A)') 'PICARD-DIRECTION LEAKAGE HOTSPOT MOVED'
    endif

    call write_real64_metric('PICARD-DIRECTION RHO DELTA 12',rho_delta(1))
    call write_real64_metric('PICARD-DIRECTION RHO DELTA 23',rho_delta(2))
    if ((rho_delta(1) == 0.0_real64).or. &
        (rho_delta(2) == 0.0_real64)) then
      write(6,'(A)') 'PICARD-DIRECTION RHO GEOMETRY UNDEFINED-ZERO-UPDATE'
    else if ((rho_delta(1) > 0.0_real64).eqv. &
             (rho_delta(2) > 0.0_real64)) then
      write(6,'(A)') 'PICARD-DIRECTION RHO GEOMETRY SAME-SIGN'
    else
      write(6,'(A)') 'PICARD-DIRECTION RHO GEOMETRY OPPOSITE-SIGN'
    endif
    write(6,'(A)') &
      'PICARD-DIRECTION COMBINED-STATE ANGLE-NOT-DEFINED-MIXED-UNITS'
    write(6,'(A)') 'PICARD-DIRECTION INNER-ERROR-BOUND NOT-AVAILABLE'
    write(6,'(A)') &
      'PICARD-DIRECTION PHYSICAL-VS-NUMERICAL-CAUSE UNRESOLVED'
    write(6,'(A)') &
      'PICARD-DIRECTION OUTER-CONVERGENCE NOT-ESTABLISHED'
  end subroutine report_update_directions


  subroutine report_leakage_hotspot(label,index_l,ties,x1,x2,x3)
    character(len=*), intent(in) :: label
    integer, intent(in) :: index_l,ties
    type(canonical_state), intent(in) :: x1,x2,x3
    integer :: igr,isnap
    real(real64) :: delta12,delta23

    igr=mod(index_l-1,x1%dims(2))+1
    isnap=(index_l-1)/x1%dims(2)+1
    delta12=x2%leakage(index_l)-x1%leakage(index_l)
    delta23=x3%leakage(index_l)-x2%leakage(index_l)
    write(6,'(A,3(1X,I0))') 'PICARD-DIRECTION LEAKAGE HOTSPOT '// &
      trim(label)//' FIRST-PLANE/GROUP/TIES',isnap,igr,ties
    call write_real64_metric('PICARD-DIRECTION LEAKAGE HOTSPOT '// &
      trim(label)//' L1',x1%leakage(index_l))
    call write_real64_metric('PICARD-DIRECTION LEAKAGE HOTSPOT '// &
      trim(label)//' L2',x2%leakage(index_l))
    call write_real64_metric('PICARD-DIRECTION LEAKAGE HOTSPOT '// &
      trim(label)//' L3',x3%leakage(index_l))
    call write_real64_metric('PICARD-DIRECTION LEAKAGE HOTSPOT '// &
      trim(label)//' DELTA12',delta12)
    call write_real64_metric('PICARD-DIRECTION LEAKAGE HOTSPOT '// &
      trim(label)//' DELTA23',delta23)
    if ((delta12 == 0.0_real64).or.(delta23 == 0.0_real64)) then
      write(6,'(A)') 'PICARD-DIRECTION LEAKAGE HOTSPOT '// &
        trim(label)//' SIGN ZERO-INVOLVED'
    else if ((delta12 > 0.0_real64).eqv.(delta23 > 0.0_real64)) then
      write(6,'(A)') 'PICARD-DIRECTION LEAKAGE HOTSPOT '// &
        trim(label)//' SIGN SAME'
    else
      write(6,'(A)') 'PICARD-DIRECTION LEAKAGE HOTSPOT '// &
        trim(label)//' SIGN OPPOSITE'
    endif
  end subroutine report_leakage_hotspot


  subroutine write_real64_metric(label,value)
    character(len=*), intent(in) :: label
    real(real64), intent(in) :: value

    write(6,'(A,1X,ES25.17E3,1X,A,Z16.16)') &
      trim(label),value,'BITS=0x',real64_bits(value)
  end subroutine write_real64_metric




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


  subroutine require_list_item(list_ptr,index0,length_expected, &
      type_expected,owner)
    type(c_ptr), intent(in) :: list_ptr
    integer, intent(in) :: index0,length_expected,type_expected
    character(len=*), intent(in) :: owner
    integer :: length_found,type_found

    call LCMLEL(list_ptr,index0,length_found,type_found)
    if ((length_found /= length_expected).or. &
        (type_found /= type_expected)) &
      call fail(trim(owner)//' LIST ITEM CONTRACT FAILED.')
  end subroutine require_list_item


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
