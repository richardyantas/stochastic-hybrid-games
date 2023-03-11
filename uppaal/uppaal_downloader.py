from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from pathlib import Path


options = Options()
download_path = Path(__file__).resolve().parents[0]
prefs = {"download.default_directory": f"{download_path}"}
options.add_experimental_option("prefs", prefs)

# options.add_argument("start-maximized")
# options.add_argument('--disable-extensions')
# options.add_argument('--force-device-scale-factor=2')
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

# driver.set_window_position(2000, 0)
# driver.maximize_window()
time.sleep(1)

driver.get(
    "https://www.it.uu.se/research/group/darts/uppaal/download/registration.php?id=12&subid=19")

input_element = driver.find_element(
    By.XPATH, '//*[@id="main-copy"]/form/table/tbody/tr[1]/td[2]/input')

# Inserte el texto deseado
input_element.send_keys("Richard Yantas Alcantara")
# time.sleep(1)

input_2 = driver.find_element(
    By.XPATH, '//*[@id="main-copy"]/form/table/tbody/tr[2]/td[2]/input')
input_2.send_keys("Researcher")

input_3 = driver.find_element(
    By.XPATH, '//*[@id="main-copy"]/form/table/tbody/tr[3]/td[2]/input')
input_3.send_keys("UTEC")

input_4 = driver.find_element(
    By.XPATH, '//*[@id="main-copy"]/form/table/tbody/tr[8]/td[2]/input')
input_4.send_keys("richardyantas5@gmail.com")

driver.find_element(
    By.XPATH, '//*[@id="main-copy"]/form/table/tbody/tr[13]/td[1]/input').click()

driver.find_element(
    By.XPATH, '//*[@id="main-copy"]/form/table/tbody/tr[14]/td/input[1]').click()

time.sleep(20)
