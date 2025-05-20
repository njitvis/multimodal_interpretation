import pandas as pd
import re

captions = pd.read_csv("./captions.csv")
extracted_captions = pd.read_csv("./extracted_captions.csv")
extracted_context = pd.read_csv("./extracted_context.csv")
if "image_id" in extracted_context.columns:
	extracted_context.drop(columns=["image_id"], inplace=True)

# CAPTION_PATTERN = re.compile(
# 	r'^\s*'
# 	r'(fig(?:ure)?\.?\s*\d+(?:\.\d+)?[a-zA-Z0-9\.-]*\s*(?:[:\-]?\s*\(\s*[a-zA-Z0-9\.-]+\s*\))?[:\-]?)\s*'
# 	, re.IGNORECASE
# )

# captions["caption"] = captions["caption"].apply(lambda txt: CAPTION_PATTERN.sub("", txt, count=1).lstrip())
# captions["caption"] = captions["caption"].str.replace("\n", "", regex=False)
# captions["caption"] = captions["caption"].str.replace(r'[^A-Za-z0-9]', "", regex=True)
# captions["caption"] = captions["caption"].str.lower()
# filtered_captions = captions["caption"].to_list()

# extracted_captions["caption"] = extracted_captions["caption"].str.replace("°", "deg", regex=False)
# extracted_captions["formatted_caption"] = extracted_captions["caption"].apply(lambda txt: CAPTION_PATTERN.sub("", txt, count=1).lstrip())
# extracted_captions["formatted_caption"] = extracted_captions["formatted_caption"].str.replace("\n", "", regex=False)
# extracted_captions["formatted_caption"] = extracted_captions["formatted_caption"]
# extracted_captions["formatted_caption"] = extracted_captions["formatted_caption"].str.lower()

# extracted_captions["filter"] = extracted_captions["formatted_caption"].isin(filtered_captions)

# # print(extracted_captions[extracted_captions["filter"]])
# print(captions[~captions["caption"].isin(extracted_captions["formatted_caption"].to_list())])
# # print(captions.loc[captions["image_id"] == 14, "caption"].to_list()[0])
# # print(extracted_captions.loc[2563, "formatted_caption"])

captions["key"] = captions["source"].str.lower() + captions["figure_ref"].str.lower()
captions["key"] = captions["key"].str.replace(r'[^A-Za-z0-9]', "", regex=True)
extracted_captions["key"] = extracted_captions["source"].str.lower() + extracted_captions["figure_ref"].str.lower()
extracted_context["key"] = extracted_context["source"].str.lower() + extracted_context["figure_ref"].str.lower()
extracted_context["key"] = extracted_context["key"].str.replace(r'[^A-Za-z0-9]', "", regex=True)

# print(extracted_context[extracted_context["key"].isin(captions["key"].to_list())].shape)
# print(extracted_captions[extracted_captions["key"].isin(captions["key"].to_list())].shape)
# print(captions[captions["key"].isin(extracted_captions["key"].to_list())].shape)
# print(captions[captions["key"].isin(extracted_context["key"].to_list())].shape)

extracted_context = (
    extracted_context
        .merge(captions[['key', 'image_id']], on='key', how='left')
)
extracted_context = extracted_context.fillna(0)
extracted_context['image_id'] = (
    extracted_context['image_id']         
        .round()              
        .astype('int64')           
)
print(extracted_context[extracted_context["image_id"] != 0])
extracted_context[['image_id', 'source', 'page', 'context', 'figure_ref']].to_csv("./extracted_context.csv", index=False)