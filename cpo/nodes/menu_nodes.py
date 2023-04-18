import pyglet
from cpo.default_resources import default_textures
from .node_types import *
import glooey

from cpo.cpo import CPO

class MenuNode:
    def __init__(self):
        self.is_menu = True

class BackgroundSprite(SpriteNode, MenuNode):
    def __init__(self, x, y, z, texture=None):
        SpriteNode.__init__(self, x=x, y=y, z=z, texture=texture)
        MenuNode.__init__(self)
        self.visible = True

    def draw(self):
        if self.visible:
            SpriteNode.draw(self)

    def toggle_visible(self):
        self.visible = not self.visible

class StandardButton(SpriteNode, MenuNode):
    def __init__(self, x, y, z=0, pressed=None, depressed=None, hover=None, on_click=None):
        self.on_click = on_click
        if pressed is None:
            self.pressed = default_textures["MENU"]
        elif type(hover) == str:
            self.pressed= default_textures[pressed]
        else:
            self.pressed = pressed

        if depressed is None:
            self.depressed = default_textures["MENU"]
        elif type(hover) == str:
            self.depressed = default_textures[depressed]
        else:
            self.depressed = self.pressed

        if hover is None:
            self.hover = default_textures["SAKURA"]
        elif type(hover) == str:
            self.hover = default_textures[hover]
        else:
            self.hover = hover

        MenuNode.__init__(self)
        SpriteNode.__init__(self, texture=self.depressed, x=x, y=y, z=z)
        
        self.hitbox_y_offset = -self.pressed.height/2.0 + 1
        self.hitbox_x_offset = -self.pressed.width/2.0 + 1

        self.hitbox = HitboxNode(
                width = self.pressed.width - 2,
                height = self.pressed.height - 2,
                x = x + self.hitbox_x_offset,
                y = y + self.hitbox_y_offset,
                z=z)

    # Overrides
    def get_hitbox(self):
        return self.hitbox

    # Overrides
    def get_position(self):
        return self.sprite.x, self.sprite.y, self.z

    # Overrides
    def set_position(self, x, y, z):
        self.sprite.x, self.sprite.y, self.z = x, y, z
        self.hitbox.set_position(x + self.hitbox_x_offset, y + self.hitbox_y_offset, z)

    def draw(self):
        self.sprite.draw()
        self.hitbox.draw()
    
    def on_mouse_press(self, x, y, button, mod):
        if self.get_hitbox().check_point_col(x, y):
            self.sprite.image = self.pressed
            if not self.on_click is None:
                self.on_click()

    def on_mouse_release(self, x, y, button, mod):
        self.sprite.image = self.depressed

    def on_mouse_motion(self, x, y, dx, dy):
        if self.get_hitbox().check_point_col(x, y):
            self.sprite.image = self.hover
        else:
            self.sprite.image = self.depressed

class HoveringButton(SpriteNode, MenuNode):
    def __init__(self, x, y, z=0, pressed=None, depressed=None, on_click=None, max_hover_offset=20):
        self.on_click = on_click
        
        self.pressed = pressed
        if self.pressed is None:
            self.pressed = default_textures["MENU"]

        self.depressed = depressed
        if depressed is None:
            self.depressed = self.pressed
        
        self.is_hovering = False
        self.max_unfold_offset = max_hover_offset # don't tell anyone but i copy pasted this from UnfoldOffset instead 
        self._unfold_offset = 0                   # of using inheritence. It'll be our lil secret ok?

        MenuNode.__init__(self)
        SpriteNode.__init__(self, texture=self.depressed, x=x, y=y, z=z)
        
        self.hitbox_y_offset = -self.pressed.height/2.0 
        self.hitbox_x_offset = -self.pressed.width/2.0 + (self.max_unfold_offset if self.max_unfold_offset < 0 else 0)

        self.hitbox = HitboxNode(
                width = self.pressed.width + abs(self.max_unfold_offset) ,
                height = self.pressed.height,
                x = x + self.hitbox_x_offset,
                y = y + self.hitbox_y_offset,
                z=z)

    # Overrides
    def get_hitbox(self):
        return self.hitbox

    def set_position(self, x, y, z):
        self.sprite.x, self.sprite.y, self.z = x, y, z
        self.hitbox.set_position(x + self.hitbox_x_offset, y + self.hitbox_y_offset, z)

    def draw(self):
        self.sprite.draw()
        self.hitbox.draw()

    def on_update(self):
        s = 2 if self.max_unfold_offset < 0 else -2

        if self.is_hovering and abs(self._unfold_offset) < abs(self.max_unfold_offset):
            self._unfold_offset += s
            self.add_position(s, 0, 0)
        elif not self.is_hovering and abs(self._unfold_offset) > 0:
            self._unfold_offset -= s
            self.add_position(-s, 0, 0)

    
    def on_mouse_press(self, x, y, button, mod):
        if self.get_hitbox().check_point_col(x, y):
            self.sprite.image = self.pressed

            if not self.on_click is None:
                self.on_click()

    def on_mouse_release(self, x, y, button, mod):
        self.sprite.image = self.depressed

    def on_mouse_motion(self, x, y, dx, dy):
        if self.get_hitbox().check_point_col(x, y):
            self.is_hovering = True
        else:
            self.is_hovering = False

class UnfoldingSidebar(MenuNode, BaseNode):
    def __init__(self, x, y, z=0, items=None, width=1, height=1, unfold_distance=100):

        self.items = items
        if self.items == None:
            self.items = []

        BaseNode.__init__(self)
        

        self.width, self.height = width, height

        self._unfold_offset = unfold_distance
        self.max_unfold_offset = unfold_distance
        self.is_hidden = True

        self.unfold_speed = 5
        if self.max_unfold_offset % self.unfold_speed != 0:
            print("WARNING: Unfold speed is not a multiple of the offset, speed will be changed to 1")
            self.unfold_speed = 1


        MenuNode.__init__(self)
        self.hitbox = HitboxNode(
                width = self.width,
                height = self.height,
                x = x,
                y = y,
                z=z
                )

    # Overrides
    def get_hitbox(self):
        return self.hitbox

    
    def on_update(self):
        s = self.unfold_speed if self.max_unfold_offset > 0 else -self.unfold_speed

        if self.is_hidden and abs(self._unfold_offset) < abs(self.max_unfold_offset):
            self._unfold_offset += s
            for item in self.items:
                item.add_position(s, 0, 0)
        elif not self.is_hidden and abs(self._unfold_offset) > 0:
            self._unfold_offset -= s
            for item in self.items:
                item.add_position(-s, 0, 0)


    def on_mouse_motion(self, x, y, dx, dy):
        if self.get_hitbox().check_point_col(x, y):
            self.is_hidden = False
        else:
            self.is_hidden = True
        
    # Overrides
    def draw(self):
        for item in self.items:
            item.draw()

        self.hitbox.draw()

class DraggableContainer(ContainerNode, HitboxHaver):
    def __init__(self, x=0, y=0, z=0, width=1, height=1, texture=None):
        self.being_dragged = False
        ContainerNode.__init__(self, x, y, z)
        HitboxHaver.__init__(self, x, y, z, width, height)
        self.add_item(self.hitbox)

    def on_mouse_press(self, x, y, button, mod):
        if hasattr(self, "is_menu") and self.is_menu:
            if self.get_hitbox().check_point_col(x, y):
                self.being_dragged = True

        else:
            if self.get_hitbox().check_point_col(x - CPO.screen_pan_x, y - CPO.screen_pan_y):
                self.being_dragged = True

    def on_mouse_release(self, x, y, button, mod):
        self.being_dragged = False

    def on_mouse_drag(self, x, y, dx, dy, button, mod):
        if self.being_dragged:
            self.add_position(dx, dy, 0)

class DraggableContainerMenu(DraggableContainer, MenuNode):
    def __init__(self, x=0, y=0, z=0, width=1, height=1):
        DraggableContainer.__init__(self, x=x, y=y, z=z, width=width, height=height)
        MenuNode.__init__(self)

class DraggableSprite(DraggableContainer):
    def __init__(self, x=0, y=0, z=0, texture=None):
        self.sprite= SpriteNode(x=x, y=y, z=z, texture=texture)
        w, h = self.sprite.get_texture().height, self.sprite.get_texture().width
        DraggableContainer.__init__(self, x=x - w/2.0, y=y - h/2.0, z=z, width=w, height=h)
        self.add_item(self.sprite)

class TextItem(MenuNode, TextNode):
    def __init__(self, text, x=0, y=0, z=0, font=None):
        TextNode.__init__(self, text, x=x, y=y, z=z, font=font)
        MenuNode.__init__(self)

class TextPrompt(BaseNode, MenuNode):
    def __init__(self):
        self.x, self.y = CPO.width/2.0, CPO.height/2.0
        self.label = glooey.text.EditableTextLabel("Hello world!")
        BaseNode.__init__(self)
        MenuNode.__init__(self)

    def draw(self):
        self.label.do_draw()


class NodeCreationMenu(DraggableContainer):
    def __init__(self, close_function=None):
        DraggableContainerMenu.__init__(self,
                x=-default_textures["NODEMENU"].width/2.0, 
                y=default_textures["NODEMENU"].height/2.0 - 30, 
                z=201, 
                width=default_textures["NODEMENU"].width - 50, 
                height=30
                )

        self.creator_close = StandardButton(
                default_textures["NODEMENU"].width/2.0  - default_textures["CLOSE"].width/2.0,
                default_textures["NODEMENU"].height/2.0 - default_textures["CLOSE"].height/2.0, 
                z=202,
                depressed="CLOSE", 
                pressed="CLOSE", 
                hover="HCLOSE",
                on_click=self.kill_menu
                )

        self.background = BackgroundSprite(0, 0, 0, texture="NODEMENU")

        self.preview_sprite = SpriteNode(texture="ABIG_LAUGH",
                x=-default_textures["NODEMENU"].width/2.0 + 100*4, 
                y=default_textures["NODEMENU"].height/2.0 - 30*4, 
                z=205
                )

        self.add_item(self.background)
        self.add_item(self.creator_close)
        self.add_item(self.preview_sprite)

    def kill_menu(self):
        CPO.nm.remove_node(self)
        del(self)

        

class StaticNodeCreationMenu:
    container = DraggableContainerMenu(
                x=-default_textures["NODEMENU"].width/2.0, 
                y=default_textures["NODEMENU"].height/2.0 - 30, 
                z=201, 
                width=default_textures["NODEMENU"].width - 50, 
                height=30)

    self.creator_close = StandardButton(
            default_textures["NODEMENU"].width/2.0  - default_textures["CLOSE"].width/2.0,
            default_textures["NODEMENU"].height/2.0 - default_textures["CLOSE"].height/2.0, 
            z=202,
            depressed="CLOSE", 
            pressed="CLOSE", 
            hover="HCLOSE",
            on_click=StaticNodeCreationMenu.close()
            )

    self.background = BackgroundSprite(0, 0, 0, texture="NODEMENU")

    self.preview_sprite = SpriteNode(texture="ABIG_LAUGH",
            x=-default_textures["NODEMENU"].width/2.0 + 100*4, 
            y=default_textures["NODEMENU"].height/2.0 - 30*4, 
            z=205
            )

    is_open = True

    @staticmethod
    def open():
        StaticNodeCreationMenu.is_open = True
        CPO.nm.add_nodes(StaticNodeCreationMenu.container)
        CPO.nm.add_node(StaticNodeCreationMenu.container)

    @staticmethod
    def close():
        StaticNodeCreationMenu.is_open = False
        CPO.nm.remove_node(StaticNodeCreationMenu.container)

    @staticmethod
    def toggle():
        if StaticNodeCreationMenu.is_open:
            StaticNodeCreationMenu.close()
        else:
            StaticNodeCreationMenu.open()

