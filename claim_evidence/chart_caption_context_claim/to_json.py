import pandas as pd
import json


all = pd.read_csv("./all.csv")
all["Claim_With_Context"].fillna("", inplace=True)

records = []
for _, row in all.iterrows():
	record_dict = {
    "chartSrc": f"{row["image_id"]}.png",
    "caption": row["caption"],
    "context": row["context"],
    "claims": [ 
      {"claim": claim, "strategy": "", "evidences": [""]}
      for claim in row["Claim_Without_Context"].split("\n")
    ]
    +
    [ 
      {"claim": claim, "strategy": "", "evidences": [""]}
      for claim in row["Claim_With_Context"].split("\n")
    ]
  }
	records.append(record_dict)

json_str = json.dumps(records, indent=2, ensure_ascii=False)

with open("all.json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)