program check_rank_census_xsm
  ! Ganlib-only census of the complete singular-value spectra retained by
  ! the frozen rank-1 SPOT basis package. No transport routine is linked.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int64,real64
  implicit none

  integer, parameter :: nstate=40,expected_groups=370
  integer, parameter :: expected_regions=8,expected_snapshots=3
  type(c_ptr) :: root,groups,group_ptr
  character(len=1024) :: path
  character(len=12) :: signature,basis_type
  character(len=64) :: owner
  integer :: state(nstate),fixb
  integer :: length_found,type_found,ngroup,nsnap,g,nreg,nmode
  integer :: rank_count(expected_snapshots),worst1,worst2,worst_stored
  integer, allocatable :: rank_root(:)
  real(real64), allocatable :: sigma(:,:),group_sigma(:)
  real(real64), allocatable :: error1(:),error2(:),sorted1(:),sorted2(:)
  real(real64) :: total,tolerance,stored_error,stored_delta_max
  real(real64) :: median1,median2

  if (command_argument_count() /= 1) &
    call fail('EXPECTED ONE BASIS-REFERENCE XSM PATH.')
  call get_command_argument(1,path)
  if (len_trim(path) == 0) call fail('EMPTY XSM PATH.')

  call LCMOP(root,trim(path),2,2,0)
  call require_record(root,'SIGNATURE',3,3,'ROOT')
  call LCMGTC(root,'SIGNATURE',12,signature)
  if (signature /= 'L_PIJ') call fail('L_PIJ SIGNATURE EXPECTED.')
  call require_record(root,'STATE-VECTOR',nstate,1,'ROOT')
  call LCMGET(root,'STATE-VECTOR',state)
  ngroup=state(8)
  if ((ngroup /= expected_groups).or.(state(14) /= 1)) &
    call fail('UNEXPECTED SPOD STATE DIMENSIONS.')
  call require_record(root,'SPOT-FIXB',1,1,'ROOT')
  call LCMGET(root,'SPOT-FIXB',fixb)
  if (fixb /= 0) call fail('POD-BUILT REFERENCE EXPECTED.')
  call require_record(root,'SPOT-BTYPE',3,3,'ROOT')
  call LCMGTC(root,'SPOT-BTYPE',12,basis_type)
  if (basis_type /= 'POD-BUILT') call fail('POD-BUILT TYPE EXPECTED.')

  call require_record(root,'POD-RANK-G',ngroup,1,'ROOT')
  allocate(rank_root(ngroup))
  call LCMGET(root,'POD-RANK-G',rank_root)
  if (any(rank_root /= 1)) call fail('FROZEN REFERENCE IS NOT RANK ONE.')
  call LCMLEN(root,'POD-SIGMA-G',length_found,type_found)
  if ((type_found /= 4).or.(mod(length_found,ngroup) /= 0)) &
    call fail('INVALID ROOT POD-SIGMA-G RECORD.')
  nsnap=length_found/ngroup
  if (nsnap /= expected_snapshots) &
    call fail('THREE-SNAPSHOT REFERENCE EXPECTED.')
  allocate(sigma(nsnap,ngroup),group_sigma(nsnap))
  allocate(error1(ngroup),error2(ngroup),sorted1(ngroup),sorted2(ngroup))
  call LCMGET(root,'POD-SIGMA-G',sigma)
  if (any(.not.ieee_is_finite(sigma)).or.any(sigma < 0.0_real64)) &
    call fail('INVALID ROOT SINGULAR VALUES.')
  call require_record(root,'GROUP',ngroup,10,'ROOT')
  groups=LCMGID(root,'GROUP')

  rank_count=0
  stored_delta_max=0.0_real64
  worst_stored=0
  do g=1,ngroup
    write(owner,'(A,I0)') 'GROUP ',g
    call require_directory_item(groups,g,owner)
    group_ptr=LCMGIL(groups,g)
    call require_record(group_ptr,'NREG2D',1,1,owner)
    call require_record(group_ptr,'NSNAP',1,1,owner)
    call require_record(group_ptr,'POD-NMODE',1,1,owner)
    call LCMGET(group_ptr,'NREG2D',nreg)
    call LCMGET(group_ptr,'NSNAP',length_found)
    call LCMGET(group_ptr,'POD-NMODE',nmode)
    if ((nreg /= expected_regions).or.(length_found /= nsnap).or. &
        (nmode /= 1)) call fail(trim(owner)//' DIMENSIONS CHANGED.')
    call require_record(group_ptr,'POD-SIGMA',nsnap,4,owner)
    call require_record(group_ptr,'POD-REC-ERR',1,4,owner)
    call LCMGET(group_ptr,'POD-SIGMA',group_sigma)
    call LCMGET(group_ptr,'POD-REC-ERR',stored_error)
    if (any(real64_bits(group_sigma) /= real64_bits(sigma(:,g)))) &
      call fail(trim(owner)//' ROOT/GROUP SPECTRA DIFFER BITWISE.')
    if ((.not.ieee_is_finite(stored_error)).or.(stored_error < 0.0_real64)) &
      call fail(trim(owner)//' INVALID STORED RANK-1 ERROR.')
    if ((sigma(1,g) <= 0.0_real64).or. &
        any(sigma(2:,g) > sigma(:nsnap-1,g))) &
      call fail(trim(owner)//' SPECTRUM IS NOT NONINCREASING.')

    total=sum(sigma(:,g)**2)
    if ((.not.ieee_is_finite(total)).or.(total <= 0.0_real64)) &
      call fail(trim(owner)//' INVALID SPECTRAL NORM.')
    error1(g)=sqrt(sum(sigma(2:,g)**2)/total)
    error2(g)=sigma(3,g)/sqrt(total)
    if (abs(stored_error-error1(g)) > stored_delta_max) then
      stored_delta_max=abs(stored_error-error1(g))
      worst_stored=g
    endif
    tolerance=real(max(nreg,nsnap),real64)*epsilon(1.0_real64)*sigma(1,g)
    nmode=count(sigma(:,g) > tolerance)
    if ((nmode < 1).or.(nmode > nsnap)) &
      call fail(trim(owner)//' INVALID NUMERICAL RANK.')
    rank_count(nmode)=rank_count(nmode)+1
  enddo
  call LCMCL(root,1)

  sorted1=error1
  sorted2=error2
  call insertion_sort(sorted1)
  call insertion_sort(sorted2)
  median1=0.5_real64*(sorted1(ngroup/2)+sorted1(ngroup/2+1))
  median2=0.5_real64*(sorted2(ngroup/2)+sorted2(ngroup/2+1))
  worst1=maxloc(error1,dim=1)
  worst2=maxloc(error2,dim=1)

  write(6,'(A)') 'SPOT-RANK-CENSUS V1'
  write(6,'(A,I0,A,I0,A,I0)') 'DIMENSIONS GROUPS=',ngroup, &
    ' SNAPSHOTS=',nsnap,' REGIONS=',expected_regions
  write(6,'(A,3(I0,1X))') 'NUMERICAL-RANK COUNTS R1/R2/R3 ',rank_count
  call write_metric('R1 ERROR MIN',minval(error1))
  call write_metric('R1 ERROR MEDIAN',median1)
  call write_metric_group('R1 ERROR MAX',error1(worst1),worst1)
  call write_metric('R1 CAPTURED-FRACTION MIN',1.0_real64-error1(worst1)**2)
  call write_spectrum('R1 WORST SPECTRUM',sigma(:,worst1))
  call write_metric('R2 ERROR MIN',minval(error2))
  call write_metric('R2 ERROR MEDIAN',median2)
  call write_metric_group('R2 ERROR MAX',error2(worst2),worst2)
  call write_metric('R2 CAPTURED-FRACTION MIN',1.0_real64-error2(worst2)**2)
  call write_spectrum('R2 WORST SPECTRUM',sigma(:,worst2))
  call write_metric_group('R1 STORED/SPECTRAL MAX ABS DELTA', &
    stored_delta_max,worst_stored)
  write(6,'(A)') 'CLASSIFICATION DIAGNOSTIC_ONLY'
  write(6,'(A)') 'SPOT-RANK-CENSUS COMPLETE'

contains

  subroutine insertion_sort(values)
    real(real64), intent(inout) :: values(:)
    real(real64) :: key
    integer :: i,j
    do i=2,size(values)
      key=values(i)
      j=i-1
      do while (j >= 1)
        if (values(j) <= key) exit
        values(j+1)=values(j)
        j=j-1
      enddo
      values(j+1)=key
    enddo
  end subroutine insertion_sort

  subroutine write_metric(label,value)
    character(len=*), intent(in) :: label
    real(real64), intent(in) :: value
    write(6,'(A,1X,ES25.17E3)') trim(label),value
  end subroutine write_metric

  subroutine write_metric_group(label,value,group)
    character(len=*), intent(in) :: label
    real(real64), intent(in) :: value
    integer, intent(in) :: group
    write(6,'(A,1X,ES25.17E3,1X,A,I0)') trim(label),value,'GROUP=',group
  end subroutine write_metric_group

  subroutine write_spectrum(label,values)
    character(len=*), intent(in) :: label
    real(real64), intent(in) :: values(:)
    write(6,'(A,1X,3(ES25.17E3,1X))') trim(label),values
  end subroutine write_spectrum

  subroutine require_record(ptr,name,length_expected,type_expected,label)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,label
    integer, intent(in) :: length_expected,type_expected
    integer :: length_actual,type_actual
    call LCMLEN(ptr,name,length_actual,type_actual)
    if ((length_actual /= length_expected).or. &
        (type_actual /= type_expected)) &
      call fail(trim(label)//' INVALID RECORD '//trim(name)//'.')
  end subroutine require_record

  subroutine require_directory_item(list_ptr,index0,label)
    type(c_ptr), intent(in) :: list_ptr
    integer, intent(in) :: index0
    character(len=*), intent(in) :: label
    integer :: length_actual,type_actual
    call LCMLEL(list_ptr,index0,length_actual,type_actual)
    if ((length_actual /= -1).or.(type_actual /= 0)) &
      call fail(trim(label)//' IS NOT A DIRECTORY.')
  end subroutine require_directory_item

  pure elemental integer(int64) function real64_bits(value)
    real(real64), intent(in) :: value
    real64_bits=transfer(value,0_int64)
  end function real64_bits

  subroutine fail(message)
    character(len=*), intent(in) :: message
    write(0,'(A)') 'SPOT-RANK-CENSUS ERROR: '//trim(message)
    error stop 2
  end subroutine fail
end program check_rank_census_xsm
