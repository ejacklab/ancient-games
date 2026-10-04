from calc import total


def test_empty():
    assert total([]) == 0


def test_one():
    assert total([5]) == 5


def test_many():
    assert total([5, 7, 11]) == 23
