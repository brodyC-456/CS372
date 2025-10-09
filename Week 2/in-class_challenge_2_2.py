inputs = [([192,168,17,2], [255,0,0,0]), ([192,168,17,2], [255,255,0,0]), ([192,168,17,2], [255,255,255,0]), ([192,168,17,2], [255,192,0,0]), ([192,168,17,2], [255,255,248,0])]

def findNetworkAndHost(ipSubnet):
    ip = ipSubnet[0]
    subnet = ipSubnet[1]
    network_num = []
    host_num = []
    for i in range(len(ip)):
        network_num.append(ip[i] & subnet[i])
        inverse = ~subnet[i] & 0xff
        host_num.append(ip[i] & inverse)
    return (network_num, host_num)

for i in inputs:
    print(findNetworkAndHost(i))