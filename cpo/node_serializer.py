from cpo.default_resources import default_textures
from cpo.node_types import *


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
        b = TextNode(x=x, y=y, z=z, text=type_data)

    elif node_type == NODE_TYPES[HitboxNode]:
        width, height = type_data.split(",")
        width, height = float(width), float(height)
        b = HitboxNode(x=x, y=y, z=z, width=width, height=height)

    b.node_id = node_id

    return b

