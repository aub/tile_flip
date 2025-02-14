import heapq
import os
import sys
import TileCache
from TileCache.Layer import Tile
from TileFlip.TileFinder import TileFinder

class Killer:
	def __init__(self, tileCacheConfigFile):
		self.tileCacheConfigFile = tileCacheConfigFile
		self.service = TileCache.Service.load(self.tileCacheConfigFile)
		self.tileFinder = TileFinder(self.tileCacheConfigFile)

	def killForPoint(self, layerName, point, delta=(0.0, 0.0), levels=None, tilePadding=0):
		bbox = (point[0] - delta[0], point[1] - delta[1], point[0] + delta[0], point[1] + delta[1])
		func = lambda tile: self.service.cache.delete(tile)
		self.tileFinder.findTiles(layerName, levels, bbox, tilePadding, func)

	def killForTmsPath(self, layerName, x, y, z):
		tile = self.tileFinder.tileForTmsPath(layerName, x, y, z)
		self.service.cache.delete(tile)

	def killToSize(self, maxMBs):
		maxBytes = maxMBs * 1048576
		heap, cacheSize = self.__walkDiskCache()
		while heap and cacheSize > maxBytes:
			atime, size, path = heapq.heappop(heap)
			cacheSize -= size
			path = self.__cachePath() + path
			try:
				os.unlink(path)
			except OSError, e:
				print >> sys.stderr, "Error removing tile %s: %s" % (path, e)

	def killAll(self):
		if os.path.isdir(self.__cachePath()):
			shutil.rmtree(self.__cachePath())

	def killTile(self, tile):
		self.service.cache.delete(tile)

	def __cachePath(self):
		return self.service.cache.basedir

	def __walkDiskCache(self):
		heap = []
		cacheSize = 0
		for root, dirs, files in os.walk(self.__cachePath()):
			for file in files:
				try:
					path = os.path.join(root, file)
					stat = os.stat(path)
					size = stat.st_size
					# We're going to use the actual on-disk size for now, until that proves to be
					# a problem.
					if False: #hasattr(stat, 'st_blocks'):
						size = stat.st_blocks * stat.st_blksize
					# strip off rootdir to keep RAM use down
					path = path[len(self.__cachePath()):]
					heapq.heappush(heap, (stat.st_atime, size, path))
					cacheSize += size
				except OSError:
					pass
		return heap, cacheSize

