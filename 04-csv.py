import pandas as pd
import json
from pathlib import Path
from tqdm import tqdm

files = Path("json").glob("*.json")

data = []
for file in tqdm(files):
    with open(file, "r") as f:
        punk = json.load(f)
    data.append(punk)

# attributes

df = pd.DataFrame([])
for punk in tqdm(data):
    id = punk['id']
    attributes = " + ".join(punk['attributes'])
    pdf = pd.DataFrame({"id": id, "attributes": attributes}, index=[0])
    df = df.append(pdf)
df = df.reset_index(drop=True)
df["id"] = df["id"].apply(int)
df = df.sort_values(["id"])
df = df.reset_index(drop=True)
df.to_csv("csv/attributes.csv", index=False)

# history

df = pd.DataFrame([])
for punk in tqdm(data):
    pdf = pd.DataFrame(punk['transactions'])
    pdf["id"] = punk["id"]
    df = df.append(pdf)

df["Date"] = pd.to_datetime(df["Date"])
df.columns = [c.lower() for c in df.columns]

amount = "12KΞ ($21.78M)"

def parse_amount(amount):
    if "<" in amount:
        return pd.Series([0.00, 0.00])
    try:
        eth, usd = amount.split("Ξ ($")
        if "K" in eth:
            eth = eth.replace("K", "")
            eth = float(eth)
            eth *= 1000
        usd = usd.replace(")", "")
        usd = usd.replace(",", "")
        if "M" in usd:
            usd = usd.replace("M", "")
            usd = float(usd)
            usd *= 1e6
        eth = float(eth)
        usd = float(usd)
        return pd.Series([eth, usd])
    except:
        return pd.Series([None, None])

df[["eth", "usd"]] = df["amount"].apply(parse_amount)

df = df[["date", "id", "type", "from", "to", "eth", "usd"]]
df["id"] = df["id"].apply(int)
df = df.sort_values(["date", "id"])
df.reset_index(drop=True)
df.to_csv("csv/history.csv", index=False)
