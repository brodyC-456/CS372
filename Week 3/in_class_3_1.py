def encode_data(message, value):
    encoded_message = message.encode("utf-8")
    encoded_value = value.to_bytes(4, "big")
    total_len = (len(encoded_message) + len(encoded_value)).to_bytes(2, "big")
    byte = (total_len + encoded_message + encoded_value)
    return byte


def decode_data(data):
    value = int.from_bytes(data[-4:], "big")
    msg = data[2:-4].decode("utf-8")
    return (msg, value)



print(encode_data("the", 63900))
data = encode_data("Hello", 63900)
print(decode_data(data))