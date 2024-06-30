from PyQt6.QtWidgets import *
from PyQt6 import uic

from customer_db_queries import *


class MyGUI(QMainWindow):
    
    def __init__(self, db : DATABASE):
        super(MyGUI, self).__init__()
        uic.loadUi("prototype.ui", self)

        self.state = "add"

        self.show()

        self.db = db
        self.C_id.setText(generateID(self.db))
        createTable(db)

        self.connectButtons()
        self.addTransition()

    def connectButtons(self):
        self.Add_btn.clicked.connect(self.HandleAddButton)
        self.Edit_btn.clicked.connect(self.HandleEditButton)
        self.Delete_btn.clicked.connect(self.HandleDeleteButton)
        self.Update_btn.clicked.connect(self.HandleUpdateButton)
        self.Exit_btn.clicked.connect(exit)

    def HandleEditButton(self):
        self.state = "edit"
        self.editState()

    def HandleUpdateButton(self):
        if self.state == "edit":
            pass

    def HandleDeleteButton(self):
        if self.state == "edit":
            pass

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
    
        '''
        insert the customer
        '''
        name=self.C_name.text()
        ph_no=self.C_Ph_no.text()
        pan=self.C_pan_no.text()
        pin=self.C_pin.text()

        msg=insertValuesIntoDb(self.db, createDataDict(name, ph_no, pan, pin))
        message=QMessageBox()
        message.setText(msg)
        message.exec()

        if msg == "values inserted":
            self.clear()


    def clearForm(self):
        '''
        clear the form
        '''
        self.C_id.setText(generateID(self.db))
        self.C_name.setText("")
        self.C_Ph_no.setText("")
        self.C_pan_no.setText("")
        self.C_pin.setText("")

    
    # def delete(self):
    #     '''
    #     deletes the customer
    #     '''


    def editState(self):
        '''
        edit the customer
        '''
        self.C_id.setReadOnly(False)
        self.C_id.setText("")
        if self.C_name.hasFocus():
            self.C_name_dropdown.setEnabled(True)
            self.C_name_dropdown.setVisible(True)
            data = returnCustomerData(self.db, "", checkID=False)
            self.C_name_dropdown.clear()  # Clear existing items
            self.C_name_dropdown.addItems([row[1] for row in data])
        else:
            self.C_name_dropdown.setEnabled(False)
            self.C_name_dropdown.setVisible(False)

        if self.C_id.hasFocus():
            self.C_id_dropdown.setEnabled(True)
            self.C_id_dropdown.setVisible(True)
            data = returnCustomerData(self.db, "", checkID=True)
            self.C_id_dropdown.clear()  # Clear existing items
            self.C_id_dropdown.addItems([row[0] for row in data])
        else:
            self.C_id_dropdown.setEnabled(False)
            self.C_id_dropdown.setVisible(False)
    

    # def update(self):
    #     '''
    #     update the customer
    #     '''
        

        
def createDataDict(name : str , ph : str , pan : str, pin : str) -> dict:
    data = {
        "name" :name,
        "phone_no" :ph ,
        "PAN" :pan,
        "pincode" :pin
    }
    return data

def main():
    db = connectDb()

    app = QApplication([])
    window = MyGUI(db)

    app.exec()
    db.close()


if __name__ == '__main__':
    main()
