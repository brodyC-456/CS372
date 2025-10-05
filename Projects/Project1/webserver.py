import socket
import sys

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) > 1: s.bind(('', int(sys.argv[1])))
else: s.bind(('', 28333))

s.listen()

while True:
    new_conn = s.accept()
    new_socket = new_conn[0]
    string = " "
    while "\r\n\r\n" not in string:
        d = new_socket.recv(4096)
        string = d.decode()
        print(string)
    new_socket.sendall("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 6\r\nConnection: close\r\n\r\nHello!".encode())
    new_socket.close()
