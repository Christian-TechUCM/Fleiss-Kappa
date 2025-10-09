import base64
import openpyxl
import webbrowser
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def _normalise_cell(value):
    """Return a numeric representation of a worksheet cell.

    The Fleiss' kappa calculator only operates on numeric inputs.  The Excel
    sheet that feeds the Windows application can, however, contain headers or
    stray whitespace.  This helper trims out empty strings, converts values that
    look like numbers into ``int``\ s and ``float``\ s, and leaves any
    unexpected text untouched so that the caller can decide how to handle it.
    """

    if value is None:
        return None

    if isinstance(value, bool):
        # Treat boolean cells as 0/1 votes.
        return int(value)

    if isinstance(value, (int, float)):
        return int(value) if isinstance(value, float) and value.is_integer() else value

    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return None

        try:
            numeric = float(stripped)
        except ValueError:
            return stripped

        return int(numeric) if numeric.is_integer() else numeric

    return value


def sanitise_rows(rows):
    """Remove headers/blank rows and ensure we only keep numeric data."""

    cleaned_rows = []
    data_started = False

    for row in rows:
        numeric_row = []
        found_text = False

        for cell in row:
            normalised = _normalise_cell(cell)

            if normalised is None:
                continue

            if isinstance(normalised, str):
                found_text = True
                break

            if normalised < 0:
                raise ValueError("Ratings must be non-negative numbers.")

            numeric_row.append(normalised)

        if found_text:
            if data_started:
                raise ValueError(
                    "Found text inside the data range. Please remove headers, comments, or notes from the 'RawData' sheet."
                )

            # Treat leading text rows as headers/instructions and skip them.
            continue

        if numeric_row:
            data_started = True
            cleaned_rows.append(numeric_row)

    return cleaned_rows

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
        # Filter out trailing None values that can appear when Excel rows vary in
        # length. The calculator treats any fully empty row as a separator that
        # should be ignored.
        filtered_row = [cell for cell in row if cell is not None]

        if not filtered_row:
            continue

        new_data.append(filtered_row)

    return new_data


def convert_ratings_to_counts(data, mode="auto"):
    """Convert either raw ratings or an existing counts matrix into counts.

    ``data`` is the sanitised worksheet payload where each row represents a
    single subject.  The historical behaviour expects *raw ratings* (for
    example ``[0, 1, 1, 3]``) and converts them into per-category tallies so
    the Fleiss' Kappa computation can run.  Some users, however, already
    provide an aggregated counts matrix (for example ``[0, 2, 1, 0]``).  This
    helper supports both layouts.

    Args:
        data: Iterable of per-subject rows containing numeric entries.
        mode: ``"auto"`` (default) attempts to infer the layout.  ``"ratings"``
            forces the raw-rating conversion path and ``"counts"`` assumes the
            input is already aggregated.

    Returns:
        A tuple ``(counts_matrix, categories)`` compatible with the remainder
        of the calculator pipeline.
    """

    if mode not in {"auto", "ratings", "counts"}:
        raise ValueError("mode must be one of: 'auto', 'ratings', or 'counts'.")

    if not data:
        return [], []

    def _looks_like_counts_matrix(rows):
        lengths = {len(row) for row in rows}
        if len(lengths) != 1:
            return False

        non_empty_totals = []

        for row in rows:
            for value in row:
                if isinstance(value, float) and not value.is_integer():
                    return False

            total = sum(row)
            if total > 0:
                non_empty_totals.append(total)

        if not non_empty_totals:
            return False

        return len(set(non_empty_totals)) == 1

    treat_as_counts = mode == "counts"

    if mode == "auto":
        treat_as_counts = _looks_like_counts_matrix(data)
    elif mode == "ratings":
        treat_as_counts = False

    if treat_as_counts:
        num_categories = len(data[0])
        categories = list(range(num_categories))
        counts_matrix = [[int(value) for value in row] for row in data]
        return counts_matrix, categories

    categories = []
    category_to_index = {}

    # Discover the set of categories that appear in the raw ratings. We keep
    # the insertion order to provide stable output and to avoid sorting
    # surprises when numeric strings are mixed with integers.

    for row in data:
        for value in row:
            if value is None:
                continue

            if value not in category_to_index:
                category_to_index[value] = len(categories)
                categories.append(value)

    counts_matrix = []

    for row in data:
        counts = [0] * len(categories)
        for value in row:
            if value is None:
                continue

            counts[category_to_index[value]] += 1

        counts_matrix.append(counts)

    return counts_matrix, categories

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

        raw_rows = []
        for row in sheet.iter_rows(values_only=True):
            raw_rows.append([cell for cell in row])

        raw_rows = delete_empty_rows(raw_rows)
        data = sanitise_rows(raw_rows)

        if not data:
            raise ValueError("No data found in worksheet 'RawData'.")

        counts_matrix, categories = convert_ratings_to_counts(data)

        num_subjects = len(counts_matrix)
        num_categories = len(categories)

        row_totals = [sum(row) for row in counts_matrix if sum(row) > 0]

        if not row_totals:
            raise ValueError("Each subject must have at least two ratings.")

        if len(set(row_totals)) != 1:
            raise ValueError(
                "Each subject must be scored by the same number of raters. Please check for missing values in 'RawData'."
            )

        num_raters = row_totals[0]

        if num_raters <= 1:
            raise ValueError("At least two ratings per subject are required to compute Fleiss' Kappa.")

        # Calculate Fleiss' Kappa
        # Step 1: Compute p_j for each category j
        p_j = [0] * num_categories
        total_ratings = sum(row_totals)

        for row in counts_matrix:
            for j in range(num_categories):
                p_j[j] += row[j]

        p_j = [p / total_ratings for p in p_j]

        # Step 2: Compute P_i for each subject i
        P_i = []
        for row in counts_matrix:
            sum_row = sum(row)
            if sum_row == 0:  # Skip if there are no ratings
                continue

            row_square_sum = sum([x ** 2 for x in row])
            P_i.append((row_square_sum - sum_row) / (sum_row * (sum_row - 1)))

        if not P_i:
            raise ValueError("Unable to compute Fleiss' Kappa because no subject has at least two ratings.")

        # Step 3: Compute P_bar (average observed agreement)
        P_bar = sum(P_i) / len(P_i)

        # Step 4: Compute P_e (expected agreement by chance)
        P_e = sum([p ** 2 for p in p_j])

        if P_e == 1:
            raise ValueError("Cannot compute Fleiss' Kappa when expected agreement is 1.")

        # Step 5: Compute Fleiss' Kappa
        kappa = (P_bar - P_e) / (1 - P_e)

        # Display the result
        result.set(f"Fleiss kappa: {kappa:.3f}")
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
