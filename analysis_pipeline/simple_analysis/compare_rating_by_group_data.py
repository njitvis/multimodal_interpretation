import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.model_selection import train_test_split


df = pd.read_csv('../data/average_rating.csv')
df.drop(columns=["mean_rating"], inplace=True)
df = df.astype(int)
df.rename(columns={
	'interpretability_rating_phd_res1': "Annotator_1",
	'interpretability_rating_phd_res2': "Annotator_2",
	'interpretability_rating_u_res1': "Annotator_3",
	'interpretability_rating_u_res2': "Annotator_4"
}, inplace=True)

def compute_agreement(labels):
    counts = Counter(labels)
    return len(counts)

df['Agreement'] = df[["Annotator_1", "Annotator_2", "Annotator_3", "Annotator_4"]].apply(compute_agreement, axis=1)
df.sort_values(by="Agreement", ascending=False, inplace=True)

df.drop(columns=["Agreement"], inplace=True)
df['image_id'] = df['image_id'].astype(str)
df['image_id'] = pd.Categorical(df['image_id'], categories=df['image_id'], ordered=True)
df_melted = pd.melt(
    df,
    id_vars=['image_id'],
    value_vars=[
        'Annotator_1',
        'Annotator_2',
        'Annotator_3',
        'Annotator_4'
    ],
    var_name='Rater',
    value_name='Rating'
)
df_melted['Group'] = df_melted['Rater'].apply(
    lambda r: 'PhD' if r in ['Annotator_1', 'Annotator_2'] else 'UG'
)
df_melted.to_csv("./sample_data/rating_with_group_pop.csv")



# for agreement_level, count in df.value_counts(subset=["Agreement"]).sort_index().items():
#     print(agreement_level, count, count/200)
#     prop_agreement.append(np.ceil((count/200) * 20).astype(int))

# target_counts = {1: 1, 2: 6, 3: 11, 4: 5}

# samples = []
# for level, n in target_counts.items():
#     group = df[df['Agreement'] == level]
#     if len(group) >= n:
#         sampled = group.sample(n=n, random_state=42)
#         samples.append(sampled)
#     else:
#         raise ValueError(f"Not enough rows with Agreement = {level} (needed {n}, found {len(group)})")

# # Combine and shuffle
# final_sample = pd.concat(samples).sample(frac=1, random_state=42).reset_index(drop=True)

# final_sample.sort_values(by="Agreement", ascending=False, inplace=True)
# final_sample.drop(columns=["Agreement"], inplace=True)


# final_sample['image_id'] = final_sample['image_id'].astype(str)
# final_sample['image_id'] = pd.Categorical(final_sample['image_id'], categories=final_sample['image_id'], ordered=True)
# final_sample_melted = pd.melt(
#     final_sample,
#     id_vars=['image_id'],
#     value_vars=[
#         'Annotator_1',
#         'Annotator_2',
#         'Annotator_3',
#         'Annotator_4'
#     ],
#     var_name='Rater',
#     value_name='Rating'
# )
# final_sample_melted['Group'] = final_sample_melted['Rater'].apply(
#     lambda r: 'PhD' if r in ['Annotator_1', 'Annotator_2'] else 'UG'
# )
# final_sample_melted.to_csv("./sample_data/rating_with_group.csv")