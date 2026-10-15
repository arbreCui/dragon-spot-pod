program one_map_mesh_fixture
  ! TEST ONLY: synthetic XSM record-layout fixture, NOT physical map evidence.
  ! No solver, transport, production artifact, or convergence claim is involved.
  ! Run in a fresh temporary directory: fixture MUTATION reencoded|continued.
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32,real32,real64
  implicit none
  integer, parameter :: ng=370,ns=3,nc=ng*ns,coarse=2,fine=4
  character(len=48) :: mutation,route
  integer :: ref_nunk,sys_nunk,prev_nunk,curr_nunk,i
  logical :: continued,exists
  character(len=16), parameter :: files(6)=[character(len=16) :: &
    'basis.xsm','system.xsm','previous.xsm','current.xsm','snapshots.xsm','third.xsm']

  if (command_argument_count() /= 2) error stop 'CASE AND ROUTE REQUIRED.'
  call get_command_argument(1,mutation)
  call get_command_argument(2,route)
  if (route /= 'reencoded'.and.route /= 'continued') error stop 'INVALID ROUTE.'
  continued=(route == 'continued')
  do i=1,size(files)
    inquire(file=trim(files(i)),exist=exists)
    if (exists) error stop 'REFUSING TO OVERWRITE A FIXTURE FILE.'
  enddo
  ref_nunk=coarse
  sys_nunk=fine
  prev_nunk=fine
  curr_nunk=fine
  select case(trim(mutation))
  case('good','no_flux64','basis_bit','state_1','state_40','forged_parent', &
       'directions','previous_flux_length','current_flux_length', &
       'previous_flux_type','current_flux_type','previous_flux_groups','current_flux_groups', &
       'previous_flux_record','current_flux_record','previous_flux_missing','current_flux_missing', &
       'previous_flux64_length','current_flux64_length','previous_flux64_type','current_flux64_type', &
       'previous_flux64_groups','current_flux64_groups','previous_flux64_record','current_flux64_record', &
       'previous_flux64_directory','current_flux64_directory')
  case('same_size')
    ref_nunk=fine
  case('old_parent')
    prev_nunk=coarse
  case('current_mismatch')
    curr_nunk=coarse
  case('system_mismatch')
    sys_nunk=fine+1
  case('reference_zero')
    ref_nunk=0
  case('reference_negative')
    ref_nunk=-1
  case('system_zero')
    sys_nunk=0
  case('system_negative')
    sys_nunk=-1
  case('previous_zero')
    prev_nunk=0
  case('previous_negative')
    prev_nunk=-1
  case('current_zero')
    curr_nunk=0
  case('current_negative')
    curr_nunk=-1
  case default
    error stop 'UNKNOWN FIXTURE MUTATION.'
  end select
  call write_system('basis.xsm',ref_nunk,.false.)
  call write_system('system.xsm',sys_nunk,.true.)
  if (mutation == 'directions') then
    ! Intentionally missing raw fields and incompatible/zero state(2).
    call write_axial('previous.xsm','previous',0,.true.,1.0_real64)
    call write_axial('current.xsm','current',coarse,.true.,2.0_real64)
    call write_axial('third.xsm','third',fine,.true.,4.0_real64)
  else
    call write_axial('previous.xsm','previous',prev_nunk,continued,1.0_real64)
    call write_axial('current.xsm','current',curr_nunk,.true.,1.0_real64)
  endif
  call write_archive()
  write(*,'(A,A)') 'TEST ONLY SYNTHETIC LAYOUT FIXTURE: ',trim(mutation)

contains

  subroutine write_system(path,nunk,current)
    character(len=*), intent(in) :: path
    integer, intent(in) :: nunk
    logical, intent(in) :: current
    type(c_ptr) :: root,groups,item
    integer :: state(40),rank(ng),g
    real(real32) :: basis,radial(ns)
    real(real64) :: sigma(ns,ng)

    call LCMOP(root,path,0,2,0)
    call LCMPTC(root,'SIGNATURE',12,'L_PIJ       ')
    state=0
    state(8)=ng
    state(9)=nunk
    state(14)=1
    if (current.and.mutation == 'state_1') state(1)=1
    if (current.and.mutation == 'state_40') state(40)=1
    call LCMPUT(root,'STATE-VECTOR',40,1,state)
    call LCMPUT(root,'SPOT-FIXB',1,1,merge(1,0,current))
    if (current) then
      call LCMPTC(root,'SPOT-BTYPE',12,'POD-FIXED   ')
      call LCMPTC(root,'LINK.BASIS',12,'TEST BASIS  ')
    else
      call LCMPTC(root,'SPOT-BTYPE',12,'POD-BUILT   ')
    endif
    call LCMPTC(root,'LINK.MACRO',12,'TEST ONLY   ')
    call LCMPTC(root,'LINK.TRACK',12,'TEST ONLY   ')
    call LCMPUT(root,'SPOT-FS-N',1,1,merge(ns,0,current))
    call LCMPUT(root,'SPOT-RBAL',1,4,0.0_real64)
    call LCMPUT(root,'SPOT-Q-L2',1,4,0.0_real64)
    call LCMPUT(root,'SPOT-Q-MAX',1,4,0.0_real64)
    call LCMPUT(root,'SPOT-REM-MIN',1,2,1.0_real32)
    rank=1
    sigma=1.0_real64
    call LCMPUT(root,'POD-RANK-G',ng,1,rank)
    call LCMPUT(root,'POD-SIGMA-G',nc,4,sigma)
    groups=LCMLID(root,'GROUP',ng)
    do g=1,ng
      item=LCMDIL(groups,g)
      call LCMPUT(item,'NREG2D',1,1,1)
      call LCMPUT(item,'NSNAP',1,1,ns)
      call LCMPUT(item,'POD-NMODE',1,1,1)
      call LCMPUT(item,'VOL2D',1,2,1.0_real32)
      basis=1.0_real32
      if (current.and.mutation == 'basis_bit'.and.g == ng) &
        basis=transfer(ieor(transfer(basis,0_int32),1_int32),basis)
      call LCMPUT(item,'POD-BASIS',1,2,basis)
      call LCMPUT(item,'POD-COEFF',ns,2,[1.0_real32,1.0_real32,1.0_real32])
      call LCMPUT(item,'POD-SIGMA',ns,4,sigma(:,g))
      call LCMPUT(item,'POD-REC-ERR',1,4,0.0_real64)
      call LCMPUT(item,'POD-ORTHO',1,4,0.0_real64)
      radial=merge(2.0_real32,1.0_real32,current)
      call LCMPUT(item,'RADIAL-OP',ns,2,radial)
    enddo
    call LCMCL(root,1)
  end subroutine write_system

  subroutine write_axial(path,owner,nunk,saved,value)
    character(len=*), intent(in) :: path,owner
    integer, intent(in) :: nunk
    logical, intent(in) :: saved
    real(real64), intent(in) :: value
    type(c_ptr) :: root
    integer :: state(40),rank(ng),offset(ng+1),unit_offset(ng+1),g
    real(real32) :: basis(ng)
    real(real64) :: coords(nc),gram(ng),height(ns),zero(nc),defect(4)

    call LCMOP(root,path,0,2,0)
    call LCMPTC(root,'SIGNATURE',12,'L_FLUX      ')
    state=0
    state(1)=ng
    state(2)=nunk
    call LCMPUT(root,'STATE-VECTOR',40,1,state)
    call LCMPUT(root,'SPOT-X-DIMS',4,1,[1,ng,ns,nc])
    rank=1
    do g=1,ng+1
      offset(g)=(g-1)*ns
      unit_offset(g)=g-1
    enddo
    basis=1.0_real32
    coords=value
    gram=1.0_real64
    height=1.0_real64
    zero=0.0_real64
    call LCMPUT(root,'SPOT-X-RANK',ng,1,rank)
    call LCMPUT(root,'SPOT-X-OFF',ng+1,1,offset)
    call LCMPUT(root,'SPOT-X-GOFF',ng+1,1,unit_offset)
    call LCMPUT(root,'SPOT-X-BOFF',ng+1,1,unit_offset)
    call LCMPUT(root,'SPOT-X-BASIS',ng,2,basis)
    call LCMPUT(root,'SPOT-X-A',nc,4,coords)
    call LCMPUT(root,'SPOT-X-L',nc,4,coords)
    call LCMPUT(root,'SPOT-X-H',ns,4,height)
    call LCMPUT(root,'SPOT-X-GRAM',ng,4,gram)
    call LCMPUT(root,'K-EFFECTIVE',1,2,1.0_real32)
    call LCMPUT(root,'SPOT-X-RHO',1,4,1.0_real64)
    call LCMPUT(root,'SPOT-X-NORM',1,4,1.0_real64)
    call LCMPUT(root,'SPOT-X-PERP',nc,4,zero)
    call LCMPUT(root,'SPOT-X-GERR',1,4,0.0_real64)
    call LCMPUT(root,'SPOT-X-FIXB',1,1,1)
    call LCMPTC(root,'SPOT-X-NID',12,'NUFISS-UNIT ')
    call LCMPTC(root,'SPOT-X-BTYP',12,'POD-FIXED   ')
    if (saved) then
      defect=0.0_real64
      if (mutation == 'directions'.and.value > 1.0_real64) &
        defect=[0.0_real64,0.5_real64,value/2.0_real64,0.5_real64]
      call LCMPUT(root,'SPOT-X-RRHO',1,4,defect(1))
      call LCMPUT(root,'SPOT-X-RLEAK',1,4,defect(2))
      call LCMPUT(root,'SPOT-X-DLEAK',1,4,defect(3))
      call LCMPUT(root,'SPOT-X-RA',1,4,defect(4))
    endif
    if (mutation /= 'directions') then
      call write_raw_list(root,'FLUX',owner,max(1,nunk),2)
      if (mutation /= 'no_flux64') call write_raw_list(root,'FLUX64',owner,max(1,nunk),4)
    endif
    call LCMCL(root,1)
  end subroutine write_axial

  subroutine write_raw_list(root,name,owner,nunk,kind)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name,owner
    integer, intent(in) :: nunk,kind
    type(c_ptr) :: groups
    integer :: g,count,length0,type0
    character(len=48) :: key
    real(real32) :: field(fine+1)
    real(real64) :: field64(fine+1)

    if (name == 'FLUX') then
      key=trim(owner)//'_flux'
    else
      key=trim(owner)//'_flux64'
    endif
    if (mutation == trim(key)//'_missing') return
    if (mutation == trim(key)//'_record') then
      call LCMPUT(root,name,1,1,1)
      return
    endif
    if (mutation == trim(key)//'_directory') then
      groups=LCMDID(root,name)
      call LCMPUT(groups,'TEST-ONLY',1,1,1)
      return
    endif
    count=ng
    if (mutation == trim(key)//'_groups') count=ng-1
    groups=LCMLID(root,name,count)
    field=1.0_real32
    field64=1.0_real64
    do g=1,count
      length0=nunk
      type0=kind
      if (g == ng.and.mutation == trim(key)//'_length') length0=nunk-1
      if (g == ng.and.mutation == trim(key)//'_type') type0=merge(4,2,kind == 2)
      if (mutation == 'forged_parent'.and.owner == 'previous') length0=coarse
      if (type0 == 2) then
        call LCMPDL(groups,g,length0,2,field(:length0))
      else
        call LCMPDL(groups,g,length0,4,field64(:length0))
      endif
    enddo
  end subroutine write_raw_list

  subroutine write_archive()
    type(c_ptr) :: root,tracks,fluxes,systems,libraries,track,flux,system,groups,item
    integer :: state(40),s,g
    real(real32) :: leak(ng)
    real(real64) :: leak64(ng)

    call LCMOP(root,'snapshots.xsm',0,2,0)
    call LCMPTC(root,'SIGNATURE',12,'L_ARCHIVE   ')
    call LCMPUT(root,'LISTDIM',1,1,ns)
    call LCMPUT(root,'SPOT-ITER-K',1,4,1.0_real64)
    call LCMPUT(root,'SPOT-L1-ERR',1,2,0.0_real32)
    tracks=LCMLID(root,'TRACK',ns)
    fluxes=LCMLID(root,'FLUX',ns)
    systems=LCMLID(root,'SYSTEM',ns)
    libraries=LCMLID(root,'MICROLIB2',ns)
    leak=1.0_real32
    leak64=1.0_real64
    do s=1,ns
      track=LCMDIL(tracks,s)
      state=0
      state(1:2)=1
      call LCMPUT(track,'STATE-VECTOR',40,1,state)
      call LCMPUT(track,'KEYFLX$ANIS',1,1,1)
      flux=LCMDIL(fluxes,s)
      call LCMPTC(flux,'SIGNATURE',12,'L_FLUX      ')
      call LCMPUT(flux,'SPOT-LEAK1D',ng,2,leak)
      call LCMPUT(flux,'LEAK1D64',ng,4,leak64)
      call LCMPUT(flux,'SPOT-FS-EQN',1,1,1)
      call LCMPUT(flux,'SPOT-FS-K',1,2,1.0_real32)
      groups=LCMLID(flux,'FLUX',ng)
      do g=1,ng
        call LCMPDL(groups,g,1,2,[1.0_real32])
      enddo
      system=LCMDIL(systems,s)
      call LCMPTC(system,'SIGNATURE',12,'L_PIJ       ')
      call LCMPUT(system,'SPOT-LEAK1D',ng,2,leak)
      item=LCMDIL(libraries,s)
      call LCMPTC(item,'SIGNATURE',12,'TEST ONLY   ')
    enddo
    call LCMCL(root,1)
  end subroutine write_archive
end program one_map_mesh_fixture
