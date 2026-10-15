program inspect_snapshot
  ! Independent read-only Ganlib inspection of newly computed pin snapshots.
  use GANLIB
  use, intrinsic :: iso_c_binding, only: c_ptr
  use, intrinsic :: iso_fortran_env, only: real32,real64,error_unit
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  type(c_ptr) :: archive,objects,track,flux,micro,macro,system,groups
  character(len=1024) :: name,prefix
  character(len=12) :: signature
  integer :: ns,ts(40),fs(40),ms(40),ss(40),key(8),mat(8),i,g,n,t,u,ios
  real(real32) :: volume(8),k
  real(real32),allocatable :: field(:)
  real(real64) :: radii(7),expected(8),area,minimum
  if(command_argument_count()/=2) call fail('USAGE: inspect_snapshot SNAPSHOT NEW_PREFIX')
  call get_command_argument(1,name)
  call get_command_argument(2,prefix)
  if(len_trim(name)>72) call fail('SHORT XSM INPUT NAME REQUIRED')
  call LCMOP(archive,trim(name),2,2,0)
  call LCMGTC(archive,'SIGNATURE',12,signature)
  if(signature/='L_ARCHIVE') call fail('NOT AN ARCHIVE')
  call require(archive,'LISTDIM',1,1)
  call LCMGET(archive,'LISTDIM',ns)
  if(ns/=1) call fail('EXACTLY ONE SNAPSHOT REQUIRED')
  track=object('TRACK');flux=object('FLUX');micro=object('MICROLIB2');system=object('SYSTEM')
  macro=LCMGID(micro,'MACROLIB')
  call require(track,'STATE-VECTOR',40,1);call LCMGET(track,'STATE-VECTOR',ts)
  call require(flux,'STATE-VECTOR',40,1);call LCMGET(flux,'STATE-VECTOR',fs)
  call require(macro,'STATE-VECTOR',40,1);call LCMGET(macro,'STATE-VECTOR',ms)
  call require(system,'STATE-VECTOR',40,1);call LCMGET(system,'STATE-VECTOR',ss)
  if(ts(1)/=8.or.ts(4)/=8.or.fs(1)/=370.or.fs(2)/=ts(2)) call fail('TRACK/FLUX DIMENSIONS')
  if(ms(1)/=370.or.ms(2)/=8.or.ms(3)/=3.or.ms(4)/=32) call fail('MACROLIB DIMENSIONS')
  call require(track,'KEYFLX',8,1);call LCMGET(track,'KEYFLX',key)
  call require(track,'MATCOD',8,1);call LCMGET(track,'MATCOD',mat)
  call require(track,'VOLUME',8,2);call LCMGET(track,'VOLUME',volume)
  if(any(key<1).or.any(key>fs(2)).or.any(mat/=[(i,i=1,8)])) call fail('PIN REGION MAP')
  if(any(volume<=0).or..not.all(ieee_is_finite(volume))) call fail('VOLUME')
  radii=[.11_real64,.308712_real64,.381084_real64,.412536_real64,.4225_real64,.435_real64,.485_real64]
  area=3*sqrt(3.0_real64)*.61776479_real64**2/2
  expected(1)=area-acos(-1.0_real64)*radii(7)**2
  do i=2,7
    expected(i)=acos(-1.0_real64)*(radii(9-i)**2-radii(8-i)**2)
  enddo
  expected(8)=acos(-1.0_real64)*radii(1)**2
  if(maxval(abs(real(volume,real64)/expected-1))>5e-6_real64) call fail('PHYSICAL GEOMETRY DIFFERS')
  call require(flux,'K-EFFECTIVE',1,2);call LCMGET(flux,'K-EFFECTIVE',k)
  if(.not.ieee_is_finite(k).or.k<=0) call fail('INVALID SNAPSHOT K')
  call require(flux,'FLUX',370,10);groups=LCMGID(flux,'FLUX')
  allocate(field(fs(2)));minimum=huge(1.0_real64)
  open(newunit=u,file=trim(prefix)//'.flux.csv',status='new',action='write',iostat=ios)
  if(ios/=0) call fail('REFUSE OUTPUT OVERWRITE')
  write(u,'(A)') 'group,region,scalar_flux'
  do g=1,370
    call LCMLEL(groups,g,n,t)
    if(n/=fs(2).or.t/=2) call fail('FLUX GROUP DIMENSIONS')
    call LCMGDL(groups,g,field)
    if(.not.all(ieee_is_finite(field))) call fail('NONFINITE FLUX')
    do i=1,8
      if(field(key(i))<=0) call fail('NONPOSITIVE SCALAR FLUX')
      minimum=min(minimum,real(field(key(i)),real64))
      write(u,'(I0,A,I0,A,ES25.17E3)') g,',',i,',',field(key(i))
    enddo
  enddo
  close(u)
  open(newunit=u,file=trim(prefix)//'.geometry.csv',status='new',action='write',iostat=ios)
  if(ios/=0) call fail('REFUSE OUTPUT OVERWRITE')
  write(u,'(A)') 'region,mixture,keyflux,stored_area_cm2,independent_area_cm2'
  do i=1,8
    write(u,'(I0,A,I0,A,I0,A,ES25.17E3,A,ES25.17E3)') i,',',mat(i),',',key(i),',',volume(i),',',expected(i)
  enddo
  close(u)
  write(*,'(A)') 'SNAPSHOT_RECORD_INSPECTION_PASS'
  write(*,'(A,I0)') 'snapshots=',ns
  write(*,'(A,I0)') 'groups=',fs(1)
  write(*,'(A,I0)') 'regions=',ts(1)
  write(*,'(A,I0)') 'fission_components=',ms(4)
  write(*,'(A,ES25.17E3)') 'k_snapshot_real32=',k
  write(*,'(A,ES25.17E3)') 'minimum_scalar_flux=',minimum
  call LCMCL(archive,1)
contains
  function object(label) result(p)
    character(len=*),intent(in)::label
    type(c_ptr)::p
    call require(archive,label,1,10)
    objects=LCMGID(archive,label);p=LCMGIL(objects,1)
  end function
  subroutine require(p,label,length,kind)
    type(c_ptr),intent(in)::p
    character(len=*),intent(in)::label
    integer,intent(in)::length,kind
    integer::a,b
    call LCMLEN(p,label,a,b)
    if(a/=length.or.b/=kind) call fail('INVALID RECORD '//label)
  end subroutine
  subroutine fail(message)
    character(len=*),intent(in)::message
    write(error_unit,'(A)') 'SNAPSHOT_RECORD_INSPECTION_FAIL: '//message
    error stop 1
  end subroutine
end program
