import pandas as pd
import json


with open("all.json", "r") as file:
    data = json.load(file)

all = pd.json_normalize(data)

with open("completed.json", "r") as file:
    data = json.load(file)

done = pd.json_normalize(data)

remaining = all[~all['chartSrc'].isin(done['chartSrc'].to_list())]

remaining.to_json("remaining.json", orient="records", indent=2)
