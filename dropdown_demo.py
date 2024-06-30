from PyQt6.QtWidgets import QApplication, QFrame, QPushButton, QVBoxLayout, QScrollArea, QWidget
from PyQt6.QtCore import Qt
import sys

class MainWindow(QFrame):
    def __init__(self, width: int = 500, height: int = 20):
        super().__init__()

        self.buttonWidth: int = width
        self.buttonHeight: int = height

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # Create a widget to hold the buttons
        self.buttonContainer = QWidget()
        self.buttonLayout = QVBoxLayout(self.buttonContainer)

        for i in range(1, 21):
            self.addButton(f"button {i}")

        self.buttonContainer.setLayout(self.buttonLayout)

        # Create a scroll area
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.buttonContainer)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Add the scroll area to the main layout
        self.layout.addWidget(self.scrollArea)

        self.setLayout(self.layout)

        # Adjust the maximum size
        self.maxLayoutSize()

    def addButton(self, placeHolder: str):
        button = QPushButton(placeHolder)
        button.setFixedSize(self.buttonWidth, self.buttonHeight)
        self.buttonLayout.addWidget(button)

    def clearLayout(self):
        while self.buttonLayout.count():
            child = self.buttonLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def maxLayoutSize(self):
        if self.buttonLayout.count() <= 5:
            self.setFixedHeight(self.buttonHeight * self.buttonLayout.count())
        else:
            self.setFixedHeight(self.buttonHeight * 5)

        self.setFixedWidth(self.buttonWidth)

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
