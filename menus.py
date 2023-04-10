from menu_nodes import *
import pyglet

CPO = None

def enter_edit_mode():
    print("Edit mode!")


def setup_base_menus():
    sidebar_items = [
                HoveringButton(CPO.width/2.0 +50, CPO.height/2.0 - 150, hover_sideways=True, pressed=default_textures["CHAT"]),
                HoveringButton(CPO.width/2.0 +50, CPO.height/2.0 - 250, hover_sideways=True, pressed=default_textures["WIFI"]),
                HoveringButton(CPO.width/2.0 +50, CPO.height/2.0 - 350, hover_sideways=True, pressed=default_textures["TERMINAL"]),
                HoveringButton(CPO.width/2.0 +50, CPO.height/2.0 - 450, hover_sideways=True, pressed=default_textures["SETTINGS"]),
            ]

    sidebar = UnfoldingSidebar(CPO.width/2.0 - 100, CPO.height/2.0 - 650, items=sidebar_items, width=10000, height=3000)
    CPO.nm.add_nodes([
            sidebar,
            HoveringButton(CPO.width/2.0 -50, CPO.height/2.0 - 50, hover_sideways=True),
            Draggable(x=-100, y=30)
            ])

    
    b = HoveringButton(-CPO.width/2.0 -25, CPO.height/2.0 - 450, hover_sideways=True, pressed=default_textures["SETTINGS"])
    
    sidebar2 = UnfoldingSidebar(-CPO.width/2.0, CPO.height/2.0 - 650, items=[b], unfold_distance=-500, width= 100, height = 400)

    CPO.nm.add_node(b)
    CPO.nm.add_node(sidebar2)

    CPO.nm.add_nodes(sidebar_items)
