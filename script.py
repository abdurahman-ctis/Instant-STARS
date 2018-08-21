import re
from tkinter import *
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys

# Test to see if TkInter is working
# tkinter._test()

# ---------- TKINTER EVENTS  ----------

def page_is_loaded(driver):
    return driver.find_element_by_tag_name("body") != None
    
    
def instantStars(*args):
    #
    #TODO: Fix browser selection
    #
    if browser == 1 or 1==1:
        driverSTARS = webdriver.Chrome()
        driverWebmail = webdriver.Chrome()
    else:
        driverSTARS = webdriver.Firefox()
        driverWebmail = webdriver.Firefox()
        
    driverWebmail.get("https://webmail.bilkent.edu.tr/")
    driverSTARS.get("https://stars.bilkent.edu.tr/srs/")
    driverSTARS.execute_script("document.getElementById('LoginForm_password').value='%s'"%spass.get())
    driverWebmail.execute_script("document.getElementById('LoginForm_password').value='%s'"%mpass.get())
    #logs in to STARS system
    wait = ui.WebDriverWait(driverSTARS, 10)
    wait.until(page_is_loaded)
    email_field = driverSTARS.find_element_by_id("LoginForm_username")
    email_field.send_keys(sid.get())
    email_field.send_keys(Keys.RETURN)
    #logs in to bilkent webmail account
    wait = ui.WebDriverWait(driverWebmail, 10)
    wait.until(page_is_loaded)
    email_field = driverWebmail.find_element_by_id("rcmloginuser")
    email_field.send_keys(mail.get())
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



def handler():
    f = open("backup", "w")
    f.write(sid.get())
    f.write(mail.get())
    f.close()
    root.quit()

if __name__=="__main__":
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", handler)


    Label(root, text="STARS id").grid(row=0, sticky=W, padx=4)
    sid = Entry(root)
    sid.grid(row=0, column=1, sticky=E, pady=4)

    Label(root, text="STARS pass").grid(row=1, sticky=W, padx=4)
    spass = Entry(root)
    spass.grid(row=1, column=1, sticky=E, pady=4)

    Label(root, text="Webmail").grid(row=2, sticky=W, padx=4)
    mail = Entry(root)
    mail.grid(row=2, column=1, sticky=E, pady=4)

    Label(root, text="Webmail pass").grid(row=3, sticky=W, padx=4)
    mpass = Entry(root)
    mpass.grid(row=3, column=1, sticky=E, pady=4)

    browser = IntVar()
    Label(root, text="Preffered browser:").grid(row=4, sticky=W)
    Radiobutton(root, text="Chrome", variable=browser, value=1).grid(row=5,sticky=W)
    Radiobutton(root, text="Firefox", variable=browser, value=2).grid(row=5, column=1, sticky=W)

    Label(root, text="Use with caution. Friends can withdraw.").grid(row=6, sticky=W)
    remember = Checkbutton(root, text="Remember credentials").grid(row=7, sticky=W)

    submit = Button(root, text="Login")
    submit.grid(row=8)
    submit.bind("<Button-1>", instantStars)

    root.mainloop()
