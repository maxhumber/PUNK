import json
from pathlib import Path
from gazpacho import Soup
from tqdm import tqdm

# load everthing

files = Path("html").glob("*.html")

# funcs

def get_id(file):
    return file.name.split(".")[0]

def get_owner(soup):
    return (
        soup
        .find("div", {"class": "col-md-10 col-md-offset-1"})[2]
        .find("a", {"href": "accountinfo"})
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
    owner = get_owner(soup)
    return dict(id=id, owner=owner, attributes=attributes, transactions=transactions)

# parse everything

for file in tqdm(files):
    try:
        id = get_id(file)
        data = parse(file)
        with open(f"json/{id}.json", "w") as f:
            json.dump(data, f, indent=2)
    except:
        pass
