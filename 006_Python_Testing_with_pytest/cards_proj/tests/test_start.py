import pytest
from cards import Card, InvalidCardId


@pytest.mark.parametrize("start_state", ["done", "in prog", "todo"])
def test_start(cards_db, start_state):
    c = Card("test start func", state=start_state)
    index = cards_db.add_card(c)
    cards_db.start(index)
    card = cards_db.get_card(index)
    assert card.state == "in prog"


# run using `pytest -v -m smoke`
@pytest.mark.smoke
def test_start_smoke(cards_db):
    """
    Start changes state from "todo" to "in prog"
    """
    i = cards_db.add_card(Card("foo", state="todo"))
    cards_db.start(i)
    c = cards_db.get_card(i)
    assert c.state == "in prog"


# run using `pytest -v -m exception`
@pytest.mark.exception
def test_start_non_existent(cards_db):
    """
    Shouldn't be able to start a non-existent card.
    """
    any_number = 123  # any number will be invalid, db is empty
    with pytest.raises(InvalidCardId):
        cards_db.start(any_number)
