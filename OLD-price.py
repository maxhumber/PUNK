import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import LabelBinarizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
from gazpacho import Soup

# load

adf = pd.read_csv("csv/attributes.csv")
hdf = pd.read_csv("csv/history.csv", parse_dates=[0])

# join

sold = hdf[hdf['type'] == "Sold"]
sold30 = sold[(pd.Timestamp("now") - sold["date"]).dt.days <= 30]
sold30 = sold30[["id", "usd"]]
df = pd.merge(sold30, adf, on="id")
df = df.dropna()

# split

target = "usd"
y = df[target]
X = df.drop(target, axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# features

mapper = DataFrameMapper([
    ("attributes", [CountVectorizer(tokenizer=lambda x: x.split(" + ")), LabelBinarizer()])
])

# model

model = LinearRegression()

# pipeline

pipe = make_pipeline(mapper, model)
pipe.fit(X_train, y_train)
score = pipe.score(X_test, y_test)

# predict

pipe.predict(X_test)

# predict from website

def scrape(id):
    url = f"https://www.larvalabs.com/cryptopunks/details/{id}"
    soup = Soup.get(url)
    attributes = soup.find("a", {"href": "/cryptopunks/search?query"}, mode="list")
    attributes = [a.text for a in attributes]
    attributes = " + ".join(attributes)
    return pd.DataFrame({"id": id, "attributes": attributes}, index=[0])

new = scrape(3356)

pipe.predict(new)[0]

# coefs

attributes = (
    pipe
    .get_params()
    ["steps"]
    [0]
    [1]
    .get_params()
    ["features"]
    [0]
    [1]
    [0]
    .get_feature_names()
)

model = pipe.get_params()["steps"][-1][-1]
coefs = model.coef_

# attributes

attrs = pd.DataFrame({
    "attribute": attributes,
    "coef": coefs
}).sort_values("coef")

attrs[attrs["attribute"] == "knitted cap"]
