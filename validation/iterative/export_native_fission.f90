program export_native_fission
  ! Read-only recovery of the original plane-1 fission operator. No solve.
  use GANLIB
  use, intrinsic :: iso_fortran_env, only: real32,int32,error_unit
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  integer,parameter :: nm=8,ng=370,nfis=32
  type(c_ptr) :: root,archive,outer,libraries,library,macro,frozen,groups,frozen_groups,item,zero_item
  integer :: state(40),g,j,m,out,ios,planes,records
  real(real32) :: nuf(nm,nfis,ng),chi(nm,nfis,ng),zero(nm,nfis)
  character(len=12),parameter :: names(9)=[character(len=12) :: &
    'NTOT0','SIGW00','SIGS00','TRANC','CHI','SCAT00','NJJS00','IJJS00','IPOS00']
  character(len=1024) :: output_path
  logical :: exists
  if(command_argument_count()/=1) call fail('usage: export_native_fission NEW_OUTPUT')
  call get_command_argument(1,output_path)
  inquire(file=trim(output_path),exist=exists)
  if(exists) call fail('output exists')
  call LCMOP(root,'snapshots.xsm',2,2,0)
  call LCMOP(frozen,'macro0.xsm',2,2,0)
  ! The historical seed wraps one L_ARCHIVE in the outer SNAP list.
  call record(root,'SNAP',1,10);outer=LCMGID(root,'SNAP');archive=LCMGIL(outer,1)
  call record(archive,'LISTDIM',1,1);call LCMGET(archive,'LISTDIM',planes)
  if(planes<1) call fail('empty snapshot archive')
  call record(archive,'MICROLIB2',planes,10);libraries=LCMGID(archive,'MICROLIB2')
  library=LCMGIL(libraries,1);macro=LCMGID(library,'MACROLIB')
  call record(macro,'STATE-VECTOR',40,1);call LCMGET(macro,'STATE-VECTOR',state)
  if(state(1)/=ng.or.state(2)/=nm.or.state(4)/=nfis) call fail('original macro dimensions')
  call record(macro,'GROUP',ng,10);groups=LCMGID(macro,'GROUP')
  call record(frozen,'GROUP',ng,10);frozen_groups=LCMGID(frozen,'GROUP')
  records=0
  do g=1,ng
    item=LCMGIL(groups,g);zero_item=LCMGIL(frozen_groups,g)
    do j=1,size(names)
      call equal_record(item,zero_item,trim(names(j)))
      records=records+1
    enddo
    call record(item,'NUSIGF',nm*nfis,2);call LCMGET(item,'NUSIGF',nuf(:,:,g))
    call record(item,'CHI',nm*nfis,2);call LCMGET(item,'CHI',chi(:,:,g))
    call record(zero_item,'NUSIGF',nm*nfis,2);call LCMGET(zero_item,'NUSIGF',zero)
    if(any(zero/=0)) call fail('MACRO0 has live fission')
  enddo
  if(.not.all(ieee_is_finite(nuf)).or..not.all(ieee_is_finite(chi))) call fail('nonfinite fission data')
  if(any(nuf<0).or.any(chi<0).or.maxval(nuf)<=0) call fail('invalid fission data')
  open(newunit=out,file=trim(output_path),status='new',access='stream',form='unformatted',iostat=ios)
  if(ios/=0) call fail('cannot create export')
  write(out) nm,ng,nfis,planes,records
  write(out) nuf,chi
  close(out)
  call LCMCL(frozen,1);call LCMCL(root,1)
  write(*,'(A,I0)') 'FISSION-RECOVERY MATCHED P0/CHI RECORDS=',records
  do m=1,nm
    write(*,'(A,I0,A,I0)') 'MATERIAL ',m,' ACTIVE FISSION COMPONENTS=',count(maxval(nuf(m,:,:),dim=2)>0)
  enddo
contains
  subroutine fail(message)
    character(len=*),intent(in) :: message
    write(error_unit,'(A)') 'FISSION-RECOVERY ERROR: '//message
    error stop 1
  end subroutine
  subroutine record(ptr,name,length,kind)
    type(c_ptr),intent(in) :: ptr
    character(len=*),intent(in) :: name
    integer,intent(in) :: length,kind
    integer :: l,k
    call LCMLEN(ptr,name,l,k)
    if(l/=length.or.k/=kind) call fail('record mismatch: '//name)
  end subroutine
  subroutine equal_record(left,right,name)
    type(c_ptr),intent(in) :: left,right
    character(len=*),intent(in) :: name
    integer :: n1,n2,t1,t2
    integer(int32),allocatable :: i1(:),i2(:)
    real(real32),allocatable :: r1(:),r2(:)
    call LCMLEN(left,name,n1,t1);call LCMLEN(right,name,n2,t2)
    if(n1/=n2.or.t1/=t2.or.n1<=0) call fail('record extent mismatch: '//name)
    if(t1==1) then
      allocate(i1(n1),i2(n1));call LCMGET(left,name,i1);call LCMGET(right,name,i2)
      if(any(i1/=i2)) call fail('integer record changed: '//name)
    else if(t1==2) then
      allocate(r1(n1),r2(n1));call LCMGET(left,name,r1);call LCMGET(right,name,r2)
      if(any(transfer(r1,[0_int32],n1)/=transfer(r2,[0_int32],n1))) call fail('real record changed: '//name)
    else
      call fail('unsupported comparison type: '//name)
    endif
  end subroutine
end program
