from tests import utils


def test_whois():
    uwhois = utils.create_uwhois()
    expected = 'whois.markmonitor.com'
    transcript = utils.read_transcript('google.com.txt')
    # Make sure there's nothing wrong with the WHOIS transcript.
    assert transcript.count(expected) == 1
    assert uwhois.get_registrar_whois_server('com', transcript) == expected
    assert uwhois.get_whois_server('bz') == ('whois.afilias-grs.info', 43)
    assert uwhois.get_whois_server('anewone') == ('anewone.whois-servers.net',
                                                  43)
    assert uwhois.get_whois_server('org.za') == ('rwhois.org.za', 4321)
    assert uwhois.get_prefix('org.za') == 'domain '
