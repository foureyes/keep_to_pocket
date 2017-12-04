import os
from bs4 import BeautifulSoup
from pocket import Pocket, PocketException

class Link:
    """Represents a link: link url, title, and tags
    """
    def __init__(self, s, importer=None):
        if importer:
            d = importer(s)
            self.title = d.get('title')
            self.link = d.get('link')
            self.tags = d.get('tags')
            self.description = d.get('description')

    def __str__(self):
        template = '[{title}]({link}) {tags}'
        return template.format(
                title=self.title, 
                link=self.link, 
                tags=','.join(self.tags)
        )

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def keep_html_import(s):
        soup = BeautifulSoup(s, 'html.parser')
        d = {}
        labels = soup.find_all(class_="label")
        d['tags'] = [label.get_text().strip() for label in labels]
        link = soup.find(class_="content")
        d['link'] = link.get_text().strip()
        title = soup.find(class_="title")
        d['title'] = title.get_text().strip() if title else d['link']
        return d


def create_and_init_link(fn):
    """Open an html file from google keep export and create a Link
    object
    """
    with open(fn, 'r') as f:
        try:
            link = Link(f.read(), importer=Link.keep_html_import)
        except UnicodeDecodeError as e:
            print('ERROR', fn)
            return None
        return link

def main():
    p = Pocket(
        # TODO: use configuration file... for now, just modify:
        consumer_key='',
        access_token=''
    )

    os.chdir('./Keep')
    dirs = os.listdir('.');
    links = [create_and_init_link(fn) for fn in dirs if fn[-4:] == 'html']
    count = 0
    for link in links:
        #add(url, title, tags
        if link.link:
            print(link)
            try:
                p.add(link.link, title=link.title, tags=','.join(link.tags))
            except Exception as e:
                print('Error', e)
                continue
            count += 1
    print('{} links imported out of {}'.format(count, len(links)))

main()
