import os

def search(area, category, type_="jsonsearch", get_detailed_posts=False, cache=True, cachedir=os.path.expanduser('~'), **kwargs):
    from craigslist._search import jsonsearch, regularsearch

    if type_ == "jsonsearch":
        return jsonsearch(area, category, type_, get_detailed_posts, cache, cachedir, **kwargs)
    elif type_ == "regularsearch":
        return regularsearch(area, category, type_, get_detailed_posts, cache, cachedir, **kwargs)
    else:
        raise Exception("unknown search type")

del os