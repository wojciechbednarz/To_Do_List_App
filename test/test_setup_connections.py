from PySide6 import QtCore


# self.add_button.clicked.connect(self.create_items_to_do)
# self.remove_button.clicked.connect(self.remove_items_to_do
# self.text_input = QtWidgets.QLineEdit()


def test_setup_connections(app, qtbot):
    app.text_input.setText("Item1")
    # with qtbot.waitSignal(app.add_button.clicked, timeout=1000):
    #     app.create_items_to_do()
    qtbot.mouseClick(app.add_button, QtCore.Qt.MouseButton.LeftButton)

    assert app.items_to_do.count() == 1
    assert app.items_to_do.item(0).text() == "Item1"
