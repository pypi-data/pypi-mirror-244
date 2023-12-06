from sys import stdout
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as bs

def selenium_wrapper(url, selenium_identifier):
    try:
        Options = webdriver.ChromeOptions() # custom options
        Options.add_argument("--headless=new") # more efficiency & dont open chrome on user computer

        driver = webdriver.Chrome(options=Options) # generates an chrome page "emulator"

        # delete devtools message (selenium popup) | not working if user compile it by python.exe program.py
        stdout.write("\033[F")
        stdout.write("\033[K")
        stdout.write("\033[F")

        driver.get(url) # """requests""" the page (emulate the page on the driver)

        # wait til load the traduction element (html) 
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((selenium_identifier[0], selenium_identifier[1])))
        # selenium_identifier value 1st example: (By.CLASS_NAME, '<element class>')
        # selenium_identifier value 2nd example: (By.ID, '<element id>')

        page_code = driver.page_source # get page code

        return bs(page_code, 'html.parser')
    except TimeoutException as tout:
        return f"Something went wrong! Error: {str(tout)}"

def translater(source_language: str, target_language: str, text: str) -> str:
    text = text.replace(' ', '%20') # making the text appropriate for the URL
        
    url_ = f'https://translate.google.com/?sl={source_language}&tl={target_language}&text={text}&op=translate' # base url

    soup = selenium_wrapper(url_, (By.CLASS_NAME, 'ryNqvb')) # get soup (selenium method)

    translated_text = soup.find('span', attrs={'class': 'ryNqvb', 'jsname': 'W297wb'}).text # finding the translation

    return translated_text
