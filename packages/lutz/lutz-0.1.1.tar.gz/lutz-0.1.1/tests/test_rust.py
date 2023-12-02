from lutz import rust


def test_sum_as_string():
    res = rust.sum_as_string(1, 2)
    assert res == "3"
