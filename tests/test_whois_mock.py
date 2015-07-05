from tests.fixtures.whois import FixtureWhois
from tests import utils


class TestWhoisMock(FixtureWhois):

    def test_whois_mock(self):
        domain = 'domaintest.net'
        uwhois = utils.create_uwhois_mock_whois_server_port()
        assert 'Domain Name: %s' % domain in uwhois.whois(domain)
