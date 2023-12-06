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
import google_tools as tools

>>> result = tools.currency_conversion(base_currency='USD', target_currency='BRL')
>>> print(result)
{
    'float': 4.9024,
    'last_update': 'Nov 25, 4:38:00 PM UTC'
}

# benchmark (u can see the benchmark on this project github repo):
>>> result = test_currency_conversion(100)
>>> print(f"MIN TIME: {result['min_time']} seconds\nMAX TIME: {result['max_time']} seconds\nAVG TIME ({result['avg']['operations']} operations): {result['avg']['time_per_operation']} seconds") # "limited" to 3 decimals
MIN TIME: 0.736 seconds
MAX TIME: 2.152 seconds
AVG TIME (100 operations): 1.077 seconds
```

## Translater Usage
```python
import google_tools as tools

>>> result = tools.translater(source_language='pt', target_language='en', text='Ola Mundo!')
>>> print(result)
Hello World!

# benchmark (u can see the benchmark on this project github repo):
>>> result = test_translater(30)
>>> print(f"MIN TIME: {result['min_time']} seconds\nMAX TIME: {result['max_time']} seconds\nAVG TIME ({result['avg']['operations']} operations): {result['avg']['time_per_operation']} seconds") # "limited" to 3 decimals
MIN TIME: 5.195 seconds
MAX TIME: 7.003 seconds
AVG TIME (30 operations): 5.924 seconds
```

### Disclaimer
This library is provided for educational purposes only and should not be used in production environments. It is not affiliated with Google and may not always provide accurate or up-to-date currency conversion rates. For real-time currency conversion services, please refer to official financial sources.
