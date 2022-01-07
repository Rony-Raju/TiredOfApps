import os
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

vowelList = ['A', 'a', 'E', 'e', 'I', 'i', 'O', 'o', 'U', 'u']


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
    driver.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()

    postings = driver.find_elements(By.CSS_SELECTOR, 'a.atw-ApplyButton')

    applications = [x.get_attribute('href') for x in postings]
    driver.get(applications[0])
    driver.find_element(By.XPATH, '//button[@id="indeedApplyButton"]').click()

    #for preliminary questions
    questions = driver.find_elements(By.XPATH, '//div[@class="ia-Questions-item css-e9ld6l eu4oa1w0"]')
    questions_text = [x.get_attribute('innerHTML') for x in questions]

    for i, x in enumerate(questions_text):
        if "USC" or "Citenship" in x:
            #weird thing to click, because element obscures
            driver.execute_script("arguments[0].click()", questions[i].find_element(By.XPATH, '//input[@value="1"]'))
        elif "sponsorship" or "sponsor" in x:
            driver.execute_script("arguments[0].click()", questions[i].find_element(By.XPATH, '//input[@value="0"]'))

    #next page
    driver.find_element(By.CSS_SELECTOR, "button.ia-continueButton").click()

    #for when they ask for a resume
    header = driver.find_element(By.XPATH, '//h1[@class="ia-BasePage-heading fs-unmask"]')
    header = header.get_attribute('innerHTML')
    print(header)
    if "resume" in header:
        #next page
        driver.find_element(By.CSS_SELECTOR, "button.ia-continueButton").click()

    #for when they ask for past job experiences
    header = driver.find_element(By.XPATH, '//h1[@class="ia-BasePage-heading fs-unmask"]')
    header = header.get_attribute('innerHTML')
    print(header)
    if "past job" in header:
        #next page
        driver.find_element(By.CSS_SELECTOR, "button.ia-continueButton").click()

    #tricky part is the letter
    job = driver.find_element(By.XPATH, '//div[@class="ia-JobHeader-details"]')
    job = job.get_attribute('innerHTML')
    #name of company
    company = job[:job.find(" - ")-1]
    print(company)
    job = driver.find_element(By.XPATH, '//div[@class="ia-JobHeader-title ia-JobHeader-title--withJobDetails"]')
    job = job.get_attribute('innerHTML')
    print(job)
    print(job[0])
    #correct grammar
    if job[0] in vowelList:
        job = 'an ' + job
        print(job)
    else:
        job = 'a ' + job

    print(job)
    #open the coverletter
    print(os.getcwd())
    file = open('TiredOfApps/coverletter.txt', 'r')

    #put these two entries into the coverletter
    for i, x in enumerate(file):
        if i == 1:
            index = x.find('this company')
            first = x[0:index]
            second = x[index+12:]
            x = first + company + ' as ' + job + second
        print(x)
    # for x in applications:
    #     driver.get(x)
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
