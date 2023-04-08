class NodeManager:
    def __init__(self):
        self.nodes = []
        self.node_ids = []
        self.node_count = 0

        # Event subscriptions, a dictionary would be suitable here in future
        self.menu_draw_subs = []
        self.draw_subs = []
        self.mouse_press_subs = []
        self.mouse_release_subs = []
        self.mouse_drag_subs = []
        self.key_press_subs = []
        self.update_subs = []

        self.window_event_lists = \
            [ self.draw_subs, self.mouse_press_subs, self.mouse_release_subs, self.mouse_drag_subs, self.key_press_subs, self.update_subs, self.menu_draw_subs]

    def add_node(self, node):
        self.nodes.append(node)
        self.node_ids.append(node.node_id)

        # We could use decorators for this, but it wouldn't be much cleaner to have a ton of functions like this instead 
        # so if statements it is lol
        if hasattr(node, "draw"):
            if hasattr(node, "is_menu") and node.is_menu:
                self.menu_draw_subs.append(node)
            else:
                self.draw_subs.append(node)

        if hasattr(node, "on_mouse_press"):
            self.mouse_press_subs.append(node)

        if hasattr(node, "on_mouse_release"):
            self.mouse_release_subs.append(node)

        if hasattr(node, "on_mouse_drag"):
            self.mouse_drag_subs.append(node)

        if hasattr(node, "on_key_press"):
            self.key_press_subs.append(node)

        if hasattr(node, "on_update"):
            self.update_subs.append(node)

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
            return False

    def draw_nodes(self):
        for node in self.draw_subs:
            node.draw()

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

    def on_key_press(self, k, mod):
        for node in self.key_press_subs:
            node.on_key_press(k, mod)

    def on_update(self):
        for node in self.update_subs:
            node.on_update()


