"""Create a complete REAL64 projection entry; no transport or qualification."""
import hashlib
import json
import os
from pathlib import Path

ROOT=Path('/Users/wen/spot')
SOURCE=ROOT/'src/SPOPROJ.f90'
OUT=ROOT/'validation/axial_material/root64_epoch_recovery_20261011/projection_chain_source'

def identity(p):
    s=p.lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

before=identity(SOURCE)
with SOURCE.open('rb') as f:
    s=os.fstat(f.fileno())
    opened=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    raw=f.read()
    s=os.fstat(f.fileno())
    eof=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
if before!=opened or before!=eof or before!=identity(SOURCE):
    raise RuntimeError('original full Source changed')
text=raw.decode()
changes=[]
def replace(old,new,count=1):
    global text
    if text.count(old)!=count:raise RuntimeError('literal complete Source transform count: '+old[:70])
    text=text.replace(old,new)
    changes.append(dict(old=old,new=new,count=count))

# The new entry is deliberately separate from the existing production entry.
count=text.count('SPOPROJ')
replace('SPOPROJ','SPOPROJ64',count)
replace('  real, allocatable :: volume3d(:),area(:),u3d(:),u2d(:),basis_state(:)',
        '  real, allocatable :: volume3d(:),area(:),basis_state(:),mirror3d(:),mirror2d(:)\n'
        '  real(kind=dp), allocatable :: u3d(:),u2d(:)')
replace('  real :: flott,weight,projected,floor_min,floor_max,group_max,relative',
        '  real :: flott\n'
        '  real(kind=dp) :: weight,projected,floor_min,floor_max,group_max,relative')
replace('  type(c_ptr) :: jpax,jptracks,jpfluxes,kptrack,kpflux,jpplane',
        '  type(c_ptr) :: jpax,jptracks,jpfluxes,kptrack,kpflux,jpplane,jpax32,jpplane32')
replace('  allocate(key3d(nreg),mat1d(nfloor),volume3d(nreg),area(nreg2d),u3d(nunk))',
        '  allocate(key3d(nreg),mat1d(nfloor),volume3d(nreg),area(nreg2d), &\n'
        '      u3d(nunk),mirror3d(nunk))')
replace("  jpax=LCMGID(kentry(2),'FLUX')",
        "  call require_record(kentry(2),'FLUX64',ngrp,10)\n"
        "  call require_record(kentry(2),'FLUX',ngrp,10)\n"
        "  jpax=LCMGID(kentry(2),'FLUX64')\n"
        "  jpax32=LCMGID(kentry(2),'FLUX')\n"
        '  ! Validate the complete global numerical authority before any write.\n'
        '  do igr=1,ngrp\n'
        '    call read_native_pair(jpax,jpax32,igr,nunk,u3d,mirror3d)\n'
        '  enddo')
replace('    allocate(key2d(nreg2d),u2d(nunk2d))',
        '    allocate(key2d(nreg2d),u2d(nunk2d),mirror2d(nunk2d))')
replace("    jpplane=LCMGID(kpflux,'FLUX')",
        "    call require_record(kpflux,'FLUX64',ngrp,10)\n"
        "    call require_record(kpflux,'FLUX',ngrp,10)\n"
        "    jpplane=LCMGID(kpflux,'FLUX64')\n"
        "    jpplane32=LCMGID(kpflux,'FLUX')\n"
        '    ! Non-scalar native unknowns are preserved from the admitted plane.\n'
        '    do igr=1,ngrp\n'
        '      call read_native_pair(jpplane,jpplane32,igr,nunk2d,u2d,mirror2d)\n'
        '    enddo')
replace('      call LCMGDL(jpax,igr,u3d)\n      call LCMGDL(jpplane,igr,u2d)',
        '      call read_native_pair(jpax,jpax32,igr,nunk,u3d,mirror3d)\n'
        '      call read_native_pair(jpplane,jpplane32,igr,nunk2d,u2d,mirror2d)')
replace('          projected=real(canonical_value)',
        '          projected=canonical_value')
replace('      call LCMPDL(jpplane,igr,nunk2d,2,u2d)',
        '      ! FLUX64 is the numerical output; FLUX is only its legacy mirror.\n'
        '      mirror2d=real(u2d)\n'
        '      if (any(.not.ieee_is_finite(mirror2d))) &\n'
        "        call XABORT('SPOPROJ64: NON-FINITE LEGACY OUTPUT MIRROR.')\n"
        '      call LCMPDL(jpplane,igr,nunk2d,4,u2d)\n'
        '      call LCMPDL(jpplane32,igr,nunk2d,2,mirror2d)')
replace('    deallocate(u2d,key2d)',
        '    deallocate(mirror2d,u2d,key2d)')
replace('  deallocate(u3d,area,volume3d,mat1d,key3d)',
        '  deallocate(mirror3d,u3d,area,volume3d,mat1d,key3d)')
replace('contains\n',
        'contains\n\n'
        '  subroutine read_native_pair(native,mirror,group,nunknown,values,mirror_values)\n'
        '    type(c_ptr), intent(in) :: native,mirror\n'
        '    integer, intent(in) :: group,nunknown\n'
        '    real(kind=dp), intent(out) :: values(nunknown)\n'
        '    real, intent(out) :: mirror_values(nunknown)\n'
        '    integer :: length,type_code,index\n'
        '    call LCMLEL(native,group,length,type_code)\n'
        '    if (length /= nunknown .or. type_code /= 4) &\n'
        "      call XABORT('SPOPROJ64: EXACT TYPE4 NATIVE ITEM REQUIRED.')\n"
        '    call LCMLEL(mirror,group,length,type_code)\n'
        '    if (length /= nunknown .or. type_code /= 2) &\n'
        "      call XABORT('SPOPROJ64: EXACT TYPE2 MIRROR ITEM REQUIRED.')\n"
        '    call LCMGDL(native,group,values)\n'
        '    call LCMGDL(mirror,group,mirror_values)\n'
        '    if (any(.not.ieee_is_finite(values)) .or. &\n'
        '        any(.not.ieee_is_finite(mirror_values))) &\n'
        "      call XABORT('SPOPROJ64: NON-FINITE NATIVE/MIRROR ITEM.')\n"
        '    do index=1,nunknown\n'
        '      if (transfer(real(values(index)),0) /= transfer(mirror_values(index),0)) &\n'
        "        call XABORT('SPOPROJ64: LEGACY MIRROR MISMATCH.')\n"
        '    enddo\n'
        '  end subroutine read_native_pair\n')

restored=text
for c in reversed(changes):
    if restored.count(c['new'])!=c['count']:
        raise RuntimeError('inverse transform count differs')
    restored=restored.replace(c['new'],c['old'])
if restored.encode()!=raw:raise RuntimeError('full Source byte inverse differs')
if any(len(line)>132 for line in text.splitlines()):raise RuntimeError('new free-form line length')
OUT.mkdir()
original=OUT/'SPOPROJ.original_exact.f90'
candidate=OUT/'SPOPROJ64.f90'
original.write_bytes(raw);candidate.write_text(text)
pins=[]
for p in (SOURCE,original,candidate,Path(__file__).resolve()):
    first=identity(p);data=p.read_bytes()
    if identity(p)!=first:raise RuntimeError('output pin changed')
    pins.append(dict(path=str(p),identity=first,sha256=hashlib.sha256(data).hexdigest(),size_bytes=len(data)))
report=dict(schema='NEW_COMPLETE_SPOPROJ64_SOURCE_TRANSFORM_V1',status='SOURCE_ONLY_NOT_COMPILED_OR_WIRED',
    input_output_pins=pins,changes=changes,full_byte_inverse_equal=True,
    all_original_Geometry_FIXB_Gram_layout_logic_preserved=True,
    no_FLUX32_numeric_fallback=True,native_global_and_plane_FLUX64_full_group_reads=True,
    legacy_FLUX32_is_checked_output_mirror_only=True,
    mathematical_restriction_and_FIXED_basis_reconstruction_preserved=True,
    publisher_global_seal_source_epoch_connection_pending=True,
    original_seventeen_controls_executed=False,continuous_REAL64_qualified=False,
    online_BOOT_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
(OUT/'COMPLETE_SOURCE_TRANSFORM_AND_CURRENT_PINS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(status=report['status'],Source_sha256=pins[2]['sha256'],Source_bytes=pins[2]['size_bytes'],changes=len(changes))))
