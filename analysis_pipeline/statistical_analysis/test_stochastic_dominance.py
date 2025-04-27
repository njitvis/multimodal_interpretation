from scipy.stats import mannwhitneyu
import pandas as pd


ug_ratings = pd.read_csv("../data/average_rating_ug.csv")
phd_ratings = pd.read_csv("../data/average_rating_rest.csv")

stat, p = mannwhitneyu(ug_ratings["mean_rating"].to_list(), phd_ratings["mean_rating"].to_list(), method="auto")

print(f'Statistics={stat:.3f}, p={p:.3f}')

print()
print("Given the differing distribution shapes, the result reflects a general shift in rating tendencies between groups, rather than a strict difference in medians.")
alpha = 0.01
if p > alpha:
    print('No ignificant difference between ratings')
else:
    print('Significant difference between ratings')
    

print()
stat, p = mannwhitneyu(phd_ratings["mean_rating"].to_list(), ug_ratings["mean_rating"].to_list(), method="auto", alternative="less")

print(f'Statistics={stat:.3f}, p={p:.3f}')

print()
alpha = 0.01
if p > alpha:
    print('PhDs rated higher than or equal to UG')
else:
    print('PhDs rated lower than equal to UG')