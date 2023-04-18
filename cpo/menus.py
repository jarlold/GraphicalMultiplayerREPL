from cpo.menu_nodes import *
import pyglet
import time

CPO = None

def enter_edit_mode():
    print("--- Player Data ---")
    p = CPO.nm.get_player()
    print(p.get_position())
    print(p._items)

def print_cool_debug():
    print("--- DEBUG DATA ---")
    print(CPO.nm.nodes)


def kill_chat():
    global chat_menu
    CPO.nm.remove_node(chat_menu)
    chat_menu = None

def create_chat_menu():
    global chat_menu # wait it's a reference type nvm tho
    if not chat_menu is None:
        return
    chat_container = DraggableContainerMenu(
            x=-default_textures["CHATMENU"].width/2.0, 
            y=default_textures["CHATMENU"].height/2.0 - 30, 
            z=201, 
            width=default_textures["CHATMENU"].width - 50, 
            height=30
            )

    chat_close = StandardButton(
            default_textures["CHATMENU"].width/2.0  - default_textures["CLOSE"].width/2.0,
            default_textures["CHATMENU"].height/2.0 - default_textures["CLOSE"].height/2.0, 
            depressed="CLOSE", 
            pressed="CLOSE", 
            hover="HCLOSE",
            on_click=kill_chat
            )

    background = BackgroundSprite(0, 0, 0, texture="CHATMENU")
    chat_container.add_item(background)
    chat_container.add_item(chat_close)
    CPO.nm.add_nodes([chat_container, chat_close])
    chat_menu = chat_container
    return chat_container


def save_level():
    CPO.nm.save_level(str(time.time()))

class MenuManager:
    def __init__(self):
        self.sidebar_left = None
        self.sidebar_right = None
        self.chat_menu = None
        self.node_creator = None

        self.create_sidebar_left()
        self.create_sidebar_right()


    def create_sidebar_left(self):
        left_sidebar_items = [
                    HoveringButton(
                        -CPO.width/2.0 - 50, 
                        CPO.height/2.0 - 50, 
                        pressed=default_textures["PLUS"], 
                        max_hover_offset = -20, 
                        on_click=self.toggle_node_creator),
                    HoveringButton(-CPO.width/2.0 - 50, CPO.height/2.0 - 150, pressed=default_textures["MINUS"], max_hover_offset = -20),
                    HoveringButton(-CPO.width/2.0 - 50, CPO.height/2.0 - 250, pressed=default_textures["SAVE"], max_hover_offset = -20, on_click=save_level),
                ]

        left_sidebar = UnfoldingSidebar(-CPO.width/2.0, CPO.height/2.0 - 650, items=left_sidebar_items, width= 100, height = 3000, unfold_distance = -100)

        CPO.nm.add_node(left_sidebar)
        CPO.nm.add_nodes(left_sidebar_items)

    def create_sidebar_right(self):
        right_sidebar_items = [
                    HoveringButton(CPO.width/2.0 +50, CPO.height/2.0 - 150, pressed=default_textures["CHAT"], on_click=self.toggle_chat_menu),
                    HoveringButton(CPO.width/2.0 +50, CPO.height/2.0 - 250, pressed=default_textures["WIFI"]),
                    HoveringButton(CPO.width/2.0 +50, CPO.height/2.0 - 350, pressed=default_textures["TERMINAL"], on_click=print_cool_debug),
                    HoveringButton(CPO.width/2.0 +50, CPO.height/2.0 - 450, pressed=default_textures["SETTINGS"], on_click=enter_edit_mode),
                ]
        right_sidebar = UnfoldingSidebar(CPO.width/2.0 - 100, CPO.height/2.0 - 650, items=right_sidebar_items, width=10000, height=3000)

        CPO.nm.add_nodes([ right_sidebar, HoveringButton(CPO.width/2.0 -50, CPO.height/2.0 - 50)])
        CPO.nm.add_nodes(right_sidebar_items)

    def toggle_node_creator(self):
        if self.node_creator is None:
            self.node_creator = NodeCreationMenu(close_function=self.toggle_node_creator)
            CPO.nm.add_nodes(self.node_creator)
            CPO.nm.add_node(self.node_creator)
        else:
            CPO.nm.remove_nodes(self.node_creator)
            CPO.nm.remove_node(self.node_creator)
            del(self.node_creator)
            self.node_creator = None

    def toggle_chat_menu(self):
        if self.chat_menu is None:
            self.chat_menu= ChatMenu(close_function=self.toggle_chat_menu)
            CPO.nm.add_nodes(self.chat_menu)
            CPO.nm.add_node(self.chat_menu)
        else:
            CPO.nm.remove_nodes(self.chat_menu)
            CPO.nm.remove_node(self.chat_menu)
            del(self.chat_menu)
            self.chat_menu = None
