import os

async def search(area, category, type_="jsonsearch", get_detailed_posts=False, cache=True, cachedir=os.path.expanduser('~'), **kwargs):
    from craigslist._search import async_jsonsearch, async_regularsearch

    if type_ == "jsonsearch":
        return async_jsonsearch(area, category, type_, get_detailed_posts, cache, cachedir, **kwargs)
    elif type_ == "regularsearch":
        return async_regularsearch(area, category, type_, get_detailed_posts, cache, cachedir, **kwargs)
    else:
        raise Exception("unknown search type")

del os