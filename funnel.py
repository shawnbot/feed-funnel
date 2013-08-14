#!/usr/bin/env python
import feedparser
import time, datetime
import json

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
            'title': parsed.feed.title,
            'href': get_href(parsed.feed.links)
        }
        for entry in parsed.entries:
            entries.append({
                'feed':         feed,
                'title':        entry.title,
                'href':         get_href(entry.links),
                'date_parsed':  entry.date_parsed,
                'author':       entry.author,
                'content':      entry.content[0].get('value'),
                'updated':      entry.updated,
            })
    sorted_entries = sorted(entries, key=lambda entry: entry["date_parsed"])
    sorted_entries.reverse()
    if limit > 0:
        return sorted_entries[0:limit]
    return sorted_entries

def get_href(links, _type='text/html'):
    filtered = filter(lambda ln: ln['type'] == _type, links)
    return len(filtered) and filtered[0].get('href') or None

class FeedJSONEncoder(json.JSONEncoder):
    def default(self, d):
        if type(d) is time.struct_time:
            return time.strftime('%X', d)
        return d

if __name__ == '__main__':
    import optparse
    import json, sys

    parser = optparse.OptionParser(usage="%prog [options] URL1 [URL2 [...]]")
    parser.add_option('--limit', '-L', dest='limit', type='int', default=100, help="""
    How many items to include in the output (default: %default)
    """.strip())
    options, urls = parser.parse_args()

    if len(urls) == 0:
        parser.print_help()
        sys.exit(1)

    entries = funnel(urls, limit=options.limit)
    json.dump(entries, sys.stdout, separators=(', ', ': '), indent=2, cls=FeedJSONEncoder)
