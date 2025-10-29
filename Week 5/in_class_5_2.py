def get_subnet_mask(slash):
    # Extract the number from slash to figure out how many "1's" (network bits) we need 
    slash = slash.split("/")
    network_bit_val = int(slash[1])
    # The rest of the bits in our subnet mask should be 0 (host bits)
    host_bit_val = 32 - network_bit_val

    # Creates a binary number with 1's as the network bits and 0's as the host bits
    binary_val = bin(((1 << network_bit_val) - 1) << host_bit_val) 
    return int(binary_val, 2)

def ip_to_val(ipv4_addr):
    ip_nums = ipv4_addr.split('.')
    for i in range(len(ip_nums)):
        ip_nums[i] = int(ip_nums[i])
    value = (ip_nums[0] << 24) | (ip_nums[1] << 16) | (ip_nums[2] << 8) | ip_nums[3]
    return value

def val_to_ip(addr):
    ip_nums = []
    ip_nums.append((addr >> 24) & 0xff)
    ip_nums.append((addr >> 16) & 0xff)
    ip_nums.append((addr >> 8) & 0xff)
    ip_nums.append((addr) & 0xff)
    return f"{ip_nums[0]}.{ip_nums[1]}.{ip_nums[2]}.{ip_nums[3]}"

def get_network_val(sub, ip_val):
    val = sub & ip_val
    return val_to_ip(val)



print(get_network_val(get_subnet_mask("/19"), ip_to_val("120.20.19.7")))