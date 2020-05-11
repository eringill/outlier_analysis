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

# functions

# linear function (y = mx + b)
def func_linear(t, a, c):
    return(a * t + c)

# ln function (y = (ln(x)) + b)
def func_log(t, a, c):
    return (a * np.log10(t) + c)

# log10 function (y = (log10(x) + b)
def func_ln(t, a, c):
    return (a * np.log(t) + c)

# perform linear regression using given function
def do_regression(df, func):
    x = df['age_rounded'].tolist()
    x = np.array(x)
    y = df['median'].tolist()
    y = np.array(y)
    popt, pcov = (curve_fit(func, x, y))
    y_hat = func(x, *popt)
    # popt = optimized equations coefficients
    # pcov = covariance
    # mean_abs_error = np.mean(np.absolute(y_hat - y))
    # mean_squ_error = np.mean(np.absolute((y_hat - y) **2))
    r_score = r2_score(y_hat, y)
    # print(r_score)
    return (r_score, popt)

# determine which regression method gives best line by examining R2 values
def find_best_line(r2_1, r2_2, r2_3):
    bestr2 = ''
    r2 = 0
    if r2_1 > r2_2:
        if r2_1 > r2_3:
            bestr2 = "The best line is fit to non-transformed data, R2= " + str(r2_1)
            r2 = linear_R2
    if r2_2 > r2_1:
        if r2_2 > r2_3:
            bestr2 = "The best line is fit to log10 data, R2= " + str(r2_2)
            r2 = log10_R2
    if r2_3 > r2_1:
        if r2_3 > r2_2:
            bestr2 = "The best line is fit to ln data, R2= " + str(r2_3)
            r2 = ln_R2
    print(bestr2)
    return (r2)

# predict median value for user input age
def return_prediction():
    if best_line == linear_R2:
        return (func_linear(int(age), *linear_coeff))
    if best_line == log10_R2:
        return (func_log(int(age), *log10_coeff))
    if best_line == ln_R2:
        return (func_ln(int(age), *ln_coeff))

# return range for acceptable values by examining range of previous
# acceptable values, dividing it in 2, then adding and subtracting that
# number from the predicted median
def z_score_ranges():
    ranges = []
    colnames = ['age_rounded', 'min', 'max', 'diff']
    table = pd.DataFrame()
    for i in np.unique(no_outliers['age_rounded']):
        age_df = no_outliers[no_outliers['age_rounded'] == i]
        minimum = min(age_df['value'])
        maximum = max(age_df['value'])
        diff = maximum - minimum
        ranges.append(i)
        ranges.append(minimum)
        ranges.append(maximum)
        ranges.append(diff)
        ranges_df = pd.DataFrame(ranges).T
        table = table.append(ranges_df, ignore_index=True)
        ranges = []
    table.columns = colnames
    max_diff = max(table['diff'])
    max_diff_split = max_diff/2
    return(max_diff_split)