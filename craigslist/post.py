import logging
import lxml.html

logger = logging.getLogger(__name__)

def process_post_url(url, get):
    logger.debug("downloading %s" % url)
    body = get(url)
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
