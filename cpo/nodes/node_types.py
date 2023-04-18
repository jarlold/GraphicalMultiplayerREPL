import pyglet
from cpo.default_resources import default_textures, default_font, default_player_animations
from pyglet.gl import *
import pyglet.shapes



NODE_PACKET_FORMAT = "NODE|{}|{},{},{}|{}|{}|DONE"
                    #      id | x y z | type | type data


class BaseNode:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z
        self.node_id = CPO.nm.get_new_node_id()

    def get_position(self):
        return self.x, self.y, self.z

    def set_position(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def add_position(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z

    def get_z_draw_level(self):
        return self.get_position()[2] - (0.1 * self.get_position()[1]) 

    # Overrides
    def as_packet(self):
        node_id = self.node_id
        x, y, z = self.get_position()
        t = NODE_TYPES[BaseNode]
        texture_name = "NA"

        return NODE_PACKET_FORMAT.format(
                node_id, x,y,z, t, texture_name
        )


class ContainerNode(BaseNode):
    def __init__(self, x=0, y=0, z=0, items=None):
        BaseNode.__init__(self, x, y, z)
        self._items = items
        if self._items is None:
            self._items = []
        self._items.sort(key = lambda x: x.get_z_draw_level())

    # Overrides
    def add_position(self, x, y, z):
        BaseNode.add_position(self, x, y, z)
        for i in self._items:
            i.add_position(x, y, z)

    def add_item(self, item):
        self._items.append(item)
        self._items.sort(key = lambda x: x.get_z_draw_level())

    def __getitem__(self, index):
        return self._items[index]

    def prepare_for_serialization(self):
        for i in self._items:
            if hasattr(i, "prepare_for_serialization"):
                i.prepare_for_serialization()

    def deserialize(self):
        for i in self._items:
            if hasattr(i, "deserialize"):
                i.deserialize()

    # Overrides
    def set_position(self, x, y, z):
        dx, dy, dz = x - self.x, y - self.y, z - self.z
        self.add_position(dx, dy, z)

    # Overrides
    def as_packet(self):
        return [i.as_packet() for i in self._items]

    # Overrides
    def draw(self):
        for item in self._items:
            if hasattr(item, "draw"): item.draw()


class SpriteNode(BaseNode):
    def __init__(self, texture=None, x=0, y=0, z=0):
        # Because of how supers work, leave this here instead of putting it
        # in the function signature
        if texture is None:
            texture = "DEFAULT_NODE"

        if isinstance(texture, str):
            self.texture_name = texture
            self.texture = default_textures[self.texture_name]
        else:
            self.texture = texture

            # TODO: this is inefficient, it doesn't happen often though
            for k in default_textures:
                if default_textures[k] == texture:
                    self.texture_name = k
                    break


        BaseNode.__init__(self, x=x, y=y, z=z)
        self.sprite = pyglet.sprite.Sprite(
                img=self.texture,
                x=x,
                y=y
                )

        self.z = z


    def deserialize(self):
        if hasattr(self, "texture") and hasattr(self, "sprite"):
            return
            
        self.texture = default_textures[self.texture_name]
        self.sprite = pyglet.sprite.Sprite(
                img=self.texture,
                x=self.x,
                y=self.y
                )

    def prepare_for_serialization(self):
        self.x, self.y = self.sprite.x, self.sprite.y
        del(self.sprite)
        del(self.texture)

    def set_texture(self, texture):
       self.sprite.image = default_textures[texture]
       self.texture_name = texture

    def get_texture_name(self):
        return self.texture_name

    def get_texture(self):
        return self.sprite.image

    # Overrides
    def get_position(self):
        return self.sprite.x, self.sprite.y, self.z

    # Overrides
    def set_position(self, x, y, z):
        self.sprite.x, self.sprite.y, self.z = x, y, z
        self.x, self.y = self.sprite.x, self.sprite.y

    def add_position(self, x, y, z):
        xyz = [ a + b for a,b in zip(self.get_position(), (x,y,z)) ]
        self.set_position(
                *xyz
                )
    
    def draw(self):
        self.sprite.draw()

    # Overrides
    def as_packet(self):
        node_id = self.node_id
        x, y, z = self.get_position()
        t = NODE_TYPES[SpriteNode]
        texture_name = self.get_texture_name()

        return NODE_PACKET_FORMAT.format(
                node_id, x,y,z, t, texture_name
        )


class TextNode(BaseNode):
    def __init__(self, text, x=0, y=0, z=0, font=None):
        # Instead of doing this in the function signature we'll do it here
        # to avoid having to import stuff
        if font is None:
            font = default_font
        BaseNode.__init__(self, x=x, y=y, z=z)
        self.label = pyglet.text.Label(text, font_name=font)

        self.label.x = x
        self.label.y = y
        self.z = z

    def prepare_for_serialization(self):
        self.text = self.label.text
        self.font = self.label.font_name
        self.x, self.y = self.label.x, self.label.y
        del(self.label)

    def deserialize(self):
        self.label = pyglet.text.Label(self.text, font_name=self.font)
    
    # Overrides
    def get_position(self):
        return self.label.x, self.label.y, self.z

    # Overrides
    def set_position(self, x, y, z):
        self.label.x, self.label.y, self.z = x, y, z

    def get_text(self):
        return self.label.text

    def set_text(self, text):
        self.label.text = text

    def draw(self):
        self.label.draw()

    # Overrides
    def as_packet(self):
        node_id = self.node_id
        x, y, z = self.get_position()
        t = NODE_TYPES[TextNode]
        text = self.get_text()

        return NODE_PACKET_FORMAT.format(
                node_id, x,y,z, t, text.replace("|","")
        )


class HitboxNode(BaseNode):
    def __init__(self, width=1, height=1, x=0, y=0, z=0):
        is_menu = True
        BaseNode.__init__(self, x=x, y=y, z=z)
        self.width, self.height, = width, height

        self.render_shape = pyglet.shapes.Rectangle(x, y, width, height, color=(255, 22, 20))
        self.render_shape.opacity = 125
        self.hitshape_visible = True

    def set_position(self, x, y, z):
        self.x, self.y, self.z = x, y, z
        self.render_shape.x, self.render_shape.y = x, y

    def add_position(self, x, y, z):
        # Very efficient super cool (sarcasm)
        xyz = [ a + b for a,b in zip(self.get_position(), (x, y, z)) ]
        self.set_position(*xyz)

    def prepare_for_serialization(self):
        self.render_shape = None

    def deserialize(self):
        self.render_shape = pyglet.shapes.Rectangle(self.x, self.y, self.width, self.height, color=(255, 22, 20))
        self.render_shape.opacity = 125

    def check_point_col(self, x, y):
        nx = x - CPO.window.width/2.0
        ny = y - CPO.window.height/2.0
        return nx <= self.x + self.width and nx >= self.x and ny <= self.y + self.height and ny >= self.y

    def check_hitnode_col(self, other):
        return self.x < other.x + other.width and \
            self.x + self.width > other.x and \
            self.y < other.y + other.height and \
            self.height + self.y > other.y and \
            self.z == other.z

    def get_hitbox(self):
        return self

    # Overrides
    def draw(self):
        if not self.hitshape_visible: return
        self.render_shape.width = self.width
        self.render_shape.height = self.height
        self.render_shape.draw()

    # Overrides
    def as_packet(self):
        node_id = self.node_id
        x, y, z = self.get_position()
        t = NODE_TYPES[HitboxNode]
        widthheight = "{},{}".format(self.width, self.height)

        return NODE_PACKET_FORMAT.format(
                node_id, x,y,z, t, widthheight
        )

class HitboxHaver:
    def __init__(self, x, y, z, width, height):
        self.hitbox = HitboxNode(
                width = width,
                height = height,
                x = x ,
                y = y,
                z = z
                )

    def check_point_col(self, x, y):
        return self.hitnode.check_point_col(x, y)

    def check_hitnode_col(self, other):
        return self.hitbox.check_hitnode_col(other)

    def get_hitbox(self):
        return self.hitbox


class WallNode(ContainerNode, HitboxHaver):
    def __init__(self, x=0, y=0, z=0, hit_width=None, hit_height=None, texture_name=None):
        self.sprite = SpriteNode( texture=texture_name, x=x, y=y, z=z)
        
        hit_width = self.sprite.get_texture().width if hit_width is None else hit_width
        hit_height = self.sprite.get_texture().height if hit_height is None else hit_height
        hitbox_x_offset = -self.sprite.get_texture().width/2.0
        hitbox_y_offset = -self.sprite.get_texture().height/2.0

        HitboxHaver.__init__(self, x + hitbox_x_offset, y+hitbox_y_offset, z, hit_width, hit_height)
        ContainerNode.__init__(self, x=x, y=y, z=z, items= [self.sprite, self.hitbox])

class PlayerNode(ContainerNode, HitboxHaver):
    def __init__(self, texture_dictionary=None, x=0, y=0, z=0, walk_speed=2, run_speed=4):
        
        # Just gotta store these bad boys
        self.walk_speed, self.run_speed = walk_speed, run_speed

        # If no textures provided, we'll just use the default ones
        if texture_dictionary is None:
            texture_dictionary = default_player_animations

        # If we're provided just one image, we'll map every action to it, so that
        # we still have a dictionary
        if isinstance(texture_dictionary, str):
            self.texture_dictionary = {
                    "WALK_UP": texture_dictionary,
                    "WALK_DOWN": texture_dictionary,
                    "WALK_LEFT": texture_dictionary,
                    "WALK_RIGHT": texture_dictionary,
                    "IDLE": texture_dictionary
                    }
        else:
            self.texture_dictionary = texture_dictionary

        # By default, we'll start out idling- and use this as the basis for our hitboxs'
        # shape
        self.texture_name = self.texture_dictionary["IDLE"]

        # Gonna be typing this out a lot lol
        idle_img = default_textures[self.texture_dictionary["IDLE"]]
        
        hitbox_y_offset = -idle_img.height/2.0 + 5
        hitbox_x_offset = -idle_img.width/2.0 + 7.5
        HitboxHaver.__init__(
                self,
                width = idle_img.width - 15,
                height = idle_img.height/3.0 ,
                x = x + hitbox_x_offset,
                y = y + hitbox_y_offset,
                z = z
                )

        self.sprite = SpriteNode(texture=idle_img, x=x, y=y, z=z)
        ContainerNode.__init__(self, x, y, z, items=[self.hitbox, self.sprite])



    def set_animation(self, animation_name):
        self.sprite.set_texture(self.texture_dictionary[animation_name])

    def add_position(self, x, y, z):
        old_pos = self.get_position()
        ContainerNode.add_position(self, x, y, z)
        
        # If that position is taken up by another hitbox, go home and cry.
        for o in CPO.nm.hitboxes:
            if o is self or (hasattr(o, "is_menu") and o.is_menu): continue
            if o.get_hitbox().check_hitnode_col(self.get_hitbox()):
                self.set_position(*old_pos)
                return False

        # Otherwise go home and give it to mom so she can hang it on the fridge
        return True

    def on_key_press(self, k, mod):
        if k == CPO.game_controls['UP']:
            self.set_animation("UP")

        if k == CPO.game_controls['LEFT']:
            self.set_animation("LEFT")

        if k == CPO.game_controls['DOWN']:
            self.set_animation("DOWN")

        if k == CPO.game_controls['RIGHT']:
            self.set_animation("RIGHT")
    
    def on_key_release(self, k, mod):
        self.set_animation("IDLE")
        if CPO.is_key_down(CPO.game_controls['UP']):
            self.set_animation("UP")

        if CPO.is_key_down(CPO.game_controls['LEFT']):
            self.set_animation("LEFT")

        if CPO.is_key_down(CPO.game_controls['DOWN']):
            self.set_animation("DOWN")

        if CPO.is_key_down(CPO.game_controls['RIGHT']):
            self.set_animation("RIGHT")

    def on_update(self):
        if CPO.is_key_down(CPO.game_controls["UP"]):
            if self.add_position(0, self.walk_speed, 0):
                CPO.pan_camera(0, -self.walk_speed)

        if CPO.is_key_down(CPO.game_controls["DOWN"]):
            if self.add_position(0, -self.walk_speed, 0):
                CPO.pan_camera(0, self.walk_speed)

        if CPO.is_key_down(CPO.game_controls["LEFT"]):
            if self.add_position(-self.walk_speed, 0, 0):
                CPO.pan_camera(self.walk_speed, 0)

        if CPO.is_key_down(CPO.game_controls["RIGHT"]):
            if self.add_position(self.walk_speed, 0, 0):
                CPO.pan_camera(-self.walk_speed, 0)

    def as_packet(self):
        return SpriteNode.as_packet(self)


# Used to turn the nodes into packets
NODE_TYPES = {
        BaseNode   : 0,
        SpriteNode : 1,
        TextNode   : 2,
        HitboxNode : 3
        }
