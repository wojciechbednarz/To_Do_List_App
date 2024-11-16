import PySide6.QtWidgets
from PySide6.QtWidgets import QListWidgetItem, QLineEdit, QListWidget
from unittest import mock
import pytest
from packaging.version import parse


def test_qline_edit_text(app):
    expected_text = "Item"
    with mock.patch.object(QLineEdit, "text", return_value=expected_text) as MockQLineEdit:
        line_edit = QLineEdit()
        text = line_edit.text()

        MockQLineEdit.assert_called_once()
        assert expected_text == text, "QLineEdit.text did not return the expected value"


@pytest.mark.xfail()
def test_q_list_widget_item_creation(app):
    expected_text = "Item"
    with mock.patch('PySide6.QtWidgets.QListWidgetItem') as MockQListWidgetItem:
        MockQListWidgetItem.side_effect = lambda text: None
        item = QListWidgetItem(expected_text)

        # Ensure QListWidgetItem was created with the correct text
        MockQListWidgetItem.assert_called_once_with(expected_text)


def test_q_list_widget_add_item(app):
    expected_text = "Item"
    with mock.patch('PySide6.QtWidgets.QListWidgetItem') as MockQListWidgetItem:
        # Create a QListWidgetItem using the text from QLineEdit
        item = QListWidgetItem(expected_text)

        # Create a QListWidget and add the item
        items_to_do = QListWidget()
        items_to_do.addItem(item)

        # Check that the item was added correctly
        assert items_to_do.count() == 1, "Item was not added to the list"
        assert items_to_do.item(0).text() == expected_text, "Item text did not match"
