program build_rank3_basis_xsm
  ! Rebuild rank-two and rank-three POD records from the same frozen raw
  ! snapshots.  Only SPOPOD/ALSVDF is called; no assembly or transport
  ! routine is linked.  The two output XSM files are copies of the locked
  ! rank-two reference prepared by the runner.  With three snapshots,
  ! rank three is full rank: the basis spans the snapshot set exactly and
  ! the out-of-span residual SPOT-X-PERP goes to the arithmetic floor.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32,int64,real32,real64
  implicit none

  integer, parameter :: nstate=40,ngroup=370,nreg=8,nsnap=3
  type(c_ptr) :: snapshots,archive,snapshot_list,reference,control,candidate
  type(c_ptr) :: tracks,fluxes,track_ptr,flux_ptr
  type(c_ptr) :: reference_groups,control_groups,candidate_groups
  type(c_ptr) :: reference_group,control_group,candidate_group
  type(c_ptr) :: flux_lists(nsnap)
  character(len=1024) :: snapshot_path,reference_path
  character(len=1024) :: control_path,candidate_path
  character(len=12) :: signature,basis_type
  character(len=80) :: owner
  integer :: listdim,s,g,r,nmode1,nmode2,max_nunk
  integer :: reference_state(nstate),nunk(nsnap)
  integer :: track_state(nstate),flux_state(nstate)
  integer :: key(nreg,nsnap),material(nreg),rank_root(ngroup)
  real(real32) :: volume(nreg,nsnap),phi(nreg,nsnap)
  real(real32) :: basis1(nreg,nsnap),basis2(nreg,nsnap)
  real(real32) :: coeff1(nsnap,nsnap),coeff2(nsnap,nsnap)
  real(real32) :: packed1(2,nsnap),packed2(3,nsnap)
  real(real32) :: ref_volume(nreg),ref_basis(nreg,2),ref_coeff(2,nsnap)
  real(real32), allocatable :: unknown(:)
  real(real64) :: sigma1(nsnap),sigma2(nsnap),ref_sigma(nsnap)
  real(real64) :: root_sigma(nsnap,ngroup),sigma_root_out(nsnap,ngroup)
  real(real64) :: rec1,rec2,ortho1,ortho2,ref_rec,ref_ortho

  if (command_argument_count() /= 4) call fail( &
    'FOUR ARGUMENTS EXPECTED: SNAPSHOTS REFERENCE CONTROL CANDIDATE.')
  call get_command_argument(1,snapshot_path)
  call get_command_argument(2,reference_path)
  call get_command_argument(3,control_path)
  call get_command_argument(4,candidate_path)
  if ((len_trim(snapshot_path) == 0).or.(len_trim(reference_path) == 0).or. &
      (len_trim(control_path) == 0).or.(len_trim(candidate_path) == 0)) &
    call fail('EMPTY COMMAND-LINE ARGUMENT.')

  call LCMOP(snapshots,trim(snapshot_path),2,2,0)
  call require_record(snapshots,'SIGNATURE',3,3,'SNAPSHOTS')
  call LCMGTC(snapshots,'SIGNATURE',12,signature)
  if (signature /= 'L_ARCHIVE') call fail('DIRECT L_ARCHIVE EXPECTED.')
  call require_record(snapshots,'LISTDIM',1,1,'SNAPSHOTS')
  call LCMGET(snapshots,'LISTDIM',listdim)
  archive=snapshots
  if (listdim == 1) then
    call require_record(snapshots,'SNAP',1,10,'SNAPSHOT WRAPPER')
    snapshot_list=LCMGID(snapshots,'SNAP')
    call require_directory_item(snapshot_list,1,'SNAPSHOT WRAPPER ITEM')
    archive=LCMGIL(snapshot_list,1)
    call require_record(archive,'SIGNATURE',3,3,'INNER SNAPSHOTS')
    call LCMGTC(archive,'SIGNATURE',12,signature)
    if (signature /= 'L_ARCHIVE') &
      call fail('INNER L_ARCHIVE EXPECTED.')
    call require_record(archive,'LISTDIM',1,1,'INNER SNAPSHOTS')
    call LCMGET(archive,'LISTDIM',listdim)
  endif
  if (listdim /= nsnap) call fail('THREE SNAPSHOTS EXPECTED.')
  call require_record(archive,'TRACK',nsnap,10,'SNAPSHOTS')
  call require_record(archive,'MICROLIB2',nsnap,10,'SNAPSHOTS')
  call require_record(archive,'SYSTEM',nsnap,10,'SNAPSHOTS')
  call require_record(archive,'FLUX',nsnap,10,'SNAPSHOTS')
  tracks=LCMGID(archive,'TRACK')
  fluxes=LCMGID(archive,'FLUX')

  max_nunk=0
  do s=1,nsnap
    write(owner,'(A,I0)') 'SNAPSHOT ',s
    call require_directory_item(tracks,s,trim(owner)//' TRACK')
    call require_directory_item(fluxes,s,trim(owner)//' FLUX')
    track_ptr=LCMGIL(tracks,s)
    flux_ptr=LCMGIL(fluxes,s)

    call require_record(track_ptr,'SIGNATURE',3,3,owner)
    call LCMGTC(track_ptr,'SIGNATURE',12,signature)
    if (signature /= 'L_TRACK') call fail(trim(owner)//' L_TRACK EXPECTED.')
    call require_record(track_ptr,'STATE-VECTOR',nstate,1,owner)
    call LCMGET(track_ptr,'STATE-VECTOR',track_state)
    nunk(s)=track_state(2)
    if ((track_state(1) /= nreg).or.(nunk(s) <= 0).or. &
        (track_state(4) <= 0)) call fail(trim(owner)//' INVALID TRACK.')
    call require_record(track_ptr,'MATCOD',nreg,1,owner)
    call require_record(track_ptr,'KEYFLX',nreg,1,owner)
    call require_record(track_ptr,'VOLUME',nreg,2,owner)
    call LCMGET(track_ptr,'MATCOD',material)
    call LCMGET(track_ptr,'KEYFLX',key(:,s))
    call LCMGET(track_ptr,'VOLUME',volume(:,s))
    if (any(material < 0).or.any(material > track_state(4)).or. &
        any(key(:,s) < 0).or.any(key(:,s) > nunk(s)).or. &
        any(.not.ieee_is_finite(volume(:,s))).or. &
        any(volume(:,s) <= 0.0_real32)) &
      call fail(trim(owner)//' INVALID REGION MAP OR VOLUME.')
    call require_unique_keys(key(:,s),owner)
    if ((s > 1).and.any(real32_bits(volume(:,s)) /= &
                         real32_bits(volume(:,1)))) &
      call fail('SNAPSHOT VOLUMES DIFFER BITWISE.')

    call require_record(flux_ptr,'SIGNATURE',3,3,owner)
    call LCMGTC(flux_ptr,'SIGNATURE',12,signature)
    if (signature /= 'L_FLUX') call fail(trim(owner)//' L_FLUX EXPECTED.')
    call require_record(flux_ptr,'STATE-VECTOR',nstate,1,owner)
    call LCMGET(flux_ptr,'STATE-VECTOR',flux_state)
    if ((flux_state(1) /= ngroup).or.(flux_state(2) /= nunk(s))) &
      call fail(trim(owner)//' FLUX/TRACK DIMENSIONS DIFFER.')
    call require_record(flux_ptr,'FLUX',ngroup,10,owner)
    flux_lists(s)=LCMGID(flux_ptr,'FLUX')
    do g=1,ngroup
      call require_list_item(flux_lists(s),g,nunk(s),2,owner)
    enddo
    max_nunk=max(max_nunk,nunk(s))
  enddo
  allocate(unknown(max_nunk))

  call LCMOP(reference,trim(reference_path),2,2,0)
  call require_record(reference,'SIGNATURE',3,3,'REFERENCE')
  call LCMGTC(reference,'SIGNATURE',12,signature)
  if (signature /= 'L_PIJ') call fail('REFERENCE L_PIJ EXPECTED.')
  call require_record(reference,'STATE-VECTOR',nstate,1,'REFERENCE')
  call LCMGET(reference,'STATE-VECTOR',reference_state)
  if ((reference_state(8) /= ngroup).or.(reference_state(9) <= 0).or. &
      (reference_state(14) /= 1)) call fail('INVALID REFERENCE STATE.')
  call require_record(reference,'SPOT-FIXB',1,1,'REFERENCE')
  call LCMGET(reference,'SPOT-FIXB',listdim)
  if (listdim /= 0) call fail('POD-BUILT REFERENCE EXPECTED.')
  call require_record(reference,'SPOT-BTYPE',3,3,'REFERENCE')
  call LCMGTC(reference,'SPOT-BTYPE',12,basis_type)
  if (basis_type /= 'POD-BUILT') call fail('POD-BUILT REFERENCE EXPECTED.')
  call require_record(reference,'POD-RANK-G',ngroup,1,'REFERENCE')
  call require_record(reference,'POD-SIGMA-G',nsnap*ngroup,4,'REFERENCE')
  call require_record(reference,'GROUP',ngroup,10,'REFERENCE')
  call LCMGET(reference,'POD-RANK-G',rank_root)
  call LCMGET(reference,'POD-SIGMA-G',root_sigma)
  if (any(rank_root /= 2)) call fail('REFERENCE IS NOT RANK TWO.')
  if (any(.not.ieee_is_finite(root_sigma)).or.any(root_sigma < 0.0_real64)) &
    call fail('INVALID REFERENCE SPECTRUM.')
  reference_groups=LCMGID(reference,'GROUP')

  call LCMOP(control,trim(control_path),1,2,0)
  call LCMOP(candidate,trim(candidate_path),1,2,0)
  call require_output_preimage(control,reference_state,'CONTROL')
  call require_output_preimage(candidate,reference_state,'CANDIDATE')
  control_groups=LCMGID(control,'GROUP')
  candidate_groups=LCMGID(candidate,'GROUP')

  rank_root=2
  sigma_root_out=0.0_real64
  do g=1,ngroup
    do s=1,nsnap
      call LCMGDL(flux_lists(s),g,unknown)
      if (any(.not.ieee_is_finite(unknown(:nunk(s))))) &
        call fail('NON-FINITE RAW FLUX UNKNOWN.')
      do r=1,nreg
        if (key(r,s) == 0) then
          phi(r,s)=0.0_real32
        else
          phi(r,s)=unknown(key(r,s))
          if (phi(r,s) <= 0.0_real32) &
            call fail('ACTIVE RAW FLUX MUST BE POSITIVE.')
        endif
      enddo
    enddo
    if (any(.not.ieee_is_finite(phi)).or.any(phi < 0.0_real32)) &
      call fail('RAW REGIONAL FLUX MUST BE FINITE AND NONNEGATIVE.')

    call SPOPOD(nreg,nsnap,phi,volume(:,1),2,nmode1,basis1,coeff1, &
      sigma1,rec1,ortho1,0,g)
    call SPOPOD(nreg,nsnap,phi,volume(:,1),3,nmode2,basis2,coeff2, &
      sigma2,rec2,ortho2,0,g)
    if ((nmode1 /= 2).or.(nmode2 /= 3)) &
      call fail('UNEXPECTED PRODUCTION POD MODE COUNT.')
    if (any(real64_bits(sigma1) /= real64_bits(sigma2))) &
      call fail('RANK REQUEST CHANGED THE SINGULAR SPECTRUM.')
    if (any(real32_bits(basis1(:,:2)) /= real32_bits(basis2(:,:2))).or. &
        any(real32_bits(coeff1(:2,:)) /= real32_bits(coeff2(:2,:)))) &
      call fail('RANK-THREE PREFIX DIFFERS FROM FRESH RANK TWO.')

    reference_group=LCMGIL(reference_groups,g)
    call load_reference_group(reference_group,g,ref_volume,ref_basis, &
      ref_coeff,ref_sigma,ref_rec,ref_ortho)
    if (any(real32_bits(ref_volume) /= real32_bits(volume(:,1)))) &
      call fail('RAW/REFERENCE VOLUMES DIFFER BITWISE.')
    if (any(real32_bits(ref_basis) /= real32_bits(basis1(:,:2))).or. &
        any(real32_bits(ref_coeff) /= real32_bits(coeff1(:2,:))).or. &
        any(real64_bits(ref_sigma) /= real64_bits(sigma1)).or. &
        (real64_bits(ref_rec) /= real64_bits(rec1)).or. &
        (real64_bits(ref_ortho) /= real64_bits(ortho1))) &
      call fail('FRESH RANK ONE DOES NOT REPRODUCE THE REFERENCE BITWISE.')

    packed1=coeff1(:2,:)
    packed2=coeff2(:3,:)
    control_group=LCMGIL(control_groups,g)
    candidate_group=LCMGIL(candidate_groups,g)
    call store_group(control_group,2,volume(:,1),basis1(:,:2),packed1, &
      sigma1,rec1,ortho1)
    call store_group(candidate_group,3,volume(:,1),basis2(:,:3),packed2, &
      sigma2,rec2,ortho2)
    sigma_root_out(:,g)=sigma2
  enddo

  call LCMPUT(control,'POD-RANK-G',ngroup,1,rank_root)
  call LCMPUT(control,'POD-SIGMA-G',nsnap*ngroup,4,sigma_root_out)
  listdim=0
  basis_type='POD-BUILT'
  call LCMPUT(control,'SPOT-FIXB',1,1,listdim)
  call LCMPTC(control,'SPOT-BTYPE',12,basis_type)
  rank_root=3
  call LCMPUT(candidate,'POD-RANK-G',ngroup,1,rank_root)
  call LCMPUT(candidate,'POD-SIGMA-G',nsnap*ngroup,4,sigma_root_out)
  call LCMPUT(candidate,'SPOT-FIXB',1,1,listdim)
  call LCMPTC(candidate,'SPOT-BTYPE',12,basis_type)

  call LCMCL(candidate,1)
  call LCMCL(control,1)
  call LCMCL(reference,1)
  call LCMCL(snapshots,1)
  deallocate(unknown)

  write(6,'(A,I0,A,I0,A,I0)') 'RANK3-BUILDER GROUPS=',ngroup, &
    ' REGIONS=',nreg,' SNAPSHOTS=',nsnap
  write(6,'(A)') 'RANK3-BUILDER FRESH-RANK2 BITWISE PASS'
  write(6,'(A)') 'RANK3-BUILDER PREFIX BITWISE PASS'
  write(6,'(A)') 'RANK3-BUILDER COMPLETE'

contains

  subroutine require_output_preimage(ptr,expected_state,label)
    type(c_ptr), intent(in) :: ptr
    integer, intent(in) :: expected_state(nstate)
    character(len=*), intent(in) :: label
    integer :: output_state(nstate)
    character(len=12) :: output_signature
    call require_record(ptr,'SIGNATURE',3,3,label)
    call LCMGTC(ptr,'SIGNATURE',12,output_signature)
    if (output_signature /= 'L_PIJ') call fail(trim(label)//' L_PIJ EXPECTED.')
    call require_record(ptr,'STATE-VECTOR',nstate,1,label)
    call LCMGET(ptr,'STATE-VECTOR',output_state)
    if (any(output_state /= expected_state)) &
      call fail(trim(label)//' STATE DIFFERS FROM REFERENCE.')
    call require_record(ptr,'GROUP',ngroup,10,label)
  end subroutine require_output_preimage

  subroutine load_reference_group(ptr,group,vol,basis,coeff,sigma,rec,ortho)
    type(c_ptr), intent(in) :: ptr
    integer, intent(in) :: group
    real(real32), intent(out) :: vol(nreg),basis(nreg,2),coeff(2,nsnap)
    real(real64), intent(out) :: sigma(nsnap),rec,ortho
    integer :: nreg0,nsnap0,nmode0
    character(len=80) :: label
    write(label,'(A,I0)') 'REFERENCE GROUP ',group
    call require_record(ptr,'NREG2D',1,1,label)
    call require_record(ptr,'NSNAP',1,1,label)
    call require_record(ptr,'POD-NMODE',1,1,label)
    call LCMGET(ptr,'NREG2D',nreg0)
    call LCMGET(ptr,'NSNAP',nsnap0)
    call LCMGET(ptr,'POD-NMODE',nmode0)
    if ((nreg0 /= nreg).or.(nsnap0 /= nsnap).or.(nmode0 /= 2)) &
      call fail(trim(label)//' INVALID DIMENSIONS.')
    call require_record(ptr,'VOL2D',nreg,2,label)
    call require_record(ptr,'POD-BASIS',nreg*2,2,label)
    call require_record(ptr,'POD-COEFF',2*nsnap,2,label)
    call require_record(ptr,'POD-SIGMA',nsnap,4,label)
    call require_record(ptr,'POD-REC-ERR',1,4,label)
    call require_record(ptr,'POD-ORTHO',1,4,label)
    call LCMGET(ptr,'VOL2D',vol)
    call LCMGET(ptr,'POD-BASIS',basis)
    call LCMGET(ptr,'POD-COEFF',coeff)
    call LCMGET(ptr,'POD-SIGMA',sigma)
    call LCMGET(ptr,'POD-REC-ERR',rec)
    call LCMGET(ptr,'POD-ORTHO',ortho)
    if (any(real64_bits(sigma) /= real64_bits(root_sigma(:,group)))) &
      call fail(trim(label)//' ROOT/GROUP SPECTRA DIFFER.')
  end subroutine load_reference_group

  subroutine store_group(ptr,nmode,vol,basis,coeff,sigma,rec,ortho)
    type(c_ptr), intent(in) :: ptr
    integer, intent(in) :: nmode
    real(real32), intent(in) :: vol(nreg),basis(nreg,nmode)
    real(real32), intent(in) :: coeff(nmode,nsnap)
    real(real64), intent(in) :: sigma(nsnap),rec,ortho
    call LCMPUT(ptr,'NREG2D',1,1,nreg)
    call LCMPUT(ptr,'NSNAP',1,1,nsnap)
    call LCMPUT(ptr,'POD-NMODE',1,1,nmode)
    call LCMPUT(ptr,'VOL2D',nreg,2,vol)
    call LCMPUT(ptr,'POD-BASIS',nreg*nmode,2,basis)
    call LCMPUT(ptr,'POD-COEFF',nmode*nsnap,2,coeff)
    call LCMPUT(ptr,'POD-SIGMA',nsnap,4,sigma)
    call LCMPUT(ptr,'POD-REC-ERR',1,4,rec)
    call LCMPUT(ptr,'POD-ORTHO',1,4,ortho)
  end subroutine store_group

  subroutine require_unique_keys(values,label)
    integer, intent(in) :: values(:)
    character(len=*), intent(in) :: label
    integer :: i,j
    do i=1,size(values)
      do j=i+1,size(values)
        if ((values(i) > 0).and.(values(i) == values(j))) &
          call fail(trim(label)//' KEYFLX VALUES ARE NOT UNIQUE.')
      enddo
    enddo
  end subroutine require_unique_keys

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

  subroutine require_list_item(list_ptr,index0,length_expected, &
                               type_expected,label)
    type(c_ptr), intent(in) :: list_ptr
    integer, intent(in) :: index0,length_expected,type_expected
    character(len=*), intent(in) :: label
    integer :: length_actual,type_actual
    call LCMLEL(list_ptr,index0,length_actual,type_actual)
    if ((length_actual /= length_expected).or. &
        (type_actual /= type_expected)) &
      call fail(trim(label)//' INVALID FLUX LIST ITEM.')
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
    write(0,'(A)') 'RANK2-BUILDER ERROR: '//trim(message)
    error stop 2
  end subroutine fail
end program build_rank3_basis_xsm
