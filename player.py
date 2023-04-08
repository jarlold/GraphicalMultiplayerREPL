from node_types import BaseNode, SpriteNode
from default_resources import default_textures

import pyglet
from pyglet.gl import *

CPO = None


class PlayerNode(SpriteNode):
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


