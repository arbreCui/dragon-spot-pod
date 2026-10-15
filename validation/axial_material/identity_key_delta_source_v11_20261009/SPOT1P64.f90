module SPOT1P64_CACHE_MOD
  use, intrinsic :: iso_fortran_env, only: int32,int64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  private

  type, public :: SPOT1P64_MODE_PLAN
    logical :: ready=.false.
    integer(int64) :: rank1_factor_bytes=0_int64
    integer(int64), allocatable :: rank1_raw_bits(:),rank1_operator_bits(:)
    ! bits stores either the original full key or only differing values.
    ! Allocated positions (including length zero) selects the delta format.
    integer(int64) :: rank1_raw_size=0_int64,rank1_operator_size=0_int64
    integer(int32), allocatable :: rank1_raw_positions(:),rank1_operator_positions(:)
    integer :: nstate=0
    integer :: nblock=0
    double precision, allocatable :: lower(:,:,:)
    integer :: rank1_lower_rows_count=0
    integer :: rank1_lower_unique_count=0
    integer, allocatable :: rank1_lower_blocks(:)
    integer, allocatable :: rank1_lower_rows(:)
    double precision, allocatable :: rank1_lower(:,:,:)
    double precision, allocatable :: factor(:,:,:)
    double precision, allocatable :: pivot_value(:,:)
    double precision, allocatable :: cprime(:,:,:)
    integer, allocatable :: pivot(:,:)
  end type SPOT1P64_MODE_PLAN

  type, public :: SPOT1P64_GROUP_PLAN
    type(SPOT1P64_MODE_PLAN), allocatable :: mode(:)
  end type SPOT1P64_GROUP_PLAN

  type(SPOT1P64_GROUP_PLAN), allocatable, save, public :: SPOT1P64_PLAN(:)
  logical, save :: cache_enabled=.false.
  integer, save :: factorized_blocks=0
  integer, save :: reused_blocks=0

  ! Separate ordinary-rank1 lifecycle; never changes the legacy enable flag.
  logical, save :: rank1_enabled=.false.
  integer(int64), parameter :: RANK1_CAP=536870912_int64
  integer(int64), parameter :: RANK1_DESCRIPTOR_PER_GROUP=4096_int64
  integer(int64), save :: rank1_bytes=0_int64,rank1_peak=0_int64
  integer(int64), save :: rank1_builds=0_int64,rank1_reuses=0_int64
  integer(int64), save :: rank1_validated_hits=0_int64
  ! Owners refer only to the first full key of each phase in this lifecycle.
  integer, save :: rank1_raw_base_owner=0,rank1_operator_base_owner=0
  public :: SPOT1P64_RANK1_ENABLED,SPOT1P64_RANK1_RESERVE
  public :: SPOT1P64_RANK1_RELEASE,SPOT1P64_RANK1_GUARD
  public :: SPOT1P64_RANK1_KEY_LOAD,SPOT1P64_RANK1_KEY_STATS
  public :: SPOT1P64_RANK1_FACTORS,SPOT1P64_RANK1_STATS
  public :: SPOT1P64_RANK1_TERMINAL,SPOT1P64_RANK1_PROGRESS

  public :: SPOT1P64_CACHE_BEGIN,SPOT1P64_CACHE_CLEAR
  public :: SPOT1P64_CACHE_PREPARE,SPOT1P64_CACHE_NOTE_BUILD
  public :: SPOT1P64_CACHE_NOTE_REUSE,SPOT1P64_CACHE_STATS
  public :: SPOT1P64_FACTOR64,SPOT1P64_SOLVE64
  public :: SPOT1P64_RANK1_LOWER_STORE,SPOT1P64_RANK1_LOWER_VALIDATE
  public :: SPOT1P64_RANK1_LOWER_LOAD
  public :: SPOT1P64_RANK1_FACTOR_PACK,SPOT1P64_RANK1_FACTOR_LOAD

contains

  subroutine SPOT1P64_CACHE_BEGIN(ngroup,enable,enable_rank1)
    integer, intent(in) :: ngroup
    logical, intent(in) :: enable
    logical, optional, intent(in) :: enable_rank1
    call SPOT1P64_CACHE_CLEAR()
    if (present(enable_rank1)) rank1_enabled=enable_rank1.and.(.not.enable)
    if (.not.enable.and..not.rank1_enabled) return
    if (ngroup <= 0) call XABORT('SPOT1P64 CACHE: INVALID GROUP COUNT.')
    if (rank1_enabled) then
      if (storage_size(0) /= 32 .or. storage_size(0.0) /= 32 .or. &
          storage_size(0.0d0) /= 64 .or. storage_size(0_int64) /= 64) &
        call XABORT('SPOT1P64 RANK1 CACHE: UNSUPPORTED ELEMENT ABI.')
      if (ngroup > 370) &
        call XABORT('SPOT1P64 RANK1 CACHE: GROUP COUNT EXCEEDS DECLARED 370.')
      call SPOT1P64_RANK1_RESERVE(int(ngroup,int64)*RANK1_DESCRIPTOR_PER_GROUP)
    endif
    allocate(SPOT1P64_PLAN(ngroup))
    cache_enabled=enable
  end subroutine SPOT1P64_CACHE_BEGIN

  subroutine SPOT1P64_CACHE_CLEAR()
    if (allocated(SPOT1P64_PLAN)) deallocate(SPOT1P64_PLAN)
    cache_enabled=.false.
    factorized_blocks=0
    reused_blocks=0
    rank1_enabled=.false.
    rank1_bytes=0_int64
    rank1_peak=0_int64
    rank1_builds=0_int64
    rank1_reuses=0_int64
    rank1_validated_hits=0_int64
    rank1_raw_base_owner=0
    rank1_operator_base_owner=0
  end subroutine SPOT1P64_CACHE_CLEAR

  subroutine SPOT1P64_CACHE_PREPARE(igroup,nmode,active)
    integer, intent(in) :: igroup,nmode
    logical, intent(out) :: active
    active=.false.
    if (.not.cache_enabled) return
    if (.not.allocated(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 CACHE: MISSING FLU LIFECYCLE.')
    if (igroup < 1 .or. igroup > size(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 CACHE: INVALID ENERGY GROUP.')
    if (.not.allocated(SPOT1P64_PLAN(igroup)%mode)) then
      allocate(SPOT1P64_PLAN(igroup)%mode(nmode))
    else if (size(SPOT1P64_PLAN(igroup)%mode) /= nmode) then
      call XABORT('SPOT1P64 CACHE: MODE COUNT CHANGED INSIDE FLU.')
    endif
    active=.true.
  end subroutine SPOT1P64_CACHE_PREPARE

  subroutine SPOT1P64_CACHE_NOTE_BUILD(nblock)
    integer, intent(in) :: nblock
    if (rank1_enabled) then
      rank1_builds=rank1_builds+int(nblock,int64)
    else
    factorized_blocks=factorized_blocks+nblock
    endif
  end subroutine SPOT1P64_CACHE_NOTE_BUILD

  subroutine SPOT1P64_CACHE_NOTE_REUSE(nblock)
    integer, intent(in) :: nblock
    if (rank1_enabled) then
      rank1_reuses=rank1_reuses+int(nblock,int64)
    else
    reused_blocks=reused_blocks+nblock
    endif
  end subroutine SPOT1P64_CACHE_NOTE_REUSE

  subroutine SPOT1P64_CACHE_STATS(nfactor,nreuse)
    integer, intent(out) :: nfactor,nreuse
    nfactor=factorized_blocks
    nreuse=reused_blocks
  end subroutine SPOT1P64_CACHE_STATS

  ! Split ALSBD's pivoted elimination from its right-hand-side work while
  ! preserving its pivot rule and each finite column's scalar arithmetic
  ! order.  The factor is valid only for exact reuse of the same matrix.
  subroutine SPOT1P64_FACTOR64(matrix,pivot,pivot_value,info)
    double precision, intent(inout) :: matrix(:,:)
    integer, intent(out) :: pivot(:),info
    double precision, intent(out) :: pivot_value(:)
    integer :: n,jcol,i,j,pivot_row
    double precision :: test,per

    n=size(matrix,1)
    if (size(matrix,2) /= n .or. size(pivot) /= n .or. &
        size(pivot_value) /= n) &
      call XABORT('SPOT1P64 FACTOR: INVALID DIMENSIONS.')
    info=0
    pivot=0
    pivot_value=0.0d0
    if (n == 1) then
      pivot(1)=1
      pivot_value(1)=matrix(1,1)
      if (pivot_value(1) == 0.0d0) info=1
      return
    endif

    do jcol=1,n-1
      test=0.0d0
      pivot_row=0
      do i=jcol,n
        if (abs(matrix(i,jcol)) <= test) cycle
        test=abs(matrix(i,jcol))
        pivot_row=i
      enddo
      if (test == 0.0d0) then
        info=1
        return
      endif
      pivot(jcol)=pivot_row
      pivot_value(jcol)=matrix(pivot_row,jcol)
      matrix(pivot_row,jcol)=matrix(jcol,jcol)
      do j=jcol+1,n
        per=matrix(pivot_row,j)/pivot_value(jcol)
        matrix(pivot_row,j)=matrix(jcol,j)
        matrix(jcol,j)=per
        do i=jcol+1,n
          matrix(i,j)=matrix(i,j)-matrix(i,jcol)*per
        enddo
      enddo
    enddo
    pivot(n)=n
    pivot_value(n)=matrix(n,n)
    if (pivot_value(n) == 0.0d0) info=1
  end subroutine SPOT1P64_FACTOR64

  subroutine SPOT1P64_SOLVE64(factor,pivot,pivot_value,rhs,info)
    double precision, intent(in) :: factor(:,:),pivot_value(:)
    integer, intent(in) :: pivot(:)
    double precision, intent(inout) :: rhs(:,:)
    integer, intent(out) :: info
    integer :: n,nrhs,jcol,j,i,k,pivot_row,iback
    double precision :: per

    n=size(factor,1)
    nrhs=size(rhs,2)
    if (size(factor,2) /= n .or. size(rhs,1) /= n .or. &
        size(pivot) /= n .or. size(pivot_value) /= n) &
      call XABORT('SPOT1P64 SOLVE: INVALID DIMENSIONS.')
    info=0
    if (n == 1) then
      if (pivot_value(1) == 0.0d0) then
        info=1
        return
      endif
      do j=1,nrhs
        rhs(1,j)=rhs(1,j)/pivot_value(1)
      enddo
      return
    endif

    do jcol=1,n-1
      pivot_row=pivot(jcol)
      if (pivot_row < jcol .or. pivot_row > n .or. &
          pivot_value(jcol) == 0.0d0) then
        info=1
        return
      endif
      do j=1,nrhs
        per=rhs(pivot_row,j)/pivot_value(jcol)
        rhs(pivot_row,j)=rhs(jcol,j)
        rhs(jcol,j)=per
        do i=jcol+1,n
          rhs(i,j)=rhs(i,j)-factor(i,jcol)*per
        enddo
      enddo
    enddo
    if (pivot_value(n) == 0.0d0) then
      info=1
      return
    endif
    do j=1,nrhs
      rhs(n,j)=rhs(n,j)/pivot_value(n)
    enddo
    do iback=2,n
      i=n-iback+1
      do j=1,nrhs
        per=rhs(i,j)
        do k=i+1,n
          per=per-factor(i,k)*rhs(k,j)
        enddo
        rhs(i,j)=per
      enddo
    enddo
  end subroutine SPOT1P64_SOLVE64


  logical function SPOT1P64_RANK1_ENABLED()
    SPOT1P64_RANK1_ENABLED=rank1_enabled
  end function SPOT1P64_RANK1_ENABLED

  subroutine SPOT1P64_RANK1_RESERVE(amount)
    integer(int64), intent(in) :: amount
    if (amount < 0_int64 .or. amount > RANK1_CAP-rank1_bytes) &
      call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
    rank1_bytes=rank1_bytes+amount
    rank1_peak=max(rank1_peak,rank1_bytes)
  end subroutine SPOT1P64_RANK1_RESERVE

  subroutine SPOT1P64_RANK1_RELEASE(amount)
    integer(int64), intent(in) :: amount
    if (amount < 0_int64 .or. amount > rank1_bytes) &
      call XABORT('SPOT1P64 RANK1 CACHE: INVALID ACCOUNTING RELEASE.')
    rank1_bytes=rank1_bytes-amount
  end subroutine SPOT1P64_RANK1_RELEASE

  subroutine SPOT1P64_RANK1_GUARD(igroup,key,phase,eligible,active)
    integer, intent(in) :: igroup,phase
    integer(int64), intent(in) :: key(:)
    logical, intent(in) :: eligible
    logical, intent(out) :: active
    integer(int64) :: amount
    active=.false.
    if (.not.rank1_enabled) return
    if (igroup < 1 .or. igroup > size(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 CACHE: INVALID ENERGY GROUP.')
    if (.not.allocated(SPOT1P64_PLAN(igroup)%mode)) then
      if (.not.eligible) return
      ! All descriptors/scalars are covered by 4096 declared bytes/group.
      allocate(SPOT1P64_PLAN(igroup)%mode(1))
    endif
    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))
      if (.not.eligible) &
        call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
      if (size(key,kind=int64) > RANK1_CAP/8_int64) &
        call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
      amount=size(key,kind=int64)*8_int64
      if (phase == 1) then
        if (allocated(plan%rank1_raw_bits)) then
          call SPOT1P64_RANK1_KEY_MATCH(igroup,key,phase)
        else
          call SPOT1P64_RANK1_KEY_STORE(igroup,key,phase)
        endif
      else if (phase == 2) then
        if (.not.allocated(plan%rank1_raw_bits)) &
          call XABORT('SPOT1P64 RANK1 CACHE: MISSING RAW IDENTITY.')
        if (allocated(plan%rank1_operator_bits)) then
          call SPOT1P64_RANK1_KEY_MATCH(igroup,key,phase)
          if (plan%ready) rank1_validated_hits=rank1_validated_hits+1_int64
        else
          call SPOT1P64_RANK1_KEY_STORE(igroup,key,phase)
        endif
      else
        call XABORT('SPOT1P64 RANK1 CACHE: INVALID IDENTITY PHASE.')
      endif
      active=.true.
    end associate
  end subroutine SPOT1P64_RANK1_GUARD

  ! Source-only V11 candidate. No floating operation is performed here.
  subroutine SPOT1P64_RANK1_KEY_STATS(igroup,phase,owner,count, &
                                    compressed,stored_words,stored_positions)
    integer, intent(in) :: igroup,phase
    integer, intent(out) :: owner
    integer(int64), intent(out) :: count,stored_words,stored_positions
    logical, intent(out) :: compressed
    owner=0
    count=0_int64
    stored_words=0_int64
    stored_positions=0_int64
    compressed=.false.
    if (.not.rank1_enabled) return
    if (.not.allocated(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
    if (igroup < 1 .or. igroup > size(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 CACHE: INVALID ENERGY GROUP.')
    if (.not.allocated(SPOT1P64_PLAN(igroup)%mode)) &
      call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
    if (size(SPOT1P64_PLAN(igroup)%mode) /= 1) &
      call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
    ! Observation only: a negative control may archive malformed metadata.
    ! The MATCH/LOAD gates below validate every format/index before use.
    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))
      if (phase == 1) then
        owner=rank1_raw_base_owner
        count=plan%rank1_raw_size
        compressed=allocated(plan%rank1_raw_positions)
        if (allocated(plan%rank1_raw_bits)) &
          stored_words=size(plan%rank1_raw_bits,kind=int64)
        if (compressed) stored_positions=size(plan%rank1_raw_positions,kind=int64)
      else if (phase == 2) then
        owner=rank1_operator_base_owner
        count=plan%rank1_operator_size
        compressed=allocated(plan%rank1_operator_positions)
        if (allocated(plan%rank1_operator_bits)) &
          stored_words=size(plan%rank1_operator_bits,kind=int64)
        if (compressed) stored_positions=size(plan%rank1_operator_positions,kind=int64)
      else
        call XABORT('SPOT1P64 RANK1 CACHE: INVALID IDENTITY PHASE.')
      endif
    end associate
  end subroutine SPOT1P64_RANK1_KEY_STATS

  subroutine SPOT1P64_RANK1_KEY_BASE_VALIDATE(owner,phase)
    integer, intent(in) :: owner,phase
    if (.not.allocated(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
    if (owner < 1 .or. owner > size(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
    if (.not.allocated(SPOT1P64_PLAN(owner)%mode)) &
      call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
    if (size(SPOT1P64_PLAN(owner)%mode) /= 1) &
      call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
    associate(base => SPOT1P64_PLAN(owner)%mode(1))
      if (phase == 1) then
        if (allocated(base%rank1_raw_positions)) &
          call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
        call SPOT1P64_RANK1_KEY_VALIDATE_DATA(base%rank1_raw_bits, &
          base%rank1_raw_positions,base%rank1_raw_size)
      else if (phase == 2) then
        if (allocated(base%rank1_operator_positions)) &
          call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
        call SPOT1P64_RANK1_KEY_VALIDATE_DATA(base%rank1_operator_bits, &
          base%rank1_operator_positions,base%rank1_operator_size)
      else
        call XABORT('SPOT1P64 RANK1 CACHE: INVALID IDENTITY PHASE.')
      endif
    end associate
  end subroutine SPOT1P64_RANK1_KEY_BASE_VALIDATE

  subroutine SPOT1P64_RANK1_KEY_VALIDATE_DATA(bits,positions,nkey,base)
    integer(int64), allocatable, intent(in) :: bits(:)
    integer(int32), allocatable, intent(in) :: positions(:)
    integer(int64), intent(in) :: nkey
    integer(int64), optional, intent(in) :: base(:)
    integer :: k,previous,p
    if (.not.allocated(bits)) &
      call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
    if (nkey < 0_int64 .or. nkey > RANK1_CAP/8_int64) &
      call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
    if (.not.allocated(positions)) then
      if (size(bits,kind=int64) /= nkey) &
        call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
      return
    endif
    if (.not.present(base)) &
      call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
    if (size(base,kind=int64) /= nkey .or. size(bits) /= size(positions)) &
      call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
    if (12_int64*size(bits,kind=int64) >= 8_int64*nkey) &
      call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
    previous=0
    do k=1,size(positions)
      p=int(positions(k))
      if (p <= previous .or. int(p,int64) > nkey) &
        call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
      if (bits(k) == base(p)) &
        call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
      previous=p
    enddo
  end subroutine SPOT1P64_RANK1_KEY_VALIDATE_DATA

  subroutine SPOT1P64_RANK1_KEY_SAVE_DATA(key,bits,positions,nkey,base)
    integer(int64), intent(in) :: key(:)
    integer(int64), allocatable, intent(inout) :: bits(:)
    integer(int32), allocatable, intent(inout) :: positions(:)
    integer(int64), intent(inout) :: nkey
    integer(int64), optional, intent(in) :: base(:)
    integer :: i,d,k
    integer(int64) :: amount
    logical :: use_delta
    if (allocated(bits) .or. allocated(positions) .or. nkey /= 0_int64) &
      call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
    if (size(key,kind=int64) > RANK1_CAP/8_int64) &
      call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
    use_delta=.false.
    d=0
    if (present(base)) then
      if (size(base) == size(key)) then
        do i=1,size(key)
          if (key(i) /= base(i)) d=d+1
        enddo
        use_delta=12_int64*int(d,int64) < 8_int64*size(key,kind=int64)
      endif
    endif
    if (use_delta) then
      amount=12_int64*int(d,int64)
      call SPOT1P64_RANK1_RESERVE(amount)
      allocate(bits(d),positions(d))
      k=0
      do i=1,size(key)
        if (key(i) == base(i)) cycle
        k=k+1
        positions(k)=int(i,int32)
        bits(k)=key(i)
      enddo
    else
      amount=8_int64*size(key,kind=int64)
      call SPOT1P64_RANK1_RESERVE(amount)
      allocate(bits(size(key)))
      bits=key
    endif
    nkey=size(key,kind=int64)
  end subroutine SPOT1P64_RANK1_KEY_SAVE_DATA

  subroutine SPOT1P64_RANK1_KEY_STORE(igroup,key,phase)
    integer, intent(in) :: igroup,phase
    integer(int64), intent(in) :: key(:)
    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))
      if (phase == 1) then
        if (rank1_raw_base_owner == 0) then
          call SPOT1P64_RANK1_KEY_SAVE_DATA(key,plan%rank1_raw_bits, &
            plan%rank1_raw_positions,plan%rank1_raw_size)
          rank1_raw_base_owner=igroup
        else
          call SPOT1P64_RANK1_KEY_BASE_VALIDATE(rank1_raw_base_owner,phase)
          call SPOT1P64_RANK1_KEY_SAVE_DATA(key,plan%rank1_raw_bits, &
            plan%rank1_raw_positions,plan%rank1_raw_size, &
            SPOT1P64_PLAN(rank1_raw_base_owner)%mode(1)%rank1_raw_bits)
        endif
      else if (phase == 2) then
        if (rank1_operator_base_owner == 0) then
          call SPOT1P64_RANK1_KEY_SAVE_DATA(key,plan%rank1_operator_bits, &
            plan%rank1_operator_positions,plan%rank1_operator_size)
          rank1_operator_base_owner=igroup
        else
          call SPOT1P64_RANK1_KEY_BASE_VALIDATE(rank1_operator_base_owner,phase)
          call SPOT1P64_RANK1_KEY_SAVE_DATA(key,plan%rank1_operator_bits, &
            plan%rank1_operator_positions,plan%rank1_operator_size, &
            SPOT1P64_PLAN(rank1_operator_base_owner)%mode(1)%rank1_operator_bits)
        endif
      else
        call XABORT('SPOT1P64 RANK1 CACHE: INVALID IDENTITY PHASE.')
      endif
    end associate
  end subroutine SPOT1P64_RANK1_KEY_STORE

  subroutine SPOT1P64_RANK1_KEY_CHECK_DATA(key,bits,positions,nkey,base)
    integer(int64), intent(in) :: key(:)
    integer(int64), allocatable, intent(in) :: bits(:)
    integer(int32), allocatable, intent(in) :: positions(:)
    integer(int64), intent(in) :: nkey
    integer(int64), optional, intent(in) :: base(:)
    integer :: i,k,p
    integer(int64) :: expected
    call SPOT1P64_RANK1_KEY_VALIDATE_DATA(bits,positions,nkey,base)
    if (size(key,kind=int64) /= nkey) &
      call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
    k=1
    do i=1,size(key)
      if (allocated(positions)) then
        expected=base(i)
        if (k <= size(positions)) then
          p=int(positions(k))
          if (i == p) then
            expected=bits(k)
            k=k+1
          endif
        endif
      else
        expected=bits(i)
      endif
      if (expected /= key(i)) &
        call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
    enddo
  end subroutine SPOT1P64_RANK1_KEY_CHECK_DATA

  subroutine SPOT1P64_RANK1_KEY_MATCH(igroup,key,phase)
    integer, intent(in) :: igroup,phase
    integer(int64), intent(in) :: key(:)
    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))
      if (phase == 1) then
        if (allocated(plan%rank1_raw_positions)) then
          call SPOT1P64_RANK1_KEY_BASE_VALIDATE(rank1_raw_base_owner,phase)
          call SPOT1P64_RANK1_KEY_CHECK_DATA(key,plan%rank1_raw_bits, &
            plan%rank1_raw_positions,plan%rank1_raw_size, &
            SPOT1P64_PLAN(rank1_raw_base_owner)%mode(1)%rank1_raw_bits)
        else
          call SPOT1P64_RANK1_KEY_CHECK_DATA(key,plan%rank1_raw_bits, &
            plan%rank1_raw_positions,plan%rank1_raw_size)
        endif
      else if (phase == 2) then
        if (allocated(plan%rank1_operator_positions)) then
          call SPOT1P64_RANK1_KEY_BASE_VALIDATE(rank1_operator_base_owner,phase)
          call SPOT1P64_RANK1_KEY_CHECK_DATA(key,plan%rank1_operator_bits, &
            plan%rank1_operator_positions,plan%rank1_operator_size, &
            SPOT1P64_PLAN(rank1_operator_base_owner)%mode(1)%rank1_operator_bits)
        else
          call SPOT1P64_RANK1_KEY_CHECK_DATA(key,plan%rank1_operator_bits, &
            plan%rank1_operator_positions,plan%rank1_operator_size)
        endif
      else
        call XABORT('SPOT1P64 RANK1 CACHE: INVALID IDENTITY PHASE.')
      endif
    end associate
  end subroutine SPOT1P64_RANK1_KEY_MATCH

  subroutine SPOT1P64_RANK1_KEY_LOAD_DATA(key,bits,positions,nkey,base)
    integer(int64), intent(out) :: key(:)
    integer(int64), allocatable, intent(in) :: bits(:)
    integer(int32), allocatable, intent(in) :: positions(:)
    integer(int64), intent(in) :: nkey
    integer(int64), optional, intent(in) :: base(:)
    integer :: k
    call SPOT1P64_RANK1_KEY_VALIDATE_DATA(bits,positions,nkey,base)
    if (size(key,kind=int64) /= nkey) &
      call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
    if (allocated(positions)) then
      key=base
      do k=1,size(positions)
        key(int(positions(k)))=bits(k)
      enddo
    else
      key=bits
    endif
  end subroutine SPOT1P64_RANK1_KEY_LOAD_DATA

  subroutine SPOT1P64_RANK1_KEY_LOAD(igroup,phase,key)
    integer, intent(in) :: igroup,phase
    integer(int64), intent(out) :: key(:)
    if (.not.rank1_enabled .or. .not.allocated(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
    if (igroup < 1 .or. igroup > size(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 CACHE: INVALID ENERGY GROUP.')
    if (.not.allocated(SPOT1P64_PLAN(igroup)%mode)) &
      call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
    if (size(SPOT1P64_PLAN(igroup)%mode) /= 1) &
      call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))
      if (phase == 1) then
        if (allocated(plan%rank1_raw_positions)) then
          call SPOT1P64_RANK1_KEY_BASE_VALIDATE(rank1_raw_base_owner,phase)
          call SPOT1P64_RANK1_KEY_LOAD_DATA(key,plan%rank1_raw_bits, &
            plan%rank1_raw_positions,plan%rank1_raw_size, &
            SPOT1P64_PLAN(rank1_raw_base_owner)%mode(1)%rank1_raw_bits)
        else
          call SPOT1P64_RANK1_KEY_LOAD_DATA(key,plan%rank1_raw_bits, &
            plan%rank1_raw_positions,plan%rank1_raw_size)
        endif
      else if (phase == 2) then
        if (allocated(plan%rank1_operator_positions)) then
          call SPOT1P64_RANK1_KEY_BASE_VALIDATE(rank1_operator_base_owner,phase)
          call SPOT1P64_RANK1_KEY_LOAD_DATA(key,plan%rank1_operator_bits, &
            plan%rank1_operator_positions,plan%rank1_operator_size, &
            SPOT1P64_PLAN(rank1_operator_base_owner)%mode(1)%rank1_operator_bits)
        else
          call SPOT1P64_RANK1_KEY_LOAD_DATA(key,plan%rank1_operator_bits, &
            plan%rank1_operator_positions,plan%rank1_operator_size)
        endif
      else
        call XABORT('SPOT1P64 RANK1 CACHE: INVALID IDENTITY PHASE.')
      endif
    end associate
  end subroutine SPOT1P64_RANK1_KEY_LOAD

  subroutine SPOT1P64_RANK1_FACTORS(igroup,nstate,nblock,npositive)
    integer, intent(in) :: igroup,nstate,nblock
    integer, optional, intent(in) :: npositive
    integer :: positive_rows
    integer(int64) :: square,amount,blocks,row_bytes,map_bytes
    if (.not.rank1_enabled) return
    if (nstate <= 0 .or. nblock <= 0) &
      call XABORT('SPOT1P64 RANK1 CACHE: INVALID FACTOR DIMENSIONS.')
    if (int(nstate,int64) > RANK1_CAP/24_int64/int(nstate,int64)) &
      call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
    square=int(nstate,int64)*int(nstate,int64)
    positive_rows=nstate
    if (present(npositive)) positive_rows=npositive
    if (positive_rows <= 0 .or. positive_rows > nstate) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    ! Dense factor/cprime, packed lower; pivots and persistent row map.
    amount=16_int64*square+8_int64*int(positive_rows,int64)*int(nstate,int64)+ &
      12_int64*int(nstate,int64)
    row_bytes=4_int64*int(positive_rows,int64)
    blocks=int(nblock,int64)
    if (blocks > RANK1_CAP/amount) &
      call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
    amount=amount*blocks
    if (row_bytes > RANK1_CAP-amount) &
      call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
    amount=amount+row_bytes
    map_bytes=4_int64*blocks
    if (map_bytes > RANK1_CAP-amount) &
      call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
    amount=amount+map_bytes
    ! Last cprime is never read; keep every full original solve.
    amount=amount-8_int64*square
    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))
      if (plan%rank1_factor_bytes /= 0_int64) &
        call XABORT('SPOT1P64 RANK1 CACHE: FACTORS ALREADY RESERVED.')
      call SPOT1P64_RANK1_RESERVE(amount)
      plan%rank1_factor_bytes=amount
      plan%rank1_lower_rows_count=positive_rows
    end associate
  end subroutine SPOT1P64_RANK1_FACTORS

  ! Only ordinary rank1 uses this storage.  Equality is INTEGER64 IEEE
  ! equality. First occurrence defines dictionary order; 49 unique blocks
  ! remain valid. Decode preserves full original matrix shape and arithmetic.

  ! Ordinary-rank1 only: FACTOR64/SOLVE64 no longer read factor diagonals
  ! after build. Keep every live entry, pivot, and pivot_value unchanged.
  subroutine SPOT1P64_RANK1_FACTOR_PACK(igroup)
    integer, intent(in) :: igroup
    double precision, allocatable :: packed(:,:,:)
    integer :: n,b,i,j,k,row
    integer(int64) :: full_bytes,packed_bytes,dead_bytes
    if (.not.rank1_enabled .or. .not.allocated(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
    if (igroup < 1 .or. igroup > size(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
    if (.not.allocated(SPOT1P64_PLAN(igroup)%mode)) &
      call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
    if (size(SPOT1P64_PLAN(igroup)%mode) /= 1) &
      call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))
      n=plan%nstate; b=plan%nblock
      if (n <= 0 .or. b <= 0 .or. plan%ready .or. .not.allocated(plan%factor)) &
        call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
      if (any(shape(plan%factor) /= (/n,n,b/))) &
        call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
      if (int(n,int64) > RANK1_CAP/24_int64/int(n,int64)) &
        call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
      full_bytes=8_int64*int(n,int64)*int(n,int64)
      if (int(b,int64) > RANK1_CAP/full_bytes) &
        call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
      full_bytes=full_bytes*int(b,int64)
      dead_bytes=8_int64*int(n,int64)*int(b,int64)
      packed_bytes=full_bytes-dead_bytes
      if (plan%rank1_factor_bytes < full_bytes) &
        call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
      ! Both arrays coexist until move_alloc. Account the complete temporary.
      call SPOT1P64_RANK1_RESERVE(packed_bytes)
      allocate(packed(n-1,n,b))
      do k=1,b
        do j=1,n
          row=0
          do i=1,n
            if (i == j) cycle
            row=row+1
            packed(row,j,k)=plan%factor(i,j,k)
          enddo
        enddo
      enddo
      call move_alloc(packed,plan%factor)
      call SPOT1P64_RANK1_RELEASE(full_bytes)
      plan%rank1_factor_bytes=plan%rank1_factor_bytes-dead_bytes
    end associate
  end subroutine SPOT1P64_RANK1_FACTOR_PACK

  subroutine SPOT1P64_RANK1_FACTOR_LOAD(igroup,block,factor)
    integer, intent(in) :: igroup,block
    double precision, intent(out) :: factor(:,:)
    integer :: n,b,i,j,row
    if (.not.rank1_enabled .or. .not.allocated(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
    if (igroup < 1 .or. igroup > size(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
    if (.not.allocated(SPOT1P64_PLAN(igroup)%mode)) &
      call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
    if (size(SPOT1P64_PLAN(igroup)%mode) /= 1) &
      call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))
      n=plan%nstate; b=plan%nblock
      if (n <= 0 .or. b <= 0 .or. .not.plan%ready .or. .not.allocated(plan%factor)) &
        call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
      if (any(shape(plan%factor) /= (/n-1,n,b/)) .or. &
          any(shape(factor) /= (/n,n/)) .or. block < 1 .or. block > b) &
        call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
      factor=0.0d0
      do j=1,n
        row=0
        do i=1,n
          if (i == j) cycle
          row=row+1
          factor(i,j)=plan%factor(row,j,block)
        enddo
      enddo
    end associate
  end subroutine SPOT1P64_RANK1_FACTOR_LOAD

  subroutine SPOT1P64_RANK1_LOWER_STORE(igroup,lower,du)
    integer, intent(in) :: igroup
    double precision, intent(in) :: lower(:,:,:)
    real, intent(in) :: du(:)
    integer :: nstate,nblock,nrow,i,j,block,row,prior,match,nunique
    integer(int64) :: released_bytes
    logical :: equal_bits
    if (.not.rank1_enabled) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (.not.allocated(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (igroup < 1 .or. igroup > size(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (.not.allocated(SPOT1P64_PLAN(igroup)%mode)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (size(SPOT1P64_PLAN(igroup)%mode) /= 1) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (.not.all(ieee_is_finite(du))) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID ROW MAP.')
    nstate=size(du); nblock=size(lower,3); nrow=count(du > 0.0)
    if (nstate <= 0 .or. nblock <= 0 .or. nrow <= 0 .or. &
        size(lower,1) /= nstate .or. size(lower,2) /= nstate) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))
      if (plan%nstate /= nstate .or. plan%nblock /= nblock .or. &
          plan%rank1_factor_bytes <= 0_int64 .or. &
          plan%rank1_lower_rows_count /= nrow) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
      if (allocated(plan%lower) .or. allocated(plan%rank1_lower_rows) .or. &
          allocated(plan%rank1_lower) .or. allocated(plan%rank1_lower_blocks) .or. &
          plan%rank1_lower_unique_count /= 0) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
      do block=1,nblock
        do j=1,nstate
          do i=1,nstate
            if (du(i) > 0.0) cycle
            if (transfer(lower(i,j,block),0_int64) /= 0_int64) &
              call XABORT('SPOT1P64 RANK1 LOWER: NONZERO OR SIGNED ZERO OMITTED ROW.')
          enddo
        enddo
      enddo
      ! FACTORS reserved all row/map and worst-case 49-unique value bytes.
      ! No temporary packed matrix or floating-point equality is constructed.
      allocate(plan%rank1_lower_rows(nrow),plan%rank1_lower_blocks(nblock))
      row=0
      do i=1,nstate
        if (du(i) <= 0.0) cycle
        row=row+1; plan%rank1_lower_rows(row)=i
      enddo
      nunique=0
      do block=1,nblock
        match=0
        do prior=1,block-1
          equal_bits=.true.
          do j=1,nstate
            do row=1,nrow
              i=plan%rank1_lower_rows(row)
              if (transfer(lower(i,j,block),0_int64) /= &
                  transfer(lower(i,j,prior),0_int64)) equal_bits=.false.
            enddo
          enddo
          if (equal_bits) then
            match=plan%rank1_lower_blocks(prior)
            exit
          endif
        enddo
        if (match == 0) then
          nunique=nunique+1; match=nunique
        endif
        plan%rank1_lower_blocks(block)=match
      enddo
      allocate(plan%rank1_lower(nrow,nstate,nunique))
      do block=1,nblock
        match=plan%rank1_lower_blocks(block)
        if (block > 1) then
          if (any(plan%rank1_lower_blocks(:block-1) == match)) cycle
        endif
        do j=1,nstate
          do row=1,nrow
            plan%rank1_lower(row,j,match)=lower(plan%rank1_lower_rows(row),j,block)
          enddo
        enddo
      enddo
      plan%rank1_lower_unique_count=nunique
      released_bytes=8_int64*int(nrow,int64)*int(nstate,int64)*int(nblock-nunique,int64)
      call SPOT1P64_RANK1_RELEASE(released_bytes)
      plan%rank1_factor_bytes=plan%rank1_factor_bytes-released_bytes
    end associate
  end subroutine SPOT1P64_RANK1_LOWER_STORE

  subroutine SPOT1P64_RANK1_LOWER_VALIDATE(igroup,nstate,nblock,du,check_unique)
    integer, intent(in) :: igroup,nstate,nblock
    real, intent(in) :: du(:)
    logical, optional, intent(in) :: check_unique
    integer :: nrow,i,row,block,highest,which,other,j,nunique
    integer(int64) :: expected_bytes,square
    logical :: equal_bits,deep
    deep=.true.
    if (present(check_unique)) deep=check_unique
    if (.not.rank1_enabled .or. nstate <= 0 .or. nblock <= 0 .or. &
        size(du) /= nstate) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (.not.allocated(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (igroup < 1 .or. igroup > size(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (.not.allocated(SPOT1P64_PLAN(igroup)%mode)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (size(SPOT1P64_PLAN(igroup)%mode) /= 1) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (.not.all(ieee_is_finite(du))) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID ROW MAP.')
    nrow=count(du > 0.0)
    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))
      nunique=plan%rank1_lower_unique_count
      if (plan%nstate /= nstate .or. plan%nblock /= nblock .or. &
          nrow <= 0 .or. allocated(plan%lower) .or. &
          plan%rank1_lower_rows_count /= nrow .or. nunique <= 0 .or. nunique > nblock) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
      if (.not.allocated(plan%rank1_lower_rows) .or. .not.allocated(plan%rank1_lower) .or. &
          .not.allocated(plan%rank1_lower_blocks)) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
      if (size(plan%rank1_lower_rows) /= nrow .or. &
          size(plan%rank1_lower,1) /= nrow .or. size(plan%rank1_lower,2) /= nstate .or. &
          size(plan%rank1_lower,3) /= nunique .or. size(plan%rank1_lower_blocks) /= nblock) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
      if (any(plan%rank1_lower_rows < 1) .or. any(plan%rank1_lower_rows > nstate)) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID ROW MAP.')
      row=0
      do i=1,nstate
        if (du(i) <= 0.0) cycle
        row=row+1
        if (plan%rank1_lower_rows(row) /= i) &
          call XABORT('SPOT1P64 RANK1 LOWER: INVALID ROW MAP.')
      enddo
      highest=0
      do block=1,nblock
        which=plan%rank1_lower_blocks(block)
        if (which < 1 .or. which > nunique .or. which > highest+1) &
          call XABORT('SPOT1P64 RANK1 LOWER: INVALID CANONICAL BLOCK MAP.')
        highest=max(highest,which)
      enddo
      if (highest /= nunique) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID CANONICAL BLOCK MAP.')
      if (deep) then
        do which=1,nunique
          do other=1,which-1
            equal_bits=.true.
            do j=1,nstate
              do row=1,nrow
                if (transfer(plan%rank1_lower(row,j,which),0_int64) /= &
                    transfer(plan%rank1_lower(row,j,other),0_int64)) equal_bits=.false.
              enddo
            enddo
            if (equal_bits) call XABORT('SPOT1P64 RANK1 LOWER: DUPLICATE DICTIONARY BLOCK.')
          enddo
        enddo
      endif
      ! Keep the parent's checked extreme-dimension boundary before products.
      if (int(nstate,int64) > RANK1_CAP/24_int64/int(nstate,int64)) &
        call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
      square=int(nstate,int64)*int(nstate,int64)
      expected_bytes=16_int64*square+12_int64*int(nstate,int64)
      if (int(nblock,int64) > RANK1_CAP/expected_bytes) &
        call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
      expected_bytes=expected_bytes*int(nblock,int64)+ &
        8_int64*int(nrow,int64)*int(nstate,int64)*int(nunique,int64)+ &
        4_int64*int(nrow,int64)+4_int64*int(nblock,int64)
      expected_bytes=expected_bytes-8_int64*square
      if (plan%ready .and. allocated(plan%factor)) then
        if (any(shape(plan%factor) /= (/nstate-1,nstate,nblock/))) &
          call XABORT('SPOT1P64 RANK1 FACTOR: INVALID PACKED DIMENSIONS.')
        expected_bytes=expected_bytes-8_int64*int(nstate,int64)*int(nblock,int64)
      endif
      if (expected_bytes /= plan%rank1_factor_bytes) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    end associate
  end subroutine SPOT1P64_RANK1_LOWER_VALIDATE

  subroutine SPOT1P64_RANK1_LOWER_LOAD(igroup,block,lower,du,already_dictionary_validated)
    integer, intent(in) :: igroup,block
    double precision, intent(out) :: lower(:,:)
    real, intent(in) :: du(:)
    logical, optional, intent(in) :: already_dictionary_validated
    integer :: row,nblock
    logical :: deep
    deep=.true.
    if (present(already_dictionary_validated)) then
      if (already_dictionary_validated) deep=.false.
    endif
    if (.not.allocated(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (igroup < 1 .or. igroup > size(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (.not.allocated(SPOT1P64_PLAN(igroup)%mode)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (size(SPOT1P64_PLAN(igroup)%mode) /= 1) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    nblock=SPOT1P64_PLAN(igroup)%mode(1)%nblock
    call SPOT1P64_RANK1_LOWER_VALIDATE(igroup,size(lower,1),nblock,du,deep)
    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))
      if (size(lower,2) /= plan%nstate .or. block < 1 .or. block > plan%nblock) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
      lower=0.0d0
      do row=1,size(plan%rank1_lower_rows)
        lower(plan%rank1_lower_rows(row),:)=plan%rank1_lower(row,:,plan%rank1_lower_blocks(block))
      enddo
    end associate
  end subroutine SPOT1P64_RANK1_LOWER_LOAD

  subroutine SPOT1P64_RANK1_STATS(built,reused,hits,live,peak,cap)
    integer(int64), intent(out) :: built,reused,hits,live,peak,cap
    built=rank1_builds
    reused=rank1_reuses
    hits=rank1_validated_hits
    live=rank1_bytes
    peak=rank1_peak
    cap=RANK1_CAP
  end subroutine SPOT1P64_RANK1_STATS

  subroutine SPOT1P64_RANK1_TERMINAL()
    if (rank1_enabled.and.rank1_builds > 0_int64) write(6,'(A,5(1X,I0))') &
      'AXMAT-RANK1-CACHE TERMINAL',rank1_builds,rank1_reuses, &
      rank1_validated_hits,rank1_peak,RANK1_CAP
  end subroutine SPOT1P64_RANK1_TERMINAL

  subroutine SPOT1P64_RANK1_PROGRESS(it,jt,igdeb,einn)
    integer, intent(in) :: it,jt,igdeb
    double precision, intent(in) :: einn
    if (.not.rank1_enabled .or. rank1_builds == 0_int64) return
    if (jt /= 1 .and. mod(jt,32) /= 0) return
    write(6,'(A,3(1X,I0),1X,ES25.16E3,4(1X,I0))') &
      'AXMAT-RANK1-CACHE PROGRESS',it,jt,igdeb,einn, &
      rank1_builds,rank1_reuses,rank1_validated_hits,rank1_peak
    flush(6)
  end subroutine SPOT1P64_RANK1_PROGRESS

end module SPOT1P64_CACHE_MOD

!-----------------------------------------------------------------------
!
! Purpose:
!   Solve the coupled one-dimensional SN equations in a radial POD
!   trial space and reconstruct the physical regional flux.
!
! The radial expansion for one energy group is
!
!        psi_i(z,mu) = sum_a B_i^a A_a(z,mu),
!
! where B is any full-rank radial basis.  Material operators, sources,
! and the streaming mass matrix are projected with the same volume inner
! product.  RANK therefore equals
! the number of axial modal unknowns; POD is not an input filter.
!
! This first clean implementation intentionally supports the constant
! diamond spatial approximation only.
!
!-----------------------------------------------------------------------
subroutine SPOT1P64(igroup,nreg2d,nfloor,ielem,nmat,nsnap,nmode,ischm,npq,nsct, &
                  lfixup,mat1d,vol1d,mat,total,sgas,basis,vol2d, &
                  radial2d,ncode,zcode,qext,du,w,pl,flux,cour,xnei)
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_fortran_env, only: int32,int64
  use SPOT1P64_CACHE_MOD, only : SPOT1P64_PLAN,SPOT1P64_CACHE_PREPARE, &
    SPOT1P64_CACHE_NOTE_BUILD,SPOT1P64_CACHE_NOTE_REUSE, &
    SPOT1P64_FACTOR64,SPOT1P64_SOLVE64,SPOT1P64_RANK1_ENABLED, &
    SPOT1P64_RANK1_RESERVE,SPOT1P64_RANK1_RELEASE, &
    SPOT1P64_RANK1_GUARD,SPOT1P64_RANK1_FACTORS, &
    SPOT1P64_RANK1_LOWER_STORE,SPOT1P64_RANK1_LOWER_VALIDATE, &
    SPOT1P64_RANK1_LOWER_LOAD, &
    SPOT1P64_RANK1_FACTOR_PACK,SPOT1P64_RANK1_FACTOR_LOAD
  use AXMAT_WHITE_TRACE_MOD, only: AXMAT_WHITE_ON,AXMAT_WHITE_ROW, &
    AXMAT_WHITE_PERIMETER,AXMAT_WHITE_KERNEL,AXMAT_WHITE_NOTE
  implicit none
  integer, parameter :: dp=kind(1.0d0)

  integer, intent(in) :: igroup,nreg2d,nfloor,ielem,nmat,nsnap,nmode
  integer, intent(in) :: ischm,npq,nsct
  integer, intent(in) :: mat1d(nfloor),mat(nfloor,nreg2d),ncode(2)
  real, intent(in) :: vol1d(nfloor),total(0:nmat),sgas(0:nmat,nsct)
  real, intent(in) :: basis(nreg2d,nmode),vol2d(nreg2d),zcode(2)
  double precision, intent(in) :: radial2d(nreg2d,nsnap)
  double precision, intent(in) :: qext(ielem,nsct,nfloor,nreg2d)
  real, intent(in) :: du(npq),w(npq),pl(nsct,npq)
  double precision, intent(out) :: flux(ielem,nsct,nfloor,nreg2d)
  double precision, intent(out) :: cour(nfloor+1,nreg2d),xnei(npq,nreg2d)
  logical, intent(in) :: lfixup

  integer :: i,a,b,n,m,l,ifloor,iface,ibm,isnap,half
  integer :: npositive,nnegative,npair,white_info
  double precision, allocatable :: white_angle(:,:),white_mode(:,:)
  double precision :: vtot,wi,scale,albedo_left,albedo_right
  double precision, allocatable :: weight(:),mass_m(:,:),total_m(:,:,:)
  double precision, allocatable :: radial_m(:,:,:)
  double precision, allocatable :: scat_m(:,:,:,:),source_m(:,:,:)
  double precision, allocatable :: mn(:,:),dn(:,:)
  double precision, allocatable :: face(:,:,:),cell(:,:,:)
  double precision, allocatable :: modal_flux(:,:,:),modal_cour(:,:)
  integer, allocatable :: opposite(:)
  logical :: translation,diagonal_basis,mode_separable,use_factor_cache
  logical :: rank1_identity_active

  call rank1_identity(1,rank1_identity_active)

  if (ielem /= 1 .or. ischm /= 1) &
    call XABORT('SPOT1P: ONLY CONSTANT DIAMOND SPATIAL APPROXIMATION IS SUPPORTED.')
  if (lfixup) &
    call XABORT('SPOT1P: NEGATIVE-FLUX FIXUP IS NOT IMPLEMENTED.')
  if (nmode <= 0 .or. nmode > nreg2d) &
    call XABORT('SPOT1P: INVALID POD MODE COUNT.')
  if (mod(npq,2) /= 0 .or. npq <= 0) &
    call XABORT('SPOT1P: AN EVEN SN ORDER IS REQUIRED.')
  if (any(vol1d <= 0.0) .or. any(vol2d <= 0.0) .or. &
      any(.not.ieee_is_finite(vol1d)) .or. &
      any(.not.ieee_is_finite(vol2d)) .or. &
      any(.not.ieee_is_finite(basis))) &
    call XABORT('SPOT1P: INVALID VOLUME OR BASIS.')
  if (any(.not.ieee_is_finite(total)) .or. &
      any(.not.ieee_is_finite(sgas)) .or. &
      any(.not.ieee_is_finite(radial2d)) .or. &
      any(.not.ieee_is_finite(qext)) .or. &
      any(.not.ieee_is_finite(pl)) .or. &
      any(.not.ieee_is_finite(zcode))) &
    call XABORT('SPOT1P: NON-FINITE OPERATOR OR SOURCE DATA.')
  if (any(.not.ieee_is_finite(du)) .or. &
      any(.not.ieee_is_finite(w)) .or. any(w <= 0.0)) &
    call XABORT('SPOT1P: INVALID SN QUADRATURE DATA.')

  half=npq/2
  npositive=count(du > 0.0)
  nnegative=count(du < 0.0)
  if (npositive /= half .or. nnegative /= half) &
    call XABORT('SPOT1P: INVALID SYMMETRIC SN DIRECTIONS.')
  allocate(opposite(npq))
  opposite=0
  do n=1,npq
    npair=0
    do m=1,npq
      ! Unary negation is exact for a finite stored IEEE real.  Compare
      ! representations so the pairing contains no numerical tolerance.
      if (transfer(du(m),0) == transfer(-du(n),0)) then
        npair=npair+1
        opposite(n)=m
      endif
    enddo
    if (npair /= 1) &
      call XABORT('SPOT1P: SN DIRECTION HAS NO UNIQUE EXACT OPPOSITE.')
  enddo
  do n=1,npq
    if (opposite(opposite(n)) /= n) &
      call XABORT('SPOT1P: SN OPPOSITE MAP IS NOT AN INVOLUTION.')
    if (count(opposite == n) /= 1) &
      call XABORT('SPOT1P: SN OPPOSITE MAP IS NOT ONE-TO-ONE.')
    if (transfer(w(opposite(n)),0) /= transfer(w(n),0)) &
      call XABORT('SPOT1P: OPPOSITE SN WEIGHTS DIFFER.')
  enddo
  translation=(ncode(1) == 4 .or. ncode(2) == 4)
  if (translation .and. (ncode(1) /= 4 .or. ncode(2) /= 4)) &
    call XABORT('SPOT1P: TRANSLATION BOUNDARIES MUST BE PAIRED.')
  if (.not.translation) then
    if (.not.(ncode(1) == 1 .or. ncode(1) == 2 .or. ncode(1) == 7)) &
      call XABORT('SPOT1P: UNSUPPORTED LEFT BOUNDARY CONDITION.')
    if (.not.(ncode(2) == 1 .or. ncode(2) == 2 .or. ncode(2) == 7)) &
      call XABORT('SPOT1P: UNSUPPORTED RIGHT BOUNDARY CONDITION.')
  endif

  allocate(weight(nreg2d),mass_m(nmode,nmode))
  allocate(total_m(nmode,nmode,nfloor))
  allocate(radial_m(nmode,nmode,nfloor))
  allocate(scat_m(nmode,nmode,nsct,nfloor))
  allocate(source_m(nsct,nfloor,nmode),mn(npq,nsct),dn(nsct,npq))
  vtot=sum(real(vol2d,dp))
  if ((.not.ieee_is_finite(vtot)) .or. vtot <= 0.0d0) &
    call XABORT('SPOT1P: INVALID RADIAL VOLUME SUM.')
  weight=real(vol2d,dp)/vtot
  if (AXMAT_WHITE_ON) then
    if (nreg2d /= 8 .or. all(nfloor /= [12,24,48]) .or. nsnap /= 3 .or. &
        nmode /= 1 .or. all(npq /= [8,16,32]) .or. nsct /= 3 .or. &
        any(ncode /= 1) .or. any(zcode /= 0.0)) &
      call XABORT('AXMAT WHITE: OUTSIDE DECLARED RANK1 VACUUM SCOPE.')
    if (abs(vtot/(sqrt(3.0d0)*AXMAT_WHITE_PERIMETER**2/24.0d0)- &
        1.0d0) > 5.0d-6) &
      call XABORT('AXMAT WHITE: PHYSICAL AREA/PERIMETER MISMATCH.')
    allocate(white_angle(npq,npq),white_mode(nmode,nmode))
    call AXMAT_WHITE_KERNEL(real(du,dp),real(w,dp), &
      AXMAT_WHITE_PERIMETER,vtot,white_angle,white_info)
    if (white_info /= 0) call XABORT('AXMAT WHITE: INVALID ANGULAR KERNEL.')
    do b=1,nmode
      do a=1,nmode
        white_mode(a,b)=real(basis(AXMAT_WHITE_ROW,a),dp)* &
                       real(basis(AXMAT_WHITE_ROW,b),dp)
      enddo
    enddo
    call AXMAT_WHITE_NOTE(igroup,white_mode(1,1))
  endif
  mass_m=0.0d0
  total_m=0.0d0
  radial_m=0.0d0
  scat_m=0.0d0
  source_m=0.0d0

  ! SPOPHYS produces this exact diagonal coordinate map.  Detect the
  ! algebraic structure from B itself so correctness does not depend on a
  ! provenance flag and avoid forming O(NREG2D*NMODE**2) projections.
  diagonal_basis=nmode == nreg2d
  if (diagonal_basis) then
    do i=1,nreg2d
      do a=1,nmode
        if (i == a) then
          if (basis(i,a) == 0.0) diagonal_basis=.false.
        else
          if (basis(i,a) /= 0.0) diagonal_basis=.false.
        endif
      enddo
    enddo
  endif

  if (diagonal_basis) then
    do i=1,nreg2d
      wi=weight(i)
      scale=real(basis(i,i),dp)
      mass_m(i,i)=wi*scale*scale
    enddo
    do ifloor=1,nfloor
      isnap=mat1d(ifloor)
      if (isnap < 1 .or. isnap > nsnap) &
        call XABORT('SPOT1P: INVALID SNAPSHOT INDEX.')
      do i=1,nreg2d
        ibm=mat(ifloor,i)
        if (ibm == 0) cycle
        if (ibm < 0 .or. ibm > nmat) &
          call XABORT('SPOT1P: MATERIAL INDEX OVERFLOW.')
        wi=weight(i)
        scale=real(basis(i,i),dp)
        total_m(i,i,ifloor)=wi*scale*real(total(ibm),dp)*scale
        radial_m(i,i,ifloor)=wi*scale*radial2d(i,isnap)*scale
        do l=1,nsct
          scat_m(i,i,l,ifloor)=wi*scale*real(sgas(ibm,l),dp)*scale
          source_m(l,ifloor,i)=wi*scale*qext(1,l,ifloor,i)
        enddo
      enddo
    enddo
  else
    do i=1,nreg2d
      wi=weight(i)
      do b=1,nmode
        do a=1,nmode
          mass_m(a,b)=mass_m(a,b)+wi*real(basis(i,a),dp)* &
            real(basis(i,b),dp)
        enddo
      enddo
    enddo
    do ifloor=1,nfloor
      isnap=mat1d(ifloor)
      if (isnap < 1 .or. isnap > nsnap) &
        call XABORT('SPOT1P: INVALID SNAPSHOT INDEX.')
      do i=1,nreg2d
        ibm=mat(ifloor,i)
        if (ibm == 0) cycle
        if (ibm < 0 .or. ibm > nmat) &
          call XABORT('SPOT1P: MATERIAL INDEX OVERFLOW.')
        wi=weight(i)
        do a=1,nmode
          do b=1,nmode
            total_m(a,b,ifloor)=total_m(a,b,ifloor)+wi* &
              real(basis(i,a),dp)*real(total(ibm),dp)*real(basis(i,b),dp)
            radial_m(a,b,ifloor)=radial_m(a,b,ifloor)+wi* &
              real(basis(i,a),dp)*radial2d(i,isnap)* &
              real(basis(i,b),dp)
            do l=1,nsct
              scat_m(a,b,l,ifloor)=scat_m(a,b,l,ifloor)+wi* &
                real(basis(i,a),dp)*real(sgas(ibm,l),dp)* &
                real(basis(i,b),dp)
            enddo
          enddo
          do l=1,nsct
            source_m(l,ifloor,a)=source_m(l,ifloor,a)+wi* &
              real(basis(i,a),dp)*qext(1,l,ifloor,i)
          enddo
        enddo
      enddo
    enddo
  endif

  ! The boundary and local systems split by radial mode exactly whenever
  ! every stored off-diagonal projected coefficient is zero.
  mode_separable=.true.
  separability: do a=1,nmode
    do b=1,nmode
      if (a == b) cycle
      if (mass_m(a,b) /= 0.0d0 .or. &
          any(total_m(a,b,:) /= 0.0d0) .or. &
          any(radial_m(a,b,:) /= 0.0d0) .or. &
          any(scat_m(a,b,:,:) /= 0.0d0)) then
        mode_separable=.false.
        exit separability
      endif
    enddo
  enddo separability
  use_factor_cache=.false.
  if ((.not.translation).and.diagonal_basis.and.mode_separable) &
    call SPOT1P64_CACHE_PREPARE(igroup,nmode,use_factor_cache)

  do n=1,npq
    do l=1,nsct
      mn(n,l)=0.5d0*real(2*l-1,dp)*real(pl(l,n),dp)
      dn(l,n)=real(w(n),dp)*real(pl(l,n),dp)
    enddo
  enddo

  allocate(face(npq,nmode,nfloor+1),cell(npq,nmode,nfloor))
  allocate(modal_flux(nsct,nfloor,nmode),modal_cour(nfloor+1,nmode))
  face=0.0d0
  cell=0.0d0

  if (translation) then
    albedo_left=real(zcode(1),dp)
    albedo_right=real(zcode(2),dp)
  else
    albedo_left=merge(1.0d0,real(zcode(1),dp),ncode(1) == 2)
    albedo_right=merge(1.0d0,real(zcode(2),dp),ncode(2) == 2)
    if (ncode(1) == 7) albedo_left=0.0d0
    if (ncode(2) == 7) albedo_right=0.0d0
  endif

  if (rank1_identity_active) then
    call rank1_identity(2,rank1_identity_active)
    use_factor_cache=rank1_identity_active
  endif

  if (.not.translation) then
    ! Solve the two-point boundary-value problem directly.  The block
    ! tridiagonal system is algebraically identical to diamond differencing
    ! but remains stable when the axial mesh is refined.
    if (mode_separable) then
      do a=1,nmode
        call boundary_solve(a,a,face,cell,albedo_left,albedo_right)
      enddo
    else
      call boundary_solve(1,nmode,face,cell,albedo_left,albedo_right)
    endif
  else
    ! Translation boundaries couple the two end faces.  Retain the compact
    ! shooting construction for this uncommon cyclic case.
    if (mode_separable) then
      do a=1,nmode
        call translation_solve(a,a,face,cell,albedo_left,albedo_right)
      enddo
    else
      call translation_solve(1,nmode,face,cell,albedo_left,albedo_right)
    endif
  endif

  modal_flux=0.0d0
  do a=1,nmode
    do ifloor=1,nfloor
      do l=1,nsct
        do n=1,npq
          modal_flux(l,ifloor,a)=modal_flux(l,ifloor,a)+dn(l,n)*cell(n,a,ifloor)
        enddo
      enddo
    enddo
  enddo
  modal_cour=0.0d0
  do a=1,nmode
    do iface=1,nfloor+1
      do n=1,npq
        modal_cour(iface,a)=modal_cour(iface,a)+real(w(n),dp)* &
          real(du(n),dp)*face(n,a,iface)
      enddo
    enddo
  enddo

  flux=0.0
  cour=0.0
  xnei=0.0
  do i=1,nreg2d
    do a=1,nmode
      do ifloor=1,nfloor
        do l=1,nsct
          flux(1,l,ifloor,i)=flux(1,l,ifloor,i)+ &
            basis(i,a)*modal_flux(l,ifloor,a)
        enddo
      enddo
      do iface=1,nfloor+1
        cour(iface,i)=cour(iface,i)+basis(i,a)*modal_cour(iface,a)
      enddo
      do n=1,npq
        xnei(n,i)=xnei(n,i)+basis(i,a)*face(n,a,1)
      enddo
    enddo
  enddo
  if (any(.not.ieee_is_finite(flux)) .or. &
      any(.not.ieee_is_finite(cour)) .or. &
      any(.not.ieee_is_finite(xnei))) &
    call XABORT('SPOT1P: NON-FINITE RECONSTRUCTED SOLUTION.')

  deallocate(opposite,modal_cour,modal_flux,cell,face)
  deallocate(dn,mn,source_m,scat_m,radial_m,total_m,mass_m,weight)
  return

contains

  subroutine rank1_identity(phase,active)
    integer, intent(in) :: phase
    logical, intent(out) :: active
    integer(int64), allocatable :: key(:)
    integer(int64) :: count_key,position,temporary_bytes
    integer :: aa,bb,rr,ss,zz,ll,nn
    logical :: eligible
    active=.false.
    if (.not.SPOT1P64_RANK1_ENABLED()) return
    eligible=nmode == 1 .and. nreg2d > 1 .and. .not.any(ncode == 4)
    if (phase == 1) then
      count_key=17_int64
      call key_count_add(count_key,size(mat1d,kind=int64))
      call key_count_add(count_key,size(mat,kind=int64))
      call key_count_add(count_key,size(vol1d,kind=int64))
      call key_count_add(count_key,size(total,kind=int64))
      call key_count_add(count_key,size(sgas,kind=int64))
      call key_count_add(count_key,size(basis,kind=int64))
      call key_count_add(count_key,size(vol2d,kind=int64))
      call key_count_add(count_key,size(radial2d,kind=int64))
      call key_count_add(count_key,size(du,kind=int64))
      call key_count_add(count_key,size(w,kind=int64))
      call key_count_add(count_key,size(pl,kind=int64))
      call key_count_add(count_key,size(zcode,kind=int64))
    else
      count_key=2_int64
      call key_count_add(count_key,size(weight,kind=int64))
      call key_count_add(count_key,size(mass_m,kind=int64))
      call key_count_add(count_key,size(total_m,kind=int64))
      call key_count_add(count_key,size(radial_m,kind=int64))
      call key_count_add(count_key,size(scat_m,kind=int64))
      call key_count_add(count_key,size(mn,kind=int64))
      call key_count_add(count_key,size(dn,kind=int64))
      if (AXMAT_WHITE_ON) then
        call key_count_add(count_key,size(white_angle,kind=int64))
        call key_count_add(count_key,size(white_mode,kind=int64))
      endif
    endif
    if (count_key < 0_int64 .or. count_key > 536870912_int64/8_int64) &
      call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
    temporary_bytes=8_int64*count_key
    call SPOT1P64_RANK1_RESERVE(temporary_bytes)
    allocate(key(count_key))
    position=0_int64
    if (phase == 1) then
      call key_integer(key,position,nreg2d)
      call key_integer(key,position,nfloor)
      call key_integer(key,position,ielem)
      call key_integer(key,position,nmat)
      call key_integer(key,position,nsnap)
      call key_integer(key,position,nmode)
      call key_integer(key,position,ischm)
      call key_integer(key,position,npq)
      call key_integer(key,position,nsct)
      call key_integer(key,position,merge(1,0,lfixup))
      call key_integer(key,position,merge(1,0,AXMAT_WHITE_ON))
      call key_integer(key,position,AXMAT_WHITE_ROW)
      call key_real64(key,position,AXMAT_WHITE_PERIMETER)
      call key_integer(key,position,ncode(1))
      call key_integer(key,position,ncode(2))
      ! Explicit ABI is also part of the immutable identity.
      call key_integer(key,position,storage_size(0.0))
      call key_integer(key,position,storage_size(0.0d0))
      do zz=1,nfloor
        call key_integer(key,position,mat1d(zz))
        call key_real32(key,position,vol1d(zz))
      enddo
      do rr=1,nreg2d
        do zz=1,nfloor
          call key_integer(key,position,mat(zz,rr))
        enddo
      enddo
      do rr=0,nmat
        call key_real32(key,position,total(rr))
      enddo
      do ll=1,nsct
        do rr=0,nmat
          call key_real32(key,position,sgas(rr,ll))
        enddo
      enddo
      do aa=1,nmode
        do rr=1,nreg2d
          call key_real32(key,position,basis(rr,aa))
        enddo
      enddo
      do rr=1,nreg2d
        call key_real32(key,position,vol2d(rr))
      enddo
      do ss=1,nsnap
        do rr=1,nreg2d
          call key_real64(key,position,radial2d(rr,ss))
        enddo
      enddo
      do nn=1,npq
        call key_real32(key,position,du(nn))
        call key_real32(key,position,w(nn))
        do ll=1,nsct
          call key_real32(key,position,pl(ll,nn))
        enddo
      enddo
      call key_real32(key,position,zcode(1))
      call key_real32(key,position,zcode(2))
    else
      call key_real64(key,position,albedo_left)
      call key_real64(key,position,albedo_right)
      do rr=1,nreg2d
        call key_real64(key,position,weight(rr))
      enddo
      do bb=1,nmode
        do aa=1,nmode
          call key_real64(key,position,mass_m(aa,bb))
        enddo
      enddo
      do zz=1,nfloor
        do bb=1,nmode
          do aa=1,nmode
            call key_real64(key,position,total_m(aa,bb,zz))
            call key_real64(key,position,radial_m(aa,bb,zz))
          enddo
        enddo
      enddo
      do zz=1,nfloor
        do ll=1,nsct
          do bb=1,nmode
            do aa=1,nmode
              call key_real64(key,position,scat_m(aa,bb,ll,zz))
            enddo
          enddo
        enddo
      enddo
      do ll=1,nsct
        do nn=1,npq
          call key_real64(key,position,mn(nn,ll))
          call key_real64(key,position,dn(ll,nn))
        enddo
      enddo
      if (AXMAT_WHITE_ON) then
        do nn=1,npq
          do rr=1,npq
            call key_real64(key,position,white_angle(rr,nn))
          enddo
        enddo
        do bb=1,nmode
          do aa=1,nmode
            call key_real64(key,position,white_mode(aa,bb))
          enddo
        enddo
      endif
    endif
    if (position /= count_key) &
      call XABORT('SPOT1P64 RANK1 CACHE: IDENTITY LENGTH ERROR.')
    call SPOT1P64_RANK1_GUARD(igroup,key,phase,eligible,active)
    deallocate(key)
    call SPOT1P64_RANK1_RELEASE(temporary_bytes)
  end subroutine rank1_identity

  subroutine key_count_add(total,amount)
    integer(int64), intent(inout) :: total
    integer(int64), intent(in) :: amount
    if (amount < 0_int64 .or. amount > 536870912_int64/8_int64-total) &
      call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
    total=total+amount
  end subroutine key_count_add

  subroutine key_integer(key,position,value)
    integer(int64), intent(inout) :: key(:),position
    integer, intent(in) :: value
    position=position+1_int64
    key(position)=int(value,int64)
  end subroutine key_integer

  subroutine key_real32(key,position,value)
    integer(int64), intent(inout) :: key(:),position
    real, intent(in) :: value
    position=position+1_int64
    key(position)=int(transfer(value,0_int32),int64)
  end subroutine key_real32

  subroutine key_real64(key,position,value)
    integer(int64), intent(inout) :: key(:),position
    double precision, intent(in) :: value
    position=position+1_int64
    key(position)=transfer(value,0_int64)
  end subroutine key_real64

  subroutine boundary_solve(first_mode,last_mode,face_flux,cell_flux, &
                            left_albedo,right_albedo)
    integer, intent(in) :: first_mode,last_mode
    double precision, intent(inout) :: face_flux(npq,nmode,nfloor+1)
    double precision, intent(inout) :: cell_flux(npq,nmode,nfloor)
    double precision, intent(in) :: left_albedo,right_albedo
    double precision, allocatable :: lower(:,:,:),diagonal(:,:,:)
    double precision, allocatable :: upper(:,:,:),right_hand(:,:)
    double precision, allocatable :: cprime(:,:,:),dprime(:,:)
    double precision, allocatable :: solution(:,:),augmented(:,:)
    double precision, allocatable :: solve_pack(:,:),rhs_one(:,:)
    double precision, allocatable :: rank1_lower_work(:,:)
    integer(int64) :: rank1_lower_work_bytes
    double precision :: h,kvalue,svalue
    integer :: block,iz,ia,ib,in,jn,il,ir,ic,info,local_state
    logical :: cached_path,cache_hit

    local_state=(last_mode-first_mode+1)*npq
    cached_path=use_factor_cache.and.(first_mode == last_mode)
    cache_hit=.false.
    if (cached_path) then
      associate(plan => SPOT1P64_PLAN(igroup)%mode(first_mode))
        cache_hit=plan%ready
        if (cache_hit) then
          if (plan%nstate /= local_state .or. plan%nblock /= nfloor+1) &
            call XABORT('SPOT1P64 CACHE: BLOCK DIMENSIONS CHANGED INSIDE FLU.')
          if (rank1_identity_active) then
            call SPOT1P64_RANK1_LOWER_VALIDATE(igroup,local_state,nfloor+1,du)
          else
          if (.not.allocated(plan%lower)) &
            call XABORT('SPOT1P64 CACHE: MISSING STORED LOWER BLOCKS.')
          if (size(plan%lower,1) /= local_state .or. &
              size(plan%lower,2) /= local_state .or. &
              size(plan%lower,3) /= nfloor+1) &
            call XABORT('SPOT1P64 CACHE: INVALID STORED LOWER BLOCKS.')
          endif
        endif
      end associate
    endif
    if (.not.cache_hit) then
      allocate(lower(local_state,local_state,nfloor+1))
      allocate(diagonal(local_state,local_state,nfloor+1))
      allocate(upper(local_state,local_state,nfloor+1))
      lower=0.0d0
      diagonal=0.0d0
      upper=0.0d0
    endif
    allocate(right_hand(local_state,nfloor+1))
    allocate(dprime(local_state,nfloor+1),solution(local_state,nfloor+1))
    if (cached_path) then
      if (cache_hit) then
        if (rank1_identity_active) then
          if (int(local_state,int64) > 536870912_int64/8_int64/int(local_state,int64)) &
            call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
          rank1_lower_work_bytes=8_int64*int(local_state,int64)*int(local_state,int64)
          call SPOT1P64_RANK1_RESERVE(rank1_lower_work_bytes)
          allocate(rank1_lower_work(local_state,local_state))
        endif
        allocate(rhs_one(local_state,1))
      else
        allocate(solve_pack(local_state,local_state+1))
      endif
    else
      allocate(cprime(local_state,local_state,nfloor+1))
      allocate(augmented(local_state,2*local_state+1))
    endif
    right_hand=0.0d0

    do block=0,nfloor
      do ia=first_mode,last_mode
        do in=1,npq
          ir=(ia-first_mode)*npq+in
          if (du(in) > 0.0) then
            if (block == 0) then
              if (.not.cache_hit) then
                diagonal(ir,ir,1)=1.0d0
                diagonal(ir,(ia-first_mode)*npq+opposite(in),1)= &
                  -left_albedo
              endif
              cycle
            endif
            iz=block
          else
            if (block == nfloor) then
              if (.not.cache_hit) then
                diagonal(ir,ir,nfloor+1)=1.0d0
                diagonal(ir,(ia-first_mode)*npq+opposite(in),nfloor+1)= &
                  -right_albedo
              endif
              cycle
            endif
            iz=block+1
          endif

          h=real(vol1d(iz),dp)
          svalue=0.0d0
          do il=1,nsct
            svalue=svalue+mn(in,il)*source_m(il,iz,ia)
          enddo
          right_hand(ir,block+1)=h*svalue

          if (cache_hit) cycle

          do ib=first_mode,last_mode
            do jn=1,npq
              ic=(ib-first_mode)*npq+jn
              kvalue=0.0d0
              if (in == jn) kvalue=kvalue+total_m(ia,ib,iz)
              do il=1,nsct
                kvalue=kvalue-mn(in,il)*scat_m(ia,ib,il,iz)*dn(il,jn)
              enddo
              kvalue=kvalue+mn(in,1)*radial_m(ia,ib,iz)*dn(1,jn)
              ! Conditional constant side trace: conservative angular exchange.
              if (AXMAT_WHITE_ON) kvalue=kvalue+ &
                white_mode(ia,ib)*white_angle(in,jn)
              if (du(in) > 0.0) then
                lower(ir,ic,block+1)=0.5d0*h*kvalue
                diagonal(ir,ic,block+1)=0.5d0*h*kvalue
              else
                diagonal(ir,ic,block+1)=0.5d0*h*kvalue
                upper(ir,ic,block+1)=0.5d0*h*kvalue
              endif
            enddo
            ic=(ib-first_mode)*npq+in
            if (du(in) > 0.0) then
              lower(ir,ic,block+1)=lower(ir,ic,block+1)- &
                real(du(in),dp)*mass_m(ia,ib)
              diagonal(ir,ic,block+1)=diagonal(ir,ic,block+1)+ &
                real(du(in),dp)*mass_m(ia,ib)
            else
              diagonal(ir,ic,block+1)=diagonal(ir,ic,block+1)- &
                real(du(in),dp)*mass_m(ia,ib)
              upper(ir,ic,block+1)=upper(ir,ic,block+1)+ &
                real(du(in),dp)*mass_m(ia,ib)
            endif
          enddo
        enddo
      enddo
    enddo

    if (cached_path) then
      associate(plan => SPOT1P64_PLAN(igroup)%mode(first_mode))
        if (cache_hit) then
          if (rank1_identity_active) then
            if (.not.allocated(plan%factor) .or. .not.allocated(plan%cprime)) &
              call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
            if (any(shape(plan%factor) /= (/local_state-1,local_state,nfloor+1/))) &
              call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
            if (any(shape(plan%cprime) /= (/local_state,local_state,nfloor/))) &
              call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
          endif
          do block=1,nfloor+1
            rhs_one(:,1)=right_hand(:,block)
            if (rank1_identity_active) then
              if (block > 1) then
                call SPOT1P64_RANK1_LOWER_LOAD(igroup,block,rank1_lower_work,du,.true.)
                rhs_one(:,1)=rhs_one(:,1)- &
                  matmul(rank1_lower_work,dprime(:,block-1))
              endif
            else
            if (block > 1) rhs_one(:,1)=rhs_one(:,1)- &
              matmul(plan%lower(:,:,block),dprime(:,block-1))
            endif
            if (rank1_identity_active) then
              call SPOT1P64_RANK1_FACTOR_LOAD(igroup,block,rank1_lower_work)
              call SPOT1P64_SOLVE64(rank1_lower_work, &
                plan%pivot(:,block),plan%pivot_value(:,block), &
                rhs_one,info)
            else
            call SPOT1P64_SOLVE64(plan%factor(:,:,block), &
              plan%pivot(:,block),plan%pivot_value(:,block), &
              rhs_one,info)
            endif
            if (info /= 0) &
              call XABORT('SPOT1P64 CACHE: INVALID STORED FACTOR.')
            dprime(:,block)=rhs_one(:,1)
          enddo
          call SPOT1P64_CACHE_NOTE_REUSE(nfloor+1)
        else
          plan%nstate=local_state
          plan%nblock=nfloor+1
          if (rank1_identity_active) &
            call SPOT1P64_RANK1_FACTORS(igroup,local_state,nfloor+1,count(du > 0.0))
          allocate(plan%factor(local_state,local_state,nfloor+1))
          allocate(plan%pivot(local_state,nfloor+1))
          allocate(plan%pivot_value(local_state,nfloor+1))
          if (rank1_identity_active) then
            allocate(plan%cprime(local_state,local_state,nfloor))
          else
            allocate(plan%cprime(local_state,local_state,nfloor+1))
          endif
          if (rank1_identity_active) then
            call SPOT1P64_RANK1_LOWER_STORE(igroup,lower,du)
          else
          allocate(plan%lower(local_state,local_state,nfloor+1))
          plan%lower=lower
          endif
          do block=1,nfloor+1
            if (block == 1) then
              plan%factor(:,:,block)=diagonal(:,:,block)
              solve_pack(:,local_state+1)=right_hand(:,block)
            else
              plan%factor(:,:,block)=diagonal(:,:,block)- &
                matmul(lower(:,:,block),plan%cprime(:,:,block-1))
              solve_pack(:,local_state+1)=right_hand(:,block)- &
                matmul(lower(:,:,block),dprime(:,block-1))
            endif
            call SPOT1P64_FACTOR64(plan%factor(:,:,block), &
              plan%pivot(:,block),plan%pivot_value(:,block),info)
            if (info /= 0) then
              if (block == 1) then
                call XABORT('SPOT1P: SINGULAR FIRST AXIAL BLOCK.')
              else
                call XABORT('SPOT1P: SINGULAR AXIAL SCHUR BLOCK.')
              endif
            endif
            solve_pack(:,:local_state)=upper(:,:,block)
            call SPOT1P64_SOLVE64(plan%factor(:,:,block), &
              plan%pivot(:,block),plan%pivot_value(:,block),solve_pack,info)
            if (info /= 0) &
              call XABORT('SPOT1P64 CACHE: NEW FACTOR SOLVE FAILED.')
            if (.not.rank1_identity_active .or. block <= nfloor) &
              plan%cprime(:,:,block)=solve_pack(:,:local_state)
            dprime(:,block)=solve_pack(:,local_state+1)
          enddo
          if (rank1_identity_active) call SPOT1P64_RANK1_FACTOR_PACK(igroup)
          plan%ready=.true.
          call SPOT1P64_CACHE_NOTE_BUILD(nfloor+1)
        endif
      end associate
    else
      augmented=0.0d0
      augmented(:,:local_state)=diagonal(:,:,1)
      augmented(:,local_state+1:2*local_state)=upper(:,:,1)
      augmented(:,2*local_state+1)=right_hand(:,1)
      call ALSBD(local_state,local_state+1,augmented,info,local_state)
      if (info /= 0) call XABORT('SPOT1P: SINGULAR FIRST AXIAL BLOCK.')
      cprime(:,:,1)=augmented(:,local_state+1:2*local_state)
      dprime(:,1)=augmented(:,2*local_state+1)

      do block=2,nfloor+1
        augmented=0.0d0
        augmented(:,:local_state)=diagonal(:,:,block)- &
          matmul(lower(:,:,block),cprime(:,:,block-1))
        augmented(:,local_state+1:2*local_state)=upper(:,:,block)
        augmented(:,2*local_state+1)=right_hand(:,block)- &
          matmul(lower(:,:,block),dprime(:,block-1))
        call ALSBD(local_state,local_state+1,augmented,info,local_state)
        if (info /= 0) call XABORT('SPOT1P: SINGULAR AXIAL SCHUR BLOCK.')
        cprime(:,:,block)=augmented(:,local_state+1:2*local_state)
        dprime(:,block)=augmented(:,2*local_state+1)
      enddo
    endif

    solution(:,nfloor+1)=dprime(:,nfloor+1)
    if (cached_path) then
      associate(plan => SPOT1P64_PLAN(igroup)%mode(first_mode))
        do block=nfloor,1,-1
          solution(:,block)=dprime(:,block)- &
            matmul(plan%cprime(:,:,block),solution(:,block+1))
        enddo
      end associate
    else
      do block=nfloor,1,-1
        solution(:,block)=dprime(:,block)- &
          matmul(cprime(:,:,block),solution(:,block+1))
      enddo
    endif
    do block=1,nfloor+1
      do ia=first_mode,last_mode
        do in=1,npq
          face_flux(in,ia,block)= &
            solution((ia-first_mode)*npq+in,block)
        enddo
      enddo
    enddo
    do iz=1,nfloor
      cell_flux(:,first_mode:last_mode,iz)=0.5d0* &
        (face_flux(:,first_mode:last_mode,iz)+ &
         face_flux(:,first_mode:last_mode,iz+1))
    enddo

    if (allocated(augmented)) deallocate(augmented)
    if (allocated(solve_pack)) deallocate(solve_pack)
    if (allocated(rhs_one)) deallocate(rhs_one)
    if (allocated(rank1_lower_work)) then
      deallocate(rank1_lower_work)
      call SPOT1P64_RANK1_RELEASE(rank1_lower_work_bytes)
    endif
    if (allocated(cprime)) deallocate(cprime)
    deallocate(solution,dprime,right_hand)
    if (allocated(upper)) deallocate(upper,diagonal,lower)
  end subroutine boundary_solve

  subroutine translation_solve(first_mode,last_mode,face_flux,cell_flux, &
                               left_albedo,right_albedo)
    integer, intent(in) :: first_mode,last_mode
    double precision, intent(inout) :: face_flux(npq,nmode,nfloor+1)
    double precision, intent(inout) :: cell_flux(npq,nmode,nfloor)
    double precision, intent(in) :: left_albedo,right_albedo
    double precision, allocatable :: affine(:),response(:,:),system(:,:)
    integer :: local_state,ico,ia,ib,in,jn,row,info

    local_state=(last_mode-first_mode+1)*npq
    allocate(affine(local_state),response(local_state,local_state))
    allocate(system(local_state,local_state+1))

    face_flux(:,first_mode:last_mode,:)=0.0d0
    call sweep(first_mode,last_mode,face_flux,cell_flux)
    do ia=first_mode,last_mode
      do in=1,npq
        row=(ia-first_mode)*npq+in
        affine(row)=face_flux(in,ia,nfloor+1)
      enddo
    enddo

    do ico=1,local_state
      face_flux(:,first_mode:last_mode,:)=0.0d0
      ia=first_mode+(ico-1)/npq
      in=mod(ico-1,npq)+1
      face_flux(in,ia,1)=1.0d0
      call sweep(first_mode,last_mode,face_flux,cell_flux)
      do ib=first_mode,last_mode
        do jn=1,npq
          row=(ib-first_mode)*npq+jn
          response(row,ico)=face_flux(jn,ib,nfloor+1)-affine(row)
        enddo
      enddo
    enddo

    system=0.0d0
    do ia=first_mode,last_mode
      do in=1,npq
        row=(ia-first_mode)*npq+in
        if (du(in) > 0.0) then
          system(row,:local_state)=-left_albedo*response(row,:)
          system(row,row)=system(row,row)+1.0d0
          system(row,local_state+1)=left_albedo*affine(row)
        else
          system(row,:local_state)=response(row,:)
          system(row,row)=system(row,row)-right_albedo
          system(row,local_state+1)=-affine(row)
        endif
      enddo
    enddo

    call ALSBD(local_state,1,system,info,local_state)
    if (info /= 0) call XABORT('SPOT1P: SINGULAR MODAL BOUNDARY SYSTEM.')
    face_flux(:,first_mode:last_mode,:)=0.0d0
    do ia=first_mode,last_mode
      do in=1,npq
        row=(ia-first_mode)*npq+in
        face_flux(in,ia,1)=system(row,local_state+1)
      enddo
    enddo
    call sweep(first_mode,last_mode,face_flux,cell_flux)

    deallocate(system,response,affine)
  end subroutine translation_solve

  subroutine sweep(first_mode,last_mode,face_flux,cell_flux)
    integer, intent(in) :: first_mode,last_mode
    double precision, intent(inout) :: face_flux(npq,nmode,nfloor+1)
    double precision, intent(inout) :: cell_flux(npq,nmode,nfloor)
    double precision, allocatable :: amat(:,:)
    double precision :: h,rhs
    integer :: iz,ia,ib,in,jn,il,ir,ic,info,local_state

    local_state=(last_mode-first_mode+1)*npq
    allocate(amat(local_state,local_state+1))
    cell_flux(:,first_mode:last_mode,:)=0.0d0
    do iz=1,nfloor
      h=real(vol1d(iz),dp)
      amat=0.0d0
      do ia=first_mode,last_mode
        do in=1,npq
          ir=(ia-first_mode)*npq+in
          rhs=0.0d0
          do ib=first_mode,last_mode
            do jn=1,npq
              ic=(ib-first_mode)*npq+jn
              if (in == jn) amat(ir,ic)=amat(ir,ic)+h*total_m(ia,ib,iz)
              do il=1,nsct
                amat(ir,ic)=amat(ir,ic)-h*mn(in,il)* &
                  scat_m(ia,ib,il,iz)*dn(il,jn)
              enddo
              amat(ir,ic)=amat(ir,ic)+h*mn(in,1)* &
                radial_m(ia,ib,iz)*dn(1,jn)
            enddo
            ic=(ib-first_mode)*npq+in
            amat(ir,ic)=amat(ir,ic)+2.0d0*real(du(in),dp)* &
              mass_m(ia,ib)
            rhs=rhs+2.0d0*real(du(in),dp)*mass_m(ia,ib)* &
              face_flux(in,ib,iz)
          enddo
          do il=1,nsct
            rhs=rhs+h*mn(in,il)*source_m(il,iz,ia)
          enddo
          amat(ir,local_state+1)=rhs
        enddo
      enddo
      call ALSBD(local_state,1,amat,info,local_state)
      if (info /= 0) call XABORT('SPOT1P: SINGULAR LOCAL MODAL SYSTEM.')
      do ia=first_mode,last_mode
        do in=1,npq
          ir=(ia-first_mode)*npq+in
          cell_flux(in,ia,iz)=amat(ir,local_state+1)
          face_flux(in,ia,iz+1)=2.0d0*cell_flux(in,ia,iz)- &
            face_flux(in,ia,iz)
        enddo
      enddo
    enddo
    deallocate(amat)
  end subroutine sweep

end subroutine SPOT1P64
