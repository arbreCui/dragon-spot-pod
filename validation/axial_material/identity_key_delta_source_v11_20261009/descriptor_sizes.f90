program descriptor_sizes
 use, intrinsic :: iso_fortran_env, only:int64
 use SPOT1P64_CACHE_MOD
 implicit none
 type(SPOT1P64_MODE_PLAN) :: mode
 type(SPOT1P64_GROUP_PLAN) :: group
 write(*,'(A,I0)') 'mode_bytes=',storage_size(mode,kind=int64)/8_int64
 write(*,'(A,I0)') 'group_bytes=',storage_size(group,kind=int64)/8_int64
end program descriptor_sizes
