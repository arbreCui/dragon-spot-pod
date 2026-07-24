program check_raw_moc_ulp_bridge_xsm
  ! Read-only audit of two distinct binary32 scalar-flux ledgers:
  !
  !   RAW-BRIDGE:
  !     K(RN32_RNE(SPOT-M-RAW)) - K(SPOT-M-EVAL)
  !
  !   PRODUCTION-STEP:
  !     K(OFF/FLUX) - K(PRE/FLUX)
  !
  ! RAW-BRIDGE is a declared direct projection of the captured binary64
  ! response.  It is not an assertion that the production path stores RAW
  ! directly, and the two ledgers are never subtracted or attributed.
  use GANLIB
  use, intrinsic :: ieee_arithmetic
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  implicit none

  integer, parameter :: ng=370
  integer, parameter :: nr=8
  integer, parameter :: nu=14
  integer, parameter :: nstate=40
  integer, parameter :: naudit_state=24
  integer, parameter :: nscalar=ng*nr
  integer, parameter :: nargs=5
  integer, parameter :: max_path=72
  integer, parameter :: max_records=4096
  integer(int64), parameter :: key_zero=2147483648_int64
  integer(int64), parameter :: two23=8388608_int64
  integer(int64), parameter :: two24=16777216_int64
  integer(int64), parameter :: two52=4503599627370496_int64

  type :: track_layout
    integer :: keyflux(nr)=0
  end type track_layout

  type :: flux_state
    real(real32) :: flux(nu,ng)=0.0_real32
  end type flux_state

  type :: audit_state
    real(real64) :: evaluated(nu,ng)=0.0_real64
    real(real64) :: raw(nu,ng)=0.0_real64
  end type audit_state

  type :: ledger_result
    integer(int64) :: step(nscalar)=0_int64
    integer(int64) :: reference_key(nscalar)=0_int64
    integer(int64) :: target_key(nscalar)=0_int64
    integer(int64) :: raw_bits(nscalar)=0_int64
    integer(int32) :: reference_bits(nscalar)=0_int32
    integer(int32) :: target_bits(nscalar)=0_int32
    character(len=24) :: classification(nscalar)=''
    integer(int64) :: unchanged=0_int64
    integer(int64) :: upward=0_int64
    integer(int64) :: downward=0_int64
    integer(int64) :: adjacent=0_int64
    integer(int64) :: raw_exact=0_int64
    integer(int64) :: collapsed_nonzero=0_int64
    integer(int64) :: rounded_zero=0_int64
    integer(int64) :: rounded_subnormal=0_int64
    integer(int64) :: max_steps=-1_int64
  end type ledger_result

  character(len=1024) :: path(nargs),arm_arg
  character(len=10) :: arm_name
  type(track_layout) :: layout
  type(flux_state) :: pre,off
  type(audit_state) :: audit
  type(ledger_result) :: bridge,production
  integer :: arm,i,j,ios

  if (command_argument_count() == 1) then
    call get_command_argument(1,arm_arg)
    if (trim(arm_arg) /= 'SELFTEST') call fail('invalid one-argument mode')
    call self_test()
    write(6,'(A)') 'RAW-MOC-ULP SELFTEST PASS'
    stop
  endif
  if (command_argument_count() /= nargs) &
    call fail('expected TRACK PRE OFF ON ARM')

  do i=1,nargs
    call get_command_argument(i,path(i))
    if (len_trim(path(i)) == 0) call fail('empty argument')
    if ((i < nargs).and.(len_trim(path(i)) > max_path)) &
      call fail('XSM path exceeds Ganlib limit')
    do j=1,i-1
      if ((i < nargs).and.(j < nargs)) then
        if (trim(path(i)) == trim(path(j))) &
          call fail('XSM paths must be distinct')
      endif
    enddo
  enddo
  read(path(nargs),*,iostat=ios) arm
  if ((ios /= 0).or.(arm < 1).or.(arm > 2)) &
    call fail('arm must be 1 or 2')
  if (arm == 1) then
    arm_name='NATIVE'
  else
    arm_name='STATIONARY'
  endif

  call require_ieee_environment()
  call load_track(trim(path(1)),layout)
  call load_flux(trim(path(2)),'PRE',pre)
  call load_flux(trim(path(3)),'OFF',off)
  call load_audit(trim(path(4)),arm,pre,audit)
  call compute_bridge(layout,pre,audit,bridge)
  call compute_production(layout,pre,off,production)
  call print_result(trim(arm_name),layout,bridge,production)

contains

  subroutine require_ieee_environment()
    type(ieee_round_type) :: mode

    if ((storage_size(0.0_real32) /= 32).or. &
        (storage_size(0.0_real64) /= 64).or. &
        (radix(0.0_real32) /= 2).or. &
        (radix(0.0_real64) /= 2).or. &
        (digits(0.0_real32) /= 24).or. &
        (digits(0.0_real64) /= 53).or. &
        (maxexponent(0.0_real32) /= 128).or. &
        (maxexponent(0.0_real64) /= 1024)) &
      call fail('IEEE binary32/binary64 environment differs')
    call ieee_get_rounding_mode(mode)
    if (mode /= ieee_nearest) call fail('rounding mode is not nearest')
  end subroutine require_ieee_environment


  subroutine load_track(xsm_path,data)
    character(len=*), intent(in) :: xsm_path
    type(track_layout), intent(out) :: data
    type(c_ptr) :: root
    integer :: state(nstate)
    character(len=12) :: track_type

    call LCMOP(root,xsm_path,2,2,0)
    call require_signature(root,'L_TRACK','TRACK')
    call require_record(root,'TRACK-TYPE',3,3,'TRACK')
    call LCMGTC(root,'TRACK-TYPE',12,track_type)
    if (trim(track_type) /= 'MCCG') call fail('TRACK is not MCCG')
    call require_record(root,'STATE-VECTOR',nstate,1,'TRACK')
    call LCMGET(root,'STATE-VECTOR',state)
    if ((state(1) /= nr).or.(state(2) /= nu).or. &
        (state(5) /= 6).or.(state(6) /= 1).or.(state(9) == 1)) &
      call fail('TRACK dimensions or MCCG branch differ')
    call require_record(root,'KEYFLX$ANIS',nr,1,'TRACK')
    call LCMGET(root,'KEYFLX$ANIS',data%keyflux)
    if (any(data%keyflux < 1).or.any(data%keyflux > nu).or. &
        has_duplicate(data%keyflux)) call fail('invalid KEYFLX layout')
    call LCMCL(root,1)
  end subroutine load_track


  subroutine load_flux(xsm_path,owner,data)
    character(len=*), intent(in) :: xsm_path,owner
    type(flux_state), intent(out) :: data
    type(c_ptr) :: root,groups
    integer :: state(nstate),group

    call LCMOP(root,xsm_path,2,2,0)
    call require_signature(root,'L_FLUX',owner)
    call require_record(root,'STATE-VECTOR',nstate,1,owner)
    call LCMGET(root,'STATE-VECTOR',state)
    if ((state(1) /= ng).or.(state(2) /= nu).or.(state(3) /= 1)) &
      call fail(trim(owner)//' dimensions or group order differ')
    call require_record(root,'FLUX',ng,10,owner)
    groups=LCMGID(root,'FLUX')
    do group=1,ng
      call require_list_item(groups,group,nu,2,trim(owner)//' FLUX')
      call LCMGDL(groups,group,data%flux(:,group))
    enddo
    if (any(.not.ieee_is_finite(data%flux))) &
      call fail(trim(owner)//' contains nonfinite FLUX')
    call LCMCL(root,1)
  end subroutine load_flux


  subroutine load_audit(xsm_path,arm,pre,data)
    character(len=*), intent(in) :: xsm_path
    integer, intent(in) :: arm
    type(flux_state), intent(in) :: pre
    type(audit_state), intent(out) :: data
    type(c_ptr) :: root,audit,groups,group_dir
    integer :: state(naudit_state),expected(naudit_state)
    integer :: ordered(ng),marker(1),group,unknown
    real(real32) :: evaluated32

    call LCMOP(root,xsm_path,2,2,0)
    call require_signature(root,'L_FLUX','ON')
    call require_record(root,'SPOT-MOC-AUD',-1,0,'ON')
    audit=LCMGID(root,'SPOT-MOC-AUD')
    call require_table_names(audit,[character(len=12) :: &
      'GROUP','NGIND','STATE-VECTOR'],'AUDIT ROOT')
    call require_record(audit,'STATE-VECTOR',naudit_state,1, &
      'AUDIT ROOT')
    call require_record(audit,'NGIND',ng,1,'AUDIT ROOT')
    call require_record(audit,'GROUP',ng,10,'AUDIT ROOT')
    call LCMGET(audit,'STATE-VECTOR',state)
    expected=[1,1,arm,1,1,1,1,1,1,1,1,1,10,1,80,0,0,4,0, &
      ng,ng,nu,nr,ng]
    if (any(state /= expected)) call fail('audit STATE-VECTOR differs')
    call LCMGET(audit,'NGIND',ordered)
    do group=1,ng
      if (ordered(group) /= group) call fail('audit NGIND differs')
    enddo

    groups=LCMGID(audit,'GROUP')
    do group=1,ng
      call require_list_item(groups,group,-1,0,'AUDIT GROUP')
      group_dir=LCMGIL(groups,group)
      call require_table_names(group_dir,[character(len=12) :: &
        'SPOT-M-EVAL','SPOT-M-GROUP','SPOT-M-QFR','SPOT-M-RAW', &
        'SPOT-M-ROLE','SPOT-M-SRC','SPOT-M-STEP'],'AUDIT GROUP')
      call require_record(group_dir,'SPOT-M-EVAL',nu,4, &
        'AUDIT GROUP')
      call require_record(group_dir,'SPOT-M-QFR',nu,4,'AUDIT GROUP')
      call require_record(group_dir,'SPOT-M-RAW',nu,4,'AUDIT GROUP')
      call require_record(group_dir,'SPOT-M-SRC',nu,4,'AUDIT GROUP')
      call require_record(group_dir,'SPOT-M-STEP',1,1,'AUDIT GROUP')
      call require_record(group_dir,'SPOT-M-ROLE',1,1,'AUDIT GROUP')
      call require_record(group_dir,'SPOT-M-GROUP',1,1, &
        'AUDIT GROUP')
      call LCMGET(group_dir,'SPOT-M-EVAL',data%evaluated(:,group))
      call LCMGET(group_dir,'SPOT-M-RAW',data%raw(:,group))
      call LCMGET(group_dir,'SPOT-M-STEP',marker)
      if (marker(1) /= 1) call fail('audit step marker differs')
      call LCMGET(group_dir,'SPOT-M-ROLE',marker)
      if (marker(1) /= 1) call fail('audit role marker differs')
      call LCMGET(group_dir,'SPOT-M-GROUP',marker)
      if (marker(1) /= group) call fail('audit group marker differs')
      if (any(.not.ieee_is_finite(data%evaluated(:,group))).or. &
          any(.not.ieee_is_finite(data%raw(:,group)))) &
        call fail('audit contains nonfinite tuple')
      do unknown=1,nu
        evaluated32=real(data%evaluated(unknown,group),real32)
        if (real64_bits(data%evaluated(unknown,group)) /= &
            real64_bits(real(evaluated32,real64))) &
          call fail('EVAL is not an exact binary32 promotion')
        if (real32_bits(evaluated32) /= &
            real32_bits(pre%flux(unknown,group))) &
          call fail('EVAL differs from PRE')
      enddo
    enddo
    call LCMCL(root,1)
  end subroutine load_audit


  subroutine compute_bridge(layout,pre,audit,result)
    type(track_layout), intent(in) :: layout
    type(flux_state), intent(in) :: pre
    type(audit_state), intent(in) :: audit
    type(ledger_result), intent(out) :: result
    real(real32) :: hardware
    integer(int32) :: reference_bits,target_bits
    integer(int64) :: reference_key,target_key,signed_step
    integer(int64) :: promoted_bits
    integer :: group,region,key,index
    logical :: overflow,is_exact

    index=0
    do group=1,ng
      do region=1,nr
        index=index+1
        key=layout%keyflux(region)
        if ((pre%flux(key,group) <= 0.0_real32).or. &
            (audit%raw(key,group) <= 0.0_real64)) &
          call fail('bridge scalar input is not strictly positive')
        reference_bits=real32_bits(pre%flux(key,group))
        call round_binary64_to_binary32_bits( &
          real64_bits(audit%raw(key,group)),target_bits,overflow)
        if (overflow) call fail('RAW conversion overflow')
        if (btest(target_bits,31)) &
          call fail('positive RAW converted to negative result')
        if (iand(target_bits,int(z'7F800000',int32)) == &
            int(z'7F800000',int32)) &
          call fail('RAW conversion is nonfinite')
        hardware=real(audit%raw(key,group),real32)
        if (real32_bits(hardware) /= target_bits) &
          call fail('software and hardware RNE conversion differ')

        reference_key=ordered_binary32_key(reference_bits)
        target_key=ordered_binary32_key(target_bits)
        signed_step=target_key-reference_key
        promoted_bits=real64_bits(real(pre%flux(key,group),real64))
        is_exact=real64_bits(audit%raw(key,group)) == promoted_bits

        result%raw_bits(index)=real64_bits(audit%raw(key,group))
        result%reference_bits(index)=reference_bits
        result%target_bits(index)=target_bits
        result%reference_key(index)=reference_key
        result%target_key(index)=target_key
        result%step(index)=signed_step
        if (is_exact) then
          result%classification(index)='RAW-EXACT'
          result%raw_exact=result%raw_exact+1_int64
        else if (signed_step == 0_int64) then
          result%classification(index)='ROUND-COLLAPSED-NONZERO'
          result%collapsed_nonzero=result%collapsed_nonzero+1_int64
        else if (signed_step > 0_int64) then
          result%classification(index)='PROJECTED-UP'
        else
          result%classification(index)='PROJECTED-DOWN'
        endif
        call accumulate_step(result,signed_step)
        if (iand(target_bits,int(z'7FFFFFFF',int32)) == 0_int32) &
          result%rounded_zero=result%rounded_zero+1_int64
        if ((iand(target_bits,int(z'7F800000',int32)) == 0_int32).and. &
            (iand(target_bits,int(z'007FFFFF',int32)) /= 0_int32)) &
          result%rounded_subnormal=result%rounded_subnormal+1_int64
      enddo
    enddo
    call require_result_closure(result,index,.true.)
  end subroutine compute_bridge


  subroutine compute_production(layout,pre,off,result)
    type(track_layout), intent(in) :: layout
    type(flux_state), intent(in) :: pre,off
    type(ledger_result), intent(out) :: result
    integer(int32) :: reference_bits,target_bits
    integer(int64) :: reference_key,target_key,signed_step
    integer :: group,region,key,index

    index=0
    do group=1,ng
      do region=1,nr
        index=index+1
        key=layout%keyflux(region)
        if ((pre%flux(key,group) <= 0.0_real32).or. &
            (off%flux(key,group) <= 0.0_real32)) &
          call fail('production scalar is not strictly positive')
        reference_bits=real32_bits(pre%flux(key,group))
        target_bits=real32_bits(off%flux(key,group))
        reference_key=ordered_binary32_key(reference_bits)
        target_key=ordered_binary32_key(target_bits)
        signed_step=target_key-reference_key
        result%reference_bits(index)=reference_bits
        result%target_bits(index)=target_bits
        result%reference_key(index)=reference_key
        result%target_key(index)=target_key
        result%step(index)=signed_step
        call accumulate_step(result,signed_step)
      enddo
    enddo
    call require_result_closure(result,index,.false.)
  end subroutine compute_production


  subroutine accumulate_step(result,signed_step)
    type(ledger_result), intent(inout) :: result
    integer(int64), intent(in) :: signed_step

    if (signed_step == 0_int64) then
      result%unchanged=result%unchanged+1_int64
    else if (signed_step > 0_int64) then
      result%upward=result%upward+1_int64
    else
      result%downward=result%downward+1_int64
    endif
    if (abs(signed_step) == 1_int64) &
      result%adjacent=result%adjacent+1_int64
    result%max_steps=max(result%max_steps,abs(signed_step))
  end subroutine accumulate_step


  subroutine require_result_closure(result,count,is_bridge)
    type(ledger_result), intent(in) :: result
    integer, intent(in) :: count
    logical, intent(in) :: is_bridge

    if (count /= nscalar) call fail('ledger tuple census differs')
    if (result%unchanged+result%upward+result%downward /= count) &
      call fail('ledger direction census does not close')
    if ((result%max_steps < 0_int64).or. &
        (result%adjacent > result%upward+result%downward)) &
      call fail('ledger summary does not close')
    if (is_bridge) then
      if (result%unchanged /= &
          result%raw_exact+result%collapsed_nonzero) &
        call fail('bridge exact/collapsed census does not close')
    endif
  end subroutine require_result_closure


  subroutine print_result(arm,layout,bridge,production)
    character(len=*), intent(in) :: arm
    type(track_layout), intent(in) :: layout
    type(ledger_result), intent(in) :: bridge,production

    write(6,'(A,1X,A)') 'RAW-MOC-ULP ARM',trim(arm)
    write(6,'(A,3(1X,I0))') 'RAW-MOC-ULP DIMS',ng,nr,nu
    write(6,'(A)') &
      'RAW-MOC-ULP ROUNDING IEEE-BINARY64-TO-BINARY32-RNE-ONCE'
    write(6,'(A)') &
      'RAW-MOC-ULP RAW-BRIDGE DECLARED-DIRECT-PROJECTION'
    call print_summary(arm,'RAW-BRIDGE',layout,bridge,.true.)
    call print_bridge_ledger(arm,layout,bridge)
    call print_summary(arm,'PRODUCTION-STEP',layout,production,.false.)
    call print_production_ledger(arm,layout,production)
    write(6,'(A,1X,A,1X,A)') &
      'RAW-MOC-ULP',trim(arm),'LEDGERS NOT-SUBTRACTED'
    write(6,'(A,1X,A,1X,A)') &
      'RAW-MOC-ULP',trim(arm),'ATTRIBUTION NONE'
    write(6,'(A,1X,A,1X,A)') &
      'RAW-MOC-ULP',trim(arm),'ACCEPTANCE-THRESHOLD NONE'
    write(6,'(A,1X,A,1X,A)') &
      'RAW-MOC-ULP',trim(arm),'CLASSIFICATION DESCRIPTIVE-ULP-CENSUS'
    write(6,'(A,1X,A,1X,A)') &
      'RAW-MOC-ULP',trim(arm),'OUTER-CONVERGENCE NOT-EVALUATED'
    write(6,'(A,1X,A,1X,A)') &
      'RAW-MOC-ULP',trim(arm),'STAGE4 NOT-AUTHORIZED'
    write(6,'(A,1X,A,1X,A)') 'RAW-MOC-ULP',trim(arm),'COMPLETE'
  end subroutine print_result


  subroutine print_summary(arm,name,layout,result,is_bridge)
    character(len=*), intent(in) :: arm,name
    type(track_layout), intent(in) :: layout
    type(ledger_result), intent(in) :: result
    logical, intent(in) :: is_bridge
    integer(int64) :: sorted(nscalar)
    integer :: first,last,total,index,group,region

    total=nscalar
    write(6,'(A,2(1X,A),1X,A,1X,I0)') &
      'RAW-MOC-ULP',trim(arm),trim(name),'TOTAL',total
    write(6,'(A,2(1X,A),1X,A,1X,I0)') &
      'RAW-MOC-ULP',trim(arm),trim(name),'UNCHANGED',result%unchanged
    write(6,'(A,2(1X,A),1X,A,1X,I0)') &
      'RAW-MOC-ULP',trim(arm),trim(name),'UPWARD',result%upward
    write(6,'(A,2(1X,A),1X,A,1X,I0)') &
      'RAW-MOC-ULP',trim(arm),trim(name),'DOWNWARD',result%downward
    write(6,'(A,2(1X,A),1X,A,1X,I0)') &
      'RAW-MOC-ULP',trim(arm),trim(name),'ADJACENT',result%adjacent
    if (is_bridge) then
      write(6,'(A,2(1X,A),1X,A,1X,I0)') &
        'RAW-MOC-ULP',trim(arm),trim(name),'RAW-EXACT', &
        result%raw_exact
      write(6,'(A,2(1X,A),1X,A,1X,I0)') &
        'RAW-MOC-ULP',trim(arm),trim(name), &
        'ROUND-COLLAPSED-NONZERO',result%collapsed_nonzero
      write(6,'(A,2(1X,A),1X,A,1X,I0)') &
        'RAW-MOC-ULP',trim(arm),trim(name),'ROUNDED-TO-ZERO', &
        result%rounded_zero
      write(6,'(A,2(1X,A),1X,A,1X,I0)') &
        'RAW-MOC-ULP',trim(arm),trim(name),'ROUNDED-SUBNORMAL', &
        result%rounded_subnormal
    endif
    write(6,'(A,2(1X,A),1X,A,1X,I0)') &
      'RAW-MOC-ULP',trim(arm),trim(name),'MAX-STEPS', &
      result%max_steps

    sorted=result%step
    call sort_int64(sorted)
    first=1
    do while (first <= total)
      last=first
      do while (last < total)
        if (sorted(last+1) /= sorted(first)) exit
        last=last+1
      enddo
      write(6,'(A,2(1X,A),1X,A,2(1X,I0))') &
        'RAW-MOC-ULP',trim(arm),trim(name),'HIST', &
        sorted(first),last-first+1
      first=last+1
    enddo

    index=0
    do group=1,ng
      do region=1,nr
        index=index+1
        if (abs(result%step(index)) == result%max_steps) then
          write(6,'(A,2(1X,A),1X,A,5(1X,I0))') &
            'RAW-MOC-ULP',trim(arm),trim(name),'MAX-TIE', &
            group,region,layout%keyflux(region),result%step(index), &
            abs(result%step(index))
        endif
      enddo
    enddo
  end subroutine print_summary


  subroutine print_bridge_ledger(arm,layout,result)
    character(len=*), intent(in) :: arm
    type(track_layout), intent(in) :: layout
    type(ledger_result), intent(in) :: result
    integer :: group,region,key,index

    index=0
    do group=1,ng
      do region=1,nr
        index=index+1
        key=layout%keyflux(region)
        write(6,'(A,2(1X,A),1X,A,3(1X,I0),1X,Z16.16,2(1X,Z8.8),&
            &4(1X,I0),1X,A)') &
          'RAW-MOC-ULP',trim(arm),'RAW-BRIDGE','LEDGER', &
          group,region,key,result%raw_bits(index), &
          result%reference_bits(index),result%target_bits(index), &
          result%reference_key(index),result%target_key(index), &
          result%step(index),abs(result%step(index)), &
          trim(result%classification(index))
      enddo
    enddo
  end subroutine print_bridge_ledger


  subroutine print_production_ledger(arm,layout,result)
    character(len=*), intent(in) :: arm
    type(track_layout), intent(in) :: layout
    type(ledger_result), intent(in) :: result
    integer :: group,region,key,index

    index=0
    do group=1,ng
      do region=1,nr
        index=index+1
        key=layout%keyflux(region)
        write(6,'(A,2(1X,A),1X,A,3(1X,I0),2(1X,Z8.8),&
            &4(1X,I0))') &
          'RAW-MOC-ULP',trim(arm),'PRODUCTION-STEP','LEDGER', &
          group,region,key,result%reference_bits(index), &
          result%target_bits(index),result%reference_key(index), &
          result%target_key(index),result%step(index), &
          abs(result%step(index))
      enddo
    enddo
  end subroutine print_production_ledger


  subroutine round_binary64_to_binary32_bits(bits64,bits32,overflow)
    integer(int64), intent(in) :: bits64
    integer(int32), intent(out) :: bits32
    logical, intent(out) :: overflow
    integer(int64) :: fraction,significand,rounded,magnitude
    integer :: exponent_field,exponent,output_exponent,shift
    logical :: negative

    negative=btest(bits64,63)
    exponent_field=int(ibits(bits64,52,11))
    fraction=ibits(bits64,0,52)
    overflow=.false.
    magnitude=0_int64

    if (exponent_field == 2047) then
      overflow=.true.
      magnitude=int(z'7F800000',int64)
    else if (exponent_field == 0) then
      magnitude=0_int64
    else
      exponent=exponent_field-1023
      significand=two52+fraction
      if (exponent > 127) then
        overflow=.true.
        magnitude=int(z'7F800000',int64)
      else if (exponent >= -126) then
        rounded=round_shift_right_even(significand,29)
        output_exponent=exponent
        if (rounded == two24) then
          rounded=two23
          output_exponent=output_exponent+1
        endif
        if (output_exponent > 127) then
          overflow=.true.
          magnitude=int(z'7F800000',int64)
        else
          magnitude=int(output_exponent+127,int64)*two23+ &
            (rounded-two23)
        endif
      else
        shift=-exponent-97
        if (shift >= 54) then
          rounded=0_int64
        else
          rounded=round_shift_right_even(significand,shift)
        endif
        if (rounded > two23) call fail('subnormal rounding overflow')
        magnitude=rounded
      endif
    endif

    bits32=int(magnitude,int32)
    if (negative) bits32=ibset(bits32,31)
  end subroutine round_binary64_to_binary32_bits


  pure integer(int64) function round_shift_right_even(value,shift)
    integer(int64), intent(in) :: value
    integer, intent(in) :: shift
    integer(int64) :: quotient,remainder,half,mask

    quotient=shiftr(value,shift)
    mask=shiftl(1_int64,shift)-1_int64
    remainder=iand(value,mask)
    half=shiftl(1_int64,shift-1)
    round_shift_right_even=quotient
    if ((remainder > half).or. &
        ((remainder == half).and.btest(quotient,0))) &
      round_shift_right_even=quotient+1_int64
  end function round_shift_right_even


  pure integer(int64) function ordered_binary32_key(bits)
    integer(int32), intent(in) :: bits
    integer(int64) :: magnitude

    magnitude=int(iand(bits,int(z'7FFFFFFF',int32)),int64)
    if (magnitude == 0_int64) then
      ordered_binary32_key=key_zero
    else if (btest(bits,31)) then
      ordered_binary32_key=key_zero-magnitude
    else
      ordered_binary32_key=key_zero+magnitude
    endif
  end function ordered_binary32_key


  subroutine self_test()
    real(real64) :: tie_down,tie_up,overflow_threshold
    integer(int32) :: bits
    logical :: overflow

    call require_ieee_environment()
    if (real32_bits(1.0_real32) /= int(z'3F800000',int32)) &
      call fail('selftest binary32 one encoding')
    call assert_round(1.0_real64,int(z'3F800000',int32),.false.)
    call assert_round(1.0_real64+2.0_real64**(-25), &
      int(z'3F800000',int32),.false.)
    tie_down=1.0_real64+2.0_real64**(-24)
    call assert_round(tie_down,int(z'3F800000',int32),.false.)
    call assert_round(nearest(tie_down,-1.0_real64), &
      int(z'3F800000',int32),.false.)
    call assert_round(nearest(tie_down,1.0_real64), &
      int(z'3F800001',int32),.false.)
    tie_up=1.0_real64+3.0_real64*2.0_real64**(-24)
    call assert_round(tie_up,int(z'3F800002',int32),.false.)
    call assert_round(scale(1.0_real64,-150),0_int32,.false.)
    call assert_round(3.0_real64*scale(1.0_real64,-150), &
      2_int32,.false.)
    call assert_round(real(transfer(int(z'007FFFFF',int32), &
      0.0_real32),real64),int(z'007FFFFF',int32),.false.)
    call assert_round(real(transfer(int(z'00800000',int32), &
      0.0_real32),real64),int(z'00800000',int32),.false.)
    call assert_round(real(transfer(int(z'7F7FFFFF',int32), &
      0.0_real32),real64),int(z'7F7FFFFF',int32),.false.)
    overflow_threshold=scale(2.0_real64-2.0_real64**(-24),127)
    call assert_round(nearest(overflow_threshold,-1.0_real64), &
      int(z'7F7FFFFF',int32),.false.)
    call round_binary64_to_binary32_bits( &
      real64_bits(overflow_threshold),bits,overflow)
    if ((.not.overflow).or. &
        (bits /= int(z'7F800000',int32))) &
      call fail('selftest conversion overflow')
    if (ordered_binary32_key(int(z'80000000',int32)) /= &
        ordered_binary32_key(0_int32)) &
      call fail('selftest signed zero key')
    if (ordered_binary32_key(int(z'80000001',int32)) /= &
        key_zero-1_int64) call fail('selftest negative minimum key')
    if (ordered_binary32_key(1_int32) /= key_zero+1_int64) &
      call fail('selftest positive minimum key')
    if (ordered_binary32_key(int(z'3F800000',int32))- &
        ordered_binary32_key(int(z'3F7FFFFF',int32)) /= 1_int64) &
      call fail('selftest binade adjacency')
    if (ordered_binary32_key(int(z'00800000',int32))- &
        ordered_binary32_key(int(z'007FFFFF',int32)) /= 1_int64) &
      call fail('selftest subnormal-normal adjacency')
    call self_test_layout()
  end subroutine self_test


  subroutine assert_round(value,expected,expected_overflow)
    real(real64), intent(in) :: value
    integer(int32), intent(in) :: expected
    logical, intent(in) :: expected_overflow
    integer(int32) :: actual
    logical :: overflow

    call round_binary64_to_binary32_bits(real64_bits(value),actual, &
      overflow)
    if ((overflow .neqv. expected_overflow).or.(actual /= expected)) &
      call fail('selftest binary64-to-binary32 RNE')
  end subroutine assert_round


  subroutine self_test_layout()
    type(track_layout) :: layout
    type(flux_state) :: pre,off
    type(audit_state), allocatable :: audit
    type(ledger_result), allocatable :: bridge,production
    integer(int32) :: base_bits,target_bits
    integer(int64) :: expected_step
    integer :: group,region,key,index
    real(real64) :: base64,next64

    allocate(audit,bridge,production)
    layout%keyflux=[8,1,7,2,6,3,5,4]
    pre%flux=1.0_real32
    off%flux=1.0_real32
    audit%evaluated=1.0_real64
    audit%raw=1.0_real64
    do group=1,ng
      do region=1,nr
        key=layout%keyflux(region)
        base_bits=int(z'3F000000',int32)+ &
          int(32*group+key,int32)
        pre%flux(key,group)=transfer(base_bits,0.0_real32)
        audit%evaluated(key,group)= &
          real(pre%flux(key,group),real64)
        expected_step=int(mod(group+2*region,7)-3,int64)
        target_bits=base_bits+int(expected_step,int32)
        if ((expected_step == 0_int64).and. &
            (mod(group+region,2) == 1)) then
          base64=real(pre%flux(key,group),real64)
          next64=real(transfer(base_bits+1_int32, &
            0.0_real32),real64)
          audit%raw(key,group)=base64+(next64-base64)/4.0_real64
        else
          audit%raw(key,group)=real(transfer(target_bits, &
            0.0_real32),real64)
        endif
        expected_step=int(mod(3*group+region,9)-4,int64)
        off%flux(key,group)=transfer(base_bits+ &
          int(expected_step,int32),0.0_real32)
      enddo
    enddo
    call compute_bridge(layout,pre,audit,bridge)
    call compute_production(layout,pre,off,production)
    index=0
    do group=1,ng
      do region=1,nr
        index=index+1
        key=layout%keyflux(region)
        if (bridge%step(index) /= &
            int(mod(group+2*region,7)-3,int64)) &
          call fail('selftest bridge group-region layout')
        if (production%step(index) /= &
            int(mod(3*group+region,9)-4,int64)) &
          call fail('selftest production group-region layout')
        base_bits=int(z'3F000000',int32)+ &
          int(32*group+key,int32)
        if ((bridge%reference_bits(index) /= base_bits).or. &
            (production%reference_bits(index) /= base_bits)) &
          call fail('selftest permuted KEYFLX layout')
      enddo
    enddo
    if ((bridge%collapsed_nonzero <= 0_int64).or. &
        (bridge%raw_exact <= 0_int64)) &
      call fail('selftest exact/collapsed partition')
  end subroutine self_test_layout


  subroutine sort_int64(values)
    integer(int64), intent(inout) :: values(:)
    integer(int64) :: held
    integer :: i,j

    do i=2,size(values)
      held=values(i)
      j=i-1
      do while (j >= 1)
        if (values(j) <= held) exit
        values(j+1)=values(j)
        j=j-1
      enddo
      values(j+1)=held
    enddo
  end subroutine sort_int64


  pure elemental integer(int32) function real32_bits(value)
    real(real32), intent(in) :: value

    real32_bits=transfer(value,0_int32)
  end function real32_bits


  pure elemental integer(int64) function real64_bits(value)
    real(real64), intent(in) :: value

    real64_bits=transfer(value,0_int64)
  end function real64_bits


  pure logical function has_duplicate(values)
    integer, intent(in) :: values(:)
    integer :: i

    has_duplicate=.false.
    do i=1,size(values)
      if (count(values == values(i)) /= 1) then
        has_duplicate=.true.
        return
      endif
    enddo
  end function has_duplicate


  subroutine require_table_names(table,expected,owner)
    type(c_ptr), intent(in) :: table
    character(len=12), intent(in) :: expected(:)
    character(len=*), intent(in) :: owner
    character(len=12) :: found(max_records)
    character(len=12) :: sorted_expected(size(expected))
    integer :: count

    call collect_names(table,found,count)
    sorted_expected=expected
    call sort_small_names(sorted_expected)
    if (count /= size(expected)) call fail(trim(owner)//' census differs')
    if (any(found(1:count) /= sorted_expected)) &
      call fail(trim(owner)//' names differ')
  end subroutine require_table_names


  subroutine collect_names(table,names,count)
    type(c_ptr), intent(in) :: table
    character(len=12), intent(out) :: names(max_records)
    integer, intent(out) :: count
    character(len=12) :: name,first

    names=' '
    count=0
    name=' '
    call LCMNXT(table,name)
    if (name == ' ') return
    first=name
    do
      count=count+1
      if (count > max_records) call fail('too many table records')
      names(count)=name
      call LCMNXT(table,name)
      if (name == first) exit
    enddo
    call sort_small_names(names(1:count))
  end subroutine collect_names


  subroutine sort_small_names(names)
    character(len=12), intent(inout) :: names(:)
    character(len=12) :: held
    integer :: i,j

    do i=2,size(names)
      held=names(i)
      j=i-1
      do while (j >= 1)
        if (names(j) <= held) exit
        names(j+1)=names(j)
        j=j-1
      enddo
      names(j+1)=held
    enddo
  end subroutine sort_small_names


  subroutine require_signature(ptr,expected,owner)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: expected,owner
    character(len=12) :: signature

    call require_record(ptr,'SIGNATURE',3,3,owner)
    call LCMGTC(ptr,'SIGNATURE',12,signature)
    if (signature /= expected) &
      call fail(trim(owner)//' signature differs')
  end subroutine require_signature


  subroutine require_record(ptr,name,length_expected,type_expected,owner)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,owner
    integer, intent(in) :: length_expected,type_expected
    integer :: length_found,type_found

    call LCMLEN(ptr,name,length_found,type_found)
    if ((length_found /= length_expected).or. &
        (type_found /= type_expected)) then
      write(0,'(A,1X,A,4(1X,I0))') trim(owner)//' invalid record', &
        trim(name),length_found,type_found,length_expected,type_expected
      call fail('record contract failure')
    endif
  end subroutine require_record


  subroutine require_list_item(ptr,index,length_expected,type_expected, &
      owner)
    type(c_ptr), intent(in) :: ptr
    integer, intent(in) :: index,length_expected,type_expected
    character(len=*), intent(in) :: owner
    integer :: length_found,type_found

    call LCMLEL(ptr,index,length_found,type_found)
    if ((type_found /= type_expected).or. &
        (length_found /= length_expected)) then
      write(0,'(A,1X,I0,4(1X,I0))') &
        trim(owner)//' invalid list item',index,length_found,type_found, &
        length_expected,type_expected
      call fail('list item contract failure')
    endif
  end subroutine require_list_item


  subroutine fail(message)
    character(len=*), intent(in) :: message

    write(0,'(A)') 'RAW-MOC-ULP ERROR: '//trim(message)
    error stop 1
  end subroutine fail

end program check_raw_moc_ulp_bridge_xsm
