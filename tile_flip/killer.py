import heapq
import os
import TileCache
import pdb
from TileCache.Layer import Tile
from tile_flip.tile_finder import TileFinder

class Killer:
	def __init__(self, tileCacheConfigFile):
		self.tileCacheConfigFile = tileCacheConfigFile
		self.service = TileCache.Service.load(self.tileCacheConfigFile)

	def killForPoint(self, layerName, point, delta=0.0, levels=None, tilePadding=0):
		bbox = (point[0] - delta, point[1] - delta, point[0] + delta, point[1] + delta)
		finder = TileFinder(self.tileCacheConfigFile)
		func = lambda tile: self.service.cache.delete(tile)
		finder.findTiles(layerName, levels, bbox, tilePadding, func)

	def killForTmsPath(self, layerName, x, y, z):
		layer = self.service.layers[layerName]
		tile = Tile(layer, x, y, z)
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
				print >>sys.stderr, "Error removing tile %s: %s" % (path, e)

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
				path = os.path.join(root, file)
				stat = os.stat(path)
				size = stat.st_size
				if hasattr(stat, 'st_blocks'):
					size = stat.st_blocks * stat.st_blksize
					# strip off rootdir to keep RAM use down
					path = path[len(self.__cachePath()):]
					heapq.heappush(heap, (stat.st_atime, size, path))
					cacheSize += size
		return heap, cacheSize

