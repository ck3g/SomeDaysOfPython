import cards
import shlex
from cards.cli import app
from typer.testing import CliRunner

runner = CliRunner()

expected = """\

  ID   state   owner   summary    
 ──────────────────────────────── 
  4    done            some task  
  5    done            a third"""


def cards_cli(command_string):
    command_list = shlex.split(command_string)
    result = runner.invoke(app, command_list)
    output = result.stdout.rstrip()
    return output


def test_done(cards_db):
    cards_db.add_card(cards.Card("some task", state="done"))
    cards_db.add_card(cards.Card("another"))
    cards_db.add_card(cards.Card("a third", state="done"))
    output = cards_cli("done")
    assert output.strip() == expected.strip()
