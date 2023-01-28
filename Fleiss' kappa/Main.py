import openpyxl
import tkinter as tk
from tkinter import filedialog

def delete_empty_rows(data):
    new_data = []
    for row in data:
        if sum(row) != 0:
            new_data.append(row)
    return new_data

def open_file_dialog():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()
    return file_path

file_path = open_file_dialog()
wb = openpyxl.load_workbook(file_path)
sheet = wb.get_sheet_by_name('Test')

data = []
for row in sheet.rows:
    data_row = []
    for cell in row:
        data_row.append(cell.value)
    data.append(data_row)

data = delete_empty_rows(data)

num_rows = len(data)
num_cols = len(data[0])

n = 0
k = num_cols
C = 0
N = 0

for i in range(num_rows):
    for j in range(num_cols):
        n += 1
        N += data[i][j]
        C += data[i][j] * (data[i][j] - 1)

mean_n = N / n
var_n = (C - n * mean_n * (mean_n - 1)) / (n - 1)

kappa = (mean_n * (k - 1) - var_n) / (mean_n * (k - 1))

root = tk.Tk()
root.title("Fleiss Kappa Calculation")
result = tk.StringVar()
result.set(f'Fleiss kappa: {kappa:.3f}')
label = tk.Label(root, textvariable=result)
label.pack()
root.mainloop()
