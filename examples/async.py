#!/usr/bin/env python3

import asyncio
import craigslist

async def main():
    async for post in craigslist.search_async('washingtondc', 'apa', postal=20071, search_distance=1):
        print(post)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
