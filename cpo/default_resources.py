import pyglet
from pyglet.gl import *

### Texture stuff ###

ani_bin = pyglet.image.atlas.TextureBin()

# Prep a player animation
def process_ani(path, general_scale=4) :
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
        "SAKURA": load_image('7.png'),
        "WIFI": load_image("menus/icons/IconBoxNetworking.png"),
        "CHAT": load_image("menus/icons/ChatBox.png"),
        "MENU": load_image("menus/icons/MenuBox.png"),
        "SETTINGS": load_image("menus/icons/IconBoxSettings.png"),
        "TERMINAL": load_image("menus/icons/TerminalBox.png"),
        "EDIT": load_image("menus/icons/EditBox.png"),
        "PLUS": load_image("menus/icons/PlusBox.png"),
        "MINUS": load_image("menus/icons/MinusBox.png"),
        "SAVE": load_image("menus/icons/FloppyDiskBox.png"),
        "CHATMENU": load_image("menus/ChatWindow.png"),
        "NODEMENU": load_image("menus/NodeCreator.png"),
        "MINIMIZE": load_image("menus/icons/MinimizeButton.png"),
        "CLOSE": load_image("menus/icons/XButton.png"),
        "HMINIMIZE": load_image("menus/icons/MinimizeButtonHighlighted.png"),
        "HCLOSE": load_image("menus/icons/XHighlightedButton.png"),
        "SMALLPLUS": load_image("menus/icons/SmallPlusButton.png"),
        "SMALLMINUS": load_image("menus/icons/SmallMinusButton.png"),
        "PLACENODE": load_image("menus/icons/PlaceNodeButton.png"),
        "NEXTSPRITE": load_image("menus/icons/NextSpriteButton.png"),
        "PREVSPRITE": load_image("menus/icons/PrevSpriteButton.png"),
        "ABIG_IDLE"  : load_image("abigail/0.png"),
        "ABIG_UP"    : load_ani("abigail/3.gif"),
        "ABIG_DOWN"  : load_ani("abigail/4.gif"),
        "ABIG_LEFT"  : load_ani("abigail/1.gif"),
        "ABIG_RIGHT" : load_ani("abigail/2.gif"),
        "ABIG_SIT"   : load_ani("abigail/6.gif"),
        "ABIG_LAUGH" : load_ani("abigail/5.gif"),
        "BED"   : load_image("svhouse/Bed.png"),
        "FLOOR" : load_image("svhouse/Floors.png"),
        "WALLS1" : load_image("svhouse/Room.png"),
        "WALLS2" : load_image("svhouse/Walls.png"),
        "FIREPLACE" : load_image("svhouse/Fireplace.png"),
        "BED" : load_image("svhouse/TV_Small.png"),
        "BOOKSHELF" : load_image("svhouse/Bookshelf_0.png"),
        "TRIM" : load_image("svhouse/Borders.png"),
        "XMASTREE" : load_image("svhouse/Xmas_Tree.png")

        }


default_player_animations = {
        "IDLE"  : "ABIG_IDLE" ,
        "UP"    : "ABIG_UP"   ,
        "DOWN"  : "ABIG_DOWN" ,
        "LEFT"  : "ABIG_LEFT" ,
        "RIGHT" : "ABIG_RIGHT",
        "SIT"   : "ABIG_SIT"  ,
        "LAUGH" : "ABIG_LAUGH"
        }


### Font stuff ###
def load_font(font_loc, fontname) :
    pyglet.font.add_file(font_loc)
    return pyglet.font.load(fontname)

VT323 = load_font("resources/fonts/vt323.ttf", "VT323")
default_font = "VT323"

