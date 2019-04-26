import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
from datetime import timedelta as td


class OlxRssParser:
    def __init__(self):
        _time = '%d %b %Y %H:%M:%S'
        self.items = dict()
        self.url = 'https://www.olx.ua/rss/'
        self.cdate = dt.strftime(dt.now()-td(minutes=20), _time)

    def get_content(self, url):
        content = requests.get(url)
        content = content.text[1:]
        content = BeautifulSoup(content, 'xml')
        return content

    def get_items(self):
        """ Gets a list of new items from OLX. """
        self.items = dict()
        _time = '%d %b %Y %H:%M:%S'
        content = self.get_content(self.url)
        items  = content.select('item')
        cdate = dt.strptime(self.cdate, _time)
        
        for i, item in enumerate(items):
            idate = item.pubDate.text.strip()
            idate = dt.strptime(idate, '%a, %d %b %Y %H:%M:%S %Z')
            idate = dt.strftime(idate, _time)
            idate = dt.strptime(idate, _time)

            if idate > cdate:
                ititle = item.title.text.strip()
                self.items[ititle] = dict()
                self.items[ititle]['pubDate'] = idate
                self.items[ititle]['link'] = item.link.text.strip()
                self.items[ititle]['guid'] = item.guid.text.strip()
                self.items[ititle]['preview'] = item.preview.text.strip()
                self.items[ititle]['catefory'] =  item.category.text.strip()
                self.items[ititle]['description'] = item.description.text.strip()

        self.cdate  = dt.strftime(dt.now(), _time)
        return self.items
