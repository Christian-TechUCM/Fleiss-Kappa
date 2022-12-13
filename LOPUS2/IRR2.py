import openpyxl

# Open the Excel workbook and select the active sheet
wb = openpyxl.load_workbook('IRR.xlsx')
sheet = wb.get_sheet_by_name('Test')

# Read the data from the sheet into a 2D list
data = []
for row in sheet.rows:
    data_row = []
    for cell in row:
        data_row.append(cell.value)
    data.append(data_row)

# Calculate the number of rows and columns in the data
num_rows = len(data)
num_cols = len(data[0])

# Initialize some variables
n = 0
k = num_cols
C = 0
N = 0

# Loop over the rows and columns of the data
for i in range(num_rows):
    for j in range(num_cols):
        n += 1
        N += data[i][j]
        C += data[i][j] * (data[i][j] - 1)

# Calculate the mean number of ratings per item
mean_n = N / n

# Calculate the variance of the number of ratings per item
var_n = (C - n * mean_n * (mean_n - 1)) / (n - 1)

# Calculate Fleiss' kappa
kappa = (mean_n * (k - 1) - var_n) / (mean_n * (k - 1))

# Print the result
print(f'Fleiss kappa: {kappa:.3f}')
