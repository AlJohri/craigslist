import logging
import lxml.html
from collections import namedtuple

logger = logging.getLogger(__name__)

DetailPost = namedtuple('DetailPost', [
    'full_title', 'address'])

async def async_process_post_url(url):
    logger.debug("downloading %s" % url)
    body = await get(url)
    return process_post_url_output(body)

def process_post_url_output(body):
    doc = lxml.html.fromstring(body)
    lxml.html.tostring(doc.cssselect("#postingbody")[0])
    full_title = "".join([x.text_content() for x in doc.cssselect("h2.postingtitle span.postingtitletext")[0].getchildren()[:-1]])
    try:
        address = doc.cssselect("div.mapaddress")[0].text
    except IndexError:
        address = None
    # doc.cssselect("div.mapAndAttrs p.attrgroup") ????
    # doc.cssselect("h2.postingtitle span.postingtitletext #titletextonly")[0].text
    # [a.get('href') for a in doc.cssselect("#thumbs a")]
    return DetailPost(full_title=full_title, address=address)