import arrow
import requests
import lxml.html
from urllib.parse import urlencode
from craigslist.utils import cdn_url_to_http

def get_url_base(city):
    return "https://{}.craigslist.org".format(city)

def get_query_url(city, search_type, offset=0, sort="date", **kwargs):
    params = {"s": offset, "sort": sort, **kwargs}
    params = {k:v for k,v in params.items() if v is not None}
    url = get_url_base(city) + "/{}/apa?{}".format(search_type, urlencode(params))
    return url

def query_jsonsearch(city, sort="date", **kwargs):

    def process_post_json(post):
        return {
            'id': post['PostingID'],
            'title': post['PostingTitle'],
            'url': cdn_url_to_http(post['PostingURL']),
            'longitude': post['Longitude'],
            'latitude': post['Latitude'],
            'price': post['Ask'],
            'bedrooms': post['Bedrooms'],
            'date': arrow.get(post['PostedDate']).isoformat(),
            'thumbnail': post.get('ImageThumb'),
            'category_id': post['CategoryID'],
        }

    def get_posts(url):
        response = requests.get(url)
        items, meta = response.json()
        baseurl = cdn_url_to_http(meta['baseurl'])
        posts = [process_post_json(x) for x in items if not x.get('GeoCluster')]
        clusters = [x for x in items if x.get('GeoCluster')]

        yield from posts
        for cluster in clusters:
            yield from get_posts(baseurl + cluster['url'])

    url = get_query_url(city, "jsonsearch", sort=sort, **kwargs)
    yield from get_posts(url)

def query_regularsearch(city, sort="date", **kwargs):

    def get_current_offset_from_response(doc):
        return int(doc.cssselect("#searchform span.pagenum span.rangeFrom")[0].text)

    def get_number_of_posts_on_current_page_from_response(doc):
        return int(doc.cssselect("#searchform span.pagenum span.rangeTo")[0].text)

    def get_num_total_posts_from_response(doc):
        return int(doc.cssselect("#searchform span.pagenum span.totalcount")[0].text)

    def get_posts_from_response(doc):
        for post in doc.cssselect("#sortable-results > div.rows > p"):
            pid = int(post.get('data-pid'))
            respost_pid = int(post.get('data-repost-of')) if post.get('data-repost-of') else None
            date = arrow.get(post.cssselect('time')[0].get('datetime'))
            url = post.cssselect("span > span > a")[0].get('href')
            title = post.cssselect("span > span > a")[0].text
            price_el = get_only_first_or_none(post.cssselect("span > span > span.price"))
            price_raw = price_el.text if price_el is not None else None
            price = int(price_raw.replace("$", "")) if price_raw else None
            housing_el = get_only_first_or_none(post.cssselect("span > span > span.housing"))
            housing = [x.strip() for x in housing_el.text.split("-\n") \
                if x.strip()] if housing_el is not None else []
            bedrooms_raw = get_only_first_or_none([x for x in housing if "br" in x])
            bedrooms = int(bedrooms_raw.replace("br", "")) if bedrooms_raw else None
            area_raw = get_only_first_or_none([x for x in housing if "ft" in x])
            area = int(area_raw.replace("ft", "")) if area_raw else None
            yield {
                "id": pid,
                "title": title,
                "url": url,
                "respost_id": respost_pid,
                "price": price,
                "bedrooms": num_bedrooms,
                "date": date,
                "area": area,
            }

    doc = lxml.html.fromstring(requests.get(get_query_url(
        city, "search", offset=0, sort=sort, **kwargs)))
    num_total_posts = get_num_total_posts_from_response(doc)
    num_posts_on_page = get_number_of_posts_on_current_page_from_response(doc)
    yield from get_posts_from_response(doc)
    for offset in range(100, num_total_posts, 100):
        doc = lxml.html.fromstring(requests.get(get_query_url(
            city, "search", offset=offset, sort=sort, **kwargs)))
        num_posts_on_page = get_number_of_posts_on_current_page_from_response(doc)
        yield from get_posts_from_response(doc)
