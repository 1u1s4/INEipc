'''
# prueba usar R en py
import os
os.environ["R_HOME"] = r"C:\Program Files\R\R-4.2.1" # change as needed
import rpy2.robjects.packages as rpackages

devtools = rpackages.importr('devtools')
devtools.install_github("1u1s4/funcionesINE")
'''
import xlsxwriter

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Expenses01.xlsx')
for j in range(3):
    worksheet = workbook.add_worksheet()

    # Some data we want to write to the worksheet.
    expenses = (
        ['Rent', 1000],
        ['Gas',   100],
        ['Food',  300],
        ['Gym',    50],
    )

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Iterate over the data and write it out row by row.
    for item, cost in (expenses):
        worksheet.write(row, col,     item)
        worksheet.write(row, col + 1, cost)
        row += 1

workbook.close()