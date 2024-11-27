import pytest
from cards import Card


@pytest.mark.parametrize(
    "starting_card",
    [
        Card("foo", state="todo"),
        Card("foo", state="in prog"),
        Card("foo", state="done"),
    ],
)
def test_card(cards_db, starting_card):
    index = cards_db.add_card(starting_card)
    cards_db.finish(index)
    card = cards_db.get_card(index)
    assert card.state == "done"


card_list = [
    Card("foo", state="todo"),
    Card("foo", state="in prog"),
    Card("foo", state="done"),
]


@pytest.mark.parametrize("starting_card", card_list, ids=str)
def test_id_str(cards_db, starting_card):
    index = cards_db.add_card(starting_card)
    cards_db.finish(index)
    card = cards_db.get_card(index)
    assert card.state == "done"


def card_state(card):
    return card.state


@pytest.mark.parametrize("starting_card", card_list, ids=card_state)
def test_id_func(cards_db, starting_card):
    index = cards_db.add_card(starting_card)
    cards_db.finish(index)
    card = cards_db.get_card(index)
    assert card.state == "done"


@pytest.mark.parametrize("starting_card", card_list, ids=lambda c: c.state)
def test_id_lambda(cards_db, starting_card):
    index = cards_db.add_card(starting_card)
    cards_db.finish(index)
    card = cards_db.get_card(index)
    assert card.state == "done"


c_list = [
    Card("foo", state="todo"),
    pytest.param(Card("foo", state="in prog"), id="special"),
    Card("foo", state="done"),
]


@pytest.mark.parametrize("starting_card", c_list, ids=card_state)
def test_id_param(cards_db, starting_card):
    index = cards_db.add_card(starting_card)
    cards_db.finish(index)
    card = cards_db.get_card(index)
    assert card.state == "done"
