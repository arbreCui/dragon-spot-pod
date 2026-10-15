! Synthetic assembly controls only: no FLU, transport or linear solve.
! The actual archive SPOASM is called beside the recovered/rebuilt baseline
! and the private physical-Pn unit. Undefined old higher-tail words are raw
! evidence only; defined old fields and radial recipes are compared externally.
module spoasm_control_abort
  implicit none
  logical, save :: expected_abort=.false.
  character(len=160), save :: wanted=''
end module
program spoasm_physical_angular_controls
  use GANLIB
  use, intrinsic :: iso_fortran_env, only:int32,int64
  use, intrinsic :: ieee_arithmetic, only:ieee_value,ieee_quiet_nan
  use spoasm_control_abort
  implicit none
  integer,parameter :: ng=370,nr=8,ns=3,nmat=24,nrad=14,nax=1800
  type(c_ptr) :: track,macro,snap,basis,out
  type(c_ptr) :: jt,jm,jf,js,jb,ji,kt,km,kf,ks,kb,ki,list,p,q,r,qa
  real :: tt(nmat,ng),ss(nmat,3,ng),rt(0:nr,ns,ng),rs(0:nr,ns,ng)
  double precision :: phi(nrad,ns,ng),qf(nrad,ns,ng),sou(nrad,ns,ng),leak(ng,ns)
  real :: volume(nr),b(nr),coeff(ns),zero8(nr),chi(nr),xs(nr),small(3)
  double precision :: sigma(ns),zero64,dpvec(nrad),rad64(nr*ns),diag(3),rootsigma(ns*ng)
  real :: ft(0:nmat),fs(0:nmat,3),rad32(nr*ns),rv(nr),bc(ns),rmin
  integer :: state(40),axstate(40),radstate(40),keys(nr),mat(nr),ranks(ng),order
  integer :: g,s,i,l,j,unit,manifest,variant,nl,precision,nlong,itype,footer(4)
  integer(int64) :: header(12)
  character(len=80) :: mode,mutation,label,who
  character(len=160) :: name
  character(len=1024) :: paths(4)
  character(len=2) :: can
  logical :: double_authority,physical
  call get_command_argument(1,mode)
  if(storage_size(0)/=32.or.storage_size(0.0)/=32.or.storage_size(0.0d0)/=64) stop 2
  open(newunit=manifest,file='manifest.jsonl',status='new',action='write')
  if(trim(mode)=='positive')then
    do j=1,4
      physical=j<=2;double_authority=mod(j,2)==1
      nl=1;if(physical)nl=3
      precision=32;if(double_authority)precision=64
      who='scalar';if(physical)who='physical'
      write(label,'(A,I0,A,I0)')trim(who),ng,'_',precision
      call inputs()
      call build_objects()
      call save_input(trim(label)//'.inputs.bin')
      do variant=1,3
        call LCMOP(out,'ASSEMBLY',0,1,0)
        select case(variant)
        case(1)
          call SPOASM(out,macro,track,snap,basis,1,0,1)
          who='archive'
        case(2)
          call SPOASM_BASELINE_REBUILT(out,macro,track,snap,basis,1,0,1)
          who='rebuilt'
        case(3)
          call SPOASM_PHYSICAL_UNIT(out,macro,track,snap,basis,1,0,1)
          who='physical_unit'
        end select
        call save_output(trim(label)//'.'//trim(who)//'.bin')
        call LCMCL(out,2)
      enddo
      call release_objects()
    enddo
    close(manifest)
    write(*,'(A)')'RAW_SPOASM_CONTROLS_COMPLETE'
  else if(trim(mode)=='production-input')then
    do i=1,4
      call get_command_argument(i+1,paths(i));if(len_trim(paths(i))==0)stop 2
    enddo
    call LCMOP(macro,trim(paths(1)),2,2,0);call LCMOP(track,trim(paths(2)),2,2,0)
    call LCMOP(snap,trim(paths(3)),2,2,0);call LCMOP(basis,trim(paths(4)),2,2,0)
    label='actualphysical370_64';nl=3;precision=64;double_authority=.true.
    call LCMGET(track,'STATE-VECTOR',axstate)
    if(axstate(1)/=384.or.axstate(2)/=1800.or.axstate(4)/=24.or.axstate(6)/=8.or. &
       axstate(7)/=48.or.axstate(15)/=32.or.axstate(16)/=3)stop 3
    call LCMGET(macro,'STATE-VECTOR',state)
    if(state(1)/=370.or.state(2)/=24.or.state(3)/=3)stop 3
    call LCMGET(snap,'LISTDIM',i);if(i/=3)stop 3
    ! Entire true-input object bytes are retained before invoking assembly.
    call LCMOP(p,'actual_inputs.xsm',0,2,0)
    q=LCMDID(p,'MACRO');call LCMEQU(macro,q)
    q=LCMDID(p,'TRACK');call LCMEQU(track,q)
    q=LCMDID(p,'SNAPSHOTS');call LCMEQU(snap,q)
    q=LCMDID(p,'BASIS');call LCMEQU(basis,q)
    call LCMCL(p,1)
    write(manifest,'(A)')'{"kind":"actual_input_objects","file":"actual_inputs.xsm"}'
    do variant=1,3
      call LCMOP(out,'ASSEMBLY',0,1,0)
      select case(variant)
      case(1)
        call SPOASM(out,macro,track,snap,basis,1,0,1);who='archive'
      case(2)
        call SPOASM_BASELINE_REBUILT(out,macro,track,snap,basis,1,0,1);who='rebuilt'
      case(3)
        call SPOASM_PHYSICAL_UNIT(out,macro,track,snap,basis,1,0,1);who='physical_unit'
      end select
      call save_output(trim(label)//'.'//trim(who)//'.bin');call LCMCL(out,2)
    enddo
    call release_objects();close(manifest)
    write(*,'(A)')'RAW_CURRENT_SPOASM_CONTROLS_COMPLETE'
  else if(trim(mode)=='negative')then
    call get_command_argument(2,mutation)
    nl=3;precision=64;double_authority=.true.;physical=.true.
    label='negative_'//trim(mutation)
    call inputs()
    select case(trim(mutation))
    case('ntot_nonfinite');tt(1,ng)=ieee_value(0.0,ieee_quiet_nan)
    case('sigw1_nonfinite');ss(1,2,ng)=ieee_value(0.0,ieee_quiet_nan)
    end select
    call build_objects()
    jm=LCMGID(macro,'GROUP');km=LCMGIL(jm,ng)
    select case(trim(mutation))
    case('ntot_length')
      call LCMPUT(km,'NTOT0',nmat-1,2,tt(1,ng))
      wanted='SPOASM AXIAL PN: INVALID NTOT0 RECORD.'
    case('ntot_type')
      state(:)=0;call LCMPUT(km,'NTOT0',nmat,1,state)
      wanted='SPOASM AXIAL PN: INVALID NTOT0 RECORD.'
    case('sigw1_length')
      call LCMPUT(km,'SIGW01',nr,2,ss(1,2,ng))
      wanted='SPOASM AXIAL PN: INVALID SIGW RECORD.'
    case('sigw2_missing')
      call LCMDEL(km,'SIGW02')
      wanted='SPOASM AXIAL PN: INVALID SIGW RECORD.'
    case('sigw2_type')
      state(:)=0;call LCMPUT(km,'SIGW02',nmat,1,state)
      wanted='SPOASM AXIAL PN: INVALID SIGW RECORD.'
    case('ntot_nonfinite','sigw1_nonfinite')
      wanted='SPOASM AXIAL PN: NON-FINITE PHYSICAL XS.'
    case('requested_order')
      call LCMGET(macro,'STATE-VECTOR',state);state(3)=2
      call LCMPUT(macro,'STATE-VECTOR',40,1,state)
      wanted='SPOASM AXIAL PN: INCOMPLETE MACRO ANGULAR ORDER.'
    case('moment_total_order')
      call LCMGET(macro,'STATE-VECTOR',state);state(10)=1
      call LCMPUT(macro,'STATE-VECTOR',40,1,state)
      wanted='SPOASM AXIAL PN: UNSUPPORTED MOMENT-DEPENDENT TOTAL.'
    case('radial_length','radial_type')
      js=LCMGID(snap,'SYSTEM');ks=LCMGIL(js,ns);list=LCMGID(ks,'GROUP');p=LCMGIL(list,ng)
      if(trim(mutation)=='radial_length')then
        call LCMPUT(p,'DRAGON-S0XSC',nr,2,rs(0,ns,ng))
      else
        state(:)=0;call LCMPUT(p,'DRAGON-S0XSC',nr+1,1,state)
      endif
      wanted='SPOASM AXIAL PN: INVALID RADIAL S0XSC RECORD.'
    case default
      stop 2
    end select
    ! Retain exact damaged input objects as native XSM as well as the complete
    ! original planned binary operands before the command-specific rejection.
    call LCMOP(p,'damaged_macro.xsm',0,2,0);call LCMEQU(macro,p);call LCMCL(p,1)
    call LCMOP(p,'damaged_snapshots.xsm',0,2,0);call LCMEQU(snap,p);call LCMCL(p,1)
    call save_input(trim(label)//'.inputs.bin')
    write(manifest,'(A)')'{"kind":"negative_expected","case":"'//trim(mutation)// &
      '","expected_XABORT":"'//trim(wanted)//'"}'
    close(manifest);expected_abort=.true.
    call LCMOP(out,'ASSEMBLY',0,1,0)
    call SPOASM_PHYSICAL_UNIT(out,macro,track,snap,basis,1,0,1)
    open(newunit=unit,file='unexpected_return.txt',status='new');write(unit,'(A)')'UNEXPECTED NORMAL RETURN';close(unit)
    stop 1
  else
    stop 2
  endif
contains
  subroutine inputs()
    do i=1,nr
      volume(i)=real(i)/64.0;b(i)=-real(i+8)/16.0;keys(i)=i;mat(i)=i
    enddo
    coeff=[0.75,1.0,1.25];sigma=[1.0d0,0.5d0,0.25d0];zero64=0.0d0;zero8=0.0;chi=1.0
    do g=1,ng
      do i=1,nmat
        tt(i,g)=1.0+real(i)/64.0+real(g)/4096.0
        ss(i,1,g)=0.25+real(i)/1024.0+real(g)/65536.0
        ss(i,2,g)=(-1.0)**i*(0.03125+real(g)/131072.0)
        ss(i,3,g)=(-1.0)**(i+1)*(0.015625+real(i)/65536.0)
      enddo
      do s=1,ns
        rt(0,s,g)=0.0;rs(0,s,g)=0.0
        do i=1,nr
          ! Nonzero common transport shift, varying by material/snapshot.
          rt(i,s,g)=tt((s-1)*nr+i,g)-(real(i+s)/1024.0)
          rs(i,s,g)=ss((s-1)*nr+i,1,g)-(real(i+s)/1024.0)
        enddo
        leak(g,s)=real(g+s,8)/1048576.0d0
        do i=1,nrad
          phi(i,s,g)=1.0d0+real(i,8)/32.0d0+real(s,8)/16.0d0+real(g,8)/4096.0d0
          qf(i,s,g)=0.25d0+real(i+s,8)/128.0d0
          sou(i,s,g)=qf(i,s,g)
        enddo
      enddo
    enddo
    ! Signed zero self-Pn is retained exactly, without clipping or factors.
    ss(1,2,1)=transfer(int(z'80000000',int32),0.0);ss(2,3,ng)=0.0
  end subroutine
  subroutine build_objects()
    call LCMOP(track,'AXTRACK',0,1,0);call LCMOP(macro,'AXMACRO',0,1,0)
    call LCMOP(snap,'SNAPSHOTS',0,1,0);call LCMOP(basis,'BASIS',0,1,0)
    axstate=0;axstate(1)=nr*48;axstate(2)=nax;axstate(4)=nmat;axstate(6)=nr
    axstate(7)=48;axstate(8)=ns;axstate(15)=32;axstate(16)=nl
    call LCMPUT(track,'STATE-VECTOR',40,1,axstate)
    state=0;state(1)=ng;state(2)=nmat;state(3)=nl;state(6)=2
    call LCMPUT(macro,'STATE-VECTOR',40,1,state);jm=LCMLID(macro,'GROUP',ng)
    do g=1,ng
      km=LCMDIL(jm,g);call LCMPUT(km,'NTOT0',nmat,2,tt(1,g))
      do l=1,nl
        write(can,'(I2.2)')l-1;call LCMPUT(km,'SIGW'//can,nmat,2,ss(1,l,g))
      enddo
    enddo
    call LCMPUT(snap,'LISTDIM',1,1,ns)
    jt=LCMLID(snap,'TRACK',ns);jf=LCMLID(snap,'FLUX',ns)
    js=LCMLID(snap,'SYSTEM',ns);ji=LCMLID(snap,'MICROLIB2',ns)
    radstate=0;radstate(1)=nr;radstate(2)=nrad;radstate(4)=nr;radstate(6)=1
    do s=1,ns
      kt=LCMDIL(jt,s);call LCMPUT(kt,'STATE-VECTOR',40,1,radstate)
      call LCMPUT(kt,'KEYFLX',nr,1,keys);call LCMPUT(kt,'MATCOD',nr,1,mat)
      call LCMPUT(kt,'VOLUME',nr,2,volume)
      kf=LCMDIL(jf,s);p=LCMLID(kf,'FLUX',ng);q=LCMLID(kf,'SOUR',ng)
      do g=1,ng
        call LCMPDL(p,g,nrad,2,real(phi(:,s,g)));call LCMPDL(q,g,nrad,2,real(sou(:,s,g)))
      enddo
      call LCMPUT(kf,'SPOT-FS-EQN',1,1,1);call LCMPUT(kf,'SPOT-FS-K',1,2,1.0)
      ! SPOT-QFISS item1 is a heterogeneous list.
      p=LCMLID(kf,'SPOT-QFISS',1);q=LCMLIL(p,1,ng)
      do g=1,ng
        call LCMPDL(q,g,nrad,2,real(qf(:,s,g)))
      enddo
      call LCMPUT(kf,'SPOT-LEAK1D',ng,2,real(leak(:,s)))
      if(double_authority)then
        p=LCMDID(kf,'SPOT-R64');q=LCMLID(p,'FLUX',ng);r=LCMLID(p,'SOUR',ng);qa=LCMLID(p,'QFISS',ng)
        do g=1,ng
          call LCMPDL(q,g,nrad,4,phi(:,s,g));call LCMPDL(r,g,nrad,4,sou(:,s,g))
          call LCMPDL(qa,g,nrad,4,qf(:,s,g))
        enddo
        call LCMPUT(kf,'LEAK1D64',ng,4,leak(:,s))
      endif
      ks=LCMDIL(js,s);state=0;state(8)=ng;state(9)=nrad;state(11)=1
      call LCMPUT(ks,'STATE-VECTOR',40,1,state);list=LCMLID(ks,'GROUP',ng)
      do g=1,ng
        p=LCMDIL(list,g);call LCMPUT(p,'DRAGON-TXSC',nr+1,2,rt(0,s,g))
        call LCMPUT(p,'DRAGON-S0XSC',nr+1,2,rs(0,s,g));call LCMPUT(p,'SPOT-S0-PHYS',nr+1,2,rs(0,s,g))
      enddo
      ki=LCMDIL(ji,s);km=LCMDID(ki,'MACROLIB');state=0;state(1)=ng;state(2)=nr;state(3)=1;state(4)=1
      call LCMPUT(km,'STATE-VECTOR',40,1,state);list=LCMLID(km,'GROUP',ng)
      do g=1,ng
        p=LCMDIL(list,g);call LCMPUT(p,'NUSIGF',nr,2,zero8);call LCMPUT(p,'CHI',nr,2,chi)
        call LCMPUT(p,'NJJS00',nr,1,[(1,i=1,nr)]);call LCMPUT(p,'IJJS00',nr,1,[(g,i=1,nr)])
        call LCMPUT(p,'IPOS00',nr,1,keys);xs=ss((s-1)*nr+1:s*nr,1,g)
        call LCMPUT(p,'SCAT00',nr,2,xs)
      enddo
    enddo
    call LCMPTC(basis,'SIGNATURE',12,'L_PIJ');state=0;state(8)=ng;state(9)=nax
    call LCMPUT(basis,'STATE-VECTOR',40,1,state);ranks=1
    call LCMPUT(basis,'POD-RANK-G',ng,1,ranks);rootsigma=1.0d0
    call LCMPUT(basis,'POD-SIGMA-G',ns*ng,4,rootsigma);jb=LCMLID(basis,'GROUP',ng)
    do g=1,ng
      kb=LCMDIL(jb,g);call LCMPUT(kb,'NREG2D',1,1,nr);call LCMPUT(kb,'NSNAP',1,1,ns)
      call LCMPUT(kb,'POD-NMODE',1,1,1);call LCMPUT(kb,'VOL2D',nr,2,volume)
      call LCMPUT(kb,'POD-BASIS',nr,2,b);call LCMPUT(kb,'POD-COEFF',ns,2,coeff)
      call LCMPUT(kb,'POD-SIGMA',ns,4,sigma);call LCMPUT(kb,'POD-REC-ERR',1,4,zero64)
      call LCMPUT(kb,'POD-ORTHO',1,4,zero64)
    enddo
  end subroutine
  subroutine release_objects()
    if(trim(mode)=='production-input')then
      ! Native XSM inputs were opened read-only: close, never erase.
      call LCMCL(track,1);call LCMCL(macro,1);call LCMCL(snap,1);call LCMCL(basis,1)
    else
      call LCMCL(track,2);call LCMCL(macro,2);call LCMCL(snap,2);call LCMCL(basis,2)
    endif
  end subroutine
  subroutine save_input(file)
    character(len=*),intent(in)::file
    header=[1_int64,370_int64,8_int64,3_int64,24_int64,14_int64,1800_int64, &
      48_int64,32_int64,int(nl,int64),int(precision,int64),1_int64]
    open(newunit=unit,file=file,status='new',form='unformatted',access='stream',convert='little_endian')
    write(unit)header,tt,ss,rt,rs,phi,qf,sou,leak,b,volume,axstate,radstate
    close(unit)
    write(manifest,'(A)')'{"kind":"input","fixture":"'//trim(label)//'","file":"'//file//'"}'
  end subroutine
  subroutine save_output(file)
    character(len=*),intent(in)::file
    header=[1_int64,int(variant,int64),370_int64,8_int64,3_int64,24_int64,14_int64, &
      1800_int64,48_int64,32_int64,int(nl,int64),int(precision,int64)]
    open(newunit=unit,file=file,status='new',form='unformatted',access='stream',convert='little_endian')
    call LCMGET(out,'STATE-VECTOR',state);write(unit)header,state
    list=LCMGID(out,'GROUP')
    do g=1,ng
      p=LCMGIL(list,g)
      call LCMLEN(p,'DRAGON-TXSC',nlong,itype);if(nlong/=25.or.itype/=2)stop 3
      call LCMGET(p,'DRAGON-TXSC',ft)
      call LCMLEN(p,'DRAGON-S0XSC',nlong,itype);if(nlong/=25*nl.or.itype/=2)stop 3
      fs=0.0;call LCMGET(p,'DRAGON-S0XSC',fs)
      call LCMGET(p,'RADIAL-OP',rad32)
      call LCMGET(p,'POD-BASIS',rv);call LCMGET(p,'POD-COEFF',bc)
      call LCMGET(p,'POD-SIGMA',sigma);call LCMGET(p,'POD-REC-ERR',diag(1))
      call LCMGET(p,'POD-ORTHO',diag(2))
      write(unit)ft,fs(:,1:nl)
      if(double_authority)then
        call LCMGET(p,'RADIAL-OP64',rad64);write(unit)rad64
      endif
      write(unit)rad32,rv,bc,sigma,diag(1:2)
    enddo
    call LCMGET(out,'POD-RANK-G',ranks);call LCMGET(out,'POD-SIGMA-G',rootsigma)
    call LCMGET(out,'SPOT-RBAL',diag(1));call LCMGET(out,'SPOT-Q-L2',diag(2))
    call LCMGET(out,'SPOT-Q-MAX',diag(3));call LCMGET(out,'SPOT-REM-MIN',rmin)
    call LCMGET(out,'SPOT-FS-N',footer(1));call LCMGET(out,'SPOT-REM-SNP',footer(2))
    call LCMGET(out,'SPOT-REM-GRP',footer(3));call LCMGET(out,'SPOT-REM-MIX',footer(4))
    write(unit)ranks,rootsigma,diag,rmin,footer;close(unit)
    write(manifest,'(A)')'{"kind":"output","fixture":"'//trim(label)//'","variant":"'// &
      trim(who)//'","file":"'//file//'"}'
  end subroutine
end program
subroutine XABORT(message)
  use spoasm_control_abort
  implicit none
  character(len=*),intent(in)::message
  integer::u
  if(expected_abort.and.trim(message)==trim(wanted))then
    open(newunit=u,file='actual_abort.txt',status='new',action='write')
    write(u,'(A)')trim(message);close(u);write(*,'(A)')'EXPECTED_NATIVE_XABORT '//trim(message)
    stop 0
  endif
  write(*,'(A)')'UNEXPECTED_XABORT '//trim(message)
  stop 1
end subroutine
