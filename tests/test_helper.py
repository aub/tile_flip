import os
import pdb
import shutil
import TileCache
from TileFlip.Seeder import Seeder
from TileCache.Layer import Tile
from TileCache.Service import Service

def clearCache():
	path = os.path.join(os.path.dirname(__file__), 'cache')
	if os.path.isdir(path):
		shutil.rmtree(path)
	
def testConfigFile():
	return os.path.join(os.path.dirname(__file__), 'data', 'tileCacheConfig.cfg')

def seedTile(x, y, z):
	seeder = Seeder(testConfigFile())
	seeder.seedForTmsPath('polar', x, y, z)

def getTile(x, y, z):
	service = TileCache.Service.load(testConfigFile())
	layer = service.layers['polar']
	return Tile(layer, x, y, z)

def seedPoint(x, y):
	seeder = Seeder(testConfigFile())
	seeder.seedForPoint('polar', (x, y), force=True)

def filePath(x, y, z):
	service = TileCache.Service.load(testConfigFile())
	layer = service.layers['polar']
	tile = Tile(layer, x, y, z)
	key = service.cache.getKey(tile)	
	return os.path.join(os.path.dirname(__file__), '..', key)

def assertTileIsCached(testCase, x, y, z):
	testCase.assertEqual(True, os.path.exists(filePath(x, y, z)))

def assertTileIsNotCached(testCase, x, y, z):
	testCase.assertEqual(False, os.path.exists(filePath(x, y, z)))

