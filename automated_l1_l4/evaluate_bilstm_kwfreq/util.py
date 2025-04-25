from collections import Counter
import json
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

# nltk.download('punkt_tab')
# nltk.download('wordnet')


with open('../keywords_dict.json') as f:
    keyword_dict = json.load(f)

lemmatizer = WordNetLemmatizer()

lemmatized_keywords = {}
for cat, words in keyword_dict.items():
    lemmas = set()
    for w in words:
        for token in word_tokenize(w.lower()):
            if token.isalpha():
                lemmas.add(lemmatizer.lemmatize(token))
    lemmatized_keywords[cat] = lemmas

category_list = list(lemmatized_keywords.keys())

def compute_category_vector(sentence):
    tokens = [tok for tok in word_tokenize(sentence.lower()) if tok.isalpha()]
    lemmas = [lemmatizer.lemmatize(tok) for tok in tokens]

    cnt = Counter()
    for lemma in lemmas:
        for cat, lemmas_set in lemmatized_keywords.items():
            if lemma in lemmas_set:
                cnt[cat] += 1

    total = len(lemmas) or 1
    return [cnt.get(cat, 0) / total for cat in category_list]