Outlier_analysis:
============
### Methods to automatically parse longitudinal numeric data for outliers.

INPUT:
-------

1. You will be asked to enter the path to a .csv file that you would like to analyze for outliers.
2. You will be asked to enter an age for which you would like to predict the median and range
3. The .csv file must contain a column labeled *'age_in_days'* and a column labeled *'values'*
4. Test data have been provided if you would like to observe the behavior of the program. Simply hit the <enter> key when
asked for input.

The code will determines outliers for any numerical dataset using the < Q1 - 1.5 * IQR OR > Q3 + 1.5 * IQR method
and the modified z-score method. Outliers are determined separately for each age.

OUTPUT:
---------

1. a .csv file containing a column called "outlier" that contains boolean values for each observation (IQR method)
and a column called "z_outlier" that contains boolean values for each observation (modified z-score method) will be generated in the same directory as the input .csv file. It will have the same name as the input file with the suffix *"_outliers.csv"*.
2. a .png file containing a plot of data outliers as determined by both methods will be generate in the same directory as the input .csv file. It will have the same name as the input .csv file with the suffix *'_outliers.png'*
3. If medians of values for ages are statistically different from each other (Kruskall-Wallis test), regression
is performed on the medians of ages 1, 3 and 5 with modified z-score outliers removed. Regression is performed using 
untransformed data, log10 and ln data to determine the best fit line. A prediction of the median
and acceptable range will then be given for a user-input age. These are printed to the terminal window.
4. A plot of the linear regression results is also generated.
