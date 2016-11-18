craigslist [**pre-alpha**]
==========================

|Travis CI Status| |Coverage Status| |License Status|

Python wrapper for craigslist.

Install
-------

::

    pip3 install --upgrade git+https://github.com/AlJohri/craigslist.git

CLI
---

::

    $ craigslist --help
    usage: craigslist [-h] {search} ...

    examples:
    craigslist search washingtondc apa --postal 20071 --search_distance 1
    craigslist search newyork aap --postal 10023 --search_distance 1 --hasPic --availabilityMode within_30_days --limit 100
    craigslist search sfbay ccc --postal 94305 --search_distance 1 --limit 10
    craigslist search vancouver sss "shoes" --condition new like_new --hasPic --max_price 20 --limit 10
    craigslist search washingtondc jjj --is_telecommuting --is_internship

    positional arguments:
      {search}
        search    search craigslist

    optional arguments:
      -h, --help  show this help message and exit

For more details, try:

::

    $ craigslist search --help

API
---

See the `examples <./examples>`__ folder.

.. code:: python

    import craigslist

    for post in craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1):
        print(post)
    
    post = craigslist.get('https://washingtondc.craigslist.org/nva/apa/5875729002.html')

Development
-----------

Setup
~~~~~

::

    make virtualenv install

Test
~~~~

::

    workon craigslist
    py.test

Disclaimer
----------

-  This library is not associated with Craigslist.
-  Please read the Craigslist `terms of
   use <https://www.craigslist.org/about/terms.of.use.en>`__.

.. |Travis CI Status| image:: https://travis-ci.org/AlJohri/craigslist.svg?branch=master
   :target: https://travis-ci.org/AlJohri/craigslist
.. |Coverage Status| image:: https://coveralls.io/repos/github/AlJohri/craigslist/badge.svg?branch=master
   :target: https://coveralls.io/github/AlJohri/craigslist?branch=master
.. |License Status| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/AlJohri/craigslist/master/LICENSE
