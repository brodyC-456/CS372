def ip_to_dec(ip):
    ip_nums = ip.split(".")
    byte_string = b''
    for num in ip_nums:
        byte_string += int(num).to_bytes()
    return int.from_bytes(byte_string)

def dec_to_ip(num):
    string = []
    string.append((num >> 24) & 0xff)
    string.append((num >> 16) & 0xff)
    string.append((num >> 8) & 0xff)
    string.append((num) & 0xff)
    return f"{string[0]}.{string[1]}.{string[2]}.{string[3]}"

print(ip_to_dec("192.168.1.2"))
print(ip_to_dec("10.20.30.40"))
print(ip_to_dec("127.0.0.1"))

print(dec_to_ip(3325256824))
print(dec_to_ip(3405803976))
print(dec_to_ip(3221225987))

