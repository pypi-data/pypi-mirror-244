# An unofficial Google Tools wrapper

## GoogleTools

This library provides a simple interface for accessing Google features.

### Installation

[See it on Pypi](https://pypi.org/project/google-tools-wrapper/)\
[See it on Github](https://github.com/xongs08/google-tools-wrapper)

```bash
pip install google-tools-wrapper
```

## Currency Conversion Usage
```python
from google_tools import GoogleTools as tools

# `only_float=True`
>>> result = tools.currency_conversion(base_currency='USD', target_currency='BRL')
>>> print(result)
4.9024

# `only_float=False`
>>> result = tools.currency_conversion(base_currency='USD', target_currency='BRL', only_float=False)
>>> print(result) # don't looks like it on terminal, just prettyfied it
{
    'conversion': [
        '1 USD',
        '4.90 BRL'
    ],
    'float': 4.9024,
    'last_update': 'Nov 25, 4:38:00 PM UTC'
}

# setting up a benchmark
import time
def currency_conversion_test(n: int, only_float_: bool = True):
    start_timer = time.time()
    for i in range(n):
        tools.currency_conversion('USD', 'BRL', only_float=only_float_)
    finish_timer = time.time() - start_timer
    avg_time = finish_timer / n
    print(avg_time:.3f)

# 1st benchmarking:
>>> currency_conversion_test(30)
1.114 seconds per operation.

# 2nd benchmarking:
>>> currency_conversion_test(30, False)
1.191 seconds per operation.
```

## Translater Usage
```python
from google_tools import GoogleTools as tools

>>> result = tools.translater(source_language='pt', target_language='en', text='Ola Mundo!')
>>> print(result) # maybe it take around 5-10 seconds to respond, depends on your cpu, selenium is a bit slow
Hello World!

# setting up a benchmark
import time
def translater_test(n: int, source_language_: str, target_language_: str, text_: str):
    start_timer = time.time()
    for i in range(n):
        tools.translater(source_language_, target_language_, text_)
    finish_timer = time.time() - start_timer
    avg_time = finish_timer / n
    print(avg_time:.3f)

>>> translater_test(10, 'pt', 'en', 'Ola, me chamo Joao Zacchello!')
6.123
```

### Disclaimer
This library is provided for educational purposes only and should not be used in production environments. It is not affiliated with Google and may not always provide accurate or up-to-date currency conversion rates. For real-time currency conversion services, please refer to official financial sources.
