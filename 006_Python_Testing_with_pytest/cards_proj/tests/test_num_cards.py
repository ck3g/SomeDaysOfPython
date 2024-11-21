import pytest
from cards import Card


@pytest.fixture(scope="function")
def cards_db_three_cards(db):
    db_ = db
    # start with empty
    db_.delete_all()
    # add three cards
    db_.add_card(Card("Learn something new"))
    db_.add_card(Card("Buuld useful tools"))
    db_.add_card(Card("Teach others"))
    return db_


def test_zero_card(cards_db):
    assert cards_db.count() == 0


def test_three_cards(cards_db_three_cards):
    cards_db = cards_db_three_cards
    assert cards_db.count() == 3


def test_no_marker(cards_db):
    assert cards_db.count() == 0


@pytest.mark.num_cards
def test_marker_with_no_param(cards_db):
    assert cards_db.count() == 0


@pytest.mark.num_cards(3)
def test_three_cards_with_marker(cards_db):
    assert cards_db.count() == 3
    # just for fun, let's look at the cards Faker made for us
    print()
    for c in cards_db.list_cards():
        print(c)


@pytest.mark.num_cards(10)
def test_ten_cards(cards_db):
    assert cards_db.count() == 10
