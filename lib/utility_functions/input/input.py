__author__ = 'cmotevasselani'

from lib.random_libs import libtcodpy as libtcod
from lib.constants.constants import Constants
from lib.utility_functions.util import Util
from lib.consoles.menu import Menu
from lib.constants.map_constants import MapConstants


class Input:


  @staticmethod
  def wait_for_keypress(state):
    key = libtcod.console_wait_for_keypress(True)
    if key.pressed == False:  # to prevent actions from being preformed twice
      state.set_player_action(Constants.DID_NOT_TAKE_TURN)
    return key

  @staticmethod
  def check_for_keypress(state):
    key = libtcod.console_check_for_keypress(True)
    if key.pressed == False:  # to prevent actions from being preformed twice
      state.set_player_action(Constants.DID_NOT_TAKE_TURN)
    return key

  @staticmethod
  def get_keypress(state, real_time):
    if real_time:
      return Input.check_for_keypress(state)
    else:
      return Input.wait_for_keypress(state)

  @staticmethod
  def handle_keys_after_keypress(key, state, real_time):
    if real_time:
      return Input.handle_playing_keys(key, state)
    else:
      return Input.handle_targeting_keys(key, state)

  @staticmethod
  def handle_keys(state, real_time):
    key = Input.get_keypress(state, real_time)
    while key.vk == libtcod.KEY_SHIFT:
      key = Input.get_keypress(state, real_time)
    # if key.vk == libtcod.KEY_ENTER and key.lalt:  # Toggle fullscreen
    #   libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    # elif key.vk == libtcod.KEY_ESCAPE:
    #   state.set_player_action(Constants.EXIT)
    return Input.handle_keys_after_keypress(key, state, real_time)

  @staticmethod
  def handle_targeting_keys(key, state):
    if key.vk == libtcod.KEY_CHAR:
      if key.c == ord('k'):
        return Util.player_target(state, 0, -1)
      elif key.c == ord('j'):
        return Util.player_target(state, 0, 1)
      elif key.c == ord('h'):
        return Util.player_target(state, -1, 0)
      elif key.c == ord('l'):
        return Util.player_target(state, 1, 0)
      elif key.c == ord('y'):
        return Util.player_target(state, -1, -1)
      elif key.c == ord('u'):
        return Util.player_target(state, 1, -1)
      elif key.c == ord('b'):
        return Util.player_target(state, -1, 1)
      elif key.c == ord('n'):
        return Util.player_target(state, 1, 1)
      elif key.c == ord('x'):
        state.status_panel.message("toggleing x: " + str(state.get_target_x()) + ', y: ' + str(state.get_target_y()))
        return Util.toggle_alive(state)
      elif key.c == ord('p'):
        if state.game_state == Constants.PAUSE:
          state.status_panel.message('handle_targeting_keys: going from paused to playing')
          state.game_state = Constants.PLAYING
          return
        elif state.game_state == Constants.PLAYING:
          state.status_panel.message('handle_targeting_keys: going from playing to paused')
          state.game_state = Constants.PAUSE
          return
        else:
          state.status_panel.message('game state is: ' + str(state.game_state))
      elif key.c == ord('s'):
        Util.save_map(state)
      else:
        state.set_player_action(Constants.NOT_VALID_KEY)

  @staticmethod
  def handle_playing_keys(key, state):
    if key.vk == libtcod.KEY_CHAR:
      if key.c == ord('p'):
        if state.game_state == Constants.PAUSE:
          state.status_panel.message('handle_targeting_keys: going from paused to playing')
          state.game_state = Constants.PLAYING
          return
        elif state.game_state == Constants.PLAYING:
          state.status_panel.message('handle_targeting_keys: going from playing to paused')
          state.game_state = Constants.PAUSE
          return
        else:
          state.status_panel.message('game state is: ' + str(state.game_state))
      else:
        state.set_player_action(Constants.NOT_VALID_KEY)





  @staticmethod
  def get_info(state, object):
    Menu().display_menu_return_index(
      object.get_info(state),
      [], MapConstants.INFO_SCREEN_WIDTH, state.con)
    state.set_player_action(Constants.NOT_VALID_KEY)

  @staticmethod
  def look(state):
    state.set_game_state(Constants.TARGETING)
    x, y = state.player.x, state.player.y
    while state.get_game_state() == Constants.TARGETING:
      (x, y) = Input.target_tile(state, x, y)
      if x is None or y is None:
        return Constants.CANCELLED
      for object in state.objects:
        if object.x == x and object.y == y:
          state.get_info(state, object)
          state.set_game_state(Constants.TARGETING)
          state.set_target(x, y)

  @staticmethod
  def target_tile(state, start_x=None, start_y=None):
    state.set_game_state(Constants.TARGETING)
    if start_x is None or start_y is None:
      state.set_target(state.player.x, state.player.y)
    else:
      state.set_target(start_x, start_y)
    while state.get_game_state() == Constants.TARGETING:
      Input.handle_keys(state)
      Util.refresh(state)

    if state.get_game_state() == Constants.FOUND_TARGET:
      x, y = state.get_target_coords()
      state.set_game_state(Constants.PLAYING)
    # TODO: Make target class? how to save/where to save targeting coords?
    # while
    if state.get_target_x() is None or state.get_target_y() is None:
      return Constants.CANCELLED
    state.game_map.get_map()[state.get_target_x()][state.get_target_y()].set_targeted(False)
    return state.get_target_x(), state.get_target_y()

  @staticmethod
  def target_monster(state, max_range=None):
    state.set_game_state(Constants.TARGETING)
    while state.get_game_state() == Constants.TARGETING:
      (x, y) = Input.target_tile(state)
      if x is None or y is None:
        return Constants.CANCELLED
      for object in state.objects:
        if object.x == x and object.y == y and object.fighter and object != state.player:
          return object






