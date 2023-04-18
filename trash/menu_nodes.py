import pyglet
from default_resources import default_textures
from node_types import SpriteNode, HitboxNode, BaseNode


CPO = None

class MenuNode:
    def __init__(self):
        self.is_menu = True


class StandardButton(SpriteNode, MenuNode):
    def __init__(self, x, y, z=0, pressed=None, depressed=None, hover=None):
        if pressed is None:
            self.pressed = default_textures["MENU"]
        else:
            self.pressed = pressed

        if depressed is None:
            self.depressed = default_textures["MENU"]
        else:
            self.depressed = self.pressed

        if hover is None:
            self.hover = default_textures["SAKURA"]

        MenuNode.__init__(self)
        SpriteNode.__init__(self, texture=self.depressed, x=x, y=y, z=z)
        
        self.hitbox_y_offset = -self.pressed.height/2.0 + 1
        self.hitbox_x_offset = -self.pressed.width/2.0 + 1

        self.hitbox = HitboxNode(
                width = self.pressed.width - 2,
                height = self.pressed.height - 2,
                x = x + self.hitbox_x_offset,
                y = y + self.hitbox_y_offset)

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

    def on_mouse_release(self, x, y, button, mod):
        self.sprite.image = self.depressed

    def on_mouse_motion(self, x, y, dx, dy):
        if self.get_hitbox().check_point_col(x, y):
            self.sprite.image = self.hover
        else:
            self.sprite.image = self.depressed

class HoveringButton(SpriteNode, MenuNode):
    def __init__(self, x, y, z=0, pressed=None, depressed=None, hover_sideways=False, on_click=None):
        self.hover_sideways = hover_sideways

        self.on_click = on_click
        
        self.pressed = pressed
        if self.pressed is None:
            self.pressed = default_textures["MENU"]

        self.depressed = depressed
        if depressed is None:
            self.depressed = self.pressed
        
        self.is_hovering = False
        self.max_hover_offset = 20
        self.hover_offset = 0

        MenuNode.__init__(self)
        SpriteNode.__init__(self, texture=self.depressed, x=x, y=y, z=z)
        
        self.hitbox_y_offset = -self.pressed.height/2.0 + 1
        self.hitbox_x_offset = -self.pressed.width/2.0 + 1

        self.hitbox = HitboxNode(
                width = self.pressed.width + self.max_hover_offset ,
                height = self.pressed.height,
                x = x + self.hitbox_x_offset,
                y = y + self.hitbox_y_offset)

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
        if self.is_hovering and self.hover_offset < self.max_hover_offset:
            self.hover_offset += 2
            if self.hover_sideways:
                self.add_position(-2, 0, 0)
            else:
                self.add_position(0, 2, 0)

        elif self.hover_offset == self.max_hover_offset and self.is_hovering:
            pass

        elif self.hover_offset > 0:
            self.hover_offset -= 2
            if self.hover_sideways:
                self.add_position(2, 0, 0)
            else:
                self.add_position(0, -2, 0)
    
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


        MenuNode.__init__(self)
        self.hitbox = HitboxNode(
                width = self.width,
                height = self.height,
                x = x,
                y = y)

    # Overrides
    def get_hitbox(self):
        return self.hitbox

    
    def on_update(self):
        s = 5 if self.max_unfold_offset > 0 else -5
        if not self.is_hidden and abs(self._unfold_offset) > 0:
            self._unfold_offset -= s
            for item in self.items:
                item.add_position(-s, 0, 0)
        elif self.is_hidden and self._unfold_offset < self.max_unfold_offset:
            self._unfold_offset += s
            for item in self.items:
                item.add_position(s, 0, 0)


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


class Draggable(MenuNode, SpriteNode):
    def __init__(self, x=0, y=0, z=0, texture=None):
        SpriteNode.__init__(self, x=x, y=y, z=z, texture=texture)


        self.hitbox_x_offset = -self.sprite.image.width/2.0
        self.hitbox_y_offset = -self.sprite.image.height/2.0
        self.hitbox = HitboxNode(
                width = self.sprite.image.width,
                height = self.sprite.image.height,
                x = x + self.hitbox_x_offset,
                y = y + self.hitbox_y_offset)
        
        self.being_dragged = False

    def get_hitbox(self):
        return self.hitbox

    def set_position(self, x, y, z):
        self.sprite.x, self.sprite.y, self.z = x, y, z
        self.hitbox.set_position(x + self.hitbox_x_offset, y + self.hitbox_y_offset, z)


    def on_mouse_press(self, x, y, button, mod):
        if self.get_hitbox().check_point_col(x, y):
            self.being_dragged = True

    def on_mouse_release(self, x, y, button, mod):
        self.being_dragged = False

    def on_mouse_drag(self, x, y, dx, dy, button, mod):
        if self.being_dragged:
            self.add_position(dx, dy, 0)

    # Overrides
    def draw(self):
        self.sprite.draw()
        self.hitbox.draw()






