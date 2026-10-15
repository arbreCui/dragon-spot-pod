import unittest
import numpy as np
from audit_fe56_temperature_interpolation import weights,mix_nodes

class TemperatureWeights(unittest.TestCase):
    temperatures=[293.,550.,900.,1200.,2000.]
    def test_node_identity(self):
        for order in (1,3):
            for i,t in enumerate(self.temperatures):
                expected=np.zeros(5,dtype=np.float32);expected[i]=1
                np.testing.assert_array_equal(weights(self.temperatures,t,order),expected)
    def test_cubic_negative_support_produces_undershoot(self):
        w=weights(self.temperatures,np.float32(893.15))
        self.assertLess(w[3],0)
        nodes=[np.array([[v]],dtype=np.float32) for v in (0,0,0,1,0)]
        self.assertLess(mix_nodes(nodes,w)[0,0],0)
    def test_linear_bracket_is_nonnegative(self):
        for t in (748.15,893.15):
            w=weights(self.temperatures,t,1)
            self.assertTrue(np.all(w>=0));self.assertEqual(np.count_nonzero(w),2)
            self.assertEqual(float(np.float32(w.sum())),1.)
            self.assertEqual(list(np.flatnonzero(w)),[1,2])
    def test_invalid_grid_rejected(self):
        with self.assertRaises(AssertionError):weights([293,900,550,1200],748)

if __name__=='__main__':unittest.main()
