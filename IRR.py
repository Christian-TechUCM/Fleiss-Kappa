import os
import pandas as pd

data = pd.read_excel (r'C:\Users\urbin\Documents\Code\COPUS-IRR\Testfiles\2.xlsx')
df = pd.DataFrame(data, columns=['L','Ind','CG','WG','OG','AnQ','SQ','WC','Prd','SP','T/Q','W','O','Lec','RtW','FUp','PQ','CQ','AnQ','MG','1o1','D/V','Adm','W','O'])
print (df)