import pandas as pd
import re

captions = pd.read_csv("./data/captions.csv")

captions["caption"] = captions["caption"].apply(lambda x: re.sub(r'- \n', '', x))
captions["caption"] = captions["caption"].apply(lambda x: re.sub(r' \n', ' ', x))
captions["caption"] = captions["caption"].apply(lambda x: re.sub(r'\n', ' ', x))
captions.to_csv("./data/captions.csv", index=False)