import json
from pathlib import Path
from gazpacho import Soup
from tqdm import tqdm

def get_id(file):
    return file.name.split(".")[0]

def get_owner(soup):
    return (
        soup
        .find("div", {"class": "col-md-10 col-md-offset-1"})[2]
        .find("a", {"href": "accountinfo"}, mode="first")
        .attrs['href']
        .split("=")[-1]
    )

def tr_to_dict(tr):
    row = [td.text for td in tr.find("td")]
    d = dict(zip(["Type", "From", "To", "Amount", "Date"], row))
    return d

def parse(file):
    with open(file, "r") as f:
        html = f.read()
    id = get_id(file)
    soup = Soup(html)
    attributes = soup.find("a", {"href": "/cryptopunks/search?query"}, mode="list")
    attributes = [a.text for a in attributes]
    trs = soup.find("tr")[1:]
    transactions = [tr_to_dict(tr) for tr in trs]
    try:
        owner = get_owner(soup)
    except:
        owner = None
    return dict(id=id, owner=owner, attributes=attributes, transactions=transactions)

files = Path("html").glob("*.html")

data = []
for file in tqdm(files):
    id = get_id(file)
    d = parse(file)
    data.append(d)

data = sorted(data, key=lambda x: x["id"])

with open(f"data/punks.json", "w") as f:
    json.dump(data, f, indent=2)
