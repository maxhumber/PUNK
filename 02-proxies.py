import random
import time
import json
from itertools import cycle
from collections import Counter
from pathlib import Path
import requests
from gazpacho import Soup
from tqdm import tqdm

# get proxies

url = "https://free-proxy-list.net/"
soup = Soup.get(url)
table = soup.find("table", {"id": "proxylisttable"})
trs = table.find("tr")[1:-1]
tr = trs[0]
proxy = ":".join([td.text for td in tr.find("td")[:2]])

def parse(tr):
    proxy = ":".join([td.text for td in tr.find("td")[:2]])
    return proxy

proxies = [parse(tr) for tr in trs]

# scrape functions

def save_html(id, proxy):
    url = f"https://www.larvalabs.com/cryptopunks/details/{id}"
    response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=5)
    html = response.text
    if "Too Many Requests" in html:
        raise Exception("Too Many Requests")
    if "Why do I have to complete a CAPTCHA?" in html:
        raise Exception("Cloudflare")
    with open(f"html/{id}.html", "w") as f:
        f.write(html)

# check already scraped

files = Path("html").glob("*.html")
scraped_ids = [int(f.name.replace(".html", "")) for f in files]
scraped_ids = set(scraped_ids)
full_ids = set(range(0, 10000))
ids = full_ids - scraped_ids

# iterate

counter = Counter()
ids = list(ids)
random.shuffle(ids)
pool = cycle(proxies)
proxy = next(pool)
while len(ids) > 0:
    try:
        id = ids[-1]
        save_html(id, proxy)
        ids.pop()
        counter["SUCCESS"] += 1
        print(counter)
    except:
        proxy = next(pool)
        counter["FAIL"] += 1
        print(counter)
        continue
    print(f"IDs left: {len(ids)}")
