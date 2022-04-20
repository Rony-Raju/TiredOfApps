
from selenium.webdriver import Firefox



def indeed_login(options, service):
    while True:
        try:
            driver = Firefox(service=service, options=options)
            try:
                driver.get("https://myjobs.indeed.com/saved?hl=en&co=US&from=_atweb_gnav-homepage")
                if driver.current_url == "https://myjobs.indeed.com/saved?hl=en&co=US&from=_atweb_gnav-homepage":
                    return driver
            except Exception as e:
                print(f"exception 2 is {e}")
              
        except Exception as e:
            print(f"exception 1 is {e}")
            driver.close()
