import itertools
import os
from bs4 import BeautifulSoup
from rel_to_abs_link import process_href


def process_file(fname):
    print 'processing {}'.format(fname)
    with open(fname) as f:
        soup = BeautifulSoup(f)

    rewrite_links(soup, fname)
    if 'course/entrance' in fname:
        fix_broken_image_links_on_entrance_page(soup)

    with open(fname, 'wb') as f:
        f.write(u'{}'.format(soup).encode('utf-8'))

def fix_broken_image_links_on_entrance_page(soup):
    ii = soup.find(alt='Interpret illustration')
    ii.attrs['src'] = '/_images/interpret.png'
    ci = soup.find(alt='Compile illustration')
    ci.attrs['src'] = '/_images/compile.png'

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
            script.attrs['src'] = process_href(script.attrs['src'], fname)


def html_files():
    for dirpath, dnames, fnames in os.walk('./build/thinkcspy/'):
        for f in fnames:
            if f.endswith('.html'):
                yield os.path.join(dirpath, f)


if __name__ == '__main__':
    map(process_file, html_files())
