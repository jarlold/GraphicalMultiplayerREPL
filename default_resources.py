import pyglet
from pyglet.gl import *

### Texture stuff ###

ani_bin = pyglet.image.atlas.TextureBin()

# Prep a player animation
def process_ani(path, general_scale=3) :
    animation = pyglet.image.load_animation(path)
    animation.scale = general_scale
    animation.add_to_texture_bin(ani_bin)
    for i in animation.frames :
        animation.width = i.image.width * general_scale
        animation.height = i.image.height * general_scale
        i.image.width = i.image.width *general_scale
        i.image.height = i.image.height *general_scale
        i.image.anchor_x = i.image.width/2
        i.image.anchor_y = i.image.height/2
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    return animation

# Load an animation from a path
def load_ani(path) :
    return process_ani("resources/" + path)

# Scale and center images where needed
def process_image(image, general_scale=4) :
    image.width = image.width * general_scale
    image.height = image.height * general_scale
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

# Loads and image into a pyglet image object.
def load_image(image) :
    img = pyglet.resource.image("resources/"+image)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    process_image(img)
    return img


default_textures = {
        "DEFAULT_NODE": load_image('node.png'),
        "WALK_CYCLE": load_ani("5.gif")
        }


### Font stuff ###
def load_font(font_loc, fontname) :
    pyglet.font.add_file(font_loc)
    return pyglet.font.load(fontname)

VT323 = load_font("resources/fonts/vt323.ttf", "VT323")
default_font = "VT323"

