import pandas as pd
import fitz
import nltk
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
import os
import shutil


#############################################################
# CONSTANTS                                                 #
#############################################################
PDF_FILE_DIR = "./datasets/PDFs"
CAPTION_PATTERN = r'\b(fig(?:ure)?\.?\s*\d+(?:\.\d+)?[a-zA-Z0-9\.-]*\s*(?:[:\-]?\s*\(\s*[a-zA-Z0-9\.-]+\s*\))?[:\-]?)\s*'
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')


#############################################################
# ULIT FUNCTIONS                                            #
#############################################################
def get_adj_content_and_caption(caption):
    pdf_file = fitz.open(f"{PDF_FILE_DIR}/{caption['source']}")
    content = ""
    page = pdf_file.load_page(caption["pageNumber"] - 1)
    content = content + page.get_text()
    page = pdf_file.load_page(caption["pageNumber"])
    content = content + page.get_text()
    page = pdf_file.load_page(caption["pageNumber"] + 1)
    content = content + page.get_text()

    pdf_file.close()

    # remove sentences from content that match the pattern
    for sentence in content.split("\n"):
        if re.search(CAPTION_PATTERN, sentence):
            content = content.replace(sentence + "\n", "")

    return content.replace("\n", " ")


def get_ref_content_and_caption(caption):
    pdf_file = fitz.open(f"{PDF_FILE_DIR}/{caption['source']}")

    caption_id = re.findall(CAPTION_PATTERN, caption["caption"], re.IGNORECASE)[0].lower().strip().replace("\n", " ").rstrip(":.")

    extracted_text = []
    for page in pdf_file:
        text_blocks = page.get_text("blocks")
        for block in text_blocks:
            block_text = block[4]
            fig_refs = re.findall(CAPTION_PATTERN, block_text, re.IGNORECASE)
            fig_refs = [ref.lower().strip().replace("\n", " ").rstrip(":.") for ref in fig_refs]
            if caption_id in fig_refs:
                extracted_text.extend(block_text.split("\n"))

    pdf_file.close()

    return " ".join(extracted_text)


def get_content_and_caption(caption):
    adj_content = get_adj_content_and_caption(c)
    ref_content = get_ref_content_and_caption(c)

    combined_sentences = adj_content.split("\n") + ref_content.split("\n")

    unique_content = " ".join(list(set(combined_sentences))).replace("- ", "")

    return unique_content, caption["caption"]


def get_similar_sentences(pdf_text, caption, threshold=0.7):
    """ Finds sentences in a research paper similar to the given caption. """
    sentences = sent_tokenize(pdf_text)
    sentences =[sentence for sentence in sentences if len(sentence.strip()) > 3]

    sentences_vectors = model.encode(sentences)

    caption_vector = model.encode([caption])[0]

    similar_sentences = []

    for i, sentence_vector in enumerate(sentences_vectors):
        similarity = cosine_similarity([sentence_vector], [caption_vector])[0][0]

        if similarity >= threshold:
            similar_sentences.append(sentences[i])

    return " ".join(similar_sentences)


def remove_captions_from_context(context, captions):
    for caption in captions:
        context = re.sub(r'\s+', ' ', context)
        context = re.sub(r'' + re.escape(caption.lower()), '', context.lower())
    
    return context

def remove_duplicates(context):
    sentences = sent_tokenize(context)
    unique_sentences = list(set(sentences))
    return " ".join(unique_sentences)




#############################################################
# MAIN FUNCTIONS                                            #
#############################################################
nltk.download('punkt_tab')

captions = pd.read_csv("./datasets/found_captions_with_vector.csv")
captions = captions[["image_id_new", "source_2", "caption_2", "pageNumber", "l1_l4_cluster"]]
captions.rename(columns={"image_id_new": "image_id", "source_2": "source", "caption_2": "caption"}, inplace=True)
print("Captions successfully read ...")

caption_with_context = pd.DataFrame(columns=['image_id', 'caption', 'sent2vec_context'])

for idx, caption in captions.iterrows():
    c = {
        "source": caption["source"],
        "pageNumber": caption["pageNumber"],
        "caption": caption["caption"],
        "image_id": caption["image_id"]
    }
    try:
        content, caption_text = get_content_and_caption(c)
        cleaned_content = remove_captions_from_context(content, captions[captions["source"] == caption["source"]]["caption"].to_list())
        unique_content = remove_duplicates(cleaned_content)
        context_sent2vec = get_similar_sentences(unique_content, caption_text)
        caption_with_context.loc[idx] = [caption["image_id"], caption["caption"], context_sent2vec]
        print(f"Extraction Successful for: {caption["image_id"]}")
    except Exception as e:
        print(f"Failed to extract context: {e}")

caption_with_context.to_csv("./datasets/found_caption_with_context.csv", index=False)

nltk_data_path = os.path.expanduser('~/nltk_data')
if os.path.exists(nltk_data_path):
    shutil.rmtree(nltk_data_path)
    print("NLTK data deleted successfully.")
else:
    print("No NLTK data found to delete.")