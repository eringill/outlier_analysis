# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: egill

import copy
# imports
import sys
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import outliers as o
import regression as r

sys.path.append("/Users/egill/Desktop/CHILDdb/python/")

filename = input("\n\nEnter the path to a csv file containing data you would like to analyze for outliers.\n\n")
age = input("\n\nEnter the age for which you would like to predict an acceptable range of values.\n\n")

data = pd.read_csv(filename)

data = o.add_age(data)

min_a = o.min_age(data)

data_split = o.split_by_age(data)

data_stats = o.calc_stats(data_split, data)

difference = o.test_for_difference(data_split)

stats_merged = o.merge_stats(data_split, data_stats)

data_outliers = o.mark_outliers(stats_merged)

data_z_scores = o.mod_z_score(data_outliers)

data_output = o.df_append(data_z_scores)

# if Kruskal-Wallace test determines medians are not stat different
# linear regression will still help here
if difference > 0.05:
    print("\n\nData medians are not statistically different. Next time point can be predicted based on the last one obtained.\n\n")

else:
    print("\n\nData medians are statistically different. Starting linear regression.\n\n")

no_outliers = o.remove_z_outliers(data_output)

# make df for regression that does not contain age 0 -  causes problems for log regression
# data_stats_regression = data_stats[data_stats['age_rounded'] != 0]
# OR
data_stats_regression = copy.deepcopy(data_stats)

data_stats_regression['age_rounded'] = data_stats_regression['age_rounded'].replace(0, 0.1)

linear_R2, linear_coeff = r.do_regression(data_stats_regression, r.func_linear)

log10_R2, log10_coeff = r.do_regression(data_stats_regression, r.func_log)

ln_R2, ln_coeff = r.do_regression(data_stats_regression, r.func_ln)

best_line = r.find_best_line(linear_R2, log10_R2, ln_R2)

print("\n\nThe predicted median value at age ", str(age), " is ", str(r.return_prediction(best_line, age, linear_coeff,
                                                                                          log10_coeff, ln_coeff)),
      "\n\n")

zero_z_score = r.z_score_ranges(no_outliers)

min_acceptable_range = r.return_prediction(best_line, age, linear_coeff, log10_coeff, ln_coeff) - zero_z_score

max_acceptable_range = r.return_prediction(best_line, age, linear_coeff, log10_coeff, ln_coeff) + zero_z_score

print("\n\nThe predicted acceptable range at age ", str(age), " is from ", str(min_acceptable_range), " to ",
      str(max_acceptable_range), "\n\n")

outlierfile = filename.replace('.csv', '_outliers.csv')

# data_output.to_csv(outlierfile, index = False)

# plot boxplot
fig, ax = plt.subplots()
flierprops = dict(marker='D', markerfacecolor='red', markersize=6, alpha=0.2, linestyle='none')
sns.boxplot(data=data_output, x='age_rounded', y='value', flierprops=flierprops, ax=ax)
ax.set_ylim(-10, 175)
plotname = filename.replace('.csv', '_outliers.png')
# plt.savefig(plotname, format="png")
plt.show()


# plot regression
x = data_stats_regression['age_rounded']
y = data_stats_regression['median']
plt.plot(x, y, 'o')
plt.plot(x, r.func_linear(x, *linear_coeff))
plt.plot(x, r.func_log(x, *log10_coeff))
plt.plot(x, r.func_ln(x, *ln_coeff))
plt.show()
