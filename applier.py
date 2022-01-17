import os
from fpdf import FPDF
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
vowelList = ['A', 'a', 'E', 'e', 'I', 'i', 'O', 'o', 'U', 'u']


def indeed(options):
    driver = Firefox(options=options)
    driver.get('https://www.indeed.com/')
    #find the user icon and click on saved jobs
    driver.find_element(By.XPATH,'//div[@class="gnav-header-1dy22ep e37uo190"]').click()
    driver.find_element(By.XPATH,'//a[@data-gnav-element-name="MyJobs"]').click()
    driver.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()

    postings = driver.find_elements(By.CSS_SELECTOR, 'a.atw-ApplyButton')

    applications = [x.get_attribute('href') for x in postings]
    for x in applications:
        driver.get(x)
        driver.find_element(By.XPATH, '//button[@id="indeedApplyButton"]').click()
        header = ''
        while("Please Review" not in header):
            try:
                #get the header each time and behave accordingly
                header = driver.find_element(By.XPATH, '//h1[@class="ia-BasePage-heading fs-unmask"]')
                header = header.get_attribute('innerHTML')
                #for preliminary questions
                if "Questions" in header:
                    questions = driver.find_elements(By.XPATH, '//div[@class="ia-Questions-item css-e9ld6l eu4oa1w0"]')
                    questions_text = [x.get_attribute('innerHTML') for x in questions]

                    for i, x in enumerate(questions_text):
                        if "sponsorship" or "sponsor" in x:
                            driver.execute_script("arguments[0].click()", questions[i].find_element(By.XPATH, '//input[@value="0"]'))
                        elif "education" in x:
                            driver.execute_script("arguments[0].click()", questions[i].find_element(By.XPATH, '//input[@value="1301880"]'))
                        elif "experience" in x:
                            driver.execute_script("arguments[0].click()", questions[i].find_element(By.XPATH, '//[@value="1301885"]'))
                        elif "salary" in x:
                            questions[i].find_element(By.CSS_SELECTOR, "div.css-d8iwdi e1jgz0i3").send_keys('65000 - 85000')
                        else:
                            #weird thing to click, because element obscures
                            driver.execute_script("arguments[0].click()", questions[i].find_element(By.XPATH, '//input[@value="1"]'))
                    #next page
                    driver.find_element(By.CSS_SELECTOR, "button.ia-continueButton").click()
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
                    driver.find_element(By.XPATH, '//div[@id="write-cover-letter-selection-card"]').click()

                    #don't forget to clear the text field of previous response
                    driver.find_element(By.XPATH, '//button[@class="ia-Coverletter-edit css-4493ey e8ju0x51"]').click()
                    #confirmation
                    driver.find_element(By.XPATH, '//button[@class="ia-ConfirmModal-button-action css-usjv6p e8ju0x51"]').click()
                    #find location of the text field
                    coverletter = driver.find_element(By.XPATH, '//textarea[@id="coverletter-textarea"]')
                    coverletter.click()

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
                    driver.find_element(By.CSS_SELECTOR, "button.ia-continueButton").click()
                    continue
                #finally check if the header is the final confirmation, and submit

                #if the header asks for resume, confirmations, past jobs, or otherwise by default
                else:
                    driver.find_element(By.CSS_SELECTOR, "button.ia-continueButton").click()
                    continue
            except ValueError:
                print("Couldn't find value")
                f = open('TiredOfApps/unfinishedApps.txt', w)
                f.write("unfinished app: ", x)
                f.close
                break


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
profile_path = r'C:\Users\Rony\AppData\Roaming\Mozilla\Firefox\Profiles\ag1yjdfi.SeleniumProfile'
options.add_argument("-profile=C:\\Users\\Rony\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\ag1yjdfi.SeleniumProfile")



indeed(options)
