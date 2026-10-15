! Non-scientific GNU Fortran startup / libc read-only FD contract control.
program readonly_fd_native_startup_control
 use, intrinsic :: iso_c_binding
 implicit none
 interface
  function c_getpid() bind(C,name="getpid") result(v)
   import c_int
   integer(c_int)::v
  end function
  function c_getpgrp() bind(C,name="getpgrp") result(v)
   import c_int
   integer(c_int)::v
  end function
  function c_fcntl(fd,cmd) bind(C,name="fcntl") result(v)
   import c_int
   integer(c_int),value::fd,cmd
   integer(c_int)::v
  end function
  function c_fopen(name,mode) bind(C,name="fopen") result(p)
   import c_char,c_ptr
   character(kind=c_char),intent(in)::name(*),mode(*)
   type(c_ptr)::p
  end function
  function c_fread(ptr,size,n,stream) bind(C,name="fread") result(v)
   import c_ptr,c_size_t
   type(c_ptr),value::ptr,stream
   integer(c_size_t),value::size,n
   integer(c_size_t)::v
  end function
  function c_fseek(stream,offset,whence) bind(C,name="fseek") result(v)
   import c_ptr,c_long,c_int
   type(c_ptr),value::stream
   integer(c_long),value::offset
   integer(c_int),value::whence
   integer(c_int)::v
  end function
  function c_fileno(stream) bind(C,name="fileno") result(v)
   import c_ptr,c_int
   type(c_ptr),value::stream
   integer(c_int)::v
  end function
  function c_fclose(stream) bind(C,name="fclose") result(v)
   import c_ptr,c_int
   type(c_ptr),value::stream
   integer(c_int)::v
  end function
  function c_write(fd,buffer,n) bind(C,name="write") result(v)
   import c_int,c_ptr,c_size_t,c_long
   integer(c_int),value::fd
   type(c_ptr),value::buffer
   integer(c_size_t),value::n
   integer(c_long)::v
  end function
  function c_error() bind(C,name="__error") result(v)
   import c_ptr
   type(c_ptr)::v
  end function
  subroutine c_exit(code) bind(C,name="exit")
   import c_int
   integer(c_int),value::code
  end subroutine
 end interface
 integer(c_int),parameter::F_GETFL=3_c_int,O_ACCMODE=3_c_int,O_RDONLY=0_c_int
 integer(c_int),parameter::fixed_fds(3)=[101,102,103]
 integer,parameter::lengths(3)=[257,521,1031]
 character(kind=c_char),target::buf(2048),one(1)
 character(kind=c_char,len=:),allocatable::name,mode
 character(len=64)::arg,number
 integer(c_int),pointer::err
 type(c_ptr)::stream
 integer(c_int)::pid,grp,expected_pid,expected_grp,flags,fd,rc
 integer(c_size_t)::got
 integer(c_long)::wrote
 integer::i,j,total,ios
 call get_command_argument(1,arg);read(arg,*,iostat=ios)expected_pid
 call require(ios==0,70,'EXPECTED_PID_ARGUMENT')
 call get_command_argument(2,arg);read(arg,*,iostat=ios)expected_grp
 call require(ios==0,70,'EXPECTED_GROUP_ARGUMENT')
 call require(command_argument_count()==2,70,'EXACT_TWO_ID_ARGUMENTS')
 pid=c_getpid();grp=c_getpgrp()
 call require(pid==expected_pid.and.grp==expected_grp.and.pid==grp,70,'SAME_PID_GROUP_AFTER_GNU_STARTUP')
 call c_f_pointer(c_error(),err);mode='rb'//c_null_char;total=0;one(1)='!'
 do i=1,3
  flags=c_fcntl(fixed_fds(i),F_GETFL)
  call require(flags>=0,71,'INHERITED_FD_PRESENT')
  call require(iand(flags,O_ACCMODE)==O_RDONLY,72,'INHERITED_FD_READONLY')
  write(number,'(I0)')fixed_fds(i);name='/dev/fd/'//trim(number)//c_null_char
  stream=c_fopen(name,mode)
  call require(c_associated(stream),73,'LIBC_DEV_FD_REOPEN_RB')
  fd=c_fileno(stream);flags=c_fcntl(fd,F_GETFL)
  call require(fd>=0.and.flags>=0.and.iand(flags,O_ACCMODE)==O_RDONLY,74,'REOPENED_FD_READONLY')
  got=c_fread(c_loc(buf(1)),1_c_size_t,int(lengths(i),c_size_t),stream)
  call require(got==int(lengths(i),c_size_t),75,'FULL_FIXTURE_READ')
  do j=1,lengths(i)
   call require(iachar(buf(j))==65+mod(i*19+(j-1)*7,26),75,'COMPLETE_FIXTURE_BYTES')
  enddo
  got=c_fread(c_loc(buf(1)),1_c_size_t,1_c_size_t,stream)
  call require(got==0_c_size_t,75,'COMPLETE_FIXTURE_EOF')
  rc=c_fseek(stream,17_c_long,0_c_int);call require(rc==0,76,'SEEK_SET_AFTER_EOF')
  got=c_fread(c_loc(buf(1)),1_c_size_t,31_c_size_t,stream)
  call require(got==31_c_size_t,76,'SEEK_READ_LENGTH')
  do j=1,31
   call require(iachar(buf(j))==65+mod(i*19+(j+16)*7,26),76,'SEEKED_FIXTURE_BYTES')
  enddo
  rc=c_fseek(stream,0_c_long,0_c_int);call require(rc==0,76,'REWIND')
  got=c_fread(c_loc(buf(1)),1_c_size_t,17_c_size_t,stream)
  call require(got==17_c_size_t,76,'PREFIX_READ')
  do j=1,17
   call require(iachar(buf(j))==65+mod(i*19+(j-1)*7,26),76,'REWOUND_FIXTURE_BYTES')
  enddo
  err=0;wrote=c_write(fixed_fds(i),c_loc(one(1)),1_c_size_t)
  call require(wrote==-1_c_long.and.err==9,77,'KERNEL_READONLY_WRITE_EBADF')
  rc=c_fclose(stream);call require(rc==0,78,'CLOSE_REOPENED_STREAM_KEEP_ORIGINAL')
  flags=c_fcntl(fixed_fds(i),F_GETFL);call require(flags>=0,78,'ORIGINAL_INHERITED_FD_REMAINS_PRESENT')
  total=total+lengths(i)
 enddo
 write(*,'(A,4(1X,I0))')'FD_NATIVE_PID_GROUP_BYTES',pid,grp,total,3
 write(*,'(A)')'FD_READONLY_EXEC_NATIVE_POSITIVE_V1'
contains
 subroutine require(ok,code,message)
  logical,intent(in)::ok
  integer,intent(in)::code
  character(len=*),intent(in)::message
  if(.not.ok)then
   write(*,'(A,1X,I0,1X,A)')'FD_CONTRACT_REFUSAL',code,message
   flush(6)
   call c_exit(int(code,c_int))
  endif
 end subroutine
end program readonly_fd_native_startup_control
