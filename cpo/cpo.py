# Standard lib
from random import randint
from threading import Thread

# Remote packages
import pyglet
from pyglet.gl import *

# Local packages
from cpo.node_manager import NodeManager
from cpo.default_resources import default_textures
from cpo import server
from cpo import client
from cpo import node_types
from cpo import menus
from cpo import menu_nodes
from cpo import node_manager


class CPO:
    # Game Information
    game_version = "2.0.0"

    # Normal settings
    game_controls = {
        "UP": ord("w"),
        "DOWN": ord("s"),
        "LEFT": ord("a"),
        "RIGHT": ord("d")
        }

    mouse_x = 0
    mouse_y = 0

    # Screen Information
    width = 1820
    height = 900
    fullscreen = False
    window = pyglet.window.Window(width=width, height=height, fullscreen=fullscreen)
    screen_pan_x = 0
    screen_pan_y = 0

    # Font settings
    default_font = "VT323"

    # Texture settings
    general_scale = 4

    # Game objects
    node_manager = None
    nm = None # I have to type this a lot ok, so when we initialize node_manager set this to point to it as well

    menu_manager = None
    mm = None

    # Networking stuff
    is_client = False
    is_server = False
    client = None
    server = None
    network_thread = None
    ip, port = "127.0.0.1", 8763 + randint(1, 10)


    @staticmethod
    def setup_window(): 
        glTranslatef(CPO.window.width/2.0, CPO.window.height/2.0, 0 )
        CPO.window.keystat = pyglet.window.key.KeyStateHandler()
        CPO.window.push_handlers(CPO.window.keystat)
        glViewport( 0, 0, CPO.width, CPO.height )

    @staticmethod
    def start_server():
        print("Hosting server on {}:{}".format(CPO.ip, CPO.port))
        CPO.server = server.Server(CPO.ip, CPO.port)
        CPO.network_thread = Thread(target=CPO.server.serve, args=[])
        CPO.network_thread.start()


    @staticmethod
    def connect_server():
        print("Connecting to {}:{}...".format(CPO.ip, CPO.port))
       #CPO.nm.add_nodes([
       #        node_types.PlayerNode(y=0, z=0) ])

        CPO.client = client.Client(CPO.ip, CPO.port)
        CPO.network_thread = Thread(target=CPO.client.connect, args=[])
        CPO.network_thread.start()

    @staticmethod
    def initialize_systems():
        # Game objects
        CPO.node_manager = NodeManager()
        CPO.nm = CPO.node_manager # I have to type this a lot ok, so when we initialize node_manager set this to point to it as well

        CPO.menu_manager = menus.MenuManager()
        CPO.mm = CPO.menu_manager
        
        
    @staticmethod
    def start_game():

        # Avoding a ciruclar import, I know there are better ways to do this...
        node_types.CPO = CPO
        client.CPO = CPO
        server.CPO = CPO
        menus.CPO = CPO
        menu_nodes.CPO = CPO
        node_manager.CPO = CPO

        CPO.initialize_systems() 
        CPO.setup_window()

        if CPO.is_client:
            CPO.connect_server()

        if CPO.is_server:
            CPO.nm.start_world()
            CPO.nm.start_server()

        if not CPO.is_server and not CPO.is_client:
            CPO.nm.start_world()
       

        pyglet.clock.schedule_interval(CPO.on_update, 1/60.0)
        pyglet.clock.schedule_interval(CPO.draw_all, 1/60.0)
        pyglet.app.run()


    @staticmethod
    def pan_camera(x, y):
        CPO.screen_pan_x += x
        CPO.screen_pan_y += y


    @staticmethod
    def is_key_down(key):
        return CPO.window.keystat[key]

    @staticmethod
    def draw_all(dt):
        CPO.window.clear()

        # Pan the camera to the player
        glTranslatef(CPO.screen_pan_x, 0, 0)
        glTranslatef(0, CPO.screen_pan_y, 0)

        # Draw most of our in-game stuff
        CPO.node_manager.draw_nodes()

        # Move the camera back
        glTranslatef(-CPO.screen_pan_x, 0, 0)
        glTranslatef(0, -CPO.screen_pan_y, 0)


      # # Draw the menus because they don't care about panning
        CPO.node_manager.draw_menus()




    @staticmethod
    @window.event # because of weird frame limiting rules this is how 
    def on_draw(): # we call draw it's intentionally even though it seems weird
        CPO.draw_all(None)


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
    def on_mouse_motion(x, y, dx, dy):
        CPO.nm.on_mouse_motion(x, y, dx, dy)
        CPO.mouse_x = x
        CPO.mouse_y = y

    @staticmethod
    @window.event
    def on_key_press(k, mod):
        CPO.nm.on_key_press(k, mod)

    @staticmethod
    @window.event
    def on_key_release(k, mod):
        CPO.nm.on_key_release(k, mod)



    @staticmethod
    def on_update(self):
        # Because of stupid ass import reasons I should have dealt with earlier
        # this has to be done here, and not in nm.on_update() TODO: Built a wrapper for globals
        if CPO.is_client:
            CPO.client.request_sync()
        CPO.nm.on_update()



