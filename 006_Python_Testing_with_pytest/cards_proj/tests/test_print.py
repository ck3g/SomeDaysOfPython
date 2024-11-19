# run `pytest -s tests/test_print.py::test_normal` to see the output
def test_normal():
    print("\nnormal print")


# run `pytest tests/test_print.py::test_disabled` to see the output
# will print text even without -s flag
def test_disabled(capsys):
    with capsys.disabled():
        print("\ncapsys disabled print")
