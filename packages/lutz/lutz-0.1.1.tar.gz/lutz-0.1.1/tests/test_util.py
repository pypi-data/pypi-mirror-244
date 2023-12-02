from lutz import util


def test_fortunes():
    res = util.get_fortune()
    assert len(res) > 0
