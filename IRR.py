from csv import excel
import pandas as pd

excel_file = '1.xlsx'

df =pd.read_excel(excel_file)

print(df.head(2))