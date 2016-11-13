async def async_process_post_url(url):
    logger.debug("downloading %s" % url)
    body = await get(url)
    return process_post_url_output(body)