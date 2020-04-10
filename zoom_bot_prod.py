from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import time
import sys

# ------------------------------------ ENTER YOUR INFO HERE ---------------------------------------------------
USERNAME = ''  # zoom username
PASSWORD = ''  # zoom password
NAME = ""  # meeting name
zoom_key = ''  # meeting_id
zoom_password = ""  # meeting_password (leave blank if no password is required)
meeting_time = ""  # in HH:MM:SS 24 hour clock
operating_system = 'mac'  # mac, windows, linux

# ------------------------------------ ADVANCED SETTINGS ---------------------------------------------------
retry_time = 1  # Time before checking if element is present again

sleep_time = 1  # Time after failure before bot tries joining the meeting again
# -------------------------------------------------------------------------------------------------------------

# initialising drivers
driver = None
if operating_system == 'mac':
    driver = webdriver.Chrome("./drivers/chromedriver_mac")
elif operating_system == 'linux':
    driver = webdriver.Chrome("./drivers/chromedriver_linux")
elif operating_system == 'windows':
    driver = webdriver.Chrome("./drivers/chromedriver_windows")
else:
    print("OS Not chosen. Please check and try again.")
    sys.exit(0)

login_url = 'https://zoom.us/wc/join/' + zoom_key + '?wpk='

# Extracting meeting hour, minutes and seconds
meeting_hour = int(meeting_time[0:2])
meeting_minute = int(meeting_time[3:5])
meeting_second = int(meeting_time[6:8])
print("meeting time: " + str(meeting_hour) + " " + str(meeting_minute) + " " + str(meeting_second))


# checks if an element is present on webpage by id
def check_if_element_exists_id(id):
    try:
        driver.find_element_by_id(id)
        return True
    except:
        return False


def check_if_element_exists_class(name):
    try:
        driver.find_element_by_class_name(name)
        return True
    except:
        return False


def wait_for_element_to_load_name(name):
    delay = 3  # seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, name)))
        print("Page Loaded!")
    except TimeoutException:
        print("Loading took too much time!")


def wait_for_element_to_load_class(name):
    delay = 3  # seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, name)))
        print("Page Loaded!")
    except TimeoutException:
        print("Loading took too much time!")


def login_and_join():
    try:
        driver.get(login_url)
        driver.find_element_by_id('email').send_keys(USERNAME)
        driver.find_element_by_id('password').send_keys(PASSWORD)
        driver.find_element_by_xpath('//div[@class="signin"]').click()

        delay = 3  # seconds

        wait_for_element_to_load_name('inputname')
        input_meeting_name = driver.find_element_by_id('inputname')
        input_meeting_name.clear()
        input_meeting_name.send_keys(NAME)

        if check_if_element_exists_id('inputpasscode'):
            driver.find_element_by_id('inputpasscode').send_keys(zoom_password)

        driver.find_element_by_id('joinBtn').click()

        wait_for_element_to_load_name('inputname')
        driver.find_element_by_class_name('zm-btn--lg').click()

        wait_for_element_to_load_class('tab-button')
        driver.find_element_by_class_name('tab-button').click()

        driver.switch_to.alert().accept()
    except Exception as e:
        while not check_if_element_exists_class('footer__leave-btn'):
            print("Failed with error: " + str(e))
            print("Retrying in " + str(retry_time) + ' seconds.')
            time.sleep(retry_time * 60)


while True:
    now = datetime.now()
    print("now time: " + str(now.hour) + " " + str(now.minute))
    if now.hour == meeting_hour and now.minute >= meeting_minute:
        print("starting login and join")
        login_and_join()
        break
    else:
        print("Meeting time not up. Sleeping for %s minutes" % str(sleep_time))
        time.sleep(sleep_time * 60)