import os
import unittest
import mox
import pdb
import TileCache
from tile_flip.killer import Killer
from test_helper import *

class KillerTests(unittest.TestCase):

	def setUp(self):
		clearCache()
		self.killer = Killer(testConfigFile())

	def testKillForPoint(self):
		seedPoint(0.0, 0.0)
		assertTileIsCached(self, 262144, 587769, 19)
		self.killer.killForPoint('polar', (0.0, 0.0))
		assertTileIsNotCached(self, 262144, 587769, 19)


	def testKillByTmsPath(self):
		seedTile(12, 70, 14)
		assertTileIsCached(self, 12, 70, 14)
		self.killer.killForTmsPath('polar', 12, 70, 14)
		assertTileIsNotCached(self, 12, 70, 14)

	def testKillToSize(self):
		seedTile(12, 70, 14)
		assertTileIsCached(self, 12, 70, 14)
		self.killer.killToSize(0.0)
		assertTileIsNotCached(self, 12, 70, 14)

	def testKillTile(self):
		seedTile(700, 600, 14)
		assertTileIsCached(self, 700, 600, 14)
		self.killer.killTile(getTile(700, 600, 14))
		assertTileIsNotCached(self, 700, 600, 14)
	
if __name__ == '__main__':
	unittest.main()
