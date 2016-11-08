import json
from datetime import datetime, timezone
from craigslist.models import JSONSearchCluster, JSONSearchPost
from craigslist.utils import cdn_url_to_http

def parse_cluster_url_output(body):
    items, meta = json.loads(body)
    baseurl = cdn_url_to_http(meta['baseurl'])
    posts = [parse_post(x)
        for x in items if not x.get('GeoCluster')]
    clusters = [parse_cluster(x, baseurl)
        for x in items if x.get('GeoCluster')]
    return posts, clusters

def parse_cluster(cluster, baseurl):
    return JSONSearchCluster(**{
        'id': cluster['GeoCluster'],
        'url': baseurl + cluster['url'],
        'longitude': cluster['Longitude'],
        'latitude': cluster['Latitude'],
        'num_posts': cluster['NumPosts'],
        'posting_ids': cluster['PostingID'].split(','),
        'date': datetime.fromtimestamp(float(cluster['PostedDate']), timezone.utc).isoformat()
    })

def parse_post(post):
    return JSONSearchPost(**{
        'id': post['PostingID'],
        'title': post['PostingTitle'],
        'url': cdn_url_to_http(post['PostingURL']),
        'longitude': post['Longitude'],
        'latitude': post['Latitude'],
        'price': post['Ask'],
        'bedrooms': post['Bedrooms'],
        'date': datetime.fromtimestamp(float(post['PostedDate']), timezone.utc).isoformat(),
        'thumbnail': post.get('ImageThumb'),
        'category_id': post['CategoryID'],
    })

from craigslist.search.jsonsearch.sync import jsonsearch
from craigslist.search.jsonsearch.async import jsonsearch as async_jsonsearch
