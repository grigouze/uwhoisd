"""
A scraper which pulls zone WHOIS servers from IANA's root zone database.
"""

import sys
import time
import urlparse

import beautifulscraper


ROOT_ZONE_DB = 'http://www.iana.org/domains/root/db'
SLEEP = 0


def main():
    """
    Scrape IANA's root zone database and write the resulting configuration
    data to stdout.
    """
    print '[overrides]'

    scraper = beautifulscraper.BeautifulScraper()
    body = scraper.go(ROOT_ZONE_DB)

    no_server = []
    for link in body.select('#tld-table .tld a'):
        if 'href' not in link.attrs:
            continue

        time.sleep(SLEEP)

        zone_url = urlparse.urljoin(ROOT_ZONE_DB, link.attrs['href'])
        body = scraper.go(zone_url)

        title = body.find('h1')
        if title is None:
            continue
        title_parts = title.string.split('.', 1)
        if len(title_parts) != 2:
            continue
        ace_zone = title_parts[1].encode('idna').lower()

        whois_server_label = body.find('b', text='WHOIS Server:')
        whois_server = ''
        if whois_server_label is not None:
            whois_server = whois_server_label.next_sibling.strip().lower()

        if whois_server == '':
            no_server.append(ace_zone)
        else:
            print '%s=%s' % (ace_zone, whois_server)

    for ace_zone in no_server:
        print '; No record for %s' % ace_zone

    return 0


if __name__ == '__main__':
    sys.exit(main())
