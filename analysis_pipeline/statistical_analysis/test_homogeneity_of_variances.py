 
from scipy.stats import levene
import pandas as pd


ug_ratings = pd.read_csv("../data/average_rating_ug.csv")
phd_ratings = pd.read_csv("../data/average_rating_rest.csv")
 
alpha = 0.05
w_stats, p_value = levene(ug_ratings["mean_rating"].to_list(), phd_ratings["mean_rating"].to_list(),
                          center='mean')
 
if p_value > alpha:
    print("Variance among groups is equal -- homogeneity of variances")
else:
    print("Variance among groups is not equal -- heterogeneity of variances")