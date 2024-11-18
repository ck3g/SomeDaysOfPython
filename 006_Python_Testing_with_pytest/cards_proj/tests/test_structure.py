from cards import Card

# Structure tests in the following way:
# Arrange-Act-Assert
# or
# Given-When-Then
#
# That helps separate tests into stages:
#   * Getting ready to do something
#   * Doing something
#   * Checking to see if it worked


def test_to_dict():
    # GIVEN(Arrange) a Card object with known contents
    c1 = Card("something", "brian", "todo", 123)

    # WHEN(Act) we call to_doct() on the object
    c2 = c1.to_dict()

    # THEN(Assert) the result will be a dictionary with known content
    c2_expected = {
        "summary": "something",
        "owner": "brian",
        "state": "todo",
        "id": 123,
    }
    assert c2 == c2_expected
