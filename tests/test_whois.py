from tests import utils


def test_get_whois_server_prefix():
    uwhois = utils.create_uwhois()
    assert uwhois.get_whois_server('newzone') == ('newzone.whois-servers.net', 43)


def test_get_whois_server_overrides():
    uwhois = utils.create_uwhois()
    assert uwhois.get_whois_server('wtf') == ('whois.donuts.co', 43)


def test_get_whois_server_with_port():
    uwhois = utils.create_uwhois()
    assert uwhois.get_whois_server('org.za') == ('rwhois.org.za', 4321)


def test_get_prefix():
    uwhois = utils.create_uwhois()
    assert uwhois.get_prefix('net') == 'domain '


def test_get_prefix_empty():
    uwhois = utils.create_uwhois()
    assert uwhois.get_prefix('org') == ''
