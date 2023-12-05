from setuptools import setup

with open("README.md", "r") as file:
    readme = file.read()

setup(
    name='google-tools-wrapper',
    version='1.5.0',
    license='MIT License',
    author='João Zacchello',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='xongsdartx@gmail.com',
    keywords=['google tools', 'google finance', 'google api', 'currency conversion', 'google translater', 'google tradutor'],
    description=u'An unofficial Google Tools wrapper',
    packages=['google_tools'],
    install_requires=['selenium', 'requests', 'bs4'],
)

#comandos:
# criar empacotamento: python.exe setup.py sdist
# enviar para pypi: twine upload dist/*
#pegue uma api key pro projeto no pypi: https://pypi.org/manage/account/token/
#pypi-AgEIcHlwaS5vcmcCJDFhMDQ4ZmRjLWU0N2EtNDEyNS1iMjA1LTI4MWYwMTJlY2I5OQACHFsxLFsiZ29vZ2xlLXRvb2xzLXdyYXBwZXIiXV0AAixbMixbImZlMzVhODZjLTMyNzQtNDAzMS1hYzBmLTEzODJmYWE5YTM0MSJdXQAABiAok4uusX74-sb4GnJAs8bSRhF2XhJUnlj42xRBvJCvzA