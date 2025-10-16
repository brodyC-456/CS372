import sys
import socket

# How many bytes is the word length?
WORD_LEN_SIZE = 2

def usage():
    print("usage: wordclient.py server port", file=sys.stderr)

packet_buffer = b''

def get_next_word_packet(s):
    """
    Return the next word packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """

    global packet_buffer
    recv_amount = 64
    # Recieve data until we have, at the very least, the first two bytes (length)
    while len(packet_buffer) < 2:
        packet_buffer += s.recv(recv_amount)
        # Returns None when we are done recieving data
        if len(packet_buffer) == 0:
            return None
    
    word_length = int.from_bytes(packet_buffer[:2], "big")
    # If our packet is incomplete, recieve more data
    while len(packet_buffer[2:]) < word_length:
        packet_buffer += s.recv(recv_amount)

    # Slice the packet off of packet_buffer and returns the complete packet
    data = packet_buffer[:word_length + 2]
    packet_buffer = packet_buffer[word_length + 2:]
    return data



def extract_word(word_packet):
    """
    Extract a word from a word packet.

    word_packet: a word packet consisting of the encoded word length
    followed by the UTF-8 word.

    Returns the word decoded as a string.
    """

    return word_packet[2:].decode("utf-8")

# Do not modify:

def main(argv):
    try:
        host = argv[1]
        port = int(argv[2])
    except:
        usage()
        return 1

    s = socket.socket()
    s.connect((host, port))

    print("Getting words:")

    while True:
        word_packet = get_next_word_packet(s)

        if word_packet is None:
            break

        word = extract_word(word_packet)

        print(f"    {word}")

    s.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))