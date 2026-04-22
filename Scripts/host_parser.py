import re
import os

# Specific file identified as the data source
target_file = "/data/data/com.termux/files/home/devices.txt"

def get_hosts():
    found_hosts = []
    if os.path.exists(target_file):
        with open(target_file, 'r') as f:
            content = f.read()
            # Extracts IPs following "Nmap scan report for"
            found_hosts = re.findall(r'Nmap scan report for (?:.* \()?(\d{1,3}(?:\.\d{1,3}){3})\)?', content)
    return sorted(list(set(found_hosts)))

if __name__ == "__main__":
    hosts = get_hosts()
    if hosts:
        for host in hosts:
            print(host)
