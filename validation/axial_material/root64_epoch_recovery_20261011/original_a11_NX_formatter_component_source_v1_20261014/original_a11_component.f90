module locale
   ! Provides localization parameters for NJOY2016.  Each site
   ! should change "lab" and "mx" for their location.  The
   ! "kind" parameter kr is for normal internal real numbers in NJOY.
   ! The default kind is assumed for normal internal integers (either
   ! 4 or 8 bytes should be OK for integers).  The CCCC files use
   ! 4-byte reals, 4-byte integers, and 8-byte Hollerith values,
   ! and k4 and k8 are provided for them.  These values are also used
   ! in subroutine timer when a C-type call is needed.  Caution: the
   ! settings for k4 and k8 may not be portable--some systems might
   ! use 1 and 2 instead of 4 and 8 for these two kinds.
   implicit none
   private
   character(8),public::lab='lanl t2'
   character(8),public::mx='        '
   integer,parameter,public::kr=selected_real_kind(12,300)
   integer,parameter,public::k4=4
   integer,parameter,public::k8=8
end module locale


program original_a11_component
 use locale
 use iso_fortran_env, only: int32,int64,error_unit
 use, intrinsic :: ieee_arithmetic
 implicit none
 integer(int32) :: ng,nr,ri,ni,nstored,ig,ix,ios,before,after,expected(370)
 real(kr) :: temperature,sigma(370),parsed,x
 character(8) :: magic
 character(11) :: field
 character(4096) :: input_path,output_path
 character :: extra
 if(storage_size(0.0)/=32.or.storage_size(0.0_kr)/=64) error stop 'original REAL32/binary64 kind required'
 if(command_argument_count()/=2) error stop 'exact private input/output args'
 call get_command_argument(1,input_path)
 call get_command_argument(2,output_path)
 open(20,file=trim(input_path),access='stream',form='unformatted',status='old',action='read')
 read(20,iostat=ios) magic,ng,nr
 if(ios/=0.or.magic/='NXA11I01'.or.ng/=370.or.nr/=79) error stop 'complete79/370 private scope'
 open(30,file=trim(output_path),access='stream',form='unformatted',status='new',action='write')
 write(30) 'NXA11O01',ng,nr
 do ri=1,nr
  read(20,iostat=ios) ni,nstored,temperature,sigma,expected
  if(ios/=0.or.ni<1.or.ni>11.or.nstored<1.or.nstored>370) error stop 'complete actual record'
  if(.not.all(ieee_is_finite(sigma)).or.any(sigma<0.0_kr)) error stop 'original finite sigma domain'
  write(30) ni,nstored,temperature
  do ig=1,ng
   x=sigma(ig)
   call a11(x,field)
   read(field,'(e11.0)',iostat=ios) parsed
   if(ios/=0.or..not.ieee_is_finite(parsed)) error stop 'native original E11.0 parse'
   before=transfer(real(x),before)
   after=transfer(real(parsed),after)
   write(30) ig,x,field,parsed,before,after,expected(ig)
  enddo
 enddo
 read(20,iostat=ios) extra
 if(ios>=0) error stop 'complete private input EOF'
 close(20)
 close(30)
 write(*,'(a)') 'ORIGINAL_A11_COMPONENT_NATIVE79_COMPLETE'
contains
   subroutine a11(x,hx)
   !--------------------------------------------------------------------
   ! Convert x to ENDF 11-column format as a string in hx.  Normally,
   ! hx has the forms +1.234567+6, +1.23456-38, or -1.2345+308.
   ! If ix=1 and x is between 1.0 and 1.e7, the 9 significant-figure
   ! extended precision forms +1.23456789, +12.3456789, ...,
   ! +123456.789 in f format are allowed as sometimes needed for
   ! resonance shapes.
   !--------------------------------------------------------------------
   ! externals
   real(kr)::x
   character(11)::hx
   ! internals
   character(1)::s
   real(kr)::ff,xx,f
   integer::n
   real(kr),parameter::zero=0
   real(kr),parameter::tenth=0.1e0_kr
   real(kr),parameter::onem=.999999999e0_kr
   real(kr),parameter::one=1
   real(kr),parameter::ten=10
   real(kr),parameter::tmil=.999999999e7_kr
   real(kr),parameter::up=.000000001e0_kr
   real(kr),parameter::top7=9.9999995e0_kr
   real(kr),parameter::top6=9.999995e0_kr
   real(kr),parameter::top5=9.99995e0_kr
   real(kr),parameter::top9=9.999999995e0_kr
   real(kr),parameter::bot9=9.99999995e0_kr

   !--check for zero as a special case
   if (x.ne.zero) go to 100
      f=0
      s='+'
      n=0
      go to 160
   100 if (x.gt.tenth.and.x.lt.tmil) go to 130

   !--normal seven, six, and five sig-fig forms
   xx=x
   n=int(log10(abs(xx)))
   if (abs(xx).lt.one) go to 110
      ff=xx/ten**n
      s='+'
      if (iabs(n).lt.10.and.abs(ff).lt.top7) go to 120
      if (iabs(n).lt.100.and.iabs(n).ge.10.and.&
        abs(ff).lt.top6) go to 120
      if (iabs(n).ge.100.and.abs(ff).lt.top5) go to 120
      ff=ff/ten
      ff=ff+up
      n=n+1
      go to 120
   110 n=1-n
      ff=xx*ten**n
      s='-'
      if (iabs(n).lt.10.and.abs(ff).lt.top7) go to 120
      if (iabs(n).lt.100.and.iabs(n).ge.10.and.&
        abs(ff).lt.top6) go to 120
      if (iabs(n).ge.100.and.abs(ff).lt.top5) go to 120
      ff=ff/ten
      ff=ff+up
      n=n-1
      if (n.gt.0) go to 120
      s='+'
   120 f=ff
   160 if (iabs(n).lt.10) then
         write(hx,'(f9.6,a,i1)') f,s,n
      else if (iabs(n).lt.100) then
         write(hx,'(f8.5,a,i2)') f,s,n
      else
         write(hx,'(f7.4,a,i3)') f,s,n
      endif
      return

   !--extended nine sig-fig form
  130 n=int(log10(abs(x)))
      if (abs(x).lt.onem) go to 140
      f=x/ten**n
      s='+'
      if (iabs(n).lt.10.and.abs(f).lt.top9) go to 150
      if (iabs(n).ge.10.and.abs(f).lt.bot9) go to 150
      f=f/ten
      n=n+1
      go to 150
  140 f=x
      s='-'
      n=-1
  150 continue
   if (n.le.0) write(hx,'(f11.8)') f
   if (n.eq.1) write(hx,'(1p,f11.7)') f
   if (n.eq.2) write(hx,'(2p,f11.6)') f
   if (n.eq.3) write(hx,'(3p,f11.5)') f
   if (n.eq.4) write(hx,'(4p,f11.4)') f
   if (n.eq.5) write(hx,'(5p,f11.3)') f
   if (n.eq.6) write(hx,'(6p,f11.2)') f
   if (n.eq.-1) n=1
   if (f.gt.onem.and.hx(10:11).eq.'00') write(hx,'(f9.6,a,i1)') f,s,n
   if (f.gt.tenth.and.f.lt.onem.and.hx(11:11).eq.'0')&
     write(hx,'(1p,f9.6,a,i1)') f,s,n
   return
   end subroutine a11

end program original_a11_component
