from gazpacho import Soup

# one punk

id = 8348
url = f"https://www.larvalabs.com/cryptopunks/details/{id}"

# get html

soup = Soup.get(url)

# accessories

attributes = soup.find("a", {"href": "/cryptopunks/search?query"}, mode="list")
attributes = [a.text for a in attributes]

# transaction history

trs = soup.find("tr")[1:]

# parse one

tr = trs[0]
row = [td.text for td in tr.find("td")]
dict(zip(["Type", "From", "To", "Amount", "Date"], row))

# function

def tr_to_dict(tr):
    row = [td.text for td in tr.find("td")]
    d = dict(zip(["Type", "From", "To", "Amount", "Date"], row))
    return d

# transactions list

transactions = [tr_to_dict(tr) for tr in trs]

# full info

{
    "id": id,
    "attributes": attributes,
    "transactions": transactions
}

# wrapped up

def scrape(id):
    url = f"https://www.larvalabs.com/cryptopunks/details/{id}"
    soup = Soup.get(url)
    attributes = soup.find("a", {"href": "/cryptopunks/search?query"}, mode="list")
    attributes = [a.text for a in attributes]
    trs = soup.find("tr")[1:]
    transactions = [tr_to_dict(tr) for tr in trs]
    return dict(id=id, attributes=attributes, transactions=transactions)

scrape(3)
