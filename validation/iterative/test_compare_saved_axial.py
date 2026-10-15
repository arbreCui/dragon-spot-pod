#!/usr/bin/env python3
"""Analytic XSM checks for the saved axial comparator; no transport solver."""
import math
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = r'''
program fixture
use GANLIB
implicit none
type(c_ptr) :: ax,trk,mac,fl,groups,grp
integer :: j,nf,nu,i,st(40),key(6),m(6),zone(6)
real :: phi3(3),area(1),dz(6),basis(1),sig(3)
real(dp) :: phi6(6),u(13),coords(3),gram(1),h(3),leak(3),val
character(1) :: tag
character(12) :: path
do j=1,3
  write(tag,'(i1)') j
  nf=3
  if(j==2) nf=6
  nu=2*nf+1
  path='ax'//tag//'.xsm';call LCMOP(ax,path,0,2,0)
  path='trk'//tag//'.xsm';call LCMOP(trk,path,0,2,0)
  path='mac'//tag//'.xsm';call LCMOP(mac,path,0,2,0)
  st=0;st(1)=1;st(2)=nu;call LCMPUT(ax,'STATE-VECTOR',40,1,st)
  st=0;st(1)=nf;st(2)=nu;st(6)=1;st(7)=nf;st(8)=3;st(11)=nf
  call LCMPUT(trk,'STATE-VECTOR',40,1,st)
  st=0;st(1)=1;st(2)=3;st(4)=1;call LCMPUT(mac,'STATE-VECTOR',40,1,st)
  do i=1,nf
    key(i)=i;zone(i)=(i-1)/(nf/3)+1
  enddo
  m=1;dz=3.0/real(nf);area=1
  call LCMPUT(trk,'KEYFLX',nf,1,key);call LCMPUT(trk,'MATCOD',nf,1,m)
  call LCMPUT(trk,'MAT1D',nf,1,zone);call LCMPUT(trk,'VOLUME',nf,2,dz)
  call LCMPUT(trk,'VOL1D',nf,2,dz);call LCMPUT(trk,'AREA2D',1,2,area)
  phi3=[2.,3.,4.];phi6=[1._dp,3._dp,2._dp,4._dp,3._dp,5._dp]
  if(j==3) phi3=[1.,3.,5.]
  u=0
  if(nf==3) u(:3)=real(phi3,dp)
  if(nf==6) u(:6)=phi6
  fl=LCMLID(ax,'FLUX64',1);call LCMPDL(fl,1,nu,4,u)
  groups=LCMLID(mac,'GROUP',1);grp=LCMDIL(groups,1);sig=1
  call LCMPUT(grp,'NUSIGF',3,2,sig)
  val=1.2_dp;call LCMPUT(ax,'SPOT-X-KEFF',1,4,val)
  val=9;call LCMPUT(ax,'SPOT-X-NORM',1,4,val)
  key(1)=1;call LCMPUT(ax,'SPOT-X-RANK',1,1,key)
  key(:2)=[0,3];call LCMPUT(ax,'SPOT-X-OFF',2,1,key)
  key(:2)=[0,1];call LCMPUT(ax,'SPOT-X-GOFF',2,1,key)
  coords=[2._dp,3._dp,4._dp]/9
  if(j==3) coords=[1._dp,3._dp,5._dp]/9
  gram=1;h=1;leak=0;basis=1
  call LCMPUT(ax,'SPOT-X-A',3,4,coords);call LCMPUT(ax,'SPOT-X-GRAM',1,4,gram)
  call LCMPUT(ax,'SPOT-X-H',3,4,h);call LCMPUT(ax,'SPOT-X-L',3,4,leak)
  call LCMPUT(ax,'SPOT-X-BASIS',1,2,basis)
  call LCMCL(ax,1);call LCMCL(trk,1);call LCMCL(mac,1)
enddo
end program
'''


class AnalyticAxialComparison(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="spot-axial-compare-")
        cls.work = Path(cls.temporary.name)
        gan = ROOT / "Ganlib/lib/Darwin_arm64"
        flags = ["gfortran", "-O0", "-g", "-fcheck=all", "-ffp-contract=off",
                 "-I" + str(gan / "modules")]
        (cls.work / "fixture.f90").write_text(FIXTURE)
        for source, name in ((cls.work / "fixture.f90", "fixture"),
                             (Path(__file__).with_name("compare_saved_axial.f90"), "compare")):
            subprocess.run(flags + [str(source), str(gan / "libGanlib.a"), "-lstdc++",
                                    "-o", str(cls.work / name)], check=True, capture_output=True, timeout=30)
        subprocess.run([str(cls.work / "fixture")], cwd=cls.work, check=True, capture_output=True, timeout=10)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def compare(self, a, b):
        args = [f"{name}{n}.xsm" for n in (a, b) for name in ("ax", "trk", "mac")]
        return subprocess.run([str(self.work / "compare"), *args], cwd=self.work,
                              capture_output=True, text=True, timeout=10)

    def metrics(self, a, b):
        result = self.compare(a, b)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return {s[0]: list(map(float, s[1:])) for line in result.stdout.splitlines()
                if (s := line.split()) and not s[0].startswith("SAVED-AXIAL")}

    def test_identity_is_exact(self):
        result = self.metrics(1, 1)
        self.assertEqual(result["CANONICAL_RRHO_RLEAK_DLEAK_RA"], [0]*4)
        self.assertEqual(result["PHYSICAL_FLUX_RELATIVE_VOLUME_L2"], [0])

    def test_nested_grid_uses_volume_average(self):
        result = self.metrics(1, 2)
        self.assertAlmostEqual(result["PHYSICAL_FLUX_RELATIVE_VOLUME_L2"][0], 0, places=15)
        self.assertEqual(result["FISSION_NORM64"], [9, 9])
        self.assertEqual(result["CANONICAL_RRHO_RLEAK_DLEAK_RA"], [0]*4)

    def test_known_shape_difference(self):
        result = self.metrics(1, 3)
        expected = math.sqrt(2/35)
        self.assertAlmostEqual(result["PHYSICAL_FLUX_RELATIVE_VOLUME_L2"][0], expected, places=14)
        self.assertAlmostEqual(result["CANONICAL_RRHO_RLEAK_DLEAK_RA"][3], expected, places=14)

    def test_wrong_refinement_direction_is_refused(self):
        self.assertNotEqual(self.compare(2, 1).returncode, 0)

    def test_physical_only_does_not_report_a_modal_norm(self):
        paths = [f"{name}{n}.xsm" for n in (1, 3) for name in ("ax", "trk", "mac")]
        result = subprocess.run([str(self.work / "compare"), *paths, "--physical-only"],
                                cwd=self.work, capture_output=True, text=True, check=True, timeout=10)
        self.assertIn("MODAL_COMPARISON OMITTED_PHYSICAL_ONLY", result.stdout)
        self.assertNotIn("CANONICAL_RRHO_RLEAK_DLEAK_RA", result.stdout)
        row = next(s for s in result.stdout.splitlines() if s.startswith("PHYSICAL_FLUX_RELATIVE_VOLUME_L2"))
        self.assertAlmostEqual(float(row.split()[1]), math.sqrt(2/35), places=14)


if __name__ == "__main__":
    unittest.main(verbosity=2)
