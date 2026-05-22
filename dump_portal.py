import requests
URL = "https://portal.mobileso.com/mcso/jail/jp_ci_c.asp"
r = requests.get(URL, timeout=10)
print(r.text[:1000])
