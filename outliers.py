# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: egill

# imports
import pandas as pd
import scipy.stats as sstats
import statistics as stat

# functions
def add_age(data_f):
    data_f['age'] = data_f['age_in_days'] / 365
    data_f['age_rounded'] = round(data_f['age'])
    return data_f


def min_age(data_f):
    return min(data_f['age_rounded'])


# split all data frames by age to calculate age-specific IQRs
def split_by_age(data_f):
    data_split = [i for _, i in data_f.groupby('age_rounded')]
    return data_split


# Find median, IQR, range of non-outlier datapoints for each age
def calc_stats(df_list, data_f):
    stats = []
    colnames = ['age_rounded', 'median', 'lower', 'upper']
    table = pd.DataFrame()
    age = min_age(data_f)
    for i in df_list:
        if len(i) > 5:  # must modify function so that stats are only generated with min of 5 samples
            stats.append(age)
            stats.append(stat.median(i['value']))
            IQR = (i['value'].describe()[6] - i['value'].describe()[4])
            stats.append(i['value'].describe()[4] - (1.5 * IQR))
            stats.append(i['value'].describe()[6] + (1.5 * IQR))
            stats_df = pd.DataFrame(stats).T
            table = table.append(stats_df, ignore_index=True)
        age += 1
        stats = []
    table.columns = colnames
    return table


# merge stats with dataframes for transperancy when conducting outlier analysis
def merge_stats(df_list, stats):
    df_list_merged = []
    for i in df_list:
        i = i.merge(stats)
        df_list_merged.append(i)
    return df_list_merged


# determine if each row is an outlier based on IQR method
def is_outlier(row):
    if row['value'] < row['lower']:
        return True
    elif row['value'] > row['upper']:
        return True
    else:
        return False


# mark IQR outliers in data frame
def mark_outliers(df_list):
    for i in df_list:
        if i.empty:
            pass
        else:
            i['outlier'] = i.apply(lambda row: is_outlier(row), axis=1)
    return df_list


# calculate modified z-score for each data point
def mod_z_score(df_list):
    for i in df_list:
        if i.empty:
            pass
        else:
            median = stat.median(i['value'])
            MAD = sstats.median_absolute_deviation(i['value'])
            i['mod_z_score'] = (0.6745 * (i['value'] - median) / MAD)
    return df_list


# merge all dataframes back together
def df_append(df_list):
    big_df = pd.DataFrame()
    for i in df_list:
        big_df = big_df.append(i, ignore_index=True, sort=True)
    return big_df


# test to see if medians of data for ages are statistically different from
# each other using Kruskal-Wallis test. If so, perform regression. If not,
# predict next age measurement range based on age 6.
# Kruskal-Wallis makes assumption that samples are independent. In this case
# they are not. Am using this test as a proxy for performing more complicated
# stats.

def test_for_difference(df_list):
    meds = "sstats.kruskal("
    for i in range(len(df_list)):
        meds = meds + "list(df_list[" + str(i) + "]['value']), "
    meds = meds[:-2]
    meds = meds + ')'
    return eval(meds)[1]


# find best fit line.
def remove_z_outliers(data_f):
    data_f['z_outlier'] = abs(data_f['mod_z_score']) > 3.5
    return data_f[data_f['z_outlier'] == False]
