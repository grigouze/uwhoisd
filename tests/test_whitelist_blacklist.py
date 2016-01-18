from tests import utils


DEFAULT_CONFIG = """
[uwhoisd]
iface=0.0.0.0
bind=0.0.0.0
port=4343
registry_whois=false
suffix=whois-servers.net
conservative=

[overrides]

[prefixes]

[recursion_patterns]

[ratelimit]
whitelist=
    %s
blacklist=
    %s
req_number=1
req_interval=1
"""


def _make_test(ip_to_test, listed):
    uwhois = utils.create_uwhois(default_config=DEFAULT_CONFIG % (listed, listed))
    assert uwhois.ip_whitelisted(ip_to_test) is True
    assert uwhois.ip_blacklisted(ip_to_test) is True


def test_white_black_listed_simple():
    ip_to_test = listed = '127.0.0.1'
    _make_test(ip_to_test, listed)


def test_white_black_listed_wilcard():
    ip_to_test = '127.0.0.1'
    listed = '127.0.0.*'
    _make_test(ip_to_test, listed)


def test_white_black_listed_range():
    ip_to_test = '127.0.0.1'
    listed = '126-127.0.0.1'
    _make_test(ip_to_test, listed)


def test_white_black_listed_enum():
    ip_to_test = '127.0.0.1'
    listed = '126,127.0.0.1'
    _make_test(ip_to_test, listed)


def test_white_black_listed_all_in_one():
    ip_to_test = '127.0.0.1'
    listed = '126,127.*.0.0-1'
    _make_test(ip_to_test, listed)


def test_ip_check_whitelist_true():
    ip_to_test = listed = '127.0.0.1'

    uwhois = utils.create_uwhois(default_config=DEFAULT_CONFIG % (listed, listed))
    assert uwhois.ip_check(ip_to_test) is True


def test_ip_check_blacklist_true():
    ip_to_test = '127.0.0.1'
    listed1 = '127.0.0.2'
    listed2 = '127.0.0.1'

    uwhois = utils.create_uwhois(default_config=DEFAULT_CONFIG % (listed1, listed2))

    try:
        uwhois.ip_check(ip_to_test)
    except ValueError as err:
        assert err.message == '# Your IP has been blacklisted due to abusive access'


def test_ip_check_ratelimit_true():
    ip_to_test = '127.0.0.1'
    listed = '127.0.0.2'

    uwhois = utils.create_uwhois(default_config=DEFAULT_CONFIG % (listed, listed))
    uwhois.ip_check(ip_to_test)
