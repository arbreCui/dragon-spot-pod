"""Finite Fortran Source only; no compiler, candidate, Ganlib or material read."""
import difflib
import hashlib
import json
from pathlib import Path
import shutil

P=Path(__file__).resolve().parent
root=Path('/Users/wen/spot')
copies=P/'DIRECT_OBSERVATION_API_SOURCE';copies.mkdir(exist_ok=True)
paths=[root/'src'/name for name in('LIBMIX.f','LIBDEN.f','TONDRV.f','TONSPH.f')]
paths += [root/'Ganlib/src'/name for name in('LCMAUX.f90','ganlib.f90','lcm_c.c','lcm.h','ganlib.h','xsm_c.c','kdi_c.c','LCMTLC.f90')]
original=[]
for path in paths:
    s=path.lstat();identity=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    raw=path.read_bytes();assert path.lstat().st_mtime_ns==s.st_mtime_ns
    shutil.copy2(path,copies/path.name)
    original.append(dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity))

def insert(source,anchor,new):
    assert source.count(anchor)==1,anchor
    return source.replace(anchor,new+anchor)

derivatives=[]
for filename in('LIBMIX.f','LIBDEN.f','TONDRV.f','TONSPH.f'):
    old=(copies/filename).read_text();new=old
    new=insert(new,'      USE GANLIB\n','      USE AXMAT_OBSERVATION_MOD_UNREADY\n')
    if filename=='LIBMIX.f':
        new=insert(new,"      CALL LCMGET(IPLIB,'STATE-VECTOR',ISTATE)\n",
            "      CALL AXOBS_LIBMIX_BEGIN(IPLIB,NBMIX,NGROUP,NBISO,MIX,\n     1 DEN,MASK,MASKL,ITSTMP,TMPDAY)\n")
        new=insert(new,'      DEALLOCATE(IPISO,JNED)\n',
            '      CALL AXOBS_LIBMIX_END(IPLIB)\n')
    elif filename=='LIBDEN.f':
        anchor='*  RECOVER PARTICLE DATA\n'
        # Insert after old-state/MASKK/LALL/LDIFF are fully read, without
        # treating final STATE9 as the old flag or evaluating undefined arrays.
        before='      CALL AXOBS_LIBDEN_OLD(IPLIB,NBMIX,NGROUP,NBISO,NL,\n     1 NDEL,NESP,NED,ITRANC,MAXNFI,NPART,LSAME,ITSTMP,TMPDAY,\n     2 STERN,MASK,MASKL,MASKK,LALL,LDIFF,NFISSI)\n'
        block='*----\n'+anchor
        assert new.count(block)==1
        new=new.replace(block,before+block)
        new=insert(new,'      DO 460 ISOT=1,NBISO\n',
            '      CALL AXOBS_LIBDEN_FISSION(NBMIX,MAXNFI,NFISS0,\n     1 NFISSI,INDFIS)\n')
    elif filename=='TONDRV.f':
        block='*----\n*  RECOMPUTE THE VECTOR LSHI\n'
        assert new.count(block)==1
        new=new.replace(block,
            '      CALL AXOBS_TRACK(NREG,NBISO,NBMIX,NGRO,MAT,MIX,DEN,\n     1 LSHI,KSPH,ITRANZ,IPROB,IGRMIN,IGRMAX)\n'+block)
        anchor='      CALL LIBMIX(IPLIB,NBMIX,NGRO,NBISO,ISONAM,MIX,DEN,MASK,MASKL,\n     > ITSTMP,TMPDAY)\n'
        assert new.count(anchor)==1
        new=new.replace(anchor,
            '      CALL AXOBS_MASK(NBISO,NBMIX,NGRO,MASK,MASKL,LSHI,\n     1 LSHI2,KSPH,ITRANZ,IPHASE,NRES2,ITSTMP,TMPDAY)\n'+anchor)
        anchor2='         CALL LIBMIX(IPLIB,NBMIX,NGRO,NBISO,ISONAM,MIX,DEN,MASK,MASKL,\n     >   ITSTMP,TMPDAY)\n'
        assert new.count(anchor2)==1
        new=new.replace(anchor2,
            '         CALL AXOBS_MASK(NBISO,NBMIX,NGRO,MASK,MASKL,LSHI,\n     1    LSHI2,KSPH,ITRANZ,IPHASE,NRES2,ITSTMP,TMPDAY)\n'+anchor2)
        anchor='      DEALLOCATE(NOCONV,MASKL,MASK)\n'
        new=insert(new,anchor,'      CALL AXOBS_FINAL(IPLIB)\n')
    else:
        anchor='      CALL TONCMI(IPLIB,IMPX,NBM,NBISO,NGRO,NL,NED,NDEL,MASKI,SPH)\n'
        new=insert(new,anchor,
            '      CALL AXOBS_SPH(NBM,NBISO,NGRO,INRS,ITRANC,IGRMIN,\n     1 IGRMAX,MASKI,SPH)\n')
    path=P/(filename[:-2]+'.observe.UNREADY.f');path.write_text(new)
    a=old.splitlines(keepends=True);b=new.splitlines(keepends=True)
    hunks=[dict(tag=t,old_start0=i,old_end0=j,new_start0=k,new_end0=l,old_full_lines=a[i:j],new_full_lines=b[k:l])for t,i,j,k,l in difflib.SequenceMatcher(a=a,b=b,autojunk=False).get_opcodes()if t!='equal']
    restored=b[:]
    for h in reversed(hunks):restored[h['new_start0']:h['new_end0']]=h['old_full_lines']
    assert ''.join(restored)==old
    assert all(h['tag']=='insert'for h in hunks)
    derivatives.append(dict(original=next(p for p in original if p['path'].endswith('/'+filename)),candidate=str(path),candidate_sha256=hashlib.sha256(new.encode()).hexdigest(),all_original_statements_bytes_unchanged=True,complete_zero_based_hunks=hunks))

(P/'COMPLETE_OBSERVATION_FORTRAN_SOURCE_INVERSE.json').write_text(json.dumps(dict(schema='READONLY_OBSERVATION_INSERT_ONLY_COMPLETE_FORTRAN_SOURCE_INVERSE_V1',source_only=True,original_Source_pins=original,complete_derivatives=derivatives,original_physical_deck_and_numeric_statements_unchanged=True,compiled_binary_linkage_or_actual_runtime_qualified=False),indent=2)+'\n')
print(json.dumps(dict(source_only=True,complete_observation_Source_files=len(original),full_insert_only_hunk_counts=[len(p['complete_zero_based_hunks'])for p in derivatives],compiled=False,material_or_API_executed=False)))
