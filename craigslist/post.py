import logging
import lxml.html

logger = logging.getLogger(__name__)

def process_post_url(url, get):
    logger.debug("downloading %s" % url)
    body = get(url)
    return process_post_url_output(body)

async def async_process_post_url(url, get):
    logger.debug("downloading %s" % url)
    body = await get(url)
    return process_post_url_output(body)

def process_post_url_output(body):
    doc = lxml.html.fromstring(body)
    # lxml.html.tostring(doc.cssselect("#postingbody")[0])
    # doc.cssselect("div.mapaddress")[0].text
    # doc.cssselect("div.mapAndAttrs p.attrgroup") ????
    # "".join([x.text_content() for x in doc.cssselect("h2.postingtitle span.postingtitletext")[0].getchildren()[:-1]])
    # doc.cssselect("h2.postingtitle span.postingtitletext #titletextonly")[0].text
    # [a.get('href') for a in doc.cssselect("#thumbs a")]
    import pdb; pdb.set_trace()
    post = body # parse stuff
    return post