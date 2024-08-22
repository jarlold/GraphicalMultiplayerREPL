import socket
import threading

CPO = None

class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.verbose = True
        self.connections = []
        self.buffsize = 512

        self.connection_threads = []
        self.max_player_count = 5

    def vprint(self, msg):
        if self.verbose:
            print(msg)

    def serve(self):
        print("Serving on " + str(self.port))
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)

        self.await_connection()
    
    def await_connection(self):
        while True and len(self.connection_threads) < self.max_player_count:
            conn, address = self.server_socket.accept()
            self.vprint("New connection from " + str(address))
            self.connections.append((conn, address))
            
            t = threading.Thread(target=self.receive_packet, args=[conn])
            t.start()

    def receive_packet(self, conn):
        while True:
            output = conn.recv(self.buffsize)
            packet = str(output, encoding='utf8')

            if packet.startswith("heartbeat"):
                self.return_heartbeat(conn)

            if packet.startswith("sync"):
                self.send_all_nodes(conn)

            if packet.startswith("delta"):
                self.send_changed_nodes(conn)

    def send_all_nodes(self, conn):
        node_packets = CPO.nm.get_all_nodes_as_packets()
        for np in node_packets:
            self.send_node_packet(conn, np)

    def send_changed_nodes(self, conn):
        node_packets = CPO.nm.get_changed_nodes_as_packets()
        for np in node_packets:
            self.send_node_packet(conn, np)

    def send_packet(self, conn, p):
        if len(p) <= self.buffsize:
            conn.sendall( bytes(p + " "*(self.buffsize - len(p)), encoding='utf8') )

        else:
            print("trying to send packet: " + p + "but it's too long!")

    def send_node_packet(self, conn, np):
        if not isinstance(np, str):
            print(np)
            print(type(np))

        self.send_packet(conn, np)

    def return_heartbeat(self, conn):
        print("Sending..")
        conn.sendall(bytes("beatheart", encoding='utf8'))
        print("sent!")

