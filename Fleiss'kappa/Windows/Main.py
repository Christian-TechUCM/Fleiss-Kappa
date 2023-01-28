import base64
import openpyxl
import webbrowser
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

instruction = """Instructions:

1. Click the 'Select File' button to choose an Excel file. Note only .xlsx,.xlsm,.xltx,.xltm are accepted.
2. Make sure the sheet inside the excel sheet is called 'RawData'.
3. The program should then automatically calculate Fleiss Kappa and display it in the window.

Note this is the scoring convention for Fleiss' Kappa

< 0	    Poor agreement 
0.01 - 0.20	Slight agreement
0.21 - 0.40	Fair agreement
0.41 - 0.60	Moderate agreement
0.61 - 0.80	Substantial agreement
0.81 - 1.00	Almost perfect agreement"""

your_code = base64.b64encode(b"""


def open_website():
    webbrowser.open("https://www.Christianurbina.com")


def open_wiki():
    webbrowser.open("https://en.wikipedia.org/wiki/Fleiss%27_kappa")

def open_github():
    webbrowser.open("https://github.com/Christian-TechUCM/IRR")


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

# Create a Figure and a set of subplots
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(["Fleiss Kappa"], [kappa])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Value")
    ax.set_title("Fleiss Kappa")

    # Embed the bar graph in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, root)
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    canvas.draw()


root = tk.Tk()
root.geometry("800x400+200+200")
root.title("Fleiss' Kappa Calculation")


# Create a Text widget that will be used to display instructions
instructions = tk.Text(root, wrap=tk.WORD, height=20, width=55)
instructions.pack(side='right', padx=20, pady=20)

# Insert instructions into the Text widget
instructions.insert(
    tk.END, instruction)

instructions.config(state="disabled")
instructions.pack()


# Selcect File Button
select_file_button = tk.Button(
    root, text="Select File", command=on_select_file_button_click)
select_file_button.pack()


# Contact Developer Button
website_button = tk.Button(root, text="Contact Developer ", command=open_website)
website_button.pack(side="bottom", anchor="w")

# GitHub Button
GitHub = tk.Button(root, text="          GitHub           ", command=open_github)
GitHub.pack(side="bottom", anchor="w")

#wiki button
Wiki = tk.Button(root, text="Fleiss' Kappa WIKI   ", command=open_wiki)
Wiki.pack(side="bottom", anchor="w")


result = tk.StringVar()
label = tk.Label(root, textvariable=result)
root.mainloop()

""")

exec(base64.b64decode(your_code))
