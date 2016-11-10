#!/usr/bin/env python3.6
"""
This example requires python 3.6 which is scheduled to be released by end of 2016.

Until then, you can get Python 3.6 like so:

brew install mercurial
brew install pyenv --HEAD
brew install pyenv-virtualenvwrapper
pyenv install 3.6.0b3

I use homebrew python (which is the system python as far as pyenv is concerned) so
I set up my global python to prefer system first and then look for the new version.
This gives us the `python3.6` command in our PATH.

pyenv global system 3.6.0b3
"""

from craigslist.api.async import search

async def main():
    async for post in search('washingtondc', 'apa', postal=20071, search_distance=1):
        print(post)

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()