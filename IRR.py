from operator import index
import pandas as pd
import os
import krippendorff
import numpy as np



def SetWorkingDirectory():
    # Ask the user to set the working directory and save as char
    working_directory = input("Please enter the working directory: ")
    # Change the working directory to the one entered by the user
    os.chdir(working_directory)

   # Set the working directory
   # os.chdir(r'C:\Users\urbin\Documents\Code\COPUS-IRR\Testfiles')


def ReadData():
    # Loop through the files in the working directory and read excel sheets into a dataframe using specified columns
    field = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
    
    for file in os.listdir():
        if file.endswith(".xlsx"):
            
            df = pd.read_excel(file,sheet_name='50 min class', usecols=field, skiprows=9)
            df = df.dropna()
            df.to_numpy()
            print(df)

def krippendorff_alpha(data, level_of_measurement):
    return krippendorff.alpha(data, level_of_measurement=level_of_measurement)
    


# , usecols=fields ['L','Ind','CG','WG','OG','AnQ','SQ','WC','Prd','SP','T/Q','W','O','Lec','RtW','FUp','PQ','CQ','AnQ','MG','1o1','D/V','Adm','W','O']


def main():
    SetWorkingDirectory()
    ReadData()


if __name__ == "__main__":
    main()
