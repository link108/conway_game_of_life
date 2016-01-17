from lib.random_libs import libtcodpy as libtcod

__author__ = 'cmotevasselani'

import shelve
from lib.constants.map_constants import MapConstants


class Util:

  @staticmethod
  def get_adjacent_tiles(game_map, x, y):
    adjacent_tiles = []
    for i in range(-1, 2):
      for j in range(-1, 2):
        if i == 0 and j == 0:
          continue
        else:
            temp_x = x + i
            temp_y = y + j
            if temp_x < len(game_map) and temp_y < len(game_map[temp_x]):
              adjacent_tiles.append(game_map[temp_x][temp_y])
    return adjacent_tiles

  @staticmethod
  def save_map(state):
    file = shelve.open(Constants.SAVE_FILE, 'n')
    file['game_map'] = self.state.game_map.game_map
    file.close()

  # def load_game(self):
  #   self.state.game_map = Map(self.state)
  #   file = shelve.open(Constants.SAVE_FILE, 'r')
  #   self.state.game_map.game_map = file['game_map']
  #   file.close()
  #   self.initialize_fov(self.state.dungeon_level)


  @staticmethod
  def toggle_alive(state):
    if state.game_map.game_map[state.get_target_x()][state.get_target_y()].alive:
      state.game_map.game_map[state.get_target_x()][state.get_target_y()].alive = False
    else:
      state.game_map.game_map[state.get_target_x()][state.get_target_y()].alive = True

  @staticmethod
  def player_target(state, dx, dy):
    state.game_map.game_map[state.get_target_x()][state.get_target_y()].targeted = False

    x = state.get_target_x() + dx
    y = state.get_target_y() + dy
    state.game_map.game_map[x][y].targeted = True
    state.set_target(x, y)

  @staticmethod
  def get_count_of_adjacent_tile(game_map, x, y):
    count = 0
    adjacent_tiles = Util.get_adjacent_tiles(game_map, x, y)
    for tile in adjacent_tiles:
      if tile.alive:
        count += 1
    return count

  @staticmethod
  def refresh(state):
    state.fov_recompute = True
    Util.render_all(state)
    libtcod.console_flush()
    for object in state.objects:
      object.clear(state.con)

  @staticmethod
  def render_all(state):
    for y in range(MapConstants.MAP_HEIGHT):
      for x in range(MapConstants.MAP_WIDTH):
        alive = state.game_map.game_map[x][y].alive
        targeted = state.game_map.game_map[x][y].targeted
        # it is visible
        if targeted:
          libtcod.console_set_char_background(state.con, x, y, MapConstants.COLOR_TARGETED, libtcod.BKGND_SET)
        elif alive:
          libtcod.console_set_char_background(state.con, x, y, MapConstants.COLOR_LIGHT_WALL, libtcod.BKGND_SET)
        else:
          libtcod.console_set_char_background(state.con, x, y, MapConstants.COLOR_lIGHT_GROUND, libtcod.BKGND_SET)
        state.game_map.game_map[x][y].explored = True
    libtcod.console_blit(state.con, 0, 0, MapConstants.SCREEN_WIDTH, MapConstants.SCREEN_HEIGHT, 0, 0, 0)
    # prepare to render the GUI panel
    libtcod.console_set_default_background(state.status_panel.get_panel(), libtcod.black)
    libtcod.console_clear(state.status_panel.get_panel())
    y = 1
    for (line, color) in state.status_panel.game_messages:
      libtcod.console_set_default_foreground(state.status_panel.get_panel(), color)
      libtcod.console_print_ex(state.status_panel.get_panel(), MapConstants.MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT,
        line)
      y += 1
    # state.status_panel.render_bar(1, 1, MapConstants.BAR_WIDTH, 'game_map_id', state.game_map.game_map_id,
    #                               state.player.fighter.max_hp(state),
    #                               libtcod.light_red, libtcod.darker_red)
    libtcod.console_print_ex(state.status_panel.get_panel(), 1, 4, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Mode: ' + str(state.game_type))
    libtcod.console_print_ex(state.status_panel.get_panel(), 1, 5, libtcod.BKGND_NONE, libtcod.LEFT,
      'Game map id:  ' + str(state.game_map.game_map_id))
    libtcod.console_print_ex(state.status_panel.get_panel(), 1, 6, libtcod.BKGND_NONE, libtcod.LEFT,
      'Turn: ' + str(state.turn))
    # blit the contents of "panel" to the root console
    libtcod.console_blit(state.status_panel.get_panel(), 0, 0, MapConstants.SCREEN_WIDTH, MapConstants.PANEL_HEIGHT, 0,
      0, MapConstants.PANEL_Y)

