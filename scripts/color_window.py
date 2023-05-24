import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QColorDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")

        # Create a button to open the color dialog
        self.button = QPushButton("Change Color", self)
        self.button.clicked.connect(self.open_color_dialog)
        self.setCentralWidget(self.button)

    def open_color_dialog(self):
        color_dialog = QColorDialog(self)

        # Get the chosen color from the color dialog
        if color_dialog.exec_():
            color = color_dialog.selectedColor()

            # Set the background color of the button
            self.button.setStyleSheet(f"background-color: {color.name()};")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
