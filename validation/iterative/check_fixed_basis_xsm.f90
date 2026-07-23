program check_fixed_basis_xsm
  ! Independent Ganlib-only, read-only check of the Stage-0B fixture.
  !
  !   check_fixed_basis_xsm basis_reference.xsm fixed_system.xsm
  !
  ! The caller must generate both systems from the same snapshot archive.
  ! This checker verifies that FIXB changes only the root basis-provenance
  ! markers: every stored POD record remains bit-identical and the live
  ! RADIAL-OP reconstruction is also bit-identical for that same input.
  ! It calls no Dragon, SPOT, assembly, or transport routine.
  use GANLIB
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
    integer :: ngroup=0
    integer, allocatable :: rank_root(:)
    real(real64), allocatable :: sigma_root(:,:)
    type(group_data), allocatable :: group(:)
  end type system_data

  character(len=1024) :: reference_path,fixed_path
  type(system_data) :: reference,fixed
  integer :: g,min_nreg,max_nreg,min_nsnap,max_nsnap
  integer :: min_nmode,max_nmode

  if (command_argument_count() /= 2) call fail( &
    'TWO ARGUMENTS EXPECTED: BASIS_REFERENCE.XSM FIXED_SYSTEM.XSM.')
  call get_command_argument(1,reference_path)
  call get_command_argument(2,fixed_path)
  if ((len_trim(reference_path) == 0).or.(len_trim(fixed_path) == 0)) &
    call fail('EMPTY XSM PATH ARGUMENT.')
  if ((len_trim(reference_path) > max_xsm_path).or. &
      (len_trim(fixed_path) > max_xsm_path)) &
    call fail('XSM PATH ARGUMENT EXCEEDS GANLIB LIMIT.')

  call load_system(trim(reference_path),0,'POD-BUILT',.false., &
    reference,'BASIS REFERENCE')
  call load_system(trim(fixed_path),1,'POD-FIXED',.true., &
    fixed,'FIXED SYSTEM')
  call compare_systems(reference,fixed)

  min_nreg=huge(0)
  max_nreg=0
  min_nsnap=huge(0)
  max_nsnap=0
  min_nmode=huge(0)
  max_nmode=0
  do g=1,reference%ngroup
    min_nreg=min(min_nreg,reference%group(g)%nreg)
    max_nreg=max(max_nreg,reference%group(g)%nreg)
    min_nsnap=min(min_nsnap,reference%group(g)%nsnap)
    max_nsnap=max(max_nsnap,reference%group(g)%nsnap)
    min_nmode=min(min_nmode,reference%group(g)%nmode)
    max_nmode=max(max_nmode,reference%group(g)%nmode)
  enddo

  write(6,'(A,7(1X,I0))') 'FIXED-BASIS-XSM DIMS',reference%ngroup, &
    min_nreg,max_nreg,min_nsnap,max_nsnap,min_nmode,max_nmode
  write(6,'(A)') 'FIXED-BASIS-XSM MARKERS PASS'
  write(6,'(A)') 'FIXED-BASIS-XSM POD-PACKAGE BITWISE PASS'
  write(6,'(A)') 'FIXED-BASIS-XSM SAME-SNAPSHOT RADIAL-OP BITWISE PASS'
  write(6,'(A)') 'FIXED-BASIS-XSM COMPLETE'

contains

  subroutine load_system(path,expected_fixb,expected_type, &
      expect_basis_link,data,owner)
    character(len=*), intent(in) :: path,expected_type,owner
    integer, intent(in) :: expected_fixb
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
    if ((data%ngroup <= 0).or.(data%state(14) /= 1)) &
      call fail(trim(owner)//' INVALID SPOD STATE-VECTOR.')

    call require_record(root,'SPOT-FIXB',1,1,owner)
    call LCMGET(root,'SPOT-FIXB',data%fixb)
    if (data%fixb /= expected_fixb) &
      call fail(trim(owner)//' SPOT-FIXB MARKER IS INVALID.')
    call require_record(root,'SPOT-BTYPE',3,3,owner)
    call LCMGTC(root,'SPOT-BTYPE',12,data%basis_type)
    if (data%basis_type /= expected_type) &
      call fail(trim(owner)//' SPOT-BTYPE MARKER IS INVALID.')

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
      if ((nreg0 <= 0).or.(nsnap0 <= 0).or.(nmode0 <= 0).or. &
          (nmode0 > nsnap0).or.(data%rank_root(g) /= nmode0)) &
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
    enddo

    call require_record(root,'POD-SIGMA-G', &
      nsnap_root*data%ngroup,4,owner)
    allocate(data%sigma_root(nsnap_root,data%ngroup))
    call LCMGET(root,'POD-SIGMA-G',data%sigma_root)
    do g=1,data%ngroup
      if (any(real64_bits(data%sigma_root(:,g)) /= &
              real64_bits(data%group(g)%sigma))) &
        call fail(trim(owner)//' GROUP/ROOT POD-SIGMA BITS DIFFER.')
    enddo
    call LCMCL(root,1)
  end subroutine load_system


  subroutine compare_systems(reference0,fixed0)
    type(system_data), intent(in) :: reference0,fixed0
    integer :: g
    character(len=128) :: label

    if ((reference0%signature /= fixed0%signature).or. &
        (reference0%signature /= 'L_PIJ')) &
      call fail('SYSTEM SIGNATURES DIFFER.')
    if (reference0%fixb /= 0) &
      call fail('REFERENCE SPOT-FIXB IS NOT ZERO.')
    if (fixed0%fixb /= 1) &
      call fail('FIXED SPOT-FIXB IS NOT ONE.')
    if ((reference0%basis_type /= 'POD-BUILT').or. &
        (fixed0%basis_type /= 'POD-FIXED')) &
      call fail('SYSTEM SPOT-BTYPE MARKERS ARE INVALID.')
    if (len_trim(reference0%link_basis) /= 0) &
      call fail('REFERENCE SYSTEM HAS A BASIS LINK.')
    if (len_trim(fixed0%link_basis) == 0) &
      call fail('FIXED SYSTEM HAS NO BASIS LINK.')
    if ((reference0%link_macro /= fixed0%link_macro).or. &
        (reference0%link_track /= fixed0%link_track)) &
      call fail('SYSTEM INPUT LINK MARKERS DIFFER.')
    if (any(reference0%state /= fixed0%state)) &
      call fail('SYSTEM STATE-VECTOR RECORDS DIFFER.')
    if (reference0%ngroup /= fixed0%ngroup) &
      call fail('SYSTEM GROUP COUNTS DIFFER.')
    if (any(reference0%rank_root /= fixed0%rank_root)) &
      call fail('ROOT POD-RANK-G RECORDS DIFFER.')
    if (any(real64_bits(reference0%sigma_root) /= &
            real64_bits(fixed0%sigma_root))) &
      call fail('ROOT POD-SIGMA-G RECORDS DIFFER BITWISE.')

    do g=1,reference0%ngroup
      write(label,'(A,I0)') 'GROUP ',g
      if (reference0%group(g)%nreg /= fixed0%group(g)%nreg) &
        call fail(trim(label)//' NREG2D RECORDS DIFFER.')
      if (reference0%group(g)%nsnap /= fixed0%group(g)%nsnap) &
        call fail(trim(label)//' NSNAP RECORDS DIFFER.')
      if (reference0%group(g)%nmode /= fixed0%group(g)%nmode) &
        call fail(trim(label)//' POD-NMODE RECORDS DIFFER.')
      if (any(real32_bits(reference0%group(g)%volume) /= &
              real32_bits(fixed0%group(g)%volume))) &
        call fail(trim(label)//' VOL2D RECORDS DIFFER BITWISE.')
      if (any(real32_bits(reference0%group(g)%basis) /= &
              real32_bits(fixed0%group(g)%basis))) &
        call fail(trim(label)//' POD-BASIS RECORDS DIFFER BITWISE.')
      if (any(real32_bits(reference0%group(g)%coeff) /= &
              real32_bits(fixed0%group(g)%coeff))) &
        call fail(trim(label)//' POD-COEFF RECORDS DIFFER BITWISE.')
      if (any(real64_bits(reference0%group(g)%sigma) /= &
              real64_bits(fixed0%group(g)%sigma))) &
        call fail(trim(label)//' POD-SIGMA RECORDS DIFFER BITWISE.')
      if (real64_bits(reference0%group(g)%rec_err) /= &
          real64_bits(fixed0%group(g)%rec_err)) &
        call fail(trim(label)//' POD-REC-ERR RECORDS DIFFER BITWISE.')
      if (real64_bits(reference0%group(g)%ortho) /= &
          real64_bits(fixed0%group(g)%ortho)) &
        call fail(trim(label)//' POD-ORTHO RECORDS DIFFER BITWISE.')
      if (any(real32_bits(reference0%group(g)%radial) /= &
              real32_bits(fixed0%group(g)%radial))) &
        call fail(trim(label)//' RADIAL-OP RECORDS DIFFER BITWISE.')
    enddo
  end subroutine compare_systems


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

    write(0,'(A)') 'FIXED-BASIS-XSM ERROR: '//trim(message)
    error stop 2
  end subroutine fail

end program check_fixed_basis_xsm
