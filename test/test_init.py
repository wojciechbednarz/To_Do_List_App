from PySide6 import QtWidgets
import pytest


@pytest.mark.basic
def test_main_window_title(app):
    assert app.windowTitle() == "ToDo App"


@pytest.mark.basic
def test_show_message_checkbox(app):
    assert app.show_message_checkbox is True


@pytest.mark.basic
def test_layout_exists(app):
    central_widget = app.centralWidget()
    assert isinstance(central_widget, QtWidgets.QWidget)

    layout = central_widget.layout()
    assert isinstance(layout, QtWidgets.QVBoxLayout)
