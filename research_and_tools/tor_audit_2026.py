import requests

# Tor default port is 9050 in Termux
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

url = "https://www.sec.gov/Archives/edgar/data/0000035402/000003540226002201/0000035402-26-002201.txt"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

print("Executing forensic pull via Onion circuit...")
try:
    r = requests.get(url, headers=headers, proxies=proxies, timeout=60)
    if r.status_code == 200:
        with open("complete_audit.txt", "wb") as f:
            f.write(r.content)
        print(f"SUCCESS: Captured {len(r.content)} bytes via Tor.")
    else:
        print(f"Tor failed: {r.status_code}. The exit node may be blocked.")
except Exception as e:
    print(f"Connection Error: {e}. Is Tor running on port 9050?")
