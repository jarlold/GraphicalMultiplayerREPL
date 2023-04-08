import pyglet
from pyglet.gl import *

import node_types
import player

from node_manager import NodeManager

class CPO:

    # Game Information
    game_version = "2.0.0"

    # Screen Information
    width = 800
    height = 600
    fullscreen = False
    window = pyglet.window.Window(width=width, height=height, fullscreen=fullscreen)

    # Font settings
    default_font = "VT323"

    # Texture settings
    general_scale = 4

    # Game objects
    node_manager = NodeManager()
    nm = node_manager # I have to type this a lot ok, hopefully this doesn't fuck things up later

    # Normal settings
    game_controls = {
        "UP": ord("w"),
        "DOWN": ord("s"),
        "LEFT": ord("a"),
        "RIGHT": ord("d")
        }

    @staticmethod
    def setup_window(): 
        glTranslatef(CPO.window.width/2.0, CPO.window.height/2.0, 0 )
        CPO.nm.add_node(
                node_types.SpriteNode()
                )
        CPO.nm.add_node(
                player.PlayerNode(y=100)
                )

        CPO.window.keystat = pyglet.window.key.KeyStateHandler()
        CPO.window.push_handlers(CPO.window.keystat)
        
    @staticmethod
    def start_game():
        # Avoding a ciruclar import, I know there are better ways to do this...
        node_types.CPO = CPO
        player.CPO = CPO
    
        CPO.setup_window()

        pyglet.clock.schedule_interval(CPO.on_update, 1/60.0)

        pyglet.app.run()

    @staticmethod
    def is_key_down(key):
        return CPO.window.keystat[key]

    @staticmethod
    @window.event
    def on_draw():
        CPO.window.clear()
        CPO.node_manager.draw_nodes()

    @staticmethod
    @window.event
    def on_mouse_press(x, y, button, mod):
        CPO.nm.on_mouse_press(x, y, button, mod)

    @staticmethod
    @window.event
    def on_mouse_release(x,y,button,mod):
        CPO.nm.on_mouse_release(x, y, button, mod)

    @staticmethod
    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        CPO.nm.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    @staticmethod
    @window.event
    def on_key_press(k, mod):
        CPO.nm.on_key_press(k, mod)


    @staticmethod
    def on_update(self):
        CPO.nm.on_update()



