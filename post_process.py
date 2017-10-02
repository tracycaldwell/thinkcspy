import itertools
import os
from bs4 import BeautifulSoup
from rel_to_abs_link import process_href


def process_file(fname):
    print 'processing {}'.format(fname)
    with open(fname) as f:
        soup = BeautifulSoup(f)

    rewrite_links(soup, fname)

    with open(fname, 'wb') as f:
        f.write(soup.prettify().encode('utf-8'))


def rewrite_links(soup, fname):
    all_links = itertools.chain(
        soup.find_all('a', class_='internal'),
        soup.find_all('link'),
        soup.find_all('a', class_='navLinkBg'),
        soup.select('.navLink a'),
    )
    for link in all_links:
        href = link.attrs['href'].replace('.html', '')
        if not href.startswith('/'):
            print dict(href=href, fname=fname, expected=process_href(href, fname))
            href = process_href(href, fname)
        link.attrs['href'] = href

    scripts = itertools.chain(
        soup.find_all('script'),
        soup.find_all('img'),
    )
    for script in scripts:
        if 'src' not in script.attrs:
            continue
        if not script.attrs['src'].startswith('/'):
            print dict(href=script.attrs['src'], fname=fname, expected=process_href(script.attrs['src'], fname))
            script.attrs['src'] = process_href(script.attrs['src'], fname)


def html_files():
    for dirpath, dnames, fnames in os.walk('./build/thinkcspy/'):
        for f in fnames:
            if f.endswith('.html'):
                yield os.path.join(dirpath, f)


if __name__ == '__main__':
    map(process_file, html_files())
