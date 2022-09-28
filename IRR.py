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


def ReadData():
    num = int(input("Please enter the number of judges: "))
    print(num)

    if num >= 1:
        # create data frame from excel sheet
        df1 = pd.read_excel("1.xlsx", sheet_name="RawData")
        np_array1 = df1.to_numpy()
    
    print(np_array1)
    # print(df1)

    if num >= 2:
        # create data frame from excel sheet
        df2 = pd.read_excel("2.xlsx", sheet_name="RawData")
        np_array2 = df2.to_numpy()

        print(np_array2)
       # print(df2)
    if num >= 3:
        # create data frame from excel sheet
        df3 = pd.read_excel("3.xlsx", sheet_name="RawData")
        print(df3)
    if num >= 4:
        # create data frame from excel sheet
        df4 = pd.read_excel("4.xlsx", sheet_name="RawData")
        print(df4)
    if num >= 5:
        # create data frame from excel sheet
        df5 = pd.read_excel("5.xlsx", sheet_name="RawData")
        print(df5)
    if num >= 6:
        # create data frame from excel sheet
        df6 = pd.read_excel("6.xlsx", sheet_name="RawData")
        print(df6)
    if num >= 7:
        # create data frame from excel sheet
        df7 = pd.read_excel("7.xlsx", sheet_name="RawData")
        print(df7)
    if num >= 8:
        # create data frame from excel sheet
        df8 = pd.read_excel("8.xlsx", sheet_name="RawData")
        print(df8)
    print("Krippendorff's alpha for nominal metric: ", krippendorff.alpha(value_counts=[np_array1,np_array2],
                                                                          level_of_measurement="nominal"))

def main():
    SetWorkingDirectory()
    ReadData()


if __name__ == "__main__":
    main()
