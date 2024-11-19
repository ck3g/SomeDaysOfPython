# tmp_path fixture is function scope
def test_tmp_path(tmp_path):
    file = tmp_path / "file.txt"
    file.write_text("Hello")
    assert file.read_text() == "Hello"


# tmp_path_factory fixture is session scope
def test_tmp_path_factory(tmp_path_factory):
    path = tmp_path_factory.mktemp("sub")
    file = path / "file.txt"
    file.write_text("Hello")
    assert file.read_text() == "Hello"
