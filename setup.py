from setuptools import setup

setup(
    name='craigslist',
    version='0.1.0',
    packages=['craigslist'],
    install_requires=['requests', 'cssselect', 'lxml', 'simplejson'],
    entry_points={
        'console_scripts': [
            'craigslist=craigslist.cli:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.5',
    ]
)
