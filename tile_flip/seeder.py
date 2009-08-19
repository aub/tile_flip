import TileCache
from TileCache.Layer import Tile
from tile_flip.tile_finder import TileFinder
import pdb

class Seeder:
	def __init__(self, tileCacheConfigFile, userId=-1, groupId=-1):
		self.tileCacheConfigFile = tileCacheConfigFile
		self.service = TileCache.Service.load(self.tileCacheConfigFile)

	def seedForPoint(self, layerName, point, delta=(0.0, 0.0), levels=None, tilePadding=0, force=False):
		bbox = (point[0] - delta[0], point[1] - delta[1], point[0] + delta[0], point[1] + delta[1])
		finder = TileFinder(self.tileCacheConfigFile)
		func = lambda tile: self.__processTile(tile, force)
		finder.findTiles(layerName, levels, bbox, tilePadding, func)

	def seedForTmsPath(self, layerName, x, y, z, force=False):
		layer = self.service.layers[layerName]
		tile = Tile(layer, x, y, z)
		self.service.renderTile(tile, force=force)

	def seedForTile(self, tile, force=False):
		self.service.renderTile(tile, force=force)

	def __processTile(self, tile, force=False):
		self.service.renderTile(tile, force=force)
