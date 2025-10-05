import socket
import sys

s = socket.socket()
if len(sys.argv) > 1:
    domain = sys.argv[1]
    s.connect((domain, int(sys.argv[2])))
else:
    print("Domain or Host not provided.")

s.sendall(("GET / HTTP/1.1\r\nHost: " + domain + "\r\nConnection: close\r\n\r\n").encode())

d = " "

while len(d) != 0:
    d = s.recv(4096)
    string = d.decode()
    print(string)

s.close()


