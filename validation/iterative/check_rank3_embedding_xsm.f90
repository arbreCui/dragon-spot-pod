program check_rank3_embedding_xsm
  ! Independently certify an exact nested rank-two -> rank-three state
  ! embedding.  Every input is opened read-only; no transport or assembly is
  ! linked.  The intended map is (a1,a2) -> (a1,a2,+0), with all physical
  ! carrier fields and CLOSED lineage left unchanged.
  use, intrinsic :: iso_c_binding, only : c_associated, c_null_ptr, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use GANLIB
  implicit none

  integer, parameter :: nstate=40,ngrp=370,nsnap=3,nreg=8
  integer, parameter :: rank2=2,rank3=3
  integer, parameter :: expected_reconstructions=ngrp*nsnap*nreg

  type axial_state
    type(c_ptr) :: root=c_null_ptr
    integer :: state(nstate)=0
    integer :: dims(4)=0
    integer, allocatable :: rank(:),offset(:),gram_offset(:),basis_offset(:)
    real(real32), allocatable :: basis(:)
    real(real64), allocatable :: coordinates(:),gram(:),leakage(:)
    real(real64), allocatable :: height(:),offspace(:)
    real(real32) :: keff=0.0_real32
    real(real64) :: keff64=0.0_real64,rho=0.0_real64
    real(real64) :: norm=0.0_real64,gram_error=0.0_real64
    integer :: fixb=0,epoch=-1
    character(len=12) :: lifecycle='',norm_id='',basis_type=''
  end type axial_state

  type rank3_basis
    type(c_ptr) :: root=c_null_ptr
    integer :: state(nstate)=0
    real(real32) :: volume(nreg,ngrp)=0.0_real32
    real(real32) :: basis(nreg,rank3,ngrp)=0.0_real32
  end type rank3_basis

  type(axial_state) :: r2,r3
  type(rank3_basis) :: pod3
  character(len=1024) :: r2ax_path,r2snap_path,r3basis_path,r3ax_path
  integer :: g,s,i,a,index2,index3,bindex2,bindex3,reconstruction_count
  real(real64) :: value2,value3

  if (command_argument_count() /= 4) call fail( &
    'USAGE: check_rank3_embedding_xsm R2_AX R2_SNAP R3_BASIS R3_AX.')
  call get_command_argument(1,r2ax_path)
  call get_command_argument(2,r2snap_path)
  call get_command_argument(3,r3basis_path)
  call get_command_argument(4,r3ax_path)
  if (len_trim(r2ax_path) == 0 .or. len_trim(r2snap_path) == 0 .or. &
      len_trim(r3basis_path) == 0 .or. len_trim(r3ax_path) == 0) &
    call fail('AN INPUT PATH IS EMPTY.')

  call load_axial(trim(r2ax_path),rank2,r2,'RANK2 AX')
  call load_axial(trim(r3ax_path),rank3,r3,'RANK3 AX')
  call load_rank3_basis(trim(r3basis_path),pod3)

  if (any(r2%state /= r3%state)) &
    call fail('AXIAL STATE-VECTOR CHANGED.')
  do g=1,ngrp
    do a=1,rank2
      do i=1,nreg
        bindex2=r2%basis_offset(g)+(a-1)*nreg+i
        bindex3=r3%basis_offset(g)+(a-1)*nreg+i
        if (bits32(r2%basis(bindex2)) /= &
            bits32(pod3%basis(i,a,g))) &
          call fail('RANK3 BASIS PREFIX DIFFERS FROM RANK2 AX.')
        if (bits32(r3%basis(bindex3)) /= &
            bits32(pod3%basis(i,a,g))) &
          call fail('RANK3 AX BASIS PREFIX DIFFERS FROM RANK3 BASIS.')
      enddo
    enddo
    do i=1,nreg
      bindex3=r3%basis_offset(g)+(rank3-1)*nreg+i
      if (bits32(r3%basis(bindex3)) /= &
          bits32(pod3%basis(i,rank3,g))) &
        call fail('RANK3 AX THIRD BASIS MODE DIFFERS FROM RANK3 BASIS.')
    enddo
    do s=1,nsnap
      do a=1,rank2
        index2=r2%offset(g)+(s-1)*rank2+a
        index3=r3%offset(g)+(s-1)*rank3+a
        if (bits64(r2%coordinates(index2)) /= &
            bits64(r3%coordinates(index3))) &
          call fail('RANK3 COORDINATE PREFIX DIFFERS FROM RANK2.')
      enddo
      index3=r3%offset(g)+s*rank3
      if (bits64(r3%coordinates(index3)) /= 0_int64) &
        call fail('RANK3 THIRD COORDINATE IS NOT POSITIVE ZERO.')
    enddo
  enddo
  write(*,'(A)') 'RANK3-EMBED LAYOUT/BASIS PREFIX BITWISE PASS'
  write(*,'(A)') 'RANK3-EMBED COORDINATE PREFIX/MODE3 +0 BITWISE PASS'

  call check_gram(r2,pod3,rank2,'RANK2 AX')
  call check_gram(r3,pod3,rank3,'RANK3 AX')
  write(*,'(A)') 'RANK3-EMBED GRAM/GERR BITWISE PASS'

  reconstruction_count=0
  do g=1,ngrp
    do s=1,nsnap
      do i=1,nreg
        value2=0.0_real64
        do a=1,rank2
          bindex2=r2%basis_offset(g)+(a-1)*nreg+i
          index2=r2%offset(g)+(s-1)*rank2+a
          value2=value2+real(r2%basis(bindex2),real64)* &
            r2%coordinates(index2)
        enddo
        value3=0.0_real64
        do a=1,rank3
          bindex3=r3%basis_offset(g)+(a-1)*nreg+i
          index3=r3%offset(g)+(s-1)*rank3+a
          value3=value3+real(r3%basis(bindex3),real64)* &
            r3%coordinates(index3)
        enddo
        if (.not.ieee_is_finite(value2) .or. value2 <= 0.0_real64) &
          call fail('RANK2 RECONSTRUCTION IS NOT FINITE AND POSITIVE.')
        if (bits64(value2) /= bits64(value3)) &
          call fail('NESTED RECONSTRUCTION CHANGED BITWISE.')
        reconstruction_count=reconstruction_count+1
      enddo
    enddo
  enddo
  if (reconstruction_count /= expected_reconstructions) &
    call fail('RECONSTRUCTION COUNT IS NOT 8880.')
  write(*,'(A,I0)') &
    'RANK3-EMBED RECONSTRUCTION BITWISE PASS COUNT=',reconstruction_count

  call compare_physical_state(r2,r3)
  call compare_flux_carriers(r2,r3)
  call require_absent(r3%root,'SPOT-X-RRHO','RANK3 AX')
  call require_absent(r3%root,'SPOT-X-RLEAK','RANK3 AX')
  call require_absent(r3%root,'SPOT-X-DLEAK','RANK3 AX')
  call require_absent(r3%root,'SPOT-X-RA','RANK3 AX')
  write(*,'(A)') 'RANK3-EMBED PHYSICAL/CARRIER BITWISE PASS'
  write(*,'(A)') 'RANK3-EMBED STALE DEFECTS ABSENT PASS'

  call check_closed_archive(trim(r2snap_path),r2,r3)
  write(*,'(A)') 'RANK3-EMBED CLOSED ARCHIVE EPOCH/RHO PASS'

  call LCMCL(pod3%root,1)
  call LCMCL(r3%root,1)
  call LCMCL(r2%root,1)
  write(*,'(A)') 'RANK3-EMBED COMPLETE'

contains

  subroutine load_axial(path,expected_rank,data,owner)
    character(len=*), intent(in) :: path,owner
    integer, intent(in) :: expected_rank
    type(axial_state), intent(out) :: data
    integer :: expected_coef,expected_gram,expected_basis,g
    character(len=12) :: signature

    call LCMOP(data%root,path,2,2,0)
    call require_character(data%root,'SIGNATURE','L_FLUX',owner)
    call require_record(data%root,'STATE-VECTOR',nstate,1,owner)
    call LCMGET(data%root,'STATE-VECTOR',data%state)
    if (data%state(1) /= ngrp .or. data%state(2) <= 0) &
      call fail(trim(owner)//' INVALID FLUX DIMENSIONS.')

    expected_coef=ngrp*nsnap*expected_rank
    expected_gram=ngrp*expected_rank*expected_rank
    expected_basis=ngrp*nreg*expected_rank
    call require_record(data%root,'SPOT-X-DIMS',4,1,owner)
    call LCMGET(data%root,'SPOT-X-DIMS',data%dims)
    if (any(data%dims /= [1,ngrp,nsnap,expected_coef])) &
      call fail(trim(owner)//' INVALID CANONICAL DIMENSIONS.')

    allocate(data%rank(ngrp),data%offset(ngrp+1))
    allocate(data%gram_offset(ngrp+1),data%basis_offset(ngrp+1))
    call require_record(data%root,'SPOT-X-RANK',ngrp,1,owner)
    call require_record(data%root,'SPOT-X-OFF',ngrp+1,1,owner)
    call require_record(data%root,'SPOT-X-GOFF',ngrp+1,1,owner)
    call require_record(data%root,'SPOT-X-BOFF',ngrp+1,1,owner)
    call LCMGET(data%root,'SPOT-X-RANK',data%rank)
    call LCMGET(data%root,'SPOT-X-OFF',data%offset)
    call LCMGET(data%root,'SPOT-X-GOFF',data%gram_offset)
    call LCMGET(data%root,'SPOT-X-BOFF',data%basis_offset)
    if (any(data%rank /= expected_rank) .or. data%offset(1) /= 0 .or. &
        data%gram_offset(1) /= 0 .or. data%basis_offset(1) /= 0) &
      call fail(trim(owner)//' INVALID CANONICAL LAYOUT.')
    do g=1,ngrp
      if (data%offset(g) /= (g-1)*nsnap*expected_rank .or. &
          data%offset(g+1) /= g*nsnap*expected_rank .or. &
          data%gram_offset(g) /= (g-1)*expected_rank*expected_rank .or. &
          data%gram_offset(g+1) /= g*expected_rank*expected_rank .or. &
          data%basis_offset(g) /= (g-1)*nreg*expected_rank .or. &
          data%basis_offset(g+1) /= g*nreg*expected_rank) &
        call fail(trim(owner)//' OFFSETS ARE NOT CANONICAL.')
    enddo

    allocate(data%basis(expected_basis),data%coordinates(expected_coef))
    allocate(data%gram(expected_gram),data%leakage(ngrp*nsnap))
    allocate(data%height(nsnap),data%offspace(ngrp*nsnap))
    call require_record(data%root,'SPOT-X-BASIS',expected_basis,2,owner)
    call require_record(data%root,'SPOT-X-A',expected_coef,4,owner)
    call require_record(data%root,'SPOT-X-GRAM',expected_gram,4,owner)
    call require_record(data%root,'SPOT-X-L',ngrp*nsnap,4,owner)
    call require_record(data%root,'SPOT-X-H',nsnap,4,owner)
    call require_record(data%root,'SPOT-X-PERP',ngrp*nsnap,4,owner)
    call require_record(data%root,'SPOT-X-GERR',1,4,owner)
    call require_record(data%root,'K-EFFECTIVE',1,2,owner)
    call require_record(data%root,'SPOT-X-KEFF',1,4,owner)
    call require_record(data%root,'SPOT-X-RHO',1,4,owner)
    call require_record(data%root,'SPOT-X-NORM',1,4,owner)
    call require_record(data%root,'SPOT-X-FIXB',1,1,owner)
    call require_character(data%root,'SPOT-X-NID','NUFISS-UNIT',owner)
    call require_character(data%root,'SPOT-X-BTYP','POD-FIXED',owner)
    call require_character(data%root,'SPOT-X-STATE','CLOSED',owner)
    call require_record(data%root,'SPOT-X-EPOCH',1,1,owner)
    call require_absent(data%root,'SPOT-X-CARR',owner)

    call LCMGET(data%root,'SPOT-X-BASIS',data%basis)
    call LCMGET(data%root,'SPOT-X-A',data%coordinates)
    call LCMGET(data%root,'SPOT-X-GRAM',data%gram)
    call LCMGET(data%root,'SPOT-X-L',data%leakage)
    call LCMGET(data%root,'SPOT-X-H',data%height)
    call LCMGET(data%root,'SPOT-X-PERP',data%offspace)
    call LCMGET(data%root,'SPOT-X-GERR',data%gram_error)
    call LCMGET(data%root,'K-EFFECTIVE',data%keff)
    call LCMGET(data%root,'SPOT-X-KEFF',data%keff64)
    call LCMGET(data%root,'SPOT-X-RHO',data%rho)
    call LCMGET(data%root,'SPOT-X-NORM',data%norm)
    call LCMGET(data%root,'SPOT-X-FIXB',data%fixb)
    call LCMGET(data%root,'SPOT-X-EPOCH',data%epoch)
    call LCMGTC(data%root,'SPOT-X-STATE',12,data%lifecycle)
    call LCMGTC(data%root,'SPOT-X-NID',12,data%norm_id)
    call LCMGTC(data%root,'SPOT-X-BTYP',12,data%basis_type)
    call LCMGTC(data%root,'SIGNATURE',12,signature)

    if (signature /= 'L_FLUX' .or. data%fixb /= 1 .or. &
        data%lifecycle /= 'CLOSED' .or. data%norm_id /= 'NUFISS-UNIT' .or. &
        data%basis_type /= 'POD-FIXED' .or. data%epoch < 0) &
      call fail(trim(owner)//' INVALID FIXED CLOSED MARKERS.')
    if (any(.not.ieee_is_finite(data%basis)) .or. &
        any(.not.ieee_is_finite(data%coordinates)) .or. &
        any(.not.ieee_is_finite(data%gram)) .or. &
        any(.not.ieee_is_finite(data%leakage)) .or. &
        any(.not.ieee_is_finite(data%height)) .or. &
        any(data%height <= 0.0_real64) .or. &
        any(.not.ieee_is_finite(data%offspace)) .or. &
        any(data%offspace < 0.0_real64) .or. &
        .not.ieee_is_finite(data%gram_error) .or. &
        data%gram_error < 0.0_real64 .or. &
        .not.ieee_is_finite(data%keff) .or. data%keff <= 0.0_real32 .or. &
        .not.ieee_is_finite(data%keff64) .or. data%keff64 <= 0.0_real64 .or. &
        .not.ieee_is_finite(data%rho) .or. data%rho <= 0.0_real64 .or. &
        .not.ieee_is_finite(data%norm) .or. data%norm <= 0.0_real64) &
      call fail(trim(owner)//' INVALID OR NON-FINITE CANONICAL FIELD.')
    if (bits32(data%keff) /= bits32(real(data%keff64,real32))) &
      call fail(trim(owner)//' REAL64/REAL32 KEFF MIRROR DIFFERS.')
    if (bits64(data%rho) /= bits64(1.0_real64/data%keff64)) &
      call fail(trim(owner)//' RHO IS NOT THE REAL64 INVERSE KEFF.')
  end subroutine load_axial


  subroutine load_rank3_basis(path,data)
    character(len=*), intent(in) :: path
    type(rank3_basis), intent(out) :: data
    type(c_ptr) :: groups,group
    integer :: ranks(ngrp),g,nreg_found,nsnap_found,nmode_found,fixb

    call LCMOP(data%root,path,2,2,0)
    call require_character(data%root,'SIGNATURE','L_PIJ','RANK3 BASIS')
    call require_record(data%root,'STATE-VECTOR',nstate,1,'RANK3 BASIS')
    call LCMGET(data%root,'STATE-VECTOR',data%state)
    if (data%state(8) /= ngrp .or. data%state(14) /= 1) &
      call fail('RANK3 BASIS INVALID SPOD STATE-VECTOR.')
    call require_record(data%root,'SPOT-FIXB',1,1,'RANK3 BASIS')
    call LCMGET(data%root,'SPOT-FIXB',fixb)
    if (fixb /= 0) call fail('RANK3 BASIS IS NOT POD-BUILT.')
    call require_character(data%root,'SPOT-BTYPE','POD-BUILT','RANK3 BASIS')
    call require_record(data%root,'POD-RANK-G',ngrp,1,'RANK3 BASIS')
    call LCMGET(data%root,'POD-RANK-G',ranks)
    if (any(ranks /= rank3)) call fail('RANK3 BASIS ROOT RANK IS NOT THREE.')
    call require_record(data%root,'GROUP',ngrp,10,'RANK3 BASIS')
    groups=LCMGID(data%root,'GROUP')
    if (.not.c_associated(groups)) call fail('RANK3 BASIS GROUP LIST IS NULL.')
    do g=1,ngrp
      call require_directory_item(groups,g,'RANK3 BASIS GROUP')
      group=LCMGIL(groups,g)
      if (.not.c_associated(group)) call fail('RANK3 BASIS GROUP IS NULL.')
      call require_record(group,'NREG2D',1,1,'RANK3 BASIS GROUP')
      call require_record(group,'NSNAP',1,1,'RANK3 BASIS GROUP')
      call require_record(group,'POD-NMODE',1,1,'RANK3 BASIS GROUP')
      call LCMGET(group,'NREG2D',nreg_found)
      call LCMGET(group,'NSNAP',nsnap_found)
      call LCMGET(group,'POD-NMODE',nmode_found)
      if (nreg_found /= nreg .or. nsnap_found /= nsnap .or. &
          nmode_found /= rank3) &
        call fail('RANK3 BASIS GROUP DIMENSIONS ARE INVALID.')
      call require_record(group,'VOL2D',nreg,2,'RANK3 BASIS GROUP')
      call require_record(group,'POD-BASIS',nreg*rank3,2, &
        'RANK3 BASIS GROUP')
      call LCMGET(group,'VOL2D',data%volume(:,g))
      call LCMGET(group,'POD-BASIS',data%basis(:,:,g))
      if (any(.not.ieee_is_finite(data%volume(:,g))) .or. &
          any(data%volume(:,g) <= 0.0_real32) .or. &
          any(.not.ieee_is_finite(data%basis(:,:,g)))) &
        call fail('RANK3 BASIS GROUP HAS INVALID NUMERICAL DATA.')
    enddo
  end subroutine load_rank3_basis


  subroutine check_gram(ax,pod,mode_count,owner)
    type(axial_state), intent(in) :: ax
    type(rank3_basis), intent(in) :: pod
    integer, intent(in) :: mode_count
    character(len=*), intent(in) :: owner
    integer :: g,a,b,i,index_g
    real(real64) :: weight_sum,gram_value,gram_error

    gram_error=0.0_real64
    do g=1,ngrp
      weight_sum=sum(real(pod%volume(:,g),real64))
      if (.not.ieee_is_finite(weight_sum) .or. weight_sum <= 0.0_real64) &
        call fail(trim(owner)//' INVALID BASIS WEIGHT SUM.')
      do a=1,mode_count
        do b=1,mode_count
          gram_value=0.0_real64
          do i=1,nreg
            gram_value=gram_value+real(pod%volume(i,g),real64)/weight_sum* &
              real(pod%basis(i,a,g),real64)* &
              real(pod%basis(i,b,g),real64)
          enddo
          index_g=ax%gram_offset(g)+(b-1)*mode_count+a
          if (bits64(gram_value) /= bits64(ax%gram(index_g))) &
            call fail(trim(owner)//' GRAM RECOMPUTE DIFFERS BITWISE.')
          if (a == b) then
            gram_error=max(gram_error,abs(gram_value-1.0_real64))
          else
            gram_error=max(gram_error,abs(gram_value))
          endif
        enddo
      enddo
    enddo
    if (bits64(gram_error) /= bits64(ax%gram_error)) &
      call fail(trim(owner)//' GERR RECOMPUTE DIFFERS BITWISE.')
  end subroutine check_gram


  subroutine compare_physical_state(left,right)
    type(axial_state), intent(in) :: left,right

    if (bits32(left%keff) /= bits32(right%keff) .or. &
        bits64(left%keff64) /= bits64(right%keff64) .or. &
        bits64(left%rho) /= bits64(right%rho) .or. &
        bits64(left%norm) /= bits64(right%norm) .or. &
        any(bits64(left%leakage) /= bits64(right%leakage)) .or. &
        any(bits64(left%height) /= bits64(right%height)) .or. &
        any(bits64(left%offspace) /= bits64(right%offspace))) &
      call fail('RANK3 EMBEDDING CHANGED K/RHO/L/H/NORM/PERP.')
    if (left%fixb /= right%fixb .or. &
        left%norm_id /= right%norm_id .or. &
        left%basis_type /= right%basis_type .or. &
        left%lifecycle /= right%lifecycle .or. &
        left%epoch /= right%epoch) &
      call fail('RANK3 EMBEDDING CHANGED FIXED-SPACE OR LIFECYCLE MARKERS.')
    call compare_optional_real64(left%root,right%root,'SPOT-KEFF64', &
      'AXIAL SPOT-KEFF64')
  end subroutine compare_physical_state


  subroutine compare_flux_carriers(left,right)
    type(axial_state), intent(in) :: left,right
    type(c_ptr) :: flux_left,flux_right,flux64_left,flux64_right
    real(real32), allocatable :: values32_left(:),values32_right(:)
    real(real64), allocatable :: values64_left(:),values64_right(:)
    integer :: g,nunk,length_left,type_left,length_right,type_right

    nunk=left%state(2)
    if (right%state(2) /= nunk) call fail('AXIAL UNKNOWN COUNT CHANGED.')
    call require_record(left%root,'FLUX',ngrp,10,'RANK2 AX')
    call require_record(right%root,'FLUX',ngrp,10,'RANK3 AX')
    call require_record(left%root,'FLUX64',ngrp,10,'RANK2 AX')
    call require_record(right%root,'FLUX64',ngrp,10,'RANK3 AX')
    flux_left=LCMGID(left%root,'FLUX')
    flux_right=LCMGID(right%root,'FLUX')
    flux64_left=LCMGID(left%root,'FLUX64')
    flux64_right=LCMGID(right%root,'FLUX64')
    if (.not.c_associated(flux_left) .or. .not.c_associated(flux_right) .or. &
        .not.c_associated(flux64_left) .or. &
        .not.c_associated(flux64_right)) &
      call fail('AXIAL FLUX LIST IS NULL.')
    allocate(values32_left(nunk),values32_right(nunk))
    allocate(values64_left(nunk),values64_right(nunk))
    do g=1,ngrp
      call LCMLEL(flux_left,g,length_left,type_left)
      call LCMLEL(flux_right,g,length_right,type_right)
      if (length_left /= nunk .or. type_left /= 2 .or. &
          length_right /= nunk .or. type_right /= 2) &
        call fail('INVALID AXIAL FLUX ITEM.')
      call LCMGDL(flux_left,g,values32_left)
      call LCMGDL(flux_right,g,values32_right)
      if (any(bits32(values32_left) /= bits32(values32_right))) &
        call fail('UNDERLYING REAL32 AXIAL FLUX CHANGED BITWISE.')

      call LCMLEL(flux64_left,g,length_left,type_left)
      call LCMLEL(flux64_right,g,length_right,type_right)
      if (length_left /= nunk .or. type_left /= 4 .or. &
          length_right /= nunk .or. type_right /= 4) &
        call fail('INVALID AXIAL FLUX64 ITEM.')
      call LCMGDL(flux64_left,g,values64_left)
      call LCMGDL(flux64_right,g,values64_right)
      if (any(bits64(values64_left) /= bits64(values64_right))) &
        call fail('UNDERLYING REAL64 AXIAL FLUX CHANGED BITWISE.')
    enddo
    deallocate(values64_right,values64_left,values32_right,values32_left)
  end subroutine compare_flux_carriers


  subroutine check_closed_archive(path,r2ax,r3ax)
    character(len=*), intent(in) :: path
    type(axial_state), intent(in) :: r2ax,r3ax
    type(c_ptr) :: archive,authority,fluxes,plane,plane_authority
    integer :: listdim,nplane,epoch,plane_epoch,s,g
    real(real32) :: leakage32(ngrp)
    real(real64) :: rho,plane_rho,iter_keff

    call LCMOP(archive,path,2,2,0)
    call require_character(archive,'SIGNATURE','L_ARCHIVE','RANK2 SNAP')
    call require_record(archive,'LISTDIM',1,1,'RANK2 SNAP')
    call LCMGET(archive,'LISTDIM',listdim)
    if (listdim /= nsnap) call fail('RANK2 SNAP LISTDIM IS NOT THREE.')
    call require_record(archive,'SPOT-ITER-K',1,4,'RANK2 SNAP')
    call LCMGET(archive,'SPOT-ITER-K',iter_keff)
    if (bits64(iter_keff) /= bits64(r3ax%keff64)) &
      call fail('RANK2 SNAP ITERATION KEFF DIFFERS FROM RANK3 AX.')
    call require_record(archive,'SPOT-R64',-1,0,'RANK2 SNAP')
    authority=LCMGID(archive,'SPOT-R64')
    if (.not.c_associated(authority)) call fail('RANK2 SNAP AUTHORITY IS NULL.')
    call require_character(authority,'STATE','CLOSED','RANK2 SNAP AUTHORITY')
    call require_record(authority,'EPOCH',1,1,'RANK2 SNAP AUTHORITY')
    call require_record(authority,'RHO',1,4,'RANK2 SNAP AUTHORITY')
    call require_record(authority,'NPLANE',1,1,'RANK2 SNAP AUTHORITY')
    call LCMGET(authority,'EPOCH',epoch)
    call LCMGET(authority,'RHO',rho)
    call LCMGET(authority,'NPLANE',nplane)
    if (epoch /= r2ax%epoch .or. epoch /= r3ax%epoch .or. nplane /= nsnap) &
      call fail('RANK2 SNAP CLOSED LINEAGE DOES NOT MATCH BOTH AX STATES.')
    if (bits64(rho) /= bits64(r2ax%rho) .or. &
        bits64(rho) /= bits64(r3ax%rho)) &
      call fail('RANK2 SNAP CLOSED RHO DOES NOT MATCH BOTH AX STATES.')

    call require_record(archive,'FLUX',nsnap,10,'RANK2 SNAP')
    fluxes=LCMGID(archive,'FLUX')
    if (.not.c_associated(fluxes)) call fail('RANK2 SNAP FLUX LIST IS NULL.')
    do s=1,nsnap
      call require_directory_item(fluxes,s,'RANK2 SNAP FLUX')
      plane=LCMGIL(fluxes,s)
      if (.not.c_associated(plane)) call fail('RANK2 SNAP PLANE IS NULL.')
      call require_record(plane,'SPOT-R64',-1,0,'RANK2 SNAP PLANE')
      plane_authority=LCMGID(plane,'SPOT-R64')
      if (.not.c_associated(plane_authority)) &
        call fail('RANK2 SNAP PLANE AUTHORITY IS NULL.')
      call require_character(plane_authority,'STATE','SOLVED', &
        'RANK2 SNAP PLANE AUTHORITY')
      call require_record(plane_authority,'EPOCH',1,1, &
        'RANK2 SNAP PLANE AUTHORITY')
      call require_record(plane_authority,'RHO',1,4, &
        'RANK2 SNAP PLANE AUTHORITY')
      call LCMGET(plane_authority,'EPOCH',plane_epoch)
      call LCMGET(plane_authority,'RHO',plane_rho)
      if (plane_epoch /= epoch .or. bits64(plane_rho) /= bits64(rho)) &
        call fail('RANK2 SNAP PLANE LINEAGE DIFFERS FROM CLOSED ROOT.')
      call require_record(plane,'SPOT-LEAK1D',ngrp,2,'RANK2 SNAP PLANE')
      call LCMGET(plane,'SPOT-LEAK1D',leakage32)
      do g=1,ngrp
        if (bits32(leakage32(g)) /= &
            bits32(real(r3ax%leakage((s-1)*ngrp+g),real32))) &
          call fail('RANK2 SNAP LEAKAGE MIRROR DIFFERS FROM RANK3 AX.')
      enddo
    enddo
    call LCMCL(archive,1)
  end subroutine check_closed_archive


  subroutine compare_optional_real64(left,right,name,owner)
    type(c_ptr), intent(in) :: left,right
    character(len=*), intent(in) :: name,owner
    integer :: left_length,left_type,right_length,right_type
    real(real64) :: left_value,right_value

    call LCMLEN(left,name,left_length,left_type)
    call LCMLEN(right,name,right_length,right_type)
    if (left_length /= right_length .or. left_type /= right_type) &
      call fail(trim(owner)//' PRESENCE OR TYPE CHANGED.')
    if (left_length == 0) return
    if (left_length /= 1 .or. left_type /= 4) &
      call fail(trim(owner)//' HAS INVALID RECORD SHAPE.')
    call LCMGET(left,name,left_value)
    call LCMGET(right,name,right_value)
    if (bits64(left_value) /= bits64(right_value)) &
      call fail(trim(owner)//' CHANGED BITWISE.')
  end subroutine compare_optional_real64


  subroutine require_record(root,name,expected_length,expected_type,owner)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name,owner
    integer, intent(in) :: expected_length,expected_type
    integer :: length_found,type_found

    call LCMLEN(root,name,length_found,type_found)
    if (length_found /= expected_length .or. type_found /= expected_type) &
      call fail(trim(owner)//' INVALID RECORD '//trim(name)//'.')
  end subroutine require_record


  subroutine require_character(root,name,expected,owner)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name,expected,owner
    character(len=12) :: found

    call require_record(root,name,3,3,owner)
    call LCMGTC(root,name,12,found)
    if (found /= expected) &
      call fail(trim(owner)//' INVALID CHARACTER RECORD '//trim(name)//'.')
  end subroutine require_character


  subroutine require_absent(root,name,owner)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name,owner
    integer :: length_found,type_found

    call LCMLEN(root,name,length_found,type_found)
    if (length_found /= 0) &
      call fail(trim(owner)//' STALE RECORD IS PRESENT: '//trim(name)//'.')
  end subroutine require_absent


  subroutine require_directory_item(list,index0,owner)
    type(c_ptr), intent(in) :: list
    integer, intent(in) :: index0
    character(len=*), intent(in) :: owner
    integer :: length_found,type_found

    call LCMLEL(list,index0,length_found,type_found)
    if (length_found /= -1 .or. type_found /= 0) &
      call fail(trim(owner)//' ITEM IS NOT A DIRECTORY.')
  end subroutine require_directory_item


  pure elemental integer(int32) function bits32(value)
    real(real32), intent(in) :: value
    bits32=transfer(value,0_int32)
  end function bits32


  pure elemental integer(int64) function bits64(value)
    real(real64), intent(in) :: value
    bits64=transfer(value,0_int64)
  end function bits64


  subroutine fail(message)
    character(len=*), intent(in) :: message
    write(0,'(A)') 'RANK3-EMBED CHECK ERROR: '//trim(message)
    error stop 2
  end subroutine fail

end program check_rank3_embedding_xsm
