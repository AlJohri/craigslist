from craigslist.search import (
    jsonsearch, async_jsonsearch,
    regularsearch, async_regularsearch)

def search(area, category, type_="jsonsearch", **kwargs):
    if type_ == "jsonsearch":
        return jsonsearch(area, category, type_, **kwargs)
    elif type_ == "regularsearch":
        return regularsearch(area, category, type_, **kwargs)
    else:
        raise Exception("unknown search type")

async def async_search(area, category, type_="jsonsearch", **kwargs):
    if type_ == "jsonsearch":
        return async_jsonsearch(area, category, type_, **kwargs)
    elif type_ == "regularsearch":
        return async_regularsearch(area, category, type_, **kwargs)
    else:
        raise Exception("unknown search type")
