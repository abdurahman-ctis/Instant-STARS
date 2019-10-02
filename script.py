import os.path
import re
from threading import Thread
from tkinter import *
from tkinter import ttk

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui

# Test to see if TkInter is working
# tkinter._test()


def page_is_loaded(driver):
    return driver.find_element_by_tag_name("body") != None


def instantStars(*args):
    #
    # TODO: Fix browser selection
    #
    if browser.get() == 1:
        driverWebmail = webdriver.Chrome()
        driverSTARS = webdriver.Chrome()
    elif browser.get() == 2:
        driverWebmail = webdriver.Firefox()
        driverSTARS = webdriver.Firefox()

    driverWebmail.get("https://webmail.bilkent.edu.tr/")
    driverSTARS.get("https://stars.bilkent.edu.tr/srs/")
    driverSTARS.execute_script(
        "document.getElementById('LoginForm_password').value='%s'" % spass.get())
    driverWebmail.execute_script(
        "document.getElementById('LoginForm_password').value='%s'" % mpass.get())
    # logs in to STARS system
    wait = ui.WebDriverWait(driverSTARS, 10)
    wait.until(page_is_loaded)
    email_field = driverSTARS.find_element_by_id("LoginForm_username")
    email_field.send_keys(sid.get())
    email_field.send_keys(Keys.RETURN)
    # logs in to bilkent webmail account
    wait = ui.WebDriverWait(driverWebmail, 10)
    wait.until(page_is_loaded)
    email_field = driverWebmail.find_element_by_id("rcmloginuser")
    email_field.send_keys(mail.get())
    email_field.send_keys(Keys.RETURN)
    new_email = driverWebmail.find_elements_by_class_name("adr")
    while not new_email:
        new_email = driverWebmail.find_elements_by_class_name("adr")
    new_email[0].click()

    driverWebmail.switch_to.frame(
        driverWebmail.find_element_by_id("messagecontframe"))
    code_field = driverWebmail.find_elements_by_class_name("pre")
    while not code_field:
        code_field = driverWebmail.find_elements_by_class_name("pre")
    code = code_field[0].get_attribute('innerHTML')
    Thread(target=driverWebmail.quit).start()
    verify = driverSTARS.find_element_by_id("EmailVerifyForm_verifyCode")
    verify.send_keys(code[19:24])
    verify.send_keys(Keys.RETURN)


# save if 'Remember me' is clicked
def handlerWrite():
    if remember.get() == 1 and sid.get() and mail.get():
        f = open("backup", "w")
        f.write(sid.get()+'\n')
        f.write(spass.get()+'\n')
        f.write(mail.get()+'\n')
        f.write(mpass.get())
        f.close()
    root.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Instant STARS")
    root.iconbitmap('icon.ico')
    root.resizable(width=False, height=False)

    sid = Entry(width=40)
    spass = Entry(width=40, show="\u2022")
    mail = Entry(width=40)
    mpass = Entry(width=40, show="\u2022")
    remember = IntVar()

    # retrieve saved info
    if os.path.isfile('./backup'):
        with open('backup') as f:
            lines = [line.rstrip('\n') for line in f]
        sid.insert(0, lines[0])
        spass.insert(0, lines[1])
        mail.insert(0, lines[2])
        mpass.insert(0, lines[3])

    root.protocol("WM_DELETE_WINDOW", handlerWrite)

    img = PhotoImage(file='stars.jpg')
    Label(root, image=img).grid()

    Label(root, text="STARS id:").grid(row=1, sticky=W, padx=4, pady=5)
    sid.grid(row=1, column=1, padx=10, pady=5)

    Label(root, text="STARS password:").grid(row=2, sticky=W, padx=4, pady=5)
    spass.grid(row=2, column=1, padx=10, pady=5)

    Label(root, text="Webmail address:").grid(row=3, sticky=W, padx=4, pady=5)
    mail.grid(row=3, column=1, padx=10, pady=5)

    Label(root, text="Webmail password:").grid(row=4, sticky=W, padx=4, pady=5)
    mpass.grid(row=4, column=1, padx=10, pady=5)

    browser = IntVar()
    Label(root, text="Preffered browser:").grid(row=5, sticky=W, padx=4)
    Radiobutton(root, text="Chrome", variable=browser,
                value=1).grid(row=6, sticky=W, padx=4)
    Radiobutton(root, text="Firefox", variable=browser,
                value=2).grid(row=7, sticky=W, padx=4)

    Label(root, text="Use with caution. Friends can withdraw.").grid(
        row=8, sticky=W, padx=4)
    rememberme = Checkbutton(root, text="Remember me",
                             variable=remember).grid(row=9, sticky=W, padx=4)

    submit = Button(root, text="      Login      ")
    submit.grid(row=10, columnspan=3, padx=4)
    submit.bind("<Button-1>", instantStars)

    root.mainloop()
