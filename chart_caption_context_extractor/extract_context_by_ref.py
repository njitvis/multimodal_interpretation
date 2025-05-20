import pandas as pd
import fitz
import nltk
from nltk.tokenize import sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity
import re
import os
import shutil



CAPTION_PATTERN = re.compile(
    r'^\s*'
    r'(fig(?:ure)?\.?\s*[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*\s*(?:[:\-]?\s*\(\s*[a-zA-Z0-9\.-]+\s*\))?[:\-]?)\s*',
    re.IGNORECASE
)

captions = pd.read_csv("./captions.csv")
sources = set(captions["source"])

context_map = {}
for source in sources:
	try:
		pdf_file = fitz.open(f"./datasets/PDFs/{source}")
		captions_from_source = captions[captions['source'] == source]
		captions_from_source = captions.dropna(subset=["figure_ref"])
		fig_ref_from_source = captions_from_source['figure_ref'].to_list()

		for page in pdf_file:
				text_blocks = page.get_text("blocks")
				for block in text_blocks:
						block_text = block[4].lower()

						block_text = re.sub(r'\n', ' ', block_text)
						block_text = re.sub(r'\s+', ' ', block_text).strip()

						if CAPTION_PATTERN.match(block_text):
							continue
						for ref in fig_ref_from_source:
							if ref in block_text:
									key = (source, ref)
									if key in context_map:
											context_map[key]["context"] += " " + block_text
									else:
											context_map[key] = {
													"source": source,
													"page": page.number + 1,
													"context": block_text,
													"figure_ref": ref
											}
		print(context_map)

		pdf_file.close()
	except Exception as ex:
		print(f"{source} not found: {ex}")

df = pd.DataFrame(context_map.values(), columns=["source", "page", "context", "figure_ref"])
df.to_csv("extracted_context.csv", index=False)