from PySide6 import QtWidgets
from unittest import mock


def test_add_items_from_file(app, mocker):
    mocker.patch.object(QtWidgets.QFileDialog, "getOpenFileName", return_value=("test.txt", "Text Files (*.txt)"))

    mock_open = mocker.patch("builtins.open", mock.mock_open(read_data="Item1\nItem2\nItem3"))
    mocker.patch("os.stat", return_value=mock.Mock(st_size=10))

    app.add_items_from_file()

    assert app.items_to_do.count() == 3
    assert app.items_to_do.item(0).text() == "Item1"
    assert app.items_to_do.item(1).text() == "Item2"
    assert app.items_to_do.item(2).text() == "Item3"

    # Verify that file was opened and read
    mock_open.assert_called_once_with("test.txt", "r")
