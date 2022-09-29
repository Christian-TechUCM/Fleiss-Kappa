from ast import Num
import pandas as pd
import os
import krippendorff
import numpy as np
import sys


def SetWorkingDirectory():
    # Ask the user to set the working directory and save as char
    working_directory = input("Please enter the working directory: ")
    # Change the working directory to the one entered by the user
    os.chdir(working_directory)


def ReadData():
    num = int(input("Please enter the number of judges: "))
    print("number of judges entered", num)
    np_array1, np_array2, np_array3, np_array4, np_array5, np_array6, np_array7, np_array8, np_array9, np_array10, np_array11, np_array12, np_array13, np_array14, np_array15 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    if num >= 1:
        # create data frame from excel sheet
        df1 = pd.read_excel("1.xlsx", sheet_name="RawData")
        np_array1 = df1.to_numpy()

    if num >= 2:
        # create data frame from excel sheet
        df2 = pd.read_excel("2.xlsx", sheet_name="RawData")
        np_array2 = df2.to_numpy()

    if num >= 3:
        # create data frame from excel sheet
        df3 = pd.read_excel("3.xlsx", sheet_name="RawData")
        np_array3 = df3.to_numpy()
        print(df3)
    if num >= 4:
        # create data frame from excel sheet
        df4 = pd.read_excel("4.xlsx", sheet_name="RawData")
        np_array4 = df4.to_numpy()
        print(df4)
    if num >= 5:
        # create data frame from excel sheet
        df5 = pd.read_excel("5.xlsx", sheet_name="RawData")
        np_array5 = df5.to_numpy()
        print(df5)
    if num >= 6:
        # create data frame from excel sheet
        df6 = pd.read_excel("6.xlsx", sheet_name="RawData")
        np_array6 = df6.to_numpy()
        print(df6)
    if num >= 7:
        # create data frame from excel sheet
        df7 = pd.read_excel("7.xlsx", sheet_name="RawData")
        np_array7 = df7.to_numpy()
        print(df7)
    if num >= 8:
        # create data frame from excel sheet
        df8 = pd.read_excel("8.xlsx", sheet_name="RawData")
        np_array8 = df8.to_numpy()
        print(df8)
    if num >= 9:
        # create data frame from excel sheet
        df9 = pd.read_excel("9.xlsx", sheet_name="RawData")
        np_array9 = df9.to_numpy()
        print(df9)
    if num >= 10:
        # create data frame from excel sheet
        df10 = pd.read_excel("10.xlsx", sheet_name="RawData")
        np_array10 = df10.to_numpy()
        print(df10)
    if num >= 11:
        # create data frame from excel sheet
        df11 = pd.read_excel("11.xlsx", sheet_name="RawData")
        np_array11 = df11.to_numpy()
        print(df11)
    if num >= 12:
        # create data frame from excel sheet
        df12 = pd.read_excel("12.xlsx", sheet_name="RawData")
        np_array12 = df12.to_numpy()
        print(df12)
    if num >= 13:
        # create data frame from excel sheet
        df13 = pd.read_excel("13.xlsx", sheet_name="RawData")
        np_array13 = df13.to_numpy()
        print(df13)
    if num >= 14:
        # create data frame from excel sheet
        df14 = pd.read_excel("14.xlsx", sheet_name="RawData")
        np_array14 = df14.to_numpy()
        print(df14)
    if num >= 15:
        # create data frame from excel sheet
        df15 = pd.read_excel("15.xlsx", sheet_name="RawData")
        np_array15 = df15.to_numpy()
        print(df15)

    krippendorff_alpha(num, np_array1, np_array2, np_array3, np_array4, np_array5, np_array6, np_array7,
                       np_array8, np_array9, np_array10, np_array11, np_array12, np_array13, np_array14, np_array15)


def krippendorff_alpha(num, np_array1, np_array2, np_array3, np_array4, np_array5, np_array6, np_array7, np_array8, np_array9, np_array10, np_array11, np_array12, np_array13, np_array14, np_array15):
    
    print(num)
    print(np_array1)
    print("np_array2 should be zero: ")
    print(np_array2)
    print("this is a end of array")
   # print (np_array2)
    print("Krippendorff's alpha: ")

    value_counts=np_array1

    print("Krippendorff's alpha for nominal metric: ", krippendorff.alpha(value_counts=value_counts,
                                                                          level_of_measurement="nominal"))
    print("Krippendorff's alpha for interval metric: ", krippendorff.alpha(value_counts=value_counts))
    


def main():
    SetWorkingDirectory()
    ReadData()
if __name__ == "__main__":
    main()
