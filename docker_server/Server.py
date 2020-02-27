import socketserver
import json
import os
import time
import threading

# Read and write dictionary to a local file.
def read_data(path):
    with open(path) as file:
        return json.load(file)

def write_data(path, map):
    with open(path, 'w') as file:
        json.dump(map, file)

# Process the request based on its operation. 
def operation(data, data_path, server):
    if data[0] == 'put':
        #lock = threading.RLock()
        #with lock:
        if os.path.isfile(data_path):
            map = read_data(data_path)
        else:
            map = {}
        map[data[1]] = data[2]
        write_data(data_path, map)
        msg = data[1].encode('utf-8')
        return msg
        # request.sendall(data[1].encode('utf-8'))
    elif data[0] == 'get':
        try:
            map = read_data(data_path)
            msg = map[data[1]].encode('utf-8')
            return msg
            # request.sendall(map[data[1]].encode('utf-8'))
        except KeyError:
            msg = 'Can\'t find the key {}'.format(data[1]).encode('utf-8')
            return msg
    elif data[0] == 'del':
        try:
            map = read_data(data_path)
            result = map.pop(data[1])
            write_data(data_path, map)
            msg = 'delete value {}'.format(result).encode('utf-8')
            return msg
        except KeyError:
            msg = 'Can\'t find the key {}'.format(data[1]).encode('utf-8')
            return msg
        # request.sendall(msg.encode('utf-8'))
    elif data[0] == 'store':
        map = read_data(data_path)
        msg = json.dumps(map).encode('utf-8')
        if len(msg) >=65000:
            msg = b'TRIMMED: '+msg[0:65000]
        return msg
        # request.sendall(msg)
    elif data[0] == 'exit':
        # request.sendall('server shutdown'.encode('utf-8'))
        os.remove(data_path)
        # os.mkdir('/stop')
        server.conti = False
        msg = 'server shutdown'.encode('utf-8')
        return msg

# Handler classes for TCP and UDP
class MyTCPHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.data_path = './temp.json'
        socketserver.BaseRequestHandler.__init__(
            self, request, client_address, server)
        return

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)

        data = self.data.decode("utf-8")
        data = data.split(' ')
        msg = operation(data, self.data_path, self.server)
        self.request.sendall(msg)
        if msg.decode('utf-8') == 'server shutdown':
            os.system('kill %d'%os.getpid())


class MyUDPHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.data_path = './temp.json'
        socketserver.BaseRequestHandler.__init__(
            self, request, client_address, server)
        return

    def handle(self):
        # self.request is the TCP socket connected to the client
        data = self.request[0].strip()
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))
        print(data)

        data = data.decode("utf-8")
        data = data.split(' ')
        msg= operation(data, self.data_path, self.server)
        socket.sendto(msg, self.client_address)
        if msg.decode('utf-8') == 'server shutdown':
            os.system('kill %d'%os.getpid())
        
# Helper class for TCP and UDP server
class MyTcpServer(socketserver.ThreadingTCPServer):
    conti = True
    def __init__(self, server_addr, Handler):
        socketserver.TCPServer.__init__(self, server_addr, Handler)

class MyUdpServer(socketserver.ThreadingUDPServer):
    conti = True
    def __init__(self, server_addr, Handler):
        socketserver.UDPServer.__init__(self, server_addr, Handler)

if __name__ == "__main__":
    import sys
    # Help information
    if len(sys.argv[1:]) <= 0:
        print('us/ts <port> UDP/TCP/TCP-and-UDP SERVER: run server on <port>.\ntus <tcpport>\
         <udpport> TCP-and-UDP SERVER: run servers on <tcpport> and <udpport> \
             sharing same key-value store.')
        sys.exit()
    HOST, PORT = "", int(sys.argv[2])
    protocol = sys.argv[1]
    print(protocol, HOST, PORT)

    # Create the server, binding to 0.0.0.0 on designed port
    
    if protocol == 'tc':
        server = MyTcpServer((HOST, PORT), MyTCPHandler)
        print('tcp server created ....')
    else:
        server = MyUdpServer((HOST, PORT), MyUDPHandler)
        print('udp server created ....')
    '''
    if protocol == 'tc':
        server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
        print('tcp server created ....')
    else:
        server = socketserver.ThreadingUDPServer((HOST, PORT), MyUDPHandler)
        print('udp server created ....')
    '''
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
    '''
    while server.conti:
        server.handle_request()
    '''       