import pyglet
from cpo.default_resources import default_textures
from cpo.node_types import *
import glooey

CPO = None


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
        elif type(pressed) == str:
            self.pressed= default_textures[pressed]
        else:
            self.pressed = pressed

        if depressed is None:
            self.depressed = default_textures["MENU"]
        elif type(depressed) == str:
            self.depressed = default_textures[depressed]
        else:
            self.depressed = self.pressed

        if hover is None:
            self.hover = self.pressed
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
    def __init__(self, x=0, y=0, z=0, width=1, height=1, texture=None, on_release=None):
        self.being_dragged = False
        ContainerNode.__init__(self, x, y, z)
        HitboxHaver.__init__(self, x, y, z, width, height)
        self.add_item(self.hitbox)
        self.on_release = on_release

    def on_mouse_press(self, x, y, button, mod):
        if hasattr(self, "is_menu") and self.is_menu:
            if self.get_hitbox().check_point_col(x, y):
                self.being_dragged = True

        else:
            if self.get_hitbox().check_point_col(x - CPO.screen_pan_x, y - CPO.screen_pan_y):
                self.being_dragged = True

    def on_mouse_release(self, x, y, button, mod):
        self.being_dragged = False
        if not self.on_release is None:
            self.on_release()

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
    def __init__(self, text, x=0, y=0, z=0, font=None, size=12, color=(255, 255, 255, 255)):
        TextNode.__init__(self, text, x=x, y=y, z=z, font=font, size=size, color=color)
        MenuNode.__init__(self)


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
                on_click=close_function
                )

        self.next_texture_btn = StandardButton(
                54 * 4,
                15 * -4,
                z=202,
                depressed="NEXTSPRITE", 
                pressed="NEXTSPRITE", 
                on_click=self.next_texture
                )

        self.prev_texture_btn = StandardButton(
                4 * 15,
                15 * -4,
                z=202,
                depressed="PREVSPRITE", 
                pressed="PREVSPRITE", 
                on_click=self.prev_texture
                )

        self.place_sprite_btn = StandardButton(
                35 * 4,
                15 * -4,
                z=202,
                depressed="PLACENODE", 
                pressed="PLACENODE", 
                on_click=self.place_sprite
                )

        self.sprite_z_up_btn = StandardButton(
                -default_textures["NODEMENU"].width/2.0 + 200,
                default_textures["NODEMENU"].height/2.0 - 46 * 4,
                z=202,
                depressed="SMALLPLUS", 
                pressed="SMALLPLUS", 
                on_click = self.raise_sprite_z
                )

        self.sprite_z_down_btn = StandardButton(
                -default_textures["NODEMENU"].width/2.0 + 8 * 4 + default_textures["SMALLMINUS"].width/2.0 - 1,
                default_textures["NODEMENU"].height/2.0 - 46 * 4,
                z=202,
                depressed="SMALLMINUS", 
                pressed="SMALLMINUS", 
                on_click = self.lower_sprite_z
                )

        self.z_label = TextItem(
                x=-default_textures["NODEMENU"].width/2.0 + 75,
                y=default_textures["NODEMENU"].height/2.0 - 50 * 4 + 6 ,
                z=202,
                text="Z: 1",
                color=(0, 0, 0, 255),
                size=24
                )


        self.background = BackgroundSprite(0, 0, 0, texture="NODEMENU")
        self.texture_index = 0
        self.preview_sprite = SpriteNode(texture="ABIG_LAUGH",
                x=-default_textures["NODEMENU"].width/2.0 + 100*4, 
                y=default_textures["NODEMENU"].height/2.0 - 30*4, 
                z=205
                )
        self.preview_sprite.is_menu = True
        self.hitbox.is_menu = True

        self.add_item(self.background)
        self.add_item(self.creator_close)
        self.add_item(self.preview_sprite)
        self.add_item(self.next_texture_btn)
        self.add_item(self.prev_texture_btn)
        self.add_item(self.place_sprite_btn)
        self.add_item(self.sprite_z_down_btn)
        self.add_item(self.sprite_z_up_btn)
        self.add_item(self.z_label)

        self.place_sprite_z = 1
        self.preview_height = 100
        self.preview_width = 100
        self.set_preview_scale("ABIG_LAUGH")

    def raise_sprite_z(self):
        self.place_sprite_z += 1
        self.z_label.set_text("Z: " + str(self.place_sprite_z))

    def lower_sprite_z(self):
        self.place_sprite_z -= 1
        self.z_label.set_text("Z: " + str(self.place_sprite_z))

    def next_texture(self):
        self.texture_index += 1
        self.texture_index = self.texture_index % len(default_textures)
        texture_name = list(default_textures.keys())[self.texture_index]
        self.preview_sprite.set_texture(
                texture_name
                )
        self.set_preview_scale(texture_name)

    def prev_texture(self):
        self.texture_index -= 1
        self.texture_index = self.texture_index % len(default_textures)
        texture_name = list(default_textures.keys())[self.texture_index]
        self.preview_sprite.set_texture(
                texture_name
                )
        self.set_preview_scale(texture_name)


    def set_preview_scale(self, texture_name):
        texture = default_textures[texture_name]

        if texture.width*CPO.general_scale*self.preview_sprite.get_scale() != self.preview_width:
            self.preview_sprite.set_scale(
                    self.preview_width / texture.width
                    )

        if texture.height*CPO.general_scale*self.preview_sprite.get_scale() > self.preview_height:
            self.preview_sprite.set_scale(
                    self.preview_height / texture.height
                    )

    def place_sprite(self):
        s = SpriteNode(
                texture=self.preview_sprite.get_texture(), 
                x=CPO.mouse_x - CPO.width/2.0 - CPO.screen_pan_x, 
                y=CPO.mouse_y - CPO.height/2.0 - CPO.screen_pan_y, 
                z=self.place_sprite_z
            )
        d =  DraggableContainer()
        d.add_item(s)
        kill = lambda : CPO.nm.remove_node(d)
        d.being_dragged = True
        d.on_release=kill
        CPO.nm.add_nodes(d)
        CPO.nm.add_node(d)


class ChatMenu(DraggableContainer):
    def __init__(self, close_function=None):
        DraggableContainerMenu.__init__(self,
                x=-default_textures["CHATMENU"].width/2.0, 
                y=default_textures["CHATMENU"].height/2.0 - 30, 
                z=201, 
                width=default_textures["CHATMENU"].width - 50, 
                height=30
                )

        self.creator_close = StandardButton(
                default_textures["CHATMENU"].width/2.0  - default_textures["CLOSE"].width/2.0,
                default_textures["CHATMENU"].height/2.0 - default_textures["CLOSE"].height/2.0, 
                z=202,
                depressed="CLOSE", 
                pressed="CLOSE", 
                hover="HCLOSE",
                on_click=close_function
                )

        self.background = BackgroundSprite(0, 0, 0, texture="CHATMENU")
        self.add_item(self.background)
        self.add_item(self.creator_close)
