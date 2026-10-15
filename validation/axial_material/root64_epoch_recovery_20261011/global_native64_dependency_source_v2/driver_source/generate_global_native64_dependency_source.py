#!/usr/bin/env python3
"""Derive complete new native SPOT Source; stdlib file operations only."""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import time

ROOT = Path('/Users/wen/spot')
REC = ROOT / 'validation/axial_material/root64_epoch_recovery_20261011'
V1 = REC / 'global_continuous_source_v1'
OUT = REC / 'global_native64_dependency_source_v2/driver_source'


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def read_pin(path):
    path = Path(path)
    a = identity(path.stat())
    with path.open('rb') as f:
        b = identity(os.fstat(f.fileno()))
        raw = f.read()
        c = identity(os.fstat(f.fileno()))
    d = identity(path.stat())
    if a != b or b != c or c != d:
        raise RuntimeError('complete EOF changed: ' + str(path))
    return raw, dict(path=str(path), size_bytes=len(raw), identity=a,
                    sha256=hashlib.sha256(raw).hexdigest(), read_scope='complete EOF',
                    before_open_EOF_after_identity_equal=True)


def fresh(path, raw):
    with path.open('xb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())


def fresh_json(path, value):
    fresh(path, (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode())


class Transform:
    def __init__(self, raw):
        self.original = raw
        self.raw = raw
        self.steps = []

    def splice(self, label, old, new, count=1):
        old = old.encode() if isinstance(old, str) else old
        new = new.encode() if isinstance(new, str) else new
        if self.raw.count(old) != count:
            raise RuntimeError('exact splice count: ' + label + ': ' + str(self.raw.count(old)))
        for i in range(count):
            # Distinct original occurrences are located against the current body.
            offset = self.raw.find(old, 0 if i == 0 else last_end)
            before = self.raw
            self.raw = before[:offset] + new + before[offset + len(old):]
            last_end = offset + len(new)
            self.steps.append(dict(label=label, mode='exact_local_byte_splice',
                                   byte_offset=offset, old=old.decode(), new=new.decode(),
                                   before_sha256=hashlib.sha256(before).hexdigest(),
                                   after_sha256=hashlib.sha256(self.raw).hexdigest(),
                                   outside_splice_exact_bytes_equal=True))

    def rename(self, old, new, count):
        pattern = rb'\b' + re.escape(old.encode()) + rb'\b'
        if len(re.findall(pattern, self.raw)) != count:
            raise RuntimeError('exact full token count: ' + old)
        before = self.raw
        self.raw = re.sub(pattern, new.encode(), before)
        self.steps.append(dict(label='independent symbol ' + old, mode='whole_identifier_rename',
                               old=old, new=new, count=count,
                               before_sha256=hashlib.sha256(before).hexdigest(),
                               after_sha256=hashlib.sha256(self.raw).hexdigest()))

    def append(self, label, raw):
        before = self.raw
        self.raw += raw
        self.steps.append(dict(label=label, mode='exact_local_byte_splice',
                               byte_offset=len(before), old='', new=raw.decode(),
                               before_sha256=hashlib.sha256(before).hexdigest(),
                               after_sha256=hashlib.sha256(self.raw).hexdigest(),
                               outside_splice_exact_bytes_equal=True))

    def verify(self):
        reverse = self.raw
        for s in reversed(self.steps):
            assert hashlib.sha256(reverse).hexdigest() == s['after_sha256']
            old = s['old'].encode(); new = s['new'].encode()
            if s['mode'] == 'whole_identifier_rename':
                pat = rb'\b' + re.escape(new) + rb'\b'
                assert len(re.findall(pat, reverse)) == s['count']
                reverse = re.sub(pat, old, reverse)
            else:
                n = s['byte_offset']; assert reverse[n:n + len(new)] == new
                reverse = reverse[:n] + old + reverse[n + len(new):]
            assert hashlib.sha256(reverse).hexdigest() == s['before_sha256']
        assert reverse == self.original
        assert max(map(len, self.raw.splitlines())) <= 132
        return dict(steps=self.steps, complete_inverse_equals_complete_basis_bytes=True,
                    basis_sha256=hashlib.sha256(self.original).hexdigest(),
                    candidate_sha256=hashlib.sha256(self.raw).hexdigest(),
                    actual_transform_steps=len(self.steps),
                    maximum_Source_line_bytes=max(map(len, self.raw.splitlines())))


LEAK_CARRIERS = '''
*     Independent native record carriers; never promote compatibility data.
      SUBROUTINE SPOT_STORE_LEAK_NATIVE64(IPFLUX,NMERG,NGRP,B2,
     1 DIFHET,GAMMA)
      USE GANLIB
      USE, INTRINSIC :: ISO_FORTRAN_ENV, ONLY: REAL32,REAL64
      USE, INTRINSIC :: IEEE_ARITHMETIC, ONLY: IEEE_IS_FINITE
      TYPE(C_PTR) IPFLUX
      INTEGER NMERG,NGRP
      REAL(REAL64) B2(4),DIFHET(NMERG,NGRP),GAMMA(NGRP)
      REAL(REAL32) B232(4),DIF32(NMERG,NGRP),GAM32(NGRP)
      IF(.NOT.ALL(IEEE_IS_FINITE(B2)).OR.
     1 .NOT.ALL(IEEE_IS_FINITE(DIFHET)).OR.
     2 .NOT.ALL(IEEE_IS_FINITE(GAMMA))) CALL XABORT(
     3 'SPOT NATIVE: NON-FINITE LEAKAGE FIELD.')
      B232=REAL(B2,REAL32)
      DIF32=REAL(DIFHET,REAL32)
      GAM32=REAL(GAMMA,REAL32)
      IF(.NOT.ALL(IEEE_IS_FINITE(B232)).OR.
     1 .NOT.ALL(IEEE_IS_FINITE(DIF32)).OR.
     2 .NOT.ALL(IEEE_IS_FINITE(GAM32))) CALL XABORT(
     3 'SPOT NATIVE: NON-FINITE LEAKAGE MIRROR.')
      CALL LCMPUT(IPFLUX,'SPOT-B2H64',4,4,B2)
      CALL LCMPUT(IPFLUX,'SPOT-DIF64',NMERG*NGRP,4,DIFHET)
      CALL LCMPUT(IPFLUX,'SPOT-GAM64',NGRP,4,GAMMA)
      CALL LCMPUT(IPFLUX,'B2  B1HOM',1,2,B232(4))
      CALL LCMPUT(IPFLUX,'DIFFHET',NMERG*NGRP,2,DIF32)
      CALL LCMPUT(IPFLUX,'GAMMA',NGRP,2,GAM32)
      RETURN
      END

      SUBROUTINE SPOT_LOAD_DIF_NATIVE64(IPFLUX,NMERG,NGRP,DIFHET)
      USE GANLIB
      USE, INTRINSIC :: ISO_FORTRAN_ENV, ONLY: REAL32,REAL64,INT32
      USE, INTRINSIC :: IEEE_ARITHMETIC, ONLY: IEEE_IS_FINITE
      TYPE(C_PTR) IPFLUX
      INTEGER NMERG,NGRP,ILONG,ITYLCM,INM,IG
      REAL(REAL64) DIFHET(NMERG,NGRP)
      REAL(REAL32) DIF32(NMERG,NGRP)
      CALL LCMLEN(IPFLUX,'SPOT-DIF64',ILONG,ITYLCM)
      IF(ILONG.NE.NMERG*NGRP.OR.ITYLCM.NE.4) CALL XABORT(
     1 'SPOT NATIVE: COMPLETE TYPE4 DIFFHET REQUIRED.')
      CALL LCMGET(IPFLUX,'SPOT-DIF64',DIFHET)
      CALL LCMLEN(IPFLUX,'DIFFHET',ILONG,ITYLCM)
      IF(ILONG.NE.NMERG*NGRP.OR.ITYLCM.NE.2) CALL XABORT(
     1 'SPOT NATIVE: COMPLETE DIFFHET MIRROR REQUIRED.')
      CALL LCMGET(IPFLUX,'DIFFHET',DIF32)
      IF(.NOT.ALL(IEEE_IS_FINITE(DIFHET)).OR.
     1 .NOT.ALL(IEEE_IS_FINITE(DIF32))) CALL XABORT(
     2 'SPOT NATIVE: NON-FINITE STORED DIFFHET.')
      DO IG=1,NGRP
        DO INM=1,NMERG
          IF(TRANSFER(REAL(DIFHET(INM,IG),REAL32),0_INT32).NE.
     1       TRANSFER(DIF32(INM,IG),0_INT32)) CALL XABORT(
     2       'SPOT NATIVE: DIFFHET MIRROR MISMATCH.')
        ENDDO
      ENDDO
      RETURN
      END

*     Terminal homogeneous coefficient output uses the original FLULPN
*     integrated-flux sums in their exact order.  It never feeds iteration.
      SUBROUTINE SPOT_CAPTURE_HOM_NATIVE64(NUNKNO,NGRP,NREG,NMAT,
     1 NMERG,VOL,MATCOD,IMERG,KEYFLX,FLUX,DIFHET,DHOM)
      USE, INTRINSIC :: ISO_FORTRAN_ENV, ONLY: REAL32,REAL64
      USE, INTRINSIC :: IEEE_ARITHMETIC, ONLY: IEEE_IS_FINITE
      INTEGER NUNKNO,NGRP,NREG,NMAT,NMERG,MATCOD(NREG),IMERG(NMAT),
     1 KEYFLX(NREG),IGR,IBM,I,IND,INM
      REAL(REAL32) VOL(NREG)
      REAL(REAL64) FLUX(NUNKNO,NGRP),DIFHET(NMERG,NGRP),DHOM(NGRP),
     1 FLXIN(NMAT,NGRP),FLTOT
      IF(NMERG.EQ.1) THEN
        DHOM(:)=DIFHET(1,:)
      ELSE
        FLXIN=0.0D0
        DO IGR=1,NGRP
          DO IBM=1,NMAT
            DO I=1,NREG
              IND=KEYFLX(I)
              IF(MATCOD(I).EQ.IBM.AND.IND.GT.0) THEN
                FLXIN(IBM,IGR)=FLXIN(IBM,IGR)+FLUX(IND,IGR)*VOL(I)
              ENDIF
            ENDDO
          ENDDO
        ENDDO
        DO IGR=1,NGRP
          DHOM(IGR)=0.0D0
          FLTOT=0.0D0
          DO IBM=1,NMAT
            INM=IMERG(IBM)
            IF(INM.LT.1.OR.INM.GT.NMERG) CALL XABORT(
     1       'SPOT NATIVE: INVALID HOMOGENEOUS LEAKAGE MAP.')
            DHOM(IGR)=DHOM(IGR)+FLXIN(IBM,IGR)*DIFHET(INM,IGR)
            FLTOT=FLTOT+FLXIN(IBM,IGR)
          ENDDO
          IF(.NOT.IEEE_IS_FINITE(FLTOT).OR.FLTOT.EQ.0.0D0)
     1      CALL XABORT('SPOT NATIVE: INVALID HOMOGENEOUS FLUX SUM.')
          DHOM(IGR)=DHOM(IGR)/FLTOT
        ENDDO
      ENDIF
      IF(.NOT.ALL(IEEE_IS_FINITE(DHOM))) CALL XABORT(
     1 'SPOT NATIVE: NON-FINITE HOMOGENEOUS COEFFICIENT OUTPUT.')
      RETURN
      END
'''.encode()


def main():
    started = time.monotonic()
    expected_names = [
        'SPOT_GLOBAL_NATIVE_DRIVER64.f', 'SPOT_GLOBAL_NATIVE_DRIVER_API.f90',
        'SPOT_FLUKEF_NATIVE64.f', 'SPOT_FLULPN_NATIVE64.f', 'SPOT_SPOF_NATIVE64.f',
        'ORIGINAL_COMPLETE_FROZEN_V1_DRIVER.f', 'ORIGINAL_COMPLETE_FROZEN_V1_API.f90',
        'ORIGINAL_COMPLETE_FROZEN_V1_KEFF.f', 'ORIGINAL_COMPLETE_FLULPN.f',
        'ORIGINAL_COMPLETE_SPOF64.f', 'COMPLETE_NATIVE64_LOCAL_TRANSFORM_PROOFS.json',
        'CURRENT_GLOBAL_NATIVE64_SOURCE_PINS_AND_BOUNDARIES.json']
    for name in expected_names:
        if (OUT / name).exists():
            raise RuntimeError('fresh Source namespace required: ' + name)
    protected = sorted(x for x in V1.rglob('*') if x.is_file()) + [
        ROOT / 'src/FLU2DR64.f', ROOT / 'src/FLUDRV.f', ROOT / 'src/FLU.f',
        ROOT / 'src/B1HOM64.f90', ROOT / 'src/B1HXS1.f', ROOT / 'src/B1DIF.f',
        ROOT / 'src/FLULPN.f', ROOT / 'src/SPOF64.f', ROOT / 'src/SPOT1P64.f90',
        ROOT / 'src/SPOR64_A9.f90']
    before = [read_pin(x)[1] for x in protected]
    freeze = json.loads(read_pin(V1 / 'COMPLETE_GLOBAL_TYPED_DRIVER_SOURCE_FREEZE.json')[0])
    for old in freeze['files']:
        if read_pin(Path(old['path']))[1] != old:
            raise RuntimeError('frozen v1 input changed')
    bases = {}
    for label, path in [
            ('driver', V1 / 'SPOT_GLOBAL_TYPED_DRIVER64.f'),
            ('API', V1 / 'SPOT_GLOBAL_TYPED_DRIVER_API.f90'),
            ('keff', V1 / 'callee_source/SPOT_FLUKEF_TYPED64.f'),
            ('FLULPN', ROOT / 'src/FLULPN.f'), ('SPOF', ROOT / 'src/SPOF64.f')]:
        bases[label] = read_pin(path)
    transforms = {}
    t = Transform(bases['driver'][0]); transforms['driver'] = t
    t.rename('SPOT_GLOBAL_TYPED_DRIVER64', 'SPOT_GLOBAL_NATIVE_DRIVER64', 2)
    t.rename('SPOT_GLOBAL_FLUSP_TYPED64', 'SPOT_GLOBAL_FLUSP_NATIVE64', 7)
    t.rename('SPOT_FLUKEF_TYPED64', 'SPOT_FLUKEF_NATIVE64', 2)
    t.splice('all three dynamic B1 homogenization calls use native ABI',
             'CALL B1HOM64(', 'CALL SPOT_B1HOM_NATIVE64(', 3)
    t.splice('full native dynamic dependency scope header',
             '*     This is a typed-driver candidate, not whole-chain qualification.\n'
             '*     Original B1HOM64 TYPE3 homogenization precision remains below.\n'
             '*     The separately recorded B1 dynamic-field gap must be repaired.\n',
             '*     New native dynamic B1/HXS2/DIF and Todorova dependency ABI.\n'
             '*     Original complete SPOT equations, epsilons and caps retained.\n'
             '*     New Source only: no compiled, online or physical qualification.\n'
             '*     Type4 leakage fields are authority; type2 is only a mirror.\n'
             '*     Native RADIAL-OP64 is mandatory at the retained POD door.\n')
    t.splice('explicit typed buckling ingress and full native leakage output ABI',
             '     7 TERMINAL_VALID)\n',
             '     7 TERMINAL_VALID,INITIAL_BUCKLING64,TERMINAL_BUCKLING64,\n'
             '     8 TERMINAL_DIFHET64,TERMINAL_DHOM64,TERMINAL_GAMMA64)\n')
    t.splice('full dynamic real64 parameter declarations',
             '      LOGICAL, INTENT(OUT) :: TERMINAL_VALID\n',
             '      LOGICAL, INTENT(OUT) :: TERMINAL_VALID\n'
             '      DOUBLE PRECISION, INTENT(IN) :: INITIAL_BUCKLING64(4)\n'
             '      DOUBLE PRECISION, INTENT(OUT) :: TERMINAL_BUCKLING64(4),\n'
             '     1 TERMINAL_DIFHET64(NMERG,NGRP),TERMINAL_DHOM64(NGRP),\n'
             '     2 TERMINAL_GAMMA64(NGRP)\n')
    t.splice('live buckling and original implicit old buckling use native real64',
             '      REAL ALBEDO(6),FLUXC(NREG),B2(4)\n',
             '      REAL ALBEDO(6),FLUXC(NREG)\n'
             '      DOUBLE PRECISION B2(4),B2VALO,CCLBD\n')
    t.splice('static materials separate from dynamic leakage carriers',
             '      REAL, ALLOCATABLE, DIMENSION(:) :: DHOM,FXSOR,XSCAT,GAMMA,V,FL,\n'
             '     1 DFL,LEAK1D\n'
             '      REAL, ALLOCATABLE, DIMENSION(:,:) :: DIFHET,SFNU\n',
             '      REAL, ALLOCATABLE, DIMENSION(:) :: FXSOR,XSCAT,V,FL,DFL\n'
             '      REAL, ALLOCATABLE, DIMENSION(:,:) :: SFNU\n'
             '      DOUBLE PRECISION, ALLOCATABLE, DIMENSION(:) ::\n'
             '     1 DHOM,GAMMA,LEAK1D\n'
             '      DOUBLE PRECISION, ALLOCATABLE, DIMENSION(:,:) :: DIFHET\n')
    t.splice('clear all added native outputs before any early rejection',
             '      TERMINAL_INNER_STATE=0\n',
             '      TERMINAL_INNER_STATE=0\n'
             '      TERMINAL_BUCKLING64=0.0D0\n'
             '      TERMINAL_DIFHET64=0.0D0\n'
             '      TERMINAL_DHOM64=0.0D0\n'
             '      TERMINAL_GAMMA64=0.0D0\n')
    t.splice('admitted typed buckling finite input guard',
             '*     General declared SPOT dimensions; no MCCG fixed shape.\n',
             '      IF(.NOT.ALL(IEEE_IS_FINITE(INITIAL_BUCKLING64)))\n'
             '     1 CALL XABORT("SPOT NATIVE: NON-FINITE INITIAL BUCKLING.")\n'
             '*     General declared SPOT dimensions; no MCCG fixed shape.\n')
    t.splice('initialize all original native leakage scratch before its use',
             '      DIFHET(:NMERG,:NGRP)=0.0\n      GAMMA(:NGRP)=1.0\n',
             '      DIFHET(:NMERG,:NGRP)=0.0D0\n'
             '      GAMMA(:NGRP)=1.0D0\n'
             '      DHOM(:NGRP)=0.0D0\n'
             '      LEAK1D(:NGRP)=0.0D0\n')
    t.splice('TYPE3 buckling seed only from typed caller, TYPE2 mathematical zero',
             "      IF(ITYPEC.GE.3) THEN\n"
             "         CALL LCMGET(IPFLUX,'B2  B1HOM',B2(4))\n"
             "         IF(ILEAK.GE.7) CALL LCMGET(IPFLUX,'B2  HETE',B2)\n"
             "      ELSE\n         B2(:4)=0.0\n      ENDIF\n",
             '      IF(ITYPEC.GE.3) THEN\n'
             '         B2(:4)=INITIAL_BUCKLING64(:4)\n'
             '      ELSE\n         B2(:4)=0.0D0\n      ENDIF\n')
    t.splice('static macrolib DIFF uses exact promotion without wrong memory type',
             "                 CALL LCMGET(KPMACR,'DIFF',DIFHET(1,IG))\n",
             "                 CALL LCMGET(KPMACR,'DIFF',DFL)\n"
             '                 DIFHET(:NMERG,IG)=DBLE(DFL(:NMERG))\n')
    t.splice('same leakage coefficient ratio retained directly in native real64',
             '                   DIFHET(INM,IG)=REAL(DDELD1/DDELN1)\n',
             '                   DIFHET(INM,IG)=DDELD1/DDELN1\n')
    t.splice('RHS and iterative leakage feedback use complete native type4',
             "CALL LCMGET(IPFLUX,'DIFFHET',DIFHET)",
             'CALL SPOT_LOAD_DIF_NATIVE64(IPFLUX,NMERG,NGRP,DIFHET)', 3)
    t.splice('Todorova initial full native flux and coefficient ABI',
             '            ALLOCATE(FLX32(NUNKNO,NGRP))\n'
             '            FLX32(:NUNKNO,:NGRP)=REAL(FLUX(:NUNKNO,:NGRP,2))\n'
             "            CALL FLULPN(IPMACR,NUNKNO,OPTION,'DIFF',NGRP,NREG,NMAT,\n"
             '     1      VOL,MATCOD,NMERG,IMERG,KEYFLX(1,1,1),FLX32,B2(4),\n'
             '     2      IPRT,DIFHET,DHOM)\n'
             '            DEALLOCATE(FLX32)\n',
             "            CALL SPOT_FLULPN_NATIVE64(IPMACR,NUNKNO,OPTION,'DIFF',\n"
             '     1      NGRP,NREG,NMAT,VOL,MATCOD,NMERG,IMERG,KEYFLX(1,1,1),\n'
             '     2      FLUX(1,1,2),B2(4),IPRT,DIFHET,DHOM)\n')
    t.splice('retained original unreachable ILEAK5 Todorova uses same typed ABI',
             '            ALLOCATE(FLX32(NUNKNO,NGRP))\n'
             '            FLX32(:NUNKNO,:NGRP)=REAL(FLUX(:NUNKNO,:NGRP,3))\n'
             '            CALL FLULPN(IPMACR,NUNKNO,OPTION,HTYPE(ITYPEC),NGRP,NREG,\n'
             '     1      NMAT,VOL,MATCOD,NMERG,IMERG,KEYFLX(1,1,1),FLX32,B2(4),\n'
             '     2      IPRT,DIFHET,DHOM)\n'
             '            DEALLOCATE(FLX32)\n',
             '            CALL SPOT_FLULPN_NATIVE64(IPMACR,NUNKNO,OPTION,\n'
             '     1      HTYPE(ITYPEC),NGRP,NREG,NMAT,VOL,MATCOD,NMERG,IMERG,\n'
             '     2      KEYFLX(1,1,1),FLUX(1,1,3),B2(4),IPRT,DIFHET,DHOM)\n')
    t.splice('initial dynamic type4 publication with separate type2 mirrors',
             "         CALL LCMPUT(IPFLUX,'B2  B1HOM',1,2,B2(4))\n"
             "         CALL LCMPUT(IPFLUX,'DIFFHET',NMERG*NGRP,2,DIFHET)\n",
             '         CALL SPOT_STORE_LEAK_NATIVE64(IPFLUX,NMERG,NGRP,B2,\n'
             '     1   DIFHET,GAMMA)\n')
    t.splice('iterative same leakage fields stored natively before feedback',
             "  350     CALL LCMPUT(IPFLUX,'B2  B1HOM',1,2,B2(4))\n"
             "          CALL LCMPUT(IPFLUX,'DIFFHET',NMERG*NGRP,2,DIFHET)\n",
             '  350     CALL SPOT_STORE_LEAK_NATIVE64(IPFLUX,NMERG,NGRP,B2,\n'
             '     1    DIFHET,GAMMA)\n')
    t.splice('original final legacy leakage record retains mirror-only meaning',
             "      IF(ITYPEC.GE.3) THEN\n"
             "         CALL LCMPUT(IPFLUX,'B2  B1HOM',1,2,B2(4))\n"
             "      ENDIF\n",
             '      IF(ITYPEC.GE.3) THEN\n'
             '         CALL SPOT_STORE_LEAK_NATIVE64(IPFLUX,NMERG,NGRP,B2,\n'
             '     1   DIFHET,GAMMA)\n'
             '      ENDIF\n')
    t.splice('legacy unreachable heterogeneous buckling serialization is mirror',
             "CALL LCMPUT(IPFLUX,'B2  HETE',3,2,B2)",
             "CALL LCMPUT(IPFLUX,'B2  HETE',3,2,REAL(B2,REAL32))")
    t.splice('legacy unreachable Gamma serialization is mirror',
             "CALL LCMPUT(IPFLUX,'GAMMA',NGRP,2,GAMMA)",
             "CALL LCMPUT(IPFLUX,'GAMMA',NGRP,2,REAL(GAMMA,REAL32))")
    t.splice('complete terminal leakage outputs from actual full native field',
             '      TERMINAL_FLUX64=FLUX(:,:,3)\n',
             '      CALL SPOT_CAPTURE_HOM_NATIVE64(NUNKNO,NGRP,NREG,NMAT,\n'
             '     1 NMERG,VOL,MATCOD,IMERG,KEYFLX(1,1,1),FLUX(1,1,3),\n'
             '     2 DIFHET,DHOM)\n'
             '      CALL SPOT_STORE_LEAK_NATIVE64(IPFLUX,NMERG,NGRP,B2,\n'
             '     1 DIFHET,GAMMA)\n'
             "      CALL LCMPUT(IPFLUX,'SPOT-DHM64',NGRP,4,DHOM)\n"
             '      TERMINAL_BUCKLING64=B2\n'
             '      TERMINAL_DIFHET64=DIFHET\n'
             '      TERMINAL_DHOM64=DHOM\n'
             '      TERMINAL_GAMMA64=GAMMA\n'
             '      TERMINAL_FLUX64=FLUX(:,:,3)\n')
    t.splice('private SPOT leakage correction ABI uses native dynamic fields',
             '      REAL VOL(NREG),B2(4),DIFHET(NMERG,NGRP)\n',
             '      REAL VOL(NREG)\n'
             '      DOUBLE PRECISION B2(4),DIFHET(NMERG,NGRP)\n')
    t.splice('private full POD door requires native radial operator authority',
             'CALL SPOF64(', 'CALL SPOT_SPOF_NATIVE64(')
    t.append('complete new native record carriers and terminal-only homogeneous output', LEAK_CARRIERS)
    assert t.raw.count(b'CALL SPOT_B1HOM_NATIVE64(') == 3
    assert t.raw.count(b'CALL SPOT_FLUKEF_NATIVE64(') == 2
    assert t.raw.count(b'CALL SPOT_FLULPN_NATIVE64(') == 2
    assert b'DBLE(GAR32' not in t.raw
    assert t.raw.count(b'      TERMINAL_VALID=.TRUE.') == 1

    k = Transform(bases['keff'][0]); transforms['keff'] = k
    k.rename('SPOT_FLUKEF_TYPED64', 'SPOT_FLUKEF_NATIVE64', 2)
    k.splice('honest full dynamic coefficient ABI header',
             '*     Complete AXMAT_FLUKEF64 numerical body retained byte-for-byte.\n'
             '*     FLUX(NUNKNO,NGRP) is DOUBLE PRECISION; coefficients remain REAL.\n',
             '*     Complete original keff formula and summation order retained.\n'
             '*     FLUX, dynamic B2 and DIFHET are DOUBLE PRECISION.\n'
             '*     Static type2 material coefficients retain exact promotions.\n')
    k.splice('native dynamic buckling and leakage coefficient ABI',
             '     1 XSNUF(0:NMAT,NIFIS,NGRP),XSCHI(0:NMAT,NIFIS,NGRP),\n'
             '     2 DIFHET(NMERG,NGRP),B2(4)\n'
             '      DOUBLE PRECISION FLUX(NUNKNO,NGRP)\n',
             '     1 XSNUF(0:NMAT,NIFIS,NGRP),XSCHI(0:NMAT,NIFIS,NGRP)\n'
             '      DOUBLE PRECISION FLUX(NUNKNO,NGRP),DIFHET(NMERG,NGRP),B2(4)\n')

    l = Transform(bases['FLULPN'][0]); transforms['FLULPN'] = l
    l.splice('independent FLULPN DECK without changing Hollerith diagnostic text',
             '*DECK FLULPN\n', '*DECK SPOT_FLULPN_NATIVE64\n')
    l.splice('independent true FLULPN procedure without changing diagnostics',
             '      SUBROUTINE FLULPN(', '      SUBROUTINE SPOT_FLULPN_NATIVE64(')
    l.splice('native Todorova flux and leakage dynamic parameters',
             '      REAL VOL(NREG),FLUX(NUNKNO,NGRP),B2,DIFHET(NMERG,NGRP),DHOM(NGRP)\n',
             '      REAL VOL(NREG)\n'
             '      DOUBLE PRECISION FLUX(NUNKNO,NGRP),B2,\n'
             '     1 DIFHET(NMERG,NGRP),DHOM(NGRP),FLTOT\n')
    l.splice('integrated iteration flux stays native, macrolib ST remains static32',
             '      REAL, ALLOCATABLE, DIMENSION(:,:) :: ST,FLXIN\n',
             '      REAL, ALLOCATABLE, DIMENSION(:,:) :: ST\n'
             '      DOUBLE PRECISION, ALLOCATABLE, DIMENSION(:,:) :: FLXIN\n')
    for old, new in [
            ('DIFHET(INM,IGR)=REAL(1.0D0/(3.0D0*GAMMA*ST2))', 'DIFHET(INM,IGR)=1.0D0/(3.0D0*GAMMA*ST2)'),
            ('DIFHET(INM,IGR)=REAL(1.0D0/(3.0D0*STR))', 'DIFHET(INM,IGR)=1.0D0/(3.0D0*STR)'),
            ('DIFHET(INM,IGR)=REAL(STOD(IGR,NGRP+1))', 'DIFHET(INM,IGR)=STOD(IGR,NGRP+1)')]:
        l.splice('same native coefficient expression without dynamic demote', old, new)
    l.splice('new honest independent complete Todorova Source header',
             '*DECK SPOT_FLULPN_NATIVE64\n',
             '*DECK SPOT_FLULPN_NATIVE64\n'
             '*     New full native dynamic API; original equations/order retained.\n'
             '*     Static macrolib records remain type2, never dynamic flux.\n'
             '*     No compiler, transport or physical qualification here.\n')

    s = Transform(bases['SPOF'][0]); transforms['SPOF'] = s
    s.rename('SPOF64', 'SPOT_SPOF_NATIVE64', 2)
    s.splice('new native POD door requires native operator lineage',
             '      IF(ILONG64.EQ.0) THEN\n'
             '        RADIAL2D64(:,:)=DBLE(RADIAL2D(:,:))\n'
             '      ELSE\n',
             '      IF(ILONG64.EQ.0) THEN\n'
             "        CALL XABORT('SPOT NATIVE: RADIAL-OP64 REQUIRED.')\n"
             '      ELSE\n')
    s.splice('honest native POD Source authority boundary header',
             '*DECK SPOT_SPOF_NATIVE64\n',
             '*DECK SPOT_SPOF_NATIVE64\n'
             '*     Complete original POD geometry/kernel and mirror check retained.\n'
             '*     Native RADIAL-OP64 is mandatory; no legacy operator promotion.\n'
             '*     Stored coherence is not external Source/input qualification.\n')

    a = Transform(bases['API'][0]); transforms['API'] = a
    a.rename('SPOT_GLOBAL_TYPED_DRIVER_API', 'SPOT_GLOBAL_NATIVE_DRIVER_API', 2)
    a.rename('SPOT_GLOBAL_TYPED_DRIVER64', 'SPOT_GLOBAL_NATIVE_DRIVER64', 3)
    a.splice('honest complete native Source-only interface boundary',
             '  ! Complete typed-driver ABI only; no caller, solve or seal is executed here.\n'
             '  ! Original TYPE3 B1HOM64 precision boundary remains explicit in the manifest.\n',
             '  ! Complete native dynamic Source-only API; no caller, solve or seal is run.\n'
             '  ! Owning host still needs full external input/Source/tool/current-state pins.\n')
    a.splice('complete sixty parameter ABI matches native fixed Source',
             '        terminal_resid64,terminal_counters,terminal_inner_state,terminal_valid)\n',
             '        terminal_resid64,terminal_counters,terminal_inner_state,terminal_valid, &\n'
             '        initial_buckling64,terminal_buckling64,terminal_difhet64, &\n'
             '        terminal_dhom64,terminal_gamma64)\n')
    a.splice('complete explicit typed buckling and leakage outputs',
             '      logical, intent(out) :: terminal_valid\n',
             '      logical, intent(out) :: terminal_valid\n'
             '      real(real64), intent(in) :: initial_buckling64(4)\n'
             '      real(real64), intent(out) :: terminal_buckling64(4)\n'
             '      real(real64), intent(out) :: terminal_difhet64(nmerg,ngrp)\n'
             '      real(real64), intent(out) :: terminal_dhom64(ngrp),terminal_gamma64(ngrp)\n')

    proof = {label: t.verify() for label, t in transforms.items()}
    output_map = {'driver': 'SPOT_GLOBAL_NATIVE_DRIVER64.f', 'API': 'SPOT_GLOBAL_NATIVE_DRIVER_API.f90',
                  'keff': 'SPOT_FLUKEF_NATIVE64.f', 'FLULPN': 'SPOT_FLULPN_NATIVE64.f',
                  'SPOF': 'SPOT_SPOF_NATIVE64.f'}
    copy_map = {'driver': 'ORIGINAL_COMPLETE_FROZEN_V1_DRIVER.f', 'API': 'ORIGINAL_COMPLETE_FROZEN_V1_API.f90',
                'keff': 'ORIGINAL_COMPLETE_FROZEN_V1_KEFF.f', 'FLULPN': 'ORIGINAL_COMPLETE_FLULPN.f',
                'SPOF': 'ORIGINAL_COMPLETE_SPOF64.f'}
    for label, name in output_map.items():
        fresh(OUT / name, transforms[label].raw)
        fresh(OUT / copy_map[label], bases[label][0])
    ast.parse(read_pin(Path(__file__).resolve())[0])
    fresh_json(OUT / 'COMPLETE_NATIVE64_LOCAL_TRANSFORM_PROOFS.json',
               dict(schema='COMPLETE_NATIVE64_SOURCE_LOCAL_TRANSFORM_PROOFS_V2',
                    proofs=proof, complete_bases={k: v[1] for k, v in bases.items()},
                    Fortran_parser_or_compiler_executed=False, transport_executed=False))
    after = [read_pin(x)[1] for x in protected]
    assert before == after
    # The real dependency namespace is independently prepared by another Source writer.
    dependency_paths = [ROOT / 'src/B1HXS1.f', ROOT / 'src/B1DIF.f', ROOT / 'src/B1SOL.f',
                        ROOT / 'src/B1BETA.f', ROOT / 'src/B1GAMA.f', ROOT / 'src/SPOT1P64.f90',
                        ROOT / 'src/SPOR64_A9.f90', ROOT / 'src/SPOMOC.f90',
                        ROOT / 'Utilib/src/ALSBD.f', ROOT / 'Utilib/src/ALEIGD.f', ROOT / 'Utilib/src/ALINVD.f',
                        ROOT / 'Ganlib/src/ganlib.f90', ROOT / 'Ganlib/src/lcmmod.f90',
                        REC / 'ROOT64_BOOTSTRAP_MINIMAL_REAL64_WIRING_ANALYSIS_20261011.txt']
    manifest = dict(schema='CURRENT_COMPLETE_NATIVE64_SPOT_SOURCE_BOUNDARIES_V2',
                    status='NEW_NATIVE_DYNAMIC_SOURCE_CANDIDATE_ONLY_REQUIRES_B1_DEPENDENCY_FREEZE_REVIEW',
                    source_pins={k: read_pin(OUT / v)[1] for k, v in output_map.items()},
                    source_writer_pin=read_pin(Path(__file__).resolve())[1],
                    proof_pin=read_pin(OUT / 'COMPLETE_NATIVE64_LOCAL_TRANSFORM_PROOFS.json')[1],
                    original_complete_basis_pins={k: v[1] for k, v in bases.items()},
                    original_and_v1_frozen_Source_before=before, original_and_v1_frozen_Source_after=after,
                    original_and_frozen_Source_unchanged=True,
                    static_original_complete_dependency_Source_pins=[read_pin(p)[1] for p in dependency_paths],
                    new_global_entry='SPOT_GLOBAL_NATIVE_DRIVER64',
                    new_private_dispatch='SPOT_GLOBAL_FLUSP_NATIVE64',
                    original_arguments=47, first_typed_arguments_retained=8, added_native_leakage_arguments=5,
                    total_explicit_ABI_arguments=60,
                    required_new_B1_dependencies=['SPOT_B1HOM_NATIVE64','SPOT_B1HXS2_NATIVE64','SPOT_B1DIF_NATIVE64'],
                    new_B1_dependency_directory=str(OUT.parent / 'b1_source'),
                    native_ingress='Complete INITIAL_FLUX64; TYPE3 INITIAL_BUCKLING64(4) supplied by real typed owning caller; TYPE2 mathematical B2=0.',
                    actual_formula_preservation=['Original complete SPOT TYPE2/3/forward/noREBA/ILEAK0or3 gates retained.',
                        'Every original eps argument, iteration cap, acceleration cycle, raw strict predicate, full normalization and SPOT/POD geometry kernel retained.',
                        'Full first/update keff expression and summation order; dynamic B2/DIFHET only ABI promoted.',
                        'Complete Todorova FLULPN formula/order, integrated FLXIN/FLTOT and outputs native, static ST/SCAT1 unchanged.',
                        'Full native flux/source/keff/strict residuals/counters and added complete leakage outputs; valid only last.',
                        'Terminal DHOM output is DIFHET zone1 for one zone, otherwise original FLULPN integrated-flux sums/order computed after final original normalization; it never feeds iteration.'],
                    native_field_records={'SPOT-B2H64': {'count':4,'type':4},
                                          'SPOT-DIF64': {'count':'NMERG*NGRP','type':4},
                                          'SPOT-GAM64': {'count':'NGRP','type':4},
                                          'SPOT-DHM64': {'count':'NGRP','type':4}},
                    dynamic_feedback='Original per-iteration DIFFHET save/reload is TYPE4 authority with full real32 bitwise demote mirrors; no legacy-only fallback. Native POD door requires actual RADIAL-OP64 with original exact type2 mirror check.',
                    static_type2_exact_promotion_permitted=['material macrolib XS/SCAT/ST/DIFF/FLUX-INTG declared static for supplied solve','VOL and SPOT geometry/quadrature/POD-BASIS'],
                    retained_unreachable_legacy_paths=['ITYPEC1 GPT Hotelling REAL demote/dead IPFLUP B2/GAMMA reads','non-SPOT doors','ILEAK>=7 FLUBLN legacy ABI; prevented by original ILEAK0or3 guard'],
                    remaining_required_real_work=['Review/freeze all three actual new B1 full bodies and bind their full EOF identities.',
                        'Independent full Source and 60-argument API review; current compiler/module/tool/lib bindings and guarded actual build.',
                        'New owning global caller cold/warm typed arrays and explicit native initial B2, fresh Source/context/geometry/material/route pins.',
                        'Actual strict SPOT global solve and actual archive/header/publication; independent current output full EOF pins.',
                        'Current global state/source producer and complete seventeen control cases, online three-plane BOOT then actual downstream next epoch.'],
                    stored_coherence_does_not_replace_external_pins=True,
                    no_old_qualification_inherited=True,
                    Fortran_parser_or_compiler_executed=False, transport_executed=False,
                    whole_continuous64_qualified=False, native_global_producer_qualified=False,
                    online_BOOT_qualified=False, seventeen_controls_qualified=False,
                    whole_INPUT_admitted=False, AAA_qualified=False, ABA_admitted=False, goal_complete=False,
                    actual_Source_writer_wall_seconds=time.monotonic()-started)
    fresh_json(OUT / 'CURRENT_GLOBAL_NATIVE64_SOURCE_PINS_AND_BOUNDARIES.json', manifest)
    print(json.dumps(dict(status=manifest['status'], source_pins=manifest['source_pins'],
                          manifest_pin=read_pin(OUT / 'CURRENT_GLOBAL_NATIVE64_SOURCE_PINS_AND_BOUNDARIES.json')[1],
                          complete_inverse_by_source={k: v['actual_transform_steps'] for k,v in proof.items()},
                          actual_protected_inputs_unchanged=True,
                          Fortran_compiler_or_transport_executed=False)))


if __name__ == '__main__':
    main()
