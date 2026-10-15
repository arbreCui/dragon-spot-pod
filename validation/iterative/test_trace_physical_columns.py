"""Analytic checks for passive column diagnostics; no transport solve."""
from pathlib import Path
import math
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = r'''
program fixture
use GANLIB
implicit none
type(c_ptr) :: track
integer :: st(40),mat(2),key(2),i
real :: vol(2),nuf(0:1,1,2)
real(dp) :: flux(2,2,3),before(2,2,3),ak(3),ak_before(3)
call LCMOP(track,'track.xsm',0,2,0)
st=0;st(2)=2;st(6)=2;st(7)=1;call LCMPUT(track,'STATE-VECTOR',40,1,st)
mat=1;key=[1,2];vol=1;nuf=1;ak=[1._dp,1.2_dp,1.3_dp];ak_before=ak
flux(:,:,1)=1;flux(1,:,2)=1;flux(2,:,2)=2;flux(:,:,3)=2;before=flux
call SPOTCOLTRACE(track,1,2,2,2,1,1,mat,key,vol,nuf,flux,ak,0.1_dp,0.01_dp)
if(any(flux/=before).or.any(ak/=ak_before)) error stop 'trace changed solver state'
call SPOTCOLTRACE(track,10,2,2,2,1,1,mat,key,vol,nuf,flux,ak,0.1_dp,0.01_dp)
if(any(flux/=before).or.any(ak/=ak_before)) error stop 'checkpoint changed solver state'
call LCMGET(track,'STATE-VECTOR',st)
if(st(2)/=2.or.st(6)/=2.or.st(7)/=1) error stop 'trace changed tracking'
call LCMCL(track,1)
print *, 'PASSIVE-TRACE-IMMUTABILITY PASS'
end program
'''


class ColumnTrace(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="spot-column-trace-")
        cls.work = Path(cls.tmp.name)
        (cls.work / "fixture.f90").write_text(FIXTURE)
        gan = ROOT / "Ganlib/lib/Darwin_arm64"
        subprocess.run(["gfortran", "-O0", "-fcheck=all", "-ffp-contract=off",
                        "-I" + str(gan / "modules"), str(cls.work / "fixture.f90"),
                        str(Path(__file__).with_name("trace_physical_columns.f90")),
                        str(gan / "libGanlib.a"), "-lstdc++", "-o", str(cls.work / "test")],
                       check=True, capture_output=True, timeout=30)
        cls.output = subprocess.run([str(cls.work / "test")], cwd=cls.work,
                                    check=True, capture_output=True, text=True, timeout=10).stdout
        cls.summary = list(map(float, next(line for line in cls.output.splitlines()
                                          if line.startswith("COLUMN-ITER 1 ")).split()[2:]))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_known_fission_reweighting_and_unchanged_column_shape(self):
        self.assertAlmostEqual(self.summary[5], 1/3, places=14)
        self.assertAlmostEqual(self.summary[6], 1/3, places=14)
        self.assertEqual(self.summary[10], 0)
        rows = [line.split() for line in self.output.splitlines() if line.startswith("COLUMN-FISSION 1 ")]
        self.assertEqual(len(rows), 2)
        self.assertAlmostEqual(float(rows[0][-2]), 1.5)
        self.assertAlmostEqual(float(rows[1][-2]), 0.75)

    def test_raw_flux_defect_and_acceleration_candidate(self):
        self.assertEqual(self.summary[4], 0.5)
        self.assertEqual(self.summary[7], 0.5)
        self.assertEqual(self.summary[8:10], [-2, 4])

    def test_diagnostic_checkpoint_is_explicitly_unaccepted_and_passive(self):
        import struct
        data = (self.work / "unaccepted_outer10.bin").read_bytes()
        self.assertEqual(data[:32].decode().strip(), "UNACCEPTED_COLUMN_TRACE_V1")
        self.assertEqual(struct.unpack_from("=7i", data, 32), (2, 2, 2, 2, 1, 1, 1))
        self.assertIn("PASSIVE-TRACE-IMMUTABILITY PASS", self.output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
