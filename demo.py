from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtCore import QEvent , QTimer
from customer_db_queries import *
from PyQt5 import QtGui
 

class MyGUI(QMainWindow):
    
    def __init__(self, db: DATABASE):
        super(MyGUI, self).__init__()
        uic.loadUi("prototype.ui", self)

        
        self.timer = QTimer()
        self.timer.setSingleShot(True)

        self.state = "add"
        self.db = db

        self.show()
        self.C_id.setText(generateID(self.db))
        createTable(db)

        self.connectButtons()
        self.addTransition()
        self.installEventFilters()
        self.connectComboBox()

    def connectButtons(self):
        self.Add_btn.clicked.connect(self.HandleAddButton)
        self.Edit_btn.clicked.connect(self.HandleEditButton)
        self.Delete_btn.clicked.connect(self.HandleDeleteButton)
        self.Update_btn.clicked.connect(self.HandleUpdateButton)
        self.Exit_btn.clicked.connect(exit)

    def connectComboBox(self):
        self.C_name_dropdown.currentIndexChanged.connect(self.displayData)

    def HandleEditButton(self):
        self.state = "edit"
        self.editState()

    def HandleUpdateButton(self):
        if not self.state == "edit":
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
        if not self.state == "edit":
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
        self.C_name_dropdown.setEnabled(False)
        self.C_name_dropdown.setVisible(False)
        self.C_id_dropdown.setEnabled(False)
        self.C_id_dropdown.setVisible(False)

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
        self.C_id.setText("")

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
            # Handle case where no data is found
            self.C_id.setText("")
            self.C_name.setText("")
            self.C_Ph_no.setText("")
            self.C_pan_no.setText("")
            self.C_pin.setText("")

    def displayDataId(self):
        curr_index=self.C_id_dropdown.currentIndex()
        data = returnCustomerData(self.db, self.C_id_dropdown.currentText(), checkID=True)
        # else:
        #     data = returnCustomerData(self.db, widget.itemText(index), checkID=True) 
        # print(index)
        # print(widget.itemText(index))

        # print(data)
            
        self.C_id.setText(data[0][0])
        self.C_name.setText(data[0][1])
        self.C_Ph_no.setText(data[0][2])
        self.C_pan_no.setText(data[0][3])
        self.C_pin.setText(data[0][4])

    def installEventFilters(self):
        self.C_name.installEventFilter(self)
        self.C_name_dropdown.installEventFilter(self)
        self.C_id.installEventFilter(self)
        self.C_id_dropdown.installEventFilter(self)

    def eventFilter(self, source, event):
        if self.state == 'edit':
            if event.type() == QEvent.Type.FocusIn:
                if source == self.C_name or source == self.C_name_dropdown:
                    self.C_name_dropdown.clear()
                    self.C_name_dropdown.addItems([row[1] for row in returnCustomerData(self.db, self.C_name.text(), checkID=False)])
                    self.handleFocusIn(self.C_name_dropdown)
                elif source == self.C_id or source == self.C_id_dropdown:
                    self.C_id_dropdown.clear()
                    self.C_id_dropdown.addItems([row[0] for row in returnCustomerData(self.db, self.C_id.text(), checkID=True)])
                    self.handleFocusIn(self.C_id_dropdown)

            if event.type() == QEvent.Type.FocusOut:
                if source == self.C_name or source == self.C_name_dropdown:
                    self.timer.singleShot(1000,  self.checkNameFocusOut)
                elif source == self.C_id or source == self.C_id_dropdown:
                    self.timer.singleShot(1000, self.checkIDFocusOut)
            

            # if event.type() == QEvent.Type.MouseButtonPress:
            #     if source == self.C_name_dropdown:
            #          self.C_name_dropdown.currentIndexChanged.connect(lambda : self.displayDataName( self.C_name_dropdown.currentIndex()))
            #         # self.displayData(self.C_name_dropdown)
            #     if source == self.C_id_dropdown:
            #         self.C_id_dropdown.currentIndexChanged.connect(self.displayDataId)

            # if event.type() == QEvent.Type.KeyPress:
            #         if source == self.C_name:
            #             self.C_name_dropdown.clear()
            #             self.C_name_dropdown.addItems([row[1] for row in returnCustomerData(self.db, self.C_name.text(), checkID=False)])
            #             self.handleFocusIn(self.C_name_dropdown)
                            
            #         if source == self.C_id:
            #             self.C_id_dropdown.clear()
            #             self.C_id_dropdown.addItems([row[0] for row in returnCustomerData(self.db, self.C_id.text(), checkID=True)])
            #             self.handleFocusIn(self.C_id_dropdown)  
                    
        return super().eventFilter(source, event)
    
    def checkNameFocusOut(self):
        if not (self.C_name.hasFocus() or self.C_name_dropdown.hasFocus):
            self.handleFocusOut(self.C_name_dropdown)
    
    def checkIDFocusOut(self):
        if not (self.C_id.hasFocus() or self.C_id_dropdown.hasFocus):
            self.handleFocusOut(self.C_id_dropdown)

    def handleFocusIn(self, widget : QWidget) -> None:
        widget.setEnabled(True)
        widget.setVisible(True)

    def handleFocusOut(self, widget : QWidget):
        widget.setEnabled(False)
        widget.setVisible(False)

def createDataDict(name: str, ph: str, pan: str, pin: str) -> dict:
    return {
        "name": name,
        "phone_no": ph,
        "PAN": pan,
        "pincode": pin
    }

def showPopUp(msg : str) -> None:
    messageBox = QMessageBox()
    messageBox.setText(msg)
    messageBox.exec()

def main():
    db = connectDb()

    app = QApplication([])
    
    windo=QWidget()
    
    window = MyGUI(db)

    app.exec()
    db.close()

if __name__ == '__main__':
    main()