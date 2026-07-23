program check_inner_sensitivity_xsm
  ! Independent, read-only Ganlib audit of the Stage-4 inner-tolerance pair.
  !
  ! Arguments:
  !   x0_h x1_h x0_h2 x1_h2 snap1_h snap1_h2
  !
  ! The program does not solve transport and does not assign a numerical
  ! acceptance threshold.  It verifies the common discrete state, recomputes
  ! the three ordered defect vectors, and reports exact componentwise order.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32,int64,real32,real64
  implicit none

  integer, parameter :: nstate=40
  integer, parameter :: expected_groups=370
  integer, parameter :: expected_planes=3
  integer, parameter :: expected_rank=1
  integer, parameter :: expected_regions=8
  integer, parameter :: expected_coefficients=1110
  integer, parameter :: max_xsm_path=72

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

  type :: plane_input
    integer :: nunknown=0
    real(real32), allocatable :: leakage(:)
    real(real32), allocatable :: qfiss(:,:)
    real(real32) :: source_keff=0.0_real32
  end type plane_input

  type :: restart_inputs
    type(plane_input) :: plane(expected_planes)
  end type restart_inputs

  character(len=1024) :: paths(6)
  character(len=5), parameter :: component_name(4) = &
    [character(len=5) :: 'RRHO','RLEAK','DLEAK','RA']
  type(canonical_state) :: x0_h,x1_h,x0_h2,x1_h2
  type(restart_inputs) :: restart_h,restart_h2
  real(real64) :: dout_h(4),dout_h2(4),dout_h2_shared_x0(4),din(4)
  integer :: i

  if (command_argument_count() /= 6) call fail( &
    'SIX ARGUMENTS EXPECTED: X0_H X1_H X0_H2 X1_H2 SNAP1_H SNAP1_H2.')
  do i=1,6
    call get_command_argument(i,paths(i))
    if (len_trim(paths(i)) == 0) call fail('EMPTY XSM PATH ARGUMENT.')
    if (len_trim(paths(i)) > max_xsm_path) &
      call fail('XSM PATH ARGUMENT EXCEEDS GANLIB LIMIT.')
  enddo

  call load_canonical_state(trim(paths(1)),0,'POD-BUILT',.false., &
    x0_h,'X0 H')
  call load_canonical_state(trim(paths(2)),1,'POD-FIXED',.true., &
    x1_h,'X1 H')
  call load_canonical_state(trim(paths(3)),0,'POD-BUILT',.false., &
    x0_h2,'X0 H2')
  call load_canonical_state(trim(paths(4)),1,'POD-FIXED',.true., &
    x1_h2,'X1 H2')

  call compare_complete_x0(x0_h,x0_h2)
  call compare_trial_space(x0_h,x1_h,'X1 H')
  call compare_trial_space(x0_h,x1_h2,'X1 H2')

  call recompute_defect(x0_h,x1_h,dout_h)
  if (any(real64_bits(dout_h) /= real64_bits(x1_h%saved_defect))) &
    call fail('DOUT H DIFFERS FROM ITS SAVED DEFECT BITS.')
  call recompute_defect(x0_h2,x1_h2,dout_h2)
  if (any(real64_bits(dout_h2) /= real64_bits(x1_h2%saved_defect))) &
    call fail('DOUT H2 DIFFERS FROM ITS SAVED DEFECT BITS.')
  call recompute_defect(x0_h,x1_h2,dout_h2_shared_x0)
  if (any(real64_bits(dout_h2_shared_x0) /= real64_bits(dout_h2))) &
    call fail('DOUT H2 DEPENDS ON WHICH IDENTICAL X0 OBJECT IS USED.')
  call recompute_defect(x1_h,x1_h2,din)

  call load_restart_inputs(trim(paths(5)),restart_h,'SNAP1 H')
  call load_restart_inputs(trim(paths(6)),restart_h2,'SNAP1 H2')
  call link_restart_to_x0(restart_h,x0_h,'SNAP1 H')
  call link_restart_to_x0(restart_h2,x0_h2,'SNAP1 H2')
  call compare_restart_inputs(restart_h,restart_h2)

  write(6,'(A)') 'INNER-SENSITIVITY X0 CANONICAL BITWISE IDENTICAL'
  write(6,'(A)') 'INNER-SENSITIVITY TRIAL-SPACE BITWISE IDENTICAL'
  write(6,'(A)') 'INNER-SENSITIVITY RADIAL-INPUTS BITWISE IDENTICAL'
  write(6,'(A)') 'INNER-SENSITIVITY ORDER RRHO RLEAK DLEAK RA'
  write(6,'(A,4(1X,ES25.17E3))') 'INNER-SENSITIVITY DOUT-H',dout_h
  write(6,'(A,4(1X,ES25.17E3))') 'INNER-SENSITIVITY DOUT-H2',dout_h2
  write(6,'(A,4(1X,ES25.17E3))') 'INNER-SENSITIVITY DIN',din
  do i=1,4
    write(6,'(A,1X,A,1X,A,1X,A,1X,A,1X,A)') &
      'INNER-SENSITIVITY COMPONENT',trim(component_name(i)), &
      'DIN-VS-DOUT-H',trim(relation(din(i),dout_h(i))), &
      'DIN-VS-DOUT-H2',trim(relation(din(i),dout_h2(i)))
  enddo
  write(6,'(A)') 'INNER-SENSITIVITY COMPLETE'

contains

  subroutine load_canonical_state(path,expected_fixb,expected_type, &
      expect_saved_defect,data,owner)
    character(len=*), intent(in) :: path,expected_type,owner
    integer, intent(in) :: expected_fixb
    logical, intent(in) :: expect_saved_defect
    type(canonical_state), intent(out) :: data
    type(c_ptr) :: root
    integer :: g,total_basis,total_gram

    call LCMOP(root,path,2,2,0)
    call require_record(root,'SIGNATURE',3,3,owner)
    call LCMGTC(root,'SIGNATURE',12,data%signature)
    if (data%signature /= 'L_FLUX') &
      call fail(trim(owner)//' L_FLUX SIGNATURE EXPECTED.')
    call require_record(root,'STATE-VECTOR',nstate,1,owner)
    call LCMGET(root,'STATE-VECTOR',data%state)

    call require_record(root,'SPOT-X-DIMS',4,1,owner)
    call LCMGET(root,'SPOT-X-DIMS',data%dims)
    if (any(data%dims /= &
        (/expected_rank,expected_groups,expected_planes, &
          expected_coefficients/)).or. &
        (data%state(1) /= expected_groups)) &
      call fail(trim(owner)//' INVALID CANONICAL DIMENSIONS.')

    allocate(data%rank(expected_groups))
    allocate(data%offset(expected_groups+1))
    allocate(data%gram_offset(expected_groups+1))
    allocate(data%basis_offset(expected_groups+1))
    call require_record(root,'SPOT-X-RANK',expected_groups,1,owner)
    call require_record(root,'SPOT-X-OFF',expected_groups+1,1,owner)
    call require_record(root,'SPOT-X-GOFF',expected_groups+1,1,owner)
    call require_record(root,'SPOT-X-BOFF',expected_groups+1,1,owner)
    call LCMGET(root,'SPOT-X-RANK',data%rank)
    call LCMGET(root,'SPOT-X-OFF',data%offset)
    call LCMGET(root,'SPOT-X-GOFF',data%gram_offset)
    call LCMGET(root,'SPOT-X-BOFF',data%basis_offset)
    if (any(data%rank /= expected_rank).or. &
        (data%offset(1) /= 0).or.(data%gram_offset(1) /= 0).or. &
        (data%basis_offset(1) /= 0)) &
      call fail(trim(owner)//' INVALID RANK OR OFFSET ORIGIN.')
    do g=1,expected_groups
      if (data%offset(g+1)-data%offset(g) /= &
          expected_planes*expected_rank) &
        call fail(trim(owner)//' INVALID COORDINATE OFFSETS.')
      if (data%gram_offset(g+1)-data%gram_offset(g) /= &
          expected_rank*expected_rank) &
        call fail(trim(owner)//' INVALID GRAM OFFSETS.')
      if (data%basis_offset(g+1)-data%basis_offset(g) /= &
          expected_regions*expected_rank) &
        call fail(trim(owner)//' INVALID BASIS OFFSETS.')
    enddo
    if (data%offset(expected_groups+1) /= expected_coefficients) &
      call fail(trim(owner)//' INVALID COORDINATE EXTENT.')
    total_basis=data%basis_offset(expected_groups+1)
    total_gram=data%gram_offset(expected_groups+1)
    if ((total_basis /= expected_groups*expected_regions*expected_rank).or. &
        (total_gram /= expected_groups*expected_rank*expected_rank)) &
      call fail(trim(owner)//' INVALID FIXED-SPACE EXTENT.')

    allocate(data%basis(total_basis))
    allocate(data%coordinates(expected_coefficients))
    allocate(data%leakage(expected_groups*expected_planes))
    allocate(data%height(expected_planes))
    allocate(data%gram(total_gram))
    allocate(data%offspace(expected_groups*expected_planes))
    call require_record(root,'SPOT-X-BASIS',total_basis,2,owner)
    call require_record(root,'SPOT-X-A',expected_coefficients,4,owner)
    call require_record(root,'SPOT-X-L', &
      expected_groups*expected_planes,4,owner)
    call require_record(root,'SPOT-X-H',expected_planes,4,owner)
    call require_record(root,'SPOT-X-GRAM',total_gram,4,owner)
    call require_record(root,'SPOT-X-PERP', &
      expected_groups*expected_planes,4,owner)
    call require_record(root,'K-EFFECTIVE',1,2,owner)
    call require_record(root,'SPOT-X-RHO',1,4,owner)
    call require_record(root,'SPOT-X-NORM',1,4,owner)
    call require_record(root,'SPOT-X-GERR',1,4,owner)
    call require_record(root,'SPOT-X-FIXB',1,1,owner)
    call require_record(root,'SPOT-X-NID',3,3,owner)
    call require_record(root,'SPOT-X-BTYP',3,3,owner)
    call LCMGET(root,'SPOT-X-BASIS',data%basis)
    call LCMGET(root,'SPOT-X-A',data%coordinates)
    call LCMGET(root,'SPOT-X-L',data%leakage)
    call LCMGET(root,'SPOT-X-H',data%height)
    call LCMGET(root,'SPOT-X-GRAM',data%gram)
    call LCMGET(root,'SPOT-X-PERP',data%offspace)
    call LCMGET(root,'K-EFFECTIVE',data%keff)
    call LCMGET(root,'SPOT-X-RHO',data%rho)
    call LCMGET(root,'SPOT-X-NORM',data%norm)
    call LCMGET(root,'SPOT-X-GERR',data%gram_error)
    call LCMGET(root,'SPOT-X-FIXB',data%fixb)
    call LCMGTC(root,'SPOT-X-NID',12,data%norm_id)
    call LCMGTC(root,'SPOT-X-BTYP',12,data%basis_type)

    if ((data%fixb /= expected_fixb).or. &
        (data%basis_type /= expected_type)) &
      call fail(trim(owner)//' INVALID FIXED-BASIS MARKERS.')
    if (data%norm_id /= 'NUFISS-UNIT') &
      call fail(trim(owner)//' INVALID NORMALIZATION ID.')
    if (any(.not.ieee_is_finite(data%basis)).or. &
        any(.not.ieee_is_finite(data%coordinates)).or. &
        any(.not.ieee_is_finite(data%leakage)).or. &
        any(.not.ieee_is_finite(data%height)).or. &
        any(data%height <= 0.0_real64).or. &
        any(.not.ieee_is_finite(data%gram)).or. &
        any(data%gram <= 0.0_real64).or. &
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
        call fail(trim(owner)//' INVALID SAVED DEFECT.')
    else
      call require_absent(root,'SPOT-X-RRHO',owner)
      call require_absent(root,'SPOT-X-RLEAK',owner)
      call require_absent(root,'SPOT-X-DLEAK',owner)
      call require_absent(root,'SPOT-X-RA',owner)
    endif
    call LCMCL(root,1)
  end subroutine load_canonical_state


  subroutine compare_complete_x0(left,right)
    type(canonical_state), intent(in) :: left,right

    if ((left%signature /= right%signature).or. &
        (left%norm_id /= right%norm_id).or. &
        (left%basis_type /= right%basis_type).or. &
        (left%fixb /= right%fixb).or. &
        (left%has_saved_defect .neqv. right%has_saved_defect)) &
      call fail('X0 CHARACTER OR MARKER RECORDS DIFFER.')
    if (any(left%state /= right%state).or.any(left%dims /= right%dims).or. &
        any(left%rank /= right%rank).or. &
        any(left%offset /= right%offset).or. &
        any(left%gram_offset /= right%gram_offset).or. &
        any(left%basis_offset /= right%basis_offset)) &
      call fail('X0 INTEGER RECORDS DIFFER BITWISE.')
    if (any(real32_bits(left%basis) /= real32_bits(right%basis)).or. &
        (real32_bits(left%keff) /= real32_bits(right%keff))) &
      call fail('X0 BINARY32 RECORDS DIFFER BITWISE.')
    if (any(real64_bits(left%coordinates) /= &
            real64_bits(right%coordinates)).or. &
        any(real64_bits(left%leakage) /= real64_bits(right%leakage)).or. &
        any(real64_bits(left%height) /= real64_bits(right%height)).or. &
        any(real64_bits(left%gram) /= real64_bits(right%gram)).or. &
        any(real64_bits(left%offspace) /= real64_bits(right%offspace)).or. &
        (real64_bits(left%rho) /= real64_bits(right%rho)).or. &
        (real64_bits(left%norm) /= real64_bits(right%norm)).or. &
        (real64_bits(left%gram_error) /= &
         real64_bits(right%gram_error))) &
      call fail('X0 BINARY64 RECORDS DIFFER BITWISE.')
  end subroutine compare_complete_x0


  subroutine compare_trial_space(reference,candidate,owner)
    type(canonical_state), intent(in) :: reference,candidate
    character(len=*), intent(in) :: owner

    if ((reference%signature /= candidate%signature).or. &
        (reference%norm_id /= candidate%norm_id)) &
      call fail(trim(owner)//' SIGNATURE OR NORMALIZATION ID CHANGED.')
    if (any(reference%state /= candidate%state).or. &
        any(reference%dims /= candidate%dims).or. &
        any(reference%rank /= candidate%rank).or. &
        any(reference%offset /= candidate%offset).or. &
        any(reference%gram_offset /= candidate%gram_offset).or. &
        any(reference%basis_offset /= candidate%basis_offset)) &
      call fail(trim(owner)//' FIXED-SPACE LAYOUT CHANGED.')
    if (any(real32_bits(reference%basis) /= &
            real32_bits(candidate%basis)).or. &
        any(real64_bits(reference%gram) /= &
            real64_bits(candidate%gram)).or. &
        any(real64_bits(reference%height) /= &
            real64_bits(candidate%height))) &
      call fail(trim(owner)//' TRIAL SPACE, GRAM, OR HEIGHT CHANGED.')
  end subroutine compare_trial_space


  subroutine recompute_defect(previous,current,defect)
    type(canonical_state), intent(in) :: previous,current
    real(real64), intent(out) :: defect(4)
    integer :: group,plane,a,b,nmode,index_a,index_b,index_g
    real(real64) :: r_rho,r_leak,d_leak,r_a
    real(real64) :: leak_scale_current,leak_scale_previous,leak_scale
    real(real64) :: numerator,denominator,delta

    call compare_trial_space(previous,current,'ORDERED STATE PAIR')
    r_rho=abs(current%rho-previous%rho)
    d_leak=maxval(abs(current%leakage-previous%leakage))
    leak_scale_current=maxval(abs(current%leakage))
    leak_scale_previous=maxval(abs(previous%leakage))
    leak_scale=max(leak_scale_current,leak_scale_previous)
    if (leak_scale == 0.0_real64) then
      if (d_leak /= 0.0_real64) call fail('INVALID ZERO-LEAKAGE BRANCH.')
      r_leak=0.0_real64
    else
      r_leak=d_leak/leak_scale
    endif

    numerator=0.0_real64
    denominator=0.0_real64
    do group=1,expected_groups
      nmode=current%rank(group)
      do plane=1,expected_planes
        do a=1,nmode
          index_a=current%offset(group)+(plane-1)*nmode+a
          delta=current%coordinates(index_a)- &
            previous%coordinates(index_a)
          do b=1,nmode
            index_b=current%offset(group)+(plane-1)*nmode+b
            index_g=current%gram_offset(group)+(b-1)*nmode+a
            numerator=numerator+current%height(plane)*delta* &
              current%gram(index_g)*(current%coordinates(index_b)- &
              previous%coordinates(index_b))
            denominator=denominator+current%height(plane)* &
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
      call fail('NON-FINITE RECOMPUTED DEFECT.')
    defect=(/r_rho,r_leak,d_leak,r_a/)
  end subroutine recompute_defect


  subroutine load_restart_inputs(path,data,owner)
    character(len=*), intent(in) :: path,owner
    type(restart_inputs), intent(out) :: data
    type(c_ptr) :: root,fluxes,systems,tracks,libraries
    type(c_ptr) :: flux_ptr,system_ptr,flux_list,q_outer,q_groups
    integer :: listdim,plane,group,flux_state(nstate),marker
    real(real32) :: l1_error
    real(real64) :: iter_keff
    character(len=12) :: signature
    character(len=96) :: label

    call LCMOP(root,path,2,2,0)
    call require_record(root,'SIGNATURE',3,3,owner)
    call LCMGTC(root,'SIGNATURE',12,signature)
    if (signature /= 'L_ARCHIVE') &
      call fail(trim(owner)//' L_ARCHIVE SIGNATURE EXPECTED.')
    call require_record(root,'LISTDIM',1,1,owner)
    call LCMGET(root,'LISTDIM',listdim)
    if (listdim /= expected_planes) &
      call fail(trim(owner)//' INVALID PLANE COUNT.')
    call require_record(root,'TRACK',expected_planes,10,owner)
    call require_record(root,'MICROLIB2',expected_planes,10,owner)
    call require_record(root,'SYSTEM',expected_planes,10,owner)
    call require_record(root,'FLUX',expected_planes,10,owner)
    call require_record(root,'SPOT-ITER-K',1,4,owner)
    call require_record(root,'SPOT-L1-ERR',1,2,owner)
    call LCMGET(root,'SPOT-ITER-K',iter_keff)
    call LCMGET(root,'SPOT-L1-ERR',l1_error)
    if ((.not.ieee_is_finite(iter_keff)).or.(iter_keff <= 0.0_real64).or. &
        (.not.ieee_is_finite(l1_error)).or.(l1_error < 0.0_real32)) &
      call fail(trim(owner)//' INVALID RESTART SUMMARY.')

    tracks=LCMGID(root,'TRACK')
    libraries=LCMGID(root,'MICROLIB2')
    systems=LCMGID(root,'SYSTEM')
    fluxes=LCMGID(root,'FLUX')
    do plane=1,expected_planes
      write(label,'(A,1X,I0)') trim(owner)//' PLANE',plane
      call require_directory_item(tracks,plane,trim(label)//' TRACK')
      call require_directory_item(libraries,plane,trim(label)//' LIBRARY')
      call require_directory_item(systems,plane,trim(label)//' SYSTEM')
      call require_directory_item(fluxes,plane,trim(label)//' FLUX')
      system_ptr=LCMGIL(systems,plane)
      flux_ptr=LCMGIL(fluxes,plane)

      call require_record(system_ptr,'SIGNATURE',3,3,label)
      call LCMGTC(system_ptr,'SIGNATURE',12,signature)
      if (signature /= 'L_PIJ') &
        call fail(trim(label)//' SYSTEM L_PIJ SIGNATURE EXPECTED.')
      call require_record(system_ptr,'SPOT-LEAK1D',expected_groups,2,label)
      allocate(data%plane(plane)%leakage(expected_groups))
      call LCMGET(system_ptr,'SPOT-LEAK1D', &
        data%plane(plane)%leakage)
      if (any(.not.ieee_is_finite(data%plane(plane)%leakage))) &
        call fail(trim(label)//' NON-FINITE RADIAL-INPUT LEAKAGE.')

      call require_record(flux_ptr,'SIGNATURE',3,3,label)
      call LCMGTC(flux_ptr,'SIGNATURE',12,signature)
      if (signature /= 'L_FLUX') &
        call fail(trim(label)//' FLUX L_FLUX SIGNATURE EXPECTED.')
      call require_record(flux_ptr,'STATE-VECTOR',nstate,1,label)
      call LCMGET(flux_ptr,'STATE-VECTOR',flux_state)
      data%plane(plane)%nunknown=flux_state(2)
      if ((flux_state(1) /= expected_groups).or. &
          (data%plane(plane)%nunknown <= 0)) &
        call fail(trim(label)//' INVALID RADIAL FLUX DIMENSIONS.')
      call require_record(flux_ptr,'FLUX',expected_groups,10,label)
      flux_list=LCMGID(flux_ptr,'FLUX')
      do group=1,expected_groups
        call require_list_item(flux_list,group, &
          data%plane(plane)%nunknown,2,trim(label)//' FLUX')
      enddo

      call require_record(flux_ptr,'SPOT-FS-EQN',1,1,label)
      call LCMGET(flux_ptr,'SPOT-FS-EQN',marker)
      if (marker /= 1) &
        call fail(trim(label)//' INVALID FIXED-SOURCE EQUATION MARKER.')
      call require_record(flux_ptr,'SPOT-FS-K',1,2,label)
      call LCMGET(flux_ptr,'SPOT-FS-K', &
        data%plane(plane)%source_keff)
      if ((.not.ieee_is_finite(data%plane(plane)%source_keff)).or. &
          (data%plane(plane)%source_keff <= 0.0_real32)) &
        call fail(trim(label)//' INVALID FROZEN-SOURCE EIGENVALUE.')

      call require_record(flux_ptr,'SPOT-QFISS',1,10,label)
      q_outer=LCMGID(flux_ptr,'SPOT-QFISS')
      call require_list_item(q_outer,1,expected_groups,10, &
        trim(label)//' SPOT-QFISS OUTER')
      q_groups=LCMGIL(q_outer,1)
      allocate(data%plane(plane)%qfiss( &
        data%plane(plane)%nunknown,expected_groups))
      do group=1,expected_groups
        call require_list_item(q_groups,group, &
          data%plane(plane)%nunknown,2,trim(label)//' SPOT-QFISS')
        call LCMGDL(q_groups,group, &
          data%plane(plane)%qfiss(:,group))
      enddo
      if (any(.not.ieee_is_finite(data%plane(plane)%qfiss)).or. &
          any(data%plane(plane)%qfiss < 0.0_real32).or. &
          (maxval(data%plane(plane)%qfiss) <= 0.0_real32)) &
        call fail(trim(label)//' INVALID FROZEN FISSION SOURCE.')
    enddo
    call LCMCL(root,1)
  end subroutine load_restart_inputs


  subroutine link_restart_to_x0(restart,x0,owner)
    type(restart_inputs), intent(in) :: restart
    type(canonical_state), intent(in) :: x0
    character(len=*), intent(in) :: owner
    integer :: plane,first,last
    character(len=96) :: label

    do plane=1,expected_planes
      write(label,'(A,1X,I0)') trim(owner)//' PLANE',plane
      first=(plane-1)*expected_groups+1
      last=plane*expected_groups
      if (any(real32_bits(restart%plane(plane)%leakage) /= &
              real32_bits(real(x0%leakage(first:last),real32)))) &
        call fail(trim(label)//' RADIAL LEAKAGE IS NOT X0 LEAKAGE.')
      if (real32_bits(restart%plane(plane)%source_keff) /= &
          real32_bits(x0%keff)) &
        call fail(trim(label)//' FROZEN-SOURCE EIGENVALUE IS NOT X0 K.')
    enddo
  end subroutine link_restart_to_x0


  subroutine compare_restart_inputs(left,right)
    type(restart_inputs), intent(in) :: left,right
    integer :: plane
    character(len=96) :: label

    do plane=1,expected_planes
      write(label,'(A,I0)') 'RADIAL INPUT PLANE ',plane
      if (left%plane(plane)%nunknown /= right%plane(plane)%nunknown) &
        call fail(trim(label)//' UNKNOWN COUNT DIFFERS.')
      if (any(real32_bits(left%plane(plane)%leakage) /= &
              real32_bits(right%plane(plane)%leakage))) &
        call fail(trim(label)//' SYSTEM LEAKAGE DIFFERS BITWISE.')
      if (real32_bits(left%plane(plane)%source_keff) /= &
          real32_bits(right%plane(plane)%source_keff)) &
        call fail(trim(label)//' SPOT-FS-K DIFFERS BITWISE.')
      if (any(real32_bits(left%plane(plane)%qfiss) /= &
              real32_bits(right%plane(plane)%qfiss))) &
        call fail(trim(label)//' SPOT-QFISS DIFFERS BITWISE.')
    enddo
  end subroutine compare_restart_inputs


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


  subroutine require_directory_item(list_ptr,index,owner)
    type(c_ptr), intent(in) :: list_ptr
    integer, intent(in) :: index
    character(len=*), intent(in) :: owner
    integer :: length_found,type_found

    call LCMLEL(list_ptr,index,length_found,type_found)
    if ((length_found /= -1).or.(type_found /= 0)) &
      call fail(trim(owner)//' LIST ITEM IS NOT A DIRECTORY.')
  end subroutine require_directory_item


  subroutine require_list_item(list_ptr,index,length_expected, &
      type_expected,owner)
    type(c_ptr), intent(in) :: list_ptr
    integer, intent(in) :: index,length_expected,type_expected
    character(len=*), intent(in) :: owner
    integer :: length_found,type_found

    call LCMLEL(list_ptr,index,length_found,type_found)
    if ((length_found /= length_expected).or. &
        (type_found /= type_expected)) then
      write(0,'(A,1X,I0,4(1X,I0))') trim(owner)//' INVALID LIST ITEM', &
        index,length_found,type_found,length_expected,type_expected
      call fail('LIST ITEM CONTRACT FAILURE.')
    endif
  end subroutine require_list_item


  pure function relation(left,right) result(label)
    real(real64), intent(in) :: left,right
    character(len=7) :: label

    if (left < right) then
      label='LESS'
    else if (left > right) then
      label='GREATER'
    else
      label='EQUAL'
    endif
  end function relation


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

    write(0,'(A)') 'INNER-SENSITIVITY-XSM ERROR: '//trim(message)
    error stop 2
  end subroutine fail

end program check_inner_sensitivity_xsm
