import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as bs
import requests

def wrapper(url: str, selenium_method: bool = False, selenium_class_identifier: tuple = None) -> bs:
    if selenium_method is True:
        try:
            Options = webdriver.ChromeOptions() # custom options
            Options.add_argument("--headless=new") # more efficiency & dont open chrome on user computer

            driver = webdriver.Chrome(options=Options) # generates an chrome page "emulator"

            # delete devtools message (selenium popup)
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            sys.stdout.write("\033[F")

            driver.get(url) # """requests""" the page (emulate the page on the driver)

            # wait til load the traduction element (html) 
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((selenium_class_identifier[0], selenium_class_identifier[1])))
            # selenium_class_identifier value 1st example: (By.CLASS_NAME, '<element class>')
            # selenium_class_identifier value 2nd example: (By.ID, '<element id>')

            page_code = driver.page_source # get page code

            soup = bs(page_code, 'html.parser')
        except TimeoutException as tout:
            return f"Something went wrong! Error: {str(tout)}" 
    else: # default wrapper
        try:
            resp = requests.get(url) # request the page
            resp.raise_for_status() # if status_code isnt 200 will return an especific exception
            soup = bs(resp.content, 'html.parser') # page code (response as bytes)
        except Exception as err:
            return f"Something went wrong! Error: {str(err)}"

    return soup # always returns soup

class GoogleTools:
    ## FINE
    def currency_conversion(base_currency: str, target_currency: str, only_float: bool = True) -> tuple | dict:
        url_ = f"https://www.google.com/finance/quote/{base_currency.upper()}-{target_currency.upper()}" # base url
            
        soup = wrapper(url=url_) # get soup (default method)
        
        currency_value = float(f"{float(soup.find('div', attrs={'class': 'YMlKec fxKbKc'}).text):.4f}") # find the value of the currency and turn into a float with up to 4 decimals

        last_update = soup.find('div', attrs={'class': 'ygUjEc', 'jsname': 'Vebqub'}).text.replace('\u202f', ' ').replace(' · Disclaimer', '') # finding the last update of the currency and filter it to remove bullshit

        conversion_dict = { # formatting the wrapped data to return it prettyfied
            'conversion': [
                f'1 {base_currency}',
                f'{currency_value:.2f} {target_currency}'
            ],
            'float': currency_value,
            'last_update': last_update
        }

        if only_float is not True: # filtering return
            return conversion_dict
        else:
            return conversion_dict['float']

    def translater(source_language: str, target_language: str, text: str) -> str:
        text = text.replace(' ', '%20') # making the text appropriate for the URL
        
        url_ = f'https://translate.google.com/?sl={source_language}&tl={target_language}&text={text}&op=translate' # base url

        soup = wrapper(url=url_, selenium_method=True, selenium_class_identifier=(By.CLASS_NAME, 'ryNqvb')) # get soup (selenium method)

        translated_text = soup.find('span', attrs={'class': 'ryNqvb', 'jsname': 'W297wb'}).text # finding the translation

        return translated_text
