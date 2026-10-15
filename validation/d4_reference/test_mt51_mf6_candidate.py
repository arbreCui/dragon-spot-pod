"""Short source-selection tests. Never execute NJOY, Dragon or transport.

Compile the exact parameter-selection block extracted from the frozen source,
not a Python approximation. This does not validate new nuclear-data integrals.
The frozen failed batch and its checker are kept unchanged.
"""
import difflib
import hashlib
from pathlib import Path
import subprocess
import tempfile
import unittest

import remaining_temperature_batch as batch


SOURCE = batch.PAIR / 'candidate/source/src/groupr.f90'
PATCH = Path(__file__).with_name('mt51_mf6_candidate.patch')
WORK = batch.ART / 'd4a-remaining-temperature-run-20261001'
ANCHOR = '   if (mfd.eq.6.and.mtd.eq.51) nz=nsigz\n'
ADDITION = '   if (mfd.eq.8.and.mtd.eq.51) nz=nsigz\n'


def sources():
    relative = str(SOURCE.relative_to(batch.PAIR))
    sealed = dict(line.split(maxsplit=1)[::-1]
                  for line in (batch.PAIR/'result.sha256').read_text().splitlines())
    original = SOURCE.read_bytes()
    assert hashlib.sha256(original).hexdigest() == sealed[relative]
    original = original.decode()
    assert original.count(ANCHOR) == 1 and ADDITION not in original
    return original, original.replace(ANCHOR, ANCHOR+ADDITION)


def selection(source, name):
    init = source.split('   subroutine init(ng,nl,nz)\n', 1)[1]
    body = init.split('   !--select control parameters\n', 1)[1].split('   econst=0\n', 1)[0]
    return f'''subroutine {name}(mfd,mtd,nsigz,lord,ng,nl,nz)
implicit none
integer,intent(in)::mfd,mtd,nsigz,lord
integer,intent(out)::ng,nl,nz
integer,parameter::ngn=370,ngg=0,ndelg=6
{body}end subroutine {name}
'''


class MF6CandidateTests(unittest.TestCase):
    def test_patch_is_one_branch_only(self):
        old, new = sources()
        diff = ''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),
                    fromfile='a/src/groupr.f90',tofile='b/src/groupr.f90'))
        self.assertEqual(PATCH.read_text(), diff)
        self.assertEqual(new.replace(ADDITION,''),old)

    def test_compiled_selection_exhaustive_reaction_grid(self):
        old, new = sources()
        program = '''program check_selection
implicit none
integer::mf,mt,ns,lord,ng0,nl0,nz0,ng1,nl1,nz1,count
count=0
do ns=1,10,9
do lord=0,1
do mf=1,36
do mt=1,900
call old_selection(mf,mt,ns,lord,ng0,nl0,nz0)
call new_selection(mf,mt,ns,lord,ng1,nl1,nz1)
if (ng1/=ng0.or.nl1/=nl0) error stop 'group/moment drift'
if (mf==8.and.mt==51) then
  if (nz0/=1.or.nz1/=ns) error stop 'missing native MF6 MT51 branch'
else
  if (nz1/=nz0) error stop 'unrelated reaction changed'
endif
count=count+1
enddo
enddo
enddo
enddo
if (count/=129600) error stop 'coverage'
print *, 'SELECTION_PASS',count
contains
'''+selection(old,'old_selection')+selection(new,'new_selection')+'end program\n'
        with tempfile.TemporaryDirectory(prefix='spot-mt51-selection-') as tmp:
            root=Path(tmp)
            (root/'selection.f90').write_text(program)
            subprocess.run(['/opt/homebrew/bin/gfortran','-Wall','-Wextra','-fcheck=all',
                            str(root/'selection.f90'),'-o',str(root/'selection')],
                           check=True,capture_output=True,timeout=30)
            result=subprocess.run([str(root/'selection')],check=True,capture_output=True,
                                  text=True,timeout=10)
            self.assertIn('SELECTION_PASS',result.stdout)
            self.assertIn('129600',result.stdout)

    def test_actual_fuel_endf_routes(self):
        expected = {'Am241':6,'Pu238':4,'Pu239':6,'Pu240':4,
                    'Pu241':4,'Pu242':6,'U235':6,'U238':4,'Cr52':4}
        for row in batch.cases():
            name=row['nuclide']
            if name not in expected:
                continue
            sections=set()
            with Path(row['endf']).open() as stream:
                for line in stream:
                    if len(line)<75:
                        continue
                    mf=int(line[70:72].strip() or '0')
                    mt=int(line[72:75].strip() or '0')
                    if mt==51 and mf in (4,6):
                        sections.add(mf)
            self.assertEqual(sections,{expected[name]},name)

    def test_unrepaired_am241_remains_refused(self):
        row=next(r for r in batch.cases() if r['nuclide']=='Am241')
        original=(Path(row['original_library']).parent/'gendf_neutron_Am241').read_bytes()
        actual=(WORK/'Am241/control/high/groupr/tape30').read_bytes()
        self.assertEqual(original,actual)
        with self.assertRaisesRegex(ValueError,'MT51 width not repaired'):
            batch.mt51.gendf_scope(original,actual,row['mat'])

    def test_existing_mfd6_cr52_repair_remains_valid(self):
        row=next(r for r in batch.cases() if r['nuclide']=='Cr52')
        original=(Path(row['original_library']).parent/'gendf_neutron_Cr52').read_bytes()
        actual=(WORK/'Cr52/control/groupr/tape30').read_bytes()
        report=batch.mt51.gendf_scope(original,actual,row['mat'])
        self.assertTrue(report['non_MT51_content_exact'])
        self.assertEqual(len(report['rows']),5)
        self.assertTrue(all(r['new_nz']==row['nsigz'] for r in report['rows']))


if __name__=='__main__':
    unittest.main()
