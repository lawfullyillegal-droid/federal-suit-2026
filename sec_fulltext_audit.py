import requests

# Target: 734919TC1
identifier = "734919TC1"

# Using the primary web-facing search URL which is more stable for DNS
url = f"https://www.sec.gov/edgar/search/#/q={identifier}"

headers = {
    'User-Agent': 'Investigative Researcher travis.ryle@outlook.com',
    'Host': 'www.sec.gov',
    'Accept': 'text/html,application/xhtml+xml,xml'
}

print(f"[*] Auditing primary EDGAR index for: {identifier}")

try:
    # We use verify=True but if SSL persists as an issue in Termux, 
    # check your 'ca-certificates' package.
    response = requests.get(url, headers=headers, timeout=15)
    if response.status_code == 200:
        print("[+] Connection Established with SEC Master Server.")
        with open("sec_fulltext_results.html", "w") as f:
            f.write(response.text)
        print("[!] Result saved to sec_fulltext_results.html")
    else:
        print(f"[!] Server returned status: {response.status_code}")
except Exception as e:
    print(f"[!] Final Resolution Error: {e}")

