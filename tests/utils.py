"""
Utility functions for testing.
"""

from os import path

import uwhoisd
from uwhoisd.utils import make_config_parser


HERE = path.dirname(__file__)


def create_uwhois(default_config=None):
    """Prepare a UWhois object for testing."""
    if default_config is None:
        config = path.join(HERE, '..', 'extra', 'uwhoisd.ini')
        parser = make_config_parser(uwhoisd.CONFIG, config)
    else:
        parser = make_config_parser(default_config, '')

    uwhois = uwhoisd.UWhois()
    uwhois.read_config(parser)
    return uwhois


def read_transcript(name):
    """Read a WHOIS transcript file."""
    with open(path.join(HERE, 'transcripts', name), 'r') as fh:
        return fh.read()
