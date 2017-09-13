from selenium import webdriver
from file_manager import *

import os
import sys
import time
import getpass


def cleanup_exit(driver):
    '''Closes the webdriver and exits script.'''

    print('Cleaning up...................')
    driver.quit()
    print('Cleanup Complete')
    sys.exit()


def init(download_area):
    '''Initializes project folder and webdriver options'''

    global base_url

    create_folder(download_area)

    try:
        options = webdriver.ChromeOptions()
        prefs = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
                 "download.default_directory": download_area}

        options.add_experimental_option("prefs", prefs)
    except Exception as e:
        print(e)
        sys.exit()

    try:
        browser = webdriver.Chrome(executable_path= os.path.join(os.getcwd(), 'chromedriver'), chrome_options = options)
        browser.get(base_url)
        browser.maximize_window()

        return browser
    except Exception as e:
        print(e)
        cleanup_exit(browser)


def login(Uname, Pword, login_name):
    ''' Attempts login using provided credentials. Returns True ons successful login, False otherwise.

    Argument list:
    Uname: ID number.
    Pword: Password.
    login_name: First name of your profile.
    '''

    global chrome
    try:
        print('Logging in..............................')

        user_el = chrome.find_element_by_name('username')
        pass_el = chrome.find_element_by_name('password')
        login_butn = chrome.find_element_by_tag_name('button')

        user_el.clear()
        pass_el.clear()
        user_el.send_keys(Uname)
        pass_el.send_keys(Pword)
        login_butn.click()
        chrome.get(base_url)

        if login_name not in chrome.page_source or 'Log in' in chrome.page_source:
            return False

        return True

    except Exception as e:
        print(e)
        cleanup_exit(chrome)


def log_out():
    '''Logs out of profile.'''

    global chrome

    try:
        logout_btn = chrome.find_elements_by_xpath("//a[text() = 'Log out']")[1]
        logout_btn.click()
        time.sleep(2)
        chrome.quit()
    except Exception as e:
        print(e)
        cleanup_exit(chrome)


def find_course(course_code):
    '''Finds course using course code provided. Retruns True if course is found, False otherwise.'''

    global chrome

    try:
        course_link_el = chrome.find_element_by_partial_link_text(course_code)
        course_link_el.click()

        return True
    except Exception as e:
        print('Could not find course {0}.'.format(course_code))
        return False


def get_materials():
    '''Downloads course material using webdriver. No return value.'''

    global chrome
    global base_url
    global project_area

    try:
        links = chrome.find_elements_by_xpath("//span[text()=' File']")
        material_link = None
        for i in range(len(links)):
            try:
                material_link = links[i].find_element_by_xpath('../..')
                print('Getting: ' + str(material_link.text))
                link_string = material_link.get_attribute('href')
                new_tab = "window.open('{0}','_blank')".format(link_string)

                chrome.execute_script(new_tab)
                print('{0} COMPLETE'.format(str(material_link.text)))
            except Exception as e:
                print("Could not get: "+str(material_link.text))
            time.sleep(1)

        while downloading_file_check(project_area):
            time.sleep(3)

        chrome.get(base_url)
    except Exception as e:
        print(e)


def login_info():
    '''Requests user login and course input. Returns a list of the input'''

    user = str(raw_input('Enter ID number: '))
    passw = getpass.unix_getpass('Enter Password(Password will not be displayed): ')
    name = str(raw_input('Enter Profile Username: '))

    return [user, passw, name]

if __name__ == '__main__':
    base_url = 'http://ourvle.mona.uwi.edu'
    project_area = os.path.join(os.getcwd(), 'course_materials')

    control_flag = True
    login_arr = login_info()
    course_arr = [str(arr_temp) for arr_temp in raw_input('Enter all course codes to download(space separated): ')\
        .strip().split(' ')]

    chrome = init(project_area)

    while control_flag:

        if login(login_arr[0], login_arr[1], login_arr[2]):
            print('Login Successful')
            control_flag = False
        else:
            choice = str(raw_input('Login unsuccessful\nEnter n - to exit and any other key to try again: '))
            if choice.lower() == 'n':
                cleanup_exit(chrome)
            else:
                login_arr = login_info()

    for course_c in course_arr:
        course_folder = os.path.join(project_area, course_c)

        if find_course(course_c):
            get_materials()
            move_all_files_to(project_area, course_folder)

    log_out()
    cleanup_exit(chrome)
