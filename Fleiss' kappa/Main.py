import openpyxl
import webbrowser
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

def open_website():
    webbrowser.open("https://www.Christianurbina.com")

def delete_empty_rows(data):
    new_data = []
    for row in data:
        if sum(row) != 0:
            new_data.append(row)
    return new_data


def open_file_dialog():
    file_path = filedialog.askopenfilename()
    return file_path


def on_select_file_button_click():
    global file_path
    file_path = open_file_dialog()
    process_file()


def process_file():
    global file_path
    global data
    global num_rows
    global num_cols
    global n
    global k
    global C
    global N
    global kappa
    global result
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.get_sheet_by_name('RawData')

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

    result.set(f'Fleiss kappa: {kappa:.3f}')
    label.pack()


root = tk.Tk()
root.geometry("600x400+200+200")
root.title("Fleiss Kappa Calculation")



# Create a Text widget that will be used to display instructions
instructions = tk.Text(root, wrap=tk.WORD, height=20, width=55)
instructions.pack(side='right', padx=20, pady=20)

# Insert instructions into the Text widget
instructions.insert(
    tk.END, "Instructions:\n\n1. Click the 'Select File' button to choose an Excel file. Note only .xlsx,.xlsm,.xltx,.xltm are accepted. \n2. Make sure the sheet inside the excel sheet is called 'RawData'. \n3. The program should then automatically calculat Fleiss Kappa and display it in the window")
instructions.config(state="disabled")
instructions.pack()

#Selcect File Button
select_file_button = tk.Button(
    root, text="Select File", command=on_select_file_button_click)
select_file_button.pack()

#Contact Developer Button
website_button = tk.Button(root, text="Contact Developer", command=open_website)
website_button.pack(side="bottom", anchor="w")

result = tk.StringVar()
label = tk.Label(root, textvariable=result)
root.mainloop()
