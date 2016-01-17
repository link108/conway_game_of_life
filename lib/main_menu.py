__author__ = 'cmotevasselani'

import shelve
from time import sleep
from lib.random_libs import libtcodpy as libtcod
from lib.map_components.map import Map
from lib.utility_functions.state import State
from lib.constants.map_constants import MapConstants
from lib.constants.constants import Constants
from lib.utility_functions.util import Util
from lib.consoles.menu import Menu
from lib.high_scores.high_scores import HighScores
from lib.utility_functions.input.input import Input


class MainMenu:

  def __init__(self, args):
    self.state = State()
    self.state.init_stuff()
    self.state.debug = bool(args.debug)
    self.state.god_mode = bool(args.god_mode)
    self.menu = Menu()
    self.state.high_scores = HighScores()

  def main_menu(self):
    # img = libtcod.image_load('rl_image.png')
    # show the background image, at twice the regular console resolution
    while not libtcod.console_is_window_closed():
      # libtcod.image_blit_2x(img, 0, 0, 0)
      choice = self.menu.display_menu_return_index('', ['Play a new game', 'Continue last game',
                                                        'Custom Map Mode', 'High Scores', 'Quit'], 30,
                                                   self.state.con)
      if choice == 0:
        self.new_game()
        self.play_game()
      elif choice == 1:
        try:
          self.load_game()
        except:
          self.message_box('No saved game to load', 24)
          continue
        self.play_game()
      elif choice == 2:
        self.make_custom_map()
        self.make_map_mode()
      elif choice == 3:
        self.show_high_scores()
      elif choice == 4:
        break

  def show_high_scores(self):
    self.state.high_scores.show_high_scores(self.state, self.menu)

  def message_box(self, message, size=50):
    self.menu.display_menu_return_index(message, [], size, self.state.con)

  def make_custom_map(self):
    self.setup_game()
    self.state.game_map = Map()
    self.state.game_map.generate_map(self.state, Map.create_blank_map)
    self.initialize_fov(self.state.dungeon_level)
    self.state.set_player_action(None)

  def make_map_mode(self):
    self.state.set_game_state(Constants.PLAYING)
    self.state.set_player_action(None)
    self.state.fov_recompute = True

    while not libtcod.console_is_window_closed():
      self.state.turn += 1
      Util.render_all(self.state)
      libtcod.console_flush()
      if Input.handle_keys(self.state) == "play":
        self.state.game_map.game_map[self.state.get_target_x()][self.state.get_target_y()].targeted = False
        self.state.status_panel.message('hihi')
        self.play_game()
    self.state.status_panel.message('###### Turn ' + str(self.state.turn) + ' has ended')

  def setup_game(self):
    self.state.status_panel.game_messages = []
    self.state.status_panel.message('Starting the game of life',
                                    libtcod.red)
    self.state.turn = 0
    self.state.score = 0

  def new_game(self):
    self.setup_game()
    self.state.game_map = Map()
    self.state.game_map.generate_map(self.state, Map.create_random_map)
    self.initialize_fov(self.state.dungeon_level)

  def initialize_fov(self, dungeon_level):
    self.state.fov_map_map[dungeon_level] = libtcod.map_new(MapConstants.MAP_WIDTH, MapConstants.MAP_HEIGHT)
    libtcod.console_clear(self.state.con)
    for y in range(MapConstants.MAP_HEIGHT):
      for x in range(MapConstants.MAP_WIDTH):
        libtcod.map_set_properties(self.state.fov_map_map[dungeon_level], x, y,
                                   True, True)
    self.state.fov_map = self.state.fov_map_map[dungeon_level]

  def play_game(self):
    self.state.set_player_action(None)
    self.state.fov_recompute = True

    while not libtcod.console_is_window_closed():
      sleep(0.20)
      self.state.turn += 1
      Util.render_all(self.state)
      libtcod.console_flush()
      self.state.game_map.process_map(self.state)
    self.state.status_panel.message('###### Turn ' + str(self.state.turn) + ' has ended')

  def save_game(self):
    file = shelve.open(Constants.SAVE_FILE, 'n')
    file['game_map'] = self.state.game_map.game_map
    file.close()

  def load_game(self):
    self.state.game_map = Map(self.state)
    file = shelve.open(Constants.SAVE_FILE, 'r')
    self.state.game_map.game_map = file['game_map']
    file.close()
    self.initialize_fov(self.state.dungeon_level)
