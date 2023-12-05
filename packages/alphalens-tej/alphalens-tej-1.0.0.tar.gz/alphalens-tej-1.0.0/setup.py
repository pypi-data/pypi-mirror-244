# coding=UTF-8
import sys
from pathlib import Path
from setuptools import Extension, setup  # noqa: E402


  


install_requires = [
    'seaborn',
    'scipy',
]

installs_for_two = [
    'pyOpenSSL',
    'ndg-httpsclient',
    'pyasn1'
]

if sys.version_info[0] < 3:
    install_requires += installs_for_two

packages = [
'alphalens',
'alphalens.tests'
]

setup(
    name='alphalens-tej',
    description='modified alphalens-reloaded=0.4.2.',
    keywords=['tej', 'big data', 'data', 'financial', 'economic','stock','TEJ',],
    version='1.0.0',
    author='tej',
    author_email='tej@tej.com.tw',
    maintainer='tej api Development Team',
    maintainer_email='tej@tej.com',
    url='https://api.tej.com.tw',
    license='MIT',
    install_requires=install_requires,
    tests_require=[
        'unittest2',
        'flake8',
        'nose',
        'httpretty',
        'mock',
        'factory_boy',
        'jsondate'
    ],
    test_suite="nose.collector",
    
    packages=packages,
    package_data = {'': ['*.csv','*.xlsx',]},
    include_package_data=True,
    
    python_requires=">=3.8"
)