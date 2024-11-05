from gui import ToDoGui
from PySide6 import QtWidgets
import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    my_widget = ToDoGui()
    my_widget.resize(800, 600)
    my_widget.show()

    sys.exit(app.exec())
