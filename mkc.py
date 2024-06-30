from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QComboBox, QLabel, QLineEdit, QMessageBox
from PyQt6.QtCore import QEvent, QTimer
from customer_db_queries import *
from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtCore import QEvent , QTimer
from customer_db_queries import *
from PyQt5 import QtGui

class MyGUI(QMainWindow):
    
    def __init__(self, db: DATABASE):
        super().__init__()

        self.timer = QTimer()
        self.timer.setSingleShot(True)

        self.state = "add"
        self.db = db

        self.setWindowTitle("Customer Management")

        # Load UI from .ui file
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        self.C_id = QLabel("")
        self.C_name = QLineEdit()
        self.C_Ph_no = QLineEdit()
        self.C_pan_no = QLineEdit()
        self.C_pin = QLineEdit()

        self.C_name_dropdown = QComboBox()

        layout.addWidget(self.C_id)
        layout.addWidget(self.C_name)
        layout.addWidget(self.C_name_dropdown)
        layout.addWidget(self.C_Ph_no)
        layout.addWidget(self.C_pan_no)
        layout.addWidget(self.C_pin)

        self.addCustomerControls(layout)

        self.connectComboBox()
        self.connectButtons()

        self.show()
        self.C_id.setText(generateID(self.db))
        createTable(db)

        self.installEventFilters()

    def addCustomerControls(self, layout):
        self.Add_btn = QPushButton("Add")
        self.Edit_btn = QPushButton("Edit")
        self.Delete_btn = QPushButton("Delete")
        self.Update_btn = QPushButton("Update")
        self.Exit_btn = QPushButton("Exit")

        layout.addWidget(self.Add_btn)
        layout.addWidget(self.Edit_btn)
        layout.addWidget(self.Delete_btn)
        layout.addWidget(self.Update_btn)
        layout.addWidget(self.Exit_btn)

    def connectButtons(self):
        self.Add_btn.clicked.connect(self.HandleAddButton)
        self.Edit_btn.clicked.connect(self.HandleEditButton)
        self.Delete_btn.clicked.connect(self.HandleDeleteButton)
        self.Update_btn.clicked.connect(self.HandleUpdateButton)
        self.Exit_btn.clicked.connect(self.close)

    def connectComboBox(self):
        self.C_name.textChanged.connect(self.updateNameDropdown)
        self.C_name_dropdown.currentIndexChanged.connect(self.displayData)

    def updateNameDropdown(self):
        search_term = self.C_name.text().strip()
        self.C_name_dropdown.clear()

        if search_term:
            data = returnCustomerNames(self.db, search_term) # type: ignore
            if data:
                self.C_name_dropdown.addItems([row[1] for row in data])

    def HandleEditButton(self):
        self.state = "edit"
        self.editState()

    def HandleUpdateButton(self):
        if self.state != "edit":
            return

        name = self.C_name.text()
        ph_no = self.C_Ph_no.text()
        pan = self.C_pan_no.text()
        pin = self.C_pin.text()

        msg = updateValuesInDb(self.db, createDataDict(name, ph_no, pan, pin))
        showPopUp(msg)

        if msg == "values updated":
            self.clearForm()

    def HandleDeleteButton(self):
        if self.state != "edit":
            return

        msg = deleteCustomer(self.db, self.C_id.text())
        showPopUp(msg)

        if msg == "customer removed successfully":
            self.clearForm()

    def HandleAddButton(self):
        if self.state == "add":
            self.addCustomer()
        else:
            self.state = "add"
            self.addTransition()

    def addTransition(self):
        self.clearForm()
        self.C_id.setText(generateID(self.db))
        self.C_id.setReadOnly(True)
        self.C_name.setEnabled(False)
        self.C_name.setText("")
        self.C_name_dropdown.setEnabled(True)
        self.C_name_dropdown.setVisible(True)
        self.C_Ph_no.setEnabled(True)
        self.C_pan_no.setEnabled(True)
        self.C_pin.setEnabled(True)

    def addCustomer(self):
        name = self.C_name.text()
        ph_no = self.C_Ph_no.text()
        pan = self.C_pan_no.text()
        pin = self.C_pin.text()

        msg = insertValuesIntoDb(self.db, createDataDict(name, ph_no, pan, pin))
        showPopUp(msg)

        if msg == "values inserted":
            self.clearForm()

    def clearForm(self):
        self.C_id.setText(generateID(self.db))
        self.C_name.setText("")
        self.C_Ph_no.setText("")
        self.C_pan_no.setText("")
        self.C_pin.setText("")

    def editState(self):
        self.C_id.setReadOnly(False)

    def displayData(self):
        input_text = self.C_name_dropdown.currentText()
        data = returnCustomerData(self.db, input_text, checkID=False)

        if data:
            self.C_id.setText(data[0][0])
            self.C_name.setText(data[0][1])
            self.C_Ph_no.setText(data[0][2])
            self.C_pan_no.setText(data[0][3])
            self.C_pin.setText(data[0][4])
        else:
            self.clearForm()

    def installEventFilters(self):
        self.C_name.installEventFilter(self)
        self.C_name_dropdown.installEventFilter(self)
        self.C_id.installEventFilter(self)

    def eventFilter(self, source, event):
        if self.state == 'edit':
            if event.type() == QEvent.Type.FocusIn:
                if source == self.C_name or source == self.C_name_dropdown:
                    self.handleFocusIn(self.C_name_dropdown)
                elif source == self.C_id:
                    self.handleFocusIn(self.C_id)

            if event.type() == QEvent.Type.FocusOut:
                if source == self.C_name:
                    self.timer.singleShot(1000, self.checkNameFocusOut)
                elif source == self.C_id:
                    self.timer.singleShot(1000, self.checkIDFocusOut)

        return super().eventFilter(source, event)

    def checkNameFocusOut(self):
        if not (self.C_name.hasFocus() or self.C_name_dropdown.hasFocus()):
            self.handleFocusOut(self.C_name_dropdown)

    def checkIDFocusOut(self):
        if not self.C_id.hasFocus():
            self.handleFocusOut(self.C_id)

    def handleFocusIn(self, widget):
        widget.setEnabled(True)
        widget.setVisible(True)

    def handleFocusOut(self, widget):
        widget.setEnabled(False)
        widget.setVisible(False)


def createDataDict(name: str, ph: str, pan: str, pin: str) -> dict:
    return {
        "name": name,
        "phone_no": ph,
        "PAN": pan,
        "pincode": pin
    }

def showPopUp(msg: str):
    messageBox = QMessageBox()
    messageBox.setText(msg)
    messageBox.exec()

def main():
    db = connectDb()
    app = QApplication([])
    window = MyGUI(db)
    app.exec()
    db.close()

if __name__ == '__main__':
    main()
