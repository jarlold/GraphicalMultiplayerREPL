import pickle
import node_serializer

class NodeManager:
    def __init__(self):
        self.nodes = [] # ALL nodes
        self.remote_nodes = [] # nodes sent by the server that are synced by the server
        self.hitboxes = [] # Contains the nodes with hitboxes, let's us check for collisions faster
        self.node_count = 0
        self.node_ids = []

        # Event subscriptions, a dictionary would be suitable here in future
        self.menu_draw_subs = []
        self.draw_subs = []
        self.mouse_press_subs = []
        self.mouse_release_subs = []
        self.mouse_drag_subs = []
        self.mouse_motion_subs = []
        self.key_press_subs = []
        self.key_release_subs = []
        self.update_subs = []

        self.window_event_lists = \
            [ self.draw_subs, self.mouse_press_subs, self.mouse_release_subs, self.mouse_drag_subs, self.key_press_subs, self.update_subs, self.menu_draw_subs, self.key_release_subs,
                    self.mouse_motion_subs]

        # Because of weird threading rules with pyglet we 
        # don't want to create a Sprite object or Label object in the networking thread
        # even if it's to add it to a list here. So we store the packets then parese them
        # into nodes from the pyglet thread.
        self.node_packet_queue = []

    def z_order_drawables(self):
        k = lambda x: x.get_position()[2] - (0.1 * x.get_position()[1])
        self.draw_subs.sort(key=k, reverse=False)

    def update_remote_nodes(self):
        while len(self.node_packet_queue) > 0:
            packet = self.node_packet_queue.pop()
            node = node_serializer.packets_to_nodes(packet)
            self.update_remote_node(node)


    def update_remote_node(self, node):
        for i, n in enumerate(self.nodes):
            if n.node_id == node.node_id:
                self.nodes[i].__dict__ = node.__dict__
                return
        self.add_node(node)

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def add_node(self, node):
        self.nodes.append(node)
        self.node_ids.append(node.node_id)

        # We could use decorators for this, but it wouldn't be much cleaner to have a ton of functions like this instead 
        # so if statements it is lol
        if hasattr(node, "draw") and (not hasattr(node, "is_menu") or not node.is_menu) :
            self.draw_subs.append(node)

        if hasattr(node, "draw") and hasattr(node, "is_menu") and node.is_menu:
            self.menu_draw_subs.append(node)

        if hasattr(node, "on_mouse_press"):
            self.mouse_press_subs.append(node)

        if hasattr(node, "on_mouse_release"):
            self.mouse_release_subs.append(node)

        if hasattr(node, "on_mouse_drag"):
            self.mouse_drag_subs.append(node)

        if hasattr(node, "on_mouse_motion"):
            self.mouse_motion_subs.append(node)

        if hasattr(node, "on_key_press"):
            self.key_press_subs.append(node)

        if hasattr(node, "on_key_release"):
            self.key_release_subs.append(node)

        if hasattr(node, "on_update"):
            self.update_subs.append(node)

        if hasattr(node, "get_hitbox"):
            self.hitboxes.append(node)


    def unsub_node_from(self, node, sublist):
        try:
            sublist.remove(node)
            return True
        except ValueError:
            return False

    def remove_node(self, node):
        t = False

        try:
            self.nodes.remove(node)
            t = True
            for sublist in self.window_event_lists:
                self.unsub_node_from(node, sublist)
        except ValueError:
            pass

        try:
            self.hitboxes.remove(node)
            t = True
        except ValueError:
            pass

        return t

    def draw_nodes(self):
        self.z_order_drawables()
        for node in self.draw_subs:
            node.draw()

    def draw_menus(self):
        for menu in self.menu_draw_subs:
            menu.draw()

    def get_new_node_id(self):
        self.node_count += 1
        return self.node_count
            
    def on_mouse_press(self, x, y, button, mod):
        for node in self.mouse_press_subs:
            node.on_mouse_press(x, y, button, mod)

    def on_mouse_release(self, x,y,button,mod):
        for node in self.mouse_release_subs:
            node.on_mouse_release(x, y, button, mod)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for node in self.mouse_drag_subs:
            node.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        for node in self.mouse_motion_subs:
            node.on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, k, mod):
        for node in self.key_press_subs:
            node.on_key_press(k, mod)

    def on_key_release(self, k , mod):
        for node in self.key_release_subs:
            node.on_key_release(k, mod)

    def on_update(self):
        for node in self.update_subs:
            node.on_update()

        self.update_remote_nodes()

    def save_level(self, level_path):
        with open(level_path, "rb"):
            pickle.dump(self)
            return True
        return False

    def get_all_nodes_as_packets(self):
        packets = []
        for node in self.nodes:
            if hasattr(node, "as_packet"):
                p = node.as_packet()
                if isinstance(p, list):
                    packets += p
                else:
                    packets.append(node.as_packet())
        return packets



