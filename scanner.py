import ipaddress
import subprocess
import socket
import json
from concurrent.futures import ThreadPoolExecutor
from scapy.all import ARP, Ether,srp

results = []

COMMON_PORTS = [
    21,
    22,
    53,
    80,
    135,
    139,
    443,
    445,
    3389
]
SERVICES = {
    21: "FTP",
    22: "SSH",
    53: "DNS",
    80: "HTTP",
    135: "RPC",
    139: "NetBIOS",
    443: "HTTPS",
    445: "SMB",
    3389: "RDP"
}

subnet = input("Enter Subnet: ")
network = ipaddress.ip_network(subnet)

# network = ipaddress.ip_network("192.168.1.0/24")

def get_hostname(ip):
    try:
        hostname = socket.gethostbyaddr(str(ip))[0]
    
        if hostname == str(ip):
            return "Unknown"
        
        return hostname
    
    except:
        return "Unknown"

def ping_host(ip):
    result = subprocess.run(
        ["ping","-n","1","-w","100",str(ip)],
        capture_output=True,
        text=True
    )

    return result.returncode == 0

def scan_port(ip,port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    sock.settimeout(0.2)

    result = sock.connect_ex((str(ip),port))

    sock.close()

    return result == 0

def scan_host(host):

    if not ping_host(host):
        return
    
    hostname = get_hostname(host)

    host_data = {
        "ip" : str(host),
        "hostname" : hostname,
        "open_ports" : [],
        "mac" : get_mac(host)
    }

    for port in COMMON_PORTS:
        if scan_port(host,port):
            host_data["open_ports"].append({
                "port" : port,
                "service" : SERVICES[port]
            })

    
    return host_data
                
def get_mac(ip):
    arp = ARP(pdst=str(ip))

    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    packet = ether / arp

    result = srp(
        packet,
        timeout = 1,
        verbose = False
    )[0]

    if result:
        return result[0][1].hwsrc

    return "Unknown"

with ThreadPoolExecutor(max_workers=50) as executor:

    results = list(
        filter(
            None,
            executor.map(scan_host,network.hosts())
        )
    )
    
for host in results:

    print(f"\n{host['ip']} - {host['hostname']}")

    for port in host["open_ports"]:

        print(
            f"  Port {port['port']} OPEN {port['service']}"
        )
        print (
            f"  MAC : {host["mac"]}"
        )

with open("scan_results.json","w") as file:
    json.dump(results,file,indent=4)

alive_hosts = len(results)

print(f"\nFound {alive_hosts} live hosts")

print("\nResults Saved to scan_results.json")

# print(results)
# print(f"\n Found {alive_hosts} live hosts")
# result = subprocess.run(
#     ["ping","-n","1","-w","100","192.168.1.1"],
#     capture_output = True,
#     text = True
# )
# print(result.returncode)
# if ping_host("192.168.1.1"):
#     hostname=get_hostname("192.168.1.1")
#     print("Host is alive")
#     print(get_hostname("192.168.1.1"))
