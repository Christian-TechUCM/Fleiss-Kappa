import pandas as pd


def ReadData():
   
   #Read multiple excel files and and store them in a matrix
    #Read the first excel file from testfiles folder
    df1 = pd.read_excel(r'C:\Users\urbin\Documents\Code\COPUS-IRR\Testfiles\1.xlsx', sheet_name='Sheet1')
    #Read the second excel file from testfiles folder
    df2 = pd.read_excel(r'C:\Users\urbin\Documents\Code\COPUS-IRR\Testfiles\2.xlsx', sheet_name='Sheet1')

    #Create a list of dataframes
    df_list = [df1, df2]

    print(df_list)





def main():
    ReadData()


if __name__ == "__main__":
    main()
