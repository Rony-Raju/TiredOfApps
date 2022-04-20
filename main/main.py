from indeed_applier import indeed
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service




options = Options()
service = Service()
service.path = "F:\\Dropbox\\UNT\\TiredofApps\\geckodriver.exe"
options.add_argument("-profile F:\\Dropbox\\UNT\\TiredofApps\\ed53ej1d.Gecko")
options.set_preference("remote.prefs.recommended", False)
options.set_preference("dom.allow_scripts_to_close_windows", True)
options.set_preference("browser.tabs.closeWindowWithLastTab", True)
options.add_argument("--marionette-port 5555")
options.add_argument("--disable-gpu-shader-disk-cache ")

# cwd = os.getcwd()
# print(cwd)

indeed(options, service)