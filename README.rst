craigslist
==========================

|Travis CI Status| |Coverage Status| |PyPi Version| |License Status|

Python wrapper for craigslist. Requires Python 3.6+.

Install
-------

::

    pip3 install --upgrade craigslist

CLI
---

::

    $ craigslist
    usage: craigslist [-h] {search,list} ...

    examples:
    craigslist search worcester apa
    craigslist search newyork tlg
    craigslist search sfbay mis
    craigslist search washingtondc apa --postal 20071 --search_distance 1
    craigslist search newyork aap --postal 10023 --search_distance 1 --hasPic --availabilityMode within_30_days --limit 100
    craigslist search sfbay ccc --postal 94305 --search_distance 1 --limit 10
    craigslist search vancouver sss "shoes" --condition new like_new --hasPic --max_price 20 --limit 10
    craigslist search washingtondc jjj --is_telecommuting --is_internship
    craigslist list areas
    craigslist list categories

    positional arguments:
      {search,list}
        search       search
        list         list

    optional arguments:
      -h, --help     show this help message and exit

For more details, try:

::

    $ craigslist search
    $ craigslist list

API
---

See the `examples <./examples>`__ folder.

`simple <./examples/simple.py>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import craigslist

    for post in craigslist.search('washingtondc', 'apa', postal=20071, search_distance=1):
        print(post)

    # craiglist posts expire. replace the url below with something current
    post = craigslist.get('https://washingtondc.craigslist.org/nva/apa/5875729002.html')

`async <./examples/async.py>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

  import asyncio
  import craigslist

  async def main():
      async for post in craigslist.search_async('washingtondc', 'apa', postal=20071, search_distance=1):
          print(post)

      # craiglist posts expire. replace the url below with something current
      post = await craigslist.get_async('https://washingtondc.craigslist.org/nva/apa/5875729002.html')

  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
  loop.close()

Development
-----------

Setup
~~~~~

::

    make install

Test
~~~~

::

    make test

Disclaimer
----------

-  This library is not associated with Craigslist.
-  Please read the Craigslist `terms of
   use <https://www.craigslist.org/about/terms.of.use.en>`__.

.. |Travis CI Status| image:: https://travis-ci.org/AlJohri/craigslist.svg?branch=master
   :target: https://travis-ci.org/AlJohri/craigslist
.. |Coverage Status| image:: https://coveralls.io/repos/github/AlJohri/craigslist/badge.svg?branch=master
   :target: https://coveralls.io/github/AlJohri/craigslist?branch=master
.. |PyPI Version| image:: https://img.shields.io/pypi/v/craigslist.svg
   :target: https://pypi.python.org/pypi/craigslist
.. |License Status| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/AlJohri/craigslist/master/LICENSE
