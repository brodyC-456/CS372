import socket

s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("localhost", 6790))

s.listen()

while True:
    client_socket,clientadr = s.accept() 
    print(clientadr)
    client_socket.sendall("I like french fries\n".encode())
    client_socket.close()