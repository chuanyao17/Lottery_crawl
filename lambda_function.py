import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def read_file(file_location):
    with open(file_location) as file:
        js = json.load(file)
    return js

def apply_lottery(account, driver):
    first_name, last_name, email, month, day, year = account.values()
    print(first_name, last_name, email, month, day, year)
    
    # find the valid entry only for the desktop
    for desktop in driver.find_elements(By.CLASS_NAME,'row.lotteries-row.hide-for-tablets.show-for-desktop'):
        print("first loop")
        for button in desktop.find_elements(By.CLASS_NAME,'btn.btn-primary.enter-button.enter-lottery-link'):
            print("second loop")
            # process the application
            print("check entry button first",button)
            driver.delete_all_cookies()
            print("check  entry button after delete cookies",button)
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'btn.btn-primary.enter-button.enter-lottery-link'))
                )
            except:
                print("no entry found")
            print("after checking, ready to click the entry button")
            button.click()
            time.sleep(1)
            print("clicked the entry button")
            driver.switch_to.frame(driver.find_element(By.CLASS_NAME,'fancybox-iframe'))
            time.sleep(1)
            driver.find_element(By.ID,'dlslot_name_first').send_keys(first_name)
            driver.find_element(By.ID,'dlslot_name_last').send_keys(last_name)
            driver.find_element(By.ID,'dlslot_ticket_qty').send_keys('2')
            driver.find_element(By.ID,'dlslot_email').send_keys(email)
            driver.find_element(By.ID,'dlslot_dob_month').send_keys(month)
            driver.find_element(By.ID,'dlslot_dob_day').send_keys(day)
            driver.find_element(By.ID,'dlslot_dob_year').send_keys(year)
            driver.find_element(By.ID,'dlslot_zip').send_keys('11101')
            Select(driver.find_element(By.ID, 'dlslot_country')).select_by_value("2")
            
            # hit the check box and wait for the recaptcha
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(1)
            check_mark = driver.find_element(By.XPATH,'/html/body/div/main/article/div/form/fieldset/p[8]/label')
            # align the check box to the right
            ActionChains(driver).move_to_element_with_offset(check_mark,-50,0).click().perform()
            
            #  hit the recaptcha if existed
            try:
                recaptcha=driver.find_element(By.XPATH,'//*[@id="post-81"]/div/form/fieldset/div[1]/div/div/iframe')
                print("found first recaptcha box",recaptcha)
                driver.switch_to.frame(recaptcha)
                driver.find_element(By.CLASS_NAME,'recaptcha-checkbox-border').click()
                print("finished clicked first recaptcha box")
                
                # try to skip the second recaptcha for 9x9 image test
                try:
                    print("check if existed second 9x9 recaptcha")
                    recaptcha_9x9=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/iframe')
                    print("found recaptcha 9x9",recaptcha_9x9)
                    driver.switch_to.default_content()
                    driver.find_element(By.CLASS_NAME,'fancybox-item.fancybox-close').click()
                    print("closed the current entry because of recptcha 9x9")
                    continue
                    # driver.switch_to.frame(recaptcha_9x9)
                    # driver.find_element(By.ID, 'recaptcha-verify-button').click()
                    # print("finshed clicked second recaptcha")
                    # driver.switch_to.default_content()
                except:
                    time.sleep(2)
                    # check if I have back to upper frame
                    # driver.switch_to.parent_frame()
                    driver.switch_to.default_content()
                    driver.switch_to.frame(driver.find_element(By.CLASS_NAME,'fancybox-iframe'))
                    print("no recaptcha 9x9 test found")
                    
            except:
                print("no recaptcha box found")
            time.sleep(4)
            
            # hit the submit button
            try:
                element = driver.find_element(By.CLASS_NAME,'btn.btn-primary')
                print("Switched back to the parent frame successfully")
            except:
                print("Not switched back to the parent frame")
            print("checked final entry button first",element)
            driver.delete_all_cookies()
            print("checked final entry button after delete cookies",element)
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'btn.btn-primary'))
                )
                element.click()
                print("submitted the enrtry")
            except:
                print("failed to submitt the entry")
            time.sleep(1)
            driver.switch_to.default_content()
            driver.find_element(By.CLASS_NAME,'fancybox-item.fancybox-close').click()
            print("finished one entry")
    print("finished current website", driver.current_url)

def main(website_list, accounts_info, driver):
    for account in accounts_info:
        for website in website_list:
            driver.delete_all_cookies()
            driver.get(website)
            print("loading website--")
            title = driver.title
            print("current website title:", title)
            current_url = driver.current_url
            print("current website URL:", current_url)
            time.sleep(3)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(1)
            apply_lottery(account, driver)

def lambda_handler(event, context):
    website_list = read_file('lottery_website.txt')
    accounts_info = read_file('accounts.txt')
    print("finished reading files")
    
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--user-data-dir=/tmp/chromium")
    # chrome_options.add_argument("--incognito")
    
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    
    chrome_options.binary_location = '/opt/chromium/chrome'
    service = Service(executable_path="/opt/chromedriver/chromedriver")
    
    # chrome_options.binary_location = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
    # service = Service(executable_path="C:\\Users\\Yao\\Desktop\\uc_test\\selenium_test\\selenium_chromium")

    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )
    print("finished loading the driver")
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    print("Starting the process")
    main(website_list, accounts_info, driver)
    print("Finished the process")
# lambda_handler(None, None)