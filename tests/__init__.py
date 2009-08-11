import unittest
from killer_test import KillerTests
from tile_finder_test import TileFinderTests

suite = unittest.TestLoader().loadTestsFromTestCase(TileFinderTests)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(KillerTests)
unittest.TextTestRunner(verbosity=2).run(suite)
