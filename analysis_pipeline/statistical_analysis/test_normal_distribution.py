import pandas as pd
from scipy import stats


print("#" * 100)
print("UG Ratings")
ug_ratings = pd.read_csv("../data/average_rating_ug.csv")

stat, p = stats.shapiro(ug_ratings["mean_rating"].to_list())

print('Statistics=%.3f, p=%.3f' % (stat, p))

alpha = 0.05
if p > alpha:
    print('Normal distribution')
else:
    print('Not normal distribution')
    
print()
print("#" * 100)
print("PhD Ratings")
phd_ratings = pd.read_csv("../data/average_rating_rest.csv")

stat, p = stats.shapiro(phd_ratings["mean_rating"].to_list())

print('Statistics=%.3f, p=%.3f' % (stat, p))

alpha = 0.05
if p > alpha:
    print('Normal distribution')
else:
    print('Not normal distribution')