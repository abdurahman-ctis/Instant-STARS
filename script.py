import re
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys

def page_is_loaded(driver):
    return driver.find_element_by_tag_name("body") != None

#logs in to bilkent webmail account
def webmail(mail, passwd):
    driverWebmail.execute_script("document.getElementById('LoginForm_password').value='%s'"%passwd)
    wait = ui.WebDriverWait(driverWebmail, 10)
    wait.until(page_is_loaded)
    email_field = driverWebmail.find_element_by_id("rcmloginuser")
    email_field.send_keys(mail)
    email_field.send_keys(Keys.RETURN)
    new_email = driverWebmail.find_elements_by_class_name("adr")
    new_email[0].click()

    driverWebmail.switch_to.frame(driverWebmail.find_element_by_id("messagecontframe"))
    code_field = driverWebmail.find_element_by_class_name("pre")
    code = code_field.get_attribute('innerHTML')
    driverWebmail.quit()
    verify = driverSTARS.find_element_by_id("EmailVerifyForm_verifyCode")
    verify.send_keys(code[19:24])
    verify.send_keys(Keys.RETURN)
    

#logs in to STARS system
def srs(id, passwd):
    driverSTARS.execute_script("document.getElementById('LoginForm_password').value='%s'"%passwd)
    wait = ui.WebDriverWait(driverSTARS, 10)
    wait.until(page_is_loaded)
    email_field = driverSTARS.find_element_by_id("LoginForm_username")
    email_field.send_keys(id)
    email_field.send_keys(Keys.RETURN)
    

sid = input("Enter STARS id: ")
spass = input("Enter STARS pass: ")
mail = input("Enter Webmail adress: ")
mpass = input("Enter Webmail password: ")

browser = input("What is your preferred browser?\n1.Chrome\n2.Firefox\n")
while not (browser=="1" or browser=="2"):
    browser = input("Enter a valid number: ")
if(browser == "1"):
    driverSTARS = webdriver.Chrome()
    driverWebmail = webdriver.Chrome()
else:
    driverSTARS = webdriver.Firefox()
    driverWebmail = webdriver.Firefox()
    
driverSTARS.get("https://stars.bilkent.edu.tr/srs/")
driverWebmail.get("https://webmail.bilkent.edu.tr/")

srs(sid,spass)
webmail(mail, mpass)
