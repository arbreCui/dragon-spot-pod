program diagnose_d4a_radial_balance
  ! Read-only fixed-source operator diagnostic, not an absorption or physics gate.
  ! No Dragon routines: the only external data access is GANLIB read-only XSM.
  use GANLIB
  use, intrinsic :: iso_c_binding, only: c_ptr
  use, intrinsic :: iso_fortran_env, only: real32,real64,int32,error_unit
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  integer, parameter :: np=3,ng=370,nr=132,ns=12,nu=144,nm=6
  type(c_ptr) :: root,authority,tracks,fluxes,systems,libraries
  type(c_ptr) :: track,flux,system,library,macro,a,fl,ql,sg,mg,sitem,mitem
  character(len=1024) :: input,output
  integer :: state(40),mat(nr),key(nr),key2(nr),cur(ns),bc(ns),icode(6),zone(nu)
  integer :: indices(nu)
  integer :: njj(nm),ijj(nm),ipos(nm),p,g,h,i,m,s,j,k,n,t,epoch,child_epoch,marker,out,ios
  real(real32) :: volume(nr),weight(nu),alpha(6),total(0:nm),self(0:nm),used_self(0:nm)
  real(real32), allocatable :: scatter(:)
  real(real64) :: u(nu,ng),q(nu,ng),leak(ng),values(11,ng,np),rho,rho_first
  real(real64) :: c_i,s_i,o_i,z_i,q_i,b_s,v,phi,off_density,term,normalized
  logical :: seen(nu),exists

  if(command_argument_count()/=2) call fail('USAGE: diagnose_d4a_radial_balance CANDIDATE_XSM OUTPUT_CSV')
  call get_command_argument(1,input,status=ios)
  if(ios/=0.or.len_trim(input)==0.or.len_trim(input)>72) call fail('INPUT PATH MUST HAVE 1..72 CHARACTERS.')
  call get_command_argument(2,output,status=ios)
  if(ios/=0.or.len_trim(output)==0) call fail('INVALID OUTPUT PATH.')
  inquire(file=trim(input),exist=exists)
  if(.not.exists) call fail('INPUT DOES NOT EXIST.')
  inquire(file=trim(output),exist=exists)
  if(exists) call fail('REFUSING TO OVERWRITE OUTPUT.')
  call LCMOP(root,trim(input),2,2,0)
  call character_record(root,'SIGNATURE','L_ARCHIVE')
  call record(root,'LISTDIM',1,1)
  call LCMGET(root,'LISTDIM',n)
  if(n/=np) call fail('EXPECTED THREE PLANES.')
  authority=directory(root,'SPOT-R64')
  call character_record(authority,'STATE','RETURNED')
  call record(authority,'NPLANE',1,1)
  call LCMGET(authority,'NPLANE',n)
  if(n/=np) call fail('AUTHORITY PLANE COUNT MISMATCH.')
  call record(authority,'EPOCH',1,1)
  call LCMGET(authority,'EPOCH',epoch)
  tracks=list(root,'TRACK',np)
  fluxes=list(root,'FLUX',np)
  systems=list(root,'SYSTEM',np)
  libraries=list(root,'MICROLIB2',np)
  values=0.0_real64
  rho_first=0.0_real64
  do p=1,np
    track=item(tracks,p)
    flux=item(fluxes,p)
    system=item(systems,p)
    library=item(libraries,p)
    call character_record(track,'SIGNATURE','L_TRACK')
    call record(track,'STATE-VECTOR',40,1)
    call LCMGET(track,'STATE-VECTOR',state)
    if(state(1)/=nr.or.state(2)/=nu.or.state(4)/=nm.or.state(5)/=ns) &
      call fail('INVALID D4-A TRACK DIMENSIONS.')
    call record(track,'MATCOD',nr,1)
    call record(track,'KEYFLX',nr,1)
    call record(track,'KEYFLX$ANIS',nr,1)
    call record(track,'KEYCUR$MCCG',ns,1)
    call record(track,'BC-REFL+TRAN',ns,1)
    call record(track,'ICODE',6,1)
    call record(track,'NZON$MCCG',nu,1)
    call record(track,'VOLUME',nr,2)
    call record(track,'V$MCCG',nu,2)
    call record(track,'ALBEDO',6,2)
    call LCMGET(track,'MATCOD',mat)
    call LCMGET(track,'KEYFLX',key)
    call LCMGET(track,'KEYFLX$ANIS',key2)
    call LCMGET(track,'KEYCUR$MCCG',cur)
    call LCMGET(track,'BC-REFL+TRAN',bc)
    call LCMGET(track,'ICODE',icode)
    call LCMGET(track,'NZON$MCCG',zone)
    call LCMGET(track,'VOLUME',volume)
    call LCMGET(track,'V$MCCG',weight)
    call LCMGET(track,'ALBEDO',alpha)
    if(any(mat<1).or.any(mat>nm).or.any(zone(:nr)/=mat)) call fail('INVALID MATERIAL MAP.')
    if(any(zone(nr+1:) > -1).or.any(zone(nr+1:) < -6)) call fail('INVALID BOUNDARY MATERIAL TAG.')
    if(any(key/=key2)) call fail('KEYFLX AND KEYFLX$ANIS DISAGREE.')
    seen=.false.
    indices=[key,cur]
    do i=1,nr+ns
      j=indices(i)
      if(j<1.or.j>nu) call fail('UNKNOWN INDEX OUT OF RANGE.')
      if(seen(j)) call fail('DUPLICATE FLUX/CURRENT INDEX.')
      seen(j)=.true.
    enddo
    if(.not.all(seen)) call fail('INCOMPLETE UNKNOWN INDEX COVERAGE.')
    if(.not.all(ieee_is_finite(volume)).or..not.all(ieee_is_finite(weight))) call fail('NONFINITE WEIGHT.')
    if(any(volume<=0).or.any(weight<=0).or.any(volume/=weight(:nr))) call fail('INVALID VOLUME/SURFACE WEIGHT.')
    if(.not.all(ieee_is_finite(alpha))) call fail('NONFINITE ALBEDO.')
    if(any(alpha/=1.0_real32).or.any(icode>0).or.any(bc/=[(i,i=1,ns)])) &
      call fail('THIS D4-A DIAGNOSTIC REQUIRES IDENTITY WHITE BOUNDARIES.')
    call record(system,'SPOT-L1-RAW',1,1)
    call LCMGET(system,'SPOT-L1-RAW',marker)
    if(marker/=1) call fail('LEAKAGE MUST BE SEPARATE REAL64, NOT EMBEDDED IN SELF SCATTER.')
    call record(flux,'SPOT-FS-EQN',1,1)
    call LCMGET(flux,'SPOT-FS-EQN',marker)
    if(marker/=1) call fail('FIXED-SOURCE EQUATION MARKER MISSING.')
    call record(flux,'LEAK1D64',ng,4)
    call LCMGET(flux,'LEAK1D64',leak)
    if(.not.all(ieee_is_finite(leak))) call fail('NONFINITE LEAK1D64.')
    a=directory(flux,'SPOT-R64')
    call character_record(a,'STATE','SOLVED')
    call record(a,'EPOCH',1,1)
    call LCMGET(a,'EPOCH',child_epoch)
    if(child_epoch/=epoch) call fail('CHILD EPOCH MISMATCH.')
    call record(a,'RHO',1,4)
    call LCMGET(a,'RHO',rho)
    if(.not.ieee_is_finite(rho).or.rho<=0) call fail('INVALID FROZEN RHO.')
    if(p==1) rho_first=rho
    if(rho/=rho_first) call fail('INCONSISTENT FROZEN RHO.')
    fl=list(a,'FLUX',ng)
    ql=list(a,'QFISS',ng)
    ! A9:281 copies the last fixed+offgroup source to terminal SOUR.
    ! QFISS is separate authority; reading SOUR here would double-count scatter.
    do g=1,ng
      call real64_item(fl,g,u(:,g))
      call real64_item(ql,g,q(:,g))
    enddo
    if(any(u(key,:)<=0)) call fail('NONPOSITIVE REGION FLUX.')
    if(any(q<0).or.any(q(cur,:)/=0)) call fail('INVALID FROZEN FISSION SOURCE.')
    macro=directory(library,'MACROLIB')
    call character_record(macro,'SIGNATURE','L_MACROLIB')
    call record(macro,'STATE-VECTOR',40,1)
    call LCMGET(macro,'STATE-VECTOR',state)
    if(state(1)/=ng.or.state(2)/=nm) call fail('INVALID MACROLIB DIMENSIONS.')
    mg=list(macro,'GROUP',ng)
    sg=list(system,'GROUP',ng)
    do g=1,ng
      sitem=item(sg,g)
      mitem=item(mg,g)
      call record(sitem,'DRAGON-TXSC',nm+1,2)
      call record(sitem,'SPOT-S0-PHYS',nm+1,2)
      call record(sitem,'DRAGON-S0XSC',nm+1,2)
      call LCMGET(sitem,'DRAGON-TXSC',total)
      call LCMGET(sitem,'SPOT-S0-PHYS',self)
      call LCMGET(sitem,'DRAGON-S0XSC',used_self)
      if(.not.all(ieee_is_finite(total)).or..not.all(ieee_is_finite(self))) call fail('NONFINITE SYSTEM XS.')
      if(any(transfer(self,[0_int32],nm+1)/=transfer(used_self,[0_int32],nm+1))) &
        call fail('SPOT-S0-PHYS MUST BE BITWISE DRAGON-S0XSC FOR RAW LEAKAGE.')
      call LCMLEN(sitem,'ALBEDO',n,t)
      if(n/=0) call fail('UNEXPECTED GROUP ALBEDO OVERRIDE.')
      call record(mitem,'NJJS00',nm,1)
      call record(mitem,'IJJS00',nm,1)
      call record(mitem,'IPOS00',nm,1)
      call LCMGET(mitem,'NJJS00',njj)
      call LCMGET(mitem,'IJJS00',ijj)
      call LCMGET(mitem,'IPOS00',ipos)
      call LCMLEN(mitem,'SCAT00',n,t)
      if(n<1.or.n>nm*ng.or.t/=2) call fail('INVALID SCAT00 LENGTH/TYPE.')
      allocate(scatter(n))
      call LCMGET(mitem,'SCAT00',scatter)
      if(.not.all(ieee_is_finite(scatter))) call fail('NONFINITE SCAT00.')
      do m=1,nm
        if(njj(m)<0.or.njj(m)>ng) call fail('INVALID SCATTER COUNT.')
        if(njj(m)==0) cycle
        if(ijj(m)<1.or.ijj(m)>ng.or.ijj(m)-njj(m)+1<1) call fail('SCATTER GROUP RANGE INVALID.')
        if(ipos(m)<1.or.ipos(m)>n.or.njj(m)>n-ipos(m)+1) call fail('SCATTER PACKED INDEX INVALID.')
      enddo
      do i=1,nr
        m=mat(i)
        v=real(volume(i),real64)
        phi=u(key(i),g)
        c_i=v*real(total(m),real64)*phi
        s_i=v*real(self(m),real64)*phi
        z_i=v*leak(g)*phi
        q_i=v*q(key(i),g)
        off_density=0.0_real64
        ! Source group descends, exactly as in SPOR64_A9 FLU2DR64_CORE.
        do j=0,njj(m)-1
          h=ijj(m)-j
          k=ipos(m)+j
          if(h==g) cycle
          term=real(scatter(k),real64)*u(key(i),h)
          off_density=off_density+term
          values(11,g,p)=values(11,g,p)+abs(v*term)
        enddo
        o_i=v*off_density
        values(1,g,p)=values(1,g,p)+c_i
        values(2,g,p)=values(2,g,p)+s_i
        values(3,g,p)=values(3,g,p)+o_i
        values(5,g,p)=values(5,g,p)+z_i
        values(6,g,p)=values(6,g,p)+q_i
        values(9,g,p)=values(9,g,p)+v*((real(total(m),real64)-real(self(m),real64)+leak(g))* &
          phi-off_density-q(key(i),g))
        values(11,g,p)=values(11,g,p)+abs(c_i)+abs(s_i)+abs(z_i)+abs(q_i)
      enddo
      do s=1,ns
        b_s=real(weight(nr+s),real64)*(u(cur(s),g)-real(alpha(-zone(nr+s)),real64)*u(cur(bc(s)),g))
        values(7,g,p)=values(7,g,p)+b_s
        values(9,g,p)=values(9,g,p)+b_s
        values(11,g,p)=values(11,g,p)+abs(b_s)
      enddo
      values(4,g,p)=values(1,g,p)-values(2,g,p)-values(3,g,p)
      values(8,g,p)=values(4,g,p)+values(5,g,p)+values(7,g,p)-values(6,g,p)
      values(10,g,p)=values(8,g,p)-values(9,g,p)
      if(.not.all(ieee_is_finite(values(:,g,p)))) call fail('NONFINITE ACCUMULATED DIAGNOSTIC.')
      deallocate(scatter)
    enddo
  enddo
  call LCMCL(root,1)
  open(newunit=out,file=trim(output),status='new',action='write',iostat=ios)
  if(ios/=0) call fail('CANNOT CREATE OUTPUT CSV.')
  write(out,'(A)') 'plane,group,collision,self_scatter,offgroup_scatter,net_removal,axial_loss,'// &
    'frozen_fission,boundary_net,residual_components,residual_local,roundoff_difference,'// &
    'absolute_term_scale,residual_over_scale,normalization_status'
  do p=1,np
    do g=1,ng
      write(out,'(I0,A,I0,11(A,ES25.17E3))',advance='no',iostat=ios) p,',',g,(',',values(i,g,p),i=1,11)
      if(ios/=0) call fail('CSV WRITE FAILED.')
      if(values(11,g,p)>0) then
        normalized=values(8,g,p)/values(11,g,p)
        write(out,'(A,ES25.17E3,A)',iostat=ios) ',',normalized,',defined'
      else
        write(out,'(A)',iostat=ios) ',undefined,zero_denominator'
      endif
      if(ios/=0) call fail('CSV WRITE FAILED.')
    enddo
  enddo
  close(out,iostat=ios)
  if(ios/=0) call fail('CSV CLOSE FAILED.')
  write(*,'(A)') 'D4A-RADIAL-BALANCE DIAGNOSTIC_ONLY; NO PHYSICS/CONVERGENCE ACCEPTANCE'
  write(*,'(A,I0,A,ES25.17E3)') 'SOURCE_EPOCH=',epoch,' FROZEN_PARENT_RHO=',rho_first
  write(*,'(A)') 'REAL64 FLUX/QFISS/LEAK1D64; REAL32 operator XS promoted at use; 1110 rows'
  write(*,'(A)') 'SOUR IS NOT READ: TERMINAL SOUR ALREADY INCLUDES OFF-GROUP SCATTERING'
  write(*,'(A)') 'SCALE=sum of absolute local collision/self/offgroup/axial/fission and net boundary terms'
  write(*,'(A)') 'RESIDUAL_COMPONENTS=M+Z+B-F; RESIDUAL_LOCAL=sum V*((T-S0+L)*u-Soff_density-Q)+B'
  write(*,'(A)') 'NET_REMOVAL IS NOT VERIFIED ABSORPTION; FROZEN QFISS IS NOT RETURNED FISSION'
  write(*,'(A)') 'BOUNDARY ZERO IS A WHITE-BC IDENTITY; FINAL FLUX HAS UNDERGONE GROUP REBALANCING'
contains
  subroutine fail(message)
    character(len=*),intent(in) :: message
    write(error_unit,'(A)') 'D4A-RADIAL-BALANCE ERROR: '//message
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
  function directory(ptr,name) result(child)
    type(c_ptr),intent(in) :: ptr
    character(len=*),intent(in) :: name
    type(c_ptr) :: child
    call record(ptr,name,-1,0)
    child=LCMGID(ptr,name)
  end function directory
  function list(ptr,name,length) result(child)
    type(c_ptr),intent(in) :: ptr
    character(len=*),intent(in) :: name
    integer,intent(in) :: length
    type(c_ptr) :: child
    call record(ptr,name,length,10)
    child=LCMGID(ptr,name)
  end function list
  function item(ptr,index) result(child)
    type(c_ptr),intent(in) :: ptr
    integer,intent(in) :: index
    type(c_ptr) :: child
    integer :: length,typ
    call LCMLEL(ptr,index,length,typ)
    if(typ/=0) call fail('LIST ITEM MUST BE DIRECTORY.')
    child=LCMGIL(ptr,index)
  end function item
  subroutine real64_item(ptr,index,field)
    type(c_ptr),intent(in) :: ptr
    integer,intent(in) :: index
    real(real64),intent(out) :: field(:)
    integer :: length,typ
    call LCMLEL(ptr,index,length,typ)
    if(length/=size(field).or.typ/=4) call fail('AUTHORITY LIST MUST BE REAL64 WITH 144 VALUES.')
    call LCMGDL(ptr,index,field)
    if(.not.all(ieee_is_finite(field))) call fail('NONFINITE REAL64 AUTHORITY FIELD.')
  end subroutine real64_item
end program diagnose_d4a_radial_balance
