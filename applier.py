import os
from datetime import datetime
from fpdf import FPDF
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
vowelList = ['A', 'a', 'E', 'e', 'I', 'i', 'O', 'o', 'U', 'u']

def next(driver):
    buttons = driver.find_elements(By.tag_name, "button")
    for text in buttons:
        if 'continue' in text.get_attribute('innerHTML'):
            text.click()
            return

def indeed(options):
    driver = Firefox(options=options)
    driver.get('https://www.indeed.com/')
    #find the user icon and click on saved jobs
    driver.find_element(By.XPATH,'//div[@class="gnav-header-1dy22ep e37uo190"]').click()
    driver.find_element(By.XPATH,'//a[@data-gnav-element-name="MyJobs"]').click()

    postings = driver.find_elements(By.CSS_SELECTOR, 'a.atw-ApplyButton')

    applications = [x.get_attribute('href') for x in postings]
    for x in applications:
        driver.get(x)
        driver.find_element(By.XPATH, '//button[@id="indeedApplyButton"]').click()
        header = ''
        link = x
        while("Please Review" not in header):
            try:
                #get the header each time and behave accordingly
                header = driver.find_element(By.XPATH, '//h1[@class="ia-BasePage-heading fs-unmask"]')
                header = header.get_attribute('innerHTML')
                #for preliminary questions
                if "Questions" in header:
                    questions = driver.find_elements(By.XPATH, '//div[@class="ia-Questions-item css-e9ld6l eu4oa1w0"]')
                    questions_text = [x.get_attribute('innerHTML') for x in questions]

                    for i, text in enumerate(questions_text):
                        try:
                            #next page
                            next(driver)
                            continue
                        except Exception:
                            pass
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
                                answers = text.find_elements(By.CSS_SELECTOR, 'label.css-d0lawn es2vvo70')
                                for selection in answers:
                                    choice = selection.find_element(By.CSS_SELECTOR, "span.css-19kaor0 eu4oa1w0")
                                    if '3' in choice.get_attribute('innerHTML'):
                                        selection.click()
                                        break
                            except Exception:
                                text.find_element(By.CSS_SELECTOR, 'input.css-qxtdct e1jgz0i3').send_keys('3')
                        elif "salary" in text:
                            questions[i].find_element(By.CSS_SELECTOR, "div.css-d8iwdi e1jgz0i3").send_keys('65000 - 85000')
                        else:
                            #weird thing to click, because element obscures
                            driver.execute_script("arguments[0].click()", questions[i].find_element(By.XPATH, '//input[@value="1"]'))
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
                    print(job[0])
                    #correct grammar
                    if job[0] in vowelList:
                        job = 'an ' + job
                        print(job)
                    else:
                        job = 'a ' + job
                    #find the location of the coverletter field and click
                    coverletter = driver.find_element(By.CSS_SELECTOR, "textarea.ia-Coverletter-textarea")
                    coverletter.click()
                    #don't forget to clear the text field of previous response
                    coverletter.send_keys(Keys.CONTROL+'a')
                    coverletter.send_keys(Keys.BACK_SPACE)

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
                        coverletter.send_keys(x)
                    #sweet this works great
                    #next page
                    next(driver)
                    continue
                #finally check if the header is the final confirmation, and submit

                #if the header asks for resume, confirmations, past jobs, or otherwise by default
                else:
                    #continued weirdness. Now just look for buttons with innerHTML with 'continue'
                    buttons = driver.find_elements(By.tag_name, "button")
                    for text in buttons:
                        if 'continue' in text.get_attribute('innerHTML'):
                            text.click()
                    continue
            except Exception:
                print("Something didn't work")
                f = open('TiredOfApps/unfinishedApps.txt', 'a+')
                now = datetime.now()
                current_time = now.strftime("%m-%d-%Y %H:%M:%S")
                f.write(f"{current_time} unfinished app: {link}\n{Exception.with_traceback}\n\n")
                f.close()
                break
        driver.find_element(By.CSS_SELECTOR, "button.ia-continueButton").click()


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
options.add_argument("-profile ed53ej1d.Gecko")
options.set_preference("remote.prefs.recommended", False)
options.set_preference("dom.allow_scripts_to_close_windows", True)
options.set_preference("browser.tabs.closeWindowWithLastTab", True)
options.add_argument("--marionette-port 42069")


# cwd = os.getcwd()
# print(cwd)
indeed(options)
