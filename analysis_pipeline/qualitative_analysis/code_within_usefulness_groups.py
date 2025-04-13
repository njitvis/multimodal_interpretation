import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')


lemmatizer = WordNetLemmatizer()
tokenizer = RegexpTokenizer(f'\w+')
stop_words = nltk.corpus.stopwords.words('english')

def preprocess_sentence(sentence):
  sentence = sentence.lower()
  sentence = tokenizer.tokenize(sentence)
  sentence = [lemmatizer.lemmatize(word) for word in sentence]
  sentence = [word for word in sentence if word not in stop_words]
  return " ".join(sentence)

reasons = pd.read_csv("./data/reasons_caption_segment.csv")

usefulness_groups = ["useful", "not_useful", "neutral"]

model_name = "all-mpnet-base-v2"
model = SentenceTransformer(model_name)
kmeans = KMeans(n_clusters=5, random_state=0)

for usefulness_group in usefulness_groups:
    group = reasons[reasons['usefulness'] == usefulness_group]

    print("🔍 Encoding sentences...")
    embeddings = model.encode(group['reason'].to_list())

    print("🧩 Clustering themes...")
    similarity_matrix = cosine_similarity(embeddings)
    labels = kmeans.fit_predict(similarity_matrix)

    group["cluster"] = labels

    group.to_csv(f"./data/clustered_{usefulness_group}_captions.csv", index=False)