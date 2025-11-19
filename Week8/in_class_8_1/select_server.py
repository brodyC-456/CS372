# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

def run_server(port):
    # TODO--fill this in
    listening_socket = socket.socket()
    listening_socket.bind(("localhost", port))
    listening_socket.listen()
    read_set = {listening_socket}

    while read_set:
        ready_to_read, _, _ = select.select(read_set, {}, {})

        for s in ready_to_read:
            if s == listening_socket:
                new_s, _ = s.accept()
                h, p = new_s.getpeername()
                print(f"{h}, {p}: connected")
                read_set.add(new_s)
            else:
                h, p = s.getpeername()
                data = s.recv(4096)
                data_len = len(data)
                if not data:
                    read_set.remove(s)
                    print(f"{h}, {p}: disconnected")
                print(f"({h}, {p}) {data_len} bytes: {data}")
                

            


#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
