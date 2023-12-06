from requests import get
from bs4 import BeautifulSoup as bs

def currency_conversion(base_currency: str, target_currency: str):
    resp = get(f'https://www.google.com/finance/quote/{base_currency.upper()}-{target_currency.upper()}')
    soup = bs(resp.content, 'html.parser')
    conversion_dict = {
        'float': float(soup.find('div', attrs={'class': 'YMlKec fxKbKc'}).text),
        'last_update': soup.find('div', attrs={'class': 'ygUjEc', 'jsname': 'Vebqub'}).text.replace(' UTC · Disclaimer', '')
    }
    return conversion_dict
