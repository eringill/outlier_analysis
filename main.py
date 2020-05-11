# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: egill

# imports
import sys
import pandas as pd
import matplotlib.pyplot as plt
import statistics as stat
import seaborn as sns
import scipy.stats as sstats
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import copy

sys.path.append("/Users/egill/Desktop/CHILDdb/python/")

filename = input("\n\nEnter the path to a csv file containing data you would like to analyze for outliers.\n\n")
age = input("\n\nEnter the age for which you would like to predict an acceptable range of values.\n\n")

data = pd.read_csv(filename)

data = add_age(data)

min_a = min_age(data)

data_split = split_by_age(data)

data_stats = calc_stats(data_split, data)

difference = test_for_difference(data_split)

stats_merged = merge_stats(data_split, data_stats)

data_outliers = mark_outliers(stats_merged)

data_z_scores = mod_z_score(data_outliers)

data_output = df_append(data_z_scores)

# if Kruskal-Wallace test determines medians are not stat different
if difference > 0.05:
    print(
        "Data medians are not statistically different. Next time point can be predicted based on the last one obtained.")

else:
    print("\n\nData medians are statistically different. Starting linear regression.\n\n")
    no_outliers = remove_z_outliers(data_output)

# make df for regression that does not contain age 0 -  causes problems for log regression
# data_stats_regression = data_stats[data_stats['age_rounded'] != 0]
# OR
data_stats_regression = copy.deepcopy(data_stats)

data_stats_regression['age_rounded'] = data_stats_regression['age_rounded'].replace(0, 0.1)

linear_R2, linear_coeff = do_regression(func_linear)

log10_R2, log10_coeff = do_regression(func_log)

ln_R2, ln_coeff = do_regression(func_ln)

best_line = find_best_line(linear_R2, log10_R2, ln_R2)

print("\n\nThe predicted median value at age ", str(age), " is ", str(return_prediction()), "\n\n")

zero_z_score = z_score_ranges()

min_acceptable_range = return_prediction() - zero_z_score

max_acceptable_range = return_prediction() + zero_z_score

print("\n\nThe predicted acceptable range at age ", str(age), " is from ", str(min_acceptable_range), " to ", str(max_acceptable_range), "\n\n")

outlierfile = filename.replace('.csv', '_outliers.csv')

data_output.to_csv(outlierfile, index = False)

#plot boxplot
fig, ax = plt.subplots()
flierprops = dict(marker='D', markerfacecolor='red', markersize=6, alpha = 0.2, linestyle = 'none')
sns.boxplot(data = data_output, x = 'age_rounded', y = 'value', flierprops = flierprops, ax = ax)
ax.set_ylim(-10,175)
plotname = filename.replace('.csv', '_outliers.png')
plt.savefig(plotname, format="png")
plt.show()

# plot regression
plt.plot(x, y, 'o')
plt.plot(x, func(x, *popt))
