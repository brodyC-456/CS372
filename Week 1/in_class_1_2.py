import socket

# create a socket
s = socket.socket()

# connect the socket to a server
server = ('starwarstel.net', 23)
s.connect(server)

while True:
    data = s.recv(100)
    str = data.decode(errors="ignore")
    print(str)

