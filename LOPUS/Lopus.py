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
    np_array1, np_array2 = 0, 0

    if num >= 1:
        # create data frame from excel sheet
        df1 = pd.read_excel("1.xlsx", sheet_name="RawData")
       # np_array1 = df1
        df1 = pd.DataFrame(data=df1)
        df1_transposed = df1.T
        np_array1 = df1_transposed.to_numpy()
        print(np_array1)

    if num >= 2:
        # create data frame from excel sheet
        # df2 = pd.read_excel("2.xlsx", sheet_name="RawData")
        #np_array2 = df2.to_numpy()

        # create data frame from excel sheet
        df2 = pd.read_excel("2.xlsx", sheet_name="RawData")
       # np_array1 = df1
        df2 = pd.DataFrame(data=df2)
        df2_transposed = df2.T
        np_array2 = df2_transposed.to_numpy()
        print(np_array2)

        value_counts = np.concatenate((np_array1, np_array2))
        print(value_counts)

        print("Krippendorff's alpha for nominal metric: ", krippendorff.alpha(value_counts=value_counts,
                                                                              level_of_measurement="Nominal"))
        print("Krippendorff's alpha for interval metric: ",
          krippendorff.alpha(value_counts=value_counts))
          

        


def main():
    SetWorkingDirectory()
    ReadData()


if __name__ == "__main__":
    main()
