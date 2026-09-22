program diagnose_d4a_axial_current
  ! Read-only saved-current diagnostic. GANLIB only; no solver, FLUX32 fallback,
  ! tolerance, clipping, convergence gate, or nuclear-reaction balance claim.
  use GANLIB
  use, intrinsic :: iso_c_binding, only: c_ptr
  use, intrinsic :: iso_fortran_env, only: real32,real64,int64,error_unit
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  integer, parameter :: nr=132,nf=3,ng=370,nreg=nr*nf,nrow=nf*ng
  type(c_ptr) :: track,axial,flux64
  character(len=1024) :: paths(3)
  integer :: ts(40),fs(40),key(nreg),axkey(nreg),mat1d(nf)
  integer :: nunk,ll4,ll5,i,p,g,s,base,ireg,index,n,t,ios,out,epoch
  integer :: equal(nf,ng),nonpositive(nf,ng),negative_bottom(ng),negative_top(ng)
  real(real32) :: area(nr),height(nf)
  real(real64), allocatable :: unknown(:)
  real(real64) :: saved(nrow),value(8,nf,ng),whole(4,ng)
  real(real64) :: a,lo,hi,phi
  logical :: exists

  if(command_argument_count()/=3) call fail('USAGE: diagnose_d4a_axial_current TRACK_XSM AXIAL_XSM NEW_OUTPUT_CSV')
  do i=1,3
    call get_command_argument(i,paths(i),status=ios)
    if(ios/=0.or.len_trim(paths(i))==0) call fail('INVALID PATH ARGUMENT.')
    if(i<=2) then
      if(len_trim(paths(i))>72) call fail('XSM PATH EXCEEDS 72 CHARACTERS; USE SHORT INPUT NAMES.')
      inquire(file=trim(paths(i)),exist=exists)
      if(.not.exists) call fail('INPUT DOES NOT EXIST: '//trim(paths(i)))
    endif
  enddo
  inquire(file=trim(paths(3)),exist=exists)
  if(exists) call fail('REFUSING TO OVERWRITE OUTPUT.')
  call LCMOP(track,trim(paths(1)),2,2,0)
  call LCMOP(axial,trim(paths(2)),2,2,0)
  call character_record(track,'SIGNATURE','L_TRACK')
  call character_record(track,'TRACK-TYPE','SPOT')
  call character_record(axial,'SIGNATURE','L_FLUX')
  call record(track,'STATE-VECTOR',40,1)
  call record(axial,'STATE-VECTOR',40,1)
  call LCMGET(track,'STATE-VECTOR',ts)
  call LCMGET(axial,'STATE-VECTOR',fs)
  nunk=ts(2)
  ll4=ts(11)
  ll5=ts(12)
  if(ts(1)/=nreg.or.ts(6)/=nr.or.ts(7)/=nf.or.ts(8)/=nf.or.fs(1)/=ng.or.fs(2)/=nunk) &
    call fail('INCONSISTENT D4-A TRACK/AXIAL DIMENSIONS.')
  if(nunk<=0.or.ll4<0.or.ll4>nunk.or.ll5/=nr*(nf+1)) call fail('INVALID CURRENT BLOCK LAYOUT.')
  if(ll5>nunk-ll4) call fail('CURRENT BLOCK EXCEEDS UNKNOWN VECTOR.')
  call record(track,'KEYFLX',nreg,1)
  call record(axial,'KEYFLX',nreg,1)
  call record(track,'MAT1D',nf,1)
  call record(track,'AREA2D',nr,2)
  call record(track,'VOL1D',nf,2)
  call LCMGET(track,'KEYFLX',key)
  call LCMGET(axial,'KEYFLX',axkey)
  call LCMGET(track,'MAT1D',mat1d)
  call LCMGET(track,'AREA2D',area)
  call LCMGET(track,'VOL1D',height)
  if(any(key<1).or.any(key>ll4)) call fail('SCALAR FLUX INDEX OUT OF RANGE OR IN CURRENT BLOCK.')
  if(any(key/=axkey)) call fail('TRACK AND AXIAL KEYFLX DISAGREE.')
  do i=1,nreg
    if(any(key(:i-1)==key(i))) call fail('DUPLICATE SCALAR FLUX INDEX.')
  enddo
  if(any(mat1d<1).or.any(mat1d>nf)) call fail('MAT1D INDEX OUT OF RANGE.')
  do s=1,nf
    if(count(mat1d==s)/=1) call fail('D4-A REQUIRES A ONE-TO-ONE FLOOR/SNAPSHOT MAP.')
  enddo
  if(.not.all(ieee_is_finite(area)).or..not.all(ieee_is_finite(height))) call fail('NONFINITE GEOMETRY.')
  if(any(area<=0).or.any(height<=0)) call fail('NONPOSITIVE AREA2D OR VOL1D.')
  call record(axial,'SPOT-X-L',nrow,4)
  call LCMGET(axial,'SPOT-X-L',saved)
  if(.not.all(ieee_is_finite(saved))) call fail('NONFINITE SAVED LEAKAGE.')
  call record(axial,'FLUX64',ng,10)
  flux64=LCMGID(axial,'FLUX64')
  epoch=-1
  call LCMLEN(axial,'SPOT-X-EPOCH',n,t)
  if(n/=0) then
    call record(axial,'SPOT-X-EPOCH',1,1)
    call LCMGET(axial,'SPOT-X-EPOCH',epoch)
  endif
  allocate(unknown(nunk))
  value=0.0_real64
  whole=0.0_real64
  nonpositive=0
  negative_bottom=0
  negative_top=0
  do g=1,ng
    call LCMLEL(flux64,g,n,t)
    if(n/=nunk.or.t/=4) call fail('FLUX64 ITEM MUST BE NUNK REAL64 VALUES.')
    call LCMGDL(flux64,g,unknown)
    if(.not.all(ieee_is_finite(unknown))) call fail('NONFINITE FLUX64 FIELD.')
    ! SPOSTATE:236-279 / SPOLE1D: floor then region, without reassociation.
    do p=1,nf
      do i=1,nr
        ireg=(i-1)*nf+p
        base=ll4+(i-1)*(nf+1)
        lo=unknown(base+p)
        hi=unknown(base+p+1)
        phi=unknown(key(ireg))
        a=real(area(i),real64)
        value(1,p,g)=value(1,p,g)+a*lo
        value(2,p,g)=value(2,p,g)+a*hi
        value(3,p,g)=value(3,p,g)+a*(hi-lo)
        value(4,p,g)=value(4,p,g)+a*real(height(p),real64)*phi
        if(phi<=0) nonpositive(p,g)=nonpositive(p,g)+1
        if(p==1.and.lo>0) negative_bottom(g)=negative_bottom(g)+1
        if(p==nf.and.hi<0) negative_top(g)=negative_top(g)+1
      enddo
      if(.not.all(ieee_is_finite(value(1:4,p,g)))) call fail('NONFINITE CURRENT/FLUX INTEGRAL.')
      if(value(4,p,g)==0.0_real64) call fail('ZERO DENOMINATOR; LEAKAGE IS UNDEFINED.')
      value(5,p,g)=value(3,p,g)/value(4,p,g)
      index=(mat1d(p)-1)*ng+g
      value(6,p,g)=saved(index)
      value(7,p,g)=value(5,p,g)-value(6,p,g)
      value(8,p,g)=(value(2,p,g)-value(1,p,g))-value(3,p,g)
      if(.not.all(ieee_is_finite(value(:,p,g)))) call fail('NONFINITE LEAKAGE DIAGNOSTIC.')
      equal(p,g)=merge(1,0,transfer(value(5,p,g),0_int64)==transfer(value(6,p,g),0_int64))
      whole(1,g)=whole(1,g)+value(3,p,g)
    enddo
    ! +z current at both faces; bottom outward flux has the opposite sign.
    whole(2,g)=-value(1,1,g)
    whole(3,g)=value(2,nf,g)
    whole(4,g)=whole(1,g)-(whole(2,g)+whole(3,g))
    if(.not.all(ieee_is_finite(whole(:,g)))) call fail('NONFINITE TELESCOPING DIAGNOSTIC.')
  enddo
  call LCMCL(axial,1)
  call LCMCL(track,1)
  open(newunit=out,file=trim(paths(3)),status='new',action='write',iostat=ios)
  if(ios/=0) call fail('CANNOT CREATE OUTPUT CSV.')
  write(out,'(A)',iostat=ios) 'plane,group,low_current,high_current,numerator,denominator,'// &
    'recomputed_leak,saved_leak,bitwise_equal,snapshot,leak_difference,face_integral_difference,'// &
    'group_numerator,bottom_outflow,top_outflow,telescoping_difference,'// &
    'bottom_negative_outflow_regions,top_negative_outflow_regions,nonpositive_flux_regions'
  if(ios/=0) call fail('CSV HEADER WRITE FAILED.')
  do p=1,nf
    do g=1,ng
      write(out,'(I0,A,I0,6(A,ES25.17E3),2(A,I0),6(A,ES25.17E3),3(A,I0))',iostat=ios) &
        p,',',g,(',',value(i,p,g),i=1,6),',',equal(p,g),',',mat1d(p), &
        ',',value(7,p,g),',',value(8,p,g),(',',whole(i,g),i=1,4), &
        ',',negative_bottom(g),',',negative_top(g),',',nonpositive(p,g)
      if(ios/=0) call fail('CSV ROW WRITE FAILED.')
    enddo
  enddo
  close(out,iostat=ios)
  if(ios/=0) call fail('CSV CLOSE FAILED.')
  write(*,'(A)') 'D4A-AXIAL-CURRENT DIAGNOSTIC_ONLY; NO PHYSICS/CONVERGENCE ACCEPTANCE'
  write(*,'(A,I0,A,I0,A,I0,A,I0)') 'EPOCH=',epoch,' NUNK=',nunk,' LL4=',ll4,' LL5=',ll5
  write(*,'(A,I0,A,I0)') 'LEAK_BITWISE_EQUAL_COUNT=',sum(equal),'/',nrow
  write(*,'(A)') 'LOW/HIGH ARE +Z CURRENT INTEGRALS; BOTTOM_OUTFLOW=-LOW; TOP_OUTFLOW=HIGH'
  write(*,'(A)') 'GROUP TOTALS/BOUNDARY COUNTS REPEAT ON EACH FLOOR ROW; DEDUPLICATE BY GROUP'
  write(*,'(A,I0,A,I0,A,I0)') 'NEGATIVE_BOTTOM_REGIONS=',sum(negative_bottom), &
    ' NEGATIVE_TOP_REGIONS=',sum(negative_top),' NONPOSITIVE_FLUX_REGIONS=',sum(nonpositive)
  write(*,'(A,I0)') 'NEGATIVE_DENOMINATOR_ROWS=',count(value(4,:,:)<0.0_real64)
contains
  subroutine fail(message)
    character(len=*),intent(in) :: message
    write(error_unit,'(A)') 'D4A-AXIAL-CURRENT ERROR: '//message
    error stop 1
  end subroutine fail
  subroutine record(ptr,name,length,kind)
    type(c_ptr),intent(in) :: ptr
    character(len=*),intent(in) :: name
    integer,intent(in) :: length,kind
    integer :: actual,typ
    call LCMLEN(ptr,name,actual,typ)
    if(actual/=length.or.typ/=kind) call fail('INVALID RECORD LENGTH/TYPE: '//name)
  end subroutine record
  subroutine character_record(ptr,name,expected)
    type(c_ptr),intent(in) :: ptr
    character(len=*),intent(in) :: name,expected
    character(len=12) :: text
    call record(ptr,name,3,3)
    call LCMGTC(ptr,name,12,text)
    if(text/=expected) call fail('INVALID CHARACTER RECORD: '//name)
  end subroutine character_record
end program diagnose_d4a_axial_current
