import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

captions = pd.read_csv("./datasets/found_captions.csv")
captions["source"] = captions["source"].apply(lambda x: x[:-2].split("/")[-1])
captions["caption"] = captions["caption"].apply(lambda x: x.lower().replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').strip())
captions = captions[["image_id", "source", "caption", "pageNumber"]]
captions.rename(columns={"image_id": "image_id_new"}, inplace=True)

captions_vectors = pd.read_csv("./datasets/chart_vectors_complete.csv")
captions_metadata = pd.read_csv("./datasets/chart_metadata.csv")
captions_of_interest = pd.merge(captions_metadata, captions_vectors, on="image_id", how="inner")
captions_of_interest = captions_of_interest[["image_id", "source", "caption", "l1_l4_cluster"]]
captions_of_interest['caption'] = captions_of_interest['caption'].str.lower()
captions_of_interest.rename(columns={"image_id": "image_id_old"}, inplace=True)

model = SentenceTransformer('all-MiniLM-L6-v2')

embeddings1 = model.encode(captions_of_interest['caption'])
embeddings2 = model.encode(captions['caption'])

similarity_matrix = cosine_similarity(embeddings1, embeddings2)

threshold = 0.75
matches = []

for i in range(similarity_matrix.shape[0]):
    max_sim_index = similarity_matrix[i].argmax()
    max_sim_score = similarity_matrix[i][max_sim_index]
    if max_sim_score > threshold:
        matches.append((captions_of_interest.iloc[i]['image_id_old'], captions_of_interest.iloc[i]['source'], captions_of_interest.iloc[i]['caption'], captions_of_interest.iloc[i]['l1_l4_cluster'],
                        captions.iloc[max_sim_index]['image_id_new'], captions.iloc[max_sim_index]['source'], captions.iloc[max_sim_index]['caption'], captions.iloc[max_sim_index]['pageNumber'],
                        max_sim_score))

merged_df = pd.DataFrame(matches, columns=['image_id_old', 'source_1', 'caption_1', 'l1_l4_cluster', 'image_id_new', 'source_2', 'caption_2', 'pageNumber', 'similarity'])

found_captions_with_vector= merged_df[merged_df['source_1'] == merged_df['source_2']]

found_captions_with_vector.to_csv("./datasets/found_captions_with_vector.csv", index=False)

