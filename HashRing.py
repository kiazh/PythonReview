import hashlib
from bisect import bisect_left, insort

def hash_value(text):
    return int(hashlib.md5(text.encode()).hexdigest(), 16) % (2**32)

class ChatLoadBalancer:

#initialises our ring
    def __init__(self, replicas=3):
        self.ring = []
        self.position_server = {}
        self.replicas = replicas
    def add_server(self, server_id):
        for i in range(self.replicas):
            vnode = f"{server_id}:{i}"
            position = hash_value(vnode)
            insort(self.ring, position)
            self.position_server[position] = server_id
    def remove_server(self, server_id):
        for i in range(self.replicas):
            vnode = f"{server_id}:{i}"
            position = hash_value(vnode)
            if position in self.position_server:
                del self.position_server[position]
                self.ring.remove(position)
    def get_server(self, chat_id):
        if not self.ring:
            return None

        chat_pos = hash_value(chat_id)
        idx = bisect_left(self.ring, chat_pos)

        if idx == len(self.ring):
            idx = 0

        server_pos = self.ring[idx]
        return self.position_server[server_pos]


lb = ChatLoadBalancer(replicas=5)
lb.add_server("A")
lb.add_server("B")
lb.add_server("C")

print(lb.get_server("chat1"))
print(lb.get_server("chat2"))
print(lb.get_server("chat3"))