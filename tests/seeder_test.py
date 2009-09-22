import os
import unittest
import mox
import pdb
import TileCache
from TileFlip.Seeder import Seeder
from test_helper import *

class SeederTests(unittest.TestCase):

	def testTileCacheService(self):
		service = TileCache.Service.load(testConfigFile())
		self.assertEqual(service.layers.keys(), ['polar'])
		self.assertEqual(type(service.cache), TileCache.Caches.Disk.Disk)

	def testSeedByBoundingBox(self):
		seeder = Seeder(testConfigFile())
		seeder.seedForPoint('polar', (2, 6), (0.0, 0.0), 1.0, 0, True)
	
	def testSeedByTmsPath(self):
		seeder = Seeder(testConfigFile())
		seeder.seedForTmsPath('polar', 10, 15, 12, True)
		assertTileIsCached(self, 10, 15, 12)

if __name__ == '__main__':
	unittest.main()

