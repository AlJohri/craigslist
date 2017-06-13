import re
import logging
import lxml.html
import asyncio
import concurrent.futures
from collections import namedtuple
from craigslist.utils import get_only_first_or_none
from craigslist.io import requests_get, asyncio_get
from craigslist.exceptions import (
    CraigslistException, CraigslistValueError)

logger = logging.getLogger(__name__)

DetailPost = namedtuple('DetailPost', [
    'id', 'repost_id', 'url', 'full_title', 'short_title', 'hood', 'num_bedrooms', 'sqftage', 'price',
    'body_html', 'body_text', 'address'])

# http://washingtondc.craigslist.org/doc/apa/5870605045.html
# http://washingtondc.craigslist.org/fb/wdc/apa/5870605045
# http://washingtondc.craigslist.org/reply/wdc/apa/5870605045

def parse_housing_el(housing_el_text):
    housing = [x.strip() for x in housing_el_text.split(" - ") if x.strip()]
    bedrooms_raw = get_only_first_or_none([x for x in housing if "br" in x])
    num_bedrooms = int(bedrooms_raw.replace("br", "")) if bedrooms_raw else None
    area_raw = get_only_first_or_none([x for x in housing if "ft" in x])
    area = int(area_raw.replace("ft", "")) if area_raw else None
    return num_bedrooms, area

def http_to_https(url):
    if url.startswith("http://"):
        return url.replace("http://", "https://", 1)

def process_post_url_output(body):

    if "<title>craigslist | post not found</title>" in body or '<title>craigslist | Page Not Found</title>' in body:
        raise CraigslistException("post not found")

    try:
        id_ = int(re.search(r'var pID = "(\d+)";', body).groups()[0])
    except IndexError:
        raise CraigslistException("post id not found on page")

    try:
        repost_id = re.search(r'var repost_of = (\d+);', body).groups()[0]
    except AttributeError:
        repost_id = None

    doc = lxml.html.fromstring(body)
    url = http_to_https(doc.cssselect("link[rel=canonical]")[0].get('href'))
    full_title = " ".join([x.text_content() for x in doc.cssselect("h2.postingtitle span.postingtitletext")[0].getchildren()[:-1]])
    short_title = doc.cssselect("h2.postingtitle span.postingtitletext #titletextonly")[0].text

    try:
        # TODO: deal with international prices
        price = doc.cssselect("h2.postingtitle span.postingtitletext .price")[0].text.replace('$', '')
    except IndexError:
        price = None

    try:
        housing_el = doc.cssselect("h2.postingtitle span.postingtitletext .housing")[0]
    except IndexError:
        housing_el = None

    if housing_el is not None:
        try:
            num_bedrooms, area = parse_housing_el(housing_el.text.replace('/ ', ''))
        except Exception:
            num_bedrooms, area = None, None
    else:
        num_bedrooms, area = None, None

    try:
        hood = doc.cssselect("h2.postingtitle span.postingtitletext #titletextonly + small")[0].text.strip().lstrip('(').rstrip(')')
    except IndexError:
        hood = None

    try:
        address = doc.cssselect("div.mapaddress")[0].text
    except IndexError:
        address = None

    body_el = doc.cssselect("#postingbody")[0]
    el_to_remove = body_el.cssselect('div.print-qrcode-container')[0]
    body_el.remove(el_to_remove)
    body_html = lxml.html.tostring(body_el).decode('utf-8')
    body_text = body_el.text_content()
    # doc.cssselect("div.mapAndAttrs p.attrgroup") ????
    # [a.get('href') for a in doc.cssselect("#thumbs a")]
    return DetailPost(
        id=id_,
        repost_id=repost_id,
        url=url,
        full_title=full_title,
        short_title=short_title,
        hood=hood,
        num_bedrooms=num_bedrooms,
        sqftage=area,
        price=price,
        body_html=body_html,
        body_text=body_text,
        address=address)

def process_post_url(url, get):
    logger.debug("downloading %s" % url)
    body = get(url)
    return process_post_url_output(body)

def get_post(post_url, get=requests_get):
  return process_post_url(post_url, get)

def get_posts(post_urls, executor, get=requests_get, as_completed=concurrent.futures.as_completed):
    futures = (executor.submit(
        process_post_url, url, get) for url in post_urls)
    try:
        yield from (future.result() for future in as_completed(futures))
    except KeyboardInterrupt: # pragma: no cover
        for future in futures:
            future.cancel()

async def process_post_url_async(url, get=asyncio_get):
    logger.debug("downloading %s" % url)
    body = await get(url)
    return process_post_url_output(body)

async def get_post_async(post_url, get=asyncio_get):
    return await process_post_url_async(post_url, get)

async def get_posts_async(post_urls, get=asyncio_get, as_completed=asyncio.as_completed):
    futures = [process_post_url_async(url, get) async for url in post_urls]
    try:
        for future in as_completed(futures):
            post = await future
            yield post
    except KeyboardInterrupt: # pragma: no cover
        for future in futures:
            future.cancel()
