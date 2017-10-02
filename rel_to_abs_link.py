import os

cases = [
    {
        'href': 'course/welcome',
        'fname': './build/thinkcspy/toc/index.html',
        'expected': '/course/welcome'
    },
    {
        'href': '../_static/livecode.css',
        'fname': './build/thinkcspy/Studios/yahtzee/index.html',
        'expected': '/_static/livecode.css'
    },
    {
        'href': '../_static/dragndrop.css',
        'fname': './build/thinkcspy/Studios/wagon-wheel/index.html',
        'expected': '/_static/dragndrop.css'
    },
    {
        'href': '../_static/basic.css',
        'fname': './build/thinkcspy/Studios/wagon-wheel.html',
        'expected': '/_static/basic.css'
    },
    {
        'href': '../_static/basic.css',
        'fname': './build/thinkcspy/Debugging/BeginningtipsforDebugging/index.html',
        'expected': '/_static/basic.css',
    },
]


def process_href(href, fname):
    important_part_of_fname = fname.replace('./build/thinkcspy', '')
    if fname != './build/thinkcspy/index.html':
        important_part_of_fname = important_part_of_fname.replace(
            '/index.html', '')
    directory, name = os.path.split(important_part_of_fname)
    return os.path.normpath(os.path.join(directory, href))


if __name__ == '__main__':
    for case in cases:
        assert process_href(case['href'], case['fname']) == case['expected'], (
            "Expected process_href('{}', '{}') to be '{}', got '{}'".format(
                case['href'],
                case['fname'],
                case['expected'],
                process_href(case['href'], case['fname']),
            ))
    print 'all tests pass'
