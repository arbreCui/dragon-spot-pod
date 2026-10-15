"""Run the complete implementation controls against the frozen-header rebuild."""
import importlib.util
from pathlib import Path
import sys
import unittest

root=Path(sys.argv[1]).resolve()
spec=importlib.util.spec_from_file_location('layered_vendor_tests',root/'build/test_native_layered_transport.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
module.LIB=root/'verification/vendor_rebuild.dylib'
result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(module.LayeredTests))
if not result.wasSuccessful():raise SystemExit(1)
