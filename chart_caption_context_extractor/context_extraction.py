import pandas as pd
import fitz
import nltk
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

captions = pd.read_csv("./datasets/found_captions_with_vector.csv")
captions = captions[["image_id_new", "source_2", "caption_2", "pageNumber", "l1_l4_cluster"]]
captions.rename(columns={"image_id_new": "image_id", "source_2": "source", "caption_2": "caption"}, inplace=True)

def get_content_and_caption(caption):
    pdf_file = fitz.open(f"./datasets/PDFs/{caption['source']}")
    content = ""
    page = pdf_file.load_page(caption["pageNumber"] - 1)
    content = content + page.get_text()
    page = pdf_file.load_page(caption["pageNumber"])
    content = content + page.get_text()
    page = pdf_file.load_page(caption["pageNumber"] + 1)
    content = content + page.get_text()

    return content.replace("\n", " "), caption["caption"]


model = SentenceTransformer('all-mpnet-base-v2')


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

    return similar_sentences

# from nltk.tokenize import word_tokenize
# from gensim.models import KeyedVectors
# import gensim.downloader as api
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity


# word2vec_model = api.load("word2vec-google-news-300")

# def get_sentence_vector(sentence, model):
#     words = word_tokenize(sentence.lower())
#     word_vectors = [model[word] for word in words if word in model]

#     if not word_vectors:
#         return np.zeros(model.vector_size)

#     return np.mean(word_vectors, axis=0)

# def get_similar_sentences_word2vec(content, caption):
#     sentences = sent_tokenize(content)

#     sentence_vectors = [get_sentence_vector(sent, word2vec_model) for sent in sentences]
#     caption_vector = get_sentence_vector(caption, word2vec_model)

#     similar_sentences = [
#         sentences[i] for i, sent_vector in enumerate(sentence_vectors)
#         if cosine_similarity([sent_vector], [caption_vector])[0][0] >= 0.7
#     ]

#     return similar_sentences


caption_with_context = pd.DataFrame(columns=['image_id', 'caption', 'sent2vec_context'])
# caption_with_context = pd.DataFrame(columns=['image_id', 'caption', 'sent2vec_context', 'word2vec_context'])

for idx, caption in captions.iterrows():
    if idx > 10:
        break
    c = {
        "source": caption["source"],
        "pageNumber": caption["pageNumber"],
        "caption": caption["caption"],
        "image_id": caption["image_id"]
    }
    content, caption_text = get_content_and_caption(c)
    context_sent2vec = get_similar_sentences(content, caption_text)
    caption_with_context.loc[idx] = [caption["image_id"], caption["caption"], context_sent2vec]
    # context_word2vec = get_similar_sentences_word2vec(content, caption_text)
    # caption_with_context.loc[idx] = [caption["image_id"], caption["caption"], context_sent2vec, context_word2vec]

caption_with_context.to_csv("./datasets/found_caption_with_context.csv", index=False)