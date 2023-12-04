from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
__version__ = '0.6.6'

# For `debug` support on Mac, we need to preload tkinter
from designer.system import setup_debug_mode
setup_debug_mode()

# Actually import all dependencies
import pygame
from designer.core.director import *
from designer.core.event import *
from designer.helpers import *
from designer.animation import *
from designer.utilities.easings import *
from designer.objects import *
from designer.colors import *
from designer.positioning import *
from designer.keyboard import *
from designer.mouse import *
from designer.movement import *

GLOBAL_DIRECTOR: Director = None

__all__ = [
    '__version__',
    'circle', 'ellipse', 'Circle', 'Ellipse',
    'arc', 'line', 'Arc', 'Line',
    'rectangle', "Rectangle",
    'text', "Text",
    'shape', 'lines', 'pen', "Shape", "Pen",
    'background_image',
    'image', 'emoji', "Image", "Emoji",
    'group',
    'draw',
    # Window information
    'set_window_color', 'get_window_color',
    'set_window_size',
    'set_background_image', 'set_window_image',
    'get_background_image', 'get_window_image',
    'get_height', 'get_window_height',
    'get_width', 'get_window_width',
    'set_window_title', 'get_window_title', 'set_window_image',
    'get_window_layers', 'set_window_layers',
    # Scene information
    'set_scene_image', 'get_scene_image',
    'set_scene_color', 'get_scene_color',
    'get_scene_height', 'get_scene_width',
    'set_scene_layers', 'get_scene_layers',
    # Events
    'when', 'starting', 'updating', 'typing', 'clicking',
    'start', 'debug',
    'stop', 'restart',
    'pause', 'resume',
    'colliding', 'colliding_with_mouse', 'would_collide',
    'destroy',
    'DesignerObject',
    # Positioning
    'above', 'below', 'beside',
    # Director stuff
    'get_director',
    'change_scene', 'push_scene', 'pop_scene',
    # Keyboard stuff
    'get_keyboard_repeat', 'set_keyboard_repeat',
    'get_keyboard_delay', 'set_keyboard_delay',
    'get_keyboard_interval', 'set_keyboard_interval',
    'enable_keyboard_repeating', 'disable_keyboard_repeating',
    # Mouse stuff
    'get_mouse_cursor', 'set_mouse_cursor',
    'get_mouse_visible', 'set_mouse_visible',
    'get_mouse_position', 'set_mouse_position',
    'get_mouse_x', 'get_mouse_y',
    # Animations
    'Animation', 'linear_animation', 'sequence_animation',
    'glide_around',
    'glide_right',
    'glide_left',
    'glide_up',
    'glide_down',
    'glide_in_degrees',
    'spin',
    # Easings
    'Linear', 'Iterate',
    # Pixels
    'get_pixels', 'get_pixels2d',
    # Music
    'play_sound',
    'play_music', 'background_music', 'pause_music', 'set_music_volume', 'is_music_playing',
    'get_music_volume', 'stop_music', 'rewind_music', 'continue_music', 'set_music_position', 'get_music_position',
    # Movement
    'move_forward', 'move_backward', 'turn_left', 'turn_right', 'go_to', 'go_to_xy', 'go_to_mouse',
    'point_towards', 'point_towards_mouse', 'point_in_direction', 'change_xy', 'change_x', 'change_y', 'set_x', 'set_y',
    'get_angle', 'get_x', 'get_y',
    'flip_x', 'flip_y', 'set_flip_x', 'set_flip_y', 'set_scale', 'set_scale_x', 'set_scale_y', 'set_background_image',
    'get_scale', 'get_scale_x', 'get_scale_y', 'get_visible', 'get_flip_x', 'get_flip_y', 'show', 'hide',
    'grow', 'grow_x', 'grow_y', 'shrink',
    'move_to_x', 'move_to_y', 'move_to', 'move_to_mouse', 'move_to_xy',
    'set_visible', 'change_scale',
    # Emoji specific
    'get_emoji_name', 'set_emoji_name',
    'get_text', 'set_text',
]
