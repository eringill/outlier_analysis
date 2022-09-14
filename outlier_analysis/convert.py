import os
import pandas as pd

_ROOT = os.path.abspath(os.path.dirname(__file__))

def conv_xlsx_to_csv():
    print("\n\nEnter the path to the xlsx file you would like to convert to csv (for input into the outlier_analysis program).\n\n")
    filename = input()

    # open file
    extension = filename.split('.')[-1]
    if (extension != "xlsx"):
        print("\nNot an xlsx file. Exiting.")
        exit()
    else:
        filename = os.path.join(_ROOT, 'data', filename) # Fix FileNotFoundError.
        data = pd.read_excel(filename)
        # For each column that isn't age_in_days, make a new csv file for it and change the column name to 'value'.
        print("\nNew csv files:")
        newFilenames = []
        for col in data.columns:
            if (col != 'age_in_days'):
                newData = (data[['age_in_days', col]]).rename(columns={col:'value'})
                newFilename = os.path.splitext(filename)[0] + "_" + col + ".csv"
                newData.to_csv(newFilename, index=False)
                newFilenames.append(newFilename)
                print("\t"+newFilename)
    return newFilenames


conv_xlsx_to_csv()