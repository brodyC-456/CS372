import socket

# create a socket
s = socket.socket()

# connect the socket to a server
server = ('localhost', 6790)
s.connect(server)

data = s.recv(100)
str = data.decode(errors="ignore")
print(str)

