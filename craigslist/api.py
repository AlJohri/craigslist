def search(area, category, type_="jsonsearch", get_detailed_posts=False, **kwargs):
    from craigslist.search import jsonsearch, regularsearch

    if type_ == "jsonsearch":
        return jsonsearch(area, category, type_, get_detailed_posts, **kwargs)
    elif type_ == "regularsearch":
        return regularsearch(area, category, type_, get_detailed_posts, **kwargs)
    else:
        raise Exception("unknown search type")

async def async_search(area, category, type_="jsonsearch", get_detailed_posts=False, **kwargs):
    from craigslist.search import async_jsonsearch, async_regularsearch

    if type_ == "jsonsearch":
        return async_jsonsearch(area, category, type_, get_detailed_posts, **kwargs)
    elif type_ == "regularsearch":
        return async_regularsearch(area, category, type_, get_detailed_posts, **kwargs)
    else:
        raise Exception("unknown search type")
