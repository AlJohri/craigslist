import logging
import lxml.html
from collections import namedtuple
from concurrent.futures import as_completed
from craigslist.utils import get_only_first_or_none

logger = logging.getLogger(__name__)

DetailPost = namedtuple('DetailPost', [
    'full_title', 'short_title', 'hood', 'num_bedrooms', 'sqftage', 'price',
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

"""
<h2 class="postingtitle">
    <span class="icon icon-star" role="button">
        <span class="screen-reader-text">favorite this post</span>
    </span>
    <span class="postingtitletext">
<span class="price">$3000</span> <span class="housing">/ 2br - </span><span id="titletextonly">Columbia Heights. Brand New 2 Bed/2 Bath</span><small> (3035 15th Street, NW)</small>        <span class="js-only banish-unbanish">
  <span class="banish" role="button">
    <span class="icon icon-trash" aria-hidden="true"></span>
    <span class="screen-reader-text">hide this posting</span>
  </span>
  <span class="unbanish" role="button">
    <span class="icon icon-trash red" aria-hidden="true"></span>
    unhide
  </span>
</span>
    </span>
</h2>
"""

"""
<section class="userbody">
  <figure class="iw multiimage">
    <div id="thumbs"><a id="1_thumb_5EtzvO5E6uB" class="thumb" data-imgid="5EtzvO5E6uB" href="https://images.craigslist.org/00q0q_5EtzvO5E6uB_600x450.jpg" title="1"><img src="https://images.craigslist.org/00q0q_5EtzvO5E6uB_50x50c.jpg" class="selected" alt=" 1"></a><a id="2_thumb_j7ikj9nPJw5" class="thumb" data-imgid="j7ikj9nPJw5" href="https://images.craigslist.org/01515_j7ikj9nPJw5_600x450.jpg" title="2"><img src="https://images.craigslist.org/01515_j7ikj9nPJw5_50x50c.jpg" alt=" 2"></a><a id="3_thumb_kakmbFGH9PU" class="thumb" data-imgid="kakmbFGH9PU" href="https://images.craigslist.org/00S0S_kakmbFGH9PU_600x450.jpg" title="3"><img src="https://images.craigslist.org/00S0S_kakmbFGH9PU_50x50c.jpg" alt=" 3"></a><a id="4_thumb_duCoSkucViU" class="thumb" data-imgid="duCoSkucViU" href="https://images.craigslist.org/00p0p_duCoSkucViU_600x450.jpg" title="4"><img src="https://images.craigslist.org/00p0p_duCoSkucViU_50x50c.jpg" alt=" 4"></a><a id="5_thumb_d0X3UCh9eoZ" class="thumb" data-imgid="d0X3UCh9eoZ" href="https://images.craigslist.org/00K0K_d0X3UCh9eoZ_600x450.jpg" title="5"><img src="https://images.craigslist.org/00K0K_d0X3UCh9eoZ_50x50c.jpg" alt=" 5"></a><a id="6_thumb_6mGTuKuRSPD" class="thumb" data-imgid="6mGTuKuRSPD" href="https://images.craigslist.org/00m0m_6mGTuKuRSPD_600x450.jpg" title="6"><img src="https://images.craigslist.org/00m0m_6mGTuKuRSPD_50x50c.jpg" alt=" 6"></a><a id="7_thumb_e6vzdNg86YN" class="thumb" data-imgid="e6vzdNg86YN" href="https://images.craigslist.org/00A0A_e6vzdNg86YN_600x450.jpg" title="7"><img src="https://images.craigslist.org/00A0A_e6vzdNg86YN_50x50c.jpg" alt=" 7"></a></div>

    <script type="text/javascript"><!--
    var imgList = [{"shortid":"5EtzvO5E6uB","url":"https://images.craigslist.org/00q0q_5EtzvO5E6uB_600x450.jpg","thumb":"https://images.craigslist.org/00q0q_5EtzvO5E6uB_50x50c.jpg","imgid":"1:00q0q_5EtzvO5E6uB"},{"shortid":"j7ikj9nPJw5","url":"https://images.craigslist.org/01515_j7ikj9nPJw5_600x450.jpg","thumb":"https://images.craigslist.org/01515_j7ikj9nPJw5_50x50c.jpg","imgid":"1:01515_j7ikj9nPJw5"},{"shortid":"kakmbFGH9PU","url":"https://images.craigslist.org/00S0S_kakmbFGH9PU_600x450.jpg","thumb":"https://images.craigslist.org/00S0S_kakmbFGH9PU_50x50c.jpg","imgid":"1:00S0S_kakmbFGH9PU"},{"shortid":"duCoSkucViU","url":"https://images.craigslist.org/00p0p_duCoSkucViU_600x450.jpg","thumb":"https://images.craigslist.org/00p0p_duCoSkucViU_50x50c.jpg","imgid":"1:00p0p_duCoSkucViU"},{"shortid":"d0X3UCh9eoZ","url":"https://images.craigslist.org/00K0K_d0X3UCh9eoZ_600x450.jpg","thumb":"https://images.craigslist.org/00K0K_d0X3UCh9eoZ_50x50c.jpg","imgid":"1:00K0K_d0X3UCh9eoZ"},{"shortid":"6mGTuKuRSPD","url":"https://images.craigslist.org/00m0m_6mGTuKuRSPD_600x450.jpg","thumb":"https://images.craigslist.org/00m0m_6mGTuKuRSPD_50x50c.jpg","imgid":"1:00m0m_6mGTuKuRSPD"},{"shortid":"e6vzdNg86YN","url":"https://images.craigslist.org/00A0A_e6vzdNg86YN_600x450.jpg","thumb":"https://images.craigslist.org/00A0A_e6vzdNg86YN_50x50c.jpg","imgid":"1:00A0A_e6vzdNg86YN"}];
    --></script>

  </figure>
  <div class="mapAndAttrs">
    <div class="mapbox">
      <div id="map" class="viewposting leaflet-container leaflet-fade-anim" data-latitude="38.853900" data-longitude="-76.889100" data-accuracy="22" tabindex="0"><div class="leaflet-map-pane" style="transform: translate3d(0px, 0px, 0px);"><div class="leaflet-tile-pane"><div class="leaflet-layer"><div class="leaflet-tile-container"></div><div class="leaflet-tile-container leaflet-zoom-animated"><img class="leaflet-tile leaflet-tile-loaded" src="//map9.craigslist.org/t09/13/2345/3134.png" style="height: 256px; width: 256px; left: -186px; top: -128px;"><img class="leaflet-tile leaflet-tile-loaded" src="//map0.craigslist.org/t09/13/2346/3134.png" style="height: 256px; width: 256px; left: 70px; top: -128px;"><img class="leaflet-tile leaflet-tile-loaded" src="//map0.craigslist.org/t09/13/2345/3135.png" style="height: 256px; width: 256px; left: -186px; top: 128px;"><img class="leaflet-tile leaflet-tile-loaded" src="//map1.craigslist.org/t09/13/2346/3135.png" style="height: 256px; width: 256px; left: 70px; top: 128px;"></div></div></div><div class="leaflet-objects-pane"><div class="leaflet-shadow-pane"></div><div class="leaflet-overlay-pane"><svg class="leaflet-zoom-animated" width="453" height="427" viewBox="-67 -64 453 427" style="transform: translate3d(-67px, -64px, 0px);"><g><path stroke-linejoin="round" stroke-linecap="round" fill-rule="evenodd" stroke="#770091" stroke-opacity="0.5" stroke-width="1" fill="#770091" fill-opacity="0.1" class="leaflet-clickable" d="M159,49A101,101,0,1,1,158.9,49 z"></path></g></svg></div><div class="leaflet-marker-pane"></div><div class="leaflet-popup-pane"></div></div></div><div class="leaflet-control-container"><div class="leaflet-top leaflet-left"><div class="leaflet-control-zoom leaflet-bar leaflet-control"><a class="leaflet-control-fullscreen leaflet-bar-part leaflet-bar-part-top" href="#" title="Toggle Full Screen"></a><a class="leaflet-control-zoom-in leaflet-bar-part " href="#" title="Zoom in"></a><a class="leaflet-control-zoom-out leaflet-bar-part leaflet-bar-part-bottom" href="#" title="Zoom out"></a></div></div><div class="leaflet-top leaflet-right"></div><div class="leaflet-bottom leaflet-left"></div><div class="leaflet-bottom leaflet-right"><div class="leaflet-control-attribution leaflet-control">© craigslist - Map data © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a></div></div></div></div>
      <div class="mapaddress">Millvale Avenue at Marlboro Pike</div>
      <p class="mapaddress">
        <small>
        (<a target="_blank" href="https://maps.google.com/?q=loc%3A+Millvale+Avenue+at+Marlboro+Pike+District+Heights+DC+US">google map</a>)
        </small>
      </p>
    </div>   <p class="attrgroup">
    <span><b>3BR</b> / <b>1Ba</b></span>
    <span><b>1000</b>ft<sup>2</sup></span>
    <span class="housing_movein_now property_date attr_is_today" data-date="2016-11-01" data-today_msg="available now">available now</span>
  </p>
  <p class="attrgroup">
    <span>cats are OK - purrr</span><br>
    <span>dogs are OK - wooof</span><br>
    <span>house</span><br>
    <span>w/d in unit</span><br>
    <span>off-street parking</span><br>
  </p>
</div>

<div class="postinginfos">
  <p class="postinginfo">post id: 5845148702</p>
  <p class="postinginfo" style="opacity: 1;">posted: <time class="timeago" datetime="2016-10-25T05:54:31-0400" title="2016-10-25  5:54am">20 days ago</time></p>
  <p class="postinginfo" style="opacity: 1;">updated: <time class="timeago" datetime="2016-11-13T21:29:33-0500" title="2016-11-13  9:29pm">20 minutes ago</time></p>
  </div>
</section>
"""

def process_post_url(url, get):
    logger.debug("downloading %s" % url)
    body = get(url)
    return process_post_url_output(body)

def process_post_url_output(body):
    doc = lxml.html.fromstring(body)
    full_title = " ".join([x.text_content() for x in doc.cssselect("h2.postingtitle span.postingtitletext")[0].getchildren()[:-1]])
    short_title = doc.cssselect("h2.postingtitle span.postingtitletext #titletextonly")[0].text
    # TODO: deal with international prices
    price = doc.cssselect("h2.postingtitle span.postingtitletext .price")[0].text.replace('$', '')

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
        full_title=full_title,
        short_title=short_title,
        hood=hood,
        num_bedrooms=num_bedrooms,
        sqftage=area,
        price=price,
        body_html=body_html,
        body_text=body_text,
        address=address)

def get_post(post_url, get):
  return process_post_url(post_url, get)

def get_posts(post_urls, executor, get):
    futures = (executor.submit(
        process_post_url, url, get) for url in post_urls)
    try:
        yield from (future.result() for future in as_completed(futures))
    except KeyboardInterrupt:
        for future in futures:
            future.cancel()

