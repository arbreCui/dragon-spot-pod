program direct_alias_entry_controls
  ! Only three structural entry guards. CLE rejects repeated parameter names
  ! before module dispatch, so this main supplies distinct names and a duplicate
  ! actual c_ptr directly to the same compiled component. No REDGET or transport
  ! call is expected. An unexpected return or another abort must fail the host.
  use GANLIB
  use, intrinsic::iso_c_binding,only:c_null_ptr,c_loc
  use, intrinsic::iso_fortran_env,only:output_unit
  implicit none
  type(c_ptr)::entries(14),opened_producers(3)
  character(len=12)::names(14)
  integer::kinds(14),access(14),n,alias_first,alias_second,i,j,ierr
  integer,target::binary_units(3)
  character(len=32)::mode
  character(len=24)::producer_file,binary_file
  if(command_argument_count()/=1)error stop 'DIRECT-ALIAS-PROBE: EXACT DECLARED MODE REQUIRED.'
  call get_command_argument(1,mode)
  entries=c_null_ptr;opened_producers=c_null_ptr
  names='';kinds=2;access=2
  select case(trim(mode))
  case('pack_original_alias')
    n=7;alias_first=5;alias_second=6
    names(1:7)=[character(len=12)::'PACK','RCON1','RCON2','RCON3','A1','A2_ALIAS','A3']
    access(1:4)=0
    call fresh_xsm(1,'negative_packout.xsm')
    call fresh_xsm(2,'negative_rcon1.xsm')
    call fresh_xsm(3,'negative_rcon2.xsm')
    call fresh_xsm(4,'negative_rcon3.xsm')
    ! All three independently pinned owned copies are really opened read-only.
    ! The second argument intentionally receives A1 instead of the opened A2.
    do i=1,3
      write(producer_file,'(A,I1,A)')'native_A',i,'.xsm'
      call LCMOP(opened_producers(i),trim(producer_file),2,2,0)
    enddo
    entries(5:7)=opened_producers
    entries(6)=entries(5)
  case('initial_contract_alias')
    n=9;alias_first=7;alias_second=8
    names(1:9)=[character(len=12)::'SYSOUT','MACRO','AXTRACK','PACK','BASIS','GRCON','RCON1','RCON2_ALIAS','RCON3']
    access(1)=0
    call fresh_xsm(1,'negative_system.xsm')
    call readonly_xsm(2,'axial_macro.xsm')
    call readonly_xsm(3,'axial_track.xsm')
    call readonly_xsm(4,'initial_pack.xsm')
    call readonly_xsm(5,'basis.xsm')
    call readonly_xsm(6,'global_rcon.xsm')
    call readonly_xsm(7,'plane1_rcon.xsm')
    call readonly_xsm(8,'plane2_rcon.xsm')
    call readonly_xsm(9,'plane3_rcon.xsm')
    entries(8)=entries(7)
  case('view_system_alias')
    n=14;alias_first=9;alias_second=10
    names=[character(len=12)::'AXOUT','ARCOUT','PROJECT','AX','AXTRACK','AXSYSTEM','AXMACRO','GRCON', &
      'SYS1','SYS2_ALIAS','SYS3','TRACK_f1','TRACK_f2','TRACK_f3']
    access(1:2)=0
    call fresh_xsm(1,'negative_ax.xsm')
    call fresh_xsm(2,'negative_archive.xsm')
    call readonly_xsm(3,'projected_boot.xsm')
    call readonly_xsm(4,'ax_current.xsm')
    call readonly_xsm(5,'axial_track.xsm')
    call readonly_xsm(6,'initial_system.xsm')
    call readonly_xsm(7,'axial_macro.xsm')
    call readonly_xsm(8,'global_rcon.xsm')
    ! Empty memory systems are intentionally ONLY early structural placeholders.
    ! The SPOBVX64 alias guard precedes any GLOBAL/SYS/track payload inspection;
    ! they are not ASM-produced systems or a transport qualification.
    kinds(9:11)=1
    call LCMOP(entries(9),'DIRECT_SYS1',0,1,0)
    call LCMOP(entries(10),'DIRECT_SYS2',0,1,0)
    call LCMOP(entries(11),'DIRECT_SYS3',0,1,0)
    entries(10)=entries(9)
    kinds(12:14)=3
    do i=1,3
      write(binary_file,'(A,I1,A)')'radial',i,'.bin'
      open(newunit=binary_units(i),file=trim(binary_file),status='old',action='read', &
        access='sequential',form='unformatted',iostat=ierr)
      if(ierr/=0)error stop 'DIRECT-ALIAS-PROBE: ACTUAL READONLY BINARY TRACK OPEN FAILED.'
      entries(11+i)=c_loc(binary_units(i))
    enddo
  case default
    error stop 'DIRECT-ALIAS-PROBE: UNDECLARED MODE.'
  end select
  ! Prove the intended duplicate pointer with different names; every other
  ! supplied operand pointer/name pair must be independent before actual entry.
  if(.not.c_associated(entries(alias_first),entries(alias_second)).or. &
     names(alias_first)==names(alias_second))error stop 'DIRECT-ALIAS-PROBE: DECLARED ALIAS SETUP FAILED.'
  do i=1,n
    if(.not.c_associated(entries(i)))error stop 'DIRECT-ALIAS-PROBE: NULL SETUP POINTER.'
    do j=1,i-1
      if(names(i)==names(j))error stop 'DIRECT-ALIAS-PROBE: REPEATED SETUP NAME.'
      if(i==alias_second.and.j==alias_first)cycle
      if(c_associated(entries(i),entries(j)))error stop 'DIRECT-ALIAS-PROBE: UNDECLARED SETUP ALIAS.'
    enddo
  enddo
  write(output_unit,'(A)')'ACTUAL-AAA3-DIRECT-ALIAS-CONTROL: '//trim(mode)
  flush(output_unit)
  select case(trim(mode))
  case('pack_original_alias')
    call APACKX64(n,names(1:n),kinds(1:n),access(1:n),entries(1:n))
  case('initial_contract_alias')
    call SPOOPP64(n,names(1:n),kinds(1:n),access(1:n),entries(1:n))
  case('view_system_alias')
    call SPOBVX64(n,names(1:n),kinds(1:n),access(1:n),entries(1:n))
  end select
  error stop 'DIRECT-ALIAS-PROBE: TARGET GUARD RETURNED; UNQUALIFIED.'
contains
  subroutine fresh_xsm(index,filename)
    integer,intent(in)::index
    character(len=*),intent(in)::filename
    logical::exists
    inquire(file=filename,exist=exists)
    if(exists)error stop 'DIRECT-ALIAS-PROBE: PRIVATE OUTPUT ALREADY EXISTS.'
    call LCMOP(entries(index),filename,0,2,0)
  end subroutine fresh_xsm
  subroutine readonly_xsm(index,filename)
    integer,intent(in)::index
    character(len=*),intent(in)::filename
    call LCMOP(entries(index),filename,2,2,0)
  end subroutine readonly_xsm
end program direct_alias_entry_controls
