import pandas as pd
import numpy as np
# from statsmodels.stats.inter_rater import fleiss_kappa
# from sklearn.metrics import cohen_kappa_score
import krippendorff
# from itertools import combinations


# print(
# "#" * 100,
# """
# \nRELIABILITY: the degree to which raters are consistent in their relative ratings of subjects, regardless of whether they assign the exact same score.
# AGREEMENT: the degree to which raters assign the same exact score to each subject.\n
# """,
# "#" * 100)

# print("\n\nAGREEMENT\n")
# def check_IRA(df, categories = [1, 2, 3, 4, 5]):
#     print()
#     cats   = sorted(df.stack().unique())
#     matrix = np.vstack([
#         [(row == c).sum() for c in cats]
#         for _, row in df.iterrows()
#     ])
#     kappa = fleiss_kappa(matrix)
#     print(f"Likert Scale: {categories}")
#     print("Fleiss' Kappa:", round(kappa, 4))

# def check_IRA_group(df):
#     print()
#     categories = sorted(df.stack().unique()) 
#     for a, b in combinations(df.columns, 2):
#         kappa = cohen_kappa_score(df[a], df[b])
#         print(f"Likert Scale: {categories}")
#         print("Cohen's Kappa:", round(kappa, 4))


ratings = pd.read_csv("../data/all_reasons.csv")
ratings = ratings[["image_id", "interpretability_rating_u_res1", "interpretability_rating_u_res2", "interpretability_rating_res1", "interpretability_rating_res2"]]
ratings['interpretability_rating_res1'] = ratings['interpretability_rating_res1'].astype(int)
ratings.set_index('image_id', inplace=True)

ratings_ug = ratings[["interpretability_rating_u_res1", "interpretability_rating_u_res2"]]
ratings_phd = ratings[["interpretability_rating_res1", "interpretability_rating_res2"]]

# print("Considering individual ratings")
# check_IRA(ratings)

# print('-' * 100)
# print("Among UG Students:")
# check_IRA_group(ratings_ug)
# print('-' * 100)
# print("Among PhD Students:")
# check_IRA_group(ratings_phd)
# print("\n# There is only slight agreement among all the raters even withing groups of expertise level")


def map_rating(r):
    if r <= 2:
        return 'Low'
    elif r == 3:
        return 'Moderate'
    else:
        return 'High'

# print('=' * 100)
# ratings_encoded = ratings.map(map_rating)
# check_IRA(ratings_encoded, categories=["Low", "Moderate", "High"])
# print('-' * 100)
# print("Among UG Students:")
# check_IRA_group(ratings_ug.map(map_rating))
# print('-' * 100)
# print("Among PhD Students:")
# check_IRA_group(ratings_ug.map(map_rating))
# print("\n# Aggreement among the raters improve when rating is categorized but still only slight agreement. However, moderate agreement is observed within groups.")
# print("=" * 100)



print("=" * 100)
print("\nRELIABILITY\n")
print("Likert scale: [1, 2, 3, 4, 5]")
alpha_nominal = krippendorff.alpha(reliability_data=ratings.to_numpy().T, level_of_measurement='ordinal')
print("Krippendorff's Alpha:", round(alpha_nominal, 3))
print()
print("Among UG Students:")
alpha_nominal = krippendorff.alpha(reliability_data=ratings_ug.to_numpy().T, level_of_measurement='ordinal')
print("Krippendorff's Alpha:", round(alpha_nominal, 3))
print()
print("Among PhD Students:")
alpha_nominal = krippendorff.alpha(reliability_data=ratings_phd.to_numpy().T, level_of_measurement='ordinal')
print("Krippendorff's Alpha:", round(alpha_nominal, 3))
print("""\n# There is only slight consistency in relative ratings among raters.
# Moderate consistency is observed among UG annotators.
# Consistency among PhD annotators is lower.""")
print()
print("-" * 100)
print()

def map_rating_num(r):
    if r <= 2:
        return 1
    elif r == 3:
        return 3
    else:
        return 5

ratings_encoded_num = ratings.map(map_rating_num)
print("Categories: [Low, Med, High]")
alpha_nominal = krippendorff.alpha(reliability_data=ratings_encoded_num.to_numpy().T, level_of_measurement='ordinal')
print("Krippendorff's Alpha:", round(alpha_nominal, 3))
print()
print("Among UG Students:")
alpha_nominal = krippendorff.alpha(reliability_data=ratings_ug.map(map_rating_num).to_numpy().T, level_of_measurement='ordinal')
print("Krippendorff's Alpha:", round(alpha_nominal, 3))
print()
print("Among PhD Students:")
alpha_nominal = krippendorff.alpha(reliability_data=ratings_phd.map(map_rating_num).to_numpy().T, level_of_measurement='ordinal')
print("Krippendorff's Alpha:", round(alpha_nominal, 3))
print("""\n# There is less consistency in relative rating among raters when categorized.
# Moderate consistency persists observed among UG annotators.
# Consistency among PhD annotators is lower.""")

print("-" * 100)
print("\n\nCONCLUSION")
print("\nRaters are less likely to have the same rating for visualizations but there is a slightly consistent pattern in their relative rating.")
print("UG annotators are more likely to have consistent rating than PhD annotators.")