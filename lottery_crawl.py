import time
import undetected_chromedriver as uc
import json
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains


def read_file(file_location):
    file=open(file_location)
    js = json.loads(file.read())
    file.close()
    return js


def apply_lottery(account):
    first_name,last_name,email,month,day,year=account.values()
    print(first_name,last_name,email,month,day,year)
    
    for desktop in driver.find_elements(By.CLASS_NAME,'row.lotteries-row.hide-for-tablets.show-for-desktop'):
        for button in desktop.find_elements(By.CLASS_NAME,'btn.btn-primary.enter-button.enter-lottery-link'):
            button.click()
            driver.switch_to.frame(driver.find_element(By.CLASS_NAME,'fancybox-iframe'))
            driver.find_element(By.ID,'dlslot_name_first').send_keys(first_name)
            driver.find_element(By.ID,'dlslot_name_last').send_keys(last_name)
            driver.find_element(By.ID,'dlslot_ticket_qty').send_keys('2')
            driver.find_element(By.ID,'dlslot_email').send_keys(email)
            driver.find_element(By.ID,'dlslot_dob_month').send_keys(month)
            driver.find_element(By.ID,'dlslot_dob_day').send_keys(day)
            driver.find_element(By.ID,'dlslot_dob_year').send_keys(year)
            driver.find_element(By.ID,'dlslot_zip').send_keys('11101')
            Select(driver.find_element(By.ID, 'dlslot_country')).select_by_value("2")
            
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(1)
            check_mark = driver.find_element(By.XPATH,'/html/body/div/main/article/div/form/fieldset/p[8]/label')
            ActionChains(driver).move_to_element_with_offset(check_mark,-50,0).click().perform()
            
            try:
                recaptcha=driver.find_element(By.XPATH,'//*[@id="post-81"]/div/form/fieldset/div[1]/div/div/iframe')
                driver.switch_to.frame(recaptcha)
                driver.find_element(By.CLASS_NAME,'recaptcha-checkbox-border').click()
                try:
                    print("test the check box and wait")
                    recaptcha_9x9=driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/iframe')
                    driver.switch_to.frame(recaptcha_9x9)
                    driver.find_element(By.ID, 'recaptcha-verify-button').click()
       
                    driver.switch_to.default_content()
                except:
                    time.sleep(5)
                    driver.switch_to.parent_frame()
                    
                
            except:
                pass
            time.sleep(4)
            driver.find_element(By.CLASS_NAME,'btn.btn-primary').click()
            driver.switch_to.default_content()
            driver.find_element(By.CLASS_NAME,'fancybox-item.fancybox-close').click()
            
def main():
    for website in website_list:
        print(website)
        driver.get(website)
        time.sleep(5)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
        for account in accounts_info:
            apply_lottery(account)
        

website_list=read_file('lottery_website.txt')   
# website_list=read_file('test.txt')   
accounts_info=read_file('accounts.txt')
driver = uc.Chrome() 
main()

    
    

    # location = check_mark.location
    # size = check_mark.size
    # w, h = size['width'], size['height']
    # print(location)
    # print(size)
    # print(w, h)