program make_raw_moc_capture_fixture
  use GANLIB
  use SPOMOC_AUDIT
  use, intrinsic :: iso_c_binding, only: c_ptr
  use, intrinsic :: iso_fortran_env, only: real32, real64
  implicit none

  integer, parameter :: ng = 370
  integer, parameter :: nr = 8
  integer, parameter :: ns = 6
  integer, parameter :: nu = 14
  integer, parameter :: nstate = 40
  integer, parameter :: nmix = 4
  integer, parameter :: nalbedo = 2
  character(len=1024) :: outdir, arm_arg, mode
  character(len=1024) :: track_path, system_path, pre_path
  character(len=1024) :: frozen_path, off_path, on_path
  integer :: arm, ios, group, unknown, region, surface, key, coupled, mix
  integer :: ngind(ng), keyflux(nr), keycur(ns), ibc(ns), nzon(nu)
  integer :: icode(ns)
  logical :: nconv(ng)
  real(real32) :: volume(nr), track_albedo(ns)
  real(real32) :: s0(0:nmix, ng), group_albedo(nalbedo, ng)
  real(real32) :: qfr(nu, ng), evaluated(nu, ng), captured_eval(nu, ng)
  real(real32) :: post(nu, ng), product32, sum32, effective_albedo
  real(real64) :: source(nu, ng), raw(nu, ng)
  real(real32) :: epsilon
  type(c_ptr) :: on

  if (command_argument_count() /= 3) &
       error stop 'expected OUTDIR ARM MODE'
  call get_command_argument(1, outdir)
  call get_command_argument(2, arm_arg)
  call get_command_argument(3, mode)
  read(arm_arg, *, iostat=ios) arm
  if ((ios /= 0) .or. (arm < 1) .or. (arm > 2)) &
       error stop 'arm must be 1 or 2'

  track_path = trim(outdir)//'/track.xsm'
  system_path = trim(outdir)//'/system.xsm'
  pre_path = trim(outdir)//'/pre.xsm'
  frozen_path = trim(outdir)//'/frozen.xsm'
  off_path = trim(outdir)//'/off.xsm'
  on_path = trim(outdir)//'/on.xsm'
  if (max(len_trim(track_path), len_trim(system_path), len_trim(pre_path), &
       len_trim(frozen_path), len_trim(off_path), len_trim(on_path)) > 72) &
       error stop 'fixture path exceeds Ganlib limit'

  keyflux = [8, 1, 7, 2, 6, 3, 5, 4]
  keycur = [14, 9, 13, 10, 12, 11]
  ibc = [2, 1, 4, 3, 6, 5]
  nzon(1:nr) = [1, 2, 3, 4, 1, 2, 3, 4]
  nzon(nr+1:nu) = [-1, -2, -3, -4, -5, -6]
  icode = [1, 0, 2, 0, 1, 2]
  volume = [1.25_real32, 2.5_real32, 3.75_real32, 5.0_real32, &
       6.25_real32, 7.5_real32, 8.75_real32, 10.0_real32]
  track_albedo = [0.125_real32, 0.25_real32, 0.375_real32, &
       0.5_real32, 0.625_real32, 0.75_real32]

  do group = 1, ng
    ngind(group) = group
    nconv(group) = .true.
    s0(0, group) = 0.0_real32
    do mix = 1, nmix
      s0(mix, group) = real(5*group + 3*mix, real32) * &
           2.0_real32**(-22)
    end do
    group_albedo(1, group) = 0.2_real32 + &
         real(mod(group, 7), real32) * 2.0_real32**(-10)
    group_albedo(2, group) = 0.7_real32 - &
         real(mod(group, 11), real32) * 2.0_real32**(-11)
    do unknown = 1, nu
      qfr(unknown, group) = real(2000 + 17*group + unknown, real32) * &
           2.0_real32**(-20)
      evaluated(unknown, group) = &
           real(4000 + 19*group + 3*unknown, real32) * &
           2.0_real32**(-19)
    end do
  end do

  source = 0.0_real64
  do group = 1, ng
    do region = 1, nr
      key = keyflux(region)
      mix = nzon(region)
      product32 = s0(mix, group) * evaluated(key, group)
      sum32 = qfr(key, group) + product32
      source(key, group) = real(sum32, real64)
    end do
    do surface = 1, ns
      key = keycur(surface)
      coupled = keycur(ibc(surface))
      effective_albedo = track_albedo(surface)
      if (icode(surface) > 0) &
           effective_albedo = group_albedo(icode(surface), group)
      product32 = effective_albedo * evaluated(coupled, group)
      source(key, group) = real(product32, real64)
    end do
  end do
  do group = 1, ng
    do unknown = 1, nu
      raw(unknown, group) = real(evaluated(unknown, group), real64) + &
           real(37*group + 5*unknown, real64) * 2.0_real64**(-42)
      post(unknown, group) = real(raw(unknown, group), real32)
    end do
  end do

  captured_eval = evaluated
  select case (trim(mode))
  case ('valid', 'status', 'extra', 'non-audit', 'raw')
    continue
  case ('eval')
    captured_eval(1, 1) = nearest(captured_eval(1, 1), 1.0_real32)
  case ('source')
    source(1, 1) = nearest(source(1, 1), 1.0_real64)
  case default
    error stop 'unknown fixture mode'
  end select
  if (trim(mode) == 'raw') raw(1, 1) = nearest(raw(1, 1), 1.0_real64)

  call write_track(trim(track_path), keyflux, keycur, ibc, nzon, &
       volume, icode, track_albedo)
  call write_system(trim(system_path), s0, group_albedo)
  call write_flux(trim(pre_path), evaluated)
  call write_flux(trim(frozen_path), post)
  call write_flux(trim(off_path), post)
  call write_flux(trim(on_path), post)

  call LCMOP(on, trim(on_path), 1, 2, 0)
  epsilon = 2.5e-7_real32
  call SPOMOC_BEGIN(on, arm, 'MCCG', 0, ng, nu, nr, 1, 740, epsilon, &
       epsilon, epsilon, .true., 0, .true., 1, 1, 0)
  call SPOMOC_FLU_PATH(.false.)
  call SPOMOC_FLU_CONTEXT(1, 1)
  call SPOMOC_DOOR_BEGIN()
  call SPOMOC_MCCGF_BEGIN(ng, ng, ngind, nu, 2, .false., nu, nr, ns, &
       1, 1, 1, 10, 1, 80, 0, 0, 4, 0)
  call SPOMOC_SET_ROLE(1, 1)
  call SPOMOC_CAPTURE(ng, ngind, nu, qfr, captured_eval, source, raw, &
       nconv)
  call SPOMOC_PUBLISH()
  call SPOMOC_FINISH()
  call apply_tamper(on, trim(mode))
  call LCMCL(on, 1)

contains

  subroutine write_track(path, keyflux, keycur, ibc, nzon, volume, &
       icode, albedo)
    character(len=*), intent(in) :: path
    integer, intent(in) :: keyflux(nr), keycur(ns), ibc(ns), nzon(nu)
    integer, intent(in) :: icode(ns)
    real(real32), intent(in) :: volume(nr), albedo(ns)
    type(c_ptr) :: root
    integer :: state(nstate)
    character(len=12) :: text

    call LCMOP(root, path, 0, 2, 0)
    text = 'L_TRACK'
    call LCMPTC(root, 'SIGNATURE', 12, text)
    text = 'MCCG'
    call LCMPTC(root, 'TRACK-TYPE', 12, text)
    state = 0
    state(1) = nr
    state(2) = nu
    state(5) = ns
    state(6) = 1
    state(9) = 0
    call LCMPUT(root, 'STATE-VECTOR', nstate, 1, state)
    call LCMPUT(root, 'KEYFLX$ANIS', nr, 1, keyflux)
    call LCMPUT(root, 'KEYCUR$MCCG', ns, 1, keycur)
    call LCMPUT(root, 'BC-REFL+TRAN', ns, 1, ibc)
    call LCMPUT(root, 'NZON$MCCG', nu, 1, nzon)
    call LCMPUT(root, 'VOLUME', nr, 2, volume)
    call LCMPUT(root, 'ICODE', ns, 1, icode)
    call LCMPUT(root, 'ALBEDO', ns, 2, albedo)
    call LCMCL(root, 1)
  end subroutine write_track


  subroutine write_system(path, s0, albedo)
    character(len=*), intent(in) :: path
    real(real32), intent(in) :: s0(0:nmix, ng)
    real(real32), intent(in) :: albedo(nalbedo, ng)
    type(c_ptr) :: root, groups, group_dir
    real(real32) :: tx(0:nmix)
    character(len=12) :: text
    integer :: group, mix

    call LCMOP(root, path, 0, 2, 0)
    text = 'L_PIJ'
    call LCMPTC(root, 'SIGNATURE', 12, text)
    groups = LCMLID(root, 'GROUP', ng)
    do group = 1, ng
      group_dir = LCMDIL(groups, group)
      do mix = 0, nmix
        tx(mix) = real(100 + 2*group + mix, real32) * 2.0_real32**(-16)
      end do
      call LCMPUT(group_dir, 'DRAGON-S0XSC', nmix + 1, 2, s0(:, group))
      call LCMPUT(group_dir, 'DRAGON-TXSC', nmix + 1, 2, tx)
      call LCMPUT(group_dir, 'ALBEDO', nalbedo, 2, albedo(:, group))
    end do
    call LCMCL(root, 1)
  end subroutine write_system


  subroutine write_flux(path, flux)
    character(len=*), intent(in) :: path
    real(real32), intent(in) :: flux(nu, ng)
    type(c_ptr) :: root, flux_list, source_list, sentinel
    integer :: state(nstate), group
    integer :: base_int(3)
    real(real32) :: source_vector(nu), base_real(2)
    real(real64) :: base_double(2)
    character(len=12) :: text

    call LCMOP(root, path, 0, 2, 0)
    text = 'L_FLUX'
    call LCMPTC(root, 'SIGNATURE', 12, text)
    state = 0
    state(1) = ng
    state(2) = nu
    state(3) = 1
    state(6) = 0
    call LCMPUT(root, 'STATE-VECTOR', nstate, 1, state)
    flux_list = LCMLID(root, 'FLUX', ng)
    source_list = LCMLID(root, 'SOUR', ng)
    do group = 1, ng
      source_vector = real(group, real32) * 2.0_real32**(-18)
      call LCMPDL(flux_list, group, nu, 2, flux(:, group))
      call LCMPDL(source_list, group, nu, 2, source_vector)
    end do
    sentinel = LCMDID(root, 'SENTINEL')
    base_int = [17, 23, 31]
    base_real = [0.125_real32, -0.375_real32]
    base_double = [1.0_real64 / 3.0_real64, -7.0_real64 / 11.0_real64]
    call LCMPUT(sentinel, 'BASE-INT', 3, 1, base_int)
    call LCMPUT(sentinel, 'BASE-REAL', 2, 2, base_real)
    call LCMPUT(sentinel, 'BASE-DOUBLE', 2, 4, base_double)
    call LCMCL(root, 1)
  end subroutine write_flux


  subroutine apply_tamper(root, mode)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: mode
    type(c_ptr) :: audit, sentinel
    integer :: state(24), extra(1), base_int(3)

    select case (trim(mode))
    case ('valid', 'eval', 'source', 'raw')
      return
    case ('status')
      audit = LCMDID(root, 'SPOT-MOC-AUD')
      call LCMGET(audit, 'STATE-VECTOR', state)
      state(2) = 0
      call LCMPUT(audit, 'STATE-VECTOR', 24, 1, state)
    case ('extra')
      audit = LCMDID(root, 'SPOT-MOC-AUD')
      extra(1) = 1
      call LCMPUT(audit, 'EXTRA', 1, 1, extra)
    case ('non-audit')
      sentinel = LCMDID(root, 'SENTINEL')
      call LCMGET(sentinel, 'BASE-INT', base_int)
      base_int(2) = base_int(2) + 1
      call LCMPUT(sentinel, 'BASE-INT', 3, 1, base_int)
    end select
  end subroutine apply_tamper

end program make_raw_moc_capture_fixture
