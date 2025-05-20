import pandas as pd
import re

captions = pd.read_csv("./captions.csv")

CAPTION_PATTERN = re.compile(
    r'^\s*'
    r'(fig(?:ure)?\.?\s*[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*\s*(?:[:\-]?\s*\(\s*[a-zA-Z0-9\.-]+\s*\))?[:\-]?)\s*',
    re.IGNORECASE
)


def get_fig_ref(s):
	s = s.lower()
	fig_refs = re.findall(CAPTION_PATTERN, s)
	if len(fig_refs) > 0:
		return fig_refs[0]
	else:
		return ''

captions["figure_ref"] = captions["caption"].apply(get_fig_ref)

print(captions[captions["figure_ref"] == ""].shape[0], "missing")

captions.to_csv("./captions.csv", index=False)