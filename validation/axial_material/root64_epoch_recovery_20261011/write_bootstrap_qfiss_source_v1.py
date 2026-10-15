"""Source-only writer: no compiler, parser, transport, or numerical execution."""
from pathlib import Path
import hashlib, json, re, time

ROOT = Path('/Users/wen/spot')
REC = ROOT / 'validation/axial_material/root64_epoch_recovery_20261011'
OUT = REC / 'bootstrap_qfiss_source_v1'
OUT.mkdir(exist_ok=True)
(OUT / 'original_exact').mkdir(exist_ok=True)
started = time.monotonic()

def pin(path):
    path = Path(path)
    stat = path.stat()
    return {'path': str(path), 'bytes': stat.st_size,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'seven_id': [stat.st_dev, stat.st_ino, stat.st_mode, stat.st_nlink,
                         stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns]}

class Transform:
    def __init__(self, original):
        self.original = original
        self.data = original
        self.changes = []
    def replace(self, old, new, label):
        assert self.data.count(old) == 1, (label, self.data.count(old))
        at = self.data.index(old)
        self.changes.append({'label': label, 'offset_before': at,
                             'old': old, 'new': new})
        self.data = self.data[:at] + new + self.data[at+len(old):]
    def finish(self, name, input_path):
        undo = self.data
        for change in reversed(self.changes):
            at = change['offset_before']
            assert undo[at:at+len(change['new'])] == change['new']
            undo = undo[:at] + change['old'] + undo[at+len(change['new']):]
        assert undo == self.original
        (OUT / name).write_text(self.data)
        (OUT / 'original_exact' / Path(input_path).name).write_text(self.original)
        (OUT / (name + '.exact_local_byte_inverse.json')).write_text(json.dumps({
            'original_input': pin(input_path), 'new_source': pin(OUT / name),
            'complete_original_reconstructed_exactly': True,
            'changes': self.changes,
            'original_sha256': hashlib.sha256(self.original.encode()).hexdigest()
        }, indent=2) + '\n')

# Preserve the complete frozen SPOSTATE64 mathematics, turning its publication
# into read-only, exact-bit comparison against the actual canonical AX records.
CAN = REC / 'continuous_chain_source/SPOSTATE64.f90'
t = Transform(CAN.read_text())
prefix = t.data[:t.data.index('subroutine SPOSTATE64(')]
t.replace(prefix, '''module SPOR64_BOOT_CANONICAL64
  ! NEW SOURCE. Full SPOSTATE64 mathematics, canonical write and recomputation.
  ! Context equality and host full-file pins are separate from solver provenance.
  use, intrinsic :: iso_c_binding, only : c_ptr, c_associated
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use GANLIB
  use SPOR64_VERIFY, only : RECORD_MATCHES, CHARACTER_RECORD_MATCHES
  implicit none
  private
  public :: SPOR64_BOOT_CANONICAL64_CHECK,SPOR64_BOOT_CANONICAL64_WRITE
contains
  subroutine SPOR64_BOOT_CANONICAL64_CHECK(ipax,iptrack,ipsystem,ipmacro,ok)
    type(c_ptr), intent(in) :: ipax,iptrack,ipsystem,ipmacro
    logical, intent(out) :: ok
    call CANONICAL_CORE(ipax,iptrack,ipsystem,ipmacro,.false.,ok)
  end subroutine SPOR64_BOOT_CANONICAL64_CHECK
  subroutine SPOR64_BOOT_CANONICAL64_WRITE(ipax,iptrack,ipsystem,ipmacro,ok)
    type(c_ptr), intent(in) :: ipax,iptrack,ipsystem,ipmacro
    logical, intent(out) :: ok
    call CANONICAL_CORE(ipax,iptrack,ipsystem,ipmacro,.true.,ok)
  end subroutine SPOR64_BOOT_CANONICAL64_WRITE
''', 'new standalone module')
t.replace('subroutine SPOSTATE64(nentry,hentry,ientry,jentry,kentry)',
          'subroutine CANONICAL_CORE(ipax,iptrack,ipsystem,ipmacro,write_mode,ok)',
          'new read-only ABI')
t.replace('  integer, intent(in) :: nentry,ientry(nentry),jentry(nentry)\n'
          '  character(len=12), intent(in) :: hentry(nentry)\n'
          '  type(c_ptr), intent(in) :: kentry(nentry)',
          '  type(c_ptr), intent(in) :: ipax,iptrack,ipsystem,ipmacro\n'
          '  type(c_ptr) :: kentry(4)\n'
          '  logical, intent(out) :: ok\n'
          '  logical, intent(in) :: write_mode\n'
          '  logical :: solve_ok', 'explicit immutable inputs')
start = t.data.index('  if (nentry /= 4)')
stop = t.data.index("  call require_record(kentry(1),'SIGNATURE'")
t.replace(t.data[start:stop], '''  ok=.false.
  if (.not.c_associated(ipax).or..not.c_associated(iptrack).or. &
      .not.c_associated(ipsystem).or..not.c_associated(ipmacro)) return
  kentry=[ipax,iptrack,ipsystem,ipmacro]

''', 'ordinary fail-closed entry and no CLE parser')
require_start = t.data.index('  subroutine require_record(')
require_end = t.data.index('  end subroutine require_record', require_start)
require_end += len('  end subroutine require_record\n')
t.replace(t.data[require_start:require_end], '', 'shared record primitives')
for match in list(re.finditer(r'  call require_record\((.*?)\)(?=\s*\n)', t.data, re.S))[::-1]:
    whole = match.group(0)
    args = re.sub(r'\s*&\s*', '', match.group(1)).replace('\n', '').split(',')
    assert len(args) == 5, args
    replacement = '  if (.not. RECORD_MATCHES(' + ','.join(args[:4]) + ')) return'
    t.replace(whole, replacement, 'mandatory typed record '+args[1])
t.replace('  ngrp=iflux(1)\n', '  ngrp=iflux(1)\n  if (ngrp /= 370.or.imacro(4) /= 32) return\n',
          'bootstrap exact 370 groups / 32 fission slots')
t.replace('    if (ilong == 0) cycle', '    if (ilong == 0) return',
          'every fission group is mandatory')
t.replace('      call solve_spd(gram,rhs,solution,nmode)',
          '      call solve_spd(gram,rhs,solution,nmode,solve_ok)\n'
          '      if (.not.solve_ok) return', 'SPD ordinary refusal')
# Change only the canonical publication tail: all preceding normalization,
# signed leakage, restriction, Gram assembly, and Cholesky operations survive.
publication_start = t.data.index('  version=1\n')
publication_end = t.data.index('  deallocate(height,offspace,basis_state,gram_flat,coordinates)')
checks = '''  version=1
  if (write_mode) then
    call LCMPUT(kentry(1),'SPOT-X-DIMS',4,1,[version,ngrp,nsnap,total_coef])
    call LCMPUT(kentry(1),'SPOT-X-RANK',ngrp,1,rank)
    call LCMPUT(kentry(1),'SPOT-X-OFF',ngrp+1,1,offset)
    call LCMPUT(kentry(1),'SPOT-X-GOFF',ngrp+1,1,gram_offset)
    call LCMPUT(kentry(1),'SPOT-X-BOFF',ngrp+1,1,basis_offset)
    call LCMPUT(kentry(1),'SPOT-X-A',total_coef,4,coordinates)
    call LCMPUT(kentry(1),'SPOT-X-GRAM',total_gram,4,gram_flat)
    call LCMPUT(kentry(1),'SPOT-X-BASIS',total_basis,2,basis_state)
    call LCMPUT(kentry(1),'SPOT-X-RHO',1,4,rho)
    call LCMPUT(kentry(1),'SPOT-X-KEFF',1,4,keff64)
    call LCMPUT(kentry(1),'SPOT-X-L',ngrp*nsnap,4,leak)
    call LCMPUT(kentry(1),'SPOT-X-H',nsnap,4,height)
    call LCMPUT(kentry(1),'SPOT-X-NORM',1,4,norm)
    call LCMPUT(kentry(1),'SPOT-X-PERP',ngrp*nsnap,4,offspace)
    call LCMPUT(kentry(1),'SPOT-X-GERR',1,4,gram_error)
    call LCMPUT(kentry(1),'SPOT-X-FIXB',1,1,fixb)
    call LCMPTC(kentry(1),'SPOT-X-NID',12,'NUFISS-UNIT ')
    call LCMPTC(kentry(1),'SPOT-X-BTYP',12,basis_type)
  else
  if (.not.CHECK_I(kentry(1),'SPOT-X-DIMS',[version,ngrp,nsnap,total_coef])) return
  if (.not.CHECK_I(kentry(1),'SPOT-X-RANK',rank)) return
  if (.not.CHECK_I(kentry(1),'SPOT-X-OFF',offset)) return
  if (.not.CHECK_I(kentry(1),'SPOT-X-GOFF',gram_offset)) return
  if (.not.CHECK_I(kentry(1),'SPOT-X-BOFF',basis_offset)) return
  if (.not.CHECK_64(kentry(1),'SPOT-X-A',coordinates)) return
  if (.not.CHECK_64(kentry(1),'SPOT-X-GRAM',gram_flat)) return
  if (.not.CHECK_32(kentry(1),'SPOT-X-BASIS',basis_state)) return
  if (.not.CHECK_64(kentry(1),'SPOT-X-RHO',[rho])) return
  if (.not.CHECK_64(kentry(1),'SPOT-X-KEFF',[keff64])) return
  if (.not.CHECK_64(kentry(1),'SPOT-X-L',leak)) return
  if (.not.CHECK_64(kentry(1),'SPOT-X-H',height)) return
  if (.not.CHECK_64(kentry(1),'SPOT-X-NORM',[norm])) return
  if (.not.CHECK_64(kentry(1),'SPOT-X-PERP',offspace)) return
  if (.not.CHECK_64(kentry(1),'SPOT-X-GERR',[gram_error])) return
  if (.not.CHECK_I(kentry(1),'SPOT-X-FIXB',[fixb])) return
  if (.not.CHARACTER_RECORD_MATCHES(kentry(1),'SPOT-X-NID',3,12,'NUFISS-UNIT')) return
  if (.not.CHARACTER_RECORD_MATCHES(kentry(1),'SPOT-X-BTYP',3,12,basis_type)) return
  endif
  ok=.true.

'''
t.replace(t.data[publication_start:publication_end], checks,
          'compare every canonical record instead of writing')
t.replace('  subroutine solve_spd(matrix,vector,result,n)',
          '  subroutine solve_spd(matrix,vector,result,n,ok)', 'explicit SPD validity')
t.replace('    integer :: row,col,k\n\n    lower=0.0_dp',
          '    integer :: row,col,k\n    logical, intent(out) :: ok\n\n'
          '    ok=.false.\n    result=0.0_dp\n    lower=0.0_dp', 'SPD initial invalid state')
t.replace('  end subroutine solve_spd', '    ok=.true.\n  end subroutine solve_spd', 'SPD final valid state')
for match in list(re.finditer(r"call XABORT\('[^'\n]*'\)", t.data))[::-1]:
    t.replace(match.group(0), 'return', 'ordinary guard refusal '+match.group(0))
# Helpers live at module scope; the original SPD remains internal to CHECK.
t.replace('end subroutine SPOSTATE64\n', '''end subroutine CANONICAL_CORE

  logical function CHECK_I(object,name,expected)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected(:)
    integer, allocatable :: actual(:)
    integer :: istat
    CHECK_I=.false.
    if (.not.RECORD_MATCHES(object,name,size(expected),1)) return
    allocate(actual(size(expected)),stat=istat)
    if (istat /= 0) return
    call LCMGET(object,name,actual)
    CHECK_I=all(actual == expected)
  end function CHECK_I

  logical function CHECK_32(object,name,expected)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name
    real(real32), intent(in) :: expected(:)
    real(real32), allocatable :: actual(:)
    integer :: istat
    CHECK_32=.false.
    if (.not.RECORD_MATCHES(object,name,size(expected),2)) return
    allocate(actual(size(expected)),stat=istat)
    if (istat /= 0) return
    call LCMGET(object,name,actual)
    CHECK_32=all(transfer(actual,0_int32,size(actual)) == &
                transfer(expected,0_int32,size(expected)))
  end function CHECK_32

  logical function CHECK_64(object,name,expected)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name
    real(real64), intent(in) :: expected(:)
    real(real64), allocatable :: actual(:)
    integer :: istat
    CHECK_64=.false.
    if (.not.RECORD_MATCHES(object,name,size(expected),4)) return
    allocate(actual(size(expected)),stat=istat)
    if (istat /= 0) return
    call LCMGET(object,name,actual)
    CHECK_64=all(transfer(actual,0_int64,size(actual)) == &
                transfer(expected,0_int64,size(expected)))
  end function CHECK_64
end module SPOR64_BOOT_CANONICAL64
''', 'read-only module comparison helpers')
assert 'XABORT' not in t.data and 'REDGET' not in t.data
t.finish('SPOR64_BOOT_CANONICAL64.f90', CAN)

# Full new explicit bootstrap ingress; its publisher must be separately wired
# to the actual terminal branch, and the independent host pins remain required.
context_source = (OUT / 'SPOR64_BOOT_CONTEXT64.f90.template').read_text()
# Publish a complete GLOBAL-only checker with the same actual numerical and
# full-context validations, allowing the independent publisher to preflight.
global_start = context_source.index('  subroutine SPOR64_BOOT_CONTEXT64_READ(')
global_stop = context_source.index('    ! One global/canonical authority is shared')
global_check = context_source[global_start:global_stop]
global_check = global_check.replace(
    'SPOR64_BOOT_CONTEXT64_READ(ipprojected,ipglobal,ipax,',
    'SPOR64_BOOT_CONTEXT64_GLOBAL_CHECK(ipglobal,ipax,')
global_check = global_check.replace(' :: ipprojected,ipglobal,ipax,ipaxtrack',
                                    ' :: ipglobal,ipax,ipaxtrack')
global_check = global_check.replace(
    '    if (.not.c_associated(ipprojected).or..not.c_associated(ipglobal)) return',
    '    if (.not.c_associated(ipglobal)) return')
global_check = global_check.replace('      if (c_associated(ipprojected,expected(i))) return\n', '')
global_check = global_check.replace('    if (c_associated(ipprojected,ipglobal)) return\n', '')
global_check += '    ok=.true.\n  end subroutine SPOR64_BOOT_CONTEXT64_GLOBAL_CHECK\n\n'
context_source = context_source.replace('  public :: SPOR64_BOOT_CONTEXT64_READ',
    '  public :: SPOR64_BOOT_CONTEXT64_READ,SPOR64_BOOT_CONTEXT64_GLOBAL_CHECK')
context_source = context_source.replace('contains\n', 'contains\n' + global_check, 1)
(OUT / 'SPOR64_BOOT_CONTEXT64.f90').write_text(context_source)

# Complete original B2N, locally transformed. The original source, transport
# policy, material formulas and numerical loop order are not replaced by a stub.
ORIGINAL = ROOT / 'src/SPOR64_B2N.f90'
t = Transform(ORIGINAL.read_text())
for old in ['SPOR64_B2N']:
    # Save a single explicit whole-text rename as a reversible local operation.
    t.replace(t.data, t.data.replace(old, 'SPOR64_BOOTQ64'), 'new independent module/routine names')
t.replace('  use SPOR64_RCONTRACT, only : SPOR64_ROUTE_CONTRACT',
          '  use SPOR64_RCONTRACT, only : SPOR64_ROUTE_CONTRACT\n'
          '  use SPOR64_BOOT_CONTEXT64, only : SPOR64_BOOT_CONTEXT64_READ, &\n'
          '      BOOT_ARCHIVE_NAMES, BOOT_PLANE_NAMES, BOOT_PLANE_AUTH_NAMES\n'
          '  use SPOR64_BOOT64, only : SPOR64_BOOT64_SAME_TREE', 'new ingress reader dependency')
t.replace('      EMPTY_MEMORY_ROOT, EXACT_INVENTORY, LIST_ITEM_IS_DIRECTORY, &',
          '      EMPTY_ROOT, EXACT_INVENTORY, LIST_ITEM_IS_DIRECTORY, &',
          'fresh roots may be complete disk-backed XSM trees')
t.replace(t.data,t.data.replace('EMPTY_MEMORY_ROOT(', 'EMPTY_ROOT('),
          'all caller output freshness uses the medium-neutral root primitive')
t.replace('  subroutine SPOR64_BOOTQ64_BUILD(ipprojected,plane_index,ipmacro_out, &\n'
          '      ipsource_out,contract,status)\n'
          '    type(c_ptr), intent(in) :: ipprojected, ipmacro_out, ipsource_out\n'
          '    type(SPOR64_ROUTE_CONTRACT), intent(in) :: contract',
          '  subroutine SPOR64_BOOTQ64_BUILD(ipprojected,ipglobal,ipax,ipaxtrack, &\n'
          '      ipaxsystem,ipaxmacro,iparchive,ipcontract,plane_index, &\n'
          '      ipmacro_out,ipsource_out,status)\n'
          '    type(c_ptr), intent(in) :: ipprojected, ipmacro_out, ipsource_out\n'
          '    type(c_ptr), intent(in) :: ipglobal,ipax,ipaxtrack,ipaxsystem\n'
          '    type(c_ptr), intent(in) :: ipaxmacro,iparchive,ipcontract\n'
          '    type(SPOR64_ROUTE_CONTRACT) :: contract\n'
          '    logical :: context_ok\n'
          '    type(c_ptr) :: input_roots(8), child\n'
          '    integer :: alias_index\n'
          '    real(real64) :: norm64\n'
          '    real(real64), allocatable :: volume64(:)', 'complete caller ABI with independent inputs')
t.replace('    status = SPOR64_BOOTQ64_PREFLIGHT_FAILED\n',
          '    status = SPOR64_BOOTQ64_PREFLIGHT_FAILED\n'
          '    input_roots=[ipprojected,ipglobal,ipax,ipaxtrack,ipaxsystem, &\n'
          '                 ipaxmacro,iparchive,ipcontract]\n'
          '    do alias_index=1,size(input_roots)\n'
          '      if (c_associated(ipmacro_out,input_roots(alias_index))) return\n'
          '      if (c_associated(ipsource_out,input_roots(alias_index))) return\n'
          '    enddo\n'
          '    call SPOR64_BOOT_CONTEXT64_READ(ipprojected,ipglobal,ipax, &\n'
          '        ipaxtrack,ipaxsystem,ipaxmacro,iparchive,ipcontract, &\n'
          '        contract,context_ok)\n'
          '    if (.not.context_ok) return\n'
          "    call LCMGET(ipglobal,'NORM64',norm64)\n", 'all input context preflight before mutation')
# The full e>0 guards remain in the old module; only this newly named bootstrap
# module consumes the independently verified epoch zero lifecycle.
t.replace("CHARACTER_RECORD_MATCHES(root_authority,'STATE',3,12, &\n        'PROJECTED')) return",
          "CHARACTER_RECORD_MATCHES(root_authority,'STATE',4,16, &\n        'PROJECTED-BOOT')) return",
          'root bootstrap 16-character state')
t.replace('    if (root_epoch <= 0) return', '    if (root_epoch /= 0) return', 'only bootstrap epoch zero')
t.replace("CHARACTER_RECORD_MATCHES(plane_authority,'STATE',3,12, &\n        'PROJECTED')) return",
          "CHARACTER_RECORD_MATCHES(plane_authority,'STATE',4,16, &\n        'PROJECTED-BOOT')) return",
          'plane bootstrap 16-character state')
t.replace("    call LCMGET(input_track,'VOLUME',volume32)\n", 
          "    call LCMGET(input_track,'VOLUME',volume32)\n"
          '    allocate(volume64(nreg),stat=allocation_status)\n'
          '    if (allocation_status /= 0) return\n'
          "    call LCMGET(input_flux,'VOLUME64',volume64)\n", 'actual verified type4 geometry authority')
t.replace('        product64 = real(volume32(ir),real64) * q64(keyflx(ir),g)',
          '        product64 = volume64(ir) * q64(keyflx(ir),g)', 'same exact volume integral via verified volume64')
t.replace('      product64 = real(volume32(ir),real64) * &\n',
          '      product64 = volume64(ir) * &\n', 'same exact mirror diagnostic volume')
t.replace("    call LCMPTC(source_authority,'STATE',12,lifecycle_state)\n", 
          "    call LCMPTC(source_authority,'STATE',12,lifecycle_state)\n"
          "    call LCMPUT(source_authority,'NORM',1,4,norm64)\n"
          "    child=LCMDID(source_authority,'GLOBAL64')\n"
          '    call LCMEQU(ipglobal,child)\n'
          "    child=LCMDID(source_authority,'SEED')\n"
          '    call LCMEQU(input_flux,child)\n', 'entire global and same-plane seed binding')
t.replace('    ! EPOCH is the source-wide commit and the final output mutation.\n',
          "    child=LCMLID(ipsource_out,'ROOT-QFISS64',NGRP)\n"
          '    do g=1,NGRP\n'
          '      call LCMPDL(child,g,nunkno,4,q64(:,g))\n'
          '    enddo\n\n'
          '    ! EPOCH is the source-wide commit and the final output mutation.\n',
          'new typed source root route; same q64 values, no REAL32 promotion')
t.replace('EXACT_INVENTORY(iplist,SCHEMA_PROJECTED_ARCHIVE_ROOT)',
          'EXACT_INVENTORY(iplist,BOOT_ARCHIVE_NAMES)', 'exact new archive inventory')
t.replace('EXACT_INVENTORY(iplist,SCHEMA_PROJECTED_PLANE_ROOT_L64) &\n'
          '        .or. EXACT_INVENTORY(iplist,SCHEMA_PROJECTED_PLANE_ROOT)',
          'EXACT_INVENTORY(iplist,BOOT_PLANE_NAMES)', 'exact new plane inventory')
t.replace('EXACT_INVENTORY(iplist,SCHEMA_PROJECTED_AUTHORITY)',
          'EXACT_INVENTORY(iplist,BOOT_PLANE_AUTH_NAMES)', 'exact new plane authority inventory')
t.replace('  public :: SPOR64_BOOTQ64_BUILD\n',
          '  public :: SPOR64_BOOTQ64_BUILD, SPOR64_BOOTQ64_READ\n'
          '  integer, parameter, public :: SPOR64_BOOTQ64_LOADED=3\n', 'actual read-back public boundary')
t.replace('end module SPOR64_BOOTQ64\n', '''
  ! Independent read-back recomputes the entire physical source from the supplied
  ! global/canonical/seed inputs. Internal copies alone cannot authorize inputs.
  subroutine SPOR64_BOOTQ64_READ(ipprojected,ipglobal,ipax,ipaxtrack, &
      ipaxsystem,ipaxmacro,iparchive,ipcontract,plane_index,ipmacro, &
      ipsource,q64,rho64,status)
    type(c_ptr), intent(in) :: ipprojected,ipglobal,ipax,ipaxtrack
    type(c_ptr), intent(in) :: ipaxsystem,ipaxmacro,iparchive,ipcontract
    type(c_ptr), intent(in) :: ipmacro,ipsource
    integer, intent(in) :: plane_index
    real(real64), allocatable, intent(out) :: q64(:,:)
    real(real64), intent(out) :: rho64
    integer, intent(out) :: status
    type(c_ptr) :: staged_macro,staged_source,source_auth,typed_source
    integer :: build_status,state(NSTATE),g,ilong,itylcm,istat
    logical :: same_macro,same_source,stage_exists
    status=SPOR64_BOOTQ64_PREFLIGHT_FAILED
    rho64=0.0_real64
    if (.not.c_associated(ipmacro).or..not.c_associated(ipsource)) return
    ! Private disk-backed full trees avoid duplicating the archive in memory.
    ! The host owns a fresh exclusive cwd; existing files are always refused.
    inquire(file='BQ64-MAC-ST',exist=stage_exists)
    if (stage_exists) return
    inquire(file='BQ64-SRC-ST',exist=stage_exists)
    if (stage_exists) return
    call LCMOP(staged_macro,'BQ64-MAC-ST',0,2,0)
    call LCMOP(staged_source,'BQ64-SRC-ST',0,2,0)
    call SPOR64_BOOTQ64_BUILD(ipprojected,ipglobal,ipax,ipaxtrack, &
        ipaxsystem,ipaxmacro,iparchive,ipcontract,plane_index, &
        staged_macro,staged_source,build_status)
    same_macro=.false.
    same_source=.false.
    if (build_status == SPOR64_BOOTQ64_COMMITTED) then
      same_macro=SPOR64_BOOT64_SAME_TREE(staged_macro,ipmacro)
      same_source=SPOR64_BOOT64_SAME_TREE(staged_source,ipsource)
    endif
    call LCMCL(staged_source,2)
    call LCMCL(staged_macro,2)
    if (.not.same_macro.or..not.same_source) return
    call LCMGET(ipsource,'STATE-VECTOR',state)
    allocate(q64(state(2),NGRP),stat=istat)
    if (istat /= 0) return
    typed_source=LCMGID(ipsource,'ROOT-QFISS64')
    do g=1,NGRP
      call LCMLEL(typed_source,g,ilong,itylcm)
      if (ilong /= state(2).or.itylcm /= 4) then
        deallocate(q64)
        return
      endif
      call LCMGDL(typed_source,g,q64(:,g))
    enddo
    source_auth=LCMGID(ipsource,'SPOT-R64')
    call LCMGET(source_auth,'RHO',rho64)
    status=SPOR64_BOOTQ64_LOADED
  end subroutine SPOR64_BOOTQ64_READ
end module SPOR64_BOOTQ64
''', 'complete exact physical/context readback')
t.finish('SPOR64_BOOTQ64.f90', ORIGINAL)

dependencies = [CAN, ORIGINAL, ROOT/'src/SPOR64_VERIFY.f90',
                ROOT/'src/SPOR64_RCONTRACT.f90', ROOT/'src/SPOR64_SCHEMA.f90',
                ROOT/'src/SPOR64_B2H.f90', ROOT/'src/SPOT_LEAKAGE.f90',
                REC/'new_source/SPOR64_BOOT64.f90',
                REC/'projection_chain_source/SPOPROJ64.f90',
                REC/'ROOT64_BOOTSTRAP_MINIMAL_REAL64_WIRING_ANALYSIS_20261011.txt',
                ROOT/'Ganlib/src/ganlib.f90', ROOT/'Ganlib/src/LCMAUX.f90',
                ROOT/'Ganlib/src/lcm_c.c',ROOT/'Ganlib/src/xsm_c.c',
                OUT/'SPOR64_BOOT_CONTEXT64.f90.template']
sources = [OUT/name for name in ['SPOR64_BOOT_CANONICAL64.f90',
                               'SPOR64_BOOT_CONTEXT64.f90', 'SPOR64_BOOTQ64.f90']]
manifest = {'status':'NEW_SOURCE_ONLY_NOT_COMPILED_NOT_RUN',
            'old_sources_modified':False, 'old_bytes_claimed':False,
            'source_pins':[pin(p) for p in sources],
            'actual_dependency_pins':[pin(p) for p in dependencies],
            'writer_pin':pin(Path(__file__)),
            'scientific_thresholds_changed':False,
            'global_publisher_actual_runtime_wired':False,
            'projected_publisher_actual_runtime_wired':False,
            'bootstrap_actual_runtime_wired':False,
            'original_17_controls_passed':False,
            'AAA_qualified':False, 'ABA_started':False,
            'independent_external_host_pins_required':True,
            'planned_compile_order':[str(p) for p in sources]}
(OUT/'SOURCE_PINS_DEPENDENCIES_AND_REMAINING_SCOPE.json').write_text(json.dumps(manifest,indent=2)+'\n')
long_lines=[]
for path in sources:
    for number,line in enumerate(path.read_text().splitlines(),1):
        if len(line)>132: long_lines.append([str(path),number,len(line)])
assert not long_lines, long_lines
print(json.dumps({'status':'SOURCE_WRITES_COMPLETE_ONLY', 'duration_seconds':time.monotonic()-started,
                  'sources':[pin(p) for p in sources], 'long_lines':long_lines},indent=2))
