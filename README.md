#ReadMe

This code is a Python script that calculates Fleiss Kappa, a statistical measure of inter-rater agreement, on data from an Excel file.

## Fleiss Kappa Calculator

A program to calculate Fleiss Kappa from an excel file.

### Instructions:
1. Click the 'Select File' button to choose an Excel file. Note only .xlsx,.xlsm,.xltx,.xltm are accepted.
2. Make sure the sheet inside the excel sheet is called 'RawData'.
3. The program should then automatically calculate Fleiss Kappa and display it in the window.

Note this is the scoring convention for Fleiss' Kappa

< 0	    Poor agreement 
0.01 - 0.20	Slight agreement
0.21 - 0.40	Fair agreement
0.41 - 0.60	Moderate agreement
0.61 - 0.80	Substantial agreement
0.81 - 1.00	Almost perfect agreement

### Dependdencies:
base64
openpyxl
webbrowser
tkinter
matplotlib


### Fleiss Kappa

Fleiss' kappa (named after Joseph L. Fleiss) is a statistical measure for assessing the reliability of agreement between a fixed number of raters when assigning categorical ratings to a number of items or classifying items. This contrasts with other kappas such as Cohen's kappa, which only work when assessing the agreement between not more than two raters or the intra-rater reliability (for one appraiser versus themself). The measure calculates the degree of agreement in classification over that which would be expected by chance.

Fleiss' kappa can be used with binary or nominal-scale. It can also be applied to Ordinal data (ranked data): the MiniTab online documentation [1] gives an example. However, this document notes: "When you have ordinal ratings, such as defect severity ratings on a scale of 1–5, Kendall's coefficients, which account for ordering, are usually more appropriate statistics to determine association than kappa alone." Keep in mind however, that Kendall rank coefficients are only appropriate for rank data.

More can be found here
https://en.wikipedia.org/wiki/Fleiss%27_kappa#:~:text=Fleiss%27%20kappa%20(named%20after%20Joseph,of%20items%20or%20classifying%20items.
