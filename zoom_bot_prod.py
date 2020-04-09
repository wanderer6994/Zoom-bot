from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import sys

#------------------------------------ ENTER YOUR INFO HERE ---------------------------------------------------
USERNAME = ''
PASSWORD = ''
NAME = "" #meeting name
zoom_key = ''
zoom_password = ""
operating_system = 'mac' # mac, windows, linux
#------------------------------------ ADVANCED SETTINGS ---------------------------------------------------
retry_time = 1
retry_time *= 60

#-------------------------------------------------------------------------------------------------------------
driver = None
if(operating_system == 'mac'):
    driver = webdriver.Chrome("./drivers/chromedriver_mac")
elif(operating_system == 'linux'):
    driver = webdriver.Chrome("./drivers/chromedriver_linux")
elif(operating_system == 'windows'):
    driver = webdriver.Chrome("./drivers/chromedriver_windows")
else:
    print("OS Not chosen. Please check and try again.")
    sys.exit(0)

login_url = 'https://zoom.us/wc/join/' +zoom_key +'?wpk='

#checks if an element is present on webpage by id
def check_if_element_exists_id(id):
    try:
        driver.find_element_by_id(id)
        return True
    except:
        return False

#join meeting at a later time if it hasn't started yet
def join_after_signin():
    try:
        driver.get(login_url)
        delay = 3
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'inputname')))
            print("Join meeting page loaded")
        except TimeoutException:
            print("Loading took too much time!")

        input_meeting_name = driver.find_element_by_id('inputname')
        input_meeting_name.clear()
        input_meeting_name.send_keys(NAME)
        driver.find_element_by_id('joinBtn').click()

        delay = 3  # seconds
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'inputname')))
            print("Join meeting page loaded")
        except TimeoutException:
            print("Loading took too much time!")

        driver.find_element_by_class_name('zm-btn--lg').click()

        driver.switch_to.alert().accept()
    except Exception as e:
        raise e


def login_and_join():
    try:
        driver.get(login_url)
        driver.find_element_by_id('email').send_keys(USERNAME)
        driver.find_element_by_id('password').send_keys(PASSWORD)
        driver.find_element_by_xpath('//div[@class="signin"]').click()

        delay = 3  # seconds
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'inputname')))
            print("Join meeting page loaded")
        except TimeoutException:
            print("Loading took too much time!")

        input_meeting_name = driver.find_element_by_id('inputname')
        input_meeting_name.clear()
        input_meeting_name.send_keys(NAME)

        if check_if_element_exists_id('inputpasscode'):
            driver.find_element_by_id('inputpasscode').send_keys(zoom_password)

        driver.find_element_by_id('joinBtn').click()

        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'inputname')))
            print("Join meeting page loaded")
        except TimeoutException:
            print("Loading took too much time!")

        driver.find_element_by_class_name('zm-btn--lg').click()

        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'tab-button')))
            print("Joined meeting successfully!")
        except TimeoutException:
            print("Loading took too much time!")
        driver.find_element_by_class_name('tab-button').click()

        driver.switch_to.alert().accept()
    except Exception as e:
        print("Failed with error: " +str(e))
        print("Retrying in " +str(retry_time) +' seconds.')
        while True:
            time.sleep(retry_time)
            join_after_signin()

login_and_join()