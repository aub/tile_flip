import math
import TileCache
import TileCache.Layer
from TileCache.Layer import Tile
import pdb

class TileFinder:
 def __init__(self, tileCacheConfigFile):
	self.tileCacheConfigFile = tileCacheConfigFile
	self.service = TileCache.Service.load(self.tileCacheConfigFile)

 def findTiles(self, layerName, levels=None, bbox=None, tilePadding=0, block=None):
		try:
			tilePadding = int(tilePadding)
		except:
			raise Exception('Your tilePadding parameter is %s, but should be an integer' % tilePadding)

		tiles = []

		layer = self.service.layers[layerName] 
		if not levels: levels = (0, len(layer.resolutions))
		if not bbox: bbox = layer.bbox
		
		for z in range(*levels):
			bottomLeft = layer.getClosestCell(z, bbox[0:2])
			topRight	 = layer.getClosestCell(z, bbox[2:4])

			metaSize = layer.getMetaSize(z)
			ztiles = int(math.ceil(float(topRight[1] - bottomLeft[1]) / metaSize[0]) * math.ceil(float(topRight[0] - bottomLeft[0]) / metaSize[1]))

			startX = bottomLeft[0] - (1 * tilePadding)
			endX = topRight[0] + metaSize[0] + (1 * tilePadding)
			stepX = metaSize[0]
			startY = bottomLeft[1] - (1 * tilePadding)
			endY = topRight[1] + metaSize[1] + (1 * tilePadding)
			stepY = metaSize[1]

			for y in range(startY, endY, stepY):
				for x in range(startX, endX, stepX):
					tiles.append(Tile(layer, x, y, z))

		if block:
			for tile in tiles:
				block(tile)

		return tiles

	# Note that this only works with disk caches.
	def isTmsPathCached(self, layerName, x, y, z):
		layer = self.service.layers[layerName]
		tile = Tile(layer, x, y, z)
		return self.service.cache.access(self.service.getKey(tile))


