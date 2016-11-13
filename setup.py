#!/usr/bin/env python3

import pypandoc
from setuptools import setup, find_packages

long_description = pypandoc.convert('README.md', 'rst')
long_description = long_description.replace("\r","")

setup(
    name='craigslist',
    version='0.1.0',
    description='Python wrapper for craigslist.',
    long_description=long_description,
    author='Al Johri',
    author_email='al.johri@gmail.com',
    url='https://github.com/AlJohri/craigslist',
    license='MIT',
    packages=find_packages(),
    package_data={'craigslist': ['data/*.json']},
    install_requires=['requests', 'cssselect', 'lxml', 'blessings'],
    entry_points={
        'console_scripts': [
            'craigslist=craigslist.cli:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ]
)
