def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1


def test_is_instance():
    assert isinstance("this is a string", str)
    assert not isinstance("10", int)


def test_booleans():
    validated = True
    assert validated is True
    assert ("hello" == "world") is False


def test_types():
    assert type("Hello" is str)
    assert type("world" is not int)
