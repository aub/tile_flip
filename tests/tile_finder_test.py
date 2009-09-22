import os
import unittest
import mox
import pdb
import TileCache
from TileFlip.TileFinder import TileFinder
from test_helper import *

class TileFinderTests(unittest.TestCase):

	def countTiles(self, tile):
		self.tileCount += 1

	def setUp(self):
		self.finder = TileFinder(testConfigFile())
		self.tileCount = 0

	def testFindingSimpleTiles(self):
		tiles = self.finder.findTiles('polar', (0, 2))
		self.assertEqual(8, len(tiles))

	def testDoingSomethingToEachTile(self):
		tiles = self.finder.findTiles('polar', (0, 2), block=self.countTiles)
		self.assertEqual(8, self.tileCount)
	
if __name__ == '__main__':
	unittest.main()
