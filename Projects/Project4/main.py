NUM_OF_PACKETS = 10

"""Converts an IP address to a bytestring"""
def convert_to_bytes(ip):
    byte = b''
    nums = ip.split('.')
    for num in nums:
        b = int(num).to_bytes(1, "big")
        byte += b
    return byte

"""Creates a psuedo IP header which will be appended to our tcp data"""
def build_pseudo_ip(source, dest, length):
    bytestring = b''
    bytestring += (source + dest + b'\x00' + b'\x06' + length)
    return bytestring

"""Computes the checksum for our 0-chechsum tcp data"""
def compute_checksum(pseudo, tcp_data):
    # Add the pseudo header to our tcp data
    data = pseudo + tcp_data

    offset = 0
    total = 0

    # Partially Copied from "Beej's Guide to Network Concepts", chapter 16
    while offset < len(data):
    # Slice 2 bytes out and get their value:
        word = int.from_bytes(data[offset:offset + 2], "big")
        total += word
        total = (total & 0xffff) + (total >> 16)  # carry around
        offset += 2
    return (~total) & 0xffff

"""Returns true if our computed checksum is equal to the existing checksum in the tcp data"""
def validate_tcp_packet(ip_file, tcp_data_file):
    # Opens and stores the contents of the IP address file and TCP data file
    with open(ip_file, "r") as file:
        ip_data = file.read()
    with open(tcp_data_file, "rb") as file:
        tcp_data = file.read()
        tcp_length = len(tcp_data)

    # Gives us a list with the source IP and Destination IP
    ip_data = ip_data.split()

    # Converting our header data to bytes
    source_bytes = convert_to_bytes(ip_data[0])
    dest_bytes = convert_to_bytes(ip_data[1])
    tcp_length = tcp_length.to_bytes(2, "big")

    pseudo_ip = build_pseudo_ip(source_bytes, dest_bytes, tcp_length)

    # Save the existing checksum from our tcp data and create a 0-checksum copy of the data
    existing_checksum = int.from_bytes(tcp_data[16:18], "big")
    tcp_zero_cksum = tcp_data[:16] + b'\x00\x00' + tcp_data[18:]

    # Forces the length of our zero-checksum packet to be even (needed for compute_checksum to work)
    if len(tcp_zero_cksum) % 2 == 1:
        tcp_zero_cksum += b'\x00'

    if compute_checksum(pseudo_ip, tcp_zero_cksum) == existing_checksum:
        return "PASS"
    else:
        return "FAIL"
    
# Testing
for i in range(NUM_OF_PACKETS):
    print(validate_tcp_packet("tcp_addrs_" + str(i) + ".txt", "tcp_data_" + str(i) + ".dat"))




