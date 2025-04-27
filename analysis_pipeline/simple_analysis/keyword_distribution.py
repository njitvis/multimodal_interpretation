from collections import Counter
import json
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# nltk.download('punkt_tab')
# nltk.download('wordnet')


with open('../data/keywords_dict.json') as f:
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

    total = sum(cnt.values()) or 1
    return [cnt.get(cat, 0) / total for cat in category_list]

labeled_sentences = pd.read_csv('../data/label_train.csv')
labeled_sentences["keyword_vector_prop"] = labeled_sentences["sentence"].apply(compute_category_vector)
for idx, key in enumerate(category_list):
    labeled_sentences[key] = labeled_sentences['keyword_vector_prop'].apply(lambda x: x[idx])
labeled_sentences.drop(columns=["sentence", "keyword_vector_prop"], inplace=True)

grouped = labeled_sentences.groupby('semantic_level').mean()


grouped.index.name = 'semantic_level'

fig, axes = plt.subplots(1, 4, figsize=(13, 4))
axes = axes.flatten()

for idx, level in enumerate(grouped.index):
    ax = axes[idx]
    values = grouped.loc[level].values
    columns = grouped.columns
    y = np.arange(len(columns))

    ax.barh(y, values)
    ax.set_title(f'Semantic Level {level}')
    ax.set_xlim(0, 1)
    if idx == 1:
        ax.set_xlabel('Average Proportion of Keyword')
    else:
        ax.set_xlabel('')

    if idx == 0:
        ax.set_yticks(y)
        ax.set_yticklabels(columns)
        ax.set_ylabel('Categories')
    else:
        ax.set_yticks([])

    ax.invert_yaxis()

plt.tight_layout()
plt.savefig("./output/keyword_distribution.png", dpi=300)
plt.close()
