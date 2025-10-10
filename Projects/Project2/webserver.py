import socket
import sys
import os

# Returns the file path in the first line of the request sent by the client using split()
def parse_request(req):
    req = req.split("\r\n")
    get = req[0].split(' ')
    path = get[1]
    return path

# Returns the name of the file from the url path
def strip_path(full_path):
    full_path = os.path.split(full_path)
    file_name = full_path[-1]
    return file_name

# Gets the file extension and maps it to a MIME type
def get_MIME_type(file):
    ext = os.path.splitext(file)[-1]
    if ext == ".txt":
        return "text/plain"
    if ext == ".html":
        return "text/html"

# Opens and reads the content of a file, and returns false if the file isnt found
def read_file(file):
    try:
        with open(file, "rb") as fp:
            data = fp.read()   # Read entire file
            return data.decode("ISO-8859-1")
    except:
        return False


s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Lets us choose a port number for the server (with CMD line)
if len(sys.argv) > 1: s.bind(('', int(sys.argv[1])))
else: s.bind(('', 28333))
s.listen()


while True:
    new_conn = s.accept()
    new_socket = new_conn[0]
    request = ""
    # Gives us the full request
    while "\r\n\r\n" not in request:
        d = new_socket.recv(4096)
        request += d.decode("ISO-8859-1")
    path = parse_request(request)
    file_name = strip_path(path)
    mime_type = get_MIME_type(file_name)
    content = read_file(file_name)
    # If the file isn't found, throw a 404 error
    if content == False:
        new_socket.sendall("HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 13\r\nConnection: close\r\n\r\n404 not found".encode("ISO-8859-1"))
        new_socket.close()
    content_length = len(content)
    new_socket.sendall(("HTTP/1.1 200 OK\r\nContent-Type: " + mime_type + "\r\nContent-Length: " + str(content_length) + "\r\nConnection: close\r\n\r\n" + content).encode("ISO-8859-1"))
    new_socket.close()


