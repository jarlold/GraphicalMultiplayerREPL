from .menu_nodes import *
import pyglet
import time

CPO = None

chat_menu = None

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

def create_sidebars():
    right_sidebar_items = [
                HoveringButton(CPO.width/2.0 +50, CPO.height/2.0 - 150, pressed=default_textures["CHAT"], on_click=create_chat_menu),
                HoveringButton(CPO.width/2.0 +50, CPO.height/2.0 - 250, pressed=default_textures["WIFI"]),
                HoveringButton(CPO.width/2.0 +50, CPO.height/2.0 - 350, pressed=default_textures["TERMINAL"], on_click=print_cool_debug),
                HoveringButton(CPO.width/2.0 +50, CPO.height/2.0 - 450, pressed=default_textures["SETTINGS"], on_click=enter_edit_mode),
            ]

    left_sidebar_items = [
                HoveringButton(-CPO.width/2.0 - 50, CPO.height/2.0 - 50, pressed=default_textures["PLUS"], max_hover_offset = -20, on_click=StaticNodeCreationMenu.toggle),
                HoveringButton(-CPO.width/2.0 - 50, CPO.height/2.0 - 150, pressed=default_textures["MINUS"], max_hover_offset = -20),
                HoveringButton(-CPO.width/2.0 - 50, CPO.height/2.0 - 250, pressed=default_textures["SAVE"], max_hover_offset = -20, on_click=save_level),
            ]

    right_sidebar = UnfoldingSidebar(CPO.width/2.0 - 100, CPO.height/2.0 - 650, items=right_sidebar_items, width=10000, height=3000)
    left_sidebar = UnfoldingSidebar(-CPO.width/2.0, CPO.height/2.0 - 650, items=left_sidebar_items, width= 100, height = 3000, unfold_distance = -100)

    CPO.nm.add_nodes([
            right_sidebar,
            left_sidebar,
            HoveringButton(CPO.width/2.0 -50, CPO.height/2.0 - 50)
            ])

    CPO.nm.add_nodes(right_sidebar_items)
    CPO.nm.add_nodes(left_sidebar_items)


def setup_base_menus():
    
    create_sidebars()
        


