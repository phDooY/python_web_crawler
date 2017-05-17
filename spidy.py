# coding=UTF-8
import argparse
import HTMLParser
import json
import re
import urllib


class MyHTMLParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.links = set()
        self.assets = set()

    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.
        if tag == "a":
            # Check the list of defined attributes.
            for name, value in attrs:
                # If href is defined, print it.
                if name == "href":
                    self.links.add(value)
        for name, value in attrs:
            if name == 'src':
                self.assets.add(value)

# Global variables to keep results from recursive main function
links_to_parse = []
links_parsed = []
result = []

parser = argparse.ArgumentParser(add_help=False,
                                 conflict_handler='resolve')
parser.add_argument('-s', '--subdomains',
                    help='Include subdomains while crawling.',
                    action='store_true')
parser.add_argument('-o', '--output',
                    help='Save output to file, specify filename.')
parser.add_argument('-u', '--url',
                    help='URL to start parsing from.')
parser.add_argument('-v', '--verbose',
                    help='Print number of URLs left to parse.',
                    action='store_true')
args = parser.parse_args()


def main(current_url=None):
    global links_to_parse
    global result

    if not current_url:

        if not args.url:
            raise KeyError('Please provide starting URL parameter -u'
                           ' when executing script.')

        current_url = args.url

    current_url = current_url.strip('/')

    if type(current_url) == unicode:
        current_url_for_open = current_url.encode('utf-8')
    else:
        current_url_for_open = current_url
    site = urllib.urlopen(current_url_for_open)
    encoding = site.headers.getparam('charset')
    site_html = site.read().decode(encoding) if encoding else site.read()

    # Getting path to filter out any 3rd party resources
    protocol, url_path = current_url.split('://')[:2]
    subdomain = url_path.split('/')[0]
    domain = '.'.join(subdomain.split('.')[-2:])
    domain_full_url = '://'.join([protocol, subdomain])
    pattern_domain = re.compile('^http(s)(.*?)\.{}'.format(domain))

    parser = MyHTMLParser()
    parser.feed(site_html)

    links_parsed.append(current_url)

    for link in list(parser.links):
        if not link:
            continue
        if len(link) <= 1:
            continue
        if link[0] == '/':
            full_link = domain_full_url + '/' + link.strip('/')
        # Filtering out 3rd party resources
        elif args.subdomains:
            if pattern_domain.search(link):
                link_url_path = link.split('://')[1]
                link_subdomain = link_url_path.split('/')[0]
                link_domain = '.'.join(link_subdomain.split('.')[-2:])
                if link_domain != domain:
                    continue
                full_link = link.strip('/')
            else:
                continue
        else:
            continue

        if full_link not in links_to_parse + links_parsed:
            links_to_parse.append(full_link)

    assets_list = [current_url + '/' + i.strip('/') for i in list(parser.assets)]

    result.append({
        'url': current_url,
        'assets': assets_list
    })

    try:
        next_url = links_to_parse.pop()
    except IndexError:
        data = json.dumps(
            result,
            indent=2,
            ensure_ascii=False).encode('utf8')
        if args.output:
            with open(args.output, 'w+') as f:
                f.write(data)
        exit()

    # For verbose STDOUT print
    if args.verbose:
        print 'url list length is {}'.format(str(len(links_to_parse)))

    main(next_url)


if __name__ == '__main__':
    main()
