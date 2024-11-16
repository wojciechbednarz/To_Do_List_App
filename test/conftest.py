import pytest
from src.gui import ToDoGui


@pytest.fixture(scope="function")
def app(qtbot):
    gui = ToDoGui()
    qtbot.addWidget(gui)
    return gui


