import itertools
import os
from bs4 import BeautifulSoup
from rel_to_abs_link import process_href


def process_file(fname):
    print 'processing {}'.format(fname)
    with open(fname) as f:
        soup = BeautifulSoup(f)

    rewrite_links(soup, fname)
    add_edit_this_page_link(soup, fname)
    if fname.endswith('save-my-spot.html'):
        fix_broken_image_links_on_entrance_page(soup)
        remove_nav_links(soup)
        include_iframe_on_entrance_page(soup)

    if fname.endswith('register.html'):
        remove_nav_links(soup)
        include_iframe_on_register_page(soup)

    with open(fname, 'wb') as f:
        f.write(u'{}'.format(soup).encode('utf-8'))

def add_edit_this_page_link(soup, fname):
    a = soup.find(class_='edit-this-page-link')
    if a is None:
        return

    a.attrs['href'] = (fname
        .replace('./build/thinkcspy', 'https://github.com/bgschiller/thinkcspy/tree/master/_sources')
        .replace('/index.html', '.rst')
        .replace('.html', '.rst'))

def fix_broken_image_links_on_entrance_page(soup):
    ii = soup.find(alt='Interpret illustration')
    ii.attrs['src'] = '/_images/interpret.png'
    ci = soup.find(alt='Compile illustration')
    ci.attrs['src'] = '/_images/compile.png'

def remove_nav_links(soup):
    for link in itertools.chain(
            soup.find_all(class_='navLink'),
            soup.find_all(class_='navLinkBg')):
        link.extract()

def include_iframe_on_register_page(soup):
    section = soup.find(id='register-for-coding-101')
    registration_iframe = BeautifulSoup('''
    <div>
        <iframe
            src="https://docs.google.com/forms/d/e/1FAIpQLSeaj_CyK2Fh2-5R5fO4MiJ8hIK_2L_rJRM0zNFUdQjhiYRtPA/viewform?embedded=true"
            width="100%"
            height="800px"
            frameborder="0"
        >
            Loading...
        </iframe>
    </div>
    ''')
    section.append(registration_iframe)


def include_iframe_on_entrance_page(soup):
    section = soup.find(id='quiz')
    quiz_iframe = BeautifulSoup('''
    <div>
        <iframe
            src="https://docs.google.com/forms/d/e/1FAIpQLSdMoTDxLQupF_1eKz6EDA8eYLaXr7LVc89Rdy_gQgw5Zs_9KA/viewform?embedded=true"
            frameborder="0"
            width="100%"
            height="1780px"
        >
            Loading...
        </iframe>
    </div>
    ''')
    section.append(quiz_iframe)

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
