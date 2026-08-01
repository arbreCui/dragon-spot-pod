module GANLIB
  use, intrinsic :: iso_c_binding, only : c_ptr, c_associated
  implicit none
  private
  public :: c_ptr, LCMGET, LCMLEN

  interface LCMGET
    module procedure LCMGET_I1
    module procedure LCMGET_R0
    module procedure LCMGET_R1
  end interface LCMGET

contains

  subroutine LCMGET_I1(ip, name, values)
    type(c_ptr), intent(in) :: ip
    character(len=*), intent(in) :: name
    integer, intent(out) :: values(:)

    if (c_associated(ip)) continue
    values = 0
    select case (name)
    case ('STATE-VECTOR')
      if (size(values) < 18) error stop 'short synthetic STATE-VECTOR'
      values(6) = 0
      values(7) = 0
      values(8) = 3
      values(9) = 3
      values(10) = 1
      values(12) = 4
      values(18) = 1
    case ('IMERGE-LEAK')
      values = 1
    case default
      error stop 'unexpected synthetic integer LCMGET'
    end select
  end subroutine LCMGET_I1

  subroutine LCMGET_R0(ip, name, value)
    type(c_ptr), intent(in) :: ip
    character(len=*), intent(in) :: name
    real, intent(out) :: value

    if (c_associated(ip)) continue
    if ((name /= 'B2  B1HOM')) error stop 'unexpected scalar LCMGET'
    value = 0.0
  end subroutine LCMGET_R0

  subroutine LCMGET_R1(ip, name, values)
    type(c_ptr), intent(in) :: ip
    character(len=*), intent(in) :: name
    real, intent(out) :: values(:)

    if (c_associated(ip)) continue
    values = 0.0
    select case (name)
    case ('EPS-CONVERGE')
      if (size(values) < 5) error stop 'short synthetic EPS-CONVERGE'
      values(1:3) = 1.0e-5
    case ('B2  HETE')
      continue
    case default
      error stop 'unexpected synthetic real LCMGET'
    end select
  end subroutine LCMGET_R1

  subroutine LCMLEN(ip, name, length, lcm_type)
    type(c_ptr), intent(in) :: ip
    character(len=*), intent(in) :: name
    integer, intent(out) :: length, lcm_type

    if (c_associated(ip)) continue
    if ((name /= 'B2  HETE') .and. (name /= 'B2  B1HOM')) then
      error stop 'unexpected synthetic LCMLEN'
    end if
    length = 0
    lcm_type = 99
  end subroutine LCMLEN

end module GANLIB
