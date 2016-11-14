from collections import namedtuple
from craigslist._search import get_query_url

RegularSearchPost = namedtuple('RegularSearchPost', [
    'id',
    'title',
    'url',
    'repost_id',
    'price',
    'bedrooms',
    'date',
    'area'])

def get_current_offset_from_response(doc):
    return int(doc.cssselect("#searchform span.pagenum span.rangeFrom")[0].text)

def get_number_of_posts_on_current_page_from_response(doc):
    return int(doc.cssselect("#searchform span.pagenum span.rangeTo")[0].text)

def get_num_total_posts_from_response(doc):
    return int(doc.cssselect("#searchform span.pagenum span.totalcount")[0].text)

"""
<li class="result-row" data-pid="5845148702" data-repost-of="4498926447">
    <a href="/mld/apa/5845148702.html" class="result-image gallery" data-ids="1:00q0q_5EtzvO5E6uB,1:01515_j7ikj9nPJw5,1:00S0S_kakmbFGH9PU,1:00p0p_duCoSkucViU,1:00K0K_d0X3UCh9eoZ,1:00m0m_6mGTuKuRSPD,1:00A0A_e6vzdNg86YN">
        <span class="result-price">$1500</span>
    </a>
    <p class="result-info">
        <span class="icon icon-star" role="button" title="save this post in your favorites list">
            <span class="screen-reader-text">favorite this post</span>
        </span>
        <time class="result-date" datetime="2016-11-14 02:34" title="Mon 14 Nov 02:34:33 AM">Nov 14</time>
        <a href="/mld/apa/5845148702.html" data-id="5845148702" class="result-title hdrlnk">Cozy Rambler - Available Upon Approval</a>
        <span class="result-meta">
            <span class="result-price">$1500</span>
            <span class="housing">
                3br -
                1000ft<sup>2</sup> -
            </span>
            <span class="result-hood"> (District Heights, MDD)</span>
            <span class="result-tags">
                pic
                <span class="maptag" data-pid="5845148702">map</span>
            </span>
            <span class="banish icon icon-trash" role="button">
                <span class="screen-reader-text">hide this posting</span>
            </span>
            <span class="unbanish icon icon-trash red" role="button" aria-hidden="true"></span>
            <a href="#" class="restore-link">
                <span class="restore-narrow-text">restore</span>
                <span class="restore-wide-text">restore this posting</span>
            </a>
        </span>
    </p>
</li>
"""

def parse_post(post):
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
    num_bedrooms = int(bedrooms_raw.replace("br", "")) if bedrooms_raw else None
    area_raw = get_only_first_or_none([x for x in housing if "ft" in x])
    area = int(area_raw.replace("ft", "")) if area_raw else None
    return RegularSearchPost(**{
        "id": pid,
        "title": title,
        "url": url,
        "respost_id": respost_pid,
        "price": price,
        "bedrooms": num_bedrooms,
        "date": date,
        "area": area,
    })

def process_page_url(url, get):
    logger.debug("downloading %s" % url)
    body = get(url)
    return parse_page_url_output(body)

# def get_posts_from_response(doc):
#     for post in doc.cssselect("#sortable-results > div.rows > p"):
#         yield parse_post(post)

def parse_page_url_output(body):
    return body

from craigslist._search.regularsearch.sync import regularsearch