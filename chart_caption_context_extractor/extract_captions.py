import pandas as pd
import fitz
import re



CAPTION_PATTERN = re.compile(
    r'^\s*'
    r'(fig(?:ure)?\.?\s*[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*\s*(?:[:\-]?\s*\(\s*[a-zA-Z0-9\.-]+\s*\))?[:\-]?)\s*',
    re.IGNORECASE
)

captions = pd.read_csv("./captions.csv")
sources = set(captions["source"])

rows = []
for source in sources:
	try:
		pdf_file = fitz.open(f"./datasets/PDFs/{source}")

		for page in pdf_file:
				text_blocks = page.get_text("blocks")
				for block in text_blocks:
						block_text = block[4]
						fig_refs = re.findall(CAPTION_PATTERN, block_text)
						if len(fig_refs) > 0:
							rows.append({
										"source": f"{pdf_file}",
										"figure_ref": fig_refs[0],
										"page": page.number + 1,
										"caption": block_text,
							})

		pdf_file.close()
	except:
		print(f"{source} not found")
df = pd.DataFrame(rows, columns=["source", "figure_ref", "page", "caption"])
df.to_csv("extracted_captions.csv", index=False)