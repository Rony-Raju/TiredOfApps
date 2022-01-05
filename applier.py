import os
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver



def indeed():
    driver = webdriver.Firefox()
    driver.get('https://www.indeed.com/')
    login = driver.find_element(By.XPATH, '//div[@class="gnav-header-16i8ao9 eu4oa1w0"]')
    login.click()
    email = driver.find_element(By.XPATH, '//input[@id="ifl-InputFormField-3"]')
    email.send_keys('rony.raju.hsi@gmail.com')
    submit = driver.find_element(By.XPATH, '//button[@class="css-rhczsh e8ju0x51"]')
    submit.click()
    password = driver.find_element(By.XPATH, '//input[@id="ifl-InputFormField-126"]')
    password.send_keys('')
    submit = driver.find_element(By.XPATH, '//button[@aria-label="Save job"]')
    submit.click()

    jobs = driver.find_element(By.XPATH, '//div[@class="icl-u-lg-hide is-embedded"]')
    jobs.click()

indeed()


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
