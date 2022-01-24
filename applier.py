import os
from datetime import datetime
import time
from fpdf import FPDF
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
vowelList = ['A', 'a', 'E', 'e', 'I', 'i', 'O', 'o', 'U', 'u']

def next(driver):
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for text in buttons:

        words = text.get_attribute('innerHTML')
        if 'Continue' in words or 'application' in words:
            text.click()
            print('going to next page')
            return

def indeed(options, service):
    driver = Firefox(service=service, options=options)
    driver.get('https://www.indeed.com/')
        #find the user icon and click on saved jobs
    driver.find_element(By.XPATH,'//div[@class="gnav-header-5fxd2s-Box eu4oa1w0"]').click()
    driver.find_element(By.XPATH,'//a[@data-gnav-element-name="MyJobs"]').click()

    postings = driver.find_elements(By.CSS_SELECTOR, 'a.atw-ApplyButton')

    applications = [x.get_attribute('href') for x in postings]
    for x in applications:
        time.sleep(0.5)
        driver.get(x)
        driver.find_element(By.XPATH, '//button[@id="indeedApplyButton"]').click()
        header = ''
        link = x
        while("Please Review" not in header):
            time.sleep(0.5)
            print(f"header is {header}\n\n\n")
            try:
                #get the header each time and behave accordingly
                header = driver.find_element(By.XPATH, '//h1[@class="ia-BasePage-heading fs-unmask"]')
                header = header.get_attribute('innerHTML')
                print(f"header is {header}\n\n\n")
                #for preliminary questions
                if "Questions" in header:
                    questions = driver.find_elements(By.XPATH, '//div[@class="ia-Questions-item css-e9ld6l eu4oa1w0"]')
                    questions_text = [x.get_attribute('innerHTML') for x in questions]

                    for i, text in enumerate(questions_text):
                        print(text)
                        if "sponsorship" in text or "sponsor" in text:
                            try:
                                driver.execute_script("arguments[0].click()", questions[i].find_element(By.XPATH, '//input[@value="0"]'))
                            except Exception:
                                pass
                        elif "education" in text:
                            driver.execute_script("arguments[0].click()", questions[i].find_element(By.XPATH, '//input[@value="Bachelor\'s"]'))
                        elif "experience" in text:
                            #find the selection and select it
                            try:
                                answers = questions[i].find_elements(By.XPATH, '//input[@type="radio"]')
                                for selection in answers:
                                    choice = selection.find_element(By.CSS_SELECTOR, "span.css-19kaor0 eu4oa1w0")
                                    if '3' in choice.get_attribute('innerHTML'):
                                        selection.click()
                                        continue
                            except Exception:
                                if 'value=""' in text:
                                    print(f'i is {i}')
                                    response = questions[i].find_element(By.XPATH, '//input[@value=""]')
                                    response.send_keys(Keys.CONTROL+'a')
                                    response.send_keys('3')
                                continue

                        elif "salary" in text:
                            questions[i].find_element(By.CSS_SELECTOR, "div.css-d8iwdi e1jgz0i3").send_keys('65000 - 85000')
                        else:
                            print('weird questions just say yes')
                            #weird thing to click, because element obscures
                            try:
                                driver.execute_script("arguments[0].click()", questions[i].find_element(By.XPATH, '//input[@value="1"]'))
                            except Exception:
                                pass

                    #next page
                    next(driver)
                    continue

                #for the letter
                elif "Want to" in header:
                    #tricky part is the letter
                    job = driver.find_element(By.XPATH, '//div[@class="ia-JobHeader-details"]')
                    job = job.get_attribute('innerHTML')
                    #name of company
                    company = job[:job.find(" - ")-1]
                    print(company)
                    job = driver.find_element(By.XPATH, '//div[@class="ia-JobHeader-title ia-JobHeader-title--withJobDetails"]')
                    job = job.get_attribute('innerHTML')
                    print(job)
                    #correct grammar
                    if job[0] in vowelList:
                        job = 'an ' + job
                    else:
                        job = 'a ' + job
                    print(job)
                    #find the location of the coverletter field and click
                    coverletter = driver.find_element(By.XPATH, '//span[@title="Write cover letter"]')
                    coverletter.click()
                    coverletter = driver.find_element(By.CSS_SELECTOR, "textarea.ia-Coverletter-textarea")
                    coverletter.click()
                    #don't forget to clear the text field of previous response
                    coverletter.send_keys(Keys.CONTROL+'a')
                    coverletter.send_keys(Keys.BACK_SPACE)

                    #open the coverletter
                    file = open('coverletter.txt', 'r')

                    #put these two entries into the coverletter
                    for i, x in enumerate(file):
                        time.sleep(0.3)
                        if i == 1:
                            index = x.find('this company')
                            first = x[0:index]
                            second = x[index+12:]
                            x = first + company + ' as ' + job + second
                        coverletter.send_keys(x)
                    #sweet this works great
                    #next page
                    next(driver)
                    continue
                #if the header asks for resume, confirmations, past jobs, or otherwise by default
                else:
                    print("nonspecific page, just skip")
                    #continued weirdness. Now just look for buttons with innerHTML with 'continue'
                    next(driver)
                    continue
            except Exception:
                print("Something didn't work")
                f = open('unfinishedApps.txt', 'a+')
                now = datetime.now()
                current_time = now.strftime("%m-%d-%Y %H:%M:%S")
                f.write(f"{current_time} unfinished app: {link}\n{Exception.with_traceback}\n\n")
                f.close()
                break
        print("End of process")
        next(driver)

    driver.close()



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

options = Options()
service = Service()
service.path = "F:\\Dropbox\\UNT\\TiredofApps\\geckodriver.exe"
options.add_argument("-profile F:\\Dropbox\\UNT\\TiredofApps\\ed53ej1d.Gecko")
options.set_preference("remote.prefs.recommended", False)
options.set_preference("dom.allow_scripts_to_close_windows", True)
options.set_preference("browser.tabs.closeWindowWithLastTab", True)
options.add_argument("--marionette-port 5555")
# options.add_argument("--disable-gpu-shader-disk-cache ")

# cwd = os.getcwd()
# print(cwd)
indeed(options, service)
