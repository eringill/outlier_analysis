# -*- coding: utf-8 -*-
# author: egill

# imports
import copy
import sys
import matplotlib.pyplot as plt
import pandas as pd
import outliers as o
import regression as r
import plotnine as p9
import warnings

# prevent plot warnings from printing
warnings.filterwarnings('ignore')

# functions
def get_filename():
    print("\n\nEnter the path to a csv file containing data you would like to analyze for outliers.\n\n")
    filename = input()
    if filename == "" or filename == "\n" or filename is None:
        filename = "data/test_data.csv"
    return filename


def get_age():
    print("\n\nWould you like to predict an acceptable range of values for an upcoming time point? (y/n)\n\n")
    reply = input().lower()
    if reply == 'y':
        print("\n\nEnter the age for which you would like to predict an acceptable range of values.\n\n")
        age = input()
        if age == "" or age == "\n" or age is None or type(age) != int:
            age = 4
        return age
    else:
        exit()
    


# get .csv filename from user
filename = get_filename()

# open file
data = pd.read_csv(filename)

# calculate age in years as float, then as rounded number
print('\n\nCalculating age in years for each sample...\n\n')
data = o.add_age(data)

# find minimum age in dataset
min_a = o.min_age(data)

# split dataframe into list of dataframes by age
data_split = o.split_by_age(data)

# calculate median, lower and upper range of expected values for each age
# using IQR method. Save this as separate dataframe.
print('\n\nCalculating medians and ranges of expected values using IQR method...\n\n')
data_stats = o.calc_stats(data_split, data)

# see if there is a significant difference between ages using Kruskal-Wallis
# test
difference = o.test_for_difference(data_split)

# merge statistics dataframe with dataframe containing observation data
stats_merged = o.merge_stats(data_split, data_stats)

# mark IQR outliers on each dataframe in list of observation dataframes
print('\n\nAnnotating IQR outliers...\n\n')
data_outliers = o.mark_outliers(stats_merged)

# calculate the modified z-score of each data point
print('\n\nCalculating modified z-scores...\n\n')
data_z_scores = o.mod_z_score(data_outliers)

# merge all dataframes in list back together
data_output = o.df_append(data_z_scores)

# mark modified z-score outliers in merged dataframe
print('\n\nAnnotating modified z-score outliers...\n\n')
data_output = o.z_outliers(data_output)

# save csv file
outlierfile = filename.replace('.csv', '_outliers.csv')

print('\n\nWriting output file...\n\n')
data_output.to_csv(outlierfile, index = False)

# plot overlay of IQR and mod-Z score outliers
print('\n\nGenerating plot of outliers...\n\n')
p = (p9.ggplot(data=data_output, mapping=p9.aes(x='age_rounded', y='value', group = 'age_rounded'))
    + p9.geom_jitter(mapping=p9.aes(color = 'z_outlier', outlier_alpha = 0.1))
    + p9.geom_boxplot(outlier_size=0, outlier_stroke=0)
    + p9.ggtitle("Outliers detected via the IQR method (boxplot)\nand modified z-score method (dotplot)")
    + p9.ylim(-10, 175)
)
print(p)
plotfile = filename.replace('.csv', '_outlierplot')
p9.ggsave(plot = p, filename = plotfile)


# ask user for age to predict range of values
age = get_age()

# if Kruskal-Wallace test determines medians are not stat different
# linear regression will still help here
if difference > 0.05:
    print(
        "\n\nData medians are not statistically different. Next time point can be predicted based on the last one "
        "obtained...\n\n")

else:
    print("\n\nData medians are statistically different. Starting linear regression...\n\n")

# remove modified z-score outliers before performing regression
no_outliers = o.remove_z_outliers(data_output)

# make a deep copy of data stats so the original doesn't get changed
data_stats_regression = copy.deepcopy(data_stats)

# only keep ages 1, 3 and 5 for regression
data_stats_regression = data_stats_regression[data_stats_regression.age_rounded.isin([1, 3, 5])]

# find R2 and formula coefficients for regression using straight line
linear_R2, linear_coeff = r.do_regression(data_stats_regression, r.func_linear)

# find R2 and formula coefficients for regression using log10 function (y = (log10(x) + b)
log10_R2, log10_coeff = r.do_regression(data_stats_regression, r.func_log)

# find R2 and formula coefficients for regression using ln function (y = (ln(x) + b)
ln_R2, ln_coeff = r.do_regression(data_stats_regression, r.func_ln)

# determine best-fit line using R2 values
best_line = r.find_best_line(linear_R2, log10_R2, ln_R2)

# use best-fit line coefficients to predict median value at age given by user
print("\n\nThe predicted median value at age ", str(age), " is ", str(r.return_prediction(best_line, age, linear_coeff,
                                                                                          log10_coeff, ln_coeff)),
      "\n\n")

# find the largest numeric range allowed by modified z-score outlier detection method,
# divide the range by 2, center the predicted median at the middle, then add half the range
# to the median to find max, subtract half the range to get min
zero_z_score = r.z_score_ranges(no_outliers)

min_acceptable_range = r.return_prediction(best_line, age, linear_coeff, log10_coeff, ln_coeff) - zero_z_score

max_acceptable_range = r.return_prediction(best_line, age, linear_coeff, log10_coeff, ln_coeff) + zero_z_score

print("\n\nThe predicted acceptable range at age ", str(age), " is from ", str(min_acceptable_range), " to ",
      str(max_acceptable_range), "\n\n")


# plot regression
print('\n\nGenerating regression plot...\n\n')
x = data_stats_regression['age_rounded']
y = data_stats_regression['median']
plt.plot(x, y, 'o')
plt.plot(x, r.func_linear(x, *linear_coeff))
plt.plot(x, r.func_log(x, *log10_coeff))
plt.plot(x, r.func_ln(x, *ln_coeff))
plt.title("Regression performed on medians of age 1, 3 and 5\ndata with outliers removed")
plt.show()


