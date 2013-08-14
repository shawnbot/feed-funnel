# Feed Funnel
Feed Funnel is a Python utility for aggregating multiple feed sources (RSS or
Atom; anything that
[feedparser](http://pythonhosted.org/feedparser/introduction.html) can handle)
into JSON data sources that can be easily templatized into HTML or feed
formats.

## Usage
funnel.py takes one or more feed URLs as positional arguments and produces JSON
on stdout, e.g.

```sh
$ funnel.py http://www.theverge.com/rss/index.xml > theverge.json
```

```
Usage: funnel.py [options] URL1 [URL2 [...]]

Options:
  -h, --help            show this help message and exit
  -L LIMIT, --limit=LIMIT
                        How many items to include in the output (default: 100)
```


