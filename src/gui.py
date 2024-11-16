import logging
import os
from PySide6 import QtCore, QtWidgets, QtGui
from src.app import add_task_from_gui


class ToDoGui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.show_message_checkbox = True
        self.setWindowTitle("ToDo App")
        self.setup_ui()
        self.setup_connections()
        QtWidgets.QWidget.setAcceptDrops(self, True)

    def add_widgets(self, widgets):
        for elem in widgets:
            if isinstance(elem, tuple):
                widget = elem[0]
                alignment = elem[1] if len(elem) > 0 else None
                if alignment is not None:
                    self.layout.addWidget(widget, alignment=alignment)
                else:
                    self.layout.addWidget(widget)
            else:
                self.layout.addWidget(elem)

    def set_item_and_priority_labels(self):
        item_priority_layout = QtWidgets.QHBoxLayout()
        item_label = QtWidgets.QLabel("Item")
        priority_label = QtWidgets.QLabel("Priority")
        item_priority_layout.addWidget(item_label)
        item_priority_layout.addWidget(priority_label)
        self.change_font_and_color(item_label, 12, "black")
        self.change_font_and_color(priority_label, 12, "black")
        self.layout.addLayout(item_priority_layout)

    def setup_ui(self):
        """Sets up the main UI components"""
        central_widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout()

        self.welcome = QtWidgets.QLabel('Welcome to the todo application!')
        self.welcome.setStyleSheet("color: black; font-size: 25px;")
        self.welcome.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.text_input = QtWidgets.QLineEdit()
        self.text_input.setPlaceholderText("Enter a new to-do item...")

        self.add_button = QtWidgets.QPushButton("Add to-do")
        self.remove_button = QtWidgets.QPushButton("Remove to-do")

        self.items_to_do = QtWidgets.QListWidget()
        self.items_to_do.setDragDropMode(QtWidgets.QListWidget.DragDropMode.InternalMove)

        self.about = QtWidgets.QMessageBox()

        self.change_font_and_color_for_elements()

        widgets = [(self.welcome, QtCore.Qt.AlignmentFlag.AlignTop), self.text_input, self.add_button,
                   self.remove_button]
        self.add_widgets(widgets)
        self.set_item_and_priority_labels()
        self.layout.addWidget(self.items_to_do)

        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        self.set_menu_bar()

    def change_font_and_color_for_elements(self):
        self.change_font_and_color(self.text_input, 14, "black")
        self.change_font_and_color(self.items_to_do, 14, "black")
        self.change_font_and_color(self.add_button, 10, "black")
        self.change_font_and_color(self.remove_button, 10, "black")

    @staticmethod
    def change_font_and_color(element, size, color):
        font = QtGui.QFont("Arial", size)
        font.setWeight(QtGui.QFont.Weight.Bold)
        element.setFont(font)
        element.setStyleSheet(f"color: {color}; background-color: #e6e6e6;")

    def setup_connections(self):
        """Connects UI actions to their respective slots"""
        self.add_button.clicked.connect(self.create_items_to_do)
        self.remove_button.clicked.connect(self.remove_items_to_do)

    def show_warning_message(self, message):
        if self.show_message_checkbox:
            error_msg = QtWidgets.QErrorMessage(self)
            error_msg.setWindowTitle("Warning")
            self.change_font_and_color(error_msg, 10, "black")
            error_msg.showMessage(message)
            error_msg.open()

    def set_prio_colors(self, priority_selector):
        priority = priority_selector.currentText()
        if priority == "High":
            self.change_font_and_color(priority_selector, 14, "red")
        elif priority == "Medium":
            self.change_font_and_color(priority_selector, 14, "yellow")
        elif priority == "Low":
            self.change_font_and_color(priority_selector, 14, "green")

    def prioritize_tasks(self, item):
        priority_widget = QtWidgets.QWidget()
        priority_layout = QtWidgets.QHBoxLayout(priority_widget)
        priority_layout.setContentsMargins(0, 0, 0, 0)

        task_checkbox = QtWidgets.QCheckBox(item.text())
        task_checkbox.stateChanged.connect(lambda: self.update_item_strike(task_checkbox))

        priority_selector = QtWidgets.QComboBox()
        priority_selector.addItems(["High", "Medium", "Low"])
        self.set_prio_colors(priority_selector)
        priority_selector.currentIndexChanged.connect(lambda: self.set_prio_colors(priority_selector))

        priority_layout.addWidget(task_checkbox)
        priority_layout.addWidget(priority_selector)
        self.items_to_do.setItemWidget(item, priority_widget)

    @QtCore.Slot()
    def create_items_to_do(self):
        text = self.text_input.text().strip()
        if text:
            item = QtWidgets.QListWidgetItem(text)
            self.items_to_do.addItem(item)
            self.text_input.clear()
            add_task_from_gui(text)
            self.prioritize_tasks(item)
        else:
            self.show_warning_message("Please enter item to do!")

    @QtCore.Slot()
    def add_items_from_file(self):
        try:
            file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, "Select a File", "", "Text Files (*.txt);;All Files (*)"
            )
            if file_path and os.stat(file_path).st_size > 0:
                with open(file_path, "r") as txt_file:
                    for line in txt_file:
                        item = QtWidgets.QListWidgetItem(line.strip())
                        self.items_to_do.addItem(item)
                        add_task_from_gui(line.strip())
                        self.text_input.clear()
                        self.prioritize_tasks(item)
            else:
                self.show_warning_message("Please enter item to do!")
        except FileNotFoundError:
            logging.error("Selected file does not exist.")
        except Exception as e:
            logging.error("An error has occurred during file loading: %s", e)

    @QtCore.Slot()
    def update_item_strike(self, item):
        """Updates the font to show strikethrough if checkbox is checked."""
        font = item.font()
        font.setStrikeOut(item.isChecked())
        item.setFont(font)

    @QtCore.Slot()
    def hide_checked_items(self, item):
        if item.checkState() == QtCore.Qt.CheckState.Checked:
            item.setHidden(True)

    @QtCore.Slot()
    def remove_items_to_do(self):
        selected_items = self.items_to_do.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            row = self.items_to_do.row(item)
            self.items_to_do.takeItem(row)

    def set_about_info(self):
        self.about.setWindowTitle("About Application")
        self.about.setText("This application version 1.0\nCreated by Wojciech Bednarz")
        self.about.setIcon(QtWidgets.QMessageBox.Icon.Information)
        self.about.open()
        self.layout.addWidget(self.about)

    @QtCore.Slot()
    def set_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        open_action = QtGui.QAction("Open", self)
        exit_action = QtGui.QAction("Exit", self)
        file_menu.addAction(open_action)
        file_menu.addAction(exit_action)

        exit_action.triggered.connect(self.close)
        open_action.triggered.connect(self.add_items_from_file)

        help_menu = menu_bar.addMenu("Help")
        about_action = QtGui.QAction("About", self)
        about_action.triggered.connect(self.set_about_info)
        help_menu.addAction(about_action)
