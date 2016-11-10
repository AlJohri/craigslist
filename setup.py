from setuptools import setup

setup(
    name='craigslist',
    version='0.1.0',
    description='Python wrapper for craigslist.',
    author='Al Johri',
    author_email='al.johri@gmail.com',
    url='https://github.com/AlJohri/craigslist',
    packages=['craigslist', 'craigslist.search'],
    package_data={'craigslist': ['data/*.json']},
    install_requires=['requests', 'cssselect', 'lxml', 'blessings'],
    entry_points={
        'console_scripts': [
            'craigslist=craigslist.cli:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.5',
    ]
)
