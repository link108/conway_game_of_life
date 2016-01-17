__author__ = 'cmotevasselani'

class Tile:
  # a tile of the map and its properties

  def __init__(self, x, y, alive, block_sight=None, explored=None):
    self.alive = alive
    # self.color = color
    self.x = x
    self.y = y
    self.targeted = False

  def set_blocked(self, value):
    self.blocked = value

  def set_targeted(self, value):
    self.targeted = value

  def set_explored(self, value):
    self.explored = value

  def set_block_sight(self, value):
    self.block_sight = value
