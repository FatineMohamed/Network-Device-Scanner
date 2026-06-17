# Network Device Scanner

A multithreaded Python network scanner that performs host discovery, hostname resolution, TCP port scanning, MAC address identification, and JSON reporting.

## Features

* ICMP host discovery (Ping Sweep)
* Hostname resolution
* TCP port scanning
* Service identification
* MAC address discovery
* Multithreaded scanning using ThreadPoolExecutor
* JSON report generation
* User-defined subnet scanning

## Technologies Used

* Python 3
* socket
* subprocess
* ipaddress
* concurrent.futures
* scapy

## Supported Services

| Port | Service |
| ---- | ------- |
| 21   | FTP     |
| 22   | SSH     |
| 53   | DNS     |
| 80   | HTTP    |
| 135  | RPC     |
| 139  | NetBIOS |
| 443  | HTTPS   |
| 445  | SMB     |
| 3389 | RDP     |

## Usage

Run the scanner:

```bash
python scanner.py
```

Enter a subnet when prompted:

```text
Enter Subnet: 192.168.1.0/24
```

Example output:

```text
192.168.1.1 - gpon.net
  Port 53 OPEN DNS
  Port 80 OPEN HTTP
  Port 443 OPEN HTTPS

192.168.1.2 - DESKTOP-SQUJU4C
  Port 135 OPEN RPC
  Port 139 OPEN NetBIOS
  Port 445 OPEN SMB
```

## JSON Reporting

Scan results are automatically exported to a JSON file.

Example:

```json
[
    {
        "ip": "192.168.1.1",
        "hostname": "ROUTER",
        "open_ports": [
            {
                "port": 80,
                "service": "HTTP"
            }
        ],
        "mac": "AA:BB:CC:DD:EE:FF"
    }
]
```

## Project Structure

```text
Network-Device-Scanner/
│
├── scanner.py
├── sample_scan_results.json
├── .gitignore
└── README.md
```

## Learning Objectives

This project was built to strengthen practical knowledge of:

* Network discovery
* TCP/IP networking
* Host enumeration
* Port scanning techniques
* Multithreading in Python
* Structured data reporting
* Python socket programming

## Disclaimer

This tool is intended for educational purposes and authorized network assessment only. Only scan networks and devices you own or have permission to test.
