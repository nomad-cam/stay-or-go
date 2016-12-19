import feedparser

def fetch_cfa_tfb_rss():
    feed = feedparser.parse("http://www.cfa.vic.gov.au/restrictions/tfbfdrforecast_rss.xml")
    print (feed)

    return feed

