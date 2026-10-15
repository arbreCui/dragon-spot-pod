import hashlib, json, pathlib, re, difflib

D=pathlib.Path('/private/tmp/axmat-rank1-cross-group-identity-key-delta-source-v11-20261009')
P=pathlib.Path('/Users/wen/spot/validation/axial_material/factor_diagonal_trim_source_v10_20261009/SPOT1P64.f90')
S=P.read_text()
assert hashlib.sha256(S.encode()).hexdigest()=='5e0d4afc9a4ebfb6f26b2e3c4ab98c53f501afa861c33a098e6ab55031c5e809'
edits=[]
def edit(name, old, new):
    global S
    assert S.count(old)==1,(name,S.count(old))
    edits.append(dict(name=name,old=old,new=new))
    S=S.replace(old,new,1)

edit('plan_integer_key_metadata',
'''    integer(int64), allocatable :: rank1_raw_bits(:),rank1_operator_bits(:)
''',
'''    integer(int64), allocatable :: rank1_raw_bits(:),rank1_operator_bits(:)
    ! bits stores either the original full key or only differing values.
    ! Allocated positions (including length zero) selects the delta format.
    integer(int64) :: rank1_raw_size=0_int64,rank1_operator_size=0_int64
    integer(int32), allocatable :: rank1_raw_positions(:),rank1_operator_positions(:)
''')
edit('two_full_base_owner_indices',
'''  integer(int64), save :: rank1_validated_hits=0_int64
''',
'''  integer(int64), save :: rank1_validated_hits=0_int64
  ! Owners refer only to the first full key of each phase in this lifecycle.
  integer, save :: rank1_raw_base_owner=0,rank1_operator_base_owner=0
''')
edit('public_complete_integer_key_decoder',
'''  public :: SPOT1P64_RANK1_RELEASE,SPOT1P64_RANK1_GUARD
''',
'''  public :: SPOT1P64_RANK1_RELEASE,SPOT1P64_RANK1_GUARD
  public :: SPOT1P64_RANK1_KEY_LOAD,SPOT1P64_RANK1_KEY_STATS
''')
edit('clear_both_full_base_owners',
'''    rank1_validated_hits=0_int64
  end subroutine SPOT1P64_CACHE_CLEAR
''',
'''    rank1_validated_hits=0_int64
    rank1_raw_base_owner=0
    rank1_operator_base_owner=0
  end subroutine SPOT1P64_CACHE_CLEAR
''')

guard=re.search(r'(?ms)^  subroutine SPOT1P64_RANK1_GUARD\(.*?^  end subroutine SPOT1P64_RANK1_GUARD\n',S).group()
new_guard=guard.replace('''          if (size(plan%rank1_raw_bits) /= size(key)) &
            call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
          if (any(plan%rank1_raw_bits /= key)) &
            call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
''','''          call SPOT1P64_RANK1_KEY_MATCH(igroup,key,phase)
''').replace('''          call SPOT1P64_RANK1_RESERVE(amount)
          allocate(plan%rank1_raw_bits(size(key)))
          plan%rank1_raw_bits=key
''','''          call SPOT1P64_RANK1_KEY_STORE(igroup,key,phase)
''').replace('''          if (size(plan%rank1_operator_bits) /= size(key)) &
            call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
          if (any(plan%rank1_operator_bits /= key)) &
            call XABORT('SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
''','''          call SPOT1P64_RANK1_KEY_MATCH(igroup,key,phase)
''').replace('''          call SPOT1P64_RANK1_RESERVE(amount)
          allocate(plan%rank1_operator_bits(size(key)))
          plan%rank1_operator_bits=key
''','''          call SPOT1P64_RANK1_KEY_STORE(igroup,key,phase)
''')
assert new_guard!=guard
edit('guard_complete_integer_comparison_and_actual_storage',guard,new_guard)

helpers='''  ! Source-only V11 candidate. No floating operation is performed here.
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

'''
anchor='  subroutine SPOT1P64_RANK1_FACTORS(igroup,nstate,nblock,npositive)\n'
edit('integer_only_key_helpers',anchor,helpers+anchor)

candidate=D/'SPOT1P64.f90'
candidate.write_text(S)
inverse=S
for e in reversed(edits):
    assert inverse.count(e['new'])==1,e['name']
    inverse=inverse.replace(e['new'],e['old'],1)
assert inverse.encode()==P.read_bytes()
(D/'region_edits.json').write_text(json.dumps(edits,indent=2)+'\n')
(D/'source.diff').write_text(''.join(difflib.unified_diff(P.read_text().splitlines(True),S.splitlines(True),fromfile=str(P),tofile=str(candidate))))
names=['SPOT1P64_FACTOR64','SPOT1P64_SOLVE64','SPOT1P64_RANK1_FACTORS','SPOT1P64_RANK1_FACTOR_PACK','SPOT1P64_RANK1_FACTOR_LOAD','SPOT1P64_RANK1_LOWER_STORE','SPOT1P64_RANK1_LOWER_VALIDATE','SPOT1P64_RANK1_LOWER_LOAD','rank1_identity','key_count_add','key_integer','key_real32','key_real64','boundary_solve','translation_solve']
retained={}
for n in names:
    pat=r'(?ms)^  subroutine '+re.escape(n)+r'\(.*?^  end subroutine '+re.escape(n)+r'\n'
    a=re.findall(pat,P.read_text());b=re.findall(pat,S)
    assert len(a)==1 and a==b,n
    retained[n]=hashlib.sha256(a[0].encode()).hexdigest()
assert all(len(line)<=132 for line in helpers.splitlines())
report=dict(status='SOURCE_ONLY_DRAFT',draft_status='UNREADY',candidate_path=str(candidate),candidate_sha256=hashlib.sha256(S.encode()).hexdigest(),
    parent_path=str(P),parent_sha256=hashlib.sha256(P.read_bytes()).hexdigest(),complete_inverse_byteexact=True,region_count=len(edits),
    floating_and_operator_source_retained=retained,original_full_temporary_key_builder_byteexact=True,
    public_guard_signature_and_original_eligibility_phase_order_retained=True,original_phase2_missing_raw_gate_retained=True,
    descriptor_bytes_per_group=4096,accounted_cap_bytes=536870912,
    actual_compile=None,actual_controls=None,actual_native_RSS=None,actual_native_AAA=None,
    cross_group_key_sharing='First full key owner per phase; subsequent same-size keys use int32 positions + int64 differences iff 12*d < 8*n; otherwise original full int64 storage.',
    complete_integer_key_comparison=True,zero_difference_delta=True,no_hash_identity=True,no_float_key_conversion=True,
    no_business_execution=True,project_written=False)
(D/'source_inverse_proof.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ('status','candidate_sha256','complete_inverse_byteexact','region_count')}))
