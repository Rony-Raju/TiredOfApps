from .next_page import next_page
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert

vowelList = ['A', 'a', 'E', 'e', 'I', 'i', 'O', 'o', 'U', 'u']

def indeed_postings(driver):
    #find the user icon and click on saved jobs
    postings = driver.find_elements(By.CSS_SELECTOR, 'a.atw-ApplyButton')
    applications = [x.get_attribute('href') for x in postings]
    for x in applications:
        driver.get(x)
        try: 
            Alert(driver).accept()
        except Exception as e:
            print(e)
        time.sleep(1)
        header = ''
        redundancy = 1
        next_page(driver)
        link = x
        while("Please Review" not in header):
            time.sleep(1)
            try:
                #get the header each time and behave accordingly
                header = driver.find_element(By.TAG_NAME, 'h1')
                header = header.get_attribute('innerHTML')
                if not redundancy:
                    break
                #for preliminary questions
                elif "Questions" in header:
                    questions = driver.find_elements(By.XPATH, '//div[@class="ia-Questions-item css-e9ld6l eu4oa1w0"]')
                    questions_text = [x.get_attribute('innerHTML') for x in questions]
                    for i, text in enumerate(questions_text):
                        if "sponsor" in text:
                            try:
                                driver.execute_script("arguments[0].click()", questions[i].find_element(By.XPATH, '//input[@value="0"]'))
                            except Exception as e:
                                print(e)
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
                            except Exception as e:
                                if 'value=""' in text:
                                    response = questions[i].find_element(By.XPATH, '//input[@value=""]')
                                    response.send_keys(Keys.CONTROL+'a')
                                    response.send_keys('3')
                                continue
                        elif "salary" in text:
                            questions[i].find_element(By.CSS_SELECTOR, "div.css-d8iwdi e1jgz0i3").send_keys('65000 - 85000')
                        else:
                            
                            #weird thing to click, because element obscures
                            try:
                                answers = questions[i].find_elements(By.XPATH, '//input[@type="radio"]')
                                for selection in answers:
                                    choice = selection.find_element(By.CSS_SELECTOR, "span.css-19kaor0 eu4oa1w0")
                                    if 'Yes' in choice.get_attribute('innerHTML'):
                                        selection.click()
                                        continue
                                # driver.execute_script("arguments[0].click()", questions[i].find_element(By.CSS_SELECTOR, '//input[@value="1"]'))
                            except Exception as e:
                                print(e)
                        #TODO: case handling for commuting and protected veteran
                    #next page
                    redundancy = next_page(driver)                 
                    continue
                #for the letter
                elif "Want to" in header:
                    #tricky part is the letter
                    job = driver.find_element(By.XPATH, '//div[@class="ia-JobHeader-details"]')
                    job = job.get_attribute('innerHTML')
                    #name of company
                    company = job[:job.find(" - ")-1]
                   
                    job = driver.find_element(By.XPATH, '//div[@class="ia-JobHeader-title ia-JobHeader-title--withJobDetails"]')
                    job = job.get_attribute('innerHTML')              
                    #correct grammar
                    if job[0] in vowelList:
                        job = 'an ' + job
                    else:
                        job = 'a ' + job               
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
                    redundancy = next_page(driver)
                    continue
                elif "Want to" in header:
                    redundancy = next_page(driver)
                #if the header asks for resume, confirmations, past jobs, or otherwise by default
                else:
                    print("something weird")
                    #continued weirdness. Now just look for buttons with innerHTML with 'continue'
                    redundancy = next_page(driver)
                    continue
            except Exception as e:
                print("Something didn't work")
                print(e)
                f = open('unfinishedApps.txt', 'a+')
                now = datetime.now()
                current_time = now.strftime("%m-%d-%Y %H:%M:%S")
                f.write(f"{current_time} unfinished app: {link}\n{e}\n\n")
                f.close()
                break
        print("End of process")
        next_page(driver)