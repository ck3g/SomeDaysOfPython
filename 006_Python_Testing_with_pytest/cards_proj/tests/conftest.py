import pytest
import cards


def pytest_addoption(parser):
    parser.addoption(
        "--func-db",
        action="store_true",
        default=False,
        help="new db for each test",
    )


def db_scope(fixture_name, config):
    if config.getoption("--func-db", None):
        return "function"

    return "session"


# # Old example without using builtin fixtures
# from pathlib import Path
# from tempfile import TemporaryDirectory
# @pytest.fixture(scope=db_scope)
# def db():
#     """CardsDB object connected to a temporary database."""
#     with TemporaryDirectory() as db_dir:
#         db_path = Path(db_dir)
#         db_ = cards.CardsDB(db_path)
#         yield db_
#         db_.close()


@pytest.fixture(scope="session")
def db(tmp_path_factory):
    """CardsDB object connected to a temporary database"""
    db_path = tmp_path_factory.mktemp("cards_db")
    db_ = cards.CardsDB(db_path)
    yield db_
    db_.close()


@pytest.fixture(scope="function")
def cards_db(db):
    """CardsDB object that's empty"""
    db.delete_all()
    return db


@pytest.fixture(scope="session")
def some_cards():
    """List of different Card objects"""
    return [
        cards.Card("write book", "Brian", "done"),
        cards.Card("edit book", "Katie", "done"),
        cards.Card("write 2nd edition", "Brian", "todo"),
        cards.Card("edit 2nd edition", "Katie", "todo"),
    ]


# Fixtures can use other fixtures
@pytest.fixture(scope="function")
def non_empty_db(cards_db, some_cards):
    """CardsDB object that's been populated with 'some cards'"""
    for c in some_cards:
        cards_db.add_card(c)

    return cards_db
