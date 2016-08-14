'''
Created on Jun 2, 2015

@author: Joseph Lim
'''
from numpy import array


class GameContext(object):

    """ This contains all the environmental constants used by the game """

    # Display resolution
    display_width = 1920
    display_height = 1080

    display_map_width = 1600
    display_map_height = 1040
    display_border = 20  # Edge around the screen for scrolling

    display_info_width = 280
    display_info_height = 300

    # Cameras
    display_camera = array([0, 0])
    display_scroll_speed = 2
    display_camera_bounds = (20, 20)

    # Hex cell constants
    hex_colour_border = (0, 0, 0)
    hex_colour_internal = (85, 107, 47)
    hex_colour_selection_border = (255, 0, 0)
    hex_colour_selection_internal = (255, 128, 128)
    hex_width = 75.0  # 43
    hex_height = 75.0

    # Turn based constants
    turn_number = 1
    turn_player_index = 1
    turn_players = [1, 2]

    # Graphics layers
    view_main = None
    view_terrain = None
    view_units = None
    view_ui = None

    # Animation
    clock_tick = 0
    clock_elapsed = 0

    @property
    def display_map_rect(self):
        """ Top left corner of map rect """
        return array([self.display_border, self.display_border])
