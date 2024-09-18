import base64
import openpyxl
import webbrowser
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

instruction = """Instructions:

1. Click the 'Select File' button to choose an Excel file. Note only .xlsx,.xlsm,.xltx,.xltm are accepted.
2. Make sure the sheet inside the excel sheet is called 'RawData'.
3. The program should then automatically calculate Fleiss Kappa and display it in the window.

Note this is the scoring convention for Fleiss' Kappa:

< 0	    Poor agreement 
0.01 - 0.20	Slight agreement
0.21 - 0.40	Fair agreement
0.41 - 0.60	Moderate agreement
0.61 - 0.80	Substantial agreement
0.81 - 1.00	Almost perfect agreement"""

# Open website functions
def open_website():
    webbrowser.open("https://www.Christianurbina.com")


def open_wiki():
    webbrowser.open("https://en.wikipedia.org/wiki/Fleiss%27_kappa")

def open_github():
    webbrowser.open("https://github.com/Christian-TechUCM/IRR")

# Remove empty rows
def delete_empty_rows(data):
    new_data = []
    for row in data:
        if sum(row) != 0:
            new_data.append(row)
    return new_data

# Open file dialog
def open_file_dialog():
    file_path = filedialog.askopenfilename()
    return file_path

# Button click handler
def on_select_file_button_click():
    global file_path
    file_path = open_file_dialog()
    process_file()

# Process Excel file and calculate Fleiss' Kappa
def process_file():
    global file_path
    global data
    global kappa
    global result

    try:
        wb = openpyxl.load_workbook(file_path)
        sheet = wb['RawData']

        data = []
        for row in sheet.iter_rows(values_only=True):
            data_row = []
            for cell in row:
                data_row.append(cell)
            data.append(data_row)

        data = delete_empty_rows(data)

        # Transpose data to get raters' ratings per subject
        num_raters = len(data[0])
        num_subjects = len(data)

        # Calculate Fleiss' Kappa
        # Step 1: Compute p_j for each category j
        p_j = [0] * num_raters
        total_ratings = 0

        for row in data:
            total_ratings += sum(row)
            for j in range(num_raters):
                p_j[j] += row[j]

        p_j = [p / total_ratings for p in p_j]

        # Step 2: Compute P_i for each subject i
        P_i = []
        for row in data:
            sum_row = sum(row)
            if sum_row == 0:  # Skip if there are no ratings
                continue
            P_i.append((sum([x ** 2 for x in row]) - sum_row) / (sum_row * (sum_row - 1)))

        # Step 3: Compute P_bar (average observed agreement)
        P_bar = sum(P_i) / num_subjects

        # Step 4: Compute P_e (expected agreement by chance)
        P_e = sum([p ** 2 for p in p_j])

        # Step 5: Compute Fleiss' Kappa
        kappa = (P_bar - P_e) / (1 - P_e)

        # Display the result
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

    except Exception as e:
        result.set(f"Error: {str(e)}")
        label.pack()

# Initialize the Tkinter app
root = tk.Tk()
root.geometry("800x400+200+200")
root.title("Fleiss' Kappa Calculation")

# Create a Text widget to display instructions
instructions = tk.Text(root, wrap=tk.WORD, height=20, width=55)
instructions.pack(side='right', padx=20, pady=20)

# Insert instructions into the Text widget
instructions.insert(tk.END, instruction)
instructions.config(state="disabled")

# Create Select File Button
select_file_button = tk.Button(root, text="Select File", command=on_select_file_button_click)
select_file_button.pack()

# Developer Contact and GitHub Buttons
website_button = tk.Button(root, text="Contact Developer ", command=open_website)
website_button.pack(side="bottom", anchor="w")

GitHub = tk.Button(root, text="         GitHub         ", command=open_github)
GitHub.pack(side="bottom", anchor="w")

# Fleiss' Kappa Wiki Button
Wiki = tk.Button(root, text="Fleiss' Kappa WIKI  ", command=open_wiki)
Wiki.pack(side="bottom", anchor="w")

# Create label to display Fleiss' Kappa result
result = tk.StringVar()
label = tk.Label(root, textvariable=result)

# Start the Tkinter event loop
root.mainloop()
