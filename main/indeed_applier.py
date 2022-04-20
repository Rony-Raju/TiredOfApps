from methods.indeed_postings import indeed_postings
from methods.indeed_login import indeed_login
from fpdf import FPDF



def indeed(options, service):
    driver = indeed_login(options, service)
    indeed_postings(driver)
    driver.close()
    return
    
   


# def letterEdit(company, position):
#     pdf = FPDF()

#     pdf.add_page()

#     pdf.set_font("Arial", size = 11)
#     file = open("coverletter.txt", "r")

#     for i, x in enumerate(file):

#         print(x)
#         pdf.cell(200, 10, txt = x, ln = 1, align = 'L')

#     pdf.output("test.pdf")


# submissions = {
#     "resume": "",
#     "coverletter": "",
#     "references" : ""
# }


