program export_d4a_pin_geometry
  ! Read-only GANLIB export of already-saved SAL topology. No Dragon linkage.
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none
  type(c_ptr) :: root, tracks, track, geom, normalization
  character(len=1024) :: path, output
  character(len=12) :: signature
  integer :: u, s, i, n, t, ne, nn, ni, nr, capacity, state(40), listdim
  integer, allocatable :: ipar(:,:), matcod(:), merge(:)
  real(real64), allocatable :: rpar(:,:), nodevol(:), mergevol(:)
  real(real32), allocatable :: volume(:)

  if (command_argument_count() /= 2) call fail('expected snapshot XSM and output paths')
  call get_command_argument(1,path)
  call get_command_argument(2,output)
  if (len_trim(path)<1 .or. len_trim(path)>72) call fail('XSM path must have 1..72 characters')
  call LCMOP(root,trim(path),2,2,0)
  call require(root,'SIGNATURE',3,3)
  call LCMGTC(root,'SIGNATURE',12,signature)
  if (signature/='L_ARCHIVE') call fail('not L_ARCHIVE')
  call require(root,'LISTDIM',1,1)
  call LCMGET(root,'LISTDIM',listdim)
  if (listdim/=3) call fail('expected three snapshots')
  call require(root,'TRACK',3,10)
  tracks=LCMGID(root,'TRACK')
  open(newunit=u,file=trim(output),status='new',action='write')
  write(u,'(A)') 'D4A_SAVED_PIN_GEOMETRY_V1'
  do s=1,3
    call LCMLEL(tracks,s,n,t)
    if (t/=0) call fail('TRACK item not a directory')
    track=LCMGIL(tracks,s)
    call require(track,'SIGNATURE',3,3)
    call LCMGTC(track,'SIGNATURE',12,signature)
    if (signature/='L_TRACK') call fail('not L_TRACK')
    call require(track,'STATE-VECTOR',40,1)
    call LCMGET(track,'STATE-VECTOR',state)
    if (any(state(1:6)/=[132,144,1,6,12,1])) call fail('unexpected TRACK dimensions')
    call require(track,'MATCOD',132,1)
    call require(track,'VOLUME',132,2)
    call LCMLEN(track,'GEOMETRY',n,t)
    if (t/=0) call fail('missing GEOMETRY directory')
    geom=LCMGID(track,'GEOMETRY')
    call require(geom,'NB_ELEM',1,1)
    call require(geom,'NB_NODE',1,1)
    call require(geom,'NIPAR',1,1)
    call LCMGET(geom,'NB_ELEM',ne)
    call LCMGET(geom,'NB_NODE',nn)
    call LCMGET(geom,'NIPAR',ni)
    if (ne<1 .or. ne>10000 .or. nn/=132 .or. ni/=3) call fail('unexpected SAL dimensions')
    call LCMLEN(geom,'IPAR',n,t)
    if (t/=1 .or. mod(n,ni)/=0 .or. n<ne*ni) call fail('invalid IPAR allocation')
    capacity=n/ni
    if (capacity>30000) call fail('saved SAL allocation outside bounded diagnostic scope')
    call LCMLEN(geom,'RPAR',n,t)
    if (t/=4 .or. mod(n,capacity)/=0) call fail('invalid RPAR')
    nr=n/capacity
    if (nr/=6) call fail('expected six SAL real parameters')
    call require(geom,'VOL_NODE',nn,4)
    call LCMLEN(track,'NXTRecords',n,t)
    if (t/=0) call fail('missing NXTRecords directory')
    normalization=LCMGID(track,'NXTRecords')
    call require(normalization,'NumMerge',nn,1)
    call require(normalization,'VolMerge',nn,4)
    allocate(ipar(ni,capacity),rpar(nr,capacity),matcod(132),volume(132),merge(nn),nodevol(nn),mergevol(nn))
    call LCMGET(geom,'IPAR',ipar)
    call LCMGET(geom,'RPAR',rpar)
    call LCMGET(geom,'VOL_NODE',nodevol)
    call LCMGET(track,'MATCOD',matcod)
    call LCMGET(track,'VOLUME',volume)
    call LCMGET(normalization,'NumMerge',merge)
    call LCMGET(normalization,'VolMerge',mergevol)
    if (any(.not.ieee_is_finite(rpar(:,:ne))) .or. any(.not.ieee_is_finite(nodevol)) .or. &
        any(.not.ieee_is_finite(mergevol)) .or. any(.not.ieee_is_finite(volume))) call fail('nonfinite geometry')
    if (any(nodevol<=0) .or. any(mergevol<=0) .or. any(volume<=0)) call fail('nonpositive areas')
    if (any(merge<1) .or. any(merge>132)) call fail('invalid NumMerge')
    write(u,'(A,5(1X,I0))') 'SNAPSHOT',s,ne,nn,ni,nr
    do i=1,132
      write(u,'(A,3(1X,I0),3(1X,ES26.17E3))') 'REGION',i,matcod(i),merge(i), &
        real(volume(i),real64),nodevol(i),mergevol(i)
    enddo
    do i=1,ne
      write(u,'(A,4(1X,I0),6(1X,ES26.17E3))') 'ELEMENT',i,ipar(:,i),rpar(:,i)
    enddo
    deallocate(ipar,rpar,matcod,volume,merge,nodevol,mergevol)
  enddo
  write(u,'(A)') 'END'
  close(u)
  call LCMCL(root,1)
  write(*,'(A)') 'D4A SAVED PIN GEOMETRY EXPORTED; GANLIB READ-ONLY; NO TRANSPORT'
contains
  subroutine require(p,key,wantlen,wanttype)
    type(c_ptr), intent(in) :: p
    character(len=*), intent(in) :: key
    integer, intent(in) :: wantlen,wanttype
    integer :: gotlen,gottype
    call LCMLEN(p,key,gotlen,gottype)
    if (gotlen/=wantlen .or. gottype/=wanttype) then
      write(*,*) trim(key),' expected ',wantlen,wanttype,' got ',gotlen,gottype
      call fail('record mismatch')
    endif
  end subroutine require
  subroutine fail(message)
    character(len=*), intent(in) :: message
    write(*,'(A,A)') 'D4A PIN GEOMETRY FAIL: ',message
    error stop 1
  end subroutine fail
end program export_d4a_pin_geometry
