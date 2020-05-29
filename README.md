Outlier_analysis
Methods to automatically parse longitudinal numeric data for outliers.

OUTPUT DESCRIPTION:

Determines outliers for any numerical dataset using the < Q1 - 1.5 * IQR OR > Q3 + 1.5 * IQR method
and the modified z-score method. Outliers are determined separately for each age.

-Prints the number of outliers in a dataset to the terminal window

-Saves a .csv file containing a column called "outlier" that contains boolean values for each observation (IQR method)
and a column called "z_outlier" that contains boolean values for each observation (modified z-score method)

-Saves a .png file containing a plot of data outliers as determined by both Methods

-If medians of values for ages are statistically different from each other (Kruskall-Wallis test), linear regression
is performed on the medians of ages 1, 3 and 5 with modified z-score outliers removed. Regression is performed using 
unmodified data, log10 and ln data to determine the best fit line. A prediction of the median
and acceptable range will then be given for a user-input age. These are printed to the terminal window.

-A plot of the linear regression results is also generated.

INSTRUCTIONS:

outliers.py can be executed in a BASH shell by typing python outliers.py
1. You will be asked to enter the path to a .csv file that you would like to analyze for outliers.
2. You will be asked to enter an age for which you would like to predict the median and range