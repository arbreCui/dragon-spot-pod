program check_one_map_xsm
  ! Independent Ganlib-only, read-only audit of one fixed-space SPOT map.
  !
  !   check_one_map_xsm basis_reference.xsm state1_system.xsm \
  !     state0_axial.xsm state1_axial.xsm state1_snapshots.xsm
  !   check_one_map_xsm --continued basis_reference.xsm \
  !     state2_system.xsm state1_axial.xsm state2_axial.xsm \
  !     state2_snapshots.xsm
  !   check_one_map_xsm --directions state1_axial.xsm \
  !     state2_axial.xsm state3_axial.xsm
  !   check_one_map_xsm --leakage-faces axial_track.xsm \
  !     state1_axial.xsm state2_axial.xsm state3_axial.xsm
  !
  ! No Dragon, SPOT, assembly, transport, or production convergence routine
  ! is linked or called.  The one-map modes read five archived XSM objects,
  ! verify the fixed POD package bit for bit, require a live RADIAL-OP change,
  ! and independently recompute the canonical defects.  Direction mode reads
  ! three frozen canonical states, describes their two stored increments,
  ! and locates the infinity-norm leakage hotspots.  Leakage-face mode also
  ! rebuilds raw leakage and reports the exact radial support of the dominant
  ! axial-face change and its minimal normalization-invariant adjacent-floor
  ! scalar/current ratios.
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

  type :: leakage_face_state
    real(real64) :: low=0.0_real64
    real(real64) :: high=0.0_real64
    real(real64) :: net=0.0_real64
    real(real32) :: numerator=0.0_real32
    real(real32) :: denominator=0.0_real32
    real(real32) :: leakage=0.0_real32
  end type leakage_face_state

  character(len=1024) :: paths(5)
  character(len=1024) :: track_path
  character(len=32) :: mode
  type(system_data) :: reference_system,current_system
  type(canonical_state) :: previous_state,current_state
  type(canonical_state) :: direction_state(3)
  integer :: i,argument_offset
  logical :: continued,direction_mode,face_mode

  continued=.false.
  direction_mode=.false.
  face_mode=.false.
  argument_offset=0
  if (command_argument_count() == 4) then
    call get_command_argument(1,mode)
    if (trim(mode) /= '--directions') call fail( &
      'ONLY --directions IS ACCEPTED IN FOUR-ARGUMENT MODE.')
    direction_mode=.true.
    do i=1,3
      call get_command_argument(i+1,paths(i))
      if (len_trim(paths(i)) == 0) call fail('EMPTY XSM PATH ARGUMENT.')
      if (len_trim(paths(i)) > max_xsm_path) &
        call fail('XSM PATH ARGUMENT EXCEEDS GANLIB LIMIT.')
    enddo
  else if (command_argument_count() == 5) then
    call get_command_argument(1,mode)
    if (trim(mode) == '--leakage-faces') then
      direction_mode=.true.
      face_mode=.true.
      call get_command_argument(2,track_path)
      if (len_trim(track_path) == 0) call fail('EMPTY TRACK PATH ARGUMENT.')
      if (len_trim(track_path) > max_xsm_path) &
        call fail('TRACK PATH ARGUMENT EXCEEDS GANLIB LIMIT.')
      do i=1,3
        call get_command_argument(i+2,paths(i))
        if (len_trim(paths(i)) == 0) call fail('EMPTY XSM PATH ARGUMENT.')
        if (len_trim(paths(i)) > max_xsm_path) &
          call fail('XSM PATH ARGUMENT EXCEEDS GANLIB LIMIT.')
      enddo
    endif
  else if (command_argument_count() == 6) then
    call get_command_argument(1,mode)
    if (trim(mode) /= '--continued') call fail( &
      'ONLY --continued IS ACCEPTED IN SIX-ARGUMENT MODE.')
    continued=.true.
    argument_offset=1
  else if (command_argument_count() /= 5) then
    call fail('EXPECTED [--continued] BASIS, SYSTEM, PREVIOUS, CURRENT, SNAP.')
  endif
  if (.not.direction_mode) then
    do i=1,5
      call get_command_argument(i+argument_offset,paths(i))
      if (len_trim(paths(i)) == 0) call fail('EMPTY XSM PATH ARGUMENT.')
      if (len_trim(paths(i)) > max_xsm_path) &
        call fail('XSM PATH ARGUMENT EXCEEDS GANLIB LIMIT.')
    enddo
  endif

  if (direction_mode) then
    call load_canonical_state(trim(paths(1)),1,'POD-FIXED',.true., &
      direction_state(1),'DIRECTION STATE X1')
    call load_canonical_state(trim(paths(2)),1,'POD-FIXED',.true., &
      direction_state(2),'DIRECTION STATE X2')
    call load_canonical_state(trim(paths(3)),1,'POD-FIXED',.true., &
      direction_state(3),'DIRECTION STATE X3')
    call compare_states_and_defects(direction_state(1), &
      direction_state(2),.true.)
    if (face_mode) then
      write(6,'(A)') 'LEAKAGE-FACES MAP12 RAW-DEFECT BITWISE PASS'
    else
      write(6,'(A)') 'PICARD-DIRECTION MAP12 RAW-DEFECT BITWISE PASS'
    endif
    call compare_states_and_defects(direction_state(2), &
      direction_state(3),.true.)
    if (face_mode) then
      write(6,'(A)') 'LEAKAGE-FACES MAP23 RAW-DEFECT BITWISE PASS'
    else
      write(6,'(A)') 'PICARD-DIRECTION MAP23 RAW-DEFECT BITWISE PASS'
    endif
    if (face_mode) then
      call report_leakage_faces(trim(track_path),trim(paths(1)), &
        trim(paths(2)),trim(paths(3)),direction_state)
    else
      call report_update_directions(direction_state(1),direction_state(2), &
        direction_state(3))
      write(6,'(A)') 'PICARD-DIRECTION COMPLETE'
    endif
  else
    call load_system(trim(paths(1)),0,0,'POD-BUILT',.false., &
      reference_system,'BASIS REFERENCE')
    call load_system(trim(paths(2)),1,3,'POD-FIXED',.true., &
      current_system,'CURRENT SYSTEM')
    call compare_systems(reference_system,current_system)

    if (continued) then
      call load_canonical_state(trim(paths(3)),1,'POD-FIXED',.true., &
        previous_state,'PREVIOUS CONTINUED STATE')
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
    call compare_states_and_defects(previous_state,current_state,continued)
    call check_restart_archive(trim(paths(5)),previous_state,current_state)

    write(6,'(A)') 'ONE-MAP-XSM POD-PACKAGE BITWISE PASS'
    write(6,'(A)') 'ONE-MAP-XSM RADIAL-OP LIVE-CHANGE PASS'
    write(6,'(A)') 'ONE-MAP-XSM RAW-RADIAL-POSITIVITY PASS'
    write(6,'(A)') 'ONE-MAP-XSM CANONICAL-LAYOUT BITWISE PASS'
    write(6,'(A)') 'ONE-MAP-XSM RAW-DEFECT BITWISE PASS'
    write(6,'(A)') 'ONE-MAP-XSM RESTART-ARCHIVE BITWISE PASS'
    write(6,'(A)') 'ONE-MAP-XSM COMPLETE'
  endif

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


  subroutine compare_states_and_defects(previous,current,continued_mode)
    type(canonical_state), intent(in) :: previous,current
    logical, intent(in) :: continued_mode
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
    if (continued_mode) then
      if ((previous%fixb /= 1).or. &
          (previous%basis_type /= 'POD-FIXED').or. &
          (.not.previous%has_saved_defect)) &
        call fail('PREVIOUS CONTINUED-STATE MARKERS ARE INVALID.')
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


  subroutine report_update_directions(x1,x2,x3)
    type(canonical_state), intent(in) :: x1,x2,x3
    integer :: igr,isnap,a,b,nmode,index_a,index_b,index_g,index_l
    integer :: l_hot_index(2),l_hot_ties(2)
    real(real64) :: a_state_sq(3),a_update_sq(2),a_dot
    real(real64) :: a_delta12_a,a_delta12_b,a_delta23_a,a_delta23_b
    real(real64) :: l_update_sq(2),l_dot,l_delta12,l_delta23
    real(real64) :: a_cosine,a_ratio,l_cosine,l_ratio
    real(real64) :: l_infinity(2),rho_delta(2)

    a_state_sq=0.0_real64
    a_update_sq=0.0_real64
    a_dot=0.0_real64
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


  subroutine report_leakage_faces(track_name,x1_name,x2_name,x3_name,states)
    character(len=*), intent(in) :: track_name,x1_name,x2_name,x3_name
    type(canonical_state), intent(in) :: states(3)
    type(c_ptr) :: track
    type(leakage_face_state) :: face(3)
    character(len=1024) :: state_name(3)
    character(len=12) :: signature,track_type
    integer :: track_state(nstate)
    integer :: ngrp,nunk,nreg,nreg2d,nfloor,nsnap,ll4,ll5
    integer :: i,index0,hot_index(2),hot_ties(2),hot_s,hot_g
    integer :: first,last,run_count,interface_z
    integer, allocatable :: keyflx(:),mat1d(:)
    real(real32), allocatable :: dz(:),area(:)
    real(real64), allocatable :: high_region(:,:),phi_below(:,:)
    real(real64), allocatable :: phi_above(:,:),interface_current(:,:)
    real(real64) :: delta(2),maximum(2)
    real(real64) :: delta_low,delta_high,high_total(3)

    state_name(1)=x1_name
    state_name(2)=x2_name
    state_name(3)=x3_name
    maximum(1)=maxval(abs(states(2)%leakage-states(1)%leakage))
    maximum(2)=maxval(abs(states(3)%leakage-states(2)%leakage))
    hot_index=0
    hot_ties=0
    do index0=1,size(states(1)%leakage)
      delta(1)=states(2)%leakage(index0)-states(1)%leakage(index0)
      delta(2)=states(3)%leakage(index0)-states(2)%leakage(index0)
      do i=1,2
        if (real64_bits(abs(delta(i))) == real64_bits(maximum(i))) then
          hot_ties(i)=hot_ties(i)+1
          if (hot_index(i) == 0) hot_index(i)=index0
        endif
      enddo
    enddo
    if (any(hot_ties /= 1).or.(hot_index(1) /= hot_index(2))) &
      call fail('LEAKAGE FACE AUDIT REQUIRES ONE COMMON UNIQUE HOTSPOT.')

    ngrp=states(1)%dims(2)
    nsnap=states(1)%dims(3)
    hot_s=(hot_index(1)-1)/ngrp+1
    hot_g=mod(hot_index(1)-1,ngrp)+1

    call LCMOP(track,track_name,2,2,0)
    call require_record(track,'SIGNATURE',3,3,'LEAKAGE FACE TRACK')
    call require_record(track,'TRACK-TYPE',3,3,'LEAKAGE FACE TRACK')
    call LCMGTC(track,'SIGNATURE',12,signature)
    call LCMGTC(track,'TRACK-TYPE',12,track_type)
    if ((signature /= 'L_TRACK').or.(track_type /= 'SPOT')) &
      call fail('LEAKAGE FACE AUDIT REQUIRES A SPOT L_TRACK.')
    call require_record(track,'STATE-VECTOR',nstate,1, &
      'LEAKAGE FACE TRACK')
    call LCMGET(track,'STATE-VECTOR',track_state)
    nreg=track_state(1)
    nunk=track_state(2)
    nreg2d=track_state(6)
    nfloor=track_state(7)
    ll4=track_state(11)
    ll5=track_state(12)
    if ((nreg <= 0).or.(nunk <= 0).or.(nreg2d <= 0).or. &
        (nfloor <= 0).or.(track_state(8) /= nsnap).or. &
        (nreg /= nreg2d*nfloor).or.(ll4 < 0).or. &
        (ll5 /= nreg2d*(nfloor+1)).or.(ll4+ll5 > nunk).or. &
        (states(1)%state(1) /= ngrp).or. &
        (states(1)%state(2) /= nunk)) &
      call fail('LEAKAGE FACE TRACK DIMENSIONS CHANGED.')
    do i=2,3
      if ((states(i)%dims(2) /= ngrp).or. &
          (states(i)%dims(3) /= nsnap).or. &
          (states(i)%state(1) /= ngrp).or. &
          (states(i)%state(2) /= nunk)) &
        call fail('LEAKAGE FACE STATE DIMENSIONS DIFFER.')
    enddo

    allocate(keyflx(nreg),mat1d(nfloor),dz(nfloor),area(nreg2d))
    allocate(high_region(nreg2d,3))
    call require_record(track,'KEYFLX',nreg,1,'LEAKAGE FACE TRACK')
    call require_record(track,'MAT1D',nfloor,1,'LEAKAGE FACE TRACK')
    call require_record(track,'VOL1D',nfloor,2,'LEAKAGE FACE TRACK')
    call require_record(track,'AREA2D',nreg2d,2,'LEAKAGE FACE TRACK')
    call LCMGET(track,'KEYFLX',keyflx)
    call LCMGET(track,'MAT1D',mat1d)
    call LCMGET(track,'VOL1D',dz)
    call LCMGET(track,'AREA2D',area)
    if (any(keyflx < 0).or.any(keyflx > nunk).or. &
        any(mat1d < 1).or.any(mat1d > nsnap).or. &
        any(.not.ieee_is_finite(dz)).or.any(dz <= 0.0_real32).or. &
        any(.not.ieee_is_finite(area)).or.any(area <= 0.0_real32)) &
      call fail('LEAKAGE FACE TRACK DATA ARE INVALID.')
    do i=1,nsnap
      if (count(mat1d == i) == 0) &
        call fail('LEAKAGE FACE TRACK HAS AN EMPTY PLANE SET.')
    enddo
    first=1
    run_count=0
    interface_z=0
    do while(first <= nfloor)
      last=first
      do
        if (last >= nfloor) exit
        if (mat1d(last+1) /= mat1d(first)) exit
        last=last+1
      enddo
      if (mat1d(first) == hot_s) then
        run_count=run_count+1
        interface_z=last
      endif
      first=last+1
    enddo
    if ((run_count /= 1).or.(interface_z >= nfloor)) &
      call fail('LEAKAGE FACE INTERFACE IS NOT ONE INTERIOR HIGH-Z FACE.')
    call LCMCL(track,1)

    allocate(phi_below(nreg2d,3),phi_above(nreg2d,3))
    allocate(interface_current(nreg2d,3))
    do i=1,3
      call verify_raw_leakage_and_faces(trim(state_name(i)),states(i), &
        ngrp,nunk,nreg2d,nfloor,nsnap,ll4,keyflx,mat1d,dz,area, &
        hot_s,hot_g,interface_z,face(i),high_region(:,i), &
        phi_below(:,i),phi_above(:,i),interface_current(:,i))
    enddo

    write(6,'(A,3(1X,I0))') &
      'LEAKAGE-FACES HOTSPOT PLANE/GROUP/TIES',hot_s,hot_g,hot_ties(1)
    write(6,'(A)') 'LEAKAGE-FACES CANONICAL-SP32 BITWISE PASS'
    write(6,'(A)') 'LEAKAGE-FACES CURRENT COMMON-SIGNED-PLUS-Z'
    write(6,'(A)') &
      'LEAKAGE-FACES FACE64 C_LOW=-SUM(A*J_LOW) C_HIGH=+SUM(A*J_HIGH)'
    call write_leakage_face_state('X1',face(1))
    call write_leakage_face_state('X2',face(2))
    call write_leakage_face_state('X3',face(3))

    delta_low=face(2)%low-face(1)%low
    delta_high=face(2)%high-face(1)%high
    call write_leakage_face_delta('12',face(1),face(2))
    call write_face_dominance('12',delta_low,delta_high)
    delta_low=face(3)%low-face(2)%low
    delta_high=face(3)%high-face(2)%high
    call write_leakage_face_delta('23',face(2),face(3))
    call write_face_dominance('23',delta_low,delta_high)
    high_total=(/face(1)%high,face(2)%high,face(3)%high/)
    call write_high_face_regions(area,high_region,high_total)
    call write_interface_ratios(interface_z,phi_below,phi_above, &
      interface_current)
    write(6,'(A)') 'LEAKAGE-FACES COMPLETE'

    deallocate(interface_current,phi_above,phi_below)
    deallocate(high_region,area,dz,mat1d,keyflx)
  end subroutine report_leakage_faces


  subroutine verify_raw_leakage_and_faces(path,canonical,ng,nun,nr,nz, &
      ns,l4,key,map,height,area,target_s,target_g,interface_z,result, &
      high_region,phi_below,phi_above,interface_current)
    character(len=*), intent(in) :: path
    type(canonical_state), intent(in) :: canonical
    integer, intent(in) :: ng,nun,nr,nz,ns,l4,target_s,target_g,interface_z
    integer, intent(in) :: key(nr*nz),map(nz)
    real(real32), intent(in) :: height(nz),area(nr)
    type(leakage_face_state), intent(out) :: result
    real(real64), intent(out) :: high_region(nr)
    real(real64), intent(out) :: phi_below(nr),phi_above(nr)
    real(real64), intent(out) :: interface_current(nr)
    type(c_ptr) :: root,fluxes
    character(len=12) :: signature
    integer :: state(nstate)
    integer :: g,s,r,z,reg,left_index,right_index,index0
    integer :: first,last,run_s
    real(real32), allocatable :: unknown(:),numerator(:),denominator(:)
    real(real32) :: scalar,difference,term,leakage
    real(real64) :: face_term
    logical :: target_found

    result%low=0.0_real64
    result%high=0.0_real64
    result%net=0.0_real64
    result%numerator=0.0_real32
    result%denominator=0.0_real32
    result%leakage=0.0_real32
    high_region=0.0_real64
    phi_below=0.0_real64
    phi_above=0.0_real64
    interface_current=0.0_real64
    target_found=.false.

    call LCMOP(root,path,2,2,0)
    call require_record(root,'SIGNATURE',3,3,'LEAKAGE FACE STATE')
    call LCMGTC(root,'SIGNATURE',12,signature)
    if (signature /= 'L_FLUX') &
      call fail('LEAKAGE FACE STATE IS NOT L_FLUX.')
    call require_record(root,'STATE-VECTOR',nstate,1,'LEAKAGE FACE STATE')
    call LCMGET(root,'STATE-VECTOR',state)
    if ((state(1) /= ng).or.(state(2) /= nun).or. &
        any(state /= canonical%state)) &
      call fail('LEAKAGE FACE STATE DIMENSIONS CHANGED.')
    call require_record(root,'FLUX',ng,10,'LEAKAGE FACE STATE')
    fluxes=LCMGID(root,'FLUX')

    allocate(unknown(nun),numerator(ns),denominator(ns))
    do g=1,ng
      call require_list_item(fluxes,g,nun,2,'LEAKAGE FACE STATE FLUX')
      call LCMGDL(fluxes,g,unknown)
      if (any(.not.ieee_is_finite(unknown))) &
        call fail('LEAKAGE FACE STATE HAS NON-FINITE UNKNOWNS.')

      numerator=0.0_real32
      denominator=0.0_real32
      do z=1,nz
        s=map(z)
        do r=1,nr
          reg=(r-1)*nz+z
          if (key(reg) > 0) then
            scalar=unknown(key(reg))
          else
            scalar=0.0_real32
          endif
          left_index=l4+(r-1)*(nz+1)+z
          right_index=left_index+1
          difference=unknown(right_index)-unknown(left_index)
          term=area(r)*difference
          numerator(s)=numerator(s)+term
          term=area(r)*height(z)
          term=term*scalar
          denominator(s)=denominator(s)+term
        enddo
      enddo
      do s=1,ns
        if (denominator(s) > 0.0_real32) then
          leakage=numerator(s)/denominator(s)
        else if (denominator(s) == 0.0_real32) then
          leakage=0.0_real32
        else
          call fail('LEAKAGE FACE STATE HAS A NEGATIVE FLUX INTEGRAL.')
        endif
        index0=(s-1)*ng+g
        if (real64_bits(real(leakage,real64)) /= &
            real64_bits(canonical%leakage(index0))) &
          call fail('RAW LEAKAGE DIFFERS FROM THE CANONICAL STATE.')
        if ((s == target_s).and.(g == target_g)) then
          result%numerator=numerator(s)
          result%denominator=denominator(s)
          result%leakage=leakage
          target_found=.true.
        endif
      enddo

      if (g == target_g) then
        do r=1,nr
          reg=(r-1)*nz+interface_z
          if ((key(reg) <= 0).or.(key(reg+1) <= 0)) &
            call fail('LEAKAGE FACE ADJACENT SCALAR UNKNOWN IS ABSENT.')
          phi_below(r)=real(unknown(key(reg)),real64)
          phi_above(r)=real(unknown(key(reg+1)),real64)
          right_index=l4+(r-1)*(nz+1)+interface_z+1
          interface_current(r)=real(unknown(right_index),real64)
        enddo
        do r=1,nr
          first=1
          do while(first <= nz)
            run_s=map(first)
            last=first
            do
              if (last >= nz) exit
              if (map(last+1) /= run_s) exit
              last=last+1
            enddo
            if (run_s == target_s) then
              left_index=l4+(r-1)*(nz+1)+first
              right_index=l4+(r-1)*(nz+1)+last+1
              result%low=result%low-real(area(r),real64)* &
                real(unknown(left_index),real64)
              face_term=real(area(r),real64)* &
                real(unknown(right_index),real64)
              result%high=result%high+face_term
              ! Retain the same common +z contribution by track radial row.
              high_region(r)=high_region(r)+face_term
            endif
            first=last+1
          enddo
        enddo
      endif
    enddo
    if (.not.target_found) call fail('LEAKAGE FACE HOTSPOT WAS NOT FOUND.')
    result%net=result%low+result%high
    if ((.not.ieee_is_finite(result%low)).or. &
        (.not.ieee_is_finite(result%high)).or. &
        (.not.ieee_is_finite(result%net)).or. &
        (.not.ieee_is_finite(result%numerator)).or. &
        (.not.ieee_is_finite(result%denominator)).or. &
        (.not.ieee_is_finite(result%leakage))) &
      call fail('LEAKAGE FACE RESULT IS NON-FINITE.')
    deallocate(denominator,numerator,unknown)
    call LCMCL(root,1)
  end subroutine verify_raw_leakage_and_faces


  subroutine write_leakage_face_state(label,state)
    character(len=*), intent(in) :: label
    type(leakage_face_state), intent(in) :: state

    write(6,'(A,1X,A,3(1X,ES24.16E3))') &
      'LEAKAGE-FACES STATE FACE64 LOW/HIGH/NET',trim(label), &
      state%low,state%high,state%net
    write(6,'(A,1X,A,3(1X,ES24.16E3))') &
      'LEAKAGE-FACES STATE SP32 NUM/DEN/LEAK',trim(label), &
      real(state%numerator,real64),real(state%denominator,real64), &
      real(state%leakage,real64)
  end subroutine write_leakage_face_state


  subroutine write_leakage_face_delta(label,left,right)
    character(len=*), intent(in) :: label
    type(leakage_face_state), intent(in) :: left,right

    write(6,'(A,1X,A,3(1X,ES24.16E3))') &
      'LEAKAGE-FACES DELTA FACE64 LOW/HIGH/NET',trim(label), &
      right%low-left%low,right%high-left%high,right%net-left%net
    write(6,'(A,1X,A,3(1X,ES24.16E3))') &
      'LEAKAGE-FACES DELTA SP32 NUM/DEN/LEAK',trim(label), &
      real(right%numerator,real64)-real(left%numerator,real64), &
      real(right%denominator,real64)-real(left%denominator,real64), &
      real(right%leakage,real64)-real(left%leakage,real64)
  end subroutine write_leakage_face_delta


  subroutine write_face_dominance(label,delta_low,delta_high)
    character(len=*), intent(in) :: label
    real(real64), intent(in) :: delta_low,delta_high

    if (abs(delta_high) > abs(delta_low)) then
      write(6,'(A)') 'LEAKAGE-FACES DELTA'//trim(label)// &
        ' HIGH-Z-FACE-DOMINANT'
    else if (abs(delta_low) > abs(delta_high)) then
      write(6,'(A)') 'LEAKAGE-FACES DELTA'//trim(label)// &
        ' LOW-Z-FACE-DOMINANT'
    else
      write(6,'(A)') 'LEAKAGE-FACES DELTA'//trim(label)// &
        ' EQUAL-FACE-MAGNITUDE'
    endif
  end subroutine write_face_dominance


  subroutine write_high_face_regions(area,value,high_total)
    real(real32), intent(in) :: area(:)
    real(real64), intent(in) :: value(:,:)
    real(real64), intent(in) :: high_total(3)
    integer :: r,j,max_r(2),ties(2),nonzero(2),positive(2),negative(2)
    real(real64) :: delta(size(value,1),2),max_abs(2),sum_abs(2)
    real(real64) :: signed_sum(2),expected_sum(2)

    if ((size(value,2) /= 3).or.(size(area) /= size(value,1))) &
      call fail('LEAKAGE HIGH-FACE REGION DIMENSIONS ARE INVALID.')
    delta(:,1)=value(:,2)-value(:,1)
    delta(:,2)=value(:,3)-value(:,2)
    if (any(.not.ieee_is_finite(delta))) &
      call fail('LEAKAGE HIGH-FACE REGION DELTA IS NON-FINITE.')
    max_abs=0.0_real64
    max_r=0
    ties=0
    nonzero=0
    positive=0
    negative=0
    sum_abs=0.0_real64
    signed_sum=0.0_real64
    expected_sum=(/high_total(2)-high_total(1), &
      high_total(3)-high_total(2)/)
    do j=1,2
      do r=1,size(value,1)
        signed_sum(j)=signed_sum(j)+delta(r,j)
        sum_abs(j)=sum_abs(j)+abs(delta(r,j))
        if (abs(delta(r,j)) > max_abs(j)) max_abs(j)=abs(delta(r,j))
        if (delta(r,j) /= 0.0_real64) nonzero(j)=nonzero(j)+1
        if (delta(r,j) > 0.0_real64) positive(j)=positive(j)+1
        if (delta(r,j) < 0.0_real64) negative(j)=negative(j)+1
      enddo
      if (sum_abs(j) <= 0.0_real64) &
        call fail('LEAKAGE HIGH-FACE REGION UPDATE IS ZERO.')
      if (real64_bits(signed_sum(j)) /= real64_bits(expected_sum(j))) &
        call fail('LEAKAGE HIGH-FACE REGION SUM DOES NOT CLOSE BITWISE.')
      do r=1,size(value,1)
        if (real64_bits(abs(delta(r,j))) == real64_bits(max_abs(j))) then
          ties(j)=ties(j)+1
          if (max_r(j) == 0) max_r(j)=r
        endif
      enddo
    enddo

    write(6,'(A)') &
      'LEAKAGE-FACES HIGH-Z REGION AREA/DELTA12/DELTA23'
    do r=1,size(value,1)
      write(6,'(A,1X,I0,3(1X,ES24.16E3))') &
        'LEAKAGE-FACES HIGH-Z REGION',r,real(area(r),real64), &
        delta(r,1),delta(r,2)
    enddo
    write(6,'(A,4(1X,I0))') &
      'LEAKAGE-FACES HIGH-Z MAX-REGION/TIES 12/23', &
      max_r(1),ties(1),max_r(2),ties(2)
    write(6,'(A,2(1X,I0))') &
      'LEAKAGE-FACES HIGH-Z EXACT-NONZERO-REGIONS 12/23',nonzero
    write(6,'(A,6(1X,I0))') &
      'LEAKAGE-FACES HIGH-Z POS/NEG/ZERO 12/23', &
      positive(1),negative(1),size(value,1)-nonzero(1), &
      positive(2),negative(2),size(value,1)-nonzero(2)
    write(6,'(A)') 'LEAKAGE-FACES HIGH-Z REGION-SUM BITWISE PASS'
    if (nonzero(1) == 1) then
      write(6,'(A)') 'LEAKAGE-FACES HIGH-Z DELTA12 EXACT-SINGLE-REGION'
    else
      write(6,'(A)') 'LEAKAGE-FACES HIGH-Z DELTA12 EXACT-MULTI-REGION'
    endif
    if (nonzero(2) == 1) then
      write(6,'(A)') 'LEAKAGE-FACES HIGH-Z DELTA23 EXACT-SINGLE-REGION'
    else
      write(6,'(A)') 'LEAKAGE-FACES HIGH-Z DELTA23 EXACT-MULTI-REGION'
    endif
    write(6,'(A,2(1X,ES24.16E3))') &
      'LEAKAGE-FACES HIGH-Z MAX-ABS/L1-SHARE 12/23', &
      max_abs(1)/sum_abs(1),max_abs(2)/sum_abs(2)
  end subroutine write_high_face_regions


  subroutine write_interface_ratios(interface_z,phi_below,phi_above, &
      face_current)
    integer, intent(in) :: interface_z
    real(real64), intent(in) :: phi_below(:,:),phi_above(:,:)
    real(real64), intent(in) :: face_current(:,:)
    integer :: r,j,nr
    integer :: ratio_positive(2),ratio_negative(2)
    integer :: current_positive(2),current_negative(2)
    integer :: face_positive,face_negative
    real(real64) :: phi_ratio(size(phi_below,1),3)
    real(real64) :: current_ratio(size(phi_below,1),3)
    real(real64) :: ratio_delta(size(phi_below,1),2)
    real(real64) :: current_delta(size(phi_below,1),2)

    nr=size(phi_below,1)
    if ((size(phi_below,2) /= 3).or. &
        any(shape(phi_above) /= shape(phi_below)).or. &
        any(shape(face_current) /= shape(phi_below))) &
      call fail('LEAKAGE FACE INTERFACE DIMENSIONS ARE INVALID.')
    if (any(.not.ieee_is_finite(phi_below)).or. &
        any(.not.ieee_is_finite(phi_above)).or. &
        any(.not.ieee_is_finite(face_current)).or. &
        any(phi_below <= 0.0_real64).or.any(phi_above <= 0.0_real64)) &
      call fail('LEAKAGE FACE INTERFACE VALUES ARE INVALID.')

    phi_ratio=phi_above/phi_below
    current_ratio=2.0_real64*face_current/(phi_below+phi_above)
    ratio_delta(:,1)=phi_ratio(:,2)-phi_ratio(:,1)
    ratio_delta(:,2)=phi_ratio(:,3)-phi_ratio(:,2)
    current_delta(:,1)=current_ratio(:,2)-current_ratio(:,1)
    current_delta(:,2)=current_ratio(:,3)-current_ratio(:,2)
    if (any(.not.ieee_is_finite(phi_ratio)).or. &
        any(.not.ieee_is_finite(current_ratio)).or. &
        any(.not.ieee_is_finite(ratio_delta)).or. &
        any(.not.ieee_is_finite(current_delta))) &
      call fail('LEAKAGE FACE INTERFACE RATIO IS NON-FINITE.')

    face_positive=count(face_current > 0.0_real64)
    face_negative=count(face_current < 0.0_real64)

    do j=1,2
      ratio_positive(j)=count(ratio_delta(:,j) > 0.0_real64)
      ratio_negative(j)=count(ratio_delta(:,j) < 0.0_real64)
      current_positive(j)=count(current_delta(:,j) > 0.0_real64)
      current_negative(j)=count(current_delta(:,j) < 0.0_real64)
    enddo

    write(6,'(A,3(1X,I0))') &
      'LEAKAGE-FACES INTERFACE FLOOR-BELOW/ABOVE/FACE', &
      interface_z,interface_z+1,interface_z+1
    write(6,'(A)') &
      'LEAKAGE-FACES INTERFACE NORMALIZATION-INVARIANT'
    write(6,'(A)') &
      'LEAKAGE-FACES INTERFACE R_PHI=PHI_ABOVE/PHI_BELOW'
    write(6,'(A)') &
      'LEAKAGE-FACES INTERFACE Q_J=2*J_FACE/(PHI_BELOW+PHI_ABOVE)'
    write(6,'(A)') &
      'LEAKAGE-FACES INTERFACE REGION R_PHI-X1/X2/X3 Q_J-X1/X2/X3'
    do r=1,nr
      write(6,'(A,1X,I0,6(1X,ES24.16E3))') &
        'LEAKAGE-FACES INTERFACE REGION',r,phi_ratio(r,:), &
        current_ratio(r,:)
    enddo
    write(6,'(A,6(1X,I0))') &
      'LEAKAGE-FACES INTERFACE R_PHI POS/NEG/ZERO 12/23', &
      ratio_positive(1),ratio_negative(1), &
      nr-ratio_positive(1)-ratio_negative(1), &
      ratio_positive(2),ratio_negative(2), &
      nr-ratio_positive(2)-ratio_negative(2)
    write(6,'(A,6(1X,I0))') &
      'LEAKAGE-FACES INTERFACE Q_J POS/NEG/ZERO 12/23', &
      current_positive(1),current_negative(1), &
      nr-current_positive(1)-current_negative(1), &
      current_positive(2),current_negative(2), &
      nr-current_positive(2)-current_negative(2)
    write(6,'(A,3(1X,I0))') &
      'LEAKAGE-FACES INTERFACE J_FACE POS/NEG/ZERO ALL-STATES', &
      face_positive,face_negative,3*nr-face_positive-face_negative
    write(6,'(A)') 'LEAKAGE-FACES INTERFACE NO-FICK-INFERENCE'
  end subroutine write_interface_ratios


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
