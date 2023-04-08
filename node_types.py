import pyglet
from default_resources import default_textures, default_font
from pyglet.gl import *


# Used to store the main game object
CPO = None

class BaseNode:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z
        self.node_id = CPO.nm.get_new_node_id()
        CPO.nm.add_node(self)

    def get_position(self):
        return self.x, self.y, self.z

    def set_position(self, x, y, z):
        self.x, self.y, self.z = x, y, z

class SpriteNode(BaseNode):
    def __init__(self, texture=default_textures["DEFAULT_NODE"], x=0, y=0, z=0):
        BaseNode.__init__(self, x=x, y=y, z=z)
        self.sprite = pyglet.sprite.Sprite(
                img=texture,
                x=x,
                y=y
                )

        self.z = z

    # Overrides
    def get_position(self):
        return self.sprite.x, self.sprite.y, self.z

    # Overrides
    def set_position(self, x, y, z):
        self.sprite.x, self.sprite.y, self.z = x, y, z
    
    def draw(self):
        self.sprite.draw()

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


class HitboxNode(BaseNode):
    def __init__(self, width=1, height=1, x=0, y=0, z=0, layer=0):
        BaseNode.__init__(self, x=x, y=y, z=z)
        self.width, self.height, self.layer = width, height, layer

    def check_point_col(self, x, y):
        pass

    def check_hitnode_col(self, other):
        return (self.x < other.x + other.w and \
            self.x + other.w > other.x and \
            self.y < other.y + other.h and \
            self.h + self.y > other.y and 
            other.layer == this.layer)

    def check_box_collision(self, x, y, width, height):
        pass


class PlayerNode(SpriteNode, HitboxNode):
    def __init__(self, texture_dictionary=None, x=0, y=0, z=0, walk_speed=1, run_speed=2):

        # If no textures provided, we'll just use the default node 
        if texture_dictionary is None:
            texture_dictionary = default_textures["WALK_CYCLE"]

        # If we're provided a static image, we'll map every action to it, so that
        # we still have a dictionary
        if type(texture_dictionary) == pyglet.image.TextureRegion or type(texture_dictionary) == pyglet.image.animation.Animation:
            self.texture_dictionary = {
                    "WALK_UP": texture_dictionary,
                    "WALK_DOWN": texture_dictionary,
                    "WALK_LEFT": texture_dictionary,
                    "WALK_RIGHT": texture_dictionary,
                    "IDLE": texture_dictionary
                    }
        else:
            self.texture_dictionary = texture_dictionary

        SpriteNode.__init__(self, 
                texture=self.texture_dictionary["IDLE"], 
                x=x, y=y, z=z)

        self.texture_dictionary = texture_dictionary
        self.walk_speed, self.run_speed = walk_speed, run_speed

    def on_update(self):
        if CPO.is_key_down(CPO.game_controls["UP"]):
            self.sprite.y += self.walk_speed
            glTranslatef(0, -self.walk_speed, 0)

        if CPO.is_key_down(CPO.game_controls["DOWN"]):
            self.sprite.y -= self.walk_speed
            glTranslatef(0, self.walk_speed, 0)

        if CPO.is_key_down(CPO.game_controls["LEFT"]):
            self.sprite.x -= self.walk_speed
            glTranslatef(self.walk_speed, 0, 0)

        if CPO.is_key_down(CPO.game_controls["RIGHT"]):
            self.sprite.x += self.walk_speed
            glTranslatef(-self.walk_speed, 0, 0)


