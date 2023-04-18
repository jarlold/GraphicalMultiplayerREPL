from node_types import *
from default_resources import default_textures


def packets_to_nodes(packet):
#   try:
    if isinstance(packet, list):
        return [packet_to_node(i) for i in packet]
    return packet_to_node(packet)


def packet_to_node(packet):
    p = packet.split("|")[1:-1]
    node_id = int(p[0]) 
    
    x, y, z = [float(i) for i in p[1].split(",")]
    node_type = int(p[2])
    type_data = str(p[3])

    if node_type == NODE_TYPES[BaseNode]:
        b = BaseNode(x=x, y=y, z=z)

    elif node_type == NODE_TYPES[SpriteNode]:
        b = SpriteNode(x=x, y=y, z=z, texture=type_data)

    elif node_type == NODE_TYPES[TextNode]:
        print(type_data)
        b = TextNode(x=x, y=y, z=z, text=type_data)

    elif node_type == NODE_TYPES[HitboxNode]:
        width, height = type_data.split(",")
        width, height = float(width), float(height)
        b = HitboxNode(x=x, y=y, z=z, width=width, height=height)


    b.node_id = node_id
    return b




class RemoteNode:
    def __init__(self, packet):
        p = packet.split("|")[1:-1]
        node_id = int(p[0]) 
        
        xyz = [float(i) for i in p[1].split(",")]
        node_type = int(p[2])
        type_data = str(p[3])

        if node_type == NODE_TYPES[BaseNode]:
            BaseNode.__init__(self)
            print("BASE NODE")

        elif node_type == NODE_TYPES[SpriteNode]:
            SpriteNode.__init__(self, texture=type_data)
            print("SPRITE NODE")

        elif node_type == NODE_TYPES[TextNode]:
            TextNode.__init__(self, text=type_data)

        elif node_type == NODE_TYPES[HitboxNode]:
            print("HIT NODE")
            width, height = type_data.split(",")
            width, height = float(width), float(height)
            HitboxNode.__init__(self, width=width, height=height)


        self.x, self.y, self.z = xyz
        self.type = node_type
        self.node_id = node_id

    
    def draw(self):
        self.sprite.image.blit(0, 0)
    
    def get_position(self):
        return self.x, self.y, self.z
    
    def set_position(self, x, y, z ):
        self.x, self.y, self.z = x, y, z

    def draw_texture(self):
        self.texture.blit(self.x, self.y)

    def draw_text(self):
        self.label.draw()





