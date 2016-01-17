
__author__ = 'cmotevasselani'

from random import randrange
from lib.constants.map_constants import MapConstants
from lib.map_components.tile import Tile
from lib.utility_functions.util import Util

class Map:

  def __init__(self):
    self.game_map = None
    self.game_maps = []
    self.game_map_id = 0
    self.previous_map_id = 1

  def generate_map(self, state, game_map_function):
    self.game_maps.insert(0, [[Tile(x, y, True, explored=state.debug)
                               for y in range(MapConstants.MAP_HEIGHT)]
                              for x in range(MapConstants.MAP_WIDTH)])
    self.game_maps.insert(1, [[Tile(x, y, True, explored=state.debug)
                               for y in range(MapConstants.MAP_HEIGHT)]
                               for x in range(MapConstants.MAP_WIDTH)])
    game_map_function(self.game_maps[self.game_map_id])
    # Map.create_random_map(self.game_maps[self.game_map_id])
    # Map.create_static_map(self.game_maps[self.game_map_id])
    self.game_map = self.game_maps[self.game_map_id]

  def update_game_map_id(self):
    self.game_map_id, self.previous_map_id = self.previous_map_id, self.game_map_id

  def process_map(self, state):
    self.update_game_map_id()
    for column in self.game_maps[self.previous_map_id]:
      for tile in column:
        num_adjacent_alive = Util.get_count_of_adjacent_tile(self.game_maps[self.previous_map_id], tile.x, tile.y)
        if tile.alive:
          if num_adjacent_alive < 2 or num_adjacent_alive > 3:
            self.game_maps[self.game_map_id][tile.x][tile.y].alive = False
          else:
            self.game_maps[self.game_map_id][tile.x][tile.y].alive = True
        else:
          if num_adjacent_alive == 3:
            self.game_maps[self.game_map_id][tile.x][tile.y].alive = True
          else:
            self.game_maps[self.game_map_id][tile.x][tile.y].alive = False
    self.game_map = self.game_maps[self.game_map_id]

  @staticmethod
  def create_static_map(game_map):
    for column in game_map:
      for tile in column:
        tile.alive = False
    game_map[30][13].alive = True
    game_map[30][14].alive = True
    game_map[31][13].alive = True
    game_map[31][14].alive = True


    game_map[21][14].alive = True
    game_map[22][14].alive = True
    game_map[23][14].alive = True

  @staticmethod
  def create_blank_map(game_map):
    for column in game_map:
      for tile in column:
        tile.alive = False

  @staticmethod
  def create_random_map(game_map):
    for column in game_map:
      for tile in column:
        if randrange(0,2,1):
          tile.alive = True
        else:
          tile.alive = False

