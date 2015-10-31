from uwhoisd.utils import ip_to_regexp


def test_charwith_point():
    ip = 'bla bla.bla'

    assert ip_to_regexp(ip) == '^bla bla\.bla$'


def test_char_without_point():
    ip = 'bla bla bla'

    assert ip_to_regexp(ip) == '^bla bla bla$'


def test_simple():
    ip = '1.1.1.1'

    assert ip_to_regexp(ip) == '^1\.1\.1\.1$'


def test_wildcard():
    ip = '1.1.1.*'

    assert ip_to_regexp(ip) == '^1\.1\.1\.\d+$'


def test_range():
    ip = '1.1.1-5.1'

    assert ip_to_regexp(ip) == '^1\.1\.(?:1|2|3|4|5)\.1$'


def test_enum():
    ip = '1.1.1,3.1'

    assert ip_to_regexp(ip) == '^1\.1\.(?:1|3)\.1$'


def test_all_in_one():
    ip = '1.*.1,4.12-19'

    assert ip_to_regexp(ip) == '^1\.\d+\.(?:1|4)\.(?:12|13|14|15|16|17|18|19)$'
