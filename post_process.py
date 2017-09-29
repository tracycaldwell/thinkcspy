import itertools
import os
from bs4 import BeautifulSoup


def process_file(fname):
    print 'processing {}'.format(fname)
    with open(fname) as f:
        soup = BeautifulSoup(f)

    rewrite_links(soup)

    with open(fname, 'wb') as f:
        f.write(soup.prettify().encode('utf-8'))


def rewrite_links(soup):
    all_links = itertools.chain(
        soup.find_all('a', class_='internal'),
        soup.find_all('link'),
        soup.find_all('a', class_='navLinkBg'),
    )
    for link in all_links:
        if '.html' not in link.attrs['href']:
            continue
        link.attrs['href'] = link.attrs['href'].replace('.html', '')


def html_files():
    for dirpath, dnames, fnames in os.walk('./build/thinkcspy/'):
        for f in fnames:
            if f.endswith('.html'):
                yield os.path.join(dirpath, f)


if __name__ == '__main__':
    map(rewrite_links, html_files())
