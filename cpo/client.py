import socket
import threading
import time

CPO = None

class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.buffsize = 512
        self.reply_threads = []
        self.heartbeat_thread = None
        self.conn = None
        self.alive = False

        self.should_send_heartbeat = True
        self.heartbeat_last_sent = 0
        self.heartbeat_last_recv = 0 
        self.heartbeat_every = 10

        self.node_packet_queue = []

        self.last_sync = 0
        self.sync_every = 30

    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.ip, self.port))
        self.alive = True
        self.request_sync()
        self.receive_packets()

    def receive_packets(self):
        while self.alive:
            output = self.conn.recv(self.buffsize)
            packet = str(output, encoding='utf8')
            self.packet_reply(packet.strip())

    def send_heartbeat(self):
        self.conn.sendall(bytes("heartbeat", encoding='utf8'))

    def request_sync(self):
        if time.time() - self.last_sync >= self.sync_every:
            self.conn.sendall(bytes("sync", encoding='utf8'))
            self.last_sync = time.time()
        else:
            self.conn.sendall(bytes("delta", encoding='utf8'))

    def packet_reply(self, packet):
        if packet.startswith("NODE|"):
            #print("Received node packet: " + packet)
            CPO.nm.node_packet_queue.append(packet)
            return

        if packet.startswith("REMOVE"):
            node_id = int(packet.replace("REMOVE ", '').strip())
            print("Trying to remove {} which {}".format(
                node_id,
                CPO.nm.remove_node_by_id(node_id)
            ))



if __name__ == "__main__":
    port = int(input("Enter port: "))
    print(port)
    c = Client("127.0.0.1", port)
    c.connect()
