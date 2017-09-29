from bs4 import BeautifulSoup
import os


def rewrite_links(fname):
    print 're-writing links in {}'.format(fname)
    with open(fname) as f:
        soup = BeautifulSoup(f)

    for link in soup.find_all('a', class_='internal'):
        if '.html' not in link.attrs['href']:
            continue
        link.attrs['href'] = link.attrs['href'].replace('.html', '/')

    with open(fname, 'wb') as f:
        f.write(soup.prettify().encode('utf-8'))


def html_files():
    for dirpath, dnames, fnames in os.walk('./build/thinkcspy/'):
        for f in fnames:
            if f.endswith('.html'):
                yield os.path.join(dirpath, f)


if __name__ == '__main__':
    map(rewrite_links, html_files())
