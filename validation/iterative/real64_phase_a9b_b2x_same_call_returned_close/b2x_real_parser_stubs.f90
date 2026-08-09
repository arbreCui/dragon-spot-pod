module B2X_REAL_PARSER_PROBES
  use, intrinsic :: iso_fortran_env, only : int32
  implicit none
  private

  integer, public :: total_redget_calls=0
  integer, public :: total_redput_calls=0
  integer, public :: xabort_calls=0
  integer(int32), public :: returned_error_bits=0_int32
  character(len=131), public :: last_abort=' '
  logical, public :: allow_abort=.false.
  integer :: parser_position=0

  public :: B2X_RESET_FULL_PARSER, B2X_START_ADAPTER_PARSE
  public :: B2X_START_SPOLEAK_PARSE, B2X_NEXT_TOKEN

contains

  subroutine B2X_RESET_FULL_PARSER()
    total_redget_calls=0
    total_redput_calls=0
    xabort_calls=0
    returned_error_bits=0_int32
    last_abort=' '
    allow_abort=.false.
    parser_position=0
  end subroutine B2X_RESET_FULL_PARSER


  subroutine B2X_START_ADAPTER_PARSE(capture_abort)
    logical, intent(in) :: capture_abort
    parser_position=2
    xabort_calls=0
    last_abort=' '
    allow_abort=capture_abort
  end subroutine B2X_START_ADAPTER_PARSE


  subroutine B2X_START_SPOLEAK_PARSE()
    parser_position=0
    xabort_calls=0
    last_abort=' '
    allow_abort=.false.
  end subroutine B2X_START_SPOLEAK_PARSE


  subroutine B2X_NEXT_TOKEN(indic,text)
    integer, intent(out) :: indic
    character(len=*), intent(out) :: text

    total_redget_calls=total_redget_calls+1
    select case(parser_position)
    case(0)
      indic=-2
      text=' '
    case default
      indic=3
      text=';'
    end select
    parser_position=parser_position+1
  end subroutine B2X_NEXT_TOKEN

end module B2X_REAL_PARSER_PROBES


subroutine REDGET(indic,nitma,flott,text,dflott)
  use B2X_REAL_PARSER_PROBES, only : B2X_NEXT_TOKEN
  implicit none
  integer :: indic, nitma
  real :: flott
  character(len=*) :: text
  double precision :: dflott

  nitma=0
  flott=0.0
  dflott=0.0d0
  call B2X_NEXT_TOKEN(indic,text)
end subroutine REDGET


subroutine REDPUT(indic,nitma,flott,text,dflott)
  use B2X_REAL_PARSER_PROBES, only : returned_error_bits, &
      total_redput_calls
  use, intrinsic :: iso_fortran_env, only : int32
  implicit none
  integer :: indic, nitma
  real :: flott
  character(len=*) :: text
  double precision :: dflott

  if (indic /= 2) error stop 'B2X real REDPUT type differs'
  total_redput_calls=total_redput_calls+1
  returned_error_bits=transfer(flott,0_int32)
  nitma=0
  text=' '
  dflott=0.0d0
end subroutine REDPUT


subroutine XABORT(message)
  use B2X_REAL_PARSER_PROBES, only : allow_abort, last_abort, xabort_calls
  implicit none
  character(len=*) :: message

  if (.not. allow_abort) then
    write(*,'(A)') 'unexpected B2X XABORT: '//trim(message)
    error stop 'unexpected B2X XABORT'
  end if
  xabort_calls=xabort_calls+1
  last_abort=trim(message)
end subroutine XABORT
