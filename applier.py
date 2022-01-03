import os
from fpdf import FPDF
from selenium import webdriver

driver = webdriver.Firefox()

def letterEdit(company, position):
    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size = 11)
    file = open("coverletter.txt", "r")

    for i, x in enumerate(file):

        print(x)
        pdf.cell(200, 10, txt = x, ln = 1, align = 'L')

    pdf.output("test.pdf")
# submissions = {
#     "resume": "",
#     "coverletter": "",
#     "references" : ""
# }


dir = 'F:\\Dropbox\\UNT'
items = list(os.listdir(dir))
for i in items:
    print(i)

letterEdit("Bimbleton Corp", "developer")
