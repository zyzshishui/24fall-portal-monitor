import time
import requests
import platform
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

USERNAME = '***'
PASSWORD = '***'
PUSHPLUS_TOKEN = '***'
SLEEP_TIME = 600    #多久刷新一次（秒），默认十分钟
CHROMEDRIVR_PATH = '/usr/bin/chromedriver-linux64/chromedriver' #linux下配置

def send_wechat(msg):
    token = PUSHPLUS_TOKEN
    title = 'portal'
    content = msg
    template = 'html'
    url = f"https://www.pushplus.plus/send?token={token}&title={title}&content={content}&template={template}"
    print(url)
    r = requests.get(url=url)
    print(r.text)

def nyu(driver):
    driver.get('https://apply.engineering.nyu.edu/account/login?')
    driver.find_element(By.NAME, 'email').send_keys(USERNAME)
    driver.find_element(By.NAME, 'password').send_keys(PASSWORD + Keys.RETURN)
    time.sleep(5)

    wait = WebDriverWait(driver, 10)
    link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Fall 2024")))
    link.click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Open Application')]")))
    button = driver.find_element(By.XPATH, "//button[contains(text(), 'Open Application')]")
    button.click()
    print("NYU: Successfully logged in")
    time.sleep(5)
    while True:
        driver.refresh()
        time.sleep(10)
        try:
            checklist = driver.find_element(By.ID, 'part_checklist_Reference')
            time.sleep(SLEEP_TIME)
        except NoSuchElementException:
            msg = 'Application Checklist disappeared'
            print(msg)
            send_wechat(msg)
            break

def ucsd(driver):
    driver.get('https://connect.grad.ucsd.edu/account/login?')
    driver.find_element(By.NAME, 'email').send_keys(USERNAME)
    driver.find_element(By.NAME, 'password').send_keys(PASSWORD + Keys.RETURN)
    time.sleep(5)
    wait = WebDriverWait(driver, 10)
    link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Graduate")))
    link.click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Open Application')]")))
    button = driver.find_element(By.XPATH, "//button[contains(text(), 'Open Application')]")
    button.click()
    print("UCSD: Successfully logged in")
    time.sleep(5)
    while True:
        driver.refresh()
        time.sleep(10)
        try:
            checklist = driver.find_element('id', 'part_checklist_Material')
            time.sleep(SLEEP_TIME)
        except NoSuchElementException:
            msg = 'UCSD Application Checklist disappeared'
            print(msg)
            send_wechat(msg)
            break

def main():
    if platform.system().lower() == 'linux':
        service = Service(executable_path=CHROMEDRIVR_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:
        driver = webdriver.Chrome(options=chrome_options)

    nyu(driver)
    # ucsd(driver)

    driver.quit()

if __name__ == '__main__':
    main()