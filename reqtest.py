
import requests
import time
import os
import json
import urllib.parse

"""
url = "https://transfer.cyberflixt.repl.co"

info = "lorem"

headers = requests.utils.default_headers()
agent = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
headers.update(agent)
print(headers)


enc = urllib.parse.quote_plus(json.dumps(info))
enc = "lorem"
url = url + '?data=' + enc
print(url)
r = requests.get(url, headers = headers)

#r = requests.get('https://google.com', headers=headers)

"""

session = requests.Session()

url = 'https://google.com'
cookies={'from-my': 'browser'}
cookies={
    '_ga_W02QY0T0GX'='GS1.1.1697526754.1.1.1697526780.0.0.0',
    '_ga'='GA1.1.1002241140.1697526755',
    
}
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

r = session.get(url, headers=headers, cookies=cookies, timeout=10)

print(r)



print('end')
