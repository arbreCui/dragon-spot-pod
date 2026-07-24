program make_raw_moc_ulp_bridge_fixture
  ! Ganlib-only XSM fixture for the raw-MOC ULP bridge reader.
  ! The group, region and unknown axes carry independent sentinels and the
  ! scalar KEYFLX layout is deliberately permuted.
  use GANLIB
  use, intrinsic :: ieee_arithmetic
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, real32, real64
  implicit none

  integer, parameter :: ng=370
  integer, parameter :: nr=8
  integer, parameter :: nu=14
  integer, parameter :: nstate=40
  integer, parameter :: naudit_state=24
  character(len=1024) :: outdir,arm_arg,mode
  character(len=1024) :: track_path,pre_path,off_path,on_path
  integer :: arm,ios,group,unknown,region,key
  integer :: keyflux(nr),marker(ng),ngind(ng)
  real(real32) :: pre(nu,ng),off(nu,ng)
  real(real64) :: evaluated(nu,ng),raw(nu,ng)
  integer(int32) :: base_bits,target_bits
  integer :: bridge_step,production_step
  real(real64) :: base64,next64

  if (command_argument_count() /= 3) &
    error stop 'expected OUTDIR ARM MODE'
  call get_command_argument(1,outdir)
  call get_command_argument(2,arm_arg)
  call get_command_argument(3,mode)
  read(arm_arg,*,iostat=ios) arm
  if ((ios /= 0).or.(arm < 1).or.(arm > 2)) &
    error stop 'arm must be 1 or 2'

  track_path=trim(outdir)//'/track.xsm'
  pre_path=trim(outdir)//'/pre.xsm'
  off_path=trim(outdir)//'/off.xsm'
  on_path=trim(outdir)//'/on.xsm'
  if (max(len_trim(track_path),len_trim(pre_path), &
      len_trim(off_path),len_trim(on_path)) > 72) &
    error stop 'fixture path exceeds Ganlib limit'

  keyflux=[8,1,7,2,6,3,5,4]
  marker=[(group,group=1,ng)]
  ngind=marker
  do group=1,ng
    do unknown=1,nu
      base_bits=int(z'3F000000',int32)+ &
        int(64*group+unknown,int32)
      pre(unknown,group)=transfer(base_bits,0.0_real32)
      off(unknown,group)=pre(unknown,group)
      evaluated(unknown,group)=real(pre(unknown,group),real64)
      target_bits=base_bits+1000_int32+int(unknown,int32)
      raw(unknown,group)=real(transfer(target_bits,0.0_real32),real64)
    enddo
    do region=1,nr
      key=keyflux(region)
      base_bits=transfer(pre(key,group),0_int32)
      bridge_step=mod(group+2*region,7)-3
      target_bits=base_bits+int(bridge_step,int32)
      if ((bridge_step == 0).and.(mod(group+region,2) == 1)) then
        base64=real(pre(key,group),real64)
        next64=real(transfer(base_bits+1_int32,0.0_real32),real64)
        raw(key,group)=base64+(next64-base64)/4.0_real64
      else
        raw(key,group)=real(transfer(target_bits,0.0_real32),real64)
      endif
      production_step=mod(3*group+region,9)-4
      off(key,group)=transfer(base_bits+ &
        int(production_step,int32),0.0_real32)
    enddo
  enddo

  select case (trim(mode))
  case ('valid','current','raw-bit','off-bit','pre','eval', &
      'group','ngind','incomplete','extra','raw-type','raw-nan', &
      'raw-inf','raw-negative','raw-overflow','raw-underflow', &
      'raw-subnormal','eval-zero','eval-negative-zero','eval-nan', &
      'eval-nonpromotion','off-zero','off-nan','key-duplicate', &
      'key-alternate','key-long','track-branch','pre-type','off-length', &
      'eval-type', &
      'raw-length','qfr-type','src-length','step-type','role-length', &
      'missing-audit')
    continue
  case default
    error stop 'unknown fixture mode'
  end select

  if (trim(mode) == 'current') then
    raw(9,1)=nearest(raw(9,1),1.0_real64)
  else if (trim(mode) == 'raw-bit') then
    key=keyflux(2)
    raw(key,1)=nearest(raw(key,1),1.0_real64)
  else if (trim(mode) == 'off-bit') then
    key=keyflux(1)
    base_bits=transfer(off(key,1),0_int32)
    off(key,1)=transfer(base_bits+1_int32,0.0_real32)
  else if (trim(mode) == 'pre') then
    key=keyflux(1)
    base_bits=transfer(pre(key,1),0_int32)
    pre(key,1)=transfer(base_bits+1_int32,0.0_real32)
  else if (trim(mode) == 'eval') then
    key=keyflux(1)
    base_bits=transfer(pre(key,1),0_int32)
    evaluated(key,1)=real(transfer(base_bits+1_int32, &
      0.0_real32),real64)
  else if (trim(mode) == 'group') then
    marker(1)=2
  else if (trim(mode) == 'ngind') then
    ngind(1)=2
  else if (trim(mode) == 'raw-nan') then
    key=keyflux(1)
    raw(key,1)=ieee_value(raw(key,1),ieee_quiet_nan)
  else if (trim(mode) == 'raw-inf') then
    key=keyflux(1)
    raw(key,1)=ieee_value(raw(key,1),ieee_positive_inf)
  else if (trim(mode) == 'raw-negative') then
    key=keyflux(1)
    raw(key,1)=-raw(key,1)
  else if (trim(mode) == 'raw-overflow') then
    key=keyflux(1)
    raw(key,1)=scale(2.0_real64-2.0_real64**(-24),127)
  else if (trim(mode) == 'raw-underflow') then
    key=keyflux(1)
    raw(key,1)=scale(1.0_real64,-150)
  else if (trim(mode) == 'raw-subnormal') then
    key=keyflux(1)
    raw(key,1)=scale(1.0_real64,-149)
  else if (trim(mode) == 'eval-zero') then
    key=keyflux(1)
    evaluated(key,1)=0.0_real64
    pre(key,1)=0.0_real32
  else if (trim(mode) == 'eval-negative-zero') then
    key=keyflux(1)
    pre(key,1)=transfer(int(z'80000000',int32),0.0_real32)
    evaluated(key,1)=real(pre(key,1),real64)
  else if (trim(mode) == 'eval-nan') then
    key=keyflux(1)
    evaluated(key,1)=ieee_value(evaluated(key,1),ieee_quiet_nan)
  else if (trim(mode) == 'eval-nonpromotion') then
    key=keyflux(1)
    evaluated(key,1)=nearest(evaluated(key,1),1.0_real64)
  else if (trim(mode) == 'off-zero') then
    key=keyflux(1)
    off(key,1)=0.0_real32
  else if (trim(mode) == 'off-nan') then
    key=keyflux(1)
    off(key,1)=ieee_value(off(key,1),ieee_quiet_nan)
  else if (trim(mode) == 'key-duplicate') then
    keyflux(8)=keyflux(1)
  else if (trim(mode) == 'key-alternate') then
    keyflux=[1,7,2,6,3,5,4,8]
  endif

  call write_track(trim(track_path),keyflux,trim(mode))
  call write_flux(trim(pre_path),pre,'PRE',trim(mode))
  call write_flux(trim(off_path),off,'OFF',trim(mode))
  call write_on(trim(on_path),off,evaluated,raw,arm,marker,ngind, &
    trim(mode))

contains

  subroutine write_track(path,keyflux,mode)
    character(len=*), intent(in) :: path,mode
    integer, intent(in) :: keyflux(nr)
    type(c_ptr) :: root
    integer :: state(nstate),long_keys(nr+1)
    character(len=12) :: text

    call LCMOP(root,path,0,2,0)
    text='L_TRACK'
    call LCMPTC(root,'SIGNATURE',12,text)
    text='MCCG'
    call LCMPTC(root,'TRACK-TYPE',12,text)
    state=0
    state(1)=nr
    state(2)=nu
    state(5)=6
    state(6)=1
    state(9)=0
    if (trim(mode) == 'track-branch') state(9)=1
    call LCMPUT(root,'STATE-VECTOR',nstate,1,state)
    if (trim(mode) == 'key-long') then
      long_keys(1:nr)=keyflux
      long_keys(nr+1)=nu
      call LCMPUT(root,'KEYFLX$ANIS',nr+1,1,long_keys)
    else
      call LCMPUT(root,'KEYFLX$ANIS',nr,1,keyflux)
    endif
    call LCMCL(root,1)
  end subroutine write_track


  subroutine write_flux(path,flux,owner,mode)
    character(len=*), intent(in) :: path,owner,mode
    real(real32), intent(in) :: flux(nu,ng)
    type(c_ptr) :: root,groups
    integer :: state(nstate),group
    real(real64) :: flux64(nu)
    character(len=12) :: text

    call LCMOP(root,path,0,2,0)
    text='L_FLUX'
    call LCMPTC(root,'SIGNATURE',12,text)
    state=0
    state(1)=ng
    state(2)=nu
    state(3)=1
    call LCMPUT(root,'STATE-VECTOR',nstate,1,state)
    groups=LCMLID(root,'FLUX',ng)
    do group=1,ng
      if ((trim(mode) == 'pre-type').and. &
          (trim(owner) == 'PRE').and.(group == 1)) then
        flux64=real(flux(:,group),real64)
        call LCMPDL(groups,group,nu,4,flux64)
      else if ((trim(mode) == 'off-length').and. &
          (trim(owner) == 'OFF').and.(group == 1)) then
        call LCMPDL(groups,group,nu-1,2,flux(1:nu-1,group))
      else
        call LCMPDL(groups,group,nu,2,flux(:,group))
      endif
    enddo
    call LCMCL(root,1)
  end subroutine write_flux


  subroutine write_on(path,flux,evaluated,raw,arm,marker,ngind,mode)
    character(len=*), intent(in) :: path,mode
    real(real32), intent(in) :: flux(nu,ng)
    real(real64), intent(in) :: evaluated(nu,ng),raw(nu,ng)
    integer, intent(in) :: arm,marker(ng),ngind(ng)
    type(c_ptr) :: root,flux_groups,audit,groups,group_dir
    integer :: state(nstate),audit_state(naudit_state),group
    integer :: one(1)
    real(real64) :: dummy(nu)
    real(real32) :: raw32(nu)
    character(len=12) :: text

    call LCMOP(root,path,0,2,0)
    text='L_FLUX'
    call LCMPTC(root,'SIGNATURE',12,text)
    state=0
    state(1)=ng
    state(2)=nu
    state(3)=1
    call LCMPUT(root,'STATE-VECTOR',nstate,1,state)
    flux_groups=LCMLID(root,'FLUX',ng)
    do group=1,ng
      call LCMPDL(flux_groups,group,nu,2,flux(:,group))
    enddo
    if (trim(mode) == 'missing-audit') then
      call LCMCL(root,1)
      return
    endif

    audit=LCMDID(root,'SPOT-MOC-AUD')
    audit_state=[1,1,arm,1,1,1,1,1,1,1,1,1,10,1,80,0,0,4,0, &
      ng,ng,nu,nr,ng]
    if (trim(mode) == 'incomplete') audit_state(2)=0
    call LCMPUT(audit,'STATE-VECTOR',naudit_state,1,audit_state)
    call LCMPUT(audit,'NGIND',ng,1,ngind)
    groups=LCMLID(audit,'GROUP',ng)
    do group=1,ng
      group_dir=LCMDIL(groups,group)
      dummy=real(group,real64)*2.0_real64**(-20)
      if ((trim(mode) == 'qfr-type').and.(group == 1)) then
        raw32=real(dummy,real32)
        call LCMPUT(group_dir,'SPOT-M-QFR',nu,2,raw32)
      else
        call LCMPUT(group_dir,'SPOT-M-QFR',nu,4,dummy)
      endif
      if ((trim(mode) == 'eval-type').and.(group == 1)) then
        raw32=real(evaluated(:,group),real32)
        call LCMPUT(group_dir,'SPOT-M-EVAL',nu,2,raw32)
      else
        call LCMPUT(group_dir,'SPOT-M-EVAL',nu,4, &
          evaluated(:,group))
      endif
      if ((trim(mode) == 'src-length').and.(group == 1)) then
        call LCMPUT(group_dir,'SPOT-M-SRC',nu-1,4,dummy(1:nu-1))
      else
        call LCMPUT(group_dir,'SPOT-M-SRC',nu,4,dummy)
      endif
      if ((trim(mode) == 'raw-type').and.(group == 1)) then
        raw32=real(raw(:,group),real32)
        call LCMPUT(group_dir,'SPOT-M-RAW',nu,2,raw32)
      else if ((trim(mode) == 'raw-length').and.(group == 1)) then
        call LCMPUT(group_dir,'SPOT-M-RAW',nu-1,4,raw(1:nu-1,group))
      else
        call LCMPUT(group_dir,'SPOT-M-RAW',nu,4,raw(:,group))
      endif
      one(1)=1
      if ((trim(mode) == 'step-type').and.(group == 1)) then
        raw32(1)=1.0_real32
        call LCMPUT(group_dir,'SPOT-M-STEP',1,2,raw32(1:1))
      else
        call LCMPUT(group_dir,'SPOT-M-STEP',1,1,one)
      endif
      if ((trim(mode) == 'role-length').and.(group == 1)) then
        call LCMPUT(group_dir,'SPOT-M-ROLE',2,1,[1,1])
      else
        call LCMPUT(group_dir,'SPOT-M-ROLE',1,1,one)
      endif
      one(1)=marker(group)
      call LCMPUT(group_dir,'SPOT-M-GROUP',1,1,one)
    enddo
    if (trim(mode) == 'extra') then
      one(1)=17
      call LCMPUT(audit,'EXTRA',1,1,one)
    endif
    call LCMCL(root,1)
  end subroutine write_on

end program make_raw_moc_ulp_bridge_fixture
