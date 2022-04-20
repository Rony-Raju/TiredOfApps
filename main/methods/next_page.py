
from selenium.webdriver.common.by import By
import time

def next_page(driver):
    try:
        buttons = driver.find_elements(By.TAG_NAME, "button")
        header = driver.find_element(By.TAG_NAME, 'h1')
    except Exception as e:
        print(e)
    for text in buttons:
        words = text.get_attribute('innerHTML')
        if 'Continue' in words or 'appl' in words or 'Apply now' in words:
            driver.execute_script("arguments[0].click()", text)
            # text.click()
            #if the next header is the same as the previous, we haven't moved
            time.sleep(2)
            new_header = driver.find_element(By.TAG_NAME, 'h1')
            if new_header == header:           
                return 0
            else:
                return 1 