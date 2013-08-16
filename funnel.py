#!/usr/bin/env python
import feedparser
from dateutil.parser import parser as dateutil_parser
import json

parse_date = dateutil_parser().parse
def coerce_date_str(date_str):
    parsed = parse_date(date_str)
    return parsed.strftime("%Y-%m-%dT%H:%M:%SZ")

def funnel(feeds, limit=100, **options):
    def to_feed(feed):
        f = {}
        f.update(options)
        if type(feed) is dict:
            f.update(feed)
        else:
            f['url'] = feed
        return f
    feeds = map(lambda feed: to_feed(feed), feeds)
    entries = []
    for feed in feeds:
        url = feed['url']
        del feed['url']
        parsed = feedparser.parse(url, **feed)
        feed = {
            'title': hasattr(parsed.feed, 'title') and parsed.feed.title or '',
            'href': hasattr(parsed.feed, 'links') and get_href(parsed.feed.links) or ''
        }
        for entry in parsed.entries:
            try:
                content = entry.content[0].get('value')
            except:
                content = entry.summary_detail.get('value')
            entries.append({
                'feed':         feed,
                'title':        entry.title,
                'href':         get_href(entry.links),
                'updated':      entry.updated,
                'date':         coerce_date_str(entry.updated),
                'author':       entry.author,
                'content':      content
            })
    sorted_entries = sorted(entries, key=lambda entry: entry['date'], reverse=True)
    if limit > 0:
        return sorted_entries[0:limit]
    return sorted_entries

def get_href(links, _type='text/html'):
    filtered = filter(lambda ln: ln.get('type') == _type, links)
    return len(filtered) and filtered[0].get('href') or None

class FeedJSONEncoder(json.JSONEncoder):
    def default(self, d):
        if type(d) is time.struct_time:
            return time.strftime('%X', d)
        return d

if __name__ == '__main__':
    import optparse
    import json, sys

    parser = optparse.OptionParser(usage='%prog [options] URL1 [URL2 [...]]')
    parser.add_option('--limit', '-L', dest='limit', type='int', default=100, help="""
    How many items to include in the output (default: %default)
    """.strip())
    options, urls = parser.parse_args()

    if len(urls) == 0:
        parser.print_help()
        sys.exit(1)

    entries = funnel(urls, limit=options.limit)
    json.dump(entries, sys.stdout, separators=(', ', ': '), indent=2, cls=FeedJSONEncoder)
