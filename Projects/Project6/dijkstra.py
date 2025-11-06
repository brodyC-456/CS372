import sys
import json
import math  # If you want to use math.inf for infinity

"""
    -------
    HELPERS
    -------
"""
# Network Functions from last project
def ipv4_to_value(ipv4_addr):

    ip_nums = ipv4_addr.split('.')
    for i in range(len(ip_nums)):
        ip_nums[i] = int(ip_nums[i])
    
    value = (ip_nums[0] << 24) | (ip_nums[1] << 16) | (ip_nums[2] << 8) | ip_nums[3]
    return value


def value_to_ipv4(addr):

    ip_nums = []
    ip_nums.append((addr >> 24) & 0xff)
    ip_nums.append((addr >> 16) & 0xff)
    ip_nums.append((addr >> 8) & 0xff)
    ip_nums.append((addr) & 0xff)
    return f"{ip_nums[0]}.{ip_nums[1]}.{ip_nums[2]}.{ip_nums[3]}"

def get_subnet_mask_value(slash):

    # Extract the number from slash to figure out how many "1's" (network bits) we need 
    slash = slash.split("/")
    network_bit_val = int(slash[1])
    # The rest of the bits in our subnet mask should be 0 (host bits)
    host_bit_val = 32 - network_bit_val

    # Creates a binary number with 1's as the network bits and 0's as the host bits
    binary_val = bin(((1 << network_bit_val) - 1) << host_bit_val) 
    return int(binary_val, 2)

def get_network(ip_value, netmask):
    # Bitwise & gives us the network value
    return ip_value & netmask 

def ips_same_subnet(ip1, ip2, slash):
    val_ip_1 = ipv4_to_value(ip1)
    val_ip_2 = ipv4_to_value(ip2)

    subnet_val = get_subnet_mask_value(slash)

    # if the two ip's have the same network number, then return true
    return get_network(val_ip_1, subnet_val) == get_network(val_ip_2, subnet_val)

def find_router_for_ip(routers, ip):
    for key, value in routers.items():
        if ips_same_subnet(key, ip, value["netmask"]):
            return key
    return None

# Other Helpers

def get_smallest_node_dist(dist, v):
    shortest = math.inf
    smallest_route = ""
    for router in v:
        if dist[router] < shortest:
            shortest = dist[router]
            smallest_route = router
    return smallest_route

def construct_path(parent, src, dest):
    path = []
    target = dest
    if parent[target] != None or target == src:
        # Starting at the target IP then adding its parents until there are none left
        while target != None:
            path.append(target)
            target = parent[target]
        # Since the list is built in reverse, we need to re-reverse it
    path.reverse()
    return path

            

def dijkstras_shortest_path(routers, src_ip, dest_ip):
    """
    This function takes a dictionary representing the network, a source
    IP, and a destination IP, and returns a list with all the routers
    along the shortest path.

    The source and destination IPs are **not** included in this path.

    Note that the source IP and destination IP will probably not be
    routers! They will be on the same subnet as the router. You'll have
    to search the routers to find the one on the same subnet as the
    source IP. Same for the destination IP. [Hint: make use of your
    find_router_for_ip() function from the last project!]

    The dictionary keys are router IPs, and the values are dictionaries
    with a bunch of information, including the routers that are directly
    connected to the key.

    This partial example shows that router `10.31.98.1` is connected to
    three other routers: `10.34.166.1`, `10.34.194.1`, and `10.34.46.1`:

    {
        "10.34.98.1": {
            "connections": {
                "10.34.166.1": {
                    "netmask": "/24",
                    "interface": "en0",
                    "ad": 70
                },
                "10.34.194.1": {
                    "netmask": "/24",
                    "interface": "en1",
                    "ad": 93
                },
                "10.34.46.1": {
                    "netmask": "/24",
                    "interface": "en2",
                    "ad": 64
                }
            },
            "netmask": "/24",
            "if_count": 3,
            "if_prefix": "en"
        },
        ...

    The "ad" (Administrative Distance) field is the edge weight for that
    connection.

    **Strong recommendation**: make functions to do subtasks within this
    function. Having it all built as a single wall of code is a recipe
    for madness.
    """

    # if the source and dest ips are on the same subnet, then no routing is necessary
    if ips_same_subnet(src_ip, dest_ip, "/24"):
        return []
    
    # Need to turn the source and destination IP's into the routers on the same subnet
    src_router = find_router_for_ip(routers, src_ip)
    dest_router = find_router_for_ip(routers, dest_ip)

    # --- Initializing Variables ---
    to_visit = set()
    dist = {}
    parent = {}

    for router in routers:
        dist[router] = math.inf
        parent[router] = None
        to_visit.add(router)
    dist[src_router] = 0

    # --- Main Loop ---

    while len(to_visit) != 0:
        # sets curr to the ip of the router with the lowest distance value, then removes it from the set
        curr = get_smallest_node_dist(dist, to_visit)
        to_visit.remove(curr)

        # If we reach our destination, construct and return our path
        if curr == dest_router:
            return construct_path(parent, src_router, dest_router)
        
        for neighbor, value in routers[curr]["connections"].items():
            alt = dist[curr] + value["ad"]
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                parent[neighbor] = curr
        
    raise Exception("Shortest Path Failed")


#------------------------------
# DO NOT MODIFY BELOW THIS LINE
#------------------------------
def read_routers(file_name):
    with open(file_name) as fp:
        data = fp.read()

    return json.loads(data)

def find_routes(routers, src_dest_pairs):
    for src_ip, dest_ip in src_dest_pairs:
        path = dijkstras_shortest_path(routers, src_ip, dest_ip)
        print(f"{src_ip:>15s} -> {dest_ip:<15s}  {repr(path)}")

def usage():
    print("usage: dijkstra.py infile.json", file=sys.stderr)

def main(argv):
    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    routes = json_data["src-dest"]

    find_routes(routers, routes)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
